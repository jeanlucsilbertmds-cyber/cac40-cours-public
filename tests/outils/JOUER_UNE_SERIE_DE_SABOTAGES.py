#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""JOUER_UNE_SERIE_DE_SABOTAGES — Ven 16-10-2026 (Paris). Simulation uniquement.

① RÔLE — Jouer en entier la série de sabotages d'une épreuve trop longue pour la nuit, par lots repris là où ils se
  sont arrêtés, sur plusieurs processeurs, et en écrire le RELEVÉ avec l'empreinte de chaque fichier du dépôt lu
  pendant la série (programmes/SERIES_DE_SABOTAGES.py). La certification de nuit vérifie ensuite ces empreintes.
② CONTEXTE D'APPEL — À la main, à chaque livraison qui change l'épreuve ou un fichier qu'elle lit (R-731), sous
  l'outil de surveillance du Chat (méthode du 10-10-2026, projet de section 12 du mode d'emploi, A-562) :
  python3 -u tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py <racine> <épreuve> <relevé> [--parts=2] [--lot=21]
  [--travail=<dossier>] — `épreuve` et `relevé` relatifs à la racine.
③ ENTRÉE — La racine d'un dépôt (un clone, jamais le dépôt où l'on travaille : l'épreuve y écrit des dossiers
  jetables) ; l'épreuve, qui doit accepter « --saboter=S1,S2,… » et porter un dictionnaire SABOTAGES ; le relevé.
④ CONDITIONS D'ENTRÉE — Le dossier de travail est propre à cette racine : il garde les lots faits et l'état du dépôt
  au départ ; si le dépôt a changé depuis, le travail est refusé (ARRET) et il faut un dossier neuf.
⑤ SORTIE — Le code de sortie : 0 relevé écrit et série conforme ; 1 relevé écrit, série NON conforme (un sabotage ne
  mord pas, un lot a rendu autre chose que 0) ; 2 rien d'écrit (dépôt changé, épreuve illisible, sortie d'un lot
  introuvable, table de lancement illisible, portée inconnue). L'ancien relevé de la même série (même nom, à la date près) est rangé dans archives/ avant l'écriture.
  [rend: 1]
⑥ TRAITEMENT — ① lire les noms des sabotages dans l'épreuve (arbre syntaxique, clé du dictionnaire SABOTAGES) ·
  ② prendre l'empreinte de chaque fichier du dépôt (sans .git ni le relevé), ou relire celle du départ et refuser si
  un fichier présent au départ a changé ou disparu ·
  ③ découper en lots ; jouer chaque lot non fait, `--parts` à la fois, l'épreuve écoutée par un module de démarrage
  qui note chaque fichier ouvert en lecture · ④ chaque lot écrit sa sortie et son code, d'abord dans un fichier
  « .part », renommé une fois fini · ⑤ quand tous sont faits : chaque sabotage doit apparaître une fois, « mord » ;
  les fichiers lus = ceux notés ET présents au départ (les dossiers jetables de l'épreuve n'y sont pas) ; leur
  empreinte doit être celle du départ · ⑥ écrire le relevé. Avec la portée « lectures » (la règle d'origine, prise
  quand la table n'en déclare pas), le relevé porte les fichiers LUS. Avec la portée « epreuve » (décision de Jean-Luc
  n°71 du 01-11-2026 à 11h41 : la série de l'épreuve d'arrivée des signaux ne se rejoue que quand le code de l'essai
  change) ou « code_execute » (05-11-2026, CHOIX D43 DU CHAT, À CONFIRMER PAR JEAN-LUC : le code de l'essai lu comme
  le code que la série exécute), le relevé porte les fichiers du dépôt dont le code a été EXÉCUTÉ pendant la série —
  l'écoute note aussi l'évènement d'audit « exec », et `SERIE.fichiers_executes` ramène chaque code exécuté, même
  dans une copie jetable, au fichier du dépôt qu'il représente ; les données n'y entrent pas, elles ne sont jamais
  exécutées. Le relevé porte les mêmes empreintes pour ces deux portées : la nuit ne compare que l'épreuve
  (« epreuve ») ou tout le code exécuté (« code_execute »), et passer de l'une à l'autre se fait d'un mot dans la
  table, sans rejouer la série. La portée vient de la table, lue par `CERTIF.options_de_lancement` (R-708), et ses
  valeurs de `SERIE.PORTEES`.
