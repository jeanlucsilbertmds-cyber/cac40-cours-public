#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Épreuves de TENIR_UN_PLANNING.py : chaque cas connaît d'avance la ligne qu'il doit voir.

① RÔLE — Prouver que le veilleur de planning dit ce qu'il doit dire : jalon en retard, jalon proche,
  jalon tenu, rendez-vous dit une seule fois, fichier illisible. ② CONTEXTE D APPEL — à la main :
  python3 -I programmes/EPREUVES_TENIR_UN_PLANNING.py ; et avec --saboter, qui retire la vérification
  de la preuve et doit faire ROUGIR les épreuves. ③ ENTRÉE — l'option --saboter, facultative.
  ④ CONDITIONS D ENTRÉE — TENIR_UN_PLANNING.py dans le même dossier. ⑤ SORTIE — une ligne par épreuve,
  et UNE valeur : le code 0 si toutes passent, 1 sinon. ⑥ TRAITEMENT — fabrique des fichiers de jalons
  dans un dossier temporaire, appelle passage_unique avec une heure fixée. ⑦ UNITÉ — heure de Paris.
  ⑧ POURQUOI — une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas une preuve (R-731).
  ⑨ CE QUI CLOCHE — la boucle main (pause de 10 minutes) n'est pas éprouvée ici. ⑩ EFFET — un dossier
  temporaire, effacé à la fin. ⑪ TERMINAISON — aucun appel réseau, aucune boucle ouverte.
