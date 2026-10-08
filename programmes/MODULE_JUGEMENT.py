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
    le point mort · les episodes independants · la coupure 70/30 avec nettoyage
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
  relevé le 19-09-2026 : `point_mort_en_fractions`, `episodes`, `coupure_70_30`,
  `wilson_bas`, `fenetres_glissantes`, `borne_basse_gain`,
  `plus_longue_serie_de_pertes` et `etalon_hasard`.
  ② `programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py` n'appelle que
  `point_mort_en_fractions`, à travers sa propre `point_mort_en_pourcents` qui
  convertit des pourcents en fractions puis délègue, parce que le calcul du
  point mort ne doit vivre qu'à un seul endroit (R-708). Ce programme-là TOURNE
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
  rien et expose quinze fonctions. Lancé en ligne de commande : il SORT DU
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
  forfait (RÉGLÉ LE 28-09-2026, A-435 ④ : il appelle `mod_positions.pnl_net`) : mesuré, un aller-retour de 100,00 € à 104,00 € rend 3 694,00 €
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
  par aucun contrôle du fichier.
  ④ Deux fonctions ne sont appelées par personne. Mesuré le 19-09-2026 en
  cherchant chaque nom dans tous les fichiers `.py` de `programmes/` hors ce
  fichier : `courbe_quotidienne` et `glissement` rendent zéro appelant, alors
  que le texte d'en-tête les compte parmi ce que le module apporte. Elles sont
  écrites, elles sont justes, et aucun rapport ne les affiche.
  ⑤ Les seuils de la méthode de jugement sont écrits dans le code et nulle part
  ailleurs. Les 21 séances d'embargo entre deux morceaux de période, les 5
  séances qui séparent deux épisodes, la coupure au sept dixièmes de la période
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
FRAIS = 300.0
GRAINE = 20260828


# ─────────────────────────────────────────────────────────────────────
# LE POINT MORT — le seuil qui remplace tout seuil fixe
# ─────────────────────────────────────────────────────────────────────

