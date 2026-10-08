#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DÉCIDÉ · outil · v1.5 · 28-08-2026 · Rôle : fabriquer le PILOTE depuis le socle et le projet.
Quand l'appeler : chaque soir après l'audit. Jamais à la main.

VERSION 1.5 — LE JARGON EST REMPLACÉ PAR DEUX MOTS QUI SE COMPRENNENT SEULS.
    « GROUPE 1 » et « GROUPE 2 » n'apprenaient rien : il fallait ouvrir le
    registre pour savoir lequel était lequel. Remarque de Jean-Luc le 28/08.
    DÉCIDÉ   = écrit par un humain, ne se régénère jamais.
    FABRIQUÉ = recréé par un programme ; le modifier à la main serait écrasé
               au passage suivant — c'est là qu'est le vrai danger.
    Les anciennes mentions restent acceptées le temps que les fichiers migrent :
    on ne casse pas ce qui déclare déjà.

VERSION 1.4 — LE DERNIER NOMBRE ÉCRIT EN DUR EST SUPPRIMÉ
    La ligne « performance de référence » n'était comptée nulle part : c'était un
    LITTÉRAL dans ce fichier, précédé d'un repli sur une clé de golden qui
    n'existe pas — le repli s'appliquait donc TOUJOURS. Le chiffre était juste le
    27/08 et le serait resté indéfiniment : le jour où la performance change, le
    pilote aurait affiché celle du 23/08 sans un mot. C'est exactement le zéro
    silencieux, dans le programme qui prétend le combattre.
    Elle est désormais LUE dans R-722, la règle qui la définit. Si R-722 manque
    ou devient illisible au motif, la ligne n'est pas affichée et le fait est
    SIGNALÉ — jamais remplacée par une valeur de secours.
    Trouvé par relecture adverse le 27/08, sur le seizième chiffre du tableau.

VERSION 1.3 — trois défauts qui ne se manifestaient pas encore mais se
manifesteront un jour, tous relevés à la relecture du 27/08 :
    · un fichier de chiffres figés SANS DATE lisible dans son nom était classé
      « le moins récent » et écarté EN SILENCE, alors que l'alerte d'ambiguïté
      l'annonçait — les deux mécanismes se contredisaient. Il est désormais
      SIGNALÉ.
    · le tri du journal des trades était ALPHABÉTIQUE. Il coïncide avec l'ordre
      chronologique parce que les dates s'écrivent AAAA-MM-JJ — par chance, pas
      par construction. Les dates sont normalisées avant tri.
    · la colonne de date de sortie était la PREMIÈRE dont le nom contient
      « sortie » : l'ordre du dictionnaire décidait à la place d'une règle
      (A-284). Le nom est maintenant exact, et l'absence de colonne reconnue
      est signalée au lieu d'être subie.

VERSION 1.2 — CE QUI CHANGE DEPUIS LA 1.1, issu de la relecture adverse du 27/08
    · LE ZÉRO SILENCIEUX EST FERMÉ SUR TOUTES LES PORTES. La classe Illisible
      existait mais ne gardait que deux des six sources. Un fichier de cours
      illisible donnait « séances 0, valeurs 0 » SANS UNE SEULE ALERTE, sur le
      fichier le plus lourd du système. Mesuré, puis corrigé et retesté : les
      cours, le sas, l'état civil et le journal des trades sont désormais
      protégés comme le registre et le backlog.
    · LE GOLDEN LE PLUS RÉCENT est retenu, jamais le premier par ordre
      alphabétique. R-701 interdit de détruire l'ancien golden du 12/07 ; le
      jour où il revient au projet, un tri alphabétique le placerait AVANT
      celui du 01/08 et le pilote annoncerait 85 opérations sans un mot.
      La présence de plusieurs goldens est en outre SIGNALÉE.
    · LE DERNIER TRADE CLOS est celui dont la date de sortie est la plus
      tardive, jamais la dernière ligne écrite du fichier : rien ne garantit
      que le journal soit trié.

LIMITE CONNUE, NON CORRIGÉE : le contrôle de régression compare des LIBELLÉS.
Tout renommage d'une ligne du tableau produira une alerte de régression, qui
sera à ignorer ce jour-là — et une alerte qu'on apprend à ignorer cesse de
protéger. Le remède serait de comparer des sources, pas des noms d'affichage.

