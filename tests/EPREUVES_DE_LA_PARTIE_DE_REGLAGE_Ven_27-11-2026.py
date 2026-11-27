#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPREUVES_DE_LA_PARTIE_DE_REGLAGE_Ven_27-11-2026.py — Ven 27-11-2026 (Paris)
EN ESSAI · épreuve · Rôle : prouver que la moulinette ne lit, ne joue, n'écrit et ne calibre QUE les 70 % moins la bande
retirée (R-505 v2, étape 3 ; A-1078), et que la garde du regard unique laisse passer ce réglage mais refuse le
jugement des 30 % sans déclaration datée (A-777, A-853, A-1073). Simulation uniquement : aucun ordre réel.

USAGE
    python3 -B tests/EPREUVES_DE_LA_PARTIE_DE_REGLAGE_Ven_27-11-2026.py <copie_sans_.git> [--sans-sabotages]
    Rien n'est écrit dans la copie : tout va dans un dossier temporaire, effacé à la fin.

LE SENS EN TÊTE — Défauts L1-2 et L1-1 du RELU de Cowork sur lot-r505-L1 (27-11-2026) : la moulinette jouait chaque
version sur toute la période de la fiche (30 % compris) et écrivait leur gain ; et la garde du regard unique (fenêtre
2000-2023 du cas 1 de C5) refusait aussi le réglage d'IND-001-RETEST sur les 20 ans. Cette épreuve repose sur des
VRAIES lignes (R-732) : la combinatoire réelle de C5E10-OBS-V1 jouée sur le fichier maître 2024-2026 (hors fenêtre du
regard unique), la fiche réelle d'IND-001-RETEST pour la garde, sur des DATES fabriquées (aucun cours lu, aucune
stratégie jouée sur 2000-2023 : préambule du plan R505, §4).

① RÔLE — Jouer les cas A (JOUER_LES_VERSIONS, en processus, `jouer` du juge espionné), B (le juge seul sous l'option
  de la partie de réglage, `jouer` et `juger` espionnés), C (la garde et le jeton de réglage), puis chaque SABOTAGE
  sur une racine de liens où un seul programme est faussé : chacun doit faire tomber au moins un cas.
② CONTEXTE D'APPEL — À la main ; et sur GitHub (épreuve longue, voir la note du lot L1-CORR).
③ ENTRÉE — La copie (sans .git) ; `--sans-sabotages` ; `--interne <racine> <travail>` est l'appel de soi-même.
④ CONDITIONS D'ENTRÉE — La copie porte programmes/, donnees/ (maître, registre, combinatoire de C5E10-OBS-V1),
  gouvernance/ et temoins/ (golden et son témoin), emp.py.
⑤ SORTIE — Le code de sortie : 0 si tous les cas tiennent ET si chaque sabotage fait tomber un cas ; 1 sinon ;
  2 si l'épreuve n'a pas pu tourner (R-734).
⑥ TRAITEMENT — ① cas sur la copie (sous-processus `--interne`) · ② pour chaque sabotage : une racine de liens, le
  programme visé recopié faussé, les cas rejoués · ③ verdict.
