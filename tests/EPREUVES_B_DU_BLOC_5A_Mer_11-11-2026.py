"""ÉPREUVES DU BLOC 5a (agent B, plan V7) — la grille de validation, le registre des essais, la déclaration datée.
Simulation uniquement. Mercredi 11-11-2026.

LE SENS EN TÊTE — Le bloc 5 doit rendre « un verdict « validée » qui veut dire quelque chose ». Ces épreuves vérifient,
sur des cas dont on connaît la réponse : qu'une stratégie au gain net franc, qui bat le hasard, est validée ; qu'une
stratégie perdante est réfutée ; qu'il manque une mesure, une ligne de la loi, une déclaration ou un tirage, et la
validation tombe ; que les seuils et les rôles se LISENT dans la table de R-505 (changer la table change le verdict,
sans changer le code) ; que le registre des essais compte les hypothèses distinctes et voit une entrée altérée ou
antidatée ; que la déclaration s'ajoute sans réécrire et ne compte que commitée avant le regard. Une épreuve qui reste
verte quand on retire ce qu'elle teste est une décoration (R-731) : `--saboter` casse le code de toutes les façons de la table SABOTAGES (dont celles des relecteurs, portées) et
chacune doit faire rougir au moins un cas. AUCUN JUGEMENT DE C5 SUR 2000-2023 : les données sont synthétiques, ou de
vrais cours de 2024-2026 joués par un signal sans talent (cas V1).

USAGE : python3 -B tests/EPREUVES_B_DU_BLOC_5A_Mer_11-11-2026.py <racine> [--saboter | nom de sabotage]
CODE : 0 si Z0 est vert et que chaque sabotage joué fait rougir au moins un cas ; 1 sinon ; 2 si une cible de
sabotage est introuvable, si le nom est inconnu ou si les données manquent (R-734).

① RÔLE — Prouver que le bloc 5a fait ce que dit sa note, et que chaque garde a des dents.
② CONTEXTE D'APPEL — À la main ; par la certification (`programmes/CERTIFIER_LA_VERSION.py`), qui lance chaque fichier
  de tests/ avec la racine, puis avec « --saboter ». Ce programme se relance en « --cas <copie> <racine> ».
③ ENTRÉE — La racine du dépôt ; « --saboter » ou un nom de sabotage, facultatif.
④ CONDITIONS D'ENTRÉE — Sous la racine : les programmes MODULE_JUGEMENT, TENIR_LE_REGISTRE_DES_ESSAIS,
  DECLARER_UNE_STRATEGIE, CONTRATS_DES_FICHIERS, COMMUN, JUGE_DES_STRATEGIES, MODULE_POSITIONS ; `emp.py` ;
  `gouvernance/REGISTRE_REGLES.md` ; `donnees/DECLARATIONS_DATEES.csv`, `donnees/cac40_strategies.csv`,
  `donnees/cours_maitre.csv` ; git.
⑤ SORTIE — Le code de sortie dit en « CODE » ; une ligne par cas et par sabotage.
  [rend: 1]
⑥ TRAITEMENT — ① pour Z0 puis chaque sabotage : copier les trois programmes du bloc et leurs deux voisins dans un
  dossier temporaire, appliquer le sabotage (un texte présent UNE fois) · ② relancer ce programme en « --cas » sur la
  copie · ③ Z0 doit être vert ; un sabotage doit faire rougir au moins un cas.
⑦ UNITÉ — Probabilités sans unité ; gains en EUROS ; points morts en POURCENTS ; durées en SÉANCES.
⑧ POURQUOI — R-731, R-732 (un cas tiré d'une vraie ligne : G0, D1, D5, V1), R-734.
⑨ CE QUI CLOCHE — ① Le cas V1 ne connaît pas la vérité d'avance (signal périodique) : il exige seulement un verdict au
  contrat et jamais « Validée » sans étalon de hasard. ② Le juge (`juger`) n'appelle pas encore la grille : ces
  épreuves appellent la grille directement, l'appel par le juge sera éprouvé par l'agent A. ③ Les sabotages ne portent
  que sur les trois programmes du bloc 5a.
⑩ EFFET — Écrit et efface des dossiers temporaires (dont des dépôts git jetables) ; n'écrit rien sous la racine.
⑪ TERMINAISON — Chaque relance « --cas » est bornée à 600 secondes ; un dépassement compte comme rouge.
  [sort: oui — code de sortie]
"""
import csv, importlib.util, io, json, os, shutil, subprocess, sys, tempfile

ICI = os.path.abspath(__file__)
GRILLE = "programmes/MODULE_JUGEMENT.py"
ESSAIS = "programmes/TENIR_LE_REGISTRE_DES_ESSAIS.py"
DECL = "programmes/DECLARER_UNE_STRATEGIE.py"
VOISINS = ("programmes/CONTRATS_DES_FICHIERS.py", "programmes/COMMUN.py")

# LES SABOTAGES : (fichier, texte présent UNE fois, remplacement). Chacun retire ce qu'un cas teste.
SABOTAGES = {
    "S01_gain_sans_seuil": [(GRILLE, '"PASSE" if p_gain < s_preuve else "BLOQUE"', '"PASSE"')],
    "S02_hasard_lu_a_l_envers": [(GRILLE, "if g >= net_strategie)", "if g <= net_strategie)")],
    "S03_tirages_jamais_insuffisants": [(GRILLE, "elif 1.0 / n_t >= s_hasard:", "elif False:")],
    "S04_inconnu_ne_bloque_pas": [(GRILLE, '        if etat == "INCONNU":\n            return cle', '        pass')],
    "S05_role_toujours_condition": [(GRILLE, '        if v == "condition":\n            return "CONDITION", ""',
                                     '        if True:\n            return "CONDITION", ""')],
    "S06_declaration_ignoree": [(GRILLE, 'if c["declaration"]["etat"] == "BLOQUE":', "if False:")],
    "S07_annees_ignorees": [(GRILLE, "elif seances_hors_examen > 0:", "elif False:")],
    "S08_c7_a_l_envers": [(GRILLE, "bas > point_mort_pct) else", "bas < point_mort_pct) else")],
    "S09_k_ignore": [(GRILLE, "        nombre = nombre / k\n", "        nombre = nombre\n")],
    "S10_plancher_ignore": [(GRILLE, '"PASSE" if n_obs >= plancher else "BLOQUE"', '"PASSE"')],
    "S11_refutation_sans_condition": [(GRILLE, '_nombre_fini(rr["p_perdante"]) and rr["p_perdante"] < niveau',
                                       '_nombre_fini(rr["p_perdante"])')],
    "S12_embargo_faux": [(GRILLE, 'return int(nombre), ""', 'return int(nombre) + 1, ""')],
    "S13_embargo_sans_au_moins": [(GRILLE, 'm = re.search(r"au moins\\s+(\\d+)", texte.lower())', "m = None")],
    "S14_cas1_juge_le_surapprentissage": [(GRILLE, '        elif cas == "1":\n            c[cle] = _controle("SANS_OBJET"',
                                            '        elif cas == "jamais":\n            c[cle] = _controle("SANS_OBJET"')],
    "S15_hasard_le_plus_doux": [(GRILLE, "p = max(ps)", "p = min(ps)")],
    "S16_c8_a_l_envers": [(GRILLE, '("PASSE" if basse > 0 else "BLOQUE")', '("PASSE" if basse < 0 else "BLOQUE")')],
    # S21 recalé par la mission REGARD (12-11-2026) : la création exclusive vit dans `_pousser_l_entree` (une entrée de
    # même nom déjà sur la branche des regards fait lever), plus dans un `os.open(O_EXCL)` du disque.
    "S21_ecriture_non_exclusive": [(ESSAIS, '                    raise FileExistsError("entrée %s déjà inscrite sur la branche des regards" % nom)',
                                    "                    continue")],
    "S22_alteration_invisible": [(ESSAIS, "if hashlib.sha256(octets).hexdigest()[:16] != nom:", "if False:")],
    "S23_essais_refaits_comptes": [(ESSAIS, "    return len(hyp), \"\"",
                                    "    return sum(1 for e in entrees.values() if e[\"nature\"] == "
                                    "\"PREENREGISTREMENT\" and (fiche_id is None or e[\"fiche_id\"] == fiche_id)), \"\"")],
    "S24_compte_hors_de_la_branche": [(ESSAIS, '        if code != 0:\n            return "INCONNU", "le commit %s n\'est pas un ancêtre',
                                       '        if False:\n            return "INCONNU", "le commit %s n\'est pas un ancêtre')],
    # S28 et Y01 SUIVENT LE JUGE (12-11-2026) : REGARD tour 3 (13f55ff6) a réindenté la boucle de l'ajout seul et
    # réécrit le choix du premier regard ; leurs anciennes cibles étaient absentes (« --saboter » rendait 2). Même
    # propriété visée, cible actuelle.
    "S28_effacement_commis_invisible": [(ESSAIS, '            if chemin not in version:\n                defauts.append(',
                                         '            if False:\n                defauts.append(')],
    "S29_regard_sans_chevauchement": [(ESSAIS, "if p[0] <= examen[1] and examen[0] <= p[1]:", "if False:")],
    "S25_resultat_orphelin_admis": [(ESSAIS, 'if saines.get(p, {}).get("nature") != "PREENREGISTREMENT":',
                                     'if saines.get(p, {}).get("nature") == "jamais":')],
    "S26_aucune_ecrit_null": [(ESSAIS, "        return COMMUN.MOT_DE_L_HORIZON_AUCUNE", "        return None")],
    "S27_registre_abime_compte": [(ESSAIS, "    if defauts:\n        return \"INCONNU\", \"registre des essais abîmé",
                                   "    if False:\n        return \"INCONNU\", \"registre des essais abîmé")],
    "S31_declaration_reecrit_le_fichier": [(DECL, 'nouveau = avant + (b"" if avant.endswith(b"\\n") else b"\\n") + ',
                                            'nouveau = avant.split(b"\\n")[0] + b"\\n" + ')],
    # S35 : l'ajout seul retiré ET la relecture qui l'aurait vu : seul le cas D2 de l'épreuve reste pour le voir
    "S35_reecriture_sans_relecture": [(DECL, 'nouveau = avant + (b"" if avant.endswith(b"\\n") else b"\\n") + ',
                                       'nouveau = avant.split(b"\\n")[0] + b"\\n" + '),
                                      (DECL, '    if not relu.startswith(avant.rstrip(b"\\n")):', "    if False:")],
    "S32_declaration_incomplete_admise": [(DECL, "    if defauts:\n        raise ValueError(\"déclaration refusée",
                                           "    if False:\n        raise ValueError(\"déclaration refusée")],
    # S33 recalé, S34 RETIRÉ (mission REGARD tour 3, décision de Jean-Luc du 12-11-2026 à 09h04, « Reparer ») :
    # l'ancre est le `sommet_principal` du premier regard, et la marche de l'histoire du fichier des déclarations
    # (que S34 sabotait) n'existe plus.
    "S33_ancre_au_sommet_meme_apres_un_regard": [(DECL, "    ancre = sommet\n    if regard:", "    ancre = sommet\n    if False:")],
    # LES DOUZE SABOTAGES DU RELECTEUR (/tmp/relB_sondes/sabotages.sh), PORTÉS : même défaut, texte de la version 2
    "X01_epoques_toujours_passe": [(GRILLE, '    if raisons:\n        rendu["etat"] = "BLOQUE"', '    if False:\n        rendu["etat"] = "BLOQUE"')],
    "X02_frais_doubles_ignore": [(GRILLE, '_controle("PASSE" if m["gain_moyen_frais_doubles_eur"] > 0 else "BLOQUE",',
                                  '_controle("PASSE",')],
    "X03_sharpe_ignore": [(GRILLE, '_controle("PASSE" if 1.0 - m["sharpe_degonfle"] < s_preuve else "BLOQUE",',
                           '_controle("PASSE",')],
    "X04_declaration_inconnue_valide": [(GRILLE, 'c["declaration"] = _controle("INCONNU", raison=rejet("declaration_manquants")',
                                         'c["declaration"] = _controle("PASSE", raison=rejet("declaration_manquants")')],
    "X05_role_illisible_affichage": [(GRILLE, '        return None, "rôle illisible à la table de R-505 : « %s »" % table[cle]["valeur"]',
                                      '        return "AFFICHAGE", ""')],
    "X06_creux_ignore": [(GRILLE, '''    if m is None:
        c["creux_un_jeton"] = _controle("INCONNU", raison=r)''', '''    if m is None:
        c["creux_un_jeton"] = _controle("PASSE", raison=r)''')],
    "X07_resultats_multiples_admis": [(ESSAIS, '    defauts += ["préenregistrement %s : %d résultats" % (p, n) for p, n in '
                                       'sorted(vus.items()) if n > 1]', '    pass')],
    "X08_superficiel_admis": [(ESSAIS, '    if code != 0 or sortie.strip() != b"false":\n        return None, "histoire absente : dépôt '
                               'superficiel ou illisible"', '    if False:\n        return None, "histoire absente : dépôt '
                               'superficiel ou illisible"')],
    "X09_empreinte_hypothese_non_verifiee": [(ESSAIS, '            if recalc != e["empreinte_hypothese"]:', '            if False:')],
    "X10_c8_role_affichage_force": [(GRILLE, '    role8, r8 = role_du_controle(table, "borne_basse_du_gain")',
                                     '    role8, r8 = "AFFICHAGE", ""')],
    "X11_kelly_absent_passe": [(GRILLE, '''    if m is None:
        c["kelly"] = _controle("INCONNU", raison=r)''', '''    if m is None:
        c["kelly"] = _controle("PASSE", raison=r)''')],
    "X12_hasard_mode_illisible_ignore": [(GRILLE, '            if p is None:\n                raisons.append(r)',
                                          '            if p is None:\n                pass')],
    "X13_inclusion_accepte_un_etat_hors_contrat": [(GRILLE, "if not isinstance(etat, str) or etat not in etats or not "
                                                    "isinstance(role, str) or role not in roles:", "if False:")],
    "X14_garde_regard_texte_admis": [(GRILLE, '"regards_anterieurs": garder("regards_anterieurs", regards_anterieurs, '
                                      'textes(regards_anterieurs),', '"regards_anterieurs": garder("regards_anterieurs", '
                                      'regards_anterieurs, True,')],
    "X15_nan_dans_les_tirages": [(GRILLE, "if not _nombre_fini(net_strategie) or not all(_nombre_fini(g) for g in gains):",
                                  "if False:")],
    "X16_domaine_ignore": [(GRILLE, "    if not dans.get(domaine, False):", "    if False:")],
    # LES SABOTAGES SURVIVANTS DU RELECTEUR DU TOUR 2, et ceux des réparations du tour 3
    "Y01_premier_regard_le_dernier": [(ESSAIS, "    return min(vus, key=lambda n: (ajout[n], n)), \"\"",
                                       "    return max(vus, key=lambda n: (ajout[n], n)), \"\"")],
    "Y02_D38_relache_a_1_sur_n_plus_1": [(GRILLE, "            elif 1.0 / n_t >= s_hasard:", "            elif 1.0 / (n_t + 1) >= s_hasard:")],
    "Y03_C7_elargi_de_5_points": [(GRILLE, "bas > point_mort_pct) else", "bas + 5 > point_mort_pct) else")],
    "Y04_chevauchement_strict": [(ESSAIS, "if p[0] <= examen[1] and examen[0] <= p[1]:", "if p[0] < examen[1] and examen[0] < p[1]:")],
    "Y05_refutee_sans_regard_unique": [(GRILLE, 'c["annees_d_examen"]["etat"] == "PASSE" and c["regard_unique"]["etat"] == "PASSE"',
                                        'c["annees_d_examen"]["etat"] == "PASSE"')],
    "Y06_regard_de_toutes_les_fiches": [(ESSAIS, '        if perimetre != "toutes" and e["fiche_id"] not in perimetre:\n            continue',
                                         '        if False:\n            continue')],
    "Y07_strictesse_ignoree": [(GRILLE, '    if (sens == "<=" and not valeur <= ref) or (sens == ">=" and not valeur >= ref):',
                                '    if False:')],
    "Y08_mesure_incomplete_admise": [(GRILLE, "    if ecarts:\n        return None, \" ; \".join(ecarts)\n    entiers",
                                      "    if False:\n        return None, \" ; \".join(ecarts)\n    entiers")],
    "Y09_mesure_mal_typee_admise": [(GRILLE, "        elif not _nombre_fini(v):\n            return None, \"%s : %s = %r n'est pas un nombre fini\"",
                                     "        elif False:\n            return None, \"%s : %s = %r n'est pas un nombre fini\"")],
    "Y10_epoque_p_non_mesuree_admise": [(GRILLE, '                    inconnues.append("époque %s : %s" % (nom, proba["motif"]))',
                                         '                    pass')],
    "Y11_kelly_strict": [(GRILLE, '_controle("PASSE" if m["kelly"] >= kmin else "BLOQUE"', '_controle("PASSE" if m["kelly"] > kmin else "BLOQUE"')],
    "Y12_voisins_sans_compte": [(GRILLE, '        ok_v = m["n_voisins"] == n_exige and m["n_voisins_gagnants"] == m["n_voisins"]',
                                 '        ok_v = m["n_voisins_gagnants"] == m["n_voisins"]')],
    # LES SABOTAGES SURVIVANTS DU RELECTEUR DU TOUR 3 (M01 à M12, rapport brut du 11-11-2026), PORTÉS sur le code de
    # ce tour, et ceux des réparations D1, D2, D4, D5 et du regard par fiche
    "Z01_M01_epoque_perdante_au_sens_large": [(GRILLE, 'if proba["p_perdante"] < seuil_epoque:', 'if proba["p_perdante"] <= seuil_epoque:')],
    "Z02_M02_minimum_moins_un": [(GRILLE, '    if gagnantes < minimum:\n', '    if gagnantes < minimum - 1:\n')],
    "Z03_M03_refutation_au_sens_large": [(GRILLE, 'rr["p_perdante"] < niveau', 'rr["p_perdante"] <= niveau')],
    "Z04_M04_gain_un_jeton_nul_admis": [(GRILLE, '_controle("PASSE" if m["gain_un_jeton_eur"] > 0 else "BLOQUE"',
                                         '_controle("PASSE" if m["gain_un_jeton_eur"] >= 0 else "BLOQUE"')],
    "Z05_M05_strictesse_relachee_de_1pct_vers_le_haut": [(GRILLE, '(sens == "<=" and not valeur <= ref)',
                                                          '(sens == "<=" and not valeur <= ref * 1.01)')],
    "Z06_M06_strictesse_relachee_de_1pct_vers_le_bas": [(GRILLE, '(sens == ">=" and not valeur >= ref)',
                                                         '(sens == ">=" and not valeur >= ref * 0.99)')],
    "Z07_M07_sharpe_au_sens_large": [(GRILLE, '1.0 - m["sharpe_degonfle"] < s_preuve', '1.0 - m["sharpe_degonfle"] <= s_preuve')],
    "Z08_M08_pbo_jusqu_a_moins_un": [(GRILLE, 'not 0.0 <= v <= 1.0', 'not -1.0 <= v <= 1.0')],
    "Z09_D1_minimum_au_seuil_005": [(GRILLE, 'lu["parts_des_seances"], s_preuve, s_epoque)', 'lu["parts_des_seances"], 0.05, s_epoque)')],
    "Z10_D1_motif_des_epoques_ignore": [(GRILLE, '            return _controle("INCONNU", raison=lu["motif"])',
                                         '            return _controle("PASSE", raison=lu["motif"])')],
    "Z11_D2_essais_non_confrontes_a_k": [(GRILLE, 'elif kk is None or m["nombre_d_essais"] < kk:', 'elif kk is None:')],
    "Z12_D4_voisins_sans_reference": [(GRILLE, '        r = _au_moins_aussi_strict(nom, x, REFERENCES_DES_DRAPEAUX[nom])\n        if r:\n',
                                       '        r = _au_moins_aussi_strict(nom, x, REFERENCES_DES_DRAPEAUX[nom])\n        if False:\n')],
    "Z13_D4_ecart_des_voisins_ignore": [(GRILLE, 'elif m["ecart_pct"] != ecart_exige:', 'elif False:')],
    "Z14_frais_multiplicateur_ignore": [(GRILLE, 'elif not m["multiplicateur_des_frais"] >= mult:', 'elif False:')],
    "Z15_frais_sans_reference": [(GRILLE, '    if r:\n        return None, r\n    return mult, ""', '    return mult, ""')],
    "Z16_D5_wilson_sur_les_operations": [(GRILLE, 'bas = wilson_bas(n_obs, wr)', 'bas = wilson_bas(len(gains), wr)')],
    "Z17_fiche_non_nommee_admise": [(VOISINS[0], '    if not isinstance(fiche_id, str) or not fiche_id.strip():\n        return None, "fiche non '
                                     'nommée : %r" % (fiche_id,)\n    if fiches is None:',
                                     '    if False:\n        return None, "fiche non nommée : %r" % (fiche_id,)\n    if fiches is None:')],
    "Z18_declaration_ancree_sur_toutes_les_fiches": [(DECL, 'T.premier_regard(racine, annees_d_examen, fiche_id)',
                                                      'T.premier_regard(racine, annees_d_examen, "BONNE")')],
}


