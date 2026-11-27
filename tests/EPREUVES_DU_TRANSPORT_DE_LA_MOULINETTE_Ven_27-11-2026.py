#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_TRANSPORT_DE_LA_MOULINETTE_Ven_27-11-2026.py — Ven 27-11-2026 (Paris). Simulation uniquement.

LE SENS EN TÊTE. Éprouve le TRANSPORT de la moulinette (lot TRANSPORT du plan R505, A-965) : les familles de tranches
de la table des épreuves longues (programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py), leur lecture par le joueur
(tests/outils/jouer_une_epreuve_longue.py) et par l'envoi (programmes/ENVOYER_LES_EPREUVES_SUR_GITHUB.py), et le
centre (programmes/TRANSPORTER_LA_MOULINETTE.py recevoir) de bout en bout : trois machines jouent trois tranches par le
VRAI DECOUPER et le VRAI enchaîneur sur des copies FABRIQUÉES (tests/EPREUVES_LANCER_UNE_STRATEGIE_Mer_25-11-2026.py,
`fabriquer` ; machines et centre de tests/EPREUVES_DE_DECOUPER_LA_MOULINETTE_Ven_27-11-2026.py, importés, R-708 :
fiche factice, cours fabriqués de 2024, doublure de JOUER) ; leurs sorties sont posées sur des branches
epreuves-longues/<passage>/<code> d'un dépôt git LOCAL, comme le circuit les pose au dépôt privé ; le centre les
rapatrie par le VRAI rapatrieur et les reçoit par le VRAI `rassembler`. Aucun cours réel, aucune date d'avant 2024.
Puis des SABOTAGES : chacun doit faire tomber au moins un cas.

USAGE
    python3 -B tests/EPREUVES_DU_TRANSPORT_DE_LA_MOULINETTE_Ven_27-11-2026.py <source> [--sans-sabotages]

① RÔLE — Prouver : une famille se déplie en ses tranches, hors de « toutes » ; une famille mal formée est refusée ; le
  joueur et l'envoi connaissent les tranches et pas la famille ; le centre reçoit les tranches de code 0, écarte une
  tranche TOMBÉE, dit « À REJOUER » avec la ligne d'envoi, termine à 0 avec un second passage, refuse un bloc d'une
  autre chaîne, refuse une copie avec .git et des passages illisibles.
② CONTEXTE D'APPEL — À la main, ou sur GitHub (épreuve longue « TransportMoul »).
③ ENTRÉE — `<source>` : racine d'une copie du dépôt ; `--sans-sabotages` : les cas seulement.
④ CONDITIONS D'ENTRÉE — git installé ; les programmes nommés existent dans la source.
⑤ SORTIE — UNE valeur : 0 tout tient · 1 un cas tombe ou un sabotage ne mord pas · 2 l'épreuve n'a pas pu tourner.
⑥ TRAITEMENT — ① cas T1 à T5 sur la source · ② chaque sabotage : une source faite de liens, le fichier saboté
  réécrit, cas rejoués, au moins un doit tomber · ③ ménage.
⑦ UNITÉ — —
⑧ POURQUOI — R-731, R-732 : T1 lit la VRAIE table (famille MoulEssai) ; T5 joue le vrai DECOUPER.
⑨ CE QUI CLOCHE — Le circuit de GitHub lui-même (relais, matrice, dépôt sur les branches) n'est pas rejoué ici : il
  l'est par le passage réel de la famille MoulEssai (preuve du lot TRANSPORT). La chaîne d'essai (tranche-essai) joue
  la vraie moulinette (environ 60 s) : elle n'est pas rejouée ici, elle l'est sur GitHub.
⑩ EFFET — Écrit sous un dossier de travail, effacé.
⑪ TERMINAISON — Chaque lancement est borné (120 s ; git 60 s). [sort: oui]
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
FAB = "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"
JOUEUR = "tests/outils/jouer_une_epreuve_longue.py"
RAPATRIEUR = "tests/outils/rapatrier_les_epreuves_longues.py"
TRANSPORT = "programmes/TRANSPORTER_LA_MOULINETTE.py"
ENVOI = "programmes/ENVOYER_LES_EPREUVES_SUR_GITHUB.py"
W2F = "tests/EPREUVES_DE_DECOUPER_LA_MOULINETTE_Ven_27-11-2026.py"
LANCEUR = "tests/EPREUVES_LANCER_UNE_STRATEGIE_Mer_25-11-2026.py"
FAM = "Fx"


