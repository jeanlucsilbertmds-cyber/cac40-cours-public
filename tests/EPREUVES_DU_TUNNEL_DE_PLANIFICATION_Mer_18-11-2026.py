#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Éprouve le tunnel de planification : contrôle installé (forfait estimé, carte des pannes) et ordonnanceur.

① RÔLE — Prouver, sur des plannings fabriqués, ce que l'étape PANNES (A-897 à
  A-900) a programmé, puis saboter chaque garde-fou et exiger qu'une épreuve
  rougisse (R-731 : une épreuve qui reste verte quand on retire ce qu'elle teste
  est une décoration).
② CONTEXTE D APPEL — `python3 tests/EPREUVES_DU_TUNNEL_DE_PLANIFICATION_Mer_18-11-2026.py
  [<racine>] [--sans-sabotage]` depuis la racine d'un clone, ou d'une copie sans
  .git (épreuve longue « Tunnel » sur GitHub, qui passe la copie en <racine>).
  <racine>, si donnée, doit être la racine de l'arbre qui porte ce fichier
  (même dossier) ; tout autre argument → ARRET, code 2 (m13 de la relecture
  f2ce23138 : un argument accepté puis ignoré est un silence). Les sabotages
  se jouent par défaut ; --sans-sabotage pour les seules épreuves.
③ ENTRÉE — Les programmes de programmes/ : CONTROLER_UN_PLANNING.py,
  TENIR_UN_PLANNING.py, ORDONNER_UN_PLANNING.py, REGLAGES_DU_PLANNING.csv.
④ CONDITIONS D ENTRÉE — git installé ; l'interpréteur de la version certifiée
  (VERSION_DE_PYTHON de programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, la seule
  écriture, A-874) : si le Python courant n'est pas cette version, le fichier
  se RELANCE sous python<VERSION> (B6 de la relecture f2ce23138 : une ligne
  admise en 3.12 seulement passait sous la 3.13 des machines du Chat et du
  relecteur) ; introuvable → ARRET, code 2, aucune épreuve jouée (R-734).
  Aucun réseau : le dépôt d'origine est un dépôt nu local, la branche d'état y est lue. Les épreuves a1 à a4 lisent les
  quatre sources d'AVANT_DE_DEMANDER DANS L'ARBRE ÉPROUVÉ (RACINE, la racine
  de l'arbre qui porte ce fichier, la même que celle passée à k13) : aucune
  épreuve n'exige un .git à cette racine (B7 et B8 de la relecture f2ce23138 :
  sur la copie sans .git de GitHub, k13 et a1 à a4 rougissaient quoi qu'il
  arrive ; la lecture par `git show origin/main`, du temps où l'erratum A-907
  n'existait que sur main, est retirée — main est fusionnée dans la branche).
⑤ SORTIE — Une ligne « PYTHON <version> <interpréteur> », lignes OK / ÉCHEC par
  épreuve, MORD / NE MORD PAS par sabotage, puis un verdict. Code 0 si tout est
  vert et que tout sabotage mord, 1 sinon — et si le passage sur le VRAI est
  rouge, AUCUN sabotage n'est joué (« SABOTAGES NON JOUÉS », m12 : un « MORD »
  sur un vrai rouge ne prouve rien) —, 2 si un sabotage ne s'applique plus (son
  texte a disparu du code), si un argument est refusé ou si la version
  certifiée de Python est introuvable.
  [rend: 1]
⑥ TRAITEMENT — Pour chaque jeu de programmes (le vrai, puis chaque sabotage
  appliqué à une copie) : fabriquer dans un dossier jetable un dépôt nu, un clone,
  un planning et la carte des pannes ; appeler le contrôle (importé) et
  l'ordonnanceur (sous-processus) ; vérifier les lignes et les codes.
⑦ UNITÉ — heures de Paris.
⑧ POURQUOI — R-731 ; superviseur R-759 du 18-11-2026.
⑨ CE QUI CLOCHE — Plannings fabriqués : le cas réel (planning du 17-11, branche
  travail-planning-17) est passé à part, sa sortie est capturée dans la note.
  Les dépôts des épreuves vivent dans un dossier jetable, jamais ceux du Chat.
  Les questions négatives jamais vues d'AVANT_DE_DEMANDER sont MESURÉES dans la
  note de livraison, pas éprouvées ici (superviseur R-759, 18-11-2026 16h17 :
  aucun réglage sur de nouveaux cas).
⑩ EFFET — Écrit seulement dans des dossiers temporaires, effacés à la fin.
⑪ TERMINAISON — Chaque sous-processus est borné à 120 s. La relance sous la
  version certifiée remplace le processus (os.execv) une fois au plus : une
  variable d'environnement la marque, une seconde mauvaise version → ARRET.
  [sort: oui]
