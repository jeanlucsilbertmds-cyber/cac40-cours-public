#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrier_les_epreuves_longues — Dim 15-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Étape GHUB ②, point 5 : « le rapatriement rend, pour chaque épreuve, le code de sortie et la sortie
capturée, dans le dépôt privé ». Le circuit des épreuves longues (.github/workflows/epreuves_longues.yml du dépôt
public) pousse chaque épreuve sur SA branche du dépôt PRIVÉ, epreuves-longues/<passage>/<code>. Ce programme, lancé
par le Chat dans son clone du privé, lit ces branches et range tout sous tests/resultats/epreuves_longues/<passage>/,
avec un BILAN.txt d'une ligne par épreuve.

① RÔLE — Rapatrier les sorties d'un passage du circuit des épreuves longues dans le dépôt privé, et dire, épreuve par
  épreuve, son code de sortie.
② CONTEXTE D'APPEL — À la main par le Chat, après la fin d'un passage (MODE_EMPLOI_DEPOT.md §13.2, geste 8bis) :
  python3 -B tests/outils/rapatrier_les_epreuves_longues.py <racine du clone privé> <numéro du passage>
  [--depuis=<dépôt>] ; aussi l'épreuve tests/EPREUVES_DU_CIRCUIT_DES_EPREUVES_LONGUES_Dim_15-11-2026.py.
