#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JOUER_LES_VERSIONS.py — Jeu 08-10-2026 (Paris)
EN ESSAI · outil · Rôle : rejouer chaque version d'une combinatoire avec le vrai juge des stratégies.
Quand l'appeler : à la main, après DECLINER_LES_STRATEGIES.

USAGE
    python3 JOUER_LES_VERSIONS.py <racine_du_depot> <combinatoire> <fichier_resultats> [--cours=<fichier>]
    exemple :
    python3 programmes/JOUER_LES_VERSIONS.py . \
        donnees/combinatoires/COMBINATOIRE_C5E10-OBS-V1_E01.csv \
        donnees/combinatoires/RESULTATS_C5E10-OBS-V1_E01.csv
    --cours=<fichier, relatif à la racine> : jouer sur un autre fichier de cours que le
    fichier maître, par exemple l'historique des 20 ans (plan V7, bloc 5l ⑤) ; la même
    option que le juge des stratégies, lue et refusée de la même façon, et passée au
    juge pour son calibrage. Sans l'option, le fichier maître, comme avant.
    --essai-sans-regard : un ESSAI DÉCLARÉ (A-863, décision de Jean-Luc du 16-11-2026 à
    20h46), sans regard unique consommé ni inscription : refusé en 2 si la racine porte
    .git, si la combinatoire porte plus d'une version, si la fiche n'est identique à aucune
    fiche de CONTRATS.FICHES_DEJA_VUES_SUR_LE_REGARD_UNIQUE (`jeton_d_essai` du juge),
    si la version jouée n'a pas l'empreinte des réglages de la fiche (avant tout jeu), ou
    si elle ne retrouve pas la fiche (mineur M5 du relecteur neuf du 16-11-2026) ;
    chaque ligne écrite commence par « ESSAI — NI RÉSULTAT NI SÉLECTION », et le fichier
    de résultats porte la colonne `statut_d_essai`, que le tri refuse.

    --tranche=<k>/<N> (A-919, 19-11-2026) : ne jouer que la tranche k (0 … N-1) de la combinatoire,
    coupée en N parts contiguës dans l'ordre du fichier (la dernière peut être plus courte) ; la combinatoire
    reste ENTIÈRE et contrôlée entière, chaque ligne écrite porte `versions_dans_l_essai` = la combinatoire
    entière, et le témoin de résultats n'est comparé que sur les versions jouées ; l'assemblage le compare ENTIER
    (relecteur du 19-11-2026, I2). Un fichier de tranche ne se
    trie pas seul (le tri exige autant de lignes que `versions_dans_l_essai`) : il s'assemble.
    python3 JOUER_LES_VERSIONS.py --assembler <combinatoire> <fichier_resultats> <tranche> [<tranche> ...]
        [--cours=<fichier>] :
    réunit les fichiers de tranche en UN fichier de résultats, dans l'ordre de la combinatoire ; refuse (1)
    si une version manque ou est en double, si une colonne n'est pas celle du contrat, si une colonne
    commune au tri porte plus d'une valeur, si l'ensemble diffère du témoin de résultats entier, et, avec --cours=, si une tranche a été jouée sur
    un autre fichier de cours (A-1076, 27-11-2026). Raison : une moulinette entière dépasse les 10 minutes par appel
    (consigne du 19-11-2026) ; le découpage vit ICI, une seule fois (superviseur R-759 du 19-11-2026, R-708).

CE QUE CE PROGRAMME EST DANS LA CHAÎNE (action A-541 du BACKLOG)
    ⓪ PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES propose les réglages ;
    Jean-Luc valide · ① DECLINER_LES_STRATEGIES fabrique les versions ·
    ② CE PROGRAMME les rejoue en appelant `jouer` du juge des stratégies, sans rien
    recalculer lui-même · ③ TRIER_LES_VARIANTES (écrit le 11-11-2026, lit le fichier
    de résultats de ce programme) · ④ `juger`.

① RÔLE — Donner, pour chaque version figée d'une stratégie, le résultat qu'elle
  aurait eu sur la période de sa fiche : nombre d'opérations, réussite, gain net.
  C'est la matière que le tri et le jugement examineront.
② CONTEXTE D'APPEL — À la main, par le Chat. Aucune tâche automatique ne l'appelle.
③ ENTRÉE — La ligne de commande, trois arguments : la racine d'un dépôt (registre
  des stratégies, fichier maître des cours, référentiel, modules de signal et de
  positions, témoin du golden) ; une combinatoire écrite par DECLINER ; le chemin
  du fichier de résultats, qui ne doit pas exister. Une option facultative,
  `--cours=<fichier>` : le fichier de cours à jouer, relatif à la racine ; et
  `--essai-sans-regard` (voir l'usage) ; toute autre option, ou celle-ci mal écrite,
  arrête tout (comme le juge, 27-10-2026).
④ CONDITIONS D'ENTRÉE — ① la combinatoire n'est pas vide, toutes ses lignes
  portent la même stratégie et le même essai, ses identifiants sont uniques, et
  son nombre de lignes égale la colonne `versions_dans_l_essai`, aucun univers
  n'écrit deux fois la même valeur · ② une seule
  version y est marquée identique à la fiche · ③ la fiche existe au registre (sa
  DERNIÈRE ligne fait foi, n°83) ; elle et CHAQUE version fusionnée suivent le
  contrat de stratégie (A-923 ; les versions depuis le 20-11-2026) · ④ le juge des stratégies, lancé seul sur cette fiche, se calibre sur
  le témoin du golden et rend le même résultat que ce programme · ⑤ chaque
  version, une fois fusionnée, est lue par le juge avec ses propres réglages ·
  ⑥ les cours de CHAQUE valeur vont assez loin après le début de la période pour
  laisser, après la FIN CALCULÉE (voir ⑥ du traitement), l'horizon CHIFFRÉ le plus long
  plus la séance d'achat (une durée « aucune » n'a pas d'échéance : aucune marge ne la
  couvre, elle est dite à l'écran ; ses positions encore ouvertes à la fin des cours sont
  mises à part, hors du total, depuis la décision de Jean-Luc du 12-11-2026 à 09h18, et
  comptées dans les deux colonnes « à part » des résultats) · ⑦ si un témoin de résultats
  existe, chaque version le retrouve · ⑧ le fichier nommé par `--cours=` existe ·
  ⑨ LA COUVERTURE (A-1076 ②, depuis le 27-11-2026) : la première séance des cours lus
  n'est pas plus d'un mois de calendrier après le début déclaré par la fiche, ni la
  dernière plus d'un mois avant sa fin (`couverture_des_cours`) ; la période et le
  nombre de séances réellement lus sont affichés à chaque lancement (ligne « COURS LUS »).
  Le moindre manquement arrête tout, avant ou pendant le jeu.
⑤ SORTIE — UNE valeur : le code de sortie, 0 quand toutes les versions sont
  jouées et écrites, 1 sinon (dont une fiche relue, depuis le 19-11-2026, ou une
  version fusionnée, depuis le 20-11-2026, qui ne suit pas le contrat de stratégie) ;
  2 quand le contrat n'a pas pu être contrôlé (R-734) — référentiel, MODULE_POSITIONS.py,
  barème des frais ou donnees/VALEURS_TTF.csv absents ou illisibles : depuis le
  20-11-2026, ce contrôle vient AVANT le calibrage, qui ne peut donc plus masquer
  ce 2 par un 1 ; 2 aussi pour un essai déclaré refusé (A-863).
  [rend: 1]
⑥ TRAITEMENT — ① lire la ligne de commande et contrôler la combinatoire ·
  ①bis (depuis le 20-11-2026, AVANT le calibrage) importer le juge du dépôt, lire la
  fiche par `fiches_du_registre` du contrat (sa DERNIÈRE ligne, n°83, depuis le
  05-11-2026), charger le module de positions, passer la fiche PUIS CHAQUE VERSION
  fusionnée au contrat de stratégie (`manques_du_contrat`, A-923 ;
  `refus_des_versions`) · ①ter (depuis le 27-11-2026, AVANT le calibrage) lire les cours par
  le lecteur unique du juge, afficher la période et le nombre de séances lus, et refuser une
  couverture insuffisante (`couverture_des_cours`, A-1076) · ② lancer
  le juge des stratégies seul sur la fiche (avec le même `--cours=`) et exiger son
  calibrage · ③ charger les modules
  par les fonctions du juge · ④ jouer la fiche telle quelle et exiger le résultat
  que le juge vient d'afficher · ⑤ jouer la version identique et exiger le même
  résultat · ⑥ CALCULER LA FIN DE PÉRIODE UTILISABLE (`fin_utilisable`, plan V7,
  bloc 5g) : la plus tardive des dates, au plus la fin écrite dans la fiche, qui
  laisse à CHAQUE valeur jouée au moins « horizon le plus long + 1 » séances
  après elle ; puis recompter cette marge valeur par valeur ; si la fin calculée
  diffère de celle de la fiche, rejouer la fiche sur la période calculée ; refuser
  un recul de plus de séances que `recul_maximum` n'en permet (CALCULÉ depuis le 27-11-2026 : le délai chiffré le
  plus long des versions + 1, A-1100 ; il était lu dans un fichier provisoire de 26 séances) ;
  demander la frontière 70/30 à `frontiere_de_la_fiche` du module de jugement ·
  ⑦ pour chaque version : fusionner, contrôler la fusion, jouer sur la période
  calculée, la couper par la même coupure (`partie_de_reglage`), écrire une ligne
  dans un fichier provisoire — chiffres de la période entière ET, colonnes « _70 »,
  chiffres de la seule partie de réglage, les seules que le tri lit ; la version identique
  doit retrouver la fiche rejouée · ⑧ comparer au témoin de résultats s'il
  existe · ⑨ renommer le fichier provisoire en fichier final.
  OÙ VIT LA FIN CALCULÉE : dans la colonne `periode_fin` de chaque ligne du
  fichier de résultats (la fin réellement jouée) ; la fin écrite dans la fiche
  est recopiée à côté, colonne `fin_ecrite_dans_la_fiche`, et le fichier de
  cours joué dans `cours_joues`, avec son empreinte. LA FICHE N'EST JAMAIS MODIFIÉE.
⑦ UNITÉ — Gains en EUROS pour 100 000 € engagés par opération ; réussite en
  POURCENTS ; tp et sl en FRACTIONS du prix d'entrée ; horizon en SÉANCES ; depuis
  le 11-11-2026, sl peut valoir le mot « sans stop » et horizon le mot « aucune ».
⑧ POURQUOI — TOUT LE CALCUL RESTE DANS LE JUGE : deux implémentations d'une même
  chose divergent toujours (R-708). Le calibrage passe par le juge lancé seul,
  parce qu'un calibrage maison comparant deux appels du même code resterait vert
  si le code ou les données changeaient (relecture du 08-10-2026, défaut A1).
  La fusion est contrôlée version par version, parce que la version identique
  à la fiche ne peut pas révéler une case oubliée (défaut A2).
