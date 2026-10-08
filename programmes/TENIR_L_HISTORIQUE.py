#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TENIR_L_HISTORIQUE.py — Sam 12-09-2026 (Paris)
FABRIQUÉ · Rôle : tenir LE fichier maître des cours — un seul, qui grandit, jamais réécrit.
Quand l'appeler : chaque soir, après la collecte ABC. Jamais à la main.

════════════════════════════════════════════════════════════════════════
POURQUOI CE PROGRAMME — la décision de Jean-Luc, 12-09-2026
════════════════════════════════════════════════════════════════════════
« Il me semble que le plus simple, ce serait d'avoir un seul fichier maître
 effectivement qui grandit. »

AVANT : deux fichiers vivaient côte à côte — `cac40_ohlcv.csv`, l'historique
Google figé au 10-07-2026, et `claude_cours_nouveaux.csv`, l'incrément. Le banc
d'essai (aujourd'hui le juge des stratégies) les fusionnait À LA LECTURE, à chaque exécution. Personne n'écrivait
jamais le maître : `CONSOLIDATION_COURS`, l'outil qui savait le faire, lisait
des exports Google qui n'existent plus depuis le 10-09.

MESURE QUI A PERMIS LA FUSION — faite le 12-09 par GitHub Actions, jamais avant :
**837 séances comparées entre Google et ABC sur leur recouvrement (31-07 → 08-09),
40 valeurs, cinq champs chacune.**
  · LES PRIX SE RACCORDENT : un seul écart sur 3 348 comparaisons de prix —
    BOUYGUES, high du 27-08, 45,74 contre 45,735. Google arrondit à deux
    décimales, ABC en garde trois. Ce n'est pas une divergence, c'est une
    précision. **Une stratégie qui compare J à J-60 ne verra aucun saut.**
  · LES VOLUMES NE SE RACCORDENT PAS TOUJOURS : onze écarts sur 837, toujours
    Google au-dessus. Le pire : VINCI, 05-08, 936 779 contre 864 779 — 72 000
    titres. **L'indicateur CMF — le flux monétaire de Chaikin, qui mesure si l'argent entre
ou sort d'une valeur — se calcule SUR LE VOLUME. **Le raccord entre les deux
fournisseurs de cours est donc visible dans les signaux, et non pas seulement
dans les prix.****
    Cause non tranchée : Google compte peut-être des échanges hors marché, ou
    révise après coup. À trancher le jour où ça pèsera sur une mesure.

════════════════════════════════════════════════════════════════════════
LES QUATRE RÈGLES, ET ELLES NE SE NÉGOCIENT PAS
════════════════════════════════════════════════════════════════════════
① UN SEUL FICHIER : `donnees/cours_maitre.csv`. Il grandit, il n'est jamais
   réécrit ni trié à l'envers. Clé unique (valeur, date).
② HUIT COLONNES : valeur, date, open, high, low, close, volume, source.
   **La huitième est la décision de Jean-Luc du 12-09** : rien ne disait d'où
   venait une ligne, et la question « Google ou ABC ? » revenait sans réponse.
③ LES SOURCES D'ORIGINE NE SONT JAMAIS TOUCHÉES. `cac40_ohlcv.csv` reste au
   dépôt, intact, sous son nom — c'est la référence Google validée contre
   FactSet au centime, vérification du 16-08-2026 (A-229). **On peut toujours s'y référer.**
④ LES RÉVISIONS DU PASSÉ SE DÉTECTENT, ELLES NE SE DEVINENT PAS. ABC rend
   trente séances à chaque passage ; on les compare TOUTES à ce qu'on a déjà.
   Une séance ancienne qui change est signalée, jamais écrasée en silence.
   **Décision laissée ouverte par Jean-Luc le 16-08-2026 (A-231) : « on verra quand le cas se
   produira ». Le voir est maintenant gratuit — la page est déjà téléchargée.**

CE QUE CE PROGRAMME NE FAIT PAS, ET C'EST DIT : il ne tranche RIEN sur une
révision détectée. Il la signale et garde les deux versions sous les yeux.
Prendre la nouvelle ou garder l'ancienne est une décision de Jean-Luc — trancher entre l'ancienne valeur et la nouvelle appartient à Jean-Luc (A-231),
et elle touche la reproductibilité des chiffres de référence figés.

════════════════════════════════════════════════════════════════════════
LES ONZE ÉLÉMENTS — ce programme est une fonction comme les autres
════════════════════════════════════════════════════════════════════════
Un programme reçoit une ligne de commande là où une fonction reçoit des
paramètres, et rend un code de sortie là où elle rend une valeur. **Ce sont les
mêmes natures sous d'autres noms : les onze éléments s'appliquent tels quels.**

① RÔLE — **LE PAS DU VERSEMENT.** La collecte du soir écrit les séances du jour
  dans un fichier d'arrivée ; ce programme les verse dans le fichier maître, qui
  grandit et n'est jamais réécrit. **Sans lui, le détecteur calcule sur la veille
  et tout reste vert** — c'est arrivé du 12 au 14-09-2026, trois soirs de suite,
  parce qu'aucun pas du circuit ne l'appelait.
② CONTEXTE D'APPEL — Le circuit du soir, pas n°4, entre « commiter la collecte »
  et « contrôler les valeurs ». **Ce pas n'a pas de tolérance à l'échec : s'il
  tombe, le passage rougit.** Jamais lancé à la main en dehors d'une
  vérification.