def charger(chemin, nom):
    """Charge un programme par son chemin.
    ① RÔLE — Prendre le module éprouvé dans la copie. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — chemin, nom.
    ④ CONDITIONS D'ENTRÉE — le fichier existe. ⑤ SORTIE — UNE valeur : le module. [rend: 1]
    ⑥ TRAITEMENT — spec_from_file_location, exécution, rangé dans sys.modules sous son nom. ⑦ UNITÉ — —.
    ⑧ POURQUOI — les modules du bloc s'importent entre eux par leur nom : ils doivent trouver la copie.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — charge du code. ⑪ TERMINAISON — Rend la main ; lève. [sort: non]"""
    spec = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nom] = m
    spec.loader.exec_module(m)
    return m


TABLE_SYNTHETIQUE = """texte avant
  **LES SEUILS DE CETTE LOI** — synthétique, pour l'épreuve

  | clé | valeur | ce qu'elle veut dire | source |
  |---|---|---|---|
  | seuil_de_preuve | 0,05 ÷ k | gain | épreuve |
  | plancher_observations | 30 | plancher | épreuve |
  | seuil_du_hasard | 0,05 ÷ k | hasard | épreuve |
  | kelly_minimum | 0,05 | filet | épreuve |
  | taux_face_au_point_mort | {c7} | ancien C7 | épreuve |
  | borne_basse_du_gain | condition | ancien C8 | épreuve |
  | refutation_borne_haute | 0,05 | réfutée | épreuve |
  | gain_un_jeton | affichage | Q-G2 | épreuve |
  | epoque_perdante | 0,05 | époque | épreuve |
  | surapprentissage_maximum | 0,30 | PBO | épreuve |
  | voisins | 26 voisins à ±10 %, tous gagnants | drapeau | épreuve |
  | frais_doubles | courtage et taxe × 2, gain > 0 | drapeau | épreuve |
  | creux_un_jeton | affichage | Q-G2 | épreuve |
  | embargo_sans_duree | {emb} | embargo | épreuve |

texte après
"""


def ops_synthetiques(gains, pas=3, debut="2030-01-01"):
    """Fabrique des opérations qui ne se chevauchent pas, une tous les `pas` jours ouvrés de calendrier fictif.
    ① RÔLE — Donner à la grille des opérations indépendantes par construction. ② CONTEXTE D'APPEL — `cas`.
    ③ ENTRÉE — les gains en euros, l'écart, la date de départ. ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — DEUX valeurs : les opérations, la liste triée des séances. [rend: 2]
    ⑥ TRAITEMENT — séances = jours consécutifs ; entrée au rang i·pas, sortie au rang i·pas+1. ⑦ UNITÉ — euros, jours.
    ⑧ POURQUOI — sans chevauchement, les observations retenues valent le nombre d'opérations (plancher maîtrisé).
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    import datetime as dt
    d0 = dt.date.fromisoformat(debut)
    seances = [(d0 + dt.timedelta(days=i)).isoformat() for i in range(len(gains) * pas + 5)]
    ops = []
    for i, g in enumerate(gains):
        ops.append({"net": float(g), "date_signal": seances[i * pas], "date_entree": seances[i * pas],
                    "date_sortie": seances[i * pas + 1], "valeur": "X"})
    return ops, seances


def poser_la_portee(d, C, portee):
    """Écrit sous `d` les réglages du registre des essais (portée du regard) et un fichier des déclarations vide.
    ① RÔLE — Donner aux cas du regard la racine que lit B2 (`regards_sur_les_annees` lit la portée dans
    `donnees/REGLAGES_DU_REGISTRE_DES_ESSAIS.csv` depuis le lot B2 du 11-11-2026). ② CONTEXTE D'APPEL — `cas` (R9,
    G15). ③ ENTRÉE — le dossier, le module des contrats, la portée (« fiche », « lignee », « toutes »).
    ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — aucune valeur. [rend: 0] ⑥ TRAITEMENT — écrire les deux fichiers.
    ⑦ UNITÉ — —. ⑧ POURQUOI — la portée est un réglage lu, jamais écrit dans le code (mission B2).
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit deux fichiers. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    os.makedirs(os.path.join(d, "donnees"), exist_ok=True)
    with open(os.path.join(d, "donnees/REGLAGES_DU_REGISTRE_DES_ESSAIS.csv"), "w", encoding="utf-8") as f:
        f.write("cle,valeur,statut,source\nportee_du_regard,%s,épreuve,épreuve\n"
                "calibrage_compte_comme_regard,oui,épreuve,épreuve\n"
                "poussees_des_regards,3,épreuve,épreuve (mission REGARD)\n"
                "depot_des_regards,%s,épreuve,épreuve (REGARD)\n" % (portee, os.path.join(d, ".depot_nu")))
    with open(os.path.join(d, "donnees/DECLARATIONS_DATEES.csv"), "w", encoding="utf-8") as f:
        f.write(",".join(C.DECLARATION_DATEE) + "\n")


IDS_DE_L_EPREUVE = ("SYN", "AUTRE", "AUTRE2", "C5-essai3", "BONNE", "ENTRE", "TARDIVE", "MEME", "NEUVE", "DISQUE")


def poser_le_registre(d):
    """Écrit sous `d` un registre des stratégies minimal qui porte les fiches de l'épreuve.
    ① RÔLE — `preenregistrer` refuse une fiche inconnue du registre des stratégies depuis B2 (N1 du relecteur neuf du
    lot B, tour 4) : chaque racine jetable doit donc porter ses fiches. ② CONTEXTE D'APPEL — `cas` (G15, R1 à R9,
    D4). ③ ENTRÉE — le dossier. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — aucune valeur. [rend: 0] ⑥ TRAITEMENT —
    écrire `donnees/cac40_strategies.csv` : en-tête « id », une ligne par identifiant de IDS_DE_L_EPREUVE.
    ⑦ UNITÉ — —. ⑧ POURQUOI — voir ①. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — écrit un fichier.
    ⑪ TERMINAISON — Rend la main. [sort: non]"""
    os.makedirs(os.path.join(d, "donnees"), exist_ok=True)
    with open(os.path.join(d, "donnees/cac40_strategies.csv"), "w", encoding="utf-8") as f:
        f.write("id\n" + "".join(i + "\n" for i in IDS_DE_L_EPREUVE))
    reglages = os.path.join(d, "donnees/REGLAGES_DU_REGISTRE_DES_ESSAIS.csv")
    if not os.path.exists(reglages):        # le seul réglage de l'écriture (mission REGARD) ; la portée reste absente
        with open(reglages, "w", encoding="utf-8") as f:
            f.write("cle,valeur,statut,source\npoussees_des_regards,3,épreuve,épreuve (mission REGARD)\n"
                    "depot_des_regards,%s,épreuve,épreuve (REGARD)\n" % os.path.join(d, ".depot_nu"))
    avec_depot_distant(d)


def avec_depot_distant(d):
    """Fait de `d` un dépôt git qui a SON dépôt distant nu, où vit la branche des regards (mission REGARD).
    ① RÔLE — Depuis le 12-11-2026, le registre des essais vit sur la branche des regards du dépôt distant de la branche
    principale, jamais sur le disque de travail. ② CONTEXTE D'APPEL — `poser_le_registre`. ③ ENTRÉE — le dossier.
    ④ CONDITIONS D'ENTRÉE — git. ⑤ SORTIE — aucune valeur. [rend: 0] ⑥ TRAITEMENT — `git init -b main` si `d/.git`
    manque ; dépôt nu `d/.depot_nu`, exclu par `.git/info/exclude`, déclaré « origin » s'il n'y en a pas.
    ⑦ UNITÉ — —. ⑧ POURQUOI — un dépôt distant par racine : deux racines ne partagent pas leurs regards.
    ⑨ CE QUI CLOCHE — le dépôt distant est un dossier local, jamais GitHub. ⑩ EFFET — écrit sous `d`.
    ⑪ TERMINAISON — Rend la main ; lève. [sort: non]"""
    g = lambda *a: subprocess.run(["git", "-C", d] + list(a), capture_output=True, check=True, text=True).stdout
    if not os.path.isdir(os.path.join(d, ".git")):
        g("init", "-q", "-b", "main")
    if not g("remote").strip():
        nu = os.path.join(d, ".depot_nu")
        subprocess.run(["git", "init", "-q", "--bare", nu], capture_output=True, check=True)
        with open(os.path.join(d, ".git", "info", "exclude"), "a", encoding="utf-8") as f:
            f.write("\n.depot_nu/\n")
        g("remote", "add", "origin", nu)