def point_mort_en_fractions(tp, sl, frais=None, capital=CAPITAL, mod_positions=None):
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
    ② CONTEXTE D'APPEL — Trois appelants, dont un automatique.
      ① `programmes/JUGE_DES_STRATEGIES.py`, à la main, une fois par stratégie jugée, en
      lui passant le module des positions pour qu'elle prenne les vrais frais.
      ② `point_mort_en_pourcents` de
      `programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py`, qui convertit
      des pourcents en fractions et délègue ici parce que le calcul ne doit
      vivre qu'à un seul endroit (R-708). Ce programme TOURNE CHAQUE SOIR,
      lancé à la ligne 223 de `.github/workflows/collecte_abc.yml`.
      ③ `_calibrage`, trois fois, pour vérifier que les résultats connus sont
      toujours retrouvés.
    ③ ENTRÉE — `tp` : l'objectif de gain, en FRACTION, 0.040 pour +4 % ·
      `sl` : la perte acceptée, en FRACTION et en valeur positive, 0.025 pour
      −2,5 % · `frais` : le montant forfaitaire des frais d'un aller-retour en
      euros, `None` par défaut, et les deux appelants de production le laissent
      à `None` · `capital` : la somme engagée par opération, 100 000 € par
      défaut, aucun appelant ne la change · `mod_positions` : le module qui
      possède le taux de frais, `None` par défaut ; le juge des stratégies et le
      programme de mesure y passent tous deux `programmes/MODULE_POSITIONS.py`.
    ④ CONDITIONS D'ENTRÉE — `tp` et `sl` doivent être des fractions strictement
      inférieures à 1 en valeur absolue, sans quoi la fonction lève. Le résultat
      doit tomber entre 0 et 100, sans quoi elle lève aussi. Si `mod_positions`
      est donné, il doit porter une fonction `frais_ordre(quantite, prix)`.
    ⑤ SORTIE — UNE valeur : le point mort, un pourcentage entre 0 et 100.
      Exemples relevés le 19-09-2026 : 43,08 pour 0.040 et 0.025 avec les frais
      forfaitaires, 32,86 pour 0.05 et 0.02 avec un taux de frais de 0,15 %.
      [rend: 1]
    ⑥ TRAITEMENT — ① faire respecter le contrat d'unité annoncé par le nom ·
      ② si aucun montant de frais n'est imposé et qu'un module de positions est
      fourni, calculer les frais SÉPARÉMENT pour la sortie au gain et pour la
      sortie au stop, puisqu'ils sont proportionnels à la valeur échangée ·
      ③ sinon, retomber sur le forfait de 300 € · ④ rendre la part que la perte
      représente dans la somme du gain et de la perte, exprimée en pourcents ·
      ⑤ refuser un résultat hors de l'intervalle 0 à 100.
    ⑦ UNITÉ — `tp` et `sl` sont des FRACTIONS. `frais` et `capital` sont des
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
      ① Le repli est muet. Quand aucun module de positions n'est donné, la
      fonction retombe sur un forfait de 300 € sans rien dire, et rend un
      chiffre qui a l'air aussi solide que l'autre. Mesuré le 19-09-2026 : le
      couple 0.040 et 0.025 rend 43,08 % par le forfait et le couple 0.05 et
      0.02 rend 32,86 % par le vrai taux ; rien dans la valeur rendue ne dit
      par quel chemin elle est passée.
      ② Le paramètre `capital` ne sert à rien au résultat. Il apparaît au
      numérateur et au dénominateur de la même fraction : mesuré le 19-09-2026,
      le couple 0.040 et 0.025 rend 43,08 % avec 100 000 € et 43,08 % avec
      10 000 €, frais forfaitaires identiques. Un lecteur qui voit ce paramètre
      croit pouvoir régler quelque chose qui ne bouge pas.
      ③ Le forfait de 300 € est un nombre recopié. `programmes/MODULE_POSITIONS.py`
      porte `FRAIS_TAUX = 0.0015`, et les frais réels d'une opération de
      100 000 € sortie à +4 % valent 306,00 € — mesuré le 19-09-2026. Le repli
      sous-estime donc les frais, dans le sens qui flatte la stratégie.
    ⑩ EFFET — Aucun : elle calcule. Aucun fichier, aucun réseau, aucune donnée
      modifiée. Elle EXÉCUTE la fonction `frais_ordre` du module qu'on lui
      passe, quatre fois par appel.
    ⑪ TERMINAISON — Rend la main avec un pourcentage dans le cas normal. PEUT
      LEVER, et dans les deux cas l'erreur remonte à l'appelant : sur un seuil
      qui n'est pas une fraction, et sur un résultat hors de 0 à 100. Un de ses
      appels peut ne pas revenir : `_exiger_des_fractions` et `_impossible`
      lèvent toutes deux.
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
    # LES FRAIS VIENNENT DU MODULE QUI LES POSSEDE, jamais d'un nombre recopie.
    # Defaut trouve le 29/08 : 300 EUR etaient ecrits en dur ici alors que
    # MODULE_POSITIONS applique 0,15 % de la valeur echangee a l'entree ET a la
    # sortie — 307,50 EUR sur une sortie a +5 %. Petit ecart, mais un nombre
    # recopie qui contredit son proprietaire, c'est R-708.
    if frais is None:
        _fo = getattr(mod_positions, "frais_ordre", None) if mod_positions else None
        if callable(_fo):
            # LES DEUX BRANCHES N'ONT PAS LES MEMES FRAIS : une sortie au
            # gain coute plus cher qu'une sortie au stop, puisque les frais
            # sont proportionnels a la valeur echangee. Appliquer les frais de
            # la branche gagnante aux deux donnait 32,96 % au lieu de 32,86.
            q = capital / 100.0                      # prix d'entree normalise
            f_gain = _fo(q, 100.0) + _fo(q, 100.0 * (1 + tp))
            f_perte = _fo(q, 100.0) + _fo(q, 100.0 * (1 - sl))
            gain = capital * tp - f_gain
            perte = capital * sl + f_perte
            return _impossible(100.0 * perte / (gain + perte), tp, sl)
        else:
            frais = FRAIS                            # repli, valeur historique
    gain = capital * tp - frais
    perte = capital * sl + frais
    return _impossible(100.0 * perte / (gain + perte), tp, sl)


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
# LES ÉPISODES INDÉPENDANTS — combien d'observations VRAIMENT distinctes
# ─────────────────────────────────────────────────────────────────────

