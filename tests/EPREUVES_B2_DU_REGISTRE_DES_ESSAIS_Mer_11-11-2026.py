"""ÉPREUVES DE B2 (plan V7) — le registre des essais : la lignée, la portée du regard, le bilan d'une fiche et k.
Simulation uniquement. Mercredi 11-11-2026.

LE SENS EN TÊTE — Le lot B a été coupé par le superviseur R-759 du 11-11-2026 (22h19) ; B2 tient le registre des
essais et la LIGNÉE. Ces épreuves vérifient, sur des cas dont on connaît la réponse : que la lignée d'une fiche relie
sa mère, ses versions et leurs sœurs, par les déclarations datées et par la case `mere` du registre ; qu'un lien
illisible ou introuvable rend INCONNU, jamais « aucune » ; que la PORTÉE du regard se LIT dans
`donnees/REGLAGES_DU_REGISTRE_DES_ESSAIS.csv` (changer le fichier change le résultat, sans toucher au code) ; que le
premier regard d'une lignée se trouve dans l'ordre de l'histoire ; que le bilan rendu à la porte du juge porte la
lignée, les regards, trois comptes d'essais et k, sans confondre « aucun regard inscrit » et « jamais regardé ».
`--saboter` casse le code (le registre des essais ET le contrat) de chaque façon de la table SABOTAGES : chacune doit faire rougir au moins un cas (R-731).

USAGE : python3 -B tests/EPREUVES_B2_DU_REGISTRE_DES_ESSAIS_Mer_11-11-2026.py <racine> [--saboter | nom de sabotage]
CODE : 0 si Z0 est vert et que chaque sabotage joué fait rougir au moins un cas ; 1 sinon ; 2 si une cible de
sabotage est introuvable, si le nom est inconnu ou si une donnée manque (R-734).

① RÔLE — Prouver que B2 fait ce que dit sa note, et que chaque garde a des dents.
② CONTEXTE D'APPEL — À la main ; par la certification, qui lance chaque fichier de tests/ avec la racine. Ce programme
  se relance en « --cas <copie> <racine> ».
③ ENTRÉE — La racine du dépôt ; « --saboter » ou un nom de sabotage, facultatif.
④ CONDITIONS D'ENTRÉE — Sous la racine : `programmes/TENIR_LE_REGISTRE_DES_ESSAIS.py`, `CONTRATS_DES_FICHIERS.py`,
  `COMMUN.py`, `JUGE_DES_STRATEGIES.py` ; `donnees/REGLAGES_DU_REGISTRE_DES_ESSAIS.csv`,
  `donnees/DECLARATIONS_DATEES.csv`, `donnees/cac40_strategies.csv` ; git.
⑤ SORTIE — Le code de sortie dit en « CODE » ; une ligne par cas et par sabotage.
  [rend: 1]
⑥ TRAITEMENT — ① pour Z0 puis chaque sabotage : copier les quatre programmes dans un dossier temporaire, appliquer le
  sabotage (un texte présent UNE fois) · ② relancer ce programme en « --cas » sur la copie · ③ Z0 doit être vert ; un
  sabotage doit faire rougir au moins un cas.
⑦ UNITÉ — Des fiches, des entrées, des essais ; k en versions du registre des stratégies plus les témoins.
⑧ POURQUOI — R-731, R-732 (cas tirés de vraies lignes : P5, K1 sur le vrai registre des stratégies, V0 sur la vraie
  racine), R-734.
⑨ CE QUI CLOCHE — ① Les déclarations sont synthétiques (le vrai fichier n'a que son en-tête au 11-11-2026). ② k est
  éprouvé sur un dépôt jetable à UN commit : l'ancrage par date de `k_a_la_date` (agent A) n'est pas éprouvé ici.
  ③ Les sabotages portent sur `TENIR_LE_REGISTRE_DES_ESSAIS.py` et `CONTRATS_DES_FICHIERS.py`.
⑩ EFFET — Écrit et efface des dossiers temporaires (dont des dépôts git jetables) ; n'écrit rien sous la racine.
  Le cas V0 EXIGE LE RÉSEAU : il lit la branche des regards de l'origine de la vraie racine (git ls-remote) ;
  réseau coupé ou origine locale, il rougit (« Failed to connect ») — relevé N-1 de Cowork, 12-11-2026 ; vert avec
  le réseau (superviseur R-759 du 12-11-2026, 13h46).
⑪ TERMINAISON — Chaque relance « --cas » est bornée à 300 secondes ; un dépassement compte comme rouge.
  [sort: oui — code de sortie]
"""
import csv, importlib.util, json, os, shutil, subprocess, sys, tempfile

ICI = os.path.abspath(__file__)
ESSAIS = "programmes/TENIR_LE_REGISTRE_DES_ESSAIS.py"
VOISINS = ("programmes/CONTRATS_DES_FICHIERS.py", "programmes/COMMUN.py", "programmes/JUGE_DES_STRATEGIES.py")
CONTRAT = VOISINS[0]

