#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_COMBLEMENT — Jeu 24-09-2026 (Paris)

À QUOI ÇA SERT : prouver que le comblement du trou de juillet (A-473) refuse ce qu'il
doit refuser, et que chaque protection tombe quand on la retire. Chaque épreuve
travaille sur une COPIE du dépôt, remise à l'état d'avant le comblement ; le dépôt
lui-même n'est jamais touché.

USAGE : python3 tests/EPREUVES_DU_COMBLEMENT_Jeu_24-09-2026.py <racine du dépôt>
CODE : 0 si toutes les épreuves rendent le résultat attendu, 1 sinon, 2 si l'histoire git manque
(clone superficiel : il faut la version 6caf152^1).
"""
import csv, os, shutil, subprocess, sys, tempfile

RACINE = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
DU, AU = "2026-07-13", "2026-07-30"
BRUT = "temoins/euronext_brut"
TEMOIN = f"temoins/TEMOIN_EURONEXT_TROU_{DU}_AU_{AU}.csv"
COMBLER = "programmes/COMBLER_LE_TROU_DEPUIS_EURONEXT.py"
# L'ÉTAT D'AVANT LE COMBLEMENT EST UNE VERSION FIXE DE L'HISTOIRE, PAS « origin/main »
# (28-09-2026). Tant que le comblement n'était pas fusionné, origin/main était cet état ;
# depuis la fusion du 25-09-2026 (6caf152, « Fusion du comblement de juillet (A-473) »),
# origin/main porte déjà les 406 lignes euronext, et l'épreuve E0 tombait — sur main aussi.
# 6caf152^1 est la version officielle juste avant la fusion : 0 ligne euronext au maître.
AVANT_COMBLEMENT = "6caf152^1"
# UN CLONE SUPERFICIEL N'A PAS CETTE VERSION (relecteur du Chat, 28-09-2026 : le mode d'emploi
# du dépôt et les prompts de Cowork clonent en --depth 1). On le dit en clair, code 2 (R-734).
if subprocess.run(["git", "-C", RACINE, "cat-file", "-e", AVANT_COMBLEMENT + "^{commit}"],
                  capture_output=True).returncode != 0:
    print(f"ARRÊT — la version {AVANT_COMBLEMENT} est absente de {RACINE} (clone superficiel ?) : "
          "lancer « git fetch --unshallow » ou cloner sans --depth, puis relancer. Rien n'a été éprouvé.")
    sys.exit(2)
VERSER = "programmes/TENIR_L_HISTORIQUE.py"
resultats = []


COPIES = []


def _effacer_les_copies():
    for c in COPIES:
        shutil.rmtree(c, ignore_errors=True)


import atexit
atexit.register(_effacer_les_copies)   # chaque copie pèse le dépôt : sans cela, le disque se remplit


def copie():
    """Une copie du dépôt, dont le maître est remis à sa version enregistrée d'avant.

    UNE SEULE COPIE VIVANTE À LA FOIS (17-10-2026) : chaque « d = copie() » ne sert que jusqu'à la copie suivante,
    donc les précédentes sont effacées avant d'en faire une nouvelle ; la dernière l'est à la sortie (atexit).
    Raison : 79 copies d'environ 290 Mo, gardées jusqu'à la fin, remplissaient le disque — l'épreuve échouait sur
    une copie impossible (« shutil.Error ») pendant la vérification du 17-10-2026 à 16h53 — trace au relevé
    tests/resultats/RELECTURES_DE_LA_REPARATION_DES_EPREUVES_DU_GARDE_FOU_Sam_17-10-2026.txt (superviseur de 22h09,
    R-759 : de fond ; même relevé). L'autre voie, copier sans « .git », n'a pas été prise : l'épreuve a besoin des versions.
    """
    _effacer_les_copies()
    del COPIES[:]
    d = tempfile.mkdtemp(prefix="epreuve_")
    COPIES.append(d)
    shutil.copytree(RACINE, d, dirs_exist_ok=True, symlinks=True)
    # la version d'avant le comblement : AVANT_COMBLEMENT, pour le fichier ET pour
    # la version enregistrée que relit la protection « le maître ne rétrécit pas »
    subprocess.run(["git", "-C", d, "reset", "-q", "--soft", AVANT_COMBLEMENT], check=True)
    subprocess.run(["git", "-C", d, "checkout", "-q", AVANT_COMBLEMENT, "--",
                    "donnees/cours_maitre.csv"], check=True)
    if os.path.exists(os.path.join(d, TEMOIN)):
        os.remove(os.path.join(d, TEMOIN))
    return d


def lancer(d, *args):
    p = subprocess.run([sys.executable, *args], cwd=d, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def remplacer(d, chemin, avant, apres):
    p = os.path.join(d, chemin)
    s = open(p, encoding="utf-8").read()
    assert s.count(avant) == 1, f"sabotage impossible, motif introuvable dans {chemin} : {avant[:50]}"
    open(p, "w", encoding="utf-8").write(s.replace(avant, apres))


def sources(d):
    c = {}
    for r in csv.DictReader(open(os.path.join(d, "donnees/cours_maitre.csv"), encoding="utf-8-sig")):
        c[r["source"]] = c.get(r["source"], 0) + 1
    return c


def epreuve(nom, attendu, obtenu, detail=""):
    ok = attendu == obtenu
    resultats.append(ok)
    print(f"  {'✅' if ok else '❌'} {nom} — attendu {attendu}, obtenu {obtenu} {detail}")


def combler_puis_verser(d):
    c1, s1 = lancer(d, COMBLER, ".", "--du", DU, "--au", AU, "--brut", BRUT)
    if c1:
        return c1, None, s1
    c2, s2 = lancer(d, VERSER, ".", "--increment", TEMOIN)
    return c1, c2, s1 + s2


def verser_le_soir(d, ligne7):
    """Ajoute une ligne à sept colonnes à l'incrément du soir de la copie, puis verse sans --increment."""
    p = os.path.join(d, "donnees", "claude_cours_nouveaux.csv")
    with open(p, "a", encoding="utf-8") as f:
        f.write(ligne7 + "\n")
    c, sortie = lancer(d, VERSER, ".")
    return c, sortie, None

