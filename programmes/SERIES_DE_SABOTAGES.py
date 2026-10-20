#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SERIES_DE_SABOTAGES — Ven 16-10-2026 (Paris) — le relevé d'une série de sabotages trop longue pour la nuit. Simulation uniquement.

① RÔLE — Écrire et vérifier le RELEVÉ d'une série de sabotages jouée hors de la certification de nuit : le verdict de la
  série, et l'EMPREINTE (sha256) de chaque fichier du dépôt que l'épreuve a lu pendant la série. Chaque nuit, la
  certification compare ces empreintes aux fichiers du jour : identiques, la série vaut toujours ; une seule différente,
  la série est à rejouer, et la certification rougit.
② CONTEXTE D'APPEL — Importé par programmes/CERTIFIER_LA_VERSION.py (`verifier_la_serie`, chaque nuit) et par
  tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py (`ecrire_le_releve`, à la livraison). Lancé seul :
  python3 programmes/SERIES_DE_SABOTAGES.py <racine> <relevé> — vérifie le relevé et dit pourquoi.
③ ENTRÉE — La racine du dépôt ; le chemin d'un relevé, relatif à la racine.
④ CONDITIONS D'ENTRÉE — Voir chaque fonction.
⑤ SORTIE — Voir chaque fonction. Lancé seul : 0 si le relevé vaut pour les fichiers du jour, 1 si un fichier a changé ou
  si la série n'était pas conforme, 2 si le relevé est absent ou illisible (R-734).
⑥ TRAITEMENT — Voir chaque fonction.
⑦ UNITÉ — Des empreintes sha256 en hexadécimal ; des chemins relatifs à la racine, séparés par « / ».
⑧ POURQUOI — Décision de Jean-Luc du 16-10-2026 à 14h30 (« Uniquement quand il y a un changement. Très bien, avec une
  alarme si on oublie. ») : la série des 167 sabotages de l'épreuve des 20 ans dure environ 6 heures (mesuré le
  16-10-2026 : 27 sabotages en 62 minutes) et ne tient pas dans le passage de nuit (4 heures fixées le 15-10-2026,
  6 heures au plus chez GitHub) ; elle se rejoue quand son code change, comme R-731 l'exige déjà, et la nuit vérifie que
  rien n'a changé depuis. Écrit une fois, lu par les deux (R-708).
⑨ CE QUI CLOCHE — Les empreintes portent sur ce que l'épreuve a LU pendant la série (relevé par le programme qui la
  joue) : un fichier que la série n'a pas lu et dont elle dépendrait quand même (par exemple par un programme lancé
  dans une copie faite ailleurs que dans le dépôt) n'est pas couvert. · Un fichier nouveau que l'épreuve se mettrait à
  lire ne se voit qu'à travers le changement de l'épreuve ou d'un programme, qui l'ont fait lire. · Lancé seul, sans la
  mesure des lectures de la nuit, il ne juge que l'épreuve, ses sabotages, les empreintes du relevé et la présence
  d'au moins un programme : une dépendance que le relevé ne porte pas n'y est pas vue.
⑩ EFFET — Lit des fichiers ; `ecrire_le_releve` écrit le relevé.
⑪ TERMINAISON — Rend la main ; lancé seul, sort par sys.exit avec le code dit en ⑤.
  [sort: oui]
"""
import ast
import hashlib
import os
import re
import sys
import tempfile

ENTETE = "# RELEVÉ D'UNE SÉRIE DE SABOTAGES — fabriqué par un programme, jamais écrit à la main (R-728)"
EMPREINTE = "EMPREINTE "
VERDICT_CONFORME = "VERDICT : tout est conforme"
LIGNE = re.compile(r"^(\S+) (mord|NE MORD PAS|NE S'APPLIQUE PLUS)\b")   # la ligne d'un sabotage, telle que l'épreuve l'écrit
# CE QU'UN ESSAI REFAIT NE PEUT PAS RENDRE MOT POUR MOT : un cas qui n'a pas pu être monté (il n'a rien jugé), un
# chemin de dossier jetable, une adresse en mémoire. Cassure N de Cowork, 17-10-2026 : 18 lignes du relevé de la boucle
# de check portaient des plantages comptés comme des morsures, et chaque nuit en aurait tiré une deux fois sur trois.
NON_REPRODUCTIBLE = re.compile(r"MONTAGE IMPOSSIBLE|/tmp/|" + re.escape(tempfile.gettempdir() + os.sep)
                               + r"| at 0x[0-9a-f]+")   # /tmp/ ET le dossier temporaire du jour (TMPDIR) : tour 11


def noms_des_sabotages(chemin):
    """Rend les noms des sabotages d'une épreuve, dans l'ordre du dictionnaire SABOTAGES.

    ① RÔLE — Savoir ce qu'une série doit contenir, sans lancer l'épreuve.
    ② CONTEXTE D'APPEL — `verifier_la_serie` ; tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py.
    ③ ENTRÉE — `chemin` : l'épreuve.
    ④ CONDITIONS D'ENTRÉE — Elle porte « SABOTAGES = {…} » au premier niveau, à clés écrites en clair ; sinon
      ValueError (clé calculée) ou liste vide.
    ⑤ SORTIE — UNE valeur : la liste des noms.
      [rend: 1]
    ⑥ TRAITEMENT — ast.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Lire la liste là où elle vit (R-708) : un relevé qui omettrait un sabotage doit être refusé
      (relecture du 16-10-2026, cassure 3 : un relevé réduit à une ligne passait).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit l'épreuve.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    for n in ast.parse(open(chemin, encoding="utf-8").read()).body:
        if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "SABOTAGES" for t in n.targets) \
                and isinstance(n.value, ast.Dict):
            return [ast.literal_eval(k) for k in n.value.keys]
    return []


