#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_RELEVER_LES_BLOCAGES_ET_RATTACHEMENT — Jeu 26-11-2026 (Paris)
Rôle : prouver que programmes/RELEVER_LES_BLOCAGES.py et programmes/VERIFIER_LE_RATTACHEMENT.py rendent les codes
que leur fiche annonce, et que l'épreuve a des dents (R-731, R-755 ②). Simulation uniquement : aucun ordre réel.
Quand l'appeler : avant toute livraison qui touche l'un de ces deux programmes.

À QUOI ÇA SERT. Ces deux programmes sont des contrôles de confiance (A-1011 : un blocage écrit est relevé ; A-1014 :
un travail sert une décision). Un contrôle qui rend 0 quoi qu'il arrive ne contrôle rien. L'épreuve lance chaque
programme, par sous-processus, sur des COPIES posées dans un dossier temporaire : jamais sur le dépôt.

LES CAS (chacun dit le code attendu et un mot attendu dans la sortie) :
  R1  vraie ligne A-1055 du BACKLOG (R-732), rapport du « Pilote V8 » qui écrit « BLOCAGE ⑥ » → code 3
  R2  un rapport du pilote sans le mot → code 0, « AUCUN BLOCAGE »
  R3  aucun rapport du pilote → code 2, « AUCUN RAPPORT DU PILOTE »
  R4  N = 1 : un blocage dans l'avant-dernier rapport seulement → code 0 (seuls les N derniers sont lus)
  R5  le mot écrit par le Chat (colonne responsable « Chat ») n'est pas relevé → code 0
  V1  vraie ligne A-1014 du BACKLOG (R-732, statut DÉCIDÉ), note « SERT : A-1014 » → code 0, « RATTACHÉ »
  V2  note sans ligne « SERT : A-… » → code 3, « NON RATTACHÉ »
  V3  note qui sert une action absente du BACKLOG → code 3
  V4  note qui sert une action non décidée (À FAIRE) → code 3
  V5  aucune paire ÉTIQUETTE=CHEMIN → code 2, « USAGE »
