"""
GROUPE 2 · outil — CONTROLER LES COURS (R-104)
Dim 06-09-2026 09h45 (Paris)

CE QUE FAIT CE PROGRAMME
------------------------
Il applique le contrôle R-104 aux séances nouvelles avant qu'elles n'entrent
dans le fichier des cours, puis il les y ajoute. C'est l'ÉTAPE 2 et l'ÉTAPE 5
des trois boucles, qui vivaient en français dans le prompt.

POURQUOI IL EXISTE
------------------
Un prompt en français est réinterprété à chaque exécution. Un programme fait
la même chose tous les soirs, et son empreinte le prouve. Le 05-09-2026, la
photographie de l'écosystème comptait 8 étapes de prompt pour le seul bloc des
cours : c'est le bloc le moins programmé de tout le système, et celui qui
alimente tous les autres.

LES QUATRE TESTS, ET LEUR NATURE DIFFÉRENTE
-------------------------------------------
TROIS SONT BLOQUANTS, parce que ce sont des IMPOSSIBILITÉS, pas des événements :
  · High >= Low
  · Open et Close dans [Low, High]
  · Volume > 0
Une séance qui viole l'un des trois est une donnée fausse. On n'écrit rien.

LE QUATRIÈME N'EST PAS BLOQUANT : une variation de clôture au-delà de 25 %.
C'est un seuil de SUSPICION, pas de rejet. La PASSATION du 28-07-2026 §7 écrit
« au-delà : suspect SAUF ANNONCE CONNUE ». Une action peut légitimement bouger
de plus de 25 % sur un résultat, une offre de rachat ou un profit warning.
Le prompt avait durci ce seuil en refus, et la nuance avait disparu en chemin :
le jour où une valeur publierait un résultat brutal, la boucle se serait
arrêtée en refusant une séance parfaitement réelle. Corrigé le 05-09-2026.

CE QU'IL N'EST PAS
------------------
Il ne va PAS chercher la feuille Google : c'est un geste d'agent, il reste au
prompt. Il reçoit des séances déjà lues et décide de leur sort.

APPELÉ PAR
----------
Les trois boucles (07h05, 08h35, 21h05), à l'étape 2 puis à l'étape 5.
════════════════════════════════════════════════════════════════════════
LES DOUZE ÉLÉMENTS — R-752 les pose à tous les niveaux, et le programme
entier est le premier niveau
════════════════════════════════════════════════════════════════════════
① RÔLE — Être le seul juge de ce qui entre dans le fichier des cours, et le
  seul écrivain de ce fichier. Les deux programmes qui vont chercher les cours
  sur le web lisent une page et convertissent des nombres ; ils ne décident
  rien. C'est ce module qui dit si une séance est vraisemblable, qui ramène
  les noms de valeurs et les dates à une seule forme, qui refuse les doublons,
  et qui écrit. Deux implémentations d'une même chose divergent toujours
  (R-708) : c'est la raison pour laquelle ce travail vit ici, et nulle part
  ailleurs.
② CONTEXTE D'APPEL — Il ne se lance pas de lui-même, il s'importe. UN SEUL
  APPELANT AUTOMATIQUE : programmes/COLLECTER_ABC_GITHUB.py, qui porte la
  ligne `import CONTROLER_LES_COURS as C` et lui prend quatre fonctions —
  `normaliser_valeur`, `normaliser_date`, `controler` et `ajouter_au_fichier`.
  Ce programme de collecte est lancé par la tâche planifiée
  .github/workflows/collecte_abc.yml, du lundi au vendredi à 18 h UTC, ce qui
  fait 20 h à Paris en été et 19 h en hiver. Un second importateur existe,
  programmes/COLLECTER_LES_COURS_ABC.py, qu'aucune tâche planifiée ne lance :
  relevé le 19-09-2026, aucun des deux fichiers de .github/workflows/ ne le
  nomme. Ce module se lance aussi à la main, avec l'argument `epreuves`, et
  joue alors son jeu d'épreuves sans rien écrire.
③ ENTRÉE — Rien sur la ligne de commande, sauf le mot `epreuves`. Tout arrive
  par les appels : une liste de séances et un tableau des clôtures
  précédentes pour `controler`, une liste de séances et un chemin de fichier
  pour `ajouter_au_fichier`. Un fichier est lu de son propre chef, et un
  seul : temoins/TEMOIN_cours_reels.csv, et uniquement par le jeu d'épreuves.
④ CONDITIONS D'ENTRÉE — Une séance est un dictionnaire portant les clés
  `valeur`, `date`, `open`, `high`, `low`, `close` et `volume` — les sept
  colonnes que programmes/CONTRATS_DES_FICHIERS.py déclare sous le nom
  COURS_NOUVEAUX pour le fichier donnees/claude_cours_nouveaux.csv. Le fichier
  d'arrivée peut ne pas exister : il est alors créé. Pour le jeu d'épreuves, le
  fichier temoins/TEMOIN_cours_reels.csv doit être présent ET inchangé, à
  l'octet près.
⑤ SORTIE — Importé, il ne rend rien lui-même : ce sont ses fonctions qui
  rendent. Lancé avec `epreuves`, il rend un code de sortie et affiche une
  ligne par test. Mesuré le 19-09-2026 sur une copie du dépôt : « 16/16 cas
  passent », code 0.
⑥ TRAITEMENT — ① ramener chaque nom de valeur et chaque date à une forme
  unique · ② appliquer à chaque séance les quatre tests de vraisemblance ·
  ③ arrêter tout le lot à la première impossibilité · ④ écarter les séances
  déjà présentes et celles antérieures au 10-07-2026 · ⑤ refuser d'écrire une
  ligne incomplète ou une date illisible · ⑥ ajouter à la fin du fichier, sans
  jamais le réécrire · ⑦ relire le fichier et lever si le compte ne tombe pas.
⑦ UNITÉ — Les prix sont en EUROS, le volume en TITRES, les dates au format
  AAAA-MM-JJ. La variation de clôture est un POURCENTAGE, avec un seuil de
  25 %. Le plancher des séances acceptées est une DATE, le 10-07-2026.
  L'horodatage affiché par le jeu d'épreuves est en heure de Paris.
⑧ POURQUOI — Quatre choix commandent tout le reste.
  ① Trois tests bloquent et un seul alerte. Une clôture hors de l'intervalle
  du jour est une impossibilité arithmétique, donc une donnée fausse ; une
  variation de 30 % est un événement, et les événements existent. Le 19-09-2026,
  une clôture passant de 31,74 à 44,44 euros, soit +40,0 %, a été signalée et
  écrite — c'est le comportement voulu.
  ② Le lot entier est jugé avant qu'une seule ligne soit écrite. Une séance
  fausse rend tout le lot suspect, et mieux vaut ne rien écrire que d'en écrire
  la moitié : le fichier des cours ne se réécrit jamais, donc une ligne fausse
  y reste.
  ③ Les noms et les dates sont ramenés à une forme unique avant toute
  comparaison. Une même entreprise s'écrit `BUREAU_VERITAS`, `BUREAU VERITAS`
  ou `Bureau Veritas` selon la source ; mesuré le 19-09-2026, les trois
  donnent ici `BUREAU_VERITAS`. Sans ce rapprochement, trois lignes de la même
  société passent pour trois sociétés, aucun doublon n'est vu, et personne ne
  s'en aperçoit.
  ④ Le jeu d'épreuves prend une vraie ligne du fichier des cours, la joue
  telle quelle puis sabotée. Neuf défauts du 06-09-2026 étaient passés entre
  des tests entièrement écrits à la main : un jeu d'épreuves contient au moins
  un exemple venu d'une vraie ligne du fichier (R-732).
⑨ CE QUI CLOCHE —
  ① Le registre annonce cinq contrôles, le programme en fait quatre. La règle
  R-104 de gouvernance/REGISTRE_REGLES.md, relevée le 19-09-2026, énonce :
  « High≥Low · Open,Close∈[Low,High] · Volume>0 · |var|<25 % · croisement
  externe 3 valeurs/jour (écart >0,5 % = alerte) ». Le cinquième — comparer
  chaque jour trois valeurs à une seconde source — n'existe nulle part dans ce
  fichier. Or c'est le seul qui verrait un chiffre glissé dans un volume, du
  genre 3 654 181 écrit pour 3 664 181 : les quatre autres ne regardent le
  volume que comme « plus grand que zéro ».
  ② Le registre dit « pas d'append » en cas d'anomalie, le programme écrit
  quand même. La même règle R-104 finit par « anomalie → ALERTE + pas de trade
  + pas d'append ». Mesuré le 19-09-2026 sur une copie du dépôt : une clôture
  de VEOLIA passant de 31,74 à 44,44 euros rend le verdict ALERTE, et la ligne
  est bel et bien dans le fichier après l'appel. L'écriture n'est refusée que
  sur un verdict BLOQUANT.
  ③ La date plancher du 10-07-2026 est écrite dans trois fichiers :
  programmes/CONTROLER_LES_COURS.py, programmes/COLLECTER_ABC_GITHUB.py et
  programmes/COLLECTER_LES_COURS_ABC.py, chacun sous le nom `DATE_PLANCHER`.
  Cette date est celle de la dernière séance de l'historique figé, que
  gouvernance/PILOTE.md annonce au 2026-07-10. Un chiffre qui existe ailleurs
  ne se recopie pas (R-708) : corriger l'un des trois sans les autres les
  ferait diverger en silence.
  ④ Le seuil de 25 % est écrit deux fois dans ce même fichier, une fois comme
  nombre dans `SEUIL_VARIATION` et une fois en toutes lettres dans le texte
  d'en-tête. Changer le nombre sans changer le texte ferait mentir
  l'explication sans qu'aucun test ne s'en aperçoive.
  ⑤ Le seuil est franchi au-delà de 25 %, alors que le registre écrit
  « |var|<25 % » : à exactement 25 %, la règle dit d'alerter et le programme
  dit OK. Mesuré le 19-09-2026 : une clôture passant de 100,0 à 125,0 rend
  « OK » ; la même à 125,01 rend « ALERTE ».
  ⑥ Le module ne connaît aucune date. Aucun test ne regarde si la date d'une
  séance est plausible. Mesuré le 19-09-2026 : une séance datée du 2099-01-01,
  par ailleurs cohérente, est acceptée et écrite sans un mot.
⑩ EFFET — Importé, il n'écrit rien tant qu'on n'appelle pas
  `ajouter_au_fichier` ; celle-ci AJOUTE à la fin du fichier qu'on lui nomme et
  ne le réécrit jamais. Lancé avec `epreuves`, il LIT
  temoins/TEMOIN_cours_reels.csv et n'écrit aucun fichier. AUCUN ACCÈS RÉSEAU,
  dans aucun des deux modes. Ne touche jamais donnees/cac40_ohlcv.csv,
  l'historique figé, ni aucun fichier de gouvernance, et ne supprime rien.
⑪ TERMINAISON — Importé, il ne termine rien : le programme appelant garde la
  main. Lancé avec `epreuves`, il SORT DU PROGRAMME avec trois codes, tous
  mesurés le 19-09-2026 sur une copie du dépôt : 0 quand les seize tests
  passent · 1 quand au moins un ne passe pas · 2 quand les tests n'ont PAS PU
  tourner, parce que temoins/TEMOIN_cours_reels.csv est absent ou a changé.
  Ce 2 distinct du 1 est voulu : « n'a pas pu tourner » n'est pas « a tourné
  et a échoué ».
⑫ DÉFINITIONS
  une séance : une journée de bourse pour une valeur, avec son ouverture, son
    plus haut, son plus bas, sa clôture et son volume.
  le fichier des cours : le fichier où les séances s'empilent sans jamais être
    réécrites ; au dépôt, c'est donnees/claude_cours_nouveaux.csv.
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
    étant qu'une copie de lecture
  le jeu d'épreuves : les cas de contrôle que le programme lance sur lui-même,
    avec l'argument `epreuves`
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par
    GitHub Actions — collecte, versement, signaux, positions, mesure,
    surveillance.
  la tâche planifiée : un fichier de .github/workflows/ qui fait tourner un
    programme à heure fixe sur une machine GitHub, sans clic ni autorisation.
  la photographie : un document qui décrivait chaque
    programme et chaque fonction de l'écosystème, abandonné le 24-09-2026 et rangé aux archives (A-452).
  le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
  l'historique figé : donnees/cac40_ohlcv.csv, le fichier de cours de référence qui n'est jamais réécrit
  la boucle : la tache planifiee qui lit les signaux et rend compte
  la raison : le texte court qui dit pourquoi une lecture a échoué, retenu sous le nom `motif`
  une action : une ligne de ce tableau, identifiée par `A-` suivi d'un nombre
"""

import csv
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo


SEUIL_VARIATION = 0.25          # 25 % — suspicion, jamais rejet
DATE_PLANCHER = "2026-07-10"    # les séances antérieures ne s'ajoutent pas