def empreinte(chemin):
    """Rend le sha256 d'un fichier, en hexadécimal.

    ① RÔLE — Dire si un fichier est resté le même, à l'octet.
    ② CONTEXTE D'APPEL — `ecrire_le_releve`, `verifier_la_serie`.
    ③ ENTRÉE — `chemin` : un fichier.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe et se lit.
    ⑤ SORTIE — UNE valeur : 64 caractères hexadécimaux.
      [rend: 1]
    ⑥ TRAITEMENT — hashlib, par blocs d'un mégaoctet.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une date ou une taille ne dit pas qu'un fichier est identique.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit le fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def ecrire_le_releve(racine, releve, epreuve, fichiers_lus, lignes, conforme, entete_libre):
    """Écrit le relevé d'une série : son en-tête, les empreintes des fichiers lus, ses lignes, son verdict.

    ① RÔLE — Garder au dépôt, en un fichier, ce qu'une série a prouvé et sur quels fichiers.
    ② CONTEXTE D'APPEL — tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py, à la fin d'une série complète.
    ③ ENTRÉE — `racine` : le dépôt · `releve` : le chemin du relevé, relatif à la racine · `epreuve` : le chemin de
      l'épreuve, relatif · `fichiers_lus` : les chemins relatifs des fichiers lus pendant la série · `lignes` : les
      lignes de résultat, une par sabotage · `conforme` : vrai si chaque lot a rendu 0 · `entete_libre` : des lignes
      de commentaire (dates, lots, incidents).
    ④ CONDITIONS D'ENTRÉE — Chaque fichier lu existe encore. L'épreuve est comptée parmi eux même si elle n'y est pas.
    ⑤ SORTIE — UNE valeur : le nombre d'empreintes écrites.
      [rend: 1]
    ⑥ TRAITEMENT — trier les chemins ; une ligne « EMPREINTE <sha256> <chemin> » par fichier ; les lignes ; le verdict.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir la fiche en tête, ⑧.
    ⑨ CE QUI CLOCHE — Un chemin qui contient un retour à la ligne casserait le relevé : refusé (ValueError).
    ⑩ EFFET — Écrit le relevé (le dossier est créé s'il manque).
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    chemins = sorted(set(fichiers_lus) | {epreuve})
    if any("\n" in c for c in chemins):
        raise ValueError("un chemin lu contient un retour à la ligne")
    texte = [ENTETE, f"# épreuve : {epreuve}"] + [f"# {l}" for l in entete_libre]
    texte += [f"{EMPREINTE}{empreinte(os.path.join(racine, c))} {c}" for c in chemins]
    texte += list(lignes) + [VERDICT_CONFORME if conforme else "VERDICT : NON CONFORME"]
    chemin = os.path.join(racine, releve)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(texte) + "\n")
    return len(chemins)


