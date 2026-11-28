#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DECOUPER_LA_MOULINETTE.py — Ven 27-11-2026 (Paris). EN ESSAI · outil. Simulation uniquement : aucun ordre réel.

LE SENS EN TÊTE. L'étape ② de la moulinette (JOUER, A-541) se découpe en tranches (`JOUER_LES_VERSIONS.tranche`, la
seule découpe, R-708) ; A-965 (Jean-Luc, 21-11-2026 à 14h43, réponse « 1 ») veut ces tranches réparties sur les
machines de GitHub. Ce programme porte les deux BOUTS de ce trajet, et la mesure qui le dimensionne ; il ne transporte
rien lui-même (le transport est le circuit de GitHub) et ne calcule aucun résultat (il appelle l'enchaîneur
programmes/ENCHAINER_LA_MOULINETTE.py, qui appelle JOUER) :
  ① CHRONOMÉTRER : jouer la fiche d'essai ESSAI-C5-2000-2026 (A-853, A-861, A-863) sur les 20 ans, chaque ligne de sa
    sortie datée en secondes depuis le départ, puis le coût de chaque phase (lecture des cours, calibrage, un jeu).
  ② PLANIFIER : à partir de CETTE mesure (lue dans la sortie du chronométrage, jamais tapée, R-728), dire en combien de
    tranches découper une fiche de V versions, combien de vagues sur P places, combien d'exécutions, et le temps.
  ③ TRANCHE (le bout « machine ») : dans une copie sans .git, faire ⓪ preparer, ① decliner et ② « jouer k N » par
    l'enchaîneur, puis écrire sur la sortie UN bloc qui porte la tranche jouée, son empreinte et les témoins du journal.
  ④ RASSEMBLER (le bout « centre ») : recevoir les blocs de plusieurs machines dans la chaîne locale, en refusant tout
    bloc qui n'est pas de CETTE chaîne (mêmes cours, mêmes réglages validés, même combinatoire, même découpage),
    écrire chaque tranche et son témoin « 2-tranche-k », et dire les tranches qui manquent (la REPRISE). L'assemblage
    reste celui de l'enchaîneur (« assembler »), qui refuse une tranche jouée sur d'autres cours (propriété de L1).

USAGE
    python3 -B programmes/DECOUPER_LA_MOULINETTE.py chronometrer <copie>
    python3 -B programmes/DECOUPER_LA_MOULINETTE.py planifier <sortie_du_chronometrage> <versions> <budget_s> <places>
        <surcout_s>
    python3 -B programmes/DECOUPER_LA_MOULINETTE.py tranche <copie> <STRATÉGIE> <ESSAI> <k> <N> [--cours-du-maitre]
    python3 -B programmes/DECOUPER_LA_MOULINETTE.py rassembler <racine> <STRATÉGIE> <ESSAI> <N> <sortie> [<sortie> …]
    python3 -B programmes/DECOUPER_LA_MOULINETTE.py tranche-essai <copie> <k> <N>
    python3 -B programmes/DECOUPER_LA_MOULINETTE.py preparer-essai <racine> <N>

① RÔLE — Mesurer le coût d'une tranche, dimensionner le découpage, jouer une tranche sur une machine, et recevoir
  les tranches au centre avec reprise de celles qui manquent.