# E0 — LE CAS NORMAL, sur les vraies données : 406 lignes « euronext », rien d'autre.
d = copie()
c1, c2, s = combler_puis_verser(d)
epreuve("E0 cas normal : codes du comblement et du versement", (0, 0), (c1, c2))
epreuve("E0 cas normal : lignes de source euronext au maître", 406, sources(d).get("euronext"))

# E1 — UN CODE ISIN QUI DÉSIGNE UNE AUTRE ACTION : le fichier de Michelin remplacé par
# celui d'Accor. Le calibrage doit refuser, et aucun témoin ne doit être écrit.
d = copie()
shutil.copy(os.path.join(d, BRUT, "FR0000120404.csv"), os.path.join(d, BRUT, "FR001400AJ45.csv"))
c, s = lancer(d, COMBLER, ".", "--du", DU, "--au", AU, "--brut", BRUT)
epreuve("E1 mauvaise action : code du comblement", 1, c)
epreuve("E1 mauvaise action : témoin écrit", False, os.path.exists(os.path.join(d, TEMOIN)))

# E2 — EURONEXT NE PUBLIE PAS UNE SÉANCE DU TROU : la ligne du 20-07 d'Accor retirée.
d = copie()
p = os.path.join(d, BRUT, "FR0000120404.csv")
lignes = open(p, encoding="utf-8-sig").read().splitlines()
open(p, "w", encoding="utf-8").write("\n".join(l for l in lignes if not l.startswith("20/07/2026")))
c, s = lancer(d, COMBLER, ".", "--du", DU, "--au", AU, "--brut", BRUT)
epreuve("E2 séance non publiée : code du comblement", 1, c, "· " + ("non publiées" in s and "motif lu" or "MOTIF ABSENT"))

# E3 — EURONEXT PUBLIE UNE SÉANCE INCONNUE DU MAÎTRE : un samedi 18-07 ajouté.
d = copie()
p = os.path.join(d, BRUT, "FR0000120404.csv")
open(p, "a", encoding="utf-8").write("\n18/07/2026;47.00;47.50;46.50;47.00;47.00;100000;1;1;47\n")
c, s = lancer(d, COMBLER, ".", "--du", DU, "--au", AU, "--brut", BRUT)
epreuve("E3 séance inconnue : code du comblement", 1, c, "· " + ("inconnues du maître ['2026-07-18']" in s and "motif lu" or "MOTIF ABSENT"))

# E4 — UNE LIGNE DU TÉMOIN QUI CONTREDIT UNE SÉANCE DÉJÀ PRÉSENTE : AIRBUS, 13-07,
# présent au maître. Le versement doit s'arrêter sans toucher au maître.
d = copie()
lancer(d, COMBLER, ".", "--du", DU, "--au", AU, "--brut", BRUT)
open(os.path.join(d, TEMOIN), "a", encoding="utf-8").write("AIRBUS,2026-07-13,1,1,1,1,1,euronext\n")
avant = open(os.path.join(d, "donnees/cours_maitre.csv"), "rb").read()
c, s = lancer(d, VERSER, ".", "--increment", TEMOIN)
apres = open(os.path.join(d, "donnees/cours_maitre.csv"), "rb").read()
epreuve("E4 séance contredite : code du versement", 1, c)
epreuve("E4 séance contredite : maître inchangé à l'octet", True, avant == apres)

# E5 — RELANCE APRÈS COMBLEMENT : rien à combler, le témoin déposé n'est pas écrasé.
d = copie()
combler_puis_verser(d)
taille = os.path.getsize(os.path.join(d, TEMOIN))
c, s = lancer(d, COMBLER, ".", "--du", DU, "--au", AU, "--brut", BRUT)
epreuve("E5 relance : code du comblement", 1, c)
epreuve("E5 relance : témoin intact", taille, os.path.getsize(os.path.join(d, TEMOIN)))

