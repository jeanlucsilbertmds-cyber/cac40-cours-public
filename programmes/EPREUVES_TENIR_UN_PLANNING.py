#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Épreuves de TENIR_UN_PLANNING.py : chaque cas connaît d'avance la ligne qu'il doit voir.

① RÔLE — Prouver que le veilleur de planning dit ce qu'il doit dire : jalon en retard, jalon proche,
  jalon tenu, rendez-vous annoncé une fois puis suivi jusqu'à sa preuve datée, fichier illisible.
② CONTEXTE D APPEL — à la main : python3 -I programmes/EPREUVES_TENIR_UN_PLANNING.py ; et avec
  --mutations, qui rejoue toutes les épreuves contre des copies du veilleur abîmées chacune d'UNE
  façon précise : chaque copie abîmée doit faire rougir au moins une épreuve.
③ ENTRÉE — l'option --mutations, facultative.
④ CONDITIONS D ENTRÉE — TENIR_UN_PLANNING.py dans le même dossier.
⑤ SORTIE — une ligne par épreuve (ou par mutation), et UNE valeur : le code 0 si toutes passent (ou si
  toutes les mutations sont tuées), 1 sinon, 2 si une mutation ne trouve plus son texte dans le veilleur.
⑥ TRAITEMENT — fabrique des fichiers de jalons dans un dossier temporaire, appelle passage_unique avec une
  heure fixée et compare. Avec --mutations : pour chaque mutation, écrit une copie du veilleur où un texte
  exact est remplacé, la charge, rejoue les épreuves, et exige au moins un échec.
⑦ UNITÉ — heure de Paris.
⑧ POURQUOI — une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas une preuve (R-731).
  L'ancien « --saboter » ne retirait qu'une seule chose, la vue des fichiers : le superviseur du 28-10-2026
  l'a repris de la relecture du 25-10-2026, qui l'avait jugé décoratif (défaut I2). Le 28-10-2026, le rendez-vous P1 est sorti du suivi dès son
  annonce ; les épreuves R1 à R9 et le cas réel de 20h43 sont nés de ce défaut.
⑨ CE QUI CLOCHE — la boucle main est éprouvée sans sa pause de 10 minutes, avec print et poser remplacés dans le
  module (R26 à R30) ; un vrai tuyau coupé, ou une vraie sortie pleine, n'est pas joué.
