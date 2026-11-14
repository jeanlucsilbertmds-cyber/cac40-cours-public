#!/usr/bin/env python3
"""ÉPREUVES DE LA NUMÉROTATION DES SOCIÉTÉS SORTIES — Plan V7, E2a tour 3 (12-11-2026). SIMULATION UNIQUEMENT.

① RÔLE — Éprouver etudes/VINGT_ANS_A_PART_Mer_11-11-2026/NUMEROTER_LES_SOCIETES_SORTIES.py, et, avec --saboter,
  vérifier que chaque garde retirée fait tomber au moins un cas.
② CONTEXTE D'APPEL — `python3 -I <ce fichier> <racine> [--saboter]`, à la main ou par le relais des séries.
③ ENTRÉE — La racine du dépôt (le programme éprouvé, LIRE_LES_COURS et les vraies tables y sont lus, jamais écrits).
④ CONDITIONS D'ENTRÉE — Les tables existent. N1, N3, N7 et N9 partent des tables D'AVANT la numérotation,
  RECONSTRUITES depuis les tables vivantes par `tables_d_origine` (lignes d'identité de numéro ≥ PREMIER_NUMERO
  retirées, leurs mnémoniques ramenés à leur ISIN dans la liste des taxes) : aucune dépendance à git, l'épreuve tourne
  aussi dans une copie sans .git (le rejeu du contrôle de livraison).
⑤ SORTIE — Le code de sortie : 0 si tous les cas passent (et, avec --saboter, si chaque sabotage mord) ; 1 sinon ;
  2 si un sabotage ne s'applique plus. [rend: 1]
⑥ TRAITEMENT — N1 vraie ligne (Alcatel, FR0000130007 : ALU, 2000-01-03 → 2016-01-06, numéro ≥ 41 ; 39 lignes,
  38 numéros) · N2 Alstom : ses deux codes ont le même numéro · N3 la vraie liste des taxes : 216 cases remplacées,
  plus aucun ISIN en deuxième colonne, toute autre ligne identique à l'octet, fins de ligne gardées · N4 un passage
  encore ouvert est refusé · N5 un mnémonique sourcé déjà porté par une autre société est refusé · N6 un ISIN de la
  liste sans mnémonique, ou avec deux, est refusé · N7 écriture sur une copie minimale : code 0, puis relancé « rien à
  faire », code 0 · N8 une table dont le plus grand numéro est 5 commence quand même à 41 · N9 le programme appliqué
  aux tables reconstruites redonne, à l'octet, les tables vivantes (si elles portent déjà les numéros).
⑦ UNITÉ — Des codes de sortie.
⑧ POURQUOI — R-731 (tout code écrit passe des épreuves sabotées) ; R-732 (un cas vient d'une vraie ligne : N1, N3).
⑨ CE QUI CLOCHE — La branche « rendu du lecteur unique changé → fichiers remis à l'identique » n'est pas éprouvée :
  aucune ligne écrite par le programme n'a de fin vide, le lecteur ne peut donc pas changer d'avis sans sabotage du
  lecteur lui-même. · La reconstruction suppose que les numéros ≥ 41 ne viennent que de ce programme : une ligne
  ajoutée à la main sous un tel numéro serait retirée à tort, et N9 rougirait.
⑩ EFFET — Des dossiers jetables, effacés à la fin.
⑪ TERMINAISON — Rend la main ; sort par sys.exit. Le lancement de N7 est borné à 120 secondes. [sort: oui]
"""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile

RACINE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else os.getcwd()
OUTIL = os.path.join(RACINE, "etudes", "VINGT_ANS_A_PART_Mer_11-11-2026", "NUMEROTER_LES_SOCIETES_SORTIES.py")
sys.path.insert(0, os.path.join(RACINE, "programmes"))
import LIRE_LES_COURS as LECTEUR  # noqa: E402