def charger(chemin, nom):
    """Charge un fichier Python comme module ; rend le module.

    ① RÔLE — Lire les programmes éprouvés par leur chemin. ② CONTEXTE D'APPEL — Les cas. ③ ENTRÉE — `chemin`, `nom`.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe. ⑤ SORTIE — UNE valeur : le module. [rend: 1] ⑥ TRAITEMENT — importlib.
    ⑦ UNITÉ — — ⑧ POURQUOI — Le fichier de la source (ou de la source sabotée), jamais un module d'ailleurs.
    ⑨ CE QUI CLOCHE — Le code de tête s'exécute. ⑩ EFFET — Exécute le fichier. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    spec = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def git(d, *args):
    """Lance git dans `d` ; rend le code. Borné à 60 s.

    ① RÔLE — Fabriquer le dépôt local des sorties. ② CONTEXTE D'APPEL — `deposer`, `racine_git`. ③ ENTRÉE — `d`, les
    arguments. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le code. [rend: 1] ⑥ TRAITEMENT — subprocess, identité
    fixe, sans signature. ⑦ UNITÉ — — ⑧ POURQUOI — Le rapatrieur lit des branches git. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans `d`. ⑪ TERMINAISON — Borné. [sort: non]
    """
    return subprocess.run(["git", "-c", "user.name=epreuve", "-c", "user.email=e@x", "-c", "commit.gpgsign=false"]
                          + list(args), cwd=d, capture_output=True, timeout=60).returncode


def table_avec(source, dest, famille):
    """Écrit dans `dest` la table de la source où les épreuves longues sont remplacées par la seule `famille` (code FAM).

    ① RÔLE — Une table de copie qui porte une famille de l'épreuve. ② CONTEXTE D'APPEL — `les_cas`. ③ ENTRÉE — `source`,
    `dest` (racines), `famille` (dict). ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Rien. [rend: rien] ⑥ TRAITEMENT — JSON lu,
    entrée ajoutée, écrit. ⑦ UNITÉ — — ⑧ POURQUOI — La vraie table, plus une famille de la chaîne factice. ⑨ CE QUI
    CLOCHE — — ⑩ EFFET — Écrit un fichier. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    t = json.load(open(os.path.join(source, "tests/LANCEMENT_DES_EPREUVES.json"), encoding="utf-8"))
    t["epreuves_longues"] = {FAM: famille}   # seule : un refus ne peut venir que d'elle (pas du compte de la table)
    os.makedirs(os.path.join(dest, "tests"), exist_ok=True)
    with open(os.path.join(dest, "tests/LANCEMENT_DES_EPREUVES.json"), "w", encoding="utf-8") as fh:
        json.dump(t, fh, ensure_ascii=False)


def deposer(nu, passage, code, sortie, cs, demande):
    """Pose une sortie de tranche sur la branche epreuves-longues/<passage>/<code> du dépôt nu `nu`.

    ① RÔLE — Imiter le dépôt du circuit (pas « deposer » du gabarit EPREUVES). ② CONTEXTE D'APPEL — `les_cas`.
    ③ ENTRÉE — `nu` : dépôt nu ; `passage`, `code` ; `sortie` : texte de SORTIE.txt ; `cs` : code de sortie ;
    `demande` : la liste des codes du passage. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Rien. [rend: rien] ⑥ TRAITEMENT —
    un dépôt jetable, les trois fichiers sous rapports/epreuves_longues/<passage>/<code>/, poussé. ⑦ UNITÉ — —
    ⑧ POURQUOI — Les noms sont ceux que le rapatrieur lit. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit au dépôt nu.
    ⑪ TERMINAISON — Borné. [sort: non]
    """
    d = tempfile.mkdtemp(prefix="dep_")
    git(d, "init", "-q")
    rel = os.path.join(d, "rapports/epreuves_longues", passage, code)
    os.makedirs(rel)
    open(os.path.join(rel, "SORTIE.txt"), "w", encoding="utf-8").write(sortie)
    json.dump({"code_de_sortie": cs, "chemin": "programmes/DECOUPER_LA_MOULINETTE.py", "arguments": []},
              open(os.path.join(rel, "RESULTAT.json"), "w", encoding="utf-8"))
    json.dump([{"code": c} for c in demande], open(os.path.join(rel, "DEMANDE.json"), "w", encoding="utf-8"))
    git(d, "add", "-A")
    git(d, "commit", "-qm", "sortie")
    git(d, "push", "-q", nu, "HEAD:refs/heads/epreuves-longues/%s/%s" % (passage, code))
    shutil.rmtree(d, ignore_errors=True)


