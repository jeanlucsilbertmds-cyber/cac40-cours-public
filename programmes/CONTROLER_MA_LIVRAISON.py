#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Refuse une livraison qui ne porte pas ses preuves, et l horodate quand elle les porte.

① RÔLE — Décider si un travail part à la relecture ou s il est refusé, sans
  rien demander à la mémoire de celui qui livre. Le fichier contrôlé est un
  document de texte, `echanges/A_RELIRE.md`, qui porte le travail soumis. Le
  programme le lit, cherche quatre propriétés, et rend un code de sortie : 0 si
  la livraison peut partir, 1 sinon. Quand elle peut partir, il écrit en queue
  du document une ligne de contrôle portant l empreinte du texte accepté et
  l heure de Paris, par exemple « <!-- CONTROLE bcf4e3f0f4e62f81 ·
  2026-09-19 23:08 Paris --> », mesurée le 19-09-2026.

② CONTEXTE D APPEL — Lancé à la main, jamais par une tâche automatique. Trois
  manières.
  ① Le Chat, avant tout dépôt : c est le sixième des huit gestes du protocole
  de livraison écrit en tête de `gouvernance/REGISTRE_REGLES.md`.
  ② Le relecteur, avec l option « --verifier », qui relit sans rien écrire.
  ③ `programmes/EPREUVES_DU_GARDE_FOU.py`, qui lance ce programme en
  sous-processus sur neuf documents fabriqués dont il sait à l avance lesquels
  doivent être refusés, puis une soixantaine de fois encore pendant son
  sabotage.
  Aucune tâche du soir ne l appelle : mesuré le 19-09-2026, la recherche du nom
  du programme dans les fichiers de tâches du dossier `.github/workflows` n en
  rend aucune occurrence.

③ ENTRÉE — La ligne de commande. Un argument obligatoire, le chemin du document
  à contrôler ; une option facultative, « --verifier ». Sans argument, le
  programme affiche ce texte et sort en 1.

④ CONDITIONS D ENTRÉE — Le fichier doit exister et se lire en UTF-8. Il doit
  porter le repère « # R-740 » ou « R-740 — LES CINQ PASSES » : les passes se
  lisent après ce repère, et un document qui ne le porte pas est refusé sans
  autre examen. Hors option de relecture, il doit être accessible en écriture.
  Le dossier grand-parent du fichier est pris pour racine du dépôt : un document
  rangé ailleurs que dans un sous-dossier du dépôt fait tomber cette racine sur
  le dossier courant. Depuis le 30-09-2026, le dossier grand-parent du document
  doit aussi être un dépôt Git qui connaît la version officielle sous le nom
  `origin/main` : sinon la livraison est refusée (R-734).

⑤ SORTIE — Un code de sortie, et un compte rendu affiché. 0 quand les quatre
  propriétés sont portées · 1 à chaque refus. Le programme sort lui-même ; il ne
  rend la main à personne.

⑥ TRAITEMENT — ① lire le document · ② refuser si le repère des cinq passes est
  absent · ③ séparer les blocs de code qui portent la trace d une exécution de
  ceux qui ne portent que de la prose · ④ refuser si la première de ces
  exécutions n apparaît qu après les deux tiers du document · ⑤ relancer les
  commandes citées et refuser chaque ligne écrite que la commande ne rend pas ·
  ⑥ refuser plus d une ligne de contrôle · ⑦ refuser si l une des cinq passes
  manque · ⑧ refuser une passe de mandat inversé, de famille ou de régression
  qui ne porte aucune sortie capturée · ⑨ refuser une passe de non-éprouvé qui
  dit « rien » sans énumérer · ⑩ confronter au code les fiches des fonctions de
  TOUS les fichiers Python du dossier `programmes`, refuser celles que le code
  contredit, et refuser s il n y a aucun programme à confronter · ⑪ refuser
  toute fonction, à tous les niveaux, qui ne porte pas ses onze premiers
  éléments · ⑫ refuser
  toute affirmation de conformité qui n est ni citée, ni enfermée dans un bloc,
  ni précédée d une sortie capturée · ⑫bis (30-09-2026) refuser un programme dont
  le code diffère de la version officielle `origin/main` sans épreuve de `tests/`
  qui le désigne, et, pour une livraison qui modifie un programme, un piège de
  R-755 ③ sans sortie qui l écarte ; refuser si `origin/main` est introuvable ·
  ⑬ afficher le compte rendu, puis sortir en 1 s il y a un refus · ⑭ sinon calculer l empreinte du corps du document et,
  selon l option, la comparer à la ligne de contrôle déjà posée ou l écrire en
  queue.

⑦ UNITÉ — Un NOMBRE DE CARACTÈRES pour la taille du document affichée · des
  NOMBRES DE BLOCS de code · des NUMÉROS DE LIGNE pour les affirmations nues ·
  un NOMBRE DE MOTIFS de refus · une EMPREINTE de seize caractères
  hexadécimaux · des SECONDES pour le délai maximal de 120 laissé à chaque
  commande relancée. L horodatage de la ligne de contrôle est en heure de Paris.

⑧ POURQUOI — Jean-Luc, le 12-09-2026 : « Ce qui me coûte, ce sont tes défauts à
  toi : affirmer sans mesurer, énumérer au lieu de désigner, livrer sans les
  cinq passes. Ceux-là reviennent sur chaque sujet. » Mesuré sur cette seule
  journée : cinq corrections sur cinq cassées par le relecteur · un plan entier
  bâti sur un programme qui n existait pas · deux alertes données avant
  vérification, toutes deux fausses · un jeu d épreuves livré comme une preuve
  alors que trois de ses huit cas ne pouvaient pas rougir · la règle des cinq
  passes écrite le matin et enfreinte le soir même.
  Les règles qui imposent ces preuves — une règle qu on n applique pas reste au
  registre en donnant l illusion d un contrôle (R-738), et les cinq passes
  s affichent avec la livraison ou il n y a pas de livraison (R-740) — reposent
  sur un ENGAGEMENT, et un engagement ne survit pas à la session qui l a pris. Ce programme ne demande
  rien à la mémoire : il lit le fichier et il refuse. C est la règle de Jean-Luc
  — « rendre l erreur impossible plutôt que mieux relire » — appliquée au Chat.
  CE QU IL CONTRÔLE, ET RIEN D AUTRE, quatre propriétés dont aucune ne demande
  de juger : ① les cinq passes sont présentes, et celles du mandat inversé, de
  la famille et de la régression portent une sortie capturée ; ② la passe de
  mandat inversé nomme au moins un cas d attaque, pas seulement « rien trouvé » ;
  ③ la passe de non-éprouvé existe et n est pas vide, ce qui n a pas été éprouvé
  étant nommé un par un ; ④ toute affirmation de conformité s accompagne d une
  sortie d outil — les mots « identique », « conforme », « complet »,
  « vérifié », « prouvé » employés sans sortie de programme au-dessus sont les
  déclencheurs mesurés de la règle « citer, c est avoir ouvert » (R-720).
  CE QU IL NE CONTRÔLE PAS, ET C EST DIT : la VÉRITÉ de ce qui est écrit. Un
  bloc de code peut être faux. Ce programme vérifie que la preuve est LÀ, jamais
  qu elle est juste — c est le travail du relecteur, et il ne le remplace pas.

⑨ CE QUI CLOCHE — Quatre points relevés le 19-09-2026 ; les deux premiers sont
  RÉGLÉS le 20-09-2026 : ① hors d un dépôt Git, les contrôles qui lisent le code
  se taisaient sans le dire ; ② un fichier Python neuf était invisible tant qu il
  n était pas ajouté à l index de Git. **Leur cause commune en portait une
  troisième, mesurée le 20-09-2026 : un travail COMMITÉ ne différait plus de la
  version de référence de Git, et le contrôle ne regardait plus rien —
  commiter suffisait à le faire taire.** Le contrôle ne consulte plus Git. Les
  limites qui restent au contrôle des fiches sont détaillées au ⑨ de `main`.
  ③ Le contrôle des fiches ne regarde que les fonctions écrites au premier
  niveau du fichier, alors que celui des onze éléments parcourt tout l arbre.
  Mesuré sur le dossier `programmes` : 295 fonctions au premier niveau pour 329
  en tout, soit 34 fonctions imbriquées ou portées par une classe dont la fiche
  n est jamais confrontée au code.
  ④ Le calibrage interne du contrôle de l ordre des mesures n est appelé par
  personne : la recherche de son nom dans tout le dépôt ne rend que la ligne qui
  le définit et, jusqu'au 24-09-2026, la fiche que la photographie en tirait.

⑩ EFFET — RÉÉCRIT entièrement le document contrôlé quand il est accepté et que
  l option de relecture est absente : corps du texte, puis une ligne de contrôle
  portant l empreinte et l horodatage. RECOPIE le dépôt entier dans un dossier
  temporaire à chaque passage — 292 fichiers, 12 Mo, 0,04 seconde mesurés le
  19-09-2026 — et y EXÉCUTE les commandes python3 citées par le document, y
  compris en mode relecture. LIT tous les fichiers Python du dossier
  `programmes` pour confronter leurs fiches, sans consulter Git pour ce
  contrôle-là ; LANCE `git` en lecture pour comparer les programmes à la version
  officielle (depuis le 30-09-2026). Aucun autre fichier du dépôt n est touché, aucun accès réseau n est
  fait par le programme lui-même.

⑪ TERMINAISON — SORT DU PROGRAMME à chaque issue, sans jamais rendre la main.
  Code 1 : aucun argument · fichier introuvable · repère des cinq passes
  absent · au moins un motif de refus · ligne de contrôle absente ou empreinte
  différente en mode relecture. Code 0 : livraison acceptée, ou relecture qui
  retrouve l empreinte. Un de ses appels peut ne pas revenir : les commandes
  citées sont relancées dans des processus séparés, chacun borné à 120 secondes.