SABOTAGES = {
    "S1_passage_ouvert_admis": [('        if not p["derniere_seance"]:\n', "        if False:\n")],
    "S2_mnemonique_double_admis": [("        if m and pris.setdefault(mnemo, n) != n:\n", "        if False:\n")],
    "S3_deux_mnemoniques_admis": [("            if len(m) != 1:\n", "            if not m:\n")],
    "S4_taxe_non_remplacee": [("                cases[1] = next(iter(m))\n", "                pass\n")],
    "S5_meme_societe_ignoree": [('        cible = autre if autre in sejours else code\n', "        cible = code\n")],
    "S6_fin_de_ligne_perdue": [("        fin = ligne[len(corps):]\n", '        fin = "\\n"\n')],
    "S7_premier_numero_ignore": [(" + [PREMIER_NUMERO - 1]", "")],
    # tour 4 (D2) : le nom corrigé ignoré, le libellé bnains tronqué revient (N9 doit rougir)
    "S8_nom_corrige_ignore": [('        nom = nm["nom"] if nm else libelle[code]\n', "        nom = libelle[code]\n")],
}


def charger(chemin):
    """Charge le programme éprouvé comme module.

    ① RÔLE — Import par chemin. ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — `chemin`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le module. [rend: 1] ⑥ TRAITEMENT — importlib. ⑦ UNITÉ — — ⑧ POURQUOI — éprouver une
    copie sabotée sans toucher l'original. ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    spec = importlib.util.spec_from_file_location("numeroter_eprouve", chemin)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


F_ID = "donnees/sources_indice/IDENTITES_DES_SOCIETES.csv"
F_TTF = "donnees/VALEURS_TTF.csv"


def tables_d_origine(premier):
    """Reconstruit les deux tables d'avant la numérotation, depuis les tables vivantes.

    ① RÔLE — Donner à N1, N3, N7 et N9 les vraies lignes d'origine sans git.
    ② CONTEXTE D'APPEL — `tour`.
    ③ ENTRÉE — `premier` : le premier numéro attribué par le programme (son PREMIER_NUMERO).
    ④ CONDITIONS D'ENTRÉE — Les deux tables vivantes existent.
    ⑤ SORTIE — DEUX valeurs : les octets des identités d'origine, ceux de la liste des taxes d'origine. [rend: 2]
    ⑥ TRAITEMENT — ① identités : retirer chaque ligne dont le numéro est ≥ `premier`, octets des autres lignes gardés ·
      ② taxes : dans chaque ligne dont la deuxième case est le mnémonique (hors « non trouvé ») d'une ligne retirée,
      remettre l'ISIN de cette ligne ; fins de ligne gardées.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le contrôle de livraison rejoue l'épreuve dans une copie SANS .git : la version précédente, qui lisait
      les tables d'origine par `git show`, y tombait (12-11-2026).
    ⑨ CE QUI CLOCHE — Fiche en tête, ⑨.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    import csv
    ident = open(os.path.join(RACINE, F_ID), "rb").read().decode("utf-8")
    gardees, isin_de = [], {}
    for ligne in ident.splitlines(keepends=True):
        r = next(csv.reader([ligne]), [])
        if r and r[0].isdigit() and int(r[0]) >= premier:
            if r[5] and r[5] != "non trouvé":
                isin_de[r[5]] = r[6]
            continue
        gardees.append(ligne)
    sortie = []
    for ligne in open(os.path.join(RACINE, F_TTF), "rb").read().decode("utf-8").splitlines(keepends=True):
        c = ligne.split(",", 2)
        if len(c) == 3 and not ligne.startswith("#") and c[1] in isin_de:
            c[1] = isin_de[c[1]]
            ligne = ",".join(c)
        sortie.append(ligne)
    return "".join(gardees).encode("utf-8"), "".join(sortie).encode("utf-8")


