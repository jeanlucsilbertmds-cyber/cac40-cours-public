#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DES_ARCHIVES_BNAINS — Dim 04-10-2026 (Paris)
Rôle : prouver que programmes/LIRE_LES_ARCHIVES_BNAINS.py lit juste les archives de bnains.org, refuse ce qui
est faux, et que chaque épreuve a des dents.
Quand l'appeler : avant toute livraison qui touche programmes/LIRE_LES_ARCHIVES_BNAINS.py (R-731).

À QUOI ÇA SERT. Le lecteur fabrique la seconde source qui répare et contrôle l'historique long (A-539). Une erreur
de lecture ne se voit pas : « 19,00 » lu 19 ou 1900, un code attribué à la mauvaise valeur, deux versions d'une
même séance dont on garde la mauvaise. Ces épreuves travaillent HORS LIGNE, sur de petites archives faites de VRAIES
lignes de bnains (tests/temoins_bnains/, provenance dans son LISEZ_MOI.md) et sur le VRAI référentiel du dépôt.

LES ÉPREUVES :
B1  lecture des témoins : AXA du 13-03-2000 lu 125.20 en clôture, une seule fois (doublon identique compté) ;
B2  virgule décimale : EADS du 10-07-2000 « 19,00 » → 19.00, rangé sous AIRBUS (code SICOVAM 5730 par la table) ;
B3  séance sans échange (« -1.00 », Eurofins 13 et 14-03-2000) : non gardée, comptée mal formée (2) ; la vraie
    ligne 53477 du 15-03-2001, dont le libellé porte un octet 0x1C, est lue ENTIÈRE (8 champs) et non comptée ;
