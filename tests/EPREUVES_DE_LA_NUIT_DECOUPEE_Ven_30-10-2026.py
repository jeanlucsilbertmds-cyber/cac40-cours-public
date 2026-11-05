#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_NUIT_DECOUPEE — Ven 30-10-2026 (Paris). Simulation uniquement.

① RÔLE — Prouver que la certification de nuit découpée en tranches parallèles joue chaque épreuve une fois et une
  seule, que chaque tranche tient sous sa limite, et que la tâche finale rougit quand une tranche manque, est rouge,
  vient d'un autre passage ou n'a pas joué ce qu'elle devait.
② CONTEXTE D'APPEL — Chaque nuit par la certification (programmes/CERTIFIER_LA_VERSION.py, qui joue toute épreuve de
  tests/) ; à la main avant toute livraison qui touche programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py ou la répartition de
  programmes/CERTIFIER_LA_VERSION.py (R-731) :
  python3 tests/EPREUVES_DE_LA_NUIT_DECOUPEE_Ven_30-10-2026.py <racine> [--saboter]
③ ENTRÉE — La racine du dépôt (le fabricant et le certificateur sont pris dans son programmes/, les journaux des
  nuits dans son rapports/journal_du_circuit/).
④ CONDITIONS D'ENTRÉE — PyYAML et coverage installés (le circuit les installe) ; sinon code 2.
⑤ SORTIE — Le code de sortie : 0 si les cas N1 à N8, D1 et F0 à F9 donnent la réponse attendue et, avec --saboter, si
  chaque sabotage en fait échouer au moins un ; 1 sinon ; 2 si un sabotage ne s'applique plus ou si un module manque.
  [rend: 1]
