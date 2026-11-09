#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DÉCIDÉ · outil · v1.0 · 28-08-2026 · Rôle : rendre les onze mesures qui disent
si une stratégie vaut quelque chose. Quand l'appeler : par le juge des stratégies,
jamais directement.

CE QU'IL NE FAIT PAS
    Il rend des chiffres. Pas de verdict oui / non : la grille qui le rendra (A-210) n'est pas encore figée.
    Il n'implemente AUCUNE des neuf fonctions qui existent deja dans le module
    de statistiques — Wilson, creux maximal, Sharpe, mirage, Kelly, voisinage,
    fenetres glissantes. Il les APPELLE (R-708).

CE QU'IL AJOUTE, ET QUI MANQUAIT
    le point mort · les observations independantes (mesurees, n°106 ; ex-episodes)
    · la coupure 70/30 avec nettoyage
    de la frontiere · la borne basse du gain moyen · l'etalon de hasard · la
    courbe de capital QUOTIDIENNE · le glissement · le temoin miroir.

① RÔLE — Porter à un seul endroit les mesures qui disent si le gain d'une
  STRATÉGIE veut dire quelque chose. Le juge des stratégies rejoue une stratégie sur
  l'historique des cours et rend la liste des opérations qu'elle aurait faites,
  chacune avec son gain net en euros. Ce gain ne suffit pas à juger : il peut
  venir d'un seul épisode de marché, reposer sur trop peu d'opérations, ou être
  battu par des entrées tirées au sort. Ce module rend les chiffres qui
  répondent à ces objections, et il ne conclut jamais lui-même. Mesuré le
  19-09-2026 en lançant `python3 programmes/MODULE_JUGEMENT.py` dans une copie
  du dépôt : 23 contrôles de calibrage affichés, tous en OK, code de sortie 0.
② CONTEXTE D'APPEL — Il est chargé par deux programmes, et un seul des deux
  tourne sans intervention humaine.
  ① `programmes/JUGE_DES_STRATEGIES.py`, lancé à la main, appelle huit de ses fonctions —
  relevé le 19-09-2026 : `point_mort_en_fractions`, `episodes` (remplacée le 05-11-2026 par
  `observations_independantes`, n°106), `coupure_70_30`,
  `wilson_bas`, `fenetres_glissantes`, `borne_basse_gain`,
  `plus_longue_serie_de_pertes` et `etalon_hasard`.
  Depuis la décision de Jean-Luc du 29-10-2026 à 21h28 (« A »), le juge demande son
  point mort à `point_mort_des_operations`, qui appelle `point_mort_en_fractions`
  une fois par opération.
  ② `programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py` n'appelle que
  `point_mort_des_operations` (donc `point_mort_en_fractions`), à travers sa propre
  `point_mort_en_pourcents` qui convertit des pourcents en fractions puis délègue,
  parce que le calcul du point mort ne doit vivre qu'à un seul endroit (R-708). Ce programme-là TOURNE
  CHAQUE SOIR : `.github/workflows/collecte_abc.yml` le lance à sa ligne 223,
  dans le passage automatique déclenché à 18h UTC du lundi au vendredi.
  Lancé directement en ligne de commande, le module ne fait que son calibrage.
③ ENTRÉE — Aucune. C'est une bibliothèque : chaque fonction reçoit ses données
  de son appelant. Lancé en ligne de commande, il n'accepte aucun argument, et
  ceux qu'on lui donnerait seraient ignorés.
④ CONDITIONS D'ENTRÉE — Python 3, avec `random`, `statistics`, `collections`,
  `math` et `datetime`, tous fournis par le langage. Aucun fichier à lire,
  aucun accès réseau : une recherche de `open(`, `os.`, `csv`, `json`,
  `requests`, `socket` et `subprocess` dans ce fichier, le 19-09-2026, rend
  zéro occurrence.
⑤ SORTIE — Deux formes selon l'usage. Chargé comme bibliothèque : il ne rend
  rien et expose quinze fonctions (05-11-2026, lot S_per : six s'ajoutent pour R-505 ⑦ et ⑪ —
  `lire_les_epoques`, `loi_de_student_inferieure`, `probabilite_epoque_perdante`,
  `minimum_d_epoques_gagnantes`, `controle_des_epoques`, `afficher_le_groupe_temoin` ; leur seul
  appelant aujourd'hui est `tests/EPREUVES_DES_EPOQUES_Jeu_05-11-2026.py`, le juge de la loi (lot JG)
  les branchera). Lancé en ligne de commande : il SORT DU
  PROGRAMME avec 0 si tous les contrôles de calibrage passent, 1 si l'un
  échoue, après avoir affiché une ligne par contrôle.
⑥ TRAITEMENT — ① poser le capital simulé, les frais de repli et la graine de
  tirage · ② définir les quinze fonctions · ③ lancé en ligne de commande
  seulement : exécuter `_calibrage`, afficher ses lignes, afficher le verdict,
  et sortir avec 0 ou 1.
⑦ UNITÉ — Les objectifs de gain et les pertes acceptées sont des FRACTIONS,
  jamais des pourcents : 0,040 vaut 4 %. Les taux de réussite et les points
  morts sont des POURCENTS entre 0 et 100. Les gains sont des EUROS, sur un
  capital de 100 000 € par opération. Les durées sont des SÉANCES de bourse,
  sauf la courbe de capital quotidienne qui compte en JOURS DE CALENDRIER.
  Le taux de frais est une FRACTION : 0,0015 vaut 0,15 % de la valeur échangée.
⑧ POURQUOI — Ce module existe pour deux raisons, et la seconde est une règle
  du projet. D'abord, ces mesures avaient déjà été produites le 28-08-2026,
  mais dans des scripts jetables : elles ne vivaient donc nulle part et
  n'étaient pas rejouables. Ensuite, un chiffre qui existe ailleurs ne se
  recopie pas (R-708) : ce module n'écrit aucune des mesures que porte déjà
  `programmes/MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py`, et il va chercher
  le taux de frais chez son propriétaire, `programmes/MODULE_POSITIONS.py`,
  plutôt que de le réécrire.
  Ce module juge des STRATÉGIES et jamais des CONDUITES. Le vocabulaire a été
  figé par Jean-Luc le 22-08-2026 : une STRATÉGIE dit QUOI acheter — ses
  signaux, son univers, son objectif de gain, sa perte acceptée, son horizon —
  tandis qu'une CONDUITE dit QUELLE STRATÉGIE ÉCOUTER quand on ne peut tenir
  qu'une position à la fois (R-509). Aucune fonction de ce fichier ne reçoit
  ni ne compare deux stratégies : elles reçoivent toutes les opérations d'UNE
  seule. Le mot « conduite » n'apparaît nulle part dans ce fichier — vérifié le
  19-09-2026.
  ET LES SEUILS D'UNE STRATÉGIE NE SONT PAS ÉCRITS ICI. L'objectif de gain, la
  perte acceptée et l'horizon arrivent toujours en paramètres, et ce module ne
  lit aucun fichier pour les obtenir : recherche de `cac40_strategies`, de
  `REGISTRE` et de `.csv` dans ce fichier le 19-09-2026, zéro occurrence. Ils
  viennent du registre des stratégies, `donnees/cac40_strategies.csv`, que le
  juge des stratégies lit pour composer la fiche qu'il passe ici, et que
  `programmes/TENIR_LES_POSITIONS.py` désigne comme la source qui fait autorité.
  Exemple : la stratégie C5-ETENDU-10 porte au REGISTRE, règle R-201, un
  objectif de +4 %, une perte acceptée de −2,5 % et 20 séances d'horizon.
⑨ CE QUI CLOCHE —
  ① Le texte d'en-tête annonce « le temoin miroir » parmi ce que le module
  ajoute, et ce témoin n'existe pas. Un témoin miroir est une comparaison à un
  placement exposé au marché exactement quand la stratégie l'est, telle que la
  décrit `etudes/CAHIER_DES_CHARGES_v3_Dim_16-08-2026_16h16.md` ligne 138.
  Mesuré le 19-09-2026 : le mot « miroir » apparaît UNE seule fois dans les
  730 lignes du fichier, dans cette ligne d'annonce, et aucune fonction ne le
  calcule. Un lecteur qui cherche cette mesure dans le module ne la trouvera
  jamais, et il ne saura pas si elle a été retirée ou jamais écrite.
  ② Le capital et les frais sont recopiés d'un module qui les possède. Relevé
  le 19-09-2026 : ce fichier porte `CAPITAL = 100_000.0` et `FRAIS = 300.0`,
  tandis que `programmes/MODULE_POSITIONS.py` porte `CAPITAL = 100_000.0` et
  `FRAIS_TAUX = 0.0015`. Les frais réels ne sont pas un forfait : sur une
  sortie à +4 % avec un capital de 100 000 €, `MODULE_POSITIONS.frais_ordre`
  appelée à l'entrée puis à la sortie rend 306,00 € quand ce fichier en
  retranche 300,00 €, soit 6,00 € d'écart par opération. La fonction
  `point_mort_en_fractions` a été corrigée le 29-08-2026 pour aller chercher
  le taux chez son propriétaire, mais `etalon_hasard` retranchait encore le
  forfait (RÉGLÉ LE 28-09-2026, A-435 ④ : il appelait `mod_positions.pnl_net` ; depuis le 28-10-2026, il joue par `JUGE_DES_STRATEGIES.jouer_une_entree`, qui demande `MODULE_POSITIONS.frais_ordre` pour les deux ordres, comme la stratégie) : mesuré, un aller-retour de 100,00 € à 104,00 € rend 3 694,00 €
  par `MODULE_POSITIONS.pnl_net` et 3 700,00 € par la formule d'`etalon_hasard`.
  L'étalon de hasard était donc comparé à une stratégie dont les gains avaient
  été calculés avec une autre convention de frais (RÉGLÉ LE 28-09-2026). Un chiffre qui existe ailleurs
  ne se recopie pas (R-708).
  ③ Six des quinze fonctions ne sont couvertes par aucun contrôle de calibrage.
  Mesuré le 19-09-2026 en cherchant chaque nom de fonction dans le corps de
  `_calibrage` : `episodes`, `borne_basse_gain`, `etalon_hasard`,
  `courbe_quotidienne`, `_exiger_des_fractions` et `_impossible` n'y
  apparaissent pas, `point_mort` non plus. C'est exactement le défaut que le
  texte de `_calibrage` dit avoir fermé le 29-08-2026 : le texte d'`episodes`
  annonce « 33 episodes retrouves exactement » et ce résultat n'est rejouable
  par aucun contrôle du fichier. (05-11-2026 : `episodes` est retirée (n°106) ;
  sa remplaçante, `observations_independantes`, est éprouvée à vérité connue
  et sur les 100 opérations étalons de C5 par
  `tests/EPREUVES_DES_OBSERVATIONS_INDEPENDANTES_Jeu_05-11-2026.py`, pas par `_calibrage`.)
  ④ Deux fonctions ne sont appelées par personne. Mesuré le 19-09-2026 en
  cherchant chaque nom dans tous les fichiers `.py` de `programmes/` hors ce
  fichier : `courbe_quotidienne` et `glissement` rendent zéro appelant, alors
  que le texte d'en-tête les compte parmi ce que le module apporte. Elles sont
  écrites, elles sont justes, et aucun rapport ne les affiche.
  ⑤ Les seuils de la méthode de jugement sont écrits dans le code et nulle part
  ailleurs. Les 21 séances d'embargo entre deux morceaux de période, les 5
  séances qui séparent deux épisodes (retirées le 05-11-2026 : n°106, lot S_ep), la coupure au sept dixièmes de la période
  et les 5 opérations minimales pour juger une fenêtre vivent tous ici.
  Recherche du mot « embargo » dans `gouvernance/REGISTRE_REGLES.md` le
  19-09-2026 : zéro occurrence. Les seuils PROPRES À UNE STRATÉGIE, eux, sont
  bien reçus en paramètres et jamais écrits ici. Les seuils de la MÉTHODE, non :
  les changer se fait en modifiant ce fichier, sans trace au REGISTRE.
⑩ EFFET — N'ÉCRIT AUCUN FICHIER et ne touche pas au réseau : recherche de
  `open(`, `os.`, `csv`, `json`, `requests`, `socket` et `subprocess` le
  19-09-2026, zéro occurrence. Lancé en ligne de commande, il AFFICHE 26 lignes.
  Aucune de ses fonctions ne modifie les données qu'on lui donne.
⑪ TERMINAISON — Chargé comme bibliothèque, il rend la main après avoir défini
  ses fonctions. Lancé en ligne de commande, il SORT DU PROGRAMME avec le code
  0 si le calibrage passe, 1 sinon. Et un de ses appels peut ne pas revenir :
  `_calibrage` appelle `point_mort_en_fractions`, qui lève une erreur non
  rattrapée quand un seuil reçu n'est pas une fraction.
⑫ DÉFINITIONS
  une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
  une stratégie : une règle qui dit QUOI acheter, avec son objectif de gain, sa perte acceptée et son horizon
  une conduite : la règle qui dit QUELLE STRATÉGIE écouter quand on ne peut
    tenir qu'une position à la fois ; ce module n'en traite aucune
  le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie
    sur l'historique des cours et rend la liste de ses opérations
  le point mort : le taux de réussite en dessous duquel une stratégie perd de l'argent
  une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
  l'horizon : le nombre de séances pendant lesquelles une position est tenue
    si ni l'objectif de gain ni la perte acceptée ne sont atteints
  l'univers : la liste des valeurs sur lesquelles une stratégie a le droit
    d'acheter, désignées par leur mnémonique
  le registre des stratégies : le fichier `cac40_strategies.csv`, une ligne par stratégie, qui porte leur état civil — identifiant, réglages, résultats connus
  le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les
    règles numérotées du projet
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
  C5-ETENDU-10 : le nom de la stratégie vivante ; ses seuils et son horizon sont lus dans `donnees/cac40_strategies.csv`.
  l'étalon de hasard : le résultat qu'obtiendraient des entrées tirées au sort jouées aux mêmes règles, et auquel la stratégie doit être comparée
  la borne basse : la valeur en dessous de laquelle ne tombe qu'un tirage sur vingt
  la courbe de capital : la valeur qu'aurait eue le portefeuille à la fin de chaque séance de bourse, positions ouvertes comprises
  la fiche : la ligne d'une stratégie au registre des stratégies `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte acceptée, son horizon et son univers
  la graine : le nombre qui fixe la suite de tirages, pour qu'un calcul fondé sur le hasard donne toujours le même résultat
  le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
  le glissement : l'écart entre le prix de sortie prévu et le prix réellement obtenu
  un témoin : un jeu de chiffres dont on connaît d'avance le résultat, employé pour prouver qu'un instrument fonctionne avant de s'en servir
  une fenêtre : un morceau de la période, jugé séparément des autres
  une fraction : la façon d'écrire un pourcentage entre 0 et 1 — 0,040 pour +4 % — par opposition au pourcent, qui écrirait 4.0