⑫ DÉFINITIONS
  une livraison : le document `echanges/A_RELIRE.md`, qui porte le travail
    soumis à la relecture
  le Chat : la conversation qui rédige la gouvernance du projet et dépose ses versions
  le relecteur : celui qui relit le travail de l autre, ici Cowork
  une passe : l une des cinq vérifications qu une livraison doit afficher —
    mandat inversé, famille, régression, non éprouvé, lien (R-740)
  une sortie capturée : un bloc de texte qui porte la trace d une exécution —
    une invite de commande ou un code de sortie — et non de la prose
  une ligne de contrôle : la ligne que ce programme pose en queue d un document
    accepté, portant l empreinte de seize caractères du texte validé
  une fiche : le texte explicatif écrit en tête d'une fonction, dans le code, qui porte ses onze rubriques.
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
"""

import hashlib, os, re, sys
from datetime import datetime
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")

PASSES = {
    "①": ["mandat inversé", "mandat inverse"],
    "②": ["famille"],
    "③": ["régression", "regression"],
    "④": ["non éprouvé", "non eprouve", "pas éprouvé", "pas eprouve"],
    "⑤": ["lien"],
}

# Les mots qui annoncent une conformité. Relevés dans les préférences de Jean-Luc :
# « c'est identique / complet / conforme / fidèle » sont des ALARMES, jamais des
# conclusions — employés sans source ouverte juste avant, ils annoncent une
# supposition déguisée en fait.
CONFORMITE = re.compile(
    r"\b(identique|conforme|complet|complète|fidèle|vérifié|verifie|prouvé|prouve|"
    r"inchangé|inchange|aucun écart|aucun ecart|tous? passent?)\b", re.I)


def blocs_captures(texte):
    """Sépare les blocs de code qui portent une exécution de ceux qui portent de la prose.

    ① RÔLE — Donner au reste du programme la seule chose qui distingue une
      preuve d une assurance : un bloc de code n est une preuve que s il porte la
      trace d une EXÉCUTION. Tout le contrôle s appuie sur cette séparation — une
      passe n est prouvée que par un bloc du premier tas, et une affirmation de
      conformité n est couverte que par un bloc du premier tas.
    ② CONTEXTE D APPEL — Deux appelants, tous deux dans ce fichier. Le contrôle
      de l ordre des mesures l appelle pour savoir où se trouve la première vraie
      mesure du document. La fonction principale l appelle une fois, sur le texte
      entier, et se sert des deux listes rendues pendant tout le reste du contrôle.
    ③ ENTRÉE — `texte` : le contenu entier du document de livraison, tel qu il a
      été lu sur le disque. Les deux appels lui passent le texte complet, jamais
      un extrait.
    ④ CONDITIONS D ENTRÉE — Du texte. Un document sans aucune barrière de code ne
      la fait pas tomber : elle rend alors deux listes vides.
    ⑤ SORTIE — DEUX valeurs : la liste des blocs qui portent une exécution, puis
      la liste des blocs de prose. Chaque bloc est donné par le couple de sa
      position de début et de sa position de fin dans le texte reçu.
      [rend: 2]
    ⑥ TRAITEMENT — ① parcourir le texte et relever chaque couple de barrières de
      code, les trois accents graves · ② chercher dans le corps du bloc la trace
      d une exécution : une ligne ouverte par une invite « $ » suivie d un mot,
      une ligne ouverte par python3, git, grep, curl, sha256sum, wc ou ls suivi
      d un mot, une mention « CODE » suivie d un nombre, les mots « code de
      sortie » suivis d un nombre, ou une flèche suivie du mot CODE et d un
      nombre · ③ ranger le bloc dans le premier tas s il porte l une de ces
      traces, dans le second sinon.
    ⑦ UNITÉ — Des POSITIONS EN CARACTÈRES dans le texte reçu, comptées à partir
      de 0.
    ⑧ POURQUOI — Un bloc de code n est pas une preuve du seul fait qu il est
      encadré. Le 12-09-2026, le relecteur a montré que six caractères — deux fois
      trois accents graves — suffisaient à la fois à CACHER quatre affirmations de
      conformité au contrôle qui les cherche, ET à faire compter ce même bloc
      comme leur preuve. La propriété retenue est la règle « ce qui se mesure ne
      s écrit jamais à la main » (R-728) appliquée à la livraison : de la prose
      entre deux barrières n est pas une mesure, quelle que soit son assurance.
      Le premier motif était plus large et acceptait une simple flèche, le mot
      « octets » et n importe quelle ligne de la forme « mot : valeur » ; il a été
      resserré aux invites de commande et aux codes de sortie, et à rien d autre.
      Exemple mesuré le 19-09-2026 sur un texte portant deux blocs, le premier
      contenant « une phrase » et le second l invite « $ python3 x.py » puis
      « ok » : la fonction rend 1 bloc d exécution et 1 bloc de prose.
    ⑨ CE QUI CLOCHE — Les barrières sont appariées deux par deux, sans vérifier
      qu elles ouvrent une ligne ni qu elles vont par paires. Mesuré le
      19-09-2026 sur un texte portant trois barrières — un bloc refermé, du texte,
      puis une barrière jamais refermée : la fonction rend un seul bloc, de la
      position 0 à la position 25, et le texte resté ouvert après la troisième
      barrière n appartient à aucun des deux tas. Une livraison dont un bloc n est
      pas refermé voit donc une partie de son texte échapper aux deux contrôles
      qui s appuient sur ces listes.
    ⑩ EFFET — Ne change rien : elle lit le texte reçu et rend deux listes. Aucun
      fichier, aucun réseau, aucun affichage.
    ⑪ TERMINAISON — Rend la main à tous les coups. Elle n emploie que la recherche
      de motif du langage, et aucun de ses appels ne peut rester en attente.
      [sort: non]
    ⑫ DÉFINITIONS
      une livraison : le document `echanges/A_RELIRE.md`, qui porte le travail
        soumis à la relecture
      une sortie capturée : un bloc de texte qui porte la trace d une exécution —
        une invite de commande ou un code de sortie — et non de la prose
      une passe : l une des cinq vérifications qu une livraison doit afficher —
        mandat inversé, famille, régression, non éprouvé, lien (R-740)
      le relecteur : celui qui relit le travail de l autre, ici Cowork
    """
    captures, proses = [], []
    for m in re.finditer(r"```.*?```", texte, re.S):
        corps = m.group(0)
        # Q4 : « une flèche suffit à faire d'un bloc de prose une preuve ». Le motif
        # acceptait `->`, `octets`, et surtout n'importe quelle ligne « mot : valeur ».
        # UNE MESURE PORTE LA TRACE D'UNE EXÉCUTION, PAS UNE PONCTUATION :
        # une invite de commande, ou un code de sortie explicite. Rien d'autre.
        execute = bool(re.search(
            r"^\s*\$ \S|^\s*(python3|git|grep|curl|sha256sum|wc|ls) \S|"
            r"^\s*CODE\s*(RÉEL|REEL)?\s*:?\s*-?\d|code de sortie\s*:?\s*-?\d|"
            r"->\s*(CODE|code)\s*-?\d",
            corps, re.M))
        (captures if execute else proses).append((m.start(), m.end()))
    return captures, proses


def dans_zone(pos, zones):
    """Dit si une position du document tombe à l intérieur d un bloc de code relevé.

    ① RÔLE — Permettre au contrôle des affirmations de conformité de laisser
      tranquille ce qui est écrit DANS un bloc de code. Un mot enfermé entre deux
      barrières est du texte rapporté, pas une affirmation de l auteur.
    ② CONTEXTE D APPEL — La fonction principale, deux fois par mot de conformité
      trouvé dans le document : une fois contre la liste des blocs qui portent une
      exécution, une fois contre la liste des blocs de prose. Jamais appelée
      ailleurs.
    ③ ENTRÉE — `pos` : la position, en caractères, du mot examiné, comptée depuis
      le début du document · `zones` : la liste des blocs à examiner, chacun donné
      par le couple de sa position de début et de sa position de fin.
    ④ CONDITIONS D ENTRÉE — Aucune. Une liste de zones vide ne la fait pas tomber :
      elle rend faux.
    ⑤ SORTIE — UNE valeur : vrai si la position tombe dans l une des zones, bornes
      comprises ; faux sinon.
      [rend: 1]
    ⑥ TRAITEMENT — ① parcourir les zones · ② rendre vrai dès qu une zone contient
      la position, bornes comprises · ③ rendre faux si aucune ne la contient.
    ⑦ UNITÉ — Des POSITIONS EN CARACTÈRES dans le document, comptées à partir de 0.
    ⑧ POURQUOI — Un relecteur reproduit les livraisons fautives qu il casse, et il
      ne peut pas citer ce qu il casse sans employer les mots qu on lui reproche.
      Le choix est assumé dans ce programme : on perd la détection d un auteur qui
      cacherait ses affirmations dans un bloc, mais ce bloc ne lui sert plus de
      preuve depuis que seul un bloc portant la trace d une exécution en est une.
      Exemple mesuré le 19-09-2026 : la position 5 dans la zone qui va de 0 à 10
      rend vrai, la position 11 rend faux, et une liste de zones vide rend faux.
    ⑨ CE QUI CLOCHE — Rien vu. Les deux bornes sont prises au sens large, ce qui
      est le comportement voulu : la barrière qui ouvre le bloc et celle qui le
      ferme appartiennent au bloc.
    ⑩ EFFET — Ne change rien. Aucun fichier, aucun réseau, aucun affichage.
    ⑪ TERMINAISON — Rend la main à tous les coups. Aucun de ses appels ne peut
      rester en attente.
      [sort: non]
    ⑫ DÉFINITIONS
      une livraison : le document `echanges/A_RELIRE.md`, qui porte le travail
        soumis à la relecture
      le relecteur : celui qui relit le travail de l autre, ici Cowork
    
      la trace : la liste des sources avec leur etat — LU, ABSENT ou ILLISIBLE — et un detail chiffre, affichee en pied de page.
      un bloc : une suite de lignes qui se suivent dans le texte et dont les dates décroissent sans trou plus grand que six jours.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    return any(a <= pos <= b for a, b in zones)


def preuve_proche(texte, pos, captures, fenetre=900):
    """Dit si une affirmation de conformité est précédée, assez près, d une mesure.

    ① RÔLE — Trancher la seule chose qui distingue « le résultat est identique »
      d une supposition : une sortie de programme lisible juste avant la phrase.
    ② CONTEXTE D APPEL — La fonction principale, une fois par mot de conformité
      qui n est ni cité entre délimiteurs ni enfermé dans un bloc de code. Jamais
      appelée ailleurs.
    ③ ENTRÉE — `texte` : le document entier · `pos` : la position, en caractères,
      du mot de conformité examiné · `captures` : la liste des blocs portant la
      trace d une exécution, chacun donné par le couple de sa position de début et
      de sa position de fin · `fenetre` : la largeur, en caractères, de la zone
      examinée avant le mot ; l unique appel ne la donne pas et laisse la valeur
      écrite dans la signature, soit 900.
    ④ CONDITIONS D ENTRÉE — Aucune. Une liste de blocs vide ne la fait pas tomber :
      elle rend faux.
    ⑤ SORTIE — UNE valeur : vrai si un bloc d exécution se termine dans la fenêtre
      qui précède la position examinée, faux sinon.
      [rend: 1]
    ⑥ TRAITEMENT — ① calculer le début de la fenêtre, soit la position moins la
      largeur, sans descendre sous le début du document · ② rendre vrai si la
      position de FIN d un bloc d exécution tombe entre ce début et la position
      examinée.
    ⑦ UNITÉ — Des POSITIONS et une LARGEUR EN CARACTÈRES.
    ⑧ POURQUOI — Une preuve est ici une PROXIMITÉ, pas un lien : rien, dans un
      document de texte, ne relie une mesure à la phrase qu elle fonde. Le
      relecteur l a dit le 12-09-2026, et la faiblesse est reconnue — un chiffre
      vrai sur un autre sujet légitime l affirmation qui le suit, « le dépôt porte
      173 fichiers » validant « le résultat est identique ». Ce qui a changé ce
      jour-là : un chiffre nu ne suffit plus, il faut une sortie de programme.
    ⑨ CE QUI CLOCHE — Deux points.
      ① La largeur de la fenêtre est un COMPTE, alors qu un garde-fou porte sur une
      propriété et jamais sur un compte (R-745). Mesuré le 19-09-2026 avec un bloc
      d exécution qui se termine à la position 10 : une affirmation posée à la
      position 910 est déclarée prouvée, la même affirmation posée à la position
      911 est déclarée nue. Un paragraphe de plus inséré entre la mesure et la
      phrase fait basculer le verdict sans que rien n ait changé au fond.
      ② Le premier paramètre n est jamais employé. Le corps de la fonction ne lit
      que la position, la liste des blocs et la largeur ; le document reçu ne sert
      à rien. Un lecteur qui la modifie peut croire qu elle examine le texte situé
      entre la mesure et l affirmation, ce qu elle ne fait pas.
    ⑩ EFFET — Ne change rien. Aucun fichier, aucun réseau, aucun affichage.
    ⑪ TERMINAISON — Rend la main à tous les coups. Aucun de ses appels ne peut
      rester en attente.
      [sort: non]
    ⑫ DÉFINITIONS
      une sortie capturée : un bloc de texte qui porte la trace d une exécution —
        une invite de commande ou un code de sortie — et non de la prose
      le relecteur : celui qui relit le travail de l autre, ici Cowork
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
    
      un garde-fou : une limite qui, franchie, fait cesser a la strategie de prendre position tout en continuant a la mesurer.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    debut = max(0, pos - fenetre)
    return any(debut <= b <= pos for a, b in captures)


def mesure_avant_ecriture(texte):
    """Refuse un document dont la première mesure n arrive qu après les deux tiers du texte.

    ① RÔLE — Faire respecter la règle « la mesure vient avant l écriture, jamais
      après » (R-744) sur la seule trace que cet ordre laisse dans un fichier : la
      PLACE de la première sortie de programme. Un document qui mesure d abord
      pose ses sorties là où elles fondent le propos ; un document dont la première
      sortie n arrive qu à la fin a été écrit en entier avant d être mesuré.
    ② CONTEXTE D APPEL — Deux appelants, tous deux dans ce fichier. La fonction
      principale, une fois par contrôle, sur le document entier. Et le calibrage
      interne, qui lui soumet quatre documents fabriqués dont on sait à l avance
      lesquels doivent être refusés.
    ③ ENTRÉE — `texte` : le contenu entier du document, tel qu il a été lu sur le
      disque.
    ④ CONDITIONS D ENTRÉE — Du texte. Un document court ou sans aucun bloc de code
      ne la fait pas tomber.
    ⑤ SORTIE — UNE valeur : la phrase de refus quand la première sortie capturée
      apparaît après 66 % du document, et une valeur vide dans tous les autres cas.
      La phrase de refus nomme la part atteinte, par exemple « la premiere SORTIE
      CAPTUREE apparait a 87% du document ».
      [rend: 1]
    ⑥ TRAITEMENT — ① compter les lignes du document et ne rien dire s il en porte
      moins de 40 · ② relever les blocs qui portent la trace d une exécution ·
      ③ ne rien dire s il n y en a aucun · ④ calculer la part du document qui
      précède le premier de ces blocs · ⑤ rendre la phrase de refus si cette part
      dépasse 66 %.
    ⑦ UNITÉ — Un NOMBRE DE LIGNES pour le seuil de 40, et une PART DU DOCUMENT
      COMPTÉE EN CARACTÈRES, exprimée en pourcents, pour le seuil de 66 %.
    ⑧ POURQUOI — Personne ne peut savoir, en lisant un fichier, dans quel ordre les
      gestes ont été faits. Ce contrôle ne juge donc aucune intention : il lit une
      propriété de FORME, vérifiable. Un document de moins de 40 lignes n a pas
      d ordre à lire, d où le seuil.
      La première version relevait les barrières de code et prenait la première
      pour une mesure. Le 13-09-2026, le relecteur a montré que trois lignes de
      PROSE entre deux barrières, collées en tête, suffisaient à faire passer un
      document que le programme venait de refuser. Le relevé des blocs d exécution,
      écrit vingt lignes plus haut dans ce même fichier, portait déjà la propriété :
      un contrôle plus faible avait été réécrit à côté de celui qui savait déjà.
    ⑨ CE QUI CLOCHE — Un document long qui ne porte AUCUNE mesure passe sans un
      mot. Mesuré le 19-09-2026 sur soixante lignes de prose sans un seul bloc de
      code : la fonction ne rend rien, donc ce contrôle accepte le document. La
      règle qu elle sert est pourtant « mesurer avant d écrire » : zéro mesure est
      le cas le plus défavorable, et c est celui qu elle laisse passer. Le refus
      vient alors d ailleurs — du contrôle des cinq passes — mais seulement pour la
      partie du document qui suit le repère des passes.
      Et ses deux seuils, 40 lignes et 66 %, sont des COMPTES, ce qu un garde-fou
      ne devrait pas porter (R-745).
    ⑩ EFFET — Ne change rien. Aucun fichier, aucun réseau, aucun affichage.
    ⑪ TERMINAISON — Rend la main à tous les coups. Son seul appel, le relevé des
      blocs de code, rend toujours la main lui aussi.
      [sort: non]
    ⑫ DÉFINITIONS
      une sortie capturée : un bloc de texte qui porte la trace d une exécution —
        une invite de commande ou un code de sortie — et non de la prose
      une passe : l une des cinq vérifications qu une livraison doit afficher —
        mandat inversé, famille, régression, non éprouvé, lien (R-740)
      le relecteur : celui qui relit le travail de l autre, ici Cowork
    
      le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
      un garde-fou : une limite qui, franchie, fait cesser a la strategie de prendre position tout en continuant a la mesurer.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    n = len(texte.split("\n"))
    if n < 40:
        return None
    # ON COMPTE LES SORTIES, PAS LES BARRIERES — cassure de Cowork, 13-09-2026.
    # Ma premiere version reperait les ``` et prenait la premiere pour une mesure.
    # **Trois lignes de PROSE entre deux accents graves, collees en tete, et le
    # garde-fou laissait passer le document qu il venait de refuser.**
    # `blocs_captures`, vingt lignes plus haut, porte deja la propriete : un bloc
    # n est une preuve que s il porte la trace d une EXECUTION. Elle est nee de la
    # P2 du 12-09 — « six caracteres desarment le controle ». **J avais reecrit un
    # controle plus faible a cote de celui qui savait deja.**
    # `blocs_captures` rend un COUPLE : les captures, puis les blocs de prose.
    # Mon premier appel dépliait le couple comme une liste — et levait.
    caps, _proses = blocs_captures(texte)
    if not caps:
        return None
    debut = min(d for d, _f in caps) / max(1, len(texte))
    if debut > 0.66:
        return (f"R-744 — la premiere SORTIE CAPTUREE apparait a {debut:.0%} du document : "
                f"le propos est ecrit AVANT la premiere mesure")
    return None


