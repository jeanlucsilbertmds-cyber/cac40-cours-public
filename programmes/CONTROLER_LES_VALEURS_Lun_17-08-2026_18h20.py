#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compare les valeurs ecrites par la collecte du soir a celles attendues, et crie ce qui manque.

CONTROLE DES VALEURS ATTENDUES — application de la regle I-9 du chapitre GESTION
DE L IDENTITE DES VALEURS (REGISTRE, 17-08-2026) : « un mnemonique attendu qui ne
renvoie rien est une ALERTE, jamais un silence ».

USAGE : python3 CONTROLER_LES_VALEURS_Lun_17-08-2026_18h20.py [dossier]
  lit  REFERENTIEL_VALEURS*.csv, cours_nouveaux*.csv et cac40_strategies*.csv
  ecrit : RIEN. Il affiche un rapport et rend un code de sortie.
CODE DE SORTIE : 0 = aucune alerte · 1 = au moins une alerte, ou fichier
indispensable introuvable.

① ROLE — **Empecher qu une valeur du CAC 40 sorte des donnees en silence.** Tout
  le reste du systeme calcule sur les lignes PRESENTES : aucun autre programme ne
  sait dire qu une ligne ATTENDUE n a jamais ete ecrite. Si le code d une valeur
  cessait de fonctionner chez le fournisseur de cours, la collecte ecrirait les
  autres valeurs et se tairait ; la valeur disparaitrait de l historique sans que
  rien ne l affiche. Ce programme est le seul endroit qui compare CE QUI EST ECRIT
  a CE QUI EST ATTENDU.
② CONTEXTE D APPEL — Le circuit du soir, apres la collecte des cours : il ne peut
  rien dire tant que les cours du jour ne sont pas ecrits. **Aucun autre programme
  du depot ne le nomme** : recherche du texte « CONTROLER_LES_VALEURS » dans les
  34 fichiers de `programmes/`, le 19-09-2026 — une seule occurrence, dans ce
  fichier meme. **Le rang exact de son pas dans le circuit n a pas pu etre
  etabli** : le fichier qui decrit le circuit n etait pas disponible au moment ou
  ce texte a ete ecrit.
③ ENTREE — La ligne de commande, UN argument facultatif : le dossier ou chercher
  les fichiers ; sans lui, le dossier courant. **Et TROIS FICHIERS, trouves par un
  morceau de leur nom** : `REFERENTIEL_VALEURS` — ce qui est attendu ·
  `cours_nouveaux` — ce que la collecte a reellement ecrit · `cac40_strategies` —
  les univers a verifier.
④ CONDITIONS D ENTREE — Le referentiel et le fichier des cours doivent exister,
  sinon le programme s arrete sans rien controler. Le referentiel doit porter les
  colonnes `nom_usuel`, `mnemonique`, `onglet_google` et `hors_univers` ; le
  fichier des cours, les colonnes `valeur` et `date` ; le registre des strategies,
  les colonnes `id`, `etat_vie` et `univers`. **Le registre des strategies peut
  manquer : le troisieme controle est alors saute et le programme continue.**
⑤ SORTIE — **Un code de sortie et un rapport affiche a l ecran. Aucun fichier
  ecrit.**
⑥ TRAITEMENT — ① lire le referentiel et ranger chaque valeur en ATTENDUE ou en
  HORS UNIVERS · ② lire les cours ecrits et relever la derniere seance · ③ premier
  controle : une valeur presente a la seance precedente et absente a la derniere ·
  ④ deuxieme controle : une valeur des cours inconnue du referentiel · ⑤ troisieme
  controle : les mnemoniques inscrits dans les univers de strategies · ⑥ afficher
  les informations, puis les alertes, et rendre le code de sortie.
⑦ UNITE — **Des NOMBRES DE VALEURS et des NOMBRES DE MNEMONIQUES ECRITS.** Les
  dates sont des dates de seance, reprises telles quelles du fichier des cours.
  Aucun prix, aucun euro, aucun volume : ce programme ne lit que des noms, des
  codes et des dates.
⑧ POURQUOI — **LA CLE EST LE MNEMONIQUE, JAMAIS LE NOM**, parce qu un meme nom s
  ecrit differemment selon le fichier : la collecte du soir ecrit
  `BUREAU_VERITAS` la ou le referentiel porte `BUREAU VERITAS`. Compares tels
  quels, ce sont deux societes distinctes, et le controle accuserait chaque soir
  une valeur parfaitement presente.
  **ET L EXCLUSION D UNE VALEUR VIT DANS LA DONNEE, JAMAIS DANS LE CODE** : la
  colonne `hors_univers` du referentiel porte le motif de l exclusion. Si
  ARCELORMITTAL revient dans l univers, la colonne s efface et ce programme suit,
  sans qu une ligne de code change. Le texte d origine du programme rapporte l
  inverse, en dur dans le code, avant le 13-09-2026 : la valeur etait ecartee par
  un test sur le debut de son nom, puis le programme s alarmait de son absence et
  de son inconnaissance — trois phrases contradictoires sur la meme valeur, dans
  le meme ecran, toutes fabriquees par l exclusion elle-meme.
