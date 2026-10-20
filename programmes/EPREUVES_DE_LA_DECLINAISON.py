#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPREUVES_DE_LA_DECLINAISON.py — Mer 07-10-2026 (Paris)
DÉCIDÉ · outil · Rôle : éprouver PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES et DECLINER_LES_STRATEGIES, puis saboter chacun pour prouver que les épreuves rougissent.

USAGE
    python3 programmes/EPREUVES_DE_LA_DECLINAISON.py <registre>

① RÔLE — Prouver que les deux premières fonctions de la chaîne
  TROUVER_LA_VERSION_OPTIMALE_DES_STRATEGIES (A-541) font ce que leur fiche
  annonce, que leurs versions sont lisibles par le juge des stratégies, et que
  chaque épreuve tombe quand on retire ce qu'elle teste (R-731 : une épreuve qui
  reste verte sous sabotage est une décoration).
② CONTEXTE D'APPEL — À la main, avant tout dépôt d'une modification des deux programmes.
③ ENTRÉE — Un argument : le chemin du registre des stratégies. Le référentiel des
  valeurs doit être dans le même dossier.
④ CONDITIONS D'ENTRÉE — Les deux programmes, `COMMUN.py` et
  `JUGE_DES_STRATEGIES.py` sont dans le même dossier que celui-ci. Le registre
  porte les fiches C5E10-OBS-V1 et MA200-S1 (R-732 : au moins un cas vient
  d'une vraie ligne du fichier).
⑤ SORTIE — Un code de sortie : 0 si toutes les épreuves passent ET si chaque
  sabotage fait tomber au moins une épreuve · 1 sinon · 2 sans argument.
⑥ TRAITEMENT — ① charger les programmes · ② lancer les épreuves · ③ pour chaque
  sabotage, charger une copie modifiée et vérifier qu'au moins une épreuve tombe ·
  ④ afficher une ligne par épreuve et par sabotage · ⑤ effacer les dossiers temporaires.
⑦ UNITÉ — —
⑧ POURQUOI — R-731 impose des épreuves avec sabotages pour tout code écrit.
⑨ CE QUI CLOCHE — Les sabotages sont des remplacements de texte : si le code
  change, un sabotage peut ne plus trouver son texte ; il est alors signalé
  « INAPPLICABLE » et compte comme un échec.
⑩ EFFET — Écrit des fichiers dans des dossiers temporaires, effacés à la fin ; rien d'autre.
⑪ TERMINAISON — SORT DU PROGRAMME avec 0, 1 ou 2.
⑫ DÉFINITIONS —
  un sabotage : une copie volontairement abîmée d'un programme, qui doit faire tomber les épreuves.
  le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, qui rejoue une stratégie et rend des chiffres.
"""
import contextlib
import glob
import csv
import importlib.util
import io
import os
import shutil
import sys
import tempfile
import types

sys.dont_write_bytecode = True   # aucun dossier __pycache__ laissé derrière (⑩)
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
P_PREP = os.path.join(ICI, "PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES.py")
P_DECL = os.path.join(ICI, "DECLINER_LES_STRATEGIES.py")
P_JUGE = os.path.join(ICI, "JUGE_DES_STRATEGIES.py")
VOIS = {"tp": {"pas": "1", "de_part_et_d_autre": "2", "minimum": "1", "maximum": "10", "raison": "r"},
        "sl": {"pas": "0.5", "de_part_et_d_autre": "2", "minimum": "0.5", "maximum": "10", "raison": "r"},
        "horizon": {"pas": "5", "de_part_et_d_autre": "3", "minimum": "3", "maximum": "20", "raison": "r"}}
CODES = {"TTE", "ENGI", "VIE", "EN", "FGR", "AIR", "RNO", "URW", "BVI", "DG"}
DOSSIERS = []


def dossier_temporaire():
    """Crée un dossier temporaire et le retient pour l'effacer à la fin.

    ① RÔLE — Garantir qu'aucune épreuve n'écrit hors d'un dossier jetable.
    ② CONTEXTE D'APPEL — `charger` et `epreuves`.
    ③ ENTRÉE — Aucune.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : le chemin du dossier.
      [rend: 1]
    ⑥ TRAITEMENT — créer, retenir, rendre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La relecture du 07-10-2026 a relevé des dossiers jamais effacés.
    ⑨ CE QUI CLOCHE — rien vu.
    ⑩ EFFET — Crée un dossier temporaire.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    d = tempfile.mkdtemp()
    DOSSIERS.append(d)
    return d


def charger(chemin, nom, texte=None):
    """Charge un programme comme module, éventuellement depuis un texte modifié.

    ① RÔLE — Donner aux épreuves le programme réel ou sa copie sabotée.
    ② CONTEXTE D'APPEL — `main`, pour chaque programme et chaque sabotage.
    ③ ENTRÉE — `chemin` : le programme · `nom` : nom du module · `texte` : code de remplacement, ou None.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe ; `COMMUN.py` est à côté de `ICI`.
    ⑤ SORTIE — UNE valeur : le module chargé.
      [rend: 1]
    ⑥ TRAITEMENT — ① écrire le texte dans un dossier temporaire si fourni · ② charger.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Saboter une copie ne touche jamais au programme livré.
    ⑨ CE QUI CLOCHE — rien vu.
    ⑩ EFFET — Écrit un fichier temporaire quand un texte est fourni.
    ⑪ TERMINAISON — Rend la main, ou lève l'erreur de chargement.
      [sort: non]
    """
    if texte is not None:
        chemin2 = os.path.join(dossier_temporaire(), os.path.basename(chemin))
        open(chemin2, "w", encoding="utf-8").write(texte)
        chemin = chemin2
    spec = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def essayer(resultats, nom, f):
    """Lance une épreuve et note si elle réussit ; une exception compte comme un échec.

    ① RÔLE — Une seule façon d'enregistrer une épreuve.
    ② CONTEXTE D'APPEL — `epreuves`, une fois par épreuve.
    ③ ENTRÉE — `resultats` : la liste à compléter · `nom` : l'intitulé · `f` : la fonction qui rend vrai ou faux.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — Rien : complète `resultats`.
      [rend: rien]
    ⑥ TRAITEMENT — appeler `f`, noter le résultat ou l'exception.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve qui plante ne doit jamais passer pour réussie.
    ⑨ CE QUI CLOCHE — rien vu.
    ⑩ EFFET — Ajoute une ligne à `resultats`.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    try:
        resultats.append((nom, bool(f())))
    except Exception as e:  # une épreuve qui plante est une épreuve qui tombe
        resultats.append((nom + " [exception %s]" % type(e).__name__, False))


def ecrire_tableau(chemin, lignes):
    """Écrit des lignes dans un fichier CSV, pour fabriquer des cas d'épreuve.

    ① RÔLE — Fabriquer un tableau de variables modifié à donner aux programmes.
    ② CONTEXTE D'APPEL — `epreuves`.
    ③ ENTRÉE — `chemin` : le fichier · `lignes` : liste de dictionnaires de mêmes clés.
    ④ CONDITIONS D'ENTRÉE — `lignes` non vide.
    ⑤ SORTIE — UNE valeur : le chemin écrit.
      [rend: 1]
    ⑥ TRAITEMENT — écrire l'en-tête puis les lignes.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Éprouver `main` sur de vrais fichiers, pas seulement les fonctions.
    ⑨ CE QUI CLOCHE — rien vu.
    ⑩ EFFET — Écrit un fichier.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()))
        w.writeheader()
        w.writerows(lignes)
    return chemin