"""

import random
import statistics
from collections import defaultdict

CAPITAL = 100_000.0
# Le forfait de 300 € (`FRAIS = 300.0`) vivait ici jusqu'au 29-10-2026 : il a disparu (A-550, ÉTUDE 18 S5).
# Les frais se lisent dans le barème daté, par `MODULE_POSITIONS.frais_ordre` ; le forfait historique
# s'y nomme « HIST_FORFAIT_300 ».
GRAINE = 20260828


# ─────────────────────────────────────────────────────────────────────
# LE POINT MORT — le seuil qui remplace tout seuil fixe
# ─────────────────────────────────────────────────────────────────────

def point_mort_en_fractions(tp, sl, mod_positions, valeur, date, bareme=None, capital=CAPITAL):
    """Taux de reussite en dessous duquel la strategie PERD, quoi qu'il arrive.

    CALIBRE sur les deux valeurs de l'ETUDE 11, retrouvees au centieme :
      +4,0 % / -2,5 %  ->  43,08 %   (documente 43,1 %)
      +1,2 % / -1,0 %  ->  59,09 %   (documente 59,1 %)

    POURQUOI IL REMPLACE UN SEUIL FIXE : un taux de 55 % est excellent a
    +5 %/-2 % et ruineux a +1,2 %/-1 %. Juger toutes les strategies sur le meme
    nombre n'a aucun sens — c'est le defaut qu'A-280 a revele.

    ① RÔLE — Donner à chaque stratégie SON propre seuil de réussite, calculé
      depuis ses réglages, pour remplacer le seuil unique qui servait avant. Sans
      ce chiffre, un taux de réussite nu ne veut rien dire : 55 % de réussite est
      excellent avec un objectif de +5 % et une perte acceptée de −2 %, et
      ruineux avec +1,2 % et −1 %. Mesuré le 19-09-2026 : les mêmes frais
      forfaitaires donnent 43,08 % pour le couple +4,0 % / −2,5 % et 59,09 %
      pour le couple +1,2 % / −1,0 %.
    ② CONTEXTE D'APPEL — Trois appelants depuis la décision de Jean-Luc du
      29-10-2026 à 21h28 (« A » : le point mort moyen des opérations jouées).
      ① `point_mort_des_operations`, ci-dessous, une fois par opération qu'on lui
      donne ; elle-même est appelée par `juger` de
      `programmes/JUGE_DES_STRATEGIES.py` (une fois par stratégie jugée) et par
      `point_mort_en_pourcents` de
      `programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py`, qui convertit
      des pourcents en fractions ; ce programme TOURNE CHAQUE SOIR (pas « Mesurer
      la performance » de `.github/workflows/collecte_abc.yml`). Le calcul ne vit
      qu'à un seul endroit (R-708).
      ② `point_mort_pire_cas`, une fois par valeur de l'univers qu'on lui donne ;
      elle n'est plus appelée que par `_calibrage` (gardée pour comparaison).
      ③ `_calibrage`, pour vérifier que les résultats connus sont toujours
      retrouvés.
    ③ ENTRÉE — `tp` : l'objectif de gain, en FRACTION, 0.040 pour +4 % ·
      `sl` : la perte acceptée, en FRACTION et en valeur positive, 0.025 pour
      −2,5 % · `mod_positions` : `programmes/MODULE_POSITIONS.py`, qui chiffre les
      frais (`frais_ordre`) · `valeur` et `date` : la valeur achetée et le jour de
      l'achat, parce que la taxe sur les transactions financières dépend de l'une et
      de l'autre (A-550) · `bareme` : le nom d'un barème, None pour le barème réel ·
      `capital` : la somme engagée par opération, 100 000 € par défaut, aucun
      appelant ne la change.
    ④ CONDITIONS D'ENTRÉE — `tp` et `sl` doivent être des fractions strictement
      inférieures à 1 en valeur absolue, sans quoi la fonction lève. Le résultat
      doit tomber entre 0 et 100, sans quoi elle lève aussi. `mod_positions` doit
      porter `frais_ordre(quantite, prix, valeur, date, sens, bareme)`.
    ⑤ SORTIE — UNE valeur : le point mort, un pourcentage entre 0 et 100.
      Exemples relevés le 29-10-2026 : 43,08 pour 0.040 et 0.025 sous le forfait
      historique de 300 € ; 32,86 pour 0.05 et 0.02 au courtage seul de 0,15 % ;
      49,25 pour 0.040 et 0.025 sous le barème réel, sur une valeur taxée en 2026
      (ÉTUDE 18, S3).
      [rend: 1]
    ⑥ TRAITEMENT — ① faire respecter le contrat d'unité annoncé par le nom ·
      ② calculer les frais SÉPARÉMENT pour la sortie au gain et pour la sortie au
      stop, puisqu'ils sont proportionnels à la valeur échangée, l'achat et la vente
      le même jour (la taxe se lit à l'achat) · ③ rendre la part que la perte
      représente dans la somme du gain et de la perte, exprimée en pourcents ·
      ④ refuser un résultat hors de l'intervalle 0 à 100.
    ⑦ UNITÉ — `tp` et `sl` sont des FRACTIONS. `capital` et les frais sont des
      EUROS. Le résultat est un POURCENTAGE entre 0 et 100.
    ⑧ POURQUOI — Le nom porte l'unité, et ce n'est pas de la décoration. Deux
      fonctions ont porté le nom `point_mort`, pris les deux mêmes arguments, et
      attendu des unités OPPOSÉES : celle-ci en fractions, celle de
      `MESURER_LA_PERFORMANCE` en pourcents. Croisées, elles rendaient 38,51 %
      au lieu de 43,08 % — un chiffre plausible, silencieux et faux. Cowork a
      reproduit le croisement le 13-09-2026, et le nom a été allongé ce jour-là.
      Les deux branches de frais existent parce qu'une sortie au gain coûte plus
      cher qu'une sortie au stop : les frais sont proportionnels à la valeur
      échangée, et appliquer ceux de la branche gagnante aux deux donnait
      32,96 % au lieu de 32,86 %. Ce défaut a été trouvé le 29-08-2026, alors
      que 300 € étaient écrits en dur ici pendant que `MODULE_POSITIONS`
      appliquait 0,15 % à l'entrée et à la sortie.
    ⑨ CE QUI CLOCHE —
      ① (RÉGLÉ LE 29-10-2026, A-550) Le repli muet sur un forfait de 300 € quand
      aucun module de positions n'était donné a disparu : le module est exigé.
      ② Le paramètre `capital` ne sert à rien au résultat. Il apparaît au
      numérateur et au dénominateur de la même fraction : mesuré le 19-09-2026,
      le couple 0.040 et 0.025 rend 43,08 % avec 100 000 € et 43,08 % avec
      10 000 €, frais forfaitaires identiques. Un lecteur qui voit ce paramètre
      croit pouvoir régler quelque chose qui ne bouge pas.
      ③ (RÉGLÉ LE 29-10-2026, A-550) Le forfait de 300 € recopié ici a disparu ; il
      se nomme « HIST_FORFAIT_300 » dans le barème, et ne sert qu'à refaire les
      chiffres anciens.
      ④ Le point mort se calcule pour UNE valeur à UNE date : une stratégie qui
      achète des valeurs taxées et d'autres non a un point mort par valeur.
      `point_mort_pire_cas` choisit la plus chère ; `point_mort_des_operations`
      fait la moyenne des opérations jouées, chacune à sa valeur et à sa date —
      la méthode choisie par Jean-Luc le 29-10-2026 à 21h28 (« A »).
    ⑩ EFFET — Aucun : elle calcule. Aucun fichier, aucun réseau, aucune donnée
      modifiée par elle. Elle EXÉCUTE la fonction `frais_ordre` du module qu'on
      lui passe, trois fois par appel (l'achat, la vente au gain, la vente au
      stop) ; au premier appel, ce module lit le barème des frais.
    ⑪ TERMINAISON — Rend la main avec un pourcentage dans le cas normal. PEUT
      LEVER, et dans les deux cas l'erreur remonte à l'appelant : sur un seuil
      qui n'est pas une fraction, sur un résultat hors de 0 à 100, sur un module
      sans `frais_ordre` (`RuntimeError`), et ce que lève `frais_ordre`
      (`ValueError`, `LookupError` : barème inconnu, valeur ou année absente de la
      liste des valeurs taxées). Un de ses appels peut ne pas revenir :
      `_exiger_des_fractions` et `_impossible` lèvent toutes deux.
      [sort: non]
    ⑫ DÉFINITIONS
      le point mort : le taux de réussite en dessous duquel une stratégie perd de l'argent
      une fraction : la façon d'écrire un pourcentage entre 0 et 1 — 0,040 pour
        +4 % — par opposition au pourcent, qui écrirait 4.0
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
      une stratégie : une règle qui dit QUOI acheter, avec son objectif de gain,
        sa perte acceptée et son horizon
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
    
      Cowork : le relecteur du projet, qui clone le dépôt, casse le code et rend ses cassures par écrit
      PRODUCTION : l etat d une strategie dont le seuil d operations est atteint et les resultats conformes, donc exploitee.
      l'objectif de gain : le pourcentage de hausse à partir duquel la position se referme sur un gain
      la perte acceptée : le pourcentage de baisse à partir duquel la position se referme sur une perte
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    _exiger_des_fractions(tp, sl)
    # LES FRAIS VIENNENT DU MODULE QUI LES POSSEDE, jamais d'un nombre recopie (R-708).
    # LES DEUX BRANCHES N'ONT PAS LES MEMES FRAIS : une sortie au gain coute plus cher
    # qu'une sortie au stop, puisque les frais sont proportionnels a la valeur echangee
    # (29-08-2026 : appliquer les frais de la branche gagnante aux deux donnait 32,96 % au
    # lieu de 32,86). Depuis le 29-10-2026 (A-550), la taxe sur les transactions
    # financieres s'ajoute a l'achat d'une valeur taxee : le point mort depend donc de la
    # valeur et de la date.
    # Le point mort passe par `frais_ordre`, ordre par ordre, et non par `frais_aller_retour` :
    # il suppose une revente un AUTRE jour que l'achat, donc la taxe payée — le cas le plus
    # cher. Un achat revendu le jour même (exonéré) coûte moins : le point mort est prudent.
    _fo = getattr(mod_positions, "frais_ordre", None)
    if not callable(_fo):
        raise RuntimeError("point_mort_en_fractions : le module des positions doit exposer frais_ordre "
                           "(aucun forfait de repli : A-550, ÉTUDE 18 S5)")
    q = capital / 100.0                      # prix d'entree normalise
    f_achat = _fo(q, 100.0, valeur, date, "achat", bareme)
    f_gain = f_achat + _fo(q, 100.0 * (1 + tp), valeur, date, "vente", bareme)
    f_perte = f_achat + _fo(q, 100.0 * (1 - sl), valeur, date, "vente", bareme)
    gain = capital * tp - f_gain
    perte = capital * sl + f_perte
    return _impossible(100.0 * perte / (gain + perte), tp, sl)


def point_mort_pire_cas(tp, sl, univers, date, mod_positions, bareme=None):
    """Le point mort de la valeur la plus chère d'un univers, à une date.

    ① RÔLE — Donner UN point mort à une stratégie dont les valeurs ne coûtent pas
      toutes la même chose : depuis la taxe sur les transactions financières (A-550),
      acheter Bouygues coûte 400 € de plus qu'acheter Airbus.
    ② CONTEXTE D'APPEL — PLUS APPELÉE PAR LE JUGE NI PAR LA MESURE DEPUIS LA DÉCISION
      DU 29-10-2026 ; GARDÉE POUR COMPARAISON. Jean-Luc a répondu « A » (message reçu à
      21h28) à la question « Avec quel point mort juger les stratégies aux vrais frais ?
      A : chaque trade compte la taxe qu'il a vraiment payée (barre 48,70 % pour
      C5E10-QA-V1) ; B : on suppose que chaque trade a payé la taxe la plus chère,
      400 € (49,25 %) » : `juger` de `programmes/JUGE_DES_STRATEGIES.py` et
      `point_mort_en_pourcents` de
      `programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py` appellent désormais
      `point_mort_des_operations`. Seul appelant restant : `_calibrage`, qui vérifie
      qu'elle retient la valeur taxée. Rien ne se supprime sans accord.
    ③ ENTRÉE — `tp`, `sl` : en FRACTIONS · `univers` : les valeurs de la stratégie
      (mnémoniques ou noms) · `date` : « AAAA-MM-JJ », le jour dont on prend le
      barème · `mod_positions` : `programmes/MODULE_POSITIONS.py` · `bareme` : None
      pour le barème réel.
    ④ CONDITIONS D'ENTRÉE — `univers` n'est pas vide ; chaque valeur figure dans la
      liste des valeurs taxées de l'année de `date`.
    ⑤ SORTIE — DEUX valeurs : le point mort le plus haut, en pourcents, et la valeur
      qui le donne.
      [rend: 2]
    ⑥ TRAITEMENT — ① calculer le point mort de chaque valeur à la date ·
      ② garder le plus haut, et la première valeur qui l'atteint dans l'ordre de
      l'univers.
    ⑦ UNITÉ — Seuils en FRACTIONS ; résultat en POURCENTS.
    ⑧ POURQUOI — Choix de méthode PESSIMISTE, dans l'esprit de R-602 (on suppose le
      pire) : le verdict C7 compare la borne basse du taux de réussite à ce point mort,
      et une stratégie qui ne passe qu'avec les frais de ses valeurs les moins chères
      ne passe pas. Exemple : C5-ETENDU-10, +4 % / −2,5 %, univers de dix valeurs dont
      neuf taxées en 2026 — 49,25 % (taxée) au lieu de 43,08 % (forfait d'avant).
      CE CHOIX N'A PAS ÉTÉ RETENU : le 29-10-2026 à 21h28, Jean-Luc a choisi l'autre
      méthode, les frais des opérations réellement jouées (`point_mort_des_operations`).
    ⑨ CE QUI CLOCHE — La date fixe le barème de TOUTES les opérations : une stratégie
      jugée sur 2024-2026 au barème de 2026 compte 0,4 % de taxe là où ses achats de
      2024 n'en payaient que 0,3 %. Le point mort est donc un peu plus haut que celui
      des opérations d'avant le 01-04-2025.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève `ValueError` sur un univers vide, et ce que lève
      `point_mort_en_fractions`.
      [sort: non]
    """
    if not univers:
        raise ValueError("point_mort_pire_cas : univers vide")
    pire, qui = None, None
    for v in univers:
        pm = point_mort_en_fractions(tp, sl, mod_positions, v, date, bareme)
        if pire is None or pm > pire:
            pire, qui = pm, v
    return pire, qui


def point_mort_des_operations(tp, sl, operations, mod_positions, bareme=None):
    """Le point mort moyen des opérations jouées, chacune à SA valeur et à SA date d'achat.

    ① RÔLE — Donner UN point mort à une stratégie dont les opérations n'ont pas toutes
      coûté la même chose : depuis la taxe sur les transactions financières (A-550),
      acheter Bouygues coûte 400 € de plus qu'acheter Airbus, et la taxe valait 0,3 %
      avant le 01-04-2025 et 0,4 % depuis. Chaque opération compte la taxe qu'elle a
      payée ; le point mort de la stratégie est la moyenne de ces points morts.
    ② CONTEXTE D'APPEL — `juger` de `programmes/JUGE_DES_STRATEGIES.py`, une fois par
      stratégie jugée, sur les opérations jugées ; `point_mort_en_pourcents` de
      `programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py`, chaque soir, une fois
      par stratégie et par comptabilité, sur les lignes du journal des trades de cette
      stratégie et de cette comptabilité ; `_calibrage`, une fois.
    ③ ENTRÉE — `tp`, `sl` : l'objectif de gain et la perte acceptée, en FRACTIONS
      (0.040 et 0.025 pour +4 % et −2,5 %) · `operations` : une liste d'opérations, chacune
      un dictionnaire qui porte au moins `valeur` (mnémonique ou nom, « BOUYGUES »,
      « UNIBAIL_RODAMCO ») et `date_entree` (« AAAA-MM-JJ », le jour de l'ACHAT, celui où
      la taxe frappe) — les autres clés sont ignorées · `mod_positions` :
      `programmes/MODULE_POSITIONS.py` · `bareme` : le nom d'un barème, None pour le
      barème réel.
    ④ CONDITIONS D'ENTRÉE — `operations` n'est pas vide ; chaque opération porte
      `valeur` et `date_entree` ; chaque valeur figure dans la liste des valeurs taxées
      de l'année de sa date d'achat.
    ⑤ SORTIE — UNE valeur : le point mort moyen, un pourcentage entre 0 et 100.
      Exemples recalculés à la main le 29-10-2026, +4 % / −2,5 %, barème réel :
      Airbus le 27-07-2026 (non taxée) 43,08 % et Bureau Veritas le même jour (taxée
      0,4 %) 49,25 % donnent 46,17 % ; les 51 opérations de C5E10-QA-V1 rejouées par la
      remesure du 29-10-2026 donnent 48,7031 %, les 89 de C5E10-OBS-V1 47,9832 %.
      [rend: 1]
    ⑥ TRAITEMENT — ① refuser une liste vide · ② pour chaque opération, demander à
      `point_mort_en_fractions` le point mort à sa valeur et à sa date d'achat, sous le
      barème donné (le calcul n'est jamais recopié ici, R-708) · ③ rendre la moyenne
      arithmétique, chaque opération pesant autant.
    ⑦ UNITÉ — Seuils en FRACTIONS ; résultat en POURCENTS.
    ⑧ POURQUOI — DÉCISION DE JEAN-LUC DU 29-10-2026, message reçu à 21h28 : « A » à la
      question « Avec quel point mort juger les stratégies aux vrais frais ? A : chaque
      trade compte la taxe qu'il a vraiment payée (barre 48,70 % pour C5E10-QA-V1) ; B :
      on suppose que chaque trade a payé la taxe la plus chère, 400 € (49,25 %). »
      Jusque-là, `point_mort_pire_cas` prenait la valeur la plus chère de l'univers au
      barème du dernier achat : une opération de 2024 (taxe 0,3 %) ou sur Airbus (pas
      de taxe) y était jugée comme si elle avait payé 400 €. La moyenne est juste
      parce que le point mort est, à une opération près, une moyenne lui-même : la
      stratégie ne perd pas d'argent tant que son taux de réussite dépasse la part
      moyenne de la perte dans gain + perte. Mesuré sur la remesure du 29-10-2026
      (C5E10-QA-V1, 51 opérations, 32 gagnantes, borne basse de Wilson 49,02 % —
      49,02496 rendu par `wilson_borne_basse` de la mesure, relecture de Cowork du
      29-10-2026, tour 3, défaut 3) : pire cas 49,25 % (ne passe
      pas), moyenne 48,70 % (passe).
    ⑨ CE QUI CLOCHE —
      ① L'exonération d'un achat revendu le jour même (pas de taxe) n'entre PAS dans ce
      point mort : `point_mort_en_fractions` suppose toujours la taxe payée à l'achat
      d'une valeur taxée. Cette exonération est déjà dans les gains de l'opération
      (`MODULE_POSITIONS.frais_aller_retour`) ; le point mort reste un peu prudent pour
      ces opérations-là.
      ② Une stratégie SANS opération n'a pas de point mort : la fonction lève, et c'est
      à l'appelant de ne pas en écrire (la mesure laisse la case vide et dit
      « echantillon insuffisant »).
      ③ Chaque opération pèse autant, ce qui suppose la même somme engagée (100 000 €)
      et les mêmes seuils pour toutes. Sous cette condition, la moyenne des points
      morts est EXACTEMENT le point mort des frais d'achat moyens : les frais d'achat
      s'annulent dans gain + perte, qui ne dépend donc pas de la valeur. Mesuré le
      29-10-2026 : Airbus et Bureau Veritas au 27-07-2026 donnent 46,16540194907746 par
      les deux chemins. Ce n'est plus vrai si un barème faisait dépendre les frais de
      VENTE de la valeur.
      ④ Le barème est celui que l'appelant donne (le barème des verdicts), pas celui
      que le journal des trades écrit dans sa colonne `bareme_reel` : la première ligne
      du journal (Bureau Veritas, 27-07-2026, payée au forfait historique de 300 €) est
      jugée comme si elle avait payé le barème des verdicts.
    ⑩ EFFET — Aucun : elle calcule. Elle EXÉCUTE `frais_ordre` du module des positions
      trois fois par opération, à travers `point_mort_en_fractions`.
    ⑪ TERMINAISON — Rend la main ; lève `ValueError` sur une liste vide ou une opération
      sans `valeur` ou sans `date_entree`, et ce que lève `point_mort_en_fractions`
      (dont `FraisNonChiffrables`, un cas de `LookupError`, quand une valeur manque à
      la liste de son année). Un de ses appels peut ne pas revenir :
      `point_mort_en_fractions` lève.
      [sort: non]
    ⑫ DÉFINITIONS
      le point mort : le taux de réussite en dessous duquel une stratégie perd de l'argent
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ;
        aucun ordre réel n'est jamais passé
      la taxe sur les transactions financières : 0,3 % puis 0,4 % (depuis le 01-04-2025)
        de la somme achetée, à l'achat d'une valeur française de plus d'un milliard
        d'euros de capitalisation, listée chaque année
    """
    if not operations:
        raise ValueError("point_mort_des_operations : aucune opération — une stratégie sans opération "
                         "n'a pas de point mort (décision de Jean-Luc du 29-10-2026, méthode A)")
    pms = []
    for o in operations:
        v, d = o.get("valeur"), o.get("date_entree")
        if not v or not d:
            raise ValueError(f"point_mort_des_operations : opération sans valeur ou sans date d'achat : {o!r}")
        pms.append(point_mort_en_fractions(tp, sl, mod_positions, v, d, bareme))
    return sum(pms) / len(pms)


def _exiger_des_fractions(tp, sl):
    """LE NOM DECLARE DES FRACTIONS — ON LE FAIT RESPECTER.

    Y1 de Cowork, 13-09-2026 : le nom ferme la moitie silencieuse **par
    convention**, et une convention ne leve pas. `point_mort_en_fractions(4.0,
    2.5)` rendait encore 38,51 % — plausible, faux, muet.
    Ce n est pas un seuil arbitraire : c est le CONTRAT que la signature annonce.
    Un objectif exprime en fraction vaut 0,040 pour +4 % ; 4.0 signifierait
    +400 %, qu aucune strategie de ce systeme n emploie. **Faire respecter un
    contrat declare n est pas poser un seuil.**

    ① RÔLE — Faire tomber tout de suite un appel dont les seuils sont écrits
      dans la mauvaise unité, au lieu de le laisser rendre un chiffre plausible
      et faux. Sans elle, `point_mort_en_fractions(4.0, 2.5)` rendait 38,51 %
      quand la bonne réponse est 43,08 % : cinq points d'écart, aucune erreur
      affichée, et un rapport qui se lit comme les autres.
    ② CONTEXTE D'APPEL — Un seul appelant : `point_mort_en_fractions`, en toute
      première ligne, avant le moindre calcul. Aucun appel depuis un autre
      programme — recherche dans tous les fichiers `.py` de `programmes/` le
      19-09-2026, zéro ligne hors de ce fichier.
    ③ ENTRÉE — `tp` : l'objectif de gain tel que l'appelant l'a reçu ·
      `sl` : la perte acceptée telle que l'appelant l'a reçue. L'unique appelant
      transmet les deux sans les modifier.
    ④ CONDITIONS D'ENTRÉE — Aucune. Une valeur `None` est acceptée et ignorée ;
      une valeur non convertible en nombre fait lever la conversion elle-même.
    ⑤ SORTIE — Ne rend rien. Elle lève, ou elle laisse passer.
      [rend: rien]
    ⑥ TRAITEMENT — ① prendre tour à tour `tp` puis `sl` · ② ignorer la valeur
      si elle vaut `None` · ③ la convertir en nombre et prendre sa valeur
      absolue · ④ lever si cette valeur atteint ou dépasse 1,0, en nommant le
      paramètre fautif et en indiquant la fonction à employer pour des
      pourcents.
    ⑦ UNITÉ — Elle contrôle que les valeurs reçues sont des FRACTIONS, c'est-à-dire
      strictement comprises entre −1 et 1 hors bornes.
    ⑧ POURQUOI — Un nom de fonction est une convention, et une convention ne
      lève pas. Deux fonctions du dépôt ont porté le même nom `point_mort`, pris
      les deux mêmes arguments et attendu des unités opposées ; Cowork a croisé
      les deux le 13-09-2026 et obtenu 38,51 %, un chiffre que rien n'aurait
      arrêté. Allonger le nom rendait l'erreur moins probable ; cette fonction
      la rend impossible au-dessus de 1,0.
    ⑨ CE QUI CLOCHE —
      ① Elle ne ferme que la moitié bruyante, et le fichier le dit déjà en
      commentaire sans que ce soit fermé. Un objectif de +0,9 % écrit `0.9` au
      lieu de `0.009` ne déclenche rien. Mesuré le 19-09-2026 avec les frais
      forfaitaires : le couple `0.9` et `0.5` rend 35,93 % là où le couple
      `0.009` et `0.005` rend 57,14 %. Vingt et un points d'écart, aucun mot.
      ② Elle n'est appelée que par une seule des trois fonctions qui reçoivent
      un objectif et une perte. Mesuré le 19-09-2026 : `etalon_hasard(ops,
      cours, univers, 4.0, 2.5, 5, module)` est acceptée sans broncher et rend
      un taux de réussite médian de 100,0 %, parce qu'un objectif de +400 % avec
      une perte acceptée de 250 % ne se touche jamais. Le contrat d'unité est
      donc fermé pour le point mort et ouvert pour l'étalon de hasard.
      ③ Aucun contrôle de calibrage ne la fait tomber. Recherche du nom
      `_exiger_des_fractions` dans le corps de `_calibrage` le 19-09-2026 :
      absent. Le jour où la comparaison serait retirée, les 23 contrôles
      passeraient toujours.
    ⑩ EFFET — Aucun : elle lit deux nombres. Aucun fichier, aucun réseau,
      aucune donnée modifiée, rien d'affiché.
    ⑪ TERMINAISON — Rend la main sans rien rendre quand les deux valeurs sont
      des fractions. LÈVE sinon, et l'erreur remonte telle quelle jusqu'à
      l'appelant du point mort. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      une fraction : la façon d'écrire un pourcentage entre 0 et 1 — 0,040 pour
        +4 % — par opposition au pourcent, qui écrirait 4.0
      le point mort : le taux de réussite en dessous duquel une stratégie perd
        de l'argent
      une stratégie : une règle qui dit QUOI acheter, avec son objectif de gain,
        sa perte acceptée et son horizon
    
      Cowork : le relecteur du projet, qui clone le dépôt, casse le code et rend ses cassures par écrit
      l'objectif de gain : le pourcentage de hausse à partir duquel la position se referme sur un gain
      l'étalon de hasard : le résultat qu'obtiendraient des entrées tirées au sort jouées aux mêmes règles, et auquel la stratégie doit être comparée
      la perte acceptée : le pourcentage de baisse à partir duquel la position se referme sur une perte
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    # LA LIMITE DE CETTE GARDE, NOMMEE PAR COWORK LE 13-09-2026 ET NON FERMEE :
    # elle n attrape qu un croisement AU-DESSUS de 1,0. En dessous, rien ne se
    # declenche — un objectif ecrit « +0,8 % » passe pour une fraction et rend
    # 43,07 % au lieu de 64,32 %. **Vingt et un points d ecart, sans un mot.**
    # ET LE DETAIL QUI REND CE CAS VICIEUX : 43,07 est le voisinage exact du
    # point mort des strategies vivantes, 43,08. **La valeur fausse tombe sur le
    # chiffre que tout le monde reconnait comme normal.**
    # Le voisinage est habite : six strategies du registre portent deja un seuil
    # sous 1 %. Aucune n est vivante aujourd hui, et aucun appel croise n existe
    # dans le code — c est une limite nommee, pas un defaut actif.
    # CE QUI LA FERMERAIT VRAIMENT : que l unite voyage DANS LA VALEUR, pas
    # seulement dans le nom de la fonction. Ce n est pas une ligne, c est un
    # changement de type, et il n a pas ete fait.
    for nom, v in (("tp", tp), ("sl", sl)):
        if v is not None and abs(float(v)) >= 1.0:
            raise ValueError(
                f"{nom}={v} n est pas une FRACTION : cette fonction attend 0.040 "
                f"pour +4 %, pas 4.0. Pour des seuils en POURCENTS, employer "
                f"MESURER_LA_PERFORMANCE.point_mort_en_pourcents().")


def _impossible(r, tp, sl):
    """Un point mort hors de [0 ; 100] est impossible — Y1 de Cowork, 13-09-2026.
    ICI, tp et sl sont des FRACTIONS : 0.040 et 0.025. Passer 4.0 et 2.5 rend
    38,51 — plausible, silencieux, et faux. La garde est la meme des deux cotes.

    ① RÔLE — Refuser un point mort qui ne peut pas exister, au lieu de le
      laisser descendre dans un rapport. Un point mort est un taux de réussite :
      il vit entre 0 et 100. Un croisement d'unités peut en produire un à
      500,69 %, et ce chiffre-là doit arrêter le calcul plutôt que s'afficher.
    ② CONTEXTE D'APPEL — Un seul appelant, `point_mort_en_fractions`, sur ses
      deux branches de sortie : celle qui calcule les frais chez le module des
      positions et celle qui retombe sur le forfait. Aucun appel depuis un autre
      programme — recherche dans tous les fichiers `.py` de `programmes/` le
      19-09-2026, zéro ligne hors de ce fichier.
    ③ ENTRÉE — `r` : le point mort qui vient d'être calculé, en pourcents ·
      `tp` : l'objectif de gain, repris tel quel pour pouvoir le nommer dans le
      message d'erreur · `sl` : la perte acceptée, pour la même raison.
      L'unique appelant transmet les trois sans les modifier.
    ④ CONDITIONS D'ENTRÉE — Aucune. Une valeur `None` est acceptée et rendue
      telle quelle.
    ⑤ SORTIE — UNE valeur, et sous deux formes selon la branche : `None` si on
      lui a passé `None`, sinon le nombre reçu, inchangé.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre `None` si la valeur reçue est `None` · ② lever si
      la valeur sort de l'intervalle 0 à 100, en affichant le point mort avec
      deux décimales, les deux seuils reçus, et le rappel que les seuils sont
      ici des fractions · ③ sinon rendre la valeur telle quelle.
    ⑦ UNITÉ — `r` est un POURCENTAGE entre 0 et 100. `tp` et `sl` sont des
      FRACTIONS, et ne servent qu'à composer le message d'erreur.
    ⑧ POURQUOI — Un croisement d'unités produit deux sortes de fautes, et une
      seule se voit. Cowork l'a mesuré le 13-09-2026 en croisant les deux
      fonctions homonymes du dépôt : dans un sens le résultat est 500,69 %,
      absurde, et il crie ; dans l'autre il est 38,51 %, plausible, et il se
      tait. Cette garde ferme la moitié bruyante. La moitié silencieuse est
      fermée ailleurs, par le contrôle d'unité des seuils.
      La même garde existe à l'identique dans
      `programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py` sous le nom
      `_refuser_l_impossible`, parce que les deux chemins de calcul devaient
      être fermés des deux côtés.
    ⑨ CE QUI CLOCHE —
      ① La garde est écrite deux fois dans le dépôt. Relevé le 19-09-2026 :
      `_impossible` ici et `_refuser_l_impossible` dans
      `MESURER_LA_PERFORMANCE`, même intervalle, même levée, messages
      différents. Deux implémentations d'une même chose divergent toujours
      (R-708) : corriger l'intervalle ici ne le corrigerait pas là-bas.
      ② L'intervalle accepté est plus large que ce qui a un sens. Un point mort
      de 0 % ou de 100 % passe, alors qu'aucune stratégie du projet n'en
      approche : les deux points morts documentés de l'ÉTUDE 11 valent 43,08 %
      et 59,09 %, mesurés le 19-09-2026. La garde attrape les fautes d'un
      facteur cent, pas celles d'un facteur dix.
      ③ Aucun contrôle de calibrage ne la fait tomber. Recherche du nom
      `_impossible` dans le corps de `_calibrage` le 19-09-2026 : absent. Les 23
      contrôles passeraient toujours si la comparaison était retirée.
    ⑩ EFFET — Aucun : elle compare un nombre. Aucun fichier, aucun réseau,
      aucune donnée modifiée, rien d'affiché.
    ⑪ TERMINAISON — Rend la main dans le cas normal. LÈVE quand la valeur sort
      de 0 à 100, et l'erreur remonte jusqu'à l'appelant du point mort. Aucun
      de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le point mort : le taux de réussite en dessous duquel une stratégie perd
        de l'argent
      une fraction : la façon d'écrire un pourcentage entre 0 et 1 — 0,040 pour
        +4 % — par opposition au pourcent, qui écrirait 4.0
    
      Cowork : le relecteur du projet, qui clone le dépôt, casse le code et rend ses cassures par écrit
      l'objectif de gain : le pourcentage de hausse à partir duquel la position se referme sur un gain
      l'ÉTUDE 11 : l'étude datée du projet qui fixe la méthode de jugement des stratégies
      la perte acceptée : le pourcentage de baisse à partir duquel la position se referme sur une perte
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if r is None:
        return None
    if not (0.0 <= r <= 100.0):
        raise ValueError(
            f"point mort impossible : {r:.2f} % pour tp={tp} sl={sl}. "
            f"ICI les seuils sont des FRACTIONS (0.040), pas des pourcents (4.0).")
    return r


def wilson_bas(n, wr_pct, z=1.96):
    """Borne basse de l'intervalle de Wilson : ce qu'on peut affirmer AU PIRE.

    ELLE VIT ICI ET NON DANS LE JUGE DES STRATÉGIES. Ecrite d'abord dans l'orchestrateur le
    29/08, alors que son propre en-tete dit « le juge des stratégies n'implemente aucune de ces
    mesures : il APPELLE » (R-708). Une mesure statistique n'a rien a faire dans
    le programme qui orchestre — et ici elle a de surcroit un calibrage.

    POURQUOI ELLE EST OBLIGATOIRE : un taux nu ne dit rien sans le nombre
    d'operations qui le porte. 58,3 % sur DOUZE operations, c'est sept gagnantes
    sur douze — borne basse 32,0 %, SOUS un point mort de 32,9. Le meme taux sur
    vingt-et-une operations donne 36,5 %, au-dessus. Le rapport affichait
    « +25,3 points de marge » et laissait croire a une marge confortable, alors
    que le cas defavorable etait perdant.
    L'ETUDE 11 l'exige — « la borne basse de Wilson confrontee au point mort de
    la strategie » — et elle n'etait pas branchee.

    ① RÔLE — Transformer un taux de réussite nu en un taux qu'on peut affirmer
      au pire, compte tenu du nombre d'opérations qui le porte. C'est ce chiffre,
      et non le taux observé, qui se compare au point mort. Mesuré le
      19-09-2026 : sept opérations gagnantes sur douze donnent 58,33 % de
      réussite et une borne basse de 31,95 %, sous un point mort de 32,86 % ;
      le même taux sur vingt et une opérations donne une borne basse de 36,47 %,
      au-dessus.
    ② CONTEXTE D'APPEL — Trois appelants. ① `fenetres_glissantes`, une fois par
      fenêtre jugeable, pour dire si cette fenêtre tient face au point mort.
      ② `programmes/JUGE_DES_STRATEGIES.py`, à la main, une fois sur la partie jamais vue
      de la coupure en deux. ③ `_calibrage`, quatre fois.
    ③ ENTRÉE — `n` : le nombre d'opérations sur lequel le taux a été calculé ·
      `wr_pct` : le taux de réussite en pourcents, et il faut lui passer la
      valeur EXACTE et non l'arrondi d'affichage · `z` : le nombre d'écarts
      types qui fixe le niveau de confiance, 1.96 par défaut ; aucun appelant ne
      le change.
    ④ CONDITIONS D'ENTRÉE — Aucune : un nombre d'opérations nul ou négatif rend
      `None` au lieu de lever. Mais le taux doit être EXACT, sinon la borne est
      fausse d'un dixième : sept sur douze vaut 58,333 et non 58,3.
    ⑤ SORTIE — UNE valeur, et sous deux formes selon la branche : `None` quand
      le nombre d'opérations est nul, absent ou inférieur à 1 ; sinon la borne
      basse en pourcents. Exemples mesurés le 19-09-2026 : 31,95 pour sept sur
      douze, 36,47 pour douze sur vingt et un, 20,65 pour une seule opération
      gagnante.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre `None` si le nombre d'opérations est nul ou
      inférieur à 1 · ② ramener le taux entre 0 et 1 · ③ calculer le centre
      corrigé de l'intervalle de Wilson · ④ calculer sa demi-largeur ·
      ⑤ rendre la différence des deux, en pourcents.
    ⑦ UNITÉ — `n` est un NOMBRE D'OPÉRATIONS. `wr_pct` et la valeur rendue sont
      des POURCENTS entre 0 et 100. `z` est un nombre d'écarts types : 1,96
      correspond à un niveau de confiance de 95 %.
    ⑧ POURQUOI — L'intervalle de Wilson est retenu plutôt que l'intervalle
      simple parce qu'il reste correct sur de petits nombres d'opérations, et
      c'est exactement le cas ici : une fenêtre est jugée dès cinq opérations.
      Cette fonction vit dans ce module et non dans le juge des stratégies parce que le
      juge des stratégies déclare lui-même n'implémenter aucune mesure et se contenter
      d'appeler ; elle y avait pourtant été écrite le 29-08-2026, et elle a été
      déplacée ici.
    ⑨ CE QUI CLOCHE —
      ① Elle peut rendre un taux négatif. Mesuré le 19-09-2026 : cinq
      opérations toutes perdantes, donc un taux de 0 %, rendent
      −2,78 dix-millièmes de milliardième au lieu de 0. La valeur est
      négligeable en soi, mais un affichage qui la formate rendrait « −0,0 % »,
      et une comparaison à zéro écrite ailleurs pourrait basculer.
      ② Rien n'oblige l'appelant à passer le taux exact. La fonction reçoit un
      nombre et ne peut pas savoir s'il a été arrondi. Le fichier porte déjà la
      trace de ce piège : la correction qui produit le taux exact avait été
      posée dans le mauvais fichier le 29-08-2026, et la borne continuait d'être
      calculée sur l'arrondi 57,1 sans que rien ne le dise.
      ③ Le niveau de confiance est écrit dans la signature et nulle part
      ailleurs. La valeur 1,96 vaut 95 %, et ce choix ne figure pas au REGISTRE :
      recherche du mot « Wilson » dans `gouvernance/REGISTRE_REGLES.md` à faire
      avant tout changement. Le changer ici changerait silencieusement le
      verdict de chaque fenêtre.
    ⑩ EFFET — Aucun : elle calcule. Aucun fichier, aucun réseau, aucune donnée
      modifiée, rien d'affiché. Elle importe `math` à chaque appel.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas dans les cas que
      ses appelants lui donnent. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      la borne basse de Wilson : le taux de réussite le plus défavorable qui reste compatible avec ce qui a été observé
      le point mort : le taux de réussite en dessous duquel une stratégie perd
        de l'argent
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
      l'ÉTUDE 11 : l'étude datée du projet qui fixe la méthode de jugement des
        stratégies
    
      la partie jamais vue : la fin de la période, celle sur laquelle la stratégie n'a pas été réglée, et donc la seule qui prouve quelque chose
      une fenêtre : un morceau de la période, jugé séparément des autres
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    import math
    if not n or n < 1:
        return None
    p = wr_pct / 100.0
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    e = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100.0 * (c - e)


# ─────────────────────────────────────────────────────────────────────
# LES OBSERVATIONS INDÉPENDANTES — combien d'occasions VRAIMENT distinctes, MESURÉ
# ─────────────────────────────────────────────────────────────────────

def observations_independantes(ops):
    """Mesure le nombre d'observations indépendantes d'une liste d'opérations, par le chevauchement réel des positions.

    ① RÔLE — Dire combien d'occasions VRAIMENT distinctes portent le gain moyen
      d'une stratégie, en le MESURANT pour chaque stratégie, et non en le
      supposant. Deux opérations dont les positions sont ouvertes en même temps
      subissent les mêmes séances de marché : si leurs gains s'écartent de la
      moyenne dans le même sens, elles n'apportent pas deux informations
      distinctes. Cent opérations qui ne se chevauchent jamais valent cent
      observations ; cent opérations rangées en vingt groupes de cinq copies
      ouvertes ensemble en valent vingt. C'est la mesure que demande R-505 ④
      (loi G, non figée) : « Le nombre se mesure pour chaque stratégie, par la
      ressemblance des opérations proches comparée au hasard ; jamais par un
      nombre fixe de séances » (décision de Jean-Luc du 01-11-2026 à 13h19,
      « 1 », n°106 : « A-304 S'APPLIQUE »). « Proches » veut dire ici : ouvertes
      en même temps, ce que disent les propres positions de la stratégie ; aucun
      nombre de séances, aucun seuil, aucune règle à choisir n'y entre.
      HISTOIRE, POUR NE RIEN SUPPRIMER SANS LE DIRE : elle remplace `episodes`
      (signaux distants de 5 séances ou moins regroupés), retirée le 05-11-2026
      (lot S_ep, tour 1, n°106). Au tour 1, elle mesurait la ressemblance des
      opérations voisines DANS L'ORDRE DES NUMÉROS, avec deux règles au choix
      (« prudente », « si_le_hasard_est_battu », constante `REGLES_DE_DEPENDANCE`),
      la troncature de Geyer, le test de Ljung et Box et sa fonction
      `_khi2_au_dela`. Tout cela est SUPPRIMÉ au tour 2 (05-11-2026, avis du
      superviseur R-759 « ARRÊTER ET SIMPLIFIER ») : le rangement par numéro
      mélangeait voisins d'un jour et d'un an, ce qui fabriquait une fausse
      question à Jean-Luc (Q-Sep1, retirée), un réglage en trop et un test sans
      dent. Au tour 3 (05-11-2026, avis du superviseur R-759 « DE FOND ») : la
      mesure du tour 2 est GARDÉE et BORNÉE par le nombre de périodes de marché
      distinctes (voir ⑥ ⑧) — rien n'est supprimé, deux cases s'ajoutent.
      Au tour 4 (05-11-2026, n°194, avis du superviseur R-759 « ARRÊTER ET
      SIMPLIFIER ») : une mesure qui verrait aussi la ressemblance entre
      opérations successives a été éprouvée et N'A PAS été écrite (voir ⑨ ①) ;
      rien n'est supprimé. Le même jour, Jean-Luc a rendu la borne K
      DÉFINITIVE (décision du 05-11-2026 à 18h33, « 1 », n°197 : « le nombre
      d'observations indépendantes retenu = le plus petit de la mesure de
      ressemblance (④, n°106) et du nombre d'opérations qui ne se recouvrent
      pas (K) ; prudence décidée ») : elle n'est plus un choix provisoire du
      Chat (n°194). La méthode entière est expliquée pas à pas dans
      `gouvernance/COMMENT_UNE_STRATEGIE_EST_REGLEE_PUIS_JUGEE.md`, partie 9
      (décision de Jean-Luc du 05-11-2026 à 18h08, « 1 », n°195).
    ② CONTEXTE D'APPEL — `programmes/JUGE_DES_STRATEGIES.py`, fonction `juger`,
      une fois par stratégie jugée, pour l'AFFICHER ; puis le juge de la loi
      (lot JG), qui comparera `n_observations` au plancher
      `plancher_observations` qu'il LIT dans la table de R-505 (jamais écrit
      ici) ; puis le tirage par groupes de n°107, qui lira
      `taille_des_groupes`. JG et n°107 lisent ces deux cases-là, JAMAIS
      `observations_mesurees`, qui est affichée et ne décide pas. JG et n°107 sont À VENIR : relevé le 05-11-2026 par
      recherche du nom dans `programmes/` et `tests/`, les seuls appelants
      AUJOURD'HUI sont le juge (affichage) et l'épreuve
      `tests/EPREUVES_DES_OBSERVATIONS_INDEPENDANTES_Jeu_05-11-2026.py`.
    ③ ENTRÉE — `ops` : la liste des opérations, chacune étant un dictionnaire
      dont trois cases sont lues : `date_entree` et `date_sortie` (textes
      « AAAA-MM-JJ », le jour de l'achat et le jour de la revente) et `net` (le
      gain net en euros). La case `valeur`, si elle existe, ne sert qu'à nommer
      l'opération dans un motif. AUCUN AUTRE ARGUMENT : ni règle, ni seuil, ni
      nombre de séances.
    ④ CONDITIONS D'ENTRÉE — `net` présent et nombre fini, sinon `ValueError`
      qui nomme l'opération. Une date absente, vide, d'un autre type qu'un texte
      ou mal écrite (autre chose que AAAA-MM-JJ, ou un jour qui n'existe pas)
      rend la mesure INCONNUE avec un motif qui nomme l'opération — jamais un
      rangement silencieux (défaut D6 du tour 1). Une date de sortie antérieure
      à la date d'entrée : `ValueError`, une telle opération est impossible.
      Une liste vide est acceptée.
    ⑤ SORTIE — UNE valeur : un dictionnaire, toujours avec les mêmes neuf
      cases : `n_operations` (entier, les opérations reçues) ·
      `n_observations` (le nombre RETENU : le plus petit de
      `observations_mesurees` et `periodes_distinctes` ; nombre à virgule,
      jamais arrondi ici, ou `None` quand la mesure est INCONNUE) ·
      `observations_mesurees` (opérations ÷ facteur, la mesure du tour 2,
      AFFICHÉE, ne décide pas ; ou `None`) · `periodes_distinctes` (K, entier :
      le plus grand nombre de positions deux à deux jamais ouvertes en même
      temps ; `None` si les dates sont illisibles) · `taille_des_groupes`
      (combien d'opérations valent une observation RETENUE : opérations ÷
      `n_observations`, 1,0 au moins, ou `None`) ·
      `paires_qui_se_chevauchent` (entier, ou `None` si les dates sont
      illisibles) · `p_hasard` (la part des tirages au hasard dont le facteur
      atteint celui mesuré, ou `None` sans paire ou sans mesure — AFFICHÉE,
      ELLE NE DÉCIDE RIEN) · `methode` (une phrase qui nomme la méthode) ·
      `motif` (`None`, ou la raison en clair d'une mesure INCONNUE).
      [rend: 1]
    ⑥ TRAITEMENT — ① contrôler le gain et lire les deux dates de chaque
      opération ; noter chaque date illisible ; refuser une sortie avant
      l'entrée · ② si une date est illisible, rendre INCONNU avec son motif ·
      ③ à 0 ou 1 opération, rendre ce nombre · ④ ranger les opérations par
      (entrée, sortie, gain), pour que la probabilité affichée ne dépende pas
      de l'ordre où l'appelant les donne · ④bis compter K, les périodes
      distinctes : parcourir les positions par date de sortie croissante et
      garder chacune dont l'entrée est APRÈS la sortie de la dernière gardée
      (bornes comprises : une entrée le jour même de cette sortie n'est pas
      gardée) ; ce parcours rend exactement le plus grand nombre de positions
      deux à deux jamais ouvertes en même temps. Raison : une ressemblance
      commune à un paquet de positions ouvertes ensemble ne se voit qu'en
      COMPARANT des paquets entre eux ; avec deux paquets, la moyenne tombe
      entre les deux et la ressemblance disparaît (deux paquets de 50 à
      ressemblance vraie 0,5 : vérité 3,9, la mesure seule rend 100 une fois
      sur dix — relecture du tour 2, R-1). Les données ne peuvent donc pas
      garantir plus d'observations indépendantes que de périodes distinctes ·
      ⑤ lister les paires dont les
      positions sont ouvertes en même temps, BORNES COMPRISES (une sortie le
      jour même d'une entrée compte : les deux positions vivent cette séance) ·
      ⑥ calculer l'écart de chaque gain à la moyenne et leur somme des carrés ;
      si elle est nulle (tous les gains égaux), rendre INCONNU avec son motif ·
      ⑦ facteur = 1 + 2 × (somme, sur les paires du ⑤, du produit des deux
      écarts) ÷ (somme des carrés) · ⑧ le facteur est ramené à 1 s'il est
      plus petit ; observations mesurées = opérations ÷ facteur ; observations
      RETENUES (`n_observations`) = le plus petit des observations mesurées et
      de K ; taille des groupes = opérations ÷ observations retenues · ⑨ s'il y
      a au moins une paire : rebattre les écarts 2 000 fois (graine 20261105)
      sur la même liste de paires et compter la part des tirages dont le
      facteur atteint celui mesuré (elle porte sur le facteur, pas sur K).
    ⑦ UNITÉ — `n_operations`, `n_observations`, `observations_mesurees` et
      `periodes_distinctes` sont des NOMBRES d'opérations ; les dates sont des jours du calendrier ; le facteur et
      `p_hasard` sont sans unité. Le gain lu est en euros, mais le résultat ne
      dépend pas de l'unité (multiplier tous les gains par un même nombre ne
      change pas le facteur).
    ⑧ POURQUOI — R-505 ⑤ teste le gain MOYEN ; l'incertitude de cette moyenne
      vaut (variance ÷ n) × (1 + 2 × somme des covariances de toutes les
      paires ÷ (n × variance)). Deux positions qui ne sont jamais ouvertes
      ensemble ne partagent aucune séance de marché : leur covariance est
      supposée nulle, et seules les paires qui se chevauchent comptent. C'est
      le raisonnement classique des rendements qui se chevauchent (Hansen et
      Hodrick, Journal of Political Economy 88(5), 1980 ; Newey et West,
      Econometrica 55(3), 1987, pour la forme pondérée). Une dépendance
      négative n'est jamais créditée — jamais plus d'observations que
      d'opérations — parce que la règle la plus stricte prime. A-304 (BACKLOG,
      28-08-2026) a écrit « 96 À 100 OBSERVATIONS » pour les 100 opérations
      étalons de C5, en comptant les paires « qui font la même chose »
      (gagnant ou perdant) ; cette proportion ne voit pas qu'une période
      entière peut tirer les gains vers le bas (24-04 au 10-06-2026 : 8
      gagnantes sur 20, contre 61 sur 100, sur le tableau du 01-08-2026 ; 7
      sur 20 contre 60 sur 100 sur les opérations rejouées par le juge au
      barème réel — une opération, ENGIE du 27-05-2026, change de signe).
      CHAQUE NOMBRE DE C5 ET SA SOURCE : sur le tableau du 01-08-2026
      (`donnees/TABLEAU_100_TRADES_C5E10_Sam_01-08-2026_23h35.csv`),
      observations mesurées 68,82 (mesure du superviseur R-759 du
      05-11-2026, recalculée en fractions exactes par le relecteur du tour 2) ;
      sur les opérations rejouées par le juge (calibrage, barème réel),
      observations mesurées 70,585 (relevé au tour 2, recalculé à
      l'identique par le relecteur) ; les deux sur 143 paires, mêmes dates,
      seuls les gains diffèrent ; périodes distinctes K = 52 (superviseur
      R-759, avant le tour 3, `superviseur_nuit/sep_t3/sortie_disjointes.txt`,
      mêmes dates donc même K pour les deux) ; RETENU : 52, le plus petit.
      Tous les quatre sont rejoués par l'épreuve E3. A-304 comptait la
      dépendance mesurée SANS test qui décide (ρ = 0,024, non significatif,
      porté quand même) : la probabilité sous le hasard est donc AFFICHÉE et
      ne décide pas ; c'est pourquoi le nombre de tirages et la graine,
      constantes de calcul, peuvent vivre ici sans être une règle de la loi.
      Deux références vérifiées s'ajoutent au tour 4 (05-11-2026) : Newey et
      West (1994), « Automatic Lag Selection in Covariance Matrix
      Estimation », Review of Economic Studies 61(4), p. 631-653,
      https://ideas.repec.org/a/oup/restud/v61y1994i4p631-653..html (la
      règle qui choisit par les données la largeur de la fenêtre, essayée au
      ⑨ ①) ; Britten-Jones, Neuberger et Nolte (2011), Journal of Business
      Finance & Accounting,
      https://openaccess.city.ac.uk/id/eprint/15212/1/JBFA%20Overlapping%20observations%20with%20BrittenJones.pdf
      (« Hansen-Hodrick and Newey-West standard errors tend to be severely
      biased down », cité au ⑨ ①).
    ⑨ CE QUI CLOCHE —
      ⓪ LE PRIX DE LA BORNE K : quand des positions ouvertes ensemble sont en
      réalité indépendantes, K les sous-compte (dix paquets de dix positions
      indépendantes : vérité 100, rendu 10 ; trente positions toutes ouvertes
      ensemble : rendu 1 — superviseur R-759, sortie_disjointes.txt). C'est
      voulu : dans une seule période, l'indépendance des positions ne peut pas
      se vérifier. En mode « un jeton » (positions jamais simultanées), K vaut
      le nombre d'opérations et la borne ne mord jamais.
      Ce que vaut la borne, mesuré dans un monde simulé aux dates de C5
      (superviseur R-759 du 05-11-2026, `mesure_complete/sortie_final.txt`,
      300 mondes par cas, médiane) : sans régime de marché, le plus petit de
      la mesure et de K vaut 52 pour une vérité de 59,2 (prudent) ; avec un
      régime, 52 pour une vérité de 44,1 et 50,3 pour une vérité de 26,4
      (optimiste dans 87 % et 99 % des tirages). K ne mesure aucune
      ressemblance : c'est une prudence. Elle est DÉCIDÉE par Jean-Luc,
      définitivement (05-11-2026 à 18h33, « 1 », n°197), et n'est plus
      provisoire ; les régimes de marché sont confiés à R-505 ⑦ (tenir dans
      chaque époque), selon la même décision. Pour C5, la borne décide :
      52 < 70,585.
      ① La mesure ne voit pas toute la dépendance : une ressemblance commune à
      un paquet de positions ouvertes ensemble n'est mesurable qu'avec
      beaucoup de paquets (c'est pourquoi K la borne, ⑥ ④bis), et une
      dépendance entre positions qui ne se chevauchent pas (un régime de
      marché qui dure plus longtemps qu'une position) est supposée nulle et
      n'est pas vue. C'est une limite à afficher, pas à corriger par un nombre
      de séances.
      Éprouvé au tour 4 (05-11-2026, superviseur R-759, n°194 et n°196) dans
      un monde simulé aux dates de C5, avec un régime commun qui persiste
      d'une séance à l'autre (AR(1), φ = 0,97) ; médianes sur 300 mondes :
      vérité 27,2 ; cette fonction 48,9 ; la même mesure étendue aux paires
      qui ne se chevauchent pas, avec une largeur choisie par la règle de
      Newey et West (1994), 47,2 ; le portefeuille quotidien avec
      Newey-West 97,0 SANS régime, pour une vérité de 60,3
      (`mesure_complete/sortie_etalon.txt`) ; aucune largeur fixe ne descend
      sous 42,6 pour une vérité de 27,3
      (`mesure_complete/sortie_balayage_m.txt`). Aucune n'a donc été écrite.
      La cause : une ressemblance qui dure une part notable de la période se
      confond avec la moyenne estimée (Britten-Jones, Neuberger et Nolte,
      2011 : « Hansen-Hodrick and Newey-West standard errors tend to be
      severely biased down »). Même sans régime, aux durées de C5, cette
      mesure est optimiste : 70,4 en médiane pour une vérité de 60,3
      (`sortie_etalon.txt`). Sur C5 réelle, avec une largeur choisie par les
      données (m = 8), la ressemblance des opérations disjointes est à la
      limite du hasard : p = 0,055 ; la mesure étendue donnerait 62,067
      (`mesure_complete/sortie_final.txt`). Ces fichiers sont dans le
      dossier de travail du Chat du 05-11-2026, pas au dépôt.
      ② Sur une cinquantaine d'opérations, le facteur est bruité ; le bruit
      mesuré sur C5E10-QA-V1 (51 opérations) est déclaré au RAPPORT du lot
      S_ep, tour 2 ; aucun contrôle de ce fichier ne le rejoue.
      ③ Toute paire qui se chevauche pèse autant, qu'elle partage une séance
      ou vingt ; la forme pondérée par la part de séances communes rend 72,1
      au lieu de 68,8 sur le tableau de C5 (superviseur, même sortie). Le
      choix « non pondéré » est celui du superviseur ; non éprouvé au-delà.
      ④ Le calcul des paires est en n² ÷ 2 et la probabilité en 2 000 × (nombre
      de paires) : quelques dixièmes de seconde sur cent opérations ; non
      mesuré au-delà de quelques centaines.
      ⑤ `p_hasard` dépend de la graine : une autre graine donne un autre
      chiffre, à quelques centièmes près ; c'est pourquoi il ne décide rien.
    ⑩ EFFET — Aucun : elle lit. Aucun fichier, aucun réseau, aucune donnée
      modifiée, rien d'affiché. Elle construit une copie triée des dates et
      des gains.
    ⑪ TERMINAISON — Rend la main, ou LÈVE `ValueError` (gain absent ou non
      fini, sortie avant l'entrée) ; l'erreur remonte à l'appelant (le juge
      l'enveloppe et affiche « non mesurées »). Toutes ses boucles sont bornées
      par le nombre d'opérations et le nombre de tirages. Aucun de ses appels
      ne peut ne pas revenir : elle n'appelle que des fonctions de la
      bibliothèque standard (dates, tri, tirage au hasard), qui reviennent
      toutes.
      [sort: non]
    ⑫ DÉFINITIONS
      les périodes distinctes (K) : le plus grand nombre de positions deux à
        deux jamais ouvertes en même temps (bornes comprises) ; dans une même
        période, le mouvement commun du marché n'est tiré qu'une fois
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      une observation indépendante : une opération dont l'issue n'apprend
        rien sur celle d'une autre ; n opérations dont le facteur vaut τ
        valent n ÷ τ observations
      ouvertes en même temps : la date d'entrée de chacune n'est pas après la
        date de sortie de l'autre (bornes comprises)
      le hasard : les mêmes gains, redistribués au hasard sur les mêmes
        positions ; seule la place des gains change, pas les dates
      le plancher : le nombre minimal d'observations indépendantes sous lequel
        R-505 ④ rend NON TRANCHÉE (TROP PETIT) ; il vit dans la table de R-505
        (`gouvernance/REGISTRE_REGLES.md`, clé `plancher_observations`) et
        n'entre pas dans cette fonction
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
      le BACKLOG : `BACKLOG_DECISIONS.md`, le tableau daté des décisions et des
        actions du projet, où chaque ligne porte un identifiant en `A-`
      C5-ETENDU-10 : le nom de la stratégie vivante ; ses seuils et son horizon sont lus dans `donnees/cac40_strategies.csv`.
"""
    import datetime
    import math
    import random
    tirages, graine = 2000, 20261105   # constantes de CALCUL de la probabilité affichée, qui ne décide rien (⑧)
    methode = ("chevauchement reel des positions : facteur = 1 + 2 x (somme, sur les paires d'operations ouvertes en "
               "meme temps, bornes comprises, du produit des ecarts de gain a la moyenne) / (somme des carres des "
               "ecarts), ramene a 1 s'il est plus petit ; observations mesurees = operations / facteur ; observations "
               "retenues = le plus petit des observations mesurees et du nombre K de periodes distinctes (positions "
               "deux a deux jamais ouvertes en meme temps) ; probabilite sous le hasard par %d permutations des gains "
               "(graine %d), affichee, ne decide pas" % (tirages, graine))
    rendu = {"n_operations": len(ops), "n_observations": None, "observations_mesurees": None,
             "periodes_distinctes": None, "taille_des_groupes": None,
             "paires_qui_se_chevauchent": None, "p_hasard": None, "methode": methode, "motif": None}
    illisibles, lues = [], []
    for i, o in enumerate(ops):
        if "net" not in o:
            raise ValueError("operation n°%d : case 'net' absente (%r)" % (i, o))
        g = o["net"]
        if isinstance(g, bool) or not isinstance(g, (int, float)) or not math.isfinite(g):
            raise ValueError("operation n°%d (%s, entree %s) : gain net %r, pas un nombre fini"
                             % (i, o.get("valeur", "valeur inconnue"), o.get("date_entree"), g))
        bornes = []
        for cle in ("date_entree", "date_sortie"):
            t = o.get(cle)
            try:
                if not isinstance(t, str) or len(t) != 10 or t[4] != "-" or t[7] != "-":
                    raise ValueError(t)
                bornes.append(datetime.date.fromisoformat(t))
            except ValueError:
                illisibles.append("operation n°%d (%s, gain %r) : %s %s"
                                  % (i, o.get("valeur", "valeur inconnue"), g, cle,
                                     "absente" if cle not in o else "%r illisible (attendu AAAA-MM-JJ)" % (t,)))
                break
        if len(bornes) == 2:
            if bornes[1] < bornes[0]:
                raise ValueError("operation n°%d (%s) : sortie %s avant l'entree %s"
                                 % (i, o.get("valeur", "valeur inconnue"), bornes[1], bornes[0]))
            lues.append((bornes[0], bornes[1], float(g)))
    if illisibles:
        rendu["motif"] = ("%d operation(s) sans date d'entree ou de sortie lisible, la mesure est INCONNUE : %s"
                          % (len(illisibles), " ; ".join(illisibles[:3]) + (" ; ..." if len(illisibles) > 3 else "")))
        return rendu
    n = len(lues)
    if n <= 1:
        rendu.update(n_observations=float(n), observations_mesurees=float(n), periodes_distinctes=n,
                     taille_des_groupes=1.0, paires_qui_se_chevauchent=0)
        return rendu
    lues.sort()
    periodes, fin = 0, None   # K : positions deux a deux jamais ouvertes ensemble, par date de sortie croissante
    for debut, sortie, _ in sorted(lues, key=lambda x: x[1]):
        if fin is None or debut > fin:
            periodes += 1
            fin = sortie
    rendu["periodes_distinctes"] = periodes
    paires = [(i, j) for i in range(n) for j in range(i + 1, n)
              if not (lues[i][1] < lues[j][0] or lues[j][1] < lues[i][0])]
    rendu["paires_qui_se_chevauchent"] = len(paires)
    gains = [g for _, _, g in lues]
    moyenne = sum(gains) / n
    ecart = [g - moyenne for g in gains]
    somme_carres = sum(e * e for e in ecart)
    if somme_carres == 0.0:
        rendu["motif"] = ("les %d gains sont tous egaux : leur ressemblance n'a pas de sens, "
                          "la mesure est INCONNUE" % n)
        return rendu
    facteur = 1.0 + 2.0 * sum(ecart[i] * ecart[j] for i, j in paires) / somme_carres
    taille = max(facteur, 1.0)
    observations_mesurees = n / taille
    retenu = min(observations_mesurees, float(periodes))
    rendu.update(n_observations=retenu, observations_mesurees=observations_mesurees,
                 taille_des_groupes=n / retenu)
    if paires:
        hasard = random.Random(graine)
        melange = list(ecart)
        atteint = 0
        for _ in range(tirages):
            hasard.shuffle(melange)
            if 1.0 + 2.0 * sum(melange[i] * melange[j] for i, j in paires) / somme_carres >= facteur - 1e-12:
                atteint += 1
        rendu["p_hasard"] = atteint / tirages
    return rendu

# ─────────────────────────────────────────────────────────────────────
# LA COUPURE 70 / 30 — avec nettoyage de la frontière
# ─────────────────────────────────────────────────────────────────────

def coupure_70_30(ops, seances_projet, embargo_seances=None, horizon=None,
                  part=0.70):
    """Coupe le TEMPS en deux, avec PURGE et EMBARGO. Aucun chiffre invente.

    LA METHODE VIENT DE LA LITTERATURE, elle n'est pas de nous : purge et
    embargo, Lopez de Prado 2018, chapitres 7 et 12. « Le purge retire du jeu
    d'apprentissage les observations qui se chevauchent avec le jeu de test ;
    l'embargo elargit l'ecart entre les deux. »

    LES 21 SEANCES SONT UNE VALEUR PUBLIEE, pas un choix arbitraire : « pour les
    periodes de purge et d'embargo nous avons retenu 21 jours, ce qui correspond
    approximativement a un mois de bourse » (Hopfield Networks for Asset
    Allocation, 2024). Un autre travail retient 30 jours. Le Chat avait d'abord
    invente « 20, 30 ou 40 jours » sans source — corrige le 28/08.

    ON COUPE SUR LE TEMPS, JAMAIS SUR LE NOMBRE D'OPERATIONS. Toute la
    litterature procede ainsi — « fenetre d'apprentissage 4 ans, fenetre de
    validation 2 ans ». Le motif est explicite : « les strategies doivent faire
    leurs preuves a travers differentes CONDITIONS DE MARCHE ». Or les conditions
    de marche suivent le TEMPS, pas le compte d'operations. Couper sur le nombre
    peut placer les deux moities dans le meme regime de marche : on ne teste plus
    rien. Defaut commis le 28/08 avant correction.

    CE QUE CETTE FONCTION NE FAIT PAS : elle ne coupe qu'UNE fois. La litterature
    dit qu'il existe mieux — la validation croisee combinatoire purgee, qui coupe
    des dizaines de fois et rend la PROBABILITE que le resultat soit un mirage,
    « nettement superieure pour limiter le sur-ajustement ». Cette mesure existe
    deja dans le module de statistiques du projet, calibree le 24/08, et n'a
    jamais servi.

    ① RÔLE — Séparer la période en une partie sur laquelle la stratégie a été
      mise au point et une partie qu'elle n'a jamais vue, puis rendre le
      résultat de chacune. C'est le second chiffre qui compte : une stratégie
      qui gagne sur la période où on l'a réglée n'a rien prouvé. Entre les deux
      parties, une zone est retirée des deux côtés pour qu'aucune opération
      ouverte avant la frontière ne déborde dans la partie jamais vue.
    ② CONTEXTE D'APPEL — Deux appelants. ① `programmes/JUGE_DES_STRATEGIES.py`, à la
      main, une fois par stratégie jugée, en lui passant l'horizon de la fiche
      et le calendrier réduit à la période que la fiche déclare. ② `_calibrage`,
      deux fois, pour vérifier que la zone retirée ne peut pas être plus courte
      que l'horizon.
    ③ ENTRÉE — `ops` : la liste des opérations, dont seules les cases
      `date_signal` et `net` sont lues · `seances_projet` : toutes les dates de
      séance de la période à couper · `embargo_seances` : la largeur en séances
      de la zone retirée, `None` par défaut, et l'appelant de production laisse
      ce défaut · `horizon` : le nombre de séances pendant lesquelles une
      position est tenue, que le juge des stratégies lit sur la fiche de la stratégie ·
      `part` : la fraction du temps qui va dans la première partie, 0,70 par
      défaut, aucun appelant ne la change.
      CONTRAT DU LOT 0 (09-11-2026) — `horizon` est un entier > 0, None (non
      fourni), ou `COMMUN.HORIZON_AUCUNE` (aucune durée maximale). Ce dernier
      refuse tout calcul par une TypeError : il n'est accepté qu'avec un
      embargo explicite (`embargo_seances`), sinon elle tombe (`int(horizon or 0)`). Rien n'y lit « aucune » en texte.
    ④ CONDITIONS D'ENTRÉE — Les dates doivent s'écrire de la même façon dans
      les opérations et dans le calendrier. Le calendrier ne doit pas être vide,
      sans quoi la recherche de la frontière tombe.
    ⑤ SORTIE — UNE valeur : un dictionnaire, et il prend TROIS formes
      différentes. Sur une liste d'opérations vide, trois cases seulement :
      les deux effectifs et le nombre d'écartées, tous à zéro — mesuré le
      19-09-2026. Quand aucune date n'est reconnue au calendrier : une seule
      case, un motif en clair. Dans le cas normal : sept cases, dont la date de
      frontière, la largeur retenue de la zone retirée, les trois effectifs et
      les deux résumés chiffrés des deux parties.
      [rend: 1]
    ⑥ TRAITEMENT — ① si aucune largeur n'est imposée, prendre la plus grande des
      deux valeurs entre 21 séances et l'horizon · ② rendre trois zéros si la
      liste est vide · ③ numéroter les séances dans l'ordre · ④ ne garder que
      les opérations dont la date de signal est au calendrier, et rendre un
      motif s'il n'en reste aucune · ⑤ placer la frontière aux sept dixièmes du
      calendrier · ⑥ ranger chaque opération avant la zone retirée, après la
      frontière, ou dans la zone retirée · ⑦ rendre les effectifs et le résumé
      de chaque côté.
    ⑦ UNITÉ — Les largeurs et les positions se comptent en SÉANCES de bourse.
      `part` est une FRACTION du temps, jamais un nombre d'opérations. Les
      résumés portent un taux de réussite en POURCENTS et un gain en EUROS.
    ⑧ POURQUOI — La coupure se fait sur le TEMPS et jamais sur le nombre
      d'opérations, parce qu'une stratégie doit faire ses preuves sur des
      CONDITIONS DE MARCHÉ différentes, et que les conditions de marché suivent
      le temps. Couper sur le nombre peut mettre les deux moitiés dans le même
      régime de marché, et alors plus rien n'est testé. Ce défaut a été commis
      le 28-08-2026 avant correction.
      La largeur de la zone retirée ne peut pas être plus courte que l'horizon
      de détention. Écrite en dur à 21 séances, elle laissait déborder toute
      opération ouverte moins de 22 séances avant la frontière sur une fiche
      d'horizon 30 : le nettoyage était incomplet par construction, et l'écart
      grandissait avec l'horizon. Défaut trouvé le 29-08-2026, et corrigé en
      prenant la plus grande des deux valeurs.
    ⑨ CE QUI CLOCHE —
      ① Les deux formes courtes du dictionnaire rendu font tomber le seul
      appelant de production. Le juge des stratégies lit les cases `res_70` et `res_30`
      juste après l'appel ; ces cases n'existent ni sur une liste vide, ni quand
      aucune date n'est reconnue. Mesuré le 19-09-2026 : la lecture rend
      `KeyError: 'res_70'`, que le juge des stratégies rattrape et affiche sous la forme
      « COUPURE 70/30 non mesuree : 'res_70' ». Un lecteur voit un nom de case
      Python, pas la raison, qui est que la période ne portait aucune opération
      reconnue.
      ② La zone retirée n'est retirée que d'un seul côté de la frontière. Les
      opérations rangées avant le sont si leur rang est inférieur à la frontière
      MOINS la largeur, et celles rangées après si leur rang dépasse la
      frontière — sans largeur. La littérature citée décrit deux gestes, la
      purge et l'embargo ; seul le premier est appliqué.
      ③ La frontière est prise sur le CALENDRIER et non sur les opérations. Si
      les opérations sont concentrées dans le premier tiers de la période, la
      partie jamais vue peut n'en contenir aucune, et la fonction rendra deux
      résumés dont l'un porte zéro opération sans qu'aucun avertissement ne le
      dise.
      ④ Les seuils de la méthode vivent ici et nulle part ailleurs : 21 séances
      et sept dixièmes. Recherche du mot « embargo » dans
      `gouvernance/REGISTRE_REGLES.md` le 19-09-2026 : zéro occurrence. Les 21
      séances portent leur source publiée dans ce texte, la coupure aux sept
      dixièmes n'en porte aucune.
    ⑩ EFFET — Aucun : elle lit. Aucun fichier, aucun réseau, aucune donnée
      modifiée, rien d'affiché. Elle construit une copie triée du calendrier et
      trois listes d'opérations.
    ⑪ TERMINAISON — Rend la main dans tous les cas que son appelant lui donne.
      PEUT LEVER sur un calendrier vide, la recherche de la frontière échouant
      alors ; le juge des stratégies rattrape et affiche « COUPURE 70/30 non mesuree ».
      Un de ses appels peut ne pas revenir : `_resume` rend toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS
      la purge : le retrait, du côté apprentissage, des opérations qui
        chevauchent la partie jamais vue
      l'embargo : l'élargissement de l'écart entre les deux parties, ici la zone
        de séances retirée des comptes
      la partie jamais vue : la fin de la période, celle sur laquelle la
        stratégie n'a pas été réglée, et donc la seule qui prouve quelque chose
      une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
      l'horizon : le nombre de séances pendant lesquelles une position est tenue
        si ni l'objectif de gain ni la perte acceptée ne sont atteints
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
      la fiche : la ligne d'une stratégie au registre des stratégies `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte acceptée, son horizon et son univers
    
      PRODUCTION : l etat d une strategie dont le seuil d operations est atteint et les resultats conformes, donc exploitee.
      la raison : le texte court qui dit pourquoi une lecture a échoué, retenu sous le nom `motif`
      le Chat : la conversation qui rédige la gouvernance du projet et dépose ses versions
      le module de statistiques : le programme qui porte le voisinage des réglages et le pire creux, `programmes/MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py`.
      le résumé : le fichier `registre_experiences_resume.csv`, une ligne par balayage — une série d'essais faits d'un coup sur une même stratégie
      un motif : un morceau de nom passé à une fonction de recherche, par exemple trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
      une fiche : la ligne qui décrit une stratégie dans le registre des stratégies, `donnees/cac40_strategies.csv` — son identifiant, ses réglages et ce qu'elle déclare.
      une fraction : la façon d'écrire un pourcentage entre 0 et 1 — 0,040 pour +4 % — par opposition au pourcent, qui écrirait 4.0
"""
    # L'EMBARGO NE PEUT PAS ETRE PLUS COURT QUE L'HORIZON DE DETENTION.
    # Defaut trouve le 29/08 : 21 seances etaient ecrites en dur alors que la
    # fiche jugee portait un horizon de 30. Une operation ouverte 22 seances
    # avant la frontiere debordait donc dans la partie « jamais vue » — le
    # nettoyage etait incomplet PAR CONSTRUCTION, et l'ecart grandit avec
    # l'horizon. Les 21 seances de la litterature valent pour un horizon plus
    # court ; on prend donc le PLUS GRAND des deux.
    if embargo_seances is None:
        embargo_seances = max(21, int(horizon or 0))
    if not ops:
        return {"n_70": 0, "n_30": 0, "n_ecartes": 0}
    cal = sorted(seances_projet)
    rang = {d: i for i, d in enumerate(cal)}
    connues = [o for o in ops if o["date_signal"] in rang]
    if not connues:
        return {"motif": "aucune date de signal reconnue au calendrier"}
    i_frontiere = int(len(cal) * part)
    frontiere = cal[min(i_frontiere, len(cal) - 1)]

    avant, apres, ecartes = [], [], []
    for o in connues:
        r = rang[o["date_signal"]]
        if r < i_frontiere - embargo_seances:
            avant.append(o)
        elif r > i_frontiere:
            apres.append(o)
        else:
            ecartes.append(o)          # la zone d'embargo, retiree des deux cotes
    return {"frontiere": frontiere, "embargo_seances": embargo_seances,
            "n_70": len(avant), "n_30": len(apres), "n_ecartes": len(ecartes),
            "res_70": _resume(avant), "res_30": _resume(apres)}


def _resume(ops):
    """Rend le taux EXACT a cote de l'arrondi d'affichage.

    LA CORRECTION ETAIT ALLEE DANS LA FONCTION HOMONYME DU MAUVAIS FICHIER.
    `wr_exact` avait ete ajoute a `resumer()` du JUGE DES STRATÉGIES le 29/08 — mais la valeur
    qui part a `wilson_bas` vient d'ICI, `_resume()` du module, qui alimente
    `coupure_70_30`. Deux noms quasi identiques dans deux programmes : le
    `b.get("wr_exact", b["wr"])` du juge des stratégies retombait donc sur l'arrondi 57,1 et
    l'ecart de 0,0383 point subsistait, inchange.
    Huitieme fois dans la journee qu'une correction est juste chez celui qui la
    porte et absente chez le voisin — la famille nommee en A-308.

    ① RÔLE — Réduire une liste d'opérations à trois nombres, en rendant le taux
      de réussite SOUS DEUX FORMES : l'arrondi qui sera affiché, et la valeur
      exacte qui sera calculée. La borne basse de Wilson se déplace d'un
      dixième selon qu'on lui donne l'un ou l'autre : douze gagnantes sur vingt
      et une valent 57,142857 et non 57,1.
    ② CONTEXTE D'APPEL — Deux appelants, tous deux dans ce fichier :
      `coupure_70_30`, deux fois par appel, une par partie de la période ; et
      `fenetres_glissantes`, une fois par fenêtre. Aucun appel depuis un autre
      programme — recherche dans tous les fichiers `.py` de `programmes/` le
      19-09-2026, zéro ligne hors de ce fichier.
    ③ ENTRÉE — `ops` : une liste d'opérations, dont seule la case `net` est lue.
      Les deux appelants lui passent un sous-ensemble des opérations qu'ils ont
      eux-mêmes reçues.
    ④ CONDITIONS D'ENTRÉE — Chaque opération doit porter une case `net`. Une
      liste vide est acceptée.
    ⑤ SORTIE — UNE valeur : un dictionnaire, et il prend DEUX formes
      différentes. Sur une liste vide, une seule case, l'effectif à zéro —
      mesuré le 19-09-2026. Sinon quatre cases : l'effectif, le taux de
      réussite arrondi au dixième, le taux exact, et le gain net arrondi au
      centime.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre l'effectif à zéro si la liste est vide · ② compter
      les opérations dont le gain net est strictement positif · ③ rendre
      l'effectif, le taux arrondi, le taux exact et la somme des gains nets.
    ⑦ UNITÉ — L'effectif est un NOMBRE D'OPÉRATIONS. Les deux taux sont des
      POURCENTS entre 0 et 100. Le gain est en EUROS.
    ⑧ POURQUOI — Les deux taux coexistent parce qu'ils servent à deux choses
      qui ne se confondent pas : l'arrondi se lit dans un rapport, l'exact
      alimente un calcul. Un témoin nourri d'un arrondi mesure l'arrondi et non
      le calcul.
      Le fichier porte la trace de ce que coûte la confusion : la même
      correction avait été posée le 29-08-2026 dans une fonction presque
      homonyme d'un autre programme, `resumer` du juge des stratégies, alors que la
      valeur qui part au calcul vient d'ici. Le juge des stratégies lisait donc toujours
      l'arrondi 57,1 et l'écart de 0,0383 point restait entier. C'est la
      huitième occurrence en un jour d'une même famille de défaut, consignée au
      BACKLOG sous l'action A-308 : un correctif juste chez celui qui le porte
      et absent chez son voisin.
    ⑨ CE QUI CLOCHE —
      ① Une opération dont le gain net est exactement nul est comptée comme
      perdante, et rien ne le dit. La condition retenue est « strictement
      positif ». Sur une stratégie dont l'objectif et les frais s'annulent, le
      taux de réussite serait sous-estimé sans qu'aucune case rendue ne permette
      de s'en apercevoir, puisque le nombre d'opérations nulles n'est pas rendu.
      ② Les deux formes du dictionnaire n'ont pas les mêmes cases, et un
      appelant qui lit le taux sur la forme courte ne trouve rien. Le fichier
      s'en protège par des lectures prudentes dans `fenetres_glissantes`, mais
      rien dans la fonction n'impose cette prudence à un futur appelant.
      ③ Le nom prête à confusion avec `resumer` du juge des stratégies, qui fait
      presque la même chose et rend des cases différentes. Deux
      implémentations d'une même chose divergent toujours (R-708) : c'est
      exactement ce qui est arrivé le 29-08-2026, et les deux fonctions vivent
      toujours toutes les deux.
    ⑩ EFFET — Aucun : elle lit. Aucun fichier, aucun réseau, aucune donnée
      modifiée, rien d'affiché.
    ⑪ TERMINAISON — Rend toujours la main. Elle lèverait sur une opération sans
      case `net`, cas qu'aucun appelant ne produit. Aucun de ses appels ne se
      termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le taux de réussite : la part des opérations qui se sont refermées sur un gain, écrite en pourcent
      la borne basse de Wilson : le taux de réussite le plus défavorable qui
        reste compatible avec ce qui a été observé
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
      le BACKLOG : `BACKLOG_DECISIONS.md`, le tableau daté des décisions et des
        actions du projet, où chaque ligne porte un identifiant en `A-`
    
      la trace : la liste des sources avec leur etat — LU, ABSENT ou ILLISIBLE — et un detail chiffre, affichee en pied de page.
      un témoin : un jeu de chiffres dont on connaît d'avance le résultat, employé pour prouver qu'un instrument fonctionne avant de s'en servir
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if not ops:
        return {"n": 0}
    g = sum(1 for o in ops if o["net"] > 0)
    return {"n": len(ops), "wr": round(100 * g / len(ops), 1),
            "wr_exact": 100.0 * g / len(ops),
            "net": round(sum(o["net"] for o in ops), 2)}


def fenetres_glissantes(ops, seances_projet, n=3, embargo=None, horizon=None,
                        point_mort_pct=None):
    """Decoupe la periode en N fenetres successives et juge chacune.

    LA METHODE L'EXIGE — ETUDE 11 : « trois fenetres glissantes (walk-forward) ».
    Le juge des stratégies n'en faisait qu'UNE, la coupure 70/30, et la fonction
    `calculer_walk_forward` du module de statistiques n'etait appelee nulle part.
    Defaut releve par Jean-Luc le 29-08-2026, apres que le Chat lui eut pose une
    question dont la reponse etait ecrite dans sa propre methode.

    POURQUOI TROIS PLUTOT QU'UNE : une coupure unique repond « la strategie
    tient-elle sur la fin ? ». Trois fenetres repondent « tient-elle A CHAQUE
    FOIS ? » — et c'est la seule facon de distinguer une strategie robuste d'une
    strategie qui a eu de la chance sur une periode. Une fenetre qui s'effondre
    quand les deux autres tiennent est un signal que la coupure 70/30 masque
    entierement, puisqu'elle moyenne tout.

    ON DECOUPE LE TEMPS, JAMAIS LE NOMBRE D'OPERATIONS, et chaque frontiere
    porte son embargo, pour les memes raisons que la coupure 70/30.

    ① RÔLE — Répondre à « la stratégie tient-elle À CHAQUE FOIS ? » plutôt qu'à
      « tient-elle sur la fin ? ». La période est découpée en morceaux
      successifs de même durée, chacun est jugé séparément, et chacun est
      comparé à son point mort et non à son seul gain. Une fenêtre qui
      s'effondre pendant que les deux autres tiennent est invisible pour une
      coupure unique, qui moyenne tout.
    ② CONTEXTE D'APPEL — Deux appelants. ① `programmes/JUGE_DES_STRATEGIES.py`, à la
      main, une fois par stratégie jugée, en demandant trois fenêtres et en
      passant le point mort de la stratégie. ② `_calibrage`, cinq fois, pour
      vérifier le découpage, le verdict par point mort, la fin réellement jugée
      et le comptage des opérations écartées.
    ③ ENTRÉE — `ops` : la liste des opérations, dont les cases `date_signal` et
      `net` sont lues · `seances_projet` : toutes les dates de séance de la
      période à découper · `n` : le nombre de fenêtres, 3 par défaut, et le juge des stratégies
      passe 3 explicitement · `embargo` : la largeur en séances de la
      zone retirée en fin de chaque fenêtre, `None` par défaut · `horizon` : le
      nombre de séances pendant lesquelles une position est tenue, lu sur la
      fiche de la stratégie · `point_mort_pct` : le point mort de la stratégie
      en pourcents, `None` par défaut ; sans lui, aucun verdict n'est rendu.
      CONTRAT DU LOT 0 (09-11-2026) — `horizon` est un entier > 0, None (non
      fourni), ou `COMMUN.HORIZON_AUCUNE` (aucune durée maximale). Ce dernier
      refuse tout calcul par une TypeError : il n'est accepté qu'avec un
      embargo explicite (`embargo`), sinon elle tombe (`int(horizon or 0)`). Rien n'y lit « aucune » en texte.
    ④ CONDITIONS D'ENTRÉE — Les dates doivent s'écrire de la même façon dans les
      opérations et dans le calendrier. Le nombre de fenêtres demandé doit être
      au moins 1. Le calendrier doit porter au moins autant de séances que de
      fenêtres, sans quoi les premières fenêtres sont vides.
    ⑤ SORTIE — UNE valeur : un dictionnaire, et il prend DEUX formes
      différentes. Quand la liste ou le calendrier sont vides, ou qu'aucune date
      n'est reconnue : deux cases, un nombre de fenêtres à zéro et un motif en
      clair. Dans le cas normal : onze cases, dont la liste des fenêtres, le
      nombre d'opérations écartées par les zones retirées, le point mort employé
      et trois verdicts d'ensemble.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre un motif si la liste ou le calendrier sont vides ·
      ② si aucune largeur n'est imposée, prendre la plus grande des deux valeurs
      entre 21 séances et l'horizon · ③ numéroter les séances dans l'ordre ·
      ④ ne garder que les opérations reconnues au calendrier · ⑤ découper le
      calendrier en morceaux de même longueur, le dernier prenant le reste ·
      ⑥ pour chaque morceau, garder les opérations nées entre son début et sa
      fin moins la zone retirée · ⑦ noter pour chaque fenêtre la fin RÉELLEMENT
      jugée et la fin du découpage, qui diffèrent de la largeur retirée ·
      ⑧ pour chaque fenêtre portant au moins 5 opérations, calculer la borne
      basse de Wilson et dire si elle passe le point mort · ⑨ compter les
      opérations qui ne sont dans aucune fenêtre · ⑩ rendre l'ensemble avec les
      verdicts.
    ⑦ UNITÉ — Les largeurs, les positions et les fins se comptent en SÉANCES de
      bourse. Les taux et le point mort sont des POURCENTS entre 0 et 100. Les
      gains sont en EUROS.
    ⑧ POURQUOI — Une fenêtre se juge contre SON point mort, jamais sur son seul
      gain. La première version ne regardait que le gain, et le juge des stratégies
      imprimait « les trois fenetres sont GAGNANTES » alors que la première
      fenêtre était SOUS le point mort pour les trois stratégies mesurées le
      29-08-2026 : 35,4 contre 43,1, 38,7 contre 43,1, 25,4 contre 32,9. La
      règle était écrite vingt lignes plus haut, dans le bloc de la coupure en
      deux, et absente ici — la famille de défaut consignée au BACKLOG sous
      l'action A-308 — et cette fois elle produisait une phrase fausse en gras
      dans un rapport qu'on lit vite.
      La fin affichée est la fin RÉELLEMENT jugée et non celle du découpage,
      parce que la zone retirée ampute chaque fenêtre de 21 séances : afficher la
      fin entière faisait chercher une opération du 15-10-2024 dans une fenêtre
      qui s'arrêtait au 01-10, sans que rien ne le dise.
      Et les opérations tombées dans les zones retirées sont COMPTÉES : sans
      cette case, un lecteur qui additionne les trois fenêtres trouve un total
      inférieur au nombre d'opérations sans savoir pourquoi — jusqu'à 12 sur 56
      pour la stratégie mesurée le 29-08-2026, soit une sur cinq.
    ⑨ CE QUI CLOCHE —
      ① Le verdict d'ensemble ne porte que sur les fenêtres jugeables, et le
      nombre de fenêtres écartées n'est pas rendu séparément. Une période où
      deux fenêtres sur trois porteraient moins de 5 opérations rendrait
      « toutes tiennent » sur la foi d'une seule fenêtre, et seule la lecture
      du détail permettrait de s'en apercevoir.
      ② Le seuil de 5 opérations qui rend une fenêtre jugeable est écrit dans
      le code et nulle part ailleurs, et il n'a pas de source citée,
      contrairement aux 21 séances de la zone retirée qui portent la leur dans
      ce texte.
      ③ Le découpage en morceaux de même longueur jette les séances restantes
      dans la dernière fenêtre. Sur un calendrier de 100 séances découpé en 3,
      les deux premières fenêtres en portent 33 et la dernière 34 : les fenêtres
      ne sont pas comparables à durée égale, et rien ne le signale.
      ④ Un nombre de fenêtres supérieur au nombre de séances rend des fenêtres
      vides sans avertissement : la longueur d'un morceau devient zéro, et
      toutes les fenêtres sauf la dernière commencent et finissent au même
      point.
    ⑩ EFFET — Aucun : elle lit. Aucun fichier, aucun réseau, aucune donnée
      modifiée, rien d'affiché. Elle construit une copie triée du calendrier et
      une liste par fenêtre.
    ⑪ TERMINAISON — Rend la main dans tous les cas que ses appelants lui
      donnent. PEUT LEVER sur un nombre de fenêtres nul, la division tombant
      alors ; le juge des stratégies rattrape et affiche « TROIS FENETRES non
      mesurees ». Deux de ses appels peuvent ne pas revenir en théorie :
      `_resume` et `wilson_bas` rendent toutes deux toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS
      une fenêtre : un morceau de la période, jugé séparément des autres
      l'embargo : l'élargissement de l'écart entre les deux parties, ici la zone de séances retirée des comptes
      le point mort : le taux de réussite en dessous duquel une stratégie perd
        de l'argent
      la borne basse de Wilson : le taux de réussite le plus défavorable qui
        reste compatible avec ce qui a été observé
      une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
      l'horizon : le nombre de séances pendant lesquelles une position est tenue
        si ni l'objectif de gain ni la perte acceptée ne sont atteints
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
      le BACKLOG : `BACKLOG_DECISIONS.md`, le tableau daté des décisions et des
        actions du projet, où chaque ligne porte un identifiant en `A-`
    
      le Chat : la conversation qui rédige la gouvernance du projet et dépose ses versions
      un motif : un morceau de nom passé à une fonction de recherche, par exemple trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
      un signal : le repérage, sur la dernière séance connue, d'une configuration de cours qui déclenche une simulation d'achat.
"""
    if not ops or not seances_projet:
        return {"n_fenetres": 0, "motif": "operations ou calendrier absents"}
    if embargo is None:
        embargo = max(21, int(horizon or 0))
    cal = sorted(seances_projet)
    rang = {d: i for i, d in enumerate(cal)}
    connues = [o for o in ops if o["date_signal"] in rang]
    if not connues:
        return {"n_fenetres": 0, "motif": "aucune date reconnue"}

    taille = len(cal) // n
    fenetres = []
    for k in range(n):
        i_debut = k * taille
        i_fin = (k + 1) * taille if k < n - 1 else len(cal)
        # l'embargo retire les operations nees juste avant la fin de la fenetre,
        # qui deborderaient sur la suivante
        dedans = [o for o in connues
                  if i_debut <= rang[o["date_signal"]] < i_fin - embargo]
        # LA FENETRE AFFICHE LA FIN QU'ELLE JUGE, PAS CELLE DU DECOUPAGE.
        # L'embargo retire les operations nees dans les dernieres seances ; la
        # fin REELLEMENT jugee est donc anterieure a la fin du decoupage — de
        # 21 seances a chaque fenetre, mesure le 29/08. Afficher la fin entiere
        # faisait chercher une operation du 15-10-2024 dans une fenetre qui
        # s'arretait au 01-10, sans que rien ne le dise. Un chiffre ne s'emploie
        # qu'avec ce qu'il mesure — ici sur une date.
        r = _resume(dedans)
        _i_jugee = max(i_debut, min(i_fin - embargo, len(cal)) - 1)
        fenetres.append({
            "n_fenetre": k + 1,
            "debut": cal[i_debut],
            "fin": cal[_i_jugee],
            "fin_decoupage": cal[min(i_fin - 1, len(cal) - 1)],
            "embargo_seances": embargo,
            "n": r["n"],
            "wr": r.get("wr"),
            "wr_exact": r.get("wr_exact"),
            "net": r.get("net"),
        })
    # UNE FENETRE SE JUGE CONTRE SON POINT MORT, PAS SUR SON SEUL GAIN.
    # Premiere version : « toutes_positives » ne regardait que le net. Le juge des stratégies
    # imprimait donc « les trois fenetres sont GAGNANTES » alors que la premiere
    # fenetre est SOUS le point mort pour les trois strategies mesurees le
    # 29/08 — QA-V1 35,4 contre 43,1 · OBS-V1 38,7 contre 43,1 · C5-EI-PARAMS
    # 25,4 contre 32,9. La regle « un taux se juge contre son point mort » etait
    # juste dans le bloc de la coupure et absente vingt lignes plus loin :
    # A-308 a l'identique, et cette fois elle produisait une phrase FAUSSE en
    # gras dans un rapport qu'on lit vite.
    utiles = [f for f in fenetres if f["n"] >= 5]
    for f in utiles:
        f["au_pire"] = wilson_bas(f["n"], f.get("wr_exact") if f.get("wr_exact")
                                  is not None else f["wr"])
        if point_mort_pct is not None and f["au_pire"] is not None:
            f["tient"] = f["au_pire"] > point_mort_pct
        else:
            f["tient"] = None
    # ON DIT CE QUE L'EMBARGO LAISSE DEHORS.
    # Les fenetres affichent leur vraie fin depuis le 29/08 — mais les
    # operations qui tombent dans les trous d'embargo n'etaient comptees NULLE
    # PART. Mesure du jour : 12 operations sur 56 pour la candidate, une sur
    # cinq. Un lecteur qui additionne les trois fenetres trouve un compte faux
    # sans savoir pourquoi. Le retrait est juste, son silence ne l'etait pas.
    _dans = sum(f["n"] for f in fenetres)
    _dehors = len(connues) - _dans
    return {"n_fenetres": n, "embargo_seances": embargo,
            "fenetres": fenetres,
            "n_utiles": len(utiles),
            "n_operations": len(connues),
            "n_dans_fenetres": _dans,
            "n_ecartees_embargo": _dehors,
            "point_mort": point_mort_pct,
            "toutes_gagnantes": all(f["net"] and f["net"] > 0 for f in utiles)
                                if utiles else None,
            "toutes_tiennent": (all(f["tient"] for f in utiles)
                                if utiles and point_mort_pct is not None
                                else None),
            "n_sous_le_point_mort": sum(1 for f in utiles if f.get("tient") is False)}


# ─────────────────────────────────────────────────────────────────────
# LES ÉPOQUES — R-505 ⑦ — et LE GROUPE TÉMOIN — R-505 ⑪ (lot S_per, étape D, 05-11-2026)
# ─────────────────────────────────────────────────────────────────────

def lire_les_epoques(texte, annees_d_examen, seances):
    """Lit le champ « epoques » d'une déclaration datée et rend les époques, avec leur part des séances.

    ① RÔLE — Transformer le découpage écrit dans la déclaration (« AAAA-MM-JJ..AAAA-MM-JJ ; … ») en
      une liste d'époques vérifiée, et dire, pour chacune, quelle part des séances des années d'examen
      elle porte. R-505 ⑦ exige que les époques soient « fixées d'avance » : le découpage vient donc de
      la déclaration et de nulle part ailleurs ; s'il manque ou s'il est faux, rien ne le remplace.
    ② CONTEXTE D'APPEL — Le juge de la loi (lot JG, À VENIR) une fois par verdict, avec le champ
      `epoques` et le champ `annees_d_examen` de la déclaration datée (contrat DECLARATION_DATEE) et les
      séances du calendrier (`programmes/CALENDRIER_DE_LA_BOURSE.py`, `seances_entre`). Relevé le
      05-11-2026 : seule l'épreuve `tests/EPREUVES_DES_EPOQUES_Jeu_05-11-2026.py` l'appelle aujourd'hui.
    ③ ENTRÉE — `texte` : le champ `epoques`, des morceaux « début..fin » séparés par « ; » ·
      `annees_d_examen` : le champ du même nom, un seul morceau « début..fin » · `seances` : les
      séances de bourse qui couvrent les années d'examen, des dates (`datetime.date`) ou des textes
      AAAA-MM-JJ, dans n'importe quel ordre.
    ④ CONDITIONS D'ENTRÉE — Aucune sur `texte` et `annees_d_examen` : tout défaut y est RENDU comme un
      motif, jamais levé. `seances` doit être itérable ; un élément qui n'est ni une date ni un texte
      AAAA-MM-JJ lève `ValueError`.
    ⑤ SORTIE — UNE valeur : un dictionnaire à trois cases. `epoques` : la liste, dans l'ordre du temps,
      de {"debut", "fin" (textes AAAA-MM-JJ), "seances" (entier)}, ou `None` · `parts_des_seances` : la
      liste des parts (séances de l'époque ÷ séances des années d'examen), même ordre, ou `None` ·
      `motif` : `None`, ou « NON JUGEABLE — <champ> : <raison> », qui nomme le champ de la déclaration
      en défaut (`epoques`, ou `annees_d_examen` s'il est illisible).
      [rend: 1]
    ⑥ TRAITEMENT — ① lire les années d'examen ; illisibles → motif qui nomme `annees_d_examen` ·
      ② champ `epoques` vide ou absent → motif « champ vide » · ③ lire chaque morceau ; date illisible,
      séparateur absent ou début après la fin → motif · ④ ranger par début ; un début qui n'est pas
      APRÈS la fin de l'époque précédente → motif « chevauchement » · ⑤ une époque qui sort des années
      d'examen → motif « débordement » · ⑥ compter les séances de chaque époque ; une séance des années
      d'examen qui n'est dans aucune époque → motif « trou », qui nomme la première ; une époque sans
      séance → motif · ⑦ rendre les époques et leurs parts.
    ⑦ UNITÉ — Les dates sont des jours du calendrier ; `seances` se compte en SÉANCES ; les parts sont
      des fractions sans unité dont la somme vaut 1.
    ⑧ POURQUOI — R-505 ⑦ : « le découpage exact est fixé dans la déclaration, avant de regarder »
      (décision de Jean-Luc du 31-10-2026 à 22h49, n°58) ; « ces 4 époques sont fixées avant le test »
      (n°80). Un découpage écrit en repli dans le code serait choisi par le programme, pas déclaré :
      c'est pourquoi un champ vide rend NON JUGEABLE et n'est jamais complété. Le trou se compte en
      SÉANCES et non en jours : entre une époque qui finit le 31-12 et une qui commence le 02-01, le
      1er janvier n'est pas un trou, puisque la Bourse est fermée (R-110 : une séance se lit dans un
      calendrier, jamais dans les cours). Les parts servent au minimum calculé
      (`minimum_d_epoques_gagnantes`) : une époque longue a plus de chances d'être gagnante qu'une
      courte, à avantage égal.
    ⑨ CE QUI CLOCHE — ① Si le calendrier reçu ne couvre pas toutes les années d'examen (il commence
      après leur début, par exemple), les parts sont calculées sur ce qu'il porte, sans le dire : la
      couverture est l'affaire de l'appelant (`seances_entre` lève hors couverture). ② Les époques sont
      rangées par leur début : un champ écrit dans le désordre est accepté s'il est par ailleurs juste.
      ③ Le séparateur « .. » et « ; » est celui du commentaire du contrat (DECLARATION_DATEE) ; aucun
      autre n'est lu.
    ⑩ EFFET — Aucun : elle lit ses arguments, n'écrit rien, n'affiche rien.
    ⑪ TERMINAISON — Rend la main, ou lève `ValueError` sur une séance mal formée. Ses boucles sont
      bornées par le nombre de morceaux et de séances. Aucun de ses appels ne peut ne pas revenir : elle
      n'appelle que la bibliothèque standard (dates).
      [sort: non]
    ⑫ DÉFINITIONS
      une époque : un morceau des années d'examen, fixé dans la déclaration avant de regarder
      une séance : un jour où la Bourse de Paris tient séance, lu au calendrier
    """
    import datetime
    rendu = {"epoques": None, "parts_des_seances": None, "motif": None}
    morceaux_examen = annees_d_examen.split("..") if isinstance(annees_d_examen, str) else []
    dates_examen = []
    for morceau in morceaux_examen:
        m = morceau.strip()
        try:
            lue = datetime.date.fromisoformat(m)
            if lue.isoformat() != m:
                raise ValueError(m)
            dates_examen.append(lue)
        except ValueError:
            break
    if len(morceaux_examen) != 2 or len(dates_examen) != 2 or dates_examen[0] > dates_examen[1]:
        rendu["motif"] = "NON JUGEABLE — annees_d_examen : %r illisible (attendu AAAA-MM-JJ..AAAA-MM-JJ)" % (
            annees_d_examen,)
        return rendu
    debut_examen, fin_examen = dates_examen
    if not isinstance(texte, str) or not texte.strip():
        rendu["motif"] = ("NON JUGEABLE — epoques : champ vide, aucune époque déclarée ; le découpage se fixe "
                          "dans la déclaration, avant de regarder (R-505 ⑦), il n'est jamais complété ici")
        return rendu
    lues = []
    for morceau in texte.split(";"):
        bornes = morceau.strip().split("..")
        dates = []
        for b in bornes:
            b = b.strip()
            try:
                lue = datetime.date.fromisoformat(b)
                if lue.isoformat() != b:
                    raise ValueError(b)
                dates.append(lue)
            except ValueError:
                break
        if len(bornes) != 2 or len(dates) != 2:
            rendu["motif"] = ("NON JUGEABLE — epoques : morceau %r illisible (attendu AAAA-MM-JJ..AAAA-MM-JJ, "
                              "morceaux séparés par « ; »)" % (morceau.strip(),))
            return rendu
        if dates[0] > dates[1]:
            rendu["motif"] = "NON JUGEABLE — epoques : époque %r, le début est après la fin" % (morceau.strip(),)
            return rendu
        lues.append((dates[0], dates[1]))
    lues.sort()
    for precedente, suivante in zip(lues, lues[1:]):
        if suivante[0] <= precedente[1]:
            rendu["motif"] = ("NON JUGEABLE — epoques : chevauchement, l'époque qui commence le %s commence "
                              "avant la fin de la précédente (%s)" % (suivante[0], precedente[1]))
            return rendu
    if lues[0][0] < debut_examen or lues[-1][1] > fin_examen:
        rendu["motif"] = ("NON JUGEABLE — epoques : débordement, les époques vont du %s au %s et les années "
                          "d'examen du %s au %s" % (lues[0][0], lues[-1][1], debut_examen, fin_examen))
        return rendu
    jours = set()
    for s in seances:
        if isinstance(s, datetime.date):
            jours.add(s if not isinstance(s, datetime.datetime) else s.date())
        else:
            try:
                lue = datetime.date.fromisoformat(s) if isinstance(s, str) else None
            except ValueError:
                lue = None
            if lue is None or lue.isoformat() != s:
                raise ValueError("seance %r : ni une date ni un texte AAAA-MM-JJ" % (s,))
            jours.add(lue)
    jours_examen = sorted(j for j in jours if debut_examen <= j <= fin_examen)
    comptes = [0] * len(lues)
    for j in jours_examen:
        place = [i for i, (a, b) in enumerate(lues) if a <= j <= b]
        if not place:
            rendu["motif"] = ("NON JUGEABLE — epoques : trou, la séance du %s est dans les années d'examen et "
                              "dans aucune époque déclarée" % (j,))
            return rendu
        comptes[place[0]] += 1
    for (a, b), c in zip(lues, comptes):
        if c == 0:
            rendu["motif"] = "NON JUGEABLE — epoques : l'époque %s..%s ne porte aucune séance" % (a, b)
            return rendu
    total = sum(comptes)
    rendu["epoques"] = [{"debut": a.isoformat(), "fin": b.isoformat(), "seances": c}
                        for (a, b), c in zip(lues, comptes)]
    rendu["parts_des_seances"] = [c / total for c in comptes]
    return rendu


def loi_de_student_inferieure(t, ddl):
    """Rend la probabilité qu'une variable de Student à `ddl` degrés de liberté soit inférieure ou égale à `t`.

    ① RÔLE — Donner la probabilité d'un résultat aussi bas que `t` sous la loi de Student, celle de la
      moyenne d'un petit échantillon dont l'écart-type est estimé. Elle sert à dire si une époque est
      « perdante à coup sûr » (R-505 ⑦).
    ② CONTEXTE D'APPEL — `probabilite_epoque_perdante`, une fois par époque ; l'épreuve
      `tests/EPREUVES_DES_EPOQUES_Jeu_05-11-2026.py` (E4, valeurs connues).
    ③ ENTRÉE — `t` : un nombre réel · `ddl` : le nombre de degrés de liberté, un nombre réel strictement
      positif (il peut avoir une virgule : le nombre d'observations retenu en a souvent une).
    ④ CONDITIONS D'ENTRÉE — `t` fini, `ddl` fini et > 0 ; sinon `ValueError`. Un booléen est refusé.
    ⑤ SORTIE — UNE valeur : la probabilité, entre 0 et 1.
      [rend: 1]
    ⑥ TRAITEMENT — ① t = 0 rend un demi · ② sinon x = ddl ÷ (ddl + t²) et la fonction bêta incomplète
      régularisée I_x(ddl ÷ 2, ½) se calcule par sa fraction continue (méthode de Lentz modifiée), sur
      x ou sur 1 − x selon le côté où elle converge vite · ③ P(T ≤ t) = ½ I_x pour t < 0, 1 − ½ I_x
      sinon.
    ⑦ UNITÉ — Sans unité : `t` est un nombre d'écarts-types, la sortie une probabilité.
    ⑧ POURQUOI — Sur une époque de peu d'observations, la loi normale rend des probabilités trop
      petites et déclarerait « perdante » une époque saine (superviseur R-759 du 05-11-2026, lot S_per,
      §3). Aucune loi de Student n'existait dans `programmes/` (seule `phi_inv`, enfermée dans le module
      de statistiques), et scipy n'est pas dans le circuit. La formule est celle des manuels :
      Abramowitz et Stegun, 26.7.1 et 26.5.8 ; fraction continue de la bêta incomplète, Press et al.,
      « Numerical Recipes », §6.4.
    ⑨ CE QUI CLOCHE — ① Le plafond d'itérations est un nombre de calcul (100 fois la racine de
      ddl ÷ 2 + ½, plus 100) ; s'il est atteint, elle lève au lieu de rendre une valeur fausse.
      ② Précision éprouvée à 10⁻³ près sur trois valeurs de table (E4), pas au-delà.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève `ValueError` (entrée invalide) ou `ArithmeticError` (fraction
      continue non convergée au plafond). La boucle est bornée par le plafond. Aucun de ses appels ne
      peut ne pas revenir : `math` seulement.
      [sort: non]
    """
    import math
    import sys
    for nom, v in (("t", t), ("ddl", ddl)):
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
            raise ValueError("%s = %r : pas un nombre fini" % (nom, v))
    if ddl <= 0:
        raise ValueError("ddl = %r : doit être strictement positif" % (ddl,))
    if t == 0:
        return 0.5
    x = ddl / (ddl + t * t)
    a, b = ddl / 2, 0.5
    if x >= 1:
        return 0.5
    tete = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log1p(-x))
    symetrique = x >= (a + 1) / (a + b + 2)
    aa, bb, xx = (b, a, 1 - x) if symetrique else (a, b, x)
    minuscule, eps = sys.float_info.min, sys.float_info.epsilon
    c, d = 1.0, 1 - (aa + bb) * xx / (aa + 1)
    d = 1 / (d if abs(d) >= minuscule else minuscule)
    h = d
    plafond = (math.isqrt(int(aa + bb)) + 1) * 100
    m = 1
    while True:
        if m > plafond:
            raise ArithmeticError("loi de Student : fraction continue non convergée (t=%r, ddl=%r)" % (t, ddl))
        num = m * (bb - m) * xx / ((aa - 1 + 2 * m) * (aa + 2 * m))
        d = 1 + num * d
        d = 1 / (d if abs(d) >= minuscule else minuscule)
        c = 1 + num / c
        c = c if abs(c) >= minuscule else minuscule
        h *= d * c
        num = -(aa + m) * (aa + bb + m) * xx / ((aa + 2 * m) * (aa + 1 + 2 * m))
        d = 1 + num * d
        d = 1 / (d if abs(d) >= minuscule else minuscule)
        c = 1 + num / c
        c = c if abs(c) >= minuscule else minuscule
        h *= d * c
        if abs(d * c - 1) <= 2 * eps:
            break
        m += 1
    i_x = 1 - tete * h / aa if symetrique else tete * h / aa
    return 0.5 * i_x if t < 0 else 1 - 0.5 * i_x


def probabilite_epoque_perdante(gains_eur, n_retenu):
    """Rend la probabilité qu'une époque aussi mauvaise vienne d'une stratégie qui ne perd pas, par Student.

    ① RÔLE — Dire si une époque est « perdante à coup sûr » au sens de R-505 ⑦ : la probabilité p de
      voir un gain moyen aussi bas si le vrai gain moyen était nul ; p petit = perdante à coup sûr.
      La comparaison au seuil est faite par l'appelant (`controle_des_epoques`), qui lit le seuil.
    ② CONTEXTE D'APPEL — `controle_des_epoques`, une fois par époque qui porte au moins une opération ;
      l'épreuve `tests/EPREUVES_DES_EPOQUES_Jeu_05-11-2026.py` (E5, E9).
    ③ ENTRÉE — `gains_eur` : les gains nets des opérations de l'époque, en euros · `n_retenu` : le
      nombre d'observations indépendantes RETENU pour ces opérations
      (`observations_independantes(ops_de_l_epoque)["n_observations"]`), ou `None` s'il est INCONNU.
    ④ CONDITIONS D'ENTRÉE — Chaque gain est un nombre fini, sinon `ValueError` ; `n_retenu` est `None`
      ou un nombre fini, sinon `ValueError`.
    ⑤ SORTIE — UNE valeur : un dictionnaire {"p_perdante", "t", "ddl", "motif"} ; `p_perdante`, `t` et
      `ddl` valent `None` et `motif` dit pourquoi quand la probabilité ne se calcule pas.
      [rend: 1]
    ⑥ TRAITEMENT — ① contrôler les gains · ② `n_retenu` absent → motif « mesure manquante » ;
      `n_retenu` < 2 → motif (aucun degré de liberté) ; moins de deux gains → motif · ③ s = écart-type
      des gains (diviseur n − 1) ; s nul → motif · ④ t = moyenne ÷ (s ÷ √n_retenu), ddl = n_retenu − 1
      · ⑤ p = `loi_de_student_inferieure(t, ddl)`, unilatéral.
    ⑦ UNITÉ — Gains en EUROS ; `t` sans unité ; `ddl` en observations ; `p_perdante` probabilité.
    ⑧ POURQUOI — Le nombre qui divise l'écart-type est le nombre RETENU et pas le nombre d'opérations :
      des opérations ouvertes ensemble n'apportent pas autant d'information qu'elles sont nombreuses ;
      c'est la décision de Jean-Luc du 05-11-2026 à 18h33 (« 1 », n°197 : « le nombre d'observations
      indépendantes retenu = le plus petit de la mesure de ressemblance (④, n°106) et du nombre
      d'opérations qui ne se recouvrent pas (K) »). Compter les opérations ferait passer pour
      « perdante à coup sûr » une époque qui n'a que quelques occasions vraiment distinctes (E5 : 20
      opérations en 4 paquets → p 0,003 à n = 20, 0,15 à n = 4). Student plutôt que la loi normale :
      voir `loi_de_student_inferieure`, ⑧.
    ⑨ CE QUI CLOCHE — ① L'écart-type est celui des opérations, pas celui des observations retenues :
      c'est l'écart-type d'une opération, divisé par la racine du nombre retenu (formule du superviseur,
      §3). ② Le test suppose des gains à peu près normaux ; non éprouvé sur des gains très asymétriques.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève `ValueError`, ou laisse remonter `ArithmeticError` de
      `loi_de_student_inferieure`. Aucune boucle hors de la lecture des gains. Aucun de ses appels ne
      peut ne pas revenir : `loi_de_student_inferieure` est bornée par son plafond.
      [sort: non]
    """
    import math
    import statistics
    gains = list(gains_eur)
    for i, g in enumerate(gains):
        if isinstance(g, bool) or not isinstance(g, (int, float)) or not math.isfinite(g):
            raise ValueError("gain n°%d = %r : pas un nombre fini" % (i, g))
    rendu = {"p_perdante": None, "t": None, "ddl": None, "motif": None}
    if n_retenu is None:
        rendu["motif"] = "MESURE MANQUANTE : nombre d'observations indépendantes retenu INCONNU"
        return rendu
    if isinstance(n_retenu, bool) or not isinstance(n_retenu, (int, float)) or not math.isfinite(n_retenu):
        raise ValueError("n_retenu = %r : pas un nombre fini" % (n_retenu,))
    if n_retenu < 2:
        rendu["motif"] = ("NON TRANCHÉE : %s observation(s) retenue(s), il en faut au moins 2 pour un écart-type"
                          % (n_retenu,))
        return rendu
    if len(gains) < 2:
        rendu["motif"] = "NON TRANCHÉE : %d gain(s), il en faut au moins 2 pour un écart-type" % len(gains)
        return rendu
    s = statistics.stdev(gains)
    if s == 0:
        rendu["motif"] = "NON TRANCHÉE : les %d gains sont égaux, écart-type nul" % len(gains)
        return rendu
    t = (math.fsum(gains) / len(gains)) / (s / math.sqrt(n_retenu))
    ddl = n_retenu - 1
    rendu.update(t=t, ddl=ddl, p_perdante=loi_de_student_inferieure(t, ddl))
    return rendu


def minimum_d_epoques_gagnantes(parts_des_seances, seuil_de_preuve, seuil_epoque):
    """Calcule, avant tout regard, le nombre minimal d'époques gagnantes qu'exige R-505 ⑦.

    ① RÔLE — Rendre le « minimum calculé par programme » de R-505 ⑦ (table : clé
      `epoques_gagnantes_minimum`), pour une stratégie, à partir de ce que sa déclaration fixe : le
      seuil de preuve de ⑤ (0,05 ÷ k) et la part de séances de chaque époque. ELLE NE REÇOIT AUCUNE
      OPÉRATION NI AUCUN GAIN : le minimum se calcule dès la déclaration, avant le regard.
    ② CONTEXTE D'APPEL — `controle_des_epoques` ; plus tard le juge de la loi (lot JG, À VENIR), qui
      peut l'appeler dès la déclaration pour afficher le minimum avant de jouer ; l'épreuve
      `tests/EPREUVES_DES_EPOQUES_Jeu_05-11-2026.py` (E1, E2, E3).
    ③ ENTRÉE — `parts_des_seances` : la part de séances de chaque époque (`lire_les_epoques`) ·
      `seuil_de_preuve` : le seuil de ⑤, 0,05 ÷ k, calculé par l'appelant avec la valeur lue dans la
      table de R-505 (clé `seuil_de_preuve`) · `seuil_epoque` : la clé `epoque_perdante` de la table.
      AUCUN ARGUMENT N'A DE VALEUR PAR DÉFAUT.
    ④ CONDITIONS D'ENTRÉE — Au moins une part ; chaque part dans ]0, 1] ; leur somme vaut 1 (à
      l'arrondi près) ; les deux seuils dans ]0, 1[. Sinon `ValueError`.
    ⑤ SORTIE — UNE valeur : un dictionnaire {"minimum" (entier entre 0 et le nombre d'époques),
      "probabilites_attendues" (la probabilité que chaque époque soit gagnante pour une stratégie juste
      assez bonne pour passer ⑤), "methode" (une phrase)}.
      [rend: 1]
    ⑥ TRAITEMENT — ① contrôler les entrées · ② z = le point de la loi normale sous lequel tombe
      1 − seuil_de_preuve · ③ p_e = Φ(z × √part_e) pour chaque époque · ④ la loi du nombre d'époques
      gagnantes (somme de tirages à pile ou face de probabilités p_e : loi de Poisson-binomiale), par
      convolution · ⑤ minimum = le plus grand m tel que P(nombre < m) ≤ seuil_epoque.
    ⑦ UNITÉ — Le minimum est un NOMBRE D'ÉPOQUES ; les parts et les probabilités sont sans unité.
    ⑧ POURQUOI — La propriété (n°58 : « la part de périodes gagnantes n'est pas nettement plus basse
      qu'attendu ») : une stratégie dont l'avantage est le même dans chaque époque, et qui passe ⑤,
      n'est refusée par ce minimum qu'au plus seuil_epoque fois (5 fois sur 100). La stratégie la plus
      faible qui passe ⑤ a un gain moyen μ* = z × σ ÷ √N ; dans une époque de n_e = part_e × N
      observations, son gain moyen est positif avec la probabilité Φ(μ* √n_e ÷ σ) = Φ(z √part_e) :
      σ et N s'annulent, AUCUN GAIN N'ENTRE. Toute stratégie homogène plus forte a des p_e plus grands,
      donc la propriété tient pour elle aussi. Le minimum dépend de k, du nombre d'époques et de leurs
      séances : ce n'est jamais un chiffre fixe (décision de Jean-Luc du 01-11-2026 à 12h28, « 3 »,
      n°80 : « Un seuil calculé par programme, à partir des propres chiffres de C5 »). Étalonnage
      (superviseur R-759 du 05-11-2026, lot S_per, §2) : 4 époques 8/5/7/4 ans, k = 69 → 3 ; refus des
      stratégies homogènes qui passent ⑤ : 0,0 à 0,2 % ; un minimum fixé à 4, ou calculé sur les
      années de réglage, en refuse 7,6 à 8,0 %. « Nettement » est lu au seuil `epoque_perdante` de la
      table, faute d'une clé propre (lecture du Chat, consignée au BACKLOG).
    ⑨ CE QUI CLOCHE — ① Ce minimum ne protège pas seul contre une stratégie sans avantage : même
      « toutes les époques gagnantes » laisse passer 1 ÷ 2^E des stratégies nulles (6,25 % pour 4
      époques) ; c'est ⑤ qui donne cette protection (⑤ et ⑦ ensemble : 0,06 %, superviseur §2).
      ② Une stratégie qui ne gagne que dans une époque sur quatre et passe ⑤ n'est refusée par ⑦
      qu'une fois sur trois environ (33,6 %, superviseur §2) : les régimes de marché, que n°197 confie
      à ⑦, ne sont couverts qu'en partie. ③ Le calcul suppose que la part d'observations retenues d'une
      époque suit sa part de séances ; mesuré dans le monde simulé du superviseur, un écart d'un facteur
      trois sur une époque ne change pas le minimum (0,2 % de refus) ; non éprouvé au-delà.
      ④ La loi normale remplace celle de Student pour z : N n'est pas connu avant le regard.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève `ValueError`. Boucles bornées par le nombre d'époques.
      Aucun de ses appels ne peut ne pas revenir : `math` et `statistics.NormalDist` seulement.
      [sort: non]
    """
    import math
    import statistics
    parts = list(parts_des_seances)
    if not parts:
        raise ValueError("aucune part de séances : aucune époque")
    for i, p in enumerate(parts):
        if isinstance(p, bool) or not isinstance(p, (int, float)) or not math.isfinite(p) or not 0 < p <= 1:
            raise ValueError("part n°%d = %r : hors de ]0, 1]" % (i, p))
    if not math.isclose(math.fsum(parts), 1):
        raise ValueError("les parts de séances font %r, pas 1" % (math.fsum(parts),))
    for nom, s in (("seuil_de_preuve", seuil_de_preuve), ("seuil_epoque", seuil_epoque)):
        if isinstance(s, bool) or not isinstance(s, (int, float)) or not 0 < s < 1:
            raise ValueError("%s = %r : hors de ]0, 1[" % (nom, s))
    loi = statistics.NormalDist()
    z = loi.inv_cdf(1 - seuil_de_preuve)
    probabilites = [loi.cdf(z * math.sqrt(p)) for p in parts]
    loi_du_nombre = [1.0]
    for p in probabilites:
        suivante = [0.0] * (len(loi_du_nombre) + 1)
        for j, q in enumerate(loi_du_nombre):
            suivante[j] += q * (1 - p)
            suivante[j + 1] += q * p
        loi_du_nombre = suivante
    minimum, sous_m = 0, 0.0
    for m in range(1, len(parts) + 1):
        sous_m += loi_du_nombre[m - 1]
        if sous_m > seuil_epoque:
            break
        minimum = m
    return {"minimum": minimum, "probabilites_attendues": probabilites,
            "methode": ("plus grand m tel que P(epoques gagnantes < m) <= seuil_epoque pour une strategie "
                        "d'avantage egal partout, juste assez bonne pour passer le gain moyen au seuil de "
                        "preuve : p_e = Phi(z(1 - seuil_de_preuve) x racine(part de seances de l'epoque)), "
                        "loi de Poisson-binomiale ; aucun gain n'entre (superviseur R-759, lot S_per, methode C)")}


def controle_des_epoques(ops, epoques, parts_des_seances, seuil_de_preuve, seuil_epoque):
    """Juge R-505 ⑦ : aucune époque perdante à coup sûr, et assez d'époques gagnantes.

    ① RÔLE — Rendre le contrôle ⑦ du verdict : répartir les opérations dans les époques déclarées,
      dire pour chacune si elle est gagnante et si elle est perdante à coup sûr, et comparer le nombre
      d'époques gagnantes au minimum calculé avant le regard.
    ② CONTEXTE D'APPEL — Le juge de la loi (lot JG, À VENIR), une fois par verdict, avec les époques
      et les parts rendues par `lire_les_epoques` et les deux seuils lus dans la table de R-505.
      Relevé le 05-11-2026 : seule l'épreuve `tests/EPREUVES_DES_EPOQUES_Jeu_05-11-2026.py` l'appelle.
      Elle ne reçoit pas le groupe témoin : le témoin informe, il ne décide pas (n°79).
    ③ ENTRÉE — `ops` : les opérations, des dictionnaires dont sont lues `date_entree`, `date_sortie`
      et `net` (gain net en euros), comme `observations_independantes` · `epoques` : la liste
      {"debut", "fin", …} de `lire_les_epoques` (ou `None`) · `parts_des_seances` : la liste de même
      longueur · `seuil_de_preuve` : 0,05 ÷ k · `seuil_epoque` : la clé `epoque_perdante`.
      AUCUN ARGUMENT N'A DE VALEUR PAR DÉFAUT.
    ④ CONDITIONS D'ENTRÉE — `parts_des_seances` de même longueur que `epoques`, sinon `ValueError` ;
      les conditions de `minimum_d_epoques_gagnantes` ; `net` comme `observations_independantes`.
    ⑤ SORTIE — UNE valeur : un dictionnaire au contrat CONTROLE_DU_VERDICT : `etat` (PASSE, BLOQUE ou
      INCONNU), `valeur` (le nombre d'époques gagnantes, ou `None`), `seuil` (le minimum, ou `None`),
      `raison`, `role` (« CONDITION »), `detail` ({} ou {"epoques", "epoques_gagnantes",
      "minimum_d_epoques_gagnantes", "parts_des_seances"} ; chaque époque porte EPOQUE_DU_VERDICT et
      `observations_retenues`). Un défaut de la déclaration rend INCONNU avec une raison qui commence
      par « NON JUGEABLE — epoques : ».
      [rend: 1]
    ⑥ TRAITEMENT — ① aucune époque reçue → INCONNU, « NON JUGEABLE — epoques » · ② calculer le
      minimum (`minimum_d_epoques_gagnantes`, sans aucun gain) · ③ ranger les opérations par
      `date_entree` et placer chacune dans l'époque qui contient sa date d'entrée ; une date illisible
      ou hors de toute époque → INCONNU, « NON JUGEABLE — epoques », qui nomme l'opération · ④ pour
      chaque époque : nombre d'opérations, gain moyen, observations retenues
      (`observations_independantes(ops_de_l_epoque)["n_observations"]`), p perdante
      (`probabilite_epoque_perdante`) ; gagnante si le gain moyen est > 0 ; perdante à coup sûr si
      p < seuil_epoque ; une époque sans opération n'est ni gagnante ni perdante et compte dans le
      total · ⑤ BLOQUE si une époque est perdante à coup sûr ou si les gagnantes sont moins que le
      minimum ; sinon INCONNU si une époque n'a pas pu être mesurée (nommée) ; sinon PASSE.
    ⑦ UNITÉ — Gains en EUROS ; époques et minimum en NOMBRE D'ÉPOQUES ; observations en nombre
      d'observations ; p probabilité ; dates AAAA-MM-JJ.
    ⑧ POURQUOI — R-505 ⑦ : « Exiger qu'aucune époque fixée d'avance ne soit perdante à coup sûr (seuil
      de 5 %), et que le nombre d'époques gagnantes atteigne un minimum calculé par programme »
      (n°58, n°80). Une opération appartient à l'époque de son ACHAT : son gain est décidé par le
      signal de ce jour-là. Une opération hors de toute époque prouve que le découpage déclaré ne
      couvre pas ce qui est jugé : l'écarter en silence changerait le résultat sans le dire. Un
      contrôle qui n'a pas pu se mesurer ne rend jamais PASSE (R-734). BLOQUE passe avant INCONNU
      quand le refus est déjà certain avec les époques mesurées : ce qui manque ne peut pas le lever.
    ⑨ CE QUI CLOCHE — ① Quatre tests « perdante » au seuil de 5 % chacun, sans correction : une
      stratégie nulle est refusée environ 18 fois sur 100 (1 − 0,95⁴) par cette moitié ; la loi dit
      « seuil de 5 % » par époque, appliqué tel quel (BACKLOG). ② « NON JUGEABLE » n'est pas un état
      d'un contrôle au contrat (ETATS_D_UN_CONTROLE) : il voyage dans la raison d'un INCONNU, que le
      juge de la loi devra lire (fragment remis au lot C). ③ Une époque d'une seule opération rend
      tout le contrôle INCONNU, sauf refus déjà certain.
    ⑩ EFFET — Aucun : elle lit, n'écrit rien, n'affiche rien.
    ⑪ TERMINAISON — Rend la main, ou lève `ValueError` (entrées hors conditions) ou laisse remonter
      celles de ses appels. Boucles bornées par le nombre d'opérations et d'époques. Aucun de ses
      appels ne peut ne pas revenir : `observations_independantes` et `loi_de_student_inferieure` sont
      bornées.
      [sort: non]
    """
    import datetime
    import math
    rendu = {"etat": "INCONNU", "valeur": None, "seuil": None, "raison": "", "role": "CONDITION", "detail": {}}
    if not epoques:
        rendu["raison"] = ("NON JUGEABLE — epoques : aucune époque reçue (la déclaration n'en porte pas, ou "
                           "lire_les_epoques l'a refusée) ; aucun découpage n'est choisi ici")
        return rendu
    parts = list(parts_des_seances)
    if len(parts) != len(epoques):
        raise ValueError("%d parts de séances pour %d époques" % (len(parts), len(epoques)))
    minimum = minimum_d_epoques_gagnantes(parts, seuil_de_preuve, seuil_epoque)["minimum"]
    rendu["seuil"] = minimum
    rangees, illisibles = [], []
    for i, o in enumerate(ops):
        d = o.get("date_entree")
        try:
            if not isinstance(d, str) or datetime.date.fromisoformat(d).isoformat() != d:
                raise ValueError(d)
            rangees.append((d, i, o))
        except ValueError:
            illisibles.append("operation n°%d (%s) : date_entree %r illisible" % (i, o.get("valeur", "?"), d))
    if illisibles:
        rendu["raison"] = "NON JUGEABLE — epoques : " + " ; ".join(illisibles)
        return rendu
    rangees.sort()
    groupes = [[] for _ in epoques]
    hors = []
    for d, i, o in rangees:
        place = [e for e, ep in enumerate(epoques) if ep["debut"] <= d <= ep["fin"]]
        if not place:
            hors.append("operation n°%d (%s, achat %s)" % (i, o.get("valeur", "?"), d))
            continue
        groupes[place[0]].append(o)
    if hors:
        rendu["raison"] = ("NON JUGEABLE — epoques : %d opération(s) hors de toute époque déclarée : %s"
                           % (len(hors), " ; ".join(hors)))
        return rendu
    lignes, inconnues, perdantes = [], [], []
    for ep, ops_e in zip(epoques, groupes):
        nom = "%s..%s" % (ep["debut"], ep["fin"])
        ligne = {"debut": ep["debut"], "fin": ep["fin"], "n_operations": len(ops_e), "gain_moyen_eur": None,
                 "p_perdante": None, "gagnante": False, "observations_retenues": 0}
        if ops_e:
            gains = [o["net"] for o in ops_e]
            mesure = observations_independantes(ops_e)
            n_retenu = mesure["n_observations"]
            ligne["observations_retenues"] = n_retenu
            ligne["gain_moyen_eur"] = math.fsum(gains) / len(gains)
            ligne["gagnante"] = ligne["gain_moyen_eur"] > 0
            if n_retenu is None:
                inconnues.append("époque %s : observations INCONNUES (%s)" % (nom, mesure["motif"]))
            else:
                proba = probabilite_epoque_perdante(gains, n_retenu)
                if proba["motif"]:
                    inconnues.append("époque %s : %s" % (nom, proba["motif"]))
                else:
                    ligne["p_perdante"] = proba["p_perdante"]
                    if proba["p_perdante"] < seuil_epoque:
                        perdantes.append("époque %s perdante à coup sûr (p = %.4g < %s)"
                                         % (nom, proba["p_perdante"], seuil_epoque))
        lignes.append(ligne)
    gagnantes = sum(1 for ligne in lignes if ligne["gagnante"])
    rendu["valeur"] = gagnantes
    rendu["detail"] = {"epoques": lignes, "epoques_gagnantes": gagnantes, "minimum_d_epoques_gagnantes": minimum,
                       "parts_des_seances": parts}
    raisons = list(perdantes)
    if gagnantes < minimum:
        raisons.append("%d époque(s) gagnante(s) sur %d, minimum calculé %d" % (gagnantes, len(lignes), minimum))
    if raisons:
        rendu["etat"] = "BLOQUE"
        rendu["raison"] = " ; ".join(raisons + (["non mesurées : " + " ; ".join(inconnues)] if inconnues else []))
    elif inconnues:
        rendu["etat"] = "INCONNU"
        rendu["raison"] = "MESURE MANQUANTE — " + " ; ".join(inconnues)
    else:
        rendu["etat"] = "PASSE"
    return rendu


def afficher_le_groupe_temoin(ops_strategie, ops_temoin, epoques):
    """Montre, sans rien décider, la stratégie à côté de son groupe témoin, sur le tout et par époque.

    ① RÔLE — Porter l'affichage de R-505 ⑪ : « le même signal, mêmes réglages, sur TOUTES les actions
      du CAC 40 à chaque date » (n°57), mis à côté de la stratégie, pour que Jean-Luc voie si l'avantage
      vient du choix des valeurs ou du moment. Le nom est « groupe témoin » : « TEMOIN » désigne déjà
      dans le juge le jeu de données du golden.
    ② CONTEXTE D'APPEL — Le juge de la loi (lot JG, À VENIR), après `controle_des_epoques`, avec les
      opérations du groupe témoin s'il a pu être joué. Relevé le 05-11-2026 : seule l'épreuve
      `tests/EPREUVES_DES_EPOQUES_Jeu_05-11-2026.py` l'appelle.
    ③ ENTRÉE — `ops_strategie`, `ops_temoin` : des opérations (`date_entree`, `net` lus) ; `ops_temoin`
      vaut `None` quand le groupe témoin n'a pas pu être joué · `epoques` : la liste de
      `lire_les_epoques`, ou `None` (seul le tout est montré).
    ④ CONDITIONS D'ENTRÉE — `net` est un nombre fini, sinon `ValueError`.
    ⑤ SORTIE — UNE valeur : un dictionnaire au contrat CONTROLE_DU_VERDICT : `role` « AFFICHAGE » ;
      `etat` « PASSE » (montré) ou « INCONNU » (avec sa raison), JAMAIS « BLOQUE » ; `valeur` le gain
      moyen du groupe témoin en euros, ou `None` ; `seuil` `None` ; `detail` {"strategie",
      "groupe_temoin", "par_epoque"}, chaque résumé portant `n_operations`, `gain_moyen_eur`,
      `part_gagnante`.
      [rend: 1]
    ⑥ TRAITEMENT — ① témoin absent → INCONNU, raison « composition du CAC 40 à chaque date absente
      (I-8) » · ② résumer chaque groupe sur le tout · ③ si des époques sont données, résumer chaque
      groupe dans chaque époque (par date d'achat) · ④ rendre PASSE.
    ⑦ UNITÉ — Gains en EUROS ; parts gagnantes en fraction ; opérations en nombre.
    ⑧ POURQUOI — « le TÉMOIN INFORME, il ne fait pas échouer C5 » (décision de Jean-Luc du 01-11-2026 à
      12h27, « 2 », n°79). L'état ne dépend donc d'aucune comparaison : il dit seulement si le témoin a
      pu être montré. Le témoin compte dans k (n°57), ce que fait le compteur de k (lot S_kk), pas
      cette fonction.
    ⑨ CE QUI CLOCHE — ① La table « membres du CAC 40 à chaque date » (I-8) n'existe pas au 05-11-2026 :
      le groupe témoin ne peut pas être joué, cette fonction rend donc INCONNU sur données réelles.
      ② Le contrat porte déjà un affichage nommé `temoin` (AFFICHAGES_DU_VERDICT, forme AFFICHAGE_DU_VERDICT)
      ; ce rendu suit CONTROLE_DU_VERDICT avec le rôle AFFICHAGE, comme le demande la consigne du lot :
      le choix entre les deux formes revient au lot C (fragment).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève `ValueError`. Boucles bornées par le nombre d'opérations et
      d'époques. Aucun de ses appels ne peut ne pas revenir : `math` seulement.
      [sort: non]
    """
    import math
    rendu = {"etat": "INCONNU", "valeur": None, "seuil": None, "raison": "", "role": "AFFICHAGE", "detail": {}}
    if ops_temoin is None:
        rendu["raison"] = ("composition du CAC 40 à chaque date absente (I-8) : le groupe témoin n'est pas joué ; "
                           "il informe, il ne décide pas (n°79)")
        return rendu
    tranches = [("tout", None, None)]
    for ep in epoques or []:
        tranches.append(("%s..%s" % (ep["debut"], ep["fin"]), ep["debut"], ep["fin"]))
    resumes = {}
    for nom_groupe, ops in (("strategie", ops_strategie), ("groupe_temoin", ops_temoin)):
        for nom_tranche, debut, fin in tranches:
            gains = []
            for o in ops:
                g = o.get("net")
                if isinstance(g, bool) or not isinstance(g, (int, float)) or not math.isfinite(g):
                    raise ValueError("%s : gain %r, pas un nombre fini" % (nom_groupe, g))
                d = o.get("date_entree")
                if debut is None or (isinstance(d, str) and debut <= d <= fin):
                    gains.append(g)
            resumes[(nom_groupe, nom_tranche)] = {
                "n_operations": len(gains),
                "gain_moyen_eur": math.fsum(gains) / len(gains) if gains else None,
                "part_gagnante": sum(1 for g in gains if g > 0) / len(gains) if gains else None}
    rendu["detail"] = {"strategie": resumes[("strategie", "tout")],
                       "groupe_temoin": resumes[("groupe_temoin", "tout")],
                       "par_epoque": [{"epoque": nom, "strategie": resumes[("strategie", nom)],
                                       "groupe_temoin": resumes[("groupe_temoin", nom)]}
                                      for nom, _, _ in tranches[1:]]}
    rendu["valeur"] = resumes[("groupe_temoin", "tout")]["gain_moyen_eur"]
    rendu["etat"] = "PASSE"
    return rendu


# ─────────────────────────────────────────────────────────────────────
# LA BORNE BASSE DU GAIN MOYEN — par rééchantillonnage
# ─────────────────────────────────────────────────────────────────────

def borne_basse_gain(ops, n_tirages=2000, graine=GRAINE):
    """Rend l'intervalle du gain moyen par reechantillonnage.

    POURQUOI : un gain moyen de +940 EUR sur 89 operations ne dit rien tant
    qu'on ne sait pas s'il tiendrait sur un autre echantillon. La borne basse
    repond a : au pire, combien ?

    ① RÔLE — Dire ce que vaudrait le gain moyen d'une stratégie sur un autre
      tirage des mêmes opérations, et donc jusqu'où il peut descendre. Un gain
      moyen nu ne dit rien : il peut tenir à deux ou trois opérations
      exceptionnelles. La méthode consiste à retirer au hasard, avec remise,
      autant d'opérations qu'il y en a, deux mille fois, et à regarder comment
      se distribuent les deux mille moyennes obtenues.
    ② CONTEXTE D'APPEL — Un seul appelant : `programmes/JUGE_DES_STRATEGIES.py`, à la
      main, une fois par stratégie jugée, sans rien préciser d'autre que la
      liste des opérations. Aucun autre appel dans le dépôt — recherche dans
      tous les fichiers `.py` de `programmes/` le 19-09-2026, une seule ligne.
    ③ ENTRÉE — `ops` : la liste des opérations, dont seule la case `net` est
      lue · `n_tirages` : le nombre de rééchantillonnages, 2000 par défaut, et
      l'unique appelant laisse ce défaut · `graine` : le nombre qui fixe la
      suite de tirages, 20260828 par défaut, pour que deux passages sur les
      mêmes données rendent exactement le même résultat.
    ④ CONDITIONS D'ENTRÉE — Chaque opération doit porter une case `net`. Moins
      de 5 opérations rend un motif au lieu d'un calcul.
    ⑤ SORTIE — UNE valeur : un dictionnaire, et il prend DEUX formes
      différentes. En dessous de 5 opérations : trois cases, l'effectif, une
      borne basse à `None` et le motif « trop peu d'operations ». Sinon cinq
      cases : l'effectif, le gain moyen observé, la borne basse au cinquième
      centile, la borne haute au quatre-vingt-quinzième, et la graine employée.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre un motif en dessous de 5 opérations · ② relever les
      gains nets · ③ fixer la suite de tirages avec la graine · ④ deux mille
      fois, tirer autant de gains qu'il y en a, AVEC REMISE, et noter leur
      moyenne · ⑤ trier les deux mille moyennes · ⑥ rendre le gain moyen
      observé et les deux moyennes situées au vingtième et au dix-neuf
      vingtièmes de la liste triée.
    ⑦ UNITÉ — Les gains et les bornes sont en EUROS. `n_tirages` et l'effectif
      sont des NOMBRES. La graine n'a pas d'unité.
    ⑧ POURQUOI — Le tirage AVEC REMISE est ce qui fait le sens de la mesure :
      il fabrique des échantillons de même taille que l'original, dans lesquels
      une opération peut apparaître deux fois et une autre pas du tout. C'est
      ainsi qu'on voit ce que pèse chaque opération dans la moyenne.
      La graine est fixée et RENDUE dans le résultat pour que deux passages sur
      les mêmes données donnent exactement le même chiffre, et pour qu'un
      lecteur puisse refaire le calcul. Sans graine fixée, la borne basse
      bougerait d'un passage à l'autre et deux rapports du même jour
      différeraient sans raison.
    ⑨ CE QUI CLOCHE —
      ① Aucun contrôle de calibrage ne la couvre. Recherche du nom
      `borne_basse_gain` dans le corps de `_calibrage` le 19-09-2026 : absent.
      Les 23 contrôles du fichier passeraient toujours si le tirage était fait
      sans remise, ou si les deux centiles étaient échangés.
      ② Le seuil de 5 opérations et le nombre de 2000 tirages sont écrits dans
      la signature et nulle part ailleurs, sans source citée. Sur de très
      petites listes, 5 opérations suffisent à déclencher un calcul dont
      l'intervalle sera très large, et rien dans le résultat ne signale cette
      largeur autrement que par les deux bornes elles-mêmes.
      ③ Les deux centiles sont pris par leur position dans la liste triée, sans
      interpolation : la borne basse est la moyenne de rang 100 sur 2000. Avec
      un nombre de tirages plus petit, l'écart entre le centile demandé et le
      rang employé grandirait sans que le nom de la case change.
      ④ Le rééchantillonnage traite les opérations comme indépendantes, alors
      que la fonction `episodes` du même fichier existe précisément pour dire
      qu'elles ne le sont pas : cent opérations peuvent ne valoir que 33
      observations. La borne basse est donc plus étroite que la réalité, dans
      le sens qui flatte la stratégie. (05-11-2026 : `episodes` est remplacée
      par `observations_independantes`, qui rend `taille_des_groupes` ; le
      tirage par groupes de cette taille (n°107) n'est pas branché ici.)
    ⑩ EFFET — Aucun sur les données reçues : elle lit. Aucun fichier, aucun
      réseau, rien d'affiché. Elle construit deux mille échantillons en mémoire.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas dans les cas que son
      appelant lui donne. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le rééchantillonnage avec remise : le tirage, dans une liste, d'autant de
        valeurs qu'elle en compte, chaque valeur pouvant être tirée plusieurs
        fois ou pas du tout
      la borne basse : la valeur en dessous de laquelle ne tombe qu'un tirage
        sur vingt
      la graine : le nombre qui fixe la suite de tirages, pour qu'un calcul
        fondé sur le hasard donne toujours le même résultat
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
    
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
      un motif : un morceau de nom passé à une fonction de recherche, par exemple trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if len(ops) < 5:
        return {"n": len(ops), "borne_basse": None, "motif": "trop peu d'operations"}
    nets = [o["net"] for o in ops]
    r = random.Random(graine)
    moyennes = []
    for _ in range(n_tirages):
        ech = [nets[r.randrange(len(nets))] for _ in nets]
        moyennes.append(sum(ech) / len(ech))
    moyennes.sort()
    return {"n": len(ops),
            "gain_moyen": round(sum(nets) / len(nets), 2),
            "borne_basse_5pct": round(moyennes[int(0.05 * len(moyennes))], 2),
            "borne_haute_95pct": round(moyennes[int(0.95 * len(moyennes))], 2),
            "graine": graine}


# ─────────────────────────────────────────────────────────────────────
# L'ÉTALON DE HASARD — des entrées tirées au sort, au même rythme
# ─────────────────────────────────────────────────────────────────────

def etalon_hasard(ops, cours, univers, tp, sl, horizon, mod_positions,
                  mode="valeur", n_tirages=200, graine=GRAINE, entree=None, admis=None, periode=None):
    """Rejoue le MEME nombre d'operations au hasard, et rend la distribution.

    TROIS MODES, ET LA LITTERATURE DIT DE FAIRE LES TROIS :
      « date »   — on garde les VALEURS reelles, on tire les DATES au hasard.
                   Teste si le MOMENT comptait. C'est le « random-entry
                   gauntlet » : cent tirages a dates aleatoires, un vrai
                   avantage doit battre la distribution.
      « valeur » — on garde les DATES reelles, on tire la VALEUR au hasard.
                   Teste si la SELECTION comptait. « Le tirage Monte Carlo teste
                   si la selection comptait ; pour evaluer un signal, la
                   selection est le souci le plus pertinent. »
      « les_deux »— on tire les deux. C'est le test de Jaffray Woodriff :
                   « donnees aleatoires avec vrais signaux, signaux aleatoires
                   avec vraies donnees, une combinaison ou un melange des deux ;
                   l'objectif est d'obtenir de meilleurs resultats que la
                   MEILLEURE strategie aleatoire. »

    DEFAUT CORRIGE LE 28/08 : la premiere version ne faisait que le mode
    « date », en tirant sur TOUTE la periode. Elle comparait donc une strategie
    qui entre APRES UNE BAISSE a un tirage uniforme — deux choses differentes.

    PIEGE A CONNAITRE, ET IL TOUCHE DIRECTEMENT CETTE STRATEGIE : « si vous
    entrez au hasard avec un stop a 9 points et un objectif a 1 point, vous
    obtiendrez un taux de reussite de 90 %, et vous ne gagneriez pas d'argent ».
    Un objectif et un stop ASYMETRIQUES fabriquent mecaniquement un taux eleve.
    C'est pourquoi on rend AUSSI le gain, jamais le seul taux de reussite.
    Verification du 28/08 : le hasard rend 43 % la ou le point mort est a
    43,1 % — le hasard tombe exactement au point mort, comme la theorie le veut.

    ① RÔLE — Mesurer ce que vaut la stratégie PAR RAPPORT au hasard, en rejouant
      le même nombre d'opérations avec des entrées tirées au sort et les mêmes
      règles de sortie. Un gain ne vaut que par son écart au hasard : si des
      entrées aléatoires rendent autant, le signal n'apporte rien.
    ② CONTEXTE D'APPEL — Un seul appelant : `programmes/JUGE_DES_STRATEGIES.py`, à la
      main, DEUX fois par stratégie jugée, une fois en mode « valeur » et une
      fois en mode « date », avec 120 tirages chacune et l'univers déclaré par
      la fiche de la stratégie. Aucun autre appel dans le dépôt — recherche dans
      tous les fichiers `.py` de `programmes/` le 19-09-2026, une seule ligne.
      Depuis le 28-10-2026, ce juge lui passe aussi sa mécanique (`entree`), sa règle
      d'achat (`admis`) et la période de la fiche ; les épreuves de `tests/` l'appellent
      de même (frais du hasard, séance d'achat, étalon dans l'indice). DEUX ÉTUDES CLOSES
      l'appellent encore à l'ancienne, sans `entree` ni `admis` : `etudes/PLAN_REBOND_APRES_PIC_EXCEPTIONNEL_DE_BAISSE_
      Mer_28-10-2026/programmes/rebond.py` et `etudes/PLAN_REBOND_CHUTE_BRUTE_HORS_KRACH_Mer_28-10-2026/programmes/
      rebond_brut.py` ; elles s'arrêtent en le disant (ValueError), et se rejouent au commit de leur gel : 09e43c2 (et
      cec1b96) pour la première, 812e705 pour la seconde (superviseur R-759 du 29-10-2026 ; leurs GEL.md ne sont pas
      touchés, ils appartiennent à une autre conversation).
    ③ ENTRÉE — `ops` : les opérations réelles ; en mode « valeur », seule la case
      `date_signal` est lue, en mode « date », seule la case `valeur` ; leur NOMBRE fixe
      combien d'entrées seront tirées ·
      `cours` : l'historique, une liste de séances par valeur, chaque séance
      portant sa date, son ouverture, son plus haut, son plus bas et sa clôture ·
      `univers` : les valeurs dans lesquelles tirer · `tp` : l'objectif de gain
      en FRACTION · `sl` : la perte acceptée en FRACTION et en valeur positive ·
      `horizon` : le nombre de séances pendant lesquelles la position est tenue ·
      `mod_positions` : le module des positions, que le juge des stratégies passe
      (`programmes/MODULE_POSITIONS.py`) ; depuis le 28-10-2026 il n'est plus lu ici,
      la mécanique `entree` le porte · `mode` : « valeur » par
      défaut · `n_tirages` : 200 par défaut, et l'appelant passe 120 ·
      `graine` : 20260828 par défaut · `entree` : la mécanique de la
      stratégie, qui rend l'opération d'un achat à la séance `j` de la valeur `v`
      ou None (`JUGE_DES_STRATEGIES.jouer_une_entree`), appelée `entree(v, j)` · `admis` : sa règle
      d'achat, vrai si l'achat est permis (`JUGE_DES_STRATEGIES.achat_admis`) ·
      `periode` : le couple des bornes de la fiche, ou None. `mod_positions` n'est
      plus lu ici depuis le 28-10-2026 : la mécanique le porte.
      CONTRAT DU LOT 0 (09-11-2026) — `horizon` est un entier > 0, None (non
      fourni), ou `COMMUN.HORIZON_AUCUNE` (aucune durée maximale). Ce dernier
      refuse tout calcul par une TypeError. ICI le corps ne lit PAS `horizon`
      (vérifié le 09-11-2026) : la durée voyage dans `entree`, construite par le
      juge ; c'est elle (agent A) qui doit savoir traiter « aucune ».
    ④ CONDITIONS D'ENTRÉE — L'univers passé doit être celui de la FICHE et non
      celui du projet entier. Chaque valeur retenue doit porter plus de séances
      que l'horizon plus trois (exigence levée le 28-10-2026 : un achat sans assez
      de séances n'est plus écarté d'avance : comme dans `jouer`, un achat tombé sur la
      dernière séance sans seuil touché rend None et n'est pas joué, et un achat suivi de
      moins de h séances est vendu à la dernière clôture, motif HORIZON). `entree` et
      `admis` sont obligatoires : sans eux, ValueError. En mode « date », chaque
      opération doit porter sa case `valeur`.
    ⑤ SORTIE — UNE valeur : un dictionnaire, et il prend DEUX formes
      différentes. Quand l'univers ou les opérations sont insuffisants, ou
      qu'aucun tirage n'a pu être exploité : deux cases, un nombre de tirages à
      zéro et un motif en clair. Sinon, jusqu'au 28-10-2026, neuf cases : le mode, le nombre de
      tirages retenus, trois taux de réussite — médian, au quatre-vingt-quinzième
      centile, maximal — trois gains aux mêmes rangs, et la graine ; depuis le
      28-10-2026, douze cases : s'y ajoutent le nombre d'opérations réelles et le
      plus petit et le plus grand nombre d'opérations jouées par un tirage.
      [rend: 1]
    ⑥ TRAITEMENT (depuis le 28-10-2026) — ① refuser sans `entree` ni `admis` ·
      ② dresser les achats que la stratégie aurait pu faire : une séance d'achat
      `j` permise par `admis`, dont la veille — la séance du signal — tombe dans la
      période, rangés par date de signal et par valeur · ③ fixer la suite de
      tirages avec la graine · ④ répéter autant de fois que demandé : pour chaque
      opération réelle, tirer un achat — en mode « valeur », la date du signal
      réel est gardée et la valeur est tirée parmi les achats permis ce jour-là ;
      sinon, la valeur réelle est gardée et la date est tirée parmi ses achats
      permis dans la période · ⑤ le jouer par `entree`, la mécanique de la
      stratégie ; None = non joué, et compté · ⑥ cumuler le gain net, le nombre de
      gagnantes et le nombre joué · ⑦ trier les taux et les gains, rendre trois
      rangs de chacun. Jusqu'au 28-10-2026, l'étalon jouait avec sa propre copie de
      l'achat-sortie, tirait hors de l'indice et hors de la période, et le mode
      « date » tirait aussi la valeur.
    ⑦ UNITÉ — `tp` et `sl` sont des FRACTIONS. Les taux sont des POURCENTS entre
      0 et 100. Les gains sont en EUROS. L'horizon est un nombre de SÉANCES.
    ⑧ POURQUOI — On rend le GAIN et pas seulement le taux de réussite, parce
      qu'un objectif et un stop asymétriques fabriquent mécaniquement un taux
      élevé sans faire gagner d'argent : entrer au hasard avec un stop neuf fois
      plus large que l'objectif donne 90 % de réussite et aucun gain.
      L'univers passé est celui de la FICHE et non celui du projet, et l'écart
      est considérable. Défaut trouvé le 29-08-2026 : le juge des stratégies passait les 39
      valeurs du projet là où la fiche en déclare 9, et l'étalon rendait alors
      +2 963 € au lieu de +22 153 €. Le hasard paraissait sept fois et demie
      plus mauvais qu'il ne l'est, et le rapport concluait donc dans le sens
      flatteur. L'univers est le paramètre le plus puissant du système, avec
      61 % de réussite dedans contre 40,8 % dehors.
      Les sorties viennent du module des positions et jamais d'un calcul écrit
      ici, pour que l'étalon et la stratégie sortent selon les mêmes règles.
    ⑨ CE QUI CLOCHE —
      ① Le mode « les_deux » est annoncé dans ce texte et n'existe pas dans le
      code. Deux branches seulement sont écrites : « valeur », et tout le reste.
      Mesuré le 19-09-2026 sur un jeu fabriqué de trois valeurs et six
      opérations, graine 99 : le mode « date » rend un taux médian de 33,3 % et
      un gain médian de −3 800 €, le mode « les_deux » rend EXACTEMENT les
      mêmes deux valeurs, et le mode « valeur » rend 16,7 % et −10 300 €. Pire,
      la case `mode` du résultat renvoie « les_deux » : un appelant qui la lit
      croit avoir obtenu le troisième test alors qu'il a obtenu le deuxième.
      Aucun appelant d'aujourd'hui ne demande ce mode, le juge des stratégies n'appelant que
      « valeur » et « date ».
      ② RÉGLÉ LE 28-09-2026 (A-435 ④) : le gain net se calculait par
      `mod_positions.pnl_net` ; depuis le 28-10-2026, par la mécanique même de la stratégie
      (`jouer_une_entree`, frais par `MODULE_POSITIONS.frais_aller_retour`) ; épreuve dans
      tests/EPREUVES_DES_FRAIS_DU_HASARD_Lun_28-09-2026.py. Ce qui était mesuré :
      les frais sont un forfait de 300 € écrit dans ce fichier, alors que la
      stratégie à laquelle l'étalon sera comparé paie 0,15 % de la valeur
      échangée à l'entrée ET à la sortie. Mesuré le 19-09-2026 sur un
      aller-retour de 100,00 € à 104,00 € avec 100 000 € engagés :
      `MODULE_POSITIONS.pnl_net` rend 3 694,00 € quand la formule employée ici
      rend 3 700,00 €, soit 6,00 € d'écart sur ce gain ; sur une perte à −2,5 %
      l'écart s'inverse, −3,75 € (relecteur du Chat, 28-09-2026 : il vaut 1,50 € par
      point de pourcentage de rendement). Un chiffre qui existe ailleurs ne se recopie
      pas (R-708) : les frais vivent dans `MODULE_POSITIONS` (`frais_aller_retour`, qui lit le
      barème daté depuis le 29-10-2026, A-550).
      ③ Aucun contrôle d'unité sur l'objectif et la perte acceptée. Mesuré le
      19-09-2026 : un appel avec 4.0 et 2.5, c'est-à-dire des pourcents au lieu
      de fractions, est accepté sans broncher et rend un taux de réussite médian
      de 100,0 %, parce qu'un objectif de +400 % ne se touche jamais et que la
      sortie se fait alors à la clôture. La fonction `_exiger_des_fractions` du
      même fichier ferme ce contrat pour le point mort, pas ici.
      ④ EN PARTIE LE 28-10-2026 (le nombre joué par tirage est rendu ; le gain, lui, n'est toujours pas ramené à
      l'effectif joué : consigné au BACKLOG) — Des tirages sont abandonnés en silence. Une entrée tirée sur la dernière
      séance d'une valeur, ou une date sans aucun achat permis, n'est pas jouée ;
      depuis le 28-10-2026 le nombre joué par tirage est rendu et affiché, mais deux
      tirages qui auraient joué 6 et 3 opérations restent comparés sur leur gain total,
      et seul le taux de réussite est ramené à l'effectif, pas le gain.
      ⑤ Aucun contrôle de calibrage ne la couvre. Recherche du nom
      `etalon_hasard` dans le corps de `_calibrage` le 19-09-2026 : absent. La
      vérification citée dans ce texte — le hasard rend 43 % là où le point mort
      est à 43,1 % — n'est rejouable par rien.
    ⑩ EFFET — Aucun sur les données reçues : elle lit. Aucun fichier, aucun
      réseau, rien d'affiché. Elle EXÉCUTE `entree` une fois par opération et par
      tirage, et `admis` une fois par séance de l'univers dont la veille tombe dans la
      période. Elle construit en mémoire l'index des achats permis, par date de signal et
      par valeur.
    ⑪ TERMINAISON — Rend toujours la main dans les cas que son appelant lui
      donne. PEUT LEVER : ValueError sans `entree` ni `admis` ; et tout ce que lève
      `entree` (le module des positions sans `vendre` ou `frais_aller_retour`) ; le
      juge des stratégies rattrape et affiche « HASARD non mesure ». Ses appels à
      `entree` et `admis` rendent la main : ils ne lisent que la série reçue.
      [sort: non]
    ⑫ DÉFINITIONS
      l'étalon de hasard : le résultat qu'obtiendraient des entrées tirées au
        sort jouées aux mêmes règles, et auquel la stratégie doit être comparée
      l'univers : la liste des valeurs sur lesquelles une stratégie a le droit
        d'acheter, désignées par leur mnémonique
      la fiche : la ligne d'une stratégie au registre des stratégies `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte acceptée, son horizon et son univers
      le point mort : le taux de réussite en dessous duquel une stratégie perd
        de l'argent
      l'horizon : le nombre de séances pendant lesquelles une position est tenue
        si ni l'objectif de gain ni la perte acceptée ne sont atteints
      une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      la graine : le nombre qui fixe la suite de tirages, pour qu'un calcul
        fondé sur le hasard donne toujours le même résultat
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
    
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
      le signal : le jour où la stratégie dit d'acheter ; l'achat lui-même a lieu à l'ouverture de la séance suivante
      un motif : un morceau de nom passé à une fonction de recherche, par exemple trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
      un signal : le repérage, sur la dernière séance connue, d'une configuration de cours qui déclenche une simulation d'achat.
"""
    # DEPUIS LE 28-10-2026, L'ÉTALON NE JOUE PLUS LUI-MÊME : il tire au sort, et la mécanique d'achat-sortie est
    # celle de la stratégie, `JUGE_DES_STRATEGIES.jouer_une_entree`, que `juger` lui passe (R-708 ; superviseur
    # R-759 du 28-10-2026). Sans elle, il refuse plutôt que de garder une seconde mécanique.
    if entree is None or admis is None:
        raise ValueError("etalon_hasard : il faut la mécanique de la stratégie (entree) et sa règle d'achat (admis), "
                         "passées par le juge des stratégies — l'étalon ne recopie pas la mécanique (R-708). Une étude "
                         "close qui l'appelle encore à l'ancienne se rejoue au commit de son gel (09e43c2, 812e705 : "
                         "voir la fiche ② de cette fonction)")
    dispo = [v for v in univers if v in cours]
    if not dispo or not ops:
        return {"n_tirages": 0, "motif": "univers ou operations insuffisants"}
    # LES ACHATS QUE LA STRATÉGIE AURAIT PU FAIRE : une séance d'achat j permise (dans l'indice ce jour-là, quand la
    # lecture le demande), dont la veille — la séance du signal — tombe dans la période de la fiche, comme dans `jouer`.
    par_date, par_valeur = {}, {}
    for v in dispo:
        s = cours[v]
        for j in range(1, len(s)):
            d_sig = s[j - 1]["date"]
            if periode and not (periode[0] <= d_sig <= periode[1]):
                continue
            if not admis(v, j):
                continue
            par_date.setdefault(d_sig, []).append((v, j))
            par_valeur.setdefault(v, []).append(j)
    r = random.Random(graine)
    taux, gains, joues = [], [], []
    for _ in range(n_tirages):
        g = n = 0
        somme = 0.0
        for o in ops:
            if mode == "valeur":
                # mode « valeur » : la DATE réelle du signal est gardée, la VALEUR est tirée parmi les achats permis ce jour-là
                cands = par_date.get(o["date_signal"], [])
                if not cands:
                    continue
                v, j = cands[r.randrange(len(cands))]
            else:
                # mode « date » : la VALEUR réelle est gardée, la DATE est tirée parmi ses achats permis dans la période
                # (jusqu'au 28-10-2026, ce mode tirait aussi la valeur, contrairement à ce texte : superviseur R-759)
                v = o["valeur"]
                js = par_valeur.get(v, [])
                if not js:
                    continue
                j = js[r.randrange(len(js))]
            op = entree(v, j)
            if op is None:          # achat non permis, ou tombé sur la dernière séance sans seuil touché : non joué, et compté
                continue
            net = op["net"]
            n += 1
            g += 1 if net > 0 else 0
            somme += net
        if n:
            taux.append(100.0 * g / n)
            gains.append(somme)
            joues.append(n)
    if not taux:
        return {"n_tirages": 0, "motif": "aucun tirage exploitable"}
    taux.sort()
    gains.sort()
    return {"mode": mode, "n_tirages": len(taux),
            "taux_median": round(taux[len(taux) // 2], 1),
            "taux_95pct": round(taux[int(0.95 * len(taux))], 1),
            "taux_max": round(taux[-1], 1),
            "gain_median": round(gains[len(gains) // 2], 0),
            "gain_95pct": round(gains[int(0.95 * len(gains))], 0),
            "gain_max": round(gains[-1], 0),
            "graine": graine,
            "operations_reelles": len(ops),
            "jouees_par_tirage_min": min(joues), "jouees_par_tirage_max": max(joues)}


# ─────────────────────────────────────────────────────────────────────
# LA COURBE DE CAPITAL QUOTIDIENNE — et non par opération
# ─────────────────────────────────────────────────────────────────────

def courbe_quotidienne(ops):
    """Rend le gain cumule JOUR PAR JOUR, pas operation par operation.

    POURQUOI CETTE DISTINCTION EST EXIGEE PAR L'ETUDE 11 : la regularite du gain
    calculee sur les operations ignore les jours sans position. Une strategie qui
    gagne bien mais ne travaille qu'un jour sur dix parait bien plus reguliere
    qu'elle ne l'est.

    ① RÔLE — Mesurer la régularité d'une stratégie en comptant TOUS les jours,
      y compris ceux où elle ne fait rien. Calculée sur les seules opérations,
      la régularité ignore les jours sans position, et une stratégie qui ne
      travaille qu'un jour sur dix paraît bien plus régulière qu'elle ne l'est.
      La fonction reconstruit donc la suite des gains cumulés jour après jour,
      sans trou, du premier au dernier signal.
    ② CONTEXTE D'APPEL — AUCUN APPELANT. Recherche du nom `courbe_quotidienne`
      dans tous les fichiers `.py` de `programmes/` hors ce fichier, le
      19-09-2026 : zéro ligne. Elle n'est pas non plus dans `_calibrage`. Elle
      est écrite, elle n'est jamais exécutée, et le texte d'en-tête du fichier
      la compte pourtant parmi ce que le module apporte.
    ③ ENTRÉE — `ops` : la liste des opérations, dont les cases `date_signal` et
      `net` sont lues. Aucun autre paramètre.
    ④ CONDITIONS D'ENTRÉE — Chaque opération doit porter une date de signal
      écrite en année, mois puis jour séparés par des traits, faute de quoi la
      conversion en date tombe. Une liste vide est acceptée.
    ⑤ SORTIE — UNE valeur : un dictionnaire, et il prend DEUX formes
      différentes. Sur une liste vide, une seule case, un nombre de jours à
      zéro — mesuré le 19-09-2026. Sinon cinq cases : le nombre de jours, le
      gain final, le gain moyen par jour, une régularité, et la suite complète
      des gains cumulés. La régularité vaut `None` quand la suite ne varie pas.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre un nombre de jours à zéro si la liste est vide ·
      ② additionner les gains nets par date de signal · ③ prendre la première et
      la dernière de ces dates · ④ parcourir tous les jours de calendrier entre
      les deux, ajouter le gain du jour au cumul et noter le cumul · ⑤ calculer
      les variations d'un jour au suivant · ⑥ rendre le nombre de jours, le
      cumul final, la variation moyenne, et le rapport de cette moyenne à
      l'écart type des variations multiplié par la racine de 252.
    ⑦ UNITÉ — Les gains et la suite sont en EUROS. Le nombre de jours est un
      nombre de JOURS DE CALENDRIER, week-ends et jours fériés compris. La
      régularité n'a pas d'unité : c'est un rapport, ramené à l'année.
    ⑧ POURQUOI — Le parcours se fait jour après jour et non d'un signal au
      suivant, parce que c'est exactement ce que la mesure sert à corriger : un
      jour sans position est un jour à variation nulle, et il doit peser dans
      l'écart type. Sauter les jours vides reviendrait à ne mesurer que les
      jours travaillés, c'est-à-dire à refaire le calcul par opération que
      cette fonction remplace.
    ⑨ CE QUI CLOCHE —
      ① La mise à l'échelle annuelle emploie la racine de 252, qui est le nombre
      de SÉANCES de bourse dans une année, sur une suite qui compte des JOURS DE
      CALENDRIER. Mesuré le 19-09-2026 sur deux opérations, l'une au 05-01 et
      l'autre au 05-03 : la fonction rend 60 jours — ce qui est bien le nombre
      de jours de calendrier entre les deux dates, bornes comprises — et une
      régularité de 2,08. Avec la racine de 365, qui correspond à l'unité
      réellement employée, la même suite donnerait 2,50. Le chiffre rendu est
      donc 20 % trop bas, et son nom ne dit pas lequel des deux il est. Un
      chiffre ne s'emploie qu'avec ce qu'il mesure.
      ② Le gain entier d'une opération est porté au jour du SIGNAL, alors que la
      position est tenue jusqu'à l'horizon. Vérifié le 19-09-2026 : la seule
      case de date lue dans cette fonction est `date_signal`, et aucune case de
      date de sortie n'y apparaît. Une opération ouverte le 5 janvier et fermée
      le 2 février fait donc un saut de tout son gain au 5 janvier et rien
      ensuite. La suite rendue n'est pas la courbe de capital d'un compte : c'est
      la suite des gains rangés à la date d'entrée.
      ③ Aucun contrôle de calibrage ne la couvre, et personne ne l'appelle. Les
      deux faits se renforcent : un défaut introduit ici ne serait vu par rien.
      ④ La suite complète des gains cumulés est rendue avec le reste. Sur deux
      ans de données, cela fait environ 730 nombres dans un dictionnaire dont
      les autres cases en portent quatre. Un appelant qui afficherait le
      dictionnaire entier noierait les quatre mesures.
    ⑩ EFFET — Aucun sur les données reçues : elle lit. Aucun fichier, aucun
      réseau, rien d'affiché. Elle construit en mémoire une suite d'un nombre
      par jour de calendrier de la période.
    ⑪ TERMINAISON — Rend la main dans le cas normal. PEUT LEVER sur une date de
      signal mal formée, la conversion en date tombant alors, et l'erreur
      remonterait telle quelle à l'appelant — qui n'existe pas aujourd'hui.
      Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      la courbe de capital : la valeur qu'aurait eue le portefeuille à la fin de chaque séance de bourse, positions ouvertes comprises
      la régularité : le rapport du gain moyen à sa dispersion, ramené à
        l'année ; plus il est grand, moins le gain dépend de quelques jours
      une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
      le signal : le jour où la stratégie dit d'acheter ; l'achat lui-même a
        lieu à l'ouverture de la séance suivante
      l'horizon : le nombre de séances pendant lesquelles une position est tenue
        si ni l'objectif de gain ni la perte acceptée ne sont atteints
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      l'ÉTUDE 11 : l'étude datée du projet qui fixe la méthode de jugement des
        stratégies
    
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      un saut : l'ouverture d'une séance au-delà du seuil de sortie, de sorte que la sortie ne se fait pas au prix prévu mais au prix d'ouverture
      un signal : le repérage, sur la dernière séance connue, d'une configuration de cours qui déclenche une simulation d'achat.
      une stratégie : une règle qui dit QUOI acheter, avec son objectif de gain, sa perte acceptée et son horizon
"""
    if not ops:
        return {"n_jours": 0}
    par_jour = defaultdict(float)
    for o in ops:
        par_jour[o["date_signal"]] += o["net"]
    jours = sorted(par_jour)
    from datetime import date, timedelta
    d0 = date(*(int(x) for x in jours[0].split("-")))
    d1 = date(*(int(x) for x in jours[-1].split("-")))
    serie, cum = [], 0.0
    d = d0
    while d <= d1:
        cum += par_jour.get(d.isoformat(), 0.0)
        serie.append(cum)
        d += timedelta(days=1)
    var = [serie[i] - serie[i - 1] for i in range(1, len(serie))]
    ec = statistics.pstdev(var) if len(var) > 1 else 0.0
    moy = sum(var) / len(var) if var else 0.0
    return {"n_jours": len(serie),
            "gain_final": round(serie[-1], 2),
            "gain_moyen_par_jour": round(moy, 2),
            "regularite": round(moy / ec * (252 ** 0.5), 2) if ec else None,
            "serie": serie}


def plus_longue_serie_de_pertes(ops):
    """La plus longue suite d'operations perdantes, dans l'ordre du temps.

    ① RÔLE — Dire combien d'opérations perdantes se sont enchaînées sans
      interruption, au pire moment de la période. C'est le chiffre qui dit ce
      qu'il faudrait supporter pour tenir la stratégie : une stratégie gagnante
      sur deux ans peut avoir aligné huit pertes de suite, et personne ne le
      voit dans un gain total.
    ② CONTEXTE D'APPEL — Deux appelants. ① `programmes/JUGE_DES_STRATEGIES.py`, à la
      main, une fois par stratégie jugée, affiché sous l'intitulé « PIRE SERIE ».
      ② `_calibrage`, une fois, sur une suite fabriquée de sept opérations dont
      on sait que la plus longue série vaut 3.
    ③ ENTRÉE — `ops` : la liste des opérations, dont les cases `date_signal` et
      `net` sont lues. Aucun autre paramètre. Les deux appelants passent la
      liste entière.
    ④ CONDITIONS D'ENTRÉE — Chaque opération doit porter une date de signal et
      un gain net. Une liste vide est acceptée.
    ⑤ SORTIE — UNE valeur : un entier, le nombre d'opérations perdantes
      consécutives de la plus longue série. Zéro sur une liste vide, et zéro
      aussi si aucune opération n'est perdante.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre zéro si la liste est vide · ② ranger les opérations
      par date de signal croissante · ③ les parcourir en tenant deux compteurs,
      la série en cours et la plus longue vue · ④ allonger la série en cours à
      chaque gain net négatif ou nul, et la remettre à zéro dès qu'un gain est
      positif · ⑤ rendre la plus longue vue.
    ⑦ UNITÉ — Un NOMBRE D'OPÉRATIONS consécutives. Ni des jours, ni des séances.
    ⑧ POURQUOI — Le tri par date est indispensable et il est fait ici plutôt que
      laissé à l'appelant : la notion même de série n'a de sens que dans l'ordre
      du temps, et une liste d'opérations peut arriver dans n'importe quel
      ordre selon la façon dont elle a été construite.
      Une opération dont le gain net est exactement nul est comptée comme
      perdante, ce qui est le choix prudent : après frais, une opération qui ne
      rapporte rien a coûté quelque chose.
    ⑨ CE QUI CLOCHE —
      ① Le tri se fait sur la date d'ENTRÉE alors que les séries se vivent dans
      l'ordre des SORTIES. Deux opérations ouvertes le même jour, ou ouvertes
      dans un ordre et fermées dans l'autre, sont comptées dans l'ordre des
      entrées. Le système ne tient qu'une position à la fois par stratégie, donc
      le cas ne se produit pas aujourd'hui, mais rien dans cette fonction ne
      l'empêche.
      ② Deux opérations portant la même date de signal sont rangées dans un
      ordre que rien ne fixe. Le tri employé conserve l'ordre d'arrivée à
      égalité de date, ce qui rend le résultat dépendant de la façon dont la
      liste a été construite plutôt que des faits.
      ③ Le chiffre rendu ne dit ni QUAND la série a eu lieu, ni combien elle a
      coûté. Une série de huit pertes au tout début de la période et la même à
      la fin ne se distinguent pas, alors qu'elles ne veulent pas dire la même
      chose sur une stratégie qu'on envisage de faire vivre.
    ⑩ EFFET — Aucun : elle lit. Aucun fichier, aucun réseau, rien d'affiché.
      Elle construit une copie triée de la liste reçue, sans modifier
      l'originale.
    ⑪ TERMINAISON — Rend toujours la main. Elle lèverait sur une opération sans
      date de signal ou sans gain net, cas qu'aucun appelant ne produit. Aucun
      de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      une série de pertes : une suite d'opérations perdantes qui se succèdent
        sans qu'aucune gagnante vienne l'interrompre
      le signal : le jour où la stratégie dit d'acheter ; l'achat lui-même a
        lieu à l'ouverture de la séance suivante
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if not ops:
        return 0
    suite = max_suite = 0
    for o in sorted(ops, key=lambda x: x["date_signal"]):
        if o["net"] <= 0:
            suite += 1
            max_suite = max(max_suite, suite)
        else:
            suite = 0
    return max_suite


# ─────────────────────────────────────────────────────────────────────
# LE GLISSEMENT — mesurable depuis les motifs de sortie
# ─────────────────────────────────────────────────────────────────────

def glissement(ops):
    """Compte les sorties sur saut et ce qu'elles pesent.

    L'ETUDE 11 declarait cette mesure ABSENTE — « la sortie s'execute exactement
    au prix theorique, ce qui n'existe pas dans la vraie vie ». Elle devient
    gratuite depuis que les sorties viennent du module des positions, qui nomme
    les sauts (A-289, A-290).

    ① RÔLE — Dire quelle part des sorties ne s'est PAS faite au prix prévu,
      parce que le marché a ouvert au-delà du seuil. Une mesure qui suppose que
      la sortie s'exécute exactement au prix théorique décrit un monde qui
      n'existe pas. Le module des positions nomme déjà ces sorties : cette
      fonction les compte.
    ② CONTEXTE D'APPEL — Un seul appelant, `_calibrage`, une fois, sur trois
      opérations fabriquées dont on sait que deux sont des sauts. AUCUN APPELANT
      EN PRODUCTION : recherche du nom `glissement` dans tous les fichiers `.py`
      de `programmes/` hors ce fichier, le 19-09-2026, zéro ligne. Le juge des stratégies
      affiche bien un compte de sorties sur saut, mais il le calcule
      lui-même au lieu d'appeler cette fonction.
    ③ ENTRÉE — `ops` : la liste des opérations, dont seule la case `motif` est
      lue — le motif étant le nom que le module des positions donne à la sortie.
      Aucun autre paramètre.
    ④ CONDITIONS D'ENTRÉE — Aucune : une opération sans case `motif` est traitée
      comme n'ayant pas sauté, la lecture étant prudente. Une liste vide est
      acceptée.
    ⑤ SORTIE — UNE valeur : un dictionnaire, et il prend DEUX formes
      différentes. Sur une liste vide, une seule case, l'effectif à zéro —
      mesuré le 19-09-2026. Sinon cinq cases : le nombre d'opérations, le nombre
      de sorties sur saut, leur part en pourcents arrondie au dixième, et le
      détail des sauts à la hausse et à la baisse.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre l'effectif à zéro si la liste est vide · ② retenir
      les opérations dont le motif de sortie se termine par la marque de saut ·
      ③ séparer les sauts à la hausse des sauts à la baisse · ④ rendre les
      comptes et la part.
    ⑦ UNITÉ — Les effectifs sont des NOMBRES D'OPÉRATIONS. La part est un
      POURCENTAGE entre 0 et 100.
    ⑧ POURQUOI — La mesure est devenue possible sans effort le jour où les
      sorties ont cessé d'être calculées par chaque module de signal pour venir
      d'un seul endroit, le module des positions, qui nomme le cas où le marché
      ouvre au-delà du seuil. Ce déplacement est consigné au BACKLOG sous les
      actions A-289 et A-290 : deux mécaniques de sortie coexistaient, l'une
      sortait au prix théorique et l'autre au prix réellement disponible, et
      l'écart mesuré le 26-08-2026 valait 19 opérations sur 100 et plus de
      12 501 € sur un étalon, soit 11,2 %.
    ⑨ CE QUI CLOCHE —
      ① La fonction épelle des noms de motif au lieu de porter sur une
      propriété. Elle retient les motifs qui se terminent par la marque de saut,
      puis compare à deux noms écrits en toutes lettres pour trier hausse et
      baisse. Le critère qui tranche tient en une question : si je renomme un
      motif dans le module des positions, mon contrôle change-t-il d'avis ? Ici
      oui, et rien ici ne le signalerait — le compte tomberait simplement à
      zéro.
      ② Le titre annonce « et ce qu'elles pesent », et le poids n'est pas
      calculé. Aucune case rendue ne porte d'euros : la fonction rend des
      comptes et une part, jamais le coût des sauts. Le chiffre qui manque est
      précisément celui qui a justifié la mesure, les 12 501 € d'écart mesurés
      le 26-08-2026.
      ③ La forme courte du dictionnaire porte la case `n` quand la forme longue
      porte `n_operations`. Un appelant qui lirait `n_operations` sans
      précaution tomberait sur une liste vide.
      ④ Personne ne l'appelle, et le juge des stratégies calcule le même compte de son
      côté. Deux implémentations d'une même chose divergent toujours (R-708) :
      celle du juge des stratégies est affichée dans les rapports, celle-ci ne l'est jamais, et
      rien ne garantit qu'elles comptent la même chose.
    ⑩ EFFET — Aucun : elle lit. Aucun fichier, aucun réseau, rien d'affiché,
      aucune donnée modifiée.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas : la lecture du
      motif est prudente et retombe sur un texte vide. Aucun de ses appels ne
      se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      un saut : l'ouverture d'une séance au-delà du seuil de sortie, de sorte
        que la sortie ne se fait pas au prix prévu mais au prix d'ouverture
      le glissement : l'écart entre le prix de sortie prévu et le prix
        réellement obtenu
      le motif de sortie : le nom que le module des positions donne à la raison
        pour laquelle une position s'est fermée
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
      le BACKLOG : `BACKLOG_DECISIONS.md`, le tableau daté des décisions et des
        actions du projet, où chaque ligne porte un identifiant en `A-`
      l'ÉTUDE 11 : l'étude datée du projet qui fixe la méthode de jugement des
        stratégies
    
      PRODUCTION : l etat d une strategie dont le seuil d operations est atteint et les resultats conformes, donc exploitee.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if not ops:
        return {"n": 0}
    sauts = [o for o in ops if o.get("motif", "").endswith("_GAP")]
    h = [o for o in sauts if o["motif"] == "TP_GAP"]
    b = [o for o in sauts if o["motif"] == "SL_GAP"]
    return {"n_operations": len(ops), "n_sauts": len(sauts),
            "part_pct": round(100 * len(sauts) / len(ops), 1),
            "sauts_hausse": len(h), "sauts_baisse": len(b)}


# ─────────────────────────────────────────────────────────────────────
# CALIBRAGE — ce module se prouve lui-meme, comme le socle commun
# ─────────────────────────────────────────────────────────────────────

def _calibrage():
    """Reproduit des resultats DEJA CONNUS. Rend (ok, lignes).

    POURQUOI CE BLOC EXISTE : les docstrings de ce fichier annoncaient des
    calibrages — « 33 episodes retrouves exactement », « 43,08 % et 59,09 % au
    centieme » — mais AUCUN n'etait executable. Un calibrage qu'on ne peut pas
    rejouer n'est pas un calibrage, c'est une affirmation. Defaut releve le
    29/08 par relecture adverse, sur un fichier livre la meme nuit qu'un socle
    qui, lui, se prouvait.

    ① RÔLE — Rendre les affirmations du fichier REJOUABLES. Les textes de ce
      module annonçaient des résultats retrouvés au centième sans qu'aucune
      commande ne permette de le vérifier. Cette fonction refait ces calculs sur
      des données dont on connaît la réponse, et dit si chacun tombe juste.
      Mesuré le 19-09-2026 dans une copie du dépôt : 23 contrôles affichés, tous
      en OK, code de sortie 0.
    ② CONTEXTE D'APPEL — Un seul appelant : le lancement du programme en ligne
      de commande, une fois. Elle n'est jamais appelée par un autre programme —
      recherche dans tous les fichiers `.py` de `programmes/` le 19-09-2026,
      zéro ligne hors de ce fichier.
    ③ ENTRÉE — Aucun paramètre. Toutes les données de contrôle sont fabriquées
      dans son corps : deux calendriers de 300 et 90 séances, un de 120, des
      listes d'opérations construites pour donner un résultat connu, et un faux
      module de positions qui applique un taux de frais de 0,15 %.
    ④ CONDITIONS D'ENTRÉE — Aucune. Elle ne lit ni fichier ni réglage, et ne
      dépend d'aucune donnée réelle : elle tourne à l'identique sur un dépôt
      vide.
    ⑤ SORTIE — DEUX valeurs (2) dans le cas normal, UNE seule (1) quand un contrôle
      s'arrête tôt : d'abord un booléen, vrai si tous les contrôles
      sont passés ; ensuite la liste des lignes à afficher, une par contrôle,
      chacune portant son intitulé et la mention OK ou ECHEC, et pour un échec
      la valeur obtenue et celle attendue.
      [rend: 2]
    ⑥ TRAITEMENT — ① préparer une fonction interne qui compare une valeur
      obtenue à une valeur attendue, avec une tolérance, et compose la ligne ·
      ② vérifier les deux points morts documentés de l'ÉTUDE 11 · ③ vérifier le
      calcul des frais à deux branches contre un faux module, et que les deux
      branches diffèrent bien · ④ vérifier le découpage en trois fenêtres et sa
      couverture du calendrier · ⑤ vérifier qu'une fenêtre sous son point mort
      est dénoncée, et qu'une fenêtre au-dessus tient · ⑥ vérifier que la fin
      affichée d'une fenêtre est la séance exacte une fois la zone retirée
      déduite, et qu'elle diffère de la fin du découpage · ⑦ vérifier que les
      opérations écartées par cette zone sont comptées et ne valent pas zéro ·
      ⑧ vérifier que le résumé rend bien le taux exact et non l'arrondi ·
      ⑨ vérifier les deux bornes de Wilson, et que le même taux sur deux tailles
      d'échantillon donne deux verdicts opposés · ⑩ vérifier que la zone retirée
      ne peut pas être plus courte que l'horizon, et qu'elle a un plancher de
      21 séances · ⑪ vérifier la plus longue série de pertes et le comptage des
      sorties sur saut · ⑫ rendre le verdict et les lignes.
    le résumé : le fichier `registre_experiences_resume.csv`, une ligne par balayage — une série d'essais faits d'un coup sur une même stratégie
    une fenêtre : un morceau de la période, jugé séparément des autres
    ⑦ UNITÉ — Les tolérances sont dans l'unité de ce qui est comparé : au
      centième de POURCENT pour les points morts, au dixième pour les bornes de
      Wilson, au dix-millième pour le taux exact, exacte pour les comptes.
    ⑧ POURQUOI — Un contrôle s'écrit sur ce qu'on vient de CHANGER, pas sur ce
      qu'on vient de voir, et ce fichier porte quatre traces de cette règle
      apprise en une journée. Les deux premiers contrôles de point mort
      appellent la branche de repli aux frais forfaitaires : ils ne touchent
      jamais le calcul à deux branches ajouté le 29-08-2026, et le sabotage fait
      le jour même — remettre les frais du gain sur les deux branches — les
      laissait passer. Le contrôle du verdict par point mort a été ajouté pour
      la même raison : les seize autres appelaient la fonction SANS point mort,
      donc le chemin neuf n'était jamais parcouru.
      Le contrôle de la zone retirée comparait au départ deux nombres écrits en
      dur, 30 et 30, sans lire ce que la fonction rend : le sabotage du
      29-08-2026, qui remettait une largeur de 1 en dur, le laissait passer
      toujours. Un témoin qui ne peut pas tomber ne garde rien.
      Et le contrôle de la fin affichée vérifie LA SÉANCE EXACTE et pas seulement
      qu'elle diffère de la fin du découpage, parce qu'un décalage d'une séance
      passerait autrement.
    ⑨ CE QUI CLOCHE —
      ① Six des quinze fonctions du fichier ne sont couvertes par aucun
      contrôle. Recherche de chaque nom dans le corps de cette fonction le
      19-09-2026 : `episodes`, `borne_basse_gain`, `etalon_hasard`,
      `courbe_quotidienne`, `_exiger_des_fractions` et `_impossible` sont
      absents, `point_mort` aussi. Les deux dernières sont les gardes d'unité
      ajoutées le 13-09-2026 : rien ne prouve qu'elles lèvent encore.
      ② Le texte de cette fonction cite « 33 episodes retrouves exactement »
      comme exemple de ce qu'elle a rendu rejouable, et ce calibrage-là est
      justement celui qui ne l'est pas. Un lecteur qui lit ce texte croit que le
      défaut a été fermé partout. (05-11-2026 : `episodes` est retirée, n°106 ;
      voir le ⑨③ de l'en-tête du fichier.)
      ③ Les contrôles sont écrits en dur dans le corps de la fonction, dont les
      trois calendriers fabriqués qui attribuent 28 jours à chaque mois. Ces
      dates ne sont pas de vraies séances de bourse : elles suffisent pour
      vérifier un découpage, elles ne vérifient rien de ce qui dépend du
      calendrier réel.
      ④ La fonction interne de comparaison exige une soustraction entre la
      valeur obtenue et la valeur attendue. Un contrôle qui compare deux valeurs
      non numériques doit donc se ramener à un booléen, ce que font six des
      contrôles écrits ici ; sur un booléen, la tolérance n'a plus de sens et
      vaut zéro par défaut, ce que rien ne dit.
    ⑩ EFFET — N'écrit aucun fichier, ne touche pas au réseau, et n'affiche rien
      elle-même : elle rend des lignes que son appelant affiche. Elle EXÉCUTE
      cinq fonctions du fichier sur des données fabriquées.
    ⑪ TERMINAISON — Rend toujours la main dans l'état d'aujourd'hui. PEUT NE PAS
      REVENIR si une fonction contrôlée se met à lever : `point_mort_en_fractions`
      lève sur un seuil qui n'est pas une fraction, et l'erreur remonterait
      jusqu'au lancement du programme, qui s'arrêterait sans afficher le verdict.
      Aucun rattrapage n'est posé ici.
      [sort: non]
    ⑫ DÉFINITIONS
      un calibrage : la vérification qu'un programme retrouve un résultat déjà
        connu ; s'il ne le retrouve plus, on n'utilise pas ce qu'il produit
      un sabotage : le retrait, dans une copie du socle, de la ligne de correction qu'une épreuve donnée est censée surveiller.
      le point mort : le taux de réussite en dessous duquel une stratégie perd
        de l'argent
      la borne basse de Wilson : le taux de réussite le plus défavorable qui
        reste compatible avec ce qui a été observé
      l'embargo : l'élargissement de l'écart entre les deux parties, ici la zone de séances retirée des comptes
      une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
      l'horizon : le nombre de séances pendant lesquelles une position est tenue
        si ni l'objectif de gain ni la perte acceptée ne sont atteints
      l'ÉTUDE 11 : l'étude datée du projet qui fixe la méthode de jugement des
        stratégies
      le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté ailleurs.
    """
    L, ok = [], True

    def dire(lib, obtenu, attendu, tol=0.0):
        """Compare un chiffre obtenu au chiffre attendu et enregistre le verdict.

        ① RÔLE — Porter un cas de calibrage : dire si une fonction du module rend encore
        ce qu'elle rendait quand le calibrage a été écrit. Sans elle, chaque cas devrait
        écrire sa propre comparaison, et la moindre différence de rédaction ferait
        diverger les verdicts.
        ② CONTEXTE D'APPEL — Définie dans `_calibrage` et appelée par elle seule, une
        fois par cas.
        ③ ENTRÉE — `lib` : le libellé du cas, affiché sur 52 caractères · `obtenu` : le
        chiffre que la fonction vient de rendre · `attendu` : le chiffre de référence,
        écrit dans le calibrage · `tol` : l'écart toléré, zéro par défaut, employé pour
        les calculs à virgule.
        ④ CONDITIONS D'ENTRÉE — `obtenu` et `attendu` doivent être des nombres : la
        soustraction est faite sans protection. La liste `L` et la variable `ok` doivent
        exister dans `_calibrage`.
        ⑤ SORTIE — Ne rend rien.
          [rend: rien]
        ⑥ TRAITEMENT — ① mesurer l'écart absolu entre l'obtenu et l'attendu · ② le
        comparer à la tolérance · ③ éteindre `ok` dès qu'un cas tombe, sans jamais le
        rallumer · ④ ajouter au compte rendu une ligne « OK » ou « ECHEC », et dans le
        second cas les deux chiffres.
        ⑦ UNITÉ — Celle de l'appelant : un pourcent, un euro ou un compte, selon le cas
        éprouvé. Elle ne la connaît pas et ne la vérifie pas.
        ⑧ POURQUOI — Le verdict d'ensemble est un ET : un seul cas tombé fait tomber le
        calibrage entier. Écrire `ok = ok and passe` plutôt que `ok = passe` est ce qui
        l'assure — sinon le dernier cas effacerait les précédents.
        ⑨ CE QUI CLOCHE — Elle ne connaît pas l'unité de ce qu'elle compare : une
        tolérance de 0,01 vaut un centime sur un euro et un point de pourcentage sur un
        taux. Un chiffre ne s'emploie qu'avec ce qu'il mesure, et ici il voyage sans son
        unité (R-708). Et un `obtenu` qui n'est pas un nombre lève une erreur de type
        plutôt que de faire tomber le cas. Relevé par lecture du code le 20-09-2026.
        ⑩ EFFET — AJOUTE une ligne à la liste `L` de `_calibrage` et modifie sa variable
        `ok`, toutes deux par effet de bord.
        ⑪ TERMINAISON — Rend la main, sauf si `obtenu` ou `attendu` n'est pas un nombre :
        la soustraction lève alors et l'erreur remonte à `_calibrage`. Aucun de ses
        appels ne se termine.
          [sort: non]
        """
        nonlocal ok
        passe = abs(obtenu - attendu) <= tol
        ok = ok and passe
        L.append(f"  {lib:<52} {'OK' if passe else 'ECHEC'}"
                 + ("" if passe else f"  obtenu {obtenu} attendu {attendu}"))

    # LE VRAI MODULE DES POSITIONS, A COTE DE CE FICHIER (A-550, 29-10-2026). Jusque-la, ce
    # calibrage employait un forfait de 300 € ecrit ici, et une fausse fonction de frais a
    # 0,0015 ecrite en dur : deux copies d'un tarif. Il rejoue desormais les chiffres
    # connus sous le bareme qui les a produits, nomme dans donnees/BAREME_FRAIS.csv.
    import importlib.util as _ilu, os as _os
    _sp = _ilu.spec_from_file_location(
        "_positions_du_calibrage", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "MODULE_POSITIONS.py"))
    _mp = _ilu.module_from_spec(_sp); _sp.loader.exec_module(_mp)
    # les deux points mort documentes dans l'ETUDE 11, sous le forfait historique de 300 €
    dire("point mort +4,0/-2,5 = 43,08 % (forfait historique)",
         round(point_mort_en_fractions(0.040, 0.025, _mp, "AIRBUS", "2026-07-27", "HIST_FORFAIT_300"), 2), 43.08, 0.01)
    dire("point mort +1,2/-1,0 = 59,09 % (forfait historique)",
         round(point_mort_en_fractions(0.012, 0.010, _mp, "AIRBUS", "2026-07-27", "HIST_FORFAIT_300"), 2), 59.09, 0.01)
    # ON ECRIT LE CONTROLE DE CE QU'ON VIENT DE CHANGER, PAS DE CE QU'ON VIENT DE VOIR.
    # Les deux controles ci-dessus passent par un forfait egal sur les deux branches : ils
    # ne touchent jamais la difference entre sortie au gain et sortie au stop (29/08 : en
    # remettant les frais du gain sur les deux branches, le calibrage passait TOUJOURS).
    _pm = point_mort_en_fractions(0.05, 0.02, _mp, "AIRBUS", "2026-07-27", "HIST_COURTAGE_SANS_TTF")
    dire("point mort a deux branches de frais = 32,86 %", round(_pm, 2), 32.86, 0.01)
    # une sortie au stop coute MOINS cher qu'une sortie au gain : si les deux
    # branches etaient confondues, le point mort remonterait a 32,96
    dire("les deux branches different bien", round(_pm, 2) != 32.96, True)
    # LA TAXE (A-550) : +4 % / -2,5 % sur une valeur taxee en 2026, bareme reel — 49,25 %
    # (ETUDE 18, S3, calcul du 08-10-2026 aux frais exacts de chaque issue) ; sur Airbus,
    # non taxee, le courtage seul : 43,08 % (100 x 2 796,25 / 6 490,25 ; recalcule le 29-10-2026,
    # le texte disait 43,25 %).
    dire("point mort +4,0/-2,5 = 49,25 % sur une valeur taxee (bareme reel)",
         round(point_mort_en_fractions(0.040, 0.025, _mp, "BUREAU_VERITAS", "2026-07-27"), 2), 49.25, 0.01)
    _pc, _qui = point_mort_pire_cas(0.040, 0.025, ["AIR", "BVI"], "2026-07-27", _mp)
    dire("le pire cas d'un univers retient la valeur taxee (BVI)", 1.0 if _qui == "BVI" else 0.0, 1.0)
    # LE POINT MORT DES OPERATIONS JOUEES (decision de Jean-Luc du 29-10-2026 a 21h28, « A ») :
    # la MOYENNE, et non le pire cas. A la main, +4 % / -2,5 %, bareme reel, 100 000 € :
    #   Airbus (non taxee) : achat 150, vente au gain 156, vente au stop 146,25
    #     100 x (2 500 + 150 + 146,25) / ((4 000 - 150 - 156) + (2 500 + 150 + 146,25)) = 43,0839 %
    #   Bureau Veritas (taxee 0,4 %) : achat 150 + 400 = 550
    #     100 x (2 500 + 550 + 146,25) / ((4 000 - 550 - 156) + (2 500 + 550 + 146,25)) = 49,2469 %
    #   moyenne des deux : (43,0839 + 49,2469) / 2 = 46,1654 % — le pire cas rendrait 49,25.
    dire("point mort des operations : moyenne AIR + BVI = 46,17 %",
         round(point_mort_des_operations(0.040, 0.025, [{"valeur": "AIR", "date_entree": "2026-07-27"},
                                                        {"valeur": "BVI", "date_entree": "2026-07-27"}], _mp), 2),
         46.17, 0.01)

    # LES FENETRES GLISSANTES DECOUPENT LE TEMPS EN PARTS EGALES.
    _cal2 = {f"2026-{1 + i // 28:02d}-{1 + i % 28:02d}" for i in range(300)}
    _ops2 = [{"date_signal": d, "net": 1.0} for d in sorted(_cal2)]
    _f = fenetres_glissantes(_ops2, _cal2, n=3, embargo=0)
    dire("trois fenetres rendues", _f["n_fenetres"], 3)
    dire("les trois couvrent tout le calendrier",
         sum(x["n"] for x in _f["fenetres"]), len(_cal2))

    # LE VERDICT DES FENETRES DOIT PORTER SUR LE POINT MORT, PAS SUR LE GAIN.
    # Sans ce temoin, la correction du 29/08 — celle qui a supprime la phrase
    # « les trois fenetres sont GAGNANTES » alors qu'une etait sous son point
    # mort — n'etait gardee par rien : les seize autres controles appelaient la
    # fonction SANS point mort, donc le chemin neuf n'etait jamais parcouru.
    # Quatrieme correction sans filet dans la meme journee.
    # On fabrique une fenetre dont on SAIT qu'elle est sous son point mort.
    _cal3 = {f"2026-{1 + i // 28:02d}-{1 + i % 28:02d}" for i in range(90)}
    _j3 = sorted(_cal3)
    _o3 = ([{"date_signal": d, "net": 1.0} for d in _j3[:12]]
           + [{"date_signal": d, "net": -1.0} for d in _j3[12:30]])
    _f3 = fenetres_glissantes(_o3, _cal3, n=1, embargo=0, point_mort_pct=90.0)
    dire("une fenetre sous son point mort est DENONCEE",
         _f3.get("n_sous_le_point_mort"), 1)
    dire("et le verdict d'ensemble ne dit pas qu'elles tiennent",
         _f3.get("toutes_tiennent"), False)
    _f4 = fenetres_glissantes(_o3, _cal3, n=1, embargo=0, point_mort_pct=1.0)
    dire("au-dessus du point mort, elle TIENT", _f4.get("toutes_tiennent"), True)
    # la fin affichee est celle REELLEMENT jugee, embargo deduit
    # IL FAUT AU MOINS DEUX FENETRES POUR QU'UN TROU D'EMBARGO EXISTE.
    # Avec une seule fenetre, l'embargo ne mord que sur la toute fin ; le
    # premier temoin ecrit ici comparait donc a zero et tombait a juste titre.
    # LES OPERATIONS DOIVENT COUVRIR TOUT LE CALENDRIER pour que l'embargo
    # morde : avec des operations groupees au debut, il ne retire rien et le
    # temoin comparait a zero.
    _o5 = [{"date_signal": d, "net": 1.0} for d in sorted(_cal3)]
    _f5 = fenetres_glissantes(_o5, _cal3, n=2, embargo=10, point_mort_pct=50.0)
    # le temoin verifie la BONNE seance, pas seulement qu'elle differe :
    # un decalage d'une seance passerait sinon.
    _cal5 = sorted(_cal3)
    _t2 = len(_cal5) // 2
    dire("la fin affichee est la seance exacte, embargo deduit",
         _f5["fenetres"][0]["fin"] == _cal5[_t2 - 10 - 1], True)
    dire("et elle differe bien de la fin du decoupage",
         _f5["fenetres"][0]["fin"] != _f5["fenetres"][0]["fin_decoupage"], True)
    # ce que l'embargo ecarte est COMPTE, jamais tu
    dire("les operations ecartees par l'embargo sont comptees",
         _f5["n_ecartees_embargo"], _f5["n_operations"] - _f5["n_dans_fenetres"])
    dire("et elles ne sont pas zero quand l'embargo mord",
         _f5["n_ecartees_embargo"] > 0, True)

    # _resume DOIT RENDRE LE TAUX EXACT, sinon la correction de l'arrondi est
    # inerte : c'est cette fonction, et non `resumer()` du juge des stratégies, qui alimente
    # `wilson_bas`. Temoin exige par Cowork le 29/08, sans quoi la correction
    # retombera — elle est deja tombee une fois.
    _r = _resume([{"net": 1.0}] * 12 + [{"net": -1.0}] * 9)
    dire("_resume rend wr_exact", "wr_exact" in _r, True)
    dire("_resume : wr_exact n'est PAS l'arrondi",
         round(_r.get("wr_exact", 0), 4), round(100 * 12 / 21, 4), 0.0001)

    # LA BORNE BASSE DE WILSON, sur les deux cas mesures le 29/08.
    # On passe le taux EXACT, jamais l'arrondi d'affichage : 7/12 vaut
    # 58,333... et non 58,3, et l'ecart deplace la borne d'un dixieme. Un
    # temoin nourri d'un arrondi mesure l'arrondi, pas le calcul.
    dire("Wilson 7 sur 12 = 32,0 %", round(wilson_bas(12, 100 * 7 / 12), 1), 32.0, 0.05)
    dire("Wilson 12 sur 21 = 36,5 %", round(wilson_bas(21, 100 * 12 / 21), 1), 36.5, 0.05)
    # et le cas qui fonde la mesure : le meme taux, deux tailles, deux verdicts
    dire("meme taux, 12 op -> SOUS le point mort de 32,86",
         wilson_bas(12, 100 * 7 / 12) < 32.86, True)
    dire("meme taux, 21 op -> AU-DESSUS",
         wilson_bas(21, 100 * 12 / 21) > 32.86, True)

    # L'EMBARGO NE PEUT PAS ETRE PLUS COURT QUE L'HORIZON.
    # La premiere version de ce controle comparait DEUX LITTERAUX — 30 et 30 —
    # sans jamais lire ce que la fonction rend. Preuve par sabotage le 29/08 :
    # en remettant embargo_seances=1 en dur, le calibrage passait TOUJOURS.
    # Un temoin qui ne peut pas tomber ne garde rien.
    _cal = {f"2026-0{1+i//28}-{1+i%28:02d}" for i in range(120)}
    _faux = [{"date_signal": d, "net": 1.0} for d in sorted(_cal)[:40]]
    _r = coupure_70_30(_faux, _cal, horizon=30)
    dire("embargo >= horizon (30 -> 30)", _r.get("embargo_seances"), 30)
    _r21 = coupure_70_30(_faux, _cal, horizon=5)
    dire("embargo plancher a 21 si horizon court", _r21.get("embargo_seances"), 21)

    # la plus longue serie de pertes
    faux = [{"date_signal": f"2026-01-{i:02d}", "net": n}
            for i, n in enumerate([1, -1, -1, -1, 1, -1, -1], start=1)]
    dire("plus longue serie de pertes = 3", plus_longue_serie_de_pertes(faux), 3)

    # le glissement compte les sorties sur saut
    g = glissement([{"motif": "TP"}, {"motif": "TP_GAP"}, {"motif": "SL_GAP"}])
    dire("glissement : 2 sauts sur 3", g["n_sauts"], 2)
    return ok, L


if __name__ == "__main__":
    import sys
    print("MODULE_JUGEMENT — calibrage\n")
    ok, lignes = _calibrage()
    for l in lignes:
        print(l)
    print("\n  " + ("CALIBRAGE OK." if ok
                    else "CALIBRAGE ECHOUE — ne rien construire dessus."))
    sys.exit(0 if ok else 1)


def point_mort(*a, **k):
    """L ANCIEN NOM REFUSE — Y1 de Cowork, 13-09-2026.

    Deux fonctions portaient ce nom, prenaient les deux memes arguments, et les
    attendaient dans des unites OPPOSEES. Cowork a reproduit ma quasi-faute du
    12-09 en les croisant : `JUGEMENT.point_mort(4.0, 2.5)` rend 38,51 %.
    **Plausible, silencieux, et faux — aucun controle de sortie ne l attrape.**
    La garde [0 ; 100] ne ferme que la moitie bruyante, celle qui rend 500 %.
    **SEUL LE NOM FERME LA MOITIE SILENCIEUSE.** On ne supprime pas l ancien nom
    sans bruit : il leve, et il dit ou aller.

    ① RÔLE — Empêcher qu'un appel écrit avec l'ancien nom continue de marcher en
      silence, et dire où aller. Le nom `point_mort` a désigné deux fonctions
      différentes dans le dépôt, qui prenaient les deux mêmes arguments dans des
      unités opposées. Supprimer purement et simplement l'ancien nom aurait fait
      tomber l'appelant sur un message de Python qui ne dit rien ; le garder
      comme piège nommé fait tomber l'appelant sur un message qui dit quelle
      fonction employer selon l'unité qu'il a en main.
    ② CONTEXTE D'APPEL — Aucun appelant, et c'est le but. Recherche du nom
      `point_mort(` dans tous les fichiers `.py` de `programmes/` le
      19-09-2026 : aucun appel de cette fonction, les deux appelants du calcul
      passant par `point_mort_en_fractions`. Elle est faite pour être appelée
      par erreur, par du code écrit avant le 13-09-2026.
    ③ ENTRÉE — `a` reçu comme `*a` : tous les arguments positionnels, quels qu'ils soient ·
      `**k` : tous les arguments nommés. Aucun n'est lu : la fonction accepte
      n'importe quel appel pour pouvoir le refuser plutôt que de laisser Python
      se plaindre d'un nombre d'arguments.
      `k`
④ CONDITIONS D'ENTRÉE — Aucune. Tout appel est accepté, et tout appel est
      refusé.
    ⑤ SORTIE — Ne rend rien : elle lève toujours, sans exception.
      [rend: rien]
    ⑥ TRAITEMENT — ① lever une erreur portant trois lignes : que ce nom n'existe
      plus parce que l'unité doit voyager avec le nom, que des seuils en
      fractions appellent `point_mort_en_fractions`, et que des seuils en
      pourcents appellent `point_mort_en_pourcents` de
      `programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un nom retiré sans bruit laisse le code qui l'employait tomber
      sur un message générique, à un endroit qui ne dit pas quoi faire. Un nom
      retiré AVEC bruit dit trois choses au même endroit : que le nom a disparu,
      pourquoi, et lequel employer selon ce qu'on a en main. Le danger qui a
      justifié ce retrait est mesuré : croisées, les deux fonctions homonymes
      rendaient 38,51 % au lieu de 43,08 %, un chiffre plausible qu'aucun
      contrôle de sortie n'attrape, parce que la garde sur l'intervalle 0 à 100
      ne ferme que la moitié bruyante.
    ⑨ CE QUI CLOCHE —
      ① Elle est définie APRÈS le bloc de lancement en ligne de commande, qui se
      termine par une sortie du programme. Vérifié le 19-09-2026 : à l'import,
      la fonction existe bien et lève comme prévu ; lancé en ligne de commande,
      le programme sort avant d'atteindre sa définition. Le piège ne vaut donc
      que pour le module importé. Aucun appelant n'est concerné aujourd'hui,
      mais un lecteur qui parcourt le fichier de haut en bas voit du code après
      la sortie du programme et ne sait pas s'il s'exécute.
      ② L'erreur levée est du type qui signale un attribut manquant, alors que
      l'attribut existe. Un appelant qui se protégerait en cherchant si le
      module porte ce nom le trouverait, et croirait pouvoir l'appeler.
      ③ Aucun contrôle de calibrage ne vérifie qu'elle lève encore. Recherche du
      nom `point_mort` dans le corps de `_calibrage` le 19-09-2026 : absent. Le
      jour où la levée serait remplacée par un calcul, les 23 contrôles
      passeraient toujours.
    ⑩ EFFET — Aucun : elle lève. Aucun fichier, aucun réseau, rien d'affiché,
      aucune donnée modifiée.
    ⑪ TERMINAISON — Elle ne rend jamais la main : elle lève systématiquement. Si
      l'appelant ne rattrape pas, le programme appelant s'arrête. Aucun de ses
      appels ne se termine, puisqu'elle n'en fait aucun.
      [sort: oui]
    ⑫ DÉFINITIONS
      le point mort : le taux de réussite en dessous duquel une stratégie perd
        de l'argent
      une fraction : la façon d'écrire un pourcentage entre 0 et 1 — 0,040 pour
        +4 % — par opposition au pourcent, qui écrirait 4.0
      Cowork : le relecteur du projet, qui clone le dépôt, casse le code et rend
        ses cassures par écrit
    """
    raise AttributeError(
        "point_mort() n existe plus : l unite doit voyager avec le nom.\n"
        "  · seuils en FRACTIONS (0.040, 0.025) -> point_mort_en_fractions()\n"
        "  · seuils en POURCENTS (4.0, 2.5)     -> "
        "MESURER_LA_PERFORMANCE.point_mort_en_pourcents()")
