#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAUT_IL_TOURNER — dit, au début de chaque passage du circuit du soir, s'il doit tourner.

① RÔLE — Décider, à l'heure de Paris où le passage démarre RÉELLEMENT, si le circuit du
  soir doit faire son travail, et s'il doit sauter la mesure de la performance. Le circuit
  public (`.github/workflows/circuit_du_soir.yml`) est réveillé par GitHub plusieurs fois
  par jour ; ce programme fait que seul le passage utile travaille.
② CONTEXTE D'APPEL — Le premier job du circuit public, `faut_il_tourner`, à chaque passage.
  À la main, pour voir la décision : python3 programmes/FAUT_IL_TOURNER.py <racine> schedule ""
③ ENTRÉE — La ligne de commande : TROIS arguments · la racine d'un clone du dépôt privé ·
  le nom de l'événement qui a lancé le passage (`github.event_name` : « schedule » pour
  un réveil planifié, « workflow_dispatch » pour un lancement à la main) · la case
  « rattrapage » cochée ou non au lancement à la main (« true », sinon n'importe quoi).
  L'environnement : `GITHUB_OUTPUT`, le fichier où GitHub lit les sorties du pas (absent
  à la main : rien n'y est écrit).
④ CONDITIONS D'ENTRÉE — Pour un réveil planifié, celles de
  programmes/FAUT_IL_RATTRAPER.py (calendrier, rapport du radar, fichier des signaux) ;
  un fichier absent n'arrête rien, il fait tourner par précaution. Trois arguments ;
  sinon le mode d'emploi et le code 1.
⑤ SORTIE — Sur la sortie standard : une ligne de verdict puis le détail. Dans
  `GITHUB_OUTPUT` : DEUX lignes, `tourner=true|false` et `rattrapage=true|false`. Code de
  sortie : 0 si la décision est prise ; 1 si elle n'a pas pu l'être (calendrier
  illisible) — le passage tourne alors par précaution, et le pas rougit (R-734 : un
  contrôle qui n'a pas pu conclure ne rend jamais 0).
⑥ TRAITEMENT — `decider` : ① lancé à la main → tourner, avec la case « rattrapage » telle
  qu'elle a été cochée · ② réveil planifié : demander à FAUT_IL_RATTRAPER si la dernière
  séance close est déjà finie — à partir de l'heure où la clôture du jour est définitive
  chez ABC Bourse (`HEURE_CLOTURE_PARIS` de programmes/COLLECTER_ABC_GITHUB.py, 18h),
  c'est celle du jour ; avant, celle de la veille — et tourner seulement si elle ne l'est
  pas · ③ un passage planifié qui tourne avant 18h saute la mesure de la performance ; un
  lancement à la main la saute aussi avant 18h, case cochée ou non.
⑦ UNITÉ — Des heures et des dates de Paris.
⑧ POURQUOI — Décision de Jean-Luc du 13-10-2026 : faire partir le circuit au plus tôt
  après la clôture (18h07), avec un secours le soir (21h23) et un rattrapage le matin
  (7h41), au lieu de 20h00 pile — à 20h00 pile, GitHub retardait le passage de plusieurs
  heures (23h25 le 08-10, 00h17 le 10-10, 02h10 le 13-10) ; sa documentation dit que les
  réveils du début de chaque heure sont retardés en forte charge, voire abandonnés.
  GitHub programme en heure UNIVERSELLE, qui ne suit pas l'heure d'été : 16h07 universelle
  vaut 18h07 l'été mais 17h07 l'hiver, avant la clôture définitive. Le circuit est donc
  réveillé à 16h07 ET 17h07 universelles, et c'est l'horloge de Paris, lue ici, qui
  décide : l'été, 18h07 tourne et 19h07 trouve le travail fait ; l'hiver, 17h07 s'arrête
  si la veille est faite (sinon il la rattrape, mesure sautée) et 18h07 tourne. Avant 18h, la collecte refuserait la ligne du jour (partielle) et
  le reste du circuit recalculerait la veille ; pire, la mesure de la performance, qui
  s'empile une ligne par jour d'horloge et passe une date déjà écrite, serait écrite
  sans la séance du jour et empêcherait celle du soir. Pour la même raison, elle est
  sautée le matin (FAUT_IL_RATTRAPER.py, ⑨ ④). Un passage dont le travail est déjà fait
  s'arrête : il ne ferait que pousser des fichiers identiques. Un lancement à la main
  avant 18h sautait la mesure seulement si la case était cochée : sinon il écrivait la
  mesure de la journée avec la séance de la veille, et celle du soir n'était plus
  écrite (relecture à mandat inversé du 13-10-2026, cas D, défaut antérieur).
  AUCUNE FENÊTRE D'INTERDICTION EN JOURNÉE : une première version (13-10-2026) refusait
  tout réveil planifié entre 9h et 18h. Le Chat l'avait ajoutée de lui-même, sans
  demande de Jean-Luc, pour arrêter le réveil de 17h07 l'hiver. Le 14-10-2026, le réveil
  prévu à 7h41 est parti à 12h37 (GitHub, 4 h 56 de retard) et cette fenêtre l'a arrêté :
  un matin où la séance de la veille aurait manqué, ses signaux auraient été perdus
  (cassure K). Elle ne protégeait rien que le reste ne protège déjà : avant 18h, la
  collecte refuse la ligne du jour (partielle) et la mesure est sautée ; un réveil en
  journée ne fait donc que rattraper la veille, et un réveil dont la veille est faite
  s'arrête. Retirée sur décision de Jean-Luc du 14-10-2026 à 18h32 (« 1 »).
⑨ CE QUI CLOCHE — ① « La clôture du jour est définitive à 17h55 chez ABC » repose sur
  UNE observation, le 09-09-2026 (A-391) ; le 14-10-2026, l'essai d'A-579 l'a vue
  définitive dès 17h35-17h36, le volume dès 17h39 ; si ABC servait un jour une ligne partielle
  après 18h, la collecte l'accepterait, et seule la détection des révisions du
  lendemain le dirait. ② Le calendrier ne couvre que 2026 (A-513) : au-delà, code 1 et
  passage par précaution, à chaque réveil. ③ Un réveil du SOIR retardé par GitHub
  après minuit est jugé comme un réveil du matin : il tourne, mais saute la mesure de
  la performance, et la journée reste sans mesure (cassure J de Cowork, 14-10-2026 ;
  la réparer demande que la mesure s'empile par séance et non par jour d'horloge —
  décision de Jean-Luc attendue, A-579).
  ④ Un passage de 18h07 où ABC n'aurait pas encore la séance du jour écrit quand même
  la mesure de la journée, sans cette séance ; le secours de 21h23 complète les cours
  et les signaux, pas la mesure (relecture du 13-10-2026 ; le risque existait à 20h00,
  il est plus probable à 18h07). ⑤ Si ce programme meurt avant d'écrire sa réponse,
  le job du circuit ne tourne pas et le pas rougit ; le réveil suivant reprend.
  ⑥ « Relancer » un passage depuis la page de GitHub garde l'événement d'origine
  (« schedule ») : relancé en journée, il s'arrête si la veille est faite, et ne
  traite jamais la séance du jour avant 18h. Pour relancer, utiliser « Run
  workflow » (THÉORIQUE, d'après la documentation de GitHub, non éprouvé ici).
  ⑦ Relecture à mandat inversé du 14-10-2026 (retrait de la fenêtre) : a) une décision
  prise juste avant 18h, la veille manquante, suivie d'une collecte qui démarre après 18h :
  la collecte, qui relit sa propre horloge, prend la ligne du jour ; la mesure est sautée,
  puis les réveils suivants trouvent le travail fait — la journée reste sans mesure ; même
  remède que ③ (une mesure par séance, A-579) ; b) à partir de 2027, faute de calendrier
  (A-513), le réveil de 17h07 tourne chaque jour par précaution, en rouge ; c) un
  rattrapage en journée écrit le rapport du radar daté du jour : si les passages du soir
  tombent ensuite, l'alerte « Circuit du soir NON passé », qui ne compare que la date,
  ne sort pas (défaut antérieur, étendu).
