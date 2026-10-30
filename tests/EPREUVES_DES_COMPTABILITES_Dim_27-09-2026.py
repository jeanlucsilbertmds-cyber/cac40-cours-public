"""EPREUVES_DES_COMPTABILITES — Dim 27-09-2026 (Paris)
DÉCIDÉ · Rôle : garder au dépôt la réparation du défaut 3 (A-493), et prouver que chaque épreuve a des dents.
Quand l'appeler : avant toute livraison qui touche le teneur, la mesure, le cockpit, le radar ou le contrat des fichiers (R-755 ②).

À QUOI ÇA SERT : garder, au dépôt, la réparation du défaut 3 de A-491 (BACKLOG A-493). Le journal
des trades n'avait pas de colonne « comptabilite » : la vente d'Unibail du 27-08, écrite une fois
en « un jeton » et une fois en « jetons illimités », était comptée dans les deux — la mesure
affichait « un jeton : 3 operation(s) · cumul 1292.25 EUR » pour un seul trade à −2 796,25 €.
Déposé au dépôt sur la relecture de Cowork du 27-09-2026 à 22h46 : ces épreuves ne vivaient que
dans l'espace du Chat, et quand il a remis le défaut dans la mesure, tout ce qui était au dépôt
est resté vert.

CE QUI TOURNE CHAQUE SOIR, SANS CE FICHIER : ① le calibrage de la mesure rejoue, par
`mesurer_une_strategie` — le chemin même de `main` —, un témoin FIGÉ (`_TEMOIN_JOURNAL` : cinq vraies
lignes du 27-09-2026, deux fabriquées) et s'arrête en code 1 sur un écart ; ② sur le vrai journal, la
mesure s'arrête si une ligne n'a pas de comptabilité reconnue, et si, pour une stratégie, les
opérations écrites dans ses deux comptabilités ne font pas le nombre de ses lignes ; ③ le radar rejoue
son témoin du maillon 13 par le chemin même qui écrit son rapport (séries, alarmes, passage en ✅ ou
❌) et contrôle que les trades sont rattachés aux identifiants du registre (❌
critiques ; le radar sort toujours en code 0 : ils se lisent dans rapports/audit_du_jour.md) ; ④ le
calibrage du teneur éprouve `fautes_d_ecriture`. Limites : un argument remplacé dans l'appel final
d'un calcul, ou la dernière ligne qui écrit au rapport, échappe à ces contrôles du soir — ce fichier-ci
le voit ; et la vérification du total de la mesure ne voit pas une ligne comptée dans la mauvaise
comptabilité — seul le témoin du calibrage la voit. Ce fichier-ci éprouve en plus le circuit de
bout en bout, et PROUVE QUE CHAQUE ÉPREUVE A DES DENTS : chaque sabotage retire une protection,
et au moins une épreuve doit alors rougir (R-731).

USAGE : python3 tests/EPREUVES_DES_COMPTABILITES_Dim_27-09-2026.py <racine du dépôt> [--saboter | nom]
  sans option : les épreuves sur le dépôt intact (Z0), environ une minute ;
  --saboter : Z0, puis chaque sabotage, environ dix minutes ; un nom : ce seul sabotage.
CODE : 0 si Z0 et V1 sont tout verts et que chaque sabotage fait rougir au moins une épreuve ; 1 sinon.
Chaque épreuve travaille sur une COPIE temporaire ; le dépôt n'est jamais touché.
Simulation uniquement.
"""
import csv, glob, os, re, shutil, subprocess, sys, tempfile
_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
ARCH = "archives/claude_journal_trades_SANS_COLONNE_COMPTABILITE_27-09-2026_voir_A-491.csv"
# LE JOURNAL TÉMOIN FIGÉ : le vrai journal des trades tel qu'il était du 27-09 au 20-10-2026 (commit 7083c48), sur
# lequel ces chiffres ont été calibrés. Chaque copie le pose à la place du vrai journal, que le circuit du soir fait
# grandir : depuis le premier trade Vinci clos, le 20-10-2026, l'épreuve rougissait sans défaut du programme
# (superviseur R-759 du 25-10-2026). Seuls E3b et E3c lisent encore le vrai journal : ils jugent des propriétés.
TEMOIN = "temoins/TEMOIN_claude_journal_trades_DU_27-09-2026_JEU_DES_COMPTABILITES.csv"
# LE REGISTRE TÉMOIN FIGÉ : `donnees/cac40_strategies.csv` tel qu'il est depuis le 10-10-2026 (commit c021921). Un horizon
# changé au registre vivant suffisait à refermer la position mal écrite de E10 et à lui ôter ses dents (second
# superviseur R-759 du 25-10-2026, mesuré avec l'horizon d'OBS à une séance). Avec le journal témoin et les cours coupés,
# c'est TOUT le jeu de données des cas qui font tourner le teneur qui est figé ; E3b et E3c restent sur le vivant.
REGISTRE_TEMOIN = "temoins/TEMOIN_cac40_strategies_DU_10-10-2026_JEU_DES_COMPTABILITES.csv"
TEN, MES = "programmes/TENIR_LES_POSITIONS.py", "programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py"
CON, COK = "programmes/CONTRATS_DES_FICHIERS.py", "programmes/GENERATEUR_COCKPIT_Sam_15-08-2026_21h50.py"
AUD = "programmes/audit_ecosysteme.py"

