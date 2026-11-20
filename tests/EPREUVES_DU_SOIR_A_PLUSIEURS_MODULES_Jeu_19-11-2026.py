#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_SOIR_A_PLUSIEURS_MODULES_Jeu_19-11-2026.py — Jeu 19-11-2026 (Paris) — épreuves du soir à plusieurs
modules de signal (BACKLOG A-925, chantier ②). Simulation uniquement — aucun ordre réel.

LE SENS EN TÊTE. Jean-Luc a décidé le 19-11-2026 à 19h23 (A-925, réponse « 1 ») de réparer le circuit du soir pour
qu'il fasse tourner PLUSIEURS modules de signal. Faits mesurés le même jour sur copie : avec le module RSI de la fiche
IND-001-RETEST ajouté aux deux fiches C5, le détecteur écrivait « plusieurs signaux… aucun signal ne sera calculé » et
les fiches C5 perdaient aussi leurs signaux ; seul, il rendait « CALIBRAGE IMPOSSIBLE » ; le radar disait « AUCUN
MODULE CONNU » même pour une fiche qui déclare son module. Ce fichier prouve, sur une copie du dépôt et sur des cours
récents seulement (le cours maître, depuis 2024 ; aucune séance de 2000 à 2023 n'est lue), que : ① le détecteur range
les fiches par signal, calibre chaque module sur son étalon et écrit chaque signal avec les fiches qui le reçoivent ;
② le teneur de positions n'attribue un signal qu'à ces fiches ; ③ une fiche dont le module est introuvable, ou dont le
module n'a pas d'étalon, est mise à part et NOMMÉE sans empêcher les autres, et le teneur la compte (le pas de fin
« Rougir si une fiche suivie a ete mise a part » rougit) ; ④ le radar reconnaît un module déclaré par la fiche.

① RÔLE — Les cas M1 à M6 ; avec `--saboter`, prouver que chaque cas MORD : chaque sabotage retire une partie de la
  correction et doit faire rougir au moins un cas ; les fichiers sont remis à l'octet avant chaque sabotage.
② CONTEXTE D'APPEL — À la main : `python3 -I tests/EPREUVES_DU_SOIR_A_PLUSIEURS_MODULES_Jeu_19-11-2026.py <racine>
  [--saboter]` ; par la certification, qui lance chaque fichier de tests/ avec la racine, puis « --saboter ».
③ ENTRÉE — `<racine>` : un clone du dépôt, jamais modifié (tout se joue sur une copie sous /dev/shm ou /tmp).
④ CONDITIONS D'ENTRÉE — La racine porte programmes/, donnees/ (registre avec C5E10-QA-V1, C5E10-OBS-V1 en QA et
  IND-001-RETEST, référentiel, cours maître avec la séance du 2026-01-21) et le module RSI REBOND.
⑤ SORTIE — UNE valeur, le code de sortie : 0 si tous les cas passent (et, avec --saboter, si chaque sabotage fait
  rougir au moins un cas) ; 1 sinon ; 2 si la copie n'a pas pu être faite. [rend: 1]
⑥ TRAITEMENT — ① copier la racine sans .git, etudes/, archives/, prompts_taches/ ni PILOTE_SOCLE* · ② passer la
  dernière ligne d'IND-001-RETEST à `etat_vie` QA (la fiche réelle, son univers et ses réglages réels) · ③ jouer les
  cas, programmes lancés en ligne de commande comme le circuit, environnement vidé · ④ avec --saboter, chaque sabotage.
⑦ UNITÉ — Prix en euros ; CCI sans unité.
⑧ POURQUOI — Boucle R-731 (épreuves avec sabotages, une vraie ligne R-732) : une épreuve qui reste verte quand on
  retire ce qu'elle teste est une décoration. VRAIES LIGNES (cours maître, mesurées le 19-11-2026) : le 2026-01-21, le
  module RSI signale LVMH (clôture 585,2) et STELLANTIS (8,23), le module C5 signale VEOLIA (29,38, CCI −139,0) ;
  VEOLIA est AUSSI dans l'univers d'IND-001-RETEST : elle ne doit pas lui être attribuée.
⑨ CE QUI CLOCHE — ① Le circuit GitHub n'est pas lancé : M3 et M5 lisent la sortie du pas du teneur
  (`fiches_mises_a_part=<n>`), dont le pas rouge est éprouvé par K5 des épreuves E8. ② Un calcul de groupe qui LÈVE
  (mise à part par `signaux_de_la_seance`) n'est pas joué : aucune vraie ligne ne le provoque (A-710). ③ Les cas
  dépendent des fiches du registre au 19-11-2026 et de la séance du 2026-01-21 au cours maître.
⑩ EFFET — Écrit seulement dans son dossier temporaire, qu'il efface à la fin.
⑪ TERMINAISON — Rend la main ; chaque programme lancé est borné à 600 s. [sort: oui — code]
"""
import csv, io, json, os, shutil, subprocess, sys, tempfile

RACINE = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else ".")
SABOTER = "--saboter" in sys.argv
CTR = "programmes/CONTRATS_DES_FICHIERS.py"
DET = "programmes/DETECTER_LES_SIGNAUX_GITHUB.py"
TEN = "programmes/TENIR_LES_POSITIONS.py"
RAD = "programmes/audit_ecosysteme.py"
SIG = "donnees/signaux_du_jour.json"


def registre_au_contrat(racine):
    """Rend le chemin du registre des stratégies, lu au contrat de la racine.
    ① RÔLE — Ne jamais écrire ici le chemin du registre : il vit au contrat, une fois. ② CONTEXTE D'APPEL — Au
    chargement de ce fichier, une fois, pour REG. ③ ENTRÉE — `racine`. ④ CONDITIONS D'ENTRÉE — le contrat existe sous la
    racine. ⑤ SORTIE — UNE valeur : `REGISTRE_DES_STRATEGIES` du contrat. [rend: 1] ⑥ TRAITEMENT — charger le contrat
    par son chemin, sous un nom à part. ⑦ UNITÉ — —. ⑧ POURQUOI — R-708 ; G1 de
    tests/EPREUVES_DU_REGISTRE_DES_STRATEGIES_Jeu_05-11-2026.py rougit sur une constante qui nomme le registre (même
    lecture que tests/EPREUVES_C_LE_SOIR_LIT_LA_FICHE_Mar_10-11-2026.py). ⑨ CE QUI CLOCHE — un contrat absent fait
    tomber le chargement, code non nul (R-734). ⑩ EFFET — exécute le contrat. ⑪ TERMINAISON — rend la main.
    [sort: non]"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("contrat_pour_multi", os.path.join(racine, CTR))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.REGISTRE_DES_STRATEGIES


REG = registre_au_contrat(RACINE)   # le chemin du registre vit au contrat (R-708)
POS = "donnees/claude_positions_ouvertes.csv"
JOU = "donnees/claude_journal_trades.csv"
MAITRE = "donnees/cours_maitre.csv"
IND, QA, OBS = "IND-001-RETEST", "C5E10-QA-V1", "C5E10-OBS-V1"
SEANCE = "2026-01-21"
RSI_COPIE = "programmes/MODULE_SIGNAL_RSI_REBOND_COPIE_SANS_ETALON.py"
ATTENDU = {"LVMH": [IND], "STELLANTIS": [IND], "VEOLIA": [OBS, QA]}


def copier():
    """Copie la racine dans un dossier jetable. ① RÔLE — Ne jamais jouer sur le dépôt. ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — RACINE. ④ CONDITIONS D'ENTRÉE — de la place sous /dev/shm ou le dossier temporaire. ⑤ SORTIE — UNE
    valeur, le chemin de la copie. [rend: 1] ⑥ TRAITEMENT — copier sans .git, etudes/, archives/, prompts_taches/, ni
    aucun fichier PILOTE_SOCLE*. ⑦ UNITÉ — —. ⑧ POURQUOI — les programmes du circuit écrivent tous (instructions du
    projet, §7) ; prompts_taches/ et PILOTE_SOCLE* ne servent à aucun cas et ne doivent pas être recopiés. ⑨ CE QUI
    CLOCHE — une copie laissée par un arrêt brutal reste. ⑩ EFFET — écrit la copie. ⑪ TERMINAISON — rend la main ;
    lève OSError. [sort: non]"""
    base = os.path.join("/dev/shm" if os.path.isdir("/dev/shm") else tempfile.gettempdir(),
                        "epreuves_multi_%d" % os.getpid())

    def ignorer(d, noms):
        out = [n for n in noms if n.startswith("PILOTE_SOCLE")]
        if d == RACINE:
            out += [n for n in noms if n in (".git", "etudes", "archives", "prompts_taches")]
        return out
    shutil.copytree(RACINE, base, ignore=ignorer)
    return base


def changer(t, ident, valeurs):
    """Rend le texte du registre où la DERNIÈRE ligne de `ident` porte les `valeurs` ({colonne: texte}).
    ① RÔLE — Fabriquer un registre de cas. ② CONTEXTE D'APPEL — `main`, `les_cas`. ③ ENTRÉE — `t` : texte du registre ·
    `ident` · `valeurs`. ④ CONDITIONS D'ENTRÉE — `ident` présent, colonnes dans l'en-tête. ⑤ SORTIE — UNE valeur, le
    texte. [rend: 1] ⑥ TRAITEMENT — lire en CSV, changer les cases, réécrire. ⑦ UNITÉ — —. ⑧ POURQUOI — la dernière
    ligne d'un identifiant fait foi (n°83). ⑨ CE QUI CLOCHE — les guillemets sont réécrits à la manière du module csv.
    ⑩ EFFET — Aucun. ⑪ TERMINAISON — lève ValueError si l'identifiant ou une colonne manque. [sort: non]"""
    lignes = list(csv.reader(io.StringIO(t)))
    rang = max(i for i, l in enumerate(lignes) if l and l[0] == ident)
    for col, v in valeurs.items():
        lignes[rang][lignes[0].index(col)] = v
    s = io.StringIO()
    csv.writer(s, lineterminator="\n").writerows(lignes)
    return s.getvalue()


def lancer(base, programme):
    """Lance un programme du circuit sur la copie, environnement vidé ; rend (code, affichage, sortie du pas).
    ① RÔLE — Jouer un pas comme le circuit. ② CONTEXTE D'APPEL — `les_cas`. ③ ENTRÉE — `base`, `programme` (chemin
    relatif). ④ CONDITIONS D'ENTRÉE — `python3` dans /usr/bin ou /bin. ⑤ SORTIE — TROIS valeurs : le code, l'affichage,
    le dictionnaire de la sortie du pas (GITHUB_OUTPUT). [rend: 3] ⑥ TRAITEMENT — fichier de sortie du pas vide, lancer,
    lire. ⑦ UNITÉ — —. ⑧ POURQUOI — l'environnement vidé évite qu'un jeton ou une variable de l'appelant n'entre dans
    l'épreuve. ⑨ CE QUI CLOCHE — un délai dépassé rend le code 124. ⑩ EFFET — ce qu'écrit le programme, dans la copie.
    ⑪ TERMINAISON — borné à 600 s. [sort: non]"""
    so = os.path.join(base, "_sortie_du_pas")
    open(so, "w").close()
    env = {"PATH": "/usr/bin:/bin", "HOME": tempfile.gettempdir(), "GITHUB_OUTPUT": so}
    try:
        p = subprocess.run([sys.executable, "-I", "-B", programme, "."], cwd=base, env=env,
                           capture_output=True, text=True, timeout=600)
        code, out = p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        code, out = 124, "délai dépassé"
    sortie = dict(l.split("=", 1) for l in open(so, encoding="utf-8").read().splitlines() if "=" in l)
    return code, out, sortie


def signaux_du_21_janvier(base):
    """Rend les signaux de la séance du 2026-01-21, calculés par `signaux_de_la_seance` du détecteur de la copie.
    ① RÔLE — Le cas M2, et le fichier que M3 donne au teneur. ② CONTEXTE D'APPEL — `les_cas`. ③ ENTRÉE — `base`.
    ④ CONDITIONS D'ENTRÉE — le registre de la copie suit IND-001-RETEST. ⑤ SORTIE — DEUX valeurs : la liste des signaux
    donnés (ou None), l'affichage. [rend: 2] ⑥ TRAITEMENT — processus neuf : `charger`, puis `signaux_de_la_seance` à
    la séance ; JSON imprimé en dernière ligne. ⑦ UNITÉ — —. ⑧ POURQUOI — le détecteur ne publie que la dernière
    séance ; une séance passée se rejoue par sa fonction, comme les épreuves du 29-10-2026. ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — Aucun dans la copie. ⑪ TERMINAISON — borné à 600 s. [sort: non]"""
    code = ("import sys, json; sys.path.insert(0, 'programmes'); import DETECTER_LES_SIGNAUX_GITHUB as D; "
            "B, m, c, l = D.charger('.'); print(json.dumps(D.signaux_de_la_seance(c, l, B, m, %r)[0]))" % SEANCE)
    try:
        p = subprocess.run([sys.executable, "-I", "-B", "-c", code], cwd=base, capture_output=True, text=True,
                           timeout=600, env={"PATH": "/usr/bin:/bin", "HOME": tempfile.gettempdir()})
        return json.loads(p.stdout.strip().splitlines()[-1]), p.stdout + p.stderr
    except Exception as e:
        return None, "%s : %s" % (type(e).__name__, e)


def clotures_du_maitre(base, valeurs, seance):
    """Rend {valeur: clôture} lues dans les VRAIES lignes du cours maître de la copie, à la séance (R-732).
    ① RÔLE — Confronter un signal à sa vraie ligne. ② CONTEXTE D'APPEL — `les_cas`, M2. ③ ENTRÉE — `base`, `valeurs`,
    `seance`. ④ CONDITIONS D'ENTRÉE — le maître porte les colonnes `valeur`, `date`, `close`. ⑤ SORTIE — UNE valeur, le
    dictionnaire. [rend: 1] ⑥ TRAITEMENT — lire en CSV, garder les lignes de la séance. ⑦ UNITÉ — euros. ⑧ POURQUOI —
    R-732 : un cas au moins vient d'une vraie ligne. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — rend la main. [sort: non]"""
    out = {}
    for l in csv.DictReader(open(os.path.join(base, MAITRE), encoding="utf-8")):
        if l.get("date") == seance and l.get("valeur") in valeurs:
            out[l["valeur"]] = float(l["close"])
    return out


def les_cas(base, reg_ind_qa, pos_vide, jou_vide):
    """Joue M1 à M6 sur `base` ; rend la liste (nom, vrai/faux, preuve).
    ① RÔLE — Les cas. ② CONTEXTE D'APPEL — `main`, une fois puis une fois par sabotage. ③ ENTRÉE — `base`,
    `reg_ind_qa` (le vrai registre, IND-001-RETEST passée en QA), `pos_vide` et `jou_vide` (les en-têtes des fichiers
    des positions et du journal). ④ CONDITIONS D'ENTRÉE — celles du fichier. ⑤ SORTIE — UNE valeur, la liste.
    [rend: 1] ⑥ TRAITEMENT — chaque cas pose registre, positions et journal, lance, juge. ⑦ UNITÉ — —. ⑧ POURQUOI —
    voir ⑧ du fichier. ⑨ CE QUI CLOCHE — voir ⑨ du fichier. ⑩ EFFET — écrit dans la copie. ⑪ TERMINAISON — celle des
    programmes lancés. [sort: non]"""
    res = []

    def dire(nom, ok, preuve):
        res.append((nom, bool(ok), str(preuve)[-600:]))

    def poser(reg, signaux=None):
        open(os.path.join(base, REG), "w", encoding="utf-8").write(reg)
        open(os.path.join(base, POS), "w", encoding="utf-8").write(pos_vide)
        open(os.path.join(base, JOU), "w", encoding="utf-8").write(jou_vide)
        if signaux is not None:
            json.dump(signaux, open(os.path.join(base, SIG), "w", encoding="utf-8"), ensure_ascii=False)

    def lu():
        return json.load(open(os.path.join(base, SIG), encoding="utf-8"))

    # M1 — DEUX MODULES LE SOIR : le détecteur calibre RSI REBOND et C5, publie sans garde ni mise à part, et dit le
    # calibrage de chacun avec ses fiches.
    poser(reg_ind_qa)
    c, o, _s = lancer(base, DET)
    j = lu() if c == 0 else {}
    cal = {x.get("nom"): x.get("fiches") for x in j.get("calibrages", [])}
    dire("M1 deux modules : code 0, deux calibrages OK (RSI-REBOND : IND-001-RETEST ; C5 : OBS, QA), ni garde ni mise "
         "à part", c == 0 and o.count("calibrage OK") == 2 and cal == {"RSI-REBOND": [IND], "C5-ETENDU-10": [OBS, QA]}
         and "garde_du_soir" not in j and "fiches_mises_a_part" not in j and j.get("strategie") == "RSI-REBOND + C5-ETENDU-10"
         and all(isinstance(s.get("fiches"), list) and s["fiches"] for s in j.get("signaux", [])),
         (c, cal, o[-400:]))

    # M2 — LES DEUX MODULES DONNENT LEURS SIGNAUX, CHACUN À SES FICHES (vraies lignes du 2026-01-21).
    dj, o2 = signaux_du_21_janvier(base)
    vues = {s["valeur"]: s.get("fiches") for s in (dj or [])}
    vraies = clotures_du_maitre(base, set(ATTENDU), SEANCE)
    dire("M2 2026-01-21 : LVMH et STELLANTIS → IND-001-RETEST seule, VEOLIA → les deux C5 seules, clôtures des vraies "
         "lignes, CCI fini partout", dj is not None and vues == ATTENDU and len(vraies) == 3
         and all(s["close"] == vraies[s["valeur"]] for s in dj)
         and all(isinstance(s.get("cci"), float) for s in dj) and next(s for s in dj if s["valeur"] == "VEOLIA")["cci"] == -139.0,
         (vues, vraies, o2[-300:]))

    # M3 — LE TENEUR N'ATTRIBUE UN SIGNAL QU'AUX FICHES QU'IL NOMME : VEOLIA (dans l'univers d'IND-001-RETEST aussi)
    # ne va qu'aux C5 ; LVMH, le CCI le plus bas des deux signaux RSI (R-207bis), prend le jeton d'IND-001-RETEST.
    poser(reg_ind_qa, {"seance": SEANCE, "signaux": dj or []})
    ct, ot, st = lancer(base, TEN)
    paires = {(p["strategie"], p["valeur"]) for p in csv.DictReader(open(os.path.join(base, POS), encoding="utf-8-sig"))}
    jeton_ind = {p["valeur"] for p in csv.DictReader(open(os.path.join(base, POS), encoding="utf-8-sig"))
                 if p["strategie"] == IND and p.get("comptabilite") == "un_jeton"}
    dire("M3 teneur : IND-001-RETEST reçoit LVMH et STELLANTIS (jeton : LVMH), les C5 reçoivent VEOLIA, IND-001-RETEST "
         "ne reçoit PAS VEOLIA, code 0, aucune fiche mise à part",
         ct == 0 and paires == {(IND, "LVMH"), (IND, "STELLANTIS"), (QA, "VEOLIA"), (OBS, "VEOLIA")}
         and jeton_ind == {"LVMH"} and st.get("fiches_mises_a_part") == "0", (ct, sorted(paires), jeton_ind, st, ot[-300:]))

    # M4 — MODULE INTROUVABLE : seule IND-001-RETEST est mise à part, nommée au fichier ; C5 tourne ; le teneur la compte.
    reg = changer(reg_ind_qa, IND, {"module_signal": "programmes/MODULE_INTROUVABLE.py"})
    poser(reg)
    c, o, _s = lancer(base, DET)
    j = lu() if c == 0 else {}
    ma = j.get("fiches_mises_a_part") or []
    poser(reg, j if c == 0 else {"seance": SEANCE, "signaux": []})
    ct, ot, st = lancer(base, TEN)
    dire("M4 module introuvable : code 0, IND-001-RETEST seule mise à part et nommée (« introuvable »), C5 calibré "
         "(univers 10), le teneur compte 1 fiche à part",
         c == 0 and [x.get("fiche") for x in ma] == [IND] and "introuvable" in ma[0].get("motif", "")
         and j.get("strategie") == "C5-ETENDU-10" and j.get("univers") == 10 and "garde_du_soir" not in j
         and ct == 0 and st.get("fiches_mises_a_part") == "1", (c, ma, ct, st, o[-300:], ot[-200:]))

    # M5 — MODULE SANS ÉTALON (copie du module RSI sous un autre nom : le juge l'accepte, le détecteur ne peut pas le
    # calibrer) : seule IND-001-RETEST est mise à part, « CALIBRAGE IMPOSSIBLE » ; C5 tourne ; le teneur la compte et
    # dit qu'elle vient du détecteur.
    shutil.copyfile(os.path.join(base, "programmes/MODULE_SIGNAL_RSI_REBOND.py"), os.path.join(base, RSI_COPIE))
    reg = changer(reg_ind_qa, IND, {"module_signal": RSI_COPIE})
    poser(reg)
    c, o, _s = lancer(base, DET)
    j = lu() if c == 0 else {}
    ma = j.get("fiches_mises_a_part") or []
    poser(reg, j if c == 0 else {"seance": SEANCE, "signaux": []})
    ct, ot, st = lancer(base, TEN)
    os.remove(os.path.join(base, RSI_COPIE))
    dire("M5 module sans étalon : code 0, IND-001-RETEST seule mise à part (CALIBRAGE IMPOSSIBLE), C5 calibré, le "
         "teneur la compte (« mise a part par le detecteur »)",
         c == 0 and [x.get("fiche") for x in ma] == [IND] and "CALIBRAGE IMPOSSIBLE" in ma[0].get("motif", "")
         and "calibrage OK" in o and j.get("univers") == 10 and ct == 0 and st.get("fiches_mises_a_part") == "1"
         and "mise a part par le detecteur" in ot, (c, ma, ct, st, o[-300:], ot[-300:]))

    # M6 — LE RADAR RECONNAÎT LE MODULE DÉCLARÉ PAR LA FICHE ; une fiche en service sans module est encore dite.
    poser(reg_ind_qa)
    cr, orad, _s = lancer(base, RAD)
    l3 = [l for l in orad.splitlines() if "3-Calcul" in l]
    ok_a = cr == 0 and l3 and not any(("AUCUN MODULE CONNU" in l or "SANS CODE DE SIGNAL" in l) and IND in l for l in l3)
    poser(changer(reg_ind_qa, IND, {"module_signal": ""}))
    cr2, orad2, _s = lancer(base, RAD)
    l3b = [l for l in orad2.splitlines() if "3-Calcul" in l]
    ok_b = any("AUCUN MODULE CONNU POUR : %s" % IND in l and QA not in l and OBS not in l for l in l3b)
    dire("M6 radar : aucune fausse alerte pour IND-001-RETEST qui déclare son module ; sans module, elle seule est dite",
         ok_a and ok_b, (cr, l3, cr2, l3b))
    return res


# (nom, fichier saboté, texte avant, texte après) — chaque texte « avant » doit exister une seule fois.
SABOTAGES = [
    ("SB1 retour à un seul module", DET,
     "    return SuiviDuSoir([GroupeDuSoir(sig, membres) for sig, membres in par_signal.values()], refusees)\n",
     "    return SuiviDuSoir([GroupeDuSoir(sig, membres) for sig, membres in list(par_signal.values())[:1]], refusees)\n"),
    ("SB2 un module sans étalon arrête tout le soir", DET,
     "            motifs_du_calibrage.append(motif)\n            mod.retirer(g, motif)\n",
     "            print(\"CODE 1 — \" + motif)\n            sys.exit(1)\n"),
    ("SB3 une fiche refusée par la garde arrête tout le soir", DET,
     "            refusees.append((ident, motif))\n            continue\n",
     "            print(\"CODE 1 — \" + motif)\n            sys.exit(1)\n"),
    ("SB4 le teneur attribue par l'univers seul", TEN,
     "            if code and code in univers and (nommees is None or sid in nommees):\n",
     "            if code and code in univers:\n"),
    ("SB5 le teneur ignore les fiches mises à part par le détecteur", TEN,
     "            if ligne[\"id\"] in _par_le_detecteur:\n", "            if False:\n"),
    ("SB6 le contrat SIGNAL sans `fiches`", CTR,
     'SIGNAL = ["valeur", "date_signal", "cmf", "cci", "close", "fiches"]\n',
     'SIGNAL = ["valeur", "date_signal", "cmf", "cci", "close"]\n'),
    ("SB7 l'étalon du module RSI retiré", DET,
     '    "programmes/MODULE_SIGNAL_RSI_REBOND.py · signaux_rsi_rebond":\n',
     '    "programmes/MODULE_SIGNAL_RSI_REBOND_RETIRE.py · signaux_rsi_rebond":\n'),
    ("SB8 le radar revient à l'énumération", RAD,
     "        if module.lower() in J.VIDE:\n",
     "        if _id not in (\"C5E10-QA-V1\", \"C5E10-OBS-V1\"):\n"),
    ("SB9 les signaux ne nomment plus leurs fiches", DET,
     "                         \"close\": serie[s[\"i\"]][\"close\"], \"fiches\": g.fiches_de(v)}\n",
     "                         \"close\": serie[s[\"i\"]][\"close\"], \"fiches\": list(mod.fiches)}\n"),
]


def main():
    """Joue les cas, puis les sabotages. ① RÔLE — Le programme. ② CONTEXTE D'APPEL — la ligne de commande.
    ③ ENTRÉE — RACINE, SABOTER. ④ CONDITIONS D'ENTRÉE — celles du fichier. ⑤ SORTIE — UNE valeur, le code (voir ⑤ du
    fichier). [rend: 1] ⑥ TRAITEMENT — copier ; registre avec IND-001-RETEST en QA ; en-têtes des positions et du
    journal ; jouer les cas ; avec --saboter, remettre les fichiers à l'octet, saboter un à un, exiger un rouge.
    ⑦ UNITÉ — —. ⑧ POURQUOI — R-731. ⑨ CE QUI CLOCHE — un motif de sabotage trouvé 0 ou 2 fois rougit le verdict (voulu :
    le sabotage doit viser le code livré). ⑩ EFFET — copie effacée à la fin. ⑪ TERMINAISON — rend la main. [sort: non]"""
    try:
        base = copier()
    except OSError as e:
        print("CODE 2 — copie impossible : %s" % e)
        return 2
    try:
        reg0 = open(os.path.join(base, REG), encoding="utf-8").read()
        reg_ind_qa = changer(reg0, IND, {"etat_vie": "QA"})
        pos_vide = open(os.path.join(base, POS), encoding="utf-8").readline()
        jou_vide = open(os.path.join(base, JOU), encoding="utf-8").readline()
        textes0 = {f: open(os.path.join(base, f), encoding="utf-8").read() for f in (CTR, DET, TEN, RAD)}
        res = les_cas(base, reg_ind_qa, pos_vide, jou_vide)
        for nom, ok, preuve in res:
            print(("  ✅ " if ok else "  ❌ ") + nom + ("" if ok else "\n       " + preuve))
        bon = all(ok for _n, ok, _p in res)
        if SABOTER:
            for nom, fichier, avant, apres in SABOTAGES:
                for f, t in textes0.items():
                    open(os.path.join(base, f), "w", encoding="utf-8").write(t)
                if textes0[fichier].count(avant) != 1:
                    print("  ❌ %s : motif trouvé %d fois (attendu 1)" % (nom, textes0[fichier].count(avant)))
                    bon = False
                    continue
                open(os.path.join(base, fichier), "w", encoding="utf-8").write(textes0[fichier].replace(avant, apres))
                r = les_cas(base, reg_ind_qa, pos_vide, jou_vide)
                rouges = [n.split(" ")[0] for n, ok, _p in r if not ok]
                print(("  ✅ " if rouges else "  ❌ ") + "%s → rougissent : %s" % (nom, ", ".join(rouges) or "AUCUNE"))
                bon = bon and bool(rouges)
            for f, t in textes0.items():
                open(os.path.join(base, f), "w", encoding="utf-8").write(t)
        print("VERDICT :", "VERT" if bon else "ROUGE")
        return 0 if bon else 1
    finally:
        shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