# E6 — LE DEMI-CENTIME : CARREFOUR 16,255 contre 16,26 le 25-06. Hors des bords du
# trou aujourd'hui ; on vérifie donc la tolérance sur un bord : clôture du 10-07
# d'Accor décalée d'un demi-centime → accepté ; d'un centime → refusé.
for decalage, attendu in (("48.995", 0), ("49.00", 1)):
    d = copie()
    p = os.path.join(d, BRUT, "FR0000120404.csv")
    s = open(p, encoding="utf-8-sig").read()
    s = s.replace("10/07/2026;48.72;49.19;48.59;48.99;48.99;", f"10/07/2026;48.72;49.19;48.59;48.99;{decalage};")
    open(p, "w", encoding="utf-8").write(s)
    c, _ = lancer(d, COMBLER, ".", "--du", DU, "--au", AU, "--brut", BRUT)
    epreuve(f"E6 clôture de bord à {decalage} au lieu de 48.99 : code", attendu, c)

# E7 — UNE SOURCE INVENTÉE, puis E8 — UNE SÉANCE DU LENDEMAIN : la cassure de Cowork
# du 24-09-2026, `ACCOR,2026-09-25,50,51,49,50.5,1000,n_importe_quoi`, rejouée.
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
# LA SÉANCE FUTURE EST LE PROCHAIN JOUR DE SEMAINE, jamais le simple lendemain (cassure
# de Cowork, 25-09-2026 00h05) : un vendredi, le lendemain est un samedi, refusé comme
# samedi avant le test de la date future — S6 rougissait à tort et E8 restait verte
# pour une autre raison.
def prochain_jour_de_semaine(jour):
    jour += timedelta(days=1)
    while jour.weekday() >= 5:
        jour += timedelta(days=1)
    return jour


demain = prochain_jour_de_semaine(datetime.now(ZoneInfo("Europe/Paris"))).strftime("%Y-%m-%d")
# E9 et E10 — la cassure suivante de Cowork, même soir : une date impossible entrait,
# une date mal écrite était refusée pour un motif faux.
for nom, ligne in (("E7 source inventée", "ACCOR,2026-07-14,1,1,1,1,1,n_importe_quoi\n"),
                   ("E8 séance future, prochain jour de semaine", f"ACCOR,{demain},50,51,49,50.5,1000,euronext\n"),
                   ("E9 date impossible 2026-02-30", "ACCOR,2026-02-30,50,51,49,50.5,1000,abc\n"),
                   ("E10 date mal écrite 2026-7-31", "ACCOR,2026-7-31,50,51,49,50.5,1000,abc\n")):
    d = copie()
    p = os.path.join(d, "temoins", "INCREMENT_FAUTIF.csv")
    open(p, "w", encoding="utf-8").write("valeur,date,open,high,low,close,volume,source\n" + ligne)
    avant = open(os.path.join(d, "donnees/cours_maitre.csv"), "rb").read()
    c, s_ = lancer(d, VERSER, ".", "--increment", "temoins/INCREMENT_FAUTIF.csv")
    apres = open(os.path.join(d, "donnees/cours_maitre.csv"), "rb").read()
    epreuve(f"{nom} : code du versement", 1, c)
    epreuve(f"{nom} : maître inchangé à l'octet", True, avant == apres)
    if nom.startswith(("E9", "E10")):
        epreuve(f"{nom} : motif « date illisible »", True, "date illisible" in s_)
    if nom.startswith("E8"):
        epreuve(f"{nom} : motif « postérieure au jour »", True, "postérieure au jour" in s_)

# ─── SABOTAGES DES CORRECTIONS : chaque correction retirée doit faire rougir une épreuve.
# S1 — la source redevient déduite de la date : E0 doit perdre ses 406 « euronext ».
d = copie()
remplacer(d, VERSER, '            src = r.get("source") or ""\n',
          '            src = "abc" if (r.get("date") or "") >= BASCULE_ABC else "google"\n')
combler_puis_verser(d)
epreuve("S1 source déduite de la date : lignes euronext (doit être 0)", None, sources(d).get("euronext"))

# S2 — l'option --increment ignorée : le versement lit l'incrément du soir, pas le témoin.
d = copie()
remplacer(d, VERSER, "        increment_chemin = sys.argv[i + 1]\n", "        pass\n")
combler_puis_verser(d)
epreuve("S2 --increment ignorée : lignes euronext (doit être 0)", None, sources(d).get("euronext"))

# S3 — le calibrage retiré : l'action d'Accor passe sous le nom de Michelin.
d = copie()
remplacer(d, COMBLER, "if len(bord_avant) < SEANCES_DE_BORD or len(bord_apres) < SEANCES_DE_BORD or faux:",
          "if False:")
shutil.copy(os.path.join(d, BRUT, "FR0000120404.csv"), os.path.join(d, BRUT, "FR001400AJ45.csv"))
c, _ = lancer(d, COMBLER, ".", "--du", DU, "--au", AU, "--brut", BRUT)
epreuve("S3 calibrage retiré : la mauvaise action passe (code 0)", 0, c)

