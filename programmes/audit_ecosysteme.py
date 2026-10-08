# -*- coding: utf-8 -*-
# ══════════════════════════════════════════════════════════════
# DÉCIDÉ · outil · Rôle : LE RADAR. Il vérifie chaque soir que l'écosystème
# ne se contredit pas, et il ne fait rien d'autre.
# Quand l'appeler : tâche planifiée de 22h04, tous les jours. Jamais à la main.
#
# ── À QUOI IL SERT, ET CE QU'IL N'EST PAS ─────────────────────────────────
# IL NE FAIT RIEN TOURNER. Il ne collecte aucun cours, ne prend aucune
# position, ne juge aucune stratégie. Il PASSE DES CONTRÔLES sur ce que les
# autres ont produit, et il écrit un rapport. Il ne corrige jamais rien : il
# signale, et un ⚠️ connu et non corrigé doit devenir une action datée, jamais
# un bruit toléré.
#
# CINQ FAMILLES DE CONTRÔLES :
#   ① LES DONNÉES SONT-ELLES COMPLÈTES — cours présents, toutes les valeurs à
#     chaque séance, données du jour fraîches.
#   ② LES CALCULS ONT-ILS BOUGÉ — c'est le maillon 10, le plus important. Il
#     reprend chaque trade clos, redemande au module de refaire le trajet, et
#     compare au journal. IL NE RÉIMPLÉMENTE AUCUNE FORMULE : il importe le
#     module de signal et l'appelle (R-708). Ce qu'il détecte, c'est qu'un
#     résultat enregistré ne correspond PLUS à ce que le calcul produit
#     aujourd'hui — journal écrit par une ancienne version, modifié après coup,
#     ou corrompu. Cas fondateur : du 01/08 au 25/08, le module comptait 85
#     opérations là où la référence en attendait 100, pendant vingt-cinq jours.
#   ③ LES RÈGLES SONT-ELLES RESPECTÉES — jamais plus d'une position vraie-vie
#     à la fois par stratégie, entrée à l'ouverture du lendemain, objectif et
#     stop conformes à la fiche.
#   ④ LA GOUVERNANCE TIENT-ELLE — le compte d'actions correspond-il au tampon,
#     les documents qui font autorité sont-ils présents.
#   ⑤ LES TÂCHES ONT-ELLES TOURNÉ — maillon 18. Chaque tâche a-t-elle laissé
#     sa trace, et à la bonne date.
#
# POURQUOI IL COMPTE PLUS QUE LES AUTRES : c'est le SEUL programme qui
# surveille tous les autres. S'il est aveugle, plus rien ne l'est — et son
# aveuglement ne se voit pas, puisqu'il annonce alors des feux verts.
#
# LE RADAR N'EST JAMAIS FIGÉ : toute brique ajoutée au système appelle une
# vérification ajoutée ici.
#
# CE QUI L'ÉPROUVE : TESTS_AUDIT.py, onze cas, un par défaut déjà rencontré.
# Il REFUSE de valider si l'un tombe. À lancer avant tout dépôt, jamais après.
#
# ── HISTORIQUE DES VERSIONS ───────────────────────────────────────────────
# v2.9 — 29-08-2026 : UN DOCUMENT DECLARE SA DATE EN PREMIER, PAS AU MAXIMUM.
#   Douzieme defaut de la meme famille, et le premier trouve par un JEU
#   D'EPREUVES plutot que par une relecture. La v2.5 lisait bien les quatre
#   premieres lignes d'un document, mais y prenait la date la PLUS RECENTE :
#   si le corps commence tot et cite une date, elle l'emporte sur l'en-tete.
#   Un rapport date du 11-08 etait lu comme du 28-08. La faute etait
#   invisible sur les fichiers reels, ou l'en-tete est seul dans les quatre
#   premieres lignes — elle n'attendait qu'un document un peu plus dense.
# v2.8 — 29-08-2026 : UN MODE INCONNU OU MANQUANT NE PASSE PLUS EN SILENCE.
#   Un mode mal orthographie — « ouvre » au lieu de « ouvré » — faisait
#   compter en CALENDAIRE pendant que le libelle annoncait « ouvre » : le
#   rapport disait une chose et calculait l'autre. Une lettre suffisait.
#   Un mode OUBLIE levait une erreur qui coupait la boucle : les taches
#   declarees apres n'etaient plus controlees DU TOUT, sans un mot.
#   Et le commentaire « on compte en jours ouvres » etait reste alors qu'il
#   n'est plus vrai que pour une tache sur quatre — meme residu que la v2.6
#   avait nettoye au meme endroit.
# v2.7 — 29-08-2026 : LE MODE DE COMPTAGE EST DECLARE PAR TACHE.
#   La v2.6 comptait en jours ouvres pour les QUATRE taches, alors qu'UNE
#   SEULE a un cron « lun-ven » : les trois boucles. L'audit, le cockpit et
#   la mesure de performance tournent 7 jours sur 7.
#   CE QUE CELA COUTAIT : un audit mort le vendredi soir n'aurait ete denonce
#   que le MARDI — quatre jours d'aveuglement sur la tache qui EST le radar.
#   Un correctif juste pour un cas, applique a des cas qui ne le demandaient
#   pas : quatrieme occurrence de cette forme en deux jours, et la premiere
#   en miroir.
# v2.6 — 29-08-2026 : L'AGE SE COMPTE EN JOURS OUVRES.
#   Les trois boucles ont un cron « lun-ven ». Avec un ecart calendaire, le
#   radar aurait denonce CHAQUE DIMANCHE et CHAQUE LUNDI MATIN une tache qui
#   fonctionne — plus les jours feries. Troisieme occurrence en deux jours de
#   la meme forme : l'alerte permanente qui n'apprend rien.
#   Deux nettoyages au passage : le commentaire de la correction ABANDONNEE
#   restait dans le fichier et enseignait la version fausse a qui lisait le
#   code ; et la date du NOM ne court-circuite plus la lecture d'un tableau.
# v2.5 — 29-08-2026 : LA DATE SE LIT AU BON ENDROIT SELON LE FICHIER.
#   Un TABLEAU s'empile : sa date vit en DERNIERE ligne. L'historique des
#   mesures ajoute une ligne par jour ; lire ses premieres lignes rendait le
#   15-08 pour toujours, et l'ecart aurait grandi d'un jour par jour — une
#   alerte permanente sur une tache qui fonctionne, le defaut meme corrige au
#   maillon 14 la veille.
#   Un DOCUMENT REDIGE porte sa date en TETE et cite des dizaines d'autres
#   dates dans son corps. La premiere correction, qui prenait la plus recente
#   du fichier entier, a CASSE ce cas : un rapport vieilli au 15-08 etait
#   annonce « 2 jours ». Reparer une chose en abimant l'autre — c'est le test
#   qui l'a montre, pas la relecture.
#   Les dates POSTERIEURES a aujourd'hui sont ignorees : une echeance n'est
#   pas une trace.
# v2.4 — 28-08-2026 : TROIS CORRECTIONS, chacune eprouvee dans les deux sens.
#   MAILLON 14 — il divisait des OCTETS par un plafond qui n'est pas en octets,
#     et criait « PLACE CRITIQUE » a plus de 100 % chaque soir
#     — 109,5 % releve le 27/08 sur le dossier reconstitue, 139,2 % sur le
#     projet reel le 28/08. Le projet pese 2,78 Mo
#     d'octets quand le compteur du serveur annonce 1,64 M pour un plafond de
#     2 M : si l'unite etait l'octet, le projet aurait cesse d'accepter toute
#     ecriture. L'explication donnee pendant des semaines — « artefact
#     d'execution locale » — etait fausse. Ce maillon INFORME desormais sur le
#     volume et n'alerte plus : la saturation se lit sur la place reelle.
#   MAILLON 18 — AJOUTE. Les deux boucles du matin du 28/08 se sont arretees
#     sans que rien ne le dise. Ce maillon verifie que chaque tache a laisse
#     sa trace, et lit la date DECLAREE dans le nom ou l'en-tete — jamais celle
#     du systeme de fichiers, qui vaut la date du telechargement et aurait mis
#     ce maillon au vert quoi qu'il arrive.
#   FUSEAU — l'age se calcule en Europe/Paris comme le reste du script.
# v2.3 — 28-08-2026 : LES SOUS-DOSSIERS SONT VUS. Le radar lisait la seule racine
#   du projet, or « claude/ » porte les positions ouvertes, le journal des trades,
#   les cours du jour et l'audit du soir. Consequence mesuree : le maillon 10-Trades,
#   le recalcul independant de chaque trade et le controle le plus important de tout
#   le radar, annoncait « Aucun trade cloture — rien a controler » ET PASSAIT AU VERT.
#   Un faux vert ne se voit jamais, contrairement a une alerte. Le defaut etait masque
#   par une compensation ecrite dans le PROMPT de la tache, qui aplatit le projet avant
#   de lancer : elle tenait tant que personne ne reecrivait ce prompt.
#   Verifie sur dossier plat : 22 OK, 12 alertes, 3 erreurs AVANT et APRES — rien casse.
#   Verifie sur arborescence reelle : 18 OK avant, 22 apres — quatre controles retrouves.
# À LANCER À CHAQUE SESSION (rituel). Détecte les dérives avant qu'elles cassent.
# Usage : python3 audit_ecosysteme.py [chemin_projet]
# Sortie : rapport ✅/⚠️/❌ par maillon + score global + fichier daté.
# VERSION 2.0 — Sam 01-08-2026 (Paris). NOM FIXE (R-713) : la version vit dans cet en-tête.
#   Ajouts du 01/08 : alias de valeurs (A-40) · empreinte du golden LUE DANS LE REGISTRE et
#   non plus en dur (A-95/96) · écart de convention de frais distingué de l'écart de calcul
#   (A-15) · prix d'entrée = ouverture (A-13, maillon 12) · creux en cours et 5 pertes
#   consécutives (A-84/A-87, maillon 13) · fraîcheur des données et volume du projet
#   (A-41, maillon 14) · chaîne LOI/HISTOIRE/MOTEUR par stratégie (A-65, maillon 15) ·
#   contrôle du backlog délégué à verif_backlog.py (A-46, maillon 16).
# VERSION 2.1 — Mar 11-08-2026 (Paris). Maillon 10 : compare le recalcul du module au P&L de
#   CONVENTION du journal (pnl_net_convention_eur) quand il existe, pour ne pas confondre une
#   sortie reelle TP_GAP (au-dessus du TP) avec une erreur de calcul (A-175). Le maillon 13
#   (creux/pertes) continue d'utiliser le P&L REEL (pnl_net_eur).
# ══════════════════════════════════════════════════════════════
"""Passe dix-neuf maillons de contrôle sur l'écosystème, affiche un rapport
d'une soixantaine de lignes, et n'en corrige jamais aucun.

① RÔLE — Être le seul programme qui surveille tous les autres. Il ne collecte
  aucun cours, ne prend aucune position, ne juge aucune stratégie : il regarde ce
  que les autres ont produit et dit ce qui ne tient pas. Chaque constat est rangé
  sous un numéro de maillon et porte un signe : ✅ quand c'est bon, ⚠️ quand c'est
  à planifier, ❌ quand c'est bloquant. Exemple relevé le 20-09-2026 à 00h17 heure
  de Paris, sur une copie du dépôt : 55 constats, 42 ✅, 13 ⚠️, 0 ❌, obtenus en
  0,47 seconde. S'il devient aveugle, plus rien ne surveille, et son aveuglement
  ne se voit pas : il annonce alors des feux verts.
② CONTEXTE D'APPEL — Deux appelants, dont un seul est automatique.
  ① Le fichier de tâches planifiées .github/workflows/collecte_abc.yml, pas
  nommé « Passer le radar sur l ecosysteme », qui exécute
  python3 programmes/audit_ecosysteme.py "$GITHUB_WORKSPACE" en redirigeant la
  sortie vers rapports/audit_du_jour.md. Ce fichier se déclenche sur
  cron "0 18 * * 1-5", soit 18h UTC du lundi au vendredi, et le radar est
  l'avant-dernier pas de la chaîne, après la collecte des cours, le versement à
  l'historique, la détection des signaux, la tenue des positions, la publication
  du cockpit, la mesure de performance et la fabrication du pilote.
  ② Jean-Luc ou le Chat, à la main, pour vérifier — et ce cas est reconnu par le
  programme lui-même, qui n'écrit alors aucun fichier de rapport.
③ ENTRÉE — La ligne de commande, un seul argument : le dossier à examiner. Sans
  argument, le programme prend /mnt/project, qui n'existe plus : mesuré le
  20-09-2026, aucun dossier de ce nom sur la machine. Il lit aussi, sans que
  personne ne le lui passe, la variable d'environnement DEPOT_CAC40 et les
  chemins /tmp/depot et /tmp/depot/d, où il va chercher le REGISTRE, le backlog
  et les six fichiers de données du maillon 19.
④ CONDITIONS D'ENTRÉE — Le dossier reçu doit exister ; s'il n'existe pas, le
  programme ne tombe pas, il se contente de ne rien trouver. Le fichier
  programmes/COMMUN.py doit se trouver à côté de ce programme : sans lui, tout
  appel qui doit choisir entre plusieurs fichiers homonymes s'arrête sur
  RuntimeError: COMMUN.le_plus_recent introuvable. C'est ce qui fait tomber trois
  des onze cas de son jeu d'épreuves, qui écrivent leur copie du radar dans le
  dossier temporaire du système, loin de COMMUN.py. Depuis le 27-09-2026, le
  maillon 13 lit aussi programmes/CONTRATS_DES_FICHIERS.py, pour rattacher chaque
  trade à l'identifiant de sa stratégie : s'il manque ou ne se charge pas, le
  radar ne tombe pas, il le dit (⚠️) et tient ses séries sur le nom brut. Depuis
  le 28-09-2026, le maillon 17 y lit aussi les noms d'une stratégie : s'il ne se
  charge pas, le radar le dit (⚠️) et emploie son repli `_noms_17`.
⑤ SORTIE — Un rapport affiché à l'écran, et un code de sortie qui vaut TOUJOURS
  ZÉRO. Le rapport porte trois lignes d'en-tête — titre horodaté, score, rappel
  de la règle — puis un constat par ligne. Mesuré le 20-09-2026 sur une copie du
  dépôt : 61 lignes en tout.
⑥ TRAITEMENT — ① lire l'argument et fixer l'heure de Paris · ② parcourir le
  dossier reçu en écartant archives, .git, __pycache__ et _site_travail, et en
  tirer deux listes, les chemins relatifs et les noms nus · ③ maillon 1, le
  prompt de la boucle est-il présent et couvre-t-il les 39 valeurs · ④ maillon 2,
  le fichier des cours est-il présent et en une seule graphie · ⑤ maillon 4,
  positions ouvertes et journal des trades · ⑥ maillon 5, cockpit et générateur
  de cockpit · ⑦ maillon 6, journal d'apprentissage et registre des stratégies ·
  ⑧ maillon 7, cinq documents de gouvernance · ⑨ maillon 8, une seule version
  vivante du pilote, golden conforme au REGISTRE, et le golden peut-il encore
  arbitrer · ⑩ maillon 10, chaque trade clos est refait par le module de signal
  et comparé au journal · ⑪ maillon 3, toute stratégie en service désigne son
  module et ce module existe · ⑫ maillon 17, états de vie officiels, fiches
  complètes, valeurs jouées dans l'univers déclaré · ⑬ maillon 12, le prix
  d'entrée est-il l'ouverture de la séance · ⑭ maillon 13, creux en cours et
  pertes consécutives · ⑮ maillon 11, un seul jeton par stratégie et objectif de
  gain et perte acceptée conformes au module · ⑯ maillon 14, fraîcheur des cours,
  séances complètes, poids du projet · ⑰ maillon 18, chaque tâche a-t-elle laissé
  sa trace datée · ⑱ maillon 15, chaque stratégie a-t-elle sa ligne au REGISTRE,
  son document et son module · ⑲ maillon 16, le backlog, confié à
  programmes/verif_backlog.py lancé en sous-processus · ⑳ maillon 19, les six
  fichiers de données suivis avancent-ils encore · ㉑ maillon 9, quels fichiers
  aucun contrôle ne regarde · ㉒ afficher le rapport, et l'écrire dans
  rapports/AUDIT_ECOSYSTEME.md seulement si la sortie mène au fichier du rituel.
le module de signal : le programme qui décide quelles valeurs acheter
⑦ UNITÉ — Les constats se comptent en LIGNES DE RAPPORT, une par constat, et les
  maillons sont numérotés de 1 à 19. Les âges de traces se comptent en JOURS,
  ouvrés pour la boucle du jour et calendaires pour les autres tâches déclarées
  au maillon 18 (deux depuis le 30-09-2026, le cockpit n'y étant plus). Les
  écarts de recalcul des trades sont en EUROS, avec un seuil à 25. Le poids du
  projet est en OCTETS. Les empreintes sont des nombres hexadécimaux de 16
  caractères. L'horodatage du rapport est en heure de Paris.
⑧ POURQUOI — Il ne réimplémente aucune formule : pour refaire un trade clos, il
  importe le vrai module de signal et l'appelle, parce que deux écritures d'un
  même calcul divergent toujours (R-708). Et il ne lit jamais la date que le
  système de fichiers donne à un fichier : il lit celle que le fichier déclare,
  dans son nom ou dans son en-tête. La raison est mesurée le 28-08-2026 : la
  tâche du soir commençait par recopier tout le projet, et chaque fichier
  arrivait avec la date du téléchargement — un rapport du 20-08 portait une date
  de fichier du 23, puis du 28 après recopie. Le contrôle des traces aurait été
  au vert quoi qu'il arrive.
⑨ CE QUI CLOCHE — sept points, tous mesurés le 20-09-2026 sur une copie du dépôt :
  ① LE CODE DE SORTIE VAUT ZÉRO MÊME QUAND UN CONTRÔLE EST BLOQUANT, ET LE PAS
  DU SOIR RESTE VERT. Le programme ne se termine jamais par une instruction de
  sortie : il s'arrête en bas de fichier, donc en code 0. Mesuré en retirant
  gouvernance/PILOTE.md d'une copie : le rapport affiche
  Score : 41 ✅ · 13 ⚠️ · 1 ❌ et le code de sortie reste 0. Le pas du fichier de
  tâches planifiées écrit pourtant if [ "$CODE" -ne 0 ]; then echo "::error::" —
  cette condition ne s'est jamais réalisée et ne peut pas se réaliser. Un
  contrôle qui n'a pas pu conclure doit rendre un code de sortie non nul (R-734).
  ② LE GOLDEN EST COMPARÉ AU TÉMOIN DU GOLDEN, PAS AUX DONNÉES VIVANTES, ET LE FILET
  ANTI-RÉGRESSION EST VERT PAR CONSTRUCTION. Le contrôle cherche les fichiers
  dont le nom contient cac40_ohlcv et prend le DERNIER de la liste triée. Or deux
  fichiers portent ce motif : donnees/cac40_ohlcv.csv, les données vivantes, et
  temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv, la copie figée du jeu
  qui a servi à prendre le golden. C'est la seconde qui est prise. Mesuré :
  empreinte du témoin e472c09da5679ec3, empreinte des données vivantes
  10e71dc94aed4ef2, empreinte attendue par le golden e472c09da5679ec3. Le rapport
  annonce donc Le golden peut arbitrer : empreinte des donnees conforme, et il
  l'annoncera toujours, puisqu'un témoin du golden figé ne change jamais. Le commentaire
  posé juste au-dessus décrit exactement cette faute et ne la corrige que pour le
  fichier du golden, pas pour le fichier de données.
  ③ LE MAILLON 19 MESURE UN AUTRE DÉPÔT QUE CELUI QU'ON LUI DONNE. Il cherche un
  dossier donnees dans cet ordre : la variable DEPOT_CAC40, puis /tmp/depot, puis
  /tmp/depot/d, et seulement ensuite le dossier reçu. Mesuré : lancé sur
  /tmp/cwlot7b, il annonce
  claude_cours_nouveaux N'AVANCE PLUS : dernière date 2026-09-11, 9 jours, alors
  que /tmp/cwlot7b/donnees/claude_cours_nouveaux.csv porte 2026-09-18 — sept
  jours d'écart. Il lisait /tmp/depot, une autre copie présente sur la machine.
  Les maillons 7, 15 et 16 ont la même porte : le REGISTRE relevé était
  /tmp/depot/gouvernance/REGISTRE_REGLES.md et le backlog
  /tmp/depot/BACKLOG_DECISIONS.md.
  ④ DEUX MAILLONS SE CONTREDISENT DANS LE MÊME RAPPORT. Mesuré sur la copie privée
  de gouvernance/PILOTE.md : le maillon 7 affiche ✅ PILOTE présent, parce qu'il
  se contente d'un nom de fichier et que gouvernance/PILOTE_SOCLE.md porte ce nom,
  pendant que le maillon 8 affiche ❌ PILOTE : AUCUN document ne se déclare
  FABRIQUÉ à sa première ligne non vide. Le lecteur n'a aucun moyen de savoir
  lequel des deux dit vrai.
  ⑤ TOUT LE TRAVAIL EST ÉCRIT AU NIVEAU DU FICHIER, SANS FONCTION PRINCIPALE ET
  SANS GARDE. Il n'y a ni main ni if __name__ == "__main__" : les dix-neuf
  maillons sont du code posé à la suite, entre la ligne 339 et la ligne 1457.
  Conséquence mesurée : importer ce fichier depuis un autre programme exécute
  l'audit entier, affiche le rapport et peut écrire rapports/AUDIT_ECOSYSTEME.md.
  Aucun maillon ne peut être appelé ni éprouvé séparément, et c'est pourquoi son
  jeu d'épreuves programmes/TESTS_AUDIT.py ne peut le juger que sur le texte
  qu'il affiche.
  ⑥ LE RÉSUMÉ DU MAILLON 16 NE PORTE AUCUN CHIFFRE. Il prend pour résumé la
  DERNIÈRE ligne affichée par programmes/verif_backlog.py. Mesuré : cette ligne
  vaut tampon que tu as toi-même écrit. Divergence = le dépôt n'a pas pris. —
  un morceau de phrase adressé au Chat. Le rapport du soir affiche donc
  ✅ [16-Backlog] Backlog contrôlé par verif_backlog.py — tampon que tu as
  toi-même écrit, et le compte d'actions, qui est l'information attendue, reste
  trois lignes plus haut dans une sortie que personne ne lit.
  ⑦ LE MAILLON 9 DÉNONCE 97 FICHIERS D'UN COUP ET N'EN NOMME QUE HUIT. Mesuré :
  ⚠️ [9-MétaRadar] 97 fichier(s) non surveillé(s) par le radar, suivi de huit noms
  et de trois points. La liste des motifs couverts est une énumération écrite à la
  main de 61 entrées, dont trouve, audit_ecosysteme, trading_journal et
  journal_trades figurent chacun deux fois. Une alerte qui revient chaque soir
  avec le même chiffre n'apprend rien, et une alerte qu'on apprend à ignorer cesse
  de protéger.
⑩ EFFET — CRÉE le dossier rapports là où vit le programme, ou à défaut dans le
  dossier reçu, à chaque passage. ÉCRIT rapports/AUDIT_ECOSYSTEME.md, et
  seulement quand sa sortie standard mène au fichier du rituel
  rapports/audit_du_jour.md. COPIE le backlog dans le dossier temporaire du
  système sous le nom _bl_audit.md et LANCE programmes/verif_backlog.py dessus,
  lequel réécrit cette copie ; l'original n'est pas touché. IMPORTE ET EXÉCUTE le
  module de signal MODULE_C5_ETENDU_10, dont le code s'exécute entièrement.
  Affiche une soixantaine de lignes. Aucun accès réseau. Ne modifie aucun fichier
  de données : vérifié le 20-09-2026 en comparant la somme de contrôle des 245
  fichiers d'une copie du dépôt avant et après un passage, aucune différence.
⑪ TERMINAISON — SORT DU PROGRAMME en arrivant au bas du fichier, donc avec le
  code 0, quel que soit le nombre de constats bloquants. PEUT S'ARRÊTER AVANT
  D'AVOIR RIEN AFFICHÉ sur une erreur non rattrapée : c'est le cas quand
  programmes/COMMUN.py est absent et qu'un choix entre homonymes se présente, et
  le rapport est alors entièrement perdu puisqu'il n'est affiché qu'à la fin. Et
  un de ses appels peut ne pas revenir : il importe et exécute le module de
  signal, et il lance programmes/verif_backlog.py en sous-processus, avec une
  limite de 60 secondes qui le protège d'une attente sans fin.
⑫ DÉFINITIONS
  le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir,
    qui contrôle l'ensemble du système et range chacun de ses constats sous un
    numéro de maillon, par exemple 18-Tâches pour le contrôle des traces
    laissées par les tâches planifiées.
  un maillon : un groupe de contrôles du radar, désigné par un numéro et un
    nom, par exemple 18-Tâches pour le contrôle des traces laissées par les
    tâches planifiées.
  un constat : une ligne du rapport, portant un signe, un numéro de maillon et une
    phrase
  le projet : le dossier reçu sur la ligne de commande, celui que le radar examine
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
    étant qu'une copie de lecture
  une trace : le fichier qu'une tâche planifiée laisse derrière elle quand
    elle a tourné — rapport de boucle, rapport d'audit, cockpit, historique
    des mesures.
  la date déclarée : la date qu'un fichier porte dans son nom ou dans son contenu,
    par opposition à celle que le système de fichiers lui donne
  la boucle du jour : la tâche planifiée qui collecte les cours et écrit le
    rapport de boucle, du lundi au vendredi seulement.
  le golden : le fichier gouvernance/golden_tests_*.json, qui fige des
    chiffres de référence ; tout écart à données identiques est une
    régression.
  le témoin du golden : la copie conservée des cours qui ont produit les chiffres figés, `temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv`.
  le REGISTRE : gouvernance/REGISTRE_REGLES.md, le document qui porte les
    règles numérotées du projet
  le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions et
    des actions du projet
  un jeton : la comptabilité où une seule position peut être ouverte à la fois par stratégie ; un signal reçu pendant une position est ignoré.
  le Chat : la conversation qui rédige la gouvernance du projet et dépose ses
    versions
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
  le fichier des cours : donnees/cac40_ohlcv.csv, l'historique des cours de
    clôture qui sert de référence validée
"""
import os, sys, json, csv, re
from datetime import datetime
from zoneinfo import ZoneInfo

PROJ = sys.argv[1] if len(sys.argv) > 1 else "/mnt/project"
now = datetime.now(ZoneInfo('Europe/Paris'))
J = ['Lun','Mar','Mer','Jeu','Ven','Sam','Dim']
# `TS` retire le 17-09-2026 : il fabriquait le nom horodate du rapport,
# abandonne au profit d un nom fixe. Une seule occurrence restait — sa
# propre definition. **Du code mort derriere une correction se lit comme du
# code vivant par qui arrive ensuite.**
TSH = J[now.weekday()] + now.strftime(' %d-%m-%Y %Hh%M') + ' (Paris)'

