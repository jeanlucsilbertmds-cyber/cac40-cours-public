"""Relève la taille et l'empreinte d'un fichier, et rend la ligne de preuve à
écrire en tête d'un rapport.

① RÔLE — Donner à qui s'apprête à lancer un programme UNE LIGNE qui dit ce que
  pèse le fichier réellement présent et quelle est son empreinte, pour que le
  rapport porte la trace de CE QUI a tourné, et non le nom de ce qu'on croyait
  lancer. Il constate, il ne juge pas.
② CONTEXTE D'APPEL — Lancé à la main, en ligne de commande, juste avant
  d'exécuter un programme. AUCUN LANCEUR AUTOMATIQUE À CE JOUR : le 19-09-2026,
  une recherche du nom `PROUVER_L_EXECUTION` dans les deux tâches planifiées du
  dépôt — `.github/workflows/collecte_abc.yml` et
  `.github/workflows/comparer_google_abc.yml` — puis dans le dossier
  `prompts_taches/`, ne rend aucune ligne ; et `gouvernance/SOCLE.csv` le range
  ligne 141 en PRESUME, avec le motif « aucun lanceur detecte — un lancement a
  la main ne s ecrit nulle part ».
③ ENTRÉE — La ligne de commande, et rien d'autre. Quatre formes : ① aucun
  argument · ② le mot `epreuves` seul · ③ un chemin de fichier · ④ un chemin,
  une taille de référence en octets, et un début d'empreinte de référence.
④ CONDITIONS D'ENTRÉE — Le chemin doit désigner un fichier lisible. La taille de
  référence doit s'écrire en chiffres seulement. L'empreinte de référence est un
  début d'empreinte SHA-256, écrit en hexadécimal, de longueur quelconque.
⑤ SORTIE — Un code de sortie, et une ligne affichée. La ligne prend la forme
  exacte « script exécuté : 11416 octets · empreinte 58f9b746 », mesurée sur ce
  fichier même le 19-09-2026, suivie de « — conforme à la référence » ou de
  « ⚠ ÉCART : … » quand une référence est donnée.
⑥ TRAITEMENT — ① relever l'heure de Paris · ② si le premier argument est
  `epreuves`, lancer le jeu d'épreuves et sortir sur son verdict · ③ sinon, s'il
  y a au moins un argument, mesurer le fichier, composer la ligne, l'afficher et
  sortir selon la conformité · ④ sans aucun argument, afficher le mode d'emploi.
⑦ UNITÉ — Les tailles sont des NOMBRES D'OCTETS, jamais des caractères : un
  fichier de texte français compte plus d'octets que de caractères, chaque
  lettre accentuée en occupant deux, et c'est l'octet qui sépare deux copies.
  L'empreinte est un nombre hexadécimal de 64 caractères, dont 8 sont affichés.
  L'écart de taille est donné deux fois : en octets, et en POURCENT de la taille
  de référence.
⑧ POURQUOI — Un fichier recopié par un agent n'est pas recopié : il est relu et
  réécrit, en condensant. Trois mesures en quatre jours, chacune prise en
  comparant le fichier exécuté au fichier déposé : le 01-09-2026,
  `audit_ecosysteme.py` a tourné à 33 623 octets contre 62 922 déposés, soit
  47 % de perdu · le 04-09 au matin, `TENIR_LES_POSITIONS.py` à 42 300 contre
  47 483, soit 11 % · le 04-09 au soir, `audit_ecosysteme.py` à 36 263 contre
  62 922, soit 42 %. Le plus grave n'est pas la perte : le programme des
  positions amputé de 11 % a passé ses QUARANTE-DEUX contrôles de calibrage, un
  programme réécrit passant ses propres témoins réécrits. Seule l'empreinte l'a
  révélé.
  ET IL NE BLOQUE PAS, DÉLIBÉRÉMENT. Un écart d'empreinte est un fait à écrire,
  pas une décision à prendre : c'est la tâche, ou Jean-Luc, qui décide de
  poursuivre ou d'arrêter selon ce que le programme touche. Un garde-fou qui
  arrête tout sur un écart attendu devient un garde-fou qu'on désactive.
⑨ CE QUI CLOCHE —
  ① Lancé sans aucun argument, il rend 0. Mesuré le 19-09-2026 :
  `python3 programmes/PROUVER_L_EXECUTION.py` affiche ses deux lignes de mode
  d'emploi, et le code de sortie relevé juste après est 0. Une tâche qui oublie
  de passer le chemin obtient donc un pas vert alors qu'aucune mesure n'a été
  prise, et rien ne le distingue d'un contrôle réussi. Un contrôle qui n'a pas
  pu tourner rend un code de sortie non nul (R-734bis).
  ② Une mesure prise sans référence est rendue comme un succès. Mesuré le
  19-09-2026 : `PROUVER_L_EXECUTION.py programmes/PROUVER_L_EXECUTION.py`
  affiche « script exécuté : 11416 octets · empreinte 58f9b746 » et rend 0. La
  fonction `ligne_de_preuve` dit pourtant honnêtement qu'elle ne conclut pas —
  elle rend la valeur vide — et c'est le lanceur en fin de fichier qui traduit
  ce « je ne sais pas » en 0.
  ③ Ce programme a annoncé pendant des mois, dans son propre texte, être appelé
  par « toute tâche qui exécute un programme, avant de le lancer », alors
  qu'aucune tâche ne l'appelle. L'écart se lit au dépôt : `gouvernance/SOCLE.csv`
  ligne 141 porte PRESUME et « aucun lanceur detecte ». Une documentation qui
  promet plus que le code ne fait est un défaut au même titre qu'une erreur de
  calcul.
  ④ Quatre fonctions du dépôt portent le nom `trouver` et ne rendent pas la même
  chose. Celle de ce fichier prend un dossier et un motif et rend une LISTE ;
  celles de `programmes/COMMUN.py` ligne 137, `programmes/JUGE_DES_STRATEGIES.py`
  ligne 168 et `programmes/claude_FABRIQUER_LE_PILOTE.py` ligne 198 prennent une
  base et plusieurs motifs et rendent UN chemin, ou rien. Deux implémentations
  d'une même chose divergent toujours (R-708) : ici elles ont déjà divergé,
  jusqu'à la forme de ce qu'elles rendent.
  ⑤ La mesure est prise AVANT le lancement, jamais pendant. Rien ne garantit que
  le fichier mesuré est celui que l'interpréteur lira ensuite : la preuve porte
  sur l'instant de la mesure, pas sur l'exécution.
  ⑥ La ligne de preuve dit QUEL fichier a tourné, mais pas LEQUEL de plusieurs
  fichiers de même nom, parce que les empreintes de référence des programmes du
  dépôt ne sont écrites nulle part. Sans cette table de référence, la ligne
  prouve la CONSTANCE d'un passage à l'autre, jamais l'IDENTITÉ. Relevé par
  Cowork le 06-09-2026, en corrigeant un texte qui prétendait le contraire.
⑩ EFFET — N'écrit aucun fichier du dépôt et ne touche pas au réseau. Le jeu
  d'épreuves, lui, crée un dossier temporaire et y écrit cinq fichiers témoins,
  qu'il n'efface jamais.
⑪ TERMINAISON — SORT DU PROGRAMME sur trois de ses quatre chemins : 0 si la
  mesure est prise ou si toutes les épreuves passent · 1 si la mesure s'écarte
  de la référence ou si une épreuve échoue · 2 si les épreuves n'ont pas pu
  tourner. Le quatrième chemin, celui du lancement sans argument, ne sort pas
  explicitement : il tombe en fin de fichier, ce que le système traduit en 0. Et
  un de ses appels peut ne pas revenir : `peser` lève sur un fichier absent, et
  la conversion de la taille de référence lève si elle n'est pas écrite en
  chiffres — mesuré le 19-09-2026, « ValueError: invalid literal for int() with
  base 10: 'abc' », affiché en trace Python, code de sortie 1.
⑫ DÉFINITIONS
  la ligne de preuve : la ligne « script exécuté : N octets · empreinte X » que
    ce programme compose, destinée à la tête d'un rapport
  l'empreinte : le nombre SHA-256 calculé sur le contenu d'un fichier ; deux
    fichiers de même empreinte ont le même contenu
  le jeu d'épreuves : les cas de contrôle que le programme lance sur lui-même,
    avec l'argument `epreuves`
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
    étant qu'une copie de lecture
  Cowork : le relecteur du projet, qui clone le dépôt, casse le code et rend ses cassures par écrit
  la trace : la liste des sources avec leur etat — LU, ABSENT ou ILLISIBLE — et un detail chiffre, affichee en pied de page.
  un garde-fou : une limite qui, franchie, fait cesser a la strategie de prendre position tout en continuant a la mesurer.
  un motif : un morceau de nom passé à une fonction de recherche, par exemple trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
"""