⑥ TRAITEMENT — Sur une copie restreinte du dépôt (programmes, tests, fiches de circuit, journaux de certification) :
  N1 le fabricant écrit le circuit dans un dossier vide, code 0 · N2 le job « certifier » est une matrice des tranches
  1 à K, sans arrêt au premier échec (fail-fast: false), qui lance « --tranche ${{ matrix.tranche }}/K » ; le job
  « reunir » dépend de lui, tourne « always() » et lance « --reunir K », le même K · N3 chaque job a une limite
  (« timeout-minutes », 360 si absente, la valeur de GitHub) d'au plus 360 minutes · N4 la répartition faite par le
  certificateur (`repartir`, durées de `durees_relevees`) place chaque lancement dans exactement une tranche, et
  chaque fichier tests/*.py qu'aucun autre fichier de tests/ n'importe y figure (relevé ici par une autre rédaction
  que celle du certificateur) · N5 la charge prévue de chaque tranche ne dépasse pas le TIERS de sa limite · N6 le
  lancement d'une épreuve déclarée « series_hors_de_la_nuit » et sa vérification sont dans la même tranche.
  Puis sur un petit dépôt d'essai (un programme, trois épreuves, sa référence écrite par le certificateur) : les K
  tranches jouées pour de bon (passage « 777 »), puis la commande de la tâche finale, prise TELLE QU'ELLE EST ÉCRITE
  dans le circuit fabriqué et jouée par bash : F0 tout est là → 0, « VERSION CERTIFIÉE » et aucune « DÉRIVE » · F1 le certificat partiel
  d'une tranche VIDE effacé → non nul (aucun lancement n'y manque : seule la règle « il en manque un » le voit) · F1b
  celui d'une tranche pleine → non nul · F2 un autre passage → non nul · F3 une épreuve rouge dans un partiel → non nul · F4 un partiel
  qui se dit impossible → non nul · F5 un lancement joué par deux tranches → non nul · F6 un lancement joué par
  aucune → non nul · F7 une répartition différente → non nul · F8 un partiel d'une autre empreinte du code → non nul ·
  F9 un journal de CE passage aux durées extrêmes : la tranche relancée seule répartit comme ses sœurs (étalonné : vu
  d'un autre passage, il change la répartition). Et (31-10-2026) : N7 le pas « deposer » d'une tranche fait au moins
  autant d'essais de poussée qu'il y a de tranches · D1 `reunir_les_mesures` sur des mesures écrites à la main
  (intersection des lignes, des embranchements, des fonctions ; empreintes différentes écartées). Et (01-11-2026,
  relecture neuve, M8) : N8 la copie restreinte porte chaque fichier .py de chaque emplacement de code que le
  fabricant de la source publie (DOSSIERS_DE_CODE) — la copie ne garde pas sa propre liste.
⑦ UNITÉ — Des minutes (limites des jobs) et des secondes (charges).
⑧ POURQUOI — Décision de Jean-Luc du 30-10-2026 à 19h02 (réponse « 1 ») : « Couper la nuit en plusieurs tâches qui
  tournent en même temps, chacune avec ses propres 6 heures, plus une tâche finale qui réunit les résultats et dit
  rouge s'il en manque un. » La nuit du 29 au 30-10-2026, la certification d'un seul tenant a été coupée par sa
  limite de 330 minutes. Le tiers : les durées relevées ont varié du simple au double d'une nuit à l'autre (la série
  de la lecture des cours : 2 730 s, 4 379 s, 5 028 s les nuits du 23, du 24 et du 30-10-2026).
⑨ CE QUI CLOCHE — Le vrai GitHub Actions n'est pas joué : la matrice, « needs », « always() » et la limite sont lus
  dans le YAML, pas observés. Le pas « deposer » (poussée au dépôt privé, renommage du journal de la tranche) n'est
  pas joué. N5 dépend des journaux présents : sur un dépôt sans journal, chaque lancement compte pour son délai.
⑩ EFFET — Écrit dans des dossiers jetables, effacés à la fin.
⑪ TERMINAISON — Rend la main ; chaque lancement est borné (120 s pour le fabricant et la tâche finale, 300 s pour
  une tranche du dépôt d'essai) ; sort par sys.exit.
  [sort: oui]
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

try:
    import yaml
    import coverage  # noqa: F401  (le certificateur le demande pour jouer une tranche)
except ImportError as e:
    print(f"ARRÊT : module manquant ({e.name})")
    sys.exit(2)

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
FAB = "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"
CERTIF = "programmes/CERTIFIER_LA_VERSION.py"
CIRCUIT = ".github/workflows/certifier_la_version.yml"
LIMITE_DE_GITHUB = 360          # minutes : GitHub coupe toute tâche à 6 heures, et c'est aussi sa limite par défaut
TIERS = 3                       # une tranche ne prévoit pas plus du tiers de sa limite (voir ⑧)
PASSAGE = "777"
SABOTAGES = {
    "Z0": [],
    "S1_epreuve_retiree_de_la_repartition": [(CERTIF, "    for c in unites:\n", "    for c in unites[1:]:\n")],
    "S2_finale_sans_always": [(FAB, "    if: ${{ always() }}\n", "")],
    "S3_partiel_manquant_accepte": [(CERTIF,
        '            fautes.append(f"tranche {i} : certificat partiel absent ou illisible ({type(e).__name__})")\n',
        "            pass\n")],
    "S4_tranche_a_400_minutes": [(FAB, "    timeout-minutes: 330\n", "    timeout-minutes: 400\n")],
    "S5_arret_au_premier_echec": [(FAB, "      fail-fast: false\n", "")],
    "S6_autre_passage_accepte": [(CERTIF, 'attendu = {"passage": passage, "nombre"', 'attendu = {"nombre"')],
    "S7_doublon_accepte": [(CERTIF, '("joué(s) par plusieurs tranches", doubles)', '("joué(s) par plusieurs tranches", [])')],
    "S8_partiel_impossible_accepte": [(CERTIF, '        elif p.get("impossible"):\n', '        elif False:\n')],
    "S9_finale_sans_dependance": [(FAB, "    needs: certifier\n", "")],
    "S10_repartitions_differentes_acceptees": [(CERTIF, "if not fautes and len({p.get(\"repartition\") for p in lus}) != 1:",
                                                "if False:")],
    "S12_moins_d_essais_que_de_tranches": [(FAB, "ESSAIS_DE_POUSSEE = TRANCHES_DE_LA_NUIT + 3\n",
                                            "ESSAIS_DE_POUSSEE = TRANCHES_DE_LA_NUIT - 1\n")],
    "Sa_passage_en_cours_non_ecarte": [(CERTIF, "        if not m or (passage_exclu and m.group(1) == passage_exclu):\n",
                                        "        if not m:\n")],
    "Sb_union_des_lignes": [(CERTIF, 'set.intersection(*(set(x["lignes"]) for x in v))', 'set.union(*(set(x["lignes"]) for x in v))')],
    "Sc_empreinte_du_code_non_verifiee": [(CERTIF, ', "tranche": i, "empreinte_du_code": empreinte}', ', "tranche": i}')],
    "Sd_union_des_embranchements": [(CERTIF, 'set.intersection(*({tuple(p) for p in x["branches"]} for x in v))',
                                     'set.union(*({tuple(p) for p in x["branches"]} for x in v))')],
    "S11_epreuve_coupee_en_deux": [(CERTIF, "        groupes.setdefault(l[0], []).append(l)\n",
                                    "        groupes.setdefault(cle_de(l[0], l[2]), []).append(l)\n"),
                                   (CERTIF, "    return [[l for l in lancements if l[0] in choisies[i]] for i in range(nombre)], charges",
                                    "    return [[l for l in lancements if cle_de(l[0], l[2]) in choisies[i]] for i in range(nombre)], charges")],
}

# Le petit dépôt d'essai : un programme à trois fonctions, une épreuve par fonction (chacune exécute sa fonction par un
# sous-processus, comme les vraies épreuves exécutent leurs programmes).
PROGRAMME = "def a():\n    return 1\n\n\ndef b():\n    return 2\n\n\ndef c():\n    return 3\n"
EPREUVE = ("import os, subprocess, sys\nracine = sys.argv[1]\n"
           "r = subprocess.run([sys.executable, '-E', '-c', 'import sys; sys.path.insert(0, %r); import P; "
           "sys.exit(0 if P.{f}() else 1)' % os.path.join(racine, 'programmes')])\nsys.exit(r.returncode)\n")


def copier_le_necessaire(source, cible):
    """Copie ce que l'épreuve lit du dépôt dans un dossier jetable.

    ① RÔLE — Travailler sur une copie, que les sabotages peuvent modifier. ② CONTEXTE D'APPEL — `tour`.
    ③ ENTRÉE — `source` : la racine · `cible` : un dossier vide. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien. [rend: rien]
    ⑥ TRAITEMENT — les *.py de chaque emplacement de code publié, lus dans DOSSIERS_DE_CODE du fabricant de la source
      (la racine, programmes/, tests/, etudes/outils/, tests/outils/ au 01-11-2026), tests/*.json, les fiches
      .github/workflows/*.yml, les journaux de certification de rapports/journal_du_circuit/.
    ⑦ UNITÉ — — ⑧ POURQUOI — Copier tout le dépôt (des milliers de fichiers) à chaque sabotage serait lent ; le
      fabricant et le certificateur n'en lisent pas davantage ici. Les emplacements sont LUS au fabricant, jamais
      épelés ici : relecture neuve du 01-11-2026 (M8), une seconde liste avait gardé les quatre anciens (R-708).
    ⑨ CE QUI CLOCHE — Un fichier lu ailleurs ne serait pas copié : le cas qui en a besoin rougirait. · Si la lecture
      de DOSSIERS_DE_CODE au fabricant échoue (fabricant absent, nom changé), l'épreuve sort en trace Python, code 1,
      et non 2 comme le ⑤ du programme le promet quand elle n'a pas pu juger : c'est rouge pour la certification
      (programmes/CERTIFIER_LA_VERSION.py compte rouge tout code non nul), seule l'étiquette est fausse. Mesuré par la
      relecture n° 2 du 04-11-2026 (m6, AttributeError, code 1). Aucun filet « code 2 » dans `main` : il rangerait
      sous « n'a pas pu juger » une vraie panne du fabricant (superviseur R-759 du même jour, tour 3).
    ⑩ EFFET — Charge le fabricant de la source (il ne fait que définir) ; écrit la copie. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    code = [(d, r".*\.(py|json)$" if d == "tests" else r".*\.py$")
            for d in charger(os.path.join(source, FAB)).DOSSIERS_DE_CODE]
    for dossier, motif in code + [(".github/workflows", r".*\.ya?ml$"),
                                  ("rapports/journal_du_circuit", r"^circuit_\d+_\d+_certifier.*\.log$")]:
        d = os.path.join(source, dossier)
        if not os.path.isdir(d):
            continue
        os.makedirs(os.path.join(cible, dossier), exist_ok=True)
        for f in os.listdir(d):
            if re.match(motif, f) and os.path.isfile(os.path.join(d, f)):
                shutil.copyfile(os.path.join(d, f), os.path.join(cible, dossier, f))


def charger(chemin):
    """Charge un module depuis son fichier et le rend.

    ① RÔLE — Appeler les fonctions du certificateur de la copie (saboté ou non). ② CONTEXTE D'APPEL — `tour`.
    ③ ENTRÉE — `chemin`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le module. [rend: 1]
    ⑥ TRAITEMENT — importlib. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Exécute le module.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    sp = importlib.util.spec_from_file_location("CERTIF_%d" % abs(hash(chemin)), chemin)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def certifier(certificateur, racine, *options, passage=PASSAGE, delai=300):
    """Lance le certificateur sur une racine et rend son code et sa sortie.

    ① RÔLE — Jouer une tranche ou écrire une référence sur le dépôt d'essai. ② CONTEXTE D'APPEL — `essai`.
    ③ ENTRÉE — `certificateur` : son chemin · `racine` · `options` · `passage` : GITHUB_RUN_ID · `delai` : secondes.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — DEUX valeurs : le code, la sortie. [rend: 2]
    ⑥ TRAITEMENT — subprocess, sans la configuration Git de la machine. ⑦ UNITÉ — Des secondes.
    ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lance un processus. ⑪ TERMINAISON — Borné à `delai`. [sort: non]
    """
    env = dict(os.environ, GITHUB_RUN_ID=passage)
    r = subprocess.run([sys.executable, "-B", certificateur, racine] + list(options), capture_output=True, text=True,
                       timeout=delai, env=env)
    return r.returncode, r.stdout + r.stderr


def tests_lances(copie):
    """Rend les tests/*.py qu'aucun autre fichier de tests/ n'importe — la règle relue ici, par une autre rédaction.

    ① RÔLE — Dire quelles épreuves de tests/ doivent figurer dans une tranche, sans demander au certificateur.
    ② CONTEXTE D'APPEL — `tour`, N4. ③ ENTRÉE — `copie`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : l'ensemble des chemins « tests/X.py ». [rend: 1]
    ⑥ TRAITEMENT — chercher « import X » ou « from X import » dans le texte des autres fichiers.
    ⑦ UNITÉ — — ⑧ POURQUOI — Une épreuve oubliée à la fois par la liste et par la répartition ne serait vue par
      aucune vérification qui demande la liste au certificateur lui-même.
    ⑨ CE QUI CLOCHE — Un import écrit autrement (importlib) n'est pas vu : le fichier serait compté comme épreuve.
    ⑩ EFFET — Lit des fichiers. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    noms = sorted(f for f in os.listdir(os.path.join(copie, "tests")) if f.endswith(".py"))
    textes = {f: open(os.path.join(copie, "tests", f), encoding="utf-8").read() for f in noms}
    importes = {f for f in noms for g, t in textes.items() if g != f
                and re.search(r"^\s*(import|from)\s+%s\b" % re.escape(f[:-3]), t, re.M)}
    return {"tests/" + f for f in noms if f not in importes}


def essai(copie, circuit, faux):
    """Joue F0 à F9 : les tranches sur un petit dépôt d'essai, puis la commande de la tâche finale.

    ① RÔLE — Prouver que la tâche finale rougit quand elle doit, en jouant SA commande telle qu'elle est écrite.
    ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — `copie` : la copie (le certificateur y est pris) · `circuit` : le YAML
      fabriqué, lu · `faux` : la liste des fautes, complétée.
    ④ CONDITIONS D'ENTRÉE — N2 a trouvé les jobs. ⑤ SORTIE — Rien. [rend: rien]
    ⑥ TRAITEMENT — Voir la fiche en tête, ⑥ (F0 à F9).
    ⑦ UNITÉ — — ⑧ POURQUOI — Voir la fiche en tête, ⑧.
    ⑨ CE QUI CLOCHE — Jusqu'à F8, le dépôt d'essai n'a pas de journal : la répartition y suit les délais (tous égaux) ;
      F9 en pose un, à la fin. F9 ne lit pas le code de sortie des deux tranches relancées (BACKLOG proposé).
    ⑩ EFFET — Écrit un dépôt d'essai jetable. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    commande = next((p.get("run") for p in circuit["jobs"]["reunir"]["steps"] if p.get("id") == "certifier"), None)
    nombre = len(circuit["jobs"]["certifier"]["strategy"]["matrix"]["tranche"])
    if not commande:
        faux.append("F commande de la tâche finale introuvable")
        return
    d = tempfile.mkdtemp(prefix="nuit_decoupee_")
    try:
        m = os.path.join(d, "depot")
        for c, t in [("programmes/P.py", PROGRAMME), ("programmes/CERTIFIER_LA_VERSION.py",
                                                       open(os.path.join(copie, CERTIF), encoding="utf-8").read()),
                     ("tests/LANCEMENT_DES_EPREUVES.json", json.dumps({"epreuves": {}}))] + [
                (f"tests/T{f}.py", EPREUVE.replace("{f}", f)) for f in "abc"]:
            os.makedirs(os.path.dirname(os.path.join(m, c)), exist_ok=True)
            open(os.path.join(m, c), "w", encoding="utf-8").write(t)
        os.makedirs(os.path.join(m, "gouvernance"))   # où le certificateur écrit sa référence
        cert = os.path.join(m, CERTIF)
        c, o = certifier(cert, m, "--ecrire-la-reference")
        if c != 0:
            faux.append(f"F référence du dépôt d'essai non écrite (code {c}) : {o.strip().splitlines()[-1:]}")
            return
        for i in range(1, nombre + 1):
            c, o = certifier(cert, m, "--tranche", f"{i}/{nombre}")
            if c != 0:
                faux.append(f"F tranche {i}/{nombre} du dépôt d'essai : code {c} : {o.strip().splitlines()[-1:]}")
                return
        partiels = os.path.join(m, "rapports", "certificats_partiels")
        garde = {f: open(os.path.join(partiels, f), encoding="utf-8").read() for f in os.listdir(partiels)}

        def finale(passage=PASSAGE):
            r = subprocess.run(["bash", "-e", "-c", commande], cwd=m, capture_output=True, text=True, timeout=120,
                               env=dict(os.environ, GITHUB_WORKSPACE=m, GITHUB_RUN_ID=passage))
            texte = open(os.path.join(m, "rapports", "CERTIFICAT_DE_LA_VERSION.md"), encoding="utf-8").read()
            for f, t in garde.items():   # remettre les partiels en état pour le cas suivant
                open(os.path.join(partiels, f), "w", encoding="utf-8").write(t)
            return r.returncode, texte

        def modifier(n, quoi):
            p = json.loads(garde[f"TRANCHE_{n}.json"])
            quoi(p)
            open(os.path.join(partiels, f"TRANCHE_{n}.json"), "w", encoding="utf-8").write(json.dumps(p))

        pleine = next(n for n in range(1, nombre + 1) if json.loads(garde[f"TRANCHE_{n}.json"])["joues"])
        autre = next(n for n in range(1, nombre + 1) if n != pleine)
        c, t = finale()
        # « DÉRIVE » : le code du dépôt d'essai est celui de sa référence, et `conclure` rangerait en « DÉRIVE DE MESURE »
        # un recul né d'une réunion fausse, sans rougir (relecteur du 31-10-2026, I2) ; D1 éprouve la réunion directement
        if c != 0 or "VERSION CERTIFIÉE" not in t or "DÉRIVE" in t:
            faux.append(f"F0 tout est là : code {c}, attendu 0, « VERSION CERTIFIÉE » et aucune « DÉRIVE »")
        # F1 : le partiel d'une tranche VIDE effacé — seule la règle « il en manque un » peut le voir, puisque aucun
        # lancement n'y manque ; F1b : celui d'une tranche pleine
        vide = next((n for n in range(nombre, 0, -1) if not json.loads(garde[f"TRANCHE_{n}.json"])["joues"]), None)
        for cas, n in (("F1", vide), ("F1b", autre)):
            if n is None:
                faux.append(f"{cas} aucune tranche vide dans le dépôt d'essai : le cas ne peut pas se jouer")
                continue
            os.remove(os.path.join(partiels, f"TRANCHE_{n}.json"))
            c, t = finale()
            if c == 0 or "IMPOSSIBLE" not in t:
                faux.append(f"{cas} le certificat partiel effacé de la tranche {n} accepté (code {c})")
        c, t = finale("778")
        if c == 0:
            faux.append("F2 des partiels d'un autre passage acceptés")

        def rouge(p):
            p["resultats"][0][3] = 1
        modifier(pleine, rouge)
        c, t = finale()
        if c == 0:
            faux.append("F3 une épreuve rouge dans un partiel acceptée")
        modifier(autre, lambda p: p.update(impossible="la mesure est aveugle (essai)"))
        c, t = finale()
        if c == 0:
            faux.append("F4 un partiel « impossible » accepté")

        def double(p):
            q = json.loads(garde[f"TRANCHE_{pleine}.json"])
            p["joues"] += q["joues"][:1]
            p["resultats"] += q["resultats"][:1]
        modifier(autre, double)
        c, t = finale()
        if c == 0:
            faux.append("F5 un lancement joué par deux tranches accepté")
        modifier(pleine, lambda p: (p["joues"].pop(0), p["resultats"].pop(0)))
        c, t = finale()
        if c == 0:
            faux.append("F6 un lancement joué par aucune tranche accepté")
        modifier(autre, lambda p: p.update(repartition="0" * 16))
        c, t = finale()
        if c == 0:
            faux.append("F7 une répartition différente acceptée")
        modifier(pleine, lambda p: p.update(empreinte_du_code="0" * 16))
        c, t = finale()
        if c == 0:
            faux.append("F8 un partiel d'un autre code (empreinte) accepté")
        # F9 — le passage en cours écarté des durées (relecteur du 31-10-2026, I2, Sa) : un journal de CE passage, aux
        # durées extrêmes, est posé ; la tranche relancée seule (« Re-run failed jobs ») doit répartir comme ses sœurs.
        # Étalonnage : le même journal, vu depuis un AUTRE passage, doit changer la répartition — sinon le cas ne prouve rien.
        C = charger(cert)
        os.makedirs(os.path.join(m, C.JOURNAUX))
        with open(os.path.join(m, C.JOURNAUX, f"circuit_{PASSAGE}_1_certifier_tranche_1.log"), "w", encoding="utf-8") as s:
            s.write("\n".join(C.ligne_du_journal(f"tests/T{f}.py", ["{copie}"], 0, d_) for f, d_ in
                              (("a", 1), ("b", 2), ("c", 10000))) + "\n")
        avant = json.loads(garde[f"TRANCHE_{pleine}.json"])["repartition"]
        apres = {}
        for passage in (PASSAGE, "999"):
            c, o = certifier(cert, m, "--tranche", f"{pleine}/{nombre}", passage=passage)
            apres[passage] = json.load(open(os.path.join(partiels, f"TRANCHE_{pleine}.json"), encoding="utf-8")).get("repartition")
        if apres["999"] == avant:
            faux.append("F9 étalonnage : le journal posé ne change pas la répartition, le cas ne prouve rien")
        elif apres[PASSAGE] != avant:
            faux.append("F9 la tranche relancée dans le même passage a lu le journal de ce passage : autre répartition")
    finally:
        shutil.rmtree(d, ignore_errors=True)


def tour(depot):
    """Joue N1 à N8, D1, puis F0 à F9 sur une copie de `depot`, et rend la liste des cas faux.

    ① RÔLE — Un tour d'épreuves. ② CONTEXTE D'APPEL — `main`, une fois tel quel puis une fois par sabotage.
    ③ ENTRÉE — `depot` : la copie restreinte à éprouver. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des fautes. [rend: 1]
    ⑥ TRAITEMENT — Voir la fiche en tête, ⑥. ⑦ UNITÉ — Minutes, secondes. ⑧ POURQUOI — Voir la fiche en tête.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit un dossier jetable. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    faux = []
    pub = tempfile.mkdtemp(prefix="nuit_publique_")
    try:
        r = subprocess.run([sys.executable, "-B", os.path.join(depot, FAB), depot, pub], capture_output=True,
                           text=True, timeout=120)
        if r.returncode != 0 or not os.path.isfile(os.path.join(pub, CIRCUIT)):
            return [f"N1 le fabricant rend {r.returncode} : {(r.stdout + r.stderr).strip()[-200:]}"]
        y = yaml.safe_load(open(os.path.join(pub, CIRCUIT), encoding="utf-8"))
    finally:
        shutil.rmtree(pub, ignore_errors=True)
    jobs = y.get("jobs") or {}
    t, f = jobs.get("certifier") or {}, jobs.get("reunir") or {}
    tranches = ((t.get("strategy") or {}).get("matrix") or {}).get("tranche")
    if not isinstance(tranches, list) or not tranches:
        return ["N2 le job « certifier » n'est pas une matrice de tranches"]
    k = len(tranches)
    if tranches != list(range(1, k + 1)):
        faux.append(f"N2 tranches {tranches}, attendu 1 à {k}")
    if (t.get("strategy") or {}).get("fail-fast") is not False:
        faux.append("N2 la matrice s'arrête au premier échec (fail-fast n'est pas false)")
    run_t = next((p.get("run", "") for p in t.get("steps", []) if p.get("id") == "certifier"), "")
    run_f = next((p.get("run", "") for p in f.get("steps", []) if p.get("id") == "certifier"), "")
    if f"--tranche ${{{{ matrix.tranche }}}}/{k}" not in run_t:
        faux.append(f"N2 la tranche ne lance pas « --tranche ${{{{ matrix.tranche }}}}/{k} » : {run_t!r}")
    if not re.search(r"--reunir %d\s*$" % k, run_f):
        faux.append(f"N2 la tâche finale ne lance pas « --reunir {k} » : {run_f!r}")
    besoins = f.get("needs")
    if "certifier" not in ([besoins] if isinstance(besoins, str) else (besoins or [])):
        faux.append("N2 la tâche finale ne dépend pas des tranches (needs)")
    if "always()" not in str(f.get("if", "")):
        faux.append("N2 la tâche finale ne tourne pas « always() » : elle se tairait quand une tranche échoue")
    for nom, j in jobs.items():
        lim = j.get("timeout-minutes", LIMITE_DE_GITHUB)
        if not isinstance(lim, int) or lim > LIMITE_DE_GITHUB:
            faux.append(f"N3 job {nom} : limite {lim!r} minutes, au-delà de {LIMITE_DE_GITHUB}")
    # N4 à N6 — la répartition du certificateur de la copie, sur les journaux de la copie
    C = charger(os.path.join(depot, CERTIF))
    lancements, _ = C.lister_les_epreuves(depot)
    delais, series = C.options_de_lancement(depot)
    parts, charges = C.repartir(lancements, C.durees_relevees(depot), delais, k)
    vus = [json.dumps(l) for p in parts for l in p]
    for l in lancements:
        n = vus.count(json.dumps(l))
        if n != 1:
            faux.append(f"N4 {C.cle_de(l[0], l[2])} : dans {n} tranche(s), attendu 1")
    places = {l[0] for p in parts for l in p}
    for e in sorted(tests_lances(depot) - places):
        faux.append(f"N4 épreuve de tests/ dans aucune tranche : {e}")
    limite = t.get("timeout-minutes", LIMITE_DE_GITHUB)
    for i, ch in enumerate(charges, 1):
        if not isinstance(limite, int) or ch * TIERS > limite * 60:
            faux.append(f"N5 tranche {i} : {ch} s prévues, au-delà du tiers de {limite} minutes")
    # N7 — assez d'essais de poussée : une tranche échoue au plus (tranches − 1) + (poussées étrangères) fois
    # (superviseur R-759 du 31-10-2026) ; moins d'essais que de tranches perd des partiels à coup sûr
    depot_t = next((p.get("run", "") for p in t.get("steps", []) if p.get("id") == "deposer"), "")
    essais = re.findall(r"for i in \$\(seq 1 (\d+)\)", depot_t)
    if len(essais) != 1 or int(essais[0]) < k:
        faux.append(f"N7 essais de poussée d'une tranche : {essais}, il en faut au moins {k} (le nombre de tranches)")
    # D1 — la réunion des mesures, éprouvée directement (prototype du superviseur R-759 du 31-10-2026) : ce qu'aucune
    # tranche n'examine est l'INTERSECTION de leurs non-examinés ; un programme d'empreintes différentes est écarté
    a_ = {"p.py": {"empreinte": "E", "lignes": [1, 2], "branches": [[1, 2], [2, 3]], "fonctions_non_examinees": ["f", "g"]}}
    b_ = {"p.py": {"empreinte": "E", "lignes": [2, 3], "branches": [[2, 3], [4, 5]], "fonctions_non_examinees": ["g", "h"]}}
    c_ = {"p.py": {"empreinte": "AUTRE", "lignes": [], "branches": [], "fonctions_non_examinees": []}}
    r_, _ = C.reunir_les_mesures([a_, b_])
    for cle, voulu in (("lignes", [2]), ("branches", [[2, 3]]), ("fonctions_non_examinees", ["g"])):
        if r_.get("p.py", {}).get(cle) != voulu:
            faux.append(f"D1 réunion des {cle} : {r_.get('p.py', {}).get(cle)}, attendu {voulu}")
    r_, e_ = C.reunir_les_mesures([a_, c_])
    if e_ != ["p.py"] or r_:
        faux.append("D1 un programme mesuré avec deux empreintes n'est pas écarté")
    # N8 — la copie porte le code de chaque emplacement que le fabricant de la SOURCE publie (relecture neuve du
    # 01-11-2026, M8) : une liste gardée par `copier_le_necessaire` oublierait un emplacement ajouté au fabricant, et
    # aucun autre cas ne le verrait (le relecteur l'a mesuré : la liste des quatre anciens restait verte)
    for dossier in charger(os.path.join(DEPOT, FAB)).DOSSIERS_DE_CODE:
        src = os.path.join(DEPOT, dossier)
        manque = sorted(f for f in (os.listdir(src) if os.path.isdir(src) else [])
                        if f.endswith(".py") and os.path.isfile(os.path.join(src, f))
                        and not os.path.isfile(os.path.join(depot, dossier, f)))
        if manque:
            faux.append(f"N8 la copie n'a pas le code de « {dossier or '.'} » : {len(manque)} fichier(s), dont {manque[:2]}")
    for e in series:
        ou = {i for i, p in enumerate(parts) for l in p if l[0] == e}
        if len(ou) != 1:
            faux.append(f"N6 série hors de la nuit {e} : son lancement et sa vérification dans {len(ou)} tranches")
    essai(depot, y, faux)
    return faux


def main():
    """Joue le tour tel quel (Z0), puis, avec --saboter, un tour par sabotage.

    ① RÔLE — Le programme entier. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — Voir la fiche en tête.
    ④ CONDITIONS D'ENTRÉE — Voir la fiche en tête. ⑤ SORTIE — Le code de sortie (0, 1, 2). [rend: 1]
    ⑥ TRAITEMENT — Pour chaque cas : copie restreinte, sabotage appliqué (chaque texte doit y être une fois), tour.
      Z0 doit être vert ; chaque sabotage doit faire au moins une faute.
    ⑦ UNITÉ — — ⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas une preuve (R-731).
    ⑨ CE QUI CLOCHE — Si la lecture de DOSSIERS_DE_CODE au fabricant échoue, trace Python, code 1 : rouge pour la
      certification, voir le ⑨ de `copier_le_necessaire`.
    ⑩ EFFET — Écrit des dossiers jetables. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    noms = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
    code = 0
    for nom in noms:
        d = tempfile.mkdtemp(prefix="nuit_copie_")
        try:
            copier_le_necessaire(DEPOT, d)
            for fichier, avant, apres in SABOTAGES[nom]:
                p = os.path.join(d, fichier)
                texte = open(p, encoding="utf-8").read()
                if texte.count(avant) != 1:
                    print(f"{nom} NE S'APPLIQUE PLUS : texte trouvé {texte.count(avant)} fois dans {fichier}")
                    code = 2
                    break
                open(p, "w", encoding="utf-8").write(texte.replace(avant, apres))
            else:
                faux = tour(d)
                if nom == "Z0":
                    print("Z0 " + ("vert" if not faux else "ROUGE : " + " | ".join(faux)))
                    code = max(code, 1 if faux else 0)
                else:
                    print(f"{nom} " + ("mord : " + str(faux[:2])[:160] if faux else "NE MORD PAS"))
                    code = max(code, 0 if faux else 1)
        finally:
            shutil.rmtree(d, ignore_errors=True)
    return code


if __name__ == "__main__":
    sys.exit(main())