SABOTAGES = {
 "Z0": [],
 "S1_contrat_sans_comptabilite": [(CON, '"pnl_net_convention_eur", "comptabilite",', '"pnl_net_convention_eur",')],
 "S2_ecriture_sans_controle": [(TEN, "    if fautes:\n        print(f\"  ❌", "    if False:\n        print(f\"  ❌"),
                               (TEN, "_ecrire_csv(f_jou, journal + r[\"trades\"], TRADE)",
                                "_ecrire_csv(f_jou, journal + r[\"trades\"], list(journal[0].keys()) if journal else TRADE)")],
 "S3_comptabilite_non_verifiee": [(TEN, 'if "comptabilite" in l and l.get("comptabilite") not in COMPTABILITES:', 'if False:')],
 "S4_mesure_sans_filtre": [(MES, "and (comptabilite is None or o.get('comptabilite') == comptabilite)]", "]")],
 "S5_mesure_par_morceau": [(MES, "return [o for o in operations if (o.get('strategie') or '').strip() in noms",
                            "return [o for o in operations if any(_norm(o.get('strategie') or '') in _norm(n) for n in noms)")],
 "S6_mesure_sans_arret": [(MES, "    if sans:\n        print(f\"ARRET", "    if False:\n        print(f\"ARRET")],
 "S7_cockpit_sans_comptabilite": [(COK, '{esc((t.get("comptabilite") or "NON DITE").replace("_", " "))}', '')],
 "S8_mesure_sans_alerte_orpheline": [(MES, "    if orphelines:\n", "    if False:\n")],
 "S9_positions_sans_controle": [(TEN, 'fautes += fautes_d_ecriture(r["positions"], POSITION, "positions ouvertes")', 'pass')],
 "S10_appariement_non_note": [(MES, "        apparies.update(id(o) for o in ops)\n", "")],
 "S11_radar_tout_ensemble": [(AUD, '_cle = (vers_id.get(_nom, _nom), (t.get("comptabilite") or "NON DITE").strip())', '_cle = ("tout", "tout")')],
 "S12_radar_sans_noms_du_registre": [(AUD, '_cle = (vers_id.get(_nom, _nom),', '_cle = (_nom,')],
 "S13_radar_ordre_du_fichier": [(AUD, 'for t in sorted(lignes, key=lambda x: (x.get("date_sortie") or "")):', 'for t in lignes:')],
 "S14_radar_creux_nul": [(AUD, "rendu[_k] = (serie, pic - eq, pic, eq, creux)", "rendu[_k] = (serie, 0.0, pic, eq, creux)")],
 "S15_radar_serie_jamais_remise": [(AUD, "serie = serie + 1 if p <= 0 else 0", "serie = serie + 1 if p <= 0 else serie")],
 "S16_radar_contrat_non_protege": [(AUD, "    except Exception as _e:\n        rapport.append((WARN, \"13-Creux\", \"CONTRATS_DES_FICHIERS illisible \"",
                                     "    except ZeroDivisionError as _e:\n        rapport.append((WARN, \"13-Creux\", \"CONTRATS_DES_FICHIERS illisible \"")],
 "S17_radar_tout_le_registre": [(AUD, "        for _l in (_serv3 or []):\n            for _n in _noms_de_la_strategie(_l):", "        for _l in (_s3 or []):\n            for _n in _noms_de_la_strategie(_l):")],
 "S18_radar_nom_partage_garde": [(AUD, "            del _vers_id[_n]\n", "            pass\n")],
 "S19_radar_nom_partage_tu": [(AUD, "        if _ambigus:\n            rapport.append", "        if False:\n            rapport.append")],
 "S20_mesure_nom_partage_tu": [(MES, "        if len(_ids) > 1:\n", "        if False:\n")],
 "S21_mesure_alerte_sur_tout_nom": [(MES, "        if len(_ids) > 1:\n", "        if len(_ids) > 0:\n")],
 "S22_mesure_sans_propriete_ecrite": [(MES, "        if _n_ecrit != _n_lignes:\n", "        if False:\n")],
 "S23_radar_rattachement_tu": [(AUD, "    check(\"13-Creux\", _ids_attendus <= _ids_vus,", "    check(\"13-Creux\", True,")],
 "S24_radar_alarme_creux_morte": [(AUD, "rendu.append((creux_actuel <= SEUIL_CREUX,", "rendu.append((True,")],
 "S25_radar_verdict_force": [(AUD, "            if _cond:\n                rendu.append((OK, _ok_txt, \"ok\"))", "            if True:\n                rendu.append((OK, _ok_txt, \"ok\"))")],
 "S26_radar_critique_ignore": [(AUD, "rendu.append((FAIL, _ko_txt, \"fail\") if _crit else", "rendu.append((WARN, _ko_txt, \"warn\") if _crit else")],
}
# ce sabotage-la doit rester VERT : l'ordre de la liste des comptabilites ne compte plus
VERTS = {"V1_ordre_des_comptabilites_inverse": [(CON, "COMPTABILITES = (UN_JETON, JETONS_ILLIMITES)", "COMPTABILITES = (JETONS_ILLIMITES, UN_JETON)")]}
SABOTAGES.update(VERTS)

