#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPROUVER_LA_PLACE_SUR_UN_VRAI_DISQUE — Jeu 05-11-2026 (Paris). Simulation uniquement.

① RÔLE — Éprouver le témoin de la place du joueur de séries sur le CHEMIN RÉEL, avec un VRAI disque plein (ENOSPC rendu
  par le noyau) : (R) une série COUPÉE par SIGKILL après un lot joué disque plein, puis REPRISE ; (A) le temporaire des
  épreuves sur un AUTRE disque que le dossier de travail. Harnais de la relecture du tour 2 (outils/m1_reprise.py et
  outils/m1_disque.py, scénario A), versé au dépôt au tour 3 (superviseur R-759 du 05-11-2026, 17h13, §C 2 et 3).
② CONTEXTE D'APPEL — À la main, avant toute livraison qui touche `surveiller_la_place`, `jouer_un_lot`, `lire_la_place`
  ou `refus_du_disque_temporaire` du joueur, en super-utilisateur, réseau et montages isolés :
  unshare -nm --propagation private python3 -B tests/outils/EPROUVER_LA_PLACE_SUR_UN_VRAI_DISQUE.py <racine> <jetable>
  Pas par la certification de nuit : il monte des disques en mémoire (tmpfs), ce qui demande ces droits.
③ ENTRÉE — `racine` : un dépôt qui porte programmes/ et tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py ; `jetable` : un
  dossier qui n'existe pas encore.
④ CONDITIONS D'ENTRÉE — Super-utilisateur dans un espace de montage privé ; environ 1,1 Go de mémoire par disque monté.
⑤ SORTIE — Le code de sortie : 0 si les deux scénarios rendent un code de joueur NON NUL (aucun faux conforme) ; 1 si
  un scénario sort CONFORME (« CASSÉ ») ; 2 si un disque n'a pas pu être monté (rien n'est prouvé, R-734).
  [rend: 1]
⑥ TRAITEMENT — L'épreuve d'essai EPR a trois sabotages ; le sabotage A2 a PERDU SES DENTS (ESSAI_SANS_DENTS=A2) ;
  l'enfant remplit le disque de son temporaire jusqu'à ENOSPC, attend 2 s, efface, et sa sortie d'erreur est jetée.
  Le relevé retenu dit « A2 mord : ['H1'] », que le disque plein refait à l'identique : seul le témoin de la place
  peut le voir. ① Un relevé retenu CONFORME (1re série, puis --raisons-acceptees), sur un tmpfs de 1100 Mo. ② R : une
  série lancée, tuée par SIGKILL dès que lot_02.code existe, puis reprise sur le même dossier de travail. ③ A : dossier
  de travail sur son propre tmpfs de 1100 Mo, TMPDIR sur un tmpfs de 8 Mo.
⑦ UNITÉ — Mo (tailles des disques).
⑧ POURQUOI — Superviseur R-759 du tour 3, §B : « chaque réparation ajoute une pièce, éprouvée seule dans un décor fait
  pour elle » ; la relecture du tour 2 a cassé le témoin de la place en jouant le chemin normal du garde-disque (coupure,
  reprise) et un temporaire ailleurs. Le dossier de travail est TOUJOURS sur un disque monté pour l'essai : une
  régression qui écrirait le temporaire dans le dossier de travail ne peut pas remplir le disque de la machine.
⑨ CE QUI CLOCHE — Une épreuve d'essai, pas les vraies séries HL et Yahoo. Le pas du fil (0,5 s) contre un remplissage
  en mémoire : le disque plein est gardé 2 s pour être vu sûrement. /dev/shm et les inodes ne sont pas éprouvés
  (BACKLOG).
⑩ EFFET — Monte et démonte des tmpfs dans `jetable` ; écrit dans `jetable`.
⑪ TERMINAISON — Rend la main ; chaque série est bornée à 600 s ; l'attente du lot 2 est bornée à 300 s. Un de mes
  appels peut ne pas revenir : non, tous sont bornés. [sort: oui]
