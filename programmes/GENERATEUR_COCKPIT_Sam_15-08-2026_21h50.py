#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GENERATEUR_COCKPIT — fabrique la page web que Jean-Luc ouvre pour voir l etat
du systeme, et n y ecrit aucun indicateur de performance de son cru.

① ROLE — Donner a Jean-Luc, en une seule page qui tient sur un telephone, ce
  que le systeme a produit dans la journee : y a-t-il une position ouverte, ou
  le compteur de la strategie en est-il, ce que le journal des operations
  cloturees contient, et si les garde-fous sont au vert. La page comporte six
  sections dans cet ordre : Aujourd hui, QA, Production, Laboratoire,
  Operations cloturees, Surveillance et archives. Chaque valeur affichee vient
  d un fichier, et la page nomme elle-meme, en pied de page, les fichiers qu
  elle a lus et ceux qui manquaient.
② CONTEXTE D APPEL — Un seul appelant automatique :
  programmes/PUBLIER_LE_SITE.py, qui lance ce programme en sous-processus avec
  un delai maximal de 600 secondes, lui passe deux fois le meme dossier de
  travail, puis fait chiffrer la page obtenue par une phrase secrete et la
  publie sous le nom index.html au depot public. PUBLIER_LE_SITE.py est
  lui-meme le pas n°9 du circuit du soir, a la ligne 205 du fichier de taches
  .github/workflows/collecte_abc.yml, sous le titre « Fabriquer et publier le
  cockpit en page web » ; ce fichier se declenche a 18h UTC du lundi au
  vendredi. Le programme se lance aussi a la main, en lui donnant un dossier
  de sources et un dossier de sortie.
③ ENTREE — La ligne de commande, deux elements facultatifs.
  `sys.argv[1]` : le dossier ou chercher les fichiers sources ; le dossier
  courant par defaut. `sys.argv[2]` : le dossier ou ecrire la page ; le
  dossier courant par defaut. PUBLIER_LE_SITE.py passe deux fois le meme
  chemin, celui du dossier `_site_travail` qu il vient de remplir. Aucune
  variable d environnement, aucun fichier de reglages, aucun acces reseau.
④ CONDITIONS D ENTREE — Le dossier de sortie doit exister et etre accessible
  en ecriture. Les dix sources peuvent toutes manquer : chacune est lue si
  elle est la, et son absence est tracee au lieu d arreter le programme.
  PUBLIER_LE_SITE.py renomme les fichiers avant de les copier, parce que le
  depot et ce programme ne les appellent pas pareil : le depot porte
  donnees/claude_cours_nouveaux.csv, ce programme cherche cours_nouveaux.csv.
⑤ SORTIE — Un fichier HTML ecrit sur le disque, et trois lignes affichees a l
  ecran. Le programme ne rend aucun code de sortie explicite : il se termine
  normalement, donc en code 0, ou il tombe sur une erreur non rattrapee.
⑥ TRAITEMENT — ① lire les deux chemins sur la ligne de commande · ② composer
  l horodatage de Paris et le nom du fichier a ecrire · ③ charger les dix
  sources et tracer, pour chacune, si elle a ete lue et combien de lignes elle
  portait · ④ composer les six sections et le pied de page · ⑤ ecrire la page ·
  ⑥ afficher le compte des sources lues, le contenu resume et le chemin ecrit
  avec l empreinte de la page.
⑦ UNITE — Les prix et les resultats sont en EUROS, ecrits a la francaise :
  espace pour les milliers, virgule pour les decimales. Les taux sont en
  POURCENTS. Les series de cours se comptent en SEANCES de bourse. Les
  graphiques sont dessines en PIXELS. L horodatage du titre et du nom de
  fichier est en heure de Paris. L empreinte affichee est un nombre
  hexadecimal de 16 caracteres.
⑧ POURQUOI — Trois choix commandent tout le reste.
  ① Ce programme ne calcule plus les indicateurs de performance depuis le
  15-08-2026. Taux de reussite, cumul net, serie en cours, pire chute, pertes
  consecutives, borne basse, point mort et voyants sont produits par
  programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py et simplement lus
  ici dans donnees/historique_mesures.csv. La raison : deux implementations d
  une meme chose divergent toujours (R-708) ; si le cockpit calculait de son
  cote, la page et le rapport du soir finiraient par annoncer deux taux de
  reussite differents pour la meme semaine, sans que rien ne le signale. La
  consequence pratique : si un chiffre manque a l affichage, il s ajoute au
  service qui mesure, jamais ici.
  ② Aucun chiffre n est ecrit en dur et aucune ressource n est chargee depuis
  Internet. Mesure le 20-09-2026 sur une page produite a partir des vraies
  donnees du depot, 25 496 octets : zero occurrence de `http://` ou
  `https://`, zero attribut `src=` ou `href=`, zero balise `script`, `link`,
  `img` ou `iframe`, zero `url(` dans les styles, zero `@import`, zero
  `fetch(`. Les graphiques sont des dessins SVG ecrits dans la page, et les
  polices sont nommees par famille — celles de l appareil. Une page qui
  dependrait d un serveur exterieur deviendrait illisible le jour ou ce
  serveur tomberait, et Jean-Luc la consulte depuis son telephone.
  ③ Une source absente ne fait pas tomber la page : le bloc concerne affiche
  ce qui lui manque et la page se genere quand meme. Mesure le 20-09-2026 :
  sur dix sources, trois manquaient — registre_candidates.csv,
  audit_du_jour.md et rapport_boucle_*.md — la page a ete ecrite et le bloc
  Laboratoire affiche « aucune donnee ». Un cockpit qui refuse de s afficher
  parce qu une source secondaire manque ne dit plus rien du tout.
⑨ CE QUI CLOCHE —
  ① La page publiee chaque soir affiche une mesure de la veille. Dans le
  fichier de taches .github/workflows/collecte_abc.yml, le pas « Fabriquer et
  publier le cockpit en page web » est a la ligne 200 et le pas « Mesurer la
  performance » a la ligne 213 : le cockpit est fabrique AVANT que la mesure
  du jour ne soit ecrite. Mesure le 20-09-2026 sur les vraies donnees du
  depot : la page annonce « Cours a jour : 2026-09-18 » et, deux sections plus
  bas, « Indicateurs lus dans historique_mesures.csv (mesure du 2026-09-17) ».
  Un lecteur qui compare les deux dates croit a un retard de collecte alors
  que c est l ordre des pas qui decale la mesure d un passage.
  ② CORRIGE LE 27-09-2026 POUR LE TABLEAU (defaut 3 de A-491) : chaque ligne dit
  sa strategie et sa comptabilite ; la synthese decrit toujours UNE strategie
  choisie par l ordre du fichier (voir `bloc_journal`, ⑨ ②). Constat d origine :
  le journal affiche cinq operations, et la synthese juste en dessous en
  annonce trois. Le tableau des operations cloturees affiche toutes les lignes
  de journal_trades.csv sans distinguer les deux comptabilites, alors que le
  meme trade y est ecrit une fois en « un jeton » et une fois en « jetons
  illimites ». Mesure le 20-09-2026 : le tableau affiche cinq lignes dont
  quatre fois UNIBAIL_RODAMCO au 2026-08-27 a -2 796,25 €, somme de la colonne
  -4 300,25 €, et la synthese en dessous lit dans la mesure « 1 / 3 » et
  « 1292.25 € ». Deux chiffres qui se contredisent sur le meme ecran, et rien
  ne dit lequel compte.
  ③ Le meme titre vit sous deux cles de cours qui ne se rejoignent jamais. La
  cle d une valeur est construite en mettant le nom en majuscules et en
  remplacant les tirets bas par des espaces ; les tirets ordinaires, eux,
  restent. Mesure le 20-09-2026 sur donnees/cac40_ohlcv.csv et
  donnees/claude_cours_nouveaux.csv : la cle `UNIBAIL-RODAMCO-WESTFIELD` porte
  644 seances du 2024-01-02 au 2026-07-10, la cle
  `UNIBAIL RODAMCO WESTFIELD` en porte 50 du 2026-07-13 au 2026-09-18. Un
  graphique dessine pour ce titre s arrete donc au 10 juillet, ou commence au
  13 juillet, sans aucun message.
  ④ Quatre fonctions ne sont appelees par personne, et trois d entre elles
  sont precisement les calculs que le changement du 15-08-2026 a retires :
  `stats_journal`, `pertes_consecutives`, `ic95_borne_basse` et `barre`.
  Releve le 20-09-2026 en rapprochant, dans l arbre syntaxique du fichier, les
  definitions et les appels. Elles fonctionnent toujours si on les appelle, et
  elles calculent un taux de reussite, un cumul, une serie en cours et une
  borne basse — exactement les chiffres que le service est seul a devoir
  produire. Un lecteur qui les trouve dans le fichier peut croire qu elles
  servent.
  ⑤ La page affiche sept chiffres qu elle calcule elle-meme. Mesure le
  20-09-2026 sur une page produite avec une position d essai et un audit d
  essai : « variation latente -0,2 % », « 2 ✅ · 1 ⚠️ · 1 ❌ », la largeur de la
  barre du compteur, les deux graduations en euros des axes des graphiques, le
  seuil de perte en euros dessine sur la courbe, « 30 strategie(s)
  archivee(s) », et la courbe d evolution du cumul. Aucun n est un indicateur
  de performance, mais la phrase « aucun calcul effectue ici » imprimee en bas
  des sections QA et Operations cloturees promet plus que ce que la page tient.
  ⑥ La courbe d evolution du cumul contredit le chiffre lu au-dessus d elle.
  Elle recoit les ecarts d un jour a l autre du cumul net et les re-additionne
  en partant de zero, ce qui perd la valeur de depart. Mesure le 20-09-2026
  sur les 14 releves de la strategie C5E10-OBS-V1 en comptabilite un jeton :
  la serie lue va de 6 884,75 € le 2026-08-26 a 1 292,25 € le 2026-09-17, et
  la courbe dessinee part de 0 € et finit a -5 592,50 €. Le tableau de la meme
  section affiche pourtant « 1292.25 € ».
  ⑦ Une seule valeur illisible au journal fait tomber toute la page. La
  couleur du resultat net est choisie par une conversion en nombre sans filet.
  Mesure le 20-09-2026 en remplacant le resultat de la premiere ligne de
  journal_trades.csv par le texte `n.d.` : le programme s arrete sur
  « ValueError: could not convert string to float: 'n.d.' » dans `bloc_journal`,
  sur la ligne qui choisit la couleur du resultat net,
  aucune page n est ecrite, et PUBLIER_LE_SITE.py s arrete alors en code 2
  avec « aucun cockpit fabrique ».
⑩ EFFET — ECRIT un fichier HTML dans le dossier de sortie, sous un nom qui
  porte le jour et l heure de Paris, par exemple
  `cockpit_Dim_20-09-2026_00h16.html` ; un nom deja pris serait ecrase, ce qui
  ne peut arriver que deux fois dans la meme minute. LIT jusqu a dix fichiers
  dans le dossier de sources et liste ce dossier ainsi que son sous-dossier
  `claude/`. Affiche trois lignes. AUCUN acces reseau, ni a la fabrication ni
  dans la page produite. Aucune donnee du depot n est modifiee.
⑪ TERMINAISON — Rend la main et se termine normalement, donc en code 0, quand
  la page est ecrite. Aucun appel a une sortie explicite. PEUT LEVER une
  erreur non rattrapee, qui arrete le programme sans ecrire de page : sur une
  valeur de resultat net illisible au journal, mesure le 20-09-2026 · sur un
  dossier de sources inexistant, que le parcours du dossier refuse · sur un
  dossier de sortie absent ou non accessible en ecriture. Et un de ses appels
  peut ne pas revenir : `_plus_recent` leve deliberement si la fonction
  `le_plus_recent` de programmes/COMMUN.py n a pas pu etre importee, plutot
  que de choisir un fichier par ordre alphabetique.
⑫ DEFINITIONS
  l historique des mesures : donnees/historique_mesures.csv, une ligne par
    jour, par strategie et par comptabilite, jamais reecrit.
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
  le cockpit : la page web que ce programme fabrique et que Jean-Luc ouvre
    pour voir l etat du systeme.
  le jeton : les 100 000 € simules du portefeuille, engages sur une seule
    position a la fois.
  le point mort : le taux de réussite en dessous duquel une stratégie perd de l'argent
  le service MESURER LA PERFORMANCE : programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py,
    le seul programme autorise a calculer les indicateurs de performance.
  les chiffres de reference : les resultats figes des fichiers
    golden_tests_*.json, qui servent a dire si un calcul a change de
    comportement.
  une comptabilite : la facon de compter les resultats, et il y en a deux,
    jamais additionnees — un jeton, une seule position a la fois avec 100 000
    € simules, et jetons illimites, toutes les occurrences du signal mesurees.
  une ligne de vie : une ligne de donnees/cac40_strategies.csv, qui donne l
    etat civil d une strategie a une date.
  PRODUCTION : l etat d une strategie dont le seuil d operations est atteint et les resultats conformes, donc exploitee.
  QA : l etat d une strategie validee sur l historique mais qui n a pas encore realise assez d operations reelles pour etre jugee.
  la raison : le texte court qui dit pourquoi une lecture a échoué, retenu sous le nom `motif`
  le depot : le depot GitHub ou vivent les fichiers du systeme, le projet n'en etant qu'une copie de lecture
  une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
import csv, json, os, sys, hashlib
# LE PLUS RÉCENT SE LIT DANS LA DATE, JAMAIS DANS L'ALPHABET (12-09-2026).
# Ce programme choisissait son golden et son rapport par `[-1]` alphabétique.
# Les noms commencent par le jour de la semaine : l'alphabet les mélange.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from COMMUN import le_plus_recent as _plus_recent
except Exception:
    def _plus_recent(c):
        """Refuse de choisir un fichier quand le vrai selectionneur n a pas pu etre charge.

        ① ROLE — Empecher que ce programme choisisse un fichier au hasard le jour ou
          programmes/COMMUN.py devient introuvable ou illisible. Elle remplace la
          fonction `le_plus_recent` de COMMUN.py, qui range des noms de fichiers datas
          sur la date lue dans leur nom ; cette doublure ne choisit rien, elle leve.
        ② CONTEXTE D APPEL — Elle n est definie que si l import de
          `COMMUN.le_plus_recent` echoue. Quand elle existe, `Sources.charger` l
          appelle jusqu a cinq fois : trois fois pour le fichier de chiffres de
          reference le plus recent et une fois pour le dernier rapport de boucle,
          plus une fois de plus quand le fichier de chiffres est illisible.
        ③ ENTREE — `c` : la liste de noms de fichiers entre lesquels il aurait fallu
          choisir. La valeur n est jamais regardee.
        ④ CONDITIONS D ENTREE — Aucune.
        ⑤ SORTIE — Ne rend jamais rien : elle leve toujours.
          [rend: rien]
        ⑥ TRAITEMENT — ① lever une erreur d execution portant le motif du refus.
        ⑦ UNITE — —
        ⑧ POURQUOI — Le programme choisissait auparavant son fichier de chiffres de
          reference et son rapport par le dernier element d un classement
          alphabetique. Les noms de ce projet commencent par le jour de la semaine
          abrege, et l alphabet les melange : trie, `Ven` sort toujours apres `Sam`,
          quelle que soit la date. Le 12-09-2026, ce choix a ete remplace par un
          classement sur la date lue dans le nom. La doublure leve plutot que de
          revenir en arriere : un refus bruyant vaut mieux qu un fichier perime choisi
          en silence.
        ⑨ CE QUI CLOCHE — L import est rattrape sur toute erreur, pas seulement sur
          une absence de fichier. Une faute de frappe dans programmes/COMMUN.py, qui
          ferait echouer sa lecture, produirait la meme doublure qu une absence, et le
          message affiche parlerait d une fonction « introuvable » alors qu elle est
          la et cassee. Releve le 20-09-2026 par lecture du bloc `try`
      qui importe `le_plus_recent` depuis programmes/COMMUN.py.
        ⑩ EFFET — N ecrit aucun fichier, ne touche pas au reseau, n affiche rien.
        ⑪ TERMINAISON — LEVE toujours, et l erreur n est rattrapee nulle part : elle
          arrete le programme. Aucun de ses appels ne se termine.
          [sort: oui]
        ⑫ DEFINITIONS
          les chiffres de reference : les resultats figes des fichiers
            golden_tests_*.json, qui servent a dire si un calcul a change de
            comportement.
          un rapport de boucle : le compte rendu que le circuit du soir ecrit
            apres chaque passage, sous un nom de la forme
            rapport_boucle_AAAA-MM-JJ.md.
        
          un refus : une ligne du garde-fou qui ajoute un motif à sa liste de refus et fait donc rendre le code 1
"""
        raise RuntimeError("COMMUN.le_plus_recent introuvable — refus de choisir "
                           "un fichier au hasard alphabetique")
from datetime import datetime
from zoneinfo import ZoneInfo

PARIS = ZoneInfo('Europe/Paris')
JOURS = ['Lun','Mar','Mer','Jeu','Ven','Sam','Dim']

C = dict(bg="#0b0c10", panel="#101218", line="#1e2028", txt="#e8e9f0", mut="#9ca3b0",
         dim="#44495a", blu="#5ab4ff", grn="#1db87a", red="#d94f4f", gld="#c9a227", vio="#8f7ee0")

