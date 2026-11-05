#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_L_OUTIL_QUI_FIGE_LES_AVIS — Dim 01-11-2026 (Paris). Simulation uniquement.

① RÔLE — Prouver que etudes/outils/FIGER_LE_TEXTE_DES_AVIS.py refuse une autre version de pdftotext que 24.02.0, voit
  un texte figé retouché et une empreinte de carnet écrite autrement, n'inscrit jamais deux fois le même texte au
  carnet, rend 2 sur un avis cité absent, et refuse une vieille ligne du même texte restée au carnet et une ligne dont
  le fichier lu nomme un autre avis ; et, avec --saboter, que chacune de ces gardes, retirée, fait tomber au moins un
  cas.
② CONTEXTE D'APPEL — Par la certification, chaque nuit, depuis la racine, la racine en argument, sans puis avec
  --saboter ; à la main avant toute livraison qui touche l'outil (R-731) :
  python3 tests/EPREUVES_DE_L_OUTIL_QUI_FIGE_LES_AVIS_Dim_01-11-2026.py <racine> [--saboter]
③ ENTRÉE — La racine du dépôt (lue, jamais écrite) : l'outil, le vérificateur des preuves du référentiel, le
  référentiel, le carnet, les avis PDF cités et leurs textes figés ; l'option --saboter.