def au_disque(d, T):
    """Recopie sous `d/registre_essais/` les entrées de la branche des regards, pour éprouver le code qui lit encore le
    registre SUR LA BRANCHE PRINCIPALE (`nombre_d_essais(commit=…)`, `premier_regard`, l'ancrage de B3).
    ① RÔLE — Garder éprouvé, tel quel, le code d'avant la mission REGARD que celle-ci ne touche pas (B3 gelé : le
    retrait de l'ancrage par l'histoire attend Jean-Luc). ② CONTEXTE D'APPEL — R5, R8, D4. ③ ENTRÉE — le dossier, le
    module du registre. ④ CONDITIONS D'ENTRÉE — un dépôt distant (`avec_depot_distant`). ⑤ SORTIE — aucune valeur.
    [rend: 0] ⑥ TRAITEMENT — lire les octets de l'union de la branche, écrire ceux qui manquent. ⑦ UNITÉ — —.
    ⑧ POURQUOI — EN PRODUCTION, PLUS RIEN N'ÉCRIT LE REGISTRE SUR LA BRANCHE PRINCIPALE : ce geste est celui de
    l'épreuve, pas du système (conséquence déclarée dans echanges/A_RELIRE_REGARD.md). ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — écrit des fichiers. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    sommet, _r = T._sommet_distant(d)
    fichiers, _d = T._octets_de_la_branche(d, sommet) if sommet else ({}, [])
    os.makedirs(os.path.join(d, "registre_essais"), exist_ok=True)
    for f, o in fichiers.items():
        if not os.path.exists(os.path.join(d, "registre_essais", f)):
            open(os.path.join(d, "registre_essais", f), "wb").write(o)


def retoucher_sur_la_branche(d, T, nom, octets):
    """Pousse sur la branche des regards un commit EN AVANCE RAPIDE qui remplace (octets donnés) ou EFFACE (None)
    l'entrée `nom` — ce que le serveur accepte (superviseur J, M3).
    ① RÔLE — Fabriquer la retouche ou l'effacement commis. ② CONTEXTE D'APPEL — R3, l'épreuve du regard unique.
    ③ ENTRÉE — le dossier, le module du registre, le nom (16 hex), les octets ou None. ④ CONDITIONS D'ENTRÉE — l'entrée
    est au sommet. ⑤ SORTIE — aucune valeur. [rend: 0] ⑥ TRAITEMENT — arbre du sommet, entrée remplacée ou retirée,
    `commit-tree`, poussée sans forçage. ⑦ UNITÉ — —. ⑧ POURQUOI — l'ajout seul est une propriété de la LECTURE.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — pousse vers le dépôt distant local. ⑪ TERMINAISON — Rend la main ; lève. [sort: non]"""
    distant, ref, _suivi = T._depot_des_regards()
    sommet, _r = T._sommet_distant(d)
    git = T.git_de(d)
    _c, arbre = git("ls-tree", sommet, "registre_essais/")
    lignes = []
    for l in arbre.decode().splitlines():
        meta, _t, chemin = l.partition("\t")
        if os.path.basename(chemin) == nom + ".json":
            if octets is None:
                continue
            _c, blob = git("hash-object", "-w", "--stdin", entree=octets)
            meta = "100644 blob " + blob.decode().strip()
        lignes.append("%s\t%s" % (meta, os.path.basename(chemin)))
    _c, sous = git("mktree", entree="".join(l + "\n" for l in lignes).encode())
    haut_texte = ("040000 tree %s\tregistre_essais\n" % sous.decode().strip()) if lignes else ""
    _c, haut = git("mktree", entree=haut_texte.encode())
    c1, commit = git("-c", "user.name=e", "-c", "user.email=e@e", "commit-tree", haut.decode().strip(), "-p", sommet,
                     "-m", "retouche")
    commit = commit.decode().strip()
    if c1 != 0 or len(commit) != 40:          # jamais « push :<branche> », qui SUPPRIMERAIT la branche des regards
        raise RuntimeError("retouche : commit-tree impossible")
    code, _s = git("push", "-q", distant, "%s:%s" % (commit, ref))
    if code != 0:
        raise RuntimeError("retouche non poussée")