# --------------------------------------------------------------------------
# LECTURE DES SOURCES — chacune tolerante a l'absence
# --------------------------------------------------------------------------
class Sources:
    """Porte les dix sources du cockpit une fois lues, et la trace de ce qui a ete lu.

    ① ROLE — Etre le seul endroit du programme qui touche au disque, pour que le
      reste ne fasse que de la mise en forme. Elle range les dix sources dans
      autant d attributs, et tient a cote une trace : pour chaque source, son nom,
      son etat — LU, ABSENT ou ILLISIBLE — et un detail chiffre. Cette trace est
      affichee en pied de page, ce qui permet a Jean-Luc de voir, sans ouvrir un
      fichier, sur quoi la page a ete construite.
    ② CONTEXTE D APPEL — `main`, une seule fois, avec `Sources(base).charger()`.
      L objet obtenu est ensuite passe a `construire`, qui le donne a chacune des
      six sections.
    ③ ENTREE — `base` : le dossier ou chercher les sources, recu par
      `Sources.__init__`.
    ④ CONDITIONS D ENTREE — Le dossier doit exister et pouvoir etre parcouru : son
      contenu est liste pour y trouver les fichiers de chiffres de reference et
      les rapports de boucle. Les dix sources, elles, peuvent toutes manquer.
    ⑤ SORTIE — Une instance, dont les attributs portent les sources lues :
      `trace`, `ohlcv`, `trades`, `positions`, `strategies`, `candidates`,
      `golden`, `audit`, `rapport` et `mesures`.
    ⑥ TRAITEMENT — ① `__init__` pose les dix attributs a vide · ② `charger` lit
      chaque source et remplit la trace · ③ `serie` rend, a la demande, la suite
      des cours de cloture d une valeur.
    ⑦ UNITE — Les cours sont en EUROS et se comptent en SEANCES de bourse. Les
      autres sources se comptent en LIGNES de fichier. Le detail de la trace des
      textes se compte en CARACTERES.
    ⑧ POURQUOI — Rassembler la lecture en un seul objet evite que dix fonctions d
      affichage ouvrent chacune les memes fichiers, avec dix facons differentes de
      traiter une absence. La trace est construite en meme temps que la lecture,
      et jamais apres : c est la seule facon qu elle dise ce qui s est reellement
      passe. Mesure le 20-09-2026 sur les vraies donnees du depot : la trace
      annonce « 7/10 lues » et nomme les trois absentes.
    ⑨ CE QUI CLOCHE — La classe ne porte aucune verification de coherence entre
      ses sources. Le journal des operations et l historique des mesures sont lus
      cote a cote sans jamais etre confrontes, et le 20-09-2026 le premier porte
      cinq lignes quand le second annonce trois operations pour la meme strategie.
      La page affiche les deux sans le dire.
    ⑩ EFFET — LIT jusqu a dix fichiers, et liste le dossier de base ainsi que son
      sous-dossier `claude/`. N ecrit aucun fichier, ne touche pas au reseau.
    ⑪ TERMINAISON — La construction rend la main. `charger` peut lever sur un
      dossier de base inexistant. Un de ses appels peut ne pas revenir :
      `_plus_recent` leve deliberement quand programmes/COMMUN.py n a pas pu etre
      importe.
    ⑫ DEFINITIONS
      l historique des mesures : donnees/historique_mesures.csv, une ligne par
        jour, par strategie et par comptabilite, jamais reecrit.
      la trace : la liste des sources avec leur etat — LU, ABSENT ou ILLISIBLE
        — et un detail chiffre, affichee en pied de page.
      le cockpit : la page web que ce programme fabrique et que Jean-Luc ouvre
        pour voir l etat du systeme.
      les chiffres de reference : les resultats figes des fichiers
        golden_tests_*.json, qui servent a dire si un calcul a change de
        comportement.
    """
    def __init__(self, base):
        """Pose a vide les dix attributs qui porteront les sources.

        ① ROLE — Garantir que les dix sources existent comme attributs avant meme que
          la lecture commence, pour qu une section qui interroge une source absente
          trouve une liste vide et non une erreur. Sans cela, le bloc Laboratoire
          tomberait chaque fois que registre_candidates.csv manque — ce qui est le cas
          au depot le 20-09-2026.
        ② CONTEXTE D APPEL — Le langage lui-meme, a la construction de l objet, dans
          `main`, une seule fois : `Sources(base).charger()`. Jamais appelee par son
          nom.
        ③ ENTREE — `self` : l objet en cours de construction. `base` : le dossier ou
          chercher les sources. Un seul appelant, `main`, et il passe le premier
          argument de la ligne de commande, ou le dossier courant quand aucun argument
          n est donne ; PUBLIER_LE_SITE.py y passe le chemin de son dossier
          `_site_travail`.
        ④ CONDITIONS D ENTREE — Aucune. Le dossier n est ni ouvert ni verifie ici ;
          `charger` s en charge.
        ⑤ SORTIE — Ne rend rien. Elle pose onze attributs sur l objet : `base`,
          `trace`, `ohlcv`, `trades`, `positions`, `strategies`, `candidates`,
          `golden`, `audit`, `rapport` et `mesures`.
          [rend: rien]
        ⑥ TRAITEMENT — ① retenir le dossier de base · ② poser la trace a liste vide ·
          ③ poser les cours a dictionnaire vide · ④ poser les cinq sources tabulaires
          a listes vides · ⑤ poser les chiffres de reference a dictionnaire vide ·
          ⑥ poser les deux textes a la valeur `None`.
        ⑦ UNITE — —
        ⑧ POURQUOI — Les valeurs de depart ne sont pas toutes du meme genre, et c est
          voulu : les sources tabulaires partent a liste vide parce que les sections
          les parcourent et qu une liste vide se parcourt sans rien produire, tandis
          que les deux textes partent a `None` parce que les sections testent leur
          presence pour choisir un message. Mesure le 20-09-2026 : le bloc
          Aujourd hui affiche « Rapport automatique indisponible » parce que
          `rapport` vaut encore `None` apres chargement.
        ⑨ CE QUI CLOCHE — Rien vu.
        ⑩ EFFET — Modifie l objet en cours de construction, et rien d autre. N ecrit
          aucun fichier, ne lit rien, ne touche pas au reseau.
        ⑪ TERMINAISON — Rend toujours la main. Elle ne leve pas. Aucun de ses appels
          ne se termine.
          [sort: non]
        ⑫ DEFINITIONS
          la trace : la liste des sources avec leur etat — LU, ABSENT ou
            ILLISIBLE — et un detail chiffre, affichee en pied de page.
          les chiffres de reference : les resultats figes des fichiers
            golden_tests_*.json, qui servent a dire si un calcul a change de
            comportement.
        """
        self.base = base
        self.trace = []      # (nom affiche, statut, detail)
        self.ohlcv = {}      # valeur -> [(date, close, high, low, open)]
        self.trades = []     # journal des operations cloturees
        self.positions = []  # positions ouvertes
        self.strategies = [] # registre d'etat civil
        self.candidates = [] # file d'idees
        self.golden = {}     # chiffres de reference figes
        self.audit = None    # texte de l'audit du jour
        self.rapport = None  # texte du dernier rapport de boucle
        self.mesures = []    # historique des mesures : LA source des indicateurs

    def _p(self, *noms):
        """Rend le premier chemin qui existe parmi plusieurs graphies d un meme fichier.

        ① ROLE — Retrouver un fichier source quelle que soit la facon dont il a ete
          nomme ou range. Le meme fichier porte en effet des noms differents selon l
          endroit : au depot il s appelle donnees/claude_cours_nouveaux.csv, dans les
          anciens dossiers claude/cours_nouveaux.csv, et ce programme le cherche sous
          cours_nouveaux.csv. Sans ce rattrapage, une source presente serait declaree
          absente et son bloc s afficherait vide.
        ② CONTEXTE D APPEL — `Sources.charger`, sept fois, une par source nommee :
          les deux fichiers de cours, le journal des operations, les positions
          ouvertes, l etat civil des strategies, la file d idees, l audit du jour et l
          historique des mesures. Jamais appelee ailleurs.
        ③ ENTREE — `self` : l objet qui porte le dossier de base. `*noms` : un ou
          plusieurs noms de fichier a essayer. Tous les appels n en passent qu un
          seul, par exemple `historique_mesures.csv`.
        ④ CONDITIONS D ENTREE — Aucune. Un nom qui ne correspond a rien rend
          simplement `None`.
        ⑤ SORTIE — UNE valeur : le chemin complet du premier fichier trouve, ou la
          valeur `None` si aucune des graphies n existe.
          [rend: 1]
        ⑥ TRAITEMENT — ① pour chaque nom propose, essayer quatre graphies dans cet
          ordre : le nom tel quel, le nom avec les tirets bas remplaces par des
          espaces, le nom precede de `claude/`, le nom precede de `claude_` ·
          ② joindre chaque graphie au dossier de base et rendre la premiere qui
          existe · ③ rendre `None` si aucune n existe.
        ⑦ UNITE — —
        ⑧ POURQUOI — L ordre des quatre graphies n est pas neutre : le nom tel quel
          passe en premier, donc un fichier range a plat gagne toujours contre le meme
          nom range dans `claude/`. C est ce que veut PUBLIER_LE_SITE.py, qui copie
          les sources a plat dans son dossier de travail sous les noms que ce
          programme attend, en retirant le prefixe `claude_` du depot. Deux fichiers
          de meme nom a deux endroits sont un defaut et jamais une intention : l un
          recoit les ecritures, l autre est lu, et rien ne le dit.
        ⑨ CE QUI CLOCHE — La graphie `claude/` + nom est essayee telle quelle, sans
          la variante a espaces, alors que les trois autres graphies s appliquent au
          nom d origine. Un fichier range en `claude/cours nouveaux.csv` ne serait
          donc pas trouve, la ou `cours nouveaux.csv` a plat le serait. Releve le 20-09-2026 par lecture
      de la boucle qui essaie les quatre graphies.
        ⑩ EFFET — Interroge le disque pour savoir si un chemin existe. N ouvre aucun
          fichier, n ecrit rien, ne touche pas au reseau.
        ⑪ TERMINAISON — Rend toujours la main. Elle ne leve pas. Aucun de ses appels
          ne se termine.
          [sort: non]
        ⑫ DEFINITIONS
          le depot : le depot GitHub ou vivent les fichiers du systeme, le projet n'en etant qu'une copie de lecture
        
          l audit du jour : le compte rendu du programme de surveillance, qui dit ce qui est vert, ce qui avertit et ce qui a echoue.
          l etat civil : donnees/cac40_strategies.csv, qui donne pour chaque strategie son objectif, son seuil de perte, son horizon et son etat de vie.
          la boucle : la tache planifiee qui lit les signaux et rend compte
          la file d idees : registre_candidates.csv, la liste des strategies a l etude, qui n engagent aucun argent.
          une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
        for n in noms:
            for cand in (n, n.replace('_', ' '), 'claude/' + n, 'claude_' + n):
                c = os.path.join(self.base, cand)
                if os.path.exists(c):
                    return c
        return None

    def _lire_csv(self, chemin):
        """Lit un fichier tabulaire en entier et rend ses lignes sous forme de
        dictionnaires.

        ① ROLE — Donner une seule facon de lire les cinq sources tabulaires du
          cockpit, pour qu elles soient toutes ouvertes avec le meme jeu de
          caracteres et la meme gestion des fins de ligne. Sans cela, un fichier
          ecrit par un tableur avec sa marque d ordre d octets en tete ferait
          apparaitre un premier nom de colonne inutilisable, du genre `﻿date`, et
          la colonne serait introuvable pour toutes les sections.
        ② CONTEXTE D APPEL — `Sources.charger`, cinq fois : journal des operations
          cloturees, positions ouvertes, etat civil des strategies, file d idees,
          historique des mesures. Jamais appelee ailleurs.
        ③ ENTREE — `self` : l objet qui porte les sources. `chemin` : le chemin
          complet du fichier a lire. Il vient toujours de `Sources._p`, donc il existe
          au moment de l appel.
        ④ CONDITIONS D ENTREE — Le fichier doit exister, se lire en UTF-8 et porter
          une premiere ligne d en-tetes : ce sont ces en-tetes qui deviennent les cles
          de chaque ligne.
        ⑤ SORTIE — UNE valeur : la liste de toutes les lignes du fichier, chacune sous
          forme de dictionnaire dont les cles sont les en-tetes. Une liste vide si le
          fichier ne porte que ses en-tetes. Mesure le 20-09-2026 sur
          donnees/claude_journal_trades.csv : cinq lignes de douze colonnes.
          [rend: 1]
        ⑥ TRAITEMENT — ① ouvrir le fichier en UTF-8 en retirant une eventuelle marque
          d ordre d octets · ② le lire en entier, ligne a ligne, en rapprochant chaque
          valeur de son en-tete · ③ rendre la liste obtenue.
        ⑦ UNITE — Un NOMBRE DE LIGNES.
        ⑧ POURQUOI — Le fichier est charge d un coup, et non parcouru au fil de l eau,
          parce que les sections le relisent plusieurs fois : le journal des operations
          est parcouru une fois pour le tableau et une autre pour le dernier titre
          traite. Les tailles le permettent : le plus gros fichier tabulaire du depot
          le 20-09-2026, donnees/cac40_ohlcv.csv, n est pas lu par cette fonction mais
          par un parcours dedie.
        ⑨ CE QUI CLOCHE — Aucune erreur n est rattrapee. Un fichier efface entre le
          moment ou `Sources._p` le trouve et le moment ou cette fonction l ouvre, ou
          un fichier dont l encodage n est pas de l UTF-8, fait tomber le programme
          sans qu aucune page ne soit ecrite — alors que toutes les autres sources
          sont lues de facon tolerante a l absence. Releve le 20-09-2026 par lecture
      du corps de cette fonction, qui ouvre le fichier sans aucun rattrapage.
        ⑩ EFFET — OUVRE et LIT un fichier. N ecrit rien, ne touche pas au reseau.
        ⑪ TERMINAISON — Rend la main dans le cas normal. PEUT LEVER sur un fichier
          disparu ou mal encode, et cette erreur n est rattrapee nulle part : elle
          arrete le programme. Aucun de ses appels ne se termine.
          [sort: non]
        ⑫ DEFINITIONS
          le cockpit : la page web que ce programme fabrique et que Jean-Luc
            ouvre pour voir l etat du systeme.
          le depot : le depot GitHub ou vivent les fichiers du systeme, le projet n'en etant qu'une copie de lecture
        
          une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
        with open(chemin, encoding='utf-8-sig', newline='') as f:
            return list(csv.DictReader(f))

    def charger(self):
        # --- cours : historique fige + cours du jour, fusionnes ---
        """Lit les dix sources du cockpit et tient la trace de ce qui a ete lu.

        ① ROLE — Faire tout le travail de disque du programme en une fois, et laisser
          derriere elle deux choses : les sources rangees dans les attributs de l
          objet, et une trace qui dit, source par source, si elle a ete lue, si elle
          manquait ou si elle etait illisible, avec un detail chiffre. Cette trace est
          affichee en pied de la page, ce qui permet de savoir sur quoi la page a ete
          batie sans ouvrir un seul fichier.
        ② CONTEXTE D APPEL — `main`, une seule fois, enchainee a la construction :
          `Sources(base).charger()`. Jamais appelee ailleurs.
        ③ ENTREE — `self` : l objet qui porte le dossier de base et les dix attributs
          a remplir. Aucun autre parametre.
        ④ CONDITIONS D ENTREE — Le dossier de base doit exister et pouvoir etre
          parcouru : son contenu est liste deux fois, pour y chercher les fichiers de
          chiffres de reference et les rapports de boucle. Les dix sources peuvent
          toutes manquer.
        ⑤ SORTIE — UNE valeur : l objet lui-meme, pour que l appelant puisse enchainer
          la construction et le chargement en une seule expression.
          [rend: 1]
        ⑥ TRAITEMENT — ① lire le fichier maître des cours dans un dictionnaire, en
          ignorant les lignes illisibles ; son absence arrête (A-442) · ② lire le journal des
          operations cloturees · ③ lire les positions ouvertes · ④ lire l etat civil
          des strategies · ⑤ lire la file d idees · ⑥ choisir le fichier de chiffres
          de reference le plus recent par la date de son nom, et le lire · ⑦ lire le
          texte de l audit du jour · ⑧ lire l historique des mesures et compter sur
          combien de jours il porte · ⑨ choisir le dernier rapport de boucle, a plat
          ou dans `claude/`, et le lire · ⑩ rendre l objet.
        ⑦ UNITE — Les cours sont en EUROS et se comptent en SEANCES de bourse. Les
          sources tabulaires se comptent en LIGNES. Les deux textes se comptent en
          CARACTERES. L historique des mesures se compte en MESURES et en JOURS.
        ⑧ POURQUOI — Trois choix commandent le reste.
          ① Une ligne de cours illisible est ignoree, jamais devinee : un cours
          manquant vaut mieux qu un cours invente, puisque la page sert a decider s il
          faut prendre position.
          ② **[RÉGLÉ LE 24-09-2026, A-442 : plus aucun repli ; le maître seul, et son absence arrête.]** Les deux fichiers de cours sont fondus dans le meme dictionnaire, l
          historique fige d abord et les cours recents ensuite, si bien que le plus
          recent gagne sur la meme date. C est ce qu il faut : le fichier des cours
          recents porte les seances que la collecte du soir vient d ecrire.
          ③ Le fichier de chiffres de reference et le rapport de boucle sont choisis
          sur la date lue dans leur nom, et non par ordre alphabetique. Les noms de ce
          projet commencent par le jour de la semaine abrege, et l alphabet les
          melange : trie, `Ven` sort toujours apres `Sam`, quelle que soit la date. Ce
          defaut a ete corrige le 12-09-2026.
        ⑨ CE QUI CLOCHE —
          ① Le meme titre vit sous deux cles qui ne se rejoignent jamais. La cle est
          construite en mettant le nom en majuscules et en remplacant les tirets bas
          par des espaces ; les tirets ordinaires restent. Mesure le 20-09-2026 sur
          donnees/cac40_ohlcv.csv et donnees/claude_cours_nouveaux.csv : la cle
          `UNIBAIL-RODAMCO-WESTFIELD` porte 644 seances du 2024-01-02 au 2026-07-10,
          la cle `UNIBAIL RODAMCO WESTFIELD` en porte 50 du 2026-07-13 au 2026-09-18.
          Les deux moities de l historique de ce titre ne se rencontrent jamais, et
          aucun message ne le dit.
          ② Les fichiers de chiffres de reference sont classes par ordre alphabetique
          avant d etre confies au selectionneur par date. Le classement alphabetique
          ne sert a rien et laisse croire a un lecteur presse que le choix se fait
          ainsi — c est precisement le defaut corrige le 12-09-2026. Releve le 20-09-2026 sur la ligne
      qui range les fichiers de chiffres de reference par ordre alphabetique
      avant de les confier au selectionneur par date.
          ③ Les chiffres de reference sont lus et traces, mais aucune section de la
          page ne les affiche. Releve le 20-09-2026 en cherchant l attribut `golden`
          dans le reste du fichier : il n apparait nulle part apres son chargement. La
          trace du pied de page annonce donc une source « LU » avec son compte de
          strategies de reference, alors que rien de ce fichier n atteint la page.
          ④ Le dernier rapport de boucle est lu, trace, et sa presence sert seulement
          a choisir entre deux phrases dans le bloc Aujourd hui. Son contenu n est
          jamais affiche ni analyse. La trace du 20-09-2026 le montre quand il est
          present : « LU, N caracteres », sans qu aucun de ces caracteres n arrive
          dans la page.
        ⑩ EFFET — LIT jusqu a dix fichiers et LISTE deux dossiers, celui de base et
          son sous-dossier `claude/`. Remplit les dix attributs de l objet. N ecrit
          aucun fichier, ne touche pas au reseau, n affiche rien.
        ⑪ TERMINAISON — Rend la main dans le cas normal. LEVE `FileNotFoundError` si le fichier maitre des cours manque, ou s il ne porte aucun cours lisible (A-471) — voulu, A-442. PEUT LEVER sur un dossier de
          base inexistant, et sur un fichier tabulaire disparu ou mal encode. Et un de
          ses appels peut ne pas revenir : `_plus_recent` leve deliberement quand la
          fonction `le_plus_recent` de programmes/COMMUN.py n a pas pu etre importee,
          plutot que de choisir un fichier par ordre alphabetique.
          [sort: non]
        ⑫ DEFINITIONS
          l historique des mesures : donnees/historique_mesures.csv, une ligne
            par jour, par strategie et par comptabilite, jamais reecrit.
          la trace : la liste des sources avec leur etat — LU, ABSENT ou
            ILLISIBLE — et un detail chiffre, affichee en pied de page.
          le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
          le cockpit : la page web que ce programme fabrique et que Jean-Luc
            ouvre pour voir l etat du systeme.
          les chiffres de reference : les resultats figes des fichiers
            golden_tests_*.json, qui servent a dire si un calcul a change de
            comportement.
          un rapport de boucle : le compte rendu que le circuit du soir ecrit
            apres chaque passage, sous un nom de la forme
            rapport_boucle_AAAA-MM-JJ.md.
          une ligne de vie : une ligne de donnees/cac40_strategies.csv, qui
            donne l etat civil d une strategie a une date.
        
          l audit du jour : le compte rendu du programme de surveillance, qui dit ce qui est vert, ce qui avertit et ce qui a echoue.
          la file d idees : registre_candidates.csv, la liste des strategies a l etude, qui n engagent aucun argent.
          le fichier des cours : le fichier où les séances s'empilent sans jamais être réécrites ; au dépôt, c'est donnees/claude_cours_nouveaux.csv.
          une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle a tourné — rapport de boucle, rapport d'audit, cockpit, historique des mesures.
          une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
        for fic, lab in (('cours_maitre.csv', 'fichier maitre des cours'),):
            ch = self._p(fic)
            if not ch:
                # PLUS DE MODE DEGRADE SUR LES COURS — A-442 : leur absence arrete.
                raise FileNotFoundError(
                    "ARRET : le fichier maitre des cours, cours_maitre.csv, est "
                    "introuvable. Aucun repli sur les anciens fichiers de cours (A-442).")
            n = 0
            with open(ch, encoding='utf-8-sig', newline='') as f:
                for r in csv.DictReader(f):
                    try:
                        val = r['valeur'].strip().upper().replace('_', ' ')
                        self.ohlcv.setdefault(val, {})[r['date']] = (
                            float(r['close']), float(r['high']), float(r['low']), float(r['open']))
                        n += 1
                    except (KeyError, ValueError, TypeError):
                        continue      # ligne illisible : ignoree, jamais devinee
            if n == 0:
                # UN MAITRE VIDE ARRETE, COMME UN MAITRE ABSENT (A-471, 24-09-2026).
                raise FileNotFoundError(
                    "ARRET : le fichier maitre des cours, cours_maitre.csv, ne porte aucun cours lisible.")
            self.trace.append((os.path.basename(ch), 'LU', f'{n} lignes ({lab})'))

        # --- journal des operations cloturees ---
        ch = self._p('journal_trades.csv')
        if ch:
            self.trades = self._lire_csv(ch)
            self.trace.append((os.path.basename(ch), 'LU', f'{len(self.trades)} operations cloturees'))
        else:
            self.trace.append(('journal_trades.csv', 'ABSENT', 'journal vide affiche'))

        # --- positions ouvertes ---
        ch = self._p('positions_ouvertes.csv')
        if ch:
            self.positions = self._lire_csv(ch)
            self.trace.append((os.path.basename(ch), 'LU', f'{len(self.positions)} position(s) ouverte(s)'))
        else:
            self.trace.append(('positions_ouvertes.csv', 'ABSENT', 'etat du jeton indetermine'))

        # --- registre d'etat civil des strategies ---
        ch = self._p('cac40_strategies.csv')
        if ch:
            self.strategies = self._lire_csv(ch)
            self.trace.append((os.path.basename(ch), 'LU', f'{len(self.strategies)} lignes de vie'))
        else:
            self.trace.append(('cac40_strategies.csv', 'ABSENT', 'cartes d identite indisponibles'))

        # --- file d idees ---
        ch = self._p('registre_candidates.csv')
        if ch:
            self.candidates = self._lire_csv(ch)
            self.trace.append((os.path.basename(ch), 'LU', f'{len(self.candidates)} idees en file'))
        else:
            self.trace.append(('registre_candidates.csv', 'ABSENT', 'laboratoire vide affiche'))

        # --- chiffres de reference figes (golden) : nom date, on prend le plus recent ---
        gold = sorted([f for f in os.listdir(self.base) if f.startswith('golden_tests') and f.endswith('.json')])
        if gold:
            ch = os.path.join(self.base, _plus_recent(gold))
            try:
                self.golden = json.load(open(ch, encoding='utf-8'))
                self.trace.append((_plus_recent(gold), 'LU', f'{len([k for k in self.golden if k != "meta"])} strategie(s) de reference'))
            except json.JSONDecodeError as e:
                self.trace.append((_plus_recent(gold), 'ILLISIBLE', str(e)[:60]))
        else:
            self.trace.append(('golden_tests_*.json', 'ABSENT', 'references non opposables'))

        # --- audit du jour + dernier rapport de boucle (textes) ---
        ch = self._p('audit_du_jour.md')
        if ch:
            self.audit = open(ch, encoding='utf-8').read()
            self.trace.append((os.path.basename(ch), 'LU', f'{len(self.audit)} caracteres'))
        else:
            self.trace.append(('audit_du_jour.md', 'ABSENT', 'verdict de controle indisponible'))

        # --- HISTORIQUE DES MESURES : la source unique des indicateurs (A-208) ---
        ch = self._p('historique_mesures.csv')
        if ch:
            self.mesures = self._lire_csv(ch)
            jours = sorted({m.get('date_mesure', '') for m in self.mesures})
            self.trace.append((os.path.basename(ch), 'LU',
                               f'{len(self.mesures)} mesures sur {len(jours)} jour(s)'))
        else:
            self.mesures = []
            self.trace.append(('historique_mesures.csv', 'ABSENT',
                               'AUCUN indicateur affichable — le service MESURER LA PERFORMANCE n a pas tourne'))

        raps = sorted([f for f in os.listdir(self.base) if 'rapport_boucle' in f])
        cl = os.path.join(self.base, 'claude')
        if os.path.isdir(cl):
            raps += sorted(['claude/' + f for f in os.listdir(cl) if 'rapport_boucle' in f])
        if raps:
            ch = os.path.join(self.base, _plus_recent(raps))
            self.rapport = open(ch, encoding='utf-8').read()
            self.trace.append((os.path.basename(ch), 'LU', f'{len(self.rapport)} caracteres'))
        else:
            self.trace.append(('rapport_boucle_*.md', 'ABSENT', 'signal du jour indetermine'))
        return self

    def serie(self, valeur):
        """Rend la suite datee des cours de cloture d une valeur, triee du plus ancien au
        plus recent.

        ① ROLE — Fournir aux deux fonctions de dessin la seule forme de donnee qu
          elles savent tracer : une liste de couples date et cours de cloture, rangee
          dans l ordre du temps. C est le seul usage des cours dans ce programme —
          ils servent a DESSINER, jamais a calculer un indicateur de performance.
        ② CONTEXTE D APPEL — Deux appelants : `bloc1_aujourdhui`, une fois, pour la
          valeur de la position ouverte · `bloc_strategie`, une fois, pour la valeur
          de la derniere operation du journal.
        ③ ENTREE — `self` : l objet qui porte les cours charges. `valeur` : le nom du
          titre, tel qu il est ecrit dans la source qui l a nomme — le fichier des
          positions ouvertes ou le journal des operations, par exemple
          `BUREAU_VERITAS`.
        ④ CONDITIONS D ENTREE — Aucune. Un nom inconnu rend une liste vide.
        ⑤ SORTIE — UNE valeur : une liste de couples, chacun fait d une date au format
          annee-mois-jour et d un cours de cloture. Liste vide quand le titre n est
          pas connu. Mesure le 20-09-2026 : `BUREAU_VERITAS` rend 694 seances.
          [rend: 1]
        ⑥ TRAITEMENT — ① mettre le nom recu en majuscules, retirer les espaces des
          bords et remplacer les tirets bas par des espaces · ② chercher cette cle
          dans les cours charges, et prendre un dictionnaire vide si elle est absente ·
          ③ rendre les couples date et cours de cloture, ranges par date.
        ⑦ UNITE — Les cours sont en EUROS. La longueur de la liste se compte en
          SEANCES de bourse.
        ⑧ POURQUOI — Le tri se fait sur la date ecrite en annee-mois-jour, ce qui
          range correctement sans avoir a convertir en date. Seul le cours de cloture
          est rendu, sur les quatre que porte chaque seance : les graphiques tracent
          une ligne, et le plus haut, le plus bas et l ouverture n y seraient pas
          dessines.
        ⑨ CE QUI CLOCHE — La normalisation du nom ne traite que les tirets bas, et le
          titre cherche peut alors rester introuvable alors que ses cours sont la.
          Mesure le 20-09-2026 : la derniere operation de
          donnees/claude_journal_trades.csv porte le nom `UNIBAIL_RODAMCO`, la
          fonction cherche donc `UNIBAIL RODAMCO`, et les fichiers de cours
          connaissent `UNIBAIL-RODAMCO-WESTFIELD` et `UNIBAIL_RODAMCO_WESTFIELD`. La
          fonction rend zero seance, et `bloc_strategie` renonce alors au graphique
          sans afficher le moindre message — le message « cours indisponibles »
          existe pourtant dans `courbe_cours`, mais il n est jamais atteint. Le meme
          fichier porte une autre facon de rapprocher deux noms, `_corr`, qui retire
          tout ce qui n est ni lettre ni chiffre ; deux normalisations differentes
          cohabitent donc dans un seul programme.
        ⑩ EFFET — LIT les cours deja charges en memoire. N ouvre aucun fichier, n
          ecrit rien, ne touche pas au reseau.
        ⑪ TERMINAISON — Rend toujours la main. Elle ne leve pas. Aucun de ses appels
          ne se termine.
          [sort: non]
        ⑫ DEFINITIONS
          une seance : une journee de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa cloture et son volume
        """
        d = self.ohlcv.get(valeur.strip().upper().replace('_', ' '), {})
        return sorted((k, v[0]) for k, v in d.items())

# --------------------------------------------------------------------------
# CALCULS — aucun chiffre affiche qui ne sorte d'ici ou d'une source
# --------------------------------------------------------------------------
def f_eur(x, signe=True):
    """Met un montant en euros a la francaise, ou rend « n.d. » si le montant est
    illisible.

    ① ROLE — Donner aux montants de la page une seule ecriture, celle que Jean-Luc
      lit sur ses releves : espace pour les milliers, virgule pour les decimales,
      symbole euro a la fin. Sans elle, un resultat de 6884.75 s afficherait tel
      quel, avec un point decimal anglais, a cote de montants ecrits autrement.
    ② CONTEXTE D APPEL — Deux appelants : `bloc1_aujourdhui`, une fois, pour le
      prix d entree de la position ouverte · `bloc_journal`, trois fois par
      operation du journal, pour le prix d entree, le prix de sortie et le
      resultat net.
    ③ ENTREE — `x` : le montant a mettre en forme, tel qu il sort du fichier,
      donc le plus souvent un texte comme `-2796.25`. `signe` : vaut `True` par
      defaut, et decide si un montant positif recoit un signe plus devant.
      `bloc1_aujourdhui` et `bloc_journal` passent `False` pour les prix, et
      laissent la valeur par defaut pour le resultat net.
    ④ CONDITIONS D ENTREE — Aucune. Une valeur vide, absente ou non numerique est
      acceptee et donne « n.d. ».
    ⑤ SORTIE — UNE valeur : un texte. Le montant mis en forme, par exemple
      `+1 234,50 €` ou `-2 796,25 €`, ou le texte `n.d.` quand la conversion en
      nombre echoue. Mesure le 20-09-2026 : `f_eur(1234.5)` rend `+1 234,50 €`,
      `f_eur(-2796.25)` rend `-2 796,25 €`, `f_eur(0)` rend `0,00 €`,
      `f_eur(None)` rend `n.d.`.
      [rend: 1]
    ⑥ TRAITEMENT — ① convertir en nombre, et rendre « n.d. » si la conversion
      echoue · ② choisir le signe plus si le montant est strictement positif et
      que l appelant l a demande · ③ ecrire le nombre avec deux decimales et une
      virgule anglaise comme separateur de milliers · ④ remplacer cette virgule
      par une espace, puis le point decimal par une virgule.
    ⑦ UNITE — Des EUROS, avec deux decimales.
    ⑧ POURQUOI — Le passage par l ecriture anglaise puis le double remplacement
      evite d avoir a regler la langue du systeme, qui n est pas la meme sur la
      machine de l hebergeur et sur celle de Jean-Luc. Le signe plus n est pose
      que sur demande parce qu il a un sens different selon la colonne : sur un
      resultat net il dit « gain », sur un prix d entree il ne voudrait rien dire.
    ⑨ CE QUI CLOCHE —
      ① Un montant deja ecrit a la francaise est rejete. Mesure le 20-09-2026 :
      `f_eur('27,28')` rend `n.d.`. Le meme fichier porte pourtant une fonction qui
      accepte les deux ecritures, `serie_mesure`, qui remplace la virgule par un
      point avant de convertir. Deux tolerances differentes cohabitent dans un
      seul programme, et le jour ou une source ecrira ses montants a la
      francaise, la moitie de la page affichera « n.d. » sans autre explication.
      ② Le remplacement s applique au texte entier et non au seul separateur. Un
      montant ne porte jamais d autre virgule ni d autre point, donc le defaut ne
      se voit pas aujourd hui ; il se verrait le jour ou l on ajouterait un
      suffixe au texte rendu.
    ⑩ EFFET — N ecrit aucun fichier, ne lit rien, ne touche pas au reseau, n
      affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne leve pas : la conversion est
      rattrapee et rendue sous forme du texte « n.d. ». Aucun de ses appels ne se
      termine.
      [sort: non]
    """
    try:
        v = float(x)
    except (TypeError, ValueError):
        return 'n.d.'
    s = '+' if (signe and v > 0) else ''
    return f"{s}{v:,.2f} €".replace(',', ' ').replace('.', ',')

def f_pct(x, dec=1):
    """Met un taux en pourcents a la francaise, ou rend « n.d. » si le taux est
    illisible.

    ① ROLE — Donner aux taux de la page une seule ecriture, avec une virgule
      decimale et le symbole pourcent. Elle sert a la seule grandeur de la page
      que le programme calcule en pourcents : la variation latente d une position
      ouverte.
    ② CONTEXTE D APPEL — Un seul appelant : `bloc1_aujourdhui`, une fois, pour
      afficher la variation latente de la position ouverte.
    ③ ENTREE — `x` : le taux a mettre en forme. `bloc1_aujourdhui` y passe le
      resultat de son propre calcul, un nombre a virgule. `dec` : le nombre de
      decimales, qui vaut 1 par defaut ; le seul appelant laisse cette valeur.
    ④ CONDITIONS D ENTREE — Aucune. Une valeur vide, absente ou non numerique est
      acceptee et donne « n.d. ».
    ⑤ SORTIE — UNE valeur : un texte. Le taux mis en forme, par exemple `33,3 %`,
      ou le texte `n.d.` quand la conversion en nombre echoue. Mesure le
      20-09-2026 : `f_pct(33.333)` rend `33,3 %`, `f_pct('n.d.')` rend `n.d.`.
      [rend: 1]
    ⑥ TRAITEMENT — ① convertir en nombre et l ecrire avec le nombre de decimales
      demande, suivi d une espace et du symbole pourcent · ② remplacer le point
      decimal par une virgule · ③ rendre « n.d. » si la conversion echoue.
    ⑦ UNITE — Des POURCENTS, avec une decimale par defaut.
    ⑧ POURQUOI — Aucun signe plus n est ajoute, contrairement aux montants : le
      seul usage est une variation latente, ou le signe moins suffit a dire que la
      position est en perte, et ou un signe plus alourdirait une ligne deja
      longue.
    ⑨ CE QUI CLOCHE — Un taux negatif mais plus petit qu un demi-dixieme s
      affiche « -0,0 % », ce qui se lit comme un zero negatif. Mesure le
      20-09-2026 : `f_pct(-0.04)` rend `-0,0 %`. Sur une position ouverte a peine
      en perte, la page affiche donc « variation latente -0,0 % », et un lecteur
      peut y voir une erreur d affichage plutot qu une perte tres faible.
    ⑩ EFFET — N ecrit aucun fichier, ne lit rien, ne touche pas au reseau, n
      affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne leve pas : la conversion est
      rattrapee et rendue sous forme du texte « n.d. ». Aucun de ses appels ne se
      termine.
      [sort: non]
    """
    try:
        return f"{float(x):.{dec}f} %".replace('.', ',')
    except (TypeError, ValueError):
        return 'n.d.'

def derniere_mesure(mesures, strategie=None, comptabilite='un jeton'):
    """Rend la mesure la plus recente pour une strategie et une comptabilite, sans
    rien recalculer.

    ① ROLE — Etre la porte d entree unique vers les indicateurs de performance.
      Toutes les valeurs chiffrees des sections QA, Production, Operations
      cloturees et Surveillance passent par elle, puis par `val` : elle choisit la
      ligne de l historique des mesures qui fait foi, et le reste du programme se
      contente de la lire. Elle ne calcule rien : deux implementations d une meme
      chose divergent toujours (R-708), et c est
      programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py qui a deja tout
      produit.
    ② CONTEXTE D APPEL — Trois appelants : `bloc_strategie`, deux fois, une par
      comptabilite · `bloc_journal`, une fois, sans preciser de strategie, pour la
      synthese sous le journal · `bloc_surveillance`, une fois par couple
      strategie et comptabilite trouve dans l historique.
    ③ ENTREE — `mesures` : la liste des lignes de donnees/historique_mesures.csv,
      chacune sous forme de dictionnaire ; les trois appelants passent l attribut
      `mesures` de l objet des sources. `strategie` : le nom de la strategie
      voulue, ou `None` pour ne pas filtrer ; `bloc_strategie` y passe le nom lu
      dans l etat civil, `bloc_journal` passe `None`. `comptabilite` : le nom de
      la comptabilite, qui vaut `un jeton` par defaut ; `bloc_strategie` passe
      `un jeton` puis `jetons il`.
    ④ CONDITIONS D ENTREE — Les lignes doivent porter les colonnes `strategie`,
      `comptabilite` et `date_mesure`. Une liste vide est acceptee. Les dates de
      mesure doivent etre ecrites annee-mois-jour pour se ranger correctement.
    ⑤ SORTIE — UNE valeur, de deux formes : la ligne retenue, sous forme de
      dictionnaire, ou la valeur `None` quand aucune ligne ne correspond. Mesure
      le 20-09-2026 sur les 84 lignes de l historique du depot : l appel sans
      strategie en comptabilite un jeton rend la ligne de C5E10-OBS-V1 datee du
      2026-09-17.
      [rend: 1]
    ⑥ TRAITEMENT — ① garder les lignes dont le nom de strategie correspond, en
      comparant les deux noms debarrasses de tout ce qui n est ni lettre ni
      chiffre · ② parmi elles, garder celles dont la comptabilite commence par les
      huit premiers caracteres de la comptabilite demandee · ③ rendre `None` si
      rien ne reste · ④ sinon ranger par date de mesure et rendre la derniere.
    ⑦ UNITE — Une LIGNE de l historique des mesures, c est-a-dire une strategie,
      une comptabilite et un jour.
    ⑧ POURQUOI — Les noms sont compares debarrasses de leur ponctuation parce que
      la meme strategie s ecrit differemment selon le fichier : l etat civil porte
      `C5-ETENDU-10`, d autres sources ecrivent `C5_ETENDU 10`. Mesure le
      20-09-2026 : les deux graphies donnent la meme forme comparable,
      `C5ETENDU10`. Sans ce rapprochement, la section afficherait « aucun
      indicateur disponible » alors que la mesure existe.
      Le rapprochement sur les huit premiers caracteres de la comptabilite sert,
      lui, a distinguer les deux seules comptabilites du systeme : le 20-09-2026,
      l historique n en porte que deux, `un jeton` et `jetons illimites`, et leurs
      huit premiers caracteres, `un jeton` et `jetons i`, suffisent a les separer.
    ⑨ CE QUI CLOCHE —
      ① La synthese affichee sous le journal decrit UNE strategie, choisie par l
      ordre du fichier. `bloc_journal` appelle cette fonction sans preciser de
      strategie, et le rangement ne porte que sur la date : a egalite de date, la
      derniere ligne du fichier l emporte. Mesure le 20-09-2026 sur l historique
      du depot, qui porte quatre lignes au 2026-09-17 — C5E10-QA-V1 puis
      C5E10-OBS-V1, chacune dans les deux comptabilites : l appel rend
      C5E10-OBS-V1, et le meme fichier lu a l envers rend C5E10-QA-V1. La page
      presente pourtant ce resultat comme la synthese du journal entier.
      ② Le rapprochement sur huit caracteres n est pas un rapprochement de nom.
      Une comptabilite qui s appellerait `un jetons partages` serait acceptee pour
      `un jeton`, puisque ses huit premiers caracteres sont identiques. Le critere
      qui tranche tient en une question : si je renomme une comptabilite, mon
      controle change-t-il d avis ? Ici oui. Releve le 20-09-2026 par lecture de la
      condition qui compare la comptabilite sur ses huit premiers caracteres.
      ③ Une comptabilite demandee de moins de huit caracteres accepte tout ce qui
      commence pareil. Mesure le 20-09-2026 : l appel avec `un` rend une ligne de
      comptabilite `un jeton`, alors que rien n a ete verifie au-dela des deux
      premieres lettres.
    ⑩ EFFET — LIT une liste deja chargee en memoire. N ouvre aucun fichier, n
      ecrit rien, ne touche pas au reseau, n affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne leve pas : les colonnes
      absentes sont remplacees par du vide. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DEFINITIONS
      l etat civil : donnees/cac40_strategies.csv, qui donne pour chaque
        strategie son objectif, son seuil de perte, son horizon et son etat de
        vie.
      l historique des mesures : donnees/historique_mesures.csv, une ligne par
        jour, par strategie et par comptabilite, jamais reecrit.
      une comptabilite : la facon de compter les resultats, et il y en a deux,
        jamais additionnees — un jeton, une seule position a la fois avec 100
        000 € simules, et jetons illimites, toutes les occurrences du signal
        mesurees.
    
      C5-ETENDU-10 : le nom de la stratégie vivante ; ses seuils et son horizon sont lus dans `donnees/cac40_strategies.csv`.
      PRODUCTION : l etat d une strategie dont le seuil d operations est atteint et les resultats conformes, donc exploitee.
      QA : l etat d une strategie validee sur l historique mais qui n a pas encore realise assez d operations reelles pour etre jugee.
      le rapprochement : le fait de reconnaître que deux écritures différentes désignent le même fichier ou la même entreprise
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    lst = [m for m in mesures
           if (not strategie or _corr(m.get('strategie', '')) == _corr(strategie))
           and (m.get('comptabilite', '') or '').startswith(comptabilite[:8])]
    if not lst:
        return None
    return sorted(lst, key=lambda m: m.get('date_mesure', ''))[-1]