"""
import datetime
import importlib.util
import os
import shutil
import sys
import tempfile
from zoneinfo import ZoneInfo

ICI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("planning", os.path.join(ICI, "TENIR_UN_PLANNING.py"))
T = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T)
if "--saboter" in sys.argv:
    T.os.path.isfile = lambda p: False   # sabotage : aucune preuve n'est vue (la preuve passe par isfile depuis le 25-10-2026)


def epreuves():
    """Joue les cas et rend le nombre d'échecs.

    ① rôle : jouer chaque cas
    ② contexte : appelée une fois par le programme
    ③ entrée : —
    ④ conditions : dossier temporaire inscriptible
    ⑤ sortie : UNE valeur, le nombre d'échecs
      [rend: 1]
    ⑥ traitement : un fichier de jalons par cas, un passage, une comparaison
    ⑦ unité : —
    ⑧ pourquoi : un cas par repère du programme
    ⑨ ce qui cloche : —
    ⑩ effet : affiche
    ⑪ terminaison : revient toujours.
      [sort: non]
    """
    P = ZoneInfo("Europe/Paris")
    t = datetime.datetime(2026, 10, 26, 12, 0, tzinfo=P)
    d = tempfile.mkdtemp()
    preuve = os.path.join(d, "preuve.md")
    open(preuve, "w").write("x")
    absent = os.path.join(d, "absent.md")
    vide = os.path.join(d, "vide.md")
    open(vide, "w").close()

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
        ⑧ pourquoi : chaque cas a son propre fichier, pour que ses marques ne se mêlent pas à celles d'un autre
        ⑨ ce qui cloche : —
        ⑩ effet : écrit un fichier dans le dossier temporaire
        ⑪ terminaison : revient toujours
          [sort: non]
        """
        f = os.path.join(d, nom)
        open(f, "w").write("jalon;echeance;preuve;libelle\n" + "\n".join(lignes) + "\n")
        return f

    cas = [
        ("retard sans preuve", fichier("a.csv", [f"A;2026-10-26 11:00;{absent};x"]), "ERREUR JALON DÉPASSÉ", False),
        ("retard avec preuve = tenu", fichier("b.csv", [f"B;2026-10-26 11:00;{preuve};x"]), "FINI", True),
        ("échéance dans 20 min", fichier("c.csv", [f"C;2026-10-26 12:20;{absent};x"]), "ALERTE", False),
        ("échéance lointaine", fichier("e.csv", [f"E;2026-10-27 12:00;{absent};x", f"F;2026-10-26 11:00;{preuve};y"]), "ETAPE 12h00 tenus 1/2", False),
        ("rendez-vous atteint", fichier("r.csv", ["R;2026-10-26 11:55;RDV;x", f"G;2026-10-27 12:00;{absent};y"]), "RDV", False),
        ("échéance illisible", fichier("i.csv", [f"I;26/10/2026;{absent};x"]), "ARRET", None),
        ("fichier réduit à l'en-tête : ARRET, jamais FINI", fichier("v.csv", []), "ARRET", None),
        # cas réel du PLAN ORANGE : J10 (bilan) prouvé avant le rendez-vous P4 de la même heure -> pas FINI tant que P4 n'est pas annoncé
        ("jalon tenu avant le dernier rendez-vous : pas FINI", fichier("p4.csv", [f"J10;2026-10-27 18:25;{preuve};bilan", "P4;2026-10-27 18:25;RDV;plage"]), "ETAPE", False),
        ("preuve vide : pas tenue", fichier("z.csv", [f"Z;2026-10-26 11:00;{vide};x"]), "ERREUR JALON DÉPASSÉ", False),
        ("preuve au chemin relatif : ARRET", fichier("rel.csv", ["Q;2026-10-27 11:00;preuve.md;x"]), "ARRET", None),
    ]
    echecs = 0
    for nom, f, attendu, fini_attendu in cas:
        if fini_attendu is True:
            premier, f1 = T.passage_unique(f, t)   # le premier passage, qui crée la liste des jalons vus, ne dit jamais FINI
            if f1 is not False:
                echecs += 1; print("ÉCHEC " + nom + " : FINI dès le premier passage → " + " | ".join(premier), flush=True)
        lignes, fini = T.passage_unique(f, t)
        ok = any(l.startswith(attendu) for l in lignes) and fini == fini_attendu
        echecs += not ok
        print(("OK  " if ok else "ÉCHEC ") + nom + " → " + " | ".join(lignes), flush=True)
    # un jalon qui disparaît d'un passage à l'autre : ERREUR, jamais FINI
    f = fichier("dis.csv", [f"A;2026-10-26 11:00;{preuve};x", f"B;2026-10-26 11:00;{absent};y"])
    T.passage_unique(f, t)
    open(f, "w").write("jalon;echeance;preuve;libelle\n" + f"A;2026-10-26 11:00;{preuve};x\n")
    lignes, fini = T.passage_unique(f, t)
    ok = any(l.startswith("ERREUR JALON DISPARU") for l in lignes) and fini is False
    echecs += not ok
    print(("OK  " if ok else "ÉCHEC ") + "jalon disparu → " + " | ".join(lignes), flush=True)
    # un essai sans écriture ne pose aucune marque de rendez-vous
    f = fichier("ess.csv", ["R9;2026-10-26 11:00;RDV;x", f"G;2026-10-27 12:00;{absent};y"])
    T.passage_unique(f, t, ecrire=False)
    ok = not os.path.exists(f + ".R9.dit")
    echecs += not ok
    print(("OK  " if ok else "ÉCHEC ") + "essai sans écriture : aucune marque", flush=True)
    # le rendez-vous ne doit pas être redit au passage suivant
    lignes, _ = T.passage_unique(os.path.join(d, "r.csv"), t)
    ok = not any(l.startswith("RDV") for l in lignes)
    echecs += not ok
    print(("OK  " if ok else "ÉCHEC ") + "rendez-vous non redit → " + " | ".join(lignes), flush=True)
    shutil.rmtree(d)
    return echecs


if __name__ == "__main__":
    n = epreuves()
    print(f"{'TOUT PASSE' if n == 0 else str(n) + ' ÉCHEC(S)'}", flush=True)
    sys.exit(0 if n == 0 else 1)