# LES SOUS-DOSSIERS COMPTENT — mesuré le 28-08-2026, et c'est le défaut le plus
# grave du radar. Le dossier « claude/ » porte les positions ouvertes, le journal
# des trades, les cours du jour et l'audit du soir. Avec os.listdir, le maillon
# 10-Trades — le recalcul indépendant de chaque trade, le contrôle le plus
# important de tout le radar — passait au VERT en annonçant « aucun trade
# clôturé, rien à contrôler ». Il ne contrôlait rien et le disait comme un succès.
# Cela ne se voyait pas grâce à une compensation écrite dans le PROMPT de la
# tâche, qui aplatit le projet avant de lancer : elle tient tant que personne ne
# réécrit ce prompt. Le correctif appartient au code, pas au prompt.
#
# DEUX LISTES, DEUX USAGES, et la distinction est nécessaire :
#   _chemins  = chemins RELATIFS — c'est ce que trouve() rend, pour que
#               os.path.join(PROJ, f) ouvre réellement le fichier.
#   fichiers  = NOMS SEULS — les contrôles existants testent l'appartenance
#               exacte et des débuts de nom ; leur donner des chemins les
#               casserait en silence.
# ─── CE QUI N'EST PAS DU VIVANT N'ENTRE JAMAIS ICI ───
# Posé le 12-09-2026 après relecture de Cowork. La correction de la veille a appris
# au radar à descendre dans les sous-dossiers — et l'a fait passer d'AVEUGLE à
# INDISCRIMINÉ, ce qui est plus traître : il arrive avec l'air d'un radar réparé.
# Mesuré par Cowork sur un clone neuf :
#   · `chemin_de(golden_tests_…json)` rendait `archives/golden…` et non
#     `gouvernance/golden…` — le tri alphabétique met `archives/` en premier.
#     LA v16 PRESCRIT DE RANGER LES VERSIONS ANTÉRIEURES EN `archives/` : la
#     fonction transformait ce rangement en piège, et sur le GOLDEN, le fichier
#     de référence figé dont tout écart bloque une livraison.
#   · le radar parcourait `.git/` : 28 fichiers, 2 770 582 octets — un quart du
#     poids annoncé par 14-Taille n'existait pas, et `9-MétaRadar` comptait
#     `HEAD`, `config`, `index` parmi ses « fichiers non surveillés ».
#   · « 9 versions du PILOTE » n'en étaient pas neuf : quatre archives, deux
#     prompts, le SOCLE écrit à la main, et le PROGRAMME qui fabrique le pilote.
#     UNE SEULE version vivante. La correction avait fabriqué sa propre alerte.
# L'EXCLUSION PORTE SUR UNE PROPRIÉTÉ, À UN SEUL ENDROIT — pas six rustines.
_NON_VIVANT = ("archives", ".git", "__pycache__", "_site_travail")

def _est_vivant(rel):
    """Un chemin relatif traverse-t-il un dossier que le radar doit ignorer ?

    ① RÔLE — Tenir à l'écart du radar tout ce qui n'est pas du vivant, pour qu'il ne
      contrôle jamais une version rangée aux archives ni un fichier interne à git.
      Sans ce filtre, le radar est passé d'AVEUGLE à INDISCRIMINÉ, ce qui est plus
      traître : il arrive avec l'air d'un radar réparé. Trois conséquences mesurées
      par Cowork le 12-09-2026 sur un clone neuf — le chemin du golden rendu était
      archives/golden au lieu de gouvernance/golden, parce que le tri alphabétique
      met archives en premier · le radar comptait 28 fichiers et 2 770 582 octets du
      dossier .git, soit un quart du poids qu'il annonçait, et rangeait HEAD, config
      et index parmi les fichiers non surveillés · il annonçait 9 versions du pilote
      là où il n'en vivait qu'UNE, les huit autres étant quatre archives, deux
      prompts, un document écrit à la main et le programme qui fabrique le pilote.
    ② CONTEXTE D'APPEL — Le parcours du dossier reçu, au démarrage du programme, une
      fois par fichier rencontré. Mesuré le 20-09-2026 sur une copie du dépôt : 245
      chemins retenus. Jamais appelée ailleurs.
    ③ ENTRÉE — `rel` : le chemin d'un fichier, relatif au dossier examiné, par exemple
      gouvernance/PILOTE.md ou archives/PILOTE_ancien.md. Un seul appelant, le
      parcours du dossier, qui le construit à partir du chemin complet.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un texte vide, un chemin absolu ou un chemin
      écrit avec des barres obliques inversées ne la font pas tomber : les barres
      inversées sont converties avant la découpe.
    ⑤ SORTIE — UNE valeur : vrai quand aucun dossier traversé ne figure dans la liste
      des dossiers écartés, faux sinon.
      [rend: 1]
    ⑥ TRAITEMENT — ① remplacer les barres obliques inversées par des barres droites ·
      ② découper le chemin en segments · ③ écarter le dernier segment, qui est le nom
      du fichier · ④ rendre faux si l'un des segments restants est archives, .git,
      __pycache__ ou _site_travail.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — L'exclusion porte sur une propriété du chemin et vit à un seul
      endroit, plutôt que d'être répétée dans chaque maillon qui pourrait en souffrir.
      Le code l'écrit ainsi : six rustines posées à six endroits
      divergent, une propriété posée une fois ne divergera pas.
    ⑨ CE QUI CLOCHE — deux points, tous deux mesurés le 20-09-2026 :
      ① Le filtre épelle des noms de dossiers. La liste écartée est une énumération de
      quatre noms écrits à la main. Un dossier rangé demain sous le nom vieux,
      obsolete ou sauvegarde y échapperait, et ses fichiers redeviendraient des
      candidats à la place du vivant. Le critère qui tranche tient en une question :
      si je renomme un dossier, mon contrôle change-t-il d'avis ? Ici oui, donc il
      épelle.
      ② Le dernier segment est écarté sans vérifier que c'est bien un nom de fichier.
      Mesuré : appelée sur le texte .git, elle rend VRAI, parce que .git y est le
      dernier segment. Le parcours du dossier ne lui donne jamais un chemin de cette
      forme — il écarte les dossiers avant de descendre — mais rien dans la fonction
      ne l'impose, et un second appelant ajouté demain n'aurait aucun moyen de le
      savoir.
    ⑩ EFFET — N'écrit aucun fichier, ne lit aucun fichier, n'affiche rien, ne touche
      pas au réseau. Elle ne fait que regarder un texte.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels ne se
      termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque
        soir, qui contrôle l'ensemble du système et range chacun de ses
        constats sous un numéro de maillon, par exemple 18-Tâches pour le
        contrôle des traces laissées par les tâches planifiées.
      un maillon : un groupe de contrôles du radar, désigné par un numéro et
        un nom, par exemple 18-Tâches pour le contrôle des traces laissées par
        les tâches planifiées.
      le golden : le fichier gouvernance/golden_tests_*.json, qui fige des
        chiffres de référence ; tout écart à données identiques est une
        régression.
      le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui
        dit ou en est le projet, ce qu'il contient et ce qui cloche
      Cowork : le relecteur du projet, qui clone le dépôt, casse le code et
        rend ses cassures par écrit
      le Chat : la conversation qui rédige la gouvernance du projet et dépose ses
        versions
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    return not any(p in _NON_VIVANT for p in rel.replace("\\", "/").split("/")[:-1])

# ─── LE PLUS RÉCENT SE LIT DANS LA DATE, JAMAIS DANS L'ALPHABET ───
# Jean-Luc, 12-09-2026 : « il regarde la date de création la plus fraîche ? »
# NON — le radar prenait `sorted(...)[-1]`, le dernier par ordre ALPHABÉTIQUE.
# Les noms commencent par le jour de la semaine : sur REGISTRE_Jeu_30-07,
# _Sam_01-08, _Ven_05-09 et _Mar_09-09, l'alphabet rend le 05-09 quand le plus
# récent est le 09-09. PROUVÉ. La fonction vit dans COMMUN (R-708) et se calibre
# sur ce cas même.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
try:
    from COMMUN import le_plus_recent as _le_plus_recent
except Exception:
    def _le_plus_recent(c):
        """Refuse de choisir entre plusieurs fichiers quand le vrai choix est indisponible.

        ① RÔLE — Faire tomber le radar bruyamment plutôt que le laisser choisir un fichier
          au hasard. La vraie fonction vit dans programmes/COMMUN.py et retient, parmi
          plusieurs fichiers homonymes, celui dont le NOM porte la date la plus récente.
          Celle-ci la remplace quand ce voisin est introuvable, et elle ne fait qu'une
          chose : lever. Sans ce refus, le programme retomberait sur le dernier par ordre
          alphabétique, qui est faux : les noms du projet commencent par le jour de la
          semaine, et sur REGISTRE_Jeu_30-07, _Sam_01-08, _Ven_05-09 et _Mar_09-09,
          l'alphabet rend le 05-09 quand le plus récent est le 09-09.
        ② CONTEXTE D'APPEL — Elle n'est définie QUE si l'import de programmes/COMMUN.py
          échoue, et elle est alors appelée à deux endroits : le choix du backlog quand
          plusieurs fichiers portent ce nom, et le choix du fichier à mesurer pour chacun
          des six fichiers de données suivis au maillon 19. Mesuré le 20-09-2026 sur une
          copie du dépôt : l'import réussit, donc cette version n'est jamais appelée.
        ③ ENTRÉE — `c` : la liste des fichiers entre lesquels il faudrait choisir. Le
          paramètre n'est pas regardé : la fonction lève avant de s'en servir.
        ④ CONDITIONS D'ENTRÉE — Aucune.
        ⑤ SORTIE — Ne rend rien : elle lève dans tous les cas.
          [rend: rien]
        ⑥ TRAITEMENT — ① lever une erreur portant le message COMMUN.le_plus_recent
          introuvable — le radar refuse de choisir un fichier au hasard alphabetique.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Un repli silencieux sur l'ordre alphabétique rendrait un fichier
          plausible et faux, et personne ne le saurait. Un arrêt net se voit. C'est la
          différence entre une panne et un silence, et c'est le silence que ce programme
          entier cherche à empêcher.
        ⑨ CE QUI CLOCHE — un point, mesuré le 20-09-2026. L'arrêt ne survient pas au
          moment où le voisin manque, mais plus tard, au premier choix entre homonymes —
          et il arrive alors que le rapport soit à moitié calculé, sans qu'une seule ligne
          n'ait été affichée, puisque l'affichage n'a lieu qu'à la toute fin. C'est ce qui
          fait tomber trois des onze cas de programmes/TESTS_AUDIT.py : leur copie du
          radar est écrite dans le dossier temporaire du système, elle n'y trouve pas
          programmes/COMMUN.py, elle s'arrête sur RuntimeError: COMMUN.le_plus_recent
          introuvable, et les trois cas annoncent lignes absentes comme si le radar avait
          perdu la vue.
        ⑩ EFFET — N'écrit aucun fichier, n'affiche rien, ne touche pas au réseau.
        ⑪ TERMINAISON — LÈVE toujours une erreur, qui n'est rattrapée nulle part et
          ARRÊTE DONC LE PROGRAMME. Aucun de ses appels ne se termine : elle n'en fait
          aucun.
          [sort: oui]
        ⑫ DÉFINITIONS
          le radar : le programme programmes/audit_ecosysteme.py, lancé chaque
            soir, qui contrôle l'ensemble du système et range chacun de ses
            constats sous un numéro de maillon, par exemple 18-Tâches pour le
            contrôle des traces laissées par les tâches planifiées.
          le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des
            décisions et des actions du projet
          un maillon : un groupe de contrôles du radar, désigné par un numéro
            et un nom, par exemple 18-Tâches pour le contrôle des traces
            laissées par les tâches planifiées.
        """
        raise RuntimeError("COMMUN.le_plus_recent introuvable — le radar refuse de "
                           "choisir un fichier au hasard alphabetique")

_chemins = []
if os.path.isdir(PROJ):
    for _d, _sd, _fs in os.walk(PROJ):
        _sd[:] = [x for x in _sd if x not in _NON_VIVANT]   # on n'y descend même pas
        for _f in _fs:
            _rel = os.path.relpath(os.path.join(_d, _f), PROJ)
            if _est_vivant(_rel):
                _chemins.append(_rel)
_chemins.sort()
fichiers = [os.path.basename(p) for p in _chemins]
# A-40 — alias de valeurs : un même titre porte plusieurs noms selon la source.
# Table unique, à compléter ici et NULLE PART AILLEURS (R-708).
ALIAS_VALEURS = {
    "unibail_rodamco": "unibail_rodamco_westfield",
    "unibail": "unibail_rodamco_westfield",
}
def _norm(s):
    # tolère espaces, tirets et underscores indifféremment (Cowork voit des espaces,
    # le Chat voit des underscores — même fichier, nommage différent selon le lecteur)
    """Ramène un texte à une forme unique, pour que deux graphies se rencontrent.

    ① RÔLE — Permettre à tout le radar de rapprocher deux écritures d'un même nom. Un
      même fichier est nommé différemment selon celui qui le regarde : Cowork voit des
      espaces, le Chat voit des soulignés, et le fichier maître des cours existe
      depuis toujours avec un espace alors que plusieurs programmes l'écrivent avec un
      souligné. Sans ce passage par une forme unique, le radar croirait à deux
      fichiers distincts et n'en contrôlerait qu'un.
    ② CONTEXTE D'APPEL — Partout dans le programme, dès qu'un nom est comparé à un
      autre : la normalisation des noms de valeurs, la recherche de fichiers par
      motif, la recherche du REGISTRE dans un dossier, la recherche du backlog, le
      choix du module de signal, la comparaison du nom du golden à celui du REGISTRE,
      le relevé des traces du maillon 18 et la liste des fichiers non surveillés du
      maillon 9.
    ③ ENTRÉE — `s` : le texte à ramener à sa forme unique, par exemple
      cac40 ohlcv.csv ou MODULE_C5_ETENDU_10.
    ④ CONDITIONS D'ENTRÉE — `s` doit être un texte. Un texte vide est accepté et rend
      un texte vide.
    ⑤ SORTIE — UNE valeur : le texte mis en minuscules, où toute suite d'espaces, de
      tirets et de soulignés devient un souligné unique. Mesuré le 20-09-2026 :
      A -_ B devient a_b.
      [rend: 1]
    ⑥ TRAITEMENT — ① mettre le texte en minuscules · ② remplacer toute suite
      d'espaces, de tirets et de soulignés par un seul souligné.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les trois séparateurs sont tenus pour équivalents plutôt que d'en
      imposer un seul, parce que le radar ne choisit pas les noms qu'il lit : il les
      reçoit d'un dépôt, d'un tableur et de deux rédacteurs humains. Exiger une
      graphie ferait rendre un constat bloquant sur un fichier parfaitement sain, ce
      qui est arrivé au maillon 2 avant sa correction.
    ⑨ CE QUI CLOCHE — deux points :
      ① Elle n'a pas de texte explicatif et porte seulement un commentaire de deux
      lignes, alors qu'elle est appelée par presque tous les maillons. C'est la
      fonction la plus employée du programme et la moins expliquée.
      ② Elle ne touche pas aux lettres accentuées : SÉANCE et SEANCE restent deux
      textes différents après passage. Aucun nom de fichier du dépôt ne porte
      d'accent le 20-09-2026, donc le cas ne s'est jamais présenté ; le jour où il se
      présentera, le rapprochement échouera sans un mot.
    ⑩ EFFET — N'écrit aucun fichier, n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main. PEUT LEVER si on lui passe autre chose qu'un texte,
      par exemple None. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque
        soir, qui contrôle l'ensemble du système et range chacun de ses
        constats sous un numéro de maillon, par exemple 18-Tâches pour le
        contrôle des traces laissées par les tâches planifiées.
      un maillon : un groupe de contrôles du radar, désigné par un numéro et
        un nom, par exemple 18-Tâches pour le contrôle des traces laissées par
        les tâches planifiées.
      une graphie : l'une des façons dont un même nom de fichier est écrit
        selon le canal par lequel on le lit — avec espaces ou tirets bas, avec
        ou sans accents
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
      le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions
        et des actions du projet
      le golden : le fichier gouvernance/golden_tests_*.json, qui fige des
        chiffres de référence ; tout écart à données identiques est une
        régression.
      Cowork : le relecteur du projet, qui clone le dépôt, casse le code et
        rend ses cassures par écrit
      le Chat : la conversation qui rédige la gouvernance du projet et dépose ses
        versions
      un constat : une ligne du rapport, portant un signe, un numéro de maillon
        et une phrase
    
      le rapprochement : le fait de reconnaître que deux écritures différentes désignent le même fichier ou la même entreprise
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    return re.sub(r"[ \-_]+", "_", s.lower())
def _norm_val(s):
    """Ramène un nom d'entreprise à sa forme unique, en appliquant la table des alias.

    ① RÔLE — Faire qu'une même entreprise écrite de deux façons dans deux fichiers ne
      passe pas pour deux sociétés distinctes. UNIBAIL_RODAMCO dans le journal des
      trades et UNIBAIL_RODAMCO_WESTFIELD dans l'historique des cours désignent la
      même valeur : sans ce rapprochement, le maillon qui refait chaque trade clos ne
      trouve pas les cours de la séance d'entrée et range le trade parmi les non
      vérifiables. Le contrôle le plus important du radar se tait alors sans qu'aucune
      erreur ne s'affiche.
    ② CONTEXTE D'APPEL — Cinq endroits, tous des maillons qui rapprochent deux
      fichiers : la construction des séries de cours par valeur et la lecture du nom
      de la valeur d'un trade au maillon 10, le contrôle du prix d'entrée au maillon
      12, le rapprochement de l'univers déclaré et des valeurs jouées au maillon 17,
      et le comptage des valeurs par séance au maillon 14.
    ③ ENTRÉE — `s` : le nom d'une entreprise tel qu'un fichier l'écrit, par exemple
      UNIBAIL-RODAMCO, Air Liquide ou BUREAU_VERITAS.
    ④ CONDITIONS D'ENTRÉE — `s` doit être un texte. Un texte vide est accepté et rend
      un texte vide.
    ⑤ SORTIE — UNE valeur : le nom mis à sa forme unique, puis remplacé par son alias
      quand la table en connaît un. Mesuré le 20-09-2026 : UNIBAIL-RODAMCO rend
      unibail_rodamco_westfield, Air Liquide rend air_liquide.
      [rend: 1]
    ⑥ TRAITEMENT — ① ramener le nom à sa forme unique, minuscules et séparateurs
      confondus · ② chercher cette forme dans la table des alias · ③ rendre l'alias
      s'il existe, sinon la forme obtenue.
    ⑦ UNITÉ — Une VALEUR, c'est-à-dire une entreprise cotée.
    ⑧ POURQUOI — La table des alias vit à un seul endroit, juste au-dessus de la
      fonction, et le code impose de la compléter là et nulle part ailleurs : deux
      tables de correspondance entretenues en parallèle divergent toujours (R-708).
      Elle compte deux entrées le 20-09-2026, unibail_rodamco et unibail, qui mènent
      toutes deux à unibail_rodamco_westfield.
    ⑨ CE QUI CLOCHE — deux points, mesurés le 20-09-2026 :
      ① La table est une énumération écrite à la main, et elle ne se remplit que
      lorsqu'une divergence a déjà coûté quelque chose. Rien ne signale une valeur
      écrite de deux façons tant que personne n'ajoute la ligne : le rapprochement
      échoue en silence et les trades concernés sont simplement comptés parmi les non
      vérifiables. Le rapport du 20-09-2026 ne porte aucune ligne de ce genre, mais
      rien ne garantit qu'il n'y en aura pas demain.
      ② L'identité d'une valeur se joue sur le MNÉMONIQUE et jamais sur le nom, et
      cette fonction travaille sur le nom. Le fichier
      donnees/REFERENTIEL_VALEURS_v3_Lun_17-08-2026_10h54.csv porte la correspondance
      entre les deux, et le maillon 17 l'emploie ; les maillons 10, 12 et 14 ne
      l'emploient pas et s'en remettent à cette table de deux lignes.
    ⑩ EFFET — N'écrit aucun fichier, n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main. PEUT LEVER si on lui passe autre chose qu'un texte.
      Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque
        soir, qui contrôle l'ensemble du système et range chacun de ses
        constats sous un numéro de maillon, par exemple 18-Tâches pour le
        contrôle des traces laissées par les tâches planifiées.
      un maillon : un groupe de contrôles du radar, désigné par un numéro et
        un nom, par exemple 18-Tâches pour le contrôle des traces laissées par
        les tâches planifiées.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée
        dans les fichiers du projet
      un trade : une opération simulée, de l'achat à la revente
      l'univers : la liste des valeurs sur lesquelles une stratégie a le droit d'acheter, désignées par leur mnémonique
    
      la table : `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740, qui porte les neuf seuils et le sens de comparaison de chacun
      le rapprochement : le fait de reconnaître que deux écritures différentes désignent le même fichier ou la même entreprise
"""
    k = _norm(s)
    return ALIAS_VALEURS.get(k, k)
def trouve(motif):
    """Rend les chemins de tous les fichiers dont le nom contient un motif.

    ① RÔLE — Donner à chaque maillon la liste des fichiers qui l'intéressent, sans
      qu'aucun d'eux n'ait à savoir dans quel sous-dossier ils sont rangés. C'est la
      porte d'entrée de presque tous les contrôles : le maillon 2 lui demande les
      fichiers de cours, le maillon 7 les documents de gouvernance, le maillon 18 les
      traces des tâches.
    ② CONTEXTE D'APPEL — Une trentaine d'endroits, répartis dans presque tous les
      maillons, plus trois fonctions du programme : la fonction qui répond par oui ou
      non à la même question, celle qui choisit le backlog quand le dépôt est
      introuvable, celle qui choisit le REGISTRE dans le même cas, et celle qui lit un
      fichier de tableur.
    ③ ENTRÉE — `motif` : le fragment de nom cherché, par exemple cac40_ohlcv, golden
      ou BACKLOG_DECISIONS. La casse, les espaces, les tirets et les soulignés sont
      indifférents.
    ④ CONDITIONS D'ENTRÉE — `motif` doit être un texte. Le parcours du dossier doit
      avoir eu lieu, ce qui est toujours vrai puisqu'il se fait au démarrage du
      programme, avant toute définition de fonction appelable.
    ⑤ SORTIE — UNE valeur : la liste des chemins RELATIFS au dossier examiné, triés
      par ordre alphabétique. Liste VIDE quand aucun fichier ne correspond. Mesuré le
      20-09-2026 sur une copie du dépôt : trouve appelée avec cac40_ohlcv rend deux
      chemins, donnees/cac40_ohlcv.csv et
      temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv.
      [rend: 1]
    ⑥ TRAITEMENT — ① ramener le motif à sa forme unique · ② parcourir les chemins
      relevés au démarrage · ③ garder ceux dont le NOM NU, ramené à sa forme unique,
      contient le motif.
    ⑦ UNITÉ — Un NOMBRE DE FICHIERS.
    ⑧ POURQUOI — Elle rend des chemins relatifs et non des noms nus, pour que
      l'appelant puisse réellement ouvrir le fichier. Le texte d'origine de cette
      fonction ajoutait « le rapprochement des graphies est inchangé : espaces,
      tirets et soulignés restent équivalents (R-719) » ; le rapprochement est bien
      celui-là, mais le code cité ne correspond pas — R-719 pose qu'on ne nomme un
      fichier qu'après l'avoir affiché. La phrase est rapportée ici telle qu'elle
      était, sans être reprise à son compte, parce que rien ne se supprime sans
      accord (R-751 ⑩). La distinction est nécessaire et
      le code la pose : les contrôles écrits avant le 28-08-2026 testaient
      l'appartenance exacte d'un nom à une liste, et leur donner des chemins les
      aurait cassés en silence. C'est pourquoi le programme tient DEUX listes, les
      chemins pour ouvrir et les noms nus pour comparer.
    ⑨ CE QUI CLOCHE — deux points, tous deux mesurés le 20-09-2026 :
      ① LE MOTIF ATTRAPE AUSSI CE QUI PARLE DU FICHIER CHERCHÉ, ET UN MAILLON S'EN
      TROUVE FAUSSÉ. Appelée avec golden, elle rend deux chemins :
      gouvernance/golden_tests_Sam_01-08-2026_20h19.json, qui est le golden, et
      temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv, qui n'est qu'un
      tableur. Appelée avec cockpit, elle rend cinq chemins dont
      etudes/ANALYSE_COCKPIT_Ven_14-08-2026_00h19.md, un document qui parle du
      cockpit. Un appelant qui prend le dernier de la liste prend donc souvent le
      mauvais fichier : c'est ainsi que le contrôle du golden finit par mesurer le
      témoin du golden au lieu des données vivantes.
      ② Le tri est alphabétique et il porte sur le chemin entier, dossier compris. Un
      appelant qui veut le fichier le plus récent ne peut donc rien en tirer : c'est
      exactement la faute que le projet a corrigée le 12-09-2026 en posant une
      fonction qui lit la date du nom, et cette fonction n'est employée qu'à deux
      endroits du radar.
    ⑩ EFFET — N'écrit aucun fichier, n'ouvre aucun fichier, n'affiche rien, ne touche
      pas au réseau : elle ne regarde que la liste de chemins relevée au démarrage.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas sur un motif absent, elle
      rend une liste vide. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque
        soir, qui contrôle l'ensemble du système et range chacun de ses
        constats sous un numéro de maillon, par exemple 18-Tâches pour le
        contrôle des traces laissées par les tâches planifiées.
      un maillon : un groupe de contrôles du radar, désigné par un numéro et
        un nom, par exemple 18-Tâches pour le contrôle des traces laissées par
        les tâches planifiées.
      le golden : le fichier gouvernance/golden_tests_*.json, qui fige des
        chiffres de référence ; tout écart à données identiques est une
        régression.
      le témoin du golden : la copie conservée des cours qui ont produit les chiffres figés, `temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv`.
      le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions
        et des actions du projet
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand
        elle a tourné — rapport de boucle, rapport d'audit, cockpit,
        historique des mesures.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
      un motif : un morceau de nom passé à une fonction de recherche, par
        exemple trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
    
      le rapprochement : le fait de reconnaître que deux écritures différentes désignent le même fichier ou la même entreprise
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    m = _norm(motif)
    return [p for p in _chemins if m in _norm(os.path.basename(p))]
def existe(motif):
    """Dit si au moins un fichier du projet porte ce motif dans son nom.

    ① RÔLE — Donner aux maillons de présence la réponse par oui ou par non dont ils
      ont besoin, sans qu'ils aient à compter eux-mêmes. C'est sur elle que reposent
      la plupart des constats de la forme tel document est présent : le prompt de la
      boucle, le script de consolidation, les positions ouvertes, le journal des
      trades, le cockpit, le générateur de cockpit, le journal d'apprentissage, le
      registre des stratégies, et les documents de gouvernance autres que le REGISTRE
      et le backlog.
    ② CONTEXTE D'APPEL — Une quinzaine d'endroits, dans les maillons 2, 3, 4, 5, 6, 7
      et 15. Jamais appelée par une autre fonction.
    ③ ENTRÉE — `motif` : le fragment de nom cherché, par exemple positions_ouvertes,
      journal_apprentissage ou MODULE_C5_ETENDU. La casse, les espaces, les tirets et
      les soulignés sont indifférents.
    ④ CONDITIONS D'ENTRÉE — `motif` doit être un texte.
    ⑤ SORTIE — UNE valeur : vrai dès qu'un fichier au moins porte ce motif, faux
      sinon. Mesuré le 20-09-2026 sur une copie du dépôt : appelée avec PILOTE elle
      rend vrai, appelée avec zzz elle rend faux.
      [rend: 1]
    ⑥ TRAITEMENT — ① demander la liste des fichiers portant ce motif · ② rendre vrai
      si cette liste n'est pas vide.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Elle passe par la recherche de fichiers déjà écrite plutôt que de
      regarder la liste des noms elle-même, pour que la façon de rapprocher deux
      graphies soit définie à un seul endroit. Deux écritures d'une même chose
      divergent toujours (R-708).
    ⑨ CE QUI CLOCHE — deux points, tous deux mesurés le 20-09-2026 :
      ① ELLE CONFOND UN FICHIER AVEC UN DOCUMENT QUI EN PARLE, ET DEUX MAILLONS DU
      MÊME RAPPORT SE CONTREDISENT. Elle hérite de la recherche par fragment de nom,
      qui attrape tout ce qui contient le motif. Mesuré en retirant
      gouvernance/PILOTE.md d'une copie du dépôt : le maillon 7 affiche
      ✅ PILOTE présent, parce que gouvernance/PILOTE_SOCLE.md porte le motif, pendant
      que le maillon 8 affiche ❌ PILOTE : AUCUN document ne se déclare FABRIQUÉ à sa
      première ligne non vide. Le document a bel et bien disparu, et le maillon qui
      contrôle sa présence dit qu'il est là.
      ② Elle ne dit rien du nombre. Un motif qui trouve un fichier et un motif qui en
      trouve cinq rendent le même oui : appelée avec cockpit elle rend vrai, et cinq
      fichiers portent ce motif dont deux maquettes et un document d'analyse.
    ⑩ EFFET — N'écrit aucun fichier, n'ouvre aucun fichier, n'affiche rien, ne touche
      pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels ne se
      termine.
      [sort: non]
    ⑫ DÉFINITIONS
      un maillon : un groupe de contrôles du radar, désigné par un numéro et
        un nom, par exemple 18-Tâches pour le contrôle des traces laissées par
        les tâches planifiées.
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque
        soir, qui contrôle l'ensemble du système et range chacun de ses
        constats sous un numéro de maillon, par exemple 18-Tâches pour le
        contrôle des traces laissées par les tâches planifiées.
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
      le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions
        et des actions du projet
      le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui
        dit ou en est le projet, ce qu'il contient et ce qui cloche
      une graphie : l'une des façons dont un même nom de fichier est écrit
        selon le canal par lequel on le lit — avec espaces ou tirets bas, avec
        ou sans accents
      la boucle du jour : la tâche planifiée qui collecte les cours et écrit
        le rapport de boucle, du lundi au vendredi seulement.
      un motif : un morceau de nom passé à une fonction de recherche, par
        exemple trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
      le cockpit : la page web que ce programme fabrique et que Jean-Luc ouvre pour voir l etat du systeme.
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    return len(trouve(motif)) > 0


