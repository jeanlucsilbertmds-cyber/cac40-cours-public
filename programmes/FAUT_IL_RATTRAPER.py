#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAUT_IL_RATTRAPER — dit, le matin, si le circuit du soir de la veille doit être relancé.

① RÔLE — Décider, chaque matin de semaine, si le circuit du soir de GitHub a fini son
  travail sur la dernière séance de bourse. S'il ne l'a pas fini, le passage du matin
  (.github/workflows/rattrapage_du_matin.yml) le relance, et les signaux et les positions
  de cette séance sont calculés quand même.
② CONTEXTE D'APPEL — Le passage du matin, du mardi au samedi. À la main, pour voir la
  décision : python3 programmes/FAUT_IL_RATTRAPER.py <racine du dépôt>.
③ ENTRÉE — `sys.argv[1]` : la racine d'un clone du dépôt. L'heure est lue à l'horloge de
  Paris.
④ CONDITIONS D'ENTRÉE — La racine porte donnees/CALENDRIER_EURONEXT.csv,
  rapports/audit_du_jour.md et donnees/signaux_du_jour.json ; programmes/
  CONTRATS_DES_FICHIERS.py et programmes/CALENDRIER_DE_LA_BOURSE.py sont à côté de ce
  programme. Un fichier absent ou illisible n'arrête rien : il est dit, et il décide
  selon le sens de la ligne ⑧.