def verifier_la_serie(racine, epreuve, releve, lus=None):
    """Dit si le relevé d'une série vaut encore pour les fichiers du jour.

    ① RÔLE — L'alarme décidée par Jean-Luc le 16-10-2026 : une série non rejouée après un changement se voit la nuit même.
    ② CONTEXTE D'APPEL — programmes/CERTIFIER_LA_VERSION.py, à la place du lancement « --saboter » d'une épreuve déclarée
      dans tests/LANCEMENT_DES_EPREUVES.json (« series_hors_de_la_nuit ») ; `main`.
    ③ ENTRÉE — `racine` : le dépôt · `epreuve` : le chemin de l'épreuve, relatif · `releve` : le chemin du relevé, relatif ·
      `lus` : les fichiers (chemins relatifs) que l'épreuve a lus cette nuit, relevés par la certification, ou None
      (vérification à la main, sans ce relevé).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le code (0 le relevé vaut ; 1 un fichier a changé, a disparu, l'épreuve n'est pas
      couverte, ou la série n'était pas conforme ; 2 le relevé est absent ou illisible) et la raison, en clair.
      [rend: 2]
    ⑥ TRAITEMENT — lire l'en-tête, les empreintes et le verdict ; exiger que chaque sabotage du dictionnaire SABOTAGES
      de l'épreuve du jour y figure une fois, « mord », sur une ligne qu'un essai refait peut rendre mot pour mot
      (`NON_REPRODUCTIBLE` : ni montage impossible, ni chemin jetable, ni adresse — cassure N de Cowork,
      17-10-2026), et qu'au moins un programme soit couvert par une empreinte (relecture du 16-10-2026, cassure 3 :
      un relevé réduit à une ligne passait) ; recalculer chaque empreinte ; nommer les fichiers qui diffèrent (cinq
      au plus). La règle « chaque programme que l'épreuve nomme a son empreinte » est retirée le 17-10-2026 : elle
      relevait des noms dans le texte de l'épreuve, sans preuve qu'elle les lise, et rattachait la série de la boucle de
      check au garde-fou par le nom d'un faux fichier d'essai ; la mesure des lectures (`lus`) en tient lieu
      (superviseur, R-759 ; décision de Jean-Luc du 17-10-2026 à 16h10).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir la fiche en tête, ⑧.
    ⑨ CE QUI CLOCHE — Voir la fiche en tête, ⑨.
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    chemin = os.path.join(racine, releve)
    try:
        lignes = open(chemin, encoding="utf-8").read().splitlines()
    except (OSError, UnicodeDecodeError) as e:
        return 2, f"relevé de la série illisible ou absent : {releve} ({type(e).__name__})"
    if not lignes or lignes[0] != ENTETE:
        return 2, f"relevé de la série sans son en-tête : {releve}"
    attendus = {}
    for l in lignes:
        if l.startswith(EMPREINTE):
            morceaux = l[len(EMPREINTE):].split(" ", 1)
            if len(morceaux) != 2 or len(morceaux[0]) != 64:
                return 2, f"ligne d'empreinte illisible dans {releve} : {l[:80]}"
            attendus[morceaux[1]] = morceaux[0]
    if epreuve not in attendus:
        return 1, f"le relevé {releve} ne couvre pas l'épreuve {epreuve}"
    if lignes[-1] != VERDICT_CONFORME:
        return 1, f"la série de {epreuve} n'était pas conforme : « {lignes[-1]} »"
    try:
        noms = noms_des_sabotages(os.path.join(racine, epreuve))
    except (OSError, SyntaxError, ValueError) as e:
        return 2, f"épreuve {epreuve} illisible : {type(e).__name__}"
    vus = {}
    for l in lignes:
        m = LIGNE.match(l)
        if m:
            vus.setdefault(m.group(1), []).append(m.group(2))
    douteuses = [l.split(" ", 1)[0] for l in lignes if LIGNE.match(l) and NON_REPRODUCTIBLE.search(l)]
    if douteuses:
        return 1, (f"relevé {releve} : {len(douteuses)} ligne(s) qu'un essai refait ne peut pas rendre mot pour mot "
                   f"(montage impossible, chemin jetable ou adresse) — {', '.join(douteuses[:5])}")
    mal = [n for n in noms if vus.get(n) != ["mord"]]
    if not noms or mal:
        return 1, (f"relevé {releve} incomplet : " + (f"{len(mal)} sabotage(s) absent(s), doublé(s) ou qui ne mordent pas"
                                                       f" — {', '.join(mal[:5])}" if noms else "l'épreuve n'a pas de SABOTAGES"))
    if not any(c.startswith("programmes/") for c in attendus):
        return 1, f"relevé {releve} : aucun programme couvert par une empreinte"
    if lus is not None:
        # La liste à surveiller ne vient pas du relevé (relecture de Cowork du 16-10-2026, cassure M1).
        if not lus:
            return 2, f"lectures de l'épreuve {epreuve} non relevées cette nuit : la série ne peut pas être jugée"
        hors = sorted(l for l in lus if l not in attendus)
        if hors:
            return 1, (f"SÉRIE À REJOUER : {len(hors)} fichier(s) lu(s) par l'épreuve sans empreinte au relevé {releve} — "
                       + ", ".join(hors[:5]) + (" …" if len(hors) > 5 else ""))
    changes = []
    for c, e in sorted(attendus.items()):
        p = os.path.join(racine, c)
        if not os.path.isfile(p):
            changes.append(c + " (disparu)")
        elif empreinte(p) != e:
            changes.append(c)
    if changes:
        return 1, (f"SÉRIE À REJOUER : {len(changes)} fichier(s) changé(s) depuis la série de {epreuve} — "
                   + ", ".join(changes[:5]) + (" …" if len(changes) > 5 else ""))
    return 0, f"série de {epreuve} jouée hors de la nuit ; {len(attendus)} fichiers identiques au relevé {releve}"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("USAGE : SERIES_DE_SABOTAGES.py <racine> <relevé, relatif à la racine>")
        sys.exit(2)
    try:
        _r = open(os.path.join(sys.argv[1], sys.argv[2]), encoding="utf-8", errors="replace").read().splitlines()
    except OSError as _x:
        print(f"relevé de la série illisible ou absent : {sys.argv[2]} ({type(_x).__name__})")
        sys.exit(2)
    _e = next((l.split(" : ", 1)[1] for l in _r if l.startswith("# épreuve : ")), "")
    _code, _raison = verifier_la_serie(sys.argv[1], _e, sys.argv[2])
    print(_raison)
    sys.exit(_code)
