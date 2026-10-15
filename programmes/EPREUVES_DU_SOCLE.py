#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Éprouve FABRIQUER_LE_SOCLE.py par huit cas de cassure, puis retire une à une
les corrections que ces cas surveillent pour vérifier que les cas savent rougir.

① RÔLE — Empêcher qu'une nouvelle version du socle soit déposée sans preuve. Le
  socle range chaque fichier d'une racine en VIVANT, PRÉSUMÉ ou DORMANT, et ce
  classement sert ensuite à décider ce qui peut être déplacé ou archivé : une
  erreur de classement fait disparaître un fichier encore utilisé. Ce programme
  rejoue huit cassures déjà survenues sur ce classement et refuse de valider si
  une seule tombe. Il ajoute un second étage, la méta-épreuve : pour six des
  huit cas, il retire dans une copie du socle la ligne de correction que le cas
  est censé surveiller, relance tout, et exige que CE cas devienne rouge. Un jeu
  d'épreuves qui reste vert quand on retire ce qu'il teste n'est pas une preuve,
  c'est une décoration (R-731).
② CONTEXTE D'APPEL — À la main, avant tout dépôt d'une version du socle, par
  celui qui vient de le modifier. AUCUNE TÂCHE PLANIFIÉE NE LE LANCE : recherche
  du mot EPREUVES_DU_SOCLE dans .github/workflows/ le 19-09-2026, zéro
  occurrence, alors que le même dossier nomme onze autres programmes par leur
  chemin. Le document archives/PHOTOGRAPHIE_ABANDONNEE_24-09-2026_voir_A-452.md le range parmi les vingt-trois
  programmes qui ne tournent pas le soir. Il se relance aussi lui-même, en
  sous-processus, une fois par sabotage.
③ ENTRÉE — La ligne de commande, un seul argument : la racine à éprouver, par
  exemple un point depuis un clone neuf. ET une variable d'environnement,
  `SOCLE_SABOTE` : quand elle vaut « 1 », la méta-épreuve n'est pas jouée. Le
  programme la pose lui-même avant de se relancer.
④ CONDITIONS D'ENTRÉE — La racine doit être un dépôt complet. Il lui faut
  programmes/FABRIQUER_LE_SOCLE.py, programmes/EPREUVES_DU_SOCLE.py,
  programmes/TENIR_LES_POSITIONS.py, un dossier .github/workflows/ portant
  collecte_abc.yml, et un dossier prompts_taches/. `SOCLE_SABOTE` ne doit pas
  déjà valoir « 1 » dans l'environnement. Le dossier temporaire du système doit
  pouvoir porter quatre copies de la racine en même temps : une copie pèse
  11 Mo pour 245 fichiers, mesuré le 19-09-2026, dont 1,1 Mo pour le seul
  BACKLOG_DECISIONS.md, soit environ 44 Mo au plus fort.
⑤ SORTIE — Un code de sortie, et rien d'autre. Le détail est affiché à l'écran :
  une ligne par épreuve, puis une ligne par sabotage, puis le bilan.
⑥ TRAITEMENT — ① sans argument, afficher ce texte et s'arrêter · ② créer un
  dossier temporaire · ③ jouer les huit épreuves, chacune sur sa propre copie de
  la racine · ④ effacer ces copies · ⑤ si `SOCLE_SABOTE` ne vaut pas « 1 », la
  poser à « 1 » et jouer la méta-épreuve · ⑥ afficher le bilan et s'arrêter.
⑦ UNITÉ — Les épreuves se comptent en CAS : huit, nommés K1, K2, K2bis, K3, K4,
  K5, K7 et R-732. Les sabotages se comptent en COUPLES DE TEXTE : six déclarés,
  cinq distincts. Les limites de temps sont en SECONDES : 300 pour un lancement
  du socle, 600 pour un relancement de ce programme. Un passage complet sur le
  dépôt du 19-09-2026 a duré 2,1 secondes.
⑧ POURQUOI — Ce programme est né d'un reproche daté, et il le porte. Le
  12-09-2026, le relecteur écrivait que le socle était « le seul programme du
  dépôt sans jeu d'épreuves, et c'est celui qui fonde le périmètre de tout le
  reste », et qu'il était arrivé sans les cinq passes de contrôle exigées par la
  règle écrite le matin même (R-740). Chaque cas vient donc d'une cassure
  réellement mesurée, jamais d'une idée : K2 d'une racine dépourvue de dossier
  .github/ sur laquelle le socle refusait de travailler, K4 d'un programme
  remplacé par un lien mort et pourtant déclaré vivant, K3 d'un programme chargé
  par motif et rangé parmi les données. Le cas R-732 lit une vraie ligne du
  dépôt, parce qu'un jeu d'épreuves doit contenir au moins un cas venu d'un vrai
  fichier (R-732).
  La méta-épreuve vient d'une seconde mesure du même jour : en retirant une
  correction du socle, les épreuves K1 et K5 restaient VERTES. Elles passaient
  grâce à une AUTRE correction, et testaient donc autre chose que ce que leur
  nom annonçait.
⑨ CE QUI CLOCHE — trois points, tous mesurés le 19-09-2026 :
  ① Le code 1 porte deux causes sans rapport. Lancé sans argument, le programme
  affiche ce texte et sort en 1 ; lancé sur un socle où une épreuve tombe, il
  sort aussi en 1. Ce texte annonce pourtant que 1 veut dire « au moins un
  tombe » : un appelant qui ne lit que le code croit qu'une épreuve est tombée
  alors qu'il s'est mal servi du programme. Le programme voisin
  programmes/PROTEGER_LA_PAGE.py réserve, lui, le code 2 à ce cas.
  ② Une racine qui n'existe pas donne un plantage brut au lieu d'un message.
  Lancé avec l'argument /racine_qui_nexiste_pas, le programme s'arrête sur
  « FileNotFoundError: [Errno 2] No such file or directory:
  '/racine_qui_nexiste_pas' », sort en 1, et laisse derrière lui le dossier
  temporaire qu'il venait de créer.
  ③ La variable `SOCLE_SABOTE` héritée de l'environnement éteint la méta-épreuve
  en silence. Lancé avec SOCLE_SABOTE=1 posée dans le terminal, le programme
  affiche les huit épreuves en vert, N'AFFICHE PAS la section « LES ÉPREUVES
  PEUVENT-ELLES ROUGIR ? », termine par « toutes les épreuves passent » et rend
  le code 0. Rien ne dit que la moitié du travail n'a pas été faite.
