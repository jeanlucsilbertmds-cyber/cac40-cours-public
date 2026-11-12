#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTROLER_LES_MARQUES_DE_LA_LOI — chaque phrase d'une loi NON FIGÉE dit d'où elle vient.
Écrit le Mer 04-11-2026 (Paris), lot G, réparation demandée par le superviseur R-759 (avis du
04-11-2026 à 19h22, réparation R1 : « une source par phrase », points (a), (b), (c) et l'étape 4).
Simulation uniquement.

① RÔLE — Lire, dans `gouvernance/REGISTRE_REGLES.md`, chaque règle dont la ligne d'ouverture porte
  « NON FIGÉE » (aujourd'hui R-505, R-512 et R-513), et vérifier que CHAQUE phrase qui dit ce que
  la loi exige finit par UNE des quatre marques fixées par le superviseur :
    [DÉCISION JL, <date> <heure>, n°NN]        décision de Jean-Luc, au relevé du Chat
    [DÉCISION JL, <date> [<heure>], A-NNN]      décision de Jean-Luc, consignée au BACKLOG
    [DÉCISION JL, R-NNN]                        règle du REGISTRE en vigueur, appliquée telle quelle
    [CHOIX DÉLÉGUÉ DÉL-Dnn]                     choix fait par le Chat sous la délégation (n°129)
    [LECTURE DU CHAT → à transformer en DÉL-Dnn] lecture du Chat pas encore consignée en choix
    [QUESTION OUVERTE Q-Gn]                     question que seul Jean-Luc peut trancher
  Puis confronter chaque marque à sa source (relevé, BACKLOG, REGISTRE, fichier des choix) et
  fabriquer la liste « CE QUI RESTE À CONFIRMER », un point par choix ou question, avec la
  question, le choix, la raison, la façon de le défaire et les phrases de la loi qu'il touche ;
  et, à côté, la partie « CE QUE LA LOI VOUS ATTRIBUE » : pour chaque source citée par une marque
  DÉCISION JL, les mots de la source copiés tels quels, puis chaque phrase de la loi qui s'en
  réclame. Refuser aussi un identifiant écrit deux fois (choix Dnn, question Q-Gn, numéro n° du
  relevé), comparé sous sa forme canonique.
  Tour 4 (Mer 04-11-2026, avis du superviseur R-759 du même jour) : la propriété « Jean-Luc parle
  dans l'entrée citée », l'unicité des identifiants et la partie « ce que la loi vous attribue »
  sont ajoutées ; aucune recherche des mots « aucune décision » n'existe ni n'est ajoutée (elle
  épellerait : le relevé ne les écrit que 3 fois).
② CONTEXTE D'APPEL — À la main, par le Chat ou par une relecture, depuis la racine d'une copie du
  dépôt : `python3 programmes/CONTROLER_LES_MARQUES_DE_LA_LOI.py [--racine D] [--liste F]
  [--calibrer]`. Aucun circuit ne l'appelle aujourd'hui (voir ⑨).
③ ENTRÉE — Quatre fichiers sous la racine : le REGISTRE ; le relevé des décisions
  `etudes/JOURNEE_31-10-2026/chemin/A_CONSIGNER_AU_BACKLOG.md` ; `BACKLOG_DECISIONS.md` ; le
  fichier des choix délégués `etudes/JOURNEE_31-10-2026/delegation/CHOIX_FAITS_POUR_JEAN-LUC.md`
  (deux tables : les choix « | Dnn | heure | question | choix | raison | comment le défaire | »,
  et les questions « | Q-Gn | question | en attendant | ce qui en dépend | source | »).
  Le relevé écrit ses entrées en titres « ## n°NN — … » (ou « ### n°93 bis — … ») et, pour les
  n°1 à n°63, en lignes de table « | NN | manque | exemple | trouvé par | rattachement | ».
  `--liste F` : écrit dans le fichier F la liste « ce qui reste à confirmer » puis la partie
  « ce que la loi vous attribue ».
  `--calibrer` : rejoue le contrôle sur des copies EN MÉMOIRE du REGISTRE, sabotées.
④ CONDITIONS D'ENTRÉE — Au moins une règle porte « NON FIGÉE » sur sa ligne d'ouverture (sinon il
  n'y a rien à contrôler : code 2, jamais un vert silencieux, R-734bis).
⑤ SORTIE — UN code de sortie : 0 = toutes les phrases sont marquées, toutes les marques tiennent
  contre leur source et aucun identifiant n'est écrit deux fois ; 1 = au moins une faute, chacune
  écrite à l'écran ; 2 = le contrôle n'a pas pu tourner (fichier absent, aucune règle NON FIGÉE),
  raison à l'écran. Avec `--calibrer` : 0 si chaque sabotage a rougi pour la raison attendue et
  chaque témoin est resté vert, 1 sinon.
⑥ TRAITEMENT — Lire les quatre fichiers ; refuser les identifiants en double ; découper chaque
  règle NON FIGÉE en lignes ; écarter
  la fin de ligne qui commence à un libellé *Raison* ou *Exemple* (les explications que R-751 ⑥
  et ⑦ demandent, qui ne prescrivent rien) ou *Constat* (un fait relevé sur le code ou les
  données, qui ne prescrit rien non plus), et la zone du texte « GARDÉE POUR MÉMOIRE » (le texte
  remplacé) ; dans le reste, chaque phrase doit finir par une marque ; une ligne de table doit
  porter ses marques dans sa dernière case ; vérifier chaque marque ; refuser tout « Dnn » sans
  son préfixe d'espace (DÉL-, GRILLE-, SECTION 0-) ; fabriquer la liste.
⑦ UNITÉ — Des phrases (une phrase = un texte qui finit par « . », « ? » ou « ! » hors des
  guillemets « » et des parenthèses, ou par la fin de la ligne).
⑧ POURQUOI — Le 04-11-2026, la loi écrivait « Tout le reste est une décision de Jean-Luc » : par
  défaut, toute phrase non classée passait pour décidée par lui, et plusieurs choix du Chat lui
  étaient présentés comme les siens (relecture du lot G, défaut B1). Le superviseur a demandé
  d'inverser ce défaut : une phrase sans source est une faute, et c'est un programme qui le dit,
  pas la parole de l'auteur (R-754 : ce qu'un programme peut vérifier, un programme le vérifie).
  La liste à confirmer est FABRIQUÉE à partir des marques, jamais écrite à la main : deux textes
  écrits à la main divergent (R-708).
⑨ CE QUI CLOCHE — (1) Le programme ne juge pas le FOND : une marque « DÉCISION JL » posée sur une
  phrase que la décision ne dit pas passe, si la décision existe à la date et à l'heure écrites ;
  la table phrase → source → mots de la source reste un travail de lecture. (2) Une phrase
  normative glissée dans une explication *Raison*, *Exemple* ou *Constat* n'est pas vue. (3) Le découpage
  en phrases suit la ponctuation : une abréviation suivie d'une majuscule (« etc. Puis ») couperait
  une phrase en deux, ce qui rougit au lieu de laisser passer. (4) Les chemins des quatre fichiers
  sont écrits ici ; un fichier déplacé rend le code 2. (5) Il n'est inscrit à aucun circuit.
  (6) La propriété « Jean-Luc parle dans l'entrée citée » dit qu'il a parlé, pas qu'il a décidé
  ce que la phrase lui attribue : l'entrée n°112 (« Jean-Luc : « Faute de mon accord ? » —
  CORRECTION DU CHAT ») passe. Elle ne vaut que pour le relevé : une marque A-NNN ou R-NNN n'est
  pas confrontée à qui parle. (7) AUCUN PROGRAMME NE PEUT VÉRIFIER QU'UNE SOURCE « DIT » LA
  PHRASE : mesuré par le superviseur R-759 le 04-11-2026 (tour 4), ni l'ancrage des nombres
  (12 faux drapeaux sur 56 phrases chiffrées) ni la lecture mot à mot des citations (6 sur 34)
  n'auraient vu une phrase qui élargit sa source (B1) ou qui la rétrécit (I2). C'est pourquoi la
  partie « ce que la loi vous attribue » met les mots de la source sous les yeux de Jean-Luc :
  c'est son filet, pas celui du programme. (8) Les mots d'une marque A-NNN sont une fenêtre de la
  ligne du BACKLOG autour de la date citée (une ligne du BACKLOG peut dépasser 15 000 caractères),
  ceux d'une marque R-NNN le début de la ligne d'ouverture de la règle : le reste n'est pas montré.
⑩ EFFET — Écrit à l'écran ; avec `--liste F`, écrit le seul fichier F.
⑪ TERMINAISON — Rend la main avec son code de sortie ; aucun de ses appels ne peut ne pas revenir
  (lectures de fichiers locaux seulement).
  [sort: oui]
"""

import argparse
import os
import re
import sys
import unicodedata

REGISTRE = "gouvernance/REGISTRE_REGLES.md"
RELEVE = "etudes/JOURNEE_31-10-2026/chemin/A_CONSIGNER_AU_BACKLOG.md"
BACKLOG = "BACKLOG_DECISIONS.md"
CHOIX = "etudes/JOURNEE_31-10-2026/delegation/CHOIX_FAITS_POUR_JEAN-LUC.md"

OUVERTURE = re.compile(r"^(?:- \*\*|#{1,6} )(R-\d+\w*)\b")
FIN_DE_BLOC = re.compile(r"^(?:- \*\*|#)")
CROCHET = re.compile(r"\[([^\[\]]*)\]")
GENRES = ("DÉCISION JL", "CHOIX DÉLÉGUÉ", "LECTURE DU CHAT", "QUESTION OUVERTE")
DECISION = re.compile(r"^DÉCISION JL, (?:(\d\d-\d\d-\d{4})(?: (\d\dh\d\d))?, )?(n°\d+(?: ?(?:bis|ter))?|A-\d+|R-\d+\w*)$")
JEAN_LUC_PARLE_TITRE = re.compile(r"Jean-Luc ?:|DE JEAN-LUC")
JEAN_LUC_PARLE_TABLE = re.compile(r"décision JL|demande JL|question JL")
JEAN_LUC_NE_PARLE_PAS = "Jean-Luc ne parle pas"
EN_DOUBLE = "en double"
DELEGUE = re.compile(r"^CHOIX DÉLÉGUÉ (DÉL-D\d+)$")
LECTURE = re.compile(r"^LECTURE DU CHAT → à transformer en (DÉL-D\d+)$")
QUESTION = re.compile(r"^QUESTION OUVERTE (Q-G\d+)$")
EXPLICATION = re.compile(r"\*(?:Raison|Exemple|Constat)[^*]*\*")
D_SANS_PREFIXE = re.compile(r"(?<![\w-])D\d+\b")
PREFIXES = ("DÉL-", "GRILLE-", "SECTION 0-")


def blocs_non_figes(texte):
    """Rend la liste des règles NON FIGÉES : (numéro, numéro de la première ligne, lignes).

    ① RÔLE — Trouver dans le REGISTRE les règles dont la ligne d'ouverture porte « NON FIGÉE ».
    ② CONTEXTE D'APPEL — `controler`, une fois par REGISTRE contrôlé.
    ③ ENTRÉE — `texte` : le texte entier du REGISTRE.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : une liste de triplets (numéro de règle, n° de ligne de l'ouverture,
      liste des lignes du bloc) ; vide si aucune règle ne porte « NON FIGÉE ».
      [rend: 1]
    ⑥ TRAITEMENT — Une ligne d'ouverture commence, en colonne 0, par « - **R-nnn » ou par un titre
      « # R-nnn » ; le bloc court jusqu'à la ligne suivante qui commence, en colonne 0, par
      « - ** » ou « # ». Le bloc est gardé si sa ligne d'ouverture contient « NON FIGÉE ».
    ⑦ UNITÉ — Des règles.
    ⑧ POURQUOI — La marque est exigée des règles préparées sous délégation et non confirmées ;
      la propriété « NON FIGÉE » les désigne sans épeler leurs numéros : renommer une règle ne
      change pas l'avis du contrôle.
    ⑨ CE QUI CLOCHE — Une règle NON FIGÉE dont la mention serait écrite sur une autre ligne que
      son ouverture ne serait pas contrôlée.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    lignes = texte.split("\n")
    sortie, i = [], 0
    while i < len(lignes):
        m = OUVERTURE.match(lignes[i])
        if not m:
            i += 1
            continue
        j = i + 1
        while j < len(lignes) and not FIN_DE_BLOC.match(lignes[j]):
            j += 1
        if "NON FIGÉE" in lignes[i]:
            sortie.append((m.group(1), i + 1, lignes[i:j]))
        i = j
    return sortie


def entree_du_releve(releve, numero):
    """Rend le texte de l'entrée n°NN du relevé des décisions, ou None.

    ① RÔLE — Retrouver une décision du relevé par son numéro.
    ② CONTEXTE D'APPEL — `verifier_une_marque`, pour chaque « DÉCISION JL, …, n°NN ».
    ③ ENTRÉE — `releve` : texte du relevé · `numero` : « 82 », « 37bis », « 93 bis »…
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte de l'entrée (titre « ## n°NN — » jusqu'au titre suivant, ou
      ligne de table « | NN | »), ou None si elle n'existe pas.
      [rend: 1]
    ⑥ TRAITEMENT — Chercher d'abord le titre « ## n°NN — », puis la ligne de table « | NN | ». Un
      suffixe « bis » ou « ter » se lit avec ou sans espace avant lui (« 93 bis » = « 93bis »).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le relevé écrit les n°1 à n°63 en table et les suivants en titres ; il écrit
      « ### n°93 bis — », avec une espace.
    ⑨ CE QUI CLOCHE — Un numéro écrit deux fois (titre et table) : le titre l'emporte ici ; c'est
      `identifiants_en_double` qui le refuse, avant toute lecture.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    m = re.fullmatch(r"(\d+) ?(bis|ter)?", numero)
    if not m:
        return None
    motif = m.group(1) + (r" ?" + m.group(2) if m.group(2) else "")
    m = re.search(r"^#{2,3} n°" + motif + r" —.*?(?=^#{2,3} |\Z)", releve, re.M | re.S)
    if m:
        return m.group(0)
    m = re.search(r"^\| " + motif + r" \|.*$", releve, re.M)
    return m.group(0) if m else None


def jean_luc_parle(entree):
    """Rend True si l'entrée du relevé montre que Jean-Luc y parle.

    ① RÔLE — Dire si une entrée du relevé peut porter une décision de Jean-Luc.
    ② CONTEXTE D'APPEL — `verifier_une_marque`, pour chaque « DÉCISION JL, …, n°NN » dont l'entrée
      existe.
    ③ ENTRÉE — `entree` : le texte rendu par `entree_du_releve`.
    ④ CONDITIONS D'ENTRÉE — `entree` n'est pas None.
    ⑤ SORTIE — UNE valeur : un booléen.
      [rend: 1]
    ⑥ TRAITEMENT — Une entrée en titre : la partie du titre après le premier « — » contient
      « Jean-Luc : » (ou « Jean-Luc: ») ou « DE JEAN-LUC ». Une ligne de table : sa quatrième case,
      « Trouvé par », contient « décision JL », « demande JL » ou « question JL ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une marque « DÉCISION JL » vers une entrée de constats (n°69 : « aucune décision
      de Jean-Luc » ; n°93 bis : « vérification faite à 12h45 ») passait au vert (relecture T3 du
      lot G, I3). Chercher les mots « aucune décision » épellerait : le relevé ne les écrit que
      3 fois, et une entrée de constats rédigée autrement passerait. La propriété est POSITIVE :
      l'entrée doit montrer que Jean-Luc parle. Mesurée par le superviseur R-759 le 04-11-2026
      (tour 4) : les 41 entrées réellement citées passent, n°69 et n°93 bis échouent.
    ⑨ CE QUI CLOCHE — Elle dit que Jean-Luc a parlé, pas qu'il a décidé ce que la phrase lui
      attribue : n°112 (« Jean-Luc : « Faute de mon accord ? » — CORRECTION DU CHAT ») passe.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    premiere = entree.split("\n", 1)[0]
    if premiere.startswith("#"):
        apres = premiere.split(" — ", 1)[1] if " — " in premiere else ""
        return bool(JEAN_LUC_PARLE_TITRE.search(apres))
    cases = [c.strip() for c in premiere.strip().strip("|").split("|")]
    return len(cases) > 3 and bool(JEAN_LUC_PARLE_TABLE.search(cases[3]))


def forme_canonique(identifiant):
    """Rend la forme canonique d'un identifiant : « Ｄ 35 », « D35 » et « d35 » donnent « D35 ».

    ① RÔLE — Comparer deux identifiants sans dépendre de leur graphie.
    ② CONTEXTE D'APPEL — `identifiants_en_double`.
    ③ ENTRÉE — `identifiant` : le texte d'une case ou d'un titre (« D1-bis », « Q-G1 », « 93 bis »).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte normalisé NFKC, sans aucun caractère autre que lettre ou
      chiffre, en majuscules (« D1-bis » → « D1BIS », « Q-G1 » → « QG1 », « 93 bis » → « 93BIS »).
      [rend: 1]
    ⑥ TRAITEMENT — NFKC ; retirer tout caractère qui n'est ni lettre ni chiffre ; majuscules.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un doublon écrit avec un tiret insécable, une lettre pleine chasse ou une espace
      ne doit pas passer (même leçon que l'unicité des règles du REGISTRE, relecture du lot G).
    ⑨ CE QUI CLOCHE — Une lettre d'une autre écriture qui ressemble à « D » (cyrillique, grecque)
      n'est pas ramenée par NFKC : l'identifiant ne serait pas reconnu, donc pas compté.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return re.sub(r"[\W_]", "", unicodedata.normalize("NFKC", identifiant)).upper()


def identifiants_en_double(texte_choix, releve):
    """Rend la liste des fautes « identifiant en double » du fichier des choix et du relevé.

    ① RÔLE — Refuser qu'un même identifiant désigne deux choses.
    ② CONTEXTE D'APPEL — `controler`, une fois.
    ③ ENTRÉE — `texte_choix` : le fichier des choix · `releve` : le relevé des décisions.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : liste de fautes, vide si chaque identifiant est unique.
      [rend: 1]
    ⑥ TRAITEMENT — Trois espaces, chacun compté à part, sur la forme canonique. Choix délégués :
      toute ligne de table du fichier des choix dont la première case a la forme canonique
      « D » + chiffres (+ « BIS » ou « TER »). Questions ouvertes : « QG » + chiffres. Relevé :
      tout titre « n°… — » (la partie entre « n° » et « — ») et toute ligne de table dont la
      première case a la forme canonique chiffres (+ « BIS » ou « TER »). Un identifiant vu plus
      d'une fois dans son espace est une faute, avec ses lignes.
    ⑦ UNITÉ — Des identifiants.
    ⑧ POURQUOI — Le 04-11-2026, D25 et D26 désignaient chacun deux choix différents dans le
      fichier qui faisait foi, et `lire_les_choix` gardait la dernière ligne sans rien dire : la
      liste à confirmer montrait un seul des deux (relecture T3, I1 ; avis du superviseur R-759,
      tour 4). Un numéro du relevé écrit deux fois ferait citer une entrée pour une autre.
    ⑨ CE QUI CLOCHE — Une ligne dont la première case n'a pas la forme d'un identifiant
      (« D-à-numéroter ») n'est pas comptée : c'est voulu, elle attend son numéro. Dans le relevé,
      un tableau d'une autre nature dont la première colonne serait numérique compterait ses
      lignes comme des entrées (aucun aujourd'hui : mesuré le 04-11-2026, 142 identifiants, aucun
      doublon).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    vus = {}
    for n, ligne in enumerate(texte_choix.split("\n"), 1):
        if not ligne.lstrip().startswith("|"):
            continue
        cle = forme_canonique(ligne.strip().strip("|").split("|")[0])
        if re.fullmatch(r"D\d+(?:BIS|TER)?", cle):
            vus.setdefault(("choix", cle), []).append(n)
        elif re.fullmatch(r"QG\d+", cle):
            vus.setdefault(("questions", cle), []).append(n)
    for n, ligne in enumerate(releve.split("\n"), 1):
        m = re.match(r"\s{0,3}#{1,6}\s*n°\s*(.+?)\s+—", ligne)
        if m:
            vus.setdefault(("relevé", forme_canonique(m.group(1))), []).append(n)
            continue
        if ligne.lstrip().startswith("|"):
            cle = forme_canonique(ligne.strip().strip("|").split("|")[0])
            if re.fullmatch(r"\d+(?:BIS|TER)?", cle):
                vus.setdefault(("relevé", cle), []).append(n)
    return [f"{espace} : l'identifiant {cle} est {EN_DOUBLE}, lignes {', '.join(map(str, lignes))}"
            for (espace, cle), lignes in sorted(vus.items()) if len(lignes) > 1]


def lire_les_choix(texte_choix):
    """Rend les choix délégués et les questions ouvertes du fichier des choix.

    ① RÔLE — Lire les deux tables du fichier des choix délégués.
    ② CONTEXTE D'APPEL — `controler`, une fois.
    ③ ENTRÉE — `texte_choix` : texte du fichier des choix.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : {« DÉL-Dnn »: [heure, question, choix, raison, défaire]} et
      {« Q-Gn »: [question, en attendant, ce qui en dépend, source]}.
      [rend: 2]
    ⑥ TRAITEMENT — Toute ligne de table dont la première case est « Dnn » est un choix ; « Q-Gn »,
      une question. Une case est la suite de caractères entre deux « | » ; une case vide reste
      vide (« || » donne une case vide).
    ⑦ UNITÉ — Des lignes de table.
    ⑧ POURQUOI — La n°129 exige que chaque choix porte la question, le choix, la raison et la façon
      de le défaire : le programme le vérifie au lieu de le supposer.
    ⑨ CE QUI CLOCHE — Un « | » écrit à l'intérieur d'une case la couperait en deux et décalerait
      les colonnes ; le contrôle du nombre de cases le signale (`controler`).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    choix, questions = {}, {}
    for ligne in texte_choix.split("\n"):
        if not ligne.startswith("| "):
            continue
        cases = [c.strip() for c in ligne.strip().strip("|").split("|")]
        if re.fullmatch(r"D\d+", cases[0]):
            choix["DÉL-" + cases[0]] = cases[1:]
        elif re.fullmatch(r"Q-G\d+", cases[0]):
            questions[cases[0]] = cases[1:]
    return choix, questions


def verifier_une_marque(contenu, sources):
    """Rend la liste des fautes d'une marque, son genre et ses identifiants.

    ① RÔLE — Confronter une marque à sa source.
    ② CONTEXTE D'APPEL — `controler`, pour chaque marque trouvée.
    ③ ENTRÉE — `contenu` : le texte entre crochets · `sources` : dictionnaire des sources lues
      (« releve », « backlog », « regles » : ensemble des règles ouvertes et non remplacées,
      « choix », « questions »).
    ④ CONDITIONS D'ENTRÉE — `contenu` commence par l'un des quatre genres.
    ⑤ SORTIE — TROIS valeurs : liste des fautes (vide si la marque tient) ; le genre ; la liste des
      identifiants (n°NN, A-NNN, R-NNN, DÉL-Dnn, Q-Gn).
      [rend: 3]
    ⑥ TRAITEMENT — Plusieurs marques séparées par « ; » dans un même crochet ne sont admises que
      si toutes sont des DÉCISION JL (une phrase qui mêle deux genres se coupe en deux). n°NN :
      l'entrée existe, ses 400 premiers caractères portent la date et l'heure écrites, et elle
      montre que Jean-Luc y parle (`jean_luc_parle` ; les deux contrôles sont faits l'un et
      l'autre, chacun avec sa faute). A-NNN :
      la ligne du BACKLOG existe et porte la date (JJ-MM-AAAA, JJ/MM/AAAA ou JJ/MM) et l'heure si
      elle est écrite. R-NNN : la règle est ouverte au REGISTRE et sa ligne d'ouverture ne dit pas
      REMPLACÉE. DÉL-Dnn : la ligne existe et ses quatre champs (question, choix, raison, défaire)
      sont remplis, ni vides ni « — ». Q-Gn : la ligne existe et ses quatre champs sont remplis.
      LECTURE → DÉL-Dnn : admise, comptée à part (à transformer).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une source citée sans être ouverte est la faute que R-719 et R-720 interdisent ;
      la n°129 exige les quatre champs de chaque choix.
    ⑨ CE QUI CLOCHE — La date et l'heure sont cherchées dans le début de l'entrée, pas comparées à
      un champ : une entrée qui cite une autre heure dans ses 400 premiers caractères passerait.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    fautes, ids = [], []
    morceaux = [x.strip() for x in contenu.split(";")]
    genres = {next((g for g in GENRES if x.startswith(g)), "?") for x in morceaux}
    if len(morceaux) > 1 and genres != {"DÉCISION JL"}:
        return [f"[{contenu}] mêle plusieurs genres : couper la phrase en deux"], "?", []
    genre = genres.pop()
    for x in morceaux:
        m = DECISION.match(x)
        if m:
            date, heure, ref = m.groups()
            ids.append(ref)
            if ref.startswith("n°"):
                e = entree_du_releve(sources["releve"], ref[2:])
                if e is None:
                    fautes.append(f"[{x}] : {ref} absent du relevé")
                else:
                    if not date or date not in e[:400] or (heure and heure not in e[:400]):
                        fautes.append(f"[{x}] : la date ou l'heure ne se lit pas en tête de {ref}")
                    if not jean_luc_parle(e):
                        fautes.append(f"[{x}] : dans {ref}, {JEAN_LUC_NE_PARLE_PAS} (titre sans « Jean-Luc : » "
                                      "ni « DE JEAN-LUC », ou case « Trouvé par » sans « décision JL », « demande JL », "
                                      "« question JL ») : ce n'est pas une décision à lui attribuer")
            elif ref.startswith("A-"):
                lb = re.search(r"^\| " + re.escape(ref) + r" \|.*$", sources["backlog"], re.M)
                j, mo, an = (date.split("-") if date else (None, None, None))
                formes = [date, f"{j}/{mo}/{an}", f"{j}/{mo}"] if date else []
                if lb is None:
                    fautes.append(f"[{x}] : {ref} absente du BACKLOG")
                elif not date or not any(f in lb.group(0) for f in formes) or (heure and heure not in lb.group(0)):
                    fautes.append(f"[{x}] : la date ou l'heure ne se lit pas dans la ligne {ref} du BACKLOG")
            else:
                if date:
                    fautes.append(f"[{x}] : une règle se cite sans date")
                if ref not in sources["regles"]:
                    fautes.append(f"[{x}] : {ref} n'est pas une règle ouverte et en vigueur au REGISTRE")
            continue
        m = DELEGUE.match(x) or LECTURE.match(x)
        if m:
            ids.append(m.group(1))
            if DELEGUE.match(x):
                c = sources["choix"].get(m.group(1))
                if c is None:
                    fautes.append(f"[{x}] : {m.group(1)} absent du fichier des choix")
                elif len(c) < 5 or any(v in ("", "—") for v in (c[1], c[2], c[3], c[4])):
                    fautes.append(f"[{x}] : {m.group(1)} n'a pas ses quatre champs (question, choix, raison, défaire)")
            continue
        m = QUESTION.match(x)
        if m:
            ids.append(m.group(1))
            q = sources["questions"].get(m.group(1))
            if q is None or len(q) < 4 or any(v in ("", "—") for v in q[:4]):
                fautes.append(f"[{x}] : {m.group(1)} absente du fichier des choix ou incomplète")
            continue
        fautes.append(f"[{x}] : marque mal écrite (les quatre libellés s'écrivent à l'identique)")
    return fautes, genre, ids


def couper_en_phrases(ligne):
    """Rend les morceaux d'une ligne : (texte, marque ou None), dans l'ordre.

    ① RÔLE — Découper une ligne de prose en phrases, chacune avec la marque qui la termine.
    ② CONTEXTE D'APPEL — `controler`, pour chaque ligne de prose d'une règle NON FIGÉE.
    ③ ENTRÉE — `ligne` : une ligne, explication *Raison*/*Exemple* déjà retirée.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : liste de (texte de la phrase, contenu de sa marque ou None).
      [rend: 1]
    ⑥ TRAITEMENT — Parcourir les caractères en comptant la profondeur des guillemets « » et des
      parenthèses. Un crochet dont le contenu commence par un genre de marque ferme la phrase en
      cours avec cette marque. Hors guillemets et parenthèses, « . », « ? » ou « ! » suivi d'un
      espace, ou de « ** » puis d'un espace, ferme la phrase en cours sans marque. La fin de la
      ligne ferme le reste.
    ⑦ UNITÉ — Des phrases.
    ⑧ POURQUOI — Une citation de Jean-Luc contient ses propres points ; elle ne doit pas couper la
      phrase qui la cite.
    ⑨ CE QUI CLOCHE — Un guillemet « non fermé déséquilibre le compte jusqu'à la fin de la ligne :
      les phrases suivantes de la ligne seraient lues comme une seule (faute possible non vue).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main (une boucle sur les caractères de la ligne).
      [sort: non]
    """
    morceaux, debut, prof, i = [], 0, 0, 0
    while i < len(ligne):
        c = ligne[i]
        if c == "[":
            m = CROCHET.match(ligne, i)
            if m and m.group(1).startswith(GENRES):
                morceaux.append((ligne[debut:i], m.group(1)))
                i = debut = m.end()
                continue
        if c in "«(":
            prof += 1
        elif c in "»)":
            prof = max(0, prof - 1)
        elif c in ".?!" and prof == 0:
            reste = ligne[i + 1:]
            if reste.startswith(" ") or reste.startswith("** ") or reste == "" or reste == "**":
                morceaux.append((ligne[debut:i + 1], None))
                debut = i + 1
        i += 1
    morceaux.append((ligne[debut:], None))
    return morceaux


def controler(textes):
    """Rend les fautes, les points à confirmer et le nombre de phrases par genre.

    ① RÔLE — Appliquer le contrôle des marques à un jeu de textes (REGISTRE, relevé, BACKLOG, choix).
    ② CONTEXTE D'APPEL — `main` (vrais fichiers) et `calibrer` (copies sabotées en mémoire).
    ③ ENTRÉE — `textes` : dictionnaire {« registre », « releve », « backlog », « choix »: texte}.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — QUATRE valeurs : liste des fautes ; dictionnaire {identifiant : liste de (règle,
      ligne, phrase)} des points à confirmer ; dictionnaire {genre : nombre de phrases qui portent
      une marque de ce genre} (une ligne de table qui porte deux genres compte une fois pour
      chacun) ; dictionnaire {source citée par une DÉCISION JL (« n°82 », « A-305 », « R-708 ») :
      liste de (règle, ligne, phrase, date citée ou None, heure citée ou None)}. Si aucune règle
      n'est NON FIGÉE, la liste des fautes porte « IMPOSSIBLE » en premier.
      [rend: 4]
    ⑥ TRAITEMENT — Refuser les identifiants en double (`identifiants_en_double`) ; lire les règles
      ouvertes et non remplacées ; lire les choix ; pour chaque règle
      NON FIGÉE : refuser tout « Dnn » sans préfixe ; ignorer la zone « GARDÉ POUR MÉMOIRE » ;
      pour une ligne de table de données, exiger des marques dans la dernière case ; pour une
      ligne de prose, retirer l'explication, couper en phrases, exiger une marque pour toute
      phrase qui contient une minuscule (une phrase toute en majuscules est un titre) ; vérifier
      chaque marque ; ranger les marques autres que DÉCISION JL dans les points à confirmer, et
      chaque source d'une DÉCISION JL dans les attributions.
    ⑦ UNITÉ — Des phrases et des marques.
    ⑧ POURQUOI — Voir l'en-tête, ⑧.
    ⑨ CE QUI CLOCHE — Voir l'en-tête, ⑨ (1) à (3).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    reg = textes["registre"]
    regles = set()
    for ligne in reg.split("\n"):
        m = OUVERTURE.match(ligne)
        if m and "REMPLACÉE" not in ligne:
            regles.add(m.group(1))
    choix, questions = lire_les_choix(textes["choix"])
    sources = {"releve": textes["releve"], "backlog": textes["backlog"], "regles": regles,
               "choix": choix, "questions": questions}
    fautes, a_confirmer, compte, attribuees = [], {}, {g: 0 for g in GENRES}, {}

    def attribuer(mq, ou_regle, ou_ligne, phrase):
        """Range chaque source d'une marque DÉCISION JL avec la phrase qui s'en réclame.

        ① RÔLE — Remplir les attributions.
        ② CONTEXTE D'APPEL — `controler`, pour chaque marque DÉCISION JL.
        ③ ENTRÉE — `mq` : le texte entre crochets · `ou_regle`, `ou_ligne` : règle et
          n° de ligne · `phrase` : la phrase ou la ligne de table.
        ④ CONDITIONS D'ENTRÉE — `mq` est de genre DÉCISION JL.
        ⑤ SORTIE — Aucune valeur.
          [rend: rien]
        ⑥ TRAITEMENT — Pour chaque morceau séparé par « ; » qui suit le motif DECISION, ajouter
          (règle, ligne, phrase, date, heure) sous sa source.
        ⑦ UNITÉ — Des marques.
        ⑧ POURQUOI — Fabriquer « ce que la loi vous attribue » (avis du superviseur R-759, tour 4,
          condition 1).
        ⑨ CE QUI CLOCHE — Un morceau mal écrit n'est pas rangé ; il est déjà une
          faute de `verifier_une_marque`.
        ⑩ EFFET — Modifie `attribuees`.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        for x in mq.split(";"):
            m = DECISION.match(x.strip())
            if m:
                attribuees.setdefault(m.group(3), []).append((ou_regle, ou_ligne, phrase, m.group(1), m.group(2)))

    fautes += identifiants_en_double(textes["choix"], textes["releve"])
    for cle, c in choix.items():
        if len(c) != 5:
            fautes.append(f"fichier des choix : {cle} a {len(c) + 1} cases au lieu de 6 (colonnes décalées)")
    blocs = blocs_non_figes(reg)
    if not blocs:
        return ["IMPOSSIBLE : aucune règle ne porte « NON FIGÉE » sur sa ligne d'ouverture"], {}, compte, {}
    for numero, premiere, lignes in blocs:
        archive = False
        for k, ligne in enumerate(lignes):
            ou = f"{numero}, ligne {premiere + k}"
            for m in D_SANS_PREFIXE.finditer(ligne):
                if not any(ligne[:m.start()].endswith(p) for p in PREFIXES):
                    fautes.append(f"{ou} : « {m.group(0)} » sans préfixe d'espace (DÉL-, GRILLE-, SECTION 0-)")
            if archive or ("GARDÉE POUR MÉMOIRE" in ligne and ligne.strip().startswith("**")):
                archive = True
                continue
            corps = ligne.strip()
            if not corps:
                continue
            if corps.startswith("|"):
                cases = [x.strip() for x in corps.strip("|").split("|")]
                if set(cases[0]) <= set("-: ") or all(set(x) <= set("-: ") for x in cases):
                    continue
                suivante = lignes[k + 1].strip() if k + 1 < len(lignes) else ""
                if suivante.startswith("|") and set(suivante.replace("|", "").strip()) <= set("-: "):
                    continue
                marques = CROCHET.findall(cases[-1])
                reste = CROCHET.sub("", cases[-1]).replace(";", "").strip()
                if not marques or reste:
                    fautes.append(f"{ou} : ligne de table sans marque seule dans sa dernière case : {corps[:90]}")
                genres_de_la_ligne = set()
                for mq in marques:
                    f, genre, ids = verifier_une_marque(mq, sources)
                    fautes += [f"{ou} : {x}" for x in f]
                    genres_de_la_ligne.add(genre)
                    if genre == "DÉCISION JL":
                        attribuer(mq, numero, premiere + k, corps)
                    for i in ids if genre != "DÉCISION JL" else []:
                        a_confirmer.setdefault(i, []).append((numero, premiere + k, corps))
                for genre in genres_de_la_ligne:
                    compte[genre] = compte.get(genre, 0) + 1
                continue
            sans_explication = EXPLICATION.split(corps, 1)[0]
            for phrase, mq in couper_en_phrases(sans_explication):
                lettres = re.sub(r"[^\w]", "", phrase)
                if mq is None:
                    if any(ch.islower() for ch in lettres):
                        fautes.append(f"{ou} : phrase sans marque : « {phrase.strip()[:120]} »")
                    continue
                if not any(ch.isalpha() for ch in lettres):
                    fautes.append(f"{ou} : marque [{mq}] sans phrase devant elle")
                f, genre, ids = verifier_une_marque(mq, sources)
                fautes += [f"{ou} : {x}" for x in f]
                compte[genre] = compte.get(genre, 0) + 1
                if genre == "DÉCISION JL":
                    attribuer(mq, numero, premiere + k, phrase.strip())
                for i in ids if genre != "DÉCISION JL" else []:
                    a_confirmer.setdefault(i, []).append((numero, premiere + k, phrase.strip()))
    return fautes, a_confirmer, compte, attribuees


def mots_de_la_source(ref, citations, textes):
    """Rend les lignes de texte qui montrent les mots d'une source, copiés tels quels.

    ① RÔLE — Mettre sous les yeux de Jean-Luc ce que dit la source qu'une phrase lui attribue.
    ② CONTEXTE D'APPEL — `ecrire_la_liste`, une fois par source attribuée.
    ③ ENTRÉE — `ref` : « n°NN », « A-NNN » ou « R-NNN » · `citations` : liste de (règle, ligne,
      phrase, date, heure) rendue par `controler` · `textes` : les quatre textes lus.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : une liste de lignes Markdown, chacune préfixée « > ».
      [rend: 1]
    ⑥ TRAITEMENT — n°NN : l'entrée entière du relevé (`entree_du_releve`). A-NNN : pour chaque date
      citée, une fenêtre de la ligne du BACKLOG, de 400 caractères avant la première heure citée
      (ou, sans heure, la première forme de la date) à 800 après, coupures marquées « […] ».
      R-NNN : les 1 200 premiers caractères de la ligne d'ouverture de la règle, coupure marquée.
      Une source introuvable rend la ligne « (source introuvable) ».
    ⑦ UNITÉ — Des caractères.
    ⑧ POURQUOI — Les mots de la source sont COPIÉS par programme, jamais réécrits : une
      paraphrase de la source referait l'écart qu'on veut montrer (avis du superviseur R-759,
      tour 4, condition 1).
    ⑨ CE QUI CLOCHE — La fenêtre d'une ligne A-NNN et la coupure d'une règle R-NNN peuvent laisser
      hors champ le passage qui compte ; la ligne entière est au BACKLOG ou au REGISTRE.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    def cite(t):
        """Rend `t` en citation Markdown.

        ① RÔLE — préfixer « > ».
        ② CONTEXTE D'APPEL — `mots_de_la_source`.
        ③ ENTRÉE — `t` : un texte.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : liste de lignes.
          [rend: 1]
        ⑥ TRAITEMENT — une ligne « > … » par ligne du texte.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — garder le texte tel quel et le distinguer de la liste.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        return ["> " + x if x else ">" for x in t.rstrip().split("\n")]
    if ref.startswith("n°"):
        e = entree_du_releve(textes["releve"], ref[2:])
        return cite(e) if e else ["> (source introuvable)"]
    if ref.startswith("A-"):
        lb = re.search(r"^\| " + re.escape(ref) + r" \|.*$", textes["backlog"], re.M)
        if not lb:
            return ["> (source introuvable)"]
        ligne, out = lb.group(0), []
        for date, heure in sorted({(c[3], c[4]) for c in citations}, key=str):
            formes = [heure] if heure else []
            if date:
                j, mo, an = date.split("-")
                formes += [date, f"{j}/{mo}/{an}", f"{j}/{mo}"]
            pos = next((ligne.find(f) for f in formes if f and f in ligne), 0)
            a, b = max(0, pos - 400), min(len(ligne), pos + 800)
            out += cite(("[…] " if a else "") + ligne[a:b] + (" […]" if b < len(ligne) else ""))
        return out
    for x in textes["registre"].split("\n"):
        m = OUVERTURE.match(x)
        if m and m.group(1) == ref:
            return cite(x[:1200] + (" […]" if len(x) > 1200 else ""))
    return ["> (source introuvable)"]


def rang_de_source(ref):
    """Rend la clé de tri d'une source : les n° du relevé, puis les A-NNN, puis les R-NNN.

    ① RÔLE — Ordonner « ce que la loi vous attribue ».
    ② CONTEXTE D'APPEL — `ecrire_la_liste`.
    ③ ENTRÉE — `ref` : « n°93 bis », « A-305 », « R-708 »…
    ④ CONDITIONS D'ENTRÉE — `ref` porte un chiffre.
    ⑤ SORTIE — TROIS valeurs, en un triplet qui sert de clé de tri : 0, 1 ou 2 ; numéro ; suffixe.
      [rend: 3]
    ⑥ TRAITEMENT — premier nombre de `ref`, et ce qui le suit.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — lire les décisions dans l'ordre de leur numéro.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    m = re.search(r"(\d+)(.*)$", ref)
    return ({"n": 0, "A": 1}.get(ref[0], 2), int(m.group(1)), m.group(2).strip())


def ecrire_la_liste(a_confirmer, choix, questions, attribuees=None, textes=None):
    """Rend le texte de la liste « CE QUI RESTE À CONFIRMER » et de la partie « CE QUE LA LOI VOUS
    ATTRIBUE », fabriquées à partir des marques.

    ① RÔLE — Fabriquer la liste que Jean-Luc lit un point à la fois, et le filet de ses décisions.
    ② CONTEXTE D'APPEL — `main`, avec `--liste` ou pour le résumé à l'écran.
    ③ ENTRÉE — `a_confirmer`, `attribuees` (rendus par `controler`) · `choix`, `questions` (rendus
      par `lire_les_choix`) · `textes` : les quatre textes lus (pour copier les mots des sources).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte Markdown.
      [rend: 1]
    ⑥ TRAITEMENT — Un point par identifiant, dans l'ordre : questions ouvertes, puis lectures du
      Chat, puis choix délégués, chacun par numéro croissant ; pour chacun, les champs du fichier
      des choix, puis chaque phrase de la loi qui le porte, avec sa règle et sa ligne. Puis, si
      `attribuees` et `textes` sont donnés, un groupe « A1, A2… » par source citée comme décision
      de Jean-Luc (n° du relevé, puis A-NNN, puis R-NNN) : les mots de la source
      (`mots_de_la_source`), puis chaque phrase de la loi qui s'en réclame. Une phrase qui cite
      plusieurs sources figure sous chacune.
    ⑦ UNITÉ — Des points à confirmer et des groupes d'attribution.
    ⑧ POURQUOI — Jean-Luc, n°129 : « me dire tous les choix que tu as pris pour moi un par un ».
      Et aucun programme ne peut vérifier qu'une source dit la phrase (en-tête, ⑨ (7)) : les
      phrases qui lui sont attribuées passent sous ses yeux à côté des mots de leur source.
    ⑨ CE QUI CLOCHE — Un choix consigné au fichier mais porté par aucune phrase n'apparaît pas :
      la liste ne dit que ce que la loi emploie. Une phrase marquée dans un *Raison*, *Exemple*
      ou *Constat* n'est pas lue, donc pas listée.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    def rang(i):
        """Rend la clé de tri d'un identifiant : les questions d'abord, puis par numéro.

        ① RÔLE — Ordonner la liste.
        ② CONTEXTE D'APPEL — `sorted`, dans `ecrire_la_liste`.
        ③ ENTRÉE — `i` : « Q-Gn » ou « DÉL-Dnn ».
        ④ CONDITIONS D'ENTRÉE — `i` porte au moins un chiffre.
        ⑤ SORTIE — DEUX valeurs, en un couple qui sert de clé de tri : 0 pour une question, 1 sinon ; numéro
          (fiche corrigée le 04-11-2026 au tour 4 : elle disait « UNE valeur »).
          [rend: 2]
        ⑥ TRAITEMENT — garder les chiffres de `i`.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — une question ouverte bloque le premier jugement de C5 : elle se lit en premier.
        ⑨ CE QUI CLOCHE — « DÉL-D1-bis » donnerait 11 (chiffres collés) ; aucun identifiant de ce
          genre n'est porté par une marque, le motif DELEGUE l'interdit.
        ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        n = int(re.sub(r"\D", "", i))
        return (0 if i.startswith("Q-") else 1, n)
    out = ["# CE QUI RESTE À CONFIRMER — fabriqué par programmes/CONTROLER_LES_MARQUES_DE_LA_LOI.py",
           "", "Simulation uniquement. Ne s'écrit jamais à la main : on change la loi ou le fichier "
           "des choix, puis on relance le programme. Une question ouverte ne s'applique pas ; "
           "elle bloque le premier jugement de C5 (garde-fou de la n°129).", ""]
    for n, i in enumerate(sorted(a_confirmer, key=rang), 1):
        out.append(f"## {n}. {i}")
        if i.startswith("Q-"):
            q = questions.get(i, ["?"] * 4)
            out += [f"- **Question** : {q[0]}", f"- **En attendant** : {q[1]}",
                    f"- **Ce qui en dépend** : {q[2]}", f"- **Source** : {q[3]}"]
        else:
            c = choix.get(i, ["?"] * 5)
            out += [f"- **Question** : {c[1]}", f"- **Choix du Chat** : {c[2]}",
                    f"- **Raison** : {c[3]}", f"- **Comment le défaire** : {c[4]}"]
        out.append("- **Phrases de la loi qui le portent** :")
        out += [f"  - {r}, ligne {l} : {p}" for r, l, p in a_confirmer[i]]
        out.append("")
    if attribuees and textes:
        phrases = {(c[0], c[1], c[2]) for v in attribuees.values() for c in v}
        out += [f"# CE QUE LA LOI VOUS ATTRIBUE — {len(attribuees)} sources, {len(phrases)} phrases ou lignes de table", "",
                "Chaque phrase ci-dessous est marquée « décision de Jean-Luc ». Sous chaque source : ses mots, "
                "copiés tels quels par le programme (jamais réécrits), puis les phrases de la loi qui s'en réclament. "
                "Aucun programme ne peut vérifier que la source dit la phrase : seul un lecteur qui a les deux sous "
                "les yeux le voit. Une phrase qui cite plusieurs sources figure sous chacune.", ""]
        for n, ref in enumerate(sorted(attribuees, key=rang_de_source), 1):
            vues = []
            for c in attribuees[ref]:
                if (c[0], c[1], c[2]) not in vues:
                    vues.append((c[0], c[1], c[2]))
            out.append(f"## A{n}. {ref} — {len(vues)} phrase(s)")
            out.append("- **Les mots de la source** :")
            out += mots_de_la_source(ref, attribuees[ref], textes)
            out.append("- **Les phrases de la loi qui s'en réclament** :")
            out += [f"  - {r}, ligne {l} : {p}" for r, l, p in vues]
            out.append("")
    return "\n".join(out)


def calibrer(textes):
    """Rend 0 si chaque sabotage rougit et chaque témoin reste vert, 1 sinon.

    ① RÔLE — Prouver que le contrôle a des dents, sur des copies en mémoire des vrais textes.
    ② CONTEXTE D'APPEL — `main`, option `--calibrer`.
    ③ ENTRÉE — `textes` : les vrais textes, lus par `main`.
    ④ CONDITIONS D'ENTRÉE — Les vrais textes sont verts (sinon un sabotage ne se distingue pas).
    ⑤ SORTIE — UN code : 0 ou 1.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque cas : copier les textes, appliquer une modification, relancer
      `controler`, comparer au verdict attendu ; pour les cas C8 à C14, la faute attendue doit
      aussi figurer (un rouge pour une autre raison ne compte pas). Cas qui doivent rougir : C1 la
      phrase « Tout le reste est une décision de Jean-Luc » remise dans la première règle NON
      FIGÉE ; C2 un « D18 » sans préfixe ; C3 une décision citée avec une heure fausse ; C4 un
      choix inexistant ; C5 deux genres dans un même crochet ; C6 un choix dont le champ « comment
      le défaire » est vidé ; C7 une ligne de table sans marque ; C8 une décision citée vers n°69,
      entrée de constats « aucune décision de Jean-Luc » (sabotage S1 de la relecture T3) ; C9 vers
      n°93 bis, « vérification faite à 12h45 » ; C10 une ligne D35 fantôme, sans « comment le
      défaire », placée avant la vraie (sabotage S4) ; C11 la ligne Q-G1 écrite deux fois ; C12 un
      titre n°82 ajouté au relevé ; C13 une ligne « Ｄ 35 » (D pleine chasse, espace) ; C14 un titre
      « n°93bis » ajouté au relevé, qui a déjà « n°93 bis ». Témoins qui doivent rester verts :
      T0 les vrais textes ; T1 une phrase marquée ajoutée ; T2 une mention de « D18 » dans le corps
      d'une phrase marquée, préfixée DÉL- ; T3 un choix D99 nouveau, complet, cité par une phrase.
    ⑦ UNITÉ — Des cas.
    ⑧ POURQUOI — Un contrôle qui reste vert quand on retire ce qu'il teste est une décoration
      (instructions du projet, §7) ; le superviseur exige un cas qui doit rougir et un cas qui
      doit passer.
    ⑨ CE QUI CLOCHE — Les sabotages visent la première règle NON FIGÉE et la première ligne de
      table qu'elle porte ; une règle sans table rend C7 sans objet (le cas le dit). C1, C2, C4,
      C5, T1, T2 et T3 ajoutent leur phrase à la fin de la deuxième ligne de cette règle : si cette
      ligne finit par une explication (*Raison*, *Exemple*, *Constat*), la phrase ajoutée n'est pas
      lue et le calibrage le dit (CALIBRAGE ROMPU) — c'est arrivé le 04-11-2026 au tour 4, quand un
      *Constat* a été écrit au bout de cette ligne ; il a été mis sur une ligne à lui.
    ⑩ EFFET — Écrit à l'écran.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    reg = textes["registre"]
    blocs = blocs_non_figes(reg)
    if not blocs:
        print("IMPOSSIBLE : aucune règle NON FIGÉE à saboter")
        return 1
    _, premiere, lignes = blocs[0]
    ouverture = lignes[0]
    ligne2 = lignes[1]
    table = next((x for x in lignes if x.strip().startswith("|") and "[" in x), None)
    m82 = re.search(r"\[DÉCISION JL, (\d\d-\d\d-\d{4}) (\d\dh\d\d), n°(\d+)\]", reg)
    del_vu = re.search(r"\[CHOIX DÉLÉGUÉ (DÉL-D\d+)\]", reg)

    def avec(**k):
        """Rend une copie des textes où les clés données sont remplacées.

        ① RÔLE — Fabriquer un cas sabotage.
        ② CONTEXTE D'APPEL — `calibrer`, une fois par cas.
        ③ ENTRÉE — `k` : {clé des textes : texte remplaçant}.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : un dictionnaire de textes.
          [rend: 1]
        ⑥ TRAITEMENT — copier, puis mettre à jour.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — saboter en mémoire, jamais sur un fichier.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        t = dict(textes)
        t.update(k)
        return t

    def choix_vide(t):
        """Rend le fichier des choix où le champ « comment le défaire » du premier choix cité est vidé.

        ① RÔLE — Fabriquer le sabotage C6.
        ② CONTEXTE D'APPEL — `calibrer`.
        ③ ENTRÉE — `t` : le texte du fichier des choix.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : le texte saboté.
          [rend: 1]
        ⑥ TRAITEMENT — trouver la ligne du premier « DÉL-Dnn » cité par la loi et vider sa dernière case.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — prouver que les quatre champs sont vérifiés (n°129).
        ⑨ CE QUI CLOCHE — si la loi ne cite aucun choix délégué, rien n'est vidé et C6 resterait vert :
          le calibrage le dirait (CALIBRAGE ROMPU).
        ⑩ EFFET — —
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        lignes_c = t.split("\n")
        for n, l in enumerate(lignes_c):
            if del_vu and l.startswith("| " + del_vu.group(1)[4:] + " |"):
                cases = l.strip().strip("|").split("|")
                cases[-1] = " "
                lignes_c[n] = "|" + "|".join(cases) + "|"
        return "\n".join(lignes_c)
    ch = textes["choix"]
    rel = textes["releve"]
    d35 = next((x for x in ch.split("\n") if x.startswith("| D35 |")), None)
    qg1 = next((x for x in ch.split("\n") if x.startswith("| Q-G1 |")), None)
    fantome = "| D35 | 19h49 (04-11) | question fantôme | choix fantôme | raison fantôme | |"
    nouveau = "| D99 | 20h00 (04-11) | question témoin | choix témoin | raison témoin | défaire témoin |"
    cas = [
        ("T0 les vrais textes", False, dict(textes)),
        ("C1 « Tout le reste est une décision de Jean-Luc » remise", True,
         avec(registre=reg.replace(ligne2, ligne2 + " Tout le reste est une décision de Jean-Luc, citée avec sa date et ses mots.", 1))),
        ("C2 « D18 » sans préfixe", True,
         avec(registre=reg.replace(ligne2, ligne2 + " Voir D18 [CHOIX DÉLÉGUÉ DÉL-D18].", 1))),
        ("C3 une décision citée à une heure fausse", True,
         avec(registre=reg.replace(m82.group(0), f"[DÉCISION JL, {m82.group(1)} 23h59, n°{m82.group(3)}]", 1) if m82 else reg + "\n")),
        ("C4 un choix inexistant", True,
         avec(registre=reg.replace(ligne2, ligne2 + " Phrase sabotée [CHOIX DÉLÉGUÉ DÉL-D999].", 1))),
        ("C5 deux genres dans un même crochet", True,
         avec(registre=reg.replace(ligne2, ligne2 + " Phrase sabotée [CHOIX DÉLÉGUÉ DÉL-D13 ; QUESTION OUVERTE Q-G1].", 1))),
        ("C6 un choix sans « comment le défaire »", True, avec(choix=choix_vide(textes["choix"]))),
        ("C7 une ligne de table sans marque", True,
         avec(registre=reg.replace(table, CROCHET.sub("", table), 1) if table else reg + "\n")),
        ("T1 une phrase marquée ajoutée", False,
         avec(registre=reg.replace(ligne2, ligne2 + " Phrase témoin [CHOIX DÉLÉGUÉ DÉL-D13].", 1))),
        ("T2 « DÉL-D18 » cité dans une phrase marquée", False,
         avec(registre=reg.replace(ligne2, ligne2 + " Voir DÉL-D18 pour le jeton [CHOIX DÉLÉGUÉ DÉL-D18].", 1))),
        ("C8 décision citée vers n°69 (constats, « aucune décision de Jean-Luc »)", True,
         avec(registre=reg.replace(m82.group(0), "[DÉCISION JL, 01-11-2026, n°69]", 1) if m82 else reg + "\n"),
         JEAN_LUC_NE_PARLE_PAS),
        ("C9 décision citée vers n°93 bis (vérification du Chat)", True,
         avec(registre=reg.replace(m82.group(0), "[DÉCISION JL, 01-11-2026 12h45, n°93 bis]", 1) if m82 else reg + "\n"),
         JEAN_LUC_NE_PARLE_PAS),
        ("C10 D35 fantôme sans « comment le défaire », avant la vraie", True,
         avec(choix=ch.replace(d35, fantome + "\n" + d35, 1) if d35 else ch + "\n"), EN_DOUBLE),
        ("C11 Q-G1 écrite deux fois", True,
         avec(choix=ch.replace(qg1, qg1 + "\n" + qg1, 1) if qg1 else ch + "\n"), EN_DOUBLE),
        ("C12 un titre n°82 ajouté au relevé", True,
         avec(releve=rel + "\n## n°82 — 01-11-2026 12h32 · Jean-Luc : « 2 »\nsabotage\n"), EN_DOUBLE),
        ("C13 « Ｄ 35 » (D pleine chasse, espace) ajoutée", True,
         avec(choix=ch.replace(d35, d35 + "\n" + d35.replace("| D35 |", "| Ｄ 35 |", 1), 1) if d35 else ch + "\n"),
         EN_DOUBLE),
        ("C14 un titre « n°93bis » ajouté au relevé, qui a « n°93 bis »", True,
         avec(releve=rel + "\n## n°93bis — sabotage\n"), EN_DOUBLE),
        ("T3 un choix D99 nouveau, complet, cité par une phrase", False,
         avec(choix=ch.replace(d35, d35 + "\n" + nouveau, 1) if d35 else ch,
              registre=reg.replace(ligne2, ligne2 + " Phrase témoin [CHOIX DÉLÉGUÉ DÉL-D99].", 1))),
    ]
    faute = False
    for nom, doit_rougir, t, *motif in cas:
        f, _, _, _ = controler(t)
        rouge = bool(f)
        raison = not motif or any(motif[0] in x for x in f)
        ok = rouge == doit_rougir and raison and (t is not textes)
        faute = faute or not ok
        vue = next((x for x in f if motif and motif[0] in x), f[0] if f else "")
        print(f"{'OK ' if ok else 'NON'} {nom} : {'ROUGE' if rouge else 'VERT'} (attendu {'ROUGE' if doit_rougir else 'VERT'}"
              + (f", faute « {motif[0]} »" if motif else "") + ")" + (f" — {vue[:110]}" if f else ""))
    print("CALIBRAGE TENU" if not faute else "CALIBRAGE ROMPU")
    return 1 if faute else 0


def main():
    """Lit les fichiers, contrôle, écrit le verdict et, sur demande, la liste ; sort avec son code.

    ① RÔLE — Point d'entrée en ligne de commande.
    ② CONTEXTE D'APPEL — Lancement du programme.
    ③ ENTRÉE — Les options `--racine`, `--liste`, `--calibrer`.
    ④ CONDITIONS D'ENTRÉE — Les quatre fichiers existent sous la racine (sinon code 2).
    ⑤ SORTIE — Aucune valeur : le programme sort avec 0, 1 ou 2 (voir l'en-tête, ⑤).
      [rend: rien]
    ⑥ TRAITEMENT — Lire ; avec `--calibrer`, calibrer et sortir ; sinon contrôler, écrire le compte
      par genre, les fautes, le nombre de points à confirmer, le nombre de sources et de phrases
      attribuées à Jean-Luc, et la liste si demandée.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit à l'écran ; avec `--liste F`, écrit F.
    ⑪ TERMINAISON — Sort du programme par `sys.exit`.
      [sort: oui]
    """
    p = argparse.ArgumentParser()
    p.add_argument("--racine", default=".")
    p.add_argument("--liste")
    p.add_argument("--calibrer", action="store_true")
    a = p.parse_args()
    textes = {}
    for cle, chemin in (("registre", REGISTRE), ("releve", RELEVE), ("backlog", BACKLOG), ("choix", CHOIX)):
        f = os.path.join(a.racine, chemin)
        if not os.path.isfile(f):
            print(f"IMPOSSIBLE : {chemin} absent sous {a.racine}")
            sys.exit(2)
        with open(f, encoding="utf-8") as h:
            textes[cle] = h.read()
    if a.calibrer:
        sys.exit(calibrer(textes))
    fautes, a_confirmer, compte, attribuees = controler(textes)
    if fautes and fautes[0].startswith("IMPOSSIBLE"):
        print(fautes[0])
        sys.exit(2)
    print("Phrases marquées, par genre : " + " · ".join(f"{g} {n}" for g, n in compte.items()))
    choix, questions = lire_les_choix(textes["choix"])
    print(f"Points à confirmer : {len(a_confirmer)} ("
          + ", ".join(sorted(a_confirmer, key=lambda i: (i[0], int(re.sub(r'\D', '', i))))) + ")")
    phrases = {(c[0], c[1], c[2]) for v in attribuees.values() for c in v}
    print(f"Ce que la loi attribue à Jean-Luc : {len(attribuees)} sources "
          f"({sum(1 for r in attribuees if r.startswith('n°'))} n° du relevé, "
          f"{sum(1 for r in attribuees if r.startswith('A-'))} A-NNN, {sum(1 for r in attribuees if r.startswith('R-'))} R-NNN), "
          f"{len(phrases)} phrases ou lignes de table")
    if a.liste:
        with open(a.liste, "w", encoding="utf-8") as h:
            h.write(ecrire_la_liste(a_confirmer, choix, questions, attribuees, textes) + "\n")
    for f in fautes:
        print("ROUGE  " + f)
    print("VERT — chaque phrase porte une marque, et chaque marque tient contre sa source" if not fautes
          else f"ROUGE — {len(fautes)} faute(s)")
    sys.exit(1 if fautes else 0)


if __name__ == "__main__":
    main()
