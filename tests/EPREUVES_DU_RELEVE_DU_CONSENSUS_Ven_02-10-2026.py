#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_RELEVE_DU_CONSENSUS — Ven 02-10-2026 (Paris)
Rôle : prouver que programmes/COLLECTER_LE_CONSENSUS.py lit juste le consensus EasyBourse, refuse ce qui est faux,
et que chaque épreuve a des dents.
Quand l'appeler : avant toute livraison qui touche programmes/COLLECTER_LE_CONSENSUS.py (R-731).

À QUOI ÇA SERT. Le collecteur relève chaque soir, chez EasyBourse, le tableau du consensus des valeurs du
référentiel. Une erreur de lecture ne se voit pas : un objectif lu 2 au lieu de 2 000 reste un nombre. C'est arrivé
le 01-10-2026 sur Hermès (« 2.000,00 € »). Ces épreuves travaillent HORS LIGNE, sur deux vraies pages relevées le
02-10-2026 et rangées dans tests/temoins_consensus/ : rien ne dépend du site ni du jour où l'on lance les épreuves,
sauf E11 qui compte sur l'horloge pour « le même jour ».

LES ÉPREUVES :
E1  vraie page TotalEnergies : 24 analystes, objectif 83.21, ISIN FR0000120271, prévisions au 26/09/2026 ;
E2  vraie page Hermès : objectif actuel 1900.00 et il y a 3 mois 2000.00 (séparateur de milliers) ;
E3  ligne « Vendre » retirée → refus ;
E4  en-tête « Il y a 7 jours » renommé → refus ;
E5  cellule « Nb analystes » vidée → refus ;
E6  page sans tableau → refus ;
E7  page TotalEnergies déposée sous l'ISIN d'ACCOR → ACCOR refusée (IDENTITÉ), TotalEnergies lue, code 1 ;
E8  Hermès dont l'objectif est réécrit « 1.900 » → refus PLAUSIBILITÉ ;
E9  référentiel absent → code 2 ;
E10 fichier de sortie corrompu (le bon en-tête, puis un champ de 200 000 caractères que le lecteur CSV refuse) →
    code 2 ;
E11 deux passages le même jour → aucune ligne en double ;
E12 nombre() : « 2.000,00 € » → 2000.00 · « 86,86 » → 86.86 · « 1.96 » → 1.96 · « 24 » → 24 ;
E13 (relecture de Cowork du 03-10-2026, cassure 1) un fichier existant dont l'en-tête a deux colonnes échangées
    (objectif_m3 et nb_analystes_actuel) → code 2, et le fichier n'est pas touché ;
E14 chemin du site, curl remplacé par un faux qui sert les vraies pages : TotalEnergies trouvée à son adresse directe ;
E15 chemin du site : Hermès sans tableau à l'adresse directe, retrouvé par la recherche, qui préfère l'adresse de Paris
    (suffixe -25) à une autre ;
