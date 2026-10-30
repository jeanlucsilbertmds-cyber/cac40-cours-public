#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JOUER_LES_VERSIONS.py — Jeu 08-10-2026 (Paris)
EN ESSAI · outil · Rôle : rejouer chaque version d'une combinatoire avec le vrai juge des stratégies.
Quand l'appeler : à la main, après DECLINER_LES_STRATEGIES.

USAGE
    python3 JOUER_LES_VERSIONS.py <racine_du_depot> <combinatoire> <fichier_resultats>
    exemple :
    python3 programmes/JOUER_LES_VERSIONS.py . \
        donnees/combinatoires/COMBINATOIRE_C5E10-OBS-V1_E01.csv \
        donnees/combinatoires/RESULTATS_C5E10-OBS-V1_E01.csv

CE QUE CE PROGRAMME EST DANS LA CHAÎNE (action A-541 du BACKLOG)
    ⓪ PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES propose les réglages ;
    Jean-Luc valide · ① DECLINER_LES_STRATEGIES fabrique les versions ·
    ② CE PROGRAMME les rejoue en appelant `jouer` du juge des stratégies, sans rien
    recalculer lui-même · ③ TRIER_LES_VARIANTES (à écrire) · ④ `juger`.

① RÔLE — Donner, pour chaque version figée d'une stratégie, le résultat qu'elle
  aurait eu sur la période de sa fiche : nombre d'opérations, réussite, gain net.
  C'est la matière que le tri et le jugement examineront.
② CONTEXTE D'APPEL — À la main, par le Chat. Aucune tâche automatique ne l'appelle.
③ ENTRÉE — La ligne de commande, trois arguments : la racine d'un dépôt (registre
  des stratégies, fichier maître des cours, référentiel, modules de signal et de
  positions, témoin du golden) ; une combinatoire écrite par DECLINER ; le chemin
  du fichier de résultats, qui ne doit pas exister.
④ CONDITIONS D'ENTRÉE — ① la combinatoire n'est pas vide, toutes ses lignes
  portent la même stratégie et le même essai, ses identifiants sont uniques, et
  son nombre de lignes égale la colonne `versions_dans_l_essai`, aucun univers
  n'écrit deux fois la même valeur · ② une seule
  version y est marquée identique à la fiche · ③ la fiche existe une fois au
  registre · ④ le juge des stratégies, lancé seul sur cette fiche, se calibre sur
  le témoin du golden et rend le même résultat que ce programme · ⑤ chaque
  version, une fois fusionnée, est lue par le juge avec ses propres réglages ·
  ⑥ les cours de CHAQUE valeur vont assez loin après la période pour l'horizon le
  plus long · ⑦ si un témoin de résultats existe, chaque version le retrouve.
  Le moindre manquement arrête tout, avant ou pendant le jeu.
⑤ SORTIE — UNE valeur : le code de sortie, 0 quand toutes les versions sont
  jouées et écrites, 1 sinon.
  [rend: 1]
⑥ TRAITEMENT — ① lire et contrôler la combinatoire · ② lancer le juge des
  stratégies seul sur la fiche et exiger son calibrage · ③ charger cours et modules
  par les fonctions du juge · ④ jouer la fiche telle quelle et exiger le résultat
  que le juge vient d'afficher · ⑤ jouer la version identique et exiger le même
  résultat · ⑥ contrôler la marge de cours après la période · ⑦ pour chaque
  version : fusionner, contrôler la fusion, jouer, écrire une ligne dans un
  fichier provisoire · ⑧ comparer au témoin de résultats s'il existe ·
  ⑨ renommer le fichier provisoire en fichier final.
⑦ UNITÉ — Gains en EUROS pour 100 000 € engagés par opération ; réussite en
  POURCENTS ; tp et sl en FRACTIONS du prix d'entrée ; horizon en SÉANCES.
⑧ POURQUOI — TOUT LE CALCUL RESTE DANS LE JUGE : deux implémentations d'une même
  chose divergent toujours (R-708). Le calibrage passe par le juge lancé seul,
  parce qu'un calibrage maison comparant deux appels du même code resterait vert
  si le code ou les données changeaient (relecture du 08-10-2026, défaut A1).
  La fusion est contrôlée version par version, parce que la version identique
  à la fiche ne peut pas révéler une case oubliée (défaut A2).