def chemin_de(nom):
    """Rend le chemin complet d'un fichier connu par son seul nom, sous-dossiers compris.

    ① RÔLE — Permettre d'ouvrir réellement un fichier dont on ne connaît que le nom
      nu. Le radar tient deux listes : les chemins relatifs, pour ouvrir, et les noms
      nus, pour comparer. Tout code qui recollait le nom nu au dossier du projet
      ratait les fichiers rangés en sous-dossier, et le radar rendait alors des
      constats bloquants FAUX en cascade. Mesuré par Cowork le 12-09-2026 sur un clone
      tel quel : golden ABSENT du projet alors qu'il est dans gouvernance,
      MODULE C5-ETENDU-10 introuvable alors qu'il est dans programmes, et
      BACKLOG EN ÉCHEC alors que verif_backlog.py est là. Un radar qui rend des
      constats bloquants faux est pire que pas de radar. Quatre endroits étaient
      fautifs ; ils passent tous par ici.
    ② CONTEXTE D'APPEL — Huit endroits, dans cinq maillons : le chargement du module
      de signal, la lecture d'un fichier de tableur, la lecture du golden et des
      données de cours au maillon 8, et le lancement de programmes/verif_backlog.py au
      maillon 16.
    ③ ENTRÉE — `nom` : le nom nu du fichier, sans dossier, par exemple
      cac40_ohlcv.csv ou verif_backlog.py. La comparaison est EXACTE, à la différence
      de la recherche par fragment employée ailleurs dans le programme.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un nom inconnu ne fait pas tomber la fonction.
    ⑤ SORTIE — UNE valeur : un chemin complet, de deux formes selon la branche. Quand
      le nom a été trouvé, c'est le dossier examiné suivi du chemin relevé au
      démarrage. Quand il n'a pas été trouvé, c'est le dossier examiné suivi du nom
      reçu, qui ne mène nulle part. Mesuré le 20-09-2026 sur une copie du dépôt :
      cac40_ohlcv.csv rend .../donnees/cac40_ohlcv.csv, et INEXISTANT.csv rend
      .../INEXISTANT.csv.
      [rend: 1]
    ⑥ TRAITEMENT — ① parcourir les chemins relevés au démarrage · ② s'arrêter au
      premier dont le nom nu est exactement le nom reçu · ③ rendre ce chemin, préfixé
      du dossier examiné · ④ à défaut, rendre le nom reçu préfixé du dossier examiné.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le repli rend un chemin qui n'existe pas, plutôt que rien : ainsi
      l'appelant échoue à l'ouverture, là où il attend un fichier, avec un message qui
      nomme le fichier manquant. Rendre rien obligerait chaque appelant à écrire son
      propre contrôle, et l'un d'eux l'oublierait.
    ⑨ CE QUI CLOCHE — deux points, mesurés le 20-09-2026 :
      ① LE PREMIER TROUVÉ L'EMPORTE, ET LE PREMIER EST LE PREMIER DANS L'ALPHABET. La
      liste des chemins est triée alphabétiquement sur le chemin entier, dossier
      compris. Avec deux fichiers du même nom dans deux dossiers différents, c'est
      celui dont le dossier vient en premier qui est rendu, quelle que soit sa date.
      Le cas s'est présenté dans le dossier même de ce travail : une copie du dépôt
      posée sous le nom _copie a fait rendre _copie/donnees/cac40_ohlcv.csv au lieu de
      donnees/cac40_ohlcv.csv, parce que le souligné précède la lettre d. C'est la
      faute que le projet a fermée ailleurs en lisant la date portée par le nom.
      ② Deux fichiers de même nom à deux endroits sont un défaut, jamais une
      intention, et cette fonction les masque au lieu de les signaler : elle en choisit
      un et se tait. Le rapport ne portera jamais la moindre ligne à ce sujet.
    ⑩ EFFET — N'ouvre aucun fichier, n'écrit rien, n'affiche rien, ne touche pas au
      réseau : elle ne fait que composer un chemin.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels ne se
      termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque
        soir, qui contrôle l'ensemble du système et range chacun de ses
        constats sous un numéro de maillon, par exemple 18-Tâches pour le
        contrôle des traces laissées par les tâches planifiées.
      un maillon : un groupe de contrôles du radar, désigné par un numéro et
        un nom, par exemple 18-Tâches pour le contrôle des traces laissées par
        les tâches planifiées.
      le golden : le fichier gouvernance/golden_tests_*.json, qui fige des
        chiffres de référence ; tout écart à données identiques est une
        régression.
      le module de signal : le programme qui décide quelles valeurs acheter
      Cowork : le relecteur du projet, qui clone le dépôt, casse le code et
        rend ses cassures par écrit
      le Chat : la conversation qui rédige la gouvernance du projet et dépose ses
        versions
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
    
      C5-ETENDU-10 : le nom de la stratégie vivante ; ses seuils et son horizon sont lus dans `donnees/cac40_strategies.csv`.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    for p in _chemins:
        if os.path.basename(p) == nom:
            return os.path.join(PROJ, p)
    return os.path.join(PROJ, nom)   # repli : l'appelant verra l'échec d'ouverture


# ─── LE REGISTRE VIT AU DÉPÔT (R-736) ───
# Posé le 09-09-2026. Le REGISTRE est la LOI et ne vit plus qu'au dépôt, en un seul
# exemplaire. Tant que ce programme le cherchait au PROJET, la copie périmée qui y
# traîne ne pouvait pas être retirée : la retirer aurait donné un ❌ CRITIQUE ici.
# On cherche donc AU DÉPÔT d'abord ; le projet ne sert plus que de repli, le temps
# que la copie en parte.
def _registre_dans(dossier):
    """Cherche un fichier de règles dans UN dossier donné, et rend son chemin complet.

    ① RÔLE — Répondre à une question simple, posée plusieurs fois de suite sur des
      dossiers différents : le REGISTRE est-il ici ? C'est le pas élémentaire de la
      recherche du REGISTRE, qui regarde d'abord au dépôt puis, seulement en repli, le
      dossier examiné.
    ② CONTEXTE D'APPEL — Deux endroits, tous deux dans la fonction qui rend le chemin
      du REGISTRE : une fois par dossier candidat du dépôt, et une fois sur le
      sous-dossier gouvernance du dossier examiné. Jamais appelée ailleurs.
    ③ ENTRÉE — `dossier` : le dossier à regarder, par exemple
      /tmp/depot/gouvernance ou le sous-dossier gouvernance du dossier examiné. Un
      texte vide est accepté.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un texte vide, un dossier inexistant ou un chemin
      qui désigne un fichier et non un dossier rendent tous rien, sans faire tomber.
    ⑤ SORTIE — UNE valeur : le chemin complet du premier fichier dont le nom contient
      REGISTRE_REGLES, ou rien. Mesuré le 20-09-2026 sur une copie du dépôt : appelée
      sur le sous-dossier gouvernance, elle rend
      .../gouvernance/REGISTRE_REGLES.md ; appelée sur /nexistepas, elle rend rien.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre rien si le dossier est vide ou n'existe pas · ② lister le
      dossier et le trier par ordre alphabétique · ③ s'arrêter au premier nom qui
      contient REGISTRE_REGLES, casse et séparateurs confondus · ④ rendre son chemin
      complet.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Elle ne regarde qu'un seul dossier, sans descendre, parce que c'est
      son appelant qui décide de l'ordre des dossiers à essayer, et que cet ordre
      porte un sens : le dépôt d'abord, le projet ensuite. Descendre les
      sous-dossiers effacerait cette distinction et rendrait impossible de dire d'où
      vient le fichier trouvé.
    ⑨ CE QUI CLOCHE — deux points, mesurés le 20-09-2026 :
      ① Elle ne dit pas combien de fichiers portaient ce motif : elle prend le premier
      dans l'ordre alphabétique et se tait. Deux registres voisins dans le même
      dossier, et le radar en lit un sans que rien ne le dise. Le projet impose
      pourtant un seul exemplaire du REGISTRE, sous un nom fixe.
      ② Le motif cherché est un nom épelé, REGISTRE_REGLES. Le critère qui tranche
      tient en une question : si je renomme un fichier, mon contrôle change-t-il
      d'avis ? Ici oui, donc il épelle. Un registre renommé deviendrait introuvable,
      et le maillon 7 rendrait un constat bloquant sur un fichier pourtant présent.
    ⑩ EFFET — LIT la liste des noms d'un dossier. N'ouvre aucun fichier, n'écrit rien,
      n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. PEUT LEVER si le dossier existe mais refuse
      d'être listé, par exemple faute de droits : l'échec du système de fichiers n'est
      pas rattrapé ici. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
      le projet : le dossier reçu sur la ligne de commande, celui que le radar examine
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque
        soir, qui contrôle l'ensemble du système et range chacun de ses
        constats sous un numéro de maillon, par exemple 18-Tâches pour le
        contrôle des traces laissées par les tâches planifiées.
      un maillon : un groupe de contrôles du radar, désigné par un numéro et
        un nom, par exemple 18-Tâches pour le contrôle des traces laissées par
        les tâches planifiées.
      un constat : une ligne du rapport, portant un signe, un numéro de maillon
        et une phrase
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if not dossier or not os.path.isdir(dossier):
        return None
    for f_ in sorted(os.listdir(dossier)):
        if _norm("REGISTRE_REGLES") in _norm(f_):
            return os.path.abspath(os.path.join(dossier, f_))
    return None


def chemin_backlog():
    """Rend le chemin complet du backlog, cherché au dépôt d'abord et au projet en repli.

    ① RÔLE — Aller chercher le tableau des décisions là où il vit réellement. Le
      backlog a quitté le projet le 05-09-2026 pour le dépôt, et seul le texte de la
      tâche planifiée le rattrapait en le recopiant dans le dossier de travail : le
      programme, lui, ne le savait pas. Un geste qui ne vit que dans une consigne
      finit par cesser, et sa cessation est muette.
    ② CONTEXTE D'APPEL — Trois endroits : le maillon 7, qui teste la présence du
      backlog et l'appelle deux fois dans la même passe, une fois pour savoir s'il
      existe et une fois pour composer la mention au dépôt ; et le maillon 16, qui a
      besoin du chemin pour en faire une copie et la faire contrôler par
      programmes/verif_backlog.py.
    ③ ENTRÉE — Aucun paramètre. Elle lit la variable d'environnement DEPOT_CAC40, et
      connaît par ailleurs deux chemins écrits en dur, /tmp/depot et /tmp/depot/d.
    ④ CONDITIONS D'ENTRÉE — Le parcours du dossier examiné doit avoir eu lieu, ce qui
      est toujours vrai. Si aucun des trois dossiers du dépôt ne porte de backlog et
      que plusieurs fichiers du projet en portent le nom, le choix est confié à la
      fonction qui lit la date du nom, et celle-ci exige que programmes/COMMUN.py soit
      présent à côté du radar.
    ⑤ SORTIE — UNE valeur : le chemin complet du backlog, ou rien quand aucun n'a été
      trouvé nulle part. Mesuré le 20-09-2026 : elle rend
      /tmp/depot/BACKLOG_DECISIONS.md.
      [rend: 1]
    ⑥ TRAITEMENT — ① essayer trois dossiers dans l'ordre, la variable
      d'environnement puis /tmp/depot puis /tmp/depot/d, et rendre le premier fichier
      dont le nom contient backlog_decisions · ② à défaut, chercher ce nom parmi les
      fichiers du dossier examiné · ③ s'il y en a plusieurs, retenir celui dont le nom
      porte la date la plus récente · ④ rendre le chemin complet, ou rien.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le dépôt passe avant le projet, et non l'inverse, parce que le projet
      n'est qu'une copie de lecture et qu'il peut porter une version périmée. Tant que
      le programme cherchait au projet d'abord, la copie périmée ne pouvait pas être
      retirée : la retirer aurait fait rendre un constat bloquant.
    ⑨ CE QUI CLOCHE — trois points, tous mesurés le 20-09-2026 :
      ① ELLE LIT UN AUTRE DÉPÔT QUE CELUI QU'ON LUI DONNE, ET RIEN NE LE DIT. Les deux
      chemins /tmp/depot et /tmp/depot/d sont écrits en dur et passent AVANT le
      dossier reçu sur la ligne de commande. Mesuré : le radar lancé sur
      /tmp/cwlot7b a rendu /tmp/depot/BACKLOG_DECISIONS.md, c'est-à-dire le backlog
      d'une tout autre copie présente sur la même machine. Le rapport affiche alors
      ✅ BACKLOG présent et le maillon 16 contrôle un fichier que personne n'a
      demandé.
      ② LA MÊME VARIABLE D'ENVIRONNEMENT EST ATTENDUE AVEC DEUX SENS DIFFÉRENTS. Ici,
      DEPOT_CAC40 doit désigner le PREMIER NIVEAU du dépôt, puisqu'on y cherche le backlog ;
      dans la fonction voisine qui cherche le REGISTRE, la même variable doit désigner
      le sous-dossier gouvernance. Les deux ne peuvent pas être vraies en même temps :
      quelle que soit la valeur donnée, l'une des deux recherches échouera.
      ③ Elle ne dit jamais d'où vient le fichier rendu. Sa voisine qui cherche le
      REGISTRE rend le chemin ET son origine, parce que déduire l'origine du chemin
      faisait mentir l'étiquette dans trois cas mesurés le 09-09-2026. Ici, l'appelant
      en est réduit à chercher le mot depot dans le chemin du projet : c'est
      exactement le raccourci qu'on a retiré à côté, et il est resté là.
    ⑩ EFFET — LIT la liste des noms de trois dossiers. N'ouvre aucun fichier, n'écrit
      rien, n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main. PEUT LEVER, et cela arrête alors le programme : si
      aucun dépôt ne porte le backlog, que plusieurs fichiers du projet en portent le
      nom, et que programmes/COMMUN.py est absent, le choix entre homonymes lève
      RuntimeError: COMMUN.le_plus_recent introuvable. Et un de ses appels peut ne pas
      revenir, pour cette même raison.
      [sort: non]
    ⑫ DÉFINITIONS
      le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions
        et des actions du projet
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
      le projet : le dossier reçu sur la ligne de commande, celui que le radar examine
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque
        soir, qui contrôle l'ensemble du système et range chacun de ses
        constats sous un numéro de maillon, par exemple 18-Tâches pour le
        contrôle des traces laissées par les tâches planifiées.
      un maillon : un groupe de contrôles du radar, désigné par un numéro et
        un nom, par exemple 18-Tâches pour le contrôle des traces laissées par
        les tâches planifiées.
      la tâche planifiée : un fichier de .github/workflows/ qui fait tourner
        un programme à heure fixe sur une machine GitHub, sans clic ni
        autorisation.
      un constat : une ligne du rapport, portant un signe, un numéro de maillon
        et une phrase
      le tableau des décisions : le fichier `BACKLOG_DECISIONS.md`, dont
        chaque ligne porte un identifiant de la forme `A-238`
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    for c in (os.environ.get("DEPOT_CAC40", ""), "/tmp/depot", "/tmp/depot/d"):
        p = _registre_dans_motif(c, "backlog_decisions")
        if p:
            return p
    rel = trouve("BACKLOG_DECISIONS")
    return os.path.abspath(os.path.join(PROJ, _le_plus_recent(rel))) if rel else None


def _registre_dans_motif(dossier, motif):
    """Cherche un fichier par fragment de nom dans UN dossier, et rend son chemin complet.

    ① RÔLE — Faire pour le backlog ce que son voisin fait pour le REGISTRE : regarder
      dans un seul dossier, sans descendre, si le fichier cherché s'y trouve. Les deux
      fonctions ne diffèrent que par un point : celle-ci reçoit le fragment de nom au
      lieu de le porter écrit en dur.
    ② CONTEXTE D'APPEL — Un seul endroit : la fonction qui rend le chemin du backlog,
      qui l'appelle une fois par dossier candidat, soit trois fois par passage. Jamais
      appelée ailleurs.
    ③ ENTRÉE — `dossier` : le dossier à regarder, par exemple /tmp/depot ·
      `motif` : le fragment de nom cherché. Un seul appelant, et il passe toujours le
      même motif, backlog_decisions, écrit en minuscules.
    ④ CONDITIONS D'ENTRÉE — Le motif doit déjà être écrit sous la forme unique du
      programme, c'est-à-dire en minuscules et avec des soulignés : il est comparé
      sans être normalisé, alors que les noms de fichiers, eux, le sont. Un motif
      écrit BACKLOG_DECISIONS ne trouverait donc rien. Le dossier, lui, peut être vide
      ou inexistant.
    ⑤ SORTIE — UNE valeur : le chemin complet du premier fichier dont le nom contient
      le motif, ou rien. Mesuré le 20-09-2026 sur une copie du dépôt : appelée avec
      backlog_decisions sur le premier niveau de la copie, elle rend
      .../BACKLOG_DECISIONS.md.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre rien si le dossier est vide ou n'existe pas · ② lister le
      dossier et le trier par ordre alphabétique · ③ s'arrêter au premier nom dont la
      forme unique contient le motif · ④ rendre son chemin complet.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Elle existe séparément de sa voisine parce que le backlog et le
      REGISTRE ne vivent pas au même endroit du dépôt : le REGISTRE est dans le
      sous-dossier gouvernance, le backlog est au premier niveau. Une seule fonction aurait
      dû recevoir à la fois le dossier et le motif, ce qui est exactement ce que
      celle-ci fait.
    ⑨ CE QUI CLOCHE — trois points, mesurés le 20-09-2026 :
      ① DEUX FONCTIONS FONT LA MÊME CHOSE, ET ELLES DIVERGENT DÉJÀ. Celle-ci
      normalise le nom du fichier avant de le comparer, sa voisine normalise les deux
      côtés. Deux écritures d'une même chose divergent toujours (R-708), et ici la
      divergence est déjà là : le motif doit être écrit en minuscules pour l'une et
      peut être écrit comme on veut pour l'autre, sans qu'aucun texte ne le dise.
      ② Elle porte un nom qui parle du REGISTRE alors qu'elle ne sert qu'au backlog.
      Qui cherche le code du backlog ne pensera pas à ouvrir une fonction appelée
      registre.
      ③ Comme sa voisine, elle prend le premier fichier dans l'ordre alphabétique sans
      dire combien il y en avait. Un backlog d'archive rangé à côté du vrai serait
      choisi s'il venait avant lui dans l'alphabet, et le radar contrôlerait
      l'archive.
    ⑩ EFFET — LIT la liste des noms d'un dossier. N'ouvre aucun fichier, n'écrit rien,
      n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. PEUT LEVER si le dossier existe mais refuse
      d'être listé. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions
        et des actions du projet
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque
        soir, qui contrôle l'ensemble du système et range chacun de ses
        constats sous un numéro de maillon, par exemple 18-Tâches pour le
        contrôle des traces laissées par les tâches planifiées.
      un motif : un morceau de nom passé à une fonction de recherche, par
        exemple trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if not dossier or not os.path.isdir(dossier):
        return None
    for f_ in sorted(os.listdir(dossier)):
        if motif in _norm(f_):
            return os.path.abspath(os.path.join(dossier, f_))
    return None


def chemin_registre():
    """Rend le chemin complet du REGISTRE et dit d'où il vient, du dépôt ou du projet.

    ① RÔLE — Donner aux maillons qui lisent la loi du projet le fichier qui fait foi,
      et leur dire d'où il sort. Le REGISTRE est le fichier où vit chaque règle, en un
      seul exemplaire, et il ne vit plus qu'au dépôt depuis le 09-09-2026. Tant que le
      programme le cherchait au projet, la copie périmée qui y traînait ne pouvait pas
      être retirée : la retirer aurait fait rendre un constat bloquant sur un fichier
      qui n'avait plus à être là.
    ② CONTEXTE D'APPEL — Quatre endroits : le maillon 7, qui teste sa présence et
      affiche son origine · la fonction qui lit le nom du golden et ses empreintes
      attendues · le maillon 15, qui y cherche la ligne de chaque stratégie.
    ③ ENTRÉE — Aucun paramètre. Elle lit la variable d'environnement DEPOT_CAC40, et
      connaît par ailleurs deux chemins écrits en dur, /tmp/depot/gouvernance et
      /tmp/depot/d/gouvernance.
    ④ CONDITIONS D'ENTRÉE — Le parcours du dossier examiné doit avoir eu lieu, ce qui
      est toujours vrai. Si le REGISTRE n'est trouvé ni au dépôt ni dans le
      sous-dossier gouvernance du projet, et que plusieurs fichiers du projet en
      portent le nom, le choix est confié à la fonction qui lit la date du nom, et
      celle-ci exige que programmes/COMMUN.py soit présent à côté du radar.
    ⑤ SORTIE — DEUX valeurs : le chemin complet, et l'origine. L'origine vaut dépôt
      ou repli projet. Quand rien n'a été trouvé, les deux valeurs sont vides. Mesuré
      le 20-09-2026 : elle rend /tmp/depot/gouvernance/REGISTRE_REGLES.md et dépôt.
      [rend: 2]
    ⑥ TRAITEMENT — ① essayer trois dossiers du dépôt dans l'ordre, la variable
      d'environnement puis les deux chemins écrits en dur, et rendre le premier
      registre trouvé avec l'origine dépôt · ② à défaut, regarder le sous-dossier
      gouvernance du projet et rendre l'origine repli projet · ③ à défaut, chercher le
      nom parmi tous les fichiers du projet, retenir celui dont le nom porte la date
      la plus récente, et rendre l'origine repli projet · ④ à défaut, ne rien rendre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Elle DIT d'où vient le fichier au lieu de laisser l'appelant le
      deviner. Une première version rendait le chemin seul, et l'appelant cherchait le
      mot depot dans la chaîne : trois cas la faisaient mentir, mesurés le
      09-09-2026 — une variable DEPOT_CAC40 pointant hors de /tmp était annoncée
      repli · un projet dont le chemin contient depot était annoncé dépôt, ce qui
      masque exactement la panne que l'étiquette doit révéler · et le sous-dossier
      gouvernance du projet figurait dans la boucle du dépôt, donc un registre du
      projet y était étiqueté dépôt. Rapporter ce qu'on croit au lieu de ce qu'on a
      fait.
    ⑨ CE QUI CLOCHE — trois points, tous mesurés le 20-09-2026 :
      ① ELLE LIT UN AUTRE DÉPÔT QUE CELUI QU'ON LUI DONNE. Les deux chemins
      /tmp/depot/gouvernance et /tmp/depot/d/gouvernance sont écrits en dur et passent
      avant le dossier reçu sur la ligne de commande. Mesuré : le radar lancé sur
      /tmp/cwlot7b a lu /tmp/depot/gouvernance/REGISTRE_REGLES.md, le registre d'une
      autre copie présente sur la même machine, et le rapport affiche
      ✅ REGISTRE présent (au dépôt). L'étiquette est juste et trompeuse à la fois :
      c'est bien un dépôt, ce n'est pas celui qu'on examine.
      ② LA MÊME VARIABLE D'ENVIRONNEMENT EST ATTENDUE AVEC DEUX SENS DIFFÉRENTS. Ici,
      DEPOT_CAC40 doit désigner le sous-dossier gouvernance ; dans la fonction voisine
      qui cherche le backlog, la même variable doit désigner le premier niveau du dépôt. Les
      deux ne peuvent pas être vraies en même temps.
      ③ Le repli sur le projet se fait sans rien dire de plus que l'étiquette. Le
      maillon 7 affiche alors REPLI SUR LE PROJET — le clone du dépôt a-t-il échoué ?,
      ce qui est une question et non un constat ; et les trois autres appelants, eux,
      jettent l'origine et lisent le fichier sans savoir qu'il peut être périmé.
    ⑩ EFFET — LIT la liste des noms de quatre dossiers. N'ouvre aucun fichier, n'écrit
      rien, n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main. PEUT LEVER, et cela arrête alors le programme : si
      le REGISTRE n'est trouvé dans aucun dossier, que plusieurs fichiers du projet en
      portent le nom, et que programmes/COMMUN.py est absent, le choix entre homonymes
      lève RuntimeError: COMMUN.le_plus_recent introuvable. Et un de ses appels peut
      ne pas revenir, pour cette même raison.
      [sort: non]
    ⑫ DÉFINITIONS
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
      le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions
        et des actions du projet
      le golden : le fichier gouvernance/golden_tests_*.json, qui fige des
        chiffres de référence ; tout écart à données identiques est une
        régression.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
      le projet : le dossier reçu sur la ligne de commande, celui que le radar examine
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque
        soir, qui contrôle l'ensemble du système et range chacun de ses
        constats sous un numéro de maillon, par exemple 18-Tâches pour le
        contrôle des traces laissées par les tâches planifiées.
      un maillon : un groupe de contrôles du radar, désigné par un numéro et
        un nom, par exemple 18-Tâches pour le contrôle des traces laissées par
        les tâches planifiées.
      une stratégie : une règle qui dit QUOI acheter, avec son objectif de
        gain, sa perte acceptée et son horizon
      un constat : une ligne du rapport, portant un signe, un numéro de maillon
        et une phrase
    
      la boucle : la tache planifiee qui lit les signaux et rend compte
"""
    for c in (os.environ.get("DEPOT_CAC40", ""), "/tmp/depot/gouvernance",
              "/tmp/depot/d/gouvernance"):
        p = _registre_dans(c)
        if p:
            return p, "dépôt"
    # REPLI SUR LE PROJET, quand le clone a échoué. Deux chemins, dans cet ordre :
    # <projet>/gouvernance d'abord — il était à tort dans la boucle du dépôt — puis
    # la racine du projet. Le chemin est rendu ABSOLU : sans cela, un projet passé en
    # chemin RELATIF donnait un chemin relatif que l'appelant préfixait une seconde
    # fois, et le maillon 8 criait sur un registre pourtant présent.
    p = _registre_dans(os.path.join(PROJ, "gouvernance"))
    if p:
        return p, "repli projet"
    rel = trouve("REGISTRE_REGLES")
    # EN CAS D'HOMONYMES, C'EST LE PLUS RÉCENT PAR LA DATE DE SON NOM.
    # Le commentaire disait ici « le DERNIER par ordre alphabétique fait foi » :
    # une convention affirmée, jamais vérifiée, et fausse — les noms commencent
    # par le jour de la semaine, l'alphabet les mélange. Jean-Luc, 12-09-2026.
    if rel:
        return os.path.abspath(os.path.join(PROJ, _le_plus_recent(rel))), "repli projet"
    return None, None

