#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Range chaque fichier d'une racine en VIVANT, PRÉSUMÉ ou DORMANT, et écrit ce
classement dans gouvernance/SOCLE.csv.

① RÔLE — Donner au projet un périmètre MESURÉ, que n'importe qui peut refaire.
  Le 12-09-2026, l'écosystème avait été partagé en « 34 vivants / 134 dormants »
  par un script écrit à la volée dans une commande et jamais déposé. Le relecteur
  l'a défait en un geste : `find . -iname "*socle*"` ne rend rien, et
  `git log --diff-filter=A` non plus. Un périmètre produit par un outil qui
  n'existe pas n'est pas un périmètre : c'est une opinion, et elle meurt avec la
  session qui l'a formée. La règle de relecture du projet exige une relance depuis
  un clone neuf (R-731) — impossible sur un programme absent du clone. Ce fichier
  est donc le premier geste, avant tout plan de rangement.
② CONTEXTE D'APPEL — À LA MAIN, par celui qui veut savoir ce qui vit, depuis un
  clone du dépôt. AUCUN LANCEUR N'A ÉTÉ TROUVÉ : recherche du mot
  FABRIQUER_LE_SOCLE dans les deux fichiers de .github/workflows/ le 19-09-2026,
  zéro occurrence ; la seule mention dans prompts_taches/ est une ligne de tableau
  d'une consigne, qui n'est pas une ligne de commande. Le programme se range
  d'ailleurs lui-même en PRÉSUMÉ, et le fichier déposé le 16-09-2026 porte
  « programmes/FABRIQUER_LE_SOCLE.py;PRESUME;aucun lanceur detecte ».
③ ENTRÉE — La ligne de commande, deux arguments dont un seul est obligatoire.
  Le premier est la racine à classer, par exemple un point depuis un clone neuf.
  Le second est le fichier à écrire ; sans lui, le programme écrit dans
  <racine>/gouvernance/SOCLE.csv.
  USAGE : python3 FABRIQUER_LE_SOCLE.py <racine> [sortie.csv]
④ CONDITIONS D'ENTRÉE — La racine doit être un dossier existant et porter au
  moins une racine qui lance quelque chose : un fichier de .github/workflows/ qui
  nomme un chemin commençant par programmes/, ou un fichier de prompts_taches/
  qui porte une ligne de commande. Tout fichier .py atteint par une chaîne doit
  être lisible. Le dossier du fichier de sortie doit pouvoir être créé. La
  commande git doit répondre, sans quoi les racines seront datées « INCONNU ».
⑤ SORTIE — Un code de sortie, et rien d'autre : 0 quand le classement est écrit,
  2 quand le programme n'a rien pu classer, 3 quand un fichier du périmètre est
  illisible. Le classement part dans le fichier CSV ; les comptes et les
  homonymes sont affichés.
⑥ TRAITEMENT — ① lister tous les fichiers de la racine, cinq noms de dossier
  écartés · ② relever les racines et les programmes qu'elles lancent · ③ signaler
  les programmes nommés par une racine et absents de l'arbre · ④ partir de ces
  programmes et suivre les chaînes : ce qu'ils importent, ce qu'ils citent, ce
  qu'ils cherchent par motif · ⑤ noter au passage les fichiers de données et de
  documents que chacun nomme · ⑥ ranger chaque fichier en VIVANT, PRÉSUMÉ ou
  DORMANT · ⑦ écrire le CSV, précédé d'une ligne de fabrication et d'une ligne
  par racine avec sa date · ⑧ afficher les trois comptes, jamais leur total ·
  ⑨ nommer les fichiers qui portent le même nom à deux endroits.
⑦ UNITÉ — Un NOMBRE DE FICHIERS. Mesure du 19-09-2026 sur une copie du dépôt de
  244 fichiers : 46 VIVANTS, 37 PRÉSUMÉS, 161 DORMANTS, en 0,075 seconde. Les
  dates des racines sont des DATES de dix caractères, AAAA-MM-JJ. L'attente
  maximale d'une date est en SECONDES : 60.
⑧ POURQUOI — Trois états et non deux, parce que ne pas trouver ne prouve rien.
  Un programme peut en nommer un autre de dix façons : par son nom, par un motif,
  par un glob, par une variable construite. Énumérer ces façons, c'est épeler.
  VIVANT est donc le seul état MESURÉ — une chaîne y mène ; PRÉSUMÉ et DORMANT
  portent exactement la même mesure, aucun lien détecté, et seule la case du
  dossier les sépare. Le total n'est jamais rendu : additionner ce qu'on mesure
  et ce qu'on ignore serait malhonnête, et tant qu'il existe des PRÉSUMÉS aucun
  rangement n'est automatique.
  DEUX RACINES ET NON UNE, et cela se mesure : le fichier de prompts des tâches
  planifiées lance programmes/GENERATEUR_COCKPIT_Sam_15-08-2026_21h50.py, qu'aucun
  workflow ne nomme. Sans cette seconde racine, le générateur du cockpit serait
  rangé parmi les fichiers sans lanceur détecté.
  LES MOTIFS ET NON LES SEULS NOMS, et cela se mesure aussi : la première version
  ne cherchait que les noms entre guillemets, et déclarait gouvernance/
  REGISTRE_REGLES.md et le golden « lus par personne » alors que des programmes
  les cherchent par morceau de nom, sous la forme trouve("REGISTRE_REGLES").
  Cette alerte fausse a été donnée à Jean-Luc avant d'être vérifiée.
  CE PROGRAMME NE DIT PAS LE RÔLE d'un fichier : le rôle ne se mesure pas, il se
  décide.
⑨ CE QUI CLOCHE — six points, tous mesurés le 19-09-2026 :
  ① Personne ne le lance, et le texte d'origine disait le contraire. Ce texte,
  écrit le 12-09-2026, annonçait « Quand l'appeler : tâche du soir, après le
  radar. Jamais à la main. » Recherche du mot FABRIQUER_LE_SOCLE dans les deux
  fichiers de .github/workflows/ : zéro occurrence. Le document
  archives/PHOTOGRAPHIE_ABANDONNEE_24-09-2026_voir_A-452.md le range parmi les vingt-trois programmes qui ne tournent
  pas le soir. Le classement déposé est donc daté du 16-09-2026 à 16h52, trois
  jours avant cette mesure, et rien ne le rafraîchit.
  ② La colonne qui dit POURQUOI un programme est vivant change d'un passage à
  l'autre, sans que rien n'ait bougé. Cinq passages sur la même copie, avec cinq
  valeurs de PYTHONHASHSEED : les états sont identiques à chaque fois, mais de une
  à cinq lignes changent de raison. Exemple relevé : programmes/JUGE_DES_STRATEGIES.py est
  « appele par DETECTER_LES_SIGNAUX_GITHUB.py » au premier passage et « appele par
  TENIR_LES_POSITIONS.py » au troisième. Deux programmes vivants l'appellent, et
  le fichier n'en nomme qu'un, tiré au sort. Comparer deux classements fait donc
  apparaître des différences qui n'en sont pas.
  ③ La colonne s'appelle « lu_par » alors que la détection ne distingue pas lire
  d'écrire : elle relève seulement qu'un programme nomme un fichier. Le fichier
  donnees/claude_cours_nouveaux.csv est déclaré « lu par 11 programme(s)
  vivant(s) », et programmes/COLLECTER_ABC_GITHUB.py, qui figure dans cette liste,
  y AJOUTE les cours du jour. Qui écrit et qui lit ne se lit nulle part, alors que
  c'est exactement la question posée quand deux fichiers portent le même nom.
  ④ Le code 2 porte trois causes sans rapport : argument manquant, racine
  introuvable, et aucune racine sous la racine. Les trois rendent 2 ; seul le
  message diffère, et un appelant qui ne lit que le code ne peut pas savoir s'il
  s'est trompé d'argument ou si le dépôt ne porte plus de tâche planifiée.
  ⑤ L'exclusion des dossiers épelle cinq noms au lieu de porter sur une propriété.
  Le critère qui tranche tient en une question : si je renomme un dossier, mon
  contrôle change-t-il d'avis ? Mesuré en renommant archives/ en vieilleries/ dans
  une copie : le classement passe de 244 à 292 fichiers et de 161 à 203 dormants,
  sans qu'un seul fichier ait changé de contenu.
  ⑥ Dans un workflow, un nom CITÉ est pris pour un nom LANCÉ. Mesuré en ajoutant
  en tête de .github/workflows/collecte_abc.yml la ligne « # on ne lance PLUS
  programmes/JUGE_DES_STRATEGIES.py depuis ce workflow » : programmes/JUGE_DES_STRATEGIES.py passe
  de « appele par TENIR_LES_POSITIONS.py » à « lance par une racine ». Une phrase
  qui dit le contraire déclare donc le programme lancé. Les fichiers de prompts ne
  retiennent plus qu'une ligne de commande et échappent à ce défaut.
⑩ EFFET — ÉCRIT le fichier de sortie, et l'ÉCRASE s'il existe déjà : par défaut
  <racine>/gouvernance/SOCLE.csv. CRÉE le dossier de ce fichier s'il manque —
  mesuré le 19-09-2026 sur une racine ne portant qu'un workflow, le dossier
  gouvernance/ y est apparu. LIT tous les fichiers .py atteints par une chaîne, et
  les racines. LANCE git en lecture seule, deux fois par racine ayant lancé un
  programme. N'écrit aucun autre fichier, ne touche à aucune donnée du système,
  aucun accès réseau.
⑪ TERMINAISON — SORT DU PROGRAMME dans tous les cas prévus, par `main`, avec 0, 2
  ou 3. PEUT S'ARRÊTER AVANT sur une erreur non rattrapée : dossier de sortie
  impossible à créer, droits refusés, disque plein.
⑫ DÉFINITIONS
  le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier
    qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une
    chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un
    dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté
    ailleurs.
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe
    les fichiers — en général un clone du dépôt.
  une racine, ou fichier-racine : un fichier qui LANCE des programmes, soit un
    fichier de .github/workflows/, soit un fichier de prompts_taches/. Le mot
    sert donc à deux choses dans ce programme, le dossier et le fichier.
  un fantôme : un programme nommé par une racine et absent de l'arbre des
    fichiers.
  un motif : un morceau de nom passé à une fonction de recherche, par exemple
    trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
  le golden : le fichier gouvernance/golden_tests_*.json, qui fige des chiffres
    de référence ; tout écart à données identiques est une régression.
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
  le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir, qui contrôle l'ensemble du système et range chacun de ses constats sous un numéro de maillon, par exemple 18-Tâches pour le contrôle des traces laissées par les tâches planifiées.
  le relecteur : celui qui relit le travail de l autre, ici Cowork