⑨ CE QUI CLOCHE — ① le calibrage du juge compare le nombre d'opérations et les
  sorties, pas les frais : des frais doublés passeraient (relecture du
  08-10-2026) ; seul le témoin de résultats les attrape, et sans témoin rien ne
  les attrape · ② la période jouée est celle de la fiche ; le signal est forcé
  à `signaux_c5etendu10` tant qu'A-542 n'est pas faite · ③ la version à zéro
  opération porte un gain de 0, que le tri devra traiter à part.
⑩ EFFET — Crée le fichier de résultats, via un fichier provisoire `.en_cours`
  effacé en cas d'échec s'il a été créé par ce lancement. Rien d'autre n'est
  écrit : le juge est lancé avec `-B`.
⑪ TERMINAISON — Sort du programme avec le code 0 ou 1. Le juge est lancé dans un
  processus séparé, sans limite de temps : s'il ne revenait pas, ce programme
  non plus.
  [sort: oui]
⑫ DÉFINITIONS
  le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui
    rejoue une stratégie sur l'historique des cours et rend ses opérations.
  une fiche : la ligne qui décrit une stratégie dans `donnees/cac40_strategies.csv`.
  une version : une ligne de la combinatoire, où chaque réglage n'a qu'une valeur.
  la combinatoire : le fichier `COMBINATOIRE_<STRATÉGIE>_<ESSAI>.csv` écrit par
    DECLINER_LES_STRATEGIES, une version par ligne.
  le témoin du golden : la copie conservée des cours qui ont produit les chiffres
    de référence ; le juge s'y calibre.
  la porte 0 : la fonction `porte_0` du juge, qui refuse une fiche incomplète.
"""
import csv
import os
import subprocess
import sys

sys.dont_write_bytecode = True

REGLAGES = ("tp", "sl", "horizon", "univers")


def arreter(message):
    """Affiche un motif d'arrêt et rend le code d'échec.

    ① RÔLE — Donner une seule forme à tous les arrêts.
    ② CONTEXTE D'APPEL — `main`, à chaque condition manquée.
    ③ ENTRÉE — `message` : le motif, en français.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : l'entier 1.
      [rend: 1]
    ⑥ TRAITEMENT — ① afficher « ARRÊT : » et le motif · ② rendre 1.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un arrêt doit se lire sans ambiguïté sur un téléphone.
    ⑨ CE QUI CLOCHE — Rien vu.
    ⑩ EFFET — Une ligne affichée.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    print("ARRÊT : %s" % message)
    return 1


def codes(texte):
    """Découpe un univers comme le juge le découpe.

    ① RÔLE — Comparer deux univers sans dépendre de l'ordre ni des espaces.
    ② CONTEXTE D'APPEL — `controler_fusion`, deux fois par version.
    ③ ENTRÉE — `texte` : un univers écrit « TTE,ENGI,... ».
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste TRIÉE des codes en majuscules, doublons gardés.
      [rend: 1]
    ⑥ TRAITEMENT — ① couper sur la virgule · ② retirer les espaces · ③ mettre en
      majuscules · ④ écarter le vide.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — `jouer` découpe exactement ainsi (ligne `demandes = ...`). Une
      liste et non un ensemble : un ensemble effaçait un doublon « TTE,TTE », que
      `jouer` joue deux fois (relecture du 08-10-2026, défaut N4).
    ⑨ CE QUI CLOCHE — C'est une seconde écriture de ce découpage : si le juge
      change le sien, celui-ci ne suivra pas. Le juge n'expose pas de fonction
      à appeler.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    return sorted(x.strip().upper() for x in (texte or "").split(",") if x.strip())


def fusionner(fiche, version):
    """Rend une copie de la fiche portant les réglages de la version.

    ① RÔLE — Fabriquer la fiche jouable d'une version.
    ② CONTEXTE D'APPEL — `main`, une fois par version.
    ③ ENTRÉE — `fiche` : la ligne du registre · `version` : la ligne de la
      combinatoire.
    ④ CONDITIONS D'ENTRÉE — Les deux portent tp, sl, horizon et univers.
    ⑤ SORTIE — UNE valeur : la fiche fusionnée, un nouveau dictionnaire.
      [rend: 1]
    ⑥ TRAITEMENT — ① copier la fiche · ② y remplacer tp, sl, horizon, univers ·
      ③ poser `_fonction_signal`.
    ⑦ UNITÉ — tp et sl en fractions ; horizon en séances.
    ⑧ POURQUOI — DECLINER le prescrit dans son en-tête : la version ne porte que
      ce qui varie, le reste vient de la fiche.
    ⑨ CE QUI CLOCHE — Le nom de la fonction de signal est écrit ici (A-542).
    ⑩ EFFET — Aucun : la fiche d'origine n'est pas modifiée.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    f = dict(fiche)
    for k in REGLAGES:
        f[k] = version[k]
    f["_fonction_signal"] = "signaux_c5etendu10"
    return f


