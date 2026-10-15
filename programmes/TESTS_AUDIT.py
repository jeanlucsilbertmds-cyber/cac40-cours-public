#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Éprouve le radar programmes/audit_ecosysteme.py par onze cas, un par défaut déjà
rencontré, et rend un code de sortie non nul dès qu'un cas tombe.

DÉCIDÉ · outil · v1.0 · 29-08-2026 · Rôle : eprouver le radar sur tous les cas
connus, et REFUSER de valider si l'un tombe.
Quand l'appeler : avant TOUT depot de audit_ecosysteme.py. Jamais apres.

POURQUOI CE FICHIER EXISTE
    Le 28 et le 29-08-2026, huit versions du radar se sont succede en une soiree.
    Chaque correction en revelait une autre, toutes de la MEME FAMILLE : un
    correctif juste pour un cas, faux pour le cas voisin.
      v2.3  les sous-dossiers sont vus
      v2.4  la date lue etait celle du fichier, pas celle de la trace
      v2.5  un tableau s'empile, un document redige non — la v2.4 avait
            repare l'un en cassant l'autre
      v2.6  le comptage calendaire criait chaque dimanche
      v2.7  le comptage ouvre avait ete applique aux quatre taches quand une
            seule a un calendrier lun-ven — miroir exact du precedent
      v2.8  un mode inconnu retombait en silence sur le calendaire, et un mode
            oublie faisait disparaitre les taches suivantes du rapport

    AUCUN de ces defauts n'a ete trouve par relecture. TOUS l'ont ete par
    execution. Et aucun n'a ete anticipe : chacun est apparu APRES la livraison.

CE QUE CE FICHIER CHANGE
    Il ne demande a personne d'etre plus vigilant — les promesses de vigilance ne
    survivent pas a la fin d'une conversation. Il RE-JOUE tous les cas connus a
    chaque modification, et il RETOURNE UN ECHEC si l'un tombe.
    Un cas ajoute ici ne peut plus etre oublie.

CE QU'IL NE FAIT PAS
    Il ne prouve pas l'absence de defaut : il prouve que les defauts DEJA VUS ne
    reviennent pas. C'est peu, et c'est la seule chose qu'un jeu de tests puisse
    honnetement offrir.

① RÔLE — Empêcher qu'une nouvelle version du radar soit déposée sans preuve. Le radar
  est le programme qui contrôle chaque soir l'ensemble du système ; quand il se
  trompe, il se tait, et personne ne voit que plus rien ne surveille. Ce programme
  rejoue onze défauts déjà rencontrés et rend un code de sortie non nul si l'un d'eux
  est revenu.
② CONTEXTE D'APPEL — À la main, depuis le dossier programmes/, avant tout dépôt d'une
  version du radar, par celui qui vient de le modifier. AUCUNE TÂCHE PLANIFIÉE NE LE
  LANCE : recherche du mot TESTS_AUDIT dans .github/workflows/ le 19-09-2026, zéro
  occurrence. Le document archives/PHOTOGRAPHIE_ABANDONNEE_24-09-2026_voir_A-452.md le range parmi les vingt-trois
  programmes qui ne tournent pas le soir, et l'étude
  etudes/PLAN_ASSAINIR_v2_Sam_12-09-2026_19h30.md le compte parmi les quatre
  programmes de preuve lancés à la main par construction.
③ ENTRÉE — La ligne de commande, un seul argument : le dossier à faire examiner par le
  radar, par exemple un point depuis un clone neuf. Sans argument, le programme prend
  le nom arbo, qui n'existe nulle part au dépôt du 19-09-2026.
④ CONDITIONS D'ENTRÉE — Le programme doit être lancé DEPUIS le dossier programmes/,
  parce qu'il cherche le radar sous le nom audit_ecosysteme.py, relatif au dossier de
  travail. Mesuré le 19-09-2026 : lancé depuis le premier niveau du dépôt, il s'arrête
  aussitôt sur ARRET : audit_ecosysteme.py introuvable, code 2. Le dossier temporaire
  du système doit pouvoir porter deux copies complètes du dépôt en même temps — une
  copie pèse 12 Mo pour 243 fichiers, mesuré le 19-09-2026.
⑤ SORTIE — Un code de sortie, et rien d'autre : 0 quand les onze cas passent, 1 quand
  au moins un tombe, 2 quand le dossier d'épreuve ou le radar est introuvable. Ce
  détail est affiché à l'écran, une ligne par cas.
⑥ TRAITEMENT — ① vérifier que le dossier d'épreuve et le radar existent ·
  ② jouer les onze cas dans l'ordre de la liste, chacun protégé pour qu'une erreur ne
  coupe pas la suite · ③ afficher une ligne par cas · ④ afficher le bilan · ⑤ rendre
  le code de sortie.
⑦ UNITÉ — Les épreuves se comptent en CAS : onze. Un passage complet a duré 5,5
  secondes sur une copie du dépôt du 19-09-2026, qui porte 243 fichiers pour 12 Mo.
⑧ POURQUOI — Les cas ne sont pas des idées : chacun vient d'un défaut réellement
  mesuré sur le radar, et un cas inscrit ici ne se retire jamais. C'est la décision
  A-308, datée du 29-08-2026, qui l'a posé ainsi après huit versions du radar en une
  soirée. Le programme a servi le jour même : il a trouvé un douzième défaut AVANT
  livraison, le premier de la série à être attrapé avant plutôt qu'après.
⑨ CE QUI CLOCHE — quatre points, tous mesurés le 19-09-2026 sur une copie du dépôt :
  ① RÉGLÉ LE 28-09-2026 (A-435 ②) : LES ONZE CAS PASSENT, et les quatre réparés rougissent quand on retire au radar ce qu'ils surveillent (tests/EPREUVES_DU_JEU_DU_RADAR_Lun_28-09-2026.py). Ce qui était mesuré : QUATRE CAS SUR ONZE TOMBAIENT, ET AUCUN NE METTAIT EN CAUSE LE RADAR. Sortie
  complète : 4 CAS SUR 11 TOMBENT. NE RIEN DEPOSER. — un tableau qui s'empile,
  dimanche, un mode inconnu, un mode oublié. Les trois derniers tombent parce que la
  copie modifiée du radar qu'ils fabriquent ne démarre plus : écrite dans le dossier
  temporaire du système, elle n'y trouve pas programmes/COMMUN.py dont le radar dépend
  depuis le 12-09-2026, et s'arrête sur RuntimeError: COMMUN.le_plus_recent
  introuvable. Le premier tombe parce qu'il écrit son fichier d'épreuve au premier
  niveau de la copie alors que le vrai a été rangé dans donnees/. Un jeu d'épreuves
  qui refuse toute livraison pour des raisons qui lui sont propres cesse d'être
  consulté.
  ② RÉGLÉ LE 28-09-2026 (A-435 ②, tests/EPREUVES_DU_JEU_DU_RADAR_Lun_28-09-2026.py) — les deux cas rougissent désormais (SA6, SA10), et dix cas sur onze sont éprouvés contre leur retrait. Ce qui était mesuré : DEUX CAS SUR ONZE NE POUVAIENT PAS ROUGIR. Mesuré en retirant du radar, dans une
  copie, exactement ce que chaque cas surveille : les sous-dossiers sont vus et une
  trace RECOPIEE garde son age sont restés VERTS. Une épreuve qui reste verte quand on
  retire ce qu'elle teste n'est pas une preuve, c'est une décoration (R-731). Cinq cas
  ont été vérifiés capables de rougir — un document redige, une date future, une trace
  absente, une trace sans date, le poids informe ; les quatre qui tombent déjà n'ont
  pas pu l'être.
  ③ RÉGLÉ LE 28-09-2026 (A-435 ②, tests/EPREUVES_DU_JEU_DU_RADAR_Lun_28-09-2026.py) — ce second étage existe, hors de ce programme. Ce qui était écrit : RIEN ICI NE VÉRIFIE QUE LES CAS PEUVENT ROUGIR. Le programme voisin
  programmes/EPREUVES_DU_SOCLE.py porte ce second étage : il retire une à une les
  corrections que ses cas surveillent et exige que le cas visé devienne rouge. Ce
  programme-ci n'a pas d'équivalent, et c'est pourquoi les deux cas décoratifs ont
  vécu sans être vus.
  ④ LE BILAN NE DISTINGUE PAS LE CAS QUI CONSTATE UN DÉFAUT DU CAS QUI N'A PAS PU SE
  JOUER. Les deux paraissent dans la même liste sous le même mot, TOMBENT. Le 19-09-2026, trois des
  quatre échecs du jour étaient du second genre, et leur détail affiché, lignes absentes,
  envoie chercher le défaut dans le radar.
⑩ EFFET — CRÉE puis EFFACE jusqu'à deux copies complètes du dépôt dans le dossier
  temporaire du système, ainsi que trois copies du radar de 91 191 octets chacune.
  LANCE le radar treize fois. NE TOUCHE À AUCUN FICHIER DU DOSSIER REÇU : vérifié le
  19-09-2026 en comparant la somme de contrôle de chacun des 243 fichiers d'une copie
  du dépôt avant et après un passage complet, aucune différence. Aucun accès réseau.
⑪ TERMINAISON — SORT DU PROGRAMME avec le code rendu par main : 0, 1 ou 2. Une erreur
  levée par un cas est rattrapée et comptée comme un échec de ce cas.
⑫ DÉFINITIONS
  le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir,
    qui contrôle l'ensemble du système et range chacun de ses constats sous un
    numéro de maillon, par exemple 18-Tâches pour le contrôle des traces
    laissées par les tâches planifiées.
  un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré
    rejoué à l'identique pour vérifier qu'il n'est pas revenu.
  une copie modifiée du radar : un exemplaire du radar dans lequel un morceau
    de texte a été remplacé, écrit dans le dossier temporaire du système, pour
    éprouver un comportement que le radar ne montre pas tel quel.
  une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle
    a tourné — rapport de boucle, rapport d'audit, cockpit, historique des
    mesures.
  la date déclarée : la date qu'un fichier porte dans son nom ou dans son
    contenu, par opposition à celle que le système de fichiers lui donne.
  la trace : la liste des sources avec leur etat — LU, ABSENT ou ILLISIBLE — et un detail chiffre, affichee en pied de page.