def serie_mesure(mesures, champ, strategie=None, comptabilite='un jeton'):
    """Rend l evolution d un indicateur dans le temps, un point par jour de mesure.

    ① ROLE — Permettre a la page de montrer non seulement l etat du jour mais son
      chemin : l historique des mesures conservant une ligne par jour, un
      indicateur peut etre suivi dans le temps au lieu d etre reduit a sa derniere
      valeur. Decision de Jean-Luc du 15-08-2026, au moment ou le cockpit a cesse
      de calculer et s est branche sur cet historique.
    ② CONTEXTE D APPEL — Un seul appelant : `bloc_strategie`, une fois, pour le
      cumul net en comptabilite un jeton, afin de dessiner la courbe d evolution
      quand l historique porte au moins deux releves.
    ③ ENTREE — `mesures` : la liste des lignes de donnees/historique_mesures.csv ;
      l appelant passe l attribut `mesures` de l objet des sources. `champ` : le
      nom de la colonne a suivre ; l appelant passe `cumul_net_eur`. `strategie` :
      le nom de la strategie, ou `None` pour ne pas filtrer ; l appelant passe le
      nom lu dans l etat civil. `comptabilite` : le nom de la comptabilite, qui
      vaut `un jeton` par defaut ; l appelant laisse cette valeur.
    ④ CONDITIONS D ENTREE — Les lignes doivent porter les colonnes `strategie`,
      `comptabilite` et `date_mesure`. Une liste vide est acceptee. La colonne
      demandee peut manquer : les lignes ou elle manque sont simplement ecartees.
    ⑤ SORTIE — UNE valeur : une liste de couples, chacun fait de la date de mesure
      et de la valeur du champ convertie en nombre, rangee du plus ancien au plus
      recent. Liste vide quand rien ne correspond. Mesure le 20-09-2026 pour
      C5E10-OBS-V1 en comptabilite un jeton sur le champ `cumul_net_eur` : 14
      points, du 2026-08-26 a 6 884,75 € au 2026-09-17 a 1 292,25 €.
      [rend: 1]
    ⑥ TRAITEMENT — ① garder les lignes dont le nom de strategie correspond, en
      comparant les deux noms debarrasses de tout ce qui n est ni lettre ni
      chiffre · ② parmi elles, garder celles dont la comptabilite commence par les
      huit premiers caracteres de la comptabilite demandee · ③ les ranger par date
      de mesure · ④ pour chacune, lire le champ demande, remplacer une virgule
      decimale par un point, convertir en nombre, et passer la ligne si la
      conversion echoue · ⑤ rendre la liste des couples.
    ⑦ UNITE — Celle du champ demande. Pour le seul usage actuel, `cumul_net_eur`,
      ce sont des EUROS. La longueur de la liste se compte en JOURS DE MESURE.
    ⑧ POURQUOI — Une ligne dont la valeur est illisible est ecartee au lieu de
      faire tomber la page : l historique s empile depuis le 26-08-2026 et porte
      des lignes ecrites par des versions successives du service, dont certaines
      colonnes peuvent etre vides. Une courbe a laquelle il manque un point reste
      lisible ; une page qui ne s affiche pas ne dit plus rien.
    ⑨ CE QUI CLOCHE —
      ① Une ligne illisible disparait sans laisser de trace. Le compte de releves
      affiche a cote de la courbe, « Evolution du cumul (14 releves) » le
      20-09-2026, est celui des points retenus, jamais celui des jours mesures. Un
      lecteur ne peut pas savoir qu il manque des jours.
      ② Le rapprochement sur les huit premiers caracteres de la comptabilite n est
      pas un rapprochement de nom : une comptabilite qui commencerait par les
      memes huit caracteres serait acceptee. Le critere qui tranche tient en une
      question : si je renomme une comptabilite, mon controle change-t-il d avis ?
      Ici oui. Releve le 20-09-2026 par lecture de la
      condition qui compare la comptabilite sur ses huit premiers caracteres.
    ⑩ EFFET — LIT une liste deja chargee en memoire. N ouvre aucun fichier, n
      ecrit rien, ne touche pas au reseau, n affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne leve pas : les conversions
      ratees sont rattrapees et la ligne est ecartee. Aucun de ses appels ne se
      termine.
      [sort: non]
    ⑫ DEFINITIONS
      l etat civil : donnees/cac40_strategies.csv, qui donne pour chaque
        strategie son objectif, son seuil de perte, son horizon et son etat de
        vie.
      l historique des mesures : donnees/historique_mesures.csv, une ligne par
        jour, par strategie et par comptabilite, jamais reecrit.
      une comptabilite : la facon de compter les resultats, et il y en a deux,
        jamais additionnees — un jeton, une seule position a la fois avec 100
        000 € simules, et jetons illimites, toutes les occurrences du signal
        mesurees.
    
      le cockpit : la page web que ce programme fabrique et que Jean-Luc ouvre pour voir l etat du systeme.
      le rapprochement : le fait de reconnaître que deux écritures différentes désignent le même fichier ou la même entreprise
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    lst = [m for m in mesures
           if (not strategie or _corr(m.get('strategie', '')) == _corr(strategie))
           and (m.get('comptabilite', '') or '').startswith(comptabilite[:8])]
    out = []
    for m in sorted(lst, key=lambda m: m.get('date_mesure', '')):
        v = m.get(champ, '')
        try:
            out.append((m.get('date_mesure', ''), float(str(v).replace(',', '.'))))
        except (TypeError, ValueError):
            continue
    return out


def _corr(s):
    """Reduit un nom a ses seules lettres et chiffres, en majuscules, pour pouvoir
    comparer deux graphies.

    ① ROLE — Permettre de reconnaitre qu une meme strategie est la meme, quelle
      que soit la ponctuation de son nom. C est le defaut d appariement le plus
      courant de ce projet : une meme chose est ecrite differemment selon le
      fichier, et sans rapprochement le programme croit avoir affaire a deux
      choses distinctes et en ignore une.
    ② CONTEXTE D APPEL — Deux appelants, tous deux dans ce fichier :
      `derniere_mesure` et `serie_mesure`. Chacun l appelle a deux endroits d une
      meme comparaison, donc deux fois par ligne de l historique des mesures
      examinee : une fois sur le nom ecrit dans la ligne, une fois sur le nom
      demande.
    ③ ENTREE — `s` : le nom a reduire. Les deux appelants y passent soit le nom lu
      dans une ligne de l historique des mesures, soit le nom lu dans l etat civil
      des strategies, par exemple `C5E10-OBS-V1`.
    ④ CONDITIONS D ENTREE — Aucune. Une valeur absente ou d une autre nature qu un
      texte est acceptee : elle est d abord convertie en texte.
    ⑤ SORTIE — UNE valeur : un texte, en majuscules, ne portant que des lettres et
      des chiffres. Mesure le 20-09-2026 : `C5-ETENDU-10` et `C5_ETENDU 10`
      rendent tous deux `C5ETENDU10`.
      [rend: 1]
    ⑥ TRAITEMENT — ① convertir la valeur recue en texte · ② la passer en
      majuscules · ③ ne garder que les caracteres qui sont des lettres ou des
      chiffres.
    ⑦ UNITE — —
    ⑧ POURQUOI — Le projet connait ce defaut sous deux cas nommes, cites dans le
      code : le cas Unibail et le cas C5E10. Une meme entreprise est ecrite
      `UNIBAIL-RODAMCO-WESTFIELD` dans un fichier et `UNIBAIL_RODAMCO` dans un
      autre ; sans rapprochement, le programme croit a deux societes distinctes et
      en ignore une. Reduire aux seules lettres et chiffres traite d un seul geste
      les tirets, les tirets bas, les espaces et la casse.
    ⑨ CE QUI CLOCHE — Ce rapprochement n est utilise que pour les noms de
      STRATEGIES. Les noms de VALEURS, eux, sont rapproches autrement, dans
      `Sources.serie`, qui se contente de remplacer les tirets bas par des
      espaces. Mesure le 20-09-2026 : le journal porte `UNIBAIL_RODAMCO`, les
      fichiers de cours portent `UNIBAIL-RODAMCO-WESTFIELD`, et le graphique de ce
      titre n est pas dessine. Deux facons de rapprocher deux noms cohabitent dans
      un seul programme, et la plus faible sert la ou le defaut est le plus
      documente.
    ⑩ EFFET — N ecrit aucun fichier, ne lit rien, ne touche pas au reseau, n
      affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne leve pas. Aucun de ses appels
      ne se termine.
      [sort: non]
    ⑫ DEFINITIONS
      l etat civil : donnees/cac40_strategies.csv, qui donne pour chaque
        strategie son objectif, son seuil de perte, son horizon et son etat de
        vie.
      l historique des mesures : donnees/historique_mesures.csv, une ligne par
        jour, par strategie et par comptabilite, jamais reecrit.
    
      C5-ETENDU-10 : le nom de la stratégie vivante ; ses seuils et son horizon sont lus dans `donnees/cac40_strategies.csv`.
      le projet : le dossier reçu sur la ligne de commande, celui que le radar examine
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    return ''.join(c for c in str(s).upper() if c.isalnum())


