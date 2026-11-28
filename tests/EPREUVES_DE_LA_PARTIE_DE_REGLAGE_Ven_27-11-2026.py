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
    # S4 et S5 (27-11-2026) visaient la version « sans délai » NON jouée et sa ligne vide : depuis A-1106 (28-11-2026)
    # elle est jouée et coupée par la purge ; leurs propriétés n'existent plus. Remplacés (lot L1CORR2) par la purge et
    # par le décalage d'un rang de la limite (SN1 de la relecture V1 du 28-11-2026).
    ("S4", "purge de la version « sans délai » retirée", "MODULE_JUGEMENT.py",
     "    if aucune:\n        debut_bande", "    if False:\n        debut_bande"),
    ("S5", "limite décalée d'un rang dans la bande (SN1 de V1)", "MODULE_JUGEMENT.py",
     '    return (cal[c["n_70"] - 1] if c["n_70"] else None), c["embargo_seances"]',
     '    return (cal[c["n_70"]] if c["n_70"] else None), c["embargo_seances"]'),
    ("S6", "jeton de réglage sans contrôle de date", JUGE, "    if str(derniere) > jeton.derniere:", "    if False:"),
    ("S7", "jeton de réglage sans contrôle de famille", JUGE,
     "    if deja:\n        return None, (\"famille", "    if False:\n        return None, (\"famille"),
    ("S8", "N5 h_max annulé par une version « aucune »", JOUER, "    h_max = max(_chiffrees) if _chiffrees else 0\n",
     "    h_max = 0 if _aucunes else max(_chiffrees)\n"),
    ("S9", "garde-fou des opérations hors des 70 % retiré", JOUER, "    if c.get(\"n_30\") or c.get(\"n_ecartes\"):",
     "    if False:"),
    ("S10", "bande de JOUER sans l'horizon (SN2 de V1)", JOUER,
     "    derniere, largeur = mod_jug.fin_de_la_partie_de_reglage(seances_fiche, h_bande, frontiere)",
     "    derniere, largeur = mod_jug.fin_de_la_partie_de_reglage(seances_fiche, 1, frontiere)"),
    ("S11", "garde sans les 30 % de la fiche (L1-1)", JUGE,
     "    dans_les_30 = bool(trente) and", "    dans_les_30 = False and"),
    ("S12", "`jouer` ne passe pas les 30 % de la fiche à la garde", JUGE,
     "periode, recu, trente=_trente)", "periode, recu, trente=None)"),
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
        # UN HORIZON DE 30 (relecture V1 du 28-11-2026, défaut 2) : avec 20 partout, « la bande suit l'horizon le plus
        # long » n'était jamais éprouvée (la bande valait 21 de toute façon)
        if l["id_version"] == TROIS[1]:
            l["horizon"] = "30"
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
    # L'ATTENDU ÉCRIT À LA MAIN, SANS LE MODULE (relecture V1 du 28-11-2026, défaut 1 : la limite attendue venait de la
    # même fonction que le code) : la bande vaut le plus grand de 21 et de l'horizon (A-305 ②) ; la limite est la séance
    # qui précède les « bande » séances retirées avant la frontière, la frontière elle-même étant retirée aussi.
    cal_f = sorted(d for d in seances if bornes[0] <= d <= bornes[1])
    bande_main = max(21, h_max)
    i_f = cal_f.index(frontiere)
    limite_main = cal_f[i_f - bande_main - 1]
    entre = sum(1 for d in cal_f if limite < d < frontiere) if limite else -1
    r.append(("A0 limite (bande %d, horizon %d) = attendu écrit à la main %s, %d séances entre elle et la frontière"
              % (largeur, h_max, limite_main, bande_main),
              limite == limite_main and largeur == bande_main and entre == bande_main, (limite, frontiere, entre)))
    # A0b UN CAS RÉEL DE DATES, RELEVÉ LE 28-11-2026 SUR LE MAÎTRE (bornes figées de la fiche, 2024-01-02 → 2026-07-10) :
    # frontière 2025-10-06 ; horizon 20 → bande 21, dernière séance lue 2025-09-04 (recompte de Cowork, RELU de L1CORR,
    # R4 : « 21 séances strictement entre 2025-09-04 et 2025-10-06 ») ; horizon 30 → bande 30.
    l20, b20 = M.fin_de_la_partie_de_reglage(cal_f, 20, frontiere)
    l30, b30 = M.fin_de_la_partie_de_reglage(cal_f, 30, frontiere)
    la, ba = M.fin_de_la_partie_de_reglage(cal_f, COMMUN.HORIZON_AUCUNE, frontiere)
    r.append(("A0b dates réelles : frontière 2025-10-06, horizon 20 → 2025-09-04 (21), « aucune » → 2025-09-04 (21), "
              "horizon 30 → %s (30)" % cal_f[cal_f.index("2025-10-06") - 31],
              frontiere == "2025-10-06" and (l20, b20) == ("2025-09-04", 21) and (la, ba) == ("2025-09-04", 21)
              and (l30, b30) == (cal_f[cal_f.index("2025-10-06") - 31], 30), (frontiere, l20, la, l30)))
    # A8 LA PURGE (A-1106), sur des opérations fabriquées, attendu à la main : bande de 21 avant la frontière ; seule
    # l'opération refermée avant la bande reste dans les 70 %.
    cf = ["2030-%02d-%02d" % (1 + i // 28, 1 + i % 28) for i in range(84)]
    o_ok = {"date_signal": cf[2], "date_sortie": cf[10], "net": 1.0, "motif": "TP"}
    o_bande = {"date_signal": cf[3], "date_sortie": cf[40], "net": -5.0, "motif": "SL"}      # refermée dans la bande
    o_ouverte = {"date_signal": cf[4], "date_sortie": cf[83], "net": 2.0, "motif": COMMUN.MOTIF_FIN_DES_DONNEES}
    o_30 = {"date_signal": cf[61], "date_sortie": cf[65], "net": 3.0, "motif": "TP"}
    c8 = M.coupure_70_30([o_ok, o_bande, o_ouverte, o_30], cf, horizon=COMMUN.HORIZON_AUCUNE, frontiere=cf[60])
    r.append(("A8 purge « sans délai » : 1 opération gardée dans les 70 %, 2 purgées, embargo 21, 1 dans les 30 %",
              (c8["n_70"], c8["n_purgees"], c8["embargo_seances"], c8["n_30"], c8["res_70"]["n"]) == (1, 2, 21, 1, 1),
              {k: c8.get(k) for k in ("n_70", "n_purgees", "embargo_seances", "n_30")}))
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
    r.append(("A3 la version « aucune » est jouée (A-1106) : sa ligne porte ses chiffres, embargo 21, fin ≤ limite",
              len(aucune) == 1 and any(v["horizon"] == "aucune" for v in vus)
              and aucune[0]["operations"] != "" and aucune[0]["embargo_seances"] == "21"
              and aucune[0]["operations"] == aucune[0]["operations_70"] and aucune[0]["periode_fin"] <= limite,
              [{k: aucune[0][k] for k in ("operations", "operations_70", "embargo_seances", "periode_fin")}]
              if aucune else []))
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
    r.append(("A6 le tri accepte le fichier (ligne « aucune » jouée)", vu_t == "accepté", vu_t[:200]))
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
    r.append(("C7 horizon « aucune » : jeton accordé jusqu'à la même limite (bande 21, A-1106)", j3 is not None, m3))
    # L1-1 TRANCHÉ (A-777, A-853, A-1073) : sans jeton, la garde protège aussi les 30 % DE LA FICHE du cas 2
    t2, t1 = J.trente_pour_cent_de_la_fiche(f2, racine), J.trente_pour_cent_de_la_fiche(f1, racine)
    try:
        J._garde_du_regard_unique(FICHE_CAS_2, "2024-01-02", "2024-06-28", ("2024-01-02", "2024-06-28"), None, trente=t2)
        g8 = "passe"
    except J.RegardNonInscrit as e:
        g8 = str(e)
    r.append(("C8 %s jouée sur 2024 sans reçu ni jeton (30 %% de la fiche %s) : refusée" % (FICHE_CAS_2, t2),
              t2 is not None and t2[0] < "2024-01-02" and "dans les 30 %" in g8 and "sans reçu" in g8, g8[:200]))
    try:
        J._garde_du_regard_unique(FICHE_CAS_1, "2024-01-02", "2026-07-10", ("2024-01-02", "2026-07-10"), None, trente=t1)
        g9 = "passe"
    except J.RegardNonInscrit as e:
        g9 = str(e)
    r.append(("C9 %s (cas 1, 2024-2026) sans reçu : la garde passe, comme avant" % FICHE_CAS_1,
              t1 is None and g9 == "passe", g9[:160]))
    # C10 `jouer` passe les 30 % de la fiche à la garde (le jeu réel d'IND-001 sans reçu, avant tout signal)
    mnemo = J.table_mnemoniques(J.trouver(racine, "REFERENTIEL_VALEURS"))
    lus, _l = J.lire_par_le_lecteur(racine, os.path.join("donnees", "cours_maitre.csv"), mnemo)
    court = {v: [x for x in s_ if x["date"] <= "2024-06-28"] for v, s_ in lus.items()}
    try:
        _pos = J.charger_module(J.trouver(racine, "MODULE_POSITIONS"), "pos_c10")
        J.jouer(dict(f2), court, mnemo, None, _pos, periode=("2024-01-02", "2024-06-28"))
        g10 = "joué"
    except J.RegardNonInscrit as e:
        g10 = str(e)
    except Exception as e:      # noqa: BLE001 — une autre chute dit que la garde n'a pas arrêté avant le signal
        g10 = "autre chute : %s: %s" % (type(e).__name__, e)
    r.append(("C10 `jouer` d'%s sur 2024 sans reçu : arrêté par la garde des 30 %% de la fiche" % FICHE_CAS_2,
              "dans les 30 %" in g10, g10[:200]))
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