# A-15 — au-delà de ce seuil, un écart n'est plus imputable à la convention de frais
# (A-50 non tranchée : journal = frais réels ~306 €, module = forfait 300 €).
SEUIL_ECART_CALCUL = 25.0   # euros

rapport = []
OK, WARN, FAIL = "✅", "⚠️", "❌"
score = {"ok":0, "warn":0, "fail":0}
def check(maillon, condition, msg_ok, msg_ko, critique=False):
    """Range un constat dans le rapport selon qu'une condition est vraie ou fausse.

    ① RÔLE — Donner à tous les maillons une seule façon d'écrire leur verdict, pour
      que le rapport du soir soit lisible d'un bout à l'autre et que le score se
      tienne tout seul. C'est le geste élémentaire du radar : un maillon ne décide pas
      de la forme de sa ligne, il donne sa condition et ses deux phrases. Mesuré le
      20-09-2026 sur une copie du dépôt : 30 appels écrits dans le programme, qui ont
      produit 42 lignes vertes et 13 lignes d'alerte.
    ② CONTEXTE D'APPEL — Trente endroits, dans les maillons 1, 2, 3, 7, 8, 11, 12, 13,
      14, 15, 16, 17, 18 et 19. Les maillons 6, 9 et 10 ne l'emploient pas et écrivent
      leur ligne directement dans le rapport, en incrémentant eux-mêmes le score.
    ③ ENTRÉE — `maillon` : le numéro et le nom du groupe de contrôles, par exemple
      18-Tâches · `condition` : ce qui doit être vrai, par exemple une liste vide
      d'écarts · `msg_ok` : la phrase à écrire quand la condition est vraie ·
      `msg_ko` : la phrase à écrire quand elle est fausse · `critique` : vrai quand
      l'échec est bloquant, faux par défaut. Mesuré le 20-09-2026 : 18 des 30 appels
      passent `critique` à vrai, les 12 autres laissent la valeur par défaut.
    ④ CONDITIONS D'ENTRÉE — Les deux phrases doivent être des textes déjà composés :
      la fonction n'en fabrique aucune, et les deux sont évaluées par l'appelant AVANT
      l'appel, même celle qui ne servira pas.
    ⑤ SORTIE — Ne rend rien. Son résultat est l'état de deux variables partagées : la
      liste des constats, à laquelle une ligne est ajoutée, et le score, dont un des
      trois compteurs augmente de un.
      [rend: rien]
    ⑥ TRAITEMENT — ① si la condition est vraie, ajouter au rapport le signe du succès,
      le maillon et la phrase de succès, et augmenter le compteur des succès · ② sinon,
      choisir le signe selon que l'échec est bloquant ou non · ③ ajouter au rapport ce
      signe, le maillon et la phrase d'échec · ④ augmenter le compteur des échecs
      bloquants ou celui des alertes.
    ⑦ UNITÉ — Un CONSTAT, c'est-à-dire une ligne de rapport. Les trois compteurs du
      score se comptent en constats : succès, alertes, échecs bloquants.
    ⑧ POURQUOI — Les échecs sont rangés en deux tas et non en un seul, parce qu'ils ne
      demandent pas le même geste : un échec bloquant est une faille à corriger en
      priorité, une alerte est à planifier. Le rapport le rappelle en troisième ligne,
      à chaque passage. Fondre les deux ferait crier le radar tous les soirs pour des
      faits connus, et une alerte qu'on apprend à ignorer cesse de protéger.
    ⑨ CE QUI CLOCHE — quatre points, tous mesurés le 20-09-2026 :
      ① AUCUN ÉCHEC BLOQUANT NE CHANGE LE CODE DE SORTIE DU PROGRAMME. Cette fonction
      compte les échecs bloquants dans le score, et personne ne lit ce compteur
      autrement que pour l'afficher. Mesuré en retirant gouvernance/PILOTE.md d'une
      copie : le rapport affiche Score : 41 ✅ · 13 ⚠️ · 1 ❌ et le programme se
      termine avec le code 0. Le pas du soir écrit pourtant
      if [ "$CODE" -ne 0 ]; then echo "::error::" : il ne se déclenchera jamais. Un
      contrôle qui n'a pas pu conclure doit rendre un code de sortie non nul (R-734).
      ② SIX APPELS PASSENT UNE PHRASE DE SUCCÈS VIDE. Cinq d'entre eux sont au maillon
      18 et un au maillon 8, tous écrits avec une condition toujours fausse, pour se
      servir de la fonction comme d'un simple moyen d'ajouter une alerte. Si l'un de
      ces appels devenait vrai un jour, le rapport porterait une ligne composée d'un
      signe vert, d'un numéro de maillon et de rien du tout. Rien dans la fonction
      n'interdit ce cas.
      ③ DEUX APPELS PASSENT LA PHRASE D'ÉCHEC sans objet, au maillon 19, sur des
      contrôles dont la condition est écrite en dur à vrai. Ces deux constats sont
      verts par construction : ils informent, ils ne contrôlent rien, et le lecteur du
      rapport n'a aucun moyen de les distinguer des trente autres.
      ④ Elle écrit dans deux variables partagées par tout le programme au lieu de
      rendre son constat. Trois maillons écrivent d'ailleurs directement dans ces
      mêmes variables sans passer par elle, et doivent alors penser à incrémenter le
      bon compteur à la main. Un oubli à cet endroit fausserait le score sans qu'aucune
      ligne ne manque au rapport.
    ⑩ EFFET — MODIFIE deux variables partagées : la liste des constats et les trois
      compteurs du score. N'écrit aucun fichier, n'affiche rien elle-même — le rapport
      n'est affiché qu'à la toute fin du programme — et ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels ne se
      termine : elle n'en fait aucun.
      [sort: non]
    ⑫ DÉFINITIONS
      un constat : une ligne du rapport, portant un signe, un numéro de maillon et une
        phrase
      un maillon : un groupe de contrôles du radar, désigné par un numéro et
        un nom, par exemple 18-Tâches pour le contrôle des traces laissées par
        les tâches planifiées.
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque
        soir, qui contrôle l'ensemble du système et range chacun de ses
        constats sous un numéro de maillon, par exemple 18-Tâches pour le
        contrôle des traces laissées par les tâches planifiées.
      le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui
        dit ou en est le projet, ce qu'il contient et ce qui cloche
    """
    if condition:
        rapport.append((OK, maillon, msg_ok)); score["ok"] += 1
    else:
        sig = FAIL if critique else WARN
        rapport.append((sig, maillon, msg_ko))
        score["fail" if critique else "warn"] += 1

# ═══ MAILLON 1 — ACQUISITION ═══
# Le prompt de la boucle a changé de nom le 13/08 : TACHE_COWORK_* est devenu
# PROMPT_BOUCLE_v4_*. Le radar cherchait l'ancien nom et criait un faux ❌ chaque
# soir (A-243). On cherche désormais les deux motifs — le radar suit le FICHIER,
# pas son ancien nom.
MOTIFS_PROMPT_BOUCLE = ["PROMPT_BOUCLE", "TACHE_COWORK"]
t = [f for m in MOTIFS_PROMPT_BOUCLE for f in trouve(m)]
prompt_4fichiers = False
if t:
    contenu = open(os.path.join(PROJ, t[0]), encoding="utf-8", errors="ignore").read()
    prompt_4fichiers = ("Groupe 2" in contenu or "Groupe2" in contenu or "4 fichiers" in contenu or "39 valeurs" in contenu)
check("1-Acquisition", len(t) > 0,
      f"Prompt de la boucle présent : {t[0] if t else '—'}",
      "Prompt de la boucle ABSENT (ni PROMPT_BOUCLE_*, ni TACHE_COWORK_*)", critique=True)
check("1-Acquisition", prompt_4fichiers,
      "Prompt couvre les 4 fichiers/39 valeurs",
      "Prompt ne couvre que G1 (10 val) — à étendre pour E4 (39 valeurs), voir A-245")

# ═══ MAILLON 2 — CONSOLIDATION / NOM DU FICHIER MAÎTRE ═══
cours = trouve("cac40_ohlcv")
# LES DEUX GRAPHIES SONT ACCEPTEES ; C'EST LA DIVERGENCE QUI NE L'EST PAS.
# Premiere version : le maillon exigeait le SOULIGNE et rendait un BLOQUANT
# quand il trouvait l'ESPACE. Or le fichier vivant s'ecrit avec un ESPACE
# depuis toujours, et la tache du soir contournait le probleme en recreant
# artificiellement la graphie a souligne dans sa copie de travail —
# le contournement MASQUAIT le defaut au lieu de le montrer (constate le 31/08).
# Ce qui compte vraiment n'est pas laquelle des deux graphies existe, mais
# qu'il n'y en ait QU'UNE : deux fichiers homonymes a une graphie pres, et
# plus personne ne sait lequel est lu. Le resolveur du service de mesure
# accepte deja les deux ; le radar fait desormais pareil.
_graphies = sorted(f for f in fichiers
                   if f.replace(" ", "_").lower() == "cac40_ohlcv.csv")
check("2-Consolidation", len(cours) > 0,
      "Fichier cours présent", "Fichier cours ABSENT", critique=True)
check("2-Consolidation", len(_graphies) <= 1,
      "Fichier maître des cours : une seule graphie (%s)"
      % (_graphies[0] if _graphies else "aucune"),
      "DEUX GRAPHIES DU FICHIER MAÎTRE : %s — plus personne ne sait laquelle "
      "est lue" % ", ".join(_graphies), critique=True)
check("2-Consolidation", existe("CONSOLIDATION"),
      "Script consolidation présent", "Script consolidation absent")

# ═══ MAILLON 3 — CALCUL SIGNAUX ═══
# CE MAILLON EST DEPLACE PLUS BAS, apres la definition de `_lire_csv` :
# il lit desormais le REGISTRE au lieu de porter des noms en dur, et le
# lecteur de CSV n'est defini qu'a la ligne 390. On emploie le lecteur
# DEJA ECRIT, jamais un second : deux lectures du meme fichier divergent
# toujours (famille A-308).

# ═══ MAILLON 4 — POSITIONS / TRADES ═══
check("4-Positions", existe("positions_ouvertes"),
      "positions_ouvertes.csv présent", "positions_ouvertes.csv absent", critique=True)
check("4-Trades", existe("trading_journal") or existe("journal_trades") or existe("journal_paper"),
      "Journal des trades présent",
      "Journal trades paper absent (à créer au démarrage de l'écriture E3)")

# ═══ MAILLON 5 — COCKPIT ═══
check("5-Cockpit", existe("cockpit"),
      "Cockpit (fichier) présent", "Cockpit absent")
check("5-Cockpit", any(f.startswith("gen_cockpit") or "generateur_cockpit" in f.lower() for f in fichiers),
      "Générateur cockpit présent (régénérable)",
      "GÉNÉRATEUR COCKPIT ABSENT — le cockpit ne peut pas se régénérer", critique=True)

# ═══ MAILLON 6 — APPRENTISSAGE ═══
check("6-Apprentissage", existe("journal_apprentissage"),
      "journal_apprentissage présent", "journal_apprentissage absent")
# LE SAS N'EXISTE PLUS : IL A ETE ABSORBE PAR LE REGISTRE LE 29-08-2026.
# `registre_candidates.csv` a ete supprime ce jour-la : il dupliquait sept
# colonnes de `cac40_strategies.csv` sous d'autres identifiants, sans qu'aucune
# colonne ne relie les deux fichiers. Reclamer un fichier supprime produit une
# alerte qu'on ne peut pas eteindre — et une alerte qu'on ne peut pas eteindre
# devient du bruit.
check("6-Apprentissage", existe("cac40_strategies"),
      "Registre des stratégies présent (le sas y a été absorbé le 29/08)",
      "REGISTRE DES STRATÉGIES ABSENT", critique=True)
# tâche mensuelle : non détectable depuis les fichiers (vit dans Cowork) -> note
rapport.append((WARN, "6-Apprentissage", "Tâche mensuelle Cowork : à vérifier dans Cowork (non visible ici)"))
score["warn"] += 1

# ═══ MAILLON 7 — GOUVERNANCE ═══
for besoin, motif in [("golden_tests","golden"),("REGISTRE","REGISTRE_REGLES"),
                      ("PILOTE","PILOTE"),("BACKLOG","BACKLOG_DECISIONS"),("veille","registre_veille")]:
    # Le REGISTRE ne vit plus au projet (R-736) : sa présence se teste au DÉPÔT.
    _cr7, _org7 = chemin_registre() if besoin == "REGISTRE" else (None, None)
    # Le BACKLOG a quitté le projet le 05-09 : sa présence se teste là où il vit.
    _present = ((_cr7 is not None) if besoin == "REGISTRE"
                else (chemin_backlog() is not None) if besoin == "BACKLOG"
                else existe(motif))
    # L'origine est RELEVÉE par la fonction, jamais déduite du chemin.
    _ou = (" (au dépôt)" if besoin == "BACKLOG" and chemin_backlog()
           and "depot" not in str(PROJ) and not existe(motif)
           else "" if besoin != "REGISTRE"
           else " (au dépôt)" if _org7 == "dépôt"
           else " (REPLI SUR LE PROJET — le clone du dépôt a-t-il échoué ?)")
    check("7-Gouvernance", _present, f"{besoin} présent{_ou}", f"{besoin} ABSENT{_ou}", critique=(besoin in ("PILOTE","REGISTRE")))

