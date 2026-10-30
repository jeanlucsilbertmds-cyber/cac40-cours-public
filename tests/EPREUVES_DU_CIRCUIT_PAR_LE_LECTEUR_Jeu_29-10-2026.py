#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVES DU CIRCUIT PAR LE LECTEUR — Jeu 29-10-2026 (Paris) — épreuves de l'étape 7 de A-577.

Simulation uniquement — aucun ordre réel.

① RÔLE — Prouver que les deux pas du circuit du soir qui touchent aux cours — le détecteur
  (`programmes/DETECTER_LES_SIGNAUX_GITHUB.py`) et le teneur de positions (`programmes/TENIR_LES_POSITIONS.py`) — lisent
  les cours comme le juge des stratégies (`programmes/JUGE_DES_STRATEGIES.py`, `lire_par_le_lecteur`) depuis l'étape 7
  de A-577, et que chaque protection a des dents : ① un signal n'est donné que pour une valeur dans le CAC 40 le jour du
  signal ; ② il se calcule sur le morceau de série sans trou qui finit à la séance ; ③ le teneur prend ses séances au
  calendrier officiel et n'achète que dans le CAC 40 le jour de l'achat ; ④ une lecture qui met des lignes à part
  arrête les deux pas sans rien écrire.
② CONTEXTE D APPEL — Depuis la racine, la racine en argument : par le certificateur (`programmes/CERTIFIER_LA_VERSION.py`)
  et à la main, avant toute livraison qui touche la lecture des cours du circuit du soir. Avec `--saboter`, chaque
  sabotage doit faire rougir au moins une épreuve ; `--saboter=D1,P2` ne joue que les sabotages nommés.
③ ENTRÉE — `sys.argv[1]` : la racine du dépôt ; `--saboter` ou `--saboter=<noms séparés par des virgules>`, facultatif.
④ CONDITIONS D ENTRÉE — Sous la racine : les trois programmes, le lecteur unique et ce qu'il lit, le module de positions,
  le module de signal C5-ETENDU-10, le registre des stratégies avec C5E10-QA-V1, le référentiel des valeurs, et le
  fichier maître `donnees/cours_maitre.csv` portant au moins les séances du 2024-01-02 au 2026-10-28. Sinon des épreuves
  rougissent.
⑤ SORTIE — UNE valeur : le code de sortie, 0 si Z0 est vert et, avec `--saboter`, si chaque sabotage joué rougit ; 1
  sinon. [rend: 1] Une ligne « == » par jeu, une ligne « <nom> mord : [...] » par sabotage qui mord, puis le détail.