def _maintenant():
    """Rend l'instant présent, en heure de Paris.

    ① RÔLE — Donner au jeu d'épreuves l'heure qu'il affiche en tête de son
      rapport, pour qu'une sortie collée dans une conversation porte la date et
      l'heure de sa production. Sans elle, deux sorties identiques seraient
      indistinguables et personne ne saurait laquelle est la plus récente.
    ② CONTEXTE D'APPEL — Le lancement du programme avec l'argument `epreuves`,
      une seule fois, dans la ligne affichée avant le premier test. Aucun autre
      appelant : le 19-09-2026, une recherche du nom `_maintenant` dans tous les
      fichiers de programmes/ et dans .github/workflows/ ne rend aucune ligne
      hors de ce fichier.
    ③ ENTRÉE — Aucun paramètre.
    ④ CONDITIONS D'ENTRÉE — Aucune, sauf que la table des fuseaux horaires du
      système porte `Europe/Paris`.
    ⑤ SORTIE — UNE valeur : l'instant présent, portant le fuseau de Paris.
      [rend: 1]
    ⑥ TRAITEMENT — ① demander l'heure courante au système en lui imposant le
      fuseau `Europe/Paris`.
    ⑦ UNITÉ — Un INSTANT, en heure de Paris, jamais en heure universelle.
    ⑧ POURQUOI — Le fuseau est imposé au lieu d'être laissé à la machine parce
      que les machines de ce projet ne sont pas à l'heure de Paris : la tâche
      planifiée .github/workflows/collecte_abc.yml se déclenche à 18 h UTC, ce
      qui fait 20 h à Paris en été et 19 h en hiver. Un horodatage pris à
      l'heure de la machine décalerait l'affichage d'une à deux heures selon la
      saison, et deux rapports du même soir paraîtraient venir de deux moments
      différents.
    ⑨ CE QUI CLOCHE —
      ① Son nom laisse croire à une horloge du programme, alors qu'elle ne sert
      qu'à un affichage. Le reste du module n'a aucune notion de temps : aucun
      test ne regarde si la date d'une séance est plausible. Mesuré le
      19-09-2026 sur une copie du dépôt : une séance datée du 2099-01-01, par
      ailleurs cohérente, est jugée « SANS_REFERENCE » puis écrite au fichier
      sans un mot.
    ⑩ EFFET — Aucun. Elle ne lit aucun fichier, n'en écrit aucun, n'affiche rien
      et ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main. Elle PEUT LEVER si la machine ne connaît pas
      le fuseau `Europe/Paris`, et cette levée n'est pas rattrapée ici. Aucun de
      ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
  une séance : une journée de bourse pour une valeur, avec son ouverture, son
    plus haut, son plus bas, sa clôture et son volume.
  le jeu d'épreuves : les cas de contrôle que le programme lance sur lui-même,
    avec l'argument `epreuves`
      la tâche planifiée : un fichier de .github/workflows/ qui fait tourner un
        programme à heure fixe sur une machine GitHub, sans clic ni autorisation.
    
    
  PRODUCTION : l etat d une strategie dont le seuil d operations est atteint et les resultats conformes, donc exploitee.
  la table : `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740, qui porte les neuf seuils et le sens de comparaison de chacun
"""
    return datetime.now(ZoneInfo("Europe/Paris"))