import hashlib
import os
import unicodedata
import sys
from datetime import datetime
from zoneinfo import ZoneInfo


def peser(chemin):
    """Rend la taille en octets et l'empreinte du fichier présent à ce chemin.

    ① RÔLE — Produire la seule mesure sur laquelle tout ce programme est bâti :
      combien pèse le fichier qui est là, et quelle est son empreinte. Sans ces deux
      nombres, rien ne distingue un programme entier d'une copie réécrite qui porte
      le même nom.
    ② CONTEXTE D'APPEL — Trois appelants, tous dans ce fichier : `ligne_de_preuve`
      avant de composer sa ligne, `_cas_venus_du_vrai_depot` pour relever la mesure
      d'un vrai programme du dépôt, et `_epreuves` pour la confronter à un calcul
      fait autrement. Aucun appel depuis un autre programme : une recherche de
      `peser(` dans tous les fichiers `.py` du dépôt, le 19-09-2026, ne rend aucune
      ligne hors de ce fichier.
    ③ ENTRÉE — `chemin` : le chemin du fichier à mesurer. `ligne_de_preuve` y passe
      sans le modifier le chemin qu'elle a reçu, par exemple
      `programmes/PROUVER_L_EXECUTION.py` donné sur la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — Le chemin doit désigner un fichier existant et lisible.
      Un fichier absent, un dossier, ou un fichier sans droit de lecture la font
      lever.
    ⑤ SORTIE — DEUX valeurs : la taille en octets, un entier ; et l'empreinte
      SHA-256 complète, 64 caractères hexadécimaux en minuscules. Mesuré le
      19-09-2026 sur ce fichier : 11416 octets, et une empreinte commençant par
      58f9b746.
      [rend: 2]
    ⑥ TRAITEMENT — ① ouvrir le fichier en mode binaire · ② lire tout son contenu
      d'un coup · ③ rendre la longueur de ce contenu et son empreinte SHA-256.
    ⑦ UNITÉ — Un NOMBRE D'OCTETS, jamais un nombre de caractères. Un fichier de
      texte français compte plus d'octets que de caractères, chaque lettre accentuée
      en occupant deux ; comparer une taille en octets à un compte de caractères
      ferait apparaître un écart là où il n'y en a pas.
    ⑧ POURQUOI — La lecture se fait en binaire et non en texte. Lire en texte
      suppose un encodage, peut échouer sur un octet inattendu, et sur certains
      systèmes remplace les fins de ligne : deux copies identiques rendraient alors
      deux empreintes différentes, et le contrôle accuserait à tort.
      La levée sur fichier absent est voulue : une tâche qui ne trouve pas le
      programme qu'elle allait lancer ne doit pas continuer en silence, et un
      contrôle qui n'a pas pu tourner rend un code de sortie non nul (R-734bis).
    ⑨ CE QUI CLOCHE — Le fichier est chargé ENTIÈREMENT en mémoire, sans aucune
      limite de taille. Sur un programme cela ne coûte rien : le plus gros du dépôt,
      `programmes/TENIR_LES_POSITIONS.py`, pèse 99 309 octets mesurés le
      19-09-2026. Mais rien n'empêche de lui passer un fichier de données —
      `donnees/cours_maitre.csv` pèse 1 635 261 octets le même jour, et cet
      historique grandit à chaque séance sans plafond.
    ⑩ EFFET — LIT un fichier du disque, en entier. N'écrit rien, n'affiche rien, ne
      touche pas au réseau.
    ⑪ TERMINAISON — Rend la main quand le fichier est lisible. LÈVE autrement, et
      la levée n'est pas rattrapée ici : `FileNotFoundError` sur un fichier absent,
      `IsADirectoryError` sur un dossier — les deux vérifiés le 19-09-2026 — et
      `PermissionError` sans droit de lecture. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      l'empreinte : le nombre SHA-256 calculé sur le contenu d'un fichier ; deux
        fichiers de même empreinte ont le même contenu
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
    """
    with open(chemin, "rb") as f:
        contenu = f.read()
    return len(contenu), hashlib.sha256(contenu).hexdigest()


