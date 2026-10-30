#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_COPIE_DES_BOUCLES — Jeu 01-10-2026 (Paris)
Rôle : rougir AVANT qu'une boucle Cowork tombe parce qu'un programme qu'elle copie a gagné une dépendance.
Quand l'appeler : avant toute livraison qui touche un fichier de COPIE_DES_BOUCLES (programmes/CONTRATS_DES_FICHIERS.py)
ou cette liste (R-731).

À QUOI ÇA SERT. Les boucles Cowork de 07h05, 08h35 et 21h05 copient quelques fichiers du dépôt dans le dossier du projet,
puis les importent : l'étape 3 recalcule les signaux (la seule redondance de calcul de l'écosystème), l'étape 5bis tient le
second jeu de positions. Le 01-10-2026, la fusion a donné à TENIR_LES_POSITIONS.py deux imports (CONTRATS_DES_FICHIERS,
COMMUN) que leur ligne `cp` ne copiait pas : les deux étapes tombaient à l'import, et rien au dépôt ne le voyait (relecture
de Cowork aff6d33). La liste des fichiers copiés est désormais écrite une fois, dans COPIE_DES_BOUCLES ; ces épreuves la
confrontent au code et la font tourner seule.

LES ÉPREUVES :
E1 PROPRIÉTÉ : tout programme du dépôt qu'un programme de la liste importe (à tous les niveaux du code) ou dont il écrit le
   nom de fichier dans une chaîne de son code (« JUGE_DES_STRATEGIES.py » dans os.path.join, un tuple parcouru par une
   boucle…) est dans la liste — la liste est fermée ; le relevé se calibre sur le module C5 (qui doit dépendre du module
   de positions) et sur le texte libre de COMMUN.py (qui ne doit rien ajouter) ;
E2 dans un dossier vide qui tient lieu de projet, la liste copiée par programmes/COPIER_POUR_LES_BOUCLES.py — le programme
   que les boucles appellent — et rien d'autre : le calibrage sur le dépôt
   (`--calibrage`) rend 0 et dit « CALIBRAGE OK », et AUCUN fichier du dépôt ne change (empreinte de chaque fichier hors
   .git, avant et après) ;
E3 dans ce dossier, le recalcul des signaux par le module retrouve les deux signaux réels connus — Bureau Veritas le
   24-07-2026 et Unibail le 20-08-2026 (premiers trades du journal) ;
E4 dans ce dossier, `tenir`, avec les modules COPIÉS, refait les DEUX vrais trades du journal, qui sortent par deux
   chemins différents : Unibail, entrée le 21-08-2026 à 103,15, vente forcée (SL) le 27-08-2026, −3 196,25 € au barème
   réel (−2 796,25 € au courtage seul, montant du journal) ; Bureau Veritas, entrée le 27-07-2026 à 27,28, sortie à
   l'ouverture au-dessus de l'objectif (TP_GAP) le 29-07-2026 à 29,24, +6 473,97 € au barème réel, taxe de 400 € comprise
   (A-550, 29-10-2026 ; +6 873,97 € au tarif de 0,15 % par ordre seul ; le journal porte +6 884,75 €, calculé avec l'ancien forfait de 300 € :
   écart de 10,78 € documenté dans rapports/RAPPROCHEMENT_JOURNAL_REJEU_2026-09-29_22h00.md et à la ligne 335 du module
   de positions). C'est le chemin des entrées et des clôtures, qu'un `tenir` sans position ne traverse pas (relecteur du
   01-10-2026) ; la sortie sur objectif a été ajoutée au troisième tour, parce qu'une dépendance cachée dans cette seule
   branche passait.
