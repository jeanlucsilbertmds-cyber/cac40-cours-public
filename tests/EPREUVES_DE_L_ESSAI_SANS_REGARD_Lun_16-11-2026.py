#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_L_ESSAI_SANS_REGARD — Lun 16-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Épreuves R-731 de l'option « --essai-sans-regard » du juge des stratégies et de la moulinette
(JOUER_LES_VERSIONS), décidée par Jean-Luc le 16-11-2026 à 20h46 (A-863, « 1 » : « Option d'essai déclarée, avec
contrôle de l'identité des réglages »). Ce qu'elles prouvent : sans l'option rien ne change ; avec elle, un essai
IDENTIQUE à une fiche déjà vue (CONTRATS.FICHES_DEJA_VUES_SUR_LE_REGARD_UNIQUE, aujourd'hui C5E10-QA-V1) passe les
deux gardes du regard unique — garde M et garde du reçu, y compris dans `jouer_une_entree` et
`MODULE_C5_ETENDU_10.backtest_c5etendu10`, où l'identifiant vaut None — sans rien inscrire ni compter ; une vraie
stratégie renommée, un réglage changé d'un cran, deux versions, un dépôt (.git dossier, fichier ou lien) sont refusés
en 2 ; chaque ligne écrite est marquée « ESSAI — NI RÉSULTAT NI SÉLECTION » ; le tri refuse un fichier d'essai.
DEPUIS LE 16-11-2026 AU SOIR (A-865, A-866, A-867 ; superviseur R-759, 3e tour) : la référence de l'identité est une
EMPREINTE FIGÉE au contrat, jamais lue dans la copie — E-ancre la recalcule sur la racine reçue et rougit au moindre
écart ; A5 (référence C5E10-QA-V1 remplacée dans la copie) et A6 (code du module C5 modifié, même nom) sont refusés en
2, A6-bis (commentaire seul) est accepté ; A1 à A4b (réglage, univers, module, identifiant autorisé ou vide) refusés ;
sous l'option, le juge ne joue pas le voisinage (E10) ; une version de la moulinette qui n'a pas les réglages de la
fiche est refusée en 2 avant tout jeu (E11).

① RÔLE — Jouer E-ancre sur la racine, puis les cas E1 à E11, A1 à A6-bis et E-ancre sur la copie (Z0), puis, avec
  --saboter, les cas rapides sous chaque sabotage S1 à S18 (le juge complet sous S13, long) : chacun doit faire rougir
  TOUS les cas qu'il vise. S10 est le CORRECTIF SABOTÉ : la référence relue dans la copie fait rougir A5 et A6. E-ancre
  vérifie aussi le VERROU de la valeur figée (CONTRATS.EMPREINTE_FIGEE_CALCULEE_AVEC : étiquette FORMAT d'emp.py et
  sha256 des octets d'emp.py ; E1, point 4, du superviseur R-759 du 17-11-2026) ; S17 et S18 le sabotent.
② CONTEXTE D'APPEL — À la main, par le Chat ou un agent.
③ ENTRÉE — La ligne de commande : la racine d'un dépôt ou d'une copie (lue, jamais écrite) ; « --saboter » facultatif ;
  « --rapide » facultatif (sans les cas longs E2b, E3, E4b, E10, sur le fichier des 20 ans, ni le sabotage long
  S13) ; « --seulement=S10,S13 » facultatif (ces sabotages seuls).
④ CONDITIONS D'ENTRÉE — La racine porte programmes/, donnees/ (registre, sources), temoins/ (fichier des 20 ans, témoin
  du golden), et la fiche C5E10-QA-V1 et IND-001-RETEST au registre.
⑤ SORTIE — Le code de sortie : 0 si Z0 est conforme et, avec --saboter, si chaque sabotage mord ; 1 sinon ; 2 si
  l'épreuve n'a pas pu tourner (R-734).
  [rend: 1]
⑥ TRAITEMENT — ① une copie jetable de la racine (sans .git ; les trois gros dossiers de sources par liens durs, lus
  seulement) · ② PREPARER_LA_MOULINETTE_D_ESSAI y écrit ESSAI-C5-2000-2026 ; on ajoute ESSAI-IND-001 (la DERNIÈRE ligne
  d'IND-001-RETEST, vraie ligne, R-732, sous un autre identifiant) et ESSAI-C5-TP (la ligne d'essai, tp +4.0 % → +4.4 %,
  un cran du voisinage à ±10 %) · ③ cas unitaires dans un sous-processus qui importe les programmes de la copie ·
  ④ cas en ligne de commande · ⑤ sous --saboter, chaque sabotage est écrit dans la copie, les cas rapides rejoués, le
  programme remis.
⑦ UNITÉ — Des secondes (délai de chaque lancement : DELAI).
⑧ POURQUOI — R-731 : épreuves à la main avec sabotages ; R-732 : une vraie ligne ; un jeu d'épreuves se sabote contre
  sa propre correction.
⑨ CE QUI CLOCHE — ① Le « clone avec .git » d'E2 est la copie où `git init` pose un vrai dépôt le temps du cas, pas un
  clone du dépôt distant. ② Les cas longs (E2b, E3, E4b) ne sont pas rejoués sous sabotage (plus de 10 minutes) : les
  sabotages visent des propriétés que les cas rapides voient. ③ La racine reçue n'est que lue : l'empreinte de son
  registre est comparée avant et après. ④ La valeur figée n'est plus recopiée ici (constante EMPREINTE_FIGEE retirée
  le 17-11-2026, correction du superviseur R-759) : ce n'était pas un témoin voulu mais la cible du sabotage S11 ; une
  recopie diverge toujours de sa source (R-708). S11 la lit désormais dans l'arbre de CONTRATS. ⑤ Le verrou d'E-ancre
  porte sur les OCTETS d'emp.py : un commentaire changé dans emp.py le fait rougir (voulu ; la marche à suivre est
  écrite au contrat, à côté de la valeur figée).
⑩ EFFET — Crée et efface un dossier temporaire ; n'écrit rien dans la racine reçue.
⑪ TERMINAISON — Sort par sys.exit. Un de mes appels peut-il ne pas revenir ? Chaque lancement est borné à DELAI.
  [sort: oui]