"""
import os
import shutil
import signal
import subprocess
import sys
import time

EPR = r'''import os, sys, subprocess, tempfile, time, importlib.util
SABOTAGES = {"A1": 4, "A2": 2, "A3": 3}
if len(sys.argv) > 3 and sys.argv[1] == "--cas":
    c, n = sys.argv[2], sys.argv[3]
    if os.environ.get("ESSAI_REMPLIR") == n:
        p = os.path.join(tempfile.gettempdir(), "remplir_%d" % os.getpid())
        try:
            with open(p, "wb") as f:
                while True:
                    f.write(b"\0" * (1 << 20))
        finally:
            time.sleep(float(os.environ.get("ESSAI_GARDER_S", "0")))
            os.remove(p)
    sp = importlib.util.spec_from_file_location("M", os.path.join(c, "M.py"))
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    sys.exit(0 if m.VAL == 1 else 1)
racine = os.path.abspath(sys.argv[1])
choix = [a.split("=", 1)[1] for a in sys.argv[2:] if a.startswith("--saboter=")]
w = racine + "_w%d" % os.getpid(); os.makedirs(w)
def cas(n, val):
    open(os.path.join(w, "M.py"), "w").write("VAL = %d\n" % val)
    p = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--cas", w, n], capture_output=True, text=True)
    return p.returncode   # la sortie d'erreur de l'enfant est capturée et JETÉE
print("Z0 programme tel quel : tous les cas conformes" if cas("Z0", 1) == 0 else "Z0 ROUGE")
for n in (choix[0].split(",") if choix else []):
    val = 1 if os.environ.get("ESSAI_SANS_DENTS") == n else SABOTAGES[n]
    print(f"{n} mord : ['H1']" if cas(n, val) != 0 else f"{n} NE MORD PAS : []")
'''
TABLE = ('{"epreuves": {}, "series_hors_de_la_nuit": {"tests/EPR.py": {"releve": "tests/resultats/SERIE_*.txt", '
         '"essais_refaits_chaque_nuit": 0, "portee_du_releve": "code_execute"}}}\n')
REL1 = "tests/resultats/SERIE_DE_SABOTAGES_DE_L_ESSAI_Mer_04-11-2026_10h00.txt"
REL2 = "tests/resultats/SERIE_DE_SABOTAGES_DE_L_ESSAI_Jeu_05-11-2026_10h00.txt"
JOUEUR = "tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py"


def depot(clone, r):
    """Fabrique le dépôt d'essai ; rend son chemin.

    ① RÔLE — Un dépôt minuscule : programmes/ et le joueur de la racine éprouvée, l'épreuve EPR, la table.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `clone` : la racine éprouvée ; `r` : le dossier à créer.
    ④ CONDITIONS D'ENTRÉE — `r` n'existe pas.
    ⑤ SORTIE — UNE valeur : `r`. [rend: 1]
    ⑥ TRAITEMENT — copies.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le joueur éprouvé est celui de la racine, tel quel (le chemin réel).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit `r`.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    shutil.copytree(os.path.join(clone, "programmes"), os.path.join(r, "programmes"),
                    ignore=shutil.ignore_patterns("__pycache__"))
    os.makedirs(os.path.join(r, "tests", "outils"))
    shutil.copy(os.path.join(clone, JOUEUR), os.path.join(r, JOUEUR))
    open(os.path.join(r, "tests", "EPR.py"), "w").write(EPR)
    open(os.path.join(r, "tests", "LANCEMENT_DES_EPREUVES.json"), "w").write(TABLE)
    return r


def jouer(r, rel, travail, env=None, extra=()):
    """Lance le joueur de la racine d'essai ; rend (code, dernière ligne FINI ou ARRET).

    ① RÔLE — Une série, bornée. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `r`, `rel`, `travail`, `env` ajouté, `extra`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : (code, texte). [rend: 1] ⑥ TRAITEMENT — subprocess.run.
    ⑦ UNITÉ — Secondes (borne de 600). ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — Un dépassement lève TimeoutExpired.
    ⑩ EFFET — Ce que fait le joueur. ⑪ TERMINAISON — 600 s au plus. [sort: non]
    """
    p = subprocess.run([sys.executable, "-B", os.path.join(r, JOUEUR), r, "tests/EPR.py", rel, "--parts=1", "--lot=1",
                        "--travail=" + travail] + list(extra), capture_output=True, text=True, timeout=600,
                       env=dict(os.environ, **(env or {})))
    fini = [l for l in p.stdout.splitlines() if l.startswith(("FINI", "ARRET"))]
    return p.returncode, (fini[-1] if fini else p.stdout[-300:])


