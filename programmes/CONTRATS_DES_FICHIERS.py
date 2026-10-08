#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONTRATS_DES_FICHIERS.py — Dim 13-09-2026 (Paris)
DÉCIDÉ · Rôle : nommer, UNE SEULE FOIS, les champs de chaque fichier que deux programmes se partagent.
Quand l'appeler : par tout programme qui écrit ou lit un fichier de liaison. Jamais recopier ses listes.

① RÔLE — Donner aux dix fichiers par lesquels les programmes du soir se parlent
  une seule liste de noms de champs, écrite à un seul endroit, et confronter
  chaque fichier à sa liste. Sans cela, celui qui écrit et celui qui lit se
  mettent d'accord de mémoire, et personne ne voit qu'ils ne sont pas d'accord.
② CONTEXTE D'APPEL — Trois appelants, relevés le 19-09-2026 en cherchant le nom
  de ce fichier dans tout le dépôt :
  ① .github/workflows/collecte_abc.yml, pas « Confronter les fichiers a leurs
  contrats » : il charge ce fichier comme module sous le nom `c` et appelle
  `confronter_tous` avec la racine du dépôt. Le pas porte `continue-on-error` :
  un écart rougit, il n'arrête pas la collecte des cours.
  ② le même fichier de circuit, dernier pas « Dire quels pas non bloquants sont
  tombes » : il appelle `fabrique_du_jour` deux fois, sur rapports/audit_du_jour.md
  puis sur gouvernance/PILOTE.md.
  ③ programmes/DETECTER_LES_SIGNAUX_GITHUB.py ligne 330, juste avant d'écrire les
  signaux, et programmes/TENIR_LES_POSITIONS.py ligne 1514, juste après les avoir
  lus : tous deux importent `verifier`.
  Les trois passent par un chargement de module, donc aucun des deux blocs de
  lancement de ce fichier ne s'exécute chez eux.
③ ENTRÉE — Aucun paramètre : c'est un programme, pas une fonction. Lancé à la
  main il accepte un argument, la racine du dépôt, qui ne sert jamais (⑨).
  Chargé comme module il ne lit rien : ses appelants passent eux-mêmes la racine.
④ CONDITIONS D'ENTRÉE — Aucune pour être chargé : ce fichier ne fait que déclarer
  des listes et des fonctions. Pour que `confronter_tous` rende un verdict utile,
  les dix fichiers nommés dans la table doivent exister sous la racine donnée.
⑤ SORTIE — Lancé à la main : un code de sortie, et rien d'autre. Chargé comme
  module : rien — ce sont ses fonctions qui rendent des valeurs.
⑥ TRAITEMENT — ① déclarer onze listes de noms de champs, et deux listes de valeurs
  admises : les sources des cours, les comptabilités (depuis le 27-09-2026) ·
  ①bis dire, par `noms_d_une_strategie`, sous quels noms le journal écrit une
  stratégie (depuis le 27-09-2026) · ② déclarer la table qui
  relie dix noms de fichiers à dix de ces listes · ③ définir cinq fonctions ·
  ④ lancé à la main, jouer les six épreuves du contrat des signaux et sortir.
⑦ UNITÉ — Aucune grandeur physique : des NOMS DE CHAMPS et des NOMBRES DE CHAMPS.
  Les dates comparées par deux de ses fonctions sont des JOURS de calendrier, en
  heure de Paris.
⑧ POURQUOI — Ce fichier est né d'un maillon cassé, le 12-09-2026.
  `DETECTER_LES_SIGNAUX_GITHUB` écrivait un signal avec la clé « date ».
  `TENIR_LES_POSITIONS` le lisait en attendant « date_signal ». Aucun des deux
  n'avait tort : ils n'avaient simplement rien en commun. Le jour du premier
  signal, rien ne se serait ouvert — et personne ne l'aurait su, parce qu'un
  programme qui n'a rien à faire et deux programmes qui ne se parlent pas rendent
  le même silence.
  TROIS FAÇONS DE DÉTECTER CE DÉSACCORD ONT ÉTÉ ESSAYÉES, et chacune a appris
  quelque chose :
  · comparer les APPELS — il n'y a aucun appel entre les deux : ce sont deux
    processus, lancés par deux pas du circuit du soir, reliés par un fichier ;
  · comparer les CHAMPS aux deux bouts, autour du fichier — plus juste, mais ni
    le code ni les données ne les portent : les colonnes des deux fichiers
    centraux sont tirées des données elles-mêmes, et le fichier des signaux a sa
    liste de signaux vide presque tous les jours, un signal étant rare par
    construction ;
  · DÉCLARER ce qui se partage — c'est ce fichier, et c'est la règle « ce qui se
    calcule ne s'écrit jamais à la main » (R-728) appliquée aux noms de champs.
  CE QUE ÇA CHANGE : chaque bout se confronte AU CONTRAT, jamais l'un à l'autre.
  « date » et « date_signal » auraient été, l'un des deux, hors contrat, et donc
  visibles du côté où la faute avait été faite.
  CE QUE CE FICHIER N'EST PAS : il ne valide aucune VALEUR. Il nomme des champs
  et donne leur ordre ; il ne dit pas ce qu'on y met, ni leur unité, ni leur
  domaine. C'est le premier niveau, et il attrape la faute du 12-09-2026.
⑨ CE QUI CLOCHE —
  ① Le fichier porte DEUX blocs de lancement, et le second n'est jamais atteint.
  Le premier joue les épreuves puis sort ; le second, plus bas, confronte les dix
  fichiers, contrôle la date de deux fichiers fabriqués et affiche un bilan.
  Mesuré le 19-09-2026 : `python3 programmes/CONTRATS_DES_FICHIERS.py .` affiche
  « CONTRATS DES FICHIERS · épreuves », six lignes vertes, « 6/6 épreuves
  passent », et sort en 0 — la ligne « 10 fichier(s) sous contrat » n'apparaît
  jamais. L'argument de la ligne de commande est donc lu par du code mort, et le
  seul moyen de faire tourner la confrontation est de charger le fichier comme
  module, ce que fait le circuit du soir.
  ② Le texte de ce programme s'est mis à mentir sur son propre contenu. Il
  annonçait « il ne couvre qu'UN fichier de liaison sur les dix recensés », alors
  que les neuf autres ont été écrits le 13-09-2026, plus bas dans ce même
  fichier. Mesuré le 19-09-2026 : la table en porte dix.
  ③ Une onzième liste est déclarée et n'est employée nulle part. Elle décrit
  l'enveloppe du fichier des signaux — la séance, la stratégie, l'heure de calcul
  — mais la table fait pointer signaux_du_jour.json vers la liste des champs d'UN
  signal, pas vers elle. Mesuré le 19-09-2026 : son nom n'apparaît qu'à sa ligne
  de déclaration. Et elle est déjà fausse : le fichier réel porte huit clés, dont
  `univers` et `valeurs_sans_cette_seance`, qu'elle ne nomme pas.
  ④ Deux fonctions de ce fichier font le même travail — dire si un fichier
  fabriqué porte la date du jour — et une seule est appelée. Deux implémentations
  d'une même chose divergent toujours (R-708), et elles ont déjà divergé : le
  19-09-2026, sur le même rapports/audit_du_jour.md, l'une trouve la date du
  17-09-2026 et l'autre répond qu'il n'y a pas de date.
⑩ EFFET — LIT des fichiers, n'en écrit aucun, ne touche pas au réseau. Lancé à la
  main, il affiche huit lignes.
⑪ TERMINAISON — Lancé à la main, SORT DU PROGRAMME : 0 si les six épreuves
  passent, 1 sinon. Chargé comme module, il rend la main après avoir déclaré ses
  listes et ses fonctions. Un de ses appels peut ne pas revenir : `_epreuves`
  appelle `verifier`, qui lève sur un nom de contrat qui ne désigne pas une liste
  de textes.