⑦ UNITÉ — Dates, séances.
⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration (instructions §7).
⑨ CE QUI CLOCHE — ① Le cas A lit le maître 2024-2026 : la partie de réglage y est 2024 → mi-2025 ; le même code sur les
  20 ans n'est joué que par K13 (fiche d'essai) de l'épreuve des cours de la moulinette. ② L'espion compte les séances
  des cours REÇUS par `jouer` : il ne voit pas une lecture faite ailleurs (aucune n'est connue, relecture V1 §4).
⑩ EFFET — Écrit et efface un dossier temporaire ; lance des sous-processus.
⑪ TERMINAISON — Sort lui-même ; chaque sous-processus borné à 900 s. Un de mes appels peut-il ne pas revenir ? Non.
"""
import contextlib
import csv
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
SID, ESSAI = "C5E10-OBS-V1", "E01"
TROIS = ("%s-%s-0914" % (SID, ESSAI), "%s-%s-0001" % (SID, ESSAI), "%s-%s-0500" % (SID, ESSAI))
COMBINATOIRE = os.path.join("donnees", "combinatoires", "COMBINATOIRE_%s_%s.csv" % (SID, ESSAI))
FICHE_CAS_2, FICHE_CAS_1 = "IND-001-RETEST", "C5E10-QA-V1"
JOUER, JUGE, TRIER = "JOUER_LES_VERSIONS.py", "JUGE_DES_STRATEGIES.py", "TRIER_LES_VARIANTES.py"

# LES SABOTAGES : (nom, quoi, programme, texte d'origine, texte saboté)
SABOTAGES = [
    ("S1", "cours non coupés à la partie de réglage", JOUER,
     '    cours_du_jeu = {v: [b for b in s_ if b["date"] <= derniere] for v, s_ in cours.items()}',
     "    cours_du_jeu = cours"),
    ("S2", "le juge juge sous l'option", JUGE, "        if mod_jug and not _reglage:", "        if mod_jug:"),
    ("S3", "lecture au-delà de la partie de réglage permise", JUGE,
     "    if limite is None or not derniere or str(derniere) > limite:", "    if limite is None or not derniere:"),
    ("S4", "version « sans délai » jouée", JOUER,
     '                if COMMUN.lire_horizon_ou_aucune(v["horizon"]) is COMMUN.HORIZON_AUCUNE:\n                    w.writerow',
     '                if False:\n                    w.writerow'),
    ("S5", "le tri refuse la ligne non jouée", TRIER, "        non_jouee = aucune and not any(",
     "        non_jouee = False and not any("),
    ("S6", "jeton de réglage sans contrôle de date", JUGE, "    if str(derniere) > jeton.derniere:", "    if False:"),
    ("S7", "jeton de réglage sans contrôle de famille", JUGE,
     "    if deja:\n        return None, (\"famille", "    if False:\n        return None, (\"famille"),
    ("S8", "N5 h_max annulé par une version « aucune »", JOUER, "    h_max = max(_chiffrees)\n",
     "    h_max = 0 if _aucunes else max(_chiffrees)\n"),
    ("S9", "garde-fou des opérations hors des 70 % retiré", JOUER, "    if c.get(\"n_30\") or c.get(\"n_ecartes\"):",
     "    if False:"),
]


def lire(chemin):
    """Lit un CSV. ① lire · ② cas A · ③ `chemin` · ④ — · ⑤ DEUX valeurs : colonnes, lignes [rend: 2] · ⑥ DictReader ·
    ⑦ — · ⑧ — · ⑨ — · ⑩ lit · ⑪ rend la main. [sort: non]"""
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        return list(r.fieldnames), list(r)


def cas_a_et_b(racine, travail):
    """Cas A (JOUER en processus) et B (le juge seul sous l'option) ; rend la liste (nom, vrai/faux, détail). [rend: 1]

    ① RÔLE — Mesurer ce que la moulinette et son calibrage LISENT et ÉCRIVENT.
    ② CONTEXTE D'APPEL — `interne`.
    ③ ENTRÉE — `racine` : la copie (ou la racine saboteuse) · `travail` : un dossier vide.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête.
    ⑤ SORTIE — UNE liste de triplets.
    ⑥ TRAITEMENT — ① combinatoire réduite à trois vraies versions, la 0500 passée « aucune » · ② la limite attendue,
      calculée par le module de jugement sur le calendrier ENTIER du maître (frontière, bande de l'horizon chiffré le
      plus long) · ③ JOUER en processus, `jouer` du juge espionné · ④ contrôles · ⑤ le juge seul sous l'option, deux fois.
    ⑦ UNITÉ — Dates.
    ⑧ POURQUOI — Défaut L1-2 (RELU de Cowork, 27-11-2026).
    ⑨ CE QUI CLOCHE — Voir l'en-tête ⑨.
    ⑩ EFFET — Écrit sous `travail` ; modifie sys.argv, sys.path et le module du juge le temps des cas.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    r = []
    prog = os.path.join(racine, "programmes")
    sys.path.insert(0, prog)
    import JUGE_DES_STRATEGIES as J
    import CONTRATS_DES_FICHIERS as C
    import COMMUN
    M = J.charger_module(J.trouver(racine, "MODULE_JUGEMENT.py"), "jug")
    col, toutes = lire(os.path.join(racine, COMBINATOIRE))
    lignes = [dict(l) for l in toutes if l["id_version"] in TROIS]
    for l in lignes:
        l["versions_dans_l_essai"] = "3"
        l["version_de_la_fiche"] = "OUI" if l["id_version"] == TROIS[0] else ""
        if l["id_version"] == TROIS[2]:
            l["horizon"] = "aucune"
    comb = os.path.join(travail, "COMBINATOIRE_%s_%s.csv" % (SID, ESSAI))
    with open(comb, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=col)
        w.writeheader()
        w.writerows(lignes)
    # LA LIMITE ATTENDUE, calculée ICI par le module de jugement (jamais recopiée) sur le calendrier entier du maître
    fiche = C.fiches_du_registre(J.trouver(racine, C.NOM_DU_REGISTRE_DES_STRATEGIES))[SID]
    _ok, _m, bornes = J.porte_0(dict(fiche))
    mnemo = J.table_mnemoniques(J.trouver(racine, "REFERENTIEL_VALEURS"))
    cours, _lect = J.lire_par_le_lecteur(racine, os.path.relpath(J.fichiers_de_cours(racine)[0], racine), mnemo)
    seances = {b["date"] for s in cours.values() for b in s}
    frontiere = M.frontiere_de_la_fiche(fiche, seances, bornes)
    h_max = max(int(l["horizon"]) for l in lignes if l["horizon"] != "aucune")
    limite, largeur = M.fin_de_la_partie_de_reglage({d for d in seances if bornes[0] <= d <= bornes[1]}, h_max,
                                                    frontiere)
    r.append(("A0 limite calculée avant la frontière (bande %d, horizon %d)" % (largeur, h_max),
              limite is not None and limite < frontiere, (limite, frontiere)))
    # A — JOUER en processus, `jouer` du juge espionné
    vus = []
    vrai_jouer = J.jouer

    def espion(f, cours_, *a, **k):
        vus.append({"max": max((b["date"] for s in cours_.values() for b in s), default=""),
                    "horizon": f.get("horizon"), "periode": k.get("periode")})
        return vrai_jouer(f, cours_, *a, **k)
    import importlib.util
    spec = importlib.util.spec_from_file_location("jouer_epreuve", os.path.join(prog, JOUER))
    JV = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(JV)
    out = os.path.join(travail, "RESULTATS.csv")
    J.jouer, argv, tampon, code = espion, sys.argv, io.StringIO(), None
    sys.argv = [JOUER, racine, comb, out]
    try:
        with contextlib.redirect_stdout(tampon):
            code = JV.main()
    except Exception as e:
        tampon.write("\nEXCEPTION %s: %s" % (type(e).__name__, e))
    finally:
        J.jouer, sys.argv = vrai_jouer, argv
    sortie = tampon.getvalue()
    r.append(("A1 JOUER sur trois vraies versions (dont une « aucune ») : code 0", code == 0, sortie[-300:]))
    lu = max((v["max"] for v in vus), default="")
    r.append(("A2 aucune séance après la limite %s reçue par `jouer` (%d appels)" % (limite, len(vus)),
              bool(vus) and lu <= limite, "lu jusqu'au %s" % lu))
    rows = lire(out)[1] if os.path.exists(out) else []
    aucune = [l for l in rows if l["horizon"] == "aucune"]
    r.append(("A3 la version « aucune » n'est jamais jouée et sa ligne ne porte aucun chiffre",
              len(aucune) == 1 and not any(v["horizon"] == "aucune" for v in vus)
              and all(aucune[0][c] == "" for c in JV.COLONNES_CHIFFREES), aucune[:1]))
    r.append(("A4 recul calculé sur l'horizon chiffré le plus long (%d), malgré la version « aucune »" % h_max,
              ("délai chiffré le plus long %d + 1" % h_max) in sortie, [l for l in sortie.splitlines() if "RECUL" in l]))
    chiffrees = [l for l in rows if l["horizon"] != "aucune"]
    r.append(("A5 lignes jouées : fin jouée ≤ limite, colonnes de la période = colonnes « _70 »",
              len(chiffrees) == 2 and all(l["periode_fin"] <= limite and l["frontiere_70_30"] == frontiere and
                                          (l["operations"], l["gain_net_euros"]) == (l["operations_70"],
                                                                                    l["gain_net_euros_70"])
                                          for l in chiffrees), [(l["periode_fin"], l["operations"]) for l in chiffrees]))
    try:
        spec_t = importlib.util.spec_from_file_location("trier_epreuve", os.path.join(prog, TRIER))
        T = importlib.util.module_from_spec(spec_t)
        spec_t.loader.exec_module(T)
        T.lire_les_resultats(out, C)
        vu_t = "accepté"
    except Exception as e:
        vu_t = "%s: %s" % (type(e).__name__, e)
    r.append(("A6 le tri accepte le fichier (ligne « aucune » non jouée)", vu_t == "accepté", vu_t[:200]))
    # A7 — le garde-fou : une opération dont le signal tombe dans les 30 % est refusée
    try:
        JV.partie_de_reglage(M, [{"date_signal": max(d for d in seances if d <= bornes[1]), "net": 1.0}],
                             {d for d in seances if bornes[0] <= d <= bornes[1]}, h_max, frontiere)
        vu7 = "accepté"
    except ValueError as e:
        vu7 = str(e)
    r.append(("A7 partie_de_reglage refuse une opération des 30 %", "dans les 30 %" in vu7, vu7[:160]))
    # B — le juge seul sous l'option : la fin jouée par A, puis une lecture jusqu'à la frontière
    fin = chiffrees[0]["periode_fin"] if chiffrees else limite
    import CONTRATS_DES_FICHIERS as _C2
    for nom, derniere, attendu in (("B1", limite, 0), ("B2", frontiere, 1)):
        appels, jugements = [], []

        def espion_j(f, cours_, *a, **k):
            # le calibrage sur le golden (C5-ETENDU-10, sur le témoin du golden, chiffres figés) n'est pas la fiche : seul
            # le jeu de la fiche visée est compté (mesuré le 27-11-2026 : le calibrage lit jusqu'au 2026-07-10)
            if f.get("id") == SID:
                appels.append(max((b["date"] for s in cours_.values() for b in s), default=""))
            return vrai_jouer(f, cours_, *a, **k)
        vrai_juger = J.juger
        J.jouer, J.juger = espion_j, (lambda *a, **k: jugements.append(1))
        sys.argv = [JUGE, racine, SID, "%s%s,%s" % (_C2.OPTION_DE_LA_PARTIE_DE_REGLAGE, derniere, min(fin, derniere))]
        tampon, code = io.StringIO(), None
        try:
            with contextlib.redirect_stdout(tampon):
                code = J.main()
        except Exception as e:
            tampon.write("\nEXCEPTION %s: %s" % (type(e).__name__, e))
        finally:
            J.jouer, J.juger, sys.argv = vrai_jouer, vrai_juger, argv
        s = tampon.getvalue()
        if nom == "B1":
            r.append(("B1 juge seul, lecture jusqu'à la limite : code 0, rien de juger, rien lu après %s" % limite,
                      code == 0 and "PARTIE DE RÉGLAGE SEULE" in s and not jugements and appels
                      and max(appels) <= limite, "code %s · juger %d · lu %s" % (code, len(jugements), appels)))
        else:
            r.append(("B2 juge seul, lecture jusqu'à la frontière %s : refus, rien joué" % frontiere,
                      code == 1 and "PARTIE DE RÉGLAGE REFUSÉE" in s and not appels and not jugements,
                      "code %s · joué %s" % (code, appels)))
    return r


def cas_c(racine):
    """Cas C : la garde du regard unique et le jeton de réglage, sur des DATES fabriquées. [rend: 1]

    ① RÔLE — Prouver : le réglage des 70 % d'une famille neuve passe la garde ; la bande et les 30 % sont refusés ; le
      jugement des 30 % sans reçu est refusé ; une famille déjà jouée sur 2000-2023 n'obtient pas de jeton.
    ② CONTEXTE D'APPEL — `interne`. ③ ENTRÉE — `racine`. ④ CONDITIONS D'ENTRÉE — le registre porte les deux fiches.
    ⑤ SORTIE — UNE liste de triplets. ⑥ TRAITEMENT — calendrier ouvré fabriqué 2000-01-03 → 2026-10-30, puis les appels.
    ⑦ UNITÉ — Dates. ⑧ POURQUOI — Défaut L1-1 (RELU de Cowork), points 39 et 40 de la file vérifiée du 27-11-2026.
    ⑨ CE QUI CLOCHE — Le calendrier est fabriqué : la frontière réelle d'IND-001 (sur le témoin) diffère d'un mois.
    ⑩ EFFET — Aucun cours lu. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    import datetime as dt
    import JUGE_DES_STRATEGIES as J
    import CONTRATS_DES_FICHIERS as C
    import COMMUN
    M = J.charger_module(J.trouver(racine, "MODULE_JUGEMENT.py"), "jug")
    r = []
    j, cal = dt.date(2000, 1, 3), []
    while j <= dt.date(2026, 10, 30):
        if j.weekday() < 5:
            cal.append(j.isoformat())
        j += dt.timedelta(days=1)
    fiches = C.fiches_du_registre(J.trouver(racine, C.NOM_DU_REGISTRE_DES_STRATEGIES))
    f2, f1 = fiches[FICHE_CAS_2], fiches[FICHE_CAS_1]
    b = (cal[0], cal[-1])
    fr = M.frontiere_de_la_fiche({}, cal, b)
    lim, _l = M.fin_de_la_partie_de_reglage(cal, 20, fr)
    jeton, motif = J.jeton_de_reglage(racine, f2, cal, b, 20, lim, M)
    r.append(("C1 jeton de réglage pour %s jusqu'au %s (frontière %s)" % (FICHE_CAS_2, lim, fr), jeton is not None,
              motif))

    def garde(derniere, recu):
        try:
            J._garde_du_regard_unique(FICHE_CAS_2, cal[0], derniere, (cal[0], derniere), recu)
            return "passe"
        except J.RegardNonInscrit as e:
            return str(e)
    g1 = garde(lim, jeton) if jeton else "pas de jeton"
    r.append(("C2 la garde laisse passer le réglage 2000 → %s avec le jeton" % lim, g1 == "passe", g1[:160]))
    g2 = garde(fr, jeton) if jeton else "pas de jeton"
    r.append(("C3 la garde refuse une lecture jusqu'à la frontière avec le même jeton (déclaration datée)",
              g2 != "passe" and "déclaration datée" in g2, g2[:200]))
    decl = C.declaration_de_la_fiche(racine, FICHE_CAS_2, dt.datetime.now(dt.timezone.utc).isoformat())
    g3 = garde(cal[-1], None)
    r.append(("C4 jugement des 30 %% sans reçu (déclaration datée de %s : %s) : refusé" % (FICHE_CAS_2,
              "absente" if decl is None else "présente"), "sans reçu" in g3, g3[:160]))
    j1, m1 = J.jeton_de_reglage(racine, f1, cal, b, 20, lim, M)
    r.append(("C5 %s, famille déjà jouée sur 2000-2023 : aucun jeton" % FICHE_CAS_1,
              j1 is None and "famille déjà jouée" in (m1 or ""), m1))
    j2, m2 = J.jeton_de_reglage(racine, f2, cal, b, 20, cal[cal.index(lim) + 1], M)
    r.append(("C6 jeton demandé une séance après la limite : refusé", j2 is None and "ni la bande" in (m2 or ""), m2))
    j3, m3 = J.jeton_de_reglage(racine, f2, cal, b, COMMUN.HORIZON_AUCUNE, lim, M)
    r.append(("C7 horizon « aucune » : refusé, largeur non tranchée", j3 is None and "pas tranchée" in (m3 or ""), m3))
    return r


def interne(racine, travail):
    """Joue tous les cas dans ce processus et les écrit en JSON sur la sortie. ① · ② `main` (sous-processus) ·
    ③ `racine`, `travail` · ④ — · ⑤ aucune valeur [rend: rien] · ⑥ A, B, C · ⑦ — · ⑧ un processus neuf par racine : les
    modules d'une racine saboteuse ne se mêlent jamais à ceux de la vraie · ⑨ — · ⑩ écrit sous `travail` ·
    ⑪ rend la main. [sort: non]"""
    os.chdir(racine)
    try:
        r = cas_a_et_b(racine, travail)
    except Exception as e:
        r = [("A/B-interrompus", False, "%s: %s" % (type(e).__name__, e))]
    try:
        r += cas_c(racine)
    except Exception as e:
        r += [("C-interrompu", False, "%s: %s" % (type(e).__name__, e))]
    print("@@RESULTATS@@" + json.dumps(r, ensure_ascii=False, default=str))


def jouer_les_cas(racine, travail):
    """Lance `interne` dans un processus neuf ; rend la liste des cas. [rend: 1] ① · ② `main` · ③ `racine`, `travail`
    · ④ — · ⑤ UNE liste · ⑥ sous-processus borné · ⑦ — · ⑧ — · ⑨ une sortie illisible rend un cas faux · ⑩ lance ·
    ⑪ rend la main (délai 900 s). [sort: non]"""
    os.makedirs(travail, exist_ok=True)
    p = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--interne", racine, travail],
                       capture_output=True, text=True, timeout=900)
    for l in p.stdout.splitlines():
        if l.startswith("@@RESULTATS@@"):
            return [tuple(x) for x in json.loads(l[len("@@RESULTATS@@"):])]
    return [("sortie illisible", False, (p.stdout + p.stderr)[-400:])]


def main(argv):
    """Verdict. ① · ② le bas du fichier · ③ `argv` · ④ — · ⑤ sort avec 0, 1 ou 2 [rend: rien] · ⑥ cas vrais, puis un
    jeu par sabotage sur une racine de liens · ⑦ — · ⑧ instructions §7 · ⑨ — · ⑩ dossier temporaire effacé ·
    ⑪ sort. [sort: oui]"""
    if argv[1:2] == ["--interne"]:
        interne(argv[2], argv[3])
        return 0
    opts = [a for a in argv[1:] if a.startswith("--")]
    pos = [a for a in argv[1:] if not a.startswith("--")]
    if len(pos) != 1 or set(opts) - {"--sans-sabotages"}:
        print(__doc__.split("LE SENS")[0])
        return 2
    source = os.path.abspath(pos[0])
    if os.path.lexists(os.path.join(source, ".git")):
        print("❌ IMPOSSIBLE — %s porte .git : l'épreuve ne tourne que sur une copie" % source)
        return 2
    travail = tempfile.mkdtemp(prefix="partie_de_reglage_")
    rouge = False
    try:
        for nom, ok, detail in jouer_les_cas(source, os.path.join(travail, "vrai")):
            rouge |= not ok
            print("%s %s : %s" % ("✅" if ok else "❌", nom, str(detail)[:300]))
        if rouge or "--sans-sabotages" in opts:
            return 1 if rouge else 0
        for nom, quoi, cible, avant, apres in SABOTAGES:
            texte = open(os.path.join(source, "programmes", cible), encoding="utf-8").read()
            if texte.count(avant) != 1:
                print("❌ IMPOSSIBLE — ancre du sabotage %s trouvée %d fois dans %s" % (nom, texte.count(avant), cible))
                return 2
            # UNE RACINE DE LIENS DURS : de vrais dossiers, un lien dur par fichier (le juge ne suit pas un dossier-lien,
            # et le contrat refuse un module de signal dont le chemin réel sort de la racine : deux mesures du
            # 27-11-2026 sur des liens symboliques) ; le seul programme visé est un vrai fichier, faussé. Repli : copie.
            sab = os.path.join(travail, "racine_" + nom)

            def lier(a, b):
                try:
                    os.link(a, b)
                except OSError:
                    shutil.copy2(a, b)
            shutil.copytree(source, sab, symlinks=True, copy_function=lier)
            os.remove(os.path.join(sab, "programmes", cible))
            open(os.path.join(sab, "programmes", cible), "w", encoding="utf-8").write(texte.replace(avant, apres))
            tombes = [n for n, ok, _ in jouer_les_cas(sab, os.path.join(travail, nom)) if not ok]
            rouge |= not tombes
            print("%s %s %s (%s) → %s" % ("✅" if tombes else "❌", nom, quoi, cible,
                                          "tombe(nt) : " + " · ".join(t.split(" ")[0] for t in tombes) if tombes
                                          else "AUCUN CAS NE TOMBE"))
        return 1 if rouge else 0
    finally:
        shutil.rmtree(travail, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