Les sous-processus tournent avec `python3 -E` : un PYTHONPATH hérité ne doit pas cacher un fichier manquant.
LES SABOTAGES, avec les épreuves qui DOIVENT rougir (chacune est exigée) : S1 COMMUN.py retiré de la liste (E1, E2) · S2 un
import d'un programme hors liste en tête du module de positions (E1, E2) · S3 la liste perd le module du signal, que la boucle charge elle-même (E3, E4 ; le calibrage ne le voit pas : il
charge les modules du dépôt, et non les copies — relecteur du 01-10-2026) ·
S4 un import hors liste écrit dans une fonction, que l'import du module n'exécute pas (E1) · S5 un chargement par nom de
fichier hors liste, appelé par la fonction de séance du module de positions (E1, E4) · S6 le calibrage écrit un fichier
dans le dépôt (E2) · S7 le module ne rend plus aucun signal (E3) · S8 un nom de fichier hors liste dans un tuple parcouru par
une boucle, dans la fonction de séance (E1 ; relecteur, second tour) · S9 un nom de fichier COMPOSÉ à l'exécution, chargé
dans la seule branche de la sortie sur objectif (E4 ; E1 ne le voit pas, par construction — relecteur, troisième tour) ·
S10 le programme de copie ne vérifie plus que chaque fichier existe (E5) · S11 il annonce la copie sans copier (E2, E3, E4).
S12 il vérifie chaque fichier en le copiant, et non avant (E5 ; relecteur, quatrième tour).
E5 un clone auquel manque le seul DERNIER fichier de la liste : le programme de copie ne copie RIEN et rend un code non nul.