def episodes(ops, seances_projet, seuil=5):
    """Regroupe les signaux separes de MOINS DE `seuil` SEANCES.

    LA REGLE VIENT D'A-210, elle n'est pas reinventee : « 100 operations = 85
    jours de signal distincts = 33 episodes independants — signaux regroupes
    s'ils sont a moins de 5 seances ; 28 a 7 seances, 20 a 10 ».

    CALIBRAGE DU 28-08-2026 : la valeur principale est retrouvee EXACTEMENT,
    33 episodes a 5 seances, avec la lecture « ecart STRICTEMENT superieur au
    seuil ouvre un nouvel episode ». Les deux valeurs secondaires donnent 26 et
    19 contre 28 et 20 documentes — ecart de 1 et 2, tres probablement du au
    trou du 29-10-2024 repare le 25/08, qui a ajoute cinq seances aux donnees.
    **Ce n'est PAS verifie, et c'est dit plutot que masque.**

    DEUX PIEGES QUE CETTE FONCTION EVITE, tous deux commis le 28/08 avant
    correction : compter en JOURS CALENDAIRES au lieu de SEANCES — un week-end
    compte alors comme deux jours de marche ; et employer l'horizon de detention
    comme critere de regroupement, ce qui mesure le chevauchement des POSITIONS
    (consequence de nos reglages) au lieu de la proximite des SIGNAUX (cause de
    marche). A-211 a deja tranche ce point : une mesure qui bouge quand on change
    l'objectif ou le stop mesure autre chose que ce qu'elle pretend.

    POURQUOI CETTE MESURE EXISTE : cent operations nees du meme creux de marche
    ne sont pas cent observations. Tout test statistique qui compte 100 la ou il
    y a 33 episodes surestime la certitude — c'est ce qui fondait a tort le
    statut « validee stricte » de C5-ETENDU-10 (A-210).

    ① RÔLE — Dire combien d'observations VRAIMENT distinctes portent un
      résultat, et non combien d'opérations il compte. Cent opérations nées du
      même creux de marché ne sont pas cent observations indépendantes : elles
      décrivent un seul événement vu cent fois. Le chiffre de référence du
      projet est écrit au BACKLOG sous l'action A-210 : 100 opérations, 85 jours
      de signal distincts, 33 épisodes indépendants.
    ② CONTEXTE D'APPEL — Un seul appelant : `programmes/JUGE_DES_STRATEGIES.py`, à la
      main, une fois par stratégie jugée, sans préciser le seuil. Aucun autre
      appel dans le dépôt — recherche dans tous les fichiers `.py` de
      `programmes/` le 19-09-2026, une seule ligne.
    ③ ENTRÉE — `ops` : la liste des opérations, chacune étant un dictionnaire
      dont seule la case `date_signal` est lue ici · `seances_projet` : toutes
      les dates de séance connues, qui servent à compter en séances et non en
      jours · `seuil` : le nombre de séances au-delà duquel deux signaux
      appartiennent à deux épisodes, 5 par défaut, et l'unique appelant laisse
      ce défaut.
    ④ CONDITIONS D'ENTRÉE — Les dates doivent s'écrire de la même façon dans
      les opérations et dans le calendrier, sinon aucune n'est reconnue. Une
      liste d'opérations vide est acceptée.
    ⑤ SORTIE — UNE valeur : un dictionnaire, et il prend TROIS formes
      différentes. Sur une liste vide, deux cases seulement : le nombre
      d'opérations à zéro et le nombre d'épisodes à zéro — mesuré le
      19-09-2026. Quand aucune date n'est reconnue au calendrier : le nombre
      d'opérations, un nombre d'épisodes à `None`, et un motif en clair. Dans le
      cas normal : cinq cases, dont le nombre de jours de signal, le nombre
      d'épisodes, le seuil employé et le nombre moyen d'opérations par épisode.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre deux cases à zéro si la liste est vide · ② numéroter
      les séances du calendrier dans l'ordre · ③ relever les jours de signal
      distincts reconnus au calendrier · ④ rendre un motif si aucun ne l'est ·
      ⑤ parcourir ces jours deux à deux et ouvrir un nouvel épisode chaque fois
      que l'écart, compté en séances, dépasse STRICTEMENT le seuil · ⑥ rendre
      les comptes.
    ⑦ UNITÉ — Les écarts se comptent en SÉANCES de bourse et jamais en jours de
      calendrier. Les épisodes et les opérations sont des NOMBRES.
    ⑧ POURQUOI — Le comptage en séances plutôt qu'en jours évite qu'un week-end
      compte pour deux jours de marché. Et c'est la proximité des SIGNAUX qui
      regroupe, jamais l'horizon de détention : l'horizon est un réglage, et une
      mesure qui bouge quand on change l'objectif ou le stop mesure les réglages
      et non le marché. Les deux pièges ont été commis le 28-08-2026 avant
      correction.
      Ce que la mesure sert à éviter est écrit : un test statistique qui compte
      100 là où il y a 33 épisodes surestime la certitude, et c'est ce qui
      fondait à tort le statut de la stratégie C5-ETENDU-10.
    ⑨ CE QUI CLOCHE —
      ① Le calibrage annoncé par ce texte n'est rejouable par rien. Le texte
      affirme « la valeur principale est retrouvee EXACTEMENT, 33 episodes a 5
      seances ». Recherche du nom `episodes` dans le corps de `_calibrage` le
      19-09-2026 : absent. C'est précisément le défaut que le texte de
      `_calibrage` dit avoir fermé le 29-08-2026 — un calibrage qu'on ne peut
      pas rejouer est une affirmation, pas un calibrage — et il est resté ouvert
      pour cette fonction.
      ② Les deux valeurs secondaires annoncées ne sont pas retrouvées, et le
      texte le dit sans le trancher : 26 et 19 obtenus contre 28 et 20
      documentés. L'explication avancée, cinq séances ajoutées par une
      réparation du 25-08-2026, est écrite comme une hypothèse et n'a pas été
      vérifiée depuis.
      ③ Les opérations dont la date de signal n'est pas au calendrier
      DISPARAISSENT du comptage sans un mot. La case rendue qui compte les
      opérations porte le total reçu, mais les épisodes ne sont construits que
      sur les dates reconnues : sur un jeu où la moitié des dates seraient
      inconnues, le nombre moyen d'opérations par épisode serait deux fois trop
      grand, et rien ne le signalerait.
      ④ Le seuil de 5 séances vit dans la signature et nulle part ailleurs. Il
      vient du BACKLOG, action A-210, et non du REGISTRE : recherche du mot
      « episode » dans `gouvernance/REGISTRE_REGLES.md` à faire avant tout
      changement. Le modifier ici changerait le nombre d'observations déclaré
      sans trace dans la loi du projet.
    ⑩ EFFET — Aucun : elle lit. Aucun fichier, aucun réseau, aucune donnée
      modifiée, rien d'affiché. Elle construit une copie triée du calendrier.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas dans les cas que
      son appelant lui donne : le juge des stratégies enveloppe malgré tout l'appel et
      afficherait « EPISODES non mesures » suivi du message. Aucun de ses
      appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      un épisode : un groupe de signaux assez proches dans le temps pour
        décrire le même mouvement de marché, et qui ne compte donc que pour une
        observation
      une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
      le signal : le jour où la stratégie dit d'acheter ; l'achat lui-même a
        lieu à l'ouverture de la séance suivante
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
      le BACKLOG : `BACKLOG_DECISIONS.md`, le tableau daté des décisions et des
        actions du projet, où chaque ligne porte un identifiant en `A-`
    
      C5-ETENDU-10 : le nom de la stratégie vivante ; ses seuils et son horizon sont lus dans `donnees/cac40_strategies.csv`.
      l'horizon : le nombre de séances pendant lesquelles une position est tenue si ni l'objectif de gain ni la perte acceptée ne sont atteints
      le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
      un motif : un morceau de nom passé à une fonction de recherche, par exemple trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
      un réglage : un des nombres qui définissent une stratégie — l'objectif de gain, la perte acceptée, l'horizon
"""
    if not ops:
        return {"n_operations": 0, "n_episodes": 0}
    rang = {d: i for i, d in enumerate(sorted(seances_projet))}
    jours = sorted({o["date_signal"] for o in ops if o["date_signal"] in rang})
    if not jours:
        return {"n_operations": len(ops), "n_episodes": None,
                "motif": "aucune date de signal reconnue au calendrier"}
    n = 1
    for a, b in zip(jours, jours[1:]):
        if rang[b] - rang[a] > seuil:
            n += 1
    return {"n_operations": len(ops), "n_jours_signal": len(jours),
            "n_episodes": n, "seuil_seances": seuil,
            "operations_par_episode": round(len(ops) / n, 2)}


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
      le sens qui flatte la stratégie.
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
                  mode="valeur", n_tirages=200, graine=GRAINE):
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
    ③ ENTRÉE — `ops` : les opérations réelles, dont seule la case `date_signal`
      est lue, et dont le NOMBRE fixe combien d'entrées seront tirées ·
      `cours` : l'historique, une liste de séances par valeur, chaque séance
      portant sa date, son ouverture, son plus haut, son plus bas et sa clôture ·
      `univers` : les valeurs dans lesquelles tirer · `tp` : l'objectif de gain
      en FRACTION · `sl` : la perte acceptée en FRACTION et en valeur positive ·
      `horizon` : le nombre de séances pendant lesquelles la position est tenue ·
      `mod_positions` : le module qui décide si une séance fait sortir, et le
      juge des stratégies y passe `programmes/MODULE_POSITIONS.py` · `mode` : « valeur » par
      défaut · `n_tirages` : 200 par défaut, et l'appelant passe 120 ·
      `graine` : 20260828 par défaut.
    ④ CONDITIONS D'ENTRÉE — L'univers passé doit être celui de la FICHE et non
      celui du projet entier. Chaque valeur retenue doit porter plus de séances
      que l'horizon plus trois. Le module passé doit porter une fonction
      `tester_seance(seance, prix_objectif, prix_stop)`.
    ⑤ SORTIE — UNE valeur : un dictionnaire, et il prend DEUX formes
      différentes. Quand l'univers ou les opérations sont insuffisants, ou
      qu'aucun tirage n'a pu être exploité : deux cases, un nombre de tirages à
      zéro et un motif en clair. Sinon huit cases : le mode, le nombre de
      tirages retenus, trois taux de réussite — médian, au quatre-vingt-quinzième
      centile, maximal — trois gains aux mêmes rangs, et la graine.
      [rend: 1]
    ⑥ TRAITEMENT — ① ne garder que les valeurs assez longues · ② dresser, pour
      chaque date de séance, la liste des valeurs disponibles ce jour-là ·
      ③ fixer la suite de tirages avec la graine · ④ répéter autant de fois que
      demandé : pour chaque opération réelle, tirer une entrée — en mode
      « valeur », une valeur parmi celles cotées à la date du signal réel ;
      sinon, une valeur et une date au hasard · ⑤ acheter à l'ouverture de la
      séance suivante · ⑥ parcourir, DEPUIS LA SÉANCE D'ACHAT (R-608, depuis le
      28-09-2026), les séances jusqu'à l'horizon et sortir dès qu'une séance touche
      l'objectif ou le stop, sinon sortir à la clôture de la h-ième séance après
      l'achat · ⑦ cumuler le gain net et le nombre de gagnantes ·
      ⑧ trier les taux et les gains des tirages, et rendre trois rangs de
      chacun.
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
      ② RÉGLÉ LE 28-09-2026 (A-435 ④) : le gain net se calcule par
      `mod_positions.pnl_net`, comme celui de la stratégie ; épreuve dans
      tests/EPREUVES_DES_FRAIS_DU_HASARD_Lun_28-09-2026.py. Ce qui était mesuré :
      les frais sont un forfait de 300 € écrit dans ce fichier, alors que la
      stratégie à laquelle l'étalon sera comparé paie 0,15 % de la valeur
      échangée à l'entrée ET à la sortie. Mesuré le 19-09-2026 sur un
      aller-retour de 100,00 € à 104,00 € avec 100 000 € engagés :
      `MODULE_POSITIONS.pnl_net` rend 3 694,00 € quand la formule employée ici
      rend 3 700,00 €, soit 6,00 € d'écart sur ce gain ; sur une perte à −2,5 %
      l'écart s'inverse, −3,75 € (relecteur du Chat, 28-09-2026 : il vaut 1,50 € par
      point de pourcentage de rendement). Un chiffre qui existe ailleurs ne se recopie
      pas (R-708) : le taux vit dans `MODULE_POSITIONS.FRAIS_TAUX`.
      ③ Aucun contrôle d'unité sur l'objectif et la perte acceptée. Mesuré le
      19-09-2026 : un appel avec 4.0 et 2.5, c'est-à-dire des pourcents au lieu
      de fractions, est accepté sans broncher et rend un taux de réussite médian
      de 100,0 %, parce qu'un objectif de +400 % ne se touche jamais et que la
      sortie se fait alors à la clôture. La fonction `_exiger_des_fractions` du
      même fichier ferme ce contrat pour le point mort, pas ici.
      ④ Des tirages sont abandonnés en silence. Une entrée tirée sur la dernière
      séance d'une valeur, ou une date sans aucune valeur cotée, est passée sans
      être comptée. Le nombre d'opérations réellement jouées par tirage n'est pas
      rendu : deux tirages qui auraient joué 6 et 3 opérations sont comparés
      comme s'ils étaient équivalents, et seul le taux de réussite est ramené à
      l'effectif, pas le gain.
      ⑤ Aucun contrôle de calibrage ne la couvre. Recherche du nom
      `etalon_hasard` dans le corps de `_calibrage` le 19-09-2026 : absent. La
      vérification citée dans ce texte — le hasard rend 43 % là où le point mort
      est à 43,1 % — n'est rejouable par rien.
    ⑩ EFFET — Aucun sur les données reçues : elle lit. Aucun fichier, aucun
      réseau, rien d'affiché. Elle EXÉCUTE la fonction `tester_seance` du module
      qu'on lui passe, jusqu'à une fois par séance de détention et par tirage.
      Elle construit en mémoire un index de toutes les dates de l'historique.
    ⑪ TERMINAISON — Rend toujours la main dans les cas que son appelant lui
      donne. PEUT LEVER si le module passé ne porte pas `tester_seance` ; le
      juge des stratégies rattrape et affiche « HASARD non mesure ». Un de ses appels
      peut ne pas revenir : `tester_seance` de `MODULE_POSITIONS` rend toujours
      la main.
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
    dispo = [v for v in univers if v in cours and len(cours[v]) > horizon + 3]
    if not dispo or not ops:
        return {"n_tirages": 0, "motif": "univers ou operations insuffisants"}
    cal = {}
    for v in dispo:
        for i, b in enumerate(cours[v]):
            cal.setdefault(b["date"], []).append((v, i))
    r = random.Random(graine)
    taux, gains = [], []
    for _ in range(n_tirages):
        g = n = 0
        somme = 0.0
        for o in ops:
            if mode == "valeur":
                cands = cal.get(o["date_signal"], [])
                if not cands:
                    continue
                v, i = cands[r.randrange(len(cands))]
            else:
                v = dispo[r.randrange(len(dispo))]
                i = r.randrange(0, len(cours[v]) - horizon - 2)
            s = cours[v]
            if i + 1 >= len(s):
                continue
            pe = s[i + 1]["open"]
            tp_a, sl_a = pe * (1 + tp), pe * (1 - sl)
            px = None
            # LA SEANCE D'ACHAT COMPTE AUSSI POUR LE HASARD (R-608 ; defaut 4 de A-491,
            # 28-09-2026, trouve par le relecteur du Chat) : le hasard se joue avec la
            # meme mecanique que la strategie qu'il juge, celle de `jouer` dans le juge des stratégies —
            # seuils des s[i + 1], echeance h seances APRES l'achat.
            for b in s[i + 1:i + 2 + horizon]:
                res = mod_positions.tester_seance(b, tp_a, sl_a)
                if res:
                    px = res[0]
                    break
            if px is None:
                suite = s[i + 2:i + 2 + horizon]      # l'echeance se compte APRES l'achat
                if not suite:
                    continue
                px = suite[-1]["close"]
            # LES FRAIS DU HASARD SONT CEUX DE LA STRATÉGIE (R-708, A-435 ④, 28-09-2026) :
            # le forfait de 300 € d'ici rendait 3 700,00 € sur un aller-retour de 100 à
            # 104 € que le module des positions compte 3 694,00 € : +6 € pour le hasard sur
            # ce gain, −3,75 € sur une perte à −2,5 % (l'écart vaut 1,50 € par point de pourcentage de rendement).
            # Le calcul vit chez son propriétaire.
            net = mod_positions.pnl_net(pe, px)
            n += 1
            g += 1 if net > 0 else 0
            somme += net
        if n:
            taux.append(100.0 * g / n)
            gains.append(somme)
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
            "graine": graine}


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
      défaut a été fermé partout.
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

    # les deux points mort documentes dans l'ETUDE 11, frais historiques
    dire("point mort +4,0/-2,5 = 43,08 %", round(point_mort_en_fractions(0.040, 0.025, frais=FRAIS), 2), 43.08, 0.01)
    dire("point mort +1,2/-1,0 = 59,09 %", round(point_mort_en_fractions(0.012, 0.010, frais=FRAIS), 2), 59.09, 0.01)

    # ON ECRIT LE CONTROLE DE CE QU'ON VIENT DE CHANGER, PAS DE CE QU'ON VIENT
    # DE VOIR. Les deux controles ci-dessus appellent la branche de REPLI, avec
    # des frais forfaitaires : ils ne touchent jamais le calcul a deux branches
    # ajoute le 29/08. Prouve par sabotage le jour meme — en remettant les frais
    # du gain sur les deux branches, le calibrage passait TOUJOURS.
    # Troisieme fois dans la journee qu'une correction reste sans filet.
    class _Faux:
        FRAIS_TAUX = 0.0015
        @staticmethod
        def frais_ordre(q, prix, taux=None):
            """Rend les frais d'un ordre, pour le seul besoin du calibrage.

            ① RÔLE — Tenir la place de la vraie fonction de frais pendant le calibrage, pour
            que celui-ci tourne même quand le module des positions n'est pas chargeable. Elle
            n'est pas le calcul du système : elle en est un double de secours.
            ② CONTEXTE D'APPEL — Définie dans la classe `_Faux`, elle-même construite par le
            calibrage quand `programmes/MODULE_POSITIONS.py` ne peut pas être chargé. Aucun
            autre appelant.
            ③ ENTRÉE — `q` : la quantité de titres · `prix` : le prix unitaire en euros ·
            `taux` : le taux de frais, `None` par défaut.
            ④ CONDITIONS D'ENTRÉE — `q` et `prix` doivent être des nombres.
            ⑤ SORTIE — UNE valeur : le montant des frais, en euros.
              [rend: 1]
            ⑥ TRAITEMENT — ① multiplier la quantité par le prix par 0,0015 · ② rendre le
            résultat.
            ⑦ UNITÉ — Le résultat est en EUROS. Le taux est une fraction, pas un pourcent :
            0,0015 vaut 0,15 %.
            ⑧ POURQUOI — Le calibrage doit pouvoir tourner seul, sans dépendre du chargement
            d'un autre fichier. C'est ce qui permet de le lancer depuis un dossier quelconque.
            ⑨ CE QUI CLOCHE — DEUX POINTS. ① **Le taux 0,0015 est recopié ici en dur**, alors
            que le taux du système vit à un seul endroit, `MODULE_POSITIONS.FRAIS_TAUX`,
            relevé à 0.0015 le 20-09-2026. Les deux concordent aujourd'hui ; rien ne le
            garantit demain, et deux implémentations d'une même chose divergent toujours
            (R-708). ② **Le paramètre `taux` n'est jamais employé** : appelée avec
            `taux=0.0025`, elle rend quand même le montant calculé à 0,0015. Un appelant qui
            croit choisir le taux ne choisit rien. Relevé par lecture du code le 20-09-2026,
            non provoqué.
            ⑩ EFFET — Aucun.
            ⑪ TERMINAISON — Rend toujours la main. Aucun de ses appels ne peut ne pas revenir.
              [sort: non]
            """
            return 0.0015 * q * prix
    _pm = point_mort_en_fractions(0.05, 0.02, mod_positions=_Faux)
    dire("point mort a deux branches de frais = 32,86 %", round(_pm, 2), 32.86, 0.01)
    # une sortie au stop coute MOINS cher qu'une sortie au gain : si les deux
    # branches etaient confondues, le point mort remonterait a 32,96
    dire("les deux branches different bien", round(_pm, 2) != 32.96, True)

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
