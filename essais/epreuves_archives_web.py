#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVES — archives_web.py et telecharger_consensus_archive.py, hors ligne.

Usage : python3 essais/epreuves_archives_web.py <dossier des pages témoins> [--saboter]
Les pages témoins sont les vraies copies relevées par l'essai du 10-10-2026 à 14h14
(dépôt privé, temoins/archives_web/). Code 0 si tout est vert et, avec --saboter, si chaque sabotage
fait rougir au moins une épreuve ; 1 sinon ; 2 si un sabotage ne s'applique plus.
"""
import contextlib, csv, gzip, importlib.util, io, os, sys, tempfile, urllib.error

ICI = os.path.dirname(os.path.abspath(__file__))
SABOTER = "--saboter" in sys.argv
TEMOINS = [a for a in sys.argv[1:] if not a.startswith("--")][0]
P2019 = open(os.path.join(TEMOINS, "liste_Boursorama_page_1_20190322073831.html"), encoding="utf-8").read()
P2026 = open(os.path.join(TEMOINS, "liste_Boursorama_page_1_20260218095336.html"), encoding="utf-8").read()

SABOTAGES = {
    "aw": {
        "K1": ('if b[:2] == b"\\x1f\\x8b":', "if False:"),
        "K2": ("if e.code not in (429, 503):", "if True:"),
        "K3": ('if not lignes or lignes[0] != ["timestamp", "statuscode", "digest"]:', "if False:"),
        "K4": ("if not (len(horodatage) == 14 and horodatage.isdigit()):", "if False:"),
        "K5": ('if code == "200"]', 'if True]'),
    },
    "tc": {
        "K6": ("if heads[:6] != ENTETES:", "if False:"),
        "K7": ("if (num, ts) in deja:", "if False:"),
        "K8": ('x = x.replace(",", "") if x.rfind(".") > x.rfind(",") else x.replace(".", "").replace(",", ".")', "pass"),
        "K9": ('if r["sort"] != "échec réseau"}', 'if True}'),
        "K10": ("if len(garde) != len(lignes):", "if False:"),
        "K11": ("if abs(recalc - float(l[\"potentiel_pct\"])) > 0.2:", "if False:"),
    },
}


def charger(nom, source, aw=None):
    d = tempfile.mkdtemp()
    p = os.path.join(d, nom + ".py")
    open(p, "w", encoding="utf-8").write(source)
    if aw is not None:
        sys.modules["archives_web"] = aw
    sp = importlib.util.spec_from_file_location(nom, p)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


class Reponse(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False


def ouvreur(suite):
    """suite : liste d'octets ou de codes d'erreur, rendus dans l'ordre. Compte les appels."""
    etat = {"n": 0}
    def ouvrir(req, timeout=0):
        x = suite[min(etat["n"], len(suite) - 1)]
        etat["n"] += 1
        if isinstance(x, int):
            raise urllib.error.HTTPError(req.full_url, x, "x", {}, None)
        return Reponse(x)
    return ouvrir, etat


