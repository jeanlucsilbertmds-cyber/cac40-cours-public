#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_CIRCUIT_DES_SERIES — Jeu 05-11-2026 (Paris). Simulation uniquement.

① RÔLE — Donner des dents, AU DÉPÔT, aux gardes du circuit des séries sur GitHub et à ses deux programmes de parts
  (superviseur R-759 du 05-11-2026, M3 : quatre gardes n'avaient de dents que dans des harnais hors du dépôt, et
  tests/outils/jouer_une_part.py, tests/outils/rassembler_les_parts.py aucune).
② CONTEXTE D'APPEL — Chaque nuit par la certification (épreuve de tests/, lancée avec la racine) ; à la main avant toute
  livraison qui touche le fabricant du circuit public ou les parts (R-731) :
  python3 tests/EPREUVES_DU_CIRCUIT_DES_SERIES_Jeu_05-11-2026.py <racine> [--saboter]
③ ENTRÉE — La racine du dépôt (on y prend programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, tests/outils/ et programmes/).
④ CONDITIONS D'ENTRÉE — git est installé ; aucun réseau n'est utilisé (dépôts nus locaux).
⑤ SORTIE — Le code de sortie : 0 si G0 à G4, M1 à M3, X3, MB1 à MB4, X2, N1 à N5, P1 à P8, C1 à C5, R1 à R4 donnent la réponse attendue et, avec --saboter, si
  chaque sabotage en fait échouer au moins un ; 1 sinon ; 2 si un sabotage ne s'applique plus.
  [rend: 1]