③ ENTRÉE — La racine d'un clone git du dépôt privé ; le numéro du passage (chiffres) ; `--depuis` : le dépôt d'où lire
  les branches (par défaut « origin » ; l'épreuve donne un dépôt nu local).
④ CONDITIONS D'ENTRÉE — git est installé ; la racine est un dépôt git ; le dépôt lu porte les branches du passage.
⑤ SORTIE — Le code de sortie : 0 si les épreuves rapatriées sont EXACTEMENT les épreuves demandées et que chacune a
  un RESULTAT.json lisible au code 0 ; 1 si au moins une a un code non nul (le BILAN dit laquelle) ; 2 si rien n'a pu
  être rapatrié, si la liste demandée est inconnue ou n'est pas la même sur toutes les branches, si une épreuve
  demandée n'a pas de branche (« ABSENTE »), si une branche n'est pas demandée, ou si une branche n'a pas de
  RESULTAT.json lisible (rien de sûr pour elle). Écrit tests/resultats/epreuves_longues/<passage>/<code>/ (SORTIE.txt,
  RESULTAT.json, le journal du job) et tests/resultats/epreuves_longues/<passage>/BILAN.txt.
  [rend: 1]
⑥ TRAITEMENT — ① `git fetch` des références refs/heads/epreuves-longues/<passage>/* vers
  refs/epreuves_lues/<passage>/* de la racine ; ② pour chaque référence : son code (le dernier morceau, vérifié par
  motif), `git archive` de la branche, extrait dans un dossier neuf ; DEMANDE.json lu (la matrice ENTIÈRE du passage,
  écrite par le pas « Jouer l epreuve » du circuit avant de lancer le joueur) ; le dossier
  rapports/epreuves_longues/<passage>/<code> et le journal recopiés dans un dossier VOISIN de la cible
  (« <code>.neuf ») ; ③ RESULTAT.json lu DANS CE VOISIN : code de sortie, durée, commande ; lisible, l'ancienne cible
  est écartée, le voisin prend sa place ; illisible, le voisin est effacé et l'ancienne cible GARDÉE ; ④ la liste
  demandée (la même sur toutes les branches) confrontée aux codes des branches : une demandée sans branche est
  « ABSENTE », une branche non demandée est signalée ; ⑤ BILAN.txt écrit (« demandées N · rapatriées M »), puis
  affiché.
⑦ UNITÉ — Des secondes (la durée lue au résultat).
⑧ POURQUOI — Un résultat qui reste sur une branche n'est relu par personne ; rangé sous tests/resultats/ de la version
  éprouvée, il voyage avec elle et le relecteur le lit (R-731). Le code de sortie est LU dans le RESULTAT.json écrit
  par le joueur (tests/outils/jouer_une_epreuve_longue.py), pas déduit de la couleur du job.
⑧bis R-D2 et R-D5 du relecteur du 15-11-2026 (jugés DE FOND par le superviseur R-759 du même jour) : un passage où
  34 épreuves sur 35 n'avaient rien déposé était rapatrié au code 0 (le rapatrieur ne connaissait pas la liste
  demandée ; R-754 : ce qu'un programme peut faire, un programme le fait) ; et la cible était effacée AVANT la copie
  (un résultat déjà rangé détruit par une branche sans dossier). La liste demandée voyage avec les résultats, par le
  même canal : chaque branche porte la matrice entière ; il suffit d'UNE branche pour connaître toutes les épreuves
  demandées, et aucune branche donne déjà le code 2. Écart déclaré à la proposition (une branche « _matrice » poussée
  par « preparer ») : la matrice dans chaque branche n'ajoute aucun pas à jeton.
⑨ CE QUI CLOCHE — Les branches ne sont pas supprimées (la session du Chat ne peut supprimer aucune branche : choix
  n°347 du circuit des séries) ; elles restent au privé. Une branche sans DEMANDE.json lisible (un passage d'avant le
  15-11-2026) rend le code 2 : la liste demandée n'est pas sûre. Une relance (« re-run ») garde le même numéro de
  passage et sa poussée est refusée (jamais forcée) : la page de GitHub peut montrer un vert que le BILAN ne montre
  pas — le BILAN fait foi.
⑩ EFFET — Écrit des références refs/epreuves_lues/… dans la racine, et des fichiers sous tests/resultats/.
⑪ TERMINAISON — Rend la main ; chaque commande git est bornée à 600 secondes.
  [sort: oui]
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

SORTIES = "rapports/epreuves_longues"    # où le circuit dépose (la sortie du joueur, --sortie)
DEMANDE = "DEMANDE.json"                 # la matrice entière du passage, écrite par le pas « Jouer l epreuve » (R-D2)
RANGEMENT = os.path.join("tests", "resultats", "epreuves_longues")
FABRICANT = os.path.join("programmes", "FABRIQUER_LE_CIRCUIT_PUBLIC.py")


def fabricant(racine):
    """Charge le fabricant du circuit public de la racine, par son chemin.

    ① RÔLE — Lire le préfixe des branches (EPREUVES_BRANCHES) et la forme d'un code (CODE_DE_SERIE) là où ils sont
    écrits, une fois (R-708). ② CONTEXTE D'APPEL — `rapatrier`. ③ ENTRÉE — la racine. ④ CONDITIONS D'ENTRÉE — Le
    fabricant est dans la racine. ⑤ SORTIE — UNE valeur : le module. [rend: 1] ⑥ TRAITEMENT — importlib.
    ⑦ UNITÉ — — ⑧ POURQUOI — Une écriture recopiée finit par différer. ⑨ CE QUI CLOCHE — Le code de tête du
    fabricant s'exécute (lecture de la table). ⑩ EFFET — Lit la racine. ⑪ TERMINAISON — Rend la main, ou lève.
    [sort: non]
    """
    spec = importlib.util.spec_from_file_location("FABRICANT_DU_RAPATRIEMENT", os.path.join(racine, FABRICANT))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(racine, *args):
    """Lance git dans la racine ; rend (code, sortie en octets, erreurs en texte).

    ① RÔLE — Un appel borné. ② CONTEXTE D'APPEL — `rapatrier`. ③ ENTRÉE — la racine, les arguments.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — TROIS valeurs. [rend: 3] ⑥ TRAITEMENT — subprocess, 600 s.
    ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — Un dépassement lève TimeoutExpired (code non nul au programme).
    ⑩ EFFET — Ce que fait git. ⑪ TERMINAISON — Rend la main ; 600 s au plus. [sort: non]
    """
    p = subprocess.run(["git", "-C", racine] + list(args), capture_output=True, timeout=600)
    return p.returncode, p.stdout, p.stderr.decode("utf-8", "replace")


def rapatrier(racine, passage, depuis="origin"):
    """Rapatrie un passage ; rend (code de sortie, lignes du bilan).

    ① RÔLE — Le corps du programme (fiche en tête). ② CONTEXTE D'APPEL — `main` ; l'épreuve. ③ ENTRÉE — `racine`,
    `passage` (chiffres), `depuis`. ④ CONDITIONS D'ENTRÉE — Fiche en tête. ⑤ SORTIE — DEUX valeurs : le code (0, 1,
    2 : fiche en tête, ⑤) et les lignes du bilan. [rend: 2] ⑥ TRAITEMENT — Fiche en tête, ⑥. ⑦ UNITÉ — —
    ⑧ POURQUOI — Fiche en tête. ⑨ CE QUI CLOCHE — Fiche en tête. ⑩ EFFET — Fiche en tête.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    if not re.fullmatch(r"[0-9]{1,20}", passage):
        return 2, [f"ARRET passage refusé : {passage[:40]!r} (des chiffres)"]
    try:
        F = fabricant(racine)
        BRANCHES, CODE = F.EPREUVES_BRANCHES, re.compile(F.CODE_DE_SERIE)
    except Exception as e:   # noqa: BLE001 — sans le fabricant, rien de sûr
        return 2, [f"ARRET fabricant illisible : {type(e).__name__} : {e}"]
    lues = f"refs/epreuves_lues/{passage}/"
    c, _, err = git(racine, "fetch", "-q", "--no-tags", depuis, f"+refs/heads/{BRANCHES}{passage}/*:{lues}*")
    if c != 0:
        return 2, [f"ARRET branches du passage {passage} illisibles : {err.strip()[:200]}"]
    c, refs, err = git(racine, "for-each-ref", "--format=%(refname)", lues)
    refs = [r for r in refs.decode().split("\n") if r]
    if c != 0 or not refs:
        return 2, [f"ARRET aucune branche {BRANCHES}{passage}/* lue"]
    dossier = os.path.join(racine, RANGEMENT, passage)
    bilan, codes = [f"passage {passage} : {len(refs)} branche(s) lue(s) ({BRANCHES}{passage}/<code>)"], []
    demandes, vus = set(), []
    for ref in sorted(refs):
        code = ref[len(lues):]
        if not CODE.fullmatch(code):
            bilan.append(f"{code[:40]!r} : nom de branche refusé, non rapatrié")
            codes.append(2)
            continue
        vus.append(code)
        c, archive, err = git(racine, "archive", "--format=tar", ref)
        neuf = tempfile.mkdtemp(prefix="rapatrier_")
        try:
            if c != 0:
                raise OSError(f"archive illisible : {err.strip()[:200]}")
            with tempfile.TemporaryFile() as t:
                t.write(archive)
                t.seek(0)
                with tarfile.open(fileobj=t) as tar:
                    for m in tar.getmembers():
                        if not (m.isfile() or m.isdir()) or m.name.startswith("/") or ".." in m.name.split("/"):
                            raise OSError(f"membre refusé dans l'archive : {m.name[:80]}")
                    tar.extractall(neuf)
            source = os.path.join(neuf, SORTIES, passage, code)
            try:
                demande = json.load(open(os.path.join(source, DEMANDE), encoding="utf-8"))
                demande = tuple(d["code"] for d in demande)
                if not demande or not all(isinstance(d, str) and CODE.fullmatch(d) for d in demande):
                    raise ValueError
                demandes.add(demande)
            except (OSError, ValueError, KeyError, TypeError):
                demandes.add(None)
            cible = os.path.join(dossier, code)
            voisin = cible + ".neuf"
            if os.path.isdir(voisin):
                shutil.rmtree(voisin)
            try:
                shutil.copytree(source, voisin)
                journaux = os.path.join(neuf, "rapports", "journal_du_circuit")
                if os.path.isdir(journaux):
                    for j in os.listdir(journaux):
                        shutil.copyfile(os.path.join(journaux, j), os.path.join(voisin, j))
                r = json.load(open(os.path.join(voisin, "RESULTAT.json"), encoding="utf-8"))
                cs = r["code_de_sortie"]
                if not isinstance(cs, int) or isinstance(cs, bool):
                    raise ValueError(f"code de sortie illisible : {cs!r}")
            except BaseException:
                shutil.rmtree(voisin, ignore_errors=True)
                if os.path.isdir(cible):
                    bilan.append(f"{code} : ancien résultat gardé (le nouveau n'est pas complet)")
                raise
            if os.path.isdir(cible):
                ancien = cible + ".ancien"
                shutil.rmtree(ancien, ignore_errors=True)
                os.rename(cible, ancien)
                os.rename(voisin, cible)
                shutil.rmtree(ancien)
            else:
                os.rename(voisin, cible)
            commande = " ".join([r.get("chemin", "?")] + [a for a in r.get("arguments", []) if a != "{copie}"])
            bilan.append(f"{code} : code {cs} · {r.get('duree_secondes', '?')} s · {commande}"
                         + (f" · REFUS {r['refus']}" if r.get("refus") else ""))
            codes.append(0 if cs == 0 else 1)
        except (OSError, ValueError, KeyError, json.JSONDecodeError, tarfile.TarError) as e:
            bilan.append(f"{code} : RIEN DE SUR ({type(e).__name__} : {e})")
            codes.append(2)
        finally:
            shutil.rmtree(neuf, ignore_errors=True)
    if None in demandes or len(demandes) != 1:
        bilan.append("liste demandée INCONNUE (DEMANDE.json absent, illisible, ou différent d'une branche à l'autre) : "
                     "rien de sûr sur les épreuves manquantes")
        codes.append(2)
    else:
        demande = next(iter(demandes))
        for c in demande:
            if c not in vus:
                bilan.append(f"{c} : ABSENTE (demandée, aucune branche : machine tombée, job annulé, poussée refusée ?)")
                codes.append(2)
        for c in vus:
            if c not in demande:
                bilan.append(f"{c} : branche NON DEMANDÉE par ce passage")
                codes.append(2)
        bilan[0] += f" · demandées {len(demande)} · rapatriées {len(vus)}"
    os.makedirs(dossier, exist_ok=True)
    with open(os.path.join(dossier, "BILAN.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(bilan) + "\n")
    return max(codes), bilan


def main():
    """La ligne de commande (fiche en tête).

    ① RÔLE — Lire les arguments, rapatrier, afficher le bilan. ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — sys.argv. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le code. [rend: 1]
    ⑥ TRAITEMENT — deux positionnels, `--depuis=` facultatif ; sinon usage, code 2. ⑦ UNITÉ — — ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Fiche en tête. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    pos = [a for a in sys.argv[1:] if not a.startswith("--")]
    opt = [a for a in sys.argv[1:] if a.startswith("--")]
    if len(pos) != 2 or any(not o.startswith("--depuis=") for o in opt) or len(opt) > 1:
        print("usage : rapatrier_les_epreuves_longues.py <racine> <passage> [--depuis=<dépôt>]", file=sys.stderr)
        return 2
    depuis = opt[0][len("--depuis="):] if opt else "origin"
    code, bilan = rapatrier(os.path.abspath(pos[0]), pos[1], depuis)
    print("\n".join(bilan))
    return code


if __name__ == "__main__":
    sys.exit(main())