⑨ CE QUI CLOCHE — **La ligne d usage d origine nommait un fichier qui n existe
  pas.** Elle annoncait `python3 controle_valeurs.py [dossier]` ; le fichier s
  appelle `CONTROLER_LES_VALEURS_Lun_17-08-2026_18h20.py`. Recherche d un fichier
  nomme `controle_valeurs.py` dans `programmes/`, le 19-09-2026 : aucun. Qui
  recopiait cette ligne obtenait « No such file or directory ». Le texte d usage
  de ce module porte desormais le vrai nom du fichier : la correction est dans le
  texte, pas dans le code.
  **Et le programme ne se confronte a aucun contrat de fichier.** Les colonnes
  partagees entre programmes sont declarees une seule fois dans
  `programmes/CONTRATS_DES_FICHIERS.py` ; recherche du texte « CONTRATS » dans ce
  fichier, le 19-09-2026 : zero occurrence. Il lit `r['valeur']` et `r['date']`
  entre crochets. Mesure du 19-09-2026 : avec un fichier de cours dont la colonne
  `date` est renommee `seance`, le programme s arrete sur `KeyError: 'date'` sur
  l instruction qui releve les dates des cours, et rend le code 1 — le meme code que « une alerte a ete levee ». Un
  circuit qui lit ce code ne peut pas distinguer un controle qui a trouve quelque
  chose d un controle qui n a pas pu tourner.
⑩ EFFET — **N ECRIT AUCUN FICHIER, ne sort pas sur le reseau, ne corrige rien.**
  Il lit trois fichiers, affiche un rapport, rend un code de sortie. Il constate.
⑪ TERMINAISON — **NE S ARRETE PAS DE LUI-MEME EN COURS DE ROUTE** : `main` rend
  un entier, et la derniere ligne du fichier passe cet entier a `sys.exit`. Deux
  codes seulement : `0` aucune alerte · `1` au moins une alerte, OU referentiel
  introuvable, OU fichier des cours introuvable. **Aucun de ses appels ne se
  termine de lui-meme.**
⑫ DEFINITIONS
  le referentiel : le fichier qui donne l identite de chaque valeur — son nom
    usuel, son mnemonique, sa place de cotation, et le motif de son exclusion
  un mnemonique : le code court d une valeur, de 1 a 5 caracteres — `TTE` pour
    TOTALENERGIES, `VIE` pour VEOLIA
  hors univers : une valeur que Jean-Luc a volontairement retiree du champ, avec
    son motif ecrit dans la colonne `hors_univers` du referentiel
  l univers d une strategie : la liste des mnemoniques sur lesquels elle a le
    droit d acheter
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
  le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
  le fichier des cours : le fichier où les séances s'empilent sans jamais être réécrites ; au dépôt, c'est donnees/claude_cours_nouveaux.csv.
  le registre : gouvernance/REGISTRE_REGLES.md, le document qui porte les regles numerotees du projet ; une regle absente du registre n'existe pas