# S4 — le refus de « rien à combler » retiré : la relance écrase le témoin par un vide.
d = copie()
remplacer(d, COMBLER, "    if not manques:\n", "    if False:\n")
combler_puis_verser(d)
lancer(d, COMBLER, ".", "--du", DU, "--au", AU, "--brut", BRUT)
n = sum(1 for _ in open(os.path.join(d, TEMOIN), encoding="utf-8")) - 1
epreuve("S4 refus retiré : lignes du témoin après relance (doit être 0)", 0, n)

# S5 — le refus des sources non admises retiré : la source inventée entre au maître.
d = copie()
remplacer(d, VERSER, "    elif src not in SOURCES_ADMISES:\n", "    elif False:\n")
remplacer(d, VERSER, "        debut, fin = SOURCES_ADMISES[src]\n", "        debut, fin = SOURCES_ADMISES.get(src, (None, None))\n")
p = os.path.join(d, "temoins", "INCREMENT_FAUTIF.csv")
open(p, "w", encoding="utf-8").write("valeur,date,open,high,low,close,volume,source\nACCOR,2026-07-14,48.5,48.99,48.03,48.03,487319,n_importe_quoi\n")
lancer(d, VERSER, ".", "--increment", "temoins/INCREMENT_FAUTIF.csv")
epreuve("S5 refus de source retiré : lignes « n_importe_quoi » au maître (doit être 1)", 1, sources(d).get("n_importe_quoi"))

# S6 — le refus des dates futures retiré : la séance du prochain jour de semaine repasse, le soir.
d = copie()
remplacer(d, VERSER, '    elif date > aujourd_hui:\n', "    elif False:\n")
c, _, _ = verser_le_soir(d, f"ACCOR,{demain},48.5,48.99,48.03,48.03,487319")
epreuve("S6 refus de date future retiré : code du versement du soir (doit être 0)", 0, c)

# S7 — la lecture de la date retirée : la date impossible repasse, le soir.
# RECALÉ LE 30-10-2026 (relecteur et superviseur R-759, B2, verdict DE FOND) : depuis le 29-10-2026, le lecteur commun
# refuse lui aussi la date impossible. S7 retire donc les DEUX juges — la lecture de la date dans `juger_la_ligne` et
# le compte du lecteur dans `_relecture` — et la ligne doit repasser (code 0). S7b ne retire que le premier : la ligne
# doit être mise à part par le lecteur (code 3, versement partiel décidé par Jean-Luc le 30-10-2026 à 13h55).
LECTEUR_MUET = ('''        return L.lignes_mises_a_part(c), c, ""\n''', '''        return 0, c, ""\n''')
d = copie()
remplacer(d, VERSER, "        lisible = False\n", "        lisible, jour = True, datetime(2026, 2, 27)\n")
remplacer(d, VERSER, *LECTEUR_MUET)
c, _, _ = verser_le_soir(d, "ACCOR,2026-02-30,48.5,48.99,48.03,48.03,487319")
epreuve("S7 lecture de la date et lecteur retirés : code du versement du soir (doit être 0)", 0, c)
d = copie()
remplacer(d, VERSER, "        lisible = False\n", "        lisible, jour = True, datetime(2026, 2, 27)\n")
c, s_, _ = verser_le_soir(d, "ACCOR,2026-02-30,48.5,48.99,48.03,48.03,487319")
epreuve("S7b lecture de la date seule retirée : mise à part par le lecteur (code 3, date illisible)", (3, True),
        (c, "MISE À PART : ACCOR · séance du 30-02-2026 · le lecteur commun la met à part — date illisible" in s_))

# E11 à E16 — LA LIGNE ENTIÈRE EST JUGÉE. Cassures de Cowork du 24-09-2026 à 22h34,
# ses lignes exactes ; la date 2026-07-14, un mardi, est absente du maître d'avant
# le comblement, pour que seul le jugement de la ligne entière puisse la refuser —
# `juger_la_ligne` de TENIR_L_HISTORIQUE, qui appelle aussi le juge des cours.
def verser_une_ligne(d, ligne):
    p = os.path.join(d, "temoins", "INCREMENT_FAUTIF.csv")
    open(p, "w", encoding="utf-8").write("valeur,date,open,high,low,close,volume,source\n" + ligne + "\n")
    avant = open(os.path.join(d, "donnees/cours_maitre.csv"), "rb").read()
    c, sortie = lancer(d, VERSER, ".", "--increment", "temoins/INCREMENT_FAUTIF.csv")
    return c, sortie, avant == open(os.path.join(d, "donnees/cours_maitre.csv"), "rb").read()