def val(mesure, champ, defaut='n.d.'):
    """Rend la valeur brute d une colonne de mesure, telle que le service l a ecrite,
    ou un texte de repli.

    ① ROLE — Etre le seul chemin par lequel un chiffre de l historique des mesures
      arrive dans la page, et garantir qu il y arrive INCHANGE. Elle ne convertit
      rien, n arrondit rien, ne met rien en forme : ce que le service a ecrit est
      ce que Jean-Luc lit. C est la traduction en code de la regle qui veut qu un
      chiffre qui existe ailleurs ne se recopie pas (R-708).
    ② CONTEXTE D APPEL — Quatre appelants, avec le nombre d endroits ou chacun l
      appelle, releve le 20-09-2026 dans l arbre syntaxique du fichier :
      `bloc_strategie`, neuf endroits · `bloc_journal`, sept · `bloc_surveillance`,
      trois · et `voyant`, un seul, pour lire la couleur avant de la traduire en
      pastille.
    ③ ENTREE — `mesure` : une ligne de l historique des mesures sous forme de
      dictionnaire, ou `None` quand aucune mesure n a ete trouvee — c est ce que
      rend `derniere_mesure` dans ce cas. `champ` : le nom de la colonne a lire,
      par exemple `taux_reussite` ou `cumul_net_eur`. `defaut` : le texte a rendre
      quand il n y a rien a lire, qui vaut `n.d.` par defaut ; `bloc_strategie` y
      passe `?` pour le seuil, `0` pour le compteur, et `voyant` y passe le texte
      vide.
    ④ CONDITIONS D ENTREE — Aucune. Une mesure absente, une colonne absente ou une
      colonne vide sont toutes acceptees et donnent le texte de repli.
    ⑤ SORTIE — UNE valeur : un texte. La valeur de la colonne, debarrassee de ses
      espaces de bord, ou le texte de repli. Mesure le 20-09-2026 : sur une mesure
      absente elle rend `n.d.`, et sur une colonne ne contenant que des espaces
      elle rend `n.d.` aussi.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre le repli si aucune mesure n est donnee · ② lire la
      colonne, prendre le texte vide si elle manque, et retirer les espaces de
      bord · ③ rendre cette valeur si elle n est pas vide, sinon le repli.
    ⑦ UNITE — Celle de la colonne lue, et elle n est pas la meme d une colonne a l
      autre : `taux_reussite` est en POURCENTS, `cumul_net_eur` en EUROS,
      `n_operations` et `pertes_consecutives` en OPERATIONS, `serie_en_cours` en
      OPERATIONS consecutives avec un signe qui dit gains ou pertes. La fonction,
      elle, ne connait aucune de ces unites : c est l appelant qui ajoute le
      symbole a cote.
    ⑧ POURQUOI — La valeur est rendue telle quelle, sans mise en forme, pour qu un
      chiffre affiche sur la page puisse etre retrouve caractere pour caractere
      dans donnees/historique_mesures.csv. Mesure le 20-09-2026 : la page affiche
      `33.3 %`, `1292.25 €` et `-5592.50 €` avec des points decimaux anglais,
      exactement comme la ligne du 2026-09-17 les ecrit. C est volontairement plus
      laid que les montants du journal, mis en forme par `f_eur`, et c est le prix
      a payer pour qu une valeur affichee soit opposable a sa source.
    ⑨ CE QUI CLOCHE — Une colonne absente et une colonne vide rendent le meme
      texte, et rien ne les distingue. Si le service cessait d ecrire la colonne
      `point_mort`, la page afficherait « point mort de cette strategie : n.d. »
      exactement comme elle le ferait pour une mesure ou ce point mort n est pas
      encore calculable. Le premier cas est une regression a corriger, le second
      un etat normal, et la page les affiche pareil.
    ⑩ EFFET — LIT un dictionnaire deja en memoire. N ouvre aucun fichier, n ecrit
      rien, ne touche pas au reseau, n affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne leve pas. Aucun de ses appels
      ne se termine.
      [sort: non]
    ⑫ DEFINITIONS
      l historique des mesures : donnees/historique_mesures.csv, une ligne par
        jour, par strategie et par comptabilite, jamais reecrit.
      le point mort : le taux de réussite en dessous duquel une stratégie perd de l'argent
      le service MESURER LA PERFORMANCE : programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py,
        le seul programme autorise a calculer les indicateurs de performance.
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if not mesure:
        return defaut
    v = (mesure.get(champ) or '').strip()
    return v if v else defaut


def voyant(mesure, champ):
    """Traduit la couleur ecrite par le service en une pastille coloree lisible dans
    la page.

    ① ROLE — Rendre visible d un coup d oeil, sur un telephone, l etat d un
      garde-fou. Le service ecrit une couleur en toutes lettres dans l historique
      des mesures ; cette fonction la transforme en un mot colore — OK en vert,
      ALERTE en rouge, en attente en dore. C est de la mise en forme, et rien d
      autre : la decision d allumer le voyant a ete prise ailleurs.
    ② CONTEXTE D APPEL — Deux appelants : `bloc_strategie`, une fois, pour le
      voyant du garde-fou sur le taux de reussite · `bloc_surveillance`, trois
      fois par ligne du tableau, pour les voyants du taux de reussite, des pertes
      consecutives et de la pire chute.
    ③ ENTREE — `mesure` : une ligne de l historique des mesures sous forme de
      dictionnaire, ou `None`. `champ` : le nom de la colonne qui porte la
      couleur ; les appelants passent `voyant_c7`, `voyant_pertes` et
      `voyant_chute`.
    ④ CONDITIONS D ENTREE — Aucune. Une mesure absente ou une couleur inconnue
      sont acceptees.
    ⑤ SORTIE — UNE valeur : un fragment de page. Un mot colore pour chacune des
      trois couleurs connues, ou un simple tiret cadratin quand la couleur est
      vide, absente ou inconnue. Mesure le 20-09-2026 : `vert` rend un « OK »
      vert, `rouge` un « ALERTE » rouge, `attente` un « en attente » dore, et
      `orange` rend le tiret.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire la couleur dans la mesure, avec le texte vide comme
      repli · ② chercher cette couleur parmi les trois connues et rendre le
      fragment correspondant · ③ rendre un tiret cadratin si elle n y est pas.
    ⑦ UNITE — —
    ⑧ POURQUOI — Les trois couleurs ne sont pas traduites par leur nom mais par ce
      qu elles veulent dire — OK, ALERTE, en attente — parce que la page doit
      rester lisible pour quelqu un qui ne distingue pas bien le vert du rouge, et
      parce que « en attente » dit, la ou « dore » ne dirait rien, que le
      garde-fou ne s est pas encore prononce faute d operations. Mesure le
      20-09-2026 : les six lignes du tableau de surveillance affichent toutes
      « en attente » sur le taux de reussite, parce que l echantillon est
      insuffisant.
    ⑨ CE QUI CLOCHE — Une couleur inconnue rend le meme tiret qu une couleur
      absente. Si le service ajoutait un quatrieme etat, la page afficherait un
      tiret sans rien signaler, et personne ne saurait qu un voyant existe et n est
      pas lu. Un affichage qui se tait sur ce qu il ne comprend pas est
      indiscernable d un affichage qui n a rien a montrer.
    ⑩ EFFET — LIT un dictionnaire deja en memoire. N ouvre aucun fichier, n ecrit
      rien, ne touche pas au reseau, n affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne leve pas. Aucun de ses appels
      ne se termine.
      [sort: non]
    ⑫ DEFINITIONS
      l historique des mesures : donnees/historique_mesures.csv, une ligne par
        jour, par strategie et par comptabilite, jamais reecrit.
      la pire chute : la plus forte baisse du cumul depuis un sommet
        precedent.
      le service MESURER LA PERFORMANCE : programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py,
        le seul programme autorise a calculer les indicateurs de performance.
      un garde-fou : une limite qui, franchie, fait cesser a la strategie de
        prendre position tout en continuant a la mesurer.
    
      le voyant : une case du tableau de bord qui vaut « vert » ou « rouge »
      un voyant : une case du tableau de bord qui vaut « vert » ou « rouge »
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    v = val(mesure, champ, '')
    return {'vert': f'<span style="color:{C["grn"]}">OK</span>',
            'rouge': f'<span style="color:{C["red"]}">ALERTE</span>',
            'attente': f'<span style="color:{C["gld"]}">en attente</span>'}.get(v, '—')


def stats_journal(trades, strategie=None):
    """Calcule sur le journal des operations un jeu d indicateurs — et n est appelee
    par personne.

    ① ROLE — Aucun aujourd hui. Cette fonction calcule le nombre d operations,
      combien sont gagnantes, le taux de reussite, le cumul net, le cumul selon la
      convention du backtest, la serie de gains ou de pertes en cours et la pire
      chute depuis un sommet. Ce sont exactement les indicateurs que le changement
      du 15-08-2026 a retires de ce programme pour les confier au service MESURER
      LA PERFORMANCE : depuis, la page les LIT dans donnees/historique_mesures.csv
      et ne les calcule plus.
    ② CONTEXTE D APPEL — PERSONNE. Releve le 20-09-2026 en rapprochant, dans l
      arbre syntaxique du fichier, les definitions et les appels : aucune des 30
      fonctions du programme ne la nomme, et le lancement du programme non plus.
      Elle est du code mort qui fonctionne toujours.
    ③ ENTREE — `trades` : la liste des operations cloturees, chacune sous forme de
      dictionnaire, telle que `Sources._lire_csv` la produit a partir de
      journal_trades.csv. `strategie` : un debut de nom de strategie pour ne
      garder que ses operations, ou `None` pour les garder toutes. Aucun appelant,
      donc aucune valeur reellement passee.
    ④ CONDITIONS D ENTREE — Les lignes doivent porter les colonnes
      `pnl_net_eur` et `pnl_net_convention_eur`. Une liste vide est acceptee.
    ⑤ SORTIE — UNE valeur, mais de DEUX FORMES DIFFERENTES selon la branche. Sur
      une liste vide, un dictionnaire de SEPT cles : `n`, `wr`, `cumul`, `serie`,
      `creux`, `gagnantes`, `cumul_conv`. Sinon, un dictionnaire de HUIT cles :
      les memes plus `pnls`, la liste des resultats nets. Mesure le 20-09-2026 :
      l appel sur une liste vide rend sept cles, l appel sur une seule operation
      en rend huit.
      [rend: 1]
    ⑥ TRAITEMENT — ① ne garder que les operations de la strategie demandee ·
      ② rendre un resultat a zero si la liste est vide · ③ convertir les deux
      colonnes de resultat en nombres, en comptant zero quand la conversion
      echoue · ④ compter les operations gagnantes · ⑤ remonter le journal depuis
      la fin pour compter la serie de gains ou de pertes en cours, positive pour
      des gains, negative pour des pertes · ⑥ parcourir les resultats dans l
      ordre en suivant le cumul et le plus haut atteint, pour relever la plus
      forte chute depuis ce plus haut · ⑦ rendre le dictionnaire.
    ⑦ UNITE — `n` et `gagnantes` se comptent en OPERATIONS. `wr` est en POURCENTS.
      `cumul`, `cumul_conv` et `creux` sont en EUROS, `creux` etant negatif ou
      nul. `serie` se compte en OPERATIONS consecutives, avec un signe qui dit
      gains ou pertes.
    ⑧ POURQUOI — Le filtre sur la strategie compare par un DEBUT de nom et non par
      une egalite, parce que le journal ecrit parfois le nom de la strategie suivi
      d une precision. La pire chute est mesuree depuis le plus haut atteint et
      non depuis le depart, parce que c est la perte qu aurait reellement subie
      quelqu un entre au plus mauvais moment.
    ⑨ CE QUI CLOCHE —
      ① Elle n est appelee par personne, et elle calcule precisement ce que le
      programme a decide de ne plus calculer. Un lecteur qui la trouve peut croire
      que la page s en sert, et corriger un chiffre ici en pensant corriger l
      affichage. Le chiffre affiche, lui, vient de
      donnees/historique_mesures.csv.
      ② Elle rend deux formes de dictionnaire selon la branche. Mesure le
      20-09-2026 : sept cles sur une liste vide, huit sinon. Un appelant qui lirait
      la cle `pnls` sans precaution tomberait sur le seul cas ou il n y a rien a
      afficher.
      ③ Un resultat illisible est compte comme zero, sans rien signaler. Une
      operation dont le resultat n a pas ete ecrit serait donc comptee comme une
      operation ni gagnante ni perdante, et ferait baisser le taux de reussite
      sans qu aucun message ne le dise.
    ⑩ EFFET — LIT une liste deja en memoire. N ouvre aucun fichier, n ecrit rien,
      ne touche pas au reseau, n affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne leve pas : les conversions
      ratees sont rattrapees. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DEFINITIONS
      la convention du backtest : la facon pessimiste de compter un resultat,
        qui retient le prix de l objectif meme quand le cours a saute
        par-dessus, pour rester comparable aux chiffres de reference.
      la pire chute : la plus forte baisse du cumul depuis un sommet
        precedent.
      le code mort : du code qui n est appele par rien et qui reste dans le
        fichier.
      le service MESURER LA PERFORMANCE : programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py,
        le seul programme autorise a calculer les indicateurs de performance.
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    lst = [t for t in trades if (not strategie or t.get('strategie', '').startswith(strategie))]
    n = len(lst)
    if n == 0:
        return dict(n=0, wr=None, cumul=0.0, serie=0, creux=0.0, gagnantes=0, cumul_conv=0.0)
    pnls, pnls_conv = [], []
    for t in lst:
        try:
            pnls.append(float(t.get('pnl_net_eur') or 0))
        except ValueError:
            pnls.append(0.0)
        try:
            pnls_conv.append(float(t.get('pnl_net_convention_eur') or 0))
        except ValueError:
            pnls_conv.append(0.0)
    gagnantes = sum(1 for p in pnls if p > 0)
    # serie en cours (gains ou pertes consecutifs, en partant de la fin)
    serie = 0
    for p in reversed(pnls):
        if serie == 0:
            serie = 1 if p > 0 else -1
        elif (p > 0 and serie > 0):
            serie += 1
        elif (p <= 0 and serie < 0):
            serie -= 1
        else:
            break
    # creux maximal de la courbe cumulee
    cum, sommet, creux = 0.0, 0.0, 0.0
    for p in pnls:
        cum += p
        sommet = max(sommet, cum)
        creux = min(creux, cum - sommet)
    return dict(n=n, wr=100.0 * gagnantes / n, cumul=sum(pnls), serie=serie,
                creux=creux, gagnantes=gagnantes, cumul_conv=sum(pnls_conv), pnls=pnls)

def pertes_consecutives(trades):
    """Compte les pertes qui se suivent en fin de journal — et n est appelee par
    personne.

    ① ROLE — Aucun aujourd hui. Ce compte est un des garde-fous du systeme : au
      dela de cinq pertes consecutives, la strategie cesse de prendre position
      tout en restant mesuree. Mais depuis le changement du 15-08-2026, c est le
      service MESURER LA PERFORMANCE qui le calcule et l ecrit dans la colonne
      `pertes_consecutives` de donnees/historique_mesures.csv ; la page se
      contente de le lire.
    ② CONTEXTE D APPEL — PERSONNE. Releve le 20-09-2026 en rapprochant, dans l
      arbre syntaxique du fichier, les definitions et les appels : aucune des 30
      fonctions du programme ne la nomme. Elle est du code mort qui fonctionne
      toujours.
    ③ ENTREE — `trades` : la liste des operations cloturees, chacune sous forme de
      dictionnaire. Aucun appelant, donc aucune valeur reellement passee.
    ④ CONDITIONS D ENTREE — Les lignes doivent porter la colonne `pnl_net_eur`, et
      la liste doit etre rangee du plus ancien au plus recent : la fonction la
      remonte depuis la fin. Une liste vide est acceptee.
    ⑤ SORTIE — UNE valeur : un entier, le nombre de pertes qui se suivent en
      partant de la derniere operation. Zero quand la derniere operation est
      gagnante ou quand la liste est vide. Mesure le 20-09-2026 sur deux
      operations negatives : elle rend 2.
      [rend: 1]
    ⑥ TRAITEMENT — ① partir de la fin du journal · ② convertir le resultat net en
      nombre, en comptant zero quand la conversion echoue · ③ ajouter un au compte
      tant que le resultat est negatif ou nul · ④ s arreter des qu un resultat est
      positif · ⑤ rendre le compte.
    ⑦ UNITE — Un NOMBRE D OPERATIONS consecutives.
    ⑧ POURQUOI — Une operation a resultat exactement nul est comptee comme une
      perte, parce que le garde-fou sert a detecter une strategie qui ne gagne
      plus : une operation qui rentre dans ses frais ne casse pas une serie de
      pertes, elle la prolonge.
    ⑨ CE QUI CLOCHE —
      ① Elle n est appelee par personne, et elle double un calcul que le service
      fait deja. Deux implementations d une meme chose divergent toujours
      (R-708) : si l une des deux changeait de definition — par exemple en cessant
      de compter une operation nulle comme une perte — rien ne le signalerait.
      ② Un resultat illisible est compte comme zero, donc comme une perte, et
      prolonge silencieusement la serie. Une ligne de journal a moitie ecrite
      ferait donc croire a une perte de plus.
      ③ Elle ne filtre sur aucune strategie, alors que le garde-fou se juge par
      strategie. Sur un journal qui porte plusieurs strategies, elle melangerait
      leurs pertes.
    ⑩ EFFET — LIT une liste deja en memoire. N ouvre aucun fichier, n ecrit rien,
      ne touche pas au reseau, n affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne leve pas : la conversion ratee
      est rattrapee. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DEFINITIONS
      le code mort : du code qui n est appele par rien et qui reste dans le
        fichier.
      le service MESURER LA PERFORMANCE : programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py,
        le seul programme autorise a calculer les indicateurs de performance.
      un garde-fou : une limite qui, franchie, fait cesser a la strategie de
        prendre position tout en continuant a la mesurer.
    
      le garde-fou : le programme `CONTROLER_MA_LIVRAISON.py`, qui accepte ou refuse un travail avant qu il parte à la relecture
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    n = 0
    for t in reversed(trades):
        try:
            p = float(t.get('pnl_net_eur') or 0)
        except ValueError:
            p = 0.0
        if p <= 0:
            n += 1
        else:
            break
    return n

def ic95_borne_basse(gagnantes, n):
    """Calcule la borne basse de l intervalle de confiance du taux de reussite — et
    n est appelee par personne.

    ① ROLE — Aucun aujourd hui. Cette borne repond a une question precise : compte
      tenu du petit nombre d operations realisees, quel est le taux de reussite le
      plus defavorable encore compatible avec ce qu on a observe ? Le garde-fou
      compare ensuite cette borne au point mort de la strategie. Depuis le
      changement du 15-08-2026, c est le service MESURER LA PERFORMANCE qui la
      calcule et l ecrit dans la colonne `borne_basse_wilson` de
      donnees/historique_mesures.csv ; la page se contente de lire son verdict.
    ② CONTEXTE D APPEL — PERSONNE. Releve le 20-09-2026 en rapprochant, dans l
      arbre syntaxique du fichier, les definitions et les appels : aucune des 30
      fonctions du programme ne la nomme. Elle est du code mort qui fonctionne
      toujours.
    ③ ENTREE — `gagnantes` : le nombre d operations gagnantes. `n` : le nombre
      total d operations. Aucun appelant, donc aucune valeur reellement passee.
    ④ CONDITIONS D ENTREE — `n` doit etre un nombre, et `gagnantes` ne doit pas le
      depasser. Un `n` inferieur a dix est accepte et fait rendre `None`.
    ⑤ SORTIE — UNE valeur, de DEUX FORMES : un nombre a virgule, la borne basse en
      pourcents, jamais negative · ou la valeur `None` quand l echantillon compte
      moins de dix operations. Mesure le 20-09-2026 : six gagnantes sur douze
      rendent 21,71 ; une gagnante sur trois rend `None` ; zero gagnante sur dix
      rendent 0,0.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre `None` si le nombre d operations est inferieur a
      dix · ② calculer la proportion de gagnantes · ③ calculer la demi-largeur de
      l intervalle en multipliant 1,96 par la racine de la variance divisee par le
      nombre d operations · ④ rendre la proportion diminuee de cette demi-largeur,
      en pourcents, ramenee a zero si elle est negative.
    ⑦ UNITE — Le resultat est en POURCENTS. `n` et `gagnantes` se comptent en
      OPERATIONS. Le seuil de dix est un NOMBRE D OPERATIONS. Le 1,96 est le
      nombre d ecarts-types qui laisse 5 % de chances de part et d autre.
    ⑧ POURQUOI — Le refus en dessous de dix operations est le point important : la
      formule employee, dite de Wald, donne des resultats faux sur un petit
      echantillon, et rend meme un intervalle de largeur nulle quand toutes les
      operations sont gagnantes ou toutes perdantes. Mesure le 20-09-2026 : zero
      gagnante sur dix rend 0,0 — un intervalle qui ne dit plus rien. Plutot qu un
      chiffre trompeur, la fonction rend `None`, et l affichage dit alors
      « echantillon insuffisant ».
    ⑨ CE QUI CLOCHE —
      ① Elle n est appelee par personne, et elle n emploie pas la meme formule que
      le service. La colonne du service s appelle `borne_basse_wilson`, du nom d
      une autre formule, plus prudente sur les petits echantillons ; cette
      fonction, elle, emploie la formule de Wald. Deux implementations d une meme
      chose divergent toujours (R-708), et ici elles divergent deja par
      construction.
      ② Le seuil de dix est un nombre ecrit dans le code, et il n est lu nulle
      part ailleurs. Un garde-fou porte sur une propriete, jamais sur un compte :
      si le systeme changeait d avis sur le nombre d operations necessaire, ce
      chiffre resterait dix sans que rien ne le signale.
      ③ Ce garde-fou est designe partout par le code « C7 », sans que ce code dise
      ce qu il recouvre : les colonnes `verdict_c7` et `voyant_c7` de
      donnees/historique_mesures.csv le portent, et la page l affiche sous le
      titre « Garde-fou taux de reussite ». Le lecteur qui veut savoir a quoi la
      borne est comparee doit ouvrir l historique, ou le point mort est ecrit en
      clair : 43,1 % pour la strategie C5E10-OBS-V1 le 2026-09-17.
    ⑩ EFFET — N ecrit aucun fichier, ne lit rien, ne touche pas au reseau, n
      affiche rien.
    ⑪ TERMINAISON — Rend toujours la main quand les conditions d entree sont
      tenues. PEUT LEVER une division par zero si on lui passe un nombre d
      operations egal a zero — mais la branche qui rend `None` en dessous de dix
      l en protege. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DEFINITIONS
      le code mort : du code qui n est appele par rien et qui reste dans le
        fichier.
      le point mort : le taux de réussite en dessous duquel une stratégie perd de l'argent
      le service MESURER LA PERFORMANCE : programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py,
        le seul programme autorise a calculer les indicateurs de performance.
      un garde-fou : une limite qui, franchie, fait cesser a la strategie de
        prendre position tout en continuant a la mesurer.
    
      la borne basse : la valeur en dessous de laquelle ne tombe qu'un tirage sur vingt
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      le garde-fou : le programme `CONTROLER_MA_LIVRAISON.py`, qui accepte ou refuse un travail avant qu il parte à la relecture
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if n < 10:
        return None
    p = gagnantes / n
    demi = 1.96 * (p * (1 - p) / n) ** 0.5
    return max(0.0, 100.0 * (p - demi))

def carte_strategie(strategies, etat):
    """Rend la derniere ligne de vie d une strategie pour un etat donne.

    ① ROLE — Dire quelle strategie une section de la page doit decrire. Les
      sections QA et Production ne connaissent pas d avance le nom de la strategie
      qu elles affichent : elles le demandent a cette fonction, qui le cherche
      dans l etat civil. Ce qu elle rend fournit ensuite le nom, l objectif, le
      seuil de perte et l horizon affiches en tete de section.
    ② CONTEXTE D APPEL — Un seul appelant : `bloc_strategie`, une fois par appel,
      et `construire` appelle `bloc_strategie` deux fois — une fois avec l etat
      `QA`, une fois avec l etat `PRODUCTION`.
    ③ ENTREE — `strategies` : la liste des lignes de donnees/cac40_strategies.csv,
      chacune sous forme de dictionnaire ; l appelant passe l attribut
      `strategies` de l objet des sources. `etat` : le debut de l etat de vie
      cherche ; les deux seules valeurs passees sont `QA` et `PRODUCTION`.
    ④ CONDITIONS D ENTREE — Les lignes doivent porter une colonne `etat_vie` ou,
      a defaut, une colonne `statut`. La liste doit etre rangee dans l ordre ou
      elle a ete ecrite : la fonction prend la DERNIERE ligne qui correspond. Une
      liste vide est acceptee.
    ⑤ SORTIE — UNE valeur, de DEUX FORMES : la derniere ligne qui correspond, sous
      forme de dictionnaire · ou la valeur `None` quand aucune ne correspond.
      Mesure le 20-09-2026 sur les 68 lignes de donnees/cac40_strategies.csv :
      l etat `QA` rend la ligne `C5E10-OBS-V1`, avec objectif `+4.0%`, seuil de
      perte `-2.5%` et horizon `20` ; l etat `PRODUCTION` rend `None`, et la
      section Production de la page affiche alors « Aucune strategie en service ».
      [rend: 1]
    ⑥ TRAITEMENT — ① pour chaque ligne, lire l etat de vie, ou le statut si l etat
      de vie manque, et prendre le texte vide si les deux manquent · ② retirer les
      espaces de bord et passer en majuscules · ③ garder les lignes dont l etat
      commence par le texte demande · ④ rendre la derniere, ou `None` si aucune.
    ⑦ UNITE — Une LIGNE DE VIE, c est-a-dire l etat civil d une strategie a une
      date.
    ⑧ POURQUOI — La derniere ligne est retenue parce que ce fichier ne se corrige
      jamais : on y ajoute une ligne a chaque changement d etat, et l ancienne
      reste pour garder la trace. Mesure le 20-09-2026 : deux lignes portent l
      etat QA, `C5E10-QA-V1` puis `C5E10-OBS-V1`, et c est la seconde qui fait
      foi. Deux colonnes sont acceptees, `etat_vie` puis `statut`, parce que le
      fichier a change de colonne en cours de route et porte encore des lignes
      anciennes.
    ⑨ CE QUI CLOCHE —
      ① Le rapprochement se fait sur un DEBUT de texte, ce qui epelle au lieu de
      porter sur une propriete. Un etat de vie `QA-SUSPENDUE` serait retenu comme
      une strategie en QA, et sa carte s afficherait en tete de la section QA sans
      aucun avertissement. Le critere qui tranche tient en une question : si je
      renomme un etat, mon controle change-t-il d avis ? Ici oui. Releve le 20-09-2026 par lecture de la
      condition qui compare l etat de vie par son debut.
      ② La derniere ligne de la LISTE est retenue, pas la ligne la plus recente
      par sa date. Le fichier porte pourtant une colonne `date_entree_etat`, qui n
      est jamais regardee. Tant que le fichier est ecrit en ajoutant a la fin, les
      deux coincident ; le jour ou une ligne serait inseree ailleurs, la page
      decrirait la mauvaise strategie sans rien dire.
      ③ Elle ne verifie pas qu une seule strategie porte l etat cherche. Mesure le
      20-09-2026 : deux lignes portent l etat QA, et la page n affiche que la
      derniere, sans mentionner l existence de l autre.
    ⑩ EFFET — LIT une liste deja en memoire. N ouvre aucun fichier, n ecrit rien,
      ne touche pas au reseau, n affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne leve pas. Aucun de ses appels
      ne se termine.
      [sort: non]
    ⑫ DEFINITIONS
      PRODUCTION : l etat d une strategie dont le seuil d operations est
        atteint et les resultats conformes, donc exploitee.
      QA : l etat d une strategie validee sur l historique mais qui n a pas
        encore realise assez d operations reelles pour etre jugee.
      l etat civil : donnees/cac40_strategies.csv, qui donne pour chaque
        strategie son objectif, son seuil de perte, son horizon et son etat de
        vie.
      l horizon : le nombre de seances au bout duquel une position se ferme si
        ni l objectif ni le seuil de perte n ont ete touches.
      une ligne de vie : une ligne de donnees/cac40_strategies.csv, qui donne
        l etat civil d une strategie a une date.
    
      la trace : la liste des sources avec leur etat — LU, ABSENT ou ILLISIBLE — et un detail chiffre, affichee en pied de page.
      le rapprochement : le fait de reconnaître que deux écritures différentes désignent le même fichier ou la même entreprise
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    lignes = [s for s in strategies if (s.get('etat_vie') or s.get('statut') or '').strip().upper().startswith(etat)]
    return lignes[-1] if lignes else None

