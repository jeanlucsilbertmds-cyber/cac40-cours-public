#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ALARME_DES_MACHINES_OISIVES.py — Ven 20-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. « Ce programme sonne quand du travail prêt attend alors qu'une machine pourrait le faire ; il sert à
ce qu'aucune machine GitHub ne reste oisive faute que quelqu'un s'en soit souvenu. » Mots de Jean-Luc du 20-11-2026
(entre 19h42 et 22h00) : « il y a des machines entières qui ne travaillent pas alors qu'il y a un énorme boulot à
faire ». L'état vient de programmes/ETAT_DES_TRAVAUX.py, jamais recalculé ici (R-708).

① RÔLE — Rendre un code NON NUL et une phrase claire dans trois cas : ① une branche À ÉPROUVER alors qu'il reste des
  fils GitHub libres ; ② une branche DÉPLOYABLE alors que rien ne tourne sur GitHub (installation oubliée) ; ③ une
  branche À RELIRE depuis plus de N minutes — rangé à part, c'est une LIMITE : Cowork ne se lance aujourd'hui que par
  le Chat.
② CONTEXTE D'APPEL — À la main par le Chat ; plus tard par un job GitHub toutes les 10 minutes (non branché : il
  faut toucher au fabricant, après l'installation de travail-file-2 et travail-livrer-2).
  python3 -B programmes/ALARME_DES_MACHINES_OISIVES.py [--depot=…] [--gh=…] [--public=…] [--sans-fetch]
                                                     [--minutes=N] [--maintenant=SECONDES_UNIX]