class EcrivainTronque(csv.DictWriter):
    """Un écrivain de tableau qui perd volontairement la dernière ligne.

    ① RÔLE — Simuler une écriture abîmée pour prouver que la relecture des deux programmes la voit.
    ② CONTEXTE D'APPEL — `ecriture_abimee`, qui le substitue au vrai écrivain.
    ③ ENTRÉE — Celle de `csv.DictWriter`.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — Un objet écrivain.
      [rend: 1]
    ⑥ TRAITEMENT — `writerows` écrit toutes les lignes sauf la dernière.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Sans écriture abîmée, une relecture neutralisée restait verte (sabotage du 07-10-2026).
    ⑨ CE QUI CLOCHE — rien vu.
    ⑩ EFFET — Écrit un fichier tronqué.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """

    def writerows(self, rows):
        """Écrit toutes les lignes sauf la dernière.

        ① RÔLE — Abîmer l'écriture.
        ② CONTEXTE D'APPEL — les programmes éprouvés, à la place du vrai écrivain.
        ③ ENTRÉE — `self` : l'écrivain lui-même · `rows` : les lignes à écrire.
        ④ CONDITIONS D'ENTRÉE — Aucune.
        ⑤ SORTIE — Ce que rend `csv.DictWriter.writerows`.
          [rend: 1]
        ⑥ TRAITEMENT — retirer la dernière ligne, écrire le reste.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Une relecture n'est prouvée que si elle voit une écriture fausse.
        ⑨ CE QUI CLOCHE — rien vu.
        ⑩ EFFET — Écrit un fichier tronqué.
        ⑪ TERMINAISON — Rend toujours la main.
          [sort: non]
        """
        return super().writerows(list(rows)[:-1])


def ecriture_abimee(module, appel):
    """Lance `appel` pendant que `module` écrit ses tableaux avec un écrivain tronqué.

    ① RÔLE — Éprouver la relecture des deux programmes.
    ② CONTEXTE D'APPEL — `epreuves`, deux fois.
    ③ ENTRÉE — `module` : le programme éprouvé · `appel` : une fonction sans argument qui lance son `main`.
    ④ CONDITIONS D'ENTRÉE — Le module importe `csv` sous ce nom.
    ⑤ SORTIE — UNE valeur : ce que rend `appel`.
      [rend: 1]
    ⑥ TRAITEMENT — ① remplacer `module.csv` par un double dont l'écrivain est tronqué · ② appeler · ③ remettre le vrai.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une relecture n'est prouvée que si on lui montre une écriture fausse.
    ⑨ CE QUI CLOCHE — rien vu.
    ⑩ EFFET — Écrit un fichier tronqué dans un dossier temporaire.
    ⑪ TERMINAISON — Rend la main, ou propage l'exception d'`appel`.
      [sort: non]
    """
    vrai = module.csv
    module.csv = types.SimpleNamespace(DictWriter=EcrivainTronque, DictReader=csv.DictReader)
    try:
        return appel()
    finally:
        module.csv = vrai