⑨ CE QUI CLOCHE — ① le calibrage du juge compare le nombre d'opérations et les
  sorties, pas les frais : des frais doublés passeraient (relecture du
  08-10-2026) ; seul le témoin de résultats les attrape, et sans témoin rien ne
  les attrape · ② le DÉBUT de la période jouée est celui de la fiche, pas la
  première séance du fichier de cours : sur un fichier qui commence plus tard
  (le fichier maître commence le 02-01-2024), `periode_debut` dit une date sans
  cours — c'est arrivé le 11-11-2026, résultats « 2000-01-03 » joués sur 2024-2026 ;
  la colonne `cours_joues` le rend visible, elle ne le corrige pas · ③ la fin
  calculée dépend de l'horizon le plus long DE CETTE COMBINATOIRE et des valeurs
  de SES univers : deux stratégies d'une même campagne peuvent donc avoir des
  fins différentes, alors que le bloc 5g ① veut une fin commune (question posée
  à Jean-Luc dans echanges/A_RELIRE_TRI.md) ; une valeur dont les cours
  s'arrêtent tôt (sortie de la cote) ramène la fin de TOUTES les versions — au
  plus de `recul_maximum` séances (délai chiffré le plus long + 1), au-delà le programme refuse en la nommant ·
  ④bis le juge, lui, ne lit pas la fin calculée (relecteur neuf, D10, question
  posée) : la partie de réglage est coupée sur les bornes de la FICHE, comme le
  juge les coupe, donc la frontière 70/30 est la même des deux côtés ; seuls les
  30 % diffèrent ·
  ④ un horizon « aucune » (COMMUN.lire_horizon_ou_aucune) n'a pas de marge
  définie : `int` lève, ce programme s'arrête · ⑤ le signal est celui
  que la fiche nomme (`module_signal`, `fonction_signal`, `reglages_signal`),
  lu par `signal_de_la_fiche` du juge — depuis le 30-10-2026 (A-542), il n'est
  plus forcé à `signaux_c5etendu10` ; une version ne fait pas varier le signal ·
  ⑥ la version à zéro
  opération porte un gain de 0, que le tri devra traiter à part.
⑩ EFFET — Crée le fichier de résultats, via un fichier provisoire `.en_cours`
  effacé en cas d'échec s'il a été créé par ce lancement. Rien d'autre n'est
  écrit : le juge est lancé avec `-B`.
⑪ TERMINAISON — Sort du programme avec le code 0, 1 ou 2 (voir ⑤). Le juge est lancé dans un
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
# LE RÉGLAGE « QUAND JOUER » DEVIENT UNE VARIABLE DE LA MOULINETTE (A-1079 ; lot W2e-FIX du 27-11-2026) : FACULTATIF,
# une combinatoire d'avant le 27-11-2026 ne porte pas sa colonne, et sa version garde alors celui de la fiche
# (« toujours » quand la fiche n'en dit rien) — ses résultats ne changent pas. Le nom vient de DECLINER, qui l'écrit.
REGLAGES_FACULTATIFS = ("quand_jouer",)
OPTION_COURS = "--cours="
# L'option de l'essai déclaré (A-863) ; son texte vit au contrat (CONTRATS.OPTION_D_ESSAI_SANS_REGARD), et `main` les
# confronte dès que l'option est lue : sans elle, ce programme n'importe rien de plus qu'avant.
OPTION_ESSAI = "--essai-sans-regard"
OPTION_TRANCHE = "--tranche="


def lire_la_tranche(arguments):
    """Rend (k, N) de `--tranche=k/N`, (None, None) sans l'option, ou lève ValueError.

    ① RÔLE — Lire l'option de tranche (A-919).
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `arguments` : `sys.argv[1:]` ; exemple réel `[…, "--tranche=2/5"]`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs.
    [rend: 2]
    ⑥ TRAITEMENT — une seule option, deux entiers, 0 ≤ k < N.
    ⑦ UNITÉ — des tranches.
    ⑧ POURQUOI — une tranche mal écrite ne doit pas jouer tout ou rien en silence (R-734).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — rend la main ou lève.
    [sort: non]
    """
    t = [a[len(OPTION_TRANCHE):] for a in arguments if a.startswith(OPTION_TRANCHE)]
    if not t:
        return None, None
    try:
        k, n = (int(x) for x in t[0].split("/"))
    except ValueError:
        raise ValueError("option %s mal écrite : %r (attendu k/N, deux entiers)" % (OPTION_TRANCHE, t[0]))
    if len(t) > 1 or not 0 <= k < n:
        raise ValueError("option %s : une seule fois, et 0 ≤ k < N (lu %s)" % (OPTION_TRANCHE, t))
    return k, n