CAS_DE_LIGNE = [
    ("E11 cours vides", "ACCOR,2026-07-14,,,,,,euronext", "champ illisible ou vide"),
    ("E12 cours en lettres", "ACCOR,2026-07-14,abc,def,ghi,jkl,xyz,euronext", "champ illisible ou vide"),
    ("E13 cours incohérents", "ACCOR,2026-07-14,50,40,60,-5,-1000,euronext", "High 40.0 < Low 60.0"),
    ("E14 valeur inconnue", "TOTO_INCONNUE,2026-07-14,50,51,49,50.5,1000,euronext", "valeur inconnue du référentiel"),
    # E15 recalé le 29-10-2026 (superviseur R-759, A-577 étape 7) : le jour sans séance n'est plus jugé par
    # « samedi ou dimanche » dans `juger_la_ligne`, mais par le lecteur commun sur le maître complété.
    # Recalé de nouveau le 30-10-2026 (relecteur, B2) : la ligne d'avant (volume 1000) était refusée par son VOLUME et
    # n'atteignait jamais le lecteur. Celle-ci est la vraie ligne d'ACCOR du 18-09-2026, source abc, portée au dimanche
    # 20-09 : `juger_la_ligne` l'admet entièrement, seul le lecteur peut la refuser.
    ("E15 un dimanche", "ACCOR,2026-09-20,45.69,46.05,45.15,45.58,1094181,abc", "ligne(s) à part dans le maître complété"),
    ("E16 prix négatifs ordonnés", "ACCOR,2026-07-14,-5,-4,-6,-5,1000,euronext", "un prix est strictement positif"),
    ("E17 virgule décimale", "ACCOR,2026-07-14,\"48,5\",48.99,48.03,48.03,487319,euronext", "pas écrit comme au maître"),
    ("E18 plus haut infini", "ACCOR,2026-07-14,48.5,inf,48.03,48.03,487319,euronext", "pas écrit comme au maître"),
    ("E19 volume décimal", "ACCOR,2026-07-14,48.5,48.99,48.03,48.03,487319.5,euronext", "pas écrit comme au maître"),
    ("E21 cours ×100", "ACCOR,2026-07-14,4850,4899,4803,4803,487319,euronext", "hors de [0.6 ; 1.67]"),
    ("E22 en 1900", "ACCOR,1900-01-01,48.5,48.99,48.03,48.03,487319,euronext", "antérieure à la première séance"),
    ("E34 plus haut ×100", "ACCOR,2026-07-14,48.5,4899,48.03,48.03,487319,euronext", "high 4899"),
    ("E35 volume ×10⁶", "ACCOR,2026-07-14,48.5,48.99,48.03,48.03,487319000000,euronext", "volume 487319000000"),
    ("E35b volume ×61", "ACCOR,2026-07-14,48.5,48.99,48.03,48.03,40000000,euronext", "volume 40000000"),
    ("E36 valeur sans passé au maître", "ARCELORMITTAL,2026-07-15,60.12,61.38,58.92,60.74,2554843,euronext", "pas encore de séance au maître"),
    ("E37 deux marches enchaînées", "ACCOR,2026-07-14,80,90,79,88.35,487319,euronext\nACCOR,2026-07-15,160,170,159,167.9,487319,euronext", "contre une clôture"),
    ("E38 graphie inconnue du maître", "Accor,2026-07-14,48.5,48.99,48.03,48.03,487319,euronext", "inconnu du maître pour cette valeur"),
    ("E39 zéros de tête", "ACCOR,2026-07-14,048.5,48.99,48.03,48.03,0487319,euronext", "pas écrit comme au maître"),
    ("E24 colonne en trop", "ACCOR,2026-07-14,48.5,48.99,48.03,48.03,487319,euronext,EXTRA", "nombre de champs"),
    ("E25a notation scientifique", "ACCOR,2026-07-14,4.85e1,48.99,48.03,48.03,487319,euronext", "pas écrit comme au maître"),
    ("E25b chiffres pleine chasse", "ACCOR,2026-07-14,４８.５,48.99,48.03,48.03,487319,euronext", "pas écrit comme au maître"),
    ("E25c signe plus", "ACCOR,2026-07-14,48.5,48.99,48.03,48.03,+487319,euronext", "pas écrit comme au maître"),
    ("E25d espaces autour", "ACCOR,2026-07-14, 48.5 ,48.99,48.03,48.03,487319,euronext", "pas écrit comme au maître"),
    ("E26a abc en juillet", "ACCOR,2026-07-14,48.5,48.99,48.03,48.03,487319,abc", "ne couvre que"),
    # E44 et E45 — la case source se lit telle qu'elle est écrite (cassure de Cowork, 24-09-2026 23h39) ;
    # sa ligne exacte, ACCOR du 13-07 du témoin d'Euronext, portée au 14-07 absent du maître d'avant
    ("E44 case source vide", "ACCOR,2026-07-14,48.5,48.99,48.03,48.03,487319,", "case source vide"),
    ("E45 source entourée d'espaces", "ACCOR,2026-07-14,48.5,48.99,48.03,48.03,487319, euronext", "source entourée d'espaces"),
    ("E26b google après sa fin", "AXA,2026-09-24,40,41,39,40.5,1000,google", "ne couvre que"),
    ("E27 ligne sans date", "ACCOR,2026-07-14,48.5,48.99,48.03,48.03,487319,euronext\nAXA,,34.68,35,34,34.5,1000,euronext", "date illisible"),
    ("E32 nom entouré d'espaces", "accor ,2026-07-14,48.5,48.99,48.03,48.03,487319,euronext", "entouré d'espaces"),
    ("E20 séance en double", "ACCOR,2026-07-14,48.5,48.99,48.03,48.03,487319,euronext\nACCOR,2026-07-14,48.5,48.99,48.03,48.1,487319,euronext", "en double"),
]
for nom, ligne, motif in CAS_DE_LIGNE:
    d = copie()
    c, sortie, intact = verser_une_ligne(d, ligne)
    epreuve(f"{nom} : code, maître intact, motif", (1, True, True), (c, intact, motif in sortie))