USAGE : python3 tests/EPREUVES_DE_LA_COPIE_DES_BOUCLES_Jeu_01-10-2026.py <racine du dépôt> [--saboter]
CODE : 0 si Z0 est vert et, avec --saboter, si chaque sabotage fait rougir CHAQUE épreuve qu'il vise ; 1 sinon ; 2 si un
sabotage ne s'applique plus.
"""
import ast, hashlib, json, os, re, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
CTR = "programmes/CONTRATS_DES_FICHIERS.py"
MODP = "programmes/MODULE_POSITIONS.py"
TEN = "programmes/TENIR_LES_POSITIONS.py"
C5 = "programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py"
COP = "programmes/COPIER_POUR_LES_BOUCLES.py"
_AIDE = ("def _aide():\n    import importlib.util, os\n"
         "    sp = importlib.util.spec_from_file_location('a', os.path.join(os.path.dirname("
         "os.path.abspath(__file__)), 'FAUT_IL_RATTRAPER.py'))\n"
         "    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)\n\n\n")
SABOTAGES = {
    "Z0": ([], set()),
    "S1_commun_oublie": ([(CTR, '    "programmes/COMMUN.py",\n', "")], {"E1", "E2"}),
    "S2_import_hors_liste": ([(MODP, "\nCAPITAL = 100_000.0\n", "\nimport FAUT_IL_RATTRAPER\nCAPITAL = 100_000.0\n")],
                             {"E1", "E2"}),
    "S3_module_du_signal_oublie": ([(CTR, '    "programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py",\n', "")],
                                   {"E3", "E4"}),
    "S4_import_dans_une_fonction": ([(MODP, "    import sys\n", "    import sys\n    import FAUT_IL_RATTRAPER\n")], {"E1"}),
    "S5_chargement_par_nom": ([(MODP, "\ndef tester_seance(", "\n" + _AIDE + "def tester_seance("),
                               (MODP, "    # LES DEUX SAUTS D'OUVERTURE D'ABORD", "    _aide()\n    # LES DEUX SAUTS D'OUVERTURE D'ABORD")], {"E1", "E4"}),
    "S8_nom_dans_un_tuple": ([(MODP, "    # LES DEUX SAUTS D'OUVERTURE D'ABORD",
                                "    for _n in ('FAUT_IL_RATTRAPER.py',):\n        pass\n    # LES DEUX SAUTS D'OUVERTURE D'ABORD")],
                             {"E1"}),
    "S9_nom_compose_sur_objectif": ([(MODP, "\ndef tester_seance(", "\n" + _AIDE.replace("'FAUT_IL_RATTRAPER.py'", "_x + '_IL_RATTRAPER.py'").replace("def _aide():\n", "def _aide():\n    _x = 'FAUT'\n") + "def tester_seance("),
                                      (MODP, '    if bar["open"] >= tp:\n        return bar["open"], "TP_GAP"', '    if bar["open"] >= tp:\n        _aide()\n        return bar["open"], "TP_GAP"')],
                                     {"E4"}),
    "S6_calibrage_ecrit": ([(TEN, "\ndef main():\n", "\ndef main():\n    open(os.path.join(sys.argv[1], 'TRACE_DU_CALIBRAGE'), 'w').write('x')\n")],
                           {"E2"}),
    "S10_copie_sans_verification": ([(COP, "    if not liste or manquants or doubles:", "    if not liste or doubles:")], {"E5"}),
    "S12_verification_en_cours_de_copie": ([(COP, "    if not liste or manquants or doubles:", "    if not liste or doubles:"),
                                            (COP, "        shutil.copyfile(os.path.join(depot, f), cible)\n",
                                             "        if not os.path.isfile(os.path.join(depot, f)):\n"
                                             "            print('COPIE DES BOUCLES IMPOSSIBLE'); return 1\n"
                                             "        shutil.copyfile(os.path.join(depot, f), cible)\n")], {"E5"}),
    "S11_copie_qui_ne_copie_rien": ([(COP, "        shutil.copyfile(os.path.join(depot, f), cible)\n", "        continue\n")], {"E2", "E3", "E4"}),
    "S7_aucun_signal": ([(C5, "\ndef signaux_c5etendu10(ohlcv):\n", "\ndef signaux_c5etendu10(ohlcv):\n    return []\n\n\ndef _ancien_signaux(ohlcv):\n")],
                        {"E3"}),
}
SIGNAUX_CONNUS = (("BUREAU_VERITAS", "2026-07-24"), ("UNIBAIL_RODAMCO", "2026-08-20"))
# DEPUIS LE 29-10-2026 (A-550), `tenir` chiffre les frais au barème réel : courtage ET taxe sur les transactions
# financières, 400,00 € à l'achat de ces deux valeurs, taxées en 2026 (donnees/VALEURS_TTF.csv). Les deux montants
# attendus sont ceux de l'ÉTUDE 18 (S9), retrouvés au centime par le calibrage de MODULE_POSITIONS : +6 473,97 € et
# −3 196,25 € ; au courtage seul, ils valaient +6 873,97 € et −2 796,25 €.
TRADES_CONNUS = [("BUREAU_VERITAS", "2026-07-27", 27.28, "2026-07-29", "TP_GAP", 6473.97),
                 ("UNIBAIL_RODAMCO", "2026-08-21", 103.15, "2026-08-27", "SL", -3196.25)]


def liste(depot):
    """Lit COPIE_DES_BOUCLES dans le module des contrats du dépôt donné et la rend.

    ① RÔLE — Prendre la liste là où elle est écrite, jamais la recopier (R-708 : deux implémentations d'une même chose
      divergent toujours).
    ② CONTEXTE D'APPEL — `epreuves`, une fois.
    ③ ENTRÉE — `depot` : la racine du dépôt éprouvé.
    ④ CONDITIONS D'ENTRÉE — Le dépôt porte programmes/CONTRATS_DES_FICHIERS.py avec COPIE_DES_BOUCLES.
    ⑤ SORTIE — UNE valeur : la liste des chemins sous la racine.
      [rend: 1]
    ⑥ TRAITEMENT — importer le module sous un nom propre, lire la constante.
    ⑦ UNITÉ — Des chemins relatifs à la racine du dépôt.
    ⑧ POURQUOI — Les sabotages changent la liste dans une copie : il faut lire celle de la copie.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Importe un module.
    ⑪ TERMINAISON — Rend la main, ou lève si l'import échoue.
      [sort: non]
    """
    import importlib.util
    sp = importlib.util.spec_from_file_location("ctr_%d" % id(depot), os.path.join(depot, CTR))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return list(m.COPIE_DES_BOUCLES)


def dependances(depot, chemin):
    """Rend les programmes du dépôt dont un programme dépend par son code.

    ① RÔLE — La propriété E1, pour un fichier.
    ② CONTEXTE D'APPEL — `epreuves`, une fois par programme de la liste.
    ③ ENTRÉE — `depot` : la racine · `chemin` : le programme, sous la racine.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe et se lit en Python.
    ⑤ SORTIE — UNE valeur : l'ensemble des chemins « programmes/X.py » que le fichier importe (`import X`, `from X
      import …`, à tous les niveaux) ou dont il écrit le nom de fichier « X.py » dans une chaîne de son code — un
      argument d'appel, une constante, un tuple parcouru par une boucle.
      [rend: 1]
    ⑥ TRAITEMENT — parcourir l'arbre syntaxique ; écarter les chaînes posées seules comme une instruction (les textes
      explicatifs, en tête ou ailleurs : elles ne font rien) ; garder les noms dont le fichier existe dans programmes/.
    ⑦ UNITÉ — Des chemins sous la racine.
    ⑧ POURQUOI — Un import ou un nom de fichier écrit dans le code se lit sans rien exécuter ; une propriété ne dépend ni
      du jour ni des données.
    ⑨ CE QUI CLOCHE — Un nom de fichier composé à l'exécution (concaténé, lu dans un fichier) n'est pas vu ; un import
      relatif est ignoré (les programmes ne forment pas un paquet) ; une recherche par début de nom, sans « .py », non
      plus — le juge le fait dans son `main` pour son module de statistiques (`trouver(base, "MODULE_STATISTIQUES")`,
      ligne 2778), hors du chemin des boucles et facultatif. Seul le chemin réel (E2 à E4) les prendrait, et seulement
      sur les chemins qu'il traverse : la vente forcée et la sortie sur objectif (S9 le prouve), pas l'échéance. À l'inverse, un nom de fichier cité dans un message (une chaîne qui sert
      à afficher) compte comme une dépendance : la liste s'élargit à tort plutôt que de se taire.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main, ou lève sur un fichier illisible.
      [sort: non]
    """
    d = os.path.join(depot, "programmes")
    existants = {f for f in os.listdir(d) if f.endswith(".py")}
    arbre = ast.parse(open(os.path.join(depot, chemin), encoding="utf-8").read())
    vus = set()
    # LES CHAÎNES POSÉES SEULES (textes explicatifs, en tête ou ailleurs) ne font rien : écartées.
    seules = {id(n.value) for n in ast.walk(arbre) if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant)}
    for n in ast.walk(arbre):
        mods = [a.name for a in n.names] if isinstance(n, ast.Import) else (
            [n.module] if isinstance(n, ast.ImportFrom) and n.module and not n.level else [])
        vus |= {m.split(".")[0] + ".py" for m in mods}
        # TOUTE CHAÎNE DU CODE qui nomme un programme, et non seulement un argument d'appel : un tuple parcouru par
        # une boucle échappait (relecteur, second tour du 01-10-2026 ; c'est ainsi que le module C5 charge le module
        # de positions).
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in seules:
            vus |= set(re.findall(r"[A-Za-z0-9_\-]+\.py\b", n.value))
    return {"programmes/" + f for f in vus if f in existants and "programmes/" + f != chemin}


def empreinte(racine):
    """Rend l'empreinte de chaque fichier sous la racine, hors .git.

    ① RÔLE — Dire si le calibrage a écrit quoi que ce soit dans le dépôt, fichiers ignorés et déjà modifiés compris.
    ② CONTEXTE D'APPEL — `epreuves`, avant et après le calibrage.
    ③ ENTRÉE — `racine` : le dossier.
    ④ CONDITIONS D'ENTRÉE — Le dossier existe.
    ⑤ SORTIE — UNE valeur : un dictionnaire chemin → empreinte sha256.
      [rend: 1]
    ⑥ TRAITEMENT — parcourir l'arborescence, lire chaque fichier.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — `git status` ne voit ni un fichier ignoré ni une écriture de plus dans un fichier déjà modifié, et ne dit
      rien sans `.git` (relecteur du 01-10-2026).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main, ou lève si un fichier ne se lit pas.
      [sort: non]
    """
    e = {}
    for d, sous, fichiers in os.walk(racine):
        sous[:] = [x for x in sous if x not in (".git", "__pycache__")]
        for f in fichiers:
            p = os.path.join(d, f)
            e[os.path.relpath(p, racine)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return e


SCRIPT = (
    "import sys, json, importlib.util; sys.path.insert(0, '.')\n"
    "import TENIR_LES_POSITIONS as T\n"
    "D = sys.argv[1]\n"
    "c = T.charger_cours_du_banc('.', D + '/donnees/cac40_ohlcv.csv', D + '/donnees/claude_cours_nouveaux.csv')\n"
    "sp = importlib.util.spec_from_file_location('m', 'MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py')\n"
    "M = importlib.util.module_from_spec(sp); sp.loader.exec_module(M)\n"
    "vus = [[v, d] for v, d in json.loads(sys.argv[2]) if any(c[v][x['i']]['date'] == d for x in M.signaux_c5etendu10(c[v]))]\n"
    "print('SIGNAUX', json.dumps(vus))\n"
    "mod = T.charger_module_positions(T.trouver_module('.'))\n"
    "def pos(s, v, d, cpt): return {'strategie': s, 'valeur': v, 'date_signal': d, 'date_entree': '',\n"
    "    'prix_entree': T.INCONNU, 'tp': T.INCONNU, 'sl': T.INCONNU, 'horizon_fin': T.INCONNU, 'statut': T.EN_ATTENTE,\n"
    "    'comptabilite': cpt, 'regles_pre_trade': '', 'explication': ''}\n"
    "r = T.tenir([pos('COURS_BAS_ARGENT_REVIENT_10', 'BUREAU_VERITAS', '2026-07-24', T.JETONS_ILLIMITES),\n"
    "            pos('COURS_BAS_ARGENT_REVIENT_6', 'UNIBAIL_RODAMCO', '2026-08-20', T.UN_JETON)], c, [], None, mod, base='.')\n"
    "print('TRADES', json.dumps([[t['valeur'], t['date_entree'], float(t['prix_entree']), t['date_sortie'],\n"
    "                            t['motif_sortie'], float(t['pnl_net_eur'])] for t in r['trades']]))\n")


def epreuves(depot, tmp):
    """Joue E1 à E4 sur la copie `depot` et rend la liste (code de l'épreuve, nom, verdict).

    ① RÔLE — Les épreuves décrites en tête.
    ② CONTEXTE D'APPEL — `main`, une fois par sabotage.
    ③ ENTRÉE — `depot` : une copie du dépôt, sabotée ou non · `tmp` : un dossier jetable.
    ④ CONDITIONS D'ENTRÉE — La copie porte ses données (cours, registre des stratégies).
    ⑤ SORTIE — UNE valeur : la liste des triplets (« E1 »…, nom, vrai si verte).
      [rend: 1]
    ⑥ TRAITEMENT — ① la propriété sur le code · ② copier la liste dans un dossier vide · ③ calibrer sur la copie du dépôt
      en mesurant ses fichiers avant et après · ④ y recalculer les signaux connus et y refaire le trade connu.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — E1 voit une dépendance nouvelle sans rien lancer ; E2 à E4 empruntent le chemin réel de la boucle, avec les
      fichiers copiés.
    ⑨ CE QUI CLOCHE — Les épreuves ne lisent pas le texte des tâches : que la boucle copie exactement la liste, c'est Cowork
      qui le confronte. E3 lit les cours comme la boucle (historique figé et fichier de la collecte) : si ce dernier perdait
      ses séances de juillet et d'août, E3 rougirait à tort.
    ⑩ EFFET — Écrit dans `tmp` ; lance deux processus.
    ⑪ TERMINAISON — Rend la main ; chaque processus est borné à 300 secondes, et un dépassement ou une sortie illisible
      lève, ce qui arrête les épreuves en erreur (code non nul).
      [sort: non]
    """
    res = []
    L = liste(depot)
    progs = [x for x in L if x.endswith(".py")]
    hors = sorted({f"{p} dépend de {x}" for p in progs for x in dependances(depot, p) if x not in L})
    # LE MOTIF SE CALIBRE (instructions du projet, § 4) : sur un cas connu qui doit sortir — le module C5 charge le
    # module de positions par son nom, écrit dans un tuple — et sur un cas qui ne doit pas sortir — le texte libre de
    # COMMUN.py, posé seul, cite audit_ecosysteme.py.
    calibre = ("programmes/MODULE_POSITIONS.py" in dependances(depot, C5)
               and "programmes/audit_ecosysteme.py" not in dependances(depot, "programmes/COMMUN.py"))
    res.append(("E1", "la liste est fermée : aucune dépendance hors liste" + (" — " + " · ".join(hors) if hors else "")
                + ("" if calibre else " — LE RELEVÉ DES DÉPENDANCES N'EST PAS CALIBRÉ"), not hors and calibre))
    projet = os.path.join(tmp, "projet")
    os.makedirs(projet)
    # LA COPIE PAR LE PROGRAMME QUE LES BOUCLES APPELLENT, et non par une boucle d'ici : le témoin emprunte le chemin réel
    # (décision de Jean-Luc du 01-10-2026 à 18h19, « Trouve une solution pour ne pas attendre demain »).
    avant = empreinte(depot)
    cop = subprocess.run([sys.executable, "-E", "-B", os.path.join(depot, COP), depot, projet],
                         capture_output=True, text=True, errors="replace", timeout=300)
    copies = sorted(os.listdir(projet))   # relevé AVANT le calibrage, qui dépose le cache de Python dans ce dossier
    cal = subprocess.run([sys.executable, "-E", "TENIR_LES_POSITIONS.py", depot, "--calibrage"], cwd=projet,
                         capture_output=True, text=True, errors="replace", timeout=300)
    apres = empreinte(depot)
    change = sorted(k for k in set(avant) | set(apres) if avant.get(k) != apres.get(k))
    res.append(("E2", "le programme de copie copie la liste, et elle seule calibre sur le dépôt sans rien y écrire"
                + (" — écrit : " + ", ".join(change[:3]) if change else "")
                + ("" if cop.returncode == 0 else " — copie : code " + str(cop.returncode)),
                cop.returncode == 0 and copies == sorted(os.path.basename(f) for f in L)
                and cal.returncode == 0 and "CALIBRAGE OK" in cal.stdout and not change))
    p = subprocess.run([sys.executable, "-E", "-c", SCRIPT, depot, json.dumps(SIGNAUX_CONNUS)], cwd=projet,
                       capture_output=True, text=True, errors="replace", timeout=300)
    lu = {l.split(" ", 1)[0]: json.loads(l.split(" ", 1)[1]) for l in p.stdout.splitlines() if l.startswith(("SIGNAUX ", "TRADES "))}
    res.append(("E3", "les deux signaux réels connus sont retrouvés avec les fichiers copiés",
                sorted(map(tuple, lu.get("SIGNAUX", []))) == sorted(SIGNAUX_CONNUS)))
    res.append(("E4", "les deux vrais trades du journal (vente forcée, sortie sur objectif) sont refaits avec les modules copiés",
                sorted(tuple(t) for t in lu.get("TRADES", [])) == sorted(TRADES_CONNUS)))
    # E5 — UN CLONE AUQUEL MANQUE LE SEUL DERNIER FICHIER DE LA LISTE : le programme ne copie RIEN et rend un code non nul
    # (R-734). Le dernier, et non tous : une copie qui s'arrêterait au premier absent aurait déjà copié les autres, et
    # mélangé dans le dossier du projet des programmes neufs et un registre ancien (relecteur, quatrième tour, sabotage S12).
    mini = os.path.join(tmp, "clone_incomplet")
    for f in L[:-1] + [CTR]:
        os.makedirs(os.path.dirname(os.path.join(mini, f)), exist_ok=True)
        shutil.copy(os.path.join(depot, f), os.path.join(mini, f))
    vide = os.path.join(tmp, "projet_vide")
    os.makedirs(vide)
    rate = subprocess.run([sys.executable, "-E", "-B", os.path.join(depot, COP), mini, vide],
                          capture_output=True, text=True, errors="replace", timeout=300)
    res.append(("E5", "un clone auquel manque le dernier fichier de la liste : rien n'est copié et le code est non nul",
                rate.returncode != 0 and not os.listdir(vide) and "COPIE DES BOUCLES IMPOSSIBLE" in rate.stdout))
    return res


def main():
    """Joue les épreuves sans sabotage, puis chaque sabotage avec --saboter.

    ① RÔLE — Dire si les épreuves prouvent quelque chose.
    ② CONTEXTE D'APPEL — Le lancement du fichier.
    ③ ENTRÉE — La ligne de commande.
    ④ CONDITIONS D'ENTRÉE — La racine donnée est une copie complète du dépôt.
    ⑤ SORTIE — UNE valeur : le code de sortie.
      [rend: 1]
    ⑥ TRAITEMENT — pour chaque cas : copier le dépôt, saboter, jouer, et exiger que chaque épreuve visée rougisse.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration (R-731) ; exiger chaque
      épreuve visée, et non « au moins une », donne ses dents à chacune (relecteur du 01-10-2026).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Crée puis efface des copies jetables ; affiche un compte rendu.
    ⑪ TERMINAISON — Rend la main par son code.
      [sort: non]
    """
    choix = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
    bon = True
    for sab in choix:
        modifs, visees = SABOTAGES[sab]
        tmp = tempfile.mkdtemp(prefix="copie_boucles_")
        try:
            depot = os.path.join(tmp, "depot")
            shutil.copytree(DEPOT, depot, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            for f, a, b in modifs:
                t = open(os.path.join(depot, f), encoding="utf-8").read()
                if t.count(a) != 1:
                    print(f"SABOTAGE {sab} INAPPLICABLE : ancre absente ou multiple dans {f}")
                    return 2
                open(os.path.join(depot, f), "w", encoding="utf-8").write(t.replace(a, b))
            res = epreuves(depot, tmp)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        rouges = [(c, x) for c, x, ok in res if not ok]
        print(f"== {sab} : {len(res) - len(rouges)} vertes, {len(rouges)} rouges")
        for c, x in rouges:
            print(f"     ROUGE {c} {x}")
        manquent = sorted(visees - {c for c, _ in rouges})
        if sab == "Z0" and rouges:
            bon = False
        if sab != "Z0" and (not rouges or manquent):
            print(f"     ⚠ LE SABOTAGE {sab} NE FAIT PAS ROUGIR " + (", ".join(manquent) if manquent else "aucune épreuve"))
            bon = False
    print("VERDICT :", "tout est conforme" if bon else "NON CONFORME")
    return 0 if bon else 1


if __name__ == "__main__":
    sys.exit(main())