def controler_fusion(J, fusion, version):
    """Vérifie que le juge lira bien les réglages de la version.

    ① RÔLE — Empêcher qu'une case oubliée à la fusion produise un résultat faux
      sans alerte.
    ② CONTEXTE D'APPEL — `main`, une fois par version, avant de la jouer.
    ③ ENTRÉE — `J` : le module du juge · `fusion` : la fiche fusionnée ·
      `version` : la ligne de la combinatoire.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des écarts, vide si tout concorde.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire tp et sl par `pourcent` du juge et les comparer à la
      version · ② lire l'horizon par `lire_horizon` · ③ comparer les univers.
    ⑦ UNITÉ — Fractions ; séances.
    ⑧ POURQUOI — Relecture du 08-10-2026 (défaut A2) : une fusion qui oubliait
      l'horizon écrivait 125 842,31 € pour une version à 5 séances, au lieu de
      73 093,64 €, sans aucune alerte.
    ⑨ CE QUI CLOCHE — Rien vu.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; `pourcent` et `lire_horizon` peuvent lever sur
      une case illisible.
      [sort: non]
    """
    ecarts = []
    for k in ("tp", "sl"):
        if abs(J.pourcent(fusion[k]) - float(version[k])) > 1e-12:
            ecarts.append("%s lu %r, version %r" % (k, fusion[k], version[k]))
    if J.lire_horizon(fusion["horizon"]) != int(version["horizon"]):
        ecarts.append("horizon lu %r, version %r" % (fusion["horizon"], version["horizon"]))
    if codes(fusion["univers"]) != codes(version["univers"]):
        ecarts.append("univers lu %r, version %r" % (fusion["univers"], version["univers"]))
    return ecarts


def calibrer_par_le_juge(base, ident):
    """Lance le juge seul sur la fiche et lit son verdict.

    ① RÔLE — Prouver que l'instrument retrouve les chiffres de référence avant de
      jouer quoi que ce soit.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `base` : la racine du dépôt · `ident` : l'identifiant de la fiche.
    ④ CONDITIONS D'ENTRÉE — Le juge est dans `programmes/` sous la racine.
    ⑤ SORTIE — DEUX valeurs : vrai si le juge est calibré et rend 0 ; la ligne de
      résultat qu'il affiche pour la fiche, ou None.
      [rend: 2]
    ⑥ TRAITEMENT — ① lancer le juge avec l'identifiant · ② exiger le code 0, la
      phrase « calibrage sur le TEMOIN du golden » et la phrase « OK, l'instrument
      est calibre » · ③ relever la ligne
      « N operations . X % de reussite . G EUR ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le calibrage du juge compare au tableau des 100 opérations de
      référence, sur le témoin du golden. Le refaire ici serait une seconde
      écriture (R-708). Le témoin est exigé : sans lui, le juge ne compare plus
      que le nombre d'opérations et se dit quand même calibré (défaut N2).
    ⑨ CE QUI CLOCHE — Ce calibrage ne porte que sur les réglages de la fiche ; les
      autres réglages sont protégés par le témoin de résultats (voir `main`).
      Dépend du texte affiché par le juge : s'il change sa phrase,
      ce contrôle s'arrête (il rougit, il ne se tait pas).
    ⑩ EFFET — Lance un processus avec `-B`, pour que Python n'écrive pas de
      fichiers compilés ; le juge lui-même n'écrit aucun fichier.
    ⑪ TERMINAISON — Rend la main ; le processus lancé n'a pas de limite de temps.
      [sort: non]
    """
    p = subprocess.run([sys.executable, "-B", os.path.join(base, "programmes", "JUGE_DES_STRATEGIES.py"),
                        base, ident], capture_output=True, text=True)
    sortie = p.stdout + p.stderr
    ok = (p.returncode == 0 and "OK, l'instrument est calibre" in sortie
          and "calibrage sur le TEMOIN du golden" in sortie)
    ligne = next((l.strip() for l in sortie.splitlines()
                  if "operations ." in l and "de reussite" in l and "EUR" in l), None)
    return ok, ligne