def recevoir(source, prive, copie, passages, nu):
    """Lance TRANSPORTER recevoir ; rend (code, sortie). Borné à 120 s.

    ① RÔLE — Le centre, lancé comme à la main. ② CONTEXTE D'APPEL — `les_cas`. ③ ENTRÉE — `source` (programmes
    éprouvés), `prive` (racine git), `copie`, `passages`, `nu`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — DEUX valeurs.
    [rend: 2] ⑥ TRAITEMENT — subprocess, PRIVE posé. ⑦ UNITÉ — — ⑧ POURQUOI — Son `main` est éprouvé. ⑨ CE QUI CLOCHE —
    — ⑩ EFFET — Celui du centre. ⑪ TERMINAISON — Borné. [sort: non]
    """
    p = subprocess.run([sys.executable, "-B", os.path.join(source, TRANSPORT), "recevoir", copie, FAM] + passages
                       + ["--depuis=" + nu, "--branche=travail-x"], capture_output=True, text=True, timeout=120,
                       env=dict(os.environ, PRIVE=prive))
    return p.returncode, p.stdout + p.stderr


def les_cas(source, travail):
    """Joue T1 à T5 sur la source ; rend [(nom, vrai si tenu, détail)].

    ① RÔLE — Les propriétés du sens en tête. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `source`, `travail`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE liste. [rend: 1] ⑥ TRAITEMENT — Voir chaque cas. ⑦ UNITÉ — —
    ⑧ POURQUOI — R-731. ⑨ CE QUI CLOCHE — En-tête ⑨. ⑩ EFFET — Écrit sous `travail`. ⑪ TERMINAISON — Borné. [sort: non]
    """
    os.makedirs(travail, exist_ok=True)
    r = []
    F = charger(os.path.join(source, FAB), "FAB_T")
    # T1 — la VRAIE table : MoulEssai se déplie en 3, hors de « toutes », et le relais connaît ses tranches
    tr = F.tranches_du_circuit(source)
    simples = [c for c, _, _ in F.epreuves_du_circuit(source)]
    ok = ([t[0] for t in tr if t[3] == "MoulEssai"] == ["MoulEssaiT0", "MoulEssaiT1", "MoulEssaiT2"]
          and [t[2] for t in tr if t[0] == "MoulEssaiT1"] == [["tranche-essai", "{copie}", "1", "3"]]
          and not any(c.startswith("MoulEssai") for c in simples) and "MoulEssaiT2" in F.RELAIS)
    r.append(("T1 famille réelle dépliée, hors de toutes, connue du relais", ok, "%d tranches" % len(tr)))
    # T2 — familles mal formées refusées
    base = {"chemin": "programmes/DECOUPER_LA_MOULINETTE.py", "pourquoi": "épreuve"}
    mauvaises = {"tranches=1": dict(base, arguments=["t", "{copie}", "{k}", "{n}"], tranches=1),
                 "tranches booléen": dict(base, arguments=["t", "{copie}", "{k}", "{n}"], tranches=True),
                 "{n} absent": dict(base, arguments=["t", "{copie}", "{k}"], tranches=3),
                 "{k} sans famille": dict(base, arguments=["t", "{copie}", "{k}"])}
    refus = []
    for nom, e in mauvaises.items():
        d = os.path.join(travail, "t2_" + str(len(refus)))
        table_avec(source, d, e)
        try:
            F.tranches_du_circuit(d)
            refus.append("%s ACCEPTÉE" % nom)
        except ValueError:
            pass
    d = os.path.join(travail, "t2_collision")
    table_avec(source, d, dict(base, arguments=["t", "{copie}", "{k}", "{n}"], tranches=3))
    t = json.load(open(os.path.join(d, "tests/LANCEMENT_DES_EPREUVES.json"), encoding="utf-8"))
    t["epreuves_longues"]["fxt1"] = dict(base, arguments=["{copie}"])
    json.dump(t, open(os.path.join(d, "tests/LANCEMENT_DES_EPREUVES.json"), "w", encoding="utf-8"))
    try:
        F.tranches_du_circuit(d)
        refus.append("collision ACCEPTÉE")
    except ValueError:
        pass
    r.append(("T2 familles mal formées refusées", not refus, " · ".join(refus) or "5 refus"))
    # T3 — le joueur : tranches connues, famille inconnue, « toutes » = les simples
    J = charger(os.path.join(source, JOUEUR), "JOUEUR_T")
    try:
        m = [x["code"] for x in J.lire_la_liste(source, "MoulEssaiT0,MoulEssaiT2")]
        toutes = len(J.lire_la_liste(source, "toutes"))
        try:
            J.lire_la_liste(source, "MoulEssai")
            fam = "ACCEPTÉE"
        except ValueError:
            fam = "refusée"
        ok = m == ["MoulEssaiT0", "MoulEssaiT2"] and toutes == len(simples) and fam == "refusée"
        r.append(("T3 joueur", ok, "%s · toutes %d · famille %s" % (m, toutes, fam)))
    except Exception as e:   # noqa: BLE001
        r.append(("T3 joueur", False, "%s : %s" % (type(e).__name__, e)))
    # T4 — l'envoi : codes de tranche connus, famille et tranche hors découpage inconnues
    try:
        ENV = charger(os.path.join(source, ENVOI), "ENVOI_T")
        inc = ENV.codes_inconnus(source, ["MoulEssaiT1", "MoulEssaiT3", "MoulEssai", "ChronoEssai"])
        r.append(("T4 envoi", inc == ["MoulEssaiT3", "MoulEssai"], "inconnus %s" % inc))
    except Exception as e:   # noqa: BLE001
        r.append(("T4 envoi", False, "%s : %s" % (type(e).__name__, e)))
    # T5 — le centre de bout en bout
    W = charger(os.path.join(source, W2F), "W2F_T")
    W.L = charger(os.path.join(source, LANCEUR), "LANCEUR_T")
    pd = os.path.join(source, "programmes")
    W.L.SOURCE_DES_PROGRAMMES = pd
    fam = dict(base, arguments=["tranche", "{copie}", W.L.SID, W.L.ESSAI, "{k}", "{n}"], tranches=3)

    def centre(nom):
        c = W.centre(pd, travail, nom)
        os.makedirs(os.path.join(c, "programmes"), exist_ok=True)
        for f in ("FABRIQUER_LE_CIRCUIT_PUBLIC.py", "FORME_D_UN_JETON.py"):
            shutil.copyfile(os.path.join(source, "programmes", f), os.path.join(c, "programmes", f))
        table_avec(source, c, fam)
        return c
    prive = os.path.join(travail, "prive")
    os.makedirs(os.path.join(prive, "tests/outils"))
    os.makedirs(os.path.join(prive, "programmes"))
    for f in (RAPATRIEUR, FAB, "programmes/FORME_D_UN_JETON.py"):
        shutil.copyfile(os.path.join(source, f), os.path.join(prive, f))
    table_avec(source, prive, fam)
    git(prive, "init", "-q")
    nu = os.path.join(travail, "nu.git")
    git(travail, "init", "-q", "--bare", nu)
    codes = ["FxT0", "FxT1", "FxT2"]
    sorties = {}
    for k in range(3):
        code, chemin = W.machine(pd, travail, "m%d" % k, k)
        sorties[k] = open(chemin, encoding="utf-8").read() if code == 0 else ""
    deposer(nu, "101", "FxT0", sorties[0], 0, codes[:3])
    deposer(nu, "101", "FxT1", sorties[1], 124, codes[:3])          # TOMBÉE : bloc présent, code 124
    deposer(nu, "101", "FxT2", sorties[2], 0, codes[:3])
    deposer(nu, "102", "FxT1", sorties[1], 0, ["FxT1"])
    c1 = centre("c1")
    code, out = recevoir(source, prive, c1, ["101"], nu)
    r.append(("T5a une tombée → À REJOUER 1, code 3", code == 3 and "TOMBÉE : FxT1" in out and "À REJOUER : 1 " in out
              and "envoyer travail-x Fx 1" in out, "code %d" % code))
    code, out = recevoir(source, prive, c1, ["102"], nu)
    r.append(("T5b reprise par un second passage → code 0", code == 0 and "TOUTES LES TRANCHES" in out, "code %d" % code))
    c2 = centre("c2")
    code, out = recevoir(source, prive, c2, ["101", "102"], nu)
    r.append(("T5c deux passages d'un coup → code 0", code == 0, "code %d" % code))
    autre = os.path.join(travail, "m0.txt")   # la sortie VRAIE de la tranche 0, dont un témoin est changé
    # une autre chaîne : témoin des réglages changé dans le bloc
    W.changer_un_bloc(autre, autre + ".x", lambda b: b["temoins"].__setitem__("0-variables-validees", "0" * 64))
    deposer(nu, "103", "FxT0", open(autre + ".x", encoding="utf-8").read(), 0, ["FxT0"])
    c3 = centre("c3")
    code, out = recevoir(source, prive, c3, ["103"], nu)
    r.append(("T5d bloc d'une autre chaîne refusé, rien écrit", code == 1 and "autre chaîne" in out
              and not os.path.exists(os.path.join(c3, W.L.CH, "e2", "tranche_0.csv")), "code %d" % code))
    code, out = recevoir(source, prive, c3, ["999"], nu)
    r.append(("T5e passage illisible → 2", code == 2, "code %d" % code))
    os.makedirs(os.path.join(c3, ".git"))
    code, out = recevoir(source, prive, c3, ["101"], nu)
    r.append(("T5f copie avec .git → 2", code == 2, "code %d" % code))
    return r


