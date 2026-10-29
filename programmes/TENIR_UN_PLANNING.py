#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fait tenir un planning par un programme : chaque jalon a une échéance et une preuve, et un retard ne se tait pas.

① RÔLE — Lire un fichier de jalons et dire, toutes les 10 minutes, où en est le
  planning : jalons tenus, prochain jalon, jalons en retard, rendez-vous avec
  Jean-Luc. Un jalon est TENU quand le fichier qui le prouve existe et n'est pas
  vide ; un rendez-vous, quand sa preuve est datée entre son échéance et l'heure
  présente. Créé le
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
  doit exister, ou, pour un rendez-vous avec Jean-Luc, « RDV » suivi d'une espace
  et du chemin ABSOLU de sa preuve. La preuve d'un rendez-vous commence par la
  ligne « <jalon> AAAA-MM-JJ HH:MM » (heure de Paris, à l'échéance ou après), puis
  les mots de Jean-Luc. Exemples réels : du 25-10-2026, « J3;2026-10-26 01:30;
  <dossier>/PROTOCOLE.md;Protocole Orange déposé avant toute mesure » ; du
  28-10-2026, « P1;2026-10-28 18:30;RDV <dossier>/preuves/P1_….txt;Plage de
  Jean-Luc : fusion… ». Un « RDV » nu, sans chemin, n'est jamais tenu.

④ CONDITIONS D ENTRÉE — Le fichier existe et se lit ; chaque échéance suit le
  format. Sinon : ligne ARRET et code 2 (fichier absent) ou 3 (illisible). Le
  fichier est relu à chaque passage : on peut ajouter un jalon sans relancer.

⑤ SORTIE — Des lignes affichées, chacune commençant par un repère, et un code de
  sortie. Repères : ETAPE (état, à chaque passage) · ALERTE (échéance dans moins
  de 30 minutes, pas encore tenue) · ERREUR JALON DÉPASSÉ (échéance passée, preuve
  absente : redit à chaque passage tant que dure le retard) · ERREUR RDV NON TENU
  (de même pour un rendez-vous) · ERREUR RDV SANS PREUVE et ERREUR PREUVE MAL
  DATÉE (redites à chaque passage) · RDV (rendez-vous atteint, dit UNE fois par
  échéance) · FINI (toutes les preuves tiennent, code 0) · ARRET (code 2 ou 3 ;
  3 aussi pour une erreur imprévue ou une marque qui ne s'écrit pas).
  Une seule valeur rendue : le code de sortie.

⑥ TRAITEMENT — À chaque passage : ① lire le fichier ; ② annoncer chaque
  rendez-vous atteint et pas encore annoncé à cette échéance (sa marque est
  écrite APRÈS l'affichage, par `poser`) ; ③ pour chaque jalon ET chaque rendez-vous, par la même boucle, juger la
  preuve (`etat_de_la_preuve`), sinon comparer l'heure à l'échéance ; ④ si tout
  tient, FINI ; sinon ETAPE avec le prochain ; ⑤ dormir 10 minutes.
  Jusqu'au 28-10-2026, un rendez-vous sortait du suivi dès son annonce : P1 a pris
  deux heures de retard sans qu'aucune ligne le dise.

⑦ UNITÉ — Heures de Paris (Europe/Paris), minutes.

⑧ POURQUOI — Une promesse de délai ne tient pas d'une conversation à l'autre ;
  un programme, si (R-754 : ce qu'un programme peut faire, un programme le fait).
  Le 25-10-2026, Jean-Luc : « comment vas-tu t'assurer que le plan sera tenu
  strictement dans les temps ? », puis « tu ne réduis pas les tâches ; il faut que
  toutes les tâches soient faites dans les délais ».

⑨ CE QUI CLOCHE — Il voit qu'un fichier EXISTE, jamais qu'il est BON : un fichier
  vide ne tient pas le jalon, mais un octet suffit. La preuve d'un rendez-vous
  est écrite par le Chat : sa date repose sur sa parole. La qualité reste aux
  relecteurs. Il meurt pendant qu'une question de l'interface attend une réponse
  (arrêt de 15h09 à 18h15 le 28-10-2026). Il ne tourne que si la
  surveillance tourne : une session arrêtée arrête tout, sans prévenir personne.
  Tenue prouvée le 25-10-2026 au soir seulement ; une nuit entière : THÉORIQUE.

⑩ EFFET — Écrit, APRÈS avoir affiché les lignes du passage (fonction `poser`),
  pour chaque rendez-vous annoncé une marque « <fichier de jalons>.<jalon>.dit »
  qui porte l'échéance annoncée, et la liste des jalons vus, « <fichier>.vus ».
  Rien d'autre.

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


def u(d):
    """Rend l'heure donnée en temps universel, pour comparer deux heures sans erreur au changement d'heure.

    ① rôle : la seule façon de comparer deux heures dans ce programme (R-708 : deux implémentations divergent)
    ② contexte : appelée par passage_unique et etat_de_la_preuve
    ③ entrée : `d`, une heure avec fuseau
    ④ conditions : `d` porte un fuseau
    ⑤ sortie : UNE valeur, la même heure en temps universel
      [rend: 1]
    ⑥ traitement : astimezone(UTC)
    ⑦ unité : heure UTC
    ⑧ pourquoi : la nuit du 25-10-2026, 02h10 existe deux fois à Paris ; comparer deux heures de Paris
    directement se trompe d'une heure (avis du superviseur du 25-10-2026)
    ⑨ ce qui cloche : —
    ⑩ effet : —
    ⑪ terminaison : revient toujours.
      [sort: non]
    """
    return d.astimezone(datetime.timezone.utc)


def passage_unique(chemin, maintenant):
    """Fait un passage : annonce, compte, et dit si tout est tenu — sans rien écrire.

    ① rôle : un examen complet du planning à l'instant donné
    ② contexte : appelée par main toutes les 10 minutes ; les épreuves l'appellent avec une heure fabriquée
    ③ entrée : `chemin`, le chemin du CSV ; `maintenant`, l'heure (datetime avec fuseau)
    ④ conditions : échéances au format AAAA-MM-JJ HH:MM ; identifiants sans espace ni « / »
    ⑤ sortie : TROIS valeurs (lignes à afficher, fini, à écrire) : fini vaut True si toutes les
    preuves tiennent, False sinon, None si le fichier est illisible ; « à écrire » est la liste des
    (chemin, texte) que main écrit APRÈS avoir affiché les lignes
      [rend: 3]
    ⑥ traitement : lire et contrôler les lignes ; jalons vus ; annonces ; une seule boucle de suivi ; état
    ⑦ unité : heure de Paris
    ⑧ pourquoi : séparer le passage de la boucle permet de l'éprouver sans attendre ; ne rien écrire ici
    empêche qu'une marque soit posée pour une annonce qui n'aurait jamais été affichée (relecture du
    28-10-2026, M3)
    ⑨ ce qui cloche : un octet tient un jalon ; la preuve d'un rendez-vous repose sur la parole du Chat
    ⑩ effet : aucun (lit des fichiers)
    ⑪ terminaison : pas de boucle ouverte, revient toujours.
      [sort: non]
    """
    h = maintenant.strftime("%Hh%M")
    try:
        lignes = lire(chemin)
        if not lignes:
            return [f"ARRET {h} aucun jalon dans le fichier (fichier vide ou tronqué)"], None, []
        for j in lignes:
            if None in j:   # une colonne en trop : un « ; » dans un chemin ou un libellé ferait lire un autre fichier (relecture du 28-10-2026, M4)
                return [f"ARRET {h} colonne en trop (un « ; » dans un chemin ou un libellé ?) : {j.get('jalon')}"], None, []
            if not all((j.get(c) or "").strip() for c in ("jalon", "echeance", "preuve")):
                return [f"ARRET {h} ligne incomplète : {j}"], None, []
            j["jalon"] = j["jalon"].strip()
            if any(c.isspace() or c == "/" for c in j["jalon"]):   # la liste .vus se coupe aux espaces (relecture du 28-10-2026, M7)
                return [f"ARRET {h} identifiant de jalon avec une espace ou un « / » : « {j['jalon']} »"], None, []
            j["preuve"] = j["preuve"].strip()
            # un rendez-vous s'écrit « RDV <chemin absolu de sa preuve> » ; « RDV » nu reste lisible, mais n'est jamais tenu (A-632, 28-10-2026)
            j["_rdv"] = j["preuve"] == "RDV" or j["preuve"].startswith("RDV ")
            j["_chemin"] = j["preuve"][3:].strip() if j["_rdv"] else j["preuve"]
            if j["_chemin"] and not os.path.isabs(j["_chemin"]):
                return [f"ARRET {h} preuve au chemin relatif (il faut un chemin absolu) : {j['jalon']}"], None, []
            j["_ech"] = datetime.datetime.strptime(j["echeance"].strip(), "%Y-%m-%d %H:%M").replace(tzinfo=P)
        ids = [j["jalon"] for j in lignes]
        if len(ids) != len(set(ids)):
            return [f"ARRET {h} identifiant de jalon en double"], None, []
    except Exception as e:
        return [f"ARRET {h} jalons illisibles : {e}"], None, []
    out, a_ecrire = [], []
    # Jalons déjà vus : un jalon qui disparaît du fichier est une ERREUR, jamais un FINI (avis du superviseur, correctif ②)
    vus_f = chemin + ".vus"
    vus = set(open(vus_f, encoding="utf-8").read().split()) if os.path.exists(vus_f) else set()
    disparus = sorted(vus - set(ids))
    for d in disparus:
        out.append(f"ERREUR JALON DISPARU {h} {d} : présent à un passage précédent, absent du fichier ; si c'est voulu, retirer la ligne « {d} » de {vus_f}")
    if set(ids) - vus:
        a_ecrire.append((vus_f, "".join(x + "\n" for x in sorted(vus | set(ids)))))
    # ANNONCE : un rendez-vous atteint est annoncé une fois PAR ÉCHÉANCE — la marque porte l'échéance annoncée,
    # donc un rendez-vous reporté est réannoncé à sa nouvelle heure (correctif ④ du 25-10-2026, fait le 28-10-2026)
    for j in lignes:
        if not j["_rdv"] or u(maintenant) < u(j["_ech"]):
            continue
        marque = f"{chemin}.{j['jalon']}.dit"
        deja = open(marque, encoding="utf-8").read().strip() if os.path.exists(marque) else ""
        if deja == j["echeance"].strip():
            continue
        out.append(f"RDV {h} {j['jalon']} « {j['libelle']} »")
        a_ecrire.append((marque, j["echeance"].strip()))
    # SUIVI : jalons ET rendez-vous passent par la même boucle (un seul code, R-708 ; superviseur du 28-10-2026)
    tenus, attente = 0, []
    for j in lignes:
        etat = etat_de_la_preuve(j, maintenant)
        if etat == "tenu":
            tenus += 1
            continue
        attente.append(j)
        if etat == "sans_preuve":
            out.append(f"ERREUR RDV SANS PREUVE {h} {j['jalon']} « {j['libelle']} » : écrire « RDV <chemin absolu> » dans la colonne preuve")
        elif etat == "mal_datee":
            out.append(f"ERREUR PREUVE MAL DATÉE {h} {j['jalon']} : la 1re ligne de {j['_chemin']} doit être « {j['jalon']} AAAA-MM-JJ HH:MM », entre l'échéance {j['echeance']} et maintenant")
        if u(maintenant) >= u(j["_ech"]):
            quoi = "ERREUR RDV NON TENU" if j["_rdv"] else "ERREUR JALON DÉPASSÉ"
            out.append(f"{quoi} {h} {j['jalon']} « {j['libelle']} » échéance {j['echeance']}")
        elif (u(j["_ech"]) - u(maintenant)).total_seconds() < ALERTE_S:
            out.append(f"ALERTE {h} {j['jalon']} « {j['libelle']} » échéance {j['echeance']} dans moins de {ALERTE_S // 60} min")
    premier_passage = not vus   # au passage qui crée la liste des jalons vus, une troncature passerait inaperçue : jamais FINI
    n_rdv = sum(1 for j in lignes if j["_rdv"])
    if not attente and not disparus and not premier_passage:
        out.append(f"FINI {h} {tenus}/{len(lignes)} tenus, dont {n_rdv} rendez-vous")
        return out, True, a_ecrire
    if attente:
        p = min(attente, key=lambda x: u(x["_ech"]))
        out.append(f"ETAPE {h} tenus {tenus}/{len(lignes)} — prochain {p['jalon']} « {p['libelle']} » avant {p['echeance']}")
    else:
        out.append(f"ETAPE {h} tenus {tenus}/{len(lignes)} — rien en attente, mais pas de FINI ce passage (premier passage ou jalon disparu)")
    return out, False, a_ecrire


def poser(a_ecrire):
    """Écrit les marques d'un passage : celle de chaque rendez-vous annoncé et la liste des jalons vus.

    ① rôle : la seule écriture du programme
    ② contexte : appelée par main APRÈS l'affichage des lignes du passage ; les épreuves l'appellent après passage_unique
    ③ entrée : `a_ecrire`, la liste des (chemin, texte) rendue par passage_unique
    ④ conditions : le dossier du fichier de jalons est inscriptible
    ⑤ sortie : —
      [rend: rien]
    ⑥ traitement : pour chaque fichier, écrire à côté puis remplacer d'un seul coup (os.replace)
    ⑦ unité : —
    ⑧ pourquoi : une marque posée avant l'affichage pouvait faire perdre une annonce pour toujours (relecture du
    28-10-2026, M3) ; écrire à côté puis remplacer évite un fichier lu à moitié écrit (§13.2 geste 6)
    ⑨ ce qui cloche : si l'affichage lui-même échoue (sortie pleine, tuyau coupé), main s'arrête avant
    d'appeler poser : l'annonce sera redite au lancement suivant, ce qui est le bon défaut. Si une écriture
    échoue ici, l'exception remonte à main, qui dit ARRET et rend 3
    ⑩ effet : écrit les fichiers « .dit » et « .vus » à côté du fichier de jalons
    ⑪ terminaison : écritures locales, revient toujours.
      [sort: non]
    """
    for chemin, texte in a_ecrire:
        with open(chemin + ".tmp", "w", encoding="utf-8") as f:
            f.write(texte)
        os.replace(chemin + ".tmp", chemin)


def etat_de_la_preuve(j, maintenant):
    """Dit où en est la preuve d'un jalon ou d'un rendez-vous, à l'heure donnée.

    ① rôle : la règle unique qui dit si une ligne du planning est tenue
    ② contexte : appelée par passage_unique, une fois par ligne et par passage
    ③ entrée : `j`, une ligne lue et préparée par passage_unique (clés `_rdv`, `_chemin`, `_ech`, `jalon`) ;
    `maintenant`, l'heure du passage (datetime avec fuseau)
    ④ conditions : `_chemin` vide ou absolu (vérifié par passage_unique)
    ⑤ sortie : UNE valeur, une chaîne parmi « tenu », « absente », « sans_preuve », « mal_datee »
      [rend: 1]
    ⑥ traitement : rendez-vous sans chemin → sans_preuve ; fichier absent, dossier ou vide → absente ;
    jalon avec fichier non vide → tenu ; rendez-vous dont l'échéance n'est pas atteinte → absente (jamais
    tenu d'avance) ; sinon la 1re ligne doit être exactement « <jalon> AAAA-MM-JJ HH:MM », heure de Paris,
    entre l'échéance et maintenant → tenu, sinon mal_datee
    ⑦ unité : heure de Paris, comparée en UTC par `u`
    ⑧ pourquoi : le 28-10-2026, le rendez-vous P1 de 18h30 est sorti du suivi dès son annonce, et deux heures
    de retard n'ont fait dire aucune ligne. La date écarte la preuve laissée par un ancien planning (le PLAN
    ORANGE avait aussi un P1) et la preuve datée dans le futur ; un rendez-vous n'est jamais tenu avant son
    échéance, sinon le veilleur disait FINI sans l'annoncer (relecture du 28-10-2026, B1)
    ⑨ ce qui cloche : la preuve d'un rendez-vous est écrite par le Chat : sa date et son contenu reposent sur sa
    parole. Une preuve préparée d'avance et datée de l'échéance tient dès l'échéance atteinte, que la plage ait
    eu lieu ou non (superviseur du 28-10-2026, essai sur copie). Le veilleur voit qu'elle est datée, jamais que
    la décision a eu lieu
    ⑩ effet : lit un fichier
    ⑪ terminaison : lecture d'une ligne d'un fichier local, revient toujours.
      [sort: non]
    """
    c = j["_chemin"]
    if j["_rdv"] and not c:
        return "sans_preuve"
    # une preuve est un VRAI fichier, non vide (un dossier ou un fichier vide ne tient pas un jalon)
    if not (os.path.isfile(c) and os.path.getsize(c) > 0):
        return "absente"
    if not j["_rdv"]:
        return "tenu"
    if u(maintenant) < u(j["_ech"]):
        return "absente"
    try:
        with open(c, encoding="utf-8-sig") as f:   # utf-8-sig : une preuve écrite avec BOM se lit (relecture du 28-10-2026, M2)
            mots = f.readline().split()
        quand = datetime.datetime.strptime(" ".join(mots[1:3]), "%Y-%m-%d %H:%M").replace(tzinfo=P)
    except (ValueError, OSError, UnicodeDecodeError):
        return "mal_datee"
    if len(mots) != 3 or mots[0] != j["jalon"] or not (u(j["_ech"]) <= u(quand) <= u(maintenant)):
        return "mal_datee"
    return "tenu"


def main():
    """Boucle : un passage toutes les 10 minutes jusqu'à FINI ou ARRET.

    ① rôle : faire tourner les passages
    ② contexte : lancée par le Chat sous la surveillance (§13)
    ③ entrée : sys.argv[1], le chemin du CSV
    ④ conditions : un argument, fichier existant
    ⑤ sortie :
    UNE valeur, le code de sortie (0 FINI, 2 fichier absent, 3 illisible ou erreur imprévue, y compris une
    marque qui ne s'écrit pas)
      [rend: 1]
    ⑥ traitement : passage_unique, affichage, puis poser les marques, puis pause — dans cet ordre : une
    marque n'est posée que pour une annonce affichée
    ⑦ unité : secondes pour la pause
    ⑧ pourquoi : la surveillance a besoin de lignes
    régulières pour rester utile
    ⑨ ce qui cloche : la boucle ne finit que par FINI ou par la coupure
    de la surveillance. Si l'AFFICHAGE lui-même échoue (sortie pleine, tuyau coupé), plus rien ne peut se
    dire : le programme s'arrête sur l'exception, sans ARRET affiché et sans poser de marque (code 120
    mesuré par la relecture du 28-10-2026) ; l'annonce sera redite au lancement suivant
    ⑩ effet : affiche les lignes ; écrit les marques par `poser`
    ⑪ terminaison : volontairement sans fin tant
    qu'un jalon manque ; la surveillance la coupe à 30 minutes.
      [sort: non]
    """
    if len(sys.argv) != 2 or not os.path.exists(sys.argv[1]):
        print("ARRET fichier de jalons absent ou non donné", flush=True)
        return 2
    while True:
        a_ecrire = []
        try:
            lignes, fini, a_ecrire = passage_unique(sys.argv[1], datetime.datetime.now(P))
        except Exception as e:   # toute erreur imprévue devient un ARRET dit, jamais un Traceback muet (relecture du 25-10-2026, I3)
            lignes, fini = [f"ARRET {datetime.datetime.now(P):%Hh%M} erreur imprévue : {type(e).__name__} {e} — corriger puis relancer"], None
        for l in lignes:
            print(l, flush=True)
        try:
            poser(a_ecrire)   # APRÈS l'affichage (relecture du 28-10-2026, M3) et DANS un try (relecture du 28-10-2026, tour 2, I2)
        except Exception as e:
            print(f"ARRET {datetime.datetime.now(P):%Hh%M} marque impossible à écrire : {type(e).__name__} {e} — corriger puis relancer", flush=True)
            return 3
        if fini is None:
            return 3
        if fini:
            return 0
        time.sleep(PAUSE_S)


if __name__ == "__main__":
    sys.exit(main())
