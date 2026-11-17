#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_MOULINETTE_D_ESSAI — Lun 16-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Épreuves R-731 de programmes/PREPARER_LA_MOULINETTE_D_ESSAI.py (décisions de Jean-Luc A-853 et A-861
du 16-11-2026 : la fiche d'essai C5 2000-2026 vit dans une copie jetable du registre, jamais dans le vrai). Quatre
propriétés, chacune avec un sabotage qui doit la faire rougir : le refus sur un dépôt (racine avec .git) ; la copie a
exactement une ligne de plus et toutes les autres identiques à l'octet ; le registre d'un dépôt refusé est inchangé ;
la ligne d'essai est la vraie ligne C5 recopiée, seuls l'identifiant, la période et le statut changeant.

① RÔLE — Jouer les cas E1 à E6 sur le programme tel quel (Z0), puis, avec --saboter, sous chaque sabotage S1 à S7.
② CONTEXTE D'APPEL — À la main, par le Chat ou un agent ; la certification si on l'y inscrit.
③ ENTRÉE — La ligne de commande : la racine d'un dépôt ou d'une copie (lue, jamais écrite), « --saboter » facultatif.
④ CONDITIONS D'ENTRÉE — La racine porte le programme, programmes/, donnees/cac40_strategies.csv et le fichier des 20 ans.
⑤ SORTIE — Le code de sortie : 0 si Z0 est conforme et, avec --saboter, si chaque sabotage mord ; 1 sinon ; 2 si
  l'épreuve n'a pas pu tourner (R-734).
  [rend: 1]
⑥ TRAITEMENT — Pour chaque cas, une mini-copie neuve dans un dossier temporaire (programmes/ copié, registre copié,
  fichier des 20 ans par lien symbolique) ; le programme (tel quel ou saboté) y est lancé dans un sous-processus.
⑦ UNITÉ — Des secondes (délai de chaque lancement : DELAI).
⑧ POURQUOI — R-731 : épreuves à la main avec sabotages ; un cas vient d'une vraie ligne (R-732) ; un jeu d'épreuves
  se sabote contre sa propre correction.
⑨ CE QUI CLOCHE — Les cas ne lancent pas la moulinette (« --jouer ») : elle est l'épreuve longue MoulinetteEssai.
  La racine reçue n'est que lue : son empreinte est comparée avant et après (cas E0).
⑩ EFFET — Crée et efface des dossiers temporaires ; n'écrit rien dans la racine reçue.
⑪ TERMINAISON — Sort par sys.exit. Un de mes appels peut-il ne pas revenir ? Chaque lancement est borné à DELAI.
  [sort: oui]
"""
import csv
import hashlib
import io
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

PROGRAMME = os.path.join("programmes", "PREPARER_LA_MOULINETTE_D_ESSAI.py")
REGISTRE = os.path.join("donnees", "cac40_strategies.csv")
VINGT_ANS = "temoins/TEMOIN_VINGT_ANS_2000_2026_COUPURE_2026-11-11_FIGE_Ven_13-11-2026_10h59.csv"
SOURCE_ATTENDUE = "C5E10-QA-V1"
CHANGEES = ("id", "periode", "statut")
DELAI = 120

SABOTAGES = {
    "S1_refus_du_git_retire": ('    if os.path.lexists(os.path.join(copie, ".git")):', "    if False:"),
    "S2_ligne_ecrite_deux_fois": ('f.write(octets + texte.getvalue().encode("utf-8"))',
                                  'f.write(octets + 2 * texte.getvalue().encode("utf-8"))'),
    "S3_une_ligne_existante_touchee": ('f.write(octets + texte.getvalue().encode("utf-8"))',
                                       'f.write(octets.replace(b"\\r\\n", b"\\n", 1) + texte.getvalue().encode("utf-8"))'),
    "S4_preparer_avant_le_refus": ("    refus = refus_du_lieu(copie)\n",
                                   "    try:\n        preparer(copie)\n    except Exception:\n        pass\n"
                                   "    refus = refus_du_lieu(copie)\n"),
    "S5_autre_fiche_source": ('SOURCES = ("C5-ETENDU-10", "C5E10-QA-V1", "C5E10-OBS-V1")',
                              'SOURCES = ("C5-ETENDU-10", "C5E10-OBS-V1", "C5E10-QA-V1")'),
    "S6_borne_de_fin_oubliee": ('BORNE_DE_FIN_EXCLUE = "2026-10-30"', 'BORNE_DE_FIN_EXCLUE = "9999-12-31"'),
    "S7_periode_non_changee": ('("periode", "%s -> %s" % (debut, fin)), ', ""),
}


def empreinte(chemin):
    """Rend l'empreinte SHA-256 d'un fichier. ① RÔLE — Comparer à l'octet. ② CONTEXTE D'APPEL — les cas.
    ③ ENTRÉE — un chemin. ④ CONDITIONS D'ENTRÉE — le fichier existe. ⑤ SORTIE — UNE valeur : 64 caractères
    hexadécimaux. [rend: 1] ⑥ TRAITEMENT — hashlib. ⑦ UNITÉ — — ⑧ POURQUOI — « identique à l'octet ».
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lit le fichier. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def mini_copie(racine, texte_du_programme, avec_git):
    """Fabrique une mini-copie neuve et rend son chemin. ① RÔLE — Un lieu jetable par cas. ② CONTEXTE D'APPEL —
    `jouer_les_cas`. ③ ENTRÉE — la racine reçue ; le texte du programme à poser ; `avec_git` : poser un dossier .git.
    ④ CONDITIONS D'ENTRÉE — fiche en tête, ④. ⑤ SORTIE — UNE valeur : le chemin de la mini-copie. [rend: 1]
    ⑥ TRAITEMENT — programmes/ copié ; le programme remplacé par le texte reçu ; registre copié ; donnees/combinatoires
    créé ; fichier des 20 ans par lien. ⑦ UNITÉ — — ⑧ POURQUOI — Ne jamais écrire dans la racine reçue ; 6 Mo par
    cas au lieu de 600. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Crée un dossier temporaire. ⑪ TERMINAISON — Rend la main.
    [sort: non]"""
    d = tempfile.mkdtemp(prefix="essai_moulinette_")
    shutil.copytree(os.path.join(racine, "programmes"), os.path.join(d, "programmes"),
                    ignore=shutil.ignore_patterns("__pycache__"))
    with open(os.path.join(d, PROGRAMME), "w", encoding="utf-8") as f:
        f.write(texte_du_programme)
    os.makedirs(os.path.join(d, "donnees", "combinatoires"))
    shutil.copyfile(os.path.join(racine, REGISTRE), os.path.join(d, REGISTRE))
    os.makedirs(os.path.join(d, "temoins"))
    os.symlink(os.path.join(os.path.abspath(racine), VINGT_ANS), os.path.join(d, VINGT_ANS))
    if avec_git:
        os.makedirs(os.path.join(d, ".git"))
    return d


