#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_LARGEUR_DES_CIRCUITS — Mar 17-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Décision de Jean-Luc A-884 du 17-11-2026 à 22h00 (« 1 » : utiliser la puissance gratuite de GitHub
sans relâcher un contrôle) et A-886 de 22h08 ; conception : etudes/A-884_GITHUB_AU_MAXIMUM_Mar_17-11-2026.md, étapes
① et ②. Un compte gratuit de GitHub ne fait tourner que 20 tâches à la fois (documentation « Actions limits »). Le
fabricant (programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py) réservait aux circuits longs une part écrite à la main
(MARGE_DES_AUTRES_CIRCUITS = 10, relevée le 15-11-2026) ; la certification est passée de 6 à 12 tranches le même jour,
la largeur réelle des autres circuits est devenue 16, et 16 + 10 = 26 > 20 sans qu'aucune épreuve le voie : les
épreuves N1 et G1 comparaient la part à la constante, pas aux fiches. Cette épreuve calcule la largeur SUR LES FICHES
FABRIQUÉES (`largeur_d_une_fiche` du fabricant) et exige que les circuits qui ne doivent jamais attendre et les
circuits longs tiennent ensemble dans les 20. Elle porte sur une propriété : renommer un circuit ne change pas sa
largeur, qui se lit dans son texte.

① RÔLE — Éprouver `structure_d_une_fiche`, `largeur_d_une_fiche`, `refus_de_la_largeur`, `fiches_du_clone_public` et
  la porte de la largeur dans `fabriquer_et_publier`, sur les fiches que le fabricant écrit vraiment.
② CONTEXTE D'APPEL — Chaque nuit par la certification (épreuve de tests/, lancée avec la racine, puis avec --saboter) ;
  à la main avant toute livraison qui touche la largeur (R-731) :
  python3 tests/EPREUVES_DE_LA_LARGEUR_DES_CIRCUITS_Mar_17-11-2026.py <racine> [--public=<clone public>]
  [--saboter | --saboter=SL1,…]