LES SABOTAGES (chacun retire, dans la COPIE, ce qu'un cas teste ; le cas nommé doit rougir) : voir SABOTAGES.

USAGE : python3 tests/EPREUVES_RELEVER_LES_BLOCAGES_ET_RATTACHEMENT_Jeu_26-11-2026.py <racine du dépôt>
        [--saboter | --saboter=S1,S2,…]
CODE : 0 tout vert (et, avec --saboter, chaque sabotage mord) · 1 un cas faux ou un sabotage non vu ·
       2 un contrôle n'a pas pu tourner (vraie ligne introuvable, programme absent, délai dépassé — R-734).
"""
import os
import shutil
import subprocess
import sys
import tempfile

RELEVER = "programmes/RELEVER_LES_BLOCAGES.py"
VERIFIER = "programmes/VERIFIER_LE_RATTACHEMENT.py"
BACKLOG = "BACKLOG_DECISIONS.md"
DELAI = 30  # secondes par lancement ; chaque lancement dure moins d'une seconde

# Chaque sabotage : (programme, texte exact à remplacer, remplaçant, cas qui doit rougir).
SABOTAGES = {
    "S1_mot_jamais_trouve": (RELEVER, 'MOT = re.compile(r"\\bblocages?\\b", re.I)',
                             'MOT = re.compile(r"\\bJAMAIS_ECRIT\\b", re.I)', "R1"),
    "S2_blocage_rend_0": (RELEVER, "        return 3\n", "        return 0\n", "R1"),
    "S3_sans_rapport_passe": (RELEVER, "    if not rapports:\n", "    if False:\n", "R3"),
    "S4_tous_les_rapports": (RELEVER, "[-n:]", "", "R4"),
    "S5_tout_responsable": (RELEVER, 'if len(cases) > 4 and "Pilote" in cases[4]:', "if len(cases) > 4:", "R5"),
    "S6_aucune_decision": (VERIFIER, 'DECISION = re.compile(r"DÉCIDÉ|TRANCHÉ")',
                           'DECISION = re.compile(r"JAMAIS_ECRIT")', "V1"),
    "S7_note_sans_sert_passe": (VERIFIER, "        if not cites:\n", "        if False:\n", "V2"),
    "S8_absente_passe": (VERIFIER, "if a not in idx or not DECISION.search(idx[a])",
                         "if a in idx and not DECISION.search(idx[a])", "V3"),
    "S9_non_decidee_passe": (VERIFIER, "if a not in idx or not DECISION.search(idx[a])",
                             "if a not in idx", "V4"),
    "S10_non_rattache_rend_0": (VERIFIER, "    return 3 if mauvais else 0\n", "    return 0\n", "V2"),
    "S11_sans_paire_accepte": (VERIFIER, "if len(argv) < 3 or", "if len(argv) < 2 or", "V5"),
}


class NonJoue(Exception):
    """Un contrôle qui n'a pas pu tourner (R-734) : jamais confondu avec un vert."""


def vraie_ligne(depot, ident):
    """Rend la ligne du BACKLOG réel qui porte l'action `ident` (R-732), ou lève NonJoue."""
    try:
        with open(os.path.join(depot, BACKLOG), encoding="utf-8") as f:
            for l in f:
                if l.startswith("| %s |" % ident):
                    return l.rstrip("\n")
    except OSError as e:
        raise NonJoue("BACKLOG illisible : %s" % e)
    raise NonJoue("vraie ligne %s introuvable dans %s" % (ident, BACKLOG))


def poser_la_copie(depot, dossier, sabotage):
    """Copie les deux programmes dans `dossier`, applique le sabotage s'il y en a un, rend leurs chemins."""
    chemins = {}
    for prog in (RELEVER, VERIFIER):
        src = os.path.join(depot, prog)
        if not os.path.isfile(src):
            raise NonJoue("programme absent : %s" % prog)
        dst = os.path.join(dossier, os.path.basename(prog))
        shutil.copyfile(src, dst)
        chemins[prog] = dst
    if sabotage:
        prog, avant, apres, _ = SABOTAGES[sabotage]
        t = open(chemins[prog], encoding="utf-8").read()
        if t.count(avant) != 1:
            raise NonJoue("sabotage %s : le texte à remplacer apparaît %d fois dans %s"
                          % (sabotage, t.count(avant), prog))
        with open(chemins[prog], "w", encoding="utf-8") as f:
            f.write(t.replace(avant, apres))
    return chemins


def ecrire(dossier, nom, texte):
    """Écrit un fichier de cas dans le dossier temporaire et rend son chemin."""
    p = os.path.join(dossier, nom)
    with open(p, "w", encoding="utf-8") as f:
        f.write(texte)
    return p


def lancer(programme, arguments, dossier):
    """Lance un programme copié ; rend (code, sortie). Un délai dépassé lève NonJoue."""
    try:
        x = subprocess.run([sys.executable, "-B", programme] + arguments, cwd=dossier,
                           capture_output=True, text=True, timeout=DELAI, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        raise NonJoue("délai de %d s dépassé : %s" % (DELAI, os.path.basename(programme)))
    return x.returncode, x.stdout + x.stderr


def jouer_les_cas(depot, sabotage=None):
    """Joue les dix cas sur une copie ; rend la liste (cas, bon, détail). Lève NonJoue si un cas ne peut tourner."""
    l1055 = vraie_ligne(depot, "A-1055")
    l1014 = vraie_ligne(depot, "A-1014")
    tete = "| Id | Action | Statut | Responsable | Source | Échéance | Liens |\n|---|---|---|---|---|---|---|\n"
    propre = "| A-90001 | rapport de passage sans rien à signaler | CONSTAT·26/11 | Pilote V8 | essai | immédiat | — |"
    bloque = "| A-90002 | rapport de passage : **BLOCAGE** sur l'essai | CONSTAT·26/11 | Pilote V8 | essai | immédiat | — |"
    chat = "| A-90003 | le Chat écrit **BLOCAGE** ici | CONSTAT·26/11 | Chat | essai | immédiat | — |"
    afaire = "| A-90004 | une action proposée | À FAIRE·26/11 | Chat | essai | — | — |"
    resultats = []
    d = tempfile.mkdtemp(prefix="epreuve_blocages_")
    try:
        c = poser_la_copie(depot, d, sabotage)
        r, v = c[RELEVER], c[VERIFIER]
        cas = [
            ("R1", r, [ecrire(d, "b1.md", tete + l1055 + "\n")], 3, "BLOCAGE A-1055 :"),
            ("R2", r, [ecrire(d, "b2.md", tete + propre + "\n")], 0, "AUCUN BLOCAGE"),
            ("R3", r, [ecrire(d, "b3.md", tete + afaire + "\n")], 2, "AUCUN RAPPORT DU PILOTE"),
            ("R4", r, [ecrire(d, "b4.md", tete + bloque + "\n" + propre + "\n"), "1"], 0, "AUCUN BLOCAGE"),
            ("R5", r, [ecrire(d, "b5.md", tete + chat + "\n" + propre + "\n")], 0, "AUCUN BLOCAGE"),
        ]
        bv = ecrire(d, "backlog_v.md", tete + l1014 + "\n" + afaire + "\n")
        cas += [
            ("V1", v, [bv, "n=" + ecrire(d, "n1.md", "SERT : A-1014\nRôle : essai.\n")], 0, "RATTACHÉ n : sert A-1014"),
            ("V2", v, [bv, "n=" + ecrire(d, "n2.md", "Rôle : essai, sans ligne de rattachement.\n")], 3,
             "NON RATTACHÉ n : aucune ligne"),
            ("V3", v, [bv, "n=" + ecrire(d, "n3.md", "SERT : A-99999\n")], 3, "NON RATTACHÉ n : A-99999"),
            ("V4", v, [bv, "n=" + ecrire(d, "n4.md", "SERT : A-90004\n")], 3, "NON RATTACHÉ n : A-90004"),
            ("V5", v, [bv], 2, "USAGE"),
        ]
        for nom, prog, args, code_attendu, mot in cas:
            code, sortie = lancer(prog, args, d)
            bon = code == code_attendu and mot in sortie
            der = (sortie.strip().splitlines() or [""])[-1][:110]
            resultats.append((nom, bon, "code %s (attendu %s) · « %s » %s · %s"
                              % (code, code_attendu, mot, "vu" if mot in sortie else "ABSENT", der)))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return resultats


def main(argv):
    """Joue le passage normal, ou les sabotages demandés ; rend le code de sortie (0, 1 ou 2)."""
    positionnels = [a for a in argv[1:] if not a.startswith("--")]
    depot = os.path.abspath(positionnels[0] if positionnels else ".")
    choix = None
    for a in argv[1:]:
        if a == "--saboter":
            choix = list(SABOTAGES)
        elif a.startswith("--saboter="):
            choix = [s for s in a.split("=", 1)[1].split(",") if s]
            inconnus = [s for s in choix if s not in SABOTAGES]
            if inconnus:
                print("SABOTAGE INCONNU : %s" % ", ".join(inconnus))
                return 2
    faute, non_joue = False, False
    try:
        normaux = jouer_les_cas(depot)
    except NonJoue as e:
        print("NON JOUÉ (R-734) : %s" % e)
        return 2
    for nom, bon, det in normaux:
        print("== %s : %s · %s" % (nom, "vert" if bon else "ROUGE <-- ATTENDU VERT", det))
        faute = faute or not bon
    if choix:
        if faute:
            print("SABOTAGES NON JOUÉS : le passage normal n'est pas vert, un sabotage n'y prouverait rien")
            return 1
        for s in choix:
            cible = SABOTAGES[s][3]
            try:
                res = dict((n, (b, d)) for n, b, d in jouer_les_cas(depot, s))
            except NonJoue as e:
                print("%s NON JOUÉ (R-734) : %s" % (s, e))
                non_joue = True
                continue
            rouges = [n for n, (b, _) in res.items() if not b]
            if cible in rouges:
                print("%s mord : [%s] · %s" % (s, ", ".join(rouges), res[cible][1]))
            else:
                print("%s NE MORD PAS <-- SABOTAGE NON VU : %s reste vert (rouges : %s)"
                      % (s, cible, ", ".join(rouges) or "aucun"))
                faute = True
    if non_joue:
        print("VERDICT : NON JOUÉ — au moins un contrôle n'a pas pu tourner (R-734)")
        return 2
    print("VERDICT :", "tout est conforme" if not faute else "ÉCHEC — voir ci-dessus")
    return 1 if faute else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
