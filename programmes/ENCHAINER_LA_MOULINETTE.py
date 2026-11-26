#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ENCHAINER_LA_MOULINETTE.py — Jeu 19-11-2026 (Paris). EN ESSAI · outil. Simulation uniquement : aucun ordre réel.

LE SENS EN TÊTE. La moulinette (A-541) : ⓪ PREPARER propose des réglages, Jean-Luc les valide · ① DECLINER les croise
en versions · ② JOUER rejoue chaque version (par tranches, puis assemblées, le tout DANS JOUER_LES_VERSIONS) ·
③ TRIER écarte les versions sous le seuil · ④ le juge examine UNE version retenue. Ce programme ne fait QU'APPELER ces
programmes dans l'ordre et écrire, après chaque étape réussie, son témoin au journal de la chaîne. La garde vit dans
programmes/VERIFIER_LA_CHAINE.py, que le JUGE appelle lui-même (A-919 ; superviseur R-759 du 19-11-2026).

USAGE
    python3 -B programmes/ENCHAINER_LA_MOULINETTE.py <racine> <STRATÉGIE> <ESSAI> <étape> [arguments]
    étapes dans l'ordre : preparer · decliner · jouer <k> <N> (k = 0 … N-1) · assembler · trier · juger <id_version>
    à tout moment avant juger : declarer "<qui, quand, mots de la décision>" — la déclaration explicite qui permet de
    juger une famille déjà jouée sur 2000-2023 (A-777, C12 ; VERIFIER_LA_CHAINE.garde_de_famille)

① RÔLE — Lancer les étapes de la moulinette dans l'ordre, sans en sauter, et en garder la trace.
② CONTEXTE D'APPEL — À la main, une étape par appel (chacune sous 10 minutes). Aucune tâche automatique.
③ ENTRÉE — `<racine>` : une COPIE du dépôt sans .git ; `<STRATÉGIE>` `<ESSAI>` : exemple réel C5E10-OBS-V1 E01 ;
  l'étape et ses arguments. Lus dans la racine : donnees/combinatoires/VARIABLES_DE_DECLINAISON_<STRATÉGIE>_<ESSAI>.csv
  (les réglages validés), VOISINAGE.csv, TEMOIN_RESULTATS_<STRATÉGIE>_<ESSAI>.csv s'il existe, le registre.
④ CONDITIONS D'ENTRÉE — La racine ne porte pas .git (l'étape juger ajoute une fiche au registre ; jamais dans un dépôt,
  A-861). Avant chaque étape, `VERIFIER_LA_CHAINE.motifs` exige les témoins intacts des étapes précédentes. La
  validation des réglages est exigée par DECLINER (colonne `valide_par`) puis par la porte du juge — c'est une
  mention écrite, rien de plus. La version jugée est donnée par l'appelant : la règle du choix n'est pas décidée
  (A-775) ; une version absente du tri est refusée ; une version d'une famille déjà jouée sur 2000-2023 est refusée
  sans déclaration (`V.motifs`, garde de famille). « jouer k N » est refusé si une tranche déjà témoignée n'est pas
  celle du découpage en N (`V.decoupage_mele`, L-3 du RELU Cowork du 25-11-2026).
⑤ SORTIE — UNE valeur, le code : 0 l'étape a tenu · 1 refus ou programme de la chaîne en échec · 2 un contrôle n'a
  pas pu tourner (R-734). Fichiers sous <racine>/CHAINE_<STRATÉGIE>_<ESSAI>/ (journal, e0 … e4, sorties .txt).
