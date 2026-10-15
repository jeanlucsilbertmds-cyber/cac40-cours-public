"""EPREUVES_DES_AJUSTEMENTS_DE_YAHOO_Jeu_08-10-2026.py — Jeu 08-10-2026 (Paris) — épreuves d'un outil d'étude.

① RÔLE — Prouver que etudes/outils/MESURER_LES_AJUSTEMENTS_DE_YAHOO.py a des dents : chaque sabotage du code, et
  chaque verdict retiré ou faussé, doit lui faire rendre un code non nul.
② CONTEXTE D'APPEL — À la main : python3 -I tests/EPREUVES_DES_AJUSTEMENTS_DE_YAHOO_Jeu_08-10-2026.py <racine>
  <dossier des réponses de Yahoo> <fichier de résultats>.
③ ENTRÉE — Trois arguments : la racine du dépôt, le dossier où l'outil garde les réponses de Yahoo, le chemin du
  relevé à écrire.
④ CONDITIONS D'ENTRÉE — Le dossier des réponses de Yahoo est complet (39 fichiers) : sinon l'outil irait sur le réseau.
⑤ SORTIE — AUCUNE valeur rendue : le relevé est écrit et affiché ; une cible de sabotage introuvable lève
  AssertionError.
⑥ TRAITEMENT — ① une COPIE du dépôt, sans .git ni archives, dans un dossier temporaire (l'outil écrit
  donnees/sources_yahoo/EVENEMENTS_YAHOO.csv : il ne tourne jamais sur le dépôt) · ② l'outil tel quel · ③ chaque
  sabotage du code de `SAB`, sur une copie de l'outil · ④ chaque sabotage du fichier des verdicts de `VER`, et R1
  (le fichier réparé d'avant la correction du 08-10-2026), le fichier étant remis en état après chacun · ⑤ chaque contre-épreuve de `CONTRE` · ⑥ noter chaque
  code de sortie.
⑦ UNITÉ — Des CODES DE SORTIE.
⑧ POURQUOI — Un jeu d'épreuves se sabote contre sa propre correction : un calibrage qui reste vert quand on retire
  ce qu'il teste n'est pas une preuve (R-731). Le relevé est écrit par le programme, jamais à la main (R-728).
⑨ CE QUI CLOCHE — Les sabotages portent sur les seuils, le témoin officiel, l'explication par les divisions
  déclarées, le jugement du pont et la preuve des corrections ; la lecture des réponses de Yahoo et l'écriture
  d'EVENEMENTS_YAHOO.csv n'en ont pas. · Retirer la vérification finale, relâcher le jugement du pont ou retirer la
  preuve des corrections ne mord pas sur les vrais fichiers (ils sont justes) : ce sont les contre-épreuves C1 à C4
  qui les éprouvent, en les jouant sur un verdict faux (V1, V3, V5) ou sur le fichier réparé d'avant la correction (R1).
⑩ EFFET — Écrit le relevé ; écrit une copie du dépôt dans un dossier temporaire.
⑪ TERMINAISON — Un lancement de l'outil par épreuve, chacun fini (aucun appel réseau, réponses gardées).
  [sort: non]
"""
import csv, datetime, io, os, shutil, subprocess, sys, tempfile, zoneinfo

racine, travail, sortie = sys.argv[1], os.path.abspath(sys.argv[2]), sys.argv[3]
OUTIL = "etudes/outils/MESURER_LES_AJUSTEMENTS_DE_YAHOO.py"
VERDICTS = "donnees/sources_yahoo/AJUSTEMENTS_DE_YAHOO.csv"
SAB = {"S1 marche décuplée (Essilor 2024 n'est plus vue)": ("MARCHE = 0.005 ", "MARCHE = 0.05 "),
       "S2 écart de baisse à 10 incertitudes (Crédit Agricole 2018 n'est plus vue)": ("ECARTS = 3 ", "ECARTS = 10 "),
       "S3 témoin : dernière séance du fichier au lieu du dernier jour ouvré":
           ("x[fin][3] / c if fin in x else None", "x[max(x)][3] / c"),
       "S4 aucune marche expliquée par une division déclarée":
           ("    non = [c for c in marches if abs((1 + c[3]) / c[5] - 1) > MARCHE]", "    non = marches"),
       "S5 toute marche expliquée, même sans division":
           ("    non = [c for c in marches if abs((1 + c[3]) / c[5] - 1) > MARCHE]",
            "    non = [c for c in marches if abs((1 + c[3]) / c[5] - 1) > 10]"),
       "S6 le pont ignore les divisions déclarées": ("                declare *= k\n        cas.append((v, z / a",
                                                     "                pass\n        cas.append((v, z / a"),
}
# Une contre-épreuve joue un sabotage des verdicts AVEC un sabotage du code : elle doit rendre 0, ce qui prouve que
# l'épreuve des verdicts mord grâce à la ligne sabotée, et non par accident.
PONT_LACHE = ('\n                              and x["ce_que_yahoo_declare"].startswith("aucune déclaration") for x in verdicts)',
              " for x in verdicts)")