def _nombre(x):
    """Rend un float, ou None si la valeur est vide ou illisible.

    ① RÔLE — Traduire ce qu'une source écrit en ce qu'un calcul peut comparer,
      et dire « rien » plutôt que de tomber quand la traduction est impossible.
      Une page web écrit « 78,20 » et « 1 000 » ; un test de vraisemblance a
      besoin de 78.2 et de 1000.0. C'est le seul endroit du module qui sait lire
      un nombre, et c'est ce qui permet aux cinq champs chiffrés d'une séance
      d'être jugés de la même façon.
    ② CONTEXTE D'APPEL — `controler_une_seance`, six fois par séance : une fois
      pour l'ouverture, le plus haut, le plus bas, la clôture, le volume, et une
      sixième pour la clôture précédente. Sur un passage du soir portant
      quarante valeurs, quelques centaines d'appels. Aucun autre appelant : le
      19-09-2026, une recherche du nom `_nombre` dans tous les fichiers de
      programmes/ ne rend, hors de ce fichier, que les définitions distinctes de
      programmes/COLLECTER_ABC_GITHUB.py et de
      programmes/COLLECTER_LES_COURS_ABC.py, qui ne sont pas celle-ci.
    ③ ENTRÉE — `x` : la valeur à lire, telle qu'elle vient du dictionnaire de la
      séance. Elle peut être un nombre déjà converti, un texte, ou rien du tout.
      Un seul appelant, `controler_une_seance`, qui passe sans les modifier les
      valeurs qu'il a lues dans la séance reçue, par exemple 58.0, `10,5`,
      `1 000` ou `#N/A`.
    ④ CONDITIONS D'ENTRÉE — Aucune. Tout lui est passable, y compris rien : elle
      ne tombe sur aucune valeur.
    ⑤ SORTIE — UNE valeur : le nombre en virgule flottante, ou « rien » quand la
      lecture est impossible. Mesuré le 19-09-2026 : `4 225 636` écrit avec des
      espaces ordinaires rend 4225636.0, et le même nombre écrit avec l'espace
      fine insécable rend « rien ».
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre « rien » si la valeur est absente · ② passer par le
      texte, retirer les blancs de début et de fin · ③ changer la virgule
      décimale en point · ④ retirer les espaces ordinaires puis les espaces
      insécables, qui séparent les milliers · ⑤ rendre « rien » sur un texte
      vide ou sur l'un des trois refus connus, `-`, `#N/A` et `N/A` · ⑥ convertir,
      et rendre « rien » si la conversion échoue.
    ⑦ UNITÉ — Celle du champ reçu : des EUROS pour les quatre prix, des TITRES
      pour le volume. La fonction ne le sait pas et ne peut pas le vérifier.
    ⑧ POURQUOI — Elle rend « rien » au lieu de lever, parce que son appelant a
      besoin de NOMMER le champ fautif. Le message rendu par
      `controler_une_seance` sur une séance amputée est « champ illisible ou
      vide — volume » : c'est le nom de la colonne qui permet de comprendre, et
      une levée l'aurait perdu.
      Les trois refus `-`, `#N/A` et `N/A` sont écrits en clair parce qu'ils ne
      sont pas des erreurs de lecture mais des réponses de la source : une
      feuille de calcul qui ne connaît pas une valeur écrit `#N/A`, et un tiret
      est la façon dont une page dit « pas de cotation ce jour-là ».
    ⑨ CE QUI CLOCHE —
      ① Elle ne connaît pas l'espace fine insécable, celle qu'ABC Bourse emploie
      pour séparer les milliers. Elle retire l'espace ordinaire et l'espace
      insécable ordinaire, pas la fine. Mesuré le 19-09-2026 sur une copie du
      dépôt : `4 225 636` écrit avec cette espace rend « rien », et la séance
      entière devient « BLOQUANT — champ illisible ou vide — volume ». Si cette
      espace arrivait jusqu'ici, un lot entier de quarante valeurs serait refusé
      pour un volume parfaitement juste. Elle n'arrive pas aujourd'hui parce que
      les deux programmes de collecte la retirent avant d'appeler, mais aucun
      texte ne dit que c'est leur travail.
      ② Un champ absent et un champ illisible rendent la même chose : « rien ».
      L'appelant les range donc dans la même liste de champs manquants, et le
      message ne dit pas si la colonne était vide ou pleine d'un texte
      incompréhensible. Les deux n'ont pourtant pas la même cause : l'un est un
      trou dans la source, l'autre un problème de lecture.
      ③ Trois fonctions du dépôt portent ce nom et ne se comportent pas de la
      même façon. Mesuré le 19-09-2026 sur `4 225 636` écrit avec l'espace fine
      insécable : celle-ci rend « rien », celle de
      programmes/COLLECTER_LES_COURS_ABC.py rend 4225636.0, et celle de
      programmes/COLLECTER_ABC_GITHUB.py lève une erreur. Trois lectures du même
      chiffre, trois réponses : deux implémentations d'une même chose divergent
      toujours (R-708).
    ⑩ EFFET — Aucun. Elle ne lit aucun fichier, n'en écrit aucun, n'affiche rien
      et ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas : l'échec de
      conversion est rattrapé et rendu sous forme de « rien ». Aucun de ses
      appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
  une séance : une journée de bourse pour une valeur, avec son ouverture, son
    plus haut, son plus bas, sa clôture et son volume.
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
    étant qu'une copie de lecture
    
    """
    if x is None:
        return None
    s = str(x).strip().replace(",", ".").replace(" ", "").replace("\u00a0", "")
    if not s or s in ("-", "#N/A", "N/A"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def controler_une_seance(seance):
    """    Applique les quatre tests à UNE séance.

    seance : dict avec au moins valeur, date, open, high, low, close, volume.

    Rend (verdict, motif) où verdict vaut :
      "OK"       — la séance est écrivable, rien à signaler
      "ALERTE"   — écrivable, mais Jean-Luc doit être notifié (motif dit quoi)
      "BLOQUANT" — donnée impossible, ne pas écrire, arrêter la boucle

    ① RÔLE — Juger une journée de bourse, et elle seule : dire si elle peut
      entrer dans le fichier des cours, si elle doit être signalée, ou si elle
      est arithmétiquement impossible. Tout ce qui est écrit dans le fichier des
      cours est passé par ici, et le fichier ne se réécrit jamais : ce qui est
      accepté l'est pour toujours.
    ② CONTEXTE D'APPEL — Trois appelants. ① `controler`, une fois par séance du
      lot, après y avoir glissé la clôture précédente quand elle est connue.
      ③ depuis le 24-09-2026, `juger_la_ligne` de programmes/TENIR_L_HISTORIQUE.py,
      une fois par ligne versée au fichier maître.
      ② `_epreuves`, seize fois, sur des séances fabriquées pour l'occasion —
      neuf écrites à la main, six tirées d'une vraie ligne du fichier des cours,
      une ajoutée pour la date ambiguë. Aucun appelant hors de ce fichier :
      relevé le 19-09-2026, ni programmes/ ni .github/workflows/ ne nomment
      `controler_une_seance` ailleurs.
    ③ ENTRÉE — `seance` : le dictionnaire d'une journée de bourse, portant les
      clés `valeur`, `date`, `open`, `high`, `low`, `close` et `volume`, plus
      éventuellement `close_precedent`. Les deux appelants passent le
      dictionnaire sans le modifier, par exemple celui d'AIRBUS au 2026-08-07,
      qui est la ligne réelle employée par le jeu d'épreuves.
    ④ CONDITIONS D'ENTRÉE — Rien n'est obligatoire : une clé absente vaut une
      valeur illisible, et la séance est alors déclarée bloquante avec le nom de
      la colonne fautive. La valeur et la date ne servent qu'à composer les
      messages ; elles ne sont pas vérifiées.
    ⑤ SORTIE — DEUX valeurs : le verdict et son motif. Le verdict prend quatre
      formes, et non trois comme l'annonce le texte d'origine : « OK », motif
      vide · « ALERTE », motif disant la variation · « BLOQUANT », motif
      nommant l'impossibilité · « SANS_REFERENCE », motif disant que le
      quatrième test n'a pas tourné faute de clôture précédente.
      [rend: 2]
    ⑥ TRAITEMENT — ① relever le nom de la valeur et la date, pour les messages ·
      ② lire les cinq champs chiffrés · ③ si l'un d'eux est illisible, le nommer
      et bloquer · ③ bis test 0 : le plus bas doit être strictement positif —
      ajouté le 24-09-2026 · ④ test 1 : le plus haut ne peut pas être sous le plus bas ·
      ⑤ test 2 : l'ouverture et la clôture doivent tenir entre le plus bas et le
      plus haut · ⑥ test 3 : le volume doit être strictement positif · ⑦ test 4 :
      s'il n'y a pas de clôture précédente, le dire et s'arrêter là ; sinon
      calculer la variation et alerter au-delà du seuil · ⑧ rendre « OK ».
    ⑦ UNITÉ — Les quatre prix sont en EUROS, le volume en TITRES. La variation
      est un POURCENTAGE de la clôture précédente, et le seuil qui déclenche
      l'alerte vaut 25 %.
    ⑧ POURQUOI — Trois tests bloquent et un seul alerte, et cette différence est
      le cœur de la fonction. Un plus haut sous un plus bas, une clôture hors de
      l'intervalle du jour, un volume nul : ce sont des impossibilités, donc des
      données fausses. Une variation de 30 % en un jour est un événement — un
      résultat brutal, une offre de rachat, un avertissement sur les profits —
      et une action a le droit de bouger ainsi. Transformer ce quatrième test en
      refus arrêterait la collecte le jour où une valeur publie un mauvais
      résultat, en rejetant une séance parfaitement réelle.
      Le verdict « SANS_REFERENCE » existe parce qu'un test muet passe pour un
      test réussi. Le quatrième test a lu pendant des semaines une colonne
      `close_precedent` qui n'existe pas dans le fichier des cours, dont les
      sept colonnes sont `valeur`, `date`, `open`, `high`, `low`, `close` et
      `volume` : il ne s'est jamais déclenché, et son silence ressemblait
      exactement à « rien à signaler ». Un contrôle qui ne peut pas s'exécuter
      doit le dire (R-734).
    ⑨ CE QUI CLOCHE —
      ① Le texte d'origine de cette fonction annonce trois verdicts ; il y en a
      quatre. « SANS_REFERENCE » a été ajouté sans que ces lignes soient reprises.
      Un lecteur qui écrirait son appelant d'après ce texte traiterait le
      quatrième verdict comme un verdict inconnu.
      ② Le seuil est franchi au-delà de 25 %, alors que la règle R-104 de
      gouvernance/REGISTRE_REGLES.md, relevée le 19-09-2026, écrit « |var|<25 % ».
      À exactement 25 %, la règle demande une alerte et le programme rend « OK ».
      Mesuré le 19-09-2026 : une clôture passant de 100,0 à 125,0 rend « OK », la
      même à 125,01 rend « ALERTE ».
      ③ La ligne qui précède le calcul de la variation demande si la clôture
      précédente est absente, alors que les deux lignes au-dessus viennent de
      rendre la main dans ce cas exact. Cette question ne peut donc jamais être
      fausse. Ce n'est pas dangereux, mais cela laisse croire qu'il existe un
      chemin où la référence serait absente ici, et il n'y en a pas.
      ④ Une clôture précédente négative ou nulle est acceptée en silence. La
      variation n'est alors pas calculée, aucun message n'est rendu, et la séance
      sort en « OK » : un contrôle qui n'a pas tourné passe pour un contrôle
      réussi — exactement le défaut que le verdict « SANS_REFERENCE » avait été
      créé pour supprimer.
      ⑤ Aucun test ne regarde la date. Mesuré le 19-09-2026 : une séance datée du
      2099-01-01, par ailleurs cohérente, sort en « SANS_REFERENCE » et sera
      écrite. Une date dans le futur n'est pourtant pas moins impossible qu'un
      plus haut sous un plus bas.
      ⑥ Le volume n'est jugé que comme « plus grand que zéro ». Un chiffre glissé
      dans un volume — 3 654 181 écrit pour 3 664 181 — passe sans être vu. Seule
      une seconde source le verrait, et la règle R-104 en prévoit une : « croisement
      externe 3 valeurs/jour (écart >0,5 % = alerte) ». Ce cinquième contrôle
      n'existe nulle part dans ce fichier.
    ⑩ EFFET — Aucun. Elle ne lit aucun fichier, n'en écrit aucun, n'affiche rien
      et ne touche pas au réseau. Elle ne modifie pas non plus la séance reçue :
      elle se contente de la lire.
    ⑪ TERMINAISON — Rend toujours la main, par l'un de ses cinq points de sortie.
      Elle ne lève pas. Aucun de ses appels ne se termine : `_nombre` rend
      toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS
  une séance : une journée de bourse pour une valeur, avec son ouverture, son
    plus haut, son plus bas, sa clôture et son volume.
  le fichier des cours : le fichier où les séances s'empilent sans jamais être
    réécrites ; au dépôt, c'est donnees/claude_cours_nouveaux.csv.
  le jeu d'épreuves : les cas de contrôle que le programme lance sur lui-même,
    avec l'argument `epreuves`
    
    
  la boucle : la tache planifiee qui lit les signaux et rend compte
  une action : une ligne de ce tableau, identifiée par `A-` suivi d'un nombre
  une clé : le texte obtenu après rapprochement, qui sert à comparer deux noms et n'est jamais affiché à un lecteur
"""
    v = seance.get("valeur", "?")
    d = seance.get("date", "?")

    o = _nombre(seance.get("open"))
    h = _nombre(seance.get("high"))
    b = _nombre(seance.get("low"))
    c = _nombre(seance.get("close"))
    vol = _nombre(seance.get("volume"))

    manquants = [n for n, x in (("open", o), ("high", h), ("low", b),
                                ("close", c), ("volume", vol)) if x is None]
    if manquants:
        return "BLOQUANT", f"{v} {d} : champ illisible ou vide — {', '.join(manquants)}"

    # TEST 0 — UN PRIX EST STRICTEMENT POSITIF. Cassure de Cowork, 24-09-2026 : une
    # ligne aux quatre prix négatifs mais ordonnés passait les tests 1 et 2. Le plus
    # bas positif suffit : les tests 1 et 2 placent les trois autres au-dessus.
    if b <= 0:
        return "BLOQUANT", f"{v} {d} : Low {b} — un prix est strictement positif"

    # TEST 1 — High >= Low. Impossible autrement.
    if h < b:
        return "BLOQUANT", f"{v} {d} : High {h} < Low {b}"

    # TEST 2 — Open et Close dans [Low, High]. Impossible autrement.
    if not (b <= o <= h):
        return "BLOQUANT", f"{v} {d} : Open {o} hors de [{b}, {h}]"
    if not (b <= c <= h):
        return "BLOQUANT", f"{v} {d} : Close {c} hors de [{b}, {h}]"

    # TEST 3 — Volume > 0. Une séance sans échange n'est pas une séance.
    if vol <= 0:
        return "BLOQUANT", f"{v} {d} : Volume {vol}"

    # TEST 4 — variation de clôture. SUSPICION, JAMAIS REJET.
    # DÉFAUT ②, trouvé par Cowork le 06-09-2026 : ce test lisait `close_precedent`,
    # une colonne qui N'EXISTE PAS dans le fichier réel (valeur,date,open,high,low,
    # close,volume). Il ne s'est donc JAMAIS déclenché — et son silence était
    # indistinguable d'un « rien à signaler ». Toute la correction du 05-09 sur le
    # seuil de 25 % portait sur un test mort.
    # Corrigé : la clôture précédente est fournie par l'appelant via
    # `clotures_precedentes`, et son ABSENCE est dite, pas tue.
    ref = _nombre(seance.get("close_precedent"))
    if ref is None:
        return "SANS_REFERENCE", (f"{v} {d} : pas de clôture précédente — "
                                  f"le test de variation n'a PAS tourné")
    if ref is not None and ref > 0:
        var = (c - ref) / ref
        if abs(var) > SEUIL_VARIATION:
            return "ALERTE", (f"variation de {var*100:+.1f} % sur {v} le {d}, "
                              f"à vérifier — clôture {ref} → {c}")

    return "OK", ""


def controler(seances, clotures_precedentes=None):
    """    Applique le contrôle à une liste de séances.

    Rend (verdict_global, ecrivables, alertes, bloquant).
    À la PREMIÈRE anomalie bloquante, on s'arrête : la suite n'est pas contrôlée,
    et RIEN n'est écrivable. C'est voulu — une donnée fausse dans le lot rend le
    lot entier suspect.

    ① RÔLE — Juger un lot de séances comme un tout, et donner à l'appelant de
      quoi décider en un coup d'œil : ce qu'il peut écrire, ce qu'il doit
      signaler, et s'il doit tout abandonner. C'est la porte d'entrée du module :
      un programme de collecte ne parle jamais aux tests un par un, il lui passe
      son lot entier.
    ② CONTEXTE D'APPEL — Les deux programmes de collecte, une seule fois par
      passage, après avoir rassemblé toutes les séances nouvelles des quarante
      valeurs. programmes/COLLECTER_ABC_GITHUB.py, lancé chaque soir par la tâche
      planifiée .github/workflows/collecte_abc.yml, écrit
      `verdict_global, bonnes, alertes, bloquant = C.controler(a_ajouter,
      clotures_precedentes=cloture_prec)`. Aucun autre appelant : relevé le
      19-09-2026, aucun autre fichier de programmes/ n'appelle cette fonction.
    ③ ENTRÉE — `seances` : la liste des séances à juger, dans l'ordre où la
      collecte les a rassemblées · `clotures_precedentes` : un tableau qui donne,
      pour chaque nom de valeur normalisé, la dernière clôture déjà présente au
      fichier des cours, et qui vaut « rien » quand l'appelant n'en fournit pas.
      Les deux appelants passent, pour `seances`, la liste de toutes les séances
      neuves du passage, et pour `clotures_precedentes` un tableau construit en
      relisant donnees/claude_cours_nouveaux.csv.
    ④ CONDITIONS D'ENTRÉE — Les clés de `clotures_precedentes` doivent être des
      noms DÉJÀ normalisés, puisque la comparaison se fait sur le nom normalisé
      de la séance. Un tableau dont les clés porteraient des espaces ne
      rapprocherait rien, et le test de variation ne tournerait pour personne,
      sans qu'aucune erreur ne s'affiche.
    ⑤ SORTIE — QUATRE valeurs. ① le verdict du lot, « OK », « ALERTE » ou
      « BLOQUANT » · ② la liste des séances écrivables, vide si le lot est
      bloquant · ③ la liste des messages d'alerte · ④ le motif du refus, texte
      vide quand le lot n'est pas bloquant.
      [rend: 4]
    ⑥ TRAITEMENT — ① prendre une copie de chaque séance, pour ne pas modifier
      celle de l'appelant · ② y glisser la clôture précédente si elle est connue
      et si la séance n'en portait pas déjà une · ③ soumettre la séance aux
      quatre tests · ④ à la première impossibilité, tout arrêter et rendre un lot
      vide · ⑤ ranger les alertes d'un côté, les séances sans référence de
      l'autre · ⑥ déclarer écrivable toute séance qui n'a pas bloqué ·
      ⑦ ajouter, s'il y a eu des séances sans référence, une alerte qui dit
      combien · ⑧ rendre « ALERTE » s'il y a la moindre alerte, « OK » sinon.
    ⑦ UNITÉ — Un NOMBRE DE SÉANCES pour les listes rendues. Les prix des séances
      sont en euros et les volumes en titres, mais cette fonction ne les regarde
      pas elle-même.
    ⑧ POURQUOI — Le lot s'arrête à la première impossibilité et rend une liste
      vide, au lieu d'écrire les séances déjà jugées bonnes. Une donnée fausse
      dans un lot rend tout le lot suspect : elle vient probablement d'un défaut
      de lecture qui touche aussi les autres lignes. Le fichier des cours ne se
      réécrit jamais, donc une moitié écrite ne se retire pas ; ne rien écrire se
      rattrape le lendemain, écrire faux ne se rattrape pas.
      Le compte des séances sans référence est ajouté aux alertes parce qu'un
      contrôle muet passe pour un contrôle réussi, et c'est ce qui rend les
      pertes silencieuses invisibles. Un contrôle qui ne peut pas s'exécuter doit
      le dire (R-734).
    ⑨ CE QUI CLOCHE —
      ① Une séance signalée en ALERTE est déclarée écrivable, et elle est écrite.
      La règle R-104 de gouvernance/REGISTRE_REGLES.md, relevée le 19-09-2026,
      finit pourtant par « anomalie → ALERTE + pas de trade + pas d'append ».
      Mesuré le 19-09-2026 sur une copie du dépôt : une clôture de VEOLIA passant
      de 31,74 à 44,44 euros, soit +40,0 %, rend le verdict ALERTE, et la ligne
      est dans le fichier après l'appel à `ajouter_au_fichier`. L'appelant voit
      « écrites : 1 » et « alertes : 1 » et peut croire que la séance douteuse a
      été écartée.
      ② Un lot parfaitement sain rend le verdict « ALERTE » quand aucune clôture
      précédente n'est fournie. Mesuré le 19-09-2026 : une seule séance normale,
      appelée sans clôtures précédentes, rend « ALERTE » avec le message « TEST DE
      VARIATION NON EFFECTUÉ sur 1 séance(s) ». C'est un avertissement de méthode,
      pas une anomalie de donnée, et rien ne distingue les deux dans le verdict.
      ③ Une seule clôture de référence sert à tout un lot. L'appelant fournit la
      dernière clôture connue de chaque valeur, et cette même clôture est
      comparée à TOUTES les séances neuves de cette valeur, jusqu'à la plus
      récente. Mesuré le 19-09-2026 sur cinq séances montant chacune de 10 % —
      40, 44, 48, 52 puis 56 euros — avec 40,0 pour référence : deux alertes sont
      rendues, « variation de +30,0 % » et « variation de +40,0 % », alors
      qu'aucune journée n'a bougé de plus de 10 %. Un rattrapage de plusieurs
      jours alerte donc à tort, et symétriquement une vraie cassure noyée dans un
      rattrapage peut rester sous le seuil.
      ④ Seule la PREMIÈRE impossibilité est nommée. Mesuré le 19-09-2026 sur un
      lot de trois séances dont la deuxième a son plus haut sous son plus bas et
      la troisième un volume nul : le motif rendu est « B 2026-09-18 : High 9.0 <
      Low 11.0 », et le volume nul de la troisième n'est jamais nommé. Celui qui
      corrige la première cause relance et découvre la seconde, un passage plus
      tard.
      ⑤ Les séances qui ont bloqué sortent quand même de la boucle par la liste
      des écrivables — la ligne qui les y ajoute vient après les trois questions
      de verdict, sans exclusion. Cela ne se voit pas aujourd'hui, parce qu'un
      verdict bloquant rend la main immédiatement et que la liste est alors jetée.
      Le jour où l'arrêt immédiat serait retiré, les séances fausses passeraient
      pour écrivables.
      ⑥ **[Sans objet depuis le 24-09-2026 : la photographie est abandonnée, A-452.]** Le relevé automatique de la photographie ne savait reconnaître que « UNE
      valeur », « DEUX valeurs » ou « TROIS valeurs » dans un cinquième élément.
      Cette fonction en rend QUATRE : sa fiche sera donc signalée comme ne disant
      pas combien de valeurs elle rend, alors qu'elle le dit.
    ⑩ EFFET — Aucun sur les fichiers : elle ne lit rien, n'écrit rien, n'affiche
      rien et ne touche pas au réseau. Elle ne modifie pas non plus les séances
      qu'on lui donne : elle en prend une copie avant d'y glisser la clôture
      précédente, et ce sont les copies qu'elle rend.
    ⑪ TERMINAISON — Rend toujours la main, soit par la sortie du lot bloquant,
      soit par la sortie finale. Elle ne lève pas. Aucun de ses appels ne se
      termine : `normaliser_valeur` et `controler_une_seance` rendent toutes deux
      la main.
      [sort: non]
    ⑫ DÉFINITIONS
  une séance : une journée de bourse pour une valeur, avec son ouverture, son
    plus haut, son plus bas, sa clôture et son volume.
  le fichier des cours : le fichier où les séances s'empilent sans jamais être
    réécrites ; au dépôt, c'est donnees/claude_cours_nouveaux.csv.
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
    étant qu'une copie de lecture
      la tâche planifiée : un fichier de .github/workflows/ qui fait tourner un
        programme à heure fixe sur une machine GitHub, sans clic ni autorisation.
      la photographie : un document qui décrivait chaque
        programme et chaque fonction de l'écosystème, abandonné le 24-09-2026 et rangé aux archives (A-452).
    
    
  la boucle : la tache planifiee qui lit les signaux et rend compte
"""
    ecrivables, alertes, sans_reference = [], [], []
    prec = clotures_precedentes or {}
    for s in seances:
        s = dict(s)
        if "close_precedent" not in s:
            cle = normaliser_valeur(s.get("valeur"))
            if cle in prec:
                s["close_precedent"] = prec[cle]
        verdict, motif = controler_une_seance(s)
        if verdict == "BLOQUANT":
            return "BLOQUANT", [], alertes, motif
        if verdict == "ALERTE":
            alertes.append(motif)
        if verdict == "SANS_REFERENCE":
            sans_reference.append(motif)
        ecrivables.append(s)

    # LE TEST QUI N'A PAS TOURNÉ SE DIT. Un contrôle muet passe pour un contrôle
    # réussi, et c'est ce qui rend les pertes silencieuses invisibles.
    if sans_reference:
        alertes.append(f"TEST DE VARIATION NON EFFECTUÉ sur {len(sans_reference)} "
                       f"séance(s) — aucune clôture précédente fournie")
    return ("ALERTE" if alertes else "OK"), ecrivables, alertes, ""


def normaliser_valeur(v):
    """    DÉFAUT ③, trouvé par Cowork le 06-09-2026.
    `BUREAU_VERITAS`, `BUREAU VERITAS` et `Bureau Veritas` s'écrivaient comme
    TROIS valeurs distinctes : 3 lignes, 0 doublon détecté. C'est exactement le
    défaut du 23-08 qui a fait perdre 26 % d'une mesure EN SILENCE, réintroduit
    dans le programme qui écrit les cours.

    ① RÔLE — Donner à une entreprise UN seul nom, quel que soit le chemin par
      lequel elle est arrivée. C'est ce qui permet de dire que deux lignes
      parlent de la même société — donc de voir un doublon, et de retrouver la
      clôture de la veille. Sans ce rapprochement, la même entreprise existe en
      plusieurs exemplaires et ses cours se répartissent entre eux.
    ② CONTEXTE D'APPEL — Trois appelants, dont deux hors de ce fichier.
      ① `controler`, une fois par séance, pour retrouver sa clôture précédente.
      ② `_cle`, à chaque fois qu'une séance est comparée à ce qui est déjà au
      fichier. ③ programmes/COLLECTER_ABC_GITHUB.py, qui l'appelle sous le nom
      `C.normaliser_valeur` à trois endroits — en relisant le fichier des cours,
      en cherchant la dernière séance d'une valeur, et surtout juste avant
      d'écrire, pour que le nom écrit soit le nom normalisé.
      programmes/COLLECTER_LES_COURS_ABC.py l'appelle de même, mais aucune tâche
      planifiée ne le lance.
    ③ ENTRÉE — `v` : le nom d'une entreprise, tel qu'il vient de sa source. Ce
      peut être un texte, ou rien du tout. Les appelants passent ce qu'ils ont lu
      sans le modifier, par exemple `BUREAU VERITAS` venu du référentiel des
      valeurs, ou `BUREAU_VERITAS` venu d'une ligne du fichier des cours.
    ④ CONDITIONS D'ENTRÉE — Aucune. Rien du tout, un texte vide ou un nombre ne
      la font pas tomber.
    ⑤ SORTIE — UNE valeur : le nom ramené à sa forme unique — majuscules, et un
      tiret bas partout où il y avait un espace ou un tiret. Mesuré le
      19-09-2026 : `BUREAU_VERITAS`, `BUREAU VERITAS` et `Bureau Veritas` rendent
      tous les trois `BUREAU_VERITAS` ; `UNIBAIL-RODAMCO-WESTFIELD` rend
      `UNIBAIL_RODAMCO_WESTFIELD` ; rien du tout rend un texte vide.
      [rend: 1]
    ⑥ TRAITEMENT — ① prendre le texte, ou un texte vide si la valeur est absente ·
      ② retirer les blancs de début et de fin · ③ passer en majuscules ·
      ④ remplacer chaque espace par un tiret bas · ⑤ remplacer chaque tiret par
      un tiret bas.
    ⑦ UNITÉ — — Un nom n'est pas une grandeur.
    ⑧ POURQUOI — Une même entreprise est écrite différemment selon le fichier :
      `BUREAU VERITAS` dans le référentiel des valeurs, `BUREAU_VERITAS` dans le
      fichier des cours. Sans rapprochement, un programme croit qu'il s'agit de
      deux sociétés distinctes et n'en compte qu'une. Le 23-08-2026, cela a fait
      disparaître 26 % des lignes d'une mesure — sans aucune erreur affichée. Le
      même défaut a été réintroduit le 06-09-2026 dans le programme qui écrit les
      cours, où trois orthographes d'une même société donnaient trois lignes et
      aucun doublon détecté.
      Le tiret est ramené au tiret bas comme l'espace parce que les noms à
      plusieurs mots du CAC 40 sont écrits des deux façons selon la source :
      `UNIBAIL-RODAMCO-WESTFIELD` et `UNIBAIL_RODAMCO` désignent la même société.
    ⑨ CE QUI CLOCHE —
      ① Les accents ne sont pas retirés. `SOCIÉTÉ GÉNÉRALE` et `SOCIETE GENERALE`
      restent deux noms différents après passage ici, alors que le reste du
      traitement s'acharne à réunir des graphies. Le défaut qu'elle corrige peut
      donc revenir par une autre porte.
      ② Rien du tout et un texte vide rendent tous deux un texte vide, qui est un
      nom valide pour la suite du programme. Mesuré le 19-09-2026 : l'absence de
      valeur rend un texte vide. Deux séances sans nom se retrouvent alors sous la
      même clé, et la seconde est prise pour le doublon de la première. Une valeur attendue qui
      ne renvoie rien devrait être une alerte, jamais un silence.
      ③ Elle ne connaît pas les mnémoniques. Le projet pose que la clé d'identité
      d'une valeur est son mnémonique — `AI`, `BN`, `MT` — et jamais son nom ;
      cette fonction rapproche des noms, ce qui est un second système d'identité
      à côté du premier.
      ④ Le texte d'origine de cette fonction parle d'un « DÉFAUT ③ » qui renvoie à
      une liste numérotée disparue : rien dans ce fichier ne dit ce qu'étaient les
      défauts ① et ②.
    ⑩ EFFET — Aucun. Elle ne lit aucun fichier, n'en écrit aucun, n'affiche rien
      et ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels
      ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
  une séance : une journée de bourse pour une valeur, avec son ouverture, son
    plus haut, son plus bas, sa clôture et son volume.
  le fichier des cours : le fichier où les séances s'empilent sans jamais être
    réécrites ; au dépôt, c'est donnees/claude_cours_nouveaux.csv.
  le référentiel des valeurs : donnees/REFERENTIEL_VALEURS_*.csv, la liste des
    valeurs à suivre, avec pour chacune son mnémonique et sa place de cotation.
      la tâche planifiée : un fichier de .github/workflows/ qui fait tourner un
        programme à heure fixe sur une machine GitHub, sans clic ni autorisation.
    
    
  Cowork : le relecteur du projet, qui clone le dépôt, casse le code et rend ses cassures par écrit
  le projet : le dossier reçu sur la ligne de commande, celui que le radar examine
"""
    return str(v or "").strip().upper().replace(" ", "_").replace("-", "_")


def normaliser_date(d):
    """    DÉFAUT ③, même origine. Le tri comparait du TEXTE : `2026-9-4` passait pour
    différent de `2026-09-04`, et `04/09/2026` tombait sous DATE_PLANCHER — jeté
    EN SILENCE. Rend toujours AAAA-MM-JJ, ou None si la date est illisible.

    ① RÔLE — Donner à une journée UNE seule écriture, pour que deux dates puissent
      être comparées en les lisant comme du texte. Toutes les comparaisons de date
      du module en dépendent : reconnaître un doublon, écarter une séance trop
      ancienne, savoir où une valeur s'était arrêtée. Et refuser, plutôt que de
      deviner, quand l'écriture reçue est ambiguë.
    ② CONTEXTE D'APPEL — Trois appelants, dont un hors de ce fichier. ① `_cle`, à
      chaque comparaison d'une séance avec ce qui est déjà au fichier.
      ② `ajouter_au_fichier`, une fois par séance, avant de décider de l'écrire.
      ③ programmes/COLLECTER_ABC_GITHUB.py, sous le nom `C.normaliser_date`, en
      relisant le fichier des cours pour savoir où chaque valeur s'était arrêtée.
      Elle est aussi appelée trois fois directement par `_epreuves`, sur des
      écritures choisies pour la mettre en défaut.
    ③ ENTRÉE — `d` : la date d'une journée de bourse, telle qu'elle vient de sa
      source. Ce peut être un texte, une date déjà construite, ou rien du tout.
      Les appelants passent ce qu'ils ont lu sans le modifier, par exemple
      `2026-09-04` venu d'une ligne du fichier des cours, ou `25/09/2026` venu
      d'une page web.
    ④ CONDITIONS D'ENTRÉE — Aucune. Rien du tout, un texte vide ou un texte sans
      séparateur ne la font pas tomber : elle rend « rien ».
    ⑤ SORTIE — UNE valeur : la date au format AAAA-MM-JJ, ou « rien » quand
      l'écriture est illisible ou ambiguë. Mesuré le 19-09-2026 : `2026-09-04` et
      `2026-9-4` rendent tous deux `2026-09-04` · `2026/09/04` rend `2026-09-04` ·
      `25/09/2026` rend `2026-09-25` · `09/04/2026`, `04.09.2026`, `20260904`,
      `2026-13-01` et le texte vide rendent tous « rien ».
      [rend: 1]
    ⑥ TRAITEMENT — ① prendre le texte et retirer ses blancs · ② rendre « rien »
      s'il est vide · ③ chercher le premier séparateur présent parmi le tiret, la
      barre oblique et le point · ④ découper en trois morceaux, et rendre « rien »
      s'il n'y en a pas exactement trois · ⑤ si le premier morceau fait quatre
      caractères, lire année, mois, jour · ⑥ sinon lire jour, mois, année, et
      rendre « rien » si les deux premiers nombres sont tous deux inférieurs ou
      égaux à 12 et différents · ⑦ rendre « rien » si le mois, le jour ou l'année
      sortent de leurs bornes · ⑧ réécrire au format AAAA-MM-JJ.
    ⑦ UNITÉ — Une DATE de calendrier, écrite année, mois, jour, sans heure ni
      fuseau. L'année est bornée entre 1900 et 2200.
    ⑧ POURQUOI — Le refus de l'ambiguïté est le choix central. Quand le jour est
      inférieur ou égal à 12, `09/04/2026` peut vouloir dire le 9 avril ou le
      4 septembre, et rien dans l'écriture ne permet de trancher. Deviner reviendrait
      à créer une séance à la mauvaise date, ce qui ne s'affiche jamais : la ligne
      existe, elle a des chiffres plausibles, elle est simplement rangée le mauvais
      jour. La fonction refuse donc, et n'accepte le jour en premier que lorsqu'il
      dépasse 12 — `25/09/2026` est lu sans hésitation possible.
      La comparaison de textes, plutôt qu'une comparaison de vraies dates, est
      rendue sûre par le format AAAA-MM-JJ : écrites ainsi, deux dates se classent
      dans l'ordre du calendrier quand on les compare lettre à lettre. C'est ce qui
      permet au plancher des séances acceptées d'être un simple texte.
    ⑨ CE QUI CLOCHE —
      ① Une date absurde est acceptée si elle est bien formée. Les bornes ne
      regardent que les nombres pris séparément : le jour entre 1 et 31, le mois
      entre 1 et 12, l'année entre 1900 et 2200. Le 31 février, qui n'existe pas,
      passe et rend `2026-02-31`, et la journée entre au fichier des cours sous une
      date qui n'a jamais existé.
      ② Le refus de l'ambiguïté fait perdre des journées réelles, en silence. Une
      source qui écrit `04.09.2026` pour le 4 septembre voit sa séance rendre
      « rien ». Mesuré le 19-09-2026 : `04.09.2026` rend « rien ». Un doublon non
      reconnu s'écrit alors deux fois, ou une séance vraie est refusée à
      l'écriture ; dans les deux cas rien ne dit laquelle des deux lectures était
      la bonne.
      ③ Le texte d'origine de cette fonction parle d'un « DÉFAUT ③ » qui renvoie à
      une liste numérotée disparue : rien dans ce fichier ne dit ce qu'étaient les
      défauts ① et ②.
      ④ Le séparateur est cherché dans un ordre fixe — tiret, puis barre oblique,
      puis point. Une écriture qui mêlerait deux séparateurs, comme `2026-09/04`,
      serait découpée sur le premier trouvé et rendrait « rien » sans que le motif
      soit dit.
    ⑩ EFFET — Aucun. Elle ne lit aucun fichier, n'en écrit aucun, n'affiche rien
      et ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas : l'échec de conversion
      d'un morceau en nombre est rattrapé et rendu sous forme de « rien ». Aucun de
      ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
  une séance : une journée de bourse pour une valeur, avec son ouverture, son
    plus haut, son plus bas, sa clôture et son volume.
  le fichier des cours : le fichier où les séances s'empilent sans jamais être
    réécrites ; au dépôt, c'est donnees/claude_cours_nouveaux.csv.
  le jeu d'épreuves : les cas de contrôle que le programme lance sur lui-même,
    avec l'argument `epreuves`
    
    """
    s = str(d or "").strip()
    if not s:
        return None
    for sep in ("-", "/", "."):
        if sep in s:
            p = [x for x in s.split(sep) if x]
            if len(p) != 3:
                return None
            try:
                if len(p[0]) == 4:                      # AAAA-M-J
                    a, m, j = int(p[0]), int(p[1]), int(p[2])
                else:                                   # J/M/AAAA
                    j, m, a = int(p[0]), int(p[1]), int(p[2])
                    # TOUR 6, COWORK : « 09/04/2026 » rendait le 9 AVRIL, en silence.
                    # Quand le jour est ≤ 12, J/M et M/J sont indistinguables. Une
                    # séance existerait alors À LA MAUVAISE DATE — famille des pertes
                    # silencieuses. On refuse l'ambiguïté : seul l'ISO est accepté
                    # dès que les deux premiers nombres sont tous deux ≤ 12.
                    if j <= 12 and m <= 12 and j != m:
                        return None
            except ValueError:
                return None
            if not (1 <= m <= 12 and 1 <= j <= 31 and 1900 <= a <= 2200):
                return None
            return f"{a:04d}-{m:02d}-{j:02d}"
    return None


def _cle(s):
    """Rend le couple qui identifie une séance : la valeur et la date, normalisées.

    ① RÔLE — Donner à une journée de bourse une identité unique, pour que deux
      écritures de la même journée se reconnaissent. C'est ce couple, et lui seul,
      qui permet de dire qu'une séance est déjà au fichier des cours : sans lui,
      la même journée s'écrirait autant de fois qu'elle est proposée, et le
      fichier, qui ne se réécrit jamais, garderait tous les exemplaires.
    ② CONTEXTE D'APPEL — `ajouter_au_fichier`, et elle seule, à trois endroits :
      une fois par ligne déjà présente dans le fichier, puis deux fois par séance
      proposée — pour demander si elle est déjà là, puis pour l'inscrire parmi les
      présentes. Aucun autre appelant : relevé le 19-09-2026, aucun autre fichier
      de programmes/ ni de .github/workflows/ ne nomme `_cle` au sens de cette
      fonction.
    ③ ENTRÉE — `s` : un dictionnaire portant au moins les clés `valeur` et `date`.
      Ce peut être une séance proposée à l'écriture, ou une ligne relue du fichier
      des cours — les deux ont la même forme, et c'est ce qui permet de les
      comparer. Un seul appelant, `ajouter_au_fichier`, qui passe l'un ou l'autre
      sans le modifier.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un dictionnaire vide ne la fait pas tomber :
      les deux clés absentes valent « rien », et les deux fonctions de
      normalisation acceptent « rien ».
    ⑤ SORTIE — DEUX valeurs, rendues ensemble : le nom de la valeur normalisé, et
      la date au format AAAA-MM-JJ. La date vaut « rien » quand elle est illisible.
      [rend: 2]
    ⑥ TRAITEMENT — ① lire la clé `valeur` et la ramener à sa forme unique · ② lire
      la clé `date` et la ramener au format AAAA-MM-JJ · ③ rendre les deux ensemble.
    ⑦ UNITÉ — — Un nom et une date ne sont pas des grandeurs.
    ⑧ POURQUOI — L'identité passe par les deux formes normalisées et jamais par le
      texte brut, parce que c'est exactement ce qui manquait quand le défaut est
      apparu. Le 06-09-2026, `BUREAU_VERITAS`, `BUREAU VERITAS` et `Bureau Veritas`
      donnaient trois lignes et aucun doublon détecté ; et `2026-9-4` passait pour
      différent de `2026-09-04`. Comparer les formes normalisées, et non les textes
      d'origine, est ce qui rend les trois premières égales et les deux secondes
      identiques.
    ⑨ CE QUI CLOCHE —
      ① Deux dates illisibles DIFFÉRENTES donnent la même identité. Mesuré le
      19-09-2026 : une séance datée `???` et une séance datée `2026` rendent toutes
      deux le même couple, avec « rien » à la place de la date. Deux journées sans
      rapport passeraient donc l'une pour le doublon de l'autre. Cela ne se produit
      pas aujourd'hui, parce que `ajouter_au_fichier` refuse tout le lot dès qu'une
      date est illisible — mais la protection vit ailleurs, et rien ici ne le dit.
      ② Elle ne porte aucun texte explicatif d'origine, alors qu'elle décide de
      l'identité d'une journée de bourse. C'est la seule fonction du fichier dans
      ce cas avec `_maintenant`.
    ⑩ EFFET — Aucun. Elle ne lit aucun fichier, n'en écrit aucun, n'affiche rien
      et ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels ne
      se termine : `normaliser_valeur` et `normaliser_date` rendent toutes deux la
      main.
      [sort: non]
    ⑫ DÉFINITIONS
  une séance : une journée de bourse pour une valeur, avec son ouverture, son
    plus haut, son plus bas, sa clôture et son volume.
  le fichier des cours : le fichier où les séances s'empilent sans jamais être
    réécrites ; au dépôt, c'est donnees/claude_cours_nouveaux.csv.
    
    """
    return (normaliser_valeur(s.get("valeur")), normaliser_date(s.get("date")))


def ajouter_au_fichier(seances, chemin):
    """    Ajoute les séances au fichier des cours. N'ÉCRASE JAMAIS.

    Clé anti-doublon : valeur + date. Une séance déjà présente est ignorée en
    silence. Les séances antérieures au 10-07-2026 ne s'ajoutent pas.

    Rend (ajoutees, ignorees_doublon, ignorees_trop_vieilles).

    ① RÔLE — Être le seul endroit du système qui écrit dans le fichier des cours,
      et garantir qu'il ne fait que grandir. Tout ce que la collecte rapporte
      passe par ici. C'est aussi ici que vivent les trois refus qui protègent le
      fichier : pas de doublon, pas de séance trop ancienne, pas de ligne
      incomplète ni de date illisible.
    ② CONTEXTE D'APPEL — Les deux programmes de collecte, une fois par passage,
      juste après le contrôle de vraisemblance et seulement si celui-ci a laissé
      des séances écrivables. programmes/COLLECTER_ABC_GITHUB.py, lancé chaque
      soir par la tâche planifiée .github/workflows/collecte_abc.yml, écrit
      `ecrites, _, _ = C.ajouter_au_fichier(bonnes, cible)`. Aucun autre
      appelant : relevé le 19-09-2026, aucun autre fichier de programmes/ ne
      l'appelle.
    ③ ENTRÉE — `seances` : la liste des séances à écrire, celles que le contrôle
      de vraisemblance a laissées passer · `chemin` : le fichier où écrire.
      L'appelant du soir passe, pour `chemin`, `donnees/claude_cours_nouveaux.csv`
      construit à partir du dossier de dépôt reçu sur sa ligne de commande.
    ④ CONDITIONS D'ENTRÉE — Le dossier du fichier doit exister et être accessible
      en écriture. Le fichier lui-même peut ne pas exister : il est alors créé
      avec sa ligne de titres. S'il existe, il doit porter une ligne de titres
      valide, car c'est elle qui décide des colonnes écrites.
    ⑤ SORTIE — TROIS valeurs : le nombre de séances ajoutées, le nombre écartées
      parce que déjà présentes, et le nombre écartées parce qu'antérieures au
      plancher du 10-07-2026.
      [rend: 3]
    ⑥ TRAITEMENT — ① relire le fichier s'il existe, pour connaître ses colonnes et
      l'identité de chaque ligne déjà présente · ② pour chaque séance proposée :
      écarter et retenir celles dont la date est illisible, compter celles qui
      sont trop anciennes, compter celles qui sont déjà là, garder les autres ·
      ③ lever si une seule date était illisible, sans rien écrire · ④ rendre trois
      zéros s'il ne reste rien à écrire · ⑤ prendre les colonnes de la première
      séance si le fichier n'existait pas · ⑥ lever si une séance a une colonne
      vide, sans rien écrire · ⑦ ajouter un saut de ligne si le fichier n'en
      finissait pas par un · ⑧ écrire les séances à la suite, en écrivant d'abord
      la ligne de titres si le fichier est neuf · ⑨ relire le fichier et lever si
      le nombre de lignes ne tombe pas juste.
    ⑦ UNITÉ — Un NOMBRE DE SÉANCES pour les trois valeurs rendues. Le plancher est
      une DATE, le 10-07-2026, comparée comme du texte. Le contrôle final compte
      des LIGNES DE FICHIER, titres exclus.
    ⑧ POURQUOI — Quatre protections, chacune née d'une perte mesurée.
      ① Le saut de ligne est vérifié avant d'ajouter. Ouvrir un fichier en ajout
      et écrire sans regarder s'il finit par un saut de ligne SOUDE la nouvelle
      ligne à la dernière : deux journées deviennent une, et le fichier, qui ne se
      réécrit jamais, perd une ligne à chaque écriture. Le 06-09-2026, la relecture
      comptait 1 ligne là où il en fallait 2.
      ② Une ligne incomplète est refusée. Une séance sans volume s'écrivait avec
      un champ vide, et bloquait la collecte au passage SUIVANT — le message
      désignant alors la séance, jamais l'écriture qui l'avait produite. Un défaut
      qui se manifeste un jour après sa cause coûte le temps qu'il faut pour
      remonter d'un jour.
      ③ Le fichier est relu et recompté après écriture. Le recomptage existait
      déjà, et personne ne comparait son résultat à ce qui était attendu. Un
      fichier abîmé doit arrêter la collecte, pas la laisser continuer sur des
      données perdues.
      ④ Le plancher du 10-07-2026 est la date de la dernière séance de
      l'historique figé : gouvernance/PILOTE.md l'annonce au 2026-07-10. Écrire
      une séance antérieure créerait une journée présente dans deux fichiers à la
      fois, sans que rien ne dise laquelle fait foi.
    ⑨ CE QUI CLOCHE —
      ① Un doublon DÉJÀ présent dans le fichier fait échouer une écriture
      parfaitement juste. Le compte attendu est déduit du nombre d'identités
      distinctes, et la relecture compte des lignes : un fichier qui porte deux
      fois la même journée a plus de lignes que d'identités. Mesuré le 19-09-2026
      sur une copie du dépôt, avec un fichier portant deux fois ACCOR au
      2026-09-16 : l'ajout d'une séance neuve rend « ÉCRITURE ABÎMÉE : 3 lignes
      relues, 2 attendues. NE PAS POURSUIVRE ». Et la ligne neuve EST écrite avant
      la levée — le fichier passe de 2 à 3 lignes. La collecte du soir s'arrête
      alors sur un fichier déjà modifié.
      ② La première écriture d'un fichier neuf y met une colonne de trop. Les
      colonnes sont prises sur la première séance, et `controler` y a glissé la
      clôture précédente. Mesuré le 19-09-2026 sur une copie du dépôt, fichier
      absent au départ : la ligne de titres écrite est
      `valeur,date,open,high,low,close,volume,close_precedent`, alors que
      programmes/CONTRATS_DES_FICHIERS.py déclare pour ce fichier les sept
      colonnes `valeur`, `date`, `open`, `high`, `low`, `close` et `volume`. Cela
      ne se voit pas aujourd'hui parce que le fichier existe et impose ses
      colonnes ; le premier soir d'un dépôt neuf, le fichier naîtrait hors contrat.
      ③ Un fichier existant mais VIDE reçoit des données sans ligne de titres.
      Comme il existe, la ligne de titres n'est pas écrite ; comme il est vide,
      les colonnes sont prises sur la séance. Mesuré le 19-09-2026 sur une copie
      du dépôt : après l'appel, le fichier contient la seule ligne
      `ACCOR,2026-09-17,50,51,49,50.5,1000`, sans titres, et la fonction lève
      « ÉCRITURE ABÎMÉE : 0 lignes relues, 1 attendues ». À la lecture suivante,
      cette ligne de données sera prise pour la ligne de titres.
      ④ Les deux refus lèvent une erreur que personne ne rattrape. Mesuré le
      19-09-2026 : une séance datée `09/04/2026` rend « DATES ILLISIBLES, rien
      n'est écrit ». programmes/COLLECTER_ABC_GITHUB.py appelle cette fonction
      sans protection : la collecte du soir s'arrête alors sur une pile d'appel,
      sans rapport écrit, alors qu'elle sait par ailleurs sortir proprement avec
      un code de sortie qui dit ce qui s'est passé.
      ⑤ Les séances déjà présentes et les séances trop anciennes sont comptées,
      mais l'appelant du soir jette ces deux comptes — il écrit
      `ecrites, _, _ = C.ajouter_au_fichier(...)`. Un passage où toutes les
      séances seraient écartées comme trop anciennes ressemble donc exactement à
      un passage où il n'y avait rien à écrire.
      ⑥ Le plancher du 10-07-2026 est écrit dans ce fichier et dans les deux
      programmes de collecte, chacun sous le nom `DATE_PLANCHER`. Un chiffre qui
      existe ailleurs ne se recopie pas (R-708) : corriger l'un des trois sans les
      autres les ferait diverger en silence.
      ⑦ Le contrôle final porte sur un COMPTE de lignes, et non sur une propriété
      du fichier. Il ne dirait rien d'une ligne écrite avec les bonnes colonnes
      mais les mauvaises valeurs, ni d'une ligne dont les colonnes auraient glissé
      d'un cran, tant que le nombre de lignes tombe juste. Réparer par une
      propriété plutôt que par une énumération est le critère du projet (A-408).
    ⑩ EFFET — ÉCRIT dans le fichier qu'on lui nomme, en AJOUT à la fin, jamais en
      réécriture. Le crée avec sa ligne de titres s'il n'existait pas. Peut lui
      ajouter un saut de ligne seul, avant d'écrire, quand il n'en finissait pas
      par un. LE RELIT ensuite en entier pour se compter. N'affiche rien, ne
      touche pas au réseau, ne supprime rien. Ne touche jamais
      donnees/cac40_ohlcv.csv, l'historique figé.
    ⑪ TERMINAISON — Rend la main avec ses trois nombres dans le cas normal. PEUT
      LEVER trois erreurs, non rattrapées ici, qui arrêtent alors le programme
      appelant : sur une date illisible et sur une colonne vide, AVANT toute
      écriture · sur un compte de lignes qui ne tombe pas, APRÈS l'écriture. Les
      trois ont été mesurées le 19-09-2026 sur une copie du dépôt. Aucun de ses
      appels ne se termine : `_cle`, `normaliser_date` et `relire_et_compter`
      rendent toutes la main.
      [sort: non]
    ⑫ DÉFINITIONS
  une séance : une journée de bourse pour une valeur, avec son ouverture, son
    plus haut, son plus bas, sa clôture et son volume.
  le fichier des cours : le fichier où les séances s'empilent sans jamais être
    réécrites ; au dépôt, c'est donnees/claude_cours_nouveaux.csv.
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
    étant qu'une copie de lecture
  le contrôle de vraisemblance : les tests de programmes/CONTROLER_LES_COURS.py
    qui jugent une séance avant qu'elle soit écrite.
      la tâche planifiée : un fichier de .github/workflows/ qui fait tourner un
        programme à heure fixe sur une machine GitHub, sans clic ni autorisation.
    
    
  l'historique figé : donnees/cac40_ohlcv.csv, le fichier de cours de référence qui n'est jamais réécrit
  un saut : l'ouverture d'une séance au-delà du seuil de sortie, de sorte que la sortie ne se fait pas au prix prévu mais au prix d'ouverture
"""
    presentes = set()
    entete = None
    if os.path.exists(chemin):
        with open(chemin, newline="", encoding="utf-8-sig") as f:
            lecteur = csv.DictReader(f)
            entete = lecteur.fieldnames
            for r in lecteur:
                presentes.add(_cle(r))

    a_ecrire, doublons, vieilles, illisibles = [], 0, 0, []
    for s in seances:
        d = normaliser_date(s.get("date"))
        if d is None:
            # UNE DATE ILLISIBLE NE SE JETTE PLUS EN SILENCE.
            illisibles.append(f"{s.get('valeur','?')} : date « {s.get('date')} »")
            continue
        if d < DATE_PLANCHER:
            vieilles += 1
            continue
        if _cle(s) in presentes:
            doublons += 1
            continue
        presentes.add(_cle(s))
        a_ecrire.append(s)

    if illisibles:
        raise ValueError("DATES ILLISIBLES, rien n'est écrit : " + " · ".join(illisibles))

    if not a_ecrire:
        return 0, doublons, vieilles

    if entete is None:
        entete = list(a_ecrire[0].keys())

    # DÉFAUT ③ : une séance sans volume s'écrivait champ vide, et BLOQUAIT la
    # boucle au tour SUIVANT — le motif désignant la séance, pas l'écriture qui
    # l'avait produite. On refuse d'écrire une ligne incomplète.
    for s in a_ecrire:
        vides = [c for c in entete if str(s.get(c, "")).strip() == ""]
        if vides:
            raise ValueError(f"LIGNE INCOMPLÈTE, rien n'est écrit : "
                             f"{s.get('valeur','?')} {s.get('date','?')} — "
                             f"colonnes vides : {', '.join(vides)}")

    # DÉFAUT ① — LE PLUS GRAVE, trouvé par Cowork le 06-09-2026.
    # Ouvrir en mode "a" et écrire SANS vérifier que le fichier finit par un saut
    # de ligne SOUDE la nouvelle ligne à la dernière : deux séances deviennent une,
    # et le fichier des cours — qui ne se réécrit jamais — perd une ligne à chaque
    # écriture. Reproduit : relire_et_compter rendait 1 au lieu de 2.
    nouveau = not os.path.exists(chemin)
    if not nouveau and os.path.getsize(chemin) > 0:
        with open(chemin, "rb") as f:
            f.seek(-1, os.SEEK_END)
            if f.read(1) not in (b"\n", b"\r"):
                with open(chemin, "a", encoding="utf-8") as g:
                    g.write("\n")

    with open(chemin, "a", newline="", encoding="utf-8") as f:
        ecrivain = csv.DictWriter(f, fieldnames=entete, extrasaction="ignore")
        if nouveau:
            ecrivain.writeheader()
        for s in a_ecrire:
            ecrivain.writerow(s)

    # LE RECOMPTAGE EST UN CONTRÔLE, PAS UNE FONCTION DISPONIBLE.
    # Cowork, 06-09 : « relire_et_compter existe, voit le compte faux, et personne
    # ne compare son résultat à ce qui était attendu. » Corrigé : on compare ici,
    # et on lève si le compte ne tombe pas. Un fichier de cours abîmé doit arrêter
    # la boucle, pas la laisser continuer sur des données perdues.
    avant = len(presentes) - len(a_ecrire)
    apres = relire_et_compter(chemin)
    if apres != avant + len(a_ecrire):
        raise RuntimeError(
            f"ÉCRITURE ABÎMÉE dans {chemin} : {apres} lignes relues, "
            f"{avant + len(a_ecrire)} attendues. NE PAS POURSUIVRE.")

    return len(a_ecrire), doublons, vieilles


def relire_et_compter(chemin):
    """    Relit le fichier après écriture et compte ses lignes.
    Sert de contrôle : ce qu'on croit avoir écrit doit s'y retrouver.

    ① RÔLE — Aller voir dans le fichier ce qui s'y trouve vraiment, au lieu de
      faire confiance à ce que l'écriture vient d'annoncer. C'est la seule mesure
      du module qui ne repose pas sur ce que le programme croit avoir fait : elle
      rouvre le fichier et recompte. Ce qui se mesure ne s'écrit pas à la main
      (R-728).
    ② CONTEXTE D'APPEL — `ajouter_au_fichier`, une seule fois, juste après
      l'écriture et avant de rendre ses comptes. Aucun autre appelant : relevé le
      19-09-2026, aucun autre fichier de programmes/ ni de .github/workflows/ ne
      nomme `relire_et_compter`.
    ③ ENTRÉE — `chemin` : le fichier à recompter. Un seul appelant,
      `ajouter_au_fichier`, qui transmet sans le modifier le chemin qu'il a
      lui-même reçu, par exemple `donnees/claude_cours_nouveaux.csv`.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un fichier absent ne la fait pas tomber : elle
      rend zéro.
    ⑤ SORTIE — UNE valeur : le nombre de lignes de données du fichier, sa ligne de
      titres exclue. Mesuré le 19-09-2026 sur une copie du dépôt : un fichier
      absent rend 0.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre zéro si le fichier n'existe pas · ② l'ouvrir en
      retirant la marque d'ordre des octets que certains éditeurs posent en tête ·
      ③ le parcourir ligne à ligne en traitant la première comme la ligne de
      titres · ④ rendre le nombre de lignes parcourues.
    ⑦ UNITÉ — Un NOMBRE DE LIGNES DE DONNÉES, titres exclus. Ce n'est PAS un
      nombre de séances distinctes : deux lignes portant la même journée comptent
      pour deux.
    ⑧ POURQUOI — Elle rouvre le fichier au lieu de se fier à ce qui vient d'être
      écrit, parce que l'écriture peut réussir en apparence et abîmer le fichier :
      une ligne soudée à la précédente fait disparaître une journée sans qu'aucune
      erreur ne s'affiche. Le 06-09-2026, cette fonction existait, voyait le compte
      faux, et personne ne comparait son résultat à ce qui était attendu. La
      comparaison a été ajoutée chez son appelant, et c'est ce qui l'a rendue utile.
    ⑨ CE QUI CLOCHE —
      ① Elle compte des lignes, quand son appelant attend un nombre d'identités
      distinctes. Un fichier portant deux fois la même journée a plus de lignes
      que d'identités, et son appelant conclut à une écriture abîmée. Mesuré le
      19-09-2026 sur une copie du dépôt, avec un fichier portant deux fois ACCOR
      au 2026-09-16 : l'ajout d'une séance neuve rend « ÉCRITURE ABÎMÉE : 3 lignes
      relues, 2 attendues ». Le fichier était en effet fautif, mais le message
      accuse l'écriture qui vient d'avoir lieu.
      ② Un fichier absent et un fichier vide rendent tous deux zéro. Les deux
      situations n'ont pourtant pas la même conséquence : sur un fichier absent,
      l'écriture crée le fichier avec sa ligne de titres ; sur un fichier vide,
      elle écrit des données sans titres.
      ③ Elle ne regarde ni les colonnes, ni les valeurs. Un fichier dont toutes les
      colonnes auraient glissé d'un cran rend le bon nombre de lignes et laisse
      passer. Réparer par une propriété plutôt que par une énumération est le
      critère du projet (A-408) ; ici, le compte ne dit rien de ce qui est écrit.
      ④ Son nom parle de relecture « après écriture », mais rien ne l'empêche d'être
      appelée à tout moment : c'est une simple mesure, et son texte d'origine en
      fait un contrôle.
    ⑩ EFFET — LIT le fichier en entier. N'écrit rien, n'affiche rien, ne touche pas
      au réseau.
    ⑪ TERMINAISON — Rend toujours la main dans les cas rencontrés. Elle PEUT LEVER,
      sans que ce soit rattrapé, si le fichier existe mais ne se lit pas — droits
      refusés, ou octets qui ne sont pas de l'UTF-8. Aucun de ses appels ne se
      termine.
      [sort: non]
    ⑫ DÉFINITIONS
  une séance : une journée de bourse pour une valeur, avec son ouverture, son
    plus haut, son plus bas, sa clôture et son volume.
  le fichier des cours : le fichier où les séances s'empilent sans jamais être
    réécrites ; au dépôt, c'est donnees/claude_cours_nouveaux.csv.
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
    étant qu'une copie de lecture
    
    
  la marque d'ordre des octets : trois octets invisibles que certains tableurs posent en tête d'un fichier et qui, s'ils ne sont pas écartés, se collent au nom de la première colonne
"""
    if not os.path.exists(chemin):
        return 0
    with open(chemin, newline="", encoding="utf-8-sig") as f:
        return sum(1 for _ in csv.DictReader(f))


TEMOIN_COURS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "temoins", "TEMOIN_cours_reels.csv")
TEMOIN_COURS_TAILLE = 20774
TEMOIN_COURS_EMPREINTE = "ae87b3c76c74428fdf2c45cf7ea54c88393370ab69dcfad0975084a523bc1b1c"