④ CONDITIONS D'ENTRÉE — — (aucun pdftotext réel : l'épreuve pose un faux pdftotext en tête du chemin, voir le ⑧).
⑤ SORTIE — Le code : 0 si chaque cas rend le code et le motif attendus (et, avec --saboter, si chaque garde retirée
  fait tomber au moins un cas) ; 1 sinon ; 2 si l'épreuve n'a pas pu juger (appel mal formé, un cas ou une garde ne
  s'applique plus, erreur imprévue). Une ligne « OK »/« FAUX » par cas, « BILAN », les gardes, « VERDICT ».
  [rend: 1]
⑥ TRAITEMENT — Un banc dans un dossier temporaire : l'outil, le vérificateur, le référentiel, le carnet, chaque avis
  PDF cité et son texte figé. Un faux pdftotext, écrit par l'épreuve, dit la version qu'on lui donne et rend, pour un
  avis, le texte figé du DÉPÔT qui porte l'empreinte de cet avis (lu par le vérificateur du dépôt, `texte_fige_de`).
  Chaque cas : une copie du banc, une préparation, l'outil lancé, son code ET un fragment de son écran comparés à
  l'attendu, plus, pour F5, le nombre de lignes du carnet. Avec --saboter, chaque garde de l'outil est retirée une à
  une, et les cas sont rejoués jusqu'au premier qui tombe.
⑦ UNITÉ — Des codes de sortie.
⑧ POURQUOI — Relecture neuve du 01-11-2026 : M3 — deux avis aux octets identiques faisaient écrire deux lignes de
  carnet pour un même texte, et le vérificateur rougissait « inscrite 2 fois » ; M2 — l'outil et le vérificateur
  comparaient l'empreinte du carnet de deux façons. Le faux pdftotext : la nuit, GitHub a pdftotext 26.01.0 ; l'outil
  exige 24.02.0 (décision de Jean-Luc du 01-11-2026 à 14h05, « on vérifie une fois, au moment de figer, avec
  l'ancienne version 24.02 ») ; l'épreuve éprouve donc la LOGIQUE de l'outil, jamais la fidélité de pdftotext.
⑨ CE QUI CLOCHE — La fidélité réelle des textes à pdftotext 24.02.0 n'est pas éprouvée ici : elle l'est au moment de
  figer, par l'outil lui-même, sur une machine qui a 24.02.0. · Le cas F5 écrit le carnet (--ecrire) sur sa copie ;
  la date de la colonne `le` est celle du jour, ce que l'épreuve ne regarde pas. · Les cas sont écrits pour l'avis
  d'ERF et celui de DSY : si l'un disparaît du référentiel, son cas « ne s'applique plus » (code 2). · Un arrêt
  brutal laisse le dossier temporaire.
⑩ EFFET — Écrit et efface un dossier temporaire ; lance l'outil.
⑪ TERMINAISON — Rend la main ; chaque lancement est borné à 120 s ; sort par sys.exit.
  [sort: oui]
"""
import csv
import glob
import hashlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

OUTIL = "etudes/outils/FIGER_LE_TEXTE_DES_AVIS.py"
VERIF = "programmes/VERIFIER_LES_PREUVES_DU_REFERENTIEL.py"
CARNET = "donnees/PROVENANCE_DES_FICHIERS.csv"
ERF = "donnees/sources_du_referentiel/ERF_EUREX_Info_002_ERF.pdf"
DSY = "donnees/sources_du_referentiel/DSY_EUREX_Info_002_DYS1.pdf"
DSY_COPIE = "donnees/sources_du_referentiel/DSY_COPIE_POUR_L_EPREUVE.pdf"
FAUX_PDFTOTEXT = '''#!%s
import hashlib, json, os, sys
a = sys.argv[1:]
if a == ["-v"]:
    sys.stderr.write("pdftotext version " + os.environ["FAUX_VERSION"] + "\\n")
    sys.exit(0)
textes = json.load(open(os.environ["FAUX_TEXTES"]))
e = hashlib.sha256(open(a[-2], "rb").read()).hexdigest()
if e not in textes:
    sys.exit(1)
sys.stdout.buffer.write(open(textes[e], "rb").read())
'''


class NeSAppliquePlus(Exception):
    """Un cas ne s'applique plus au dépôt éprouvé : l'épreuve ne peut pas juger (code 2).

    ① RÔLE — Séparer « l'outil a mal répondu » de « le cas n'a pas pu être préparé » (référentiel, avis, texte figé ou
      ligne de carnet attendus absents ou changés).
    ② CONTEXTE D'APPEL — Levée par `construire`, `fabriquer_les_cas` et la préparation `deux_avis_identiques` ; reçue
      par `main`.
    ③ ENTRÉE — Le motif, en texte.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — — (une classe d'exception ne rend rien)
    ⑥ TRAITEMENT — —
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734 : une épreuve qui n'a pas pu juger ne rend jamais 0 ; `main` écrit « VERDICT IMPOSSIBLE — un
      cas ne s'applique plus » et rend 2.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — —
    """
    pass


def charger(chemin):
    """Charge un module depuis son fichier.

    ① RÔLE — Prendre au vérificateur du dépôt sa règle de nom des textes figés (R-708 : jamais recopiée ici).
    ② CONTEXTE D'APPEL — `construire`, une fois.
    ③ ENTRÉE — `chemin` : le fichier du module.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe.
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — importlib, sans écrire de cache de compilation.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le vérificateur ne fait que définir des fonctions à son chargement.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute le module.
    ⑪ TERMINAISON — Rend la main ou lève. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("VERIFICATEUR_DE_L_EPREUVE", chemin)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def construire(depot, travail):
    """Construit le banc, le faux pdftotext et sa table des textes ; rend les chemins utiles.

    ① RÔLE — Préparer, une fois, ce que chaque cas recopie.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `depot` : la racine éprouvée · `travail` : un dossier temporaire vide.
    ④ CONDITIONS D'ENTRÉE — Un seul référentiel au dépôt ; il cite ERF et DSY ; chaque avis cité a son texte figé.
      Sinon NeSAppliquePlus.
    ⑤ SORTIE — TROIS valeurs : le banc, le dossier du faux pdftotext, la table (fichier JSON empreinte → texte).
      [rend: 3]
    ⑥ TRAITEMENT — Copier l'outil, le vérificateur, le référentiel, le carnet, les avis cités et leurs textes figés ;
      écrire le faux pdftotext ; écrire la table, prise au dépôt par `texte_fige_de` du vérificateur du dépôt.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le faux rend le texte du DÉPÔT, jamais celui du cas : un cas qui retouche un texte figé le rend
      différent de « l'extraction », comme une vraie retouche.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans `travail`.
    ⑪ TERMINAISON — Rend la main ou lève. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    V = charger(os.path.join(depot, VERIF))
    refs = [os.path.relpath(p, depot) for p in glob.glob(os.path.join(depot, "donnees", "REFERENTIEL_VALEURS_*.csv"))]
    if len(refs) != 1:
        raise NeSAppliquePlus(f"{len(refs)} référentiel(s) au dépôt")
    lus = list(csv.DictReader(open(os.path.join(depot, refs[0]), encoding="utf-8-sig", newline="")))
    avis = sorted({f for r in lus for f in (r.get("fichiers_cites") or "").split(";") if f.lower().endswith(".pdf")})
    if ERF not in avis or DSY not in avis:
        raise NeSAppliquePlus("le référentiel ne cite plus ERF ou DSY")
    banc = os.path.join(travail, "banc")
    table = {}
    for f in [OUTIL, VERIF, CARNET, refs[0]] + avis + [V.texte_fige_de(depot, a) for a in avis]:
        if not os.path.isfile(os.path.join(depot, f)):
            raise NeSAppliquePlus(f"{f} absent du dépôt")
        os.makedirs(os.path.dirname(os.path.join(banc, f)), exist_ok=True)
        shutil.copyfile(os.path.join(depot, f), os.path.join(banc, f))
    for a in avis:
        table[hashlib.sha256(open(os.path.join(depot, a), "rb").read()).hexdigest()] = \
            os.path.join(depot, V.texte_fige_de(depot, a))
    faux = os.path.join(travail, "faux")
    os.makedirs(faux)
    open(os.path.join(faux, "pdftotext"), "w").write(FAUX_PDFTOTEXT % sys.executable)
    os.chmod(os.path.join(faux, "pdftotext"), 0o755)
    json.dump(table, open(os.path.join(travail, "textes.json"), "w"))
    return banc, faux, os.path.join(travail, "textes.json")


def fabriquer_les_cas(banc):
    """Rend la table des cas.

    ① RÔLE — Écrire chaque cas : sa préparation, ses options, la version que dit le faux pdftotext, le code et le
      fragment attendus, et le contrôle qui suit.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `banc`.
    ④ CONDITIONS D'ENTRÉE — Le carnet du banc inscrit le texte d'ERF une fois à son empreinte, sur une ligne entière
      (finie par « \n ») qui porte une fois cette empreinte et une fois l'avis d'ERF pour fichier lu ; sinon
      NeSAppliquePlus.
    ⑤ SORTIE — UNE valeur : nom → (préparation, options, version, code attendu, fragment attendu, contrôle après).
      [rend: 1]
    ⑥ TRAITEMENT — Lire le texte d'ERF et sa ligne du carnet ; de cette vraie ligne, tirer la vieille ligne de F8
      (une autre empreinte, le reste identique, placée avant elle) et la ligne de F9 (le fichier lu changé en l'avis
      de DSY) ; fabriquer les préparations.
    ⑦ UNITÉ — Des codes de sortie.
    ⑧ POURQUOI — F2 : la version (décision de 14h05) ; F3 : la fidélité ; F4 : la comparaison d'empreinte (M2) ;
      F5 : un texte, une ligne (M3) ; F6 : l'appel mal formé (R-734). F7, F8, F9 (relecture n° 2 du 04-11-2026, I1,
      m2, m3 ; superviseur R-759 du même jour, tour 3) : trois gardes de l'outil qu'aucun cas ne mordait — l'avis
      cité illisible (G5), une seule ligne par texte (G6), l'avis pour fichier lu (G7). F8 copie la vraie ligne
      (R-732) avec le même produit_par et le même fichier lu, et la place AVANT la bonne : sinon le contrôle de
      produit_par ou de lu rougirait à la place de G6, et G6 ne mordrait pas.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit le banc.
    ⑪ TERMINAISON — Rend la main ou lève NeSAppliquePlus.
      [sort: non]
    """
    V = charger(os.path.join(banc, VERIF))
    t_erf = V.texte_fige_de(banc, ERF)
    octets = open(os.path.join(banc, t_erf), "rb").read()
    e = hashlib.sha256(octets).hexdigest()
    carnet = open(os.path.join(banc, CARNET), "rb").read()
    ligne = (t_erf + "," + e + ",").encode()
    if carnet.count(ligne) != 1:
        raise NeSAppliquePlus(f"le carnet n'inscrit pas une fois {t_erf} à son empreinte")
    # F8 et F9 partent de la VRAIE ligne du carnet pour le texte d'ERF, en entier (R-732)
    debut = carnet.find(ligne)
    fin = carnet.find(b"\n", debut)
    if (debut > 0 and carnet[debut - 1:debut] != b"\n") or fin < 0:
        raise NeSAppliquePlus(f"la ligne de {t_erf} n'est pas une ligne entière du carnet")
    vraie = carnet[debut:fin + 1]
    lu_erf = ("," + ERF + ",").encode()
    if vraie.count(e.encode()) != 1 or vraie.count(lu_erf) != 1:
        raise NeSAppliquePlus(f"la ligne de {t_erf} ne porte pas une fois son empreinte et l'avis d'ERF pour fichier lu")
    # F8 : une vieille ligne du même texte, à une autre empreinte, même produit_par, même lu, AVANT la bonne
    vieille = vraie.replace(e.encode(), hashlib.sha256(octets + b"ancienne extraction\n").hexdigest().encode())
    carnet_vieille_ligne = carnet.replace(vraie, vieille + vraie)
    # F9 : la bonne ligne, seule et juste, sauf son fichier lu, qui nomme l'avis de DSY
    carnet_lu_d_un_autre = carnet.replace(vraie, vraie.replace(lu_erf, ("," + DSY + ",").encode()))

    def remplacer(d, chemin, nouveaux):
        """Remplace un fichier du dossier d'un cas par d'autres octets.

        ① RÔLE — Amener un défaut dans la copie d'un cas, sans toucher au banc.
        ② CONTEXTE D'APPEL — Les préparations des cas (F3, F4…) et `deux_avis_identiques`, une fois par cas, dans le
          dossier du cas que `jouer` vient de copier.
        ③ ENTRÉE — `d` : le dossier du cas · `chemin` : le fichier, depuis `d` · `nouveaux` : les octets à écrire.
        ④ CONDITIONS D'ENTRÉE — Le fichier existe dans `d` ; sinon FileNotFoundError, que `main` rend en code 2.
        ⑤ SORTIE — Aucune valeur.
          [rend: 0]
        ⑥ TRAITEMENT — Effacer le fichier, puis écrire les octets sous le même nom.
        ⑦ UNITÉ — Des octets.
        ⑧ POURQUOI — Même geste que `remplacer` de l'épreuve du référentiel, où le banc est copié en liens durs et où
          écrire à travers un lien modifierait le banc ; ici `jouer` copie le banc par `shutil.copytree`, effacer
          d'abord n'est qu'une précaution.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Efface et écrit un fichier du dossier du cas.
        ⑪ TERMINAISON — Rend la main ou lève OSError. Aucun de mes appels ne peut ne pas revenir.
          [sort: non]
        """
        os.remove(os.path.join(d, chemin))
        open(os.path.join(d, chemin), "wb").write(nouveaux)

    def deux_avis_identiques(d):
        """Prépare le cas F5 : deux avis aux octets identiques, cités tous les deux par le référentiel.

        ① RÔLE — Amener, dans la copie d'un cas, la situation de M3.
        ② CONTEXTE D'APPEL — `jouer`, comme préparation du cas F5, dans le dossier du cas.
        ③ ENTRÉE — `d` : le dossier du cas.
        ④ CONDITIONS D'ENTRÉE — Le référentiel du cas cite l'avis de DSY une seule fois ; sinon NeSAppliquePlus.
        ⑤ SORTIE — Aucune valeur.
          [rend: 0]
        ⑥ TRAITEMENT — Copier l'avis de DSY sous le nom DSY_COPIE ; dans le référentiel, lu en octets, remplacer la
          citation de DSY par « DSY;DSY_COPIE » (`remplacer`).
        ⑦ UNITÉ — Des octets.
        ⑧ POURQUOI — Relecture neuve du 01-11-2026, M3 : deux avis aux octets identiques faisaient écrire deux lignes
          de carnet pour un même texte. Le référentiel est lu en octets pour que sa marque d'ordre d'octets reste
          telle quelle.
        ⑨ CE QUI CLOCHE — Le référentiel est pris par `glob(...)[0]` : `construire` a déjà exigé qu'il soit seul au
          dépôt, et le banc n'en copie qu'un.
        ⑩ EFFET — Écrit un PDF et réécrit le référentiel, dans le dossier du cas.
        ⑪ TERMINAISON — Rend la main ou lève NeSAppliquePlus. Aucun de mes appels ne peut ne pas revenir.
          [sort: non]
        """
        shutil.copyfile(os.path.join(d, DSY), os.path.join(d, DSY_COPIE))
        ref = glob.glob(os.path.join(d, "donnees", "REFERENTIEL_VALEURS_*.csv"))[0]
        brut = open(ref, "rb").read()                 # en octets : la marque d'ordre d'octets reste telle quelle
        if brut.count(DSY.encode()) != 1:
            raise NeSAppliquePlus("DSY n'est pas cité une seule fois au référentiel")
        remplacer(d, os.path.relpath(ref, d), brut.replace(DSY.encode(), (DSY + ";" + DSY_COPIE).encode()))

    def une_ligne_pour_dsy(d):
        """Contrôle après le cas F5 : le carnet porte une seule ligne pour le texte figé de DSY.

        ① RÔLE — Compter au carnet ce que M3 demandait : un texte, une ligne.
        ② CONTEXTE D'APPEL — `jouer`, après l'outil, quand le cas F5 a rendu le code et le motif attendus.
        ③ ENTRÉE — `d` : le dossier du cas.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : None s'il y a exactement une ligne ; sinon le motif « <n> ligne(s) au carnet pour
          <texte> ».
          [rend: 1]
        ⑥ TRAITEMENT — Nommer le texte figé de DSY par `V.texte_fige_de` (le vérificateur du banc) ; lire le carnet
          du cas par le module csv ; compter les lignes dont la colonne `fichier` est ce nom.
        ⑦ UNITÉ — Un nombre de lignes, dans le motif.
        ⑧ POURQUOI — Le code et le motif de l'outil ne suffisent pas : on compte au carnet le défaut que M3 avait vu.
        ⑨ CE QUI CLOCHE — Le carnet est lu en « utf-8 », pas en « utf-8-sig » : un carnet à marque d'ordre d'octets
          ferait lever KeyError, que `main` rend en code 2 (faux rouge, jamais faux vert) ; le carnet du dépôt n'en a
          pas (mesuré le 04-11-2026).
        ⑩ EFFET — Lit le carnet du cas.
        ⑪ TERMINAISON — Rend la main ou lève. Aucun de mes appels ne peut ne pas revenir.
          [sort: non]
        """
        t =V.texte_fige_de(d, DSY)
        n = sum(1 for r in csv.DictReader(io.StringIO(open(os.path.join(d, CARNET), encoding="utf-8").read()))
                if r["fichier"] == t)
        return None if n == 1 else f"{n} ligne(s) au carnet pour {t}"

    return {
        "F1_temoin": (lambda d: None, [], "24.02.0", 0, "VERDICT CONFORME", None),
        "F2_autre_version": (lambda d: None, [], "26.01.0", 2, "n'est pas la version 24.02.0", None),
        "F3_texte_fige_retouche": (lambda d: remplacer(d, t_erf, octets + b"ligne ajoutee\n"), [], "24.02.0", 1,
                                   "diffère de pdftotext", None),
        "F4_empreinte_du_carnet_en_majuscules": (lambda d: remplacer(d, CARNET, carnet.replace(
            ligne, (t_erf + "," + e.upper() + ",").encode())), [], "24.02.0", 1, "le carnet ne porte pas", None),
        "F5_deux_avis_aux_memes_octets": (deux_avis_identiques, ["--ecrire"], "24.02.0", 0, "VERDICT CONFORME",
                                          une_ligne_pour_dsy),
        "F6_appel_mal_forme": ("SANS_RACINE", [], "24.02.0", 2, "appel mal formé", None),
        "F7_avis_cite_absent": (lambda d: os.remove(os.path.join(d, ERF)), [], "24.02.0", 2, "est illisible", None),
        "F8_vieille_ligne_avant_la_bonne": (lambda d: remplacer(d, CARNET, carnet_vieille_ligne), [], "24.02.0", 1,
                                            "pour fichier lu (2 ligne(s))", None),
        "F9_ligne_juste_lu_d_un_autre_avis": (lambda d: remplacer(d, CARNET, carnet_lu_d_un_autre), [], "24.02.0", 1,
                                              "pour fichier lu (1 ligne(s))", None),
    }


def jouer(banc, faux, table, travail, cas, bavard=True, jusqu_a_la_premiere_chute=False):
    """Joue les cas et rend les justes et les faux.

    ① RÔLE — Lancer l'outil sur chaque cas et juger.
    ② CONTEXTE D'APPEL — `main` : sur le banc, puis une fois par garde sabotée.
    ③ ENTRÉE — `banc` · `faux` : le dossier du faux pdftotext · `table` : sa table · `travail` · `cas` · `bavard` ·
      `jusqu_a_la_premiere_chute`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : justes, faux (listes de noms).
      [rend: 2]
    ⑥ TRAITEMENT — Pour chaque cas : copier le banc, préparer, lancer l'outil (faux pdftotext en tête du chemin,
      version donnée), juger le code, le fragment, puis le contrôle après.
    ⑦ UNITÉ — Des codes de sortie.
    ⑧ POURQUOI — Le fragment distingue une détection d'un plantage.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit et efface un dossier par cas ; écrit à l'écran.
    ⑪ TERMINAISON — Rend la main ; chaque lancement est borné à 120 s.
      [sort: non]
    """
    justes, tombes = [], []
    for nom, (prep, options, version, attendu, fragment, apres) in cas.items():
        d = os.path.join(travail, "cas")
        shutil.rmtree(d, ignore_errors=True)
        shutil.copytree(banc, d)
        try:
            args = [] if prep == "SANS_RACINE" else [d] + options
            if prep != "SANS_RACINE":
                prep(d)
            env = dict(os.environ, PATH=faux + os.pathsep + os.environ.get("PATH", ""), FAUX_VERSION=version,
                       FAUX_TEXTES=table)
            p = subprocess.run([sys.executable, "-B", "-I", os.path.join(d, OUTIL)] + args, capture_output=True,
                               text=True, timeout=120, env=env)
            ecran = p.stdout + p.stderr
            ok = p.returncode == attendu and fragment in ecran
            if ok and apres:
                motif = apres(d)
                if motif:
                    ok, ecran = False, ecran + "\nCONTRÔLE APRÈS : " + motif
            (justes if ok else tombes).append(nom)
            if bavard or not ok:
                fin = [l for l in ecran.splitlines() if l.startswith(("VERDICT", "CONTRÔLE", "Traceback"))][-2:]
                print(("OK   " if ok else "FAUX ") + f"{nom} : code {p.returncode} (attendu {attendu}, motif « {fragment} »)"
                      + " — " + " | ".join(x[:110] for x in fin))
        finally:
            shutil.rmtree(d, ignore_errors=True)
        if jusqu_a_la_premiere_chute and tombes:
            break
    return justes, tombes


GARDES = {
    "G1_version_exigee": ("        verifier_la_version()\n", "        pass\n"),
    "G2_comparaison_octet_pour_octet": ("    if octets != extrait:\n", "    if False:\n"),
    "G3_empreinte_du_carnet": ("V.inscrite_au_carnet(carnet, texte, e) != 1", "False"),
    "G4_un_avis_par_contenu": ("                if texte not in textes:", "                if True:"),
    "G5_avis_cite_illisible": ("raise Impossible(f\"l'avis {f} est illisible : {e}\")", "continue"),
    "G6_une_seule_ligne_par_texte": ("len(lignes) != 1", "False"),
    "G7_avis_pour_fichier_lu": ('lignes[0]["lu"] != chemin', "False"),
}


def main(argv):
    """Le point d'entrée.

    ① RÔLE — Jouer les cas, puis les gardes sabotées si demandé.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — `argv` : le nom du programme, la racine, --saboter facultatif.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le code de sortie (voir le ⑤ du programme).
      [rend: 1]
    ⑥ TRAITEMENT — Le ⑥ du programme ; une NeSAppliquePlus ou une erreur imprévue rend « VERDICT IMPOSSIBLE » et 2.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734 : une épreuve qui n'a pas pu juger ne rend jamais 0.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit et efface un dossier temporaire ; écrit à l'écran.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    args = [a for a in argv[1:] if a != "--saboter"]
    if len(args) != 1 or not os.path.isdir(args[0]):
        print(__doc__.split("③")[0])
        print("VERDICT IMPOSSIBLE — appel mal formé")
        return 2
    travail = tempfile.mkdtemp(prefix="epreuves_outil_qui_fige.")
    impossible = False
    try:
        banc, faux, table = construire(os.path.abspath(args[0]), travail)
        cas = fabriquer_les_cas(banc)
        justes, tombes = jouer(banc, faux, table, travail, cas)
        print(f"BILAN {len(justes)} / {len(cas)} cas justes")
        ok = not tombes
        if "--saboter" in argv[1:]:
            source = open(os.path.join(banc, OUTIL), encoding="utf-8").read()
            for nom, (a, b) in GARDES.items():
                if source.count(a) != 1:
                    print(f"{nom} NE S'APPLIQUE PLUS")
                    impossible = True
                    continue
                os.remove(os.path.join(banc, OUTIL))
                open(os.path.join(banc, OUTIL), "w", encoding="utf-8").write(source.replace(a, b))
                _, t = jouer(banc, faux, table, travail, cas, bavard=False, jusqu_a_la_premiere_chute=True)
                print(f"{nom} mord : {t}" if t else f"{nom} NE MORD PAS []")
                ok = ok and bool(t)
            os.remove(os.path.join(banc, OUTIL))
            open(os.path.join(banc, OUTIL), "w", encoding="utf-8").write(source)
    except NeSAppliquePlus as e:
        print(f"VERDICT IMPOSSIBLE — un cas ne s'applique plus : {e}")
        return 2
    except Exception as e:                                # dernier filet : une panne de l'épreuve n'est pas un verdict
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