VERSION 1.1 — CE QUI CHANGE DEPUIS LA 1.0 (26-08-2026 23h00)
    · os.walk au lieu de os.listdir : les SOUS-DOSSIERS sont vus. Mesuré le
      26/08 : « claude/ » porte 29 fichiers sur 114, dont les positions
      ouvertes. Le disque monté les aplatit à la racine, ce qui masquait
      entièrement le défaut de ce côté-là.
    · l'identité d'un fichier ne se joue plus sur une troncature à 14
      caractères mais sur le motif entier (A-284 : ne jamais laisser l'ordre
      alphabétique trancher à la place d'une décision).
    · le pilote déclare EN TÊTE le canal sur lequel il a été fabriqué et le
      nombre de fichiers vus. Le même programme lu par deux canaux produit
      deux pilotes différents : il ne calcule pas mal, il ne voit pas la même
      chose.

LA VERSION VIT DANS CE FICHIER, ET C'EST DÉLIBÉRÉ (R-713). Deux entrées du
projet ont porté ce nom sans qu'on puisse les distinguer autrement qu'en
lisant leur code. Toute version future incrémente ce numéro.
Quand l'appeler : chaque soir, après l'audit. Jamais à la main.

CE QU'IL FAIT
    Il lit le socle écrit à la main, compte ce qui est comptable, liste les
    fichiers et leur rôle déclaré, et ÉCRIT le pilote.

CE QU'IL NE FAIT JAMAIS
    Il n'invente aucun chiffre : tout est compté depuis les sources.
    Il n'écrit dans aucun autre fichier.
    Il ne corrige rien : il signale.

POURQUOI IL EXISTE
    Le 25-08-2026, le pilote a été mis à jour section par section et une section
    sur neuf a été oubliée : 40 fichiers manquaient à sa carte. Ce n'était pas
    une inattention, c'était une projection maintenue à la main. Ce programme
    supprime la chose à se rappeler au lieu de demander de mieux s'en souvenir.

LES NOMS ONT DEUX GRAPHIES selon le canal — espaces ou soulignés. Rien n'est
supposé : chaque fichier est CHERCHÉ dans les deux formes, et le nom réellement
trouvé est affiché.

════════════════════════════════════════════════════════════════════════
LES DOUZE ÉLÉMENTS — R-752 les pose à tous les niveaux, et le programme
entier est le premier niveau
════════════════════════════════════════════════════════════════════════
① RÔLE — Fabriquer gouvernance/PILOTE.md, le document que le rituel de début de
  session fait lire en premier et que la hiérarchie documentaire place au-dessus
  de tous les autres. Le pilote dit trois choses : ce qui cloche, où en est le
  projet en une quinzaine de chiffres, et quels fichiers déclarent leur rôle. Ce
  programme ne décide rien et ne corrige rien : il compte sur les fichiers eux-
  mêmes, il liste, il signale. Ce qui se calcule ne s'écrit jamais à la main
  (R-728), et le pilote est l'exemple que cette règle cite en premier.
② CONTEXTE D'APPEL — UN SEUL APPELANT AUTOMATIQUE : le pas « Fabriquer le
  PILOTE » de .github/workflows/collecte_abc.yml, qui écrit
  `python3 programmes/claude_FABRIQUER_LE_PILOTE.py "$GITHUB_WORKSPACE"
  "$GITHUB_WORKSPACE/gouvernance/PILOTE.md"`. Cette tâche part du lundi au
  vendredi à 18 h UTC, ce qui fait 20 h à Paris en été et 19 h en hiver, et le
  pas porte `continue-on-error: true` : son échec est annoncé mais n'arrête pas
  le reste du circuit. Aucun programme de programmes/ ne l'importe ni ne le
  lance : relevé le 19-09-2026 par recherche de son nom dans programmes/ et dans
  .github/workflows/, les seules mentions hors de la tâche planifiée sont des
  textes explicatifs d'autres programmes.
③ ENTRÉE — Deux arguments de ligne de commande, tous deux facultatifs. Le
  premier est la racine à lire, et le second le fichier à écrire. Sans le
  premier, la racine vaut `/mnt/project`. Sans le second, la sortie est
  `<racine>/gouvernance/PILOTE.md`, ou `<racine>/PILOTE.md` si le dossier
  `gouvernance` n'existe pas. La variable d'environnement `DEPOT_CAC40` est lue
  elle aussi, comme second endroit où chercher le registre et le backlog.
④ CONDITIONS D'ENTRÉE — La racine doit exister et se parcourir. Le dossier du
  fichier de sortie doit exister : mesuré le 19-09-2026 sur une copie du dépôt,
  un lancement sans aucun argument fait tout le travail puis s'arrête sur
  « FileNotFoundError: [Errno 2] No such file or directory:
  '/mnt/project/PILOTE.md' », et rien n'est écrit.
⑤ SORTIE — Un code de sortie, et un seul : 0. Il vaut 0 que le pilote porte
  zéro alerte ou dix. Tout le reste est écrit dans le fichier de sortie et
  affiché à l'écran.
⑥ TRAITEMENT — ① lire le socle écrit à la main · ② compter sur chaque source
  les chiffres du tableau · ③ relever le rôle déclaré en tête de chaque fichier ·
  ④ dresser la liste des alertes · ⑤ composer le texte du pilote · ⑥ le comparer
  au pilote de la veille et signaler tout élément disparu · ⑦ écrire le fichier ·
  ⑧ afficher le bilan et les alertes.
⑦ UNITÉ — Des NOMBRES DE FICHIERS, de lignes, de règles, d'actions et de
  séances. Deux grandeurs seulement sortent de là : les octets du projet, et les
  euros des chiffres figés. L'horodatage est en heure de Paris.
⑧ POURQUOI — Le 25-08-2026, le pilote était tenu à la main, section par
  section ; une section sur neuf a été oubliée et 40 fichiers ont disparu de sa
  carte sans que personne le voie. Ce programme supprime la chose à se rappeler
  au lieu de demander de mieux s'en souvenir.
  Il déclare en tête du pilote le canal sur lequel il a lu et le nombre de
  fichiers qu'il a vus, parce que le même programme lancé depuis deux endroits
  produit deux pilotes différents : il ne calcule pas mal, il ne voit pas la
  même chose. Le pilote fabriqué le 17-09-2026 porte ainsi « Canal de lecture :
  `/home/runner/work/Cac-40-signals-sur-git-hub-pour-Claude-/Cac-40-signals-sur-
  git-hub-pour-Claude-` — 238 fichiers vus ».
  Il n'écrit qu'un seul fichier, et jamais dans une source : un document qui
  corrigerait ce qu'il mesure ne mesurerait plus rien.
⑨ CE QUI CLOCHE —
  ① Le nombre d'actions annoncé par le tampon du backlog n'est lu que derrière
  le mot OK. Le motif employé exige les lettres OK suivies de deux étoiles, puis
  le nombre, puis le mot actions ; un tampon d'échec ne rapproche donc rien et ne
  rend aucun nombre. Mesuré le 19-09-2026 : le backlog du
  dépôt porte « CONTRÔLE AUTOMATIQUE : ÉCHEC** — 413 actions au tableau » et
  418 lignes de tableau ; le pilote fabriqué affiche « actions au tampon : ? »
  et n'émet AUCUNE alerte d'écart, parce que la comparaison exige deux entiers
  et que « ? » n'en est pas un. L'écart de cinq lignes existe et ne se voit
  nulle part. Le jour où le contrôle du backlog échoue est précisément celui où
  l'on voudrait connaître ce nombre.
  ② RÉGLÉ LE 28-09-2026 (A-435 ①) : la version se lit sur le pied de page du
  registre, la dernière ligne qui porte son titre suivi de « vN.N » (limite
  connue : une citation du titre suivie d'une version, placée APRÈS le pied,
  serait prise pour lui ; un titre écrit en minuscules donne « ? ») ; épreuve dans
  tests/EPREUVES_DE_LA_VERSION_DU_REGISTRE_Lun_28-09-2026.py. Ce qui était mesuré :
  la version du registre est lue sur la ligne qui dit de ne pas la lire. Le
  motif prend le premier « vN.N » des 400 premiers caractères de
  gouvernance/REGISTRE_REGLES.md. Or ces 400 caractères portent un
  avertissement : « LA VERSION ET LE COMPTE DES RÈGLES NE SONT PAS ICI — ILS SE
  LISENT EN PIED DE PAGE. Corrigé le 13-09-2026 : cette ligne portait « v4.0 »
  quand le pied de page portait « v4.4 » ». Le motif attrape ce « v4.0 » cité
  comme contre-exemple. Mesuré le 19-09-2026 : le pilote annonce « version du
  registre : 4.0 », tandis que le pied de page du registre porte « v6.1 ·
  révisé le 19-09-2026 ». Deux versions majeures d'écart, dans le document que
  le rituel fait lire en premier.
  ③ Un chemin écrit en dur sert de repli et fait lire un clone périmé. Le
  registre et le backlog sont cherchés dans quatre endroits successifs : la
  racine donnée, la variable d'environnement `DEPOT_CAC40`, puis `/tmp/depot` et
  `/tmp/depot/d`. La racine donnée passe bien en premier, mais seulement si elle
  PORTE le fichier ; sinon le repli s'applique en silence. Mesuré le
  19-09-2026 : lancé sur un dossier d'essai ne contenant ni backlog ni registre,
  le pilote a annoncé « actions au tampon 382 · règles R 105 · version du
  registre 4.0 · origine du registre : dépôt », tous lus dans `/tmp/depot`, un
  clone daté du 12-09-2026, vieux de sept jours — et aucune alerte « SOURCE
  INTROUVABLE » n'a été émise. Le vrai dépôt porte 418 lignes de tableau et
  116 règles R.
  ④ Cinq chiffres sont comptés et jamais affichés, parce que la liste qui fixe
  l'ordre du tableau ne les nomme pas. Mesuré le 19-09-2026 sur une copie du
  dépôt : « règles I » vaut 11, « lignes de tableau » 418, « lignes de
  positions » 0, « octets du projet » 10 703 473, et « première séance » est
  également calculée. Aucun des cinq n'apparaît dans le pilote. Le commentaire
  qui accompagne le comptage des règles I explique qu'un chapitre entier de la
  loi était invisible au pilote ; il l'est encore, pour une autre raison, deux
  cents lignes plus loin.
  ⑤ La place occupée par le projet a de nouveau disparu du tableau, sans un mot.
  Mesuré le 19-09-2026 : rapports/audit_du_jour.md ne porte ni « PLACE PROJET :
  NN,NN % » ni « Place RÉELLE », les deux seules écritures que le lecteur
  accepte, et la ligne « place du projet » est absente du pilote fabriqué. Le
  contrôle de régression ne la rattrape pas non plus, parce que
  gouvernance/PILOTE.md du 17-09-2026 ne la porte pas davantage : dès qu'un
  élément manque deux jours de suite, sa disparition devient définitivement
  invisible.
  ⑥ Le programme rend toujours 0. La tâche planifiée ne juge le pas que sur ce
  code, et son message d'erreur ne part donc jamais : un pilote annonçant
  « SOURCE INTROUVABLE » ou « RÉGRESSION » laisse un pas vert derrière lui. Un
  contrôle qui ne peut pas faire rougir ce qu'il surveille n'est pas un contrôle.
  ⑦ Une seconde classe du même nom vit ailleurs. programmes/COMMUN.py ligne 687
  porte une classe `Illisible` qui n'est pas celle-ci : la sienne prend un second
  paramètre `chemin` et porte une méthode `__repr__`. Mesuré le 19-09-2026 :
  afficher un objet d'ici rend « <P.Illisible object at 0x7fdc01e34fd0> », celui
  de COMMUN rend « Illisible('fichier vide') ». Deux implémentations d'une même
  chose divergent toujours (R-708).
  ⑧ Le module `glob` est importé et n'est employé nulle part. Relevé le
  19-09-2026 en comparant les noms importés aux noms employés dans l'arbre
  syntaxique du fichier : `glob` est le seul import sans usage.
⑩ EFFET — ÉCRIT UN SEUL FICHIER, celui nommé en second argument, et le réécrit
  entièrement à chaque passage. Il LIT le registre, le backlog, les cours, l'état
  civil des stratégies, les positions ouvertes, les chiffres figés, le journal
  des trades, l'audit du soir, le socle et le pilote de la veille, puis parcourt
  l'arborescence entière pour compter les fichiers et lire leurs six premières
  lignes. AUCUN ACCÈS RÉSEAU. Il ne touche à aucune source et ne supprime rien.
⑪ TERMINAISON — SORT DU PROGRAMME avec le code rendu par `main`, toujours 0.
  Et un de ses appels peut ne pas revenir : `main` lève une erreur non rattrapée
  quand le dossier du fichier de sortie n'existe pas — mesuré le 19-09-2026 sur
  un lancement sans argument.
⑫ DÉFINITIONS
  le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui dit
    ou en est le projet, ce qu'il contient et ce qui cloche
  le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté ailleurs.
  le depot : le depot GitHub ou vivent les fichiers du systeme, le projet n'en
    etant qu'une copie de lecture
  le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions et des actions du projet
  le tampon : la ligne d'horodatage posee en tete du backlog par
    programmes/verif_backlog.py, qui annonce elle-meme un nombre d'actions
  le registre : gouvernance/REGISTRE_REGLES.md, le document qui porte les regles
    numerotees du projet ; une regle absente du registre n'existe pas
  la tache planifiee : un fichier de .github/workflows/ qui fait tourner un
    programme a heure fixe sur une machine GitHub, sans clic ni autorisation
  les chiffres figes : gouvernance/golden_tests_*.json, les resultats de
    reference qu'un calcul juste doit retrouver au centime pres
  l'audit du soir : programmes/audit_ecosysteme.py, lance chaque soir par la
    tache planifiee, qui ecrit rapports/audit_du_jour.md
  l'etat civil des strategies : donnees/cac40_strategies.csv, la liste des
    strategies avec pour chacune son etat de vie, son compteur et son univers
  le sas : les fiches de strategie en etat LABO a l'etat civil, celles qui
    attendent d'etre jugees par le juge des stratégies
  le zero silencieux : un chiffre affiche a zero parce que la lecture a rate,
    et que rien ne distingue ce ratage d'un vrai zero
  un role declare : la mention DECIDE ou FABRIQUE placee en tete d'un fichier,
    qui dit si ce fichier s'ecrit a la main ou se refabrique tout seul
  le controle de regression : la comparaison du pilote en cours de fabrication
    avec celui de la veille, un element disparu etant tenu pour une perte
  l'ecosysteme : l'ensemble des fichiers qui font tourner le systeme, par
    opposition aux dossiers de travail qu'un programme fabrique puis abandonne
  une seance : une journee de bourse pour une valeur, avec son ouverture, son
    plus haut, son plus bas, sa cloture et son volume
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
  la tâche planifiée : un fichier de .github/workflows/ qui fait tourner un programme à heure fixe sur une machine GitHub, sans clic ni autorisation.
  le golden : le fichier gouvernance/golden_tests_*.json, qui fige des chiffres de référence ; tout écart à données identiques est une régression.
  le zéro silencieux : un programme qui rend zéro là où il aurait dû dire qu'il n'a pas pu lire, sans rien afficher
  les chiffres figés : les résultats d'un test sur le passé, enregistrés une fois pour toutes, auxquels on compare ce que le système obtient vraiment
  une clé : le texte obtenu après rapprochement, qui sert à comparer deux noms et n'est jamais affiché à un lecteur
"""

import csv
import glob
import os
import unicodedata
import re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")
JOURS = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]


# ─── CE QUI N'EST PAS L'ÉCOSYSTÈME N'ENTRE PAS DANS LE PILOTE ───
# Trouvé le 13-09-2026 par le premier passage de bout en bout. Le pilote
# annonçait « 2 fichiers de chiffres figés » en nommant DEUX FOIS LE MÊME :
# `PUBLIER_LE_SITE` fabrique `_site_travail/` quelques secondes avant lui, et
# y recopie les données pour bâtir le cockpit. **Le pilote comptait ce dossier
# de travail comme s'il faisait partie du système** — d'où le golden en double,
# et une partie des 142 « rôle non déclaré » (`_site_travail/cac40_ohlcv.csv`…).
# Le socle porte la même exclusion depuis hier ; le pilote ne l'avait pas.
_HORS_ECOSYSTEME = ("_site_travail", ".git", "__pycache__", "archives", "node_modules")


def _marcher(base):
    """os.walk, mais sans les dossiers qui ne sont pas l'écosystème.

① RÔLE — Parcourir l'arborescence du dépôt en laissant dehors ce qui n'est pas le
  système. Tous les comptages de fichiers du pilote passent par ici : sans ce
  filtre, le pilote compte comme siens les fichiers de travail qu'un autre
  programme vient de fabriquer, et ses chiffres gonflent sans que rien ne le dise.
② CONTEXTE D'APPEL — Trois appelants, tous dans ce fichier, et jamais hors de
  lui. ① `trouver`, deux fois, pour ses deux parcours de repli quand un fichier
  n'a pas été trouvé par son nom exact. ② `compter`, deux fois : pour chercher
  les fichiers de chiffres figés, puis pour dresser la liste de tous les
  fichiers. ③ `roles`, une fois, pour visiter chaque fichier et y lire son rôle
  déclaré. Une fabrication déclenche donc une dizaine de parcours complets.
③ ENTRÉE — `base` : le dossier à parcourir. Les appelants transmettent sans le
  modifier la racine reçue en premier argument de la ligne de commande — lors du
  passage du soir, le dossier de travail de la machine GitHub, que le pilote
  fabriqué le 17-09-2026 affiche en tête sous la forme
  `/home/runner/work/Cac-40-signals-sur-git-hub-pour-Claude-/Cac-40-signals-sur-git-hub-pour-Claude-`.
④ CONDITIONS D'ENTRÉE — Aucune. Un chemin inexistant ne la fait pas tomber : le
  parcours ne rend simplement aucun triplet.
⑤ SORTIE — Ne rend rien par `return` : **c'est un générateur, il produit ses
      valeurs une par une**, morceau par morceau : pour chaque dossier visité,
  un triplet — le chemin du dossier, la liste de ses sous-dossiers retenus, la
  liste de ses fichiers. C'est un générateur : rien n'est parcouru tant que
  l'appelant ne consomme pas.
  [rend: générateur]
⑥ TRAITEMENT — ① demander à `os.walk` de descendre depuis `base` · ② remplacer
  SUR PLACE la liste des sous-dossiers par ceux dont le nom n'est pas dans la
  liste des exclus, ce qui empêche la descente dans les autres · ③ rendre le
  triplet à l'appelant.
⑦ UNITÉ — Un NOMBRE DE FICHIERS et de dossiers. Aucune grandeur physique.
⑧ POURQUOI — Cinq noms sont exclus, et l'un d'eux vient d'un incident précis. Le
  13-09-2026, le premier passage de bout en bout a fabriqué un pilote qui
  annonçait « 2 fichiers de chiffres figés » en nommant DEUX FOIS LE MÊME :
  programmes/PUBLIER_LE_SITE.py fabrique le dossier `_site_travail/` quelques
  secondes avant le pilote et y recopie les données pour bâtir le cockpit. Le
  pilote comptait ce dossier de travail comme s'il faisait partie du système,
  d'où le doublon et une partie des 142 fichiers alors déclarés « rôle non
  déclaré ». Les quatre autres exclus — `.git`, `__pycache__`, `archives`,
  `node_modules` — ne sont pas davantage le système : le premier est la mémoire
  de l'outil de version, le deuxième un cache du langage, le troisième contient
  par définition ce qui est tombé, le quatrième les dépendances d'un site.
  Le remplacement se fait SUR PLACE, sur la liste que `os.walk` prête, parce que
  c'est la seule façon de lui dire de ne pas descendre : reconstruire une
  nouvelle liste laisserait le parcours entrer quand même dans les dossiers
  écartés, et le filtre ne servirait qu'à cacher leur nom.
⑨ CE QUI CLOCHE —
  ① Le filtre épelle des noms au lieu de porter sur une propriété. Le critère qui
  tranche tient en une question : si je renomme un dossier, mon contrôle
  change-t-il d'avis ? Ici oui — renommer `_site_travail` en `_travail_du_site`
  le ferait rentrer dans le décompte, et le doublon de chiffres figés du
  13-09-2026 reviendrait à l'identique.
  ② Le dossier `.github` n'est pas exclu, et c'est voulu, mais ses fichiers
  n'arrivent nulle part. Ils sont comptés dans « fichiers du projet », et
  `roles` ne regarde que les extensions .md, .py, .csv et .json : les deux
  fichiers .yml de .github/workflows/, qui sont les tâches faisant tourner tout
  le circuit du soir, ne figurent ni dans la liste des fichiers qui déclarent
  leur rôle, ni dans celle des fichiers qui n'en déclarent pas.
  ③ Le filtre ne porte que sur les DOSSIERS. Un fichier nommé `archives` ou
  `_site_travail` serait compté normalement. Ce n'est pas dangereux aujourd'hui,
  mais le nom de la liste des exclus ne le dit pas.
⑩ EFFET — LIT l'arborescence du dossier reçu. N'écrit aucun fichier, n'affiche
  rien, ne touche pas au réseau. Elle MODIFIE sur place la liste des
  sous-dossiers que `os.walk` lui prête, et c'est précisément par là qu'elle
  agit.
⑪ TERMINAISON — Rend la main à chaque triplet, et s'achève quand l'arborescence
  est épuisée. Elle ne lève pas. Aucun de ses appels ne se termine.
  [sort: non]
⑫ DÉFINITIONS
  l'ecosysteme : l'ensemble des fichiers qui font tourner le systeme, par
    opposition aux dossiers de travail qu'un programme fabrique puis abandonne
  le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui dit
    ou en est le projet, ce qu'il contient et ce qui cloche
  les chiffres figes : gouvernance/golden_tests_*.json, les resultats de
    reference qu'un calcul juste doit retrouver au centime pres
  un role declare : la mention DECIDE ou FABRIQUE placee en tete d'un fichier,
    qui dit si ce fichier s'ecrit a la main ou se refabrique tout seul
  la tache planifiee : un fichier de .github/workflows/ qui fait tourner un
    programme a heure fixe sur une machine GitHub, sans clic ni autorisation
  le depot : le depot GitHub ou vivent les fichiers du systeme, le projet n'en
    etant qu'une copie de lecture
    
  `archives` : le dossier du dépôt où sont rangées les versions tombées, sous un nom qui dit pourquoi elles sont tombées
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
  le cockpit : la page web que ce programme fabrique et que Jean-Luc ouvre pour voir l etat du systeme.
  une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    for d, sd, fs in os.walk(base):
        sd[:] = [x for x in sd if x not in _HORS_ECOSYSTEME]
        yield d, sd, fs


def horodatage():
    """Rend la date et l'heure de Paris, écrites pour être lues.

① RÔLE — Donner au pilote la ligne qui dit quand il a été fabriqué. C'est le
  seul moyen de savoir, en ouvrant le document, si l'on regarde le passage du
  soir ou celui de la veille — et le rituel de début de session commence par
  cette vérification.
② CONTEXTE D'APPEL — `main`, une seule fois, dans la deuxième ligne du pilote.
  Aucun autre appelant : relevé le 19-09-2026, le nom `horodatage` n'apparaît
  qu'à deux endroits de ce fichier, sa définition et cet appel.
③ ENTRÉE — Aucun paramètre.
④ CONDITIONS D'ENTRÉE — Aucune, sauf que la table des fuseaux horaires du
  système connaisse `Europe/Paris`.
⑤ SORTIE — UNE valeur : un texte de la forme « Sam 19-09-2026 23h51 (Paris) »,
  mesuré le 19-09-2026 sur une copie du dépôt. Le jour est abrégé en trois
  lettres, la date s'écrit jour, mois, année.
  [rend: 1]
⑥ TRAITEMENT — ① demander l'heure courante au système en lui imposant le fuseau
  de Paris · ② prendre l'abréviation du jour dans la liste des sept jours, rangée
  du lundi au dimanche · ③ composer le texte.
⑦ UNITÉ — Un INSTANT, en heure de Paris, jamais en heure universelle.
⑧ POURQUOI — Le fuseau est imposé au lieu d'être laissé à la machine parce que
  la machine qui fabrique le pilote n'est pas à l'heure de Paris : la tâche
  .github/workflows/collecte_abc.yml part à 18 h UTC, ce qui fait 20 h à Paris
  en été et 19 h en hiver. Un horodatage pris à l'heure de la machine
  décalerait le pilote d'une à deux heures selon la saison, et deux documents du
  même soir paraîtraient venir de deux moments différents.
  Le jour de la semaine est écrit en toutes lettres abrégées parce que le pilote
  se lit d'abord pour savoir si l'on est un jour de bourse : « Sam » répond sans
  qu'il faille ouvrir un calendrier.
⑨ CE QUI CLOCHE —
  ① La liste des sept jours est écrite dans ce fichier, en français, alors que le
  même besoin existe ailleurs dans le système. Un chiffre ou un libellé qui
  existe ailleurs ne se recopie pas (R-708) : deux listes de jours peuvent
  diverger, par exemple sur l'accentuation, sans qu'aucun contrôle ne les
  compare.
  ② Le texte rendu ne porte pas les secondes. Deux fabrications lancées dans la
  même minute produisent deux pilotes portant exactement le même horodatage, et
  rien ne dit lequel est le dernier.
⑩ EFFET — Aucun. Elle ne lit aucun fichier, n'en écrit aucun, n'affiche rien et
  ne touche pas au réseau.
⑪ TERMINAISON — Rend la main. Elle PEUT LEVER si la machine ne connaît pas le
  fuseau `Europe/Paris`, et cette levée n'est pas rattrapée ici — elle
  arrêterait le programme. Aucun de ses appels ne se termine.
  [sort: non]
⑫ DÉFINITIONS
  le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui dit
    ou en est le projet, ce qu'il contient et ce qui cloche
  la tache planifiee : un fichier de .github/workflows/ qui fait tourner un
    programme a heure fixe sur une machine GitHub, sans clic ni autorisation
    
  la table : `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740, qui porte les neuf seuils et le sens de comparaison de chacun
  le rituel de début de session : les gestes imposés à l'ouverture d'une conversation — relever la date, cloner le dépôt, lire le PILOTE, lire le rapport du radar
  une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    n = datetime.now(PARIS)
    return f"{JOURS[n.weekday()]} {n.strftime('%d-%m-%Y %Hh%M')} (Paris)"


def _norm_nom(x):
    """Normalise un nom de fichier — MÊME RÈGLE QUE LE RADAR, volontairement.
    Deux programmes qui cherchent le même fichier avec deux normalisations
    différentes trouvent la même chose jusqu'au jour où un nom porte un point ou
    une apostrophe : l'un le voit, l'autre non, et personne ne compare. (09-09-2026)

    ① RÔLE — Donner à un nom de fichier UNE seule écriture, pour que deux noms
      puissent être rapprochés malgré leurs accents, leurs majuscules, leurs
      espaces et leurs tirets. C'est ce qui permet de retrouver le registre et le
      backlog quel que soit le canal par lequel ils sont arrivés.
    ② CONTEXTE D'APPEL — `_au_depot`, et elle seule, une fois par nom de fichier
      examiné dans le dossier fouillé. Aucun autre appelant : relevé le
      19-09-2026, le nom `_norm_nom` n'apparaît qu'à deux endroits de ce fichier.
    ③ ENTRÉE — `x` : le nom d'un fichier, tel que le système l'a rendu. Un seul
      appelant, `_au_depot`, qui passe sans les modifier les noms rendus par la
      liste du dossier, par exemple `BACKLOG_DECISIONS.md` ou
      `REGISTRE_REGLES.md`.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un nombre, un texte vide ou rien du tout ne
      la font pas tomber : la valeur est d'abord passée par le texte.
    ⑤ SORTIE — UNE valeur : le nom en minuscules, sans accent, avec un tiret bas
      partout où il y avait un espace ou un tiret. `REGISTRE_REGLES.md` rend
      `registre_regles.md` ; `ANCIEN BACKLOG_DECISIONS.md` rend
      `ancien_backlog_decisions.md`.
      [rend: 1]
    ⑥ TRAITEMENT — ① décomposer chaque lettre accentuée en sa lettre et son
      accent · ② retirer tout ce qui est une marque d'accent · ③ passer en
      minuscules · ④ remplacer chaque espace par un tiret bas · ⑤ remplacer
      chaque tiret par un tiret bas.
    ⑦ UNITÉ — — Un nom n'est pas une grandeur.
    ⑧ POURQUOI — Les noms de ce projet ont deux graphies selon le canal : le même
      document s'écrit avec des espaces d'un côté et avec des tirets bas de
      l'autre. Sans rapprochement, le programme croit qu'il s'agit de deux
      fichiers et n'en trouve aucun.
      La règle de normalisation est VOLONTAIREMENT la même que celle de l'audit
      du soir. Deux programmes qui cherchent le même fichier avec deux
      normalisations différentes trouvent la même chose jusqu'au jour où un nom
      porte un point ou une apostrophe : l'un le voit, l'autre non, et personne
      ne compare les deux réponses. Ce choix a été acté le 09-09-2026.
    ⑨ CE QUI CLOCHE —
      ① « Même règle que le radar » est une promesse que rien ne vérifie. Les deux
      fonctions sont écrites deux fois, dans deux fichiers, et aucun contrôle ne
      compare leurs réponses sur un même nom. Deux implémentations d'une même
      chose divergent toujours (R-708) : le jour où l'une des deux est corrigée
      seule, la promesse tombe sans que rien ne s'affiche.
      ② Le point et l'apostrophe, cités par le texte d'origine comme le cas
      dangereux, ne sont toujours pas traités. Un fichier nommé
      `REGISTRE.REGLES.md` ou `L'ETAT_CIVIL.csv` garde son point et son
      apostrophe après passage ici.
    ⑩ EFFET — Aucun. Elle ne lit aucun fichier, n'en écrit aucun, n'affiche rien
      et ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels
      ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
  le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions et des actions du projet
  le registre : gouvernance/REGISTRE_REGLES.md, le document qui porte les regles
    numerotees du projet ; une regle absente du registre n'existe pas
  l'audit du soir : programmes/audit_ecosysteme.py, lance chaque soir par la
    tache planifiee, qui ecrit rapports/audit_du_jour.md
    
  le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir, qui contrôle l'ensemble du système et range chacun de ses constats sous un numéro de maillon, par exemple 18-Tâches pour le contrôle des traces laissées par les tâches planifiées.
  une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    x = unicodedata.normalize("NFD", str(x))
    x = "".join(c for c in x if unicodedata.category(c) != "Mn")
    return x.lower().replace(" ", "_").replace("-", "_")


def _au_depot(motif, sous_dossiers):
    """Cherche un fichier au DÉPÔT. Rend (chemin absolu, "dépôt") ou (None, None).
    Le REGISTRE et le BACKLOG y vivent depuis les 05 et 08-09-2026 (R-736) ; ce
    programme les cherchait au PROJET, donc la copie périmée qui y traîne ne pouvait
    pas être retirée. Un seul chemin de recherche pour les deux : quand on corrige un
    défaut, on le cherche partout où il vit, pas seulement là où il a été vu.

    ① RÔLE — Trouver au dépôt les deux documents qui font autorité, le registre
      des règles et le backlog des décisions, et dire d'où ils viennent au lieu de
      laisser deviner. Le pilote est le document que le rituel fait lire en début
      de session : s'il annonce une version du registre, il doit pouvoir dire sur
      quelle copie il l'a lue.
    ② CONTEXTE D'APPEL — Deux appelants, tous deux dans ce fichier :
      `_backlog_et_origine` et `_registre_et_origine`, chacun une fois par appel.
      Ces deux-là sont eux-mêmes appelés par `trouver`, donc à chaque recherche du
      registre ou du backlog — une dizaine de fois par fabrication.
    ③ ENTRÉE — `motif` : le morceau de nom à retrouver, déjà écrit en minuscules
      avec des tirets bas, `backlog_decisions` ou `registre_regles` ·
      `sous_dossiers` : la liste ordonnée des dossiers à fouiller, construite par
      `_racines_depot`. Lors du passage du soir, cette liste vaut
      [`$GITHUB_WORKSPACE`, `/tmp/depot`, `/tmp/depot/d`] pour le backlog, les
      mêmes suivis de `/gouvernance` pour le registre.
    ④ CONDITIONS D'ENTRÉE — Le motif doit être écrit comme `_norm_nom` écrit les
      noms : en minuscules, sans accent, avec des tirets bas. Un motif contenant
      une majuscule ou un espace ne rapprocherait rien, et la fonction rendrait
      « introuvable » sans qu'aucune erreur ne s'affiche.
    ⑤ SORTIE — DEUX valeurs. Quand un fichier est trouvé : son chemin absolu, et
      le texte « dépôt ». Quand aucun ne l'est : « rien » et « rien ».
      [rend: 2]
    ⑥ TRAITEMENT — ① prendre les dossiers de la liste, dans l'ordre · ② passer
      ceux qui n'existent pas · ③ lister le dossier et le parcourir par ordre
      alphabétique · ④ rendre le premier fichier dont le nom normalisé CONTIENT le
      motif · ⑤ rendre « rien » si aucun dossier n'a répondu.
    ⑦ UNITÉ — — Un chemin n'est pas une grandeur.
    ⑧ POURQUOI — La recherche est séparée pour ces deux documents parce qu'ils ont
      quitté le projet pour le dépôt les 05 et 08-09-2026, et que la copie périmée
      restée au projet ne pouvait pas être retirée tant que les programmes la
      lisaient encore. Tout fichier du système vit au dépôt, le projet n'en étant
      que la copie de lecture (R-736).
      Un seul chemin de recherche sert aux deux documents, au lieu d'un par
      document : quand on corrige un défaut, on le cherche partout où il vit, pas
      seulement là où il a été vu.
    ⑨ CE QUI CLOCHE —
      ① L'ordre alphabétique décide quel fichier fait foi. La fonction garde le
      PREMIER nom, dans l'ordre alphabétique, dont la forme normalisée contient le
      motif. Mesuré le 19-09-2026 sur une copie : avec un fichier
      `ANCIEN BACKLOG_DECISIONS.md` posé à côté du vrai backlog, le pilote a lu
      l'ancien et affiché « actions au tampon : 99 », puis l'alerte « ÉCART DE
      COMPTAGE : le tampon dit 99, le fichier porte 418 lignes ». C'est exactement
      le défaut que l'action A-284 du backlog enregistre : ne jamais laisser
      l'ordre alphabétique trancher à la place d'une décision. Et la présence de
      plusieurs candidats n'est même pas signalée.
      ② Le mot rendu est toujours « dépôt », quel que soit l'endroit où le fichier
      a été trouvé. Les trois autres chemins fouillés — la variable
      d'environnement `DEPOT_CAC40`, `/tmp/depot` et `/tmp/depot/d` — rendent le
      même mot. Mesuré le 19-09-2026 : lancée sur un dossier ne portant aucun des
      deux documents, la chaîne a lu un clone de `/tmp/depot` daté du 12-09-2026
      et le pilote a tout de même annoncé « origine du registre : dépôt ». La
      fonction qui existe pour dire d'où vient le fichier donne donc la même
      réponse pour quatre provenances, dont une copie vieille de sept jours.
      ③ Le rapprochement se fait par CONTENANCE, pas par égalité. Un fichier nommé
      `REGISTRE_REGLES_ARCHIVE_2025.md` contient `registre_regles` et serait
      retenu si son nom passait avant dans l'ordre alphabétique.
      ④ Une seule cause d'échec est rattrapée. Un dossier existant mais illisible
      fait lever `os.listdir`, et cette levée n'est pas rattrapée ici : elle
      arrête le programme au lieu de faire passer au dossier suivant.
    ⑩ EFFET — LIT la liste des noms de un à quatre dossiers. N'écrit aucun
      fichier, n'affiche rien, ne touche pas au réseau, et ne lit le CONTENU
      d'aucun fichier.
    ⑪ TERMINAISON — Rend la main, par la sortie du premier fichier trouvé ou par
      la sortie finale. Elle PEUT LEVER sur un dossier existant mais illisible.
      Aucun de ses appels ne se termine : `_norm_nom` rend toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS
  le depot : le depot GitHub ou vivent les fichiers du systeme, le projet n'en
    etant qu'une copie de lecture
  le registre : gouvernance/REGISTRE_REGLES.md, le document qui porte les regles
    numerotees du projet ; une regle absente du registre n'existe pas
  le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions et des actions du projet
  le tampon : la ligne d'horodatage posee en tete du backlog par
    programmes/verif_backlog.py, qui annonce elle-meme un nombre d'actions
  le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui dit
    ou en est le projet, ce qu'il contient et ce qui cloche
    
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
  le rapprochement : le fait de reconnaître que deux écritures différentes désignent le même fichier ou la même entreprise
  un motif : un morceau de nom passé à une fonction de recherche, par exemple trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
"""
    for c in sous_dossiers:
        if c and os.path.isdir(c):
            for f_ in sorted(os.listdir(c)):
                if motif in _norm_nom(f_):
                    return os.path.abspath(os.path.join(c, f_)), "dépôt"
    return None, None


# LA RACINE QU ON DONNE PRIME SUR CELLE QUI EST ECRITE EN DUR.
# Trouve le 13-09-2026 par Jean-Luc, sur une alerte que j avais laissee passer :
# le pilote annoncait « le tampon dit 357, le fichier porte 358 » alors que le
# backlog en porte 383. **Il lisait `/tmp/depot/BACKLOG_DECISIONS.md`, un clone
# oublie de plusieurs jours dans la machine du Chat, AVANT de regarder la racine
# qu on lui passe en argument.**
# Sur GitHub le dossier n existe pas, donc le pilote du soir lit le bon fichier —
# mais un programme qui prefere un chemin absolu a son argument est un piege qui
# attend, et il a deja menti une fois dans un rapport lu par Jean-Luc.
_RACINE_DONNEE = [sys.argv[1]] if len(sys.argv) > 1 else []


def _racines_depot(sous=""):
    """Rend la liste ordonnée des dossiers où chercher le registre et le backlog.

    ① RÔLE — Fixer, en un seul endroit, l'ordre dans lequel les deux documents qui
      font autorité sont cherchés. Sans cette liste unique, chaque recherche
      choisirait son propre ordre et deux appels du même programme pourraient lire
      deux fichiers différents.
    ② CONTEXTE D'APPEL — Deux appelants, tous deux dans ce fichier :
      `_backlog_et_origine`, qui l'appelle sans argument, et
      `_registre_et_origine`, qui l'appelle avec `gouvernance`.
    ③ ENTRÉE — `sous` : le sous-dossier à ajouter à chaque racine, ou un texte
      vide pour rester à la racine. Les deux appelants passent l'un un texte vide,
      l'autre `gouvernance`.
    ④ CONDITIONS D'ENTRÉE — Aucune. Les dossiers nommés n'ont pas besoin
      d'exister : c'est `_au_depot` qui écarte ceux qui manquent.
    ⑤ SORTIE — UNE valeur : la liste des chemins à fouiller, dans l'ordre. Elle
      compte de un à quatre éléments selon ce qui est renseigné. Lors du passage du
      soir, la machine GitHub ne définit pas `DEPOT_CAC40` et les dossiers de
      `/tmp` n'existent pas, si bien que seul le premier chemin répond.
      [rend: 1]
    ⑥ TRAITEMENT — ① partir de la racine donnée sur la ligne de commande, si elle
      l'a été · ② y ajouter la variable d'environnement `DEPOT_CAC40`, puis
      `/tmp/depot`, puis `/tmp/depot/d` · ③ écarter les entrées vides · ④ coller le
      sous-dossier demandé à la fin de chacune.
    ⑦ UNITÉ — — Une liste de chemins n'est pas une grandeur.
    ⑧ POURQUOI — La racine donnée sur la ligne de commande passe EN PREMIER, et ce
      n'est pas un détail d'écriture. Le 13-09-2026, Jean-Luc a relevé que le
      pilote annonçait « le tampon dit 357, le fichier porte 358 » alors que le
      backlog du dépôt en portait 383 : le programme lisait
      `/tmp/depot/BACKLOG_DECISIONS.md`, un clone oublié de plusieurs jours,
      AVANT de regarder la racine qu'on lui passait en argument. Un programme qui
      préfère un chemin écrit en dur à son propre argument a déjà menti une fois
      dans un rapport lu par Jean-Luc.
    ⑨ CE QUI CLOCHE —
      ① Faire passer la racine donnée en premier ne suffit pas : les chemins
      écrits en dur restent des REPLIS, et un repli s'applique en silence. Mesuré
      le 19-09-2026 : lancé sur un dossier d'essai ne portant ni backlog ni
      registre, le pilote a annoncé « actions au tampon 382 · règles R 105 ·
      version du registre 4.0 », tous lus dans `/tmp/depot`, un clone daté du
      12-09-2026 — sans aucune alerte, alors que le vrai dépôt porte 418 lignes de
      tableau et 116 règles R. La correction du 13-09-2026 a changé l'ordre, elle
      n'a pas fermé la porte.
      ② Les deux chemins de `/tmp` sont écrits en dur dans le code. Ils désignent
      l'endroit où une session clone le dépôt sur sa propre machine, ce qui n'a
      rien à faire dans un programme lancé par une tâche planifiée. Ils ne se
      voient pas aujourd'hui sur la machine GitHub parce que ces dossiers n'y
      existent pas, mais ils sont un piège qui attend.
      ③ La liste se construit à partir de `sys.argv`, lu au chargement du module,
      et non à partir d'un paramètre. La fonction rend donc une réponse qui dépend
      de la ligne de commande et non de ce qu'on lui demande : un programme qui
      importerait ce fichier pour se servir de `trouver` sur un autre dossier
      verrait le registre lu ailleurs, sans le savoir.
    ⑩ EFFET — LIT la variable d'environnement `DEPOT_CAC40` et la ligne de
      commande. N'écrit rien, n'affiche rien, ne touche pas au réseau, et ne
      regarde même pas si les dossiers existent.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels
      ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
  le depot : le depot GitHub ou vivent les fichiers du systeme, le projet n'en
    etant qu'une copie de lecture
  le registre : gouvernance/REGISTRE_REGLES.md, le document qui porte les regles
    numerotees du projet ; une regle absente du registre n'existe pas
  le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions et des actions du projet
  le tampon : la ligne d'horodatage posee en tete du backlog par
    programmes/verif_backlog.py, qui annonce elle-meme un nombre d'actions
  le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui dit
    ou en est le projet, ce qu'il contient et ce qui cloche
  la tache planifiee : un fichier de .github/workflows/ qui fait tourner un
    programme a heure fixe sur une machine GitHub, sans clic ni autorisation
    
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
  une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    b = _RACINE_DONNEE + [os.environ.get("DEPOT_CAC40", ""), "/tmp/depot", "/tmp/depot/d"]
    return [os.path.join(x, sous) if sous else x for x in b if x]


def _backlog_et_origine():
    """Rend (chemin, origine) du BACKLOG — au dépôt d'abord, à sa racine.
    Sans cela le PILOTE perdait « actions au tampon » en silence : le backlog a
    quitté le projet le 05-09-2026, et seul le prompt de la tâche le rattrapait en
    le recopiant. Un geste qui ne vit que dans une consigne finit par cesser.

    ① RÔLE — Désigner LE fichier de backlog que le pilote lira, et dire d'où il
      vient. Deux chiffres du tableau en dépendent, le nombre d'actions annoncé
      par le tampon et le nombre de lignes du tableau, ainsi que le relevé des
      actions citées mais inexistantes.
    ② CONTEXTE D'APPEL — `trouver`, et elle seule, à chaque fois qu'on lui demande
      un fichier dont l'un des motifs contient `BACKLOG_DECISIONS` — donc quatre
      fois par fabrication : deux appels dans `compter`, un dans `controler` et un
      dans le relevé des sources introuvables.
    ③ ENTRÉE — Aucun paramètre.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — DEUX valeurs, rendues par l'appel à `_au_depot` : le chemin absolu du backlog et le texte « dépôt »,
      ou « rien » et « rien » quand aucun des dossiers fouillés n'en porte.
      [rend: 2]
    ⑥ TRAITEMENT — ① demander la liste ordonnée des racines, sans sous-dossier ·
      ② y chercher un fichier dont le nom normalisé contient `backlog_decisions`.
    ⑦ UNITÉ — — Un chemin n'est pas une grandeur.
    ⑧ POURQUOI — Le backlog a quitté le projet pour le dépôt le 05-09-2026. Tant
      que ce programme le cherchait au projet, la ligne « actions au tampon »
      disparaissait du pilote en silence ; seul le texte de consigne de la tâche
      planifiée la rattrapait, en recopiant le fichier avant chaque passage. Un
      geste qui ne vit que dans une consigne finit par cesser, et rien ne le dit
      le jour où il cesse.
    ⑨ CE QUI CLOCHE —
      ① Elle promet une origine et n'en rend qu'une. Son nom annonce qu'elle dit
      d'où vient le fichier ; en pratique elle rend toujours le même mot, « dépôt »,
      que le backlog ait été lu à la racine donnée, dans le dossier nommé par la
      variable d'environnement `DEPOT_CAC40`, ou dans le clone périmé de
      `/tmp/depot`. Mesuré le 19-09-2026 : sur un dossier d'essai vide, le
      backlog effectivement lu était celui de `/tmp/depot`, daté du 12-09-2026, et
      rien ne l'a dit.
      ② Le texte d'origine dit « au dépôt d'abord », ce qui laisse croire à un
      second recours ; il n'y en a aucun ici. Quand elle rend « rien », `trouver`
      reprend sa recherche ordinaire dans l'arborescence, et c'est ce repli-là,
      écrit ailleurs, qui existe réellement.
    ⑩ EFFET — LIT la liste des noms de un à quatre dossiers, par
      l'intermédiaire de `_au_depot`. N'écrit rien, n'affiche rien, ne touche pas
      au réseau.
    ⑪ TERMINAISON — Rend la main. Un de ses appels peut ne pas revenir :
      `_au_depot` lève sur un dossier existant mais illisible.
      [sort: non]
    ⑫ DÉFINITIONS
  le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions et des actions du projet
  le tampon : la ligne d'horodatage posee en tete du backlog par
    programmes/verif_backlog.py, qui annonce elle-meme un nombre d'actions
  le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui dit
    ou en est le projet, ce qu'il contient et ce qui cloche
  le depot : le depot GitHub ou vivent les fichiers du systeme, le projet n'en
    etant qu'une copie de lecture
  la tache planifiee : un fichier de .github/workflows/ qui fait tourner un
    programme a heure fixe sur une machine GitHub, sans clic ni autorisation
    
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
"""
    return _au_depot("backlog_decisions", _racines_depot())


def _registre_et_origine():
    """Rend (chemin ABSOLU du REGISTRE, origine) — "dépôt" ou "repli projet".
    Rend (None, None) s'il est introuvable des deux côtés.

    LA FONCTION DIT D'OÙ VIENT LE FICHIER, ELLE NE LE LAISSE PAS DEVINER (R-736).
    Sans cette origine, le PILOTE pouvait annoncer « version du registre : 3.8 » en
    ayant lu la copie périmée du projet, sans que rien ne signale que le clone du
    dépôt avait échoué — dans le document même que le rituel fait lire en début de
    session. Mesuré et corrigé le 09-09-2026, à l'identique du radar.

    ① RÔLE — Désigner LE fichier de registre que le pilote lira, et dire d'où il
      vient. Quatre lignes du tableau en dépendent : le nombre de règles R, le
      nombre de règles I, la version du registre et la performance de référence.
    ② CONTEXTE D'APPEL — Deux appelants, tous deux dans ce fichier. ① `trouver`, à
      chaque fois qu'on lui demande un fichier dont l'un des motifs contient
      `REGISTRE_REGLES` — quatre fois par fabrication. ② `compter`, une fois,
      juste après, pour écrire l'origine dans le tableau du pilote.
    ③ ENTRÉE — Aucun paramètre.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — DEUX valeurs, rendues par l'appel à `_au_depot` : le chemin absolu du registre et le texte « dépôt »,
      ou « rien » et « rien » quand aucun des dossiers fouillés n'en porte.
      [rend: 2]
    ⑥ TRAITEMENT — ① demander la liste ordonnée des racines, chacune suivie de
      `gouvernance` · ② y chercher un fichier dont le nom normalisé contient
      `registre_regles`.
    ⑦ UNITÉ — — Un chemin n'est pas une grandeur.
    ⑧ POURQUOI — Le pilote est le document que le rituel fait lire en premier :
      s'il annonce une version du registre, il doit dire sur quelle copie il l'a
      lue. Avant le 09-09-2026, il pouvait annoncer « version du registre : 3.8 »
      en ayant lu la copie périmée restée au projet, sans que rien ne signale que
      le clone du dépôt avait échoué. Tout fichier du système vit au dépôt, le
      projet n'en étant que la copie de lecture (R-736), et la même correction a
      été portée au même moment dans l'audit du soir.
    ⑨ CE QUI CLOCHE —
      ① Le texte d'origine annonce deux réponses possibles, « dépôt » ou « repli
      projet ». Cette fonction ne rend jamais « repli projet » : ce mot est écrit
      dans `compter`, qui le pose lui-même quand cette fonction n'a rien trouvé et
      que `trouver` a fini par trouver le registre ailleurs. Un lecteur qui
      écrirait son appelant d'après ce texte attendrait une valeur qui ne vient
      jamais d'ici.
      ② Le mot « dépôt » est rendu pour quatre provenances différentes. Mesuré le
      19-09-2026 : lancée sur un dossier d'essai ne portant pas de registre, la
      chaîne a lu `/tmp/depot/gouvernance/REGISTRE_REGLES.md`, un clone daté du
      12-09-2026, et le pilote a annoncé « origine du registre : dépôt » avec
      « règles R 105 » — quand le vrai dépôt en porte 116. La fonction qui existe
      pour ne pas laisser deviner l'origine laisse deviner l'essentiel.
      ③ Le registre n'est cherché que dans un sous-dossier `gouvernance`. Un
      registre rangé à la racine du dépôt ne serait pas trouvé par ici ; il ne
      serait rattrapé que par la recherche ordinaire de `trouver`, et l'origine
      deviendrait alors « repli projet » alors que le fichier viendrait du dépôt.
    ⑩ EFFET — LIT la liste des noms de un à quatre dossiers, par
      l'intermédiaire de `_au_depot`. N'écrit rien, n'affiche rien, ne touche pas
      au réseau.
    ⑪ TERMINAISON — Rend la main. Un de ses appels peut ne pas revenir :
      `_au_depot` lève sur un dossier existant mais illisible.
      [sort: non]
    ⑫ DÉFINITIONS
  le registre : gouvernance/REGISTRE_REGLES.md, le document qui porte les regles
    numerotees du projet ; une regle absente du registre n'existe pas
  le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui dit
    ou en est le projet, ce qu'il contient et ce qui cloche
  le depot : le depot GitHub ou vivent les fichiers du systeme, le projet n'en
    etant qu'une copie de lecture
  l'audit du soir : programmes/audit_ecosysteme.py, lance chaque soir par la
    tache planifiee, qui ecrit rapports/audit_du_jour.md
    
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
  une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    return _au_depot("registre_regles", _racines_depot("gouvernance"))


def trouver(base, *motifs):
    """Cherche par motif, dans les deux graphies. Rend le chemin RÉEL ou None.

    LE REGISTRE d'abord au dépôt, quel que soit `base` (R-736) ; à défaut, la
    recherche ordinaire ci-dessous sert de repli sur le projet.

    ① RÔLE — Retrouver un fichier du système à partir d'un bout de son nom, quelle
      que soit la façon dont il est écrit. C'est le seul chemin par lequel ce
      programme atteint ses sources : registre, backlog, cours, état civil des
      stratégies, positions, journal des trades, audit du soir, socle et chiffres
      figés passent tous par ici.
    ② CONTEXTE D'APPEL — Trois appelants, tous dans ce fichier. ① `compter`,
      treize fois, une par source à lire et cinq de plus pour le relevé des
      sources introuvables. ② `controler`, deux fois, pour relire le backlog et le
      registre. ③ `main`, une fois, pour le socle. Aucun appel hors de ce fichier :
      relevé le 19-09-2026 par recherche du nom dans programmes/ et dans
      .github/workflows/.
    ③ ENTRÉE — `base` : le dossier où chercher · `*motifs` : un ou plusieurs bouts
      de nom, essayés dans l'ordre. Les appelants passent la racine reçue sur la
      ligne de commande et des noms écrits tels qu'ils existent, par exemple
      `cac40_ohlcv.csv`, ou `claude_positions_ouvertes.csv` puis
      `positions_ouvertes.csv` quand deux écritures sont possibles.
      `motifs`
④ CONDITIONS D'ENTRÉE — Au moins un motif. Un appel sans motif ne tombe pas
      mais rend toujours « rien », ce qui se lira comme un fichier absent.
    ⑤ SORTIE — UNE valeur : le chemin du fichier trouvé, ou « rien ». Le chemin
      rendu est ABSOLU quand il vient de la recherche au dépôt, et RELATIF à
      `base` quand il vient de la recherche ordinaire. Les deux formes coexistent
      dans la même sortie.
      [rend: 1]
    ⑥ TRAITEMENT — ① si l'un des motifs nomme le registre, le chercher d'abord au
      dépôt et rendre ce chemin s'il existe · ② faire de même pour le backlog ·
      ③ essayer chaque motif tel quel à la racine, puis avec ses tirets bas changés
      en espaces, puis l'inverse · ④ parcourir toute l'arborescence et rendre le
      premier fichier dont le nom est exactement le motif, espaces et tirets bas
      confondus · ⑤ parcourir de nouveau et rendre le premier fichier, par ordre
      alphabétique, dont le nom COMMENCE par le motif privé de son extension ·
      ⑥ rendre « rien ».
    ⑦ UNITÉ — — Un chemin n'est pas une grandeur.
    ⑧ POURQUOI — Les noms de ce projet ont deux graphies selon le canal par lequel
      ils arrivent : espaces d'un côté, tirets bas de l'autre. Rien n'est supposé,
      chaque fichier est cherché dans les deux formes, et c'est le nom réellement
      trouvé qui est ensuite affiché au pilote.
      La descente dans les sous-dossiers a été ajoutée le 26-08-2026 après mesure :
      le dossier `claude/` portait alors 29 fichiers sur 114, soit un quart du
      projet, dont les positions ouvertes. Une simple liste du dossier racine ne
      les voyait pas, et le canal par lequel le Chat lisait le projet les aplatit à
      la racine, ce qui masquait entièrement le défaut de ce côté-là.
      La dernière recherche compare le motif ENTIER privé de son extension, et non
      une troncature à un nombre fixe de caractères : deux fichiers partageant
      leurs premiers caractères seraient sinon indiscernables, et c'est l'ordre
      alphabétique qui trancherait — ce que l'action A-284 du backlog interdit.
    ⑨ CE QUI CLOCHE —
      ① Pour le registre et le backlog, la fonction IGNORE son propre paramètre
      `base`. Elle passe par `_racines_depot`, qui lit `sys.argv` au chargement du
      module. Demander le registre d'un dossier donné rend donc le registre d'un
      AUTRE dossier, sans que la signature le laisse deviner. Mesuré le
      19-09-2026 : lancé sur un dossier d'essai sans registre, le programme a lu
      `/tmp/depot/gouvernance/REGISTRE_REGLES.md`, clone du 12-09-2026, et annoncé
      « règles R 105 » quand le dépôt en porte 116.
      ② La dernière recherche retient le premier fichier par ordre alphabétique
      dont le nom COMMENCE par le motif, sans jamais signaler qu'il y avait
      plusieurs candidats. C'est le défaut que l'action A-284 enregistre, et il
      survit dans la fonction dont le commentaire cite cette action.
      ③ Les chemins rendus n'ont pas tous la même forme. Le registre et le backlog
      reviennent en chemin absolu, les autres en chemin relatif à `base`. Un
      appelant qui composerait un chemin à partir de ce qui est rendu obtiendrait
      un résultat différent selon la source, et rien ne l'annonce.
      ④ Les cinq recherches successives ne disent jamais laquelle a répondu.
      Trouver un fichier par son nom exact et le trouver par un début de nom dans
      un sous-dossier inattendu ne se valent pas, et l'appelant ne peut pas faire
      la différence.
      ⑤ La liste des extensions retirées avant la dernière comparaison est écrite
      en dur — MD, PY, CSV, JSON, HTML, TXT. Un motif se terminant par `.yml` ou
      `.png` garderait son extension et ne rapprocherait rien.
    ⑩ EFFET — LIT l'arborescence sous `base`, jusqu'à deux parcours complets par
      appel, et la liste des noms des dossiers du dépôt. Ne lit le CONTENU d'aucun
      fichier. N'écrit rien, n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main par l'un de ses six points de sortie. Un de ses
      appels peut ne pas revenir : `_registre_et_origine` et `_backlog_et_origine`
      lèvent sur un dossier existant mais illisible.
      [sort: non]
    ⑫ DÉFINITIONS
  le registre : gouvernance/REGISTRE_REGLES.md, le document qui porte les regles
    numerotees du projet ; une regle absente du registre n'existe pas
  le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions et des actions du projet
  le depot : le depot GitHub ou vivent les fichiers du systeme, le projet n'en
    etant qu'une copie de lecture
  le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui dit
    ou en est le projet, ce qu'il contient et ce qui cloche
  le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté ailleurs.
  les chiffres figes : gouvernance/golden_tests_*.json, les resultats de
    reference qu'un calcul juste doit retrouver au centime pres
  l'etat civil des strategies : donnees/cac40_strategies.csv, la liste des
    strategies avec pour chacune son etat de vie, son compteur et son univers
  l'audit du soir : programmes/audit_ecosysteme.py, lance chaque soir par la
    tache planifiee, qui ecrit rapports/audit_du_jour.md
    
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
  le Chat : la conversation qui rédige la gouvernance du projet et dépose ses versions
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
  un motif : un morceau de nom passé à une fonction de recherche, par exemple trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
  une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if any("REGISTRE_REGLES" in str(m) for m in motifs):
        _d, _ = _registre_et_origine()
        if _d:
            return _d
    if any("BACKLOG_DECISIONS" in str(m) for m in motifs):
        _d, _ = _backlog_et_origine()
        if _d:
            return _d
    for m in motifs:
        for essai in (m, m.replace("_", " "), m.replace(" ", "_")):
            p = os.path.join(base, essai)
            if os.path.exists(p):
                return p
    # LES SOUS-DOSSIERS COMPTENT. Mesuré le 26-08-2026 : le dossier « claude/ »
    # porte 29 fichiers sur 114 — un quart du projet — dont les positions
    # ouvertes. Un os.listdir ne les voit pas, et le disque du Chat les aplatit
    # à la racine, ce qui masquait entièrement le défaut de ce côté-là.
    for m in motifs:
        for d, _, fs in _marcher(base):
            for f in fs:
                if f == m or f.replace(" ", "_") == m.replace(" ", "_"):
                    return os.path.join(d, f)
    cle = [m.replace(" ", "_").upper() for m in motifs]
    for d, _, fs in _marcher(base):
        for f in sorted(fs):
            n = f.replace(" ", "_").upper()
            for c in cle:
                # l'identité se joue sur le motif ENTIER sans son extension,
                # jamais sur une troncature arbitraire : deux fichiers partageant
                # les mêmes premiers caractères seraient sinon indiscernables,
                # et c'est l'ordre alphabétique qui trancherait (A-284).
                racine = re.sub(r"\.(MD|PY|CSV|JSON|HTML|TXT)$", "", c)
                if n.startswith(racine):
                    return os.path.join(d, f)
    return None


class Illisible:
    """NE JAMAIS CONFONDRE « INCONNU » ET « ZERO » (A-226). Une liste vide veut
    dire « zero ligne » ; une lecture ratee doit dire « je n'ai pas pu lire ».
    Tant que les deux partagent la meme valeur, aucun garde-fou ne peut les
    distinguer — c'est le zero silencieux que ce programme est cense combattre.
    Cet objet se comporte comme un vide MAIS se reconnait."""
    def __init__(self, motif):
        """Garde le motif pour lequel une lecture a échoué.

        ① RÔLE — Retenir la raison de l'échec, pour que l'alerte affichée au
          pilote dise POURQUOI la source n'a pas pu être lue et non seulement
          qu'elle ne l'a pas été. Le pilote écrit par exemple « SOURCE ILLISIBLE :
          les cours — FileNotFoundError ».
        ② CONTEXTE D'APPEL — Le langage lui-même, chaque fois qu'un objet
          `Illisible` est construit. Trois endroits le construisent, tous dans ce
          fichier : `lire`, deux fois, et `lignes_csv`, trois fois.
        ③ ENTRÉE — `self` : l'objet en cours de construction, fourni par le
          langage · `motif` : la raison de l'échec. Les appelants passent soit le
          texte `chemin absent`, soit le texte `fichier vide`, soit le nom de
          l'erreur rencontrée, par exemple `FileNotFoundError` ou `UnicodeDecodeError`.
        ④ CONDITIONS D'ENTRÉE — Aucune. Le motif n'est ni vérifié ni contraint.
        ⑤ SORTIE — Ne rend rien. Elle pose une valeur sur l'objet.
          [rend: rien]
        ⑥ TRAITEMENT — ① ranger le motif reçu sur l'objet.
        ⑦ UNITÉ — — Un motif d'échec n'est pas une grandeur.
        ⑧ POURQUOI — Il faut ne jamais confondre « inconnu » et « zéro ». Une
          liste vide veut dire « zéro ligne » ; une lecture ratée doit dire « je
          n'ai pas pu lire ». Tant que les deux partagent la même valeur, aucun
          garde-fou ne peut les distinguer, et un fichier de cours illisible donne
          « séances 0, valeurs 0 » sans une seule alerte. Ce besoin est consigné
          au backlog sous l'identifiant A-226.
        ⑨ CE QUI CLOCHE —
          ① L'objet ne retient pas QUEL fichier n'a pas pu être lu. Le motif seul
          est gardé. C'est l'appelant qui doit se souvenir du nom de la source et
          le joindre à l'alerte ; s'il l'oublie, l'alerte dit « OSError » sans dire
          sur quoi. La classe du même nom de programmes/COMMUN.py, ligne 687,
          prend un second paramètre `chemin` : deux implémentations d'une même
          chose divergent toujours (R-708).
        ⑩ EFFET — Pose une valeur sur l'objet en construction. Ne lit ni n'écrit
          aucun fichier, n'affiche rien, ne touche pas au réseau.
        ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses
          appels ne se termine.
          [sort: non]
        ⑫ DÉFINITIONS
  le zero silencieux : un chiffre affiche a zero parce que la lecture a rate,
    et que rien ne distingue ce ratage d'un vrai zero
  le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui dit
    ou en est le projet, ce qu'il contient et ce qui cloche
  le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions et des actions du projet
        
  la raison : le texte court qui dit pourquoi une lecture a échoué, retenu sous le nom `motif`
  un motif : un morceau de nom passé à une fonction de recherche, par exemple trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
  une lecture ratée : un objet de la classe `Illisible`, rendu à la place des données quand la lecture n'a pas pu se faire, et qui porte sa raison
  une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
        self.motif = motif
    def __len__(self):
        """Rend zéro, pour que l'objet se compte comme un vide.

        ① RÔLE — Permettre à un objet qui dit « je n'ai pas pu lire » de traverser
          sans tomber tout le code écrit pour une liste. C'est ce qui autorise le
          programme à porter l'information « illisible » jusqu'à l'alerte, au lieu
          de s'arrêter à la lecture.
        ② CONTEXTE D'APPEL — Le langage lui-même, chaque fois qu'on demande la
          longueur d'un objet `Illisible` ou qu'on le parcourt. Jamais appelée par
          son nom.
        ③ ENTRÉE — `self` : l'objet, fourni par le langage.
        ④ CONDITIONS D'ENTRÉE — Aucune.
        ⑤ SORTIE — UNE valeur : le nombre zéro, toujours.
          [rend: 1]
        ⑥ TRAITEMENT — ① rendre zéro.
        ⑦ UNITÉ — Un NOMBRE DE LIGNES, et il vaut toujours zéro.
        ⑧ POURQUOI — L'objet doit se comporter comme un vide MAIS se reconnaître.
          S'il levait à la moindre question, il faudrait l'entourer de précautions
          partout ; s'il ressemblait à une vraie liste vide sans se distinguer, il
          ne servirait à rien. Se compter comme zéro et se reconnaître par son type
          est le seul arrangement qui laisse le programme continuer sans effacer
          l'information.
        ⑨ CE QUI CLOCHE —
          ① Rendre zéro rend l'objet indistinguable d'un vide pour tout code qui
          ne demande pas son type. Un appelant qui écrit « s'il n'y a pas de
          lignes, alors zéro séance » obtient exactement le zéro silencieux que
          cette classe existe pour supprimer. Ce fichier s'en protège en demandant
          le type à chaque source, mais rien ne l'y oblige, et un oubli ne
          s'afficherait pas.
        ⑩ EFFET — Aucun. Elle ne lit ni n'écrit aucun fichier, n'affiche rien et ne
          touche pas au réseau.
        ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses
          appels ne se termine.
          [sort: non]
        ⑫ DÉFINITIONS
  le zero silencieux : un chiffre affiche a zero parce que la lecture a rate,
    et que rien ne distingue ce ratage d'un vrai zero
        
  le zéro silencieux : un programme qui rend zéro là où il aurait dû dire qu'il n'a pas pu lire, sans rien afficher
  une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
        return 0
    def __iter__(self):
        """Rend un parcours vide, pour que l'objet se traverse sans rien donner.

        ① RÔLE — Laisser passer sans tomber le code qui parcourt les lignes d'un
          fichier. C'est le pendant du comptage à zéro : l'objet doit se comporter
          comme un vide de bout en bout, sinon la première boucle rencontrée
          arrêterait le programme.
        ② CONTEXTE D'APPEL — Le langage lui-même, chaque fois qu'un objet
          `Illisible` est parcouru par une boucle ou changé en liste. Jamais
          appelée par son nom.
        ③ ENTRÉE — `self` : l'objet, fourni par le langage.
        ④ CONDITIONS D'ENTRÉE — Aucune.
        ⑤ SORTIE — UNE valeur : un parcours sur une suite vide, qui ne rend jamais
          aucun élément.
          [rend: 1]
        ⑥ TRAITEMENT — ① rendre le parcours d'une suite vide.
        ⑦ UNITÉ — — Un parcours n'est pas une grandeur.
        ⑧ POURQUOI — Le motif de l'échec est conservé dans l'objet, mais il ne doit
          jamais sortir par le parcours : une boucle qui recevrait le texte
          `FileNotFoundError` comme s'il s'agissait d'une ligne de données
          fabriquerait un chiffre faux à partir d'un message d'erreur. Rendre un
          parcours vide est la seule réponse qui ne mente pas.
        ⑨ CE QUI CLOCHE — Rien vu.
        ⑩ EFFET — Aucun. Elle ne lit ni n'écrit aucun fichier, n'affiche rien et ne
          touche pas au réseau.
        ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses
          appels ne se termine.
          [sort: non]
        ⑫ DÉFINITIONS
  le zero silencieux : un chiffre affiche a zero parce que la lecture a rate,
    et que rien ne distingue ce ratage d'un vrai zero
        
  une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
        return iter(())
    def __bool__(self):
        """Rend faux, pour que l'objet se teste comme un vide.

        ① RÔLE — Faire qu'un « je n'ai pas pu lire » réponde faux aux questions de
          la forme « est-ce qu'il y a quelque chose ? ». Sans cela, l'objet
          répondrait vrai par défaut et un fichier illisible passerait pour un
          fichier plein.
        ② CONTEXTE D'APPEL — Le langage lui-même, chaque fois qu'un objet
          `Illisible` est employé comme condition. Deux endroits de ce fichier s'en
          servent directement : `main`, qui demande si le pilote de la veille a été
          lu avant de chercher une régression, et `main` de nouveau, qui demande si
          le socle a été lu avant de l'écrire. Jamais appelée par son nom.
        ③ ENTRÉE — `self` : l'objet, fourni par le langage.
        ④ CONDITIONS D'ENTRÉE — Aucune.
        ⑤ SORTIE — UNE valeur : faux, toujours.
          [rend: 1]
        ⑥ TRAITEMENT — ① rendre faux.
        ⑦ UNITÉ — — Une réponse par oui ou par non n'est pas une grandeur.
        ⑧ POURQUOI — Sans cette méthode, le langage se rabat sur le comptage à
          zéro, ce qui donnerait la même réponse ; elle est écrite quand même pour
          que la réponse soit une DÉCISION du programme et non un effet de bord
          d'une autre méthode. Le jour où le comptage changerait, le test de
          présence ne suivrait pas en silence.
        ⑨ CE QUI CLOCHE —
          ① Répondre faux mélange deux cas dans `main` : « le pilote de la veille
          n'a pas pu être lu » et « il n'existe pas encore ». Dans les deux cas, le
          contrôle de régression est sauté sans un mot. Mesuré le 19-09-2026 : une
          fabrication vers un fichier de sortie neuf ne produit aucune alerte de
          régression, ce qui est juste, mais une fabrication vers un pilote
          existant devenu illisible n'en produirait pas davantage, ce qui ne l'est
          pas.
        ⑩ EFFET — Aucun. Elle ne lit ni n'écrit aucun fichier, n'affiche rien et ne
          touche pas au réseau.
        ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses
          appels ne se termine.
          [sort: non]
        ⑫ DÉFINITIONS
  le zero silencieux : un chiffre affiche a zero parce que la lecture a rate,
    et que rien ne distingue ce ratage d'un vrai zero
  le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui dit
    ou en est le projet, ce qu'il contient et ce qui cloche
  le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté ailleurs.
  le controle de regression : la comparaison du pilote en cours de fabrication
    avec celui de la veille, un element disparu etant tenu pour une perte
        
  une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
        return False


def _date_du_nom(n):
    """Rend la date portée dans le nom, au format triable. None si absente.

    ① RÔLE — Permettre de classer par date des fichiers dont seul le nom porte
      l'information. Elle sert à désigner LE fichier de chiffres figés qui fait
      foi quand plusieurs coexistent, en retenant le plus récent et jamais le
      premier par ordre alphabétique.
    ② CONTEXTE D'APPEL — `compter`, et elle seule, trois fois de suite : pour
      repérer les fichiers de chiffres figés dont le nom ne porte aucune date,
      pour écarter ceux-là du classement, puis pour classer les autres. Aucun
      appel hors de ce fichier.
    ③ ENTRÉE — `n` : le chemin d'un fichier. L'appelant passe des chemins de
      fichiers de chiffres figés, par exemple
      `gouvernance/golden_tests_Sam_01-08-2026_20h19.json`, le seul présent au
      dépôt le 19-09-2026.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un chemin vide ou sans date ne la fait pas
      tomber.
    ⑤ SORTIE — UNE valeur : la date réécrite année, mois, jour, ou « rien » quand
      le nom n'en porte pas. Mesuré le 19-09-2026 :
      `golden_tests_Sam_01-08-2026_20h19.json` rend `2026-08-01`.
      [rend: 1]
    ⑥ TRAITEMENT — ① ne garder que le nom du fichier, sans son dossier · ② y
      chercher deux chiffres, un tiret, deux chiffres, un tiret, quatre chiffres ·
      ③ réécrire les trois morceaux dans l'ordre année, mois, jour · ④ rendre
      « rien » si rien n'a été trouvé.
    ⑦ UNITÉ — Une DATE de calendrier, sans heure ni fuseau, écrite année, mois,
      jour pour que deux dates se classent dans l'ordre du calendrier quand on les
      compare lettre à lettre.
    ⑧ POURQUOI — Le classement des fichiers de chiffres figés ne peut pas se faire
      par ordre alphabétique de leur nom. La règle R-701 du registre nomme
      `golden_tests_Sam_01-08-2026_20h19.json` comme référence en vigueur et
      interdit de détruire l'ancien fichier du 12-07 ; le jour où celui-ci
      reviendrait au dépôt, un tri alphabétique le placerait AVANT celui du 01-08
      et le pilote annoncerait 85 opérations au lieu de 100, sans un mot.
      La date est réécrite année, mois, jour parce que c'est la seule écriture où
      comparer deux textes revient à comparer deux dates.
    ⑨ CE QUI CLOCHE —
      ① L'ordre des trois nombres est supposé, jamais vérifié. Le motif accepte
      deux chiffres, deux chiffres, quatre chiffres, et décide que c'est jour,
      mois, année. Un fichier nommé `golden_tests_08-01-2026.json` serait lu comme
      le 8 janvier, qu'il s'agisse du 8 janvier ou du 1er août, et rien ne
      permettrait de le savoir.
      ② Une date écrite année, mois, jour dans le nom n'est pas vue. Le motif exige
      quatre chiffres à la FIN ; `golden_tests_2026-08-01.json` ne rapproche rien
      et rend « rien ». Le fichier est alors rangé parmi ceux qui sont impossibles
      à classer, et signalé — ce qui est le bon comportement, mais pour une
      mauvaise raison.
      ③ Elle prend la PREMIÈRE date du nom. Un nom qui en porterait deux, par
      exemple une version et une date de prise, rendrait la première rencontrée
      sans que rien ne signale l'ambiguïté.
    ⑩ EFFET — Aucun. Elle ne lit aucun fichier — elle ne regarde que le texte du
      chemin —, n'en écrit aucun, n'affiche rien et ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels
      ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
  les chiffres figes : gouvernance/golden_tests_*.json, les resultats de
    reference qu'un calcul juste doit retrouver au centime pres
  le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui dit
    ou en est le projet, ce qu'il contient et ce qui cloche
  le registre : gouvernance/REGISTRE_REGLES.md, le document qui porte les regles
    numerotees du projet ; une regle absente du registre n'existe pas
  le depot : le depot GitHub ou vivent les fichiers du systeme, le projet n'en
    etant qu'une copie de lecture
    
  une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    m = re.search(r"(\d{2})-(\d{2})-(\d{4})", os.path.basename(n))
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else None


def lire(ch):
    """Rend le texte entier d'un fichier, ou un objet qui dit pourquoi il a échoué.

    ① RÔLE — Être le seul endroit où ce programme ouvre un fichier en texte, et
      faire qu'un échec de lecture ne se confonde jamais avec un fichier vide. Le
      registre, le backlog, l'audit du soir, le socle et le pilote de la veille
      passent tous par ici.
    ② CONTEXTE D'APPEL — Deux appelants, tous deux dans ce fichier. ① `compter`,
      quatre fois : le registre, le backlog, l'audit du soir, et une cinquième
      lecture de l'audit pour y chercher la place du projet. ② `controler`, deux
      fois, pour relire le backlog et le registre. ③ `main`, deux fois : le socle,
      puis le pilote de la veille. Aucun appel hors de ce fichier.
    ③ ENTRÉE — `ch` : le chemin du fichier à lire, ou « rien » quand la recherche
      n'a rien trouvé. Les appelants passent sans le modifier ce que `trouver` leur
      a rendu, par exemple `gouvernance/REGISTRE_REGLES.md`, et `main` passe en
      plus le chemin de sortie du pilote.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un chemin vide, inexistant ou illisible ne la
      fait pas tomber.
    ⑤ SORTIE — UNE valeur, de deux natures différentes. Le texte entier du fichier
      quand la lecture réussit. Sinon, un objet qui se compte comme vide, se teste
      comme faux, et porte la raison de l'échec — `chemin absent` quand aucun
      chemin n'a été donné, ou le nom de l'erreur rencontrée.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre un objet « illisible » si aucun chemin n'a été
      donné · ② ouvrir le fichier en UTF-8, en remplaçant les octets
      indéchiffrables au lieu de s'arrêter · ③ rendre son texte entier · ④ rendre
      un objet « illisible » portant le nom de l'erreur si l'ouverture a échoué.
    ⑦ UNITÉ — Un TEXTE, en caractères. Le fichier le plus gros lu par cette
      fonction est le registre des règles.
    ⑧ POURQUOI — Les octets indéchiffrables sont remplacés plutôt que de faire
      échouer la lecture, parce qu'un seul caractère abîmé au milieu d'un registre
      de mille deux cents lignes ne doit pas faire disparaître du pilote le nombre
      de règles, la version et la performance de référence.
      L'objet rendu en cas d'échec se comporte comme un vide MAIS se reconnaît, et
      c'est tout l'objet de la manœuvre : une liste vide veut dire « zéro ligne »,
      une lecture ratée doit dire « je n'ai pas pu lire ». Tant que les deux
      partagent la même valeur, aucun garde-fou ne peut les distinguer.
    ⑨ CE QUI CLOCHE —
      ① Un fichier abîmé se lit sans un mot. Le remplacement des octets
      indéchiffrables n'est signalé nulle part : le texte rendu passe pour intact,
      et un motif qui ne rapproche plus rien sera lu comme « la règle n'est pas
      là » plutôt que comme « la ligne est abîmée ».
      ② Un dossier n'est pas distingué d'un fichier. Passer le chemin d'un dossier
      fait lever une erreur système, qui est rattrapée et rendue sous forme
      d'objet « illisible » portant le nom de l'erreur — une réponse juste, mais
      qui ne dit pas que le chemin désignait autre chose qu'un fichier.
      ③ Le fichier n'est jamais refermé explicitement. Il l'est par le ramassage
      automatique du langage, ce qui suffit ici où une dizaine de lectures ont
      lieu, mais la même écriture dans une boucle sur deux cents fichiers
      épuiserait les descripteurs ouverts.
    ⑩ EFFET — LIT le fichier nommé, en entier et en mémoire. N'écrit rien,
      n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main, par l'un de ses trois points de sortie.
      Elle ne lève pas pour les trois familles d'erreurs rattrapées. Aucun de ses
      appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
  le zero silencieux : un chiffre affiche a zero parce que la lecture a rate,
    et que rien ne distingue ce ratage d'un vrai zero
  le registre : gouvernance/REGISTRE_REGLES.md, le document qui porte les regles
    numerotees du projet ; une regle absente du registre n'existe pas
  le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions et des actions du projet
  le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté ailleurs.
  le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui dit
    ou en est le projet, ce qu'il contient et ce qui cloche
  l'audit du soir : programmes/audit_ecosysteme.py, lance chaque soir par la
    tache planifiee, qui ecrit rapports/audit_du_jour.md
    
  la raison : le texte court qui dit pourquoi une lecture a échoué, retenu sous le nom `motif`
  un motif : un morceau de nom passé à une fonction de recherche, par exemple trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
  une lecture ratée : un objet de la classe `Illisible`, rendu à la place des données quand la lecture n'a pas pu se faire, et qui porte sa raison
  une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if not ch:
        return Illisible("chemin absent")
    try:
        return open(ch, encoding="utf-8", errors="replace").read()
    except (OSError, TypeError, ValueError) as e:
        return Illisible(type(e).__name__)


def lignes_csv(ch):
    """Rend les lignes d'un fichier à colonnes, ou un objet qui dit pourquoi il a échoué.

    ① RÔLE — Être le seul endroit où ce programme lit un fichier à colonnes, et
      faire qu'un échec de lecture ne se confonde jamais avec un fichier sans
      ligne. Les cours, l'état civil des stratégies, les positions ouvertes et le
      journal des trades passent tous par ici.
    ② CONTEXTE D'APPEL — `compter`, et elle seule, treize fois par fabrication :
      chaque source à colonnes est lue une fois pour savoir si elle est lisible,
      puis une seconde fois pour ses lignes. Aucun appel hors de ce fichier.
    ③ ENTRÉE — `ch` : le chemin du fichier à lire, ou « rien » quand la recherche
      n'a rien trouvé. L'appelant passe sans le modifier ce que `trouver` lui a
      rendu, par exemple `donnees/cac40_ohlcv.csv`, qui portait 25 116 lignes le
      19-09-2026.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un chemin vide, inexistant ou illisible ne la
      fait pas tomber. Le fichier doit porter une première ligne de noms de
      colonnes : c'est elle qui donne leurs clés aux lignes rendues.
    ⑤ SORTIE — UNE valeur, de deux natures différentes. La liste des lignes, chaque
      ligne étant un tableau qui associe à chaque nom de colonne sa valeur, quand
      la lecture réussit. Sinon, un objet qui se compte comme vide, se teste comme
      faux, et porte la raison de l'échec — `chemin absent`, `fichier vide`, ou le
      nom de l'erreur rencontrée.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre un objet « illisible » si aucun chemin n'a été donné ·
      ② ouvrir le fichier en UTF-8 en retirant la marque d'ordre des octets que
      certains tableurs posent en tête · ③ lire toutes les lignes · ④ rendre un
      objet « illisible » si la lecture a échoué · ⑤ rendre un objet « illisible »
      si aucune ligne n'a été lue ET que le fichier fait moins de quatre octets ·
      ⑥ rendre la liste des lignes.
    ⑦ UNITÉ — Un NOMBRE DE LIGNES. Les valeurs de chaque ligne restent des textes :
      cette fonction ne convertit rien.
    ⑧ POURQUOI — La marque d'ordre des octets est retirée à la lecture parce qu'un
      tableur qui enregistre un fichier à colonnes la pose en tête, et que le nom
      de la première colonne porterait alors ces octets invisibles devant lui : le
      programme chercherait la colonne `valeur`, le fichier en porterait une dont
      le nom commence par trois octets qu'on ne voit pas, et le rapprochement
      échouerait sans qu'aucune erreur ne s'affiche.
      Les erreurs sont rendues sous forme d'objet plutôt que levées, parce que
      l'appelant a besoin de NOMMER la source fautive : le pilote écrit « SOURCE
      ILLISIBLE : les cours — OSError », et c'est le nom de la source qui permet de
      comprendre. Une levée l'aurait perdu.
    ⑨ CE QUI CLOCHE —
      ① Le zéro silencieux reste ouvert sur les cours. Un fichier ne vaut
      « illisible » que s'il ne rend aucune ligne ET qu'il fait moins de quatre
      octets. Un fichier réduit à sa seule ligne de noms de colonnes en fait
      davantage et passe pour lisible. Mesuré le 19-09-2026 sur une copie : un
      `donnees/cac40_ohlcv.csv` réduit à sa ligne d'en-tête de 38 octets fait
      afficher au pilote « séances 0 · valeurs 0 · dernière séance ? », et aucune
      des six alertes produites ce jour-là ne parle des cours. C'est exactement le
      cas que la classe « illisible » a été écrite pour supprimer, et il survit
      dans la fonction qui s'en sert.
      ② Le seuil de quatre octets est un nombre écrit en dur, sans rapport avec ce
      qu'il mesure. Un garde-fou porte sur une propriété, jamais sur un compte : la
      propriété qui tranche ici serait « le fichier porte une ligne de noms de
      colonnes et au moins une ligne de données ».
      ③ Le fichier est lu en entier en mémoire à chaque appel, et chaque source est
      lue deux fois — une fois pour savoir si elle est lisible, une fois pour ses
      lignes. Mesuré le 19-09-2026 : deux lectures de `donnees/cac40_ohlcv.csv`
      prennent 0,11 seconde pour 25 116 lignes, ce qui ne gêne pas aujourd'hui,
      mais le résultat de la première lecture est jeté sans être employé.
      ④ Une ligne plus courte ou plus longue que l'en-tête est acceptée en silence.
      Les colonnes manquantes valent « rien » et les colonnes en trop sont rangées
      à part sous une clé unique. Aucun contrôle ne compare les champs lus aux
      champs déclarés, alors que programmes/CONTRATS_DES_FICHIERS.py existe pour
      cela.
    ⑩ EFFET — LIT le fichier nommé, en entier et en mémoire, et demande sa taille
      au système. N'écrit rien, n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main, par l'un de ses quatre points de sortie.
      Elle PEUT LEVER si le fichier disparaît entre la lecture et la demande de
      taille, ce cas n'étant pas rattrapé. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
  le zero silencieux : un chiffre affiche a zero parce que la lecture a rate,
    et que rien ne distingue ce ratage d'un vrai zero
  une seance : une journee de bourse pour une valeur, avec son ouverture, son
    plus haut, son plus bas, sa cloture et son volume
  l'etat civil des strategies : donnees/cac40_strategies.csv, la liste des
    strategies avec pour chacune son etat de vie, son compteur et son univers
  le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui dit
    ou en est le projet, ce qu'il contient et ce qui cloche
    
  la marque d'ordre des octets : trois octets invisibles que certains tableurs posent en tête d'un fichier et qui, s'ils ne sont pas écartés, se collent au nom de la première colonne
  la raison : le texte court qui dit pourquoi une lecture a échoué, retenu sous le nom `motif`
  le rapprochement : le fait de reconnaître que deux écritures différentes désignent le même fichier ou la même entreprise
  le zéro silencieux : un programme qui rend zéro là où il aurait dû dire qu'il n'a pas pu lire, sans rien afficher
  un garde-fou : une limite qui, franchie, fait cesser a la strategie de prendre position tout en continuant a la mesurer.
  une clé : le texte obtenu après rapprochement, qui sert à comparer deux noms et n'est jamais affiché à un lecteur
"""
    if not ch:
        return Illisible("chemin absent")
    try:
        r = list(csv.DictReader(open(ch, encoding="utf-8-sig")))
    except (OSError, TypeError, csv.Error, ValueError) as e:
        return Illisible(type(e).__name__)
    if not r and os.path.getsize(ch) < 4:
        return Illisible("fichier vide")
    return r


# ─────────────────────────────────────────────────────────────────────
# COMPTER — jamais un nombre écrit en dur
# ─────────────────────────────────────────────────────────────────────

def compter(base):
    """Relève sur les sources tous les chiffres du tableau du pilote.

    ① RÔLE — Établir, par lecture des fichiers eux-mêmes, la quinzaine de chiffres
      qui disent où en est le projet : combien de règles, combien d'actions,
      combien de séances, quelles stratégies vivantes, quelle dernière opération
      close, quels chiffres de référence. Ce qui se calcule ne s'écrit jamais à la
      main (R-728), et cette fonction est l'endroit où cette règle s'applique pour
      le pilote. Elle relève aussi, et c'est aussi important, ce qu'elle n'a PAS pu
      lire : une source introuvable, illisible ou ambiguë est rangée à part pour
      être signalée.
    ② CONTEXTE D'APPEL — `main`, une seule fois par fabrication, avant le relevé
      des rôles et avant la composition du texte. Aucun appel hors de ce fichier :
      relevé le 19-09-2026 par recherche du nom dans programmes/ et dans
      .github/workflows/.
    ③ ENTRÉE — `base` : la racine à lire. Un seul appelant, `main`, qui transmet
      sans le modifier le premier argument de la ligne de commande, ou
      `/mnt/project` quand aucun n'est donné.
    ④ CONDITIONS D'ENTRÉE — Aucune source n'est obligatoire : chacune qui manque
      est rangée dans la liste des sources muettes au lieu de faire tomber la
      fonction. La racine doit se parcourir.
    ⑤ SORTIE — DEUX valeurs. ① un tableau des chiffres relevés, dont les clés
      portent le libellé exact affiché au pilote, plus quatre clés de service
      commençant par un tiret bas : les stratégies vivantes détaillées, les sources
      illisibles, les sources ambiguës et les sources introuvables. ② un tableau
      qui dit, pour chaque source, le NOM du fichier réellement lu.
      **Selon la branche, elle rend 1 ou 2 valeur(s).**
      [rend: 2]
⑥ TRAITEMENT — ① lire le registre : compter les règles R et les règles I,
      relever la version et la performance de référence · ② lire le backlog :
      relever le nombre d'actions annoncé par le tampon et compter les lignes du
      tableau · ③ lire les cours : compter les séances, les valeurs, la première et
      la dernière, et les séances dont le compte de valeurs s'écarte du compte le
      plus fréquent · ④ lire l'état civil des stratégies : compter les vivantes et
      relever pour chacune son état, son compteur et son univers · ⑤ compter les
      positions ouvertes, en regroupant les lignes par valeur et date d'entrée ·
      ⑥ compter les fiches du sas et celles dont les cinq champs obligatoires sont
      remplis · ⑦ dresser la liste des sources introuvables · ⑧ choisir le fichier
      de chiffres figés le plus récent et en tirer le test de balance · ⑨ lire le
      journal des trades et retenir l'opération dont la date de sortie est la plus
      tardive · ⑩ lire l'audit du soir et y chercher la place du projet · ⑪ compter
      les fichiers et les octets.
    ⑦ UNITÉ — Des NOMBRES DE RÈGLES, d'actions, de lignes, de séances, de valeurs,
      de fiches et de fichiers. Deux exceptions : les octets du projet, et les
      euros du test de balance et de la performance de référence.
    ⑧ POURQUOI — Aucun chiffre n'est écrit dans ce programme, et c'est la règle qui
      commande tout le reste. La ligne « performance de référence » était autrefois
      un nombre écrit en dur ici, précédé d'un repli sur une clé de chiffres figés
      qui n'existait pas — le repli s'appliquait donc toujours. Le chiffre était
      juste le 27-08-2026 et le serait resté indéfiniment : le jour où la
      performance change, le pilote aurait affiché celle du 23-08 sans un mot.
      Elle est désormais lue dans la règle R-722, qui la définit et qui porte, au
      registre relevé le 19-09-2026, « la PERFORMANCE DE RÉFÉRENCE devient
      89 opérations · 58,43 % · +939,71 EUR par trade · +83 634,24 EUR ». Si cette
      règle manque ou devient illisible, la ligne n'est PAS affichée et le fait est
      signalé, jamais remplacée par une valeur de secours.
      Les règles sont comptées par IDENTIFIANT et non par forme d'écriture. Le
      08-09-2026, le motif employé n'acceptait que les règles écrites en liste,
      sous la forme `- **R-NNN**` ; les six règles écrites en titre, `### R-731` à
      `### R-735`, étaient invisibles. Le même défaut cachait les onze règles du
      chapitre sur l'identité des valeurs, toutes écrites `### I-N —` : un chapitre
      entier de la loi ne comptait pas. Et l'on compte les identifiants UNIQUES,
      jamais les occurrences : une règle citée deux fois ne fait pas deux règles.
      Une position n'est pas une ligne. Le fichier des positions porte une ligne
      par couple stratégie et comptabilité : quatre lignes pour une seule position
      tenue sur deux stratégies. Compter les lignes ferait croire que la règle
      R-605, qui interdit plus d'une position à la fois en comptabilité « un
      jeton », est enfreinte alors qu'elle ne l'est pas.
      Le fichier de chiffres figés retenu est le plus RÉCENT, jamais le premier par
      ordre alphabétique : la règle R-701 interdit de détruire l'ancien fichier du
      12-07, et le jour où il reviendrait au dépôt un tri alphabétique le placerait
      avant celui du 01-08, faisant annoncer au pilote 85 opérations au lieu de 100.
      La dernière opération close est celle dont la DATE DE SORTIE est la plus
      tardive, jamais la dernière ligne écrite : rien ne garantit que le journal
      soit trié. Les dates sont réécrites année, mois, jour avant le tri, parce
      qu'un tri de textes ne coïncide avec l'ordre du calendrier que dans cette
      écriture-là — par chance, pas par construction. Et la colonne de date de
      sortie est choisie sur un nom EXACT, jamais sur le premier nom qui contient
      le mot « sortie » : l'ordre des colonnes ne doit pas décider à la place d'une
      règle, ce que l'action A-284 du backlog consigne.
    ⑨ CE QUI CLOCHE —
      ① Le nombre d'actions du tampon n'est lu que derrière le mot OK. Mesuré le
      19-09-2026 : le backlog du dépôt porte « CONTRÔLE AUTOMATIQUE : ÉCHEC** —
      413 actions au tableau », le motif ne rapproche rien, et le pilote affiche
      « actions au tampon : ? ». Comme la comparaison avec le nombre de lignes
      exige deux entiers, l'écart réel entre 413 et les 418 lignes comptées n'est
      signalé nulle part. Le jour où le contrôle du backlog échoue est précisément
      celui où ce nombre importe.
      ② RÉGLÉ LE 28-09-2026 (A-435 ①) : la version se lit en pied de page, sur la
      dernière ligne qui porte le titre du registre suivi de « vN.N ». Ce qui était mesuré : la version du registre est
      prise sur la ligne qui dit de ne pas la prendre là. Le motif retient le premier « vN.N » des 400 premiers caractères du
      registre. Ces 400 caractères portent l'avertissement « LA VERSION ET LE
      COMPTE DES RÈGLES NE SONT PAS ICI — ILS SE LISENT EN PIED DE PAGE. Corrigé le
      13-09-2026 : cette ligne portait « v4.0 » quand le pied de page portait
      « v4.4 » ». Mesuré le 19-09-2026 : le motif attrape ce « v4.0 » cité comme
      contre-exemple, et le pilote annonce « version du registre : 4.0 » quand le
      pied de page porte « v6.1 · révisé le 19-09-2026 ».
      ③ Cinq chiffres sont comptés et jamais affichés. Mesuré le 19-09-2026 sur une
      copie du dépôt : « règles I » vaut 11, « lignes de tableau » 418, « lignes de
      positions » 0, « octets du projet » 10 703 473, et « première séance » est
      aussi calculée. Aucun des cinq n'est dans la liste qui fixe l'ordre du
      tableau du pilote, donc aucun n'est écrit. Le commentaire qui accompagne le
      comptage des règles I explique qu'un chapitre entier de la loi était
      invisible ; il l'est toujours, pour une autre raison.
      ④ La place du projet a disparu du tableau sans un mot. Le lecteur accepte
      deux écritures, « PLACE PROJET : NN,NN % » et « Place RÉELLE ». Mesuré le
      19-09-2026 : rapports/audit_du_jour.md n'en porte aucune, la clé n'est pas
      posée, et la ligne manque au pilote sans qu'aucune alerte ne le dise. C'est
      le même défaut qu'en août, quand l'audit avait changé de libellé — et à
      l'époque seul le contrôle de régression l'avait vu.
      ⑤ Le compteur d'une stratégie est choisi par l'ordre des colonnes. La
      fonction imbriquée qui le cherche retient la première colonne dont le nom
      contient « compteur » OU dont la valeur contient « /50 ». Le nombre 50 est
      écrit en dur : une stratégie dont le compteur irait jusqu'à 30 ne serait pas
      reconnue par cette seconde condition. Et si deux colonnes conviennent, c'est
      l'ordre du fichier qui tranche — le défaut même que l'action A-284 interdit,
      dans la fonction dont un commentaire voisin cite cette action.
      ⑥ Un statut de position absent vaut « ouverte ». Une ligne sans colonne de
      statut est comptée comme une position en cours. Un fichier de positions dont
      la colonne aurait changé de nom ferait donc annoncer des positions ouvertes
      qui n'existent pas, sans un mot.
      ⑦ Le test de balance est cherché dans la première stratégie du fichier de
      chiffres figés qui en porte un, puis la recherche s'arrête. Mesuré le
      19-09-2026 : `gouvernance/golden_tests_Sam_01-08-2026_20h19.json` ne porte
      qu'une stratégie, `C5-ETENDU-10`. Le jour où il en porterait deux, le pilote
      afficherait celle qui vient en premier sans dire laquelle, ni qu'il y en
      avait une autre.
      ⑧ Le module `json` est chargé À L'INTÉRIEUR du bloc protégé, et le nom
      `json.JSONDecodeError` est employé dans la liste des erreurs rattrapées. Si
      ce chargement échouait, la liste des erreurs ferait elle-même lever une
      erreur de nom inconnu, et le programme s'arrêterait à l'endroit prévu pour
      ne pas s'arrêter.
      ⑨ Le fichier de chiffres figés illisible n'est pas signalé. Toutes les
      erreurs de son bloc sont rattrapées et abandonnées sans rien ajouter aux
      listes de service : la ligne « test de balance » disparaît alors du tableau
      en silence, alors que les cinq autres sources ont droit à une alerte.
      ⑩ Chaque source à colonnes est lue deux fois, et le résultat de la première
      lecture est jeté. Mesuré le 19-09-2026 : deux lectures de
      `donnees/cac40_ohlcv.csv` prennent 0,11 seconde pour 25 116 lignes.
      ⑪ La ligne qui suit la lecture des chiffres figés est un `pass` que rien
      n'atteint. Il ne fait rien de mal, mais il laisse croire qu'une branche a été
      retirée sans que son texte le dise.
    ⑩ EFFET — LIT dix fichiers de sources — registre, backlog, cours, état civil
      des stratégies, positions ouvertes, chiffres figés, journal des trades et
      audit du soir — et PARCOURT l'arborescence entière plusieurs fois. N'écrit
      AUCUN fichier, n'affiche rien, ne touche pas au réseau, et ne modifie aucune
      source.
    ⑪ TERMINAISON — Rend toujours la main. Elle PEUT LEVER par ses appels :
      `trouver` lève sur un dossier existant mais illisible, et la demande de
      taille de chaque fichier lève si le fichier disparaît en cours de parcours.
        [sort: non]
    ⑫ DÉFINITIONS
  le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui dit
    ou en est le projet, ce qu'il contient et ce qui cloche
  le registre : gouvernance/REGISTRE_REGLES.md, le document qui porte les regles
    numerotees du projet ; une regle absente du registre n'existe pas
  le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions et des actions du projet
  le tampon : la ligne d'horodatage posee en tete du backlog par
    programmes/verif_backlog.py, qui annonce elle-meme un nombre d'actions
  les chiffres figes : gouvernance/golden_tests_*.json, les resultats de
    reference qu'un calcul juste doit retrouver au centime pres
  l'etat civil des strategies : donnees/cac40_strategies.csv, la liste des
    strategies avec pour chacune son etat de vie, son compteur et son univers
  le sas : les fiches de strategie en etat LABO a l'etat civil, celles qui
    attendent d'etre jugees par le juge des stratégies
  une seance : une journee de bourse pour une valeur, avec son ouverture, son
    plus haut, son plus bas, sa cloture et son volume
  l'audit du soir : programmes/audit_ecosysteme.py, lance chaque soir par la
    tache planifiee, qui ecrit rapports/audit_du_jour.md
  le depot : le depot GitHub ou vivent les fichiers du systeme, le projet n'en
    etant qu'une copie de lecture
  le zero silencieux : un chiffre affiche a zero parce que la lecture a rate,
    et que rien ne distingue ce ratage d'un vrai zero
    
  C5-ETENDU-10 : le nom de la stratégie vivante ; ses seuils et son horizon sont lus dans `donnees/cac40_strategies.csv`.
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
  une clé : le texte obtenu après rapprochement, qui sert à comparer deux noms et n'est jamais affiché à un lecteur
  une stratégie : une règle qui dit QUOI acheter, avec son objectif de gain, sa perte acceptée et son horizon
"""
    c, src = {}, {}

    ch = trouver(base, "REGISTRE_REGLES")
    # D'OÙ VIENT LE REGISTRE LU — relevé, jamais deviné (09-09-2026).
    # Le PILOTE est le document que le rituel fait lire en début de session : s'il
    # annonce une version du registre, il doit dire s'il l'a lue au dépôt ou sur la
    # copie de repli du projet. Sans cela, un clone échoué passerait inaperçu.
    _p_reg, _org_reg = _registre_et_origine()
    c["origine du registre"] = _org_reg if _org_reg else (
        "repli projet" if ch else "INTROUVABLE")
    if ch:
        t = lire(ch)
        if isinstance(t, Illisible):
            c.setdefault("_illisibles", []).append(("le registre", t.motif))
            t = ""
        # MOTIF PAR IDENTIFIANT, JAMAIS PAR FORME D'ECRITURE (R-720). Corrige le 08-09-2026 :
        # l'ancien motif ^- **R-NNN** ne voyait pas les regles ecrites en titre "### R-NNN",
        # soit 6 regles sur 100 invisibles (R-731 a R-735). On compte les UNIQUES, jamais
        # les occurrences : une regle citee deux fois ne fait pas deux regles.
        c["règles R"] = len({m.group(1) for m in re.finditer(
            r"^(?:[-*+]\s+|#{1,6}\s+)\*{0,2}\s*(R-\d+\w*)\b", t, re.M)})
        # MEME DEFAUT, MEME REMEDE, mesure du 08-09-2026 : les ONZE regles du chapitre
        # GESTION DE L'IDENTITE DES VALEURS sont TOUTES ecrites "### I-N —". L'ancien motif
        # en comptait ZERO, et un chapitre entier de la loi etait invisible au pilote.
        c["règles I"] = len({m.group(1) for m in re.finditer(
            r"^(?:[-*+]\s+|#{1,6}\s+)\*{0,2}\s*(I-\d+\w*)\b", t, re.M)})
        # LA VERSION SE LIT EN PIED DE PAGE, comme le registre le dit en tête (A-435 ①,
        # 28-09-2026). Les 400 premiers caractères portaient l'avertissement lui-même,
        # qui cite « v4.0 » comme contre-exemple : le pilote annonçait 4.0 pour un
        # registre en v6.8. LE PIED DE PAGE EST LA DERNIÈRE LIGNE QUI PORTE LE TITRE DU
        # REGISTRE SUIVI DE SA VERSION — pas simplement la dernière ligne : une ligne de
        # contrôle du garde-fou (<!-- CONTROLE … -->) ou une annexe posée après lui
        # faisaient annoncer « ? » ou une version citée (relecteur du Chat, 28-09-2026).
        _pieds = re.findall(r"REGISTRE DES RÈGLES[^\n,]*,\s*v(\d+\.\d+)", t)
        c["version du registre"] = _pieds[-1] if _pieds else "?"
        # LA PERFORMANCE DE RÉFÉRENCE SE LIT DANS R-722, JAMAIS EN DUR.
        # Elle était écrite comme littéral de repli dans ce programme, avec une
        # clé de golden qui n'existe pas — donc le repli s'appliquait TOUJOURS.
        # Le chiffre était juste le 27/08 et l'aurait été indéfiniment : le jour
        # où la performance change, le pilote aurait affiché celle du 23/08 sans
        # un mot. C'est le zéro silencieux, dans le programme qui le combat.
        # R-722 est la règle qui DÉFINIT ces deux nombres : elle fait autorité,
        # et une règle absente du registre n'existe pas.
        r722 = re.search(r"^- \*\*R-722\*\*.*$", t, re.M)
        if r722:
            p = re.search(r"PERFORMANCE DE RÉFÉRENCE\D{0,30}\*\*(.{0,80}?)\*\*",
                          r722.group(0))
            if p:
                c["performance de référence"] = p.group(1).strip() + " (R-722)"
            else:
                c.setdefault("_ambigus", []).append(
                    "R-722 existe mais sa performance de référence n'est pas "
                    "lisible par le motif : elle n'est PAS affichée plutôt "
                    "qu'affichée fausse")
        else:
            c.setdefault("_ambigus", []).append(
                "R-722 introuvable au registre : la performance de référence "
                "MANQUE au pilote. Ce n'est pas zéro, c'est inconnu.")
        src["le registre"] = os.path.basename(ch)

    ch = trouver(base, "BACKLOG_DECISIONS.md")
    if ch:
        t = lire(ch)
        if isinstance(t, Illisible):
            c.setdefault("_illisibles", []).append(("le backlog", t.motif))
            t = ""
        m = re.search(r"OK\*\*\s*—\s*(\d+)\s*actions", t)
        c["actions au tampon"] = int(m.group(1)) if m else "?"
        c["lignes de tableau"] = len(re.findall(r"^\|\s*A-\d+\w*\s*\|", t, re.M))
        src["le backlog"] = os.path.basename(ch)

    ch = trouver(base, "cours_maitre.csv")
    if ch and isinstance(lignes_csv(ch), Illisible):
        c.setdefault("_illisibles", []).append(("les cours", lignes_csv(ch).motif))
        ch = None
    if ch:
        r = lignes_csv(ch)
        d = sorted({x["date"] for x in r if x.get("date")})
        v = {x["valeur"] for x in r if x.get("valeur")}
        c["séances"] = len(d)
        c["valeurs"] = len(v)
        c["première séance"] = d[0] if d else "?"
        c["dernière séance de l'historique figé"] = d[-1] if d else "?"
        par = {}
        for x in r:
            par[x.get("date")] = par.get(x.get("date"), 0) + 1
        ref = max(set(par.values()), key=list(par.values()).count) if par else 0
        c["séances incomplètes"] = sum(1 for n in par.values() if n != ref)
        src["les cours"] = os.path.basename(ch)

    ch = trouver(base, "cac40_strategies.csv")
    if ch and isinstance(lignes_csv(ch), Illisible):
        c.setdefault("_illisibles", []).append(("l'état civil", lignes_csv(ch).motif))
        ch = None
    if ch:
        r = lignes_csv(ch)
        viv = [x for x in r
               if (x.get("etat_vie") or "").strip().upper() in ("QA", "PRODUCTION")]
        c["stratégies vivantes"] = len(viv)
        def _cpt(x):
            """Rend le compteur d'une stratégie, lu dans sa ligne d'état civil.

            ① RÔLE — Retrouver, dans la ligne d'une stratégie, la case qui dit
              combien d'opérations elle a jouées sur le nombre exigé avant tout
              jugement. Ce nombre est affiché au pilote sous chaque stratégie
              vivante.
            ② CONTEXTE D'APPEL — `compter`, une fois par stratégie vivante.
              Mesuré le 19-09-2026 sur une copie du dépôt : deux appels, pour
              `C5E10-QA-V1` et `C5E10-OBS-V1`.
            ③ ENTRÉE — `x` : la ligne d'une stratégie, c'est-à-dire le tableau qui
              associe à chaque nom de colonne sa valeur. L'appelant passe sans la
              modifier une ligne de `donnees/cac40_strategies.csv`, dont l'en-tête
              relevé le 19-09-2026 porte trente-trois colonnes, parmi lesquelles
              `compteur`.
            ④ CONDITIONS D'ENTRÉE — Aucune. Une ligne sans colonne de compteur ne
              la fait pas tomber.
            ⑤ SORTIE — UNE valeur : le texte du compteur, par exemple `1/50`,
              mesuré le 19-09-2026 pour `C5E10-QA-V1` ; ou le texte
              `compteur NON TROUVÉ` quand aucune colonne ne convient.
              [rend: 1]
            ⑥ TRAITEMENT — ① parcourir les colonnes dans l'ordre du fichier ·
              ② retenir la première dont le nom contient `compteur`, majuscules et
              minuscules confondues, ou dont la valeur contient `/50` · ③ rendre sa
              valeur si elle n'est ni vide ni un tiret · ④ rendre
              `compteur NON TROUVÉ`.
            ⑦ UNITÉ — Un NOMBRE D'OPÉRATIONS sur un nombre exigé, écrit en toutes
              lettres comme `1/50`. La fonction ne convertit rien : elle rend du
              texte.
            ⑧ POURQUOI — Un compteur absent est dit, jamais remplacé par un blanc :
              un pilote qui afficherait une case vide laisserait croire à zéro
              opération, alors que la question est « où est la colonne ? ».
            ⑨ CE QUI CLOCHE —
              ① L'ordre des colonnes décide. Si deux colonnes conviennent, c'est
              celle qui vient en premier dans le fichier qui l'emporte, et rien ne
              le signale. C'est le défaut que l'action A-284 du backlog consigne :
              ne jamais laisser l'ordre trancher à la place d'une règle — et un
              commentaire voisin, dans la même fonction hôte, cite cette action à
              propos d'un autre choix de colonne.
              ② Le nombre 50 est écrit en dur dans la seconde condition. Une
              stratégie dont le compteur irait jusqu'à 30 ne serait reconnue que par
              le nom de sa colonne ; si ce nom changeait, le compteur deviendrait
              introuvable sans qu'aucun contrôle ne s'en aperçoive.
              ③ Le tiret long est accepté comme valeur absente, le tiret court ne
              l'est pas. Une ligne portant un tiret ordinaire rendrait ce tiret
              comme s'il s'agissait d'un compteur.
            ⑩ EFFET — Aucun. Elle ne lit aucun fichier, n'en écrit aucun, n'affiche
              rien et ne touche pas au réseau.
            ⑪ TERMINAISON — Rend toujours la main, par l'un de ses deux points de
              sortie. Elle ne lève pas. Aucun de ses appels ne se termine.
              [sort: non]
            ⑫ DÉFINITIONS
  l'etat civil des strategies : donnees/cac40_strategies.csv, la liste des
    strategies avec pour chacune son etat de vie, son compteur et son univers
  le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui dit
    ou en est le projet, ce qu'il contient et ce qui cloche
  le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions et des actions du projet
            
  une stratégie : une règle qui dit QUOI acheter, avec son objectif de gain, sa perte acceptée et son horizon
  une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
            for k in x:
                if "compteur" in k.lower() or "/50" in str(x.get(k) or ""):
                    v = (x.get(k) or "").strip()
                    if v and v != "—":
                        return v
            return "compteur NON TROUVÉ"
        c["_vivantes"] = [(x.get("id", "?"), (x.get("etat_vie") or "").strip(),
                           _cpt(x), (x.get("univers") or "").strip()[:44])
                          for x in viv]
        src["l'état civil"] = os.path.basename(ch)

    ch = trouver(base, "claude_positions_ouvertes.csv", "positions_ouvertes.csv")
    if ch:
        r = lignes_csv(ch)
        if isinstance(r, Illisible):
            c.setdefault("_illisibles", []).append(("les positions", r.motif))
        else:
            # UNE POSITION N'EST PAS UNE LIGNE. Le fichier porte une ligne par
            # (strategie x comptabilite) : quatre lignes pour UNE position tenue
            # sur deux strategies. Compter les lignes ferait croire que R-605
            # est enfreinte, alors qu'elle ne l'est pas.
            ouv = [x for x in r if (x.get("statut") or "OUVERTE").strip().upper()
                   not in ("FERMEE", "FERMÉE", "CLOSE")]
            c["positions ouvertes"] = len({(x.get("valeur"), x.get("date_entree"))
                                           for x in ouv})
            c["lignes de positions"] = len(ouv)
        src["les positions"] = os.path.basename(ch)

    # LE SAS N EXISTE PLUS, ET CE N EST PAS UNE PERTE — A-326, 29-08-2026.
    # `registre_candidates.csv` a ete ABSORBE dans `cac40_strategies.csv` : un seul
    # registre porte desormais l etat civil des strategies. **Les cinq candidates
    # sont au registre, en etat LABO** — C4-RAV-ELARGI, C5-EI-PARAMS,
    # C2-GAP-CONSENSUS, C5E10-SELECTION, C5E10-A4-OOS. Verifie le 13-09-2026.
    # Le pilote reclamait ce fichier CHAQUE SOIR depuis quinze jours : « SOURCE
    # INTROUVABLE : le sas ». **Ce n etait pas un signal, c etait un faux positif
    # herite** — A-326 le disait deja du cockpit le 30-08, personne n avait
    # corrige le pilote. Une alerte qui dure sans etre instruite devient un bruit,
    # et un bruit cache les vraies.
    # Les fiches se comptent donc au REGISTRE DES STRATEGIES, sa vraie source.
    ch = trouver(base, "cac40_strategies.csv")
    if ch and not isinstance(lignes_csv(ch), Illisible):
        r = [x for x in lignes_csv(ch) if (x.get("etat_vie") or "").strip().upper() == "LABO"]
        OB = ["indicateurs", "univers", "tp", "sl", "horizon"]
        VIDE = ("", "-", "\u2014", "a renseigner", "\u00e0 renseigner")
        c["fiches au sas"] = len(r)
        c["fiches complètes"] = sum(
            1 for x in r
            if all((x.get(k) or "").strip().lower() not in VIDE for k in OB))

    # UNE SOURCE INTROUVABLE SE DIT, elle ne se tait pas. Sans cela, le pilote
    # aurait l'air complet en ayant perdu une donnée — c'est le pire des cas.
    c["_sources_muettes"] = [nom for nom, motifs in (
        ("le registre", ("REGISTRE_REGLES",)),
        ("le backlog", ("BACKLOG_DECISIONS.md",)),
        ("les cours", ("cours_maitre.csv",)),
        ("l'état civil des stratégies", ("cac40_strategies.csv",)),
        ("les positions", ("claude_positions_ouvertes.csv", "positions_ouvertes.csv")),
    ) if not trouver(base, *motifs)]

    # LES DEUX NOMBRES ET LEURS DEUX ROLES (R-722) : un TEST DE BALANCE n'est
    # jamais une PERFORMANCE. Le pilote doit porter les deux, nommés.
    # LE GOLDEN LE PLUS RÉCENT, JAMAIS LE PREMIER PAR ORDRE ALPHABÉTIQUE.
    # R-701 dit que l'ancien golden du 12/07 ne doit pas être détruit ; le jour
    # où il revient au projet, un tri alphabétique le placerait AVANT celui du
    # 01/08 et le pilote annoncerait 85 opérations sans un mot (A-284).
    gs = sorted({os.path.join(d, f) for d, _, fs in _marcher(base) for f in fs
                 if f.replace(" ", "_").lower().startswith("golden_tests")})
    if len(gs) > 1:
        c.setdefault("_ambigus", []).append(
            f"{len(gs)} fichiers de chiffres figés — le plus récent est retenu : "
            + ", ".join(os.path.basename(x) for x in gs))
    # UN FICHIER SANS DATE NE S'ÉCARTE PAS EN SILENCE. Avec `or ""`, un golden
    # nommé sans date lisible se classait DERNIER, donc « le moins récent », et
    # disparaissait sans un mot alors que l'alerte d'ambiguïté, elle, l'annonçait.
    # Les deux mécanismes se contredisaient. On le SIGNALE au lieu de l'écarter.
    sans_date = [x for x in gs if not _date_du_nom(x)]
    if sans_date:
        c.setdefault("_ambigus", []).append(
            "chiffres figés sans date lisible dans le nom, donc impossibles à "
            "classer : " + ", ".join(os.path.basename(x) for x in sans_date))
    datables = [x for x in gs if _date_du_nom(x)]
    ch = (max(datables, key=_date_du_nom) if datables
          else (gs[0] if gs else trouver(base, "golden_tests_")))
    if ch:
        try:
            import json
            g = json.load(open(ch, encoding="utf-8"))
            for k, v in g.items():
                if k == "meta":
                    continue
                ji = v.get("jetons_illimites", {})
                if ji:
                    c["test de balance"] = (f"{ji.get('n')} op · {ji.get('wr')} % · "
                                            f"{ji.get('net'):+,.2f} €".replace(",", " "))
                    break
            pass
        except (json.JSONDecodeError, OSError, TypeError, AttributeError):
            pass
        src["les chiffres figés"] = os.path.basename(ch)

    # dernier trade clos
    ch = trouver(base, "claude_journal_trades.csv", "journal_trades.csv")
    if ch and isinstance(lignes_csv(ch), Illisible):
        c.setdefault("_illisibles", []).append(("le journal des trades",
                                                lignes_csv(ch).motif))
        ch = None
    if ch:
        r = lignes_csv(ch)
        if r:
            # LE DERNIER ÉCRIT N'EST PAS LE DERNIER CLOS. Rien ne garantit que
            # le journal soit trié : on prend la date de sortie la plus tardive,
            # jamais la dernière ligne du fichier.
            # LE TRI DOIT ÊTRE CHRONOLOGIQUE, PAS ALPHABÉTIQUE. Avec des dates
            # en AAAA-MM-JJ les deux coïncident — PAR CHANCE, pas par
            # construction. Le jour où une date s'écrirait JJ-MM-AAAA, le tri
            # deviendrait faux sans un mot. On normalise donc avant de trier.
            # Et la colonne se choisit sur un nom EXACT, jamais sur le premier
            # qui contient un mot : l'ordre du dictionnaire ne doit jamais
            # décider à la place d'une règle (A-284).
            def _dt(x):
                """Rend la date de sortie d'une opération, réécrite pour être triée.

                ① RÔLE — Donner à chaque ligne du journal des trades une date
                  comparable, pour que la dernière opération CLOSE soit désignée par sa
                  date et non par sa place dans le fichier.
                ② CONTEXTE D'APPEL — `compter`, deux fois par ligne du journal des
                  trades : une première fois pour savoir si au moins une ligne porte une
                  date de sortie, une seconde fois comme clé de tri.
                ③ ENTRÉE — `x` : la ligne d'une opération, c'est-à-dire le tableau qui
                  associe à chaque nom de colonne sa valeur. L'appelant passe sans la
                  modifier une ligne de `donnees/claude_journal_trades.csv`.
                ④ CONDITIONS D'ENTRÉE — Aucune. Une ligne sans colonne de date de sortie
                  ne la fait pas tomber.
                ⑤ SORTIE — UNE valeur : la date réécrite année, mois, jour quand elle
                  était écrite jour, mois, année ; la valeur telle quelle quand elle ne
                  rapproche pas ce motif ; un texte vide quand aucune colonne reconnue
                  n'existe.
                  [rend: 1]
                ⑥ TRAITEMENT — ① parcourir les colonnes · ② retenir la première dont le
                  nom, sans blancs et en minuscules, est exactement `date_sortie`,
                  `date_cloture` ou `date_clôture` · ③ si sa valeur commence par deux
                  chiffres, un tiret, deux chiffres, un tiret, quatre chiffres, la
                  réécrire année, mois, jour · ④ sinon la rendre telle quelle · ⑤ rendre
                  un texte vide si aucune colonne ne convient.
                ⑦ UNITÉ — Une DATE de calendrier, sans heure ni fuseau.
                ⑧ POURQUOI — Le tri doit être chronologique et non alphabétique. Avec
                  des dates écrites année, mois, jour, les deux coïncident — PAR CHANCE,
                  pas par construction. Le jour où une date s'écrirait jour, mois,
                  année, le tri deviendrait faux sans un mot, et le pilote annoncerait
                  une opération close qui n'est pas la dernière. La réécriture supprime
                  ce hasard.
                  Et la colonne se choisit sur un nom EXACT, jamais sur le premier nom
                  qui contient le mot « sortie » : l'ordre des colonnes ne doit pas
                  décider à la place d'une règle, ce que l'action A-284 du backlog
                  consigne.
                ⑨ CE QUI CLOCHE —
                  ① Les valeurs qui ne rapprochent pas le motif sont rendues telles
                  quelles et se retrouvent mélangées aux dates réécrites dans le même
                  tri. Une colonne où coexisteraient deux écritures donnerait un
                  classement dont une partie serait juste et l'autre non, sans qu'aucune
                  alerte ne le dise.
                  ② Une ligne dont la date de sortie est VIDE rend un texte vide, qui se
                  classe avant toutes les autres. Une opération encore ouverte, écrite
                  au journal sans date de sortie, ne fausse donc pas le dernier rang —
                  mais rien ne dit qu'elle a été mise de côté, et le pilote annonce
                  « dernier trade clos » pour une ligne dont il n'a pas vérifié qu'elle
                  l'était.
                  ③ Les trois noms de colonne acceptés sont écrits en dur, alors que
                  `programmes/CONTRATS_DES_FICHIERS.py` existe pour déclarer une fois
                  pour toutes les champs d'un fichier partagé. Un chiffre ou un libellé
                  qui existe ailleurs ne se recopie pas (R-708).
                ⑩ EFFET — Aucun. Elle ne lit aucun fichier, n'en écrit aucun, n'affiche
                  rien et ne touche pas au réseau.
                ⑪ TERMINAISON — Rend toujours la main, par l'un de ses trois points de
                  sortie. Elle ne lève pas. Aucun de ses appels ne se termine.
                  [sort: non]
                ⑫ DÉFINITIONS
      le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui dit
        ou en est le projet, ce qu'il contient et ce qui cloche
      le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions et des actions du projet
                
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
                for k in x:
                    if k.strip().lower() in ("date_sortie", "date_cloture",
                                             "date_clôture"):
                        v = str(x.get(k) or "").strip()
                        m = re.match(r"(\d{2})-(\d{2})-(\d{4})", v)
                        return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else v
                return ""
            if not any(_dt(x) for x in r):
                c.setdefault("_ambigus", []).append(
                    "journal des trades sans colonne de date de sortie "
                    "reconnue : le dernier trade affiché est le dernier ÉCRIT, "
                    "pas forcément le dernier CLOS")
            else:
                r = sorted(r, key=_dt)
            d = r[-1]
            c["dernier trade clos"] = " · ".join(
                str(d.get(k)) for k in list(d)[:4] if d.get(k))
        src["le journal des trades"] = os.path.basename(ch)

    # la place occupée, relevée par l'audit du soir
    # Le nom long est ARCHIVÉ depuis le 12-09-2026 : deux rapports d'audit
    # coexistaient — celui de GitHub, frais, et celui de l'ancienne tâche Cowork,
    # périmé de plusieurs jours. Le pilote pouvait afficher le verdict du second.
    ch = trouver(base, "audit_du_jour.md")
    if ch:
        # L'AUDIT PORTE DEUX CHIFFRES DE PLACE, et l'un est un artefact connu :
        # le maillon 14-Taille compare des OCTETS a un plafond en TOKENS et
        # annonce plus de 100 %. Le chiffre autoritaire est celui rendu par
        # project_info. On ne prend QUE celui-la, et si on ne le trouve pas on ne met
        # RIEN plutot qu'un faux.
        # DEUX LIBELLES SONT ACCEPTES, et il faut les deux. L'audit a ecrit « Place REELLE »
        # jusqu'au 30-08-2026, puis « PLACE PROJET : NN,NN % » depuis le 01-09-2026, forme
        # rendue contractuelle dans son prompt. Ce lecteur ne cherchait que l'ancienne : la
        # place a disparu du pilote sans un mot, et seul le controle de regression l'a vu
        # (08-09-2026). Celui qui lit et celui qui ecrit ne doivent jamais diverger en silence.
        m = re.search(
            r"(?:PLACE\s+PROJET|Place\s+R[EÉ]ELLE)[^0-9]{0,30}(\d+[.,]\d+)\s*%",
            lire(ch), re.I)
        if m:
            c["place du projet"] = m.group(1).replace(".", ",") + " %"
        src["l'audit du soir"] = os.path.basename(ch)

    fichiers = [os.path.join(d, f) for d, _, fs in _marcher(base) for f in fs]
    c["fichiers du projet"] = len(fichiers)
    c["octets du projet"] = sum(os.path.getsize(f) for f in fichiers)
    return c, src


# ─────────────────────────────────────────────────────────────────────
# LIRE LES RÔLES — déclarés en tête de chaque fichier
# ─────────────────────────────────────────────────────────────────────

def roles(base):
    """Relève, en tête de chaque fichier, le rôle qu'il déclare.

    ① RÔLE — Dire de chaque fichier du dépôt s'il s'écrit à la main ou s'il se
      refabrique tout seul, en lisant ce que le fichier déclare lui-même. C'est ce
      qui permet au pilote de porter la carte du projet, et c'est ce qui évite la
      faute la plus coûteuse du système : corriger à la main un document qui sera
      écrasé au passage suivant.
    ② CONTEXTE D'APPEL — `main`, une seule fois par fabrication, juste après le
      comptage. Aucun appel hors de ce fichier.
    ③ ENTRÉE — `base` : la racine à parcourir. Un seul appelant, `main`, qui
      transmet sans le modifier le premier argument de la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un dossier inexistant rend deux listes vides.
    ⑤ SORTIE — DEUX valeurs : la liste des fichiers qui déclarent un rôle, chacun
      avec le texte de sa déclaration, et la liste de ceux qui n'en déclarent pas,
      chacun avec un texte vide. Les deux sont classées par chemin. Mesuré le
      19-09-2026 sur une copie du dépôt : 31 fichiers déclarent leur rôle, 195 n'en
      déclarent pas.
      [rend: 2]
    ⑥ TRAITEMENT — ① parcourir l'arborescence et retenir le chemin relatif de
      chaque fichier · ② les classer par ordre alphabétique · ③ écarter ceux dont
      l'extension n'est ni .md, ni .py, ni .csv, ni .json · ④ lire les SIX
      premières lignes de chacun · ⑤ retirer de chaque ligne les signes de mise en
      forme qui l'ouvrent, puis regarder si elle COMMENCE par l'une des six
      mentions acceptées · ⑥ ranger le fichier dans l'une ou l'autre liste.
    ⑦ UNITÉ — Un NOMBRE DE FICHIERS.
    ⑧ POURQUOI — Deux mots seulement sont employés, et ils se comprennent sans
      rien consulter. DÉCIDÉ veut dire écrit par un humain, et ne se régénère
      jamais ; FABRIQUÉ veut dire recréé par un programme, et le modifier à la main
      serait écrasé au passage suivant — c'est là qu'est le vrai danger. Les mots
      d'avant, « GROUPE 1 » et « GROUPE 2 », n'apprenaient rien : il fallait ouvrir
      le registre pour savoir lequel était lequel. Remarque de Jean-Luc du
      28-08-2026. Les anciennes mentions restent acceptées le temps que les
      fichiers migrent : on ne casse pas ce qui déclare déjà.
      La mention doit OUVRIR la ligne, et jamais s'y trouver n'importe où. Une
      phrase comme « Jean-Luc a décidé de remplacer… » n'est pas une déclaration de
      rôle : constaté le 28-08-2026, une recherche large rendait 13 rôles dont
      11 faux.
      Six lignes seulement sont lues, parce qu'une déclaration de rôle est une
      en-tête : la chercher plus loin ferait retenir une phrase du corps du
      document, et lire tous les fichiers en entier coûterait un parcours complet
      du dépôt à chaque fabrication.
    ⑨ CE QUI CLOCHE —
      ① Une phrase qui commence par le verbe « Fabrique » passe pour une
      déclaration de rôle. La comparaison porte sur les premières lettres, et
      `FABRIQUE` est l'une des mentions acceptées. Mesuré le 19-09-2026 :
      `programmes/FABRIQUER_LE_RELEVE_DES_TACHES.py` figure dans la liste des
      fichiers qui déclarent leur rôle, avec le texte « Fabrique le releve des
      prompts des taches planifiees, texte compris. » — une phrase ordinaire qui ne
      déclare rien. Le pilote annonce donc un rôle déclaré de plus qu'il n'y en a.
      ② Dix-huit fichiers ne sont dans aucune des deux listes. Seules quatre
      extensions sont regardées. Mesuré le 19-09-2026 : le pilote annonce
      « 244 fichiers vus », « 31 fichiers qui déclarent leur rôle » et
      « 195 fichiers sans rôle déclaré » — dix-huit fichiers ne sont nulle part,
      dont les deux fichiers .yml de .github/workflows/, qui sont les tâches
      planifiées faisant tourner tout le circuit du soir. Ils ne peuvent ni
      déclarer un rôle ni être reprochés de n'en pas déclarer.
      ③ Un fichier qu'on ne peut pas ouvrir est compté comme un fichier sans rôle.
      L'échec de lecture est rattrapé et abandonné ; le fichier part dans la liste
      des sans-rôle, exactement comme un fichier parfaitement lisible qui n'en
      déclare pas. Deux causes très différentes donnent la même ligne du pilote.
      ④ Le texte déclaré est rendu tel quel, sans borne de longueur. Un fichier
      dont la première ligne est un paragraphe entier fait entrer ce paragraphe
      dans la carte du pilote, comme on le voit pour
      `etudes/ANALYSE_DE_LA_PHOTO_DE_L_ECOSYSTEME_ET_DE_SES_OUTILS.md`, dont la
      déclaration relevée le 19-09-2026 se termine par deux astérisques restés
      collés.
      ⑤ Les six mentions acceptées sont écrites en dur dans le code, alors que la
      règle qui les définit vit au registre. Un chiffre ou un libellé qui existe
      ailleurs ne se recopie pas (R-708) : ajouter une mention au registre sans
      toucher à ce code la rendrait invisible au pilote.
    ⑩ EFFET — PARCOURT l'arborescence sous la racine et LIT les six premières
      lignes de chaque fichier retenu. N'écrit rien, n'affiche rien, ne touche pas
      au réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas sur la lecture d'un
      fichier, cet échec étant rattrapé. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
  un role declare : la mention DECIDE ou FABRIQUE placee en tete d'un fichier,
    qui dit si ce fichier s'ecrit a la main ou se refabrique tout seul
  le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui dit
    ou en est le projet, ce qu'il contient et ce qui cloche
  le depot : le depot GitHub ou vivent les fichiers du systeme, le projet n'en
    etant qu'une copie de lecture
  le registre : gouvernance/REGISTRE_REGLES.md, le document qui porte les regles
    numerotees du projet ; une regle absente du registre n'existe pas
  la tache planifiee : un fichier de .github/workflows/ qui fait tourner un
    programme a heure fixe sur une machine GitHub, sans clic ni autorisation
    
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
"""
    out, sans = [], []
    tous = []
    for d, _, fs in _marcher(base):
        for f in fs:
            rel = os.path.relpath(os.path.join(d, f), base)
            tous.append((rel, os.path.join(d, f)))
    for f, p in sorted(tous):
        if not os.path.isfile(p) or not f.endswith((".md", ".py", ".csv", ".json")):
            continue
        tete = ""
        try:
            with open(p, encoding="utf-8", errors="replace") as fh:
                for _ in range(6):
                    l = fh.readline()
                    if not l:
                        break
                    # DEUX MOTS QUI SE COMPRENNENT SANS RIEN CONSULTER.
                    # « GROUPE 1 » et « GROUPE 2 » étaient du jargon : il fallait
                    # ouvrir le registre pour savoir lequel était lequel.
                    # DÉCIDÉ  = écrit par un humain, ne se régénère jamais.
                    # FABRIQUÉ = recréé par un programme, ne s'écrit jamais à la
                    #            main — le modifier serait écrasé au passage suivant.
                    # Les anciennes mentions restent acceptées le temps que les
                    # fichiers migrent : on ne casse pas ce qui déclare déjà.
                    # LA MENTION DOIT OUVRIR LA LIGNE, jamais s'y trouver
                    # n'importe où : « Jean-Luc a décidé de remplacer… » n'est
                    # pas une déclaration de rôle. Constaté le 28/08 : une
                    # recherche large rendait 13 rôles dont 11 faux.
                    h = l.strip().lstrip("#*\"'> \t").upper()
                    if h.startswith(("DÉCIDÉ", "DECIDE", "FABRIQUÉ", "FABRIQUE",
                                     "GROUPE 1", "GROUPE 2")):
                        tete = l.strip().lstrip("#*\"'> \t").strip()
                        break
        except OSError:
            pass
        (out if tete else sans).append((f, tete))
    return out, sans


# ─────────────────────────────────────────────────────────────────────
# CONTRÔLER — signaler, jamais corriger
# ─────────────────────────────────────────────────────────────────────

def controler(base, c, sans):
    """Dresse la liste de ce qui cloche, sans jamais rien corriger.

    ① RÔLE — Réunir en une seule liste tout ce que le pilote doit signaler :
      références mortes, écarts de comptage, séances incomplètes, fichiers sans
      rôle déclaré, sources ambiguës, illisibles ou introuvables. Cette liste
      devient la première section du pilote, celle que le rituel de début de
      session fait lire avant tout le reste.
    ② CONTEXTE D'APPEL — `main`, une seule fois par fabrication, après le comptage
      et le relevé des rôles, et avant la composition du texte. Aucun appel hors de
      ce fichier.
    ③ ENTRÉE — `base` : la racine à lire · `c` : le tableau des chiffres relevés
      par `compter` · `sans` : la liste des fichiers sans rôle déclaré, rendue par
      `roles`. Un seul appelant, `main`, qui passe les trois sans les modifier.
    ④ CONDITIONS D'ENTRÉE — Le tableau des chiffres doit porter les clés de service
      commençant par un tiret bas, telles que `compter` les pose ; leur absence ne
      fait pas tomber la fonction mais supprime silencieusement les alertes
      correspondantes.
    ⑤ SORTIE — UNE valeur : la liste des phrases d'alerte, dans l'ordre où elles
      sont ajoutées. Elle est vide quand rien n'a été trouvé. Mesuré le
      19-09-2026 sur une copie du dépôt : trois alertes — deux références mortes et
      195 fichiers sans rôle déclaré.
      [rend: 1]
    ⑥ TRAITEMENT — ① relire le backlog et le registre · ② relever les actions et
      les règles CITÉES dans le backlog qui n'existent nulle part · ③ comparer le
      nombre d'actions annoncé par le tampon au nombre de lignes du tableau ·
      ④ signaler les séances dont le compte de valeurs s'écarte · ⑤ signaler les
      fichiers sans rôle déclaré · ⑥ reprendre les sources ambiguës, illisibles et
      introuvables relevées au comptage · ⑦ signaler un sas dont aucune fiche n'est
      complète.
    ⑦ UNITÉ — Des NOMBRES D'ACTIONS, de règles, de séances et de fichiers. Chaque
      alerte porte son propre compte, et les listes affichées sont coupées à cinq
      ou six éléments.
    ⑧ POURQUOI — Le programme signale et ne corrige jamais. Un document qui
      corrigerait ce qu'il mesure ne mesurerait plus rien : toute correction se
      fait à la source, puis on refabrique.
      Le motif qui relève les règles du registre est EXACTEMENT celui du comptage,
      et ce n'est pas un détail. S'ils divergent, le pilote déclare MORTES des
      règles vivantes : mesuré le 08-09-2026, R-731, R-732, R-733, R-734, R-734bis
      et R-735 étaient accusées d'inexistence alors qu'elles sont au registre,
      écrites en titre et non en liste.
      Une source introuvable se dit, elle ne se tait pas. Sans cela, le pilote
      aurait l'air complet en ayant perdu une donnée, et c'est le pire des cas :
      ce n'est pas zéro, c'est inconnu.
    ⑨ CE QUI CLOCHE —
      ① Les références mortes ne sont cherchées que dans le backlog. Le registre
      est lu, mais seulement pour savoir quelles règles existent : une règle qui en
      citerait une autre, disparue, ne serait jamais signalée. Mesuré le
      19-09-2026 : les deux alertes de références mortes portent uniquement sur des
      identifiants cités dans le backlog — neuf actions et six règles.
      ② L'écart de comptage du backlog ne peut pas se signaler quand le tampon est
      en échec. La comparaison exige deux entiers ; or le nombre d'actions n'est lu
      que derrière le mot OK et vaut « ? » sinon. Mesuré le 19-09-2026 : le tampon
      du dépôt annonce « ÉCHEC** — 413 actions » et le tableau porte 418 lignes ;
      aucune alerte d'écart n'est produite. Le garde-fou s'éteint exactement le jour
      où il servirait.
      ③ Une séance incomplète est définie par rapport au compte le plus FRÉQUENT,
      jamais par rapport à un nombre attendu. Si une valeur disparaissait
      durablement des cours, le nouveau compte deviendrait le plus fréquent et ce
      sont les séances complètes d'avant qui seraient signalées.
      ④ L'alerte sur les fichiers sans rôle noie les autres. Mesuré le 19-09-2026 :
      elle porte sur 195 fichiers et revient à chaque passage. Une alerte
      permanente apprend à ne plus regarder, et elle occupe un tiers de la première
      section du pilote.
      ⑤ L'alerte « SAS VIDE » ne se déclenche que si des fiches existent. Un sas
      réellement vide — aucune fiche du tout — ne produit aucune alerte, alors que
      c'est le cas où le juge des stratégies n'a vraiment rien à juger.
      ⑥ La fonction relit le backlog et le registre alors que `compter` vient de les
      lire. Les deux lectures ne sont pas comparées, et rien ne garantit qu'elles
      portent sur le même fichier si l'arborescence a changé entre-temps.
    ⑩ EFFET — LIT le backlog et le registre, et PARCOURT l'arborescence par ses
      appels à la recherche de fichiers. N'écrit rien, n'affiche rien, ne touche pas
      au réseau, et ne modifie ni le tableau des chiffres ni la liste des fichiers
      qu'on lui passe.
    ⑪ TERMINAISON — Rend toujours la main. Elle PEUT LEVER par son appel à
      `trouver`, qui lève sur un dossier existant mais illisible.
      [sort: non]
    ⑫ DÉFINITIONS
  le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui dit
    ou en est le projet, ce qu'il contient et ce qui cloche
  le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions et des actions du projet
  le tampon : la ligne d'horodatage posee en tete du backlog par
    programmes/verif_backlog.py, qui annonce elle-meme un nombre d'actions
  le registre : gouvernance/REGISTRE_REGLES.md, le document qui porte les regles
    numerotees du projet ; une regle absente du registre n'existe pas
  le sas : les fiches de strategie en etat LABO a l'etat civil, celles qui
    attendent d'etre jugees par le juge des stratégies
  une seance : une journee de bourse pour une valeur, avec son ouverture, son
    plus haut, son plus bas, sa cloture et son volume
  un role declare : la mention DECIDE ou FABRIQUE placee en tete d'un fichier,
    qui dit si ce fichier s'ecrit a la main ou se refabrique tout seul
  le zero silencieux : un chiffre affiche a zero parce que la lecture a rate,
    et que rien ne distingue ce ratage d'un vrai zero
  le depot : le depot GitHub ou vivent les fichiers du systeme, le projet n'en
    etant qu'une copie de lecture
    
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
  le garde-fou : le programme `CONTROLER_MA_LIVRAISON.py`, qui accepte ou refuse un travail avant qu il parte à la relecture
  une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
"""
    al = []
    ch = trouver(base, "BACKLOG_DECISIONS.md")
    chr_ = trouver(base, "REGISTRE_REGLES")
    if ch and chr_:
        t, r = lire(ch), lire(chr_)
        act = {m.group(1) for m in re.finditer(r"^\|\s*(A-\d+\w*)\s*\|", t, re.M)}
        # LE MEME MOTIF QUE LE COMPTAGE, et ce n'est pas un detail : s'ils divergent, le
        # pilote declare MORTES des regles vivantes. Mesure du 08-09-2026 : R-731, R-732,
        # R-733, R-734, R-734bis et R-735 accusees d'inexistence alors qu'elles sont au
        # registre, ecrites en titre.
        reg = {m.group(1) for m in re.finditer(
            r"^(?:[-*+]\s+|#{1,6}\s+)\*{0,2}\s*(R-\d+\w*)\b", r, re.M)}
        fa = sorted({x for x in re.findall(r"\bA-\d+\w*", t)} - act)
        fr = sorted({x for x in re.findall(r"\bR-\d+\w*", t)} - reg)
        if fa:
            al.append(f"RÉFÉRENCE MORTE : {len(fa)} action(s) citées et inexistantes "
                      f"— {', '.join(fa[:6])}{' …' if len(fa) > 6 else ''}")
        if fr:
            al.append(f"RÉFÉRENCE MORTE : {len(fr)} règle(s) citées et inexistantes "
                      f"— {', '.join(fr)}")
    if isinstance(c.get("actions au tampon"), int) and isinstance(c.get("lignes de tableau"), int):
        if c["actions au tampon"] != c["lignes de tableau"]:
            al.append(f"ÉCART DE COMPTAGE : le tampon dit {c['actions au tampon']}, "
                      f"le fichier porte {c['lignes de tableau']} lignes")
    if c.get("séances incomplètes"):
        al.append(f"SÉANCE INCOMPLÈTE : {c['séances incomplètes']} séance(s) "
                  f"n'ont pas leur compte de valeurs")
    if sans:
        al.append(f"RÔLE NON DÉCLARÉ : {len(sans)} fichier(s) sans mention DÉCIDÉ ou FABRIQUÉ "
                  f"— {', '.join(x[0] for x in sans[:5])}"
                  f"{' …' if len(sans) > 5 else ''}")
    for a in c.get("_ambigus", []):
        al.append(f"SOURCE AMBIGUË : {a}")
    for s, motif in c.get("_illisibles", []):
        al.append(f"SOURCE ILLISIBLE : {s} — {motif}. Les chiffres qui en "
                  f"dépendent MANQUENT. Ce n'est pas zéro, c'est inconnu.")
    for s in c.get("_sources_muettes", []):
        al.append(f"SOURCE INTROUVABLE : {s} — les chiffres qui en dépendent "
                  f"MANQUENT au pilote. Ce n'est pas zéro, c'est inconnu.")
    if c.get("fiches complètes") == 0 and c.get("fiches au sas"):
        al.append("SAS VIDE : aucune fiche complète, le juge des stratégies n'a rien à juger")
    return al


# ─────────────────────────────────────────────────────────────────────

def main():
    """Fabrique le pilote, le compare à celui de la veille, l'écrit et affiche le bilan.

    ① RÔLE — Enchaîner les quatre relevés — socle, chiffres, rôles, alertes —,
      composer le document, vérifier qu'aucun élément présent hier n'a disparu,
      écrire le fichier et rendre compte à l'écran. C'est le seul endroit du
      programme qui écrit sur le disque.
    ② CONTEXTE D'APPEL — Le lancement du programme, et lui seul. Sa valeur de
      retour est passée directement à la sortie du processus. Le lancement
      automatique est le pas « Fabriquer le PILOTE » de
      .github/workflows/collecte_abc.yml, du lundi au vendredi à 18 h UTC, soit
      20 h à Paris en été et 19 h en hiver.
    ③ ENTRÉE — Aucun paramètre. Elle lit elle-même la ligne de commande : le
      premier argument est la racine, le second le fichier à écrire. La tâche
      planifiée passe `$GITHUB_WORKSPACE` puis
      `$GITHUB_WORKSPACE/gouvernance/PILOTE.md`.
    ④ CONDITIONS D'ENTRÉE — La racine doit se parcourir, et le DOSSIER du fichier
      de sortie doit exister. Mesuré le 19-09-2026 : un lancement sans argument
      fait tout le travail puis s'arrête sur « FileNotFoundError: [Errno 2] No such
      file or directory: '/mnt/project/PILOTE.md' », et rien n'est écrit.
    ⑤ SORTIE — UNE valeur : le nombre 0, toujours, quel que soit le nombre
      d'alertes.
      [rend: 1]
    ⑥ TRAITEMENT — ① déterminer la racine et le fichier de sortie · ② lire le
      socle · ③ relever les chiffres, les rôles et les alertes · ④ composer le
      document : en-tête, canal de lecture, alertes, tableau des chiffres,
      stratégies vivantes, sources, fichiers avec et sans rôle déclaré, puis le
      socle recopié tel quel · ⑤ relire le pilote de la veille et comparer les
      libellés des lignes de tableau · ⑥ insérer un avertissement de régression
      avant le tableau si des libellés ont disparu · ⑦ écrire le fichier ·
      ⑧ afficher le chemin, la taille, le socle lu, les comptes de rôles et les
      alertes · ⑨ rendre 0.
    ⑦ UNITÉ — Des NOMBRES DE FICHIERS et d'alertes. La taille du document écrit est
      en OCTETS : mesuré le 19-09-2026 sur une copie du dépôt, 21 592 octets.
      L'horodatage est en heure de Paris.
    ⑧ POURQUOI — La destination par défaut est le dossier `gouvernance`, et jamais
      la racine. Le 16-09-2026, le contrôle des homonymes a trouvé DEUX fichiers
      `PILOTE.md` vivant côte à côte : 21 260 octets à la racine, à jour, et
      18 046 octets dans `gouvernance`, figés au 13-09. La tâche planifiée passait
      pourtant le bon chemin en second argument : c'était le défaut du programme
      qui créait le doublon, puisque lancé à la main sans ce second argument il
      écrivait à la racine, et personne ne lisait ce fichier-là.
      Le contrôle de régression existe parce qu'un contrôle sans contrôle est mort.
      Avant d'écrire, le programme compare le document composé à celui de la
      veille : un élément qui DISPARAÎT est une régression, jamais une
      amélioration. C'est ce qui a manqué le 25-08-2026, où une section entière est
      tombée sans bruit. Le programme ne juge pas le contenu, il compare des
      PRÉSENCES.
      Le canal de lecture et le nombre de fichiers vus sont écrits en tête du
      document parce que le même programme lancé depuis deux endroits produit deux
      pilotes différents : il ne calcule pas mal, il ne voit pas la même chose.
    ⑨ CE QUI CLOCHE —
      ① Le contrôle de régression surveille aussi le socle, qui est écrit à la
      main. Il relève la première case de TOUTES les lignes de tableau du
      document, et le socle est recopié en entier à la fin du pilote, avec ses
      propres tableaux. Mesuré le 19-09-2026 sur une copie : renommer une ligne de
      `gouvernance/PILOTE_SOCLE.md` de « les règles » en « les regles (renomme) »
      fait apparaître l'alerte « RÉGRESSION : 1 élément(s) présents hier et absents
      aujourd'hui — les règles ». Le contrôle accuse une perte de mesure là où il
      n'y a qu'une réécriture voulue.
      ② Le contrôle compare des LIBELLÉS d'affichage, pas des sources. Tout
      renommage d'une ligne du tableau produira une alerte de régression, à ignorer
      ce jour-là — et une alerte qu'on apprend à ignorer cesse de protéger. Ce
      défaut est connu et écrit dans l'en-tête du programme comme limite non
      corrigée ; le remède serait de comparer des sources.
      ③ Le contrôle ne voit rien quand l'élément manque DEUX jours de suite.
      Mesuré le 19-09-2026 : la ligne « place du projet » est absente du pilote
      fabriqué et absente aussi de `gouvernance/PILOTE.md` du 17-09-2026 ; aucune
      alerte de régression ne la mentionne. Une perte devient donc définitivement
      invisible dès le second passage.
      ④ La fonction rend toujours 0. La tâche planifiée écrit
      `|| { echo "::error::Fabriquer le PILOTE A ÉCHOUÉ"; exit 1; }` et ne juge donc
      le pas que sur ce code : un pilote annonçant « SOURCE INTROUVABLE » ou
      « RÉGRESSION » laisse un pas vert. Un contrôle qui n'a pas pu tourner, ou qui
      a trouvé une faute, doit rendre un code non nul (R-734).
      ⑤ L'alerte de régression est ajoutée à la liste APRÈS que cette liste a été
      écrite dans le document. L'avertissement figure bien dans le texte, mais la
      section « CE QUI CLOCHE » du pilote ne le porte pas : la régression est
      affichée à l'écran et insérée en encadré, jamais rangée avec les autres
      alertes. Deux endroits du même document disent deux choses différentes.
      ⑥ Le repli sur la racine ne se déclenche que si le dossier `gouvernance`
      manque. Si ce dossier existe mais que le fichier ne peut pas y être écrit,
      la fonction lève et rien n'est produit ; le pilote de la veille reste en
      place, à sa date, et seul l'horodatage qu'il porte permet de s'en apercevoir.
      ⑦ Le socle absent devient une ligne de texte dans le document. Quand la
      lecture échoue, le pilote porte « *(socle introuvable)* » à la place de la
      dernière section, mais aucune alerte n'est ajoutée à la liste : la perte est
      visible pour qui lit jusqu'au bout, invisible pour qui lit la première
      section.
    ⑩ EFFET — ÉCRIT le fichier de sortie, entièrement, à chaque passage. LIT le
      socle, le pilote de la veille, et toutes les sources par ses appels. AFFICHE
      quatre lignes de bilan suivies d'une ligne par alerte. AUCUN ACCÈS RÉSEAU.
      Aucun autre fichier n'est touché, aucune source n'est modifiée, rien n'est
      supprimé.
    ⑪ TERMINAISON — Rend la main avec 0 dans le cas normal. Elle PEUT LEVER une
      erreur non rattrapée qui arrête alors le programme : quand le dossier du
      fichier de sortie n'existe pas, mesuré le 19-09-2026 sur un lancement sans
      argument. Un de ses appels peut aussi ne pas revenir : `compter`, `controler`
      et `trouver` lèvent sur un dossier existant mais illisible.
      [sort: non]
    ⑫ DÉFINITIONS
  le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui dit
    ou en est le projet, ce qu'il contient et ce qui cloche
  le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté ailleurs.
  le controle de regression : la comparaison du pilote en cours de fabrication
    avec celui de la veille, un element disparu etant tenu pour une perte
  la tache planifiee : un fichier de .github/workflows/ qui fait tourner un
    programme a heure fixe sur une machine GitHub, sans clic ni autorisation
  un role declare : la mention DECIDE ou FABRIQUE placee en tete d'un fichier,
    qui dit si ce fichier s'ecrit a la main ou se refabrique tout seul
  le depot : le depot GitHub ou vivent les fichiers du systeme, le projet n'en
    etant qu'une copie de lecture
  le zero silencieux : un chiffre affiche a zero parce que la lecture a rate,
    et que rien ne distingue ce ratage d'un vrai zero
    
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
  la tâche planifiée : un fichier de .github/workflows/ qui fait tourner un programme à heure fixe sur une machine GitHub, sans clic ni autorisation.
  une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    base = sys.argv[1] if len(sys.argv) > 1 else "/mnt/project"
    # LA DESTINATION PAR DEFAUT EST `gouvernance/`, JAMAIS LA RACINE.
    # Trouve le 16-09-2026 par le controle des homonymes du socle, ecrit le
    # jour meme. **Deux `PILOTE.md` coexistaient : 21 260 octets a la racine,
    # a jour, et 18 046 octets dans `gouvernance/`, figes au 13-09.**
    # Le workflow passe bien `$GITHUB_WORKSPACE/gouvernance/PILOTE.md` en
    # second argument — **il avait raison. C est le DEFAUT du programme qui
    # creait le doublon : lance a la main sans second argument, il ecrivait a
    # la racine, et personne ne lisait ce fichier-la.**
    # Le §11 des instructions nomme `gouvernance/PILOTE.md` comme premier
    # document de la hierarchie : le defaut doit y mener.
    _defaut = os.path.join(base, "gouvernance", "PILOTE.md")
    if not os.path.isdir(os.path.dirname(_defaut)):
        _defaut = os.path.join(base, "PILOTE.md")
    sortie = sys.argv[2] if len(sys.argv) > 2 else _defaut

    socle_ch = trouver(base, "PILOTE_SOCLE.md")
    socle = lire(socle_ch)
    c, src = compter(base)
    lus, sans = roles(base)
    al = controler(base, c, sans)

    L = []
    L.append("FABRIQUÉ · Rôle : dire où en est le projet et ce qu'il contient.")
    L.append("Quand l'appeler : au rituel de début de session.\n")
    L.append("# PILOTE")
    L.append(f"**Fabriqué le {horodatage()} — CE FICHIER N'EST JAMAIS ÉCRIT À LA MAIN.**")
    L.append(f"**Canal de lecture : `{os.path.abspath(base)}` — "
             f"{c.get('fichiers du projet', '?')} fichiers vus.** "
             "*Le même programme lu par deux canaux produit deux pilotes différents : "
             "il ne calcule pas mal, il ne voit pas la même chose. Un disque monté est "
             "en retard sur le projet, et toute absence qu'il annonce est à vérifier "
             "avant d'être crue (R-710).*")
    L.append("Toute correction se fait à la source, puis on refabrique.\n")

    if al:
        L.append("## ⚠️ CE QUI CLOCHE\n")
        for a in al:
            L.append(f"- {a}")
        L.append("")
    else:
        L.append("## ✅ AUCUNE ALERTE\n")

    L.append("## OÙ EN EST LE PROJET\n")
    L.append("| | |")
    L.append("|---|---|")
    ordre = ["stratégies vivantes", "positions ouvertes", "dernier trade clos",
             "dernière séance de l'historique figé", "séances", "valeurs", "séances incomplètes",
             "test de balance", "performance de référence",
             "actions au tampon", "règles R", "version du registre", "origine du registre",
             "fiches au sas", "fiches complètes", "fichiers du projet",
             "place du projet"]
    for k in ordre:
        if k in c:
            v = c[k]
            L.append(f"| {k} | **{v:,}** |".replace(",", " ")
                     if isinstance(v, int) else f"| {k} | **{v}** |")
    if c.get("_vivantes"):
        L.append("")
        for i, e, cp, u in c["_vivantes"]:
            L.append(f"- **{i}** · état {e} · compteur {cp} · univers {u}")
    L.append("")
    L.append("*Chiffres comptés depuis : " +
             " · ".join(f"{k} ({v})" for k, v in src.items()) + "*\n")

    L.append(f"## LES {len(lus)} FICHIERS QUI DÉCLARENT LEUR RÔLE\n")
    L.append("*DÉCIDÉ = écrit à la main, ne se régénère jamais · FABRIQUÉ = recréé par un programme, le modifier à la main serait écrasé au passage suivant.*\n")
    for f, t in lus:
        L.append(f"- `{f}` — {t}")
    if sans:
        L.append(f"\n## LES {len(sans)} FICHIERS SANS RÔLE DÉCLARÉ\n")
        for f, _ in sans:
            L.append(f"- `{f}`")
    L.append("\n---\n")
    L.append("## LE SOCLE — la seule partie écrite à la main\n")
    L.append(socle if socle else "*(socle introuvable)*")

    # ─────────────────────────────────────────────────────────────
    # LE CONTRÔLE DU CONTRÔLE — un contrôle sans contrôle est mort.
    # Avant d'écrire, on compare au pilote de la veille : un élément qui
    # DISPARAÎT est une régression, jamais une amélioration. C'est ce qui
    # a manqué le 25-08-2026, où une section entière est tombée sans bruit.
    # Le programme ne juge pas le contenu : il compare des PRÉSENCES.
    # ─────────────────────────────────────────────────────────────
    txt = "\n".join(L)
    ancien = lire(sortie)
    if ancien:
        def elements(t):
            """Rend les libellés de toutes les lignes de tableau d'un document.

            ① RÔLE — Donner au contrôle de régression la liste de ce qu'un pilote
              portait, pour qu'on puisse la comparer à celle du pilote en cours de
              fabrication. Un libellé présent hier et absent aujourd'hui est tenu pour
              une perte.
            ② CONTEXTE D'APPEL — `main`, deux fois, dans la même comparaison : une fois
              sur le pilote de la veille, une fois sur le texte qui vient d'être
              composé. Appelée seulement si le pilote de la veille a pu être lu.
            ③ ENTRÉE — `t` : le texte entier d'un pilote. L'appelant passe d'un côté ce
              que la lecture du fichier de sortie a rendu, de l'autre le document qu'il
              vient d'assembler.
            ④ CONDITIONS D'ENTRÉE — Aucune. Un texte vide rend un ensemble vide.
            ⑤ SORTIE — UNE valeur : l'ensemble des libellés trouvés, sans doublon et
              sans ordre. Sur le pilote fabriqué le 19-09-2026, il contient les seize
              libellés du tableau des chiffres, le séparateur `---` des tableaux, et les
              libellés des tableaux que le socle apporte avec lui.
              [rend: 1]
            ⑥ TRAITEMENT — ① chercher, à chaque début de ligne, une barre verticale
              suivie du texte jusqu'à la barre suivante · ② écarter les cases dont le
              premier caractère est une étoile, qui sont les valeurs en gras · ③ retirer
              les blancs de début et de fin · ④ réunir sans doublon.
            ⑦ UNITÉ — Un NOMBRE DE LIBELLÉS.
            ⑧ POURQUOI — Le contrôle compare des PRÉSENCES et non des valeurs. Une
              valeur qui change est une nouvelle mesure, ce qui est normal ; un libellé
              qui disparaît veut dire qu'une source ne répond plus, ce qui ne l'est pas.
              Le 25-08-2026, une section entière du pilote est tombée sans bruit, et
              rien ne l'a vu : c'est cet incident qui a fait écrire ce contrôle.
              Les cases commençant par une étoile sont écartées parce que le tableau du
              pilote écrit ses valeurs en gras, entre doubles étoiles : sans cette
              exclusion, la moindre variation d'un chiffre serait lue comme la
              disparition d'un élément.
            ⑨ CE QUI CLOCHE —
              ① Elle ne fait aucune différence entre les lignes du tableau fabriqué et
              celles du socle, qui est écrit à la main et recopié en entier à la fin du
              pilote. Mesuré le 19-09-2026 sur une copie : renommer une ligne de
              `gouvernance/PILOTE_SOCLE.md` de « les règles » en
              « les regles (renomme) » fait apparaître « RÉGRESSION : 1 élément(s)
              présents hier et absents aujourd'hui — les règles ». Une réécriture voulue
              d'un document à la main est signalée comme une perte de mesure.
              ② Le séparateur des tableaux entre dans l'ensemble. La ligne `|---|---|`
              donne le libellé `---`, qui n'est pas un élément mesuré. Il ne disparaît
              jamais, donc il ne déclenche rien, mais il fausse tout comptage qu'on
              voudrait faire de cet ensemble.
              ③ Le rapprochement se fait sur le texte affiché, jamais sur la source
              derrière. Renommer un libellé du tableau produit donc à la fois une
              disparition et une apparition, et seule la disparition est signalée : le
              message annonce une régression là où il n'y a qu'un changement de nom.
            ⑩ EFFET — Aucun. Elle ne lit aucun fichier, n'en écrit aucun, n'affiche rien
              et ne touche pas au réseau.
            ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels
              ne se termine.
              [sort: non]
            ⑫ DÉFINITIONS
      le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui dit
        ou en est le projet, ce qu'il contient et ce qui cloche
      le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté ailleurs.
      le controle de regression : la comparaison du pilote en cours de fabrication
        avec celui de la veille, un element disparu etant tenu pour une perte
            
      le rapprochement : le fait de reconnaître que deux écritures différentes désignent le même fichier ou la même entreprise
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
            return {m.group(1).strip()
                    for m in re.finditer(r"^\|\s*([^|*][^|]*?)\s*\|", t, re.M)}
        perdus = sorted(elements(ancien) - elements(txt))
        if perdus:
            avert = ("\n> ⚠️ **RÉGRESSION — ces éléments étaient dans le pilote "
                     "de la veille et n'y sont plus : " + ", ".join(perdus) +
                     ". Un élément qui disparaît est une régression, jamais une "
                     "amélioration. Chercher pourquoi la source ne répond plus "
                     "AVANT de considérer ce pilote comme valable.**\n")
            i = txt.find("## OÙ EN EST LE PROJET")
            txt = txt[:i] + avert + "\n" + txt[i:] if i > 0 else avert + txt
            al.append(f"RÉGRESSION : {len(perdus)} élément(s) présents hier et "
                      f"absents aujourd'hui — {', '.join(perdus[:5])}")

    with open(sortie, "w", encoding="utf-8") as f:
        f.write(txt)

    print(f"PILOTE fabriqué : {sortie}  ({len(txt.encode()):,} octets)".replace(",", " "))
    print(f"  socle lu       : {os.path.basename(socle_ch) if socle_ch else 'INTROUVABLE'}")
    print(f"  rôles déclarés : {len(lus)} · sans rôle : {len(sans)}")
    print(f"  alertes        : {len(al)}")
    for a in al:
        print(f"    ⚠️  {a}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