③ ENTRÉE — Les options de ETAT_DES_TRAVAUX, plus --minutes (défaut MINUTES_PAR_DEFAUT) et --maintenant (pour les
  épreuves ; défaut : l'horloge).
④ CONDITIONS D'ENTRÉE — Celles de ETAT_DES_TRAVAUX.
⑤ SORTIE — Le code de sortie, le plus urgent l'emporte : 1 MACHINES OISIVES · 4 INSTALLATION OUBLIÉE · 3 RELECTURE
  EN ATTENTE (LIMITE) · 0 rien · 2 IMPOSSIBLE (l'état n'a pas pu être lu, R-734) · 5 PLANTAGE. Toutes les phrases
  sont affichées, pas seulement la plus urgente.
⑥ TRAITEMENT — Appeler `etat_des_travaux`, puis `alarmes`.
⑦ UNITÉ — Minutes pour le seuil ; fils GitHub.
⑧ POURQUOI — Le 20-11-2026, des épreuves prêtes attendaient pendant que GitHub ne faisait rien, et une installation
  a été faite sans republication. Une alarme lue par un programme ne dépend pas d'un réveil du Chat.
⑨ CE QUI CLOCHE — (a) MINUTES_PAR_DEFAUT = 30 est une PROPOSITION, non décidée par Jean-Luc. (b) « Rien ne tourne »
  compte TOUT passage vivant du dépôt public, y compris pages-build-deployment. (c) Les vieilles branches jamais
  supprimées (travail-livrer à côté de travail-livrer-2) sonnent comme les autres : trancher leur sort revient à
  Jean-Luc. (d) L'heure d'entrée en « À RELIRE » est estimée : la plus récente de la note et des résultats GitHub.
⑩ EFFET — Celui de ETAT_DES_TRAVAUX (fetch) ; écrit sur la sortie standard.
⑪ TERMINAISON — Sort par sys.exit ; les appels à git et gh sont bornés par ETAT_DES_TRAVAUX.DELAI_S.
"""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ETAT_DES_TRAVAUX as E

MINUTES_PAR_DEFAUT = 30
RIEN, OISIVES, IMPOSSIBLE, RELECTURE, INSTALLATION, PLANTAGE = 0, 1, 2, 3, 4, 5
URGENCE = (OISIVES, INSTALLATION, RELECTURE)


def alarmes(etat, minutes, maintenant):
    """Rend les alarmes d'un état.

    ① RÔLE — Le cœur de l'alarme : de l'état aux phrases, sans rien lire.
    ② CONTEXTE D'APPEL — `main` ; les épreuves l'appellent directement.
    ③ ENTRÉE — `etat` : la valeur de E.etat_des_travaux · `minutes` : le seuil de la relecture en attente ·
      `maintenant` : secondes Unix.
    ④ CONDITIONS D'ENTRÉE — `etat` porte « fils », « passages », « branches ».
    ⑤ SORTIE — DEUX valeurs : le code (le plus urgent dans l'ordre URGENCE, ou RIEN) · la liste des phrases.
      [rend: 2]
    ⑥ TRAITEMENT — ① À ÉPROUVER et fils libres > 0 → OISIVES · ② DÉPLOYABLE et aucun passage vivant → INSTALLATION ·
      ③ À RELIRE depuis plus de `minutes` → RELECTURE, phrase marquée « LIMITE ». Une branche INSTALLÉE ne sonne jamais.
    ⑦ UNITÉ — Minutes ; fils.
    ⑧ POURQUOI — Voir le module.
    ⑨ CE QUI CLOCHE — Voir le module, (c) et (d).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    libres = etat["fils"]["libres"]
    codes, phrases = set(), []
    for b in etat["branches"]:
        if b["etat"] == "À ÉPROUVER" and libres > 0:
            codes.add(OISIVES)
            phrases.append(f"MACHINES OISIVES — {b['branche']} attend ses épreuves longues alors que {libres} fil(s) "
                           f"GitHub sur {etat['fils']['largeur']} sont libres : {b['action']}")
        elif b["etat"] == "DÉPLOYABLE" and not etat["passages"]:
            codes.add(INSTALLATION)
            phrases.append(f"INSTALLATION OUBLIÉE — {b['branche']} est DÉPLOYABLE et rien ne tourne sur GitHub : "
                           f"{b['action']}")
        elif b["etat"] == "À RELIRE":
            heures = [b["note_heure"] or 0] + [r["heure"] for r in b["resultats"].values()]
            attente = (maintenant - max(heures)) / 60
            if attente > minutes:
                codes.add(RELECTURE)
                phrases.append(f"RELECTURE EN ATTENTE (LIMITE : Cowork ne se lance que par le Chat) — {b['branche']} "
                               f"attend depuis {int(attente)} min (seuil {minutes}) : {b['action']}")
    code = next((c for c in URGENCE if c in codes), RIEN)
    return code, phrases


def main():
    """Lit la ligne de commande, sonne ou se tait, sort.

    ① RÔLE — Le programme en ligne de commande.
    ② CONTEXTE D'APPEL — Voir le module.
    ③ ENTRÉE — La ligne de commande.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Le code de sortie décrit au module.
      [rend: rien]
    ⑥ TRAITEMENT — Options ; E.etat_des_travaux puis `alarmes`, tous deux dans le même « try » (une exception
      sort en 5 PLANTAGE, jamais en 1) ; affichage.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit sur la sortie standard.
    ⑪ TERMINAISON — Sort par sys.exit.
      [sort: oui]
    """
    p = argparse.ArgumentParser(description="Alarme des machines oisives.")
    p.add_argument("--depot", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    p.add_argument("--gh", default="gh")
    p.add_argument("--public", default=E.PUBLIC_PAR_DEFAUT)
    p.add_argument("--sans-fetch", action="store_true")
    p.add_argument("--minutes", type=int, default=MINUTES_PAR_DEFAUT)
    p.add_argument("--maintenant", type=int, default=None)
    a = p.parse_args()
    try:
        etat = E.etat_des_travaux(a.depot, a.gh, a.public, fetch=not a.sans_fetch)
        # DANS le try (RELU Cowork m1, 20-11-2026) : un plantage ici sortait en code 1, lu MACHINES OISIVES
        code, phrases = alarmes(etat, a.minutes, a.maintenant if a.maintenant is not None else int(time.time()))
    except E.Impossible as e:
        print(f"IMPOSSIBLE — {e} — aucune alarme ne peut être jugée (R-734)")
        sys.exit(IMPOSSIBLE)
    except Exception as e:  # PLANTAGE : jamais lu comme un verdict
        print(f"PLANTAGE — {type(e).__name__} : {e}")
        sys.exit(PLANTAGE)
    for x in phrases:
        print(x)
    if code == RIEN:
        print(f"RIEN — aucune machine oisive, aucune installation oubliée, aucune relecture en attente depuis plus "
              f"de {a.minutes} min (fils libres : {etat['fils']['libres']}/{etat['fils']['largeur']})")
    sys.exit(code)


if __name__ == "__main__":
    main()