# LES SABOTAGES : (fichier, texte présent UNE fois, remplacement). Chacun retire ce qu'un cas teste.
SABOTAGES = {
    "B2S01_portee_ignoree": [(ESSAIS, '    if ligne["valeur"] == "fiche":', '    if True:')],
    "B2S02_sens_fille_vers_mere_ignore": [(ESSAIS, "        voisins.setdefault(fi, set()).add(m)\n", "")],
    "B2S03_liens_du_registre_ignores": [(ESSAIS, '                    liens.add((m, e["fiche_id"], "registre des essais"))',
                                         '                    pass')],
    "B2S04_mere_introuvable_admise": [(ESSAIS, '            if e["mere"] not in par_empreinte:\n                return None, [], "entrée %s : mère %s '
                                       'introuvable au registre des essais" % (nom, e["mere"])',
                                       '            if e["mere"] not in par_empreinte:\n                continue')],
    "B2S26_identite_a_l_octet_pres": [(CONTRAT, "    return str(identifiant).strip().casefold()", "    return str(identifiant)")],
    "B2S27_nom_inconnu_admis": [(CONTRAT, '    if not trouvees:\n        return None, "fiche « %s » inconnue',
                                 '    if not trouvees:\n        return fiche_id.strip(), ""\n        return None, "fiche « %s » inconnue')],
    "B2S28_nom_ambigu_admis": [(CONTRAT, "    if len(trouvees) > 1:", "    if False:")],
    # B2S29 SUIT LE JUGE (12-11-2026) : REGARD tour 3 (13f55ff6) a donné à `premier_regard` le même début que
    # `regards_sur_les_annees` ; l'ancienne cible y était présente 2 fois (« --saboter » rendait 2). Même propriété
    # (`regards_sur_les_annees` refuse une fiche inconnue), cible rendue unique par la fin propre à la fonction.
    "B2S29_regards_sans_identite": [(ESSAIS, "    if connue is None:\n        return None, raison\n    examen = _bornes(annees_d_examen)\n"
                                     "    if examen is None:\n        return None, \"années d'examen illisibles : %r\" % (annees_d_examen,)\n"
                                     "    entrees, defauts = lire_le_registre(racine)\n    if defauts:\n        return None, \"registre des essais abîmé : \" + defauts[0]\n"
                                     "    perimetre, raison = _perimetre_du_regard(racine, connue, entrees)\n    if perimetre is None:\n        return None, raison\n"
                                     "    return _regards_dans(racine, entrees, examen, perimetre, sauf)",
                                     "    if False:\n        return None, raison\n    examen = _bornes(annees_d_examen)\n"
                                     "    if examen is None:\n        return None, \"années d'examen illisibles : %r\" % (annees_d_examen,)\n"
                                     "    entrees, defauts = lire_le_registre(racine)\n    if defauts:\n        return None, \"registre des essais abîmé : \" + defauts[0]\n"
                                     "    perimetre, raison = _perimetre_du_regard(racine, connue, entrees)\n    if perimetre is None:\n        return None, raison\n"
                                     "    return _regards_dans(racine, entrees, examen, perimetre, sauf)")],
    "B2S25_derniere_declaration_seule": [(ESSAIS, "    for decl in declarations:\n", "    for decl in declarations[-1:]:\n")],
    "B2S30_forme_canonique_non_posee_a_la_lecture": [(ESSAIS, "            e = dict(e, fiche_id=canon)\n", "")],
    "B2S31_nom_inconnu_admis_a_la_lecture": [(ESSAIS, '            if canon is None:\n                defauts.append("%s : %s" % (nom_f, raison))\n'
                                                      '                continue\n', "")],
    "B2S32_genre_non_verifie_a_la_lecture": [(ESSAIS, '            if e["genre_d_essai"] not in C.GENRES_D_ESSAI:\n                defauts',
                                              '            if False:\n                defauts')],
    "B2S33_reglage_du_calibrage_ignore": [(ESSAIS, 'if e["genre_d_essai"] == "CALIBRAGE" and calib["valeur"] == "non":', "if False:")],
    "B2S34_calibrage_jamais_regard": [(ESSAIS, 'if e["genre_d_essai"] == "CALIBRAGE" and calib["valeur"] == "non":',
                                       'if e["genre_d_essai"] == "CALIBRAGE":')],
    "B2S35_contrat_compare_a_l_octet": [(CONTRAT, '        if ligne["fiche_id"] != canon:', '        if ligne["fiche_id"] != fiche_id:')],
    "B2S36_declarations_non_canoniques": [(CONTRAT, '        ligne["fiche_id"] = canon\n', "")],
    "B2S37_declaration_au_nom_inconnu_admise": [(CONTRAT, '        if canon is None:\n            raise ValueError(f"{DECLARATIONS_DATEES}, ligne {numero}',
                                                 '        if False:\n            raise ValueError(f"{DECLARATIONS_DATEES}, ligne {numero}')],
    "B2S38_bilan_inconnu_compte_zero": [(ESSAIS, 'essais_de_la_fiche="INCONNU", essais_de_la_lignee="INCONNU",',
                                         'essais_de_la_fiche=0, essais_de_la_lignee=0,')],
    "B2S39_essais_d_une_fiche_inconnue_zero": [(ESSAIS, '        if fiche_id is None:\n            return "INCONNU", raison',
                                                '        if fiche_id is None:\n            return 0, ""')],
    "B2S40_lignee_d_une_fiche_inconnue": [(ESSAIS, "    canon, raison = C.identite_de_la_fiche(racine, fiche_id, fiches)\n    if canon is None:\n"
                                           "        return None, [], raison", "    canon, raison = fiche_id.strip(), \"\"\n    if canon is None:\n"
                                           "        return None, [], raison")],
    "B2S41_lignee_nommant_un_inconnu_admise": [(ESSAIS, "            if cm is None or cf is None:\n                return None, [],",
                                                "            if cm is None or cf is None:\n                continue\n                return None, [],")],
    "B2S42_parts_de_la_derniere_declaration_seule": [(ESSAIS, "                    if d.get(\"part_regardee\", \"\") not in parts:\n"
                                                      "                        parts.append(d.get(\"part_regardee\", \"\"))",
                                                      "                    parts[:] = [d.get(\"part_regardee\", \"\")]")],
    "B2S24_declarations_non_lues": [(ESSAIS, "        declarations = C.declarations_du_fichier(racine)\n", "        declarations = []\n")],
    "B2S05_lignee_illisible_prise_pour_aucune": [(ESSAIS, '        if lus is None:\n            return None, [], "déclaration de',
                                                  '        if lus is None:\n            lus = []\n        if False:\n'
                                                  '            return None, [], "déclaration de')],
    "B2S06_aucune_illisible": [(ESSAIS, '    if texte.strip().lower() == "aucune":\n        return []',
                                '    if texte.strip().lower() == "aucune":\n        return None')],
    "B2S08_propre_fille_admise": [(ESSAIS, "            if f == mere:\n                return None",
                                   "            if False:\n                return None")],
    "B2S09_espace_admis": [(ESSAIS, "any(c.isspace() for c in i)", "False")],
    "B2S10_valeur_hors_domaine_admise": [(ESSAIS, '    elif ligne["valeur"] not in domaine:', '    elif False:')],
    "B2S11_cle_double_admise": [(ESSAIS, "    if len(trouvees) != 1:", "    if not trouvees:")],
    "B2S12_en_tete_non_verifie": [(ESSAIS, "        if lecteur.fieldnames != EN_TETE_DES_REGLAGES:", "        if False:")],
    "B2S13_reglage_absent_pris_pour_lignee": [(ESSAIS, '    if not os.path.isfile(chemin):\n        return None, "réglages',
                                               '    if not os.path.isfile(chemin):\n        return {"cle": "portee_du_regard", '
                                               '"valeur": "lignee", "statut": "", "source": ""}, ""\n        return None, "réglages')],
    "B2S14_inconnu_dit_aucun_regard": [(ESSAIS, '        b["annees_deja_regardees"] = "INCONNU"',
                                        '        b["annees_deja_regardees"] = "AUCUN REGARD INSCRIT"')],
    "B2S15_temoins_non_transmis_a_k": [(ESSAIS, "JU.k_a_la_date(racine, date_declaration, temoins)",
                                        'JU.k_a_la_date(racine, date_declaration, "aucun")')],
    "B2S16_essais_de_la_lignee_non_filtres": [(ESSAIS, '\n           and (famille_de is None or e["fiche_id"] in famille_de)}', "}")],
    "B2S17_sauf_ignore": [(ESSAIS, '        if e["nature"] != "PREENREGISTREMENT" or nom in sauf:',
                           '        if e["nature"] != "PREENREGISTREMENT":')],
    "B2S18_premier_regard_par_fiche": [(ESSAIS, "    vus, raison = _regards_dans(racine, entrees, examen, perimetre, ())",
                                        "    vus, raison = _regards_dans(racine, entrees, examen, {connue}, ())")],
    "B2S19_composante_non_parcourue": [(ESSAIS, "            if v not in famille:", "            if False:")],
    "B2S20_parts_declarees_non_recopiees": [(ESSAIS, '                if d["fiche_id"] in b["lignee"]:', "                if False:")],
    "B2S21_toutes_lu_comme_lignee": [(ESSAIS, '    if ligne["valeur"] == "toutes":\n        return "toutes", ""',
                                      '    if False:\n        return "toutes", ""')],
    "B2S22_chevauchement_strict": [(ESSAIS, "if p[0] <= examen[1] and examen[0] <= p[1]:", "if p[0] < examen[1] and examen[0] < p[1]:")],
    "B2S23_lignee_hors_compte_des_essais": [(ESSAIS, '        lignee, _l, raison = lignee_de_la_fiche(racine, lignee_de, entrees)\n'
                                             '        if lignee is None:\n            return "INCONNU"',
                                             '        lignee, _l, raison = lignee_de_la_fiche(racine, lignee_de, entrees)\n'
                                             '        if lignee is None:\n            lignee = [lignee_de]\n        if False:\n'
                                             '            return "INCONNU"')],
}

