#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_CALENDRIER_DE_LA_BOURSE — Mer 30-09-2026 (Paris)
Rôle : prouver que programmes/CALENDRIER_DE_LA_BOURSE.py répond juste, SUR DES RÉPONSES ÉCRITES À LA MAIN, et que
chaque épreuve a des dents.
Quand l'appeler : avant toute livraison qui touche programmes/CALENDRIER_DE_LA_BOURSE.py ou
donnees/CALENDRIER_EURONEXT.csv (R-731).

À QUOI ÇA SERT. Le message du soir de Jean-Luc demande à ce module quelle séance il attend. La relecture indépendante
du 30-09-2026 a montré que les épreuves du message calculaient leurs dates AVEC ce module : un module faux rendait les
épreuves fausses avec lui (le week-end non sauté restait vert). Ici, chaque réponse attendue est écrite à la main,
à des dates fixes, sur le vrai fichier du dépôt : rien ne dépend du jour où l'on lance les épreuves.

LES ÉPREUVES :
C1 le vrai fichier se lit : couvert du 01-01-2026 au 31-12-2026, fermetures exactement 01-01, 03-04, 06-04, 01-05,
   25-12 (texte des boucles, relevé le 08-09-2026 sur la page officielle d'Euronext) ;
C2 jour de bourse ou non, sur des dates écrites à la main (samedi, dimanche, 24-12, 25-12, 31-12, 01-05, un mardi) ;
C3 dernier jour de bourse (un dimanche → le vendredi ; le 26-12 → le 24-12 ; le lundi de Pâques → le jeudi d'avant) ;
C4 jours de bourse de retard (du jeudi 24-09 au mercredi 30-09 : 4, et non 6 jours du calendrier) ;
C5 hors couverture : le 01-01-2027 et le 31-12-2025 lèvent HorsCalendrier ;
C6 les refus de lire() : en-tête faux, état inconnu, date « 20260501 », « 2026-W18-5 » ou « 2026-02-30 », deux bornes
   basses, borne haute absente, bornes inversées, un jour écrit deux fois, une fermeture hors bornes, une fermeture un
   samedi ou un dimanche, une fermeture avant la borne basse, une colonne de trop, fichier absent ;
C7 les tolérances de lire() : marque d'ordre d'octets d'Excel, ligne vide, bornes écrites dans l'autre ordre ;
C8 lancé seul : code 0 et « 5 fermeture(s) » sur le dépôt ; code 1 sans calendrier.
LES SABOTAGES : K1 week-end non sauté · K2 fermetures ignorées · K3 jours du calendrier comptés · K4 couverture non
contrôlée · K5 état non contrôlé · K6 en-tête non contrôlé · K8 samedi jour de bourse · K9 forme de date non exigée ·
K10 doublon toléré · K11 fermeture hors bornes tolérée · K12 fermeture un week-end tolérée · K13 marque d'Excel
refusée · K14 bornes non comptées · K15 dernier jour décalé d'un jour · K16 lancé seul, code 0 toujours · K17 retard
compté avec le jour de départ · K18 demi-séance prise pour une fermeture · K19 fermeture un dimanche tolérée · K20
fermeture avant la borne basse tolérée.

USAGE : python3 tests/EPREUVES_DU_CALENDRIER_DE_LA_BOURSE_Mer_30-09-2026.py <racine du dépôt> [--saboter]
CODE : 0 si Z0 est vert et, avec --saboter, si chaque sabotage fait rougir au moins une épreuve ; 1 sinon ; 2 si un
sabotage ne s'applique plus.
"""
import importlib.util, os, shutil, subprocess, sys, tempfile
from datetime import date

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
MODULE = "programmes/CALENDRIER_DE_LA_BOURSE.py"
D = date.fromisoformat
SABOTAGES = {
    "Z0": [],
    "K1_week_end_non_saute": [('    return jour.weekday() < 5 and jour not in cal["fermes"]', '    return jour not in cal["fermes"]')],
    "K2_fermetures_ignorees": [('    return jour.weekday() < 5 and jour not in cal["fermes"]', '    return jour.weekday() < 5')],
    "K3_jours_du_calendrier": [("        n += est_jour_de_bourse(d, cal)\n", "        n += 1\n")],
    "K4_couverture_non_controlee": [('    if not (cal["depuis"] <= jour <= cal["jusqu_au"]):', "    if False:")],
    "K5_etat_non_controle": [("        if l[1] not in ETATS:", "        if False:")],
    "K6_entete_non_controle": [("    if not lignes or lignes[0] != list(contrats.CALENDRIER):", "    if not lignes:")],
    "K8_samedi_jour_de_bourse": [('jour.weekday() < 5 and jour not in', 'jour.weekday() < 6 and jour not in')],
    "K9_forme_de_date_libre": [('    if not re.fullmatch(r"\\d{4}-\\d{2}-\\d{2}", texte):\n        raise ValueError(texte)\n', "")],
    "K10_doublon_tolere": [("            if d in jours:\n", "            if False:\n")],
    "K11_hors_bornes_tolere": [("        if not depuis[0] <= d <= jusqu_au[0]:", "        if False:")],
    "K12_week_end_tolere": [("        if d.weekday() >= 5:\n", "        if False:\n")],
    "K13_marque_excel_refusee": [('open(os.path.join(racine, FICHIER), encoding="utf-8-sig"', 'open(os.path.join(racine, FICHIER), encoding="utf-8"')],
    "K14_bornes_non_comptees": [("    if len(depuis) != 1 or len(jusqu_au) != 1 or depuis[0] > jusqu_au[0]:", "    if not depuis or not jusqu_au:")],
    "K15_dernier_jour_decale": [("    d = jusqu_au_inclus\n", "    d = jusqu_au_inclus - timedelta(days=1)\n")],
    "K16_seul_code_0": [("        sys.exit(1)\n", "        sys.exit(0)\n")],
    "K17_retard_avec_depart": [("    n, d = 0, apres + timedelta(days=1)\n", "    n, d = 0, apres\n")],
    "K19_dimanche_tolere": [("        if d.weekday() >= 5:\n", "        if d.weekday() == 5:\n")],
    "K20_borne_basse_toleree": [("        if not depuis[0] <= d <= jusqu_au[0]:", "        if not d <= jusqu_au[0]:")],
    "K18_demi_seance_fermee": [('            if l[1] == "FERME":\n                fermes.add(d)\n', "            fermes.add(d)\n")],
}
ENTETE = "date,etat,source,citation,fichiers_cites"   # le contrat CALENDRIER depuis le 27-10-2026 (cinq colonnes)
B = ["2026-01-01,COUVERT_DEPUIS,e,,", "2026-12-31,COUVERT_JUSQU_AU,e,,"]


def ecrire(d, lignes, bom=False):
    """Écrit un calendrier d'épreuve dans la racine `d` et rend cette racine.

    ① RÔLE — Fabriquer un fichier donné ligne à ligne, pour les refus et les tolérances de lire().
    ② CONTEXTE D'APPEL — `epreuves`, une fois par cas.
    ③ ENTRÉE — `d` : un dossier · `lignes` : les lignes, en-tête compris · `bom` : vrai pour ajouter la marque
      d'ordre d'octets qu'écrit Excel.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la racine `d`.
      [rend: 1]
    ⑥ TRAITEMENT — créer donnees/, écrire le fichier.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Chaque refus vise une faute de frappe réaliste.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans `d`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    os.makedirs(os.path.join(d, "donnees"), exist_ok=True)
    open(os.path.join(d, "donnees", "CALENDRIER_EURONEXT.csv"), "w", encoding="utf-8-sig" if bom else "utf-8").write(
        "\n".join(lignes) + "\n")
    return d


def leve(f, *a):
    """Rend le nom de l'erreur levée par f(*a), ou None si elle rend la main.

    ① RÔLE — Dire si un appel est refusé, et par quelle erreur.
    ② CONTEXTE D'APPEL — `epreuves`.
    ③ ENTRÉE — `f` : une fonction · `a` : ses arguments.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nom de la classe de l'erreur, ou None.
      [rend: 1]
    ⑥ TRAITEMENT — appeler, attraper.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un refus se prouve par l'erreur, pas par le silence.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui de `f`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    try:
        f(*a)
        return None
    except Exception as e:
        return type(e).__name__


def epreuves(mod_path, tmp):
    """Joue les épreuves avec le module `mod_path` et rend la liste (nom, verdict).

    ① RÔLE — Les épreuves décrites en tête.
    ② CONTEXTE D'APPEL — `main`, une fois par sabotage.
    ③ ENTRÉE — `mod_path` : le module, saboté ou non, avec CONTRATS_DES_FICHIERS.py à côté · `tmp` : un dossier
      jetable.
    ④ CONDITIONS D'ENTRÉE — Le dépôt porte donnees/CALENDRIER_EURONEXT.csv.
    ⑤ SORTIE — UNE valeur : la liste des couples (nom, vrai si verte).
      [rend: 1]
    ⑥ TRAITEMENT — importer le module, l'interroger sur le vrai fichier puis sur des fichiers fabriqués, le lancer
      seul.
    ⑦ UNITÉ — Des dates et des jours de bourse.
    ⑧ POURQUOI — Les réponses attendues sont écrites à la main : le module ne se juge pas lui-même.
    ⑨ CE QUI CLOCHE — Les dates choisies couvrent 2026 seulement, comme le fichier.
    ⑩ EFFET — Écrit dans `tmp`, lance un processus.
    ⑪ TERMINAISON — Rend la main ; le lancement seul est borné à 60 secondes.
      [sort: non]
    """
    sp = importlib.util.spec_from_file_location("cal_%d" % id(tmp), mod_path)
    K = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(K)
    res = []
    try:
        cal = K.lire(DEPOT)
        ok1 = (cal["depuis"], cal["jusqu_au"]) == (D("2026-01-01"), D("2026-12-31")) and cal["fermes"] == {
            D("2026-01-01"), D("2026-04-03"), D("2026-04-06"), D("2026-05-01"), D("2026-12-25")}
    except Exception:
        cal, ok1 = None, False
    res.append(("C1 le vrai fichier : bornes 2026 et les cinq fermetures", ok1))
    if cal is None:
        return res + [("C2-C5 sans calendrier lisible", False)]
    q = lambda x: K.est_jour_de_bourse(D(x), cal)
    try:
        ok2 = (q("2026-10-03"), q("2026-10-04"), q("2026-12-24"), q("2026-12-25"), q("2026-12-31"), q("2026-05-01"),
               q("2026-04-07"), q("2026-09-30")) == (False, False, True, False, True, False, True, True)
    except Exception:
        ok2 = False
    res.append(("C2 jour de bourse : sam, dim non ; 24-12, 31-12 oui ; 25-12, 01-05 non ; un mardi oui", ok2))
    dj = lambda x: K.dernier_jour_de_bourse(D(x), cal).isoformat()
    try:
        ok3 = (dj("2026-10-04"), dj("2026-12-26"), dj("2026-04-06"), dj("2026-05-01"), dj("2026-09-30")) == (
            "2026-10-02", "2026-12-24", "2026-04-02", "2026-04-30", "2026-09-30")
    except Exception:
        ok3 = False
    res.append(("C3 dernier jour de bourse : dim→ven, 26-12→24-12, lundi de Pâques→jeudi, 01-05→30-04", ok3))
    ja = lambda a, b: K.jours_de_bourse_apres(D(a), D(b), cal)
    try:
        ok4 = (ja("2026-09-24", "2026-09-30"), ja("2026-04-02", "2026-04-07"), ja("2026-12-23", "2026-12-28"),
               ja("2026-09-30", "2026-10-01"), ja("2026-09-30", "2026-09-30")) == (4, 1, 2, 1, 0)
    except Exception:
        ok4 = False
    res.append(("C4 retard en jours de bourse : 24-09→30-09 = 4 ; Pâques = 1 ; Noël = 2", ok4))
    res.append(("C5 hors couverture : 01-01-2027 et 31-12-2025 lèvent HorsCalendrier",
                leve(K.est_jour_de_bourse, D("2027-01-01"), cal) == "HorsCalendrier"
                and leve(K.est_jour_de_bourse, D("2025-12-31"), cal) == "HorsCalendrier"))
    n = iter(range(100))
    dos = lambda: os.path.join(tmp, "c%d" % next(n))
    refus = {
        "en-tête faux": [ENTETE + "s"] + B,
        "état inconnu": [ENTETE] + B + ["2026-05-01,OUVERT,e,,"],
        "date 20260501": [ENTETE] + B + ["20260501,FERME,e,,"],
        "date 2026-W18-5": [ENTETE] + B + ["2026-W18-5,FERME,e,,"],
        "date 2026-02-30": [ENTETE] + B + ["2026-02-30,FERME,e,,"],
        "deux bornes basses": [ENTETE] + B + ["2026-02-01,COUVERT_DEPUIS,e,,"],
        "borne haute absente": [ENTETE, B[0]],
        "bornes inversées": [ENTETE, "2026-12-31,COUVERT_DEPUIS,e,,", "2026-01-01,COUVERT_JUSQU_AU,e,,"],
        "un jour FERME et DEMI_SEANCE": [ENTETE] + B + ["2026-12-24,FERME,e,,", "2026-12-24,DEMI_SEANCE,e,,"],
        "un jour FERME deux fois": [ENTETE] + B + ["2026-12-25,FERME,e,,", "2026-12-25,FERME,e,,"],
        "fermeture hors bornes": [ENTETE] + B + ["2027-01-01,FERME,e,,"],
        "fermeture un samedi": [ENTETE] + B + ["2026-10-03,FERME,e,,"],
        "fermeture un dimanche": [ENTETE] + B + ["2026-10-04,FERME,e,,"],
        "fermeture avant la borne basse": [ENTETE] + B + ["2025-12-25,FERME,e,,"],
        "une colonne de trop": [ENTETE] + B + ["2026-05-01,FERME,e,,,x"],
    }
    rates = [k for k, L in refus.items() if leve(K.lire, ecrire(dos(), L)) != "ValueError"]
    vide = dos(); os.makedirs(vide)
    if leve(K.lire, vide) != "FileNotFoundError":
        rates.append("fichier absent")
    res.append(("C6 refus de lire()" + (" — acceptés à tort : " + ", ".join(rates) if rates else ""), not rates))
    try:
        c1 = K.lire(ecrire(dos(), [ENTETE] + B + ["", "2026-05-01,FERME,e,,"], bom=True))
        c2 = K.lire(ecrire(dos(), [ENTETE, B[1], "2026-05-01,FERME,e,,", B[0]]))
        ok7 = c1["fermes"] == {D("2026-05-01")} and (c2["depuis"], c2["jusqu_au"]) == (D("2026-01-01"), D("2026-12-31"))
    except Exception:
        ok7 = False
    res.append(("C7 tolérances : marque d'Excel, ligne vide, bornes dans l'autre ordre", ok7))
    p = subprocess.run([sys.executable, mod_path, DEPOT], capture_output=True, text=True, timeout=60)
    p2 = subprocess.run([sys.executable, mod_path, vide], capture_output=True, text=True, timeout=60)
    # le code 0 n'est dû que si aujourd'hui est couvert ; hors 2026, le code 1 est la bonne réponse
    couvert = cal["depuis"] <= date.today() <= cal["jusqu_au"]
    res.append(("C8 lancé seul : code 0 et « 5 fermeture(s) » sur le dépôt ; code 1 sans calendrier",
                p.returncode == (0 if couvert else 1) and "5 fermeture(s)" in p.stdout and p2.returncode == 1))
    return res


def main():
    """Joue les épreuves sans sabotage, puis chaque sabotage avec --saboter.

    ① RÔLE — Dire si les épreuves prouvent quelque chose.
    ② CONTEXTE D'APPEL — Le lancement du fichier.
    ③ ENTRÉE — La ligne de commande.
    ④ CONDITIONS D'ENTRÉE — La racine donnée porte le module, programmes/CONTRATS_DES_FICHIERS.py et le calendrier.
    ⑤ SORTIE — UNE valeur : le code de sortie.
      [rend: 1]
    ⑥ TRAITEMENT — pour chaque cas : copier le module et le module des contrats, saboter, jouer, compter les rouges.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration (R-731).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Crée puis efface des dossiers jetables ; affiche un compte rendu.
    ⑪ TERMINAISON — Rend la main par son code.
      [sort: non]
    """
    src = open(os.path.join(DEPOT, MODULE), encoding="utf-8").read()
    choix = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
    bon = True
    for sab in choix:
        tmp = tempfile.mkdtemp(prefix="calendrier_")
        try:
            t = src
            for a, b in SABOTAGES[sab]:
                if t.count(a) != 1:
                    print(f"SABOTAGE {sab} INAPPLICABLE : ancre absente ou multiple")
                    return 2
                t = t.replace(a, b)
            mod = os.path.join(tmp, "CALENDRIER_DE_LA_BOURSE.py")
            open(mod, "w", encoding="utf-8").write(t)
            shutil.copy(os.path.join(DEPOT, "programmes", "CONTRATS_DES_FICHIERS.py"), tmp)
            res = epreuves(mod, tmp)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        rouges = [x for x, ok in res if not ok]
        print(f"== {sab} : {len(res) - len(rouges)} vertes, {len(rouges)} rouges")
        for x in rouges:
            print("     ROUGE " + x)
        if sab == "Z0" and rouges:
            bon = False
        if sab != "Z0" and not rouges:
            print(f"     ⚠ LE SABOTAGE {sab} NE FAIT RIEN ROUGIR : épreuve sans dents")
            bon = False
    print("VERDICT :", "tout est conforme" if bon else "NON CONFORME")
    return 0 if bon else 1


if __name__ == "__main__":
    sys.exit(main())