def lignes_csv(octets):
    """Lit des octets CSV en lignes-dictionnaires. ① RÔLE — aide. ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — octets.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la liste. [rend: 1] ⑥ TRAITEMENT — csv.DictReader.
    ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    import csv
    import io
    return list(csv.DictReader(io.StringIO(octets.decode("utf-8-sig"))))


def tour(outil):
    """Joue N1 à N9 sur le programme `outil` ; rend la liste des cas faux.

    ① RÔLE — Un tour. ② CONTEXTE D'APPEL — `main`, tel quel puis par sabotage. ③ ENTRÉE — chemin du programme.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : liste de noms de cas faux. [rend: 1] ⑥ TRAITEMENT — fiche en
    tête, ⑥. ⑦ UNITÉ — — ⑧ POURQUOI — fiche en tête. ⑨ CE QUI CLOCHE — fiche en tête. ⑩ EFFET — dossier jetable.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    faux = []
    T = charger(outil)
    ok = LECTEUR.isin_valide
    o_id, o_ttf = tables_d_origine(T.PREMIER_NUMERO)
    ident = lignes_csv(o_id)
    passages = lignes_csv(open(os.path.join(RACINE, LECTEUR.PASSAGES), "rb").read())
    mnemos = {r["isin"]: r for r in lignes_csv(open(T.MNEMOS, "rb").read())}
    groupes = {r["isin"]: r for r in lignes_csv(open(T.GROUPES, "rb").read())}
    nouv, refus = T.plan_des_numeros(ident, passages, mnemos, groupes, ok)
    alc = [r for r in nouv if r["isin"] == "FR0000130007"]
    if refus or len(nouv) != 39 or len({r["numero"] for r in nouv}) != 38 or len(alc) != 1 \
            or (alc[0]["mnemonique"], alc[0]["debut"], alc[0]["fin"]) != ("ALU", "2000-01-03", "2016-01-06") \
            or int(alc[0]["numero"]) < 41:
        faux.append("N1")
    alst = {r["numero"] for r in nouv if r["isin"] in ("FR0000120198", "FR0010220475")}
    if len(alst) != 1:
        faux.append("N2")
    ttf = o_ttf
    sortie, n, r3 = T.ramener_la_taxe(ttf, ident + nouv, ok)
    a, b = ttf.split(b"\n"), sortie.split(b"\n")
    autres_egales = len(a) == len(b) and all(x == y for x, y in zip(a, b) if not any(ok(c) for c in x.decode().split(",")[1:2]))
    reste = [l for l in sortie.decode().splitlines() if ok((l.split(",") + ["", ""])[1])]
    fins = [x.endswith(b"\r") for x in a] == [y.endswith(b"\r") for y in b]
    if r3 or n != 216 or reste or not autres_egales or not fins:
        faux.append("N3")
    base_id = [{"numero": "1", "societe": "A", "debut": "", "fin": "", "nom_cote": "A", "mnemonique": "AA",
                "isin": "FR0000120404", "preuve": "", "etat": ""}]
    p_ouvert = [{"isin_bnains": "FR0000130007", "libelle_bnains": "X", "premiere_seance": "2000-01-03",
                 "derniere_seance": ""}]
    if not T.plan_des_numeros(base_id, p_ouvert, {}, {}, ok)[1]:
        faux.append("N4")
    p_ferme = [dict(p_ouvert[0], derniere_seance="2001-01-03")]
    m_double = {"FR0000130007": {"isin": "FR0000130007", "mnemonique": "AA", "source": "s", "citation": "c",
                                 "lu_le": "d"}}
    if not T.plan_des_numeros(base_id, p_ferme, m_double, {}, ok)[1]:
        faux.append("N5")
    sans = "annee,mnemonique,nom_usuel\r\n2012,FR0000130007,X\r\n".encode()
    deux = base_id + [dict(base_id[0], numero="2", isin="FR0000130007", mnemonique="B1"),
                      dict(base_id[0], numero="2", isin="FR0000130007", mnemonique="B2")]
    if not T.ramener_la_taxe(sans, base_id, ok)[2] or not T.ramener_la_taxe(sans, deux, ok)[2]:
        faux.append("N6")
    cinq = [dict(base_id[0], numero="5")]
    n8 = T.plan_des_numeros(cinq, p_ferme, {}, {}, ok)[0]
    if not n8 or n8[0]["numero"] != "41":
        faux.append("N8")
    d = tempfile.mkdtemp(prefix="E2a_num_")
    try:
        for rel in ("programmes/LIRE_LES_COURS.py", "programmes/CONTRATS_DES_FICHIERS.py", LECTEUR.PASSAGES):
            os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
            shutil.copy(os.path.join(RACINE, rel), os.path.join(d, rel))
        open(os.path.join(d, F_ID), "wb").write(o_id)
        open(os.path.join(d, F_TTF), "wb").write(o_ttf)
        for rel in os.listdir(os.path.join(RACINE, "programmes")):     # les modules que les deux lecteurs importent
            if rel.endswith(".py") and not os.path.exists(os.path.join(d, "programmes", rel)):
                shutil.copy(os.path.join(RACINE, "programmes", rel), os.path.join(d, "programmes", rel))
        k1 = subprocess.run([sys.executable, "-I", outil, d, "--ecrire"], capture_output=True, text=True, timeout=120)
        k2 = subprocess.run([sys.executable, "-I", outil, d, "--ecrire"], capture_output=True, text=True, timeout=120)
        if k1.returncode != 0 or "FINI écrit" not in k1.stdout or k2.returncode != 0 or "rien à faire" not in k2.stdout:
            faux.append(f"N7 ({k1.returncode}, {k2.returncode} : {(k1.stdout + k1.stderr)[-200:]!r})")
        vivant_id = open(os.path.join(RACINE, F_ID), "rb").read()
        if vivant_id != o_id and (open(os.path.join(d, F_ID), "rb").read() != vivant_id
                                  or open(os.path.join(d, F_TTF), "rb").read() != open(os.path.join(RACINE, F_TTF), "rb").read()):
            faux.append("N9 (le programme appliqué aux tables reconstruites ne redonne pas les tables vivantes)")
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return faux