HYP = {"tp_pct": 4.0, "sl_pct": 2.5, "horizon": 20, "univers": ["AC"], "signal": ["f", "0123"],
       "periode": "2030-01-01..2030-12-31", "bareme": "Fortuneo"}
EXAMEN = "2000-01-03..2023-12-29"


def charger(chemin, nom):
    """Charge un programme par son chemin.
    ① RÔLE — Prendre le module éprouvé dans la copie. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — chemin, nom.
    ④ CONDITIONS D'ENTRÉE — le fichier existe. ⑤ SORTIE — UNE valeur : le module. [rend: 1]
    ⑥ TRAITEMENT — spec_from_file_location, exécution, rangé dans sys.modules sous son nom. ⑦ UNITÉ — —.
    ⑧ POURQUOI — les modules s'importent entre eux par leur nom : ils doivent trouver la copie.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — charge du code. ⑪ TERMINAISON — Rend la main ; lève. [sort: non]"""
    spec = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nom] = m
    spec.loader.exec_module(m)
    return m


IDS_DE_L_EPREUVE = ("MERE", "FILLE1", "FILLE2", "SANS", "V9", "C5", "BALAYAGE", "B-V3", "ORPHELINE", "AUTRE", "F2030",
                    "G2030", "X", "Y")


def poser_racine(d, C, portee="lignee", declarations=(), en_tete=None, reglages=None, ids=IDS_DE_L_EPREUVE,
                 calibrage="oui"):
    """Écrit sous `d` les deux fichiers que lit le regard : les réglages et les déclarations datées.
    ① RÔLE — Fabriquer une racine synthétique. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — le dossier, le module des
    contrats, la portée, des déclarations {fiche_id, lignee, part_regardee, date}, un en-tête de réglages ou des
    lignes de réglages à écrire telles quelles, les identifiants du registre des stratégies minimal, la réponse au
    réglage du calibrage. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — aucune valeur. [rend: 0]
    ⑥ TRAITEMENT — écrire `donnees/cac40_strategies.csv` (en-tête « id », une ligne par identifiant),
    `donnees/REGLAGES_DU_REGISTRE_DES_ESSAIS.csv` (sauf portée None) et
    `donnees/DECLARATIONS_DATEES.csv` à l'en-tête du contrat, chaque case non donnée valant « x ». ⑦ UNITÉ — —.
    ⑧ POURQUOI — les regards lisent ces deux fichiers ; depuis la mission REGARD, le registre des essais vit sur la
    branche des regards d'un dépôt distant (`depot_jetable`). ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit deux fichiers, et
    un dépôt git avec son dépôt distant nu.
    ⑪ TERMINAISON — Rend la main. [sort: non]"""
    os.makedirs(os.path.join(d, "donnees"), exist_ok=True)
    with open(os.path.join(d, "donnees/cac40_strategies.csv"), "w", encoding="utf-8") as f:
        f.write("id\n" + "".join(i + "\n" for i in ids))
    reg = os.path.join(d, "donnees/REGLAGES_DU_REGISTRE_DES_ESSAIS.csv")
    if portee is None:
        if os.path.exists(reg):
            os.remove(reg)
    else:
        with open(reg, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(en_tete or ["cle", "valeur", "statut", "source"])
            for l in (reglages or [["portee_du_regard", portee, "épreuve", "épreuve"],
                                   ["calibrage_compte_comme_regard", calibrage, "épreuve", "épreuve"],
                                   ["poussees_des_regards", "3", "épreuve", "épreuve (mission REGARD)"],
                                   ["depot_des_regards", os.path.join(d, ".depot_nu"), "épreuve", "épreuve (REGARD)"]]):
                w.writerow(l)
    with open(os.path.join(d, "donnees/DECLARATIONS_DATEES.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=C.DECLARATION_DATEE)
        w.writeheader()
        for x in declarations:
            ligne = {c: "x" for c in C.DECLARATION_DATEE}
            ligne.update(fiche_id=x["fiche_id"], lignee=x["lignee"], part_regardee=x.get("part_regardee", "aucune"),
                         date_declaration=x.get("date", "2026-11-01T10:00+01:00"))
            w.writerow(ligne)
    depot_jetable(d)


def depot_jetable(d):
    """Fait de `d` un dépôt git qui a SON dépôt distant nu, où vit la branche des regards.
    ① RÔLE — Depuis la mission REGARD (12-11-2026), le registre des essais vit sur la branche des regards du dépôt
    distant de la branche principale (`CONTRATS_DES_FICHIERS.BRANCHE_DES_REGARDS`), jamais sur le disque : chaque
    racine synthétique doit avoir le sien, pour que deux racines ne partagent pas leurs regards. ② CONTEXTE D'APPEL —
    `poser_racine`, à chaque racine. ③ ENTRÉE — le dossier. ④ CONDITIONS D'ENTRÉE — git. ⑤ SORTIE — aucune valeur.
    [rend: 0] ⑥ TRAITEMENT — `git init` si `d/.git` manque ; un dépôt nu `d/.depot_nu` (exclu par `.git/info/exclude`)
    déclaré « origin » s'il n'y a pas de dépôt distant. ⑦ UNITÉ — —. ⑧ POURQUOI — une racine imbriquée (d/deux) qui
    n'aurait pas son `.git` lirait celui de son parent. ⑨ CE QUI CLOCHE — rien n'est poussé vers GitHub : le dépôt
    distant est un dossier local. ⑩ EFFET — écrit sous `d`. ⑪ TERMINAISON — Rend la main ; lève. [sort: non]"""
    if not os.path.isdir(os.path.join(d, ".git")):
        git_jetable(d, "init", "-q", "-b", "main")
    if not git_jetable(d, "remote"):
        nu = os.path.join(d, ".depot_nu")
        subprocess.run(["git", "init", "-q", "--bare", nu], check=True, capture_output=True)
        with open(os.path.join(d, ".git", "info", "exclude"), "a", encoding="utf-8") as f:
            f.write("\n.depot_nu/\n")
        git_jetable(d, "remote", "add", "origin", nu)


def git_jetable(d, *args):
    """Lance git dans un dépôt jetable.
    ① RÔLE — fabriquer une histoire. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — dossier, arguments.
    ④ CONDITIONS D'ENTRÉE — git installé. ⑤ SORTIE — UNE valeur : la sortie texte. [rend: 1] ⑥ TRAITEMENT — lancer,
    lever si le code est non nul. ⑦ UNITÉ — —. ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — git écrit dans `d`.
    ⑪ TERMINAISON — Rend la main ; lève. [sort: non]"""
    return subprocess.run(["git", "-C", d, "-c", "user.name=epreuve", "-c", "user.email=e@e"] + list(args),
                          capture_output=True, text=True, check=True).stdout.strip()


def cas(copie, racine):
    """Joue tous les cas sur une copie des programmes et rend leurs résultats.

    ① RÔLE — Le cœur de l'épreuve. ② CONTEXTE D'APPEL — le mode « --cas ». ③ ENTRÉE — le dossier de la copie, la
    racine. ④ CONDITIONS D'ENTRÉE — celles de l'en-tête. ⑤ SORTIE — UNE liste de (nom, vert : booléen, détail).
    [rend: 1] ⑥ TRAITEMENT — P : la portée ; L : la lecture du champ lignée ; G : la lignée ; R : les regards ;
    E : les essais ; PR : le premier regard ; B : le bilan ; K : k ; V0 : la vraie racine. ⑦ UNITÉ — —.
    ⑧ POURQUOI — voir l'en-tête. ⑨ CE QUI CLOCHE — voir l'en-tête. ⑩ EFFET — dossiers temporaires.
    ⑪ TERMINAISON — rend la main ; une erreur dans un cas le rend rouge. [sort: non]
    """
    sys.path.insert(0, os.path.join(copie, "programmes"))
    charger(os.path.join(copie, "programmes/COMMUN.py"), "COMMUN")
    C = charger(os.path.join(copie, "programmes/CONTRATS_DES_FICHIERS.py"), "CONTRATS_DES_FICHIERS")
    charger(os.path.join(copie, "programmes/JUGE_DES_STRATEGIES.py"), "JUGE_DES_STRATEGIES")
    T = charger(os.path.join(copie, ESSAIS), "TENIR_LE_REGISTRE_DES_ESSAIS")
    res = []

    def ok(nom, cond, det=""):
        """Range un cas. ① RÔLE — noter. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — nom, condition, détail.
        ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — aucune valeur. [rend: 0] ⑥ TRAITEMENT — ajouter. ⑦ UNITÉ — —.
        ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — modifie `res`. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        res.append((nom, bool(cond), det))

    def essai(nom, f):
        """Joue un groupe de cas dans un dossier temporaire ; une exception le rend rouge. ① RÔLE — isoler.
        ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — nom, fonction qui reçoit le dossier. ④ CONDITIONS D'ENTRÉE — —.
        ⑤ SORTIE — aucune valeur. [rend: 0] ⑥ TRAITEMENT — créer le dossier, appeler, effacer. ⑦ UNITÉ — —.
        ⑧ POURQUOI — une erreur n'est pas un vert. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — `res`, un dossier temporaire.
        ⑪ TERMINAISON — Rend la main. [sort: non]"""
        d = tempfile.mkdtemp(prefix="b2_%s_" % nom)
        try:
            f(d)
        except Exception as ex:
            res.append((nom, False, "%s: %s" % (type(ex).__name__, str(ex)[:200])))
        finally:
            shutil.rmtree(d, ignore_errors=True)

    # ── P : LA PORTÉE DU REGARD, LUE DANS UN FICHIER ──
    def p(d):
        poser_racine(d, C, portee=None)
        ok("P1 réglages absents : portée inconnue", T.portee_du_regard(d)[0] is None)
        poser_racine(d, C, en_tete=["cle", "valeur", "etat", "source"])
        ok("P2 en-tête hors de EN_TETE_DES_REGLAGES : portée inconnue", T.portee_du_regard(d)[0] is None)
        poser_racine(d, C, reglages=[["portee_du_regard", "fiche", "a", "b"], ["portee_du_regard", "lignee", "a", "b"]])
        ok("P3 clé écrite deux fois : portée inconnue", T.portee_du_regard(d)[0] is None)
        poser_racine(d, C, portee="famille")
        ok("P4 valeur hors du domaine (« famille ») : portée inconnue", T.portee_du_regard(d)[0] is None)
        for v in T.PORTEES_DU_REGARD:
            poser_racine(d, C, portee=v)
            ok("P4b « %s » se lit" % v, (T.portee_du_regard(d)[0] or {}).get("valeur") == v)
        vraie, r = T.portee_du_regard(racine)
        ok("P5 VRAI fichier du dépôt : « lignee », statut « À CONFIRMER PAR JEAN-LUC »",
           vraie is not None and vraie["valeur"] == "lignee" and "À CONFIRMER PAR JEAN-LUC" in vraie["statut"], repr((vraie, r)))
    essai("P", p)

    # ── L : LE CHAMP « lignee » ──
    def l(_d):
        ok("L1 « aucune » : aucun lien", T.liens_de_la_lignee("aucune") == [] and T.liens_de_la_lignee(" Aucune ") == [])
        ok("L2 « C5 → V1, V2 » : deux liens", T.liens_de_la_lignee("C5 → V1, V2") == [("C5", "V1"), ("C5", "V2")])
        ok("L3 deux morceaux, flèche « -> »", T.liens_de_la_lignee("A -> B ; B → D") == [("A", "B"), ("B", "D")])
        illisibles = ["", "   ", None, "A", "A → ", "A → B → C", "A B → C", "A → A", "→ B", "A → B,, C"]
        ko = [x for x in illisibles if T.liens_de_la_lignee(x) is not None]
        ok("L4 dix écritures illisibles rendent None (jamais « aucune »)", not ko, repr(ko))
    essai("L", l)

    decl_famille = [{"fiche_id": "MERE", "lignee": "MERE → FILLE1, FILLE2", "part_regardee": "2000-2023, rejeu du 28-10"},
                    {"fiche_id": "FILLE1", "lignee": "aucune"}, {"fiche_id": "SANS", "lignee": "aucune"},
                    {"fiche_id": "V9", "lignee": "C5 → V9"}]

    # ── G : LA LIGNÉE ──
    def g(d):
        poser_racine(d, C, declarations=decl_famille)
        fam, liens, r = T.lignee_de_la_fiche(d, "FILLE1")
        ok("G1 lignée de FILLE1 : sa mère et sa sœur (sens fille → mère)", fam == ["FILLE1", "FILLE2", "MERE"], repr((fam, r)))
        ok("G1b les liens disent leur source", ["MERE", "FILLE1", "déclaration de MERE du 2026-11-01T10:00+01:00"] in liens,
           repr(liens))
        ok("G2 une fiche sans lien : elle seule", T.lignee_de_la_fiche(d, "SANS")[0] == ["SANS"])
        fam, _l, r = T.lignee_de_la_fiche(d, "MERE-bis")
        ok("G2b une fiche INCONNUE du registre (« MERE-bis ») : lignée INCONNUE, jamais « elle seule » (D2)",
           fam is None and "inconnue" in r, repr((fam, r)))
        ok("G2c « mere », « Mere », « MERE » : la même lignée, sous la forme canonique",
           all(T.lignee_de_la_fiche(d, x)[0] == ["FILLE1", "FILLE2", "MERE"] for x in ("mere", "Mere", " MERE ")))
        T.preenregistrer(d, "V9", dict(HYP, periode="2030-01-01..2030-06-30"))
        ok("G6 un lien écrit dans la seule déclaration de la FILLE (C5 n'en a pas) : V9 est de la lignée de C5",
           T.lignee_de_la_fiche(d, "C5")[0] == ["C5", "V9"], repr(T.lignee_de_la_fiche(d, "C5")))
        h = T.empreinte_de_l_hypothese(dict(HYP, periode="2030-01-01..2030-02-28"))
        T.preenregistrer(d, "BALAYAGE", dict(HYP, periode="2030-01-01..2030-02-28"))
        T.preenregistrer(d, "B-V3", dict(HYP, periode="2030-01-01..2030-02-28", tp_pct=5.0), mere=h)
        ok("G3 lien du registre (case « mere ») : B-V3 et BALAYAGE sont d'une même lignée",
           T.lignee_de_la_fiche(d, "B-V3")[0] == ["B-V3", "BALAYAGE"], repr(T.lignee_de_la_fiche(d, "B-V3")))
        T.preenregistrer(d, "ORPHELINE", dict(HYP, tp_pct=6.0), mere="ffffffffffffffff")
        fam, _l, r = T.lignee_de_la_fiche(d, "SANS")
        ok("G4 une « mere » introuvable rend toute lignée inconnue", fam is None and "introuvable" in r, repr((fam, r)))
        d2 = os.path.join(d, "deux")
        poser_racine(d2, C, declarations=decl_famille + [{"fiche_id": "AUTRE", "lignee": "AUTRE V1"}])
        T.preenregistrer(d2, "AUTRE", HYP)
        fam, _l, r = T.lignee_de_la_fiche(d2, "SANS")
        ok("G5 un champ « lignee » illisible d'une fiche du registre : INCONNU, jamais « aucune »",
           fam is None and "illisible" in r, repr((fam, r)))
        d3 = os.path.join(d, "avenir")
        poser_racine(d3, C, declarations=[{"fiche_id": "F2030", "lignee": "F2030 → G2030", "date": "2030-01-05T10:00+01:00"}])
        ok("G7 une déclaration datée dans l'AVENIR dit quand même son lien (union de toutes les déclarations)",
           T.lignee_de_la_fiche(d3, "G2030")[0] == ["F2030", "G2030"], repr(T.lignee_de_la_fiche(d3, "G2030")))
        d4 = os.path.join(d, "union")
        poser_racine(d4, C, declarations=[{"fiche_id": "MERE", "lignee": "MERE → FILLE1"},
                                          {"fiche_id": "MERE", "lignee": "aucune", "date": "2030-01-05T10:00+01:00"}])
        ok("G8 une déclaration POSTÉRIEURE « aucune » n'efface pas le lien : l'UNION de toutes les lignes (D6b)",
           T.lignee_de_la_fiche(d4, "FILLE1")[0] == ["FILLE1", "MERE"], repr(T.lignee_de_la_fiche(d4, "FILLE1")))
        d5 = os.path.join(d, "espace")
        poser_racine(d5, C, declarations=[{"fiche_id": "MERE ", "lignee": "mere → Fille1"}])
        ok("G9 une déclaration dont l'identifiant porte une espace et une autre casse garde ses liens (D6c)",
           T.lignee_de_la_fiche(d5, "FILLE1")[0] == ["FILLE1", "MERE"], repr(T.lignee_de_la_fiche(d5, "FILLE1")))
        ok("G9b ... et `declaration_de_la_fiche` la trouve sous « mere » (le contrat comparait à l'octet, l.1581)",
           (C.declaration_de_la_fiche(d5, "mere", "2099-01-01T00:00+01:00") or {}).get("fiche_id") == "MERE")
        d6 = os.path.join(d, "inconnue")
        poser_racine(d6, C, declarations=[{"fiche_id": "INCONNUE", "lignee": "aucune"}])
        fam, _l, r = T.lignee_de_la_fiche(d6, "SANS")
        ok("G10 une ligne de déclaration au nom INCONNU du registre : lignée INCONNUE (défaut du fichier, D5)",
           fam is None and "inconnue" in r, repr((fam, r)))
        d7 = os.path.join(d, "fille_inconnue")
        poser_racine(d7, C, declarations=[{"fiche_id": "MERE", "lignee": "MERE → INCONNUE"}])
        fam, _l, r = T.lignee_de_la_fiche(d7, "SANS")
        ok("G11 une lignée qui nomme une fiche INCONNUE : lignée INCONNUE", fam is None and "inconnue" in r, repr((fam, r)))
    essai("G", g)

    # ── R : LES REGARDS, COMPTÉS SUR LA PORTÉE LUE ──
    def rr(d):
        poser_racine(d, C, declarations=decl_famille)
        b = T.preenregistrer(d, "FILLE2", dict(HYP, periode="2010-01-04..2012-12-31"))
        T.preenregistrer(d, "FILLE2", dict(HYP, periode="2024-01-02..2026-10-30"))
        ok("R1 portée « lignee » : l'essai de la SŒUR sur 2010-2012 est un regard de FILLE1 et de MERE",
           T.regards_sur_les_annees(d, EXAMEN, "FILLE1")[0] == [b] and T.regards_sur_les_annees(d, EXAMEN, "MERE")[0] == [b])
        ok("R1b ... pas de SANS, hors de la lignée", T.regards_sur_les_annees(d, EXAMEN, "SANS")[0] == [])
        poser_racine(d, C, portee="fiche", declarations=decl_famille)
        ok("R2 MÊME REGISTRE, réglage « fiche » : FILLE1 n'a plus de regard (changé sans toucher au code)",
           T.regards_sur_les_annees(d, EXAMEN, "FILLE1")[0] == [] and T.regards_sur_les_annees(d, EXAMEN, "FILLE2")[0] == [b])
        poser_racine(d, C, portee="toutes", declarations=decl_famille)
        ok("R2b réglage « toutes » : SANS voit le regard", T.regards_sur_les_annees(d, EXAMEN, "SANS")[0] == [b])
        poser_racine(d, C, portee="nimporte", declarations=decl_famille)
        vus, r = T.regards_sur_les_annees(d, EXAMEN, "FILLE1")
        ok("R3 réglage illisible : INCONNU, jamais une liste vide", vus is None, r)
        poser_racine(d, C, declarations=decl_famille)
        ok("R4 « sauf » retire le jugement lui-même", T.regards_sur_les_annees(d, EXAMEN, "FILLE1", sauf=(b,))[0] == [])
        T.preenregistrer(d, "SANS", dict(HYP, periode="n'importe quoi"))
        ok("R5 la période illisible d'une fiche HORS lignée ne rend pas FILLE1 inconnue",
           T.regards_sur_les_annees(d, EXAMEN, "FILLE1")[0] == [b])
        poser_racine(d, C, portee="toutes", declarations=decl_famille)
        ok("R5b ... mais la rend inconnue en portée « toutes »", T.regards_sur_les_annees(d, EXAMEN, "FILLE1")[0] is None)
        d3 = os.path.join(d, "bornes")
        poser_racine(d3, C, portee="fiche")
        T.preenregistrer(d3, "X", dict(HYP, periode="1999-01-04..2000-01-03"))
        T.preenregistrer(d3, "Y", dict(HYP, periode="1998-01-05..2000-01-02"))
        ok("R6 une période qui FINIT sur la première séance d'examen est un regard ; la veille, non",
           len(T.regards_sur_les_annees(d3, EXAMEN, "X")[0] or []) == 1 and T.regards_sur_les_annees(d3, EXAMEN, "Y")[0] == [])
    essai("R", rr)

    # ── E : LES ESSAIS DE LA LIGNÉE ──
    def e(d):
        poser_racine(d, C, declarations=decl_famille)
        T.preenregistrer(d, "FILLE1", HYP)
        T.preenregistrer(d, "FILLE1", HYP)                       # le même essai refait
        T.preenregistrer(d, "FILLE2", dict(HYP, tp_pct=5.0))
        T.preenregistrer(d, "MERE", dict(HYP, tp_pct=6.0))
        T.preenregistrer(d, "SANS", dict(HYP, tp_pct=7.0))
        ok("E1 essais de la fiche FILLE1 : 1 ; de sa lignée : 3 ; du registre : 4",
           T.nombre_d_essais(d, fiche_id="FILLE1") == (1, "") and T.nombre_d_essais(d, lignee_de="FILLE1") == (3, "")
           and T.nombre_d_essais(d) == (4, ""), repr(T.nombre_d_essais(d, lignee_de="FILLE1")))
        T.preenregistrer(d, "ORPHELINE", dict(HYP, tp_pct=8.0), mere="ffffffffffffffff")
        n, r = T.nombre_d_essais(d, lignee_de="FILLE1")
        ok("E2 lignée inconnue : nombre d'essais de la lignée INCONNU", n == "INCONNU", r)
    essai("E", e)

    # ── PR : LE PREMIER REGARD D'UNE LIGNÉE, DANS L'ORDRE DE L'HISTOIRE ──
    def pr(d):
        # Depuis la mission REGARD (tour 3), `premier_regard` lit la branche des regards et rend le NOM de l'entrée
        # (son `sommet_principal` est l'ancre de la déclaration) ; l'ordre est celui de cette branche.
        poser_racine(d, C, declarations=decl_famille)
        n1 = T.preenregistrer(d, "FILLE2", dict(HYP, periode="2010-01-04..2010-12-31"))
        n2 = T.preenregistrer(d, "FILLE1", dict(HYP, periode="2011-01-03..2011-12-30"))
        r1 = T.premier_regard(d, EXAMEN, "FILLE1")
        ok("PR1 portée « lignee » : le premier regard de FILLE1 est celui de sa sœur (1re entrée)", r1 == (n1, ""), repr(r1))
        poser_racine(d, C, portee="fiche", declarations=decl_famille)
        r2 = T.premier_regard(d, EXAMEN, "FILLE1")
        ok("PR2 portée « fiche » : son propre essai (2e entrée)", r2 == (n2, ""), repr(r2))
        ok("PR3 une fiche sans regard : « »", T.premier_regard(d, EXAMEN, "SANS") == ("", ""))
        poser_racine(d, C, portee=None, declarations=decl_famille)
        ok("PR4 réglages absents : None", T.premier_regard(d, EXAMEN, "FILLE1")[0] is None)
    essai("PR", pr)

    # ── B : LE BILAN, ET K ──
    def bb(d):
        git_jetable(d, "init", "-q")
        # de VRAIES fiches du registre (copié tel quel, pour k) : mère C5E10-QA-V1, filles C5E10-SELECTION et
        # C5E10-TP5-SL5 — une lignée SYNTHÉTIQUE posée sur de vrais identifiants
        decl_vraies = [{"fiche_id": "C5E10-QA-V1", "lignee": "C5E10-QA-V1 → C5E10-SELECTION, C5E10-TP5-SL5",
                        "part_regardee": "2000-2023, rejeu du 28-10"}]
        poser_racine(d, C, declarations=decl_vraies)
        shutil.copy(os.path.join(racine, "donnees/cac40_strategies.csv"), os.path.join(d, "donnees/cac40_strategies.csv"))
        git_jetable(d, "add", ".")
        git_jetable(d, "commit", "-qm", "registre")
        git_jetable(d, "update-ref", "refs/remotes/origin/main", "HEAD")   # k se lit sur la branche principale (REGARD)
        b0 = T.bilan_de_la_fiche(d, "C5E10-SELECTION", EXAMEN, "2099-01-01T00:00+01:00", "1")
        ok("B1 les clés du bilan, dans l'ordre de CLES_DU_BILAN", tuple(b0) == T.CLES_DU_BILAN, repr(tuple(b0)))
        ok("B2 aucun essai : « AUCUN REGARD INSCRIT », et le registre dit ne rien savoir d'avant lui",
           b0["annees_deja_regardees"] == "AUCUN REGARD INSCRIT" and b0["avant_le_registre"] == "HISTORIQUE NON COMPTABILISÉ")
        ok("B3 la part regardée DÉCLARÉE par la mère est rendue telle quelle",
           b0["parts_regardees_declarees"].get("C5E10-QA-V1") == "2000-2023, rejeu du 28-10", repr(b0["parts_regardees_declarees"]))
        ok("K1 VRAI registre des stratégies (copié dans un dépôt jetable) et un témoin : k = 69 (68 versions + 1)",
           (b0["k"] or {}).get("valeur") == 69 and (b0["k"] or {}).get("versions_comptees") == 68, repr(b0["k"]))
        b1 = T.bilan_de_la_fiche(d, "C5E10-SELECTION", EXAMEN)
        ok("K2 sans date de déclaration : k non compté, la raison le dit", b1["k"] is None and "k" in b1["raisons"])
        T.preenregistrer(d, "C5E10-TP5-SL5", dict(HYP, periode="2010-01-04..2010-12-31"))
        b2 = T.bilan_de_la_fiche(d, "C5E10-SELECTION", EXAMEN)
        ok("B4 un regard de la sœur : « OUI », lignée et essais rendus",
           b2["annees_deja_regardees"] == "OUI" and b2["lignee"] == ["C5E10-QA-V1", "C5E10-SELECTION", "C5E10-TP5-SL5"]
           and b2["essais_de_la_fiche"] == 0 and b2["essais_de_la_lignee"] == 1 and b2["essais_du_registre"] == 1, repr(b2))
        poser_racine(d, C, portee=None, declarations=decl_vraies)
        shutil.copy(os.path.join(racine, "donnees/cac40_strategies.csv"), os.path.join(d, "donnees/cac40_strategies.csv"))
        b3 = T.bilan_de_la_fiche(d, "C5E10-SELECTION", EXAMEN)
        ok("B5 réglages absents (fiche CONNUE) : « INCONNU », jamais « AUCUN REGARD INSCRIT »",
           b3["fiche_id"] == "C5E10-SELECTION" and b3["annees_deja_regardees"] == "INCONNU" and "regards" in b3["raisons"], repr(b3["annees_deja_regardees"]))
    essai("B", bb)

    # ── N : L'IDENTITÉ DE LA FICHE (relecteur neuf du lot B, tour 4, N1 MAJEUR) ──
    def n(d):
        poser_racine(d, C, portee="fiche")
        nom = T.preenregistrer(d, " fille1 ", dict(HYP, periode="2010-01-04..2010-12-31"))
        e = T.lire_le_registre(d)[0][nom]      # le registre vit sur la branche des regards (mission REGARD)
        ok("N1a « fille1 » avec espaces : l'entrée porte « FILLE1 », tel qu'écrit au registre", e["fiche_id"] == "FILLE1",
           e["fiche_id"])
        ok("N1a2 ... et c'est un regard de « FILLE1 », de « FILLE1 » suivi d'une espace et de « fille1 »",
           all(T.regards_sur_les_annees(d, EXAMEN, f)[0] == [nom] for f in ("FILLE1", "FILLE1 ", "fille1")))
        try:
            T.preenregistrer(d, "INCONNUE", HYP)
            refuse = False
        except ValueError:
            refuse = True
        ok("N1b un nom inconnu du registre des stratégies est REFUSÉ à l'écriture", refuse)
        vus, r = T.regards_sur_les_annees(d, EXAMEN, "INCONNUE")
        ok("N1d regards d'une fiche inconnue : INCONNU, jamais une liste vide", vus is None and "inconnue" in r, r)
        entree = {"nature": "PREENREGISTREMENT", "horodatage_paris": "2026-11-11T22:00:00+01:00", "alea": "0a0b0c0d",
                  "fiche_id": "fille2 ", "genre_d_essai": "ESSAI", "famille": "NON_DECLARE", "mere": "", "hypothese": dict(HYP, periode="2011-01-03..2011-12-30"),
                  "empreinte_hypothese": T.empreinte_de_l_hypothese(dict(HYP, periode="2011-01-03..2011-12-30")), "octets": {},
                  "periode_conception": "NON_DECLARE", "part_regardee": "NON_DECLARE", "regle_univers": "NON_DECLARE",
                  "date_regle_univers": "NON_DECLARE", "sommet_principal": "INCONNU"}   # champ du contrat (REGARD tour 3)
        ecrite = T._ecrire(d, entree, "NATURES_DES_ENTREES_D_ESSAI")
        ok("N1c une entrée ÉCRITE « fille2 » (hors de preenregistrer) compte pour FILLE2 : regard et essai",
           T.regards_sur_les_annees(d, EXAMEN, "FILLE2")[0] == [ecrite] and T.nombre_d_essais(d, fiche_id="FILLE2") == (1, ""),
           repr(T.regards_sur_les_annees(d, EXAMEN, "FILLE2")))
        d2 = os.path.join(d, "ambigu")
        poser_racine(d2, C, ids=("AB", "ab"))
        ok("N1e deux fiches qui ne diffèrent que par la casse : nom ambigu, refusé", C.identite_de_la_fiche(d2, "Ab")[0] is None)
        ok("N1f le préfixe n'est plus une identité : « CALIBRAGE:MERE » est inconnu (le calibrage est un GENRE, D3)",
           C.identite_de_la_fiche(d, "CALIBRAGE:MERE")[0] is None and C.identite_de_la_fiche(d, "Mere") == ("MERE", ""))
        inconnue = dict(entree, fiche_id="FILLEl", alea="0a0b0c0e")
        T._ecrire(d, inconnue, "NATURES_DES_ENTREES_D_ESSAI")
        _s, defauts = T.lire_le_registre(d)
        ok("N2 une entrée ÉCRITE au nom inconnu « FILLEl » (L minuscule) est un DÉFAUT de lecture, et les regards de "
           "FILLE1 deviennent INCONNUS (D5)", any("FILLEl" in x for x in defauts)
           and T.regards_sur_les_annees(d, EXAMEN, "FILLE1")[0] is None, repr(defauts))
        d3 = os.path.join(d, "genre")
        poser_racine(d3, C, portee="fiche")
        T._ecrire(d3, dict(entree, fiche_id="FILLE2", genre_d_essai="AUTRE"), "NATURES_DES_ENTREES_D_ESSAI")
        _s, defauts = T.lire_le_registre(d3)
        ok("N3 un genre d'essai hors de GENRES_D_ESSAI est un défaut de lecture", any("genre" in x for x in defauts),
           repr(defauts))
        try:
            T.preenregistrer(d3, "FILLE2", HYP, genre="AUTRE")
            ok("N3b ... et il est refusé à l'écriture", False)
        except ValueError:
            ok("N3b ... et il est refusé à l'écriture", True)
    essai("N", n)

    # ── C : LE CALIBRAGE, UN GENRE RATTACHÉ À SA FICHE (relecteur de B2, D3 ; question J3) ──
    def cal(d):
        poser_racine(d, C, declarations=decl_famille)
        c = T.preenregistrer(d, "fille2", dict(HYP, periode="2010-01-04..2010-12-31"), genre="CALIBRAGE")
        e = T.lire_le_registre(d)[0][c]        # le registre vit sur la branche des regards (mission REGARD)
        ok("C1 un calibrage s'écrit sur sa fiche (« FILLE2 ») avec le genre CALIBRAGE, sans préfixe",
           e["fiche_id"] == "FILLE2" and e["genre_d_essai"] == "CALIBRAGE", repr(e["fiche_id"]))
        ok("C2 réglage « oui » : le calibrage de la sœur est un regard de FILLE1, et un essai de FILLE2",
           T.regards_sur_les_annees(d, EXAMEN, "FILLE1")[0] == [c] and T.nombre_d_essais(d, fiche_id="FILLE2") == (1, ""))
        poser_racine(d, C, declarations=decl_famille, calibrage="non")
        ok("C3 MÊME REGISTRE, réglage « non » : plus un regard, toujours un essai",
           T.regards_sur_les_annees(d, EXAMEN, "FILLE1")[0] == [] and T.nombre_d_essais(d, fiche_id="FILLE2") == (1, ""))
        poser_racine(d, C, declarations=decl_famille, calibrage="peut-etre")
        ok("C4 réglage du calibrage illisible : regards INCONNUS", T.regards_sur_les_annees(d, EXAMEN, "FILLE1")[0] is None)
        vrai, r = T.calibrage_compte_comme_regard(racine)
        ok("C5 VRAI réglage du dépôt : « oui », statut « À CONFIRMER PAR JEAN-LUC »",
           vrai is not None and vrai["valeur"] == "oui" and "À CONFIRMER PAR JEAN-LUC" in vrai["statut"], repr((vrai, r)))
    essai("C", cal)

    # ── I : UNE FICHE INCONNUE EST INCONNUE, JAMAIS ZÉRO ; « Mere », « mere », « MERE » ONT LE MÊME BILAN (D1, D2) ──
    def inc(d):
        poser_racine(d, C, declarations=decl_famille)
        T.preenregistrer(d, "FILLE1", HYP)
        ok("I1 essais d'une fiche INCONNUE : INCONNU, jamais 0",
           T.nombre_d_essais(d, fiche_id="INCONNUE")[0] == "INCONNU" and T.nombre_d_essais(d, lignee_de="INCONNUE")[0] == "INCONNU")
        b = T.bilan_de_la_fiche(d, "INCONNUE", EXAMEN)
        ok("I2 bilan d'une fiche INCONNUE : regards, essais de la fiche et de la lignée INCONNUS, lignée None, raisons dites",
           b["annees_deja_regardees"] == "INCONNU" and b["essais_de_la_fiche"] == "INCONNU"
           and b["essais_de_la_lignee"] == "INCONNU" and b["lignee"] is None and "essais_de_la_fiche" in b["raisons"], repr(b))
        bs = [T.bilan_de_la_fiche(d, x, EXAMEN) for x in ("MERE", "Mere", " mere")]
        ok("I3 « MERE », « Mere », « mere » : le MÊME bilan, part regardée déclarée comprise (D1)",
           bs[0] == bs[1] == bs[2] and bs[0]["parts_regardees_declarees"].get("MERE") == "2000-2023, rejeu du 28-10"
           and bs[1]["fiche_id"] == "MERE", repr([x["parts_regardees_declarees"] for x in bs]))
        d2 = os.path.join(d, "parts")
        poser_racine(d2, C, declarations=[{"fiche_id": "MERE", "lignee": "aucune", "part_regardee": "2000-2023, rejeu du 02-10"},
                                          {"fiche_id": "mere", "lignee": "aucune", "part_regardee": "aucune"}])
        ok("I4 les parts regardées de TOUTES les déclarations, pas la dernière seule",
           T.bilan_de_la_fiche(d2, "MERE", EXAMEN)["parts_regardees_declarees"].get("MERE")
           == "2000-2023, rejeu du 02-10" + T.SEPARATEUR_DES_PARTS + "aucune",
           repr(T.bilan_de_la_fiche(d2, "MERE", EXAMEN)["parts_regardees_declarees"]))
    essai("I", inc)

    # ── V0 : LA VRAIE RACINE ──
    def v0(_d):
        b = T.bilan_de_la_fiche(racine, "C5E10-QA-V1", EXAMEN)
        ok("V0 vraie racine, C5E10-QA-V1 : réglage « lignee », lignée = elle seule, aucun regard INSCRIT",
           b["portee_du_regard"]["valeur"] == "lignee" and b["lignee"] == ["C5E10-QA-V1"]
           and b["annees_deja_regardees"] == "AUCUN REGARD INSCRIT", repr({k: b[k] for k in ("lignee", "regards", "raisons")}))
    essai("V0", v0)
    return res


def preparer(racine, sab):
    """Copie les programmes et applique un sabotage.
    ① RÔLE — Donner à chaque sabotage sa copie. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — la racine, le nom ou « Z0 ».
    ④ CONDITIONS D'ENTRÉE — chaque texte visé est présent UNE fois. ⑤ SORTIE — UNE valeur : le dossier. [rend: 1]
    ⑥ TRAITEMENT — copier, remplacer. ⑦ UNITÉ — —. ⑧ POURQUOI — une cible introuvable ne sabote rien : elle lève.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — crée un dossier temporaire. ⑪ TERMINAISON — rend la main ou lève LookupError.
    [sort: non]"""
    d = tempfile.mkdtemp(prefix="b2_%s_" % sab)
    os.makedirs(os.path.join(d, "programmes"))
    for f in (ESSAIS,) + VOISINS:
        shutil.copy(os.path.join(racine, f), os.path.join(d, f))
    for f, a, b in ([] if sab == "Z0" else SABOTAGES[sab]):
        p = os.path.join(d, f)
        t = open(p, encoding="utf-8").read()
        if t.count(a) != 1:
            shutil.rmtree(d)
            raise LookupError("sabotage %s : le texte visé est présent %d fois dans %s" % (sab, t.count(a), f))
        open(p, "w", encoding="utf-8").write(t.replace(a, b))
    return d


def jouer(racine, sab):
    """Relance ce programme en « --cas » sur la copie d'un sabotage et rend ses lignes.
    ① RÔLE — Isoler chaque copie dans son processus. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — racine, sabotage.
    ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : liste de (nom, vert, détail). [rend: 1] ⑥ TRAITEMENT —
    préparer, relancer (borné à 300 s), lire le JSON, effacer la copie. ⑦ UNITÉ — —. ⑧ POURQUOI — les modules ont
    les mêmes noms. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — dossiers temporaires. ⑪ TERMINAISON — rend la main ; un
    dépassement rend un cas rouge. [sort: non]"""
    d = preparer(racine, sab)
    try:
        r = subprocess.run([sys.executable, "-B", ICI, "--cas", d, racine], capture_output=True, text=True, timeout=300)
        try:
            return [tuple(x) for x in json.loads(r.stdout.strip().splitlines()[-1])]
        except (ValueError, IndexError):
            return [("relance", False, (r.stderr or r.stdout)[-400:])]
    except subprocess.TimeoutExpired:
        return [("relance", False, "plus de 300 s")]
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main(argv):
    """Joue Z0 puis les sabotages demandés.
    ① RÔLE — Le chef d'orchestre. ② CONTEXTE D'APPEL — la ligne de commande. ③ ENTRÉE — `argv`.
    ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1] ⑥ TRAITEMENT — « --cas » : jouer les
    cas et écrire leur JSON ; sinon Z0, puis les sabotages ; afficher. ⑦ UNITÉ — —. ⑧ POURQUOI — R-731, R-734.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — affiche. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    if argv[:1] == ["--cas"]:
        print(json.dumps(cas(argv[1], argv[2]), ensure_ascii=False))
        return 0
    if not argv:
        print(__doc__.split("\n\n")[2])
        return 2
    racine = os.path.abspath(argv[0])
    for f in ("donnees/REGLAGES_DU_REGISTRE_DES_ESSAIS.csv", "donnees/DECLARATIONS_DATEES.csv",
              "donnees/cac40_strategies.csv") + (ESSAIS,) + VOISINS:
        if not os.path.exists(os.path.join(racine, f)):
            print("DONNÉE MANQUANTE : %s" % f)
            return 2
    demandes = []
    if len(argv) > 1:
        demandes = list(SABOTAGES) if argv[1] == "--saboter" else [argv[1]]
        if any(s not in SABOTAGES for s in demandes):
            print("sabotage inconnu : %s" % argv[1])
            return 2
    try:
        z0 = jouer(racine, "Z0")
    except LookupError as ex:
        print(ex)
        return 2
    rouges = [x for x in z0 if not x[1]]
    for nom, vert, det in z0:
        print("  %s  %s%s" % ("VERT " if vert else "ROUGE", nom, ("  — " + det) if (det and not vert) else ""))
    print("== Z0 : %d cas, %d rouge(s)" % (len(z0), len(rouges)))
    code = 1 if rouges else 0
    for s in demandes:
        try:
            r = jouer(racine, s)
        except LookupError as ex:
            print(ex)
            return 2
        mord = [n for n, v, _d in r if not v]
        print("  %s  %s — %s" % ("MORD " if mord else "MUET ", s, ", ".join(mord[:4]) if mord else "aucun cas ne rougit"))
        if not mord:
            code = 1
    print("VERDICT : %s" % ("conforme" if code == 0 else "NON CONFORME"))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