⑦ UNITÉ — —
⑧ POURQUOI — Décision de Jean-Luc du 16-10-2026 à 14h30 : la série des 167 sabotages de l'épreuve des 20 ans se rejoue
  quand son code change, avec une alarme la nuit si on oublie. Elle dure environ 6 heures sur la machine du Chat
  (27 sabotages en 62 minutes mesurés le 16-10-2026) : les lots permettent la reprise si la machine redémarre, et
  plusieurs lots en même temps divisent la durée. Repères en tête de ligne pour la surveillance : ETAPE, ERREUR,
  FINI, ARRET.
⑨ CE QUI CLOCHE — Le module d'écoute passe par PYTHONPATH : l'épreuve est lancée sans « -I », et un programme qu'elle
  lance avec « -I », « -E » ou « -S », ou avec un environnement remplacé (`env=` sans PYTHONPATH), n'est pas écouté
  — ni ses lectures ni son code exécuté ne sont notés —, et du code exécuté par `exec` d'une chaîne lue dans un fichier
  ne porte pas le nom de ce fichier (relecteur du 05-11-2026, défaut 2 : les cinq mécanismes, détaillés au ⑨ ③ de
  programmes/SERIES_DE_SABOTAGES.py) ; la vérification de
  nuit ne le rattrape pas non plus : ce qui n'est pas lu sous l'écoute n'a pas d'empreinte (la règle « chaque
  programme nommé », qui le rattrapait par hasard de nommage, est retirée le 17-10-2026). · Avec la portée
  « lectures », seules les ouvertures SOUS LA RACINE comptent : un programme exécuté dans une copie faite ailleurs
  n'est pas couvert (la mesure « exec » ne leur est pas appliquée : changer leur mesure pourrait rendre « SÉRIE À
  REJOUER » à la nuit suivante, environ 6 heures pour les 20 ans ; décision séparée, BACKLOG). · Les limites de la
  mesure « exec » : programmes/SERIES_DE_SABOTAGES.py, ⑨. · Un fichier compilé
  (__pycache__) lu à la place d'un .py est ramené à son .py. · Un lot coupé recommence en entier.
⑩ EFFET — Écrit dans le dossier de travail (lots, empreintes du départ, écoutes) et le relevé ; l'épreuve écrit ses
  dossiers jetables.
⑪ TERMINAISON — Rend la main quand tous les lots ont fini ; un lot n'a pas de délai (il en faut plus de deux heures) ;
  sort par sys.exit avec le code dit en ⑤.
  [sort: oui]
"""
import concurrent.futures
import datetime
import json
import os
import re
import subprocess
import sys
import zoneinfo

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "..", "..", "programmes"))
import SERIES_DE_SABOTAGES as SERIE   # noqa: E402  (le relevé : écrit une fois, lu par la certification, R-708)
import CERTIFIER_LA_VERSION as CERTIF  # noqa: E402  (l'environnement de la nuit : défini une fois, R-708)

PARIS = zoneinfo.ZoneInfo("Europe/Paris")
# L'ÉCOUTE : chaque processus note les fichiers qu'il ouvre en lecture (dossier SERIE_ECOUTE) et, depuis le
# 05-11-2026, le fichier de chaque code qu'il EXÉCUTE (évènement d'audit « exec », dossier SERIE_EXECUTION, à part :
# la lecture des notes « lus » de la portée « lectures » reste inchangée).
ECOUTE = '''import os, sys
_d = os.environ.get("SERIE_ECOUTE")
_x = os.environ.get("SERIE_EXECUTION")
if _d:
    _f = open(os.path.join(_d, "lus.%d" % os.getpid()), "a", encoding="utf-8")
    _g = open(os.path.join(_x, "executes.%d" % os.getpid()), "a", encoding="utf-8") if _x else None
    def _h(ev, a):
        if ev == "open" and a and isinstance(a[0], (str, bytes)) and "w" not in str(a[1] or "r") and "a" not in str(a[1] or "r"):
            _f.write(os.path.realpath(os.fsdecode(a[0])) + "\\n"); _f.flush()
        elif _g is not None and ev == "exec" and a and hasattr(a[0], "co_filename"):
            _g.write(a[0].co_filename + "\\n"); _g.flush()
    sys.addaudithook(_h)
'''
LIGNE = SERIE.LIGNE


def heure():
    """Rend l'heure de Paris, « HHhMM ».

    ① RÔLE — Dater les repères. ② CONTEXTE D'APPEL — Partout. ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte. [rend: 1] ⑥ TRAITEMENT — datetime. ⑦ UNITÉ — Heure de Paris.
    ⑧ POURQUOI — Les repères sont lus pendant des heures. ⑨ CE QUI CLOCHE — — ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    return datetime.datetime.now(PARIS).strftime("%Hh%M")


