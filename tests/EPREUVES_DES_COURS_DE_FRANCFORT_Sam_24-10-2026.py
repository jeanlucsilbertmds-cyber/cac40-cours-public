#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DES_COURS_DE_FRANCFORT — Sam 24-10-2026 (Paris). Simulation uniquement.

① RÔLE — Prouver que programmes/FABRIQUER_LES_COURS_DE_FRANCFORT.py refait, depuis les 38 réponses de Yahoo rangées au
  dépôt, exactement le fichier des cours de Francfort ; qu'il refuse (code 1) toute réponse que le carnet n'inscrit
  pas telle qu'elle est ; qu'il rend 2 sur une panne ou une sortie refusée ; qu'il ne laisse pas de fichier provisoire ;
  et, avec --saboter, que chacune de ses gardes, retirée, fait tomber au moins un cas.
② CONTEXTE D'APPEL — Par la certification (programmes/CERTIFIER_LA_VERSION.py), chaque nuit, depuis la racine, la racine
  en argument, puis avec --saboter. À la main :
  python3 tests/EPREUVES_DES_COURS_DE_FRANCFORT_Sam_24-10-2026.py <racine> [--saboter]
③ ENTRÉE — La racine du dépôt (lue, jamais écrite) ; l'option --saboter.
④ CONDITIONS D'ENTRÉE — —
⑤ SORTIE — Le code : 0 si chaque cas rend le code et le motif attendus (et, avec --saboter, si chaque garde retirée fait
  tomber un cas) ; 1 sinon ; 2 si l'épreuve n'a pas pu juger (une garde ou un cas ne s'applique plus, erreur imprévue).
  [rend: 1]
⑥ TRAITEMENT — Un banc dans un dossier temporaire : tout programmes/*.py, le carnet et les 38 réponses. Chaque cas : une
  copie du banc en liens durs, un fichier remplacé (jamais écrit à travers un lien), le programme lancé par
  sous-processus, son code ET un fragment de son écran comparés à l'attendu, et l'empreinte de la sortie quand elle
  est écrite. E11 éprouve la conversion d'une réponse fabriquée (clôture vide, nulle, heure de nuit) ; E12 force
  l'échec du renommage pour éprouver le nettoyage du provisoire.
⑦ UNITÉ — Des codes de sortie et des empreintes sha256.
⑧ POURQUOI — R-731 et R-755 ② ; l'empreinte attendue est MESURÉE : celle du fichier du dépôt le 24-10-2026, que l'outil
  d'avant (etudes/outils/CONFRONTER_A_FRANCFORT.py) et ce programme refont tous deux depuis les réponses
  retéléchargées le même jour.
⑨ CE QUI CLOCHE — L'empreinte attendue vient du même traitement : l'épreuve prouve qu'on le refait, pas qu'il est juste
  (la justesse vient de la confrontation à Paris, faite par l'outil). · Un arrêt brutal laisse le dossier temporaire.
⑩ EFFET — Écrit et efface un dossier temporaire ; lance le programme.
⑪ TERMINAISON — Rend la main ; chaque lancement est borné à 300 s ; sort par sys.exit.
  [sort: oui]
"""
import csv
import glob
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

PROG = "programmes/FABRIQUER_LES_COURS_DE_FRANCFORT.py"
CARNET = "donnees/PROVENANCE_DES_FICHIERS.csv"
BRUTS = "donnees/sources_francfort/bruts_yahoo_24-10-2026"
ATTENDU = "38c3ce950f6dc815100834b1bbda8039d248e5cea43c559d6fdcc72cdc76bfc1"   # mesuré le 24-10-2026


class NeSAppliquePlus(Exception):
    pass


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def construire_le_banc(depot, banc):
    """① Copier ce que lit le programme. ⑤ —. [sort: non]"""
    a_copier = {os.path.relpath(p, depot) for p in glob.glob(os.path.join(depot, "programmes", "*.py"))}
    a_copier |= {CARNET} | {os.path.relpath(p, depot) for p in glob.glob(os.path.join(depot, BRUTS, "*.json"))}
    if not any(f.startswith(BRUTS) for f in a_copier):
        raise NeSAppliquePlus("aucune réponse brute au dépôt")
    for f in sorted(a_copier):
        os.makedirs(os.path.dirname(os.path.join(banc, f)), exist_ok=True)
        shutil.copyfile(os.path.join(depot, f), os.path.join(banc, f))


def copie(banc, d):
    """① Copie du banc en liens durs. [sort: non]"""
    for base, _, fichiers in os.walk(banc):
        c = os.path.join(d, os.path.relpath(base, banc))
        os.makedirs(c, exist_ok=True)
        for f in fichiers:
            os.link(os.path.join(base, f), os.path.join(c, f))


def remplacer(d, chemin, octets):
    """① Remplacer un fichier sans écrire à travers son lien. [sort: non]"""
    p = os.path.join(d, chemin)
    if os.path.lexists(p):
        os.remove(p)
    with open(p, "wb") as f:
        f.write(octets)


def cas(banc):
    """① La table des cas. ⑤ UNE valeur : nom → (préparation, arguments, code, fragment, empreinte ou None).
      [rend: 1]
      [sort: non]"""
    carnet = open(os.path.join(banc, CARNET), "rb").read()
    acr = f"{BRUTS}/ACR.F.json"
    brut = open(os.path.join(banc, acr), "rb").read()
    if b'"close":[' not in brut or not carnet.count(acr.encode() + b","):
        raise NeSAppliquePlus("la réponse d'Accor ou sa ligne au carnet a changé de forme")
    ligne_acr = [l for l in carnet.split(b"\n") if l.startswith(acr.encode() + b",")][0]

    def carnet_sans(d):
        remplacer(d, CARNET, b"\n".join(l for l in carnet.split(b"\n") if l != ligne_acr))

    def carnet_double(d):
        remplacer(d, CARNET, carnet.rstrip(b"\n") + b"\n" + ligne_acr + b"\n")

    def carnet_autre_sorte(d):
        remplacer(d, CARNET, carnet.replace(ligne_acr, ligne_acr.replace("téléchargement".encode(), "écrit à la main".encode(), 1)))

    def brut_altere(d):
        i = brut.index(b'"close":[') + 9
        j = i
        while brut[j:j + 1] not in b"0123456789":
            j += 1
        chiffre = b"1" if brut[j:j + 1] != b"1" else b"2"
        remplacer(d, acr, brut[:j] + chiffre + brut[j + 1:])

    def brut_mal_forme(d):
        o = b'{"chart":{"result":[]}}'
        remplacer(d, acr, o)
        remplacer(d, CARNET, carnet.replace(ligne_acr, ligne_acr.replace(
            ligne_acr.split(b",")[1], hashlib.sha256(o).hexdigest().encode(), 1)))

    return {
        "E01_vraies_reponses": (None, ["{d}", "{s}"], 0, "écrit :", ATTENDU),
        "E02_reponse_alteree": (brut_altere, ["{d}", "{s}"], 1, "empreinte différente", None),
        "E03_reponse_absente": (lambda d: os.remove(os.path.join(d, acr)), ["{d}", "{s}"], 1, "réponse absente", None),
        "E04_ligne_du_carnet_retiree": (carnet_sans, ["{d}", "{s}"], 1, "inscrit 0 fois", None),
        "E05_ligne_du_carnet_en_double": (carnet_double, ["{d}", "{s}"], 1, "inscrit 2 fois", None),
        "E06_inscrite_autrement": (carnet_autre_sorte, ["{d}", "{s}"], 1, "pas comme téléchargement", None),
        "E07_sortie_existante": (lambda d: open(os.path.join(os.path.dirname(d), "sortie_" + os.path.basename(d)), "w").close(),
                                 ["{d}", "{s}"], 2, "la sortie existe déjà", None),
        "E08_sortie_sous_la_racine": (None, ["{d}", "{d}/donnees/x.csv"], 2, "sous la racine", None),
        "E09_sans_argument": (None, [], 2, "usage", None),
        "E10_reponse_mal_formee_inscrite": (brut_mal_forme, ["{d}", "{s}"], 2, "IMPOSSIBLE", None),
        "E11_conversion": ("CONVERSION", None, 0, "CONVERSION JUSTE", None),
        "E12_renommage_refuse": ("RENOMMAGE", ["{d}", "{s}"], 2, "IMPOSSIBLE", None),
    }


CONVERSION = r'''
import json, sys
sys.path.insert(0, sys.argv[1]); sys.dont_write_bytecode = True
import FABRIQUER_LES_COURS_DE_FRANCFORT as F
r = {"chart": {"result": [{"timestamp": [946890000, 946976400, 947062800, 947113200],
                           "indicators": {"quote": [{"close": [None, 0.0, 10.123456, 11.5]}]}}]}}
c = F.clotures(json.dumps(r).encode())
# 947113200 = 05-01-2000 23h00 en temps universel : + 2 h, le 06-01-2000 ; une clôture vide et une nulle tombent
print("CONVERSION JUSTE" if c == {"2000-01-05": 10.123456, "2000-01-06": 11.5} else f"CONVERSION FAUSSE {c}")
'''
RENOMMAGE = r'''
import os, runpy, sys
def refuse(*a, **k):
    raise OSError("renommage refusé par l'épreuve")
os.rename = refuse
sys.argv = [sys.argv[1]] + sys.argv[2:]
runpy.run_path(sys.argv[0], run_name="__main__")
'''


def jouer(banc, travail, table, prog, bavard=True, premiere_chute=False):
    """① Jouer les cas. ⑤ DEUX valeurs : justes, faux.
      [rend: 2]
      [sort: non]"""
    justes, faux = [], []
    for nom, (prep, args, attendu, fragment, empreinte) in table.items():
        d = tempfile.mkdtemp(prefix="cas_", dir=travail)
        s = os.path.join(os.path.dirname(d), "sortie_" + os.path.basename(d))
        try:
            copie(banc, d)
            p = os.path.join(d, prog)
            if prep == "CONVERSION":
                cmd = [sys.executable, "-B", "-I", "-c", CONVERSION, os.path.dirname(p)]
            elif prep == "RENOMMAGE":
                cmd = [sys.executable, "-B", "-I", "-c", RENOMMAGE, p] + [a.format(d=d, s=s) for a in args]
            else:
                if prep:
                    prep(d)
                cmd = [sys.executable, "-B", "-I", p] + [a.format(d=d, s=s) for a in args]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            ecran = r.stdout + r.stderr
            ok = r.returncode == attendu and fragment in ecran
            if empreinte is not None:
                ok = ok and os.path.isfile(s) and sha(s) == empreinte
            if attendu != 0 and os.path.exists(s) and nom != "E07_sortie_existante":
                ok = False
            if any(".en_cours." in f for f in os.listdir(os.path.dirname(s)) if f.startswith("sortie_" + os.path.basename(d))):
                ok = False
            (justes if ok else faux).append(nom)
            if bavard or not ok:
                print(("OK   " if ok else "FAUX ") + f"{nom} : code {r.returncode} (attendu {attendu}, motif « {fragment} ») — "
                      + ecran.strip().splitlines()[-1][:110] if ecran.strip() else "")
        finally:
            shutil.rmtree(d, ignore_errors=True)
            for f in os.listdir(os.path.dirname(s)):
                if f.startswith("sortie_" + os.path.basename(d)):
                    os.remove(os.path.join(os.path.dirname(s), f))
        if premiere_chute and faux:
            break
    return justes, faux


GARDES = {
    "G01_empreinte": ("    if hashlib.sha256(octets).hexdigest() != lignes[0][\"sha256\"]:", "    if False:"),
    "G02_une_seule_ligne": ("    if len(lignes) != 1:", "    if not lignes:"),
    "G03_sorte": ("    if lignes[0][\"produit_par\"] != TELECHARGEMENT:", "    if False:"),
    "G04_reponse_absente": ("    if not os.path.isfile(p):", "    if False:"),
    "G05_sortie_existante": ("    if os.path.exists(sortie) or os.path.commonpath([sortie, racine]) == racine:",
                             "    if os.path.commonpath([sortie, racine]) == racine:"),
    "G06_sortie_sous_la_racine": ("    if os.path.exists(sortie) or os.path.commonpath([sortie, racine]) == racine:",
                                  "    if os.path.exists(sortie):"),
    "G07_cloture_vide": ("        if fermes[i] is None:\n            continue", "        if False:\n            continue"),
    "G08_cloture_positive": ("        if fermes[i] > 0:", "        if True:"),
    "G09_deux_heures": ("datetime.timedelta(hours=2)", "datetime.timedelta(hours=0)"),
    "G10_fin_de_bnains": ("if d <= FIN_DE_BNAINS)", "if True)"),
    "G11_arrondi": ("repr(round(x, 4))", "repr(x)"),
    "G12_ordre": ("    ordre = sorted(SYMBOLES.items(), key=lambda vs: f\"{vs[0]}__{vs[1]}.csv\")",
                  "    ordre = sorted(SYMBOLES.items(), key=lambda vs: f\"{vs[0]}__{vs[1]}.csv\", reverse=True)"),
    "G13_nettoyage_du_provisoire": ("            os.remove(provisoire)", "            pass"),
    "G14_refus_en_code_1": ("        return 1\n", "        return 2\n"),
    "G15_dernier_filet": ("    except Exception as e:                                # dernier filet",
                          "    except ZeroDivisionError as e:                        # dernier filet"),
}


def main(argv):
    """① Le point d'entrée. ⑤ UNE valeur : le code de sortie.
      [rend: 1]
      [sort: non]"""
    args = [a for a in argv[1:] if a != "--saboter"]
    if len(args) != 1 or not os.path.isdir(args[0]):
        print("VERDICT IMPOSSIBLE — appel mal formé")
        return 2
    depot = os.path.abspath(args[0])
    travail = tempfile.mkdtemp(prefix="epreuves_francfort.")
    try:
        banc = os.path.join(travail, "banc")
        construire_le_banc(depot, banc)
        table = cas(banc)
        justes, faux = jouer(banc, travail, table, PROG)
        print(f"BILAN {len(justes)} / {len(table)} cas justes")
        ok, impossible = not faux, False
        if "--saboter" in argv[1:]:
            source = open(os.path.join(banc, PROG), encoding="utf-8").read()
            for nom, (a, b) in GARDES.items():
                if source.count(a) != 1:
                    print(f"{nom} NE S'APPLIQUE PLUS")
                    impossible = True
                    continue
                sab = os.path.join(travail, "sabotage")
                shutil.rmtree(sab, ignore_errors=True)
                copie(banc, sab)
                remplacer(sab, PROG, source.replace(a, b).encode("utf-8"))
                _, tombes = jouer(sab, travail, table, PROG, bavard=False, premiere_chute=True)
                shutil.rmtree(sab, ignore_errors=True)
                print(f"{nom} mord : {tombes}" if tombes else f"{nom} NE MORD PAS []")
                ok = ok and bool(tombes)
    except NeSAppliquePlus as e:
        print(f"VERDICT IMPOSSIBLE — un cas ne s'applique plus : {e}")
        return 2
    except Exception as e:
        print(f"VERDICT IMPOSSIBLE — erreur imprévue de l'épreuve : {type(e).__name__} : {e}")
        return 2
    finally:
        shutil.rmtree(travail, ignore_errors=True)
    if impossible:
        print("VERDICT IMPOSSIBLE — une garde ne s'applique plus")
        return 2
    print("VERDICT", "CONFORME" if ok else "NON CONFORME")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