"""

import atexit
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from zoneinfo import ZoneInfo

SCRIPT = "audit_ecosysteme.py"
_A_EFFACER = []          # dossiers temporaires des copies modifiées, effacés à la sortie
atexit.register(lambda: [shutil.rmtree(x, ignore_errors=True) for x in _A_EFFACER])


def _nb_taches(script=SCRIPT):
    """Compte les tâches que le radar déclare surveiller par leurs traces.

    ① RÔLE — Dire combien de lignes le maillon 18 doit rendre, en le lisant dans le
      radar au lieu de l'écrire ici. Le nombre a changé le 30-09-2026 (quatre, puis
      trois quand le cockpit a cessé d'être déclaré) : écrit en dur, il faisait tomber
      trois cas sans que le radar soit en faute.
    ② CONTEXTE D'APPEL — `_c_sous_dossiers`, `_c_mode_inconnu` et `_c_mode_oublie`,
      au plus une fois chacun (pas du tout si le radar lève avant, ou, dans
      `_c_mode_inconnu`, si la ligne de la boucle est absente ou ne dit pas
      INCONNU).
    ③ ENTRÉE — `script` : le radar à lire, par défaut `audit_ecosysteme.py` dans le
      dossier courant, qui est programmes/ quand ce programme tourne.
    ④ CONDITIONS D'ENTRÉE — Le radar doit contenir une liste `_declarations = [` fermée
      par une ligne « ] » indentée de quatre espaces. Sinon, la fonction LÈVE : mieux
      vaut un cas qui tombe qu'un nombre deviné.
    ⑤ SORTIE — UNE valeur : le nombre de déclarations, un entier. Mesuré le 30-09-2026 :
      3.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire le radar · ② isoler le texte entre `_declarations = [` et
      la ligne « ] » qui la ferme · ③ y compter les lignes qui ouvrent une déclaration,
      c'est-à-dire qui commencent par une parenthèse suivie d'un guillemet.
    ⑦ UNITÉ — Un NOMBRE DE TÂCHES.
    ⑧ POURQUOI — Un garde-fou porte sur une propriété, jamais sur un compte (R-721) ;
      et un chiffre qui existe ailleurs ne se recopie pas (R-708).
    ⑨ CE QUI CLOCHE — Elle lit le texte du radar, pas ce qu'il exécute. Mesuré par
      le relecteur le 30-09-2026 : une déclaration entre apostrophes, une déclaration
      écrite sur deux lignes, et la seconde de deux déclarations sur une même ligne ne
      sont pas comptées ; le compte est alors trop bas, et les cas qui exigent « au
      moins » ce nombre deviennent plus permissifs sans le dire. Seul un compte nul
      est refusé.
    ⑩ EFFET — LIT un fichier. N'écrit rien.
    ⑪ TERMINAISON — Rend la main ; LÈVE si la liste est introuvable ou vide. Aucun de ses
      appels ne se termine.
      [sort: non]
    """
    with open(script, encoding="utf-8") as f:
        texte = f.read()
    if "_declarations = [" not in texte or "\n    ]" not in texte.split("_declarations = [", 1)[1]:
        raise RuntimeError("liste _declarations introuvable dans " + script)
    bloc = texte.split("_declarations = [", 1)[1].split("\n    ]", 1)[0]
    n = len(re.findall(r'^\s*\("', bloc, re.M))
    if n == 0:
        raise RuntimeError("aucune tâche déclarée lue dans " + script)
    return n


def _lignes18(dossier, script=SCRIPT):
    """Lance le radar et rend les lignes qu'il consacre au contrôle des traces.

    ① RÔLE — Donner à dix des onze cas la seule matière qu'ils jugent : les lignes que
      le radar consacre au contrôle des traces laissées par les tâches planifiées. Le
      radar affiche un rapport d'une soixantaine de lignes, une par constat, chacune
      préfixée d'un signe et d'un numéro de maillon ; ces cas ne regardent que celles
      du maillon 18. Sans cette fonction, dix appels de sous-processus seraient écrits
      dix fois, et deux écritures d'une même chose divergent toujours (R-708).
    ② CONTEXTE D'APPEL — Dix des onze cas, une fois chacun, sauf deux fois pour le cas
      de la trace recopiée : `_c_sous_dossiers`, `_c_recopie`, `_c_tableau_empile`,
      `_c_document_redige`, `_c_date_future`, `_c_weekend`, `_c_mode_inconnu`,
      `_c_mode_oublie`, `_c_trace_absente` et `_c_sans_date`. Seul
      `_c_place_pas_alerte` ne l'appelle pas : il regarde un autre maillon et refait
      lui-même son lancement. Jamais appelée ailleurs.
    ③ ENTRÉE — `dossier` : le dossier que le radar doit examiner, soit le dossier
      d'épreuve reçu sur la ligne de commande, soit une copie temporaire fabriquée par
      le cas · `script` : le programme à lancer, qui vaut par défaut le nom
      audit_ecosysteme.py ; les trois cas qui éprouvent un radar modifié y passent le
      chemin d'une copie écrite dans le dossier temporaire du système.
    ④ CONDITIONS D'ENTRÉE — Le programme doit être lancé depuis le dossier
      programmes/, parce que le nom audit_ecosysteme.py est relatif au dossier de
      travail. Mesuré le 19-09-2026 : lancé depuis le premier niveau du dépôt, le
      programme s'arrête avant tout cas sur ARRET : audit_ecosysteme.py introuvable,
      code 2.
    ⑤ SORTIE — UNE valeur : la liste des lignes affichées par le radar qui contiennent
      le texte 18-T. Liste VIDE quand le radar n'a rien affiché, y compris quand il
      s'est arrêté sur une erreur.
      [rend: 1]
    ⑥ TRAITEMENT — ① lancer le radar dans un sous-processus, avec le même interpréteur
      Python que celui qui exécute ce programme · ② lui passer le dossier à examiner
      comme unique argument · ③ capturer ses deux sorties, en remplaçant les
      caractères illisibles plutôt qu'en tombant · ④ ne garder de la sortie normale
      que les lignes contenant 18-T.
    ⑦ UNITÉ — Un NOMBRE DE LIGNES. Mesuré le 19-09-2026 sur une copie du dépôt :
      quatre lignes, une par tâche déclarée dans le radar — la boucle du jour, l'audit
      du soir, la tâche du cockpit, la mesure de performance. Trois depuis le
      30-09-2026 : le cockpit n'est plus déclaré.
    ⑧ POURQUOI — Le sous-processus emploie l'interpréteur courant et non le mot
      python3 : les copies éprouvées vivent dans un dossier temporaire, et rien ne
      garantit que le python3 trouvé dans le chemin du système soit celui qui a
      démarré ce programme. Les caractères illisibles sont remplacés plutôt que de
      faire tomber la lecture, parce que le rapport du radar porte des signes colorés
      et des lettres accentuées dont le codage dépend de la machine.
    ⑨ CE QUI CLOCHE — trois points, tous mesurés le 19-09-2026 :
      ① Le code de sortie du radar n'est jamais regardé, et sa sortie d'erreur est
      capturée puis jetée. Un radar qui s'arrête sur une erreur rend donc une liste
      vide, exactement comme un radar qui a tourné sans rien dire du maillon 18. C'est
      le cas aujourd'hui : les trois cas qui lancent une copie modifiée du radar
      reçoivent une liste vide parce que cette copie s'arrête sur RuntimeError:
      COMMUN.le_plus_recent introuvable, et ce programme annonce ligne absente. Le
      lecteur cherche un défaut dans le radar alors que c'est le lancement qui a
      échoué.
      ② Aucune limite de temps. Un radar qui n'en finirait pas bloquerait le jeu
      d'épreuves sans message et sans fin. Un passage complet dure 5,5 secondes sur
      une copie du dépôt, donc le défaut ne s'est jamais vu ; le programme voisin
      programmes/EPREUVES_DU_SOCLE.py, lui, borne chacun de ses lancements à 300
      secondes.
      ③ Le filtre épelle. Il cherche le texte 18-T, début du libellé 18-Tâches :
      renommer ce maillon éteindrait dix cas d'un coup, en silence, chacun annonçant
      ligne absente. Le critère qui tranche tient en une question : si je renomme, mon
      contrôle change-t-il d'avis ? Ici oui, donc il épelle.
    ⑩ EFFET — LANCE UN AUTRE PROGRAMME. Le radar lancé crée le dossier rapports/ s'il
      n'existe pas, et n'y écrit son rapport que lorsque sa sortie standard mène au
      fichier du rituel du soir — ce qui n'arrive jamais ici, puisqu'elle est
      capturée. Vérifié le 19-09-2026 : somme de contrôle des 243 fichiers d'une copie
      du dépôt avant et après un passage complet du jeu d'épreuves, aucune différence.
      Cette fonction elle-même n'écrit aucun fichier, n'affiche rien et ne touche pas
      au réseau.
    ⑪ TERMINAISON — Rend la main dans toutes les conditions mesurées. PEUT LEVER si le
      sous-processus ne peut pas démarrer, par exemple sur un chemin de programme
      inexistant. Aucun de ses appels ne se termine : un radar qui s'arrête n'arrête
      que son propre sous-processus, et sa sortie revient ici comme un résultat
      ordinaire.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir,
        qui contrôle l'ensemble du système et range chacun de ses constats sous un
        numéro de maillon, par exemple 18-Tâches pour le contrôle des traces
        laissées par les tâches planifiées.
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré
        rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle
        a tourné — rapport de boucle, rapport d'audit, cockpit, historique des
        mesures.
      la boucle du jour : la tâche planifiée qui collecte les cours et écrit le
        rapport de boucle, du lundi au vendredi seulement.
      une copie modifiée du radar : un exemplaire du radar dans lequel un morceau
        de texte a été remplacé, écrit dans le dossier temporaire du système, pour
        éprouver un comportement que le radar ne montre pas tel quel.
    
      la trace : la liste des sources avec leur etat — LU, ABSENT ou ILLISIBLE — et un detail chiffre, affichee en pied de page.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    r = subprocess.run([sys.executable, script, dossier],
                       capture_output=True, text=True, errors="replace")
    return [x for x in r.stdout.splitlines() if "18-T" in x]


def _dater(dossier, motif, date_voulue):
    """Force la date DECLAREE d'une trace, dans son contenu.

    ① RÔLE — Fabriquer une trace vieille sans toucher au calendrier : remplacer, dans
      le CONTENU des fichiers d'une copie, la date qu'ils déclarent par celle que le
      cas veut éprouver. Deux cas en ont besoin — vérifier qu'une trace recopiée garde
      son âge, et vérifier qu'un dimanche la boucle du jour reste silencieuse pendant
      que l'audit du soir est dénoncé.
    ② CONTEXTE D'APPEL — Deux cas, et toujours sur une copie temporaire :
      `_c_recopie`, une fois, sur les fichiers dont le nom contient audit_du_jour ;
      `_c_weekend`, trois fois de suite, sur rapport_boucle, puis cours_nouveaux, puis
      audit_du_jour. Jamais appelée ailleurs.
    ③ ENTRÉE — `dossier` : la copie à modifier, jamais le dossier d'épreuve reçu ·
      `motif` : le fragment de nom de fichier à retenir, écrit en minuscules, par
      exemple audit_du_jour · `date_voulue` : la date à écrire, sous la forme
      année-mois-jour, par exemple 2026-08-11.
    ④ CONDITIONS D'ENTRÉE — `dossier` doit exister et ses fichiers être accessibles en
      écriture. Les fichiers visés doivent porter leur date sous la forme
      année-mois-jour : c'est la seule forme reconnue ici.
    ⑤ SORTIE — Ne rend rien. Son résultat est l'état des fichiers de la copie.
      [rend: rien]
    ⑥ TRAITEMENT — ① parcourir tous les fichiers du dossier, sous-dossiers compris ·
      ② ne garder que ceux dont le nom, mis en minuscules, contient le motif ·
      ③ lire le fichier en remplaçant les caractères illisibles · ④ y remplacer TOUTES
      les dates, des deux formes, année-mois-jour et jour-mois-année, par la date
      voulue écrite dans la même forme · ⑤ réécrire le fichier · ⑥ faire de même dans
      son NOM, et le renommer ; si deux traces prennent le même nom, la dernière
      reste · une erreur de lecture ou d'écriture remonte au cas (28-09-2026).
    ⑦ UNITÉ — Une DATE de calendrier, écrite année-mois-jour.
    ⑧ POURQUOI — La date est changée dans le contenu et non dans le nom du fichier,
      parce que c'est là que le radar la lit pour les fichiers visés : au dépôt du
      19-09-2026, rapports/audit_du_jour.md et donnees/claude_cours_nouveaux.csv
      portent tous deux un nom sans date. Changer la date du fichier sur le disque ne
      servirait à rien : le radar ne la lit plus depuis le 28-08-2026, précisément
      parce qu'elle ment après une recopie.
    ⑨ CE QUI CLOCHE — deux points, mesurés le 19-09-2026, RÉGLÉS le 28-09-2026 avec
      un troisième (la date portée par le NOM restait, et le cas « dimanche » ne
      pouvait pas rougir). Ce qui était mesuré :
      ① LA FORME DE DATE RECONNUE N'EST PAS CELLE QU'ÉCRIT LE RADAR, ET LE
      VIEILLISSEMENT N'A DONC PAS LIEU. Le rapport d'audit commence par la ligne #
      AUDIT ÉCOSYSTÈME CAC 40 — Jeu 17-09-2026 23h56 (Paris) : le jour vient en
      premier, l'année en dernier. La forme cherchée ici est l'inverse, l'année
      d'abord, et ne la rencontre pas. Mesuré : après un forçage au 2026-08-11 des
      fichiers portant audit_du_jour, le radar annonce toujours dernière trace datée
      2026-09-17. Le radar, lui, lit les DEUX formes. La trace prétendument vieillie a
      exactement l'âge qu'elle avait, et les deux cas qui s'appuient dessus jugent
      autre chose que ce qu'ils annoncent.
      ② Un échec d'écriture est avalé sans un mot : les erreurs du système de fichiers
      sont rattrapées et rien n'est affiché. Un fichier en lecture seule laisse donc
      le cas s'exécuter sur une donnée non modifiée, et ce cas rendra un verdict vert
      sur une situation qu'il n'a pas fabriquée.
    ⑩ EFFET — RÉÉCRIT entièrement chaque fichier dont le nom porte le motif, dans le
      dossier reçu, et RENOMME ceux dont le nom porte une date. N'affiche rien, ne touche pas au réseau. Ses deux appelants ne lui
      donnent que des copies temporaires ; rien dans la fonction ne l'impose.
    ⑪ TERMINAISON — Rend la main, ou LÈVE sur une erreur du système de fichiers,
      que le cas appelant transforme en échec ; un mauvais codage ne la fait pas
      lever, la lecture remplaçant les caractères illisibles. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir,
        qui contrôle l'ensemble du système et range chacun de ses constats sous un
        numéro de maillon, par exemple 18-Tâches pour le contrôle des traces
        laissées par les tâches planifiées.
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré
        rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle
        a tourné — rapport de boucle, rapport d'audit, cockpit, historique des
        mesures.
      la date déclarée : la date qu'un fichier porte dans son nom ou dans son
        contenu, par opposition à celle que le système de fichiers lui donne.
      la boucle du jour : la tâche planifiée qui collecte les cours et écrit le
        rapport de boucle, du lundi au vendredi seulement.
    
      l'audit du soir : programmes/audit_ecosysteme.py, lance chaque soir par la tache planifiee, qui ecrit rapports/audit_du_jour.md
      la trace : la liste des sources avec leur etat — LU, ABSENT ou ILLISIBLE — et un detail chiffre, affichee en pied de page.
"""
    # LES DEUX FORMES DE DATE, DANS LE CONTENU ET DANS LE NOM (28-09-2026, A-435 ②) :
    # le radar lit la date du NOM d'abord pour un document, et les deux formes,
    # année-mois-jour et jour-mois-année. Ne remplacer que la première forme, et
    # seulement dans le contenu, laissait au cas « dimanche » la date du 07-09 portée
    # par le nom rapports/claude_rapport_boucle_2026-09-07.md : il restait vert
    # quand on retirait au radar le calcul en jours ouvrés.
    a, m, j = date_voulue.split("-")
    inverse = f"{j}-{m}-{a}"
    def _redater(texte):
        """Remplace toutes les dates d'un texte par la date voulue, dans leur forme.

        ① RÔLE — Vieillir ou rajeunir une trace, contenu et nom, pour `_dater`.
        ② CONTEXTE D'APPEL — `_dater`, deux fois par fichier : son contenu, son nom.
        ③ ENTRÉE — `texte` : un contenu de fichier ou un nom de fichier.
        ④ CONDITIONS D'ENTRÉE — `date_voulue` (année-mois-jour) et `inverse`
          (jour-mois-année) sont posées par `_dater` avant l'appel.
        ⑤ SORTIE — UNE valeur : le texte, chaque date remplacée.
          [rend: 1]
        ⑥ TRAITEMENT — ① remplacer chaque année-mois-jour par `date_voulue` ·
          ② remplacer chaque jour-mois-année par `inverse`.
        ⑦ UNITÉ — Des DATES de calendrier.
        ⑧ POURQUOI — Le radar lit les deux formes (voir `_dater`).
        ⑨ CE QUI CLOCHE — Une suite de chiffres qui a la forme d'une date sans en
          être une est remplacée aussi : les copies sont jetables.
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend toujours la main.
          [sort: non]
        """
        texte = re.sub(r"20\d\d-\d{2}-\d{2}", date_voulue, texte)
        return re.sub(r"\d{2}-\d{2}-20\d\d", inverse, texte)
    cibles = [p for p in glob.glob(dossier + "/**/*", recursive=True)
              if os.path.isfile(p) and motif in os.path.basename(p).lower()]
    for p in cibles:                      # une erreur d écriture n est plus avalée
        with open(p, encoding="utf-8", errors="replace") as f:
            t = f.read()
        with open(p, "w", encoding="utf-8") as f:
            f.write(_redater(t))
        nouveau = os.path.join(os.path.dirname(p), _redater(os.path.basename(p)))
        if nouveau != p:
            os.replace(p, nouveau)        # deux traces du même jour : la dernière reste