def ligne_de_preuve(chemin, taille_attendue=None, empreinte_attendue=None):
    """Compose la ligne de preuve, et dit si la mesure s'écarte d'une référence.

    ① RÔLE — Transformer deux nombres bruts en une phrase que l'on colle en tête
      d'un rapport, et dire dans le même geste si ce qui a été mesuré correspond à
      ce qui était attendu. C'est elle qui fait la différence entre « le radar a
      tourné » et « le radar ENTIER a tourné ».
    ② CONTEXTE D'APPEL — Trois appelants, tous dans ce fichier : le lanceur en fin
      de programme, une fois, avec ce qui vient de la ligne de commande ; `_epreuves`,
      quatre fois, avec une référence juste puis deux références sabotées puis
      aucune référence ; et `_cas_venus_du_vrai_depot`, deux fois, sur un vrai
      programme du dépôt.
    ③ ENTRÉE — `chemin` : le fichier à mesurer · `taille_attendue` : la taille de
      référence en octets, ou rien · `empreinte_attendue` : le début de l'empreinte
      de référence, ou rien. Depuis la ligne de commande, les deux références
      viennent des deuxième et troisième arguments, absents le plus souvent.
    ④ CONDITIONS D'ENTRÉE — Le chemin doit désigner un fichier lisible : elle ne
      vérifie rien et laisse `peser` lever. La taille de référence doit déjà être un
      entier, la conversion se faisant chez l'appelant. L'empreinte de référence est
      comparée en minuscules, sa casse n'a donc pas d'importance.
    ⑤ SORTIE — TROIS valeurs : la ligne à écrire · le verdict · l'écart en français.
      Le verdict prend TROIS formes, pas deux : vrai quand tout correspond, faux
      quand quelque chose diffère, et la valeur vide quand aucune référence n'a été
      donnée — on ne peut alors rien conclure, et c'est dit ainsi plutôt que
      supposé. L'écart est un texte vide sauf quand le verdict est faux.
      [rend: 3]
    ⑥ TRAITEMENT — ① mesurer le fichier · ② composer la ligne avec la taille et les
      8 premiers caractères de l'empreinte · ③ si aucune référence n'est donnée,
      rendre la ligne seule et le verdict vide · ④ comparer la taille, et écrire
      l'écart en octets et en pourcent · ⑤ comparer le début de l'empreinte ·
      ⑥ rendre la ligne suivie de « conforme à la référence », ou de l'écart.
    ⑦ UNITÉ — La taille est un NOMBRE D'OCTETS. L'écart est donné deux fois : en
      octets, et en POURCENT de la taille de référence. L'empreinte affichée est un
      nombre hexadécimal ramené à 8 caractères.
    ⑧ POURQUOI — Le libellé de la ligne est fixe au caractère près : c'est un texte
      destiné à être comparé d'un rapport à l'autre, et un texte qui passe par la
      tête d'un agent change de forme. Le faire écrire par un programme est ce qui
      le rend comparable.
      L'empreinte est ramenée à 8 caractères parce que la ligne se lit sur un
      téléphone : 64 caractères la feraient passer à la ligne, et 8 suffisent à
      repérer un changement.
      Le verdict vide existe pour ne pas confondre « rien ne cloche » avec « je n'ai
      rien à quoi comparer ».
    ⑨ CE QUI CLOCHE —
      ① Le signe de l'écart annonce un gain là où il y a une perte. L'écart est
      calculé comme la référence moins la mesure, puis affiché avec son signe : un
      fichier plus PETIT que prévu donne donc un plus. Mesuré le 19-09-2026 en
      rejouant l'incident du 01-09-2026, sur un fichier de 33 623 octets contre
      62 922 attendus : la sortie est « taille 33623 au lieu de 62922 (+29299
      octets, +47 %) ». Le fichier a perdu 47 % de son contenu, et la ligne qui
      dénonce cette perte affiche « +47 % ».
      ② L'empreinte de référence est comparée par DÉBUT de chaîne, sans longueur
      minimale. Mesuré le 19-09-2026 sur ce fichier, dont l'empreinte commence par
      58f9b746 : avec la référence `5`, la sortie est « conforme à la référence » et
      le code de sortie est 0. Une référence d'un seul caractère déclare donc
      conforme un fichier sur seize, quel qu'en soit le contenu.
      ③ Une référence de taille donnée seule, sans empreinte, suffit à faire écrire
      « conforme à la référence ». Deux fichiers de même taille et de contenu
      différent passent alors le contrôle — or c'est exactement ce que l'empreinte
      était censée attraper.
    ⑩ EFFET — LIT le fichier mesuré, par `peser`. N'écrit aucun fichier, n'affiche
      rien elle-même : elle rend des textes que son appelant affiche. Aucun accès
      réseau.
    ⑪ TERMINAISON — Rend la main quand le fichier est lisible, et elle ne lève pas
      elle-même. Et un de ses appels peut ne pas revenir : `peser` lève sur un
      fichier absent, un dossier ou un fichier illisible — mesuré le 19-09-2026 sur
      un chemin inexistant, « FileNotFoundError: [Errno 2] No such file or
      directory », affiché en trace Python, code de sortie 1.
      [sort: non]
    ⑫ DÉFINITIONS
      la ligne de preuve : la ligne « script exécuté : N octets · empreinte X » que ce programme compose, destinée à la tête d'un rapport
      l'empreinte : le nombre SHA-256 calculé sur le contenu d'un fichier ; deux
        fichiers de même empreinte ont le même contenu
    
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir, qui contrôle l'ensemble du système et range chacun de ses constats sous un numéro de maillon, par exemple 18-Tâches pour le contrôle des traces laissées par les tâches planifiées.
"""
    taille, empreinte = peser(chemin)
    court = empreinte[:8]
    ligne = f"script exécuté : {taille} octets · empreinte {court}"

    if taille_attendue is None and empreinte_attendue is None:
        return ligne, None, ""

    ecarts = []
    if taille_attendue is not None and taille != taille_attendue:
        perdu = taille_attendue - taille
        pourcent = (perdu / taille_attendue * 100) if taille_attendue else 0
        ecarts.append(f"taille {taille} au lieu de {taille_attendue} "
                      f"({perdu:+d} octets, {pourcent:+.0f} %)")
    if empreinte_attendue is not None and not empreinte.startswith(empreinte_attendue.lower()):
        ecarts.append(f"empreinte {court} au lieu de {empreinte_attendue[:8]}")

    if not ecarts:
        return ligne + "  — conforme à la référence", True, ""
    return ligne + "  ⚠ ÉCART : " + " · ".join(ecarts), False, " · ".join(ecarts)