⑥ TRAITEMENT — G (le pas « version » et le pas « meme_depot » du circuit FABRIQUÉ, extraits du gabarit et joués par
  bash contre un dépôt privé nu local ; le jeton vide, l'aide aux identifiants n'a pas d'effet sur un dépôt local) :
  G0 version en attente lancée depuis sa branche → 0 · G1 lancée depuis une autre branche publique → 1 · G2 deux
  versions en attente au privé → 1 · G3 le privé a avancé après le clonage → 1 · G4 « meme_depot » : HEAD égal au
  commit de la préparation → 0, autre commit → 1. M (la poussée vers le public, `publier` et le crochet du fabricant,
  dans de vrais clones git) : M1 LE CHEMIN RÉEL (tour 3, B-1) : un dépôt privé que `main` accepte, sur
  « travail-essai » ; le fabricant lancé en ligne de commande « <privé> <clone public> --publier » sur un clone public
  sur « travail-essai » qui SUIT origin/main avec push.default upstream : il pose LUI-MÊME le crochet et publie à
  travers lui → code 0, travail-essai du public = HEAD du clone, main du public inchangé · M2 le crochet posé par
  `main`, sur ce même clone : un « git push » ordinaire, « git push origin HEAD:main », et la poussée d'un autre commit
  que HEAD vers la bonne branche, refusés, main inchangé · X3 la branche publique a reçu un commit d'ailleurs : une
  nouvelle publication rend 1 et la branche n'est pas écrasée (jamais de poussée forcée) · M3 privé sur
  travail-essai, clone public sur main (d'un public neuf) : `publier` refuse, aucune branche créée · MB1 à MB4, X2
  (tour 4, M-b, « main --publier » sur un public NEUF ; ce qui part au public = ce que `main` a écrit ou retiré) :
  MB1 un fichier égaré portant un jeton fictif et tmp_essai/entete.txt → 1, les deux NOMMÉS, aucune branche
  publique · MB2 un fichier égaré sans jeton → 1, nommé · MB3 arbre propre → 0, le programme ZZ publié · MB4 ZZ
  retiré du privé → 0, retiré du public · X2 un crochet « post-receive » du public remet la branche à son ancienne
  pointe après la poussée → 1, « n'est pas le commit poussé ». N1 le filet des gabarits accepte le gabarit
  des séries, et refuse ce gabarit privé de « persist-credentials: false », puis d'un « shell: bash » d'un pas qui
  reçoit le jeton ; « max-parallel » vaut au plus 16 ; le joueur des parts et le rassembleur sont lancés sous
  « unshare -rn » · N2 (tour 3, M-2) le filet accepte le gabarit (T0) et refuse F1 à F7 : jeton dans l'env du job,
  du circuit, toJSON(secrets), secrets['…'], un pas bash à jeton qui lance un programme de la version, qui écrit ou
  copie vers $GITHUB_ENV, qui écrit une variable dans un fichier (F5 à F7 ajoutés AVANT le code de la version, pour
  n'être refusés que pour leur raison) ; (tour 4, M-a) refuse F9 (une ligne de mise au point qui calcule le base64
  dans « Deposer ») et F13 (« echo » du jeton), accepte F10 (« set -x » en tête) ; (tour 5) refuse F14
  (« ${JETON:0:20} », relecture de Cowork du 06-11-2026, D4), F15 (un pas à jeton inoffensif APRÈS du code de la
  version, propriété ⑨ du filet) et F16 (une expression « ${{ … }} » dans le script d'un pas à jeton, propriété ⑩),
  et accepte F15b (le même pas que F15, avant le code de la version) · N3 (tour 3, M-3, contre l'accident ; tour 5,
  superviseur R-759 du 06-11-2026, §4 ①) : des crochets posés dans .git/hooks du dépôt cloné, une configuration
  globale qui les sert, « core.fsmonitor » et un filtre « clean » dans .git/config du dépôt cloné, une fausse
  commande « git » dans le PATH ; les pas « deposer » (d'une part) et « lire_les_parts » du circuit FABRIQUÉ, joués
  par bash contre un privé nu local avec un jeton FICTIF : déposés et lus, et aucune forme du jeton vue par un
  piège ; des témoins prouvent d'abord que chaque piège voit le jeton d'un git ordinaire ; (tour 6, R5-1) le VRAI
  .gitignore de la racine dans le dossier de travail et un « .pyc » dans « tmp_lot_01 » : la branche déposée ne porte
  aucun « .pyc » et porte lot_01.code (témoin : git check-ignore exclut ce chemin) ; ce .gitignore remplacé par un
  lien symbolique → non nul, « lien symbolique » · N4 (tour 5, superviseur
  R-759 du 06-11-2026, §2 ; relecture de Cowork, D2 et D3) : CHAQUE pas à jeton du gabarit fabriqué, dans l'ordre du
  gabarit, « set -x » en tête et toutes les traces de git allumées (TRACES, GIT_TRACE_REDACT=0 compris), joué par
  bash contre un serveur local qui EXIGE une identification (`servir`) → 0, au moins une identification reçue
  pendant le pas, et AUCUNE forme du jeton fictif (lui, son base64 avec ou sans « x-access-token: », le préfixe
  PREFIXE_DU_BASE64) dans sa sortie entière ; témoins : le serveur refuse qui ne s'identifie pas, et un en-tête
  calculé (l'ancienne forme) fait écrire le base64 par les traces · N5 (tour 5) : le pas « deposer » d'une part avec
  PART=« 0:refs/heads/main » → non nul, « valeur refusee pour PART », main du privé inchangé. P (les parts, sur un dépôt d'essai minuscule dont l'épreuve EXÉCUTE un module dans une copie) :
  P1 joueur seul et 2 parts rassemblées → codes 0, relevés identiques hors ligne 3 et ligne « joué par » · P2 une
  part dont le flux « execution » est vidé → rassemblement 2, aucun relevé · P3 une part sans sa place libre
  minimale (un « lot_NN.place » retiré) → rassemblement 2 · P4 un relevé retenu où A2 fait tomber H2 → rassemblement
  1, « raisons à examiner » · P5 (tour 3, B-2) un lot compté dont la place est retirée, puis reprise → 1, « place libre
  minimale None » · P6 (M-1) TMPDIR sur /dev/shm, autre système de fichiers → ARRET, 2 · P7 (M-1) chaque lot voit son
  temporaire dans « tmp_lot_NN » du dossier de travail · P8 (tour 6, R5-4) le joueur lancé avec chaque variable de
  FICHIERS_DE_COMMANDES_DE_GITHUB du fabricant posée : l'épreuve jouée n'en reçoit aucune (témoin : elle reçoit une
  variable ordinaire posée au même endroit).
  C (tests/outils/comparer_les_releves.py, relecture du 05-11-2026, B1) : C1 le relevé de P1 contre sa copie en
  « \r\n » → 1 · C2 contre sa copie dont seule la ligne « joué par » diffère → 0 · C3 (tour 3, m-3) sans ligne
  « joué par » à droite → 1 · C4 « --calibrage » entre deux relevés locaux → 1 · C5 « --calibrage », machine contre
  GitHub → 0 (C3 à C5 : depuis le 08-11-2026, relevé n°327, les deux côtés sont fabriqués par l'épreuve, « machine
  locale » à gauche et « GitHub » à droite, quelle que soit la machine qui joue l'épreuve : sur GitHub, le relevé de
  P1 disait déjà « GitHub » et C5 rougissait). R (tests/outils/ranger_le_releve.py,
  N2) : R1 un relevé dont la ligne « joué par » dit un autre commit que la pointe de la version → 1, rien rangé ·
  R2 le commit de la pointe → 0, rangé · R2bis, R3, R4 (tour 3, M-4) la ligne écrite par `ligne_joue_par` du joueur
  puis jugée par le rangeur : pointe propre → 0 ; arbre modifié non commité (« MODIFIÉ ») → 1 ; SERIE_COMMIT posé à
  la main hors de GitHub sur une copie sans .git (« inconnu ») → 1.
⑦ UNITÉ — Des codes de sortie.
⑧ POURQUOI — Superviseur R-759 du 05-11-2026, M3 (« Verser au dépôt les épreuves des gardes G1 à G4 (dont un cas
  meme_depot) et celles de jouer_une_part.py et rassembler_les_parts.py »), M2 et N1. Avec l'option 2 (décision de
  Jean-Luc du 05-11-2026 à 13h36), le circuit qui tourne est celui de la version éprouvée : seule une épreuve du dépôt,
  jouée chaque nuit sur main, garde ses gardes.
⑨ CE QUI CLOCHE — Rien n'est joué sur GitHub : actions/checkout est imité par « git clone », ETAPE_MUETTE par bash ;
  l'adresse du dépôt privé écrite dans le gabarit est remplacée par un dépôt nu local (G, N3, N5) ou par le serveur
  local de `servir` (N4, en HTTP simple et non HTTPS : ce que github.com accepte de l'aide aux identifiants reste
  THÉORIQUE). N4 exige l'interface locale : lancée sous « unshare -rn », l'épreuve doit d'abord monter « lo », sinon
  N4 rougit (« serveur local impossible » ou code non nul : rien de prouvé). N3 joue l'ACCIDENT
  (modèle de menace de Jean-Luc du 05-11-2026, 17h36), pas un code écrit pour nuire ($GITHUB_ENV d'un pas sans jeton,
  /proc, sudo : BACKLOG). P6 exige /dev/shm sur un autre disque : sinon il rougit (rien de prouvé). Le
  pas « version » est extrait du gabarit par lecture d'indentation, pas par un lecteur YAML. P ne joue pas une vraie
  série (HL, Yahoo).
⑩ EFFET — Écrit dans des dossiers jetables, effacés à la fin.
⑪ TERMINAISON — Rend la main ; chaque lancement est borné à 300 secondes ; sort par sys.exit.
  [sort: oui]
"""
import base64
import http.server
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import threading

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
FABRICANT = "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"
OUTILS = ("tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py", "tests/outils/jouer_une_part.py",
          "tests/outils/rassembler_les_parts.py")
COMPARATEUR = "tests/outils/comparer_les_releves.py"
RANGEUR = "tests/outils/ranger_le_releve.py"
GIT_ENV = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_COUNT="0",
               GIT_AUTHOR_NAME="essai", GIT_AUTHOR_EMAIL="essai@essai", GIT_COMMITTER_NAME="essai",
               GIT_COMMITTER_EMAIL="essai@essai", GIT_TERMINAL_PROMPT="0")
# TOUR 5 (superviseur R-759 du 06-11-2026, §2) : les traces de git que la mise au point allume, toutes à la fois ;
# GIT_TRACE_REDACT=0 demande à git d'écrire EN CLAIR l'en-tête « Authorization » de ses traces HTTP (le pas à jeton
# doit le remettre à 1 lui-même : SANS_RIEN_DE_LA_VERSION du fabricant).
TRACES = {"GIT_TRACE": "1", "GIT_TRACE2": "1", "GIT_TRACE2_EVENT": "1", "GIT_TRACE2_PERF": "1", "GIT_TRACE_CURL": "1",
          "GIT_CURL_VERBOSE": "1", "GIT_TRACE_PACKET": "1", "GIT_TRACE_SETUP": "1", "GIT_TRACE_PERFORMANCE": "1",
          "GIT_TRACE_REDACT": "0"}
# « x-access-token: » en base64 (15 octets, donc 20 caractères sans « = ») : le début de TOUT en-tête d'identification
# de ce circuit, quel que soit le jeton (même préfixe que l'action T4-4 du BACKLOG pour programmes/FORME_D_UN_JETON.py).
PREFIXE_DU_BASE64 = base64.b64encode(b"x-access-token:").decode()


class ServeurQuiExigeUneIdentification(http.server.BaseHTTPRequestHandler):
    """Un serveur git par HTTP, local, qui refuse toute requête sans la bonne identification « Basic ».

    Chaque requête : sans l'en-tête « Authorization » attendu → 401 et « WWW-Authenticate: Basic » (git demande alors
    une identification à son aide, comme chez github.com) ; avec → la requête passe à « git http-backend ». La classe
    reçoit, par `servir`, trois attributs : `racine` (le dossier des dépôts nus), `attendu` (le base64 attendu) et
    `recus` (une liste où chaque requête ajoute « identifié », « sans » ou « faux »).
    """
    racine, attendu, recus = "", "", []

    def log_message(self, *args):
        """Tait le journal de chaque requête.

        ① RÔLE — Garder la sortie de l'épreuve lisible.
        ② CONTEXTE D'APPEL — http.server, à chaque requête.
        ③ ENTRÉE — Le format et ses valeurs (ignorés).
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Aucune valeur. [rend: rien]
        ⑥ TRAITEMENT — Rien.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Par défaut, http.server écrit chaque requête sur la sortie d'erreur de l'épreuve.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main. [sort: non]
        """

    def servir_une_requete(self):
        """Répond à une requête GET ou POST de git.

        ① RÔLE — Exiger l'identification, puis servir le dépôt.
        ② CONTEXTE D'APPEL — http.server, par do_GET et do_POST.
        ③ ENTRÉE — La requête (chemin, en-têtes, corps, éventuellement découpé en morceaux « chunked »).
        ④ CONDITIONS D'ENTRÉE — git est installé (« git http-backend »).
        ⑤ SORTIE — Aucune valeur ; la réponse est écrite à git. [rend: rien]
        ⑥ TRAITEMENT — le corps lu (morceaux recollés) ; CHAQUE en-tête « Authorization » (git en envoie deux
          identiques avec « -c http.extraheader », mesuré le 06-11-2026) comparé à « basic <attendu> » (le mot
          « basic » sans égard à la casse, le base64 à l'identique) ; aucun, ou un différent : 401 ; sinon « git http-backend »
          lancé avec les variables CGI, sa réponse (en-têtes, « Status: », corps) recopiée.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Un dépôt nu servi par chemin de fichier ne demande aucune identification : le jeton n'y est jamais
          employé, et l'absence de fuite ne prouverait rien. Mesure du superviseur R-759 du 06-11-2026, §2, refaite ici.
        ⑨ CE QUI CLOCHE — Un serveur d'essai : ni HTTPS, ni protocole « dumb », ni compression de la réponse. Le corps
          d'une requête est lu entier en mémoire (les dépôts de l'épreuve sont minuscules).
        ⑩ EFFET — Ajoute un mot à `recus` ; une poussée identifiée écrit dans le dépôt nu servi.
        ⑪ TERMINAISON — Rend la main ; « git http-backend » est borné à 120 s. [sort: non]
        """
        corps = b""
        if self.headers.get("Transfer-Encoding", "").lower() == "chunked":
            while True:
                n = int(self.rfile.readline().strip().split(b";")[0] or b"0", 16)
                if n == 0:
                    self.rfile.readline()
                    break
                corps += self.rfile.read(n)
                self.rfile.readline()
        elif self.command == "POST":
            corps = self.rfile.read(int(self.headers.get("Content-Length") or 0))
        valeurs = [v.partition(" ") for v in self.headers.get_all("Authorization") or []]
        if not valeurs or any(m.lower() != "basic" or v.strip() != self.attendu for m, _, v in valeurs):
            self.recus.append("faux" if valeurs else "sans")
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="epreuve"')
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        self.recus.append("identifié")
        chemin, _, requete = self.path.partition("?")
        env = dict(os.environ, GIT_PROJECT_ROOT=self.racine, GIT_HTTP_EXPORT_ALL="1", REQUEST_METHOD=self.command,
                   PATH_INFO=chemin, QUERY_STRING=requete, REMOTE_USER="epreuve", REMOTE_ADDR="127.0.0.1",
                   CONTENT_TYPE=self.headers.get("Content-Type", ""), CONTENT_LENGTH=str(len(corps)),
                   HTTP_CONTENT_ENCODING=self.headers.get("Content-Encoding", ""),
                   GIT_PROTOCOL=self.headers.get("Git-Protocol", ""), GIT_CONFIG_GLOBAL=os.devnull,
                   GIT_CONFIG_NOSYSTEM="1")
        p = subprocess.run(["git", "http-backend"], input=corps, capture_output=True, env=env, timeout=120)
        tete, separe, reste = p.stdout.partition(b"\r\n\r\n")
        if not separe:
            tete, _, reste = p.stdout.partition(b"\n\n")
        entetes = [l.split(":", 1) for l in tete.decode("latin-1").splitlines() if ":" in l]
        statut = next((int(v.split()[0]) for k, v in entetes if k.lower() == "status"), 200)
        self.send_response(statut)
        for k, v in entetes:
            if k.lower() != "status":
                self.send_header(k, v.strip())
        self.send_header("Content-Length", str(len(reste)))
        self.end_headers()
        self.wfile.write(reste)

    do_GET = do_POST = servir_une_requete


def servir(racine, attendu, recus):
    """Démarre ServeurQuiExigeUneIdentification sur 127.0.0.1, à un port libre, dans un fil à part ; rend le serveur.

    ① RÔLE — Donner au cas N4 un dépôt privé qui exige une identification, comme github.com.
    ② CONTEXTE D'APPEL — `tour`, cas N4.
    ③ ENTRÉE — `racine` : le dossier des dépôts nus servis · `attendu` : le base64 de « x-access-token:<jeton> »
      attendu · `recus` : la liste où noter chaque requête.
    ④ CONDITIONS D'ENTRÉE — L'interface locale (127.0.0.1) est joignable ; sous « unshare -rn », elle doit avoir été
      montée (« lo » est éteinte dans un espace réseau neuf).
    ⑤ SORTIE — UNE valeur : le serveur (son port : server_address[1]). Lève OSError si le port ne s'ouvre pas.
      [rend: 1]
    ⑥ TRAITEMENT — une sous-classe qui porte les trois valeurs ; ThreadingHTTPServer ; serve_forever dans un fil
      « démon ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Fiche de ServeurQuiExigeUneIdentification.servir_une_requete, ⑧.
    ⑨ CE QUI CLOCHE — Le fil vit jusqu'à `shutdown` (appelé par `tour`) ou la fin du processus.
    ⑩ EFFET — Ouvre un port local.
    ⑪ TERMINAISON — Rend la main aussitôt. [sort: non]
    """
    classe = type("ServeurDeLEpreuve", (ServeurQuiExigeUneIdentification,),
                  {"racine": racine, "attendu": attendu, "recus": recus})
    serveur = http.server.ThreadingHTTPServer(("127.0.0.1", 0), classe)
    threading.Thread(target=serveur.serve_forever, daemon=True).start()
    return serveur


EPR = '''import os, sys, shutil, subprocess, tempfile, importlib.util
SABOTAGES = {"A1": 1, "A2": 2, "A3": 3}
if len(sys.argv) > 2 and sys.argv[1] == "--cas":
    c = sys.argv[2]
    sp = importlib.util.spec_from_file_location("M", os.path.join(c, "programmes", "M.py"))
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    sys.exit(0 if m.VAL == 1 else 1)
racine = os.path.abspath(sys.argv[1])
choix = [a.split("=", 1)[1] for a in sys.argv[2:] if a.startswith("--saboter=")]
if os.environ.get("ESSAI_TEMP_VU"):
    open(os.environ["ESSAI_TEMP_VU"], "a").write(tempfile.gettempdir() + "\\n")
if os.environ.get("ESSAI_ENV_VU"):
    open(os.environ["ESSAI_ENV_VU"], "a").write(" ".join(sorted(os.environ)) + "\\n")
d = tempfile.mkdtemp(prefix="essai_parts_"); r = os.path.join(d, "r")
shutil.copytree(racine, r, ignore=shutil.ignore_patterns("archives", "resultats"))
code = subprocess.run([sys.executable, "-B", os.path.join(r, "tests", "EPR.py"), "--cas", r]).returncode
shutil.rmtree(d)
print("Z0 programme tel quel : tous les cas conformes")
for n in (choix[0].split(",") if choix else []):
    print(f"{n} mord : ['H1']" if code == 0 else f"{n} NE MORD PAS : []")
'''
TABLE = ('{"epreuves": {}, "series_hors_de_la_nuit": {"tests/EPR.py": {"releve": "tests/resultats/SERIE_*.txt", '
         '"essais_refaits_chaque_nuit": 0, "portee_du_releve": "code_execute"}}}\n')
REL = "tests/resultats/SERIE_DE_SABOTAGES_DE_L_ESSAI_Jeu_05-11-2026_14h00.txt"
RETENU = "tests/resultats/SERIE_DE_SABOTAGES_DE_L_ESSAI_Mer_04-11-2026_14h00.txt"
SABOTAGES = {
    "SG1_branche_lancee_non_comparee": [(FABRICANT, '''          [ "$VERSION" = "$BRANCHE_PUBLIQUE" ] ||''',
                                         '''          true ||''')],
    "SG2_versions_en_attente_non_comptees": [(FABRICANT, '''            [ "$attente" = "refs/heads/$VERSION" ] ||''',
                                              '''            true ||''')],
    "SG3_pointe_non_comparee": [(FABRICANT, '''          [ -n "$pointe" ] && [ "$(git -C "$GITHUB_WORKSPACE" -c core.hooksPath=/dev/null rev-parse HEAD)" = "$pointe" ] ||''',
                                 '''          true ||''')],
    "SG4_meme_depot_non_compare": [(FABRICANT, '''          [ "$(git rev-parse HEAD)" = "$SHA" ] ||''', '''          true ||''')],
    "SM1_poussee_sans_cible": [(FABRICANT, '''    p = git("push", "-q", "origin", "HEAD:" + cible)''',
                                '''    p = git("push", "-q")''')],
    "SM2_crochet_sans_dents": [(FABRICANT, '''  [ "$r_ref" = "refs/heads/$b" ] ||''', '''  true ||''')],
    # TOUR 3 (superviseur R-759 du 05-11-2026, 17h13, §C) : chaque pièce touchée, retirée seule, sur le chemin réel
    "SB1_crochet_juge_la_forme_ecrite": [(FABRICANT, '''  [ "$r_ref" = "refs/heads/$b" ] ||''',
                                          '''  case "$l_ref" in refs/heads/*) ;; *) exit 1;; esac; [ "$r_ref" = "refs/heads/$b" ] ||''')],
    "SB1_crochet_sans_commit_compare": [(FABRICANT, '''  [ "$l_sha" = "$tete" ] ||''', '''  true ||''')],
    # TOUR 4 (superviseur R-759 du 05-11-2026, 18h56, §E) : M-b, X2, M-a
    "SMb_publier_revient_a_add_A": [(FABRICANT, "    presents = [c for c in liste if os.path.lexists(os.path.join(public, c))]\n",
                                     "    git(\"add\", \"-A\")\n    presents = []\n"),
                                    (FABRICANT, "    if en_trop:\n", "    if False:\n")],
    "SMb_etat_non_confronte": [(FABRICANT, "    if en_trop:\n", "    if False:\n")],
    "SX2_publier_sans_relire_la_pointe": [(FABRICANT, "    if not distante or distante[0] != tete:", "    if False:")],
    # TOUR 5 (superviseur R-759 du 06-11-2026, §2) : plus aucune valeur tirée du jeton dans le shell ; chaque retour à
    # l'ancienne forme doit faire paraître une forme du jeton dans la sortie d'un pas, traces allumées (N4)
    "SMa_base64_recalcule": [(FABRICANT, '''AUTORISATION = ("''',
                              '''AUTORISATION = ("          AUTH64=$(printf 'x-access-token:%s' \\"$JETON\\" | base64 -w0)\\n"
                "          echo \\"::add-mask::$AUTH64\\"\\n"
                "''')],
    "SMa_en_tete_calcule": [(FABRICANT, '''                "          A=(-c credential.helper= -c \\"credential.helper=$AIDE\\")\\n")''',
                             '''                "          A=(-c \\"http.extraheader=AUTHORIZATION: basic $(printf 'x-access-token:%s' \\"$JETON\\" | base64 -w0)\\")\\n")''')],
    "SMa_traces_http_non_caviardees": [(FABRICANT, '''export PATH=/usr/bin:/bin GIT_TRACE_REDACT=1 GIT_CONFIG_NOSYSTEM=1''',
                                        '''export PATH=/usr/bin:/bin GIT_CONFIG_NOSYSTEM=1''')],
    "SMa_filet_ne_cherche_plus_JETON": [(FABRICANT, '''                if "JETON" in reste:''', '''                if False:''')],
    "SX3_publier_pousse_en_force": [(FABRICANT, '''    p = git("push", "-q", "origin", "HEAD:" + cible)''',
                                     '''    p = git("push", "-q", "--force", "origin", "HEAD:" + cible)''')],
    "SB2_lot_sans_place_admis": [(OUTILS[0], "        except (OSError, ValueError):\n            return None\n    return min(places)",
                                  "        except (OSError, ValueError):\n            continue\n    return min(places)")],
    "SM1_temporaire_d_un_autre_disque_admis": [(OUTILS[0], "    if os.stat(temporaire).st_dev != os.stat(travail).st_dev:",
                                                "    if False:")],
    "SM1_temporaire_du_lot_non_force": [(OUTILS[0], "    env.update({v: temporaire for v in VARIABLES_DU_TEMPORAIRE})",
                                         "    pass")],
    "SN2_secrets_hors_des_places_admis": [(FABRICANT, '''                if "secrets" in l.lower() and i not in permises:''',
                                           '''                if False:''')],
    "SN2_commandes_non_lues": [(FABRICANT, "                hors = sorted(set(commandes) - COMMANDES_DU_SYSTEME)",
                                "                hors = []")],
    "SN2_redirections_non_lues": [(FABRICANT, '''                          if any(c != "/dev/null" for c in cibles) else "")''',
                                   '''                          if False else "")''')],
    "SN2_fichiers_de_github_non_lus": [(FABRICANT, "                if any(f in pas for f in FICHIERS_DE_COMMANDES_DE_GITHUB):",
                                        "                if False:")],
    # TOUR 5 (superviseur R-759 du 06-11-2026, §4 ①) : la poussée ne lance plus git dans le dossier de travail
    "SN3_git_dans_le_dossier_de_travail": [(FABRICANT, '''          cd "$T" && git init -q . || { echo "::error::POUSSEE REFUSEE — dossier neuf impossible"; exit 1; }''',
                                            '''          git init -q . || { echo "::error::POUSSEE REFUSEE — dossier neuf impossible"; exit 1; }''')],
    "SN3_parts_lues_dans_le_depot_joue": [(FABRICANT, '''          cd "$T" && git init -q . || { echo "::error::dossier neuf impossible"; exit 1; }''',
                                           '''          cd "$GITHUB_WORKSPACE" || { echo "::error::dossier neuf impossible"; exit 1; }''')],
    # TOUR 6 (relecture neuve du tour 5, R5-1 et R5-4) : chaque geste ajouté, retiré seul
    "SN3_exclusions_du_depot_non_recopiees": [(FABRICANT, '''cp -- "$GITHUB_WORKSPACE/.gitignore" .git/info/exclude''',
                                               '''true''')],
    "SN3_gitignore_en_lien_symbolique_admis": [(FABRICANT, '''[ -L "$GITHUB_WORKSPACE/.gitignore" ]''',
                                                '''[ -L "$GITHUB_WORKSPACE/.nulle_part" ]''')],
    "SP8_fichiers_de_github_transmis_au_code_joue": [(OUTILS[0], "        env.pop(v, None)\n", "        pass\n")],
    "SN3_path_non_fixe": [(FABRICANT, '''"          export PATH=/usr/bin:/bin GIT_TRACE_REDACT=1''', '''"          export GIT_TRACE_REDACT=1''')],
    "SN3_configuration_globale_lue": [(FABRICANT, ''' GIT_CONFIG_GLOBAL=/dev/null\\n"''', '''\\n"''')],
    "SM4_publier_sans_ligne_modifie": [(OUTILS[0], '''                commit += " MODIFIÉ"''', '''                pass''')],
    "SM4_serie_commit_lu_hors_de_github": [(OUTILS[0], '''    commit = os.environ.get("SERIE_COMMIT", "").strip() if sur_github else ""''',
                                            '''    commit = os.environ.get("SERIE_COMMIT", "").strip()''')],
    "SM4_rangeur_admet_modifie": [(RANGEUR, "    if d and d.group(2):", "    if False:")],
    "Sm3_comparateur_sans_ligne_joue_par": [(COMPARATEUR, "        if len(joue) != 1:", "        if False:")],
    "Sm3_calibrage_sans_machine": [(COMPARATEUR, "        if calibrage and not joue[0].startswith(JOUE_PAR + machine + \" ; \"):",
                                    "        if False:")],
    "SM3_publier_sans_garde_de_branche": [(FABRICANT, '''    if not b or refus_de_branche(prive, public):''',
                                           '''    if not b:''')],
    "SN1_filet_sans_persist": [(FABRICANT, '''                    if not re.search(r"^\\s*persist-credentials:\\s*false\\s*$", pas, re.M):''',
                                '''                    if False:''')],
    # TOUR 5 : les deux propriétés nouvelles du filet (⑨ l'ordre, ⑩ les expressions), l'ordre du gabarit lui-même, et
    # la vérification des valeurs de la matrice dans la poussée
    "SN5_pas_a_jeton_apres_le_code_admis": [(FABRICANT, '''                    if a_jeton and premier is not None and a > premier and not (rang == len(suite) - 1 and pousse):''',
                                             '''                    if False:''')],
    "SN5_lecture_des_parts_apres_le_code": [(FABRICANT, '''apres_le_clonage=SERIES_PARTS_VERTES + SERIES_LIRE_LES_PARTS,''',
                                             '''apres_le_clonage=SERIES_PARTS_VERTES,'''),
                                            (FABRICANT, '''%(reseau)s      - name: Rassembler et ecrire le releve''',
                                             '''%(reseau)s%(lire)s      - name: Rassembler et ecrire le releve'''),
                                            (FABRICANT, '''    "meme_depot": SERIES_MEME_DEPOT, "copie": SERIES_COPIE,''',
                                             '''    "lire": SERIES_LIRE_LES_PARTS, "meme_depot": SERIES_MEME_DEPOT, "copie": SERIES_COPIE,''')],
    "SN6_expression_dans_un_pas_a_jeton_admise": [(FABRICANT, '''                if "${{" in script:''', '''                if False:''')],
    "SN7_valeur_de_la_matrice_non_verifiee": [(FABRICANT, '''""" + nom + """" =~ ^[A-Za-z0-9_-]+$ ]] ||''',
                                               '''""" + nom + """" =~ . ]] ||''')],
    "SN2_rassembler_sans_reseau_coupe": [(FABRICANT, '''          unshare -rn python3 -B -u tests/outils/rassembler_les_parts.py''',
                                          '''          python3 -B -u tests/outils/rassembler_les_parts.py''')],
    "SC1_fins_de_ligne_traduites": [(COMPARATEUR, 'open(chemins[0], encoding="utf-8", newline="")',
                                     'open(chemins[0], encoding="utf-8")'),
                                    (COMPARATEUR, 'open(chemins[1], encoding="utf-8", newline="")',
                                     'open(chemins[1], encoding="utf-8")')],
    "SR1_commit_du_releve_non_compare": [(RANGEUR, "branche and tete == m.group(1) == pointe", "branche")],
    "SP2_rassembleur_sans_flux_execution": [("tests/outils/rassembler_les_parts.py",
                                             "            if attendus and not PART.ecoute_nomme(",
                                             "            if False and not PART.ecoute_nomme(")],
    # la garde retirée ET le minimum pris sur les parts qui en ont un (sinon le min() d'un None plante, et la garde
    # générale rend 2 pour une autre raison : premier passage du 05-11-2026, « NE MORD PAS »)
    "SP3_place_des_parts_non_exigee": [("tests/outils/rassembler_les_parts.py", "    if sans:\n", "    if False:\n")],
}


def lancer(args, env=None, cwd=None):
    """Lance une commande ; rend (code, sortie et erreur réunies).

    ① RÔLE — Un lancement borné.
    ② CONTEXTE D'APPEL — Partout dans `tour`.
    ③ ENTRÉE — `args` : la commande ; `env` : l'environnement (GIT_ENV par défaut) ; `cwd` : le dossier.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : (code, texte). [rend: 1]
    ⑥ TRAITEMENT — subprocess.run, borné à 300 s.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — Un dépassement lève TimeoutExpired, qui fait sortir l'épreuve sur une trace (code non nul).
    ⑩ EFFET — Ce que fait la commande.
    ⑪ TERMINAISON — Rend la main ; 300 s au plus. [sort: non]
    """
    p = subprocess.run(args, capture_output=True, text=True, env=env or GIT_ENV, cwd=cwd, timeout=300)
    return p.returncode, p.stdout + p.stderr


def pas_du_gabarit(texte, ident):
    """Rend le bloc « run » d'un pas du gabarit (premier pas d'identifiant `ident`), sans son indentation.

    ① RÔLE — Jouer le pas tel que le circuit le porte, sans le recopier.
    ② CONTEXTE D'APPEL — `tour`, cas G.
    ③ ENTRÉE — `texte` : le gabarit des séries ; `ident` : la valeur de « id: ».
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le script, ou "" si le pas ou son bloc manque. [rend: 1]
    ⑥ TRAITEMENT — la ligne « id: <ident> », puis la ligne « run: | », puis les lignes plus indentées qu'elle.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Fiche en tête, ⑨.
    ⑨ CE QUI CLOCHE — Le premier pas de ce nom seulement (« meme_depot » existe dans deux jobs, identique).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    lignes = texte.split("\n")
    debut = [i for i, l in enumerate(lignes) if l.strip() == "id: " + ident]
    if not debut:
        return ""
    i = debut[0]
    while i < len(lignes) and lignes[i].strip() != "run: |":
        i += 1
    if i == len(lignes):
        return ""
    marge = len(lignes[i]) - len(lignes[i].lstrip())
    corps = []
    for l in lignes[i + 1:]:
        if l.strip() and len(l) - len(l.lstrip()) <= marge:
            break
        corps.append(l[marge + 2:])
    return "\n".join(corps) + "\n"


def charger(chemin, nom):
    """Charge un programme comme un module.

    ① RÔLE — Appeler les fonctions du fabricant de la racine éprouvée.
    ② CONTEXTE D'APPEL — `tour`.
    ③ ENTRÉE — `chemin`, `nom`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le module. [rend: 1]
    ⑥ TRAITEMENT — importlib.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — Le code de tête du programme s'exécute (le fabricant construit ses gabarits à l'import).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]
    """
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def depot_d_essai(racine, d, nom):
    """Fabrique le dépôt d'essai des cas P ; rend son chemin.

    ① RÔLE — Un dépôt minuscule où une série de 3 sabotages tourne en quelques secondes.
    ② CONTEXTE D'APPEL — `tour`, cas P.
    ③ ENTRÉE — `racine` : la racine éprouvée ; `d` : le dossier jetable ; `nom`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin. [rend: 1]
    ⑥ TRAITEMENT — programmes/ (liens vers ceux de la racine), les trois outils copiés, l'épreuve EPR, un module M,
      la table de lancement (portée « code_execute »), un relevé retenu CONFORME où chaque sabotage fait tomber H1.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le témoin de la raison du joueur exige un relevé retenu.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans `d`.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    r = os.path.join(d, nom)
    os.makedirs(os.path.join(r, "programmes"))
    for f in os.listdir(os.path.join(racine, "programmes")):
        if f.endswith(".py"):
            shutil.copyfile(os.path.join(racine, "programmes", f), os.path.join(r, "programmes", f))
    for o in OUTILS:
        os.makedirs(os.path.dirname(os.path.join(r, o)), exist_ok=True)
        shutil.copyfile(os.path.join(racine, o), os.path.join(r, o))
    os.makedirs(os.path.join(r, "tests", "resultats"))
    for c, texte in (("tests/EPR.py", EPR), ("programmes/M.py", "VAL = 1\n"),
                     ("tests/LANCEMENT_DES_EPREUVES.json", TABLE),
                     (RETENU, "# RELEVÉ\n# épreuve : tests/EPR.py\nA1 mord : ['H1']\nA2 mord : ['H1']\n"
                              "A3 mord : ['H1']\nVERDICT : tout est conforme\n")):
        with open(os.path.join(r, c), "w", encoding="utf-8") as f:
            f.write(texte)
    return r


def tour(racine):
    """Joue G, M, N, P avec les programmes de `racine` ; rend la liste des cas faux.

    ① RÔLE — Un tour d'épreuves.
    ② CONTEXTE D'APPEL — `main`, une fois tel quel puis une fois par sabotage.
    ③ ENTRÉE — `racine` : une racine qui porte le fabricant, tests/outils/, programmes/ et le .gitignore (N3 ; absent,
      le témoin de N3 rougit).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des noms des cas faux. [rend: 1]
    ⑥ TRAITEMENT — Fiche en tête, ⑥.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Fiche en tête, ⑧.
    ⑨ CE QUI CLOCHE — Fiche en tête, ⑨.
    ⑩ EFFET — Dossiers jetables, effacés.
    ⑪ TERMINAISON — Rend la main ; chaque lancement borné à 300 s. [sort: non]
    """
    faux = []
    d = tempfile.mkdtemp(prefix="circuit_series_")
    try:
        F = charger(os.path.join(racine, FABRICANT), "FABRICANT_EPROUVE")
        # ---- G : le pas « version » et « meme_depot », joués contre un privé nu local
        prive = os.path.join(d, "prive.git")
        graine = os.path.join(d, "graine")
        lancer(["git", "init", "-q", "--bare", "-b", "main", prive])
        lancer(["git", "init", "-q", "-b", "main", graine])
        open(os.path.join(graine, "a.txt"), "w").write("main\n")
        lancer(["git", "-C", graine, "add", "-A"])
        lancer(["git", "-C", graine, "commit", "-qm", "main"])
        lancer(["git", "-C", graine, "checkout", "-qb", "travail-essai"])
        open(os.path.join(graine, "a.txt"), "a").write("en attente\n")
        lancer(["git", "-C", graine, "commit", "-qam", "en attente"])
        lancer(["git", "-C", graine, "push", "-q", prive, "main", "travail-essai"])
        ws = os.path.join(d, "ws")
        lancer(["git", "clone", "-q", "-b", "travail-essai", prive, ws])
        version = os.path.join(d, "version.sh")
        meme = os.path.join(d, "meme_depot.sh")
        open(version, "w").write(pas_du_gabarit(F.SERIES, "version").replace(F.DEPOT_PRIVE_ADRESSE, prive))
        open(meme, "w").write(pas_du_gabarit(F.SERIES, "meme_depot"))

        def pas(script, **env):
            return lancer(["bash", "-e", script], env=dict(GIT_ENV, JETON="", GITHUB_WORKSPACE=ws, **env), cwd=ws)[0]

        if pas(version, VERSION="travail-essai", BRANCHE_PUBLIQUE="travail-essai") != 0:
            faux.append("G0 (version en attente depuis sa branche refusée)")
        if pas(version, VERSION="travail-essai", BRANCHE_PUBLIQUE="main") != 1:
            faux.append("G1 (lancée depuis une autre branche publique, admise)")
        lancer(["git", "-C", graine, "push", "-q", prive, "travail-essai:travail-autre"])
        if pas(version, VERSION="travail-essai", BRANCHE_PUBLIQUE="travail-essai") != 1:
            faux.append("G2 (deux versions en attente, admises)")
        lancer(["git", "-C", graine, "push", "-q", prive, "--delete", "travail-autre"])
        open(os.path.join(graine, "a.txt"), "a").write("avance\n")
        lancer(["git", "-C", graine, "commit", "-qam", "avance"])
        lancer(["git", "-C", graine, "push", "-q", prive, "travail-essai"])
        if pas(version, VERSION="travail-essai", BRANCHE_PUBLIQUE="travail-essai") != 1:
            faux.append("G3 (le clone n'est plus la pointe, admis)")
        tete = lancer(["git", "-C", ws, "rev-parse", "HEAD"])[1].strip()
        if pas(meme, SHA=tete) != 0 or pas(meme, SHA="0" * 40) != 1:
            faux.append("G4 (meme_depot : le commit de la préparation n'est pas comparé)")
        # ---- M : la poussée vers le public
        pub = os.path.join(d, "public.git")
        lancer(["git", "init", "-q", "--bare", "-b", "main", pub])
        semis = os.path.join(d, "semis")
        lancer(["git", "init", "-q", "-b", "main", semis])
        open(os.path.join(semis, "p.txt"), "w").write("public main\n")
        lancer(["git", "-C", semis, "add", "-A"])
        lancer(["git", "-C", semis, "commit", "-qm", "public main"])
        lancer(["git", "-C", semis, "push", "-q", pub, "main"])
        main_avant = lancer(["git", "-C", pub, "rev-parse", "main"])[1].strip()
        priv = os.path.join(d, "priv")
        lancer(["git", "clone", "-q", "-b", "travail-essai", prive, priv])
        # M1, LE CHEMIN RÉEL (tour 3, B-1) : un dépôt privé que `main` accepte (programmes/, fiches de circuit, table de
        # lancement de la racine), sur travail-essai ; le fabricant lancé en ligne de commande avec --publier pose
        # LUI-MÊME le crochet, puis publie à travers lui (la relecture du tour 2 l'a vu refuser à chaque fois)
        privm = os.path.join(d, "privm")
        for sous in ("programmes", os.path.join(".github", "workflows"), "tests"):
            os.makedirs(os.path.join(privm, sous))
        for f in os.listdir(os.path.join(racine, "programmes")):
            if f.endswith(".py"):
                shutil.copyfile(os.path.join(racine, "programmes", f), os.path.join(privm, "programmes", f))
        for f in os.listdir(os.path.join(racine, ".github", "workflows")):
            shutil.copyfile(os.path.join(racine, ".github", "workflows", f), os.path.join(privm, ".github", "workflows", f))
        shutil.copyfile(os.path.join(racine, F.LANCEMENT), os.path.join(privm, F.LANCEMENT))
        lancer(["git", "init", "-q", "-b", "travail-essai", privm])
        lancer(["git", "-C", privm, "add", "-A"])
        lancer(["git", "-C", privm, "commit", "-qm", "version en attente"])
        c1 = os.path.join(d, "c1")
        lancer(["git", "clone", "-q", pub, c1])
        lancer(["git", "-C", c1, "checkout", "-q", "-b", "travail-essai", "--track", "origin/main"])
        lancer(["git", "-C", c1, "config", "push.default", "upstream"])
        code, sortie = lancer([sys.executable, "-B", os.path.join(racine, FABRICANT), privm, c1, "--publier"])
        apres = lancer(["git", "-C", pub, "rev-parse", "main"])[1].strip()
        poussee = lancer(["git", "-C", pub, "rev-parse", "travail-essai"])[1].strip()
        crochet = os.path.isfile(os.path.join(c1, ".git", "hooks", "pre-push"))
        if (code != 0 or not crochet or apres != main_avant
                or poussee != lancer(["git", "-C", c1, "rev-parse", "HEAD"])[1].strip()):
            faux.append(f"M1 (main --publier : code {code}, crochet posé {crochet}, main du public "
                        f"{'inchangé' if apres == main_avant else 'TOUCHÉ'} ; {sortie.strip().splitlines()[-1:]})")
        # M2 : le crochet que `main` a posé, sur le même clone : un « git push » ordinaire (amont origin/main), puis
        # « HEAD:main », refusés ; main du public inchangé
        open(os.path.join(c1, "p.txt"), "a").write("geste manuel\n")
        lancer(["git", "-C", c1, "commit", "-qam", "geste manuel"])
        k1 = lancer(["git", "-C", c1, "push", "-q"])[0]
        k2 = lancer(["git", "-C", c1, "push", "-q", "origin", "HEAD:main"])[0]
        lancer(["git", "-C", c1, "commit", "-q", "--allow-empty", "-m", "second geste"])   # HEAD~1 : en avance, pas HEAD
        k3 = lancer(["git", "-C", c1, "push", "-q", "origin", "HEAD~1:refs/heads/travail-essai"])[0]
        apres = lancer(["git", "-C", pub, "rev-parse", "main"])[1].strip()
        if k1 == 0 or k2 == 0 or k3 == 0 or apres != main_avant:
            faux.append(f"M2 (crochet : git push {k1}, HEAD:main {k2}, un autre commit que HEAD {k3}, main "
                        f"{'inchangé' if apres == main_avant else 'TOUCHÉ'})")
        # X3 : la branche publique a divergé (un commit d'ailleurs) ; une nouvelle publication est refusée, jamais forcée
        etranger = os.path.join(d, "etranger")
        if lancer(["git", "clone", "-q", "-b", "travail-essai", pub, etranger])[0] != 0:
            faux.append("X3 (aucune branche travail-essai au public : la première publication n'a pas eu lieu)")
        else:
            open(os.path.join(etranger, "e.txt"), "w").write("commit d'ailleurs\n")
            lancer(["git", "-C", etranger, "add", "-A"])
            lancer(["git", "-C", etranger, "commit", "-qm", "d'ailleurs"])
            lancer(["git", "-C", etranger, "push", "-q", "origin", "travail-essai"])
            avant_x3 = lancer(["git", "-C", pub, "rev-parse", "travail-essai"])[1].strip()
            lancer(["git", "-C", c1, "reset", "-q", "--hard", "HEAD~2"])
            # (tour 4) plus de « p.txt » modifié ici : M-b le refuserait AVANT la poussée, et SX3 ne mordrait plus
            kx3, _ = lancer([sys.executable, "-B", os.path.join(racine, FABRICANT), privm, c1, "--publier"])
            apres_x3 = lancer(["git", "-C", pub, "rev-parse", "travail-essai"])[1].strip()
            if kx3 != 1 or apres_x3 != avant_x3:
                faux.append(f"X3 (branche publique divergente : publication code {kx3}, "
                            f"{'intacte' if apres_x3 == avant_x3 else 'ÉCRASÉE'})")
        old = os.environ.copy()
        # M3 sur un public NEUF (seulement main) : sans la garde de `publier`, la poussée créerait travail-essai depuis
        # main (premier passage du 05-11-2026 : sur le public de M1, git refusait pour une autre raison, non-fast-forward)
        pub3 = os.path.join(d, "public3.git")
        lancer(["git", "init", "-q", "--bare", "-b", "main", pub3])
        lancer(["git", "-C", semis, "push", "-q", pub3, "main"])
        c3 = os.path.join(d, "c3")
        lancer(["git", "clone", "-q", pub3, c3])
        open(os.path.join(c3, "p.txt"), "a").write("version en attente sur main\n")
        os.environ.update({k: v for k, v in GIT_ENV.items() if k.startswith("GIT_")})
        try:
            # (tour 4) p.txt est dans la liste : sinon M-b refusait avant la garde de branche, et le sabotage
            # SM3_publier_sans_garde_de_branche ne mordait plus (premier passage du 05-11-2026, 19h25)
            code3, _ = F.publier(priv, c3, ["p.txt"])
        finally:
            os.environ.clear()
            os.environ.update(old)
        branches3 = lancer(["git", "-C", pub3, "for-each-ref", "--format=%(refname)"])[1].split()
        if code3 != 1 or branches3 != ["refs/heads/main"]:
            faux.append(f"M3 (privé travail-essai vers clone public main : code {code3})")
        # MB1 à MB4, X2 (tour 4, M-b, superviseur R-759 du 05-11-2026 à 18h56) : sur le CHEMIN RÉEL, « main --publier »
        # sur un public NEUF ; ce qui part au public = ce que `main` a écrit ou retiré, ni plus ni moins
        pub4 = os.path.join(d, "public4.git")
        lancer(["git", "init", "-q", "--bare", "-b", "main", pub4])
        lancer(["git", "-C", semis, "push", "-q", pub4, "main"])
        c4 = os.path.join(d, "c4")
        lancer(["git", "clone", "-q", pub4, c4])
        lancer(["git", "-C", c4, "checkout", "-q", "-b", "travail-essai"])
        zz = "programmes/ZZ_RETIRE_PAR_L_EPREUVE.py"
        open(os.path.join(privm, zz), "w").write("VALEUR = 1\n")
        lancer(["git", "-C", privm, "add", "-A"])
        lancer(["git", "-C", privm, "commit", "-qm", "un programme qui sera retiré"])

        def publier4():
            k, o = lancer([sys.executable, "-B", os.path.join(racine, FABRICANT), privm, c4, "--publier"])
            pointe = lancer(["git", "-C", pub4, "rev-parse", "--verify", "-q", "refs/heads/travail-essai"])
            arbre = lancer(["git", "-C", pub4, "ls-tree", "-r", "--name-only", "travail-essai"])[1].split() \
                if pointe[0] == 0 else []
            return k, o, pointe[1].strip() if pointe[0] == 0 else "", arbre
        # MB1 : un fichier égaré portant un jeton FICTIF, et tmp_essai/entete.txt (cas 4 de la relecture du tour 3)
        os.makedirs(os.path.join(c4, "tmp_essai"))
        open(os.path.join(c4, "note_du_chat.txt"), "w").write("jeton=FICTIF_JETON_DE_L_EPREUVE_123\n")
        import base64 as _b64e   # l'en-tête calculé ici : écrit en clair, ce fichier serait refusé au public (M5)
        open(os.path.join(c4, "tmp_essai", "entete.txt"), "w").write(
            "AUTHORIZATION: basic " + _b64e.b64encode(b"x-access-token:FICTIF").decode() + "\n")
        k, o, pointe, arbre = publier4()
        if k != 1 or pointe or "note_du_chat.txt" not in o or "tmp_essai/entete.txt" not in o:
            faux.append(f"MB1 (fichiers égarés avec un jeton fictif : code {k}, branche publique "
                        f"{'CRÉÉE' if pointe else 'absente'}, nommés {'note_du_chat.txt' in o}/{'tmp_essai/entete.txt' in o})")
        os.remove(os.path.join(c4, "note_du_chat.txt"))
        shutil.rmtree(os.path.join(c4, "tmp_essai"))
        # MB2 : un fichier égaré SANS jeton : refusé aussi (la propriété porte sur la liste, pas sur le contenu)
        open(os.path.join(c4, "autre.txt"), "w").write("rien de secret\n")
        k, o, pointe, arbre = publier4()
        if k != 1 or pointe or "autre.txt" not in o:
            faux.append(f"MB2 (fichier égaré sans jeton : code {k}, branche publique {'CRÉÉE' if pointe else 'absente'})")
        os.remove(os.path.join(c4, "autre.txt"))
        # MB3 : arbre propre : publié, le programme ZZ compris
        k, o, pointe, arbre = publier4()
        if k != 0 or pointe != lancer(["git", "-C", c4, "rev-parse", "HEAD"])[1].strip() or zz not in arbre:
            faux.append(f"MB3 (arbre propre : code {k}, {zz} publié {zz in arbre})")
        # MB4 : le programme retiré du privé est retiré du public
        lancer(["git", "-C", privm, "rm", "-q", zz])
        lancer(["git", "-C", privm, "commit", "-qm", "programme retiré"])
        k, o, pointe, arbre = publier4()
        if k != 0 or not arbre or zz in arbre:
            faux.append(f"MB4 (programme retiré : code {k}, encore au public {zz in arbre})")
        # X2 : un crochet du public déplace la branche après la poussée ; `publier` relit la pointe et refuse
        crochet4 = os.path.join(pub4, "hooks", "post-receive")
        with open(crochet4, "w") as f:
            f.write('#!/bin/sh\nwhile read o n r; do if [ "$r" = refs/heads/travail-essai ] && '
                    '[ "$o" != 0000000000000000000000000000000000000000 ]; then git update-ref "$r" "$o"; fi; done\n')
        os.chmod(crochet4, 0o755)
        open(os.path.join(privm, "programmes", "ZZ_SECOND.py"), "w").write("VALEUR = 2\n")
        lancer(["git", "-C", privm, "add", "-A"])
        lancer(["git", "-C", privm, "commit", "-qm", "second"])
        k, o, pointe, arbre = publier4()
        if k != 1 or "n'est pas le commit poussé" not in o:
            faux.append(f"X2 (pointe publique déplacée après la poussée : code {k})")
        # ---- N : le jeton pas par pas, les machines, le réseau coupé
        try:
            F.verifier_les_gabarits_publics({"series": F.SERIES}, "")
        except ValueError as e:
            faux.append(f"N1 (gabarit des séries refusé : {e})")
        for retire, quoi in (("          persist-credentials: false\n", "persist-credentials"),
                             ("        id: version\n        shell: bash\n", "shell: bash du pas version")):
            sabote = F.SERIES.replace(retire, "        id: version\n" if "id: version" in retire else "", 1)
            try:
                F.verifier_les_gabarits_publics({"series": sabote}, "")
                faux.append(f"N1 (gabarit sans {quoi} accepté par le filet)")
            except ValueError:
                pass
        # N2 (tour 3, M-2) : le filet par PROPRIÉTÉ ; T0 accepté, F1 à F7 refusés (harnais de la relecture du tour 2,
        # outils/filet_jeton.py, versé ici, plus F5 écrit en bloc, F6b sans redirection, F7 une redirection vers un fichier)
        # (tour 5) les pas ajoutés par F5 à F7 le sont JUSTE AVANT le clonage du public de « preparer », donc avant tout
        # code de la version : chacun n'est refusé que pour SA raison, pas pour la propriété ⑨ de l'ordre
        sec = "${{ secrets.JETON_DEPOTS }}"
        jp = "      - name: Jouer la part\n        id: jouer_la_part\n        env:\n"
        nj = "    name: jouer ${{ matrix.serie }} ${{ matrix.part }}/${{ matrix.nb_parts }}\n"
        pc = "      - uses: actions/checkout@v5\n        with:\n          path: _code\n"

        def pas_bash(script, suite=jp):
            return "      - name: Pas ajoute\n        shell: bash\n        env:\n          JETON: " + sec + "\n        run: |\n" + \
                "".join("          " + l + "\n" for l in script.split("\n")) + suite

        def tot(script):
            return F.SERIES.replace(pc, pas_bash(script, pc), 1)
        cas_du_filet = [("T0 gabarit tel quel", F.SERIES, False),
                        ("F1 env du job", F.SERIES.replace(nj, nj + "    env:\n      JETON: " + sec + "\n", 1), True),
                        ("F2 env du circuit", F.SERIES.replace("\npermissions:\n", "\nenv:\n  JETON: " + sec + "\npermissions:\n", 1), True),
                        ("F3 toJSON(secrets)", F.SERIES.replace(jp, jp + "          TOUS: ${{ toJSON(secrets) }}\n", 1), True),
                        ("F4 secrets['…']", F.SERIES.replace(jp, jp + "          JETON: ${{ secrets['JETON_DEPOTS'] }}\n", 1), True),
                        ("F5 programme de la version", tot("./tests/outils/un_script.sh"), True),
                        ("F6 écrit GITHUB_ENV", tot('echo "JETON=$JETON" >> "$GITHUB_ENV"'), True),
                        ("F6b copie vers GITHUB_ENV", tot('cp "$RUNNER_TEMP/x" "$GITHUB_ENV"'), True),
                        # F7 écrit une variable SANS nommer JETON : sinon le refus de M-a le masquait, et le sabotage
                        # SN2_redirections_non_lues ne mordait plus (premier passage du 05-11-2026, 19h25)
                        ("F7 sortie écrite dans un fichier", tot('echo "$AIDE" > "$RUNNER_TEMP/j"'), True),
                        # (tour 5) ⑨ l'ordre : le MÊME pas inoffensif, admis avant le code de la version (F15b), refusé
                        # après (F15) ; ⑩ une expression de GitHub dans le script d'un pas à jeton (F16)
                        ("F15 pas à jeton après du code de la version", F.SERIES.replace(jp, pas_bash("echo rien"), 1), True),
                        ("F15b le même pas avant le code de la version", tot("echo rien"), False),
                        ("F16 expression de GitHub dans le script", tot('echo "${{ matrix.serie }}"'), True)]
        # tour 4, M-a (relecture du tour 3, F9, F10, F13), dans le pas « Deposer » d'une part ; tour 5, F14 (relecture
        # de Cowork du 06-11-2026, D4 : une sous-chaîne du jeton, que GitHub ne masquerait pas)
        dep = [x for x in F.SERIES.split("\n      - ") if "id: deposer\n" in x]
        run_dep = ("      - " + dep[0]).split("        run: |\n", 1) if dep else ["", ""]
        ajoute = lambda l: F.SERIES.replace(run_dep[0] + "        run: |\n",
                                            run_dep[0] + "        run: |\n          " + l + "\n", 1) if dep else F.SERIES
        cas_du_filet += [("F9 mise au point de l'en-tête", ajoute("""printf 'x-access-token:%s' "$JETON" | base64 -w0"""), True),
                         ("F10 set -x en tête", ajoute("set -x"), False),
                         ("F13 echo du jeton", ajoute('echo "$JETON"'), True),
                         ("F14 sous-chaîne du jeton", ajoute('echo "${JETON:0:20}"'), True)]
        for nom_f, texte_f, refus_attendu in cas_du_filet:
            if nom_f[:2] != "T0" and texte_f == F.SERIES:
                faux.append(f"N2 ({nom_f} : variante non appliquée)")
                continue
            try:
                F.verifier_les_gabarits_publics({"series": texte_f}, "")
                refuse = False
            except ValueError:
                refuse = True
            if refuse != refus_attendu:
                faux.append(f"N2 ({nom_f} : {'refusé' if refuse else 'accepté'})")
        # N3 (tour 3, M-3, contre l'accident ; tour 5, superviseur R-759 du 06-11-2026, §4 ①) : un pas de la version a
        # posé des crochets dans .git/hooks du dépôt cloné, une configuration globale qui les sert, « core.fsmonitor »
        # et un filtre « clean » dans .git/config du dépôt cloné, et une fausse commande « git » dans le PATH ; les pas
        # à jeton du circuit FABRIQUÉ (dépôt d'une part, puis lecture des parts) tournent : aucun de ces pièges ne voit
        # le jeton (fictif), et la part est bien déposée puis lue. Des témoins prouvent d'abord que chaque piège voit
        # le jeton d'un git ordinaire.
        privn = os.path.join(d, "privn.git")
        lancer(["git", "init", "-q", "--bare", "-b", "main", privn])
        lancer(["git", "-C", graine, "push", "-q", privn, "main"])
        wsn = os.path.join(d, "wsn")
        lancer(["git", "clone", "-q", privn, wsn])
        journal = os.path.join(d, "vu_par_les_pieges.txt")
        crochets = os.path.join(wsn, ".git", "hooks")
        for h in ("pre-commit", "commit-msg", "post-commit", "pre-push", "reference-transaction", "post-checkout",
                  "post-index-change", "pre-auto-gc"):
            with open(os.path.join(crochets, h), "w") as f:
                f.write(f'#!/bin/sh\necho "crochet {h} JETON=$JETON PARAM=$GIT_CONFIG_PARAMETERS" >> "{journal}"\nexit 0\n')
            os.chmod(os.path.join(crochets, h), 0o755)
        # le filtre recopie son entrée (le contenu du fichier) ; « core.fsmonitor » ne lit rien (git ne lui donne pas
        # d'entrée : un « cat » y attendait sans fin, premier passage du 06-11-2026) et ne rend rien (git refait alors
        # sa propre recherche)
        for nom_e, fin in (("filtre", "cat"), ("fsmonitor", "exit 0")):
            with open(os.path.join(d, nom_e + ".sh"), "w") as f:
                f.write(f'#!/bin/sh\necho "{nom_e} JETON=$JETON" >> "{journal}"\n{fin}\n')
            os.chmod(os.path.join(d, nom_e + ".sh"), 0o755)
        lancer(["git", "-C", wsn, "config", "core.fsmonitor", os.path.join(d, "fsmonitor.sh")])
        lancer(["git", "-C", wsn, "config", "filter.espion.clean", os.path.join(d, "filtre.sh")])
        with open(os.path.join(wsn, ".git", "info", "attributes"), "w") as f:
            f.write("* filter=espion\n")
        # la fausse commande est en TÊTE du PATH de envn : elle s'en retire, puis lance le vrai git
        faux_bin = os.path.join(d, "faux_bin")
        os.makedirs(faux_bin)
        with open(os.path.join(faux_bin, "git"), "w") as f:
            f.write(f'#!/bin/sh\necho "fausse commande git JETON=$JETON" >> "{journal}"\nPATH=${{PATH#*:}} exec git "$@"\n')
        os.chmod(os.path.join(faux_bin, "git"), 0o755)
        globale = os.path.join(d, "globale.cfg")
        open(globale, "w").write(f"[core]\n\thooksPath = {crochets}\n")
        fictif = "FICTIF_JETON_DE_L_EPREUVE_123"
        import base64 as _b64
        fictif_b64 = _b64.b64encode(("x-access-token:" + fictif).encode()).decode()
        formes = (fictif, fictif_b64, PREFIXE_DU_BASE64, _b64.b64encode(fictif.encode()).decode())
        rt = os.path.join(d, "runner_temp")
        os.makedirs(os.path.join(rt, "travail"))
        os.makedirs(os.path.join(wsn, "rapports", "journal_du_circuit"))   # ETAPE_MUETTE l'écrit sur GitHub
        open(os.path.join(wsn, "rapports", "journal_du_circuit", "circuit_7_1_jouer.log"), "w").write("OK\n")
        open(os.path.join(rt, "travail", "lot_01.code"), "w").write("0\n")
        # N3 (tour 6, R5-1) : un « .pyc » laissé par une épreuve dans « tmp_lot_NN » et le VRAI .gitignore de la racine
        # éprouvée dans le dossier de travail ; témoin : ce .gitignore exclut bien ce chemin (git check-ignore, dans un
        # dépôt à part, sans les pièges)
        pyc = "tmp_lot_01/tmpq/programmes/__pycache__/M.cpython-311.pyc"
        os.makedirs(os.path.dirname(os.path.join(rt, "travail", pyc)))
        open(os.path.join(rt, "travail", pyc), "wb").write(b"\x00compile")
        gi = os.path.join(racine, ".gitignore")
        if os.path.isfile(gi):
            shutil.copyfile(gi, os.path.join(wsn, ".gitignore"))
        gt = os.path.join(d, "temoin_gitignore")
        lancer(["git", "init", "-q", gt])
        if os.path.isfile(gi):
            shutil.copyfile(gi, os.path.join(gt, ".gitignore"))
        if lancer(["git", "-C", gt, "check-ignore", "-q", "rapports/series_longues/7/HL/part_0/" + pyc])[0] != 0:
            faux.append("N3 (témoin : le .gitignore de la racine n'exclut pas un « .pyc » — l'essai ne prouve rien)")
        envn = dict(GIT_ENV, JETON=fictif, GITHUB_WORKSPACE=wsn, RUNNER_TEMP=rt, GITHUB_RUN_ID="7",
                    GITHUB_RUN_ATTEMPT="1", GITHUB_JOB="jouer", SERIE="HL", PART="0", GIT_CONFIG_GLOBAL=globale,
                    PATH=faux_bin + os.pathsep + os.environ.get("PATH", "/usr/bin:/bin"))
        # les témoins : un git ordinaire, lancé dans le dépôt cloné avec le jeton dans l'environnement
        open(os.path.join(wsn, "temoin.txt"), "w").write("témoin\n")
        lancer(["git", "-C", wsn, "add", "temoin.txt"], env=envn)
        lancer(["git", "-C", wsn, "commit", "-q", "-m", "témoin"], env=envn)
        temoin = open(journal).read().split("\n") if os.path.isfile(journal) else []
        for piege in ("crochet ", "fsmonitor ", "filtre ", "fausse commande git "):
            if not any(l.startswith(piege) and fictif in l for l in temoin):
                faux.append(f"N3 (témoin : le piège « {piege.strip()} » ne voit pas le jeton d'un git ordinaire — "
                            "l'essai ne prouve rien)")
        open(journal, "w").close()

        def pas_n3(ident, n, **env):
            t = [x for x in F.SERIES.split("\n      - ") if "id: " + ident + "\n" in x]
            script = pas_du_gabarit("      - " + t[n], ident) if len(t) > n else ""
            script = script.replace(F.DEPOT_PRIVE_ADRESSE, privn)
            chemin = os.path.join(d, ident + ".sh")
            open(chemin, "w").write(script)
            return lancer(["bash", "-e", "-o", "pipefail", chemin], env=dict(envn, **env), cwd=wsn)

        # N5 (tour 5) : une valeur de la matrice qui porte « : » (elle ferait écrire une autre référence que la branche
        # de la part) est refusée avant toute poussée, et main du privé ne bouge pas
        main_n5 = lancer(["git", "-C", privn, "rev-parse", "main"])[1].strip()
        k5, o5 = pas_n3("deposer", 0, PART="0:refs/heads/main")
        if k5 == 0 or "valeur refusee pour PART" not in o5 or lancer(["git", "-C", privn, "rev-parse", "main"])[1].strip() != main_n5:
            faux.append(f"N5 (valeur de la matrice « 0:refs/heads/main » : dépôt code {k5})")
        # N3 (tour 6, R5-1) : un .gitignore qui est un lien symbolique est refusé avant toute poussée
        if os.path.lexists(os.path.join(wsn, ".gitignore")):
            os.replace(os.path.join(wsn, ".gitignore"), os.path.join(d, "gitignore_mis_de_cote"))
        open(os.path.join(d, "vise_par_le_lien"), "w").write("*.code\n")
        os.symlink(os.path.join(d, "vise_par_le_lien"), os.path.join(wsn, ".gitignore"))
        kln, oln = pas_n3("deposer", 0)
        os.remove(os.path.join(wsn, ".gitignore"))
        if os.path.lexists(os.path.join(d, "gitignore_mis_de_cote")):
            os.replace(os.path.join(d, "gitignore_mis_de_cote"), os.path.join(wsn, ".gitignore"))
        if kln == 0 or "lien symbolique" not in oln:
            faux.append(f"N3 (.gitignore en lien symbolique : dépôt code {kln})")
        kd, od = pas_n3("deposer", 0)
        kl, ol = pas_n3("lire_les_parts", 0)
        arbre = lancer(["git", "-C", privn, "ls-tree", "-r", "--name-only",
                        "refs/heads/" + F.SERIES_BRANCHES + "7/HL/part_0"])[1].split()
        pyc_depose = any(x.endswith(".pyc") for x in arbre)
        code_depose = "rapports/series_longues/7/HL/part_0/lot_01.code" in arbre
        if pyc_depose or not code_depose:
            faux.append(f"N3 (exclusions du dépôt : « .pyc » déposé {pyc_depose}, lot_01.code déposé {code_depose})")
        vu = open(journal).read() if os.path.isfile(journal) else ""
        deposee = lancer(["git", "-C", privn, "rev-parse", "--verify", "-q",
                          "refs/heads/" + F.SERIES_BRANCHES + "7/HL/part_0"])[0] == 0
        lue = os.path.isdir(os.path.join(rt, "parts", "part_0"))
        fuites = [x for x in formes if x in vu]
        if kd != 0 or kl != 0 or not deposee or not lue or fuites:
            faux.append(f"N3 (dépôt {kd}, lecture {kl}, branche déposée {deposee}, part lue {lue}, formes du jeton vues "
                        f"par un piège : {len(fuites)})")
        # N4 (tour 5, superviseur R-759 du 06-11-2026, §2 ; relecture de Cowork, D2 et D3) : CHAQUE pas à jeton du
        # gabarit FABRIQUÉ, dans l'ordre du gabarit, « set -x » en tête et toutes les traces de git allumées (TRACES),
        # contre un serveur local qui EXIGE une identification : code 0, au moins une identification reçue PENDANT le
        # pas (le jeton a bien servi), et AUCUNE forme du jeton fictif dans la sortie entière. Deux témoins d'abord :
        # le serveur refuse qui ne s'identifie pas, et l'ancienne forme (en-tête calculé) écrit le base64 sous ces
        # traces — la recherche est calibrée sur un cas qui doit être trouvé.
        servi = os.path.join(d, "servi")
        os.makedirs(servi)
        privh = os.path.join(servi, "privh.git")
        lancer(["git", "init", "-q", "--bare", "-b", "main", privh])
        lancer(["git", "-C", privh, "config", "http.receivepack", "true"])
        lancer(["git", "-C", graine, "push", "-q", privh, "main"])
        wsh = os.path.join(d, "wsh")
        lancer(["git", "clone", "-q", privh, wsh])
        rth = os.path.join(d, "runner_temp_h")
        os.makedirs(os.path.join(rth, "travail"))
        open(os.path.join(rth, "travail", "lot_01.code"), "w").write("0\n")
        os.makedirs(os.path.join(wsh, "rapports", "journal_du_circuit"))
        open(os.path.join(wsh, "rapports", "journal_du_circuit", "circuit_8_1_jouer.log"), "w").write("OK\n")
        recus = []
        try:
            serveur = servir(servi, fictif_b64, recus)
        except OSError as e:
            serveur = None
            faux.append(f"N4 (serveur local impossible : {e} — rien de prouvé)")
        if serveur is not None:
            try:
                url = f"http://127.0.0.1:{serveur.server_address[1]}/privh.git"
                # GIT_CEILING_DIRECTORIES et cwd=d : les témoins ne lisent la configuration d'AUCUN dépôt englobant
                # (premier passage du 06-11-2026 : lancé depuis un clone dont .git/config porte un en-tête
                # d'identification, git l'envoyait aussi au serveur d'essai, qui refusait)
                envh = dict(GIT_ENV, JETON=fictif, GITHUB_WORKSPACE=wsh, RUNNER_TEMP=rth, GITHUB_RUN_ID="8",
                            GITHUB_RUN_ATTEMPT="1", GITHUB_JOB="jouer", SERIE="HL", PART="1", VERSION="main",
                            BRANCHE_PUBLIQUE="main", GIT_CEILING_DIRECTORIES=os.path.dirname(d), **TRACES)
                k_sans = lancer(["git", "ls-remote", url], env=envh, cwd=d)[0]
                k_ancien, o_ancien = lancer(["git", "-c", "http.extraheader=AUTHORIZATION: basic " + fictif_b64,
                                             "ls-remote", url], env=envh, cwd=d)
                if k_sans == 0 or k_ancien != 0 or fictif_b64 not in o_ancien:
                    faux.append(f"N4 (témoins : sans identification code {k_sans}, attendu non nul ; en-tête calculé "
                                f"code {k_ancien}, base64 écrit par les traces {fictif_b64 in o_ancien} — l'essai ne "
                                "prouve rien)")
                a_jeton = [x for x in F.SERIES.split("\n      - ") if F.JETON_DU_PAS.rstrip("\n") in x.split("\n")]
                if not a_jeton:
                    faux.append("N4 (aucun pas à jeton lu dans le gabarit)")
                for x in a_jeton:
                    ident = next((l.split("id:", 1)[1].strip() for l in x.split("\n") if l.startswith("        id:")), "")
                    script = pas_du_gabarit("      - " + x, ident).replace(F.DEPOT_PRIVE_ADRESSE, url)
                    chemin = os.path.join(d, "n4_" + ident + ".sh")
                    open(chemin, "w").write("set -x\n" + script)
                    avant_le_pas = recus.count("identifié")
                    p4 = subprocess.run(["bash", "-e", "-o", "pipefail", chemin], env=envh, cwd=wsh,
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=300)
                    vues = [f for f in formes if f in p4.stdout]
                    if p4.returncode != 0 or recus.count("identifié") == avant_le_pas or vues:
                        faux.append(f"N4 (pas « {ident} » sous set -x et traces de git : code {p4.returncode}, "
                                    f"identifications reçues {recus.count('identifié') - avant_le_pas}, formes du jeton "
                                    f"écrites {len(vues)})")
            finally:
                serveur.shutdown()
                serveur.server_close()
        if F.PARTS_EN_MEME_TEMPS > 16:
            faux.append(f"N1 (max-parallel {F.PARTS_EN_MEME_TEMPS} > 16)")
        lances = [l.strip() for l in F.SERIES.split("\n") if '.py "$RUNNER_TEMP/depot"' in l]
        if len(lances) != 2 or not all(l.startswith("unshare -rn python3 ") for l in lances):
            faux.append(f"N1 (parts et rassemblement pas tous sous unshare -rn : {lances})")
        # ---- P : les parts
        def parts(r, n, avant=None):
            codes = []
            for i in range(n):
                codes.append(lancer([sys.executable, "-B", os.path.join(r, OUTILS[1]), r, "tests/EPR.py", REL,
                                     f"--part={i}", f"--nb-parts={n}", "--lot=2", "--parallele=1",
                                     f"--travail={r}_parts/p{i}"])[0])
            if avant:
                avant(r + "_parts")
            c, o = lancer([sys.executable, "-B", os.path.join(r, OUTILS[2]), r, "tests/EPR.py", REL,
                           f"--depuis={r}_parts", f"--travail={r}_rassemble"])
            p = os.path.join(r, REL)
            return codes, c, o, (open(p, encoding="utf-8").read() if os.path.isfile(p) else "")

        def net(t):
            lignes = t.split("\n")
            return [l for i, l in enumerate(lignes) if i != 2 and not l.startswith("# joué par : ")]

        r = depot_d_essai(racine, d, "P1_seul")
        vu_tmp = os.path.join(d, "temporaires_vus.txt")
        vu_env = os.path.join(d, "environnements_vus.txt")
        de_github = {v: os.path.join(d, "commandes_de_github_" + v) for v in F.FICHIERS_DE_COMMANDES_DE_GITHUB}
        for f_ in de_github.values():
            open(f_, "w").close()
        c, _ = lancer([sys.executable, "-B", os.path.join(r, OUTILS[0]), r, "tests/EPR.py", REL, "--parts=1", "--lot=2",
                       f"--travail={r}_travail"], env=dict(GIT_ENV, ESSAI_TEMP_VU=vu_tmp, ESSAI_ENV_VU=vu_env,
                                                           ESSAI_TEMOIN_ENV="1", **de_github))
        # P8 (tour 6, R5-4) : l'épreuve jouée ne reçoit aucun fichier de commandes de GitHub ; témoin : elle reçoit
        # une variable ordinaire posée au même endroit (sinon l'essai ne prouve rien)
        vus_env = open(vu_env).read().split() if os.path.isfile(vu_env) else []
        recus = sorted(set(vus_env) & set(de_github))
        if "ESSAI_TEMOIN_ENV" not in vus_env or recus:
            faux.append(f"P8 (fichiers de commandes de GitHub reçus par l'épreuve jouée : {recus} ; témoin reçu "
                        f"{'ESSAI_TEMOIN_ENV' in vus_env})")
        # P7 (tour 3, M-1) : chaque lot a vu son temporaire DANS le dossier de travail
        vus_tmp = open(vu_tmp).read().split() if os.path.isfile(vu_tmp) else []
        if not vus_tmp or not all(v.startswith(os.path.realpath(r + "_travail") + os.sep + "tmp_lot_") for v in vus_tmp):
            faux.append(f"P7 (temporaire des lots hors du dossier de travail : {vus_tmp[:2]})")
        # P5 (tour 3, B-2) : un lot compté sans sa place (« .code » sans « .place ») rend la reprise NON CONFORME
        places_p5 = sorted(f for f in (os.listdir(r + "_travail") if os.path.isdir(r + "_travail") else [])
                           if f.endswith(".place"))
        if places_p5:
            os.remove(os.path.join(r + "_travail", places_p5[0]))
        c5, o5 = lancer([sys.executable, "-B", os.path.join(r, OUTILS[0]), r, "tests/EPR.py", REL, "--parts=1", "--lot=2",
                         f"--travail={r}_travail"])
        if not places_p5 or c5 != 1 or "place libre minimale None" not in o5:
            faux.append(f"P5 (lot compté sans place : reprise code {c5})")
        # P6 (tour 3, M-1) : le temporaire sur un autre système de fichiers que le dossier de travail → ARRET, code 2
        if not os.path.isdir("/dev/shm") or os.stat("/dev/shm").st_dev == os.stat(d).st_dev:
            faux.append("P6 (aucun autre système de fichiers inscriptible pour l'essai : /dev/shm absent ou même disque)")
        else:
            r6 = depot_d_essai(racine, d, "P6")
            c6, o6 = lancer([sys.executable, "-B", os.path.join(r6, OUTILS[0]), r6, "tests/EPR.py", REL, "--parts=1",
                             "--lot=2", f"--travail={r6}_travail"], env=dict(GIT_ENV, TMPDIR="/dev/shm"))
            if c6 != 2 or "dossier temporaire" not in o6:
                faux.append(f"P6 (temporaire sur un autre disque : code {c6})")
        r = depot_d_essai(racine, d, "P1_seul_bis")
        c, _ = lancer([sys.executable, "-B", os.path.join(r, OUTILS[0]), r, "tests/EPR.py", REL, "--parts=1", "--lot=2",
                       f"--travail={r}_travail"])
        seul = open(os.path.join(r, REL), encoding="utf-8").read() if os.path.isfile(os.path.join(r, REL)) else ""
        cp, c2_, o, deux = parts(depot_d_essai(racine, d, "P1_deux"), 2)
        if c != 0 or cp != [0, 0] or c2_ != 0 or not seul or net(seul) != net(deux):
            faux.append(f"P1 (joueur seul {c}, parts {cp}, rassemblement {c2_}, relevés égaux {net(seul) == net(deux)})")

        def vider(dossier):
            e = os.path.join(dossier, "p1", "execution")
            for f in os.listdir(e):
                open(os.path.join(e, f), "w").close()

        cp, c, o, rel = parts(depot_d_essai(racine, d, "P2"), 2, vider)
        if c != 2 or rel:
            faux.append(f"P2 (flux execution vidé : rassemblement {c})")

        def sans_place(dossier):
            p0 = os.path.join(dossier, "p0")
            places = sorted(f for f in (os.listdir(p0) if os.path.isdir(p0) else []) if f.endswith(".place"))
            if places:
                os.remove(os.path.join(dossier, "p0", places[0]))

        cp, c, o, rel = parts(depot_d_essai(racine, d, "P3"), 2, sans_place)
        if c != 2 or rel:
            faux.append(f"P3 (part sans place libre minimale : rassemblement {c})")
        # ---- C : le comparateur des relevés (B1) ; R : le rangeur (N2)
        a = os.path.join(d, "a.txt")
        open(a, "w", encoding="utf-8", newline="").write(deux)
        for nom_c, texte_c, attendu in (("C1 fins de ligne \\r\\n", deux.replace("\n", "\r\n"), 1),
                                        ("C2 seules les lignes « joué par » diffèrent",
                                         "\n".join(l if not l.startswith("# joué par : ") else "# joué par : ailleurs"
                                                   for l in deux.split("\n")), 0)):
            b = os.path.join(d, "b.txt")
            open(b, "w", encoding="utf-8", newline="").write(texte_c)
            k = lancer([sys.executable, "-B", os.path.join(racine, COMPARATEUR), a, b])[0]
            if k != attendu:
                faux.append(f"{nom_c} (code {k}, attendu {attendu})")
        # C3 à C5 (tour 3, m-3) : une ligne « joué par » de chaque côté ; avec --calibrage, machine à gauche, GitHub à droite
        # Réparation du 08-11-2026 (relevé n°327, Q6 = 1 du relevé n°347) : sur GitHub, le relevé de P1 dit déjà
        # « GitHub » (GITHUB_ACTIONS vaut « true ») ; C5 comparait alors deux relevés « GitHub » et rougissait. Les deux
        # côtés sont donc fabriqués ICI, quelle que soit la machine : « machine locale » à gauche, « GitHub » à droite.
        b = os.path.join(d, "b.txt")
        local = "\n".join(l.replace("# joué par : GitHub ; ", "# joué par : machine locale ; ") for l in deux.split("\n"))
        if local.count("# joué par : machine locale ; ") != 1:
            faux.append("C3 à C5 (le relevé de P1 ne porte pas exactement une ligne « joué par » lisible)")
        open(a, "w", encoding="utf-8", newline="").write(local)
        sans_ligne = "\n".join(l for l in local.split("\n") if not l.startswith("# joué par : "))
        en_github = "\n".join(l.replace("# joué par : machine locale ; ", "# joué par : GitHub ; ") for l in local.split("\n"))
        for nom_c, texte_c, options, attendu in (("C3 sans ligne « joué par » à droite", sans_ligne, [], 1),
                                                 ("C4 calibrage entre deux relevés locaux", local, ["--calibrage"], 1),
                                                 ("C5 calibrage machine contre GitHub", en_github, ["--calibrage"], 0)):
            open(b, "w", encoding="utf-8", newline="").write(texte_c)
            k = lancer([sys.executable, "-B", os.path.join(racine, COMPARATEUR), a, b] + options)[0]
            if k != attendu or (attendu == 0 and texte_c == local):
                faux.append(f"{nom_c} (code {k}, attendu {attendu})")
        cl = os.path.join(d, "clone_version")
        lancer(["git", "clone", "-q", "-b", "travail-essai", prive, cl])
        os.makedirs(os.path.join(cl, "tests", "outils"))
        shutil.copyfile(os.path.join(racine, OUTILS[0]), os.path.join(cl, OUTILS[0]))
        os.symlink(os.path.join(racine, "programmes"), os.path.join(cl, "programmes"))
        pointe = lancer(["git", "-C", cl, "rev-parse", "HEAD"])[1].strip()
        rel_r = os.path.join(d, os.path.basename(REL))
        for nom_r, commit, attendu in (("R1 relevé d'un autre commit", "f" * 40, 1), ("R2 relevé de la pointe", pointe, 0)):
            open(rel_r, "w", encoding="utf-8").write(f"# RELEVÉ\n# joué par : GitHub ; Python 3.11.0 ; commit {commit} ; "
                                                     "passage 1.1 ; place libre minimale 9000 Mo (plancher 1024 Mo)\n")
            k = lancer([sys.executable, "-B", os.path.join(racine, RANGEUR), cl, rel_r])[0]
            range_ = os.path.isfile(os.path.join(cl, REL))
            if k != attendu or range_ != (attendu == 0):
                faux.append(f"{nom_r} (code {k}, rangé {range_})")
        # R2bis, R3, R4 (tour 3, M-4) : la ligne écrite par `ligne_joue_par` du joueur de la racine, puis le rangeur
        J = charger(os.path.join(racine, OUTILS[0]), "JOUEUR_EPROUVE")
        propre = os.path.join(d, "clone_propre")
        lancer(["git", "clone", "-q", "-b", "travail-essai", prive, propre])
        modifie = os.path.join(d, "clone_modifie")
        lancer(["git", "clone", "-q", "-b", "travail-essai", prive, modifie])
        open(os.path.join(modifie, "a.txt"), "a").write("changement non commité\n")
        sans_git = os.path.join(d, "copie_sans_git")
        os.makedirs(sans_git)
        sauve = {k: os.environ.get(k) for k in ("GITHUB_ACTIONS", "SERIE_COMMIT")}
        try:
            os.environ.pop("GITHUB_ACTIONS", None)
            os.environ.pop("SERIE_COMMIT", None)
            l_propre, l_modifie = J.ligne_joue_par(propre, 9000), J.ligne_joue_par(modifie, 9000)
            os.environ["SERIE_COMMIT"] = pointe
            l_declare = J.ligne_joue_par(sans_git, 9000)
        finally:
            for k_, v_ in sauve.items():
                if v_ is None:
                    os.environ.pop(k_, None)
                else:
                    os.environ[k_] = v_
        for nom_r, ligne_r, attendu in (("R2bis ligne du joueur sur la pointe propre", l_propre, 0),
                                        ("R3 ligne du joueur sur un arbre modifié", l_modifie, 1),
                                        ("R4 SERIE_COMMIT posé à la main hors de GitHub", l_declare, 1)):
            if os.path.isfile(os.path.join(cl, REL)):
                os.remove(os.path.join(cl, REL))
            open(rel_r, "w", encoding="utf-8").write("# RELEVÉ\n# " + ligne_r + "\n")
            k = lancer([sys.executable, "-B", os.path.join(racine, RANGEUR), cl, rel_r])[0]
            if k != attendu:
                faux.append(f"{nom_r} (code {k}, attendu {attendu} ; {ligne_r[:90]})")
        r4 = depot_d_essai(racine, d, "P4")
        with open(os.path.join(r4, RETENU), "w", encoding="utf-8") as f:
            f.write("# RELEVÉ\nA1 mord : ['H1']\nA2 mord : ['H2']\nA3 mord : ['H1']\nVERDICT : tout est conforme\n")
        cp, c, o, rel = parts(r4, 2)
        if c != 1 or "# raisons à examiner" not in rel or "raison changée A2" not in rel:
            faux.append(f"P4 (raison changée par les parts : rassemblement {c})")
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return faux


def main():
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Fiche en tête.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — Fiche en tête.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1]
    ⑥ TRAITEMENT — un tour tel quel ; avec --saboter, une copie de la racine par sabotage (fabricant, outils,
      programmes/ et, depuis le tour 6, le .gitignore copiés — N3 le lit ; le fichier visé écrit saboté), un tour par
      copie.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Fiche en tête.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Fiche en tête.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    faux = tour(DEPOT)
    print("Z0 programmes tels quels : " + ("G0 à G4, M1 à M3, X3, MB1 à MB4, X2, N1 à N5, P1 à P8, C1 à C5, R1 à R4 conformes" if not faux else
                                            "FAUX " + ", ".join(faux)))
    code = 1 if faux else 0
    if "--saboter" in sys.argv:
        for nom, remplacements in SABOTAGES.items():
            d = tempfile.mkdtemp(prefix="circuit_series_sab_")
            try:
                for f in [FABRICANT, COMPARATEUR, RANGEUR, ".gitignore"] + list(OUTILS):
                    os.makedirs(os.path.dirname(os.path.join(d, f)), exist_ok=True)
                    shutil.copyfile(os.path.join(DEPOT, f), os.path.join(d, f))
                for f in os.listdir(os.path.join(DEPOT, "programmes")):
                    if f.endswith(".py") and not os.path.exists(os.path.join(d, "programmes", f)):
                        shutil.copyfile(os.path.join(DEPOT, "programmes", f), os.path.join(d, "programmes", f))
                shutil.copytree(os.path.join(DEPOT, ".github", "workflows"), os.path.join(d, ".github", "workflows"))
                shutil.copyfile(os.path.join(DEPOT, "tests", "LANCEMENT_DES_EPREUVES.json"),
                                os.path.join(d, "tests", "LANCEMENT_DES_EPREUVES.json"))
                for fichier, a, b in remplacements:
                    t = open(os.path.join(d, fichier), encoding="utf-8").read()
                    if t.count(a) != 1:
                        print(f"{nom} NE S'APPLIQUE PLUS : texte cible trouvé {t.count(a)} fois dans {fichier}")
                        return 2
                    open(os.path.join(d, fichier), "w", encoding="utf-8").write(t.replace(a, b))
                f = tour(d)
            finally:
                shutil.rmtree(d, ignore_errors=True)
            print(f"{nom} {'mord' if f else 'NE MORD PAS'} : {f}")
            code |= 0 if f else 1
    print("VERDICT : tout est conforme" if code == 0 else "VERDICT : NON CONFORME")
    return code


if __name__ == "__main__":
    sys.exit(main())