def copie(sab, vivant=False):
    d = tempfile.mkdtemp(prefix="d3_")
    shutil.copytree(DEPOT, d, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git", "_site_travail", "__pycache__"))
    if not vivant:
        shutil.copyfile(os.path.join(d, TEMOIN), os.path.join(d, "donnees/claude_journal_trades.csv"))
        etiqueter_le_temoin(d)
        shutil.copyfile(os.path.join(d, REGISTRE_TEMOIN), os.path.join(d, "donnees/cac40_strategies.csv"))
        couper_les_cours(d, DERNIERE_SEANCE_DU_JEU)
    for f, a, b in SABOTAGES[sab]:
        p = os.path.join(d, f); t = open(p, encoding="utf-8").read()
        assert t.count(a) == 1, (sab, f, a[:50]); open(p, "w", encoding="utf-8").write(t.replace(a, b))
    return d

def etiqueter_le_temoin(d):
    """Pose sur le journal témoin (figé le 27-09-2026, treize colonnes) le barème de chaque montant (A-550).

    Depuis le 29-10-2026, le contrat du journal des trades porte deux colonnes de plus, `bareme_reel` et
    `bareme_convention` : le nom de la ligne de donnees/BAREME_FRAIS.csv qui a produit chaque montant (ÉTUDE 18,
    A1bis), et le teneur de positions refuse d'écrire un journal sans elles. Le témoin, figé, ne change pas : sa
    COPIE installée dans le dossier d'épreuve reçoit les étiquettes de la règle A1bis, celles du vrai journal —
    « HIST_FORFAIT_300 » pour le montant réel de Bureau Veritas du 27-07-2026 (+6 884,75 €, ancien forfait),
    « HIST_COURTAGE_SANS_TTF » pour tous les autres montants. Aucun montant n'est réécrit.
    """
    p = os.path.join(d, "donnees/claude_journal_trades.csv")
    with open(p, encoding="utf-8", newline="") as fh:
        r = csv.DictReader(fh)
        champs = list(r.fieldnames) + ["bareme_reel", "bareme_convention"]
        lignes = list(r)
    for l in lignes:
        bv = (l["valeur"], l["date_entree"]) == ("BUREAU_VERITAS", "2026-07-27")
        l["bareme_reel"] = "HIST_FORFAIT_300" if bv else "HIST_COURTAGE_SANS_TTF"
        l["bareme_convention"] = "HIST_COURTAGE_SANS_TTF"
    with open(p, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=champs)
        w.writeheader()
        w.writerows(lignes)

def run(d, *args):
    r = subprocess.run([sys.executable, *args], cwd=d, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr

# LA DERNIÈRE SÉANCE DU JEU DE L'ÉPREUVE, le jour où elle a été écrite (27-09-2026) : chaque copie qui n'est pas
# « vivante » coupe les cours après elle. Sans cela, la position mal écrite de E10 se referme sur les séances suivantes, son trade entre au journal,
# et c'est le contrôle du journal qui la refuse : le sabotage S9 (positions sans contrôle) n'était plus vu (mesuré le
# 25-10-2026 : clôture le 2026-10-22, refus par « journal des trades, ligne 6 … INCONNUE »).
DERNIERE_SEANCE_DU_JEU = "2026-09-25"

def couper_les_cours(d, jusqu_a):
    p = os.path.join(d, "donnees/cours_maitre.csv")
    with open(p, encoding="utf-8", newline="") as fh:
        lignes = list(csv.reader(fh))
    with open(p, "w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerows([lignes[0]] + [l for l in lignes[1:] if l[1] <= jusqu_a])

def journal(d):
    return list(csv.DictReader(open(os.path.join(d, "donnees/claude_journal_trades.csv"), encoding="utf-8-sig")))

def poser_positions(d):
    sys.path.insert(0, os.path.join(d, "programmes"))
    pos = [dict(strategie="C5E10-OBS-V1", valeur="UNIBAIL_RODAMCO", date_signal="2026-08-20", date_entree="2026-08-21",
                prix_entree="103.15", tp="107.276", sl="100.57125", horizon_fin="2026-09-18", statut="OUVERTE",
                comptabilite=c, regles_pre_trade="", explication="epreuve") for c in ("un_jeton", "jetons_illimites")]
    col = ["strategie", "valeur", "date_signal", "date_entree", "prix_entree", "tp", "sl", "horizon_fin",
           "statut", "comptabilite", "regles_pre_trade", "explication"]
    with open(os.path.join(d, "donnees/claude_positions_ouvertes.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=col); w.writeheader(); w.writerows(pos)

def mesure_lignes(out):
    return {(m[0], m[1]): (int(m[2]), m[3]) for m in
            re.findall(r"(C5E10-\w+-V1) · (un jeton|jetons illimites) : (\d+) operation\(s\) · cumul (\S+) EUR", out)}

def epreuves(sab):
    res = []
    def dire(nom, ok, detail=""):
        res.append((nom, ok, detail))
    # E1 calibrage du teneur
    d = copie(sab); c, o = run(d, TEN, d, "--calibrage")
    dire("E1 calibrage du teneur OK", c == 0 and "CALIBRAGE OK" in o, o.strip().splitlines()[-1] if o.strip() else "")
    # E2 contrat : le journal migre respecte son contrat
    c, o = run(d, "-c", "import sys;sys.path.insert(0,'programmes');import CONTRATS_DES_FICHIERS as c;"
                      "e=[x for x in c.confronter_tous('.') if 'journal_trades' in x];print(e);sys.exit(1 if e else 0)")
    dire("E2 journal conforme au contrat", c == 0, o.strip()[:120])
    # E3 mesure sur le journal témoin figé : chiffres attendus
    c, o = run(d, MES, d); m = mesure_lignes(o)
    att = {("C5E10-QA-V1", "un jeton"): (1, "-2796.25"), ("C5E10-QA-V1", "jetons illimites"): (1, "-2796.25"),
           ("C5E10-OBS-V1", "un jeton"): (1, "-2796.25"), ("C5E10-OBS-V1", "jetons illimites"): (2, "897.75")}
    dire("E3 mesure du journal témoin = chiffres attendus", c == 0 and m == att, str(m))
    dv = copie(sab, vivant=True); cv, ov = run(dv, MES, dv); shutil.rmtree(dv)
    dire("E3b aucune ligne orpheline sur le vrai journal", "AUCUNE" not in ov, "")
    dire("E3c aucune alerte de nom partage sur le vrai registre", "ALERTE : le nom" not in ov, "")
    # E11 radar : une serie par strategie et comptabilite, rattachee a l'identifiant du registre
    c, o = run(d, AUD, d)
    series = re.findall(r"\[13-Creux\] (\S+) · ([a-z ]+) : série de pertes en cours : (\d+)", o)
    dire("E19 le temoin du soir du radar est retrouve", "✅ [13-Creux] Témoin du maillon 13 retrouvé" in o, "")
    dire("E11 radar : 4 series d'une perte, par identifiant", sorted(series) == sorted(
        [(s, b, "1") for s in ("C5E10-OBS-V1", "C5E10-QA-V1") for b in ("un jeton", "jetons illimites")]), str(series))
    shutil.rmtree(d)
    # E4 de bout en bout : cloture Unibail rejouee, chaque ligne ecrite porte sa comptabilite
    d = copie(sab); poser_positions(d)
    c, o = run(d, TEN, d); j = journal(d)
    neuves = [l for l in j if l["strategie"] == "C5E10-OBS-V1"]
    dire("E4 les clotures du soir portent leur comptabilite", c == 0 and sorted(l.get("comptabilite") for l in neuves)
         == ["jetons_illimites", "un_jeton"], f"code {c} · {[l.get('comptabilite') for l in neuves]}")
    c, o = run(d, MES, d); m = mesure_lignes(o)
    # la cloture rejouee se chiffre au bareme reel depuis le 29-10-2026 (A-550) : −3 196,25 € (taxe de 400 € a l'achat
    # d'Unibail), ajoutee a la ligne du temoin (−2 796,25 €, courtage seul) — avant A-550, −5 592,50 €.
    dire("E5 mesure apres rejeu : OBS un jeton 2 ops -5992.50", m.get(("C5E10-OBS-V1", "un jeton")) == (2, "-5992.50"), str(m.get(("C5E10-OBS-V1", "un jeton"))))
    shutil.rmtree(d)
    # E12 radar apres rejeu : les lignes nouvelles (identifiant) et anciennes (nom court) font UNE serie
    d = copie(sab); poser_positions(d); run(d, TEN, d)
    c, o = run(d, AUD, d)
    series = re.findall(r"\[13-Creux\] (\S+) · ([a-z ]+) : série de pertes en cours : (\d+)", o)
    dire("E12 radar apres rejeu : OBS un jeton = 2 pertes, une seule serie", ("C5E10-OBS-V1", "un jeton", "2") in series
         and len(series) == 4, str(series))
    shutil.rmtree(d)
    # E13 radar sur une serie melee de gains, rangee dans le desordre dans le fichier :
    # chronologie 08-27 -2796.25 · 09-10 +5000 · 09-15 -25000 · 09-20 -1000
    # => serie de pertes 2 (remise a zero par le gain), creux en cours 26 000 EUR > 20 % : alarme R-502
    d = copie(sab); p = os.path.join(d, "donnees/claude_journal_trades.csv")
    j = journal(d); base_l = [l for l in j if l["strategie"] == "COURS_BAS_ARGENT_REVIENT_6" and l["comptabilite"] == "un_jeton"][0]
    for ds, v in (("2026-09-20", "-1000.00"), ("2026-09-10", "5000.00"), ("2026-09-15", "-25000.00")):
        j.append(dict(base_l, strategie="C5E10-QA-V1", date_sortie=ds, pnl_net_eur=v))
    with open(p, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(j[0].keys())); w.writeheader(); w.writerows(j)
    c, o = run(d, AUD, d)
    dire("E13 radar : serie 2 apres un gain, dans l'ordre des dates", "C5E10-QA-V1 · un jeton : série de pertes en cours : 2" in o, "")
    dire("E13b radar : creux de 26 000 EUR -> alarme R-502", "❌ [13-Creux] C5E10-QA-V1 · un jeton : SEUIL DE CREUX FRANCHI : 26 000" in o, "")
    shutil.rmtree(d)
    # E14 contrat illisible : le radar le dit et rend son rapport
    d = copie(sab); open(os.path.join(d, CON), "a", encoding="utf-8").write("\ndef (\n")
    c, o = run(d, AUD, d)
    dire("E14 contrat illisible : le radar le dit, rapport complet", "CONTRATS_DES_FICHIERS illisible" in o and o.count("\n") > 50, f"{o.count(chr(10))} lignes")
    shutil.rmtree(d)
    # E15 deux strategies vivantes partagent un nom court : le radar l'ecarte et le dit, la mesure le dit
    d = copie(sab); p = os.path.join(d, "donnees/cac40_strategies.csv")
    reg = list(csv.DictReader(open(p, encoding="utf-8-sig")))
    reg.append(dict([r for r in reg if r["id"] == "C5E10-QA-V1"][0], id="C5E10-QA-V2"))
    with open(p, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(reg[0].keys())); w.writeheader(); w.writerows(reg)
    c, o = run(d, AUD, d)
    series = re.findall(r"\[13-Creux\] (\S+) · ([a-z ]+) : série de pertes en cours : (\d+)", o)
    dire("E15 nom partage : le radar le dit et ne le rattache a aucune", "plusieurs stratégies vivantes" in o
         and "COURS_BAS_ARGENT_REVIENT_6" in [s for s, b, n in series], str(series))
    c, o = run(d, MES, d)
    dire("E15c nom partage : la mesure le dit", "designe 2 strategies vivantes" in o, "")
    shutil.rmtree(d)
    # E16 une ligne ARCHIVEE du registre partage le nom de QA-V1 : seules les vivantes comptent, rien a dire
    d = copie(sab); p = os.path.join(d, "donnees/cac40_strategies.csv")
    reg = list(csv.DictReader(open(p, encoding="utf-8-sig")))
    reg.append(dict([r for r in reg if r["id"] == "C5E10-QA-V1"][0], id="C5E10-QA-V0", etat_vie="ARCHIVEE"))
    with open(p, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(reg[0].keys())); w.writeheader(); w.writerows(reg)
    c, o = run(d, AUD, d)
    series = re.findall(r"\[13-Creux\] (\S+) · ([a-z ]+) : série de pertes en cours : (\d+)", o)
    dire("E16 homonyme archive : QA-V1 garde ses series, aucun avertissement", "plusieurs stratégies vivantes" not in o
         and ("C5E10-QA-V1", "un jeton", "1") in series, str(series))
    shutil.rmtree(d)
    # E17 le sabotage de Cowork (27-09, 22h46), sous la forme qui echappe au calibrage : la
    # boucle de main compte toutes les lignes dans chaque comptabilite -> la mesure s'arrete
    d = copie(sab); p = os.path.join(d, MES); t = open(p, encoding="utf-8").read()
    a = "        for comptabilite, gref, s in mesurer_une_strategie(operations, carte):"
    if t.count(a) == 1:
        open(p, "w", encoding="utf-8").write(t.replace(a, "        for comptabilite, gref, s in "
            "[(l, g, stats(ops, 'pnl_net_eur')) for l, g, _x in mesurer_une_strategie(operations, carte)]:"))
    c, o = run(d, MES, d)
    dire("E17 double compte injecte dans main : la mesure s'arrete", c == 1 and "compte deux fois" in o, f"code {c}")
    shutil.rmtree(d)
    # E18 les noms du registre perdus avant le calcul : le radar le dit (critique)
    d = copie(sab); p = os.path.join(d, AUD); t = open(p, encoding="utf-8").read()
    a = "    _tem += [dict("
    if t.count(a) == 1:
        open(p, "w", encoding="utf-8").write(t.replace(a, "    _vers_id = {}\n" + a))
    c, o = run(d, AUD, d)
    dire("E18 noms du registre perdus : le radar le dit", "❌ [13-Creux] TRADES NON RATTACHÉS" in o, "")
    shutil.rmtree(d)
    # E10 une position au livre mal ecrit : refus PAR LE CONTRÔLE DES POSITIONS, rien d'ecrit (second superviseur
    # R-759 du 25-10-2026 : « INCONNUE » seul pouvait venir du contrôle du journal, si la position se refermait)
    d = copie(sab); poser_positions(d); j_avant = open(os.path.join(d, "donnees/claude_journal_trades.csv"), "rb").read()
    p = os.path.join(d, "donnees/claude_positions_ouvertes.csv"); t = open(p, encoding="utf-8").read()
    t = t.replace("2026-08-20,2026-08-21,103.15,107.276,100.57125,2026-09-18,OUVERTE,un_jeton",
                  "2026-09-23,2026-09-24,103.15,150,50,,OUVERTE,un jeton", 1)
    open(p, "w", encoding="utf-8").write(t); avant = open(p, "rb").read()
    c, o = run(d, TEN, d)
    dire("E10 position au livre mal ecrit : refus par le controle des positions, code 1, rien ecrit", c == 1
         and any("positions ouvertes, ligne" in l and "INCONNUE" in l for l in o.splitlines())
         and open(p, "rb").read() == avant
         and open(os.path.join(d, "donnees/claude_journal_trades.csv"), "rb").read() == j_avant, f"code {c}")
    shutil.rmtree(d)
    # E6 ancien journal (sans colonne) : le teneur refuse d'ecrire, rien ne change
    d = copie(sab); shutil.copyfile(os.path.join(d, ARCH), os.path.join(d, "donnees/claude_journal_trades.csv")); poser_positions(d)
    avant = open(os.path.join(d, "donnees/claude_journal_trades.csv"), "rb").read()
    c, o = run(d, TEN, d)
    apres = open(os.path.join(d, "donnees/claude_journal_trades.csv"), "rb").read()
    dire("E6 journal sans colonne : refus, code 1, journal intact", c == 1 and avant == apres and "ABSENTE" in o, f"code {c}")
    shutil.rmtree(d)
    # E7 une ligne a la comptabilite vide : la mesure s'arrete
    d = copie(sab); p = os.path.join(d, "donnees/claude_journal_trades.csv"); t = open(p, encoding="utf-8").read()
    t = t.replace(",un_jeton,", ",,", 1); open(p, "w", encoding="utf-8").write(t)
    c, o = run(d, MES, d)
    dire("E7 comptabilite vide : la mesure s'arrete (code 1)", c == 1 and "sans comptabilite" in o, f"code {c}")
    shutil.rmtree(d)
    # E8 une ligne au nom inconnu : alerte, comptee nulle part
    d = copie(sab); p = os.path.join(d, "donnees/claude_journal_trades.csv"); t = open(p, encoding="utf-8").read()
    t = t.replace("COURS_BAS_ARGENT_REVIENT_10,BUREAU_VERITAS", "C5-ETENDU-10,BUREAU_VERITAS", 1); open(p, "w", encoding="utf-8").write(t)
    c, o = run(d, MES, d); m = mesure_lignes(o)
    dire("E8 nom inconnu : alerte et compte nulle part", "comptees dans AUCUNE" in o and m.get(("C5E10-OBS-V1", "jetons illimites")) == (1, "-2796.25"), str(m.get(("C5E10-OBS-V1", "jetons illimites"))))
    shutil.rmtree(d)
    # E9 cockpit : la ligne Unibail un jeton de la strategie a 6 est nommee
    d = copie(sab); run(d, "programmes/PUBLIER_LE_SITE.py", d)
    h = "".join(open(f, encoding="utf-8").read() for f in glob.glob(os.path.join(d, "_site_travail/cockpit_*.html")))
    dire("E9 cockpit : strategie et comptabilite affichees", "COURS_BAS_ARGENT_REVIENT_6 · un jeton" in h, "")
    shutil.rmtree(d)
    return res

_choix = (list(SABOTAGES) if "--saboter" in sys.argv else [_args[1]] if len(_args) > 1 else ["Z0"])
_faute = False
for sab in _choix:
    r = epreuves(sab)
    rouges = [x for x in r if not x[1]]
    doit_etre_vert = sab == "Z0" or sab in VERTS
    print(f"== {sab} : {len(r) - len(rouges)} vertes, {len(rouges)} rouges" + (
        "  <-- ATTENDU : 0 rouge" if doit_etre_vert and rouges else "  <-- SABOTAGE NON VU" if not doit_etre_vert and not rouges else ""))
    _faute = _faute or (doit_etre_vert and bool(rouges)) or (not doit_etre_vert and not rouges)
    for nom, ok, det in r:
        if not ok:
            print(f"     ROUGE {nom} · {det}")
print("VERDICT :", "tout est conforme" if not _faute else "ECHEC — voir ci-dessus")
sys.exit(1 if _faute else 0)