⑩ EFFET — Lit trois fichiers (par FAUT_IL_RATTRAPER) ; écrit deux lignes dans
  `GITHUB_OUTPUT` s'il est posé.
⑪ TERMINAISON — Sort par sys.exit, en 0 ou 1. Aucun appel qui puisse ne pas revenir.
  [sort: oui]
"""
import importlib.util
import os
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")
DECIDE, INDECIS = 0, 1


def _module(nom):
    """Charge un programme voisin comme module et le rend.

    ① RÔLE — Emprunter l'heure de clôture et la décision du rattrapage là où elles sont
      écrites une fois (R-708 : deux implémentations d'une même chose divergent toujours).
    ② CONTEXTE D'APPEL — `decider`, une ou deux fois.
    ③ ENTRÉE — `nom` : le nom du fichier, sans dossier.
    ④ CONDITIONS D'ENTRÉE — Le fichier est dans le dossier de ce programme.
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — importer le fichier sous un nom propre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le programme et les modules qu'il emprunte voyagent ensemble, au dépôt
      privé comme au dépôt public.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Importe un module (COLLECTER_ABC_GITHUB n'agit qu'en `__main__`).
    ⑪ TERMINAISON — Rend la main, ou lève si l'import échoue.
      [sort: non]
    """
    ici = os.path.dirname(os.path.abspath(__file__))
    sp = importlib.util.spec_from_file_location("tourner_" + nom[:-3], os.path.join(ici, nom))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def decider(racine, maintenant, evenement, case_rattrapage):
    """Rend la décision du passage et les lignes qui la justifient.

    ① RÔLE — Le cœur du programme.
    ② CONTEXTE D'APPEL — `main`, une fois ; les épreuves, avec une heure choisie.
    ③ ENTRÉE — `racine` : le clone · `maintenant` : la date et l'heure de Paris (un
      datetime avec fuseau) · `evenement` : « schedule » ou autre · `case_rattrapage` :
      « true » si la case est cochée.
    ④ CONDITIONS D'ENTRÉE — Voir la fiche du fichier.
    ⑤ SORTIE — QUATRE valeurs : le code (DECIDE ou INDECIS) · tourner (booléen) ·
      rattrapage (booléen) · la liste des lignes à afficher, la première étant le verdict.
      [rend: 4]
    ⑥ TRAITEMENT — Voir la fiche du fichier, ⑥.
    ⑦ UNITÉ — Des heures de Paris.
    ⑧ POURQUOI — Séparée de `main` pour être éprouvée avec une heure choisie.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit trois fichiers, par FAUT_IL_RATTRAPER.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    heure = f"{maintenant:%Y-%m-%d %H:%M} (Paris)"
    cloture = _module("COLLECTER_ABC_GITHUB.py").HEURE_CLOTURE_PARIS
    if evenement != "schedule":
        tot = maintenant.hour < cloture
        r = case_rattrapage == "true" or tot
        return DECIDE, True, r, [f"▶️ TOURNER — lancé à la main ({evenement}) le {heure}"
                                 + (", mesure sautée (case « rattrapage » cochée)" if case_rattrapage == "true"
                                    else f", mesure sautée (avant {cloture}h)" if tot else "")]
    soir = maintenant.hour >= cloture
    # FAUT_IL_RATTRAPER attend la séance « avant le jour qu'on lui donne » : le soir, on lui
    # donne demain, et la séance attendue est celle d'aujourd'hui si la Bourse a ouvert.
    jour = maintenant.date() + (timedelta(days=1) if soir else timedelta(0))
    code, lignes = _module("FAUT_IL_RATTRAPER.py").decider(racine, jour)
    rattrapage = not soir
    suite = f", mesure sautée (avant {cloture}h)" if rattrapage else ""
    if code == 0:
        return DECIDE, False, rattrapage, [f"⏹️ NE PAS TOURNER — réveil du {heure} : travail déjà fait"] + lignes
    if code == 10:
        return DECIDE, True, rattrapage, [f"▶️ TOURNER — réveil du {heure}{suite}"] + lignes
    return INDECIS, True, rattrapage, [f"🚨 TOURNER PAR PRÉCAUTION — réveil du {heure}{suite} : "
                                       "la décision n'a pas pu se prendre"] + lignes


