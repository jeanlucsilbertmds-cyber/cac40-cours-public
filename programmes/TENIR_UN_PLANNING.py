#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fait tenir un planning par un programme : chaque jalon a une échéance et une preuve, et un retard ne se tait pas.

① RÔLE — Lire un fichier de jalons et dire, toutes les 10 minutes, où en est le
  planning : jalons tenus, prochain jalon, jalons en retard, rendez-vous avec
  Jean-Luc. Un jalon est TENU quand le fichier qui le prouve existe. Créé le
  25-10-2026 pour le PLAN ORANGE 27-10 (BACKLOG A-623), rendu générique le même
  soir à la demande de Jean-Luc (BACKLOG A-624). Mode d'emploi complet :
  MODE_EMPLOI_DEPOT.md §13.

② CONTEXTE D APPEL — Lancé à la main par le Chat, SOUS L OUTIL DE SURVEILLANCE
  (Monitor), avec la commande du §13 du mode d'emploi : un verrou contre les
  doubles copies, un journal, un filtre sur les repères. La surveillance tient la
  machine du Chat éveillée et réveille le Chat à chaque ligne affichée ; elle
  s'arrête au bout de 30 minutes et le Chat la relance (MODE_EMPLOI_DEPOT.md §12).
  Aucune tâche automatique ne l'appelle.

③ ENTRÉE — Un seul argument : le chemin d'un fichier CSV séparé par « ; », avec
  l'en-tête « jalon;echeance;preuve;libelle ». echeance au format
  « AAAA-MM-JJ HH:MM », heure de Paris. preuve = le chemin ABSOLU du fichier qui
  doit exister, ou le mot « RDV » pour un rendez-vous avec Jean-Luc. Exemple réel
  du 25-10-2026 : « J3;2026-10-26 01:30;<dossier>/PROTOCOLE.md;Protocole Orange
  déposé avant toute mesure ».

④ CONDITIONS D ENTRÉE — Le fichier existe et se lit ; chaque échéance suit le
  format. Sinon : ligne ARRET et code 2 (fichier absent) ou 3 (illisible). Le
  fichier est relu à chaque passage : on peut ajouter un jalon sans relancer.

⑤ SORTIE — Des lignes affichées, chacune commençant par un repère, et un code de
  sortie. Repères : ETAPE (état, à chaque passage) · ALERTE (échéance dans moins
  de 30 minutes, preuve absente) · ERREUR JALON DÉPASSÉ (échéance passée, preuve
  absente : redit à chaque passage tant que dure le retard) · RDV (rendez-vous
  atteint, dit UNE seule fois) · FINI (toutes les preuves existent, code 0) ·
  ARRET (code 2 ou 3). Une seule valeur rendue : le code de sortie.

⑥ TRAITEMENT — À chaque passage : ① lire le fichier ; ② annoncer chaque
  rendez-vous atteint et pas encore annoncé, puis écrire sa marque ; ③ pour chaque
  jalon, regarder si la preuve existe, sinon comparer l'heure à l'échéance ; ④ si
  tout est prouvé, FINI ; sinon ETAPE avec le prochain jalon ; ⑤ dormir 10 minutes.

⑦ UNITÉ — Heures de Paris (Europe/Paris), minutes.