⑩ EFFET — CRÉE puis EFFACE jusqu'à vingt-sept copies complètes de la racine dans
  le dossier temporaire du système : trois pour les épreuves, six pour les
  sabotages, et trois de plus dans chacun des six sous-processus. ÉCRIT un
  fichier s.csv dans chacune de ces copies. EFFACE le dossier .github/ dans
  l'une d'elles et y REMPLACE un programme par un lien symbolique mort dans une
  autre. LANCE des sous-processus. POSE la variable d'environnement
  `SOCLE_SABOTE` à « 1 » dans le processus, sans jamais la retirer. NE TOUCHE À
  AUCUN FICHIER DE LA RACINE REÇUE : vérifié le 19-09-2026 en comparant la somme
  de contrôle de chacun des 245 fichiers avant et après un passage complet,
  aucune différence. Aucun accès réseau.
⑪ TERMINAISON — SORT DU PROGRAMME dans tous les cas normaux : 0 quand les huit
  épreuves passent et qu'aucune n'est déclarée inutile, 1 sinon, et 1 aussi
  quand l'argument manque. PEUT S'ARRÊTER SUR UNE ERREUR NON RATTRAPÉE — racine
  absente, dossier temporaire impossible à créer, disque plein, ou dépassement
  d'une limite de temps. Et un de ses appels peut ne pas revenir : `main` se
  termine elle-même.
⑫ DÉFINITIONS
  le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier
    qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une
    chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un
    dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté
    ailleurs.
  un sabotage : le retrait, dans une copie du socle, de la ligne de correction
    qu'une épreuve donnée est censée surveiller.
  la méta-épreuve : le second étage de ce programme, qui rejoue toutes les
    épreuves une fois par sabotage et exige que l'épreuve visée devienne rouge.
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
  le détail : le fichier `registre_experiences.csv`, une ligne par expérience
  le relecteur : celui qui relit le travail de l autre, ici Cowork
  un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré rejoué à l'identique pour vérifier qu'il n'est pas revenu.