def main():
    """Affiche la décision, l'écrit pour GitHub et sort par son code.

    ① RÔLE — Point d'entrée.
    ② CONTEXTE D'APPEL — La ligne de commande, et le job `faut_il_tourner` du circuit public.
    ③ ENTRÉE — `sys.argv[1:4]` : racine, événement, case « rattrapage ».
    ④ CONDITIONS D'ENTRÉE — Trois arguments ; sinon le mode d'emploi, et code 1.
    ⑤ SORTIE — Ne rend rien : sort par sys.exit.
      [rend: rien]
    ⑥ TRAITEMENT — ① lire l'heure de Paris · ② décider · ③ écrire les deux sorties ·
      ④ afficher · ⑤ sortir.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — GitHub lit les sorties ; Jean-Luc et le relecteur lisent le texte.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit deux lignes dans `GITHUB_OUTPUT` s'il est posé ; affiche.
    ⑪ TERMINAISON — Sort par sys.exit, en 0 ou 1.
      [sort: oui]
    """
    if len(sys.argv) != 4:
        print("usage : python3 programmes/FAUT_IL_TOURNER.py <racine> <événement> <case rattrapage>")
        sys.exit(INDECIS)
    try:
        code, tourner, rattrapage, lignes = decider(sys.argv[1], datetime.now(PARIS), sys.argv[2], sys.argv[3])
    except Exception as e:      # dans le doute, on tourne : une séance non lue perd ses signaux
        try:   # la mesure n'est sautée qu'avant l'heure de clôture, comme à la main
            rattrapage = datetime.now(PARIS).hour < _module("COLLECTER_ABC_GITHUB.py").HEURE_CLOTURE_PARIS
        except Exception:
            rattrapage = True   # l'heure de clôture elle-même est illisible : mesure sautée par précaution
        code, tourner = INDECIS, True
        lignes = [f"🚨 TOURNER PAR PRÉCAUTION — décision impossible ({type(e).__name__}: {str(e)[:120]})"]
    sortie = os.environ.get("GITHUB_OUTPUT")
    if sortie:
        with open(sortie, "a", encoding="utf-8") as f:
            f.write(f"tourner={'true' if tourner else 'false'}\nrattrapage={'true' if rattrapage else 'false'}\n")
    print("\n".join(lignes))
    sys.exit(code)


if __name__ == "__main__":
    main()