# E28 à E31 — LE FICHIER LUI-MÊME : encodage, en-tête, absence, source manquante.
FICHIERS_FAUTIFS = [
    ("E28 fichier en Latin-1", "valeur,date,open,high,low,close,volume,source\nSOCIETE_G\xe9N\xe9RALE,2026-07-14,1,1,1,1,1,euronext\n".encode("latin-1"), "UTF-8"),
    ("E29 en-tête en capitales", "VALEUR,date,open,high,low,close,volume,source\nACCOR,2026-07-14,48.5,48.99,48.03,48.03,487319,euronext\n".encode(), "en-tête inattendu"),
    ("E30 séparateur point-virgule", "valeur;date;open;high;low;close;volume;source\nACCOR;2026-07-14;48.5;48.99;48.03;48.03;487319;euronext\n".encode(), "en-tête inattendu"),
    ("E31 --increment sans colonne source", "valeur,date,open,high,low,close,volume\nACCOR,2026-07-14,48.5,48.99,48.03,48.03,487319\n".encode(), "en-tête inattendu"),
    ("E33 fichier absent", None, "introuvable"),
]
for nom, octets, motif in FICHIERS_FAUTIFS:
    d = copie()
    p = os.path.join(d, "temoins", "INCREMENT_FAUTIF.csv")
    if octets is not None:
        open(p, "wb").write(octets)
    avant = open(os.path.join(d, "donnees/cours_maitre.csv"), "rb").read()
    c, sortie = lancer(d, VERSER, ".", "--increment", "temoins/INCREMENT_FAUTIF.csv")
    intact = avant == open(os.path.join(d, "donnees/cours_maitre.csv"), "rb").read()
    epreuve(f"{nom} : code, maître intact, motif, sans trace Python", (1, True, True, False),
            (c, intact, motif in sortie, "Traceback" in sortie))

# E40 — `--increment` SUR LE CHEMIN DU FICHIER DU SOIR : les raccords s'appliquent quand
# même, le mode se lit à l'option et non au chemin (agent indépendant, 24-09-2026).
d = copie()
open(os.path.join(d, "donnees", "claude_cours_nouveaux.csv"), "w", encoding="utf-8").write(
    "valeur,date,open,high,low,close,volume,source\nACCOR,2026-07-14,4850,4899,4803,4803,487319,euronext\n")
avant = open(os.path.join(d, "donnees/cours_maitre.csv"), "rb").read()
c, sortie = lancer(d, VERSER, ".", "--increment", "donnees/claude_cours_nouveaux.csv")
epreuve("E40 --increment sur le chemin du soir : code, maître intact, motif du raccord",
        (1, True, True), (c, avant == open(os.path.join(d, "donnees/cours_maitre.csv"), "rb").read(),
                          "hors de [0.6 ; 1.67]" in sortie))

# S20 — le mode relu au chemin : un fichier à SEPT colonnes, sans source, posé sur le
# chemin du soir et versé par --increment, entre alors sans aucun raccord.
SEPT = "valeur,date,open,high,low,close,volume\nACCOR,2026-07-14,4850,4899,4803,4803,487319\n"
for sabote, attendu in ((False, 1), (True, 0)):
    d = copie()
    if sabote:
        remplacer(d, VERSER, '    par_increment = "--increment" in sys.argv\n', "    par_increment = increment_chemin != INCREMENT\n")
    open(os.path.join(d, "donnees", "claude_cours_nouveaux.csv"), "w", encoding="utf-8").write(SEPT)
    c, _ = lancer(d, VERSER, ".", "--increment", "donnees/claude_cours_nouveaux.csv")
    epreuve(f"{'S20 mode relu au chemin' if sabote else 'E40b sept colonnes par --increment sur le chemin du soir'} : code", attendu, c)

# E41 à E43 — LES CONTOURNEMENTS DU QUATRIÈME TOUR (agent indépendant, 24-09-2026).
HUIT = "valeur,date,open,high,low,close,volume,source\nACCOR,2026-07-14,4850,4899,4803,4803,487319,euronext\n"

def soir_a_huit_colonnes(d):
    open(os.path.join(d, "donnees", "claude_cours_nouveaux.csv"), "w", encoding="utf-8").write(HUIT)
    return lancer(d, VERSER, ".")