def remplacer(lignes, parametre, **changements):
    """Rend une copie d'un tableau où la ligne d'un réglage porte des cases changées.

    ① RÔLE — Fabriquer un cas défectueux à partir d'un tableau valide.
    ② CONTEXTE D'APPEL — `epreuves`.
    ③ ENTRÉE — `lignes` : le tableau · `parametre` : le réglage visé · `changements` : les cases à changer.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : la copie modifiée.
      [rend: 1]
    ⑥ TRAITEMENT — copier chaque ligne, changer celle du réglage visé.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Ne jamais modifier le tableau valide partagé entre épreuves.
    ⑨ CE QUI CLOCHE — rien vu.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    return [dict(l, **changements) if l["parametre"] == parametre else l for l in lignes]


def fusionner(registre, version):
    """Rend la fiche jouable d'une version : la fiche d'origine dont tp, sl, horizon et univers sont remplacés.

    ① RÔLE — Reproduire le passage de l'étape ① à l'étape ② décrit par DECLINER_LES_STRATEGIES.
    ② CONTEXTE D'APPEL — `epreuves`.
    ③ ENTRÉE — `registre` : dictionnaire identifiant → fiche · `version` : une ligne de la combinatoire.
    ④ CONDITIONS D'ENTRÉE — La stratégie de la version existe au registre.
    ⑤ SORTIE — UNE valeur : la fiche fusionnée.
      [rend: 1]
    ⑥ TRAITEMENT — copier la fiche, remplacer les quatre cases.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Prouver qu'une version se lit par le juge des stratégies.
    ⑨ CE QUI CLOCHE — Cette fusion n'existe encore que dans les épreuves : l'étape ② la fera (A-542).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève KeyError si la stratégie est absente.
      [sort: non]
    """
    return dict(registre[version["strategie"]], **{k: version[k] for k in ("tp", "sl", "horizon", "univers")})


def epreuves(prep, decl, juge, registre):
    """Lance toutes les épreuves et rend leurs résultats.

    ① RÔLE — Vérifier, cas par cas, ce que les fiches des deux programmes annoncent.
    ② CONTEXTE D'APPEL — `main`, une fois sur les vrais programmes, puis une fois par sabotage.
    ③ ENTRÉE — `prep`, `decl`, `juge` : les trois modules · `registre` : le chemin du registre.
    ④ CONDITIONS D'ENTRÉE — Celles de l'en-tête.
    ⑤ SORTIE — UNE valeur : la liste de couples (nom de l'épreuve, réussie ou non).
      [rend: 1]
    ⑥ TRAITEMENT — Une épreuve par propriété annoncée.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve par propriété dit précisément ce qui casse.
    ⑨ CE QUI CLOCHE — rien vu.
    ⑩ EFFET — Écrit des fichiers dans des dossiers temporaires.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    R = []
    e = lambda nom, f: essayer(R, nom, f)  # noqa: E731
    e("pourcents_de lit « -2.5% » comme 2.5", lambda: prep.pourcents_de("-2.5%") == 2.5)
    e("pourcents_de lit « -0.6% » comme 0.6", lambda: prep.pourcents_de("-0.6%") == 0.6)
    e("pourcents_de refuse « à renseigner », « 4-5 », « nan »",
      lambda: [prep.pourcents_de(x) for x in ("à renseigner", "4-5", "nan")] == [None, None, None])
    e("voisins : 4 ±2 crans de 1 → 2..6", lambda: prep.voisins(4.0, VOIS["tp"]) == [2, 3, 4, 5, 6])
    e("voisins : bornes respectées (horizon ≤ 20)", lambda: max(prep.voisins(20.0, VOIS["horizon"])) == 20)
    e("voisins : la valeur de la fiche est gardée même hors bornes", lambda: 25.0 in prep.voisins(25.0, VOIS["horizon"]))
    fiche = {"id": "X-1", "tp": "+4.0%", "sl": "-2.5%", "horizon": "20j", "univers": "TTE,ENGI"}
    e("preparer : fiche complète, horizon « 20j » accepté",
      lambda: prep.preparer(fiche, VOIS, "E01", "h", CODES)[1] == [])
    e("preparer : univers = entier (virgules) puis chaque valeur",
      lambda: [l for l in prep.preparer(fiche, VOIS, "E01", "h", CODES)[0]
               if l["parametre"] == "univers"][0]["valeurs_a_essayer"] == "TTE,ENGI;TTE;ENGI")
    e("preparer : univers d'une seule valeur proposé une seule fois",
      lambda: [l for l in prep.preparer(dict(fiche, univers="TTE"), VOIS, "E01", "h", CODES)[0]
               if l["parametre"] == "univers"][0]["valeurs_a_essayer"] == "TTE")
    e("preparer : tp « à renseigner » refusé", lambda: len(prep.preparer(dict(fiche, tp="à renseigner"), VOIS, "E01", "h", CODES)[1]) == 1)
    e("preparer : univers « à renseigner » refusé", lambda: len(prep.preparer(dict(fiche, univers="à renseigner"), VOIS, "E01", "h", CODES)[1]) == 1)
    e("preparer : univers avec code inconnu refusé", lambda: len(prep.preparer(dict(fiche, univers="TTE ENGI"), VOIS, "E01", "h", CODES)[1]) == 1)
    e("preparer : univers répétant un code refusé", lambda: len(prep.preparer(dict(fiche, univers="TTE,ENGI,TTE"), VOIS, "E01", "h", CODES)[1]) == 1)
    e("preparer : horizon « 7.5 » refusé", lambda: len(prep.preparer(dict(fiche, horizon="7.5"), VOIS, "E01", "h", CODES)[1]) == 1)
    e("preparer : réglage absent du voisinage refusé",
      lambda: len(prep.preparer(fiche, {k: v for k, v in VOIS.items() if k != "sl"}, "E01", "h", CODES)[1]) == 1)
    e("preparer : réglages du signal marqués NON jouables",
      lambda: {l["parametre"] for l in prep.preparer(fiche, VOIS, "E01", "h", CODES)[0] if l["jouable"] == "NON"}
      == {"duree_cmf", "duree_cci", "seuil_cci", "entree", "filtres"})
    e("preparer : univers en minuscules normalisé", lambda: [l for l in prep.preparer(dict(fiche, univers="tte,engi"), VOIS, "E01", "h", CODES)[0]
               if l["parametre"] == "univers"][0]["valeur_fiche"] == "TTE,ENGI")
    e("preparer : objectif de 0 % ou de 150 % refusé",
      lambda: len(prep.preparer(dict(fiche, tp="0%"), VOIS, "E01", "h", CODES)[1]) == 1
      and len(prep.preparer(dict(fiche, tp="150%"), VOIS, "E01", "h", CODES)[1]) == 1)
    e("preparer : pas d'horizon infini refusé sans planter",
      lambda: len(prep.preparer(fiche, dict(VOIS, horizon=dict(VOIS["horizon"], pas="inf")), "E01", "h", CODES)[1]) == 1)
    e("preparer : voisins sous 0,01 % écartés",
      lambda: min(float(x) for x in [l for l in prep.preparer(dict(fiche, sl="-0.6%"), dict(VOIS, sl=dict(VOIS["sl"], minimum="0.001", pas="0.595")), "E01", "h", CODES)[0]
                                     if l["parametre"] == "sl"][0]["valeurs_a_essayer"].split(";")) >= 0.01)
    e("preparer : pas d'horizon non entier refusé",
      lambda: len(prep.preparer(fiche, dict(VOIS, horizon=dict(VOIS["horizon"], pas="2.5")), "E01", "h", CODES)[1]) == 1)
    e("nombre_de_versions : 5 × 5 × 4 × 3 = 300",
      lambda: prep.nombre_de_versions(prep.preparer(fiche, VOIS, "E01", "h", CODES)[0]) == 300)

    d = dossier_temporaire()
    f_v = ecrire_tableau(os.path.join(d, "v.csv"), [dict(v, parametre=k, unite="u") for k, v in VOIS.items()])
    e("PREPARER sur la vraie fiche C5E10-OBS-V1 rend 0", lambda: prep.main([registre, "C5E10-OBS-V1", f_v, "E01", d]) == 0)
    e("PREPARER refuse la vraie fiche MA200-S1 (univers « A TRANCHER »)",
      lambda: prep.main([registre, "MA200-S1", f_v, "E01", d]) == 1)
    e("PREPARER refuse d'écraser un essai existant", lambda: prep.main([registre, "C5E10-OBS-V1", f_v, "E01", d]) == 1)
    e("PREPARER refuse un numéro d'essai mal formé", lambda: prep.main([registre, "C5E10-OBS-V1", f_v, "1", d]) == 1)
    e("PREPARER refuse une fiche absente", lambda: prep.main([registre, "N-EXISTE-PAS", f_v, "E09", d]) == 1)
    e("PREPARER refuse un identifiant dangereux", lambda: prep.main([registre, "../X", f_v, "E09", d]) == 1)
    reg2 = ecrire_tableau(os.path.join(d, "reg_double.csv"),
                          [l for l in prep.lire_tableau(registre) if l["id"] == "C5E10-OBS-V1"] * 2)
    for ref in glob.glob(os.path.join(os.path.dirname(os.path.abspath(registre)), "REFERENTIEL_VALEURS*.csv")):
        shutil.copy(ref, d)
    d3 = dossier_temporaire()
    reg3 = shutil.copy(registre, d3)
    for ref in glob.glob(os.path.join(os.path.dirname(os.path.abspath(registre)), "REFERENTIEL_VALEURS*.csv")):
        shutil.copy(ref, d3)
        shutil.copy(ref, os.path.join(d3, "REFERENTIEL_VALEURS_copie.csv"))
    e("PREPARER refuse deux référentiels", lambda: prep.main([reg3, "C5E10-OBS-V1", f_v, "E03", d3]) == 1)
    reg4 = ecrire_tableau(os.path.join(d3, "reg_mt.csv"),
                          [dict([l for l in prep.lire_tableau(registre) if l["id"] == "C5E10-OBS-V1"][0], id="X-MT", univers="TTE,MT")])
    os.remove(os.path.join(d3, "REFERENTIEL_VALEURS_copie.csv"))
    reg5 = ecrire_tableau(os.path.join(d3, "reg_espace.csv"),
                          [dict([l for l in prep.lire_tableau(registre) if l["id"] == "C5E10-OBS-V1"][0], id="X Y")])
    e("PREPARER refuse un identifiant de forme inattendue présent au registre", lambda: prep.main([reg5, "X Y", f_v, "E05", d3]) == 1)
    e("PREPARER refuse une fiche contenant MT, hors univers au référentiel", lambda: prep.main([reg4, "X-MT", f_v, "E04", d3]) == 1)
    e("PREPARER refuse une fiche présente deux fois", lambda: prep.main([reg2, "C5E10-OBS-V1", f_v, "E02", d]) == 1)

    sortie = os.path.join(d, "VARIABLES_DE_DECLINAISON_C5E10-OBS-V1_E01.csv")
    e("PREPARER : le fichier écrit porte 1 100 versions annoncées",
      lambda: prep.nombre_de_versions(prep.lire_tableau(sortie)) == 1100)
    if not os.path.exists(sortie):
        R.append(("PREPARER n'a pas écrit le tableau : épreuves de DECLINER impossibles", False))
        return R
    lignes = decl.lire_tableau(sortie)
    # LA DATE DE VALIDATION SUIT LA DATE DE PRÉPARATION : une validation ne peut pas
    # précéder la préparation. Une date écrite en dur faisait tomber l'épreuve dès
    # le lendemain (constaté le 08-10-2026).
    _jour = lignes[0]["prepare_le"][:10]
    _validation = "Jean-Luc le %s-%s-%s" % (_jour[8:10], _jour[5:7], _jour[0:4])
    valid = [dict(l, valide_par=_validation) if l["jouable"] == "OUI" else l for l in lignes]
    reg = {l["id"]: l for l in prep.lire_tableau(registre)}
    fic = reg["C5E10-OBS-V1"]
    codes = {(l.get("mnemonique") or "").strip().upper() for l in prep.lire_tableau(
        glob.glob(os.path.join(os.path.dirname(os.path.abspath(registre)), "REFERENTIEL_VALEURS*.csv"))[0])
        if not (l.get("hors_univers") or "").strip()} - {""}
    ver = lambda t: decl.verifier(t, fic, codes)  # noqa: E731

    remplace = lambda param, **ch: remplacer(valid, param, **ch)  # noqa: E731
    e("DECLINER refuse un tableau non validé", lambda: ver(lignes) != [])
    e("DECLINER accepte un tableau validé", lambda: ver(valid) == [])
    e("DECLINER refuse « — » comme validation", lambda: ver(remplace("tp", valide_par="—")) != [])
    e("DECLINER refuse jouable « oui » en minuscules", lambda: ver(remplace("tp", jouable="oui")) != [])
    # Valeurs vidées ET message exigé : sinon le refus venait de la règle « NON jouable sans valeurs à essayer »
    # et non de celle-ci (cassure M1 de la relecture de Cowork du 20-10-2026, 9702048).
    e("DECLINER refuse tp non jouable",
      lambda: any("ce réglage doit être jouable" in m for m in ver(remplace("tp", jouable="NON", valeurs_a_essayer=""))))
    # LE MOMENT D'ACHAT ET LES FILTRES (A-546 ⑤ ⑥, décision de Jean-Luc du 10-10-2026 à 18h29) :
    # écrits par PREPARER, NON jouables, avec la valeur réelle de la fiche C5E10-OBS-V1 (R-732).
    e("PREPARER écrit le moment d'achat et les filtres, NON jouables, avec la valeur de la fiche",
      lambda: all(any(l["parametre"] == p and l["jouable"] == "NON"
                      and l["valeur_fiche"] == (fic.get(p) or "").strip() for l in lignes)
                  for p in ("entree", "filtres")) and (fic.get("entree") or "").strip() != "")
    e("DECLINER refuse un moment d'achat jouable", lambda: ver(remplace("entree", jouable="OUI")) != [])
    e("DECLINER refuse des filtres jouables", lambda: ver(remplace("filtres", jouable="OUI")) != [])
    e("DECLINER refuse un moment d'achat qui ne dit pas ce que dit le registre",
      lambda: ver(remplace("entree", valeur_fiche="Close J")) != [] and ver(remplace("entree", valeur_fiche="")) != [])
    e("DECLINER refuse une ligne NON qui porte des valeurs à essayer",
      lambda: ver(remplace("entree", valeurs_a_essayer="Open J+1;Close J")) != []
      and ver(remplace("duree_cci", valeurs_a_essayer="10;14")) != [])
    e("DECLINER accepte un tableau ancien, sans moment d'achat ni filtres",
      lambda: ver([l for l in valid if l["parametre"] not in ("entree", "filtres")]) == [])
    e("DECLINER refuse un paramètre inconnu", lambda: ver(valid + [dict(valid[0], parametre="banane")]) != [])
    e("DECLINER refuse un paramètre en double", lambda: ver(valid + [valid[0]]) != [])
    e("DECLINER refuse « 2; 2;3 »", lambda: ver(remplace("tp", valeurs_a_essayer="2; 2;3;4")) != [])
    e("DECLINER refuse « 2;2.0;4 »", lambda: ver(remplace("tp", valeurs_a_essayer="2;2.0;4")) != [])
    e("DECLINER refuse une valeur illisible", lambda: ver(remplace("tp", valeurs_a_essayer="-3;abc;4")) != [])
    e("DECLINER refuse un horizon 7.5 ou 0", lambda: ver(remplace("horizon", valeurs_a_essayer="0;7.5;20")) != [])
    e("DECLINER refuse si la valeur de la fiche manque", lambda: ver(remplace("tp", valeurs_a_essayer="2;3")) != [])
    e("DECLINER refuse deux stratégies", lambda: ver([dict(valid[0], strategie="AUTRE")] + valid[1:]) != [])
    e("DECLINER refuse deux essais", lambda: ver([dict(valid[0], essai="E02")] + valid[1:]) != [])
    e("DECLINER refuse un essai dangereux", lambda: ver([dict(l, essai="X/../E") for l in valid]) != [])
    e("DECLINER refuse un tableau sans tp", lambda: ver([l for l in valid if l["parametre"] != "tp"]) != [])
    e("DECLINER refuse « à valider » comme validation", lambda: ver(remplace("tp", valide_par="à valider")) != [])
    e("DECLINER refuse une date de validation impossible ou antérieure à la préparation",
      lambda: ver(remplace("tp", valide_par="Jean-Luc le 99-99-0000")) != []
      and ver(remplace("tp", valide_par="Jean-Luc le 01-01-2020")) != [])
    e("DECLINER accepte une validation entourée d'espaces", lambda: ver(remplace("tp", valide_par="  %s " % _validation)) == [])
    e("DECLINER refuse « Jean-Luc : NON » et « JEAN-LUCAS »",
      lambda: ver(remplace("tp", valide_par="Jean-Luc : NON")) != [] and ver(remplace("tp", valide_par="JEAN-LUCAS")) != []
      and ver(remplace("tp", valide_par=_validation.replace(" le ", " NON "))) != [])
    e("DECLINER : un même ensemble dans un autre ordre est un doublon",
      lambda: ver(remplace("univers", valeurs_a_essayer="TTE,ENGI;ENGI,TTE")) != [])
    e("DECLINER refuse un code d'univers étranger à la fiche", lambda: ver(remplace("univers", valeurs_a_essayer=valid[3]["valeurs_a_essayer"] + ";BNP")) != [])
    e("DECLINER refuse un code hors univers (MT)", lambda: ver(remplace("univers", valeurs_a_essayer=valid[3]["valeurs_a_essayer"] + ";MT")) != [])
    e("DECLINER refuse une valeur_fiche qui contredit le registre", lambda: ver(remplace("tp", valeur_fiche="3", valeurs_a_essayer="2;3")) != [])
    e("DECLINER refuse un objectif de 0 ou de 60 %", lambda: ver(remplace("tp", valeurs_a_essayer="0;4;60")) != [])
    e("DECLINER refuse un réglage du signal marqué jouable", lambda: ver(remplace("seuil_cci", jouable="OUI")) != [])
    e("DECLINER refuse une stratégie de forme dangereuse", lambda: ver([dict(l, strategie="../X") for l in valid]) != [])
    e("DECLINER refuse une stratégie absente du registre", lambda: decl.verifier(valid, None, codes) != [])
    cols, vers = decl.decliner(valid)
    e("DECLINER : 1 100 versions, identifiants uniques",
      lambda: len(vers) == 1100 and len({v["id_version"] for v in vers}) == 1100)
    e("DECLINER : forme de l'identifiant C5E10-OBS-V1-E01-0001", lambda: vers[0]["id_version"] == "C5E10-OBS-V1-E01-0001")
    fiche_v = [v for v in vers if v["version_de_la_fiche"] == "OUI"]
    e("DECLINER : une seule version de la fiche, tp 0.04, sl 0.025, horizon 20",
      lambda: [(v["tp"], v["sl"], v["horizon"]) for v in fiche_v] == [("0.04", "0.025", "20")])
    e("DECLINER : le nombre total voyage avec chaque ligne", lambda: all(v["versions_dans_l_essai"] == "1100" for v in vers))

    fiche_jouable = lambda v: fusionner(reg, v)  # noqa: E731
    e("JUGE : la version de la fiche, fusionnée, passe la porte 0", lambda: juge.porte_0(fiche_jouable(fiche_v[0]))[0] is True)
    e("JUGE : pourcent lit le stop 0.5 % comme 0.005",
      lambda: juge.pourcent([v for v in vers if v["sl"] == "0.015"][0]["sl"]) == 0.015 and juge.pourcent("0.005") == 0.005)
    e("JUGE : l'univers entier se découpe en 10 codes comme le fait jouer",
      lambda: len(fiche_jouable(fiche_v[0])["univers"].split(",")) == 10)
    f_valid = ecrire_tableau(os.path.join(d, "valide.csv"), valid)
    d2 = dossier_temporaire()
    e("DECLINER main rend 0 sur un tableau validé", lambda: decl.main([registre, f_valid, d2]) == 0)
    e("DECLINER main refuse d'écraser", lambda: decl.main([registre, f_valid, d2]) == 1)
    e("DECLINER main refuse un tableau non validé", lambda: decl.main([registre, sortie, dossier_temporaire()]) == 1)
    e("PREPARER voit une écriture abîmée (relecture)",
      lambda: ecriture_abimee(prep, lambda: prep.main([registre, "C5E10-OBS-V1", f_v, "E07", dossier_temporaire()])) == 1)
    e("DECLINER voit une écriture abîmée (relecture)",
      lambda: ecriture_abimee(decl, lambda: decl.main([registre, f_valid, dossier_temporaire()])) == 1)
    e("DECLINER main : le fichier relu porte 1 100 lignes",
      lambda: len(decl.lire_tableau(os.path.join(d2, "COMBINATOIRE_C5E10-OBS-V1_E01.csv"))) == 1100)
    return R


SABOTAGES = [
    (P_PREP, "le signe n'est plus retiré", "return abs(float(t.replace", "return (float(t.replace"),
    (P_PREP, "la valeur de la fiche n'est plus gardée", "    vals.add(round(valeur, 4))\n", ""),
    (P_PREP, "les bornes ne sont plus appliquées", "vals = {v for v in vals if mini <= v <= maxi}", "vals = vals"),
    (P_PREP, "un code d'univers inconnu passe", "if not codes or inconnus:", "if not codes:"),
    (P_PREP, "l'univers est écrit avec des +", 'ensembles = [",".join(codes)]', 'ensembles = ["+".join(codes)]'),
    (P_PREP, "l'écrasement d'un essai n'est plus refusé", 'open(sortie, "x"', 'open(sortie, "w"'),
    (P_PREP, "une fiche double passe", "if len(fiches) != 1:", "if not fiches:"),
    (P_PREP, "la relecture est neutralisée", "if lire_tableau(sortie) != lignes:", "if False:"),
    (P_PREP, "le total annoncé est faux", "total *= len(", "total += len("),
    (P_DECL, "la validation n'est plus exigée", 'if not validation_valable(l):', "if False:"),
    (P_DECL, "le produit oublie le dernier réglage", "itertools.product(*listes)", "itertools.product(*listes[:-1])"),
    (P_DECL, "la version de la fiche n'est plus repérée", '"OUI" if [x[0] for x in combo] == fiche else ""', '""'),
    (P_DECL, "les doublons de valeurs passent", "if len(cles) != len(set(cles)):", "if False:"),
    (P_DECL, "l'écrasement n'est plus refusé", 'open(sortie, "x"', 'open(sortie, "w"'),
    (P_DECL, "plusieurs essais passent", "if len(essais) != 1 or", "if False and"),
    (P_DECL, "un paramètre en double passe", "if len(params) != len(set(params)):", "if False:"),
    (P_DECL, "un réglage obligatoire absent passe", '            motifs.append("réglage obligatoire absent : %s" % p)', "            pass"),
    (P_DECL, "la relecture est neutralisée", "if relu != versions or", "if False and"),
    (P_DECL, "tp et sl ne sont plus convertis en fraction", "(cle / 100)", "(cle)"),
    (P_DECL, "la forme de la stratégie n'est plus contrôlée", ' or not FORME_ID.match(next(iter(strategies)) or "")', ""),
    (P_PREP, "un pas d'horizon non entier passe", 'if p == "horizon" and not pas_entier(voisinage[p].get("pas")):', "if False:"),
    (P_PREP, "la forme de l'identifiant n'est plus contrôlée", "if not FORME_ID.match(ident):", "if False:"),
    (P_DECL, "un objectif nul ou énorme passe", "not PREPARER.POURCENT_MINIMUM <= float(t) <= PREPARER.POURCENT_MAXIMUM", "False"),
    (P_DECL, "un réglage du signal jouable passe", 'elif p in DU_SIGNAL and j != "NON":', "elif False:"),
    (P_DECL, "le moment d'achat n'est plus confronté au registre", 'if l.get("parametre") in D_ACHAT and fiche is not None and', 'if False and'),
    (P_DECL, "une ligne NON porte des valeurs sans alerte", 'if l.get("jouable") == "NON" and (l.get("valeurs_a_essayer") or "").strip():', "if False:"),
    (P_DECL, "un moment d'achat jouable passe", 'elif p in D_ACHAT and j != "NON":', "elif False:"),
    (P_PREP, "le moment d'achat et les filtres ne sont plus écrits", "    for p, libelle in REGLAGES_D_ACHAT:", "    for p, libelle in ():"),
    (P_PREP, "la valeur de la fiche n'est plus recopiée", '(fiche.get(p) or "").strip(), "", "", "NON",', '"", "", "", "NON",'),
    (P_PREP, "l'univers n'est plus mis en majuscules", "[m.strip().upper() for m in brut", "[m.strip() for m in brut"),
    (P_PREP, "deux référentiels passent", "if len(refs) != 1:", "if not refs:"),
    (P_DECL, "valeur_fiche n'est plus confrontée au registre", "f[0] != valeur_au_registre(p, fiche)", "False"),
    (P_DECL, "l'univers n'est plus confronté à la fiche", "not set(x[0]) <= permis", "False"),
    (P_PREP, "les valeurs hors univers ne sont plus écartées", '\n                        if not (l.get("hors_univers") or "").strip()}', "}"),
    (P_DECL, "n'importe quelle mention commençant par Jean-Luc valide", "if not VALIDATION.match(texte):", "if not texte.upper().startswith(\"JEAN-LUC\"):"),
    (P_DECL, "la date de validation n'est plus contrôlée", "return jour >= prepare", "return True"),
    (P_DECL, "les espaces de bord ne sont plus retirés", 'texte = (ligne.get("valide_par") or "").strip()', 'texte = (ligne.get("valide_par") or "")'),
    (P_DECL, "l'ordre d'un ensemble distingue deux doublons", "tuple(sorted(codes))", "tuple(codes)"),
    (P_PREP, "les voisins trop petits ne sont plus écartés", "if POURCENT_MINIMUM <= x <= POURCENT_MAXIMUM]", "if x > 0]"),
]


def main(argv):
    """Lance les épreuves sur les vrais programmes, puis chaque sabotage.

    ① RÔLE — Le point d'entrée.
    ② CONTEXTE D'APPEL — Le lancement en ligne de commande.
    ③ ENTRÉE — `argv` : le chemin du registre.
    ④ CONDITIONS D'ENTRÉE — Celles de l'en-tête.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2.
      [rend: 1]
    ⑥ TRAITEMENT — ① épreuves sur les vrais programmes · ② chaque sabotage doit en
      faire tomber une · ③ effacer les dossiers temporaires · ④ bilan.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un jeu d'épreuves se sabote contre sa propre correction (R-731).
    ⑨ CE QUI CLOCHE — rien vu.
    ⑩ EFFET — Dossiers temporaires, effacés.
    ⑪ TERMINAISON — Rend la main avec un code ; c'est le bloc final qui sort.
      [sort: non]
    """
    if len(argv) != 1:
        print(__doc__)
        return 2
    registre = argv[0]
    juge = charger(P_JUGE, "juge")
    with contextlib.redirect_stdout(io.StringIO()):
        res = epreuves(charger(P_PREP, "prep"), charger(P_DECL, "decl"), juge, registre)
    ok = True
    for nom, r in res:
        print(("  OK    " if r else "  ÉCHEC ") + nom)
        ok &= r
    print("ÉPREUVES : %d / %d" % (sum(r for _, r in res), len(res)))
    for chemin, nom, avant, apres in SABOTAGES:
        texte = open(chemin, encoding="utf-8").read()
        if texte.count(avant) != 1:
            print("  INAPPLICABLE  sabotage « %s » (texte trouvé %d fois)" % (nom, texte.count(avant)))
            ok = False
            continue
        texte = texte.replace(avant, apres)
        prep = charger(P_PREP, "prep_s", texte if chemin == P_PREP else None)
        decl = charger(P_DECL, "decl_s", texte if chemin == P_DECL else None)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                r = epreuves(prep, decl, juge, registre)
        except Exception as ex:  # un sabotage qui fait planter les épreuves les a fait tomber
            r = [("épreuves interrompues : %s" % type(ex).__name__, False)]
        tombees = [n for n, x in r if not x]
        print(("  ROUGIT        " if tombees else "  RESTE VERT !  ") + "sabotage « %s » : %d épreuve(s) tombée(s)" % (nom, len(tombees)))
        ok &= bool(tombees)
    for d in DOSSIERS:
        shutil.rmtree(d, ignore_errors=True)
    print("VERDICT : " + ("TOUT EST TENU" if ok else "DÉFAUT"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