# ═══ COHÉRENCE : une seule version vivante des docs de pilotage ═══
# UNE VERSION SE DÉCLARE, ELLE NE S'ÉPELLE PAS.
# Trois rondes de Cowork sur ce seul contrôle, et son diagnostic de méthode vaut
# mieux que les trois correctifs : « vos deux corrections précédentes étaient justes
# et chacune a créé le défaut suivant — l'aveugle est devenu indiscriminé, puis
# l'indiscriminé est devenu sélectif-par-liste. C'est le même geste à chaque fois :
# réparer par une ÉNUMÉRATION ce qui demande une PROPRIÉTÉ. »
# SON CRITÈRE, à appliquer avant d'écrire tout contrôle :
#     SI JE RENOMME UN FICHIER, MON CONTRÔLE CHANGE-T-IL D'AVIS ? Si oui, il épelle.
# La liste d'exceptions par nom se contournait en un fichier : Cowork a posé
# `etudes/ETUDE_20_LE_PILOTE_EXPLIQUE.md`, qui PARLE du pilote sans en être une
# version, et le radar a compté deux versions.
# LA PROPRIÉTÉ EXISTE DÉJÀ, en tête des fichiers, et le protocole de cohérence l'a
# créée pour ça : un document FABRIQUÉ est produit par un programme ; un document
# DÉCIDÉ est écrit à la main. Le PILOTE porte FABRIQUÉ, le SOCLE porte DÉCIDÉ.
# VÉRIFIÉ AVANT D'EMPLOYER : `FABRIQUÉ · Rôle :` est en ligne 8 de PILOTE.md, pas
# en ligne 1 — une fenêtre de six lignes le ratait. On lit les vingt premières.
def _est_version_vivante(chemin_rel, doc):
    """Un fichier est-il la version vivante d'un document, ou seulement un homonyme ?

    ① RÔLE — Compter les versions vivantes d'un document de pilotage sans se tromper
      sur ce qu'est une version. La règle tient en une phrase : un document se déclare
      à sa première ligne non vide. Elle vient de Cowork, le 12-09-2026, après quatre
      rondes sur ce seul contrôle : vos quatre corrections ont chacune été justes et
      chacune a déplacé le défaut d'un cran — aveugle, puis indiscriminé, puis
      sélectif-par-liste, puis sélectif-par-ressemblance ; le point commun n'est pas
      la hâte, c'est que le contrôle est écrit avant que la propriété soit définie.
    ② CONTEXTE D'APPEL — Un seul endroit, le maillon 8, une fois par fichier du projet
      et pour le seul document PILOTE. Mesuré le 20-09-2026 sur une copie du dépôt :
      245 appels, dont un seul rend vrai.
    ③ ENTRÉE — `chemin_rel` : le chemin d'un fichier, relatif au dossier examiné, par
      exemple gouvernance/PILOTE.md · `doc` : le nom du document cherché. Un seul
      appelant, le maillon 8, et il passe toujours PILOTE pour `doc`.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un fichier absent, illisible ou codé autrement
      qu'en UTF-8 rend faux sans faire tomber : la lecture remplace les caractères
      illisibles et toute erreur est rattrapée.
    ⑤ SORTIE — UNE valeur : vrai quand le fichier se termine par .md, porte le nom
      cherché et déclare FABRIQUÉ à sa première ligne non vide ; faux dans tous les
      autres cas. Mesuré le 20-09-2026 sur une copie du dépôt : gouvernance/PILOTE.md
      rend vrai, gouvernance/PILOTE_SOCLE.md rend faux.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre faux si le nom ne se termine pas par .md · ② rendre faux
      si le nom du fichier ne contient pas le nom du document, casse indifférente ·
      ③ ouvrir le fichier et lire ligne par ligne · ④ à la première ligne qui n'est pas
      vide, rendre vrai si elle commence par FABRIQUÉ, faux sinon · ⑤ rendre faux si
      l'ouverture échoue ou si le fichier ne porte aucune ligne non vide.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le contrôle porte sur une DÉCLARATION et non sur une ressemblance,
      parce que les quatre façons précédentes laissaient toutes passer quelque chose,
      et chacune a été mesurée : chercher un NOM laissait passer un fichier
      AVANT_FABRIQUER_LE_PILOTE.txt, un document écrit à la main et le programme qui
      fabrique le pilote · chercher un nom SAUF une liste d'exceptions se contournait
      en un fichier, et Cowork a posé etudes/ETUDE_20_LE_PILOTE_EXPLIQUE.md, qui parle
      du pilote sans en être une version · chercher le mot FABRIQUÉ quelque part dans
      les vingt premières lignes laissait passer un compte rendu qui parle du pilote et
      cite la règle, car ressembler n'est pas déclarer · et vingt lignes est un COMPTE,
      donc un préambule de vingt-six lignes faisait annoncer AUCUNE version vivante sur
      un fichier intact, pendant que le maillon 7 le disait présent. Lire la PREMIÈRE
      ligne non vide n'est ni un nom, ni une liste, ni un compte.
    ⑨ CE QUI CLOCHE — deux points, mesurés le 20-09-2026 :
      ① Elle lit le fichier entier ligne par ligne alors qu'elle s'arrête presque
      toujours à la première, mais elle l'ouvre pour les 245 fichiers du projet à
      chaque passage. Deux filtres la protègent, l'extension et le nom, et c'est ce qui
      rend le coût invisible : mesuré, un passage complet du radar dure 0,47 seconde.
      Le jour où le premier filtre sera élargi, le coût apparaîtra d'un coup.
      ② Le mot déclaré est épelé, FABRIQUÉ, accent compris. Un document qui écrirait
      FABRIQUE sans accent serait compté comme non vivant, et le maillon 8 rendrait un
      constat bloquant sur un fichier parfaitement sain. Le critère qui tranche tient
      en une question : si je change une lettre, mon contrôle change-t-il d'avis ? Ici
      oui.
    ⑩ EFFET — OUVRE et LIT les fichiers du projet qui passent les deux premiers
      filtres. N'écrit aucun fichier, n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas : toute erreur d'ouverture
      ou de lecture est rattrapée et rendue sous la forme d'un faux. Aucun de ses
      appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir qui
        dit ou en est le projet, ce qu'il contient et ce qui cloche
      un fichier fabriqué : un fichier qu'un programme réécrit en entier à
        chaque passage, et que personne n'édite à la main
      un maillon : un groupe de contrôles du radar, désigné par un numéro et
        un nom, par exemple 18-Tâches pour le contrôle des traces laissées par
        les tâches planifiées.
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque
        soir, qui contrôle l'ensemble du système et range chacun de ses
        constats sous un numéro de maillon, par exemple 18-Tâches pour le
        contrôle des traces laissées par les tâches planifiées.
      le projet : le dossier reçu sur la ligne de commande, celui que le radar examine
      Cowork : le relecteur du projet, qui clone le dépôt, casse le code et
        rend ses cassures par écrit
      le Chat : la conversation qui rédige la gouvernance du projet et dépose ses
        versions
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if not chemin_rel.lower().endswith(".md"):
        return False
    if doc.lower() not in os.path.basename(chemin_rel).lower():
        return False
    try:
        with open(os.path.join(PROJ, chemin_rel), encoding="utf-8", errors="replace") as _fh:
            for _ligne in _fh:
                if _ligne.strip():
                    return _ligne.strip().upper().startswith("FABRIQUÉ")
    except Exception:
        return False
    return False

for doc in ["PILOTE"]:
    _versions = [p for p in _chemins if _est_version_vivante(p, doc)]
    n = len(_versions)
    # TROIS ÉTATS, PAS DEUX. `n <= 1` rendait « 1 seule version vivante » quand il y
    # en avait ZÉRO — Cowork l'a mesuré : aucun fichier REPRISE au dépôt, et le radar
    # affichait ✅ en annonçant un chiffre faux. Un contrôle qui affirme le contraire
    # de ce qu'il mesure est pire qu'un contrôle absent.
    if n == 0:
        # DIRE LAQUELLE DES DEUX FAUTES, jamais les deux d'un coup : Cowork, 12-09 —
        # « le message accuse le fichier d'une faute qu'il n'a pas commise », et le
        # maillon 7 le disait présent dans le même rapport. Un fichier qui porte le
        # nom mais ne se déclare pas est un cas DIFFÉRENT d'un fichier absent.
        _portant_le_nom = [p for p in _chemins
                           if p.lower().endswith(".md")
                           and doc.lower() in os.path.basename(p).lower()]
        if _portant_le_nom:
            rapport.append((FAIL, "8-Cohérence",
                            f"{doc} : AUCUN document ne se déclare FABRIQUÉ à sa première "
                            f"ligne non vide. Portent ce nom, sans le déclarer : "
                            f"{', '.join(_portant_le_nom)}. Soit le document a disparu, soit "
                            f"un préambule a été ajouté en tête — et il sera écrasé au "
                            f"prochain passage du fabricant")); score["fail"] += 1
            continue
        rapport.append((FAIL, "8-Cohérence",
                        f"{doc} : AUCUN fichier de ce nom — le document a disparu"))
        score["fail"] += 1
        continue
    _n_avant_check = n
    check("8-Cohérence", n <= 1,
          f"{doc} : 1 seule version vivante ({_versions[0]})",
          f"{doc} : {n} versions présentes — anti-monstre exige 1 seule ({', '.join(_versions)})")

# ═══ COHÉRENCE : chiffres de référence — A-95/A-96 ═══
# L'empreinte n'est PLUS écrite en dur ici (elle devenait fausse à chaque nouveau
# golden). Elle est LUE DANS LE REGISTRE, seule source de vérité (R-701, R-708).
def _golden_attendu():
    """Lit dans le REGISTRE quel fichier de référence fait foi et quelles empreintes il doit porter.

    ① RÔLE — Faire que le radar n'écrive jamais lui-même le nom du golden ni ses
      empreintes. Elles étaient autrefois écrites en dur dans ce programme, et elles
      devenaient fausses à chaque nouveau golden : le radar criait alors sur un fichier
      sain, ou se taisait sur un fichier remplacé. Le REGISTRE est la seule source, et
      un chiffre qui existe ailleurs ne se recopie pas (R-708).
    ② CONTEXTE D'APPEL — Un seul endroit, le maillon 8, une fois par passage, juste
      avant le contrôle de présence du golden. Jamais appelée ailleurs.
    ③ ENTRÉE — Aucun paramètre. Elle va chercher elle-même le chemin du REGISTRE, par
      la fonction qui regarde au dépôt d'abord et au projet en repli.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un REGISTRE introuvable ou illisible ne la fait
      pas tomber.
    ⑤ SORTIE — DEUX valeurs : le nom du fichier de référence attendu, et la liste des
      empreintes attendues. Trois formes selon la branche. Quand le REGISTRE est
      introuvable ou illisible, les deux valeurs sont vides. Quand il est lisible mais
      ne nomme aucun fichier de référence, le nom est vide et la liste peut ne pas
      l'être. Mesuré le 20-09-2026 sur une copie du dépôt : elle rend
      golden_tests_Sam_01-08-2026_20h19.json et deux empreintes, e0d67e1b628bca69 et
      a0e38dd02eaf4ca0.
      [rend: 2]
    ⑥ TRAITEMENT — ① demander le chemin du REGISTRE · ② ne rien rendre s'il est
      introuvable · ③ le lire en entier, en ignorant les caractères illisibles, et ne
      rien rendre si la lecture échoue · ④ y chercher le premier nom de la forme
      golden_tests suivi de .json, écrit entre accents graves · ⑤ y relever tous les
      nombres hexadécimaux de seize caractères précédés du mot empreinte · ⑥ rendre le
      nom et la liste.
    ⑦ UNITÉ — Les empreintes sont des nombres hexadécimaux de SEIZE caractères.
    ⑧ POURQUOI — Elle relève TOUTES les empreintes du REGISTRE et non une seule,
      parce que l'appelant ne vérifie pas laquelle est laquelle : il exige que toutes
      celles annoncées se retrouvent dans le golden. C'est plus sûr qu'un
      rapprochement chiffre à chiffre, qui obligerait le radar à connaître la structure
      interne du golden et donc à la recopier.
    ⑨ CE QUI CLOCHE — trois points, mesurés le 20-09-2026 :
      ① Les deux motifs de recherche épellent une mise en forme. Le nom du fichier
      n'est trouvé que s'il est écrit entre accents graves, et une empreinte n'est
      relevée que si le mot empreinte la précède immédiatement. Changer la mise en
      forme du REGISTRE, sans rien changer à son contenu, ferait disparaître le nom ou
      les empreintes. Dans le premier cas le maillon 8 affiche
      REGISTRE : aucun fichier de référence nommé — impossible de savoir quel golden
      fait foi ; dans le second, le contrôle des empreintes ne se fait pas du tout, en
      silence, puisqu'il n'a lieu que si la liste n'est pas vide.
      ② Elle rend le PREMIER nom rencontré, sans dire s'il y en avait d'autres. Un
      REGISTRE qui citerait deux goldens, par exemple en racontant l'histoire de
      l'ancien, ferait contrôler l'ancien sans que rien ne le signale.
      ③ Elle hérite de la porte de la fonction qui cherche le REGISTRE : mesuré, le
      registre lu était /tmp/depot/gouvernance/REGISTRE_REGLES.md, celui d'une autre
      copie présente sur la machine, et non celui du dossier reçu sur la ligne de
      commande. Le nom du golden qui fait foi peut donc venir d'un autre dépôt que
      celui qu'on examine.
    ⑩ EFFET — OUVRE et LIT le REGISTRE en entier. N'écrit aucun fichier, n'affiche
      rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas : l'échec de lecture est
      rattrapé. Un de ses appels PEUT ne pas revenir : la recherche du REGISTRE lève
      RuntimeError: COMMUN.le_plus_recent introuvable quand plusieurs registres
      homonymes sont trouvés au projet et que programmes/COMMUN.py est absent.
      [sort: non]
    ⑫ DÉFINITIONS
      le golden : le fichier gouvernance/golden_tests_*.json, qui fige des
        chiffres de référence ; tout écart à données identiques est une
        régression.
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
      l'empreinte : le nombre SHA-256 calculé sur le contenu d'un fichier ;
        deux fichiers de même empreinte ont le même contenu
      un maillon : un groupe de contrôles du radar, désigné par un numéro et
        un nom, par exemple 18-Tâches pour le contrôle des traces laissées par
        les tâches planifiées.
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque
        soir, qui contrôle l'ensemble du système et range chacun de ses
        constats sous un numéro de maillon, par exemple 18-Tâches pour le
        contrôle des traces laissées par les tâches planifiées.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
      le projet : le dossier reçu sur la ligne de commande, celui que le radar examine
    """
    # Le REGISTRE vit au DÉPÔT (R-736) : on passe par chemin_registre(),
    # qui cherche au dépôt d'abord et retombe sur le projet en repli.
    _cr, _ = chemin_registre()   # chemin ABSOLU, dépôt d'abord (R-736)
    if not _cr:
        return None, []
    try:
        txt = open(_cr, encoding="utf-8", errors="ignore").read()
    except Exception:
        return None, []
    m = re.search(r"`(golden_tests_[^`]+\.json)`", txt)
    emp = re.findall(r"empreinte ([0-9a-f]{16})", txt)
    return (m.group(1) if m else None), emp

g_att, emp_att = _golden_attendu()
g_present = trouve("golden")
if g_att is None:
    check("8-Cohérence", False, "",
          "REGISTRE : aucun fichier de référence nommé — impossible de savoir quel golden fait foi")
else:
    # COMPARER DES NOMS À DES NOMS, jamais un nom à un chemin (Cowork, 12-09-2026) :
    # `trouve()` rend des chemins relatifs — « gouvernance/golden_tests_….json » —
    # et le REGISTRE désigne un NOM. L'égalité était impossible, d'où un ❌ CRITIQUE
    # permanent sur un fichier pourtant présent. Même famille que chemin_de().
    check("8-Cohérence", any(_norm(g_att) == _norm(os.path.basename(f))
                             for f in g_present if f.lower().endswith(".json")),
          f"Golden de référence présent et conforme au REGISTRE ({g_att})",
          f"Le REGISTRE désigne {g_att} — ABSENT du projet (présents : {g_present})", critique=True)
    # ═══ LE GOLDEN PEUT-IL ENCORE ARBITRER ? ═══
    # X2 de Cowork, 12-09-2026 : « les deux seules lignes du radar sur le golden
    # portent sur sa PRESENCE et sur son NOM. Aucune ne rejoue un chiffre. »
    # La hierarchie dit pourtant : « tout ecart a DONNEES IDENTIQUES = regression ».
    # **Or les donnees ont change, et aujourd hui le calcul du P&L a change trois
    # fois : l horizon, le taux de frais, la conversion d unite. Le seul filet du
    # systeme est absent le jour ou il servirait.** Le radar ne rejoue pas les
    # chiffres — c est le travail du juge des stratégies — mais il DIT si le filet est tendu.
    try:
        # UN MOTIF QUI CHERCHE « golden » ATTRAPE AUSSI CE QUI EN PARLE.
        # Mesure du 13-09 : Cowork depose `TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN...csv`,
        # et mon `trouve("golden")` le prend pour le golden — json.load sur un CSV,
        # et l alerte devient « impossible de dire s il peut arbitrer ».
        # **C est la famille de la journee, une derniere fois : chercher un mot au
        # lieu de designer une propriete.** Le golden est un .json, pas un .csv.
        _jsons = [p for p in g_present if p.lower().endswith(".json")]
        if not _jsons:
            raise ValueError("aucun golden .json parmi " + str(g_present))
        _gj2 = json.load(open(chemin_de(os.path.basename(_jsons[-1])), encoding="utf-8"))
        _meta = _gj2.get("meta", {})
        _att_l = int(_meta.get("nb_lignes_csv", 0))
        _att_e = str(_meta.get("hash_donnees_sha256_16", ""))
        _don = trouve("cac40_ohlcv")
        if _att_l and _don:
            import hashlib as _h
            _brut = open(chemin_de(os.path.basename(_don[-1])), "rb").read()
            _n = _brut.count(b"\n")
            _e = _h.sha256(_brut).hexdigest()[:16]
            # L EMPREINTE TRANCHE, LE COMPTE NE DIT RIEN — Cowork, 13-09-2026.
            # Mon message affichait « 25111 lignes contre 25117 » : le golden compte
            # les lignes de DONNEES, en-tete exclu, et je comptais des lignes BRUTES.
            # **Deux conventions melangees dans une seule phrase d alerte, qui
            # laissait croire a six lignes d ecart la ou il y en a cinq.**
            # L empreinte, elle, a tranche en une seconde : le jeu du golden a ete
            # retrouve sur le Drive, `e472c09da5679ec3` au caractere pres.
            # Le compte n est donc plus affiche du tout : il n apporte rien et il ment.
            check("8-Cohérence", _e == _att_e,
                  f"Le golden peut arbitrer : empreinte des donnees conforme ({_att_e})",
                  f"LE GOLDEN NE PEUT PLUS ARBITRER UN ECART DE CALCUL : empreinte "
                  f"attendue {_att_e}, donnees actuelles {_e}. "
                  f"Tout ecart peut venir des DONNEES et non du calcul — le filet "
                  f"anti-regression est detendu.")
    except Exception as _e2:
        rapport.append((WARN, "8-Cohérence",
                        f"golden : impossible de dire s il peut arbitrer ({_e2})"))
        score["warn"] += 1

    if emp_att:
        emp_ok = False
        for f in g_present:
            if _norm(g_att) == _norm(os.path.basename(f)):   # nom contre nom
                try:
                    gj = json.dumps(json.load(open(chemin_de(f), encoding="utf-8")))
                    emp_ok = all(e in gj for e in emp_att)
                except Exception:
                    pass
        check("8-Cohérence", emp_ok,
              f"Empreintes conformes au REGISTRE ({', '.join(emp_att)})",
              f"EMPREINTES DIVERGENTES entre le golden et le REGISTRE ({', '.join(emp_att)})", critique=True)

# ═══ MAILLON 10 — CONTRÔLE DES TRADES CLÔTURÉS (recalcul par LE MODULE) ═══
# R-708 : ce contrôle ne réimplémente AUCUNE formule. Il importe MODULE_C5_ETENDU_10
# et appelle _c5e10_sortie(), la fonction de référence. Toute divergence entre deux
# implémentations d'un même calcul est inévitable — d'où l'interdiction de recopier.
import importlib.util as _ilu

def _charge_module():
    """Charge le module de signal du projet pour pouvoir le faire recalculer.

    ① RÔLE — Mettre entre les mains du radar le vrai programme qui décide des achats,
      pour qu'il puisse lui redemander de refaire chaque trade clos au lieu d'en
      recopier la formule. C'est ce qui rend possible le maillon 10, le contrôle le
      plus important de tout le radar : il reprend chaque trade du journal, redemande
      au module de refaire le trajet, et compare. Ce qu'il détecte, c'est qu'un
      résultat enregistré ne correspond PLUS à ce que le calcul produit aujourd'hui —
      journal écrit par une ancienne version, modifié après coup, ou abîmé. Cas
      fondateur : du 01-08 au 25-08-2026, le module comptait 85 opérations là où la
      référence en attendait 100, pendant vingt-cinq jours.
    ② CONTEXTE D'APPEL — Un seul endroit, juste avant le maillon 10, une fois par
      passage. Son résultat sert ensuite à trois maillons : le 10 pour le recalcul, le
      11 pour l'objectif de gain et la perte acceptée des positions ouvertes, et le 12
      pour le prix d'entrée.
    ③ ENTRÉE — Aucun paramètre. Elle parcourt la liste des noms de fichiers relevée au
      démarrage du programme.
    ④ CONDITIONS D'ENTRÉE — Le module trouvé doit pouvoir s'exécuter de bout en bout,
      puisque le charger revient à le lancer. Il doit ensuite porter la fonction de
      sortie et les deux réglages que les maillons 11 et 12 lui demanderont.
    ⑤ SORTIE — DEUX valeurs : le module chargé et le nom du fichier. Trois formes
      selon la branche. Quand tout s'est bien passé, le module et son nom. Quand le
      fichier a été trouvé mais n'a pas pu être chargé, rien et le nom suivi de la
      mention échec import et du message de l'erreur. Quand aucun fichier ne porte ce
      nom, deux valeurs vides. Mesuré le 20-09-2026 sur une copie du dépôt : elle rend
      le module et le nom MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py.
      [rend: 2]
    ⑥ TRAITEMENT — ① trier les noms de fichiers du projet par ordre alphabétique
      DÉCROISSANT · ② s'arrêter au premier dont la forme unique contient
      MODULE_C5_ETENDU_10 et qui se termine par .py · ③ le charger comme un programme,
      ce qui l'exécute · ④ rendre le module et son nom · ⑤ si le chargement échoue,
      rendre rien et un nom accompagné du message de l'erreur · ⑥ si aucun fichier ne
      correspond, rendre deux valeurs vides.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le module est chargé au lieu d'être nommé en dur dans une
      instruction d'import, parce que son nom porte une date et change donc à chaque
      nouvelle version. Et il est chargé plutôt que recopié parce que deux écritures
      d'un même calcul divergent toujours (R-708) : c'est l'interdiction même sur
      laquelle repose le maillon 10, et le code la rappelle à l'endroit où il s'en
      sert.
    ⑨ CE QUI CLOCHE — trois points, tous mesurés le 20-09-2026 :
      ① LE MODULE RETENU EST LE DERNIER DANS L'ALPHABET, PAS LE PLUS RÉCENT. Le tri
      est décroissant sur le nom nu, et les noms du projet commencent par le jour de la
      semaine : sur deux versions nommées _Jeu_30-07 et _Mar_09-09, le tri décroissant
      rend _Mar_09-09, mais sur _Sam_01-08 et _Ven_05-09 il rendrait _Ven_05-09 qui
      est bien le plus récent, et sur _Jeu_17-09 et _Sam_01-08 il rendrait _Sam_01-08
      qui ne l'est pas. Le projet a posé le 12-09-2026 une fonction qui lit la date du
      nom, précisément pour cela, et elle n'est pas employée ici. Le cas ne se
      présente pas aujourd'hui : un seul fichier porte ce nom.
      ② CHARGER LE MODULE, C'EST L'EXÉCUTER. Tout ce que ce programme fait au niveau
      du fichier est fait, à chaque passage du radar. Le module de signal actuel se
      contente de définir des fonctions et des réglages, donc rien de visible ne se
      produit ; un module qui écrirait un fichier ou lirait le réseau au chargement le
      ferait sans que le radar le sache.
      ③ La recherche épelle le nom MODULE_C5_ETENDU_10. Une stratégie nouvelle mise en
      service demain avec un autre module ne serait pas contrôlée par le maillon 10 :
      son nom ne figure pas dans le code. C'est exactement la faute que le maillon 3 a
      fermée le 30-08-2026 en lisant le registre au lieu de porter des noms en dur, et
      elle est restée ici.
    ⑩ EFFET — OUVRE, LIT ET EXÉCUTE un fichier de programme. N'écrit aucun fichier
      lui-même, n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas : l'échec du chargement
      est rattrapé et rendu sous forme de message. Un de ses appels PEUT ne pas
      revenir : le module chargé est exécuté entièrement, et rien ne borne ce qu'il
      fait.
      [sort: non]
    ⑫ DÉFINITIONS
      le module de signal : le programme qui décide quelles valeurs acheter
      un trade : une opération simulée, de l'achat à la revente
      un maillon : un groupe de contrôles du radar, désigné par un numéro et
        un nom, par exemple 18-Tâches pour le contrôle des traces laissées par
        les tâches planifiées.
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque
        soir, qui contrôle l'ensemble du système et range chacun de ses
        constats sous un numéro de maillon, par exemple 18-Tâches pour le
        contrôle des traces laissées par les tâches planifiées.
      le projet : le dossier reçu sur la ligne de commande, celui que le radar examine
      une stratégie : une règle qui dit QUOI acheter, avec son objectif de
        gain, sa perte acceptée et son horizon
      l'objectif de gain : le pourcentage de hausse à partir duquel la
        position se referme sur un gain
      la perte acceptée : le pourcentage de baisse à partir duquel la position
        se referme sur une perte
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
    """
    for f in sorted(fichiers, reverse=True):
        if _norm("MODULE_C5_ETENDU_10") in _norm(f) and f.endswith(".py"):
            try:
                spec = _ilu.spec_from_file_location("mod_c5e10", chemin_de(f))
                m = _ilu.module_from_spec(spec); spec.loader.exec_module(m)
                return m, f
            except Exception as e:
                return None, f"{f} (échec import : {e})"
    return None, None

# A-250 : ces deux variables ne sont définies que dans la branche else ci-dessous,
# celle où le module s'importe. Sans ces valeurs par défaut, un échec d'import fait
# planter le maillon 13 (NameError sur f_tr) AVANT que le rapport ne soit imprimé —
# l'audit se tait entièrement le soir précis où il devrait alerter.
f_tr = None
trades = []
def _lire_csv(motifs):
    """Lit le premier fichier de tableur trouvé pour un motif, et rend ses lignes.

    ① RÔLE — Donner aux maillons le contenu d'un fichier de tableur sans qu'aucun
      d'eux n'ait à savoir où il est rangé, ni à écrire son propre lecteur. Elle est
      définie hors de la branche qui charge le module de signal, exprès : le maillon 11
      en a besoin même quand ce module ne se charge pas. Sans cela, un échec de
      chargement faisait tomber le maillon suivant AVANT que le rapport ne soit
      affiché, et l'audit se taisait entièrement le soir précis où il aurait dû
      alerter.
    ② CONTEXTE D'APPEL — Neuf endroits, dans cinq maillons : le journal des trades,
      les cours du jour et l'historique des cours au maillon 10 · le registre des
      stratégies au maillon 3 · le registre des stratégies, les positions ouvertes et
      le référentiel des valeurs au maillon 17 · les positions ouvertes au maillon 11 ·
      l'historique des cours au maillon 14.
    ③ ENTRÉE — `motifs` : la liste des fragments de nom à essayer, dans l'ordre. Les
      neuf appels n'en passent qu'un seul chacun, par exemple journal_trades ou
      cac40_ohlcv.
    ④ CONDITIONS D'ENTRÉE — Aucune. Une liste vide, un motif qui ne correspond à rien,
      un fichier illisible ou mal formé rendent tous un résultat vide sans faire
      tomber.
    ⑤ SORTIE — DEUX valeurs : la liste des lignes, chacune sous forme de
      correspondances entre un nom de colonne et sa valeur, et le chemin relatif du
      fichier lu. Deux formes selon la branche : une liste vide et rien du tout quand
      aucun fichier n'a pu être lu. Mesuré le 20-09-2026 sur une copie du dépôt :
      appelée avec cac40_ohlcv elle rend 25 116 lignes et le chemin
      donnees/cac40_ohlcv.csv ; appelée avec zzz elle rend une liste vide et rien.
      [rend: 2]
    ⑥ TRAITEMENT — ① essayer chaque motif dans l'ordre reçu · ② pour chaque motif,
      essayer chaque fichier trouvé dans l'ordre alphabétique · ③ l'ouvrir en UTF-8 en
      écartant la marque d'ordre des octets, et lire toutes ses lignes · ④ s'arrêter au
      PREMIER fichier lu sans erreur et rendre ses lignes avec son chemin · ⑤ passer au
      suivant sans rien dire si la lecture échoue · ⑥ rendre une liste vide et rien
      quand tout a échoué.
    ⑦ UNITÉ — Un NOMBRE DE LIGNES de tableur, en-tête exclu.
    ⑧ POURQUOI — Elle écarte la marque d'ordre des octets à l'ouverture parce que les
      fichiers du projet ont plusieurs origines — un tableur, un service web, deux
      programmes — et que cette marque invisible en tête de fichier colle au nom de la
      première colonne. Le nom de colonne devient alors introuvable, et le maillon
      compte zéro ligne utilisable sans qu'aucune erreur ne s'affiche.
    ⑨ CE QUI CLOCHE — trois points, tous mesurés le 20-09-2026 :
      ① ELLE PREND LE PREMIER FICHIER DANS L'ALPHABET, ET DEUX MOTIFS EN TROUVENT
      PLUSIEURS. Appelée avec cac40_ohlcv, elle a le choix entre
      donnees/cac40_ohlcv.csv et temoins/TEMOIN_cac40_ohlcv_JEU_DU_GOLDEN_01-08-2026.csv ;
      c'est le premier qui est pris, mais uniquement parce que la lettre d précède la
      lettre t. Renommer un dossier changerait le fichier contrôlé, et rien ne le
      dirait. Le radar dispose d'une fonction qui lit la date portée par le nom,
      précisément pour ces cas, et elle n'est pas employée ici.
      ② UN FICHIER ILLISIBLE EST SILENCIEUSEMENT REMPLACÉ PAR LE SUIVANT, OU PAR RIEN.
      L'échec de lecture est rattrapé sans un mot. Un historique des cours abîmé ferait
      donc rendre une liste vide, et le maillon 14 afficherait
      Historique des cours introuvable — séances non vérifiables : le message accuse
      une absence là où il s'agit d'un fichier présent et cassé.
      ③ Elle lit le fichier entier en mémoire, quelle que soit sa taille. Mesuré :
      l'historique des cours fait 25 116 lignes, ce qui ne pose aucun problème
      aujourd'hui, et il grandit d'environ 39 lignes par séance de bourse.
    ⑩ EFFET — OUVRE et LIT des fichiers de tableur. N'écrit aucun fichier, n'affiche
      rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas : toute erreur de lecture
      est rattrapée. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      un maillon : un groupe de contrôles du radar, désigné par un numéro et
        un nom, par exemple 18-Tâches pour le contrôle des traces laissées par
        les tâches planifiées.
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque
        soir, qui contrôle l'ensemble du système et range chacun de ses
        constats sous un numéro de maillon, par exemple 18-Tâches pour le
        contrôle des traces laissées par les tâches planifiées.
      le module de signal : le programme qui décide quelles valeurs acheter
      la marque d'ordre des octets : trois octets invisibles que certains
        tableurs posent en tête d'un fichier et qui, s'ils ne sont pas
        écartés, se collent au nom de la première colonne
      le référentiel des valeurs : donnees/REFERENTIEL_VALEURS_*.csv, la liste des valeurs à suivre, avec pour chacune son mnémonique et sa place de cotation.
      le registre des stratégies : le fichier `cac40_strategies.csv`, une
        ligne par stratégie, qui porte leur état civil — identifiant,
        réglages, résultats connus
      une séance : une journée de bourse pour une valeur, avec son ouverture,
        son plus haut, son plus bas, sa clôture et son volume.
      le projet : le dossier reçu sur la ligne de commande, celui que le radar examine
      un motif : un morceau de nom passé à une fonction de recherche, par
        exemple trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
    """
    for m in motifs:
        for f in trouve(m):
            try:
                with open(chemin_de(f), newline="", encoding="utf-8-sig") as fh:
                    return list(csv.DictReader(fh)), f
            except Exception:
                pass
    return [], None

MOD, MOD_NOM = _charge_module()
if MOD is None:
    rapport.append((FAIL, "10-Trades",
        f"MODULE C5-ETENDU-10 introuvable ou non importable ({MOD_NOM}) — "
        "recalcul des trades IMPOSSIBLE (R-708 interdit de réimplémenter la formule)"))
    score["fail"] += 1
else:
    trades, f_tr = _lire_csv(["journal_trades"])
    cours_rows, _ = _lire_csv(["cours_nouveaux"])
    hist_rows, _  = _lire_csv(["cac40_ohlcv"])

    if f_tr is None:
        rapport.append((OK, "10-Trades", "Aucun trade clôturé à ce jour — rien à contrôler"))
        score["ok"] += 1
    else:
        # séries OHLCV par valeur, au format attendu par le module
        serie = {}
        for r in (hist_rows + cours_rows):
            try:
                b = {"date": r["date"], "open": float(r["open"]), "high": float(r["high"]),
                     "low": float(r["low"]), "close": float(r["close"]),
                     "volume": float(r.get("volume") or 1)}
                serie.setdefault(_norm_val(r["valeur"]), {})[r["date"]] = b
            except Exception:
                pass
        serie = {v: [d[k] for k in sorted(d)] for v, d in serie.items()}

        ecarts, ecarts_frais, controles, sans_cours = [], [], 0, 0
        for t in trades:
            try:
                v, d_e = t["valeur"], t["date_entree"]
                # A-175 (11-08) : le module recalcule la sortie AU PRIX TP (convention). On
                # compare donc au P&L de CONVENTION du journal quand il existe
                # (pnl_net_convention_eur), et non au P&L reel (pnl_net_eur) qui peut refleter
                # une sortie TP_GAP au-dessus du TP. Repli sur pnl_net_eur pour les trades
                # anciens sans colonne convention.
                _pnl_conv = str(t.get("pnl_net_convention_eur") or "").strip()
                _pnl_ref = _pnl_conv if _pnl_conv else str(t["pnl_net_eur"])
                pnl_inscrit = float(_pnl_ref.replace(" ", "").replace(",", "."))
            except Exception:
                continue
            oh = serie.get(_norm_val(v))
            if not oh:
                sans_cours += 1; continue
            idx = [k for k, b in enumerate(oh) if b["date"] == d_e]
            if not idx or idx[0] == 0:
                sans_cours += 1; continue
            # le module entre à i_signal+1 : on lui passe donc l'indice précédent
            res = MOD._c5e10_sortie(oh, idx[0] - 1)
            if res is None:
                sans_cours += 1; continue
            controles += 1
            # A-15 — DEUX natures d'écart, à ne pas confondre :
            #  · écart de CONVENTION DE FRAIS : le journal inscrit les frais RÉELS
            #    (0,15 %/ordre), le module applique un forfait. Écart faible et attendu
            #    tant que la décision A-50 n'est pas prise → ⚠, pas ❌.
            #  · écart de CALCUL : tout le reste → ❌.
            d = abs(res["pnl"] - pnl_inscrit)
            if d > SEUIL_ECART_CALCUL:
                ecarts.append(f"{v} {d_e} : journal {pnl_inscrit:+.0f} € vs module "
                              f"{res['pnl']:+.0f} € ({res['motif']})")
            elif d > 1.0:
                ecarts_frais.append(f"{v} {d_e} : {d:.0f} €")

        if ecarts:
            rapport.append((FAIL, "10-Trades",
                f"ÉCART DE CALCUL sur {len(ecarts)}/{controles} trade(s) : " + " | ".join(ecarts[:3])
                + (" …" if len(ecarts) > 3 else "")))
            score["fail"] += 1
        elif controles:
            rapport.append((OK, "10-Trades",
                f"{controles} trade(s) clôturé(s) recalculé(s) PAR LE MODULE ({MOD_NOM}) — "
                f"aucun écart de CALCUL (seuil {SEUIL_ECART_CALCUL:.0f} €)"))
            score["ok"] += 1
        else:
            rapport.append((WARN, "10-Trades",
                "Journal des trades présent mais aucun trade contrôlable (cours d'entrée introuvables)"))
            score["warn"] += 1
        if ecarts_frais:
            rapport.append((WARN, "10-Trades",
                f"{len(ecarts_frais)} trade(s) avec écart de CONVENTION DE FRAIS (attendu tant "
                f"que A-50 n'est pas tranchée, ce n'est PAS une erreur de calcul) : "
                + " | ".join(ecarts_frais[:3]) + (" …" if len(ecarts_frais) > 3 else "")))
            score["warn"] += 1
        if sans_cours:
            rapport.append((WARN, "10-Trades",
                f"{sans_cours} trade(s) non vérifiable(s) : cours de la séance d'entrée absents"))
            score["warn"] += 1

# ═══ MAILLON 17 — LE REGISTRE DIT-IL LA VÉRITÉ SUR CE QUI TOURNE ? ═══
# Né des défauts du 22/08 : une stratégie tournait depuis onze jours sans exister
# au registre, et la fiche de l'autre portait l'univers de la première. Aucun des
# seize maillons ne comparait le DÉCLARÉ au RÉEL. Celui-ci le fait.
# AUTONOME À DESSEIN : il relit lui-même ses deux fichiers et ne dépend d'aucune
# variable d'un autre maillon (leçon de A-250/A-251/A-258).
# ═══ MAILLON 3 — CALCUL SIGNAUX ═══
# LE RADAR LIT LE REGISTRE, IL NE PORTE PLUS DE NOMS EN DUR.
# Premiere version : trois noms de strategies etaient ecrits DANS LE CODE —
# C5-ETENDU-10, C5-EI, C4-RAV — et le maillon alertait « strategie production
# sans code » sur les deux dernieres. Or le registre les donne au stade
# LABORATOIRE : deux FAUSSES ALERTES repetees chaque soir depuis des semaines,
# usant l'attention sur un rapport que personne ne lit deja.
# Et la reciproque etait pire : une strategie reellement mise en service
# demain n'aurait ete surveillee par AUCUN maillon, son nom ne figurant pas
# dans le code. Arbitrage A-324 du 30-08-2026 : est en service ce qui porte
# QA ou PRODUCTION au registre, et rien d'autre.
# on emploie le lecteur DEJA ECRIT, jamais un second : deux lectures du meme
# fichier divergent toujours (famille A-308).
_s3, _f_s3 = _lire_csv(["cac40_strategies"])
_serv3 = [s for s in _s3
          if (s.get("etat_vie") or "").strip().upper() in ("QA", "PRODUCTION")]
# LE LIEN FICHE -> CODE PASSE PAR LA COLONNE `chemin`, PAS PAR LE NOM.
# Premiere version : on cherchait la racine de l'identifiant dans les noms de
# fichiers — « C5E10 » ne se trouve nulle part, le module s'appelant
# MODULE_C5_ETENDU_10. Le maillon denoncait alors DEUX strategies qui ont
# pourtant leur code. Chercher un code par ressemblance de nom est exactement
# ce que le chapitre IDENTITE interdit ; tant que la fiche ne DESIGNE pas son
# module, ce controle ne peut rien affirmer.
_MODULES = {"C5E10-QA-V1": "MODULE_C5_ETENDU",
            "C5E10-OBS-V1": "MODULE_C5_ETENDU"}
_sans_code, _sans_lien = [], []
for s in _serv3:
    _id = (s.get("id") or "").strip()
    _mot = _MODULES.get(_id)
    if not _mot:
        _sans_lien.append(_id)
    elif not existe(_mot):
        _sans_code.append("%s (%s)" % (_id, _mot))
check("3-Calcul", not _sans_lien,
      "Toute stratégie en service désigne son module de signal",
      "AUCUN MODULE CONNU POUR : %s — la fiche ne dit pas quel code produit "
      "ses signaux, le lien n'existe qu'en mémoire humaine" % ", ".join(_sans_lien))
check("3-Calcul", bool(_serv3),
      "%d stratégie(s) en service, dont le code est vérifié" % len(_serv3),
      "Aucune stratégie en service au registre : rien à vérifier ici")
check("3-Calcul", not _sans_code,
      "Toute stratégie en service a son code de signal",
      "EN SERVICE SANS CODE DE SIGNAL : %s — elle prend des positions et son "
      "calcul est introuvable" % ", ".join(_sans_code), critique=True)

_strats, _f_str = _lire_csv(["cac40_strategies"])
_p17, _f_p17 = _lire_csv(["positions_ouvertes"])
if _f_str is None:
    rapport.append((WARN, "17-Registre", "Registre des stratégies ABSENT — comparaison impossible"))
    score["warn"] += 1
else:
    ETATS_OFFICIELS = {"LABO", "QA", "PRODUCTION", "SUSPENDUE",
                       "JAMAIS_VECUE", "VECUE-PUIS-ARCHIVEE"}
    # ① les états employés existent-ils ? A-194 en définit six, pas un de plus.
    _hors = sorted({(s.get("etat_vie") or "").strip() for s in _strats
                    if (s.get("etat_vie") or "").strip()} - ETATS_OFFICIELS)
    check("17-Registre", not _hors,
          "États de vie tous officiels (six valeurs admises, A-194)",
          f"ÉTAT DE VIE INCONNU : {', '.join(_hors)} — A-194 n'en définit que six")
    # ② toute stratégie qui écrit des positions a-t-elle une fiche ?
    # LES NOMS D'UNE STRATÉGIE SE LISENT AU CONTRAT (R-708 : deux implémentations
    # d'une même chose divergent toujours). Jusqu'au 28-09-2026, ce maillon
    # recopiait trois fois la règle « l'identifiant, et le nom avant la
    # parenthèse » de `noms_d_une_strategie`. Sans le contrat, le radar ne se
    # tait pas (A-250) : il le dit, et garde la règle écrite ici, NOMMÉE comme repli.
    try:
        from CONTRATS_DES_FICHIERS import noms_d_une_strategie as _noms_17
    except Exception as _e17:
        rapport.append((WARN, "17-Registre", "CONTRATS_DES_FICHIERS illisible "
                        f"({type(_e17).__name__}) — noms des stratégies lus par le repli du radar"))
        score["warn"] += 1
        def _noms_17(s):
            """Rend les noms d'une stratégie quand le contrat ne se charge pas.

            ① RÔLE — Repli de `noms_d_une_strategie`, pour que le maillon 17 tourne
              sans le contrat au lieu de faire tomber le radar.
            ② CONTEXTE D'APPEL — Le maillon 17, seulement si l'import du contrat a
              échoué ; l'échec est alors écrit au rapport.
            ③ ENTRÉE — `s` : une ligne du registre des stratégies, un dictionnaire.
            ④ CONDITIONS D'ENTRÉE — Aucune : une case absente vaut vide.
            ⑤ SORTIE — UNE valeur : l'ensemble {identifiant, nom avant la
              parenthèse}, sans la chaîne vide.
              [rend: 1]
            ⑥ TRAITEMENT — Même règle que le contrat, écrite une seconde fois.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — « L'audit se tait entièrement le soir précis où il devrait
              alerter » (A-250) : sans repli, un contrat cassé ferait tomber le radar
              entier (mesuré : sans cette fonction, zéro ligne du maillon 17 et le
              code 1, épreuve E4 de tests/EPREUVES_DES_NOMS_AU_CONTRAT).
            ⑨ CE QUI CLOCHE — C'est une copie de la règle du contrat (R-708) : si le
              contrat change, elle ne suit pas. Elle ne sert que le soir où il ne se
              charge pas, et ce soir-là le rapport le dit.
            ⑩ EFFET — Aucun.
            ⑪ TERMINAISON — Rend toujours la main.
              [sort: non]
            """
            return {(s.get("id") or "").strip(), (s.get("nom") or "").split(" (")[0].strip()} - {""}
    _noms = set().union(*(_noms_17(s) for s in _strats))
    # LES STRATEGIES EN SERVICE SE LISENT AU REGISTRE, PAS DANS LES POSITIONS
    # OUVERTES. Premiere version : on prenait les strategies presentes dans
    # positions_ouvertes.csv. Le 30-08-2026, apres la cloture UNIBAIL, ce
    # fichier est VIDE — le maillon a donc rendu « 0 active » AU VERT, alors
    # que DEUX strategies tournent. Un faux silence est plus dangereux qu'une
    # fausse alerte : personne ne regarde ce qui est vert.
    # A-324 tranche le perimetre : est en service ce qui porte QA ou PRODUCTION.
    EN_SERVICE = {"QA", "PRODUCTION"}
    _serv = [s for s in _strats
             if (s.get("etat_vie") or "").strip().upper() in EN_SERVICE]
    check("17-Registre", len(_serv) > 0,
          f"{len(_serv)} stratégie(s) en service au registre (QA ou PRODUCTION)",
          "AUCUNE stratégie en service au registre — si c'est voulu, aucune "
          "position ne devrait s'ouvrir ; sinon un état a été mal posé")
    # les strategies qui engagent des positions doivent TOUTES avoir leur fiche
    _actives = {(p.get("strategie") or "").strip() for p in _p17
                if (p.get("strategie") or "").strip()}
    _orphelines = sorted(_actives - _noms)
    check("17-Registre", not _orphelines,
          f"Toute stratégie qui engage une position a sa fiche "
          f"({len(_actives)} avec position ouverte)",
          f"STRATÉGIE SANS FICHE — elle engage des positions et n'existe pas au "
          f"registre : {', '.join(_orphelines)}", critique=True)
    # et toute strategie EN SERVICE doit avoir sa fiche complete
    _incompletes = []
    for s in _serv:
        _m = [c for c in ("indicateurs", "univers", "tp", "sl", "horizon",
                          "periode")
              if not (s.get(c) or "").strip()
              or (s.get(c) or "").strip().lower() in ("a renseigner",
                                                      "à renseigner", "—", "-")]
        if _m:
            _incompletes.append("%s (%s)" % (s.get("id"), ", ".join(_m)))
    check("17-Registre", not _incompletes,
          "Toute stratégie en service a sa fiche complète",
          "EN SERVICE AVEC FICHE INCOMPLÈTE : " + " · ".join(_incompletes))
    # ③ l'univers déclaré correspond-il aux valeurs réellement jouées ?
    # On ne vérifie que l'INCLUSION : une valeur jouée hors de l'univers déclaré
    # est une faute certaine ; l'inverse ne prouve rien (une valeur peut ne pas
    # avoir signalé). Le rapprochement passe par le référentiel des valeurs.
    _ref, _f_ref = _lire_csv(["REFERENTIEL_VALEURS"])
    _mnemo = {}
    for _r in _ref:
        _m = (_r.get("mnemonique") or "").strip()
        _n = (_r.get("nom_usuel") or "").strip()
        if _m and _n:
            _mnemo[_m] = _norm_val(_n)
    if not _mnemo:
        rapport.append((WARN, "17-Registre",
            "Univers NON VÉRIFIABLE — référentiel des valeurs introuvable"))
        score["warn"] += 1
    else:
        _univ = {}
        for s in _strats:
            _u = (s.get("univers") or "").strip()
            # une position peut porter l'identifiant OU le nom court : les deux
            # désignent la même fiche (jusqu'au 28-09-2026, le nom seul était lu,
            # et une position écrite sous l'identifiant échappait au contrôle)
            for _cle in (_noms_17(s) if _u else ()):
                _univ[_cle] = {_mnemo.get(x.strip(), _norm_val(x.strip()))
                               for x in _u.split(",") if x.strip()}
        _ecarts = set()
        for p in _p17:
            _s = (p.get("strategie") or "").strip()
            _v = _norm_val(p.get("valeur") or "")
            if _s in _univ and _v and not any(
                    _v == u or _v.startswith(u) or u.startswith(_v) for u in _univ[_s]):
                _ecarts.add(f"{_s} joue {p.get('valeur')}")
        check("17-Registre", not _ecarts,
              "Valeurs jouées cohérentes avec l'univers déclaré",
              f"VALEUR HORS UNIVERS DÉCLARÉ : {' | '.join(sorted(_ecarts))} — "
              "la fiche décrit une autre stratégie que celle qui tourne")

# ═══ MAILLON 12 — A-13 : LE PRIX D'ENTRÉE EST-IL BIEN L'OUVERTURE ? ═══
# R-601 : l'entrée se fait à l'OUVERTURE du lendemain du signal. Un prix d'entrée
# qui ne serait pas l'open de sa séance trahirait une entrée impossible en vrai.
if MOD is not None and f_tr is not None:
    faux_open, verif_open = [], 0
    for t in trades:
        try:
            v, d_e = t["valeur"], t["date_entree"]
            pe = float(str(t["prix_entree"]).replace(" ", "").replace(",", "."))
        except Exception:
            continue
        oh = serie.get(_norm_val(v))
        if not oh:
            continue
        b = [x for x in oh if x["date"] == d_e]
        if not b:
            continue
        verif_open += 1
        if abs(b[0]["open"] - pe) > 0.01:
            faux_open.append(f'{v} {d_e} : entrée {pe} vs ouverture {b[0]["open"]}')
    if verif_open:
        check("12-EntréeOpen", not faux_open,
              f"{verif_open} trade(s) : prix d'entrée = ouverture de la séance (R-601 respectée)",
              f"ENTRÉE HORS OUVERTURE (R-601 violée) : {' | '.join(faux_open[:3])}", critique=True)

# ═══ MAILLON 13 — A-84 : LE CREUX EN COURS (contrôle QUOTIDIEN) ═══
# R-502 : creux depuis le plus haut > 20 % → la stratégie repasse les 7 critères.
# R-507 : 5 pertes consécutives → revue complète.
if f_tr is not None and trades:
    SEUIL_CREUX = 0.20 * 100000      # R-502, seuil porté à 20 % le 01/08
    ALERTE_PERTES = 5                # R-507
    # UNE SÉRIE PAR STRATÉGIE ET PAR COMPTABILITÉ, JAMAIS TOUTES ENSEMBLE (défaut 3 de
    # A-491, 27-09-2026 ; trouvé par le relecteur du Chat). Le journal porte le même
    # trade une fois par comptabilité, et plusieurs stratégies : les additionner
    # comptait la vente d'Unibail du 27-08 quatre fois — « Série de pertes en cours : 4 »
    # alors que chaque stratégie n'en a qu'une, et une seule perte de plus déclenchait
    # l'alarme R-507 à tort. Les deux comptabilités ne s'additionnent jamais (R-604).
    # Chaque série suit l'ordre des dates de sortie, pas l'ordre du fichier.
    # Une stratégie s'écrit sous deux noms au journal (identifiant du registre, nom
    # court des lignes anciennes) : on la ramène à son identifiant par la fonction
    # déclarée une fois au contrat (R-708). Un nom hors des stratégies vivantes, ou
    # partagé par deux d'entre elles, reste tel quel.
    # LE RADAR NE SE TAIT PAS SI LE CONTRAT NE SE CHARGE PAS (A-250 : « l'audit se tait
    # entièrement le soir précis où il devrait alerter ») : sans lui, les séries se
    # font sur le nom brut, et on le DIT. Seules les stratégies vivantes sont
    # rattachées ; un nom qui désignerait deux stratégies vivantes n'est rattaché à
    # aucune, et on le dit aussi (relecteur du Chat, tour 2, 27-09-2026).
    _vers_id, _ambigus = {}, set()
    try:
        from CONTRATS_DES_FICHIERS import noms_d_une_strategie as _noms_de_la_strategie
        for _l in (_serv3 or []):
            for _n in _noms_de_la_strategie(_l):
                _id = (_l.get("id") or "").strip()
                if _vers_id.get(_n, _id) != _id:
                    _ambigus.add(_n)
                _vers_id[_n] = _id
        for _n in _ambigus:
            del _vers_id[_n]
        if _ambigus:
            rapport.append((WARN, "13-Creux", "Nom(s) désignant plusieurs stratégies vivantes, "
                            f"séries tenues sur le nom brut : {', '.join(sorted(_ambigus))}"))
            score["warn"] += 1
    except Exception as _e:
        rapport.append((WARN, "13-Creux", "CONTRATS_DES_FICHIERS illisible "
                        f"({type(_e).__name__}) — séries tenues sur le nom brut du journal"))
        score["warn"] += 1
    def _series_du_journal(lignes, vers_id):
        """Rend {(strategie, comptabilite): (serie de pertes, creux en cours, marque, cumul, pire creux)}.

        ① RÔLE — Le calcul du maillon 13, sorti pour être éprouvé chaque soir sur un
          témoin (Cowork, 27-09-2026 à 22h46 : le défaut remis, tout restait vert).
        ② CONTEXTE D'APPEL — Le maillon 13, deux fois : sur le témoin, puis sur le journal.
        ③ ENTRÉE — `lignes` : des lignes du journal · `vers_id` : nom écrit → identifiant.
        ④ CONDITIONS D'ENTRÉE — Aucune : un résultat illisible est sauté.
        ⑤ SORTIE — UNE valeur : le dictionnaire ci-dessus.
          [rend: 1]
        ⑥ TRAITEMENT — ① trier par date de sortie · ② grouper par identifiant et
          comptabilité · ③ pour chaque groupe, cumuler, suivre la marque et le creux,
          et compter les pertes depuis le dernier gain.
        ⑦ UNITÉ — EUROS ; la série en NOMBRE DE TRADES.
        ⑧ POURQUOI — Défaut 3 de A-491 : tout additionné, Unibail comptait quatre fois.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend toujours la main.
          [sort: non]
        """
        groupes = {}
        for t in sorted(lignes, key=lambda x: (x.get("date_sortie") or "")):
            try:
                _v = float(str(t["pnl_net_eur"]).replace(" ", "").replace(",", "."))
            except Exception:
                continue
            _nom = (t.get("strategie") or "?").strip()
            _cle = (vers_id.get(_nom, _nom), (t.get("comptabilite") or "NON DITE").strip())
            groupes.setdefault(_cle, []).append(_v)
        rendu = {}
        for _k, pnls in groupes.items():
            eq = pic = creux = 0.0
            for p in pnls:
                eq += p; pic = max(pic, eq); creux = max(creux, pic - eq)
            serie = 0
            for p in pnls:
                serie = serie + 1 if p <= 0 else 0
            rendu[_k] = (serie, pic - eq, pic, eq, creux)
        return rendu

    def _constats_13(lignes, vers_id):
        """Rend les constats du maillon 13 : [(condition, phrase si vrai, phrase si faux, critique)].

        ① RÔLE — Tout le jugement du maillon 13, seuils compris, en un chemin que le
          témoin rejoue chaque soir : c'est ce chemin même qui juge le journal.
        ② CONTEXTE D'APPEL — Le maillon 13, deux fois : sur le témoin, puis sur le journal.
        ③ ENTRÉE — `lignes` : des lignes du journal · `vers_id` : nom écrit → identifiant.
        ④ CONDITIONS D'ENTRÉE — Aucune.
        ⑤ SORTIE — UNE valeur : la liste des constats, trois par stratégie et
          comptabilité (creux R-502, série R-507, bilan), rangés par identifiant.
          [rend: 1]
        ⑥ TRAITEMENT — ① séries par `_series_du_journal` · ② pour chacune, comparer
          le creux au seuil de 20 % et la série au seuil de 5 pertes.
        ⑦ UNITÉ — EUROS ; la série en NOMBRE DE TRADES.
        ⑧ POURQUOI — Relecteur du Chat, 27-09-2026 : le témoin n'éprouvait que le
          calcul des séries ; forcer une alarme à vrai, ou appeler sans les noms du
          registre, le laissait vert. Témoin et journal passent désormais par ici.
        ⑨ CE QUI CLOCHE — Un ❌ du radar ne fait pas rougir le pas du circuit (le
          radar sort toujours en code 0, par construction) : il se lit dans le
          journal du pas et dans rapports/audit_du_jour.md, que le rituel lit.
        ⑩ EFFET — Aucun : c'est l'appelant qui écrit au rapport.
        ⑪ TERMINAISON — Rend toujours la main.
          [sort: non]
        """
        rendu = []
        for (_s, _c), (serie_pertes, creux_actuel, pic, eq, creux) in sorted(_series_du_journal(lignes, vers_id).items()):
            _qui = f"{_s} · {_c.replace('_', ' ')}"
            rendu.append((creux_actuel <= SEUIL_CREUX,
                  f"{_qui} : creux en cours {creux_actuel:,.0f} € ({100*creux_actuel/100000:.1f} %) — sous le seuil de 20 %"
                  .replace(",", " "),
                  f"{_qui} : SEUIL DE CREUX FRANCHI : {creux_actuel:,.0f} € ({100*creux_actuel/100000:.1f} %) > 20 % — "
                  "la stratégie doit REPASSER LES 7 CRITÈRES (R-502)".replace(",", " "), True))
            rendu.append((serie_pertes < ALERTE_PERTES,
                  f"{_qui} : série de pertes en cours : {serie_pertes} (alerte à {ALERTE_PERTES})",
                  f"{_qui} : ALARME R-507 : {serie_pertes} PERTES CONSÉCUTIVES — revue complète des 7 critères", True))
            rendu.append((True,
                  f"{_qui} : marque (plus haut) {pic:,.0f} € · cumul {eq:,.0f} € · pire creux historique "
                  f"{creux:,.0f} € ({100*creux/100000:.1f} %)".replace(",", " "), "", False))
        return rendu

    def _lignes_13(constats):
        """Rend les lignes du rapport pour des constats : [(signe, texte, compteur du score)].

        ① RÔLE — Transformer les constats du maillon 13 en ✅, ⚠️ ou ❌, par le chemin
          que le témoin rejoue — c'est ce chemin même qui écrit le rapport du journal.
        ② CONTEXTE D'APPEL — Le maillon 13, deux fois : sur le témoin, puis sur le journal.
        ③ ENTRÉE — `constats` : la liste rendue par `_constats_13`.
        ④ CONDITIONS D'ENTRÉE — Aucune.
        ⑤ SORTIE — UNE valeur : une ligne par constat, dans l'ordre.
          [rend: 1]
        ⑥ TRAITEMENT — vrai → ✅ ; faux et critique → ❌ ; faux sinon → ⚠️ — la règle
          de `check`.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Relecteur du Chat, tour 7 (27-09-2026) : la boucle qui appliquait
          les constats n'était pas éprouvée ; forcer une alarme à vrai y laissait le
          témoin vert et écrivait « 27,8 % — sous le seuil de 20 % ».
        ⑨ CE QUI CLOCHE — `check` reste la règle des autres maillons : deux écritures
          de la même règle (R-708), la seconde sortie pour être éprouvée.
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend toujours la main.
          [sort: non]
        """
        rendu = []
        for _cond, _ok_txt, _ko_txt, _crit in constats:
            if _cond:
                rendu.append((OK, _ok_txt, "ok"))
            else:
                rendu.append((FAIL, _ko_txt, "fail") if _crit else (WARN, _ko_txt, "warn"))
        return rendu

    # LE TÉMOIN, REJOUÉ CHAQUE SOIR PAR LE MÊME CHEMIN QUE LE JOURNAL. Stratégie A (écrite
    # « S ») : la vente d'Unibail en deux comptabilités (vraies lignes), puis un gain et
    # deux pertes rangés dans le désordre → un jeton : série 2 (remise à zéro par le
    # gain), creux 26 000 € > 20 %, ALARME R-502 ; jetons illimités : série 1, sans
    # alarme. Stratégie B (écrite « T ») : cinq pertes de 100 € → ALARME R-507.
    _tem = [dict(strategie="S", comptabilite="un_jeton", date_sortie="2026-08-27", pnl_net_eur="-2796.25"),
            dict(strategie="S", comptabilite="jetons_illimites", date_sortie="2026-08-27", pnl_net_eur="-2796.25"),
            dict(strategie="S", comptabilite="un_jeton", date_sortie="2026-09-20", pnl_net_eur="-1000.00"),
            dict(strategie="S", comptabilite="un_jeton", date_sortie="2026-09-10", pnl_net_eur="5000.00"),
            dict(strategie="S", comptabilite="un_jeton", date_sortie="2026-09-15", pnl_net_eur="-25000.00")]
    _tem += [dict(strategie="T", comptabilite="un_jeton", date_sortie=f"2026-09-0{i}", pnl_net_eur="-100")
             for i in range(1, 6)]
    _r = [(sig, txt) for sig, txt, _k in _lignes_13(_constats_13(_tem, {"S": "A-ID", "T": "B-ID"}))]
    _attendu = [(OK, "A-ID · jetons illimites : creux en cours 2 796 € (2.8 %) — sous le seuil de 20 %"),
                (OK, "A-ID · jetons illimites : série de pertes en cours : 1 (alerte à 5)"),
                (FAIL, "A-ID · un jeton : SEUIL DE CREUX FRANCHI : 26 000 € (26.0 %) > 20 % — la stratégie doit REPASSER LES 7 CRITÈRES (R-502)"),
                (OK, "A-ID · un jeton : série de pertes en cours : 2 (alerte à 5)"),
                (OK, "B-ID · un jeton : creux en cours 500 € (0.5 %) — sous le seuil de 20 %"),
                (FAIL, "B-ID · un jeton : ALARME R-507 : 5 PERTES CONSÉCUTIVES — revue complète des 7 critères")]
    _vu = [x for x in _r if "marque (plus haut)" not in x[1]]
    check("13-Creux", _vu == _attendu, "Témoin du maillon 13 retrouvé (une série par stratégie et "
          "comptabilité, remise à zéro sur un gain, alarmes R-502 et R-507 déclenchées)",
          f"TÉMOIN DU MAILLON 13 FAUX — son jugement a changé : {_vu}", critique=True)
    # LES NOMS DU REGISTRE SONT BIEN PASSÉS : chaque stratégie vivante qui a des trades
    # doit apparaître sous son identifiant (sinon l'appel a perdu `_vers_id`).
    # L'attendu se calcule SANS `_vers_id`, depuis le registre, pour qu'un `_vers_id`
    # vidé ou faux se voie. Limite : un argument remplacé dans l'appel final, plus bas,
    # échapperait à ce contrôle.
    _ids_vivants = {(_l.get("id") or "").strip() for _l in (_serv3 or [])}
    _noms_journal = {(t.get("strategie") or "").strip() for t in trades}
    _ids_attendus, _verifiable = set(), True
    try:
        for _l in (_serv3 or []):
            if _noms_de_la_strategie(_l) & _noms_journal and not (_noms_de_la_strategie(_l) & _ambigus):
                _ids_attendus.add((_l.get("id") or "").strip())
    except NameError:
        _verifiable = False     # contrat illisible (fonction non chargée) : déjà dit plus haut
    _ids_vus = {k[0] for k in _series_du_journal(trades, _vers_id)}
    if not _verifiable:
        rapport.append((WARN, "13-Creux", "Rattachement des trades aux identifiants du registre "
                        "NON VÉRIFIABLE — contrat illisible"))
        score["warn"] += 1
    else:
        check("13-Creux", _ids_attendus <= _ids_vus,
              f"Trades rattachés aux identifiants du registre : {', '.join(sorted(_ids_vus & _ids_vivants)) or 'aucun'}",
              f"TRADES NON RATTACHÉS À LEUR IDENTIFIANT : attendus {sorted(_ids_attendus)}, vus {sorted(_ids_vus)}",
              critique=True)

    for _sig, _txt, _k in _lignes_13(_constats_13(trades, _vers_id)):
        rapport.append((_sig, "13-Creux", _txt))
        score[_k] += 1

# ═══ MAILLON 11 — POSITIONS OUVERTES (cohérence) ═══
pos, f_pos = _lire_csv(["positions_ouvertes"])
if f_pos is None:
    rapport.append((WARN, "11-Positions", "Fichier des positions ouvertes ABSENT"))
    score["warn"] += 1
else:
    ouvertes = [p for p in pos if (p.get("statut") or "").upper() == "OUVERTE"]
    attente  = [p for p in pos if (p.get("statut") or "").upper() == "EN_ATTENTE_ENTREE"]
    # A-258 : le vocabulaire des comptabilités a changé le 13/08 — « performance_vraie_vie »
    # est devenu « un_jeton ». Le filtre ne connaissait que l'ancien nom : il comptait donc
    # ZÉRO position par construction, et le ✅ « règle 1 position vraie-vie respectée » ne
    # prouvait rien — une violation du « un seul jeton à la fois » serait passée inaperçue.
    # On accepte les DEUX noms : l'ancien reste valide pour les historiques déjà écrits.
    COMPTABILITES_UN_JETON = ("un_jeton", "performance_vraie_vie")
    vraie_vie = [p for p in (ouvertes + attente)
                 if (p.get("comptabilite") or "").strip() in COMPTABILITES_UN_JETON]
    # A-258 (suite) : la règle n'est pas « une position en tout » mais « une position
    # à la fois PAR STRATÉGIE » (prompt de la boucle, R-605). Deux positions un_jeton
    # sur DEUX stratégies différentes sont donc LÉGITIMES. On compte par stratégie.
    from collections import Counter as _Counter
    _par_strategie = _Counter((p.get("strategie") or "?").strip() for p in vraie_vie)
    _violations = [f"{s} : {n}" for s, n in sorted(_par_strategie.items()) if n > 1]
    check("11-Positions", not _violations,
          f"Positions : {len(ouvertes)} ouverte(s), {len(attente)} en attente — "
          f"{len(vraie_vie)} en un jeton sur {len(_par_strategie)} stratégie(s), "
          "règle 1 jeton par stratégie respectée",
          f"RÈGLE VIOLÉE : plusieurs positions un jeton sur la même stratégie — {' | '.join(_violations)}",
          critique=True)
    # cohérence TP/SL — vérifiable UNIQUEMENT si le module de référence est
    # importable (R-708 interdit de réimplémenter la formule). Sans lui on dit
    # NON VÉRIFIABLE : on ne conclut jamais à la conformité, ni à l'absence.
    if MOD is None:
        rapport.append((WARN, "11-Positions",
            "TP/SL des positions NON VÉRIFIABLE — module C5-ETENDU-10 absent"))
        score["warn"] += 1
    else:
        faux = []
        for p in ouvertes:
            try:
                pe, tp, sl = float(p["prix_entree"]), float(p["tp"]), float(p["sl"])
                if abs(tp - pe*(1+MOD.C5E10_TP)) > 0.01 or abs(sl - pe*(1-MOD.C5E10_SL)) > 0.01:
                    faux.append(p.get("valeur","?"))
            except Exception:
                pass
        check("11-Positions", not faux,
              f"TP/SL des positions ouvertes conformes au module (+{100*MOD.C5E10_TP:.1f} % / -{100*MOD.C5E10_SL:.1f} %)",
              f"TP/SL INCOHÉRENTS sur : {', '.join(faux)}", critique=True)

# ═══ MAILLON 14 — A-41 : FRAÎCHEUR DES DONNÉES ET TAILLE DU PROJET ═══
from datetime import timedelta as _td
_cn = trouve("cours_nouveaux")
if _cn:
    try:
        with open(os.path.join(PROJ, _cn[0]), newline="", encoding="utf-8-sig") as fh:
            _rows = list(csv.DictReader(fh))
        _dates = sorted({r["date"] for r in _rows if r.get("date")})
        if _dates:
            _last = datetime.strptime(_dates[-1], "%Y-%m-%d").date()
            _age = (now.date() - _last).days
            # tolérance : week-end + 1 jour de publication
            check("14-Fraîcheur", _age <= 4,
                  f"Dernière séance lue : {_dates[-1]} ({_age} j) — données fraîches",
                  f"DONNÉES PÉRIMÉES : dernière séance {_dates[-1]}, soit {_age} jours — "
                  "la boucle ne lit plus (vérifier Cowork et le réveil Google)", critique=True)
    except Exception as e:
        rapport.append((WARN, "14-Fraîcheur", f"cours_nouveaux illisible : {e}")); score["warn"] += 1
else:
    rapport.append((WARN, "14-Fraîcheur", "cours_nouveaux absent — fraîcheur non vérifiable")); score["warn"] += 1

# ═══ MAILLON 14bis — UNE SÉANCE PORTE-T-ELLE TOUTES SES VALEURS ? ═══
# Né du trou du 29-10-2024 : l'historique portait 643 séances à 39 valeurs et UNE
# à 34. Cinq valeurs manquaient à cette seule date. Aucun des dix-sept maillons ne
# comptait les valeurs par séance : le trou est resté invisible des mois, et il
# fausse en silence tout calcul qui traverse cette date.
# LE NOMBRE DE RÉFÉRENCE N'EST PAS ÉCRIT EN DUR : il se déduit du fichier lui-même
# (le compte le plus fréquent). Un contrôle qui coderait « 39 » mourrait le jour où
# l'univers change — c'est exactement la faute que R-720 décrit.
_ohlcv_rows, _f_ohlcv = _lire_csv(["cac40_ohlcv"])
if _f_ohlcv is None:
    rapport.append((WARN, "14-Séances", "Historique des cours introuvable — séances non vérifiables"))
    score["warn"] += 1
else:
    from collections import Counter as _Cnt
    _par_seance = {}
    for _r in _ohlcv_rows:
        _d = (_r.get("date") or "").strip()
        _v = (_r.get("valeur") or "").strip()
        if _d and _v:
            _par_seance.setdefault(_d, set()).add(_norm_val(_v))
    if not _par_seance:
        rapport.append((WARN, "14-Séances", f"{_f_ohlcv} : aucune séance lisible"))
        score["warn"] += 1
    else:
        _comptes = {d: len(v) for d, v in _par_seance.items()}
        _attendu = _Cnt(_comptes.values()).most_common(1)[0][0]
        _incompletes = sorted(d for d, n in _comptes.items() if n != _attendu)
        _detail = " | ".join(f"{d} : {_comptes[d]} valeurs" for d in _incompletes[:3])
        check("14-Séances", not _incompletes,
              f"{len(_comptes)} séance(s) portent toutes {_attendu} valeurs ({_f_ohlcv})",
              f"SÉANCE(S) INCOMPLÈTE(S) : {len(_incompletes)} sur {len(_comptes)} s'écartent "
              f"du compte de référence ({_attendu} valeurs, déduit du fichier) — {_detail}"
              + (" …" if len(_incompletes) > 3 else ""))


# taille du projet : au-delà de ~85 % la capacité devient bloquante (incident 29/07)
try:
    # la taille se mesure sur les CHEMINS, sinon les fichiers des sous-dossiers
    # sont silencieusement comptés pour zéro
    _octets = sum(os.path.getsize(os.path.join(PROJ, p)) for p in _chemins
                  if os.path.isfile(os.path.join(PROJ, p)))
    # ON NE DIVISE PAS DES OCTETS PAR UN PLAFOND QUI N'EST PAS EN OCTETS.
    # Établi le 28-08-2026 : le projet pèse 2 784 646 OCTETS pendant que le
    # compteur du serveur annonce 1 643 088 pour un plafond de 2 000 000. Si
    # l'unité était l'octet, le projet serait à 139 % et REFUSERAIT toute
    # écriture — il n'a rien refusé. Deux fichiers suffisent à le montrer :
    # l'historique des cours et le BACKLOG font à eux seuls 2 110 294 octets,
    # déjà au-dessus du compteur, et il reste plus de cent fichiers.
    # Le rapport mesuré est de 1,69 octet par unité, cohérent avec le 1,70
    # obtenu par un calibrage indépendant le 26/08.
    #
    # CE QUE CETTE ERREUR A COÛTÉ : le maillon criait « PLACE CRITIQUE 109 % »
    # chaque soir. L'explication donnée depuis des jours — « artefact
    # d'exécution locale, dossier reconstitué » — était FAUSSE : même sur le
    # vrai projet monté, le maillon aurait crié, puisque le vrai projet pèse
    # 2,78 Mo d'octets. Une alerte rouge apprivoisée pendant des semaines, et
    # une alerte qu'on apprend à ignorer cesse de protéger.
    #
    # LE CHIFFRE JUSTE EXISTE, ET IL EST RELEVÉ PAR LA TÂCHE : le prompt
    # compare knowledge_size à max_knowledge_size, deux valeurs de la MÊME
    # unité. Ce rapport est correct quelle que soit l'unité. Le script ne
    # recalcule donc RIEN : il rapporte le poids en octets pour le ménage, et
    # renvoie explicitement au chiffre autoritaire pour la saturation.
    # UNE ALERTE PERMANENTE N'EST PAS UNE ALERTE. Le premier seuil retenu,
    # 2 500 000 octets, était déjà franchi le jour même — il aurait crié tous les
    # soirs sans jamais rien apprendre, et une alerte qu'on apprend à ignorer
    # cesse de protéger. C'est précisément le défaut qu'on venait de corriger au
    # même endroit. Ce repère devient donc une INFORMATION, jamais une alerte :
    # la saturation se lit sur la place réelle relevée par la tâche, et elle a
    # son propre seuil à 85 %.
    _seuil_octets = 10**12        # jamais atteint : ce maillon informe, il n'alerte pas
    check("14-Taille", _octets < _seuil_octets,
          f"Poids du projet : {_octets:,} octets sur {len(fichiers)} fichiers"
          " — INFORMATION de volume pour le ménage, jamais une alerte. La"
          " saturation se lit sur la place RÉELLE relevée par la tâche : le"
          " plafond n'est pas exprimé en octets.".replace(",", " "),
          f"VOLUME ÉLEVÉ : {_octets:,} octets sur {len(fichiers)} fichiers — le ménage"
          " devient utile. Ce n'est PAS une alerte de saturation : celle-là se lit"
          " sur la place réelle relevée par la tâche.".replace(",", " "))
except Exception:
    pass

# ═══ MAILLON 18 — LES TÂCHES ONT-ELLES PRODUIT CE QU'ELLES DEVAIENT ? ═══
# TROUVÉ LE 28-08-2026 : les deux boucles du matin, 07h05 et 08h35, se sont
# arrêtées en cours de route — ni réussies ni échouées, ABANDONNÉES. Personne ne
# l'a su. AUCUNE ALERTE N'EXISTAIT POUR ÇA, et c'est pourquoi la boucle du soir
# a dû rattraper une séance vieille de deux jours. Le système pouvait donc cesser
# de tourner sans que rien ne le dise : pas une erreur, un SILENCE.
#
# ON NE LIT PAS LA DATE DU FICHIER — ELLE MENT, ET C'EST PROUVÉ.
# Première version de ce maillon, corrigée le soir même : elle lisait le mtime,
# c'est-à-dire la date du fichier SUR LE DISQUE. Or la tâche commence par
# recopier tout le projet en local : chaque fichier arrive avec la date du
# téléchargement. Mesuré par contraste : un rapport du 20-08 portait un mtime du
# 23, puis du 28 après recopie. EN PRODUCTION, CE MAILLON AURAIT ÉTÉ AU VERT
# QUOI QU'IL ARRIVE — un faux vert structurel, la famille même du défaut du
# maillon 10 qu'on venait de fermer, rouverte au maillon suivant.
#
# LA DATE VRAIE EST DÉCLARÉE, ET ELLE EST LÀ DEUX FOIS : dans le NOM du fichier
# (rapport_boucle_2026-08-27.md, cockpit_Ven_28-08-2026_22h00.html) et dans son
# EN-TÊTE (« # AUDIT DU JOUR — … — 2026-08-27_22h25 »). On lit celle-là.
#
# ET ON NE LIT PAS L'ÉTAT DES TÂCHES — le script n'y a pas accès. Il fait
# l'inverse, et c'est plus robuste : une tâche qui tourne LAISSE UNE TRACE
# DATÉE. Une trace absente ou vieille dénonce la tâche quelle qu'en soit la
# cause : arrêt, échec, prompt cassé, tâche désactivée par mégarde.
try:
    from datetime import datetime as _dt, timedelta as _td
    _aujourdhui = datetime.now(ZoneInfo("Europe/Paris")).date()

    def _date_declaree(chemin):
        """Rend la date qu'un fichier DÉCLARE, dans son nom ou dans son contenu.

        ① RÔLE — Dire de quand date réellement la trace laissée par une tâche planifiée,
          pour que le maillon 18 puisse dénoncer une tâche qui a cessé de tourner. La date
          que le système de fichiers donne à un fichier ment, et c'est prouvé : la tâche du
          soir commençait par recopier tout le projet, et chaque fichier arrivait avec la
          date du téléchargement. Mesuré par contraste le 28-08-2026, un rapport du 20-08
          portait une date de fichier du 23, puis du 28 après recopie — le contrôle des
          traces aurait été au vert quoi qu'il arrive.
        ② CONTEXTE D'APPEL — Un seul endroit, le maillon 18, une fois par fichier
          candidat, pour chacune des tâches déclarées. Mesuré le 20-09-2026 sur une
          copie du dépôt : quatre lignes de rapport en sont issues, une par tâche ; trois
          depuis le 30-09-2026, le cockpit n'étant plus déclaré.
        ③ ENTRÉE — `chemin` : le chemin d'un fichier, relatif au dossier examiné, par
          exemple rapports/audit_du_jour.md ou donnees/historique_mesures.csv. Un seul
          appelant, le maillon 18, qui lui passe tour à tour chaque fichier dont le nom
          contient l'un des motifs d'une tâche.
        ④ CONDITIONS D'ENTRÉE — Aucune. Un fichier absent, illisible, trop gros ou sans
          aucune date rend rien du tout, sans faire tomber.
        ⑤ SORTIE — UNE valeur : une date de calendrier, ou rien quand aucune n'a pu être
          lue. Mesuré le 20-09-2026 sur une copie du dépôt : rapports/audit_du_jour.md
          rend le 2026-09-17, donnees/claude_cours_nouveaux.csv rend le 2026-09-18,
          cockpit/claude_cockpit_Lun_07-09-2026_22h02.html rend le 2026-09-07, et
          gouvernance/PILOTE.md ne rend rien.
          [rend: 1]
        ⑥ TRAITEMENT — ① si le fichier est un tableur, ignorer son nom ; sinon prendre son
          nom · ② y chercher une date écrite année-mois-jour, puis, à défaut, une date
          écrite jour-mois-année, et la rendre si elle est valide · ③ à défaut, rendre rien
          si le fichier pèse plus de deux millions d'octets · ④ lire le fichier ENTIER
          s'il s'agit d'un tableur, seulement ses QUATRE PREMIÈRES lignes sinon · ⑤ y
          relever toutes les dates des deux formes · ⑥ écarter celles qui sont postérieures
          à aujourd'hui · ⑦ rendre rien s'il n'en reste aucune · ⑧ rendre la PLUS RÉCENTE
          pour un tableur, la PREMIÈRE rencontrée pour un document rédigé.
        ⑦ UNITÉ — Une DATE de calendrier. Le seuil au-delà duquel le fichier n'est pas lu
          est en OCTETS, et vaut deux millions.
        ⑧ POURQUOI — Deux sortes de fichiers, deux endroits où la date vit, et le
          programme les distingue par l'extension plutôt que par une devinette sur le
          contenu. Un TABLEAU s'empile : l'historique des mesures ajoute une ligne par jour
          et n'est jamais réécrit, donc lire ses premières lignes rendait le 15-08 pour
          toujours et l'écart annoncé grandissait d'un jour chaque jour — une alerte
          permanente sur une tâche qui fonctionne. Un DOCUMENT RÉDIGÉ porte sa date en
          tête et cite des dizaines d'autres dates dans son corps, puisqu'un rapport
          d'audit parle de tous les fichiers du projet. Et parmi les dates de l'en-tête,
          c'est la PREMIÈRE qui compte et non la plus récente : la version du 29-08-2026
          prenait la plus récente des quatre premières lignes, et un rapport daté du 11-08
          était lu comme du 28-08. La faute était invisible sur les fichiers réels, où
          l'en-tête est seul dans ces quatre lignes ; elle n'attendait qu'un document un
          peu plus dense. Enfin, une date postérieure à aujourd'hui est une échéance ou une
          coquille, jamais une trace : retenue, elle ferait croire qu'une tâche arrêtée
          vient de tourner.
        ⑨ CE QUI CLOCHE — quatre points, tous mesurés le 20-09-2026 :
          ① UN FICHIER TROP GROS EST TRAITÉ COMME UN FICHIER SANS DATE. Au-delà de deux
          millions d'octets, la fonction rend rien, et le maillon 18 affiche alors
          a laissé une trace SANS DATE LISIBLE — on ne peut pas dire si la tâche a tourné.
          Le message accuse le fichier d'une faute qu'il n'a pas commise. Aucune des
          quatre tâches alors déclarées n'était concernée : le plus gros fichier qu'elles
          laissent est donnees/claude_cours_nouveaux.csv, 86 836 octets. Mais
          donnees/cours_maitre.csv, qui pèse 1 635 261 octets et grandit d'environ
          39 lignes par séance, s'approche du seuil ; le jour où une tâche sera surveillée
          par un fichier de cette taille, elle passera pour muette.
          ② LE NOM L'EMPORTE SUR LE CONTENU, SANS COMPARAISON NI MESSAGE. Pour un document
          rédigé, la date du nom est rendue dès qu'elle existe et le contenu n'est jamais
          lu. Mesuré : cockpit/claude_cockpit_Lun_07-09-2026_22h02.html rend le 2026-09-07
          quel que soit ce qu'il raconte à l'intérieur. Un fichier recopié sous un nom
          ancien avec un contenu neuf serait annoncé vieux, et l'inverse aussi.
          ③ LE SEUIL ET LE NOMBRE DE LIGNES LUES SONT DES CHIFFRES ÉCRITS EN DUR : deux
          millions d'octets, quatre lignes. Le projet a déjà payé cette forme au même
          endroit : vingt lignes était un COMPTE, et un préambule de vingt-six lignes
          faisait annoncer AUCUNE version vivante sur un fichier intact. Un garde-fou porte
          sur une propriété, jamais sur un compte (R-721).
          ④ Elle ne dit jamais D'OÙ vient la date qu'elle rend, du nom ou du contenu.
          L'appelant écrit pourtant date DÉCLARÉE dans le rapport, ce qui laisse croire à
          une seule origine. Deux fichiers d'une même tâche peuvent donc donner deux dates
          lues de deux façons différentes, et c'est la plus récente qui l'emporte sans que
          rien ne le signale.
        ⑩ EFFET — OUVRE et LIT les fichiers candidats du maillon 18. N'écrit aucun
          fichier, n'affiche rien, ne touche pas au réseau.
        ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas : l'échec d'ouverture est
          rattrapé, une date impossible comme un 31 février est écartée, et la lecture
          remplace les caractères illisibles. Aucun de ses appels ne se termine.
          [sort: non]
        ⑫ DÉFINITIONS
          une trace : le fichier qu'une tâche planifiée laisse derrière elle
            quand elle a tourné — rapport de boucle, rapport d'audit, cockpit,
            historique des mesures.
          la date déclarée : la date qu'un fichier porte dans son nom ou dans son contenu, par opposition à celle que le système de fichiers lui donne.
          un maillon : un groupe de contrôles du radar, désigné par un numéro
            et un nom, par exemple 18-Tâches pour le contrôle des traces
            laissées par les tâches planifiées.
          le radar : le programme programmes/audit_ecosysteme.py, lancé chaque
            soir, qui contrôle l'ensemble du système et range chacun de ses
            constats sous un numéro de maillon, par exemple 18-Tâches pour le
            contrôle des traces laissées par les tâches planifiées.
          la tâche planifiée : un fichier de .github/workflows/ qui fait
            tourner un programme à heure fixe sur une machine GitHub, sans
            clic ni autorisation.
          le projet : le dossier reçu sur la ligne de commande, celui que le radar examine
          une séance : une journée de bourse pour une valeur, avec son
            ouverture, son plus haut, son plus bas, sa clôture et son volume.
          le pilote : gouvernance/PILOTE.md, le document fabrique chaque soir
            qui dit ou en est le projet, ce qu'il contient et ce qui cloche
        
          la trace : la liste des sources avec leur etat — LU, ABSENT ou ILLISIBLE — et un detail chiffre, affichee en pied de page.
          un garde-fou : une limite qui, franchie, fait cesser a la strategie de prendre position tout en continuant a la mesurer.