def sortie_rejouee(texte, base="."):
    """Relance les commandes citées et compare leur vraie sortie à ce qui est écrit.

    ① RÔLE — Attraper une sortie de programme fabriquée. C est le seul contrôle du
      programme qui ne juge pas l apparence d un texte : il exécute la commande et
      compare. Les autres jugeaient une barrière, une invite, une longueur — et
      tous se contournent par un texte mieux écrit.
    ② CONTEXTE D APPEL — La fonction principale, une fois par contrôle, après le
      contrôle de l ordre des mesures et avant celui des cinq passes. Jamais
      appelée ailleurs.
    ③ ENTRÉE — `texte` : le contenu entier du document · `base` : le dossier depuis
      lequel les commandes seront relancées ; l unique appel lui passe la racine du
      dépôt, déduite en remontant de deux dossiers depuis le fichier contrôlé, et
      le dossier courant quand cette racine ne porte pas de sous-dossier de
      programmes.
    ④ CONDITIONS D ENTRÉE — Le dossier reçu doit pouvoir être recopié. Il faut
      pouvoir créer un dossier temporaire et lancer des processus.
    ⑤ SORTIE — TROIS valeurs : la liste des commandes dont toutes les lignes
      écrites se retrouvent dans la vraie sortie · la liste des commandes
      fabriquées, chacune donnée avec la première ligne écrite qui ne s y retrouve
      pas · la liste des commandes qui n ont pas pu être relancées. Quand la copie
      du dépôt échoue, les deux premières listes sont vides et la troisième porte
      la seule mention « copie impossible — RIEN N A ETE REJOUE ».
      [rend: 3]
    ⑥ TRAITEMENT — ① recopier le dossier reçu dans un dossier temporaire, en
      laissant de côté l historique Git, les caches de Python et le dossier de
      travail du site · ② parcourir les lignes du document et retenir celles qui
      sont exactement une invite « $ » suivie d une commande python3, sans
      redirection ni enchaînement · ③ mettre de côté, en les nommant, celles qui
      portent un guillemet ou l option d exécution directe · ④ lancer la commande
      dans la copie, avec un délai maximal de 120 secondes · ⑤ relever les lignes
      écrites sous l invite, jusqu à la prochaine invite ou la fin du bloc ·
      ⑥ ranger la commande parmi les fabriquées si l une de ces lignes ne se
      retrouve pas dans la vraie sortie, espaces mis à part, et parmi les vérifiées
      sinon · ⑦ effacer la copie.
    ⑦ UNITÉ — Des SECONDES pour le délai maximal de 120. Le reste est un NOMBRE DE
      COMMANDES.
    ⑧ POURQUOI — Le 13-09-2026, le Chat a écrit QUATRE FOIS, sous une invite
      réelle, « la sortie en tête est une vraie capture — R-744 ne mord pas ». Le
      programme n écrit jamais cette phrase : c était une réponse fabriquée,
      présentée comme une mesure, dans le document même qui instaurait « mesurer
      avant d écrire ».
      La relance se fait sur une COPIE et jamais dans le dépôt. Le 14-09-2026,
      lancé sur un document qui citait ce garde-fou appliqué au fichier de
      livraison, le contrôle a RÉÉCRIT ce fichier et changé son empreinte. Un
      contrôle qui modifie ce qu il contrôle fabrique l état qu il mesure.
      La copie est bon marché : mesurée le 19-09-2026, elle porte 292 fichiers et
      12 Mo, et prend 0,04 seconde, l historique Git étant laissé de côté.
    ⑨ CE QUI CLOCHE — Trois points.
      ① Une commande citée qui n est pas un python3 n est ni relancée ni signalée.
      Mesuré le 19-09-2026 sur un document citant « $ grep -rn toto programmes/ »
      suivi de « aucune occurrence » : les trois listes rendues sont vides. Le
      texte d origine de la fonction promettait pourtant que ce qui n a pas pu être
      vérifié se dit. La passe qui demande de chercher le même défaut ailleurs est
      la première concernée, puisqu elle s écrit le plus souvent avec une recherche
      de texte.
      ② Une commande qui ne peut pas se relancer est accusée d être fabriquée.
      Mesuré le 19-09-2026 sur un document citant « $ python3 programmes/PAS_LA.py »
      suivi de « ok » : la commande est rangée parmi les FABRIQUÉES, et la
      livraison est refusée. Un programme déplacé, renommé ou supprimé depuis la
      mesure suffit donc à faire accuser une sortie parfaitement vraie.
      ③ Une invite sans aucune ligne écrite dessous disparaît des trois listes.
      Mesuré le 19-09-2026 sur un bloc ne portant que l invite « $ python3
      programmes/CONTRATS_DES_FICHIERS.py . » : les trois listes sont vides, alors
      que la commande a bien été lancée. Le compte rendu affiché sous-estime donc
      ce qui a été relancé.
    ⑩ EFFET — CRÉE un dossier temporaire à chaque appel, y RECOPIE le dossier reçu
      en entier, puis l efface à la fin. LANCE des processus : ceux que le document
      cite, avec les droits de celui qui contrôle. N écrit rien dans le dépôt et
      n affiche rien elle-même.
    ⑪ TERMINAISON — Rend la main avec ses trois listes. Chaque commande relancée
      porte un délai maximal de 120 secondes, au-delà duquel elle est rangée parmi
      celles qui n ont pas pu être relancées : aucun appel ne peut la retenir
      indéfiniment.
      [sort: non]
    ⑫ DÉFINITIONS
      une livraison : le document `echanges/A_RELIRE.md`, qui porte le travail
        soumis à la relecture
      le Chat : la conversation qui rédige la gouvernance du projet et dépose ses versions
      une passe : l une des cinq vérifications qu une livraison doit afficher —
        mandat inversé, famille, régression, non éprouvé, lien (R-740)
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
    
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      un bloc : une suite de lignes qui se suivent dans le texte et dont les dates décroissent sans trou plus grand que six jours.
"""
    import re as _re, subprocess as _sp, shlex as _shlex, shutil as _sh, tempfile as _tf
    # ON REJOUE SUR UNE COPIE, JAMAIS DANS LE DEPOT — cassure de Cowork, 14-09-2026.
    # Mesure : lance sur un document qui cite `CONTROLER_MA_LIVRAISON.py
    # echanges/A_RELIRE.md`, le controle a REECRIT ce fichier. **L empreinte a
    # change.** Un controle qui modifie ce qu il controle est pire qu un controle
    # absent : il fabrique l etat qu il mesure.
    # La copie exclut `.git` — 9,3 Mo, 0,044 s sur clone neuf (sa mesure).
    verifiees, fabriquees, ignorees = [], [], []
    _copie = _tf.mkdtemp(prefix="controle_")
    try:
        _sh.copytree(base, os.path.join(_copie, "d"),
                     ignore=_sh.ignore_patterns(".git", "__pycache__", "_site_travail"),
                     dirs_exist_ok=True)
        base = os.path.join(_copie, "d")
    except Exception:
        _sh.rmtree(_copie, ignore_errors=True)
        return [], [], ["copie impossible — RIEN N A ETE REJOUE"]
    lignes = texte.split("\n")
    for i, l in enumerate(lignes):
        m = _re.match(r"^\$ (python3 [^\n|><&;]+)$", l.strip())
        if not m:
            continue
        cmd = m.group(1).strip()
        if "-c " in cmd or '"' in cmd or "'" in cmd:
            ignorees.append(cmd[:60]); continue
        try:
            r = _sp.run(_shlex.split(cmd), capture_output=True, text=True,
                        errors="replace", timeout=120, cwd=base)
        except Exception:
            ignorees.append(cmd[:60]); continue
        vraie = (r.stdout + r.stderr)
        # les lignes ecrites sous l invite, jusqu a la prochaine invite ou la fin du bloc
        ecrites = []
        for j in range(i + 1, len(lignes)):
            x = lignes[j]
            if x.strip().startswith("$ ") or x.strip().startswith("```"):
                break
            if x.strip():
                ecrites.append(x.strip())
        if not ecrites:
            continue
        # UNE LIGNE ECRITE DOIT SE RETROUVER DANS LA VRAIE SORTIE, aux espaces pres
        nu = lambda z: " ".join(z.split())
        vn = nu(vraie)
        absentes = [e for e in ecrites if nu(e) and nu(e) not in vn]
        if absentes:
            fabriquees.append((cmd[:52], absentes[0][:64]))
        else:
            verifiees.append(cmd[:52])
    _sh.rmtree(_copie, ignore_errors=True)
    return verifiees, fabriquees, ignorees