# (nom, fichier, texte, remplacement) : chaque sabotage retire une propriété éprouvée
SABOTAGES = [
    ("S1_tombee_acceptee", TRANSPORT, "if cs == 0 and os.path", "if os.path"),
    ("S2_sans_ligne_de_reprise", TRANSPORT, "if code == 3:\n        print(\"POUR", "if False:\n        print(\"POUR"),
    ("S3_passage_illisible_tu", TRANSPORT, "    if not lus:\n", "    if False:\n"),
    ("S4_famille_comme_simple", FAB, "        if tranches is None:\n            rendu.append",
     "        if True:\n            rendu.append"),
    ("S5_n_non_exige", FAB, 'or arguments.count("{n}") != 1', 'or False'),
    ("S6_joueur_sans_tranches", JOUEUR, "    table = F.epreuves_jouables(racine)\n",
     "    table = {c: (ch, a) for c, ch, a in F.epreuves_du_circuit(racine)}\n"),
    ("S7_envoi_sans_tranches", ENVOI, 'if hasattr(F, "epreuves_jouables"):', 'if False:'),
    ("S8_chaine_inversee", "programmes/DECOUPER_LA_MOULINETTE.py", "return a[2], a[3]", "return a[3], a[2]"),
    ("S9_collision_permise", FAB, "            if t.lower() in vus:\n", "            if False:\n"),
]