# --------------------------------------------------------------------------
# RENDU — briques HTML/SVG, aucune dependance reseau
# --------------------------------------------------------------------------
def esc(s):
    """Neutralise les trois caracteres qui feraient lire un texte de donnee comme du
    code de page.

    ① ROLE — Empecher qu un nom de valeur, un motif de sortie ou une note venant d
      un fichier ne casse la page en y injectant des balises. Sans elle, une note
      d archive contenant `<b>` serait interpretee comme une mise en gras et tout
      ce qui suit changerait d apparence ; un texte contenant un chevron ouvrant
      seul pourrait faire disparaitre une partie de la page.
    ② CONTEXTE D APPEL — Sept appelants, avec le nombre d endroits ou chacun l
      appelle, releve le 20-09-2026 dans l arbre syntaxique du fichier :
      `bloc_strategie`, neuf endroits · `bloc_surveillance`, sept ·
      `bloc_journal`, quatre · `bloc1_aujourdhui`, trois · `bloc_laboratoire`,
      trois · `construire`, deux · `courbe_cours`, un.
    ③ ENTREE — `s` : le texte a neutraliser, tel qu il sort d un fichier, par
      exemple le nom d une valeur ou la note d une strategie archivee. Une valeur
      d une autre nature qu un texte est acceptee : elle est d abord convertie.
    ④ CONDITIONS D ENTREE — Aucune.
    ⑤ SORTIE — UNE valeur : un texte, ou les trois caracteres esperluette,
      chevron ouvrant et chevron fermant ont ete remplaces par leur ecriture
      protegee. Mesure le 20-09-2026 : `SOCIETE "X" & <b>` rend
      `SOCIETE "X" &amp; &lt;b&gt;`.
      [rend: 1]
    ⑥ TRAITEMENT — ① convertir la valeur recue en texte · ② remplacer l
      esperluette par son ecriture protegee · ③ remplacer le chevron ouvrant ·
      ④ remplacer le chevron fermant.
    ⑦ UNITE — —
    ⑧ POURQUOI — L esperluette est traitee EN PREMIER, et cet ordre est le point
      important : si les chevrons etaient traites d abord, l esperluette que leur
      ecriture protegee introduit serait a son tour remplacee, et `<b>`
      deviendrait `&amp;lt;b&amp;gt;`, qui s afficherait tel quel a l ecran au
      lieu de montrer le texte d origine.
    ⑨ CE QUI CLOCHE — Les guillemets ne sont pas neutralises, alors que le texte
      rendu est parfois pose a l interieur d un attribut entoure de guillemets.
      Mesure le 20-09-2026 : `courbe_cours` construit
      `aria-label="{esc(titre)}"`, et un titre contenant `ACME "X"` produit
      `aria-label="ACME "X""` — l attribut se ferme au premier guillemet du nom, et
      le reste est lu comme d autres attributs. Le titre vient du nom de la valeur
      en position, donc d un fichier de donnees. Aucune valeur du CAC 40 ne porte
      de guillemet aujourd hui, et c est la seule raison pour laquelle le defaut
      ne se voit pas.
    ⑩ EFFET — N ecrit aucun fichier, ne lit rien, ne touche pas au reseau, n
      affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne leve pas. Aucun de ses appels
      ne se termine.
      [sort: non]
    """
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))

def sec(titre, corps, sous=''):
    """Compose une des six sections de la page : un cadre, un titre, un sous-titre et
    un corps.

    ① ROLE — Donner aux six sections de la page la meme apparence, pour que
      Jean-Luc les reconnaisse au meme endroit d une fois sur l autre : meme fond,
      meme bordure, meme arrondi, meme espacement. Elle ne decide rien de ce qui
      est affiche : elle enveloppe ce que la section lui donne.
    ② CONTEXTE D APPEL — Un seul appelant : `construire`, six fois, une par
      section, dans cet ordre : Aujourd hui, QA, Production, Laboratoire,
      Operations cloturees, Surveillance et archives.
    ③ ENTREE — `titre` : le titre de la section, par exemple `Aujourd'hui`.
      `corps` : le contenu deja compose de la section, tel que la fonction de bloc
      l a rendu. `sous` : le sous-titre, qui vaut le texte vide par defaut ; l
      appelant le donne pour les six sections, par exemple `prend-on position ?`.
    ④ CONDITIONS D ENTREE — Le titre, le corps et le sous-titre doivent etre deja
      prets a etre affiches : cette fonction ne neutralise rien. Le corps est
      attendu comme un fragment de page, avec ses propres balises.
    ⑤ SORTIE — UNE valeur : un texte, le fragment de page complet de la section.
      [rend: 1]
    ⑥ TRAITEMENT — ① ouvrir un cadre avec le fond, la bordure, l arrondi, la marge
      interieure et la marge basse · ② y poser le titre · ③ y poser le sous-titre
      en petits caracteres attenues · ④ y poser le corps tel quel · ⑤ refermer le
      cadre.
    ⑦ UNITE — Les tailles sont en PIXELS : titre a 13, sous-titre a 10, marge
      interieure a 14, marge basse a 14.
    ⑧ POURQUOI — Toutes les couleurs et toutes les tailles sont ecrites ici, dans
      le fragment de page, et non dans une feuille de style separee, parce que la
      page ne doit rien charger depuis Internet : elle est publiee sur un depot
      public et ouverte depuis un telephone. Mesure le 20-09-2026 sur une page
      produite a partir des vraies donnees du depot, 25 496 octets : zero balise
      `link`, zero `@import`, zero `url(`.
    ⑨ CE QUI CLOCHE — Le titre et le sous-titre sont poses sans etre neutralises,
      alors que le corps, lui, est compose par des fonctions qui neutralisent ce
      qui vient des fichiers. Les six titres sont aujourd hui ecrits en dur dans
      `construire`, donc le defaut ne se voit pas ; il apparaitrait le jour ou un
      titre de section viendrait d un fichier.
    ⑩ EFFET — N ecrit aucun fichier, ne lit rien, ne touche pas au reseau, n
      affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne leve pas. Aucun de ses appels
      ne se termine.
      [sort: non]
    """
    return (f'<section style="background:{C["panel"]};border:1px solid {C["line"]};border-radius:10px;'
            f'padding:14px;margin:0 0 14px"><h2 style="margin:0 0 2px;font-size:13px;color:{C["txt"]}">{titre}</h2>'
            f'<div style="font-size:10px;color:{C["dim"]};margin-bottom:10px">{sous}</div>{corps}</section>')

def det(label, inner):
    """Compose un bloc que le lecteur deplie lui-meme, replie par defaut.

    ① ROLE — Mettre au bas de la page ce qui est utile mais encombrant, sans
      allonger la page : le vocabulaire du systeme et la liste des fichiers lus
      pour produire la page. Replies, ces deux blocs tiennent en deux lignes ;
      deplies, ils donnent tout le detail. La page est lue sur un telephone, ou
      chaque ligne compte.
    ② CONTEXTE D APPEL — Un seul appelant : `construire`, deux fois — une fois
      pour le bloc « Vocabulaire », une fois pour le bloc « Sources lues pour
      produire cette page ».
    ③ ENTREE — `label` : le texte toujours visible, sur lequel on appuie pour
      deplier. `inner` : le contenu cache, deja compose ; pour le second appel, c
      est le tableau de la trace suivi d une phrase.
    ④ CONDITIONS D ENTREE — Le contenu cache doit etre deja pret a etre affiche :
      cette fonction ne neutralise rien.
    ⑤ SORTIE — UNE valeur : un texte, le fragment de page du bloc depliable.
      [rend: 1]
    ⑥ TRAITEMENT — ① ouvrir un bloc depliable · ② y poser le texte toujours
      visible, en bleu et avec un curseur qui indique qu on peut appuyer · ③ y
      poser le contenu cache, en petits caracteres attenues · ④ refermer.
    ⑦ UNITE — Les tailles sont en PIXELS : 11 pour le texte visible comme pour le
      contenu.
    ⑧ POURQUOI — Le depliage repose sur une balise que le navigateur sait ouvrir
      et fermer tout seul, sans une ligne de programme. C est la seule interaction
      de toute la page, et elle est obtenue sans rien charger depuis Internet :
      mesure le 20-09-2026 sur une page produite a partir des vraies donnees du
      depot, zero balise `script`.
    ⑨ CE QUI CLOCHE — Le texte visible est pose sans etre neutralise. Les deux
      seuls textes passes sont ecrits en dur dans `construire`, donc le defaut ne
      se voit pas aujourd hui.
    ⑩ EFFET — N ecrit aucun fichier, ne lit rien, ne touche pas au reseau, n
      affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne leve pas. Aucun de ses appels
      ne se termine.
      [sort: non]
    ⑫ DEFINITIONS
      la trace : la liste des sources avec leur etat — LU, ABSENT ou ILLISIBLE
        — et un detail chiffre, affichee en pied de page.
    
      un bloc : une suite de lignes qui se suivent dans le texte et dont les dates décroissent sans trou plus grand que six jours.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    return (f'<details style="margin:6px 0"><summary style="cursor:pointer;color:{C["blu"]};font-size:11px">{label}</summary>'
            f'<div style="padding:8px 2px;color:{C["mut"]};font-size:11px;line-height:1.6">{inner}</div></details>')

def tab(entetes, lignes):
    """Compose un tableau, ou un message quand il n y a aucune ligne a montrer.

    ① ROLE — Donner a tous les tableaux de la page la meme apparence, et surtout
      garantir qu un tableau vide DIT qu il est vide au lieu de disparaitre. Un
      tableau sans lignes qui s afficherait comme une zone blanche serait
      indiscernable d un tableau qui n a pas ete produit du tout.
    ② CONTEXTE D APPEL — Cinq appelants, avec le nombre d endroits ou chacun l
      appelle, releve le 20-09-2026 dans l arbre syntaxique du fichier :
      `bloc_journal`, deux endroits — le journal lui-meme et sa synthese ·
      `bloc_surveillance`, deux — les voyants et les strategies archivees ·
      `bloc_strategie`, un — les deux comptabilites · `bloc_laboratoire`, un — la
      file d idees · `construire`, un — la trace des sources lues.
    ③ ENTREE — `entetes` : la liste des titres de colonnes, par exemple
      `['Date', 'Titre', 'Entree', 'Sortie', 'Motif', 'Resultat net']`. `lignes` :
      la liste des lignes, chacune etant elle-meme une liste de cases deja pretes
      a etre affichees.
    ④ CONDITIONS D ENTREE — Les cases doivent DEJA etre neutralisees ou mises en
      forme par l appelant : cette fonction les pose telles quelles. Le nombre de
      cases par ligne n est pas verifie et devrait valoir celui des entetes.
    ⑤ SORTIE — UNE valeur, de DEUX FORMES selon la branche : le fragment de page
      du tableau quand il y a au moins une ligne · sinon le message « aucune
      donnee », en petits caracteres attenues, sans aucune colonne. Mesure le
      20-09-2026 sur les vraies donnees du depot : la section Laboratoire affiche
      « aucune donnee », parce que registre_candidates.csv est absent.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre le message « aucune donnee » si la liste de lignes est
      vide · ② composer la ligne d entetes, alignees a gauche, en petits
      caracteres attenues, soulignees d un filet · ③ composer chaque ligne, case
      par case, soulignee d un filet tres pale · ④ assembler le tout dans un
      tableau qui prend toute la largeur.
    ⑦ UNITE — Les tailles sont en PIXELS : 9 pour les entetes, 11 pour les cases.
      Le nombre de lignes se compte en LIGNES DE TABLEAU.
    ⑧ POURQUOI — Les cases sont posees sans etre neutralisees, et cela se declare
      parce que c est une condition d entree : les appelants passent parfois un
      fragment de page volontaire, comme un resultat net entoure d une couleur ou
      une pastille de voyant, et neutraliser ici detruirait ces fragments. La
      contrepartie est que chaque appelant doit neutraliser lui-meme ce qui vient
      d un fichier.
    ⑨ CE QUI CLOCHE —
      ① Le nombre de cases par ligne n est jamais confronte au nombre d entetes.
      Une ligne plus courte produit un tableau ou les cases suivantes glissent
      d une colonne, sans aucun message. Releve le 20-09-2026 par lecture du corps
      de cette fonction, qui compose les cases sans jamais les compter.
      ② Le message du cas vide dit « aucune donnee », sans dire de quelle source
      il s agit ni si elle etait absente ou simplement vide. Mesure le
      20-09-2026 : la section Laboratoire affiche « aucune donnee » alors que la
      trace du pied de page, elle, precise « registre_candidates.csv, ABSENT ». Un
      lecteur qui ne deplie pas le pied de page ne peut pas faire la difference
      entre une file d idees vide et un fichier qui manque.
    ⑩ EFFET — N ecrit aucun fichier, ne lit rien, ne touche pas au reseau, n
      affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne leve pas. Aucun de ses appels
      ne se termine.
      [sort: non]
    ⑫ DEFINITIONS
      la trace : la liste des sources avec leur etat — LU, ABSENT ou ILLISIBLE
        — et un detail chiffre, affichee en pied de page.
      une comptabilite : la facon de compter les resultats, et il y en a deux,
        jamais additionnees — un jeton, une seule position a la fois avec 100
        000 € simules, et jetons illimites, toutes les occurrences du signal
        mesurees.
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if not lignes:
        return f'<div style="font-size:11px;color:{C["dim"]};padding:6px 0">aucune donnee</div>'
    h = ''.join(f'<th style="text-align:left;padding:5px 6px;color:{C["dim"]};font-size:9px;'
                f'border-bottom:1px solid {C["line"]}">{c}</th>' for c in entetes)
    b = ''.join('<tr>' + ''.join(
        f'<td style="padding:6px;font-size:11px;color:{C["mut"]};'
        f'border-bottom:1px solid rgba(255,255,255,.03)">{c}</td>' for c in r) + '</tr>' for r in lignes)
    return f'<table style="width:100%;border-collapse:collapse;margin:6px 0"><tr>{h}</tr>{b}</table>'

def barre(courant, seuil):
    """Compose une barre de progression vers le seuil de validation — et n est
    appelee par personne.

    ① ROLE — Aucun aujourd hui. Elle dessine le compteur d operations d une
      strategie : le nombre d operations realisees, le nombre a atteindre, et une
      barre verte dont la largeur dit ou on en est. `bloc_strategie` affiche bien
      ce compteur et cette barre dans la page, mais il les compose lui-meme, avec
      le meme fragment recopie, au lieu de l appeler.
    ② CONTEXTE D APPEL — PERSONNE. Releve le 20-09-2026 en rapprochant, dans l
      arbre syntaxique du fichier, les definitions et les appels : aucune des 30
      fonctions du programme ne la nomme. Elle est du code mort qui fonctionne
      toujours.
    ③ ENTREE — `courant` : le nombre d operations deja realisees. `seuil` : le
      nombre d operations a atteindre pour que la strategie soit jugee. Aucun
      appelant, donc aucune valeur reellement passee.
    ④ CONDITIONS D ENTREE — Les deux valeurs doivent etre des nombres ; un seuil
      nul ou absent est accepte et donne une barre vide.
    ⑤ SORTIE — UNE valeur : un texte, le fragment de page du compteur et de la
      barre. Mesure le 20-09-2026 avec trois operations sur cinquante : le texte
      commence par « OPÉRATIONS RÉALISÉES — 3 / 50 ».
      [rend: 1]
    ⑥ TRAITEMENT — ① poser la largeur a zero si le seuil est nul ou absent ·
      ② sinon calculer la part realisee en pourcents, plafonnee a cent · ③ ecrire
      la ligne de texte qui donne les deux nombres · ④ dessiner le fond de la
      barre, puis la part verte a la largeur calculee.
    ⑦ UNITE — `courant` et `seuil` se comptent en OPERATIONS. La largeur est en
      POURCENTS, entre 0 et 100. Les tailles sont en PIXELS : 10 pour le texte, 12
      pour la hauteur de la barre.
    ⑧ POURQUOI — La largeur est plafonnee a cent pour qu une strategie qui depasse
      son seuil ne fasse pas deborder la barre hors de son cadre. Mesure le
      20-09-2026 : la strategie C5E10-OBS-V1 en est a 3 operations sur 50, soit
      une barre a 6 %.
    ⑨ CE QUI CLOCHE —
      ① Elle n est appelee par personne, alors que `bloc_strategie` affiche
      exactement la meme chose en recopiant le meme fragment de page. Deux
      implementations d une meme chose divergent toujours (R-708) : une correction
      apportee a l une ne toucherait pas l autre, et c est la copie recopiee qui
      est affichee.
      ② Les deux versions ne portent pas le meme texte. Celle-ci ecrit
      « OPÉRATIONS RÉALISÉES » avec les accents, celle de `bloc_strategie` ecrit
      « OPERATIONS REALISEES » sans accents. C est la version sans accents que
      Jean-Luc voit : mesure le 20-09-2026 sur la page produite a partir des
      vraies donnees du depot.
      ③ Un `courant` negatif donnerait une largeur negative, qui n est pas
      plafonnee par le bas.
    ⑩ EFFET — N ecrit aucun fichier, ne lit rien, ne touche pas au reseau, n
      affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne leve pas : la division est
      evitee quand le seuil est nul. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DEFINITIONS
      le code mort : du code qui n est appele par rien et qui reste dans le
        fichier.
      le seuil de validation : le nombre d operations qu une strategie doit
        realiser avant qu on juge ses resultats.
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    pct = 0 if not seuil else min(100, 100.0 * courant / seuil)
    return (f'<div style="font-size:10px;color:{C["dim"]}">OPÉRATIONS RÉALISÉES — {courant} / {seuil}</div>'
            f'<div style="background:#12151d;border:1px solid {C["line"]};border-radius:6px;height:12px;margin:4px 0 12px">'
            f'<div style="width:{pct:.1f}%;height:100%;background:{C["grn"]};border-radius:6px"></div></div>')

def courbe_cours(serie, entree=None, sortie=None, tp=None, sl=None, w=340, h=150, titre=''):
    """Dessine la courbe d un titre avec son entree, sa sortie, son objectif et son
    seuil de perte.

    ① ROLE — Montrer en une image ce qu un tableau de chiffres ne fait pas voir :
      ou en est le cours par rapport au prix d entree, a quelle distance se
      trouvent l objectif et le seuil de perte, et quelle forme le cours a prise
      entre les deux. C est le seul usage des cours dans ce programme — ils
      servent a DESSINER, jamais a calculer un indicateur de performance.
    ② CONTEXTE D APPEL — Deux appelants, trois endroits, releves le 20-09-2026
      dans l arbre syntaxique du fichier : `bloc1_aujourdhui`, un endroit, pour la
      position ouverte, sur les 120 dernieres seances · `bloc_strategie`, deux
      endroits, pour la derniere operation du journal, une fois sur tout l
      historique et une fois sur les 60 dernieres seances.
    ③ ENTREE — `serie` : la liste des couples date et cours de cloture, rangee du
      plus ancien au plus recent, telle que `Sources.serie` la rend. `entree` : la
      date d entree a marquer, ou `None`. `sortie` : la date de sortie a marquer,
      ou `None` ; `bloc1_aujourdhui` passe `None`, puisqu une position ouverte n a
      pas de sortie. `tp` : le prix de l objectif, ou `None`. `sl` : le prix du
      seuil de perte, ou `None`. `w` : la largeur du dessin, 340 par defaut, et
      aucun appelant ne la change. `h` : la hauteur, 150 par defaut ;
      `bloc_strategie` passe 140 pour le second de ses deux graphiques. `titre` :
      le texte de remplacement du dessin, vide par defaut ; les trois appels le
      donnent.
    ④ CONDITIONS D ENTREE — La serie doit deja etre rangee par date : la fonction
      ne la range pas. Les dates d entree et de sortie doivent etre ecrites
      exactement comme celles de la serie pour etre reconnues. Les prix doivent
      etre des nombres ou `None`.
    ⑤ SORTIE — UNE valeur, de DEUX FORMES selon la branche : le dessin complet,
      sous forme de fragment de page · ou, quand la serie est vide ou ne porte
      qu un seul point, le message « cours indisponibles — graphique non produit ».
      Mesure le 20-09-2026 : une serie d un seul point rend bien ce message.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre le message si la serie porte moins de deux points ·
      ② relever le plus bas et le plus haut des cours, et les elargir a l objectif
      et au seuil de perte s ils sortent de la plage · ③ ajouter une marge de 6 %
      de part et d autre, ou une unite si la plage est plate · ④ poser le cadre de
      dessin : 40 pixels a gauche pour les graduations, 6 a droite, 14 en haut, 20
      en bas · ⑤ tracer l objectif et le seuil de perte en pointilles, avec leur
      prix ecrit a gauche · ⑥ tracer la courbe des cours en bleu · ⑦ poser un
      trait vertical et un point sur les dates d entree et de sortie, avec leur
      etiquette · ⑧ ecrire la premiere et la derniere date en bas, le plus haut et
      le plus bas a gauche.
    ⑦ UNITE — Les cours, l objectif et le seuil de perte sont en EUROS. La serie
      se compte en SEANCES de bourse. La largeur, la hauteur et les marges sont en
      PIXELS. La marge de plage est en POURCENTS de l amplitude.
    ⑧ POURQUOI — Trois choix commandent le dessin.
      ① Le message « graphique non produit » remplace le dessin au lieu de le
      laisser vide : un graphique invente serait pire que pas de graphique, sur
      une page qui sert a decider s il faut prendre position.
      ② La marge de 6 % evite que la courbe touche les bords du cadre et que le
      plus haut et le plus bas se confondent avec les graduations.
      ③ Le dessin est ecrit directement dans la page, en formes geometriques, et
      non produit comme une image a charger. Mesure le 20-09-2026 sur une page
      produite a partir des vraies donnees du depot : zero balise `img`, zero
      attribut `src`.
    ⑨ CE QUI CLOCHE —
      ① Le point d entree n est PAS pose au prix d entree, mais au cours de
      cloture du jour d entree — et la page affiche les deux. Mesure le
      20-09-2026 sur une epreuve montee avec une position d essai entree le
      2026-09-01 a 27,28 € : le texte de la section annonce « Entrée le 2026-09-01
      à 27,28 € » et l etiquette doree du graphique, juste en dessous, annonce
      « ENTRÉE 27.19 » — la cloture de BUREAU_VERITAS ce jour-la selon
      donnees/cac40_ohlcv.csv. Deux prix pour le meme evenement, sur le meme
      ecran, et rien ne dit qu ils ne mesurent pas la meme chose. Le systeme entre
      d ailleurs a l OUVERTURE du lendemain du signal, ce qui fait un troisieme
      prix encore : l ouverture du 2026-09-01 valait 27,20 €.
      ② Une date d entree absente de la serie dessinee fait disparaitre le
      marqueur, en silence. Mesure le 20-09-2026 sur une serie de trois seances a
      laquelle on demande de marquer une date anterieure : le dessin est produit,
      sans aucun marqueur ni aucun message. Le cas se produit des que la position
      a ete ouverte il y a plus de 120 seances pour le graphique de la section
      Aujourd hui, ou plus de 60 pour le second graphique de la section QA.
      ③ Les prix ecrits sur les pointilles emploient le point decimal anglais,
      alors que tous les autres prix de la page emploient la virgule. Mesure le
      20-09-2026 : le graphique affiche « objectif 110.00 » et « seuil de perte
      95.00 » tandis que le texte de la meme section affiche « 27,28 € ». Deux
      ecritures du meme genre de nombre sur le meme ecran.
      ④ Un objectif ou un seuil de perte valant exactement zero est traite comme
      une valeur absente et n est pas dessine. Ce n est pas un prix plausible pour
      une action, mais c est bien une valeur que le programme ne distingue pas de
      « non renseigne ».
      ⑤ Le texte de remplacement du dessin est neutralise, mais pas les guillemets
      qu il pourrait contenir : `esc` ne traite que l esperluette et les deux
      chevrons. Un nom de valeur portant un guillemet fermerait l attribut.
    ⑩ EFFET — N ecrit aucun fichier, ne lit rien, ne touche pas au reseau, n
      affiche rien. Le dessin rendu ne charge aucune ressource exterieure.
    ⑪ TERMINAISON — Rend toujours la main dans les deux branches. Elle ne leve
      pas : la branche du message protege des divisions par zero, et la marge
      garantit une plage non nulle. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DEFINITIONS
      l objectif : le prix auquel la position se ferme en gain.
      le seuil de perte : le prix auquel la position se ferme en perte.
      une seance : une journee de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa cloture et son volume
    
      QA : l etat d une strategie validee sur l historique mais qui n a pas encore realise assez d operations reelles pour etre jugee.
      une action : une ligne de ce tableau, identifiée par `A-` suivi d'un nombre