def bareme_du_temoin(f_comb, sid, essai):
    """Dit sous quel barème des frais le témoin de résultats a été fait, ou None sans témoin.

    ① RÔLE — Lire l'étiquette de barème du témoin (A-550, superviseur R-759, C15, 29-10-2026).
    ② CONTEXTE D'APPEL — `main`, une fois, avant de jouer les versions.
    ③ ENTRÉE — `f_comb` : la combinatoire · `sid`, `essai` : la stratégie et l'essai.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nom du barème (une ligne de `donnees/BAREME_FRAIS.csv`), ou None s'il
      n'y a pas de témoin.
      [rend: 1]
    ⑥ TRAITEMENT — ① chercher le témoin à côté de la combinatoire · ② lire sa colonne `bareme` ·
      ③ exiger UNE seule valeur, non vide, sur toutes les lignes.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un montant ne se vérifie qu'avec le barème qui l'a produit (ÉTUDE 18, A1bis). Le
      témoin de C5E10-OBS-V1 E01 a été fait au courtage seul, avant la taxe : sans son étiquette, la
      moulinette, passée au barème réel, ne le retrouvait plus (mesuré le 29-10-2026 : version 0914,
      gain 71 855,72 € au lieu de 97 155,72 €) et s'arrêtait. Le superviseur a refusé de REMPLACER le
      témoin (une référence de calibrage ne se réécrit pas) : il est GARDÉ et ÉTIQUETÉ.
    ⑨ CE QUI CLOCHE — Un témoin sans colonne `bareme` arrête la moulinette (ValueError) : c'est voulu,
      un témoin sans barème ne prouve rien.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ; lève ValueError si l'étiquette manque ou varie.
      [sort: non]
    """
    f_tem = os.path.join(os.path.dirname(f_comb), "TEMOIN_RESULTATS_%s_%s.csv" % (sid, essai))
    if not os.path.exists(f_tem):
        return None
    vals = {(r.get("bareme") or "").strip() for r in csv.DictReader(open(f_tem, encoding="utf-8-sig"))}
    if len(vals) != 1 or "" in vals:
        raise ValueError("le témoin %s ne dit pas sous quel barème des frais il a été fait (colonne "
                         "« bareme », une seule valeur) : %r" % (os.path.basename(f_tem), sorted(vals)))
    return vals.pop()