def _calibrage_r744():
    """Éprouve le contrôle de l ordre des mesures sur quatre documents fabriqués.

    ① RÔLE — Vérifier que le contrôle de l ordre des mesures refuse ce qu il doit
      refuser ET laisse passer ce qu il doit accepter. Un jeu d épreuves qui ne
      porte que le vrai et le faux ne voit pas le contournement ; celui-ci porte
      aussi le cas du contournement et celui du document court.
    ② CONTEXTE D APPEL — Aucun appelant. Mesuré le 19-09-2026 : la recherche du nom
      de cette fonction dans tout le dépôt ne rend que la ligne qui la définit et,
      jusqu'au 24-09-2026, la fiche que la photographie en tirait. Elle ne tourne donc que si quelqu un
      la lance à la main depuis une session Python.
    ③ ENTRÉE — Aucun paramètre. Elle fabrique elle-même ses quatre documents.
    ④ CONDITIONS D ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : vrai si les quatre cas rendent le verdict attendu, faux
      dès qu un seul tombe à côté. Le détail part à l affichage.
      [rend: 1]
    ⑥ TRAITEMENT — ① fabriquer un bloc de sortie d exécution, un bloc de prose et
      un corps de soixante lignes · ② bâtir quatre documents : la sortie à la fin
      qui doit être refusée, la sortie en tête qui doit passer, la prose en tête
      avec la sortie au bout qui doit être refusée, et un document de trois lignes
      qui doit passer · ③ soumettre chacun au contrôle de l ordre des mesures ·
      ④ afficher pour chacun le verdict obtenu et s il est juste · ⑤ rendre vrai si
      les quatre le sont.
    ⑦ UNITÉ — Un NOMBRE DE CAS.
    ⑧ POURQUOI — Le troisième cas est celui que le relecteur a trouvé le
      13-09-2026 : un document qui doit échouer, auquel on ajoute trois lignes de
      prose entre accents graves en tête. Sans lui, le jeu d épreuves restait vert
      sur un contrôle qu on venait de contourner. Le quatrième cas vérifie que le
      contrôle ne mord pas sur un document court, sans quoi il refuserait tout.
      Mesuré le 19-09-2026, lancée à la main : les quatre cas rendent le verdict
      attendu et la fonction rend vrai.
    ⑨ CE QUI CLOCHE — Personne ne l appelle, donc elle ne protège rien. Elle a été
      écrite pour que le contrôle de l ordre des mesures ne s affaiblisse pas en
      silence, et elle ne tourne ni au dépôt, ni dans les épreuves du garde-fou,
      qui lancent le programme de l extérieur et ne peuvent donc pas atteindre une
      fonction interne. Le jour où le contrôle qu elle éprouve cessera de mordre,
      rien ne rougira.
    ⑩ EFFET — Affiche quatre lignes, une par cas. N écrit aucun fichier, ne touche
      pas au réseau.
    ⑪ TERMINAISON — Rend la main à tous les coups. Son seul appel, le contrôle de
      l ordre des mesures, rend toujours la main lui aussi.
      [sort: non]
    ⑫ DÉFINITIONS
      le garde-fou : le programme `CONTROLER_MA_LIVRAISON.py`, qui accepte ou refuse un travail avant qu il parte à la relecture
      une sortie capturée : un bloc de texte qui porte la trace d une exécution —
        une invite de commande ou un code de sortie — et non de la prose
      le relecteur : celui qui relit le travail de l autre, ici Cowork
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
    
      la fiche : la ligne d'une stratégie au registre des stratégies `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte acceptée, son horizon et son univers
      la photographie : un document qui décrivait chaque programme et chaque fonction de l'écosystème, abandonné le 24-09-2026 et rangé aux archives (A-452).
      le détail : le fichier `registre_experiences.csv`, une ligne par expérience
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    sortie = "```\n$ python3 mesure.py\nresultat : 42\n```\n"
    prose = "```\nune phrase\nune autre\nune troisieme\n```\n"
    corps = "\n".join(f"phrase {k}" for k in range(60))
    cas = [
        ("A  vraie sortie a la fin        DOIT ECHOUER", corps + "\n" + sortie, True),
        ("B  vraie sortie en tete         DOIT PASSER ", sortie + "\n" + corps, False),
        ("C  prose en tete, sortie au bout DOIT ECHOUER", prose + "\n" + corps + "\n" + sortie, True),
        ("D  document court                DOIT PASSER ", "trois lignes\nseulement\nici", False),
    ]
    ok = True
    for nom, texte, doit_echouer in cas:
        r = mesure_avant_ecriture(texte)
        juste = bool(r) == doit_echouer
        ok = ok and juste
        print(f"  {nom} -> {'REFUSE' if r else 'passe'}  {'OK' if juste else '*** FAUX ***'}")
    return ok


MARQUEUR = r"^<!-- CONTROLE ([0-9a-f]{16}) [^\n]*-->$"


def _corps_et_marqueurs(texte):
    """Sépare le corps d une livraison de sa ligne de contrôle, et compte ces lignes.

    ① RÔLE — Faire porter l empreinte sur le texte livré, et sur rien d autre. Sans
      cette séparation, l empreinte engloberait la ligne de contrôle que le
      programme vient lui-même de poser, et deux passages de suite ne donneraient
      jamais la même valeur.
    ② CONTEXTE D APPEL — La fonction principale, une fois, après que tous les refus
      ont été examinés et juste avant le calcul de l empreinte. Jamais appelée
      ailleurs.
    ③ ENTRÉE — `texte` : le contenu entier du document, tel qu il a été lu sur le
      disque.
    ④ CONDITIONS D ENTRÉE — Du texte. Un document vide ou sans aucune ligne de
      contrôle ne la fait pas tomber.
    ⑤ SORTIE — DEUX valeurs : le corps à hacher, puis le nombre de lignes de
      contrôle trouvées. Le corps est le texte privé de sa ligne de contrôle de
      queue et de ses sauts de ligne finaux quand la dernière ligne de contrôle
      ferme le document ; c est le texte ENTIER, inchangé, quand du texte non vide
      la suit ; et c est le texte privé de ses seuls sauts de ligne finaux quand il
      n y a aucune ligne de contrôle.
      [rend: 2]
    ⑥ TRAITEMENT — ① relever les lignes qui sont entièrement une ligne de contrôle ·
      ② s il n y en a aucune, rendre le texte privé de ses sauts de ligne finaux et
      le nombre zéro · ③ sinon regarder ce qui suit la dernière : s il reste du
      texte non vide, rendre le texte entier et le nombre trouvé · ④ sinon, rendre
      tout ce qui précède cette dernière ligne, privé de ses sauts de ligne finaux,
      et le nombre trouvé.
    ⑦ UNITÉ — Un NOMBRE DE LIGNES DE CONTRÔLE.
    ⑧ POURQUOI — L ancienne écriture retirait la ligne de contrôle par un motif qui
      autorisait le point à avaler les retours à la ligne. Le 14-09-2026, le
      relecteur a mesuré ce que cela donnait : une ligne de contrôle insérée en
      colonne 0 à la neuvième ligne faisait tomber TOUT le reste dans le motif, et
      sur une livraison de 180 lignes le corps haché n en gardait plus que 8. Les
      172 autres — chiffres du radar et verdict de non-régression compris —
      n étaient couvertes par rien, et le programme annonçait « validée et
      intacte ».
      La propriété retenue : la ligne de contrôle est la DERNIÈRE ligne, et elle est
      SEULE. Une ligne de contrôle qui n est pas en queue ne ferme rien ; elle reste
      donc dans le corps, change l empreinte, et se voit.
      Le cas du document sans aucune ligne de contrôle a coûté un tour de relecture
      entier : à l écriture il n y a pas encore de ligne de contrôle, et ce chemin
      rendait le texte AVEC son saut de ligne final, alors qu à la lecture le corps
      en était privé. La même fonction rendait deux corps différents, et toute
      première validation était ensuite déclarée falsifiée — ligne de contrôle
      écrite 4443bff7b99ee621, relue 235233a20260f0dd.
      Exemple mesuré le 19-09-2026 : sur le texte « ligne 1 » suivi d une ligne de
      contrôle, elle rend le corps « ligne 1 » et le nombre 1 ; sur un texte de deux
      lignes sans ligne de contrôle, elle rend ces deux lignes et le nombre 0.
    ⑨ CE QUI CLOCHE — Une ligne de contrôle étrangère posée au MILIEU d un document
      le laisse passer une fois, puis le bloque pour toujours. Mesuré le
      19-09-2026 : à une livraison acceptée, une ligne de contrôle portant
      l empreinte 0000000000000000 est insérée à la cinquième ligne. Comme du texte
      la suit, la fonction rend le texte ENTIER pour corps ; le document ne portant
      qu une seule ligne de contrôle, rien ne le refuse ; il est accepté en code 0,
      et le programme écrit en queue une seconde ligne de contrôle,
      a4eb6455dda7e4ba. Au passage suivant, le document en porte deux et il est
      refusé — « 2 LIGNES DE CONTROLE » — et il le restera tant que personne n aura
      retiré l une des deux à la main.
    ⑩ EFFET — Ne change rien : elle rend deux valeurs, et le texte reçu reste
      intact. Aucun fichier, aucun réseau, aucun affichage.
    ⑪ TERMINAISON — Rend la main à tous les coups. Aucun de ses appels ne peut
      rester en attente.
      [sort: non]
    ⑫ DÉFINITIONS
      une livraison : le document `echanges/A_RELIRE.md`, qui porte le travail
        soumis à la relecture
      une ligne de contrôle : la ligne que ce programme pose en queue d un document
        accepté, portant l empreinte de seize caractères du texte validé
      le relecteur : celui qui relit le travail de l autre, ici Cowork
    
      un motif : un morceau de nom passé à une fonction de recherche, par exemple trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
"""
    lignes = texte.split("\n")
    positions = [i for i, l in enumerate(lignes) if re.match(MARQUEUR, l)]
    if not positions:
        # CC1 DE COWORK, tours 44 et 45 — restee ouverte un tour entier.
        # **A L ECRITURE il n y a pas encore de marqueur : ce chemin rendait le
        # texte AVEC son saut de ligne final. A la LECTURE, le corps est rstrip.
        # La meme fonction rendait deux corps differents**, et toute premiere
        # validation etait ensuite declaree FALSIFIEE.
        # Mesure du 14-09 : marqueur ecrit 4443bff7b99ee621, relu 235233a20260f0dd.
        # **La ligne de queue ne disait plus « ce fichier n a pas bouge », elle
        # disait « quelqu un a lance le programme deux fois ».**
        return texte.rstrip("\n"), 0
    dernier = positions[-1]
    if [l for l in lignes[dernier + 1:] if l.strip()]:
        return texte, len(positions)
    return "\n".join(lignes[:dernier]).rstrip("\n"), len(positions)


def _marqueur_de_queue(texte):
    """Rend la ligne de contrôle qui ferme le document, jamais une autre.

    ① RÔLE — Donner au mode de relecture la seule ligne de contrôle qui fasse foi :
      celle que le programme a posée en fermant le document. C est son empreinte
      qui sera comparée à celle du texte présent.
    ② CONTEXTE D APPEL — La fonction principale, une fois, et seulement quand le
      programme est lancé avec l option de relecture. Jamais appelée ailleurs.
    ③ ENTRÉE — `texte` : le contenu entier du document, tel qu il a été lu sur le
      disque.
    ④ CONDITIONS D ENTRÉE — Du texte. Un document vide ne la fait pas tomber.
    ⑤ SORTIE — UNE valeur : la correspondance trouvée sur la dernière ligne non
      vide quand cette ligne est une ligne de contrôle, son premier groupe portant
      l empreinte de seize caractères ; une valeur vide quand la dernière ligne non
      vide n en est pas une, et quand le document ne porte aucune ligne non vide.
      [rend: 1]
    ⑥ TRAITEMENT — ① parcourir les lignes du document à l envers · ② passer les
      lignes vides · ③ s arrêter à la première ligne non vide rencontrée et dire si
      elle est une ligne de contrôle.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — L ancienne lecture prenait la PREMIÈRE ligne de contrôle du
      document, donc celle qu un tiers vient d insérer en tête. Le seul marqueur
      qui fasse foi est le dernier.
      Exemple mesuré le 19-09-2026 : sur un texte dont la ligne de contrôle est
      suivie de deux lignes vides, elle rend bien l empreinte aaaaaaaaaaaaaaaa ;
      sur un texte où la ligne de contrôle ouvre le document et où du texte la
      suit, elle ne rend rien ; sur un texte vide, elle ne rend rien.
    ⑨ CE QUI CLOCHE — Rien vu.
    ⑩ EFFET — Ne change rien. Aucun fichier, aucun réseau, aucun affichage.
    ⑪ TERMINAISON — Rend la main à tous les coups. Aucun de ses appels ne peut
      rester en attente.
      [sort: non]
    ⑫ DÉFINITIONS
      une ligne de contrôle : la ligne que ce programme pose en queue d un document
        accepté, portant l empreinte de seize caractères du texte validé
      le relecteur : celui qui relit le travail de l autre, ici Cowork
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    for l in reversed(texte.split("\n")):
        if not l.strip():
            continue
        return re.match(MARQUEUR, l)
    return None