CORRECTIONS_MUETTES = ("    if faux:\n        return 1\n", "    if False:\n        return 1\n")
CONTRE = {"C1 V3 joué avec un pont jugé par n'importe quelle ligne de la valeur": (PONT_LACHE, "V3"),
          "C2 V1 joué avec la vérification finale retirée": (("    return 1 if sans else 0", "    return 0"), "V1"),
          "C3 V5 joué avec la preuve des corrections retirée": (CORRECTIONS_MUETTES, "V5"),
          "C4 R1 joué avec la preuve des corrections retirée": (CORRECTIONS_MUETTES, "R1"),
          # 09-10-2026 : une correction défaite remplacée par une opération déclarée le même jour (Accor 2010) n'est
          # « plus vue » QUE si la marche restante est celle de l'opération ; R2 mord grâce à cette comparaison
          "C5 R2 joué avec n'importe quelle marche acceptée en remplacement":
              (("if len(vue) == 1 and abs((1 + vue[0]) / (1 + permise) - 1) <= FACTEUR:",
                "if len(vue) == 1 and abs((1 + vue[0]) / (1 + permise) - 1) <= 10:"), "R2")}
VER = {"V1 verdict de Carrefour 11-04-2000 retiré": ("CARREFOUR,2000-04-11,", None),
       "V2 verdict d'EssilorLuxottica daté d'un autre jour": ("ESSILORLUXOTTICA,2024-05-06,", "ESSILORLUXOTTICA,2024-05-07,"),
       "V3 verdict d'Euronext 2021 marqué comme déclaré": ("EURONEXT,2021-04-30,aucune déclaration", "EURONEXT,2021-04-30,division"),
       "V4 en-tête du fichier des verdicts faussé": ("valeur,date,ce_que_yahoo_declare,", "valeur,jour,ce_que_yahoo_declare,"),
       "V5 facteur à défaire d'EssilorLuxottica faux de 0,5 %": (",184.07/180.12", ",185.00/180.12")}
REPARE = "donnees/sources_yahoo/historique_long_repare.csv"
R1 = "R1 fichier réparé tel qu'avant la correction (les facteurs de Yahoo défaits remis)"
# Accor avant le 02-07-2010 ajustée avec le prix technique d'Euronext (11,40 €) au lieu de l'ouverture d'Edenred
# déclarée (13,00 €) : la marche restante (+44,3 %) n'est plus celle de l'opération déclarée (+53,9 %)
R2 = "R2 Accor 2010 ajustée avec une autre valeur d'Edenred que celle déclarée"

copie = os.path.join(tempfile.mkdtemp(), "depot")
shutil.copytree(racine, copie, ignore=shutil.ignore_patterns(".git", "archives"))
texte = open(os.path.join(copie, OUTIL), encoding="utf-8").read()
verdicts = open(os.path.join(copie, VERDICTS), encoding="utf-8").read()
repare = open(os.path.join(copie, REPARE), encoding="utf-8").read()
sys.path.insert(0, os.path.join(copie, "programmes"))
import CONTROLER_L_HISTORIQUE_LONG as K          # la lecture des facteurs, jamais recopiée (R-708)


def lancer(code_outil):
    """Écrit `code_outil` à la place de l'outil dans la copie, le lance, rend son code de sortie.

    ① RÔLE — Une épreuve. ② CONTEXTE D'APPEL — La boucle du programme. ③ ENTRÉE — `code_outil` : le texte de l'outil.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le code de sortie. [rend: 1] ⑥ TRAITEMENT — Écrire, lancer.
    ⑦ UNITÉ — Un CODE. ⑧ POURQUOI — L'outil importe programmes/ par un chemin relatif à lui-même : la copie le garde.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit l'outil dans la copie ; l'outil écrit EVENEMENTS_YAHOO.csv dans la copie.
    ⑪ TERMINAISON — L'outil lit les réponses gardées. [sort: non]
    """
    open(os.path.join(copie, OUTIL), "w", encoding="utf-8").write(code_outil)
    return subprocess.run([sys.executable, "-I", os.path.join(copie, OUTIL), copie, travail],
                          capture_output=True, cwd=copie).returncode


lignes = [f"# Épreuves de {OUTIL}, jouées sur une copie du dépôt le "
          f"{datetime.datetime.now(zoneinfo.ZoneInfo('Europe/Paris')):%d-%m-%Y à %Hh%M} (Paris) par un programme.",
          "# Un sabotage mord quand le code de sortie n'est plus 0."]
lignes.append(f"Z0 outil tel quel, verdicts tels quels : code {lancer(texte)}")
for nom, (a, b) in SAB.items():
    assert texte.count(a) == 1, nom
    code = lancer(texte.replace(a, b))
    lignes.append(f"{nom} : code {code} — {'mord' if code else 'NE MORD PAS'}")