"""
    if not serie or len(serie) < 2:
        return f'<div style="font-size:11px;color:{C["dim"]};padding:10px 0">cours indisponibles — graphique non produit</div>'
    vals = [v for _, v in serie]
    lo, hi = min(vals), max(vals)
    if tp: hi = max(hi, tp)
    if sl: lo = min(lo, sl)
    pad = (hi - lo) * 0.06 or 1
    lo -= pad; hi += pad
    x0, x1, y0, y1 = 40, w - 6, 14, h - 20
    X = lambda i: round(x0 + (x1 - x0) * i / (len(serie) - 1), 1)
    Y = lambda v: round(y1 - (y1 - y0) * (v - lo) / (hi - lo), 1)
    pts = ' '.join(f'{X(i)},{Y(v)}' for i, (_, v) in enumerate(serie))
    idx = {d: i for i, (d, _) in enumerate(serie)}
    s = [f'<svg viewBox="0 0 {w} {h}" style="width:100%;max-width:{w}px" role="img" aria-label="{esc(titre)}">']
    for v, col, lab in ((tp, C['grn'], 'objectif'), (sl, C['red'], 'seuil de perte')):
        if v:
            s.append(f'<line x1="{x0}" y1="{Y(v)}" x2="{x1}" y2="{Y(v)}" stroke="{col}" stroke-width="1.2" '
                     f'stroke-dasharray="5 4"/><text x="2" y="{Y(v)+3}" fill="{col}" font-size="8">{lab} {v:.2f}</text>')
    s.append(f'<polyline points="{pts}" fill="none" stroke="{C["blu"]}" stroke-width="1.4"/>')
    for d, col, lab, dy in ((entree, C['gld'], 'ENTRÉE', -6), (sortie, C['vio'], 'SORTIE', 12)):
        if d and d in idx:
            i = idx[d]; v = serie[i][1]
            s.append(f'<line x1="{X(i)}" y1="{y0}" x2="{X(i)}" y2="{y1}" stroke="{col}" stroke-width="1" opacity=".55"/>'
                     f'<circle cx="{X(i)}" cy="{Y(v)}" r="4" fill="{col}"/>'
                     f'<text x="{min(X(i), w-62)}" y="{Y(v)+dy}" fill="{col}" font-size="9" font-weight="600">{lab} {v:.2f}</text>')
    s.append(f'<text x="{x0}" y="{h-4}" fill="{C["dim"]}" font-size="8">{serie[0][0]}</text>'
             f'<text x="{x1-52}" y="{h-4}" fill="{C["dim"]}" font-size="8">{serie[-1][0]}</text>'
             f'<text x="2" y="{y0+4}" fill="{C["dim"]}" font-size="8">{hi:.0f}€</text>'
             f'<text x="2" y="{y1}" fill="{C["dim"]}" font-size="8">{lo:.0f}€</text></svg>')
    return ''.join(s)

def courbe_cumul(pnls, w=340, h=120):
    """Dessine une courbe cumulee a partir d une suite d ecarts, en partant de zero.

    ① ROLE — Montrer la forme d une progression plutot que sa seule valeur du
      jour : une suite de gains et de pertes se lit mal dans un tableau, et se
      voit tout de suite sur une courbe. Elle sert a la courbe d evolution du
      cumul net affichee dans les sections QA et Production.
    ② CONTEXTE D APPEL — Un seul appelant : `bloc_strategie`, un endroit, et
      seulement quand l historique des mesures porte au moins deux releves pour la
      strategie. `bloc_strategie` ne lui passe pas le cumul, mais les ECARTS d un
      releve au suivant.
    ③ ENTREE — `pnls` : la liste des ecarts a cumuler, en euros. `w` : la largeur
      du dessin, 340 par defaut, et l appelant ne la change pas. `h` : la hauteur,
      120 par defaut, et l appelant ne la change pas.
    ④ CONDITIONS D ENTREE — Les ecarts doivent etre des nombres, dans l ordre du
      temps. Une liste vide est acceptee.
    ⑤ SORTIE — UNE valeur, de DEUX FORMES selon la branche : le dessin complet,
      sous forme de fragment de page · ou, quand la liste est vide, le message
      « aucune opération clôturée — courbe non produite ». Mesure le 20-09-2026 :
      une liste vide rend bien ce message.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre le message si la liste est vide · ② construire la
      suite cumulee en partant de zero et en ajoutant chaque ecart · ③ relever le
      plus bas et le plus haut, zero compris, et les elargir de 10 % · ④ poser le
      cadre de dessin : 46 pixels a gauche, 6 a droite, 12 en haut, 18 en bas ·
      ⑤ tracer la ligne du zero, avec son etiquette · ⑥ ecrire la valeur la plus
      haute atteinte · ⑦ tracer la courbe en vert et poser un point sur le dernier
      releve.
    ⑦ UNITE — Les ecarts et la suite cumulee sont en EUROS. La largeur, la hauteur
      et les marges sont en PIXELS. La marge de plage est en POURCENTS de l
      amplitude.
    ⑧ POURQUOI — La ligne du zero est tracee et etiquetee parce que c est la seule
      graduation qui a un sens ici : une courbe de gains cumules se lit d abord a
      la question « est-on au-dessus ou en dessous de zero ». Zero est aussi
      toujours inclus dans la plage, pour que cette ligne reste visible meme quand
      toute la courbe est du meme cote.
    ⑨ CE QUI CLOCHE —
      ① La courbe affichee dans la page contredit le chiffre affiche juste
      au-dessus d elle. Elle part toujours de zero, donc elle perd la valeur de
      depart de ce qu on lui donne a cumuler. Mesure le 20-09-2026 sur les 14
      releves de la strategie C5E10-OBS-V1 en comptabilite un jeton : les cumuls
      lus dans donnees/historique_mesures.csv vont de 6 884,75 € le 2026-08-26 a
      1 292,25 € le 2026-09-17, et la courbe dessinee part de 0 € et finit a
      -5 592,50 €. Le tableau de la meme section affiche pourtant « 1292.25 € ».
      ② Deux etiquettes se superposent exactement quand la courbe ne monte jamais
      au-dessus de zero. L etiquette du zero et celle de la valeur la plus haute
      sont posees a la meme hauteur, et portent le meme texte. Mesure le
      20-09-2026 sur les ecarts reels de C5E10-OBS-V1 : les deux etiquettes sont
      ecrites a la hauteur 22,5 et disent toutes deux « 0 € ».
      ③ L etiquette du haut donne la valeur la plus HAUTE atteinte, jamais la
      valeur FINALE, alors que c est le point final que le dessin met en evidence
      par un rond vert. Un lecteur qui cherche ou finit la courbe lit un chiffre
      qui n est pas le sien.
      ④ Le remplacement du separateur de milliers s applique a tout le fragment
      compose jusque-la, pas seulement au nombre : la ligne du zero, sa graduation
      et le cadre du dessin y passent aussi. Aucun d eux ne contient de virgule
      aujourd hui, et c est la seule raison pour laquelle rien ne se voit.
      ⑤ Le nombre est arrondi a l euro entier, alors que les montants du journal
      sont affiches avec deux decimales. Mesure le 20-09-2026 sur les ecarts
      1 234 567 et 1 : l etiquette rend `1 234 568 €`, la ou `f_eur` sur la meme
      valeur rendrait `+1 234 568,00 €`.
    ⑩ EFFET — N ecrit aucun fichier, ne lit rien, ne touche pas au reseau, n
      affiche rien. Le dessin rendu ne charge aucune ressource exterieure.
    ⑪ TERMINAISON — Rend toujours la main dans les deux branches. Elle ne leve
      pas : la branche du message protege du cas vide, et la marge garantit une
      plage non nulle. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DEFINITIONS
      l historique des mesures : donnees/historique_mesures.csv, une ligne par
        jour, par strategie et par comptabilite, jamais reecrit.
      une comptabilite : la facon de compter les resultats, et il y en a deux,
        jamais additionnees — un jeton, une seule position a la fois avec 100
        000 € simules, et jetons illimites, toutes les occurrences du signal
        mesurees.
    
      PRODUCTION : l etat d une strategie dont le seuil d operations est atteint et les resultats conformes, donc exploitee.
      QA : l etat d une strategie validee sur l historique mais qui n a pas encore realise assez d operations reelles pour etre jugee.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if not pnls:
        return f'<div style="font-size:11px;color:{C["dim"]};padding:8px 0">aucune opération clôturée — courbe non produite</div>'
    cum, serie = 0.0, [0.0]
    for p in pnls:
        cum += p; serie.append(cum)
    lo, hi = min(serie + [0.0]), max(serie + [0.0])
    pad = (hi - lo) * 0.1 or 1
    lo -= pad; hi += pad
    x0, x1, y0, y1 = 46, w - 6, 12, h - 18
    X = lambda i: round(x0 + (x1 - x0) * i / max(1, len(serie) - 1), 1)
    Y = lambda v: round(y1 - (y1 - y0) * (v - lo) / (hi - lo), 1)
    pts = ' '.join(f'{X(i)},{Y(v)}' for i, v in enumerate(serie))
    return (f'<svg viewBox="0 0 {w} {h}" style="width:100%;max-width:{w}px" role="img" aria-label="gains cumulés">'
            f'<line x1="{x0}" y1="{Y(0)}" x2="{x1}" y2="{Y(0)}" stroke="{C["line"]}" stroke-width="1"/>'
            f'<text x="2" y="{Y(0)+3}" fill="{C["dim"]}" font-size="8">0 €</text>'
            f'<text x="2" y="{Y(max(serie))+3}" fill="{C["dim"]}" font-size="8">{max(serie):,.0f} €</text>'.replace(',', ' ') +
            f'<polyline points="{pts}" fill="none" stroke="{C["grn"]}" stroke-width="2"/>'
            f'<circle cx="{X(len(serie)-1)}" cy="{Y(serie[-1])}" r="3" fill="{C["grn"]}"/></svg>')

# --------------------------------------------------------------------------
# LES 6 BLOCS (A-207 V1)
# --------------------------------------------------------------------------
def bloc1_aujourdhui(S):
    """Compose la section « Aujourd hui », qui repond a une seule question : prend-on
    position ?

    ① ROLE — Donner la reponse que Jean-Luc vient chercher en premier. La section
      a deux etats qui s excluent. Jeton engage : une position est en cours, et la
      section affiche sa valeur, sa date d entree, son prix d entree, son
      echeance, sa variation latente et le graphique du cours avec l objectif et
      le seuil de perte. Jeton libre : aucune position, et la section affiche
      qu aucune entree n a lieu, plus le rappel des deux verifications que rien
      n automatise. Un bandeau ferme la section avec la date du dernier cours et
      le resultat du controle du soir.
    ② CONTEXTE D APPEL — Un seul appelant : `construire`, une fois, pour la
      premiere des six sections de la page.
    ③ ENTREE — `S` : l objet des sources, deja charge. La section y lit les cours,
      les positions ouvertes, le texte de l audit du jour et la presence du
      dernier rapport de boucle.
    ④ CONDITIONS D ENTREE — Aucune source n est obligatoire. Les cours absents
      donnent « n.d. » comme date, l audit absent donne « controle
      indisponible », le rapport absent change la phrase affichee.
    ⑤ SORTIE — UNE valeur : un texte, le fragment de page de la section, corps
      puis bandeau.
      [rend: 1]
    ⑥ TRAITEMENT — ① relever la date de cours la plus recente, toutes valeurs
      confondues · ② compter dans le texte de l audit les marqueurs de reussite,
      d avertissement et d echec, et composer le verdict · ③ relever les positions
      dont le statut commence par OUVERT, et prendre toutes les positions si
      aucune ne correspond · ④ s il y a une position : lire son objectif, son
      seuil de perte et son prix d entree, calculer la variation latente entre le
      dernier cours et le prix d entree, et composer le cadre puis le graphique
      des 120 dernieres seances · ⑤ sinon composer le cadre « Aucune entree
      aujourd hui » et le rappel des verifications manuelles · ⑥ composer le
      bandeau et le coller sous le corps.
    ⑦ UNITE — Les prix sont en EUROS. La variation latente est en POURCENTS. Le
      graphique porte sur 120 SEANCES de bourse. Les compteurs de l audit se
      comptent en MARQUEURS trouves dans le texte.
    ⑧ POURQUOI — Le rappel des deux verifications manuelles n est affiche que
      lorsqu il n y a pas de position, c est-a-dire au seul moment ou il sert : ce
      sont des controles a faire AVANT d entrer. Les deux regles pre-trade —
      aucune publication de resultats sous 3 jours, aucune intervention de banque
      centrale sous 24 heures — ne sont automatisees par aucun programme du
      systeme, et la page le dit pour que personne ne croie qu elles le sont.
    ⑨ CE QUI CLOCHE —
      ① Une position FERMEE est affichee comme une position OUVERTE. Quand aucune
      ligne ne porte un statut commencant par OUVERT, le programme retombe sur la
      liste entiere des positions au lieu de conclure qu il n y en a aucune.
      Mesure le 20-09-2026 sur une epreuve ou la seule ligne porte le statut
      `FERMEE` : la page affiche « Position ouverte — BUREAU_VERITAS », avec sa
      variation latente et son graphique. C est la reponse inverse de celle que
      la section promet, sur la question que Jean-Luc pose en premier.
      ② Le verdict du controle compte des marqueurs dans un texte au lieu de lire
      un resultat, et il se trompe sur le vrai rapport. Mesure le 20-09-2026 avec
      rapports/audit_du_jour.md du depot : la page affiche « 46 ✅ · 14 ⚠️ · 2 ❌ »,
      alors que la deuxieme ligne du rapport, ecrite par le programme de
      surveillance lui-meme, dit « Score : 45 ✅ · 10 ⚠️ · 0 ❌ ». Cette ligne de
      score est elle-meme comptee, ce qui explique une unite de chaque ecart ; le
      reste vient de marqueurs employes ailleurs dans le texte. La page annonce
      donc deux echecs la ou le rapport n en declare aucun.
      ③ Une variable locale porte le meme nom qu une fonction du fichier. La
      valeur de la position est rangee sous le nom `val`, qui est aussi le nom de
      la fonction qui lit un champ de mesure. Tant que cette section n appelle pas
      cette fonction, rien ne casse ; le jour ou quelqu un l y appellerait, le
      programme tomberait sur une erreur de variable non definie, y compris dans
      la branche ou aucune position n existe. Releve le 20-09-2026 sur la ligne qui
      range la valeur de la position sous le nom `val`.
      ④ La variation latente est calculee ici, alors que la section affiche par
      ailleurs des chiffres lus. Elle compare le dernier cours connu au prix d
      entree, sans frais et sans convention, et ne correspond donc a aucun des
      chiffres que le service MESURER LA PERFORMANCE ecrit.
      ⑤ Le graphique et le texte donnent deux prix differents pour la meme
      entree. Mesure le 20-09-2026 sur une epreuve avec une position d essai : le
      texte annonce « Entrée le 2026-09-01 à 27,28 € » et l etiquette du graphique
      « ENTRÉE 27.19 », qui est la cloture de ce jour-la.
      ⑥ Seule la PREMIERE position est affichee. Le systeme n en autorise qu une a
      la fois par strategie, mais rien ici ne le verifie ni ne signale les autres.
    ⑩ EFFET — LIT des donnees deja en memoire. N ouvre aucun fichier, n ecrit
      rien, ne touche pas au reseau, n affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne leve pas : les conversions de
      prix sont rattrapees. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DEFINITIONS
      l audit du jour : le compte rendu du programme de surveillance, qui dit
        ce qui est vert, ce qui avertit et ce qui a echoue.
      l objectif : le prix auquel la position se ferme en gain.
      la variation latente : l ecart entre le dernier cours connu et le prix d
        entree d une position encore ouverte, exprime en pourcents.
      le jeton : les 100 000 € simules du portefeuille, engages sur une seule
        position a la fois.
      le seuil de perte : le prix auquel la position se ferme en perte.
      les regles pre-trade : les deux verifications a faire avant d entrer, qu
        aucun programme n automatise — aucune publication de resultats sous 3
        jours, aucune intervention de banque centrale sous 24 heures.
      un rapport de boucle : le compte rendu que le circuit du soir ecrit
        apres chaque passage, sous un nom de la forme
        rapport_boucle_AAAA-MM-JJ.md.
    
      le service MESURER LA PERFORMANCE : programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py, le seul programme autorise a calculer les indicateurs de performance.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    # fraicheur : derniere date de cours toutes valeurs confondues
    dates = sorted({d for v in S.ohlcv.values() for d in v})
    derniere = dates[-1] if dates else None
    # verdict du controle : compte des marqueurs dans l'audit
    verdict = 'contrôle indisponible'
    if S.audit:
        ok, warn, ko = S.audit.count('✅'), S.audit.count('⚠'), S.audit.count('❌')
        verdict = (f'<b style="color:{C["grn"]}">{ok} ✅</b> · <b style="color:{C["gld"]}">{warn} ⚠️</b> · '
                   f'<b style="color:{C["red"]}">{ko} ❌</b>')
    ouvertes = [p for p in S.positions if (p.get('statut') or '').upper().startswith('OUVERT')] or S.positions

    if ouvertes:
        p = ouvertes[0]
        val = p.get('valeur', '?')
        serie = S.serie(val)
        try:
            tp, sl = float(p.get('tp') or 0) or None, float(p.get('sl') or 0) or None
            pe = float(p.get('prix_entree') or 0)
        except ValueError:
            tp = sl = None; pe = 0.0
        dernier = serie[-1][1] if serie else None
        latent = ((dernier - pe) / pe * 100) if (dernier and pe) else None
        corps = (f'<div style="border:1px solid {C["line"]};border-radius:8px;padding:12px;margin-bottom:8px">'
                 f'<div style="font-size:19px;color:{C["txt"]}">Position ouverte — {esc(val)}</div>'
                 f'<div style="font-size:11px;color:{C["mut"]};margin-top:6px;line-height:1.6">'
                 f'Entrée le {esc(p.get("date_entree","?"))} à {f_eur(pe, False)} · échéance {esc(p.get("horizon_fin","?"))}'
                 + (f' · variation latente {f_pct(latent)} au cours du {serie[-1][0]}' if latent is not None else '')
                 + f'</div></div>'
                 + courbe_cours(serie[-120:], p.get('date_entree'), None, tp, sl, titre=f'{val} en position')
                 + f'<div style="font-size:10px;color:{C["dim"]};margin-top:4px">Bleu : le cours. Point doré : entrée. '
                   f'Pointillé vert : objectif. Pointillé rouge : seuil de perte.</div>')
    else:
        # jeton libre : le rapport de boucle porte le verdict du jour
        phrase = 'Aucune position ouverte — capital disponible.'
        detail = ('Le rapport automatique le plus récent ne signale aucun signal d\'entrée.'
                  if S.rapport else 'Rapport automatique indisponible : signal du jour indéterminé.')
        corps = (f'<div style="border:1px solid {C["line"]};border-radius:8px;padding:12px;margin-bottom:8px">'
                 f'<div style="font-size:19px;color:{C["txt"]}">Aucune entrée aujourd\'hui</div>'
                 f'<div style="font-size:11px;color:{C["mut"]};margin-top:6px;line-height:1.6">{phrase} {detail}</div>'
                 f'<div style="font-size:11px;color:{C["gld"]};margin-top:8px">⚠ Vérifications manuelles avant toute '
                 f'entrée : publication de résultats sous 3 jours ? intervention de banque centrale sous 24 h ? '
                 f'Aucun automatisme ne les couvre.</div></div>')

    bandeau = (f'<div style="display:flex;gap:8px;flex-wrap:wrap;font-size:10px;color:{C["mut"]}">'
               f'<span style="border:1px solid {C["line"]};border-radius:6px;padding:5px 8px">Cours à jour : '
               f'<b style="color:{C["txt"]}">{derniere or "n.d."}</b></span>'
               f'<span style="border:1px solid {C["line"]};border-radius:6px;padding:5px 8px">Contrôle : {verdict}</span></div>')
    return corps + bandeau

def bloc_strategie(S, etat, titre_vide):
    """Compose la section d une strategie — QA ou Production — a partir des
    indicateurs deja mesures.

    ① ROLE — Montrer ou en est une strategie : son identite et ses reglages, son
      compteur d operations vers le seuil de validation, ses resultats dans les
      deux comptabilites, le verdict de son garde-fou, l evolution de son cumul et
      le graphique de la derniere operation du journal. La meme fonction sert les
      deux sections de la page, avec un etat different, pour que QA et Production
      aient exactement la meme forme.
    ② CONTEXTE D APPEL — Un seul appelant : `construire`, deux fois — une fois
      avec l etat `QA` et le message de repli « Aucune stratégie en QA », une fois
      avec l etat `PRODUCTION` et le message « Aucune stratégie en service ».
    ③ ENTREE — `S` : l objet des sources, deja charge. `etat` : le debut de l etat
      de vie cherche, `QA` ou `PRODUCTION`. `titre_vide` : le texte a afficher
      quand aucune strategie ne porte cet etat.
    ④ CONDITIONS D ENTREE — Aucune source n est obligatoire. L etat civil absent
      fait afficher le message de repli ; l historique des mesures absent fait
      afficher qu aucun indicateur n est disponible.
    ⑤ SORTIE — UNE valeur : un texte, le fragment de page de la section, sous
      TROIS FORMES selon la branche. Le message de repli suivi d une description
      de ce qu on verrait, quand aucune strategie ne porte l etat. Un message
      disant qu aucun indicateur n a encore ete ecrit, quand la strategie existe
      mais n a aucune mesure. Sinon la section complete : entete, tableau des deux
      comptabilites, verdict du garde-fou, courbe d evolution s il y a au moins
      deux releves, graphiques du dernier titre traite, et mention de la source.
      [rend: 1]
    ⑥ TRAITEMENT — ① chercher la derniere ligne de vie portant l etat demande, et
      rendre le message de repli s il n y en a pas · ② lire le nom de la strategie
      · ③ chercher sa derniere mesure dans chacune des deux comptabilites, et
      rendre un message s il n y en a aucune · ④ lire le seuil de validation et le
      compteur, et calculer la part realisee pour la largeur de la barre ·
      ⑤ composer l entete avec le nom, l objectif, le seuil de perte, l echeance
      et le compteur · ⑥ composer le tableau des deux comptabilites, valeurs lues ·
      ⑦ composer le verdict du garde-fou et son voyant, lus · ⑧ si l historique
      porte au moins deux releves, composer la courbe d evolution a partir des
      ecarts d un releve au suivant · ⑨ si le journal n est pas vide, prendre sa
      derniere operation, calculer son seuil de perte en euros, et composer deux
      graphiques — tout l historique, puis 60 seances · ⑩ ajouter la mention de la
      source et assembler.
    ⑦ UNITE — Le compteur et le seuil de validation se comptent en OPERATIONS. La
      largeur de la barre est en POURCENTS, plafonnee a 100. Les prix sont en
      EUROS, les taux en POURCENTS. Le second graphique porte sur 60 SEANCES.
    ⑧ POURQUOI — Tous les indicateurs affiches sont LUS dans
      donnees/historique_mesures.csv et aucun n est recalcule ici. Deux
      implementations d une meme chose divergent toujours (R-708) : si cette
      section calculait son taux de reussite, la page et le rapport du soir
      finiraient par annoncer deux chiffres differents pour la meme semaine. C est
      la decision du 15-08-2026, et c est pourquoi la section porte en bas la
      mention « aucun calcul effectue ici » avec la date de la mesure employee :
      un chiffre affiche doit pouvoir etre retrouve, caractere pour caractere,
      dans le fichier.
    ⑨ CE QUI CLOCHE —
      ① La mention « aucun calcul effectue ici » est fausse. La section calcule et
      affiche la largeur de la barre du compteur, le seuil de perte en euros
      dessine sur les graphiques, et les ecarts d un releve au suivant qui
      nourrissent la courbe d evolution. Aucun n est un indicateur de performance,
      mais la phrase promet plus que ce que la section tient.
      ② La courbe d evolution contredit le tableau place juste au-dessus d elle.
      Elle recoit les ecarts d un releve au suivant et les re-additionne en
      partant de zero, ce qui perd la valeur de depart. Mesure le 20-09-2026 sur
      les 14 releves de C5E10-OBS-V1 en comptabilite un jeton : les cumuls lus
      vont de 6 884,75 € le 2026-08-26 a 1 292,25 € le 2026-09-17, la courbe part
      de 0 € et finit a -5 592,50 €, et le tableau de la meme section affiche
      « 1292.25 € ».
      ③ Le graphique montre la derniere operation du JOURNAL, sans verifier qu
      elle appartient a la strategie decrite. Les deux sections, QA et Production,
      dessineraient donc la meme operation. Releve le 20-09-2026 sur la ligne qui prend la
      derniere operation du journal, sans aucun filtre sur la strategie.
      ④ Le prix de sortie selon la convention du backtest est passe au graphique
      comme s il etait l objectif, et s y affiche sous l etiquette « objectif ».
      Ce sont deux choses differentes : l objectif est le prix vise a l avance, le
      prix de convention est le prix retenu apres coup pour rester comparable aux
      chiffres de reference. Releve le 20-09-2026 sur la ligne qui lit le prix de
      sortie de convention et le passe au graphique comme objectif.
      ⑤ Le graphique disparait sans un mot quand les cours du titre sont
      introuvables. Mesure le 20-09-2026 sur les vraies donnees du depot : la
      derniere operation du journal porte le nom `UNIBAIL_RODAMCO`, les fichiers
      de cours connaissent `UNIBAIL-RODAMCO-WESTFIELD`, la serie rendue est vide,
      et la section ne porte aucune mention de graphique — le message « cours
      indisponibles » existe pourtant dans `courbe_cours`, mais il n est jamais
      atteint.
      ⑥ Le rattrapage du calcul du seuil de perte ne couvre qu une seule sorte d
      erreur. Un champ absent, qui vaut alors `None`, ne serait pas rattrape par
      la branche ecrite, qui n attend qu une valeur illisible. Releve le 20-09-2026 sur le bloc de rattrapage
      du calcul du seuil de perte en euros, qui n attend qu une valeur illisible.
      ⑦ Le compteur et le seuil de validation sont poses dans la page sans etre
      neutralises, alors que le nom de la strategie, lui, l est. Ils viennent tous
      les trois du meme fichier.
      ⑧ La barre du compteur est composee ici en recopiant le fragment de page que
      la fonction `barre` produit deja, et les deux textes different : `barre`
      ecrit « OPÉRATIONS RÉALISÉES » avec les accents, cette section « OPERATIONS
      REALISEES » sans accents. C est la version sans accents que Jean-Luc voit.
    ⑩ EFFET — LIT des donnees deja en memoire. N ouvre aucun fichier, n ecrit
      rien, ne touche pas au reseau, n affiche rien.
    ⑪ TERMINAISON — Rend toujours la main dans les trois branches. Elle ne leve
      pas sur les donnees du depot du 20-09-2026 : les conversions sont
      rattrapees. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DEFINITIONS
      PRODUCTION : l etat d une strategie dont le seuil d operations est
        atteint et les resultats conformes, donc exploitee.
      QA : l etat d une strategie validee sur l historique mais qui n a pas
        encore realise assez d operations reelles pour etre jugee.
      la convention du backtest : la facon pessimiste de compter un resultat,
        qui retient le prix de l objectif meme quand le cours a saute
        par-dessus, pour rester comparable aux chiffres de reference.
      le point mort : le taux de réussite en dessous duquel une stratégie perd de l'argent
      le service MESURER LA PERFORMANCE : programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py,
        le seul programme autorise a calculer les indicateurs de performance.
      le seuil de validation : le nombre d operations qu une strategie doit
        realiser avant qu on juge ses resultats.
      un garde-fou : une limite qui, franchie, fait cesser a la strategie de
        prendre position tout en continuant a la mesurer.
      une comptabilite : la facon de compter les resultats, et il y en a deux,
        jamais additionnees — un jeton, une seule position a la fois avec 100
        000 € simules, et jetons illimites, toutes les occurrences du signal
        mesurees.
      une ligne de vie : une ligne de donnees/cac40_strategies.csv, qui donne
        l etat civil d une strategie a une date.
    
      l historique des mesures : donnees/historique_mesures.csv, une ligne par jour, par strategie et par comptabilite, jamais reecrit.
      le seuil de perte : le prix auquel la position se ferme en perte.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    carte = carte_strategie(S.strategies, etat)
    if not carte:
        return (f'<div style="font-size:15px;color:{C["mut"]}">{titre_vide}</div>'
                f'<div style="font-size:11px;color:{C["mut"]};margin-top:6px;line-height:1.6">'
                f'Structure identique a l autre section : graphique du titre avec entree, objectif et '
                f'seuil de perte, compteur, comparaison a la reference.</div>')
    ident = carte.get('id') or carte.get('nom') or '?'
    mj = derniere_mesure(S.mesures, ident, 'un jeton')
    mi = derniere_mesure(S.mesures, ident, 'jetons il')
    if not mj and not mi:
        return (f'<div style="font-size:12px;color:{C["txt"]}">Strategie <b>{esc(ident)}</b></div>'
                f'<div style="font-size:11px;color:{C["gld"]};margin-top:8px;line-height:1.6">'
                f'Aucun indicateur disponible : le service MESURER LA PERFORMANCE n a pas encore ecrit '
                f'de mesure pour cette strategie. Rien n est calcule ici — voir historique_mesures.csv.</div>')

    seuil = val(mj or mi, 'seuil', '?')
    compteur = val(mj or mi, 'compteur', '0')
    try:
        pct = min(100, 100 * float(compteur) / float(seuil))
    except (TypeError, ValueError, ZeroDivisionError):
        pct = 0

    entete = (f'<div style="font-size:11px;color:{C["mut"]};line-height:1.6;margin-bottom:8px">'
              f'Strategie <b style="color:{C["txt"]}">{esc(ident)}</b> — objectif '
              f'<b style="color:{C["grn"]}">{esc(carte.get("tp","?"))}</b>, seuil de perte '
              f'<b style="color:{C["red"]}">{esc(carte.get("sl","?"))}</b>, echeance '
              f'{esc(carte.get("horizon","?"))}. Validation a <b style="color:{C["txt"]}">{seuil} '
              f'operations</b>.</div>'
              f'<div style="font-size:10px;color:{C["dim"]}">OPERATIONS REALISEES — {compteur} / {seuil}</div>'
              f'<div style="background:#12151d;border:1px solid {C["line"]};border-radius:6px;height:12px;'
              f'margin:4px 0 12px"><div style="width:{pct:.1f}%;height:100%;background:{C["grn"]};'
              f'border-radius:6px"></div></div>')

    # tableau des deux comptabilites — valeurs LUES
    lignes = []
    for lab, m in (('Un jeton (portefeuille reel)', mj), ('Jetons illimites (qualite du signal)', mi)):
        if not m:
            lignes.append([lab, 'aucune mesure', '', '', ''])
            continue
        lignes.append([lab, val(m, 'n_operations'), val(m, 'taux_reussite') + ' %',
                       val(m, 'cumul_net_eur') + ' €', val(m, 'conformite_promis')])
    tableau = tab(['Comptabilite', 'Operations', 'Reussite', 'Cumul net', 'Face au promis'], lignes)

    # verdict du garde-fou, LU (point mort calcule par le service)
    m0 = mj or mi
    verdict = (f'<div style="font-size:11px;color:{C["mut"]};margin:8px 0;line-height:1.6">'
               f'<b>Garde-fou taux de reussite</b> : {esc(val(m0, "verdict_c7"))} '
               f'(point mort de cette strategie : {esc(val(m0, "point_mort"))} %) — {voyant(m0, "voyant_c7")}'
               f'</div>')

    # evolution dans le temps, si l historique compte plusieurs jours
    evo = ''
    serie = serie_mesure(S.mesures, 'cumul_net_eur', ident, 'un jeton')
    if len(serie) >= 2:
        evo = (f'<div style="font-size:11px;color:{C["txt"]};margin:10px 0 2px">Evolution du cumul '
               f'({len(serie)} releves)</div>' + courbe_cumul([b - a for (_, a), (_, b) in zip(serie, serie[1:])]))

    # graphique du dernier titre traite — les COURS servent au DESSIN, pas au calcul
    graph = ''
    if S.trades:
        tr = S.trades[-1]
        sr = S.serie(tr.get('valeur', ''))
        try:
            tp = float(tr.get('prix_sortie_convention') or 0) or None
        except ValueError:
            tp = None
        sl = None
        try:
            pe = float(tr.get('prix_entree') or 0)
            slp = float(str(carte.get('sl') or '').replace('%', '').replace(',', '.') or 0)
            if pe and slp:
                sl = round(pe * (1 + slp / 100), 2) if slp < 0 else round(pe * (1 - slp / 100), 2)
        except ValueError:
            pass
        if sr:
            graph = (f'<div style="font-size:11px;color:{C["txt"]};margin:10px 0 2px">'
                     f'{esc(tr.get("valeur",""))} — historique complet, entree et sortie situees</div>'
                     + courbe_cours(sr, tr.get('date_entree'), tr.get('date_sortie'), tp, sl, titre='historique')
                     + f'<div style="font-size:11px;color:{C["txt"]};margin:12px 0 2px">60 dernieres seances</div>'
                     + courbe_cours(sr[-60:], tr.get('date_entree'), tr.get('date_sortie'), tp, sl, h=140, titre='60 seances')
                     + f'<div style="font-size:10px;color:{C["dim"]};margin-top:4px">Bleu : le cours. '
                       f'Point dore : entree. Point violet : sortie. Pointille vert : objectif. '
                       f'Pointille rouge : seuil de perte.</div>')

    src = (f'<div style="font-size:9px;color:{C["dim"]};margin-top:8px">Indicateurs lus dans '
           f'historique_mesures.csv (mesure du {esc(val(m0, "date_mesure"))}) — aucun calcul effectue ici.</div>')
    return entete + tableau + verdict + evo + graph + src