def source_sabotee(source, dest, fichier, avant, apres):
    """Fabrique une source faite de liens, où `fichier` est remplacé par son texte saboté ; rend `dest` ou None.

    ① RÔLE — Rejouer les cas sur un programme privé d'une propriété. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `source`,
    `dest`, `fichier` (relatif), `avant`, `apres`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : `dest`, ou None si
    l'ancre n'est pas trouvée exactement une fois. [rend: 1] ⑥ TRAITEMENT — liens pour chaque entrée de la racine,
    copies des fichiers de programmes/, tests/ et tests/outils/ (le joueur refuse un lien) ; le fichier saboté écrit. ⑦ UNITÉ — — ⑧ POURQUOI — La source n'est jamais
    modifiée. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit sous `dest`. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    texte = open(os.path.join(source, fichier), encoding="utf-8").read()
    if texte.count(avant) != 1:
        return None
    reels = {"", "programmes", "tests", "tests/outils"}
    for d in sorted(reels):
        os.makedirs(os.path.join(dest, d), exist_ok=True)
        for f in os.listdir(os.path.join(source, d)):
            rel = os.path.join(d, f) if d else f
            if rel in reels or rel == fichier:
                continue
            if d and os.path.isfile(os.path.join(source, rel)):   # le joueur refuse un programme lancé qui est un lien
                shutil.copyfile(os.path.join(source, rel), os.path.join(dest, rel))
            else:
                os.symlink(os.path.join(source, rel), os.path.join(dest, rel))
    with open(os.path.join(dest, fichier), "w", encoding="utf-8") as fh:
        fh.write(texte.replace(avant, apres))
    return dest


def main(argv):
    """La ligne de commande ; rend le code de sortie.

    ① RÔLE — En-tête. ② CONTEXTE D'APPEL — `__main__`. ③ ENTRÉE — `argv`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE
    valeur : 0, 1 ou 2. [rend: 1] ⑥ TRAITEMENT — cas ; sabotages ; ménage. ⑦ UNITÉ — — ⑧ POURQUOI — R-731, R-734.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Dossier de travail effacé. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    pos = [a for a in argv[1:] if not a.startswith("--")]
    opts = [a for a in argv[1:] if a.startswith("--")]
    if len(pos) != 1 or set(opts) - {"--sans-sabotages"}:
        print("usage : %s <source> [--sans-sabotages]" % argv[0])
        return 2
    source = os.path.abspath(pos[0])
    if not all(os.path.isfile(os.path.join(source, f)) for f in (FAB, JOUEUR, RAPATRIEUR, TRANSPORT, ENVOI, W2F, LANCEUR)):
        print("❌ IMPOSSIBLE — un programme éprouvé manque dans %s" % source)
        return 2
    travail = tempfile.mkdtemp(prefix="transport_", dir="/dev/shm" if os.path.isdir("/dev/shm") else None)
    rouge = False
    try:
        try:
            cas = les_cas(source, os.path.join(travail, "vrai"))
        except Exception as e:   # noqa: BLE001
            print("❌ IMPOSSIBLE — les cas n'ont pas pu tourner : %s : %s" % (type(e).__name__, e))
            return 2
        for nom, ok, detail in cas:
            print("%s %s : %s" % ("✅" if ok else "❌", nom, detail))
            rouge |= not ok
        if "--sans-sabotages" in opts:
            return 1 if rouge else 0
        for nom, fichier, avant, apres in SABOTAGES:
            sab = source_sabotee(source, os.path.join(travail, "src_" + nom), fichier, avant, apres)
            if sab is None:
                print("❌ IMPOSSIBLE — ancre du sabotage %s absente ou multiple" % nom)
                return 2
            try:
                tombes = [c for c, ok, _ in les_cas(sab, os.path.join(travail, nom)) if not ok]
            except Exception as e:   # noqa: BLE001 — un sabotage qui fait planter l'épreuve la fait tomber
                tombes = ["plantage %s" % type(e).__name__]
            print("%s %s → %s" % ("✅" if tombes else "❌", nom,
                                  ("tombe(nt) : " + " · ".join(c.split()[0] for c in tombes)) if tombes
                                  else "AUCUN CAS NE TOMBE"))
            rouge |= not tombes
            shutil.rmtree(os.path.join(travail, nom), ignore_errors=True)
        return 1 if rouge else 0
    finally:
        shutil.rmtree(travail, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