③ ENTRÉE — La racine d'un dépôt : programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, programmes/FORME_D_UN_JETON.py,
  tests/LANCEMENT_DES_EPREUVES.json, .github/workflows/collecte_abc.yml. Avec --public, le dossier d'un clone du dépôt
  public : ses fiches posées à la main (celles que le fabricant n'écrit pas) entrent dans L0 et L5.
④ CONDITIONS D'ENTRÉE — PyYAML installé (L1 compare la lecture du fabricant à la sienne ; sans lui, L1 est FAUX :
  un contrôle qui n'a pas pu tourner ne passe pas, R-734).
⑤ SORTIE — Le code de sortie : 0 si chaque cas donne la réponse attendue et, avec --saboter, si chaque sabotage en fait
  échouer au moins un ; 1 sinon ; 2 si un sabotage ne s'applique plus.
  [rend: 1]
⑥ TRAITEMENT —
  L0 (la propriété, sur les VRAIES fiches fabriquées, R-732) : les cinq circuits que la publication écrit
  (`ce_que_la_publication_ecrit`), plus, avec --public, les fiches du clone public que le fabricant n'écrit pas ;
  `refus_de_la_largeur` ne rend aucun refus ; le détail du calcul est affiché.
  L1 (l'étalonnage, sur les mêmes fiches) : la largeur calculée vaut 1 pour le circuit du soir et pour le relais,
  PLACES_LONGUES pour la certification, les séries et les épreuves longues, qui sont des fiches du réservoir
  (étape FILE-2, 20-11-2026 : `largeur_d_une_fiche` rend RESERVOIR_DES_PLACES) ; et la lecture du fabricant (groupe,
  « needs », « max-parallel », tailles de matrice, depuis A-896 « queue » et « cancel-in-progress » du groupe, depuis
  FILE-2 le groupe de chaque JOB et sa file) est celle de PyYAML, fiche par fiche.
  L2 (le calculateur, sur des fiches écrites ici, chacune avec sa réponse) : jobs sans lien qui s'additionnent, chaîne
  qui ne s'additionne pas, losange, « needs » en ligne, matrice 2 × 3, « max-parallel » qui borne, matrice calculée par
  GitHub bornée, un faux « jobs: » dans un bloc « run: | » ignoré, groupe en ligne, groupe à « ${{ » rendu absent ; et
  la fiche du réservoir (FILE-2) ; les refus, chacun pour SA raison : matrice calculée sans borne, « uses: »,
  « concurrency: » de job écrit sur sa ligne, un job sans place dans une fiche à places, une place non bornée, une
  place sans file, une place qui tue le job en cours, un « concurrency: » de job sans « group: », « needs » vers un
  job absent, cycle, « max-parallel » non entier, « include » en clair, élément de matrice qui n'est pas un scalaire,
  chaîne non fermée, ligne hors du sous-ensemble, valeur continuée, tabulation, aucun job.
  L3 (la propriété, sur des fiches ajoutées aux vraies) : une fiche nouvelle non classée → refus « sans famille » ; une
  fiche « jamais attendre » sans groupe → refus « sans groupe » ; une fiche « peut attendre » de 50 tâches → aucun
  refus (elle attend) ; une fiche « jamais attendre » de 3 tâches avec son groupe → refus « largeur du compte
  dépassée » ; deux fiches « longs » d'un même groupe, en file, comptent pour une (L3e ; deux « jamais attendre »
  d'un même groupe sont refusées, voir L3j) ; une famille inconnue → refus. Depuis A-896 (la file unique, `refus_de_la_file`) : deux fiches d'un même groupe dont une sans « queue: max »
  → refus ; une fiche « peut attendre » qui porte le groupe des longs → refus ; une seule tâche de trop (total 21) →
  refus (D3 de la relecture de A-884) ; une fiche « jamais attendre » dont le job prend une place du réservoir →
  refus, et le circuit du soir seul dans son groupe → aucun refus (E1 de la relecture de A-896).
  L7 (le réservoir, étape FILE-2) : la somme vaut 1 + 1 + PLACES_LONGUES, au plus TACHES_EN_MEME_TEMPS_DU_COMPTE, et
  PLACES_LONGUES = TACHES_EN_MEME_TEMPS_DU_COMPTE − 2 (A-888) ; chaque job des fiches « longs » porte une place
  bornée (« ${{ s == '18' && '18' || … || '1' }} », une seule source, chaque place de 2 à PLACES_LONGUES une fois) en
  file. Les sabotages SL18 et SL28 retirent ou dénaturent le groupe de passage par branche (la protection fine).
  L6 (les entrées du bouton, E4 de la relecture de A-896) : chaque fiche fabriquée porte au plus
  ENTREES_DU_BOUTON_AU_PLUS entrées ; celle des séries, exactement len(ENTREES_FIXES_DES_SERIES) + len(ENTREES_PAR_SERIE)
  × le nombre de séries (comptées par PyYAML).
  L4 (`fiches_du_clone_public`) : rend chaque `.yml` et `.yaml` du dossier, rien d'autre ; un dossier absent → {}.
  L5 (la porte, le fabricant en ligne de commande sur une copie minuscule de la racine, sans git) : vers un public
  neuf → 0 et la ligne du total ; vers un public qui porte une fiche nouvelle non classée → 1, « ARRÊT », la fiche
  nommée ; avec --public, vers un public qui porte les fiches posées à la main → 0.
⑦ UNITÉ — Des tâches de GitHub ; des codes de sortie.
⑧ POURQUOI — R-731 : tout code écrit a ses épreuves au dépôt, avec des sabotages qui mordent chacun pour sa raison.
  L'étude A-884 (§ 3.1) demandait que l'épreuve ROUGISSE d'abord sur l'état d'avant (26 > 20) : sortie capturée dans
  la note de livraison du 17-11-2026.
⑨ CE QUI CLOCHE — Le lecteur des fiches n'est pas celui de GitHub : PyYAML sert d'étalon (pas d'arbitre : il lit
  « on » comme True). Sans --public, les fiches posées à la main au dépôt public ne sont pas lues par L0 : c'est la
  porte de la publication (L5) qui les lit, au moment où elles comptent. Ce que GitHub fait au-delà de 20 tâches
  (file ou annulation) n'est éprouvé nulle part : THÉORIQUE (étude A-884, § 3.1, point 4).
⑩ EFFET — Écrit dans des dossiers jetables, effacés à la fin.
⑪ TERMINAISON — Rend la main ; chaque lancement est borné à 300 secondes ; sort par sys.exit.
  [sort: oui]
"""
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
_publics = [a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--public=")]
PUBLIC = os.path.abspath(_publics[0]) if _publics else None
FABRICANT = "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"
JETON = "programmes/FORME_D_UN_JETON.py"     # chargé par le fabricant (refus_avant_publication), à côté de lui
TABLE = "tests/LANCEMENT_DES_EPREUVES.json"
CIRCUIT_PRIVE = ".github/workflows/collecte_abc.yml"
LUS = (FABRICANT, JETON, TABLE, CIRCUIT_PRIVE)
NOTES = []
PERMISSIONS = "permissions:\n  contents: read\n"


def lancer(args, cwd=None):
    """Lance une commande ; rend (code, sortie et erreurs réunies).

    ① RÔLE — Un lancement borné. ② CONTEXTE D'APPEL — `tour` (L5). ③ ENTRÉE — `args`, `cwd`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — DEUX valeurs : le code, le texte. [rend: 2] ⑥ TRAITEMENT — subprocess, 300 s.
    ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — Un dépassement lève TimeoutExpired : rangé parmi les cas faux.
    ⑩ EFFET — Ce que fait la commande. ⑪ TERMINAISON — Rend la main ; 300 s au plus. [sort: non]
    """
    p = subprocess.run(args, capture_output=True, text=True, cwd=cwd, timeout=300, errors="replace")
    return p.returncode, p.stdout + p.stderr


def charger(chemin, nom):
    """Charge un programme comme un module, par son chemin.

    ① RÔLE — Appeler les fonctions de la racine éprouvée. ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — `chemin`, `nom`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le module. [rend: 1] ⑥ TRAITEMENT — importlib.
    ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — Le code de tête du programme s'exécute. ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]
    """
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fiche(jobs, groupe="g", tete="", file=""):
    """Rend le texte d'une fiche minuscule : `tete`, un groupe de concurrence (sauf None), puis `jobs`.

    ① RÔLE — Écrire les fiches des cas L2 et L3 sans les recopier. ② CONTEXTE D'APPEL — `tour`.
    ③ ENTRÉE — `jobs` : le texte du bloc des jobs, sans « jobs: » ; `groupe` ; `tete` : des lignes de tête ; `file` :
      des lignes ajoutées sous « concurrency: » (A-896 : « queue: max »), sans effet si `groupe` est None.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le texte. [rend: 1] ⑥ TRAITEMENT — concaténation.
    ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    concurrence = "" if groupe is None else f"concurrency:\n  group: {groupe}\n  cancel-in-progress: false\n{file}"
    return f"name: essai\non:\n  workflow_dispatch:\n{tete}{concurrence}{PERMISSIONS}jobs:\n{jobs}"


UN = "  a:\n    runs-on: ubuntu-latest\n    steps:\n      - run: true\n"
# étape FILE-2 : un job à sa place, écrit ici sans le fabricant (l'expression bornée recopiée de sa forme documentée)
_BORNE_I = "${{ " + "".join("inputs.premiere_place == '%d' && '%d' || " % (k, k) for k in range(18, 1, -1)) + "'1' }}"
_BORNE_M = "${{ " + "".join("matrix.place == '%d' && '%d' || " % (k, k) for k in range(18, 1, -1)) + "'1' }}"
PLACE_I = UN.replace("    runs-on", "    concurrency:\n      group: place-longue-" + _BORNE_I
                     + "\n      cancel-in-progress: false\n      queue: max\n    runs-on")
PLACE_M = "    concurrency:\n      group: place-longue-" + _BORNE_M + "\n      cancel-in-progress: false\n      queue: max\n"
# L2 : (nom, texte, réponse attendue : (groupe, largeur), ou le fragment du refus)
CAS_DU_CALCULATEUR = [
    ("L2a deux jobs sans lien s'additionnent", fiche(UN + UN.replace("  a:", "  b:")), ("g", 2)),
    ("L2b une chaîne ne s'additionne pas", fiche(UN + UN.replace("  a:", "  b:\n    needs: a")), ("g", 1)),
    ("L2c losange : b et c ensemble", fiche(UN + UN.replace("  a:", "  b:\n    needs: a") + UN.replace("  a:", "  c:\n    needs:\n      - a")
                                            + UN.replace("  a:", "  d:\n    needs: [b, c]")), ("g", 2)),
    ("L2d matrice 2 × 3", fiche("  a:\n    strategy:\n      matrix:\n        x:\n          - 1\n          - 2\n        y: [p, q, r]\n"
                                "    runs-on: ubuntu-latest\n"), ("g", 6)),
    ("L2e max-parallel borne la matrice", fiche("  a:\n    strategy:\n      max-parallel: 4\n      matrix:\n        y: [p, q, r, s, t, u]\n"
                                                 "    runs-on: ubuntu-latest\n"), ("g", 4)),
    ("L2f matrice calculée par GitHub, bornée, plus un job libre",
     fiche("  a:\n    strategy:\n      max-parallel: 7\n      matrix:\n        include: ${{ fromJSON(x) }}\n    runs-on: ubuntu-latest\n"
           + UN.replace("  a:", "  b:")), ("g", 8)),
    ("L2g un faux « jobs: » dans un bloc run est ignoré",
     fiche("  a:\n    runs-on: ubuntu-latest\n    steps:\n      - run: |\n          jobs:\n            z:\n              strategy:\n"
           "                max-parallel: 99\n"), ("g", 1)),
    ("L2h groupe écrit sur sa ligne", "on:\n  push:\nconcurrency: seul\n" + PERMISSIONS + "jobs:\n" + UN, ("seul", 1)),
    ("L2i groupe qui change d'un passage à l'autre", fiche(UN, groupe="g-${{ github.ref }}"), (None, 1)),
    ("L2j matrice calculée sans borne", fiche("  a:\n    strategy:\n      matrix:\n        include: ${{ fromJSON(x) }}\n"
                                             "    runs-on: ubuntu-latest\n"), "largeur sans borne"),
    ("L2k job qui appelle un circuit", fiche("  a:\n    uses: ./.github/workflows/x.yml\n"), "porte « uses: »"),
    ("L2l job qui porte son groupe sur sa ligne", fiche("  a:\n    concurrency: x\n    runs-on: ubuntu-latest\n"),
     "porte « concurrency: » sur sa ligne"),
    # étape FILE-2 : les fiches du réservoir — chaque job sur une place bornée, en file, sinon refus pour SA raison
    ("L2w fiche du réservoir", fiche(PLACE_I + UN.replace("  a:", "  b:\n    needs: a").replace("    runs-on", PLACE_M + "    runs-on")),
     ("place-longue-1…18", 18)),
    ("L2x un job sans place dans une fiche à places", fiche(PLACE_I + UN.replace("  a:", "  b:")), "sans place dans une fiche à places"),
    ("L2y une place non bornée", fiche(UN.replace("    runs-on", "    concurrency:\n      group: place-longue-${{ matrix.place }}\n"
                                                  "      queue: max\n    runs-on")), "groupe de job non reconnu"),
    ("L2z une place sans file", fiche(PLACE_I.replace("      queue: max\n", "")), "n'est pas une file"),
    ("L2za une place qui tue le job en cours", fiche(PLACE_I.replace("cancel-in-progress: false", "cancel-in-progress: true")),
     "n'est pas une file"),
    ("L2zb concurrency de job sans group", fiche(UN.replace("    runs-on", "    concurrency:\n      queue: max\n    runs-on")),
     "sans « group: »"),
    ("L2m needs vers un job absent", fiche(UN.replace("  a:", "  a:\n    needs: z")), "absent de la fiche"),
    ("L2n cycle de needs", fiche(UN.replace("  a:", "  a:\n    needs: b") + UN.replace("  a:", "  b:\n    needs: a")), "cycle"),
    ("L2o max-parallel non entier", fiche("  a:\n    strategy:\n      max-parallel: ${{ x }}\n      matrix:\n        y: [1, 2]\n"),
     "pas un entier positif"),
    ("L2p include écrit en clair", fiche("  a:\n    strategy:\n      matrix:\n        include:\n          - y: 1\n"), "écrit en clair"),
    ("L2q élément de matrice qui n'est pas un scalaire", fiche("  a:\n    strategy:\n      matrix:\n        y:\n          - k: 1\n"),
     "pas un scalaire"),
    ("L2r chaîne non fermée", fiche(UN.replace("runs-on: ubuntu-latest", 'runs-on: "ubuntu')), "non fermée"),
    ("L2s ligne hors du sous-ensemble", fiche(UN.replace("    runs-on", '    "runs-on"')), "ni « clé: valeur »"),
    ("L2t valeur continuée", fiche(UN.replace("  a:\n", "  a:\n    needs: b\n      c\n") + UN.replace("  a:", "  b:")),
     "continuée"),
    ("L2u tabulation", fiche(UN).replace("ubuntu-latest", "ubuntu-latest\t"), "U+0009"),
    ("L2v aucun job", "on:\n  push:\n" + PERMISSIONS + "jobs:\n", "aucun job"),
]


def tour(racine):
    """Joue L0 à L6 sur `racine` ; rend la liste des cas faux.

    ① RÔLE — Un tour complet. ② CONTEXTE D'APPEL — `main`, une fois tel quel et une fois par sabotage.
    ③ ENTRÉE — `racine` : la racine éprouvée (la vraie, ou une copie sabotée). ④ CONDITIONS D'ENTRÉE — Fiche en tête.
    ⑤ SORTIE — UNE valeur : la liste des cas faux (textes). [rend: 1]
    ⑥ TRAITEMENT — Fiche en tête, L0 à L6. La table des familles est augmentée pour L3 puis rendue telle quelle.
    ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête. ⑨ CE QUI CLOCHE — Fiche en tête. ⑩ EFFET — Dossiers jetables.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    faux = []
    d = tempfile.mkdtemp(prefix="largeur_")
    try:
        F = charger(os.path.join(racine, FABRICANT), "fabricant_largeur")
        soir = F.fabriquer_le_circuit(open(os.path.join(racine, CIRCUIT_PRIVE), encoding="utf-8").read())
        fabriquees = {c.split("/")[-1]: o.decode("utf-8") for c, o in F.ce_que_la_publication_ecrit(racine, [], [], soir)
                      if c.startswith(".github/workflows/")}
        a_la_main = {}
        if PUBLIC:
            a_la_main = {n: t for n, t in F.fiches_du_clone_public(PUBLIC).items() if n not in fabriquees}
            NOTES.append(f"fiches posées à la main lues au clone public : {', '.join(sorted(a_la_main)) or 'aucune'}")
        else:
            NOTES.append("sans --public : les fiches posées à la main au dépôt public ne sont pas lues par L0 ; la porte "
                         "de la publication les lit (L5)")
        # ---- L0 : la propriété, sur les vraies fiches
        refus, lignes = F.refus_de_la_largeur(dict(fabriquees, **a_la_main))
        for l in lignes:
            NOTES.append("L0 " + l)
        faux += ["L0 " + r for r in refus]
        # ---- L7 (étape FILE-2, 20-11-2026) : LE RÉSERVOIR — la somme des fiches fabriquées vaut le soir (1) + le
        # relais (1) + PLACES_LONGUES, recalculée ici sans le fabricant, et ne dépasse pas la limite du compte (A-888 :
        # 2 places toujours libres) ; chaque job des trois circuits longs porte une place BORNÉE — « <préfixe>${{ s ==
        # '18' && '18' || … || s == '2' && '2' || '1' }} », chaque k de 2 à PLACES_LONGUES une fois, rien d'autre
        # (SL25 : « s || … » ouvrirait un groupe par valeur reçue), avec « queue: max » (SL26)
        total = next((int(m.group(1)) for l in lignes for m in [re.search(r"sans attendre : .* = ([0-9]+) \(limite", l)] if m),
                     None)
        attendu_t = 1 + 1 + F.PLACES_LONGUES
        if total != attendu_t or attendu_t > F.TACHES_EN_MEME_TEMPS_DU_COMPTE:
            faux.append(f"L7 somme des circuits qui n'attendent pas : {total}, attendu {attendu_t} (soir 1 + relais 1 + "
                        f"{F.PLACES_LONGUES} places), limite {F.TACHES_EN_MEME_TEMPS_DU_COMPTE}")
        if F.PLACES_LONGUES != F.TACHES_EN_MEME_TEMPS_DU_COMPTE - 2:
            faux.append(f"L7 {F.PLACES_LONGUES} places longues : A-888 en veut {F.TACHES_EN_MEME_TEMPS_DU_COMPTE - 2} "
                        "(2 places toujours libres)")
        borne = (r"\$\{\{ (?:(?P<s>matrix\.place|inputs\.premiere_place|matrix\.tranche) == '(?P<k>[0-9]+)' && '(?P=k)' \|\| )*"
                 r"'1' \}\}")
        for nom, texte in sorted(fabriquees.items()):
            if F.FAMILLES_DES_CIRCUITS_PUBLICS.get(nom) != F.LONGS:
                continue
            _, jobs_l, _ = F.structure_d_une_fiche(texte)
            for j, v in sorted(jobs_l.items()):
                g = v["groupe"] or ""
                m = re.fullmatch(re.escape(F.PREFIXE_DES_PLACES) + borne, g)
                ks = [int(k) for k in re.findall(r" == '([0-9]+)'", g)]
                sources = set(re.findall(r"(matrix\.place|inputs\.premiere_place|matrix\.tranche) ==", g))
                if not m or sorted(ks) != list(range(2, F.PLACES_LONGUES + 1)) or len(sources) != 1:
                    faux.append(f"L7 {nom}, job {j} : place absente ou non bornée aux places 1 à {F.PLACES_LONGUES} : {g[:90]}")
                if (v["file"] or {}).get("queue") != "max" or (v["file"] or {}).get("cancel-in-progress") == "true":
                    faux.append(f"L7 {nom}, job {j} : sa place n'est pas une file ({v['file']})")
        # ---- L1 : l'étalonnage
        # étape FILE-2 : les trois circuits longs sont des fiches du réservoir, chacune de largeur PLACES_LONGUES (leurs
        # passages ensemble n'occupent jamais plus de places qu'il n'y en a)
        attendu = {os.path.basename(F.CIRCUIT_PUBLIC): 1, os.path.basename(F.CIRCUIT_RELAIS): 1,
                   os.path.basename(F.CIRCUIT_CERTIFICATION): F.PLACES_LONGUES,
                   os.path.basename(F.CIRCUIT_SERIES): F.PLACES_LONGUES,
                   os.path.basename(F.CIRCUIT_EPREUVES): F.PLACES_LONGUES}
        if sorted(attendu) != sorted(fabriquees):
            faux.append(f"L1 circuits fabriqués {sorted(fabriquees)} au lieu de {sorted(attendu)}")
        for nom, largeur in attendu.items():
            try:
                g, l = F.largeur_d_une_fiche(fabriquees.get(nom, ""))
            except ValueError as e:
                faux.append(f"L1 {nom} : refusée : {e}")
                continue
            if l != largeur:
                faux.append(f"L1 {nom} : largeur {l} au lieu de {largeur}")
            if F.FAMILLES_DES_CIRCUITS_PUBLICS.get(nom) == F.LONGS and g != F.RESERVOIR_DES_PLACES:
                faux.append(f"L1 {nom} : groupe {g} au lieu de {F.RESERVOIR_DES_PLACES}")
        try:
            import yaml
        except ImportError:
            faux.append("L1 PyYAML absent : l'étalonnage du lecteur n'a pas pu tourner (R-734)")
            yaml = None
        for nom, texte in sorted(dict(fabriquees, **a_la_main).items()) if yaml else ():
            try:
                groupe, jobs, file = F.structure_d_une_fiche(texte)
            except ValueError as e:
                faux.append(f"L1 {nom} : lecture du fabricant refusée : {e}")
                continue
            y = yaml.safe_load(texte)
            c = y.get("concurrency")
            gy = c.get("group") if isinstance(c, dict) else c
            # A-896 : la file du groupe, comparée à PyYAML (qui lit « false » comme un booléen : remis en texte)
            fy = {k: (None if not isinstance(c, dict) or k not in c else
                      str(c[k]).lower() if isinstance(c[k], bool) else str(c[k])) for k in ("queue", "cancel-in-progress")}
            if file != fy:
                faux.append(f"L1 {nom} : file lue par le fabricant {file} ≠ PyYAML {fy}")
            jy = {}
            for j, corps in (y.get("jobs") or {}).items():
                besoins = corps.get("needs", [])
                strategie = corps.get("strategy") or {}
                matrice = strategie.get("matrix")
                if matrice is None:
                    tailles = None
                elif isinstance(matrice, str):
                    tailles = [None]
                else:
                    tailles = sorted((len(v) if isinstance(v, list) else None for v in matrice.values()), key=str)
                cj = corps.get("concurrency")
                jy[j] = {"needs": [besoins] if isinstance(besoins, str) else list(besoins),
                         "max_parallel": strategie.get("max-parallel"), "matrice": tailles,
                         # étape FILE-2 : le groupe de job et sa file, comparés à PyYAML
                         "groupe": (cj.get("group") if isinstance(cj, dict) else cj),
                         "file": None if not isinstance(cj, dict) else
                         {k: (None if k not in cj else str(cj[k]).lower() if isinstance(cj[k], bool) else str(cj[k]))
                          for k in ("queue", "cancel-in-progress")}}
            jf = {j: dict(v, matrice=None if v["matrice"] is None else sorted(v["matrice"], key=str)) for j, v in jobs.items()}
            if (groupe, jf) != (gy, jy):
                faux.append(f"L1 {nom} : lecture du fabricant {groupe, jf} ≠ PyYAML {gy, jy}")
        # ---- L6 : les entrées du bouton (E4 de la relecture de A-896, superviseur R-759 du 18-11-2026) : comptées sur
        # chaque fiche fabriquée, ENTREES_DU_BOUTON_AU_PLUS au plus ; celles des séries, exactement celles des deux
        # tuples qui écrivent le bouton (une entrée écrite à la main ailleurs serait comptée en trop)
        for nom, texte in sorted(fabriquees.items()) if yaml else ():
            y = yaml.safe_load(texte)
            declencheurs = y.get(True) or y.get("on") or {}
            entrees = ((declencheurs.get("workflow_dispatch") or {}).get("inputs") or {}) if isinstance(declencheurs, dict) else {}
            if len(entrees) > F.ENTREES_DU_BOUTON_AU_PLUS:
                faux.append(f"L6 {nom} : {len(entrees)} entrées du bouton, au-delà de {F.ENTREES_DU_BOUTON_AU_PLUS}")
            if nom == os.path.basename(F.CIRCUIT_SERIES):
                attendu_e = len(F.ENTREES_FIXES_DES_SERIES) + len(F.ENTREES_PAR_SERIE) * len(F.SERIES_DU_CIRCUIT)
                if len(entrees) != attendu_e:
                    faux.append(f"L6 {nom} : {len(entrees)} entrées du bouton au lieu de {attendu_e} (les tuples du fabricant)")
                NOTES.append(f"L6 {nom} : {len(entrees)} entrées du bouton (au plus {F.ENTREES_DU_BOUTON_AU_PLUS})")
        # ---- L2 : le calculateur
        for nom, texte, reponse in CAS_DU_CALCULATEUR:
            try:
                vu = F.largeur_d_une_fiche(texte)
            except ValueError as e:
                if not isinstance(reponse, str) or reponse not in str(e):
                    faux.append(f"{nom} : refusée ({e}) au lieu de {reponse}")
                continue
            if vu != reponse:
                faux.append(f"{nom} : {vu} au lieu de {reponse}")
        # ---- L3 : la propriété, sur des fiches ajoutées aux vraies
        familles = dict(F.FAMILLES_DES_CIRCUITS_PUBLICS)
        try:
            F.FAMILLES_DES_CIRCUITS_PUBLICS.update({"jamais_sans_groupe.yml": F.JAMAIS_ATTENDRE,
                                                    "peut_attendre.yml": F.PEUT_ATTENDRE,
                                                    "jamais_large.yml": F.JAMAIS_ATTENDRE,
                                                    # « longs » depuis E1 (18-11-2026) : deux « jamais attendre » d'un
                                                    # même groupe sont refusées (L3j), deux « longs », non
                                                    "jamais_meme_groupe_1.yml": F.LONGS,
                                                    "jamais_meme_groupe_2.yml": F.LONGS,
                                                    "jamais_21.yml": F.JAMAIS_ATTENDRE,
                                                    "jamais_dans_les_places.yml": F.JAMAIS_ATTENDRE,
                                                    "peut_attendre_dans_la_file.yml": F.PEUT_ATTENDRE,
                                                    "famille_inconnue.yml": "plus tard"})
            soir_texte = fabriquees[os.path.basename(F.CIRCUIT_PUBLIC)]
            if soir_texte.count("concurrency:\n  group: circuit-du-soir\n") != 1:
                faux.append("L3j le groupe du circuit du soir n'est plus lu à sa place : le cas ne s'applique plus")
            large = fiche("  a:\n    strategy:\n      matrix:\n        y: [1, 2, 3]\n    runs-on: ubuntu-latest\n", groupe="large")
            cent = fiche("  a:\n    strategy:\n      matrix:\n        y: [" + ", ".join(map(str, range(50))) + "]\n",
                         groupe="cent")
            for nom, ajout, fragment in (
                    ("L3a fiche nouvelle non classée", {"nouvelle.yml": fiche(UN, groupe="nouvelle")}, "nouvelle.yml : fiche publique sans famille"),
                    ("L3b jamais attendre sans groupe", {"jamais_sans_groupe.yml": fiche(UN, groupe=None)}, "jamais_sans_groupe.yml : comptée parmi"),
                    ("L3c peut attendre de 50 tâches", {"peut_attendre.yml": cent}, None),
                    ("L3d jamais attendre de 3 tâches", {"jamais_large.yml": large}, "largeur du compte dépassée"),
                    # deux fiches d'une tâche dans le groupe des longs, en file : le groupe compte pour sa plus large (18)
                    ("L3e deux fiches d'un même groupe, en file", {"jamais_meme_groupe_1.yml": fiche(PLACE_I, groupe="longs-commun", file="  queue: max\n"),
                                                                   "jamais_meme_groupe_2.yml": fiche(PLACE_I, groupe="longs-commun", file="  queue: max\n")}, None),
                    # A-896 : un groupe partagé sans file perd une demande en attente (essai réel du 18-11-2026)
                    ("L3g deux fiches d'un même groupe, sans file", {"jamais_meme_groupe_1.yml": fiche(UN, groupe="commun"),
                                                                     "jamais_meme_groupe_2.yml": fiche(UN, groupe="commun", file="  queue: max\n")},
                     "jamais_meme_groupe_1.yml : groupe « commun » partagé par 2 fiches sans « queue: max »"),
                    ("L3h peut attendre dans le réservoir des longs", {"peut_attendre_dans_la_file.yml": fiche(PLACE_I, groupe=None)},
                     "peut_attendre_dans_la_file.yml : classée « peut attendre » mais porte le groupe compté"),
                    # E1 de la relecture de A-896 (superviseur R-759 du 18-11-2026) : la famille « jamais attendre », jamais
                    # un nom ; le vrai circuit du soir mis dans la file des longs → refus ; le soir seul dans son groupe → vert
                    ("L3j jamais attendre dans la file des longs",
                     # étape FILE-2 : une fiche « jamais attendre » dont les jobs prennent une place du réservoir
                     {"jamais_dans_les_places.yml": fiche(PLACE_I, groupe=None)},
                     f"jamais_dans_les_places.yml : classée « {F.JAMAIS_ATTENDRE} » mais partage son groupe"),
                    ("L3k jamais attendre seul dans son groupe", {}, None),
                    # D3 de la relecture de A-884 : la frontière exacte, un de trop (largeur du soir 1, du relais 1 : 21)
                    ("L3i une tâche de trop, exactement", {"jamais_21.yml": fiche(UN, groupe="vingt_et_un")}, "largeur du compte dépassée"),
                    ("L3f famille inconnue", {"famille_inconnue.yml": fiche(UN, groupe="inconnue")}, "famille « plus tard » inconnue")):
                refus, _ = F.refus_de_la_largeur(dict(fabriquees, **ajout))
                if fragment is None and refus:
                    faux.append(f"{nom} : refusée : {refus}")
                elif fragment is not None and not any(fragment in r for r in refus):
                    faux.append(f"{nom} : non refusée pour sa raison ({fragment}) : {refus}")
        finally:
            F.FAMILLES_DES_CIRCUITS_PUBLICS.clear()
            F.FAMILLES_DES_CIRCUITS_PUBLICS.update(familles)
        # ---- L4 : les fiches d'un clone public
        dossier = os.path.join(d, "pub4", ".github", "workflows")
        os.makedirs(dossier)
        for n in ("a.yml", "b.yaml", "c.txt"):
            open(os.path.join(dossier, n), "w", encoding="utf-8").write(n)
        os.makedirs(os.path.join(dossier, "d.yml"))
        if sorted(F.fiches_du_clone_public(os.path.join(d, "pub4"))) != ["a.yml", "b.yaml"] \
                or F.fiches_du_clone_public(os.path.join(d, "absent")) != {}:
            faux.append("L4 fiches_du_clone_public ne rend pas exactement les .yml et .yaml du dossier")
        # ---- L5 : la porte, le fabricant en ligne de commande sur une copie minuscule (sans git)
        mini = os.path.join(d, "mini")
        for f in LUS:
            os.makedirs(os.path.dirname(os.path.join(mini, f)), exist_ok=True)
            shutil.copyfile(os.path.join(racine, f), os.path.join(mini, f))
        essais = [("L5a public neuf", {}, 0, "circuits qui peuvent tourner ensemble sans attendre"),
                  ("L5b public avec une fiche nouvelle non classée", {"nouvelle.yml": fiche(UN, groupe="nouvelle")}, 1,
                   "nouvelle.yml : fiche publique sans famille")]
        if PUBLIC:
            essais.append(("L5c public avec ses fiches posées à la main", a_la_main, 0,
                           "circuits qui peuvent tourner ensemble sans attendre"))
        for k, (nom, posees, code_attendu, fragment) in enumerate(essais):
            pub = os.path.join(d, f"pub5_{k}")
            os.makedirs(os.path.join(pub, ".github", "workflows"))
            for n, t in posees.items():
                open(os.path.join(pub, ".github", "workflows", n), "w", encoding="utf-8").write(t)
            c, o = lancer([sys.executable, "-B", os.path.join(mini, FABRICANT), mini, pub])
            if c != code_attendu or fragment not in o or (code_attendu and "ARRÊT" not in o):
                faux.append(f"{nom} : code {c} au lieu de {code_attendu}, « {fragment} » {'lu' if fragment in o else 'absent'} : "
                            f"{o[-400:]}")
    except Exception as e:   # noqa: BLE001 — une erreur imprévue est un cas faux, jamais un passage
        faux.append(f"erreur imprévue : {type(e).__name__} : {e}")
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return faux


SABOTAGES = {
    # la cible (18, décision de Jean-Luc A-888) peut changer : le sabotage la remplace sans lire sa valeur (19 = la limite moins un)
    "SL1_largeur_cible_19": [(FABRICANT, "\nLARGEUR_DES_CIRCUITS_LONGS = ",
                              "\nLARGEUR_DES_CIRCUITS_LONGS = TACHES_EN_MEME_TEMPS_DU_COMPTE - 1  # ")],
    "SL2_relais_elargi_a_3": [(FABRICANT, "  relayer:\n    runs-on: ubuntu-latest\n",
                               "  relayer:\n    strategy:\n      matrix:\n        n: [1, 2, 3]\n    runs-on: ubuntu-latest\n")],
    "SL3_non_classee_toleree": [(FABRICANT, "        if famille is None:\n            refus.append(",
                                 "        if famille is None:\n            famille = PEUT_ATTENDRE\n        if False:\n            refus.append(")],
    "SL4_largeur_constante": [(FABRICANT, "    return groupe, meilleure\n", "    return groupe, 2\n")],
    # A-896 : la certification remise « peut attendre » (l'état d'avant, défaut D1) dans le groupe des longs → refus
    "SL5_certification_peut_attendre": [(FABRICANT, "    os.path.basename(CIRCUIT_CERTIFICATION): LONGS,",
                                         "    os.path.basename(CIRCUIT_CERTIFICATION): PEUT_ATTENDRE,")],
    "SL6_needs_ignores": [(FABRICANT, "        if any(a in ancetres[b] for a in choisis for b in choisis):\n",
                           "        if False:\n")],
    "SL7_max_parallel_ignore": [(FABRICANT, '                jobs[chemin[1]]["max_parallel"] = int(valeur)\n',
                                 "                pass\n")],
    "SL8_sans_groupe_admis": [(FABRICANT, "            refus.append(f\"{nom} : comptée parmi",
                               "            (lambda *_: None)(f\"{nom} : comptée parmi")],
    "SL9_peut_attendre_compte_quand_meme": [(FABRICANT, "            attente[cle] = max(attente.get(cle, 0), largeur)\n            continue\n",
                                             "            attente[cle] = max(attente.get(cle, 0), largeur)\n")],
    "SL10_porte_retiree": [(FABRICANT, "    refus, lignes = refus_de_la_largeur(fiches_du_clone_public(public))\n",
                            "    refus, lignes = [], []\n")],
    "SL11_matrice_comptee_un": [(FABRICANT, "                taille *= n\n", "                taille = 1\n")],
    "SL12_bloc_lu_comme_des_cles": [(FABRICANT, "            bloc = colonne\n            continue\n        pile.append((colonne, cle))",
                                     "            pass\n        pile.append((colonne, cle))")],
    "SL13_rassembler_sans_borne": [(FABRICANT, "      max-parallel: %(series_au_plus)d\n", "")],
    # A-896, la file unique : la certification dans son ancien groupe (15 + 18 + 1 + 1 > 20)
    # étape FILE-2 : la tranche de la certification hors du réservoir (sa place retirée) : la fiche n'est plus bornée
    "SL14_certification_hors_de_la_file": [(FABRICANT, '%(place_de_la_tranche)s    # 330 minutes PAR TRANCHE', '    # 330 minutes PAR TRANCHE')],
    # « queue: max » retiré de la certification : le groupe partagé n'est plus une file
    "SL15_certification_sans_queue_max": [(FABRICANT, "  queue: max\npermissions:\n  contents: read\njobs:\n  preparer:\n    # LE COMMIT DE LA NUIT",
                                           "permissions:\n  contents: read\njobs:\n  preparer:\n    # LE COMMIT DE LA NUIT")],
    # le contrôle de la file neutralisé
    "SL16_file_non_controlee": [(FABRICANT, "            if file[\"queue\"] != \"max\":\n", "            if False:\n")],
    # la porte des « peut attendre » dans un groupe compté retirée
    "SL17_peut_attendre_dans_la_file_admis": [(FABRICANT, "        if set(groupes_reels(groupe)) & groupes_comptes:\n",
                                               "        if False:\n")],
    # étape FILE-2 (20-11-2026) : le réservoir — compté pour UNE place (la somme oublierait les 17 autres) ; une place
    # non bornée (« ${{ s || … »), une place sans file, 19 places (A-888 en veut 18)
    "SL23_places_comptees_une_fois": [(FABRICANT, "    return NOMS_DES_PLACES if groupe == RESERVOIR_DES_PLACES else (groupe,)",
                                       "    return NOMS_DES_PLACES[:1] if groupe == RESERVOIR_DES_PLACES else (groupe,)")],
    "SL25_place_non_bornee": [(FABRICANT, '''    return "${{ " + "".join("%s == '%d' && '%d' || " % (source, k, k)''',
                               '''    return "${{ " + source + " || " + "".join("%s == '%d' && '%d' || " % (source, k, k)''')],
    "SL26_place_sans_file": [(FABRICANT, '''            + "\\n      cancel-in-progress: false\\n      queue: max\\n")''',
                              '''            + "\\n      cancel-in-progress: false\\n")''')],
    "SL27_dix_neuf_places": [(FABRICANT, "\nPLACES_LONGUES = LARGEUR_DES_CIRCUITS_LONGS\n", "\nPLACES_LONGUES = LARGEUR_DES_CIRCUITS_LONGS + 1\n")],
    # E1 : le refus du partage de groupe d'un « jamais attendre » neutralisé
    "SL19_jamais_attendre_partage_admis": [(FABRICANT, "        if autres:\n", "        if False:\n")],
    # E4 : une entrée du bouton des séries écrite à la main, hors des tuples qui le comptent
    "SL20_entree_hors_du_tuple": [(FABRICANT, "    inputs:\n%(entrees)sconcurrency:",
                                   "    inputs:\n      demande:\n        type: string\n%(entrees)sconcurrency:")],
    # L6, la limite « au plus ENTREES_DU_BOUTON_AU_PLUS » : le calcul de SERIES_AU_PLUS qui ne retire plus les entrées
    # fixes, et onze entrées fixes de plus DANS le tuple (le compte du tuple reste juste) : 14 + 2 × 6 = 26 > 25
    "SL21_bouton_au_dela_de_la_limite": [(FABRICANT, "SERIES_AU_PLUS = (ENTREES_DU_BOUTON_AU_PLUS - len(ENTREES_FIXES_DES_SERIES))",
                                          "SERIES_AU_PLUS = (ENTREES_DU_BOUTON_AU_PLUS - 0)"),
                                         (FABRICANT, '    ("nombre_de_places", CORPS_DE_L_ENTREE_NOMBRE_DE_PLACES))\n',
                                          '    ("nombre_de_places", CORPS_DE_L_ENTREE_NOMBRE_DE_PLACES)) + tuple(("x%d" % i, "        type: string\\n") for i in range(11))\n')],
    # étape FILE-2 : la protection fine — le groupe de passage des épreuves retiré (deux passages d'une même branche
    # tourneraient ensemble), nommé par le passage au lieu de la branche (aucune protection), ou sans file
    "SL18_epreuves_sans_groupe_de_passage": [(FABRICANT, '"groupe": GROUPE_DES_EPREUVES,', '"groupe": "",')],
    "SL28_groupe_par_passage": [(FABRICANT, 'GROUPE_DES_EPREUVES = "epreuves-longues-${{ github.ref_name }}"',
                                 'GROUPE_DES_EPREUVES = "epreuves-longues-${{ github.run_id }}"')],
}


def main():
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Fiche en tête. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — Fiche en tête.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1]
    ⑥ TRAITEMENT — un tour tel quel ; avec --saboter (ou --saboter=SL1,…), une copie des fichiers LUS par sabotage, le
      fichier visé écrit saboté, un tour par copie.
    ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Fiche en tête.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    faux = tour(DEPOT)
    print("Z0 programmes tels quels : " + ("L0 à L7 conformes" if not faux else "FAUX " + " | ".join(faux)))
    for n in dict.fromkeys(NOTES):
        print("NOTE " + n)
    code = 1 if faux else 0
    choix = [a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--saboter=")]
    if "--saboter" in sys.argv or choix:
        for nom in [n for n in SABOTAGES if not choix or n in choix[0] or n.split("_")[0] in choix[0]]:
            d = tempfile.mkdtemp(prefix="largeur_sab_")
            try:
                for f in LUS:
                    os.makedirs(os.path.dirname(os.path.join(d, f)), exist_ok=True)
                    shutil.copyfile(os.path.join(DEPOT, f), os.path.join(d, f))
                for fichier, a, b in SABOTAGES[nom]:
                    t = open(os.path.join(d, fichier), encoding="utf-8").read()
                    if t.count(a) != 1:
                        print(f"{nom} NE S'APPLIQUE PLUS : texte cible trouvé {t.count(a)} fois dans {fichier}")
                        return 2
                    open(os.path.join(d, fichier), "w", encoding="utf-8").write(t.replace(a, b))
                f = tour(d)
            finally:
                shutil.rmtree(d, ignore_errors=True)
            print(f"{nom} {'mord' if f else 'NE MORD PAS'} : {f[:3]}")
            code |= 0 if f else 1
    print("VERDICT : tout est conforme" if code == 0 else "VERDICT : NON CONFORME")
    return code


if __name__ == "__main__":
    sys.exit(main())