def _variante(remplacements):
    """Ecrit une copie du script avec des substitutions, rend son chemin.

    ① RÔLE — Donner aux cas un radar volontairement modifié, sans toucher au vrai.
      Trois défauts déjà rencontrés ne se montrent qu'en changeant le radar lui-même :
      lui faire croire qu'on est dimanche, lui faire écrire un mode de comptage mal
      orthographié, lui retirer un mode de comptage.
    ② CONTEXTE D'APPEL — Trois cas, une fois chacun : `_c_weekend`, `_c_mode_inconnu`,
      `_c_mode_oublie`. Chacun efface le fichier reçu dès qu'il a fini, dans une
      clause qui s'exécute même en cas d'erreur. Jamais appelée ailleurs.
    ③ ENTRÉE — `remplacements` : une liste de couples de textes, l'ancien puis le
      nouveau. Les trois appelants n'en passent qu'un seul chacun ; exemple relevé le
      19-09-2026, remplacer 1, "ouvré" par 1, "ouvre".
    ④ CONDITIONS D'ENTRÉE — Le fichier audit_ecosysteme.py doit être lisible depuis le
      dossier de travail. Chaque texte à remplacer doit figurer au moins une fois dans
      le radar : mesuré le 19-09-2026, les trois ancres employées par les cas y
      figurent exactement une fois chacune. Le dossier temporaire du système doit
      pouvoir porter une copie du radar, soit 91 191 octets.
    ⑤ SORTIE — UNE valeur : le chemin du fichier écrit, dans le dossier temporaire du
      système, avec le suffixe .py. L'appelant est chargé de l'effacer.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire le radar en entier · ② pour chaque couple, lever
      `ValueError` si l'ancien texte est absent, sinon remplacer la PREMIÈRE
      occurrence · ③ créer un dossier temporaire, y recopier les programmes voisins
      du radar, et y écrire le résultat sous `radar_modifie.py` · ④ rendre son
      chemin. Le dossier est effacé à la sortie du programme.
    ⑦ UNITÉ — Un NOMBRE D'OCCURRENCES : au moins une exigée, une seule remplacée.
    ⑧ POURQUOI — Le fichier temporaire n'est pas effacé à la fermeture parce qu'il
      doit survivre à celle-ci pour être lancé ensuite comme un programme par un
      sous-processus. Et une seule occurrence est remplacée, pour que le cas modifie
      exactement l'endroit qu'il vise et pas ses homonymes.
    ⑨ CE QUI CLOCHE — quatre points, tous mesurés le 19-09-2026 ; ① et ② RÉGLÉS le
      28-09-2026 (A-435 ②) : la copie emporte ses voisins, et l'ancre absente lève
      `ValueError`, qui ne disparaît pas sous `-O`. Ce qui était mesuré :
      ① LA COPIE NE DÉMARRE PLUS, ET TROIS CAS SUR ONZE TOMBENT À CAUSE DE CELA. Elle
      est écrite dans le dossier temporaire du système, loin du dépôt. Or depuis le
      12-09-2026 le radar charge la fonction le_plus_recent depuis
      programmes/COMMUN.py, cherché à côté de lui : dans le dossier temporaire ce
      voisin n'existe pas, et la copie s'arrête sur RuntimeError:
      COMMUN.le_plus_recent introuvable — le radar refuse de choisir un fichier au
      hasard alphabetique. Conséquence mesurée : dimanche, un mode inconnu et un mode
      oublié tombent tous les trois, en annonçant lignes absentes, et le jeu
      d'épreuves conclut NE RIEN DEPOSER alors que le radar n'y est pour rien.
      ② Le contrôle de présence de l'ancre est une assertion, et les assertions
      disparaissent quand Python est lancé avec l'option -O. Mesuré : avec python3 -O,
      un appel portant une ancre qui n'existe nulle part rend tout de même un chemin,
      et ce fichier est une copie EXACTE du radar. Les trois cas éprouveraient alors
      un radar non modifié, et passeraient ou tomberaient sans rapport avec ce qu'ils
      annoncent surveiller.
      ③ Le refus, quand il tombe, accuse le mauvais coupable. L'ancre est une ligne du
      radar recopiée caractère pour caractère : une seule espace ajoutée dans le
      radar, sans le moindre changement de comportement, ferait lever ici, et le jeu
      d'épreuves nommerait le cas plutôt que la mise en forme qui a bougé.
      ④ Le fichier temporaire n'est jamais effacé par cette fonction. Les trois
      appelants s'en chargent ; un quatrième cas ajouté demain qui l'oublierait
      laisserait 91 191 octets derrière lui, sans que rien ne le signale.
    ⑩ EFFET — CRÉE un dossier temporaire (les programmes voisins, environ 3 Mo, et
      la copie modifiée) ; il est effacé à la sortie du programme. LIT le radar. N'affiche rien, ne touche pas au réseau, ne modifie aucun
      fichier du dépôt.
    ⑪ TERMINAISON — Rend la main. PEUT LEVER : une erreur d'assertion quand un texte à
      remplacer est absent, et une erreur du système de fichiers quand le radar est
      illisible ou le dossier temporaire plein. Ces erreurs remontent au cas appelant,
      où elles sont rattrapées et transformées en échec. Aucun de ses appels ne se
      termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir,
        qui contrôle l'ensemble du système et range chacun de ses constats sous un
        numéro de maillon, par exemple 18-Tâches pour le contrôle des traces
        laissées par les tâches planifiées.
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré
        rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une copie modifiée du radar : un exemplaire du radar dans lequel un morceau
        de texte a été remplacé, écrit dans le dossier temporaire du système, pour
        éprouver un comportement que le radar ne montre pas tel quel.
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    src = open(SCRIPT, encoding="utf-8").read()
    for a, b in remplacements:
        if src.count(a) < 1:        # pas d assert : il disparait sous python3 -O
            raise ValueError(f"ancre introuvable : {a[:40]}")
        src = src.replace(a, b, 1)
    # LA COPIE EMPORTE SES VOISINS (28-09-2026) : le radar importe COMMUN.py et
    # CONTRATS_DES_FICHIERS.py depuis son propre dossier ; seule dans le dossier
    # temporaire, la copie s arretait sur RuntimeError et trois cas tombaient.
    d = tempfile.mkdtemp(prefix="radar_modifie_")
    _A_EFFACER.append(d)
    ici = os.path.dirname(os.path.abspath(SCRIPT))
    for voisin in os.listdir(ici):
        if voisin.endswith(".py") and voisin != SCRIPT:
            shutil.copy(os.path.join(ici, voisin), d)
    chemin = os.path.join(d, "radar_modifie.py")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(src)
    return chemin


def cas(nom, verifie):
    """Execute un cas. Rend (nom, passe, detail).

    ① RÔLE — Empêcher qu'un cas qui s'effondre arrête le programme entier. Un cas est
      une fonction ordinaire : sans cette protection, la première erreur couperait la
      liste au milieu et les cas suivants ne seraient jamais joués — exactement le
      défaut que le radar portait le 29-08-2026, où un mode de comptage oublié faisait
      disparaître du rapport les tâches déclarées après lui, sans un mot.
    ② CONTEXTE D'APPEL — `main`, une fois par cas, soit onze fois par passage. Jamais
      appelée ailleurs.
    ③ ENTRÉE — `nom` : le libellé affiché du cas, par exemple une trace absente est
      denoncee · `verifie` : la fonction à exécuter, appelée sans argument. Un seul
      appelant, `main`, et il passe une fonction sans nom qui appelle le cas avec le
      dossier d'épreuve reçu sur la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — `verifie` doit pouvoir être appelée sans argument et
      rendre deux valeurs : un verdict vrai ou faux, puis un détail affichable.
    ⑤ SORTIE — TROIS valeurs : le nom reçu, le
      verdict, ce détail. Deux formes selon la branche. Quand le cas s'est déroulé, le
      verdict et ce détail sont ceux qu'il a rendus. Quand le cas a levé, le verdict
      est faux et ce détail est la phrase le cas lui-meme a plante : suivie du type de
      l'erreur et de son message.
      [rend: 3]
    ⑥ TRAITEMENT — ① appeler la fonction reçue · ② si une erreur ordinaire survient,
      rendre un échec portant le type et le message de cette erreur · ③ sinon rendre
      le nom, le verdict et ce détail.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un cas qui s'effondre et un cas qui constate un défaut sont deux
      choses différentes, et ce détail les sépare à l'écran : la mention explicite que
      c'est le CAS qui est tombé évite de chercher le défaut du mauvais côté. Les deux
      comptent pourtant pour un échec, parce qu'un cas qu'on ne peut plus jouer ne
      prouve plus rien.
    ⑨ CE QUI CLOCHE — deux points :
      ① Le nom reçu est rendu tel quel et ne sert jamais. `main` connaît déjà le nom
      qu'il vient de passer et pourrait l'afficher lui-même ; le faire voyager aller
      et retour laisse croire que la fonction pourrait le changer, ce qu'elle ne fait
      dans aucune branche.
      ② Un cas qui rendrait autre chose que deux valeurs serait rangé parmi les cas
      qui ont planté, le dépaquetage échouant à l'intérieur de la protection. Le
      message affiché serait le cas lui-meme a plante : ValueError, ce qui désigne une
      erreur du cas là où il s'agit d'une erreur de forme du résultat. Aucun des onze
      cas ne le produit aujourd'hui : les onze rendent bien deux valeurs.
    ⑩ EFFET — N'écrit aucun fichier, n'affiche rien, ne touche pas au réseau
      elle-même. Ce qu'elle CHANGE vient entièrement du cas qu'elle exécute : dix des
      onze lancent le radar, sept recopient le dépôt entier dans le dossier temporaire
      du système, trois y écrivent une copie du radar.
    ⑪ TERMINAISON — Rend la main pour toutes les erreurs ordinaires. NE RATTRAPE PAS
      une interruption au clavier ni un arrêt demandé par le programme, qui ne font
      pas partie de la famille d'erreurs attrapée ici : ceux-là traversent et arrêtent
      le programme. Et un de ses appels peut ne pas revenir, puisque la fonction reçue
      est quelconque.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir,
        qui contrôle l'ensemble du système et range chacun de ses constats sous un
        numéro de maillon, par exemple 18-Tâches pour le contrôle des traces
        laissées par les tâches planifiées.
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré
        rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle
        a tourné — rapport de boucle, rapport d'audit, cockpit, historique des
        mesures.
    """
    try:
        ok, detail = verifie()
    except Exception as e:
        return nom, False, f"le cas lui-meme a plante : {type(e).__name__} {e}"
    return nom, ok, detail


# ─────────────────────────────────────────────────────────────────────
# LES CAS — un par defaut deja rencontre. On n'en retire jamais.
# ─────────────────────────────────────────────────────────────────────

def _c_sous_dossiers(base):
    """v2.3 — le radar doit voir les fichiers des sous-dossiers.

    ① RÔLE — Rejouer le défaut du 28-08-2026, le plus grave que le radar ait porté :
      il ne regardait que les fichiers posés au premier niveau du projet et ignorait
      ceux des sous-dossiers. Le dossier claude/ portait alors les positions ouvertes,
      le journal des trades, les cours du jour et le rapport d'audit ; le maillon qui
      recalcule chaque trade clôturé passait au VERT en annonçant aucun trade clôturé,
      rien à contrôler. Il ne contrôlait rien et le disait comme un succès.
    ② CONTEXTE D'APPEL — `main`, une seule fois, premier des onze cas, par
      l'intermédiaire de `cas`. Il n'est jamais appelé par son nom : il est inscrit
      dans la liste CAS écrite plus bas dans ce même programme, ce qui le fait
      apparaître sans appelant dans le document archives/PHOTOGRAPHIE_ABANDONNEE_24-09-2026_voir_A-452.md.
    ③ ENTRÉE — `base` : le dossier à faire examiner par le radar. Un seul appelant,
      `main`, et il transmet sans le modifier l'argument reçu sur la ligne de
      commande.
    ④ CONDITIONS D'ENTRÉE — `base` doit exister, et le radar être lançable depuis le
      dossier de travail.
    ⑤ SORTIE — DEUX valeurs : le verdict, vrai quand le radar a rendu, sur le maillon
      des tâches, au moins une ligne par tâche déclarée et que toutes annoncent la date du jour, et un détail affichable donnant le nombre de
      lignes obtenues.
      [rend: 2]
    ⑥ TRAITEMENT — (depuis le 28-09-2026) ① recopier le dossier reçu dans un dossier
      temporaire, et en retirer tout fichier dont le nom porte l'un des motifs des
      tâches · ② y écrire, sous sous/dossier/, une trace datée du jour pour chacune
      des tâches déclarées · ③ lancer le radar sur la copie · ④ rendre vrai si les lignes
      des tâches sont au moins autant que de tâches déclarées dans le radar, nombre lu par `_nb_taches` (trois depuis le 30-09-2026, le cockpit n'étant plus déclaré) et annoncent TOUTES la date du jour.
    ⑦ UNITÉ — Un NOMBRE DE LIGNES, autant que de tâches déclarées dans le radar, nombre lu par `_nb_taches` (trois depuis le 30-09-2026, le cockpit n'étant plus déclaré).
    ⑧ POURQUOI — Le nombre n'est pas choisi : il vient des tâches que le radar déclare
      surveiller — la boucle du jour, l'audit du soir et la mesure de performance ; le
      cockpit l'était jusqu'au 30-09-2026.
    ⑨ CE QUI CLOCHE — RÉGLÉ LE 28-09-2026 (A-435 ②, tests/EPREUVES_DU_JEU_DU_RADAR_Lun_28-09-2026.py) — le cas fabrique, dans une copie, une trace datée du jour par tâche, à deux niveaux de profondeur, exige que le radar annonce cette date pour chacune (quatre alors, trois depuis le 30-09-2026), et tombe quand le radar ne descend plus dans les sous-dossiers (SA10) ; il ne dépend plus des vraies traces du dépôt. Ce qui était mesuré : un point, et il ôte au cas toute valeur de preuve. LE CAS NE
      PEUT PAS ROUGIR QUAND ON LUI RETIRE CE QU'IL SURVEILLE. Mesuré le 19-09-2026 :
      dans une copie du dépôt, la liste de fichiers du radar a été réduite à ceux du
      premier niveau — c'est exactement le défaut du 28-08 — puis ce programme
      relancé. Ce cas est resté VERT, 4 lignes de controle (4 attendues), pendant que
      deux autres cas tombaient. Cela tient à ce que le radar écrit une ligne par
      tâche déclarée DANS TOUS LES CAS : quand la trace est introuvable, il écrit n'a
      laissé AUCUNE trace, qui est encore une ligne. Le cas compte donc des tâches
      déclarées, jamais des fichiers trouvés dans des sous-dossiers. Une épreuve qui
      reste verte quand on retire ce qu'elle teste n'est pas une preuve, c'est une
      décoration (R-731).
    ⑩ EFFET — (depuis le 28-09-2026) CRÉE puis EFFACE une copie complète du dépôt,
      y ÉCRIT trois traces, LANCE le radar sur elle. Ne touche pas au dossier reçu,
      n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main. PEUT LEVER ce que lève le lancement du radar ;
      l'erreur remonte alors à `cas`, qui la transforme en échec de ce cas. Aucun de
      ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir,
        qui contrôle l'ensemble du système et range chacun de ses constats sous un
        numéro de maillon, par exemple 18-Tâches pour le contrôle des traces
        laissées par les tâches planifiées.
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré
        rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle
        a tourné — rapport de boucle, rapport d'audit, cockpit, historique des
        mesures.
      la boucle du jour : la tâche planifiée qui collecte les cours et écrit le
        rapport de boucle, du lundi au vendredi seulement.
    
      l'audit du soir : programmes/audit_ecosysteme.py, lance chaque soir par la tache planifiee, qui ecrit rapports/audit_du_jour.md
      la trace : la liste des sources avec leur etat — LU, ABSENT ou ILLISIBLE — et un detail chiffre, affichee en pied de page.
"""
    # UNE LIGNE PAR TÂCHE NE PROUVE RIEN : le radar en écrit une même quand il ne
    # trouve rien (28-09-2026, A-435 ②). Le cas FABRIQUE donc, dans une copie, une trace
    # datée d'aujourd'hui pour chacune des tâches déclarées, à deux niveaux de profondeur,
    # et exige que le radar annonce cette date pour toutes. Il ne dépend plus des
    # vraies traces du dépôt (relecteur du Chat, tour 2 : sans l'audit du soir réel, la
    # version précédente tombait, radar juste).
    jour = datetime.now(ZoneInfo("Europe/Paris")).date().isoformat()
    with tempfile.TemporaryDirectory() as t:
        d = os.path.join(t, "d")
        shutil.copytree(base, d)
        # LES VRAIES TRACES SONT RETIRÉES DE LA COPIE (relecteur du Chat, tour 3) : le
        # radar retient la date la plus récente ; le soir, les vraies traces portent
        # aussi la date du jour, et un radar qui ne descendrait qu'à un niveau les
        # aurait vues à la place des traces fabriquées.
        motifs = ("rapport_boucle", "cours_nouveaux", "audit_du_jour", "historique_mesures")
        for rac, _sd, fs in os.walk(d):
            for x in fs:
                if any(m in x.lower() for m in motifs):
                    os.remove(os.path.join(rac, x))
        prof = os.path.join(d, "sous", "dossier")
        os.makedirs(prof)
        for nom, texte in ((f"claude_rapport_boucle_{jour}.md", f"# boucle {jour}\n"),
                           (f"audit_du_jour_{jour}.md", f"# audit {jour}\n"),
                           ("historique_mesures.csv", f"date_mesure,valeur\n{jour},1\n")):
            with open(os.path.join(prof, nom), "w", encoding="utf-8") as f:
                f.write(texte)
        l = _lignes18(d)
    vues = [x for x in l if f"DÉCLARÉE {jour}" in x]
    manquent = [x.split("] ")[-1][:40] for x in l if f"DÉCLARÉE {jour}" not in x]
    n = _nb_taches()
    return len(l) >= n and len(vues) == len(l), (
        f"{len(vues)} trace(s) fabriquée(s) vue(s) sur {len(l)} ({n} attendues)"
        + (f" · non vues : {manquent}" if manquent else ""))


def _c_recopie(base):
    """v2.4 — LE PLUS IMPORTANT. Une trace vieille RECOPIEE A NEUF doit garder
    son age. C'etait un faux vert structurel : en production le maillon aurait
    ete au vert quoi qu'il arrive, la tache recopiant tout le projet avant de
    lancer.

    ① RÔLE — Rejouer le défaut du 28-08-2026 au soir : le radar lisait l'âge d'une
      trace sur la date que le système de fichiers donne au fichier, et non sur celle
      que le fichier déclare. Or la tâche du soir commençait par recopier tout le
      projet en local, et chaque fichier arrivait avec la date du téléchargement : le
      contrôle des traces aurait été au vert quoi qu'il arrive. Mesuré par contraste à
      l'époque : un rapport du 20-08 portait une date de fichier du 23, puis du 28
      après recopie.
    ② CONTEXTE D'APPEL — `main`, une seule fois, deuxième des onze cas, par
      l'intermédiaire de `cas`. Inscrit dans la liste CAS écrite plus bas dans ce même
      programme, jamais appelé par son nom.
    ③ ENTRÉE — `base` : le dossier à recopier puis à faire examiner. Un seul appelant,
      `main`, qui transmet sans le modifier l'argument reçu sur la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — `base` doit exister. Le dossier temporaire du système doit
      pouvoir porter DEUX copies complètes du dépôt en même temps : une copie pèse 12
      Mo pour 243 fichiers, mesuré le 19-09-2026.
    ⑤ SORTIE — DEUX valeurs : le verdict et un détail affichable. Trois formes de
      détail — la ligne de l'audit du soir est absente quand le radar n'a rien dit de
      cette tâche, age illisible quand la ligne ne porte aucun nombre de jours, et
      sinon les deux âges relevés suivis de doivent etre EGAUX.
      [rend: 2]
    ⑥ TRAITEMENT — ① recopier le dépôt dans un premier dossier temporaire · ② y forcer
      la date déclarée des fichiers dont le nom porte audit_du_jour ·
      ③ relever l'âge annoncé par le radar sur la ligne de l'audit du soir ·
      ④ recopier ce premier dossier dans un second · ⑤ y relever le même âge ·
      ⑥ rendre vrai si les deux nombres sont égaux · ⑦ effacer les deux copies.
    ⑦ UNITÉ — Un ÂGE EN JOURS, lu dans le texte du radar juste avant le mot jour.
    ⑧ POURQUOI — Le cas compare une copie à sa copie plutôt qu'à un nombre attendu,
      parce que la propriété qui compte est recopier ne doit pas rajeunir, et qu'un
      garde-fou porte sur une propriété, jamais sur un nombre écrit en dur (R-721).
    ⑨ CE QUI CLOCHE — trois points, tous mesurés le 19-09-2026, et ensemble ils vident
      le cas de sa preuve alors que son propre texte le dit LE PLUS IMPORTANT :
      RÉGLÉ LE 28-09-2026 (A-435 ②, tests/EPREUVES_DU_JEU_DU_RADAR_Lun_28-09-2026.py) — le cas vieillit la trace sur le disque avant la recopie et la rajeunit après ; il tombe quand le radar lit la date du disque (SA6). Ce qui était mesuré :
      ① LA RECOPIE NE RAJEUNIT PAS LES FICHIERS, contrairement à ce que le commentaire
      du code annonce. L'outil de recopie employé conserve la date des fichiers.
      Mesuré : un dossier recopié une fois, puis la copie recopiée à son tour, rendent
      tous trois la même date à la microseconde près — 2026-09-19 21:51:15.002461. La
      situation que le cas veut fabriquer n'est donc jamais fabriquée.
      ② LE CAS NE PEUT PAS ROUGIR. Mesuré : dans une copie du dépôt, le radar a été
      forcé à lire l'âge sur la date du fichier, ce qui est exactement le défaut du
      28-08, puis ce programme relancé. Ce cas est resté VERT, avant recopie 0 j,
      apres 0 j. Les deux copies portant la même date, l'égalité est vraie quelle que
      soit la façon de lire l'âge. Une épreuve qui reste verte quand on retire ce
      qu'elle teste n'est pas une preuve, c'est une décoration (R-731).
      ③ LE VIEILLISSEMENT N'A PAS LIEU NON PLUS. La fonction qui force la date ne
      reconnaît que la forme année-mois-jour, alors que le rapport d'audit écrit la
      sienne jour-mois-année : # AUDIT ÉCOSYSTÈME CAC 40 — Jeu 17-09-2026 23h56
      (Paris). Mesuré : après le forçage au 2026-08-11, le radar annonce toujours
      dernière trace datée 2026-09-17.
    ⑩ EFFET — CRÉE puis EFFACE deux copies complètes du dépôt dans le dossier
      temporaire du système, 24 Mo au plus fort. RÉÉCRIT dans la première copie les
      fichiers dont le nom porte audit_du_jour — un seul au dépôt du 19-09-2026,
      rapports/audit_du_jour.md. LANCE le radar deux fois. NE TOUCHE PAS au dossier
      reçu. Aucun accès réseau.
    ⑪ TERMINAISON — Rend la main. Les copies sont effacées même en cas d'erreur, le
      dossier temporaire étant refermé automatiquement. PEUT LEVER quand le disque est
      plein ou quand la recopie échoue ; l'erreur remonte à `cas`, qui la transforme
      en échec de ce cas. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir,
        qui contrôle l'ensemble du système et range chacun de ses constats sous un
        numéro de maillon, par exemple 18-Tâches pour le contrôle des traces
        laissées par les tâches planifiées.
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré
        rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle
        a tourné — rapport de boucle, rapport d'audit, cockpit, historique des
        mesures.
      la date déclarée : la date qu'un fichier porte dans son nom ou dans son
        contenu, par opposition à celle que le système de fichiers lui donne.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
    
      PRODUCTION : l etat d une strategie dont le seuil d operations est atteint et les resultats conformes, donc exploitee.
      l'audit du soir : programmes/audit_ecosysteme.py, lance chaque soir par la tache planifiee, qui ecrit rapports/audit_du_jour.md
"""
    with tempfile.TemporaryDirectory() as t:
        a = os.path.join(t, "a")
        shutil.copytree(base, a)
        # LA TRACE EST FABRIQUÉE (28-09-2026) : le cas ne dépend plus de la vraie trace
        # de l'audit du soir, absente le soir précis où le circuit est cassé (A-441).
        with open(os.path.join(a, "rapports", "audit_du_jour.md"), "w", encoding="utf-8") as f:
            f.write("# AUDIT ÉCOSYSTÈME CAC 40 — Mar 11-08-2026 21h00 (Paris)\n")
        _dater(a, "audit_du_jour", "2026-08-11")
        # LA DATE DU DISQUE DOIT MENTIR, sinon le cas ne prouve rien (28-09-2026, A-435 ②).
        # shutil.copytree CONSERVE les dates de modification : la « recopie » ne les
        # rajeunissait pas, et un radar qui aurait lu la date du disque passait. On
        # vieillit donc la trace sur le disque avant, et on la rajeunit après la recopie.
        _vieux = time.mktime((2026, 8, 11, 12, 0, 0, 0, 0, -1))
        for _p in glob.glob(a + "/**/*audit_du_jour*", recursive=True):
            os.utime(_p, (_vieux, _vieux))
        av = [x for x in _lignes18(a) if "audit du soir" in x]
        b = os.path.join(t, "b")
        shutil.copytree(a, b)
        for _p in glob.glob(b + "/**/*audit_du_jour*", recursive=True):
            os.utime(_p, None)         # recopie : la date du disque devient celle d'aujourd'hui
        ap = [x for x in _lignes18(b) if "audit du soir" in x]
        if not av or not ap:
            return False, "la ligne de l'audit du soir est absente"
        na = re.search(r"(\d+) jour", av[0])
        nb = re.search(r"(\d+) jour", ap[0])
        if not na or not nb:
            return False, "age illisible"
        return na.group(1) == nb.group(1), (
            f"avant recopie {na.group(1)} j, apres {nb.group(1)} j "
            f"— doivent etre EGAUX")


def _c_tableau_empile(base):
    """v2.5 — un tableau qui s'empile porte sa date en DERNIERE ligne.

    ① RÔLE — Rejouer le défaut du 29-08-2026 sur les fichiers qui s'empilent.
      L'historique des mesures ajoute une ligne par jour et n'est jamais réécrit :
      lire ses premières lignes rendait toujours sa plus ancienne date, et l'écart
      annoncé par le radar grandissait d'un jour chaque jour — une alerte permanente
      sur une tâche qui fonctionne, et une alerte qu'on apprend à ignorer cesse de
      protéger. La date d'un tel fichier vit en DERNIÈRE ligne.
    ② CONTEXTE D'APPEL — `main`, une seule fois, troisième des onze cas, par
      l'intermédiaire de `cas`. Inscrit dans la liste CAS écrite plus bas dans ce même
      programme, jamais appelé par son nom.
    ③ ENTRÉE — `base` : le dossier à recopier puis à faire examiner. Un seul appelant,
      `main`, qui transmet sans le modifier l'argument reçu sur la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — `base` doit exister, et le dossier temporaire du système
      pouvoir porter une copie complète du dépôt : 12 Mo pour 243 fichiers, mesuré le
      19-09-2026.
    ⑤ SORTIE — DEUX valeurs : le verdict et un détail affichable. Deux formes — ligne
      absente quand le radar n'a rien dit de la mesure de performance, sinon les
      trente derniers caractères de la ligne lue suivis de la date attendue.
      [rend: 2]
    ⑥ TRAITEMENT — ① recopier le dépôt dans un dossier temporaire · ② y écrire à la
      racine un fichier historique_mesures.csv de deux lignes de données, la plus
      ancienne datée du 2026-01-15 et la plus récente du 2026-08-27 · ③ lancer le
      radar · ④ ne garder que la ligne parlant de la performance · ⑤ rendre vrai si
      elle porte la date de la DERNIÈRE ligne du fichier · ⑥ effacer la copie.
    ⑦ UNITÉ — Une DATE de calendrier.
    ⑧ POURQUOI — Les deux dates du fichier fabriqué sont volontairement dans l'ordre
      croissant et éloignées de sept mois : si le radar lisait la première ligne, il
      annoncerait le 2026-01-15, et l'écart avec la date attendue serait trop grand
      pour passer inaperçu.
    ⑨ CE QUI CLOCHE — un point, mesuré le 19-09-2026, RÉGLÉ LE 28-09-2026 : le fichier
      fabriqué remplace désormais le vrai, dans donnees/, et le cas passe ; il tombe
      quand le radar lit un tableau comme un document (épreuve SA1). Ce qui était mesuré : Le fichier fabriqué est écrit au PREMIER NIVEAU de la copie, alors
      que le vrai vit dans donnees/. Le radar descend dans les sous-dossiers depuis le
      28-08-2026 : il trouve donc DEUX fichiers nommés historique_mesures.csv et
      retient la plus récente de leurs dates. Le vrai fichier du dépôt étant daté du
      2026-09-17, il l'emporte sur le 2026-08-27 fabriqué. Sortie mesurée le
      19-09-2026 à 21h50 : ECHEC un tableau qui s'empile : DERNIERE ligne — lu : (s) —
      date DÉCLARÉE 2026-09-17 (2026-08-27 attendu). La fin de ligne citée change avec
      les jours, puisque le radar passe du succès à l'alerte quand la trace dépasse
      deux jours ; ce qui ne change pas est la date retenue, celle du vrai fichier et
      non celle du fichier fabriqué. Le cas est rouge sans qu'aucun défaut du radar ne
      soit en cause, et ce programme conclut pourtant NE RIEN DEPOSER. Le cas n'a donc
      pas pu être éprouvé contre sa propre correction : personne ne sait s'il sait
      rougir pour la bonne raison.
    ⑩ EFFET — CRÉE puis EFFACE une copie complète du dépôt dans le dossier temporaire
      du système. ÉCRIT le fichier donnees/historique_mesures.csv de cette copie, à
      la place du vrai. LANCE le radar une fois. NE TOUCHE PAS au dossier reçu. Aucun accès
      réseau.
    ⑪ TERMINAISON — Rend la main. La copie est effacée même en cas d'erreur, le
      dossier temporaire étant refermé automatiquement. PEUT LEVER quand le disque est
      plein ou quand la recopie échoue ; l'erreur remonte à `cas`, qui la transforme
      en échec de ce cas. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir,
        qui contrôle l'ensemble du système et range chacun de ses constats sous un
        numéro de maillon, par exemple 18-Tâches pour le contrôle des traces
        laissées par les tâches planifiées.
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré
        rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle
        a tourné — rapport de boucle, rapport d'audit, cockpit, historique des
        mesures.
      la date déclarée : la date qu'un fichier porte dans son nom ou dans son
        contenu, par opposition à celle que le système de fichiers lui donne.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
    
      la trace : la liste des sources avec leur etat — LU, ABSENT ou ILLISIBLE — et un detail chiffre, affichee en pied de page.
"""
    with tempfile.TemporaryDirectory() as t:
        d = os.path.join(t, "d")
        shutil.copytree(base, d)
        # LE FICHIER FABRIQUÉ REMPLACE LE VRAI, DANS donnees/ (28-09-2026, A-435 ②) :
        # écrit au premier niveau, il côtoyait le vrai, et le radar retenait le vrai.
        p = os.path.join(d, "donnees", "historique_mesures.csv")
        with open(p, "w", encoding="utf-8") as f:
            f.write("date_mesure,valeur\n2026-01-15,1\n2026-08-27,2\n")
        l = [x for x in _lignes18(d) if "performance" in x]
        if not l:
            return False, "ligne absente"
        return "2026-08-27" in l[0], f"lu : {l[0][-30:]} (2026-08-27 attendu)"


def _c_document_redige(base):
    """v2.5 — un document redige porte sa date en TETE, et cite des dizaines
    d'autres dates dans son corps. Les prendre toutes rendait n'importe laquelle.

    ① RÔLE — Rejouer le douzième défaut de la série, trouvé le 29-08-2026 par ce jeu
      d'épreuves lui-même, et le premier à avoir été attrapé AVANT livraison plutôt
      qu'après. Un rapport d'audit déclare sa date en première ligne puis cite des
      dizaines d'autres dates dans son corps, puisqu'il parle de tous les fichiers du
      projet. Le radar prenait la plus récente des dates trouvées dans les quatre
      premières lignes : un document daté du 11-08 était lu comme du 28-08. La faute
      était invisible sur les fichiers réels, où l'en-tête est seul dans ces quatre
      lignes.
    ② CONTEXTE D'APPEL — `main`, une seule fois, quatrième des onze cas, par
      l'intermédiaire de `cas`. Inscrit dans la liste CAS écrite plus bas dans ce même
      programme, jamais appelé par son nom.
    ③ ENTRÉE — `base` : le dossier à recopier puis à faire examiner. Un seul appelant,
      `main`, qui transmet sans le modifier l'argument reçu sur la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — `base` doit exister et porter au moins un fichier dont le
      nom contient audit_du_jour ; le dossier temporaire du système doit pouvoir
      porter une copie complète du dépôt, 12 Mo pour 243 fichiers mesurés le
      19-09-2026.
    ⑤ SORTIE — DEUX valeurs : le verdict et un détail affichable. Deux formes — ligne
      absente quand le radar n'a rien dit de l'audit du soir, sinon les trente
      derniers caractères de la ligne lue suivis de la date attendue.
      [rend: 2]
    ⑥ TRAITEMENT — ① recopier le dépôt dans un dossier temporaire · ② y remplacer
      chaque fichier dont le nom porte audit_du_jour par trois lignes : un titre daté
      du 2026-08-11, une ligne vide, puis un corps citant le 2026-08-28 et le
      2026-08-27 · ③ lancer le radar · ④ ne garder que la ligne parlant de l'audit du
      soir · ⑤ rendre vrai si elle porte la date de l'EN-TÊTE · ⑥ effacer la copie.
    ⑦ UNITÉ — Une DATE de calendrier.
    ⑧ POURQUOI — Le corps fabriqué cite des dates POSTÉRIEURES à celle de l'en-tête,
      et dans les quatre premières lignes : c'est la seule forme qui sépare prendre la
      première de prendre la plus récente. Un corps citant des dates plus anciennes
      laisserait les deux façons de lire donner le même résultat, et le cas serait
      vert dans les deux mondes.
    ⑨ CE QUI CLOCHE — un point, et il ne porte pas sur la valeur de preuve du cas. LE
      CAS SAIT ROUGIR : mesuré le 19-09-2026, dans une copie du dépôt le radar a été
      forcé à prendre la date la plus récente au lieu de la première, et ce cas est
      devenu ROUGE. Ce qui cloche est ce détail affiché : il ne montre que les trente
      derniers caractères de la ligne lue, soit re (cas des boucles du 28/08). — un
      fragment de la phrase d'alerte du radar qui ne porte aucune date. Le verdict est
      juste, ce détail n'apprend rien à qui lit la sortie.
    ⑩ EFFET — CRÉE puis EFFACE une copie complète du dépôt dans le dossier temporaire
      du système. ÉCRASE dans cette copie tous les fichiers dont le nom porte
      audit_du_jour — un seul au dépôt du 19-09-2026, rapports/audit_du_jour.md. LANCE
      le radar une fois. NE TOUCHE PAS au dossier reçu. Aucun accès réseau.
    ⑪ TERMINAISON — Rend la main. La copie est effacée même en cas d'erreur, le
      dossier temporaire étant refermé automatiquement. PEUT LEVER quand le disque est
      plein ou quand la recopie échoue ; l'erreur remonte à `cas`, qui la transforme
      en échec de ce cas. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir,
        qui contrôle l'ensemble du système et range chacun de ses constats sous un
        numéro de maillon, par exemple 18-Tâches pour le contrôle des traces
        laissées par les tâches planifiées.
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré
        rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle
        a tourné — rapport de boucle, rapport d'audit, cockpit, historique des
        mesures.
      la date déclarée : la date qu'un fichier porte dans son nom ou dans son
        contenu, par opposition à celle que le système de fichiers lui donne.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
    
      l'audit du soir : programmes/audit_ecosysteme.py, lance chaque soir par la tache planifiee, qui ecrit rapports/audit_du_jour.md
"""
    with tempfile.TemporaryDirectory() as t:
        d = os.path.join(t, "d")
        shutil.copytree(base, d)
        # la trace est posée même si le dépôt n'en a pas (28-09-2026, relecteur du Chat)
        cibles = set(glob.glob(d + "/**/*audit_du_jour*", recursive=True))
        cibles.add(os.path.join(d, "rapports", "audit_du_jour.md"))
        for p in cibles:
            with open(p, "w", encoding="utf-8") as f:
                f.write("# AUDIT DU JOUR — 2026-08-11\n\ntexte citant 2026-08-28 "
                        "et 2026-08-27 dans son corps\n")
        l = [x for x in _lignes18(d) if "audit du soir" in x]
        if not l:
            return False, "ligne absente"
        return "2026-08-11" in l[0], f"lu : {l[0][-30:]} (2026-08-11 attendu)"


def _c_date_future(base):
    """v2.5 — une echeance n'est pas une trace.

    ① RÔLE — Vérifier qu'une date postérieure à aujourd'hui n'est jamais prise pour la
      trace d'une tâche. Un fichier peut porter une échéance ou une coquille : retenue
      comme trace, elle ferait croire que la tâche vient de tourner, et le radar se
      tairait sur une tâche arrêtée. C'est le silence, et non l'erreur, qui est le
      danger de ce programme.
    ② CONTEXTE D'APPEL — `main`, une seule fois, cinquième des onze cas, par
      l'intermédiaire de `cas`. Inscrit dans la liste CAS écrite plus bas dans ce même
      programme, jamais appelé par son nom.
    ③ ENTRÉE — `base` : le dossier à recopier puis à faire examiner. Un seul appelant,
      `main`, qui transmet sans le modifier l'argument reçu sur la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — `base` doit exister, et le dossier temporaire du système
      pouvoir porter une copie complète du dépôt : 12 Mo pour 243 fichiers, mesuré le
      19-09-2026.
    ⑤ SORTIE — DEUX valeurs : le verdict et un détail affichable. Deux formes — ligne
      absente quand le radar n'a rien dit de la mesure de performance, sinon les
      trente derniers caractères de la ligne lue suivis du rappel que 2099 ne doit pas
      y figurer.
      [rend: 2]
    ⑥ TRAITEMENT — ① recopier le dépôt dans un dossier temporaire · ② y écrire à la
      racine un fichier historique_mesures.csv de deux lignes de données, l'une datée
      du 2026-08-27, l'autre du 2099-12-31 · ③ lancer le radar · ④ ne garder que la
      ligne parlant de la performance · ⑤ rendre vrai si l'année 2099 n'y apparaît pas
      · ⑥ effacer la copie.
    ⑦ UNITÉ — Une DATE de calendrier. L'année 2099 n'a pas d'autre rôle que d'être
      hors d'atteinte : n'importe quelle date future ferait le même office.
    ⑧ POURQUOI — Le cas cherche l'ABSENCE d'un texte plutôt que la présence d'une date
      précise, parce que la propriété qui compte est qu'aucune date future ne
      ressorte, quelle qu'elle soit.
    ⑨ CE QUI CLOCHE — deux points, mesurés le 19-09-2026 ; le ① RÉGLÉ LE 28-09-2026 :
      le fichier fabriqué remplace le vrai, dans donnees/ (épreuve SA5 de
      tests/EPREUVES_DU_JEU_DU_RADAR). Ce qui était mesuré :
      ① Le cas est VERT aujourd'hui pour une raison qui n'est pas la sienne, et il le
      serait même si le fichier fabriqué n'existait pas. Ce fichier est écrit au
      PREMIER NIVEAU de la copie alors que le vrai vit dans donnees/ : le radar en
      voit deux et garde la date la plus récente qui ne soit pas future, soit le
      2026-09-17 du vrai fichier. Sortie mesurée le 19-09-2026 à 21h50 : lu : (s) —
      date DÉCLARÉE 2026-09-17. Le cas vérifie donc surtout que le vrai fichier du
      dépôt n'est pas daté de 2099.
      ② Malgré cela, LE CAS SAIT ROUGIR. Mesuré : dans une copie du dépôt, le filtre
      des dates futures a été retiré du radar, et le cas est devenu ROUGE, date
      DÉCLARÉE 2099-12-31. C'est ce qui le sépare de deux cas du même programme qui,
      eux, restent verts sous le retrait de ce qu'ils surveillent.
    ⑩ EFFET — CRÉE puis EFFACE une copie complète du dépôt dans le dossier temporaire
      du système. ÉCRIT le fichier donnees/historique_mesures.csv de cette copie, à
      la place du vrai. LANCE le radar une fois. NE TOUCHE PAS au dossier reçu. Aucun accès
      réseau.
    ⑪ TERMINAISON — Rend la main. La copie est effacée même en cas d'erreur, le
      dossier temporaire étant refermé automatiquement. PEUT LEVER quand le disque est
      plein ou quand la recopie échoue ; l'erreur remonte à `cas`, qui la transforme
      en échec de ce cas. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir,
        qui contrôle l'ensemble du système et range chacun de ses constats sous un
        numéro de maillon, par exemple 18-Tâches pour le contrôle des traces
        laissées par les tâches planifiées.
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré
        rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle
        a tourné — rapport de boucle, rapport d'audit, cockpit, historique des
        mesures.
      la date déclarée : la date qu'un fichier porte dans son nom ou dans son
        contenu, par opposition à celle que le système de fichiers lui donne.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
    """
    with tempfile.TemporaryDirectory() as t:
        d = os.path.join(t, "d")
        shutil.copytree(base, d)
        # dans donnees/, à la place du vrai (28-09-2026, A-435 ② : écrit au premier
        # niveau, il côtoyait le vrai ; le cas avait pourtant déjà ses dents, par le filtre
        # des dates futures — mesure du relecteur du Chat. Le changement est d'uniformité.)
        p = os.path.join(d, "donnees", "historique_mesures.csv")
        with open(p, "w", encoding="utf-8") as f:
            f.write("date_mesure,valeur\n2026-08-27,1\n2099-12-31,2\n")
        l = [x for x in _lignes18(d) if "performance" in x]
        if not l:
            return False, "ligne absente"
        return "2099" not in l[0], f"lu : {l[0][-30:]} (2099 ne doit PAS sortir)"


def _c_weekend(base):
    """v2.6 et v2.7 — la boucle ne tourne pas le week-end, l'audit si.
    Le dimanche : la boucle SILENCIEUSE, l'audit DENONCE.

    ① RÔLE — Rejouer deux défauts jumeaux du 29-08-2026. La boucle du jour a un
      calendrier du lundi au vendredi, l'audit du soir tourne sept jours sur sept.
      Compter l'âge des traces en jours de calendrier pour tout le monde faisait crier
      le radar chaque dimanche et chaque lundi matin sur une boucle qui fonctionne ;
      compter en jours ouvrés pour tout le monde aurait laissé un audit mort le
      vendredi soir passer inaperçu jusqu'au mardi — quatre jours d'aveuglement sur la
      tâche qui EST le radar.
    ② CONTEXTE D'APPEL — `main`, une seule fois, sixième des onze cas, par
      l'intermédiaire de `cas`. Inscrit dans la liste CAS écrite plus bas dans ce même
      programme, jamais appelé par son nom.
    ③ ENTRÉE — `base` : le dossier à recopier puis à faire examiner. Un seul appelant,
      `main`, qui transmet sans le modifier l'argument reçu sur la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — `base` doit exister. Le dossier temporaire du système doit
      pouvoir porter une copie complète du dépôt, 12 Mo pour 243 fichiers, et une
      copie du radar de 91 191 octets. Le texte remplacé dans le radar doit y figurer
      : mesuré le 19-09-2026, il y figure exactement une fois.
    ⑤ SORTIE — DEUX valeurs : le verdict et un détail affichable. Deux formes — lignes
      absentes quand le radar n'a rien dit de la boucle ou de l'audit, sinon une
      phrase qui nomme séparément le verdict rendu sur chacune des deux tâches.
      [rend: 2]
    ⑥ TRAITEMENT — ① recopier le dépôt dans un dossier temporaire · ② y forcer au
      vendredi 2026-08-28 la date déclarée des traces de la boucle, des cours du jour
      et de l'audit · ③ fabriquer une copie du radar où le jour courant est remplacé
      par le dimanche 30-08-2026 · ④ lancer cette copie sur le dossier recopié · ⑤
      relever la ligne de la boucle et celle de l'audit · ⑥ rendre vrai si la première
      est un succès et la seconde une alerte · ⑦ effacer la copie du radar, même en
      cas d'erreur.
    ⑦ UNITÉ — Une DATE de calendrier pour le jour simulé, et deux SIGNES en tête de
      ligne pour le verdict : celui du succès sur la boucle, celui de l'alerte sur
      l'audit.
    ⑧ POURQUOI — Le cas éprouve les DEUX tâches dans le même passage, parce que le
      défaut de 2026 n'était pas dans l'une ou dans l'autre mais dans l'idée qu'un
      seul mode de comptage vaudrait pour toutes. Vérifier une seule tâche laisserait
      passer le correctif appliqué partout, qui est justement celui qui avait été
      livré.
    ⑨ CE QUI CLOCHE — trois points, tous mesurés le 19-09-2026, ET LE CAS TOMBE
      AUJOURD'HUI :
      ① La copie modifiée du radar ne démarre plus. Écrite dans le dossier temporaire
      du système, elle n'y trouve pas programmes/COMMUN.py, dont le radar dépend
      depuis le 12-09-2026, et s'arrête sur RuntimeError: COMMUN.le_plus_recent
      introuvable. Le radar n'affiche alors rien du tout, et le cas rend lignes
      absentes. Le défaut est dans la fabrication de la copie, pas dans le radar.
      ② Le forçage des dates ne prend pas sur le rapport d'audit. La fonction employée
      ne reconnaît que la forme année-mois-jour, quand le rapport écrit la sienne
      jour-mois-année : # AUDIT ÉCOSYSTÈME CAC 40 — Jeu 17-09-2026 23h56 (Paris). La
      trace de l'audit garde donc sa vraie date, et la situation que le cas veut
      fabriquer n'est fabriquée qu'à moitié.
      ③ Tant que la copie du radar ne démarre pas, le cas ne peut pas être éprouvé
      contre sa propre correction : personne ne sait aujourd'hui s'il saurait rougir.
      Une épreuve qui reste verte quand on retire ce qu'elle teste n'est pas une
      preuve, c'est une décoration (R-731) — et une épreuve qu'on ne peut pas jouer
      n'en est pas une non plus.
    ⑩ EFFET — CRÉE puis EFFACE une copie complète du dépôt dans le dossier temporaire
      du système, et une copie du radar de 91 191 octets. RÉÉCRIT dans la copie du
      dépôt les fichiers dont le nom porte rapport_boucle, cours_nouveaux ou
      audit_du_jour. LANCE la copie du radar une fois. NE TOUCHE PAS au dossier reçu.
      Aucun accès réseau.
    ⑪ TERMINAISON — Rend la main. La copie du radar est effacée même en cas d'erreur,
      par une clause finale ; la copie du dépôt l'est par la fermeture automatique du
      dossier temporaire. PEUT LEVER quand le texte à remplacer est absent du radar,
      quand le disque est plein ou quand la recopie échoue ; l'erreur remonte à `cas`,
      qui la transforme en échec de ce cas. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir,
        qui contrôle l'ensemble du système et range chacun de ses constats sous un
        numéro de maillon, par exemple 18-Tâches pour le contrôle des traces
        laissées par les tâches planifiées.
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré
        rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une copie modifiée du radar : un exemplaire du radar dans lequel un morceau
        de texte a été remplacé, écrit dans le dossier temporaire du système, pour
        éprouver un comportement que le radar ne montre pas tel quel.
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle
        a tourné — rapport de boucle, rapport d'audit, cockpit, historique des
        mesures.
      la date déclarée : la date qu'un fichier porte dans son nom ou dans son
        contenu, par opposition à celle que le système de fichiers lui donne.
      la boucle du jour : la tâche planifiée qui collecte les cours et écrit le
        rapport de boucle, du lundi au vendredi seulement.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
    
      l'audit du soir : programmes/audit_ecosysteme.py, lance chaque soir par la tache planifiee, qui ecrit rapports/audit_du_jour.md
"""
    with tempfile.TemporaryDirectory() as t:
        d = os.path.join(t, "d")
        shutil.copytree(base, d)
        for m in ("rapport_boucle", "cours_nouveaux", "audit_du_jour"):
            _dater(d, m, "2026-08-28")          # vendredi
        v = _variante([('_aujourdhui = datetime.now(ZoneInfo("Europe/Paris")).date()',
                        '_aujourdhui = _dt(2026, 8, 30).date()')])   # dimanche
        try:
            l = _lignes18(d, v)
            b = [x for x in l if "boucle" in x]
            a = [x for x in l if "audit du soir" in x]
            if not b or not a:
                return False, "lignes absentes"
            ok = b[0].startswith("✅") and a[0].startswith("⚠️")
            return ok, ("dimanche : boucle "
                        + ("silencieuse" if b[0].startswith("✅") else "DENONCEE A TORT")
                        + ", audit "
                        + ("denonce" if a[0].startswith("⚠️") else "MUET A TORT"))
        finally:
            os.unlink(v)


def _c_mode_inconnu(base):
    """v2.8 — un mode mal orthographie ne doit pas retomber en silence sur le
    calendaire tout en affichant l'autre etiquette.

    ① RÔLE — Rejouer le défaut du 29-08-2026 : avec le mot ouvre écrit au lieu de
      ouvré, le radar retombait en silence sur le comptage en jours de calendrier tout
      en affichant l'étiquette ouvre. Le rapport disait une chose et calculait
      l'autre, et une seule lettre suffisait. Le radar doit désormais refuser tout
      mode qu'il ne connaît pas, et le dire.
    ② CONTEXTE D'APPEL — `main`, une seule fois, septième des onze cas, par
      l'intermédiaire de `cas`. Inscrit dans la liste CAS écrite plus bas dans ce même
      programme, jamais appelé par son nom.
    ③ ENTRÉE — `base` : le dossier à faire examiner. Un seul appelant, `main`, qui
      transmet sans le modifier l'argument reçu sur la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — `base` doit exister. Le texte remplacé dans le radar doit
      y figurer : mesuré le 19-09-2026, la suite 1, "ouvré" y figure exactement une
      fois. Le dossier temporaire du système doit pouvoir porter une copie du radar,
      91 191 octets.
    ⑤ SORTIE — DEUX valeurs : le verdict et un détail affichable. Deux formes — ligne
      absente quand le radar n'a rien dit de la boucle, sinon le nombre de lignes
      obtenues suivi de oui ou de NON selon que le mode a été dénoncé.
      [rend: 2]
    ⑥ TRAITEMENT — ① fabriquer une copie du radar où la déclaration de la boucle porte
      ouvre au lieu de ouvré · ② lancer cette copie sur le dossier reçu, SANS recopie
      préalable · ③ relever la ligne de la boucle · ④ rendre vrai si elle contient le
      mot INCONNU et si le radar a rendu au moins une ligne par tâche déclarée ·
      ⑤ effacer la copie du radar, même en cas d'erreur.
    ⑦ UNITÉ — Un NOMBRE DE LIGNES, autant que de tâches déclarées dans le radar, nombre lu par `_nb_taches` (trois depuis le 30-09-2026, le cockpit n'étant plus déclaré).
    ⑧ POURQUOI — Le cas exige DEUX choses à la fois : que le mode inconnu soit
      dénoncé, et que toutes les tâches restent contrôlées. Dénoncer en coupant la
      boucle ferait disparaître du rapport les tâches déclarées ensuite, ce qui est
      exactement le second défaut du même jour, surveillé par le cas voisin. Un
      correctif juste pour un cas est presque toujours faux pour le cas voisin : c'est
      la famille de défaut qui a fait naître ce programme (A-308).
    ⑨ CE QUI CLOCHE — deux points, mesurés le 19-09-2026, ET LE CAS TOMBE AUJOURD'HUI
      :
      ① La copie modifiée du radar ne démarre plus. Écrite dans le dossier temporaire
      du système, elle n'y trouve pas programmes/COMMUN.py, dont le radar dépend
      depuis le 12-09-2026, et s'arrête sur RuntimeError: COMMUN.le_plus_recent
      introuvable. Le radar n'affiche rien, et le cas rend ligne absente. Tant qu'il
      ne démarre pas, personne ne sait si ce cas saurait rougir.
      ② Le cas lance une copie MODIFIÉE du radar directement sur le dossier reçu, sans
      le recopier au préalable, alors que sept des onze cas prennent cette précaution.
      Vérifié le 19-09-2026 : aucun des 243 fichiers d'une copie du dépôt n'a été
      modifié par un passage complet. Mais rien dans le cas ne l'empêche, et le radar
      lancé crée au besoin un dossier rapports/ là où on le fait travailler.
    ⑩ EFFET — CRÉE puis EFFACE une copie du radar de 91 191 octets dans le dossier
      temporaire du système. LANCE cette copie une fois, sur le dossier reçu. N'écrit
      aucun fichier dans ce dossier, vérifié par somme de contrôle des 243 fichiers
      d'une copie du dépôt avant et après un passage complet. Aucun accès réseau.
    ⑪ TERMINAISON — Rend la main. La copie du radar est effacée même en cas d'erreur,
      par une clause finale. PEUT LEVER quand le texte à remplacer est absent du radar
      ; l'erreur remonte à `cas`, qui la transforme en échec de ce cas. Aucun de ses
      appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir,
        qui contrôle l'ensemble du système et range chacun de ses constats sous un
        numéro de maillon, par exemple 18-Tâches pour le contrôle des traces
        laissées par les tâches planifiées.
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré
        rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une copie modifiée du radar : un exemplaire du radar dans lequel un morceau
        de texte a été remplacé, écrit dans le dossier temporaire du système, pour
        éprouver un comportement que le radar ne montre pas tel quel.
      la boucle du jour : la tâche planifiée qui collecte les cours et écrit le
        rapport de boucle, du lundi au vendredi seulement.
    """
    v = _variante([('1, "ouvré"', '1, "ouvre"')])
    try:
        l = _lignes18(base, v)
        b = [x for x in l if "boucle" in x]
        if not b:
            return False, "ligne absente"
        return "INCONNU" in b[0] and len(l) >= _nb_taches(), (
            f"{len(l)} lignes, mode denonce : {'oui' if 'INCONNU' in b[0] else 'NON'}")
    finally:
        os.unlink(v)


def _c_mode_oublie(base):
    """v2.8 — un mode oublie ne doit pas faire disparaitre les taches suivantes.

    ① RÔLE — Rejouer le second défaut du 29-08-2026 : une déclaration de tâche à
      laquelle il manquait son mode de comptage levait une erreur attrapée tout en bas
      du radar, et les tâches déclarées APRÈS celle-là n'étaient plus contrôlées du
      tout, sans un mot. La tâche du cockpit et la mesure de performance
      disparaissaient du rapport en silence. Une déclaration mal formée doit être
      dénoncée seule, les autres continuant d'être contrôlées.
    ② CONTEXTE D'APPEL — `main`, une seule fois, huitième des onze cas, par
      l'intermédiaire de `cas`. Inscrit dans la liste CAS écrite plus bas dans ce même
      programme, jamais appelé par son nom.
    ③ ENTRÉE — `base` : le dossier à faire examiner. Un seul appelant, `main`, qui
      transmet sans le modifier l'argument reçu sur la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — `base` doit exister. La déclaration complète de la boucle
      du jour doit figurer dans le radar, caractère pour caractère : mesuré le
      19-09-2026, elle y figure exactement une fois. Le dossier temporaire du système
      doit pouvoir porter une copie du radar, 91 191 octets.
    ⑤ SORTIE — DEUX valeurs : le verdict et un détail affichable, qui donne le nombre
      de lignes obtenues puis oui ou NON selon que la déclaration mal formée a été
      dénoncée.
      [rend: 2]
    ⑥ TRAITEMENT — ① fabriquer une copie du radar où la déclaration de la boucle du
      jour perd son mode de comptage · ② lancer cette copie sur le dossier reçu, SANS
      recopie préalable · ③ rendre vrai si le radar a rendu au moins une ligne par tâche
      déclarée ET si l'une d'elles dénonce une déclaration INCOMPLÈTE · ④ effacer la
      copie du radar, même en cas d'erreur.
    ⑦ UNITÉ — Un NOMBRE DE LIGNES, autant que de tâches déclarées dans le radar, nombre lu par `_nb_taches` (trois depuis le 30-09-2026, le cockpit n'étant plus déclaré).
    ⑧ POURQUOI — Le cas exige toutes les lignes EN PLUS de la dénonciation, parce que
      c'est la disparition silencieuse des tâches suivantes qui était le vrai défaut,
      pas l'absence de message. Un radar qui dénoncerait la déclaration mal formée
      puis s'arrêterait passerait un contrôle qui ne regarderait que le message.
    ⑨ CE QUI CLOCHE — deux points, mesurés le 19-09-2026, ET LE CAS TOMBE AUJOURD'HUI
      :
      ① La copie modifiée du radar ne démarre plus, et le message d'échec est trompeur
      au point d'envoyer chercher le défaut exactement là où il n'est pas. Écrite dans
      le dossier temporaire du système, la copie n'y trouve pas programmes/COMMUN.py,
      dont le radar dépend depuis le 12-09-2026, et s'arrête sur RuntimeError:
      COMMUN.le_plus_recent introuvable. Le radar n'affiche rien. Sortie mesurée : 0
      lignes (4 attendues), declaration denoncee : NON — qui se lit exactement comme
      le défaut que ce cas surveille, la disparition de toutes les tâches du rapport,
      alors que le radar n'a jamais démarré.
      ② Le cas lance une copie MODIFIÉE du radar directement sur le dossier reçu, sans
      le recopier au préalable, alors que sept des onze cas prennent cette précaution.
      Vérifié le 19-09-2026 : aucun des 243 fichiers d'une copie du dépôt n'a été
      modifié par un passage complet. Mais rien dans le cas ne l'empêche.
    ⑩ EFFET — CRÉE puis EFFACE une copie du radar de 91 191 octets dans le dossier
      temporaire du système. LANCE cette copie une fois, sur le dossier reçu. N'écrit
      aucun fichier dans ce dossier, vérifié par somme de contrôle des 243 fichiers
      d'une copie du dépôt avant et après un passage complet. Aucun accès réseau.
    ⑪ TERMINAISON — Rend la main. La copie du radar est effacée même en cas d'erreur,
      par une clause finale. PEUT LEVER quand le texte à remplacer est absent du radar
      ; l'erreur remonte à `cas`, qui la transforme en échec de ce cas. Aucun de ses
      appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir,
        qui contrôle l'ensemble du système et range chacun de ses constats sous un
        numéro de maillon, par exemple 18-Tâches pour le contrôle des traces
        laissées par les tâches planifiées.
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré
        rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une copie modifiée du radar : un exemplaire du radar dans lequel un morceau
        de texte a été remplacé, écrit dans le dossier temporaire du système, pour
        éprouver un comportement que le radar ne montre pas tel quel.
      la boucle du jour : la tâche planifiée qui collecte les cours et écrit le
        rapport de boucle, du lundi au vendredi seulement.
    """
    v = _variante([('("la boucle du jour", ["rapport_boucle", "cours_nouveaux"], 1, "ouvré")',
                    '("la boucle du jour", ["rapport_boucle", "cours_nouveaux"], 1)')])
    try:
        l = _lignes18(base, v)
        n = _nb_taches()
        return len(l) >= n and any("INCOMPLÈTE" in x for x in l), (
            f"{len(l)} lignes ({n} attendues), declaration denoncee : "
            f"{'oui' if any('INCOMPL' in x for x in l) else 'NON'}")
    finally:
        os.unlink(v)


def _c_trace_absente(base):
    """Une tache qui n'a laisse AUCUNE trace doit etre denoncee.

    ① RÔLE — Vérifier que le radar dénonce une tâche dont il ne trouve plus aucune
      trace. C'est le cas qui répond au constat du 28-08-2026 : les deux boucles du
      matin s'étaient arrêtées en cours de route, ni réussies ni échouées, et personne
      ne l'a su. Le système pouvait cesser de tourner sans que rien ne le dise — pas
      une erreur, un SILENCE.
    ② CONTEXTE D'APPEL — `main`, une seule fois, neuvième des onze cas, par
      l'intermédiaire de `cas`. Inscrit dans la liste CAS écrite plus bas dans ce même
      programme, jamais appelé par son nom.
    ③ ENTRÉE — `base` : le dossier à recopier puis à faire examiner. Un seul appelant,
      `main`, qui transmet sans le modifier l'argument reçu sur la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — `base` doit exister, et le dossier temporaire du système
      pouvoir porter une copie complète du dépôt : 12 Mo pour 243 fichiers, mesuré le
      19-09-2026.
    ⑤ SORTIE — DEUX valeurs : le verdict et un détail affichable. Deux formes — aucune
      ligne : la tache a disparu du rapport quand le radar n'a rien dit de l'audit du
      soir, sinon les soixante premiers caractères de la ligne lue.
      [rend: 2]
    ⑥ TRAITEMENT — ① recopier le dépôt dans un dossier temporaire · ② y effacer tous
      les fichiers dont le nom contient audit_du_jour · ③ lancer le radar · ④ ne
      garder que la ligne parlant de l'audit du soir · ⑤ rendre vrai si elle commence
      par le signe de l'alerte · ⑥ effacer la copie.
    ⑦ UNITÉ — Un SIGNE en tête de ligne, celui de l'alerte.
    ⑧ POURQUOI — Le cas distingue deux échecs qui se ressemblent : une tâche dénoncée
      et une tâche qui a DISPARU du rapport. Le second est plus grave, puisqu'il ne
      laisse rien à lire, et ce détail affiché le nomme explicitement.
    ⑨ CE QUI CLOCHE — un point, et il ne porte pas sur la valeur de preuve du cas. LE
      CAS SAIT ROUGIR : mesuré le 19-09-2026, dans une copie du dépôt le radar a été
      forcé à déclarer un succès quand il ne trouve aucune trace, et le cas est devenu
      ROUGE en affichant la ligne verte fabriquée. Ce qui cloche est que le cas épelle
      le signe de l'alerte : si le radar rangeait demain ce constat parmi les fautes
      bloquantes, ce qui serait une amélioration, la ligne changerait de signe et le
      cas tomberait pour une raison qui n'est pas celle qu'il annonce. Le critère qui
      tranche tient en une question : si je change l'étiquette, mon contrôle
      change-t-il d'avis ? Ici oui, donc il épelle.
    ⑩ EFFET — CRÉE puis EFFACE une copie complète du dépôt dans le dossier temporaire
      du système. EFFACE dans cette copie tous les fichiers dont le nom porte
      audit_du_jour — un seul au dépôt du 19-09-2026, rapports/audit_du_jour.md. LANCE
      le radar une fois. NE TOUCHE PAS au dossier reçu. Aucun accès réseau.
    ⑪ TERMINAISON — Rend la main. La copie est effacée même en cas d'erreur, le
      dossier temporaire étant refermé automatiquement. PEUT LEVER quand le disque est
      plein ou quand la recopie échoue ; l'erreur remonte à `cas`, qui la transforme
      en échec de ce cas. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir,
        qui contrôle l'ensemble du système et range chacun de ses constats sous un
        numéro de maillon, par exemple 18-Tâches pour le contrôle des traces
        laissées par les tâches planifiées.
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré
        rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle
        a tourné — rapport de boucle, rapport d'audit, cockpit, historique des
        mesures.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
    
      l'audit du soir : programmes/audit_ecosysteme.py, lance chaque soir par la tache planifiee, qui ecrit rapports/audit_du_jour.md
"""
    with tempfile.TemporaryDirectory() as t:
        d = os.path.join(t, "d")
        shutil.copytree(base, d)
        for p in glob.glob(d + "/**/*audit_du_jour*", recursive=True):
            os.unlink(p)
        l = [x for x in _lignes18(d) if "audit du soir" in x]
        if not l:
            return False, "aucune ligne : la tache a disparu du rapport"
        return l[0].startswith("⚠️"), f"{l[0][:60]}"


def _c_sans_date(base):
    """Une trace sans date lisible ne doit pas passer pour un succes.

    ① RÔLE — Vérifier qu'un fichier présent mais dont la date ne se lit pas n'est
      jamais compté comme la preuve qu'une tâche a tourné. Un fichier peut être là
      sans rien prouver : tronqué, vidé, ou écrit dans une forme que le radar ne
      reconnaît pas. Le dire est un aveu utile ; le taire est le silence que ce
      programme entier cherche à empêcher.
    ② CONTEXTE D'APPEL — `main`, une seule fois, dixième des onze cas, par
      l'intermédiaire de `cas`. Inscrit dans la liste CAS écrite plus bas dans ce même
      programme, jamais appelé par son nom.
    ③ ENTRÉE — `base` : le dossier à recopier puis à faire examiner. Un seul appelant,
      `main`, qui transmet sans le modifier l'argument reçu sur la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — `base` doit exister et porter au moins un fichier dont le
      nom contient audit_du_jour ; le dossier temporaire du système doit pouvoir
      porter une copie complète du dépôt, 12 Mo pour 243 fichiers mesurés le
      19-09-2026.
    ⑤ SORTIE — DEUX valeurs : le verdict et un détail affichable. Deux formes — ligne
      absente quand le radar n'a rien dit de l'audit du soir, sinon les soixante
      premiers caractères de la ligne lue.
      [rend: 2]
    ⑥ TRAITEMENT — ① recopier le dépôt dans un dossier temporaire · ② y remplacer tous
      les fichiers dont le nom contient audit_du_jour par la seule ligne aucune date
      ici · ③ lancer le radar · ④ ne garder que la ligne parlant de l'audit du soir ·
      ⑤ rendre vrai si elle commence par le signe de l'alerte · ⑥ effacer la copie.
    ⑦ UNITÉ — Un SIGNE en tête de ligne, celui de l'alerte.
    ⑧ POURQUOI — Le fichier est remplacé par un texte court et volontairement dépourvu
      de chiffres, parce que le radar lit les quatre premières lignes d'un document
      rédigé : une seule ligne sans aucun nombre ne peut donner aucune date par
      accident.
    ⑨ CE QUI CLOCHE — un point, et il ne porte pas sur la valeur de preuve du cas. LE
      CAS SAIT ROUGIR : mesuré le 19-09-2026, dans une copie du dépôt le radar a été
      forcé à déclarer un succès quand aucune date n'est lisible, et le cas est devenu
      ROUGE en affichant la ligne verte fabriquée. Ce qui cloche est que le cas épelle
      le signe de l'alerte, comme le cas voisin de la trace absente : si le radar
      rangeait demain ce constat parmi les fautes bloquantes, ce qui serait une
      amélioration, la ligne changerait de signe et le cas tomberait pour une raison
      qui n'est pas celle qu'il annonce.
    ⑩ EFFET — CRÉE puis EFFACE une copie complète du dépôt dans le dossier temporaire
      du système. ÉCRASE dans cette copie tous les fichiers dont le nom porte
      audit_du_jour — un seul au dépôt du 19-09-2026, rapports/audit_du_jour.md. LANCE
      le radar une fois. NE TOUCHE PAS au dossier reçu. Aucun accès réseau.
    ⑪ TERMINAISON — Rend la main. La copie est effacée même en cas d'erreur, le
      dossier temporaire étant refermé automatiquement. PEUT LEVER quand le disque est
      plein ou quand la recopie échoue ; l'erreur remonte à `cas`, qui la transforme
      en échec de ce cas. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir,
        qui contrôle l'ensemble du système et range chacun de ses constats sous un
        numéro de maillon, par exemple 18-Tâches pour le contrôle des traces
        laissées par les tâches planifiées.
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré
        rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle
        a tourné — rapport de boucle, rapport d'audit, cockpit, historique des
        mesures.
      la date déclarée : la date qu'un fichier porte dans son nom ou dans son
        contenu, par opposition à celle que le système de fichiers lui donne.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
    
      l'audit du soir : programmes/audit_ecosysteme.py, lance chaque soir par la tache planifiee, qui ecrit rapports/audit_du_jour.md
      la trace : la liste des sources avec leur etat — LU, ABSENT ou ILLISIBLE — et un detail chiffre, affichee en pied de page.
"""
    with tempfile.TemporaryDirectory() as t:
        d = os.path.join(t, "d")
        shutil.copytree(base, d)
        for p in glob.glob(d + "/**/*audit_du_jour*", recursive=True):
            open(p, "w", encoding="utf-8").write("aucune date ici\n")
        l = [x for x in _lignes18(d) if "audit du soir" in x]
        if not l:
            return False, "ligne absente"
        return l[0].startswith("⚠️"), f"{l[0][:60]}"


def _c_place_pas_alerte(base):
    """v2.4 — le poids du projet INFORME, il n'alerte plus. Il divisait des
    octets par un plafond qui n'est pas en octets et criait a plus de 100 %.

    ① RÔLE — Rejouer le défaut du 28-08-2026 sur le maillon qui mesure le poids du
      projet. Il divisait un nombre d'octets par un plafond qui n'est pas exprimé en
      octets, et annonçait PLACE CRITIQUE 109 % chaque soir. L'alerte était fausse et
      permanente, et une alerte qu'on apprend à ignorer cesse de protéger. Le maillon
      informe désormais du volume, il n'alerte plus sur la saturation.
    ② CONTEXTE D'APPEL — `main`, une seule fois, onzième et dernier des onze cas, par
      l'intermédiaire de `cas`. Inscrit dans la liste CAS écrite plus bas dans ce même
      programme, jamais appelé par son nom. C'est le seul cas qui ne regarde pas le
      maillon des tâches.
    ③ ENTRÉE — `base` : le dossier à faire examiner par le radar. Un seul appelant,
      `main`, qui transmet sans le modifier l'argument reçu sur la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — `base` doit exister, et le radar être lançable depuis le
      dossier de travail sous le nom audit_ecosysteme.py.
    ⑤ SORTIE — DEUX valeurs : le verdict et un détail affichable, qui vaut maillon
      absent, informe sans pourcentage, ou ALERTE ou pourcentage present.
      [rend: 2]
    ⑥ TRAITEMENT — ① lancer le radar sur le dossier reçu · ② ne garder que les lignes
      du maillon du poids · ③ rendre vrai si la première commence par le signe du
      succès et ne contient aucun signe pour cent.
    ⑦ UNITÉ — Le maillon éprouvé compte des OCTETS ; ce cas, lui, ne compte rien : il
      regarde deux propriétés du texte affiché, le signe de tête et l'absence de
      pourcentage.
    ⑧ POURQUOI — Le cas interdit le signe pour cent plutôt que de viser un chiffre,
      parce que la propriété qui compte est qu'aucun rapport ne soit calculé entre
      deux grandeurs d'unités différentes. Viser un chiffre ferait retomber dans le
      défaut qu'on éteint : un garde-fou porte sur une propriété, jamais sur un nombre
      écrit en dur (R-721).
    ⑨ CE QUI CLOCHE — deux points, mesurés le 19-09-2026, et aucun ne porte sur la
      valeur de preuve du cas. LE CAS SAIT ROUGIR : dans une copie du dépôt, le
      plafond du radar a été ramené de mille milliards d'octets à 2 500 000, et le cas
      est devenu ROUGE, ALERTE ou pourcentage present.
      ① Le lancement du radar est réécrit ici au lieu d'employer la fonction que les
      dix autres cas partagent, parce que celle-ci ne rend que les lignes du maillon
      des tâches. Deux écritures d'une même chose divergent toujours (R-708) : une
      limite de temps ajoutée au point commun n'atteindrait pas ce cas.
      ② Le cas épelle deux textes du radar : le numéro et le nom du maillon,
      14-Taille, et le signe du succès. Renommer le maillon rendrait maillon absent et
      le cas tomberait pour une raison qui n'est pas celle qu'il annonce. Le critère
      qui tranche tient en une question : si je renomme, mon contrôle change-t-il
      d'avis ? Ici oui, donc il épelle.
    ⑩ EFFET — LANCE le radar sur le dossier reçu, sans copie préalable. Vérifié le
      19-09-2026 : somme de contrôle des 243 fichiers d'une copie du dépôt avant et
      après un passage complet du jeu d'épreuves, aucune différence. N'écrit rien
      lui-même, n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main. PEUT LEVER si le sous-processus ne peut pas démarrer
      ; l'erreur remonte à `cas`, qui la transforme en échec de ce cas. Aucun de ses
      appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir,
        qui contrôle l'ensemble du système et range chacun de ses constats sous un
        numéro de maillon, par exemple 18-Tâches pour le contrôle des traces
        laissées par les tâches planifiées.
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré
        rejoué à l'identique pour vérifier qu'il n'est pas revenu.
    
      un garde-fou : une limite qui, franchie, fait cesser a la strategie de prendre position tout en continuant a la mesurer.
"""
    r = subprocess.run([sys.executable, SCRIPT, base],
                       capture_output=True, text=True, errors="replace")
    l = [x for x in r.stdout.splitlines() if "14-Taille" in x]
    if not l:
        return False, "maillon absent"
    return l[0].startswith("✅") and "%" not in l[0], (
        "informe sans pourcentage" if l[0].startswith("✅")
        else "ALERTE ou pourcentage present")


CAS = [
    ("les sous-dossiers sont vus", _c_sous_dossiers),
    ("une trace RECOPIEE garde son age", _c_recopie),
    ("un tableau qui s'empile : DERNIERE ligne", _c_tableau_empile),
    ("un document redige : date en TETE", _c_document_redige),
    ("une date future est ignoree", _c_date_future),
    ("dimanche : boucle muette, audit denonce", _c_weekend),
    ("un mode inconnu est denonce", _c_mode_inconnu),
    ("un mode oublie n'efface pas les suivants", _c_mode_oublie),
    ("une trace absente est denoncee", _c_trace_absente),
    ("une trace sans date n'est pas un succes", _c_sans_date),
    ("le poids informe, il n'alerte pas", _c_place_pas_alerte),
]


def main():
    """Joue les onze cas, affiche le bilan, rend 0, 1 ou 2.

    ① RÔLE — Réduire l'état du radar à un seul code de sortie que celui qui vient de
      le modifier peut juger avant de déposer, et afficher en chemin de quoi
      comprendre ce qui est tombé. Sans ce code, rien n'empêcherait de déposer une
      version du radar qui a cessé de voir ce qu'elle voyait la veille.
    ② CONTEXTE D'APPEL — Le lancement du programme, et lui seul. Sa valeur de retour
      est passée directement à la sortie du processus.
    ③ ENTRÉE — Aucun paramètre. Elle lit la ligne de commande, dont elle ne prend que
      le premier argument, le dossier d'épreuve ; sans argument, elle prend le nom
      arbo, qui n'existe nulle part au dépôt du 19-09-2026.
    ④ CONDITIONS D'ENTRÉE — Le dossier d'épreuve doit exister, et le fichier
      audit_ecosysteme.py être présent dans le dossier de travail — donc le programme
      doit être lancé depuis programmes/. Le dossier temporaire du système doit
      pouvoir porter deux copies complètes du dépôt en même temps, 12 Mo chacune pour
      243 fichiers, mesuré le 19-09-2026.
    ⑤ SORTIE — UNE valeur : un entier. 2 quand le dossier d'épreuve est introuvable, 2
      aussi quand le radar est introuvable, 1 quand au moins un cas tombe, 0 quand les
      onze passent.
      [rend: 1]
    ⑥ TRAITEMENT — ① prendre le dossier d'épreuve sur la ligne de commande, ou le nom
      arbo · ② s'arrêter en 2 si ce dossier n'existe pas · ③ s'arrêter en 2 si le
      radar n'est pas là · ④ annoncer le nombre de cas · ⑤ jouer chaque cas de la
      liste, dans l'ordre, enveloppé pour qu'une erreur ne coupe pas la suite ·
      ⑥ afficher une ligne par cas, le verdict puis ce détail · ⑦ si un cas est tombé,
      afficher le compte, la consigne de ne rien déposer et la liste des noms, puis
      rendre 1 · ⑧ sinon afficher que les cas passent, rappeler ce que cela ne prouve
      pas, et rendre 0.
    ⑦ UNITÉ — Les épreuves se comptent en CAS : onze. Un passage complet a duré 5,5
      secondes sur une copie du dépôt du 19-09-2026, qui porte 243 fichiers pour 12
      Mo.
    ⑧ POURQUOI — Le code 2 est réservé au mauvais usage — dossier ou radar introuvable
      — et séparé du code 1, qui dit qu'un cas est tombé : celui qui ne lit que le
      code sait ainsi si ce programme a refusé de travailler ou s'il a constaté un
      défaut. Et les deux dernières lignes affichées rappellent ce que le programme ne
      prouve pas : il ne prouve pas l'absence de défaut, il prouve que les défauts
      déjà vus ne sont pas revenus. C'est la seule chose qu'un jeu d'épreuves puisse
      honnêtement offrir, et le taire laisserait croire l'inverse.
    ⑨ CE QUI CLOCHE — cinq points, tous mesurés le 19-09-2026 sur une copie du dépôt :
      ① RÉGLÉ LE 28-09-2026 (A-435 ②) : LES ONZE CAS PASSENT, et les quatre réparés rougissent quand on retire au radar ce qu'ils surveillent (tests/EPREUVES_DU_JEU_DU_RADAR_Lun_28-09-2026.py). Ce qui était mesuré : QUATRE CAS SUR ONZE TOMBAIENT, ET AUCUN NE METTAIT EN CAUSE LE RADAR.
      Sortie complète : 4 CAS SUR 11 TOMBENT. NE RIEN DEPOSER. — un tableau qui
      s'empile, dimanche, un mode inconnu, un mode oublié. Les trois derniers tombent
      parce que la copie modifiée du radar qu'ils fabriquent ne démarre plus : écrite
      dans le dossier temporaire du système, elle n'y trouve pas programmes/COMMUN.py
      dont le radar dépend depuis le 12-09-2026, et s'arrête sur RuntimeError:
      COMMUN.le_plus_recent introuvable. Le premier tombe parce qu'il écrit son
      fichier d'épreuve au premier niveau de la copie alors que le vrai a été rangé
      dans donnees/. Un jeu d'épreuves qui refuse toute livraison pour des raisons qui
      lui sont propres cesse d'être consulté, et c'est exactement la forme de défaut
      qu'il a été écrit pour empêcher.
      ② LE BILAN NE DISTINGUE PAS LE CAS QUI CONSTATE UN DÉFAUT DU CAS QUI N'A PAS PU
      SE JOUER. Les deux paraissent dans la même liste sous le même mot, TOMBENT.
      Le 19-09-2026, trois des quatre échecs du jour étaient du second genre, et leur détail affiché,
      lignes absentes, envoie chercher le défaut dans le radar.
      ③ RÉGLÉ LE 28-09-2026 (A-435 ②, tests/EPREUVES_DU_JEU_DU_RADAR_Lun_28-09-2026.py) — les deux cas rougissent désormais. Ce qui était mesuré : DEUX CAS SUR ONZE NE POUVAIENT PAS ROUGIR. Mesuré en retirant du radar, dans une
      copie, exactement ce que chaque cas surveille : les sous-dossiers sont vus et
      une trace RECOPIEE garde son age sont restés VERTS. Une épreuve qui reste verte
      quand on retire ce qu'elle teste n'est pas une preuve, c'est une décoration
      (R-731). Cinq cas ont été vérifiés capables de rougir ; les quatre qui tombent
      déjà n'ont pas pu l'être.
      ④ RÉGLÉ LE 28-09-2026 (A-435 ②, tests/EPREUVES_DU_JEU_DU_RADAR_Lun_28-09-2026.py) — ce second étage existe, hors de ce programme. Ce qui était écrit : RIEN ICI NE VÉRIFIE QUE LES CAS PEUVENT ROUGIR. Le programme voisin
      programmes/EPREUVES_DU_SOCLE.py porte ce second étage : il retire une à une les
      corrections que ses cas surveillent et exige que le cas visé devienne rouge. Ce
      programme-ci n'a pas d'équivalent, et c'est pourquoi les deux cas décoratifs ont
      vécu sans être vus.
      ⑤ La liste des cas est écrite à la main hors de cette fonction, et le nombre
      annoncé en découle : ajouter une fonction de cas sans l'inscrire dans la liste
      la rendrait invisible, sans un mot. Mesuré : le document archives/PHOTOGRAPHIE_ABANDONNEE_24-09-2026_voir_A-452.md
      range les onze fonctions de cas parmi les fonctions sans appelant, précisément
      parce qu'aucune n'est appelée par son nom.
    ⑩ EFFET — Affiche une quinzaine de lignes. Ce qu'elle CHANGE vient des cas : sept
      d'entre eux recopient le dépôt entier dans le dossier temporaire du système,
      l'un deux fois ; trois y écrivent une copie du radar de 91 191 octets ; tous
      effacent ce qu'ils ont créé. NE TOUCHE À AUCUN FICHIER DU DOSSIER REÇU : vérifié
      le 19-09-2026 en comparant la somme de contrôle de chacun des 243 fichiers d'une
      copie du dépôt avant et après un passage complet, aucune différence. Aucun accès
      réseau.
    ⑪ TERMINAISON — Rend la main avec 0, 1 ou 2. Elle ne lève pas : chaque cas est
      enveloppé, et une erreur d'un cas devient un échec de ce cas. Un de ses appels
      peut ne pas revenir — `cas` exécute une fonction quelconque et ne rattrape ni
      l'interruption au clavier ni un arrêt demandé par le programme.
      [sort: non]
    ⑫ DÉFINITIONS
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir,
        qui contrôle l'ensemble du système et range chacun de ses constats sous un
        numéro de maillon, par exemple 18-Tâches pour le contrôle des traces
        laissées par les tâches planifiées.
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré
        rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une copie modifiée du radar : un exemplaire du radar dans lequel un morceau
        de texte a été remplacé, écrit dans le dossier temporaire du système, pour
        éprouver un comportement que le radar ne montre pas tel quel.
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle
        a tourné — rapport de boucle, rapport d'audit, cockpit, historique des
        mesures.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    base = sys.argv[1] if len(sys.argv) > 1 else "arbo"
    if not os.path.isdir(base):
        print(f"ARRET : dossier d'epreuve introuvable — {base}")
        return 2
    if not os.path.exists(SCRIPT):
        print(f"ARRET : {SCRIPT} introuvable")
        return 2

    print(f"EPREUVE DU RADAR — {len(CAS)} cas, un par defaut deja rencontre\n")
    echecs = []
    for nom, fn in CAS:
        n, ok, detail = cas(nom, lambda f=fn: f(base))
        print(f"  {'OK   ' if ok else 'ECHEC'} {n:<44} {detail}")
        if not ok:
            echecs.append(n)
    print()
    if echecs:
        print(f"  {len(echecs)} CAS SUR {len(CAS)} TOMBENT. NE RIEN DEPOSER.")
        for e in echecs:
            print(f"    - {e}")
        return 1
    print(f"  LES {len(CAS)} CAS PASSENT. Le radar peut etre depose.")
    print("  Cela ne prouve PAS qu'il est sans defaut : cela prouve que les")
    print("  defauts deja vus ne sont pas revenus.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