def monter(d, taille):
    """Monte un tmpfs ; rend True s'il est monté.

    ① RÔLE — Un vrai disque qui se remplit. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `d`, `taille` (« 1100m »).
    ④ CONDITIONS D'ENTRÉE — Super-utilisateur, espace de montage privé. ⑤ SORTIE — UNE valeur : booléen. [rend: 1]
    ⑥ TRAITEMENT — mount -t tmpfs. ⑦ UNITÉ — Mo. ⑧ POURQUOI — Fiche en tête, ⑥. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Un montage. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    os.makedirs(d, exist_ok=True)
    return subprocess.run(["mount", "-t", "tmpfs", "-o", "size=" + taille, "tmpfs", d]).returncode == 0


def main():
    """Le programme entier (fiche en tête).

    ① RÔLE — Fiche en tête. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — Fiche en tête.
    ④ CONDITIONS D'ENTRÉE — Fiche en tête. ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1] ⑥ TRAITEMENT — Fiche en tête.
    ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête. ⑨ CE QUI CLOCHE — Fiche en tête. ⑩ EFFET — Fiche en tête.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    clone, jet = os.path.realpath(sys.argv[1]), os.path.realpath(sys.argv[2])
    os.makedirs(jet)
    grand, seul, petit = os.path.join(jet, "grand"), os.path.join(jet, "seul"), os.path.join(jet, "petit")
    montes = []
    try:
        for d_, t_ in ((grand, "1100m"), (seul, "1100m"), (petit, "8m")):
            if not monter(d_, t_):
                print(f"IMPOSSIBLE : tmpfs {d_} non monté (super-utilisateur, unshare -m ?) — rien n'est prouvé")
                return 2
            montes.append(d_)
        os.makedirs(os.path.join(grand, "tmp"))
        base = depot(clone, os.path.join(grand, "base"))
        env_grand = {"TMPDIR": os.path.join(grand, "tmp")}
        jouer(base, REL1, os.path.join(grand, "w_base"), env_grand)
        c, l = jouer(base, REL1, os.path.join(grand, "w_base"), env_grand, ["--raisons-acceptees=A1,A2,A3"])
        print(f"-- relevé retenu : code {c} · {l[:150]}")
        if c != 0:
            print("IMPOSSIBLE : le relevé retenu n'est pas conforme — rien n'est prouvé")
            return 2
        res = []
        # la copie du scénario A est prise AVANT R : la série de R range le relevé retenu dans archives/ (premier essai
        # du 05-11-2026 : copié après, A n'avait plus de relevé retenu et sortait NON CONFORME pour cette seule raison)
        r_a = os.path.join(seul, "d_A")
        shutil.copytree(base, r_a)
        # R : coupé par SIGKILL après le lot 2 joué disque plein, puis repris
        env = dict(os.environ, ESSAI_SANS_DENTS="A2", ESSAI_REMPLIR="A2", ESSAI_GARDER_S="2", **env_grand)
        w = os.path.join(grand, "w_coupee")
        p = subprocess.Popen([sys.executable, "-B", os.path.join(base, JOUEUR), base, "tests/EPR.py", REL2, "--parts=1",
                              "--lot=1", "--travail=" + w], env=env, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, start_new_session=True)
        debut = time.time()
        while not os.path.exists(os.path.join(w, "lot_02.code")) and time.time() - debut < 300 and p.poll() is None:
            time.sleep(0.05)
        os.killpg(p.pid, signal.SIGKILL)
        p.wait()
        lots = sorted(f for f in os.listdir(w) if f.startswith("lot_") and f.endswith((".code", ".place")))
        c, l = jouer(base, REL2, w, {"ESSAI_SANS_DENTS": "A2", **env_grand})
        res.append(c != 0)
        print(f"== R coupée (SIGKILL) après le lot 2 disque plein, puis reprise : lots écrits avant la coupure {lots} ; "
              f"code {c} -> {'TENU' if c != 0 else 'CASSÉ (faux conforme)'} · {l[:200]}")
        # A : le temporaire sur un autre disque (8 Mo) que le dossier de travail (son propre tmpfs)
        c, l = jouer(r_a, REL2, os.path.join(seul, "w_A"), {"ESSAI_SANS_DENTS": "A2", "ESSAI_REMPLIR": "A2",
                                                            "ESSAI_GARDER_S": "2", "TMPDIR": petit})
        res.append(c != 0)
        print(f"== A temporaire sur un autre disque plein : code {c} -> {'TENU' if c != 0 else 'CASSÉ (faux conforme)'} · "
              f"{l[:400]}")
        print("FIN", sum(res), "/", len(res), "scénarios sans faux conforme")
        return 0 if all(res) else 1
    finally:
        for d_ in reversed(montes):
            subprocess.run(["umount", d_])


if __name__ == "__main__":
    sys.exit(main())