"""
import datetime
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
from zoneinfo import ZoneInfo

P = ZoneInfo("Europe/Paris")
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROG = os.path.join(RACINE, "programmes")
FICHIERS = ("CONTROLER_UN_PLANNING.py", "TENIR_UN_PLANNING.py", "ORDONNER_UN_PLANNING.py", "REGLAGES_DU_PLANNING.csv",
            "ECRIRE_LE_TABLEAU.py", "AVANT_DE_DEMANDER.py")
M1 = datetime.datetime(2026, 11, 18, 13, 0, tzinfo=P)
ENTETE = ("etape;livre;depend_de;charge_h_min;charge_h_max;delai_h_min;delai_h_max;ecart;agents_min;agents_max;"
          "points_min;points_max;jugement_auteur;etat")
CARTE = ("panne;categorie;detection;reponse;tenue_par;reste_a_l_humain\n"
         "P1;redemarrage_machine;programmes/ORDONNER_UN_PLANNING.py : limite passée sans preuve;RELANCER;reveil_du_chat;rien\n"
         "P2;agent_tue;programmes/ORDONNER_UN_PLANNING.py : limite passée sans preuve;RELANCER;ordonnanceur;rien\n"
         "P3;forfait;programmes/CONTROLER_UN_PLANNING.py : estimation;ESTIMÉ;ordonnanceur;rien\n"
         "P4;contexte;NON PROGRAMMABLE : la conversation ne se lit pas;consigne fixe;reveil_du_chat;rien\n"
         "P5;executant_occupe;SANS OBJET : aucun exécutant extérieur dans ce projet d'épreuve;;humain;rien\n"
         "P6;demande_refusee;SANS OBJET : aucune demande;;humain;rien\n"
         "P7;donnees_perimees;SANS OBJET : aucune donnée;;humain;rien\n"
         "P8;decision_humaine;programmes/ORDONNER_UN_PLANNING.py : RDV;question;chat;répondre\n")


def sh(cmd, cwd, env=None):
    """Lance une commande, rend (code, sortie). Bornée à 120 s."""
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=120, env=env)
    return p.returncode, p.stdout + p.stderr


def sur(cmd, cwd, env=None):
    """Comme sh, mais une commande de PRÉPARATION qui échoue lève RuntimeError avec sa cause : l'épreuve rougit
    (m10 de la relecture f2ce23138 : un commit raté laissait l'origine vide et 36 épreuves sur 38 vertes)."""
    c, o = sh(cmd, cwd, env)
    if c != 0:
        raise RuntimeError(f"préparation ratée : {' '.join(cmd[:4])} → {c} {o.strip()[:300]}")
    return o


ETAT = "etat-pl"
PREFIXE = "/AILLEURS/depot"     # racine_des_preuves des épreuves : les preuves n'existent que rendues relatives au clone


def depot(t, prog, nom="clone", nu=None):
    """Fabrique (ou réutilise) un dépôt nu « origine » et un clone portant les programmes `prog` ; rend (clone, env)."""
    env = dict(os.environ, GIT_AUTHOR_NAME="e", GIT_AUTHOR_EMAIL="e@e", GIT_COMMITTER_NAME="e", GIT_COMMITTER_EMAIL="e@e")
    neuf = nu is None
    nu = nu or os.path.join(t, "origine.git")
    cl = os.path.join(t, nom)
    if neuf:
        sur(["git", "init", "-q", "--bare", nu], t)
    sur(["git", "clone", "-q", nu, cl], t)
    if not neuf:
        sur(["git", "checkout", "-q", "main"], cl, env)
    if neuf:
        os.makedirs(os.path.join(cl, "programmes"))
        for n in FICHIERS:
            shutil.copy(os.path.join(prog, n), os.path.join(cl, "programmes", n))
        sur(["git", "add", "-A"], cl, env)
        sur(["git", "commit", "-q", "-m", "x"], cl, env)
        sur(["git", "push", "-q", "origin", "HEAD:refs/heads/main"], cl, env)
    return cl, env


def planning(cl, etapes, extra="", pct="5", capture="2026-11-18 12:36", raz="2026-11-25 02:00", carte=CARTE,
             rdv=(), cap="6", releve="2026-11-18 12:40", en_cours="0", sans_jalon=()):
    """Écrit un planning d'épreuve sous <clone>/pl ; `etapes` : [(id, deps, état)] ; rend le dossier.
    Les preuves sont écrites sous PREFIXE (absent de la machine) : elles ne se trouvent que rendues relatives au clone."""
    d = os.path.join(cl, "pl")
    os.makedirs(os.path.join(d, "preuves"), exist_ok=True)
    w = lambda n, x: open(os.path.join(d, n), "w", encoding="utf-8").write(x)
    w("planning.csv", f"cle;valeur\nobjectif;Éprouver le tunnel.\ndebut;{releve}\n"
      f"forfait_capture;{capture}\nforfait_pourcentage;{pct}\nforfait_remise_a_zero;{raz}\n"
      f"ressources_releve;{releve}\nagents_plafond;6\nagents_en_cours;{en_cours}\nprocesseurs;2\n"
      f"agents_simultanes_max;{cap}\nbranche_d_etat;{ETAT}\nracine_des_preuves;{PREFIXE}\n"
      "disque_libre_go;10\ngithub;oui\nlimites_parallelisme;2 processeurs\njugement_auteur;JUGE.md\n"
      "estimation_expert;EXPERT.md\njalons;jalons.csv\n"
      + ("carte_des_pannes;carte.csv\n" if carte is not None else "") + extra)
    if carte is not None:
        w("carte.csv", carte)
    w("etapes.csv", ENTETE + "\n" + "".join(f"{i};livre {i};{dp};1;1;2;4;e;1;1;1;1;JUSTE;{et}\n" for i, dp, et in etapes))
    w("leviers.csv", "etape;levier;verdict;gain_ou_raison\n" +
      "".join(f"{i};{n};NON APPLICABLE;r\n" for i, _, _ in etapes for n in range(1, 7)))
    ids = " ".join(i for i, _, _ in etapes)
    w("JUGE.md", f"écrit le 2026-11-18 12:00\n{ids}\n")
    w("EXPERT.md", f"écrit le 2026-11-18 12:30\n{ids}\n")
    w("jalons.csv", "jalon;echeance;preuve;libelle\n" + "".join(
        f"{i};2026-11-30 12:00;{'RDV ' if i in rdv else ''}{PREFIXE}/pl/preuves/{i}.md;{i}\n" for i, _, _ in etapes
        if i not in sans_jalon))
    return d


def prouver(d, i):
    open(os.path.join(d, "preuves", i + ".md"), "w", encoding="utf-8").write("fait\n")


def distant(t, chemin):
    """Lit un fichier de la branche d'état au dépôt nu ; None s'il manque."""
    c, o = sh(["git", "--git-dir", os.path.join(t, "origine.git"), "show", f"{ETAT}:{chemin}"], t)
    return o if c == 0 else None


class Jeu:
    """Un jeu de programmes à éprouver : chemins et appels."""

    def __init__(self, prog, t):
        self.prog, self.t = prog, t
        self.n = 0

    def neuf(self):
        self.n += 1
        t = os.path.join(self.t, f"cas{self.n}")
        os.makedirs(t)
        cl, env = depot(t, self.prog)
        return t, cl, env

    def ordo(self, cl, env, d, quand=M1, appliquer=True, auteur="chat", plus=()):
        a = [sys.executable, os.path.join(cl, "programmes", "ORDONNER_UN_PLANNING.py"), d,
             f"--maintenant={quand:%Y-%m-%dT%H:%M}", f"--auteur={auteur}"] + (["--appliquer"] if appliquer else []) \
            + list(plus)
        return sh(a, cl, env)

    def module(self, cl, nom):
        sys.path.insert(0, os.path.join(cl, "programmes"))
        try:
            for n in ("TENIR_UN_PLANNING", "CONTROLER_UN_PLANNING", "ORDONNER_UN_PLANNING"):
                sys.modules.pop(n, None)
            spec = importlib.util.spec_from_file_location(nom, os.path.join(cl, "programmes", nom + ".py"))
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            return m
        finally:
            sys.path.pop(0)

    def ctl(self, cl, d, quand=M1):
        m = self.module(cl, "CONTROLER_UN_PLANNING")
        return m.controler(d, quand, os.path.join(cl, "programmes", "REGLAGES_DU_PLANNING.csv"))


def debut(o, mot):
    """Les lignes de la sortie qui commencent par `mot` (la consigne du REVEIL cite les repères)."""
    return [l for l in o.splitlines() if l.startswith(mot)]


def k1_sans_veilleur_code_2(j):
    t, cl, env = j.neuf()
    seul = os.path.join(t, "seul")
    os.makedirs(seul)
    shutil.copy(os.path.join(cl, "programmes", "CONTROLER_UN_PLANNING.py"), seul)
    c, o = sh([sys.executable, os.path.join(seul, "CONTROLER_UN_PLANNING.py"), "x"], seul, env)
    assert c == 2 and "Traceback" not in o and o.startswith("ARRET"), (c, o)


def k2_releve_frais(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "en_cours")], en_cours="1")
    c, s, r = j.ctl(cl, d)
    assert r == [], r
    assert any(l.startswith("CALCUL forfait RELEVÉ") for l in c), c
    assert any("— forfait RELEVÉ" in l for l in c if l.startswith("CALCUL fin réelle")), c


def k3_releve_perime_estime_sans_refus(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire")])
    c, s, r = j.ctl(cl, d, datetime.datetime(2026, 11, 19, 20, 0, tzinfo=P))
    assert not [x for x in r if "FORFAIT" in x], r
    l = [x for x in c if x.startswith("CALCUL forfait ESTIMÉ")]
    assert l and "ESTIMÉ 19.8 %" in l[0], c          # 5 % + 5/10,6 %/h × 31,4 h
    assert any("— forfait ESTIMÉ" in x for x in c if x.startswith("CALCUL fin réelle")), c
    assert any(x.startswith("FORFAIT ESTIMÉ") for x in s), s


def k4_remise_passee_avancee(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire")])
    c, s, r = j.ctl(cl, d, datetime.datetime(2026, 11, 26, 10, 0, tzinfo=P))
    l = [x for x in c if x.startswith("CALCUL forfait ESTIMÉ")]
    assert l and "remise à zéro 2026-12-02 02:00" in l[0] and "ESTIMÉ 15.1 %" in l[0], l
    assert not [x for x in r if "FORFAIT" in x], r


def k5_au_dela_du_plafond_signal(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire")], pct="97", capture="2026-11-24 12:00", releve="2026-11-24 12:00")
    c, s, r = j.ctl(cl, d, datetime.datetime(2026, 11, 24, 13, 0, tzinfo=P))
    assert not [x for x in r if x.startswith("FORFAIT :")], r
    assert any("au-delà du plafond" in x for x in s), s


def k6_carte_absente_refusee(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire")], carte=None)
    _, _, r = j.ctl(cl, d)
    assert any(x.startswith("CARTE DES PANNES ABSENTE") for x in r), r


def k7_carte_categorie_manquante(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire")], carte="\n".join(CARTE.splitlines()[:-1]) + "\n")
    _, _, r = j.ctl(cl, d)
    assert any("non traitée(s) decision_humaine" in x for x in r), r


def k8_carte_formes(j):
    t, cl, env = j.neuf()
    mauvaise = CARTE + ("P9;inconnue;programmes/ORDONNER_UN_PLANNING.py;r;chat;rien\n"
                        "P10;forfait;programmes/N_EXISTE_PAS.py : x;r;chat;rien\n"
                        "P11;forfait;SANS OBJET :;;chat;rien\n"
                        "P12;forfait;programmes/ORDONNER_UN_PLANNING.py;r;personne;rien\n"
                        "P13;forfait;programmes/ORDONNER_UN_PLANNING.py;;chat;rien\n")
    d = planning(cl, [("A", "", "a_faire")], carte=mauvaise)
    _, s, r = j.ctl(cl, d)
    attendus = ["catégorie « inconnue »", "lu « programmes/N_EXISTE_PAS.py »", "« SANS OBJET : » sans raison",
                "tenue_par « personne »", "(P13) : réponse vide"]
    for a in attendus:
        assert any(a in x for x in r), (a, r)
    assert any("NON PROGRAMMABLE : la conversation ne se lit pas" in x for x in s), s


def k10_tableau_ecrit_depuis_le_controle(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "en_cours"), ("B", "A", "a_faire")], en_cours="1")
    sortie = os.path.join(t, "tableau.md")
    c, o = sh([sys.executable, os.path.join(cl, "programmes", "ECRIRE_LE_TABLEAU.py"), d, sortie,
               f"--maintenant={M1:%Y-%m-%dT%H:%M}"], cl, env)
    lignes = open(sortie, encoding="utf-8").read().splitlines()
    assert c == 0 and [l.split(" | ")[0] for l in lignes if l.startswith("| A") or l.startswith("| B")] == ["| A", "| B"], (c, o)
    assert any("forfait RELEVÉ" in l for l in lignes if l.startswith("- CALCUL fin réelle")), lignes


def k9_signe_de_vie_au_controle(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "en_cours")], en_cours="1")
    _, s, r = j.ctl(cl, d)
    assert r == [] and any(x.startswith("SIGNE DE VIE DE LA CONVERSATION ABSENT") for x in s), (r, s)
    j.ordo(cl, env, d)                                   # le passage pousse vie/chat.txt (13h00)
    sh(["git", "fetch", "-q", "origin"], cl, env)
    _, s, r = j.ctl(cl, d, M1 + datetime.timedelta(minutes=29))
    assert r == [], r
    _, s, r = j.ctl(cl, d, M1 + datetime.timedelta(minutes=31))
    assert any(x.startswith("ERREUR SIGNE DE VIE PÉRIMÉ") for x in r), r
    _, s, r = j.ctl(cl, d, M1 - datetime.timedelta(minutes=5))
    assert any(x.startswith("ERREUR SIGNE DE VIE DATÉ DANS LE FUTUR") for x in r), r


def k11_tenue_declaree_sans_preuve_refusee(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "tenu"), ("B", "A", "en_cours")], en_cours="1")
    _, _, r = j.ctl(cl, d)
    assert any(x.startswith("ÉTAPE A DÉCLARÉE TENUE, PREUVE ABSENTE") for x in r), r