def faux_verdicts(cle):
    """Rend le texte du fichier des verdicts saboté par l'épreuve de `VER` dont le nom commence par `cle`.

    ① RÔLE — Fabriquer un verdict manquant ou faux. ② CONTEXTE D'APPEL — Les boucles du programme.
    ③ ENTRÉE — `cle` : « V1 », « V2 »… ④ CONDITIONS D'ENTRÉE — La cible existe une fois.
    ⑤ SORTIE — UNE valeur : le texte. [rend: 1] ⑥ TRAITEMENT — Retirer la ligne, ou remplacer le texte.
    ⑦ UNITÉ — — ⑧ POURQUOI — Les épreuves et les contre-épreuves partagent le même sabotage. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    a, b = next(v for k, v in VER.items() if k.startswith(cle + " "))
    assert verdicts.count(a) == 1, cle
    if b is None:
        return "".join(l for l in verdicts.splitlines(keepends=True) if not l.startswith(a))
    return verdicts.replace(a, b)




def repare_d_avant():
    """Rend le texte du fichier réparé où chaque ajustement défait est remis : les erreurs de Yahoo reviennent.

    ① RÔLE — Fabriquer le fichier réparé d'avant la décision du 08-10-2026. ② CONTEXTE D'APPEL — `saboter_donnees`.
    ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le texte. [rend: 1]
    ⑥ TRAITEMENT — Chaque ligne d'une valeur à défaire, d'avant sa date : prix ÷ facteur, volume × facteur.
    ⑦ UNITÉ — — ⑧ POURQUOI — L'outil doit refuser un fichier réparé qui garde les erreurs. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    a_def = K.lire_a_defaire(os.path.join(copie, VERDICTS))
    sortie_ = io.StringIO()
    w = csv.writer(sortie_, lineterminator="\n")
    for l in csv.reader(io.StringIO(repare)):
        for v, d, f in a_def:
            if l[0] == v and l[1] < d:
                l = l[:2] + [repr(float(x) / f) for x in l[2:6]] + [repr(float(l[6]) * f)] + l[7:]
        w.writerow(l)
    return sortie_.getvalue()


def accor_autre_valeur():
    """Rend le texte du fichier réparé où Accor, avant le 02-07-2010, porte l'ajustement d'Edenred à 11,40 € au lieu de 13,00 €.

    ① RÔLE — Fabriquer le cas R2. ② CONTEXTE D'APPEL — `saboter_donnees`. ③ ENTRÉE — —. ④ CONDITIONS D'ENTRÉE — Le
    fichier réparé de la copie porte Accor 2010 ajustée à 13,00 € (décision de Jean-Luc du 09-10-2026 à 21h00).
    ⑤ SORTIE — UNE valeur : le texte. [rend: 1] ⑥ TRAITEMENT — Les quatre prix d'Accor d'avant le 02-07-2010
    × (37,125 − 11,40) ÷ (37,125 − 13,00), le volume ÷ ce nombre. ⑦ UNITÉ — — ⑧ POURQUOI — Une valeur distribuée
    fausse laisse dans le fichier une marche qui n'est pas celle de l'opération déclarée : l'outil doit la voir.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    g = (37.125 - 11.40) / (37.125 - 13.00)
    sortie_ = io.StringIO()
    w = csv.writer(sortie_, lineterminator="\n")
    for l in csv.reader(io.StringIO(repare)):
        if l[0] == "ACCOR" and l[1] < "2010-07-02":
            l = l[:2] + [repr(float(x) * g) for x in l[2:6]] + [repr(float(l[6]) / g)] + l[7:]
        w.writerow(l)
    return sortie_.getvalue()


def saboter_donnees(cle):
    """Écrit dans la copie le fichier saboté par `cle` ; rend la fonction qui le remet en état.

    ① RÔLE — Un seul geste pour les sabotages des verdicts et du fichier réparé. ② CONTEXTE D'APPEL — Les boucles.
    ③ ENTRÉE — `cle` : « V1 »… « V5 », ou « R1 ». ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la fonction.
    [rend: 1] ⑥ TRAITEMENT — Écrire. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit dans la copie.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    chemin, original, faux = ((os.path.join(copie, REPARE), repare, repare_d_avant()) if cle == "R1" else
                              (os.path.join(copie, REPARE), repare, accor_autre_valeur()) if cle == "R2" else
                              (os.path.join(copie, VERDICTS), verdicts, faux_verdicts(cle)))
    open(chemin, "w", encoding="utf-8").write(faux)
    return lambda: open(chemin, "w", encoding="utf-8").write(original)


for nom in list(VER) + [R1, R2]:
    remettre = saboter_donnees(nom.split()[0])
    code = lancer(texte)
    remettre()
    lignes.append(f"{nom} : code {code} — {'mord' if code else 'NE MORD PAS'}")
for nom, ((a, b), cle) in CONTRE.items():
    assert texte.count(a) == 1, nom
    remettre = saboter_donnees(cle)
    code = lancer(texte.replace(a, b))
    remettre()
    lignes.append(f"{nom} : code {code} — {'contre-épreuve confirmée' if code == 0 else 'CONTRE-ÉPREUVE ÉCHOUÉE'}")
lignes.append(f"Z1 outil et verdicts remis en état : code {lancer(texte)}")
open(sortie, "w", encoding="utf-8").write("\n".join(lignes) + "\n")
print("\n".join(lignes))
shutil.rmtree(os.path.dirname(copie))
