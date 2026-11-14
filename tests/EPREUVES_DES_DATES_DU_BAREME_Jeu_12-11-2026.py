#!/usr/bin/env python3
"""ÉPREUVES DES DATES DU BARÈME — Plan V7, E2a tour 4 (jeudi 12-11-2026). SIMULATION UNIQUEMENT.

① RÔLE — Tendre un filet sur les DATES des lignes de taxe de donnees/BAREME_FRAIS.csv, par deux propriétés, sans
  recopier aucune date (R-708 : deux exemplaires d'une même valeur finissent toujours par diverger) : ① P1 — chaque
  ligne de taxe qui a une date de début porte cette date EN TOUTES LETTRES dans sa propre colonne `source`, sous la
  forme « à compter du <jour> <mois> <année> » (« 1er » pour le premier du mois) ; ② P2 — dans chaque suite de lignes
  de taxe de même barème, même instrument et même sens, les périodes se suivent sans trou ni chevauchement (le début
  d'une ligne est le lendemain de la fin de la précédente ; seule la dernière peut être sans fin).
② CONTEXTE D'APPEL — `python3 -I <ce fichier> <racine> [--saboter]`, à la main ou par la certification.
③ ENTRÉE — La racine du dépôt. Le barème est lu par le lecteur du circuit (MODULE_POSITIONS._lire_un_tableau, qui le
  confronte à son contrat), sur une COPIE (programmes/MODULE_POSITIONS.py, programmes/CONTRATS_DES_FICHIERS.py,
  donnees/BAREME_FRAIS.csv) dans un dossier jetable.
④ CONDITIONS D'ENTRÉE — Les trois fichiers existent. Sinon : code 2.
⑤ SORTIE — Le code de sortie : 0 si P1 et P2 tiennent sur le barème tel quel (et, avec --saboter, si chaque sabotage
  fait rougir au moins une propriété) ; 1 sinon ; 2 si un sabotage ne s'applique plus ou si une lecture échoue.
  [rend: 1]
⑥ TRAITEMENT — Z0 : P1 et P2 sur le barème tel quel, une ligne par ligne de taxe (sa source contient-elle sa date ?)
  · avec --saboter : chaque sabotage change le barème DE LA COPIE (texte remplacé une fois exactement), puis P1 et P2
  sont rejoués ; un sabotage « mord » si au moins une propriété rougit.
⑦ UNITÉ — Des dates AAAA-MM-JJ et des jours civils.
⑧ POURQUOI — Relecteur E2a du tour 3 (12-11-2026, D1, « MOYEN ») : début de la ligne 0,2 % avancé de 2012-08-01 à
  2012-01-01 sur une copie → taxe prélevée à tort de janvier à juillet 2012, et l'inventaire, l'épreuve du barème et le
  calibrage restaient verts. Superviseur R-759 du même jour (marche qui fait foi) : une épreuve sur une PROPRIÉTÉ, la
  date lue dans la source de la même ligne, jamais une date recopiée dans l'épreuve ; le K3 de l'inventaire relit le
  même barème que le calcul et ne peut pas voir une donnée fausse.
⑨ CE QUI CLOCHE — P1 vérifie que la date ÉCRITE dans la source est celle de `debut`, pas que la source dit vrai :
  la phrase a été recopiée à la main (ligne 0,4 % : relevée le 12-11-2026 sur le BOFiP). · P1 ne porte que sur
  `debut` : les `fin` sont gardées par P2 et la ligne suivante, SAUF LA DERNIÈRE — donner une fin à la ligne 0,4 %
  (une taxe qui s'arrêterait au 2025-12-31) reste vert (relecteur E2a tour 4, R1, 12-11-2026 : consigné, non réparé). · Une ligne de taxe sans date
  de début (l'ETF, taux 0) n'est pas soumise à P1 : elle est nommée dans la sortie. · P2 ne compare que les lignes de
  même barème, instrument et sens : un chevauchement entre « action » et « action_et_etf » ne serait pas vu.
⑩ EFFET — Des dossiers jetables, effacés à la fin.
⑪ TERMINAISON — Rend la main ; sort par sys.exit. [sort: oui]
"""
import datetime
import importlib.util
import os
import shutil
import sys
import tempfile