def cas(copie, racine):
    """Joue tous les cas sur une copie des programmes du bloc et rend leurs résultats.

    ① RÔLE — Le cœur de l'épreuve. ② CONTEXTE D'APPEL — le mode « --cas ». ③ ENTRÉE — le dossier de la copie, la
    racine. ④ CONDITIONS D'ENTRÉE — celles de l'en-tête. ⑤ SORTIE — UNE liste de (nom, vert : booléen, détail).
    [rend: 1] ⑥ TRAITEMENT — G : la grille ; R : le registre des essais ; D : la déclaration ; V1 : vrais cours.
    ⑦ UNITÉ — —. ⑧ POURQUOI — voir l'en-tête. ⑨ CE QUI CLOCHE — voir l'en-tête. ⑩ EFFET — dossiers temporaires.
    ⑪ TERMINAISON — rend la main ; une erreur dans un cas le rend rouge. [sort: non]
    """
    sys.path.insert(0, os.path.join(copie, "programmes"))
    COMMUN = charger(os.path.join(copie, "programmes/COMMUN.py"), "COMMUN")
    C = charger(os.path.join(copie, "programmes/CONTRATS_DES_FICHIERS.py"), "CONTRATS_DES_FICHIERS")
    J = charger(os.path.join(copie, GRILLE), "MODULE_JUGEMENT")
    T = charger(os.path.join(copie, ESSAIS), "TENIR_LE_REGISTRE_DES_ESSAIS")
    D = charger(os.path.join(copie, DECL), "DECLARER_UNE_STRATEGIE")
    res = []

    def ok(nom, cond, det=""):
        """Range un cas. ① RÔLE — noter. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — nom, condition, détail.
        ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — aucune valeur. [rend: 0] ⑥ TRAITEMENT — ajouter. ⑦ UNITÉ — —.
        ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — modifie `res`. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        res.append((nom, bool(cond), det))

    def essai(nom, f):
        """Joue un cas, une exception le rend rouge. ① RÔLE — isoler. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — nom,
        fonction. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — aucune valeur. [rend: 0] ⑥ TRAITEMENT — appeler.
        ⑦ UNITÉ — —. ⑧ POURQUOI — une erreur n'est pas un vert. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — `res`.
        ⑪ TERMINAISON — Rend la main. [sort: non]"""
        try:
            f()
        except Exception as ex:
            res.append((nom, False, "%s: %s" % (type(ex).__name__, str(ex)[:200])))

    table = lambda c7="condition", emb="plus longue détention observée, au moins 21": J.table_de_la_loi(
        TABLE_SYNTHETIQUE.format(c7=c7, emb=emb))
    # DES MESURES, JAMAIS UN ÉTAT (simplification 1) : la grille calcule l'état
    tout_passe = {"kelly": {"kelly": 0.2, "gain_moyen_net_eur": 500.0},
                  "voisins": {"n_voisins": 26, "n_voisins_gagnants": 26, "ecart_pct": 10.0},
                  "frais_doubles": {"gain_moyen_frais_doubles_eur": 300.0, "multiplicateur_des_frais": 2.0},
                  "gain_un_jeton": {"gain_un_jeton_eur": 1000.0},
                  "creux_un_jeton": {"creux_un_jeton_eur": -2000.0}}
    mesures_cas2 = {"surapprentissage": {"pbo": 0.10, "nombre_d_essais": 5},
                    "sharpe_degonfle": {"sharpe_degonfle": 0.999, "nombre_d_essais": 5}}

    def hasard(net, n, au_dessus=0):
        """Un étalon de hasard synthétique : `n` tirages, dont `au_dessus` font au moins aussi bien que `net`.
        ① RÔLE — maîtriser p. ② CONTEXTE D'APPEL — les cas G. ③ ENTRÉE — net, nombre, nombre au-dessus.
        ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : un rendu au format d'`etalon_hasard`. [rend: 1]
        ⑥ TRAITEMENT — gains sous `net`, puis `au_dessus` gains au-dessus. ⑦ UNITÉ — euros. ⑧ POURQUOI — vérité connue.
        ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        g = sorted([net - 1000.0 - i for i in range(n - au_dessus)] + [net + 1.0 + i for i in range(au_dessus)])
        return {"n_tirages": n, "gains_des_tirages": g}

    # Une stratégie au gain franc : 60 opérations, 40 gagnantes à +900 €, 20 perdantes à −300 € (point mort fictif 40 %).
    bonnes, seances = ops_synthetiques([900] * 40 + [-300] * 20)
    import random
    random.Random(7).shuffle(bonnes)   # gains mêlés, dates gardées dans l'ordre
    for i, o in enumerate(bonnes):
        o["date_signal"] = o["date_entree"] = seances[i * 3]
        o["date_sortie"] = seances[i * 3 + 1]
    net_bon = sum(o["net"] for o in bonnes)
    # LES ÉPOQUES SONT DÉCLARÉES, LA GRILLE LES CALCULE (D1) : deux moitiés des années d'examen synthétiques
    _m = len(seances) // 2
    epoques_args = dict(epoques_declarees="%s..%s ; %s..%s" % (seances[0], seances[_m - 1], seances[_m], seances[-1]),
                        annees_d_examen="%s..%s" % (seances[0], seances[-1]), seances_d_examen=seances)

    def g_base(**kw):
        """La grille sur la bonne stratégie, tout fourni, avec des remplacements. ① RÔLE — un appel de référence.
        ② CONTEXTE D'APPEL — les cas G. ③ ENTRÉE — les arguments à remplacer. ④ CONDITIONS D'ENTRÉE — —.
        ⑤ SORTIE — UNE valeur : le rendu de la grille. [rend: 1] ⑥ TRAITEMENT — composer, appeler. ⑦ UNITÉ — —.
        ⑧ POURQUOI — un cas = un écart à la référence. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main. [sort: non]"""
        a = dict(table=table(), cas="1", k=1, ops=bonnes, point_mort_pct=40.0, declaration_manquants=[],
                 seances_hors_examen=0, regards_anterieurs=[], hasard=[hasard(net_bon, 2000)],
                 mesures_externes=tout_passe, **epoques_args)
        a.update(kw)
        return J.grille_de_validation(**a)

    VALIDEE = C.MOTS_DU_VERDICT[0]

    # G0 — VRAIE LIGNE (R-732) : la table de R-505 du REGISTRE du jour se lit, et sa ligne du plancher vaut 30.
    def g0():
        t = J.table_de_la_loi(open(os.path.join(racine, "gouvernance/REGISTRE_REGLES.md"), encoding="utf-8").read())
        ok("G0 table réelle de R-505 : plancher_observations = 30, seuil_de_preuve = 0,05 ÷ k (k = 69 → 0,000725)",
           J.seuil_de_la_loi(t, "plancher_observations") == (30.0, "")
           and abs(J.seuil_de_la_loi(t, "seuil_de_preuve", 69)[0] - 0.05 / 69) < 1e-15,
           "%r" % (J.seuil_de_la_loi(t, "seuil_de_preuve", 69),))
        # avec la table réelle du jour, les rôles de C7 et C8 manquent : rien n'est validé (dépendance envers A)
        r = g_base(table=t)
        ok("G0b table réelle du 11-11 : pas de validation tant que la ligne de C7 manque",
           r["verdict"] != VALIDEE and r["premier_controle_bloquant"] == "taux_face_au_point_mort",
           "%s / %s / %s" % (r["verdict"], r["motif"], r["premier_controle_bloquant"]))
    essai("G0", g0)

    def compose(r):
        """Compose un verdict complet autour du rendu de la grille. ① RÔLE — confronter au contrat VERDICT.
        ② CONTEXTE D'APPEL — G1. ③ ENTRÉE — le rendu de la grille. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur :
        la liste des écarts. [rend: 1] ⑥ TRAITEMENT — remplir ce que le juge ajoutera, confronter. ⑦ UNITÉ — —.
        ⑧ POURQUOI — la grille rend la partie du verdict qui lui revient. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main. [sort: non]"""
        return C.ecarts_d_une_entree("verdict composé", dict(
            regle="R-505 v1 du 04-11-2026", date_verdict="2030-12-31T20:00:00+01:00", fiche_id="SYN",
            cas="1", declaration={"date_declaration": "x", "empreinte": "y"}, verdict=r["verdict"], motif=r["motif"],
            premier_controle_bloquant=r["premier_controle_bloquant"],
            k={c: 1 for c in C.K_DU_VERDICT} | {"compte": C.COMPTES_DE_K[0]}, seuil_de_preuve=r["seuil_de_preuve"],
            controles=r["controles"],
            affichages={a: {"valeur": None, "confiance": None, "raison": ""} for a in C.AFFICHAGES_DU_VERDICT},
            empreinte_code_juge="z", preenregistrement="p"), "VERDICT")

    def g1():
        r = g_base()
        ok("G1 stratégie au gain franc, hasard battu (2000 tirages) : Validée", r["verdict"] == VALIDEE,
           "%s / %s / %s" % (r["verdict"], r["motif"], r["premier_controle_bloquant"]))
        ok("G1c seize contrôles, dans l'ordre du contrat", list(r["controles"]) == list(C.CONTROLES_DU_VERDICT))
        ecarts = compose(r)
        ok("G1b le verdict composé avec la grille, VRAIES époques comprises, tient le contrat VERDICT "
           "(la grille ne garde que les champs du contrat)", not ecarts, "; ".join(ecarts)[:300])
    essai("G1", g1)

    def g2():
        r = g_base(hasard=[hasard(net_bon, 15)])
        ok("G2 15 tirages pour un seuil de 0,05 ÷ 1 (1/15 ≥ 0,05) : hasard INCONNU, pas de validation",
           r["verdict"] == C.MOTS_DU_VERDICT[2] and r["motif"] == "MESURE MANQUANTE bat_le_hasard", r["motif"])
        r = g_base(hasard=[hasard(net_bon, 2000, au_dessus=150)])
        ok("G2b 150 tirages sur 2000 font mieux : p = 151/2001 > 0,05 → NE BAT PAS LE HASARD",
           r["motif"] == "NE BAT PAS LE HASARD" and abs(r["controles"]["bat_le_hasard"]["valeur"] - 151 / 2001) < 1e-12,
           "%s %r" % (r["motif"], r["controles"]["bat_le_hasard"]["valeur"]))
        r = g_base(hasard=[hasard(net_bon, 2000), hasard(net_bon, 2000, au_dessus=150)])
        ok("G2c deux modes, l'un battu de peu : le plus strict décide", r["motif"] == "NE BAT PAS LE HASARD", r["motif"])
        p, n, _ = J.p_du_hasard(10.0, {"gains_des_tirages": list(range(11))})
        ok("G2d p_du_hasard : 11 tirages 0..10, la stratégie à 10 → p = 2/12", abs(p - 2 / 12) < 1e-12 and n == 11)
    essai("G2", g2)

    def g3():
        mauvaises, _s = ops_synthetiques([-900] * 40 + [300] * 20)
        r = g_base(ops=mauvaises, hasard=[hasard(sum(o["net"] for o in mauvaises), 2000, au_dessus=1500)])
        ok("G3 stratégie perdante franche : RÉFUTÉE", r["verdict"] == C.MOTS_DU_VERDICT[1], r["verdict"])
        t = J.table_de_la_loi(TABLE_SYNTHETIQUE.format(c7="condition", emb="30").replace(
            "  | refutation_borne_haute | 0,05 | réfutée | épreuve |\n", ""))
        r = g_base(ops=mauvaises, table=t)
        ok("G3b sans la ligne refutation_borne_haute : jamais RÉFUTÉE, NE BAT PAS ZÉRO",
           r["verdict"] == C.MOTS_DU_VERDICT[2] and r["motif"] == "NE BAT PAS ZÉRO", "%s / %s" % (r["verdict"], r["motif"]))
    essai("G3", g3)

    def g4():
        r = g_base(declaration_manquants=["lignee", "hypothese"])
        ok("G4 déclaration sans lignée : NON JUGEABLE, motif « lignee »",
           r["verdict"] == C.MOTS_DU_VERDICT[3] and r["motif"] == "lignee", "%s / %s" % (r["verdict"], r["motif"]))
        r = g_base(seances_hors_examen=12)
        ok("G4b 12 séances hors des années d'examen : NON TRANCHÉE (DONNÉES DE CHOIX)",
           r["motif"] == "DONNÉES DE CHOIX", r["motif"])
        r = g_base(regards_anterieurs=["0123456789abcdef"])
        ok("G4c second regard : pas de validation", r["verdict"] != VALIDEE, r["verdict"])
    essai("G4", g4)

    def g5():
        # C7 : 40 opérations, 30 % de gagnantes à +5 000 €, 70 % de perdantes à −500 € ; point mort 50 %.
        rares, _s = ops_synthetiques(([5000] * 3 + [-500] * 7) * 4)
        hz = [hasard(sum(o["net"] for o in rares), 2000)]
        base5 = dict(ops=rares, point_mort_pct=50.0, hasard=hz)
        r = g_base(**base5)
        ok("G5 C7 en condition : taux sous le point mort → pas de validation, C7 nommé",
           r["verdict"] != VALIDEE and r["premier_controle_bloquant"] == "taux_face_au_point_mort",
           "%s / %s" % (r["verdict"], r["premier_controle_bloquant"]))
        r = g_base(table=table(c7="affichage"), **base5)
        ok("G5b C7 en affichage (la table change, le code non) : Validée", r["verdict"] == VALIDEE,
           "%s / %s / %s" % (r["verdict"], r["motif"], r["premier_controle_bloquant"]))
        t = J.table_de_la_loi(TABLE_SYNTHETIQUE.format(c7="condition", emb="30").replace(
            "  | taux_face_au_point_mort | condition | ancien C7 | épreuve |\n", ""))
        r = g_base(table=t)
        ok("G5c ligne de C7 absente : rôle INCONNU, pas de validation",
           r["motif"] == "MESURE MANQUANTE taux_face_au_point_mort", r["motif"])
    essai("G5", g5)

    def g6():
        r = g_base(k=10)
        ok("G6 seuil « 0,05 ÷ k » avec k = 10 : seuil de preuve 0,005",
           abs(r["seuil_de_preuve"] - 0.005) < 1e-15, "%r" % r["seuil_de_preuve"])
        r = g_base(k="INCONNU")
        ok("G6b k INCONNU : gain INCONNU, pas de validation", r["motif"] == "MESURE MANQUANTE gain_bat_zero", r["motif"])
        peu, _s = ops_synthetiques([900] * 15 + [-300] * 5)
        r = g_base(ops=peu, hasard=[hasard(sum(o["net"] for o in peu), 2000)])
        ok("G6c 20 observations sous le plancher de 30 : TROP PETIT", r["motif"] == "TROP PETIT", r["motif"])
    essai("G6", g6)

    def g7():
        r = g_base(cas="2", mesures_externes=tout_passe)
        ok("G7 cas 2 sans mesure de surapprentissage : INCONNU, pas de validation",
           r["motif"] == "MESURE MANQUANTE surapprentissage", r["motif"])
        r = g_base(cas="1")
        ok("G7b cas 1 : le surapprentissage est SANS_OBJET",
           r["controles"]["surapprentissage"]["etat"] == "SANS_OBJET")
        r = g_base(mesures_externes={**tout_passe, "voisins": {"n_voisins": 26, "n_voisins_gagnants": 25, "ecart_pct": 10.0}})
        ok("G7c drapeau des voisins levé (25 gagnants sur 26) : DRAPEAU", r["motif"] == "DRAPEAU", r["motif"])
        r = g_base(mesures_externes={**tout_passe, "kelly": {"kelly": 0.01, "gain_moyen_net_eur": 500.0}})
        ok("G7d Kelly 0,01 sous 0,05 : KELLY", r["motif"] == "KELLY", r["motif"])
        r = g_base(mesures_externes={c: v for c, v in tout_passe.items() if c != "gain_un_jeton"})
        ok("G7e gain en un jeton non mesuré : aucun INCONNU admis, pas de validation", r["verdict"] != VALIDEE,
           r["motif"])
    essai("G7", g7)

    def g8():
        # C8 : borne basse du gain sous zéro (gains très dispersés, moyenne faible), C7 en affichage pour l'isoler
        dispersees, _s = ops_synthetiques([20000, -19000] * 30)
        r = g_base(ops=dispersees, table=table(c7="affichage"), point_mort_pct=10.0,
                   hasard=[hasard(sum(o["net"] for o in dispersees), 2000)])
        ok("G8 C8 : borne basse du gain moyen sous zéro → pas de validation",
           r["verdict"] != VALIDEE and r["controles"]["borne_basse_du_gain"]["etat"] == "BLOQUE",
           "%s / %s" % (r["verdict"], r["controles"]["borne_basse_du_gain"]))
    essai("G8", g8)

    def g9():
        A = COMMUN.HORIZON_AUCUNE
        e, _r = J.embargo_de_la_strategie(A, bonnes, seances, table(emb="35"))
        ok("G9 embargo « aucune », table = 35 : 35 séances", e == 35, repr(e))
        longues = [dict(o) for o in bonnes]
        longues[5]["date_sortie"] = seances[5 * 3 + 40]
        e, _r = J.embargo_de_la_strategie(A, longues, seances, table())
        ok("G9b « plus longue détention, au moins 21 » : la détention de 40 séances l'emporte", e == 40, repr(e))
        e, _r = J.embargo_de_la_strategie(A, bonnes, seances, table())
        ok("G9c détentions d'une séance : le plancher écrit, 21, l'emporte", e == 21, repr(e))
        e, r = J.embargo_de_la_strategie(20, bonnes, seances, table())
        ok("G9d horizon entier : aucun embargo imposé (la coupure garde sa règle)", e is None and r == "")
        t = J.table_de_la_loi(TABLE_SYNTHETIQUE.format(c7="condition", emb="30").replace(
            "  | embargo_sans_duree | 30 | embargo | épreuve |\n", ""))
        e, r = J.embargo_de_la_strategie(A, bonnes, seances, t)
        ok("G9e ligne absente : pas d'embargo, la raison le dit", e is None and "absente" in r, r)
        # le contrat du lot 0 : « aucune » sans embargo explicite fait tomber la coupure et les fenêtres
        # la coupure reçoit sa frontière (exigée depuis le 12-11-2026, mission TRI : la frontière est une donnée établie
        # une fois, lue partout et jamais recalculée, R-708 ; décision du superviseur du tri, tour 3 ; réparation G9 du
        # 13-11-2026, superviseur R-759) : le refus attendu en G9f reste CELUI DE L'HORIZON « aucune », et G9g compare
        # les deux membres sur la MÊME frontière
        for nom, f in (("coupure", lambda **k: J.coupure_70_30(bonnes, seances,
                                                             frontiere=J.frontiere_de_la_fiche({}, seances, None), **k)),
                       ("fenetres", lambda **k: J.fenetres_glissantes(bonnes, seances, n=3, **k))):
            try:
                f(horizon=A)
                ok("G9f %s : « aucune » sans embargo est refusée" % nom, False, "pas d'erreur")
            except TypeError as ex:
                ok("G9f %s : « aucune » sans embargo est refusée" % nom, COMMUN.MESSAGE_DE_L_HORIZON_AUCUNE[:30] in str(ex))
            cle = "embargo_seances" if nom == "coupure" else "embargo"
            a, b = f(horizon=A, **{cle: 25}), f(horizon=20, **{cle: 25})
            ok("G9g %s : « aucune » avec embargo 25 = horizon 20 avec embargo 25" % nom, a == b)
    essai("G9", g9)

    def g10():
        try:
            J.table_de_la_loi(TABLE_SYNTHETIQUE.format(c7="condition", emb="30") .replace(
                "  | kelly_minimum | 0,05 | filet | épreuve |\n",
                "  | kelly_minimum | 0,05 | filet | épreuve |\n  | kelly_minimum | 0,10 | filet | épreuve |\n"))
            ok("G10 une clé écrite deux fois est refusée", False, "acceptée")
        except ValueError:
            ok("G10 une clé écrite deux fois est refusée", True)
        try:
            J.table_de_la_loi("rien ici")
            ok("G10b titre absent : refus", False)
        except ValueError:
            ok("G10b titre absent : refus", True)
    essai("G10", g10)

    def g10c():
        # le DOMAINE, là où la strictesse ne suffit pas : 0 est « plus strict » que toute référence « <= », mais n'est pas
        # une probabilité ; « 0,05 ÷ k » avec k = 0 non plus
        t0 = lambda cle: J.table_de_la_loi(TABLE_SYNTHETIQUE.format(c7="condition", emb="30").replace(
            "| %s | 0,05 |" % cle, "| %s | 0 |" % cle))
        ok("G10c domaine : refutation_borne_haute « 0 » refusée (pas une probabilité)",
           J.seuil_de_la_loi(t0("refutation_borne_haute"), "refutation_borne_haute")[0] is None)
        t1 = J.table_de_la_loi(TABLE_SYNTHETIQUE.format(c7="condition", emb="30").replace(
            "| seuil_de_preuve | 0,05 ÷ k |", "| seuil_de_preuve | 0 |"))
        ok("G10d domaine : seuil_de_preuve « 0 » refusé", J.seuil_de_la_loi(t1, "seuil_de_preuve", 1)[0] is None)
    essai("G10c", g10c)

    # ── G11 à G13 : CAS GÉNÉRÉS DEPUIS LE CONTRAT (superviseur R-759, point 3) ──
    import copy, math
    NAN = float("nan")
    reference = g_base()

    def g11():
        # niveau du verdict : chaque clé de CONTROLES_DU_VERDICT, isolément, mise hors de l'état qui autorise
        base = copy.deepcopy(reference["controles"])
        ok("G11-0 la référence passe l'inclusion", J.verdict_par_inclusion(base, C.CONTROLES_DU_VERDICT, "1") == "")
        n_cas = n_bons = 0
        for cle in C.CONTROLES_DU_VERDICT:
            role = base[cle]["role"]
            pert = [("etat", "INCONNU"), ("etat", "ROUGE"), ("etat", "passe"), ("etat", NAN), ("etat", None),
                    ("role", "affichage"), ("role", None), ("absente", None), ("pas_un_dict", None)]
            pert += [("etat", "BLOQUE")] if role == "CONDITION" else []
            pert += [("etat", "SANS_OBJET")] if cle not in J.SANS_OBJET_EN_CAS_1 else []
            for champ, v in pert:
                x = copy.deepcopy(base)
                if champ == "absente":
                    del x[cle]
                elif champ == "pas_un_dict":
                    x[cle] = "PASSE"
                else:
                    x[cle][champ] = v
                n_cas += 1
                n_bons += J.verdict_par_inclusion(x, C.CONTROLES_DU_VERDICT, "1") == cle
        ok("G11 %d perturbations isolées de la référence (16 clés × état/rôle hors contrat, BLOQUE, INCONNU, NaN, "
           "SANS_OBJET hors ⑧) : chacune nomme sa clé, jamais « Validée »" % n_cas, n_bons == n_cas,
           "%d / %d" % (n_bons, n_cas))
        x = copy.deepcopy(base)
        for cle in J.SANS_OBJET_EN_CAS_1:
            x[cle]["etat"] = "SANS_OBJET"
        ok("G11b ⑧ SANS_OBJET : admis en cas 1, refusé en cas 2",
           J.verdict_par_inclusion(x, C.CONTROLES_DU_VERDICT, "1") == ""
           and J.verdict_par_inclusion(x, C.CONTROLES_DU_VERDICT, "2") == "surapprentissage")
    essai("G11", g11)

    def g12():
        # niveau des ENTRÉES : chaque canal, isolément, BLOQUE / INCONNU / hors contrat / NaN → jamais « Validée » ;
        # puis CHAQUE CHAMP de chaque mesure retiré un par un, puis mal typé (superviseur, N-A)
        ext = lambda cle, v: {**tout_passe, cle: v} if v is not None else {c: w for c, w in tout_passe.items() if c != cle}
        ops_nan = [dict(o) for o in bonnes]; ops_nan[3]["net"] = NAN
        peu, _s = ops_synthetiques([900] * 15 + [-300] * 5)
        h_nan = hasard(net_bon, 2000); h_nan["gains_des_tirages"] = [NAN] * 1990 + [net_bon + 5] * 10
        t_c7 = lambda v: J.table_de_la_loi(TABLE_SYNTHETIQUE.format(c7=v, emb="30"))
        t_val = lambda cle, v: J.table_de_la_loi("\n".join(
            l if not l.strip().startswith("| %s |" % cle) else "  | %s | %s | x | x |" % (cle, v)
            for l in TABLE_SYNTHETIQUE.format(c7="condition", emb="30").split("\n")))
        cas2 = lambda cle, v: dict(cas="2", mesures_externes={**tout_passe, **mesures_cas2,
                                                             **({cle: v} if v is not None else {})})
        cas2_sans = lambda cle: dict(cas="2", mesures_externes={c: v for c, v in {**tout_passe, **mesures_cas2}.items()
                                                               if c != cle})
        perturbations = {
            "declaration BLOQUE": dict(declaration_manquants=["lignee"]),
            "declaration INCONNU": dict(declaration_manquants=None),
            "declaration hors contrat": dict(declaration_manquants=""),
            "declaration NaN": dict(declaration_manquants=[NAN]),
            "annees BLOQUE": dict(seances_hors_examen=3),
            "annees INCONNU": dict(seances_hors_examen=None),
            "annees texte": dict(seances_hors_examen="0"),
            "annees négatif": dict(seances_hors_examen=-5),
            "annees booléen": dict(seances_hors_examen=False),
            "annees NaN": dict(seances_hors_examen=NAN),
            "regard BLOQUE": dict(regards_anterieurs=["0123456789abcdef"]),
            "regard INCONNU": dict(regards_anterieurs=None),
            "regard hors contrat 'False'": dict(regards_anterieurs="False"),
            "regard booléen": dict(regards_anterieurs=False),
            "regard NaN": dict(regards_anterieurs=[NAN]),
            "observations BLOQUE (20)": dict(ops=peu, hasard=[hasard(sum(o["net"] for o in peu), 2000)]),
            "ops INCONNU": dict(ops=None),
            "ops hors contrat": dict(ops="x"),
            "ops NaN": dict(ops=ops_nan),
            "gain BLOQUE (k énorme)": dict(k=10 ** 9),
            "k INCONNU": dict(k=None),
            "k booléen": dict(k=True),
            "k NaN": dict(k=NAN),
            "hasard BLOQUE": dict(hasard=[hasard(net_bon, 2000, au_dessus=200)]),
            "hasard INCONNU": dict(hasard=None),
            "hasard dict seul": dict(hasard=hasard(net_bon, 2000)),
            "hasard NaN": dict(hasard=[h_nan]),
            "hasard tout NaN (NaN >= x vaut faux : p minimal)": dict(hasard=[{"n_tirages": 2000,
                                                                              "gains_des_tirages": [NAN] * 2000}]),
            "hasard un mode illisible": dict(hasard=[hasard(net_bon, 2000), {"motif": "x"}]),
            "hasard liste vide": dict(hasard=[]),
            "epoques déclarées absentes": dict(epoques_declarees=None),
            "epoques déclarées vides": dict(epoques_declarees=""),
            "epoques déclarées illisibles": dict(epoques_declarees="2030-01-01 à 2030-06-30"),
            "epoques avec un trou": dict(epoques_declarees="%s..%s ; %s..%s" % (seances[0], seances[_m - 2],
                                                                             seances[_m], seances[-1])),
            "epoques qui débordent": dict(epoques_declarees="%s..%s ; %s..%s" % (seances[0], seances[_m - 1],
                                                                              seances[_m], "2099-12-31")),
            "epoques en dictionnaire (un état venu de l'appelant)": dict(epoques_declarees={"etat": "PASSE"}),
            "annees d'examen absentes": dict(annees_d_examen=None),
            "annees d'examen illisibles": dict(annees_d_examen="toujours"),
            "seances absentes": dict(seances_d_examen=None),
            "seances vides": dict(seances_d_examen=[]),
            "seances mal typées": dict(seances_d_examen=[1, 2, 3]),
            "seances illisibles": dict(seances_d_examen=["hier"] + seances[1:]),
            "epoques : une époque perdante (gains de la 1re moitié retournés)": dict(
                ops=[dict(o, net=-abs(o["net"]) - 100) if o["date_entree"] < seances[_m] else o for o in bonnes]),
            "kelly BLOQUE": dict(mesures_externes=ext("kelly", {"kelly": 0.01, "gain_moyen_net_eur": 1.0})),
            "kelly INCONNU": dict(mesures_externes=ext("kelly", None)),
            "kelly texte": dict(mesures_externes=ext("kelly", {"kelly": "0.2", "gain_moyen_net_eur": 1.0})),
            "kelly NaN": dict(mesures_externes=ext("kelly", {"kelly": NAN, "gain_moyen_net_eur": 1.0})),
            "kelly état PASSE vide (N-A)": dict(mesures_externes=ext("kelly", {"etat": "PASSE"})),
            "voisins BLOQUE": dict(mesures_externes=ext("voisins", {"n_voisins": 26, "n_voisins_gagnants": 25, "ecart_pct": 10.0})),
            "voisins trop peu (10 sur 10)": dict(mesures_externes=ext("voisins", {"n_voisins": 10, "n_voisins_gagnants": 10,
                                                                                 "ecart_pct": 10.0})),
            "voisins mesurés à ±5 % (la table dit ±10 %)": dict(mesures_externes=ext(
                "voisins", {"n_voisins": 26, "n_voisins_gagnants": 26, "ecart_pct": 5.0})),
            "D4 table « 1 voisin à ±10 % », 1 sur 1": dict(table=t_val("voisins", "1 voisins à ±10 %, tous gagnants"),
                                                       mesures_externes=ext("voisins", {"n_voisins": 1,
                                                                                        "n_voisins_gagnants": 1,
                                                                                        "ecart_pct": 10.0})),
            "D4 table « 26 voisins à ±1 % », mesurés à ±1 %": dict(
                table=t_val("voisins", "26 voisins à ±1 %, tous gagnants"),
                mesures_externes=ext("voisins", {"n_voisins": 26, "n_voisins_gagnants": 26, "ecart_pct": 1.0})),
            "frais mesurés × 1 (la table dit × 2)": dict(mesures_externes=ext(
                "frais_doubles", {"gain_moyen_frais_doubles_eur": 300.0, "multiplicateur_des_frais": 1.0})),
            "table « frais × 1 », mesurés × 1": dict(table=t_val("frais_doubles", "courtage et taxe × 1, gain > 0"),
                                                    mesures_externes=ext("frais_doubles", {
                                                        "gain_moyen_frais_doubles_eur": 300.0,
                                                        "multiplicateur_des_frais": 1.0})),
            "ligne frais_doubles illisible": dict(table=t_val("frais_doubles", "doublés")),
            "voisins INCONNU": dict(mesures_externes=ext("voisins", None)),
            "voisins état PASSE vide (N-A)": dict(mesures_externes=ext("voisins", {"etat": "PASSE"})),
            "frais doublés BLOQUE": dict(mesures_externes=ext("frais_doubles", {"gain_moyen_frais_doubles_eur": -1.0,
                                                                                "multiplicateur_des_frais": 2.0})),
            "frais doublés INCONNU": dict(mesures_externes=ext("frais_doubles", None)),
            "frais doublés NaN": dict(mesures_externes=ext("frais_doubles", {"gain_moyen_frais_doubles_eur": NAN,
                                                                             "multiplicateur_des_frais": 2.0})),
            "frais doublés état PASSE vide (N-A)": dict(mesures_externes=ext("frais_doubles", {"etat": "PASSE"})),
            "gain un jeton INCONNU": dict(mesures_externes=ext("gain_un_jeton", None)),
            "creux un jeton INCONNU": dict(mesures_externes=ext("creux_un_jeton", None)),
            "creux un jeton état PASSE vide (N-A)": dict(mesures_externes=ext("creux_un_jeton", {"etat": "PASSE"})),
            "cas ' 1'": dict(cas=" 1"), "cas INCONNU": dict(cas=None), "cas entier": dict(cas=1),
            "point mort BLOQUE (99)": dict(point_mort_pct=99.0),
            "point mort INCONNU": dict(point_mort_pct=None),
            "point mort texte": dict(point_mort_pct="40"),
            "point mort NaN": dict(point_mort_pct=NAN),
            "point mort négatif": dict(point_mort_pct=-1.0),
            "rôle de C7 illisible, C7 BLOQUE": dict(table=t_c7("conditionnel à Q-G3 : affichage en attendant"),
                                                    point_mort_pct=99.0),
            "rôle de C7 « Condition (n°352) »": dict(table=t_c7("Condition (n°352)")),
            "N-D seuil de preuve « 5 ÷ k », k = 69 (0,072 : une probabilité, mais moins stricte)":
                dict(table=t_val("seuil_de_preuve", "5 ÷ k"), k=69, hasard=[hasard(net_bon, 20000)]),
            "N-D seuil de preuve « 1 »": dict(table=t_val("seuil_de_preuve", "1")),
            "N-D seuil du hasard « 1 »": dict(table=t_val("seuil_du_hasard", "1")),
            "seuil du hasard 0,00135 (n°352, retiré) écrit à la table, k = 69 (décision n°42 : 0,05 ÷ 69 = 0,000725)":
                dict(table=t_val("seuil_du_hasard", "0,00135"), k=69, hasard=[hasard(net_bon, 20000)]),
            "N-D kelly_minimum 0,01 (sous 0,05)": dict(table=t_val("kelly_minimum", "0,01")),
            "N-D plancher 29": dict(table=t_val("plancher_observations", "29")),
            "N-D surapprentissage_maximum 0,5 (cas 2)": dict(table=t_val("surapprentissage_maximum", "0,5"),
                                                            **cas2("surapprentissage", None)),
            "seuil du hasard illisible (0,05 / k)": dict(table=t_val("seuil_du_hasard", "0,05 / k")),
            "voisins illisible à la table": dict(table=t_val("voisins", "beaucoup de voisins")),
        }
        for cle in ("surapprentissage", "sharpe_degonfle"):
            perturbations["cas 2, " + cle + " absent"] = cas2_sans(cle)
            perturbations["cas 2, " + cle + " état PASSE vide (N-A)"] = cas2(cle, {"etat": "PASSE"})
        perturbations["cas 2, surapprentissage BLOQUE (0,40)"] = cas2("surapprentissage", {"pbo": 0.40, "nombre_d_essais": 5})
        perturbations["cas 2, Sharpe dégonflé BLOQUE (0,90)"] = cas2("sharpe_degonfle", {"sharpe_degonfle": 0.90, "nombre_d_essais": 5})
        perturbations["cas 2, nombre d'essais 0"] = cas2("surapprentissage", {"pbo": 0.1, "nombre_d_essais": 0})
        perturbations["cas 2, pbo négatif (−0,01)"] = cas2("surapprentissage", {"pbo": -0.01, "nombre_d_essais": 5})
        perturbations["cas 2, Sharpe dégonflé au-dessus de 1"] = cas2("sharpe_degonfle", {"sharpe_degonfle": 1.01,
                                                                                         "nombre_d_essais": 5})
        for cle in ("surapprentissage", "sharpe_degonfle"):
            # D2 : k = 69, une correction qui compte 1 essai
            kw = cas2(cle, dict(mesures_cas2[cle], nombre_d_essais=1))
            kw["mesures_externes"] = {c: (dict(v, nombre_d_essais=69) if c in mesures_cas2 and c != cle else v)
                                      for c, v in kw["mesures_externes"].items()}
            perturbations["D2 cas 2, k = 69, %s compté sur 1 essai" % cle] = dict(kw, k=69,
                                                                                hasard=[hasard(net_bon, 20000)])
        # CHAQUE CHAMP DE CHAQUE MESURE, retiré puis mal typé (champs lus au contrat ou à la proposition de B)
        mesures = {**tout_passe, **mesures_cas2}
        for cle, m in mesures.items():
            base_kw = cas2(cle, None) if cle in mesures_cas2 else {}
            for champ in list(m):
                sans = {c: v for c, v in m.items() if c != champ}
                faux = dict(m, **{champ: "x"})
                for nom, v in (("retiré", sans), ("mal typé", faux), ("NaN", dict(m, **{champ: NAN}))):
                    kw = dict(base_kw) if base_kw else {}
                    kw["mesures_externes"] = {**(kw.get("mesures_externes") or tout_passe), cle: v}
                    perturbations["%s.%s %s" % (cle, champ, nom)] = kw
        temoin = g_base(**cas2("surapprentissage", None))
        ok("G12-0 témoin : en cas 2, toutes les MESURES fournies, la référence est Validée", temoin["verdict"] == VALIDEE,
           "%s / %s" % (temoin["verdict"], temoin["motif"]))
        r = g_base(mesures_externes={c: {"etat": "PASSE"} for c in tout_passe})
        ok("G12-0b témoin INVERSÉ (N-A) : des états « PASSE » sans mesure ne valident JAMAIS",
           r["verdict"] != VALIDEE, "%s / %s" % (r["verdict"], r["motif"]))
        tombes = []
        for nom, kw in perturbations.items():
            try:
                r = g_base(**kw)
                if r["verdict"] == VALIDEE:
                    tombes.append(nom)
            except Exception as ex:
                tombes.append("%s (%s: %s)" % (nom, type(ex).__name__, str(ex)[:60]))
        ok("G12 %d entrées perturbées une à une (BLOQUE / INCONNU / hors contrat / NaN / champ retiré ou mal typé / "
           "seuil moins strict) : aucune « Validée », aucune erreur" % len(perturbations), not tombes,
           "; ".join(tombes)[:400])
    essai("G12", g12)

    def g13():
        # le rôle vient de la loi ou de la table, jamais de l'appelant
        r = g_base(mesures_externes={c: dict(v, role="AFFICHAGE", etat="BLOQUE") for c, v in tout_passe.items()})
        ok("G13 un rôle ou un état écrit par l'appelant est ignoré (mesures ; les époques n'en reçoivent plus)",
           r["controles"]["epoques"]["role"] == "CONDITION" and r["controles"]["voisins"]["role"] == "CONDITION"
           and r["verdict"] == VALIDEE, r["verdict"])
        for cle in J.ROLE_LU_A_LA_TABLE:
            for valeur, attendu in (("condition", "CONDITION"), ("affichage", "AFFICHAGE")):
                lignes = TABLE_SYNTHETIQUE.format(c7="condition", emb="30").split("\n")
                lignes = [l if not l.strip().startswith("| %s |" % cle) else "  | %s | %s | x | x |" % (cle, valeur)
                          for l in lignes]
                r = g_base(table=J.table_de_la_loi("\n".join(lignes)))
                ok("G13 %s : la table dit « %s », la grille rend %s" % (cle, valeur, attendu),
                   r["controles"][cle]["role"] == attendu, r["controles"][cle]["role"])
    essai("G13", g13)

    def g14():
        # LES FRONTIÈRES, générées : pour chaque comparaison de la grille, juste sous / sur / juste au-dessus du seuil.
        # La table des comparaisons couvre chaque CONDITION du contrat qui compare un nombre à un seuil ; la couverture
        # se vérifie depuis CONTROLES_DU_VERDICT (G14-0).
        eps = 1e-9
        tv = lambda cle, v: J.table_de_la_loi("\n".join(
            l if not l.strip().startswith("| %s |" % cle) else "  | %s | %s | x | x |" % (cle, v)
            for l in TABLE_SYNTHETIQUE.format(c7="condition", emb="30").split("\n")))
        from decimal import Decimal
        nombre = lambda x: format(Decimal(x), "f").replace(".", ",")      # exact : la case relue redonne le même flottant
        etat = lambda r, cle: r["controles"][cle]["etat"]
        p_gain = reference["controles"]["gain_bat_zero"]["valeur"]
        h10 = hasard(net_bon, 20000, au_dessus=10)      # p = 11 / 20001, loin de la borne 1 / tirages (DÉL-D38)
        p_hz = g_base(hasard=[h10])["controles"]["bat_le_hasard"]["valeur"]
        c7 = reference["controles"]["taux_face_au_point_mort"]["valeur"]
        n_obs = reference["controles"]["observations_independantes"]["valeur"]
        bb = reference["controles"]["borne_basse_du_gain"]["valeur"]
        # DEUX ÉPOQUES MAÎTRISÉES : 30 opérations dans la première (séances 0 à 89), 30 dans la seconde
        import random as _rnd

        def deux(g1, g2):
            """Opérations en deux époques. ① RÔLE — maîtriser chaque époque. ② CONTEXTE D'APPEL — G14.
            ③ ENTRÉE — les gains de la 1re et de la 2de époque. ④ CONDITIONS D'ENTRÉE — 30 gains au plus dans la 1re.
            ⑤ SORTIE — UNE valeur : les opérations. [rend: 1] ⑥ TRAITEMENT — mêler chaque liste (graine fixe), une
            opération tous les 3 jours. ⑦ UNITÉ — euros. ⑧ POURQUOI — vérité connue. ⑨ CE QUI CLOCHE — —.
            ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]"""
            g1, g2 = list(g1), list(g2)
            _rnd.Random(3).shuffle(g1); _rnd.Random(4).shuffle(g2)
            o1, _s = ops_synthetiques(g1)
            o2, _s = ops_synthetiques(g2, debut=ep_s[90])
            return o1 + o2
        ep_s = seances
        ep_args = dict(epoques_declarees="%s..%s ; %s..%s" % (ep_s[0], ep_s[89], ep_s[90], ep_s[-1]),
                       annees_d_examen="%s..%s" % (ep_s[0], ep_s[-1]), seances_d_examen=ep_s)
        tiede = [900] * 13 + [-800] * 17          # moyenne −63 € : perdante, pas « à coup sûr » (p ≈ 0,3)
        franche = [900] * 20 + [-300] * 10
        ep_une, ep_zero = deux(tiede, franche), deux(tiede, tiede[:29])
        ep_seule = deux(franche, [900])
        frontieres = {
            # clé : [(libellé, arguments de g_base, état attendu)]
            "gain_bat_zero": [
                ("seuil juste au-dessus de p", dict(table=tv("seuil_de_preuve", nombre(p_gain * 1.0001))), "PASSE"),
                ("seuil = p", dict(table=tv("seuil_de_preuve", nombre(p_gain))), "BLOQUE"),
                ("seuil juste sous p", dict(table=tv("seuil_de_preuve", nombre(p_gain * 0.9999))), "BLOQUE"),
            ],
            "bat_le_hasard": [
                ("seuil juste au-dessus de p", dict(table=tv("seuil_du_hasard", nombre(p_hz * 1.0001)), hasard=[h10]), "PASSE"),
                ("seuil = p", dict(table=tv("seuil_du_hasard", nombre(p_hz)), hasard=[h10]), "BLOQUE"),
                ("seuil juste sous p", dict(table=tv("seuil_du_hasard", nombre(p_hz * 0.9999)), hasard=[h10]), "BLOQUE"),
                ("DÉL-D38 : seuil 0,05, 20 tirages : 1/20 = seuil → INCONNU", dict(table=tv("seuil_du_hasard", "0,05"),
                                                                              hasard=[hasard(net_bon, 20)]), "INCONNU"),
                ("DÉL-D38 : seuil 0,05, 21 tirages → mesuré", dict(table=tv("seuil_du_hasard", "0,05"),
                                                                   hasard=[hasard(net_bon, 21)]), "PASSE"),
                ("DÉL-D38 : 1/(n+1) < seuil ≤ 1/n (n = 25, seuil 0,04) → INCONNU", dict(table=tv("seuil_du_hasard", "0,04"),
                                                                                   hasard=[hasard(net_bon, 25)]), "INCONNU"),
            ],
            "taux_face_au_point_mort": [
                ("point mort = borne − 1", dict(point_mort_pct=c7 - 1), "PASSE"),
                ("point mort = borne", dict(point_mort_pct=c7), "BLOQUE"),
                ("point mort = borne + ε", dict(point_mort_pct=c7 + 1e-6), "BLOQUE"),
            ],
            "borne_basse_du_gain": [
                ("borne basse décalée à +1 €", dict(ops=[dict(o, net=o["net"] - bb + 1) for o in bonnes]), "PASSE"),
                ("borne basse décalée à 0 €", dict(ops=[dict(o, net=o["net"] - bb) for o in bonnes]), "BLOQUE"),
                ("borne basse décalée à −1 €", dict(ops=[dict(o, net=o["net"] - bb - 1) for o in bonnes]), "BLOQUE"),
            ],
            "kelly": [
                ("kelly = minimum + ε", dict(mesures_externes={**tout_passe, "kelly": {"kelly": 0.05 + eps, "gain_moyen_net_eur": 1.0}}), "PASSE"),
                ("kelly = minimum", dict(mesures_externes={**tout_passe, "kelly": {"kelly": 0.05, "gain_moyen_net_eur": 1.0}}), "PASSE"),
                ("kelly = minimum − ε", dict(mesures_externes={**tout_passe, "kelly": {"kelly": 0.05 - eps, "gain_moyen_net_eur": 1.0}}), "BLOQUE"),
            ],
            "frais_doubles": [
                ("gain +ε", dict(mesures_externes={**tout_passe, "frais_doubles": {"gain_moyen_frais_doubles_eur": eps, "multiplicateur_des_frais": 2.0}}), "PASSE"),
                ("gain 0", dict(mesures_externes={**tout_passe, "frais_doubles": {"gain_moyen_frais_doubles_eur": 0.0, "multiplicateur_des_frais": 2.0}}), "BLOQUE"),
                ("gain −ε", dict(mesures_externes={**tout_passe, "frais_doubles": {"gain_moyen_frais_doubles_eur": -eps, "multiplicateur_des_frais": 2.0}}), "BLOQUE"),
            ],
            "voisins": [
                ("26 sur 26", dict(mesures_externes={**tout_passe, "voisins": {"n_voisins": 26, "n_voisins_gagnants": 26, "ecart_pct": 10.0}}), "PASSE"),
                ("25 sur 26", dict(mesures_externes={**tout_passe, "voisins": {"n_voisins": 26, "n_voisins_gagnants": 25, "ecart_pct": 10.0}}), "BLOQUE"),
                ("27 sur 27", dict(mesures_externes={**tout_passe, "voisins": {"n_voisins": 27, "n_voisins_gagnants": 27, "ecart_pct": 10.0}}), "BLOQUE"),
            ],
            "annees_d_examen": [("0 séance hors examen", dict(seances_hors_examen=0), "PASSE"),
                                ("1 séance hors examen", dict(seances_hors_examen=1), "BLOQUE")],
            "surapprentissage": [
                ("pbo = maximum − ε", dict(cas="2", mesures_externes={**tout_passe, **mesures_cas2, "surapprentissage": {"pbo": 0.30 - eps, "nombre_d_essais": 5}}), "PASSE"),
                ("pbo = maximum", dict(cas="2", mesures_externes={**tout_passe, **mesures_cas2, "surapprentissage": {"pbo": 0.30, "nombre_d_essais": 5}}), "BLOQUE"),
                ("pbo = maximum + ε", dict(cas="2", mesures_externes={**tout_passe, **mesures_cas2, "surapprentissage": {"pbo": 0.30 + eps, "nombre_d_essais": 5}}), "BLOQUE"),
            ],
            # D3 (M07) : « 1 − 0,95 = 0,050000000000000044 » n'est pas une frontière en flottants ; 0,03125 = 2⁻⁵ et
            # 0,96875 = 1 − 2⁻⁵ sont exacts : 1 − 0,96875 == 0,03125, sans arrondi
            "sharpe_degonfle": [
                ("1 − dsr juste sous le seuil (dsr = nextafter(0,96875, 1))", dict(cas="2", table=tv("seuil_de_preuve", "0,03125 ÷ k"), mesures_externes={**tout_passe, **mesures_cas2, "sharpe_degonfle": {"sharpe_degonfle": math.nextafter(0.96875, 1.0), "nombre_d_essais": 5}}), "PASSE"),
                ("1 − dsr = seuil exactement (0,03125)", dict(cas="2", table=tv("seuil_de_preuve", "0,03125 ÷ k"), mesures_externes={**tout_passe, **mesures_cas2, "sharpe_degonfle": {"sharpe_degonfle": 0.96875, "nombre_d_essais": 5}}), "BLOQUE"),
                ("1 − dsr juste au-dessus du seuil", dict(cas="2", table=tv("seuil_de_preuve", "0,03125 ÷ k"), mesures_externes={**tout_passe, **mesures_cas2, "sharpe_degonfle": {"sharpe_degonfle": math.nextafter(0.96875, 0.0), "nombre_d_essais": 5}}), "BLOQUE"),
                # D2 : nombre d'essais confronté à k (k = 10)
                ("D2 nombre d'essais = k", dict(cas="2", k=10, mesures_externes={**tout_passe, "surapprentissage": {"pbo": 0.1, "nombre_d_essais": 10}, "sharpe_degonfle": {"sharpe_degonfle": 0.999999, "nombre_d_essais": 10}}), "PASSE"),
                ("D2 nombre d'essais = k − 1", dict(cas="2", k=10, mesures_externes={**tout_passe, "surapprentissage": {"pbo": 0.1, "nombre_d_essais": 10}, "sharpe_degonfle": {"sharpe_degonfle": 0.999999, "nombre_d_essais": 9}}), "INCONNU"),
            ],
            "gain_un_jeton": [
                ("gain +ε", dict(mesures_externes={**tout_passe, "gain_un_jeton": {"gain_un_jeton_eur": eps}}), "PASSE"),
                ("gain 0", dict(mesures_externes={**tout_passe, "gain_un_jeton": {"gain_un_jeton_eur": 0.0}}), "BLOQUE"),
                ("gain −ε", dict(mesures_externes={**tout_passe, "gain_un_jeton": {"gain_un_jeton_eur": -eps}}), "BLOQUE"),
            ],
            "creux_un_jeton": [   # aucune limite à la table : mesuré → affiché ; non mesuré → INCONNU
                ("mesuré", dict(), "PASSE"),
                ("non mesuré", dict(mesures_externes={c: v for c, v in tout_passe.items() if c != "creux_un_jeton"}), "INCONNU"),
            ],
            "declaration": [("0 champ manquant", dict(declaration_manquants=[]), "PASSE"),
                            ("1 champ manquant", dict(declaration_manquants=["lignee"]), "BLOQUE")],
            "regard_unique": [("0 regard antérieur", dict(regards_anterieurs=[]), "PASSE"),
                              ("1 regard antérieur", dict(regards_anterieurs=["0123456789abcdef"]), "BLOQUE")],
            "epoques": [
                # le minimum (k = 1, deux moitiés : 1) — une gagnante sur deux le fait, zéro ne le fait pas
                ("1 époque gagnante, minimum 1", dict(ops=ep_une, **ep_args), "PASSE"),
                ("0 époque gagnante, minimum 1", dict(ops=ep_zero, **ep_args), "BLOQUE"),
                # une époque d'une seule opération : non mesurable → INCONNU (relecteur du tour 3, M11)
                ("une époque d'une seule opération", dict(ops=ep_seule, **ep_args), "INCONNU"),
            ],
        }
        frontieres["observations_independantes"] = [
            ("plancher = n_obs", dict(table=tv("plancher_observations", "%d" % n_obs)), "PASSE"),
            ("plancher = n_obs + 1", dict(table=tv("plancher_observations", "%d" % (n_obs + 1))), "BLOQUE"),
        ]
        # PROPRIÉTÉ, PAS ÉNUMÉRATION (D3) : CHAQUE contrôle du contrat a ses frontières, sans exception nommée
        manque = sorted(set(C.CONTROLES_DU_VERDICT) - set(frontieres))
        ok("G14-0 chaque contrôle de CONTROLES_DU_VERDICT a ses frontières (aucune exclusion)", not manque,
           "sans frontière : %s" % manque)
        # la frontière de « perdante à coup sûr » : p de la 1re époque d'ep_une, mesuré, puis seuil = p, p × 1,0001
        p1 = g_base(ops=ep_une, **ep_args)["controles"]["epoques"]["detail"]["epoques"][0]["p_perdante"]
        dit = lambda r: "perdante à coup sûr" in r["controles"]["epoques"]["raison"]
        ok("G14-p p de l'époque tiède mesuré, dans ]0,05 ; 1[ (la référence de strictesse l'admet)", 0.05 < p1 < 1, repr(p1))
        ok("G14-p seuil d'époque = p : pas « perdante à coup sûr » (p < seuil, strictement)",
           not dit(g_base(ops=ep_une, table=tv("epoque_perdante", nombre(p1)), **ep_args)))
        ok("G14-p seuil d'époque = p × 1,0001 : « perdante à coup sûr »",
           dit(g_base(ops=ep_une, table=tv("epoque_perdante", nombre(p1 * 1.0001)), **ep_args)))
        ok("G14-p seuil d'époque = p × 0,9999 : pas « perdante à coup sûr »",
           not dit(g_base(ops=ep_une, table=tv("epoque_perdante", nombre(p1 * 0.9999)), **ep_args)))
        # la frontière de RÉFUTÉE (M03) : la borne haute au niveau p, puis p × 1,0001
        mauvaises, _s = ops_synthetiques([-900] * 40 + [300] * 20)
        rm = g_base(ops=mauvaises)
        p_ref = J.probabilite_epoque_perdante([o["net"] for o in mauvaises],
                                              rm["controles"]["observations_independantes"]["valeur"])["p_perdante"]
        ok("G14-r niveau de réfutation = p : pas RÉFUTÉE (p < niveau, strictement)", 0 < p_ref < 0.05
           and g_base(ops=mauvaises, table=tv("refutation_borne_haute", nombre(p_ref)))["verdict"] != C.MOTS_DU_VERDICT[1],
           repr(p_ref))
        ok("G14-r niveau de réfutation = p × 1,0001 : RÉFUTÉE",
           g_base(ops=mauvaises, table=tv("refutation_borne_haute", nombre(p_ref * 1.0001)))["verdict"]
           == C.MOTS_DU_VERDICT[1])
        faux = []
        for cle, cas_ in frontieres.items():
            for lib, kw, attendu in cas_:
                r = g_base(**kw)
                if etat(r, cle) != attendu:
                    faux.append("%s %s : %s au lieu de %s" % (cle, lib, etat(r, cle), attendu))
        ok("G14 frontières (juste sous / sur / juste au-dessus) de %d comparaisons" % sum(len(v) for v in frontieres.values()),
           not faux, "; ".join(faux)[:500])
    essai("G14", g14)

    def g15():
        # LES CINQ CAS NOMMÉS PAR LE SUPERVISEUR (3e saisine)
        mauvaises, _s = ops_synthetiques([-900] * 40 + [300] * 20)
        r = g_base(ops=mauvaises, regards_anterieurs=["0123456789abcdef"],
                   hasard=[hasard(sum(o["net"] for o in mauvaises), 2000, au_dessus=1500)])
        ok("G15a RÉFUTÉE avec un regard antérieur : pas RÉFUTÉE, motif DONNÉES DE CHOIX",
           r["verdict"] == C.MOTS_DU_VERDICT[2] and r["motif"] == "DONNÉES DE CHOIX", "%s / %s" % (r["verdict"], r["motif"]))
        d = tempfile.mkdtemp(prefix="b_g15_")
        poser_le_registre(d)
        poser_la_portee(d, C, "fiche")
        hyp = {"tp_pct": 4.0, "sl_pct": 2.5, "horizon": 20, "univers": ["AC"], "signal": ["f", "0123"],
               "periode": "2030-01-01..2030-12-31", "bareme": "Fortuneo"}
        try:
            T.preenregistrer(d, "AUTRE", dict(hyp, periode="1999-01-04..2000-01-03"))
            vus, raison = T.regards_sur_les_annees(d, "2000-01-03..2023-12-29", "AUTRE")
            ok("G15b une période qui FINIT sur la première séance d'examen est un regard", len(vus or []) == 1, raison)
            T.preenregistrer(d, "AUTRE2", dict(hyp, periode="1998-01-05..2000-01-02"))
            vus2, _r = T.regards_sur_les_annees(d, "2000-01-03..2023-12-29", "AUTRE2")
            ok("G15c une période qui finit LA VEILLE n'en est pas un", vus2 == [])
        finally:
            shutil.rmtree(d)
    essai("G15", g15)

    def g16():
        # D3 (M05, M06) : LA STRICTESSE À SA FRONTIÈRE, générée depuis les deux tables de références — chaque seuil
        # accepté À la référence et du côté strict, refusé du côté laxiste (écart de 0,1 %, ou d'une unité si entier)
        tv = lambda cle, v: J.table_de_la_loi("\n".join(
            l if not l.strip().startswith("| %s |" % cle) else "  | %s | %s | x | x |" % (cle, v)
            for l in TABLE_SYNTHETIQUE.format(c7="condition", emb="30").split("\n")))
        ecrit = lambda x: ("%.12g" % x).replace(".", ",")
        entiers = {"embargo_sans_duree", "voisins_nombre"}
        lecteurs = {
            "voisins_nombre": lambda x: J._voisins_exiges(tv("voisins", "%s voisins à ±10 %%, tous gagnants" % ecrit(x)))[0],
            "voisins_ecart_pct": lambda x: J._voisins_exiges(tv("voisins", "26 voisins à ±%s %%, tous gagnants" % ecrit(x)))[0],
            "frais_multiplicateur": lambda x: J._frais_exiges(tv("frais_doubles", "courtage et taxe × %s, gain > 0"
                                                                  % ecrit(x)))[0],
        }
        faux, n = [], 0
        for refs in (J.REFERENCES_DE_STRICTESSE, J.REFERENCES_DES_DRAPEAUX):
            for cle, (sens, texte, _src) in refs.items():
                r = float(texte.split("÷")[0].strip().replace(",", "."))
                par_k = "÷" in texte
                pas = (1.0, 1.0) if cle in entiers else (r * 0.001, r * 0.001)
                strict = r - pas[0] if sens == "<=" else r + pas[1]
                laxe = r + pas[0] if sens == "<=" else r - pas[1]
                lire = lecteurs.get(cle) or (lambda x, cle=cle, par_k=par_k: J.seuil_de_la_loi(
                    tv(cle, ecrit(x) + (" ÷ k" if par_k else "")), cle, 69)[0])
                for lib, x, accepte in (("= référence", r, True), ("plus strict", strict, True), ("plus laxiste", laxe, False)):
                    n += 1
                    if (lire(x) is not None) != accepte:
                        faux.append("%s %s (%s) : %s" % (cle, lib, ecrit(x), "refusé" if accepte else "accepté"))
        ok("G16 strictesse à la frontière : %d cas générés depuis les références (numériques et drapeaux)" % n,
           not faux and n == 3 * (len(J.REFERENCES_DE_STRICTESSE) + len(J.REFERENCES_DES_DRAPEAUX)), "; ".join(faux)[:400])
    essai("G16", g16)

    def g17():
        # D1 : les époques se calculent DANS la grille ; aucune entrée ne porte plus leur état
        import inspect
        params = inspect.signature(J.grille_de_validation).parameters
        ok("G17 la grille n'a plus d'entrée « epoques » (un état d'époques ne peut plus venir de l'appelant)",
           "epoques" not in params and {"epoques_declarees", "annees_d_examen", "seances_d_examen"} <= set(params))
        # le minimum se calcule au seuil de preuve DU JUGEMENT : k = 69 → 0,05 ÷ 69 → 2 (deux moitiés), pas 1 (0,05)
        r = g_base(k=69, hasard=[hasard(net_bon, 20000)])
        lu = J.lire_les_epoques(epoques_args["epoques_declarees"], epoques_args["annees_d_examen"], seances)
        attendu = J.minimum_d_epoques_gagnantes(lu["parts_des_seances"], 0.05 / 69, 0.05)["minimum"]
        a_005 = J.minimum_d_epoques_gagnantes(lu["parts_des_seances"], 0.05, 0.05)["minimum"]
        ok("G17b k = 69 : minimum d'époques gagnantes = %r (calculé à 0,05 ÷ 69), pas %r (0,05)" % (attendu, a_005),
           r["controles"]["epoques"]["seuil"] == attendu and attendu != a_005,
           repr(r["controles"]["epoques"]["seuil"]))
        # « gagnante » se calcule : une époque à −5 000 € de moyenne n'est jamais gagnante
        ops = [dict(o, net=-5000.0 - i) if o["date_entree"] < seances[_m] else o for i, o in enumerate(bonnes)]
        r = g_base(ops=ops)
        ep = r["controles"]["epoques"]["detail"]["epoques"]
        ok("G17c une époque à −5 000 € n'est pas gagnante, et le contrôle ne passe pas",
           ep[0]["gagnante"] is False and r["controles"]["epoques"]["etat"] != "PASSE", repr(ep[0]))
    essai("G17", g17)

    def g18():
        # D5 : la borne de Wilson du taux se calcule sur les observations RETENUES, pas sur le nombre d'opérations.
        # Chaque opération doublée aux mêmes dates : 120 opérations, au plus 60 qui ne se recouvrent pas.
        doubles = [dict(o) for o in bonnes for _ in range(2)]
        r = g_base(ops=doubles, hasard=[hasard(2 * net_bon, 2000)])
        n_obs = r["controles"]["observations_independantes"]["valeur"]
        wr = 100.0 * sum(1 for o in doubles if o["net"] > 0) / len(doubles)
        ok("G18 opérations doublées : observations retenues %r < 120 opérations" % n_obs, n_obs is not None and n_obs < 120)
        ok("G18b C7 : borne de Wilson sur %r observations (%.4f), pas sur 120 opérations (%.4f)"
           % (n_obs, J.wilson_bas(n_obs, wr), J.wilson_bas(120, wr)),
           r["controles"]["taux_face_au_point_mort"]["valeur"] == J.wilson_bas(n_obs, wr)
           and J.wilson_bas(n_obs, wr) < J.wilson_bas(120, wr), repr(r["controles"]["taux_face_au_point_mort"]))
    essai("G18", g18)


    # ── LE REGISTRE DES ESSAIS ──
    hyp = {"tp_pct": 4.0, "sl_pct": 2.5, "horizon": 20, "univers": ["AC", "AI"], "signal": ["f", "0123"],
           "periode": ["2030-01-01", "2030-12-31"], "bareme": "Fortuneo"}

    def r1():
        # Depuis la mission REGARD (12-11-2026), le registre vit sur la branche des regards : une entrée ne s'y efface
        # pas (l'union des ajouts reste lue), d'où UNE racine par défaut fabriqué.
        d = tempfile.mkdtemp(prefix="b_r1_")
        poser_le_registre(d)
        try:
            ok("R0 registre absent : 0 essai", T.nombre_d_essais(d) == (0, ""))
            p = T.preenregistrer(d, "SYN", hyp)
            T.preenregistrer(d, "SYN", dict(hyp))
            ok("R1 la même hypothèse deux fois : 1 essai", T.nombre_d_essais(d) == (1, ""), repr(T.nombre_d_essais(d)))
            T.preenregistrer(d, "SYN", dict(hyp, horizon=COMMUN.HORIZON_AUCUNE))
            ok("R1b « aucune » et « 20 » : 2 essais", T.nombre_d_essais(d) == (2, ""))
            lus, _df = T.lire_le_registre(d)
            ecrits = [lus[n] for n in sorted(lus)]
            ok("R1c « aucune » s'écrit par le mot en JSON",
               any(e.get("hypothese", {}).get("horizon") == COMMUN.MOT_DE_L_HORIZON_AUCUNE for e in ecrits))
            T.preenregistrer(d, "AUTRE", dict(hyp, tp_pct=5.0))
            ok("R1d compte par fiche : SYN 2, AUTRE 1",
               T.nombre_d_essais(d, fiche_id="SYN") == (2, "") and T.nombre_d_essais(d, fiche_id="AUTRE") == (1, ""))
            T.inscrire_le_resultat(d, p, {"n": 3})
            ok("R2 un résultat ne compte pas comme un essai", T.nombre_d_essais(d) == (3, ""))
            try:
                T.inscrire_le_resultat(d, "0000000000000000", {"n": 1})
                ok("R2b résultat sans préenregistrement refusé", False)
            except FileNotFoundError:
                ok("R2b résultat sans préenregistrement refusé", True)
            # création exclusive : la même entrée deux fois ne s'écrase pas
            try:
                T._ecrire(d, dict(ecrits[0]), "NATURES_DES_ENTREES_D_ESSAI")
                ok("R4 création exclusive : écrire deux fois la même entrée", False, "écrasée sans erreur")
            except FileExistsError:
                ok("R4 création exclusive : écrire deux fois la même entrée", True)
        finally:
            shutil.rmtree(d)
        import hashlib
        # une entrée orpheline poussée à la main se voit
        d = tempfile.mkdtemp(prefix="b_r2c_")
        poser_le_registre(d)
        try:
            T.preenregistrer(d, "SYN", hyp)
            orph = {"nature": "RESULTAT", "horodatage_paris": "x", "alea": "00000000",
                    "preenregistrement": "ffffffffffffffff", "resultat": None, "echec": "E: x"}
            octets = (json.dumps(orph, sort_keys=True, indent=1) + "\n").encode()
            T._pousser_l_entree(d, hashlib.sha256(octets).hexdigest()[:16], octets)
            n, raison = T.nombre_d_essais(d)
            ok("R2c résultat orphelin : registre abîmé, compte INCONNU", n == "INCONNU" and "préenregistrement" in raison,
               raison)
        finally:
            shutil.rmtree(d)
        # une entrée retouchée se voit : sous son nom (« altérée ») ou par un commit qui la remplace (« modifiée »)
        d = tempfile.mkdtemp(prefix="b_r3_")
        poser_le_registre(d)
        try:
            p = T.preenregistrer(d, "SYN", hyp)
            sommet, _r = T._sommet_distant(d)
            t0 = T._octets_de_la_branche(d, sommet)[0][p + ".json"]
            retoucher_sur_la_branche(d, T, p, t0.replace(b'"alea": "', b'"alea": "9', 1))
            n, raison = T.nombre_d_essais(d)
            ok("R3 entrée retouchée par un commit poussé : compte INCONNU (« modifiée »)",
               n == "INCONNU" and "modifiée" in raison, raison)
        finally:
            shutil.rmtree(d)
        d = tempfile.mkdtemp(prefix="b_r3b_")
        poser_le_registre(d)
        try:
            p = T.preenregistrer(d, "SYN", hyp)
            sommet, _r = T._sommet_distant(d)
            t0 = T._octets_de_la_branche(d, sommet)[0][p + ".json"]
            T._pousser_l_entree(d, "0123456789abcdef", t0.replace(b'"alea": "', b'"alea": "9', 1))
            n, raison = T.nombre_d_essais(d)
            ok("R3b entrée poussée sous un nom qui n'est pas l'empreinte de ses octets : compte INCONNU (« altérée »)",
               n == "INCONNU" and "altérée" in raison, raison)
        finally:
            shutil.rmtree(d)
    essai("R1", r1)

    def depot_jetable():
        """Un dépôt git jetable sur la branche « main ». ① RÔLE — éprouver l'ordre de l'histoire.
        ② CONTEXTE D'APPEL — les cas R et D. ③ ENTRÉE — —. ④ CONDITIONS D'ENTRÉE — git.
        ⑤ SORTIE — DEUX valeurs : le dossier et la fonction g(*args, date=None) qui lance git. [rend: 2]
        ⑥ TRAITEMENT — init sur « main », identité fixe. ⑦ UNITÉ — —. ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —.
        ⑩ EFFET — crée un dossier. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        d = tempfile.mkdtemp(prefix="b_git_")
        poser_le_registre(d)
        env = dict(os.environ, GIT_AUTHOR_NAME="b", GIT_AUTHOR_EMAIL="b@x", GIT_COMMITTER_NAME="b",
                   GIT_COMMITTER_EMAIL="b@x")
        g0 = lambda *a, date=None: subprocess.run(["git", "-C", d] + list(a), capture_output=True, check=True,
                                                  env=dict(env, **({"GIT_COMMITTER_DATE": date,
                                                                    "GIT_AUTHOR_DATE": date} if date else {})))

        def g(*a, date=None):
            """Lance git ; après un commit sur « main », la branche principale du contrat la suit (REGARD tour 3).
            ① RÔLE — l'ancre d'un regard est la branche principale qu'il voit. ② CONTEXTE D'APPEL — R5, R8, D4.
            ③ ENTRÉE — arguments, date. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : le processus. [rend: 1]
            ⑥ TRAITEMENT — lancer ; si commit sur main, `update-ref refs/remotes/origin/main HEAD`. ⑦ UNITÉ — —.
            ⑧ POURQUOI — sans dépôt distant de main, la référence est posée à la main. ⑨ CE QUI CLOCHE — —.
            ⑩ EFFET — git écrit. ⑪ TERMINAISON — Rend la main ; lève. [sort: non]"""
            r = g0(*a, date=date)
            if a[:1] == ("commit",) and g0("symbolic-ref", "--short", "HEAD").stdout.strip() == b"main":
                g0("update-ref", "refs/remotes/origin/main", "HEAD")
            return r
        g("init", "-q", "-b", "main")
        return d, g

    def r5():
        d, g = depot_jetable()
        try:
            # LE REGISTRE RECOPIÉ SUR LA BRANCHE PRINCIPALE PAR L'ÉPREUVE (`au_disque`) : le code qui le lit à un commit est
            # gardé tel quel ; en production, plus rien ne l'y écrit (mission REGARD, conséquence déclarée).
            T.preenregistrer(d, "SYN", hyp); au_disque(d, T)
            g("add", "-A"); g("commit", "-qm", "a", date="2030-01-10T12:00:00+01:00")
            c1 = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
            T.preenregistrer(d, "SYN", dict(hyp, tp_pct=6.0)); au_disque(d, T)
            # commit AJOUTÉ APRÈS, mais daté AVANT (un rebase ou un amend change les dates) : l'ordre fait foi
            g("add", "-A"); g("commit", "-qm", "b", date="2029-06-01T12:00:00+01:00")
            T.preenregistrer(d, "SYN", dict(hyp, tp_pct=7.0))   # poussé sur la branche des regards, jamais commité ici
            ok("R5 compte au premier commit : 1 essai (le second, antidaté, vient après dans l'histoire)",
               T.nombre_d_essais(d, c1, branche="main") == (1, ""), repr(T.nombre_d_essais(d, c1, branche="main")))
            ok("R5b compte au sommet : 2 (l'essai non commité n'y est pas)",
               T.nombre_d_essais(d, "main", branche="main") == (2, ""))
            ok("R5c compte sans date : la branche des regards, 3", T.nombre_d_essais(d) == (3, ""))
            g("checkout", "-q", "-b", "cote"); g("commit", "-q", "--allow-empty", "-m", "hors branche")
            cote = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
            g("checkout", "-q", "main")
            ok("R5d un commit qui n'est pas sur la branche principale : INCONNU",
               T.nombre_d_essais(d, cote, branche="main")[0] == "INCONNU")
            # un effacement commis rougit
            f = subprocess.run(["git", "-C", d, "ls-files", "registre_essais"], capture_output=True,
                               text=True).stdout.split()[0]
            g("rm", "-q", f); g("commit", "-qm", "menage")
            n, raison = T.nombre_d_essais(d, c1, branche="main")
            ok("R5e une entrée effacée puis commitée : compte INCONNU, même à un commit d'avant",
               n == "INCONNU" and "effacée" in raison, raison)
        finally:
            shutil.rmtree(d)
    essai("R5", r5)

    def r6():
        d = tempfile.mkdtemp(prefix="b_r6_")
        poser_le_registre(d)
        try:
            p = T.preenregistrer(d, "SYN", hyp)
            T.inscrire_le_resultat(d, p, {"n": 1})
            T.inscrire_le_resultat(d, p, {"n": 2})
            n, raison = T.nombre_d_essais(d)
            ok("R6 deux résultats pour un même essai : registre abîmé, INCONNU", n == "INCONNU" and "résultats" in raison,
               raison)
        finally:
            shutil.rmtree(d)
        d = tempfile.mkdtemp(prefix="b_r7_")
        poser_le_registre(d)
        try:
            import hashlib
            p = T.preenregistrer(d, "SYN", hyp)
            e = json.loads(json.dumps(T.lire_le_registre(d)[0][p]))
            e["hypothese"]["tp_pct"] = 9.0          # l'hypothèse change, l'empreinte écrite non ; le nom est RECALCULÉ
            octets = (json.dumps(e, sort_keys=True, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
            T._pousser_l_entree(d, hashlib.sha256(octets).hexdigest()[:16], octets)
            n, raison = T.nombre_d_essais(d)
            ok("R7 hypothèse retouchée, nom recalculé : l'empreinte d'hypothèse recalculée le voit",
               n == "INCONNU" and "empreinte d'hypothèse" in raison, raison)
        finally:
            shutil.rmtree(d)
        d, g = depot_jetable()
        cl = tempfile.mkdtemp(prefix="b_r8_")
        try:
            T.preenregistrer(d, "SYN", hyp); au_disque(d, T); g("add", "-A"); g("commit", "-qm", "a")
            T.preenregistrer(d, "SYN", dict(hyp, tp_pct=5.0)); au_disque(d, T); g("add", "-A"); g("commit", "-qm", "b")
            subprocess.run(["git", "clone", "-q", "--depth", "1", "file://" + d, cl + "/c"], capture_output=True, check=True)
            n, raison = T.nombre_d_essais(cl + "/c", "HEAD", branche="HEAD")
            ok("R8 clone superficiel : INCONNU", n == "INCONNU" and "superficiel" in raison, raison)
        finally:
            shutil.rmtree(d); shutil.rmtree(cl)
    essai("R6", r6)

    def r9():
        d = tempfile.mkdtemp(prefix="b_r9_")
        poser_le_registre(d)
        poser_la_portee(d, C, "fiche")
        examen = "2000-01-03..2023-12-29"
        try:
            T.preenregistrer(d, "SYN", dict(hyp, periode=["2024-01-02", "2026-10-30"]))
            b = T.preenregistrer(d, "SYN", dict(hyp, periode="2010-01-04..2012-12-31"))
            vus, r = T.regards_sur_les_annees(d, examen, "SYN")
            ok("R9 regards de SYN sur 2000-2023 : la seule entrée 2010-2012 (2024-2026 n'en est pas)", vus == [b],
               repr((vus, r)))
            c = T.preenregistrer(d, "C5-essai3", dict(hyp, periode="2001-01-02..2005-12-30", tp_pct=5.0))
            vus, r = T.regards_sur_les_annees(d, examen, "SYN")
            ok("R9b portée « fiche » (RÉGLAGE lu, lot B2 ; la lignée s'éprouve dans l'épreuve de B2) : l'essai d'une "
               "AUTRE fiche sans lien (« C5-essai3 ») n'est pas un regard de SYN", vus == [b], repr((vus, r)))
            ok("R9b2 ... et c'est un regard de « C5-essai3 »", T.regards_sur_les_annees(d, examen, "C5-essai3")[0] == [c])
            ok("R9c le jugement lui-même s'exclut par « sauf »",
               T.regards_sur_les_annees(d, examen, "SYN", sauf=(b,))[0] == [])
            T.preenregistrer(d, "AUTRE", dict(hyp, periode="n'importe quoi"))
            ok("R9d2 la période illisible d'une AUTRE fiche ne rend pas SYN inconnue",
               T.regards_sur_les_annees(d, examen, "SYN")[0] == [b])
            T.preenregistrer(d, "SYN", dict(hyp, periode="n'importe quoi"))
            vus, r = T.regards_sur_les_annees(d, examen, "SYN")
            ok("R9d une période illisible de la fiche : INCONNU (on ne sait pas si elle a regardé)", vus is None, r)
            ok("R9e années d'examen illisibles : INCONNU", T.regards_sur_les_annees(d, "x", "SYN")[0] is None)
            ok("R9f fiche non nommée (« » ou None) : INCONNU, et la raison dit « non nommée » (pas « inconnue »)",
               all(T.regards_sur_les_annees(d, examen, x)[0] is None
                   and "non nommée" in T.regards_sur_les_annees(d, examen, x)[1] for x in ("", None)))
        finally:
            shutil.rmtree(d)
    essai("R9", r9)

    # ── LA DÉCLARATION DATÉE ──
    def ligne_complete(fiche="SYN", date="2030-01-05T10:00+01:00"):
        """Une déclaration complète synthétique. ① RÔLE — un cas. ② CONTEXTE D'APPEL — les cas D. ③ ENTRÉE — fiche,
        date. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : le dictionnaire. [rend: 1] ⑥ TRAITEMENT — remplir
        chaque champ du contrat. ⑦ UNITÉ — —. ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main. [sort: non]"""
        l = {c: "valeur de l'épreuve" for c in C.DECLARATION_DATEE}
        l.update(fiche_id=fiche, date_declaration=date, cas="1", reglages='{"tp": 0.04, "horizon": "aucune"}',
                 regard_sans_decision="", parametres_libres="2", date_regle_univers="2029-12-01", lignee="aucune")
        # parametres_libres et date_regle_univers : contrôlés depuis la mission B3 (defauts_par_champ) ;
        # lignee « aucune » : une lignée LISIBLE (lue par B2 depuis le 11-11-2026) — fusion J des deux intentions
        return l

    def d1():
        with open(os.path.join(racine, C.DECLARATIONS_DATEES), encoding="utf-8-sig") as f:
            entete = next(csv.reader(f))
        ok("D1 vraie ligne : l'en-tête du fichier du dépôt est le contrat DECLARATION_DATEE", entete == C.DECLARATION_DATEE)
        ok("D1b une ligne complète n'a aucun défaut", D.defauts_d_une_declaration(ligne_complete()) == [],
           repr(D.defauts_d_une_declaration(ligne_complete())))
        sans = ligne_complete(); sans["lignee"] = "  "
        ok("D1c une lignée vide est un défaut", any("lignee" in x for x in D.defauts_d_une_declaration(sans)))
    essai("D1", d1)

    def d2():
        d = tempfile.mkdtemp(prefix="b_d2_")
        poser_le_registre(d)
        try:
            os.makedirs(os.path.join(d, "donnees"), exist_ok=True)
            shutil.copy(os.path.join(racine, C.DECLARATIONS_DATEES), os.path.join(d, C.DECLARATIONS_DATEES))
            avant = open(os.path.join(d, C.DECLARATIONS_DATEES), "rb").read()
            n = D.ajouter_une_declaration(d, ligne_complete())
            D.ajouter_une_declaration(d, ligne_complete("AUTRE", "2030-01-06T10:00+01:00"))
            apres = open(os.path.join(d, C.DECLARATIONS_DATEES), "rb").read()
            ok("D2 ajout seul : l'ancien fichier est un préfixe exact, deux lignes de plus",
               apres.startswith(avant) and apres.count(b"\n") == avant.count(b"\n") + 2 and n == 2, "ligne %r" % n)
            l = C.declaration_de_la_fiche(d, "SYN", "2030-02-01T00:00+01:00")
            ok("D2b la lecture du contrat retrouve la déclaration", l is not None and l["cas"] == "1")
            mauvaise = ligne_complete(); mauvaise["hypothese"] = ""
            try:
                D.ajouter_une_declaration(d, mauvaise)
                ok("D3 incomplète : refusée", False)
            except ValueError:
                ok("D3 incomplète : refusée, fichier inchangé",
                   open(os.path.join(d, C.DECLARATIONS_DATEES), "rb").read() == apres)
        finally:
            shutil.rmtree(d)
    essai("D2", d2)

    def d4():
        d, g = depot_jetable()
        try:
            examen = "2000-01-03..2023-12-29"
            os.makedirs(os.path.join(d, "donnees"), exist_ok=True)
            shutil.copy(os.path.join(racine, C.DECLARATIONS_DATEES), os.path.join(d, C.DECLARATIONS_DATEES))
            # la portée du regard, lue par B2 : le VRAI réglage du dépôt (« lignee » au 11-11-2026)
            shutil.copy(os.path.join(racine, T.REGLAGES), os.path.join(d, T.REGLAGES))
            reg = os.path.join(d, T.REGLAGES)     # son dépôt commun : son dépôt nu local (mission REGARD, tour 2)
            texte = "".join(l for l in open(reg, encoding="utf-8").read().splitlines(True)
                            if not l.startswith("depot_des_regards,"))
            open(reg, "w", encoding="utf-8").write(texte + "depot_des_regards,%s,épreuve,épreuve\n"
                                                   % os.path.join(d, ".depot_nu"))
            g("add", "-A"); g("commit", "-qm", "entete", date="2030-01-01T12:00:00+01:00")
            # BONNE : déclarée, commitée, PUIS regardée
            D.ajouter_une_declaration(d, ligne_complete("BONNE", "2030-01-05T10:00+01:00"))
            g("add", "-A"); g("commit", "-qm", "decl bonne", date="2030-01-05T10:00:00+01:00")
            T.preenregistrer(d, "BONNE", dict(hyp, periode="2001-01-02..2005-12-30"))
            g("add", "-A"); g("commit", "-q", "--allow-empty", "-m", "regard bonne", date="2030-01-06T10:00:00+01:00")
            # ENTRE : regardée, déclarée, regardée encore (superviseur : « premier_regard min → max »)
            T.preenregistrer(d, "ENTRE", dict(hyp, periode="2002-01-02..2003-12-30"))
            g("add", "-A"); g("commit", "-q", "--allow-empty", "-m", "regard 1 entre", date="2030-01-06T12:00:00+01:00")
            D.ajouter_une_declaration(d, ligne_complete("ENTRE", "2030-01-07T10:00+01:00"))
            g("add", "-A"); g("commit", "-qm", "decl entre", date="2030-01-07T10:00:00+01:00")
            T.preenregistrer(d, "ENTRE", dict(hyp, periode="2004-01-02..2005-12-30"))
            g("add", "-A"); g("commit", "-q", "--allow-empty", "-m", "regard 2 entre", date="2030-01-08T10:00:00+01:00")
            # TARDIVE : regardée PUIS déclarée, dans un commit daté AVANT le regard (rebase, amend)
            T.preenregistrer(d, "TARDIVE", dict(hyp, periode="2001-01-02..2005-12-30"))
            g("add", "-A"); g("commit", "-q", "--allow-empty", "-m", "regard tardive", date="2030-01-10T10:00:00+01:00")
            D.ajouter_une_declaration(d, ligne_complete("TARDIVE", "2030-01-04T10:00+01:00"))
            g("add", "-A"); g("commit", "-qm", "decl tardive", date="2030-01-02T10:00:00+01:00")
            # MEME : déclaration et regard dans le MÊME commit
            T.preenregistrer(d, "MEME", dict(hyp, periode="2001-01-02..2005-12-30"))
            D.ajouter_une_declaration(d, ligne_complete("MEME", "2030-01-11T10:00+01:00"))
            g("add", "-A"); g("commit", "-qm", "les deux")
            # NEUVE : déclarée et commitée APRÈS les regards d'AUTRES fiches, jamais regardée elle-même
            D.ajouter_une_declaration(d, ligne_complete("NEUVE", "2030-01-12T10:00+01:00"))
            g("add", "-A"); g("commit", "-qm", "decl neuve")
            l, r = D.declaration_engagee(d, "BONNE", examen)
            ok("D4 déclarée, commitée, puis regardée : engagée", l is not None and l["fiche_id"] == "BONNE", r)
            l, r = D.declaration_engagee(d, "TARDIVE", examen)
            ok("D4b regardée puis déclarée, commit antidaté : NON engagée (l'ordre fait foi, pas la date)", l is None, r)
            l, r = D.declaration_engagee(d, "MEME", examen)
            ok("D4c déclarée dans le commit même du premier regard : NON engagée", l is None, r)
            l, r = D.declaration_engagee(d, "NEUVE", examen)
            ok("D4d HORS LIGNÉE : déclarée après les regards d'AUTRES fiches sans lien (lignées « aucune »), jamais "
               "regardée : engagée",
               l is not None and l["fiche_id"] == "NEUVE", r)
            l, r = D.declaration_engagee(d, "ENTRE", examen)
            ok("D4g déclarée entre le premier et le second regard : NON engagée (le PREMIER regard fait l'ancre)",
               l is None, r)
            l, r = D.declaration_engagee(d, "NEUVE", "2026-01-02..2026-06-30")
            ok("D4h sans aucun regard sur SES années d'examen, déclarée sur la branche : engagée", l is not None, r)
            D.ajouter_une_declaration(d, ligne_complete("DISQUE", "2030-01-13T10:00+01:00"))
            l, r = D.declaration_engagee(d, "DISQUE", examen)
            ok("D4e écrite sur le disque, pas commitée : NON engagée", l is None, r)
            # un effacement de déclaration APRÈS le regard ne change pas l'ancre
            chemin = os.path.join(d, C.DECLARATIONS_DATEES)
            lignes = open(chemin, encoding="utf-8").read().split("\n")
            open(chemin, "w", encoding="utf-8").write("\n".join(lignes[:1] + lignes[2:]))
            g("add", "-A"); g("commit", "-qm", "effacement")
            l, r = D.declaration_engagee(d, "BONNE", examen)
            ok("D4f une déclaration effacée APRÈS le regard : la ligne d'avant le regard fait toujours foi (ancre du "
               "regard, décision « Reparer » du 12-11-2026)", l is not None and l["fiche_id"] == "BONNE", r)
        finally:
            shutil.rmtree(d)
    essai("D4", d4)

    def d5():
        fiches = C.lire_les_fiches(racine)
        f = fiches["C5E10-QA-V1"]
        j, s = D.empreintes_du_code(racine, f["module_signal"])
        ok("D5 vraie fiche C5E10-QA-V1 : deux empreintes de 16 caractères",
           len(j) == 16 and len(s) == 16 and all(c in "0123456789abcdef" for c in j + s), "%s %s" % (j, s))
        d = tempfile.mkdtemp(prefix="b_d5_")
        try:
            os.makedirs(os.path.join(d, "programmes"))
            shutil.copy(os.path.join(racine, "emp.py"), os.path.join(d, "emp.py"))
            src = open(os.path.join(racine, "programmes/JUGE_DES_STRATEGIES.py"), encoding="utf-8").read()
            os.makedirs(os.path.dirname(os.path.join(d, f["module_signal"])), exist_ok=True)
            shutil.copy(os.path.join(racine, f["module_signal"]), os.path.join(d, f["module_signal"]))
            open(os.path.join(d, "programmes/JUGE_DES_STRATEGIES.py"), "w", encoding="utf-8").write(
                src.replace('"""', '"""Texte ajouté. ', 1))
            j2, _s = D.empreintes_du_code(d, f["module_signal"])
            open(os.path.join(d, "programmes/JUGE_DES_STRATEGIES.py"), "w", encoding="utf-8").write(src + "\nX_B = 1\n")
            j3, _s = D.empreintes_du_code(d, f["module_signal"])
            ok("D5b un texte changé ne change pas l'empreinte ; du code changé la change", j2 == j and j3 != j)
        finally:
            shutil.rmtree(d)
    essai("D5", d5)

    # ── V1 : DE VRAIS COURS (2024-2026, années déjà vues — aucun regard) ──
    def v1():
        JU = charger(os.path.join(racine, "programmes/JUGE_DES_STRATEGIES.py"), "JUGE_DES_STRATEGIES")
        P = charger(os.path.join(racine, "programmes/MODULE_POSITIONS.py"), "MODULE_POSITIONS")
        mnemo = JU.table_mnemoniques(JU.trouver(racine, "REFERENTIEL_VALEURS"))
        lu = JU.charger_cours(os.path.join(racine, "donnees/cours_maitre.csv"))
        cours = {}
        for m in ("AC", "AI", "AIR", "CS"):
            cle = mnemo.get(m, JU.cle_valeur(m))
            cours[cle] = [b for b in lu.get(cle, []) if "2024-01-02" <= b["date"] <= "2026-10-30"]
        sig = JU.SignalNomme(lambda s: [{"i": k} for k in range(0, len(s) - 1, 15)], {}, "épreuve B, V1")
        fiche = {"id": "B-V1", "tp": "4%", "sl": "2.5%", "horizon": "20", "univers": "AC, AI, AIR, CS",
                 "entree": "DÉFAUT", "donnees_demandees": "cours", "periode": "2024-01-02..2026-10-30"}
        ops, _ = JU.jouer(fiche, cours, mnemo, sig, P)
        t = J.table_de_la_loi(open(os.path.join(racine, "gouvernance/REGISTRE_REGLES.md"), encoding="utf-8").read())
        pm = J.point_mort_des_operations(0.04, 0.025, ops, P)
        r = J.grille_de_validation(t, "1", 69, ops=ops, point_mort_pct=pm, declaration_manquants=[],
                                   seances_hors_examen=0, regards_anterieurs=[])
        ok("V1 vrais cours, signal périodique (%d opérations) : verdict au contrat, jamais Validée sans hasard" % len(ops),
           len(ops) > 30 and r["verdict"] in C.MOTS_DU_VERDICT and r["verdict"] != VALIDEE
           and list(r["controles"]) == list(C.CONTROLES_DU_VERDICT),
           "%s / %s / obs %s / p_gain %s" % (r["verdict"], r["motif"], r["controles"]["observations_independantes"]["valeur"],
                                             r["controles"]["gain_bat_zero"]["valeur"]))
    essai("V1", v1)
    return res


def preparer(racine, sab):
    """Copie les programmes du bloc et leurs voisins, et applique un sabotage.
    ① RÔLE — Donner à chaque sabotage sa copie. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — la racine, le nom ou « Z0 ».
    ④ CONDITIONS D'ENTRÉE — chaque texte visé est présent UNE fois. ⑤ SORTIE — UNE valeur : le dossier. [rend: 1]
    ⑥ TRAITEMENT — copier, remplacer. ⑦ UNITÉ — —. ⑧ POURQUOI — une cible introuvable ne sabote rien : elle lève.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — crée un dossier temporaire. ⑪ TERMINAISON — rend la main ou lève LookupError.
    [sort: non]"""
    d = tempfile.mkdtemp(prefix="b5a_%s_" % sab)
    os.makedirs(os.path.join(d, "programmes"))
    for f in (GRILLE, ESSAIS, DECL) + VOISINS:
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
    ① RÔLE — Isoler chaque copie dans son processus (les modules ont les mêmes noms). ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — racine, sabotage. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : liste de (nom, vert, détail).
    [rend: 1] ⑥ TRAITEMENT — préparer, relancer (borné à 600 s), lire le JSON, effacer la copie. ⑦ UNITÉ — —.
    ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — dossiers temporaires. ⑪ TERMINAISON — rend la main ; un
    dépassement rend un cas rouge. [sort: non]"""
    d = preparer(racine, sab)
    try:
        r = subprocess.run([sys.executable, "-B", ICI, "--cas", d, racine], capture_output=True, text=True, timeout=600)
        try:
            return [tuple(x) for x in json.loads(r.stdout.strip().splitlines()[-1])]
        except (ValueError, IndexError):
            return [("relance", False, (r.stderr or r.stdout)[-400:])]
    except subprocess.TimeoutExpired:
        return [("relance", False, "plus de 600 s")]
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
    for f in ("gouvernance/REGISTRE_REGLES.md", "donnees/DECLARATIONS_DATEES.csv", "donnees/cours_maitre.csv", "emp.py"):
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
