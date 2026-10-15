#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Porte les neuf calculs qui disent si une stratégie vaut quelque chose, et la
table des seuils qui tranchent.

① RÔLE — Le reste du système sait EXÉCUTER une stratégie et vérifier qu'il
  calcule juste. Il ne sait pas dire si cette stratégie est bonne. Ce fichier
  est l'instrument qui le dit : neuf fonctions qui mesurent chacune un aspect
  d'une liste d'opérations passées — la chance qu'un bon taux de réussite soit
  dû au hasard, la pire chute du cumul des gains, la part du capital qu'il
  serait raisonnable d'engager, la résistance du réglage à une variation de
  ±10 % — et un juge à huit critères qui compare ces mesures à neuf seuils et rend un score sur
  huit critères. Il ne décide rien : il mesure, et Jean-Luc décide.
② CONTEXTE D'APPEL — Ce fichier n'est jamais lancé. C'est une bibliothèque, que
  deux programmes vont chercher sur le disque et EXÉCUTENT pour s'en servir :
  `programmes/JUGE_DES_STRATEGIES.py`, dans sa fonction `main`, par `trouver(base,
  "MODULE_STATISTIQUES")` ; et `programmes/JUGER_SUR_8_CRITERES.py`, par
  `_charger(base, "MODULE_STATISTIQUES_*")`. Les deux le cherchent par un début
  de nom, parce que la date du 24-08-2026 fait partie du nom du fichier.
  IL NE TOURNE PAS LE SOIR : le pas du soir `TENIR_LES_POSITIONS.py` charge
  `JUGE_DES_STRATEGIES.py` pour deux de ses fonctions, `cle_valeur` et la lecture des
  cours, et ce chargement n'exécute pas ce fichier-ci. Il ne s'exécute que quand
  `JUGE_DES_STRATEGIES.py` est lancé seul. Mesuré en exécutant, par Cowork puis par le Chat,
  le 24-09-2026. Aucune tâche planifiée ne l'appelle.
③ ENTRÉE — Aucune : pas de ligne de commande, pas de fonction de lancement.
  Chaque fonction reçoit ses propres paramètres de son appelant.
④ CONDITIONS D'ENTRÉE — Python seul, et sa bibliothèque livrée d'origine
  (`math`, `statistics`, `random`, `datetime`, `itertools`). Aucun fichier,
  aucun autre programme du projet, aucun accès réseau. Ce fichier peut donc être
  exécuté n'importe où, y compris hors du dépôt.
⑤ SORTIE — Ne rend rien. Exécuté, il pose dans l'objet obtenu neuf fonctions et
  une table de seuils nommée `CRITERES_VALIDATION_EXPERTS`, qui porte neuf
  entrées pour huit critères — le quatrième critère en a deux, la chute maximale
  et la durée sous l'eau.
⑥ TRAITEMENT — Les neuf fonctions, dans l'ordre du fichier, avec l'état mesuré
  le 19-09-2026 de leurs appels : une recherche de chaque nom dans tous les
  fichiers `.py` du dépôt, `archives/` mis à part, donne le relevé suivant.
  ① `calculer_pbo` — la probabilité qu'un réglage ne doive ses bons résultats
  qu'au réglage lui-même. APPELÉE PAR PERSONNE.
  ② `calculer_significativite_wr` — le taux de réussite bat-il pile ou face.
  Appelée par `JUGER_SUR_8_CRITERES.py`, fonction `mesures_disponibles`.
  ③ `calculer_deflated_sharpe` — le rapport gain sur secousses, dégonflé du
  nombre d'essais qu'il a fallu pour le trouver. APPELÉE PAR PERSONNE.
  ④ `calculer_time_underwater` — la pire chute du cumul des gains et le temps
  qu'il faut pour en sortir. Appelée par `JUGE_DES_STRATEGIES.py`, fonction `juger`, et par
  `JUGER_SUR_8_CRITERES.py`, fonction `mesures_disponibles`.
  ⑤ `calculer_kelly_fractionnel` — la part du capital à engager. Appelée par
  `JUGER_SUR_8_CRITERES.py`, fonction `mesures_disponibles`.
  ⑥ `calculer_stabilite_parametrique` — le réglage tient-il à ±10 %. Appelée par
  `JUGE_DES_STRATEGIES.py`, fonction `juger`, et par `JUGER_SUR_8_CRITERES.py`, fonction
  `mesures_disponibles`.
  ⑦ `calculer_walk_forward` — la stratégie tient-elle sur des tranches de temps
  successives. APPELÉE PAR PERSONNE.
  ⑧ `calculer_sharpe_ratio` — le gain moyen rapporté à sa dispersion. Appelée
  par `JUGER_SUR_8_CRITERES.py`, fonction `mesures_disponibles`.
  ⑨ `evaluer_strategie_8_criteres` — le juge à huit critères, qui compare neuf mesures à la
  table et rend un score sur huit. Appelée par `JUGER_SUR_8_CRITERES.py`,
  fonction `calibrer`.
⑦ UNITÉ — Elles ne se mélangent pas, et elles se sont déjà croisées.
  Un POURCENT : `wr_pct` (63,1 pour 63,1 %), `dd_max_pct`, `esperance_pct`, et
  le seuil 25 du critère C4a.
  Une FRACTION entre 0 et 1 : `p_null` (0,5 pour le pur hasard), `p_value`,
  `pbo`, `dsr`, `kelly_fractionnel`, `frais_pct`, `tp`, `sl`, `fraction`, et les
  seuils 0,05 · 0,95 · 0,30 · 0,05 · 0,005 de la table.
  Des EUROS : `gain`, `net`, `dd_max_eur`, `capital`, dont la valeur par défaut
  est 100 000 € par opération.
  Des JOURS de calendrier : `time_underwater_max_jours`, et le seuil 365.
  Un NOMBRE D'OPÉRATIONS : `n_trades`, `n_strategies_testees`, `n_variations`.
  Un NOMBRE DE SÉANCES de bourse : `periodes_par_an`, par défaut 252.
  UN SUFFIXE `_pct` QUI DIT DEUX CHOSES : `dd_max_pct` vaut 0,5 pour une chute
  d'un demi-pourcent du capital, tandis que `frais_pct` vaut 0,0015 pour des
  frais de 0,15 % — l'un est un pourcent, l'autre une fraction, sous le même
  suffixe.
⑧ POURQUOI — Ces neuf fonctions ne sont pas écrites ici : elles ont été
  EXTRAITES le 24-08-2026 des lignes 6538 à 7177 d'un fichier du Drive,
  `projet_cac40_v2_56_AVEC_PROTOCOLE.py`, 784 957 octets, empreinte sha256
  b92a1cc79579a9bef882233600628df55a05f1bbd27ccd4592ba3e379b99eefc, et
  l'extraction a été vérifiée octet pour octet le jour même. Les sortir du gros
  fichier était la condition pour qu'elles puissent être appelées, calibrées et
  corrigées une par une.
  CINQ DÉFAUTS ONT ÉTÉ CORRIGÉS LE 24-08-2026, trois trouvés en lisant le code
  et deux en l'exécutant, et ils sont consignés ici parce qu'ils disent ce que le
  code fait aujourd'hui.
  ① `calculer_sharpe_ratio` ne s'annualisait pas : la formule calculait
  sqrt(periodes_par_an / 252), soit sqrt(1) = 1 avec la valeur par défaut, donc
  une multiplication par un. La formule juste multiplie par sqrt(252) = 15,8745.
  ② La loi normale inverse rendait, dans ses queues, l'approximation
  sqrt(−ln(1−p)), dont l'erreur CROÎT avec p — donc fausse précisément quand le
  nombre d'essais est grand, c'est-à-dire là où le dégonflage compte le plus.
  Remplacée par la queue de Wichura AS241, exacte à 1e-8.
  ③ `calculer_pbo` prenait une partition sur N à pas régulier, sur une liste
  rendue en ordre alphabétique : un pas régulier privilégie donc toujours les
  mêmes positions de blocs. Remplacé par un tirage au hasard à graine fixe
  20260824 — le biais disparaît, et deux passages rendent le même chiffre.
  ④ Les huit seuils du juge à huit critères étaient écrits deux fois, dans la table et de
  nouveau en dur dans le corps du juge à huit critères. Un chiffre qui existe ailleurs ne se
  recopie pas (R-708). Le juge à huit critères a été réécrit pour lire la table.
  ⑤ Révélé par le calibrage et invisible à la lecture : la loi normale inverse
  rendait zéro pour tout p ≤ 0,5, donc la moitié basse de la loi était MUETTE au
  lieu d'être fausse — le pire des cas, parce qu'un zéro ne se remarque pas.
  Corrigé par la symétrie de la fonction, Phi⁻¹(p) = −Phi⁻¹(1−p).
  UNE FAUSSE ALERTE, À NE PAS ROUVRIR : `calculer_deflated_sharpe` a semblé
  rendre toujours zéro. Vérification faite le 24-08-2026, elle fonctionne comme
  prévu ; le zéro n'est pas une panne, c'est la réponse. Après un grand nombre
  d'essais, un bon rapport gain sur secousses ne prouve plus rien : avec les
  3 888 combinaisons que prévoit la méthode du projet, il faut un Sharpe
  supérieur à 2,56 pour que le résultat signifie quelque chose.
  DEUX CONFLITS DE SEUIL RESTENT NON TRANCHÉS. ① La probabilité de
  sur-apprentissage : la table exige moins de 0,30, l'expert consulté le
  08-07-2026 dit moins de 0,50. ② Les frais du huitième critère : la table exige
  au moins 0,005, soit 50 points de base, tandis que le système en applique 15 —
  `MODULE_POSITIONS.FRAIS_TAUX` vaut 0,0015, le tarif Fortuneo PROGRESS. Tant que
  ce second conflit dure, aucune stratégie ne peut atteindre 8 sur 8.
  DEUX FONCTIONS NE SE CALIBRENT PAS SEULES : `calculer_stabilite_parametrique`
  et `calculer_walk_forward` attendent une façon de rejouer la stratégie, qui
  leur est fournie par leur appelant. Elles ne peuvent donc être éprouvées que par un programme qui rejoue la stratégie :
  aujourd'hui le juge des stratégies et `JUGER_SUR_8_CRITERES.py`, pour la stabilité seulement ; le walk-forward n'est appelé par personne.
⑨ CE QUI CLOCHE —
  ① LES SEUILS SONT DANS LE CODE, PAS AU REGISTRE, ET LA LOI DIT LE CONTRAIRE.
  La règle « les seuils vivent au REGISTRE, jamais dans le code » est écrite en
  toutes lettres dans `gouvernance/REGISTRE_REGLES.md`, règle R-743, deuxième
  geste, ligne 860, et elle y désigne nommément ce fichier : « Neuf seuils
  écrits en dur dans MODULE_STATISTIQUES enfreignaient déjà cette consigne ».
  Mesuré le 19-09-2026 : le mot REGISTRE n'apparaît pas une seule fois dans ce
  fichier — `grep -c REGISTRE` rend 0. Les neuf seuils appliqués vivent aux
  lignes 1730 à 1740, dans `CRITERES_VALIDATION_EXPERTS`, et c'est là, et nulle
  part ailleurs, que le juge à huit critères va les chercher. Le REGISTRE en porte une COPIE À LA
  MAIN, sous le titre « GRILLE-26-04 — la grille qui tourne aujourd'hui », qui
  annonce elle-même avoir été « relevée dans
  MODULE_STATISTIQUES.CRITERES_VALIDATION_EXPERTS le 13-09-2026 et recopiée ici
  au chiffre près ». Deux copies d'un même chiffre finissent toujours par
  diverger (R-708) : le jour où un seuil changera dans le code, le REGISTRE
  continuera d'annoncer l'ancien, et le seul contrôle qui existe —
  `seuils_du_registre` de `programmes/JUGER_SUR_8_CRITERES.py` — ne vérifie que
  la PRÉSENCE du texte « 0,30 » dans le document, jamais l'égalité de deux
  valeurs.
  ② ONZE AUTRES NOMBRES DÉCIDENT, ET ILS NE SONT MÊME PAS DANS LA TABLE.
  Relevés le 19-09-2026 par leur numéro de ligne : 0,30 et 0,50 décident du
  verdict FAIBLE / MOYEN / ÉLEVÉ de la probabilité de sur-apprentissage
  (lignes 486 et 488) · 0,05 et 0,01 décident de `significatif_95` et
  `significatif_99` (lignes 633 et 634) · 0,95, 0,90 et 0,80 décident du verdict
  EXCELLENT / BON / ACCEPTABLE du Sharpe dégonflé (lignes 859, 861 et 863) · 0,5
  et 0 décident si un réglage est déclaré stable (ligne 1405) · 0,005 décide du
  huitième critère en repli (ligne 2003) · 6 décide du passage de ARCHIVÉE à EN
  COURS DE TEST (ligne 2010). Vingt nombres tranchent donc au total, neuf dans la
  table et onze hors d'elle, et pas un seul n'est lu au REGISTRE.
  ③ LA TABLE EST LUE POUR SIX CRITÈRES SUR NEUF, ET DÉCORATIVE POUR TROIS.
  Mesuré le 19-09-2026 en modifiant la table puis en rejouant le juge à huit critères sur les
  chiffres témoins de la stratégie C5-EI, qui donnent 7 sur 8 : durcir le seuil
  du premier critère de 0,05 à 0,001 fait bien tomber le verdict à 6 sur 8, donc
  cette entrée est lue ; mais porter le seuil des frais de 0,005 à 0,99 — ce qui
  rend ce critère impossible à passer — laisse le verdict à 7 sur 8, et mettre à
  faux l'exigence du walk-forward le laisse aussi à 7 sur 8. Les entrées
  `C6_stabilite`, `C7_wf_positifs` et
  `C8_frais_realistes` ne sont donc jamais consultées. Un lecteur qui corrige un
  seuil dans la table croit avoir changé le juge à huit critères, et n'a rien changé du tout.
  ④ LE SUFFIXE `_pct` PORTE DEUX UNITÉS DIFFÉRENTES. Mesuré le 19-09-2026 :
  `calculer_time_underwater` rend `dd_max_pct` valant 0,5 pour une chute de
  500 € sur 100 000 €, soit un demi-POURCENT ; `calculer_kelly_fractionnel`
  attend `frais_pct` valant 0,0015 pour des frais de 0,15 %, soit une FRACTION.
  Le même suffixe désigne donc deux grandeurs qui diffèrent d'un facteur cent.
  C'est exactement le genre de croisement qui a coûté une journée le 13-09-2026,
  quand 50 a été passé à la place de 0,5 comme probabilité du hasard : la
  variance devenait négative, la fonction rendait son cas de repli, et une
  p-value de 1,0 sortait sur 103 opérations à 63 % de réussite.
  ⑤ TROIS FONCTIONS SUR NEUF NE SONT APPELÉES PAR PERSONNE. Mesuré le
  19-09-2026 en cherchant chaque nom dans tous les fichiers `.py` du dépôt,
  `archives/` mis à part : `calculer_pbo`, `calculer_deflated_sharpe` et
  `calculer_walk_forward` ne rendent aucune ligne d'appel. Ce sont justement les
  trois mesures que `JUGER_SUR_8_CRITERES.py` déclare ne pas savoir produire, et
  qu'il rend vides. Le code qui saurait les produire existe donc, et n'est
  branché nulle part.
  ⑥ TROIS RATTRAPAGES D'ERREUR SANS NOM AVALENT TOUT. Aux lignes 402, 428 et
  1025, la forme employée rattrape n'importe quelle erreur sans dire laquelle, y
  compris une interruption au clavier. Ligne 428, elle est dans la boucle qui
  range chaque opération dans son bloc de temps : une opération dont la date est
  mal écrite est SAUTÉE en silence, et le calcul continue sur les autres sans que
  rien n'indique qu'il en manque.
  ⑦ LES CHIFFRES DE RÉFÉRENCE DU SHARPE DÉGONFLÉ NE SONT PAS REPRODUCTIBLES EN
  L'ÉTAT. Ce texte annonce, pour un Sharpe de 1,5 : 1,000 sur 2 essais, 0,996 sur
  100 essais, 0,000 sur 3 888 essais. La fonction demande quatre nombres, et deux
  ne sont pas dits : la variance des Sharpe de l'ensemble et le nombre
  d'opérations. Mesuré le 19-09-2026 en essayant 998 000 couples — variance de
  0,005 à 10 par pas de 0,005, nombre d'opérations de 2 à 500 — 127 couples
  rendent exactement ce triplet, et aucun moyen ne permet de savoir lequel a
  servi. Un chiffre de référence qu'on ne peut pas rejouer n'arbitre rien.
⑩ EFFET — N'écrit aucun fichier, n'affiche rien, ne touche pas au réseau : une
  exécution de ce fichier ne fait que définir neuf fonctions et une table. UNE
  SEULE DE SES FONCTIONS LAISSE UNE TRACE HORS D'ELLE-MÊME :
  `calculer_stabilite_parametrique` appelle `random.seed(42)`, ligne 1366, qui
  remplace la graine du tirage au hasard de TOUT le programme appelant. Mesuré le
  19-09-2026 : après `random.seed(7)`, le tirage suivant rend 0,32383276 sans
  appel à cette fonction, et 0,42192181 avec.
⑪ TERMINAISON — Aucun code de sortie : ce fichier n'a pas de fonction de
  lancement et ne s'arrête jamais de lui-même. Chacune de ses neuf fonctions rend
  la main dans le cas ordinaire. Trois peuvent lever une erreur non rattrapée, ce
  qui arrêterait le programme appelant : `calculer_deflated_sharpe` sur une
  variance négative, `calculer_walk_forward` sur un signal sans date, et
  `evaluer_strategie_8_criteres` sur une mesure présente mais vide — les trois
  mesurées le 19-09-2026. Et un de ses appels peut ne pas revenir :
  `calculer_stabilite_parametrique` et `calculer_walk_forward` appellent la
  façon de rejouer que leur appelant leur a donnée, et ce qu'elle fait leur
  échappe.