"""
        # LA DATE DU NOM NE PRIME PAS SUR UN TABLEAU. Aujourd'hui aucun tableau
        # de trace ne porte de date dans son nom, donc c'est sans effet — mais si
        # « cours_nouveaux.csv » devenait « cours_nouveaux_2026-08-15.csv », sa
        # dernière ligne ne serait plus jamais lue et le défaut du 15-08
        # reviendrait par une autre porte. On ne lit le nom que pour les
        # documents rédigés.
        if chemin.lower().endswith((".csv", ".tsv")):
            _base = ""
        else:
            _base = os.path.basename(chemin)
        _m = re.search(r"(20\d\d)-(\d{2})-(\d{2})", _base)
        if not _m:
            _m2 = re.search(r"(\d{2})-(\d{2})-(20\d\d)", _base)
            if _m2:
                _m = None
                try:
                    return _dt(int(_m2.group(3)), int(_m2.group(2)),
                               int(_m2.group(1))).date()
                except ValueError:
                    pass
        if _m:
            try:
                return _dt(int(_m.group(1)), int(_m.group(2)),
                           int(_m.group(3))).date()
            except ValueError:
                pass
        # DEUX SORTES DE FICHIERS, DEUX ENDROITS OÙ LA DATE VIT.
        # UN TABLEAU S'EMPILE : sa date est en DERNIÈRE ligne. L'historique des
        #   mesures ajoute une ligne par jour et n'est jamais écrasé — lire ses
        #   premières lignes rendait le 15-08 pour toujours, et l'écart aurait
        #   grandi d'un jour par jour : une alerte permanente sur une tâche qui
        #   fonctionne.
        # UN DOCUMENT RÉDIGÉ porte sa date en TÊTE, et cite des dizaines d'autres
        #   dates dans son corps — un rapport d'audit parle de tous les fichiers
        #   du projet. Y chercher la date la plus récente revient à lire n'importe
        #   laquelle : constaté à l'instant, un rapport vieilli au 15-08 était
        #   annoncé « 2 jours » parce qu'il mentionnait une date récente.
        # La première correction a donc cassé ce que la seconde réparait. On
        # distingue par l'extension, jamais par une devinette sur le contenu.
        try:
            _p = os.path.join(PROJ, chemin)
            if os.path.getsize(_p) > 2_000_000:
                return None                      # trop gros pour être lu ici
            _tableau = chemin.lower().endswith((".csv", ".tsv"))
            with open(_p, encoding="utf-8", errors="replace") as _fh:
                _txt = _fh.read() if _tableau else "".join(
                    _fh.readline() for _ in range(4))
        except OSError:
            return None
        _vues = []
        for _a, _b, _c in re.findall(r"(20\d\d)-(\d{2})-(\d{2})", _txt):
            try:
                _vues.append(_dt(int(_a), int(_b), int(_c)).date())
            except ValueError:
                pass
        for _a, _b, _c in re.findall(r"(\d{2})-(\d{2})-(20\d\d)", _txt):
            try:
                _vues.append(_dt(int(_c), int(_b), int(_a)).date())
            except ValueError:
                pass
        # une date POSTÉRIEURE à aujourd'hui est une date d'échéance ou une
        # coquille, jamais une trace : on ne la retient pas.
        _vues = [d for d in _vues if d <= _aujourdhui]
        if not _vues:
            return None
        # UN TABLEAU S'EMPILE : sa date est la PLUS RÉCENTE.
        # UN DOCUMENT DÉCLARE SA DATE EN PREMIER : c'est la PREMIÈRE rencontrée.
        # Trouvé le 29/08 par le jeu d'épreuves, et c'est un douzième défaut de
        # la même famille : la v2.5 lisait bien les quatre premières lignes d'un
        # document, mais y prenait le MAXIMUM. Si le corps commence tôt et cite
        # une date plus récente que l'en-tête, elle l'emporte — un rapport daté
        # du 11-08 était lu comme du 28-08.
        # Le maximum et le premier coïncident tant que l'en-tête est seul dans
        # les quatre lignes : la faute était invisible sur les fichiers réels.
        return max(_vues) if _tableau else _vues[0]

    # CHAQUE TÂCHE A SON PROPRE CALENDRIER, ET LE COMPTAGE DOIT LE SUIVRE.
    # Défaut corrigé le 29/08, en miroir exact du précédent : le comptage en
    # jours ouvrés avait été appliqué aux QUATRE tâches alors qu'UNE SEULE a un
    # cron « lun-ven ». Les trois autres tournent 7 jours sur 7.
    # CE QUE CELA COÛTAIT : un audit mort le vendredi soir n'aurait été dénoncé
    # que le MARDI — quatre jours pendant lesquels le radar est aveugle sur la
    # tâche qui EST le radar. En calendaire, il l'est dès le dimanche.
    # Un correctif juste pour un cas, appliqué à des cas qui ne le demandaient
    # pas : c'est la quatrième fois en deux jours que cette forme revient.
    # Le mode se déclare donc PAR TÂCHE, jamais en global.
    # UNE DÉCLARATION INCOMPLÈTE NE DOIT PAS FAIRE TOMBER LES SUIVANTES.
    # Trouvé le 29/08 : un mode oublié levait une erreur de dépaquetage, attrapée
    # tout en bas — et les tâches déclarées APRÈS celle qui manquait n'étaient
    # plus contrôlées du tout, sans un mot. Le cockpit et la mesure de
    # performance disparaissaient du rapport en silence. Chaque déclaration est
    # donc examinée séparément : celle qui est mal formée est dénoncée, les
    # autres continuent d'être contrôlées.
    _declarations = [
        ("la boucle du jour", ["rapport_boucle", "cours_nouveaux"], 1, "ouvré"),
        ("l'audit du soir", ["audit_du_jour"], 1, "calendaire"),
        ("la mesure de performance", ["historique_mesures"], 2, "calendaire"),
    ]
    # LE COCKPIT N'EST PLUS DÉCLARÉ ICI (30-09-2026, travail de nuit demandé par
    # Jean-Luc le 29-09). Deux faits, mesurés :
    # ① LE COCKPIT N'ÉCRIT RIEN AU DÉPÔT PRIVÉ. PUBLIER_LE_SITE.py fabrique la page
    #   dans _site_travail/, qui n'est pas enregistré, et l'envoie au dépôt PUBLIC
    #   (commit « cockpit 2026-09-29 20h22 »). Le motif « cockpit » ne trouvait donc
    #   que des fichiers qu'aucune tâche n'écrit : le soir du 29-09, la « dernière
    #   trace » était etudes/illustrations/A443_cockpit_courbe_3D_4D_Mar_22-09-2026_12h35.jpeg,
    #   une image du 22-09 — d'où l'alerte « le cockpit n'a rien écrit depuis 7 jours »,
    #   fausse chaque soir.
    # ② LE RADAR NE PEUT PAS VOIR LE COCKPIT S'ARRÊTER. Dans .github/workflows/collecte_abc.yml,
    #   le pas du cockpit passe AVANT le radar, dans le même job, et sa commande est
    #   l'appel seul du programme, sans `continue-on-error`, sans `shell:` ni `if:` ;
    #   aucun pas jusqu'au radar ne porte de `if:` : si PUBLIER_LE_SITE.py sort avec un
    #   code non nul, le passage s'arrête et le radar ne tourne pas ce soir-là. (Limite,
    #   relevée par le relecteur : PUBLIER_LE_SITE.py ne vérifie pas le code de retour
    #   du générateur ; un générateur qui écrit une page puis échoue laisse publier
    #   avec le code 0.) Ce qui le dit alors : le pas rouge dans GitHub,
    #   et la date du rapport du radar, relevée au début de chaque conversation (rituel,
    #   étape 3bis). La trace de « l'audit du soir » ci-dessus devrait aussi le dire au
    #   passage suivant, mais elle est illisible en production (le pas du radar vide
    #   rapports/audit_du_jour.md avant que le radar le lise : mesuré, « SANS DATE
    #   LISIBLE » chaque soir) — défaut consigné au BACKLOG le 30-09-2026, non réparé.
    #   tests/EPREUVES_DU_COCKPIT_AU_RADAR_Mer_30-09-2026.py vérifie que cet ordre tient.
    # LA PROPRIÉTÉ, pour toute tâche à déclarer ici : elle doit LAISSER UN FICHIER DANS
    # LE DÉPÔT QUE CE RADAR EXAMINE. Une tâche qui n'en laisse aucun ne se surveille pas
    # par ses traces ; la déclarer ne produit qu'une alerte sur des fichiers étrangers.
    _propres = []
    for _decl in _declarations:
        if len(_decl) == 4:
            _propres.append(_decl)
        else:
            check("18-Tâches", False, "",
                  f"déclaration de tâche INCOMPLÈTE : {_decl!r} — il manque son "
                  f"mode de comptage. Cette tâche n'est pas contrôlée ; les "
                  f"autres le restent.")
    for _lib, _motifs, _jours, _mode in _propres:
        _f = []
        for _m0 in _motifs:
            _f += [p for p in _chemins if _m0 in _norm(os.path.basename(p))]
        if not _f:
            check("18-Tâches", False, "",
                  f"{_lib} n'a laissé AUCUNE trace — la tâche n'a peut-être "
                  f"jamais tourné")
            continue
        _dates = [d for d in (_date_declaree(p) for p in _f) if d]
        if not _dates:
            check("18-Tâches", False, "",
                  f"{_lib} a laissé une trace SANS DATE LISIBLE — on ne peut pas "
                  f"dire si la tâche a tourné. Ce n'est pas un succès.")
            continue
        # LE MODE EST CELUI DE LA TÂCHE, déclaré juste au-dessus.
        # Les trois boucles ont un cron « lun-ven » : elles NE TOURNENT PAS le
        # week-end. Avec un écart calendaire, le radar aurait dénoncé chaque
        # dimanche et chaque lundi matin une tâche qui fonctionne parfaitement
        # — plus les jours fériés. Vérifié : dernière boucle le vendredi 28,
        # l'écart calendaire vaut 1, 2 puis 3 jours du samedi au lundi, quand
        # l'écart ouvré vaut 0, 0 puis 1.
        # C'est la TROISIÈME fois en deux jours que la même forme de défaut
        # revient : une alerte permanente qui n'apprend rien, fermée au maillon
        # 14, rouverte sur l'historique des mesures, rouverte ici par le
        # calendrier. Deux cas qui se ressemblent, un correctif qui vaut pour
        # l'un et pas pour l'autre.
        # UN MODE INCONNU NE RETOMBE PAS EN SILENCE SUR UNE VALEUR PAR DÉFAUT.
        # Trouvé le 29/08 : avec « ouvre » au lieu de « ouvré », le else prenait
        # la main et comptait en CALENDAIRE pendant que le libellé annonçait
        # « ouvre ». Le rapport disait une chose et calculait l'autre — la même
        # étiquette menteuse que le maillon 14 portait avec ses octets. Une
        # lettre suffisait. On refuse donc tout mode hors des deux connus.
        if _mode not in ("ouvré", "calendaire"):
            check("18-Tâches", False, "",
                  f"{_lib} déclare un mode de comptage INCONNU : {_mode!r}. "
                  f"Aucun âge n'est calculé — il vaut mieux ne rien dire que "
                  f"dire un chiffre sous une étiquette qui ment.")
            continue
        if _mode == "ouvré":
            _age = 0
            _d = max(_dates)
            while _d < _aujourdhui:
                _d += _td(days=1)
                if _d.weekday() < 5:
                    _age += 1
        else:
            _age = (_aujourdhui - max(_dates)).days
        check("18-Tâches", _age <= _jours,
              f"{_lib} a laissé sa trace il y a {_age} jour(s) {_mode}(s) — date "
              f"DÉCLARÉE "
              f"{max(_dates)}",
              f"{_lib} n'a rien écrit depuis {_age} jour(s) {_mode}(s), au-delà des "
              f"{_jours} "
              f"attendus — dernière trace datée {max(_dates)}. La tâche s'est "
              f"peut-être ARRÊTÉE sans le dire (cas des boucles du 28/08).")
except Exception as _e:
    check("18-Tâches", False, "", f"contrôle des traces impossible : {_e}")


# ═══ MAILLON 15 — A-65 : LA CHAÎNE DES 3 PIÈCES PAR STRATÉGIE ═══
# Toute stratégie en production a une LOI (ligne du REGISTRE), une HISTOIRE
# (fichier STRATEGIE_*.md) et un MOTEUR (module .py). Une pièce manquante = trou.
_cr2, _ = chemin_registre()       # chemin ABSOLU, dépôt d'abord (R-736)
_txt_reg = ""
if _cr2:
    try:
        _txt_reg = open(_cr2, encoding="utf-8", errors="ignore").read()
    except Exception:
        pass
for _strat, _motif_hist, _motif_moteur in [("C5-ETENDU-10", "STRATEGIE_C5_ETENDU_10", "MODULE_C5_ETENDU")]:
    _loi = _strat in _txt_reg
    _hist = existe(_motif_hist)
    _moteur = existe(_motif_moteur)
    _manque = [n for n, ok in (("LOI (registre)", _loi), ("HISTOIRE (dossier)", _hist),
                               ("MOTEUR (module)", _moteur)) if not ok]
    check("15-Chaîne", not _manque,
          f"{_strat} : chaîne complète — LOI + HISTOIRE + MOTEUR",
          f"{_strat} : pièce(s) manquante(s) — {', '.join(_manque)}", critique=True)

# ═══ MAILLON 16 — A-46 : CONTRÔLE DU BACKLOG (délégué à verif_backlog.py) ═══
# R-708 : on n'écrit PAS un second contrôle du backlog ici, on APPELLE le script existant.
_vb = [f for f in fichiers if _norm("verif_backlog") in _norm(f) and f.endswith(".py")]
_cbl = chemin_backlog()          # au dépôt d'abord (R-736)
_bl = [_cbl] if _cbl else []
if not _vb:
    rapport.append((WARN, "16-Backlog", "verif_backlog.py absent — contrôle du backlog non effectué"))
    score["warn"] += 1
elif not _bl:
    rapport.append((FAIL, "16-Backlog", "BACKLOG_DECISIONS absent")); score["fail"] += 1
else:
    import subprocess, shutil as _sh, tempfile
    try:
        # copie de travail : le script tamponne le fichier, on ne touche pas à l'original
        _tmp = os.path.join(tempfile.gettempdir(), "_bl_audit.md")
        _sh.copy(_cbl, _tmp)
        _r = subprocess.run([sys.executable, chemin_de(_vb[0]), _tmp],
                            capture_output=True, text=True, timeout=60)
        _sortie = (_r.stdout or "").strip().splitlines()
        _resume = _sortie[-1] if _sortie else "(pas de sortie)"
        _alertes = [l.strip() for l in _sortie if l.strip().startswith(("❌", "⚠"))]
        # TOUS LES ❌, JAMAIS LES TROIS PREMIERS (30-09-2026). Le message ne montrait que les
        # trois premières alertes : trois ❌ anciens (A-425, A-435, A-471) occupaient ces
        # places pour de bon, et un ❌ nouveau n'arrivait jamais au rapport du soir —
        # prouvé par le relecteur du Chat avec une action témoin numérotée A-503, avant que ce
        # numéro serve à une vraie action (0 mention au radar).
        _echecs = [a for a in _alertes if a.startswith("❌")]
        check("16-Backlog", _r.returncode == 0,
              f"Backlog contrôlé par verif_backlog.py — {_resume}",
              f"BACKLOG EN ÉCHEC : {' | '.join(_echecs) or _resume}", critique=True)
        for _a in _alertes:
            if _a.startswith("⚠"):
                rapport.append((WARN, "16-Backlog", _a)); score["warn"] += 1
    except Exception as e:
        rapport.append((WARN, "16-Backlog", f"verif_backlog.py non exécutable : {e}")); score["warn"] += 1

# ═══ MAILLON 19 — LES DONNÉES AU DÉPÔT AVANCENT-ELLES ENCORE ? ═══
# POSÉ LE 08-09-2026. Motif : la migration met les fichiers au dépôt GitHub, et
# RIEN ne mesure qu'ils continuent d'y avancer. Le 08-09, la copie du Drive avait
# 25 jours de retard sur les cours et personne ne l'a su ; le même soir,
# historique_mesures.csv s'arrêtait au 06-09 des DEUX côtés, sans alerte.
#
# CE MAILLON REMPLACE LE COMPARATEUR QU'ON N'A PAS. La double écriture aurait dit
# « les deux copies concordent » ; elle a été abandonnée parce qu'une transition
# sans critère de fin devient l'état permanent. Ce qui la remplace n'est pas la
# concordance mais la FRAÎCHEUR : un fichier qui cesse d'avancer se dénonce seul,
# et ce signal attrape aussi bien le cas où plus personne n'écrit que celui où
# deux endroits se contredisent.
#
# ON NE LIT PAS LA DATE DU FICHIER — elle ment, c'est le défaut corrigé au
# maillon 18. On lit la DERNIÈRE DATE ÉCRITE DANS LE CONTENU : première colonne
# d'un CSV daté, ou la date la plus récente qu'il porte.
#
# LE SEUIL EST CELUI DE CHAQUE FICHIER, pas un chiffre unique — un fichier écrit
# chaque jour de bourse et un historique figé ne vieillissent pas pareil.
_DONNEES_SUIVIES = [
    ("cac40_ohlcv",            None, "historique figé — ne bouge que sur fusion"),
    ("claude_cours_nouveaux",  2,    "séances nouvelles, écrit par les boucles"),
    ("historique_mesures",     2,    "une ligne par jour, écrit par la mesure"),
    ("claude_journal_lectures",2,    "une ligne par passage de boucle"),
    ("claude_journal_trades",  None, "s'empile aux clôtures — peut rester stable"),
    ("claude_positions_ouvertes", None, "état courant — peut être vide"),
]

def _derniere_date_du_contenu(chemin):
    """Rend, sous forme de texte, la date la plus récente écrite DANS un fichier.

    ① RÔLE — Dire si un fichier de données du dépôt avance encore. C'est la seule
      mesure du maillon 19, posé le 08-09-2026 : la migration a mis les fichiers au
      dépôt GitHub et rien ne mesurait qu'ils continuaient d'y être écrits. Ce jour-là,
      la copie du Drive avait 25 jours de retard sur les cours et personne ne l'a su ;
      le même soir, l'historique des mesures s'arrêtait au 06-09 des DEUX côtés, sans
      alerte.
    ② CONTEXTE D'APPEL — Un seul endroit, le maillon 19, une fois pour chacun des six
      fichiers de données suivis : l'historique figé des cours, les cours du jour,
      l'historique des mesures, le journal des lectures, le journal des trades et les
      positions ouvertes. Jamais appelée ailleurs.
    ③ ENTRÉE — `chemin` : le chemin complet du fichier à lire, par exemple
      /tmp/depot/donnees/claude_cours_nouveaux.csv. Un seul appelant, le maillon 19,
      qui le compose à partir du dossier de données qu'il a trouvé et du nom du
      fichier qu'il a retenu.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un fichier absent, illisible ou sans date rend
      rien du tout, sans faire tomber.
    ⑤ SORTIE — UNE valeur : la date la plus récente trouvée, sous forme de TEXTE
      écrit année-mois-jour, ou rien quand le fichier ne porte aucune date de cette
      forme. Mesuré le 20-09-2026 :
      donnees/claude_cours_nouveaux.csv rend le texte 2026-09-18 et
      gouvernance/golden_tests_Sam_01-08-2026_20h19.json rend le texte 2026-07-10.
      [rend: 1]
    ⑥ TRAITEMENT — ① ouvrir le fichier en UTF-8 en écartant la marque d'ordre des
      octets et en remplaçant les caractères illisibles · ② rendre rien si la lecture
      échoue · ③ relever tous les textes de la forme année-mois-jour · ④ rendre le plus
      grand dans l'ordre alphabétique, ou rien si aucun n'a été trouvé.
    ⑦ UNITÉ — Une DATE de calendrier, rendue comme un TEXTE et non comme une date.
    ⑧ POURQUOI — Elle lit la date écrite DANS le fichier et jamais celle que le
      système de fichiers lui donne, pour la même raison qui vaut au maillon 18 : la
      seconde vaut la date du téléchargement et met le contrôle au vert quoi qu'il
      arrive. Et la comparaison de textes écrits année-mois-jour donne le même ordre
      que la comparaison de dates, ce qui évite d'avoir à les convertir toutes.
    ⑨ CE QUI CLOCHE — quatre points, tous mesurés le 20-09-2026 :
      ① ELLE NE FILTRE PAS LES DATES FUTURES, ALORS QUE SA VOISINE DU MAILLON 18 LE
      FAIT. Mesuré sur un fichier de deux lignes portant 2099-12-31 : elle rend
      2099-12-31. Une échéance ou une coquille dans un fichier de données ferait donc
      annoncer une fraîcheur parfaite sur un fichier qui n'avance plus. C'est
      exactement le défaut que le maillon 18 a fermé le 29-08-2026, et il est resté
      ouvert ici.
      ② ELLE LIT LE FICHIER ENTIER EN MÉMOIRE, SANS AUCUN SEUIL DE TAILLE. Sa voisine
      du maillon 18 refuse au-delà de deux millions d'octets ; celle-ci n'a pas de
      limite, et l'un des six fichiers qu'elle lit est l'historique figé des cours.
      Mesuré : donnees/cac40_ohlcv.csv pèse 1 362 570 octets, et il est lu en entier à
      chaque passage.
      ③ Elle rend un texte là où l'appelant attend une date, et c'est l'appelant qui
      doit le convertir. Mesuré : cette conversion est enveloppée dans une clause qui
      avale silencieusement l'échec et passe au fichier suivant. Un texte de la bonne
      forme mais impossible comme 2026-02-31 ferait donc DISPARAÎTRE le fichier du
      rapport, sans une ligne.
      ④ Elle relève ses dates dans TOUT le fichier, en-tête et commentaires compris,
      et non dans la colonne de date. Une date citée dans une ligne de commentaire
      l'emporterait sur la dernière ligne de données.
    ⑩ EFFET — OUVRE et LIT un fichier en entier. N'écrit aucun fichier, n'affiche
      rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas : l'échec d'ouverture est
      rattrapé et rendu sous la forme d'un rien. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      un maillon : un groupe de contrôles du radar, désigné par un numéro et
        un nom, par exemple 18-Tâches pour le contrôle des traces laissées par
        les tâches planifiées.
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque
        soir, qui contrôle l'ensemble du système et range chacun de ses
        constats sous un numéro de maillon, par exemple 18-Tâches pour le
        contrôle des traces laissées par les tâches planifiées.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
      l'historique figé : donnees/cac40_ohlcv.csv, le fichier de cours de
        référence qui n'est jamais réécrit
      la marque d'ordre des octets : trois octets invisibles que certains
        tableurs posent en tête d'un fichier et qui, s'ils ne sont pas
        écartés, se collent au nom de la première colonne
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand
        elle a tourné — rapport de boucle, rapport d'audit, cockpit,
        historique des mesures.
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    import re as _re
    try:
        with open(chemin, encoding="utf-8-sig", errors="replace") as _f:
            _txt = _f.read()
    except Exception:
        return None
    _d = _re.findall(r"20\d{2}-\d{2}-\d{2}", _txt)
    return max(_d) if _d else None