def comparer_au_temoin(f_comb, sid, essai, f_resultats):
    """Compare les résultats d'un lancement au témoin de résultats, s'il existe.

    ① RÔLE — Protéger les réglages que le calibrage du juge ne touche pas : il ne
      rejoue que les réglages de la fiche.
    ② CONTEXTE D'APPEL — `main`, une fois, après avoir joué toutes les versions.
    ③ ENTRÉE — `f_comb` : la combinatoire · `sid`, `essai` : la stratégie et
      l'essai · `f_resultats` : le fichier provisoire qui vient d'être écrit, ou
      (depuis le 29-10-2026, C15) un dictionnaire id_version -> ligne, quand les
      versions ont été rejouées sous le barème du témoin.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des écarts, vide si tout concorde ou s'il
      n'y a pas de témoin.
      [rend: 1]
    ⑥ TRAITEMENT — ① chercher `TEMOIN_RESULTATS_<STRATÉGIE>_<ESSAI>.csv` à côté
      de la combinatoire · ② absent : l'annoncer et rendre une liste vide ·
      ③ présent : comparer, version par version, opérations, réussite exacte et
      gain net, et signaler toute version manquante ou en trop.
    ⑦ UNITÉ — Euros ; pourcents.
    ⑧ POURQUOI — Relecture du 08-10-2026, défaut N1 : l'ordre des tests de sortie
      inversé dans le module de positions laissait le juge calibré, la fiche
      inchangée, et faisait passer la version tp 2 % / sl 1,5 % de 25 495,70 € à
      28 990,45 € sans alerte.
    ⑨ CE QUI CLOCHE — Un témoin absent ne protège rien : c'est annoncé à l'écran,
      pas refusé. Un témoin se fige sur décision de Jean-Luc ; une révision des
      cours passés par ABC fera aussi rougir la comparaison, ce qui est voulu.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS
      le témoin de résultats : une copie figée des résultats d'un lancement jugé
        bon, rangée à côté de la combinatoire, qui sert de référence aux suivants.
    """
    f_tem = os.path.join(os.path.dirname(f_comb), "TEMOIN_RESULTATS_%s_%s.csv" % (sid, essai))
    if not os.path.exists(f_tem):
        print("AUCUN TÉMOIN DE RÉSULTATS (%s) : seuls les réglages de la fiche sont"
              " protégés par le calibrage." % os.path.basename(f_tem))
        return []
    champs = ("operations", "reussite_pourcents_exacte", "gain_net_euros")
    tem = {r["id_version"]: r for r in csv.DictReader(open(f_tem, encoding="utf-8-sig"))}
    # `f_resultats` : un fichier de résultats, OU un dictionnaire id_version -> ligne, quand la comparaison se fait
    # sous le barème du témoin et non sous celui des résultats écrits (C15, 29-10-2026).
    res = f_resultats if isinstance(f_resultats, dict) else \
        {r["id_version"]: r for r in csv.DictReader(open(f_resultats, encoding="utf-8"))}
    ecarts = ["%s absente du témoin" % k for k in sorted(set(res) - set(tem))]
    ecarts += ["%s absente des résultats" % k for k in sorted(set(tem) - set(res))]
    for k in sorted(set(res) & set(tem)):
        for c in champs:
            if res[k].get(c) != tem[k].get(c):
                ecarts.append("%s %s : %s au lieu de %s" % (k, c, res[k].get(c), tem[k].get(c)))
    print("TÉMOIN DE RÉSULTATS : %d versions comparées, %d écarts" % (len(tem), len(ecarts)))
    return ecarts