⑫ DÉFINITIONS
  une opération : un achat simulé suivi de sa revente, avec son gain net en
    euros ; aucun ordre réel n'est jamais passé
  le juge à huit critères : `evaluer_strategie_8_criteres`, la fonction de `MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py` qui compare neuf mesures à leurs seuils et rend un score sur huit
  la table : `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740, qui porte les neuf
    seuils et le sens de comparaison de chacun
  la grille : la liste des huit critères et de leurs seuils ; celle qui tourne s'appelle GRILLE-26-04 et vit dans `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740 de ce fichier
  le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les
    règles numérotées du projet
  le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur
    l'historique des cours et rend la liste de ses opérations
  le taux de réussite : la part des opérations qui se sont refermées sur un gain,
    écrite en pourcent
  la p-value : la probabilité qu'un taux de réussite au moins aussi bon soit
    obtenu par le seul hasard ; plus elle est petite, moins le hasard explique le
    résultat
  le Sharpe : le rapport du gain moyen à sa dispersion, ramené à l'année
  le Sharpe dégonflé : le Sharpe corrigé du nombre de stratégies essayées ; plus
    on en essaie, plus un bon Sharpe peut n'être que du hasard
  la probabilité de sur-apprentissage : la probabilité qu'une stratégie doive ses
    bons résultats au réglage sur les données passées plutôt qu'à un effet réel
  le Kelly fractionnel : la part du capital qu'il serait raisonnable d'engager
    sur une opération, compte tenu du taux de réussite et des gains et pertes
    attendus
  la durée sous l'eau : le nombre de jours pendant lesquels le cumul des gains
    reste sous son plus haut précédent
  le walk-forward : le rejeu d'une stratégie sur des tranches de temps
    successives, pour voir si elle tient hors de la période qui a servi à la
    régler
  le backtest : le rejeu d'une stratégie sur des cours passés, pour estimer ce
    qu'elle aurait donné
  un point de base : un centième de pourcent ; 15 points de base valent 0,15 %
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
    étant qu'une copie de lecture
  l'exécutant : le service qui lance les programmes du soir sans intervention humaine
  la boucle : la tache planifiee qui lit les signaux et rend compte
  la graine : le nombre qui fixe la suite de tirages, pour qu'un calcul fondé sur le hasard donne toujours le même résultat
  la pire chute : la plus forte baisse du cumul depuis un sommet precedent.
  le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
  un réglage : un des nombres qui définissent une stratégie — l'objectif de gain, la perte acceptée, l'horizon
  un signal : le repérage, sur la dernière séance connue, d'une configuration de cours qui déclenche une simulation d'achat.
  une fraction : la façon d'écrire un pourcentage entre 0 et 1 — 0,040 pour +4 % — par opposition au pourcent, qui écrirait 4.0
  une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle a tourné — rapport de boucle, rapport d'audit, cockpit, historique des mesures.