"""

import csv, os, re, subprocess, sys
from datetime import datetime, date as _date_py
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")
NON_VIVANT = ("archives", ".git", "__pycache__", "_site_travail", "node_modules")

# un programme en appelle un autre : import, nom de fichier cité, chargement dynamique
_RE_IMPORT = re.compile(r"^\s*(?:from|import)\s+([A-Za-z_][A-Za-z0-9_]*)", re.M)
_RE_PY_CITE = re.compile(r"['\"]([A-Za-z0-9_.\-]+\.py)['\"]")
# un fichier de données ou de document, cité par son nom
_RE_FICHIER = re.compile(r"['\"]([A-Za-z0-9_.\- ]+\.(?:csv|json|md|yml|html|txt))['\"]")
# ① LE DÉFAUT CORRIGÉ : un fichier cherché par MOTIF, pas par son nom complet.
#    `trouve("REGISTRE_REGLES")` · `trouver(base, "golden")` · `_p(base, "journal_trades.csv")`
# Les motifs declares dans une constante : MOTIFS_X = [...] ou MOTIF_X = (...)
_RE_LISTE_MOTIFS = re.compile(r"MOTIFS?_[A-Z_]*\s*=\s*[\[\(]([^\]\)]+)[\]\)]")
_RE_MOTIF = re.compile(r"(?:trouve|trouver|trouve_tous|trouver_tous|_p|chemin_de)\s*\(\s*"
                       r"(?:[A-Za-z_][A-Za-z0-9_]*\s*,\s*)?['\"]([A-Za-z0-9_.\-]{3,})['\"]")


def date_git(racine, chemin_rel):
    """Rend la date du dernier enregistrement d'un fichier au dépôt — ou None.

    ① RÔLE — Dire de quand date une racine sans la lire dans son nom. Une racine
      mal datée fait juger frais un classement qui ne l'est pas : le 12-09-2026, le
      relevé des tâches planifiées s'appelait `..._15h20.txt` pour une lecture
      faite à 16h51 — une heure et demie d'écart, dans un nom écrit sans être
      mesuré.
    ② CONTEXTE D'APPEL — `main`, DEUX FOIS par racine qui a lancé au moins un
      programme : une fois pour écrire la ligne « # RACINE » du fichier, une fois
      pour l'afficher à l'écran. Mesuré le 19-09-2026 sur une copie du dépôt : deux
      racines, quatre appels. Jamais appelée ailleurs.
    ③ ENTRÉE — `racine` : le dossier du dépôt, toujours l'argument reçu sur la
      ligne de commande et transmis sans modification · `chemin_rel` : le chemin
      d'une racine relatif à ce dossier, par exemple
      .github/workflows/collecte_abc.yml.
    ④ CONDITIONS D'ENTRÉE — Aucune. Ni l'absence de git, ni un dossier qui n'est
      pas un dépôt, ni un chemin qui n'existe pas ne la font tomber.
    ⑤ SORTIE — UNE valeur, de deux formes : un texte de dix caractères
      AAAA-MM-JJ, par exemple 2026-09-16 ; ou None quand aucune date n'a pu être
      obtenue.
      [rend: 1]
    ⑥ TRAITEMENT — ① demander à git la date du dernier enregistrement portant sur
      ce seul chemin · ② prendre ce qu'il affiche, sans les espaces · ③ en garder
      les dix premiers caractères, qui sont la date · ④ rendre None si rien n'a été
      affiché, ou si quoi que ce soit a échoué.
    ⑦ UNITÉ — Une DATE de dix caractères, AAAA-MM-JJ, dans le fuseau que git rend.
      L'attente maximale est en SECONDES : 60.
    ⑧ POURQUOI — Le dépôt connaît la vraie date d'un fichier sans la lire dans son
      nom, et aucun renommage ne l'atteint. Le document gouvernance/PILOTE_SOCLE.md
      pose ce principe dès sa cinquième ligne : « CE FICHIER NE CITE AUCUN NOM DE
      FICHIER, ET C'EST DÉLIBÉRÉ », et il le chiffre — « Mesuré le 26-08-2026 : sur
      les 42 noms datés cités dans le BACKLOG, 25 ne pointent plus vers rien —
      60 % ». Désigner vaut mieux qu'épeler.
    ⑨ CE QUI CLOCHE — trois points, tous mesurés le 19-09-2026 :
      ① None veut dire trois choses différentes, et le fichier écrit n'en garde
      aucune. Sur un dépôt d'épreuve créé pour la mesure : un fichier enregistré
      rend « 2026-09-19 » ; un fichier présent mais jamais enregistré rend None ;
      un fichier qui n'existe pas rend None ; et un dossier qui n'est pas un dépôt
      rend None. Les trois derniers s'écrivent tous « dernier commit INCONNU » dans
      le fichier. Un lecteur ne peut pas distinguer une racine oubliée par git d'un
      dossier qui n'a jamais été un dépôt.
      ② Tout est rattrapé, y compris ce qui mériterait de rougir. L'absence de la
      commande git, un dépôt abîmé et un dépassement des 60 secondes rendent tous
      None en silence. La règle du projet veut qu'un contrôle qui n'a pas pu
      tourner rende un code non nul (R-734) : ici, rien ne le signale.
      ③ La même date est demandée deux fois par racine, une fois pour le fichier et
      une fois pour l'affichage, au lieu d'être calculée une fois et transmise. Un
      chiffre qui existe ailleurs ne se recopie pas (R-708) : les deux appels
      peuvent se répondre différemment si un enregistrement survient entre les deux.
    ⑩ EFFET — LANCE la commande git en sous-processus, en lecture seule. N'écrit
      aucun fichier, n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève jamais : toute erreur est
      rattrapée et rendue sous la forme None. Son appel à git peut ne pas revenir
      avant 60 secondes, et le dépassement est alors rattrapé comme le reste.
      [sort: non]
    ⑫ DÉFINITIONS
      le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier
        qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une
        chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un
        dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté
        ailleurs.
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe
        les fichiers — en général un clone du dépôt.
      une racine, ou fichier-racine : un fichier qui LANCE des programmes, soit un
        fichier de .github/workflows/, soit un fichier de prompts_taches/. Le mot
        sert donc à deux choses dans ce programme, le dossier et le fichier.
      le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions et des actions du projet
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    try:
        r = subprocess.run(["git", "-C", racine, "log", "-1", "--format=%cI", "--", chemin_rel],
                           capture_output=True, text=True, timeout=60)
        t = (r.stdout or "").strip()
        return t[:10] if t else None
    except Exception:
        return None