def tranche(versions, k, n):
    """Rend la tranche k sur n de la liste, parts contiguës de taille ⌈len/n⌉.

    ① RÔLE — LE découpage, une fois (R-708).
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `versions` : la liste des versions de la combinatoire ; `k` : le rang de la tranche ; `n` : le nombre
      de tranches (exemple réel : 2695 versions, k = 2, n = 5).
    ④ CONDITIONS D'ENTRÉE — 0 ≤ k < n.
    ⑤ SORTIE — UNE liste.
    [rend: 1]
    ⑥ TRAITEMENT — tranche de liste.
    ⑦ UNITÉ — versions.
    ⑧ POURQUOI — parts disjointes dont la réunion est la combinatoire.
    ⑨ CE QUI CLOCHE — une tranche peut être vide si n dépasse le nombre de versions.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — rend la main.
    [sort: non]
    """
    taille = -(-len(versions) // n)
    return versions[k * taille:(k + 1) * taille]


def assembler(arguments):
    """Réunit des fichiers de tranche en un fichier de résultats ; rend le code de sortie.

    ① RÔLE — Refaire UN fichier de résultats, celui que le tri lit, à partir des tranches (A-919).
    ② CONTEXTE D'APPEL — `main`, sous `--assembler`.
    ③ ENTRÉE — `arguments` : la combinatoire, le fichier de sortie, puis les fichiers de tranche ; et, n'importe où,
      au plus une option `--cours=<fichier, relatif à la racine>` : le fichier de cours que les tranches DEVAIENT jouer
      (l'enchaîneur la passe depuis le 27-11-2026, lot L1, A-1076). Exemple réel :
      `--cours=temoins/TEMOIN_VINGT_ANS_2000_2026_COUPURE_2026-11-11_FIGE_Ven_13-11-2026_10h59.csv`.
    ④ CONDITIONS D'ENTRÉE — la sortie n'existe pas.
    ⑤ SORTIE — UNE valeur : 0 écrit, 1 refus.
    [rend: 1]
    ⑥ TRAITEMENT — ⓪ avec `--cours=` : exiger que la colonne `cours_joues` de CHAQUE ligne de chaque tranche nomme ce
    fichier (une tranche jouée sur d'autres cours est refusée, en nommant le fichier lu) ; sans l'option, rien de plus
    qu'avant (les tranches doivent seulement s'accorder entre elles, ④) ·
    ① exiger les champs du contrat dans chaque tranche · ② refuser une version en double ou hors de
    la combinatoire · ③ refuser une version de la combinatoire sans résultat (une tranche perdue rougit ICI) ·
    ④ exiger `versions_dans_l_essai` = la combinatoire entière et une seule valeur par colonne commune au tri ·
    ⑤ comparer l'ensemble au témoin de résultats ENTIER, sans filtre d'identifiants (`comparer_au_temoin` ; sous un
    autre barème que le témoin, les identifiants seuls) · ⑥ écrire dans l'ordre de la combinatoire, par un fichier
    provisoire renommé.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — le tri exige un fichier par essai.
    ⑨ CE QUI CLOCHE — les chiffres ne sont pas rejoués : l'assemblage recopie. `--cours=` compare des NOMS de
    fichier (chemins normalisés), pas les octets : l'empreinte des cours est gardée par la porte du juge
    (VERIFIER_LA_CHAINE.motifs, `empreinte_des_cours_jusqu_a`).
    ⑩ EFFET — Écrit la sortie.
    ⑪ TERMINAISON — rend la main.
    [sort: non]
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import CONTRATS_DES_FICHIERS as C
    # LE FICHIER DE COURS ATTENDU (A-1076, lot L1) : lu et refusé comme dans `main` (`lire_la_ligne_de_commande`).
    attendu = [a[len(OPTION_COURS):] for a in arguments if a.startswith(OPTION_COURS)]
    arguments = [a for a in arguments if not a.startswith(OPTION_COURS)]
    if len(attendu) > 1 or (attendu and not attendu[0]) or any(a.startswith("--") for a in arguments):
        return arreter("--assembler : au plus une option « --cours=<fichier> », aucune autre option (lu %s)"
                       % (attendu + [a for a in arguments if a.startswith("--")]))
    if len(arguments) < 3:
        return arreter("--assembler <combinatoire> <fichier_resultats> <tranche> [<tranche> ...]")
    f_comb, f_out, tranches = arguments[0], arguments[1], arguments[2:]
    if os.path.exists(f_out):
        return arreter("le fichier de résultats existe déjà : %s" % f_out)
    ids = [v["id_version"] for v in csv.DictReader(open(f_comb, encoding="utf-8-sig"))]
    vus = {}
    for f in tranches:
        lecteur = csv.DictReader(open(f, encoding="utf-8"))
        if lecteur.fieldnames != list(C.RESULTATS_DES_VERSIONS):
            return arreter("%s : colonnes différentes du contrat RESULTATS_DES_VERSIONS" % f)
        for r in lecteur:
            if r["id_version"] in vus:
                return arreter("%s en double (%s)" % (r["id_version"], f))
            if attendu and os.path.normpath(r["cours_joues"]) != os.path.normpath(attendu[0]):
                return arreter("%s : la version %s a été jouée sur %s, pas sur %s (--cours=) — une tranche jouée sur "
                               "d'autres cours ne s'assemble pas (A-1076)" % (f, r["id_version"], r["cours_joues"],
                                                                            attendu[0]))
            vus[r["id_version"]] = r
    hors, manque = sorted(set(vus) - set(ids)), [i for i in ids if i not in vus]
    if hors or manque:
        return arreter("%d versions hors de la combinatoire (%s) · %d versions de la combinatoire sans résultat (%s)"
                       " : une tranche manque ou est de trop" % (len(hors), hors[:3], len(manque), manque[:3]))
    communes = {c: {r[c] for r in vus.values()} for c in C.COLONNES_COMMUNES_A_UN_TRI + ("versions_dans_l_essai",)}
    if any(len(v) != 1 for v in communes.values()) or communes["versions_dans_l_essai"] != {str(len(ids))}:
        return arreter("conditions de jeu différentes d'une tranche à l'autre : %s"
                       % {c: sorted(v) for c, v in communes.items() if len(v) != 1})
    # LE TÉMOIN ENTIER, UNE FOIS, SUR L'ENSEMBLE (relecteur du 19-11-2026, I2 ; superviseur R-759, ④) : sous --tranche,
    # chaque tranche ne s'est comparée qu'à ses versions — une version du témoin hors de la combinatoire n'y était plus
    # jamais signalée. Ici, aucun filtre d'identifiants. Sous le barème du témoin, les chiffres se comparent aussi ; sous
    # un autre barème, seuls les identifiants (les chiffres ont été comparés tranche par tranche, sous le bon barème).
    paire = {(r["strategie"], r["essai"]) for r in vus.values()}
    if len(paire) != 1:
        return arreter("stratégie ou essai différents d'une tranche à l'autre : %s" % sorted(paire))
    sid, essai = paire.pop()
    try:
        b_tem = bareme_du_temoin(f_comb, sid, essai)
    except ValueError as e:
        return arreter(str(e))
    if b_tem is None or b_tem == communes["bareme"].copy().pop():
        ecarts = comparer_au_temoin(f_comb, sid, essai, vus)
    else:
        ecarts = comparer_au_temoin(f_comb, sid, essai, vus, chiffres=False)
    if ecarts:
        return arreter("l'ensemble assemblé diffère du témoin de résultats entier (%d écarts) : %s"
                       % (len(ecarts), " · ".join(ecarts[:5])))
    with open(f_out + ".en_cours", "x", encoding="utf-8", newline="") as s:
        w = csv.DictWriter(s, fieldnames=list(C.RESULTATS_DES_VERSIONS))
        w.writeheader()
        w.writerows(vus[i] for i in ids)
    os.replace(f_out + ".en_cours", f_out)
    print("ASSEMBLÉ : %s · %d versions de %d tranches" % (f_out, len(ids), len(tranches)))
    return 0
# D'OÙ VIENT LE RECUL MAXIMUM (A-1100) : il était lu, jusqu'au 27-11-2026, dans
# donnees/combinatoires/RECUL_MAXIMUM_DE_LA_FIN.csv (26 séances, « PROVISOIRE, À DÉCIDER PAR JEAN-LUC », posé par
# l'agent TRI le 11-11-2026) ; il est désormais CALCULÉ (`recul_maximum`). Le fichier n'est plus lu ; il n'est ni effacé
# ni déplacé ici (rien ne se supprime sans validation).
DECISION_DU_RECUL = ("A-1100, Jean-Luc, 27-11-2026 à 19h29, « 1 » : le recul est calculé = le délai le plus long de la "
                     "liste des versions + 1 (la séance d'achat)")


def recul_maximum(horizon_max):
    """Rend de combien de séances, au plus, la fin calculée peut reculer : le délai chiffré le plus long + 1.

    ① RÔLE — Borner le recul de la fin calculée par un chiffre CALCULÉ sur la liste des versions, jamais écrit à la
      main (A-1100).
    ② CONTEXTE D'APPEL — `main`, une fois, juste après le calcul de la fin ; les épreuves, par import.
    ③ ENTRÉE — `horizon_max` : le délai (durée) CHIFFRÉ le plus long des versions de la combinatoire, en séances,
      tel que `main` le calcule (`h_max`) : les versions « sans délai » (horizon AUCUNE, A-645) n'y comptent pas ;
      0 quand aucune version n'a de délai chiffré. Exemple réel : la combinatoire d'IND-001-RETEST E01 (délais de 3 à
      25 séances, décision du 08-10-2026) → 25.
    ④ CONDITIONS D'ENTRÉE — `horizon_max` est un entier positif ou nul.
    ⑤ SORTIE — UNE valeur : le recul maximum, en séances (exemple réel : 25 → 26, la valeur que le fichier provisoire
      portait).
      [rend: 1]
    ⑥ TRAITEMENT — `horizon_max + 1`.
    ⑦ UNITÉ — Des séances (dates de cours distinctes des valeurs jouées, comme `recul_en_seances`).
    ⑧ POURQUOI — Décision de Jean-Luc du 27-11-2026 à 19h29 (A-1100, « 1 ») : « un chiffre qui se calcule ne s'écrit
      pas à la main » (R-728) ; 26 = 25 (délai le plus long, décision du 08-10-2026) + 1 (la séance d'achat). La fin
      calculée recule normalement d'au plus ce nombre de séances quand le fichier de cours s'arrête à la fin de la
      fiche ; au-delà, c'est qu'une valeur s'arrête tôt (sortie de la cote, trou) : `main` refuse en la nommant
      (relecteur neuf du 11-11-2026, D6).
    ⑨ CE QUI CLOCHE — ① La protection « un horizon absurde (250 au lieu de 25) fait refuser » que donnait le chiffre
      fixe DISPARAÎT : le recul permis grandit avec le délai le plus long ; un délai faux ne se voit plus qu'au contrôle
      des réglages validés par Jean-Luc (⓪). ② « + 1 » est aussi le besoin de `fin_utilisable` (`besoin = horizon_max
      + 1`) : deux écritures de la même séance d'achat, non reliées (la ligne de `fin_utilisable` est l'ancre d'un
      sabotage de tests/EPREUVES_DU_TRI_ET_DE_LA_FIN_CALCULEE_Mer_11-11-2026.py, J6). ③ Les positions des versions
      « sans délai » encore ouvertes à la fin des données ne sont pas traitées ici (lot L2 du plan R505).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    return horizon_max + 1


def decaler_d_un_mois(date, sens):
    """Rend la date décalée d'un mois de calendrier, vers l'avant (sens = +1) ou vers l'arrière (sens = -1).

    ① RÔLE — Donner la tolérance « un mois » du contrôle de couverture (`couverture_des_cours`).
    ② CONTEXTE D'APPEL — `couverture_des_cours`, deux fois ; les épreuves, par import.
    ③ ENTRÉE — `date` : AAAA-MM-JJ ; `sens` : +1 ou -1. Exemple réel : (« 2000-01-03 », +1) → « 2000-02-03 ».
    ④ CONDITIONS D'ENTRÉE — `date` est une date valide ; `sens` vaut +1 ou -1.
    ⑤ SORTIE — UNE valeur : la date AAAA-MM-JJ ; le jour est ramené au dernier jour du mois quand il n'y existe pas
      (« 2026-03-31 », -1 → « 2026-02-28 »).
      [rend: 1]
    ⑥ TRAITEMENT — mois ± 1, l'année suivant ; jour borné par `calendar.monthrange`.
    ⑦ UNITÉ — Des dates de calendrier.
    ⑧ POURQUOI — A-1076 ② : « écart d'un mois au plus » ; un mois de calendrier, pas un nombre de jours écrit ici.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError sur une date illisible ou un sens autre que ±1.
      [sort: non]
    """
    import calendar
    if sens not in (1, -1):
        raise ValueError("sens %r : +1 ou -1 seulement" % (sens,))
    a, m, j = (int(x) for x in date.split("-"))
    m += sens
    a, m = (a + 1, 1) if m == 13 else (a - 1, 12) if m == 0 else (a, m)
    return "%04d-%02d-%02d" % (a, m, min(j, calendar.monthrange(a, m)[1]))


def couverture_des_cours(seances, bornes):
    """Compare la période déclarée par la fiche à la période réellement couverte par les cours lus.

    ① RÔLE — LE CONTRÔLE DE COUVERTURE (A-1076 ②) : refuser de jouer quand le fichier de cours lu ne couvre pas la
      période que la fiche déclare.
    ② CONTEXTE D'APPEL — `main`, une fois, juste après la lecture des cours et AVANT le calibrage par le juge (pour que
      le juge ne joue même pas la fiche sur des cours qui ne la couvrent pas) ; les épreuves, par import.
    ③ ENTRÉE — `seances` : l'ensemble des dates de séance des cours lus, toutes valeurs réunies (le calendrier que
      `frontiere_de_la_fiche` reçoit) · `bornes` : (periode_debut, periode_fin) de la fiche, rendues par la porte 0 du
      juge. Exemple réel : la fiche IND-001-RETEST déclare (« 2000-01-03 », « 2026-10-30 ») ; donnees/cours_maitre.csv
      couvre du 2024-01-02 au 2026-11-26.
    ④ CONDITIONS D'ENTRÉE — Les dates s'écrivent AAAA-MM-JJ.
    ⑤ SORTIE — QUATRE valeurs : la première séance lue, la dernière (None, None si aucune), le nombre de séances lues
      comprises dans les bornes, et le motif du refus (None si la couverture tient).
      [rend: 4]
    ⑥ TRAITEMENT — ① aucune séance → motif · ② première séance plus tard qu'un mois après periode_debut → motif ·
      ③ dernière séance plus tôt qu'un mois avant periode_fin → motif · ④ compter les séances dans les bornes.
    ⑦ UNITÉ — Des dates ; des séances.
    ⑧ POURQUOI — A-1076 (découvert le 27-11-2026) : le 26-11-2026, IND-001-RETEST, qui déclarait 2000-01-03 →
      2026-10-30, a été joué sur donnees/cours_maitre.csv (742 séances, 2024-01-02 → 2026-11-25) SANS ALERTE ; ses
      « 70 % » allaient de janvier 2024 à décembre 2025. La loi R-505 version 2, étape 3, « CONTRÔLE AJOUTÉ » : « à
      chaque lancement, elle vérifie qu'elle a bien lu les 20 ans (période et nombre de séances réellement lus) ;
      sinon elle refuse de jouer ».
    ⑨ CE QUI CLOCHE — ① Seuls les DEUX BOUTS sont contrôlés : un trou de plusieurs années au milieu du fichier passe ·
      ② le calendrier réunit toutes les valeurs : une valeur de l'univers dont les cours commencent tard n'est pas
      refusée ici (c'est voulu : une valeur entrée tard dans l'indice, I-8) · ③ le mois de tolérance vient d'A-1076 ;
      l'interpréter comme un mois de calendrier est un choix de l'écrivain (lot L1 du 27-11-2026).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError sur une borne illisible (`decaler_d_un_mois`).
      [sort: non]
    """
    if not seances:
        return None, None, 0, "aucune séance dans le fichier de cours lu"
    premiere, derniere = min(seances), max(seances)
    dedans = sum(1 for d in seances if bornes[0] <= d <= bornes[1])
    motifs = []
    if premiere > decaler_d_un_mois(bornes[0], 1):
        motifs.append("la fiche commence le %s, les cours lus le %s" % (bornes[0], premiere))
    if derniere < decaler_d_un_mois(bornes[1], -1):
        motifs.append("la fiche finit le %s, les cours lus le %s" % (bornes[1], derniere))
    return premiere, derniere, dedans, (" ; ".join(motifs) + " — écart de plus d'un mois (A-1076)") if motifs else None


def recul_en_seances(dates_par_valeur, fin, fin_de_la_fiche):
    """Compte de combien de séances la fin calculée recule par rapport à celle de la fiche.

    ① RÔLE — Mesurer le recul que `recul_maximum` borne (A-1100).
    ② CONTEXTE D'APPEL — `main`, une fois ; les épreuves, par import.
    ③ ENTRÉE — `dates_par_valeur` : {valeur : dates triées} des valeurs jouées · `fin` : la fin calculée ·
      `fin_de_la_fiche` : la fin écrite dans la fiche.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nombre de dates de séance distinctes, toutes valeurs jouées réunies, après `fin` et au
      plus tard à `fin_de_la_fiche`.
      [rend: 1]
    ⑥ TRAITEMENT — Réunir les dates, garder celles de l'intervalle, compter.
    ⑦ UNITÉ — Des séances.
    ⑧ POURQUOI — Ce sont ces séances-là que la période jouée perd.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    return len({d for ds in dates_par_valeur.values() for d in ds if fin < d <= fin_de_la_fiche})


def empreinte_des_cours_jusqu_a(chemin, fin):
    """Rend l'empreinte des seules séances d'un fichier de cours datées au plus tard de la fin de la fiche.

    ① RÔLE — Identifier les cours qui ont servi au choix, sans dépendre des séances ajoutées ensuite.
    ② CONTEXTE D'APPEL — `main` (écrit l'empreinte dans les résultats) ; `frontiere_attendue` de
      `programmes/TRIER_LES_VARIANTES.py` (la recalcule), par import : une seule écriture (R-708).
    ③ ENTRÉE — `chemin` : un fichier de cours au format du fichier maître (colonne `date`) · `fin` : la fin écrite
      dans la fiche, AAAA-MM-JJ.
    ④ CONDITIONS D'ENTRÉE — Le fichier a une colonne `date`.
    ⑤ SORTIE — UNE valeur : seize caractères hexadécimaux (SHA-256 de l'en-tête et des lignes retenues, dans
      l'ordre du fichier).
      [rend: 1]
    ⑥ TRAITEMENT — ① lire l'en-tête et repérer `date` · ② garder chaque ligne dont la date est ≤ `fin`, telle
      qu'écrite · ③ hacher.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecteur de la mission TRI, tour 3, M2 : le fichier maître grandit chaque soir ; une empreinte
      du fichier ENTIER rendait intriable le lendemain un fichier de résultats dont la fiche finit avant les
      séances ajoutées. Ce que le tri garantit (frontière et colonnes « _70 ») ne dépend que des séances jusqu'à la
      fin de la fiche : c'est la propriété qui compte. Une séance passée révisée change l'empreinte, et c'est voulu.
    ⑨ CE QUI CLOCHE — ① Les colonnes de la période ENTIÈRE dépendent aussi des séances après la fin (sorties des
      dernières positions) : l'empreinte ne les protège pas ; le tri ne les lit pas. ② Une ligne déplacée dans le
      fichier sans changer de contenu change l'empreinte (ordre gardé).
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ; lève ValueError sans colonne `date`.
      [sort: non]
    """
    import hashlib
    h = hashlib.sha256()
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        lecteur = csv.reader(f)
        entete = next(lecteur)
        if "date" not in entete:
            raise ValueError("%s : pas de colonne « date »" % chemin)
        i = entete.index("date")
        h.update(("\x1f".join(entete) + "\n").encode("utf-8"))
        for ligne in lecteur:
            if len(ligne) > i and ligne[i] <= fin:
                h.update(("\x1f".join(ligne) + "\n").encode("utf-8"))
    return h.hexdigest()[:16]


def empreinte_du_bareme(mod_pos, nom):
    """Rend l'empreinte du CONTENU d'un barème des frais, tel que le module de positions le lit.

    ① RÔLE — LA définition de « le barème réellement utilisé » (contrat : colonne `empreinte_du_bareme` de
      RESULTATS_DES_VERSIONS), une fois (R-708 : deux définitions d'une même chose divergent toujours).
    ② CONTEXTE D'APPEL — `main` (écrite dans le fichier de résultats) ; `VERIFIER_LA_CHAINE.porte_du_juge` (recalculée
      sur le barème que le juge utiliserait), par import.
    ③ ENTRÉE — `mod_pos` : le module de positions chargé (celui qui chiffre) ; `nom` : le nom du barème, exemple
      réel « REEL ».
    ④ CONDITIONS D'ENTRÉE — le module porte `_lire_un_tableau`, sa lecture de donnees/BAREME_FRAIS.csv.
    ⑤ SORTIE — UNE valeur : seize caractères hexadécimaux.
    [rend: 1]
    ⑥ TRAITEMENT — ① les lignes du barème lues par le module (`_lire_un_tableau("BAREME_FRAIS.csv", "BAREME_FRAIS")`,
      la lecture même de `cout_d_un_ordre`) · ② celles dont `nom_bareme` vaut `nom`, dans l'ordre du fichier · ③ chaque
      ligne en JSON à clés triées · ④ sha256 de l'ensemble, seize premiers caractères.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur R-759 du 19-11-2026, tour 3, I2 : le tarif peut changer entre ② et ④ sous le même nom ;
      mesuré : courtage REEL 0.0015 → 0.015, la porte comparait le seul nom, la fiche était jouée (−247 262,12 €).
    ⑨ CE QUI CLOCHE — ① La liste des valeurs taxées (donnees/VALEURS_TTF.csv) n'y entre pas : la taxe dépend aussi
      d'elle. ② Les colonnes de source et de remarque y entrent : une remarque corrigée change l'empreinte.
    ⑩ EFFET — lit le barème (par le module, qui le garde en mémoire).
    ⑪ TERMINAISON — rend la main ; lève ValueError si aucune ligne ne porte ce nom.
    [sort: non]
    """
    import hashlib
    import json
    lignes = [l for l in mod_pos._lire_un_tableau("BAREME_FRAIS.csv", "BAREME_FRAIS") if l.get("nom_bareme") == nom]
    if not lignes:
        raise ValueError("barème inconnu : %r (donnees/BAREME_FRAIS.csv)" % nom)
    texte = "\n".join(json.dumps(l, sort_keys=True, ensure_ascii=False) for l in lignes)
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()[:16]


def partie_de_reglage(mod_jug, ops, seances_de_la_fiche, horizon, frontiere):
    """Rend la partie de réglage (les 70 % les plus anciens) d'une version, coupée PAR LE MODULE DE JUGEMENT.

    ① RÔLE — Donner au tri des chiffres qui ne contiennent RIEN des 30 % gardés pour le jugement.
    ② CONTEXTE D'APPEL — `main`, une fois par version.
    ③ ENTRÉE — `mod_jug` : `programmes/MODULE_JUGEMENT.py` chargé · `ops` : les opérations jouées ·
      `seances_de_la_fiche` : les dates de séance des cours lus comprises dans les bornes de la FICHE · `horizon` :
      l'horizon de la version, en séances · `frontiere` : la date rendue par `frontiere_de_la_fiche` du module de
      jugement, la seule fonction qui l'établit (12-11-2026).
    ④ CONDITIONS D'ENTRÉE — Les dates sont celles du fichier de cours joué.
    ⑤ SORTIE — DEUX valeurs : l'embargo en séances (ou None sans opération), le résumé des opérations de la partie
      de réglage (`{"n": 0}` sans opération).
      [rend: 2]
    ⑥ TRAITEMENT — ① appeler `coupure_70_30` du module de jugement, avec l'horizon de la version et la frontière
      reçue · ② refuser une coupure qui ne reconnaît aucune date · ③ refuser une coupure qui a coupé à une AUTRE
      séance que la frontière reçue, celle que `main` écrit dans le fichier (relecteur, tour 3, M1) · ④ rendre son
      embargo et son résumé « res_70 ».
    ⑦ UNITÉ — Dates ; séances ; euros et pourcents dans le résumé.
    ⑧ POURQUOI — Relecteur neuf du 11-11-2026, D1 MAJEUR : le tri choisissait sur la période entière, 30 % réservés
      compris ; la version retenue n'était plus jugée hors échantillon. La coupure est celle du juge (`juger`, ligne
      `c = J.coupure_70_30(ops, _sea, horizon=_h_emb, frontiere=J.frontiere_de_la_fiche(fiche, seances, _bornes))`,
      avec `_sea` réduit aux bornes de la fiche) : importée, jamais recopiée (R-708). Le contrôle ③ compare la coupe
      RÉELLE à la valeur écrite : sans lui, une frontière DÉCLARÉE perdue en route (`frontiere=None`, ou une autre
      date) faisait couper ailleurs que la frontière écrite, et entrer des séances des 30 % dans les colonnes « _70 »
      sans bruit (sonde X4 du relecteur du 12-11-2026 : 40 opérations devenues 50). Le calendrier est construit comme dans `main` du juge (`seances = {b["date"] for s in
      cours.values() for b in s}`), une ligne recopiée faute de fonction exposée.
    ⑨ CE QUI CLOCHE — ① La frontière dépend des bornes de la FICHE, pas de la fin calculée : c'est ce que fera le
      juge, et c'est voulu (la fin ne touche que les 30 %). ② Sans opération, `coupure_70_30` ne rend pas
      d'embargo : la case reste vide.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError si aucune date de signal n'est reconnue au calendrier, ou si la
      coupe réelle n'est pas la frontière reçue.
      [sort: non]
    """
    c = mod_jug.coupure_70_30(ops, seances_de_la_fiche, horizon=horizon, frontiere=frontiere)
    if "motif" in c:
        raise ValueError("coupure 70/30 impossible : %s" % c["motif"])
    if ops and c.get("frontiere") != frontiere:
        raise ValueError("la coupure a coupé au %s, la frontière écrite est le %s : rien n'est écrit"
                         % (c.get("frontiere"), frontiere))
    return c.get("embargo_seances"), c.get("res_70", {"n": 0})


def lire_la_ligne_de_commande(arguments):
    """Sépare les arguments de position et l'option `--cours=`, et refuse une option mal écrite.

    ① RÔLE — Lire la ligne de commande comme le juge des stratégies la lit (`main` du juge, lignes
      `_args = ...` et `_mal = ...`, 27-10-2026), pour que `--cours=` veuille dire la même chose ici et là.
    ② CONTEXTE D'APPEL — `main`, une fois, avant tout ; et les épreuves du tri
      (`tests/EPREUVES_DU_TRI_ET_DE_LA_FIN_CALCULEE_Mer_11-11-2026.py`), par import.
    ③ ENTRÉE — `arguments` : la liste des arguments, sans le nom du programme (`sys.argv[1:]`).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — TROIS valeurs : la liste des arguments de position ; le fichier de cours nommé par
      `--cours=`, ou None sans l'option ; le motif du refus, ou None si la ligne est bien écrite.
      [rend: 3]
    ⑥ TRAITEMENT — ① séparer ce qui commence par « -- » du reste · ② refuser toute option qui n'est pas
      « --cours=<quelque chose> » · ③ refuser « --cours= » écrit deux fois · ④ rendre le fichier nommé.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Relecture et superviseur du 27-10-2026, sur le juge : « --cours fichier », sans « = »,
      était ignoré, et « fichier » devenait la fiche visée. Ici, il deviendrait le troisième argument de
      position. Le refus de deux `--cours=` est PLUS STRICT que le juge, qui prend le premier en silence :
      deux fichiers de cours pour un lancement, c'est une ligne de commande à reprendre, pas un choix.
    ⑨ CE QUI CLOCHE — C'est une seconde écriture de la lecture du juge (R-708) : le juge ne l'expose pas
      comme fonction. Si le juge accepte un jour une autre option, ce programme la refusera : il rougit,
      il ne se tait pas.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    positions = [a for a in arguments if not a.startswith("--")]
    options = [a for a in arguments if a.startswith("--")]
    mal = [a for a in options if not (a.startswith(OPTION_COURS) and len(a) > len(OPTION_COURS))]
    if mal:
        return positions, None, ("option inconnue ou mal écrite : %s (seule « --cours=<fichier> » existe)"
                                 % mal)
    if len(options) > 1:
        return positions, None, "option « --cours= » écrite %d fois : %s" % (len(options), options)
    return positions, (options[0][len(OPTION_COURS):] if options else None), None