⑥ TRAITEMENT — Pour Z0 puis chaque sabotage : copier la racine sans ses gros dossiers de sources, appliquer le sabotage,
  lancer CODE dans un sous-processus depuis la copie, compter les rouges. Les cas de CODE :
  C1 Eiffage, signal du 04-11-2025 (vraie ligne du maître) : REFUSÉ, Eiffage n'entre dans le CAC 40 que le 22-12-2025 ;
     aucune valeur dite « sans séance ».
  C2 Eiffage, signal du 30-04-2026 : DONNÉ, avec les chiffres de la lecture d'avant la bascule (CMF 0,069936, CCI −97,01,
     relevés le 29-10-2026 sur le code d'avant) et la clôture de la vraie ligne du maître.
  C3 un trou dans Bouygues le 15-10-2026 : le signal du 22-10-2026 se calcule sur le morceau qui commence le 16-10, et
     n'est pas donné ; sans le trou, il l'est, avec la clôture de la vraie ligne.
  C4 le détecteur lancé en entier sur le maître coupé au 22-10-2026 : signal Bouygues ; même maître troué : aucun.
  C5 le détecteur lancé en entier sur le maître coupé au 20-10-2026, Eiffage entrée dans l'indice le 21-10-2026 dans la
     copie (au lieu du 22-12-2025) : son vrai signal du 20-10 est refusé, dit au fichier et à l'écran ; avec les vrais
     passages, il est donné. (Le maître ne peut pas être coupé au 04-11-2025 : le calibrage du détecteur exige le
     signal connu d'Unibail du 20-08-2026.)
  C6 une ligne à la date illisible dans le maître : le détecteur sort en code 2 et n'écrit pas le fichier des signaux.
  T1 le teneur lancé en entier, maître coupé au 27-10-2026 : la position en attente sur le signal Bouygues du 22-10-2026
     s'ouvre le 23-10 à l'ouverture de la vraie ligne du maître.
  T2 même cas, la séance du 23-10-2026 retirée pour TOUTES les valeurs : la position ne saute pas au 26-10 ; elle attend
     le 23-10, et un incident le dit.
  T3 le calendrier du teneur avec la lecture : porte le 23-10 manquant aux cours, finit à la dernière date des cours.
  T4 Eiffage, signal du 04-11-2025 : avec la lecture, l'achat du 05-11 est refusé et la position retirée ; sans lecture,
     elle s'ouvre à l'ouverture de la vraie ligne du 05-11-2025.
  T5 Eiffage, signal du 20-10-2026 : acheté le 21-10 à l'ouverture de la vraie ligne ; avec une sortie de l'indice le
     20-10 (passages modifiés), refusé.
  T6 une lecture sans le juge : `entrer` lève.
  T7 une ligne à la date illisible : le teneur sort en code 2 et laisse les positions intactes.
  Depuis le 29-10-2026 (superviseur R-759, réparations jugées DE FOND) :
  C7 VINCI privée de sa séance du 20-10-2026 (cas réel du relecteur) : le détecteur la dit « ◌ » et la compte, code 0.
  T8 Eiffage sortie de l'indice le jour de son signal du 20-10-2026 (passages modifiés dans la copie) : le teneur
     retire la position et le dit par « ⛔ », code 0 (règle provisoire, BACKLOG A-638).
  V0 le versement (`programmes/TENIR_L_HISTORIQUE.py`) d'une séance déjà au maître : code 0.
  Depuis le 30-10-2026 (versement partiel, décision de Jean-Luc à 13h55 : « fais le traitement sans aucune concession
  sur la qualité ») — le maître de la veille privé de la séance du 28-10, l'incrément du soir l'apporte :
  V1 plus une barre VINCI au 01-05-2026, Bourse fermée (cas réel du relecteur) : VINCI mise à part et nommée, les lignes
     du 28-10 versées, code 3, alerte `rapports/ALERTE_LIGNES_MISES_A_PART.md`.
  V2 le tri appelé directement : un jour fermé et une date illisible mis à part, la vraie ligne gardée (le critère est
     le compte du lecteur, pas une liste de sortes).
  V3 ACCOR du 28-10 à la clôture ×100 : mise à part par `juger_la_ligne`, les autres versées, code 3.
  V4 la même ligne quand le 28-10 est déjà au maître : refus en bloc, code 1, maître intact.
  V5 le lecteur en échec (nature des trous illisible) : code 1, maître intact, alerte qui dit ce qui lève le refus,
     sans trace Python.
  V6 la ligne fausse de V3 deux fois dans l'incrément : séance en double, refus en bloc, code 1.
  V7 V1 en `--verifier` : code 3, maître intact, aucune alerte. (V1 vérifie aussi le compte des lignes versées écrit
     dans l'alerte.) La relecture finale du maître complété après mise à part n'a pas de cas : aucun couple de lignes
     neuves saines seules mais refusées ensemble n'a été construit ; elle échoue fermée (code 1, rien d'écrit).
⑦ UNITÉ — Des codes de sortie ; dans les cas, des dates AAAA-MM-JJ, des euros par titre, des indicateurs sans unité.
⑧ POURQUOI — Décision de Jean-Luc du 26-10-2026 à 19h43 (« Mais n'oublie pas de le basculer plus tard, sinon on va se
  casser les dents [...] il faut que ce soit fait rapidement ») : deux lectures des mêmes cours divergent toujours
  (R-708). Un jeu d'épreuves se sabote contre sa propre correction : une épreuve qui reste verte quand on retire ce
  qu'elle teste n'est pas une preuve (R-731). Les cas réels (R-732) viennent du maître et du rejeu des 722 séances fait
  le 29-10-2026 (107 signaux avant la bascule ; après : 96 donnés à l'identique, 11 refusés hors de l'indice — 9 Eiffage,
  2 Bureau Veritas).
⑨ CE QUI CLOCHE — Aucun trou réel n'existe dans le maître : les trous sont fabriqués en retirant de vraies lignes. ·
  La sortie de l'indice le jour du signal (T5) est fabriquée : aucune valeur du maître ne sort de l'indice sur sa
  période. · Les dates du maître sont écrites ici : si le maître perdait ces séances, les cas rougiraient (et le diraient).
  · Le lecteur attend les cours jusqu'à la veille (heure de Paris) : au-delà du 31-12-2026, tant que le calendrier
  d'Euronext de 2027 n'est pas relevé, tout rougit, comme le circuit.
⑩ EFFET — Des copies temporaires de la racine, effacées à la fin. N'écrit rien sous la racine.
⑪ TERMINAISON — Chaque sous-processus est borné à 900 secondes ; chacun lance le détecteur et le teneur au plus quatre
  fois chacun, bornés à 300 secondes.
  [sort: oui]
"""
import os, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
DET = "programmes/DETECTER_LES_SIGNAUX_GITHUB.py"
POS = "programmes/TENIR_LES_POSITIONS.py"
BAN = "programmes/JUGE_DES_STRATEGIES.py"
VER = "programmes/TENIR_L_HISTORIQUE.py"
# Les gros dossiers de sources que ni le détecteur ni le teneur ne lisent (le lecteur lit le maître) : hors de la copie.
SANS = ("sources_yahoo", "sources_bnains", "sources_francfort")
SABOTAGES = {
    "Z0": [],
    "D1_le_detecteur_ne_coupe_plus_aux_trous": [(DET, '    serie = B.couper_aux_trous(serie, lecture["trous"].get(cle, []))[-1]\n', "")],
    "D2_le_detecteur_ignore_l_indice": [(DET, 'dedans = B.dans_l_indice(lecture["passages"].get(B.cle_valeur(v), []), seance)', "dedans = True")],
    "D3_le_detecteur_lit_par_charger_cours": [(DET, "        cours, lecture = B.lire_par_le_lecteur(racine, os.path.relpath(fichiers[0], racine), mnemo)",
                                               '        cours, lecture = B.charger_cours(*fichiers), {"passages": {}, "trous": {}, "composition": True, "seances": []}')],
    "D4_la_detection_n_est_plus_bornee_a_la_seance": [(DET, "        serie, sig = signaux_sur(cours, lecture, B, mod, v, seance)",
                                                       "        serie, sig = signaux_sur(cours, lecture, B, mod, v)")],
    "D5_le_juge_ignore_les_lignes_mises_a_part": [(BAN, "    if a_part:\n", "    if False:\n")],
    "J1_les_seances_tirees_des_cours": [(BAN, '    seances = [iso(d) for d, _ in lecteur.CAL.seances_entre(min(lues), max(lues), c["seances"])] if lues else []',
                                         "    seances = sorted({iso(d) for d in lues})")],
    "J2_les_seances_au_dela_des_cours": [(BAN, 'lecteur.CAL.seances_entre(min(lues), max(lues), c["seances"])',
                                          'lecteur.CAL.seances_entre(min(lues), c["fin"], c["seances"])')],
    "P1_le_calendrier_ignore_la_lecture": [(POS, '    if lecture is not None:\n        return list(lecture["seances"])',
                                            '    if False:\n        return list(lecture["seances"])')],
    "P2_l_achat_hors_de_l_indice_admis": [(POS, "        if lecture is not None:\n            _j = next(", "        if False:\n            _j = next(")],
    "P3_tenir_pour_de_vrai_ne_passe_pas_la_lecture": [(POS, "    r = tenir(positions, cours, signaux, prochaine, mod, base=base, lecture=lecture, juge=juge)",
                                                       "    r = tenir(positions, cours, signaux, prochaine, mod, base=base)")],
    "P4_le_teneur_lit_par_charger_cours_du_banc": [(POS, "        cours, lecture, juge = lire_les_cours_du_soir(base)",
                                                    "        cours, lecture, juge = charger_cours_du_banc(base, *_fichiers_de_cours(base)), None, None")],
    "P5_tenir_ne_passe_pas_la_lecture_a_entrer": [(POS, "                              reglages, lecture, juge)", "                              reglages)")],
    "P6_une_lecture_sans_juge_acceptee": [(POS, "    if lecture is not None and juge is None:", "    if False:")],
    "P7_la_position_refusee_gardee": [(POS, "    return [p for p in positions if id(p) not in retirees], incidents", "    return positions, incidents")],
    # H1, D6, P8 (29-10-2026, superviseur R-759 : réparations jugées DE FOND)
    # H1 recalé le 30-10-2026 : la relecture vit dans `_relecture`, le seul appel du lecteur par le versement.
    "H1_le_versement_ne_fait_plus_relire_le_maitre": [(VER, '        return L.lignes_mises_a_part(c), c, ""\n', '        return 0, c, ""\n')],
    # H3 à H8, X1, X6 (30-10-2026, versement partiel décidé par Jean-Luc à 13h55 ; relecteur du 30-10-2026, I1)
    "H3_le_tri_enumere_le_jour_ferme": [(VER, "        if n > n0:\n", '        if c.get("hors_seance"):\n')],
    "H4_rien_n_est_verse_quand_une_ligne_tombe": [(VER, "    partiel = not par_increment and not neuf\n", "    partiel = False\n")],
    "H5_le_code_3_devient_0": [(VER, "        sys.exit(3)\n    sys.exit(0)", "        sys.exit(0)\n    sys.exit(0)")],
    "H6_l_alerte_des_lignes_tue": [(VER, "        ecrire_l_alerte_des_lignes_a_part(a_part, ajouts)\n", "")],
    "H7_le_juge_des_lignes_ne_met_plus_a_part": [(VER, "        if motifs and partiel and k not in cles_de_la_veille and k not in vues:\n", "        if False:\n")],
    "H8_une_ligne_deja_au_maitre_mise_a_part": [(VER, "        if motifs and partiel and k not in cles_de_la_veille and k not in vues:\n",
                                                  "        if motifs and partiel and k not in vues:\n")],
    "X1_l_echec_du_lecteur_non_rattrape": [(VER, "        except (ValueError, OSError) as e:\n            return None, {}", "        except OSError as e:\n            return None, {}")],
    "X6_l_echec_du_lecteur_rend_zero": [(VER, '            return None, {}, f"{type(e).__name__} : {e}"\n', '            return 0, {}, ""\n')],
    # H9 à H11 (relecteur du 30-10-2026, tour 3, M1 : R3, R4, R1)
    "H9_le_double_d_une_ligne_a_part_pardonne": [(VER, "        if motifs and partiel and k not in cles_de_la_veille and k not in vues:\n",
                                                   "        if motifs and partiel and k not in cles_de_la_veille:\n")],
    "H10_verifier_rend_zero": [(VER, "        sys.exit(3 if a_part else 0)\n", "        sys.exit(0)\n")],
    "H11_le_compte_des_ajouts_non_corrige": [(VER, "            ajouts -= len(ecartees)\n", "")],
    "D6_les_valeurs_aveugles_tues": [(DET, '    aveugles = [x for x in detail if x["cmf"] is None or x["cci"] is None]',
                                      "    aveugles = []")],
    "P8_le_retrait_tu_a_l_ecran": [(POS, '        if i.startswith("ACHAT REFUSE"):', "        if False:")],
}
CODE = r'''
import sys, os, csv, json, subprocess, copy
sys.path.insert(0, "programmes")
import JUGE_DES_STRATEGIES as B, TENIR_LES_POSITIONS as T, DETECTER_LES_SIGNAUX_GITHUB as D
rouges = []
def dire(nom, ok, det=""):
    if not ok:
        rouges.append(nom + " · " + str(det)[:300])
MAITRE = "donnees/cours_maitre.csv"
ORIGINAL = open(MAITRE, encoding="utf-8").read().splitlines()
ENTETE, LIGNES = ORIGINAL[0], ORIGINAL[1:]
col = ENTETE.split(",")
def vraie(v, d):
    """La vraie ligne du maître d'origine, en dictionnaire (None si absente)."""
    for l in LIGNES:
        x = dict(zip(col, l.split(",")))
        if x["valeur"] == v and x["date"] == d:
            return x
    return None
def ecrire_maitre(garder):
    with open(MAITRE, "w", encoding="utf-8") as f:
        f.write("\n".join([ENTETE] + [l for l in LIGNES if garder(dict(zip(col, l.split(","))))]) + "\n")
def lancer(prog):
    try:
        p = subprocess.run([sys.executable, "-B", prog, "."], capture_output=True, text=True, timeout=300)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return 124, "délai dépassé"
def un(nom, f):
    try:
        f()
    except Exception as e:
        dire(nom, False, "%s : %s" % (type(e).__name__, e))

# ── sur le maître d'origine, au niveau des fonctions
Bd, mod, cours, lec = D.charger(".")
def c1():
    dj, rf, ss, det = D.signaux_de_la_seance(cours, lec, Bd, mod, "2025-11-04")
    e = next((x for x in det if x["valeur"] == "EIFFAGE"), {})
    ok = ("EIFFAGE" in [x["valeur"] for x in rf] and "EIFFAGE" not in [x["valeur"] for x in dj] and ss == []
          and e.get("dans_l_indice") is False and e.get("signal_hors_de_l_indice") is True and vraie("EIFFAGE", "2025-11-04"))
    dire("C1 Eiffage 04-11-2025 : signal refusé hors du CAC 40, aucune valeur sans séance", ok,
         ([x["valeur"] for x in dj], [x["valeur"] for x in rf], ss, e))
def c2():
    dj, rf, ss, det = D.signaux_de_la_seance(cours, lec, Bd, mod, "2026-04-30")
    e = next((x for x in dj if x["valeur"] == "EIFFAGE"), None)
    l = vraie("EIFFAGE", "2026-04-30")
    ok = e is not None and (e["cmf"], e["cci"]) == (0.069936, -97.01) and l and e["close"] == float(l["close"]) and not rf
    dire("C2 Eiffage 30-04-2026 : signal donné, chiffres d'avant la bascule, clôture de la vraie ligne", ok, (e, l and l["close"], rf))
def c3():
    dj, rf, ss, det = D.signaux_de_la_seance(cours, lec, Bd, mod, "2026-10-22")
    e = next((x for x in dj if x["valeur"] == "BOUYGUES"), None)
    l = vraie("BOUYGUES", "2026-10-22")
    dire("C3a Bouygues 22-10-2026 sans trou : signal donné, clôture de la vraie ligne", e is not None and l and e["close"] == float(l["close"]), (e, l))
    with open("_troue.csv", "w", encoding="utf-8") as f:
        f.write("\n".join([ENTETE] + [x for x in LIGNES if x.split(",")[1] <= "2026-10-22"
                                      and not x.startswith("BOUYGUES,2026-10-15,")]) + "\n")
    mn = Bd.table_mnemoniques(Bd.trouver(".", "REFERENTIEL_VALEURS"))
    ct, lt = Bd.lire_par_le_lecteur(".", "_troue.csv", mn)
    s, sig = D.signaux_sur(ct, lt, Bd, mod, "BOUYGUES", "2026-10-22")
    dj2, rf2, ss2, det2 = D.signaux_de_la_seance(ct, lt, Bd, mod, "2026-10-22")
    ok = s[0]["date"] == "2026-10-16" and "BOUYGUES" not in [x["valeur"] for x in dj2 + rf2] and "2026-10-15" in lt["trous"]["BOUYGUES"]
    dire("C3b trou de Bouygues le 15-10-2026 : calcul sur le morceau du 16-10, pas de signal le 22-10", ok,
         (s[0]["date"], [x["valeur"] for x in dj2]))
un("C1", c1); un("C2", c2); un("C3", c3)

mod_p = T.charger_module_positions(T.trouver_module("."))
reg = T.reglages_du_registre(".")
cp, lp, J = T.lire_les_cours_du_soir(".")
def pos(v, dsig, strat="C5E10-QA-V1"):
    return {"strategie": strat, "valeur": v, "date_signal": dsig, "date_entree": "", "prix_entree": T.INCONNU,
            "tp": T.INCONNU, "sl": T.INCONNU, "horizon_fin": T.INCONNU, "statut": T.EN_ATTENTE,
            "comptabilite": T.UN_JETON, "regles_pre_trade": "", "explication": "", "frais_non_chiffrables": ""}
def t4():
    r, inc = T.entrer([pos("EIFFAGE", "2025-11-04")], cp, mod_p, 20, None, reg, lp, J)
    dire("T4a Eiffage, signal du 04-11-2025 : achat du 05-11 refusé, position retirée, incident dit", r == [] and
         any("ACHAT REFUSE" in x and "EIFFAGE" in x for x in inc), (r, inc))
    r0, inc0 = T.entrer([pos("EIFFAGE", "2025-11-04")], cp, mod_p, 20, None, reg)
    l = vraie("EIFFAGE", "2025-11-05")
    dire("T4b sans lecture : ouverte le 05-11-2025 à l'ouverture de la vraie ligne", len(r0) == 1 and r0[0]["statut"] == T.OUVERTE
         and l and float(r0[0]["prix_entree"]) == float(l["open"]), (r0, l))
def t5():
    r, inc = T.entrer([pos("EIFFAGE", "2026-10-20")], cp, mod_p, 20, None, reg, lp, J)
    l = vraie("EIFFAGE", "2026-10-21")
    dire("T5a Eiffage, signal du 20-10-2026 : acheté le 21-10 à l'ouverture de la vraie ligne", len(r) == 1 and
         r[0]["statut"] == T.OUVERTE and r[0]["date_entree"] == "2026-10-21" and l and float(r[0]["prix_entree"]) == float(l["open"]), (r, l))
    ls = dict(lp, passages=dict(lp["passages"], EIFFAGE=[("2025-12-22", "2026-10-20")]))
    r2, inc2 = T.entrer([pos("EIFFAGE", "2026-10-20")], cp, mod_p, 20, None, reg, ls, J)
    dire("T5b sortie de l'indice le jour du signal : achat du lendemain refusé", r2 == [] and any("ACHAT REFUSE" in x for x in inc2), (r2, inc2))
def t6():
    try:
        T.entrer([pos("EIFFAGE", "2026-10-20")], cp, mod_p, 20, None, reg, lp, None)
        dire("T6 une lecture sans le juge : entrer lève", False, "entrer n'a pas levé")
    except ValueError:
        pass
un("T4", t4); un("T5", t5); un("T6", t6)

# ── le circuit lancé en entier, sur des maîtres coupés, troués ou abîmés
SIG = "donnees/signaux_du_jour.json"
FPOS = "donnees/claude_positions_ouvertes.csv"
def c4():
    ecrire_maitre(lambda x: x["date"] <= "2026-10-22")
    code, out = lancer("programmes/DETECTER_LES_SIGNAUX_GITHUB.py")
    s = json.load(open(SIG, encoding="utf-8")) if code == 0 else {}
    dire("C4a détecteur, maître coupé au 22-10-2026 : signal Bouygues", code == 0 and s.get("seance") == "2026-10-22"
         and "BOUYGUES" in [x["valeur"] for x in s.get("signaux", [])], (code, out[-300:]))
    ecrire_maitre(lambda x: x["date"] <= "2026-10-22" and not (x["valeur"] == "BOUYGUES" and x["date"] == "2026-10-15"))
    code, out = lancer("programmes/DETECTER_LES_SIGNAUX_GITHUB.py")
    s = json.load(open(SIG, encoding="utf-8")) if code == 0 else {}
    dire("C4b détecteur, même maître troué le 15-10 : aucun signal Bouygues", code == 0 and s.get("seance") == "2026-10-22"
         and "BOUYGUES" not in [x["valeur"] for x in s.get("signaux", [])], (code, out[-300:]))
PASSAGES = "donnees/sources_indice/PASSAGES_DANS_LE_CAC40.csv"
def c5():
    # Le détecteur calcule sur la DERNIÈRE séance et se calibre sur Unibail au 20-08-2026 : le maître ne peut pas être
    # coupé au 04-11-2025. On garde le vrai signal d'Eiffage du 20-10-2026 (maître coupé au 20-10) et on fait entrer
    # Eiffage dans l'indice le 21-10-2026 au lieu du 22-12-2025, dans la copie seulement.
    vrai = open(PASSAGES, encoding="utf-8").read()
    assert vrai.count("FR0000130452,Eiffage,2025-12-22,") == 1
    try:
        open(PASSAGES, "w", encoding="utf-8").write(vrai.replace("FR0000130452,Eiffage,2025-12-22,", "FR0000130452,Eiffage,2026-10-21,"))
        ecrire_maitre(lambda x: x["date"] <= "2026-10-20")
        code, out = lancer("programmes/DETECTER_LES_SIGNAUX_GITHUB.py")
        s = json.load(open(SIG, encoding="utf-8")) if code == 0 else {}
        e = next((x for x in s.get("detail_indicateurs", []) if x["valeur"] == "EIFFAGE"), {})
        dire("C5a détecteur, Eiffage entrée le 21-10 : son signal du 20-10-2026 refusé, dit au fichier et à l'écran",
             code == 0 and s.get("seance") == "2026-10-20" and "EIFFAGE" not in [x["valeur"] for x in s.get("signaux", [])]
             and e.get("signal_hors_de_l_indice") is True and "EIFFAGE · signal REFUSÉ" in out, (code, e, out[-300:]))
    finally:
        open(PASSAGES, "w", encoding="utf-8").write(vrai)
    code, out = lancer("programmes/DETECTER_LES_SIGNAUX_GITHUB.py")
    s = json.load(open(SIG, encoding="utf-8")) if code == 0 else {}
    dire("C5b mêmes cours, vrais passages : le signal d'Eiffage du 20-10-2026 est donné", code == 0
         and "EIFFAGE" in [x["valeur"] for x in s.get("signaux", [])], (code, out[-300:]))
def c6():
    ecrire_maitre(lambda x: True)
    with open(MAITRE, "a", encoding="utf-8") as f:
        f.write("VINCI,26/10/2026,1,1,1,1,1,abc\n")
    if os.path.exists(SIG):
        os.remove(SIG)
    code, out = lancer("programmes/DETECTER_LES_SIGNAUX_GITHUB.py")
    dire("C6 une ligne à part : détecteur en code 2, aucun fichier de signaux", code == 2 and not os.path.exists(SIG)
         and "LECTURE DES COURS REFUS" in out, (code, out[-300:]))
def poser(positions, seance):
    T._ecrire_csv(FPOS, positions, T.POSITION)
    json.dump({"seance": seance, "signaux": [], "valeurs_sans_cette_seance": []}, open(SIG, "w", encoding="utf-8"))
def t1():
    ecrire_maitre(lambda x: x["date"] <= "2026-10-27")
    poser([pos("BOUYGUES", "2026-10-22")], "2026-10-27")
    code, out = lancer("programmes/TENIR_LES_POSITIONS.py")
    p = T._lire_csv(FPOS)
    l = vraie("BOUYGUES", "2026-10-23")
    dire("T1 teneur, vraie ligne : Bouygues achetée le 23-10-2026 à l'ouverture du maître", code == 0 and len(p) == 1
         and p[0]["statut"] == T.OUVERTE and p[0]["date_entree"] == "2026-10-23" and l
         and float(p[0]["prix_entree"]) == float(l["open"]), (code, p, out[-300:]))
def t2():
    ecrire_maitre(lambda x: x["date"] <= "2026-10-27" and x["date"] != "2026-10-23")
    poser([pos("BOUYGUES", "2026-10-22")], "2026-10-27")
    code, out = lancer("programmes/TENIR_LES_POSITIONS.py")
    p = T._lire_csv(FPOS)
    dire("T2 la séance du 23-10 manque à toutes les valeurs : l'achat ne saute pas au 26-10, il attend le 23-10 et le dit",
         code == 0 and len(p) == 1 and p[0]["statut"] == T.EN_ATTENTE and p[0]["date_entree"] == "2026-10-23"
         and "seance d'entree 2026-10-23 absente des cours de BOUYGUES" in out, (code, p, out[-300:]))
    c, l, _ = T.lire_les_cours_du_soir(".")
    cal = T.calendrier(c, l)
    dire("T3 le calendrier du teneur : porte le 23-10 manquant aux cours, finit à la dernière date des cours",
         "2026-10-23" in cal and cal[-1] == "2026-10-27" and "2026-10-23" not in T.calendrier(c), (cal[-4:],))
def t7():
    ecrire_maitre(lambda x: True)
    with open(MAITRE, "a", encoding="utf-8") as f:
        f.write("VINCI,26/10/2026,1,1,1,1,1,abc\n")
    poser([pos("BOUYGUES", "2026-10-22")], "2026-10-28")
    avant = open(FPOS, "rb").read()
    code, out = lancer("programmes/TENIR_LES_POSITIONS.py")
    dire("T7 une ligne à part : teneur en code 2, positions intactes", code == 2 and open(FPOS, "rb").read() == avant
         and "LECTURE DES COURS REFUSEE" in out, (code, out[-300:]))
def c7():
    # VINCI privée du 20-10-2026 (cas réel du relecteur du 29-10-2026, I2) : 6 séances sans trou au 28-10, aucun CMF.
    ecrire_maitre(lambda x: not (x["valeur"] == "VINCI" and x["date"] == "2026-10-20"))
    code, out = lancer("programmes/DETECTER_LES_SIGNAUX_GITHUB.py")
    dire("C7 VINCI privée du 20-10-2026 : dite « ◌ » et comptée, code 0", code == 0 and "◌ VINCI" in out
         and "depuis le 2026-10-21" in out and "1 valeur(s) sans calcul possible" in out, (code, out[-400:]))
def t8():
    # Eiffage sortie de l'indice le jour même de son signal du 20-10-2026 (passages modifiés dans la copie) : le teneur
    # retire la position et le dit par « ⛔ », code 0 (règle provisoire, BACKLOG A-638).
    vrai = open(PASSAGES, encoding="utf-8").read()
    assert vrai.count("FR0000130452,Eiffage,2025-12-22,,") == 1
    try:
        open(PASSAGES, "w", encoding="utf-8").write(vrai.replace("FR0000130452,Eiffage,2025-12-22,,", "FR0000130452,Eiffage,2025-12-22,2026-10-20,"))
        ecrire_maitre(lambda x: x["date"] <= "2026-10-27")
        poser([pos("EIFFAGE", "2026-10-20")], "2026-10-27")
        code, out = lancer("programmes/TENIR_LES_POSITIONS.py")
        p = T._lire_csv(FPOS)
        dire("T8 achat hors du CAC 40 : position retirée et dite « ⛔ », code 0", code == 0 and p == []
             and "⛔ ACHAT REFUSE" in out and "EIFFAGE" in out, (code, p, out[-400:]))
    finally:
        open(PASSAGES, "w", encoding="utf-8").write(vrai)
def v1():
    # Une barre VINCI au 01-05-2026, Bourse fermée (cas réel du relecteur du 29-10-2026, I1) : avant, versée en code 0,
    # puis le détecteur et le teneur s'arrêtaient chaque soir. Depuis le 30-10-2026, le versement la met à part et verse
    # le reste (V1 à V5 ci-dessous) ; V0 d'abord : une séance déjà au maître se verse en code 0.
    ecrire_maitre(lambda x: True)
    subprocess.run("git init -q . && git add donnees/cours_maitre.csv && git -c user.name=e -c user.email=e@e -c commit.gpgsign=false "
                   "commit -qm maitre", shell=True, check=True, capture_output=True)
    inc = "donnees/claude_cours_nouveaux.csv"
    entete7 = "valeur,date,open,high,low,close,volume"
    du_28 = [",".join(x.split(",")[:7]) for x in LIGNES if x.split(",")[1] == "2026-10-28"]
    open(inc, "w", encoding="utf-8").write("\n".join([entete7] + du_28) + "\n")
    code0, out0 = lancer(VER_P)
    dire("V0 versement propre (séance du 28-10 déjà au maître) : code 0", code0 == 0, (code0, out0[-300:]))
    # LE VERSEMENT PARTIEL (décision de Jean-Luc du 30-10-2026 à 13h55) : le maître de la veille n'a pas la séance du
    # 28-10, l'incrément du soir l'apporte, plus des lignes fausses. Les lignes NEUVES fausses sont mises à part et
    # nommées, les autres versées, code 3 ; une ligne fausse DÉJÀ au maître, ou un lecteur en échec, refuse tout.
    ALP, ALM = "rapports/ALERTE_LIGNES_MISES_A_PART.md", "rapports/ALERTE_FICHIER_MAITRE.md"
    def veille_sans_le_28():
        ecrire_maitre(lambda x: x["date"] != "2026-10-28")
        subprocess.run("git add donnees/cours_maitre.csv && git -c user.name=e -c user.email=e@e -c commit.gpgsign=false "
                       "commit -q --allow-empty -m veille", shell=True, check=True, capture_output=True)
        for f in (ALP, ALM):
            if os.path.exists(f):
                os.remove(f)
    def au_maitre(v, d):
        return any(l.split(",")[0] == v and l.split(",")[1] == d for l in open(MAITRE, encoding="utf-8").read().splitlines())
    def du_28_au_maitre():
        return sum(1 for l in open(MAITRE, encoding="utf-8").read().splitlines() if l.split(",")[1] == "2026-10-28")
    vinci_28 = next(x for x in du_28 if x.startswith("VINCI,"))
    # V1 — cas réel du relecteur du 29-10-2026 : une barre VINCI au 01-05-2026, Bourse fermée, que `juger_la_ligne`
    # admet et que le lecteur commun met à part.
    veille_sans_le_28()
    open(inc, "w", encoding="utf-8").write("\n".join([entete7] + du_28 + [vinci_28.replace("2026-10-28", "2026-05-01")]) + "\n")
    code, out = lancer(VER_P)
    alp = open(ALP, encoding="utf-8").read() if os.path.exists(ALP) else ""
    dire("V1 VINCI au 01-05-2026 (Bourse fermée) mise à part, les %d lignes du 28-10 versées, code 3, alerte qui la nomme"
         % len(du_28), code == 3 and du_28_au_maitre() == len(du_28) and not au_maitre("VINCI", "2026-05-01")
         and "MISE À PART : VINCI · séance du 01-05-2026" in out and "**VINCI**, séance du 01-05-2026" in alp
         and "jour sans séance" in alp and not os.path.exists(ALM)
         and ("a versé les %d autre(s)" % len(du_28)) in alp, (code, du_28_au_maitre(), out[-400:], alp[:300]))
    # V7 — le même cas en `--verifier` : code 3, rien d'écrit, aucune alerte (relecteur du 30-10-2026, tour 3, R4).
    veille_sans_le_28()
    avant = open(MAITRE, "rb").read()
    p = subprocess.run([sys.executable, "-B", VER_P, ".", "--verifier"], capture_output=True, text=True, timeout=300)
    dire("V7 --verifier : code 3, maître intact, aucune alerte", p.returncode == 3 and open(MAITRE, "rb").read() == avant
         and not os.path.exists(ALP) and "1 mise(s) à part" in p.stdout, (p.returncode, p.stdout[-300:]))
    # V2 — même cas, deux sortes que le lecteur met à part (jour fermé, date illisible) : la règle est le COMPTE du
    # lecteur, pas une liste de sortes (relecteur du 30-10-2026, I1, H3). Appel direct du tri.
    import TENIR_L_HISTORIQUE as VT
    base = [dict(zip(col, l.split(","))) for l in LIGNES if l.split(",")[1] != "2026-10-28"]
    v28 = dict(zip(col, next(l for l in LIGNES if l.startswith("VINCI,2026-10-28,")).split(",")))
    tries, err = VT.trier_les_lignes_neuves(base, [dict(v28, date="2026-05-01"), dict(v28, date="2026-02-30"), v28])
    dire("V2 tri direct : le jour fermé et la date illisible mis à part, la vraie ligne du 28-10 gardée",
         err == "" and [x["date"] for x, _ in tries] == ["2026-05-01", "2026-02-30"]
         and "date illisible" in tries[1][1], (err, [(x["date"], m) for x, m in tries]))
    # V3 — une ligne neuve refusée par `juger_la_ligne` (clôture d'ACCOR du 28-10 ×100) : mise à part, les autres versées.
    veille_sans_le_28()
    faux = [x if not x.startswith("ACCOR,") else ",".join(x.split(",")[:5] + [str(float(x.split(",")[5]) * 100)] + x.split(",")[6:7])
            for x in du_28]
    open(inc, "w", encoding="utf-8").write("\n".join([entete7] + faux) + "\n")
    code, out = lancer(VER_P)
    dire("V3 ACCOR du 28-10 à la clôture ×100 mise à part par le juge des lignes, %d lignes versées, code 3"
         % (len(du_28) - 1), code == 3 and du_28_au_maitre() == len(du_28) - 1 and not au_maitre("ACCOR", "2026-10-28")
         and "MISE À PART : ACCOR · séance du 28-10-2026" in out and os.path.exists(ALP), (code, du_28_au_maitre(), out[-400:]))
    # V6 — la même ligne fausse DEUX FOIS dans l'incrément : séance en double, refus en bloc (relecteur du 30-10-2026,
    # tour 3, R3).
    veille_sans_le_28()
    open(inc, "w", encoding="utf-8").write("\n".join([entete7] + faux + [x for x in faux if x.startswith("ACCOR,")]) + "\n")
    avant = open(MAITRE, "rb").read()
    code, out = lancer(VER_P)
    dire("V6 ligne mise à part en double dans l'incrément : refus en bloc, code 1, maître intact",
         code == 1 and open(MAITRE, "rb").read() == avant and "en double" in out, (code, out[-300:]))
    # V4 — la même ligne fausse, mais la séance du 28-10 est DÉJÀ au maître : refus en bloc, maître intact. L'incrément
    # est réécrit ici, sans le double de V6 : sinon V4 refuserait pour la « séance en double » et ne prouverait plus
    # rien (sabotage H8 non vu, contrôles finaux du 30-10-2026 à 15h21).
    open(inc, "w", encoding="utf-8").write("\n".join([entete7] + faux) + "\n")
    ecrire_maitre(lambda x: True)
    subprocess.run("git add donnees/cours_maitre.csv && git -c user.name=e -c user.email=e@e -c commit.gpgsign=false "
                   "commit -q --allow-empty -m complet", shell=True, check=True, capture_output=True)
    avant = open(MAITRE, "rb").read()
    code, out = lancer(VER_P)
    dire("V4 ligne fausse d'une séance déjà au maître : refus en bloc, code 1, maître intact",
         code == 1 and open(MAITRE, "rb").read() == avant and "RIEN N'EST ÉCRIT" in out and "en double" not in out,
         (code, out[-300:]))
    # V5 — le lecteur en échec (nature des trous à l'en-tête faux) : refus en bloc, alerte du maître avec « CE QUI LÈVE
    # CE REFUS », sans trace Python (relecteur du 30-10-2026, I1, X6 et X1 ; le chemin du 04-01-2027, A-639).
    veille_sans_le_28()
    open(inc, "w", encoding="utf-8").write("\n".join([entete7] + du_28) + "\n")
    nt = "donnees/NATURE_DES_TROUS.csv"
    garde = open(nt, encoding="utf-8").read()
    try:
        open(nt, "w", encoding="utf-8").write("nimporte,quoi\n1,2\n")
        avant = open(MAITRE, "rb").read()
        code, out = lancer(VER_P)
        alm = open(ALM, encoding="utf-8").read() if os.path.exists(ALM) else ""
        dire("V5 lecteur en échec : code 1, maître intact, alerte « CE QUI LÈVE CE REFUS », sans trace Python",
             code == 1 and open(MAITRE, "rb").read() == avant and "CE QUI LÈVE CE REFUS" in alm
             and "Traceback" not in out and "la relecture par le lecteur commun a échoué" in out, (code, out[-300:]))
    finally:
        open(nt, "w", encoding="utf-8").write(garde)
VER_P = "programmes/TENIR_L_HISTORIQUE.py"
un("C4", c4); un("C5", c5); un("C6", c6); un("C7", c7); un("T1", t1); un("T2", t2); un("T7", t7); un("T8", t8); un("V1", v1)
ecrire_maitre(lambda x: True)
print("ROUGES %d" % len(rouges))
for x in rouges:
    print("  " + x)
'''


def jeu(sab):
    """Joue les épreuves sur une copie de la racine, sabotée ou non, et rend le nombre de rouges et leur détail.

    ① RÔLE — Un jeu complet d'épreuves.
    ② CONTEXTE D APPEL — Le programme principal, une fois pour Z0 et une fois par sabotage joué.
    ③ ENTRÉE — `sab` : le nom du sabotage, une clé de SABOTAGES.
    ④ CONDITIONS D ENTRÉE — Chaque texte visé par le sabotage existe une seule fois dans son fichier.
    ⑤ SORTIE — DEUX valeurs : le nombre de rouges (−1 si le sabotage ne s'applique pas, 99 si CODE a planté), et le
      détail.
      [rend: 2]
    ⑥ TRAITEMENT — copier la racine sans .git, archives, caches ni gros dossiers de sources ; saboter ; lancer CODE
      depuis la copie ; lire « ROUGES n ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas une preuve (R-731). CODE réécrit
      le maître et les fichiers du soir : il ne tourne jamais ailleurs que dans une copie.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Une copie temporaire, effacée.
    ⑪ TERMINAISON — Bornée à 900 secondes.
      [sort: non]
    """
    d = tempfile.mkdtemp(prefix="circuit_lecteur_")
    try:
        r = os.path.join(d, "r")
        shutil.copytree(DEPOT, r, ignore=shutil.ignore_patterns(".git", "__pycache__", "archives", "etudes", "temoins",
                                                                   "tests", "rapports", *SANS))
        # Le versement relit la version enregistrée du maître (git show HEAD) : V0 et V1 font un dépôt git jetable,
        # dans la copie seulement.
        for f, a, b in SABOTAGES[sab]:
            p = os.path.join(r, f)
            t = open(p, encoding="utf-8").read()
            if t.count(a) != 1:
                return -1, "texte du sabotage introuvable (%d fois) : %s" % (t.count(a), a[:60])
            with open(p, "w", encoding="utf-8") as h:
                h.write(t.replace(a, b))
        try:
            x = subprocess.run([sys.executable, "-B", "-c", CODE], cwd=r, capture_output=True, text=True, timeout=900)
        except subprocess.TimeoutExpired:
            return 99, "délai de 900 s dépassé"
        lignes = x.stdout.strip().splitlines()
        tete = next((l for l in lignes if l.startswith("ROUGES ")), None)
        if x.returncode != 0 or tete is None:
            return 99, "plantage : " + (x.stderr.strip().splitlines() or ["?"])[-1][:200]
        return int(tete.split()[1]), "\n".join(lignes[lignes.index(tete) + 1:])
    finally:
        shutil.rmtree(d, ignore_errors=True)


_sab = next((a for a in sys.argv[1:] if a.startswith("--saboter")), None)
if _sab is None:
    _choix = ["Z0"]
elif _sab == "--saboter":
    _choix = list(SABOTAGES)
else:
    _choix = ["Z0"] + [n for n in _sab.split("=", 1)[1].split(",") if n]
_faute = False
for sab in _choix:
    if sab not in SABOTAGES:
        print(f"== {sab} : INCONNU <-- SABOTAGE NON VU OU INVALIDE")
        _faute = True
        continue
    n, det = jeu(sab)
    if sab == "Z0":
        bon = n == 0
        print(f"== {sab} : {'vert' if n == 0 else str(n) + ' rouge(s)'} {'(attendu)' if bon else '<-- ATTENDU VERT'}")
    else:
        # un plantage (99) ou un sabotage inapplicable (-1) ne prouve rien : il ne compte jamais comme sabotage vu
        bon = 0 < n < 99
        etat = "PLANTAGE" if n == 99 else "INAPPLICABLE" if n < 0 else "vert" if n == 0 else str(n) + " rouge(s)"
        print(f"== {sab} : {etat} {'(attendu)' if bon else '<-- SABOTAGE NON VU OU INVALIDE'}")
        noms = [l.strip().split(" · ")[0] for l in det.splitlines() if l.strip()] if bon else []
        print(f"{sab} " + (f"mord : {noms}" if bon else "NE MORD PAS"))
    if det and (not bon or sab == "Z0"):
        print(det)
    _faute = _faute or not bon
print("VERDICT :", "tout est conforme" if not _faute else "ECHEC — voir ci-dessus")
sys.exit(1 if _faute else 0)