def reconstruire(d):
    """Le maître comblé est enregistré, puis effacé, puis reconstruit par --premier-remplissage."""
    combler_puis_verser(d)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "-c", "user.email=e@e", "-c", "user.name=e", "commit", "-qm", "e"], check=True)
    os.remove(os.path.join(d, "donnees", "cours_maitre.csv"))
    return lancer(d, VERSER, ".", "--premier-remplissage")

d = copie()
c, sortie = soir_a_huit_colonnes(d)
epreuve("E41 fichier du soir à huit colonnes : code, motif", (1, True), (c, "en-tête inattendu" in sortie))
d = copie()
c, sortie = reconstruire(d)
epreuve("E42 reconstruction qui perdrait les 406 d'Euronext : code, motif, maître absent",
        (1, True, False), (c, "LA RECONSTRUCTION PERDRAIT" in sortie,
                           os.path.exists(os.path.join(d, "donnees", "cours_maitre.csv"))))
for options in (["--increment=x.csv"], ["x.csv"], ["--increment", "a.csv", "--increment", "b.csv"]):
    d = copie()
    c, _ = lancer(d, VERSER, ".", *options)
    epreuve(f"E43 ligne de commande {' '.join(options)} : code", 2, c)

# S21 à S23 — chaque correction retirée, le contournement rouvre.
d = copie()
remplacer(d, VERSER, "    admis = [COURS_MAITRE] if par_increment else [COURS_NOUVEAUX]\n",
          "    admis = [COURS_MAITRE] if par_increment else [COURS_NOUVEAUX, COURS_MAITRE]\n")
c, _ = soir_a_huit_colonnes(d)
epreuve("S21 soir à huit colonnes admis : la ligne ×100 entre (code 0)", 0, c)
d = copie()
remplacer(d, VERSER, "        if perdues:\n            ex = sorted(perdues)[:3]\n            print(f\"  ❌ ARRÊT : LA RECONSTRUCTION",
          "        if False:\n            ex = sorted(perdues)[:3]\n            print(f\"  ❌ ARRÊT : LA RECONSTRUCTION")
c, _ = reconstruire(d)
epreuve("S22 reconstruction sans garde : les 406 disparaissent (code 0)", (0, None), (c, sources(d).get("euronext")))
d = copie()
remplacer(d, VERSER, "    if inconnus or sys.argv.count(\"--increment\") > 1:\n", "    if False:\n")
c, _ = lancer(d, VERSER, ".", "--increment=x.csv")
epreuve("S23 options non vérifiées : --increment=x.csv passe (code 0)", 0, c)

# E23 — LA SÉANCE DU JOUR AVANT LA CLÔTURE, jugée à 09 h puis à 19 h (appel direct).
sys.path.insert(0, os.path.join(RACINE, "programmes"))
import TENIR_L_HISTORIQUE as _T
_auj = datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d")
_jour = datetime.now(ZoneInfo("Europe/Paris")).weekday()
_ligne = dict(valeur="ACCOR", date=_auj, open="45.1", high="45.2", low="45.0", close="45.1", volume="1200", source="abc")
_m9, _ = _T.juger_la_ligne(_ligne, "abc", _auj, {"ACCOR"}, "2024-01-02", {}, False, heure=9)
_m19, _ = _T.juger_la_ligne(_ligne, "abc", _auj, {"ACCOR"}, "2024-01-02", {}, False, heure=19)
if _jour < 5:
    epreuve("E23 séance du jour : refusée à 9 h, admise à 19 h", (True, []),
            (any("avant la clôture" in m for m in _m9), _m19))

