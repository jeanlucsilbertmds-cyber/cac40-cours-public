#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_VERIFICATION_DES_NOTES — Sam 17-10-2026 (Paris). Simulation uniquement.

① RÔLE — Prouver, sur une VRAIE note de la boucle de check, que la vérification d'une note par le garde-fou dit juste :
  une relecture écrite avant le contrôle du rôle est rejetée comme invérifiable par le garde-fou de sa propre version,
  et refusée par le garde-fou d'aujourd'hui, avec le reçu du rôle. Et que la garde du programme de la boucle qui exige
  ce reçu a des dents.
② CONTEXTE D'APPEL — Chaque nuit par la certification (programmes/CERTIFIER_LA_VERSION.py), telle quelle et avec
  « --saboter » ; à la main avant toute livraison qui touche le garde-fou ou la vérification des notes (R-731) :
  python3 tests/EPREUVES_DE_LA_VERIFICATION_DES_NOTES_Sam_17-10-2026.py <racine> [--saboter]
③ ENTRÉE — La racine d'un clone du dépôt, avec son historique : le programme de la boucle est pris dans son
  programmes/, et le témoin est le commit a714f09 de cette racine.
④ CONDITIONS D'ENTRÉE — git sur la machine ; le commit a714f09 (la relecture de Cowork du 16-10-2026 à 18h05) dans la
  racine — la certification clone le dépôt avec tout son historique (`fetch-depth: 0`). S'il manque, les cas sont
  déclarés non joués et la sortie vaut 2 (R-734 : un contrôle qui n'a pas pu tourner ne rend jamais 0).
⑤ SORTIE — Le code de sortie : 0 si B19, B19bis et B19ter donnent la réponse attendue et, avec --saboter, si chaque
  sabotage en fait échouer au moins un ; 1 sinon ; 2 si le témoin manque, si un sabotage ne s'applique plus, ou si la
  copie du témoin n'a pas pu être faite.
  [rend: 1]
⑥ TRAITEMENT — B19 : `verifier_la_note` du programme de la boucle sur a714f09 → code 2, « ne sait pas contrôler le
  rôle » (le garde-fou de cette version ignore « --attendu ») · B19bis : une copie de travail de a714f09, où l'on pose
  le garde-fou, le registre et les programmes d'aujourd'hui ; le garde-fou y refuse la relecture, avec un motif qui
  parle du relecteur et le reçu du rôle · B19ter : dans la même copie, une note sans ses passes est refusée, AVEC le
  reçu. Avec --saboter : la garde du programme qui exige le reçu, retirée dans une copie du programme.
⑦ UNITÉ — Des codes de sortie.
⑧ POURQUOI — Ces trois cas vivaient dans l'épreuve de la boucle (tests/EPREUVES_DE_LA_BOUCLE_DE_CHECK_Ven_16-10-2026.py).
  B19bis copie tout programmes/ et gouvernance/ : la série des sabotages de la boucle dépendait donc de 66 fichiers,
  dont gouvernance/PILOTE.md, réécrit chaque soir par le circuit — une fois la version versée, la nuit aurait déclaré
  la série « à rejouer » chaque nuit (relecture indépendante du 17-10-2026, vers 13h20). Sortis ici, ils tournent
  chaque nuit, et la série de la boucle ne dépend plus que de la boucle et de son épreuve. Données réelles : R-732.
⑨ CE QUI CLOCHE — Le seul sabotage d'ici vise le programme de la boucle ; les gardes du garde-fou sont sabotées par
  tests/SABOTER_LES_CORRECTIONS_DU_GARDE_FOU_Mar_22-09-2026.py.
⑩ EFFET — Crée puis retire une copie de travail dans la racine, et un dossier jetable.
⑪ TERMINAISON — Rend la main ; chaque garde-fou est borné à 600 secondes ; sort par sys.exit.
  [sort: oui]
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
RACINE = os.path.abspath(_args[0]) if _args else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE = os.path.join(RACINE, "programmes", "BOUCLE_DE_CHECK.py")
TEMOIN_REEL = "a714f09"         # relecture de Cowork du 16-10-2026, 18h05, sur travail-filet
SABOTAGES = {
    "S1_recu_du_role_ignore": [("        if not any(x.startswith(RECU_DU_ROLE) for x in lignes):\n", "        if False:\n")],
}


def charger(chemin):
    """Charge le programme de la boucle depuis `chemin` et le rend.

    ① RÔLE — Avoir le programme vrai ou saboté. ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — `chemin`. ④ CONDITIONS
    D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le module. [rend: 1] ⑥ TRAITEMENT — importlib. ⑦ UNITÉ — —
    ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Exécute le module (définitions seulement). ⑪ TERMINAISON — Rend la
    main. [sort: non]
    """
    sp = importlib.util.spec_from_file_location("BOUCLE_%d" % id(chemin), chemin)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def tour(module):
    """Joue B19, B19bis et B19ter avec le programme à `module` ; rend la liste des cas faux.

    ① RÔLE — Un tour d'épreuves. ② CONTEXTE D'APPEL — `main`, une fois tel quel puis une fois par sabotage.
    ③ ENTRÉE — `module` : le chemin du programme de la boucle. ④ CONDITIONS D'ENTRÉE — Le témoin est dans la racine.
    ⑤ SORTIE — UNE valeur : la liste des noms des cas faux ; « … MONTAGE IMPOSSIBLE … » si la copie n'a pas pu être
    faite. [rend: 1] ⑥ TRAITEMENT — Voir la fiche en tête, ⑥. ⑦ UNITÉ — — ⑧ POURQUOI — Voir la fiche en tête.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Une copie de travail dans la racine, retirée. ⑪ TERMINAISON — Rend la main ; chaque
    garde-fou est borné à 600 secondes. [sort: non]
    """
    B = charger(module)
    faux = []
    code, motif = B.verifier_la_note(RACINE, TEMOIN_REEL, B.NOTE_DE_COWORK)
    if code != 2 or "ne sait pas contrôler le rôle" not in motif:      # son garde-fou ignore « --attendu »
        faux.append(f"B19 ({code} {motif[:80]})")
    d = tempfile.mkdtemp(prefix="verification_des_notes_")
    copie = os.path.join(d, "depot")
    verrou = B.prendre_le_verrou_des_copies(RACINE)
    if verrou is None:
        return faux + ["B19bis (MONTAGE IMPOSSIBLE : verrou des copies tenu par un autre programme)"]
    try:
        try:
            ajout = subprocess.run(["git", "-C", RACINE, "worktree", "add", "-q", "--detach", copie, TEMOIN_REEL],
                                   capture_output=True)
        finally:
            verrou.close()
        if ajout.returncode != 0:
            return faux + [f"B19bis (MONTAGE IMPOSSIBLE : git worktree add : code {ajout.returncode})"]
        for dossier in ("programmes", "gouvernance"):
            shutil.copytree(os.path.join(RACINE, dossier), os.path.join(copie, dossier), dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("__pycache__"))
        if os.path.isfile(os.path.join(RACINE, "emp.py")):
            shutil.copy(os.path.join(RACINE, "emp.py"), os.path.join(copie, "emp.py"))
        r = subprocess.run([sys.executable, B.GARDE_FOU, B.NOTE_DE_COWORK, "--verifier", "--attendu=relecture"],
                           cwd=copie, capture_output=True, text=True, timeout=600)
        if (r.returncode != 1 or "RELECTEUR" not in r.stdout
                or not any(x.strip().startswith(B.RECU_DU_ROLE) for x in r.stdout.split("\n"))):
            faux.append(f"B19bis (code {r.returncode})")
        # B19ter — le garde-fou d'aujourd'hui sur une note sans ses passes : un refus, AVEC le reçu (relecture
        # indépendante du 16-10-2026, cinquième tour : le refus précoce sortait avant le reçu).
        open(os.path.join(copie, B.NOTE_DE_COWORK), "w", encoding="utf-8").write(
            "DÉCIDÉ · Rôle : porter la relecture de celui qui n'a pas produit.\n\nsans les passes\n")
        r = subprocess.run([sys.executable, B.GARDE_FOU, B.NOTE_DE_COWORK, "--verifier", "--attendu=relecture"],
                           cwd=copie, capture_output=True, text=True, timeout=600)
        if r.returncode != 1 or not any(x.strip().startswith(B.RECU_DU_ROLE) for x in r.stdout.split("\n")):
            faux.append(f"B19ter (code {r.returncode})")
    finally:
        verrou = B.prendre_le_verrou_des_copies(RACINE)
        try:
            subprocess.run(["git", "-C", RACINE, "worktree", "remove", "--force", "--force", copie], capture_output=True)
            shutil.rmtree(d, ignore_errors=True)
            subprocess.run(["git", "-C", RACINE, "worktree", "prune"], capture_output=True)
        finally:
            if verrou is not None:
                verrou.close()
    return faux


def main():
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Voir la fiche en tête. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — Voir la fiche en tête.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1] ⑥ TRAITEMENT — Voir la fiche en tête ; une
    ligne « Z0 … », puis une ligne par sabotage, « <nom> mord : […] » ou « <nom> NE MORD PAS : [] ». ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir la fiche en tête. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Voir la fiche en tête. ⑪ TERMINAISON — Rend
    la main. [sort: non]
    """
    if subprocess.run(["git", "-C", RACINE, "cat-file", "-e", TEMOIN_REEL + "^{commit}"],
                      capture_output=True).returncode != 0:
        print(f"VERDICT : NON CONFORME — témoin {TEMOIN_REEL} absent de la racine : cas non joués (R-734)")
        return 2
    faux = tour(MODULE)
    print("Z0 programme tel quel : " + ("B19, B19bis et B19ter conformes" if not faux else "FAUX " + ", ".join(faux)))
    impossible = any("MONTAGE IMPOSSIBLE" in f for f in faux)
    code = 1 if faux else 0
    if "--saboter" in sys.argv and not impossible:
        texte = open(MODULE, encoding="utf-8").read()
        for nom, remplacements in SABOTAGES.items():
            t = texte
            for a, b in remplacements:
                if t.count(a) != 1:
                    print(f"{nom} NE S'APPLIQUE PLUS : texte cible trouvé {t.count(a)} fois")
                    return 2
                t = t.replace(a, b)
            d = tempfile.mkdtemp(prefix="verification_des_notes_sab_")
            try:
                p = os.path.join(d, "BOUCLE_DE_CHECK.py")
                open(p, "w", encoding="utf-8").write(t)
                f = tour(p)
            finally:
                shutil.rmtree(d, ignore_errors=True)
            print(f"{nom} {'mord' if f else 'NE MORD PAS'} : {f}", flush=True)
            code |= 0 if f else 1
    if impossible:
        print("VERDICT : NON CONFORME — la copie du témoin n'a pas pu être faite (R-734)")
        return 2
    print("VERDICT : tout est conforme" if code == 0 else "VERDICT : NON CONFORME")
    return code


if __name__ == "__main__":
    sys.exit(main())