RACINE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else os.getcwd()
FICHIERS = ("programmes/MODULE_POSITIONS.py", "programmes/CONTRATS_DES_FICHIERS.py", "donnees/BAREME_FRAIS.csv")
MOIS = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre",
        "décembre")
# Chaque sabotage : (texte cherché dans le barème, remplacement). Le texte cherché est pris DANS le barème au moment
# du jeu (une ligne lue, sa date substituée) : aucune date n'est écrite ici.
SABOTAGES = ("S1_debut_du_0_2_avance_au_premier_janvier", "S2_phrase_datee_retiree_de_la_ligne_0_4",
             "S3_chevauchement_0_3_et_0_4", "S4_trou_entre_0_2_et_0_3",
             # relecteur E2a tour 4 (12-11-2026), D1 : la condition « dans SA PROPRE source » (l. 93) et la forme
             # « à compter du » (`en_lettres`) n'étaient gardées par aucun sabotage ; D2 : la branche « ligne sans
             # fin suivie d'une autre » non plus
             "S5_sources_des_lignes_0_2_et_0_3_echangees", "S6_date_nue_sans_a_compter_du_dans_la_ligne_0_2",
             "S7_ligne_de_taxe_ajoutee_apres_la_ligne_sans_fin")


def en_lettres(d):
    """Écrit une date comme le droit fiscal l'écrit. ① RÔLE — « à compter du 1er août 2012 ». ② CONTEXTE D'APPEL —
    `proprietes`. ③ ENTRÉE — `d` : une date. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le texte. [rend: 1]
    ⑥ TRAITEMENT — « 1er » pour le premier, le numéro sinon ; mois en français. ⑦ UNITÉ — — ⑧ POURQUOI — fiche en
    tête. ⑨ CE QUI CLOCHE — une source qui écrirait « 1 août » ou « premier août » ne serait pas reconnue (P1 rougit).
    ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    return f"à compter du {'1er' if d.day == 1 else d.day} {MOIS[d.month - 1]} {d.year}"


def lire(dossier):
    """Lit le barème par le lecteur du circuit, dans `dossier`. ① RÔLE — une lecture neuve. ② CONTEXTE D'APPEL —
    `jouer`. ③ ENTRÉE — un dossier qui porte les trois FICHIERS. ④ CONDITIONS D'ENTRÉE — idem. ⑤ SORTIE — UNE
    valeur : la liste des lignes du barème (dictionnaires). [rend: 1] ⑥ TRAITEMENT — module chargé sous un nom neuf
    (son cache est neuf), `_lire_un_tableau("BAREME_FRAIS.csv", "BAREME_FRAIS")`. ⑦ UNITÉ — — ⑧ POURQUOI — lire comme
    le calcul lit (même contrat, même saut du commentaire). ⑨ CE QUI CLOCHE — appelle une fonction privée du module.
    ⑩ EFFET — — ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]
    """
    spec = importlib.util.spec_from_file_location(f"mp_{abs(hash(dossier))}",
                                                  os.path.join(dossier, "programmes", "MODULE_POSITIONS.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m._lire_un_tableau("BAREME_FRAIS.csv", "BAREME_FRAIS")


def proprietes(lignes):
    """P1 et P2 sur les lignes de taxe ; rend (fautes, constats).

    ① RÔLE — Le cœur. ② CONTEXTE D'APPEL — `jouer`. ③ ENTRÉE — les lignes du barème. ④ CONDITIONS D'ENTRÉE — les
    dates écrites se lisent (ValueError sinon). ⑤ SORTIE — DEUX valeurs : la liste des fautes (textes), la liste des
    constats (une ligne par ligne de taxe). [rend: 2] ⑥ TRAITEMENT — fiche en tête, ①. ⑦ UNITÉ — jours civils.
    ⑧ POURQUOI — fiche en tête. ⑨ CE QUI CLOCHE — fiche en tête. ⑩ EFFET — — ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    fautes, constats = [], []
    taxes = [l for l in lignes if l["nature"] == "ttf"]
    for l in taxes:
        nom = f"{l['nom_bareme']} {l['instrument']} {l['sens']} taux {l['taux_fraction']}"
        if not l["debut"]:
            constats.append(f"{nom} : sans date de début, hors P1")
            continue
        texte = en_lettres(datetime.date.fromisoformat(l["debut"]))
        ok = texte in l["source"]
        constats.append(f"{nom} : début {l['debut']} — « {texte} » dans sa source : {'oui' if ok else 'NON'}")
        if not ok:
            fautes.append(f"P1 {nom} : la source ne porte pas « {texte} »")
    suites = {}
    for l in taxes:
        if l["debut"] or l["fin"]:
            suites.setdefault((l["nom_bareme"], l["instrument"], l["sens"]), []).append(l)
    for cle, s in suites.items():
        s.sort(key=lambda l: l["debut"] or "0000-00-00")
        for a, b in zip(s, s[1:]):
            if not a["fin"]:
                fautes.append(f"P2 {cle} : une ligne sans fin ({a['debut']}) est suivie d'une autre ({b['debut']})")
                continue
            attendu = datetime.date.fromisoformat(a["fin"]) + datetime.timedelta(days=1)
            if not b["debut"] or datetime.date.fromisoformat(b["debut"]) != attendu:
                genre = "chevauchement" if b["debut"] and b["debut"] < attendu.isoformat() else "trou"
                fautes.append(f"P2 {cle} : {genre} entre la fin {a['fin']} et le début {b['debut'] or '(vide)'}")
    return fautes, constats