E16 chemin du site : rien ne vient (curl n'écrit aucun fichier) → « aucune page consensus », code 1 ;
E17 une valeur absente du fichier maître des cours : lue, et le contrôle de plausibilité non fait est DIT ;
E18 référentiel sans la colonne isin → code 2 ; sans fichier maître des cours, la lecture se fait et le dit ;
E19 la ligne de commande : sans argument → 2 ; avec --pages → le code du relevé ;
E20 une ligne inconnue ajoutée au tableau est ignorée ; une cellule de trop dans une ligne connue → refus ;
E21 le fichier maître porte, APRÈS la vraie, une séance plus ancienne au cours absurde : la plausibilité se juge sur
    la séance la plus récente, pas sur la dernière ligne lue ;
E22 un fichier existant au bon en-tête dont la dernière ligne n'a pas de saut de ligne → code 2, et le fichier n'est
    pas touché (sinon la ligne ajoutée se souderait à la dernière) ;
E23 (relecture de Cowork du 03-10-2026, deuxième tour, cas C4) une ligne existante coupée à 6 champs, finie par un saut
    de ligne → code 2, et le fichier n'est pas touché ;
E24 (cas C2) un fichier fini par « \r » seul → code 2, et le fichier n'est pas touché ;
E25 (cas C5) le fichier de sortie est un dossier, en ligne de commande → code 2 et non 1 (le 1 dit « une valeur non
    lue »).
Z0 charge le VRAI fichier programmes/COLLECTER_LE_CONSENSUS.py, et non une copie : la certification
(programmes/CERTIFIER_LA_VERSION.py) ne crédite que ce qui s'exécute dans un fichier de programmes/ ; une copie dans
un dossier jetable laissait le collecteur entier « jamais exécuté ». Les sabotages, eux, se jouent sur des copies.
LES SABOTAGES (avec --saboter) : K1 identité non contrôlée · K2 virgule décimale ignorée · K3 cellule vide lue 0 ·
K4 en-têtes non contrôlés · K5 plausibilité non contrôlée · K6 doublons acceptés · K7 grandeurs manquantes tolérées ·
K8 nombre de référentiels non contrôlé · K9 fichier corrompu non intercepté · K10 en-tête du fichier existant non
confronté · K11 recherche du site sans préférence pour Paris · K12 référentiel sans colonnes accepté · K13 cellule de
trop tolérée · K14 dernier cours pris sur la dernière ligne lue et non sur la séance la plus récente · K15 fichier
sans saut de ligne final accepté · K16 lignes existantes non comptées · K17 erreur imprévue sortie en 1.

USAGE : python3 tests/EPREUVES_DU_RELEVE_DU_CONSENSUS_Ven_02-10-2026.py <racine du dépôt> [--saboter]
CODE : 0 si toutes les épreuves sont vertes et, avec --saboter, si chaque sabotage fait rougir au moins une
épreuve ; 1 sinon ; 2 si un sabotage ne s'applique plus (son texte cible a disparu du programme).
"""
import contextlib, csv, importlib.util, io, os, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
RACINE = os.path.abspath(_args[0] if _args else ".")
PROG = os.path.join(RACINE, "programmes", "COLLECTER_LE_CONSENSUS.py")
TEMOINS = os.path.join(RACINE, "tests", "temoins_consensus")
TTE = open(os.path.join(TEMOINS, "TTE_FR0000120271_2026-10-02.html"), "rb").read().decode("latin-1")
RMS = open(os.path.join(TEMOINS, "RMS_FR0000052292_2026-10-02.html"), "rb").read().decode("latin-1")

SABOTAGES = {
    "K1": ('if d["isin_page"] != isin:', "if False:"),
    "K2": ('if "," in t:', "if False:"),
    "K3": ('raise ValueError(f"ligne « {lib} », colonne {col} : cellule vide")', 'return "0"'),
    "K4": ("if ent[-4:] != ENTETES:", "if False:"),
    "K5": ("if not 0.5 <= ratio <= 3.0:", "if False:"),
    "K6": ("if (jour, isin) in deja:", "if False:"),
    "K7": ("    if manq:", "    if False:"),
    "K8": ("if len(refs) != 1:", "if False:"),
    "K9": ("except csv.Error as e:", "except ZeroDivisionError as e:"),
    "K10": ("if entete != CHAMPS:", "if False:"),
    "K11": ('key=lambda u: (not u.endswith("-25"), u)', "key=lambda u: u"),
    "K12": ('if not valeurs or not {"nom_usuel", "mnemonique", "isin"} <= set(valeurs[0]):', "if not valeurs:"),
    "K13": ("if len(tds) != 5:", "if False:"),
    "K14": ('if x["valeur"] not in derniers or x["date"] >= derniers[x["valeur"]][0]:', "if True:"),
    "K15": ('if f.read(1) != b"\\n":', 'if f.read(1) not in (b"\\n", b"\\r"):'),
    "K16": (" if len(l) != len(CHAMPS)]", " if False]"),
    "K17": ("        code = 2\n    sys.exit(code)", "        code = 1\n    sys.exit(code)"),
}


class FauxSite:
    """Remplace curl et la pause : sert des pages connues, comme le ferait le site, et note les adresses demandées."""

    def __init__(self, pages):
        self.pages, self.demandes = pages, []

    def run(self, args, **k):
        adresse, chemin = args[-1], args[args.index("-o") + 1]
        self.demandes.append(adresse)
        for debut, texte in self.pages.items():
            if adresse.startswith(debut):
                open(chemin, "w", encoding="latin-1").write(texte)
                break

    def sleep(self, secondes):
        pass


def en_ligne(m, r, pages):
    """Lance `collecter` sur le chemin du site (sans --pages), avec un faux site. Rend (code, sortie, faux site)."""
    faux = FauxSite(pages)
    vrais = m.subprocess, m.time
    m.subprocess, m.time = faux, faux
    try:
        sortie = io.StringIO()
        with contextlib.redirect_stdout(sortie):
            code = m.collecter(r)
    finally:
        m.subprocess, m.time = vrais
    return code, sortie.getvalue(), faux


def charger(source=None):
    if source is None:
        sp = importlib.util.spec_from_file_location("collecteur_eprouve", PROG)
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        return m
    d = tempfile.mkdtemp()
    p = os.path.join(d, "COLLECTER_LE_CONSENSUS.py")
    open(p, "w", encoding="utf-8").write(source)
    sp = importlib.util.spec_from_file_location("collecteur_eprouve", p)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def racine_d_essai(valeurs, pages):
    """valeurs : [(nom, mnemonique, isin)] ; pages : {isin: texte}. Rend la racine."""
    r = tempfile.mkdtemp()
    os.makedirs(os.path.join(r, "donnees"))
    os.makedirs(os.path.join(r, "pages"))
    with open(os.path.join(r, "donnees", "REFERENTIEL_VALEURS_essai.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["nom_usuel", "mnemonique", "isin"])
        w.writerows(valeurs)
    shutil.copy(os.path.join(RACINE, "donnees", "cours_maitre.csv"), os.path.join(r, "donnees", "cours_maitre.csv"))
    for isin, s in pages.items():
        open(os.path.join(r, "pages", f"{isin}.html"), "w", encoding="latin-1").write(s)
    return r


def lancer(m, r):
    sortie = io.StringIO()
    with contextlib.redirect_stdout(sortie):
        code = m.collecter(r, os.path.join(r, "pages"))
    return code, sortie.getvalue()


def leve(m, s):
    try:
        m.lire_page(s)
        return False
    except ValueError:
        return True


def epreuves(m):
    res = {}
    try:
        d = m.lire_page(TTE)
        res["E1"] = (d["nb_analystes_actuel"], d["objectif_actuel"], d["isin_page"], d["previsions_au"]) == (
            "24", "83.21", "FR0000120271", "26/09/2026")
    except Exception:
        res["E1"] = False
    try:
        d = m.lire_page(RMS)
        res["E2"] = (d["objectif_actuel"], d["objectif_m3"]) == ("1900.00", "2000.00")
    except Exception:
        res["E2"] = False
    i = TTE.find(">Vendre<", TTE.find("Il y a 3 mois"))
    a, b = TTE.rfind("<tr", 0, i), TTE.find("</tr>", i) + 5
    res["E3"] = leve(m, TTE[:a] + TTE[b:])
    res["E4"] = leve(m, TTE.replace("Il y a 7 jours", "Il y a 8 jours", 1))
    j = TTE.find("Nb analystes", TTE.find("Il y a 3 mois"))
    k = TTE.find("<td>24</td>", j)
    res["E5"] = k > 0 and leve(m, TTE[:k] + "<td></td>" + TTE[k + 11:])
    res["E6"] = leve(m, "<html>rien</html>")
    try:
        r = racine_d_essai([("ACCOR", "AC", "FR0000120404"), ("TOTALENERGIES", "TTE", "FR0000120271")],
                           {"FR0000120404": TTE, "FR0000120271": TTE})
        code, out = lancer(m, r)
        lignes = list(csv.DictReader(open(os.path.join(r, "donnees", "consensus_easybourse.csv"), encoding="utf-8")))
        res["E7"] = code == 1 and "IDENTITÉ" in out and [x["isin"] for x in lignes] == ["FR0000120271"]
    except Exception:
        res["E7"] = False
    try:
        faux = RMS.replace("<td>1.900,00 ", "<td>1.900 ")
        r = racine_d_essai([("HERMES INTL", "RMS", "FR0000052292")], {"FR0000052292": faux})
        code, out = lancer(m, r)
        res["E8"] = code == 1 and "PLAUSIBILIT" in out
    except Exception:
        res["E8"] = False
    try:
        r = racine_d_essai([("TOTALENERGIES", "TTE", "FR0000120271")], {"FR0000120271": TTE})
        os.remove(os.path.join(r, "donnees", "REFERENTIEL_VALEURS_essai.csv"))
        res["E9"] = lancer(m, r)[0] == 2
    except Exception:
        res["E9"] = False
    try:
        r = racine_d_essai([("TOTALENERGIES", "TTE", "FR0000120271")], {"FR0000120271": TTE})
        open(os.path.join(r, "donnees", "consensus_easybourse.csv"), "w", encoding="utf-8").write(
            ",".join(m.CHAMPS) + "\n" + "x" * 200000 + "\n")
        res["E10"] = lancer(m, r)[0] == 2
    except Exception:
        res["E10"] = False
    try:
        r = racine_d_essai([("TOTALENERGIES", "TTE", "FR0000120271")], {"FR0000120271": TTE})
        lancer(m, r)
        lancer(m, r)
        n = len(list(csv.DictReader(open(os.path.join(r, "donnees", "consensus_easybourse.csv"), encoding="utf-8"))))
        res["E11"] = n == 1
    except Exception:
        res["E11"] = False
    try:
        res["E12"] = [m.nombre(v) for v in ["2.000,00 €", "86,86 ", "1.96", "24"]] == ["2000.00", "86.86", "1.96", "24"]
    except Exception:
        res["E12"] = False
    try:
        r = racine_d_essai([("TOTALENERGIES", "TTE", "FR0000120271")], {"FR0000120271": TTE})
        chemin = os.path.join(r, "donnees", "consensus_easybourse.csv")
        ent = list(m.CHAMPS)
        i, j = ent.index("objectif_m3"), ent.index("nb_analystes_actuel")
        ent[i], ent[j] = ent[j], ent[i]
        open(chemin, "w", encoding="utf-8").write(",".join(ent) + "\n")
        avant = open(chemin, encoding="utf-8").read()
        code, out = lancer(m, r)
        res["E13"] = code == 2 and "en-tête" in out and open(chemin, encoding="utf-8").read() == avant
    except Exception:
        res["E13"] = False
    try:
        r = racine_d_essai([("TOTALENERGIES", "TTE", "FR0000120271")], {})
        code, out, faux = en_ligne(m, r, {m.SITE + "/action-consensus/x/FR0000120271-25": TTE})
        res["E14"] = code == 0 and len(faux.demandes) == 1
    except Exception:
        res["E14"] = False
    try:
        r = racine_d_essai([("HERMES INTL", "RMS", "FR0000052292")], {})
        recherche = ('<a href="/action-consensus/hermes/FR0000052292-11">autre place</a>'
                     '<a href="/action-consensus/hermes/FR0000052292-25">Paris</a>')
        code, out, faux = en_ligne(m, r, {m.SITE + "/action-consensus/x/": "<html>pas de tableau</html>",
                                          m.SITE + "/recherche?q=FR0000052292": recherche,
                                          m.SITE + "/action-consensus/hermes/FR0000052292-25": RMS})
        lignes = list(csv.DictReader(open(os.path.join(r, "donnees", "consensus_easybourse.csv"), encoding="utf-8")))
        res["E15"] = code == 0 and [x["adresse"] for x in lignes] == [m.SITE + "/action-consensus/hermes/FR0000052292-25"]
    except Exception:
        res["E15"] = False
    try:
        r = racine_d_essai([("ACCOR", "AC", "FR0000120404")], {})
        code, out, faux = en_ligne(m, r, {})
        res["E16"] = code == 1 and "aucune page consensus" in out and len(faux.demandes) == 2
    except Exception:
        res["E16"] = False
    try:
        r = racine_d_essai([("NOM ABSENT DU MAITRE", "TTE", "FR0000120271")], {"FR0000120271": TTE})
        code, out = lancer(m, r)
        res["E17"] = code == 0 and "plausibilité non contrôlée" in out and "NOM ABSENT DU MAITRE" in out
    except Exception:
        res["E17"] = False
    try:
        r = racine_d_essai([("TOTALENERGIES", "TTE", "FR0000120271")], {"FR0000120271": TTE})
        ref = os.path.join(r, "donnees", "REFERENTIEL_VALEURS_essai.csv")
        open(ref, "w", encoding="utf-8").write("nom_usuel,mnemonique\nTOTALENERGIES,TTE\n")
        sans_colonne = lancer(m, r)[0] == 2
        r = racine_d_essai([("TOTALENERGIES", "TTE", "FR0000120271")], {"FR0000120271": TTE})
        os.remove(os.path.join(r, "donnees", "cours_maitre.csv"))
        code, out = lancer(m, r)
        res["E18"] = sans_colonne and code == 0 and "plausibilité non contrôlée" in out
    except Exception:
        res["E18"] = False
    try:
        r = racine_d_essai([("TOTALENERGIES", "TTE", "FR0000120271")], {"FR0000120271": TTE})
        prog = getattr(m, "__file__", PROG)
        sans = subprocess.run([sys.executable, "-B", prog], capture_output=True, timeout=120).returncode
        avec = subprocess.run([sys.executable, "-B", prog, r, "--pages", os.path.join(r, "pages")],
                              capture_output=True, timeout=120).returncode
        res["E19"] = (sans, avec) == (2, 0)
    except Exception:
        res["E19"] = False
    try:
        debut = TTE.find("<tr", TTE.find(">Vendre<", TTE.find("Il y a 3 mois")) - 400)
        inconnue = TTE[:debut] + "<tr><td>Ligne inconnue</td><td>1</td></tr>" + TTE[debut:]
        lue = m.lire_page(inconnue)["vendre_actuel"] == m.lire_page(TTE)["vendre_actuel"]
        k = TTE.find("<td>24</td>", TTE.find("Nb analystes", TTE.find("Il y a 3 mois")))
        res["E20"] = k > 0 and lue and leve(m, TTE[:k] + "<td>99</td>" + TTE[k:])
    except Exception:
        res["E20"] = False
    try:
        r = racine_d_essai([("TOTALENERGIES", "TTE", "FR0000120271")], {"FR0000120271": TTE})
        maitre = os.path.join(r, "donnees", "cours_maitre.csv")
        entete = open(maitre, encoding="utf-8").readline().strip().split(",")
        vieille = {c: "" for c in entete}
        vieille.update(date="2000-01-03", valeur="TOTALENERGIES", close="1")
        with open(maitre, "a", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, entete).writerow(vieille)
        code, out = lancer(m, r)
        res["E21"] = code == 0 and "PLAUSIBILIT" not in out
    except Exception:
        res["E21"] = False
    try:
        r = racine_d_essai([("TOTALENERGIES", "TTE", "FR0000120271")], {"FR0000120271": TTE})
        chemin = os.path.join(r, "donnees", "consensus_easybourse.csv")
        lancer(m, r)
        texte = open(chemin, encoding="utf-8", newline="").read()
        open(chemin, "w", encoding="utf-8", newline="").write(texte.rstrip("\r\n").replace("2026-", "2000-", 1))
        avant = open(chemin, encoding="utf-8", newline="").read()
        code, out = lancer(m, r)
        res["E22"] = code == 2 and "saut de ligne" in out and open(chemin, encoding="utf-8", newline="").read() == avant
    except Exception:
        res["E22"] = False
    for cas, abime in (("E23", lambda x: x + ",".join(x.splitlines()[-1].split(",")[:6]) + "\r\n"),
                       ("E24", lambda x: x[:-1])):
        try:
            r = racine_d_essai([("TOTALENERGIES", "TTE", "FR0000120271")], {"FR0000120271": TTE})
            chemin = os.path.join(r, "donnees", "consensus_easybourse.csv")
            lancer(m, r)
            texte = open(chemin, encoding="utf-8", newline="").read().replace("2026-", "2000-")
            open(chemin, "w", encoding="utf-8", newline="").write(abime(texte))
            avant = open(chemin, encoding="utf-8", newline="").read()
            code, out = lancer(m, r)
            res[cas] = code == 2 and "ARRÊT" in out and open(chemin, encoding="utf-8", newline="").read() == avant
        except Exception:
            res[cas] = False
    try:
        r = racine_d_essai([("TOTALENERGIES", "TTE", "FR0000120271")], {"FR0000120271": TTE})
        os.makedirs(os.path.join(r, "donnees", "consensus_easybourse.csv"))
        prog = getattr(m, "__file__", PROG)
        res["E25"] = subprocess.run([sys.executable, "-B", prog, r, "--pages", os.path.join(r, "pages")],
                                    capture_output=True, timeout=120).returncode == 2
    except Exception:
        res["E25"] = False
    return res


def main():
    source = open(PROG, encoding="utf-8").read()
    res = epreuves(charger())
    rouges = [k for k, v in res.items() if not v]
    print(f"Z0 programme tel quel : {len(res) - len(rouges)}/{len(res)} épreuves vertes" + (f" · ROUGES {rouges}" if rouges else ""))
    code = 1 if rouges else 0
    if "--saboter" in sys.argv:
        for k, (cible, remplace) in SABOTAGES.items():
            if source.count(cible) != 1:
                print(f"{k} NE S'APPLIQUE PLUS : texte cible trouvé {source.count(cible)} fois")
                return 2
            r = epreuves(charger(source.replace(cible, remplace)))
            tombees = [e for e, v in r.items() if not v]
            print(f"{k} {'mord' if tombees else 'NE MORD PAS'} : {tombees}")
            if not tombees:
                code = 1
    return code


if __name__ == "__main__":
    sys.exit(main())
