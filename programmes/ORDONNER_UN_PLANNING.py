#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dit, à partir des PRISES et des PREUVES, quelles étapes d'un planning lancer maintenant, et prend ces étapes.

① RÔLE — Le cœur du TUNNEL de planification (A-898). À chaque entrée dans le
  tunnel (fin d'un traitement, réveil de 10 minutes, tâche planifiée horaire),
  ce programme relit le planning et UNE source d'état commune à toutes les
  sessions : la branche dédiée `etat-…` du dépôt (clé branche_d_etat de
  planning.csv), qui porte un fichier de PRISE par étape, prises/<ÉTAPE>.txt
  (qui, heure, limite = heure + délai maximal déclaré, chutes), et un signe de
  vie par auteur, vie/chat.txt et vie/tache.txt. L'état de chaque étape est
  tiré par UNE fonction, `situation`, que lisent aussi le chien de garde et le
  contrôle du planning. Il décide, écrit les prises nouvelles et les POUSSE
  lui-même ; si la poussée est refusée parce qu'un autre passage a écrit
  entre-temps, il ne lance rien. Puis il imprime les gestes à exécuter tels
  quels : LANCER, RELANCER, DÉCISION, BLOQUÉE, et la ligne de fin.
  Exemple réel : le 18-11-2026, la machine du Chat s'arrête à 08h17 ; une prise
  dont la limite passe sans preuve est TOMBÉE, et le passage suivant, de la
  conversation ou de la tâche horaire, dit RELANCER.

② CONTEXTE D APPEL — Par la consigne fixe (`consigne`, option --consigne) : le
  message de chaque réveil send_later du Chat, et la consigne de la tâche
  planifiée horaire (conçue, pas créée). À la main sans --appliquer pour voir
  sans rien écrire. Par tests/EPREUVES_DU_TUNNEL_DE_PLANIFICATION_Mer_18-11-2026.py.
  Par CONTROLER_UN_PLANNING.controler (lire_tout sans réseau, puis situation).

③ ENTRÉE — `<dossier du planning>` ; options : --appliquer (écrit et pousse les
  prises et le signe de vie ; sinon rien n'est écrit) ; --auteur=chat|tache
  (défaut chat : le nom du signe de vie et le « qui » des prises) ;
  --chien-de-garde ; --consigne ; --maintenant=AAAA-MM-JJTHH:MM (épreuves).
  Lit planning.csv (branche_d_etat obligatoire ; agents_simultanes_max ;
  racine_des_preuves et calculs facultatives), etapes.csv, le fichier de
  jalons, programmes/REGLAGES_DU_PLANNING.csv (etats_qui_liberent, etats_actifs,
  seuil_calcul_lourd_h, calculs_lourds_max, signe_de_vie_max_min).

④ CONDITIONS D ENTRÉE — Le dossier est dans un clone git dont « origin » se lit
  (et, avec --appliquer, s'écrit). Sinon ARRET et code 2, AVANT toute décision.

⑤ SORTIE — Des lignes : TENUE, EN COURS, EN ATTENTE DE JEAN-LUC, EN FILE,
  LANCER, RELANCER, BLOQUÉE, CALCUL LOURD SUR LA MACHINE, DÉCISION, puis UNE
  ligne de fin : REVEIL, AUCUN REVEIL ou BLOQUÉ. Codes : 0 rien d'anormal ·
  1 une DÉCISION attend, une étape est BLOQUÉE ou rien ne peut plus avancer ·
  2 rien n'a pu être conclu (fichier, git) : UNE ligne ARRET, aucune décision,
  aucune écriture (R-734) · 75 la poussée de l'état a été refusée parce qu'un
  autre passage a écrit entre-temps : rien n'est lancé. Avec --chien-de-garde :
  0 ou 1 (ALERTE).

⑥ TRAITEMENT — `lire_tout` (tout ce qui peut échouer, avant toute décision) ;
  `situation` (l'état de chaque étape, voir sa fiche) ; ordre par le chemin
  critique ; places ; `ecrire_et_pousser` ; lignes ; ligne de fin.

⑦ UNITÉ — Heures de Paris ; délais en heures ; minutes pour le signe de vie.

⑧ POURQUOI — Jean-Luc, 18-11-2026 : 12h31 « tout chaîner pour que dès qu'une
  action dépendante de l'autre finit, l'autre reprend » ; 12h49 « tout ce qui
  doit être, qui peut passer dans un programme, doit l'être » ; 12h51 « des
  conditions qui te font rentrer dans le tunnel d'un programme ». Superviseur
  R-759 du 18-11 après la relecture f3829629 : « ARRÊTER ET SIMPLIFIER » — une
  seule source d'« en cours », la prise ; puis, après la relecture bcf7756c
  (16h17) : une fonction unique `situation` et l'état BLOQUÉ, la voie GitHub
  retirée.

⑨ CE QUI CLOCHE — Exécuter les lignes reste à la parole : un LANCER non suivi
  se voit seulement quand sa limite passe (TOMBÉE), soit le délai maximal
  déclaré de l'étape, 12 à 30 h sur le planning du 17-11 ; la réponse rapide
  est le chien de garde (30 min), si la tâche horaire tourne. Le refus de
  poussée comme verrou est THÉORIQUE entre deux sessions réelles (éprouvé sur
  deux clones locaux). Une preuve dont le chemin absolu n'est pas sous
  racine_des_preuves est lue telle quelle, donc sur CETTE machine. L'état
  « ecrit » ne se prouve pas : avec etats_qui_liberent = ecrit|tenu,
  l'ordonnanceur ne libère que sur « tenu ». Les calculs lourds ne sont connus
  que déclarés (clé calculs) ; un calcul destiné à GitHub est BLOQUÉ tant que
  la voie GitHub n'existe pas (étape FILE). La branche d'état reçoit un commit
  par passage.

⑩ EFFET — Avec --appliquer : un commit sur la branche d'état (prises et
  vie/<auteur>.txt), poussé sans forcer. Rien dans la copie de travail ni
  l'index du clone.

⑪ TERMINAISON — Chaque appel git est borné à 120 s ; revient toujours.
"""
import datetime
import os
import re
import shlex
import subprocess
import sys
import tempfile
from zoneinfo import ZoneInfo

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
try:
    import CONTROLER_UN_PLANNING as C   # noqa: E402  (« prête », chemin critique, réglages, signe de vie : R-708)
    import TENIR_UN_PLANNING as T       # noqa: E402  (préparation et jugement des preuves : R-708)
except ImportError as _e:
    print(f"ARRET ordonnanceur impossible : {_e} (programmes/CONTROLER_UN_PLANNING.py et TENIR_UN_PLANNING.py à côté)")
    sys.exit(2)

P = ZoneInfo("Europe/Paris")
CHUTES_MAX = 3          # superviseur R-759 du 18-11-2026 : « arrêt après trois chutes »
REVEIL_MIN = 10         # 18-11-2026 12h51 : réveil send_later toutes les 10 minutes
OCCUPE = 75             # un autre passage a la main : rien n'est doublé
DELAI_S = 120


def git(racine, *args, entree=None, env=None):
    """Lance git dans le clone et rend (code, sortie, erreur).

    ① RÔLE — Le seul appel de git du programme.
    ② CONTEXTE D APPEL — Par lire_tout, ecrire_et_pousser, branche_courante, origine.
    ③ ENTRÉE — `racine` ; `args` : les arguments de git ; `entree` : texte sur l'entrée standard ; `env` : variables en plus.
    ④ CONDITIONS D ENTRÉE — git installé.
    ⑤ SORTIE — TROIS valeurs : code (127 git absent, 124 délai dépassé), sortie, erreur.
      [rend: 3]
    ⑥ TRAITEMENT — subprocess.run borné à DELAI_S.
    ⑦ UNITÉ — secondes.
    ⑧ POURQUOI — Un appel qui ne revient pas bloquerait le tunnel.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui de la commande.
    ⑪ TERMINAISON — Bornée par DELAI_S.
      [sort: non]
    """
    e = dict(os.environ, **(env or {}))
    try:
        p = subprocess.run(["git", *args], cwd=racine, input=entree, capture_output=True, text=True,
                           timeout=DELAI_S, env=e)
        return p.returncode, p.stdout, p.stderr
    except FileNotFoundError:
        return 127, "", "git absent"
    except subprocess.TimeoutExpired:
        return 124, "", "délai dépassé"


def git_exige(racine, *args, entree=None, env=None):
    """Lance git et rend sa sortie sans les blancs de bord ; un échec lève C.Impossible.

    ① RÔLE — Les appels git dont l'échec interdit de conclure (écriture de la branche d'état).
    ② CONTEXTE D APPEL — Par ecrire_et_pousser.
    ③ ENTRÉE — `racine` ; `args` : les arguments de git ; `entree` : texte sur l'entrée standard ; `env` : variables en plus.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la sortie ; code non nul → C.Impossible avec la commande et l'erreur.
      [rend: 1]
    ⑥ TRAITEMENT — git, puis contrôle du code.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734 : un passage qui n'a pas pu écrire l'état ne conclut rien (code 2).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui de la commande.
    ⑪ TERMINAISON — Bornée par git.
      [sort: non]
    """
    code, out, err = git(racine, *args, entree=entree, env=env)
    if code != 0:
        raise C.Impossible(f"git {args[0]} a échoué ({' '.join(err.split())[:160]})")
    return out.strip()


def lire_prise(texte):
    """Lit une prise (lignes « cle=valeur ») et rend son dictionnaire.

    ① RÔLE — La seule lecture d'une prise.
    ② CONTEXTE D APPEL — Par lire_tout.
    ③ ENTRÉE — `texte` : le contenu de prises/<ÉTAPE>.txt.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le dictionnaire ; une ligne sans « = » ou une limite illisible lève C.Impossible.
      [rend: 1]
    ⑥ TRAITEMENT — découpe au premier « = » ; limite lue par C.heure ; chutes en chiffres ASCII.
    ⑦ UNITÉ — heures de Paris.
    ⑧ POURQUOI — Une prise mal lue ferait relancer ou bloquer à tort : mieux vaut ne pas conclure (code 2).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Revient toujours ou lève.
      [sort: non]
    """
    d = {}
    for l in texte.splitlines():
        if not l.strip():
            continue
        if "=" not in l:
            raise C.Impossible(f"prise illisible : « {l} »")
        k, v = l.split("=", 1)
        d[k.strip()] = v.strip()
    # chiffres ASCII seulement : str.isdigit admet « ² », que int() refuse plus loin (superviseur R-759 du 25-11-2026)
    if C.heure(d.get("limite", "")) is None or not re.fullmatch(r"[0-9]+", d.get("chutes", "0")):
        raise C.Impossible(f"prise sans limite lisible ou chutes non entières : {d}")
    return d


def ecrire_prise(d):
    """Rend le texte d'une prise, clés dans un ordre fixe.

    ① RÔLE — La seule écriture d'une prise.
    ② CONTEXTE D APPEL — Par ordonner.
    ③ ENTRÉE — `d` : dictionnaire de la prise.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte.
      [rend: 1]
    ⑥ TRAITEMENT — etape, qui, heure, limite, chutes, tenue, decision, une ligne chacune si présente.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un ordre fixe rend les différences lisibles d'un commit à l'autre.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    return "".join(f"{k}={d[k]}\n" for k in ("etape", "qui", "heure", "limite", "chutes", "tenue", "decision")
                   if d.get(k) not in (None, ""))


def preuve_dans_le_clone(j, racine, prefixe, maintenant):
    """Dit si la preuve d'un jalon est tenue DANS CE CLONE.

    ① RÔLE — Rendre la preuve portable d'une session à l'autre (N2 de la relecture f3829629).
    ② CONTEXTE D APPEL — Par etats.
    ③ ENTRÉE — `j` : ligne de jalon préparée par T.preparer ; `racine` : le clone ; `prefixe` : clé
      racine_des_preuves (le début absolu des chemins écrits dans les jalons) ; `maintenant`.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : True si T.etat_de_la_preuve dit « tenu » sur le chemin rendu relatif au clone.
      [rend: 1]
    ⑥ TRAITEMENT — chemin sous `prefixe` → racine + reste ; sinon inchangé ; jugement par le veilleur (R-708).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les 47 preuves du planning du 17-11 commencent par /home/claude/cac-40-signals-sur-git-hub-pour-claude-/ :
      lues telles quelles, une tâche horaire en session neuve ne les voit pas, et une étape finie était relancée.
    ⑨ CE QUI CLOCHE — Un chemin absolu hors du préfixe reste lu sur cette machine.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    c = j["_chemin"]
    if prefixe and c.startswith(prefixe.rstrip("/") + "/"):
        c = os.path.join(racine, c[len(prefixe.rstrip("/")) + 1:])
    return T.etat_de_la_preuve(dict(j, _chemin=c), maintenant) == "tenu"


def lire_calculs(texte, seuil_h):
    """Lit la clé « calculs » de planning.csv : les calculs lourds déclarés, et où ils tournent.

    ① RÔLE — Appliquer A-900 : classer chaque calcul lourd déclaré — « github » au-delà du seuil, sinon « machine ».
    ② CONTEXTE D APPEL — Par lire_tout.
    ③ ENTRÉE — `texte` : « E3b:6|E5:4:PRIVÉ données privées absentes du dépôt public »
      (étape:heures machine déclarées[:PRIVÉ raison]) ; `seuil_h` : réglage seuil_calcul_lourd_h.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : {étape: « github » ou « machine »}, {étape: raison du maintien sur la machine} ;
      une entrée illisible lève C.Impossible.
      [rend: 2]
    ⑥ TRAITEMENT — découpe sur « | » puis « : » ; au-delà du seuil et non PRIVÉ → github ; sinon machine.
    ⑦ UNITÉ — heures machine.
    ⑧ POURQUOI — Jean-Luc, 18-11-2026 12h53 (A-900) : « 6, donc 2 plus 2 calculs lourds. Sauf si tu as le moyen
      […] de le faire passer par GitHub ».
    ⑨ CE QUI CLOCHE — La durée est déclarée, jamais mesurée ici ; un calcul non déclaré n'est pas compté. Le seuil
      est une PROPOSITION non décidée. La voie GitHub est retirée (superviseur R-759, 18-11-2026 16h17) : une étape
      classée « github » est BLOQUÉE par situation jusqu'à l'étape FILE ; garder cette syntaxe est à Jean-Luc.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Revient toujours ou lève.
      [sort: non]
    """
    ou, raisons = {}, {}
    for brut in [x.strip() for x in (texte or "").split("|") if x.strip()]:
        morceaux = brut.split(":", 2)
        h = C.nombre(morceaux[1]) if len(morceaux) > 1 else None
        if h is None or h < 0:
            raise C.Impossible(f"clé « calculs » : entrée illisible « {brut} » — attendu étape:heures[:PRIVÉ raison]")
        prive = len(morceaux) == 3 and morceaux[2].strip().upper().startswith("PRIVÉ")
        if len(morceaux) == 3 and not prive:
            raise C.Impossible(f"clé « calculs » : « {brut} » — troisième partie autre que « PRIVÉ raison »")
        e = morceaux[0].strip()
        if h > seuil_h and not prive:
            ou[e] = "github"
        else:
            ou[e] = "machine"
            raisons[e] = (morceaux[2].strip()[5:].strip(" :") or "sans raison écrite") if prive else \
                f"{h:g} h déclarées, sous le seuil de {seuil_h:g} h"
    return ou, raisons


def branche_courante(racine):
    """Rend la branche du clone, ou « <branche du planning> ».

    ① RÔLE — Écrire la consigne.
    ② CONTEXTE D APPEL — Par consigne.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nom.
      [rend: 1]
    ⑥ TRAITEMENT — git rev-parse --abbrev-ref HEAD.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le planning du 18-11 vit sur travail-planning-17, pas sur main.
    ⑨ CE QUI CLOCHE — Tête détachée → texte de remplacement.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Bornée par git.
      [sort: non]
    """
    code, out, _ = git(racine, "rev-parse", "--abbrev-ref", "HEAD")
    b = out.strip()
    return b if code == 0 and b and b != "HEAD" else "<branche du planning>"


def origine(racine):
    """Rend l'adresse du dépôt d'origine, sans identifiant ni jeton.

    ① RÔLE — Écrire la commande de clone de la tâche planifiée.
    ② CONTEXTE D APPEL — Par consigne.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : l'adresse, ou « <adresse du dépôt> ».
      [rend: 1]
    ⑥ TRAITEMENT — git remote get-url origin ; « utilisateur@ » retiré.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un jeton ne s'écrit jamais dans un texte qui voyage.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Bornée par git.
      [sort: non]
    """
    code, out, _ = git(racine, "remote", "get-url", "origin")
    return re.sub(r"//[^/@]*@", "//", out.strip()) if code == 0 and out.strip() else "<adresse du dépôt>"


def consigne(racine, dossier, pour="reveil"):
    """Rend LA consigne fixe du tunnel, pour le réveil du Chat ou pour la tâche planifiée horaire.

    ① RÔLE — Un seul texte d'entrée dans le tunnel (R-708) : la commande et la règle « exécuter les lignes telles
      quelles », jamais une liste écrite à la main.
    ② CONTEXTE D APPEL — Par ordonner (ligne REVEIL) et par main (--consigne).
    ③ ENTRÉE — `racine` ; `dossier` ; `pour` : « reveil » ou « tache ».
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte.
      [rend: 1]
    ⑥ TRAITEMENT — branche et chemin relatif du planning lus sur le clone.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — 18-11-2026 12h51 : le réveil porte « UNE commande fixe » ; A-905 (13h46) : l'alerte du chien de
      garde part par la notification de l'application Claude.
    ⑨ CE QUI CLOCHE — Le texte ne s'exécute pas seul : le Chat ou la tâche le suivent.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    b = branche_courante(racine)
    rel = os.path.relpath(os.path.abspath(dossier), racine)
    prog = f"python3 programmes/ORDONNER_UN_PLANNING.py {rel}"
    regle = (" ; code 75 : un autre passage a pris la main, rien à faire ; code 2 : le dire à Jean-Luc. Exécuter, "
             "telles quelles et dans ce tour, chaque ligne LANCER et RELANCER ; dire à Jean-Luc chaque ligne DÉCISION, "
             "BLOQUÉE et BLOQUÉ. Rien d'autre à écrire ni à pousser : l'ordonnanceur pousse lui-même l'état.")
    if pour == "tache":
        return (f"TUNNEL DE PLANIFICATION (tâche horaire, session neuve). D=$(mktemp -d) && git clone -q "
                f"{origine(racine)} \"$D\" && cd \"$D\" && git checkout -q {b} && {prog} --chien-de-garde ; s'il ne "
                "rend pas 0, le résultat de cette tâche COMMENCE par sa ligne « ALERTE CHIEN DE GARDE … », recopiée "
                f"telle quelle (elle déclenche la notification). Puis {prog} --appliquer --auteur=tache" + regle +
                " Ne pas reprogrammer de réveil : la tâche est horaire.")
    return (f"TUNNEL DE PLANIFICATION. cd {racine} && git checkout -q {b} && git pull -q --ff-only && "
            f"{prog} --appliquer --auteur=chat" + regle +
            " Puis programmer le réveil que dit la ligne REVEIL, ou aucun si la ligne de fin dit AUCUN REVEIL ou "
            "BLOQUÉ.")


def lire_tout(dossier, maintenant, reseau=True):
    """Lit TOUT ce dont le passage a besoin ; la moindre lecture impossible lève C.Impossible, avant toute décision.

    ① RÔLE — Garantir R-734 (N1 de la relecture f3829629) : un passage qui ne peut pas tout lire ne conclut rien.
    ② CONTEXTE D APPEL — Par ordonner et chien_de_garde (réseau) ; par CONTROLER_UN_PLANNING.controler (sans réseau).
    ③ ENTRÉE — `dossier` ; `maintenant` ; `reseau` : False = la branche d'état lue dans les références LOCALES du
      clone (refs/remotes/origin/<branche>), sans ls-remote ni fetch.
    ④ CONDITIONS D ENTRÉE — Voir la fiche du programme.
    ⑤ SORTIE — UNE valeur : un dictionnaire (racine, rel, réglages, tête, étapes, délais, jalons, prises, base de la
      branche d'état ou None, signes de vie, calculs).
      [rend: 1]
    ⑥ TRAITEMENT — réglages ; planning.csv, etapes.csv, jalons (préparés par T.preparer) ; dépendances connues et
      sans cycle ; avec réseau, `git ls-remote` puis `git fetch` de la branche d'état ; lecture des prises et des
      signes de vie dans l'objet de la référence.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le 18-11, en code 2, l'ancien passage relançait quand même ce qu'il ne voyait plus (N1). Le
      contrôle lit la même chose sans aller sur le réseau (superviseur R-759 du 18-11-2026, 16h17 : une seule
      lecture de l'état).
    ⑨ CE QUI CLOCHE — Sans réseau, l'état est aussi frais que le dernier fetch du clone.
    ⑩ EFFET — Avec réseau : git fetch (objets et référence distante de la seule branche d'état).
    ⑪ TERMINAISON — Bornée par git.
      [sort: non]
    """
    racine = C.racine_du_depot(dossier)
    if racine is None:
        raise C.Impossible(f"{dossier} n'est dans aucun clone git")
    R = C.lire_reglages(C.REGLAGES)
    tete = {l["cle"]: l["valeur"] for l in C.lire_table(os.path.join(dossier, "planning.csv"), ("cle", "valeur"))}
    etapes = C.lire_table(os.path.join(dossier, "etapes.csv"), C.COLONNES_ETAPES)
    f_j = C.chemin_de(tete, dossier, "jalons")
    if not f_j or not os.path.isfile(f_j):
        raise C.Impossible(f"jalons absents : {f_j or '(clé jalons)'}")
    jalons = {}
    for j in T.lire(f_j):
        motif = T.preparer(j)
        if motif:
            raise C.Impossible(f"jalons : {motif}")
        jalons[j["jalon"]] = j
    b = tete.get("branche_d_etat", "")
    if not re.fullmatch(r"etat-[A-Za-z0-9._-]+", b):
        raise C.Impossible("planning.csv : clé « branche_d_etat » absente ou hors forme etat-<nom>")
    cap = C.nombre(tete.get("agents_simultanes_max", ""))
    if cap is None or cap < 1:
        raise C.Impossible("planning.csv : agents_simultanes_max absent ou < 1")
    ou, raisons = lire_calculs(tete.get("calculs", ""), R["seuil_calcul_lourd_h"])
    ids = [e["etape"] for e in etapes]
    deps = {e["etape"]: [d.strip() for d in e["depend_de"].split(",") if d.strip()] for e in etapes}
    inconnues = sorted({d for i in deps for d in deps[i] if d not in ids})
    if inconnues:
        raise C.Impossible(f"etapes.csv : dépendance(s) inconnue(s) {', '.join(inconnues)}")
    if C.a_un_cycle(deps):
        raise C.Impossible("etapes.csv : dépendances en cycle")
    presente = True
    if reseau:
        code, out, err = git(racine, "ls-remote", "--heads", "origin", b)
        if code != 0:
            motif = " ".join(err.split())[:120]       # hors de la f-string : Python 3.11, la version certifiée (B6)
            raise C.Impossible(f"git ls-remote origin a échoué ({motif})")
        presente = bool(out.strip())
        code, _, err = git(racine, "fetch", "-q", "origin", f"+refs/heads/{b}:refs/remotes/origin/{b}") \
            if presente else (0, "", "")
        if code != 0:
            motif = " ".join(err.split())[:120]
            raise C.Impossible(f"git fetch de {b} a échoué ({motif})")
    code, sha, _ = git(racine, "rev-parse", "-q", "--verify", f"refs/remotes/origin/{b}")
    base = sha.strip() if presente and code == 0 else None
    if reseau and presente and base is None:
        raise C.Impossible(f"référence de {b} illisible après le fetch")
    prises, vie = {}, {}
    if base:
        code, noms, _ = git(racine, "ls-tree", "-r", "--name-only", base)
        if code != 0:
            raise C.Impossible(f"lecture de {b} impossible")
        for n in noms.split():
            code, texte, _ = git(racine, "show", f"{base}:{n}")
            if code != 0:
                raise C.Impossible(f"lecture de {b}:{n} impossible")
            if n.startswith("prises/") and n.endswith(".txt"):
                prises[n[7:-4]] = lire_prise(texte)
            elif n.startswith("vie/") and n.endswith(".txt"):
                vie[n[4:-4]] = texte.strip()
    return {"racine": racine, "rel": os.path.relpath(os.path.abspath(dossier), racine), "R": R, "tete": tete,
            "etapes": etapes, "jalons": jalons, "ids": ids, "deps": deps, "branche_etat": b, "base": base,
            "prises": prises, "vie": vie, "cap": int(cap), "ou": ou, "raisons": raisons,
            "delai": {e["etape"]: C.nombre(e["delai_h_max"]) or 0.0 for e in etapes}}


def situation(L, maintenant):
    """Rend l'état de chaque étape, tiré des prises et des preuves : LA règle d'état, lue par tous.

    ① RÔLE — La seule règle d'état (superviseur R-759, 18-11-2026 16h17 : l'état était calculé à trois endroits —
      ordonner, le chien de garde, le contrôle — « une fonction unique situation »).
    ② CONTEXTE D APPEL — Par ordonner, chien_de_garde et CONTROLER_UN_PLANNING.controler.
    ③ ENTRÉE — `L` : rendu de lire_tout ; `maintenant`.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire — etat {étape: tenue, en_cours, tombee, decision, prete, bloquee ou
      attend}, raison {étape bloquée: texte}, a_ecrire {étape: prise}, executant {étape: chat, humain ou github},
      lourd (étapes déclarées calcul lourd sur la machine), occupe et occupe_lourd (étapes en cours du Chat).
      [rend: 1]
    ⑥ TRAITEMENT — dans cet ordre : prise portant tenue= → tenue, jamais réévaluée ; preuve trouvée dans le clone
      → tenue, écrite dans la prise ; sans jalon → bloquee ; exécutant autre que chat ou humain → bloquee ; prise
      portant decision= → decision ; prise ouverte → en_cours si sa limite est à venir, tombee sinon ; branche d'état
      absente (premier passage) et étape déclarée active (réglage etats_actifs) → prise « déclaration », en_cours ;
      déclarée tenu → bloquee ; sinon prete (C.etapes_pretes, réglage etats_qui_liberent) ou attend.
    ⑦ UNITÉ — heures de Paris, comparées en temps universel.
    ⑧ POURQUOI — Relecture de bcf7756c : B1 (12 étapes sans jalon sautées en silence, « AUCUN REVEIL » et code 0
      avec 29 étapes sur 58 non faites), B2 (le travail déclaré en cours relancé au premier passage), M3 (deux
      définitions de « prête »).
    ⑨ CE QUI CLOCHE — Une prise écrite à la main passe pour vraie. Les dépendantes d'une étape bloquée restent
      « attend » : seule la ligne BLOQUÉ de fin le dit (pas de fermeture transitive, choix du superviseur). L'import
      des étapes déclarées actives n'a lieu qu'au premier passage : une étape déclarée active ensuite est prête.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    U, h = datetime.timezone.utc, f"{maintenant:%Y-%m-%d %H:%M}"
    R, pref = L["R"], L["tete"].get("racine_des_preuves", "")
    declare = {e["etape"]: e["etat"] for e in L["etapes"]}
    ex = {i: "humain" if i in L["jalons"] and L["jalons"][i]["_rdv"] else
          ("github" if L["ou"].get(i) == "github" else "chat") for i in L["ids"]}
    etat, raison, a_ecrire = {}, {}, {}
    for i in L["ids"]:
        p = L["prises"].get(i)
        if p and p.get("tenue"):
            etat[i] = "tenue"
        elif i in L["jalons"] and preuve_dans_le_clone(L["jalons"][i], L["racine"], pref, maintenant):
            etat[i] = "tenue"
            a_ecrire[i] = dict(p or {"etape": i, "qui": "ordonnanceur", "heure": h, "limite": h, "chutes": "0"}, tenue=h)
        elif i not in L["jalons"]:
            etat[i], raison[i] = "bloquee", "aucun jalon de ce nom : aucune preuve ne pourra la dire tenue"
        elif ex[i] not in ("chat", "humain"):
            etat[i], raison[i] = "bloquee", (f"exécutant « {ex[i]} » sans voie : la voie GitHub est retirée jusqu'à "
                                             "l'étape FILE (superviseur R-759) — à trancher par Jean-Luc")
        elif p and p.get("decision"):
            etat[i] = "decision"
        elif p:
            etat[i] = "en_cours" if C.heure(p["limite"]).astimezone(U) > maintenant.astimezone(U) else "tombee"
        elif L["base"] is None and declare[i] in R["etats_actifs"]:
            limite = maintenant + datetime.timedelta(hours=L["delai"][i])
            etat[i] = "en_cours"
            a_ecrire[i] = {"etape": i, "qui": "déclaration", "heure": h, "limite": f"{limite:%Y-%m-%d %H:%M}",
                           "chutes": "0"}
        elif declare[i] == "tenu":
            etat[i], raison[i] = "bloquee", "déclarée tenue dans etapes.csv, preuve absente : jamais lancée"
        else:
            etat[i] = "a_faire"
    libre = {"tenue": "tenu", "en_cours": "en_cours"}
    pretes = C.etapes_pretes(L["ids"], L["deps"], {i: libre.get(etat[i], etat[i]) for i in L["ids"]},
                             R["etats_qui_liberent"])
    for i in L["ids"]:
        if etat[i] == "a_faire":
            etat[i] = "prete" if i in pretes else "attend"
    lourd = {i for i in L["ids"] if L["ou"].get(i) == "machine"}
    cours = {i for i in L["ids"] if etat[i] == "en_cours" and ex[i] == "chat"}
    return {"etat": etat, "raison": raison, "a_ecrire": a_ecrire, "executant": ex, "lourd": lourd,
            "occupe": len(cours), "occupe_lourd": len(cours & lourd)}


def ecrire_et_pousser(L, fichiers, auteur, maintenant):
    """Écrit les fichiers donnés sur la branche d'état, en un commit, et le pousse sans forcer.

    ① RÔLE — Prendre les étapes : le refus de poussée fait office de verrou entre sessions.
    ② CONTEXTE D APPEL — Par ordonner, avec --appliquer, une fois par passage.
    ③ ENTRÉE — `L` (dont la base lue par lire_tout) ; `fichiers` : {chemin dans la branche: texte} ; `auteur` ;
      `maintenant`.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : « poussé », ou « refusé » si la tête distante a bougé depuis la base (un autre passage
      a écrit) ; tout autre échec lève C.Impossible (code 2).
      [rend: 1]
    ⑥ TRAITEMENT — index temporaire (GIT_INDEX_FILE) : read-tree de la base (ou vide), hash-object et update-index
      de chaque fichier, write-tree, commit-tree (parent = base), push <commit>:refs/heads/<branche> sans force ;
      après un refus, relecture de la tête distante par ls-remote : différente de la base → « refusé » ; égale ou
      illisible → C.Impossible.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur R-759 du 18-11 : « Si la poussée est refusée, un autre a pris l'étape : il ne lance
      rien. » M1 de la relecture bcf7756c : reconnu aux mots de l'erreur, un refus par crochet du dépôt (branche
      protégée) rendait « OCCUPÉ », code 75, pour toujours ; la propriété « la tête a bougé » ne dépend d'aucun mot.
    ⑨ CE QUI CLOCHE — Un refus pour un fichier sans rapport (l'autre auteur a écrit son signe de vie) fait aussi
      passer le tour.
    ⑩ EFFET — Objets git, un commit, une poussée.
    ⑪ TERMINAISON — Bornée par git.
      [sort: non]
    """
    r, b = L["racine"], L["branche_etat"]
    with tempfile.TemporaryDirectory() as t:
        env = {"GIT_INDEX_FILE": os.path.join(t, "index"), "GIT_AUTHOR_NAME": f"ordonnanceur ({auteur})",
               "GIT_AUTHOR_EMAIL": "ordonnanceur@localhost", "GIT_COMMITTER_NAME": f"ordonnanceur ({auteur})",
               "GIT_COMMITTER_EMAIL": "ordonnanceur@localhost"}
        git_exige(r, *(["read-tree", L["base"]] if L["base"] else ["read-tree", "--empty"]), env=env)
        for chemin, texte in sorted(fichiers.items()):
            sha = git_exige(r, "hash-object", "-w", "--stdin", entree=texte, env=env)
            git_exige(r, "update-index", "--add", "--cacheinfo", f"100644,{sha},{chemin}", env=env)
        commit = git_exige(r, "commit-tree", git_exige(r, "write-tree", env=env), "-m",
                           f"état du planning {L['rel']} — {maintenant:%Y-%m-%d %H:%M} ({auteur})",
                           *(["-p", L["base"]] if L["base"] else []), env=env)
        c, _, err = git(r, "push", "-q", "origin", f"{commit}:refs/heads/{b}")
        if c == 0:
            return "poussé"
        c, tete, _ = git(r, "ls-remote", "--heads", "origin", b)
        if c == 0 and (tete.split() or [None])[0] != L["base"]:
            return "refusé"
        raise C.Impossible(f"poussée de {b} refusée sans qu'un autre passage ait écrit ({' '.join(err.split())[:160]})")


def signe_de_vie(L, auteur, maintenant):
    """Rend le texte du signe de vie d'un auteur.

    ① RÔLE — Dire « le tunnel de cet auteur a tourné à telle heure » (A-904).
    ② CONTEXTE D APPEL — Par ordonner, avec --appliquer.
    ③ ENTRÉE — `L`, `auteur`, `maintenant`.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : « SIGNE DE VIE <AAAA-MM-JJTHH:MM:SS+HH:MM> · <planning> · <auteur> » et un saut de ligne.
      [rend: 1]
    ⑥ TRAITEMENT — heure ISO avec décalage, lisible par C.age_du_signe.
    ⑦ UNITÉ — heure de Paris.
    ⑧ POURQUOI — Un fichier par auteur : la conversation et la tâche n'écrivent jamais le même fichier (N3).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    return f"SIGNE DE VIE {maintenant.isoformat(timespec='seconds')} · {L['rel']} · {auteur}\n"


def ordonner(dossier, maintenant, appliquer, auteur="chat"):
    """Fait un passage complet du tunnel et rend (lignes, code).

    ① RÔLE — Toute la décision et l'écriture de l'état, sans affichage, pour être éprouvée.
    ② CONTEXTE D APPEL — Par main ; par les épreuves.
    ③ ENTRÉE — `dossier`, `maintenant`, `appliquer`, `auteur`.
    ④ CONDITIONS D ENTRÉE — Voir la fiche du programme.
    ⑤ SORTIE — DEUX valeurs : les lignes et le code (0, 1 ou 75 ; le code 2 passe par l'exception C.Impossible).
      [rend: 2]
    ⑥ TRAITEMENT — lire_tout ; situation ; ordre par le chemin critique ; par étape : tenue nouvelle → TENUE ;
      bloquee → BLOQUÉE et code 1 ; en_cours → EN COURS ; decision, ou tombee pour la CHUTES_MAX-ième fois →
      DÉCISION et code 1 ; tombee → RELANCER ; prete → LANCER ; places du Chat (agents_simultanes_max,
      calculs_lourds_max) sinon EN FILE ; poussée ; lignes des gestes ; ligne de fin : REVEIL s'il reste du travail
      en cours ou lancé, AUCUN REVEIL si tout est tenu ou si seules des DÉCISION attendent, sinon BLOQUÉ et code 1.
    ⑦ UNITÉ — heures.
    ⑧ POURQUOI — Voir la fiche du programme. B1 de la relecture bcf7756c : « AUCUN REVEIL » n'est plus permis tant
      qu'une étape n'est pas tenue (R-734).
    ⑨ CE QUI CLOCHE — Voir la fiche du programme. Une RELANCE ne revérifie pas les dépendances.
    ⑩ EFFET — Avec `appliquer` : la branche d'état.
    ⑪ TERMINAISON — Revient toujours ou lève C.Impossible.
      [sort: non]
    """
    L = lire_tout(dossier, maintenant)
    S = situation(L, maintenant)
    R, ids, etat, a_ecrire, ex = L["R"], L["ids"], S["etat"], S["a_ecrire"], S["executant"]
    livre = {e["etape"]: re.sub(r"\s+", " ", e["livre"])[:90] for e in L["etapes"]}
    _, res, _ = C.calculer_chemin({i: 0.0 if etat[i] == "tenue" else L["delai"][i] for i in ids}, L["deps"])
    occupe, occupe_lourd = S["occupe"], S["occupe_lourd"]
    sorties, gestes, decisions, attente, code = [], [], [], False, 0
    h = f"{maintenant:%Y-%m-%d %H:%M}"
    for i in sorted(ids, key=lambda i: (res[i][2], i)):
        e, p = etat[i], L["prises"].get(i)
        chutes = int(p["chutes"]) + 1 if e == "tombee" else 0
        if e == "tenue" and i in a_ecrire:
            sorties.append(f"TENUE {i} : preuve trouvée" + (", inscrite dans la prise" if appliquer else ""))
        elif e == "bloquee":
            sorties.append(f"BLOQUÉE {i} : {S['raison'][i]}")
            code = 1
        elif e == "en_cours":
            p = p or a_ecrire[i]
            quoi = "EN ATTENTE DE JEAN-LUC" if ex[i] == "humain" else "EN COURS"
            sorties.append(f"{quoi} {i} : pris par {p['qui']} à {p['heure']}, limite {p['limite']}")
            attente = True
        elif e == "decision" or chutes >= CHUTES_MAX:
            if chutes:
                a_ecrire[i] = dict(p, chutes=str(chutes), decision=f"tombée {chutes} fois, {h}")
            sorties.append(f"DÉCISION {i} : tombée {CHUTES_MAX} fois sans preuve — plus de relance ; dire à Jean-Luc "
                           f"la cause ; pour reprendre, retirer prises/{i}.txt de {L['branche_etat']}")
            decisions.append(i)
            code = 1
        elif e in ("tombee", "prete"):
            attente = True
            if ex[i] == "chat":
                if occupe >= L["cap"] or (i in S["lourd"] and occupe_lourd >= R["calculs_lourds_max"]):
                    sorties.append(f"EN FILE {i} : places pleines ({occupe}/{L['cap']} travaux du Chat"
                                   + (f", {occupe_lourd}/{R['calculs_lourds_max']:g} calculs lourds"
                                      if i in S["lourd"] else "") + ")")
                    continue
                occupe += 1
                occupe_lourd += 1 if i in S["lourd"] else 0
            limite = maintenant + datetime.timedelta(hours=L["delai"][i])
            a_ecrire[i] = {"etape": i, "qui": auteur, "heure": h, "limite": f"{limite:%Y-%m-%d %H:%M}",
                           "chutes": str(chutes)}
            gestes.append(("RELANCER" if chutes else "LANCER", i))
    if appliquer:
        fichiers = {f"prises/{i}.txt": ecrire_prise(p) for i, p in a_ecrire.items()}
        fichiers[f"vie/{auteur}.txt"] = signe_de_vie(L, auteur, maintenant)
        if ecrire_et_pousser(L, fichiers, auteur, maintenant) == "refusé":
            return [f"OCCUPÉ : la poussée de {L['branche_etat']} a été refusée — un autre passage a écrit "
                    "entre-temps ; rien n'est lancé"], OCCUPE
    pref = L["tete"].get("racine_des_preuves", "")
    for geste, i in gestes:
        preuve = L["jalons"][i]["_chemin"]
        if pref and preuve.startswith(pref.rstrip("/") + "/"):
            preuve = preuve[len(pref.rstrip("/")) + 1:]
        if ex[i] == "humain":
            sorties.append(f"{geste} {i} humain : d'abord python3 programmes/AVANT_DE_DEMANDER.py {shlex.quote(livre[i])} "
                           f"(A-819, A-906 : lire les décisions qui en parlent avant la question), puis le Chat pose à "
                           f"Jean-Luc ce qui reste ouvert de « {livre[i]} » — preuve attendue {preuve}")
            continue
        if i in L["raisons"]:
            sorties.append(f"CALCUL LOURD SUR LA MACHINE {i} : {L['raisons'][i]}")
        sorties.append(f"{geste} {i} chat : « {livre[i]} » — pris jusqu'à {a_ecrire[i]['limite']}, "
                       f"preuve attendue {preuve}")
    non_tenues = [i for i in ids if etat[i] != "tenue"]
    if attente:
        sorties.append(f"REVEIL send_later dans {REVEIL_MIN} min, message : {consigne(L['racine'], dossier)}")
    elif not non_tenues:
        sorties.append("AUCUN REVEIL : toutes les étapes sont tenues")
    elif decisions:
        sorties.append("AUCUN REVEIL : rien en cours ni prêt — la suite attend les DÉCISION ci-dessus")
    else:
        sorties.append(f"BLOQUÉ : {len(non_tenues)} étape(s) non tenue(s), rien ne peut avancer "
                       f"({', '.join(non_tenues)}) — dire à Jean-Luc")
        code = 1
    return sorties, code


def chien_de_garde(dossier, maintenant):
    """Dit si le tunnel de la CONVERSATION vit ; sinon, la ligne d'alerte — seulement s'il reste une étape non tenue.

    ① RÔLE — Le chien de garde (A-626, A-904, A-905) : le seul témoin d'une conversation arrêtée.
    ② CONTEXTE D APPEL — Par main (--chien-de-garde), en PREMIER geste de la tâche planifiée horaire.
    ③ ENTRÉE — `dossier` ; `maintenant`.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : la ligne à afficher et le code (0 rien à signaler · 1 ALERTE).
      [rend: 2]
    ⑥ TRAITEMENT — TOUT dans un même try : lire_tout ; situation (la même que celle d'ordonner) ; vie/chat.txt lu
      par C.age_du_signe ; ALERTE si une étape n'est pas tenue et que le signe est absent, illisible, daté dans le
      futur ou plus vieux que signe_de_vie_max_min ; toute exception = ALERTE.
    ⑦ UNITÉ — minutes.
    ⑧ POURQUOI — A-904 et A-905 (Jean-Luc, 18-11-2026 13h46 : « Par notification, ici sur la messagerie »). Ne lire
      que vie/chat.txt évite que la tâche horaire se rassure elle-même. Une étape bloquée compte (B1 de la relecture
      bcf7756c : le chien, muet, ne comptait que l'en cours et le prêt) ; m3 : une prise abîmée faisait planter le
      chien hors de son try.
    ⑨ CE QUI CLOCHE — THÉORIQUE : qu'un résultat commençant par l'alerte déclenche la notification n'a jamais été
      essayé ; si la tâche horaire ne tourne pas, rien n'alerte. Une conversation vivante dont toutes les étapes
      restantes sont bloquées ne fait pas alerter le chien : c'est la ligne BLOQUÉ d'ordonner qui le dit.
    ⑩ EFFET — git fetch de la branche d'état.
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    try:
        L = lire_tout(dossier, maintenant)
        etat = situation(L, maintenant)["etat"]
        reste = [i for i in L["ids"] if etat[i] != "tenue"]
        if not reste:
            return "CHIEN DE GARDE : toutes les étapes sont tenues — rien à surveiller", 0
        age = C.age_du_signe(L["vie"].get("chat", ""), maintenant)
        seuil = L["R"]["signe_de_vie_max_min"]
        if age is None or age < 0 or age > seuil:
            quoi = "absent ou illisible" if age is None else ("daté dans le futur" if age < 0 else f"vieux de {age:.0f} min")
            return (f"ALERTE CHIEN DE GARDE : signe de vie de la conversation {quoi} (plus de {seuil:g} min admis) alors "
                    f"que {len(reste)} étape(s) ne sont pas tenues ({', '.join(reste[:6])}) — la conversation ou la "
                    "machine du Chat est sans doute arrêtée"), 1
        return f"CHIEN DE GARDE : la conversation vit — signe de vie il y a {age:.0f} min", 0
    except Exception as e:   # R-734 : ne pas pouvoir conclure est une alerte, jamais un silence
        return f"ALERTE CHIEN DE GARDE : l'ordonnanceur ne peut pas lire l'état ({type(e).__name__} {e})", 1


def main(argv):
    """Lit la ligne de commande, fait un passage, affiche, rend le code.

    ① RÔLE — L'entrée du tunnel.
    ② CONTEXTE D APPEL — `python3 programmes/ORDONNER_UN_PLANNING.py <dossier> [--appliquer] [--auteur=chat|tache]
      [--maintenant=AAAA-MM-JJTHH:MM] [--consigne] [--chien-de-garde]`.
    ③ ENTRÉE — `argv` sans le nom du programme.
    ④ CONDITIONS D ENTRÉE — Un dossier.
    ⑤ SORTIE — UNE valeur : le code (voir la fiche du programme).
      [rend: 1]
    ⑥ TRAITEMENT — options ; --chien-de-garde → chien_de_garde ; --consigne → les deux consignes ; sinon ordonner ;
      toute exception → UNE ligne ARRET et 2, aucune autre ligne (R-734).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un passage qui n'a pas pu conclure ne rend jamais 0 et ne dit aucun geste (N1).
    ⑨ CE QUI CLOCHE — --maintenant n'est pas réservé aux épreuves.
    ⑩ EFFET — Affiche ; ceux d'ordonner.
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    pos = [a for a in argv if not a.startswith("--")]
    opt = [a for a in argv if a.startswith("--")]
    maintenant, appliquer, mode, auteur = datetime.datetime.now(P), False, "ordonner", "chat"
    for o in opt:
        if o == "--appliquer":
            appliquer = True
        elif o in ("--chien-de-garde", "--consigne"):
            mode = o[2:]
        elif o.startswith("--auteur=") and o[9:] in ("chat", "tache"):
            auteur = o[9:]
        elif o.startswith("--maintenant="):
            maintenant = C.heure(o.split("=", 1)[1].replace("T", " "))
            if maintenant is None:
                print("ARRET --maintenant hors format AAAA-MM-JJTHH:MM")
                return 2
        else:
            print(f"ARRET option inconnue : {o}")
            return 2
    if len(pos) != 1:
        print("ARRET usage : ORDONNER_UN_PLANNING.py <dossier du planning> [--appliquer] [--consigne] [--chien-de-garde]")
        return 2
    if mode == "chien-de-garde":
        ligne, code = chien_de_garde(pos[0], maintenant)
        print(ligne)
        return code
    try:
        if mode == "consigne":
            racine = C.racine_du_depot(pos[0])
            if racine is None:
                raise C.Impossible(f"{pos[0]} n'est dans aucun clone git")
            print("CONSIGNE DU RÉVEIL : " + consigne(racine, pos[0], "reveil"))
            print("CONSIGNE DE LA TÂCHE HORAIRE : " + consigne(racine, pos[0], "tache"))
            return 0
        lignes, code = ordonner(pos[0], maintenant, appliquer, auteur)
    except Exception as e:   # C.Impossible ou imprévue : R-734, une seule ligne, rien d'autre
        print(f"ARRET ordonnanceur impossible : {type(e).__name__} {e}")
        return 2
    print(f"ORDONNANCEUR {os.path.abspath(pos[0])} — {maintenant:%Y-%m-%d %H:%M} (Paris)"
          + ("" if appliquer else " — à blanc, rien d'écrit"))
    for l in lignes:
        print(l)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