def trouver(dossier, motif):
    """Cherche les fichiers dont le nom contient un motif, les deux graphies admises.

    ① RÔLE — Retrouver un fichier quand on n'est pas sûr de la façon dont son nom
      est écrit : avec des espaces ou des tirets bas, avec ou sans accents, en
      majuscules ou non. Et rendre TOUT ce qui correspond, au pluriel, pour qu'un
      nom porté par deux fichiers se voie au lieu de se cacher.
    ② CONTEXTE D'APPEL — Uniquement le jeu d'épreuves de ce fichier : `_epreuves`
      l'appelle quatre fois sur un dossier temporaire, `_cas_venus_du_vrai_depot`
      une fois sur le dossier des programmes. Aucune fonction du service rendu en
      ligne de commande ne l'appelle : ce chemin passe par `ligne_de_preuve` et
      `peser`, jamais par elle.
    ③ ENTRÉE — `dossier` : la racine à parcourir, sous-dossiers compris · `motif` :
      le morceau de nom cherché. Les épreuves y passent un dossier temporaire et des
      motifs comme `MODULE_POSITIONS`, `claude/audit_du_jour` ou `ÉTUDE 11`.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un dossier absent ne la fait pas lever : le
      parcours ne rend simplement rien, ce qui est indistinguable d'une absence de
      correspondance. Le motif est du texte, de n'importe quelle graphie.
    ⑤ SORTIE — UNE valeur : la LISTE triée des chemins trouvés, vide si rien ne
      correspond. Jamais un chemin seul.
      [rend: 1]
    ⑥ TRAITEMENT — ① ramener le motif à une forme commune : accents ôtés, tout en
      minuscules, espaces, barres, tirets et points remplacés par des tirets bas,
      répétitions réduites à un seul, bords nettoyés · ② parcourir le dossier et
      tous ses sous-dossiers · ③ pour chaque fichier, ramener à cette même forme son
      nom seul, puis son chemin relatif · ④ garder ceux dont l'un des deux contient
      le motif ramené · ⑤ rendre la liste triée.
    ⑦ UNITÉ — Un NOMBRE DE FICHIERS. Aucune grandeur physique.
    ⑧ POURQUOI — Un même fichier apparaît sous deux orthographes selon le canal par
      lequel on le lit, et les deux se ressemblent assez pour qu'une consigne fausse
      paraisse juste : `audit ecosysteme.py` avec un espace contre
      `audit_ecosysteme.py` avec un tiret bas. Quatre bascules ont été mesurées en
      vingt-quatre heures les 03 et 04-09-2026, sur un seul fichier. Tout nom de
      fichier cité dans une consigne se relève sur le fichier vivant, jamais de
      mémoire (R-719) ; cette fonction est l'outil de ce relevé.
      Elle rend une liste et non un chemin parce que rendre le premier trouvé
      cacherait le second : un nom porté par deux fichiers est un problème, et le
      problème doit sortir.
    ⑨ CE QUI CLOCHE —
      ① Le motif est cherché comme un MORCEAU de nom, jamais comme un nom entier, et
      rien n'avertit qu'il est trop court. Mesuré le 19-09-2026 :
      `trouver("programmes", "MODULE")` rend quatre chemins —
      `MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py`, `MODULE_JUGEMENT.py`,
      `MODULE_POSITIONS.py` et `MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py` — et
      `trouver(".", "a")` en rend 280. Un appelant qui reçoit plusieurs chemins ne
      peut donc pas distinguer deux graphies d'un même fichier d'un motif qui a
      simplement ratissé le dossier.
      ② Le point est ramené au tiret bas comme les espaces, donc l'extension
      disparaît de la comparaison : le motif `audit_du_jour` correspond aussi bien à
      `audit_du_jour.md` qu'à un `audit_du_jour.py` qui vivrait à côté. Deux
      fichiers de même nom et d'extensions différentes sont rendus comme s'ils
      étaient deux graphies du même.
      ③ La fonction n'est appelée que par ses propres épreuves. Le défaut qu'elle
      ferme — deux graphies d'un même nom — n'est donc fermé nulle part dans ce que
      le programme rend en service.
    ⑩ EFFET — LIT l'arborescence du dossier donné, les noms seulement, sans ouvrir
      aucun fichier. N'écrit rien, n'affiche rien, aucun accès réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas, pas même sur un dossier
      absent. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      une graphie : l'une des façons dont un même nom de fichier est écrit selon le
        canal par lequel on le lit — avec espaces ou tirets bas, avec ou sans
        accents
      le jeu d'épreuves : les cas de contrôle que le programme lance sur lui-même,
        avec l'argument `epreuves`
    
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      un motif : un morceau de nom passé à une fonction de recherche, par exemple trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    def _norm(x):
        """Ramène un nom de fichier à une forme unique, pour pouvoir le comparer.

        ① RÔLE — Permettre de retrouver un fichier quand son nom n'est pas écrit
        exactement comme il l'est sur le disque. Sans elle, une recherche de
        `COLLECTER-ABC GITHUB.py` ne trouverait pas `COLLECTER_ABC_GITHUB.py`.
        ② CONTEXTE D'APPEL — Définie dans `trouver` et appelée par elle, sur le motif
        cherché et sur chaque nom de fichier parcouru.
        ③ ENTRÉE — `x` : le texte à normaliser, un nom de fichier ou un motif de
        recherche.
        ④ CONDITIONS D'ENTRÉE — Aucune : tout ce qui peut s'écrire en texte est accepté.
        ⑤ SORTIE — UNE valeur : le texte normalisé, en minuscules, sans accents, les
        séparateurs ramenés à un souligné unique et retirés des deux bouts. Mesuré le
        20-09-2026 : `MODULE_POSITIONS.py` rend `module_positions_py`, et
        `COLLECTER-ABC GITHUB.py` rend `collecter_abc_github_py`.
          [rend: 1]
        ⑥ TRAITEMENT — ① décomposer les caractères accentués · ② retirer les accents ·
        ③ passer en minuscules · ④ remplacer espace, barre oblique, barre inverse, tiret
        et POINT par un souligné · ⑤ réduire les soulignés répétés à un seul · ⑥ retirer
        les soulignés des deux bouts.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Les noms voyagent entre un dépôt, un message dicté à la voix et une
        ligne de commande, et ne survivent pas identiques au voyage. Comparer des formes
        normalisées plutôt que des noms bruts est ce qui rend la recherche utilisable.
        ⑨ CE QUI CLOCHE — **Le POINT est traité comme un séparateur, donc l'extension
        disparaît de la comparaison** : `module_positions_py` ne distingue plus
        `MODULE_POSITIONS.py` de `MODULE_POSITIONS_py`, et un fichier compilé
        `MODULE_POSITIONS.pyc` se compare sur la même base. Ce défaut est déjà porté au
        BACKLOG sous A-432, dans la famille des recherches qui correspondent sur un
        morceau de nom. Mesuré le 20-09-2026.
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend toujours la main. Aucun de ses appels ne peut ne pas revenir.
          [sort: non]
        """
        x = unicodedata.normalize("NFD", str(x))
        x = "".join(c for c in x if unicodedata.category(c) != "Mn")
        x = x.lower()
        for sep in (" ", "/", "\\", "-", "."):
            x = x.replace(sep, "_")
        while "__" in x:
            x = x.replace("__", "_")
        return x.strip("_")

    cible = _norm(motif)
    trouves = []
    for racine, _, fichiers in os.walk(dossier):
        for f in fichiers:
            rel = os.path.relpath(os.path.join(racine, f), dossier)
            if cible in _norm(f) or cible in _norm(rel):
                trouves.append(os.path.join(racine, f))
    return sorted(trouves)


def _cas_venus_du_vrai_depot(dossier=None):
    """Construit les cas d'épreuve qui portent sur de vrais programmes du dépôt.

    ① RÔLE — Empêcher que le jeu d'épreuves ne se contente de fichiers fabriqués
      pour lui. Les vraies données de ce programme sont les vrais programmes : ce
      sont eux qu'il mesure en service, et c'est sur eux que le contrôle doit être
      tiré au moins une fois.
    ② CONTEXTE D'APPEL — `_epreuves`, une seule fois, en dernier, après les cas
      écrits à la main. Jamais appelée ailleurs.
    ③ ENTRÉE — `dossier` : le dossier des programmes à parcourir, `None` par défaut. Son unique
      appelant ne passe rien, et la fonction prend alors le dossier où vit ce
      fichier, `programmes/`.
    ④ CONDITIONS D'ENTRÉE — Le dossier doit exister et porter au moins deux fichiers
      d'extension `.py`. En dessous, elle refuse de travailler.
    ⑤ SORTIE — UNE valeur : une liste de TROIS cas, chacun formé d'un verdict vrai
      ou faux et de son libellé. Elle ne rend jamais une liste vide : soit trois
      cas, soit une levée.
      [rend: 1]
    ⑥ TRAITEMENT — ① prendre le dossier de ce fichier si aucun n'est donné ·
      ② lister les fichiers `.py` et lever s'il y en a moins de deux · ③ prendre le
      premier par ordre alphabétique, et relever sa taille et son empreinte ·
      ④ premier cas : le confronter à sa propre mesure · ⑤ deuxième cas : le
      confronter à une taille amputée de 5 000 octets et vérifier que l'écart est
      dénoncé · ⑥ troisième cas : vérifier que son nom se retrouve dans son propre
      dossier · ⑦ rendre les trois.
    ⑦ UNITÉ — Les tailles sont des NOMBRES D'OCTETS, et l'amputation d'épreuve vaut
      5 000 octets. Le minimum exigé est un NOMBRE DE FICHIERS, fixé à deux.
    ⑧ POURQUOI — Ce fichier n'ouvrait AUCUN fichier réel avant le 06-09-2026, jour
      où Cowork l'a relevé. Son chemin d'échec était donc du code inatteignable, et
      il rendait 0 comme un programme complet : n'ayant rien qui puisse manquer, il
      n'avait rien qui puisse échouer. Un jeu d'épreuves contient au moins un cas
      venu d'une vraie ligne du fichier (R-732), et un contrôle qui n'a pas pu
      tourner rend un code de sortie non nul (R-734bis) — la seconde règle était
      satisfaite ici parce que la première était violée.
      La levée sur dossier introuvable applique la même idée : un contrôle qui ne
      tourne pas est un contrôle qui échoue, jamais un contrôle qui passe.
    ⑨ CE QUI CLOCHE —
      ① Le premier cas ne peut pas échouer, et il est compté comme les autres. Il
      confronte un fichier à la mesure qu'il vient lui-même de prendre sur ce
      fichier ; son libellé le dit, « TAUTOLOGIQUE ». Mesuré le 19-09-2026, la
      sortie annonce « 14/14 cas passent » et ce cas est l'un des quatorze : le
      total annonce donc une épreuve de plus qu'il n'y en a réellement.
      ② Le vrai programme éprouvé est le premier par ordre alphabétique, jamais un
      fichier choisi. Mesuré le 19-09-2026, c'était `BANC_ESSAI.py`, 48 940 octets ; depuis son renommage du 28-09-2026, c'est `COLLECTER_ABC_GITHUB.py`, 30 972 octets. Le
      jour où un fichier `.py` de nom plus petit est déposé dans `programmes/`,
      l'épreuve change de cible sans que personne l'ait décidé ; et si ce fichier
      pèse moins de 5 000 octets, le deuxième cas se compare à une taille de
      référence négative, ce que rien ne signale.
      ③ Les deux nombres qui gouvernent la fonction — le minimum de deux fichiers et
      l'amputation de 5 000 octets — sont écrits dans le code sans qu'aucune phrase
      ne dise d'où ils viennent ni ce qui les justifie.
    ⑩ EFFET — LIT la liste des noms du dossier des programmes, et LIT EN ENTIER le
      premier fichier `.py` qu'elle y trouve : trois fois, une par mesure. N'écrit
      rien, n'affiche rien, aucun accès réseau.
    ⑪ TERMINAISON — Rend la main avec ses trois cas dans le cas normal. LÈVE
      `FileNotFoundError` quand le dossier porte moins de deux fichiers `.py`, avec
      un message qui dit que les cas venus de la vraie donnée n'ont pas tourné. Et
      un de ses appels peut ne pas revenir : `peser` lève si le fichier a disparu
      entre le listage du dossier et sa lecture.
      [sort: non]
    ⑫ DÉFINITIONS
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      le jeu d'épreuves : les cas de contrôle que le programme lance sur lui-même,
        avec l'argument `epreuves`
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
    
      Cowork : le relecteur du projet, qui clone le dépôt, casse le code et rend ses cassures par écrit
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if dossier is None:
        dossier = os.path.dirname(os.path.abspath(__file__))
    reels = sorted(f for f in os.listdir(dossier) if f.endswith(".py"))
    if len(reels) < 2:
        raise FileNotFoundError(
            f"ÉPREUVES INCOMPLÈTES : moins de deux vrais programmes dans {dossier}. "
            f"Les cas venus de la vraie donnée n'ont PAS tourné (R-732).")
    cible = os.path.join(dossier, reels[0])
    vraie_taille, vraie_emp = peser(cible)
    cas = []
    _, conf, _ = ligne_de_preuve(cible, vraie_taille, vraie_emp[:8])
    cas.append((conf is True, f"VRAI programme {reels[0]} : conforme à sa propre mesure "
                              f"(TAUTOLOGIQUE — ne peut pas échouer ; la mesure est "
                              f"éprouvée contre hashlib dans les cas manuels)"))
    _, conf, ec = ligne_de_preuve(cible, vraie_taille - 5000, vraie_emp[:8])
    cas.append((conf is False and "octets" in ec,
                f"VRAI programme amputé de 5 000 o : dénoncé"))
    cas.append((len(trouver(dossier, reels[0][:-3])) >= 1,
                f"VRAI nom retrouvé dans le vrai dossier : {reels[0]}"))
    return cas