③ ENTRÉE — La ligne de commande : la racine du dépôt, `--verifier` pour ne rien
  écrire, et `--premier-remplissage` pour autoriser la création du maître quand il
  n'existe pas, et `--increment CHEMIN` pour verser un autre fichier que
  l'incrément du soir (ajouté le 24-09-2026 pour combler le trou de juillet,
  A-473). **Et trois fichiers** : `donnees/cours_maitre.csv` (le maître),
  `donnees/cac40_ohlcv.csv` (le passé Google : lu au premier remplissage, et
  chaque soir pour vérifier qu'aucune de ses séances n'a disparu du maître),
  `donnees/claude_cours_nouveaux.csv` (l'incrément du soir).
④ CONDITIONS D'ENTRÉE — La racine doit exister, et être un dépôt git : la version
  enregistrée du maître y est relue. **Le maître doit exister** — sans
  `--premier-remplissage`, son absence arrête le programme depuis le 24-09-2026
  (A-442). **L'historique Google doit exister aussi.** L'incrément doit porter
  au moins une ligne — un incrément vide arrête le programme. **Chaque ligne doit
  passer `juger_la_ligne`** (depuis le 24-09-2026) : source admise, date lisible
  d'un jour de semaine passé, valeur du référentiel, cours possibles. Trois
  programmes doivent être à côté : `CONTRATS_DES_FICHIERS.py`, qui déclare les
  sources admises, `CONTROLER_LES_COURS.py`, le juge des cours, et `COMMUN.py`,
  qui choisit le référentiel.
⑤ SORTIE — **Un code de sortie, et rien d'autre.** Tout le reste passe par
  l'affichage : le bilan, les alertes, le rapport des révisions.
⑥ TRAITEMENT — ① charger le maître · ② s'il est vide, le remplir avec tout le
  passé Google · ③ charger l'incrément, et s'arrêter s'il est vide · ④ ajouter
  les séances absentes, comparer les séances déjà présentes · ⑤ si une séance a
  changé, écrire le rapport et s'arrêter sans toucher au maître · ⑥ sinon,
  réécrire le maître trié et afficher le bilan.
⑦ UNITÉ — Prix en euros, volume en titres, dates au format AAAA-MM-JJ.
  **Les comptes affichés sont des nombres de LIGNES, jamais de séances** : une
  séance porte autant de lignes qu'il y a de valeurs.
⑧ POURQUOI — Les quatre règles ci-dessus, et trois arrêts délibérés : l'incrément
  vide, la révision détectée, et la vérification qui n'écrit rien.
  **Chacun répare un silence mesuré. Le plus coûteux : du 12 au 14-09-2026, ce
  programme n'était appelé par aucun pas du circuit du soir. Les cours du jour
  étaient collectés, écrits dans `donnees/claude_cours_nouveaux.csv`, et jamais
  versés dans `donnees/cours_maitre.csv`. Le détecteur calculait donc ses signaux
  sur la veille — trois soirs de suite, avec un passage entièrement vert.**
⑨ CE QUI CLOCHE — **Quatre silences, tous inscrits au BACKLOG, sous l'action A-424 du 19-09-2026, aucun corrigé ici :**
  corriger ferait bouger le code pendant qu'on le documente.
  · l'écriture du maître n'est pas atomique — une interruption le laisse tronqué ;
    **depuis le 24-09-2026 (A-442), le passage suivant le détecte et s'arrête**,
    mais l'écriture elle-même reste non atomique ;
  · `source_de` rend le même repli pour une colonne absente et pour une colonne
    vide — un maître à sept colonnes passerait entièrement en « ? » sans un mot ;
  · `lire` rend une liste vide pour « fichier absent » et pour « fichier vide » ;
  · `cle_valeur` traite le cas Unibail par une énumération d'un seul élément.
⑩ EFFET — **RÉÉCRIT `donnees/cours_maitre.csv` EN ENTIER**, trié · **crée
  `rapports/`** s'il manque et y écrit `revisions_du_passe.csv` · **change le
  dossier de travail du processus**, ce qui rend tous les chemins relatifs à la
  racine passée · **jette silencieusement toute colonne absente des huit
  déclarées** — une colonne ajoutée en amont disparaîtrait sans un mot.
⑪ TERMINAISON — **NE REND JAMAIS LA MAIN : tous les chemins terminent.**
  0 = versement fait, ou vérification · 1 = incrément vide, révision détectée,
  ligne refusée par `juger_la_ligne`, ou référentiel illisible, et dans ces cas
  RIEN n'est écrit au maître · 2 = aucun argument, ou
  `--increment` sans chemin.
  **Un code non nul arrête la chaîne du soir : pas de signaux, pas de positions,
  pas de mesure.**

USAGE : python3 TENIR_L_HISTORIQUE.py <racine> [--verifier] [--premier-remplissage] [--increment CHEMIN]
CODE : 0 = écrit · 1 = révision détectée, rien écrit · 2 = source illisible

⑫ DÉFINITIONS —
  le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
  CMF : le flux monétaire de Chaikin, qui mesure si l'argent entre ou sort d'une valeur ; sans unité, borné à ±1.
  le maître : `donnees/cours_maitre.csv`, le fichier unique qui porte tout
    l'historique des cours et n'est jamais réécrit.
  l'incrément : `donnees/claude_cours_nouveaux.csv`, où la collecte écrit les cours du jour avant leur versement au fichier maître.
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub
    Actions — collecte, versement, signaux, positions, mesure, surveillance.
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
  le détecteur : programmes/DETECTER_LES_SIGNAUX_GITHUB.py, qui écrit les signaux du jour
  un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré rejoué à l'identique pour vérifier qu'il n'est pas revenu.
  une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
"""

import csv, math, os, sys
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CONTRATS_DES_FICHIERS import SOURCES_ADMISES     # déclarées une fois (R-708)
from CONTROLER_LES_COURS import controler_une_seance    # LE juge des cours, le même que la collecte (R-708)
from COMMUN import le_plus_recent                       # le même choix de référentiel que la collecte
from COLLECTER_ABC_GITHUB import HEURE_CLOTURE_PARIS    # l'heure où la séance du jour est complète
from CONTRATS_DES_FICHIERS import COURS_MAITRE, COURS_NOUVEAUX
import bisect, re

PRIX_ECRIT = re.compile(r"(0|[1-9][0-9]*)(\.[0-9]+)?")  # « 45.9 », « 35 » — comme le maître
VOLUME_ECRIT = re.compile(r"[1-9][0-9]*")                 # « 487319 », sans zéro de tête
# UN FICHIER VERSÉ À LA MAIN SE RACCORDE AU MAÎTRE, pas à lui-même. Mesures du 24-09-2026
# sur les 27 213 lignes du maître :
#   · chacun des quatre prix d'une séance, rapporté à la clôture de la veille ou du
#     lendemain : de 0,701 à 1,414 ; clôture contre clôture à 15 séances d'écart, la
#     taille du trou de juillet : de 0,665 à 1,532 → bande [0,6 ; 1,67] ;
#   · le volume d'une séance, rapporté à la médiane des volumes de sa valeur : de
#     0,085 à 15,6 → bande [0,02 ; 50] (un volume ×61 entrait sous [0,01 ; 100]).
# Relecture de l'agent indépendant du Chat, 24-09-2026 : un cours ×100, un plus haut
# ×100, un volume ×10⁶ et deux marches de ×1,9 enchaînées dans le même fichier entraient.
RAPPORT_VOISIN = (0.6, 1.67)
RAPPORT_VOLUME = (0.02, 50.0)

PARIS = ZoneInfo("Europe/Paris")
MAITRE = os.path.join("donnees", "cours_maitre.csv")
# LES COLONNES DU MAÎTRE VIENNENT DU CONTRAT (R-708 : deux implémentations d'une même
# chose divergent toujours). Jusqu'au 28-09-2026 elles étaient recopiées ici, à
# l'identique ; une colonne ajoutée au contrat aurait été perdue ici sans un mot.
COLONNES = list(COURS_MAITRE)

# Les deux sources d'origine, et la date où l'une passe le relais à l'autre.
# Le 09-09-2026 est le premier jour collecté par GitHub Actions chez ABC.
HISTORIQUE_GOOGLE = os.path.join("donnees", "cac40_ohlcv.csv")
INCREMENT = os.path.join("donnees", "claude_cours_nouveaux.csv")
BASCULE_ABC = SOURCES_ADMISES["abc"][0]   # le 2026-09-09, déclaré une fois dans les contrats


def cle_valeur(nom):
    """Rapproche les graphies — « AIR LIQUIDE » et « AIR_LIQUIDE » sont la même.

    Recopie la règle de JUGE_DES_STRATEGIES, qui porte son propre motif : « sans cela,
    26 % d'une mesure se perd EN SILENCE » — mesuré le 23-08-2026 sur Bureau Veritas et Unibail (A-264).
    La règle d'un seul endroit (R-708) voudrait qu'on l'importe ; ce programme doit tourner seul dans une
    tâche GitHub sans dépendance, et la règle tient en deux lignes. **Si elle
    change dans JUGE_DES_STRATEGIES, elle doit changer ici — c'est le prix, et il est dit.**

    ① RÔLE — Donner à une même valeur une seule écriture, pour que deux lignes
      venues de deux sources se reconnaissent.
    ② CONTEXTE D APPEL — `main`, cinq fois : au chargement du maître, du passé
      Google, de l incrément, puis au tri et au compte final.
    ③ ENTRÉE — `nom` : le nom d une valeur tel qu écrit dans un fichier de cours.
    ④ CONDITIONS D ENTRÉE — Aucune : accepte n importe quelle chaîne.
    ⑤ SORTIE — UNE valeur : le nom en majuscules, espaces et tirets remplacés par
      des tirets bas, **et `WESTFIELD` retiré quand le nom est celui d Unibail**.
      [rend: 1]
    ⑥ TRAITEMENT — ① majuscules · ② tirets et tirets bas deviennent des espaces ·
      ③ découper puis rejoindre par un tiret bas, ce qui écrase les espaces
      multiples · ④ un cas particulier : Unibail-Rodamco-Westfield devient
      Unibail-Rodamco.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — **DEUX GESTES DISTINCTS, et ils ne servent pas la même chose.**
      **① LES SÉPARATEURS.** La même entreprise s'écrit `UNIBAIL-RODAMCO-WESTFIELD`
      dans un fichier de cours et `UNIBAIL_RODAMCO_WESTFIELD` dans un autre.
      Tirets et tirets bas sont ramenés au même, **et cela suffit à rapprocher ces
      deux écritures-là.** Le 23-08-2026, l absence d un tel rapprochement a fait
      disparaître 26 % des lignes d une mesure, sans aucune erreur affichée.
      **② LE RACCOURCISSEMENT D UNIBAIL, ligne écrite à la main.** Elle ne
      rapproche rien : les deux écritures ci-dessus donnent déjà
      `UNIBAIL_RODAMCO_WESTFIELD` après ①. **Elle RETIRE « WESTFIELD »**, pour que
      la clé corresponde à `UNIBAIL_RODAMCO`, l écriture employée par
      `donnees/cac40_strategies.csv` et par
      `programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py`.
    ⑨ CE QUI CLOCHE — **La ligne Unibail est un raccourcissement écrit à la main,
      qui ne vaut que pour cette valeur.** Elle existe parce que les fichiers de
      cours portent le nom complet et le registre des stratégies le nom court.
      **Si une autre société était nommée différemment entre ces deux fichiers, il
      faudrait une ligne de plus — et rien ne le signalerait : la valeur serait
      simplement absente des mesures.**
      **Mesuré le 20-09-2026 : sans cette ligne, `UNIBAIL-RODAMCO-WESTFIELD` et
      `UNIBAIL_RODAMCO_WESTFIELD` donnent tous deux `UNIBAIL_RODAMCO_WESTFIELD`.
      Les séparateurs suffisent à les rapprocher ; c est avec `UNIBAIL_RODAMCO`
      du registre que le raccord manquerait.**
    ⑩ EFFET — Aucun.

    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS —
      l'incrément : `donnees/claude_cours_nouveaux.csv`, où la collecte écrit les
        cours du jour avant leur versement au fichier maître.
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
      le registre : gouvernance/REGISTRE_REGLES.md, le document qui porte les regles numerotees du projet ; une regle absente du registre n'existe pas
      le registre des stratégies : le fichier `cac40_strategies.csv`, une ligne par stratégie, qui porte leur état civil — identifiant, réglages, résultats connus
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    n = "_".join(nom.strip().upper().replace("-", " ").replace("_", " ").split())
    return n.replace("UNIBAIL_RODAMCO_WESTFIELD", "UNIBAIL_RODAMCO")


def lire(chemin):
    """Lit un fichier de cours et rend ses lignes datées.

    ① RÔLE — Seul point de lecture des trois fichiers de cours de ce programme :
      le maître, l historique Google, l incrément du soir. Tout ce qui entre ici
      vient d un disque ; rien n est calculé.
    ② CONTEXTE D APPEL — `main` l appelle trois fois, toujours au début.
    ③ ENTRÉE — `chemin` : un chemin de fichier CSV, relatif à la racine du dépôt.
      Les trois valeurs réellement passées sont `donnees/cours_maitre.csv`,
      `donnees/cac40_ohlcv.csv`, `donnees/claude_cours_nouveaux.csv`.
    ④ CONDITIONS D ENTRÉE — Aucune. Un chemin inexistant est un cas prévu.
    ⑤ SORTIE — UNE valeur : la liste des lignes, chacune un dictionnaire dont les
      clés sont les colonnes du CSV. **Les lignes sans colonne `date`, ou dont la
      date est vide, sont ÉCARTÉES SANS MOT.**
      [rend: 1]
    ⑥ TRAITEMENT — ① si le fichier n existe pas, rendre la liste vide · ② sinon,
      l ouvrir en ignorant le marqueur d encodage en tête · ③ ne garder que les
      lignes portant une date.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — L encodage `utf-8-sig` vient d un fait mesuré : les fichiers
      produits sous Windows portent trois octets invisibles en tête, et sans
      cette lecture la PREMIÈRE COLONNE devient introuvable — donc tout le
      fichier est rejeté, sans erreur.
    ⑨ CE QUI CLOCHE — **Une liste vide veut dire DEUX choses : le fichier n'existe
      pas, ou il existe et ne porte aucune ligne datée.**
      **Concrètement** : si `donnees/claude_cours_nouveaux.csv` est effacé, la
      fonction rend une liste vide · s'il existe mais que la collecte n'y a rien
      écrit, elle rend aussi une liste vide. **Le premier cas est une panne, le
      second une soirée sans cours neufs — et l'appelant réagit pareil aux deux.**
      C'est le cas qui a fondé cet élément de la méthode, relevé le 17-09-2026.
    ⑩ EFFET — Aucun : elle ouvre en lecture, n écrit rien, ne crée rien.
    ⑪ TERMINAISON — Rend toujours la main. Aucun de ses appels ne termine le
      [sort: non]
    ⑫ DÉFINITIONS —
      le maître : `donnees/cours_maitre.csv`, le fichier unique qui porte tout
        l'historique des cours et n'est jamais réécrit.
      l'incrément : `donnees/claude_cours_nouveaux.csv`, où la collecte écrit les cours du jour avant leur versement au fichier maître.
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if not os.path.isfile(chemin):
        return []
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f) if r.get("date")]


def source_de(ligne, defaut):
    """Dit d où vient une ligne de cours déjà enregistrée.

    ① RÔLE — Nommer la provenance d une ligne — `google`, `abc` ou `euronext` —
      pour l écrire au maître quand la ligne y entre, et dans le rapport des
      révisions du passé. C est ce qui permet de savoir QUI a fourni une séance.
    ② CONTEXTE D APPEL — `main`, deux fois : quand une ligne de l incrément du
      SOIR entre au maître, et à la ligne du rapport de révision, quand une séance
      déjà enregistrée a changé. **Pas pour `--increment`** : sa case source se lit
      telle qu'elle est écrite, sans repli (cassure de Cowork, 24-09-2026 23h39).
    ③ ENTRÉE — `ligne` : une ligne du maître ou de l incrément · `defaut` : la
      valeur à rendre si la provenance manque. **Deux appelants : le versement
      passe la source que dit la date, le rapport des révisions passe `'?'`.**
    ④ CONDITIONS D ENTRÉE — Aucune : une ligne sans colonne `source` est un cas
      prévu.
    ⑤ SORTIE — UNE valeur : la provenance, ou `defaut`.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire la colonne `source` · ② retirer les espaces de bord ·
      ③ si le résultat est vide, rendre `defaut`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les cours viennent de deux fournisseurs successifs : Google
      jusqu'au 10-09-2026, ABC Bourse depuis. **Les prix des deux se raccordent
      sans écart, mais les VOLUMES diffèrent sur onze séances parmi 837.** Or
      l'indicateur CMF se calcule sur le volume : un écart de volume change un
      signal. **La huitième colonne dit donc, pour chaque ligne, de quel
      fournisseur elle vient — sans quoi on ne peut pas juger si un écart est une
      erreur ou une simple couture entre deux sources.**
    ⑨ CE QUI CLOCHE — **Une colonne ABSENTE et une colonne VIDE rendent toutes
      deux le repli `'?'`, et rien ne les distingue.** Un fichier maître à sept colonnes au lieu de huit passerait
      entièrement en `'?'` sans un mot — et le rapport des révisions dirait
      `?=12.34` sur chaque ligne, ce qui se lit comme une donnée manquante
      ponctuelle et non comme un fichier entier dont la structure a changé.
    ⑩ EFFET — Aucun : elle ne modifie ni la ligne reçue ni rien d autre.

    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS —
      CMF : le flux monétaire de Chaikin, qui mesure si l'argent entre ou sort d'une
        valeur ; sans unité, borné à ±1.
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    return (ligne.get("source") or "").strip() or defaut


def ecrire_l_alerte(raison, details):
    """Dépose l'alerte du fichier maître, pour que Jean-Luc décide lui-même de la réparation.

    ① RÔLE — Écrire `rapports/ALERTE_FICHIER_MAITRE.md` quand le versement s'arrête parce que le
      fichier maître des cours est absent, vide, a rétréci, ou n'a pas pu être contrôlé : ce qui
      s'est passé, et la question posée à Jean-Luc, avec ses trois réponses.
    ② CONTEXTE D'APPEL — Depuis `main`, juste avant chacun de ses arrêts sur le fichier maître.
      Le circuit du soir dépose ensuite ce fichier dans le dépôt ; la tâche du soir de Cowork, à
      23h, le lit et prévient Jean-Luc.
    ③ ENTRÉE — `raison` : une phrase qui dit ce qui s'est passé · `details` : une liste de lignes
      qui le précisent, par exemple les couples valeur-séance disparus.
    ④ CONDITIONS D'ENTRÉE — Le dossier courant est la racine du dépôt : `main` s'y est placé.
    ⑤ SORTIE — Rend `None`.
      [rend: rien]
    ⑥ TRAITEMENT — ① créer le dossier `rapports` s'il manque · ② écrire le fichier d'alerte, qui
      remplace un éventuel fichier précédent · ③ dire à l'écran où il est écrit.
    ⑦ UNITÉ — Aucune.
    ⑧ POURQUOI — **Décision de Jean-Luc du 24-09-2026** : quand le fichier maître a un problème,
      rien ne se répare tout seul ; le système doit dire pourquoi il a échoué et lui demander s'il
      veut reprendre la version de la veille, reconstruire, ou rien toucher. Ses mots : *« Je veux
      qu'il me pose la question […] qu'il ne fasse pas tout seul. »* Et l'alerte doit passer par
      Cowork, dont la tâche du soir le prévient déjà à chaque passage.
    ⑨ CE QUI CLOCHE — Rien de relevé. Le rangement de l'alerte une fois le problème résolu n'est
      pas fait ici : c'est l'étape du versement du circuit du soir qui, quand le versement réussit,
      range l'alerte aux archives sous un nom qui dit « résolue le … » — cassure de Cowork du
      24-09-2026 : avant, l'alerte restait au dépôt pour toujours.
    ⑩ EFFET — ÉCRIT `rapports/ALERTE_FICHIER_MAITRE.md`, et affiche une ligne.
    ⑪ TERMINAISON — Rend la main. Peut lever si le dossier `rapports` ne peut pas être créé ou
      écrit.
      [sort: non]
    ⑫ DÉFINITIONS
      le fichier maître : `donnees/cours_maitre.csv`, l'historique officiel des cours, auquel on
        ajoute chaque soir la séance du jour.
    """
    maintenant = datetime.now(ZoneInfo("Europe/Paris"))
    os.makedirs("rapports", exist_ok=True)
    chemin = os.path.join("rapports", "ALERTE_FICHIER_MAITRE.md")
    lignes = [
        f"# ALERTE — LE FICHIER MAÎTRE DES COURS — {maintenant.strftime('%d-%m-%Y %Hh%M')} (Paris)",
        "",
        f"**Ce qui s'est passé** : {raison}",
        "",
        *[f"- {d}" for d in details],
        "",
        "**Rien n'a été réparé automatiquement** — décision de Jean-Luc du 24-09-2026 (A-442). "
        "Le circuit du soir s'est arrêté au versement : ni signaux, ni positions, ni mesures ce soir.",
        "",
        "## LA QUESTION POUR JEAN-LUC — répondre A, B ou C, à Cowork ou au Chat",
        "",
        "- **A — reprendre le fichier maître de la veille**, enregistré dans le dépôt. "
        "Recommandé : une copie exacte, rien de mélangé.",
        "- **B — le reconstruire** à partir de l'historique Google figé, `donnees/cac40_ohlcv.csv`, "
        "et des arrivées ABC, `donnees/claude_cours_nouveaux.csv`. Une reconstruction qui perdrait "
        "des séances enregistrées — par exemple les 406 d'Euronext du trou de juillet — est refusée : "
        "il faudrait les reverser ensuite par `--increment`.",
        "- **C — ne rien toucher**, et chercher d'abord pourquoi c'est arrivé.",
        "",
        "En cas d'urgence, après A ou B, relancer le circuit du jour depuis GitHub (« Run workflow »).",
        "Dès que le versement du soir réussit de nouveau, ce fichier est rangé aux archives "
        "automatiquement, sous un nom qui dit « résolue le … » ; tant qu'il est là, la tâche du soir "
        "de Cowork alerte.",
    ]
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")
    print(f"  alerte écrite : {chemin}")


def lire_l_increment(chemin, par_increment):
    """Lit le fichier à verser, sans rien écarter en silence, ou dit pourquoi il ne se lit pas.

    ① RÔLE — Donner au versement TOUTES les lignes du fichier à verser, ou un motif
      d'arrêt clair. `lire` écarte une ligne sans date ; ici, rien ne s'écarte : une
      ligne sans date doit être refusée par `juger_la_ligne`, pas disparaître.
    ② CONTEXTE D'APPEL — `main`, une fois, avant tout jugement.
    ③ ENTRÉE — `chemin` : le fichier à verser · `par_increment` : vrai quand il vient
      de l'option `--increment`, faux pour l'incrément du soir.
    ④ CONDITIONS D'ENTRÉE — Aucune : un fichier absent est un motif.
    ⑤ SORTIE — DEUX valeurs : la liste des lignes, et le motif d'arrêt, vide si le
      fichier se lit.
      [rend: 2]
    ⑥ TRAITEMENT — ① refuser un fichier absent · ② le lire en UTF-8, marque d'ordre
      des octets admise, et refuser un autre encodage · ③ exiger l'en-tête EXACT d'un
      contrat de `programmes/CONTRATS_DES_FICHIERS.py` : les huit colonnes du maître
      pour `--increment`, qui doit dire sa source ; les sept de la collecte, et elles
      seules, pour l'incrément du soir · ④ rendre toutes les lignes.
    ⑦ UNITÉ — Des lignes.
    ⑧ POURQUOI — Relecture de l'agent indépendant du Chat, 24-09-2026 : une ligne
      sans date disparaissait en code 0 ; un fichier Latin-1 ou UTF-16 faisait
      tomber le programme sans un mot ; un en-tête « VALEUR » le faisait tomber sur
      une clé absente ; un fichier absent ou séparé par des points-virgules était
      annoncé « vide », avec « la collecte du soir a probablement échoué ». Et un
      fichier versé à la main sans colonne source recevait « google » d'après sa
      date, quelle que soit son origine.
    ⑨ CE QUI CLOCHE — Rien de relevé.
    ⑩ EFFET — Lit le fichier ; n'écrit rien.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    if not os.path.isfile(chemin):
        return [], f"{chemin} est introuvable."
    try:
        with open(chemin, encoding="utf-8-sig", newline="") as f:
            lecteur = csv.DictReader(f)
            entete = lecteur.fieldnames or []
            lignes = list(lecteur)
    except UnicodeDecodeError as e:
        return [], f"{chemin} n'est pas écrit en UTF-8 : {e}"
    # Le soir, SEPT colonnes et rien d autre : un fichier du soir à huit colonnes
    # porterait sa propre source et entrerait sans aucun raccord (agent indépendant,
    # 24-09-2026). Ce qui porte une source passe par `--increment`.
    admis = [COURS_MAITRE] if par_increment else [COURS_NOUVEAUX]
    if entete not in admis:
        return [], (f"en-tête inattendu dans {chemin} : {','.join(entete) or '(aucun)'} — "
                    f"attendu : {' ou '.join(','.join(c) for c in admis)}")
    return lignes, ""


def juger_la_ligne(r, src, aujourd_hui, connues, premiere, voisinage, par_increment,
                   heure=None):
    """Dit tout ce qui empêche une ligne du fichier à verser d'entrer au fichier maître.

    ① RÔLE — Juger une ligne ENTIÈRE avant qu'elle entre au maître : sa forme, sa
      source, sa date, sa valeur, l'écriture de ses nombres et ses cours. Une seule
      fonction pour toute la ligne, parce que réparer champ par champ laissait passer
      le champ suivant — trois tours de relecture de Cowork le 24-09-2026 (la source,
      puis la date, puis les cours), puis la relecture de l'agent indépendant du Chat.
    ② CONTEXTE D'APPEL — `main`, une fois par ligne du fichier à verser, avant tout
      ajout.
    ③ ENTRÉE — `r` : la ligne · `src` : la source retenue pour elle · `aujourd_hui` :
      la date du jour à Paris, AAAA-MM-JJ · `connues` : les valeurs du référentiel,
      rapprochées par `cle_valeur` · `premiere` : la première date du maître ·
      `voisinage` : ce que le MAÎTRE sait de cette valeur, un dictionnaire aux clés
      `debut` (sa première séance), `veille` et `lendemain` (les clôtures du maître
      qui encadrent la date, ou `None`), `mediane_volume` et `graphies` (les noms
      sous lesquels le maître l'écrit) · `par_increment` : vrai pour `--increment` ·
      `heure` : l'heure de Paris, prise à l'horloge quand elle n'est pas donnée.
    ④ CONDITIONS D'ENTRÉE — Aucune : un champ absent est un motif de refus.
    ⑤ SORTIE — DEUX valeurs : la liste des motifs de refus, vide si la ligne peut
      entrer, et l'alerte du juge des cours, vide s'il n'en a pas.
      [rend: 2]
    ⑥ TRAITEMENT — ① autant de champs que l'en-tête · ② un nom sans espace de bord ·
      ③ une source non vide, sans espace de bord, admise, dans sa période · ④ une date qui se lit AAAA-MM-JJ et se
      réécrit à l'identique, un jour de semaine, ni avant la première séance du
      maître, ni après aujourd'hui, ni aujourd'hui avant l'heure de clôture · ⑤ une
      valeur du référentiel · ⑥ des prix écrits comme au maître, chiffres et point, et
      un volume en chiffres · ⑦ les cours jugés par `controler_une_seance` de
      `programmes/CONTROLER_LES_COURS.py`, le juge de la collecte : « BLOQUANT » est un
      refus, « ALERTE » est rendue · ⑧ pour `--increment` seulement : la valeur a
      déjà une séance au maître avant cette date, le nom est l'une de ses graphies au
      maître, chacun des quatre prix se raccorde aux clôtures du maître qui encadrent
      la date, dans `RAPPORT_VOISIN`, et le volume à la médiane de la valeur, dans
      `RAPPORT_VOLUME`. Le raccord se fait au maître et jamais au fichier lui-même :
      deux lignes fausses ne se valident pas l'une l'autre.
    ⑦ UNITÉ — Prix en euros, volume en titres, dates AAAA-MM-JJ, heure de Paris.
    ⑧ POURQUOI — Le juge des cours existait déjà ; en écrire un second aurait fait
      deux juges qui divergeraient un jour (R-708). Ce qu'il ne regarde pas est jugé
      ici, parce que seul ce programme reçoit des lignes d'ailleurs que de la collecte.
      Le raccord au maître ne s'applique qu'à `--increment` : le soir, une vraie
      séance peut chuter de 25 % sur un résultat, et le juge des cours ne fait qu'alerter.
    ⑨ CE QUI CLOCHE — Un jour férié de semaine, comme le 25-12, est accepté : aucun
      calendrier de la bourse n'existe au dépôt. Un nom écrit autrement que dans le
      maître — casse, tiret bas — est accepté le soir s'il se rapproche d'une valeur
      connue : c'est A-474. Par `--increment`, une vraie séance hors des bandes — une
      chute de plus de 40 %, une division d'action — est refusée : c'est voulu, un
      fichier versé à la main qui s'écarte à ce point attend la décision de Jean-Luc.
      **Les bandes arrêtent les erreurs GROSSIÈRES — unité, virgule, ×100 — jamais une
      erreur PLAUSIBLE** : deux valeurs aux cours voisins échangées, ou tous les prix
      ×1,6 entrent (agent indépendant, 24-09-2026). Seul un calibrage sur une seconde
      source prouve qu'un cours est vrai : c'est ce que fait
      `programmes/COMBLER_LE_TROU_DEPUIS_EURONEXT.py` avant d'écrire son témoin.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main ; `controler_une_seance` ne lève pas.
      [sort: non]
    """
    ici = f"{r.get('valeur')};{r.get('date')}"
    motifs = []
    if None in r or any(v is None for v in r.values()):
        motifs.append(f"{ici} : nombre de champs différent de l'en-tête")
    nom = r.get("valeur") or ""
    if nom != nom.strip():
        motifs.append(f"{ici} : nom de valeur entouré d'espaces")
    date = r.get("date") or ""
    if not src:
        motifs.append(f"{ici} : case source vide — un fichier versé par --increment dit d'où vient chaque ligne")
    elif src != src.strip():
        motifs.append(f"{ici} : source entourée d'espaces")
    elif src not in SOURCES_ADMISES:
        motifs.append(f"{ici} : source « {src} » non admise — admises : {', '.join(SOURCES_ADMISES)}")
    else:
        debut, fin = SOURCES_ADMISES[src]
        if (debut and date < debut) or (fin and date > fin):
            motifs.append(f"{ici} : la source « {src} » ne couvre que {debut or 'le début'} → "
                          f"{fin or 'aujourd hui'}")
    try:
        jour = datetime.strptime(date, "%Y-%m-%d")
        lisible = jour.strftime("%Y-%m-%d") == date
    except (ValueError, TypeError):
        lisible = False
    if heure is None:
        heure = datetime.now(PARIS).hour
    if not lisible:
        motifs.append(f"{ici} : date illisible — format attendu AAAA-MM-JJ")
    elif jour.weekday() >= 5:
        motifs.append(f"{ici} : un {('samedi', 'dimanche')[jour.weekday() - 5]}, jour sans séance")
    elif date > aujourd_hui:
        motifs.append(f"{ici} : séance postérieure au jour ({aujourd_hui})")
    elif date == aujourd_hui and heure < HEURE_CLOTURE_PARIS:
        motifs.append(f"{ici} : séance du jour avant la clôture ({HEURE_CLOTURE_PARIS} h, Paris)")
    elif premiere and date < premiere:
        motifs.append(f"{ici} : antérieure à la première séance du maître ({premiere}) — "
                      f"étendre l'historique vers le passé est une décision de Jean-Luc")
    if cle_valeur(nom) not in connues:
        motifs.append(f"{ici} : valeur inconnue du référentiel")
    for champ in ("open", "high", "low", "close", "volume"):
        texte = r.get(champ) or ""
        forme = VOLUME_ECRIT if champ == "volume" else PRIX_ECRIT
        if texte and not forme.fullmatch(texte):
            motifs.append(f"{ici} : {champ} « {texte} » n'est pas écrit comme au maître — "
                          f"{'des chiffres' if champ == 'volume' else 'des chiffres et un point'}")
    veille = voisinage.get("veille")
    seance = dict(r) if veille is None else dict(r, close_precedent=veille)
    verdict, motif = controler_une_seance(seance)
    if verdict == "BLOQUANT":
        motifs.append(f"{ici} : cours impossibles — {motif}")
    if par_increment:
        debut = voisinage.get("debut")
        if not debut or date < debut:
            motifs.append(f"{ici} : la valeur n'a pas encore de séance au maître avant cette date "
                          f"(première : {debut or 'aucune'}) — étendre son historique vers le passé "
                          f"est une décision de Jean-Luc")
        if nom not in voisinage.get("graphies", ()):
            motifs.append(f"{ici} : nom « {nom} » inconnu du maître pour cette valeur — il l'écrit "
                          f"{' ou '.join(sorted(voisinage.get('graphies', ()))) or 'nulle part'}")
        if not motifs:
            for quand, n in (("la veille", veille), ("le lendemain", voisinage.get("lendemain"))):
                for champ in ("open", "high", "low", "close"):
                    if n and not RAPPORT_VOISIN[0] <= float(r[champ]) / n <= RAPPORT_VOISIN[1]:
                        motifs.append(f"{ici} : {champ} {r[champ]} contre une clôture de {n} {quand} "
                                      f"au maître — rapport {float(r[champ]) / n:.3g}, hors de "
                                      f"[{RAPPORT_VOISIN[0]} ; {RAPPORT_VOISIN[1]}]")
            med = voisinage.get("mediane_volume")
            if med and not RAPPORT_VOLUME[0] <= float(r["volume"]) / med <= RAPPORT_VOLUME[1]:
                motifs.append(f"{ici} : volume {r['volume']} contre une médiane de {med:g} pour cette "
                              f"valeur — rapport {float(r['volume']) / med:.3g}, hors de "
                              f"[{RAPPORT_VOLUME[0]} ; {RAPPORT_VOLUME[1]}]")
    return motifs, (motif if verdict == "ALERTE" else "")


def main():
    """Verse les séances du jour dans le fichier maître des cours.

    ① RÔLE — **Le pas du VERSEMENT, entre la collecte et la détection.** La
      collecte écrit les séances du jour dans un fichier d arrivée ; ce
      programme les ajoute au fichier maître, qui grandit et n est jamais
      réécrit. **Sans ce pas, le détecteur calcule sur la veille et tout reste
      vert** — c est arrivé du 12 au 14-09-2026, trois soirs de suite.
    ② CONTEXTE D APPEL — Le circuit du soir, pas n°4, entre « commiter la
      collecte » et « contrôler les valeurs ». Ce pas n a PAS de tolérance à
      l échec : s il tombe, le passage rougit.
    ③ ENTRÉE — La ligne de commande. `sys.argv[1]` : la racine du dépôt — le
      workflow passe `$GITHUB_WORKSPACE`. `--verifier` : ne rien écrire, dire
      seulement ce qui serait fait. `--premier-remplissage` : autoriser la
      création du maître quand il n'existe pas. `--increment CHEMIN` : verser
      ce fichier au lieu de l incrément du soir, chemin relatif à la racine ;
      il doit porter les huit colonnes du maître, source comprise, et c est sa
      source qui est écrite au maître.
      Exemple réel : le comblement du trou de juillet depuis Euronext (A-473).
    ④ CONDITIONS D ENTRÉE — La racine doit exister ; sinon le changement de
      dossier lève. Les trois fichiers de cours peuvent tous manquer : chacun
      est un cas prévu.
    ⑤ SORTIE — Ne rend rien. **Tout passe par le code de sortie et l affichage.**
      [rend: rien]
    ⑥ TRAITEMENT — ① charger le maître, une entrée par couple valeur-date ·
      ② s il est absent ou vide, **s arrêter**, sauf si `--premier-remplissage` est
      demandé : le remplir alors avec tout l historique Google · ② bis sinon,
      **vérifier qu il n a pas rétréci** : chaque couple valeur-séance de la
      version enregistrée au dépôt, et de l historique Google, doit y être ;
      sinon s arrêter ·
      ③ charger l incrément du soir, ou le fichier de `--increment`, par
      `lire_l_increment`, qui refuse un fichier absent, mal encodé ou à l en-tête
      inattendu, et **s arrêter s il est vide** · ③ bis **s arrêter sans rien écrire** si
      `juger_la_ligne` refuse une seule ligne — source, date, valeur ou cours — ou
      si le référentiel des valeurs ne se lit pas ·
      ④ pour chaque ligne : absente du maître, elle est ajoutée avec la source
      qu elle porte, ou à défaut celle que dit sa date ; déjà présente,
      ses cinq champs sont comparés à l ancienne · ⑤ si un écart est trouvé,
      écrire le rapport des révisions et **s arrêter sans rien toucher au
      maître** · ⑥ sinon, réécrire le maître trié et afficher le bilan.
    ⑦ UNITÉ — Les prix sont en euros, le volume en titres, les dates au format
      AAAA-MM-JJ. **Les comptes affichés — lignes, valeurs, ajouts — sont des
      nombres de lignes, jamais des séances.**
    ⑧ POURQUOI — **Trois arrêts délibérés, et chacun répare un silence mesuré.**
      · L incrément vide : le 12-09, si la collecte échouait, ce programme
        rendait 0 et un maître inchangé. Un contrôle qui compte sur un autre
        contrôle pour parler ne protège rien.
      · Les révisions : quand ABC change une séance déjà enregistrée, rien n est
        écrit. **Trancher entre l ancienne et la nouvelle appartient à Jean-Luc
        — trancher entre l'ancienne valeur et la nouvelle appartient à Jean-Luc (A-231), parce que cela touche la reproductibilité des chiffres figés.**
      · `--verifier` : permet de voir ce qui serait fait sans rien écrire, ce
        qui rend le programme rejouable sur un clone.
    ⑨ CE QUI CLOCHE — **L écriture du maître n est pas atomique** : le fichier
      est ouvert en écriture, donc vidé, puis rempli. Une interruption entre les
      deux laisse un maître tronqué. **Depuis le 24-09-2026 (A-442), le passage
      suivant le détecte** — des couples valeur-séance enregistrés au dépôt ou
      présents dans l historique Google manquent — **et s arrête** ; l écriture,
      elle, reste non atomique.
    ⑩ EFFET — **RÉÉCRIT `donnees/cours_maitre.csv` EN ENTIER**, trié par valeur
      puis par date · **crée le dossier `rapports/`** s il manque, et y écrit
      `revisions_du_passe.csv` · **change le dossier de travail du processus**
      par `os.chdir`, ce qui rend tous les chemins relatifs à la racine passée ·
      **`extrasaction=\"ignore\"` JETTE SILENCIEUSEMENT toute colonne absente de
      `COLONNES`** — une colonne ajoutée en amont disparaîtrait sans un mot.
    ⑪ TERMINAISON — **NE REND JAMAIS LA MAIN : tous les chemins terminent le
      programme.** Code 2 : aucun argument, `--increment` sans chemin, option inconnue ou mal placée · Code 1 : reconstruction qui perdrait des séances enregistrées, ligne refusée par `juger_la_ligne`, référentiel illisible, maître absent sans
      `--premier-remplissage`, maître qui a rétréci, version enregistrée ou
      historique Google illisibles, incrément vide, ou révisions détectées · Code 0 : versement fait, ou vérification demandée.
      **Le circuit du soir n a pas de tolérance sur ce pas : un code non nul
      [sort: oui]
    ⑫ DÉFINITIONS —
      le maître : `donnees/cours_maitre.csv`, le fichier unique qui porte tout
        l'historique des cours et n'est jamais réécrit.
      l'incrément : `donnees/claude_cours_nouveaux.csv`, où la collecte écrit les
        cours du jour avant leur versement au fichier maître.
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par
        GitHub Actions — collecte, versement, signaux, positions, mesure,
        surveillance."""
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    racine = sys.argv[1]
    verifier = "--verifier" in sys.argv
    # --increment CHEMIN — verser un autre fichier que l incrément du soir.
    # Ajouté le 24-09-2026 pour combler le trou de juillet (A-473) : les séances
    # manquantes, venues d Euronext, passent par CE programme et donc par toutes
    # ses protections, au lieu d un second programme qui écrirait le maître.
    # Le chemin est relatif à la racine, puisque le programme s y place.
    increment_chemin = INCREMENT
    if "--increment" in sys.argv:
        i = sys.argv.index("--increment")
        if i + 1 >= len(sys.argv) or sys.argv[i + 1].startswith("--"):
            print("  ❌ ARRÊT : --increment demande le chemin d'un fichier de cours.")
            sys.exit(2)
        increment_chemin = sys.argv[i + 1]
    # UNE OPTION MAL ÉCRITE N EST PAS IGNORÉE. Agent indépendant, 24-09-2026 :
    # `--increment=inc.csv` ou `inc.csv` seul versaient en silence l incrément du soir
    # et affichaient « écrit » ; `--increment inc.csv .` tombait sur `os.chdir`.
    attendus = {"--verifier", "--premier-remplissage", "--increment"}
    reste = sys.argv[2:]
    if "--increment" in reste:
        j = reste.index("--increment")
        reste = reste[:j] + reste[j + 2:]
    inconnus = [a_ for a_ in reste if a_ not in attendus] + (
        [racine] if racine.startswith("--") else [])
    if inconnus or sys.argv.count("--increment") > 1:
        print(f"  ❌ ARRÊT : ligne de commande inattendue — {' '.join(inconnus) or '--increment répété'}.")
        print("     Attendu : TENIR_L_HISTORIQUE.py <racine> [--verifier] [--premier-remplissage] "
              "[--increment CHEMIN]")
        sys.exit(2)
    os.chdir(racine)

    maitre = {}
    for r in lire(MAITRE):
        maitre[(cle_valeur(r["valeur"]), r["date"])] = r
    neuf = not maitre

    # PROTECTION 1 — LE MAITRE N EST JAMAIS RECREE EN SILENCE (A-442, 24-09-2026).
    # Mesure du 24-09 sur une copie : maitre supprime, ce pas du soir le
    # reconstruisait depuis les anciens fichiers et finissait en vert ; aucun
    # programme en aval ne voyait jamais le maitre manquer. Decision de Jean-Luc
    # du 20-09-2026 : « Si le maitre n est pas la, il y a un message d alerte de
    # toute urgence. » Une premiere creation se demande donc explicitement.
    if neuf and "--premier-remplissage" not in sys.argv:
        print(f"  ❌ ARRÊT : LE FICHIER MAÎTRE {MAITRE} EST ABSENT OU VIDE.")
        print("     Il n'est PAS recréé en silence depuis les anciens fichiers de cours")
        print("     (décision de Jean-Luc du 20-09-2026, A-442). Une première création")
        print("     se demande explicitement, avec l'option --premier-remplissage.")
        ecrire_l_alerte(f"le fichier maître {MAITRE} est absent ou vide.",
                        ["Il n'a PAS été recréé depuis les anciens fichiers."])
        sys.exit(1)

    # PROTECTION 2 — LE MAITRE NE RETRECIT JAMAIS (A-442, 24-09-2026).
    # Mesure du 24-09 sur une copie : maitre coupe a ses 1 000 dernieres lignes,
    # ce pas le completait a 2 585 lignes au lieu de 26 807 et finissait en vert.
    # Deux proprietes, jamais un compte : (a) chaque couple valeur-seance de la
    # version ENREGISTREE au depot est encore la ; (b) chaque couple de
    # l historique Google de reference, qui ne change jamais, est la aussi — ce
    # second test attrape meme une troncature deja enregistree.
    if not neuf:
        import io, subprocess
        try:
            enregistre = subprocess.run(
                ["git", "show", "HEAD:" + MAITRE.replace(os.sep, "/")],
                capture_output=True, check=True).stdout.decode("utf-8-sig")
        except Exception as e:
            print(f"  ❌ ARRÊT : la version enregistrée de {MAITRE} ne se relit pas "
                  f"— le contrôle qui empêche le maître de rétrécir n'a pas pu tourner : {e}")
            ecrire_l_alerte(f"la version enregistrée de {MAITRE} ne se relit pas ; le contrôle "
                            f"qui empêche le maître de rétrécir n'a pas pu tourner.", [str(e)])
            sys.exit(1)
        cles_enregistrees = {(cle_valeur(r["valeur"]), r["date"])
                             for r in csv.DictReader(io.StringIO(enregistre))}
        cles_google = {(cle_valeur(r["valeur"]), r["date"]) for r in lire(HISTORIQUE_GOOGLE)}
        if not cles_google:
            print(f"  ❌ ARRÊT : l'historique Google de référence {HISTORIQUE_GOOGLE} est absent ou vide "
                  f"— le contrôle qui empêche le maître de rétrécir n'a pas pu tourner.")
            ecrire_l_alerte(f"l'historique Google de référence {HISTORIQUE_GOOGLE} est absent ou vide ; "
                            f"le contrôle qui empêche le maître de rétrécir n'a pas pu tourner.", [])
            sys.exit(1)
        perdues = (cles_enregistrees | cles_google) - set(maitre)
        if perdues:
            ex = sorted(perdues)[:3]
            print(f"  ❌ ARRÊT : LE FICHIER MAÎTRE {MAITRE} A RÉTRÉCI — {len(perdues)} couple(s) "
                  f"valeur-séance ont disparu.")
            print(f"     Exemples : {ex}")
            print("     Il n'est pas réécrit : le rétablir depuis le dépôt avant tout calcul.")
            ecrire_l_alerte(f"le fichier maître {MAITRE} a rétréci : {len(perdues)} couple(s) "
                            f"valeur-séance ont disparu.", [f"exemples : {ex}",
                            "Il n'a pas été réécrit."])
            sys.exit(1)

    if neuf:
        # PREMIER REMPLISSAGE — le passé Google d'abord, tel quel.
        for r in lire(HISTORIQUE_GOOGLE):
            maitre[(cle_valeur(r["valeur"]), r["date"])] = dict(r, source="google")
        print(f"  premier remplissage · {len(maitre)} lignes depuis l'historique Google")

    # L'INCRÉMENT — Google jusqu'au 08-09, ABC à partir du 09-09.
    # UN INCRÉMENT VIDE NE SE TAIT PAS. Trouvé par mon propre mandat inversé le
    # 12-09 : si la collecte ABC échoue et rend un fichier sans lignes, ce
    # programme rendait code 0 et un maître inchangé — **exactement la cessation
    # muette que tout le système combat**. Le collecteur alerte de son côté, mais
    # un contrôle qui dépend d'un autre contrôle pour parler ne protège rien.
    # LE MODE SE LIT À L OPTION, JAMAIS AU CHEMIN. Agent indépendant, 24-09-2026 :
    # `--increment donnees/claude_cours_nouveaux.csv` passait pour le soir et
    # contournait tous les raccords, alors que `./donnees/…` les appliquait.
    par_increment = "--increment" in sys.argv
    increment, raison = lire_l_increment(increment_chemin, par_increment)
    if raison:
        print(f"  ❌ ARRÊT : {raison} RIEN N'EST ÉCRIT.")
        sys.exit(1)
    if not increment:
        print(f"  ⚠️ L'INCRÉMENT EST VIDE : {increment_chemin} ne porte aucune séance.")
        print("     Le maître n'est pas touché, mais AUCUNE séance neuve n'arrive.")
        print("     La collecte du soir a probablement échoué — voir son rapport.")
        sys.exit(1)

    # UNE LIGNE DE L INCRÉMENT N ENTRE QUE SI SA SOURCE EST ADMISE ET SA DATE PASSÉE.
    # Cassure de Cowork, 24-09-2026 : `ACCOR,2026-09-25,…,n_importe_quoi` versé par
    # `--increment` entrait au maître en code 0 — une source inventée, et une séance
    # du lendemain. Refus en bloc : RIEN n est écrit si une seule ligne est fautive.
    aujourd_hui = datetime.now(PARIS).strftime("%Y-%m-%d")
    fautes, vues = [], set()
    # LE RÉFÉRENTIEL DIT QUELLES VALEURS EXISTENT. Cassure de Cowork, 24-09-2026 :
    # `TOTO_INCONNUE` entrait au maître. Sans référentiel lisible, le contrôle ne
    # peut pas tourner : il le dit et s arrête (R-734).
    try:
        noms = [f for f in os.listdir("donnees")
                if f.upper().startswith("REFERENTIEL_VALEURS") and f.endswith(".csv")]
        with open(os.path.join("donnees", le_plus_recent(noms)), encoding="utf-8-sig") as f:
            connues = {cle_valeur(x["nom_usuel"]) for x in csv.DictReader(f)}
    except Exception as e:
        print(f"  ❌ ARRÊT : le référentiel des valeurs ne se lit pas — le contrôle des lignes "
              f"n'a pas pu tourner : {e}")
        sys.exit(1)

    # CE QUE LE MAÎTRE SAIT DE CHAQUE VALEUR, avant tout ajout : ses clôtures datées,
    # sa première séance, la médiane de ses volumes, ses graphies. Le fichier à verser
    # n'y entre pas : deux lignes fausses ne se valident pas l'une l'autre.
    import statistics
    clotures, volumes, graphies = {}, {}, {}
    for (kv, kd), x in maitre.items():
        graphies.setdefault(kv, set()).add(x["valeur"])
        if PRIX_ECRIT.fullmatch(x.get("close") or "") and VOLUME_ECRIT.fullmatch(x.get("volume") or ""):
            clotures.setdefault(kv, []).append((kd, float(x["close"])))
            volumes.setdefault(kv, []).append(float(x["volume"]))
    for kv in clotures:
        clotures[kv].sort()
    medianes = {kv: statistics.median(v) for kv, v in volumes.items()}
    premiere = min((d for (_, d) in maitre), default="")
    alertes = []

    ajouts, revisions = 0, []
    for r in increment:
        k = (cle_valeur(r.get("valeur") or ""), r.get("date") or "")
        # LA SOURCE ÉCRITE EST CELLE QUE PORTE LA LIGNE, quand elle en porte une.
        # Trouvé le 24-09-2026 en préparant le comblement du trou de juillet : la
        # source était déduite de la seule date, et les lignes d Euronext datées de
        # juillet auraient été écrites « google ». L incrément du soir n a pas
        # de colonne source : pour lui, rien ne change.
        # Un fichier versé par `--increment` porte TOUJOURS sa colonne source :
        # `lire_l_increment` l'exige, et le repli par la date ne vaut que le soir.
        # SA CASE SE LIT TELLE QU'ELLE EST ÉCRITE, sans repli ni nettoyage (cassure de
        # Cowork, 24-09-2026 23h39) : une case vide recevait « google » d'après sa date,
        # alors que Google n'a jamais fourni les séances de juillet. Vide ou entourée
        # d'espaces, la case est refusée par `juger_la_ligne`.
        if par_increment:
            src = r.get("source") or ""
        else:
            src = source_de(r, "abc" if (r.get("date") or "") >= BASCULE_ABC else "google")
        # TOUTE LA LIGNE EST JUGÉE, PAR UNE SEULE FONCTION (cassures de Cowork, 24-09-2026).
        suite = clotures.get(k[0], [])
        avant_ = bisect.bisect_left(suite, (k[1], float("-inf")))
        apres_ = bisect.bisect_right(suite, (k[1], float("inf")))
        voisinage = dict(debut=suite[0][0] if suite else None,
                         veille=suite[avant_ - 1][1] if avant_ > 0 else None,
                         lendemain=suite[apres_][1] if apres_ < len(suite) else None,
                         mediane_volume=medianes.get(k[0]), graphies=graphies.get(k[0], set()))
        motifs, alerte = juger_la_ligne(r, src, aujourd_hui, connues, premiere, voisinage,
                                        par_increment)
        fautes += motifs
        if alerte:
            alertes.append(alerte)
        # UNE MÊME SÉANCE DEUX FOIS DANS L INCRÉMENT se dit comme telle, et non comme
        # une « révision du passé », ce qu elle n est pas.
        if k in vues:
            fautes.append(f"{r['valeur']};{r['date']} : séance en double dans l'incrément")
        vues.add(k)
        if k not in maitre:
            maitre[k] = dict(r, source=src)
            ajouts += 1
            continue
        # ④ LA RÉVISION SE DÉTECTE : la ligne existe déjà, a-t-elle changé ?
        anc = maitre[k]
        for champ in ("open", "high", "low", "close", "volume"):
            a, b = (anc.get(champ) or "").strip(), (r.get(champ) or "").strip()
            if a and b and a != b:
                try:
                    if abs(float(a) - float(b)) < 1e-9:
                        continue
                except ValueError:
                    pass
                # « incrément=… » et non une source : relecture de l'agent indépendant,
                # 24-09-2026 — étiqueter la nouvelle valeur « google » d'après sa date
                # faisait croire que Google s'était révisé lui-même.
                revisions.append(f"{r['valeur']};{r['date']};{champ};"
                                 f"{source_de(anc,'?')}={a};incrément={b}")

    for a_ in alertes[:10]:
        print(f"  ⚠️ ALERTE DU JUGE DES COURS — {a_}")
    if fautes:
        print(f"  ❌ ARRÊT : {len(fautes)} motif(s) de refus dans {increment_chemin} — RIEN N'EST ÉCRIT.")
        for f_ in fautes[:10]:
            print(f"     · {f_}")
        sys.exit(1)

    if revisions:
        os.makedirs("rapports", exist_ok=True)
        chemin = os.path.join("rapports", "revisions_du_passe.csv")
        with open(chemin, "w", encoding="utf-8", newline="") as f:
            f.write("valeur;date;champ;ancienne;nouvelle\n" + "\n".join(revisions) + "\n")
        print(f"  ⚠️ {len(revisions)} RÉVISION(S) DU PASSÉ DÉTECTÉE(S) — écrites dans {chemin}")
        print("     Une séance déjà enregistrée a changé de valeur à la source.")
        print("     RIEN N'EST ÉCRIT AU MAÎTRE : prendre la nouvelle version ou garder")
        print("     l'ancienne est une décision de Jean-Luc (A-231), et elle touche la")
        print("     reproductibilité des chiffres de référence figés.")
        sys.exit(1)

    # UNE RECONSTRUCTION NE PERD PAS CE QUI EST ENREGISTRÉ. Agent indépendant,
    # 24-09-2026 : maître effacé, `--premier-remplissage` le refaisait depuis Google et
    # l incrément du soir, et les 406 séances d Euronext du trou de juillet
    # disparaissaient en code 0. Même propriété que la protection 2, appliquée aussi
    # au premier remplissage : chaque couple de la version enregistrée doit être là.
    if neuf:
        import io, subprocess
        try:
            enregistre = subprocess.run(
                ["git", "show", "HEAD:" + MAITRE.replace(os.sep, "/")],
                capture_output=True, check=True).stdout.decode("utf-8-sig")
        except Exception:
            enregistre = ""          # aucune version enregistrée : vraie première création
        perdues = {(cle_valeur(x["valeur"]), x["date"])
                   for x in csv.DictReader(io.StringIO(enregistre)) if x.get("date")} - set(maitre)
        if perdues:
            ex = sorted(perdues)[:3]
            print(f"  ❌ ARRÊT : LA RECONSTRUCTION PERDRAIT {len(perdues)} couple(s) valeur-séance "
                  f"enregistrés au dépôt. Exemples : {ex}")
            print("     Rien n'est écrit : reprendre la version enregistrée (réponse A).")
            ecrire_l_alerte(f"la reconstruction du fichier maître {MAITRE} perdrait {len(perdues)} "
                            f"couple(s) valeur-séance enregistrés au dépôt.",
                            [f"exemples : {ex}", "Rien n'a été écrit."])
            sys.exit(1)

    if verifier:
        print(f"  {len(maitre)} lignes · {ajouts} à ajouter · 0 révision · AUCUNE ÉCRITURE")
        sys.exit(0)

    lignes = sorted(maitre.values(), key=lambda r: (cle_valeur(r["valeur"]), r["date"]))
    with open(MAITRE, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLONNES, extrasaction="ignore")
        w.writeheader()
        w.writerows(lignes)
    par_source = {}
    for r in lignes:
        par_source[r.get("source", "?")] = par_source.get(r.get("source", "?"), 0) + 1
    dates = sorted({r["date"] for r in lignes})
    print(f"  écrit : {MAITRE}")
    print(f"  {len(lignes)} lignes · {len({cle_valeur(r['valeur']) for r in lignes})} valeurs"
          f" · du {dates[0]} au {dates[-1]}")
    print(f"  par source : " + " · ".join(f"{k} {v}" for k, v in sorted(par_source.items())))
    print(f"  {ajouts} ligne(s) ajoutée(s) ce passage")
    sys.exit(0)


if __name__ == "__main__":
    main()