⑫ DÉFINITIONS
  un contrat : une des listes de noms de champs déclarées dans ce programme
  un fichier de liaison : un fichier qu'un programme écrit et qu'un autre lit,
    seul lien entre deux programmes qui ne s'appellent jamais
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par
    GitHub Actions — collecte, versement, signaux, positions, mesure,
    surveillance.
  le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir, qui contrôle l'ensemble du système et range chacun de ses constats sous un numéro de maillon, par exemple 18-Tâches pour le contrôle des traces laissées par les tâches planifiées.
  le détecteur : programmes/DETECTER_LES_SIGNAUX_GITHUB.py, qui écrit les signaux
    du jour
  le teneur de positions : programmes/TENIR_LES_POSITIONS.py, qui lit les
    signaux et ouvre ou ferme les positions simulées
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
  la table : `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740, qui porte les neuf seuils et le sens de comparaison de chacun
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
  un maillon : un groupe de contrôles du radar, désigné par un numéro et un nom, par exemple 18-Tâches pour le contrôle des traces laissées par les tâches planifiées.
  un signal : le repérage, sur la dernière séance connue, d'une configuration de cours qui déclenche une simulation d'achat.
"""

# ══════════════════════════════════════════════════════════════════════
# donnees/signaux_du_jour.json — écrit par DETECTER, lu par TENIR
# ══════════════════════════════════════════════════════════════════════
# MESURÉ AVANT D'ÊTRE ÉCRIT, le 13-09-2026, sur les deux bouts réels :
#   DETECTER écrit : cci, close, cmf, date, valeur
#   TENIR lit      : date_signal, strategie, valeur
# **Trois champs écrits que personne ne lit, deux champs lus que personne
# n'écrit. Un seul est commun : `valeur`.**
#
# LE CONTRAT TRANCHE, IL NE CONSTATE PAS. Il retient :
#   · `valeur` et `date_signal` — ce qu'il faut pour ouvrir une position ;
#   · `cmf`, `cci`, `close` — ce qui permet de relire un signal sans refaire
#     le calcul, et qui sert au cockpit.
# `strategie` N'EST PAS un champ du signal : le détecteur calcule une règle,
# il ne sait pas quelles stratégies la suivent. C'est l'adaptateur de TENIR qui
# l'ajoute, en lisant l'univers de chaque stratégie AU REGISTRE.

SIGNAL = ["valeur", "date_signal", "cmf", "cci", "close"]

# L'ENVELOPPE du fichier, autour de la liste des signaux.
SIGNAUX_DU_JOUR = ["seance", "strategie", "calcule_le", "signaux",
                   "calibrage", "detail_indicateurs",
                   # écrits par programmes/DETECTER_LES_SIGNAUX_GITHUB.py et lus par
                   # programmes/MESSAGE_DU_SOIR.py, déclarés le 30-09-2026 (relecteur).
                   "univers", "valeurs_sans_cette_seance"]

# LES FICHIERS FABRIQUÉS CHAQUE SOIR ET LE MOTIF DE LEUR DATE, écrits une fois (R-708 :
# deux implémentations d'une même chose divergent toujours). Lus par programmes/
# MESSAGE_DU_SOIR.py, et par le second bloc principal de ce programme — qui ne
# s'exécute jamais, le premier bloc principal sortant avant lui (défaut ancien, relevé
# par le relecteur le 30-09-2026). Le circuit du soir (.github/workflows/
# collecte_abc.yml) en porte encore une copie littérale. Les deux sont consignés au
# BACKLOG sous A-510 (30-09-2026).
FABRIQUES_DU_SOIR = (
    ("rapports/audit_du_jour.md", r"CAC 40 . \w+ (\d{2}-\d{2}-\d{4})", "ecrit"),
    ("gouvernance/PILOTE.md", r"Fabriqu\u00e9 le \w+ (\d{2}-\d{2}-\d{4})", "fabrique"),
)

# LES FICHIERS QUE LES BOUCLES COWORK COPIENT DANS LE DOSSIER DU PROJET (étape 5bis de leur
# texte : la ligne `cp` des programmes, puis celle du registre des stratégies), écrits une
# fois ici, en chemins sous la racine du dépôt. Le 01-10-2026, la fusion a donné à
# programmes/TENIR_LES_POSITIONS.py deux imports (CONTRATS_DES_FICHIERS, COMMUN) que la ligne
# `cp` des boucles ne copiait pas : leurs étapes 3 (signaux) et 5bis (positions) tombaient à
# l'import, et rien au dépôt ne pouvait le voir (relecture de Cowork aff6d33, réponse du Chat
# cc990b8, réparation 51fe7b2 ; décision de Jean-Luc du 01-10-2026 à 16h31 : « Fait ce qu'il
# faut pour réparer professionnellement »). tests/EPREUVES_DE_LA_COPIE_DES_BOUCLES_Jeu_01-10-
# 2026.py rougit quand un programme de cette liste importe, ou charge par son nom de fichier,
# un programme du dépôt absent de la liste, et quand ces seuls fichiers, copiés dans un
# dossier vide, ne refont plus un vrai trade du journal. Le texte des trois boucles doit
# copier exactement ces fichiers : c'est Cowork, seul à lire les tâches, qui le confronte.
COPIE_DES_BOUCLES = (
    "programmes/TENIR_LES_POSITIONS.py",
    "programmes/MODULE_POSITIONS.py",
    "programmes/JUGE_DES_STRATEGIES.py",
    "programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py",
    "programmes/CONTRATS_DES_FICHIERS.py",
    "programmes/COMMUN.py",
    "programmes/MODULE_JUGEMENT.py",
    "donnees/cac40_strategies.csv",
)


def verifier(nom_du_contrat, champs_vus, sens):
    """Confronte des champs AU CONTRAT — jamais un bout à l'autre.

    ① RÔLE — Donner aux deux bouts d'un fichier partagé un juge commun. Celui qui
      écrit et celui qui lit ne se comparent jamais l'un à l'autre : chacun
      compare ses champs à la même liste déclarée dans ce programme. Un champ hors
      contrat est donc une faute contre la référence, et non contre l'autre
      programme : elle se voit du côté où elle a été faite.
    ② CONTEXTE D'APPEL — Trois appelants, relevés le 19-09-2026 en cherchant le
      nom `verifier` dans tout le dépôt :
      ① programmes/DETECTER_LES_SIGNAUX_GITHUB.py, ligne 330, juste AVANT d'écrire
      donnees/signaux_du_jour.json, avec `sens` valant 'ECRIT' ; un écart y arrête
      le programme en code 3 et rien n'est écrit.
      ② programmes/TENIR_LES_POSITIONS.py, ligne 1514, juste APRÈS avoir lu ce
      fichier, avec `sens` valant 'LU' ; un écart y fait rendre 1, et aucune
      position ne s'ouvre.
      ③ `_epreuves`, dans ce même programme, six fois de suite.
    ③ ENTRÉE — `nom_du_contrat` : le nom, en toutes lettres, d'une des listes
      déclarées dans ce programme ; les deux appelants du circuit du soir passent
      tous les deux 'SIGNAL'. `champs_vus` : la liste des noms de champs réellement
      présents, que les deux appelants obtiennent en prenant les clés du premier
      signal du fichier. `sens` : 'ECRIT' du côté de celui qui écrit, 'LU' du côté
      de celui qui lit.
    ④ CONDITIONS D'ENTRÉE — `nom_du_contrat` doit désigner une liste de textes
      déclarée au niveau de ce programme. `champs_vus` doit être une suite de
      textes. `sens` doit valoir exactement 'ECRIT' ou 'LU', en majuscules.
    ⑤ SORTIE — UNE valeur : une liste de phrases, vide si tout tient. Trois formes
      différentes. Contrat inconnu : une seule phrase, « contrat « X » inconnu —
      il n'est pas déclaré ici ». Champ vu que le contrat ne nomme pas : « ECRIT
      « date » : HORS CONTRAT SIGNAL ». Champ du contrat qui n'a pas été écrit :
      « NON ÉCRIT « date_signal » : le contrat SIGNAL le nomme » — et cette
      dernière forme n'est produite que lorsque `sens` vaut 'ECRIT'.
      [rend: 1]
    ⑥ TRAITEMENT — ① chercher, parmi les noms déclarés du programme, celui qui est
      demandé · ② s'il n'existe pas, rendre une seule phrase et s'arrêter là ·
      ③ nommer, par ordre alphabétique, les champs vus que le contrat ne porte
      pas · ④ si `sens` vaut 'ECRIT', nommer en plus les champs du contrat qui
      manquent · ⑤ rendre la liste.
    ⑦ UNITÉ — Un NOMBRE DE CHAMPS. Aucune grandeur physique.
    ⑧ POURQUOI — Le manque est traité différemment selon le sens, et c'est voulu.
      Celui qui ÉCRIT doit fournir tout le contrat : s'il oublie `date_signal`, le
      lecteur ne saura pas de quelle séance vient le signal et ne pourra pas ouvrir
      la position. Celui qui LIT a le droit de n'employer qu'une partie des
      champs : le teneur de positions n'emploie que `valeur` et `date_signal` sur
      les cinq déclarés, et exiger qu'il lise aussi `cmf`, `cci` et `close`
      n'apporterait rien et le ferait rougir à tort.
    ⑨ CE QUI CLOCHE —
      ① N'importe quel nom déclaré dans le programme est accepté comme contrat, y
      compris un nom qui ne désigne pas une liste de champs. Mesuré le 19-09-2026 :
      demander le contrat « verifier » — le nom de la fonction elle-même — arrête
      le programme sur « TypeError: 'function' object is not iterable » ; demander
      le contrat « CONTRATS_PAR_FICHIER » rend sans broncher « LU « a » : HORS
      CONTRAT CONTRATS_PAR_FICHIER », en prenant dix noms de fichiers pour des noms
      de champs. Les deux appelants du circuit du soir n'attrapent que l'absence du
      module : une erreur de type les arrêterait net.
      ② Une valeur de `sens` mal orthographiée éteint la moitié du contrôle sans
      rien dire. Mesuré le 19-09-2026 sur le contrat du signal, avec le seul champ
      `valeur` présenté : 'ECRIT' rend quatre écarts — `cci`, `close`, `cmf` et
      `date_signal` non écrits ; 'ecrit', en minuscules, rend une liste vide. Un
      écrivain qui se tromperait de casse serait déclaré conforme alors qu'il
      n'écrit qu'un champ sur cinq.
      ③ Ni l'ordre des champs ni leur répétition ne sont contrôlés : la comparaison
      se fait sur des ensembles. Un fichier qui porterait deux fois la même colonne
      passerait sans un mot.
    ⑩ EFFET — Aucun. Ne lit aucun fichier, n'écrit rien, n'affiche rien, ne touche
      pas au réseau : elle rend des phrases que son appelant affiche.
    ⑪ TERMINAISON — Rend la main quand ses entrées sont du bon type. PEUT LEVER
      `TypeError`, non rattrapée, si le nom donné désigne autre chose qu'une suite
      de textes — mesuré le 19-09-2026. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      un contrat : une des listes de noms de champs déclarées dans ce programme
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par
        GitHub Actions — collecte, versement, signaux, positions, mesure,
        surveillance.
      le teneur de positions : programmes/TENIR_LES_POSITIONS.py, qui lit les
        signaux et ouvre ou ferme les positions simulées
    
      CCI : l'indice du canal des matières premières, qui mesure de combien le cours s'écarte de sa moyenne récente ; sans unité, typiquement entre −200 et +200.
      CMF : le flux monétaire de Chaikin, qui mesure si l'argent entre ou sort d'une valeur ; sans unité, borné à ±1.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
      le signal : le jour où la stratégie dit d'acheter ; l'achat lui-même a lieu à l'ouverture de la séance suivante
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    attendu = globals().get(nom_du_contrat)
    if attendu is None:
        return [f"contrat « {nom_du_contrat} » inconnu — il n'est pas déclaré ici"]
    ecarts = []
    for c in sorted(set(champs_vus) - set(attendu)):
        ecarts.append(f"{sens} « {c} » : HORS CONTRAT {nom_du_contrat}")
    if sens == "ECRIT":
        for c in sorted(set(attendu) - set(champs_vus)):
            ecarts.append(f"NON ÉCRIT « {c} » : le contrat {nom_du_contrat} le nomme")
    return ecarts


def _epreuves():
    """Le cas fondateur, rejoué : le contrat aurait-il vu le maillon cassé ?

    ① RÔLE — Rejouer sur le contrat d'aujourd'hui le désaccord du 12-09-2026, et
      dire s'il l'aurait vu. C'est la seule preuve que `verifier` fait son travail :
      sans elle, un contrat n'est qu'une liste de mots que personne n'a éprouvée.
    ② CONTEXTE D'APPEL — Le lancement du programme à la main, et lui seul. Aucun
      pas du circuit du soir ne l'appelle : relevé le 19-09-2026, le circuit charge
      ce fichier comme module et appelle `confronter_tous` et `fabrique_du_jour`,
      jamais les épreuves.
    ③ ENTRÉE — Aucun paramètre.
    ④ CONDITIONS D'ENTRÉE — Aucune : elle n'ouvre aucun fichier et se suffit des
      listes déclarées dans ce programme.
    ⑤ SORTIE — UNE valeur : vrai si les six épreuves passent, faux sinon. Les six
      verdicts sont affichés au passage, un par ligne.
      [rend: 1]
    ⑥ TRAITEMENT — ① présenter au contrat du signal le détecteur d'avant la
      correction, qui écrivait « date », et vérifier que « date » est dit hors
      contrat · ② vérifier que « date_signal » est dit non écrit · ③ présenter le
      détecteur corrigé et vérifier qu'aucun écart n'est rendu · ④ vérifier qu'un
      lecteur qui n'emploie que `valeur` et `date_signal` est accepté · ⑤ vérifier
      qu'un lecteur qui attend `strategie` est refusé · ⑥ vérifier qu'un nom de
      contrat inexistant est dit et non ignoré · ⑦ afficher le compte, et rendre
      vrai si les six sont passées.
    ⑦ UNITÉ — Un NOMBRE D'ÉPREUVES PASSÉES, sur six.
    ⑧ POURQUOI — Les six épreuves sont bâties sur un cas réellement survenu et non
      sur un exemple inventé : le 12-09-2026, le détecteur écrivait la clé « date »
      et le teneur de positions lisait « date_signal ». Une épreuve qui reproduit
      un défaut connu prouve que le contrôle l'aurait attrapé ; une épreuve inventée
      ne prouve que l'imagination de son auteur.
      Les épreuves ④ et ⑤ tiennent l'autre moitié de la propriété : un lecteur
      partiel est permis, un lecteur qui attend un champ absent du contrat est
      refusé. Sans elles, un contrôle qui refuserait tout resterait vert.
    ⑨ CE QUI CLOCHE —
      ① Le nombre attendu, six, est écrit à deux endroits de la fonction : dans la
      phrase affichée et dans la comparaison finale. Un chiffre qui existe ailleurs
      ne se recopie pas (R-708) : ajouter une septième épreuve sans toucher aux
      deux endroits fait rendre faux à un jeu qui passe entièrement.
      ② Le verdict porte sur un COMPTE et non sur une propriété. Le critère du
      projet est qu'un garde-fou porte sur une propriété, jamais sur un compte :
      ici, une épreuve supprimée par erreur ferait tomber le total à cinq, ce qui
      se lit comme un contrôle en échec alors que c'est une épreuve disparue.
      ③ Elle n'éprouve qu'un contrat sur onze. Les dix autres listes déclarées dans
      ce programme — positions, trades, mesures, cours maître, cours nouveaux,
      stratégies, lectures, socle, consensus, enveloppe des signaux — ne passent
      aucune épreuve, et rien ne dit qu'elles n'en passent pas.
      ④ Aucune épreuve ne sabote le contrôle lui-même. Toutes présentent des champs
      à `verifier` ; aucune ne vérifie que le jeu rougirait si `verifier` cessait de
      faire son travail.
    ⑩ EFFET — AFFICHE six lignes de verdict, puis une ligne vide et une ligne de
      compte. N'écrit aucun fichier, ne lit rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main. Elle ne lève pas elle-même. Un de ses appels peut
      ne pas revenir : `verifier` lève `TypeError` si le nom de contrat demandé ne
      désigne pas une liste de textes — ce qui n'arrive sur aucun des six jeux
      qu'elle lui donne, mesuré le 19-09-2026, les six épreuves passant.
      [sort: non]
    ⑫ DÉFINITIONS
      un contrat : une des listes de noms de champs déclarées dans ce programme
      le détecteur : programmes/DETECTER_LES_SIGNAUX_GITHUB.py, qui écrit les
        signaux du jour
      le teneur de positions : programmes/TENIR_LES_POSITIONS.py, qui lit les
        signaux et ouvre ou ferme les positions simulées
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par
        GitHub Actions — collecte, versement, signaux, positions, mesure,
        surveillance.
    
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      un garde-fou : une limite qui, franchie, fait cesser a la strategie de prendre position tout en continuant a la mesurer.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    bons = 0
    e = verifier("SIGNAL", ["valeur", "date", "cmf", "cci", "close"], "ECRIT")
    ok = any("date »" in x and "HORS CONTRAT" in x for x in e)
    print(f"  {'✅' if ok else '❌'} le détecteur d'hier, qui écrivait « date » : vu")
    bons += ok
    ok = any("date_signal" in x and "NON ÉCRIT" in x for x in e)
    print(f"  {'✅' if ok else '❌'} et « date_signal » manquant : vu aussi")
    bons += ok
    e2 = verifier("SIGNAL", ["valeur", "date_signal", "cmf", "cci", "close"], "ECRIT")
    print(f"  {'✅' if not e2 else '❌'} le détecteur corrigé : aucun écart")
    bons += (not e2)
    e3 = verifier("SIGNAL", ["valeur", "date_signal"], "LU")
    print(f"  {'✅' if not e3 else '❌'} un lecteur qui n'emploie que deux champs : permis")
    bons += (not e3)
    e4 = verifier("SIGNAL", ["valeur", "strategie"], "LU")
    ok = any("strategie" in x for x in e4)
    print(f"  {'✅' if ok else '❌'} un lecteur qui attend « strategie » : refusé")
    bons += ok
    e5 = verifier("INCONNU", ["a"], "LU")
    print(f"  {'✅' if e5 else '❌'} un contrat qui n'existe pas : dit, pas ignoré")
    bons += bool(e5)
    print(f"\n  {bons}/6 épreuves passent")
    return bons == 6


if __name__ == "__main__":
    import sys
    print("CONTRATS DES FICHIERS · épreuves")
    sys.exit(0 if _epreuves() else 1)

# ═══════════════════════════════════════════════════════════════════
# LES NEUF AUTRES CONTRATS — écrits le 13-09-2026
#
# LA MÉTHODE DE LA PHOTOGRAPHIE v3 l exigeait : « ce qui se partage se déclare ». La
    # photographie est abandonnée depuis le 24-09-2026 (A-452) ; le principe reste écrit
    # dans les instructions du projet, au §7.
# Un seul fichier de liaison sur dix avait son contrat. Les neuf autres le
# reçoivent ici, RELEVÉS SUR LE FICHIER VIVANT et jamais de mémoire :
# l en-tête a été lu, le séparateur mesuré (celui qui donne le plus de
# colonnes), aucun nom n a été deviné.
#
# **CE QUE CE FICHIER N EST PAS** : il ne dit pas ce que les champs SIGNIFIENT,
# ni leur unité, ni leur domaine. Il dit leur NOM et leur ORDRE. C est le
# premier niveau, et il attrape la faute du 12-09 — un détecteur qui écrivait
# « date » quand le teneur lisait « date_signal ».
# ═══════════════════════════════════════════════════════════════════

# positions ouvertes — TENIR_LES_POSITIONS écrit, le cockpit et la mesure lisent
POSITION = [
    "strategie", "valeur", "date_signal", "date_entree",
    "prix_entree", "tp", "sl", "horizon_fin",
    "statut", "comptabilite", "regles_pre_trade", "explication",
]

# journal des trades clos — TENIR_LES_POSITIONS écrit, MESURER_LA_PERFORMANCE lit
# LA COMPTABILITÉ EST UNE COLONNE DEPUIS LE 27-09-2026 (défaut 3 de A-491, choix 1 de
# Jean-Luc à 21h32). Avant, elle n'était écrite que dans le texte de l'explication : la
# vente d'Unibail du 27-08 figurait deux fois par stratégie, une par comptabilité, et
# la mesure comptait les deux lignes dans chacune — « un jeton : 3 operation(s) ·
# cumul 1292.25 EUR » pour un seul trade réel à −2 796,25 €. Le teneur de positions
# remplissait bien la case, mais écrivait avec les colonnes du fichier existant, et
# `extrasaction="ignore"` la jetait sans un mot.
TRADE = [
    "strategie", "valeur", "date_entree", "prix_entree",
    "date_sortie", "prix_sortie", "motif_sortie", "pnl_net_eur",
    "prix_sortie_convention", "pnl_net_convention_eur", "comptabilite",
    "regles_pre_trade", "explication",
]

# LES COMPTABILITÉS ADMISES dans la colonne `comptabilite` des positions et du journal.
# Déclarées ICI une fois ; le teneur de positions et la mesure les importent (R-708 :
# deux implémentations d'une même chose divergent toujours). Une valeur hors de cette
# liste est refusée à l'écriture par le teneur, et arrête la mesure.
# un_jeton : une seule position à la fois par stratégie — ce que Jean-Luc gagnerait.
# jetons_illimites : tout signal est suivi — ce qui dit si la stratégie marche (R-604).
UN_JETON = "un_jeton"
JETONS_ILLIMITES = "jetons_illimites"
COMPTABILITES = (UN_JETON, JETONS_ILLIMITES)
# Les deux se lisent PAR LEUR NOM, jamais par leur rang dans la liste : inverser
# l'ordre de la liste ne doit rien changer (relecteur du Chat, 27-09-2026 : avec
# `UN_JETON, JETONS_ILLIMITES = COMPTABILITES`, inverser la liste appliquait la
# règle « une position à la fois » aux jetons illimités, calibrage toujours vert).

# historique des mesures, empilé jamais écrasé — MESURER écrit, le cockpit lit
MESURE = [
    "date_mesure", "strategie", "comptabilite", "etat",
    "n_operations", "gagnantes", "taux_reussite", "borne_basse_wilson",
    "point_mort", "verdict_c7", "cumul_net_eur", "esperance_eur",
    "facteur_profit", "serie_en_cours", "pertes_consecutives", "pire_chute_pct",
    "pire_chute_eur", "compteur", "seuil", "conformite_promis",
    "voyant_c7", "voyant_pertes", "voyant_chute", "temoin_permanent",
    "temoin_miroir", "rapport_gain_secousses", "source_calibrage",
]

# l historique des cours qui grandit — TENIR_L_HISTORIQUE écrit, tout le reste lit
COURS_MAITRE = [
    "valeur", "date", "open", "high",
    "low", "close", "volume", "source",
]

# LES SOURCES ADMISES dans la huitième colonne du maître — TENIR_L_HISTORIQUE refuse
# toute autre valeur. Cassure de Cowork du 24-09-2026 : une ligne versée avec la source
# « n_importe_quoi » entrait au maître sans un mot. Une source nouvelle s'ajoute ICI,
# sur décision de Jean-Luc, et nulle part ailleurs (R-708).
# CHAQUE SOURCE A SA PÉRIODE, bornes incluses, None = sans borne. Mesuré le 24-09-2026
# dans le maître : google du 2024-01-02 au 2026-09-08, abc à partir du 2026-09-09 —
# date de la bascule de la collecte vers ABC Bourse ; euronext, la bourse elle-même,
# publie tout le passé qu'on lui demande. Relecture de l'agent indépendant du Chat,
# 24-09-2026 : une ligne « abc » datée de 2023 entrait au maître.
SOURCES_ADMISES = {
    "google": (None, "2026-09-08"),
    "abc": ("2026-09-09", None),
    "euronext": (None, None),
}

# la collecte du soir — COLLECTER_ABC écrit, TENIR_L_HISTORIQUE lit
COURS_NOUVEAUX = [
    "valeur", "date", "open", "high",
    "low", "close", "volume",
]

# l état civil des stratégies — Jean-Luc décide, les programmes lisent
STRATEGIE = [
    "id", "nom", "chemin", "indicateurs",
    "tp", "sl", "n_trades", "wr",
    "net_2ans", "ann", "date_test", "statut",
    "note", "entree", "filtres", "kelly",
    "mcl", "horizon", "version", "etat_vie",
    "date_entree_etat", "compteur", "seuil_validation", "wr_promis",
    "wr_constate", "conformite", "forcage", "univers",
    "origine", "bloque_par", "rang_priorite", "etude_ref",
    "periode",
]

# journal des passages de collecte
LECTURE = [
    "horodatage_passage_paris", "modifiedTime_sheet_paris", "derniere_date_vue", "seance_nouvelle_oui_non",
    "statut",
]

# le calendrier de la Bourse de Paris — écrit à la main depuis la page officielle
# d'Euronext, lu par programmes/CALENDRIER_DE_LA_BOURSE.py (30-09-2026, R-758 : il
# reprend au circuit la connaissance des jours fériés que seules les boucles Cowork
# avaient). `etat` vaut FERME, DEMI_SEANCE (la bourse est ouverte), COUVERT_DEPUIS
# ou COUVERT_JUSQU_AU (les bornes au-delà desquelles le fichier ne sait rien).
CALENDRIER = [
    "date", "etat", "source",
]

# qui est vivant — FABRIQUER_LE_SOCLE écrit, le radar lit
SOCLE = [
    "chemin", "etat", "pourquoi", "lu_par",
]

# les extractions Boursorama — module consensus
CONSENSUS = [
    "date_extraction", "date_ref_ouvree", "valeur", "recommandation",
    "dernier_cours", "objectif_cours", "potentiel", "nb_analystes",
    "niveau",
]

# La table qui relie un fichier à son contrat — un seul endroit.
CONTRATS_PAR_FICHIER = {
    "claude_positions_ouvertes.csv": POSITION,
    "claude_journal_trades.csv": TRADE,
    "historique_mesures.csv": MESURE,
    "cours_maitre.csv": COURS_MAITRE,
    "claude_cours_nouveaux.csv": COURS_NOUVEAUX,
    "cac40_strategies.csv": STRATEGIE,
    "claude_journal_lectures.csv": LECTURE,
    "SOCLE.csv": SOCLE,
    "historique_consensus.csv": CONSENSUS,
    "CALENDRIER_EURONEXT.csv": CALENDRIER,
    "signaux_du_jour.json": SIGNAL,
}


def noms_d_une_strategie(ligne_du_registre):
    """Rend les noms sous lesquels le journal des trades peut écrire une stratégie.

    ① RÔLE — Dire, en un seul endroit, quels noms désignent une stratégie du
      registre dans le journal des trades, pour que la mesure et le radar
      rattachent chaque trade à la même stratégie.
    ② CONTEXTE D'APPEL — `main` de MESURER_LA_PERFORMANCE, une fois par stratégie
      vivante, et une fois de plus par stratégie vivante pour dénoncer un nom
      partagé ; le maillon 13 du radar (`audit_ecosysteme.py`), une fois par
      stratégie vivante (QA ou PRODUCTION) du registre ; depuis le 28-09-2026, le
      maillon 17 du radar, jusqu'à trois fois par ligne du registre (toutes les
      lignes, celles en service, celles qui déclarent un univers), et
      `reglages_du_registre` de `TENIR_LES_POSITIONS.py`, une fois par ligne du
      registre, pour ranger seuils et horizon sous chacun des noms.
    ③ ENTRÉE — `ligne_du_registre` : une ligne de `donnees/cac40_strategies.csv`,
      un dictionnaire qui porte `id` et `nom`.
    ④ CONDITIONS D'ENTRÉE — Aucune : une case absente vaut vide.
    ⑤ SORTIE — UNE valeur : un ensemble de textes, vide si la ligne n'a ni
      identifiant ni nom. Exemple réel : la ligne `C5E10-OBS-V1` du registre rend
      {"C5E10-OBS-V1", "COURS_BAS_ARGENT_REVIENT_10"}.
      [rend: 1]
    ⑥ TRAITEMENT — ① prendre l'identifiant, sans espaces autour · ② prendre le
      nom jusqu'à la première parenthèse, sans espaces autour · ③ rendre les deux,
      sans le texte vide.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le journal porte deux écritures d'une même stratégie : le teneur
      de positions écrit l'identifiant depuis le 12-09-2026 (`C5E10-OBS-V1`), les
      lignes plus anciennes le nom court (`COURS_BAS_ARGENT_REVIENT_10`). Le
      rapprochement se fait par ÉGALITÉ, jamais par morceau : par morceau,
      Bureau Veritas, écrit `C5-ETENDU-10`, allait aux deux stratégies, dont les
      noms longs contiennent tous deux ce texte (défaut 3 de A-491, 27-09-2026).
    ⑨ CE QUI CLOCHE — Un nom court n'est pas unique au registre : mesuré le
      27-09-2026 par le relecteur du Chat, 28 noms y désignent plusieurs lignes,
      par exemple « Signal RAV — Retour a la Valeur » pour `C4-RAV` et
      `C4-RAV-RETEST`. Sans effet sur les deux stratégies vivantes ce jour-là. Le
      radar écarte et signale un nom qui désignerait deux stratégies vivantes ;
      la mesure le signale aussi, mais compte les mêmes trades dans les deux —
      consigné dans A-493.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    return {(ligne_du_registre.get("id") or "").strip(),
            (ligne_du_registre.get("nom") or "").split(" (")[0].strip()} - {""}


def date_ecrite(base, chemin, motif):
    """Lit la date (et l heure, si elle suit) qu un fichier fabriqué porte dans son en-tête.

    ① RÔLE — Porter à UN SEUL endroit la lecture de la date d écriture d un fichier
      fabriqué. Deux façons de lire la même date divergent toujours (R-708) :
      `fabrique_du_jour` la compare au jour, programmes/FAUT_IL_RATTRAPER.py la
      compare à la séance attendue, programmes/MESSAGE_DU_SOIR.py l affiche ; tous
      la prennent ici.
    ② CONTEXTE D'APPEL — `fabrique_du_jour`, dans ce programme ;
      programmes/FAUT_IL_RATTRAPER.py ; programmes/MESSAGE_DU_SOIR.py.
    ③ ENTRÉE — `base` : la racine du dépôt · `chemin` : le fichier sous cette racine,
      avec des barres obliques · `motif` : l expression qui capture la date dans son
      premier groupe, par exemple celle de FABRIQUES_DU_SOIR pour
      rapports/audit_du_jour.md.
    ④ CONDITIONS D'ENTRÉE — La date se trouve dans les 600 premiers caractères, et le
      groupe rend trois nombres séparés par des tirets, année en tête ou en queue.
    ⑤ SORTIE — TROIS valeurs : la date en AAAA-MM-JJ, ou None · l heure en HH:MM
      quand l en-tête l écrit juste après la date sous la forme « 20h21 », sinon
      None · la raison quand la date manque (« ABSENT » si le fichier n existe pas,
      « SANS DATE » si le motif ne trouve rien), ou None quand la date est lue.
      [rend: 3]
    ⑥ TRAITEMENT — ① composer le chemin · ② dire l absence · ③ lire 600 caractères ·
      ④ chercher le motif · ⑤ remettre la date en année-mois-jour · ⑥ lire l heure
      qui suit la date, s il y en a une.
    ⑦ UNITÉ — Une date du calendrier ; une heure de Paris, telle que l écrit le
      fichier.
    ⑧ POURQUOI — Extraite de `fabrique_du_jour` le 01-10-2026, quand un deuxième
      programme a eu besoin de la même date : le rattrapage du matin (A-515,
      décision de Jean-Luc du 01-10-2026 à 00h01, « 1 »). L heure s y ajoute le même
      jour (relecteur) : un rapport écrit le matin et un rapport écrit le soir
      portent la même date, et seul l ordre des heures dit lequel suit le calcul
      des signaux.
    ⑨ CE QUI CLOCHE — Un motif sans groupe de capture, ou une date écrite avec des
      barres obliques, lève IndexError (mesuré le 19-09-2026 sur `fabrique_du_jour`,
      dont c est le corps).
    ⑩ EFFET — Lit les 600 premiers caractères du fichier.
    ⑪ TERMINAISON — Rend la main ; peut lever IndexError (voir ⑨).
      [sort: non]
    """
    import re as _re, os as _os
    p = _os.path.join(base, *chemin.split("/"))
    if not _os.path.isfile(p):
        return None, None, "ABSENT"
    t = open(p, encoding="utf-8", errors="replace").read(600)
    m = _re.search(motif, t)
    if not m:
        return None, None, "SANS DATE"
    ecrit = m.group(1)
    # le motif peut rendre AAAA-MM-JJ ou JJ-MM-AAAA : on normalise
    n = ecrit.split("-")
    h = _re.match(r"\s+(\d{2})h(\d{2})\b", t[m.end(1):])
    return ((ecrit if len(n[0]) == 4 else f"{n[2]}-{n[1]}-{n[0]}"),
            (f"{h.group(1)}:{h.group(2)}" if h else None), None)


def fabrique_du_jour(base, chemin, motif, quoi):
    """Dit si un fichier FABRIQUE porte la date d aujourd hui.

    ① RÔLE — Dire si un fichier refait chaque soir porte bien la date du jour.
      Le 16-09-2026, les deux fichiers que le rituel de début de session fait lire
      — rapports/audit_du_jour.md et gouvernance/PILOTE.md — étaient figés depuis
      trois jours : ils étaient commités par le même pas du circuit, ce pas
      tombait, et tous les passages restaient verts. Le rapport lu ce matin-là
      datait du dimanche précédent, et son lecteur a cru lire celui du jour. Un
      contrôle de date a été posé sur le rapport le matin même ; le PILOTE n'en
      avait toujours pas, alors qu'il porte déjà sa date en tête sous la forme
      « Fabriqué le ... » — le même défaut, le même jour, et un seul des deux
      surveillé. Cette fonction couvre les deux, et tout fichier fabriqué à venir.
    ② CONTEXTE D'APPEL — Un seul appelant, relevé le 19-09-2026 :
      .github/workflows/collecte_abc.yml, dernier pas « Dire quels pas non
      bloquants sont tombes », qui charge ce programme comme module et appelle la
      fonction deux fois de suite, une fois par fichier surveillé. Ce pas est le
      dernier du circuit parce que le rapport du radar est écrit par un pas
      antérieur : appelée plus tôt, la fonction trouverait la date de la veille et
      rougirait chaque soir.
    ③ ENTRÉE — `base` : la racine du dépôt ; l'appelant passe la variable
      d'environnement GITHUB_WORKSPACE, et un point à défaut. `chemin` : le chemin
      du fichier surveillé sous cette racine, écrit avec des barres obliques ; les
      deux valeurs réellement passées sont « rapports/audit_du_jour.md » et
      « gouvernance/PILOTE.md ». `motif` : l'expression qui trouve la date dans
      l'en-tête du fichier et la capture dans son premier groupe ; l'appelant passe
      pour le premier fichier un motif qui cherche « CAC 40 », un caractère, un
      mot, puis une date en jour-mois-année, et pour le second un motif qui cherche
      « Fabriqué le », un mot, puis la même forme de date. `quoi` : le verbe à
      insérer dans la phrase de reproche — « ecrit » pour le premier fichier,
      « fabrique » pour le second.
    ④ CONDITIONS D'ENTRÉE — Le motif doit porter exactement un groupe de capture,
      et ce groupe doit rendre une date séparée par des tirets, écrite soit
      année-mois-jour, soit jour-mois-année. La date doit se trouver dans les 600
      premiers caractères du fichier : au-delà, elle n'est pas lue. Mesuré le
      19-09-2026 sur rapports/audit_du_jour.md, ces 600 caractères couvrent les dix
      premières lignes, et la date est en première ligne.
    ⑤ SORTIE — UNE valeur, de deux natures. Rien du tout quand le fichier porte la
      date du jour. Sinon une phrase à afficher, de trois formes : fichier absent,
      date introuvable dans l'en-tête, ou date différente de celle du jour. Exemple
      réel, mesuré le 19-09-2026 sur le dépôt : « rapports/audit_du_jour.md : ecrit
      le 17-09-2026, aujourd hui est le 2026-09-19 — LE CIRCUIT DU SOIR N A PAS
      TOURNE ».
      [rend: 1]
    ⑥ TRAITEMENT — ① lire la date par `date_ecrite` (depuis le 01-10-2026 : elle
      compose le chemin, dit l'absence, lit les 600 premiers caractères, cherche le
      motif et remet la date en année-mois-jour) · ② rendre une phrase si le
      fichier n'existe pas · ③ rendre une phrase si le motif ne trouve rien · ④ la
      comparer à la date du jour à Paris · ⑤ rendre une phrase si elles diffèrent,
      avec la date en jour-mois-année, rien sinon.
    ⑦ UNITÉ — Des JOURS de calendrier, en heure de Paris. Aucune heure n'est
      comparée : un fichier écrit à 00 h 05 et un fichier écrit à 23 h 55 le même
      jour sont également du jour.
    ⑧ POURQUOI — La fonction ne connaît aucun fichier par son nom : l'appelant lui
      donne le chemin, le motif et le verbe. Le critère du projet tient en une
      question — si je renomme un fichier, mon contrôle change-t-il d'avis ? Ici
      non ; surveiller un fichier fabriqué de plus coûte une ligne chez l'appelant,
      et aucune ici. La forme contraire vit dans ce même programme :
      `audit_du_jour_est_du_jour` épelle son fichier et son motif, et elle ne
      trouve plus la date depuis que l'en-tête qu'elle cherche a été retiré.
      Et le contrôle ne juge pas le CONTENU : il compare deux dates. Un rapport
      périmé est complet, cohérent et faux ; aucune lecture de son texte ne le
      trahit, seule sa date le fait.
    ⑨ CE QUI CLOCHE —
      ① Un motif mal formé arrête le programme au lieu de rendre une phrase.
      Mesuré le 19-09-2026 : un motif sans groupe de capture s'arrête sur
      « IndexError: no such group », et un motif qui capture une date écrite avec
      des barres obliques, « 19/09/2026 », s'arrête sur « IndexError: list index
      out of range » au moment de la découpe par tirets. Le motif venant de
      l'appelant, une faute de frappe chez lui tombe ici. Le pas du circuit qui
      l'appelle se termine par une instruction qui avale l'échec : l'arrêt y
      passerait inaperçu.
      ② La phrase rendue affirme une cause qu'elle n'a pas mesurée : « LE CIRCUIT
      DU SOIR N A PAS TOURNE ». La fonction n'a comparé que deux dates. Mesuré le
      19-09-2026 sur le dépôt, les deux fichiers portent le 17-09-2026 et la phrase
      accuse le circuit entier, alors qu'un seul pas peut être tombé, ou que le
      circuit peut simplement ne pas tourner le week-end.
      ③ La date reprochée et la date du jour ne s'écrivent pas de la même façon
      dans la même phrase. Mesuré le 19-09-2026 : « ecrit le 17-09-2026, aujourd
      hui est le 2026-09-19 ». Le lecteur doit retourner l'une des deux pour les
      comparer, et c'est justement la comparaison qui est en jeu.
      ④ Un fichier daté du lendemain est traité comme un fichier périmé, avec la
      même phrase « N A PAS TOURNE ». La fonction ne compare pas deux dates dans le
      temps, elle regarde seulement si elles sont égales.
    ⑩ EFFET — LIT les 600 premiers caractères du fichier désigné. N'écrit rien,
      n'affiche rien, ne touche pas au réseau. Charge quatre modules du langage à
      chaque appel plutôt qu'une fois pour toutes.
    ⑪ TERMINAISON — Rend la main dans tous les cas prévus. PEUT LEVER `IndexError`,
      non rattrapée, sur un motif sans groupe de capture ou sur une date qui n'est
      pas séparée par des tirets — les deux mesurés le 19-09-2026. Aucun de ses
      appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      un fichier fabriqué : un fichier qu'un programme réécrit en entier à chaque
        passage, et que personne n'édite à la main
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par
        GitHub Actions — collecte, versement, signaux, positions, mesure,
        surveillance.
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir, qui contrôle l'ensemble du système et range chacun de ses constats sous un numéro de maillon, par exemple 18-Tâches pour le contrôle des traces laissées par les tâches planifiées.
      le rituel de début de session : les gestes imposés à l'ouverture d'une
        conversation — relever la date, cloner le dépôt, lire le PILOTE, lire le
        rapport du radar
    
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      un motif : un morceau de nom passé à une fonction de recherche, par exemple trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    from datetime import datetime as _DT
    from zoneinfo import ZoneInfo as _ZI
    ecrit_iso, _heure, raison = date_ecrite(base, chemin, motif)
    if raison == "ABSENT":
        return f"{chemin} ABSENT — le rituel de session lit un fichier qui n existe pas"
    if raison:
        return (f"{chemin} ne porte PAS sa date d ecriture — "
                f"impossible de savoir s il est du jour")
    # la phrase dit la date en jour-mois-année, comme l écrivent les deux fichiers
    # surveillés (FABRIQUES_DU_SOIR) : la phrase reste celle d avant le 01-10-2026
    ecrit = f"{ecrit_iso[8:10]}-{ecrit_iso[5:7]}-{ecrit_iso[:4]}"
    auj = _DT.now(_ZI("Europe/Paris"))
    if ecrit_iso != auj.strftime("%Y-%m-%d"):
        return (f"{chemin} : {quoi} le {ecrit}, aujourd hui est le "
                f"{auj.strftime('%Y-%m-%d')} — LE CIRCUIT DU SOIR N A PAS TOURNE")
    return None


def audit_du_jour_est_du_jour(base):
    """Dit si `rapports/audit_du_jour.md` a ete ecrit AUJOURD HUI.

    ① RÔLE — Dire si le rapport du radar a été écrit aujourd'hui. C'est la première
      version du contrôle de date, écrite le 16-09-2026 pour ce seul fichier.
      `fabrique_du_jour`, dans ce même programme, fait le même travail pour
      n'importe quel fichier fabriqué, et c'est elle que le circuit du soir appelle.
    ② CONTEXTE D'APPEL — Aucun appelant. Recherche du nom
      `audit_du_jour_est_du_jour` dans les fichiers de programme, de circuit et de
      documentation du dépôt le 19-09-2026 : il n'apparaît qu'à sa propre ligne de
      définition.
    ③ ENTRÉE — `base` : la racine du dépôt sous laquelle chercher
      rapports/audit_du_jour.md. Aucun appelant, donc aucune valeur réellement
      passée.
    ④ CONDITIONS D'ENTRÉE — Le fichier rapports/audit_du_jour.md doit porter, dans
      ses 400 premiers caractères, la mention « ECRIT LE » suivie d'une date écrite
      année-mois-jour.
    ⑤ SORTIE — UNE valeur, de deux natures. Rien du tout si la date lue est celle
      du jour. Sinon une phrase à afficher, de trois formes : fichier absent,
      mention de date introuvable, ou date différente de celle du jour.
      [rend: 1]
    ⑥ TRAITEMENT — ① composer le chemin rapports/audit_du_jour.md sous la racine ·
      ② rendre une phrase si le fichier n'existe pas · ③ lire ses 400 premiers
      caractères · ④ y chercher « ECRIT LE » suivi d'une date, et rendre une phrase
      s'il n'y en a pas · ⑤ comparer cette date à celle du jour à Paris · ⑥ rendre
      une phrase si elles diffèrent, rien sinon.
    ⑦ UNITÉ — Des JOURS de calendrier, en heure de Paris.
    ⑧ POURQUOI — Le contrôle compare deux dates et ne juge pas le contenu : un
      rapport périmé est complet et cohérent, et rien dans son texte ne dit qu'il a
      trois jours. C'est exactement ce qui s'est produit le 16-09-2026 : le radar
      écrivait un fichier au nom daté, le circuit du soir en commitait un au nom
      fixe, les deux ne se rencontraient jamais, le fichier lu au rituel du matin
      datait du 13-09-2026 — et il portait sa date, sans que rien au monde ne la
      compare à celle du jour.
    ⑨ CE QUI CLOCHE —
      ① Elle ne trouve plus jamais la date, parce qu'elle cherche une mention qui
      n'existe plus. « ECRIT LE » a été ajouté en tête du rapport le matin du
      17-09-2026 puis retiré l'après-midi, un second écrivain sur le même fichier
      ayant été jugé pire que le défaut qu'il réparait. Mesuré le 19-09-2026 :
      compter les « ECRIT LE » dans rapports/audit_du_jour.md donne 0, et la
      fonction rend « rapports/audit_du_jour.md ne porte PAS sa date d ecriture —
      impossible de savoir s il est du jour ». Le fichier porte pourtant sa date,
      en première ligne : « # AUDIT ÉCOSYSTÈME CAC 40 — Jeu 17-09-2026 23h56
      (Paris) ».
      ② Elle épelle ce que sa voisine tient par une propriété : le chemin, le motif
      et le verbe sont écrits dans son corps, alors que `fabrique_du_jour` les reçoit
      de son appelant. Deux implémentations d'une même chose divergent toujours
      (R-708), et elles ont déjà divergé : le 19-09-2026, sur le même fichier, la
      voisine trouve la date du 17-09-2026 et celle-ci répond qu'il n'y a pas de
      date.
      ③ C'est du code mort qui reste vert. Personne ne l'appelle, aucune épreuve ne
      la joue, et son défaut ① n'apparaît qu'en l'appelant à la main.
    ⑩ EFFET — LIT les 400 premiers caractères de rapports/audit_du_jour.md. N'écrit
      rien, n'affiche rien, ne touche pas au réseau. Charge quatre modules du
      langage à chaque appel.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas : son motif porte un
      groupe de capture, et la date qu'il accepte est déjà en année-mois-jour, donc
      aucune découpe n'est faite. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir, qui contrôle l'ensemble du système et range chacun de ses constats sous un numéro de maillon, par exemple 18-Tâches pour le contrôle des traces laissées par les tâches planifiées.
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par
        GitHub Actions — collecte, versement, signaux, positions, mesure,
        surveillance.
      le rituel de début de session : les gestes imposés à l'ouverture d'une
        conversation — relever la date, cloner le dépôt, lire le PILOTE, lire le
        rapport du radar
      un fichier fabriqué : un fichier qu'un programme réécrit en entier à chaque
        passage, et que personne n'édite à la main
    
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    import re as _re, os as _os
    from datetime import datetime as _DT
    from zoneinfo import ZoneInfo as _ZI
    p = _os.path.join(base, "rapports", "audit_du_jour.md")
    if not _os.path.isfile(p):
        return "rapports/audit_du_jour.md ABSENT — le rituel de session lit un fichier qui n existe pas"
    t = open(p, encoding="utf-8", errors="replace").read(400)
    m = _re.search(r"ECRIT LE (\d{4}-\d{2}-\d{2})", t)
    if not m:
        return ("rapports/audit_du_jour.md ne porte PAS sa date d ecriture — "
                "impossible de savoir s il est du jour")
    ecrit = m.group(1)
    auj = _DT.now(_ZI("Europe/Paris")).strftime("%Y-%m-%d")
    if ecrit != auj:
        return (f"rapports/audit_du_jour.md a ete ecrit le {ecrit}, aujourd hui est le {auj} — "
                f"LE CIRCUIT DU SOIR N A PAS TOURNE, et son verdict est perime")
    return None


def confronter_tous(base):
    """Confronte CHAQUE fichier de liaison à son contrat. Rend la liste des écarts.

    ① RÔLE — Donner leur valeur aux listes déclarées dans ce programme. Une liste
      de champs qui n'est jamais confrontée au fichier est une déclaration
      d'intention : le fichier peut perdre une colonne, en gagner une ou en
      renommer une, et rien ne le dit. Cette fonction ouvre les dix fichiers de
      liaison, lit leur en-tête et nomme chaque écart.
    ② CONTEXTE D'APPEL — Un seul appelant, relevé le 19-09-2026 :
      .github/workflows/collecte_abc.yml, pas « Confronter les fichiers a leurs
      contrats », qui charge ce programme comme module sous le nom `c` et appelle la
      fonction avec la racine du dépôt. Le pas sort en 1 dès qu'un écart est rendu,
      mais il porte `continue-on-error` : il rougit, il n'arrête pas la collecte des
      cours.
    ③ ENTRÉE — `base` : la racine sous laquelle chercher les dix fichiers.
      L'appelant passe la variable d'environnement GITHUB_WORKSPACE.
    ④ CONDITIONS D'ENTRÉE — La racine doit être un dossier lisible. Aucun fichier
      n'est exigé : un fichier manquant est rendu comme écart, jamais comme erreur.
    ⑤ SORTIE — UNE valeur : une liste de phrases, vide quand chaque fichier porte
      exactement les champs de son contrat — ce qui était le cas le 19-09-2026 sur
      le dépôt. Cinq formes différentes : introuvable · illisible, pour un fichier
      de signaux mal formé · vide, pas même un en-tête · N champs du contrat
      absents · N champs hors contrat.
      [rend: 1]
    ⑥ TRAITEMENT — ① pour chacun des dix noms de la table, parcourir l'arborescence
      sous la racine en sautant les dossiers archives, .git, __pycache__ et
      _site_travail, jusqu'à trouver un fichier de ce nom · ② rendre un écart si
      aucun n'est trouvé · ③ pour le fichier de signaux, le charger et passer au
      suivant si sa liste de signaux est vide, sinon prendre les clés de son premier
      signal · ④ pour un fichier en colonnes, prendre la première ligne qui n'est ni
      vide ni un commentaire, choisir comme séparateur celui des trois — point-
      virgule, virgule, tabulation — qui découpe cette ligne en le plus de morceaux,
      puis découper · ⑤ nommer les champs du contrat absents, puis les champs
      présents que le contrat ne nomme pas.
    ⑦ UNITÉ — Un NOMBRE DE CHAMPS, et un nombre de fichiers. Aucune grandeur
      physique.
    ⑧ POURQUOI — Le séparateur n'est pas supposé, il est mesuré sur l'en-tête
      lui-même. Les dix fichiers ne sont pas écrits de la même façon : mesuré le
      19-09-2026, donnees/cours_maitre.csv sépare ses colonnes par des virgules et
      gouvernance/SOCLE.csv par des points-virgules. Un contrôle qui supposerait la
      virgule verrait dans le second une seule colonne nommée
      « chemin;etat;pourquoi;lu_par », et rendrait un écart faux sur un fichier
      juste.
      Les lignes de commentaire sont sautées pour la même raison d'observation :
      gouvernance/SOCLE.csv commence par trois lignes de commentaire, dont deux
      entre guillemets, et son en-tête n'est qu'en quatrième ligne.
      Et la fonction ne corrige rien. Un écart peut être une régression comme une
      évolution voulue — une colonne ajoutée exprès la veille. Trancher appartient à
      Jean-Luc : le contrôle rend l'écart lisible, il ne décide pas.
    ⑨ CE QUI CLOCHE —
      ① Le fichier des signaux n'est presque jamais contrôlé. Quand sa liste de
      signaux est vide, la fonction passe au suivant sans rien dire — et un signal
      est rare par construction. Mesuré le 19-09-2026 : donnees/signaux_du_jour.json
      porte une liste de signaux vide, la fonction rend zéro écart, et le seul
      contrat pour lequel des épreuves existent n'a pas été confronté du tout. Le
      pas du circuit affiche alors le même silence que si tout avait été vérifié.
      ② Deux fichiers de même nom à deux endroits : le premier trouvé gagne, et
      rien ne dit qu'il y en a un second. Mesuré le 19-09-2026 dans un dossier
      d'épreuve portant deux fichiers nommés SOCLE.csv, l'un conforme, l'autre
      réduit à deux colonnes nommées X et Y : le parcours rencontre d'abord le
      conforme, la fonction rend zéro écart, et la copie fautive n'est jamais
      ouverte. Le projet tient deux fichiers de même nom à deux endroits pour un
      défaut et jamais pour une intention ; ce contrôle ne le voit pas.
      ③ Les dossiers écartés du parcours sont épelés par leur nom : archives, .git,
      __pycache__, _site_travail. Un dossier de travail créé demain sous un autre
      nom sera parcouru, et une copie qu'il contient pourra être prise pour le
      fichier officiel.
      ④ La liste des champs en écart est coupée à cinq noms sans le dire. Mesuré le
      19-09-2026 sur un fichier d'épreuve réduit aux colonnes a et b : la phrase
      rendue est « historique_mesures.csv : 27 champ(s) du contrat ABSENT(s) —
      date_mesure, strategie, comptabilite, etat, n_operations ». Le compte est
      juste, la liste en montre cinq sur vingt-sept, et rien ne signale la coupure.
      ⑤ Quand aucun des trois séparateurs n'est présent, le point-virgule est choisi
      quand même et l'en-tête entier devient un seul nom de champ. Mesuré le
      19-09-2026 sur un en-tête séparé par des espaces : « cours_maitre.csv : 1
      champ(s) HORS CONTRAT — valeur date open high low close volume source ».
      L'écart est bien signalé, mais la cause affichée est un nom de colonne absurde
      et non « séparateur introuvable ».
      ⑥ Le module de lecture des fichiers en colonnes est chargé et jamais employé :
      il est importé en tête de la fonction, et aucun appel ne s'en sert. Le
      découpage est fait à la main, ce qui ignore les guillemets : un nom de colonne
      contenant le séparateur serait coupé en deux.
    ⑩ EFFET — LIT l'arborescence sous la racine, puis la première ligne utile de
      chacun des fichiers trouvés — ou le contenu entier pour le fichier de signaux,
      qui est chargé en mémoire. N'écrit rien, n'affiche rien, ne touche pas au
      réseau.
    ⑪ TERMINAISON — Rend la main dans tous les cas prévus. Elle ne lève pas sur un
      fichier de signaux mal formé : l'échec de chargement est rattrapé et rendu
      comme écart. Elle peut lever si un fichier trouvé ne s'ouvre pas du tout, par
      exemple faute de droits de lecture. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      un contrat : une des listes de noms de champs déclarées dans ce programme
      un fichier de liaison : un fichier qu'un programme écrit et qu'un autre lit,
        seul lien entre deux programmes qui ne s'appellent jamais
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par
        GitHub Actions — collecte, versement, signaux, positions, mesure,
        surveillance.
    
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      la table : `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740, qui porte les neuf seuils et le sens de comparaison de chacun
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
      le projet : le dossier reçu sur la ligne de commande, celui que le radar examine
      un signal : le repérage, sur la dernière séance connue, d'une configuration de cours qui déclenche une simulation d'achat.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    import csv as _csv, json as _json, os as _os
    ecarts = []
    for nom, attendus in CONTRATS_PAR_FICHIER.items():
        chemin = None
        for r, sd, fs in _os.walk(base):
            sd[:] = [x for x in sd if x not in ("archives", ".git", "__pycache__", "_site_travail")]
            if nom in fs:
                chemin = _os.path.join(r, nom); break
        if chemin is None:
            ecarts.append(f"{nom} : INTROUVABLE — un contrat sans fichier est un lien mort")
            continue
        if nom.endswith(".json"):
            try:
                d = _json.load(open(chemin, encoding="utf-8"))
            except Exception as e:
                ecarts.append(f"{nom} : ILLISIBLE ({type(e).__name__})"); continue
            sg = d.get("signaux") or []
            if not sg:
                continue   # pas de signal ce jour-la : rien a confronter, et ce n est pas un ecart
            trouves = list(sg[0].keys())
        else:
            ligne = None
            for l in open(chemin, encoding="utf-8-sig", errors="replace"):
                if l.strip() and not l.startswith("#") and not l.startswith(chr(34) + "#"):
                    ligne = l.rstrip("\n\r"); break
            if ligne is None:
                ecarts.append(f"{nom} : VIDE — pas même un en-tête"); continue
            sep = max((";", ",", "\t"), key=lambda x: ligne.count(x))
            trouves = [c.strip().strip(chr(34)) for c in ligne.split(sep)]
        manquants = [c for c in attendus if c not in trouves]
        surnumeraires = [c for c in trouves if c not in attendus]
        if manquants:
            ecarts.append(f"{nom} : {len(manquants)} champ(s) du contrat ABSENT(s) — "
                          + ", ".join(manquants[:5]))
        if surnumeraires:
            ecarts.append(f"{nom} : {len(surnumeraires)} champ(s) HORS CONTRAT — "
                          + ", ".join(surnumeraires[:5]))
    return ecarts