def etat_du_depot(racine):
    """Rend l'empreinte de chaque fichier du dépôt, sans .git ni __pycache__.

    ① RÔLE — Fixer l'état de départ, pour la reprise et pour la vérification de fin. ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` : le dépôt. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : {chemin relatif : sha256}.
    [rend: 1] ⑥ TRAITEMENT — os.walk. ⑦ UNITÉ — — ⑧ POURQUOI — Voir la fiche en tête, ⑥ ②.
    ⑨ CE QUI CLOCHE — Les liens symboliques sont suivis comme des fichiers. ⑩ EFFET — Lit tout le dépôt.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    etat = {}
    for r, ds, fs in os.walk(racine):
        ds[:] = [d for d in ds if d not in (".git", "__pycache__")]
        for f in fs:
            p = os.path.join(r, f)
            if os.path.isfile(p):
                etat[os.path.relpath(p, racine).replace(os.sep, "/")] = SERIE.empreinte(p)
    return etat


def jouer_un_lot(racine, epreuve, travail, k, lot):
    """Joue un lot de sabotages ; rend (k, code).

    ① RÔLE — Un morceau de la série, repris s'il est déjà fait. ② CONTEXTE D'APPEL — `main`, en parallèle.
    ③ ENTRÉE — `racine`, `epreuve` (relative), `travail` : le dossier de travail · `k` : le numéro du lot · `lot` : ses
      noms. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : (k, code de l'épreuve). [rend: 1]
    ⑥ TRAITEMENT — si lot_k.code existe, le relire ; sinon lancer l'épreuve écoutée, sans la configuration git de la
      machine (`CERTIF.SANS_LA_CONFIGURATION_GIT_DE_LA_MACHINE`), sortie dans lot_k.out.part puis renommée, code dans
      lot_k.code. ⑦ UNITÉ — — ⑧ POURQUOI — Voir la fiche en tête. Sans la configuration git : cassure N de Cowork,
      17-10-2026 — le relevé était écrit dans un autre environnement que celui où la nuit le rejoue.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit dans `travail` ; lance l'épreuve.
    ⑪ TERMINAISON — Attend la fin de l'épreuve, sans délai. [sort: non]
    """
    fin = os.path.join(travail, f"lot_{k:02d}.code")
    if os.path.exists(fin):
        return k, int(open(fin).read().strip())
    ecoute = os.path.join(travail, "ecoute")
    sortie = os.path.join(travail, f"lot_{k:02d}.out")
    env = dict(os.environ, PYTHONPATH=os.path.join(travail, "module"), SERIE_ECOUTE=ecoute, PYTHONUNBUFFERED="1",
               SERIE_EXECUTION=os.path.join(travail, "execution"))
    env.update(CERTIF.SANS_LA_CONFIGURATION_GIT_DE_LA_MACHINE)   # l'environnement où la nuit refait les essais
    with open(sortie + ".part", "w", encoding="utf-8") as s:
        code = subprocess.run([sys.executable, "-u", os.path.join(racine, epreuve), racine, "--saboter=" + ",".join(lot)],
                              cwd=racine, env=env, stdout=s, stderr=subprocess.STDOUT).returncode
    os.replace(sortie + ".part", sortie)
    open(fin, "w").write(str(code))
    print(f"ETAPE {heure()} lot {k} fini, code {code} ({len(lot)} sabotages)", flush=True)
    return k, code


def main():
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Voir la fiche en tête. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — Voir la fiche en tête.
    ④ CONDITIONS D'ENTRÉE — Voir la fiche en tête. ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1]
    ⑥ TRAITEMENT — Voir la fiche en tête. ⑦ UNITÉ — — ⑧ POURQUOI — Voir la fiche en tête.
    ⑨ CE QUI CLOCHE — Voir la fiche en tête. ⑩ EFFET — Voir la fiche en tête. ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    pos = [a for a in sys.argv[1:] if not a.startswith("--")]
    opt = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    if len(pos) != 3:
        print("ARRET usage : JOUER_UNE_SERIE_DE_SABOTAGES.py <racine> <épreuve> <relevé> [--parts=2] [--lot=21] [--travail=…]")
        return 2
    racine, epreuve, releve = os.path.realpath(pos[0]), pos[1], pos[2]
    parts, taille = int(opt.get("parts", 2)), int(opt.get("lot", 21))
    travail = os.path.realpath(opt.get("travail", os.path.join(racine, "..", "serie_" + os.path.basename(epreuve)[:-3])))
    try:
        noms = SERIE.noms_des_sabotages(os.path.join(racine, epreuve))
    except (OSError, SyntaxError, ValueError) as e:
        print(f"ARRET épreuve {epreuve} illisible : {type(e).__name__} : {e}")
        return 2
    if not noms:
        print(f"ARRET aucun dictionnaire SABOTAGES lisible dans {epreuve}")
        return 2
    # LA PORTÉE DU RELEVÉ, lue à la table de lancement par le certificateur (R-708) ; une racine sans table (un dépôt
    # d'essai) garde la portée d'origine, « lectures ».
    try:
        portee = (CERTIF.options_de_lancement(racine)[1].get(epreuve) or {}).get("portee")
    except FileNotFoundError:
        portee = None
    except ValueError as e:
        print(f"ARRET table de lancement illisible : {e}")
        return 2
    portee = SERIE.PORTEE_LECTURES if portee is None else portee
    if portee not in SERIE.PORTEES:
        print(f"ARRET portée du relevé inconnue pour {epreuve} : {portee!r}")
        return 2
    os.makedirs(os.path.join(travail, "module"), exist_ok=True)
    os.makedirs(os.path.join(travail, "ecoute"), exist_ok=True)
    os.makedirs(os.path.join(travail, "execution"), exist_ok=True)
    open(os.path.join(travail, "module", "sitecustomize.py"), "w").write(ECOUTE)
    depart = os.path.join(travail, "etat_du_depart.json")
    etat = etat_du_depot(racine)
    etat.pop(releve, None)        # le relevé lui-même change à chaque série
    if os.path.exists(depart):
        avant = json.load(open(depart, encoding="utf-8"))
        # Seuls les fichiers présents au départ comptent : un dossier jetable laissé par un lot coupé n'empêche pas
        # la reprise (mesuré le 16-10-2026 sur un dépôt d'essai : le relevé écrit dans la racine la refusait).
        differents = [c for c, e in avant.items() if etat.get(c) != e]
        if differents:
            print(f"ARRET le dépôt a changé depuis le départ de cette série ({travail}) : {', '.join(differents[:5])} "
                  "— prendre un dossier de travail neuf")
            return 2
        etat = avant
        print(f"ETAPE {heure()} reprise : dépôt identique au départ, lots déjà faits gardés", flush=True)
    else:
        json.dump(etat, open(depart, "w", encoding="utf-8"))
        open(os.path.join(travail, "debut.txt"), "w").write(datetime.datetime.now(PARIS).strftime("%d-%m-%Y %Hh%M"))
    lots = [noms[i:i + taille] for i in range(0, len(noms), taille)]
    print(f"ETAPE {heure()} {len(noms)} sabotages en {len(lots)} lots, {parts} à la fois", flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=parts) as g:
        codes = dict(g.map(lambda kl: jouer_un_lot(racine, epreuve, travail, *kl), enumerate(lots, 1)))
    # ⑤ le compte : chaque sabotage une fois, « mord »
    vus, lignes, z0 = {}, [], []
    for k in range(1, len(lots) + 1):
        try:
            sortie_du_lot = open(os.path.join(travail, f"lot_{k:02d}.out"), encoding="utf-8", errors="replace").read()
        except OSError:
            print(f"ARRET la sortie du lot {k} manque alors que son code est écrit : effacer lot_{k:02d}.code et relancer")
            return 2
        for l in sortie_du_lot.splitlines():
            m = LIGNE.match(l)
            if m:
                vus.setdefault(m.group(1), []).append(m.group(2))
                lignes.append(l)
            elif l.startswith("Z0 "):
                z0.append(f"lot {k} : {l}")
    manquent = [n for n in noms if n not in vus]
    doubles = [n for n, v in vus.items() if len(v) != 1]
    ne_mordent_pas = [n for n, v in vus.items() if v != ["mord"]]
    lots_rouges = [k for k, c in codes.items() if c != 0]
    if manquent:
        print(f"ERREUR {len(manquent)} sabotage(s) sans résultat : {', '.join(manquent[:8])}")
    # les fichiers lus : notés par l'écoute ET présents au départ (pas les dossiers jetables)
    lus = set()
    for f in os.listdir(os.path.join(travail, "ecoute")):
        for p in open(os.path.join(travail, "ecoute", f), encoding="utf-8", errors="replace").read().splitlines():
            if p.startswith(racine + os.sep):
                rel = os.path.relpath(p, racine).replace(os.sep, "/")
                m = re.match(r"^(.*/)?__pycache__/([^/.]+)\.[^/]+\.pyc$", rel)
                if m:
                    rel = (m.group(1) or "") + m.group(2) + ".py"
                if rel in etat:
                    lus.add(rel)
    # le code exécuté (portées « epreuve » et « code_execute ») : une propriété mesurée, ramenée au dépôt (R-708)
    executes = SERIE.fichiers_executes(os.path.join(travail, "execution"), etat)
    couverts = lus if portee == SERIE.PORTEE_LECTURES else executes
    # Un fichier disparu pendant la série est un changement, pas un plantage (relecture indépendante, 17-10-2026, tour
    # 15 : un fichier lu, effacé par l'épreuve, faisait sortir le joueur sur une trace, code 1, au lieu d'ARRET).
    change = [c for c in sorted(couverts | {epreuve}) if not os.path.isfile(os.path.join(racine, c))
              or SERIE.empreinte(os.path.join(racine, c)) != etat.get(c)]
    if change:
        print(f"ARRET {len(change)} fichier(s) lu(s) ont changé pendant la série : {', '.join(change[:5])}")
        return 2
    conforme = not (manquent or doubles or ne_mordent_pas or lots_rouges)
    entete = [f"série jouée du {open(os.path.join(travail, 'debut.txt')).read()} au "
              f"{datetime.datetime.now(PARIS):%d-%m-%Y %Hh%M} (Paris), {len(lots)} lots de {taille} au plus, {parts} à la fois,",
              f"par tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py ; {len(noms)} sabotages attendus, {len(vus)} joués, "
              f"{sum(v == ['mord'] for v in vus.values())} mordent ; lots rouges : {lots_rouges or 'aucun'}",
              f"portée du relevé : {portee}" + ("" if portee == SERIE.PORTEE_LECTURES else
                                                 " — empreintes du code EXÉCUTÉ par la série (évènement « exec »), sans "
                                                 "les données ; la nuit compare " + ("le seul code de l'épreuve (décision "
                                                 "n°71 du 01-11-2026, lue au mot)" if portee == SERIE.PORTEE_EPREUVE else
                                                 "tout ce code (choix D43 du Chat du 05-11-2026, à confirmer par "
                                                 "Jean-Luc)"))] + z0
    # Une seule version vivante : l'ancien relevé de la même série va dans archives/, sous un nom qui dit pourquoi.
    prefixe = re.sub(r"_[A-Z][a-z]{2}_\d{2}-\d{2}-\d{4}_\d{2}h\d{2}\.txt$", "_", os.path.basename(releve))
    dossier = os.path.join(racine, os.path.dirname(releve))
    for ancien in sorted(os.listdir(dossier)) if prefixe != os.path.basename(releve) and os.path.isdir(dossier) else []:
        if ancien.startswith(prefixe) and ancien != os.path.basename(releve):
            os.makedirs(os.path.join(racine, "archives"), exist_ok=True)
            os.replace(os.path.join(dossier, ancien), os.path.join(
                racine, "archives", ancien[:-4] + "_REMPLACE_PAR_" + os.path.basename(releve)))
            print(f"ETAPE {heure()} ancien relevé rangé dans archives/ : {ancien}")
    n = SERIE.ecrire_le_releve(racine, releve, epreuve, sorted(couverts), lignes, conforme, entete)
    print(f"FINI {heure()} relevé {releve} : {len(vus)} sabotages, {n} empreintes, "
          f"{'conforme' if conforme else 'NON CONFORME'}", flush=True)
    return 0 if conforme else 1


if __name__ == "__main__":
    sys.exit(main())