⑥ TRAITEMENT — garde · lancement du programme de l'étape · témoin si et seulement si le programme a rendu 0.
⑦ UNITÉ — secondes (délais).
⑧ POURQUOI — A-919 : le 19-11-2026, le juge a été lancé sans ① ② ③. Rien n'est recalculé ici (R-708).
⑨ CE QUI CLOCHE — ① Trois gestes de fichier restent ici : recopier le tableau validé dans le dossier de la chaîne
  (pour le figer par son empreinte), poser le témoin de résultats à côté de la combinatoire (JOUER le cherche là),
  ajouter au registre de la copie la fiche de la version jugée, MARQUÉE (CONTRATS.MARQUE_DE_MOULINETTE, A-921 ; une
  fois : rien si la dernière ligne de l'identifiant est déjà celle-là). ② La période jouée est celle de la fiche : aucun regard consommé.
⑩ EFFET — Écrit sous le dossier de la chaîne ; juger ajoute au plus une ligne au registre de la racine.
⑪ TERMINAISON — Chaque programme est borné (580 s JOUER et le juge, 300 s les autres). [sort: oui — code]
"""
import csv
import io
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import VERIFIER_LA_CHAINE as V  # noqa: E402  la garde et le journal vivent là (R-708)

import CONTRATS_DES_FICHIERS as C  # noqa: E402  le registre est nommé au contrat, une fois (R-708)

REG = C.REGISTRE_DES_STRATEGIES
FAITE = {"preparer": "0-proposition", "decliner": "1-decliner", "assembler": "2-assembler", "trier": "3-trier"}
EXIGEES = {"preparer": 0, "decliner": 2, "jouer": 3, "assembler": 3, "trier": 4, "juger": 5, "declarer": 0}
NB_ARGS = {"jouer": 2, "juger": 1, "declarer": 1}


def lancer(racine, ch, nom, *args, delai=300):
    """Lance un programme de la racine ; rend son code de sortie.

    ① RÔLE — Lancer un programme de la chaîne par son chemin réel dans la racine, et garder sa sortie.
    ② CONTEXTE D'APPEL — `faire`, une fois par étape (preparer, decliner, jouer, assembler, trier, juger).
    ③ ENTRÉE — `racine` : la copie ; `ch` : le dossier de la chaîne ; `nom` : la sortie, relative à `ch`, sans .txt ;
      `args` : le programme, relatif à la racine, et ses arguments ; `delai` : en secondes (300, ou 580 pour JOUER et
      le juge). Exemple réel : `lancer(racine, ch, "e3/sortie", "programmes/TRIER_LES_VARIANTES.py", …)`.
    ④ CONDITIONS D'ENTRÉE — le sous-dossier de `nom` existe sous `ch` (créé par `faire` avant l'appel).
    ⑤ SORTIE — UNE valeur : le code de sortie du programme lancé.
    [rend: 1]
    ⑥ TRAITEMENT — ① environnement nettoyé des variables GITHUB_* et DEPOT_*, puis DEPOT_CAC40 pointé sur la racine et
      GITHUB_OUTPUT dans le dossier de la chaîne · ② `python3 -B`, dans la racine, sous le délai · ③ sortie et erreurs
      écrites dans `<ch>/<nom>.txt` · ④ les six dernières lignes affichées.
    ⑦ UNITÉ — secondes (le délai).
    ⑧ POURQUOI — un programme lancé depuis la copie lit la copie, jamais le dépôt (relecteur du 19-11-2026, I4 : sans
      ce nettoyage, DEPOT_CAC40 hérité aurait fait lire le vrai dépôt).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — le programme lancé écrit ce qu'il écrit ; ici, `<ch>/<nom>.txt`.
    ⑪ TERMINAISON — rend la main ; lève V.Impossible au-delà du délai (le processus est alors tué par `subprocess.run`) ;
      aucun appel ne peut ne pas revenir.
    [sort: non]
    """
    env = {k: v for k, v in os.environ.items() if not k.startswith(("GITHUB_", "DEPOT_"))}
    env.update(DEPOT_CAC40=racine, GITHUB_OUTPUT=os.path.join(ch, "github_output"))
    try:
        p = subprocess.run([sys.executable, "-B"] + list(args), cwd=racine, capture_output=True, text=True,
                           timeout=delai, env=env)
    except subprocess.TimeoutExpired:
        raise V.Impossible("%s : délai de %d s dépassé" % (args[0], delai))
    with open(os.path.join(ch, nom + ".txt"), "w", encoding="utf-8") as fh:
        fh.write(p.stdout + p.stderr)
    print("%s → code %d\n%s" % (args[0], p.returncode,
                                "\n".join("  " + l for l in (p.stdout + p.stderr).splitlines()[-6:])))
    return p.returncode


def ajouter_la_fiche(racine, sid, essai, v):
    """Ajoute au registre de la copie la fiche de la version `v` (ligne du tri), une fois, MARQUÉE.

    ① RÔLE — Écrire la fiche que le juge lira pour la version retenue.
    ② CONTEXTE D'APPEL — `faire`, à l'étape juger, juste avant de lancer le juge.
    ③ ENTRÉE — `racine` : la copie ; `sid`, `essai` : exemple réel C5E10-OBS-V1, E01 ; `v` : une ligne du fichier trié
      ③ (id_version, tp, sl, horizon, univers).
    ④ CONDITIONS D'ENTRÉE — la racine ne porte pas .git (vérifié par `main`) ; le registre porte une ligne de `sid`.
    ⑤ SORTIE — aucune.
    [rend: rien]
    ⑥ TRAITEMENT — ① la dernière ligne de la stratégie (décision n°83 : la dernière ligne d'un identifiant fait foi) ·
      ② huit cases changées : id, tp, sl, horizon, univers, etat_vie, statut, et LA MARQUE DE MOULINETTE
      (CONTRATS.COLONNE_DE_LA_MARQUE_DE_MOULINETTE ← « MARQUE_DE_MOULINETTE <STRATÉGIE> <ESSAI> ») · ③ rien si la
      dernière ligne de la version est déjà celle-là (M2) · ④ sinon, une ligne ajoutée, fin de ligne du fichier gardée.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — A-921 (décision de Jean-Luc du 19-11-2026 à 12h31) : la porte du juge reconnaît une version à cette
      marque, écrite ici et nulle part à la main.
    ⑨ CE QUI CLOCHE — voir ⑨ ① de l'en-tête : un geste de fichier reste ici, hors des programmes de la moulinette.
    ⑩ EFFET — écrit (ajoute une ligne) au registre de la copie.
    ⑪ TERMINAISON — rend la main ; lève IndexError si le registre n'a aucune ligne de `sid` (`main` la convertit en
      code 2).
    [sort: non]
    """
    reg = os.path.join(racine, REG)
    with open(reg, "rb") as fh:
        octets = fh.read()
    lignes = list(csv.reader(io.StringIO(octets.decode("utf-8-sig"), newline="")))
    ent = lignes[0]
    neuve = list([l for l in lignes[1:] if l and l[ent.index("id")] == sid][-1])
    for col, val in (("id", v["id_version"]), ("tp", v["tp"]), ("sl", v["sl"]), ("horizon", v["horizon"]),
                     ("univers", v["univers"]), ("etat_vie", "LABO"),
                     ("statut", "ESSAI (A-919) : version retenue par la moulinette, copie jetable"),
                     (C.COLONNE_DE_LA_MARQUE_DE_MOULINETTE, "%s %s %s" % (C.MARQUE_DE_MOULINETTE, sid, essai))):
        neuve[ent.index(col)] = val
    deja = [l for l in lignes[1:] if l and l[ent.index("id")] == v["id_version"]]
    if deja and deja[-1] == neuve:
        return
    with open(reg, "a", encoding="utf-8", newline="") as fh:
        csv.writer(fh, lineterminator="\r\n" if octets.endswith(b"\r\n") else "\n").writerow(neuve)


def faire(racine, sid, essai, etape, args):
    """Fait une étape de la chaîne ; rend son code.

    ① RÔLE — L'aiguillage : lancer le programme de l'étape, puis écrire son témoin s'il a rendu 0.
    ② CONTEXTE D'APPEL — `main`, une fois, après la garde.
    ③ ENTRÉE — `racine`, `sid`, `essai` ; `etape` : preparer, decliner, jouer, assembler, trier, juger ou declarer ;
      `args` : (k, N) pour jouer, (id_version,) pour juger, (texte,) pour declarer, vide sinon.
    ④ CONDITIONS D'ENTRÉE — la garde de `main` (`V.motifs`) n'a rien rendu.
    ⑤ SORTIE — UNE valeur : 0 l'étape a tenu, 1 le programme de l'étape a échoué ou la tranche est déjà jouée.
      [rend: 1]
    ⑥ TRAITEMENT — selon l'étape : preparer (e0, et le tableau validé recopié dans valide/) · decliner (e1, et le
      témoin de résultats recopié s'il existe) · jouer (une tranche, e2) · assembler (e2) · trier (e3) · juger (la
      fiche ajoutée au registre, MARQUÉE, puis le juge sur cette fiche, e4) · declarer (`V.declarer_la_famille`, une
      fois : une seconde déclaration ne change rien et le dit) ; le témoin au journal après un code 0.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — A-919 : une étape n'existe pour la suite que si son témoin est écrit, et il ne l'est qu'après réussite.
    ⑨ CE QUI CLOCHE — ① la version jugée est donnée par l'appelant (A-775 non décidée) · ② l'étape juger se relance
      tant que son témoin n'existe pas, et peut se relancer après : deux lignes « 4-juger-… » au journal, la dernière
      fait foi (M1 du relecteur du 19-11-2026, consigné).
    ⑩ EFFET — écrit sous le dossier de la chaîne ; juger ajoute au plus une ligne au registre de la copie.
    ⑪ TERMINAISON — rend la main, ou lève V.Impossible (délai, témoin impossible) ; chaque programme lancé est borné
      par `lancer`.
    [sort: non]
    """
    ch = V.dossier(racine, sid, essai)
    t = V.temoins(ch)
    variables, comb = "VARIABLES_DE_DECLINAISON_%s_%s.csv" % (sid, essai), "COMBINATOIRE_%s_%s.csv" % (sid, essai)
    if etape == "declarer":
        print("DÉCLARATION DE FAMILLE %s : %s" % ("écrite" if V.declarer_la_famille(ch, args[0]) else
                                                 "déjà au journal, inchangée (la première fait foi)",
                                                 open(os.path.join(ch, V.FICHIER_DE_FAMILLE), encoding="utf-8").read().strip()))
    elif etape == "preparer":
        for d in ("e0", "valide"):
            os.makedirs(os.path.join(ch, d))
        if lancer(racine, ch, "e0/sortie", "programmes/PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES.py", REG,
                  sid, "donnees/combinatoires/VOISINAGE.csv", essai, os.path.join(ch, "e0")):
            return 1
        shutil.copyfile(os.path.join(racine, "donnees/combinatoires", variables), os.path.join(ch, "valide", variables))
        V.temoigner(ch, "0-variables-validees", "valide/" + variables)
        V.temoigner(ch, "0-proposition", "e0/" + variables)
    elif etape == "decliner":
        os.makedirs(os.path.join(ch, "e1"))
        if lancer(racine, ch, "e1/sortie", "programmes/DECLINER_LES_STRATEGIES.py", REG,
                  os.path.join(ch, t["0-variables-validees"][0]), os.path.join(ch, "e1")):
            return 1
        tem = "TEMOIN_RESULTATS_%s_%s.csv" % (sid, essai)
        if os.path.exists(os.path.join(racine, "donnees/combinatoires", tem)):
            shutil.copyfile(os.path.join(racine, "donnees/combinatoires", tem), os.path.join(ch, "e1", tem))
            V.temoigner(ch, "1-temoin-de-resultats", "e1/" + tem)
        V.temoigner(ch, "1-decliner", "e1/" + comb)
    elif etape == "jouer":
        k, n = args
        if "2-tranche-%s" % k in t:
            print("REFUS : la tranche %s est déjà jouée" % k)
            return 1
        os.makedirs(os.path.join(ch, "e2"), exist_ok=True)
        if lancer(racine, ch, "e2/sortie_%s" % k, "programmes/JOUER_LES_VERSIONS.py", ".",
                  os.path.join(ch, t["1-decliner"][0]), os.path.join(ch, "e2", "tranche_%s.csv" % k),
                  "--tranche=%s/%s" % (k, n), delai=580):
            return 1
        V.temoigner(ch, "2-tranche-%s" % k, "e2/tranche_%s.csv" % k)
    elif etape == "assembler":
        noms = sorted((e for e in t if e.startswith("2-tranche-")), key=lambda e: int(e[len("2-tranche-"):]))
        if lancer(racine, ch, "e2/sortie_assembler", "programmes/JOUER_LES_VERSIONS.py", "--assembler",
                  os.path.join(ch, t["1-decliner"][0]), os.path.join(ch, "e2", "RESULTATS_%s_%s.csv" % (sid, essai)),
                  *[os.path.join(ch, t[e][0]) for e in noms]):
            return 1
        V.temoigner(ch, "2-assembler", "e2/RESULTATS_%s_%s.csv" % (sid, essai))
    elif etape == "trier":
        os.makedirs(os.path.join(ch, "e3"))
        if lancer(racine, ch, "e3/sortie", "programmes/TRIER_LES_VARIANTES.py", ".",
                  os.path.join(ch, "e3", "TRI_%s_%s.csv" % (sid, essai)), os.path.join(ch, t["2-assembler"][0])):
            return 1
        V.temoigner(ch, "3-trier", "e3/TRI_%s_%s.csv" % (sid, essai))
    else:   # juger : la garde a déjà dit que la version est parmi les retenues ; le juge le revérifie lui-même
        ident = args[0]
        retenue = [r for r in V.lire(os.path.join(ch, t["3-trier"][0])) if V.norme(r["id_version"]) == V.norme(ident)]
        ajouter_la_fiche(racine, sid, essai, retenue[0])
        os.makedirs(os.path.join(ch, "e4"), exist_ok=True)
        if lancer(racine, ch, "e4/juge_%s" % ident, "programmes/JUGE_DES_STRATEGIES.py", racine, ident, delai=580):
            print("REFUS ④ : le juge a échoué — aucun témoin ④ n'est écrit")
            return 1
        V.temoigner(ch, "4-juger-%s" % ident, "e4/juge_%s.txt" % ident)
    return 0


def main(argv):
    """Rend le code de sortie de la ligne de commande.

    ① RÔLE — Lire les arguments, refuser un dépôt, garder, aiguiller.
    ② CONTEXTE D'APPEL — `__main__`.
    ③ ENTRÉE — `argv` : exemple réel `[…, "/dev/shm/x/depot", "C5E10-OBS-V1", "E01", "jouer", "0", "5"]`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 0 l'étape a tenu · 1 refus · 2 usage faux, racine avec .git, ou contrôle impossible
      (R-734).
    [rend: 1]
    ⑥ TRAITEMENT — ① arguments (nombre, étape connue ; pour « jouer » : k et N entiers ASCII écrits sans zéro de tête,
      0 ≤ k < N — L-10 et L-7 du RELU Cowork du 25-11-2026) · ② .git refusé (A-861) · ③ garde :
      `V.motifs` exige les témoins des étapes précédentes (et, à juger, la garde de famille), une étape déjà faite est
      refusée, et « jouer k N » est refusé si les tranches déjà jouées sont d'un autre découpage (`V.decoupage_mele`)
      · ④ `faire` · ⑤ les erreurs de fichier et de contrôle converties en code 2.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — A-919 : la chaîne ⓪ ① ② ③ ④ ne se saute pas. L-10 du RELU Cowork du 25-11-2026 (14h20) : `k` était
      le TEXTE de l'argument ; « jouer 0 3 » puis « jouer 00 3 » écrivaient deux témoins (2-tranche-0, 2-tranche-00),
      la tranche 0 jouée deux fois, puis l'assemblage refusait et la chaîne était perdue (cas B2). Une seule graphie
      par nombre ferme ce chemin. L-7 du même RELU : « jouer 5 3 » passait le contrôle et ne tombait qu'au vrai JOUER
      (`JOUER_LES_VERSIONS.lire_la_tranche` exige 0 ≤ k < N) ; refusé ici, avant tout écrit.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — voir l'en-tête du fichier ; affiche.
    ⑪ TERMINAISON — rend la main ; c'est `__main__` qui passe le code à `sys.exit`.
    [sort: non]
    """
    if len(argv) < 5 or argv[4] not in EXIGEES or len(argv) != 5 + NB_ARGS.get(argv[4], 0) or \
            (argv[4] == "jouer" and not (all(a.isascii() and a.isdigit() and a == str(int(a)) for a in argv[5:]) and
                                         0 <= int(argv[5]) < int(argv[6]))):
        print(__doc__.split("① RÔLE")[0])
        return 2
    racine, sid, essai, etape, args = os.path.abspath(argv[1]), argv[2], argv[3], argv[4], argv[5:]
    if os.path.lexists(os.path.join(racine, ".git")):
        print("ARRÊT : %s porte .git — la moulinette ne tourne que sur une copie (A-861)" % racine)
        return 2
    try:
        os.makedirs(V.dossier(racine, sid, essai), exist_ok=True)
        m = V.motifs(racine, sid, essai, EXIGEES[etape], args[0] if etape == "juger" else None)
        if FAITE.get(etape) in V.temoins(V.dossier(racine, sid, essai)):
            m.append("étape %s déjà faite : un essai ne se refait pas" % etape)
        if etape == "jouer" and not m:
            m += V.decoupage_mele(V.dossier(racine, sid, essai), int(args[1]))
        if m:
            print("REFUS de l'étape %s — la chaîne ⓪ ① ② ③ ④ ne se saute pas (A-919) :\n  %s" % (etape, "\n  ".join(m)))
            return 1
        return faire(racine, sid, essai, etape, args)
    except (V.Impossible, OSError, ValueError, KeyError, IndexError) as e:
        print("CONTRÔLE IMPOSSIBLE (R-734) : %s: %s" % (type(e).__name__, e))
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