# OÙ EST `donnees/` — CORRIGÉ LE 08-09-2026 APRÈS LE PREMIER TIR.
# La première version cherchait sous PROJ. Or la tâche d'audit reconstitue le
# PROJET (structure plate + claude/), qui n'a PAS de donnees/ : le maillon ne
# trouvait rien et se déclarait NON APPLICABLE. Il n'a pas rendu un faux vert —
# il a annoncé son aveuglement, ce qui est le bon comportement — mais il n'a
# RIEN mesuré. Le dossier donnees/ n'existe que du côté DÉPÔT.
# Le radar cherche donc là où le dépôt est réellement cloné, puis se rabat.
_dep = None
for _cand in (os.environ.get("DEPOT_CAC40", ""), "/tmp/depot/donnees",
              "/tmp/depot/d/donnees", os.path.join(PROJ, "donnees"),
              os.path.join(PROJ, "..", "donnees")):
    if _cand and os.path.isdir(_cand):
        _dep = _cand
        break
if _dep is None:
    rapport.append((WARN, "19-Fraîcheur dépôt",
                    "dossier donnees/ introuvable — la fraîcheur au dépôt n'est PAS mesurée. "
                    "Le dépôt est-il cloné dans cette session ? Chemins essayés : "
                    "$DEPOT_CAC40, /tmp/depot/donnees, /tmp/depot/d/donnees, <projet>/donnees"))
    score["warn"] += 1