def _epreuves():
    """Lance tous les cas d'épreuve du programme et dit s'ils passent tous.

    ① RÔLE — Donner à qui modifie ce programme le moyen de savoir en une commande si
      les quatre comportements dont tout dépend tiennent encore : mesurer juste,
      dénoncer un écart de taille, dénoncer un écart d'empreinte, et refuser de
      conclure quand il n'y a rien à quoi comparer.
    ② CONTEXTE D'APPEL — Le lanceur en fin de fichier, quand le premier argument de
      la ligne de commande est le mot `epreuves`. Jamais appelée autrement, et
      jamais pendant le service rendu.
    ③ ENTRÉE — Aucun paramètre. Elle fabrique elle-même les fichiers sur lesquels
      elle travaille.
    ④ CONDITIONS D'ENTRÉE — Le système doit permettre de créer un dossier temporaire
      et d'y écrire. Le dossier `programmes/` doit porter au moins deux fichiers
      `.py`, exigence de `_cas_venus_du_vrai_depot` qu'elle appelle en dernier.
    ⑤ SORTIE — UNE valeur : vrai si tous les cas passent, faux sinon. Elle affiche
      en plus une ligne par cas, puis le total.
      [rend: 1]
    ⑥ TRAITEMENT — ① créer un dossier temporaire et y écrire un fichier témoin de
      26 octets · ② calculer à part sa taille et son empreinte, sans passer par le
      programme · ③ vérifier que la mesure du programme donne les mêmes ·
      ④ vérifier qu'une référence juste donne le verdict conforme, et que la ligne
      commence par le libellé attendu · ⑤ saboter la taille de référence de
      5 000 octets, puis l'empreinte par `deadbeef`, et vérifier que chaque écart
      est dénoncé · ⑥ vérifier que sans référence le verdict est « on ne sait pas »
      · ⑦ écrire des fichiers aux graphies différentes et vérifier que la recherche
      les retrouve · ⑧ vérifier qu'un fichier absent fait lever · ⑨ ajouter les cas
      venus de vrais programmes · ⑩ afficher chaque cas, puis le total, et rendre le
      verdict d'ensemble.
    ⑦ UNITÉ — Un NOMBRE DE CAS pour le total. Les sabotages portent sur des
      OCTETS — 5 000 ajoutés à la taille de référence — et sur une empreinte
      remplacée par `deadbeef`.
    ⑧ POURQUOI — Les cas sont écrits à la main et non dérivés du code : une épreuve
      qui recalcule ce que le code calcule passe toujours, quoi qu'il arrive. La
      taille et l'empreinte du témoin sont donc obtenues autrement que par le
      programme, puis confrontées à ce qu'il rend.
      Et chaque comportement est éprouvé DEUX fois, une fois juste et une fois
      saboté : une épreuve qui reste verte quand on retire ce qu'elle teste n'est
      pas une preuve.
    ⑨ CE QUI CLOCHE —
      ① Le dossier temporaire n'est jamais effacé. Mesuré le 19-09-2026 : 33
      dossiers temporaires présents avant un passage, 34 après. Chaque lancement des
      épreuves laisse donc derrière lui un dossier et les cinq fichiers témoins
      qu'il contient.
      ② Le nombre de cas n'est comparé à rien. La sortie du 19-09-2026 annonce
      « 14/14 cas passent », tandis que l'action A-358 du `BACKLOG_DECISIONS.md`
      décrit ce programme au 06-09-2026 comme « 7 581 o · a305722f, 8 cas » — il
      pèse aujourd'hui 11 416 octets et porte 14 cas. Rien ne rapproche ces deux
      relevés, et rien ne signalerait la disparition d'un cas : le total afficherait
      simplement un nombre plus petit, toujours en vert.
      ③ Le service rendu n'est pas éprouvé. Tous les cas appellent les fonctions
      directement ; aucun ne lance le programme par sa ligne de commande. Les trois
      formes de la ligne de commande échappent donc aux épreuves, dont celle qui
      rend 0 sans aucun argument — mesuré le 19-09-2026.
    ⑩ EFFET — CRÉE un dossier temporaire et y ÉCRIT cinq fichiers ainsi qu'un
      sous-dossier `claude/` ; ne les efface jamais. LIT le dossier `programmes/` du
      dépôt et le premier fichier `.py` qui s'y trouve. AFFICHE une ligne par cas et
      un total. Aucun fichier du dépôt n'est modifié, aucun accès réseau.
    ⑪ TERMINAISON — Rend la main avec vrai ou faux dans le cas normal. Et un de ses
      appels peut ne pas revenir : `_cas_venus_du_vrai_depot` lève
      `FileNotFoundError` si le dossier des programmes porte moins de deux fichiers
      `.py`, et `peser` lève si un témoin a disparu. Le lanceur en fin de fichier
      rattrape ces levées et sort alors en code 2, jamais en 0.
      [sort: non]
    ⑫ DÉFINITIONS
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      un sabotage : le retrait, dans une copie du socle, de la ligne de correction qu'une épreuve donnée est censée surveiller.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
    
      l'empreinte : le nombre SHA-256 calculé sur le contenu d'un fichier ; deux fichiers de même empreinte ont le même contenu
      un témoin : un jeu de chiffres dont on connaît d'avance le résultat, employé pour prouver qu'un instrument fonctionne avant de s'en servir
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    import tempfile
    d = tempfile.mkdtemp()
    p = os.path.join(d, "temoin.py")
    contenu = b"# temoin\nprint('bonjour')\n"
    with open(p, "wb") as f:
        f.write(contenu)
    vraie_taille = len(contenu)
    vraie_empreinte = hashlib.sha256(contenu).hexdigest()

    cas = []

    t, e = peser(p)
    cas.append((t == vraie_taille and e == vraie_empreinte,
                "peser rend la vraie taille et la vraie empreinte"))

    ligne, conforme, _ = ligne_de_preuve(p, vraie_taille, vraie_empreinte[:8])
    cas.append((conforme is True, "conforme quand tout correspond"))
    cas.append((ligne.startswith("script exécuté : "),
                "la ligne commence par le libellé exact du prompt"))

    _, conforme, ecart = ligne_de_preuve(p, vraie_taille + 5000, vraie_empreinte[:8])
    cas.append((conforme is False and "octets" in ecart,
                "sabotage taille : l'écart est dénoncé"))

    _, conforme, ecart = ligne_de_preuve(p, vraie_taille, "deadbeef")
    cas.append((conforme is False and "empreinte" in ecart,
                "sabotage empreinte : l'écart est dénoncé"))

    _, conforme, _ = ligne_de_preuve(p)
    cas.append((conforme is None,
                "sans référence : on ne conclut pas, on dit qu'on ne sait pas"))

    with open(os.path.join(d, "MODULE POSITIONS.py"), "wb") as f:
        f.write(b"x")
    with open(os.path.join(d, "MODULE_POSITIONS.py"), "wb") as f:
        f.write(b"y")
    cas.append((len(trouver(d, "MODULE_POSITIONS")) == 2,
                "les deux GRAPHIES sont trouvées (ce n'est PAS le cas des homonymes)"))
    os.makedirs(os.path.join(d, "claude"), exist_ok=True)
    with open(os.path.join(d, "claude", "audit_du_jour.md"), "wb") as f:
        f.write(b"x")
    cas.append((len(trouver(d, "claude_audit_du_jour")) == 1,
                "graphie réelle des instructions v14 : claude_audit_du_jour"))
    cas.append((len(trouver(d, "claude/audit_du_jour")) == 1,
                "graphie réelle du prompt de l'audit : claude/audit_du_jour"))
    with open(os.path.join(d, "ETUDE_11_CIRCUIT.md"), "wb") as f:
        f.write(b"x")
    cas.append((len(trouver(d, "ÉTUDE 11")) == 1,
                "accent du REGISTRE contre fichier sans accent"))

    manque = False
    try:
        peser(os.path.join(d, "inexistant.py"))
    except OSError:
        manque = True
    cas.append((manque, "fichier absent : lève au lieu de continuer en silence"))

    cas.extend(_cas_venus_du_vrai_depot())

    passes = sum(1 for ok, _ in cas if ok)
    for ok, libelle in cas:
        print(f"  {'OK  ' if ok else 'FAUX'} {libelle}")
    print(f"\n  {passes}/{len(cas)} cas passent")
    return passes == len(cas)


if __name__ == "__main__":
    maintenant = datetime.now(ZoneInfo("Europe/Paris"))
    if len(sys.argv) > 1 and sys.argv[1] == "epreuves":
        print(f"PROUVER L'EXECUTION — jeu d'épreuves · {maintenant:%d-%m-%Y %Hh%M} (Paris)\n")
        try:
            sys.exit(0 if _epreuves() else 1)
        except (FileNotFoundError, OSError) as e:
            # R-734bis : un contrôle qui n'a PAS PU tourner rend 2, jamais 0.
            print(f"\n  ❌ ÉPREUVES INCOMPLÈTES : {e}")
            sys.exit(2)
    if len(sys.argv) > 1:
        ligne, conforme, _ = ligne_de_preuve(
            sys.argv[1],
            int(sys.argv[2]) if len(sys.argv) > 2 else None,
            sys.argv[3] if len(sys.argv) > 3 else None)
        print(ligne)
        sys.exit(0 if conforme is not False else 1)
    print("Usage : python3 PROUVER_L_EXECUTION.py <chemin> [taille] [empreinte]")
    print("        python3 PROUVER_L_EXECUTION.py epreuves")