def bloc_laboratoire(S):
    """Compose la section « Laboratoire » : le tableau des idees a l etude.

    ① ROLE — Montrer ce qui est en cours d etude sans engager d argent, pour que
      la page ne donne pas l impression que le systeme se limite a ce qu il joue.
      Chaque idee est decrite par trois choses : son nom, d ou elle vient, et ou
      elle en est.
    ② CONTEXTE D APPEL — Un seul appelant : `construire`, une fois, pour la
      quatrieme des six sections de la page.
    ③ ENTREE — `S` : l objet des sources, deja charge. La section n y lit qu une
      chose, la file d idees issue de registre_candidates.csv.
    ④ CONDITIONS D ENTREE — Aucune. Une file vide ou un fichier absent sont
      acceptes.
    ⑤ SORTIE — UNE valeur : un texte, le fragment de page du tableau, ou le
      message « aucune donnee » quand la file est vide. Mesure le 20-09-2026 sur
      les vraies donnees du depot : la section affiche « aucune donnee », parce
      que registre_candidates.csv n est pas au depot.
      [rend: 1]
    ⑥ TRAITEMENT — ① pour chaque idee, lire son nom, son origine et son stade, et
      les neutraliser · ② composer un tableau a trois colonnes.
    ⑦ UNITE — Un NOMBRE D IDEES, soit une LIGNE DE TABLEAU par idee.
    ⑧ POURQUOI — Les trois valeurs sont neutralisees avant d etre posees dans la
      page, parce qu elles viennent d un fichier ecrit a la main : un nom d idee
      contenant un chevron casserait la page a partir de cet endroit.
    ⑨ CE QUI CLOCHE —
      ① Un nom d idee absent devient un point d interrogation, mais une origine ou
      un stade absents deviennent une case vide, sans point d interrogation. Trois
      colonnes du meme tableau, trois comportements a l absence dont deux se
      ressemblent. Releve le 20-09-2026 sur la ligne qui compose
      chaque ligne du tableau.
      ② Le message du cas vide ne distingue pas une file d idees vide d un fichier
      absent. Mesure le 20-09-2026 : la section affiche « aucune donnee » alors
      que la trace du pied de page precise « registre_candidates.csv, ABSENT ». Un
      lecteur qui ne deplie pas le pied de page ne peut pas faire la difference.
      ③ Les colonnes de la page sont titrees « Idée, Origine, Statut », alors que
      la colonne lue dans le fichier s appelle `stade`. Deux mots pour la meme
      chose, a un ecran d ecart.
    ⑩ EFFET — LIT une liste deja en memoire. N ouvre aucun fichier, n ecrit rien,
      ne touche pas au reseau, n affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne leve pas. Aucun de ses appels
      ne se termine.
      [sort: non]
    ⑫ DEFINITIONS
      la file d idees : registre_candidates.csv, la liste des strategies a l
        etude, qui n engagent aucun argent.
      la trace : la liste des sources avec leur etat — LU, ABSENT ou ILLISIBLE
        — et un detail chiffre, affichee en pied de page.
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    lignes = [[esc(c.get('nom', '?')), esc(c.get('origine', '')), esc(c.get('stade', ''))] for c in S.candidates]
    return tab(['Idée', 'Origine', 'Statut'], lignes)

def bloc_journal(S):
    """Compose la section « Operations cloturees » : le tableau des operations, puis
    leur synthese lue.

    ① ROLE — Donner la liste complete de ce qui a ete joue, operation par
      operation, avec sa date de sortie, son titre, ses prix, son motif de sortie
      et son resultat net colore ; puis, en dessous, une synthese qui n est pas
      calculee ici mais lue dans l historique des mesures. Le tableau sert a
      verifier, la synthese a juger.
    ② CONTEXTE D APPEL — Un seul appelant : `construire`, une fois, pour la
      cinquieme des six sections de la page.
    ③ ENTREE — `S` : l objet des sources, deja charge. La section y lit deux
      choses : le journal des operations cloturees et l historique des mesures.
    ④ CONDITIONS D ENTREE — Chaque ligne du journal doit porter un resultat net
      CONVERTIBLE EN NOMBRE : c est la seule condition dure de tout le programme,
      et elle n est pas rattrapee.
    ⑤ SORTIE — UNE valeur : un texte, le fragment de page — le tableau des
      operations, suivi soit de la synthese et de la mention de sa source, soit
      d un message disant qu aucune mesure n a encore ete ecrite.
      [rend: 1]
    ⑥ TRAITEMENT — ① pour chaque operation, composer une ligne : date de sortie,
      titre avec, dessous en petit, strategie et comptabilite (« NON DITE » si
      la case est vide), prix d entree, prix de sortie, motif, et resultat net en vert s il
      est positif, en rouge sinon · ② chercher la mesure la plus recente en
      comptabilite un jeton, toutes strategies confondues · ③ si elle existe,
      composer la synthese — gagnantes sur total, serie en cours, pire chute,
      cumul net — et la mention de sa date · ④ sinon composer un message disant
      que le service n a pas encore ecrit de mesure · ⑤ assembler.
    ⑦ UNITE — Les prix et les resultats sont en EUROS. La serie en cours se compte
      en OPERATIONS consecutives, avec un signe qui dit gains ou pertes. Le
      tableau se compte en LIGNES, une par operation.
    ⑧ POURQUOI — La synthese est lue et non calculee, et la section le declare en
      toutes lettres avec la date de la mesure employee. C est la decision du
      15-08-2026 : deux implementations d une meme chose divergent toujours
      (R-708), et un chiffre affiche doit pouvoir etre retrouve caractere pour
      caractere dans donnees/historique_mesures.csv. Le resultat net est colore,
      et c est la seule couleur porteuse de sens du tableau : elle evite d avoir a
      lire le signe.
    ⑨ CE QUI CLOCHE —
      ① CORRIGE LE 27-09-2026 POUR LE TABLEAU (defaut 3 de A-491) : chaque ligne
      porte desormais sa strategie et sa comptabilite, lues au journal qui a recu
      cette colonne le meme jour. Le constat d origine suit. Le tableau et la
      synthese se contredisaient sur le meme ecran. Le tableau
      affiche toutes les lignes du journal sans distinguer les deux
      comptabilites, alors que le meme trade y est ecrit une fois en « un jeton »
      et une fois en « jetons illimites ». Mesure le 20-09-2026 sur les vraies
      donnees du depot : le tableau affiche cinq lignes, dont quatre fois
      UNIBAIL_RODAMCO au 2026-08-27 a -2 796,25 €, somme de la colonne
      -4 300,25 € ; la synthese juste en dessous annonce « 1 / 3 » et
      « 1292.25 € ». Le projet interdit d additionner les deux comptabilites, et
      le tableau les presente pourtant l une sous l autre sans rien dire.
      ② La synthese decrit UNE strategie, choisie par l ordre du fichier. Elle est
      demandee sans preciser de strategie, et le rangement ne porte que sur la
      date : a egalite de date, la derniere ligne du fichier l emporte. Mesure le
      20-09-2026 sur l historique du depot, qui porte quatre lignes au
      2026-09-17 : la synthese decrit C5E10-OBS-V1, et le meme fichier lu a l
      envers ferait decrire C5E10-QA-V1. Rien sur la page ne nomme la strategie
      dont la synthese parle.
      ③ Une seule valeur illisible fait tomber toute la page. La couleur du
      resultat net est choisie par une conversion en nombre sans filet. Mesure le
      20-09-2026 en remplacant le resultat de la premiere ligne du journal par le
      texte `n.d.` : le programme s arrete sur « ValueError: could not convert
      string to float: 'n.d.' » sur la ligne qui choisit la couleur du
      resultat net ; aucune page n est ecrite, et
      PUBLIER_LE_SITE.py s arrete alors en code 2 avec « aucun cockpit fabrique ».
      La mise en forme du meme montant, juste a cote, est faite par `f_eur`, qui
      rattrape ce cas et rend « n.d. » ; le meme montant est donc converti deux
      fois dans la meme ligne, une fois avec filet et une fois sans.
      ④ La pire chute est cachee quand elle vaut zero, en comparant sa valeur
      ecrite a trois textes : `0.00`, `0` et `n.d.`. Une mesure qui ecrirait
      `0.0` ou `0,00` afficherait donc « 0.0 € » au lieu de « aucune ». Le
      critere porte sur l ecriture du nombre, pas sur sa valeur.
      ⑤ Le tableau ne dit nulle part qu il melange les deux comptabilites, alors
      que le journal porte une colonne d explication qui le precise ligne par
      ligne. Cette colonne n est jamais affichee.
    ⑩ EFFET — LIT des donnees deja en memoire. N ouvre aucun fichier, n ecrit
      rien, ne touche pas au reseau, n affiche rien.
    ⑪ TERMINAISON — Rend la main dans le cas normal. PEUT LEVER sur un resultat
      net illisible, et cette erreur n est rattrapee nulle part : elle arrete le
      programme avant qu aucune page ne soit ecrite. Aucun de ses appels ne se
      termine.
      [sort: non]
    ⑫ DEFINITIONS
      l historique des mesures : donnees/historique_mesures.csv, une ligne par
        jour, par strategie et par comptabilite, jamais reecrit.
      la pire chute : la plus forte baisse du cumul depuis un sommet
        precedent.
      le service MESURER LA PERFORMANCE : programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py,
        le seul programme autorise a calculer les indicateurs de performance.
      une comptabilite : la facon de compter les resultats, et il y en a deux,
        jamais additionnees — un jeton, une seule position a la fois avec 100
        000 € simules, et jetons illimites, toutes les occurrences du signal
        mesurees.
    
      le projet : le dossier reçu sur la ligne de commande, celui que le radar examine
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    lignes = []
    # CHAQUE LIGNE DIT SA STRATEGIE ET SA COMPTABILITE (defaut 3 de A-491, 27-09-2026).
    # Avant, le tableau affichait quatre fois UNIBAIL_RODAMCO au 27-08 a -2 796,25 EUR
    # sans dire que c etaient deux strategies fois deux comptabilites : un lecteur
    # qui additionnait trouvait -4 300,25 EUR, alors que la synthese annoncait 1 292,25.
    for t in S.trades:
        # sous le titre, en petit et coupable n importe ou : un nom de strategie
        # d un seul tenant elargissait la page a 650 px sur un ecran de 400 px.
        lignes.append([esc(t.get('date_sortie', '')),
                       f'{esc(t.get("valeur", ""))}<div style="font-size:9px;color:{C["mut"]};'
                       f'overflow-wrap:anywhere">{esc(t.get("strategie", ""))} · '
                       f'{esc((t.get("comptabilite") or "NON DITE").replace("_", " "))}</div>',
                       f_eur(t.get('prix_entree'), False), f_eur(t.get('prix_sortie'), False),
                       esc(t.get('motif_sortie', '')),
                       f'<b style="color:{C["grn"] if float(t.get("pnl_net_eur") or 0) > 0 else C["red"]}">'
                       f'{f_eur(t.get("pnl_net_eur"))}</b>'])
    # SYNTHESE : valeurs LUES dans l historique des mesures, jamais recalculees ici (A-208)
    m = derniere_mesure(S.mesures, None, 'un jeton')
    if m:
        synth = tab(['Taux de reussite', 'Serie en cours', 'Pire chute depuis un sommet', 'Cumul net'],
                    [[f'{val(m, "gagnantes")} / {val(m, "n_operations")}',
                      val(m, 'serie_en_cours'),
                      (val(m, 'pire_chute_eur') + ' €') if val(m, 'pire_chute_eur', '0') not in ('0.00', '0', 'n.d.') else 'aucune',
                      f'<b style="color:{C["grn"]}">{val(m, "cumul_net_eur")} €</b>']])
        src = (f'<div style="font-size:9px;color:{C["dim"]};margin-top:6px">Synthese lue dans '
               f'historique_mesures.csv (mesure du {esc(val(m, "date_mesure"))}) — aucun calcul effectue ici.</div>')
    else:
        synth = (f'<div style="font-size:11px;color:{C["gld"]};padding:6px 0">Synthese indisponible : '
                 f'le service MESURER LA PERFORMANCE n a pas encore ecrit de mesure.</div>')
        src = ''
    return tab(['Date', 'Titre · strategie · comptabilite', 'Entree', 'Sortie', 'Motif',
                'Resultat net'], lignes) + synth + src