else:
    _auj = datetime.now(ZoneInfo("Europe/Paris")).date()
    for _motif, _seuil, _quoi in _DONNEES_SUIVIES:
        _cands = [f for f in os.listdir(_dep) if _norm(_motif) in _norm(f)]
        if not _cands:
            rapport.append((WARN, "19-Fraîcheur dépôt",
                            f"{_motif} absent du dépôt — {_quoi}"))
            score["warn"] += 1
            continue
        _p = os.path.join(_dep, _le_plus_recent(_cands))   # la date, jamais l alphabet
        _dt = _derniere_date_du_contenu(_p)
        if _dt is None:
            # Un fichier d'ÉTAT COURANT vide n'a pas de date, et c'est normal :
            # zéro position ouverte est un état légitime, pas une anomalie.
            if _seuil is None:
                check(f"19-{_motif}", True,
                      f"aucune date au contenu — {_quoi} (état vide, normal)",
                      "sans objet")
            else:
                rapport.append((WARN, "19-Fraîcheur dépôt",
                                f"{_motif} : aucune date lisible dans le contenu"))
                score["warn"] += 1
            continue
        try:
            _age = (_auj - datetime.strptime(_dt, "%Y-%m-%d").date()).days
        except Exception:
            continue
        if _seuil is None:
            check(f"19-{_motif}", True,
                  f"dernière date au dépôt {_dt} (âge {_age} j) — {_quoi}, pas de seuil",
                  "sans objet")
        else:
            check(f"19-{_motif}", _age <= _seuil,
                  f"dernière date au dépôt {_dt} (âge {_age} j, seuil {_seuil}) — {_quoi}",
                  f"N'AVANCE PLUS : dernière date {_dt}, {_age} jours — {_quoi}. "
                  f"Soit la tâche n'écrit plus, soit elle écrit ailleurs qu'au dépôt.")

# ═══ MÉTA-VÉRIFICATION — angles morts du radar ═══
# Liste les fichiers du projet qu'AUCUNE vérification ci-dessus ne surveille.
motifs_couverts = ["PROMPT_BOUCLE","TACHE_COWORK","cac40_ohlcv","CONSOLIDATION","MODULE_C5_ETENDU","MODULE_C5_EI",
    "RAV","positions_ouvertes","trading_journal","journal_trades","journal_paper","cockpit",
    "gen_cockpit","generateur_cockpit","journal_apprentissage","registre_candidates","golden",
    "REGISTRE_REGLES","PILOTE","BACKLOG_DECISIONS","registre_veille","REPRISE","audit_ecosysteme",
    "PASSATION","cours_nouveaux","journal_lectures","audit_du_jour","strategies_validees",
    "cac40_strategies","protocole_qualite","journal_trades","COMMENT_MARCHE","PRT_SYNTAXE","TEST_PROREALTIME","historique",
    "signal_achat","methodologies","C6_","C8_","MEMOIRE","AUDIT_","backlog_au",
    # ajoutés le 01/08 — documents créés depuis la dernière mise à jour du radar
    "STRATEGIE_","ETUDE_","TABLEAU_","verif_backlog","C5_ETENDU_10","ETAT_REEL",
    "REVEIL_GOOGLEFINANCE","SOLUTION_CHARGEMENT","TACHE_COWORK","MODULE_C5",
    "golden_tests","registre_","claude_","journal_","cac40_","projet_cac40",
    "trading_journal","audit_ecosysteme","REGISTRE_"]
non_couverts = [f for f in fichiers
                if not any(_norm(m) in _norm(f) for m in motifs_couverts)
                and not f.startswith(".") and f != "__pycache__"]
if non_couverts:
    rapport.append((WARN, "9-MétaRadar",
        f"{len(non_couverts)} fichier(s) non surveillé(s) par le radar : {', '.join(sorted(non_couverts)[:8])}"
        + (" …" if len(non_couverts) > 8 else "")))
    score["warn"] += 1
else:
    rapport.append((OK, "9-MétaRadar", "Tous les fichiers du projet sont couverts par une vérification"))
    score["ok"] += 1

# ═══ RAPPORT ═══
lignes = [f"# AUDIT ÉCOSYSTÈME CAC 40 — {TSH}",
          f"# Score : {score['ok']} ✅  ·  {score['warn']} ⚠️  ·  {score['fail']} ❌",
          f"# Règle : tout ❌ = faille bloquante à corriger en priorité ; tout ⚠️ = à planifier.",
          ""]
for sig, maillon, msg in rapport:
    lignes.append(f"{sig} [{maillon}] {msg}")
texte = "\n".join(lignes)
print(texte)

# ─── SAUVEGARDE — LÀ OÙ LE PROGRAMME TOURNE, PAS OÙ IL TOURNAIT AUTREFOIS
# TROUVÉ PAR LE PREMIER PASSAGE COMPLET, le 13-09-2026 à 12h11, et c est
# exactement ce que le retrait des masques devait produire :
#   ❌ collecte · Passer le radar A ECHOUE (code 1)
#   FileNotFoundError: '/mnt/user-data/outputs/AUDIT_ECOSYSTEME_...md'
# `/mnt/user-data/outputs` n existe que dans la machine du Chat. **C est un
# vestige de la vie du radar en tâche Cowork.** Sur GitHub, le dossier n existe
# pas, et le radar mourait APRÈS avoir tout calculé — son rapport etait complet,
# son ecriture tombait.
# **Ce matin encore, `set +e` et `|| true` auraient rendu ce pas VERT.**
# Le rapport va desormais dans `rapports/`, au depot, ou le workflow le commite ;
# et le programme ne se recopie plus lui-meme : git s en charge.
import os as _os
_dest = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
                      "rapports")
if not _os.path.isdir(_dest):
    _dest = _os.path.join(PROJ, "rapports")
_os.makedirs(_dest, exist_ok=True)
def _sortie_mene_au_rituel():
    """Dit si la sortie du programme est redirigée vers le fichier que lit le rituel du soir.

    ① RÔLE — Distinguer le passage du soir d'une simple vérification, pour que seul le
      premier laisse un fichier derrière lui. Le problème qu'elle règle est mesuré :
      le 17-09-2026, le dépôt portait 59 rapports datés, dont six écrits dans la même
      nuit et trois en six minutes, tous produits par des tours de vérification. Le
      protocole de livraison demande de relancer jusqu'à ce qu'un tour ne trouve rien :
      plus il est suivi, plus le dépôt grossit. Et le radar signale lui-même le nombre
      de fichiers que personne ne surveille — il grossissait donc ce qu'il mesure.
    ② CONTEXTE D'APPEL — Un seul endroit, la toute fin du programme, une fois par
      passage, juste après l'affichage du rapport. Son résultat décide si le fichier
      rapports/AUDIT_ECOSYSTEME.md est écrit ou non.
    ③ ENTRÉE — Aucun paramètre. Elle regarde le descripteur de sortie standard du
      processus, par le chemin /proc/self/fd/1, et le compare au fichier
      rapports/audit_du_jour.md du dossier où vit le programme.
    ④ CONDITIONS D'ENTRÉE — Le système doit offrir /proc, ce qui est le cas sur les
      machines Linux où tourne la tâche planifiée et faux sur macOS et sur Windows. Le
      fichier rapports/audit_du_jour.md doit exister pour que la comparaison puisse
      avoir lieu.
    ⑤ SORTIE — UNE valeur : vrai quand la sortie standard mène exactement au même
      fichier que rapports/audit_du_jour.md, faux dans tous les autres cas. Mesuré le
      20-09-2026 sur une copie du dépôt : lancée avec une redirection vers
      rapports/audit_du_jour.md, elle rend vrai et le programme affiche
      [Rapport : .../rapports/AUDIT_ECOSYSTEME.md] ; lancée avec une redirection vers
      un autre fichier ou à travers un tuyau, elle rend faux et le programme affiche
      [Verification — aucun rapport date ecrit.].
      [rend: 1]
    ⑥ TRAITEMENT — ① lire vers quoi pointe la sortie standard, et rendre faux si le
      système ne le dit pas · ② composer le chemin attendu, celui de
      rapports/audit_du_jour.md · ③ relever l'identité des deux fichiers auprès du
      système, et rendre faux si l'un des deux n'existe pas · ④ rendre vrai si les deux
      identités sont la même.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Elle compare les FICHIERS eux-mêmes et non leurs noms. La première
      version comparait le nom du fichier de sortie au texte audit_du_jour.md, et elle
      se trompait dans les DEUX sens : un fichier quelconque nommé ainsi taisait le
      rapport alors qu'il aurait été juste de l'écrire, et renommer le fichier du
      rituel désarmait le contrôle. C'était une énumération d'un seul élément,
      déguisée en propriété. Le critère qui tranche tient en une question : si je
      renomme un fichier, mon contrôle change-t-il d'avis ? Demander au système
      l'identité d'un fichier répond non : deux chemins différents vers le même
      fichier rendent le même verdict, et un homonyme ailleurs ne trompe plus.
    ⑨ CE QUI CLOCHE — trois points, dont deux sont nommés par le code lui-même :
      ① UNE SORTIE EN TUYAU N'EST PAS VUE. La forme
      audit_ecosysteme.py | tee rapports/audit_du_jour.md mène à un tuyau et non au
      fichier : la fonction rend faux, et le rapport du soir ne serait pas écrit alors
      qu'il devrait l'être. Mesuré le 20-09-2026 : lancée à travers un tuyau, le
      programme affiche [Verification — aucun rapport date ecrit.]. Le pas de la tâche
      planifiée ne fait pas cela, il redirige ; un humain pourrait.
      ② SUR UN SYSTÈME SANS /proc, ELLE REND TOUJOURS FAUX. C'est le cas de macOS et de
      Windows. Le programme revient alors au comportement d'avant la correction : il
      n'écrit aucun rapport daté. C'est la dégradation SÛRE, jamais pire que ce qui
      existait.
      ③ LE FICHIER ÉCRIT N'EST PAS CELUI QUI EST COMPARÉ, ET LES DEUX NOMS SE
      RESSEMBLENT. La fonction compare à rapports/audit_du_jour.md, et quand elle rend
      vrai, le programme écrit rapports/AUDIT_ECOSYSTEME.md — un second fichier, de
      nom fixe, écrasé à chaque passage du soir. Le fichier du rituel, lui, est écrit
      par la redirection du pas de la tâche planifiée, pas par ce programme. Un lecteur
      qui cherche qui écrit rapports/audit_du_jour.md ne le trouvera nulle part dans ce
      fichier.
    ⑩ EFFET — LIT le lien que le système tient sur la sortie standard, et relève
      l'identité de deux fichiers. N'écrit aucun fichier, n'affiche rien, ne touche pas
      au réseau. C'est son APPELANT qui écrit, selon ce qu'elle rend.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas : les deux échecs
      possibles, l'absence de /proc et l'absence d'un des deux fichiers, sont
      rattrapés et rendus sous la forme d'un faux. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le rituel de début de session : les gestes imposés à l'ouverture d'une
        conversation — relever la date, cloner le dépôt, lire le PILOTE, lire
        le rapport du radar
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque
        soir, qui contrôle l'ensemble du système et range chacun de ses
        constats sous un numéro de maillon, par exemple 18-Tâches pour le
        contrôle des traces laissées par les tâches planifiées.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
      la tâche planifiée : un fichier de .github/workflows/ qui fait tourner
        un programme à heure fixe sur une machine GitHub, sans clic ni
        autorisation.
      le protocole de livraison : la suite de huit gestes imposée avant toute livraison, dont l'un
        demande de recommencer jusqu'à ce qu'un tour ne trouve plus rien
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    # ON COMPARE LES FICHIERS, PAS LEURS NOMS — cassure de Cowork, tour 64.
    # **La premiere version comparait `basename(cible) == "audit_du_jour.md"`.
    # Elle se trompait dans les DEUX sens : un fichier quelconque nomme ainsi
    # taisait le message alors qu il serait vrai · renommer le rituel desarmait
    # le controle.** Le §7 pose le critere en une question : SI JE RENOMME UN
    # FICHIER, MON CONTROLE CHANGE-T-IL D AVIS ? Il changeait. C etait une
    # enumeration d un seul element, deguisee en propriete.
    # **`os.stat()` compare les fichiers eux-memes : deux chemins differents
    # vers le meme fichier rendent le meme verdict, et un homonyme ailleurs ne
    # trompe plus.**
    try:
        cible = _os.readlink("/proc/self/fd/1")
    except OSError:
        return False
    attendu = _os.path.join(_dest, "audit_du_jour.md")
    try:
        a, b = _os.stat(cible), _os.stat(attendu)
    except OSError:
        return False
    return (a.st_dev, a.st_ino) == (b.st_dev, b.st_ino)


# UN LANCEMENT DE VERIFICATION N ECRIT PAS DE RAPPORT DATE — cassure de
# Cowork, tour 64. **Mesure du 17-09 : 59 rapports dates au depot, dont SIX de
# la nuit, TROIS en six minutes — tous produits par des tours de verification.**
# **R-746 demande de relancer jusqu a ce qu un tour ne trouve rien : plus le
# protocole est suivi, plus le depot grossit. Et le radar signale lui-meme
# « N fichiers non surveilles » : il grossit ce qu il mesure.**
# **LA PROPRIETE, la meme que pour le message : si la sortie mene au fichier du
# rituel, ce lancement EST celui du soir — il ecrit son rapport date. Sinon
# c est une verification, et elle n a rien a laisser au depot.**
# Le rapport reste affiche a l ecran dans les deux cas : rien n est perdu.
_du_soir = _sortie_mene_au_rituel()
if _du_soir:
    # NOM FIXE, PAS D HORODATAGE — cassure de Cowork, 17-09-2026.
    # **Le rapport horodate est le defaut qu il mesure.** Son diff entre 18h13
    # et 18h14 le montre : le second compte 237 fichiers la ou le premier en
    # comptait 236, **et le 237e est le premier rapport.** Le radar grossit ce
    # qu il mesure, et signale ensuite « N fichiers non surveilles ».
    # Mesure du 17-09 : 58 rapports avant le lot du Chat, 60 apres.
    # **L historique vit dans git, pas dans les noms de fichier** (A-414).
    out = _os.path.join(_dest, "AUDIT_ECOSYSTEME.md")
    open(out, "w", encoding="utf-8").write(texte + "\n")
    print(f"\n[Rapport : {out}]")
else:
    print(f"\n[Verification — aucun rapport date ecrit. Le circuit du soir "
          f"en ecrit un ; ce lancement n en est pas.]")
# L AVERTISSEMENT « CE LANCEMENT N ECRIT PAS LE FICHIER DU RITUEL » EST RETIRE.
# **JEAN-LUC, 17-09-2026 : « si on a deja l ecosysteme qui repond au probleme,
# je ne comprends plus le probleme. Quel probleme essayes-tu de resoudre ? »**
#
# Le probleme d origine etait reel : `rapports/audit_du_jour.md` etait fige
# depuis trois jours et le rituel du §3 le faisait lire comme s il etait frais.
# **Mais il est deja resolu, par `fabrique_du_jour()` dans
# programmes/CONTRATS_DES_FICHIERS.py, ecrit le meme matin : il compare la date
# portee par le fichier a celle du jour et refuse si elles different.**
#
# L avertissement n ajoutait rien : quelqu un qui relance ce programme en
# croyant rafraichir le fichier du rituel sera detrompe par le controle de date,
# qui porte sur le FAIT — le fichier est-il du jour — et non sur une intention.
# **Il aura coute deux tours de relecture et deux corrections, pour resoudre un
# probleme qui n existait plus.**

# JE N ECRIS PAS `audit_du_jour.md` — CASSURE DE COWORK, 16-09-2026.
# **Mon diagnostic etait FAUX.** J avais conclu que le radar ecrivait un nom
# date et le workflow un nom fixe, « les deux ne se rencontrant jamais ».
# **La redirection du pas 246 ecrivait deja le nom fixe, et elle est la depuis
# le 12-09.** Mon correctif a mis DEUX MAINS sur le meme fichier : deux
# descripteurs, deux positions independantes, et la seconde ecriture coupait
# la premiere en plein mot — « A201_ORIGINE_BANQUES_Ve[Rapport du jour : ... ».
# **Et la preuve que ma cause etait fausse tient en un fichier : `PILOTE.md`
# porte un nom FIXE, sans aucun nom date nulle part, et il est fige au 13-09
# exactement comme le rapport. Une cause qui n explique qu un des deux fichiers
# arretes le meme jour au meme commit n est pas la cause.**
