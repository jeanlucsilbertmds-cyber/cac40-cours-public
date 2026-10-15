#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_REFERENTIEL_DE_LA_MESURE — Mer 30-09-2026 (Paris)
Rôle : prouver que la mesure de la performance (programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py)
trouve le référentiel des valeurs là où il vit, et que chaque épreuve a des dents.
Quand l'appeler : avant toute livraison qui touche `charger_referentiel` (R-755 ②).

À QUOI ÇA SERT. Le référentiel des valeurs (donnees/REFERENTIEL_VALEURS_*.csv) relie le nom d'une entreprise à
son code de bourse, par exemple BUREAU_VERITAS à BVI. La mesure s'en sert pour vérifier que chaque opération
porte sur une valeur de l'univers autorisé de sa stratégie. Elle le cherchait à la racine du dépôt, où il n'est
pas : chaque soir, « referentiel introuvable », puis une fausse alerte « HORS UNIVERS » sur Bureau Veritas et
Unibail, qui sont pourtant dans l'univers (A-495 (d), travail de nuit du 30-09-2026 demandé par Jean-Luc).

LES ÉPREUVES, chacune sur une copie du dépôt :
E1 sur la copie telle quelle, la table relie BUREAU_VERITAS à BVI et UNIBAIL_RODAMCO à URW ;
E2 un référentiel plus récent posé dans archives/, qui relie BUREAU_VERITAS à XXX, est ignoré ;
E3 deux référentiels dans donnees/, le plus récent par la date de son nom l'emporte (il relie BUREAU_VERITAS à
   YYY) ;
E4 le chemin réel : la mesure lancée sur la copie écrit « referentiel : … valeurs connues » et aucune alerte
   « HORS UNIVERS » sur BUREAU_VERITAS ni UNIBAIL_RODAMCO ;
E5 un référentiel plus récent dont l'extension est « .CSV » en majuscules est ignoré ;
E2, E3 et E5 passent aussi par la collecte du soir (programmes/COLLECTER_ABC_GITHUB.py, `lire_referentiel`) : les
   deux programmes lisent le même fichier, et chacune de ces épreuves exige qu'ils choisissent le même (relecteurs
   du 30-09-2026).
LES SABOTAGES : S1 remet la recherche à la racine (E1, E4) · S2 cherche dans toute l'arborescence, archives
comprises (E2) · S3 prend le premier par l'alphabet au lieu du plus récent (E3) · S4 accepte l'extension sans
tenir compte de la casse (E5) · S5 fait accepter « .CSV » à la collecte seule (E5).