"""

def calculer_pbo(matrice_trades: list[list[dict]], n_partitions: int = 16) -> dict:
    """Dit quelle part du temps le meilleur réglage d'un lot n'est qu'un mirage.

    ① RÔLE — Répondre à la question que le reste du système ne sait pas poser :
      quand on essaie beaucoup de réglages et qu'on garde le meilleur, ce meilleur
      est-il bon, ou seulement chanceux ? La fonction reçoit un LOT de stratégies
      avec leurs opérations, découpe le temps en blocs, et refait un grand nombre de
      fois l'expérience suivante : prendre la moitié des blocs, y désigner la
      stratégie gagnante, puis regarder où cette gagnante se classe sur l'autre
      moitié. Si elle retombe souvent dans la moitié basse du classement, c'est que
      la sélection ne valait rien. La part des expériences où elle retombe ainsi est
      le chiffre rendu : 0 veut dire que la sélection tient toujours, 1 qu'elle ne
      tient jamais. Le critère C3 de la grille exige moins de 0,30.
    ② CONTEXTE D'APPEL — PERSONNE NE L'APPELLE. Mesuré le 19-09-2026 par une
      recherche du nom `calculer_pbo` dans tous les fichiers `.py` du dépôt,
      `archives/` mis à part : aucune ligne d'appel, hors la définition elle-même.
      `programmes/JUGER_SUR_8_CRITERES.py` rend d'ailleurs cette mesure VIDE, avec
      pour motif écrit dans son code qu'elle « exige une MATRICE de rejeux », c'est-
      à-dire le lot entier des stratégies essayées et non une seule.
    ③ ENTRÉE — `matrice_trades` : la liste des stratégies du lot, chacune étant
      elle-même la liste de ses opérations ; chaque opération est un tableau portant
      au moins `date`, écrite année-mois-jour, et `gain`, en euros. Aucun appelant
      aujourd'hui, donc aucune valeur réellement passée. `n_partitions` : le nombre
      de blocs de temps, 16 quand rien n'est précisé.
    ④ CONDITIONS D'ENTRÉE — Au moins deux stratégies dans le lot, au moins une
      opération portant une date, et une période couverte d'au moins quatre jours.
      Toutes les stratégies du lot doivent avoir été jouées sur la MÊME période,
      sans quoi les blocs de temps ne les comparent pas entre elles.
    ⑤ SORTIE — UNE valeur : un tableau. Il prend cinq formes selon la branche, et
      elles ne portent pas les mêmes cases. Quand le calcul aboutit : `pbo`,
      `pbo_pct`, `logits`, `n_combinaisons`, `n_partitions`, `verdict` et
      `logit_median`. Dans les quatre cas d'arrêt — moins de deux stratégies, aucune
      date, date mal écrite, période trop courte — `logit_median` est ABSENTE et une
      case `erreur` apparaît à la place. Mesuré le 19-09-2026 sur un lot d'une seule
      stratégie : le tableau rendu porte `erreur` valant « Moins de 2 combinaisons »
      et ne porte pas `logit_median`.
      [rend: 1]
    ⑥ TRAITEMENT — ① refuser un lot de moins de deux stratégies · ② rassembler
      toutes les dates du lot et en prendre la plus ancienne et la plus récente ·
      ③ refuser si aucune date, ou si la plus ancienne ne se lit pas ·
      ④ si la période en JOURS est inférieure au nombre de blocs demandé, réduire le
      nombre de blocs à un septième de la durée, sans descendre sous quatre ·
      ⑤ pour chaque stratégie, additionner ses gains dans le bloc qui correspond à
      la date de chaque opération · ⑥ dresser la liste de toutes les façons de
      prendre la moitié des blocs · ⑦ si elles dépassent mille, en tirer mille au
      hasard avec la graine fixe 20260824 · ⑧ pour chacune : désigner la stratégie
      qui gagne sur la moitié retenue, compter combien de stratégies font moins bien
      qu'elle sur l'autre moitié, ramener ce rang entre 0 et 1, et en prendre le
      logarithme du rapport au complément · ⑨ le chiffre rendu est la part de ces
      logarithmes qui sont négatifs ou nuls · ⑩ poser le verdict FAIBLE sous 0,30,
      MOYEN sous 0,50, ÉLEVÉ au-dessus.
    ⑦ UNITÉ — Le chiffre rendu, `pbo`, est une FRACTION entre 0 et 1 ; `pbo_pct` est
      le même chiffre écrit en POURCENT, dans un texte, pour l'affichage.
      `n_partitions` est un NOMBRE DE BLOCS de temps. Les gains sont des EUROS. La
      durée de la période est un NOMBRE DE JOURS de calendrier, et la durée d'un bloc
      un NOMBRE DE JOURS à virgule. Les logarithmes rendus sont sans unité.
    ⑧ POURQUOI — Le tirage au hasard porte une GRAINE FIXE, 20260824, et ce n'est
      pas une commodité. La liste de toutes les façons de couper les blocs est
      produite en ordre alphabétique : en y prenant une partition sur N à pas
      régulier, ce qu'une version antérieure faisait, on retient toujours les mêmes
      positions de blocs, et le chiffre rendu s'en trouve faussé. Le tirage au hasard
      enlève ce biais ; la graine fixe rend le résultat reproductible au chiffre
      près, ce qu'exige tout calibrage. Mesuré le 19-09-2026 sur un lot de
      20 stratégies et 120 opérations chacune : deux passages successifs rendent le
      même 0,421.
      Le plafond de mille partitions existe parce que le nombre de façons de prendre
      huit blocs sur seize est de 12 870 : les parcourir toutes coûte treize fois
      plus de temps pour un chiffre qui ne bouge plus.
      Le rang est ramené entre 0 et 1 en ajoutant un demi avant de diviser, puis
      borné entre 0,001 et 0,999, parce que le logarithme du rapport au complément
      n'existe ni en 0 ni en 1 : sans cette précaution, la stratégie qui arrive
      dernière ferait tomber la fonction.
    ⑨ CE QUI CLOCHE —
      ① Le chiffre rendu quand RIEN N'A ÉTÉ MESURÉ est 0,0, qui est la MEILLEURE
      valeur possible. Mesuré le 19-09-2026 sur un lot d'une seule stratégie : le
      tableau rendu porte `pbo` valant 0.0, avec le verdict INSUFFISANT et une case
      `erreur`. Un appelant qui lit `pbo` sans regarder `verdict` ni `erreur` reçoit
      donc « aucun sur-apprentissage » là où il n'y a eu aucun calcul, et le critère
      C3 de la grille, qui exige moins de 0,30, est passé haut la main.
      ② La comparaison qui décide de réduire le nombre de blocs mélange deux unités.
      Elle compare la durée de la période, en JOURS, au nombre de blocs demandé, qui
      est un COMPTE. Les deux grandeurs n'ont pas de rapport : une période de
      20 jours avec 16 blocs demandés passe sans réduction, et donne des blocs d'un
      jour et quart chacun.
      ③ La branche de refus qui suit cette réduction n'est jamais atteinte. La
      réduction pose le nombre de blocs au plus grand entre quatre et un septième de
      la durée, puis refuse si ce nombre est inférieur à quatre. Mesuré le
      19-09-2026 : pour une durée de 0 à 100 000 jours, ce calcul ne rend jamais
      moins de quatre. Le message « Période trop courte » ne peut donc pas sortir, et
      une période de quatre jours est calculée normalement : mesuré le même jour sur
      trois stratégies couvrant quatre jours, la fonction rend 1,0 avec le verdict
      ÉLEVÉ, sans un mot d'avertissement.
      ④ Ce que la fonction calcule n'est pas ce que son texte d'origine annonçait. Le
      texte décrivait un rang ramené entre 0 et 1 en divisant par le nombre de
      stratégies AUGMENTÉ DE UN ; le code divise par le nombre de stratégies, après
      avoir ajouté un demi au rang. Les deux donnent des chiffres voisins mais
      différents, et rien ne dit lequel fait foi.
      ⑤ Une opération dont la date est mal écrite est SAUTÉE sans un mot. Le
      rattrapage d'erreur de la boucle qui range les opérations dans leurs blocs,
      ligne 428, n'a pas de nom et avale tout. Une stratégie dont toutes les dates
      seraient mal écrites entrerait dans le calcul avec des gains nuls partout, et
      serait comparée aux autres comme si elle n'avait rien gagné.
      ⑥ Le chiffre 0,30 qui pose le verdict FAIBLE est écrit ligne 486, et le seuil
      du critère C3 est écrit 0,30 lui aussi, ligne 1733, dans la table des seuils. Un
      chiffre qui existe ailleurs ne se recopie pas (R-708) : le jour où le conflit
      ouvert sur ce seuil sera tranché — la table exige moins de 0,30, l'expert
      consulté le 08-07-2026 dit moins de 0,50 — corriger l'un sans l'autre fera
      afficher « FAIBLE » à côté d'un critère non passé.
    ⑩ EFFET — Ne lit ni n'écrit aucun fichier, n'affiche rien, ne touche pas au
      réseau. Elle ne modifie pas le lot de stratégies qu'elle reçoit : elle en
      construit un tableau de gains par bloc à part. Le tirage au hasard qu'elle
      emploie est un tirage à elle, créé pour l'occasion, et ne touche pas à la
      graine du hasard du programme appelant.
    ⑪ TERMINAISON — Rend toujours la main, par l'une de ses cinq sorties. Elle ne
      lève pas : la lecture des dates et le rangement des opérations sont rattrapés.
      Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      une opération : un achat simulé suivi de sa revente, avec son gain net en
        euros ; aucun ordre réel n'est jamais passé
      la grille : la liste des huit critères et de leurs seuils ; celle qui tourne
        s'appelle GRILLE-26-04 et vit dans `CRITERES_VALIDATION_EXPERTS`, lignes 1730
        à 1740 de ce fichier
      la table des seuils : `CRITERES_VALIDATION_EXPERTS`, qui porte les neuf seuils
        et le sens de comparaison de chacun
      la probabilité de sur-apprentissage : la probabilité qu'une stratégie doive ses
        bons résultats au réglage sur les données passées plutôt qu'à un effet réel
      un bloc : une suite de lignes qui se suivent dans le texte et dont les dates décroissent sans trou plus grand que six jours.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
    
      la boucle : la tache planifiee qui lit les signaux et rend compte
      la graine : le nombre qui fixe la suite de tirages, pour qu'un calcul fondé sur le hasard donne toujours le même résultat
      une fraction : la façon d'écrire un pourcentage entre 0 et 1 — 0,040 pour +4 % — par opposition au pourcent, qui écrirait 4.0
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    import math
    import statistics
    from itertools import combinations

    n_strategies = len(matrice_trades)
    if n_strategies < 2:
        return {'pbo': 0.0, 'pbo_pct': '—', 'logits': [], 'n_combinaisons': n_strategies,
                'n_partitions': n_partitions, 'verdict': 'INSUFFISANT', 'erreur': 'Moins de 2 combinaisons'}

    # ── ÉTAPE 1 : agréger les gains par bloc temporel ──
    # Trouver la plage de dates globale
    toutes_dates = []
    for trades in matrice_trades:
        for t in trades:
            d = t.get('date', '')
            if d: toutes_dates.append(d)

    if not toutes_dates:
        return {'pbo': 0.0, 'pbo_pct': '—', 'logits': [], 'verdict': 'INSUFFISANT',
                'n_combinaisons': n_strategies, 'n_partitions': n_partitions,
                'erreur': 'Aucun trade'}

    toutes_dates.sort()
    date_min = toutes_dates[0]
    date_max = toutes_dates[-1]

    # Convertir dates en index numérique
    from datetime import datetime as _dt
    try:
        d_min = _dt.strptime(date_min, '%Y-%m-%d')
        d_max = _dt.strptime(date_max, '%Y-%m-%d')
    except:
        return {'pbo': 0.0, 'pbo_pct': '—', 'logits': [], 'verdict': 'ERREUR',
                'n_combinaisons': n_strategies, 'n_partitions': n_partitions,
                'erreur': 'Format date invalide'}

    duree_totale = (d_max - d_min).days
    if duree_totale < n_partitions:
        # Réduire le nombre de partitions
        n_partitions = max(4, duree_totale // 7)
        if n_partitions < 4:
            return {'pbo': 0.0, 'pbo_pct': '—', 'logits': [], 'verdict': 'INSUFFISANT',
                    'n_combinaisons': n_strategies, 'n_partitions': n_partitions,
                    'erreur': f'Période trop courte ({duree_totale}j)'}

    duree_bloc_jours = duree_totale / n_partitions

    # Pour chaque stratégie : matrice de gains par bloc [n_strat][n_partitions]
    matrice_blocs = []
    for trades in matrice_trades:
        blocs = [0.0] * n_partitions
        for t in trades:
            try:
                d = _dt.strptime(t.get('date', ''), '%Y-%m-%d')
                idx = int((d - d_min).days / duree_bloc_jours)
                idx = min(idx, n_partitions - 1)
                blocs[idx] += t.get('gain', 0.0)
            except:
                continue
        matrice_blocs.append(blocs)

    # ── ÉTAPE 2 : itérer sur les partitions IS/OOS ──
    # Pour M=16, C(16, 8) = 12 870 combinaisons (un peu lourd)
    # On limite à un échantillon raisonnable
    indices = list(range(n_partitions))
    moitie = n_partitions // 2
    toutes_partitions = list(combinations(indices, moitie))

    # Limiter pour rester rapide
    MAX_PARTITIONS = 1000
    if len(toutes_partitions) > MAX_PARTITIONS:
        # CORRIGÉ 24-08-2026 (défaut 3) : l'ancienne version prenait une
        # partition sur N à PAS RÉGULIER. Or `combinations` rend ses tuples
        # en ordre lexicographique : un pas régulier privilégie donc
        # systématiquement certaines positions de blocs, ce qui biaise le PBO.
        # Remplacé par un tirage ALÉATOIRE, mais à GRAINE FIXE : le résultat
        # reste reproductible au chiffre près, condition du calibrage (9bis).
        import random as _rd
        _tirage = _rd.Random(20260824)
        toutes_partitions = _tirage.sample(toutes_partitions, MAX_PARTITIONS)

    logits = []
    for partition_is in toutes_partitions:
        partition_oos = tuple(i for i in indices if i not in partition_is)

        # Performance in-sample par stratégie
        perfs_is = []
        perfs_oos = []
        for blocs in matrice_blocs:
            perf_is = sum(blocs[i] for i in partition_is)
            perf_oos = sum(blocs[i] for i in partition_oos)
            perfs_is.append(perf_is)
            perfs_oos.append(perf_oos)

        # Trouver la stratégie gagnante en IS
        idx_best_is = perfs_is.index(max(perfs_is))

        # Rang de cette stratégie en OOS
        perf_best_oos = perfs_oos[idx_best_is]
        # Rang = nombre de stratégies avec perf_oos < perf_best_oos
        rang_brut = sum(1 for p in perfs_oos if p < perf_best_oos)
        # Normaliser dans ]0, 1[
        rang_norm = (rang_brut + 0.5) / n_strategies
        rang_norm = max(0.001, min(0.999, rang_norm))  # sécurité

        # Logit
        logit = math.log(rang_norm / (1 - rang_norm))
        logits.append(logit)

    # ── ÉTAPE 3 : PBO = proportion de logits ≤ 0 ──
    n_logits = len(logits)
    n_negatifs = sum(1 for l in logits if l <= 0)
    pbo = n_negatifs / n_logits if n_logits > 0 else 0.0

    # Verdict
    if pbo < 0.30:
        verdict = 'FAIBLE'
    elif pbo < 0.50:
        verdict = 'MOYEN'
    else:
        verdict = 'ÉLEVÉ'

    return {
        'pbo': pbo,
        'pbo_pct': f'{pbo*100:.1f}%',
        'logits': logits,
        'n_combinaisons': n_strategies,
        'n_partitions': n_partitions,
        'verdict': verdict,
        'logit_median': statistics.median(logits) if logits else 0.0,
    }


# ═══════════════════════════════════════════════════════════════════════
# 8 MÉTRIQUES VALIDÉES PAR LE COMITÉ D'EXPERTS (López de Prado, Lo, Hull,
# Vince, Aronson, Chan) — adoptées le 26/04/2026 sur recommandation collective.
# ═══════════════════════════════════════════════════════════════════════

def calculer_significativite_wr(n_trades: int, wr_pct: float, p_null: float = 0.5) -> dict:
    """Dit quelle chance il y a qu'un taux de réussite pareil sorte de pile ou face.

    ① RÔLE — Donner au premier critère de la grille le chiffre qu'il compare à son
      seuil. Un taux de réussite de 63,1 % sur 103 opérations paraît bon, mais pile
      ou face rend parfois 63 % sur 103 tirages. Cette fonction mesure l'écart entre
      le taux observé et le hasard pur, le rapporte à la dispersion attendue, et en
      tire la probabilité qu'un tel écart soit dû au seul hasard. Mesuré le
      19-09-2026 sur 103 opérations à 63,1 % : cet écart vaut 2,1737 fois la
      dispersion attendue, et la probabilité rendue est 0,0078 — le critère C1, qui
      exige moins de 0,05, est passé.
    ② CONTEXTE D'APPEL — Un seul appelant, `programmes/JUGER_SUR_8_CRITERES.py`,
      dans sa fonction `mesures_disponibles`, une fois par stratégie
      mesurée. Il lui passe le nombre d'opérations, le taux de réussite calculé sur
      ces opérations, et la valeur 0,5.
    ③ ENTRÉE — `n_trades` : le nombre d'opérations. Son seul appelant y met le
      nombre d'opérations rendues par le juge des stratégies, par exemple 103 pour la stratégie
      C5E10-OBS-V1 le 19-09-2026. `wr_pct` : le taux de réussite EN POURCENT, non
      arrondi, par exemple 63,10679611650485 pour ces mêmes 103 opérations.
      `p_null` : la probabilité de référence, 0,5 quand rien n'est précisé, et 0,5
      est aussi ce que son appelant passe explicitement.
    ④ CONDITIONS D'ENTRÉE — `p_null` doit être une PROBABILITÉ strictement comprise
      entre 0 et 1, jamais un pourcent. Le 13-09-2026, 50 y a été passé à la place de
      0,5 : la dispersion attendue devenait négative, la fonction rendait son cas de
      repli, et une probabilité de 1,0 sortait sur 103 opérations à 63 % de réussite
      — un résultat impossible, et c'est ce qui a permis de voir la faute.
    ⑤ SORTIE — UNE valeur : un tableau, sous trois formes. Quand le calcul aboutit :
      `z_score`, arrondi au millième, `p_value`, arrondie au dix-millième,
      `significatif_95` et `significatif_99`. Quand il n'y a aucune opération : les
      mêmes quatre cases, avec 0 et 1,0, PLUS une case `erreur` valant « Pas de
      trades ». Quand la dispersion attendue est nulle ou négative : les quatre cases
      seulement, SANS case `erreur` — mesuré le 19-09-2026 en passant une probabilité
      de référence de 1,0.
      [rend: 1]
    ⑥ TRAITEMENT — ① refuser un nombre d'opérations nul ou négatif · ② ramener le
      taux de réussite de pourcent en fraction, en divisant par cent · ③ calculer la
      dispersion attendue sous l'hypothèse du hasard, qui vaut la probabilité de
      référence multipliée par son complément et divisée par le nombre d'opérations ·
      ④ refuser si cette dispersion est nulle ou négative · ⑤ diviser l'écart entre
      le taux observé et la probabilité de référence par la racine de cette
      dispersion · ⑥ en tirer la probabilité par la fonction d'erreur complémentaire
      de la loi normale · ⑦ dire si cette probabilité est sous 0,05 puis sous 0,01.
    ⑦ UNITÉ — `wr_pct` est un POURCENT : 63,1 et non 0,631. `p_null` et `p_value`
      sont des FRACTIONS entre 0 et 1. `n_trades` est un NOMBRE D'OPÉRATIONS.
      `z_score` est un nombre de fois la dispersion attendue, donc sans unité.
      `significatif_95` et `significatif_99` valent vrai ou faux.
    ⑧ POURQUOI — La probabilité est obtenue par une approximation de la loi normale
      plutôt que par le calcul exact de la loi binomiale, parce que cette
      approximation ne demande que la bibliothèque livrée avec Python. Tout ce
      fichier tient sans aucune bibliothèque installée, ce qui lui permet d'être
      exécuté n'importe où, y compris hors du dépôt.
      Les deux cases `significatif_95` et `significatif_99` emploient les seuils
      d'usage de la littérature, 0,05 et 0,01. Le critère C1 de la grille n'en lit
      aucune : il reprend la probabilité et la compare lui-même à son propre seuil,
      qui vaut aussi 0,05.
    ⑨ CE QUI CLOCHE —
      ① LE CALCUL NE RÉPOND PAS À LA QUESTION POSÉE, ET UNE STRATÉGIE PERDANTE EST
      DÉCLARÉE SIGNIFICATIVE. Le texte d'origine annonce un test à un seul côté,
      « le taux de réussite est-il SUPÉRIEUR au hasard », mais la probabilité
      calculée prend la valeur absolue de l'écart : elle répond donc à « le taux
      s'ÉCARTE-T-IL du hasard », dans un sens ou dans l'autre. Mesuré le 19-09-2026 :
      103 opérations à 63,1 % de réussite rendent une probabilité de 0,0078, et
      103 opérations à 36,9 % — une stratégie qui perd deux fois sur trois — rendent
      la MÊME probabilité de 0,0078, avec `significatif_99` à vrai. Le critère C1 de
      la grille, qui exige seulement une probabilité inférieure à 0,05, serait donc
      passé par une stratégie franchement perdante. Aucune stratégie du projet n'est
      aujourd'hui dans ce cas, mais rien n'empêche qu'une le soit.
      ② Les trois sorties ne portent pas les mêmes cases. La case `erreur` n'apparaît
      que dans un des deux cas de refus : mesuré le 19-09-2026, un nombre
      d'opérations nul la fait apparaître, une probabilité de référence de 1,0 ne la
      fait pas apparaître. Un appelant qui distingue « mesuré » de « pas mesuré » en
      cherchant cette case se trompe une fois sur deux.
      ③ Le cas de refus rend une probabilité de 1,0, qui est la PIRE valeur possible
      et aussi une valeur parfaitement plausible. Rien dans le chiffre ne dit s'il
      vient d'un calcul ou d'un renoncement. C'est exactement ce qui a masqué la
      faute du 13-09-2026 pendant un temps : la sortie était un nombre ordinaire.
      ④ Les seuils 0,05 et 0,01, lignes 633 et 634, sont écrits dans le corps de la
      fonction, hors de la table des seuils de ce fichier, et hors du REGISTRE. La
      règle du projet veut que les seuils vivent au REGISTRE et jamais dans le code —
      `gouvernance/REGISTRE_REGLES.md`, règle R-743, deuxième geste. Et le 0,05 de la
      ligne 633 est le même nombre que le seuil du critère C1, écrit ligne 1731 : un
      chiffre qui existe ailleurs ne se recopie pas (R-708).
      ⑤ Le taux de réussite est reçu en POURCENT et la probabilité de référence en
      FRACTION, dans la même signature, sans que rien dans les noms ne le dise —
      `wr_pct` porte son unité, `p_null` non. C'est le croisement exact qui a coûté
      la journée du 13-09-2026.
    ⑩ EFFET — Ne lit ni n'écrit aucun fichier, n'affiche rien, ne touche pas au
      réseau, ne modifie rien de ce qu'elle reçoit.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas : la racine carrée n'est
      prise que d'une valeur dont la fonction vient de vérifier qu'elle est
      strictement positive. Elle n'appelle aucune fonction du projet.
      [sort: non]
    ⑫ DÉFINITIONS
      une opération : un achat simulé suivi de sa revente, avec son gain net en
        euros ; aucun ordre réel n'est jamais passé
      le taux de réussite : la part des opérations qui se sont refermées sur un gain,
        écrite en pourcent
      la grille : la liste des huit critères et de leurs seuils ; celle qui tourne
        s'appelle GRILLE-26-04 et vit dans `CRITERES_VALIDATION_EXPERTS`, lignes 1730
        à 1740 de ce fichier
      la table des seuils : `CRITERES_VALIDATION_EXPERTS`, qui porte les neuf seuils
        et le sens de comparaison de chacun
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les
        règles numérotées du projet
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur
        l'historique des cours et rend la liste de ses opérations
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
    
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    import math
    if n_trades <= 0:
        return {'z_score': 0, 'p_value': 1.0, 'significatif_95': False, 'significatif_99': False,
                'erreur': 'Pas de trades'}
    p_obs = wr_pct / 100
    var = p_null * (1 - p_null) / n_trades
    if var <= 0:
        return {'z_score': 0, 'p_value': 1.0, 'significatif_95': False, 'significatif_99': False}
    sigma = math.sqrt(var)
    z = (p_obs - p_null) / sigma
    # p-value bilatérale via approximation normale
    # P(|Z| > z) = 2 × (1 - Φ(|z|))
    # Φ approximation : erfc(z/sqrt(2))/2
    p_value = math.erfc(abs(z) / math.sqrt(2))
    return {
        'z_score': round(z, 3),
        'p_value': round(p_value, 4),
        'significatif_95': p_value < 0.05,
        'significatif_99': p_value < 0.01,
    }


def calculer_deflated_sharpe(sharpe_observe: float, n_strategies_testees: int,
                               variance_sharpe_ensemble: float, n_trades: int,
                               skewness: float = 0, kurtosis: float = 3) -> dict:
    """Dégonfle le rapport gain sur secousses du nombre d'essais qu'il a fallu pour
    le trouver.

    ① RÔLE — Donner au deuxième critère de la grille le chiffre qu'il compare à son
      seuil. Quand on essaie trois mille réglages et qu'on garde le meilleur, le
      meilleur est bon en partie parce qu'on en a essayé trois mille : c'est vrai
      même si aucun ne vaut rien. Cette fonction calcule d'abord le rapport gain sur
      secousses que le PUR HASARD aurait produit au mieux, compte tenu du nombre
      d'essais, puis mesure de combien le rapport observé le dépasse, et en fait une
      probabilité entre 0 et 1. Mesuré le 19-09-2026 pour un rapport observé de 1,5,
      une variance de l'ensemble de 0,25 et 100 opérations : sur 2 essais elle rend
      1,0 — EXCELLENT ; sur 100 essais 0,945 — BON ; sur 3 888 essais 0,017 —
      INSUFFISANT. Le même rapport de 1,5 ne prouve donc plus rien une fois qu'on a
      essayé 3 888 combinaisons.
    ② CONTEXTE D'APPEL — PERSONNE NE L'APPELLE. Mesuré le 19-09-2026 par une
      recherche du nom `calculer_deflated_sharpe` dans tous les fichiers `.py` du
      dépôt, `archives/` mis à part : aucune ligne d'appel, hors la définition
      elle-même. `programmes/JUGER_SUR_8_CRITERES.py` rend cette mesure VIDE, avec
      pour motif écrit dans son code qu'elle « exige le LOT ENTIER » : deux de ses
      quatre entrées sont des grandeurs de l'ensemble des stratégies essayées, et non
      d'une stratégie prise seule.
    ③ ENTRÉE — `sharpe_observe` : le rapport gain sur secousses de la stratégie
      jugée, annualisé. `n_strategies_testees` : le nombre total de stratégies
      essayées pour arriver à celle-là. `variance_sharpe_ensemble` : la variance des
      rapports de tout le lot essayé. `n_trades` : le nombre d'opérations de la
      stratégie jugée. `skewness` : l'asymétrie des gains, 0 quand rien n'est
      précisé. `kurtosis` : l'épaisseur des queues, 3 quand rien n'est précisé, qui
      est la valeur de la loi normale. Aucun appelant aujourd'hui, donc aucune valeur
      réellement passée.
    ④ CONDITIONS D'ENTRÉE — Au moins deux stratégies essayées et au moins deux
      opérations. La variance de l'ensemble doit être POSITIVE OU NULLE : sa racine
      est prise sans vérification, et une variance négative fait lever la fonction —
      mesuré le 19-09-2026, « ValueError: math domain error ».
    ⑤ SORTIE — UNE valeur : un tableau, sous trois formes qui ne portent pas les
      mêmes cases. Quand le calcul aboutit, cinq cases : `dsr` entre 0 et 1 arrondi
      au millième, `sharpe_observe`, `sharpe_attendu_max_sous_H0`, `z_dsr` et
      `verdict`. Quand il y a moins de deux stratégies essayées ou moins de deux
      opérations, DEUX cases seulement : `dsr` valant 0 et `verdict` valant
      INSUFFISANT. Quand le dénominateur du calcul devient nul ou négatif, deux
      cases : `dsr` valant 0 et `verdict` valant INDÉFINI.
      [rend: 1]
    ⑥ TRAITEMENT — ① refuser moins de deux stratégies essayées ou moins de deux
      opérations · ② calculer le rapport que le pur hasard aurait produit au mieux
      sur le nombre d'essais donné, par la formule de Bailey et López de Prado, qui
      mêle deux points de la loi normale inverse pondérés par la constante d'Euler,
      0,5772156649 · ③ calculer le dénominateur de correction, qui tient compte de
      l'asymétrie et de l'épaisseur des queues · ④ refuser si ce dénominateur est nul
      ou négatif · ⑤ diviser l'écart entre le rapport observé et le rapport du hasard
      par ce dénominateur, en le multipliant par la racine du nombre d'opérations
      diminué de un · ⑥ transformer ce résultat en probabilité par la loi normale ·
      ⑦ poser le verdict EXCELLENT au-dessus de 0,95, BON au-dessus de 0,90,
      ACCEPTABLE au-dessus de 0,80, INSUFFISANT en dessous.
    ⑦ UNITÉ — `dsr` est une PROBABILITÉ entre 0 et 1. `sharpe_observe`,
      `sharpe_attendu_max_sous_H0` et `z_dsr` sont des rapports, donc SANS UNITÉ.
      `n_strategies_testees` est un NOMBRE DE STRATÉGIES, `n_trades` un NOMBRE
      D'OPÉRATIONS. `variance_sharpe_ensemble` est le CARRÉ d'un rapport, ce qui
      explique qu'on en prenne la racine. `skewness` et `kurtosis` sont sans unité,
      et la valeur 3 de la seconde correspond à une loi normale.
    ⑧ POURQUOI — La fonction imbriquée `phi_inv` calcule la loi normale inverse,
      dont Python ne livre pas la fonction toute faite. Elle est écrite en deux
      morceaux : une approximation de Beasley, Springer et Moro au centre de la loi,
      et la queue de Wichura AS241 sur les bords. Ce choix vient d'une correction du
      24-08-2026 : l'approximation employée auparavant dans les queues, la racine de
      l'opposé du logarithme du complément, voit son erreur CROÎTRE avec la
      probabilité demandée — donc elle était fausse précisément quand le nombre
      d'essais est grand, c'est-à-dire là où le dégonflage compte le plus. La version
      d'aujourd'hui est exacte à un cent-millionième.
      La partie basse de la loi est traitée par symétrie, en calculant la partie
      haute et en changeant le signe, parce que la loi normale inverse est impaire.
      Cette symétrie répond à un second défaut du même jour : la fonction rendait
      ZÉRO pour toute probabilité inférieure ou égale à 0,5, donc la moitié basse de
      la loi était MUETTE au lieu d'être fausse — le pire des cas, parce qu'un zéro
      ne se remarque pas.
    ⑨ CE QUI CLOCHE —
      ① UNE VARIANCE NULLE DONNE LE MEILLEUR VERDICT POSSIBLE. Si toutes les
      stratégies essayées ont le même rapport gain sur secousses, leur variance vaut
      zéro, le rapport attendu du hasard devient zéro lui aussi, et l'écart n'est
      plus dégonflé du tout. Mesuré le 19-09-2026 pour un rapport observé de 1,5, une
      variance de 0 et 100 opérations sur 100 essais : la fonction rend `dsr` valant
      1,0 et le verdict EXCELLENT, là où elle rend 0,945 avec une variance de 0,25.
      Le dégonflage disparaît sans qu'aucune case ne le signale.
      ② Une variance NÉGATIVE fait tomber la fonction. Sa racine est prise sans
      vérification, ligne 844. Mesuré le 19-09-2026 avec une variance de −0,25 :
      « ValueError: math domain error ». Le refus posé en tête ne regarde que le
      nombre de stratégies et le nombre d'opérations.
      ③ Les deux cas de refus rendent `dsr` valant 0, qui est aussi la PIRE valeur
      mesurable. Mesuré le 19-09-2026 avec une seule stratégie essayée : le tableau
      rendu est `{'dsr': 0, 'verdict': 'INSUFFISANT'}`. Or le critère C2 de la
      grille, qui exige au moins 0,95, prend par défaut la valeur 0 quand la case
      manque : « pas mesuré » et « très mauvais » aboutissent au même verdict, et
      rien ne les distingue.
      ④ Les trois sorties ne portent pas les mêmes cases. Mesuré le 19-09-2026, la
      branche qui aboutit rend cinq cases et les deux branches de refus n'en rendent
      que deux. Un appelant qui lit `z_dsr` ou `sharpe_attendu_max_sous_H0` tombe sur
      une case absente dès qu'un refus a eu lieu.
      ⑤ La moitié de la fonction imbriquée `phi_inv` est du code que rien ne peut
      atteindre. La partie basse de la loi est renvoyée par symétrie AVANT le calcul
      de l'écart au centre, donc cet écart n'est jamais négatif en dessous ; les
      deux branches écrites pour ce cas — le choix entre la probabilité et son
      complément, ligne 816, et le changement de signe final, ligne 841 — ne peuvent
      donc plus servir. Elles restent là, et laissent croire que le cas est traité
      deux fois.
      ⑥ La vérification « au moins deux stratégies essayées » est faite deux fois,
      ligne 775 puis ligne 843, la seconde étant devenue sans objet. De même, « au
      moins deux opérations » est vérifié ligne 775 puis de nouveau ligne 851.
      ⑦ Les trois seuils 0,95, 0,90 et 0,80 qui posent le verdict, lignes 859, 861 et
      863, sont écrits dans le corps de la fonction, hors de la table des seuils de
      ce fichier et hors du REGISTRE, alors que la règle du projet veut que les
      seuils vivent au REGISTRE et jamais dans le code — `gouvernance/
      REGISTRE_REGLES.md`, règle R-743, deuxième geste. Et le 0,95 de la ligne 859
      est le même nombre que le seuil du critère C2, écrit ligne 1732 : un chiffre qui
      existe ailleurs ne se recopie pas (R-708).
    ⑩ EFFET — Ne lit ni n'écrit aucun fichier, n'affiche rien, ne touche pas au
      réseau, ne modifie rien de ce qu'elle reçoit.
    ⑪ TERMINAISON — Rend la main par l'une de ses trois sorties dans le cas
      ordinaire. PEUT LEVER une erreur non rattrapée sur une variance négative, ce
      qui arrêterait le programme appelant avec une trace Python. Aucun de ses appels
      ne se termine : `phi_inv` est écrite ici et rend toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS
      une opération : un achat simulé suivi de sa revente, avec son gain net en
        euros ; aucun ordre réel n'est jamais passé
      le Sharpe : le rapport du gain moyen à sa dispersion, ramené à l'année
      le Sharpe dégonflé : le Sharpe corrigé du nombre de stratégies essayées ; plus
        on en essaie, plus un bon Sharpe peut n'être que du hasard
      la grille : la liste des huit critères et de leurs seuils ; celle qui tourne
        s'appelle GRILLE-26-04 et vit dans `CRITERES_VALIDATION_EXPERTS`, lignes 1730
        à 1740 de ce fichier
      la table des seuils : `CRITERES_VALIDATION_EXPERTS`, qui porte les neuf seuils
        et le sens de comparaison de chacun
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les
        règles numérotées du projet
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
    
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      un refus : une ligne du garde-fou qui ajoute un motif à sa liste de refus et fait donc rendre le code 1
      une stratégie : une règle qui dit QUOI acheter, avec son objectif de gain, sa perte acceptée et son horizon
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle a tourné — rapport de boucle, rapport d'audit, cockpit, historique des mesures.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    import math
    if n_strategies_testees < 2 or n_trades < 2:
        return {'dsr': 0, 'verdict': 'INSUFFISANT'}

    # Sharpe attendu maximum sous H0 (multiple testing) — formule Bailey-López de Prado
    # SR_0 = sqrt(V) × ((1 - γ) × Φ⁻¹(1 - 1/N) + γ × Φ⁻¹(1 - 1/(N×e)))
    # où γ ≈ 0.5772 (constante d'Euler-Mascheroni)
    gamma = 0.5772156649
    e = math.e
    N = n_strategies_testees
    V = variance_sharpe_ensemble

    # Approximation Φ⁻¹ via formule de Beasley-Springer-Moro pour les valeurs courantes
    def phi_inv(p):
        # Approximation Beasley-Springer-Moro pour Φ⁻¹, queue par Wichura AS241.
        # CORRIGÉ 24-08-2026 (défaut 5, RÉVÉLÉ PAR LE CALIBRAGE) : l'original
        # rendait 0 pour tout p <= 0.5, ce qui rend la moitié BASSE de la loi
        # inatteignable et donc muette au lieu d'être fausse — le pire cas.
        # Φ⁻¹ est impaire : Φ⁻¹(p) = −Φ⁻¹(1−p). On traite donc p < 0.5 par
        # symétrie plutôt que de rendre zéro.
        """Rend le point de la loi normale sous lequel tombe une proportion donnée.

        ① RÔLE — Traduire une probabilité en écart-type, opération dont le Sharpe
        dégonflé a besoin pour dire de combien un résultat dépasse ce que le hasard
        produirait. Sans elle, la mesure ne pourrait pas être calculée.
        ② CONTEXTE D'APPEL — Définie dans `calculer_deflated_sharpe` et appelée par elle,
        ainsi que par elle-même : les probabilités inférieures à un demi sont traitées en
        rappelant la fonction sur leur complément.
        ③ ENTRÉE — `p` : une probabilité, nombre compris entre zéro et un exclus.
        ④ CONDITIONS D'ENTRÉE — Aucune : les valeurs hors bornes sont traitées, pas
        refusées.
        ⑤ SORTIE — UNE valeur : le nombre d'écarts-type correspondant à `p`, zéro quand
        `p` sort de l'intervalle ouvert.
          [rend: 1]
        ⑥ TRAITEMENT — ① si `p` est hors de l'intervalle, rendre zéro · ② si `p` est
        inférieur à un demi, rendre l'opposé du résultat obtenu sur `1 - p`, la fonction
        étant impaire · ③ sinon appliquer l'approximation de Beasley-Springer-Moro au
        centre de la loi, et celle de Wichura dans la queue.
        ⑦ UNITÉ — L'entrée est une PROBABILITÉ, sans unité, entre zéro et un. La sortie
        est un nombre d'ÉCARTS-TYPE.
        ⑧ POURQUOI — Le traitement par symétrie a été ajouté le 24-08-2026, après que le
        calibrage a révélé que la version d'origine rendait zéro pour toute probabilité
        inférieure ou égale à un demi. **La moitié basse de la loi était donc inatteignable
        et muette au lieu d'être fausse, ce qui est le pire des deux cas** : un résultat
        faux se voit, un résultat absent se confond avec un résultat neutre.
        ⑨ CE QUI CLOCHE — Zéro est rendu pour les entrées hors bornes, et zéro est aussi
        une valeur légitime : c'est ce que rend une probabilité d'exactement un demi.
        L'appelant ne peut pas distinguer « la médiane » de « tu m'as donné n'importe
        quoi ». Relevé par lecture du code le 20-09-2026, non provoqué.
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend toujours la main. Son seul appel est un appel à elle-même,
        qui ne peut se produire qu'une fois : le second passage a une probabilité
        supérieure à un demi et n'entre plus dans cette branche.
          [sort: non]
        """
        if p <= 0 or p >= 1:
            return 0.0
        if p < 0.5:
            return -phi_inv(1 - p)
        a = [-3.969683028665376e+01, 2.209460984245205e+02,
             -2.759285104469687e+02, 1.383577518672690e+02,
             -3.066479806614716e+01, 2.506628277459239e+00]
        b = [-5.447609879822406e+01, 1.615858368580409e+02,
             -1.556989798598866e+02, 6.680131188771972e+01,
             -1.328068155288572e+01]
        q = p - 0.5
        if abs(q) <= 0.425:
            r = q * q
            return (((((a[0]*r + a[1])*r + a[2])*r + a[3])*r + a[4])*r + a[5]) * q / \
                   (((((b[0]*r + b[1])*r + b[2])*r + b[3])*r + b[4])*r + 1)
        # cas extrêmes
        # CORRIGÉ 24-08-2026 (défaut 2) : l'ancienne version rendait
        # sqrt(-ln(1-p)), une approximation dont l'erreur CROÎT avec p —
        # donc fausse précisément quand N est grand, c'est-à-dire quand le
        # nombre d'essais est élevé et que la déflation compte le plus.
        # Remplacée par la queue de Wichura (AS241), même famille que la
        # branche centrale déjà présente au-dessus.
        r = p if q < 0 else 1 - p
        if r <= 0:
            return 0.0
        r = math.sqrt(-math.log(r))
        if r <= 5:
            r -= 1.6
            num = ((((((7.7454501427834140764e-4*r + 0.0227238449892691845833)*r
                   + 0.24178072517745061177)*r + 1.27045825245236838258)*r
                   + 3.64784832476320460504)*r + 5.7694972214606914055)*r
                   + 4.6303378461565452959)*r + 1.42343711074968357734
            den = ((((((1.05075007164441684324e-9*r + 5.475938084995344946e-4)*r
                   + 0.0151986665636164571966)*r + 0.14810397642748007459)*r
                   + 0.68976733498510000455)*r + 1.6763848301838038494)*r
                   + 2.05319162663775882187)*r + 1.0
        else:
            r -= 5
            num = ((((((2.01033439929228813265e-7*r + 2.71155556874348757815e-5)*r
                   + 0.0012426609473880784386)*r + 0.026532189526576123093)*r
                   + 0.29656057182850489123)*r + 1.7848265399172913358)*r
                   + 5.4637849111641143699)*r + 6.6579046435011037772
            den = ((((((2.04426310338993978564e-15*r + 1.4215117583164458887e-7)*r
                   + 1.8463183175100546818e-5)*r + 7.868691311456132591e-4)*r
                   + 0.0148753612908506148525)*r + 0.13692988092273580531)*r
                   + 0.59983220655588793769)*r + 1.0
        val = num / den
        return -val if q < 0 else val

    if N >= 2:
        sr0 = math.sqrt(V) * ((1 - gamma) * phi_inv(1 - 1/N) + gamma * phi_inv(1 - 1/(N * e)))
    else:
        sr0 = 0

    # DSR (déflation)
    # DSR = Φ((SR_obs - SR_0) × sqrt(N - 1) / sqrt(1 - skew × SR_obs + (kurt-1)/4 × SR_obs²))
    denom2 = 1 - skewness * sharpe_observe + (kurtosis - 1) / 4 * sharpe_observe ** 2
    if denom2 <= 0 or n_trades < 2:
        return {'dsr': 0, 'verdict': 'INDÉFINI'}

    z_dsr = (sharpe_observe - sr0) * math.sqrt(n_trades - 1) / math.sqrt(denom2)

    # Φ(z) via erf
    dsr = (1 + math.erf(z_dsr / math.sqrt(2))) / 2

    if dsr >= 0.95:
        verdict = 'EXCELLENT'
    elif dsr >= 0.90:
        verdict = 'BON'
    elif dsr >= 0.80:
        verdict = 'ACCEPTABLE'
    else:
        verdict = 'INSUFFISANT'

    return {
        'dsr': round(dsr, 3),
        'sharpe_observe': round(sharpe_observe, 3),
        'sharpe_attendu_max_sous_H0': round(sr0, 3),
        'z_dsr': round(z_dsr, 3),
        'verdict': verdict,
    }


def calculer_time_underwater(trades: list, capital: float = 100_000) -> dict:
    """Mesure la pire chute du cumul des gains et le temps qu'il faut pour en sortir.

    ① RÔLE — Donner au quatrième critère de la grille ses DEUX chiffres, et donner
      au juge des stratégies la ligne « PIRE CREUX » de son rapport. Une stratégie qui
      gagne à la fin peut avoir été très longtemps en perte au milieu, et c'est ce
      qu'un investisseur vit réellement. La fonction empile les gains des opérations
      dans l'ordre des dates, suit la courbe obtenue, et relève deux choses : de
      combien cette courbe est descendue au plus bas sous son plus haut précédent, et
      combien de jours elle a passé sous ce plus haut. Mesuré le 19-09-2026 sur
      20 opérations fabriquées, douze gagnantes à 400 € et huit perdantes à 250 € :
      la pire chute est de 500 €, soit 0,5 % du capital, et le plus long passage sous
      le plus haut dure 3 jours.
    ② CONTEXTE D'APPEL — Deux appelants, la fonction la plus employée de ce fichier.
      ① `programmes/JUGE_DES_STRATEGIES.py`, fonction `juger`, qui en tire la ligne « PIRE CREUX » de
      son rapport et ne lui passe pas de capital, donc laisse la valeur par défaut de
      100 000 €. ② `programmes/JUGER_SUR_8_CRITERES.py`, dans sa fonction
      `mesures_disponibles`, qui lui passe un capital explicite et en tire les cases
      `dd_pct` et `underwater_jours` du tableau des mesures.
    ③ ENTRÉE — `trades` : la liste des opérations, chacune étant un tableau portant
      `date`, écrite année-mois-jour, et `gain`, en euros. Les deux appelants
      construisent cette liste en renommant leurs propres cases : `JUGE_DES_STRATEGIES.py`
      écrit `{"date": o["date_signal"], "gain": o["net"]}`, et
      `JUGER_SUR_8_CRITERES.py` écrit la même chose. `capital` : le capital de
      référence servant à dire la chute en pourcent, 100 000 € quand rien n'est
      précisé.
    ④ CONDITIONS D'ENTRÉE — Aucune : une liste vide, une date mal écrite ou une case
      `gain` absente ne la font pas tomber. La liste n'a pas besoin d'être triée,
      elle l'est ici. Le capital doit être différent de zéro, faute de quoi la
      division qui donne le pourcent lèverait — mais aucun appelant ne passe zéro.
    ⑤ SORTIE — UNE valeur : un tableau de QUATRE cases, mais LES DEUX BRANCHES NE
      RENDENT PAS LES MÊMES. Quand la liste porte des opérations : `dd_max_eur`,
      `dd_max_pct`, `time_underwater_max_jours` et `time_underwater_total_jours`.
      Quand la liste est vide : `dd_max_eur`, `dd_max_pct`,
      `time_underwater_max_jours` et `time_underwater_jours` — cette dernière case
      n'existe nulle part ailleurs, et `time_underwater_total_jours` manque.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre des zéros si la liste est vide · ② trier les opérations
      par leur date, écrite comme un texte · ③ parcourir la liste en ajoutant chaque
      gain à un cumul · ④ si le cumul dépasse son plus haut précédent, refermer le
      creux en cours, ajouter sa durée au total, et retenir le nouveau plus haut avec
      sa date · ⑤ sinon, calculer l'écart au plus haut, le retenir s'il est le pire
      vu, ouvrir un creux s'il n'y en avait pas, et retenir la durée écoulée depuis
      le début de ce creux si elle est la plus longue vue · ⑥ rendre les quatre
      chiffres.
    ⑦ UNITÉ — `dd_max_eur` est en EUROS, arrondi à l'unité. `dd_max_pct` est un
      POURCENT du capital de référence, arrondi au dixième : 0,5 signifie un demi-
      pourcent, et non une fraction. `time_underwater_max_jours` et
      `time_underwater_total_jours` sont des NOMBRES DE JOURS DE CALENDRIER, pas des
      séances de bourse : un creux qui traverse un week-end compte ces deux jours.
      `capital` est en EUROS.
    ⑧ POURQUOI — La chute est ramenée à un capital FIXE de 100 000 € et non au cumul
      du moment, parce que la règle du projet est qu'un seul montant de 100 000 € est
      engagé par opération, toujours le même : la chute en pourcent se lit alors
      directement comme une part du montant risqué. Un rapport au cumul donnerait un
      pourcent qui change de sens selon le moment de la courbe.
      La durée d'un creux se compte à partir de la date du DERNIER PLUS HAUT, et non
      de la première opération perdante : le creux commence au sommet, pas au premier
      pas de la descente. C'est cette convention qui rend le chiffre comparable au
      seuil du critère C4b, qui exige moins de 365 jours.
    ⑨ CE QUI CLOCHE —
      ① LES DEUX BRANCHES RENDENT DES CASES DIFFÉRENTES, ET L'UNE PORTE UN NOM QUI
      N'EXISTE NULLE PART AILLEURS. Mesuré le 19-09-2026 : sur 20 opérations, les
      cases rendues sont `dd_max_eur`, `dd_max_pct`, `time_underwater_max_jours` et
      `time_underwater_total_jours` ; sur une liste vide, ce sont `dd_max_eur`,
      `dd_max_pct`, `time_underwater_jours` et `time_underwater_max_jours`. La case
      `time_underwater_jours` n'apparaît que dans la branche vide, et
      `time_underwater_total_jours` n'apparaît que dans l'autre. Un appelant qui lit
      la durée totale sur une liste vide tombe sur une case absente.
      ② LA DURÉE TOTALE OUBLIE LE CREUX QUI N'EST PAS ENCORE REFERMÉ. La durée n'est
      ajoutée au total qu'au moment où la courbe repasse au-dessus de son plus haut.
      Une stratégie qui finit en perte n'a donc jamais refermé son dernier creux, et
      celui-ci ne compte pas. Mesuré le 19-09-2026 sur trois opérations — un gain de
      1 000 € le 1er janvier, puis deux pertes le 1er mars et le 1er juin — la
      fonction rend `time_underwater_max_jours` valant 151 et
      `time_underwater_total_jours` valant 0. Le total annonce zéro jour sous l'eau
      pour une stratégie qui y a passé cinq mois et n'en est pas sortie.
      ③ Les cases que rend cette fonction ne sont pas celles que son texte d'origine
      annonçait. Le texte promettait `dd_max_eur, dd_max_pct, time_underwater_jours,
      time_underwater_max_jours`, et la branche qui aboutit rend
      `time_underwater_total_jours` à la place de la troisième. Ce n'est pas sans
      conséquence : le 13-09-2026, `programmes/JUGER_SUR_8_CRITERES.py` avait deviné
      les noms `dd_pct` et `underwater_jours` au lieu de les relever, les deux
      rendaient vide, et un vide se lit comme un critère non passé. Le code de ce
      programme en porte encore le commentaire, dans sa fonction `mesures_disponibles` :
      « On ne devine pas une cle. »
      ④ UN CUMUL EXACTEMENT REVENU À SON SOMMET N'EN SORT PAS. La comparaison de la
      ligne 1029 est stricte : à égalité, la fonction reste dans la branche du creux
      et le creux n'est pas refermé. Mesuré le 19-09-2026 sur quatre opérations —
      +1 000 € le 1er janvier, −500 € le 1er février, +500 € le 1er mars, +500 € le
      1er septembre — le cumul est revenu à son sommet de 1 000 € dès le 1er mars, et
      la fonction rend pourtant `time_underwater_total_jours` valant 243, c'est-à-dire
      le 1er janvier au 1er septembre. La perte n'a duré que 59 jours, ce que la case
      `time_underwater_max_jours` dit correctement. Les deux chiffres du même tableau
      se contredisent donc, et c'est le plus gros qui est faux.
      ⑤ Les dates sont triées COMME DES TEXTES, jamais comme des dates. L'écriture
      année-mois-jour fait que les deux ordres coïncident, mais une date écrite
      autrement — jour-mois-année, par exemple — serait triée de travers sans qu'une
      erreur apparaisse, et le parcours du cumul se ferait dans le désordre.
      ⑥ Une opération dont la date ne se lit pas est SAUTÉE en silence, et son gain
      est perdu pour le cumul. Le rattrapage d'erreur de la ligne 1025 n'a pas de nom
      et avale tout. Une liste dont toutes les dates seraient mal écrites rendrait
      quatre zéros, exactement comme une liste vide.
      ⑦ Le pourcent de chute est rapporté au capital d'UNE opération, 100 000 €,
      alors que la chute qu'il mesure est celle d'un CUMUL de plusieurs opérations.
      Sur une longue série, la chute en euros peut dépasser 100 000 € et le pourcent
      dépasser cent, sans que le chiffre veuille dire ce qu'un lecteur attend d'un
      pourcent.
    ⑩ EFFET — Ne lit ni n'écrit aucun fichier, n'affiche rien, ne touche pas au
      réseau. Elle ne modifie pas la liste qu'elle reçoit : le tri produit une
      nouvelle liste.
    ⑪ TERMINAISON — Rend toujours la main, par l'une de ses deux sorties. Elle ne
      lève pas dans les conditions d'appel d'aujourd'hui : la lecture des dates est
      rattrapée, et les deux appelants passent un capital non nul. Elle n'appelle
      aucune fonction du projet.
      [sort: non]
    ⑫ DÉFINITIONS
      une opération : un achat simulé suivi de sa revente, avec son gain net en
        euros ; aucun ordre réel n'est jamais passé
      la durée sous l'eau : le nombre de jours pendant lesquels le cumul des gains
        reste sous son plus haut précédent
      le creux : la période qui va d'un plus haut du cumul jusqu'au moment où ce plus
        haut est dépassé de nouveau
      la grille : la liste des huit critères et de leurs seuils ; celle qui tourne
        s'appelle GRILLE-26-04 et vit dans `CRITERES_VALIDATION_EXPERTS`, lignes 1730
        à 1740 de ce fichier
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur
        l'historique des cours et rend la liste de ses opérations
    
      la pire chute : la plus forte baisse du cumul depuis un sommet precedent.
      une fraction : la façon d'écrire un pourcentage entre 0 et 1 — 0,040 pour +4 % — par opposition au pourcent, qui écrirait 4.0
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if not trades:
        return {'dd_max_eur': 0, 'dd_max_pct': 0, 'time_underwater_jours': 0,
                'time_underwater_max_jours': 0}

    from datetime import datetime as _dt
    trades_tries = sorted(trades, key=lambda t: t.get('date', ''))

    cum = 0
    peak = 0
    peak_date = None
    dd_max_eur = 0
    dd_max_pct = 0
    underwater_actuel = 0  # jours
    underwater_max = 0
    underwater_total_jours = 0
    in_drawdown = False
    debut_dd = None

    for t in trades_tries:
        try:
            d = _dt.strptime(t['date'], '%Y-%m-%d')
        except:
            continue
        cum += t.get('gain', 0)

        if cum > peak:
            # Nouveau plus haut → on sort du drawdown
            if in_drawdown:
                duree = (d - debut_dd).days
                underwater_total_jours += duree
                in_drawdown = False
            peak = cum
            peak_date = d
        else:
            # En drawdown
            dd = peak - cum
            if dd > dd_max_eur:
                dd_max_eur = dd
                dd_max_pct = dd / capital * 100
            if not in_drawdown:
                in_drawdown = True
                debut_dd = peak_date if peak_date else d
            underwater_actuel = (d - debut_dd).days if debut_dd else 0
            if underwater_actuel > underwater_max:
                underwater_max = underwater_actuel

    return {
        'dd_max_eur': round(dd_max_eur, 0),
        'dd_max_pct': round(dd_max_pct, 1),
        'time_underwater_max_jours': underwater_max,
        'time_underwater_total_jours': underwater_total_jours,
    }


def calculer_kelly_fractionnel(wr_pct: float, tp: float, sl: float,
                                 frais_pct: float = 0.0025, fraction: float = 0.25) -> dict:
    """Dit quelle part du capital il serait raisonnable d'engager sur une opération.

    ① RÔLE — Donner au cinquième critère de la grille le chiffre qu'il compare à son
      seuil, et dire si la stratégie gagne de l'argent une fois les frais payés. La
      formule de Kelly répond à une question précise : connaissant le taux de
      réussite et le rapport entre ce qu'on gagne quand ça marche et ce qu'on perd
      quand ça ne marche pas, quelle part du capital faut-il engager pour faire
      croître ce capital le plus vite possible sans le ruiner ? Le chiffre brut est
      ensuite réduit d'une fraction, parce que la formule complète suppose des
      grandeurs connues avec certitude, ce qui n'est jamais le cas. Mesuré le
      19-09-2026 pour un taux de réussite de 63,1 %, un objectif de gain de 4 %, une
      perte acceptée de 2,5 % et le taux de frais réel de 0,0015 : la formule brute
      rend 0,851 et la version réduite de moitié 0,0943. Le critère C5, qui exige au
      moins 0,05, est passé.
    ② CONTEXTE D'APPEL — Un seul appelant, `programmes/JUGER_SUR_8_CRITERES.py`,
      dans sa fonction `mesures_disponibles`, une fois par stratégie
      mesurée. Il en retient la seule case `kelly_fractionnel`.
    ③ ENTRÉE — `wr_pct` : le taux de réussite EN POURCENT, non arrondi. `tp` :
      l'objectif de gain, EN FRACTION, 0,04 pour 4 %. `sl` : la perte acceptée, EN
      FRACTION ET SANS SON SIGNE, 0,025 pour −2,5 %. `frais_pct` : le taux de frais
      par ordre, EN FRACTION, 0,0025 quand rien n'est précisé. `fraction` : la part
      de la formule brute à retenir, 0,25 quand rien n'est précisé. Son seul appelant
      lui passe l'objectif et la perte lus sur la fiche de la stratégie et convertis
      en fractions, le taux de frais qu'il est allé lire dans
      `MODULE_POSITIONS.FRAIS_TAUX` — 0,0015, relevé le 19-09-2026 — et la valeur 0,5
      à la place du quart.
    ④ CONDITIONS D'ENTRÉE — La perte acceptée augmentée des frais doit être
      STRICTEMENT POSITIVE, sinon la fonction refuse. Les trois grandeurs `tp`, `sl`
      et `frais_pct` doivent être exprimées dans la MÊME unité, la fraction, faute de
      quoi le rapport calculé n'a aucun sens. `sl` doit être donné SANS son signe :
      une perte écrite −0,025 rendrait la perte nette négative et ferait prendre la
      branche de refus.
    ⑤ SORTIE — UNE valeur : un tableau, sous deux formes qui ne portent pas les mêmes
      cases. Quand le calcul aboutit, CINQ cases : `kelly_brut`,
      `kelly_fractionnel`, `b_ratio`, `esperance_par_trade` et `esperance_pct`. Quand
      la perte nette est nulle ou négative, CINQ cases également, mais
      `esperance_pct` est remplacée par `erreur` valant « Perte unitaire <= 0 » — et
      les quatre autres valent 0.
      [rend: 1]
    ⑥ TRAITEMENT — ① ramener le taux de réussite de pourcent en fraction · ②
      calculer le gain net d'une opération gagnante, l'objectif diminué des frais ·
      ③ calculer la perte nette d'une opération perdante, la perte acceptée augmentée
      des frais · ④ refuser si cette perte nette est nulle ou négative · ⑤ calculer
      le rapport du gain net à la perte nette · ⑥ appliquer la formule de Kelly, qui
      est ce rapport multiplié par le taux de réussite, diminué du taux d'échec, le
      tout divisé par ce rapport · ⑦ multiplier par la fraction demandée · ⑧
      calculer l'espérance d'une opération, le gain net pondéré par le taux de
      réussite moins la perte nette pondérée par le taux d'échec · ⑨ rendre les cinq
      chiffres arrondis.
    ⑦ UNITÉ — `wr_pct` est un POURCENT : 63,1 et non 0,631. `tp`, `sl`, `frais_pct`,
      `fraction`, `kelly_brut` et `kelly_fractionnel` sont des FRACTIONS du capital,
      entre 0 et 1 : 0,0943 veut dire 9,43 % du capital. `b_ratio` est un rapport de
      deux fractions, donc SANS UNITÉ. `esperance_par_trade` est une FRACTION du
      capital engagé sur une opération, et `esperance_pct` le même chiffre en
      POURCENT. Sur les 100 000 € engagés par opération dans ce projet, une espérance
      de 0,01451 vaut donc 1 451 € par opération.
    ⑧ POURQUOI — Les frais sont retirés du gain ET ajoutés à la perte, et non
      comptés une seule fois, parce qu'un aller-retour se paie deux fois : une fois à
      l'achat, une fois à la revente. Le tarif du projet est de 0,15 % par ordre —
      `MODULE_POSITIONS.FRAIS_TAUX` vaut 0,0015, tarif Fortuneo PROGRESS.
      La formule complète de Kelly est réduite d'une fraction parce qu'elle suppose
      le taux de réussite et le rapport gain sur perte connus exactement. Ils sont
      ici ESTIMÉS sur un nombre fini d'opérations, et une estimation trop optimiste
      fait engager trop, ce qui ruine plus vite que la formule ne fait gagner. Le
      quart est la valeur d'usage de la littérature ; le seul appelant retient la
      moitié.
    ⑨ CE QUI CLOCHE —
      ① LE TAUX DE FRAIS PAR DÉFAUT N'EST PAS LE TARIF DU PROJET, ET IL EST TROIS
      FOIS ET DEMIE TROP GRAND. La signature pose `frais_pct` à 0,0025, soit 25
      points de base, alors que le tarif réellement appliqué est de 0,0015, soit 15
      points de base — `MODULE_POSITIONS.FRAIS_TAUX`, le tarif Fortuneo PROGRESS.
      Mesuré le 19-09-2026 pour un taux de réussite de 63,1 %, un objectif de 4 % et
      une perte acceptée de 2,5 % : avec la valeur par défaut, la version réduite
      rend 0,0901 ; avec le tarif réel, 0,0943. L'écart est de 4,7 %, et il va dans
      le sens pessimiste, donc il ne se remarque pas. Le seul appelant d'aujourd'hui
      passe le tarif réel et n'est pas touché, mais un appelant qui ferait confiance
      à la valeur par défaut le serait. Un chiffre qui existe ailleurs ne se recopie
      pas (R-708) : ce taux-ci a déjà été recopié faux, le 13-09-2026, à 0,005 dans
      `programmes/JUGER_SUR_8_CRITERES.py`, ce qui déplaçait le Kelly de 19,8 %.
      ② Le nom `frais_pct` annonce un pourcent et porte une fraction. Dans ce même
      fichier, `dd_max_pct` porte bien un pourcent et `esperance_pct` aussi : le même
      suffixe désigne donc deux grandeurs qui diffèrent d'un facteur cent, dans deux
      fonctions voisines.
      ③ LE CHIFFRE RENDU PEUT ÊTRE NÉGATIF, ET RIEN NE LE SIGNALE. Une stratégie qui
      perd de l'argent donne un Kelly négatif, ce qui veut dire en toute rigueur
      qu'il faudrait parier dans l'autre sens. Mesuré le 19-09-2026 pour un taux de
      réussite de 30 %, un objectif de 4 % et une perte acceptée de 2,5 % : la
      fonction rend `kelly_fractionnel` valant −0,0455, sans aucune case pour le
      dire. Le critère C5, qui exige au moins 0,05, rejette bien ce chiffre, mais
      aucun appelant n'est averti que la valeur rendue n'a pas le sens d'une part de
      capital.
      ④ Les deux sorties ne portent pas les mêmes cases : la branche de refus rend
      `erreur` à la place d'`esperance_pct`. Mesuré le 19-09-2026 avec une perte
      acceptée et des frais tous deux nuls. Un appelant qui lit `esperance_pct` tombe
      sur une case absente dès qu'un refus a eu lieu.
      ⑤ Le refus rend `kelly_fractionnel` valant 0, qui est aussi une valeur
      parfaitement mesurable : un Kelly de zéro veut dire « n'engager rien ». Rien
      dans le chiffre ne dit s'il vient d'un calcul ou d'un renoncement.
      ⑥ La fonction ne vérifie pas que ses trois grandeurs sont bien des fractions.
      Mesuré le 19-09-2026 en passant l'objectif de gain en POURCENT, 4 au lieu de
      0,04, tout le reste inchangé : la fonction rend un rapport gain sur perte de
      150,887, un Kelly réduit de 0,3143 et une espérance de 251,328 %. Elle conseille
      donc d'engager près d'un tiers du capital sur la foi d'une espérance de
      251 % par opération, sans une erreur et sans un avertissement, et le critère C5
      est passé haut la main.
    ⑩ EFFET — Ne lit ni n'écrit aucun fichier, n'affiche rien, ne touche pas au
      réseau, ne modifie rien de ce qu'elle reçoit.
    ⑪ TERMINAISON — Rend toujours la main, par l'une de ses deux sorties. Elle ne
      lève pas : la seule division risquée, par la perte nette, est précédée du
      contrôle qui refuse une perte nette nulle ou négative. Elle n'appelle aucune
      fonction du projet.
      [sort: non]
    ⑫ DÉFINITIONS
      une opération : un achat simulé suivi de sa revente, avec son gain net en
        euros ; aucun ordre réel n'est jamais passé
      le taux de réussite : la part des opérations qui se sont refermées sur un gain,
        écrite en pourcent
      le Kelly fractionnel : la part du capital qu'il serait raisonnable d'engager
        sur une opération, compte tenu du taux de réussite et des gains et pertes
        attendus
      l'objectif de gain : le pourcentage de hausse à partir duquel la position se
        referme sur un gain
      la perte acceptée : le pourcentage de baisse à partir duquel la position se
        referme sur une perte
      la fiche : la ligne d'une stratégie au registre des stratégies
        `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte acceptée,
        son horizon et son univers
      la grille : la liste des huit critères et de leurs seuils ; celle qui tourne
        s'appelle GRILLE-26-04 et vit dans `CRITERES_VALIDATION_EXPERTS`, lignes 1730
        à 1740 de ce fichier
      un point de base : un centième de pourcent ; 15 points de base valent 0,15 %
    
      l'espérance : le résultat moyen d'une opération, en euros
      un refus : une ligne du garde-fou qui ajoute un motif à sa liste de refus et fait donc rendre le code 1
      une fraction : la façon d'écrire un pourcentage entre 0 et 1 — 0,040 pour +4 % — par opposition au pourcent, qui écrirait 4.0
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    p = wr_pct / 100
    q = 1 - p
    # Gain net moyen sur WIN = TP - frais ; perte nette moyenne sur LOSS = SL + frais
    gain_unitaire = tp - frais_pct
    perte_unitaire = sl + frais_pct
    if perte_unitaire <= 0:
        return {'kelly_brut': 0, 'kelly_fractionnel': 0, 'b_ratio': 0, 'esperance_par_trade': 0,
                'erreur': 'Perte unitaire <= 0'}
    b = gain_unitaire / perte_unitaire  # ratio gain/perte
    # Kelly = (p × b - q) / b
    kelly = (p * b - q) / b
    kelly_frac = kelly * fraction
    esperance = p * gain_unitaire - q * perte_unitaire

    return {
        'kelly_brut': round(kelly, 4),
        'kelly_fractionnel': round(kelly_frac, 4),
        'b_ratio': round(b, 3),
        'esperance_par_trade': round(esperance, 5),
        'esperance_pct': round(esperance * 100, 3),
    }


def calculer_stabilite_parametrique(fonction_backtest, params_base: dict,
                                     pourcentage: float = 0.10, n_variations: int = 5) -> dict:
    """Rejoue la stratégie avec des réglages voisins et regarde si le gain s'effondre.

    ① RÔLE — Distinguer une stratégie posée sur une colline d'une stratégie posée
      sur une aiguille. Une stratégie sur une colline tient encore quand on bouge un
      peu ses réglages : le gain baisse sans disparaître. Une stratégie sur une
      aiguille s'effondre au premier pas de côté — elle ne décrivait pas le marché,
      elle collait à un jeu de données précis. La fonction prend les réglages
      d'origine, en tire plusieurs jeux voisins en faisant varier chaque nombre de
      ±10 % au hasard, demande à son appelant de rejouer la stratégie avec chacun, et
      compare les gains obtenus. Elle donne ainsi au sixième critère de la grille son
      seul chiffre.
    ② CONTEXTE D'APPEL — Deux appelants. ① `programmes/JUGE_DES_STRATEGIES.py`, fonction `juger`,
      qui en tire la ligne « VOISINAGE » de son rapport et les mots COLLINE ou
      AIGUILLE, et qui lui passe l'objectif de gain, la perte acceptée et l'horizon,
      avec cinq variations. ② `programmes/JUGER_SUR_8_CRITERES.py`, fonction `mesures_disponibles`, qui
      lui passe l'objectif de gain et la perte acceptée seulement, avec quatre
      variations, et n'en retient que la case `stable`. CE SECOND APPEL N'A JAMAIS
      LIEU : ce programme n'appelle cette fonction que si une façon de rejouer lui a
      été fournie, et mesuré le 19-09-2026, ses deux seules lignes d'appel à la
      fonction qui la transmet — lignes 474 et 1208 — passent une valeur VIDE à cette
      place. Le seul appel réel est donc celui de `JUGE_DES_STRATEGIES.py`.
    ③ ENTRÉE — `fonction_backtest` : une façon de rejouer la stratégie, fournie par
      l'appelant ; elle reçoit un jeu de réglages et rend un tableau portant le gain
      sous le nom `net_a` ou `net`. `params_base` : les réglages d'origine, par
      exemple `{"tp": 0.04, "sl": 0.025, "horizon": 20.0}` pour `JUGE_DES_STRATEGIES.py`.
      `pourcentage` : l'amplitude de la variation, 0,10 quand rien n'est précisé, et
      0,10 est aussi ce que les deux appelants passent. `n_variations` : le nombre de
      jeux voisins à essayer, 5 quand rien n'est précisé ; `JUGE_DES_STRATEGIES.py` passe 5 et
      `JUGER_SUR_8_CRITERES.py` passe 4.
    ④ CONDITIONS D'ENTRÉE — La façon de rejouer doit exister et être appelable : la
      fonction l'appelle une première fois SANS rien rattraper, et une valeur vide y
      ferait lever. Elle doit rendre un tableau portant `net_a` ou `net`. Les
      réglages doivent porter au moins un nombre, sans quoi aucune variation n'est
      possible et tous les jeux voisins sont identiques à l'original.
    ⑤ SORTIE — UNE valeur : un tableau de SEPT cases, toujours les mêmes :
      `net_base`, `net_min`, `net_max`, `net_moyen`, `ecart_relatif`, `stable` et
      `n_variations`. Il n'y a pas de seconde forme : ou bien le tableau est rendu,
      ou bien la fonction lève.
      [rend: 1]
    ⑥ TRAITEMENT — ① fixer la graine du tirage au hasard à 42 · ② rejouer la
      stratégie avec les réglages d'origine et relever son gain · ③ retenir les
      réglages qui sont des nombres, en écartant ceux nommés `capital` et `frais` ·
      ④ pour chaque variation demandée, tirer au hasard un écart entre −10 % et
      +10 % de chaque réglage retenu, en arrondissant à l'entier et sans descendre
      sous un pour les réglages entiers · ⑤ rejouer avec ce jeu voisin, et passer au
      suivant sans rien dire si le rejeu tombe · ⑥ relever le plus petit gain, le
      plus grand et la moyenne · ⑦ diviser l'étendue des gains par la valeur absolue
      de la moyenne · ⑧ déclarer le réglage stable si ce rapport est inférieur à 0,5
      ET que le plus petit gain reste positif · ⑨ rendre les sept chiffres.
    ⑦ UNITÉ — `net_base`, `net_min`, `net_max` et `net_moyen` sont des EUROS,
      arrondis à l'unité. `pourcentage` est une FRACTION : 0,10 pour ±10 %.
      `ecart_relatif` est un RAPPORT sans unité, arrondi au millième : 0,3 veut dire
      que l'étendue des gains vaut trois dixièmes du gain moyen. `n_variations` en
      entrée est un NOMBRE DE JEUX VOISINS DEMANDÉS, et `n_variations` en sortie est
      un NOMBRE DE REJEUX RÉELLEMENT ABOUTIS — les deux portent le même nom et ne
      comptent pas la même chose. `stable` vaut vrai ou faux. Les réglages
      eux-mêmes portent l'unité que leur donne l'appelant : l'objectif de gain et la
      perte acceptée sont des fractions, l'horizon un nombre de séances de bourse.
    ⑧ POURQUOI — La graine du tirage au hasard est fixée pour que deux passages sur
      les mêmes données rendent exactement le même verdict. Sans elle, une stratégie
      déclarée stable un jour pourrait être déclarée instable le lendemain sans que
      rien n'ait changé, et aucun calibrage ne serait possible.
      Les réglages nommés `capital` et `frais` sont écartés de la variation parce que
      ce ne sont pas des réglages de la stratégie : ce sont des données du monde. Le
      capital engagé est une décision, 100 000 € par opération, et le taux de frais
      est le tarif du courtier, 0,15 % par ordre. Les faire varier mesurerait la
      sensibilité au courtier, pas la solidité de la stratégie.
      Le verdict exige DEUX choses à la fois, un écart contenu ET un plus petit gain
      qui reste positif, parce qu'un écart faible ne prouve rien s'il est faible
      autour d'une perte : une stratégie qui perd régulièrement la même somme a un
      écart minuscule.
      Enfin, ces variantes sont des ESSAIS et doivent être comptées comme telles dans
      le nombre de stratégies essayées, faute de quoi le dégonflage du Sharpe
      sous-estime le nombre de tentatives.
    ⑨ CE QUI CLOCHE —
      ① ELLE ÉCRASE LA GRAINE DU HASARD DE TOUT LE PROGRAMME APPELANT. La ligne 1366
      appelle `random.seed(42)`, qui touche le tirage commun à tout le processus, et
      non un tirage qui lui serait propre. Mesuré le 19-09-2026 : après
      `random.seed(7)`, le tirage suivant rend 0,32383276 si cette fonction n'a pas
      été appelée, et 0,42192181 si elle l'a été. Un programme qui aurait fixé sa
      propre graine pour être reproductible cesse de l'être dès qu'il appelle cette
      fonction, et rien ne l'en avertit. La fonction `calculer_pbo`, dans ce même
      fichier, fait le contraire : elle se crée un tirage à elle.
      ② UN RÉGLAGE STABLE EST DÉCLARÉ STABLE MÊME QUAND AUCUNE VARIATION N'A PU ÊTRE
      ESSAYÉE. Les rejeux qui tombent sont sautés en silence. Mesuré le 19-09-2026
      avec une façon de rejouer qui aboutit la première fois puis lève ensuite : la
      fonction rend `stable` valant vrai, `ecart_relatif` valant 0,0 et
      `n_variations` valant 0. Le verdict « stable » est donc rendu sur la foi d'un
      seul gain, celui des réglages d'origine, et il faut regarder la case
      `n_variations` pour s'en apercevoir. Le seul appelant qui lit cette fonction
      aujourd'hui, `programmes/JUGER_SUR_8_CRITERES.py`, ne retient que `stable`.
      ③ UN RÉGLAGE VRAI OU FAUX EST TRAITÉ COMME UN NOMBRE ET VARIÉ. En Python, vrai
      et faux sont des entiers, ce que le tri des réglages ne vérifie pas. Mesuré le
      19-09-2026 avec les réglages `{"tp": 0.04, "mode": True}` : la façon de rejouer
      reçoit `mode` valant vrai au premier appel, puis l'entier 1 aux suivants. Aucun
      appelant d'aujourd'hui ne passe de réglage vrai ou faux, mais rien n'empêche
      qu'il en passe un.
      ④ LE TRI DES RÉGLAGES ÉPELLE DEUX NOMS AU LIEU DE PORTER SUR UNE PROPRIÉTÉ. Il
      écarte les réglages nommés exactement `capital` et `frais`. Le critère qui
      tranche tient en une question : si je renomme un réglage, mon contrôle
      change-t-il d'avis ? Ici oui, donc il épelle. Un réglage nommé `frais_pct`,
      `taux_de_frais` ou `capital_engage` serait varié de ±10 %, et le rapport
      mesurerait alors la sensibilité au tarif du courtier en croyant mesurer la
      solidité de la stratégie.
      ⑤ LE SEUIL DU VERDICT EST ÉCRIT DANS LE CORPS, ET PAS DANS LA TABLE. Les deux
      conditions de la ligne 1405, un rapport inférieur à 0,5 et un plus petit gain
      strictement positif, ne viennent ni de la table des seuils de ce fichier ni du
      REGISTRE. La table porte bien une entrée `C6_stabilite`, ligne 1737, avec un
      seuil « vrai » — mais ce seuil ne sert à rien, puisque le vrai ou faux est déjà
      décidé ici. La règle du projet veut que les seuils vivent au REGISTRE et jamais
      dans le code — `gouvernance/REGISTRE_REGLES.md`, règle R-743, deuxième geste.
      ⑥ La façon de rejouer est appelée SANS RATTRAPAGE la première fois, ligne 1368,
      et AVEC rattrapage les fois suivantes, ligne 1386. La même erreur arrête donc la
      fonction ou passe inaperçue selon le moment où elle survient.
      ⑦ Le gain est cherché sous DEUX noms, `net_a` d'abord puis `net`, sans qu'aucune
      phrase ne dise lequel fait foi ni pourquoi il y en a deux. Mesuré le
      19-09-2026, le nom `net_a` ne se trouve nulle part ailleurs : une recherche
      dans tous les fichiers `.py` du dépôt, `archives/` mis à part, ne rend aucune
      ligne hors de ce fichier. La façon de rejouer que `programmes/JUGE_DES_STRATEGIES.py`
      construit, ligne 520, rend `net`. Le premier nom cherché est donc mort, et un
      lecteur qui voit deux noms croit que deux appelants existent.
      ⑧ Un réglage qui vaut ZÉRO ne varie jamais : l'écart tiré est proportionnel à
      la valeur du réglage, donc nul. Un réglage nul est donc compté comme varié
      alors qu'il ne l'est pas, et `n_variations` l'inclut quand même.
    ⑩ EFFET — Ne lit ni n'écrit aucun fichier, n'affiche rien, ne touche pas au
      réseau. ELLE MODIFIE LA GRAINE DU TIRAGE AU HASARD COMMUNE À TOUT LE PROCESSUS
      APPELANT, en la fixant à 42. Elle ne modifie pas les réglages qu'elle reçoit :
      chaque jeu voisin est une copie. Et ELLE FAIT REJOUER LA STRATÉGIE, autant de
      fois que de variations demandées plus une : ce que ce rejeu fait échappe
      entièrement à son contrôle, et il peut lire des fichiers et prendre du temps.
    ⑪ TERMINAISON — Rend la main avec son tableau dans le cas ordinaire. Et un de
      ses appels peut ne pas revenir : le PREMIER appel à la façon de rejouer,
      ligne 1368, n'est pas rattrapé, donc une erreur levée là arrête la fonction et
      le programme appelant ; une valeur vide passée à la place d'une façon de
      rejouer y lèverait également. Les appels suivants, eux, sont rattrapés.
      [sort: non]
    ⑫ DÉFINITIONS
      une opération : un achat simulé suivi de sa revente, avec son gain net en
        euros ; aucun ordre réel n'est jamais passé
      un réglage : un des nombres qui définissent une stratégie — l'objectif de gain,
        la perte acceptée, l'horizon
      l'horizon : le nombre de séances pendant lesquelles une position est tenue si ni l'objectif de gain ni la perte acceptée ne sont atteints
      la grille : la liste des huit critères et de leurs seuils ; celle qui tourne
        s'appelle GRILLE-26-04 et vit dans `CRITERES_VALIDATION_EXPERTS`, lignes 1730
        à 1740 de ce fichier
      la table des seuils : `CRITERES_VALIDATION_EXPERTS`, qui porte les neuf seuils
        et le sens de comparaison de chacun
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les
        règles numérotées du projet
      le Sharpe : le rapport du gain moyen à sa dispersion, ramené à l'année
    
      la graine : le nombre qui fixe la suite de tirages, pour qu'un calcul fondé sur le hasard donne toujours le même résultat
      une fraction : la façon d'écrire un pourcentage entre 0 et 1 — 0,040 pour +4 % — par opposition au pourcent, qui écrirait 4.0
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    import random
    random.seed(42)

    res_base = fonction_backtest(params_base)
    net_base = res_base.get('net_a', res_base.get('net', 0))

    nets = [net_base]
    details = [{'params': params_base, 'net': net_base}]

    keys_var = [k for k in params_base if isinstance(params_base[k], (int, float))
                and k not in ('capital', 'frais')]

    for _ in range(n_variations):
        params_test = dict(params_base)
        for k in keys_var:
            v = params_base[k]
            delta = v * random.uniform(-pourcentage, pourcentage)
            if isinstance(v, int):
                params_test[k] = max(1, int(round(v + delta)))
            else:
                params_test[k] = v + delta
        try:
            res = fonction_backtest(params_test)
            net = res.get('net_a', res.get('net', 0))
            nets.append(net)
            details.append({'params': params_test, 'net': net})
        except Exception:
            continue

    net_min = min(nets)
    net_max = max(nets)
    net_moyen = sum(nets) / len(nets)
    ecart_relatif = (net_max - net_min) / abs(net_moyen) if net_moyen != 0 else 0

    return {
        'net_base': round(net_base, 0),
        'net_min': round(net_min, 0),
        'net_max': round(net_max, 0),
        'net_moyen': round(net_moyen, 0),
        'ecart_relatif': round(ecart_relatif, 3),
        'stable': ecart_relatif < 0.5 and net_min > 0,
        'n_variations': len(nets) - 1,
    }


def calculer_walk_forward(fonction_backtest, signaux: list, dates_decoupage: list,
                          params: dict) -> dict:
    """Rejoue la stratégie sur des tranches de temps successives et dit si elle tient
    partout.

    ① RÔLE — Donner au septième critère de la grille son seul chiffre. Couper
      l'historique en deux — soixante-dix pour cent pour régler, trente pour
      vérifier — ne donne qu'une seule épreuve, et le résultat dépend entièrement de
      l'endroit où l'on coupe. Cette fonction découpe la période en plusieurs
      tranches successives, fait rejouer la stratégie sur chacune, et regarde si le
      gain reste positif dans TOUTES. Une stratégie qui gagne beaucoup sur une
      tranche et perd sur les autres a un bon gain total et ne vaut rien : c'est
      exactement ce que cette découpe fait voir.
    ② CONTEXTE D'APPEL — PERSONNE NE L'APPELLE. Mesuré le 19-09-2026 par une
      recherche du nom `calculer_walk_forward` dans tous les fichiers `.py` du dépôt,
      `archives/` mis à part : la seule ligne rendue hors de la définition est un
      COMMENTAIRE de `programmes/MODULE_JUGEMENT.py`, devenu depuis le texte explicatif
      de sa fonction `fenetres_glissantes`, qui constate
      précisément cela — « `calculer_walk_forward` du module de statistiques n'etait
      appelee nulle part ». `programmes/JUGER_SUR_8_CRITERES.py` rend cette mesure
      VIDE, avec pour motif écrit dans son code qu'elle « exige un decoupage en
      fenetres », c'est-à-dire une liste de dates que personne ne produit.
    ③ ENTRÉE — `fonction_backtest` : une façon de rejouer la stratégie, fournie par
      l'appelant ; elle reçoit une liste de signaux et un jeu de réglages, et rend un
      tableau portant `nb_a`, `wr_a` et `net_a`. `signaux` : la liste des signaux,
      chacun étant un tableau portant au moins `date`. `dates_decoupage` : les dates
      qui délimitent les tranches, écrites année-mois-jour ; N dates donnent N moins
      une tranches. `params` : les réglages de la stratégie, transmis tels quels à la
      façon de rejouer. Aucun appelant aujourd'hui, donc aucune valeur réellement
      passée.
    ④ CONDITIONS D'ENTRÉE — CHAQUE signal doit porter une case `date` : elle est lue
      directement, sans précaution, et son absence fait lever la fonction — mesuré le
      19-09-2026, « KeyError: 'date' ». Les dates de découpage doivent être triées du
      plus ancien au plus récent, sans quoi les tranches sont vides. Une tranche doit
      porter au moins cinq signaux pour être retenue.
    ⑤ SORTIE — UNE valeur : un tableau, sous DEUX FORMES QUI NE PARTAGENT QUE DEUX
      CASES SUR NEUF. Quand au moins une tranche a été retenue, SEPT cases :
      `fenetres`, `n_fenetres`, `wr_moyen`, `net_moyen`, `wr_min`, `wr_max` et
      `tous_positifs`. Quand aucune tranche n'a été retenue, QUATRE cases :
      `fenetres`, `wr_moyen`, `net_moyen` et `coherence`. Mesuré le 19-09-2026 : la
      case `tous_positifs` n'existe que dans la première forme, et la case
      `coherence` n'existe que dans la seconde.
      [rend: 1]
    ⑥ TRAITEMENT — ① trier les signaux par leur date · ② pour chaque paire de dates
      de découpage successives, retenir les signaux dont la date est comprise entre
      les deux, la première incluse et la seconde exclue · ③ sauter la tranche si
      elle porte moins de cinq signaux · ④ faire rejouer la stratégie sur cette
      tranche, et sauter la tranche sans rien dire si le rejeu tombe · ⑤ retenir pour
      chaque tranche son nombre d'opérations, son taux de réussite et son gain ·
      ⑥ rendre quatre zéros et un « faux » si aucune tranche n'a été retenue ·
      ⑦ sinon calculer la moyenne, le minimum et le maximum des taux de réussite, la
      moyenne des gains, et dire si tous les gains sont strictement positifs.
    ⑦ UNITÉ — `wr_moyen`, `wr_min` et `wr_max` sont des POURCENTS, arrondis au
      dixième. `net_moyen` est en EUROS, arrondi à l'unité. `n_fenetres` est un
      NOMBRE DE TRANCHES, et `nb_a` un NOMBRE D'OPÉRATIONS dans une tranche.
      `tous_positifs` et `coherence` valent vrai ou faux. Les dates de découpage sont
      des DATES DE CALENDRIER, écrites année-mois-jour.
    ⑧ POURQUOI — Une tranche de moins de cinq signaux est écartée parce qu'un taux
      de réussite calculé sur quatre opérations ne veut rien dire : il ne peut valoir
      que 0, 25, 50, 75 ou 100 %, et une seule opération le déplace d'un quart. La
      garder ferait entrer ce bruit dans la moyenne des tranches à égalité avec une
      tranche de deux cents opérations.
      Le critère retenu est que TOUTES les tranches soient positives, et non que leur
      moyenne le soit, parce que c'est exactement la faute que cette mesure cherche :
      une stratégie qui doit tout son gain à une seule tranche a une bonne moyenne et
      n'a rien prouvé.
    ⑨ CE QUI CLOCHE —
      ① LES DEUX SORTIES NE PARTAGENT QUE DEUX CASES SUR NEUF, ET LA CASE QUE LE
      TEXTE D'ORIGINE PROMETTAIT N'EXISTE JAMAIS QUAND LA FONCTION ABOUTIT. Le texte
      annonçait `{fenetres, wr_moyen, net_moyen, coherence}`. Mesuré le 19-09-2026 :
      quand trois tranches sont retenues, les cases rendues sont `fenetres`,
      `n_fenetres`, `wr_moyen`, `net_moyen`, `wr_min`, `wr_max` et `tous_positifs` —
      `coherence` est ABSENTE. Quand aucune tranche n'est retenue, `coherence`
      apparaît et vaut faux, tandis que `tous_positifs`, `n_fenetres`, `wr_min` et
      `wr_max` disparaissent. Un appelant qui lit `coherence`, comme le texte le lui
      disait, ne trouve jamais de réponse quand la mesure réussit, et trouve toujours
      « faux » quand elle échoue.
      ② UNE MESURE RATÉE EST INDISCERNABLE D'UNE STRATÉGIE QUI PERD. Mesuré le
      19-09-2026 avec une façon de rejouer qui lève à chaque tranche : la fonction
      rend exactement le même tableau que pour une liste de signaux vide —
      `{'fenetres': [], 'wr_moyen': 0, 'net_moyen': 0, 'coherence': False}`. Rien ne
      distingue « le rejeu est cassé » de « il n'y avait rien à mesurer », et les
      deux se lisent comme un critère C7 non passé.
      ③ UN SIGNAL SANS DATE FAIT TOMBER LA FONCTION, ALORS QUE LE TRI QUI LE PRÉCÈDE
      L'ACCEPTE. Le tri lit la date avec une précaution qui rend un texte vide si
      elle manque ; la sélection des tranches, elle, la lit directement. Mesuré le
      19-09-2026 sur dix signaux sans date : « KeyError: 'date' ». Deux lectures de
      la même case, à trois lignes d'écart, avec deux conduites opposées.
      ④ LE TAUX DE RÉUSSITE MOYEN NE TIENT PAS COMPTE DE LA TAILLE DES TRANCHES. La
      moyenne est prise sur les taux eux-mêmes, donc une tranche de cinq opérations
      pèse autant qu'une tranche de deux cents. C'est le seul endroit du calcul où le
      nombre d'opérations d'une tranche, pourtant relevé sous le nom `nb_a`, est
      ignoré.
      ⑤ UNE TRANCHE DONT LE REJEU TOMBE DISPARAÎT SANS UN MOT, et la case
      `tous_positifs` porte alors sur les tranches SURVIVANTES. Une stratégie dont la
      moitié des tranches auraient échoué pourrait ainsi être déclarée positive
      partout. La case `n_fenetres` permet de s'en apercevoir, mais rien n'oblige à
      la lire, et le texte d'origine ne l'annonçait même pas.
      ⑥ Le minimum de cinq signaux par tranche est un nombre écrit dans le corps de
      la fonction, ligne 1562, sans justification et sans source. Il ne vient ni de la
      table des seuils de ce fichier ni du REGISTRE, alors que la règle du projet
      veut que les seuils vivent au REGISTRE et jamais dans le code —
      `gouvernance/REGISTRE_REGLES.md`, règle R-743, deuxième geste.
      ⑦ Les trois cases lues sur le rejeu — `nb_a`, `wr_a` et `net_a` — ne sont
      produites par aucun programme du dépôt. Mesuré le 19-09-2026, une recherche de
      `net_a` dans tous les fichiers `.py`, `archives/` mis à part, ne rend aucune
      ligne hors de ce fichier, et `nb_a` comme `wr_a` n'apparaissent qu'à
      l'intérieur d'autres mots. La façon de rejouer que cette fonction attend n'a
      donc jamais été écrite, et le premier qui l'écrira devra deviner ces trois
      noms — ce qui est exactement la faute commise le 13-09-2026, quand deux noms de
      cases devinés au lieu d'être relevés ont fait rendre des mesures vides que le
      juge à huit critères a lues comme des critères non passés.
      ⑧ Les dates sont comparées COMME DES TEXTES, jamais comme des dates.
      L'écriture année-mois-jour fait que les deux ordres coïncident, mais une date
      écrite autrement placerait les signaux dans les mauvaises tranches sans qu'une
      erreur apparaisse.
    ⑩ EFFET — Ne lit ni n'écrit aucun fichier, n'affiche rien, ne touche pas au
      réseau. Elle ne modifie pas la liste de signaux qu'elle reçoit : le tri produit
      une nouvelle liste. ELLE FAIT REJOUER LA STRATÉGIE, une fois par tranche
      retenue : ce que ce rejeu fait échappe entièrement à son contrôle, et il peut
      lire des fichiers et prendre du temps.
    ⑪ TERMINAISON — Rend la main par l'une de ses deux sorties dans le cas
      ordinaire. PEUT LEVER une erreur non rattrapée sur un signal dépourvu de case
      `date`, ce qui arrêterait le programme appelant — mesuré le 19-09-2026,
      « KeyError: 'date' ». Et un de ses appels peut ne pas revenir : la façon de
      rejouer est fournie par l'appelant, et ce qu'elle fait échappe à cette
      fonction ; les erreurs qu'elle lève sont toutefois rattrapées.
      [sort: non]
    ⑫ DÉFINITIONS
      une opération : un achat simulé suivi de sa revente, avec son gain net en
        euros ; aucun ordre réel n'est jamais passé
      un signal : le repérage, sur la dernière séance connue, d'une configuration de cours qui déclenche une simulation d'achat.
      le walk-forward : le rejeu d'une stratégie sur des tranches de temps
        successives, pour voir si elle tient hors de la période qui a servi à la
        régler
      le taux de réussite : la part des opérations qui se sont refermées sur un gain,
        écrite en pourcent
      la grille : la liste des huit critères et de leurs seuils ; celle qui tourne
        s'appelle GRILLE-26-04 et vit dans `CRITERES_VALIDATION_EXPERTS`, lignes 1730
        à 1740 de ce fichier
      la table des seuils : `CRITERES_VALIDATION_EXPERTS`, qui porte les neuf seuils
        et le sens de comparaison de chacun
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les
        règles numérotées du projet
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    fenetres = []
    sig_tries = sorted(signaux, key=lambda s: s.get('date', ''))

    for i in range(len(dates_decoupage) - 1):
        d_debut = dates_decoupage[i]
        d_fin = dates_decoupage[i + 1]
        sig_fenetre = [s for s in sig_tries if d_debut <= s['date'] < d_fin]
        if len(sig_fenetre) < 5:
            continue
        try:
            res = fonction_backtest(sig_fenetre, params)
            fenetres.append({
                'debut': d_debut, 'fin': d_fin,
                'n': res.get('nb_a', 0),
                'wr': res.get('wr_a', 0),
                'net': res.get('net_a', 0),
            })
        except Exception:
            continue

    if not fenetres:
        return {'fenetres': [], 'wr_moyen': 0, 'net_moyen': 0, 'coherence': False}

    wrs = [f['wr'] for f in fenetres if f['n'] > 0]
    nets = [f['net'] for f in fenetres if f['n'] > 0]

    return {
        'fenetres': fenetres,
        'n_fenetres': len(fenetres),
        'wr_moyen': round(sum(wrs) / len(wrs), 1) if wrs else 0,
        'net_moyen': round(sum(nets) / len(nets), 0) if nets else 0,
        'wr_min': round(min(wrs), 1) if wrs else 0,
        'wr_max': round(max(wrs), 1) if wrs else 0,
        'tous_positifs': all(n > 0 for n in nets) if nets else False,
        # Cohérence = si tous les Net sont > 0, la stratégie est robuste sur la période
    }


def calculer_sharpe_ratio(trades: list, periodes_par_an: int = 252) -> float:
    """Rapporte le gain moyen d'une opération à la dispersion de ces gains, ramenée à
    l'année.

    ① RÔLE — Fournir l'ingrédient que le dégonflage du Sharpe attend. Deux
      stratégies qui rapportent autant ne se valent pas si l'une le fait
      régulièrement et l'autre par à-coups : celle qui secoue oblige à supporter des
      écarts que peu de gens supportent. Ce chiffre rapporte le gain moyen à
      l'ampleur de ces écarts, puis le ramène à l'échelle d'une année pour qu'il soit
      comparable aux chiffres publiés. Mesuré le 19-09-2026 sur 20 opérations
      fabriquées, douze gagnantes à 400 € et huit perdantes à 250 € : il rend
      6,802540423475464.
    ② CONTEXTE D'APPEL — Un seul appelant, `programmes/JUGER_SUR_8_CRITERES.py`,
      dans sa fonction `mesures_disponibles`, une fois par stratégie
      mesurée. Il ne lui passe que la liste des opérations et range le résultat dans
      la case `sharpe` de son tableau de mesures. Ce chiffre n'est comparé à AUCUN
      seuil de la grille : il ne sert qu'à nourrir le deuxième critère, qui a besoin
      du Sharpe pour le dégonfler — et ce deuxième critère n'est pas produit
      aujourd'hui.
    ③ ENTRÉE — `trades` : la liste des opérations, chacune étant un tableau portant
      `gain`, en euros ; la case `date` n'est pas lue ici. Son seul appelant lui
      passe la liste qu'il a construite sous la forme `{"date": …, "gain": …}`.
      `periodes_par_an` : le nombre de périodes dans une année, 252 quand rien n'est
      précisé, et son seul appelant ne précise rien.
    ④ CONDITIONS D'ENTRÉE — Au moins deux opérations, sans quoi la dispersion ne peut
      pas se calculer. Chaque opération doit porter un gain qui soit un nombre : une
      case `gain` absente est remplacée par zéro, mais une case portant du texte
      ferait lever le calcul de la moyenne.
    ⑤ SORTIE — UNE valeur, et c'est un NOMBRE SEUL, pas un tableau — la seule
      fonction de ce fichier dans ce cas. Elle rend le rapport calculé, un nombre à
      virgule, ou bien l'entier 0 dans trois cas : moins de deux opérations, gain
      moyen exactement nul, dispersion exactement nulle. Mesuré le 19-09-2026 : sur
      20 opérations elle rend le nombre à virgule 6,802540423475464 ; sur une seule
      opération elle rend l'entier 0.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre 0 si la liste est vide ou porte moins de deux
      opérations · ② relever le gain de chaque opération, zéro quand la case manque ·
      ③ calculer la moyenne de ces gains, et rendre 0 si elle est exactement nulle ·
      ④ calculer leur écart type, et rendre 0 s'il est exactement nul · ⑤ diviser la
      moyenne par l'écart type et multiplier par la racine du nombre de périodes par
      an.
    ⑦ UNITÉ — Les gains sont des EUROS, mais le rapport rendu est SANS UNITÉ : les
      euros du numérateur et ceux du dénominateur s'annulent. `periodes_par_an` est
      un NOMBRE DE SÉANCES DE BOURSE : 252 est le nombre de séances d'une année
      boursière, week-ends et jours fériés retirés.
    ⑧ POURQUOI — La multiplication par la racine du nombre de périodes par an vient
      d'une correction du 24-08-2026. La formule d'origine calculait la racine de
      `periodes_par_an` DIVISÉ PAR 252, soit la racine de 1 avec la valeur par
      défaut : l'annualisation était donc une multiplication par un, sans effet.
      La formule juste multiplie par la racine du nombre de périodes, soit
      sqrt(252) = 15,8745 avec la valeur par défaut. La racine, et non le nombre
      lui-même, parce que la dispersion d'une somme de périodes indépendantes croît
      comme la racine de leur nombre, tandis que le gain croît comme leur nombre : le
      rapport des deux croît donc comme la racine.
      Un gain moyen exactement nul rend 0 plutôt que de laisser le calcul se faire,
      parce que le rapport serait nul de toute façon et que le chiffre n'aurait aucun
      sens : une stratégie dont le gain moyen est nul n'a rien à rapporter à ses
      secousses.
    ⑨ CE QUI CLOCHE —
      ① L'ANNUALISATION SUPPOSE UNE OPÉRATION PAR SÉANCE DE BOURSE, CE QUI N'EST PAS
      LE CAS, ET LE CHIFFRE RENDU EST DONC TRÈS SURÉVALUÉ. Multiplier par la racine
      de 252 n'est juste que si les gains fournis sont des gains QUOTIDIENS. Ici ce
      sont des gains PAR OPÉRATION, et une stratégie du projet fait de l'ordre de
      cent opérations sur plusieurs années. Mesuré le 19-09-2026 sur 20 opérations
      fabriquées, la fonction rend 6,80 ; un rapport gain sur secousses supérieur à
      2 est déjà considéré comme exceptionnel dans la littérature financière, et
      au-delà de 3 il signale presque toujours une erreur de méthode. Le chiffre
      n'est aujourd'hui comparé à aucun seuil, donc il ne fait rien échouer — mais le
      jour où le deuxième critère de la grille sera branché, il recevra une valeur
      gonflée et déclarera excellent ce qui ne l'est pas.
      ② LE ZÉRO RENDU EN CAS DE REFUS NE SE DISTINGUE PAS D'UN ZÉRO CALCULÉ. Mesuré
      le 19-09-2026 : une seule opération rend 0, et deux opérations de +100 € et
      −100 € rendent 0 également. Dans le premier cas rien n'a été mesuré, dans le
      second le gain moyen est vraiment nul. Un appelant ne peut pas les distinguer,
      et le deuxième critère de la grille prend justement 0 comme valeur par défaut
      quand la mesure manque.
      ③ Le type de ce qui est rendu change selon la branche. Mesuré le 19-09-2026 :
      20 opérations rendent un nombre à virgule, une seule opération rend un entier.
      Son seul appelant s'en protège par une précaution qui accepte aussi un tableau,
      alors que la fonction n'en rend jamais : le code de `programmes/
      JUGER_SUR_8_CRITERES.py`, fonction `mesures_disponibles`, écrit
      `m["sharpe"] = r.get("sharpe") if isinstance(r, dict) else r` : « si c'est un
      tableau, prends la case, sinon prends la valeur ». Cette précaution laisse croire que les deux
      formes ont été observées.
      ④ C'est la SEULE fonction de ce fichier qui rend un nombre seul ; les huit
      autres rendent un tableau. Elle n'a donc aucune case pour dire pourquoi elle a
      renoncé, là où les autres portent une case `erreur` ou un `verdict`.
      ⑤ La dispersion est calculée comme un écart type d'ÉCHANTILLON, qui divise par
      le nombre d'opérations diminué de un. Sur deux opérations, ce diviseur vaut un,
      et le rapport rendu peut prendre n'importe quelle valeur. Aucun nombre minimum
      d'opérations n'est exigé au-delà de deux.
      ⑥ Le nombre 252, écrit dans la signature ligne 1593, ne vient ni de la table des
      seuils de ce fichier ni du REGISTRE, alors que la règle du projet veut que les
      seuils vivent au REGISTRE et jamais dans le code — `gouvernance/
      REGISTRE_REGLES.md`, règle R-743, deuxième geste.
    ⑩ EFFET — Ne lit ni n'écrit aucun fichier, n'affiche rien, ne touche pas au
      réseau, ne modifie rien de ce qu'elle reçoit.
    ⑪ TERMINAISON — Rend toujours la main dans les conditions d'appel d'aujourd'hui.
      Elle PEUT LEVER si une case `gain` porte du texte au lieu d'un nombre : le
      calcul de la moyenne lève alors, et rien n'est rattrapé ici. Elle n'appelle
      aucune fonction du projet.
      [sort: non]
    ⑫ DÉFINITIONS
      une opération : un achat simulé suivi de sa revente, avec son gain net en
        euros ; aucun ordre réel n'est jamais passé
      le Sharpe : le rapport du gain moyen à sa dispersion, ramené à l'année
      le Sharpe dégonflé : le Sharpe corrigé du nombre de stratégies essayées ; plus
        on en essaie, plus un bon Sharpe peut n'être que du hasard
      une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
      la grille : la liste des huit critères et de leurs seuils ; celle qui tourne
        s'appelle GRILLE-26-04 et vit dans `CRITERES_VALIDATION_EXPERTS`, lignes 1730
        à 1740 de ce fichier
      la table des seuils : `CRITERES_VALIDATION_EXPERTS`, qui porte les neuf seuils
        et le sens de comparaison de chacun
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les
        règles numérotées du projet
    
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      une stratégie : une règle qui dit QUOI acheter, avec son objectif de gain, sa perte acceptée et son horizon
"""
    import statistics, math
    if not trades or len(trades) < 2:
        return 0
    gains = [t.get('gain', 0) for t in trades]
    moy = statistics.mean(gains)
    if moy == 0:
        return 0
    sd = statistics.stdev(gains)
    if sd == 0:
        return 0
    # CORRIGÉ 24-08-2026 (défaut 1 du bloc extrait) : la formule d'origine
    # calculait sqrt(periodes_par_an / 252), soit sqrt(1) = 1 avec la valeur
    # par défaut — l'annualisation était donc SANS EFFET. La formule juste
    # multiplie par la racine du nombre de périodes par an.
    sharpe = moy / sd * math.sqrt(periodes_par_an)
    return sharpe


# ═══════════════════════════════════════════════════════════════════════
# CRITÈRES DE VALIDATION CONSOLIDÉS — Adoptés le 26/04/2026
# Source : Comité d'experts (López de Prado, Lo, Hull, Vince, Aronson, Chan)
# ═══════════════════════════════════════════════════════════════════════

CRITERES_VALIDATION_EXPERTS = {
    'C1_significativite': {'seuil': 0.05, 'op': '<', 'description': 'p-value WR vs hasard'},
    'C2_dsr': {'seuil': 0.95, 'op': '>=', 'description': 'Deflated Sharpe Ratio (Bailey-LdP)'},
    'C3_pbo': {'seuil': 0.30, 'op': '<', 'description': 'Probability of Backtest Overfitting'},
    'C4a_dd_pct': {'seuil': 25, 'op': '<', 'description': 'Drawdown max en % du capital'},
    'C4b_underwater': {'seuil': 365, 'op': '<', 'description': 'Time Underwater max en jours'},
    'C5_kelly_frac': {'seuil': 0.05, 'op': '>=', 'description': 'Kelly fractionnel ≥ 5%'},
    'C6_stabilite': {'seuil': True, 'op': '==', 'description': 'Stable sous variations ±10%'},
    'C7_wf_positifs': {'seuil': True, 'op': '==', 'description': 'Walk-forward : toutes fenêtres positives'},
    'C8_frais_realistes': {'seuil': 0.005, 'op': '>=', 'description': 'Frais ≥ 50 bps'},
}


def evaluer_strategie_8_criteres(stats: dict) -> dict:
    """Compare neuf mesures à leurs seuils et rend un score sur huit, avec le détail
    critère par critère.

    ① RÔLE — Transformer neuf chiffres en une décision lisible. C'est le seul endroit
      du système où une stratégie reçoit un verdict : VALIDÉE, EN COURS DE TEST ou
      ARCHIVÉE. Il ne calcule rien lui-même — il reçoit les mesures déjà faites,
      confronte chacune à son seuil, compte celles qui passent, et rend le compte
      avec le détail de chaque comparaison. Mesuré le 19-09-2026 sur les chiffres
      connus de la stratégie C5-EI au 26-04-2026 — probabilité du hasard 0,007,
      Sharpe dégonflé 1,03, probabilité de sur-apprentissage 0,30, chute maximale
      4,6 %, 119 jours sous l'eau, Kelly fractionnel 0,093, stabilité vraie, toutes
      les tranches positives, frais 0,005 : il rend 7 sur 8 et le statut « EN COURS
      DE TEST », exactement ce qu'annonce le mémo du 27-04-2026.
    ② CONTEXTE D'APPEL — Un seul appelant, `programmes/JUGER_SUR_8_CRITERES.py`,
      dans sa fonction `calibrer`, qui lui passe une COPIE des chiffres
      témoins de C5-EI et vérifie qu'il rend bien 7. C'EST SON SEUL EMPLOI
      AUJOURD'HUI : ce même programme s'arrête avant de le rappeler sur des mesures
      réelles, parce que quatre des neuf mesures qu'il sait produire restent vides et
      qu'un score calculé sur cinq serait indiscernable d'un score complet. Le juge à huit critères
      ne sert donc qu'à prouver qu'il fonctionne encore.
    ③ ENTRÉE — `stats` : un tableau portant les neuf mesures, sous les noms
      `p_value`, `dsr`, `pbo`, `dd_pct`, `underwater_jours`, `kelly_frac`, `stable`,
      `wf_tous_positifs` et `frais_pct`. Son seul appelant lui passe une copie du
      tableau nommé `TEMOIN` dans son propre code.
    ④ CONDITIONS D'ENTRÉE — Chaque case, SI ELLE EST PRÉSENTE, doit porter un nombre
      ou un vrai-faux, jamais une valeur vide. Une case absente est remplacée par une
      valeur de repli, mais une case PRÉSENTE ET VIDE fait lever la comparaison —
      mesuré le 19-09-2026 en passant un Sharpe dégonflé vide, « TypeError: '>=' not
      supported between instances of 'NoneType' and 'float' ».
    ⑤ SORTIE — UNE valeur : un tableau de QUATRE cases, toujours les mêmes, sans
      autre forme. `n_criteres_passes`, un entier de 0 à 8 ; `n_total`, qui vaut
      toujours 8 ; `statut`, un texte ; et `details`, la liste des huit comparaisons,
      chacune portant le nom du critère, la valeur reçue, le seuil sous forme de
      texte, et un vrai-faux.
      **Selon la branche, elle rend 1 ou 2 valeur(s).**
      [rend: 1]
⑥ TRAITEMENT — ① lire dans la table le seuil et le sens de comparaison d'un
      critère nommé · ② comparer une valeur à ce seuil, en traitant « inférieur à »
      comme tel et TOUT AUTRE SENS comme « supérieur ou égal » · ③ confronter la
      probabilité du hasard au critère C1 · ④ le Sharpe dégonflé au critère C2 ·
      ⑤ la probabilité de sur-apprentissage au critère C3 · ⑥ la chute maximale ET la
      durée sous l'eau aux deux seuils du critère C4, qui n'est passé que si les deux
      le sont · ⑦ le Kelly fractionnel au critère C5 · ⑧ la stabilité au critère C6,
      en la reprenant TELLE QUELLE · ⑨ les tranches positives au critère C7, de même ·
      ⑩ le taux de frais au critère C8, en cherchant dans la table une entrée nommée
      `C8_frais_min` et, à défaut, en comparant à 0,005 écrit ici · ⑪ compter les
      critères passés · ⑫ poser le statut : VALIDÉE si tous sont passés, EN COURS DE
      TEST à partir de six, ARCHIVÉE en dessous.
      le détail : le fichier `registre_experiences.csv`, une ligne par expérience
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
    ⑦ UNITÉ — Elles ne se mélangent pas, et cette fonction en manipule quatre. Des
      FRACTIONS entre 0 et 1 : `p_value`, `dsr`, `pbo`, `kelly_frac`, `frais_pct`, et
      leurs seuils 0,05 · 0,95 · 0,30 · 0,05 · 0,005. Un POURCENT : `dd_pct`, et son
      seuil 25. Des JOURS DE CALENDRIER : `underwater_jours`, et son seuil 365. Des
      vrais-faux : `stable` et `wf_tous_positifs`. `n_criteres_passes` et `n_total`
      sont des NOMBRES DE CRITÈRES.
    ⑧ POURQUOI — Le juge à huit critères LIT ses seuils dans la table plutôt que de les recopier, et
      c'est une correction du 24-08-2026 : les huit seuils étaient auparavant écrits
      deux fois, dans la table et de nouveau en dur dans ce corps. Un chiffre qui
      existe ailleurs ne se recopie pas (R-708), parce que deux copies d'un même
      nombre finissent toujours par diverger, et la divergence ne se voit nulle part
      — elle déplace seulement la frontière entre une stratégie validée et une
      stratégie archivée.
      Le nombre total de critères est COMPTÉ sur les comparaisons réellement faites
      et non écrit à la main, pour la même raison : un garde-fou porte sur une
      propriété, jamais sur un compte.
      Le quatrième critère porte DEUX seuils pour un seul critère, la chute et la
      durée, parce que les deux disent la même chose sous deux angles : une chute
      faible mais qui dure des années est aussi insupportable qu'une chute brutale.
      Les prendre séparément donnerait deux critères sur huit à une seule idée.
      Et le barème — huit sur huit pour valider, six ou sept pour rester à l'essai —
      a été adopté le 26-04-2026 avec la grille elle-même. Il est recopié au REGISTRE
      sous le titre « GRILLE-26-04 — la grille qui tourne aujourd'hui ».
    ⑨ CE QUI CLOCHE —
      ① LE HUITIÈME CRITÈRE NE LIT PAS LA TABLE : IL CHERCHE UNE CASE QUI N'Y EXISTE
      PAS ET RETOMBE SUR UN NOMBRE ÉCRIT ICI. La ligne 2002 cherche dans la table une
      entrée nommée `C8_frais_min`. Mesuré le 19-09-2026, les neuf noms de la table
      sont `C1_significativite`, `C2_dsr`, `C3_pbo`, `C4a_dd_pct`, `C4b_underwater`,
      `C5_kelly_frac`, `C6_stabilite`, `C7_wf_positifs` et `C8_frais_realistes` :
      `C8_frais_min` n'y est pas, et le repli de la ligne 2003 s'applique donc
      TOUJOURS, avec le nombre 0,005 écrit là. La conséquence se mesure : en portant
      le seuil de l'entrée `C8_frais_realistes` de 0,005 à 0,99, ce qui rend ce
      critère impossible à passer, et en rejouant les chiffres témoins de C5-EI, le
      verdict ne bouge pas d'un point — 7 sur 8 avant, 7 sur 8 après. Pour comparer,
      durcir dans la même table le seuil du premier critère de 0,05 à 0,001 fait bien
      tomber le verdict de 7 sur 8 à 6 sur 8 : les autres entrées, elles, sont lues.
      Un lecteur qui corrige le seuil des frais dans la table croit donc avoir changé
      le juge à huit critères, et n'a rien changé.
      ② LES SIXIÈME ET SEPTIÈME CRITÈRES NE LISENT PAS LA TABLE NON PLUS. Lignes 1990
      et 1996, la stabilité et les tranches positives sont reprises telles quelles,
      sans passer par la comparaison au seuil. Mesuré le 19-09-2026 : en mettant à
      faux le seuil de l'entrée `C7_wf_positifs` et en rejouant les chiffres témoins
      de C5-EI, le verdict reste 7 sur 8. Trois des neuf entrées de la table sont donc
      décoratives, et la correction du 24-08-2026 qui annonce que « le juge à huit critères LIT
      désormais la table et ne recopie plus aucun nombre » ne vaut que pour six.
      ③ AJOUTER UN CRITÈRE À LA TABLE NE SUFFIT PAS, CONTRAIREMENT À CE QUE LE CODE
      ANNONCE. Le commentaire de la ligne 1938 affirme qu'ajouter une entrée suffit et
      que le juge à huit critères la prendra sans être modifié. Mesuré le 19-09-2026 en ajoutant une
      dixième entrée à la table puis en rejouant : la table compte bien dix entrées,
      et le juge à huit critères rend toujours un total de 8. Les huit comparaisons sont écrites une
      par une dans le corps, et aucune boucle ne parcourt la table.
      ④ LE SENS DE COMPARAISON « ÉGAL » ÉCRIT DANS LA TABLE N'EST JAMAIS APPLIQUÉ. La
      comparaison de la ligne 1946 ne connaît que deux cas : « inférieur à », et tout
      le reste traité comme « supérieur ou égal ». Les entrées `C6_stabilite` et
      `C7_wf_positifs` portent pourtant le sens « égal », relevé le 19-09-2026. Comme
      ces deux critères ne passent de toute façon pas par cette comparaison, le
      défaut est sans effet aujourd'hui ; il se réveillerait le jour où l'on
      brancherait la table pour eux.
      ⑤ LES VALEURS DE REPLI DÉCIDENT DU VERDICT, ET CE SONT ENCORE DES NOMBRES
      ÉCRITS ICI. Quand une case manque, le juge à huit critères prend 1,0 pour la probabilité du
      hasard, 0 pour le Sharpe dégonflé, 1,0 pour la probabilité de
      sur-apprentissage, 100 pour la chute, 99 999 pour la durée sous l'eau, 0 pour
      le Kelly et le taux de frais, faux pour la stabilité et les tranches. Mesuré le
      19-09-2026 sur un tableau VIDE : le juge à huit critères rend 0 sur 8 et le statut ARCHIVÉE,
      sans un mot disant qu'aucune mesure ne lui a été donnée. Une stratégie sur
      laquelle personne n'a rien mesuré est donc archivée comme une stratégie
      mauvaise.
      ⑥ UNE MESURE PRÉSENTE MAIS VIDE FAIT TOMBER LE JUGE À HUIT CRITÈRES. La valeur de repli n'est
      prise que si la case est ABSENTE ; une case présente et vide est comparée
      telle quelle. Mesuré le 19-09-2026 en passant un Sharpe dégonflé vide :
      « TypeError: '>=' not supported between instances of 'NoneType' and 'float' ».
      Or `programmes/JUGER_SUR_8_CRITERES.py` pose délibérément les neuf cases,
      celles qu'il ne sait pas produire étant VIDES : le jour où il appellera le juge à huit critères
      sur ses mesures réelles, le juge à huit critères s'arrêtera sur une erreur au lieu de rendre un
      score partiel.
      ⑦ LE SEUIL 6 QUI SÉPARE « ARCHIVÉE » DE « EN COURS DE TEST » EST UN COMPTE
      ÉCRIT EN DUR, ligne 2010, et il ne suit pas le total. Le total, lui, est bien
      compté sur les comparaisons faites, ligne 2007. Si le nombre de critères passait
      un jour à dix, six sur dix suffirait encore à rester à l'essai, alors que six
      sur huit et six sur dix ne disent pas la même chose.
      ⑧ AUCUN SEUIL N'EST LU AU REGISTRE, ALORS QUE LA LOI DU PROJET L'EXIGE ET
      DÉSIGNE CE FICHIER. La règle R-743 de `gouvernance/REGISTRE_REGLES.md`,
      deuxième geste, ligne 860, écrit : « LES SEUILS VIVENT AU REGISTRE, JAMAIS DANS
      LE CODE », et ajoute « Neuf seuils écrits en dur dans MODULE_STATISTIQUES
      enfreignaient déjà cette consigne ». Mesuré le 19-09-2026, le mot REGISTRE
      n'apparaît pas une seule fois dans ce fichier. Le REGISTRE en porte une COPIE À
      LA MAIN, qu'il déclare lui-même « relevée dans
      MODULE_STATISTIQUES.CRITERES_VALIDATION_EXPERTS le 13-09-2026 et recopiée ici
      au chiffre près ». Le seul contrôle qui existe, `seuils_du_registre` de
      `programmes/JUGER_SUR_8_CRITERES.py`, ne vérifie que la PRÉSENCE du texte
      « 0,30 » dans le document, jamais l'égalité de deux valeurs.
      ⑨ LE VERDICT NE NOMME PAS SA GRILLE. Le statut rendu est « VALIDÉE (8/8) » et
      non « VALIDÉE (8/8) selon GRILLE-26-04 », alors que la règle R-743 de
      `gouvernance/REGISTRE_REGLES.md`, premier geste, pose que « 7/8 » ne veut rien
      dire sans le nom de la grille. Il existe une seconde grille, GRILLE-A210,
      commencée le 14-08-2026 et inachevée, dont sept critères sur huit diffèrent de
      celle-ci — ce ne sont pas deux versions d'une grille, ce sont deux grilles.
      ⑩ DEUX SEUILS DE LA TABLE RESTENT EN CONFLIT OUVERT, ET LE JUGE À HUIT CRITÈRES LES APPLIQUE
      SANS RIEN DIRE. ① La probabilité de sur-apprentissage : la table exige moins de
      0,30, l'expert consulté le 08-07-2026 dit moins de 0,50. ② Le taux de frais :
      la table exige au moins 0,005, soit 50 points de base, tandis que le système
      applique réellement 0,0015 — `MODULE_POSITIONS.FRAIS_TAUX`, le tarif Fortuneo
      PROGRESS. Tant que ce second conflit dure, AUCUNE stratégie mesurée sur les
      frais réels ne peut atteindre 8 sur 8 : le huitième critère est perdu
      d'avance. Le témoin de C5-EI passe ce critère uniquement parce qu'on lui
      attribue des frais de 0,005, qui ne sont pas ceux du projet.
    ⑩ EFFET — Ne lit ni n'écrit aucun fichier, n'affiche rien, ne touche pas au
      réseau. Elle ne modifie pas le tableau de mesures qu'elle reçoit : elle ne fait
      qu'y lire. Elle ne modifie pas non plus la table des seuils, qu'elle ne fait
      que consulter.
    ⑪ TERMINAISON — Rend la main avec son tableau dans le cas ordinaire. PEUT LEVER
      une erreur non rattrapée quand une des mesures qu'elle compare est présente et
      vide, ce qui arrêterait le programme appelant — mesuré le 19-09-2026,
      « TypeError ». Elle n'appelle aucune fonction du projet : les deux petites
      fonctions qu'elle emploie sont écrites à l'intérieur d'elle-même et rendent
      toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS
      une opération : un achat simulé suivi de sa revente, avec son gain net en
        euros ; aucun ordre réel n'est jamais passé
      le juge à huit critères : `evaluer_strategie_8_criteres`, la fonction de `MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py` qui compare neuf mesures à leurs seuils et rend un score sur huit
      la grille : la liste des huit critères et de leurs seuils ; celle qui tourne
        s'appelle GRILLE-26-04 et vit dans `CRITERES_VALIDATION_EXPERTS`, lignes 1730
        à 1740 de ce fichier
      la table des seuils : `CRITERES_VALIDATION_EXPERTS`, qui porte les neuf seuils
        et le sens de comparaison de chacun
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les
        règles numérotées du projet
      la p-value, ici « la probabilité du hasard » : la probabilité qu'un taux de
        réussite au moins aussi bon soit obtenu par le seul hasard
      le Sharpe dégonflé : le rapport gain sur secousses corrigé du nombre de
        stratégies essayées ; plus on en essaie, plus un bon rapport peut n'être que
        du hasard
      la probabilité de sur-apprentissage : la probabilité qu'une stratégie doive ses
        bons résultats au réglage sur les données passées plutôt qu'à un effet réel
      le Kelly fractionnel : la part du capital qu'il serait raisonnable d'engager
        sur une opération, compte tenu du taux de réussite et des gains et pertes
        attendus
      la durée sous l'eau : le nombre de jours pendant lesquels le cumul des gains
        reste sous son plus haut précédent
      un point de base : un centième de pourcent ; 50 points de base valent 0,5 %
      un témoin : un jeu de chiffres dont on connaît d'avance le résultat, employé
        pour prouver qu'un instrument fonctionne avant de s'en servir
    """
    # CORRIGÉ 24-08-2026 (défaut 4 du bloc extrait) : les seuils étaient écrits
    # DEUX FOIS — dans CRITERES_VALIDATION_EXPERTS et de nouveau en dur ici.
    # Deux sources de vérité pour un même seuil divergent toujours ; R-708
    # l'interdit. Le juge à huit critères LIT désormais la table et ne recopie plus aucun
    # nombre. Ajouter un neuvième critère à la table suffit : le juge le prend
    # sans être modifié — principe « un contrôle lit, il ne compte pas ».
    def _seuil(cle):
        """Rend le seuil d'un critère de jugement et le sens de la comparaison.

        ① RÔLE — Donner au juge à huit critères, pour un critère nommé, la valeur à ne pas franchir et le
        sens dans lequel la franchir est mauvais. C'est le seul point où les seuils sont
        lus : sans elle, chaque critère porterait son chiffre en clair.
        ② CONTEXTE D'APPEL — Définie dans `evaluer_strategie_8_criteres` et appelée par
        `_passe`, définie juste à côté, une fois par critère.
        ③ ENTRÉE — `cle` : le nom du critère, par exemple `C1_significativite`.
        ④ CONDITIONS D'ENTRÉE — La clé doit exister dans la table
        `CRITERES_VALIDATION_EXPERTS`, qui porte neuf entrées relevées le 20-09-2026.
        ⑤ SORTIE — DEUX valeurs : le seuil, un nombre, et le sens de la comparaison, le
        texte `<` ou `>=`. Exemple mesuré le 20-09-2026 : `C1_significativite` rend
        `(0.05, '<')`.
          [rend: 2]
        ⑥ TRAITEMENT — ① prendre l'entrée de la table portant ce nom · ② en rendre le
        seuil et l'opérateur.
        ⑦ UNITÉ — Celle du critère : une probabilité pour `C1_significativite`, un
        pourcent pour `C4a_dd_pct`, une fraction pour `C8_frais_realistes`. **Elle ne la
        porte pas** : l'unité vit dans la table, pas ici.
        ⑧ POURQUOI — Le seuil et le sens voyagent ensemble parce que les deux décident du
        verdict : un seuil de 0,05 ne veut rien dire tant qu'on ignore s'il faut être
        au-dessus ou en dessous. Les séparer serait la façon la plus sûre d'inverser un
        jugement.
        ⑨ CE QUI CLOCHE — Une clé absente de la table lève une erreur de clé, que le juge à huit critères
        ne rattrape pas. **Ce n'est pas théorique** : le juge à huit critères cherche ailleurs une clé
        `C8_frais_min` qui n'est pas dans la table, et retombe alors sur une valeur écrite
        en clair dans le code — défaut déjà porté au BACKLOG sous A-434. Relevé le
        20-09-2026 sur les neuf clés de la table.
        ⑩ EFFET — Aucun. Elle lit la table sans la modifier.
        ⑪ TERMINAISON — Rend la main, ou LÈVE une erreur de clé sur un nom absent. Aucun
        de ses appels ne se termine.
          [sort: non]
        """
        c = CRITERES_VALIDATION_EXPERTS[cle]
        return c['seuil'], c['op']

    def _passe(valeur, cle):
        """Dit si une mesure franchit son seuil du bon côté.

        ① RÔLE — Rendre le verdict d'un critère : la stratégie passe-t-elle ce test, oui
        ou non. C'est la brique dont le compte « 7 sur 8 » est fait.
        ② CONTEXTE D'APPEL — Définie dans `evaluer_strategie_8_criteres` et appelée par
        elle, une fois par critère jugé.
        ③ ENTRÉE — `valeur` : le chiffre mesuré sur la stratégie · `cle` : le nom du
        critère, par exemple `C1_significativite`.
        ④ CONDITIONS D'ENTRÉE — `valeur` doit être un nombre : une valeur absente, rendue
        par une mesure qui n'a pas pu être faite, fait lever la comparaison. La clé doit
        exister dans la table des critères.
        ⑤ SORTIE — UNE valeur : vrai quand le critère est passé, faux sinon.
          [rend: 1]
        ⑥ TRAITEMENT — ① demander le seuil et le sens · ② comparer la valeur au seuil
        dans ce sens · ③ rendre le résultat.
        ⑦ UNITÉ — Celle du critère, portée par la table et jamais par cette fonction.
        ⑧ POURQUOI — Le sens de la comparaison est lu et non écrit ici, pour qu'un
        changement de règle au seul endroit qui porte les seuils suffise. Un chiffre qui
        existe ailleurs ne se recopie pas (R-708).
        ⑨ CE QUI CLOCHE — Le sens n'a que deux branches : tout opérateur qui n'est pas
        `<` est traité comme `>=`. Un opérateur mal orthographié dans la table ne ferait
        pas rougir la fonction, il inverserait silencieusement la moitié des verdicts.
        Réparer par une propriété plutôt que par une énumération est le critère du projet
        (R-745). Relevé par lecture du code le 20-09-2026, non provoqué.
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main, ou LÈVE — une erreur de type sur une valeur qui
        n'est pas un nombre, une erreur de clé sur un nom absent, cette dernière venant de
        son appel à `_seuil`. **Un de ses appels peut donc ne pas revenir.**
          [sort: non]
        """
        s, op = _seuil(cle)
        return (valeur < s) if op == '<' else (valeur >= s)

    details = []
    n_passes = 0

    # C1
    p = stats.get('p_value', 1.0)
    ok1 = _passe(p, 'C1_significativite')
    details.append({'critere': 'C1 Significativité', 'valeur': p,
                    'seuil': f"{_seuil('C1_significativite')[1]}{_seuil('C1_significativite')[0]}", 'ok': ok1})
    if ok1: n_passes += 1

    # C2
    dsr = stats.get('dsr', 0)
    ok2 = _passe(dsr, 'C2_dsr')
    details.append({'critere': 'C2 DSR', 'valeur': dsr,
                    'seuil': f"{_seuil('C2_dsr')[1]}{_seuil('C2_dsr')[0]}", 'ok': ok2})
    if ok2: n_passes += 1

    # C3
    pbo = stats.get('pbo', 1.0)
    ok3 = _passe(pbo, 'C3_pbo')
    details.append({'critere': 'C3 PBO', 'valeur': pbo,
                    'seuil': f"{_seuil('C3_pbo')[1]}{_seuil('C3_pbo')[0]}", 'ok': ok3})
    if ok3: n_passes += 1

    # C4 — deux seuils, un seul critère
    dd = stats.get('dd_pct', 100)
    uw = stats.get('underwater_jours', 99999)
    ok4 = _passe(dd, 'C4a_dd_pct') and _passe(uw, 'C4b_underwater')
    details.append({'critere': 'C4 DD + TUW', 'valeur': f'DD={dd}% UW={uw}j',
                    'seuil': f"DD{_seuil('C4a_dd_pct')[1]}{_seuil('C4a_dd_pct')[0]}"
                             f" + UW{_seuil('C4b_underwater')[1]}{_seuil('C4b_underwater')[0]}", 'ok': ok4})
    if ok4: n_passes += 1

    # C5
    kf = stats.get('kelly_frac', 0)
    ok5 = _passe(kf, 'C5_kelly_frac')
    details.append({'critere': 'C5 Kelly fractionnel', 'valeur': kf,
                    'seuil': f"{_seuil('C5_kelly_frac')[1]}{_seuil('C5_kelly_frac')[0]}", 'ok': ok5})
    if ok5: n_passes += 1

    # C6
    stable = stats.get('stable', False)
    ok6 = stable
    details.append({'critere': 'C6 Stabilité paramétrique', 'valeur': stable, 'seuil': 'True', 'ok': ok6})
    if ok6: n_passes += 1

    # C7
    wf = stats.get('wf_tous_positifs', False)
    ok7 = wf
    details.append({'critere': 'C7 Walk-forward positif', 'valeur': wf, 'seuil': 'True', 'ok': ok7})
    if ok7: n_passes += 1

    # C8
    frais = stats.get('frais_pct', 0)
    ok8 = _passe(frais, 'C8_frais_min') if 'C8_frais_min' in CRITERES_VALIDATION_EXPERTS \
          else frais >= 0.005
    details.append({'critere': 'C8 Frais réalistes', 'valeur': frais, 'seuil': '≥0.005 (50bps)', 'ok': ok8})
    if ok8: n_passes += 1

    n_total = len(details)   # le juge COMPTE ce qu'il a évalué, il ne suppose pas 8
    if n_passes == n_total:
        statut = f'✅ VALIDÉE ({n_passes}/{n_total})'
    elif n_passes >= 6:
        statut = '🔍 EN COURS DE TEST'
    else:
        statut = '📦 ARCHIVÉE'

    return {
        'n_criteres_passes': n_passes,
        'n_total': n_total,
        'statut': statut,
        'details': details,
    }