def saboter(texte, nom, lignes):
    """Rend le barème saboté, ou None si le sabotage ne s'applique plus.

    ① RÔLE — Fabriquer chaque sabotage À PARTIR des lignes lues. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — le texte du
    barème, le nom du sabotage, ses lignes lues. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le texte ou None.
    [rend: 1] ⑥ TRAITEMENT — S1 : la ligne de taux 0.002, son « ,<début>, » remplacé par le 1er janvier de la même
    année · S2 : la ligne de taux 0.004, la phrase « à compter du … » de son début retirée de sa source · S3 : la ligne de
    taux 0.003, sa fin portée au lendemain de sa fin · S4 : la ligne de taux 0.002, sa fin avancée d'un jour. Chaque
    texte remplacé doit se trouver une fois exactement · S5 : les sources des lignes 0.002 et 0.003 échangées (chaque
    phrase reste dans le barème, mais plus dans sa propre ligne) · S6 : dans la source de la ligne 0.002, « à compter du
    <date> » réduit à « <date> » · S7 : la ligne 0.004 (sans fin) recopiée sous elle avec un début un an plus tard et la
    phrase de sa source mise à cette date (P1 tient sur elle, seule P2 peut rougir). ⑦ UNITÉ — — ⑧ POURQUOI — aucune date écrite dans l'épreuve.
    ⑨ CE QUI CLOCHE — les sabotages repèrent les lignes par leur taux. ⑩ EFFET — — ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    par_taux = {l["taux_fraction"]: l for l in lignes if l["nature"] == "ttf" and l["instrument"] == "action"}
    D = datetime.date.fromisoformat
    try:
        if nom.startswith("S1"):
            l = par_taux["0.002"]
            a, b = f",{l['debut']},{l['fin']},", f",{l['debut'][:4]}-01-01,{l['fin']},"
        elif nom.startswith("S2"):
            l = par_taux["0.004"]
            a = en_lettres(D(l["debut"]))
            b = "à une date"
        elif nom.startswith("S3"):
            l = par_taux["0.003"]
            a = f",{l['debut']},{l['fin']},"
            b = f",{l['debut']},{(D(l['fin']) + datetime.timedelta(days=1)).isoformat()},"
        elif nom.startswith("S4"):
            l = par_taux["0.002"]
            a = f",{l['debut']},{l['fin']},"
            b = f",{l['debut']},{(D(l['fin']) - datetime.timedelta(days=1)).isoformat()},"
        elif nom.startswith("S5"):
            s2, s3 = par_taux["0.002"]["source"], par_taux["0.003"]["source"]
            if texte.count(s2) != 1 or texte.count(s3) != 1 or "\0" in texte:
                return None
            return texte.replace(s2, "\0").replace(s3, s2).replace("\0", s3)
        elif nom.startswith("S6"):
            l = par_taux["0.002"]
            # la date est écrite ici SANS `en_lettres`, sinon un `en_lettres` qui perdrait « à compter du » rendrait
            # le sabotage vide et il mordrait par accident (mutation M4 du relecteur, rejouée le 12-11-2026)
            d = D(l["debut"])
            nue = f"{'1er' if d.day == 1 else d.day} {MOIS[d.month - 1]} {d.year}"
            a, b = "à compter du " + nue, nue
        else:
            l = par_taux["0.004"]
            if l["fin"]:
                return None
            ouverte = [x for x in texte.splitlines(keepends=True) if f",{l['debut']},," in x]
            if len(ouverte) != 1:
                return None
            plus_tard = D(l["debut"]).replace(year=D(l["debut"]).year + 1)
            nouvelle = ouverte[0].replace(f",{l['debut']},,", f",{plus_tard.isoformat()},,").replace(
                en_lettres(D(l["debut"])), en_lettres(plus_tard))
            if nouvelle.count(en_lettres(plus_tard)) != 1:
                return None
            return texte.replace(ouverte[0], ouverte[0] + nouvelle)
    except (KeyError, ValueError):
        return None
    return texte.replace(a, b) if texte.count(a) == 1 else None


def jouer(texte_du_bareme):
    """Pose une copie, y écrit le barème donné, lit, rend (fautes, constats).

    ① RÔLE — un passage. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — le texte du barème. ④ CONDITIONS D'ENTRÉE — les
    FICHIERS existent sous RACINE. ⑤ SORTIE — DEUX valeurs : fautes, constats. [rend: 2] ⑥ TRAITEMENT — copie,
    écriture, `lire`, `proprietes`. ⑦ UNITÉ — — ⑧ POURQUOI — ne jamais toucher le dépôt. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — un dossier jetable, effacé. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    d = tempfile.mkdtemp(prefix="dates_bareme_")
    try:
        for rel in FICHIERS:
            os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
            shutil.copy(os.path.join(RACINE, rel), os.path.join(d, rel))
        with open(os.path.join(d, "donnees", "BAREME_FRAIS.csv"), "w", encoding="utf-8", newline="") as f:
            f.write(texte_du_bareme)
        return proprietes(lire(d))
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    """Z0 puis les sabotages. ① RÔLE — fiche en tête. ② CONTEXTE D'APPEL — ligne de commande. ③ ENTRÉE — sys.argv.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le code. [rend: 1] ⑥ TRAITEMENT — fiche en tête.
    ⑦ UNITÉ — — ⑧ POURQUOI — fiche en tête. ⑨ CE QUI CLOCHE — — ⑩ EFFET — dossiers jetables.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    try:
        texte = open(os.path.join(RACINE, "donnees", "BAREME_FRAIS.csv"), encoding="utf-8", newline="").read()
        fautes, constats = jouer(texte)
        d = tempfile.mkdtemp(prefix="dates_bareme_l_")
        try:
            for rel in FICHIERS:
                os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
                shutil.copy(os.path.join(RACINE, rel), os.path.join(d, rel))
            lignes = lire(d)
        finally:
            shutil.rmtree(d, ignore_errors=True)
    except Exception as e:   # noqa: BLE001 — relecteur E2b tour 2, m2 : toute exception du Z0 sort en code 2 (R-734)
        print(f"ARRET lecture impossible : {type(e).__name__} : {e}")
        sys.exit(2)
    for c in constats:
        print("   " + c)
    print("Z0 barème tel quel : " + ("P1 et P2 tiennent" if not fautes else "ROUGE — " + " · ".join(fautes)))
    code = 1 if fautes else 0
    if "--saboter" in sys.argv:
        for nom in SABOTAGES:
            # relecteur E2a tour 4, D2 : une propriété qui lève sur un barème saboté sort en code 2, pas en trace ;
            # relecteur E2b tour 2, m2 : `saboter` aussi dans le try
            try:
                t = saboter(texte, nom, lignes)
                if t is None:
                    print(f"{nom} NE S'APPLIQUE PLUS")
                    sys.exit(2)
                f, _ = jouer(t)
            except Exception as e:   # noqa: BLE001 — relecteur E2b tour 1, M4 : toute exception, type affiché, code 2
                print(f"{nom} ARRET lecture ou propriété impossible : {type(e).__name__} : {e}")
                sys.exit(2)
            print(f"{nom} {'mord' if f else 'NE MORD PAS'} : {f[:2]}")
            code = code or (0 if f else 1)
        print("VERDICT : " + ("tout est conforme" if code == 0 else "NON CONFORME"))
    sys.exit(code)


if __name__ == "__main__":
    main()
