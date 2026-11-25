#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVE DE CALIBRAGE DE LA MÉTHODE DES 30 % (ARBITRAGE du 14-11-2026, étape 6, correction C6) — Simulation uniquement.
Mercredi 25-11-2026.

LE SENS EN TÊTE — Au regard unique sur les 30 %, m versions d'une famille sont jugées ensemble, et le contrôle ⑤
(« le gain bat zéro ») se décide par `MODULE_JUGEMENT.romano_wolf_du_gain`, qui promet : « si aucune version n'a de
talent, je n'en validerai au moins une qu'au plus une fois sur 1 ÷ seuil ». Cette promesse n'est prouvée qu'en grand
échantillon (Romano et Wolf 2005). Ce programme la MESURE à nos tailles (50 à 250 opérations par version), avec des
gains dissymétriques (+1/−3) et des opérations LIÉES PAR PAQUETS — c'est là que la contre-expertise du 14-11-2026 a
mesuré 10 à 17 % au lieu de 5 % pour un écart-type ordinaire (C6 : « c'est là qu'elle peut rougir »). L'arbitre exige un
risque ≤ 2,5 % par famille ; s'il est dépassé, on studentise autrement (variance robuste à la dépendance) et on relance.
Données FABRIQUÉES : formes de gains écrites ici, dates fictives à partir du 2024-01-01 ; aucun cours n'est lu, et
surtout aucune année de 2000 à 2023.

USAGE : python3 -B programmes/CALIBRER_LA_METHODE_DES_30.py <racine> [mondes par case, défaut 1000] [seuil]
CODE : 0 si chaque case EXIGÉE tient le seuil ; 1 si l'une le dépasse de façon démontrée ; 2 si une donnée manque, si
un argument est faux ou si une case n'a pas pu se mesurer (R-734).

① RÔLE — Mesurer le taux de familles « sans talent » où au moins une version est validée à tort, et sortir non nul
  s'il dépasse le seuil promis.
② CONTEXTE D'APPEL — Avant tout regard sur des années d'examen d'une famille (étape 6 de l'ARBITRAGE), et après toute
  modification de `romano_wolf_du_gain`. Trop long pour la machine du Chat : joué sur GitHub, code `CalibrageDes30`
  de `tests/LANCEMENT_DES_EPREUVES.json` (« epreuves_longues »). Les épreuves rapides, dont les dents de ce calibrage
  (E8), vivent dans `tests/EPREUVES_DE_LA_METHODE_DES_30_Mer_25-11-2026.py`.
③ ENTRÉE — La racine du dépôt ; facultatifs : le nombre de mondes par case (entier ≥ 50), le seuil (dans ]0, 0,5[ ;
  par défaut `MODULE_JUGEMENT.SEUIL_PAR_FAMILLE_DEFAUT`, dont la valeur revient à Jean-Luc).
④ CONDITIONS D'ENTRÉE — Sous la racine : `programmes/MODULE_JUGEMENT.py` et `programmes/CALIBRER_LE_HASARD_DES_GAINS.py`.
  Sinon code 2.
⑤ SORTIE — Le code de sortie dit en « CODE ». À l'écran : une ligne par case (taux mesuré, verdict), le verdict d'ensemble.
  [rend: 1]
⑥ TRAITEMENT — ① lire les arguments · ② pour chaque forme, chaque taille, chaque liaison et chaque ressemblance :
  fabriquer des familles sans talent (`fabriquer_une_famille`), les juger par `romano_wolf_du_gain`, compter
  (`mesurer_le_risque`) · ③ juger chaque case exigée (`verdict_d_une_case`) · ④ rendre le code.
⑦ UNITÉ — Gains en EUROS pour 100 000 € par opération ; jours de CALENDRIER ; taux sans unité.
⑧ POURQUOI — Une promesse de risque se mesure, elle ne se suppose pas (même principe que
  `programmes/CALIBRER_LE_HASARD_DES_GAINS.py`, qui calibre une version seule ; ici, une FAMILLE). La ressemblance
  0,96 est celle de deux versions à un cran de réglage (méthode « au carré », §A.4) ; le maximum de Romano et Wolf doit
  en tenir compte sans dépasser son seuil.