USAGE : python3 tests/EPREUVES_DU_REFERENTIEL_DE_LA_MESURE_Mer_30-09-2026.py <racine du dépôt> [--saboter]
CODE : 0 si les épreuves sont vertes sans sabotage et, avec --saboter, si chaque sabotage fait rougir au moins
une épreuve ; 1 sinon ; 2 si un sabotage ne s'applique plus (ancre absente).
"""
import importlib.util, os, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
MES = "programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py"
COL = "programmes/COLLECTER_ABC_GITHUB.py"
SABOTAGES = {
    "Z0": [],
    "S1_a_plat": [(MES, '    d = os.path.join(base, "donnees")\n', '    d = base\n')],
    "S2_archives_lues": [(MES, "    cands = [f for f in (os.listdir(d) if os.path.isdir(d) else [])",
                          "    cands = [f for f in [os.path.join(a, x) for a, _s, xs in os.walk(base) for x in xs]"),
                         (MES, '             if f.upper().startswith("REFERENTIEL_VALEURS")',
                          '             if os.path.basename(f).upper().startswith("REFERENTIEL_VALEURS")')],
    "S4_extension_sans_casse": [(MES, 'and f.endswith(".csv")]', 'and f.lower().endswith(".csv")]')],
    "S3_le_plus_ancien": [(MES, "[os.path.join(d, le_plus_recent(cands))]", "[os.path.join(d, sorted(cands)[0])]")],
    # S5 (relecteur du 30-09-2026) : la COLLECTE accepte l'extension sans tenir compte de la casse ; la mesure non.
    "S5_collecte_sans_casse": [(COL, 'and f.endswith(".csv")]', 'and f.lower().endswith(".csv")]')],
}


def charger(r):
    """Importe la mesure de la copie `r` et rend le module.

    ① RÔLE — appeler la vraie fonction, jamais une copie de sa recherche (R-708).
    ② CONTEXTE D'APPEL — `epreuves`, une fois.
    ③ ENTRÉE — `r` : la racine d'une copie du dépôt.
    ④ CONDITIONS D'ENTRÉE — le programme doit s'importer sans lancer sa fonction principale.
    ⑤ SORTIE — UNE valeur : le module, dont on emploie `charger_referentiel` et `_norm`.
      [rend: 1]
    ⑥ TRAITEMENT — importer le fichier de la copie sous un nom neuf.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — le chemin réel, dans la copie sabotée.
    ⑨ CE QUI CLOCHE — `COMMUN` est importé par la fonction depuis le dossier du programme ; Python réutilise le
      module déjà chargé, celui de la première copie jouée : un sabotage de `COMMUN` ne serait pas vu (aucun ne
      le touche aujourd'hui).
    ⑩ EFFET — importe un module ; modifie le chemin des imports.
    ⑪ TERMINAISON — rend la main, ou lève si l'import échoue.
      [sort: non]
    """
    sp = importlib.util.spec_from_file_location("MESURE_copie_%d" % id(r), os.path.join(r, MES))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def collecte(r):
    """Rend ce que la collecte du soir lit dans le référentiel de la copie `r` : nom usuel → code de bourse.

    ① RÔLE — faire passer E2, E3 et E5 par le chemin réel de la collecte, pas seulement par celui de la mesure :
      les deux programmes lisent le même fichier, et c'est leur accord qu'on éprouve (relecteur du 30-09-2026).
    ② CONTEXTE D'APPEL — `epreuves`, une fois par référentiel fabriqué.
    ③ ENTRÉE — `r` : la racine d'une copie du dépôt.
    ④ CONDITIONS D'ENTRÉE — la collecte doit s'importer sans se lancer ; `donnees/` doit porter un référentiel.
    ⑤ SORTIE — UNE valeur : le dictionnaire nom usuel (tel qu'écrit au référentiel) → code de bourse sans son
      suffixe de place.
      [rend: 1]
    ⑥ TRAITEMENT — importer `COLLECTER_ABC_GITHUB.py` de la copie sous un nom neuf, appeler `lire_referentiel`,
      retirer le dernier caractère du code (« p » pour Paris, « n » pour Amsterdam).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — une épreuve qui dit « comme la collecte » doit passer par la collecte.
    ⑨ CE QUI CLOCHE — `lire_referentiel` arrête le programme (sys.exit) si aucun référentiel n'est trouvé ; ce cas
      n'est pas joué ici.
    ⑩ EFFET — importe un module ; modifie le chemin des imports.
    ⑪ TERMINAISON — rend la main, ou sort si la collecte ne trouve aucun référentiel.
      [sort: oui]
    """
    sp = importlib.util.spec_from_file_location("COLLECTE_copie_%d" % id(r), os.path.join(r, COL))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    _nom, lignes = m.lire_referentiel(r)
    return {n: code[:-1] for n, code, _place in lignes}


def epreuves(r):
    """Joue E1 à E5 sur la copie `r` et rend la liste (nom, verdict).

    ① RÔLE — les épreuves décrites en tête.
    ② CONTEXTE D'APPEL — `main`, une fois par sabotage.
    ③ ENTRÉE — `r` : une copie du dépôt, éventuellement sabotée.
    ④ CONDITIONS D'ENTRÉE — le référentiel réel doit porter les colonnes mnemonique et nom_usuel.
    ⑤ SORTIE — UNE valeur : la liste des couples (nom de l'épreuve, vrai si verte).
      [rend: 1]
    ⑥ TRAITEMENT — ① E1 sur la copie · ② E4, la mesure lancée sur la copie · ③ E2, un référentiel plus récent
      dans archives/ · ④ E3, un référentiel plus récent dans donnees/ · ⑤ E5, un référentiel plus récent en
      « .CSV » ; E2, E3 et E5 interrogent aussi la collecte (`collecte`).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — E4 passe avant les fichiers fabriqués, pour que ceux-ci ne faussent pas le chemin réel.
    ⑨ CE QUI CLOCHE — les référentiels fabriqués ne portent qu'une ligne ; la mesure réelle n'est lancée que
      sur la copie telle quelle.
    ⑩ EFFET — écrit deux fichiers dans la copie ; lance la mesure, qui écrit dans la copie.
    ⑪ TERMINAISON — rend la main ; la mesure est arrêtée au bout de 600 secondes.
      [sort: non]
    """
    res = []
    m = charger(r)
    bv, ur = m._norm("BUREAU_VERITAS"), m._norm("UNIBAIL_RODAMCO")   # la forme de la mesure, jamais recopiée

    def col_bv():
        """La valeur que la collecte associe à Bureau Veritas, noms ramenés à la forme de la mesure."""
        return {m._norm(k): v for k, v in collecte(r).items()}.get(bv)
    t = m.charger_referentiel(r)
    res.append(("E1 BUREAU_VERITAS → BVI et UNIBAIL_RODAMCO → URW", t.get(bv) == "BVI" and t.get(ur) == "URW"))
    p = subprocess.run([sys.executable, os.path.join(r, MES), r], cwd=r, capture_output=True, text=True,
                       errors="replace", timeout=600)
    s = p.stdout + p.stderr
    hors = [l for l in s.splitlines() if "HORS UNIVERS" in l and ("BUREAU_VERITAS" in l or "UNIBAIL" in l)]
    res.append(("E4 la mesure trouve le référentiel et ne crie pas « HORS UNIVERS »",
                "valeurs connues" in s and not hors))
    entete = "mnemonique,nom_usuel\n"
    os.makedirs(os.path.join(r, "archives"), exist_ok=True)
    open(os.path.join(r, "archives", "REFERENTIEL_VALEURS_v9_Jeu_31-12-2026_10h00.csv"), "w",
         encoding="utf-8").write(entete + "XXX,BUREAU_VERITAS\n")
    res.append(("E2 un référentiel plus récent dans archives/ est ignoré, par la mesure et par la collecte",
                charger(r).charger_referentiel(r).get(bv) == "BVI" and col_bv() == "BVI"))
    open(os.path.join(r, "donnees", "REFERENTIEL_VALEURS_v4_Mer_30-12-2026_10h00.csv"), "w",
         encoding="utf-8").write(entete + "YYY,BUREAU_VERITAS\n")
    res.append(("E3 le plus récent de donnees/ l'emporte, pour la mesure et pour la collecte",
                charger(r).charger_referentiel(r).get(bv) == "YYY" and col_bv() == "YYY"))
    open(os.path.join(r, "donnees", "REFERENTIEL_VALEURS_v5_Jeu_31-12-2026_11h00.CSV"), "w",
         encoding="utf-8").write(entete + "ZZZ,BUREAU_VERITAS\n")
    res.append(("E5 un « .CSV » en majuscules est ignoré, par la mesure et par la collecte",
                charger(r).charger_referentiel(r).get(bv) == "YYY" and col_bv() == "YYY"))
    return res


def main():
    """Joue les épreuves sans sabotage, puis chaque sabotage avec --saboter.

    ① RÔLE — dire si les épreuves prouvent quelque chose.
    ② CONTEXTE D'APPEL — le lancement du fichier.
    ③ ENTRÉE — la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — la racine doit être un dépôt complet.
    ⑤ SORTIE — UNE valeur : le code de sortie.
      [rend: 1]
    ⑥ TRAITEMENT — pour chaque cas : copier le dépôt, appliquer le sabotage, jouer, compter les rouges.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration (R-731).
    ⑨ CE QUI CLOCHE — chaque cas recopie le dépôt entier.
    ⑩ EFFET — crée puis efface des copies ; affiche un compte rendu.
    ⑪ TERMINAISON — rend la main par son code.
      [sort: non]
    """
    choix = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
    bon = True
    for sab in choix:
        d = tempfile.mkdtemp(prefix="referentiel_mesure_")
        try:
            r = os.path.join(d, "r")
            shutil.copytree(DEPOT, r, ignore=shutil.ignore_patterns(".git", "_site_travail", "__pycache__"))
            for f, a, b in SABOTAGES[sab]:
                p = os.path.join(r, f)
                x = open(p, encoding="utf-8").read()
                if x.count(a) != 1:
                    print(f"SABOTAGE {sab} INAPPLICABLE : ancre absente ou multiple — l'épreuve ne prouverait plus rien")
                    return 2
                open(p, "w", encoding="utf-8").write(x.replace(a, b))
            res = epreuves(r)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        rouges = [n for n, ok in res if not ok]
        print(f"== {sab} : {len(res) - len(rouges)} vertes, {len(rouges)} rouges")
        for n in rouges:
            print("     ROUGE " + n)
        if sab == "Z0" and rouges:
            bon = False
        if sab != "Z0" and not rouges:
            print(f"     ⚠ LE SABOTAGE {sab} NE FAIT RIEN ROUGIR : épreuve sans dents")
            bon = False
    print("VERDICT :", "tout est conforme" if bon else "NON CONFORME")
    return 0 if bon else 1


if __name__ == "__main__":
    sys.exit(main())