"""

import os, shutil, subprocess, sys, tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
SOCLE = os.path.join(ICI, "FABRIQUER_LE_SOCLE.py")


def lancer(racine, sortie):
    """Lance le socle sur une racine préparée et rapporte ce qu'il a dit.

    ① RÔLE — Donner à une épreuve la matière qu'elle juge : le code de sortie du
      socle et la totalité de ce qu'il a affiché. Sans cette fonction, chacune des
      quatre épreuves qui font tourner le socle construirait son propre appel de
      sous-processus, et quatre écritures d'une même chose finiraient par diverger
      (R-708).
    ② CONTEXTE D'APPEL — `main`, quatre fois, une par épreuve qui a besoin de faire
      tourner le socle. K2 sur une copie privée de son dossier .github/, K2bis sur
      un dossier qui ne porte qu'un fichier texte, K4 sur une copie où un programme
      est remplacé par un lien mort, K3 sur une copie intacte. Jamais appelée
      ailleurs.
    ③ ENTRÉE — `racine` : le dossier que le socle doit classer, toujours une copie
      temporaire et jamais la racine reçue sur la ligne de commande · `sortie` : le
      chemin du fichier que le socle doit écrire, toujours un fichier nommé s.csv
      placé à la racine de cette même copie.
    ④ CONDITIONS D'ENTRÉE — Le fichier programmes/FABRIQUER_LE_SOCLE.py doit exister
      à côté de ce programme : son chemin est calculé une fois pour toutes au
      chargement, à partir du dossier de ce fichier. Le socle doit finir en moins de
      300 secondes.
    ⑤ SORTIE — DEUX valeurs : le code de sortie du socle, un entier, et la totalité
      de ce qu'il a affiché, un texte — sa sortie standard puis sa sortie d'erreur,
      collées l'une à l'autre.
      [rend: 2]
    ⑥ TRAITEMENT — ① lancer le socle dans un sous-processus, avec le même
      interpréteur Python que celui qui exécute ce programme · ② lui passer la
      racine puis le chemin du fichier à écrire · ③ capturer ses deux sorties ·
      ④ les coller · ⑤ rendre le code et le texte.
    ⑦ UNITÉ — La limite de temps est en SECONDES : 300. La première valeur rendue
      est un CODE DE SORTIE du socle : 0 quand le classement est écrit, 2 quand
      aucune racine n'a été trouvée, 3 quand un fichier du périmètre est illisible.
    ⑧ POURQUOI — Le sous-processus emploie l'interpréteur courant et non le mot
      « python3 » : les copies vivent dans un dossier temporaire, et rien ne
      garantit que le python3 trouvé dans le chemin du système soit celui qui a
      démarré ce programme.
      Les deux sorties sont collées parce que les épreuves cherchent un texte sans
      se soucier du canal qui l'a porté : l'épreuve K2bis cherche les mots « AUCUNE
      RACINE », que le socle affiche du côté normal, tandis qu'un plantage
      apparaîtrait du côté des erreurs.
    ⑨ CE QUI CLOCHE — deux points :
      ① Coller la sortie normale et la sortie d'erreur rend un message attendu
      indiscernable d'un plantage. L'épreuve K2bis est la seule à juger sur le
      texte, et rien ne lui dit par quel canal les mots sont arrivés : un plantage
      du socle dont la trace contiendrait « AUCUNE RACINE » la ferait passer au
      vert. Aucune mesure ne l'a provoqué — c'est une lecture du code, et elle est
      donnée comme telle.
      ② La limite de 300 secondes n'est pas rattrapée. Au-delà, le lancement lève
      `TimeoutExpired`, qui traverse cette fonction, arrête le programme sans
      message compréhensible et laisse les copies temporaires derrière lui. Un
      passage complet dure 2,1 secondes sur le dépôt du 19-09-2026 : la limite n'a
      jamais été approchée, et c'est la seule raison pour laquelle ce défaut ne
      s'est jamais vu.
    ⑩ EFFET — LANCE UN AUTRE PROGRAMME, qui écrit le fichier désigné par `sortie`
      dans la copie temporaire. Cette fonction elle-même n'écrit aucun fichier,
      n'affiche rien et ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main dans le cas normal. PEUT LEVER `TimeoutExpired`
      au-delà de 300 secondes. Aucun de ses appels ne se termine : un socle qui
      s'arrête n'arrête que son propre sous-processus, et son code revient ici comme
      une valeur ordinaire.
      [sort: non]
    ⑫ DÉFINITIONS
      le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier
        qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une
        chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un
        dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté
        ailleurs.
      un sabotage : le retrait, dans une copie du socle, de la ligne de correction
        qu'une épreuve donnée est censée surveiller.
      la méta-épreuve : le second étage de ce programme, qui rejoue toutes les
        épreuves une fois par sabotage et exige que l'épreuve visée devienne rouge.
    
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      la trace : la liste des sources avec leur etat — LU, ABSENT ou ILLISIBLE — et un detail chiffre, affichee en pied de page.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    r = subprocess.run([sys.executable, SOCLE, racine, sortie],
                       capture_output=True, text=True, timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def lire(sortie):
    """Relit le classement écrit par le socle et le rend interrogeable.

    ① RÔLE — Ramener le classement du socle sous une forme où une épreuve peut
      poser une question précise : quel état porte tel fichier, et avec quelle
      raison. Quatre des huit épreuves ne jugent rien d'autre que cela.
    ② CONTEXTE D'APPEL — `main`, UNE seule fois, sur le fichier produit par
      l'épreuve K3. Les épreuves K3, K1, K5 et R-732 travaillent ensuite toutes les
      quatre sur ce seul résultat. Jamais appelée ailleurs.
    ③ ENTRÉE — `sortie` : le chemin du fichier écrit par le socle. Un seul appelant,
      `main`, et il passe le fichier nommé s.csv placé à la racine de la copie
      fabriquée pour l'épreuve K3.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un fichier absent ne la fait pas tomber : elle
      rend alors un résultat vide, sans le dire.
    ⑤ SORTIE — UNE valeur : un dictionnaire. La clé est le chemin du fichier tel que
      le socle l'a écrit, par exemple programmes/FABRIQUER_LE_SOCLE.py ; la valeur
      est un couple, l'état puis la raison affichée. Le dictionnaire est vide quand
      le fichier n'existe pas.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre un résultat vide si le fichier n'existe pas · ② lire le
      fichier ligne à ligne · ③ sauter les lignes commençant par un dièse et celle
      qui commence par « chemin; » · ④ découper chaque ligne restante sur le
      point-virgule · ⑤ ne garder que les trois premières cases, et seulement quand
      la ligne en porte au moins trois.
    ⑦ UNITÉ — Un NOMBRE DE FICHIERS : 245 clés rendues sur le dépôt du 19-09-2026.
    ⑧ POURQUOI — Trois cases sur quatre suffisent : les épreuves jugent l'état et la
      raison, jamais la liste des programmes qui lisent le fichier. Exiger au moins
      trois cases écarte les lignes tronquées sans avoir à les signaler, ce qui
      convient à un usage où le fichier vient d'être écrit par un programme connu.
    ⑨ CE QUI CLOCHE — trois points :
      ① Deux lignes de commentaire du socle entrent dans le résultat comme si
      c'étaient des fichiers. Le socle écrit ses commentaires avec un écrivain CSV,
      qui les entoure de guillemets parce qu'ils contiennent le séparateur
      point-virgule : la ligne déposée est « "# RACINE ; .github/workflows/
      collecte_abc.yml ; dernier commit INCONNU" », elle commence par un guillemet
      et non par un dièse, et le filtre ne la voit pas. Mesuré le 19-09-2026 : le
      fichier porte 244 lignes de données et cette fonction rend 245 clés ; la clé
      en trop est « "# RACINE » et son prétendu état est «  prompts_taches/
      PROMPTS_TACHES_PLANIFIEES_Sam_12-09-2026_16h51.txt  ». Les deux lignes de
      racine produisent la même clé, donc la seconde efface la première. Aucune
      épreuve ne regarde cette clé aujourd'hui ; une épreuve qui compterait les
      fichiers en compterait un qui n'existe pas.
      ② Le fichier est découpé à la main sur le point-virgule alors qu'il est écrit
      par un écrivain CSV. Deux implémentations d'une même chose divergent toujours
      (R-708) : la quatrième case, qui liste les programmes lecteurs, est elle aussi
      jointe par des points-virgules et donc mise entre guillemets — la ligne
      « BACKLOG_DECISIONS.md;VIVANT;lu par 2 programme(s) vivant(s);
      "audit_ecosysteme.py;claude_FABRIQUER_LE_PILOTE.py" » relevée le 19-09-2026 en
      porte l'exemple — et le découpage la casse en morceaux. Les trois premières
      cases restent justes, donc le défaut ne se voit pas ; il se verra le jour où
      une épreuve voudra lire les lecteurs.
      ③ Un même chemin vu deux fois écrase silencieusement le précédent. Le socle
      n'en produit pas aujourd'hui, puisqu'il parcourt un arbre de fichiers ; rien
      dans cette fonction ne le garantit.
    ⑩ EFFET — LIT un fichier. N'écrit rien, n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main sur un fichier lisible. PEUT LEVER sur un fichier
      qui n'est pas en UTF-8, ou dont la lecture est refusée : seule l'absence du
      fichier est rattrapée. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier
        qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une
        chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un
        dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté
        ailleurs.
      un sabotage : le retrait, dans une copie du socle, de la ligne de correction
        qu'une épreuve donnée est censée surveiller.
      la méta-épreuve : le second étage de ce programme, qui rejoue toutes les
        épreuves une fois par sabotage et exige que l'épreuve visée devienne rouge.
    
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      la raison : le texte court qui dit pourquoi une lecture a échoué, retenu sous le nom `motif`
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    lignes = {}
    if not os.path.isfile(sortie):
        return lignes
    for l in open(sortie, encoding="utf-8"):
        if l.startswith("#") or l.startswith("chemin;"):
            continue
        c = l.rstrip("\n").split(";")
        if len(c) >= 3:
            lignes[c[0]] = (c[1], c[2])
    return lignes


def copier(src, dst):
    """Recopie une racine entière dans un dossier neuf, sans quatre dossiers.

    ① RÔLE — Donner à chaque épreuve son propre dépôt, qu'elle peut casser sans
      toucher au vrai. Les épreuves effacent un dossier entier, remplacent un
      programme par un lien mort et retirent des lignes du socle : faits sur la
      racine reçue, ces gestes la détruiraient.
    ② CONTEXTE D'APPEL — Quatre appels en tout. Trois dans `main`, pour les épreuves
      K2, K4 et K3, et un dans `verifier_les_epreuves`, rejoué une fois par
      sabotage. Jamais appelée ailleurs.
    ③ ENTRÉE — `src` : la racine à recopier, toujours celle reçue sur la ligne de
      commande · `dst` : le dossier à créer, toujours situé sous un dossier
      temporaire du système, et qui ne doit pas déjà exister.
    ④ CONDITIONS D'ENTRÉE — `src` doit exister et être un dossier. `dst` ne doit PAS
      exister : l'outil de recopie le crée lui-même et refuse un dossier déjà en
      place. Le disque doit pouvoir porter 11 Mo de plus, mesuré le 19-09-2026 sur
      une racine de 245 fichiers.
    ⑤ SORTIE — Ne rend rien. Son résultat est le dossier créé.
      [rend: rien]
    ⑥ TRAITEMENT — ① recopier l'arbre entier depuis `src` vers `dst` · ② en écartant
      quatre noms de dossier, .git, __pycache__, _site_travail et archives.
    ⑦ UNITÉ — Un NOMBRE DE FICHIERS et des OCTETS : 245 fichiers et 11 Mo par copie
      sur le dépôt du 19-09-2026, dont 1,1 Mo pour le seul BACKLOG_DECISIONS.md. Un
      passage complet du programme en fabrique vingt-sept, dont quatre au plus
      coexistent, soit environ 44 Mo au plus fort.
    ⑧ POURQUOI — Les quatre dossiers écartés le sont pour deux raisons différentes,
      et elles ne se devinent pas. Les dossiers archives et __pycache__ sont déjà
      écartés par le socle lui-même : les laisser dans la copie ne changerait pas le
      classement mais allongerait la recopie. Le dossier .git, lui, pèse à lui seul
      plus que tout le reste dans un dépôt qui a de l'historique, et aucune épreuve
      ne juge l'historique.
    ⑨ CE QUI CLOCHE — deux points :
      ① Aucune protection. Une racine qui n'existe pas donne un plantage brut au
      lieu d'un message. Mesuré le 19-09-2026 avec l'argument
      /racine_qui_nexiste_pas : le programme s'arrête sur « FileNotFoundError:
      [Errno 2] No such file or directory: '/racine_qui_nexiste_pas' », en code 1,
      et laisse derrière lui le dossier temporaire qui venait d'être créé. Un
      lecteur qui ne connaît pas le programme ne peut pas savoir que son argument
      est en cause.
      ② Écarter .git prive la copie de son historique, et le socle s'en sert. Il
      demande à git la date du dernier enregistrement de chacune de ses racines ;
      dans la copie il n'obtient rien et écrit « dernier commit INCONNU », relevé le
      19-09-2026 dans le fichier produit. Aucune épreuve ne juge cette date, donc
      rien ne tombe ; mais une épreuve qui voudrait la vérifier ne le pourrait pas
      depuis une copie, et le défaut ne se découvrirait qu'à ce moment-là.
    ⑩ EFFET — CRÉE un dossier et y recopie jusqu'à 245 fichiers, 11 Mo. Ne touche
      pas à la source, n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main. PEUT LEVER quand la source n'existe pas, quand la
      destination existe déjà, ou quand le disque est plein. Aucun de ses appels ne
      se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier
        qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une
        chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un
        dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté
        ailleurs.
      un sabotage : le retrait, dans une copie du socle, de la ligne de correction
        qu'une épreuve donnée est censée surveiller.
      la méta-épreuve : le second étage de ce programme, qui rejoue toutes les
        épreuves une fois par sabotage et exige que l'épreuve visée devienne rouge.
    
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
"""
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".git", "__pycache__",
                                                            "_site_travail", "archives"))


# ══════════════════════════════════════════════════════════════════════════
# CHAQUE ÉPREUVE EST SABOTÉE CONTRE SA PROPRE CORRECTION
# ══════════════════════════════════════════════════════════════════════════
# Cowork, 12-09, et c'est la cassure la plus grave de la journée :
#   « J'ai retiré la correction du tour 2 (la seconde racine) et les épreuves K1
#    et K5 sont restées VERTES. K7 l'est aussi, elle vérifie que deux mots sont
#    imprimés. TROIS ÉPREUVES SUR HUIT NE PEUVENT PAS ROUGIR. »
# Mesuré moi-même après lui : K2 rougit, K1 et K5 non. Elles passaient grâce à
# une AUTRE correction — les trois états — et testaient donc autre chose que ce
# que leur nom annonçait. **UN JEU D'ÉPREUVES QUI NE PEUT PAS ROUGIR N'EST PAS
# UNE PREUVE : c'est une décoration, et je l'avais livré comme une preuve.**
#
# LA RÈGLE : pour chaque épreuve, on retire SA correction dans une copie du socle
# et on exige que CETTE épreuve tombe. Une épreuve qui reste verte sous le
# sabotage de sa propre correction est déclarée INUTILE, et le programme échoue.

SABOTAGES = {
    "K2": ('    d_pt = os.path.join(racine, "prompts_taches")\n    if os.path.isdir(d_pt):',
           '    d_pt = os.path.join(racine, "prompts_taches")\n    if False:'),
    "K4": ('        raise SocleIllisible(f"{chemin} : {type(e).__name__} {e}")',
           '        return set(), set(), set()'),
    "K3": ('        for m in motifs:\n            for t in noms_py:',
           '        for m in []:\n            for t in noms_py:'),
    "K1": ('            etat, motif = "PRESUME", "aucun lanceur detecte — un lancement a la main ne s ecrit nulle part"',
           '            etat, motif = "DORMANT", "appele par personne"'),
    "K7": ('    print(f"    VIVANTS  {v:>4}  — mesure : une chaine y mene")',
           '    print(f"    total {v+pr}")'),
}
SABOTAGES["K5"] = SABOTAGES["K1"]


def verifier_les_epreuves(depot):
    """Retire chaque correction, exige que SON épreuve tombe. Rend la liste des inutiles.

    ① RÔLE — Répondre à la seule question que les huit épreuves ne peuvent pas se
      poser elles-mêmes : peuvent-elles seulement devenir rouges ? Une épreuve qui
      reste verte quand on retire ce qu'elle teste n'est pas une preuve, c'est une
      décoration (R-731). Cette fonction fabrique la contre-épreuve.
    ② CONTEXTE D'APPEL — `main`, une seule fois, après les huit épreuves, et
      seulement quand la variable d'environnement `SOCLE_SABOTE` ne vaut pas « 1 ».
      Jamais appelée ailleurs, et jamais dans les sous-processus qu'elle lance.
    ③ ENTRÉE — `depot` : la racine à éprouver. Un seul appelant, `main`, et il
      transmet sans le modifier l'argument reçu sur la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — `SOCLE_SABOTE` doit déjà valoir « 1 » dans
      l'environnement au moment de l'appel, sinon chaque sous-processus relancerait
      à son tour cette fonction, sans fin ; `main` la pose juste avant d'appeler. La
      racine doit porter programmes/FABRIQUER_LE_SOCLE.py ET
      programmes/EPREUVES_DU_SOCLE.py. Chaque texte à retirer doit figurer
      EXACTEMENT UNE FOIS dans le socle.
    ⑤ SORTIE — UNE valeur : la liste des noms d'épreuves qui n'ont pas rougi, vide
      quand toutes ont rougi. Deux formes de nom, et elles ne disent pas la même
      chose : le nom seul, par exemple « K1 », quand l'épreuve a été jouée et n'a
      pas rougi ; le nom suivi de « (sabotage inapplicable) » quand le texte à
      retirer n'a pas été trouvé dans le socle, donc quand l'épreuve n'a même pas
      été jouée.
      [rend: 1]
    ⑥ TRAITEMENT — ① afficher un titre · ② comparer la liste des huit épreuves à
      celle des sabotages et annoncer celles qui ne sont pas couvertes · ③ pour
      chaque sabotage, créer un dossier temporaire, y recopier la racine, remplacer
      dans le socle de cette copie le texte visé par sa version affaiblie, relancer
      CE programme depuis la copie, chercher la marque d'échec de l'épreuve visée
      dans ce que le sous-processus a affiché, afficher le verdict, effacer la copie
      · ④ rendre la liste des épreuves qui n'ont pas rougi.
    ⑦ UNITÉ — Les épreuves se comptent en CAS : huit au total, six portent un
      sabotage, et ces six sabotages ne forment que cinq couples de texte distincts,
      car K1 et K5 partagent le même. La limite de temps d'un sous-processus est en
      SECONDES : 600.
    ⑧ POURQUOI — Cette fonction est née d'une mesure du 12-09-2026 : en retirant une
      correction du socle, les épreuves K1 et K5 restaient VERTES, et K7 aussi.
      Elles passaient grâce à une AUTRE correction que celle qu'elles annonçaient
      surveiller. Trois épreuves sur huit ne pouvaient pas rougir, et le jeu avait
      été livré comme une preuve.
      Le sabotage se fait dans une COPIE et jamais dans la racine reçue, parce qu'il
      consiste à casser volontairement un programme du dépôt.
      Le programme est relancé DEPUIS LA COPIE et non depuis la racine, pour que les
      épreuves jouées soient exactement celles qui accompagnent le socle saboté.
    ⑨ CE QUI CLOCHE — six points, tous mesurés le 19-09-2026 :
      ① Un sous-processus qui n'arrive pas à démarrer est déclaré « épreuve
      inutile ». Le verdict ne repose que sur la présence d'une marque d'échec dans
      ce que le sous-processus a affiché, et un sous-processus qui s'arrête tout de
      suite n'affiche rien de tel. Mesuré dans une copie jetable où le
      sous-processus lève une erreur dès son entrée dans `main` : la sortie annonce
      « 6 EPREUVE(S) INUTILE(S) — elles ne peuvent pas rougir » et nomme les six,
      alors qu'AUCUNE n'a été jouée. Le programme rougit, donc rien ne passe en
      silence ; mais il envoie chercher un défaut dans les épreuves au lieu d'un
      défaut dans le lancement.
      ② Le verdict ne regarde pas QUELLES épreuves ont rougi, seulement que celle
      qu'il vise en fait partie. Mesuré : en retirant la correction visée par K1,
      DEUX épreuves deviennent rouges, K1 et K5, parce que la même ligne du socle
      les tient toutes les deux. Un sabotage qui ferait rougir les huit épreuves
      serait compté comme une réussite pour chacune d'elles.
      ③ K1 et K5 sont comptées comme deux sabotages alors qu'il n'y en a qu'un.
      Mesuré : le dictionnaire des sabotages porte six clés mais cinq couples de
      texte distincts, et les couples de K1 et K5 sont le même objet. L'avertissement
      affiché annonce « 6/8 éprouvées », ce qui surestime la couverture, et la même
      copie est fabriquée puis relancée deux fois pour rien.
      ④ La liste des huit épreuves est écrite à la main dans cette fonction, alors
      que les épreuves elles-mêmes vivent dans `main`. Rien ne relie les deux : un
      neuvième cas ajouté à `main` n'apparaîtrait pas dans cette liste, et
      l'avertissement continuerait d'annoncer « 6/8 éprouvées ». Mesuré : `main`
      porte huit appels au verdict et la liste écrite à la main porte huit noms, les
      deux concordent aujourd'hui par la seule attention de celui qui écrit. Un
      contrôle porte sur une propriété, jamais sur une énumération.
      ⑤ Les textes à retirer sont des copies de lignes du socle, recopiées caractère
      pour caractère. Une espace ajoutée suffit à les décrocher. Mesuré : une seule
      espace ajoutée dans une ligne de FABRIQUER_LE_SOCLE.py, sans le moindre
      changement de comportement, et la sortie devient « K2 : sabotage inapplicable
      (0 occurrence) — épreuve NON VÉRIFIÉE » puis « 1 EPREUVE(S) INUTILE(S) », code
      1. Le rejet est bruyant, ce qui est bien ; mais il accuse l'épreuve K2 alors
      que c'est la mise en forme du socle qui a bougé.
      ⑥ Deux épreuves ne sont jamais sabotées, et l'avertissement qui le dit ne fait
      rien tomber. Mesuré : « NON COUVERTES par le sabotage : K2bis, R-732 ». R-732
      est justement le cas qui vient d'une vraie ligne du dépôt, exigé parce qu'un
      jeu d'épreuves doit contenir au moins un cas venu d'un vrai fichier (R-732).
      Personne ne sait si ces deux-là peuvent rougir.
    ⑩ EFFET — CRÉE puis EFFACE un dossier temporaire par sabotage, six en tout,
      portant chacun une copie complète de la racine. MODIFIE le socle DANS CETTE
      COPIE. LANCE six sous-processus de ce même programme, qui fabriquent chacun
      trois copies de plus et écrivent dans chacune. Affiche une ligne par sabotage.
      NE TOUCHE PAS à la racine reçue. Aucun accès réseau.
    ⑪ TERMINAISON — Rend la main. PEUT LEVER `TimeoutExpired` au-delà de 600
      secondes pour un sous-processus, et une erreur système quand le dossier
      temporaire ne peut pas être créé ou quand le disque est plein. Aucun de ses
      appels ne se termine : un sous-processus qui s'arrête n'arrête que lui-même.
      [sort: non]
    ⑫ DÉFINITIONS
      le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier
        qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une
        chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un
        dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté
        ailleurs.
      un sabotage : le retrait, dans une copie du socle, de la ligne de correction
        qu'une épreuve donnée est censée surveiller.
      la méta-épreuve : le second étage de ce programme, qui rejoue toutes les
        épreuves une fois par sabotage et exige que l'épreuve visée devienne rouge.
    
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      le sabotage : retirer ce qu un contrôle surveille pour vérifier qu il tombe
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    print("\n  ═══ LES ÉPREUVES PEUVENT-ELLES ROUGIR ? ═══")
    # M1 de Cowork : « la méta-épreuve ne couvre que six épreuves sur huit, et ne
    # le dit pas ». Un contrôle qui tait sa propre couverture laisse croire qu'il
    # couvre tout — c'est la cessation muette appliquée à un contrôle de contrôles.
    _tous = ["K2", "K2bis", "K4", "K3", "K1", "K5", "K7", "R-732"]
    _hors = [n for n in _tous if n not in SABOTAGES]
    if _hors:
        print(f"  ⚠️ NON COUVERTES par le sabotage : {', '.join(_hors)} — "
              f"{len(SABOTAGES)}/{len(_tous)} éprouvées")
    inutiles = []
    for nom, (avant, apres) in SABOTAGES.items():
        base = tempfile.mkdtemp(prefix=f"sabot_{nom}_")
        r = os.path.join(base, "depot")
        copier(depot, r)
        cible = os.path.join(r, "programmes", "FABRIQUER_LE_SOCLE.py")
        t = open(cible, encoding="utf-8").read()
        if t.count(avant) != 1:
            print(f"  ⚠️  {nom} : sabotage inapplicable ({t.count(avant)} occurrence) — épreuve NON VÉRIFIÉE")
            inutiles.append(nom + " (sabotage inapplicable)")
            shutil.rmtree(base, ignore_errors=True)
            continue
        open(cible, "w", encoding="utf-8").write(t.replace(avant, apres, 1))
        # relancer LES épreuves depuis la copie sabotée
        rr = subprocess.run([sys.executable, os.path.join(r, "programmes", "EPREUVES_DU_SOCLE.py"), r],
                            capture_output=True, text=True, timeout=600)
        sortie = (rr.stdout or "") + (rr.stderr or "")
        rougit = f"❌ {nom} " in sortie
        print(f"  {'✅' if rougit else '❌'} {nom} rougit quand on retire sa correction"
              + ("" if rougit else "   ← ÉPREUVE INUTILE"))
        if not rougit:
            inutiles.append(nom)
        shutil.rmtree(base, ignore_errors=True)
    return inutiles


def main():
    """Joue les huit épreuves, puis la méta-épreuve, et arrête le programme.

    ① RÔLE — Réduire l'état du socle à un seul code de sortie qu'un relecteur ou une
      tâche peut juger, et afficher en chemin de quoi comprendre ce qui est tombé.
      Sans ce code, rien n'empêcherait de déposer une version du socle qui classe
      mal.
    ② CONTEXTE D'APPEL — Le lancement du programme, et lui seul. Elle est donc aussi
      appelée dans chacun des six sous-processus que la méta-épreuve lance, où elle
      s'arrête avant la méta-épreuve.
    ③ ENTRÉE — Aucun paramètre. Elle lit la ligne de commande, dont elle ne prend
      que le premier argument, la racine à éprouver, et la variable d'environnement
      `SOCLE_SABOTE`.
    ④ CONDITIONS D'ENTRÉE — Un argument au moins. La racine doit être un dépôt
      complet : programmes/FABRIQUER_LE_SOCLE.py,
      programmes/EPREUVES_DU_SOCLE.py, programmes/TENIR_LES_POSITIONS.py, un dossier
      .github/workflows/ portant collecte_abc.yml, et un dossier prompts_taches/.
    ⑤ SORTIE — Ne rend rien : elle se termine toujours par un code de sortie.
      [rend: rien]
    ⑥ TRAITEMENT — ① sans argument, afficher le texte en tête du programme et
      s'arrêter en 1 · ② créer un dossier temporaire · ③ K2, sur une copie privée de
      son dossier .github/, le socle doit travailler et rendre 0 · ④ K2bis, sur un
      dossier ne portant qu'un fichier texte, le socle doit rendre 2 et afficher
      « AUCUNE RACINE » · ⑤ K4, sur une copie où programmes/TENIR_LES_POSITIONS.py
      est remplacé par un lien symbolique mort, le socle doit rendre un code non nul
      et n'écrire aucun fichier · ⑥ K3, sur une copie intacte, le programme
      MODULE_STATISTIQUES, qui n'est chargé que par motif, doit être classé VIVANT ·
      ⑦ K1, le socle ne doit pas se classer lui-même DORMANT · ⑧ K5, aucun des
      quatre programmes de preuve ne doit être DORMANT · ⑨ K7, l'affichage du socle
      doit porter les mots VIVANTS et PRESUMES, jamais un total · ⑩ R-732, le
      fichier .github/workflows/collecte_abc.yml doit être classé VIVANT ·
      ⑪ effacer les copies · ⑫ si `SOCLE_SABOTE` ne vaut pas « 1 », la poser à « 1 »
      et jouer la méta-épreuve · ⑬ afficher le bilan et s'arrêter en 0 ou en 1.
    ⑦ UNITÉ — Les épreuves se comptent en CAS : huit. Les codes attendus du socle
      sont des CODES DE SORTIE : 0 pour K2, 2 pour K2bis, et n'importe quel code non
      nul pour K4. Un passage complet a duré 2,1 secondes sur le dépôt du
      19-09-2026, qui porte 245 fichiers.
    ⑧ POURQUOI — Les épreuves K3, K1, K5 et R-732 lisent le MÊME classement, celui
      produit par la copie de K3, au lieu d'en produire un chacune. Quatre
      classements d'une même racine coûteraient quatre recopies de 11 Mo pour un
      résultat identique.
      L'épreuve K4 remplace un programme par un lien symbolique qui ne mène nulle
      part, parce que c'est le seul moyen de fabriquer un fichier illisible sans
      demander de droits particuliers ; et elle vérifie que RIEN n'est écrit, parce
      qu'un classement partiel est pire qu'un classement absent.
      La méta-épreuve est jouée en dernier et dans le même programme, pour qu'un
      seul lancement rende un seul verdict.
    ⑨ CE QUI CLOCHE — cinq points, tous mesurés le 19-09-2026 :
      ① Deux épreuves passent au vert quand le socle n'écrit rien du tout. Mesuré
      dans une copie jetable où le socle s'arrête juste avant d'écrire son fichier :
      K4 et K5 restent VERTES tandis que K2, K3, K1, K7 et R-732 tombent. K4 se
      contente d'un code non nul et d'un fichier absent, ce qu'un socle qui ne fait
      jamais rien satisfait toujours. K5 cherche des programmes classés DORMANT dans
      un classement vide, n'en trouve aucun, et conclut que tout va bien.
      ② Quatre épreuves sur huit reposent sur un seul lancement du socle. Dans la
      même mesure, K3, K1 et R-732 tombent toutes les trois avec le même motif,
      « ligne absente » ou « absent », alors que la cause unique est que le
      classement n'a pas été écrit. Le lecteur voit quatre défauts là où il y en a
      un.
      ③ Le nom du fichier de tâche planifiée est épelé. L'épreuve R-732 cherche un
      chemin se terminant par collecte_abc.yml, écrit en toutes lettres, alors que
      .github/workflows/ en porte deux le 19-09-2026, collecte_abc.yml et
      comparer_google_abc.yml. Un renommage ferait tomber l'épreuve pour une raison
      qui n'est pas celle qu'elle annonce. Le critère qui tranche tient en une
      question : si je renomme un fichier, mon contrôle change-t-il d'avis ? Ici
      oui, donc il épelle.
      ④ Les copies temporaires survivent à un plantage. Leur effacement est fait
      après les huit épreuves ; mesuré sur une racine inexistante, un dossier
      epreuves_socle_ reste dans le dossier temporaire du système, et 11 Mo y
      resteraient si le plantage arrivait plus tard.
      ⑤ La variable `SOCLE_SABOTE` est posée à « 1 » et jamais retirée. Elle ne vit
      que le temps du processus, donc rien ne fuit vers le terminal ; mais tout
      programme lancé ensuite depuis ce processus l'hériterait et sauterait sa
      propre méta-épreuve sans le dire.
    ⑩ EFFET — CRÉE trois copies complètes de la racine et un dossier vide dans le
      dossier temporaire du système, puis les efface. ÉCRIT un fichier s.csv dans
      chacune des copies. EFFACE le dossier .github/ dans l'une, REMPLACE
      programmes/TENIR_LES_POSITIONS.py par un lien symbolique mort dans une autre.
      POSE la variable d'environnement `SOCLE_SABOTE` à « 1 » dans le processus.
      Affiche une ligne par épreuve, puis le bilan. NE TOUCHE À AUCUN FICHIER DE LA
      RACINE REÇUE : vérifié le 19-09-2026 en comparant la somme de contrôle de
      chacun des 245 fichiers avant et après un passage complet, aucune différence.
      Aucun accès réseau.
    ⑪ TERMINAISON — SORT DU PROGRAMME, et ne rend jamais la main : 0 quand les huit
      épreuves passent et qu'aucune n'est déclarée inutile, 1 quand au moins une
      tombe, et 1 aussi quand l'argument manque. PEUT S'ARRÊTER AVANT sur une erreur
      non rattrapée venue de `copier`, de `lancer` ou de `verifier_les_epreuves`.
      Aucun de ses appels ne se termine de lui-même : les quatre rendent la main ou
      lèvent.
        [sort: oui]
    ⑫ DÉFINITIONS
      le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier
        qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une
        chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un
        dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté
        ailleurs.
      un sabotage : le retrait, dans une copie du socle, de la ligne de correction
        qu'une épreuve donnée est censée surveiller.
      la méta-épreuve : le second étage de ce programme, qui rejoue toutes les
        épreuves une fois par sabotage et exige que l'épreuve visée devienne rouge.
    """
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    depot = sys.argv[1]
    echecs = []

    def verdict(nom, ok, detail):
        """Affiche le résultat d'une épreuve et retient son nom si elle tombe.

        ① RÔLE — Donner à chaque épreuve du jeu une ligne lisible à l'écran, et tenir la
        liste de celles qui sont tombées. Sans elle, `main` afficherait huit résultats
        sans pouvoir dire à la fin lesquels ont échoué, et le code de sortie ne pourrait
        pas être calculé.
        ② CONTEXTE D'APPEL — Définie dans `main` et appelée par elle seule, une fois par
        épreuve, soit huit fois par passage. Elle n'existe pas hors de `main`.
        ③ ENTRÉE — `nom` : le libellé de l'épreuve, par exemple « K1 » · `ok` : vrai ou
        faux, le verdict déjà calculé par l'appelant · `detail` : la phrase à afficher
        quand l'épreuve tombe, par exemple « 2 fichier(s) de meme nom non signale(s) ».
        Un seul appelant, et il passe toujours les trois.
        ④ CONDITIONS D'ENTRÉE — La liste `echecs` doit exister dans `main` avant le
        premier appel : cette fonction y ajoute sans jamais la créer.
        ⑤ SORTIE — Ne rend rien.
          [rend: rien]
        ⑥ TRAITEMENT — ① afficher le nom précédé de ✅ ou ❌ selon `ok` · ② si l'épreuve
        est tombée, afficher `detail` en retrait et ajouter `nom` à la liste `echecs`.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Le verdict et son enregistrement sont faits au même endroit pour
        qu'aucune épreuve affichée en rouge ne puisse être oubliée du compte final. Les
        séparer laisserait la porte ouverte à une épreuve qui rougit à l'écran sans
        changer le code de sortie — un pas vert sur un programme effondré est le pire
        des silences.
        ⑨ CE QUI CLOCHE — Elle écrit dans une liste qui ne lui est pas passée : `echecs`
        appartient à `main` et elle la modifie par effet de bord. Rien dans sa signature
        ne le dit, et un lecteur qui la déplacerait hors de `main` la casserait sans
        avertissement. Relevé par lecture du code le 20-09-2026, jamais provoqué.
        ⑩ EFFET — AFFICHE une à deux lignes à l'écran. AJOUTE un nom à la liste `echecs`
        de `main` quand l'épreuve tombe.
        ⑪ TERMINAISON — Rend toujours la main. Aucun de ses appels ne peut ne pas revenir.
          [sort: non]
        """
        print(f"  {'✅' if ok else '❌'} {nom}")
        if not ok:
            print(f"       {detail}")
            echecs.append(nom)

    base = tempfile.mkdtemp(prefix="epreuves_socle_")

    # ─── K2 : une racine sans workflow mais AVEC des prompts doit fonctionner
    r1 = os.path.join(base, "sans_workflow")
    copier(depot, r1)
    shutil.rmtree(os.path.join(r1, ".github"), ignore_errors=True)
    code, sortie = lancer(r1, os.path.join(r1, "s.csv"))
    verdict("K2 — racine SANS workflow mais AVEC prompts_taches : le socle travaille",
            code == 0, f"code {code} · {sortie.strip()[:150]}")

    # ─── K2bis : aucune racine du tout → CODE 2, pas un plantage
    r2 = tempfile.mkdtemp(prefix="vide_")
    open(os.path.join(r2, "un_fichier.txt"), "w").write("rien")
    code, sortie = lancer(r2, os.path.join(r2, "s.csv"))
    verdict("K2bis — AUCUNE racine : code 2 et message clair, pas un plantage",
            code == 2 and "AUCUNE RACINE" in sortie, f"code {code} · {sortie.strip()[:120]}")

    # ─── K4 : un fichier illisible doit rendre un code NON NUL (R-734)
    r3 = os.path.join(base, "illisible")
    copier(depot, r3)
    cible = os.path.join(r3, "programmes", "TENIR_LES_POSITIONS.py")
    if os.path.isfile(cible):
        os.remove(cible)
        os.symlink("/nexiste_pas_du_tout", cible)
    code, sortie = lancer(r3, os.path.join(r3, "s.csv"))
    verdict("K4 — un programme illisible : code NON NUL, rien d'écrit (R-734)",
            code != 0 and not os.path.isfile(os.path.join(r3, "s.csv")),
            f"code {code} · fichier écrit : {os.path.isfile(os.path.join(r3,'s.csv'))}")

    # ─── K3 : un programme chargé PAR MOTIF n'est pas « appelé par personne »
    r4 = os.path.join(base, "motif")
    copier(depot, r4)
    code, sortie = lancer(r4, os.path.join(r4, "s.csv"))
    lg = lire(os.path.join(r4, "s.csv"))
    ms = [v for k, v in lg.items() if "MODULE_STATISTIQUES" in k]
    # RESSERRÉ le 12-09 : la méta-épreuve a déclaré cette épreuve INUTILE. Elle
    # exigeait seulement « pas appele par personne » — or sous sabotage le verdict
    # devient « nomme par N programmes, mecanisme non resolu », qui passait aussi.
    # Un test qui accepte tout sauf UNE valeur ne teste presque rien. Il faut
    # exiger le verdict ATTENDU, pas l'absence du verdict redouté.
    verdict("K3 — programme chargé par motif : reconnu VIVANT, pas seulement nommé",
            bool(ms) and ms[0][0] == "VIVANT",
            f"verdict rendu : {ms[0] if ms else 'ligne absente'}")

    # ─── K1 : le socle ne se déclare pas DORMANT lui-même
    lgs = [v for k, v in lg.items() if "FABRIQUER_LE_SOCLE" in k]
    verdict("K1 — le socle ne se range pas lui-même parmi les dormants",
            bool(lgs) and lgs[0][0] != "DORMANT",
            f"verdict rendu : {lgs[0] if lgs else 'ligne absente'}")

    # ─── K5 : l'appareil de preuve n'est pas DORMANT
    preuve = ["PROUVER_L_EXECUTION", "TESTS_AUDIT", "verif_backlog", "protocole_qualite"]
    morts = [n for n in preuve
             for k, v in lg.items() if n in k and v[0] == "DORMANT"]
    verdict("K5 — l'appareil de preuve n'est jamais DORMANT",
            not morts, f"rangés dormants : {morts}")

    # ─── K7 : la sortie sépare le mesuré du présumé, jamais un total
    verdict("K7 — deux natures affichées, jamais un total",
            "VIVANTS" in sortie and "PRESUMES" in sortie,
            "la sortie additionne mesuré et décrété")

    # ─── R-732 : un cas venu d'une VRAIE ligne du dépôt
    vrai = [k for k in lg if k.endswith("collecte_abc.yml")]
    verdict("R-732 — le workflow réel est reconnu comme racine",
            bool(vrai) and lg[vrai[0]][0] == "VIVANT",
            f"verdict : {lg.get(vrai[0]) if vrai else 'absent'}")

    shutil.rmtree(base, ignore_errors=True)
    shutil.rmtree(r2, ignore_errors=True)

    # ─── LA META-EPREUVE, sauf si on est deja dans une copie sabotee
    if os.environ.get("SOCLE_SABOTE") != "1":
        os.environ["SOCLE_SABOTE"] = "1"
        inutiles = verifier_les_epreuves(depot)
        if inutiles:
            print(f"\n  {len(inutiles)} EPREUVE(S) INUTILE(S) — elles ne peuvent pas rougir :")
            for i in inutiles:
                print(f"    · {i}")
            echecs.append(f"{len(inutiles)} epreuve(s) qui ne prouvent rien")

    print()
    if echecs:
        print(f"  {len(echecs)} ÉPREUVE(S) TOMBÉE(S) — LE SOCLE N'EST PAS VALIDÉ")
        for e in echecs:
            print(f"    · {e}")
        sys.exit(1)
    print("  toutes les épreuves passent")
    sys.exit(0)


if __name__ == "__main__":
    main()