⑨ CE QUI CLOCHE — ① Monde stylisé : copule normale par paquets ; un krach réel peut lier autrement. ② Le régime
  persistant (0,8 d'un paquet au suivant) est AFFICHÉ, non exigé : aucune méthode qui ne regarde qu'une période ne voit
  un régime aussi long qu'elle (`probabilite_que_le_gain_soit_du_hasard`, ⑨ ①). ③ « Dépasse de façon démontrée » est
  un test binomial unilatéral à 0,001 : un dépassement léger peut passer inaperçu à 1 000 mondes. ④ Le contrôle ⑥
  (Holm sur des p de tirage) n'est pas calibré ici : ses p sont exacts par construction. ⑤ Durée NON MESURÉE en entier
  sur la machine du Chat (seul un essai réduit l'a été).
⑩ EFFET — N'écrit aucun fichier ; affiche.
⑪ TERMINAISON — Rend un code de sortie. Boucles bornées par le nombre de cases, de mondes et de tirages. Aucun appel ne
  peut ne pas revenir.
  [sort: oui — code de sortie]
⑫ DÉFINITIONS
  une famille sans talent : m versions dont le vrai gain moyen par opération est nul
  un faux gagnant : une version de cette famille validée par `romano_wolf_du_gain`
  une case : forme × taille × liaison × ressemblance
"""
import datetime
import importlib.util
import math
import os
import random
import sys
import zlib
from statistics import NormalDist

sys.dont_write_bytecode = True

DEBUT = datetime.date(2024, 1, 1)                     # dates fictives, 2024 et après (aucune année 2000-2023)
PERIODE_JOURS = 900                                   # ≈ 2,5 ans
VERSIONS_PAR_FAMILLE = 10
TAILLES = (50, 250)                                   # les deux bords de « 50 à 250 observations » (ARBITRAGE, étape 6)
# liaison : (taille des paquets, corrélation dans un paquet, persistance d'un paquet au suivant, exigée ?)
LIAISONS = {
    "indépendantes": (1, 0.0, 0.0, True),
    "paquets de 10 liés (0,36)": (10, 0.36, 0.0, True),
    "régime persistant (0,8) — affiché": (10, 0.36, 0.8, False),
}
RESSEMBLANCES = {"versions indépendantes": 0.0, "versions ressemblantes (0,96)": 0.96}
NIVEAU_DE_L_ALERTE = 0.001


def fabriquer_les_formes():
    """Fabrique les formes de gains, chacune recentrée sur un gain moyen exactement nul.

    ① RÔLE — Donner aux familles des gains dissymétriques, sans lire aucun cours.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : dictionnaire nom → liste triée de (gain en euros, durée en jours).
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque forme (objectif, stop, part gagnante, durée) : 400 opérations régulièrement réparties
      entre gains et pertes, avec un petit écart déterministe ; puis retrancher la moyenne ; trier par gain.
    ⑦ UNITÉ — EUROS pour 100 000 € ; JOURS.
    ⑧ POURQUOI — « +1/−3 » est la forme qui trompe le plus Student (méthode « au carré », §7.1) ; « +4/−2,5 » est
      celle de C5 ; le tri permet la copule (rang ↔ gain).
    ⑨ CE QUI CLOCHE — Formes stylisées, pas mesurées sur des cours.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. Aucun appel ne peut ne pas revenir.
      [sort: non]
    """
    formes = {}
    for nom, objectif, stop, gagnantes, duree in (("+1/-3 (10 jours)", 1000.0, 3000.0, 300, 10),
                                                  ("+4/-2,5 (20 jours)", 4000.0, 2500.0, 154, 20)):
        brut = [(objectif + 10.0 * (k % 15) - 70.0, duree) for k in range(gagnantes)]
        brut += [(-stop + 20.0 * (k % 15) - 140.0, duree) for k in range(400 - gagnantes)]
        moyenne = math.fsum(g for g, _ in brut) / len(brut)
        formes[nom] = sorted((g - moyenne, d) for g, d in brut)
    return formes


def fabriquer_une_famille(hasard, forme, n, m, liaison, ressemblance):
    """Fabrique une famille de m versions SANS TALENT, de n opérations chacune.

    ① RÔLE — Le monde simulé d'une case.
    ② CONTEXTE D'APPEL — `mesurer_le_risque`, une fois par monde.
    ③ ENTRÉE — `hasard` : un `random.Random` · `forme` : liste triée (gain, durée) · `n`, `m` : entiers ≥ 2 et ≥ 1 ·
      `liaison` : une valeur de LIAISONS · `ressemblance` : corrélation des gains entre versions, dans [0, 1[.
    ④ CONDITIONS D'ENTRÉE — Celles de ③.
    ⑤ SORTIE — UNE valeur : dictionnaire nom → opérations (`net`, `date_entree`, `date_sortie`).
      [rend: 1]
    ⑥ TRAITEMENT — ① tirer des jours de départ de paquets et, par opération, un z de base (facteur commun du paquet,
      qui suit le précédent avec la persistance, plus un bruit) · ② si `ressemblance` > 0 : toutes les versions
      gardent ces jours, et la version i prend le gain de rang Φ(√r × z + √(1 − r) × bruit_i) ; sinon chaque version
      est tirée à part · ③ convertir en opérations datées à partir de `DEBUT`.
    ⑦ UNITÉ — EUROS ; JOURS.
    ⑧ POURQUOI — Copule normale : garde exactement la forme (donc un gain moyen nul) tout en liant les gains d'un
      paquet et ceux de versions voisines (mêmes jours, gains très corrélés) — le cas des versions à un cran.
    ⑨ CE QUI CLOCHE — `CALIBRER_LE_HASARD_DES_GAINS.fabriquer_une_strategie` fait la même chose pour une version : elle
      n'est pas réutilisée, car elle ne rend pas les z dont la ressemblance a besoin.
    ⑩ EFFET — Aucun (consomme le hasard reçu).
    ⑪ TERMINAISON — Rend la main. Boucles bornées par n × m. Aucun appel ne peut ne pas revenir.
      [sort: non]
    """
    phi = NormalDist().cdf
    paquet, rho, persistance, _exigee = liaison
    taille = len(forme)

    def jours_et_z():
        """Tire les jours d'entrée et les z d'une version.

        ① RÔLE — Le tirage de base d'une version.
        ② CONTEXTE D'APPEL — `fabriquer_une_famille`.
        ③ ENTRÉE — —
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : liste de n couples (jour, z).
          [rend: 1]
        ⑥ TRAITEMENT — Départs de paquets triés ; facteur commun u qui suit le précédent ; z = √rho × u + bruit.
        ⑦ UNITÉ — Jours depuis `DEBUT` ; z sans unité.
        ⑧ POURQUOI — Voir `fabriquer_une_famille`, ⑧.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Consomme le hasard de la fonction qui l'entoure.
        ⑪ TERMINAISON — Rend la main ; boucles bornées par n. Aucun appel ne peut ne pas revenir.
          [sort: non]
        """
        sortie = []
        departs = sorted(hasard.randrange(PERIODE_JOURS - paquet - 40) for _ in range(-(-n // paquet)))
        u = hasard.gauss(0.0, 1.0)
        for rang, depart in enumerate(departs):
            if rang:
                u = persistance * u + math.sqrt(1.0 - persistance * persistance) * hasard.gauss(0.0, 1.0)
            for k in range(paquet):
                if len(sortie) < n:
                    sortie.append((depart + k, math.sqrt(rho) * u + math.sqrt(1.0 - rho) * hasard.gauss(0.0, 1.0)))
        return sortie

    base = jours_et_z()
    famille = {}
    for i in range(m):
        if ressemblance > 0.0:
            vues = [(j, math.sqrt(ressemblance) * z + math.sqrt(1.0 - ressemblance) * hasard.gauss(0.0, 1.0))
                    for j, z in base]
        else:
            vues = base if i == 0 else jours_et_z()
        ops = []
        for j, z in vues:
            gain, duree = forme[min(taille - 1, int(phi(z) * taille))]
            ops.append({"net": gain, "date_entree": (DEBUT + datetime.timedelta(days=j)).isoformat(),
                        "date_sortie": (DEBUT + datetime.timedelta(days=j + duree - 1)).isoformat()})
        famille["v%02d" % i] = ops
    return famille


def mesurer_le_risque(methode, fabriquer, mondes, seuil):
    """Compte les mondes où une méthode valide au moins une version d'une famille sans talent.

    ① RÔLE — Le cœur du calibrage, séparé de la méthode jugée pour que l'épreuve E8 puisse lui donner une méthode
      fausse et vérifier qu'il la voit.
    ② CONTEXTE D'APPEL — `main`, une fois par case ; l'épreuve E8.
    ③ ENTRÉE — `methode` : fonction (versions, debut, fin, seuil) qui rend la liste des noms validés, ou lève
      `ValueError` · `fabriquer` : fonction (k) qui rend la famille du monde k · `mondes` : entier ≥ 1 · `seuil` :
      dans ]0, 1[.
    ④ CONDITIONS D'ENTRÉE — Celles de ③.
    ⑤ SORTIE — UNE valeur : dictionnaire `faux` (mondes à au moins un faux gagnant), `non_calculables`, `mondes`.
      [rend: 1]
    ⑥ TRAITEMENT — Pour k de 0 à mondes − 1 : fabriquer, juger sur [DEBUT, DEBUT + PERIODE_JOURS − 1] ; un
      `ValueError` compte « non calculable », jamais « faux » ni « juste ».
    ⑦ UNITÉ — Des NOMBRES DE MONDES.
    ⑧ POURQUOI — Le risque promis porte sur la famille : un seul faux gagnant suffit à compter le monde.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. Une boucle bornée par `mondes`. Un appel de `methode` peut-il ne pas revenir ? Pas
      celui de `romano_wolf_du_gain` (boucles bornées).
      [sort: non]
    """
    fin = (DEBUT + datetime.timedelta(days=PERIODE_JOURS - 1)).isoformat()
    faux = non_calculables = 0
    for k in range(mondes):
        try:
            validees = methode(fabriquer(k), DEBUT.isoformat(), fin, seuil)
        except ValueError:
            non_calculables += 1
            continue
        faux += bool(validees)
    return {"faux": faux, "non_calculables": non_calculables, "mondes": mondes}


def verdict_d_une_case(mesure, seuil, binomiale):
    """Rend le verdict d'une case : « TIENT », « DÉPASSE » ou « INCONNU ».

    ① RÔLE — Décider si le taux mesuré dépasse le seuil promis de façon démontrée.
    ② CONTEXTE D'APPEL — `main`, une fois par case ; l'épreuve E8.
    ③ ENTRÉE — `mesure` : un rendu de `mesurer_le_risque` · `seuil` : le risque promis · `binomiale` : fonction (x, n, p), la
      probabilité d'au moins x succès sur n (`CALIBRER_LE_HASARD_DES_GAINS.binomiale_au_dessus`, réutilisée, R-708).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le mot du verdict.
      [rend: 1]
    ⑥ TRAITEMENT — Plus de 10 % de mondes non calculables → INCONNU (R-734) ; sinon DÉPASSE si la probabilité d'au
      moins `faux` faux gagnants au seuil promis est sous `NIVEAU_DE_L_ALERTE` ; sinon TIENT.
    ⑦ UNITÉ — Sans unité.
    ⑧ POURQUOI — Un taux mesuré fluctue : seul un dépassement improbable au risque promis est une preuve.
    ⑨ CE QUI CLOCHE — Voir l'en-tête, ⑨ ③.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. Aucun appel ne peut ne pas revenir.
      [sort: non]
    """
    calcules = mesure["mondes"] - mesure["non_calculables"]
    if calcules < 0.9 * mesure["mondes"]:
        return "INCONNU"
    if binomiale(mesure["faux"], calcules, seuil) < NIVEAU_DE_L_ALERTE:
        return "DÉPASSE"
    return "TIENT"


def charger(chemin, nom):
    """Charge un programme du dépôt par son chemin.

    ① RÔLE — Prendre le module de la racine reçue, pas un autre.
    ② CONTEXTE D'APPEL — `main` ; l'épreuve E8.
    ③ ENTRÉE — `chemin` : chemin du fichier · `nom` : nom du module.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe.
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — spec_from_file_location, exécution, rangé dans sys.modules.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les modules importent leurs voisins par leur nom.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Charge et exécute du code.
    ⑪ TERMINAISON — Rend la main ou lève. Aucun appel ne peut ne pas revenir.
      [sort: non]
    """
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    sys.modules[nom] = module
    spec.loader.exec_module(module)
    return module


def main(argv):
    """Joue toutes les cases et rend le code.

    ① RÔLE — Le chef d'orchestre du calibrage.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — `argv` : la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête, ③ et ④.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2.
      [rend: 1]
    ⑥ TRAITEMENT — Lire les arguments et les modules ; pour chaque case, mesurer et juger ; afficher ; rendre le code.
    ⑦ UNITÉ — Taux en POURCENTS à l'écran.
    ⑧ POURQUOI — R-731 (une mesure qui peut rougir), R-734 (code non nul si une case n'a pas pu se mesurer).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Rend la main. Aucun appel ne peut ne pas revenir.
      [sort: non]
    """
    if len(argv) < 2 or len(argv) > 4:
        print(__doc__.split("USAGE")[1].split("①")[0].strip())
        return 2
    racine = os.path.abspath(argv[1])
    for f in ("programmes/MODULE_JUGEMENT.py", "programmes/CALIBRER_LE_HASARD_DES_GAINS.py"):
        if not os.path.exists(os.path.join(racine, f)):
            print("DONNÉE MANQUANTE : %s" % f)
            return 2
    sys.path.insert(0, os.path.join(racine, "programmes"))
    J = charger(os.path.join(racine, "programmes/MODULE_JUGEMENT.py"), "MODULE_JUGEMENT")
    C = charger(os.path.join(racine, "programmes/CALIBRER_LE_HASARD_DES_GAINS.py"), "CALIBRER_LE_HASARD_DES_GAINS")
    try:
        mondes = int(argv[2]) if len(argv) > 2 else 1000
        seuil = float(argv[3]) if len(argv) > 3 else J.SEUIL_PAR_FAMILLE_DEFAUT
    except ValueError:
        print("ARGUMENT ILLISIBLE : %s" % argv[2:])
        return 2
    if mondes < 50 or not (0.0 < seuil < 0.5):
        print("ARGUMENT HORS DE SA FORME : mondes %d (≥ 50), seuil %r (dans ]0, 0,5[)" % (mondes, seuil))
        return 2

    def methode(versions, debut, fin, s):
        """Juge une famille par la méthode éprouvée.

        ① RÔLE — Brancher `romano_wolf_du_gain` sur `mesurer_le_risque`.
        ② CONTEXTE D'APPEL — `mesurer_le_risque`.
        ③ ENTRÉE — `versions` : la famille · `debut`, `fin` : la période · `s` : le seuil.
        ④ CONDITIONS D'ENTRÉE — `methode.monde` posé par `fabriquer`.
        ⑤ SORTIE — UNE valeur : la liste des validées.
          [rend: 1]
        ⑥ TRAITEMENT — Appel avec une graine propre au monde.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Sans graine propre, tous les mondes partageraient leurs tirages.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main ou lève `ValueError`.
          [sort: non]
        """
        return J.romano_wolf_du_gain(versions, debut, fin, seuil=s, graine=len(versions) + methode.monde)["validees"]

    print("CALIBRAGE DE LA MÉTHODE DES 30 %% — %d versions par famille, %d mondes par case, seuil %r"
          % (VERSIONS_PAR_FAMILLE, mondes, seuil))
    code = 0
    for nom_forme, forme in fabriquer_les_formes().items():
        for n in TAILLES:
            for nom_liaison, liaison in LIAISONS.items():
                for nom_ress, ress in RESSEMBLANCES.items():
                    hasard = random.Random(zlib.crc32(("%s|%d|%s|%s" % (nom_forme, n, nom_liaison, nom_ress)).encode()))

                    def fabriquer(k):
                        """Fabrique la famille du monde k de la case.

                        ① RÔLE — Le monde k.
                        ② CONTEXTE D'APPEL — `mesurer_le_risque`.
                        ③ ENTRÉE — `k` : entier.
                        ④ CONDITIONS D'ENTRÉE — —
                        ⑤ SORTIE — UNE valeur : la famille.
                          [rend: 1]
                        ⑥ TRAITEMENT — Noter k pour la graine de `methode`, puis `fabriquer_une_famille`.
                        ⑦ UNITÉ — —
                        ⑧ POURQUOI — La graine du jugement suit le monde.
                        ⑨ CE QUI CLOCHE — —
                        ⑩ EFFET — Consomme le hasard de la case.
                        ⑪ TERMINAISON — Rend la main. Aucun appel ne peut ne pas revenir.
                          [sort: non]
                        """
                        methode.monde = k
                        return fabriquer_une_famille(hasard, forme, n, VERSIONS_PAR_FAMILLE, liaison, ress)
                    mesure = mesurer_le_risque(methode, fabriquer, mondes, seuil)
                    verdict = verdict_d_une_case(mesure, seuil, C.binomiale_au_dessus)
                    exigee = liaison[3]
                    calcules = max(1, mesure["mondes"] - mesure["non_calculables"])
                    print("  %-8s %-20s n=%-4d %-36s %-30s : %5.2f %% (%d sur %d, %d non calculables)%s"
                          % (verdict, nom_forme, n, nom_liaison, nom_ress, 100.0 * mesure["faux"] / calcules,
                             mesure["faux"], calcules, mesure["non_calculables"], "" if exigee else " — affiché"))
                    if exigee and verdict == "INCONNU":
                        code = max(code, 2) if code != 1 else 1
                    if exigee and verdict == "DÉPASSE":
                        code = 1
    print("VERDICT : %s" % {0: "la méthode tient son seuil dans chaque case exigée",
                            1: "DÉPASSE — studentiser autrement (ARBITRAGE, étape 6) et relancer",
                            2: "INCONNU — une case n'a pas pu se mesurer"}[code])
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