⑩ EFFET — des dossiers temporaires, effacés à la fin.
⑪ TERMINAISON — aucun appel réseau, aucune boucle ouverte.
"""
import datetime
import importlib.util
import os
import shutil
import sys
import tempfile
from zoneinfo import ZoneInfo

ICI = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(ICI, "TENIR_UN_PLANNING.py")

# Chaque mutation : (nom, texte exact du veilleur, texte qui le remplace). Le texte doit exister UNE fois.
MUTATIONS = [
    ("le cri du rendez-vous en retard est retiré",
     'quoi = "ERREUR RDV NON TENU" if j["_rdv"] else "ERREUR JALON DÉPASSÉ"',
     'quoi = "ERREUR JALON DÉPASSÉ"'),
    ("le rendez-vous sort du suivi (le défaut du 28-10-2026)",
     'for j in lignes:\n        etat = etat_de_la_preuve(j, maintenant)',
     'for j in lignes:\n        if j["_rdv"]:\n            continue\n        etat = etat_de_la_preuve(j, maintenant)'),
    ("la date de la preuve d'un rendez-vous est ignorée",
     'if len(mots) != 3 or mots[0] != j["jalon"] or not (u(j["_ech"]) <= u(quand) <= u(maintenant)):',
     'if len(mots) != 3:'),
    ("une preuve datée AVANT l'échéance est acceptée",
     'not (u(j["_ech"]) <= u(quand) <= u(maintenant))',
     'not (u(quand) <= u(maintenant))'),
    ("une preuve datée dans le FUTUR est acceptée",
     'not (u(j["_ech"]) <= u(quand) <= u(maintenant))',
     'not (u(j["_ech"]) <= u(quand))'),
    ("un rendez-vous est tenu avant son échéance (le bloquant de la relecture du 28-10-2026)",
     'if u(maintenant) < u(j["_ech"]):\n        return "absente"',
     'if False:\n        return "absente"'),
    ("des mots en plus sur la 1re ligne de la preuve passent",
     'if len(mots) != 3 or mots[0]',
     'if mots[0]'),
    ("une preuve avec BOM n'est plus lue",
     'with open(c, encoding="utf-8-sig") as f:',
     'with open(c, encoding="utf-8") as f:'),
    ("« prochain » = la première ligne en attente, pas la plus ancienne (le symptôme de 20h48)",
     'p = min(attente, key=lambda x: u(x["_ech"]))',
     'p = attente[0]'),
    ("les heures ne passent plus en UTC (changement d'heure)",
     'return d.astimezone(datetime.timezone.utc)',
     'return d'),
    ("à l'instant de l'échéance, ALERTE au lieu d'ERREUR",
     'if u(maintenant) >= u(j["_ech"]):\n            quoi',
     'if u(maintenant) > u(j["_ech"]):\n            quoi'),
    ("une colonne en trop passe",
     'if None in j:',
     'if False:'),
    ("un identifiant avec une espace passe",
     'if any(c.isspace() or c == "/" for c in j["jalon"]):',
     'if False:'),
    ("un « RDV » nu compte comme tenu",
     'return "sans_preuve"',
     'return "tenu"'),
    ("l'annonce est redite à chaque passage",
     'if deja == j["echeance"].strip():\n            continue',
     'if False:\n            continue'),
    ("un rendez-vous reporté n'est pas réannoncé",
     'if deja == j["echeance"].strip():',
     'if deja:'),
    ("aucune preuve n'est vue (l'ancien sabotage)",
     'if not (os.path.isfile(c) and os.path.getsize(c) > 0):',
     'if True:'),
    ("un fichier vide tient le jalon",
     'if not (os.path.isfile(c) and os.path.getsize(c) > 0):',
     'if not os.path.isfile(c):'),
    ("la liste des vus est réécrite avec les seuls identifiants présents",
     '"".join(x + "\\n" for x in sorted(vus | set(ids)))',
     '"".join(x + "\\n" for x in sorted(set(ids)))'),
    ("main pose les marques AVANT d'afficher",
     '        for l in lignes:\n            print(l, flush=True)\n        try:\n            poser(a_ecrire)',
     '        poser(a_ecrire)\n        for l in lignes:\n            print(l, flush=True)\n        try:\n            pass'),
    ("poser hors du try de main",
     '        try:\n            poser(a_ecrire)   #',
     '        poser(a_ecrire)\n        try:\n            pass   #'),
    ("main ne pose plus aucune marque",
     '            poser(a_ecrire)   #',
     '            pass   #'),
    ("une marque impossible à écrire ne rend plus 3",
     '— corriger puis relancer", flush=True)\n            return 3',
     '— corriger puis relancer", flush=True)\n            return 0'),
    ("un fichier illisible ne rend plus 3",
     '        if fini is None:\n            return 3',
     '        if fini is None:\n            return 0'),
    ("un identifiant en double passe",
     'if len(ids) != len(set(ids)):',
     'if False:'),
    ("un « / » dans un identifiant passe",
     'c.isspace() or c == "/"',
     'c.isspace()'),
    ("une ligne sans preuve passe",
     'if not all((j.get(c) or "").strip() for c in ("jalon", "echeance", "preuve")):',
     'if False:'),
    ("à l'instant exact de l'échéance, pas d'annonce",
     'if not j["_rdv"] or u(maintenant) < u(j["_ech"]):',
     'if not j["_rdv"] or u(maintenant) <= u(j["_ech"]):'),
    ("la date de la preuve d'un rendez-vous comparée sur l'horloge, sans UTC",
     'not (u(j["_ech"]) <= u(quand) <= u(maintenant))',
     'not (j["_ech"] <= quand <= maintenant)'),
    ("un dossier tient le jalon",
     'if not (os.path.isfile(c) and os.path.getsize(c) > 0):',
     'if not (os.path.exists(c) and os.path.getsize(c) > 0):'),
    ("le garde « avant l'échéance » comparé sur l'horloge, sans UTC",
     'if u(maintenant) < u(j["_ech"]):\n        return "absente"',
     'if maintenant < j["_ech"]:\n        return "absente"'),
    ("l'annonce comparée sur l'horloge, sans UTC",
     'if not j["_rdv"] or u(maintenant) < u(j["_ech"]):',
     'if not j["_rdv"] or maintenant < j["_ech"]:'),
    ("FINI ne s'arrête plus",
     '        if fini:\n            return 0',
     '        if fini:\n            pass'),
    ("FINI rend 3",
     '        if fini:\n            return 0',
     '        if fini:\n            return 3'),
    ("main ne rattrape plus l'erreur imprévue",
     '        except Exception as e:   # toute erreur imprévue',
     '        except ZeroDivisionError as e:   # toute erreur imprévue'),
    ("fichier absent ne rend plus 2",
     '        return 2\n    while True:',
     '        return 0\n    while True:'),
    ("la liste des vus n'est jamais posée",
     'if set(ids) - vus:\n        a_ecrire.append((vus_f',
     'if False:\n        a_ecrire.append((vus_f'),
    ("le premier passage peut dire FINI",
     'premier_passage = not vus',
     'premier_passage = False'),
]


def charger(chemin):
    """Charge un fichier du veilleur comme module.

    ① rôle : rendre le module à éprouver, vrai ou abîmé
    ② contexte : appelée par le programme principal, une fois pour le vrai veilleur et une fois par mutation
    ③ entrée : `chemin`, le chemin d'un fichier Python du veilleur
    ④ conditions : le fichier existe et se compile
    ⑤ sortie : UNE valeur, le module chargé
      [rend: 1]
    ⑥ traitement : importlib, sans passer par sys.path
    ⑦ unité : —
    ⑧ pourquoi : rejouer les mêmes épreuves contre plusieurs versions du veilleur
    ⑨ ce qui cloche : —
    ⑩ effet : exécute le haut du fichier (définitions seulement : main n'est pas lancée)
    ⑪ terminaison : revient toujours.
      [sort: non]
    """
    spec = importlib.util.spec_from_file_location("planning_" + str(abs(hash(chemin))), chemin)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def passer(T, f, t):
    """Fait un passage du veilleur puis pose ses marques, comme main.

    ① rôle : rejouer exactement ce que fait un passage de main, sans l'attente
    ② contexte : appelée par `epreuves`, à chaque passage d'un cas
    ③ entrée : `T`, le module du veilleur ; `f`, le fichier de jalons ; `t`, l'heure du passage
    ④ conditions : —
    ⑤ sortie : DEUX valeurs, les lignes et « fini » du passage
      [rend: 2]
    ⑥ traitement : passage_unique, puis poser
    ⑦ unité : heure de Paris
    ⑧ pourquoi : depuis le 28-10-2026, passage_unique n'écrit plus rien ; main écrit après l'affichage
    ⑨ ce qui cloche : —
    ⑩ effet : écrit les marques du cas
    ⑪ terminaison : revient toujours
      [sort: non]
    """
    lignes, fini, a_ecrire = T.passage_unique(f, t)
    T.poser(a_ecrire)
    return lignes, fini


def epreuves(T, parler=True):
    """Joue les cas contre le module `T` et rend le nombre d'échecs.

    ① rôle : jouer chaque cas
    ② contexte : appelée une fois pour le vrai veilleur, puis une fois par mutation
    ③ entrée : `T`, le module du veilleur ; `parler`, faux pour ne rien afficher (mutations)
    ④ conditions : dossier temporaire inscriptible
    ⑤ sortie : UNE valeur, le nombre d'échecs
      [rend: 1]
    ⑥ traitement : un fichier de jalons par cas, un ou deux passages, une comparaison
    ⑦ unité : —
    ⑧ pourquoi : un cas par repère du programme, et un cas par mutation à tuer
    ⑨ ce qui cloche : —
    ⑩ effet : affiche, si `parler`
    ⑪ terminaison : revient toujours.
      [sort: non]
    """
    P = ZoneInfo("Europe/Paris")
    t = datetime.datetime(2026, 10, 26, 12, 0, tzinfo=P)
    d = tempfile.mkdtemp()
    echecs = 0

    def ecrit(nom, texte):
        """Écrit un fichier dans le dossier temporaire et rend son chemin.

        ① rôle : fabriquer une preuve ou un fichier de jalons
        ② contexte : appelée par `epreuves`
        ③ entrée : `nom`, le nom du fichier ; `texte`, son contenu
        ④ conditions : le dossier `d` existe
        ⑤ sortie : UNE valeur, le chemin écrit
          [rend: 1]
        ⑥ traitement : écrire
        ⑦ unité : —
        ⑧ pourquoi : chaque cas a ses propres fichiers, pour que ses marques ne se mêlent pas à celles d'un autre
        ⑨ ce qui cloche : —
        ⑩ effet : écrit un fichier
        ⑪ terminaison : revient toujours
          [sort: non]
        """
        f = os.path.join(d, nom)
        with open(f, "w", encoding="utf-8") as h:
            h.write(texte)
        return f

    def fichier(nom, lignes):
        """Écrit un fichier de jalons d'épreuve et rend son chemin.

        ① rôle : fabriquer le fichier de jalons d'un cas
        ② contexte : appelée par `epreuves`, une fois par cas
        ③ entrée : `nom`, le nom du fichier ; `lignes`, les lignes de jalons sans l'en-tête
        ④ conditions : le dossier temporaire `d` existe
        ⑤ sortie : UNE valeur, le chemin du fichier écrit
          [rend: 1]
        ⑥ traitement : écrire l'en-tête « jalon;echeance;preuve;libelle », puis les lignes
        ⑦ unité : —
        ⑧ pourquoi : chaque cas a son propre fichier
        ⑨ ce qui cloche : —
        ⑩ effet : écrit un fichier dans le dossier temporaire
        ⑪ terminaison : revient toujours
          [sort: non]
        """
        return ecrit(nom, "jalon;echeance;preuve;libelle\n" + "\n".join(lignes) + "\n")

    def juger(nom, ok, lignes):
        """Compte et affiche le verdict d'un cas.

        ① rôle : une ligne OK ou ÉCHEC par cas
        ② contexte : appelée par `epreuves`
        ③ entrée : `nom` ; `ok`, le verdict ; `lignes`, ce que le veilleur a dit
        ④ conditions : —
        ⑤ sortie : — (le compte d'échecs est mis à jour)
          [rend: rien]
        ⑥ traitement : incrémenter, afficher
        ⑦ unité : —
        ⑧ pourquoi : un seul format de verdict
        ⑨ ce qui cloche : —
        ⑩ effet : affiche, si `parler`
        ⑪ terminaison : revient toujours
          [sort: non]
        """
        nonlocal echecs
        echecs += not ok
        if parler:
            print(("OK  " if ok else "ÉCHEC ") + nom + " → " + " | ".join(lignes), flush=True)

    preuve = ecrit("preuve.md", "x")
    absent = os.path.join(d, "absent.md")
    vide = ecrit("vide.md", "")

    try:
        # ---- les cas d'un seul passage (après un premier passage muet, qui crée la liste des jalons vus)
        cas = [
            ("retard sans preuve", fichier("a.csv", [f"A;2026-10-26 11:00;{absent};x"]), "ERREUR JALON DÉPASSÉ", False),
            ("retard avec preuve = tenu", fichier("b.csv", [f"B;2026-10-26 11:00;{preuve};x"]), "FINI", True),
            ("échéance dans 20 min", fichier("c.csv", [f"C;2026-10-26 12:20;{absent};x"]), "ALERTE", False),
            ("échéance lointaine", fichier("e.csv", [f"E;2026-10-27 12:00;{absent};x", f"F;2026-10-26 11:00;{preuve};y"]), "ETAPE 12h00 tenus 1/2", False),
            ("échéance illisible", fichier("i.csv", [f"I;26/10/2026;{absent};x"]), "ARRET", None),
            ("fichier réduit à l'en-tête : ARRET, jamais FINI", fichier("v.csv", []), "ARRET", None),
            ("preuve vide : pas tenue", fichier("z.csv", [f"Z;2026-10-26 11:00;{vide};x"]), "ERREUR JALON DÉPASSÉ", False),
            ("preuve au chemin relatif : ARRET", fichier("rel.csv", ["Q;2026-10-27 11:00;preuve.md;x"]), "ARRET", None),
            ("preuve de rendez-vous au chemin relatif : ARRET", fichier("relr.csv", ["Q;2026-10-27 11:00;RDV preuve.md;x"]), "ARRET", None),
            # cas réel du PLAN ORANGE : J10 (bilan) prouvé avant le rendez-vous P4 de la même heure -> pas FINI tant que P4 n'est pas prouvé
            ("jalon tenu avant le dernier rendez-vous : pas FINI", fichier("p4.csv", [f"J10;2026-10-27 18:25;{preuve};bilan", f"P4;2026-10-27 18:25;RDV {absent};plage"]), "ETAPE", False),
        ]
        for nom, f, attendu, fini_attendu in cas:
            premier, f1 = passer(T, f, t)
            if fini_attendu is True and f1 is not False:
                juger(nom + " : FINI dès le premier passage", False, premier)
                continue
            lignes, fini = passer(T, f, t)
            juger(nom, any(l.startswith(attendu) for l in lignes) and fini == fini_attendu, lignes)

        # ---- R1 à R3 : un rendez-vous atteint sans preuve est annoncé UNE fois, puis redit en retard à chaque passage
        f = fichier("r.csv", [f"R;2026-10-26 11:55;RDV {absent};plage", f"G;2026-10-27 12:00;{absent};y"])
        l1, f1 = passer(T, f, t)
        l2, f2 = passer(T, f, t)
        juger("R1 rendez-vous atteint : annoncé", any(l.startswith("RDV 12h00 R") for l in l1), l1)
        juger("R2 annonce unique : pas redite au passage suivant", not any(l.startswith("RDV") for l in l2), l2)
        juger("R3 rendez-vous sans preuve : « NON TENU » redit aux deux passages, jamais FINI",
              any(l.startswith("ERREUR RDV NON TENU 12h00 R") for l in l1) and any(l.startswith("ERREUR RDV NON TENU 12h00 R") for l in l2)
              and f1 is False and f2 is False, l2)
        juger("R4 le rendez-vous en retard est le « prochain », pas le jalon suivant",
              any(l.startswith("ETAPE") and "prochain R " in l for l in l2), l2)

        # ---- R5 : preuve datée à l'échéance ou après → tenu, FINI
        bon = ecrit("bon.txt", "R5 2026-10-26 11:58\nJean-Luc : « 1 »\n")
        f = fichier("r5.csv", [f"R5;2026-10-26 11:55;RDV {bon};plage"])
        passer(T, f, t)
        lignes, fini = passer(T, f, t)
        juger("R5 preuve datée après l'échéance : tenu, FINI", fini is True and any(l.startswith("FINI") for l in lignes), lignes)

        # ---- R6 : preuve datée AVANT l'échéance → mal datée, pas tenu
        tot = ecrit("tot.txt", "R6 2026-10-26 11:00\nécrite avant le rendez-vous\n")
        f = fichier("r6.csv", [f"R6;2026-10-26 11:55;RDV {tot};plage"])
        passer(T, f, t)
        lignes, fini = passer(T, f, t)
        juger("R6 preuve datée avant l'échéance : pas tenue",
              fini is False and any(l.startswith("ERREUR PREUVE MAL DATÉE") for l in lignes), lignes)

        # ---- R7 : preuve d'un autre jour (le P1 du PLAN ORANGE, le 25-10) → mal datée
        vieux = ecrit("vieux.txt", "R7 2026-10-25 08:30\nancien planning\n")
        f = fichier("r7.csv", [f"R7;2026-10-26 11:55;RDV {vieux};plage"])
        passer(T, f, t)
        lignes, fini = passer(T, f, t)
        juger("R7 preuve d'un autre jour : pas tenue", fini is False and any(l.startswith("ERREUR PREUVE MAL DATÉE") for l in lignes), lignes)

        # ---- R7b : preuve au nom d'un autre rendez-vous → mal datée ; sans date → mal datée
        autre = ecrit("autre.txt", "P9 2026-10-26 11:58\n")
        nue = ecrit("nue.txt", "x")
        f = fichier("r7b.csv", [f"R7;2026-10-26 11:55;RDV {autre};plage", f"R8;2026-10-26 11:55;RDV {nue};plage"])
        passer(T, f, t)
        lignes, fini = passer(T, f, t)
        juger("R7b preuve au nom d'un autre, ou sans date : pas tenues",
              fini is False and sum(l.startswith("ERREUR PREUVE MAL DATÉE") for l in lignes) == 2, lignes)

        # ---- R8 : « RDV » nu → SANS PREUVE redit, jamais FINI
        f = fichier("r8.csv", ["R8;2026-10-26 11:55;RDV;plage"])
        passer(T, f, t)
        lignes, fini = passer(T, f, t)
        juger("R8 « RDV » nu : SANS PREUVE, jamais FINI",
              fini is False and any(l.startswith("ERREUR RDV SANS PREUVE") for l in lignes), lignes)

        # ---- R9 : un rendez-vous reporté est réannoncé à sa nouvelle heure, une fois
        f = fichier("r9.csv", [f"R9;2026-10-26 11:50;RDV {absent};plage"])
        passer(T, f, t)
        fichier("r9.csv", [f"R9;2026-10-26 11:57;RDV {absent};plage reportée"])
        l1, _ = passer(T, f, t)
        l2, _ = passer(T, f, t)
        juger("R9 report : réannoncé une fois à la nouvelle échéance",
              any(l.startswith("RDV 12h00 R9") for l in l1) and not any(l.startswith("RDV") for l in l2), l1 + l2)

        # ---- R10 : un rendez-vous pas encore atteint n'est pas annoncé, et alerte 30 min avant
        f = fichier("r10.csv", [f"R10;2026-10-26 12:20;RDV {absent};plage"])
        passer(T, f, t)
        lignes, fini = passer(T, f, t)
        juger("R10 rendez-vous dans 20 min : ALERTE, pas d'annonce",
              any(l.startswith("ALERTE") for l in lignes) and not any(l.startswith("RDV") for l in lignes) and fini is False, lignes)

        # ---- le cas réel du 28-10-2026 à 20h43 : J1 tenu, P1 (18h30) sans preuve, J2 demain
        j1 = ecrit("J1.txt", "preuve de J1")
        f = fichier("reel.csv", [
            f"J1;2026-10-28 18:00;{j1};A-629 ①",
            f"P1;2026-10-28 18:30;RDV {absent};Plage de Jean-Luc : fusion, puis trois décisions",
            f"J2;2026-10-29 08:30;{absent};certificat du 29-10"])
        ecrit("reel.csv.P1.dit", "2026-10-28 18:30")       # P1 déjà annoncé, comme le 28-10 à 18h37
        ecrit("reel.csv.vus", "J1\nP1\nJ2\n")
        lignes, fini = passer(T, f, datetime.datetime(2026, 10, 28, 20, 43, tzinfo=P))
        juger("cas réel de 20h43 : P1 dit en retard et « prochain », jamais oublié",
              any(l.startswith("ERREUR RDV NON TENU 20h43 P1") for l in lignes)
              and any(l.startswith("ETAPE 20h43 tenus 1/3 — prochain P1") for l in lignes)
              and not any(l.startswith("RDV") for l in lignes) and fini is False, lignes)

        # ---- R11 (bloquant de la relecture du 28-10-2026) : preuve préparée d'avance, datée de l'échéance future.
        # Avant l'échéance : jamais tenue, jamais FINI. Après : elle tient — c'est la limite déclarée (parole du Chat).
        avance = ecrit("avance.txt", "R11 2026-10-26 12:30\npréparée d'avance\n")
        f = fichier("r11.csv", [f"R11;2026-10-26 12:30;RDV {avance};plage future"])
        passer(T, f, t)
        l1, f1 = passer(T, f, t)
        l2, f2 = passer(T, f, datetime.datetime(2026, 10, 26, 12, 40, tzinfo=P))
        juger("R11 preuve préparée d'avance : pas FINI avant l'échéance, annoncé puis tenu après",
              f1 is False and not any(l.startswith("FINI") for l in l1)
              and not any(l.startswith("ERREUR") for l in l1)   # avant l'heure, une preuve prête n'est pas une faute : silence
              and f2 is True and any(l.startswith("RDV 12h40 R11") for l in l2), l1 + l2)

        # ---- R12 : preuve datée dans le futur → mal datée
        futur = ecrit("futur.txt", "R12 2026-10-26 14:00\n")
        f = fichier("r12.csv", [f"R12;2026-10-26 11:55;RDV {futur};plage"])
        passer(T, f, t)
        lignes, fini = passer(T, f, t)
        juger("R12 preuve datée dans le futur : pas tenue", fini is False and any(l.startswith("ERREUR PREUVE MAL DATÉE") for l in lignes), lignes)

        # ---- R13 : des mots en plus sur la 1re ligne → mal datée ; une preuve avec BOM se lit
        bavard = ecrit("bavard.txt", "R13 2026-10-26 11:58 et des mots en plus\n")
        bom = ecrit("bom.txt", "\ufeffR14 2026-10-26 11:58\nJean-Luc : « 1 »\n")
        f = fichier("r13.csv", [f"R13;2026-10-26 11:55;RDV {bavard};plage", f"R14;2026-10-26 11:55;RDV {bom};plage"])
        passer(T, f, t)
        lignes, fini = passer(T, f, t)
        juger("R13 1re ligne avec des mots en plus : mal datée ; preuve avec BOM : tenue",
              fini is False and sum(l.startswith("ERREUR PREUVE MAL DATÉE") for l in lignes) == 1
              and any("R13" in l and l.startswith("ERREUR PREUVE MAL DATÉE") for l in lignes)
              and any(l.startswith("ETAPE 12h00 tenus 1/2") for l in lignes), lignes)

        # ---- R15 : « prochain » = l'échéance la plus ancienne en attente, pas la première ligne du fichier
        f = fichier("r15.csv", [f"Z9;2026-10-29 08:30;{absent};demain", f"P1;2026-10-26 10:00;RDV {absent};plage passée", f"Z8;2026-10-27 09:00;{absent};après-demain"])
        passer(T, f, t)
        lignes, fini = passer(T, f, t)
        juger("R15 « prochain » = le plus ancien en attente", any(l.startswith("ETAPE") and "prochain P1 " in l for l in lignes), lignes)

        # ---- R16 : la nuit du 25-10-2026, 02h00-03h00 existe deux fois à Paris. Échéance 02h30 de la PREMIÈRE heure (00h30 UTC) ;
        # passage à la SECONDE 02h10 (fold=1, 01h10 UTC) : l'échéance est dépassée. Comparées sans passer en UTC, deux heures de
        # Paris se comparent sur l'horloge (02h10 < 02h30) et le veilleur dirait ALERTE.
        f = fichier("r16.csv", [f"R16;2026-10-25 02:30;{absent};nuit du changement d'heure"])
        nuit = datetime.datetime(2026, 10, 25, 2, 10, fold=1, tzinfo=P)
        passer(T, f, nuit)
        lignes, fini = passer(T, f, nuit)
        juger("R16 changement d'heure : ERREUR à la seconde 02h10, pas ALERTE",
              any(l.startswith("ERREUR JALON DÉPASSÉ") for l in lignes) and not any(l.startswith("ALERTE") for l in lignes), lignes)

        # ---- R17 : à l'instant exact de l'échéance, ERREUR et non ALERTE (relecture du 28-10-2026, M8)
        f = fichier("r17.csv", [f"R17;2026-10-26 12:00;{absent};x"])
        passer(T, f, t)
        lignes, fini = passer(T, f, t)
        juger("R17 à l'instant de l'échéance : ERREUR, pas ALERTE",
              any(l.startswith("ERREUR JALON DÉPASSÉ") for l in lignes) and not any(l.startswith("ALERTE") for l in lignes), lignes)

        # ---- R18 : une colonne en trop (un « ; » dans un chemin) → ARRET ; un identifiant avec une espace → ARRET
        f = ecrit("r18.csv", "jalon;echeance;preuve;libelle\n" + f"R18;2026-10-26 11:00;{d}/a;b.md;x\n")
        lignes, fini = passer(T, f, t)
        juger("R18 colonne en trop : ARRET", fini is None and any(l.startswith("ARRET") for l in lignes), lignes)
        f = fichier("r19.csv", [f"J 1;2026-10-26 11:00;{preuve};x"])
        lignes, fini = passer(T, f, t)
        juger("R19 identifiant avec une espace : ARRET", fini is None and any(l.startswith("ARRET") for l in lignes), lignes)

        # ---- R20 à R23 : les gardes de lecture (relecture du 28-10-2026, tour 2, mineurs)
        f = fichier("r20.csv", [f"D;2026-10-26 11:00;{preuve};x", f"D;2026-10-26 11:00;{preuve};y"])
        lignes, fini = passer(T, f, t)
        juger("R20 identifiant en double : ARRET", fini is None and any(l.startswith("ARRET") for l in lignes), lignes)
        f = fichier("r21.csv", [f"J/1;2026-10-26 11:00;{preuve};x"])
        lignes, fini = passer(T, f, t)
        juger("R21 identifiant avec un « / » : ARRET", fini is None and any(l.startswith("ARRET") for l in lignes), lignes)
        f = fichier("r22.csv", ["J;2026-10-26 11:00;;x"])
        lignes, fini = passer(T, f, t)
        juger("R22 ligne sans preuve : ARRET", fini is None and any(l.startswith("ARRET") for l in lignes), lignes)
        f = fichier("r23.csv", [f"R23;2026-10-26 12:00;RDV {absent};plage"])
        lignes, fini = passer(T, f, t)
        juger("R23 annonce à l'instant exact de l'échéance", any(l.startswith("RDV 12h00 R23") for l in lignes), lignes)

        # ---- R24 : un rendez-vous au changement d'heure — échéance 02h30 de la 1re heure (00h30 UTC), preuve datée 02h50
        # (1re heure, 00h50 UTC), passage à la 2e 02h40 (fold=1, 01h40 UTC) : la preuve tombe entre les deux, donc tenue.
        # Comparée sur l'horloge sans passer en UTC, 02h50 > 02h40 : elle serait dite MAL DATÉE.
        nuit_p = ecrit("nuit.txt", "R24 2026-10-25 02:50\n")
        f = fichier("r24.csv", [f"R24;2026-10-25 02:30;RDV {nuit_p};plage de nuit"])
        # Passage à la 2e 02h10 (fold=1, 01h10 UTC) : sur l'horloge, 02h10 < 02h30 ferait croire l'échéance pas encore
        # atteinte (garde « avant l'échéance ») ; en UTC elle l'est (relecture du 28-10-2026, tour 3, survivant MF).
        nuit2 = datetime.datetime(2026, 10, 25, 2, 10, fold=1, tzinfo=P)
        l1, _ = passer(T, f, nuit2)
        lignes, fini = passer(T, f, nuit2)
        juger("R24 rendez-vous au changement d'heure : annoncé et tenu, comparé en UTC",
              fini is True and any(l.startswith("RDV 02h10 R24") for l in l1), l1 + lignes)

        # ---- R25 (relecture du 28-10-2026, tour 2, I3 ; superviseur, condition 1) : B retiré ET C ajouté au même passage ;
        # au 3e passage, B est encore DISPARU et rien n'est FINI — la liste des vus ne perd jamais un identifiant
        f = fichier("r25.csv", [f"A;2026-10-26 11:00;{preuve};x", f"B;2026-10-26 11:00;{preuve};y"])
        passer(T, f, t)
        fichier("r25.csv", [f"A;2026-10-26 11:00;{preuve};x", f"C;2026-10-26 11:00;{preuve};z"])
        l2, f2 = passer(T, f, t)
        l3, f3 = passer(T, f, t)
        juger("R25 jalon retiré pendant qu'un autre arrive : encore DISPARU au 3e passage, pas de FINI",
              any(l.startswith("ERREUR JALON DISPARU 12h00 B") for l in l3) and f2 is False and f3 is False, l3)

        # ---- R26 à R30 : la boucle main elle-même (relecture du 28-10-2026, tour 2, I1 et I2)
        class _Arret(Exception):
            """Exception d'arrêt levée par `dormir` pour sortir de la boucle de main au n-ième passage."""
        vrai_poser, vrai_sleep, vrai_argv = T.poser, T.time.sleep, sys.argv
        def jouer_main(fjal, n_passages, imprimer=None, poser=None):
            """Joue main sur `fjal` pendant n passages et rend (code, journal des gestes).

            ① rôle : faire tourner la vraie boucle main sans attendre 10 minutes
            ② contexte : appelée par les épreuves R26 à R30
            ③ entrée : `fjal` le fichier de jalons ; `n_passages` ; `imprimer` et `poser`, des remplaçants facultatifs
            ④ conditions : —
            ⑤ sortie : DEUX valeurs, le code rendu (ou le nom de l'exception) et la liste des gestes
              [rend: 2]
            ⑥ traitement : remplacer sleep (arrêt au n-ième passage), print du module et poser par des enregistreurs
            ⑦ unité : —
            ⑧ pourquoi : l'ordre « afficher puis poser » et les codes de sortie vivent dans main, que rien n'éprouvait
            ⑨ ce qui cloche : print est remplacé dans le module seulement
            ⑩ effet : rend toujours au module ses vraies fonctions
            ⑪ terminaison : sleep lève _Arret au n-ième appel, donc revient toujours
              [sort: non]
            """
            gestes, compte = [], [0]
            def dormir(_):
                """remplace time.sleep : compte les passages et arrête la boucle au n-ième

                ① rôle : remplace time.sleep : compte les passages et arrête la boucle au n-ième
                ② contexte : main, à la fin de chaque passage
                ③ entrée : `_`, la durée demandée, ignorée
                ④ conditions : —
                ⑤ sortie : —
                  [rend: rien]
                ⑥ traitement : compter ; lever _Arret au n-ième
                ⑦ unité : —
                ⑧ pourquoi : éprouver main sans attendre 10 minutes
                ⑨ ce qui cloche : —
                ⑩ effet : lève _Arret
                ⑪ terminaison : revient toujours, ou lève exprès
                  [sort: non]
                """
                compte[0] += 1
                if compte[0] >= n_passages:
                    raise _Arret()
            def imp(*a, **k):
                """remplace print dans le module : enregistre la ligne, puis appelle le remplaçant d'affichage s'il y en a un

                ① rôle : remplace print dans le module : enregistre la ligne, puis appelle le remplaçant d'affichage s'il y en a un
                ② contexte : main, à chaque ligne affichée
                ③ entrée : `a` et `k`, les arguments de print ; la ligne est `a[0]`
                ④ conditions : —
                ⑤ sortie : —
                  [rend: rien]
                ⑥ traitement : noter ; appeler `imprimer`
                ⑦ unité : —
                ⑧ pourquoi : voir l'ordre afficher-puis-poser
                ⑨ ce qui cloche : —
                ⑩ effet : ajoute au journal des gestes
                ⑪ terminaison : revient toujours, ou lève exprès
                  [sort: non]
                """
                gestes.append(("print", str(a[0]) if a else ""))
                if imprimer:
                    imprimer()
            def pos(x):
                """remplace poser : enregistre l'appel, puis appelle le vrai poser ou son remplaçant

                ① rôle : remplace poser : enregistre l'appel, puis appelle le vrai poser ou son remplaçant
                ② contexte : main, après l'affichage
                ③ entrée : `x`, la liste des marques à écrire
                ④ conditions : —
                ⑤ sortie : —
                  [rend: rien]
                ⑥ traitement : noter ; appeler
                ⑦ unité : —
                ⑧ pourquoi : voir l'ordre afficher-puis-poser et les marques réellement posées
                ⑨ ce qui cloche : —
                ⑩ effet : ajoute au journal ; écrit les marques si c'est le vrai poser
                ⑪ terminaison : revient toujours, ou lève exprès
                  [sort: non]
                """
                gestes.append(("poser", len(x)))
                (poser or vrai_poser)(x)
            T.time.sleep, T.poser, sys.argv = dormir, pos, ["veilleur", fjal]
            T.print = imp
            try:
                code = T.main()
            except _Arret:
                code = "arrêté"
            except Exception as e:
                code = type(e).__name__
            finally:
                T.time.sleep, T.poser, sys.argv = vrai_sleep, vrai_poser, vrai_argv
                del T.print
            return code, gestes

        f = fichier("m1.csv", [f"M1;2026-10-26 11:55;RDV {absent};plage", f"G;2099-01-01 12:00;{absent};loin"])
        code, gestes = jouer_main(f, 2)
        annonces = [g for g in gestes if g[0] == "print" and g[1].startswith("RDV")]
        prem_poser = next(i for i, g in enumerate(gestes) if g[0] == "poser")
        juger("R26 main : affiche AVANT de poser, et l'annonce n'est pas redite au 2e passage",
              len(annonces) == 1 and gestes.index(annonces[0]) < prem_poser and os.path.exists(f + ".M1.dit"), [str(gestes)])

        def plein():
            """simule une sortie pleine (/dev/full) : lève OSError

            ① rôle : simule une sortie pleine (/dev/full) : lève OSError
            ② contexte : imp, à chaque ligne affichée
            ③ entrée : —
            ④ conditions : —
            ⑤ sortie : —
              [rend: rien]
            ⑥ traitement : lever OSError 28
            ⑦ unité : —
            ⑧ pourquoi : le cas mesuré par la relecture du tour 2 : l'annonce perdue
            ⑨ ce qui cloche : —
            ⑩ effet : lève
            ⑪ terminaison : revient toujours, ou lève exprès
              [sort: oui]
            """
            raise OSError(28, "No space left on device")
        f = fichier("m2.csv", [f"M2;2026-10-26 11:55;RDV {absent};plage"])
        code, gestes = jouer_main(f, 2, imprimer=plein)
        juger("R27 main : un affichage qui échoue ne pose aucune marque", code == "OSError" and not os.path.exists(f + ".M2.dit"), [str(code), str(gestes)])

        def casse(_):
            """simule une marque qui ne s'écrit pas : lève OSError

            ① rôle : simule une marque qui ne s'écrit pas : lève OSError
            ② contexte : main, à la place de poser
            ③ entrée : `_`, la liste des marques, ignorée
            ④ conditions : —
            ⑤ sortie : —
              [rend: rien]
            ⑥ traitement : lever OSError 13
            ⑦ unité : —
            ⑧ pourquoi : main doit rendre 3 (relecture du tour 2, I2)
            ⑨ ce qui cloche : —
            ⑩ effet : lève
            ⑪ terminaison : revient toujours, ou lève exprès
              [sort: oui]
            """
            raise OSError(13, "Permission denied")
        f = fichier("m3.csv", [f"M3;2026-10-26 11:55;RDV {absent};plage"])
        code, gestes = jouer_main(f, 2, poser=casse)
        juger("R28 main : une marque qui ne s'écrit pas rend 3 et le dit", code == 3 and any(g[0] == "print" and g[1].startswith("ARRET") for g in gestes), [str(code), str(gestes)])

        f = fichier("m4.csv", [f"M4;2026-10-26 11:00;{preuve};x"])
        ecrit("m4.csv.vus", "M4\n")
        code, gestes = jouer_main(f, 2, poser=casse)
        juger("R29 main : FINI affiché puis marque qui échoue rend 3, jamais 0", code == 3, [str(code), str(gestes)])

        f = fichier("m5.csv", [f"M5;26/10/2026;{absent};x"])
        code, gestes = jouer_main(f, 2)
        juger("R30 main : un fichier illisible rend 3", code == 3, [str(code), str(gestes)])

        # ---- R31 (relecture du 28-10-2026, tour 3) : un dossier ne tient pas un jalon
        os.mkdir(os.path.join(d, "dossier_preuve"))
        f = fichier("r31.csv", [f"R31;2026-10-26 18:00;{d}/dossier_preuve;rapport"])
        passer(T, f, t)
        lignes, fini = passer(T, f, t)
        juger("R31 un dossier ne tient pas un jalon", fini is False and any(l.startswith("ETAPE 12h00 tenus 0/1") for l in lignes), lignes)

        # ---- R32 à R34 : main jusqu'au bout — vrai poser, FINI au 2e passage, code 0 ; erreur imprévue → 3 ; fichier absent → 2
        f = fichier("m6.csv", [f"M6;2026-10-26 11:00;{preuve};x"])
        code, gestes = jouer_main(f, 3)
        juger("R32 main : vrai poser, sans .vus, FINI au 2e passage et code 0",
              code == 0 and sum(g[0] == "poser" for g in gestes) == 2 and any(g[0] == "print" and g[1].startswith("FINI") for g in gestes), [str(code), str(gestes)])
        vrai_passage = T.passage_unique
        def panne(*a, **k):
            """simule une erreur imprévue du passage : lève RuntimeError

            ① rôle : simule une erreur imprévue du passage : lève RuntimeError
            ② contexte : main, à la place de passage_unique
            ③ entrée : `a` et `k`, les arguments du passage, ignorés
            ④ conditions : —
            ⑤ sortie : —
              [rend: rien]
            ⑥ traitement : lever RuntimeError
            ⑦ unité : —
            ⑧ pourquoi : main doit dire ARRET et rendre 3 (relecture du tour 3, N3)
            ⑨ ce qui cloche : —
            ⑩ effet : lève
            ⑪ terminaison : revient toujours, ou lève exprès
              [sort: oui]
            """
            raise RuntimeError("panne d'épreuve")
        T.passage_unique = panne
        try:
            code, gestes = jouer_main(fichier("m7.csv", [f"M7;2026-10-26 11:00;{preuve};x"]), 2)
        finally:
            T.passage_unique = vrai_passage
        juger("R33 main : une erreur imprévue devient ARRET, code 3",
              code == 3 and any(g[0] == "print" and g[1].startswith("ARRET") for g in gestes), [str(code), str(gestes)])
        code, gestes = jouer_main(os.path.join(d, "n_existe_pas.csv"), 2)
        juger("R34 main : fichier de jalons absent, code 2", code == 2, [str(code), str(gestes)])

        # ---- un jalon qui disparaît d'un passage à l'autre : ERREUR, jamais FINI
        f = fichier("dis.csv", [f"A;2026-10-26 11:00;{preuve};x", f"B;2026-10-26 11:00;{absent};y"])
        passer(T, f, t)
        fichier("dis.csv", [f"A;2026-10-26 11:00;{preuve};x"])
        lignes, fini = passer(T, f, t)
        juger("jalon disparu", any(l.startswith("ERREUR JALON DISPARU") for l in lignes) and fini is False, lignes)

        # ---- un essai sans écriture ne pose aucune marque de rendez-vous
        f = fichier("ess.csv", [f"R9;2026-10-26 11:00;RDV {absent};x", f"G;2026-10-27 12:00;{absent};y"])
        T.passage_unique(f, t)
        juger("passage_unique seul n'écrit rien : aucune marque, aucune liste des vus",
              not os.path.exists(f + ".R9.dit") and not os.path.exists(f + ".vus"), [])
    except Exception as e:      # une copie abîmée peut planter : c'est un échec, jamais un silence
        juger(f"plantage {type(e).__name__} {e}", False, [])
    finally:
        shutil.rmtree(d)
    return echecs


def mutations():
    """Rejoue les épreuves contre chaque copie abîmée du veilleur et rend le code de sortie.

    ① rôle : prouver que chaque épreuve a des dents
    ② contexte : appelée quand l'option --mutations est donnée
    ③ entrée : —
    ④ conditions : chaque texte de MUTATIONS existe UNE fois dans le veilleur
    ⑤ sortie : UNE valeur, 0 si toutes les mutations sont tuées, 1 si l'une survit, 2 si un texte est introuvable
      [rend: 1]
    ⑥ traitement : copier le veilleur, remplacer le texte, charger, rejouer, compter les échecs
    ⑦ unité : —
    ⑧ pourquoi : une mutation qui survit est une épreuve décorative (R-731)
    ⑨ ce qui cloche : une mutation dont le texte a changé dans le veilleur ne mesure plus rien : code 2, jamais un vert
    ⑩ effet : un dossier temporaire, effacé à la fin ; affiche une ligne par mutation
    ⑪ terminaison : revient toujours.
      [sort: non]
    """
    src = open(SOURCE, encoding="utf-8").read()
    d = tempfile.mkdtemp()
    code = 0
    try:
        for i, (nom, avant, apres) in enumerate(MUTATIONS, 1):
            n = src.count(avant)
            if n != 1:
                print(f"INTROUVABLE M{i} {nom} : le texte apparaît {n} fois dans le veilleur", flush=True)
                code = 2
                continue
            chemin = os.path.join(d, f"mutant_{i}.py")
            with open(chemin, "w", encoding="utf-8") as h:
                h.write(src.replace(avant, apres))
            try:
                e = epreuves(charger(chemin), parler=False)
            except Exception as x:
                e = 1
                nom += f" (plantage au chargement : {type(x).__name__})"
            print(("TUÉE    " if e else "SURVIT  ") + f"M{i} {nom} — {e} épreuve(s) rougie(s)", flush=True)
            if not e and code == 0:
                code = 1
    finally:
        shutil.rmtree(d)
    return code


if __name__ == "__main__":
    if "--mutations" in sys.argv:
        sys.exit(mutations())
    n = epreuves(charger(SOURCE))
    print(f"{'TOUT PASSE' if n == 0 else str(n) + ' ÉCHEC(S)'}", flush=True)
    sys.exit(0 if n == 0 else 1)