"""
import csv, os, sys
from datetime import datetime
from zoneinfo import ZoneInfo

def norm(s):
    """Rend une cle de comparaison : majuscules, sans espaces ni ponctuation.

    ① ROLE — **Permettre de reconnaitre le meme nom ecrit de deux facons.** C est
      la seule fonction de rapprochement du programme : tout ce qui est compare
      passe par elle, des deux cotes de la comparaison.
    ② CONTEXTE D APPEL — `main`, a chaque ligne lue du referentiel, du fichier des
      cours et de chaque univers de strategie.
    ③ ENTREE — `s` : ce qu il faut normaliser — un nom de valeur, un mnemonique ou
      un nom d onglet. **Les appelants lui passent des cases de fichier CSV, deja
      remplacees par une chaine vide quand elles sont absentes.**
    ④ CONDITIONS D ENTREE — Aucune : `str(s)` accepte n importe quoi.
    ⑤ SORTIE — **UNE valeur : une chaine en majuscules ne portant que des lettres
      et des chiffres.** Une chaine vide en entree rend une chaine vide.
      [rend: 1]
    ⑥ TRAITEMENT — ① passer en texte · ② passer en majuscules · ③ ne garder que les
      caracteres alphanumeriques · ④ recoller le tout.
    ⑦ UNITE — —
    ⑧ POURQUOI — Les fichiers de cours portent des NOMS, pas des mnemoniques, et
      les separateurs different d un fichier a l autre. Mesure du 19-09-2026 :
      `norm('BUREAU VERITAS')` et `norm('BUREAU_VERITAS')` rendent tous deux
      `BUREAUVERITAS`, donc la ligne du referentiel et la ligne des cours se
      rapprochent. Sans cela, BUREAU VERITAS serait declaree inconnue du
      referentiel chaque soir. Le texte d origine de cette fonction annonce que la
      correction de fond — porter le mnemonique dans les fichiers de cours — est
      prevue au chapitre I-4 du REGISTRE ; ce document n etait pas disponible pour
      le verifier.
    ⑨ CE QUI CLOCHE — **Deux valeurs differentes peuvent rendre la meme cle, et la
      seconde efface la premiere sans un mot.** Mesure du 19-09-2026 :
      `norm('TOTAL ENERGIES')` et `norm('TOTALENERGIES')` rendent tous deux
      `TOTALENERGIES`. Avec un referentiel de DEUX lignes portant ces deux
      ecritures, le programme a affiche « referentiel lu : 1 valeurs attendues » et
      « aucune alerte » : une des deux valeurs n etait plus attendue du tout, et
      rien ne le disait.
      **Et `norm(None)` rend la chaine `NONE`**, mesure le meme jour — une case
      absente deviendrait une valeur nommee NONE au lieu d une case vide. Aucun
      appel d aujourd hui ne lui passe `None` : `main` remplace chaque case absente
      par une chaine vide avant d appeler. Le piege dort, il n est pas arme.
    ⑩ EFFET — Ne modifie rien : ni fichier, ni reseau, ni valeur exterieure.
    ⑪ TERMINAISON — **Rend toujours la main.** Aucun de ses appels ne se termine.
      [sort: non]
    """
    return ''.join(c for c in str(s).upper() if c.isalnum())

def _mn_hors(v):
    """Rend le mnemonique d une entree hors univers, quel que soit son format.

    ① ROLE — **Donner le mnemonique d une valeur volontairement ecartee**, pour que
      le troisieme controle puisse dire « ce mnemonique est au referentiel mais en
      a ete ecarte » plutot que « ce mnemonique est inconnu ». Les deux se
      reparent autrement : une coquille se corrige dans la fiche de la strategie,
      une exclusion se rediscute avec Jean-Luc.
    ② CONTEXTE D APPEL — `main`, une seule fois, dans le troisieme controle, au
      moment de construire la table des mnemoniques ecartes. **Un seul appelant.**
    ③ ENTREE — `v` : une entree de la table des valeurs hors univers. **L appelant
      lui passe un triplet (nom usuel, motif de l exclusion, mnemonique), construit
      a la lecture du referentiel.**
    ④ CONDITIONS D ENTREE — Une sequence indexable. **Elle n exige pas une longueur
      de trois : elle la verifie.**
    ⑤ SORTIE — **UNE valeur : le troisieme element s il existe, sinon la chaine
      vide.**
      [rend: 1]
    ⑥ TRAITEMENT — ① mesurer la longueur · ② rendre le troisieme element, ou une
      chaine vide.
    ⑦ UNITE — —
    ⑧ POURQUOI — La garde de longueur evite qu une entree plus courte arrete le
      programme sur une erreur d index au milieu du controle. Elle rend alors une
      chaine vide, que l appelant ecarte de lui-meme avec son test `if m`.
    ⑨ CE QUI CLOCHE — **La garde ne peut jamais servir aujourd hui.** La table des
      valeurs hors univers est remplie a UN SEUL endroit du programme — recherche
      du texte `hors_univers[` dans le fichier, le 19-09-2026 : une occurrence — et
      cet endroit ecrit toujours un triplet. La branche qui rend la chaine vide n
      est donc jamais prise, et rien ne la met a l epreuve.
      **Et si elle l etait, elle se tairait** : mesure du 19-09-2026,
      `_mn_hors(('A','B'))` rend une chaine vide ; l appelant la jette avec `if m`,
      et la valeur sort du controle sans qu aucune ligne ne l annonce. Une entree
      mal formee passerait pour une valeur sans mnemonique.
    ⑩ EFFET — Ne modifie rien : ni fichier, ni reseau, ni valeur exterieure.
    ⑪ TERMINAISON — **Rend toujours la main.** Aucun de ses appels ne se termine.
      [sort: non]
    """
    return v[2] if len(v) > 2 else ""


def _p(base, motif):
    """Cherche un fichier par un morceau de son nom, a plat puis dans l arborescence.

    ① ROLE — **Trouver les trois fichiers de travail ou qu ils soient**, pour que
      le programme fonctionne aussi bien la ou les fichiers sont a la racine qu au
      depot, ou ils vivent dans le dossier `donnees/`.
    ② CONTEXTE D APPEL — `main`, trois fois : pour le referentiel, pour le fichier
      des cours, puis pour le registre des strategies.
    ③ ENTREE — `base` : le dossier ou chercher — l argument de la ligne de commande,
      ou le dossier courant · `motif` : le morceau de nom cherche. **Les trois
      valeurs reellement passees sont `REFERENTIEL_VALEURS`, `cours_nouveaux` et
      `cac40_strategies`.**
    ④ CONDITIONS D ENTREE — `base` doit etre un dossier lisible : sinon la lecture
      du dossier arrete le programme sur une erreur de langage, sans message propre.
    ⑤ SORTIE — **UNE valeur : le chemin du premier fichier dont le nom contient le
      motif, ou `None` si aucun ne le contient.**
      [rend: 1]
    ⑥ TRAITEMENT — ① lire les noms presents a la racine, en ordre alphabetique, et
      rendre le premier qui porte le motif · ② sinon descendre dans l arborescence,
      en sautant `archives`, `.git`, `__pycache__` et `_site_travail` · ③ rendre le
      premier trouve · ④ sinon ne rien rendre.
    ⑦ UNITE — —
    ⑧ POURQUOI — **Les dossiers sautes portent des fichiers qui ressemblent aux
      bons.** `archives/` garde les versions tombees : sans ce saut, un referentiel
      retire pourrait etre lu a la place du courant, et le controle dirait manquant
      ce qui a ete ajoute depuis.
      Le texte d origine de la fonction rapporte que la recherche a plat seule est
      le meme defaut, survenu cinq fois avant le 13-09-2026 — sur le radar, la
      mesure, le teneur de positions, le pilote et le registre des experiences : le
      programme s arretait proprement sur « referentiel introuvable » alors que le
      fichier existait, un dossier plus bas.
    ⑨ CE QUI CLOCHE — **Elle prend le PREMIER par ordre alphabetique, pas le plus
      recent.** Les referentiels portent un nom date qui commence par le jour de la
      semaine. Mesure du 19-09-2026, deux fichiers cote a cote dans `donnees/` :
      `REFERENTIEL_VALEURS_Lun_17-08-2026.csv`, qui porte 1 valeur, et
      `REFERENTIEL_VALEURS_Sam_13-09-2026.csv`, qui en porte 3. Le programme a
      affiche « referentiel lu : 1 valeurs attendues
      (REFERENTIEL_VALEURS_Lun_17-08-2026.csv) » : il a pris le plus ANCIEN, parce
      que « Lun » vient avant « Sam » dans l alphabet. Les deux valeurs ajoutees
      depuis n etaient plus attendues par personne.
      **Le depot porte deja la fonction qui tranche par la date** : `le_plus_recent`
      dans `programmes/COMMUN.py`, que la collecte des cours emploie sur ce meme
      referentiel depuis le 12-09-2026. Deux implementations d une meme chose
      divergent toujours (R-708).
      **Et la correspondance porte sur un MORCEAU de nom, sans exiger `.csv`.**
      Mesure du 19-09-2026 : avec `cours_nouveaux.csv` et
      `ARCHIVE_cours_nouveaux.csv` dans le meme dossier, le programme a lu le
      second et annonce « derniere seance ecrite : 2026-01-05 » au lieu du 18-09 —
      une majuscule vient avant une minuscule dans l alphabet des caracteres.
    ⑩ EFFET — **Lit le contenu des dossiers**, y compris en descendant dans l
      arborescence. Ne modifie rien.
    ⑪ TERMINAISON — **Rend toujours la main**, avec un chemin ou `None`. Aucun de
      ses appels ne se termine.
      [sort: non]
    """
    for f in sorted(os.listdir(base)):
        if motif in f:
            return os.path.join(base, f)
    for r, sd, fs in os.walk(base):
        sd[:] = [x for x in sd if x not in ("archives", ".git", "__pycache__", "_site_travail")]
        for f in sorted(fs):
            if motif in f:
                return os.path.join(r, f)
    return None

def main():
    """Conduit les trois controles, affiche le rapport et rend le code de sortie.

    ① ROLE — **Rendre le verdict du soir sur l identite des valeurs.** C est le seul
      endroit du programme qui lit des fichiers, qui decide ce qui est une alerte et
      ce qui n est qu une information, et qui fixe le code de sortie.
    ② CONTEXTE D APPEL — Le lancement du programme, et lui seul : la derniere ligne
      du fichier l appelle et passe ce qu elle rend a `sys.exit`.
    ③ ENTREE — **Aucun parametre.** Elle lit la ligne de commande — un dossier
      facultatif, le dossier courant sinon — puis trois fichiers cherches par un
      morceau de leur nom : `REFERENTIEL_VALEURS`, `cours_nouveaux` et
      `cac40_strategies`.
    ④ CONDITIONS D ENTREE — Le referentiel et le fichier des cours doivent exister
      et porter leurs colonnes : `nom_usuel`, `mnemonique`, `onglet_google` et
      `hors_univers` pour le premier, `valeur` et `date` pour le second. Le registre
      des strategies est facultatif. **Le referentiel doit etre lu en `utf-8-sig`.**
    ⑤ SORTIE — **UNE valeur, un entier : `0` aucune alerte · `1` au moins une
      alerte, ou un fichier indispensable introuvable.** Et un rapport affiche a l
      ecran, informations d abord, alertes ensuite.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire le referentiel et ranger chaque ligne en ATTENDUE — sous
      sa cle de nom normalisee, et aussi sous son nom d onglet — ou en HORS UNIVERS
      quand la colonne `hors_univers` est remplie · ② lire le fichier des cours et
      relever la derniere date ecrite · ③ premier controle : les valeurs presentes a
      l avant-derniere date et absentes a la derniere · ④ deuxieme controle : les
      valeurs des cours qui ne sont ni attendues ni hors univers · ⑤ troisieme
      controle, pour chaque fiche de strategie portant un univers ou en QA ou en
      PRODUCTION : ecarter les univers non renseignes, signaler les mnemoniques
      ecrits deux fois, l univers vide sur une strategie jouee, les mnemoniques
      inconnus du referentiel et les mnemoniques hors univers · ⑥ afficher l
      horodatage, les informations, puis les alertes.
    ⑦ UNITE — Des NOMBRES DE VALEURS et des NOMBRES DE MNEMONIQUES ECRITS. L
      horodatage affiche est une heure de Paris. **Les dates sont comparees comme du
      TEXTE, pas comme des dates** : le classement des seances est le classement
      alphabetique des chaines.
    ⑧ POURQUOI — **Le referentiel est lu en `utf-8-sig` et non en `utf-8`.** Il
      porte un marqueur d ordre d octets invisible en tete. Lu en `utf-8`, sa
      premiere colonne ne s appelle plus `nom_usuel` mais ce marqueur suivi de
      `nom_usuel`, la
      lecture du nom rend une valeur vide pour TOUTES les lignes, et le programme ne
      connait plus aucun nom. Le texte d origine rapporte qu il a crie « VALEUR
      INCONNUE DU REFERENTIEL » sur huit valeurs du CAC 40 parfaitement presentes,
      le 13-09-2026 : un caractere invisible, et un controle qui accuse a tort.
      **Les mnemoniques inconnus et les mnemoniques hors univers font DEUX alertes
      distinctes**, parce qu ils appellent deux gestes opposes : un mnemonique
      absent du referentiel est une coquille, et c est la fiche de la strategie
      qu il faut corriger ; un mnemonique ecarte volontairement est une decision, et
      c est la decision qu il faut revoir. Un lecteur qui suit le mauvais motif
      corrige la mauvaise chose.
      **Le denominateur du troisieme controle compte les jetons ECRITS, pas les
      distincts**, pour qu un mnemonique inscrit deux fois laisse une trace au lieu
      de disparaitre dans un ensemble.
    ⑨ CE QUI CLOCHE — **Le premier controle ne controle pas ce que le programme
      annonce.** Il compare la derniere seance a la PRECEDENTE, pas au referentiel :
      une valeur attendue qui n a jamais ete collectee n est jamais vue. Mesure du
      19-09-2026 : avec un referentiel de trois valeurs dont SANOFI, et un fichier
      de cours ou SANOFI n apparait sur aucune des deux seances, le programme a
      affiche « controle 1 : aucune valeur disparue » et « aucune alerte », code de
      sortie 0. La regle I-9 qu il cite demande l inverse : un mnemonique attendu
      qui ne renvoie rien est une alerte.
      **Le code de sortie 1 porte trois causes.** Recherche de `return 1` dans le
      fichier, le 19-09-2026 : trois occurrences — referentiel introuvable, fichier
      des cours introuvable, et alertes levees. Mesure du 19-09-2026 : dans un
      dossier vide, le programme affiche « ARRET : referentiel introuvable » et rend
      1, exactement comme un soir a deux alertes. Un circuit qui lit ce code ne sait
      pas si le controle a trouve quelque chose ou s il n a pas pu tourner.
      **Le compte affiche par le deuxieme controle ne mesure pas ce que le controle
      a examine.** Le controle parcourt TOUTES les lignes du fichier des cours,
      toutes dates confondues ; la ligne affichee annonce le nombre de valeurs de la
      DERNIERE seance seulement. Mesure du 19-09-2026 : avec un fichier de cours
      portant quatre valeurs distinctes sur deux seances et trois a la derniere, le
      programme a ecrit « controle 2 : les 3 valeurs des cours existent toutes au
      referentiel » alors qu il en avait verifie quatre.
      **Un fichier de cours vide rend une phrase verte.** Mesure du 19-09-2026 :
      avec un fichier ne portant que sa ligne d en-tete, le programme affiche
      « controle 2 : les 0 valeurs des cours existent toutes au referentiel ». L
      alerte « le fichier des cours du jour est VIDE » est bien levee a cote, mais
      la ligne du deuxieme controle affirme un resultat sur rien.
      **Deux lignes du referentiel qui se ressemblent n en font plus qu une, en
      silence.** Mesure du 19-09-2026 : un referentiel portant `TOTAL ENERGIES` et
      `TOTALENERGIES` sur deux lignes a fait afficher « referentiel lu : 1 valeurs
      attendues » et « aucune alerte ». La seconde ligne a ecrase la premiere dans
      la table des attendues.
      **Le rapport du troisieme controle peut annoncer un manque qui n existe pas.**
      Le numerateur compte des valeurs distinctes du referentiel, le denominateur
      des jetons ecrits. Mesure du 19-09-2026, sur l univers `TTE,ENGI,VIE,VIE` dont
      les trois mnemoniques distincts sont tous au referentiel : le programme a
      affiche « 3/4 mnemonique(s) de son univers reconnu(s) ». Le doublon est bien
      signale par ailleurs, mais le rapport laisse croire qu une valeur sur quatre
      manque.
      **Le nom affiche pour une valeur disparue inconnue est la cle normalisee.**
      Mesure du 19-09-2026 : une valeur ecrite `INCONNUE_XY` dans les cours et
      absente du referentiel est annoncee « VALEUR DISPARUE : INCONNUEXY (?) » — le
      separateur a disparu, et le nom affiche ne se retrouve tel quel dans aucun
      fichier.
      **Le classement des seances repose sur le format de la date.** Il est juste
      tant que les dates s ecrivent AAAA-MM-JJ, ce que la collecte du soir declare
      ecrire ; avec un format ou le jour vient en premier, « derniere seance » ne
      designerait plus la plus recente, et les deux premiers controles porteraient
      sur les mauvaises lignes sans rien afficher d anormal.
    ⑩ EFFET — **N ECRIT AUCUN FICHIER et ne sort pas sur le reseau.** Elle ouvre
      trois fichiers en lecture et affiche un rapport. Elle ne corrige rien : ni le
      referentiel, ni les cours, ni les fiches de strategies.
    ⑪ TERMINAISON — **REND TOUJOURS LA MAIN**, par trois chemins : `return 1` quand
      le referentiel manque, `return 1` quand le fichier des cours manque, et une
      derniere sortie qui vaut 1 s il y a des alertes et 0 sinon. **Aucun de ses
      appels ne se termine de lui-meme** : `norm`, `_mn_hors` et `_p` rendent
      toujours la main. **Elle peut en revanche s arreter sur une erreur de langage
      si une colonne attendue manque** : mesure du 19-09-2026, une colonne `date`
      renommee `seance` arrete le programme sur `KeyError: 'date'`, sur l instruction
      qui releve les dates des cours, avec le code de sortie 1.
      [sort: non]
    ⑫ DEFINITIONS
      un jeton : la comptabilité où une seule position peut être ouverte à la fois par stratégie ; un signal reçu pendant une position est ignoré.
      l etat de vie d une strategie : LABO, QA ou PRODUCTION ; une strategie en QA
        ou en PRODUCTION est jouee, une strategie en LABO ne l est pas
      une fiche de strategie : une ligne du registre des strategies, qui porte son
        identifiant, son etat de vie et son univers
    
      hors univers : une valeur que Jean-Luc a volontairement retiree du champ, avec son motif ecrit dans la colonne `hors_univers` du referentiel
      la fiche : la ligne d'une stratégie au registre des stratégies `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte acceptée, son horizon et son univers
      la table : `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740, qui porte les neuf seuils et le sens de comparaison de chacun
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
      le fichier des cours : le fichier où les séances s'empilent sans jamais être réécrites ; au dépôt, c'est donnees/claude_cours_nouveaux.csv.
      le referentiel : le fichier qui donne l identite de chaque valeur — son nom usuel, son mnemonique, sa place de cotation, et le motif de son exclusion
      le registre : gouvernance/REGISTRE_REGLES.md, le document qui porte les regles numerotees du projet ; une regle absente du registre n'existe pas
      un mnemonique : le code court d une valeur, de 1 a 5 caracteres — `TTE` pour TOTALENERGIES, `VIE` pour VEOLIA
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle a tourné — rapport de boucle, rapport d'audit, cockpit, historique des mesures.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    base = sys.argv[1] if len(sys.argv) > 1 else '.'
    now = datetime.now(ZoneInfo('Europe/Paris'))
    alertes, infos = [], []

    # --- le referentiel : la liste de ce qui est ATTENDU
    ch = _p(base, 'REFERENTIEL_VALEURS')
    if not ch:
        print("ARRET : referentiel introuvable — impossible de savoir ce qui est attendu.")
        return 1
    # `utf-8-sig` ET NON `utf-8` — prouve le 13-09-2026.
    # Le referentiel porte un marqueur d ordre d octets invisible. Lu en `utf-8`,
    # sa PREMIERE colonne s appelle '\ufeffnom_usuel' : `r.get('nom_usuel')` rend
    # None pour TOUTES les lignes, et le programme ne connaissait AUCUN nom.
    # Il criait « VALEUR INCONNUE DU REFERENTIEL » sur huit valeurs du CAC 40
    # parfaitement presentes. **Un caractere invisible, et un controle qui accuse
    # a tort — exactement le genre d alerte qui apprend a ne plus regarder.**
    ref = list(csv.DictReader(open(ch, encoding='utf-8-sig')))
    _a_renseigner = []   # fiches dont l univers n est pas encore rempli
    attendues = {}   # cle normalisee -> (nom, mnemonique)
    hors_univers = {}  # cle normalisee -> (nom, motif) — volontairement dehors
    for r in ref:
        nom = (r.get('nom_usuel') or '').strip()
        mn = (r.get('mnemonique') or '').strip()
        og = (r.get('onglet_google') or '').strip()
        # L EXCLUSION D ARCELORMITTAL EST RETIREE — CC1/CC2 de Cowork, 13-09-2026.
        # Le programme EXCLUAIT cette valeur, puis S ALARMAIT de son absence :
        #   « je ne l attends pas » · « elle a disparu » · « elle m est inconnue »
        # — trois phrases contradictoires sur la meme valeur, dans le meme ecran.
        # **Les deux alertes etaient fabriquees par l exclusion elle-meme**, et
        # « 39 valeurs attendues » etait faux : il y en a 40, moins celle sautee.
        #
        # ET LE COMMENTAIRE CITAIT A-235 COMME SI ELLE L AUTORISAIT. A-235 dit :
        #   « ARCELORMITTAL EST ABSENTE DE NOS DONNEES — cause inconnue, A DETECTER
        #    ET RESOUDRE » · et la reponse de Jean-Luc du 17/08 : « je n ai bien sur
        #    pas exclu cette valeur — il y a un probleme quelque part ».
        # **Une action qui demande de RESOUDRE une anomalie a ete lue comme une
        # permission de la MASQUER.**
        # Et la premisse est perimee : « absente » etait vrai sous Google ; ABC la
        # ramene depuis le 09-09. L anomalie s est resolue seule, l exclusion est
        # restee — et c est elle qui faisait crier le controle.
        # A-408 : si je renomme ArcelorMittal, mon controle change-t-il d avis ?
        # `nom.startswith('ARCELOR')` repondait oui. Il epelait.
        # HORS UNIVERS : la colonne du referentiel fait foi — A-410, 13-09-2026.
        # Une valeur hors univers n est pas ATTENDUE : ne pas la voir n est pas
        # une anomalie. **Le motif vit dans la donnee, pas dans le code** — si
        # Jean-Luc rentre ARCELORMITTAL dans l univers, il efface la colonne et
        # les deux programmes suivent, sans qu on touche a une ligne de code.
        if (r.get('hors_univers') or '').strip():
            # ON LA RETIENT AU LIEU DE L OUBLIER — sinon on refait la faute exacte
            # que Cowork a denoncee ce matin : une valeur retiree des ATTENDUES
            # redevient « inconnue du referentiel » et « disparue », et le
            # programme s alarme de ce qu il a lui-meme ecarte.
            # **Je l ai reproduite en une heure, sur la meme valeur.**
            hors_univers[norm(nom)] = (nom, (r.get('hors_univers') or '').strip(), mn)
            continue
        if not mn:
            continue
        attendues[norm(nom)] = (nom, mn)
        if og:
            attendues[norm(og)] = (nom, mn)
    noms_ref = {v for v in attendues.values()}
    infos.append(f"referentiel lu : {len(noms_ref)} valeurs attendues ({os.path.basename(ch)})")

    # --- les cours reellement ecrits
    ch = _p(base, 'cours_nouveaux')
    if not ch:
        print("ARRET : fichier des cours du jour introuvable.")
        return 1
    cours = list(csv.DictReader(open(ch, encoding='utf-8')))
    if not cours:
        alertes.append("le fichier des cours du jour est VIDE")
        cours = []
    dates = sorted({r['date'] for r in cours})
    derniere = dates[-1] if dates else None
    presentes = {norm(r['valeur']) for r in cours if r['date'] == derniere}
    infos.append(f"derniere seance ecrite : {derniere} · {len(presentes)} valeur(s)")

    # --- CONTROLE 1 : une valeur attendue qui ne renvoie rien
    # NOTE : la boucle ne collecte aujourd'hui que l'univers de la strategie
    # vivante, pas les 39 valeurs. On controle donc contre l'univers reellement
    # collecte a la seance PRECEDENTE : une valeur qui etait la hier et qui
    # disparait aujourd'hui est l'anomalie a attraper.
    if len(dates) >= 2:
        veille = {norm(r['valeur']) for r in cours if r['date'] == dates[-2]}
        disparues = {d for d in (veille - presentes) if d not in hors_univers}
        for d in sorted(disparues):
            nom = attendues.get(d, (d, '?'))
            alertes.append(f"VALEUR DISPARUE : {nom[0]} ({nom[1]}) etait presente le {dates[-2]}, absente le {derniere}")
        if not disparues:
            infos.append(f"controle 1 : aucune valeur disparue depuis le {dates[-2]}")
    else:
        infos.append("controle 1 : moins de deux seances, comparaison impossible")

    for k, (nom, motif, _m) in sorted(hors_univers.items()):
        infos.append(f"hors univers, volontairement : {nom} — {motif}")

    # --- CONTROLE 2 : une valeur inconnue du referentiel
    inconnues = {r['valeur'] for r in cours
                 if norm(r['valeur']) not in attendues
                 and norm(r['valeur']) not in hors_univers}
    for v in sorted(inconnues):
        alertes.append(f"VALEUR INCONNUE DU REFERENTIEL : « {v} » presente dans les cours")
    if not inconnues:
        infos.append(f"controle 2 : les {len(presentes)} valeurs des cours existent toutes au referentiel")

    # --- CONTROLE 3 : les univers de strategies
    ch = _p(base, 'cac40_strategies')
    if ch:
        vivantes = [r for r in csv.DictReader(open(ch, encoding='utf-8-sig'))
                    # TOUTE FICHE QUI PORTE UN UNIVERS EST CONTROLEE, quel que soit
                    # son etat de vie. CC2 de Cowork, 13-09-2026 :
                    #   « en passant MA200-S1 en LABO — geste juste par ailleurs — tu as
                    #    retire du champ du controle les 39 mnemoniques que tu venais
                    #    d y ecrire. »
                    # Il l avait signale au tour precedent : « cinq fiches portent un
                    # univers que ce controle ne regarde jamais ». **Il y en avait six,
                    # et la sixieme etait celle que je venais d ecrire a la main.**
                    # Un univers qui n est pas joue peut quand meme porter une coquille,
                    # et c est meme LA qu elle dort le plus longtemps.
                    # L UNIVERS VIDE reste reserve aux QA et PRODUCTION : une fiche en
                    # LABO a le droit de ne pas encore avoir d univers.
                    if (r.get('univers') or '').strip()
                    or (r.get('etat_vie') or '').strip().upper() in ('QA', 'PRODUCTION')]
        for s in vivantes:
            # L UNIVERS SEUL — le nom de la strategie n a rien a y faire.
            # Mesure du 13-09 : `champ` collait le nom apres l univers, et le
            # DERNIER mnemonique se soudait a lui — « VIE » devenait
            # « VIE COURS_BAS_ARGENT_REVIENT_6 », donc introuvable.
            # **5 reconnues sur 6, 9 sur 10 : le controle perdait exactement une
            # valeur par strategie, toujours la derniere, et personne ne pouvait
            # le voir puisqu il n annonce qu un compte.**
            # ET PAS DE REPLI SUR `filtres` : ce champ porte des conditions de
            # marche — « Phase haussiere, Resultats proches, Annonce macro » —
            # pas des mnemoniques. **Le repli transformait un univers VIDE en
            # trois jetons francais, donc en « 0 reconnue » au lieu d une alerte.**
            # C est le meme motif que le reste : un repli muet qui deguise une
            # absence en resultat.
            champ = (s.get('univers') or '')
            # LA CLE EST LE MNEMONIQUE, JAMAIS LE NOM — et ce programme faisait
            # l inverse de la loi qu il cite en tete. CC1 de Cowork, 13-09-2026 :
            #   « le tuple porte le mnemonique. Le code prend le nom. Les univers
            #    sont ecrits en mnemoniques : ce controle rendra 0 QUOI QU IL
            #    ARRIVE, et il ne l a jamais dit parce qu il ne leve aucune
            #    alerte — c est un infos.append, jamais un alertes.append. »
            # Mesure : l univers de C5E10-OBS-V1 vaut « TTE,ENGI,VIE,EN,FGR,… ».
            # Reconnues par le NOM : 0. Par le MNEMONIQUE : 11.
            # **Un controle qui ne peut rien trouver et qui se tait est pire qu un
            # controle absent : il occupe la place.**
            # On compare MNEMONIQUE a MNEMONIQUE, sur des jetons entiers — sinon
            # « EN » se trouverait dans « ENGI ».
            # LE DENOMINATEUR COMPTE LES JETONS ECRITS, PAS LES DISTINCTS — CC2.
            # « en, BVI ,fgr,RNO,URW,VIE,VIE » porte SEPT jetons ecrits ; l ensemble
            # en retenait six, et « 6/6 » s affichait. **Un mnemonique declare deux
            # fois ne laissait aucune trace**, alors que c est exactement le genre
            # de coquille que ce controle vient d apprendre a voir.
            # UNE ABSENCE DECLAREE N EST PAS UNE COQUILLE. Cinq fiches portent
            # « à renseigner » dans leur univers, et la sixieme porte la phrase que
            # je viens d y ecrire pour dire que la liste d avril n existe pas.
            # **Les traiter comme des mnemoniques produirait cinq fausses alertes
            # « inconnu du referentiel » la ou il faut lire « pas encore rempli ».**
            # Un mnemonique fait 1 a 5 caracteres ; une phrase n en est pas un.
            _brut = str(champ).strip()
            # PAS DE SEUIL DE LONGUEUR — trouve par mon propre garde-fou, 13-09.
            # J avais ecrit `len(_brut) > 120`, et 35 mnemoniques font 132 caracteres :
            # **un univers legitime etait pris pour un texte de remplacement.**
            # C est exactement ce que Cowork me reprochait une heure plus tot — un
            # COMPTE devenu critere. La propriete est ailleurs : un univers est une
            # liste de jetons COURTS ; un texte de remplacement porte des espaces
            # et des mots. **Si un seul jeton depasse 6 caracteres, ce n est pas un
            # univers.**
            _jx = [x.strip() for x in _brut.replace(";", ",").split(",") if x.strip()]
            if "renseigner" in _brut.lower() or any(len(x) > 6 for x in _jx):
                # CC3 de Cowork : quatre fiches sans univers rendaient quatre lignes
                # d information et ZERO alerte. « C est peut-etre delibere pour des
                # LABO ; rien ne le dit, et le lecteur ne peut pas distinguer un
                # choix d un oubli. » **C est la forme exacte que je venais de
                # corriger sur MA200-S1 deux heures plus tot.**
                # UN COMPTE EST DIT, ET IL SE VOIT : une ligne isolee se noie, un
                # total se lit. Ce n est pas une alerte — un LABO a le droit de ne
                # pas avoir d univers — mais ce n est plus un murmure.
                _a_renseigner.append(f"{s.get('id','?')} ({(s.get('etat_vie') or '?').strip()})")
                continue
            ecrits = [norm(x) for x in str(champ).replace(";", ",").split(",") if x.strip()]
            jetons = set(ecrits)
            if len(ecrits) != len(jetons):
                from collections import Counter as _C
                _d = sorted(k for k, v in _C(ecrits).items() if v > 1)
                alertes.append(f"DOUBLON dans l univers de {s.get('id','?')} : "
                               + ", ".join(f"« {x} »" for x in _d)
                               + f" — {len(ecrits)} mnemonique(s) ecrit(s) pour "
                                 f"{len(jetons)} distinct(s)")
            # DEUX ZEROS QUI NE DISENT PAS LA MEME CHOSE — CC2 de Cowork, 13-09.
            # MA200-S1 est en PRODUCTION avec un univers VIDE. Le controle
            # affichait « 0 valeur reconnue » pour elle COMME pour les autres :
            # **un lecteur ne pouvait pas distinguer « son univers est vide » de
            # « le controle ne sait pas lire ». Le meme zero couvrait deux causes
            # opposees.** Et un univers vide sur une strategie en PRODUCTION est
            # une ALERTE, pas une information.
            if not jetons:
                if (s.get('etat_vie') or '').strip().upper() not in ('QA', 'PRODUCTION'):
                    continue
                alertes.append(f"UNIVERS VIDE : la strategie {s.get('id','?')} est en "
                               f"{(s.get('etat_vie') or '?').strip()} et son champ univers "
                               f"ne porte aucun mnemonique")
                continue
            trouvees = [n for (n, m) in noms_ref if m and norm(m) in jetons]
            # ET DANS L AUTRE SENS — CC1 de Cowork, 13-09-2026, et c est l inverse
            # de la loi que ce programme cite en tete :
            #   « un mnemonique attendu qui ne renvoie rien est une ALERTE,
            #    jamais un silence »
            # Je parcourais le REFERENTIEL et je comptais qui s y retrouve. **Je ne
            # regardais JAMAIS les jetons de l univers qui ne sont au referentiel.**
            # Son sabotage : ajouter « ZZZZ » a un univers. Ecran INCHANGE.
            # Une coquille, une valeur sortie de l indice, un mnemonique modifie —
            # le controle qui existe pour ca ne le voyait pas.
            # DEUX CAUSES, DEUX MOTIFS, DEUX GESTES — CC1 de Cowork, 13-09-2026.
            # J ecrivais « absent du referentiel » en testant contre les ATTENDUES.
            # Sur `MT`, sorti de l univers a midi, le programme disait a trois
            # lignes d ecart : « ARCELORMITTAL est au referentiel, volontairement
            # hors univers » PUIS « son mnemonique est absent du referentiel ».
            # **Un lecteur qui suit le motif donne corrige la mauvaise chose :**
            #   absent du referentiel = coquille -> corriger la fiche de strategie
            #   hors univers          = exclu volontairement -> revoir la decision
            # C est la faute du tour 21 sous une forme neuve, sur la meme valeur.
            connus = {norm(m) for (n, m) in noms_ref if m}
            exclus = {norm(m): nom for (nom, m) in
                      [(v[0], _mn_hors(v)) for v in hors_univers.values()] if m}
            orphelins, ecartes = [], []
            for j in sorted(jetons):
                if j in connus:
                    continue
                (ecartes if j in exclus else orphelins).append(j)
            if orphelins:
                alertes.append(f"MNEMONIQUE INCONNU dans l univers de {s.get('id','?')} : "
                               + ", ".join(f"« {o} »" for o in orphelins)
                               + " — absent du referentiel : coquille ou valeur inconnue,"
                                 " corriger la fiche de la strategie")
            if ecartes:
                alertes.append(f"MNEMONIQUE HORS UNIVERS dans la fiche de {s.get('id','?')} : "
                               + ", ".join(f"« {e} » ({exclus[e]})" for e in ecartes)
                               + " — la valeur EST au referentiel mais en a ete ecartee"
                                 " volontairement : revoir la decision, ou la retirer de la fiche")
            # UN CHIFFRE NE S EMPLOIE QU AVEC CE QU IL MESURE — CC2 de Cowork.
            # « 10 valeur(s) reconnue(s) » s ecrivait pareil pour 10 sur 10 et
            # 10 sur 11. Le denominateur manquait dans la ligne meme que je
            # venais de reparer.
            infos.append(f"controle 3 : strategie {s.get('id','?')} — "
                         f"{len(trouvees)}/{len(ecrits)} mnemonique(s) de son univers "
                         f"reconnu(s) au referentiel")
        if not vivantes:
            infos.append("controle 3 : aucune strategie en QA ou en PRODUCTION")
    else:
        infos.append("controle 3 : registre des strategies introuvable")

    # --- rapport
    print(f"CONTROLE DES VALEURS ATTENDUES — {now.strftime('%d-%m-%Y %Hh%M')} (Paris)")
    print(f"regle I-9 du chapitre GESTION DE L'IDENTITE DES VALEURS\n")
    if _a_renseigner:
        infos.append(f"univers A RENSEIGNER : {len(_a_renseigner)} fiche(s) — "
                     + " · ".join(_a_renseigner))
    for i in infos:
        print("   ", i)
    print()

    if alertes:
        print(f"*** {len(alertes)} ALERTE(S) ***")
        for a in alertes:
            print("   !!", a)
        return 1
    print("   aucune alerte")
    return 0

if __name__ == '__main__':
    sys.exit(main())