"""
import csv
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

JUGE = os.path.join("programmes", "JUGE_DES_STRATEGIES.py")
MOULINETTE = os.path.join("programmes", "JOUER_LES_VERSIONS.py")
TRI = os.path.join("programmes", "TRIER_LES_VARIANTES.py")
PREPARER = os.path.join("programmes", "PREPARER_LA_MOULINETTE_D_ESSAI.py")
REGISTRE = os.path.join("donnees", "cac40_strategies.csv")
COMBINATOIRE = os.path.join("donnees", "combinatoires", "COMBINATOIRE_ESSAI-C5-2000-2026_E01.csv")
VINGT_ANS = "temoins/TEMOIN_VINGT_ANS_2000_2026_COUPURE_2026-11-11_FIGE_Ven_13-11-2026_10h59.csv"
OPTION = "--essai-sans-regard"
MARQUE = "ESSAI — NI RÉSULTAT NI SÉLECTION · "
EXCLUS = (".git", "etudes", "archives", "rapports", os.path.join("temoins", "archives_web"), "__pycache__")
PAR_LIENS = (os.path.join("donnees", "sources_bnains"), os.path.join("donnees", "sources_francfort"),
             os.path.join("donnees", "sources_yahoo"))
DELAI = 400

# LE MODULE DE SIGNAL DE C5E10-QA-V1, celui que la fiche d'essai recopie (cas A6 et A6-bis)
MODULE_C5 = os.path.join("programmes", "MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py")


def changer_la_valeur_figee(texte):
    """Change d'un caractère la valeur figée de C5E10-QA-V1 dans le texte de CONTRATS (sabotage S11).
    ① RÔLE — Faire rougir E-ancre par la constante. ② CONTEXTE D'APPEL — `main`, sous --saboter. ③ ENTRÉE — le texte
    de programmes/CONTRATS_DES_FICHIERS.py de la copie. ④ CONDITIONS D'ENTRÉE — il définit
    FICHES_DEJA_VUES_SUR_LE_REGARD_UNIQUE en littéral, avec C5E10-QA-V1 → (qui, valeur), et la valeur y figure une fois.
    ⑤ SORTIE — UNE valeur : le texte saboté. [rend: 1] ⑥ TRAITEMENT — lire la valeur dans l'ARBRE du texte
    (`ast.literal_eval` de l'affectation), puis changer son dernier caractère — vers « 1 » s'il vaut « 0 », sinon vers
    « 0 » (la valeur emp-v2 finit par 0 : la remplacer par « 0 » ne changeait rien, et l'épreuve s'arrêtait en 2,
    mesuré le 17-11-2026). ⑦ UNITÉ — — ⑧ POURQUOI — La valeur était RECOPIÉE ici (EMPREINTE_FIGEE, ancienne ligne 77) : deux
    implémentations d'une même chose divergent toujours (R-708). Correction du superviseur R-759 du 17-11-2026 : la
    lire depuis CONTRATS, la seule source. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main ; lève
    ValueError si la valeur est introuvable ou présente plus d'une fois. [sort: non]"""
    import ast
    valeur = None
    for n in ast.parse(texte).body:
        if (isinstance(n, ast.Assign) and any(isinstance(c, ast.Name) and c.id == "FICHES_DEJA_VUES_SUR_LE_REGARD_UNIQUE"
                                              for c in n.targets)):
            valeur = ast.literal_eval(n.value)["C5E10-QA-V1"][1]
    if not valeur or texte.count(valeur) != 1:
        raise ValueError("valeur figée de C5E10-QA-V1 introuvable ou répétée dans CONTRATS : %r" % valeur)
    return texte.replace(valeur, valeur[:-1] + ("1" if valeur.endswith("0") else "0"))


def saboter_un_reglage_de_c5(texte):
    """Change d'un caractère le tp de la DERNIÈRE ligne de C5E10-QA-V1 du registre (sabotage S12).
    ① RÔLE — Faire rougir E-ancre par un réglage de la fiche autorisée. ② CONTEXTE D'APPEL — `main`, sous --saboter.
    ③ ENTRÉE — le texte du registre. ④ CONDITIONS D'ENTRÉE — la ligne porte « ,+4.0%, » une fois. ⑤ SORTIE — UNE
    valeur : le texte saboté. [rend: 1] ⑥ TRAITEMENT — « +4.0% » devient « +4.1% » sur cette ligne seule.
    ⑦ UNITÉ — — ⑧ POURQUOI — superviseur R-759 (3e tour) : l'épreuve E-ancre rougit si l'on change d'un caractère
    un réglage de C5E10-QA-V1. ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — Rend la main ; lève ValueError si
    la ligne n'a pas la forme attendue. [sort: non]"""
    lignes = texte.splitlines(True)
    i = max(k for k, l in enumerate(lignes) if l.startswith("C5E10-QA-V1,"))
    if lignes[i].count(",+4.0%,") != 1:
        raise ValueError("ligne C5E10-QA-V1 inattendue : %r" % lignes[i][:120])
    lignes[i] = lignes[i].replace(",+4.0%,", ",+4.1%,")
    return "".join(lignes)


# Chaque sabotage : (fichier, [(ancien, nouveau), ...] ou une fonction texte → texte, préfixes des cas qui doivent
# TOUS rougir, long). Un sabotage « long » se joue sur le juge complet (`juge_d_essai_complet`), pas sur les cas rapides.
SABOTAGES = {
    "S1_identite_retiree": (JUGE, [("        if empreinte == reference:\n            return JetonDEssai(",
                                    "        if True:\n            return JetonDEssai(")], "E1"),
    "S2_refus_du_git_retire": (JUGE, [
        ('    if os.path.lexists(os.path.join(racine, ".git")):\n        return None, "%s porte .git',
         '    if False:\n        return None, "%s porte .git'),
        ('    if os.path.lexists(os.path.join(jeton.racine, ".git")):', "    if False:"),
        ('        if os.path.lexists(os.path.join(base, ".git")):\n            print("ARRET (essai refusé)',
         '        if False:\n            print("ARRET (essai refusé)')], "E2"),
    "S3_plus_d_une_version_admise": (JUGE, [("    if versions != 1:", "    if False:")], "E6"),
    "S4_tri_accepte_l_essai": (TRI, [("        raise ValueError(\"%s : fichier d'ESSAI",
                                      "        ValueError(\"%s : fichier d'ESSAI")], "E7"),
    "S5_garde_du_regard_sans_jeton": (JUGE, [("    if isinstance(recu, JetonDEssai):\n        _ok, _motif",
                                              "    if False:\n        _ok, _motif")], "E4"),
    "S6_garde_m_sans_jeton": (JUGE, [("    if m_regard and _jeton_valable(jeton,",
                                      "    if False and _jeton_valable(jeton,")], "E4"),
    "S7_sortie_non_marquee": (JUGE, [("    if not isinstance(sys.stdout, _SortieMarquee):\n        sys.stdout =",
                                      "    if False:\n        sys.stdout =")], "E1"),
    "S8_jeton_d_un_autre_module_admis": (JUGE, [("    if nom_du_module is not None and nom_du_module != jeton.module:",
                                                 "    if False:")], "E4"),
    "S9_jeton_d_une_autre_fiche_admis": (JUGE, [("    if qui is not None and qui != jeton.fiche_id:", "    if False:")],
                                         "E4"),
    # S10 — LE CORRECTIF SABOTÉ (superviseur R-759, 3e tour) : la référence relue dans la copie, comme avant A-865.
    "S10_reference_relue_dans_la_copie": (JUGE, [(
        "        reference = valeurs[1]",
        "        reference = empreinte_des_reglages(dict(_C.fiches_du_registre(trouver(racine, "
        "_C.NOM_DU_REGISTRE_DES_STRATEGIES)).get(aut) or {}, id=propre.get(\"id\"), periode=propre.get(\"periode\"), "
        "statut=propre.get(\"statut\")), lire_module)[0]")], ("A5", "A6 ")),
    # S11 : le dernier caractère de la valeur figée changé, valeur LUE dans CONTRATS (`changer_la_valeur_figee`).
    "S11_constante_changee_d_un_caractere": (os.path.join("programmes", "CONTRATS_DES_FICHIERS.py"),
                                             changer_la_valeur_figee, "E-ancre"),
    "S12_reglage_de_C5E10_change_d_un_caractere": (REGISTRE, saboter_un_reglage_de_c5, "E-ancre"),
    "S13_voisinage_joue_sous_jeton": (JUGE, [("    if jeton is not None:\n        # A-866", "    if False:\n        # A-866")],
                                      "E10", True),
    "S14_identifiant_vide_admis": (JUGE, [("    if not ident.strip():", "    if False:")], "A4b"),
    "S15_version_differente_jouee": (MOULINETTE, [("        if _emp_v != _emp_f:", "        if False:")], "E11"),
    # S16 — la version de Python retirée du motif de refus (superviseur R-759 du 17-11-2026, point 5).
    "S16_version_de_python_retiree_du_motif": (JUGE, [('"%d.%d.%d" % sys.version_info[:3])', '"")')], ("A5", "A6 ")),
    # S17 et S18 — LE VERROU de la valeur figée (E1, point 4, du superviseur R-759 du 17-11-2026) : un octet d'emp.py
    # changé (un commentaire ajouté à la fin : la valeur figée ne bouge pas, seul le sha256 change) ; l'étiquette
    # rangée au contrat changée. E-ancre doit rougir sous chacun.
    "S17_emp_py_change_d_un_octet": ("emp.py", lambda texte: texte + "# octet ajouté par le sabotage S17\n", "E-ancre"),
    "S18_etiquette_du_verrou_changee": (os.path.join("programmes", "CONTRATS_DES_FICHIERS.py"),
                                        [('    "format": "emp-v2",\n', '    "format": "emp-v9",\n')], "E-ancre"),
}

# Le sous-processus des cas unitaires : il importe les programmes DE LA COPIE (sabotés ou non) et rend un JSON
# {cas : texte de l'écart} ; vide si tout est conforme.
UNITE = r'''
import csv, io, json, os, subprocess, sys
copie = sys.argv[1]
sys.path.insert(0, os.path.join(copie, "programmes"))
import JUGE_DES_STRATEGIES as J, CONTRATS_DES_FICHIERS as C
faux = {}
def ecart(cas, texte):
    faux.setdefault(cas, texte)
reg = C.fiches_du_registre(J.trouver(copie, C.NOM_DU_REGISTRE_DES_STRATEGIES))
essai, ind, tp = reg["ESSAI-C5-2000-2026"], reg["ESSAI-IND-001"], reg["ESSAI-C5-TP"]
# E1 : une vraie fiche (IND-001-RETEST) recopiée sous ESSAI-IND-001
j, m = J.jeton_d_essai(copie, ind, 1)
if j is not None or "identique à aucune" not in (m or ""):
    ecart("E1 vraie fiche renommée", "jeton %r, motif %r" % (j, m))
# E5 : un cran de tp — refusé par l'empreinte des réglages figée (A-865)
j, m = J.jeton_d_essai(copie, tp, 1)
if j is not None or "empreinte des réglages" not in (m or ""):
    ecart("E5 tp d'un cran", "jeton %r, motif %r" % (j, m))
# A1 à A4b : la fiche d'essai changée d'un réglage, d'univers, de module ou d'identifiant (attaques du relecteur neuf
# du 16-11-2026, RELECTEUR_ESSAI_SANS_REGARD) ; chacune doit être REFUSÉE, sans panne.
_moins_une = ",".join(essai["univers"].split(",")[:-1])
for nom, cases in (("A1 sl", {"sl": "-2.6%"}), ("A1 horizon", {"horizon": "21"}), ("A1 tp", {"tp": "+4.1%"}),
                   ("A1 fonction", {"fonction_signal": "autre"}),
                   ("A2 univers sans sa dernière valeur", {"univers": _moins_une}),
                   ("A3 autre module", {"module_signal": ind["module_signal"],
                                        "fonction_signal": ind["fonction_signal"]}),
                   ("A4 identifiant d'une fiche autorisée", {"id": "C5E10-QA-V1"}),
                   ("A4b identifiant vide", {"id": ""}), ("A4b identifiant blanc", {"id": "  "})):
    try:
        j, m = J.jeton_d_essai(copie, dict(essai, **cases), 1)
    except Exception as e:
        ecart(nom, "refus par une panne : %s : %s" % (type(e).__name__, str(e)[:160]))
        continue
    if j is not None:
        ecart(nom, "jeton accordé")
# E6 : deux versions
j, m = J.jeton_d_essai(copie, essai, 2)
if j is not None or "versions" not in (m or ""):
    ecart("E6 deux versions", "jeton %r, motif %r" % (j, m))
# E4 : l'essai identique passe les deux gardes, y compris là où l'identifiant vaut None
jeton, m = J.jeton_d_essai(copie, essai, 1)
if jeton is None:
    ecart("E4 jeton de l'essai identique", m)
else:
    cours = J.charger_cours(os.path.join(copie, sys.argv[2]))
    import importlib.util
    pos = J.charger_module(J.trouver(copie, "MODULE_POSITIONS.py"), "pos_unite")
    v = sorted(k for k in cours if any(str(b["date"]).startswith("2005") for b in cours[k]))[0]
    serie = [b for b in cours[v] if "2004-06" <= str(b["date"]) <= "2006-12-31"]
    k = next(i for i, b in enumerate(serie) if str(b["date"]) >= "2005-03-01")
    try:
        J.jouer_une_entree(v, serie, k, 0.04, 0.025, 20, pos, None, None, jeton)
    except Exception as e:
        ecart("E4 jouer_une_entree avec le jeton", "%s : %s" % (type(e).__name__, str(e)[:200]))
    try:
        J.jouer_une_entree(v, serie, k, 0.04, 0.025, 20, pos, None, None, None)
        ecart("E4 jouer_une_entree sans jeton", "admise dans la fenêtre sans reçu")
    except J.RegardNonInscrit:
        pass
    sig = J.signal_de_la_fiche(copie, essai)
    c5 = sig.module
    v5 = c5.C5E10_UNIVERS[0]
    cle = J.table_mnemoniques(J.trouver(copie, "REFERENTIEL_VALEURS")).get(v5, v5)
    barres = [b for b in cours.get(cle, cours.get(v5, [])) if "2004-01-01" <= str(b["date"]) <= "2006-12-31"]
    if not barres:
        ecart("E4 backtest C5", "aucune barre de %s en 2004-2006" % v5)
    else:
        try:
            c5.backtest_c5etendu10({v5: barres}, bareme="HIST_FORFAIT_300", recu=jeton)
        except Exception as e:
            ecart("E4 backtest C5 avec le jeton", "%s : %s" % (type(e).__name__, str(e)[:200]))
        try:
            c5.backtest_c5etendu10({v5: barres}, bareme="HIST_FORFAIT_300")
            ecart("E4 backtest C5 sans jeton", "admis dans la fenêtre sans reçu")
        except J.RegardNonInscrit:
            pass
    for qui, mod, nom in ((None, None, "qui None"), ("ESSAI-C5-2000-2026", None, "sa fiche")):
        try:
            J._garde_du_regard_unique(qui, "2005-01-03", "2005-02-01", ("2005-01-03", "2005-02-01"), jeton, mod)
        except Exception as e:
            ecart("E4 garde du regard, " + nom, "%s : %s" % (type(e).__name__, str(e)[:200]))
    for qui, mod, nom in (("C5E10-QA-V1", None, "autre fiche"), (None, "AUTRE_MODULE.py", "autre module")):
        try:
            J._garde_du_regard_unique(qui, "2005-01-03", "2005-02-01", ("2005-01-03", "2005-02-01"), jeton, mod)
            ecart("E4 garde du regard, " + nom, "jeton admis")
        except J.RegardNonInscrit:
            pass
        except Exception as e:
            ecart("E4 garde du regard, " + nom, "refus par une panne : %s : %s" % (type(e).__name__, str(e)[:160]))
    faux_jeton = J.JetonDEssai(copie, jeton.fiche_id, jeton.module, object())
    try:
        J._garde_du_regard_unique(None, "2005-01-03", "2005-02-01", ("2005-01-03", "2005-02-01"), faux_jeton)
        ecart("E4 jeton sans sceau", "admis")
    except J.RegardNonInscrit:
        pass
    except Exception as e:
        ecart("E4 jeton sans sceau", "refus par une panne : %s : %s" % (type(e).__name__, str(e)[:160]))
    per = ("2000-01-03", "2026-10-29")
    l_avec, r_avec = J.garde_composition(copie, essai, per, jeton)
    l_sans, r_sans = J.garde_composition(copie, essai, per)
    if r_avec or not r_sans or l_avec != l_sans:
        ecart("E4 garde M", "avec jeton %r ; sans jeton %r" % (r_avec[:80], r_sans[:80]))
    # E9 : .git en fichier, puis en lien, posé APRÈS la déclaration
    g = os.path.join(copie, ".git")
    for forme in ("fichier", "lien"):
        if forme == "fichier":
            open(g, "w").write("gitdir: /nulle/part\n")
        else:
            os.symlink("/tmp", g)
        try:
            if J._jeton_valable(jeton, None)[0]:
                ecart("E9 .git " + forme, "jeton encore valable")
            if J.jeton_d_essai(copie, essai, 1)[0] is not None:
                ecart("E9 .git " + forme, "jeton rendu")
        finally:
            os.remove(g)
# E7 : un fichier de résultats d'essai, synthétique, refusé par le tri
import TRIER_LES_VARIANTES as T
champs = list(C.RESULTATS_DES_VERSIONS)
for nom, entete, valeur in (("colonne", champs + [C.COLONNE_DU_STATUT_D_ESSAI], C.STATUT_D_ESSAI),
                            ("marque", champs, None)):
    f = os.path.join(sys.argv[3], "RESULTATS_%s.csv" % nom)
    with open(f, "w", encoding="utf-8", newline="") as s:
        w = csv.DictWriter(s, fieldnames=entete)
        w.writeheader()
        ligne = {c: "" for c in entete}
        ligne.update({"id_version": "X-E01-0001", "strategie": "X", "essai": "E01", "versions_dans_l_essai": "1"})
        if valeur:
            ligne[C.COLONNE_DU_STATUT_D_ESSAI] = valeur
        else:
            ligne["bareme"] = C.STATUT_D_ESSAI
        w.writerow(ligne)
    try:
        T.lire_les_resultats(f, C)
        ecart("E7 tri, " + nom, "fichier d'essai lu")
    except ValueError as e:
        if "fichier d'ESSAI" not in str(e):
            ecart("E7 tri, " + nom, "refus pour une autre raison : %s" % str(e)[:160])
print(json.dumps(faux, ensure_ascii=False))
'''


def empreinte(chemin):
    """Rend les seize premiers caractères du SHA-256 d'un fichier. ① RÔLE — Comparer à l'octet. ② CONTEXTE D'APPEL —
    `main`, `etat`. ③ ENTRÉE — un chemin. ④ CONDITIONS D'ENTRÉE — le fichier existe. ⑤ SORTIE — UNE valeur : 16
    caractères hexadécimaux. [rend: 1] ⑥ TRAITEMENT — hashlib. ⑦ UNITÉ — — ⑧ POURQUOI — « identique à l'octet ».
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lit le fichier. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def copie_jetable(racine):
    """Fabrique une copie jetable de la racine, sans .git, et rend son chemin. ① RÔLE — Ne jamais écrire la racine.
    ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — la racine. ④ CONDITIONS D'ENTRÉE — fiche en tête, ④. ⑤ SORTIE — UNE
    valeur : le chemin de la copie. [rend: 1] ⑥ TRAITEMENT — tout sauf EXCLUS ; les dossiers PAR_LIENS par liens durs.
    ⑦ UNITÉ — — ⑧ POURQUOI — 130 Mo au lieu de 640 ; les sources ne sont que lues par le juge et la moulinette.
    ⑨ CE QUI CLOCHE — Un programme qui ÉCRIRAIT dans une source liée écrirait la racine : aucun ne le fait ici.
    ⑩ EFFET — Crée un dossier temporaire. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    d = os.path.join(tempfile.mkdtemp(prefix="essai_sans_regard_"), "copie")
    racine = os.path.abspath(racine)

    def ignorer(dossier, noms):
        """Rend les noms à ne pas copier. ① RÔLE — EXCLUS et PAR_LIENS. ② CONTEXTE D'APPEL — copytree. ③ ENTRÉE — le
        dossier, ses noms. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la liste. [rend: 1] ⑥ TRAITEMENT —
        comparer les chemins relatifs. ⑦ UNITÉ — — ⑧ POURQUOI — voir la fonction. ⑨ CE QUI CLOCHE — — ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main. [sort: non]"""
        rel = os.path.relpath(dossier, racine)
        return [n for n in noms if os.path.normpath(os.path.join(rel, n)) in EXCLUS + PAR_LIENS
                or n in ("__pycache__", ".git") or (rel == "temoins" and n.startswith("DOCUMENTS_"))]
    shutil.copytree(racine, d, ignore=ignorer, symlinks=True)
    for p in PAR_LIENS:
        if os.path.isdir(os.path.join(racine, p)):
            shutil.copytree(os.path.join(racine, p), os.path.join(d, p), copy_function=os.link)
    return d


def lancer(copie, *arguments):
    """Lance un programme de la copie ; rend (code, sortie). ① RÔLE — Un lancement borné. ② CONTEXTE D'APPEL — les cas.
    ③ ENTRÉE — la copie ; le programme et ses arguments. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — DEUX valeurs : le code
    (124 au délai) ; la sortie et les erreurs. [rend: 2] ⑥ TRAITEMENT — subprocess.run, -B, dans la copie.
    ⑦ UNITÉ — Des secondes. ⑧ POURQUOI — Le code de sortie est ce que le circuit lit. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance un processus. ⑪ TERMINAISON — Rend la main ; DELAI au plus. [sort: non]"""
    try:
        p = subprocess.run([sys.executable, "-B"] + list(arguments), capture_output=True, text=True, timeout=DELAI,
                           cwd=copie)
    except subprocess.TimeoutExpired:
        return 124, "délai dépassé"
    return p.returncode, p.stdout + p.stderr


def toutes_marquees(sortie):
    """Dit si chaque ligne non vide commence par la marque d'essai. ① RÔLE — A-863, sortie marquée. ② CONTEXTE
    D'APPEL — les cas. ③ ENTRÉE — un texte. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : vrai ou faux. [rend: 1]
    ⑥ TRAITEMENT — ligne par ligne. ⑦ UNITÉ — — ⑧ POURQUOI — Une ligne recopiée seule garde sa nature d'essai.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]"""
    lignes = [l for l in sortie.splitlines() if l.strip()]
    return bool(lignes) and all(l.startswith(MARQUE) for l in lignes)


def ajouter_les_fiches(copie):
    """Ajoute au registre de la copie ESSAI-IND-001 et ESSAI-C5-TP. ① RÔLE — Les fiches des cas E1, E2, E5.
    ② CONTEXTE D'APPEL — `main`, après PREPARER. ③ ENTRÉE — la copie. ④ CONDITIONS D'ENTRÉE — le registre porte
    IND-001-RETEST et ESSAI-C5-2000-2026 ; il finit par une fin de ligne. ⑤ SORTIE — — ⑥ TRAITEMENT — lire l'en-tête
    (première ligne hors commentaires « # »), les dernières lignes des deux identifiants, écrire deux lignes en fin.
    ⑦ UNITÉ — — ⑧ POURQUOI — E1 : une VRAIE ligne (R-732) sous un autre nom ; E5 : un cran de ±10 % sur tp.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit le registre de la copie. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    f = os.path.join(copie, REGISTRE)
    texte = open(f, encoding="utf-8-sig").read()
    lignes = [l for l in texte.splitlines(True) if not l.startswith("#")]
    entete = next(csv.reader([lignes[0]]))
    dernieres = {}
    for l in csv.DictReader(io.StringIO("".join(lignes))):
        dernieres[l["id"]] = l
    ind = dict(dernieres["IND-001-RETEST"], id="ESSAI-IND-001")
    tp = dict(dernieres["ESSAI-C5-2000-2026"], id="ESSAI-C5-TP")
    if tp["tp"] != "+4.0%":
        raise RuntimeError("tp de la fiche d'essai inattendu : %r" % tp["tp"])
    tp["tp"] = "+4.4%"
    s = io.StringIO()
    w = csv.DictWriter(s, fieldnames=entete, lineterminator="\n" if "\r\n" not in texte else "\r\n")
    w.writerow(ind)
    w.writerow(tp)
    with open(f, "a", encoding="utf-8", newline="") as sortie:
        sortie.write(s.getvalue())


def combinatoire_a_deux(copie, dossier):
    """Écrit une combinatoire de deux versions de la fiche d'essai et rend son chemin. ① RÔLE — Le cas E6 en ligne de
    commande. ② CONTEXTE D'APPEL — `cas_rapides`. ③ ENTRÉE — la copie ; un dossier où écrire. ④ CONDITIONS D'ENTRÉE —
    PREPARER a écrit la combinatoire d'une version. ⑤ SORTIE — UNE valeur : le chemin. [rend: 1] ⑥ TRAITEMENT — la
    ligne recopiée sous un second identifiant, non marquée identique ; « versions_dans_l_essai » à 2. ⑦ UNITÉ — —
    ⑧ POURQUOI — La moulinette contrôle l'annonce avant l'essai : elle doit être cohérente pour atteindre le refus.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit un fichier. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    lignes = list(csv.DictReader(open(os.path.join(copie, COMBINATOIRE), encoding="utf-8-sig")))
    champs = list(lignes[0].keys())
    deux = [dict(lignes[0], versions_dans_l_essai="2"),
            dict(lignes[0], id_version=lignes[0]["id_version"][:-4] + "0002", versions_dans_l_essai="2",
                 version_de_la_fiche="")]
    f = os.path.join(dossier, "COMBINATOIRE_ESSAI-C5-2000-2026_E01.csv")
    with open(f, "w", encoding="utf-8", newline="") as s:
        w = csv.DictWriter(s, fieldnames=champs)
        w.writeheader()
        w.writerows(deux)
    return f


# E-ANCRE (superviseur R-759, 3e tour ; A-865) : la valeur figée au contrat est ÉGALE à l'empreinte recalculée depuis
# le registre et le module de la racine — la fiche C5E10-QA-V1 (dernière ligne), alignée sur l'identifiant, la période
# et le statut de la fiche d'essai par les fonctions mêmes de PREPARER_LA_MOULINETTE_D_ESSAI (R-708), période prise
# sur le témoin figé des 20 ans. Rend un JSON {calculee, figee, jouable}.
ANCRE = r'''
import json, os, sys
racine = sys.argv[1]
sys.path.insert(0, os.path.join(racine, "programmes"))
import hashlib
import JUGE_DES_STRATEGIES as J, CONTRATS_DES_FICHIERS as C, PREPARER_LA_MOULINETTE_D_ESSAI as P
src = C.fiches_du_registre(J.trouver(racine, C.NOM_DU_REGISTRE_DES_STRATEGIES))["C5E10-QA-V1"]
entete = list(src)
debut, fin = P.periode_d_essai(P.seances_du_fichier(os.path.join(racine, P.COURS_DES_VINGT_ANS)))
fiche = dict(zip(entete, P.ligne_d_essai(entete, [src[c] for c in entete], debut, fin)))
calculee, jouable = J.empreinte_des_reglages(fiche, J.lire_module_du_jour(racine))
figee = C.FICHES_DEJA_VUES_SUR_LE_REGARD_UNIQUE.get("C5E10-QA-V1")
# LE VERROU (E1, point 4, du superviseur R-759 du 17-11-2026) : l'étiquette d'emp.py et le sha256 de ses octets, lus
# sur la racine, doivent être ceux rangés au contrat avec la valeur figée.
sys.path.insert(0, racine)
import emp
verrou = getattr(C, "EMPREINTE_FIGEE_CALCULEE_AVEC", None) or {}
octets = hashlib.sha256(open(os.path.join(racine, "emp.py"), "rb").read()).hexdigest()
print(json.dumps({"calculee": calculee, "jouable": jouable,
                  "figee": repr(figee[1] if isinstance(figee, tuple) and len(figee) == 2 else figee),
                  "egale": isinstance(figee, tuple) and len(figee) == 2 and figee[1] == calculee,
                  "format": [getattr(emp, "FORMAT", None), verrou.get("format")],
                  "sha256_emp_py": [octets, verrou.get("sha256_des_octets_d_emp_py")],
                  "verrou_tenu": bool(verrou) and getattr(emp, "FORMAT", None) == verrou.get("format")
                                 and octets == verrou.get("sha256_des_octets_d_emp_py"),
                  "emp_charge": os.path.abspath(emp.__file__)}))
'''

# LE JETON D'UNE FICHE DU REGISTRE DE LA COPIE : imprime « ACCORDÉ » ou « REFUS : <motif> ».
JETON = r'''
import os, sys
copie, ident = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(copie, "programmes"))
import JUGE_DES_STRATEGIES as J, CONTRATS_DES_FICHIERS as C
f = C.fiches_du_registre(J.trouver(copie, C.NOM_DU_REGISTRE_DES_STRATEGIES))[ident]
j, m = J.jeton_d_essai(copie, f, 1)
print("ACCORDÉ" if j is not None else "REFUS : %s" % m)
'''


def cas_e_ancre(racine):
    """Joue E-ancre sur une racine ; rend la liste des cas faux. ① RÔLE — Prouver que la valeur figée au contrat
    (A-865) est celle que le registre et le module de la racine donnent aujourd'hui. ② CONTEXTE D'APPEL — `main` (sur
    la racine reçue : dans le circuit, la version éprouvée) ; `cas_rapides` (sur la copie, rejoué sous S11 et S12).
    ③ ENTRÉE — une racine, seulement lue. ④ CONDITIONS D'ENTRÉE — elle porte PREPARER, le registre, le témoin des
    20 ans. ⑤ SORTIE — UNE valeur : la liste (vide si tout tient ; jusqu'à deux cas faux : la valeur, le verrou).
    [rend: 1] ⑥ TRAITEMENT — ANCRE dans un sous-processus : valeur recalculée contre valeur figée ; puis le VERROU —
    étiquette FORMAT d'emp.py et sha256 des octets d'emp.py de la racine contre CONTRATS.EMPREINTE_FIGEE_CALCULEE_AVEC.
    ⑦ UNITÉ — — ⑧ POURQUOI — Superviseur R-759 (3e tour), point 4 : figer n'est pas une recopie fautive (R-708) si une
    épreuve la recalcule et rougit au moindre écart (modèle : les sha256 des témoins figés au contrat). Point 5 : si C5
    change légitimement, cette épreuve rougit — voulu (A-754), la décision revient à Jean-Luc. Le verrou : E1, point
    4, du superviseur R-759 du 17-11-2026 — un emp.py affaibli suivi d'un recalcul de la valeur rendait tout vert
    (MAJ-1 du relecteur). ⑨ CE QUI CLOCHE — Le verrou porte sur les octets : un commentaire changé dans emp.py le fait
    rougir (voulu, marche à suivre au contrat). ⑩ EFFET —
    Lance un processus. ⑪ TERMINAISON — Rend la main ; DELAI au plus. [sort: non]"""
    code, sortie = lancer(racine, "-c", ANCRE, racine)
    try:
        r = json.loads(sortie.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return ["E-ancre n'a pas tourné : code %d, %r" % (code, sortie[-300:])]
    print("  E-ancre %s sous Python %d.%d.%d : calculée %s, jouable %s, figée %s" % (
        (os.path.basename(racine),) + sys.version_info[:3] + (r["calculee"], r["jouable"], r["figee"])))
    print("  E-ancre verrou : étiquette emp.py %s / contrat %s · sha256 emp.py %s… / contrat %s… · emp chargé : %s" % (
        r["format"][0], r["format"][1], r["sha256_emp_py"][0][:16], str(r["sha256_emp_py"][1])[:16], r["emp_charge"]))
    faux = []
    if not (r["egale"] and r["jouable"]):
        faux.append("E-ancre : calculée %s (jouable %s), figée %s" % (r["calculee"], r["jouable"], r["figee"]))
    if not r["verrou_tenu"]:
        faux.append("E-ancre : verrou rompu — étiquette %s contre %s au contrat ; sha256 d'emp.py %s contre %s au "
                    "contrat (tout recalcul : mutation verte, FORMAT changé, décision de Jean-Luc ; CONTRATS, "
                    "EMPREINTE_FIGEE_CALCULEE_AVEC)" % (r["format"][0], r["format"][1], r["sha256_emp_py"][0],
                                                        r["sha256_emp_py"][1]))
    return faux


def lignes_du_registre(copie):
    """Rend l'en-tête et la DERNIÈRE ligne de chaque identifiant du registre de la copie. ① RÔLE — Fabriquer les
    lignes d'A5. ② CONTEXTE D'APPEL — `cas_de_la_reference`. ③ ENTRÉE — la copie. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : l'en-tête ; {id : ligne}. [rend: 2] ⑥ TRAITEMENT — csv, hors commentaires « # ».
    ⑦ UNITÉ — — ⑧ POURQUOI — la dernière ligne d'un identifiant fait foi (n°83). ⑨ CE QUI CLOCHE — — ⑩ EFFET —
    Lit le registre. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    texte = open(os.path.join(copie, REGISTRE), encoding="utf-8-sig").read()
    lignes = [l for l in texte.splitlines(True) if not l.startswith("#")]
    dernieres = {}
    for l in csv.DictReader(io.StringIO("".join(lignes))):
        dernieres[l["id"]] = l
    return next(csv.reader([lignes[0]])), dernieres


def cas_de_la_reference(copie):
    """Joue A5, A6 et A6-bis : la RÉFÉRENCE changée dans la copie ; rend la liste des cas faux.
    ① RÔLE — Le défaut B1 du relecteur neuf du 16-11-2026 : la référence de l'identité était lue dans la copie.
    ② CONTEXTE D'APPEL — `cas_rapides` (donc sous chaque sabotage, dont S10, le correctif saboté).
    ③ ENTRÉE — la copie préparée. ④ CONDITIONS D'ENTRÉE — `ajouter_les_fiches` a tourné. ⑤ SORTIE — UNE valeur : la
    liste. [rend: 1] ⑥ TRAITEMENT — A5 : au registre, une ligne C5E10-QA-V1 qui recopie IND-001-RETEST (elle devient
    la dernière, donc celle qui fait foi), puis ESSAI-A5, la même recopie sous l'identifiant, la période et le statut
    de l'essai → jeton refusé, juge en 2 · A6 : une ligne de CODE ajoutée au module C5, même nom → refusé, juge en 2 ·
    A6-bis : un COMMENTAIRE seul ajouté au module → jeton ACCORDÉ. Registre et module remis à l'octet après chaque cas.
    Un refus doit nommer la version exacte de Python qui a calculé (superviseur R-759 du 17-11-2026, point 5 ; S16).
    ⑦ UNITÉ — — ⑧ POURQUOI — Superviseur R-759 (3e tour), épreuve demandée ; A-865. Le juge en ligne de commande
    n'est lancé que si le jeton est refusé : accordé, il jouerait la fiche (long), et le cas est déjà rouge.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit puis remet le registre et le module de la copie. ⑪ TERMINAISON — Rend la
    main ; DELAI au plus par lancement. [sort: non]"""
    faux = []
    f_reg, f_mod = os.path.join(copie, REGISTRE), os.path.join(copie, MODULE_C5)
    reg, mod = open(f_reg, "rb").read(), open(f_mod, "rb").read()
    entete, dernieres = lignes_du_registre(copie)
    essai = dernieres["ESSAI-C5-2000-2026"]
    fausse = dict(dernieres["IND-001-RETEST"], id="C5E10-QA-V1")
    a5 = dict(fausse, id="ESSAI-A5", periode=essai["periode"], statut=essai["statut"])
    s = io.StringIO()
    w = csv.DictWriter(s, fieldnames=entete, lineterminator="\r\n" if b"\r\n" in reg else "\n")
    w.writerow(fausse)
    w.writerow(a5)
    cas = (("A5 référence C5E10-QA-V1 remplacée par IND-001 dans la copie", f_reg, reg + s.getvalue().encode("utf-8"),
            "ESSAI-A5", False),
           ("A6 code du module C5 modifié, même nom", f_mod, mod + b"\n_A6_CODE_MODIFIE_DANS_LA_COPIE = 1\n",
            "ESSAI-C5-2000-2026", False),
           ("A6-bis commentaire seul ajouté au module C5", f_mod, mod + b"\n# A6-bis : un commentaire, rien d'autre\n",
            "ESSAI-C5-2000-2026", True))
    for nom, fichier, octets, ident, accorde in cas:
        origine = reg if fichier == f_reg else mod
        try:
            with open(fichier, "wb") as sortie_f:
                sortie_f.write(octets)
            code, sortie = lancer(copie, "-c", JETON, copie, ident)
            vu = (sortie.strip().splitlines() or ["(rien)"])[-1]
            if accorde:
                if vu != "ACCORDÉ":
                    faux.append("%s : jeton attendu, %r" % (nom, vu[:200]))
                continue
            if not vu.startswith("REFUS : "):
                faux.append("%s : %s" % (nom, vu[:200]))
                continue
            # LE MOTIF NOMME LA VERSION DE PYTHON (superviseur R-759 du 17-11-2026, point 5) : `lancer` prend le même
            # interpréteur que cette épreuve, donc sa version exacte doit figurer dans le motif.
            if ("sous Python %d.%d.%d" % sys.version_info[:3]) not in vu:
                faux.append("%s : le motif ne nomme pas Python %d.%d.%d : %r" % ((nom,) + sys.version_info[:3]
                                                                               + (vu[-160:],)))
                continue
            code, sortie = lancer(copie, JUGE, copie, ident, OPTION)
            if code != 2 or "essai refusé" not in sortie or not toutes_marquees(sortie):
                faux.append("%s, juge : code %d, %r" % (nom, code, sortie[-200:]))
        finally:
            with open(fichier, "wb") as sortie_f:
                sortie_f.write(origine)
    return faux


def cas_d_une_version_differente(copie, dossier):
    """Joue E11 : la moulinette sous l'option, UNE version marquée identique à la fiche mais de tp 0,06 au lieu de
    0,04 ; rend la liste des cas faux. ① RÔLE — Le mineur M5 du relecteur neuf du 16-11-2026. ② CONTEXTE D'APPEL —
    `cas_rapides`. ③ ENTRÉE — la copie ; un dossier de travail. ④ CONDITIONS D'ENTRÉE — PREPARER a écrit la
    combinatoire. ⑤ SORTIE — UNE valeur : la liste. [rend: 1] ⑥ TRAITEMENT — la combinatoire recopiée, tp à 0.06 ;
    attendu : code 2, « essai refusé », toutes lignes marquées, AUCUN calibrage (rien joué), aucun fichier écrit.
    ⑦ UNITÉ — — ⑧ POURQUOI — Sous l'option, une version qui n'a pas les réglages de la fiche d'essai jouerait des
    réglages non autorisés dans la fenêtre du regard unique, avec le jeton ; refus en 2 comme les autres refus
    d'essai. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit dans le dossier de travail. ⑪ TERMINAISON — Rend la main ; DELAI
    au plus. [sort: non]"""
    lignes = list(csv.DictReader(open(os.path.join(copie, COMBINATOIRE), encoding="utf-8-sig")))
    if len(lignes) != 1 or lignes[0]["tp"] != "0.04":
        return ["E11 combinatoire d'essai inattendue : %r" % lignes]
    d = os.path.join(dossier, "E11")
    os.makedirs(d, exist_ok=True)
    f = os.path.join(d, os.path.basename(COMBINATOIRE))
    with open(f, "w", encoding="utf-8", newline="") as s:
        w = csv.DictWriter(s, fieldnames=list(lignes[0]))
        w.writeheader()
        w.writerow(dict(lignes[0], tp="0.06"))
    r = os.path.join(d, "R11.csv")
    if os.path.exists(r):
        os.remove(r)
    code, sortie = lancer(copie, MOULINETTE, copie, f, r, "--cours=" + VINGT_ANS, OPTION)
    if (code != 2 or "essai refusé" not in sortie or not toutes_marquees(sortie) or "CALIBRAGE" in sortie
            or os.path.exists(r)):
        return ["E11 moulinette, version différente de la fiche : code %d, calibrage %s, %r"
                % (code, "CALIBRAGE" in sortie, sortie[-240:])]
    return []


def cas_rapides(copie, dossier):
    """Joue les cas rapides ; rend la liste des cas faux. ① RÔLE — Le cœur du jeu d'épreuves, rejoué sous sabotage.
    ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — la copie préparée ; un dossier de travail hors de la copie.
    ④ CONDITIONS D'ENTRÉE — `ajouter_les_fiches` a tourné. ⑤ SORTIE — UNE valeur : la liste « Ex … : raison ».
    [rend: 1] ⑥ TRAITEMENT — les cas unitaires (UNITE) ; E1 juge en ligne de commande, refus 2 marqué ; E2 dans un
    vrai dépôt (`git init`), ESSAI-IND-001 et ESSAI-C5-2000-2026 avec l'option, refus 2 ; E5 ESSAI-C5-TP, refus 2 ;
    E6 moulinette à deux versions, refus 2 marqué ; E9 .git en fichier puis en lien, refus 2 ; E7 tri, refus ;
    A1 à A4b (dans UNITE) ; E-ancre sur la copie ; A5, A6, A6-bis (`cas_de_la_reference`) ; E11 (M5).
    ⑦ UNITÉ — — ⑧ POURQUOI — fiche en tête. ⑨ CE QUI CLOCHE — Le dépôt d'E2 est retiré à la fin du cas, même en
    erreur. ⑩ EFFET — Crée et retire .git dans la copie ; écrit dans le dossier de travail. ⑪ TERMINAISON — Rend la
    main. [sort: non]"""
    faux = []
    code, sortie = lancer(copie, "-c", UNITE, copie, VINGT_ANS, dossier)
    try:
        faux += ["%s : %s" % kv for kv in json.loads(sortie.strip().splitlines()[-1]).items()]
    except (ValueError, IndexError):
        faux.append("UNITE n'a pas tourné : code %d, %r" % (code, sortie[-300:]))
    code, sortie = lancer(copie, JUGE, copie, "ESSAI-IND-001", OPTION)
    if code != 2 or "essai refusé" not in sortie or not toutes_marquees(sortie):
        faux.append("E1 juge, vraie fiche renommée : code %d, marquée %s, %r" % (code, toutes_marquees(sortie),
                                                                              sortie[-200:]))
    code, sortie = lancer(copie, JUGE, copie, "ESSAI-C5-TP", OPTION)
    if code != 2 or "empreinte des réglages" not in sortie:
        faux.append("E5 juge, tp d'un cran : code %d, %r" % (code, sortie[-200:]))
    faux += cas_e_ancre(copie)
    faux += cas_de_la_reference(copie)
    faux += cas_d_une_version_differente(copie, dossier)
    subprocess.run(["git", "init", "-q", copie], check=True)
    try:
        for ident in ("ESSAI-IND-001", "ESSAI-C5-2000-2026"):
            code, sortie = lancer(copie, JUGE, copie, ident, OPTION)
            if code != 2 or "porte .git" not in sortie:
                faux.append("E2 juge dans un dépôt, %s : code %d, %r" % (ident, code, sortie[-200:]))
        code, sortie = lancer(copie, "-c", "import sys; sys.path.insert(0, sys.argv[1] + '/programmes'); "
                              "import JUGE_DES_STRATEGIES as J, CONTRATS_DES_FICHIERS as C; "
                              "f = C.fiches_du_registre(J.trouver(sys.argv[1], C.NOM_DU_REGISTRE_DES_STRATEGIES)); "
                              "print(J.jeton_d_essai(sys.argv[1], f['ESSAI-C5-2000-2026'], 1)[0] is None)", copie)
        if sortie.strip().splitlines()[-1:] != ["True"]:
            faux.append("E2 jeton dans un dépôt : %r" % sortie[-200:])
    finally:
        shutil.rmtree(os.path.join(copie, ".git"), ignore_errors=True)
    for forme in ("fichier", "lien"):
        g = os.path.join(copie, ".git")
        if forme == "fichier":
            open(g, "w").write("gitdir: /nulle/part\n")
        else:
            os.symlink("/tmp", g)
        try:
            code, sortie = lancer(copie, JUGE, copie, "ESSAI-C5-2000-2026", OPTION)
            if code != 2 or "porte .git" not in sortie:
                faux.append("E9 juge, .git %s : code %d, %r" % (forme, code, sortie[-200:]))
        finally:
            os.remove(g)
    f2 = combinatoire_a_deux(copie, dossier)
    r2 = os.path.join(dossier, "R2.csv")
    if os.path.exists(r2):
        os.remove(r2)   # écrit par un tour saboté précédent (S3) : chaque tour part d'un dossier propre
    code, sortie = lancer(copie, MOULINETTE, copie, f2, r2, "--cours=" + VINGT_ANS, OPTION)
    if code != 2 or "versions" not in sortie or not toutes_marquees(sortie) or os.path.exists(r2):
        faux.append("E6 moulinette, deux versions : code %d, %r" % (code, sortie[-200:]))
    code, sortie = lancer(copie, TRI, copie, os.path.join(dossier, "TRIE.csv"),
                          os.path.join(dossier, "RESULTATS_colonne.csv"))
    if code == 0 or "fichier d'ESSAI" not in sortie:
        faux.append("E7 tri en ligne de commande : code %d, %r" % (code, sortie[-200:]))
    return faux


def etat(copie):
    """Rend l'état de la copie : k du registre et empreinte de tous ses fichiers. ① RÔLE — « registre des essais et k
    inchangés ». ② CONTEXTE D'APPEL — `cas_longs`, avant et après. ③ ENTRÉE — la copie. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un texte « k=… arbre=… ». [rend: 1] ⑥ TRAITEMENT — `versions_du_registre` du juge ; sha256
    de chaque fichier, chemins compris, hors .git et __pycache__. ⑦ UNITÉ — — ⑧ POURQUOI — Un essai n'écrit rien :
    ni registre, ni registre des essais (qui vit sur une branche distante, inaccessible sans .git), ni compte.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lit la copie. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    code, sortie = lancer(copie, "-c", "import csv, io, sys; sys.path.insert(0, sys.argv[1] + '/programmes'); "
                          "import JUGE_DES_STRATEGIES as J, CONTRATS_DES_FICHIERS as C; "
                          "f = J.trouver(sys.argv[1], C.NOM_DU_REGISTRE_DES_STRATEGIES); "
                          "l = list(csv.DictReader(io.StringIO(''.join(x for x in open(f, encoding='utf-8-sig') "
                          "if not x.startswith('#'))))); "
                          "print(J.versions_du_registre(l, J.lire_module_du_jour(sys.argv[1]))[1])", copie)
    h = hashlib.sha256()
    for d, ds, fs in os.walk(copie):
        ds[:] = sorted(x for x in ds if x not in (".git", "__pycache__"))
        for n in sorted(fs):
            p = os.path.join(d, n)
            h.update(os.path.relpath(p, copie).encode("utf-8"))
            h.update(open(p, "rb").read())
    return "k=%s arbre=%s" % (sortie.strip().splitlines()[-1] if sortie.strip() else "?", h.hexdigest()[:16])


def juge_d_essai_complet(copie):
    """Joue le juge sous l'option sur les 20 ans (E4b) et regarde son voisinage (E10) ; rend la liste des cas faux.
    ① RÔLE — L'essai joué de bout en bout par le juge seul. ② CONTEXTE D'APPEL — `cas_longs` ; `main` sous le
    sabotage long S13. ③ ENTRÉE — la copie préparée. ④ CONDITIONS D'ENTRÉE — PREPARER a tourné. ⑤ SORTIE — UNE
    valeur : la liste. [rend: 1] ⑥ TRAITEMENT — E4b : code 0, toutes lignes marquées, calibré, des opérations,
    hasard joué, aucun échec · E10 : la ligne « VOISINAGE … NON JOUÉ » présente, et aucun voisin joué (« voisin(s) a
    +- » absent). ⑦ UNITÉ — Des secondes. ⑧ POURQUOI — E10 : décision de Jean-Luc du 16-11-2026 à 23h15 (A-866,
    « 2 ») : sous l'option, le juge ne joue pas les 26 voisins ; seule la fiche d'essai regarde 2000-2023.
    ⑨ CE QUI CLOCHE — Environ une minute sur deux cœurs. ⑩ EFFET — Lance un processus. ⑪ TERMINAISON — Rend la
    main ; DELAI au plus. [sort: non]"""
    faux = []
    code, sortie = lancer(copie, JUGE, copie, "ESSAI-C5-2000-2026", "--cours=" + VINGT_ANS, OPTION)
    attendus = ("OK, l'instrument est calibre", "operations . ", "HASARD  l'ACTION", "HASARD  les DATES")
    manquent = [a for a in attendus if a not in sortie]
    if code != 0 or manquent or not toutes_marquees(sortie) or "EN ÉCHEC" in sortie or "REFUSEE (garde M" in sortie:
        faux.append("E4b juge avec l'option : code %d, manquent %s, marquée %s, %r" % (
            code, manquent, toutes_marquees(sortie), sortie[-300:]))
    if "VOISINAGE            NON JOUÉ" not in sortie or "voisin(s) a +-" in sortie:
        faux.append("E10 voisinage sous jeton : %r" % next((l for l in sortie.splitlines() if "VOISINAGE" in l),
                                                           "(aucune ligne VOISINAGE)"))
    print("  E4b juge : %s" % next((l for l in sortie.splitlines() if "operations . " in l), "(aucune ligne)"))
    print("  E10 juge : %s" % next((l for l in sortie.splitlines() if "VOISINAGE" in l), "(aucune ligne VOISINAGE)"))
    return faux


def cas_longs(copie, dossier):
    """Joue les cas longs, sur les 20 ans ; rend la liste des cas faux. ① RÔLE — Les refus « comme aujourd'hui » et
    l'essai joué de bout en bout. ② CONTEXTE D'APPEL — `main`, Z0 seulement. ③ ENTRÉE — la copie ; un dossier de
    travail. ④ CONDITIONS D'ENTRÉE — `ajouter_les_fiches` a tourné. ⑤ SORTIE — UNE valeur : la liste. [rend: 1]
    ⑥ TRAITEMENT — E2b ESSAI-IND-001 sans l'option dans un dépôt → code 1, refus du regard ; E3 ESSAI-C5-2000-2026 sans
    l'option → code 1, « REFUSEE (garde M, regard unique) » ; E4b et E10 avec l'option (`juge_d_essai_complet`) :
    juge → 0, toutes lignes marquées, calibré, des opérations, hasard joué, voisinage NON joué (A-866), aucun échec ; moulinette → 0, colonne d'essai écrite ; état
    de la copie identique avant et après ; le tri refuse le vrai fichier. ⑦ UNITÉ — Des secondes. ⑧ POURQUOI — fiche
    en tête. ⑨ CE QUI CLOCHE — Environ cinq minutes sur deux cœurs. ⑩ EFFET — Crée et retire .git ; écrit dans le
    dossier de travail. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    faux = []
    subprocess.run(["git", "init", "-q", copie], check=True)
    try:
        code, sortie = lancer(copie, JUGE, copie, "ESSAI-IND-001", "--cours=" + VINGT_ANS)
        if code != 1 or not ("REFUSEE (garde M, regard unique)" in sortie or "RegardNonInscrit" in sortie):
            faux.append("E2b sans option dans un dépôt : code %d, %r" % (code, sortie[-300:]))
    finally:
        shutil.rmtree(os.path.join(copie, ".git"), ignore_errors=True)
    code, sortie = lancer(copie, JUGE, copie, "ESSAI-C5-2000-2026", "--cours=" + VINGT_ANS)
    if code != 1 or "REFUSEE (garde M, regard unique)" not in sortie:
        faux.append("E3 sans option : code %d, %r" % (code, sortie[-300:]))
    avant = etat(copie)
    faux += juge_d_essai_complet(copie)
    r = os.path.join(dossier, "RESULTATS_E4.csv")
    code, sortie = lancer(copie, MOULINETTE, copie, os.path.join(copie, COMBINATOIRE), r, "--cours=" + VINGT_ANS,
                          OPTION)
    entete = open(r, encoding="utf-8").readline() if os.path.exists(r) else ""
    if code != 0 or not toutes_marquees(sortie) or "statut_d_essai" not in entete:
        faux.append("E4b moulinette avec l'option : code %d, en-tête %r, %r" % (code, entete[-80:], sortie[-300:]))
    print("  E4b moulinette : %s" % next((l for l in sortie.splitlines() if "ce programme :" in l), "(aucune ligne)"))
    apres = etat(copie)
    print("  E4b état de la copie avant %s · après %s" % (avant, apres))
    if avant != apres:
        faux.append("E4b état de la copie changé : %s -> %s" % (avant, apres))
    if os.path.exists(r):
        code, sortie = lancer(copie, TRI, copie, os.path.join(dossier, "TRIE_E4.csv"), r)
        if code == 0 or "fichier d'ESSAI" not in sortie:
            faux.append("E7b tri du vrai fichier d'essai : code %d, %r" % (code, sortie[-200:]))
    return faux


def main():
    """Prépare la copie, joue Z0, puis chaque sabotage. ① RÔLE — Point d'entrée. ② CONTEXTE D'APPEL — Le lancement.
    ③ ENTRÉE — fiche en tête, ③. ④ CONDITIONS D'ENTRÉE — fiche en tête, ④. ⑤ SORTIE — UNE valeur : 0, 1 ou 2.
    [rend: 1] ⑥ TRAITEMENT — fiche en tête, ⑥. ⑦ UNITÉ — — ⑧ POURQUOI — fiche en tête. ⑨ CE QUI CLOCHE — Un
    sabotage dont le texte n'est pas trouvé rend 2 (il ne mordrait sur rien). ⑩ EFFET — Crée puis efface la copie.
    ⑪ TERMINAISON — Rend la main. [sort: non]"""
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    seulement = [a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--seulement=")]
    if (len(args) != 1 or any(a not in ("--saboter", "--rapide") and not a.startswith("--seulement=")
                              for a in sys.argv[1:] if a.startswith("--"))
            or any(s not in SABOTAGES for x in seulement for s in x.split(","))):
        print(__doc__.split("①")[0])
        return 2
    seulement = {s for x in seulement for s in x.split(",")}
    racine = os.path.abspath(args[0])
    avant_racine = empreinte(os.path.join(racine, REGISTRE))
    # E-ANCRE SUR LA RACINE REÇUE (dans le circuit : la version éprouvée, main le soir), avant toute copie
    faux_ancre = cas_e_ancre(racine)
    copie = copie_jetable(racine)
    dossier = os.path.join(os.path.dirname(copie), "travail")
    os.makedirs(dossier)
    try:
        code, sortie = lancer(copie, PREPARER, copie)
        if code != 0:
            print("ARRÊT : PREPARER rend %d : %s" % (code, sortie[-300:]))
            return 2
        ajouter_les_fiches(copie)
        faux = faux_ancre + cas_rapides(copie, dossier)
        if "--rapide" not in sys.argv:
            faux += cas_longs(copie, dossier)
        if faux:
            print("Z0 NON CONFORME :")
            for f in faux:
                print("  " + f)
            return 1
        print("Z0 programmes tels quels : E-ancre, E1 à E11, A1 à A6-bis%s conformes"
              % (" (rapides)" if "--rapide" in sys.argv else ""))
        if "--saboter" in sys.argv:
            ne_mord_pas = []
            for nom, (prog, remplacements, cibles, *long_) in SABOTAGES.items():
                if seulement and nom not in seulement:
                    continue
                long_ = bool(long_ and long_[0])
                if long_ and "--rapide" in sys.argv:
                    print("%s NON JOUÉ : sabotage long, exclu par --rapide" % nom)
                    continue
                cibles = (cibles,) if isinstance(cibles, str) else cibles
                chemin = os.path.join(copie, prog)
                with open(chemin, encoding="utf-8", newline="") as s:
                    origine = s.read()
                texte = origine
                if callable(remplacements):
                    texte = remplacements(texte)
                else:
                    for ancien, nouveau in remplacements:
                        if texte.count(ancien) != 1:
                            print("ARRÊT : sabotage %s : texte trouvé %d fois : %r" % (nom, texte.count(ancien),
                                                                                      ancien[:60]))
                            return 2
                        texte = texte.replace(ancien, nouveau)
                if texte == origine:
                    print("ARRÊT : sabotage %s : rien n'a changé" % nom)
                    return 2
                with open(chemin, "w", encoding="utf-8", newline="") as s:
                    s.write(texte)
                try:
                    f_s = juge_d_essai_complet(copie) if long_ else cas_rapides(copie, dossier)
                finally:
                    with open(chemin, "w", encoding="utf-8", newline="") as s:
                        s.write(origine)
                mord = {c: [f.split(" :")[0] for f in f_s if f.startswith(c)] for c in cibles}
                tous = all(mord.values())
                print("%s %s : %s" % (nom, "mord" if tous else "NE MORD PAS",
                                      sorted({x for v in mord.values() for x in v}) if tous else (mord, f_s)))
                if not tous:
                    ne_mord_pas.append(nom)
            if ne_mord_pas:
                print("VERDICT : NON CONFORME — sabotages sans effet : %s" % ne_mord_pas)
                return 1
        if empreinte(os.path.join(racine, REGISTRE)) != avant_racine:
            print("VERDICT : NON CONFORME — le registre de la racine a changé")
            return 1
        print("VERDICT : tout est conforme")
        return 0
    finally:
        shutil.rmtree(os.path.dirname(copie), ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