⑧ POURQUOI — Une promesse de délai ne tient pas d'une conversation à l'autre ;
  un programme, si (R-754 : ce qu'un programme peut faire, un programme le fait).
  Le 25-10-2026, Jean-Luc : « comment vas-tu t'assurer que le plan sera tenu
  strictement dans les temps ? », puis « tu ne réduis pas les tâches ; il faut que
  toutes les tâches soient faites dans les délais ».

⑨ CE QUI CLOCHE — Il voit qu'un fichier EXISTE, jamais qu'il est BON : un fichier
  vide tient le jalon. La qualité reste aux relecteurs. Il ne tourne que si la
  surveillance tourne : une session arrêtée arrête tout, sans prévenir personne.
  Tenue prouvée le 25-10-2026 au soir seulement ; une nuit entière : THÉORIQUE.

⑩ EFFET — Écrit, pour chaque rendez-vous annoncé, une marque
  « <fichier de jalons>.<jalon>.dit » à côté du fichier de jalons. Rien d'autre.

⑪ TERMINAISON — Boucle sans fin tant qu'un jalon manque ; la surveillance la
  coupe à 30 minutes. Aucun appel réseau : aucun de ses appels ne peut rester
  bloqué.
"""
import csv
import datetime
import os
import sys
import time
from zoneinfo import ZoneInfo

P = ZoneInfo("Europe/Paris")
PAUSE_S = 600       # 10 minutes entre deux passages
ALERTE_S = 1800     # alerte 30 minutes avant une échéance sans preuve


def lire(chemin):
    """Lit le fichier de jalons.

    ① rôle : rendre les lignes du fichier de jalons
    ② contexte : appelée à chaque passage de passage_unique
    ③ entrée : `chemin`, le chemin du CSV
    ④ conditions : fichier lisible, séparateur « ; »
    ⑤ sortie : UNE valeur, la
    liste des lignes (dictionnaires)
      [rend: 1]
    ⑥ traitement : csv.DictReader
    ⑦ unité : —
    ⑧ pourquoi : relire à
    chaque passage permet d'ajouter un jalon sans relancer
    ⑨ ce qui cloche : une colonne manquante lève
    KeyError plus loin, rattrapée par passage_unique
    ⑩ effet : —
    ⑪ terminaison : lecture d'un fichier
    local, revient toujours.
      [sort: non]
    """
    with open(chemin, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f, delimiter=";"))


def passage_unique(chemin, maintenant, ecrire=True):
    """Fait un passage : annonce, compte, et dit si tout est prouvé.

    ① rôle : un examen complet du planning à l'instant donné
    ② contexte : appelée par main toutes les
    10 minutes ; les épreuves l'appellent avec une heure fabriquée
    ③ entrée : `chemin`, le chemin du CSV ; `maintenant`, l'heure (datetime avec fuseau) ; `ecrire`, faux pour
    n'écrire ni la marque des rendez-vous ni la liste des jalons vus
    ④ conditions : échéances au format AAAA-MM-JJ HH:MM
    ⑤ sortie : UNE valeur,
    un couple (lignes à afficher, fini) où fini vaut True si toutes les preuves existent, ou None si le
    fichier est illisible
      [rend: 2]
    ⑥ traitement : rendez-vous, puis jalons, puis état
    ⑦ unité : heure de Paris
    ⑧ pourquoi : séparer le passage de la boucle permet de l'éprouver sans attendre
    ⑨ ce qui cloche :
    une preuve vide compte comme tenue
    ⑩ effet : écrit la marque des rendez-vous annoncés
    ⑪ terminaison :
    pas de boucle ouverte, revient toujours.
      [sort: non]
    """
    h = maintenant.strftime("%Hh%M")
    u = lambda d: d.astimezone(datetime.timezone.utc)   # comparer en UTC : juste au changement d'heure (avis du superviseur, 25-10-2026)
    try:
        lignes = lire(chemin)
        if not lignes:
            return [f"ARRET {h} aucun jalon dans le fichier (fichier vide ou tronqué)"], None
        for j in lignes:
            if not all((j.get(c) or "").strip() for c in ("jalon", "echeance", "preuve")):
                return [f"ARRET {h} ligne incomplète : {j}"], None
            j["preuve"] = j["preuve"].strip()
            if j["preuve"] != "RDV" and not os.path.isabs(j["preuve"]):
                return [f"ARRET {h} preuve au chemin relatif (il faut un chemin absolu) : {j['jalon']}"], None
            j["_ech"] = datetime.datetime.strptime(j["echeance"].strip(), "%Y-%m-%d %H:%M").replace(tzinfo=P)
        ids = [j["jalon"] for j in lignes]
        if len(ids) != len(set(ids)):
            return [f"ARRET {h} identifiant de jalon en double"], None
    except Exception as e:
        return [f"ARRET {h} jalons illisibles : {e}"], None
    out = []
    # Jalons déjà vus : un jalon qui disparaît du fichier est une ERREUR, jamais un FINI (avis du superviseur, correctif ②)
    vus_f = chemin + ".vus"
    vus = set(open(vus_f, encoding="utf-8").read().split()) if os.path.exists(vus_f) else set()
    disparus = sorted(vus - set(ids))
    for d in disparus:
        out.append(f"ERREUR JALON DISPARU {h} {d} : présent à un passage précédent, absent du fichier ; si c'est voulu, retirer la ligne « {d} » de {vus_f}")
    if ecrire and set(ids) - vus:
        with open(vus_f, "a", encoding="utf-8") as f:
            f.write("\n".join(sorted(set(ids) - vus)) + "\n")
    rdv = [x for x in lignes if x["preuve"] == "RDV"]
    rdv_restants = 0
    for j in rdv:
        marque = f"{chemin}.{j['jalon']}.dit"
        if os.path.exists(marque):
            continue
        if u(maintenant) >= u(j["_ech"]):
            out.append(f"RDV {h} {j['jalon']} « {j['libelle']} »")
            if ecrire:
                with open(marque, "w", encoding="utf-8") as f:
                    f.write(h)
        else:
            rdv_restants += 1
    jalons = [x for x in lignes if x["preuve"] != "RDV"]
    tenus, attente = 0, []
    for j in jalons:
        # une preuve est un VRAI fichier, non vide (un dossier ou un fichier vide ne tient pas un jalon)
        if os.path.isfile(j["preuve"]) and os.path.getsize(j["preuve"]) > 0:
            tenus += 1
            continue
        attente.append(j)
        if u(maintenant) > u(j["_ech"]):
            out.append(f"ERREUR JALON DÉPASSÉ {h} {j['jalon']} « {j['libelle']} » échéance {j['echeance']}")
        elif (u(j["_ech"]) - u(maintenant)).total_seconds() < ALERTE_S:
            out.append(f"ALERTE {h} {j['jalon']} « {j['libelle']} » échéance {j['echeance']} dans moins de {ALERTE_S // 60} min")
    premier_passage = not vus   # au passage qui crée la liste des jalons vus, une troncature passerait inaperçue : jamais FINI
    if not attente and not rdv_restants and not disparus and not premier_passage:
        out.append(f"FINI {h} {tenus}/{len(jalons)} jalons tenus, {len(rdv)} rendez-vous annoncés")
        return out, True
    if attente:
        p = min(attente, key=lambda x: u(x["_ech"]))
        out.append(f"ETAPE {h} tenus {tenus}/{len(jalons)} — prochain {p['jalon']} « {p['libelle']} » avant {p['echeance']}")
    else:
        out.append(f"ETAPE {h} tenus {tenus}/{len(jalons)} — reste {rdv_restants} rendez-vous à annoncer")
    return out, False


def main():
    """Boucle : un passage toutes les 10 minutes jusqu'à FINI ou ARRET.

    ① rôle : faire tourner les passages
    ② contexte : lancée par le Chat sous la surveillance (§13)
    ③ entrée : sys.argv[1], le chemin du CSV
    ④ conditions : un argument, fichier existant
    ⑤ sortie :
    UNE valeur, le code de sortie (0 FINI, 2 fichier absent, 3 illisible)
      [rend: 1]
    ⑥ traitement : passage_unique
    puis pause
    ⑦ unité : secondes pour la pause
    ⑧ pourquoi : la surveillance a besoin de lignes
    régulières pour rester utile
    ⑨ ce qui cloche : la boucle ne finit que par FINI ou par la coupure
    de la surveillance
    ⑩ effet : affiche les lignes
    ⑪ terminaison : volontairement sans fin tant
    qu'un jalon manque ; la surveillance la coupe à 30 minutes.
      [sort: non]
    """
    if len(sys.argv) != 2 or not os.path.exists(sys.argv[1]):
        print("ARRET fichier de jalons absent ou non donné", flush=True)
        return 2
    while True:
        try:
            lignes, fini = passage_unique(sys.argv[1], datetime.datetime.now(P))
        except Exception as e:   # toute erreur imprévue devient un ARRET dit, jamais un Traceback muet (relecture du 25-10-2026, I3)
            lignes, fini = [f"ARRET {datetime.datetime.now(P):%Hh%M} erreur imprévue : {type(e).__name__} {e} — corriger puis relancer"], None
        for l in lignes:
            print(l, flush=True)
        if fini is None:
            return 3
        if fini:
            return 0
        time.sleep(PAUSE_S)


if __name__ == "__main__":
    sys.exit(main())