def lister(racine):
    """Rend tous les chemins de la racine, cinq noms de dossier écartés.

    ① RÔLE — Donner l'arbre des fichiers sur lequel tout le reste travaille. C'est
      lui qui décide ce qui PEUT être classé : un fichier absent de cette liste
      n'apparaîtra dans aucun état, ni vivant, ni présumé, ni dormant.
    ② CONTEXTE D'APPEL — Deux fois par passage. `fabriquer` l'appelle pour obtenir
      la liste à classer, et `racines` l'appelle pour savoir quels programmes
      existent vraiment, afin de nommer ceux qu'une racine désigne sans qu'ils
      soient là. Jamais appelée ailleurs.
    ③ ENTRÉE — `racine` : le dossier à parcourir, toujours l'argument reçu sur la
      ligne de commande et transmis sans modification, par exemple un point depuis
      un clone neuf.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un dossier qui n'existe pas ne la fait pas
      tomber : elle rend alors une liste vide, sans le dire.
    ⑤ SORTIE — UNE valeur : la liste triée des chemins, relatifs à la racine, par
      exemple programmes/FABRIQUER_LE_SOCLE.py. Liste vide si le dossier n'existe
      pas ou ne porte aucun fichier.
      [rend: 1]
    ⑥ TRAITEMENT — ① descendre l'arbre depuis la racine · ② à chaque niveau,
      retirer de la descente les dossiers dont le nom figure parmi les cinq écartés
      · ③ pour chaque fichier restant, garder son chemin relatif à la racine ·
      ④ trier.
    ⑦ UNITÉ — Un NOMBRE DE FICHIERS : 244 chemins rendus sur la copie du dépôt du
      19-09-2026, dont 35 fichiers .py.
    ⑧ POURQUOI — Les cinq dossiers écartés le sont pour deux raisons différentes.
      archives/ garde les versions tombées : les classer reviendrait à déclarer
      dormant ce qui est rangé exprès, et à noyer le classement — le dossier porte
      48 fichiers le 19-09-2026, qui feraient passer le classement de 244 à 292
      lignes.
      .git, __pycache__, _site_travail et node_modules ne portent aucun fichier
      écrit par quelqu'un : ce sont des dépôts de travail que les outils
      refabriquent.
    ⑨ CE QUI CLOCHE — trois points, tous mesurés le 19-09-2026 :
      ① L'écart porte sur des NOMS de dossier, pas sur une propriété. Le critère
      qui tranche tient en une question : si je renomme un dossier, mon contrôle
      change-t-il d'avis ? Mesuré en renommant archives/ en vieilleries/ dans une
      copie : le classement passe de 244 à 292 fichiers, et de 161 à 203 dormants.
      Un renommage suffit donc à faire entrer 48 fichiers rangés exprès.
      ② L'écart s'applique à TOUT dossier portant l'un de ces cinq noms, où qu'il
      soit dans l'arbre, et pas seulement à la racine. Un dossier donnees/archives/
      serait écarté sans que rien ne le dise.
      ③ Un dossier qui n'existe pas rend une liste vide, exactement comme un
      dossier vide. Mesuré avec le chemin /nexiste_pas_du_tout : la fonction rend
      la liste vide et ne lève pas. `main` contrôle l'existence de la racine avant
      d'en arriver là, donc le défaut ne se voit pas aujourd'hui ; il se verrait le
      jour où un autre appelant l'emploierait.
    ⑩ EFFET — LIT les noms des dossiers et des fichiers de l'arbre, jamais leur
      contenu. N'écrit rien, n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas sur un dossier absent.
      Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier
        qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une
        chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un
        dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté
        ailleurs.
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe
        les fichiers — en général un clone du dépôt.
      une racine, ou fichier-racine : un fichier qui LANCE des programmes, soit un
        fichier de .github/workflows/, soit un fichier de prompts_taches/. Le mot
        sert donc à deux choses dans ce programme, le dossier et le fichier.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    out = []
    for r, sd, fs in os.walk(racine):
        sd[:] = [x for x in sd if x not in NON_VIVANT]
        for f in fs:
            out.append(os.path.relpath(os.path.join(r, f), racine))
    return sorted(out)


def racines(racine):
    """Rend ce qui LANCE des programmes, et ce qu'une racine nomme en vain.

    ① RÔLE — Trouver le point de départ de toutes les chaînes. Sans racine, rien
      n'est mesurable : un programme n'est vivant que parce que quelque chose le
      lance, et ce quelque chose doit être écrit dans un fichier du dépôt.
    ② CONTEXTE D'APPEL — `fabriquer`, une seule fois, avant tout classement.
      Jamais appelée ailleurs.
    ③ ENTRÉE — `racine` : le dossier à fouiller, toujours l'argument reçu sur la
      ligne de commande et transmis sans modification.
    ④ CONDITIONS D'ENTRÉE — Aucune sur le dossier lui-même : l'absence de
      .github/workflows/ comme celle de prompts_taches/ est prévue. En revanche
      chaque fichier trouvé dans ces deux dossiers doit pouvoir être ouvert.
    ⑤ SORTIE — QUATRE valeurs : ① l'ensemble des noms de programmes lancés, sans
      leur chemin, par exemple audit_ecosysteme.py · ② la liste des chemins des
      fichiers-racines, relatifs à la racine · ③ la liste des sources, une phrase
      par racine qui a lancé quelque chose, de la forme « workflow
      collecte_abc.yml » ou « prompts NOM.txt » · ④ la liste triée des fantômes.
      Mesure du 19-09-2026 sur une copie du dépôt : 12 programmes lancés, 4
      fichiers-racines, 2 sources, 0 fantôme.
      [rend: 4]
    ⑥ TRAITEMENT — ① si .github/workflows/ existe, prendre ses fichiers .yml et
      .yaml dans l'ordre des noms, les compter comme fichiers-racines, y relever
      tout chemin commençant par programmes/ et finissant par .py · ② si
      prompts_taches/ existe, prendre TOUS ses fichiers, les compter comme
      fichiers-racines, et n'y retenir que les LIGNES DE COMMANDE : une ligne qui
      commence par python, python3, sh, bash ou ./ suivie d'un chemin finissant par
      .py · ③ écarter de celles-ci les chemins absolus qui ne commencent pas par
      /tmp/depot · ④ ne garder que le dernier morceau du chemin, le nom du fichier
      · ⑤ lister l'arbre pour savoir quels programmes existent vraiment · ⑥ nommer
      ceux qui sont lancés et absents.
    ⑦ UNITÉ — Un NOMBRE DE PROGRAMMES et un NOMBRE DE FICHIERS. Sur la copie du
      dépôt du 19-09-2026 : 11 programmes viennent du workflow collecte_abc.yml et
      un douzième, programmes/GENERATEUR_COCKPIT_Sam_15-08-2026_21h50.py, du seul
      fichier de prompts.
    ⑧ POURQUOI — DEUX SOURCES ET NON UNE, et c'est la correction la plus lourde de
      ce programme. La version précédente ne regardait que .github/workflows/ : sur
      une racine sans ce dossier, elle rendait le code 2 et refusait de travailler,
      alors que son auteur avait écrit qu'elle « peut balayer le dépôt comme le
      projet ». Les tâches planifiées sont une seconde racine, et elle existe déjà
      au dépôt. Sans elle, quatre programmes qui prouvent que le système dit vrai —
      PROUVER_L_EXECUTION, TESTS_AUDIT, verif_backlog, protocole_qualite —
      tombaient parmi les fichiers sans lanceur détecté.
      UNE RACINE NE SE LIT PAS COMME DE LA PROSE. La correction d'avant cherchait
      des mots dans le texte, et la phrase « ne lance JAMAIS python3 X.py »
      déclarait X vivant : la négation était invisible, et la contamination se
      propageait aux fichiers que X nomme. Un lancement est une LIGNE DE COMMANDE —
      la commande commence la ligne, sans texte français devant. Une phrase, même
      impérative, n'est pas une commande.
      UN CHEMIN ABSOLU HORS DU DÉPÔT N'EST PAS UN PROGRAMME DE L'ÉCOSYSTÈME : c'est
      un brouillon que la tâche écrit elle-même au moment où elle tourne. Les
      chemins sous /tmp/depot sont gardés parce que c'est là que les tâches clonent
      le dépôt, et les lignes de commande du fichier de prompts s'écrivent sous
      cette forme : « python3 /tmp/depot/programmes/GENERATEUR_COCKPIT_....py ».
      LES DEUX LECTURES LÈVENT AU LIEU DE SE TAIRE. Elles étaient lues sans
      protection : un workflow illisible rendait une trace d'erreur brute, un
      prompt illisible passait en silence avec un code 0. Un contrôle qui n'a pas
      pu tourner rend un code non nul (R-734).
      ET CE QUI EST LANCÉ EST CONFRONTÉ À CE QUI EXISTE, avec la MÊME définition
      d'exister que le reste du programme. Ce parcours-ci incluait autrefois
      archives/ alors que la liste de référence l'exclut : un programme mis au
      rebut et toujours nommé par une racine était alors invisible dans les deux
      sens — absent du classement, et pas compté comme fantôme.
    ⑨ CE QUI CLOCHE — cinq points, tous mesurés le 19-09-2026 :
      ① Un fichier rangé dans l'un des deux dossiers est déclaré racine même s'il
      ne lance rien. Tout fichier de .github/workflows/ et TOUT fichier de
      prompts_taches/ entre dans la liste des fichiers-racines, sans qu'on regarde
      son contenu ; le classement leur donne alors l'état VIVANT avec la raison
      « racine : elle lance des programmes ». Deux cas le montrent sur la copie du
      dépôt : .github/workflows/comparer_google_abc.yml, qui écrit son python à
      l'intérieur du workflow et ne nomme aucun fichier de programmes/, et
      prompts_taches/CONSIGNE_COMMENTER_LES_28_PROGRAMMES_Sam_19-09-2026.md, qui
      ne porte aucune ligne de commande. Les deux sont déclarés lanceurs de
      programmes.
      ② Un fichier illisible lève, mais un fichier binaire passe. La lecture
      remplace les caractères qu'elle ne comprend pas au lieu de refuser. Mesuré en
      déposant 300 octets tirés au hasard dans prompts_taches/ : le programme rend
      le code 0 et le fichier est classé « VIVANT;racine : elle lance des
      programmes ».
      ③ Un programme lancé par une racine et absent est seulement signalé, et le
      programme rend quand même 0. Mesuré en ajoutant la ligne « python3
      programmes/JE_NEXISTE_PAS.py » dans prompts_taches/ : la sortie affiche
      « ⚠️ 1 programme(s) nomme(s) par une racine et ABSENT(s) : JE_NEXISTE_PAS.py »
      et le code de sortie est 0. Une racine qui décrit un système qui n'existe
      plus est exactement ce que ce relevé devait rendre visible ; un pas vert
      l'efface.
      ④ Le relevé des workflows n'accepte qu'une seule écriture du chemin, celle
      qui commence par programmes/. Un workflow qui lancerait un programme depuis
      un autre dossier, ou depuis un chemin absolu, ne serait pas vu, et le
      programme lancé tomberait parmi ceux sans lanceur détecté.
      ⑤ Dans un workflow, un nom CITÉ est pris pour un nom LANCÉ. Le relevé cherche
      la suite de caractères « programmes/ » suivie d'un nom finissant par .py,
      n'importe où dans le fichier, y compris dans un commentaire et y compris
      dans une phrase qui dit le contraire. Mesuré en ajoutant en tête de
      .github/workflows/collecte_abc.yml la ligne « # on ne lance PLUS
      programmes/JUGE_DES_STRATEGIES.py depuis ce workflow » : programmes/JUGE_DES_STRATEGIES.py
      devient « VIVANT;lance par une racine », alors qu'il est « VIVANT;appele par
      TENIR_LES_POSITIONS.py » sans cette ligne. Les fichiers de prompts, eux, ne
      retiennent plus qu'une ligne de commande, donc ce défaut ne les touche pas.
    ⑩ EFFET — LIT les noms et le contenu des fichiers des deux dossiers de racines,
      et parcourt tout l'arbre pour dresser la liste des programmes présents.
      N'écrit rien, n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main dans le cas normal. LÈVE `SocleIllisible` dès
      qu'une racine ne peut pas être ouverte, ce qui arrête le classement et fait
      rendre le code 3. Aucun de ses appels ne se termine : `lister` rend toujours
      la main.
      [sort: non]
    ⑫ DÉFINITIONS
      le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier
        qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une
        chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un
        dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté
        ailleurs.
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe
        les fichiers — en général un clone du dépôt.
      une racine, ou fichier-racine : un fichier qui LANCE des programmes, soit un
        fichier de .github/workflows/, soit un fichier de prompts_taches/. Le mot
        sert donc à deux choses dans ce programme, le dossier et le fichier.
      un fantôme : un programme nommé par une racine et absent de l'arbre des
        fichiers.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
    
      la raison : le texte court qui dit pourquoi une lecture a échoué, retenu sous le nom `motif`
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle a tourné — rapport de boucle, rapport d'audit, cockpit, historique des mesures.
"""
    lances, sources, fichiers_racines = set(), [], []
    # L2 de Cowork : « K4 n'est corrigée que sur un chemin sur trois ». Les racines
    # étaient lues sans protection — un workflow illisible rendait un traceback, un
    # prompt illisible passait en silence avec un code 0. Les deux chemins lèvent
    # maintenant `SocleIllisible`, comme la lecture des programmes (R-734).
    d_wf = os.path.join(racine, ".github", "workflows")
    if os.path.isdir(d_wf):
        for f in sorted(os.listdir(d_wf)):
            if f.endswith((".yml", ".yaml")):
                rel = os.path.join(".github", "workflows", f)
                fichiers_racines.append(rel)
                try:
                    t = open(os.path.join(d_wf, f), encoding="utf-8", errors="replace").read()
                except Exception as e:
                    raise SocleIllisible(f"racine {rel} : {type(e).__name__} {e}")
                trouve = set(re.findall(r"programmes/([A-Za-z0-9_.\-]+\.py)", t))
                if trouve:
                    lances |= trouve
                    sources.append(f"workflow {f}")
    d_pt = os.path.join(racine, "prompts_taches")
    if os.path.isdir(d_pt):
        for f in sorted(os.listdir(d_pt)):
            rel = os.path.join("prompts_taches", f)
            fichiers_racines.append(rel)
            try:
                t = open(os.path.join(d_pt, f), encoding="utf-8", errors="replace").read()
            except Exception as e:
                raise SocleIllisible(f"racine {rel} : {type(e).__name__} {e}")
            # R2 de Cowork, 12-09 — ma correction précédente était une SECONDE
            # LISTE DE MOTS, et elle ignorait la négation comme la première
            # ignorait les synonymes : « ne lance JAMAIS python3 X.py » déclarait
            # X vivant, et la contamination se propageait aux données qu'il lit.
            # **Mon essai n'était passé que par chance de l'ordre des mots.**
            # SA CORRECTION, et elle vaut mieux : une racine ne se lit pas comme
            # de la prose. UN LANCEMENT EST UNE LIGNE DE COMMANDE — la commande
            # commence la ligne, sans texte français devant. Une phrase, même
            # impérative, n'est pas une commande.
            # R1 : un chemin absolu hors du dépôt — `/tmp/…` — n'est JAMAIS un
            # programme de l'écosystème. C'est un brouillon que la tâche écrit
            # elle-même au moment où elle tourne. Mon « fantôme » `abc_test.py`
            # en était un, et je l'avais donné comme preuve que L4 marchait.
            trouve = set()
            for ligne in t.split("\n"):
                m = re.match(r"\s*(?:\$\s*)?(?:python3?|sh|bash|\./)\s+(\S+\.py)\b", ligne)
                if not m:
                    continue
                chemin_py = m.group(1)
                if chemin_py.startswith("/") and not chemin_py.startswith("/tmp/depot"):
                    continue          # brouillon hors dépôt, pas l'écosystème
                trouve.add(os.path.basename(chemin_py))
            if trouve:
                lances |= trouve
                sources.append(f"prompts {f}")
    # L4 de Cowork : « une racine qui pointe vers rien ne dit rien ». Un programme
    # nommé par une racine mais ABSENT de l'arbre passait en silence — la racine
    # décrivait un système qui n'existe plus, et personne ne le voyait.
    # R3 de Cowork : DEUX DÉFINITIONS DE « EXISTE » dans le même programme.
    # `lister()` exclut archives/ ; ce parcours-ci les incluait. Un programme mis
    # au rebut, désigné par une racine, était invisible DANS LES DEUX SENS :
    # absent du socle, et pas compté comme fantôme. **C'est exactement ce que L4
    # devait rendre visible : une racine qui décrit un système qui n'existe plus.**
    presents = {os.path.basename(p) for p in lister(racine) if p.endswith(".py")}
    fantomes = sorted(n for n in lances if n not in presents)
    return lances, fichiers_racines, sources, fantomes


class SocleIllisible(Exception):
    """Un fichier du périmètre n'a pas pu être ouvert. R-734 : un contrôle qui n'a
    pas pu tourner rend un code NON NUL. K4 de Cowork : un programme remplacé par
    un lien mort était déclaré VIVANT, le compte ne bougeait pas, le code de sortie
    restait 0 — `except Exception: return set(), set()` avalait tout. Le dépôt
    portait déjà l'épreuve inverse dans PROUVER_L_EXECUTION : « fichier absent :
    lève au lieu de continuer en silence ». Le défaut corrigé là était réintroduit ici."""


def cles_de(chemin_rel):
    """Rend les écritures sous lesquelles un programme peut désigner ce fichier.

    ① RÔLE — Dire, en un seul endroit, sous quels noms un fichier est cherché
      dans le code : son nom entier, son nom sans extension, et les mêmes privés du
      préfixe `claude_`.
    ② CONTEXTE D'APPEL — `lecteurs`, du même programme, une fois par fichier ; et
      `programmes/QUI_TOUCHE_CE_FICHIER.py`, une fois par fichier demandé.
    ③ ENTRÉE — `chemin_rel` : le chemin du fichier relatif à la racine, par
      exemple `donnees/claude_journal_trades.csv`.
    ④ CONDITIONS D'ENTRÉE — Aucune : le fichier n'a pas besoin d'exister.
    ⑤ SORTIE — UNE valeur : un ensemble de chaînes en minuscules. Pour l'exemple :
      `claude_journal_trades.csv`, `claude_journal_trades`, `journal_trades.csv`,
      `journal_trades`.
      [rend: 1]
    ⑥ TRAITEMENT — ① réduire le chemin à son nom · ② garder le nom et le nom sans
      extension, en minuscules · ③ ajouter les mêmes privés de `claude_` · ④ rendre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Cette construction vivait dans `lecteurs` ; elle en est sortie le
      28-09-2026 pour que `QUI_TOUCHE_CE_FICHIER` cherche les MÊMES noms que le
      socle. Deux implémentations d'une même chose divergent toujours (R-708).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main. Aucun de ses appels ne peut ne pas
      revenir.
      [sort: non]
    """
    nom = os.path.basename(chemin_rel)
    cles = {nom.lower(), os.path.splitext(nom)[0].lower()}
    cles |= {c.replace("claude_", "") for c in list(cles)}
    return cles


def lecteurs(lu_par, chemin_rel):
    """Rend l'ensemble des programmes qui portent un motif désignant ce fichier.

    ① RÔLE — **Dire, en un seul endroit, quand un nom relevé dans un programme
      désigne un fichier donné.** C'est la règle de rapprochement du socle ; elle
      vivait dans `fabriquer`, imbriquée, donc hors de portée de tout autre
      programme.
    ② CONTEXTE D'APPEL — `fabriquer`, par sa fonction interne `lecteurs_de`, une
      fois par fichier classé ; et `programmes/QUI_TOUCHE_CE_FICHIER.py`, une fois
      par fichier demandé. Deux appelants, une seule règle (R-708 : deux
      implémentations d'une même chose divergent toujours).
    ③ ENTRÉE — `lu_par` : un dictionnaire dont chaque clé est un nom ou un motif
      relevé dans un programme, en minuscules, et chaque valeur l'ensemble des
      programmes qui le portent. `chemin_rel` : le chemin du fichier, relatif à la
      racine, par exemple `donnees/claude_journal_trades.csv`.
    ④ CONDITIONS D'ENTRÉE — Les clés de `lu_par` sont en minuscules ; `fabriquer`
      les y met, et `QUI_TOUCHE_CE_FICHIER` aussi.
    ⑤ SORTIE — UNE valeur : un ensemble de noms de programmes, vide quand aucun
      motif ne désigne ce fichier.
      [rend: 1]
    ⑥ TRAITEMENT — ① réduire le chemin à son nom de fichier · ② construire les
      clés : le nom entier, le nom sans son extension, et les mêmes privés du
      préfixe `claude_` · ③ pour chaque motif connu, retenir ses programmes si le
      motif est l'une de ces clés, ou si l'une de ces clés commence par le motif et
      que ce motif fait au moins cinq caractères · ④ rendre la réunion.
    ⑦ UNITÉ — Le seuil 5 est un NOMBRE DE CARACTÈRES.
    ⑧ POURQUOI — Les programmes ne nomment pas toujours un fichier de la même
      façon : l'un écrit `claude_cours_nouveaux.csv`, l'autre `cours_nouveaux`, un
      troisième `REGISTRE_REGLES` pour `REGISTRE_REGLES.md`. Le seuil de cinq
      caractères existe pour qu'un motif court comme `cle` n'attrape pas la moitié
      du dépôt. Sortie de `fabriquer` le 28-09-2026 pour que l'outil de R-755 ①
      emploie la MÊME règle que le socle, au lieu d'une copie.
    ⑨ CE QUI CLOCHE — La correspondance par DÉBUT de nom sur-détecte dès que deux
      fichiers partagent un préfixe d'au moins cinq caractères : un motif
      `historique` attrape aussi bien `historique_mesures.csv` que
      `historique_consensus.csv`. Relevé le 20-09-2026, non provoqué.
    ⑩ EFFET — Aucun. Elle lit `lu_par` sans le modifier.
    ⑪ TERMINAISON — Rend toujours la main. Aucun de ses appels ne peut ne pas
      revenir.
      [sort: non]
    """
    cles = cles_de(chemin_rel)
    # un motif est un DEBUT de nom : « REGISTRE_REGLES » trouve « REGISTRE_REGLES.md »
    trouves = set()
    for cle, qui in lu_par.items():
        if cle in cles or any(c.startswith(cle) for c in cles if len(cle) >= 5):
            trouves |= qui
    return trouves


def ce_qu_il_appelle(chemin):
    """Rend ce qu'un programme appelle, ce qu'il nomme, et ce qu'il cherche.

    ① RÔLE — Fournir le maillon suivant de la chaîne. C'est cette fonction qui
      décide si un fichier sera VIVANT : un programme n'entre dans le classement
      que parce qu'un autre, déjà vivant, le nomme ici.
    ② CONTEXTE D'APPEL — `fabriquer`, une fois par programme atteint, au fur et à
      mesure que la chaîne se déroule. Mesuré le 19-09-2026 sur une copie du
      dépôt : 46 fichiers sont déclarés vivants, dont les programmes passés par
      ici. Jamais appelée ailleurs.
    ③ ENTRÉE — `chemin` : le chemin complet d'un fichier .py à lire. Un seul
      appelant, `fabriquer`, et il passe le premier fichier de l'arbre dont le nom
      est celui du programme qu'il cherche.
    ④ CONDITIONS D'ENTRÉE — Le fichier doit pouvoir être ouvert. Il n'a pas besoin
      d'être en UTF-8 : les caractères incompris sont remplacés.
    ⑤ SORTIE — TROIS valeurs : ① l'ensemble des programmes appelés, par leur nom
      d'import ou par leur nom de fichier · ② l'ensemble des fichiers nommés,
      données et documents, auxquels sont ajoutés les motifs · ③ l'ensemble des
      motifs seuls. Le texte qui vivait ici jusqu'au 19-09-2026 n'en annonçait que
      deux.
      [rend: 3]
    ⑥ TRAITEMENT — ① lire le fichier en entier · ② relever les noms qui suivent un
      import · ③ relever les noms de fichiers .py cités entre guillemets · ④
      relever les fichiers de données et de documents cités entre guillemets —
      csv, json, md, yml, html, txt · ⑤ relever les motifs passés directement à une
      fonction de recherche · ⑥ relever les motifs déclarés dans une constante dont
      le nom commence par MOTIF_ ou MOTIFS_ · ⑦ ajouter les motifs à la liste des
      fichiers nommés.
    ⑦ UNITÉ — Un NOMBRE DE NOMS. Mesure du 19-09-2026 sur
      programmes/TENIR_LES_POSITIONS.py : 11 programmes appelés, 10 fichiers
      nommés, 0 motif.
    ⑧ POURQUOI — UN PROGRAMME CHARGÉ PAR MOTIF EST UN PROGRAMME. La version
      d'avant rangeait un programme trouvé par trouver(base, "MODULE_STATISTIQUES")
      parmi les données : la ligne produite se contredisait, « appele par personne »
      et « lu par BANC_ESSAI.py » sur la même ligne. Tout motif qui mène à un .py
      part donc du côté des programmes.
      UN MOTIF DÉCLARÉ DANS UNE LISTE EST UN MOTIF. Le 13-09-2026, le relecteur a
      montré que etudes/PROMPT_BOUCLE_v4....md était classé dormant, « aucun
      lecteur detecte », alors que programmes/audit_ecosysteme.py le cherche par
      MOTIFS_PROMPT_BOUCLE = ["PROMPT_BOUCLE", "TACHE_COWORK"] et l'affiche en vert
      dans le rapport de chaque soir. Le déplacer aurait rendu ce vert faux. Le
      relevé ne captait que les motifs passés directement à une fonction de
      recherche ; ceux qui transitent par une constante lui échappaient.
    ⑨ CE QUI CLOCHE — trois points, tous mesurés le 19-09-2026 :
      ① Un import qui nomme plusieurs modules n'en livre qu'un. Le relevé s'arrête
      au premier nom qui suit le mot import. Mesuré sur ce fichier même, dont la
      ligne d'import est « import csv, os, re, subprocess, sys » : la fonction rend
      csv, collections, datetime et zoneinfo — os, re, subprocess et sys sont
      perdus. Aucun programme du dépôt n'est aujourd'hui importé en deuxième
      position sur une telle ligne, et c'est la seule raison pour laquelle ce
      défaut n'a rien cassé.
      ② Les modules du langage et les programmes du projet sont mélangés dans le
      même ensemble. Sur programmes/TENIR_LES_POSITIONS.py, les 11 « programmes
      appelés » sont JUGE_DES_STRATEGIES.py, CONTRATS_DES_FICHIERS, MODULE_POSITIONS.py, et
      huit modules de Python : csv, glob, importlib, json, os, shutil, sys,
      tempfile. Le tri se fait plus tard, en confrontant ces noms à ceux des
      fichiers existants ; un jour où un programme du projet porterait le nom d'un
      module du langage, les deux seraient confondus.
      ③ Un fichier qui n'est pas en UTF-8 est lu quand même, caractères remplacés,
      au lieu d'être signalé. Seul un fichier qu'on ne peut pas ouvrir du tout —
      absent, ou lien mort — fait lever. Un programme au mauvais encodage rendrait
      donc une liste d'appels incomplète, et rien ne le dirait.
    ⑩ EFFET — LIT un fichier. N'écrit rien, n'affiche rien, ne touche pas au
      réseau.
    ⑪ TERMINAISON — Rend la main sur un fichier ouvrable. LÈVE `SocleIllisible`
      sinon, ce qui arrête le classement et fait rendre le code 3 : le 12-09-2026,
      un programme remplacé par un lien mort était au contraire déclaré VIVANT, le
      compte ne bougeait pas et le code de sortie restait 0. Aucun de ses appels ne
      se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier
        qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une
        chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un
        dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté
        ailleurs.
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe
        les fichiers — en général un clone du dépôt.
      un motif : un morceau de nom passé à une fonction de recherche, par exemple
        trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir, qui contrôle l'ensemble du système et range chacun de ses constats sous un numéro de maillon, par exemple 18-Tâches pour le contrôle des traces laissées par les tâches planifiées.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
    
      le relecteur : celui qui relit le travail de l autre, ici Cowork
"""
    try:
        s = open(chemin, encoding="utf-8", errors="replace").read()
    except Exception as e:
        raise SocleIllisible(f"{chemin} : {type(e).__name__} {e}")
    progs = set(_RE_IMPORT.findall(s)) | set(_RE_PY_CITE.findall(s))
    motifs = set(_RE_MOTIF.findall(s))
    # UN MOTIF DECLARE DANS UNE LISTE EST UN MOTIF. Cassure de Cowork, 13-09-2026 :
    # `etudes/PROMPT_BOUCLE_v4...md` etait classe DORMANT, « aucun lecteur detecte »,
    # alors que `audit_ecosysteme.py` le cherche par
    #     MOTIFS_PROMPT_BOUCLE = ["PROMPT_BOUCLE", "TACHE_COWORK"]
    # et l affiche en ✅ dans le rapport de CHAQUE SOIR. **Le deplacer aurait rendu
    # ce vert faux.** `_RE_MOTIF` ne captait que les motifs passes DIRECTEMENT a
    # `trouve(...)` ; ceux qui transitent par une constante lui echappaient.
    # C est la meme famille que tout le reste du jour : le motif voit une forme et
    # rate l autre.
    for _m in _RE_LISTE_MOTIFS.finditer(s):
        motifs |= set(re.findall(r"[\"']([A-Za-z0-9_.\-]{3,})[\"']", _m.group(1)))
    fichiers = set(_RE_FICHIER.findall(s)) | motifs
    return progs, fichiers, motifs


def fabriquer(racine):
    """Range chaque fichier de la racine dans l'un des trois états, et dit pourquoi.

    ① RÔLE — Produire le classement lui-même : une ligne par fichier, avec son
      état, la raison de cet état, et les programmes qui le nomment. C'est le
      cœur du programme ; tout le reste prépare ou affiche son résultat.
    ② CONTEXTE D'APPEL — `main`, une seule fois, avant toute écriture. Jamais
      appelée ailleurs.
    ③ ENTRÉE — `racine` : le dossier à classer, toujours l'argument reçu sur la
      ligne de commande et transmis sans modification.
    ④ CONDITIONS D'ENTRÉE — La racine doit exister. Tout fichier .py atteint par
      une chaîne doit être lisible, faute de quoi le classement s'arrête.
    ⑤ SORTIE — QUATRE valeurs (4) dans le cas normal, UNE seule (1) quand le
      classement ne peut pas se faire. ① les lignes du
      classement, une liste de quatre cases — chemin, état, pourquoi, programmes
      qui nomment le fichier séparés par des points-virgules — OU None quand
      aucune racine ne lance quoi que ce soit · ② la liste des chemins des
      fichiers-racines · ③ la liste des sources · ④ la liste des fantômes. Les
      trois dernières sont rendues dans les deux cas, y compris quand la première
      est None.
      [rend: 4]
    ⑥ TRAITEMENT — ① lister tous les fichiers · ② relever les racines, les
      programmes qu'elles lancent et les fantômes · ③ s'arrêter là, en rendant None
      à la place des lignes, si aucun programme n'est lancé · ④ partir des
      programmes lancés et dérouler la chaîne : pour chacun, relever ce qu'il
      appelle et ce qu'il nomme, puis empiler les programmes ainsi découverts ·
      ⑤ noter pour chaque fichier nommé quels programmes le nomment · ⑥ ranger
      ensuite chaque fichier de l'arbre, dans cet ordre : racine, puis programme
      atteint par la chaîne, puis programme nommé par un vivant, puis programme
      sans lanceur, puis fichier nommé par un vivant, puis fichier d'un dossier qui
      fait autorité, puis le reste.
    ⑦ UNITÉ — Un NOMBRE DE FICHIERS. Mesure du 19-09-2026 sur une copie du dépôt
      de 244 fichiers : 46 VIVANTS, 37 PRÉSUMÉS, 161 DORMANTS. Le rapprochement
      d'un motif et d'un nom de fichier exige au moins 5 CARACTÈRES.
    ⑧ POURQUOI — L'ORDRE DES CAS EST LE CLASSEMENT LUI-MÊME. Un programme atteint
      par la chaîne est vivant avant d'être jugé sur ses lecteurs ; un programme
      que personne ne lance mais qu'un vivant nomme est présumé et non dormant —
      l'information était déjà là, et c'est l'ordre des cas qui la jetait, au point
      qu'une ligne portait « appele par personne » et « lu par BANC_ESSAI.py » à la
      fois.
      NE PAS TROUVER NE PROUVE RIEN, ET CELA VAUT D'ABORD POUR LES PROGRAMMES. Un
      lancement à la main ne s'écrit nulle part : quatre programmes du dépôt —
      PROUVER_L_EXECUTION, TESTS_AUDIT, verif_backlog, protocole_qualite — ne sont
      lancés que par quelqu'un qui tape leur nom. Ils sont donc présumés, jamais
      dormants. La même prudence vaut pour les dossiers qui font autorité —
      gouvernance, donnees, temoins, prompts_taches, echanges : un programme peut
      nommer un fichier de dix façons, et énumérer ces façons, c'est épeler. La
      mesure qui l'a imposé est donnée par l'auteur du programme : « j'ai annoncé
      que le golden est lu par 6 programmes en comptant les mentions du mot ; la
      première version du socle en trouvait ZÉRO ; celle-ci en trouve 3. Aucun des
      trois chiffres n'est fiable. »
      DORMANT ET PRÉSUMÉ PORTENT LA MÊME MESURE, et le mot le dit maintenant. Le
      relecteur, le 13-09-2026 : « seule diffère la case du dossier. Ton garde-fou
      protège 25 fichiers non prouvés et en laisse déplacer 96 exactement aussi peu
      prouvés. » Cette porte ne se referme pas par du code : elle ne se referme
      qu'en prouvant, fichier par fichier, qu'un dormant est inerte — et cette
      preuve n'existe pas.
    ⑨ CE QUI CLOCHE — quatre points, tous mesurés le 19-09-2026 :
      ① La raison affichée pour un programme vivant est tirée au sort. Quand deux
      programmes vivants en appellent un troisième, seul le premier arrivé est
      écrit, et l'ordre d'arrivée dépend de l'ordre interne d'un ensemble, qui
      change d'un passage à l'autre. Cinq passages sur la même copie, avec cinq
      valeurs de PYTHONHASHSEED : les états sont identiques, mais de une à cinq
      lignes changent de raison — programmes/JUGE_DES_STRATEGIES.py est « appele par
      DETECTER_LES_SIGNAUX_GITHUB.py » au premier passage et « appele par
      TENIR_LES_POSITIONS.py » au troisième. Deux classements pris à deux moments
      ne sont donc pas comparables ligne à ligne.
      ② Un programme nommé par un autre programme mais absent de l'arbre disparaît
      sans un mot. Mesuré en ajoutant « import JE_NEXISTE_PAS_DU_TOUT » à
      programmes/PUBLIER_LE_SITE.py, qui est vivant : la sortie n'affiche aucun
      avertissement et le code de sortie est 0. Le relevé des fantômes ne couvre
      que les programmes nommés par une RACINE.
      ③ Le rapprochement d'un fichier et de son lecteur se fait par DÉBUT DE NOM,
      à partir de cinq caractères. gouvernance/PILOTE.md et
      gouvernance/PILOTE_SOCLE.md sont tous deux crédités du même lecteur,
      claude_FABRIQUER_LE_PILOTE.py. Ce programme nomme bien les deux, donc le
      résultat est juste ici ; mais la règle employée donnerait le même résultat
      s'il n'en nommait qu'un.
      ④ Le rapprochement d'un motif et d'un programme se fait de la même façon, et
      il ne se relit pas. Les quatre rapprochements du jour sont
      MODULE_C5_ETENDU_10 vers le fichier daté correspondant, MODULE_STATISTIQUES
      vers le sien, et deux noms complets vers eux-mêmes. Un motif de cinq
      caractères qui serait le début de deux noms de programmes les déclarerait
      tous les deux appelés.
    ⑩ EFFET — LIT l'arbre des fichiers et le contenu de chaque programme atteint
      par une chaîne. N'écrit aucun fichier, n'affiche rien, ne touche pas au
      réseau : elle rend des lignes que son appelant écrit.
    ⑪ TERMINAISON — Rend la main dans le cas normal. PEUT LEVER `SocleIllisible`,
      venue de `racines` ou de `ce_qu_il_appelle`, quand un fichier du périmètre ne
      peut pas être ouvert. Aucun de ses appels ne se termine : `lister`,
      `racines` et `ce_qu_il_appelle` rendent la main ou lèvent.
      [sort: non]
    ⑫ DÉFINITIONS
      le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier
        qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une
        chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un
        dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté
        ailleurs.
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe
        les fichiers — en général un clone du dépôt.
      une racine, ou fichier-racine : un fichier qui LANCE des programmes, soit un
        fichier de .github/workflows/, soit un fichier de prompts_taches/. Le mot
        sert donc à deux choses dans ce programme, le dossier et le fichier.
      un fantôme : un programme nommé par une racine et absent de l'arbre des
        fichiers.
      un motif : un morceau de nom passé à une fonction de recherche, par exemple
        trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
      le golden : le fichier gouvernance/golden_tests_*.json, qui fige des chiffres
        de référence ; tout écart à données identiques est une régression.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
    
      la raison : le texte court qui dit pourquoi une lecture a échoué, retenu sous le nom `motif`
      le rapprochement : le fait de reconnaître que deux écritures différentes désignent le même fichier ou la même entreprise
"""
    tous = lister(racine)
    noms_py = {os.path.basename(p) for p in tous if p.endswith(".py")}
    lances, fichiers_racines, sources, fantomes = racines(racine)
    if not lances:
        return None, fichiers_racines, sources, fantomes

    # UN ORDRE FIXE (28-09-2026) : parcourus dans l'ordre d'un ensemble, les programmes
    # changeaient d'ordre d'un lancement à l'autre, et la colonne « pourquoi » avec eux
    # (« appele par TENIR_LES_POSITIONS.py » un jour, « par DETECTER_LES_SIGNAUX_GITHUB.py »
    # le lendemain, sur le même dépôt : de 2 à 6 lignes sur 306 différaient selon la graine
    # de hachage, graines 0 à 5, mesure du relecteur). La pile de départ ET les deux boucles
    # qui l'alimentent sont triées : un programme appelé par deux autres prenait pour
    # « pourquoi » l'un ou l'autre selon la graine (relecteur, dépôt fabriqué : 8 contre 4
    # sur 12 graines ; épreuve Z1 de tests/EPREUVES_DU_SOCLE_STABLE_Lun_28-09-2026.py).
    vus, pile, lu_par, pourquoi = set(), sorted(lances), {}, {}
    for r in lances:
        pourquoi[r] = "lance par une racine"
    while pile:
        n = pile.pop()
        if n in vus:
            continue
        vus.add(n)
        chemin = next((os.path.join(racine, p) for p in tous if os.path.basename(p) == n), None)
        if not chemin:
            continue
        progs, fichiers, motifs = ce_qu_il_appelle(chemin)
        for f in fichiers:
            lu_par.setdefault(f.lower(), set()).add(n)
        # K3 — un MOTIF qui resout vers un .py designe un PROGRAMME, pas une donnee
        for m in motifs:
            for t in noms_py:
                if t.lower().startswith(m.lower()) and len(m) >= 5:
                    progs.add(t)
        for a in sorted(progs):
            cible = a if a.endswith(".py") else a + ".py"
            for t in sorted(noms_py):
                if t == cible or t.startswith(cible[:-3]):
                    if t not in vus:
                        pile.append(t)
                        pourquoi.setdefault(t, f"appele par {n}")

    def lecteurs_de(chemin_rel):
        """Rend l'ensemble des programmes qui lisent un fichier donné.

        ① RÔLE — Remplir la dernière case de chaque ligne du classement : qui lit ce
        fichier. C'est ce qui distingue un fichier VIVANT d'un fichier DORMANT — un
        fichier que personne ne lit n'a pas de raison d'être tenu à jour.
        ② CONTEXTE D'APPEL — Définie dans `fabriquer` et appelée par elle seule, une fois
        par fichier du dépôt classé.
        ③ ENTRÉE — `chemin_rel` : le chemin du fichier relatif à la racine, par exemple
        `donnees/claude_cours_nouveaux.csv`. Un seul appelant, qui passe toujours un
        chemin relatif.
        ④ CONDITIONS D'ENTRÉE — Le dictionnaire `lu_par` doit avoir été construit dans
        `fabriquer` avant le premier appel : il associe un motif de recherche à
        l'ensemble des programmes qui le portent.
        ⑤ SORTIE — UNE valeur : un ensemble de noms de programmes, vide quand personne
        ne lit ce fichier.
          [rend: 1]
        ⑥ TRAITEMENT — Confier la question à la fonction `lecteurs`, du même
        programme, avec le dictionnaire `lu_par` de `fabriquer` : elle réduit le chemin
        à son nom, construit ses clés (nom entier, sans extension, sans le préfixe
        `claude_`) et retient les programmes dont un motif est l'une de ces clés ou,
        s'il fait au moins cinq caractères, le début de l'une d'elles. Depuis le
        28-09-2026 la règle vit là, pour que `QUI_TOUCHE_CE_FICHIER` l'emploie aussi.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Les programmes ne nomment pas toujours un fichier de la même façon :
        l'un écrit `claude_cours_nouveaux.csv`, l'autre `cours_nouveaux`, un troisième
        `REGISTRE_REGLES` pour `REGISTRE_REGLES.md`. Comparer les noms bruts ferait
        passer pour DORMANT un fichier lu tous les soirs. Le seuil de cinq caractères
        existe pour qu'un motif court comme `cle` n'attrape pas la moitié du dépôt.
        ⑨ CE QUI CLOCHE — La correspondance par DÉBUT de nom sur-détecte dès que deux
        fichiers partagent un préfixe d'au moins cinq caractères : un motif
        `historique` attrape aussi bien `historique_mesures.csv` que
        `historique_consensus.csv`, et les deux recevraient les mêmes lecteurs. Réparer
        par une propriété plutôt que par une énumération de longueurs est le critère du
        projet (R-745). Relevé par lecture du code le 20-09-2026, non provoqué.
        ⑩ EFFET — Aucun. Elle lit `lu_par` sans le modifier.
        ⑪ TERMINAISON — Rend toujours la main. Aucun de ses appels ne peut ne pas revenir.
          [sort: non]
        """
        return lecteurs(lu_par, chemin_rel)

    lignes = []
    for p in tous:
        nom = os.path.basename(p)
        lect = lecteurs_de(p)
        if p in fichiers_racines:
            etat, motif = "VIVANT", "racine : elle lance des programmes"
        elif p.endswith(".py") and nom in vus:
            etat, motif = "VIVANT", pourquoi.get(nom, "atteint par chainage")
        elif p.endswith(".py") and lect:
            # K3 — l information etait la et l ordre des branches la jetait : un .py
            # ne pouvait jamais etre sauve par un lecteur. « appele par personne »
            # ET « lu par BANC_ESSAI.py » sur la meme ligne.
            etat, motif = "PRESUME", f"nomme par {len(lect)} programme(s) vivant(s), mecanisme non resolu"
        elif p.endswith(".py"):
            # K6 — l asymetrie « ne pas trouver ne prouve rien » etait appliquee aux
            # DONNEES, alors que c est sur les PROGRAMMES que la detection rate :
            # un lancement a la main (PROUVER_L_EXECUTION, TESTS_AUDIT,
            # verif_backlog, protocole_qualite) n est ecrit nulle part.
            etat, motif = "PRESUME", "aucun lanceur detecte — un lancement a la main ne s ecrit nulle part"
        elif lect:
            etat, motif = "VIVANT", f"lu par {len(lect)} programme(s) vivant(s)"
        elif p.split(os.sep)[0] in ("gouvernance", "donnees", "temoins", "prompts_taches", "echanges"):
            # NE PAS TROUVER NE PROUVE RIEN — la regle de Jean-Luc, §9 de ses
            # preferences, appliquee ici. Un programme peut nommer un fichier de
            # dix facons : par son nom, par un motif, par un glob, par une variable
            # construite. Enumerer ces facons, c est EPELER — le piege dans lequel
            # je suis tombe cinq fois cette nuit. Mesure : j ai annonce « le golden
            # est lu par 6 programmes » en comptant les MENTIONS du mot ; la premiere
            # version du socle en trouvait ZERO ; celle-ci en trouve 3. Aucun des
            # trois chiffres n est fiable.
            # DONC : pour les dossiers qui font autorite, l absence de lecteur
            # detecte n emporte JAMAIS le verdict « dormant ». Le socle dit ce qu il
            # sait et nomme ce qu il ignore. C est a l humain de trancher.
            etat, motif = "PRESUME", "dossier qui fait autorite — aucun lecteur detecte"
        else:
            # DORMANT ET PRESUME PORTENT LA MEME MESURE — Cowork, 13-09-2026, et
            # c est la cassure la plus profonde du socle :
            #   « seule differe la case du dossier. Ton garde-fou protege 25
            #    fichiers non prouves et en laisse deplacer 96 exactement aussi
            #    peu prouves. »
            # **Il a raison, et je ne referme pas cette porte par du code : elle
            # ne se referme qu en prouvant, fichier par fichier, qu un dormant
            # est inerte — et cette preuve n existe pas.**
            # Le mot est donc change pour dire ce qu il mesure vraiment. « Dormant »
            # laissait entendre un verdict ; il n y a qu une absence de detection,
            # exactement comme pour un presume.
            etat, motif = "DORMANT", ("aucun lecteur detecte — MEME MESURE QU UN "
                                      "PRESUME, seul le dossier differe")
        lignes.append([p, etat, motif, ";".join(sorted(lect)) if lect else ""])
    return lignes, fichiers_racines, sources, fantomes


def homonymes(lignes):
    """Nomme les fichiers qui portent le même nom à deux endroits.

    ① RÔLE — Faire voir le défaut qui ne se voit pas : deux fichiers de même nom,
      l'un qui reçoit les écritures et l'autre qui est lu, et rien qui le dise.
    ② CONTEXTE D'APPEL — `main`, une seule fois, après l'écriture du classement et
      juste avant la fin du programme. Jamais appelée ailleurs : recherche de son
      nom dans programmes/ le 19-09-2026, un seul appel, à la ligne 443 de ce
      fichier.
    ③ ENTRÉE — `lignes` : les lignes du classement. Un seul appelant, `main`, et il
      transmet telles quelles les lignes rendues par `fabriquer`, chacune étant une
      liste de quatre cases dont la première est le chemin.
    ④ CONDITIONS D'ENTRÉE — Aucune. Les lignes peuvent aussi être des textes, dont
      la première case est alors séparée par un point-virgule ; ce cas est prévu et
      fonctionne, mais aucun appelant ne l'emploie.
    ⑤ SORTIE — UNE valeur : la liste triée des couples. Chaque couple porte le nom
      partagé et la liste triée des chemins qui le portent. Liste vide quand aucun
      nom n'est porté deux fois — c'est le cas sur la copie du dépôt du
      19-09-2026.
      [rend: 1]
    ⑥ TRAITEMENT — ① pour chaque ligne, prendre le chemin, en tirer le nom du
      fichier et le dossier · ② passer les chemins dont le dossier commence par
      archives ou temoins · ③ ranger les chemins par nom de fichier · ④ ne garder
      que les noms portés par plus d'un chemin, triés.
    ⑦ UNITÉ — Un NOMBRE DE CHEMINS par nom de fichier : un couple est signalé dès
      2.
    ⑧ POURQUOI — Ce contrôle est né de trois jours de silence, du 13 au 16-09-2026.
      Deux fichiers s'appelaient historique_mesures.csv, l'un à la racine du dépôt,
      l'autre dans donnees/. Le programme qui mesure la performance écrivait dans
      celui de la racine ; le workflow, le générateur du cockpit et le programme
      qui publie le site lisaient celui de donnees/, que plus personne ne
      modifiait depuis le 11-09. Le pas du workflow qui dépose les mesures, le
      pilote et le rapport du radar faisait un seul git add sur les trois : il
      tombait, et tout ce qui suivait était perdu. Résultat mesuré le 16-09 :
      gouvernance/PILOTE.md et rapports/audit_du_jour.md n'avaient pas bougé
      depuis le 13-09, et le rituel
      de début de session faisait lire un rapport de dimanche en croyant lire celui
      du jour. Le classement, lui, déclarait les DEUX fichiers vivants, avec le
      même motif et les mêmes quatre lecteurs : il range chaque fichier avec son
      chemin, mais il ne comparait jamais les noms entre eux.
      LA PROPRIÉTÉ : deux fichiers de même nom à des endroits différents sont
      presque toujours un défaut, jamais une intention.
      CE CONTRÔLE NE REFUSE RIEN : il nomme les couples, un par un, avec leurs deux
      chemins. Trancher lequel garder appartient à Jean-Luc — un homonyme peut être
      voulu, par exemple une archive qui conserve son nom d'origine. C'est pourquoi
      archives/ et temoins/ sont écartés : leur rôle est précisément de garder un
      fichier sous son nom d'avant. Et c'est pourquoi la fonction rend la LISTE des
      couples et jamais leur compte : un garde-fou porte sur une propriété, jamais
      sur un nombre (R-745).
    ⑨ CE QUI CLOCHE — trois points, tous mesurés le 19-09-2026 :
      ① L'écart d'archives/ ne sert jamais, parce que ces fichiers ne sont pas dans
      les lignes reçues. L'arbre est dressé sans ce dossier : le dépôt porte 48
      fichiers dans archives/, et le classement écrit n'en compte aucun. La même
      protection est donc écrite à deux endroits, et celle-ci est morte.
      ② L'écart épelle deux noms de dossier au lieu de porter sur une propriété. Le
      critère qui tranche tient en une question : si je renomme un dossier, mon
      contrôle change-t-il d'avis ? Ici oui — un dossier temoins/ renommé
      echantillons/ ferait apparaître ses fichiers parmi les homonymes, sans qu'un
      seul octet ait changé.
      ③ Deux formes d'entrée sont acceptées, une seule est employée. La fonction
      sait lire une ligne donnée comme un texte séparé par des points-virgules :
      appelée sur ["a/x.csv;VIVANT", "b/x.csv;VIVANT"], elle rend bien le couple
      x.csv avec ses deux chemins. Aucun appelant ne passe par là, donc cette
      branche n'est jamais éprouvée par l'usage.
    ⑩ EFFET — Aucun. Elle ne lit aucun fichier, n'écrit rien, n'affiche rien, ne
      touche pas au réseau : elle travaille sur ce qu'on lui donne et rend une
      liste.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas sur les formes prévues.
      Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier
        qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une
        chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un
        dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté
        ailleurs.
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe
        les fichiers — en général un clone du dépôt.
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir, qui contrôle l'ensemble du système et range chacun de ses constats sous un numéro de maillon, par exemple 18-Tâches pour le contrôle des traces laissées par les tâches planifiées.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
    
      un garde-fou : une limite qui, franchie, fait cesser a la strategie de prendre position tout en continuant a la mesurer.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    import collections as _c
    par_nom = _c.defaultdict(list)
    for l in lignes:
        ch = l[0] if isinstance(l, (list, tuple)) else str(l).split(";")[0]
        nom = ch.replace("\\", "/").split("/")[-1]
        dossier = ch.replace("\\", "/").rsplit("/", 1)[0] if "/" in ch else ""
        # un homonyme dans archives/ ou temoins/ est VOULU : c est leur role
        if dossier.startswith(("archives", "temoins")):
            continue
        par_nom[nom].append(ch)
    return sorted((n, sorted(c)) for n, c in par_nom.items() if len(c) > 1)


def main():
    """Classe la racine, écrit le fichier, affiche les comptes, et arrête le programme.

    ① RÔLE — Réduire l'état d'un dépôt à un fichier qu'on peut relire et à un code
      de sortie qu'un relecteur peut juger, sans jamais rendre un total qui
      mélangerait ce qui est mesuré et ce qui est ignoré.
    ② CONTEXTE D'APPEL — Le lancement du programme, et lui seul. Elle est aussi
      appelée dans les sous-processus que programmes/EPREUVES_DU_SOCLE.py, qui
      éprouve ce programme, lance sur des copies préparées.
    ③ ENTRÉE — Aucun paramètre. Elle lit la ligne de commande : le premier argument
      est la racine, le second, facultatif, est le fichier à écrire. Sans second
      argument, elle écrit dans <racine>/gouvernance/SOCLE.csv.
    ④ CONDITIONS D'ENTRÉE — Un argument au moins. La racine doit être un dossier
      existant portant au moins une racine qui lance un programme. Le dossier du
      fichier de sortie doit pouvoir être créé, et le fichier écrit.
    ⑤ SORTIE — Ne rend rien : elle se termine toujours par un code de sortie.
      [rend: rien]
    ⑥ TRAITEMENT — ① sans argument, afficher le texte en tête du programme et
      s'arrêter en 2 · ② s'arrêter en 2 si la racine n'est pas un dossier ·
      ③ classer la racine · ④ s'arrêter en 3 si un fichier du périmètre est
      illisible, sans rien écrire · ⑤ signaler les programmes nommés par une racine
      et absents · ⑥ s'arrêter en 2 si aucune racine n'a été trouvée · ⑦ créer le
      dossier de sortie si besoin, puis écrire le fichier : une ligne de
      fabrication horodatée, une ligne par racine avec la date de son dernier
      enregistrement, la ligne des titres, puis le classement · ⑧ afficher la
      racine, les sources et leur date · ⑨ afficher les trois comptes séparément et
      la consigne de ne rien ranger automatiquement · ⑩ nommer les homonymes ·
      ⑪ s'arrêter en 0.
    ⑦ UNITÉ — Un NOMBRE DE FICHIERS pour les trois comptes. L'horodatage de la
      ligne de fabrication est en heure de Paris, au format AAAA-MM-JJ HH:MM. Les
      dates des racines sont des DATES de dix caractères. Mesure du 19-09-2026 sur
      une copie du dépôt : 244 fichiers, 46 vivants, 37 présumés, 161 dormants, en
      0,075 seconde.
    ⑧ POURQUOI — LES DEUX NATURES NE S'ADDITIONNENT PAS. L'affichage disait
      autrefois « 48 vivants », ce qui mélangeait ce qui est mesuré et ce qui est
      décrété. Dire ce qu'on ignore est honnête ; l'ajouter à ce qu'on sait ne
      l'est pas.
      LES RACINES ENTRENT DANS LE FICHIER, PAS SEULEMENT DANS L'AFFICHAGE : un
      avertissement que rien ne peut relire n'a pas d'existence dès que la tâche
      est finie. Chaque racine y figure avec la date que le dépôt lui donne.
      LE SOCLE DIT LA DATE, IL NE JUGE PAS DE LA FRAÎCHEUR, et il n'a plus de
      seuil. Le seuil de sept jours a été supprimé, pas atténué : un relevé de
      trois mois dont aucune tâche n'a bougé est frais, et le seuil l'aurait
      condamné à tort. Le contrôle de fraîcheur n'est pas du ressort de ce
      programme — il ne peut pas voir une dictée faite après le relevé ; il est du
      ressort de celui qui tient la liste des tâches.
      RIEN N'EST ÉCRIT QUAND UN FICHIER EST ILLISIBLE : un classement partiel est
      pire qu'un classement absent, parce qu'il a l'air complet. Et un contrôle qui
      n'a pas pu tourner rend un code non nul (R-734).
    ⑨ CE QUI CLOCHE — quatre points, tous mesurés le 19-09-2026 :
      ① Le code 2 porte trois causes sans rapport. Lancé sans argument, le
      programme affiche son texte d'en-tête et rend 2 ; lancé sur /nexiste_pas_xyz,
      il affiche « CODE 2 — racine introuvable » et rend 2 ; lancé sur un dossier
      ne portant qu'un fichier texte, il affiche « CODE 2 — AUCUNE RACINE » et rend
      2. Un appelant qui ne lit que le code ne peut pas distinguer une erreur
      d'usage d'un dépôt qui ne porte plus de tâche planifiée.
      ② Les programmes fantômes ne font pas rougir. Mesuré en ajoutant la ligne
      « python3 programmes/JE_NEXISTE_PAS.py » dans prompts_taches/ : la sortie
      porte « ⚠️ 1 programme(s) nomme(s) par une racine et ABSENT(s) » et le code de
      sortie est 0. Une racine qui décrit un système qui n'existe plus passe donc
      pour un succès.
      ③ Les deux lignes de racine écrites en tête du fichier passent par l'écrivain
      CSV, qui les entoure de guillemets parce qu'elles contiennent le séparateur
      point-virgule. La deuxième ligne du fichier produit est « "# RACINE ;
      .github/workflows/collecte_abc.yml ; dernier commit INCONNU" » : elle
      commence par un guillemet et non par un dièse. Un lecteur qui saute les
      lignes commençant par un dièse les prend pour des fichiers — c'est ce qui
      arrive à la fonction de relecture de programmes/EPREUVES_DU_SOCLE.py, qui rend
      245 entrées pour 244 fichiers classés.
      ④ Le dossier de sortie est créé sans qu'on le demande. Mesuré sur une racine
      ne portant qu'un fichier de workflow : le programme y crée un dossier
      gouvernance/ et y écrit SOCLE.csv. Un classement lancé sur un dossier qui
      n'est pas le dépôt y laisse donc une trace inattendue.
    ⑩ EFFET — ÉCRIT et ÉCRASE le fichier de sortie, par défaut
      <racine>/gouvernance/SOCLE.csv. CRÉE le dossier de ce fichier s'il manque.
      LANCE git en lecture seule, deux fois par racine ayant lancé un programme —
      mesuré : quatre lancements pour deux racines. LIT l'arbre et les programmes
      atteints. Affiche de dix à vingt lignes. Ne touche à aucun autre fichier,
      aucun accès réseau.
    ⑪ TERMINAISON — SORT DU PROGRAMME, et ne rend jamais la main : 0 quand le
      fichier est écrit, 2 quand il n'y avait rien à classer, 3 quand un fichier du
      périmètre est illisible. PEUT S'ARRÊTER AVANT sur une erreur non rattrapée :
      dossier de sortie impossible à créer, droits refusés, disque plein. Aucun de
      ses appels ne se termine de lui-même : `fabriquer`, `date_git` et `homonymes`
      rendent la main ou lèvent.
        [sort: oui]
    ⑫ DÉFINITIONS
      le socle : le programme programmes/FABRIQUER_LE_SOCLE.py et le fichier
        qu'il écrit, qui rangent chaque fichier d'une racine en VIVANT quand une
        chaîne d'appels y mène, en PRÉSUMÉ quand aucun lien n'est détecté dans un
        dossier qui fait autorité, et en DORMANT quand aucun lien n'est détecté
        ailleurs.
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe
        les fichiers — en général un clone du dépôt.
      une racine, ou fichier-racine : un fichier qui LANCE des programmes, soit un
        fichier de .github/workflows/, soit un fichier de prompts_taches/. Le mot
        sert donc à deux choses dans ce programme, le dossier et le fichier.
      un fantôme : un programme nommé par une racine et absent de l'arbre des
        fichiers.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
    
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle a tourné — rapport de boucle, rapport d'audit, cockpit, historique des mesures.
"""
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    racine = sys.argv[1]
    sortie = sys.argv[2] if len(sys.argv) > 2 else os.path.join(racine, "gouvernance", "SOCLE.csv")
    if not os.path.isdir(racine):
        print(f"CODE 2 — racine introuvable : {racine}"); sys.exit(2)
    try:
        lignes, fichiers_racines, sources, fantomes = fabriquer(racine)
    except SocleIllisible as e:
        print(f"CODE 3 — UN FICHIER DU PERIMETRE EST ILLISIBLE : {e}")
        print("  R-734 : un controle qui n a pas pu tourner rend un code NON NUL.")
        print("  RIEN N EST ECRIT — un socle partiel est pire qu un socle absent.")
        sys.exit(3)
    if fantomes:
        print(f"  ⚠️ {len(fantomes)} programme(s) nomme(s) par une racine et ABSENT(s) : "
              + ", ".join(fantomes))
    if lignes is None:
        print(f"CODE 2 — AUCUNE RACINE sous {racine} : ni workflow, ni prompts_taches.")
        print("  Une racine est ce qui LANCE un programme. Sans racine, aucune")
        print("  partition n est possible — et ce n est pas un defaut du socle.")
        sys.exit(2)
    os.makedirs(os.path.dirname(sortie), exist_ok=True)
    with open(sortie, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["# FABRIQUÉ par FABRIQUER_LE_SOCLE.py le "
                    + datetime.now(PARIS).strftime("%Y-%m-%d %H:%M") + " (Europe/Paris)"])
        # N1 de Cowork : « un ⚠️ que rien ne peut lire n'a pas d'existence ».
        # L'avertissement vivait dans l'affichage d'une exécution — c'est-à-dire
        # nulle part dès que la tâche est finie. Les racines entrent donc dans le
        # FICHIER, avec la date que git leur donne, pour qu'on puisse les relire.
        for _s in sources:
            _n = _s.split(" ", 1)[-1]
            _r = next((p for p in fichiers_racines if os.path.basename(p) == _n), _n)
            w.writerow([f"# RACINE ; {_r} ; dernier commit {date_git(racine, _r) or 'INCONNU'}"])
        w.writerow(["chemin", "etat", "pourquoi", "lu_par"])
        w.writerows(lignes)
    v = sum(1 for l in lignes if l[1] == "VIVANT")
    pr = sum(1 for l in lignes if l[1] == "PRESUME")
    do = sum(1 for l in lignes if l[1] == "DORMANT")
    print(f"  racine   : {racine}")
    # LE SOCLE DIT LA DATE, IL NE JUGE PAS DE LA FRAÎCHEUR — et il n'a plus de seuil.
    # N4 de Cowork, 12-09, et c'est la correction la plus nette de la journée :
    #   « tu n'as pas besoin d'un meilleur seuil, tu n'as pas besoin de seuil. »
    # J'avais écrit que la propriété « le relevé date d'avant la dernière dictée »
    # était inapplicable parce que rien au dépôt ne dit quand a eu lieu la dictée.
    # FAUX, et mesuré : le relevé enregistre `modifiee le` pour CHACUNE des douze
    # tâches. La donnée était là, douze fois. **Le contrôle n'est simplement pas du
    # ressort du socle — il ne peut pas voir une dictée faite après le relevé. Il est
    # du ressort de celui qui tient la liste des tâches.** Les sept jours sont donc
    # supprimés, pas atténués : un relevé de trois mois dont aucune tâche n'a bougé
    # est FRAIS, et le seuil l'aurait condamné à tort.
    if not sources:
        print("  sources  : aucune")
    for s_ in sources:
        _nom = s_.split(" ", 1)[-1]
        _rel = next((p for p in fichiers_racines if os.path.basename(p) == _nom), _nom)
        _d = date_git(racine, _rel)
        print(f"  source   : {s_}  · dernier commit : {_d or 'HORS DÉPÔT — date inconnue'}")
    # K7 — DEUX NATURES, JAMAIS UN TOTAL. « 48 vivants » melangeait ce qui est
    # MESURE et ce qui est DECRETE. Dire ce qu on ignore est honnete ; l additionner
    # a ce qu on sait ne l est pas.
    print(f"  {len(lignes)} fichiers")
    print(f"    VIVANTS  {v:>4}  — mesure : une chaine y mene")
    print(f"    PRESUMES {pr:>4}  — aucun lien detecte, CE QUI NE PROUVE RIEN")
    print(f"    DORMANTS {do:>4}  — aucun lien detecte, hors dossier d autorite")
    if pr or do:
        print(f"  >>> AUCUN RANGEMENT AUTOMATIQUE — ni des PRESUMES, ni des DORMANTS.")
        print(f"      Les deux portent la MEME mesure : aucun lien detecte. Seule la")
        print(f"      case du dossier les separe, et une case n est pas une preuve.")
    print(f"  ecrit : {sortie}")
    # LES HOMONYMES, NOMMES UN PAR UN — ne refuse rien, signale.
    _h = homonymes(lignes)
    if _h:
        print(f"\n  ⚠️  {len(_h)} NOM(S) PORTE(S) PAR PLUSIEURS FICHIERS — "
              f"l un recoit les ecritures, l autre est lu, et rien ne le dit :")
        for _n, _c in _h:
            print(f"     {_n}")
            for _x in _c:
                print(f"        {_x}")
    else:
        print("  aucun nom de fichier porte a deux endroits (hors archives et temoins)")
    sys.exit(0)


if __name__ == "__main__":
    main()