B4  conflit réel : Hermès du 21-10-2004, deux versions différentes → aucune gardée, les deux au fichier des conflits ;
B5  archives imbriquées (2004, 2009) lues ; les deux fichiers « infos.txt » comptés, jamais lus ;
B6  Suez (témoin d'Engie) gardé ; FINAXA et les droits d'AXA (codes non voulus) non gardés ;
B7  codes : l'ancien ISIN de Dassault Systèmes est LU dans la colonne source_isin du référentiel ; l'ancien ISIN
    d'Eurofins vient de ANCIENS_ISIN ; AXA reçoit son ISIN et ses codes SICOVAM sans zéro de tête ;
B8  un code qui désignerait deux valeurs → code 2, rien n'est écrit ;
B9  une archive manquante → code 1, rien n'est écrit, l'archive est nommée ;
B10 une archive corrompue → code 2 ;
B11 référentiel absent, ou sans la colonne source_isin → code 2 ;
B12 ligne de commande : sans argument → 2 ; erreur imprévue → 2 ; lecture réussie → 0 et trois fichiers aux
    en-têtes attendus ;
B13 nombre() : « 1.234,5 » refusé, « -1.00 » refusé, « 19,00 » → « 19.00 », « 17.08 » inchangé ;
B14 telecharger() avec un faux site : télécharge ce qui manque, ne retélécharge pas ce qui est là, nomme l'échec
    (coupure à la lecture, écriture qui échoue en cours de fichier), et une archive inachevée ne prend jamais le vrai
    nom ; --telecharger en ligne de commande l'appelle ;
B15 l'inventaire porte l'empreinte réelle de chaque archive lue et ses lignes lues et gardées ;
B18 droits de souscription : la vraie ligne « AXA DS » du 11-11-2009, dont le libellé est celui de la ligne AXA gardée
    le même jour suivi de « DS », donne le droit d'AXA, premier jour 11-11-2009, clôture 0,413 ; la vraie ligne « SAFT GROUPE DS » du
    même jour, d'une société hors du référentiel, n'en donne aucun ;
B17 une archive incomplète : avec le vrai seuil (3 jours ouvrés), les témoins, qui sautent du 14-03 au 10-07-2000,
    sont refusés (code 1), rien n'est écrit ; les autres épreuves relâchent ce seuil, faute de quoi aucune ne
    passerait ;
B16 deux défauts FABRIQUÉS, absents des vraies archives (mesuré le 04-10-2026) : une table de conversion dont un code
    SICOVAM n'est pas un nombre → code 2 ; la vraie ligne AXA du 11-11-2009 coupée à quatre champs → comptée mal
    formée, non gardée ; la vraie ligne « AXA DS » du même jour, dont la clôture est remplacée par « abc », est comptée
    mal formée et ne donne aucun droit.
B19 droits au libellé différent de celui de l'action (relecture de Cowork du 07-10-2026) : les vraies lignes
    « SOCIETE GENERALE » et « SOCIETE GENER DS » du 09-10-2009 donnent le droit de Société Générale ; la vraie ligne
    « CARREFOUR PROP DS » (19-12-2008) n'est pas rattachée à « CARREFOUR » ; une ligne FABRIQUÉE « C DS », dont le
    début de libellé est commun à Carrefour et à Crédit Agricole, n'est rattachée à aucune des deux.
Z0 charge le VRAI fichier du programme (la certification ne crédite que ce qui s'exécute dans programmes/) ; les
sabotages se jouent sur des copies.
LES SABOTAGES (avec --saboter) : S1 virgule non convertie · S2 négatif accepté · S3 doublons différents gardés ·
S4 fichiers non-séance lus · S5 code partagé accepté · S6 archive manquante tolérée · S7 anciens ISIN du référentiel
ignorés · S8 nom provisoire non employé au téléchargement · S9 zéros de tête des codes SICOVAM gardés ·
S10 lignes coupées par `splitlines` · S11 lacune tolérée · S12 droits de souscription ignorés · S13 libellé
exact exigé (la règle du 04-10-2026) · S14 début de libellé commun à deux valeurs accepté.

USAGE : python3 tests/EPREUVES_DES_ARCHIVES_BNAINS_Dim_04-10-2026.py <racine du dépôt> [--saboter | --saboter=S1,S2…]
CODE : 0 si tout est vert et, avec --saboter, si chaque sabotage fait rougir au moins une épreuve ; 1 sinon ; 2 si
un sabotage ne s'applique plus (son texte cible a disparu du programme).
"""
import contextlib, csv, glob, hashlib, importlib.util, io, os, shutil, subprocess, sys, tempfile, urllib.error

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
RACINE = os.path.abspath(_args[0] if _args else ".")
PROG = os.path.join(RACINE, "programmes", "LIRE_LES_ARCHIVES_BNAINS.py")
CONTRATS = os.path.join(RACINE, "programmes", "CONTRATS_DES_FICHIERS.py")
TEMOINS = os.path.join(RACINE, "tests", "temoins_bnains")
REFERENTIEL = glob.glob(os.path.join(RACINE, "donnees", "REFERENTIEL_VALEURS_*.csv"))[0]
ARCHIVES_TEMOINS = ["cours/france/2000.ZIP", "cours/france/2004.ZIP", "cours/france/2009.ZIP", "conv_isin.zip"]

SABOTAGES = {
    "S1": ('t = t.replace(",", ".")', "pass"),
    "S2": ("if float(t) < 0:", "if False:"),
    "S3": ("if len({v[2] for v in versions}) > 1:", "if False:"),
    "S4": ("            fichiers_du_jour.ignores += 1", "            yield '0000-00-00', z.read(n)"),
    "S5": ("if codes.get(c, v) != v:", "if False:"),
    "S6": ("    if manquantes:\n", "    if False:\n"),
    "S7": ('re.findall(r"remplace ([A-Z]{2}[0-9A-Z]{10})", r["source_isin"])', "[]"),
    "S8": ('open(cible + ".partiel", "wb").write(octets)\n            os.replace(cible + ".partiel", cible)',
           'open(cible, "wb").write(octets)'),
    "S9": ('add(str(int(r["SICOVAM"])))', 'add(r["SICOVAM"].strip())'),
    "S11": ("    if trous:\n", "    if False:\n"),
    "S12": ('droit = re.fullmatch(r"(.+?)\\s+(DS|DPS)", p[1].strip())', "droit = None"),
    "S13": ("if lib.startswith(prefixe)}", "if lib == prefixe}"),
    "S14": ("if len(valeurs) == 1:", "if valeurs:"),
    "S10": ('contenu.decode("latin-1").split("\\n")', 'contenu.decode("latin-1").splitlines()'),
}


def charger(source=None):
    """Charge le vrai programme, ou une copie sabotée posée à côté d'une copie des contrats."""
    if source is None:
        chemin = PROG
    else:
        d = tempfile.mkdtemp()
        shutil.copy(CONTRATS, d)
        chemin = os.path.join(d, "LIRE_LES_ARCHIVES_BNAINS.py")
        open(chemin, "w", encoding="utf-8").write(source)
    sp = importlib.util.spec_from_file_location("lecteur_bnains_eprouve", chemin)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    m.ARCHIVES = list(ARCHIVES_TEMOINS)
    m.LACUNE = 10 ** 6      # les témoins sautent des mois entiers ; B17 remet le vrai seuil
    return m


def racine_d_essai(referentiel=REFERENTIEL):
    """Une racine jetable : donnees/ avec le référentiel, et un dossier d'archives copié des témoins."""
    r = tempfile.mkdtemp()
    os.makedirs(os.path.join(r, "donnees"))
    if referentiel:
        shutil.copy(referentiel, os.path.join(r, "donnees", os.path.basename(referentiel)))
    arch = os.path.join(r, "archives_bnains")
    shutil.copytree(TEMOINS, arch)
    return r, arch


def lancer(m, *argv):
    sortie = io.StringIO()
    with contextlib.redirect_stdout(sortie):
        code = m.main(list(argv))
    return code, sortie.getvalue()


def lignes(chemin):
    return list(csv.reader(open(chemin, encoding="utf-8", newline="")))


class FauxSite:
    """Remplace urllib.request.urlopen : sert des octets connus, échoue sur commande, ou coupe en route."""

    def __init__(self, contenus, coupe=()):
        self.contenus, self.coupe, self.demandes = contenus, set(coupe), []

    def __call__(self, req, timeout=None):
        url = req.full_url
        self.demandes.append(url)
        nom = url.rsplit("/", 1)[1]
        if nom not in self.contenus:
            raise urllib.error.HTTPError(url, 404, "absent", {}, None)
        faux = self

        class Reponse:
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                if nom in faux.coupe:
                    raise ConnectionResetError("coupé en route")
                return faux.contenus[nom]
        return Reponse()


def epreuves(m):
    res = {}
    # B1 à B6, B12, B15 : une lecture réussie des témoins
    try:
        r, arch = racine_d_essai()
        code, out = lancer(m, r, arch)
        extrait = lignes(os.path.join(r, "donnees", "sources_bnains", "bnains_cac40.csv"))
        conflits = lignes(os.path.join(r, "donnees", "sources_bnains", "CONFLITS_BNAINS.csv"))
        inventaire = lignes(os.path.join(r, "donnees", "sources_bnains", "ARCHIVES_BNAINS.csv"))
        par = {(l[0], l[1]): l for l in extrait[1:]}
        axa = [l for l in extrait[1:] if l[0] == "AXA" and l[1] == "2000-03-13"]
        res["B1"] = code == 0 and len(axa) == 1 and axa[0][7] == "125.20" and "doublons identiques 1" in out
        res["B2"] = par.get(("AIRBUS", "2000-07-10"), [""] * 9)[4:8] == ["19.00", "19.19", "17.50", "17.50"] \
            and par[("AIRBUS", "2000-07-10")][2] == "5730" and par[("AXA", "2001-03-15")][7] == "124.50"
        res["B3"] = ("EUROFINS SCIENTIFIC", "2000-03-13") not in par and "mal formées 2" in out
        res["B4"] = ("HERMES INTL", "2004-10-21") not in par and len(conflits) == 3 \
            and {l[2] for l in conflits[1:]} == {"5229", "FR0000052292"} and ("AXA", "2004-10-21") in par
        res["B5"] = ("AXA", "2009-11-11") in par and "fichiers non lus 2" in out
        droits = lignes(os.path.join(r, "donnees", "sources_bnains", "DROITS_BNAINS.csv"))
        res["B18"] = droits == [m.DROITS_BNAINS, ["AXA", "FR0010821561", "AXA DS", "2009-11-11", "2009-11-11", "1", "0.413"]]
        res["B6"] = ("SUEZ", "2000-03-13") in par and not any(l[3] in ("FINAXA", "AXA DS") for l in extrait[1:])
        res["B12"] = extrait[0] == m.COURS_BNAINS and conflits[0] == m.COURS_BNAINS \
            and inventaire[0] == ["archive", "octets", "sha256", "lignes_lues", "lignes_gardees"]
        vraie = hashlib.sha256(open(os.path.join(arch, "2000.ZIP"), "rb").read()).hexdigest()
        res["B15"] = inventaire[1][:3] == ["2000.ZIP", str(os.path.getsize(os.path.join(arch, "2000.ZIP"))), vraie] \
            and inventaire[1][3:] == ["11", "7"] and len(inventaire) == 4
    except Exception:
        for k in ("B1", "B2", "B3", "B4", "B5", "B6", "B12", "B15", "B18"):
            res[k] = False
    # B7 : les codes, sur le vrai référentiel
    try:
        r, arch = racine_d_essai()
        codes = m.codes_des_valeurs(r, m.lire_conversion(os.path.join(arch, "conv_isin.zip")))
        res["B7"] = codes.get("FR0000130650") == "DASSAULT SYSTEMES" and codes.get("FR0000038259") == "EUROFINS SCIENTIFIC" \
            and codes.get("3825") == "EUROFINS SCIENTIFIC" and codes.get("12062") == "AXA" \
            and codes.get("FR0000120628") == "AXA" and "012062" not in codes and codes.get("12052") == "SUEZ"
    except Exception:
        res["B7"] = False
    # B8 : un code partagé
    try:
        r, arch = racine_d_essai()
        ref = glob.glob(os.path.join(r, "donnees", "REFERENTIEL_VALEURS_*.csv"))[0]
        texte = open(ref, encoding="utf-8-sig").read().replace(",FR0000120404,", ",FR0000120628,", 1)
        open(ref, "w", encoding="utf-8-sig").write(texte)
        code, out = lancer(m, r, arch)
        res["B8"] = code == 2 and "deux valeurs" in out and not os.path.exists(os.path.join(r, "donnees", "sources_bnains"))
    except Exception:
        res["B8"] = False
    # B9 : une archive manquante
    try:
        r, arch = racine_d_essai()
        os.remove(os.path.join(arch, "2004.ZIP"))
        code, out = lancer(m, r, arch)
        res["B9"] = code == 1 and "cours/france/2004.ZIP" in out and not os.path.exists(os.path.join(r, "donnees", "sources_bnains"))
    except Exception:
        res["B9"] = False
    # B10 : une archive corrompue
    try:
        r, arch = racine_d_essai()
        open(os.path.join(arch, "2009.ZIP"), "wb").write(b"PK pas une archive")
        code, out = lancer(m, r, arch)
        res["B10"] = code == 2 and "BadZipFile" in out
    except Exception:
        res["B10"] = False
    # B11 : référentiel absent, ou sans source_isin
    try:
        r, arch = racine_d_essai(referentiel=None)
        code1, _ = lancer(m, r, arch)
        r, arch = racine_d_essai()
        ref = glob.glob(os.path.join(r, "donnees", "REFERENTIEL_VALEURS_*.csv"))[0]
        rows = list(csv.DictReader(open(ref, encoding="utf-8-sig")))
        with open(ref, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=[c for c in rows[0] if c != "source_isin"], extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
        code2, out2 = lancer(m, r, arch)
        res["B11"] = code1 == 2 and code2 == 2 and "source_isin" in out2
    except Exception:
        res["B11"] = False
    # B12 (suite) : la ligne de commande, et l'erreur imprévue
    try:
        prog = getattr(m, "__file__", PROG)
        sans = subprocess.run([sys.executable, "-B", prog], capture_output=True, timeout=120).returncode
        r, arch = racine_d_essai()
        imprevue = subprocess.run([sys.executable, "-B", prog, r, os.path.join(arch, "LISEZ_MOI.md"), "--telecharger"],
                                  capture_output=True, timeout=120)
        res["B12"] = res["B12"] and sans == 2 and imprevue.returncode == 2 and "imprévue" in imprevue.stdout.decode("utf-8")
    except Exception:
        res["B12"] = False
    # B13 : nombre()
    try:
        refus = 0
        for t in ("1.234,5", "-1.00", "abc"):
            try:
                m.nombre(t)
            except ValueError:
                refus += 1
        res["B13"] = refus == 3 and m.nombre("19,00") == "19.00" and m.nombre(" 17.08 ") == "17.08"
    except Exception:
        res["B13"] = False
    # B14 : telecharger()
    try:
        d = tempfile.mkdtemp()
        open(os.path.join(d, "2000.ZIP"), "wb").write(b"deja la")
        # conv_isin.zip : le site rend du texte et non des octets — l'écriture échoue EN COURS de fichier
        faux = FauxSite({"2004.ZIP": b"octets 2004", "2009.ZIP": b"octets 2009", "conv_isin.zip": "du texte"},
                        coupe={"2009.ZIP"})
        with contextlib.redirect_stdout(io.StringIO()):
            echecs = m.telecharger(d, ouvrir=faux)
        noms = sorted(os.listdir(d))
        ok = (open(os.path.join(d, "2000.ZIP"), "rb").read() == b"deja la"
              and open(os.path.join(d, "2004.ZIP"), "rb").read() == b"octets 2004"
              and "2009.ZIP" not in noms and "conv_isin.zip" not in noms
              and not any(u.endswith("/2000.ZIP") for u in faux.demandes)
              and len(echecs) == 2 and any("2009.ZIP" in e and "coupé" in e for e in echecs)
              and any("conv_isin.zip" in e and "TypeError" in e for e in echecs)
              and faux.demandes[0] == m.ADRESSE + "cours/france/2004.ZIP")
        r, arch = racine_d_essai()
        vrai = m.telecharger
        m.telecharger = lambda dossier: ["faux échec"]
        try:
            code, out = lancer(m, r, arch, "--telecharger")
        finally:
            m.telecharger = vrai
        res["B14"] = ok and code == 0 and "ÉCHEC du téléchargement — faux échec" in out
    except Exception:
        res["B14"] = False
    # B17 : le vrai seuil de lacune sur les témoins, qui sautent de mars à juillet 2000
    try:
        vrai = 3
        m.LACUNE, garde = vrai, m.LACUNE
        try:
            r, arch = racine_d_essai()
            code, out = lancer(m, r, arch)
        finally:
            m.LACUNE = garde
        res["B17"] = code == 1 and "du 2000-03-14 au 2000-07-10" in out and "incomplète" in out \
            and not os.path.exists(os.path.join(r, "donnees", "sources_bnains"))
    except Exception:
        res["B17"] = False
    # B16 : deux défauts fabriqués
    try:
        r, arch = racine_d_essai()
        open(os.path.join(arch, "conv_isin.zip"), "wb").write(zip_de([("conv_isin.csv", b"SICOVAM;ISIN\r\nabc;FR0000120628\r\n")]))
        code1, out1 = lancer(m, r, arch)
        r, arch = racine_d_essai()
        open(os.path.join(arch, "2009.ZIP"), "wb").write(
            zip_de([("200911.ZIP", zip_de([("20091111.txt", b"FR0000120628\tAXA\t16.94\t17.15\r\n"
                                               b"FR0010821561\tAXA DS\t0.435\t0.445\t0.403\tabc\t83642101\r\n")]))]))
        code2, out2 = lancer(m, r, arch)
        extrait = lignes(os.path.join(r, "donnees", "sources_bnains", "bnains_cac40.csv"))
        res["B16"] = code1 == 2 and "ligne 2 illisible" in out1 and code2 == 0 and "mal formées 4" in out2 \
            and lignes(os.path.join(r, "donnees", "sources_bnains", "DROITS_BNAINS.csv")) == [m.DROITS_BNAINS] \
            and not any(l[1] == "2009-11-11" for l in extrait[1:])
    except Exception:
        res["B16"] = False
    # B19 : droits dont le libellé n'est pas celui de l'action — vraies lignes, réunies dans une séance d'essai
    try:
        r, arch = racine_d_essai()
        vraies = (b"FR0000130809\tSOCIETE GENERALE\t47.600\t48.450\t47.080\t47.490\t6766522\r\n"      # 09-10-2009
                  b"FR0010811950\tSOCIETE GENER DS\t2.600\t2.810\t2.490\t2.500\t13470739\r\n"         # 09-10-2009
                  b"FR0000120172\tCARREFOUR\t26.600\t27.700\t26.600\t27.340\t4282609\r\n"            # 19-12-2008
                  b"FR0010693192\tCARREFOUR PROP DS\t0.010\t0.010\t0.010\t0.010\t11197\r\n"          # 19-12-2008
                  b"FR0000045072\tCREDIT AGRICOLE SA\t13.780\t14.270\t13.540\t14.010\t22992887\r\n"  # 09-06-2008
                  b"FR0099999999\tC DS\t1.000\t1.000\t1.000\t1.000\t100\r\n")                       # FABRIQUÉE
        open(os.path.join(arch, "2009.ZIP"), "wb").write(zip_de([("200910.ZIP", zip_de([("20091009.txt", vraies)]))]))
        code, out = lancer(m, r, arch)
        droits = lignes(os.path.join(r, "donnees", "sources_bnains", "DROITS_BNAINS.csv"))
        res["B19"] = code == 0 and droits == [m.DROITS_BNAINS, ["SOCIETE GENERALE", "FR0010811950", "SOCIETE GENER DS",
                                                                "2009-10-09", "2009-10-09", "1", "2.500"]]
    except Exception:
        res["B19"] = False
    return res


def zip_de(fichiers):
    """Une archive en mémoire faite des (nom, octets) donnés."""
    import zipfile
    tampon = io.BytesIO()
    with zipfile.ZipFile(tampon, "w") as z:
        for nom, octets in fichiers:
            z.writestr(nom, octets)
    return tampon.getvalue()


def main():
    source = open(PROG, encoding="utf-8").read()
    res = epreuves(charger())
    rouges = [k for k, v in res.items() if not v]
    print(f"Z0 programme tel quel : {len(res) - len(rouges)}/{len(res)} épreuves vertes" + (f" · ROUGES {rouges}" if rouges else ""))
    code = 1 if rouges else 0
    choix = [a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--saboter=")]
    if "--saboter" in sys.argv or choix:
        for k, (cible, remplace) in SABOTAGES.items():
            if choix and k not in choix[0]:
                continue
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
    # Tous les dossiers d'essai vont sous UN dossier, effacé à la fin : mesuré le 07-10-2026, les
    # passages successifs avaient laissé 2 460 dossiers dans /tmp et rempli le disque.
    _DOSSIER_D_ESSAI = tempfile.mkdtemp(prefix="epreuves_")
    tempfile.tempdir = os.environ["TMPDIR"] = _DOSSIER_D_ESSAI
    try:
        sys.exit(main())
    finally:
        shutil.rmtree(_DOSSIER_D_ESSAI, ignore_errors=True)