def lancer(copie):
    """Lance le programme de la mini-copie sur elle ; rend (code, sortie). ① RÔLE — Un lancement borné.
    ② CONTEXTE D'APPEL — `jouer_les_cas`. ③ ENTRÉE — la mini-copie. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — DEUX
    valeurs : le code de sortie (124 au délai) ; la sortie et les erreurs. [rend: 2] ⑥ TRAITEMENT — subprocess.run.
    ⑦ UNITÉ — Des secondes. ⑧ POURQUOI — Le code de sortie est ce que le circuit lit. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance un processus. ⑪ TERMINAISON — Rend la main ; DELAI au plus. [sort: non]"""
    try:
        p = subprocess.run([sys.executable, "-B", os.path.join(copie, PROGRAMME), copie], capture_output=True,
                           text=True, timeout=DELAI, cwd=copie)
    except subprocess.TimeoutExpired:
        return 124, "délai dépassé"
    return p.returncode, p.stdout + p.stderr


def jouer_les_cas(racine, texte_du_programme):
    """Joue E1 à E6 ; rend la liste des cas faux (vide si tout est conforme). ① RÔLE — Le jeu d'épreuves.
    ② CONTEXTE D'APPEL — `main`, pour Z0 et chaque sabotage. ③ ENTRÉE — la racine ; le texte du programme.
    ④ CONDITIONS D'ENTRÉE — fiche en tête, ④. ⑤ SORTIE — UNE valeur : la liste des cas faux, chacun « Ex : raison ».
    [rend: 1] ⑥ TRAITEMENT — E1 refus sur une racine avec .git (code 2, « porte .git ») ; E2 une ligne de plus, les
    octets d'origine en préfixe exact ; E3 registre inchangé après le refus de E1 ; E4 la vraie ligne C5E10-QA-V1
    recopiée, seuls id, periode, statut changent, période 2000-01-03 -> dernière séance avant le 2026-10-30, calculée
    ici par une lecture à part du fichier des 20 ans ; E5 second passage refusé, registre inchangé ; E6 combinatoire
    d'une version marquée OUI, seuils 0.04 et 0.025, horizon 20. ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête.
    ⑨ CE QUI CLOCHE — E4 recalcule la période à part : un défaut commun aux deux lectures passerait. ⑩ EFFET — Crée
    et efface des mini-copies. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    faux = []
    origine = open(os.path.join(racine, REGISTRE), "rb").read()
    # E1 et E3 : une racine avec .git
    d = mini_copie(racine, texte_du_programme, True)
    try:
        avant = empreinte(os.path.join(d, REGISTRE))
        code, sortie = lancer(d)
        if code != 2 or "porte .git" not in sortie:
            faux.append("E1 refus sur un dépôt : code %d, %r" % (code, sortie[-200:]))
        if empreinte(os.path.join(d, REGISTRE)) != avant:
            faux.append("E3 le registre d'un dépôt refusé a changé")
    finally:
        shutil.rmtree(d, ignore_errors=True)
    # E2, E4, E5, E6 : une copie sans .git
    d = mini_copie(racine, texte_du_programme, False)
    try:
        code, sortie = lancer(d)
        neuf = open(os.path.join(d, REGISTRE), "rb").read()
        if code != 0:
            faux.append("E2 préparation : code %d, %r" % (code, sortie[-200:]))
        lignes_o = origine.splitlines(keepends=True)
        lignes_n = neuf.splitlines(keepends=True)
        if not neuf.startswith(origine) or len(lignes_n) != len(lignes_o) + 1 or lignes_n[:-1] != lignes_o:
            faux.append("E2 une ligne de plus, les autres à l'octet : %d lignes contre %d, préfixe %s" % (
                len(lignes_n), len(lignes_o), "identique" if neuf.startswith(origine) else "différent"))
        lues_o = list(csv.reader(io.StringIO(origine.decode("utf-8-sig"), newline="")))
        lues_n = list(csv.reader(io.StringIO(neuf.decode("utf-8-sig"), newline="")))
        entete = lues_o[0]
        src = [r for r in lues_o[1:] if r and r[0] == SOURCE_ATTENDUE][-1]
        essai = lues_n[-1]
        dates = {r["date"] for r in csv.DictReader(open(os.path.join(racine, VINGT_ANS), encoding="utf-8-sig"))}
        periode = "%s -> %s" % (min(x for x in dates if x[:4] == "2000"), max(x for x in dates if x < "2026-10-30"))
        attendu = dict(zip(entete, src), id="ESSAI-C5-2000-2026", periode=periode)
        ecarts = [c for c in entete if c != "statut" and dict(zip(entete, essai)).get(c) != attendu[c]]
        statut = dict(zip(entete, essai)).get("statut", "")
        if len(essai) != len(src) or ecarts or not statut.startswith("ESSAI") or statut == attendu["statut"]:
            faux.append("E4 vraie ligne C5 : colonnes en écart %s, statut %r" % (ecarts, statut[:40]))
        avant = empreinte(os.path.join(d, REGISTRE))
        code, sortie = lancer(d)
        if code != 2 or empreinte(os.path.join(d, REGISTRE)) != avant:
            faux.append("E5 second passage : code %d, registre %s" % (
                code, "inchangé" if empreinte(os.path.join(d, REGISTRE)) == avant else "CHANGÉ"))
        comb = os.path.join(d, "donnees", "combinatoires", "COMBINATOIRE_ESSAI-C5-2000-2026_E01.csv")
        v = list(csv.DictReader(open(comb, encoding="utf-8"))) if os.path.isfile(comb) else []
        if len(v) != 1 or (v[0]["tp"], v[0]["sl"], v[0]["horizon"], v[0]["version_de_la_fiche"],
                           v[0]["versions_dans_l_essai"], v[0]["univers"]) != (
                "0.04", "0.025", "20", "OUI", "1", attendu["univers"]):
            faux.append("E6 combinatoire : %r" % (v[:1],))
    except (OSError, IndexError, KeyError, ValueError) as e:
        faux.append("E2-E6 illisibles : %s : %s" % (type(e).__name__, e))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return faux


def main(arguments):
    """Point d'entrée ; rend le code de sortie. ① RÔLE — Z0 puis les sabotages. ② CONTEXTE D'APPEL — `__main__`.
    ③ ENTRÉE — sys.argv[1:]. ④ CONDITIONS D'ENTRÉE — fiche en tête, ④. ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1]
    ⑥ TRAITEMENT — E0 empreinte du registre de la racine avant ; Z0 ; chaque sabotage : son ancre présente une fois,
    remplacée, jeu des cas, « mord » si au moins un cas est faux ; E0 après. ⑦ UNITÉ — — ⑧ POURQUOI — R-731, R-734.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Affiche. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    positions = [a for a in arguments if not a.startswith("--")]
    if len(positions) != 1 or set(a for a in arguments if a.startswith("--")) - {"--saboter"}:
        print("ARRET usage : <racine> [--saboter]")
        return 2
    racine = os.path.abspath(positions[0])
    try:
        texte = open(os.path.join(racine, PROGRAMME), encoding="utf-8").read()
        e0 = empreinte(os.path.join(racine, REGISTRE))
    except OSError as e:
        print("ARRET %s" % e)
        return 2
    ok = True
    faux = jouer_les_cas(racine, texte)
    print("Z0 programme tel quel : %s" % ("E1 à E6 conformes" if not faux else "FAUX %s" % faux))
    ok = ok and not faux
    if "--saboter" in arguments:
        for nom, (ancre, remplacement) in SABOTAGES.items():
            if texte.count(ancre) != 1:
                print("%s : ancre trouvée %d fois — sabotage NON JOUÉ" % (nom, texte.count(ancre)))
                ok = False
                continue
            faux_s = jouer_les_cas(racine, texte.replace(ancre, remplacement))
            print("%s %s : %s" % (nom, "mord" if faux_s else "NE MORD PAS", [f.split(" : ")[0] for f in faux_s]))
            ok = ok and bool(faux_s)
    if empreinte(os.path.join(racine, REGISTRE)) != e0:
        print("E0 le registre de la racine reçue a changé")
        ok = False
    print("VERDICT : %s" % ("tout est conforme" if ok else "NON CONFORME"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