def bloc_surveillance(S):
    """Compose la section « Surveillance et archives » : les voyants de chaque
    strategie, puis les strategies retirees.

    ① ROLE — Montrer d un coup d oeil si un garde-fou est pres de ceder, pour
      chaque strategie et chaque comptabilite connues de l historique des mesures,
      et rappeler ensuite ce qui a deja ete retire. Trois garde-fous sont
      affiches : le taux de reussite face au point mort, les pertes consecutives
      face a cinq, et la pire chute face a moins vingt pourcents. Tous les
      chiffres sont LUS : la page et le programme de surveillance lisent donc
      exactement les memes.
    ② CONTEXTE D APPEL — Un seul appelant : `construire`, une fois, pour la
      sixieme et derniere des six sections de la page.
    ③ ENTREE — `S` : l objet des sources, deja charge. La section y lit deux
      choses : l historique des mesures et l etat civil des strategies.
    ④ CONDITIONS D ENTREE — Aucune. Un historique vide fait afficher qu aucun
      voyant n est disponible ; un etat civil vide fait afficher zero strategie
      archivee.
    ⑤ SORTIE — UNE valeur : un texte, le fragment de page — le tableau des
      voyants ou son message de repli, puis la phrase qui explique ce qui se passe
      au franchissement d une limite, puis le compte des strategies archivees et
      le tableau des six dernieres.
      [rend: 1]
    ⑥ TRAITEMENT — ① parcourir l historique et relever tous les couples strategie
      et comptabilite rencontres · ② pour chaque couple, chercher sa mesure la
      plus recente · ③ composer une ligne avec le verdict du garde-fou sur le taux
      de reussite, les pertes consecutives sur cinq, et la pire chute sur moins
      vingt pourcents, chacun suivi de son voyant · ④ composer le tableau, ou un
      message si aucune ligne · ⑤ relever dans l etat civil les strategies dont le
      statut ou l etat de vie contient ARCHIV · ⑥ composer le tableau des six
      dernieres, avec leur nom et le debut de leur note · ⑦ assembler.
    ⑦ UNITE — Les pertes consecutives se comptent en OPERATIONS, avec une limite
      de 5. La pire chute est en POURCENTS, avec une limite de moins 20. Le taux
      de reussite et le point mort sont en POURCENTS. Les notes d archive sont
      coupees a 90 CARACTERES.
    ⑧ POURQUOI — La liste des couples a afficher est construite a partir de ce que
      l historique contient reellement, et non a partir d une liste de strategies
      ecrite dans le code. Une strategie ajoutee au systeme apparait donc dans le
      tableau des le premier soir ou elle est mesuree, sans qu on ait a toucher a
      ce programme. Mesure le 20-09-2026 sur les vraies donnees du depot : six
      lignes apparaissent, trois strategies dans deux comptabilites chacune.
      La phrase sur le franchissement d une limite est affichee en toutes lettres
      parce que le systeme ne se modifie jamais lui-meme : il arrete de prendre
      position, il continue de mesurer, et la suite appartient a Jean-Luc.
    ⑨ CE QUI CLOCHE —
      ① Les deux limites affichees, 5 pertes consecutives et moins 20 pourcents de
      chute, sont ecrites dans le texte de la page. Le verdict, lui, est calcule
      ailleurs par le service. Si le service changeait de limite, la page
      continuerait d afficher les anciennes a cote du nouveau voyant, et personne
      ne le verrait. Un chiffre qui existe ailleurs ne se recopie pas (R-708).
      ② Le relevé des strategies archivees porte sur un MORCEAU de mot, `ARCHIV`,
      cherche dans deux colonnes collees l une a l autre. Un etat de vie
      `NON-ARCHIVEE` serait compte comme archive, et une strategie dont le statut
      finit par `ARCH` et dont l etat de vie commence par `IVEE` le serait aussi,
      par simple collage des deux textes. Releve le 20-09-2026 sur les deux lignes qui
      relevent les strategies archivees.
      ③ Le tableau des archives est titre « Cloture, Motif », mais la premiere
      colonne affiche le NOM de la strategie et la seconde le debut de sa note.
      Aucune des deux ne porte une date de cloture ni un motif. Mesure le
      20-09-2026 sur les vraies donnees du depot : la premiere ligne affiche
      « CCI sort <-100 » sous le titre « Cloture ».
      ④ Les notes sont coupees a 90 caracteres sans que rien ne le dise. Mesure le
      20-09-2026 : quatre des six lignes affichees se terminent par « au moment où
      le prix de clôture est co », phrase tranchee en plein mot.
      ⑤ Le premier parcours de l historique range les mesures par date pour rien :
      il ne sert qu a relever des couples, et le rangement n a aucun effet sur un
      ensemble.
      ⑥ Le compte annonce est celui de TOUTES les strategies archivees, mais le
      tableau n en montre que six, et rien ne relie les deux nombres autrement que
      par la phrase « les 6 dernieres ». Mesure le 20-09-2026 : « 30 strategie(s)
      archivee(s) au registre — les 6 dernieres ».
    ⑩ EFFET — LIT des donnees deja en memoire. N ouvre aucun fichier, n ecrit
      rien, ne touche pas au reseau, n affiche rien.
    ⑪ TERMINAISON — Rend la main dans le cas normal. PEUT LEVER si une ligne de
      l historique n a ni colonne `strategie` ni colonne `comptabilite` : le
      rangement des couples comparerait alors une absence a un texte. Le cas ne
      se produit pas sur les donnees du depot du 20-09-2026. Aucun de ses appels
      ne se termine.
      [sort: non]
    ⑫ DEFINITIONS
      l etat civil : donnees/cac40_strategies.csv, qui donne pour chaque
        strategie son objectif, son seuil de perte, son horizon et son etat de
        vie.
      l historique des mesures : donnees/historique_mesures.csv, une ligne par
        jour, par strategie et par comptabilite, jamais reecrit.
      la pire chute : la plus forte baisse du cumul depuis un sommet
        precedent.
      le point mort : le taux de réussite en dessous duquel une stratégie perd de l'argent
      le service MESURER LA PERFORMANCE : programmes/MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py,
        le seul programme autorise a calculer les indicateurs de performance.
      un garde-fou : une limite qui, franchie, fait cesser a la strategie de
        prendre position tout en continuant a la mesurer.
      une comptabilite : la facon de compter les resultats, et il y en a deux,
        jamais additionnees — un jeton, une seule position a la fois avec 100
        000 € simules, et jetons illimites, toutes les occurrences du signal
        mesurees.
    
      CCI : l'indice du canal des matières premières, qui mesure de combien le cours s'écarte de sa moyenne récente ; sans unité, typiquement entre −200 et +200.
      un motif : un morceau de nom passé à une fonction de recherche, par exemple trouve("REGISTRE_REGLES"), au lieu du nom complet du fichier.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    lignes = []
    vus = set()
    for m in sorted(S.mesures, key=lambda x: x.get('date_mesure', '')):
        cle = (m.get('strategie'), m.get('comptabilite'))
        vus.add(cle)
    for (strat, compta) in sorted(vus):
        m = derniere_mesure(S.mesures, strat, compta or 'un jeton')
        if not m:
            continue
        lignes.append([f'{esc(strat)} · {esc(compta)}',
                       f'{esc(val(m, "verdict_c7"))} {voyant(m, "voyant_c7")}',
                       f'{esc(val(m, "pertes_consecutives"))} / 5 {voyant(m, "voyant_pertes")}',
                       f'{esc(val(m, "pire_chute_pct"))} % / −20 % {voyant(m, "voyant_chute")}'])
    if not lignes:
        table = (f'<div style="font-size:11px;color:{C["gld"]};padding:6px 0">Aucun voyant disponible : '
                 f'le service MESURER LA PERFORMANCE n a pas encore ecrit de mesure.</div>')
    else:
        table = tab(['Strategie', 'Taux de reussite vs point mort', 'Pertes consecutives',
                     'Pire chute depuis un sommet'], lignes)

    archivees = [s for s in S.strategies
                 if 'ARCHIV' in (s.get('statut', '') + s.get('etat_vie', '')).upper()]
    arch = tab(['Cloture', 'Motif'],
               [[esc(s.get('nom', '?')), esc((s.get('note', '') or '')[:90])] for s in archivees[-6:]])
    return (table
            + f'<div style="font-size:11px;color:{C["mut"]};margin:6px 0;line-height:1.6">Au franchissement '
              f'd une limite, la strategie cesse automatiquement de prendre position tout en restant mesuree. '
              f'La suite releve de votre decision : rearmement, retour au laboratoire, ou retrait definitif.</div>'
            + f'<div style="font-size:10px;color:{C["dim"]};margin-top:8px">{len(archivees)} strategie(s) '
              f'archivee(s) au registre — les 6 dernieres :</div>' + arch)


def construire(S, horo):
    """Assemble la page complete : en-tete, les six sections, et le pied de page.

    ① ROLE — Donner a la page sa forme definitive et son ordre. Les six sections
      sont composees dans l ordre ou Jean-Luc les lit, et le pied de page porte
      deux choses depliables : le vocabulaire du systeme, et la liste des fichiers
      qui ont servi a produire la page avec leur etat. C est cette derniere liste
      qui permet de savoir, sans ouvrir un fichier, sur quoi la page a ete batie.
    ② CONTEXTE D APPEL — Un seul appelant : `main`, une fois, juste apres le
      chargement des sources et juste avant l ecriture du fichier.
    ③ ENTREE — `S` : l objet des sources, deja charge. `horo` : l horodatage a
      afficher, compose par `main` sous la forme jour de la semaine abrege, date
      et heure de Paris, par exemple `Dim 20-09-2026 00h16`.
    ④ CONDITIONS D ENTREE — Les sources doivent etre deja chargees : cette
      fonction ne lit aucun fichier. L horodatage doit etre pret a etre affiche.
    ⑤ SORTIE — UNE valeur : un texte, la page complete, de la declaration de
      document a la balise de fin. Mesure le 20-09-2026 sur les vraies donnees du
      depot : 25 326 caracteres.
      [rend: 1]
    ⑥ TRAITEMENT — ① composer le tableau de la trace des sources, en marquant en
      dore tout etat qui n est pas LU · ② composer le bloc depliable du
      vocabulaire · ③ composer le bloc depliable des sources lues, suivi d une
      phrase sur l origine des valeurs · ④ composer la declaration de document,
      l entete de page, le titre de l onglet et le reglage d affichage mobile ·
      ⑤ composer l entete visible : la mention de simulation, le titre, l
      horodatage · ⑥ appeler les six sections, chacune dans son cadre, avec son
      sous-titre · ⑦ coller le pied de page et refermer.
    ⑦ UNITE — Les tailles sont en PIXELS. La largeur de la page est plafonnee a
      560 pixels. L horodatage est en heure de Paris.
    ⑧ POURQUOI — La toute premiere ligne visible de la page dit « Simulation
      uniquement — aucun ordre réel ». Elle est posee la, avant le titre, parce
      que la page affiche des positions, des prix d entree et des resultats en
      euros, et qu elle est publiee sur un depot public : un lecteur qui tombe
      dessus doit savoir en une seconde qu aucun ordre n est transmis a un
      courtier.
      La largeur plafonnee a 560 pixels et le reglage d affichage mobile viennent
      du meme besoin : Jean-Luc ouvre cette page sur son telephone.
    ⑨ CE QUI CLOCHE —
      ① La phrase du pied de page promet plus que la page ne tient. Elle annonce
      « aucune valeur écrite en dur », alors que la section Surveillance affiche
      les deux limites des garde-fous en texte : « / 5 » pour les pertes
      consecutives et « / −20 % » pour la pire chute. Mesure le 20-09-2026 sur les
      vraies donnees du depot : les six lignes du tableau de surveillance portent
      ces deux nombres, qui ne viennent d aucun fichier.
      ② Le tableau de la trace colore de la meme facon un fichier ABSENT et un
      fichier ILLISIBLE. Les deux apparaissent en dore, et seul le mot les
      distingue. Un fichier de chiffres de reference que l on n arrive pas a lire
      est pourtant un incident, la ou un fichier absent peut etre un etat normal.
      ③ Le style du corps de page declare deux fois la meme propriete de marge :
      `margin:0` au debut, `margin:auto` a la fin. C est la seconde qui s
      applique, et la premiere ne sert a rien. Releve le 20-09-2026 par lecture de
      la balise de corps de page.
      ④ Le vocabulaire affiche en pied de page est ecrit ici, dans ce programme,
      alors que les memes definitions vivent dans les documents de gouvernance du
      depot. Deux implementations d une meme chose divergent toujours (R-708) : le
      jour ou une definition changera au registre, celle de la page restera.
      ⑤ La page se declare « conforme A-207 V1 » a deux endroits — dans l entete
      visible et dans le pied de page — sans que ce code dise au lecteur ce qu il
      recouvre. A-207 est l action du BACKLOG_DECISIONS.md qui a specifie les six
      sections de cette page, le 14-08-2026.
    ⑩ EFFET — LIT des donnees deja en memoire et appelle les six sections. N ouvre
      aucun fichier, n ecrit rien, ne touche pas au reseau, n affiche rien. La
      page rendue ne charge aucune ressource exterieure.
    ⑪ TERMINAISON — Rend la main dans le cas normal. PEUT LEVER par l un de ses
      appels : `bloc_journal` leve sur un resultat net illisible au journal, et
      `bloc_surveillance` peut lever sur une ligne de mesure sans colonne de
      strategie. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DEFINITIONS
      PRODUCTION : l etat d une strategie dont le seuil d operations est
        atteint et les resultats conformes, donc exploitee.
      QA : l etat d une strategie validee sur l historique mais qui n a pas
        encore realise assez d operations reelles pour etre jugee.
      la pire chute : la plus forte baisse du cumul depuis un sommet
        precedent.
      la trace : la liste des sources avec leur etat — LU, ABSENT ou ILLISIBLE
        — et un detail chiffre, affichee en pied de page.
      le laboratoire : les idees a l etude, qui n engagent aucun argent.
      un garde-fou : une limite qui, franchie, fait cesser a la strategie de
        prendre position tout en continuant a la mesurer.
      une comptabilite : la facon de compter les resultats, et il y en a deux,
        jamais additionnees — un jeton, une seule position a la fois avec 100
        000 € simules, et jetons illimites, toutes les occurrences du signal
        mesurees.
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    trace = tab(['Source', 'État', 'Détail'],
                [[esc(n), ('LU' if e == 'LU' else f'<b style="color:{C["gld"]}">{e}</b>'), esc(d)]
                 for n, e, d in S.trace])
    pied = (det('Vocabulaire',
                '<b>QA</b> : la stratégie est validée sur l\'historique mais n\'a pas encore assez d\'opérations '
                'réelles pour être statistiquement jouable. <b>Production</b> : seuil atteint, résultats conformes, '
                'stratégie exploitée. <b>Laboratoire</b> : idées en cours d\'étude, aucune position engagée. '
                '<b>Un jeton</b> : 100 000 € simulés, une position à la fois — la performance réellement '
                'atteignable. <b>Jetons illimités</b> : toutes les occurrences du signal mesurées, chevauchements '
                'compris — évaluation de la qualité du signal, sans correspondance avec un portefeuille réel. '
                'Ensemble en simulation : aucun ordre n\'est transmis.')
            + det('Sources lues pour produire cette page', trace
                  + '<div style="font-size:10px;margin-top:6px">Page produite automatiquement par '
                    'GENERATEUR_COCKPIT, conforme A-207 V1. Chaque valeur affichée provient d\'un fichier '
                    'ci-dessus ou d\'un calcul sur ces fichiers — aucune valeur écrite en dur.</div>'))
    return (f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>Tableau de bord CAC 40 — {horo}</title></head>'
            f'<body style="margin:0;background:{C["bg"]};color:{C["txt"]};'
            f'font-family:-apple-system,\'Segoe UI\',Roboto,sans-serif;padding:12px;max-width:560px;margin:auto">'
            f'<header style="margin:4px 0 14px">'
            f'<div style="font-size:9px;color:{C["dim"]};text-transform:uppercase;letter-spacing:.15em">'
            f'Simulation uniquement — aucun ordre réel</div>'
            f'<h1 style="margin:3px 0 0;font-size:18px">Tableau de bord</h1>'
            f'<div style="font-size:10px;color:{C["dim"]}">{horo} (Paris) · généré automatiquement · '
            f'conforme A-207 V1</div></header>'
            + sec("Aujourd'hui", bloc1_aujourdhui(S), 'prend-on position ?')
            + sec('QA', bloc_strategie(S, 'QA', 'Aucune stratégie en QA'),
                  'stratégie en phase de validation — comptage des opérations')
            + sec('Production', bloc_strategie(S, 'PRODUCTION', 'Aucune stratégie en service'),
                  'stratégies validées, exploitées')
            + sec('Laboratoire', bloc_laboratoire(S), 'idées à l\'étude')
            + sec('Opérations clôturées', bloc_journal(S), 'le journal')
            + sec('Surveillance et archives', bloc_surveillance(S), 'garde-fous et stratégies retirées')
            + f'<footer style="padding:2px 2px 22px">{pied}</footer></body></html>')

def main():
    """Lit la ligne de commande, fabrique la page, l ecrit, et rend compte en trois
    lignes.

    ① ROLE — Enchainer les trois gestes du programme — charger, composer, ecrire —
      et laisser derriere lui de quoi verifier ce qui vient d etre fait : combien
      de sources ont ete lues et lesquelles manquaient, ce que la page contient,
      et l empreinte du texte ecrit. Ces trois lignes sont ce que
      PUBLIER_LE_SITE.py recopie dans le journal du circuit du soir.
    ② CONTEXTE D APPEL — Le lancement du programme, et lui seul.
    ③ ENTREE — Aucun parametre. Elle lit la ligne de commande : le premier
      argument est le dossier des sources, le second le dossier de sortie, et les
      deux valent le dossier courant quand ils ne sont pas donnes.
      PUBLIER_LE_SITE.py passe deux fois le meme chemin, celui de son dossier
      `_site_travail`.
    ④ CONDITIONS D ENTREE — Le dossier des sources doit exister et pouvoir etre
      parcouru. Le dossier de sortie doit EXISTER : il n est pas cree.
    ⑤ SORTIE — Ne rend rien. Elle laisse derriere elle un fichier HTML sur le
      disque et trois lignes affichees a l ecran.
      [rend: rien]
    ⑥ TRAITEMENT — ① lire les deux chemins sur la ligne de commande · ② prendre l
      heure de Paris, composer l horodatage affiche et le nom du fichier a ecrire ·
      ③ charger les sources · ④ composer la page · ⑤ l ecrire en UTF-8 · ⑥ compter
      les sources lues et afficher les manquantes · ⑦ afficher le nombre d
      operations, de positions, d idees et de lignes de vie · ⑧ afficher le chemin
      ecrit, la taille de la page et son empreinte.
    ⑦ UNITE — La page se compte en CARACTERES. L empreinte est un nombre
      hexadecimal de 16 caracteres. L horodatage et le nom de fichier sont en
      heure de Paris.
    ⑧ POURQUOI — L empreinte de la page est affichee pour que deux passages
      puissent etre compares sans ouvrir les fichiers : deux empreintes
      identiques veulent dire que rien n a bouge. Le compte rendu est volontaire-
      ment court, trois lignes, parce que le detail vit dans la page elle-meme, au
      pied, dans le bloc depliable des sources lues ; et parce que
      PUBLIER_LE_SITE.py n en recopie que les 400 dernieres lettres dans le
      journal du circuit du soir.
    ⑨ CE QUI CLOCHE —
      ① Le nom du fichier commence par le jour de la semaine, et c est ce qui fait
      publier la mauvaise page. PUBLIER_LE_SITE.py choisit la page a publier par
      `sorted(...)[-1]`, donc par ordre alphabetique ; tries, les sept jours
      donnent Dim, Jeu, Lun, Mar, Mer, Sam, Ven, et « Ven » sort toujours dernier.
      Si le dossier de travail contient deux cockpits, celui du vendredi est
      publie meme s il est plus ancien. Le meme programme porte par ailleurs, en
      tete, le rappel que le plus recent se lit dans la date et jamais dans l
      alphabet, corrige le 12-09-2026 pour ses propres lectures — mais le nom
      qu il produit, lui, n a pas change.
      ② Aucun code de sortie n est rendu. Le programme se termine normalement,
      donc en code 0, ou il tombe sur une erreur non rattrapee. Il n existe aucun
      etat intermediaire : une page produite avec sept sources sur dix rend le
      meme code qu une page produite avec dix sur dix. Mesure le 20-09-2026 sur
      les vraies donnees du depot : « sources : 7/10 lues | MANQUANTES :
      registre_candidates.csv, audit_du_jour.md, rapport_boucle_*.md », et le
      programme se termine normalement.
      ③ Le dossier de sortie n est pas cree. Mesure le 20-09-2026 en donnant un
      dossier qui n existe pas : le programme s arrete sur « FileNotFoundError:
      [Errno 2] No such file or directory », apres avoir lu toutes les sources et
      compose toute la page — donc apres tout le travail, et pour rien.
      ④ Deux passages dans la meme minute ecrasent le premier fichier. Le nom ne
      porte que l heure et la minute, et l ecriture ne verifie pas si le nom est
      deja pris.
      ⑤ Le compte rendu ne dit pas l essentiel : que les indicateurs affiches
      viennent d une mesure d un autre jour. Mesure le 20-09-2026 sur les vraies
      donnees du depot : les trois lignes affichees annoncent le nombre de
      sources, le nombre d operations et le chemin ecrit, sans jamais nommer la
      date de la mesure employee, qui est le 2026-09-17 alors que la derniere
      seance lue est le 2026-09-18.
    ⑩ EFFET — ECRIT un fichier HTML dans le dossier de sortie, sous un nom qui
      porte le jour et l heure de Paris, par exemple
      `cockpit_Dim_20-09-2026_00h16.html`. Un fichier de meme nom serait ecrase.
      LIT jusqu a dix fichiers dans le dossier des sources et liste ce dossier
      ainsi que son sous-dossier `claude/`. Affiche trois lignes. AUCUN acces
      reseau.
    ⑪ TERMINAISON — Rend la main, et le programme se termine alors normalement,
      donc en code 0. Elle ne rend aucune valeur et n appelle aucune sortie
      explicite. PEUT LEVER, et l erreur arrete alors le programme sans qu aucune
      page ne soit ecrite : dossier de sortie absent, dossier de sources absent,
      resultat net illisible au journal, fichier tabulaire disparu ou mal encode.
      Et un de ses appels peut ne pas revenir : `_plus_recent` leve deliberement
      quand la fonction `le_plus_recent` de programmes/COMMUN.py n a pas pu etre
      importee, plutot que de choisir un fichier par ordre alphabetique.
      [sort: non]
    ⑫ DEFINITIONS
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
      le cockpit : la page web que ce programme fabrique et que Jean-Luc ouvre
        pour voir l etat du systeme.
      une ligne de vie : une ligne de donnees/cac40_strategies.csv, qui donne
        l etat civil d une strategie a une date.
      une seance : une journee de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa cloture et son volume
    """
    base = sys.argv[1] if len(sys.argv) > 1 else '.'
    sortie = sys.argv[2] if len(sys.argv) > 2 else '.'
    now = datetime.now(PARIS)
    horo = f"{JOURS[now.weekday()]} {now.strftime('%d-%m-%Y %Hh%M')}"
    nom = f"cockpit_{JOURS[now.weekday()]}_{now.strftime('%d-%m-%Y_%Hh%M')}.html"

    S = Sources(base).charger()
    html = construire(S, horo)
    chemin = os.path.join(sortie, nom)
    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(html)

    # compte rendu court (3 lignes), le detail vit dans la page
    lus = sum(1 for _, e, _ in S.trace if e == 'LU')
    print(f"sources : {lus}/{len(S.trace)} lues" +
          (f" | MANQUANTES : {', '.join(n for n, e, _ in S.trace if e != 'LU')}" if lus < len(S.trace) else ""))
    print(f"contenu : {len(S.trades)} opération(s) au journal · {len(S.positions)} position(s) ouverte(s) · "
          f"{len(S.candidates)} idée(s) · {len(S.strategies)} ligne(s) de vie")
    print(f"écrit   : {chemin} ({len(html)} caractères, "
          f"sha256 {hashlib.sha256(html.encode()).hexdigest()[:16]})")

if __name__ == '__main__':
    main()