def _lire_code():
    """Rend le module LIRE_LE_CODE, voisin de ce programme.

    ① RÔLE — Donner accès à l empreinte du code que le projet emploie déjà.
    ② CONTEXTE D APPEL — `programmes_modifies`, deux fois par programme qui diffère
      de la version officielle.
    ③ ENTRÉE — Aucune.
    ④ CONDITIONS D ENTRÉE — `LIRE_LE_CODE.py` doit se trouver à côté de ce programme,
      et `emp.py` à la racine du dépôt ; sinon l import lève.
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — ajouter le dossier de ce programme au chemin des imports, puis
      importer.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Deux implémentations d une même chose divergent toujours (R-708) :
      le relecteur du 30-09-2026 l a mesuré sur une première version qui recopiait
      ce calcul.
    ⑨ CE QUI CLOCHE — Un import raté lève ; `main` le rattrape et refuse.
    ⑩ EFFET — Modifie le chemin des imports du processus.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    ici = os.path.dirname(os.path.abspath(__file__))
    if ici not in sys.path:
        sys.path.insert(0, ici)
    import LIRE_LE_CODE
    return LIRE_LE_CODE


def _git(racine, *arguments):
    """Lance une commande `git` en lecture dans la racine et rend son résultat.

    ① RÔLE — Un seul endroit où ce programme appelle `git`.
    ② CONTEXTE D APPEL — `programmes_modifies`, trois fois, puis une fois par
      programme qui diffère de la version officielle.
    ③ ENTRÉE — `racine` : le dossier du dépôt · `arguments` : les mots de la
      commande, sans le mot `git`.
    ④ CONDITIONS D ENTRÉE — `git` doit être installé ; sinon l appel lève.
    ⑤ SORTIE — UNE valeur : le résultat du processus, avec son code, sa sortie et
      ses erreurs en texte.
      [rend: 1]
    ⑥ TRAITEMENT — lancer `git -C <racine> <arguments>` et capturer ses sorties.
    ⑦ UNITÉ — Un délai en SECONDES, soixante.
    ⑧ POURQUOI — un délai borne l attente : un dépôt verrouillé ne doit pas bloquer
      le contrôle sans fin.
    ⑨ CE QUI CLOCHE — Un dépassement du délai lève au lieu de rendre un résultat ;
      `main` le rattrape et refuse.
    ⑩ EFFET — Lance un processus `git`, qui ne fait que lire.
    ⑪ TERMINAISON — Rend la main, ou lève au bout de soixante secondes.
      [sort: non]
    """
    import subprocess as _sp
    return _sp.run(["git", "-C", racine, "-c", "core.quotePath=false", *arguments],
                   capture_output=True, text=True, timeout=60)


def programmes_modifies(racine):
    """Rend les programmes dont le CODE diffère de la version officielle du dépôt.

    ① RÔLE — Désigner, sans rien demander à l auteur, les programmes qu une
      livraison change, pour exiger de chacun une épreuve (R-755 ②).
    ② CONTEXTE D APPEL — `main`, une fois par passage.
    ③ ENTRÉE — `racine` : le dossier du dépôt examiné.
    ④ CONDITIONS D ENTRÉE — `racine` doit être un dépôt Git qui connaît la version
      officielle sous le nom `origin/main`. Sinon, la fonction rend une erreur.
    ⑤ SORTIE — DEUX valeurs : la liste triée des chemins des programmes modifiés
      (relatifs à la racine), puis rien ; ou rien, puis le texte de l erreur.
      [rend: 2]
    ⑥ TRAITEMENT — ① vérifier que `origin/main` existe · ② relever les fichiers
      Python de `programmes/` qui diffèrent de `origin/main`, enregistrés ou non,
      et ceux qui ne sont pas encore suivis · ③ écarter ceux qui n existent plus ·
      ④ écarter ceux dont seul le texte explicatif de tête diffère, par l empreinte
      que le projet emploie déjà (`LIRE_LE_CODE.empreinte_du_code`, qui passe la
      main à `emp.py` : fiches du module, des classes et des fonctions retirées).
    ⑦ UNITÉ — Des CHEMINS de fichiers.
    ⑧ POURQUOI — Décision de Jean-Luc du 29-09-2026 à 09h36 (« 1 », écrite dans
      A-494) : la base de comparaison est la VERSION OFFICIELLE, `origin/main`.
      Elle ne bouge qu à la fusion : enregistrer (commiter) ne peut donc plus faire
      taire le contrôle — le défaut mesuré le 20-09-2026, quand la base était la
      dernière version enregistrée et qu un travail commité ne différait plus de
      rien. Un contrôle qui ne peut pas tourner le dit (R-734) : sans `origin/main`,
      l erreur est rendue, et `main` refuse.
    ⑨ CE QUI CLOCHE — `origin/main` est la copie LOCALE de la version officielle :
      si elle n a pas été rafraîchie, la comparaison porte sur une version
      ancienne. Ne sont pas examinés : un programme hors de `programmes/`, les
      tâches du circuit (`.github/workflows/`), un programme supprimé ou déplacé
      hors de `programmes/`. Pour un programme qui existe dans la version
      officielle, un changement du seul texte explicatif de tête n est pas compté,
      même quand le programme l AFFICHE (`print(__doc__…)` : onze appels dans dix
      programmes de la version en attente, recomptés par le relecteur le
      30-09-2026) : ce qu il affiche change alors sans épreuve. Un programme NEUF,
      absent de la version officielle, est toujours compté — c est le cas de
      QUI_TOUCHE_CE_FICHIER.py, créé par la version en attente. Lire
      « modifié » comme « dont le code diffère » est une lecture du Chat de la
      décision du 29-09 (qui dit « tout programme qui en diffère »), soumise à
      Jean-Luc.
    ⑩ EFFET — Lance `git` en lecture dans la racine. Aucun fichier n est écrit.
    ⑪ TERMINAISON — Rend la main. Chaque appel à `git` est borné à 60 secondes ;
      un dépassement lève et remonte à `main`.
      [sort: non]
    """
    base_ref = "refs/remotes/origin/main"   # la référence entière : un tag du même nom ne la masque pas
    if _git(racine, "rev-parse", "--verify", "--quiet", base_ref).returncode != 0:
        return None, ("la version officielle origin/main est introuvable dans " + racine
                      + " — pas de dépôt Git, ou pas de copie locale de la version officielle")
    diff = _git(racine, "diff", "-z", "--name-only", base_ref, "--", "programmes/")
    neufs = _git(racine, "ls-files", "-z", "--others", "--exclude-standard", "--", "programmes/")
    if diff.returncode != 0 or neufs.returncode != 0:
        return None, "git n a pas pu comparer à origin/main : " + (diff.stderr or neufs.stderr).strip()[:200]
    modifies = []
    for chemin in sorted({c for c in diff.stdout.split("\0") + neufs.stdout.split("\0") if c}):
        if not chemin.endswith(".py") or not os.path.isfile(os.path.join(racine, chemin)):
            continue
        base = _git(racine, "show", base_ref + ":" + chemin)
        actuel = open(os.path.join(racine, chemin), encoding="utf-8", errors="replace").read()
        if base.returncode == 0:
            # l'outil du projet, jamais une seconde écriture (R-708) : `emp.py` par
            # LIRE_LE_CODE, qui retire les textes explicatifs de tête (R-752)
            try:
                if _lire_code().empreinte_du_code(base.stdout) == _lire_code().empreinte_du_code(actuel):
                    continue
            except SyntaxError:
                pass                     # illisible : compté comme modifié
        modifies.append(chemin)
    return modifies, None


def epreuves_de(racine, programme):
    """Rend les épreuves de `tests/` qui désignent un programme.

    ① RÔLE — Dire si un programme modifié est vérifié par au moins une épreuve.
    ② CONTEXTE D APPEL — `main`, une fois par programme modifié.
    ③ ENTRÉE — `racine` : le dossier du dépôt · `programme` : le chemin relatif du
      programme.
    ④ CONDITIONS D ENTRÉE — `QUI_TOUCHE_CE_FICHIER.py` et `FABRIQUER_LE_SOCLE.py`
      doivent se trouver à côté de ce programme ; sinon l import lève.
    ⑤ SORTIE — UNE valeur : la liste triée des chemins des fichiers Python de
      `tests/` trouvés.
      [rend: 1]
    ⑥ TRAITEMENT — ① importer `QUI_TOUCHE_CE_FICHIER` depuis le dossier de ce
      programme · ② lui demander les trois parties — les fichiers qui écrivent le
      nom du programme, ceux qui le cherchent par motif, ceux qui nomment un
      programme des deux premières · ③ garder les fichiers Python sous `tests/`.
    ⑦ UNITÉ — Des CHEMINS de fichiers.
    ⑧ POURQUOI — La décision du 29-09-2026 dit « au moins une épreuve de `tests/`,
      trouvée par `programmes/QUI_TOUCHE_CE_FICHIER.py` » : l outil est importé,
      jamais recopié (R-708).
    ⑨ CE QUI CLOCHE — Une épreuve trouvée NOMME le programme, ou un programme qui
      le nomme ; rien ne dit qu elle exerce la partie modifiée. Mesuré par le
      relecteur le 30-09-2026 : une simple mention dans un COMMENTAIRE d un
      programme déjà éprouvé suffit à rendre « éprouvé » un programme neuf, puisque
      la troisième partie de QUI_TOUCHE_CE_FICHIER compte les mentions. Ne garder
      que les deux premières parties serait plus strict que la décision du 29-09,
      qui nomme l outil sans restreindre ses parties : question posée à Jean-Luc.
      Mesuré le 30-09-2026 sur la version en attente : 18 programmes dont le code
      diffère de la version officielle ; 17 ont une épreuve qui les nomme, 1
      (JUGER_SUR_8_CRITERES.py) n a qu une épreuve indirecte.
    ⑩ EFFET — Lit les fichiers du dépôt. N écrit rien.
    ⑪ TERMINAISON — Rend la main ; l import ou la lecture peuvent lever.
      [sort: non]
    """
    import importlib.util as _iu
    ici = os.path.dirname(os.path.abspath(__file__))
    if ici not in sys.path:
        sys.path.insert(0, ici)
    _sp = _iu.spec_from_file_location("QUI_TOUCHE_CE_FICHIER", os.path.join(ici, "QUI_TOUCHE_CE_FICHIER.py"))
    _q = _iu.module_from_spec(_sp)
    _sp.loader.exec_module(_q)
    trouves = set()
    for partie in _q.qui_touche(racine, programme):
        trouves |= {c for c in partie if c.replace(os.sep, "/").startswith("tests/") and c.endswith(".py")}
    return sorted(trouves)


def pieges_r755(racine):
    """Rend la liste des pièges déjà connus, lue dans R-755 ③ du registre.

    ① RÔLE — Donner au contrôle les pièges qu un relecteur doit chercher d abord,
      tels que la règle les énumère aujourd hui.
    ② CONTEXTE D APPEL — `main`, une fois, quand la livraison modifie au moins un
      programme.
    ③ ENTRÉE — `racine` : le dossier du dépôt.
    ④ CONDITIONS D ENTRÉE — `gouvernance/REGISTRE_REGLES.md` doit exister et porter
      la section « ### R-755 » avec son point ③ ; sinon la liste rendue est vide.
    ⑤ SORTIE — UNE valeur : la liste des intitulés, dans l ordre de la règle, par
      exemple « un lecteur du même fichier oublié ».
      [rend: 1]
    ⑥ TRAITEMENT — ① lire le registre · ② isoler la section R-755 · ③ y isoler le
      point ③, jusqu à la phrase « Un piège nouveau » · ④ prendre le texte en gras
      qui ouvre chaque ligne de liste.
    ⑦ UNITÉ — Des intitulés en français.
    ⑧ POURQUOI — R-755 ③ dit : « Un piège nouveau trouvé en relecture s ajoute à
      cette liste, ici, par révision de la règle. » La liste vit donc au registre,
      et ce contrôle la LIT à chaque passage au lieu d en garder une copie (R-708).
    ⑨ CE QUI CLOCHE — Elle dépend de la forme d écriture : un piège ajouté sans gras
      en tête de ligne ne serait pas lu. Une liste vide est traitée par `main` comme
      un contrôle qui n a pas pu tourner.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main à tous les coups.
      [sort: non]
    """
    chemin = os.path.join(racine, "gouvernance", "REGISTRE_REGLES.md")
    if not os.path.isfile(chemin):
        return []
    t = open(chemin, encoding="utf-8", errors="replace").read()
    i = t.find("\n### R-755")
    if i < 0:
        return []
    fin = t.find("\n### ", i + 5)
    sec = t[i:fin if fin > 0 else len(t)]
    j = sec.find("\n③ ")
    k = sec.find("Un piège nouveau", j)
    if j < 0 or k < 0:
        return []
    return [m.group(1).strip() for m in re.finditer(r"(?m)^- \*\*(.+?)\*\*", sec[j:k])]


def main():
    """Décide si la livraison part ou non, et pose l empreinte du texte accepté.

    ① RÔLE — Réduire l état d un document de livraison à une seule décision que
      son auteur ne peut pas négocier : elle part, ou elle ne part pas. Et laisser
      dans le document lui-même la trace de cette décision, pour que le relecteur
      sache, en le rouvrant, qu il a bien été contrôlé et qu il n a pas bougé
      depuis.
    ② CONTEXTE D APPEL — Le lancement du programme, et lui seul. Trois manières :
      le Chat à la main, au sixième des huit gestes du protocole de livraison écrit
      en tête de `gouvernance/REGISTRE_REGLES.md`, avant tout dépôt · le relecteur,
      avec l option de relecture, qui vérifie sans rien écrire ·
      `programmes/EPREUVES_DU_GARDE_FOU.py`, qui lance le programme en
      sous-processus sur neuf documents fabriqués puis une soixantaine de fois
      pendant son sabotage. Aucune tâche du soir ne l appelle : mesuré le
      19-09-2026, la recherche du nom du programme dans les fichiers de tâches du
      dossier `.github/workflows` n en rend aucune occurrence.
    ③ ENTRÉE — Aucun paramètre. Elle lit la ligne de commande : le premier mot qui
      ne commence pas par deux tirets est pris pour le chemin du document, et la
      présence du mot « --verifier » met le programme en mode relecture.
    ④ CONDITIONS D ENTRÉE — Un chemin doit être donné, et le fichier doit exister et
      se lire. Le document doit porter le repère des cinq passes. Hors mode
      relecture, il doit être accessible en écriture. Le dossier grand-parent du
      fichier est pris pour racine du dépôt.
    ⑤ SORTIE — Ne rend rien : elle sort elle-même du programme, en rendant un code
      de sortie. 0 quand les quatre propriétés sont portées ou quand la relecture
      retrouve l empreinte, 1 à chaque refus.
      [rend: rien]
    ⑥ TRAITEMENT — ① afficher le mode d emploi et sortir en 1 si aucun chemin n est
      donné · ② refuser si le fichier est introuvable · ③ lire le document ·
      ④ chercher la DERNIÈRE occurrence du repère des cinq passes et refuser s il
      est absent · ⑤ séparer les blocs d exécution des blocs de prose · ⑥ refuser
      si la première sortie capturée n arrive qu après les deux tiers du document ·
      ⑦ relancer les commandes citées, refuser chaque sortie fabriquée, et afficher
      ce qui n a pas pu être relancé · ⑧ refuser plus d une ligne de contrôle ·
      ⑨ refuser si l une des cinq passes manque · ⑩ refuser une passe de mandat
      inversé, de famille ou de régression qui ne porte aucune sortie capturée, la
      zone d une passe allant de son titre au titre gras de la passe suivante ·
      ⑪ refuser une passe de non-éprouvé qui dit « rien » sans énumérer ·
        [sort: oui]
      ⑫ relever TOUS les fichiers Python du dossier `programmes`, et refuser s il
      n y en a aucun · refuser une fiche que le code contredit sur ses paramètres,
      sur son nombre de valeurs rendues — un appel à une fonction du même fichier
      rendant ce qu elle rend — ou sur sa terminaison, une fonction qui lève
      toujours ne rendant pas la main · afficher le nombre de fiches dont le
      nombre de valeurs n a pu être confronté · ⑬ refuser toute fonction, à tous
      les niveaux, qui ne porte pas ses onze premiers éléments · ⑭ refuser toute affirmation de conformité qui
      n est ni citée entre délimiteurs, ni enfermée dans un bloc, ni précédée d une
      sortie capturée · ⑭bis (30-09-2026, R-755 ② et ③) relever les programmes dont
      le code diffère de la version officielle `origin/main`, refuser si ce relevé
      est impossible, refuser chacun qu aucune épreuve de `tests/` ne désigne, et,
      s il y en a au moins un, refuser chaque piège de R-755 ③ dont l intitulé, en
      gras, n est pas suivi dans les 1 500 caractères, avant le piège suivant, d une
      sortie capturée à une place qui lui est propre — le contrôle vérifie cette
      place, pas que la sortie écarte le piège · ⑮ afficher le
      compte rendu et sortir en 1 s il y a un refus · ⑯ calculer l empreinte du corps du document · ⑰ en mode relecture, la
      comparer à la ligne de contrôle et sortir ; sinon réécrire le document avec
      sa nouvelle ligne de contrôle et sortir en 0.
    ⑦ UNITÉ — Un NOMBRE DE CARACTÈRES pour la taille du document affichée · des
      NOMBRES DE BLOCS de code · des NUMÉROS DE LIGNE pour les affirmations nues ·
      un NOMBRE DE MOTIFS de refus · une EMPREINTE de seize caractères
      hexadécimaux. L horodatage de la ligne de contrôle est en heure de Paris.
    ⑧ POURQUOI — Les passes se lisent APRÈS le repère et jamais au fil du texte. Le
      12-09-2026, le relecteur a montré qu il suffisait de citer un bon jeu de
      passes en tête du document pour que le contrôle l accepte sans jamais
      descendre jusqu aux vraies. Ce n est pas un cas tordu : c est le cas normal
      d une relecture, puisqu un relecteur ne peut pas citer ce qu il casse.
      La zone d une passe se borne sur le titre gras de la passe suivante, et non
      sur un mot. Mesuré le 12-09-2026 : le mot « lien », qui nomme la cinquième
      passe, apparaissait DANS la sortie de programme collée en troisième passe —
      « aucun lien detecte » — et refermait la zone au milieu de la preuve.
      Le contrôle automatique de la passe de régression a été RETIRÉ le 17-09-2026
      après quatre versions cassées en une soirée : la dernière refusait la
      vérification par clone neuf, où rien n est modifié par construction, et
      refusait toute livraison qui n était pas l un des deux fichiers d échange.
      Un garde-fou qui refuse le travail légitime coûte plus qu il ne protège. La
      règle demeure, en tête du registre, tenue par la relecture et non par ce
      programme.
      Le mode de relecture existe parce que vérifier une livraison ne doit pas la
      modifier : le relecteur qui contrôlait la ligne de contrôle réécrivait le
      fichier de l autre sans le savoir.
    ⑨ CE QUI CLOCHE — Quatre points relevés le 19-09-2026, dont trois sont RÉGLÉS
      le 20-09-2026 : ① hors d un dépôt Git les contrôles qui lisent le code se
      taisaient, ② un fichier Python neuf était invisible tant qu il n était pas
      ajouté à l index de Git, ④ les refus ne nommaient que quatre cas sans dire
      combien il en restait. **Les deux premiers avaient une cause commune, et
      elle en portait une troisième, mesurée le 20-09-2026 : un travail COMMITÉ
      ne différait plus de la version de référence de Git, et le contrôle ne
      regardait plus rien. Commiter suffisait à le faire taire.** Le contrôle ne
      consulte plus Git : il lit tous les programmes. Restent :
      **Les trois qui suivaient — ③ les fonctions imbriquées jamais confrontées,
      ⑥ le nombre de valeurs lu sous cinq formes seulement, ⑦ la terminaison lue
      dans trois formules — sont RÉGLÉS le 22-09-2026, par la décision de Jean-Luc
      de poser une MARQUE exacte.** Le contrôle ne lit plus le français : la fiche
      porte `[rend: …]` à la fin de son ⑤ et `[sort: oui|non]` à la fin de son ⑪,
      écrits par `programmes/MARQUER_LES_FICHES.py` d après le code, et ce contrôle
      recalcule les mêmes faits par `programmes/LIRE_LE_CODE.py` avant de comparer.
      Une fiche sans marque est refusée. Reste :
      ⑤ Un appel à une fonction d un AUTRE fichier ou d une bibliothèque compte
      toujours pour UNE valeur : `return divmod(a, b)` rend un couple, et la marque
      posée dirait 1. Seuls les appels à une fonction du même fichier sont résolus.
      ⑧ **La marque est calculée depuis le code : elle dit donc toujours vrai du
      code, et rien de la phrase qui l entoure.** C est le marqueur, une fois, qui
      signale une phrase en désaccord avec elle ; ensuite plus personne ne le fait.
      ⑨ (30-09-2026, relecteur) Un texte placé en commentaire HTML (`<!-- … -->`),
      invisible à l affichage, est lu comme un texte visible : des pièges, des
      sorties, des passes entières peuvent y être cachés et satisfaire le contrôle.
      Le contrôle des pièges (⑭bis) ne juge pas le contenu d une sortie : une sortie
      vide de sens, placée au bon endroit, le satisfait.
    ⑩ EFFET — RÉÉCRIT entièrement le document contrôlé quand il est accepté et que
      le mode relecture est absent : corps du texte, puis une ligne de contrôle
      portant l empreinte et l horodatage de Paris. RECOPIE le dépôt entier dans un
      dossier temporaire — 292 fichiers, 12 Mo, 0,04 seconde mesurés le 19-09-2026
      — et y EXÉCUTE les commandes python3 citées par le document, y compris en
      mode relecture. LIT tous les fichiers Python du dossier `programmes` pour en
      confronter les fiches, sans consulter Git pour ce contrôle-là, et fait
      calculer `programmes/LIRE_LE_CODE.py`. LANCE `git` en
      lecture dans la racine du document pour comparer les programmes à
      `origin/main` (depuis le 30-09-2026), et importe `QUI_TOUCHE_CE_FICHIER.py`.
      Affiche de deux à une dizaine de lignes. Aucun autre fichier du dépôt n est
      touché.
    ⑪ TERMINAISON — SORT DU PROGRAMME à chaque issue, et ne rend jamais la main.
      Code 1 : aucun argument · fichier introuvable · repère des cinq passes
      absent · au moins un motif de refus · ligne de contrôle absente ou empreinte
      différente en mode relecture. Code 0 : livraison acceptée, ou relecture qui
      retrouve l empreinte, y compris sous la forme d avant le 14-09-2026. Un de
      ses appels peut ne pas revenir : la relance des commandes citées lance des
      processus séparés, chacun borné à 120 secondes.
    ⑫ DÉFINITIONS
      une livraison : le document `echanges/A_RELIRE.md`, qui porte le travail
        soumis à la relecture
      le Chat : la conversation qui rédige la gouvernance du projet et dépose ses versions
      le relecteur : celui qui relit le travail de l autre, ici Cowork
      une passe : l une des cinq vérifications qu une livraison doit afficher —
        mandat inversé, famille, régression, non éprouvé, lien (R-740)
      une sortie capturée : un bloc de texte qui porte la trace d une exécution —
        une invite de commande ou un code de sortie — et non de la prose
      une ligne de contrôle : la ligne que ce programme pose en queue d un document
        accepté, portant l empreinte de seize caractères du texte validé
      une fiche : le texte explicatif écrit en tête d'une fonction, dans le code, qui porte ses onze rubriques.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
    """
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    # Q5 : « vérifier ta livraison modifie ta livraison ». Le relecteur qui contrôle
    # la ligne de queue enfreignait « chacun écrase le sien, jamais celui de l'autre »
    # sans le savoir, et pouvait la pousser sans la voir.
    verifier = "--verifier" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    chemin = args[0] if args else None
    if not chemin:
        print(__doc__); sys.exit(1)
    if not os.path.isfile(chemin):
        print(f"REFUSÉ — {chemin} introuvable"); sys.exit(1)
    t = open(chemin, encoding="utf-8", errors="replace").read()
    # Q2 de Cowork, 12-09, LA PLUS GRAVE DU TOUR : `pos = min([bas.find(m)…])`
    # lisait la PREMIÈRE occurrence dans tout le document. Il suffisait de citer un
    # bon jeu de passes en tête pour que le contrôle l'accepte et ne descende jamais
    # jusqu'aux vraies. **Et ce n'est pas un cas tordu : c'est le cas NORMAL d'une
    # relecture.** Sa relecture d'hier a été refusée pour cette raison — le contrôle
    # jugeait les livraisons creuses qu'il citait comme preuves d'attaque.
    # « UN RELECTEUR NE PEUT PAS CITER CE QU'IL CASSE. »
    # LA CORRECTION : les passes se lisent APRÈS le repère `R-740`, un marqueur
    # explicite placé par l'auteur — jamais par une recherche au fil du texte.
    _rep = max(t.rfind("# R-740"), t.rfind("R-740 — LES CINQ PASSES"))
    if _rep < 0:
        print("  ❌ LIVRAISON REFUSÉE — le repère « # R-740 » est absent.")
        print("     Les passes se lisent APRÈS ce repère, jamais au fil du texte :")
        print("     sinon un jeu de passes cité en exemple est pris pour le vrai.")
        sys.exit(1)
    t_passes = t[_rep:]
    bas = t_passes.lower()
    captures, proses = blocs_captures(t)
    refus = []
    _r744 = mesure_avant_ecriture(t)
    if _r744:
        refus.append(_r744)
    # LA SORTIE CITEE SE REJOUE. Un texte fabrique sous une invite reelle est
    # la faute la plus grave du 13-09 : quatre depots l ont portee.
    # LA RACINE, PAS LE DOSSIER DU FICHIER. Mesure du 13-09 : lance depuis
    # `echanges/`, un `python3 programmes/x.py` ne trouve rien — et le controle
    # criait « SORTIE FABRIQUEE » sur des sorties parfaitement vraies.
    # **Un garde-fou qui accuse a tort est aussi cher qu un garde-fou muet.**
    _rac = os.path.dirname(os.path.dirname(os.path.abspath(chemin))) or "."
    if not os.path.isdir(os.path.join(_rac, "programmes")):
        _rac = "."
    _ver, _fab, _ign = sortie_rejouee(t, _rac)
    for cmd, ligne in _fab:
        refus.append(f"SORTIE FABRIQUEE — « {cmd} » ne rend pas « {ligne} »")
    # DETTE PAYEE, 14-09 — Cowork, deux tours de suite : « le rejeu attend
    # toujours ses `_ver` et `_ign` ». Je les rendais et personne ne les lisait.
    # **Un controle qui IGNORE en silence ment par omission** : le lecteur croit
    # que tout a ete rejoue. Ce qui n a pas pu l etre se DIT, sans refuser —
    # une commande non rejouable n est pas une faute.
    if _fab or _ign:
        print(f"  REJEU — {len(_ver)} verifiee(s) · {len(_fab)} fabriquee(s) · "
              f"{len(_ign)} non rejouable(s)")
        for c in _ign:
            print(f"     non rejouee : {c}")
    # DETTE PAYEE — le nombre de marqueurs etait COMPTE et jamais refuse.
    # Deux marqueurs dans un document sont une anomalie : l un des deux ment.
    _nb_m = len([l for l in t.split("\n") if re.match(MARQUEUR, l)])
    if _nb_m > 1:
        refus.append(f"{_nb_m} LIGNES DE CONTROLE — une seule fait foi, "
                     f"les autres sont etrangeres au document")

    # ① les cinq passes, nommées
    manquantes = [n for n, mots in PASSES.items() if not any(m in bas for m in mots)]
    if manquantes:
        refus.append(f"LES CINQ PASSES : {', '.join(manquantes)} absente(s) — R-740")

    # ② LES PASSES ①, ② ET ③ SE PRODUISENT, ELLES NE SE RÉDIGENT PAS.
    # P1 de Cowork : mon test était `re.search(r"\d", zone)` — N'IMPORTE QUEL
    # CHIFFRE dans les 700 premiers caractères valait « cas d'attaque », et une
    # livraison porte toujours une date. **Le test était vrai par construction :
    # un contrôle qui ne peut pas rougir, au cœur du programme censé l'empêcher.**
    # Et son test de la passe ④, `len(...) < 40`, était UN COMPTE dans un garde-fou.
    # LA CORRECTION EST SA RECOMMANDATION : ces passes portent une sortie CAPTURÉE
    # ou elles ne valent rien. « Rien trouvé » sans sortie est refusé.
    # LA PASSE ② REJOINT LES DEUX AUTRES — 18-09-2026.
    # **DEUX FOIS DE SUITE ELLE A PORTE UNE AFFIRMATION FAUSSE** : le 17-09
    # « deux autres commits nomment un fichier qu ils ne touchent pas » — il n y
    # en avait aucun sur quarante ; le 18-09 « la photographie annonce 296
    # fonctions » — le document en annonce 297, et « 296 » n y figure nulle part.
    # **LA CAUSE, NOMMEE PAR COWORK : c est la seule des cinq passes qui s ecrit
    # sans lancer d outil.** Les quatre autres portent une preuve ou une
    # enumeration ; celle-ci portait une phrase.
    # **LA PARADE EST LA MEME QUE POUR ① ET ③ : elle porte une sortie capturee.**
    # Chercher ailleurs est un GESTE — un parcours, une recherche — et son
    # resultat s affiche. **Une recherche affichee qui ne trouve rien vaut mieux
    # qu une phrase affirmant qu on a cherche.**
    for cle, nom in (("①", "MANDAT INVERSÉ"), ("②", "FAMILLE"), ("③", "RÉGRESSION")):
        pos = min([bas.find(m) for m in PASSES[cle] if bas.find(m) >= 0] or [-1])
        if pos < 0:
            continue
        pos += _rep
        # LA ZONE SE BORNE SUR LE MARQUEUR DE PASSE, PAS SUR UN MOT.
        # Mesuré le 12-09 sur ma propre livraison : le mot « lien » — marqueur de
        # la passe ⑤ — apparaissait DANS la sortie de programme collée en passe ③
        # (« aucun lien detecte »), et bornait la zone AU MILIEU de la preuve.
        # **Une passe bornée par un mot qui vit dans sa propre preuve.** C'est la
        # famille de ce que Cowork me reproche depuis hier : chercher un mot au fil
        # du texte au lieu de lire une structure. Les passes sont numérotées ① à ⑤
        # — ce sont ces marqueurs qui les séparent, et rien d'autre.
        # ON BORNE SUR LA FORME DU TITRE, PAS SUR LE SYMBOLE NU.
        # BB3 de Cowork, 13-09-2026, mesuré sur son propre document : sa phrase
        # d introduction disait « la mesure de ta passe ④, faite en entier ». Le
        # symbole ④ apparaissait 41 caracteres apres le titre de la passe ①, et
        # il la refermait AVANT son bloc. **Trois refus pour une citation.**
        # « Tu es passe du mot au symbole, et le symbole est encore du texte
        # libre. Un relecteur ne peut toujours pas CITER une passe a l interieur
        # d une autre sans la couper. »
        # C est la meme famille, une couche plus bas : le mot au tour 7, le
        # marqueur au tour 7bis, « lien mort » au tour 10, « passe ④ » ce soir.
        # UN TITRE DE PASSE OUVRE UNE LIGNE ET PORTE SON GRAS. Une citation au
        # fil d une phrase n en est pas un.
        fin = len(t)
        for marq in ("①", "②", "③", "④", "⑤"):
            if marq == cle:
                continue
            for _m in re.finditer(r"^\s*\*\*" + marq, t[pos + 5:], re.M):
                fin = min(fin, pos + 5 + _m.start())
                break
        # LA TOLERANCE DE 200 CARACTERES EST RETIREE — 17-09-2026.
        # **Trouvee par les epreuves du garde-fou, a leur premiere execution.**
        # Elle servait a accepter un bloc pose juste apres le titre de la passe
        # suivante. **Dans un document court, elle attrapait le bloc de la passe
        # SUIVANTE : une passe ① sans aucune preuve passait, parce que le bloc de
        # la passe ③ tombait dans sa tolerance.**
        # Et c etait un COMPTE, ce que R-745 interdit : 200 ne mesure rien.
        # **La capture doit COMMENCER dans la passe. Sa fin peut deborder — un
        # bloc long reste dans la passe ou il commence.**
        if not any(pos <= a < fin for a, b in captures):
            refus.append(f"PASSE {cle} ({nom}) : aucune SORTIE CAPTURÉE — "
                         f"ce qui se mesure ne s'écrit pas à la main (R-728)")

    # ③ la passe ④ nomme ce qui n'a pas été éprouvé — pas de compte de caractères
    j = min([bas.find(m) for m in PASSES["④"] if bas.find(m) >= 0] or [-1])
    if j >= 0:
        zone = t[j + _rep:j + _rep + 500]
        if re.search(r"\b(rien|aucun|néant|neant)\b", zone[:120], re.I) and \
           not re.search(r"[·\-—]\s*\w+.*[·\-—]", zone):
            refus.append("PASSE ④ : « rien » sans énumération — ce qui n'a pas "
                         "été éprouvé se NOMME, un par un")

    # LE CONTROLE AUTOMATIQUE DE LA PASSE ③ EST RETIRE — 17-09-2026.
    # **QUATRE VERSIONS EN UNE SOIREE, CASSEES LES QUATRE FOIS**, et la derniere
    # bloquait deux gestes legitimes :
    # · elle REFUSAIT la verification par clone neuf que le §5 impose aux deux
    #   roles — dans un clone neuf rien n est modifie, le releve est vide par
    #   construction, et le controle refusait ;
    # · elle ne savait relever que `echanges/`, jamais un fichier NEUF, jamais
    #   une etude ou un programme — **elle refusait tout ce qui n etait pas l un
    #   des deux fichiers d echange**, alors que le protocole s applique a tout.
    # Et sa borne se refermait sur elle-meme des la deuxieme livraison d un tour.
    #
    # **LA REGLE RESTE, EN TETE DU REGISTRE : la sortie de la passe ③ doit
    # pouvoir rougir si la livraison est fausse.** Elle est tenue par la
    # relecture, pas par ce programme. **Un garde-fou qui refuse le travail
    # legitime coute plus qu il ne protege** — et ce controle refusait la
    # livraison du relecteur, la verification par clone neuf, et toute etude.

    # ⑤ UNE FICHE ECRITE DANS LE CODE DIT-ELLE CE QUE LE CODE FAIT ?
    # **DEMANDE DE JEAN-LUC, 19-09-2026** : « est-ce que ce que tu ecris est bien
    # strictement ce que font les programmes, et pas ton imagination ? »
    # **CAS REEL, vingt minutes plus tot** : la fiche de `ouvrir_sur_signaux`
    # annoncait recevoir les reglages par strategie. **Sa signature ne les recoit
    # pas.** La fiche portait ses onze elements, le garde-fou l a laissee passer.
    # **CE QUI SE VERIFIE, ET CE QUI NE SE VERIFIE PAS.** Le role, le pourquoi et
    # ce qui cloche sont une LECTURE — aucun programme ne peut les juger. Mais
    # les parametres, les valeurs rendues et les codes de sortie SE LISENT DANS
    # LE CODE : une fiche qui les contredit est fausse, et cela se mesure.
    # **C est le seul controle qui ne demande rien a la memoire de celui qui
    # livre.** Il porte sur les programmes modifies par cette livraison.
    # **LA PORTEE N EST PLUS « CE QUE GIT DIT MODIFIE » — 20-09-2026.**
    # Premier etat : `git diff --name-only HEAD`. **Un travail COMMITE ne
    # differe plus de HEAD : le releve etait vide, et le controle ne regardait
    # plus rien.** Mesure du 20-09-2026 sur la branche
    # `travail-non-valide-20-09-2026` : refusee tant que le travail n etait pas
    # commite, ACCEPTEE (code 0) une fois commite, sans qu une seule fiche ait
    # change. **Commiter suffisait a faire taire le garde-fou.**
    # **LA PROPRIETE** : toute fiche de tout programme du dossier `programmes`
    # est confrontee a son code, a chaque passage. Ce que git dit modifie ne
    # compte plus. **Cout mesure le 20-09-2026 : zero fiche fausse sur les 34
    # programmes de la branche, donc rien de legitime n est bloque.**
    # **UN CONTROLE QUI N A PAS PU TOURNER LE DIT (R-734)** : sans dossier
    # `programmes`, ou sans un seul fichier Python dedans, la livraison est
    # refusee au lieu de passer sans rien avoir regarde.
    import ast as _ast5
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import LIRE_LE_CODE as _lire5
    _racine5 = os.path.dirname(os.path.dirname(os.path.abspath(chemin)))
    _dos5 = os.path.join(_racine5, "programmes")
    _pys = sorted(os.path.join("programmes", x) for x in
                  (os.listdir(_dos5) if os.path.isdir(_dos5) else [])
                  if x.endswith(".py"))
    if not _pys:
        refus.append(f"FICHES NON CONTRÔLÉES (R-734) — aucun programme Python dans "
                     f"{_dos5} : le contrôle n'a rien pu confronter")
    _faux = []
    for _p5 in _pys:
        _abs = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(chemin))), _p5)
        if not os.path.isfile(_abs):
            continue
        try:
            _a5 = _ast5.parse(open(_abs, encoding="utf-8", errors="replace").read())
        except Exception:
            continue
        # **LES NOEUDS PROPRES D UNE FONCTION** : son corps, sans descendre dans
        # les fonctions, classes ou lambdas qu elle definit. **`ast.walk` y
        # descendait : un `return` ou un `yield` d une fonction imbriquee etait
        # compte a la fonction qui l enveloppe.** Mesure du 20-09-2026 : sans
        # effet sur les 34 programmes d aujourd hui, mais le controle des
        # generateurs, ci-dessous, en depend.
        # **TOUTE FONCTION, A TOUS LES NIVEAUX — releve de Cowork, 22-09-2026.**
        # Premier etat : seules les fonctions du premier niveau du fichier
        # etaient confrontees a leur code. **Mesure de Cowork sur la version en
        # attente : 296 fonctions confrontees, 34 non — 14 methodes de classe et
        # 20 fonctions imbriquees — sur 330.** Cas construit par lui : une
        # methode qui annonce UNE valeur et rend un couple, acceptee. Les
        # fonctions sont donc prises dans tout l arbre, et reperees par leur
        # NOEUD et non par leur nom, qui n est unique a aucun niveau.
        # **LE CALCUL DE CE QUE FAIT LE CODE VIT DANS UN SEUL FICHIER — decision
        # de Jean-Luc du 22-09-2026.** `programmes/LIRE_LE_CODE.py` dit ce qu une
        # fonction rend et si elle rend la main ; `programmes/MARQUER_LES_FICHES.py`
        # ecrit ce fait dans la fiche sous la forme `[rend: …]` et `[sort: …]` ; ce
        # controle le recalcule et compare a la marque. **Le garde-fou ne lit plus
        # le francais.** Avant cette decision il cherchait « UNE valeur », « DEUX
        # valeurs »… dans le ⑤ et trois formules dans le ⑪ : chaque mot ajoute a
        # cette liste, le 22-09-2026, a produit un faux refus ailleurs.
        _fns5 = _lire5.fonctions_du_fichier(_a5)
        for _fn in _fns5:
            # **UN ELEMENT SE RECONNAIT EN DEBUT DE LIGNE — releve de Cowork,
            # 22-09-2026.** Premier etat : le SIGNE cherche n importe ou dans le
            # texte. Cas construit par lui : une fiche sans son ⑦ UNITE, dont le
            # ⑥ TRAITEMENT numerote sept etapes de ① a ⑦ — **le ⑦ de l etape
            # tenait lieu de l element absent**, et la fiche etait acceptee. Un
            # element ouvre sa ligne ; une etape numerotee se lit dans le fil
            # d une phrase. Mesure du 22-09-2026 avant adoption : sur les 34
            # programmes, aucune fiche ne porte un signe autrement qu en tete de
            # ligne, donc aucune n est accusee par ce changement.
            _d5 = _ast5.get_docstring(_fn) or ""
            if not all(re.search(rf"(?m)^\s*{c}", _d5) for c in "①②③④⑤⑥⑦⑧⑨⑩⑪"):
                continue
            _i5 = _d5.find("③"); _j5 = _d5.find("④", _i5)
            _e5z = _d5[_i5:_j5] if _i5 >= 0 else ""
            # TOUS LES PARAMETRES, y compris `*chemins` et `**options`.
            # **Premier jet : seuls les parametres ordinaires etaient releves,
            # et `charger_cours_du_banc(base, *chemins)` voyait son `chemins`
            # signale comme invente.** Le motif etait faux, pas la fiche.
            _reels = [a.arg for a in _fn.args.args]
            _reels += [a.arg for a in getattr(_fn.args, "kwonlyargs", [])]
            for _v in (_fn.args.vararg, _fn.args.kwarg):
                if _v is not None:
                    _reels.append(_v.arg)
            # **UN PARAMETRE ETOILE PEUT PORTER SON ETOILE — releve de Cowork,
            # 22-09-2026.** Cas construit par lui : `def f(*cours)` dont le ③
            # ecrit « `*cours` : les series », REFUSE a tort. Les trois
            # ecritures sont acceptees : le nom nu, avec une etoile, avec deux.
            _oublies = [a for a in _reels
                        if not any(f"`{_e}{a}`" in _e5z for _e in ("", "*", "**"))]
            # UN PARAMETRE ANNONCE QUI N EXISTE PAS DANS LA SIGNATURE.
            # **Le motif ne retient que ce qui est PRESENTE comme un parametre** :
            # un nom entre accents graves suivi de `:` ou de ` — `, comme
            # « `positions` : toutes les positions ». Premier jet, il relevait
            # TOUT nom entre accents graves — **il signalait `trouver_module`,
            # une fonction CITEE dans le texte, comme un parametre invente.**
            # Un motif se calibre avant de servir ; celui-la ne l avait pas ete.
            _annonces = re.findall(r"`(\w+)`\s*(?::|—)", _e5z)
            _inventes = [a for a in set(_annonces)
                         if a not in _reels and a not in ("None", "self")]
            # LE ⑤ SE LIT AUSSI DANS LE CODE — cassure de Cowork, 19-09-2026.
            # **Mon controle ne regardait que le ③, et je l avais nomme moi-meme
            # comme non eprouve : « il ne regarde que le ③, les dix autres
            # elements peuvent mentir librement ».** Il a cherche la, et trouve :
            # la fiche de `tenir` annoncait DEUX valeurs la ou le code rend UN
            # dictionnaire de SIX cles, dont `incidents` et `alerte`.
            # **Un lecteur qui suit la fiche croit recuperer un couple.**
            # **CE QUI SE COMPTE : un `return` de tuple donne son nombre
            # d elements · un dictionnaire, un objet ou un appel donnent UNE
            # valeur · aucun `return` avec valeur signifie que rien n est rendu.**
            # **ON NE TRANCHE QUE SI TOUS LES `return` S ACCORDENT.** Premier
            # jet : le PREMIER `return` rencontre decidait. **Mesure du 19-09 :
            # `_fichiers_de_cours` porte un `return` de couple et un `return`
            # d appel — le controle accusait une fiche juste.**
            # Une fonction dont les retours ne s accordent pas ne peut pas etre
            # confrontee a un nombre : le controle se tait plutot que d accuser.
            # **LA MARQUE, ET PLUS LA PHRASE.** La fiche porte `[rend: …]` a la
            # fin de son ⑤ et `[sort: oui|non]` a la fin de son ⑪, ecrits par
            # `programmes/MARQUER_LES_FICHES.py` d apres le code. Ici on recalcule
            # les memes faits et on compare. **Une fiche sans marque est refusee** :
            # sans elle, rien n est controle, et un controle qui ne controle rien
            # doit le dire (R-734). Pour la poser, relancer le marqueur.
            _rend5, _sort5 = _lire5.faits_de_la_fonction(_fn, _a5)
            # La marque OUVRE sa ligne. Sans cette ancre, une phrase qui PARLE de
            # la marque — le texte du marqueur lui-meme — etait lue comme une
            # marque : mesure du 22-09-2026 sur `marquer_un_fichier`.
            _mq_rend5 = re.search(r"(?m)^[ \t]*\[rend: ([^\]]+)\]", _d5)
            _mq_sort5 = re.search(r"(?m)^[ \t]*\[sort: (oui|non)\]", _d5)
            _ou5 = f"{_fn.name} dans {os.path.basename(_p5)}"
            if not _mq_rend5 or not _mq_sort5:
                _faux.append(f"{_ou5} : fiche sans sa marque — relancer "
                             f"programmes/MARQUER_LES_FICHES.py")
            else:
                if _mq_rend5.group(1) != _rend5:
                    _faux.append(f"{_ou5} : la marque dit « rend: {_mq_rend5.group(1)} », "
                                 f"le code rend « {_rend5} »")
                if (_mq_sort5.group(1) == "oui") != _sort5:
                    _faux.append(f"{_ou5} : la marque dit « sort: {_mq_sort5.group(1)} », "
                                 f"le code {'sort' if _sort5 else 'rend la main'}")
            if _oublies:
                _faux.append(f"{_fn.name} dans {os.path.basename(_p5)} : ③ ne nomme pas "
                             + ", ".join(_oublies))
            if _inventes:
                _faux.append(f"{_fn.name} dans {os.path.basename(_p5)} : ③ annonce "
                             + ", ".join(_inventes) + " — absent(s) de la signature")
    if _faux:
        refus.append("FICHE CONTREDITE PAR LE CODE — " + " · ".join(_faux[:4])
                     + (f" … et {len(_faux) - 4} autre(s)" if len(_faux) > 4 else ""))
    # **UN CONTROLE QUI SE TAIT LE DIT (R-734).** Les fiches dont le ⑤ n a pu
    # etre confronte a aucun nombre — generateur, ou forme inconnue — sont
    # comptees et affichees : un silence compte ne se confond pas avec un accord.

    # ⑥ TOUTE FONCTION PORTE SES ONZE PREMIERS ELEMENTS — 19 puis 20-09-2026.
    # **DEMANDE DE JEAN-LUC, 19-09-2026** : « quand on va ameliorer le code ou le
    # modifier, il faudra garder ces regles. Comment ce sera fait ? »
    # **Premier etat : ce controle ne portait que sur les fonctions NEUVES**,
    # celles absentes de la version que git appelle HEAD. **Meme defaut que le
    # controle des fiches, plus haut : une fois le travail commite, HEAD le
    # contient, plus aucune fonction n est neuve, et le controle ne voyait
    # plus rien.** Il avait ete borne aux fonctions neuves parce que 255
    # fonctions attendaient alors leur texte ; **mesure du 20-09-2026 : les 329
    # fonctions des 34 programmes, a tous les niveaux, portent leurs onze
    # premiers elements.** La borne n a plus d objet.
    # **LA PROPRIETE** : toute fonction de tout programme du dossier
    # `programmes`, a tous les niveaux — imbriquee ou portee par une classe
    # comprise —, porte les elements ① a ⑪. **Le ⑫ n est pas exige : il
    # n existe que si la fonction emploie un terme du projet.**
    import ast as _ast6
    _sans6 = []
    for _p6 in _pys:
        _abs6 = os.path.join(_racine5, _p6)
        try:
            _ap6 = _ast6.parse(open(_abs6, encoding="utf-8", errors="replace").read())
        except Exception as _e6:
            _sans6.append(f"{os.path.basename(_p6)} : illisible ({type(_e6).__name__})")
            continue
        for _fn6 in _ast6.walk(_ap6):
            if not isinstance(_fn6, (_ast6.FunctionDef, _ast6.AsyncFunctionDef)):
                continue
            _d6 = _ast6.get_docstring(_fn6) or ""
            # Le signe ouvre sa ligne : une etape numerotee dans une phrase ne
            # tient pas lieu d element (releve de Cowork, 22-09-2026).
            _mq = [c for c in "①②③④⑤⑥⑦⑧⑨⑩⑪"
                   if not re.search(rf"(?m)^\s*{c}", _d6)]
            if _mq:
                _sans6.append(f"{_fn6.name} dans {os.path.basename(_p6)} : "
                              f"éléments manquants {''.join(_mq)}")
    if _sans6:
        refus.append("FONCTION SANS SES ONZE PREMIERS ÉLÉMENTS — " + " · ".join(_sans6[:4])
                     + (f" … et {len(_sans6) - 4} autre(s)" if len(_sans6) > 4 else ""))

    # ④ toute conformité affirmée porte sa preuve
    nus = []
    for m in CONFORMITE.finditer(t):
        # LE VRAI DÉGÂT DE P2 ÉTAIT LA PREUVE, PAS LA CACHETTE — tranché le 12-09
        # après la cassure inverse de Cowork. Sa P2 disait deux choses : un bloc
        # cachait les affirmations, ET le même bloc comptait comme leur preuve.
        # **La seconde est le dégât : elle fabrique une preuve à partir de rien.**
        # Elle est fermée par Q4 — un bloc n'est une sortie que s'il porte une
        # invite ou un code de sortie.
        # La première ne peut pas être fermée sans interdire de CITER : un relecteur
        # reproduit les livraisons fautives qu'il fabrique, et « un relecteur ne peut
        # pas citer ce qu'il casse ». **Ce qui est entre deux barrières est du texte
        # RAPPORTÉ, pas une affirmation de l'auteur.** Le choix est assumé : on
        # perd la détection d'un auteur qui cacherait ses affirmations dans un bloc
        # — mais ce bloc ne lui sert plus de preuve, donc il n'y gagne rien.
        if dans_zone(m.start(), captures) or dans_zone(m.start(), proses):
            continue
        # CITER N'EST PAS AFFIRMER. Faux positif mesuré sur ma propre livraison :
        # je NOMMAIS les mots de conformité pour décrire le contrôle — « identique,
        # conforme, complet, prouvé, inchangé » — et le programme les a pris pour
        # cinq affirmations. Un mot entre guillemets, en italique ou en code est
        # MENTIONNÉ, pas EMPLOYÉ. La distinction est une propriété du texte, pas
        # une liste d'exceptions : elle vaut pour tout mot, connu ou non.
        # Q3 : le délimiteur doit être COLLÉ au mot, pas quelque part dans le
        # voisinage. Cowork : « tes propres livraisons sont écrites en gras du début
        # à la fin : sur elles, le contrôle ④ est éteint presque partout. »
        # `**Le résultat** est identique **et complet**` passait.
        _av = t[max(0, m.start() - 2):m.start()]
        _ap = t[m.end():m.end() + 2]
        if any(_av.endswith(o) and _ap.startswith(fm)
               for o, fm in (("«", "»"), ("« ", " »"), ("*", "*"), ("`", "`"), ('"', '"'))):
            continue
        if not preuve_proche(t, m.start(), captures):
            ligne = t[:m.start()].count("\n") + 1
            nus.append(f"ligne {ligne} : « {m.group(0)} »")
    if nus:
        refus.append("CONFORMITÉ SANS PREUVE (R-720) — " + " · ".join(nus[:6])
                     + (f" … et {len(nus)-6} autre(s)" if len(nus) > 6 else ""))

    # ⑤ R-755 ② ET ③ — 30-09-2026 (A-494, décision de Jean-Luc du 29-09 à 09h36).
    # ② Tout programme dont le CODE diffère de la version officielle est vérifié par
    #   au moins une épreuve de tests/. ③ Quand la livraison modifie un programme, le
    #   document porte, pour chaque piège de R-755 ③, son intitulé suivi d'une sortie
    #   capturée qui l'écarte. Un contrôle qui ne peut pas tourner refuse (R-734).
    # la racine du DOCUMENT, jamais le repli « . » de la relance des commandes :
    # le dossier courant n'est pas forcément le dépôt livré
    _rac755 = os.path.dirname(os.path.dirname(os.path.abspath(chemin)))
    try:
        _mods, _err = programmes_modifies(_rac755)
    except Exception as _e:
        _mods, _err = None, f"{type(_e).__name__} : {_e}"
    if _err:
        refus.append(f"PROGRAMMES MODIFIÉS NON MESURÉS (R-734) — {_err}")
    else:
        _sans = []
        for _p in _mods:
            try:
                if not epreuves_de(_rac755, _p):
                    _sans.append(_p)
            except Exception as _e:
                _sans.append(f"{_p} (recherche impossible : {type(_e).__name__})")
        if _sans:
            refus.append("PROGRAMME MODIFIÉ SANS ÉPREUVE (R-755 ②) — aucune épreuve de tests/ ne le "
                         "désigne : " + " · ".join(_sans[:6])
                         + (f" … et {len(_sans)-6} autre(s)" if len(_sans) > 6 else ""))
        if _mods:
            _pieges = pieges_r755(_rac755)
            if not _pieges:
                refus.append("PIÈGES DE R-755 ③ ILLISIBLES (R-734) — la liste n'a pas pu être lue "
                             "dans gouvernance/REGISTRE_REGLES.md")
            # CHAQUE PIÈGE A SA PROPRE SORTIE (relecteur du 30-09-2026) : son intitulé en
            # GRAS, puis la première sortie capturée qui suit, à moins de 1 500 caractères,
            # sans l'intitulé en gras d'un autre piège entre les deux ; et une sortie ne
            # sert qu'à un piège. Le contrôle ne juge pas si la sortie écarte vraiment le
            # piège : il exige qu'une sortie distincte lui soit attachée.
            _gras = {}
            for _pg in _pieges:
                # L APOSTROPHE, DROITE OU TYPOGRAPHIQUE, EST UNE SEULE CLASSE (30-09-2026, 06h40) :
                # deux remplacements successifs réécrivaient la classe posée par le premier
                # (« n['['’]]emprunte ») ; un piège écrit au registre avec l apostrophe DROITE
                # — c est le cas de « n'emprunte » — ne pouvait plus être reconnu, et toute
                # livraison qui modifie un programme était refusée.
                _motif = r"\*\*\s*" + r"\s+".join("['’]".join(re.escape(x) for x in re.split(r"['’]", w))
                                                for w in _pg.split()) + r"\s*\*\*"
                _gras[_pg] = [m.end() for m in re.finditer(_motif, t, re.IGNORECASE)]
            _tous = sorted(e for v in _gras.values() for e in v)
            _manque, _prises = [], {}
            for _pg in _pieges:
                _vue = None
                for _fin in _gras[_pg]:
                    _suiv = [a for a, b in captures if _fin <= a <= _fin + 1500]
                    if not _suiv:
                        continue
                    _c = min(_suiv)
                    if any(_fin < e < _c for e in _tous):
                        continue
                    _vue = _c
                    break
                if _vue is None or _vue in _prises.values():
                    _manque.append(_pg)
                else:
                    _prises[_pg] = _vue
            if _manque:
                refus.append(f"PIÈGES DE R-755 ③ SANS SORTIE ATTACHÉE — {len(_mods)} programme(s) "
                             "modifié(s) : pour chaque piège, écrire son intitulé EN GRAS puis, dans les "
                             "1 500 caractères et avant le piège suivant, une sortie capturée à une place "
                             "qui lui est propre (le contrôle vérifie cette place, pas que la sortie écarte "
                             "le piège : c'est la relecture qui le juge) : " + " · ".join(_manque))
    print(f"  fichier : {chemin} · {len(t)} caractères · {len(captures)} sortie(s) capturée(s) · {len(proses)} bloc(s) de prose")
    if refus:
        print(f"\n  ❌ LIVRAISON REFUSÉE — {len(refus)} motif(s) :")
        for r in refus:
            print(f"     · {r}")
        print("\n  La livraison ne part pas. Corriger, puis relancer.")
        sys.exit(1)
    # P4 de Cowork : « le programme ne laisse aucune trace, donc rien ne prouve
    # qu'il a tourné — et toi non plus, à la session suivante ». La trace devient
    # une PROPRIÉTÉ DU FICHIER : une ligne en queue portant l'empreinte du texte
    # accepté. Le relecteur recalcule ; si elle diffère ou manque, la livraison
    # n'a pas été contrôlée.
    corps, _nb_marqueurs = _corps_et_marqueurs(t)
    emp = hashlib.sha256(corps.encode("utf-8")).hexdigest()[:16]
    if verifier:
        _m = _marqueur_de_queue(t)
        if not _m:
            print("  ❌ AUCUNE LIGNE DE CONTRÔLE — cette livraison n'a pas été validée")
            sys.exit(1)
        # CC DE COWORK, tours 44 puis 46 — LE CORRECTIF NE PORTAIT QUE L ECRIVAIN.
        # **123 livraisons sur 129 restent declarees falsifiees, dont 116 justes
        # a un saut de ligne pres** : elles ont ete tamponnees par l ancien
        # ecrivain, qui hachait le texte AVEC son saut final.
        # **Le lecteur accepte donc les DEUX formes** — l ancienne et la
        # nouvelle — plutot que de declarer falsifie tout l historique.
        # Ce n est pas une tolerance sur le contenu : les deux empreintes portent
        # exactement le meme texte, a un caractere de fin pres.
        _emp_ancienne = hashlib.sha256((corps + "\n").encode("utf-8")).hexdigest()[:16]
        if _m.group(1) == _emp_ancienne and _m.group(1) != emp:
            print(f"  ✅ validée et intacte · empreinte {_m.group(1)} "
                  f"(forme d avant le 14-09) · AUCUNE ÉCRITURE")
            sys.exit(0)
        if _m.group(1) != emp:
            print(f"  ❌ EMPREINTE DIFFÉRENTE — validée {_m.group(1)}, texte actuel {emp}")
            print("     La livraison a été modifiée après sa validation.")
            sys.exit(1)
        print(f"  ✅ validée et intacte · empreinte {emp} · AUCUNE ÉCRITURE")
        sys.exit(0)
    with open(chemin, "w", encoding="utf-8") as fh:
        fh.write(corps.rstrip("\n") + f"\n\n<!-- CONTROLE {emp} · "
                 f"{datetime.now(PARIS).strftime('%Y-%m-%d %H:%M')} Paris -->\n")
    print(f"  ✅ les quatre propriétés sont portées · empreinte {emp} écrite en queue")
    sys.exit(0)


if __name__ == "__main__":
    main()