def main():
    """Contrôle, calibre, puis joue toutes les versions.

    ① RÔLE — Point d'entrée du programme.
    ② CONTEXTE D'APPEL — Le lancement, et lui seul.
    ③ ENTRÉE — La ligne de commande (voir l'en-tête).
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête, ④.
    ⑤ SORTIE — UNE valeur : 0 ou 1, passée à la sortie du processus.
      [rend: 1]
    ⑥ TRAITEMENT — Voir l'en-tête, ⑥.
    ⑦ UNITÉ — Voir l'en-tête, ⑦.
    ⑧ POURQUOI — Voir l'en-tête, ⑧.
    ⑨ CE QUI CLOCHE — Voir l'en-tête, ⑨.
    ⑩ EFFET — Crée le fichier de résultats.
    ⑪ TERMINAISON — Rend la main ; une exception imprévue efface le fichier
      provisoire puis remonte.
      [sort: non]
    """
    if len(sys.argv) != 4:
        print(__doc__.split("①")[0])
        return 1
    base, f_comb, f_out = (os.path.abspath(a) for a in sys.argv[1:])
    if os.path.exists(f_out):
        return arreter("le fichier de résultats existe déjà : %s" % f_out)

    versions = list(csv.DictReader(open(f_comb, encoding="utf-8-sig")))
    if not versions:
        return arreter("la combinatoire est vide")
    strats = {v["strategie"] for v in versions}
    essais = {v["essai"] for v in versions}
    if len(strats) != 1 or len(essais) != 1:
        return arreter("plusieurs stratégies ou essais dans la combinatoire : %s %s"
                       % (sorted(strats), sorted(essais)))
    ids = [v["id_version"] for v in versions]
    if len(set(ids)) != len(ids):
        return arreter("identifiants de version en double")
    annonces = {v["versions_dans_l_essai"] for v in versions}
    if annonces != {str(len(versions))}:
        return arreter("la combinatoire annonce %s versions et en porte %d"
                       % (sorted(annonces), len(versions)))
    vides = [v["id_version"] for v in versions if not codes(v["univers"])]
    if vides:
        # « , » passe la porte 0 et se joue avec zéro opération, sans alerte
        # (relecture du 08-10-2026, défaut N7).
        return arreter("univers vide pour %s" % vides[:5])
    doubles = [v["id_version"] for v in versions if len(set(codes(v["univers"]))) != len(codes(v["univers"]))]
    if doubles:
        # `jouer` joue un code autant de fois qu'il est écrit : « TTE,TTE » double
        # les opérations (relecture du 08-10-2026, défaut N4).
        return arreter("valeur écrite deux fois dans l'univers de %s" % doubles[:5])
    ident_v = [v for v in versions if (v.get("version_de_la_fiche") or "").strip()]
    if len(ident_v) != 1:
        return arreter("%d versions marquées identiques à la fiche" % len(ident_v))
    sid, essai = strats.pop(), essais.pop()

    ok, ligne_juge = calibrer_par_le_juge(base, sid)
    print("CALIBRAGE PAR LE JUGE SEUL : %s" % ("OK" if ok else "ÉCHEC"))
    if not ok or not ligne_juge:
        return arreter("le juge des stratégies ne se calibre pas, ou n'a pas joué la fiche")
    print("  le juge affiche : %s" % ligne_juge)

    sys.path.insert(0, os.path.join(base, "programmes"))
    import JUGE_DES_STRATEGIES as J
    if os.path.dirname(os.path.abspath(J.__file__)) != os.path.join(base, "programmes"):
        return arreter("le juge importé n'est pas celui du dépôt : %s" % J.__file__)
    mnemo = J.table_mnemoniques(J.trouver(base, "REFERENTIEL_VALEURS"))
    # LES COURS PASSENT PAR LE LECTEUR UNIQUE, COMME DANS `main` DU JUGE (A-577, étape 1, 27-10-2026) : ce
    # programme se compare au juge, il lit donc comme lui — sinon le juge affiche 89 opérations et ce
    # programme 100 sur la même fiche (C5E10-OBS-V1, mesuré le 27-10-2026). Deux lectures divergent (R-708).
    try:   # le juge refuse lui-même une lecture qui a écarté des lignes (`lire_par_le_lecteur`, 27-10-2026)
        cours, lecture = J.lire_par_le_lecteur(base, os.path.relpath(J.fichiers_de_cours(base)[0], base), mnemo)
    except ValueError as e:
        if not str(e).startswith("le lecteur unique"):
            raise
        return arreter(str(e))
    mod_sig = J.charger_module(J.trouver(base, "MODULE_C5_ETENDU_10"), "sig")
    mod_pos = J.charger_module(J.trouver(base, "MODULE_POSITIONS.py"), "pos")
    fiches = [f for f in csv.DictReader(open(J.trouver(base, "cac40_strategies.csv"),
                                             encoding="utf-8-sig")) if f["id"] == sid]
    if len(fiches) != 1:
        return arreter("fiche %s trouvée %d fois au registre" % (sid, len(fiches)))
    fiche = fiches[0]

    def jouer_une(f, bareme=None, ops_rendues=None):
        """Fait passer une fiche par la porte 0 puis la joue.

        ① RÔLE — Un seul chemin de jeu pour la fiche, la version identique et
          toutes les versions.
        ② CONTEXTE D'APPEL — `main`, une fois par fiche à jouer.
        ③ ENTRÉE — `f` : une fiche, d'origine ou fusionnée · `bareme` : None pour le
          barème des trades vécus, sinon le nom d'un barème (celui du témoin, C15) ·
          `ops_rendues` : une liste où recopier les opérations jouées, ou None.
        ④ CONDITIONS D'ENTRÉE — Les cours, le référentiel et les deux modules sont
          chargés par `main`.
        ⑤ SORTIE — DEUX valeurs : le résumé rendu par `resumer` du juge ; les bornes
          de la période rendues par la porte 0.
          [rend: 2]
        ⑥ TRAITEMENT — ① porte 0 · ② poser la fonction de signal si absente ·
          ③ `jouer` sur la période · ④ refuser une valeur absente des cours ·
          ⑤ résumer.
        ⑦ UNITÉ — Euros ; pourcents ; dates AAAA-MM-JJ.
        ⑧ POURQUOI — Le même appel que `main` du juge, ligne `ops, inconnus = jouer(...)`.
        ⑨ CE QUI CLOCHE — Rien vu.
        ⑩ EFFET — Pose `_fonction_signal` dans la fiche reçue si elle ne l'a pas.
        ⑪ TERMINAISON — Rend la main, ou lève ValueError sur un refus.
          [sort: non]
        ⑫ DÉFINITIONS
          la porte 0 : la fonction `porte_0` du juge, qui refuse une fiche incomplète.
        """
        ok0, manq, bornes = J.porte_0(f)
        if not ok0:
            raise ValueError("la porte 0 refuse : %s" % manq)
        f.setdefault("_fonction_signal", "signaux_c5etendu10")
        if bareme is None:
            ops, inconnus = J.jouer(f, cours, mnemo, mod_sig, mod_pos, periode=bornes, lecture=lecture)
        else:
            ops, inconnus = J.jouer(f, cours, mnemo, mod_sig, mod_pos, periode=bornes, lecture=lecture,
                                    bareme=bareme)
        if ops_rendues is not None:
            ops_rendues.extend(ops)
        if inconnus:
            raise ValueError("valeurs absentes des cours : %s" % inconnus)
        return J.resumer(ops), bornes

    ref, bornes = jouer_une(dict(fiche))
    if ref["n"] == 0:
        return arreter("la fiche elle-même ne produit aucune opération")
    texte_ref = "{} operations . {} % de reussite . {:+,.2f} EUR".format(ref["n"], ref["wr"], ref["net"])
    print("  ce programme : %s" % texte_ref)
    if texte_ref != ligne_juge:
        return arreter("ce programme et le juge seul ne rendent pas la même chose pour la fiche")
    r_id, _ = jouer_une(fusionner(fiche, ident_v[0]))
    if (r_id["n"], r_id.get("wr_exact"), r_id.get("net")) != (ref["n"], ref["wr_exact"], ref["net"]):
        return arreter("la version %s, identique à la fiche, ne retrouve pas la fiche"
                       % ident_v[0]["id_version"])
    print("  version identique %s : même résultat" % ident_v[0]["id_version"])

    # LA MARGE SE COMPTE VALEUR PAR VALEUR : compter les séances de toutes les
    # valeurs laissait passer un univers dont les cours s'arrêtaient trois séances
    # après la période (relecture du 08-10-2026, défaut N3). Une opération ouverte
    # en fin de période serait alors close avant son horizon, sans alerte.
    h_max = max(int(v["horizon"]) for v in versions)
    marge = {}
    for m in sorted({c for v in versions for c in codes(v["univers"])}):
        cle = mnemo.get(m, J.cle_valeur(m))
        marge[m] = sum(1 for b in cours.get(cle, []) if b["date"] > bornes[1])
    plus_court = min(marge, key=marge.get)
    print("PÉRIODE JOUÉE : %s -> %s · marge la plus courte : %s, %d séances après la fin"
          " · horizon max %d" % (bornes[0], bornes[1], plus_court, marge[plus_court], h_max))
    if marge[plus_court] < h_max + 1:
        return arreter("pas assez de cours après la période pour %s et l'horizon %d"
                       % (plus_court, h_max))

    champs = ["id_version", "strategie", "essai", "versions_dans_l_essai", "tp", "sl",
              "horizon", "univers", "periode_debut", "periode_fin", "operations",
              "reussite_pourcents_exacte", "gain_net_euros", "bareme"]
    # LE TÉMOIN SE COMPARE SOUS SON PROPRE BARÈME (C15, 29-10-2026) : chaque version est jouée deux fois quand le
    # témoin a été fait sous un autre barème que celui des résultats — sous le barème des verdicts pour les résultats
    # écrits, sous celui du témoin pour la comparaison — et l'écart entre les deux doit être EXACTEMENT la taxe
    # payée à l'achat (mêmes opérations ; un achat revendu le jour même ne paie pas la taxe). L'écart n'est la taxe
    # que si les deux barèmes ne diffèrent QUE par elle (courtage seul contre réel) : sinon, arrêt, et c'est voulu.
    b_tem = bareme_du_temoin(f_comb, sid, essai)
    # Les résultats se chiffrent sous le BARÈME DES VERDICTS (le défaut du juge, `MODULE_POSITIONS.BAREME_DES_VERDICTS`,
    # superviseur R-759 tour 2, D2) ; le témoin n'est rejoué à part que s'il a été fait sous un autre barème.
    b_res = J.bareme_des_verdicts(None, mod_pos)
    rejouer = b_tem is not None and b_tem != b_res
    vue_du_temoin, invariant_faux = {}, []
    if b_tem is not None:
        print("TÉMOIN FAIT SOUS LE BARÈME %s%s" % (b_tem, " : chaque version est aussi rejouée sous ce barème"
                                                   if rejouer else ""))
    provisoire = f_out + ".en_cours"
    cree = False  # on n'efface que ce qu'on a créé (relecture du 08-10-2026, N5)
    try:
        with open(provisoire, "x", encoding="utf-8", newline="") as s:
            cree = True
            w = csv.DictWriter(s, fieldnames=champs)
            w.writeheader()
            for i, v in enumerate(versions, 1):
                fusion = fusionner(fiche, v)
                ecarts = controler_fusion(J, fusion, v)
                if ecarts:
                    raise ValueError("fusion fausse pour %s : %s" % (v["id_version"], ecarts))
                ops_r = []
                r, b = jouer_une(fusion, None, ops_r)
                if b != bornes:
                    raise ValueError("période différente pour %s : %s" % (v["id_version"], b))
                if rejouer:
                    ops_t = []
                    r_t, _ = jouer_une(fusion, b_tem, ops_t)
                    vue_du_temoin[v["id_version"]] = {
                        "operations": str(r_t["n"]),
                        "reussite_pourcents_exacte": "%.6f" % r_t["wr_exact"] if r_t["n"] else "",
                        "gain_net_euros": "%.2f" % r_t["net"] if r_t["n"] else "0.00"}
                    cle_op = lambda o: (o["valeur"], o["date_signal"], o["date_sortie"], o["motif"], o["px"])
                    # la taxe payée sous un barème : achats non revendus le jour même (BOFiP, BOI-TCA-FIN-10-10, § 60)
                    taxe_de = lambda bar: sum(
                        mod_pos.cout_d_un_ordre(o["valeur"], o["date_entree"], "achat", 100000.0, bar)["taxe"]
                        for o in ops_r if o["date_entree"] != o["date_sortie"])
                    # le gain sous le barème du témoin moins le gain sous celui des résultats = ce que les résultats
                    # paient de taxe en plus (négatif si c'est le témoin qui la paie)
                    taxes = taxe_de(b_res) - taxe_de(b_tem)
                    ecart = sum(o["net"] for o in ops_t) - sum(o["net"] for o in ops_r)
                    if [cle_op(o) for o in ops_t] != [cle_op(o) for o in ops_r] or abs(ecart - taxes) > 0.01:
                        invariant_faux.append("%s : écart %.2f € pour %.2f € de taxe" % (v["id_version"], ecart, taxes))
                w.writerow({"id_version": v["id_version"], "strategie": sid, "essai": essai,
                            "versions_dans_l_essai": len(versions), "tp": v["tp"], "sl": v["sl"],
                            "horizon": v["horizon"], "univers": v["univers"],
                            "periode_debut": bornes[0], "periode_fin": bornes[1],
                            "operations": r["n"],
                            "reussite_pourcents_exacte": "%.6f" % r["wr_exact"] if r["n"] else "",
                            "gain_net_euros": "%.2f" % r["net"] if r["n"] else "0.00",
                            "bareme": b_res})
                if i % 250 == 0:
                    print("  %d / %d" % (i, len(versions)), flush=True)
        if invariant_faux:
            print("L'ÉCART ENTRE LES DEUX BARÈMES N'EST PAS LA TAXE (%d) :" % len(invariant_faux))
            for e in invariant_faux[:10]:
                print("  %s" % e)
            os.remove(provisoire)
            return arreter("l'écart au témoin n'est pas expliqué par la taxe : rien n'est écrit")
        ecarts = comparer_au_temoin(f_comb, sid, essai, vue_du_temoin if rejouer else provisoire)
        if ecarts:
            print("ÉCARTS AVEC LE TÉMOIN DE RÉSULTATS (%d) :" % len(ecarts))
            for e in ecarts[:10]:
                print("  %s" % e)
            os.remove(provisoire)
            return arreter("les résultats ne retrouvent pas le témoin : rien n'est écrit")
    except BaseException:
        if cree and os.path.exists(provisoire):
            os.remove(provisoire)
        raise
    os.replace(provisoire, f_out)
    print("ÉCRIT : %s · %d versions" % (f_out, len(versions)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