def epreuves(aw, tc):
    r = {}
    def essai(nom, f):
        try:
            r[nom] = bool(f())
        except Exception:
            r[nom] = False
    def e1():
        maj, L = tc.lire_liste(P2019)
        a = L[0]
        return len(L) == 19 and (a["valeur"], a["recommandation"], a["objectif"], a["nb_analystes"]) == ("ACCOR", "Renforcer", "45.906", "18") and maj == "21.03.19"
    def e2():
        maj, L = tc.lire_liste(P2026)
        a = L[0]
        return len(L) == 23 and (a["valeur"], a["recommandation"], a["objectif"], a["nb_analystes"]) == ("ACCOR", "Acheter", "55.441", "19") and maj == "17.02.26"
    def leve(f, exc):
        try:
            f()
            return False
        except exc:
            return True
    essai("E1 vraie copie 2019", e1)
    essai("E2 vraie copie 2026", e2)
    essai("E3 bloc absent → refus", lambda: leve(lambda: tc.lire_liste("<html>rien</html>"), ValueError))
    essai("E4 en-tête renommé → refus", lambda: leve(lambda: tc.lire_liste(P2026.replace("Obj. Cours**", "Objectif**", 1)), ValueError))
    def e5():
        o, _ = ouvreur([gzip.compress("bonjour".encode())])
        return aw._demander("https://exemple.invalid/u", ouvrir=o, pause=0) == b"bonjour"
    essai("E5 copie compressée → décompressée", e5)
    def e6():
        o, st = ouvreur([503, 503, b"ok"])
        return aw._demander("https://exemple.invalid/u", ouvrir=o, pause=0) == b"ok" and st["n"] == 3
    essai("E6 refus 503 → réessai", e6)
    def e7():
        o, st = ouvreur([404, b"ok"])
        return leve(lambda: aw._demander("https://exemple.invalid/u", ouvrir=o, pause=0), aw.ErreurArchives) and st["n"] == 1
    essai("E7 404 → erreur sans réessai", e7)
    def e8():
        o, _ = ouvreur([b'[["a","b","c"],["20190322073831","200","X"]]'])
        return leve(lambda: aw.lister_copies("x", ouvrir=o, pause=0), aw.ErreurArchives)
    essai("E8 index à en-tête inattendu → erreur", e8)
    essai("E9 horodatage invalide → erreur", lambda: leve(lambda: aw.lire_copie("x", "2019", ouvrir=ouvreur([b"ok"])[0], pause=0), aw.ErreurArchives))
    def e10():
        o, _ = ouvreur([b'[["timestamp","statuscode","digest"],["20190322073831","200","A"],["20190323073831","302","B"]]'])
        return aw.lister_copies("x", ouvrir=o, pause=0) == [("20190322073831", "A")]
    essai("E10 copie non-200 écartée", e10)
    def e11():
        racine = tempfile.mkdtemp()
        tc.archives_web.lister_copies = lambda adr, **k: [("20260218095336", "E")] if adr.endswith("paris/") else []
        tc.archives_web.lire_copie = lambda adr, ts, **k: P2026
        tc.PAUSE = 0
        sys.argv = ["x", racine]
        with contextlib.redirect_stdout(io.StringIO()):
            tc.main(); tc.main()
        n = len(list(csv.DictReader(open(os.path.join(racine, "donnees", "consensus_archives_boursorama.csv"), encoding="utf-8"))))
        return n == 23
    essai("E11 relance → aucune ligne en double", e11)
    essai("E12 nombres anglais et français", lambda: [tc._nombre(x) for x in [" 1,005.000 ", "2 152,000", "+20.964%", "Atteint"]] == ["1005.000", "2152.000", "20.964", "atteint"])
    def e13():
        racine = tempfile.mkdtemp(); etat = {"n": 0}
        def lire(adr, ts, **k):
            etat["n"] += 1
            if etat["n"] == 1:
                raise tc.archives_web.ErreurArchives("code 503")
            return P2026
        tc.archives_web.lister_copies = lambda adr, **k: [("20260218095336", "E")] if adr.endswith("paris/") else []
        tc.archives_web.lire_copie = lire
        tc.PAUSE = 0
        sys.argv = ["x", racine]
        c1 = tc.main(); c2 = tc.main()
        n = len(list(csv.DictReader(open(os.path.join(racine, "donnees", "consensus_archives_boursorama.csv"), encoding="utf-8"))))
        return c1 == 1 and c2 == 0 and n == 23
    essai("E13 échec réseau → repris à la relance", e13)
    def e14():
        racine = tempfile.mkdtemp(); os.makedirs(os.path.join(racine, "donnees"))
        fl = os.path.join(racine, "donnees", "consensus_archives_boursorama.csv")
        with open(fl, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, tc.CHAMPS); w.writeheader(); w.writerow({k: "1" for k in tc.CHAMPS})
        tc._purger(fl, os.path.join(racine, "donnees", "consensus_archives_index.csv"))
        return len(list(csv.DictReader(open(fl, encoding="utf-8")))) == 0
    essai("E14 lignes orphelines retirées", e14)
    def e15():
        faux = P2026.replace("55,441", "65,441", 1)
        return faux != P2026 and leve(lambda: tc.lire_liste(faux), ValueError)
    essai("E15 objectif incohérent avec le potentiel → refus", e15)
    return r


def charger_tous(src_aw, src_tc):
    aw = charger("archives_web", src_aw)
    tc = charger("telecharger_consensus_archive", src_tc, aw)
    return aw, tc


def main():
    src = {"aw": open(os.path.join(ICI, "archives_web.py"), encoding="utf-8").read(),
           "tc": open(os.path.join(ICI, "telecharger_consensus_archive.py"), encoding="utf-8").read()}
    r = epreuves(*charger_tous(src["aw"], src["tc"]))
    rouges = [k for k, v in r.items() if not v]
    print(f"Z0 tel quel : {len(r) - len(rouges)}/{len(r)} vertes" + (f" · ROUGES {rouges}" if rouges else ""))
    code = 1 if rouges else 0
    if SABOTER:
        for fic, sabs in SABOTAGES.items():
            for k, (cible, rempl) in sabs.items():
                if src[fic].count(cible) != 1:
                    print(f"{k} NE S'APPLIQUE PLUS ({src[fic].count(cible)} occurrences)")
                    return 2
                s2 = dict(src); s2[fic] = src[fic].replace(cible, rempl)
                rr = epreuves(*charger_tous(s2["aw"], s2["tc"]))
                tomb = [e.split()[0] for e, v in rr.items() if not v]
                print(f"{k} {'mord' if tomb else 'NE MORD PAS'} : {tomb}")
                if not tomb:
                    code = 1
    return code


if __name__ == "__main__":
    sys.exit(main())