def _cas_venus_du_vrai_fichier(chemin=None):
    """    Prend de VRAIES lignes du fichier des cours et en fait des cas d'épreuve —
    une telle quelle, quatre sabotées. Si le fichier n'est pas là, rend une liste
    vide ET LE DIT : un contrôle qui ne tourne pas ne doit jamais passer pour un
    contrôle réussi.

    ① RÔLE — Confronter le contrôle des séances à ce que la VRAIE donnée contient,
      et non à ce que le programmeur suppose qu'elle contient. Les tests écrits à
      la main éprouvent ce à quoi leur auteur a pensé ; une vraie ligne porte les
      formes, les arrondis et les manques que personne n'a prévus. Un jeu
      d'épreuves contient au moins un exemple venu d'une vraie ligne du fichier
      (R-732).
    ② CONTEXTE D'APPEL — `_epreuves`, une seule fois, après les neuf tests écrits à
      la main et avant les trois vérifications de date. Aucun autre appelant :
      relevé le 19-09-2026, aucun autre fichier de programmes/ ni de
      .github/workflows/ ne nomme `_cas_venus_du_vrai_fichier`.
    ③ ENTRÉE — `chemin` : le fichier de cours dans lequel puiser la ligne réelle.
      Il vaut « rien » par défaut, et le témoin figé du dépôt est alors employé.
      Son seul appelant, `_epreuves`, ne lui passe aucun argument : c'est donc
      toujours temoins/TEMOIN_cours_reels.csv qui est lu.
    ④ CONDITIONS D'ENTRÉE — Le témoin doit être présent ET inchangé, à l'octet
      près : 20 774 octets, et l'empreinte SHA-256 écrite dans ce fichier sous le
      nom `TEMOIN_COURS_EMPREINTE`. Le fichier lu doit porter les colonnes d'une
      séance, `high`, `low` et `close` devant être des nombres lisibles.
    ⑤ SORTIE — UNE valeur : la liste des tests fabriqués. SIX tests quand le
      fichier porte des lignes — un mesuré le 19-09-2026 sur une copie du dépôt :
      la ligne réelle employée est AIRBUS au 2026-08-07. Une liste VIDE quand le
      fichier n'a que sa ligne de titres.
      [rend: 1]
    ⑥ TRAITEMENT — ① vérifier que le témoin est bien celui qu'on croit · ② prendre
      le témoin si aucun chemin n'a été donné · ③ lever si le fichier est
      introuvable · ④ le lire en entier · ⑤ rendre une liste vide s'il ne porte
      aucune ligne · ⑥ prendre la ligne du MILIEU · ⑦ en fabriquer six tests : la
      ligne telle quelle, la même avec sa clôture précédente, puis quatre copies
      abîmées — plus haut et plus bas échangés, volume mis à zéro, clôture portée
      hors de ses bornes, clôture précédente choisie pour donner une variation de
      40 %.
    ⑦ UNITÉ — Un NOMBRE DE TESTS pour la liste rendue. Les prix de la ligne réelle
      sont en euros et son volume en titres. La variation fabriquée est un
      POURCENTAGE, ici 40 %, choisi au-dessus du seuil de 25 % pour que l'alerte se
      déclenche.
    ⑧ POURQUOI — La ligne du milieu est prise plutôt que la première ou la
      dernière, parce que les bords d'un fichier sont les endroits les plus
      susceptibles d'être particuliers : la première ligne suit immédiatement les
      titres, la dernière peut être incomplète si l'écriture a été interrompue.
      Le milieu est une ligne ordinaire.
      Chaque copie abîmée sabote UNE propriété et une seule, et chacune vise un des
      quatre tests : le plus haut sous le plus bas, le volume nul, la clôture hors
      bornes, la variation au-delà du seuil. Un test qui reste vert quand on retire
      ce qu'il surveille n'est pas une preuve.
      Et la clôture précédente est fabriquée en divisant la clôture réelle par 1,4 :
      c'est une variation de 40 % quelle que soit la valeur tirée du fichier, donc
      un test qui ne dépend pas de la ligne sur laquelle il tombe.
    ⑨ CE QUI CLOCHE —
      ① Son texte d'origine annonce « une telle quelle, quatre sabotées », soit
      cinq tests ; elle en rend six. Mesuré le 19-09-2026 : la liste contient six
      éléments. Un sixième a été ajouté — la ligne réelle accompagnée de sa propre
      clôture, qui doit rendre « OK » — sans que ces lignes soient reprises.
      ② Son texte d'origine annonce qu'elle « rend une liste vide ET LE DIT » quand
      le fichier n'est pas là. Elle ne rend rien du tout : elle LÈVE. C'est le
      comportement voulu depuis que rendre zéro a été reconnu comme un silence, et
      le texte décrit l'ancien.
      ③ Le témoin est figé sur 390 séances de 10 valeurs seulement, du 2026-07-13
      au 2026-09-03 — mesuré le 19-09-2026. Il ne porte donc pas les quarante
      valeurs du référentiel, et une orthographe de nom ou un format de volume propre à
      l'une des trente autres ne serait jamais éprouvé.
      ④ La taille et l'empreinte du témoin sont écrites dans ce fichier, et le
      témoin vit dans temoins/. Remplacer le témoin sans corriger les deux nombres
      fait rendre le code 2 — ce qui est voulu — mais rien ne dit, au moment de le
      remplacer, qu'il faut aussi toucher le code.
      ⑤ La ligne du milieu change dès qu'une ligne est ajoutée au témoin : le test
      ne porte pas sur une journée choisie mais sur celle qui se trouve là. Deux
      versions du témoin éprouvent donc deux journées différentes, sans que la
      sortie le dise.
    ⑩ EFFET — LIT deux fois le témoin : une fois en entier pour vérifier son
      empreinte, une fois pour en extraire les lignes. N'écrit aucun fichier,
      n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main avec sa liste dans le cas normal. LÈVE quand le
      témoin est absent, et son appelant ne la rattrape pas : c'est le lancement du
      programme qui l'attrape et s'arrête avec le code 2 — mesuré le
      19-09-2026 sur une copie du dépôt. Un de ses appels peut ne pas revenir en
      rendant une valeur : `_verrouiller_temoin` lève quand le témoin a changé, et
      cette levée traverse cette fonction sans être rattrapée.
      [sort: non]
    ⑫ DÉFINITIONS
  une séance : une journée de bourse pour une valeur, avec son ouverture, son
    plus haut, son plus bas, sa clôture et son volume.
  le fichier des cours : le fichier où les séances s'empilent sans jamais être
    réécrites ; au dépôt, c'est donnees/claude_cours_nouveaux.csv.
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
    étant qu'une copie de lecture
  le jeu d'épreuves : les cas de contrôle que le programme lance sur lui-même,
    avec l'argument `epreuves`
  l'empreinte : le nombre SHA-256 calculé sur le contenu d'un fichier ; deux
    fichiers de même empreinte ont le même contenu
      le témoin : le fichier temoins/TEMOIN_cours_reels.csv, copie figée de vraies
        séances, sur laquelle les épreuves tournent toujours à l'identique.
      le référentiel : donnees/REFERENTIEL_VALEURS_*.csv, la liste des valeurs à
        suivre, avec pour chacune son mnémonique et sa place de cotation.
    
    """
    import csv as _csv
    # TÉMOIN FIGÉ AU DÉPÔT (tour 5, Cowork) : /mnt/project n'existe que sur la machine
    # du Chat. Dans tout clone neuf — donc dans la routine — le fichier réel était
    # absent et les épreuves rendaient 2 sur un code SAIN : un rouge permanent.
    # Le vrai fichier des cours est copié une fois sous temoins/, et l'épreuve le lit.
    _verrouiller_temoin(TEMOIN_COURS, TEMOIN_COURS_TAILLE, TEMOIN_COURS_EMPREINTE)
    chemin = chemin or TEMOIN_COURS
    if not os.path.exists(chemin):
        # R-734 POUSSÉE JUSQU'À SA CONSÉQUENCE, trouvée par Cowork le 06-09-2026 :
        # ce bloc DISAIT l'incomplétude et rendait quand même 0. Un humain voyait
        # l'avertissement ; une machine qui lit le code de sortie voyait « tout va
        # bien ». Et c'est la machine qui décide, puisque c'est tout l'objet d'un
        # garde-fou. UN CONTRÔLE QUI NE TOURNE PAS EST UN CONTRÔLE QUI ÉCHOUE.
        raise FileNotFoundError(
            f"ÉPREUVES INCOMPLÈTES : le fichier réel {chemin} est introuvable. "
            f"Les cas venus de la vraie donnée n'ont PAS tourné (R-732).")
    with open(chemin, newline="", encoding="utf-8-sig") as f:
        lignes = list(_csv.DictReader(f))
    if not lignes:
        return []
    v = dict(lignes[len(lignes) // 2])
    return [
        (dict(v), "SANS_REFERENCE", f"VRAIE ligne du fichier : {v.get('valeur')} {v.get('date')}"),
        ({**v, "close_precedent": v["close"]}, "OK", "VRAIE ligne AVEC sa clôture précédente"),
        ({**v, "high": v["low"], "low": v["high"]}, "BLOQUANT", "VRAIE ligne, High et Low inversés"),
        ({**v, "volume": "0"}, "BLOQUANT", "VRAIE ligne, volume mis à zéro"),
        ({**v, "close": str(float(v["high"]) + 10)}, "BLOQUANT", "VRAIE ligne, Close hors bornes"),
        ({**v, "close_precedent": str(float(v["close"]) / 1.4)}, "ALERTE", "VRAIE ligne, variation +40 %"),
    ]


def _verrouiller_temoin(chemin, taille, empreinte):
    """    TOUR 6, COWORK : les témoins étaient épinglés dans A_RELIRE.md, jamais dans le
    code. Résultat mesuré : 20 774 octets de vrais cours remplacés par 113 octets
    inventés, verdict identique, code 0. Et un rapport REGÉNÉRÉ par le programme
    lui-même — la circularité tuée au tour 4 — passait 17/17.

    Le verrou voyage désormais AVEC le code : il marche depuis un clone, une tâche,
    ou un garde-fou automatique, qui ne lisent qu'un code de sortie. Remplacer un
    témoin devient un geste à DEUX endroits — donc visible.

    Rend 2 si le témoin ne correspond pas : c'est « n'a pas pu tourner », jamais
    « a tourné et échoue ».

    ① RÔLE — Garantir que les tests tournent bien sur la donnée de référence qu'ils
      croient employer, et pas sur autre chose. Sans ce verrou, un jeu d'épreuves
      peut afficher « tout passe » alors qu'il s'est exécuté sur un fichier
      inventé : le verdict est le même, et rien dans la sortie ne permet de faire
      la différence.
    ② CONTEXTE D'APPEL — `_cas_venus_du_vrai_fichier`, une seule fois, en tout
      premier, avant même de choisir le fichier à lire. Aucun autre appelant :
      relevé le 19-09-2026, aucun autre fichier de programmes/ ni de
      .github/workflows/ ne nomme `_verrouiller_temoin`.
    ③ ENTRÉE — `chemin` : le fichier de référence à vérifier · `taille` : le nombre
      d'octets qu'il doit faire · `empreinte` : l'empreinte SHA-256 qu'il doit
      avoir. Un seul appelant, `_cas_venus_du_vrai_fichier`, qui passe toujours les
      trois valeurs écrites dans ce fichier sous les noms TEMOIN_COURS,
      TEMOIN_COURS_TAILLE et TEMOIN_COURS_EMPREINTE — soit
      temoins/TEMOIN_cours_reels.csv, 20 774 octets, et l'empreinte commençant par
      ae87b3c7. Relevé le 19-09-2026 sur le dépôt : le fichier fait bien 20 774
      octets et porte bien cette empreinte.
    ④ CONDITIONS D'ENTRÉE — Les trois valeurs doivent se rapporter au même fichier.
      Rien ne le vérifie : ce sont trois valeurs indépendantes, et c'est à celui qui
      appelle de les tenir ensemble.
    ⑤ SORTIE — Ne rend rien. Elle parle uniquement en levant : si elle rend la main,
      c'est que le fichier est le bon.
      [rend: rien]
    ⑥ TRAITEMENT — ① lever si le fichier n'existe pas · ② le lire en entier, en
      octets · ③ lever si sa taille ou son empreinte SHA-256 ne sont pas celles
      attendues, en disant les deux mesurées et les deux attendues.
    ⑦ UNITÉ — Des OCTETS pour la taille. L'empreinte est un nombre hexadécimal de
      64 caractères, dont les huit premiers seulement sont affichés dans le message
      d'erreur.
    ⑧ POURQUOI — Les deux nombres vivent DANS le code, et non dans un document à
      côté, parce que c'est le code qui voyage. Un clone neuf, une tâche planifiée
      ou un contrôle automatique ne lisent qu'un code de sortie : ils n'ouvriront
      jamais le document où le témoin était épinglé. Le 06-09-2026, 20 774 octets
      de vrais cours ont été remplacés par 113 octets inventés — le verdict est
      resté identique, et le code de sortie est resté 0.
      Et la même levée sert pour un fichier absent et pour un fichier changé,
      parce que les deux disent la même chose à celui qui lance : les tests n'ont
      PAS PU tourner. C'est le code 2, et jamais le code 1 qui dirait qu'ils ont
      tourné et échoué.
      Remplacer le témoin devient ainsi un geste à DEUX endroits — le fichier, et
      les deux nombres du code — donc un geste visible.
    ⑨ CE QUI CLOCHE —
      ① Son texte d'origine annonce « Rend 2 si le témoin ne correspond pas ». Elle
      ne rend rien du tout : elle LÈVE, et c'est le lancement du programme, bien
      plus loin, qui transforme cette levée en code 2. Mesuré le 19-09-2026 sur une
      copie du dépôt : un témoin tronqué fait sortir le programme en code 2, avec
      le message « TÉMOIN SUBSTITUÉ : TEMOIN_cours_reels.csv fait 5 o · 7ed9d10b,
      attendu 20774 o · ae87b3c7 ». Le comportement est le bon ; c'est le texte qui
      décrit une autre mécanique.
      ② Elle lève la même erreur pour « absent » et pour « changé », alors que ses
      messages distinguent bien les deux. Un appelant qui voudrait traiter
      différemment un témoin manquant et un témoin substitué ne le pourrait qu'en
      lisant le texte du message.
      ③ L'empreinte est recalculée deux fois quand le témoin ne correspond pas —
      une fois pour comparer, une fois pour l'afficher. Sans conséquence sur un
      fichier de 20 774 octets, mais le calcul est refait au lieu d'être gardé.
      ④ La taille est vérifiée en plus de l'empreinte, alors que l'empreinte suffit :
      deux fichiers de même empreinte ont le même contenu, donc la même taille. Le
      second nombre n'ajoute aucune garantie, et il ajoute un endroit à tenir à jour.
    ⑩ EFFET — LIT le fichier en entier, en octets. N'écrit rien, n'affiche rien, ne
      touche pas au réseau.
    ⑪ TERMINAISON — Rend la main sans valeur quand le fichier est le bon. LÈVE
      sinon, et cette levée n'est rattrapée ni ici ni chez son appelant : elle
      remonte jusqu'au lancement du programme, qui s'arrête avec le code 2.
      Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
    étant qu'une copie de lecture
  le jeu d'épreuves : les cas de contrôle que le programme lance sur lui-même,
    avec l'argument `epreuves`
  l'empreinte : le nombre SHA-256 calculé sur le contenu d'un fichier ; deux
    fichiers de même empreinte ont le même contenu
      un témoin : un jeu de chiffres dont on connaît d'avance le résultat, employé
        pour prouver qu'un instrument fonctionne avant de s'en servir
      le témoin : le fichier temoins/TEMOIN_cours_reels.csv, copie figée de vraies
        séances, sur laquelle les épreuves tournent toujours à l'identique.
      la tâche planifiée : un fichier de .github/workflows/ qui fait tourner un
        programme à heure fixe sur une machine GitHub, sans clic ni autorisation.
    
    
  Cowork : le relecteur du projet, qui clone le dépôt, casse le code et rend ses cassures par écrit
  un garde-fou : une limite qui, franchie, fait cesser a la strategie de prendre position tout en continuant a la mesurer.
"""
    import hashlib as _h
    if not os.path.exists(chemin):
        raise FileNotFoundError(f"TÉMOIN ABSENT : {chemin}")
    contenu = open(chemin, "rb").read()
    if len(contenu) != taille or _h.sha256(contenu).hexdigest() != empreinte:
        raise FileNotFoundError(
            f"TÉMOIN SUBSTITUÉ : {os.path.basename(chemin)} fait {len(contenu)} o · "
            f"{_h.sha256(contenu).hexdigest()[:8]}, attendu {taille} o · {empreinte[:8]}. "
            f"Les épreuves ne tournent PAS sur une référence inconnue.")


def _epreuves():
    """    Jeu d'épreuves. Chaque cas doit tomber juste, et les sabotages doivent
    être dénoncés. Un programme qui passe ses propres témoins réécrits ne
    prouve rien : ces cas sont écrits À LA MAIN, pas dérivés du code.

    ① RÔLE — Prouver que le contrôle des séances dit encore ce qu'il doit dire,
      et le prouver de telle sorte qu'un retrait de garde-fou fasse rougir la
      sortie. C'est le seul garde-fou du module : rien d'autre ne vérifie que les
      quatre tests fonctionnent, et il est lancé à la main, jamais par le circuit
      du soir.
    ② CONTEXTE D'APPEL — Le lancement du programme avec l'argument `epreuves`, et
      lui seul. Son résultat devient directement le code de sortie du processus.
      Aucun appelant automatique : relevé le 19-09-2026, aucun des deux fichiers
      de .github/workflows/ ne nomme ce programme, et aucun autre fichier de
      programmes/ n'appelle cette fonction. Elle tourne donc quand quelqu'un la
      lance, et à ce moment-là seulement.
    ③ ENTRÉE — Aucun paramètre. Elle lit un fichier, et un seul :
      temoins/TEMOIN_cours_reels.csv, par l'intermédiaire de
      `_cas_venus_du_vrai_fichier`.
    ④ CONDITIONS D'ENTRÉE — Le témoin doit être présent et inchangé à l'octet près,
      sans quoi rien ne tourne. Et les vérifications internes du programme doivent
      être actives : lancé avec l'option qui les désactive, les trois
      vérifications de date de cette fonction ne s'exécutent pas, et la sortie ne
      le dit pas.
    ⑤ SORTIE — UNE valeur : vrai si tous les tests sont tombés juste, faux sinon.
      Elle affiche par ailleurs une ligne par test et une ligne de total. Mesuré le
      19-09-2026 sur une copie du dépôt : « 16/16 cas passent », et le programme
      sort en code 0.
      [rend: 1]
    ⑥ TRAITEMENT — ① dresser neuf tests écrits à la main, couvrant les quatre tests
      de vraisemblance et la lecture des nombres à la française · ② y ajouter les
      six tests fabriqués à partir d'une vraie ligne du fichier des cours ·
      ③ vérifier au passage que la date ambiguë est refusée et que la date sans
      ambiguïté est acceptée · ④ ajouter un seizième test, la séance dont la date
      est ambiguë · ⑤ jouer chaque test, comparer le verdict obtenu au verdict
      attendu, et afficher la ligne · ⑥ afficher le total · ⑦ rendre vrai si le
      compte des tests réussis égale le compte des tests.
    ⑦ UNITÉ — Un NOMBRE DE TESTS. Les prix des séances fabriquées sont en euros et
      leurs volumes en titres, mais ce sont des valeurs choisies pour éprouver, pas
      des cours réels — sauf pour les six qui viennent du témoin.
    ⑧ POURQUOI — Les tests écrits à la main et les tests venus de la vraie donnée
      coexistent parce qu'ils n'éprouvent pas la même chose. Ceux écrits à la main
      couvrent chaque test de vraisemblance exactement une fois, y compris des cas
      qu'aucune donnée réelle ne produirait. Ceux venus du fichier portent les
      formes que personne n'avait prévues : neuf défauts du 06-09-2026 étaient
      passés entre des tests entièrement écrits à la main. Un jeu d'épreuves
      contient au moins un exemple venu d'une vraie ligne du fichier (R-732).
      Et l'échec de lecture du témoin REMONTE au lieu d'être transformé en
      avertissement. Le 06-09-2026, ce programme affichait « FICHIER RÉEL ABSENT —
      les épreuves sont INCOMPLÈTES », annonçait « 9/9 cas passent » alors qu'il en
      manquait six, ET RENDAIT 0. Le message était là, et la machine qui ne lit
      qu'un code de sortie voyait « tout va bien ». Un contrôle qui n'a pas pu
      tourner rend un code de sortie non nul (R-734bis) : c'est ce que le code 2
      dit ici.
    ⑨ CE QUI CLOCHE —
      ① Les trois vérifications de date se font par un mécanisme que le langage
      désactive à la demande. Lancé avec l'option qui les retire, le programme joue
      quinze tests au lieu de dix-huit vérifications et sort en code 0 sans qu'une
      ligne signale l'absence. Un garde-fou qui disparaît sur une option de
      lancement n'est pas un garde-fou.
      ② Le compte attendu n'est écrit nulle part. Elle rend vrai dès que tous les
      tests DRESSÉS passent, quel que soit leur nombre : s'il n'en restait qu'un,
      la sortie annoncerait « 1/1 cas passent » et le code serait 0. Ce qui protège
      aujourd'hui est la levée du témoin, pas un compte attendu.
      ③ Elle ne teste que `controler_une_seance`. Cinq des douze fonctions du
      module ne sont jamais appelées par ce jeu d'épreuves : ni `controler`, qui
      décide du sort d'un lot entier, ni `ajouter_au_fichier`, qui écrit — c'est
      pourtant la seule fonction du module qui touche un fichier, et c'est elle qui
      a porté le défaut le plus grave, celui qui soudait deux journées en une.
      ④ Son texte d'origine annonce que « ces cas sont écrits À LA MAIN, pas dérivés
      du code », alors que six des seize sont dérivés d'une ligne de fichier et un
      septième est ajouté plus bas. La phrase décrit l'état d'avant l'ajout des
      tests venus de la vraie donnée.
      ⑤ Le seizième test vérifie que la séance à date ambiguë passe le contrôle de
      séance, et son libellé annonce que « l'ÉCRITURE la refusera ». Cette
      deuxième moitié n'est jamais jouée : `ajouter_au_fichier` n'est pas appelée.
      La promesse est dans le texte du test, pas dans le test.
    ⑩ EFFET — AFFICHE une ligne par test, une ligne vide et une ligne de total.
      LIT temoins/TEMOIN_cours_reels.csv, par l'intermédiaire de
      `_cas_venus_du_vrai_fichier`. N'écrit AUCUN fichier, ne touche pas au réseau,
      ne modifie aucune donnée du dépôt.
    ⑪ TERMINAISON — Rend la main avec vrai ou faux dans le cas normal, et le
      lancement du programme en fait un code de sortie, 0 ou 1. Un de ses appels
      peut ne pas revenir en rendant une valeur : `_cas_venus_du_vrai_fichier` lève
      quand le témoin est absent ou a changé, et cette levée traverse cette
      fonction sans être rattrapée ; le lancement du programme l'attrape et SORT DU
      PROGRAMME avec le code 2 — mesuré le 19-09-2026 sur une copie du dépôt. Elle
      peut aussi LEVER elle-même si l'une des trois vérifications de date est
      fausse, et cette levée-là n'est attrapée par personne.
      [sort: non]
    ⑫ DÉFINITIONS
  une séance : une journée de bourse pour une valeur, avec son ouverture, son
    plus haut, son plus bas, sa clôture et son volume.
  le fichier des cours : le fichier où les séances s'empilent sans jamais être
    réécrites ; au dépôt, c'est donnees/claude_cours_nouveaux.csv.
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
    étant qu'une copie de lecture
  le jeu d'épreuves : les cas de contrôle que le programme lance sur lui-même,
    avec l'argument `epreuves`
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par
    GitHub Actions — collecte, versement, signaux, positions, mesure,
    surveillance.
      le témoin : le fichier temoins/TEMOIN_cours_reels.csv, copie figée de vraies
        séances, sur laquelle les épreuves tournent toujours à l'identique.
    
    
  un garde-fou : une limite qui, franchie, fait cesser a la strategie de prendre position tout en continuant a la mesurer.
"""
    cas = [
        ({"valeur": "TOTALENERGIES", "date": "2026-09-04", "open": 58.0,
          "high": 59.0, "low": 57.5, "close": 58.5, "volume": 1000},
         "SANS_REFERENCE", "séance normale SANS clôture précédente — le test 4 le DIT"),
        ({"valeur": "X", "date": "2026-09-04", "open": 10, "high": 9,
          "low": 11, "close": 10, "volume": 100},
         "BLOQUANT", "High < Low"),
        ({"valeur": "X", "date": "2026-09-04", "open": 12, "high": 11,
          "low": 10, "close": 10.5, "volume": 100},
         "BLOQUANT", "Open au-dessus du High"),
        ({"valeur": "X", "date": "2026-09-04", "open": 10.5, "high": 11,
          "low": 10, "close": 9, "volume": 100},
         "BLOQUANT", "Close sous le Low"),
        ({"valeur": "X", "date": "2026-09-04", "open": 10, "high": 11,
          "low": 10, "close": 10.5, "volume": 0},
         "BLOQUANT", "Volume nul"),
        ({"valeur": "X", "date": "2026-09-04", "open": 10, "high": 11,
          "low": 10, "close": 10.5, "volume": None},
         "BLOQUANT", "Volume manquant"),
        ({"valeur": "X", "date": "2026-09-04", "open": 10, "high": 20,
          "low": 10, "close": 20, "volume": 100, "close_precedent": 10},
         "ALERTE", "variation +100 % — signalée, PAS rejetée"),
        ({"valeur": "X", "date": "2026-09-04", "open": 10, "high": 11,
          "low": 9, "close": 9.5, "volume": 100, "close_precedent": 10},
         "OK", "variation -5 %, sous le seuil"),
        ({"valeur": "X", "date": "2026-09-04", "open": "10,5", "high": "11,0",
          "low": "10,0", "close": "10,8", "volume": "1 000"},
         "SANS_REFERENCE", "virgule décimale et espace de milliers"),
    ]
    # RÈGLE DE COWORK, 06-09-2026 — LA PLUS IMPORTANTE DE TOUTES :
    # « Un jeu d'épreuves doit contenir au moins un cas où le programme est appelé
    # avec ce que la VRAIE donnée contient, pas avec ce que le programmeur suppose
    # qu'elle contient. » Les neuf premiers cas sont écrits à la main, et pas un
    # seul ne venait d'une ligne du fichier des cours. C'est ce qui a laissé passer
    # NEUF défauts, dont un qui soudait deux séances en une.
    # L'ÉCHEC REMONTE. Il n'est ni rattrapé ni transformé en avertissement.
    cas.extend(_cas_venus_du_vrai_fichier())

    # TOUR 6 : la date ambigue est REFUSEE, pas devinee
    assert normaliser_date("09/04/2026") is None, "date ambiguë acceptée"
    assert normaliser_date("25/09/2026") == "2026-09-25", "date sans ambiguïté refusée"
    assert normaliser_date("2026-09-04") == "2026-09-04"
    cas.append(({"valeur":"X","date":"09/04/2026","open":1,"high":2,"low":1,"close":1.5,"volume":10},
                "SANS_REFERENCE", "date ambiguë 09/04 : le contrôle de séance passe, l'ÉCRITURE la refusera"))

    passes = 0
    for seance, attendu, libelle in cas:
        obtenu, motif = controler_une_seance(seance)
        ok = obtenu == attendu
        passes += ok
        print(f"  {'OK  ' if ok else 'FAUX'} {libelle:<42} attendu {attendu:<9} obtenu {obtenu}")
        if not ok and motif:
            print(f"       motif rendu : {motif}")
    total = len(cas)
    print(f"\n  {passes}/{total} cas passent")
    return passes == total


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "epreuves":
        print(f"CONTROLER LES COURS — jeu d'épreuves · {_maintenant():%d-%m-%Y %Hh%M} (Paris)\n")
        try:
            sys.exit(0 if _epreuves() else 1)
        except FileNotFoundError as e:
            # Code 2, distinct du 1 : « n'a pas pu tourner » n'est pas
            # « a tourné et a échoué ». Les deux échouent, ils ne disent pas
            # la même chose.
            print(f"\n  ❌ {e}")
            sys.exit(2)
    print("Usage : python3 CONTROLER_LES_COURS.py epreuves")
    print("Sinon, ce module s'importe : controler(seances) puis ajouter_au_fichier(...)")