def fin_utilisable(dates_par_valeur, debut, fin_de_la_fiche, horizon_max):
    """Calcule la fin de période la plus tardive qui laisse assez de séances après elle à chaque valeur.

    ① RÔLE — Donner, PAR PROGRAMME, la fin de la période jouée (plan V7, bloc 5g, complément du
      11-11-2026 à 20h17 : « LA FIN DE LA PÉRIODE SE CALCULE PAR PROGRAMME, ELLE NE S'ÉCRIT PAS À LA MAIN »).
    ② CONTEXTE D'APPEL — `main`, une fois, après le calibrage et la version identique ; les épreuves du tri,
      par import, sur de vraies séries de cours.
    ③ ENTRÉE — `dates_par_valeur` : pour chaque valeur jouée (son mnémonique), la liste TRIÉE des dates
      de ses séances, AAAA-MM-JJ, telle que le lecteur unique les rend · `debut` et `fin_de_la_fiche` : les
      bornes rendues par la porte 0 · `horizon_max` : l'horizon le plus long de la combinatoire, en séances.
    ④ CONDITIONS D'ENTRÉE — Au moins une valeur ; `horizon_max` est un entier ≥ 0, 0 = toutes les versions sont
      « aucune » (relecteur neuf E1F phase 2, m-2 : `main` lui passe alors 0 ; le besoin vaut 1 séance).
    ⑤ SORTIE — DEUX valeurs : la fin calculée (AAAA-MM-JJ), ou None si aucune fin ne laisse assez de
      séances ; la valeur qui la limite (celle dont les cours s'arrêtent le plus tôt ; None si c'est la
      fiche qui limite), ou la première valeur fautive si la fin est None.
      [rend: 2]
    ⑥ TRAITEMENT — ① le besoin est `horizon_max + 1` séances après la fin : la séance d'achat (l'Open du
      lendemain du signal, R-601) puis `horizon_max` séances de détention · ② pour chaque valeur, la
      séance qui doit rester après la fin est `dates[-besoin]` ; une valeur qui n'a pas `besoin + 1`
      séances ne laisse aucune fin · ③ la borne est la plus précoce de ces séances · ④ si la borne tombe
      après la fin écrite dans la fiche, la fin de la fiche est gardée telle quelle · ⑤ sinon la fin est la
      DERNIÈRE séance, parmi celles des valeurs jouées, qui tombe avant la borne ; elle n'est donc pas
      forcément une séance de la valeur qui limite (une valeur en trou n'empêche pas les autres de jouer
      jusqu'à la veille de sa séance) · ⑥ aucune séance entre le début de la fiche et la borne vaut
      « aucune fin ».
    ⑦ UNITÉ — Des dates AAAA-MM-JJ ; des séances.
    ⑧ POURQUOI — Une position achetée le dernier jour doit avoir une fin connue, sinon elle est fermée à
      la fin des données, avant son horizon, sans alerte (relecture du 08-10-2026, défaut N3). Exemple
      réel du 11-11-2026 à 19h53 : la fiche IND-001-RETEST portait une fin au 30-10-2026 écrite à la
      main, Accor n'avait que 7 séances après, pour une durée essayée de 25 ; le Chat a dû ramener la fin
      à la main au 05-10-2026, la 26e séance d'Accor avant sa dernière. La même condition, `marge <
      h_max + 1`, existait déjà ici en REFUS : elle devient un CALCUL, et le refus reste comme garde-fou.
      La fin de la fiche n'est jamais dépassée : la fiche dit jusqu'où on a le droit de regarder.
    ⑨ CE QUI CLOCHE — ① Les séances comptées sont celles du fichier de cours, trous exclus ; une valeur
      suspendue longtemps à la fin compterait moins de jours de calendrier. ② Cette fonction ne borne pas le recul :
      `main` le borne ensuite par `recul_maximum` (calculé, A-1100 ; relecteur neuf du
      11-11-2026, D6) et refuse au-delà en nommant la valeur qui limite.
      ③ La fin dépend des valeurs jouées : une valeur sortie de la cote tôt ramène la fin de tous.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    besoin = horizon_max + 1
    borne, limite = None, None
    for m in sorted(dates_par_valeur):
        dates = dates_par_valeur[m]
        if len(dates) < besoin + 1:
            return None, m
        if borne is None or dates[-besoin] < borne:
            borne, limite = dates[-besoin], m
    if borne > fin_de_la_fiche:
        return fin_de_la_fiche, None          # la fiche laisse déjà assez de séances : sa fin est gardée telle quelle
    candidates = [d for ds in dates_par_valeur.values() for d in ds if debut <= d < borne]
    if not candidates:
        return None, limite
    return max(candidates), limite


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
    ⑥ TRAITEMENT — ① copier la fiche, avec le signal qu'elle nomme · ② y remplacer
      tp, sl, horizon, univers, et `quand_jouer` si la version le porte (REGLAGES_FACULTATIFS, lot W2e-FIX).
    ⑦ UNITÉ — tp et sl en fractions ; horizon en séances.
    ⑧ POURQUOI — DECLINER le prescrit dans son en-tête : la version ne porte que
      ce qui varie, le reste vient de la fiche.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun : la fiche d'origine n'est pas modifiée.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    f = dict(fiche)
    for k in REGLAGES:
        f[k] = version[k]
    for k in REGLAGES_FACULTATIFS:   # présent dans la version : il remplace celui de la fiche (lot W2e-FIX)
        if k in version:
            f[k] = version[k]
    return f


def empreinte_de_la_version(J, fiche, version, lire_module):
    """Rend l'empreinte des réglages d'une version de la moulinette : celle de la fiche fusionnée qu'on joue.

    ① RÔLE — Donner à une version la MÊME empreinte que la fiche du registre qui porterait ses réglages (superviseur
      R-759 du 14-11-2026, CARNET partie 1, §4.2 : « une version de moulinette EST une fiche fusionnée »).
    ② CONTEXTE D'APPEL — `main`, une fois par version, pour la colonne `empreinte_des_reglages` du fichier de
      résultats ; les épreuves (fiche et version aux mêmes réglages).
    ③ ENTRÉE — `J` : le module du juge · `fiche` : la dernière ligne de la fiche au registre · `version` : une ligne de
      la combinatoire · `lire_module` : la fonction de `J.lire_module_du_jour`.
    ④ CONDITIONS D'ENTRÉE — Celles de `fusionner`.
    ⑤ SORTIE — UNE valeur : seize caractères hexadécimaux. Exemple réel : C5E10-OBS-V1-E01-0914 (tp 0,04, sl 0,025,
      20 séances, les 10 valeurs de la fiche) rend l'empreinte de la fiche C5E10-OBS-V1 elle-même.
      [rend: 1]
    ⑥ TRAITEMENT — `fusionner`, puis `J.empreinte_des_reglages`, premier élément.
    ⑦ UNITÉ — Une empreinte, comparable par égalité seulement.
    ⑧ POURQUOI — Une seule définition de l'empreinte (R-708) : l'ancienne empreinte du tri ne hachait que quatre
      réglages et ne voyait pas le signal (relecteur neuf du 14-11-2026, D2). Écrite AU MOMENT DU JEU, elle ne relit
      pas la fiche du jour au moment du tri (⑨ de l'ancienne fonction du tri).
    ⑨ CE QUI CLOCHE — Le module est lu au jour du jeu (voir ⑨ ① d'`empreinte_des_reglages`).
    ⑩ EFFET — Celui de `lire_module`.
    ⑪ TERMINAISON — Rend la main ; lève ce que lève le juge.
      [sort: non]
    """
    return J.empreinte_des_reglages(fusionner(fiche, version), lire_module)[0]


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
      version ; « sans stop » se compare comme un mot (`COMMUN.est_le_mot_du_stop_aucun`) ·
      ② lire l'horizon par `lire_horizon` ; « aucune » se compare comme un mot
      (`COMMUN.lire_horizon_ou_aucune`) · ③ comparer les univers.
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
    import COMMUN   # déjà chargé par le juge : le même module, donc les mêmes sentinelles (lecture des mots, R-708)
    ecarts = []
    for k in ("tp", "sl"):
        # « SANS STOP » (A-541, 19-10-2026 ; mission VENTE du 11-11-2026) : un mot, comparé comme un mot ; il ne passe
        # jamais par `pourcent`, qui le lirait illisible.
        mots = [k == "sl" and COMMUN.est_le_mot_du_stop_aucun(x) for x in (fusion[k], version[k])]
        if any(mots):
            ecart = not all(mots)
        else:
            ecart = abs(J.pourcent(fusion[k]) - float(version[k])) > 1e-12
        if ecart:
            ecarts.append("%s lu %r, version %r" % (k, fusion[k], version[k]))
    # LA DURÉE « AUCUNE » (A-645, mission VENTE) : reconnue par la lecture commune ; un nombre reste lu par le juge.
    aucunes = [COMMUN.lire_horizon_ou_aucune(x) is COMMUN.HORIZON_AUCUNE for x in (fusion["horizon"], version["horizon"])]
    if any(aucunes):
        if not all(aucunes):
            ecarts.append("horizon lu %r, version %r" % (fusion["horizon"], version["horizon"]))
    elif J.lire_horizon(fusion["horizon"]) != int(version["horizon"]):
        ecarts.append("horizon lu %r, version %r" % (fusion["horizon"], version["horizon"]))
    if codes(fusion["univers"]) != codes(version["univers"]):
        ecarts.append("univers lu %r, version %r" % (fusion["univers"], version["univers"]))
    # « QUAND JOUER » (lot W2e-FIX) : comparé comme l'ENSEMBLE des types de marché que lit le juge (MODULE_QUAND_JOUER,
    # R-708), seulement si la version le porte.
    if "quand_jouer" in version:
        import MODULE_QUAND_JOUER as _Q
        if _Q.lire_quand_jouer(fusion.get("quand_jouer") or _Q.TOUJOURS) != _Q.lire_quand_jouer(version["quand_jouer"]):
            ecarts.append("quand_jouer lu %r, version %r" % (fusion.get("quand_jouer"), version["quand_jouer"]))
    return ecarts


def refus_des_versions(contrat, J, mod_pos, base, fiche, versions):
    """Rend les refus du contrat de stratégie pour chaque version de la combinatoire, fusionnée avec la fiche.

    ① RÔLE — Passer CHAQUE version au contrat de stratégie (A-923), pas seulement la fiche du registre (M5 du RELU
      e77edfacf, 20-11-2026).
    ② CONTEXTE D'APPEL — `main`, une fois, avant le calibrage, après que la fiche elle-même a passé le contrat.
    ③ ENTRÉE — `contrat` : le module CONTRATS_DES_FICHIERS chargé · `J` : le juge · `mod_pos` : le module de positions
      (None : le contrat le charge, ou lève s'il manque) · `base` : la racine · `fiche` : la dernière ligne de la fiche
      au registre · `versions` : les lignes de la combinatoire. Exemple réel : COMBINATOIRE_C5E10-OBS-V1_E01, 2 695
      versions.
    ④ CONDITIONS D'ENTRÉE — Chaque version porte les cases de REGLAGES (celles de `fusionner`).
    ⑤ SORTIE — UNE valeur : la liste des refus, VIDE si toutes les versions suivent le contrat ; chaque refus est
      « <id_version> — <case> : <motif> » (le texte rendu par `manques_du_contrat`, case nommée en tête). Exemple mesuré
      (20-11-2026) : version 0001 réécrite « TTE,ZZZ » → « C5E10-OBS-V1-E01-0001 — univers : mnémonique(s) absent(s) du
      référentiel : ZZZ ».
      [rend: 1]
    ⑥ TRAITEMENT — pour chaque version : `fusionner` (la fiche jouée), son `etat_vie` mis à
      `contrat.ETAT_D_UNE_VERSION_DE_MOULINETTE` (« LABO » : une version se joue au laboratoire, jamais au soir), puis
      `contrat.manques_du_contrat` sur elle ; chaque refus préfixé de l'identifiant de la version.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La combinatoire fait varier univers, tp, sl et horizon par version ; la fiche seule au contrat
      laissait jouer une version « TTE,ZZZ », arrêtée plus loin par la marge de cours sans nommer la case (RELU
      e77edfacf, M5). Le contrôle vit au contrat, il est APPELÉ ici (R-708 : deux écritures d'une même chose divergent).
      L'état « LABO » : sans lui, les contrôles du SOIR s'appliquaient aux versions d'une fiche suivie par le soir
      (mesuré le 20-11-2026 : 245 refus faux sur 3 675 versions de C5E10-QA-V1, toutes à « sans stop », réglage que
      PREPARER ⓪ propose et que ce programme joue).
    ⑨ CE QUI CLOCHE — ① Durée : un appel du contrat par version (mesuré le 20-11-2026 après la mémoire du chemin du
      référentiel : voir la note echanges/A_RELIRE.md) ; sous --tranche, TOUTE la combinatoire est contrôlée à chaque
      tranche, comme ses autres contrôles. ② Les avis du contrat (`avis_du_contrat`) ne sont pas rendus ici. ③ La fiche
      elle-même reste contrôlée sous SON état (contrôles du soir compris) : une fiche QA à « sans stop » est refusée —
      éprouvé par JOUER lui-même depuis le 20-11-2026 (E24 de tests/EPREUVES_DU_CONTRAT_DE_STRATEGIE_Jeu_19-11-2026.py,
      sabotage S18 ; M1 du RELU 33ee384ae).
    ⑩ EFFET — Celui de `manques_du_contrat` (lit, charge le module de signal de la fiche au premier appel).
    ⑪ TERMINAISON — Rend la main ; laisse passer ContratImpossible (le contrôle n'a pas tourné), que `main` rend en 2.
      [sort: non]
    """
    refus = []
    for v in versions:
        version_au_labo = dict(fusionner(fiche, v), etat_vie=contrat.ETAT_D_UNE_VERSION_DE_MOULINETTE)
        for r in contrat.manques_du_contrat(version_au_labo, base, J=J, mod_pos=mod_pos):
            refus.append("%s — %s" % (v["id_version"], r))
    return refus


def calibrer_par_le_juge(base, ident, cours=None, essai=False):
    """Lance le juge seul sur la fiche et lit son verdict.

    ① RÔLE — Prouver que l'instrument retrouve les chiffres de référence avant de
      jouer quoi que ce soit.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `base` : la racine du dépôt · `ident` : l'identifiant de la fiche · `cours` : le
      fichier de cours de `--cours=`, relatif à la racine, ou None pour le fichier maître · `essai` : vrai sous
      l'option « --essai-sans-regard » (A-863), qui est alors passée au juge ; ses lignes, toutes marquées, sont
      lues privées de la marque.
    ④ CONDITIONS D'ENTRÉE — Le juge est dans `programmes/` sous la racine.
    ⑤ SORTIE — DEUX valeurs : vrai si le juge est calibré et rend 0 ; la ligne de
      résultat qu'il affiche pour la fiche, ou None.
      [rend: 2]
    ⑥ TRAITEMENT — ① lancer le juge avec l'identifiant, et `--cours=` s'il est donné, pour que
      la ligne qu'il affiche soit jouée sur les mêmes cours que ce programme · ② exiger le code 0, la
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
    commande = [sys.executable, "-B", os.path.join(base, "programmes", "JUGE_DES_STRATEGIES.py"), base, ident]
    if cours:
        commande.append(OPTION_COURS + cours)
    if essai:
        import CONTRATS_DES_FICHIERS as _CE
        commande.append(_CE.OPTION_D_ESSAI_SANS_REGARD)
    p = subprocess.run(commande, capture_output=True, text=True)
    sortie = p.stdout + p.stderr
    if essai:   # la marque de chaque ligne du juge (A-863) ôtée pour lire sa ligne de résultat comme d'habitude
        sortie = "".join(l[len(_CE.STATUT_D_ESSAI + " · "):] if l.startswith(_CE.STATUT_D_ESSAI + " · ") else l
                         for l in sortie.splitlines(True))
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


def comparer_au_temoin(f_comb, sid, essai, f_resultats, ids=None, chiffres=True):
    """Compare les résultats d'un lancement au témoin de résultats, s'il existe.

    ① RÔLE — Protéger les réglages que le calibrage du juge ne touche pas : il ne
      rejoue que les réglages de la fiche.
    ② CONTEXTE D'APPEL — `main`, une fois, après avoir joué toutes les versions.
    ③ ENTRÉE — `f_comb` : la combinatoire · `sid`, `essai` : la stratégie et
      l'essai · `f_resultats` : le fichier provisoire qui vient d'être écrit, ou
      (depuis le 29-10-2026, C15) un dictionnaire id_version -> ligne, quand les
      versions ont été rejouées sous le barème du témoin · `ids` : sous --tranche, les
      versions jouées (le témoin est filtré sur elles), None sinon · `chiffres` : faux
      pour ne comparer que les identifiants (`assembler`, sous un autre barème que le
      témoin, A-919).
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
    tem = {r["id_version"]: r for r in csv.DictReader(open(f_tem, encoding="utf-8-sig"))
           if ids is None or r["id_version"] in ids}   # sous --tranche, les seules versions jouées (A-919)
    # `f_resultats` : un fichier de résultats, OU un dictionnaire id_version -> ligne, quand la comparaison se fait
    # sous le barème du témoin et non sous celui des résultats écrits (C15, 29-10-2026).
    res = f_resultats if isinstance(f_resultats, dict) else \
        {r["id_version"]: r for r in csv.DictReader(open(f_resultats, encoding="utf-8"))}
    ecarts = ["%s absente du témoin" % k for k in sorted(set(res) - set(tem))]
    ecarts += ["%s absente des résultats" % k for k in sorted(set(tem) - set(res))]
    for k in sorted(set(res) & set(tem)) if chiffres else ():    # chiffres=False : les identifiants seuls (A-919)
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
    ⑤ SORTIE — UNE valeur : 0 ou 1, passée à la sortie du processus ; 2 quand un essai déclaré est refusé (A-863)
      ou quand le contrat de stratégie n'a pas pu être contrôlé (R-734, depuis le 19-11-2026 ; AVANT le calibrage
      depuis le 20-11-2026, pour que le juge qui tombe faute de référentiel ne masque plus ce 2 par un 1).
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
    # L'ESSAI DÉCLARÉ (A-863, décision de Jean-Luc du 16-11-2026 à 20h46) : l'option est ôtée de la ligne AVANT sa
    # lecture habituelle, et la sortie marquée AVANT toute écriture, par la fonction du juge de ce dossier (R-708).
    # SANS L'OPTION, RIEN NE CHANGE : aucun import de plus (ce programme se lance aussi seul, copié hors du dépôt, par
    # les épreuves du tri) ; le texte de l'option est confronté au contrat dès qu'elle est lue.
    if sys.argv[1:2] == ["--assembler"]:
        return assembler(sys.argv[2:])
    try:
        k_tranche, n_tranches = lire_la_tranche(sys.argv[1:])
    except ValueError as e:
        return arreter("%s. Rien n'est joué." % e)
    sys.argv = [a for a in sys.argv if not a.startswith(OPTION_TRANCHE)]
    essai_declare = OPTION_ESSAI in sys.argv[1:]
    if essai_declare and n_tranches is not None:
        return arreter("--tranche= et %s ensemble : un essai sans regard ne joue qu'une version" % OPTION_ESSAI)
    jeton = None
    if essai_declare:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import CONTRATS_DES_FICHIERS as _CE
        import JUGE_DES_STRATEGIES as _JE
        _JE.marquer_la_sortie()
        if _CE.OPTION_D_ESSAI_SANS_REGARD != OPTION_ESSAI or sys.argv[1:].count(OPTION_ESSAI) > 1:
            print("ARRÊT (essai refusé) : option %s écrite deux fois, ou différente du contrat (%s). Rien n'est joué."
                  % (OPTION_ESSAI, _CE.OPTION_D_ESSAI_SANS_REGARD))
            return 2
    positions, autre_cours, refus = lire_la_ligne_de_commande([a for a in sys.argv[1:] if a != OPTION_ESSAI])
    if refus:
        return arreter(refus + ". Rien n'est joué.")
    if len(positions) != 3:
        print(__doc__.split("①")[0])
        return 1
    base, f_comb, f_out = (os.path.abspath(a) for a in positions)
    if os.path.exists(f_out):
        return arreter("le fichier de résultats existe déjà : %s" % f_out)
    # LE FICHIER DE COURS, RELATIF À LA RACINE COMME POUR LE JUGE (`os.path.join(base, _autre)` dans son `main`) ;
    # son existence est exigée ici, avant le calibrage, pour que l'arrêt dise ce qui manque.
    if autre_cours is not None and not os.path.isfile(os.path.join(base, autre_cours)):
        return arreter("le fichier de cours de --cours= n'existe pas : %s" % os.path.join(base, autre_cours))

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
    if essai_declare:
        # L'IDENTITÉ DE L'ESSAI, AVANT LE CALIBRAGE (A-863) : la règle vit dans `jeton_d_essai` du juge, la seule ;
        # elle refuse en 2 un dépôt, plus d'une version, une fiche qui n'est identique à aucune fiche autorisée.
        if os.path.dirname(os.path.abspath(_JE.__file__)) != os.path.join(base, "programmes"):
            print("ARRÊT (essai refusé) : un essai se joue avec la moulinette de la copie jouée (%s), pas %s"
                  % (os.path.join(base, "programmes"), _JE.__file__))
            return 2
        _fe = _CE.fiches_du_registre(_JE.trouver(base, _CE.NOM_DU_REGISTRE_DES_STRATEGIES)).get(sid)
        if _fe is None:
            print("ARRÊT (essai refusé) : fiche %s absente du registre. Rien n'est joué." % sid)
            return 2
        jeton, motif = _JE.jeton_d_essai(base, _fe, len(versions))
        if jeton is None:
            print("ARRÊT (essai refusé) : %s. Rien n'est joué." % motif)
            return 2
        # LA VERSION JOUÉE A LES RÉGLAGES DE LA FICHE D'ESSAI, AVANT TOUT JEU (mineur M5 du relecteur neuf du
        # 16-11-2026) : le jeton couvre la FICHE ; une version marquée identique mais d'un autre réglage (tp 0,06 au lieu
        # de 0,04) jouerait, avec le jeton, des réglages non autorisés dans la fenêtre du regard unique. Même mesure
        # que la colonne des résultats (`empreinte_de_la_version`, R-708). Refus en 2, comme les autres refus d'essai.
        _lire = _JE.lire_module_du_jour(base)
        _emp_v = empreinte_de_la_version(_JE, _fe, versions[0], _lire)
        _emp_f = _JE.empreinte_des_reglages(_fe, _lire)[0]
        if _emp_v != _emp_f:
            print("ARRÊT (essai refusé) : la version %s n'a pas les réglages de la fiche %s (empreinte %s, fiche %s)."
                  " Rien n'est joué." % (versions[0]["id_version"], sid, _emp_v, _emp_f))
            return 2
        print("ESSAI DÉCLARÉ (A-863) : %s, une version ; rien n'est inscrit ni compté, le fichier écrit porte la colonne"
              " %s et le tri le refuse" % (sid, _CE.COLONNE_DU_STATUT_D_ESSAI))

    # LE CONTRAT DE STRATÉGIE, AVANT LE CALIBRAGE ET AVANT TOUT JEU (20-11-2026, M4 et M5 du RELU e77edfacf) : la fiche
    # relue au registre ET CHAQUE VERSION fusionnée passent le contrat ; un contrôle qui n'a pas pu tourner rend 2
    # (R-734). Avant le 20-11-2026, le contrat venait APRÈS le calibrage : sans référentiel, le juge tombait d'abord et
    # ce programme rendait 1 (« le juge ne se calibre pas »), le 2 annoncé n'était jamais atteint ; et une version
    # « TTE,ZZZ » n'était arrêtée que par la marge de cours, sans nommer la case.
    sys.path.insert(0, os.path.join(base, "programmes"))
    import JUGE_DES_STRATEGIES as J
    if os.path.dirname(os.path.abspath(J.__file__)) != os.path.join(base, "programmes"):
        return arreter("le juge importé n'est pas celui du dépôt : %s" % J.__file__)
    # LA FICHE EST LA DERNIÈRE LIGNE DE SON IDENTIFIANT (décision de Jean-Luc n°83 du 01-11-2026 à 12h33 : « La
    # dernière ligne ajoutée fait foi. Les précédentes restent comme historique. ») : le nom du registre et sa lecture
    # vivent au contrat (programmes/CONTRATS_DES_FICHIERS.py, chargé depuis le même dossier que le juge). Avant le
    # 05-11-2026, une fiche écrite deux fois arrêtait ce programme (« trouvée 2 fois au registre »).
    import CONTRATS_DES_FICHIERS as contrat
    fiche = contrat.fiches_du_registre(J.trouver(base, contrat.NOM_DU_REGISTRE_DES_STRATEGIES)).get(sid)
    if fiche is None:
        return arreter("fiche %s absente du registre" % sid)
    # LE MODULE DE POSITIONS, celui que `jouer` emploie ; absent, le contrat le dit (ContratImpossible, code 2).
    f_pos = J.trouver(base, "MODULE_POSITIONS.py")
    mod_pos = J.charger_module(f_pos, "pos") if f_pos else None
    # LA FICHE RELUE ICI PASSE LE CONTRAT DE STRATÉGIE, PAS SEULEMENT `porte_0` (relecteur neuf du contrat du 19-11-2026,
    # M3) : un registre réécrit entre ⓪ et ② faisait jouer ① ② ③ une fiche hors contrat (mesuré : univers « TTE,ZZZ »,
    # `porte_0` (True, [])). Le contrôle vit au contrat, il est APPELÉ ici (R-708). PUIS CHAQUE VERSION (M5) : la
    # combinatoire fait varier univers, tp, sl et horizon, et un fichier réécrit entre ⓪ et ② vaut pour elle aussi.
    try:
        refus_du_contrat = contrat.manques_du_contrat(fiche, base, J=J, mod_pos=mod_pos)
        if refus_du_contrat:
            return arreter("la fiche %s ne suit pas le contrat de stratégie (A-923) : %s"
                           % (sid, " ; ".join(refus_du_contrat)))
        refus_des_v = refus_des_versions(contrat, J, mod_pos, base, fiche, versions)
    except contrat.ContratImpossible as e:
        print("ARRÊT : le contrat de stratégie n'a pas pu être contrôlé (R-734) : %s. Rien n'est joué." % e)
        return 2
    if refus_des_v:
        return arreter("%d version(s) ne suivent pas le contrat de stratégie (A-923) : %s%s. Rien n'est joué."
                       % (len(refus_des_v), " ‖ ".join(refus_des_v[:5]), " ‖ …" if len(refus_des_v) > 5 else ""))
    print("CONTRAT DE STRATÉGIE : la fiche et les %d versions le suivent" % len(versions))

    mnemo = J.table_mnemoniques(J.trouver(base, "REFERENTIEL_VALEURS"))
    # LES COURS PASSENT PAR LE LECTEUR UNIQUE, COMME DANS `main` DU JUGE (A-577, étape 1, 27-10-2026) : ce
    # programme se compare au juge, il lit donc comme lui — sinon le juge affiche 89 opérations et ce
    # programme 100 sur la même fiche (C5E10-OBS-V1, mesuré le 27-10-2026). Deux lectures divergent (R-708).
    # `--cours=` : le fichier nommé, relatif à la racine, comme le juge (plan V7, bloc 5l ⑤) ; sinon le maître.
    # LUS AVANT LE CALIBRAGE depuis le 27-11-2026 (A-1076, lot L1) : le contrôle de couverture refuse AVANT que le juge
    # ne joue la fiche sur des cours qui ne couvrent pas sa période.
    f_cours_rel = (os.path.relpath(os.path.join(base, autre_cours), base) if autre_cours is not None
                   else os.path.relpath(J.fichiers_de_cours(base)[0], base))
    try:   # le juge refuse lui-même une lecture qui a écarté des lignes (`lire_par_le_lecteur`, 27-10-2026)
        cours, lecture = J.lire_par_le_lecteur(base, f_cours_rel, mnemo)
    except ValueError as e:
        if not str(e).startswith("le lecteur unique"):
            raise
        return arreter(str(e))
    # LE CONTRÔLE DE COUVERTURE (A-1076 ② ; R-505 v2, étape 3, « CONTRÔLE AJOUTÉ ») : la période déclarée par la fiche
    # contre la période réellement lue ; affiché à CHAQUE lancement, refus au-delà d'un mois d'écart.
    seances_lues = {b["date"] for s_ in cours.values() for b in s_}
    ok_c, _manq_c, bornes_c = J.porte_0(dict(fiche))
    if ok_c:   # sinon la porte 0 refusera plus bas, en nommant ce qui manque (`jouer_une`)
        prem_c, dern_c, dedans_c, refus_c = couverture_des_cours(seances_lues, bornes_c)
        print("COURS LUS : %s · %s -> %s · %d séance(s) lues, dont %d dans la période de la fiche %s -> %s"
              % (f_cours_rel, prem_c, dern_c, len(seances_lues), dedans_c, bornes_c[0], bornes_c[1]))
        if refus_c:
            return arreter("COUVERTURE DES COURS INSUFFISANTE : %s ; le fichier %s ne couvre pas la période déclarée "
                           "par la fiche %s. Rien n'est joué." % (refus_c, f_cours_rel, sid))

    ok, ligne_juge = (calibrer_par_le_juge(base, sid, autre_cours) if jeton is None
                      else calibrer_par_le_juge(base, sid, autre_cours, essai=True))
    print("CALIBRAGE PAR LE JUGE SEUL : %s" % ("OK" if ok else "ÉCHEC"))
    if not ok or not ligne_juge:
        return arreter("le juge des stratégies ne se calibre pas, ou n'a pas joué la fiche")
    print("  le juge affiche : %s" % ligne_juge)
    # LE SIGNAL N'EST PLUS CHARGÉ ICI (A-542, 30-10-2026) : chaque fiche jouée le nomme, `jouer_une` le lit par
    # `signal_de_la_fiche` du juge, la seule lecture (R-708). LE MODULE DE POSITIONS, LA FICHE ET LE CONTRAT sont
    # chargés et contrôlés AVANT le calibrage depuis le 20-11-2026 (plus haut).

    def jouer_une(f, bareme=None, ops_rendues=None, periode=None):
        """Fait passer une fiche par la porte 0 puis la joue.

        ① RÔLE — Un seul chemin de jeu pour la fiche, la version identique et
          toutes les versions.
        ② CONTEXTE D'APPEL — `main`, une fois par fiche à jouer.
        ③ ENTRÉE — `f` : une fiche, d'origine ou fusionnée · `bareme` : None pour le
          barème des trades vécus, sinon le nom d'un barème (celui du témoin, C15) ·
          `ops_rendues` : une liste où recopier les opérations jouées, ou None · `periode` : les bornes à
          jouer, ou None pour celles de la fiche (la fin calculée, bloc 5g, arrive par là).
        ④ CONDITIONS D'ENTRÉE — Les cours, le référentiel et les deux modules sont
          chargés par `main`.
        ⑤ SORTIE — DEUX valeurs : le résumé rendu par `resumer` du juge ; les bornes
          de la période rendues par la porte 0 (celles de la fiche, même quand `periode`
          en impose d'autres : `main` compare ces bornes d'une version à l'autre).
          [rend: 2]
        ⑥ TRAITEMENT — ① porte 0 · ② lire le signal que la fiche nomme, par
          `signal_de_la_fiche` du juge (A-542) · ③ `jouer` sur `periode`, ou à défaut
          sur la période de la fiche, avec CE signal · ④ refuser une valeur absente
          des cours · ⑤ résumer.
        ⑦ UNITÉ — Euros ; pourcents ; dates AAAA-MM-JJ.
        ⑧ POURQUOI — Le même appel que `main` du juge, ligne `ops, inconnus = jouer(...)`.
        ⑨ CE QUI CLOCHE — Rien vu.
        ⑩ EFFET — Aucun sur la fiche reçue. Charge le module de signal nommé au
          premier appel (le juge le garde ensuite en mémoire).
        ⑪ TERMINAISON — Rend la main, ou lève ValueError sur un refus — porte 0, ou
          signal nommé introuvable.
          [sort: non]
        ⑫ DÉFINITIONS
          la porte 0 : la fonction `porte_0` du juge, qui refuse une fiche incomplète.
        """
        ok0, manq, bornes = J.porte_0(f)
        if not ok0:
            raise ValueError("la porte 0 refuse : %s" % manq)
        mod_sig = J.signal_de_la_fiche(base, f)   # le signal que la fiche nomme, lu à un seul endroit (A-542)
        a_jouer = periode if periode is not None else bornes
        # REGARD UNIQUE (R-505 ③, mission REGARD du 12-11-2026) : aucune inscription ici, donc aucun reçu — une version
        # jouée dans la fenêtre du regard unique est REFUSÉE par `jouer` (RegardNonInscrit). Pas 7 (GitHub), hors mission.
        # ESSAI DÉCLARÉ (A-863) : le jeton tient lieu de reçu ; None hors essai, comme avant.
        _recu = {} if jeton is None else {"recu": jeton}   # sans essai, l'appel d'avant, à l'identique
        # LE DÉCOUPAGE DU JOUR MÊME pour une version « quand jouer » (A-1105, lot W2e-FIX) ; « toujours » : aucun
        # argument de plus, l'appel d'avant à l'identique.
        _tm = J.decoupage_pour_la_fiche(base, f)
        if _tm is not None:
            _recu = dict(_recu, types_de_marche=_tm)
        if bareme is None:
            ops, inconnus = J.jouer(f, cours, mnemo, mod_sig, mod_pos, periode=a_jouer, lecture=lecture, **_recu)
        else:
            ops, inconnus = J.jouer(f, cours, mnemo, mod_sig, mod_pos, periode=a_jouer, lecture=lecture,
                                    bareme=bareme, **_recu)
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
        if jeton is not None:   # sous l'option d'essai, refus en 2 comme les autres refus d'essai (M5)
            print("ARRÊT (essai refusé) : la version %s, identique à la fiche, ne retrouve pas la fiche"
                  % ident_v[0]["id_version"])
            return 2
        return arreter("la version %s, identique à la fiche, ne retrouve pas la fiche"
                       % ident_v[0]["id_version"])
    print("  version identique %s : même résultat" % ident_v[0]["id_version"])

    # LA FIN DE LA PÉRIODE JOUÉE SE CALCULE (plan V7, bloc 5g, complément du 11-11-2026 à 20h17) : la plus tardive
    # qui laisse à chaque valeur l'horizon CHIFFRÉ le plus long plus la séance d'achat, sans dépasser la fiche. La
    # fiche n'est pas modifiée ; la fin calculée vit dans la colonne `periode_fin` des résultats.
    # LA DURÉE « AUCUNE » (A-645, mission VENTE du 11-11-2026) N'A PAS D'ÉCHÉANCE : aucune fin calculée ne protège
    # une position ouverte en fin de période. `vendre` la rend à la dernière clôture connue sous le motif
    # FIN_DES_DONNEES, et `resumer` du juge la met À PART, hors du total (décision de Jean-Luc du 12-11-2026 à
    # 09h18) ; elle s'écrit dans les colonnes « à part » des résultats. La fin se calcule sur les durées chiffrées ;
    # le cas « aucune » est DIT ici. Sans aucune durée chiffrée, le besoin est la seule séance d'achat (h_max = 0).
    # UN HORIZON ILLISIBLE (« 0 », « abc ») N'EST PAS ARRÊTÉ ICI : `controler_fusion` l'arrête version par version,
    # avec son motif « horizon lu … » (cas de l'épreuve de la moulinette, 20-10-2026) ; il ne compte pas dans la fin.
    import COMMUN
    _durees = [COMMUN.lire_horizon_ou_aucune(v["horizon"]) for v in versions]
    _aucunes = sum(1 for d in _durees if d is COMMUN.HORIZON_AUCUNE)
    _chiffrees = [d for d in _durees if d is not COMMUN.HORIZON_AUCUNE and d is not None]
    if _aucunes:
        print("DURÉE « AUCUNE » : %d version(s) ; une position encore ouverte à la fin des cours est mise À PART, hors du"
              " total (motif FIN_DES_DONNEES, décision de Jean-Luc du 12-11-2026 à 09h18)" % _aucunes)
    h_max = max(_chiffrees) if _chiffrees else 0
    dates = {}
    for m in sorted({c for v in versions for c in codes(v["univers"])}):
        cle = mnemo.get(m, J.cle_valeur(m))
        dates[m] = [b["date"] for b in cours.get(cle, [])]
    fin, limite = fin_utilisable(dates, bornes[0], bornes[1], h_max)
    if fin is None:
        return arreter("pas assez de cours après la période pour %s et l'horizon %d" % (limite, h_max))
    periode_jouee = (bornes[0], fin)
    recul_max = recul_maximum(h_max)   # CALCULÉ, plus lu dans un fichier (A-1100)
    recul = recul_en_seances(dates, fin, bornes[1])
    print("RECUL DE LA FIN : %d séance(s) · au plus %d (calculé : délai chiffré le plus long %d + 1 ; %s)"
          % (recul, recul_max, h_max, DECISION_DU_RECUL))
    if recul > recul_max:
        # UNE SEULE VALEUR QUI S'ARRÊTE TÔT NE RAMÈNE PAS EN SILENCE LA FIN DE TOUTES LES VERSIONS (D6, 11-11-2026)
        return arreter("la fin calculée recule de %d séances (au plus %d) : ramenée au %s par %s et l'horizon %d ; "
                       "rien n'est joué" % (recul, recul_max, fin, limite, h_max))
    print("PÉRIODE ÉCRITE DANS LA FICHE : %s -> %s · FIN CALCULÉE : %s%s" % (
        bornes[0], bornes[1], fin, " (inchangée)" if limite is None else
        " (ramenée par %s et l'horizon %d ; la fiche n'est pas modifiée)" % (limite, h_max)))
    # LA MARGE SE COMPTE VALEUR PAR VALEUR, ET SE RECOMPTE APRÈS LE CALCUL : compter les séances de toutes les
    # valeurs laissait passer un univers dont les cours s'arrêtaient trois séances après la période (relecture du
    # 08-10-2026, défaut N3). Ce recompte est le garde-fou du calcul : il ne peut rougir que si `fin_utilisable` se
    # trompe.
    marge = {m: sum(1 for d in ds if d > fin) for m, ds in dates.items()}
    plus_court = min(marge, key=marge.get)
    print("PÉRIODE JOUÉE : %s -> %s · cours : %s · marge la plus courte : %s, %d séances après la fin"
          " · horizon max %d" % (periode_jouee[0], periode_jouee[1], f_cours_rel, plus_court, marge[plus_court],
                                 h_max))
    if marge[plus_court] < h_max + 1:
        return arreter("pas assez de cours après la période pour %s et l'horizon %d"
                       % (plus_court, h_max))
    # LA FICHE REJOUÉE SUR LA PÉRIODE CALCULÉE : la version identique doit la retrouver plus bas, sur cette période-là.
    ref_jouee = ref if fin == bornes[1] else jouer_une(dict(fiche), periode=periode_jouee)[0]
    if fin != bornes[1]:
        # AUCUNE OPÉRATION EST UN RÉSULTAT, JAMAIS UN ARRÊT (D5, 11-11-2026) : `resumer` rend alors {"n": 0}, sans « wr ».
        print("  la fiche sur la période jouée : %s" % ("aucune opération" if not ref_jouee["n"] else
              "{} operations . {} % de reussite . {:+,.2f} EUR".format(ref_jouee["n"], ref_jouee["wr"],
                                                                     ref_jouee["net"])))
    # LA PARTIE DE RÉGLAGE (70 %) : coupée par le module de jugement, sur les séances des bornes de la FICHE, comme
    # `juger` le fera (D1, 11-11-2026). LA FRONTIÈRE VIENT DE `frontiere_de_la_fiche`, la seule fonction qui l'établit,
    # appelée aussi par le juge et par le tri (superviseur R-759 de la mission TRI, 12-11-2026) ; le calendrier est
    # celui que `main` du juge construit (`seances = {b["date"] for s in cours.values() for b in s}`).
    mod_jug = J.charger_module(J.trouver(base, "MODULE_JUGEMENT.py"), "jug")
    # `seances_lues` : le calendrier des cours lus, établi une fois, juste après la lecture (contrôle de couverture).
    frontiere = mod_jug.frontiere_de_la_fiche(fiche, seances_lues, bornes)
    if frontiere is None:
        return arreter("aucune séance des cours lus dans les bornes de la fiche : pas de frontière 70/30")
    seances_fiche = {d for d in seances_lues if bornes[0] <= d <= bornes[1]}
    print("PARTIE DE RÉGLAGE : signaux avant la frontière %s, embargo déduit (coupure du module de jugement) ;"
          " SEULE cette partie est écrite dans les colonnes « _70 », les seules que le tri lit" % frontiere)

    # LES CHAMPS DU FICHIER DE RÉSULTATS VIVENT AU CONTRAT : le tri les lit aussi (programmes/TRIER_LES_VARIANTES.py,
    # 11-11-2026) ; un fichier lu par deux programmes se déclare une fois (instructions du projet, §7).
    champs = list(contrat.RESULTATS_DES_VERSIONS)
    if jeton is not None:   # A-863 : la colonne d'essai, hors contrat ; le tri refuse le fichier qui la porte
        champs.append(contrat.COLONNE_DU_STATUT_D_ESSAI)
    colonne_d_essai = {contrat.COLONNE_DU_STATUT_D_ESSAI: contrat.STATUT_D_ESSAI} if jeton is not None else {}
    # L'EMPREINTE DES SEULES SÉANCES JUSQU'À LA FIN DE LA FICHE (M2, 12-11-2026) : le maître grandit chaque soir.
    empreinte_cours = empreinte_des_cours_jusqu_a(os.path.join(base, f_cours_rel), bornes[1])
    # LE TÉMOIN SE COMPARE SOUS SON PROPRE BARÈME (C15, 29-10-2026) : chaque version est jouée deux fois quand le
    # témoin a été fait sous un autre barème que celui des résultats — sous le barème des verdicts pour les résultats
    # écrits, sous celui du témoin pour la comparaison — et l'écart entre les deux doit être EXACTEMENT la taxe
    # payée à l'achat (mêmes opérations ; un achat revendu le jour même ne paie pas la taxe). L'écart n'est la taxe
    # que si les deux barèmes ne diffèrent QUE par elle (courtage seul contre réel) : sinon, arrêt, et c'est voulu.
    b_tem = bareme_du_temoin(f_comb, sid, essai)
    # Les résultats se chiffrent sous le BARÈME DES VERDICTS (le défaut du juge, `MODULE_POSITIONS.BAREME_DES_VERDICTS`,
    # superviseur R-759 tour 2, D2) ; le témoin n'est rejoué à part que s'il a été fait sous un autre barème.
    b_res = J.bareme_des_verdicts(None, mod_pos)
    empreinte_bareme = empreinte_du_bareme(mod_pos, b_res)   # le CONTENU du barème des résultats (I2, 19-11-2026)
    rejouer = b_tem is not None and b_tem != b_res
    vue_du_temoin, invariant_faux = {}, []
    if b_tem is not None:
        print("TÉMOIN FAIT SOUS LE BARÈME %s%s" % (b_tem, " : chaque version est aussi rejouée sous ce barème"
                                                   if rejouer else ""))
    # L'EMPREINTE DES RÉGLAGES DE CHAQUE VERSION, ÉCRITE AU JEU (superviseur R-759 du 14-11-2026, CARNET, §4.2) : le
    # module de signal est lu au jour du jeu, une fois pour toutes les versions.
    lire_module = J.lire_module_du_jour(base)
    # L'EMPREINTE DE LA FICHE DE BASE (superviseur R-759 du 14-11-2026, tour 3, §1.3) : la même fonction, sur la fiche
    # telle qu'elle est jouée ; écrite sur chaque ligne, elle est une condition commune du tri — deux fichiers joués
    # avec un code de module, un signal ou une période différents ne se mêlent plus en un classement.
    empreinte_fiche = J.empreinte_des_reglages(fiche, lire_module)[0]
    provisoire = f_out + ".en_cours"
    cree = False  # on n'efface que ce qu'on a créé (relecture du 08-10-2026, N5)
    try:
        with open(provisoire, "x", encoding="utf-8", newline="") as s:
            cree = True
            w = csv.DictWriter(s, fieldnames=champs)
            w.writeheader()
            jouees = versions if n_tranches is None else tranche(versions, k_tranche, n_tranches)
            if n_tranches is not None:
                print("TRANCHE %d/%d : %d versions sur %d" % (k_tranche, n_tranches, len(jouees), len(versions)))
            for i, v in enumerate(jouees, 1):
                fusion = fusionner(fiche, v)
                ecarts = controler_fusion(J, fusion, v)
                if ecarts:
                    raise ValueError("fusion fausse pour %s : %s" % (v["id_version"], ecarts))
                ops_r = []
                r, b = jouer_une(fusion, None, ops_r, periode_jouee)
                if b != bornes:
                    raise ValueError("période différente pour %s : %s" % (v["id_version"], b))
                # UNE DURÉE « AUCUNE » N'A PAS DE PARTIE DE RÉGLAGE CHIFFRÉE (phase 2 d'E1F, 13-11-2026) : l'embargo de
                # la coupure 70/30 sans durée maximale n'est PAS tranché par Jean-Luc (`juger` refuse par
                # MOTIF_AUCUNE_NON_TRANCHEE ; `duree_d_embargo_sans_horizon` reste une proposition). Les colonnes
                # « _70 » et l'embargo restent VIDES — jamais « 0 » — : le tri lit une case vide comme NON MESURABLE
                # et écarte la version (`passe_le_critere`). Avant ce geste, `int("aucune")` arrêtait toute la moulinette.
                if COMMUN.lire_horizon_ou_aucune(v["horizon"]) is COMMUN.HORIZON_AUCUNE:
                    emb_v, r70 = None, None
                else:
                    emb_v, r70 = partie_de_reglage(mod_jug, ops_r, seances_fiche, int(v["horizon"]), frontiere)
                if v is ident_v[0] and (r["n"], r.get("wr_exact"), r.get("net")) != (
                        ref_jouee["n"], ref_jouee.get("wr_exact"), ref_jouee.get("net")):
                    raise ValueError("la version %s, identique à la fiche, ne retrouve pas la fiche sur la période"
                                     " jouée" % v["id_version"])
                if rejouer:
                    ops_t = []
                    r_t, _ = jouer_une(fusion, b_tem, ops_t, periode_jouee)
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
                w.writerow(dict({"id_version": v["id_version"], "strategie": sid, "essai": essai,
                            "versions_dans_l_essai": len(versions), "tp": v["tp"], "sl": v["sl"],
                            "horizon": v["horizon"], "univers": v["univers"],
                            "empreinte_des_reglages": empreinte_de_la_version(J, fiche, v, lire_module),
                            "empreinte_de_la_fiche": empreinte_fiche,
                            "periode_debut": periode_jouee[0], "periode_fin": periode_jouee[1],
                            "operations": r["n"],
                            "reussite_pourcents_exacte": "%.6f" % r["wr_exact"] if r["n"] else "",
                            "gain_net_euros": "%.2f" % r["net"] if r["n"] else "0.00",
                            "bareme": b_res, "empreinte_du_bareme": empreinte_bareme,
                            "fin_ecrite_dans_la_fiche": bornes[1],
                            "cours_joues": f_cours_rel, "empreinte_des_cours": empreinte_cours,
                            "frontiere_70_30": frontiere, "embargo_seances": "" if emb_v is None else emb_v,
                            "operations_70": "" if r70 is None else r70["n"],
                            "reussite_pourcents_exacte_70": "%.6f" % r70["wr_exact"] if r70 and r70["n"] else "",
                            "gain_net_euros_70": "" if r70 is None else ("%.2f" % r70["net"] if r70["n"] else "0.00"),
                            # LES POSITIONS MISES À PART (R1 du superviseur du tour 3, 13-11-2026 ; décision de
                            # Jean-Luc du 12-11-2026 à 09h18) : hors des trois colonnes du total, écrites ici avec
                            # leur nombre et leur gain ou perte du moment. Une version dont toutes les positions
                            # restent ouvertes ne s'écrit plus « 0 opération, 0,00 € » sans trace.
                            "operations_a_part_fin_des_donnees": r.get("fin_des_donnees", {}).get("n", 0),
                            "gain_net_euros_a_part_fin_des_donnees": "%.2f" % r.get("fin_des_donnees", {}).get(
                                "net", 0.0)}, **colonne_d_essai))
                if i % 250 == 0:
                    print("  %d / %d" % (i, len(jouees)), flush=True)
        if invariant_faux:
            print("L'ÉCART ENTRE LES DEUX BARÈMES N'EST PAS LA TAXE (%d) :" % len(invariant_faux))
            for e in invariant_faux[:10]:
                print("  %s" % e)
            os.remove(provisoire)
            return arreter("l'écart au témoin n'est pas expliqué par la taxe : rien n'est écrit")
        ecarts = comparer_au_temoin(f_comb, sid, essai, vue_du_temoin if rejouer else provisoire,
                                    None if n_tranches is None else {v["id_version"] for v in jouees})
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
    print("ÉCRIT : %s · %d versions" % (f_out, len(jouees)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