② CONTEXTE D'APPEL — À la main, par le Chat. « chronometrer » : aussi comme épreuve longue sur GitHub (code
  ChronoEssai de tests/LANCEMENT_DES_EPREUVES.json). « tranche » : sur une machine (aujourd'hui, à la main ou par une
  épreuve ; le circuit de la moulinette n'existe pas, voir ⑨). Aucune tâche automatique.
③ ENTRÉE — Voir USAGE. `<copie>`, `<racine>` : une COPIE du dépôt sans .git (A-861). `<sortie>` : un fichier texte
  (par exemple SORTIE.txt rapatrié d'une épreuve longue) qui porte un ou plusieurs blocs de tranche.
④ CONDITIONS D'ENTRÉE — Voir chaque fonction. Pour « tranche » et « rassembler » : les réglages validés
  (donnees/combinatoires/VARIABLES_DE_DECLINAISON_<S>_<E>.csv, mention de Jean-Luc) sont les MÊMES octets sur la
  machine et au centre.
⑤ SORTIE — UNE valeur, le code : 0 fait · 1 refus (bloc étranger, tranche déjà reçue autrement, étape en échec) ·
  2 un contrôle n'a pas pu tourner, usage faux (R-734) · 3 « rassembler » : tout ce qui est reçu est bon, mais des
  tranches manquent (leur liste est écrite : « À REJOUER »).
⑥ TRAITEMENT — Voir `main` et chaque mode.
⑦ UNITÉ — Secondes ; versions ; tranches ; places (machines de GitHub en même temps).
⑧ POURQUOI — Mesure de L1 (27-11-2026, machine du Chat) : une tranche d'une version sur 20 ans prend 75 s, dont
  lecture 26 s et calibrage 40 s, payés à CHAQUE tranche ; sous le délai de 580 s de l'enchaîneur, 60 à 80 versions
  par tranche ; IND-001-RETEST compte environ 21 000 versions (A-1076). La lecture et le calibrage ne se partagent
  PAS entre machines proprement (il faudrait transporter les cours lus, hors du lecteur unique A-577) : ils se paient
  une fois PAR TRANCHE, et la seule façon propre de les payer moins souvent est d'avoir MOINS de tranches, plus
  grosses — ce que dit le mode « planifier », pour chaque budget de tranche.
⑨ CE QUI CLOCHE — ① LE TRANSPORT N'EXISTE PAS : le circuit des épreuves longues (epreuves_longues.yml) ne joue qu'un
  CODE de sa table, aux arguments FIGÉS, au plus 64 codes (EPREUVES_AU_PLUS du fabricant, 61 pris le 27-11-2026), et
  ne rapporte que SORTIE.txt et RESULTAT.json : un bloc de tranche voyage dans SORTIE.txt, mais une tranche par code
  ne tient pas pour 21 000 versions. Le circuit propre (« circuit=moulinette » au relais, matrice des k) est une
  extension du fabricant, proposée, non écrite. ② « chronometrer » repère les phases par des TEXTES recopiés de
  JOUER_LES_VERSIONS.main (MARQUES) : si l'un change là-bas, le chronométrage rend 2 (« marque absente »), jamais un
  faux chiffre. ③ La fiche d'essai n'a qu'UNE version (A-863 : l'essai sans regard refuse plus d'une version et refuse
  « --tranche= ») : le coût par version est celui d'UN jeu de la fiche, mesuré sur C5 (6 valeurs) ; le coût d'une
  version d'une autre famille (IND, 1 ou 39 valeurs) n'est pas mesuré. ④ « rassembler » ne compare pas le témoin
  « 0-proposition » (la proposition de ⓪ peut porter l'heure de sa fabrication) : la combinatoire de ①, qui en
  découle, est comparée. ⑤ Le bloc porte la tranche en texte dans la sortie de la machine : une tranche de plusieurs
  mégaoctets alourdit SORTIE.txt d'autant.
⑩ EFFET — « chronometrer » : comme PREPARER_LA_MOULINETTE_D_ESSAI --jouer (la copie). « tranche » : sous
  <copie>/CHAINE_<S>_<E>/ (l'enchaîneur). « rassembler » : e2/tranche_<k>.csv et des lignes du journal de la chaîne
  locale. « planifier » : aucun.
⑪ TERMINAISON — Sort par sys.exit. Les programmes lancés sont bornés (voir chaque fonction).
[sort: oui]
"""
import csv
import hashlib
import io
import json
import math
import os
import re
import subprocess
import sys
import threading
import time

sys.dont_write_bytecode = True
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import ENCHAINER_LA_MOULINETTE as E  # noqa: E402  les étapes, leurs témoins et leurs exigences vivent là (R-708)
import VERIFIER_LA_CHAINE as V  # noqa: E402  le journal et la garde vivent là (R-708)
import PREPARER_LA_MOULINETTE_D_ESSAI as P  # noqa: E402  la fiche d'essai et sa commande vivent là (R-708)

ESSAI_PROGRAMME = os.path.join("programmes", "PREPARER_LA_MOULINETTE_D_ESSAI.py")
# LES MARQUES DE PHASE : textes écrits par JOUER_LES_VERSIONS.main (et, pour la fin, par PREPARER_LA_MOULINETTE_D_ESSAI),
# dans l'ordre où ils sortent. Recopiés (⑨ ②) : un texte changé là-bas fait rendre 2 au chronométrage. Une ligne de
# l'essai déclaré porte en tête la marque d'essai du juge (« ESSAI — NI RÉSULTAT NI SÉLECTION · ») : une marque compte
# en tête de ligne ou juste après « · » (`porte_la_marque`).
MARQUES = (("contrat", "CONTRAT DE STRATÉGIE"), ("cours_lus", "COURS LUS"),
           ("calibrage", "CALIBRAGE PAR LE JUGE SEUL"), ("fiche_jouee", "  ce programme :"),
           ("identique", "  version identique"), ("reglage", "PARTIE DE RÉGLAGE"),
           ("fin", "CODE DE LA MOULINETTE"))
DEBUT_DU_BLOC, FIN_DU_BLOC = "=== BLOC DE TRANCHE (DECOUPER_LA_MOULINETTE) ===", "=== FIN DU BLOC DE TRANCHE ==="
# Les témoins de la chaîne qu'une machine et le centre doivent porter À L'IDENTIQUE (⑨ ④ : pas « 0-proposition »).
TEMOINS_COMPARES = (E.TEMOIN_DES_COURS, "0-variables-validees", E.FAITE["decliner"])
DELAI_DU_CHRONOMETRAGE = 1800   # secondes : 75 s mesurées par L1 sur la machine du Chat ; borne large, sous 30 min
TEMOIN_DE_TRANCHE = "2-tranche-%d"   # la forme que l'enchaîneur écrit (`faire`, étape jouer) ; vérifiée en tête de main


def porte_la_marque(texte, marque):
    """Rend vrai si la ligne commence par la marque, ou la porte juste après « · » (ligne marquée d'essai).

    ① RÔLE — Reconnaître une phase dans une ligne de sortie.
    ② CONTEXTE D'APPEL — `chronometrer`, `lire_un_chronometrage`.
    ③ ENTRÉE — `texte` : une ligne de sortie ; `marque` : un texte de MARQUES.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur, booléenne.
    [rend: 1]
    ⑥ TRAITEMENT — `startswith`, ou « · <marque> » dans la ligne.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Mesuré le 27-11-2026 : sans la seconde forme, aucune marque n'était vue (toutes les lignes de JOUER
      portent la marque d'essai « ESSAI — NI RÉSULTAT NI SÉLECTION · »).
    ⑨ CE QUI CLOCHE — Une ligne qui citerait une marque après « · » ailleurs compterait (aucune vue).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    return texte.startswith(marque) or (" · " + marque) in texte


def empreinte(texte):
    """Rend le sha256 hexadécimal des octets UTF-8 d'un texte.

    ① RÔLE — Une seule façon d'empreindre une tranche transportée, la même que celle du journal (V.sha, sur le fichier).
    ② CONTEXTE D'APPEL — `bloc_de_tranche`, `lire_les_blocs`.
    ③ ENTRÉE — `texte` : le contenu d'un fichier de tranche.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 64 caractères hexadécimaux.
    [rend: 1]
    ⑥ TRAITEMENT — hashlib.sha256 sur l'encodage UTF-8.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — le journal empreint les OCTETS du fichier : le texte est lu et réécrit en octets identiques
      (`newline=""`), donc les deux empreintes se comparent.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — rend la
    main.
    [sort: non]
    """
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()


def chronometrer(copie):
    """Joue la fiche d'essai avec chaque ligne datée ; rend (code, {phase: secondes depuis le départ}).

    ① RÔLE — Mesurer, sur la machine où il tourne, le coût réel des phases d'une tranche sur 20 ans.
    ② CONTEXTE D'APPEL — `main`, mode « chronometrer » ; l'épreuve longue ChronoEssai sur GitHub.
    ③ ENTRÉE — `copie` : une copie du dépôt sans .git (PREPARER_LA_MOULINETTE_D_ESSAI le refuse sinon, code 2).
    ④ CONDITIONS D'ENTRÉE — celles de PREPARER_LA_MOULINETTE_D_ESSAI (registre, fichier des 20 ans).
    ⑤ SORTIE — DEUX valeurs : le code de l'essai ; le dictionnaire des marques vues (première occurrence), en
      secondes depuis le lancement.
    [rend: 2]
    ⑥ TRAITEMENT — « PREPARER_LA_MOULINETTE_D_ESSAI.py <copie> --jouer » lancé avec PYTHONUNBUFFERED=1 (sinon la
      moulinette, sa fille, écrit par blocs et toutes les lignes arrivent à la fin) ; chaque ligne lue est affichée
      précédée de « [+<s> s] » ; la première ligne qui commence par une marque de MARQUES date sa phase. Au-delà de
      DELAI_DU_CHRONOMETRAGE, le processus est tué et le code est 124.
    ⑦ UNITÉ — secondes (horloge monotone).
    ⑧ POURQUOI — A-965 et le mandat du lot W2f : MESURER sur GitHub, pas extrapoler ; la fiche d'essai est la seule
      fiche que la moulinette peut jouer sur 2000-2023 sans regard (A-853, A-863).
    ⑨ CE QUI CLOCHE — voir l'en-tête, ⑨ ② et ⑨ ③. La sortie affichée porte aussi les résultats de l'essai (famille C5,
      déjà jouée, A-853) : la machine les écrit, ce programme ne les lit pas.
    ⑩ EFFET — celui de l'essai ; affiche.
    ⑪ TERMINAISON — rend la main ; l'essai est tué au délai.
    [sort: non]
    """
    env = dict(os.environ, PYTHONUNBUFFERED="1")
    t0 = time.monotonic()
    p = subprocess.Popen([sys.executable, "-B", os.path.join(copie, ESSAI_PROGRAMME), copie, "--jouer"], cwd=copie,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
    vus = {}
    minuteur = threading.Timer(DELAI_DU_CHRONOMETRAGE, p.kill)   # tue aussi un essai muet (aucune ligne)
    minuteur.start()
    try:
        for ligne in p.stdout:
            t = time.monotonic() - t0
            print("[+%7.1f s] %s" % (t, ligne.rstrip("\n")), flush=True)
            for nom, marque in MARQUES:
                if nom not in vus and porte_la_marque(ligne, marque):
                    vus[nom] = round(t, 1)
            if t > DELAI_DU_CHRONOMETRAGE:
                p.kill()
                break
        code = p.wait(timeout=60)
    finally:
        minuteur.cancel()
        if p.poll() is None:
            p.kill()
    if time.monotonic() - t0 > DELAI_DU_CHRONOMETRAGE:
        code = 124
    vus["total"] = round(time.monotonic() - t0, 1)
    return code, vus


def couts(vus):
    """Rend les coûts d'une tranche tirés des marques : (fixe_s, par_version_s, détail) ; lève ValueError si une marque manque.

    ① RÔLE — Traduire les instants des marques en coûts : ce qu'une tranche paie une fois, et ce qu'elle paie par
      version.
    ② CONTEXTE D'APPEL — `main` (modes chronometrer et planifier).
    ③ ENTRÉE — `vus` : {phase: secondes depuis le départ}, avec « total ».
    ④ CONDITIONS D'ENTRÉE — toutes les marques de MARQUES et « total » présentes (sinon ValueError, qui fait rendre 2).
    ⑤ SORTIE — TROIS valeurs : le coût fixe (s), le coût d'une version (s), le détail {lecture, calibrage, un_jeu,
      fixe, par_version, total}.
    [rend: 3]
    ⑥ TRAITEMENT — lecture = cours_lus − contrat ; calibrage = calibrage − cours_lus ; un_jeu = fiche_jouee −
      calibrage ; fixe = reglage (tout ce qui précède la boucle des versions : démarrage, préparation, contrat,
      lecture, calibrage, jeux de la fiche, de la version identique et, si la fin est recalculée, de la fiche sur la
      période jouée — la ligne « PARTIE DE RÉGLAGE » est écrite juste avant la boucle) ; par_version = fin − reglage
      (l'essai n'a qu'une version : la boucle en joue une ; plus l'écriture et la recopie des résultats).
    ⑦ UNITÉ — secondes.
    ⑧ POURQUOI — la tranche paie le fixe UNE fois, puis chaque version (`main` de JOUER_LES_VERSIONS).
    ⑨ CE QUI CLOCHE — par_version est celui d'UNE version de la fiche d'essai (6 valeurs, C5) : voir l'en-tête ⑨ ③.
      Une version jouée sous deux barèmes (témoin de résultats, `rejouer`) coûte deux jeux : non compté.
    ⑩ EFFET — —
    ⑪ TERMINAISON — rend la main, ou lève.
    [sort: non]
    """
    manque = [n for n, _ in MARQUES if n not in vus] + ([] if "total" in vus else ["total"])
    if manque:
        raise ValueError("marque(s) absente(s) de la sortie : %s" % ", ".join(manque))
    d = {"lecture": vus["cours_lus"] - vus["contrat"], "calibrage": vus["calibrage"] - vus["cours_lus"],
         "un_jeu": vus["fiche_jouee"] - vus["calibrage"], "fixe": vus["reglage"],
         "par_version": vus["fin"] - vus["reglage"], "total": vus["total"]}
    d = {k: round(v, 1) for k, v in d.items()}
    return d["fixe"], d["par_version"], d


def lire_un_chronometrage(chemin):
    """Rend {phase: secondes} relu dans une sortie du mode « chronometrer » (par exemple SORTIE.txt de GitHub).

    ① RÔLE — Que « planifier » parte de la MESURE écrite par la machine, jamais d'un chiffre tapé (R-728).
    ② CONTEXTE D'APPEL — `main`, mode planifier.
    ③ ENTRÉE — `chemin` : le fichier de sortie.
    ④ CONDITIONS D'ENTRÉE — le fichier se lit en UTF-8.
    ⑤ SORTIE — UN dictionnaire.
    [rend: 1]
    ⑥ TRAITEMENT — chaque ligne « [+<s> s] <texte> » : la première ligne dont le texte commence par une marque date
      sa phase ; « total » = la ligne « CHRONO total= » écrite par `main`, sinon l'instant de la dernière ligne.
    ⑦ UNITÉ — secondes.
    ⑧ POURQUOI — R-728.
    ⑨ CE QUI CLOCHE — sans la ligne CHRONO, le total est l'instant de la
      dernière ligne (au plus la seconde d'avant la fin).
    ⑩ EFFET — lit.
    ⑪ TERMINAISON — rend la main.
    [sort: non]
    """
    vus, dernier = {}, None
    with open(chemin, encoding="utf-8", errors="replace") as fh:
        for ligne in fh:
            m = re.match(r"\[\+\s*([0-9.]+) s\] (.*)$", ligne.rstrip("\n"))
            if m:
                t, texte = float(m.group(1)), m.group(2)
                dernier = t
                for nom, marque in MARQUES:
                    if nom not in vus and porte_la_marque(texte, marque):
                        vus[nom] = t
            m2 = re.match(r"CHRONO total=([0-9.]+)", ligne)
            if m2:
                vus["total"] = float(m2.group(1))
    if "total" not in vus and dernier is not None:
        vus["total"] = dernier
    return vus


def planifier(versions, fixe, par_version, budget, places, surcout):
    """Rend le plan de découpage d'une fiche de `versions` versions : un dictionnaire, ou lève ValueError.

    ① RÔLE — Dire, avant de lancer, combien de tranches, de vagues, d'exécutions et de temps une fiche coûtera.
    ② CONTEXTE D'APPEL — `main`, mode planifier ; les épreuves.
    ③ ENTRÉE — `versions` (≥ 1) ; `fixe`, `par_version` : secondes mesurées (`couts`) ; `budget` : secondes qu'un
      lancement de JOUER peut durer (580 sous l'enchaîneur ; jusqu'à 19 200 sous un job de GitHub) ; `places` (≥ 1) :
      machines en même temps ; `surcout` : secondes d'un job hors JOUER (démarrage, clone, copie, preparer, decliner,
      dépôt du résultat), mesurées sur un passage.
    ④ CONDITIONS D'ENTRÉE — par_version > 0 ; budget > fixe (sinon aucune version ne tient : ValueError).
    ⑤ SORTIE — UN dictionnaire : versions_par_tranche, tranches, vagues, executions, secondes_machine,
      secondes_au_mur, part_du_fixe (fraction du temps machine payée en fixe).
    [rend: 1]
    ⑥ TRAITEMENT — versions_par_tranche = ⌊(budget − fixe) / par_version⌋ ; tranches = ⌈versions /
      versions_par_tranche⌉, porté à min(places, versions) s'il est plus petit (mesuré le 27-11-2026 : sans cela, un
      budget de 19 200 s donnait 3 tranches pour 8 places, 18 300 s au mur au lieu de 6 925), puis la taille RÉELLE de tranche de JOUER (⌈versions / tranches⌉, `tranche`) ; vagues =
      ⌈tranches / places⌉ ; une vague dure surcout + fixe + taille × par_version ; au mur = vagues × cette durée ;
      machine = tranches × (surcout + fixe) + versions × par_version.
    ⑦ UNITÉ — secondes, versions, tranches, vagues.
    ⑧ POURQUOI — voir l'en-tête ⑧ : le fixe se paie par tranche ; le plan montre ce qu'il coûte.
    ⑨ CE QUI CLOCHE — les vagues sont supposées se suivre sans attente (relais, file de GitHub) ; la dernière vague
      peut être incomplète (comptée pleine : borne haute).
    ⑩ EFFET — —
    ⑪ TERMINAISON — rend la main, ou lève.
    [sort: non]
    """
    if versions < 1 or places < 1 or par_version <= 0 or budget <= fixe:
        raise ValueError("plan impossible : versions %s, places %s, par version %s s, budget %s s, fixe %s s"
                         % (versions, places, par_version, budget, fixe))
    vpt = int((budget - fixe) // par_version)
    if vpt < 1:
        raise ValueError("budget %s s : aucune version ne tient après le fixe de %s s" % (budget, fixe))
    n = max(-(-versions // vpt), min(places, versions))   # au moins une tranche par place : aucune machine oisive
    taille = -(-versions // n)
    vagues = -(-n // places)
    une_vague = surcout + fixe + taille * par_version
    machine = n * (surcout + fixe) + versions * par_version
    return {"versions_par_tranche": taille, "tranches": n, "vagues": vagues, "executions": n,
            "secondes_machine": round(machine), "secondes_au_mur": round(vagues * une_vague),
            "part_du_fixe": round(n * (surcout + fixe) / machine, 3)}


def bloc_de_tranche(ch, sid, essai, k, n):
    """Rend le texte du bloc qui transporte la tranche k/N jouée dans la chaîne `ch` ; lève V.Impossible si elle manque.

    ① RÔLE — Ce que la machine renvoie : la tranche, son empreinte, et les témoins qui disent de QUELLE chaîne elle est.
    ② CONTEXTE D'APPEL — `faire_une_tranche`, après « jouer k N » réussi.
    ③ ENTRÉE — `ch` : le dossier de la chaîne ; `sid`, `essai`, `k`, `n`.
    ④ CONDITIONS D'ENTRÉE — le témoin « 2-tranche-k » est au journal.
    ⑤ SORTIE — UN texte : DEBUT_DU_BLOC, une ligne JSON, FIN_DU_BLOC.
    [rend: 1]
    ⑥ TRAITEMENT — le fichier de tranche lu en texte (`newline=""` : octets gardés) ; son empreinte doit être celle du
      journal (sinon Impossible) ; JSON {strategie, essai, k, n, temoins: {étape: sha256} pour TEMOINS_COMPARES et la
      tranche, tranche: le texte, sha256}.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — le circuit ne rapporte que la sortie (en-tête ⑨ ①) ; JSON pour que le texte (virgules,
      guillemets, sauts de ligne) passe sans échappement à la main.
    ⑨ CE QUI CLOCHE — en-tête ⑨ ⑤.
    ⑩ EFFET — lit.
    ⑪ TERMINAISON — rend la main, ou lève.
    [sort: non]
    """
    t = V.temoins(ch)
    cle = TEMOIN_DE_TRANCHE % k
    if cle not in t:
        raise V.Impossible("la tranche %d n'a pas de témoin au journal de %s" % (k, ch))
    with open(os.path.join(ch, t[cle][0]), encoding="utf-8", newline="") as fh:
        texte = fh.read()
    if empreinte(texte) != t[cle][1]:
        raise V.Impossible("la tranche %d ne porte pas l'empreinte de son témoin" % k)
    temoins = {e: t[e][1] for e in TEMOINS_COMPARES if e in t}
    temoins[cle] = t[cle][1]
    corps = {"strategie": sid, "essai": essai, "k": k, "n": n, "temoins": temoins, "tranche": texte,
             "sha256": empreinte(texte)}
    return "%s\n%s\n%s" % (DEBUT_DU_BLOC, json.dumps(corps, ensure_ascii=True, sort_keys=True), FIN_DU_BLOC)


def enchainer(copie, sid, essai, *args):
    """Lance une étape de l'enchaîneur dans la copie ; rend son code. Borné.

    ① RÔLE — Faire jouer les étapes par l'enchaîneur, qui garde l'ordre et écrit les témoins (A-919) — jamais ici.
    ② CONTEXTE D'APPEL — `faire_une_tranche`.
    ③ ENTRÉE — `copie`, `sid`, `essai` ; `*args` : l'étape et ses arguments.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le code de l'enchaîneur (124 au délai).
    [rend: 1]
    ⑥ TRAITEMENT — « python3 -B <ce dossier>/ENCHAINER_LA_MOULINETTE.py <copie> <S> <E> <étape…> », sortie
      affichée telle quelle. Délai : 900 s (les délais propres de l'enchaîneur — 580 s pour JOUER, 300 s sinon — sont
      plus courts : c'est lui qui coupe d'abord).
    ⑦ UNITÉ — secondes.
    ⑧ POURQUOI — R-708 : l'enchaîneur VOISIN de ce programme — celui que `E` importe, donc
      celui de la version jouée quand ce programme est lancé depuis la copie (sur GitHub : <copie>/programmes/).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — celui de l'étape.
    ⑪ TERMINAISON — bornée.
    [sort: non]
    """
    try:
        p = subprocess.run([sys.executable, "-B", os.path.join(ICI, "ENCHAINER_LA_MOULINETTE.py"),
                            copie, sid, essai] + list(args), cwd=copie, capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        print("ÉTAPE %s : délai de 900 s dépassé" % " ".join(args))
        return 124
    sys.stdout.write(p.stdout + p.stderr)
    return p.returncode


def faire_une_tranche(copie, sid, essai, k, n, maitre=False):
    """Le bout « machine » : ⓪ ① puis « jouer k N », et le bloc ; rend le code.

    ① RÔLE — Jouer UNE tranche sur une machine qui n'a que la copie, et en renvoyer la preuve.
    ② CONTEXTE D'APPEL — `main`, mode tranche.
    ③ ENTRÉE — `copie` (sans .git), `sid`, `essai`, `k`, `n` ; `maitre` : « --cours-du-maitre » passé à ⓪.
    ④ CONDITIONS D'ENTRÉE — la copie porte les réglages validés de la fiche ; aucune chaîne n'y est commencée, ou
      seulement ⓪ ① (reprise sur la même machine).
    ⑤ SORTIE — UNE valeur : 0 la tranche est jouée et son bloc écrit ; sinon le code de la première étape en échec.
    [rend: 1]
    ⑥ TRAITEMENT — preparer (sauf si « 0-proposition » est déjà au journal), decliner (de même), « jouer k N »,
      chacun par `enchainer` ; puis `bloc_de_tranche` affiché.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — ⓪ ① sont rejoués sur chaque machine (quelques secondes) : la machine ne reçoit que la
      copie ; « rassembler » vérifie au centre que ⓪ ① y ont donné les mêmes octets.
    ⑨ CE QUI CLOCHE — si ⓪ ① ne sont pas déterministes (ils devraient l'être : mêmes fichiers d'entrée), toutes les
      tranches sont refusées au centre — visible, jamais silencieux.
    ⑩ EFFET — écrit sous <copie>/CHAINE_<S>_<E>/ ; affiche.
    ⑪ TERMINAISON — rend la main.
    [sort: non]
    """
    if os.path.lexists(os.path.join(copie, ".git")):
        print("ARRÊT (DECOUPER) : %s porte .git — la moulinette ne tourne que sur une copie (A-861) ; rien n'est lancé"
              % copie)
        return 2
    t = V.temoins(V.dossier(copie, sid, essai)) if os.path.isdir(V.dossier(copie, sid, essai)) else {}
    etapes = [] if E.FAITE["preparer"] in t else [["preparer"] + (["--cours-du-maitre"] if maitre else [])]
    etapes += [] if E.FAITE["decliner"] in t else [["decliner"]]
    for etape in etapes + [["jouer", str(k), str(n)]]:
        code = enchainer(copie, sid, essai, *etape)
        if code:
            print("TRANCHE %d/%d : l'étape %s a rendu %d — aucun bloc" % (k, n, etape[0], code))
            return code
    print(bloc_de_tranche(V.dossier(copie, sid, essai), sid, essai, k, n))
    return 0


# LA CHAÎNE D'ESSAI (lot TRANSPORT du plan R505, A-965, 27-11-2026). La fiche d'essai ESSAI-C5-2000-2026 (A-853, A-861,
# A-863) n'a qu'une version et JOUER refuse « --tranche= » avec « --essai-sans-regard » : elle ne passe pas par
# l'enchaîneur. Pour éprouver le TRANSPORT de bout en bout sur GitHub, elle est DÉCLINÉE ARTIFICIELLEMENT en N versions
# identiques (mêmes réglages, identifiants <fiche>-E01-0001 … -000N) : la tranche k du découpage en N (JOUER.tranche,
# taille ⌈N/N⌉ = 1) est la version k, jouée seule par la commande de l'essai déclaré. La chaîne porte les mêmes témoins
# que celle de l'enchaîneur (cours, réglages, proposition, combinatoire) : `rassembler` la reçoit sans rien savoir de
# l'essai. Ses fichiers : e0/FICHE_D_ESSAI.txt (la ligne de la fiche au registre de la copie, et l'empreinte du fichier
# des cours), e0/PROPOSITION_D_ESSAI.txt, e1/COMBINATOIRE_D_ESSAI_EN_<N>.csv, e2/combinatoire_<k>.csv (la version k).
TEXTE_DE_LA_PROPOSITION_D_ESSAI = ("proposition : aucune — fiche d'essai %s (A-853, A-861, A-863), déclinée "
                                   "artificiellement en N versions identiques par DECOUPER_LA_MOULINETTE (lot TRANSPORT, "
                                   "A-965) ; réglages = ceux de la fiche\n" % P.IDENTIFIANT)


def chaine_d_essai(copie, n):
    """Fait (ou relit) la chaîne d'essai déclinée en n versions dans la copie ; rend le dossier de la chaîne.

    ① RÔLE — Donner à la fiche d'essai une chaîne aux mêmes témoins que celle de l'enchaîneur, pour que le transport
      s'éprouve sur GitHub sans regard (commentaire ci-dessus).
    ② CONTEXTE D'APPEL — `faire_une_tranche_d_essai` (machine) ; `main`, mode preparer-essai (centre, avant
      `rassembler`) ; programmes/TRANSPORTER_LA_MOULINETTE.py (centre).
    ③ ENTRÉE — `copie` : une copie du dépôt sans .git ; `n` : le nombre de tranches (≥ 2).
    ④ CONDITIONS D'ENTRÉE — Celles de PREPARER_LA_MOULINETTE_D_ESSAI.preparer, si la chaîne n'existe pas encore.
    ⑤ SORTIE — UNE valeur : le dossier de la chaîne (V.dossier). Lève V.Impossible si une chaîne existe déjà avec
      une autre combinatoire (un autre n), ValueError ou OSError si la préparation tombe.
    [rend: 1]
    ⑥ TRAITEMENT — Chaîne déjà commencée (témoin « 1-decliner » au journal) : son fichier doit être
      e1/COMBINATOIRE_D_ESSAI_EN_<n>.csv, sinon Impossible ; rendue telle quelle (la garde des empreintes est celle de
      V.motifs, appelée par `rassembler` et par la tranche). Sinon : ① P.preparer(copie) (registre de la copie et
      combinatoire d'une version) ; ② E.ecrire_les_cours(ch, False) (les 20 ans, témoin « 0-cours-de-la-chaine ») ;
      ③ e0/FICHE_D_ESSAI.txt : l'en-tête et la ligne de la fiche d'essai du registre de la copie, puis « cours <chemin>
      sha256 <empreinte du fichier> » → témoin « 0-variables-validees » ; ④ e0/PROPOSITION_D_ESSAI.txt →
      « 0-proposition » ; ⑤ la combinatoire d'une version, répétée n fois, identifiants -0001 … -<n> sur 4 chiffres
      → « 1-decliner ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — TEMOINS_COMPARES : la machine et le centre doivent porter les mêmes octets ; tout est fabriqué depuis
      les fichiers de la copie, sans heure ni hasard, donc deux machines sur la même pointe donnent les mêmes
      empreintes. L'empreinte du fichier des cours entre dans le témoin des réglages : le témoin des cours de
      l'enchaîneur ne porte que le CHEMIN (deux contenus sous un même nom passeraient).
    ⑨ CE QUI CLOCHE — Les n versions sont IDENTIQUES : la chaîne d'essai éprouve le transport et l'accueil, pas un
      résultat ; elle n'est jamais triée ni jugée (aucun programme de la chaîne ne la lit après `rassembler`).
      L'assemblage de JOUER sur elle n'est pas éprouvé ici.
    ⑩ EFFET — Écrit dans la copie : registre, combinatoire d'essai (P.preparer), dossier de la chaîne.
    ⑪ TERMINAISON — Rend la main, ou lève.
    [sort: non]
    """
    ch = V.dossier(copie, P.IDENTIFIANT, P.ESSAI)
    nom_comb = "e1/COMBINATOIRE_D_ESSAI_EN_%d.csv" % n
    t = V.temoins(ch) if os.path.isdir(ch) else {}
    if E.FAITE["decliner"] in t:
        if t[E.FAITE["decliner"]][0] != nom_comb:
            raise V.Impossible("la chaîne d'essai de %s est déclinée en %s, pas en %d tranches"
                               % (copie, t[E.FAITE["decliner"]][0], n))
        return ch
    P.preparer(copie)
    os.makedirs(os.path.join(ch, "e0"))
    os.makedirs(os.path.join(ch, "e1"))
    E.ecrire_les_cours(ch, False)
    with open(os.path.join(copie, P.REGISTRE), encoding="utf-8-sig", newline="") as fh:
        lignes = list(csv.reader(fh))
    i_id = lignes[0].index("id")
    fiche = [r for r in lignes[1:] if len(r) > i_id and r[i_id] == P.IDENTIFIANT]
    if len(fiche) != 1:
        raise V.Impossible("la fiche d'essai est %d fois au registre de la copie" % len(fiche))
    sortie = io.StringIO()
    csv.writer(sortie, lineterminator="\n").writerows([lignes[0], fiche[0]])
    with open(os.path.join(copie, P.COURS_DES_VINGT_ANS), "rb") as fh:
        cours = hashlib.sha256(fh.read()).hexdigest()
    with open(os.path.join(ch, "e0", "FICHE_D_ESSAI.txt"), "w", encoding="utf-8", newline="") as fh:
        fh.write(sortie.getvalue() + "cours %s sha256 %s\n" % (P.COURS_DES_VINGT_ANS, cours))
    V.temoigner(ch, "0-variables-validees", "e0/FICHE_D_ESSAI.txt")
    with open(os.path.join(ch, "e0", "PROPOSITION_D_ESSAI.txt"), "w", encoding="utf-8", newline="") as fh:
        fh.write(TEXTE_DE_LA_PROPOSITION_D_ESSAI)
    V.temoigner(ch, "0-proposition", "e0/PROPOSITION_D_ESSAI.txt")
    with open(os.path.join(copie, P.COMBINATOIRE), encoding="utf-8", newline="") as fh:
        une = list(csv.DictReader(fh))
    if len(une) != 1:
        raise V.Impossible("la combinatoire d'essai porte %d versions, une attendue" % len(une))
    with open(os.path.join(ch, nom_comb), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(une[0]), lineterminator="\n")
        w.writeheader()
        for k in range(n):
            w.writerow(dict(une[0], id_version="%s-%s-%04d" % (P.IDENTIFIANT, P.ESSAI, k + 1)))
    V.temoigner(ch, E.FAITE["decliner"], nom_comb)
    return ch


def faire_une_tranche_d_essai(copie, k, n):
    """Le bout « machine » de la chaîne d'essai : la version k jouée seule par l'essai déclaré, puis le bloc ; rend le code.

    ① RÔLE — Jouer UNE tranche de la fiche d'essai déclinée en n (commentaire de TEXTE_DE_LA_PROPOSITION_D_ESSAI) et en
      renvoyer la preuve, comme `faire_une_tranche` pour une vraie chaîne.
    ② CONTEXTE D'APPEL — `main`, mode tranche-essai ; sur GitHub, la famille « MoulEssai » de
      tests/LANCEMENT_DES_EPREUVES.json (circuit des épreuves longues, lot TRANSPORT).
    ③ ENTRÉE — `copie` (sans .git) ; `k`, `n` (0 ≤ k < n, n ≥ 2).
    ④ CONDITIONS D'ENTRÉE — Celles de `chaine_d_essai`.
    ⑤ SORTIE — UNE valeur : 0 la tranche est jouée et son bloc écrit ; 2 copie avec .git, ou n < 2 ; 1 refus de la
      garde, tranche déjà jouée, découpage mêlé, ou moulinette en échec (son code, s'il est non nul) ; 124 au délai.
    [rend: 1]
    ⑥ TRAITEMENT — .git refusé ; `chaine_d_essai` ; V.motifs (étapes ⓪ ① intactes) ; tranche déjà témoignée →
      refus ; V.decoupage_mele ; e2/combinatoire_<k>.csv = l'en-tête et la ligne de JOUER.tranche(combinatoire, k, n) ;
      la commande P.commande_de_jeu (option d'essai lue au contrat, CONTRATS_DES_FICHIERS) vers e2/tranche_<k>.csv,
      sortie gardée dans e2/sortie_<k>.txt, bornée à DELAI_DU_CHRONOMETRAGE ; code 0 → témoin « 2-tranche-k » et
      `bloc_de_tranche` affiché ; sinon les six dernières lignes de la sortie (les erreurs) et le code.
    ⑦ UNITÉ — Secondes (délai).
    ⑧ POURQUOI — Le transport s'éprouve sur la seule fiche qui joue les 20 ans sans regard (A-853, A-863). Le découpage
      est celui de JOUER (R-708), pour que `rassembler` et sa garde (`V.decoupage_mele`) le reconnaissent.
    ⑨ CE QUI CLOCHE — La sortie de la moulinette n'est pas affichée quand elle réussit (elle porte les chiffres de
      l'essai ; le bloc porte de toute façon le fichier de résultats) : elle reste dans la copie. Le délai de
      DELAI_DU_CHRONOMETRAGE (30 min) vaut pour UNE version ; il n'est pas celui d'une vraie tranche.
    ⑩ EFFET — Écrit dans la copie (chaîne d'essai) ; affiche le bloc.
    ⑪ TERMINAISON — Rend la main ; la moulinette est bornée.
    [sort: non]
    """
    if os.path.lexists(os.path.join(copie, ".git")):
        print("ARRÊT (DECOUPER) : %s porte .git — la moulinette ne tourne que sur une copie (A-861) ; rien n'est lancé"
              % copie)
        return 2
    if n < 2:
        print("ARRÊT (DECOUPER) : une tranche d'essai exige au moins 2 tranches (lu %d)" % n)
        return 2
    ch = chaine_d_essai(copie, n)
    m = V.motifs(copie, P.IDENTIFIANT, P.ESSAI, E.EXIGEES["jouer"])
    if TEMOIN_DE_TRANCHE % k in V.temoins(ch):
        m.append("la tranche %d est déjà jouée" % k)
    m += V.decoupage_mele(ch, n)
    if m:
        print("REFUS de la tranche d'essai %d/%d :\n  %s" % (k, n, "\n  ".join(m)))
        return 1
    import JOUER_LES_VERSIONS as JOUER
    import CONTRATS_DES_FICHIERS as CE
    with open(os.path.join(ch, V.temoins(ch)[E.FAITE["decliner"]][0]), encoding="utf-8", newline="") as fh:
        lignes = list(csv.DictReader(fh))
    part = JOUER.tranche(lignes, k, n)
    os.makedirs(os.path.join(ch, "e2"), exist_ok=True)
    comb = os.path.join(ch, "e2", "combinatoire_%d.csv" % k)
    with open(comb, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(lignes[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(part)
    rel = "e2/tranche_%d.csv" % k
    commande = P.commande_de_jeu(copie, os.path.relpath(comb, copie), os.path.join(ch, rel),
                                 CE.OPTION_D_ESSAI_SANS_REGARD)
    try:
        p = subprocess.run(commande, cwd=copie, capture_output=True, text=True, timeout=DELAI_DU_CHRONOMETRAGE)
    except subprocess.TimeoutExpired:
        print("TRANCHE D'ESSAI %d/%d : délai de %d s dépassé — aucun bloc" % (k, n, DELAI_DU_CHRONOMETRAGE))
        return 124
    with open(os.path.join(ch, "e2", "sortie_%d.txt" % k), "w", encoding="utf-8") as fh:
        fh.write(p.stdout + p.stderr)
    if p.returncode:
        print("TRANCHE D'ESSAI %d/%d : la moulinette a rendu %d — aucun bloc\n%s" % (
            k, n, p.returncode, "\n".join("  " + l for l in (p.stdout + p.stderr).splitlines()[-6:])))
        return p.returncode
    V.temoigner(ch, TEMOIN_DE_TRANCHE % k, rel)
    print("TRANCHE D'ESSAI %d/%d : jouée (sortie de la moulinette gardée dans la copie, non affichée)" % (k, n))
    print(bloc_de_tranche(ch, P.IDENTIFIANT, P.ESSAI, k, n))
    return 0


def chaine_de_la_commande(arguments):
    """Rend (stratégie, essai) de la chaîne qu'une commande de tranche joue ; lève ValueError si ce n'en est pas une.

    ① RÔLE — Dire au centre (programmes/TRANSPORTER_LA_MOULINETTE.py) dans quelle chaîne recevoir les tranches d'une
      famille de la table, sans recopier la forme des commandes de ce programme (R-708).
    ② CONTEXTE D'APPEL — TRANSPORTER_LA_MOULINETTE (recevoir) ; les épreuves.
    ③ ENTRÉE — `arguments` : les arguments d'une famille de tests/LANCEMENT_DES_EPREUVES.json (avec « {k} », « {n} »
      remplacés ou non).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : l'identifiant de la stratégie, l'essai.
    [rend: 2]
    ⑥ TRAITEMENT — « tranche-essai {copie} k n » → (P.IDENTIFIANT, P.ESSAI) ; « tranche {copie} S E k n
      [--cours-du-maitre] » → (S, E) ; tout autre forme → ValueError.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir ①.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main, ou lève.
    [sort: non]
    """
    a = list(arguments)
    if len(a) == 4 and a[0] == "tranche-essai":
        return P.IDENTIFIANT, P.ESSAI
    if len(a) in (6, 7) and a[0] == "tranche" and (len(a) == 6 or a[6] == "--cours-du-maitre"):
        return a[2], a[3]
    raise ValueError("commande de tranche inconnue : %r" % a[:2])


def lire_les_blocs(chemins):
    """Rend la liste des blocs lus dans les fichiers, chacun vérifié en lui-même ; lève ValueError sinon.

    ① RÔLE — Ne rien accepter d'illisible, de tronqué, ou dont le contenu ne porte pas son empreinte.
    ② CONTEXTE D'APPEL — `rassembler`.
    ③ ENTRÉE — `chemins` : des fichiers de sortie.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE liste de dictionnaires (le JSON du bloc, plus « source »).
    [rend: 1]
    ⑥ TRAITEMENT — entre chaque DEBUT_DU_BLOC et le FIN_DU_BLOC suivant, une ligne JSON ; champs exigés ; k et n
      entiers, 0 ≤ k < n ; empreinte du texte = sha256 = témoin de la tranche. Un début sans fin → refus.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — une sortie coupée au délai (code 124) peut porter un bloc tronqué.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — lit.
    ⑪ TERMINAISON — rend la main, ou lève.
    [sort: non]
    """
    blocs = []
    for chemin in chemins:
        with open(chemin, encoding="utf-8") as fh:
            lignes = fh.read().split("\n")
        i = 0
        while i < len(lignes):
            if lignes[i].strip() == DEBUT_DU_BLOC:
                if i + 2 >= len(lignes) or lignes[i + 2].strip() != FIN_DU_BLOC:
                    raise ValueError("%s : bloc de tranche tronqué (ligne %d)" % (chemin, i + 1))
                b = json.loads(lignes[i + 1])
                if not isinstance(b, dict) or not isinstance(b.get("temoins"), dict) or not all(
                        isinstance(b.get(c), str) for c in ("strategie", "essai", "tranche", "sha256")):
                    raise ValueError("%s : bloc mal formé (ligne %d)" % (chemin, i + 2))
                if not (isinstance(b["k"], int) and isinstance(b["n"], int) and 0 <= b["k"] < b["n"]):
                    raise ValueError("%s : tranche %r/%r hors découpage" % (chemin, b["k"], b["n"]))
                if empreinte(b["tranche"]) != b["sha256"] or b["temoins"].get(TEMOIN_DE_TRANCHE % b["k"]) != b["sha256"]:
                    raise ValueError("%s : la tranche %d ne porte pas son empreinte" % (chemin, b["k"]))
                b["source"] = chemin
                blocs.append(b)
                i += 3
            else:
                i += 1
    return blocs


def rassembler(racine, sid, essai, n, chemins):
    """Le bout « centre » : reçoit les blocs dans la chaîne locale ; rend (code, tranches manquantes).

    ① RÔLE — Recevoir les tranches jouées ailleurs comme si l'enchaîneur les avait jouées ici, mais seulement si elles
      sont de CETTE chaîne, et dire ce qui manque.
    ② CONTEXTE D'APPEL — `main`, mode rassembler, après le rapatriement des sorties.
    ③ ENTRÉE — `racine` (copie sans .git, où ⓪ ① ont été faits par l'enchaîneur), `sid`, `essai`, `n`, `chemins`.
    ④ CONDITIONS D'ENTRÉE — la garde de l'étape jouer passe (`V.motifs` avec E.EXIGEES["jouer"]) et le découpage en n
      ne mêle rien (`V.decoupage_mele`).
    ⑤ SORTIE — DEUX valeurs : 0 toutes les tranches sont là · 1 refus (rien n'est écrit) · 3 reçues, mais il en manque ;
      la liste des k manquants.
    [rend: 2]
    ⑥ TRAITEMENT — TOUT est vérifié AVANT d'écrire : ① garde et découpage ; ② `lire_les_blocs` (un bloc illisible :
      refus, code 1) ; ③ chaque bloc : même
      stratégie, même essai, même n, et chaque témoin de TEMOINS_COMPARES égal à celui du journal local ; ④ deux blocs
      d'un même k : refus s'ils diffèrent, un seul gardé s'ils sont identiques ; ⑤ un k déjà témoigné ici : ignoré
      s'il a la même empreinte (une reprise qui renvoie tout), refus sinon. Puis, pour chaque k neuf, dans l'ordre :
      e2/tranche_k.csv créé (jamais écrasé) aux octets du bloc, et `V.temoigner(ch, "2-tranche-k", …)`.
    ⑦ UNITÉ — tranches.
    ⑧ POURQUOI — A-919 (une étape n'existe que par son témoin) ; A-1076 (une tranche jouée sur d'autres cours ne
      s'assemble pas : l'empreinte du témoin des cours est comparée ici, et l'assemblage de JOUER compare encore la
      colonne cours_joues) ; reprise : une tranche tombée est simplement absente, et rejouée.
    ⑨ CE QUI CLOCHE — en-tête ⑨ ④. Le témoin est écrit par CE programme (par la fonction de l'enchaîneur,
      V.temoigner), pas par l'enchaîneur : l'enchaîneur ne sait pas recevoir une tranche jouée ailleurs.
    ⑩ EFFET — écrit e2/tranche_<k>.csv et le journal.
    ⑪ TERMINAISON — rend la main ; lève V.Impossible ou ValueError
      (convertis en 2 par `main`).
    [sort: non]
    """
    ch = V.dossier(racine, sid, essai)
    m = V.motifs(racine, sid, essai, E.EXIGEES["jouer"]) + V.decoupage_mele(ch, n)
    if m:
        print("REFUS — la chaîne locale ne peut pas recevoir de tranche :\n  %s" % "\n  ".join(m))
        return 1, []
    local = V.temoins(ch)
    refus, neufs = [], {}
    try:
        blocs = lire_les_blocs(chemins)
    except ValueError as e:   # un bloc tronqué, mal formé ou qui ne porte pas son empreinte est REFUSÉ, pas « impossible »
        print("REFUS — rien n'est écrit :\n  %s" % e)
        return 1, []
    for b in blocs:
        ou = "%s (tranche %s)" % (b["source"], b["k"])
        if (b["strategie"], b["essai"], b["n"]) != (sid, essai, n):
            refus.append("%s : bloc de %s %s en %s tranches, attendu %s %s en %d" % (ou, b["strategie"], b["essai"],
                                                                                     b["n"], sid, essai, n))
            continue
        for e in TEMOINS_COMPARES:
            if e not in local or b["temoins"].get(e) != local[e][1]:
                refus.append("%s : témoin %s différent de la chaîne locale — tranche d'une autre chaîne" % (ou, e))
        cle = TEMOIN_DE_TRANCHE % b["k"]
        if cle in local and local[cle][1] != b["sha256"]:
            refus.append("%s : la tranche %d est déjà reçue avec une autre empreinte" % (ou, b["k"]))
        if b["k"] in neufs and neufs[b["k"]]["sha256"] != b["sha256"]:
            refus.append("%s : deux blocs différents pour la tranche %d" % (ou, b["k"]))
        if cle not in local:
            neufs.setdefault(b["k"], b)
    if refus:
        print("REFUS — rien n'est écrit :\n  %s" % "\n  ".join(refus))
        return 1, []
    os.makedirs(os.path.join(ch, "e2"), exist_ok=True)
    for k in sorted(neufs):
        rel = "e2/tranche_%d.csv" % k
        with open(os.path.join(ch, rel), "x", encoding="utf-8", newline="") as fh:
            fh.write(neufs[k]["tranche"])
        V.temoigner(ch, TEMOIN_DE_TRANCHE % k, rel)
        print("REÇUE : tranche %d/%d (%s)" % (k, n, neufs[k]["source"]))
    t = V.temoins(ch)
    manquent = [k for k in range(n) if TEMOIN_DE_TRANCHE % k not in t]
    if manquent:
        print("À REJOUER : %s (sur %d)" % (" ".join(str(k) for k in manquent), n))
        return 3, manquent
    print("TOUTES LES TRANCHES SONT LÀ : %d — l'assemblage est « ENCHAINER_LA_MOULINETTE.py … assembler »" % n)
    return 0, []


def entier(texte, nom, minimum):
    """Rend int(texte) si c'est un entier ASCII ≥ minimum, sinon lève ValueError.

    ① RÔLE — Lire un argument entier de la ligne de commande.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `texte` : l'argument ; `nom` : son nom, pour le message ; `minimum` : la plus petite valeur permise.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : l'entier.
    [rend: 1]
    ⑥ TRAITEMENT — Chiffres ASCII seuls, sans zéro de tête (comme l'enchaîneur, L-10 du RELU Cowork du 25-11-2026).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734 : un argument faux arrête, jamais une valeur devinée.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main, ou lève.
    [sort: non]
    """
    if not (texte.isascii() and texte.isdigit() and texte == str(int(texte)) and int(texte) >= minimum):
        raise ValueError("%s : entier ≥ %d attendu, lu %r" % (nom, minimum, texte))
    return int(texte)


def main(argv):
    """Rend le code de sortie de la ligne de commande.

    ① RÔLE — aiguiller vers le mode.
    ② CONTEXTE D'APPEL — `__main__`.
    ③ ENTRÉE — `argv` (voir USAGE).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : voir l'en-tête ⑤.
    [rend: 1]
    ⑥ TRAITEMENT — ⓪ la forme du témoin de tranche est vérifiée contre l'enchaîneur (`E.faire` doit l'écrire telle
      quelle : son texte porte « "2-tranche-%s" % k ») · ① le mode et ses arguments · ② le mode · ③ ValueError,
      OSError, V.Impossible → 2.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734.
    ⑨ CE QUI CLOCHE — ⓪ est une recherche de texte dans l'enchaîneur : elle ne prouve
      que la présence de la forme.
    ⑩ EFFET — celui du mode.
    ⑪ TERMINAISON — rend la main.
    [sort: non]
    """
    import inspect
    if '"2-tranche-%s" % k' not in inspect.getsource(E.faire):
        print("CONTRÔLE IMPOSSIBLE (R-734) : l'enchaîneur n'écrit plus le témoin de tranche « 2-tranche-<k> »")
        return 2
    try:
        mode, a = (argv[1] if len(argv) > 1 else ""), argv[2:]
        if mode == "chronometrer" and len(a) == 1:
            code, vus = chronometrer(os.path.abspath(a[0]))
            fixe, pv, d = couts(vus)
            print("CHRONO total=%.1f · " % d["total"] + " · ".join("%s=%.1f s" % (k, v) for k, v in d.items()
                                                                if k != "total") + " · code de l'essai %d" % code)
            return code
        if mode == "planifier" and len(a) == 5:
            fixe, pv, d = couts(lire_un_chronometrage(a[0]))
            p = planifier(entier(a[1], "versions", 1), fixe, pv, float(a[2]), entier(a[3], "places", 1), float(a[4]))
            print("MESURE LUE (%s) : fixe %.1f s · par version %.1f s · lecture %.1f s · calibrage %.1f s · un jeu %.1f s"
                  % (a[0], fixe, pv, d["lecture"], d["calibrage"], d["un_jeu"]))
            print("PLAN : " + " · ".join("%s=%s" % kv for kv in p.items()))
            return 0
        if mode == "tranche" and len(a) in (5, 6) and (len(a) == 5 or a[5] == "--cours-du-maitre"):
            k, n = entier(a[3], "k", 0), entier(a[4], "N", 1)
            if k >= n:
                raise ValueError("k = %d hors du découpage en %d" % (k, n))
            return faire_une_tranche(os.path.abspath(a[0]), a[1], a[2], k, n, maitre=len(a) == 6)
        if mode == "tranche-essai" and len(a) == 3:
            k, n = entier(a[1], "k", 0), entier(a[2], "N", 1)
            if k >= n:
                raise ValueError("k = %d hors du découpage en %d" % (k, n))
            return faire_une_tranche_d_essai(os.path.abspath(a[0]), k, n)
        if mode == "preparer-essai" and len(a) == 2:
            racine = os.path.abspath(a[0])
            if os.path.lexists(os.path.join(racine, ".git")):
                print("ARRÊT : %s porte .git (A-861)" % racine)
                return 2
            ch = chaine_d_essai(racine, entier(a[1], "N", 2))
            print("CHAÎNE D'ESSAI PRÊTE : %s · " % ch + " · ".join(
                "%s %s…" % (e, h[:12]) for e, (_f, h) in sorted(V.temoins(ch).items())))
            return 0
        if mode == "rassembler" and len(a) >= 5:
            racine = os.path.abspath(a[0])
            if os.path.lexists(os.path.join(racine, ".git")):
                print("ARRÊT : %s porte .git (A-861)" % racine)
                return 2
            return rassembler(racine, a[1], a[2], entier(a[3], "N", 1), a[4:])[0]
        print(__doc__.split("① RÔLE")[0])
        return 2
    except (ValueError, OSError, V.Impossible) as e:
        print("CONTRÔLE IMPOSSIBLE (R-734) : %s: %s" % (type(e).__name__, e))
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