if __name__ == "__main__":
    import sys as _sys
    base = _sys.argv[1] if len(_sys.argv) > 1 else "."
    ec = confronter_tous(base)
    # LES DEUX FICHIERS QUE LE RITUEL FAIT LIRE, surveilles de la meme facon.
    # LE MOTIF SE CALIBRE SUR L EN-TETE QUE LE PROGRAMME ECRIT VRAIMENT.
    # Mon premier motif cherchait « ECRIT LE AAAA-MM-JJ » — un en-tete que
    # j avais ajoute le matin puis RETIRE l apres-midi, quand Cowork a
    # montre qu il creait un second ecrivain sur le fichier.
    # **Le controle cherchait donc une ligne qui n existait plus, et
    # rendait « ne porte PAS sa date » sur un fichier qui la porte.**
    # Le radar ecrit : « # AUDIT ECOSYSTEME CAC 40 — Mer 16-09-2026 17h50 ».
    # Les deux fichiers et leurs motifs vivent dans FABRIQUES_DU_SOIR (30-09-2026).
    for _ch, _mo, _q in FABRIQUES_DU_SOIR:
        _d = fabrique_du_jour(base, _ch, _mo, _q)
        if _d:
            ec = list(ec) + [_d]
    print(f"  {len(CONTRATS_PAR_FICHIER)} fichier(s) sous contrat")
    if ec:
        print(f"  *** {len(ec)} ECART(S) ***")
        for e in ec:
            print("   !!", e)
        _sys.exit(1)
    print("  aucun ecart : chaque fichier porte exactement les champs de son contrat")