def main():
    """Tel quel, puis chaque sabotage dans une copie. ① RÔLE — fiche en tête. ② CONTEXTE D'APPEL — ligne de commande.
    ③ ENTRÉE — sys.argv. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le code. [rend: 1] ⑥ TRAITEMENT — fiche
    en tête. ⑦ UNITÉ — — ⑧ POURQUOI — fiche en tête. ⑨ CE QUI CLOCHE — — ⑩ EFFET — dossiers jetables.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    faux = tour(OUTIL)
    print("Z0 programme tel quel : " + ("N1 à N9 conformes" if not faux else "FAUX " + ", ".join(faux)))
    code = 1 if faux else 0
    if "--saboter" in sys.argv:
        texte = open(OUTIL, encoding="utf-8").read()
        for nom, remplacements in SABOTAGES.items():
            t = texte
            for cible, rempl in remplacements:
                if t.count(cible) != 1:
                    print(f"{nom} NE S'APPLIQUE PLUS : texte cible trouvé {t.count(cible)} fois")
                    return 2
                t = t.replace(cible, rempl)
            d = tempfile.mkdtemp(prefix="E2a_sab_")
            try:
                copie = os.path.join(d, os.path.basename(OUTIL))
                open(copie, "w", encoding="utf-8").write(t)
                for f in ("MNEMONIQUES_DES_SOCIETES_SORTIES.csv", "ISIN_D_UNE_MEME_SOCIETE.csv",
                          "NOMS_DES_SOCIETES_SORTIES.csv"):
                    shutil.copy(os.path.join(os.path.dirname(OUTIL), f), os.path.join(d, f))
                tombes = tour(copie)
            finally:
                shutil.rmtree(d, ignore_errors=True)
            print(f"{nom} {'mord' if tombes else 'NE MORD PAS'} : {tombes}")
            code = code or (0 if tombes else 1)
        print("VERDICT : " + ("tout est conforme" if code == 0 else "NON CONFORME"))
    sys.exit(code)


if __name__ == "__main__":
    main()