⑤ SORTIE — Une ligne de verdict, puis le détail, sur la sortie standard. Code de sortie :
  0 = rien à rattraper ; 10 = à rattraper ; 1 = impossible de décider (le calendrier ne se
  lit pas) — le passage du matin rattrape alors quand même, et rougit (R-734 : un
  contrôle qui n'a pas pu conclure ne rend jamais 0).
⑥ TRAITEMENT — ① la séance attendue : le dernier jour de bourse AVANT aujourd'hui, par le
  calendrier · ② la date et l'heure du rapport du radar, lues par `date_ecrite` · ③ la
  séance, l'heure du calcul (`calcule_le`) et les valeurs sans cette séance, dans le
  fichier des signaux · ④ rien à faire si et seulement si les signaux portent la séance
  attendue ou une plus récente, ne laissent aucune valeur sans elle, ET si le radar a
  écrit son rapport APRÈS le calcul de ces signaux ; sinon, rattraper.
⑦ UNITÉ — Des jours du calendrier de Paris (AAAA-MM-JJ).
⑧ POURQUOI — Décision de Jean-Luc du 01-10-2026 à 00h01 (« 1 ») : un deuxième passage
  automatique, le lendemain matin, si le circuit du soir n'a pas fini — comme la boucle
  Cowork de 07h05, seule à rattraper ce cas jusqu'ici (tableau des fonctions des tâches,
  rapports/TABLEAU_FONCTIONS_DES_TACHES_Mer_30-09-2026.md, ligne 10.38 ; R-758 : avant
  d'arrêter ce qui tourne, reprendre chacune de ses fonctions). Le radar est le dernier
  pas du circuit et ne tourne que si tous les pas bloquants sont passés : un rapport
  écrit APRÈS le calcul des signaux prouve que le circuit a fini ce passage-là. La DATE
  seule ne suffit pas (relecteur, 01-10-2026) : un rapport écrit par un rattrapage le
  matin porte la même date que le circuit du soir qui tombe après les signaux. La séance
  des signaux s'ajoute parce que la collecte n'est pas bloquante : un soir où ABC ne
  répond pas, le circuit finit sans la séance ; et les valeurs sans la séance, parce
  qu'une collecte du matin les complète. DANS LE DOUTE, ON RATTRAPE : relancer ne double
  ni une position ni un trade (épreuves T1 et T2 de
  tests/EPREUVES_DU_RATTRAPAGE_Jeu_01-10-2026.py), et le passage du matin relance le
  circuit SANS sa mesure de la performance, qui s'empile par date d'horloge (voir ⑨ ④) ;
  alors qu'une séance non calculée perd ses signaux pour toujours.
⑨ CE QUI CLOCHE — ① Un circuit qui tombe à chaque passage tombera aussi le matin : le
  rattrapage ne répare que les pannes passagères (réseau, poussée refusée) ; une panne
  durable reste dite par le message du soir (« Circuit du soir NON passé »). ② Le
  calendrier ne couvre que 2026 (A-513) : au-delà, code 1 et rattrapage de précaution.
  ③ Les signaux d'une séance se calculent jusqu'à la collecte du soir suivant : un
  rattrapage qui échoue aussi le matin laisse la journée pour une relance à la main —
  EN COCHANT « rattrapage » dans « Run workflow » : sans elle, la mesure de la journée
  s'écrit et empêche celle du soir (voir ④).
  ④ La mesure de la performance s'empile une ligne par jour d'HORLOGE, et passe une date
  déjà écrite : lancée le matin, elle empêchait celle du soir (relecteur, 01-10-2026).
  Le passage du matin la saute donc ; la mesure du soir manqué n'est jamais écrite.
  ⑤ Une valeur durablement absente (retirée de la cote) ferait relancer chaque matin :
  elle est alors aussi une alerte du contrôle des valeurs, à trancher par Jean-Luc.
⑩ EFFET — Lit trois fichiers ; n'écrit rien.
⑪ TERMINAISON — Sort par sys.exit, en 0, 10 ou 1.
  [sort: oui]
"""
import importlib.util
import json
import os
import re
import sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

RAPPORT = "rapports/audit_du_jour.md"
SIGNAUX = "donnees/signaux_du_jour.json"
RIEN, RATTRAPER, INDECIS = 0, 10, 1


def _module(nom):
    """Charge un programme voisin comme module et le rend.

    ① RÔLE — Emprunter le calendrier et la lecture des dates là où ils sont écrits une
      fois (R-708 : deux implémentations d'une même chose divergent toujours).
    ② CONTEXTE D'APPEL — `decider`, deux fois.
    ③ ENTRÉE — `nom` : le nom du fichier, sans dossier.
    ④ CONDITIONS D'ENTRÉE — Le fichier est dans le dossier de ce programme.
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — importer le fichier sous un nom propre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le programme et les modules qu'il emprunte voyagent ensemble.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Importe un module.
    ⑪ TERMINAISON — Rend la main, ou lève si l'import échoue.
      [sort: non]
    """
    ici = os.path.dirname(os.path.abspath(__file__))
    sp = importlib.util.spec_from_file_location("rattrapage_" + nom[:-3], os.path.join(ici, nom))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def decider(racine, aujourd_hui):
    """Rend la décision du matin et les lignes qui la justifient.

    ① RÔLE — Le cœur du programme.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `racine` : le clone · `aujourd_hui` : la date du jour à Paris (une date).
    ④ CONDITIONS D'ENTRÉE — Voir la fiche du fichier.
    ⑤ SORTIE — DEUX valeurs : le code (RIEN, RATTRAPER ou INDECIS) · la liste des lignes
      à afficher, la première étant le verdict.
      [rend: 2]
    ⑥ TRAITEMENT — voir la fiche du fichier, ⑥.
    ⑦ UNITÉ — Des dates.
    ⑧ POURQUOI — Séparée de `main` pour être éprouvée avec une date choisie.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit trois fichiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    lignes = []
    try:
        K = _module("CALENDRIER_DE_LA_BOURSE.py")
        cal = K.lire(racine)
        attendue = K.dernier_jour_de_bourse(aujourd_hui - timedelta(days=1), cal)
    except Exception as e:
        return INDECIS, [f"🚨 RATTRAPAGE PAR PRÉCAUTION — séance attendue inconnue : calendrier inutilisable "
                         f"({type(e).__name__}: {str(e)[:120]})"]
    lignes.append(f"séance attendue : {attendue.isoformat()} (dernier jour de bourse avant le {aujourd_hui.isoformat()})")
    # ② le rapport du radar : sa date ET son heure
    try:
        C = _module("CONTRATS_DES_FICHIERS.py")
        motif = next(x[1] for x in C.FABRIQUES_DU_SOIR if x[0] == RAPPORT)
        d_rap, h_rap, raison = C.date_ecrite(racine, RAPPORT, motif)
    except Exception as e:
        d_rap, h_rap, raison = None, None, f"illisible ({type(e).__name__})"
    radar = f"{d_rap} {h_rap}" if d_rap and h_rap else None
    lignes.append("rapport du radar : " + (radar or (f"{d_rap}, SANS HEURE" if d_rap else raison)))
    # ③ les signaux : leur séance, l'heure de leur calcul, les valeurs sans la séance
    seance, calcul, manquent = None, None, None
    try:
        s = json.load(open(os.path.join(racine, SIGNAUX), encoding="utf-8"))
        if not isinstance(s, dict):
            raise ValueError("forme inattendue")
        seance = s.get("seance")
        if not (isinstance(seance, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", seance)):
            raise ValueError(f"séance « {str(seance)[:20]} »")
        date.fromisoformat(seance)
        m = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", str(s.get("calcule_le", "")))
        calcul = m.group(1) if m else None
        manquent = s.get("valeurs_sans_cette_seance")
        manquent = manquent if isinstance(manquent, list) else None
    except Exception as e:
        seance = None
        lignes.append(f"signaux : illisibles ({type(e).__name__}: {str(e)[:80]})")
    else:
        lignes.append(f"signaux : séance {seance}, calculés le {calcul or 'HEURE ILLISIBLE'}"
                      + (f", {len(manquent)} valeur(s) sans cette séance" if manquent else "")
                      + (", liste des valeurs sans la séance ILLISIBLE" if manquent is None else ""))
    # ④ la décision — dans le doute, on rattrape
    a = attendue.isoformat()
    pourquoi = []
    if seance is None or seance < a:
        pourquoi.append("les signaux ne portent pas cette séance")
    elif manquent is None or manquent:
        pourquoi.append("des valeurs n'ont pas cette séance, ou leur liste est illisible")
    if radar is None or calcul is None or radar < calcul:
        pourquoi.append("le radar n'a pas écrit son rapport après le calcul des signaux")
    if not pourquoi:
        lignes.insert(0, f"✅ RIEN À RATTRAPER — le circuit a fini la séance du {a}")
        return RIEN, lignes
    lignes.insert(0, f"⚠️ À RATTRAPER — séance du {attendue.isoformat()} : " + " ; ".join(pourquoi))
    return RATTRAPER, lignes


def main():
    """Affiche la décision et sort par son code.

    ① RÔLE — Point d'entrée.
    ② CONTEXTE D'APPEL — La ligne de commande, et le passage du matin.
    ③ ENTRÉE — `sys.argv[1]` : la racine du clone.
    ④ CONDITIONS D'ENTRÉE — Un argument ; sinon le mode d'emploi, et code 1.
    ⑤ SORTIE — Ne rend rien : sort par sys.exit.
      [rend: rien]
    ⑥ TRAITEMENT — ① lire l'heure de Paris · ② décider · ③ afficher · ④ sortir.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le passage du matin lit le code, Jean-Luc et le relecteur lisent le texte.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Sort par sys.exit, en 0, 10 ou 1.
      [sort: oui]
    """
    if len(sys.argv) < 2:
        print("usage : python3 programmes/FAUT_IL_RATTRAPER.py <racine du dépôt>")
        sys.exit(INDECIS)
    code, lignes = decider(sys.argv[1], datetime.now(ZoneInfo("Europe/Paris")).date())
    print("\n".join(lignes))
    sys.exit(code)


if __name__ == "__main__":
    main()