# ---------------------------------------------------------------- épreuves de l'ordonnanceur
def o1_prise_puis_en_cours(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire"), ("B", "A", "a_faire")])
    c, o = j.ordo(cl, env, d)
    assert c == 0 and debut(o, "LANCER A chat") and not debut(o, "LANCER B"), (c, o)
    p = distant(t, "prises/A.txt")
    assert p and "qui=chat" in p and "limite=2026-11-18 17:00" in p and "chutes=0" in p and "branche=" not in p, p
    c, o = j.ordo(cl, env, d, M1 + datetime.timedelta(minutes=10))
    assert c == 0 and debut(o, "EN COURS A : pris par chat") and not debut(o, "LANCER"), (c, o)


def o2_tombee_relancer_puis_decision(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire")])
    j.ordo(cl, env, d)
    q = M1
    for n in (1, 2):
        q = q + datetime.timedelta(hours=5)              # limite de la prise (4 h) passée sans preuve : tombée
        c, o = j.ordo(cl, env, d, q)
        assert c == 0 and debut(o, "RELANCER A chat") and f"chutes={n}" in distant(t, "prises/A.txt"), (n, c, o)
    q = q + datetime.timedelta(hours=5)
    c, o = j.ordo(cl, env, d, q)
    assert c == 1 and debut(o, "DÉCISION A") and not debut(o, "RELANCER"), (c, o)
    c, o = j.ordo(cl, env, d, q + datetime.timedelta(minutes=10))
    assert c == 1 and debut(o, "DÉCISION A") and not debut(o, "RELANCER") and not debut(o, "LANCER"), (c, o)


def o3_tenue_ecrite_jamais_relancee(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire"), ("B", "A", "a_faire")])
    j.ordo(cl, env, d)
    prouver(d, "A")
    c, o = j.ordo(cl, env, d, M1 + datetime.timedelta(minutes=10))
    assert c == 0 and debut(o, "TENUE A") and debut(o, "LANCER B chat") and "tenue=" in distant(t, "prises/A.txt"), o
    os.remove(os.path.join(d, "preuves", "A.md"))       # session neuve : la preuve n'est plus là (sonde N2)
    c, o = j.ordo(cl, env, d, M1 + datetime.timedelta(hours=6))
    assert not debut(o, "LANCER A") and not debut(o, "RELANCER A"), o


def o4_humain(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("Q", "", "a_faire")], rdv=("Q",))
    c, o = j.ordo(cl, env, d)
    assert debut(o, "LANCER Q humain : d'abord python3 programmes/AVANT_DE_DEMANDER.py 'livre Q'") and "courriel" not in o, o
    c, o = j.ordo(cl, env, d, M1 + datetime.timedelta(minutes=10))
    assert c == 0 and debut(o, "EN ATTENTE DE JEAN-LUC Q"), (c, o)


def o5_places(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire"), ("B", "", "a_faire")], cap="1")
    c, o = j.ordo(cl, env, d)
    assert len(debut(o, "LANCER ")) == 1 and debut(o, "EN FILE") and distant(t, "prises/B.txt") is None, o


def o6_github_bloquee_et_prives(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire"), ("B", "", "a_faire"), ("C", "", "a_faire"), ("D", "", "a_faire")],
                 extra="calculs;A:2|B:2:PRIVÉ données privées absentes du dépôt public|C:0,2|D:0,3\n")
    c, o = j.ordo(cl, env, d)
    assert c == 1 and debut(o, "BLOQUÉE A : exécutant « github » sans voie") and not debut(o, "LANCER A"), (c, o)
    assert debut(o, "CALCUL LOURD SUR LA MACHINE B : données privées absentes du dépôt public"), o
    assert debut(o, "EN FILE") and "calculs lourds" in o, o       # B, C, D sur la machine : 2 lourds au plus


def o8_panne_reseau_code_2_sans_rien(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire")])
    j.ordo(cl, env, d)
    avant = distant(t, "prises/A.txt")
    sh(["git", "remote", "set-url", "origin", os.path.join(t, "nulle_part.git")], cl, env)   # sonde N1
    c, o = j.ordo(cl, env, d, M1 + datetime.timedelta(hours=5))
    assert c == 2 and o.strip().count("\n") == 0 and o.startswith("ARRET") and "RELANCER" not in o, (c, o)
    assert "Impossible" in o and "a échoué" in o, o                       # la cause : git, pas un bogue (m12)
    assert distant(t, "prises/A.txt") == avant


def o9_conflit_de_poussee(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire")])
    cl2, _ = depot(t, j.prog, "clone2", os.path.join(t, "origine.git"))
    shutil.copytree(d, os.path.join(cl2, "pl"))
    d2 = os.path.join(cl2, "pl")
    m = j.module(cl2, "ORDONNER_UN_PLANNING")
    vrai = m.lire_tout

    def lire_puis_laisser_l_autre_ecrire(*a):
        L = vrai(*a)
        j.ordo(cl, env, d)                               # la conversation prend A pendant que la tâche décide
        return L
    m.lire_tout = lire_puis_laisser_l_autre_ecrire
    lignes, code = m.ordonner(d2, M1, True, "tache")
    assert code == 75 and lignes[0].startswith("OCCUPÉ") and not [l for l in lignes if "LANCER" in l], (code, lignes)
    assert "qui=chat" in distant(t, "prises/A.txt") and distant(t, "vie/tache.txt") is None


def o10_dependance_inconnue_code_2(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire"), ("B", "Z", "a_faire")])
    c, o = j.ordo(cl, env, d)
    assert c == 2 and "dépendance(s) inconnue(s) Z" in o and not debut(o, "LANCER"), (c, o)


def o11_bloquees_jamais_muettes(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "tenu"), ("B", "A", "a_faire"), ("C", "", "a_faire"), ("D", "C", "a_faire")],
                 sans_jalon=("C",))
    c, o = j.ordo(cl, env, d, appliquer=False)
    assert c == 1 and debut(o, "BLOQUÉE A : déclarée tenue") and debut(o, "BLOQUÉE C : aucun jalon"), (c, o)
    assert not debut(o, "LANCER") and o.splitlines()[-1].startswith("BLOQUÉ : 4 étape(s) non tenue(s)"), (c, o)
    c, o = j.ordo(cl, env, d, appliquer=False, plus=["--chien-de-garde"])
    assert c == 1 and o.startswith("ALERTE CHIEN DE GARDE") and "4 étape(s)" in o, (c, o)   # B1 : jamais muet


def o12_a_blanc_n_ecrit_rien(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire")])
    c, o = j.ordo(cl, env, d, appliquer=False)
    a, _ = sh(["git", "--git-dir", os.path.join(t, "origine.git"), "rev-parse", "--verify", "-q", ETAT], t)
    assert debut(o, "LANCER A") and a != 0, o


def o13_signes_de_vie_par_auteur(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire")])
    j.ordo(cl, env, d)
    j.ordo(cl, env, d, M1 + datetime.timedelta(minutes=10), auteur="tache")
    assert distant(t, "vie/chat.txt") == "SIGNE DE VIE 2026-11-18T13:00:00+01:00 · pl · chat\n", distant(t, "vie/chat.txt")
    assert distant(t, "vie/tache.txt") == "SIGNE DE VIE 2026-11-18T13:10:00+01:00 · pl · tache\n"


def o14_consigne_fixe(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire")])
    c, o = sh([sys.executable, os.path.join(cl, "programmes", "ORDONNER_UN_PLANNING.py"), d, "--consigne"], cl, env)
    tache = debut(o, "CONSIGNE DE LA TÂCHE HORAIRE")[0]
    assert c == 0 and "pl --appliquer --auteur=chat" in o and tache.index("--chien-de-garde") < tache.index(
        "--appliquer") and "rebase" not in o and "courriel" not in o, o


def o15_chien_de_garde(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire")])
    g = lambda q: j.ordo(cl, env, d, q, appliquer=False, plus=["--chien-de-garde"])
    c, o = g(M1)
    assert c == 1 and o.startswith("ALERTE CHIEN DE GARDE : signe de vie de la conversation absent"), (c, o)
    j.ordo(cl, env, d)                                   # la conversation passe à 13h00
    c, o = g(M1 + datetime.timedelta(minutes=30))
    assert c == 0 and o.startswith("CHIEN DE GARDE : la conversation vit"), (c, o)
    c, o = g(M1 + datetime.timedelta(minutes=31))
    assert c == 1 and "vieux de 31 min" in o, (c, o)
    c, o = g(M1 - datetime.timedelta(minutes=5))        # sonde : signe daté dans le futur
    assert c == 1 and "daté dans le futur" in o, (c, o)
    j.ordo(cl, env, d, M1 + datetime.timedelta(minutes=40), auteur="tache")
    c, o = g(M1 + datetime.timedelta(minutes=41))       # la tâche seule vit : la conversation reste morte
    assert c == 1, (c, o)
    prouver(d, "A")
    j.ordo(cl, env, d, M1 + datetime.timedelta(minutes=50), auteur="tache")
    c, o = g(M1 + datetime.timedelta(hours=3))          # tout est tenu : rien à surveiller, aucune alerte
    assert c == 0 and "toutes les étapes sont tenues" in o, (c, o)
    sh(["git", "remote", "set-url", "origin", os.path.join(t, "nulle_part.git")], cl, env)
    c, o = g(M1 + datetime.timedelta(hours=3))          # ne peut pas lire : alerte
    assert c == 1 and "ne peut pas lire" in o, (c, o)


def o16_prise_abimee(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire")])
    j.ordo(cl, env, d)
    m = j.module(cl, "ORDONNER_UN_PLANNING")

    def casse(*a):
        raise ValueError("situation cassée")
    m.situation = casse                                   # tout le corps du chien est dans son try (m3)
    ligne, code = m.chien_de_garde(d, M1)
    assert code == 1 and "situation cassée" in ligne, (code, ligne)
    w = os.path.join(t, "w")                              # une prise sans limite, poussée par un autre (sonde m3, X2)
    sh(["git", "clone", "-q", "-b", ETAT, os.path.join(t, "origine.git"), w], t)
    open(os.path.join(w, "prises", "A.txt"), "w").write("etape=A\nqui=x\nheure=2026-11-18 13:00\nchutes=0\ntenue=x\n")
    sh(["git", "commit", "-qam", "abime"], w, env)
    sh(["git", "push", "-q", "origin", ETAT], w, env)
    c, o = j.ordo(cl, env, d, M1 + datetime.timedelta(minutes=10))
    assert c == 2 and o.startswith("ARRET") and "limite" in o, (c, o)
    c, o = j.ordo(cl, env, d, appliquer=False, plus=["--chien-de-garde"])
    assert c == 1 and o.startswith("ALERTE CHIEN DE GARDE") and "limite" in o, (c, o)


def o17_refus_par_crochet_code_2(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire")])
    crochet = os.path.join(t, "origine.git", "hooks", "pre-receive")
    open(crochet, "w").write("#!/bin/sh\necho refusé par le dépôt >&2\nexit 1\n")
    os.chmod(crochet, 0o755)                              # branche protégée : refus sans course (M1)
    for _ in range(2):
        c, o = j.ordo(cl, env, d)
        assert c == 2 and o.startswith("ARRET") and "OCCUPÉ" not in o, (c, o)


def o18_en_cours_declare_importe_une_fois(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "en_cours"), ("B", "", "a_faire")], cap="1", en_cours="1")
    c, o = j.ordo(cl, env, d)
    assert c == 0 and debut(o, "EN COURS A : pris par déclaration") and not debut(o, "LANCER A"), (c, o)
    assert debut(o, "EN FILE B") and "qui=déclaration" in distant(t, "prises/A.txt"), o     # B2
    e = os.path.join(d, "etapes.csv")
    texte = open(e).read()
    open(e, "w").write(texte.replace(";JUSTE;a_faire", ";JUSTE;en_cours"))
    c, o = j.ordo(cl, env, d, M1 + datetime.timedelta(minutes=10))
    assert distant(t, "prises/B.txt") is None and debut(o, "EN FILE B"), o                 # jamais ensuite


def k12_controle_lit_la_situation(j):
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire"), ("B", "A", "a_faire")])
    c, s, r = j.ctl(cl, d)
    assert any("RESSOURCES SOUS-EMPLOYÉES : A" in x for x in r), r        # états déclarés : A prête, 0 agent
    j.ordo(cl, env, d)                                                    # l'ordonnanceur prend A
    sh(["git", "fetch", "-q", "origin"], cl, env)
    c, s, r = j.ctl(cl, d, M1 + datetime.timedelta(minutes=5))
    assert not any("SOUS-EMPLOYÉES" in x for x in r), r
    assert any(x.startswith("CALCUL étapes prêtes non lancées, la moins de marge d'abord (situation") for x in c), c


CARTE_DU_DEPOT = os.path.join(RACINE, "etudes", "CARTE_DES_PANNES_DU_PROJET.csv")


def k13_carte_du_depot_se_lit(j):
    """B4 (relecture 8887e31e) : la VRAIE carte du dépôt se lit, ligne par ligne, et passe le contrôle de forme.
    Le jeu sabotant porte sa propre copie de la carte (même nom de fichier) ; sinon la carte du dépôt est lue.
    La racine passée est RACINE, celle de l'arbre qui porte ce fichier : la copie jouée sur GitHub n'a pas de .git
    (B7 de la relecture f2ce23138)."""
    t, cl, env = j.neuf()
    m = j.module(cl, "CONTROLER_UN_PLANNING")
    R = m.lire_reglages(os.path.join(cl, "programmes", "REGLAGES_DU_PLANNING.csv"))
    propre = os.path.join(j.prog, os.path.basename(CARTE_DU_DEPOT))
    carte = propre if os.path.isfile(propre) else CARTE_DU_DEPOT
    attendu = sum(1 for l in open(carte, encoding="utf-8").read().splitlines()[1:] if l.strip())
    refus, signaux = [], []
    n = m.controler_la_carte(carte, RACINE, R, refus, signaux)    # une colonne en trop lève Impossible : rouge
    assert n == attendu, (n, attendu)
    assert refus == [], refus


def k14_c14_non_tenue_lue_dans_la_situation(j):
    """M5 (relecture 8887e31e) : une étape DÉCLARÉE tenue sans preuve n'est pas tenue ; signe périmé → ERREUR,
    comme le chien de garde (cas rejoué du relecteur : chien ALERTE, contrôle muet)."""
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "tenu")])
    j.ordo(cl, env, d)                                   # pousse vie/chat.txt à 13h00 (A : BLOQUÉE)
    sh(["git", "fetch", "-q", "origin"], cl, env)
    _, s, r = j.ctl(cl, d, M1 + datetime.timedelta(minutes=31))
    assert any(x.startswith("ERREUR SIGNE DE VIE PÉRIMÉ") for x in r), r
    c, o = j.ordo(cl, env, d, quand=M1 + datetime.timedelta(minutes=31), appliquer=False, plus=["--chien-de-garde"])
    assert c == 1 and o.startswith("ALERTE CHIEN DE GARDE"), (c, o)


def k15_situation_illisible_refusee(j):
    """M5 (relecture 8887e31e) : situation impossible → REFUS « ERREUR ÉTAT ILLISIBLE », et aucune « prête » tirée
    des états déclarés à la place."""
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire"), ("B", "A", "a_faire")])
    f = os.path.join(d, "planning.csv")
    x = open(f, encoding="utf-8").read()
    open(f, "w", encoding="utf-8").write(x.replace(f"branche_d_etat;{ETAT}\n", "branche_d_etat;hors-forme\n"))
    c, s, r = j.ctl(cl, d)
    assert any(x.startswith("ERREUR ÉTAT ILLISIBLE") and "branche_d_etat" in x for x in r), r   # la cause (m12)
    assert not any("SOUS-EMPLOYÉES" in x for x in r), r
    assert any(x.endswith("(état illisible) : non calculées") for x in c), c                     # m11


def k16_sans_branche_la_situation_du_premier_passage(j):
    """M5 (relecture 8887e31e) : sans branche d'état, le contrôle lit situation comme l'ordonnanceur à son premier
    passage — A déclarée « ecrit » est importée en cours, B attend : rien n'est prêt."""
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "ecrit"), ("B", "A", "a_faire")], en_cours="1")
    c, s, r = j.ctl(cl, d)
    assert any(x == "CALCUL étapes prêtes non lancées, la moins de marge d'abord (situation de l'ordonnanceur) : aucune"
               for x in c), c
    assert not any("SOUS-EMPLOYÉES" in x for x in r), r


def k17_bogue_de_l_ordonnanceur_jamais_un_refus(j):
    """m12 (relecture f2ce23138) : un PROGRAMME faux (ici NameError dans situation) n'est jamais un refus « état
    illisible » : l'exception remonte du contrôle (la ligne de commande rend alors 2)."""
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire")])
    f = os.path.join(cl, "programmes", "ORDONNER_UN_PLANNING.py")
    with open(f, "a", encoding="utf-8") as x:
        x.write("\n\ndef situation(L, maintenant):\n    raise NameError('bogue posé par k17')\n")
    try:
        c, s, r = j.ctl(cl, d)
    except NameError as e:
        assert "bogue posé par k17" in str(e), e
        return
    raise AssertionError(f"le bogue est devenu un refus : {[x for x in r if 'ILLISIBLE' in x]}")


def k18_ligne_courte_ou_guillemet_non_ferme_refuses(j):
    """m9 (relecture f2ce23138) : sur une copie de la VRAIE carte, une ligne privée de sa dernière colonne, puis un
    guillemet ouvrant non fermé, lèvent Impossible avec leur cause — jamais une lecture silencieuse."""
    t, cl, env = j.neuf()
    m = j.module(cl, "CONTROLER_UN_PLANNING")
    propre = os.path.join(j.prog, os.path.basename(CARTE_DU_DEPOT))
    lignes = open(propre if os.path.isfile(propre) else CARTE_DU_DEPOT, encoding="utf-8").read().splitlines()
    for cas, l3, motif in (("courte", lignes[2].rsplit(";", 1)[0], "colonne manquante"),
                           ("guillemet", lignes[2].split(";", 1)[0] + ';"' + lignes[2].split(";", 1)[1], "saut de ligne")):
        f = os.path.join(t, cas + ".csv")
        open(f, "w", encoding="utf-8").write("\n".join(lignes[:2] + [l3] + lignes[3:]) + "\n")
        try:
            m.lire_table(f, m.COLONNES_PANNES)
        except m.Impossible as e:
            fin = "ligne 3 " if cas == "courte" else f"se termine à la ligne {len(lignes)} "
            assert motif in str(e) and fin in str(e), (cas, str(e))
            continue
        raise AssertionError(f"{cas} : lue sans refus")


def k20_donnee_hostile_jamais_une_erreur_du_programme(j):
    """n1 de la relecture a1e52c568 et superviseurs R-759 du 25-11-2026 (14h16, 14h19) : chaque champ de planning.csv,
    etapes.csv, jalons.csv et leviers.csv (une ligne chacun) reçoit tour à tour une valeur hostile ; le contrôle,
    sans puis avec branche d'état, ne lève JAMAIS (ni erreur du programme, ni Impossible = code 2) : une valeur de
    champ fausse est un REFUS (code 1). Exemple réel du relecteur : l'échéance « 30/11/2026 12:00 » tapée à la main."""
    hostiles = ("", "texte", "²", "1e12", "1e308", "inf", "-inf", "nan", "-1", "30/11/2026 12:00", "2026-02-30 12:00",
                "9999-12-31 23:59")
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire"), ("B", "A", "a_faire")])
    m = j.module(cl, "CONTROLER_UN_PLANNING")
    leves, vus = [], 0
    for avec_etat in (False, True):
        if avec_etat:
            j.ordo(cl, env, d)
            sur(["git", "fetch", "-q", "origin"], cl, env)
        for nom in ("planning.csv", "etapes.csv", "jalons.csv", "leviers.csv"):
            f = os.path.join(d, nom)
            propre = open(f, encoding="utf-8").read()
            lignes = [l.split(";") for l in propre.splitlines()]
            cibles = [(r, 1) for r in range(1, len(lignes))] if nom == "planning.csv" else \
                [(1, c) for c in range(len(lignes[0]))]
            for r, c in cibles:
                for v in hostiles:
                    l2 = [list(x) for x in lignes]
                    l2[r][c] = v
                    open(f, "w", encoding="utf-8").write("".join(";".join(x) + "\n" for x in l2))
                    vus += 1
                    try:
                        m.controler(d, M1, os.path.join(cl, "programmes", "REGLAGES_DU_PLANNING.csv"))
                    except Exception as e:
                        leves.append(f"{nom}:{lignes[r][0] if nom == 'planning.csv' else lignes[0][c]}={v!r} → "
                                     f"{type(e).__name__} {str(e)[:80]}")
            open(f, "w", encoding="utf-8").write(propre)
    assert vus > 400 and not leves, (vus, leves[:6])
    # le cas réel, en ligne de commande : code 1 et le refus nomme le jalon et le texte lu
    f = os.path.join(d, "jalons.csv")
    x = open(f, encoding="utf-8").read()            # lu AVANT d'ouvrir en écriture (qui vide le fichier)
    assert x.count("A;2026-11-30 12:00;") == 1, x
    open(f, "w", encoding="utf-8").write(x.replace("A;2026-11-30 12:00;", "A;30/11/2026 12:00;"))
    c, o = sh([sys.executable, os.path.join(cl, "programmes", "CONTROLER_UN_PLANNING.py"), d, "--maintenant=2026-11-18 13:00"],
              cl, env)
    assert c == 1 and "« 30/11/2026 12:00 » (jalon A)" in o and "imprévue" not in o, (c, o[-600:])


def k21_delais_aux_bornes_du_calendrier(j):
    """Superviseur R-759 du 25-11-2026, 14h19 : la somme des délais max se compare EN NOMBRE à la fin du calendrier ;
    juste en dessous (une heure), les dates se calculent sans lever ; juste au-dessus, REFUS « HORS DU CALENDRIER ».
    Le relevé du forfait est frais et la remise à zéro à venir : le calendrier repoussé après la remise est calculé."""
    t, cl, env = j.neuf()
    m = j.module(cl, "CONTROLER_UN_PLANNING")
    d = planning(cl, [("A", "", "a_faire"), ("B", "A", "a_faire")])
    f = os.path.join(d, "etapes.csv")
    propre = open(f, encoding="utf-8").read()
    raz = datetime.datetime(2026, 11, 25, 2, 0, tzinfo=P)
    borne = m.heures_jusqu_a_la_fin_du_calendrier(M1) - (raz - M1).total_seconds() / 3600
    for ecart, refuse in ((-1, False), (1, True)):
        h = (borne + ecart - 4) // 1                     # A garde 4 h ; B porte le reste (entier : la somme tombe juste)
        open(f, "w", encoding="utf-8").write(propre.replace("B;livre B;A;1;1;2;4;", f"B;livre B;A;1;1;2;{h:.0f};"))
        c, s, r = j.ctl(cl, d)
        hors = [x for x in r if x.startswith("DÉLAIS HORS DU CALENDRIER")]
        assert bool(hors) == refuse, (ecart, h, hors, r)
        if not refuse:
            assert any(x.startswith("CALCUL fin réelle (forfait compris) réaliste") for x in c), c


def k22_ligne_vide_numero_physique(j):
    """n2 de la relecture a1e52c568 : une ligne vide (sautée par le lecteur CSV) ne décale pas le numéro annoncé —
    cas du relecteur : en-tête, « a;1 », ligne vide, « b » → « ligne 4 »."""
    t, cl, env = j.neuf()
    m = j.module(cl, "CONTROLER_UN_PLANNING")
    f = os.path.join(t, "vide.csv")
    open(f, "w", encoding="utf-8").write("cle;valeur\na;1\n\nb\n")
    try:
        m.lire_table(f, ("cle", "valeur"))
    except m.Impossible as e:
        assert "ligne 4 " in str(e) and "colonne manquante" in str(e), str(e)
        return
    raise AssertionError("ligne courte lue sans refus")


def k19_prise_corrompue_refus_etat_illisible(j):
    """Superviseur R-759 du 25-11-2026 (condition 2) : un ÉTAT corrompu (une prise sans « = » sur la branche d'état)
    reste un REFUS « ERREUR ÉTAT ILLISIBLE » qui nomme la prise — le resserrement de C9bis ne le change pas en ARRET."""
    t, cl, env = j.neuf()
    d = planning(cl, [("A", "", "a_faire")])
    j.ordo(cl, env, d)
    w = os.path.join(t, "w")
    sur(["git", "clone", "-q", "-b", ETAT, os.path.join(t, "origine.git"), w], t)
    open(os.path.join(w, "prises", "A.txt"), "w", encoding="utf-8").write("ceci n'est pas une prise\n")
    sur(["git", "commit", "-qam", "corrompue"], w, env)
    sur(["git", "push", "-q", "origin", ETAT], w, env)
    sur(["git", "fetch", "-q", "origin"], cl, env)
    c, s, r = j.ctl(cl, d)
    assert any(x.startswith("ERREUR ÉTAT ILLISIBLE") and "prise illisible" in x for x in r), r


def avant(j, question, racine=None):
    return sh([sys.executable, os.path.join(j.prog, "AVANT_DE_DEMANDER.py"), question,
               f"--racine={racine or RACINE}"], RACINE)          # l'arbre éprouvé, jamais origin/main (B8)


def trouves(o):
    return [l.split()[2] for l in o.splitlines() if l.startswith("À LIRE ") and not l.startswith("À LIRE AVANT")]


def a1_question_du_15_11_trouve_a814(j):
    c, o = avant(j, "quand ai-je le droit d'installer ?")
    assert c == 1 and "A-814" in trouves(o) and o.startswith("DÉCISIONS QUI EN PARLENT — À LIRE"), (c, o[-600:])
    assert "déjà tranché" not in o and "AVANT_DE_DEMANDER" not in o, o[-600:]


def a2_blocs_de_la_fiche_a788_et_erratum_a907(j):
    c, o = avant(j, "comptabilité des blocs de la fiche")
    assert c == 1 and "A-907" in trouves(o) and "A-788" in o and "déjà tranché" not in o, (c, o[-900:])
    assert all("VOIR L'ERRATUM A-907" in l for l in o.splitlines() if l.startswith("À LIRE A-141 ")), o[-900:]


def a3_societes_sorties_trouve_a713_a802_a829(j):
    c, o = avant(j, "sociétés sorties refus")
    assert c == 1 and {"A-713", "A-802", "A-829"} <= set(trouves(o)), (c, trouves(o))


def a4_jamais_tranchee_ne_trouve_rien(j):
    c, o = avant(j, "faut-il acheter des obligations japonaises en yen")
    assert c == 0 and not trouves(o) and o.startswith("RIEN TROUVÉ, ce qui ne prouve rien"), (c, o[:600])


def a5_lecture_impossible_code_2(j):
    t = os.path.join(j.t, "vide")
    os.makedirs(t, exist_ok=True)
    c, o = avant(j, "quand ai-je le droit d'installer ?", t)
    assert c == 2 and o.startswith("ARRET"), (c, o)


EPREUVES = [k1_sans_veilleur_code_2, k2_releve_frais, k3_releve_perime_estime_sans_refus, k4_remise_passee_avancee,
            k5_au_dela_du_plafond_signal, k6_carte_absente_refusee, k7_carte_categorie_manquante, k8_carte_formes,
            k9_signe_de_vie_au_controle, k10_tableau_ecrit_depuis_le_controle, k11_tenue_declaree_sans_preuve_refusee,
            k12_controle_lit_la_situation, k13_carte_du_depot_se_lit, k14_c14_non_tenue_lue_dans_la_situation,
            k15_situation_illisible_refusee, k16_sans_branche_la_situation_du_premier_passage,
            k17_bogue_de_l_ordonnanceur_jamais_un_refus, k18_ligne_courte_ou_guillemet_non_ferme_refuses,
            k19_prise_corrompue_refus_etat_illisible, k20_donnee_hostile_jamais_une_erreur_du_programme,
            k21_delais_aux_bornes_du_calendrier, k22_ligne_vide_numero_physique,
            o1_prise_puis_en_cours, o2_tombee_relancer_puis_decision, o3_tenue_ecrite_jamais_relancee, o4_humain,
            o5_places, o6_github_bloquee_et_prives, o8_panne_reseau_code_2_sans_rien,
            o9_conflit_de_poussee, o10_dependance_inconnue_code_2, o11_bloquees_jamais_muettes,
            o12_a_blanc_n_ecrit_rien, o13_signes_de_vie_par_auteur, o14_consigne_fixe, o15_chien_de_garde,
            o16_prise_abimee, o17_refus_par_crochet_code_2, o18_en_cours_declare_importe_une_fois,
            a1_question_du_15_11_trouve_a814, a2_blocs_de_la_fiche_a788_et_erratum_a907,
            a3_societes_sorties_trouve_a713_a802_a829, a4_jamais_tranchee_ne_trouve_rien, a5_lecture_impossible_code_2]

# Chaque sabotage retire UN garde-fou ; au moins une épreuve doit rougir.
SABOTAGES = {
    "S1 import du veilleur sans garde (plantage code 1)": ("CONTROLER_UN_PLANNING.py",
        "        sys.exit(2)\n    raise", "        raise\n    raise"),
    "S2 relevé périmé refusé (le frein revient)": ("CONTROLER_UN_PLANNING.py",
        '            signaux.append(f"FORFAIT ESTIMÉ (relevé', '            refus.append(f"FORFAIT ESTIMÉ (relevé'),
    "S3 estimation sans consommation": ("CONTROLER_UN_PLANNING.py",
        "        est = pct + taux * max(age, 0.0)", "        est = pct"),
    "S4 remise à zéro non avancée": ("CONTROLER_UN_PLANNING.py",
        "        raz_now = raz_now + datetime.timedelta(hours=periode_h)", "        break"),
    "S5 plafond refuse au lieu de signaler": ("CONTROLER_UN_PLANNING.py",
        '            signaux.append(f"FORFAIT {source_forfait} {pct:.1f} % au-delà',
        '            refus.append(f"FORFAIT {source_forfait} {pct:.1f} % au-delà'),
    "S6 carte non exigée": ("CONTROLER_UN_PLANNING.py",
        '    controler_la_carte(carte, racine_du_depot(os.path.dirname(carte)) if carte else None, R, refus, signaux)',
        "    pass"),
    "S7 catégories non comptées": ("CONTROLER_UN_PLANNING.py",
        "    manque = [c for c in R[\"categories_de_pannes\"] if c not in vues]", "    manque = []"),
    "S8 programme de détection non vérifié": ("CONTROLER_UN_PLANNING.py",
        "            if not prog or racine is None or not os.path.isfile(os.path.join(racine, prog)):",
        "            if not prog:"),
    "S9 « prête » sans les dépendances": ("CONTROLER_UN_PLANNING.py",
        '    return [i for i in ids if etat[i] == "a_faire" and all(etat[d] in qui_liberent for d in deps[i])]',
        '    return [i for i in ids if etat[i] == "a_faire"]'),
    "S10 signe périmé accepté au contrôle": ("CONTROLER_UN_PLANNING.py",
        '    elif reste and (age < 0 or age > R["signe_de_vie_max_min"]):', "    elif False:"),
    "S11 tenue déclarée sans preuve acceptée": ("CONTROLER_UN_PLANNING.py",
        '                and TENIR_UN_PLANNING.etat_de_la_preuve(j, maintenant) != "tenu"):', "                and False):"),
    "S12 tableau sans les lignes du contrôle": ("ECRIRE_LE_TABLEAU.py",
        "        m = R.match(l)\n", "        m = None\n"),
    "S13 code 2 qui conclut (ls-remote ignoré)": ("ORDONNER_UN_PLANNING.py",
        '            raise C.Impossible(f"git ls-remote origin a échoué ({motif})")', '            out = ""'),
    "S14 tenue réévaluée à chaque passage": ("ORDONNER_UN_PLANNING.py",
        '        if p and p.get("tenue"):\n            etat[i] = "tenue"', '        if False:\n            etat[i] = "tenue"'),
    "S15 preuve lue au chemin absolu": ("ORDONNER_UN_PLANNING.py",
        '    if prefixe and c.startswith(prefixe.rstrip("/") + "/"):\n        c = os.path.join',
        '    if False:\n        c = os.path.join'),
    "S16 jamais tombée": ("ORDONNER_UN_PLANNING.py",
        '> maintenant.astimezone(U) else "tombee"', '> maintenant.astimezone(U) else "en_cours"'),
    "S17 chutes sans fin": ("ORDONNER_UN_PLANNING.py",
        '        elif e == "decision" or chutes >= CHUTES_MAX:', '        elif e == "decision":'),
    "S18 refus de poussée ignoré": ("ORDONNER_UN_PLANNING.py",
        '        if ecrire_et_pousser(L, fichiers, auteur, maintenant) == "refusé":',
        '        if ecrire_et_pousser(L, fichiers, auteur, maintenant) and False:'),
    "S19 places ignorées": ("ORDONNER_UN_PLANNING.py",
        '                if occupe >= L["cap"] or (i in S["lourd"] and occupe_lourd >= R["calculs_lourds_max"]):',
        "                if False:"),
    "S20 calcul lourd gardé sur la machine": ("ORDONNER_UN_PLANNING.py",
        "        if h > seuil_h and not prive:", "        if False:"),
    "S22 à blanc qui écrit": ("ORDONNER_UN_PLANNING.py",
        "    if appliquer:\n        fichiers = {", "    if True:\n        fichiers = {"),
    "S23 signe de vie jamais écrit": ("ORDONNER_UN_PLANNING.py",
        '        fichiers[f"vie/{auteur}.txt"] = signe_de_vie(L, auteur, maintenant)', "        pass"),
    "S24 chien de garde aveugle au futur": ("ORDONNER_UN_PLANNING.py",
        "        if age is None or age < 0 or age > seuil:", "        if age is None or age > seuil:"),
    "S25 chien de garde qui lit la tâche": ("ORDONNER_UN_PLANNING.py",
        '        age = C.age_du_signe(L["vie"].get("chat", ""), maintenant)',
        '        age = C.age_du_signe(L["vie"].get("tache", "") or L["vie"].get("chat", ""), maintenant)'),
    "S26 chien de garde qui crie quand tout est fini": ("ORDONNER_UN_PLANNING.py",
        "        if not reste:\n            return", "        if False:\n            return"),
    "S27 chien de garde muet quand il ne peut pas lire": ("ORDONNER_UN_PLANNING.py",
        '        return f"ALERTE CHIEN DE GARDE : l\'ordonnanceur ne peut pas lire l\'état ({type(e).__name__} {e})", 1',
        '        return "CHIEN DE GARDE : rien", 0'),
    "S28 dépendance inconnue ignorée": ("ORDONNER_UN_PLANNING.py",
        "    if inconnues:\n        raise", "    if False:\n        raise"),
    "S29 déclarée tenue sans preuve lancée": ("ORDONNER_UN_PLANNING.py",
        '        elif declare[i] == "tenu":', '        elif False:'),
    "S30 chien de garde qui ne compte pas les bloquées": ("ORDONNER_UN_PLANNING.py",
        '        reste = [i for i in L["ids"] if etat[i] != "tenue"]',
        '        reste = [i for i in L["ids"] if etat[i] in ("en_cours", "tombee", "prete")]'),
    "S31 question humaine sans recherche préalable": ("ORDONNER_UN_PLANNING.py",
        "d'abord python3 programmes/AVANT_DE_DEMANDER.py {shlex.quote(livre[i])} ", "d'abord "),
    "S32 synonymes retirés": ("AVANT_DE_DEMANDER.py",
        '("droit", "interdi", "permis")', '("droit",)'),
    "S33 idées cherchées dans toute la ligne": ("AVANT_DE_DEMANDER.py",
        r'    return max((compter(s, groupes) for s in re.split(r"[.;!?]\s|«|»|\||\n", t)), default=0), compter(t, groupes)',
        "    return compter(t, groupes), compter(t, groupes)"),
    "S34 lecture impossible rendue muette": ("AVANT_DE_DEMANDER.py",
        '            print(f"ARRET lecture impossible de {fichier} : {e}")\n            return 2',
        '            print(f"ARRET lecture impossible de {fichier} : {e}")\n            continue'),
    "S35 plafond trop court": ("AVANT_DE_DEMANDER.py",
        '(("BACKLOG_DECISIONS.md", "ligne", 15, True)', '(("BACKLOG_DECISIONS.md", "ligne", 5, True)'),
    "S36 BLOQUÉE muette (B1, le continue d'avant)": ("ORDONNER_UN_PLANNING.py",
        '            sorties.append(f"BLOQUÉE {i} : {S[\'raison\'][i]}")\n            code = 1', "            pass"),
    "S37 fin sans BLOQUÉ (B1, AUCUN REVEIL d'avant)": ("ORDONNER_UN_PLANNING.py",
        "    elif decisions:", "    elif True:"),
    "S38 étape sans jalon non bloquée": ("ORDONNER_UN_PLANNING.py",
        '        elif i not in L["jalons"]:', "        elif False:"),
    "S39 en cours déclaré non importé (B2)": ("ORDONNER_UN_PLANNING.py",
        '        elif L["base"] is None and declare[i] in R["etats_actifs"]:', "        elif False:"),
    "S40 en cours déclaré importé à chaque passage": ("ORDONNER_UN_PLANNING.py",
        '        elif L["base"] is None and declare[i] in R["etats_actifs"]:',
        '        elif declare[i] in R["etats_actifs"]:'),
    "S41 exécutant github retombé sur le Chat (M4)": ("ORDONNER_UN_PLANNING.py",
        '        elif ex[i] not in ("chat", "humain"):', "        elif False:"),
    "S42 X1 toute poussée échouée lue comme OCCUPÉ (M1)": ("ORDONNER_UN_PLANNING.py",
        '        if c == 0 and (tete.split() or [None])[0] != L["base"]:', "        if True:"),
    "S43 X2 prise sans limite acceptée (m3)": ("ORDONNER_UN_PLANNING.py",
        '    if C.heure(d.get("limite", "")) is None or', '    if False and C.heure(d.get("limite", "")) is None or'),
    "S44 chien de garde hors de son try (m3)": ("ORDONNER_UN_PLANNING.py",
        '    try:\n        L = lire_tout(dossier, maintenant)\n        etat = situation(L, maintenant)["etat"]',
        '    L = lire_tout(dossier, maintenant)\n    etat = situation(L, maintenant)["etat"]\n    try:'),
    "S45 contrôle sur les états déclarés malgré la branche d'état (M3)": ("CONTROLER_UN_PLANNING.py",
        "        if vue:\n            pretes, en_cours", "        if False:\n            pretes, en_cours"),
    "S46 carte du dépôt à sept colonnes (B4)": ("../etudes/CARTE_DES_PANNES_DU_PROJET.csv",
        " (LU : 30 h) — la réponse rapide", " (LU : 30 h) ; la réponse rapide"),
    "S47 C14 sur les états déclarés (M5)": ("CONTROLER_UN_PLANNING.py",
        '    reste = [i for i in vue["etat"] if vue["etat"][i] != "tenue"] if vue else []',
        '    reste = [e["etape"] for e in etapes if e["etat"] != "tenu"]'),
    "S48 situation illisible rabattue en signal (M5)": ("CONTROLER_UN_PLANNING.py",
        '        refus.append(f"ERREUR ÉTAT ILLISIBLE', '        signaux.append(f"ERREUR ÉTAT ILLISIBLE'),
    "S49 situation seulement avec la branche d'état (M5)": ("CONTROLER_UN_PLANNING.py",
        '        vue, ligne_sv = O.situation(Lo, maintenant), Lo["vie"].get("chat")',
        '        vue, ligne_sv = O.situation(Lo, maintenant) if Lo["base"] else None, Lo["vie"].get("chat")'),
    "S50 « prête » des états déclarés si la situation manque (M5)": ("CONTROLER_UN_PLANNING.py",
        "            pretes = []", '            pretes = etapes_pretes(ids, deps, etat, R["etats_qui_liberent"])'),
    # S51 ne mord QUE si les épreuves tournent sous la version certifiée (3.11) : sous 3.12 et plus, la ligne compile.
    # C'est la preuve que la relance de main a lieu (superviseur R-759 du 25-11-2026).
    "S51 f-string à guillemets imbriqués, Python 3.12 seulement (B6)": ("ORDONNER_UN_PLANNING.py",
        'raise C.Impossible(f"git ls-remote origin a échoué ({motif})")',
        'raise C.Impossible(f"git ls-remote origin a échoué ({" ".join(err.split())[:120]})")'),
    "S52 tout bogue rabattu en état illisible (m12)": ("CONTROLER_UN_PLANNING.py",
        "    except (Impossible, O.C.Impossible, OSError, UnicodeError, csv.Error) as e:", "    except Exception as e:"),
    "S53 ligne courte lue en silence (m9)": ("CONTROLER_UN_PLANNING.py",
        "                if None in brut.values():\n", "                if False:\n"),
    "S54 guillemet non fermé lu en silence (m9)": ("CONTROLER_UN_PLANNING.py",
        '                if any(v is not None and ("\\n" in v or "\\r" in v) for v in brut.values()):\n',
        "                if False:\n"),
    "S55 échéance mal tapée remontée en erreur du programme (n1)": ("TENIR_UN_PLANNING.py",
        "    except ValueError:   # une DONNÉE mal tapée", "    except ZeroDivisionError:   # une DONNÉE mal tapée"),
    "S56 délais sans borne de calendrier (n1, OverflowError)": ("CONTROLER_UN_PLANNING.py",
        "        if somme_h + attente_h > heures_jusqu_a_la_fin_du_calendrier(maintenant):",
        "        if False:"),
    "S57 jalons invalides en code 2 au lieu d'un refus (superviseur 14h19)": ("CONTROLER_UN_PLANNING.py",
        '        refus.append("JALONS INVALIDES POUR LE VEILLEUR : " + " | ".join(arrets))',
        '        raise Impossible("JALONS INVALIDES POUR LE VEILLEUR : " + " | ".join(arrets))'),
    "S58 numéro d'enregistrement au lieu de ligne (n2)": ("CONTROLER_UN_PLANNING.py",
        "                n = lecteur.line_num\n", "                n = len(lignes) + 2\n"),
}


def passer(prog, t, dire):
    """Passe toutes les épreuves sur le jeu `prog` ; rend le nombre d'échecs. Avec `dire`, le nombre d'épreuves
    JOUÉES est écrit à la fin (superviseur R-759 du 25-11-2026 : aucune sautée en silence)."""
    j = Jeu(prog, t)
    echecs = joues = 0
    for f in EPREUVES:
        joues += 1
        try:
            f(j)
            if dire:
                print(f"OK {f.__name__}", flush=True)
        except Exception as e:
            echecs += 1
            if dire:
                print(f"ÉCHEC {f.__name__} : {type(e).__name__} {str(e)[:400]}", flush=True)
    if dire:
        print(f"ÉPREUVES JOUÉES : {joues} sur {len(EPREUVES)}, dont {echecs} en échec", flush=True)
    return echecs


MARQUE_DE_RELANCE = "EPREUVES_DU_TUNNEL_RELANCE"


def version_certifiee():
    """Rend la version de Python certifiée (« 3.11 ») lue à sa seule écriture, ou le cas réel qui l'empêche.

    ① RÔLE — Lire VERSION_DE_PYTHON sans la recopier (R-708 : deux écritures d'une même chose divergent toujours).
    ② CONTEXTE D APPEL — Par sous_la_version_certifiee, une fois.
    ③ ENTRÉE — Le texte de programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py de l'arbre éprouvé.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : (« X.Y », None), ou (None, le cas réel : fichier illisible, « absente », « écrite N
      fois (lignes …) », ou « affectée mais pas sous la forme … » avec les lignes d'affectation lues).
      [rend: 2]
    ⑥ TRAITEMENT — motif de ligne entière `VERSION_DE_PYTHON = "X.Y"` ; exactement une occurrence exigée ; sinon les
      lignes qui contiennent le nom disent le cas (n3 de la relecture a1e52c568 : « absente ou écrite plusieurs fois »
      égarait pour une ligne unique suivie d'un commentaire ; superviseur R-759 du 25-11-2026 : dire le cas réel).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — A-874 (Jean-Luc, 17-11-2026 07h48, « 1 ») : la version des circuits est fixée, écrite là seulement ;
      superviseur R-759 du 25-11-2026 : zéro ou plusieurs occurrences → ARRET, jamais un second lecteur silencieux.
    ⑨ CE QUI CLOCHE — Lecture du TEXTE, pas de l'objet Python : une écriture calculée (« VERSION = A + B ») ne serait
      pas vue — elle rend None, donc ARRET, jamais une fausse version.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    try:
        texte = open(os.path.join(PROG, "FABRIQUER_LE_CIRCUIT_PUBLIC.py"), encoding="utf-8").read()
    except OSError as e:
        return None, f"illisible : {e}"
    v = re.findall(r'^VERSION_DE_PYTHON = "(\d+\.\d+)"$', texte, re.M)
    if len(v) == 1:
        return v[0], None
    # les AFFECTATIONS du nom (ses usages, nombreux dans le fabricant, ne disent rien du cas)
    lignes = [(n, l.strip()) for n, l in enumerate(texte.splitlines(), 1) if re.match(r"\s*VERSION_DE_PYTHON\s*=[^=]", l)]
    if len(v) > 1:
        exactes = [str(n) for n, l in lignes if re.fullmatch(r'VERSION_DE_PYTHON = "[0-9]+[.][0-9]+"', l)]
        return None, f"écrite {len(v)} fois (lignes {', '.join(exactes)})"   # hors f-string : 3.11 (B6)
    if not lignes:
        return None, "absente"
    return None, ("affectée mais pas sous la forme VERSION_DE_PYTHON = \"X.Y\" seule sur sa ligne — "
                  + " | ".join(f"ligne {n} : {l}" for n, l in lignes)[:300])


def sous_la_version_certifiee():
    """Vérifie que ce processus tourne sous la version certifiée ; sinon se relance sous python<version>.

    ① RÔLE — Que TOUT ce que les épreuves exécutent (modules importés, ordonnanceur lancé par sys.executable) tourne
      sous la version certifiée, sur la machine du Chat comme sur GitHub.
    ② CONTEXTE D APPEL — Par main, avant toute épreuve.
    ③ ENTRÉE — sys.version_info ; la variable MARQUE_DE_RELANCE ; le PATH.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : None si la version est la bonne, sinon le motif d'ARRET ; ne revient pas quand il se
      relance (le processus est remplacé).
      [rend: 1]
    ⑥ TRAITEMENT — version_certifiee ; égale → None ; marque déjà posée → motif ; shutil.which("python" + version)
      absent → motif ; sinon marque posée et os.execv vers cet interpréteur, mêmes arguments.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — B6 de la relecture f2ce23138 : une f-string admise depuis la 3.12 seulement passait sous la 3.13 des
      machines du Chat et du relecteur, et toute la chaîne de l'ordonnanceur tombait sous la 3.11 de GitHub ;
      superviseur R-759 du 25-11-2026 : « le lanceur des épreuves s'exécute sous python<VERSION_DE_PYTHON> ».
    ⑨ CE QUI CLOCHE — Ce fichier d'épreuves seulement : les autres épreuves du dépôt tournent sous le Python de
      la machine (à consigner au BACKLOG). Sur GitHub, python3 est déjà la 3.11 : aucune relance.
    ⑩ EFFET — Pose la variable MARQUE_DE_RELANCE ; remplace le processus.
    ⑪ TERMINAISON — Une relance au plus (la marque l'empêche de boucler).
      [sort: oui]
    """
    v, cas = version_certifiee()
    if v is None:
        return f"VERSION_DE_PYTHON {cas} dans programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"
    if f"{sys.version_info[0]}.{sys.version_info[1]}" == v:
        return None
    if os.environ.get(MARQUE_DE_RELANCE):
        return f"relancé, mais sous Python {sys.version.split()[0]} au lieu de {v}"
    exe = shutil.which(f"python{v}")
    if exe is None:
        return f"Python {v} (version certifiée) introuvable : python{v} absent du PATH"
    os.environ[MARQUE_DE_RELANCE] = "1"
    sys.stdout.flush()
    os.execv(exe, [exe, "-B", os.path.abspath(__file__)] + sys.argv[1:])


def main():
    """Épreuves sur le vrai, puis chaque sabotage ; rend le code."""
    args = sys.argv[1:]
    for a in args:
        if a == "--sans-sabotage":
            continue
        if a.startswith("-") or not os.path.isdir(a) or not os.path.samefile(a, RACINE):
            print(f"ARRET argument refusé « {a} » : seuls <racine de ce fichier, {RACINE}> et --sans-sabotage")
            return 2
    motif = sous_la_version_certifiee()
    if motif:
        print(f"ARRET {motif} — aucune épreuve jouée (R-734)")
        return 2
    print(f"PYTHON {sys.version.split()[0]} {sys.executable}", flush=True)
    code = 0
    with tempfile.TemporaryDirectory() as t:
        rouges = passer(PROG, os.path.join(t, "vrai"), True)
        if rouges:
            code = 1
        if "--sans-sabotage" in args:
            return code
        if rouges:
            print(f"SABOTAGES NON JOUÉS : le vrai est rouge ({rouges} épreuve(s)) — un « MORD » n'y prouverait rien")
            print(f"ÉPREUVES : code {code}")
            return code
        for nom, (cible, a, b) in SABOTAGES.items():
            s = open(os.path.join(PROG, cible), encoding="utf-8").read()
            if s.count(a) != 1:
                print(f"SABOTAGE INAPPLICABLE {nom} : texte trouvé {s.count(a)} fois")
                return 2
            dm = os.path.join(t, "sab_" + nom.split()[0])
            os.makedirs(dm)
            for n in FICHIERS:
                shutil.copy(os.path.join(PROG, n), dm)
            # le nom seul : une cible hors de programmes/ (la carte du dépôt, S46) est copiée dans le jeu, jamais
            # réécrite à sa place
            open(os.path.join(dm, os.path.basename(cible)), "w", encoding="utf-8").write(s.replace(a, b))
            n = passer(dm, os.path.join(t, "w_" + nom.split()[0]), False)
            print(f"{'MORD' if n else 'NE MORD PAS'} {nom} ({n} épreuve(s) rouge(s))", flush=True)
            if not n:
                code = 1
    print("ÉPREUVES : " + ("TOUTES VERTES, TOUS LES SABOTAGES MORDENT" if code == 0 else f"code {code}"))
    return code


if __name__ == "__main__":
    sys.exit(main())