# S8 à S11 — chaque juge retiré, la ligne fautive repasse (code 0).
SABOTAGES_DE_LIGNE = [
    ("S8 juge des cours retiré", VERSER, "    verdict, motif = controler_une_seance(seance)\n",
     "    verdict, motif = \"OK\", \"\"\n", "ACCOR,2026-07-14,48.5,48.03,48.99,48.5,487319,euronext"),
    # S9 recalé le 29-10-2026 : la protection du jour sans séance est la relecture par le lecteur commun.
    ("S9 relecture par le lecteur commun retirée", VERSER, '''        return L.lignes_mises_a_part(c), c, ""\n''', '''        return 0, c, ""\n''',
     "ACCOR,2026-09-20,48.5,48.99,48.03,48.03,487319", "soir"),
    ("S13 raccord au maître retiré", VERSER, "                    if n and not RAPPORT_VOISIN[0] <= float(r[champ]) / n <= RAPPORT_VOISIN[1]:\n",
     "                    if False:\n", "ACCOR,2026-07-14,4850,4899,4803,4803,487319,euronext"),
    ("S15 compte des champs retiré", VERSER, "    if None in r or any(v is None for v in r.values()):\n",
     "    if False:\n", "ACCOR,2026-07-14,48.5,48.99,48.03,48.03,487319,euronext,EXTRA"),
    ("S16 période des sources retirée", VERSER, "        if (debut and date < debut) or (fin and date > fin):\n",
     "        if False:\n", "ACCOR,2026-07-14,48.5,48.99,48.03,48.03,487319,abc"),
    ("S17 raccord du volume retiré", VERSER, "            if med and not RAPPORT_VOLUME[0] <= float(r[\"volume\"]) / med <= RAPPORT_VOLUME[1]:\n",
     "            if False:\n", "ACCOR,2026-07-14,48.5,48.99,48.03,48.03,487319000000,euronext"),
    ("S18 passé de la valeur retiré", VERSER, "        if not debut or date < debut:\n", "        if False:\n",
     "ARCELORMITTAL,2026-07-15,60.12,61.38,58.92,60.74,2554843,euronext"),
    ("S19 graphie retirée", VERSER, "        if nom not in voisinage.get(\"graphies\", ()):\n", "        if False:\n",
     "Accor,2026-07-14,48.5,48.99,48.03,48.03,487319,euronext"),
    ("S24 case source avec repli par la date", VERSER, '            src = r.get("source") or ""\n',
     '            src = source_de(r, "google")\n', "ACCOR,2026-07-14,48.5,48.99,48.03,48.03,487319,"),
    ("S24b case source nettoyée de ses espaces", VERSER, '            src = r.get("source") or ""\n',
     '            src = (r.get("source") or "").strip()\n', "ACCOR,2026-07-14,48.5,48.99,48.03,48.03,487319, euronext"),
    ("S12 relecture stricte retirée", VERSER, "        if texte and not forme.fullmatch(texte):\n", "        if False:\n",
     "ACCOR,2026-07-14,48.5,48.99,48.03,48.03,+487319", "soir"),
]
for nom, fichier, avant_, apres_, ligne, *mode in SABOTAGES_DE_LIGNE:
    d = copie()
    remplacer(d, fichier, avant_, apres_)
    c, _, _ = (verser_le_soir if mode else verser_une_ligne)(d, ligne)
    epreuve(f"{nom} : la ligne fautive repasse (code 0)", 0, c)

# S10 et S14 RECALÉS LE 30-10-2026 (relecteur et superviseur R-759, B2, verdict DE FOND), comme S7 : le lecteur commun
# refuse lui aussi la valeur inconnue et l'année 1900. Retirer le seul refus de `juger_la_ligne` ne fait plus passer la
# ligne. Chaque sabotage retire donc LES DEUX juges (la ligne doit repasser, code 0) ; et une épreuve ne retire que
# le premier (la ligne doit être mise à part par le lecteur, code 3, avec son motif).
for nom, avant_, apres_, ligne, quoi in (
        ("S10 valeur connue", "    if cle_valeur(nom) not in connues:\n", "    if False:\n",
         "TOTO_INCONNUE,2026-07-14,50,51,49,50.5,1000",
         "MISE À PART : TOTO_INCONNUE · séance du 14-07-2026 · le lecteur commun la met à part — valeur absente du référentiel"),
        ("S14 première séance", "    elif premiere and date < premiere:\n", "    elif False:\n",
         "ACCOR,1900-01-01,48.5,48.99,48.03,48.03,487319",
         "MISE À PART : ACCOR · séance du 01-01-1900 · le lecteur commun la met à part — date hors du calendrier officiel")):
    d = copie()
    remplacer(d, VERSER, avant_, apres_)
    remplacer(d, VERSER, *LECTEUR_MUET)
    c, _, _ = verser_le_soir(d, ligne)
    epreuve(f"{nom} et lecteur retirés : la ligne fautive repasse (code 0)", 0, c)
    d = copie()
    remplacer(d, VERSER, avant_, apres_)
    c, s_, _ = verser_le_soir(d, ligne)
    epreuve(f"{nom[:3]}b {nom[4:]} seule retirée : mise à part par le lecteur (code 3, motif)", (3, True), (c, quoi in s_))

# E16b et S11 — LE TEST « PRIX STRICTEMENT POSITIF » DU JUGE DES COURS, appelé
# directement : par le versement, un prix négatif est déjà refusé par son écriture,
# et un prix nul par le raccord aux voisines ; le juge des cours sert aussi la collecte du soir.
_appel = ("import sys; sys.path.insert(0, 'programmes'); from CONTROLER_LES_COURS import controler_une_seance as j; "
          "print(j(dict(valeur='ACCOR', date='2026-07-14', open='0', high='0', low='0', close='0', volume='1'))[0])")
d = copie()
c, sortie = lancer(d, "-c", _appel)
epreuve("E16b juge des cours, prix nuls : BLOQUANT", "BLOQUANT", sortie.strip())
remplacer(d, "programmes/CONTROLER_LES_COURS.py", "    if b <= 0:\n", "    if False:\n")
c, sortie = lancer(d, "-c", _appel)
epreuve("S11 prix positif retiré : les prix nuls repassent", True, sortie.strip() != "BLOQUANT")

print(f"\n  {sum(resultats)}/{len(resultats)} épreuves conformes")
sys.exit(0 if all(resultats) else 1)
