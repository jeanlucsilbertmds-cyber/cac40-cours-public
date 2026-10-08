#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MESURER LA PERFORMANCE — service 4 du moteur central.
Projet CAC 40 · conforme A-208 (decisions D1 et D2 du 15-08-2026).
Simulations uniquement — aucun ordre reel.

CE QUE FAIT CE SERVICE, ET RIEN D'AUTRE :
il LIT le journal des operations terminees, le registre des strategies et les
chiffres de reference figes, puis il ECRIT une ligne par JOUR, par STRATEGIE et
par COMPTABILITE dans l'historique des mesures.

REGLE FONDATRICE (A-208) : personne d'autre ne calcule ces chiffres. Le cockpit,
la surveillance et le rapport du soir LISENT le fichier produit ici. Si un chiffre
nouveau est necessaire, il s'ajoute ICI, jamais chez celui qui l'affiche.

L'HISTORIQUE DES MESURES S'EMPILE, IL N'EST JAMAIS ECRASE (decision JL du 15/08) :
une ligne par jour permet de voir l'EVOLUTION des indicateurs — seul moyen de
detecter une degradation lente — et de savoir ce que le systeme savait a une date.

CALIBRAGE OBLIGATOIRE : au demarrage, le service doit retrouver les chiffres deja
connus. S'il n'y parvient pas, il S'ARRETE et n'ecrit rien.

USAGE : python3 mesurer_la_performance.py [dossier_sources] [dossier_sortie]

① RÔLE — Donner chaque soir, en chiffres, l'état de chaque stratégie simulée
  encore vivante : combien d'opérations terminées, combien de gagnantes, combien
  d'euros gagnés ou perdus, et si le taux de réussite constaté suffit à couvrir
  les frais. C'est le SEUL endroit du système où ces chiffres se calculent :
  le cockpit, le document de pilotage et la surveillance du soir se contentent
  de relire le fichier écrit ici. Sans cette règle, le même indicateur serait
  calculé dans trois programmes et les trois donneraient trois valeurs.
  Mesuré le 19-09-2026 sur le vrai journal : quatre lignes produites, deux
  stratégies vivantes fois deux comptabilités.
② CONTEXTE D'APPEL — Un seul appelant automatique : l'étape « Mesurer la
  performance » de `.github/workflows/collecte_abc.yml`, ligne 223, lancée
  chaque soir après la collecte des cours et la tenue des positions. Elle passe
  UN SEUL argument, `"$GITHUB_WORKSPACE"`, le dossier du dépôt cloné sur la
  machine jetable ; le dossier de sortie n'est donc pas donné et vaut le dossier
  courant. Cette étape porte `continue-on-error: true` — son échec ne bloque pas
  la collecte — mais la commande se termine par un `echo "::error::"` qui fait
  quand même apparaître l'échec en rouge dans le journal du passage.
  Jean-Luc ou le Chat peuvent aussi le lancer à la main.
③ ENTRÉE — La ligne de commande, deux arguments, tous deux facultatifs. Le
  premier est le dossier où chercher les fichiers à lire, le dossier courant par
  défaut. Le second est le dossier où écrire l'historique des mesures, le
  dossier courant par défaut. Le circuit du soir ne passe que le premier.
④ CONDITIONS D'ENTRÉE — Le journal des opérations terminées doit être trouvable
  sous le dossier de sources, sous l'un des noms `journal_trades.csv` ou
  `claude_journal_trades.csv`, à plat ou dans un sous-dossier. Il doit porter
  une opération sur Bureau Veritas aux montants exacts du calibrage, sinon rien
  n'est écrit. Et LE DOSSIER `donnees/` DOIT DÉJÀ EXISTER sous le dossier de
  sortie : le programme ne le crée pas.
⑤ SORTIE — Un code de sortie, et rien d'autre : 0 quand les mesures ont été
  écrites, 0 également quand aucune stratégie n'est vivante au registre, 1 quand
  le journal est introuvable et 1 quand le calibrage échoue. Tout le reste est
  affiché à l'écran.
⑥ TRAITEMENT — ① lire le journal des opérations terminées · ② refaire trois
  chiffres déjà connus et s'arrêter s'ils ne tombent pas juste · ③ relever au
  registre des stratégies celles qui sont en essai ou en production · ④ charger
  les chiffres de référence figés · ⑤ charger le référentiel qui relie un nom
  d'entreprise à son code de bourse · ⑥ reconstruire la courbe du capital jour
  après jour · ⑦ calculer les deux témoins de comparaison · ⑧ pour chaque
  stratégie, retrouver ses opérations, vérifier qu'elles portent sur des valeurs
  autorisées, et composer DEUX lignes, une par comptabilité · ⑨ ajouter à
  l'historique les lignes du jour qui n'y sont pas déjà · ⑩ afficher le bilan.
⑦ UNITÉ — Les résultats en EUROS · les taux de réussite, le point mort, la borne
  basse et la pire chute en POURCENTS, jamais en fractions · les opérations en
  NOMBRE D'OPÉRATIONS TERMINÉES · la date de mesure en année-mois-jour, heure de
  Paris · le rapport gain sur secousses sans unité, ramené à l'année.
⑧ POURQUOI — Un seul calculateur, décidé le 15-08-2026 sous l'identifiant A-208.
  Quand un même indicateur se calcule à plusieurs endroits, les copies divergent
  et personne ne sait laquelle croire : c'est exactement ce qui est arrivé au
  point mort, calculé ici en pourcents et dans `programmes/MODULE_JUGEMENT.py`
  en fractions, sous le même nom et avec les deux mêmes arguments. Croisés le
  12-09-2026, les deux chemins rendaient 38,51 % au lieu de 43,08 % — un chiffre
  plausible, que rien n'aurait attrapé. Depuis, ce programme ne calcule plus le
  point mort : il convertit et délègue au propriétaire du calcul.
  L'empilement des mesures, décidé par Jean-Luc le 15-08-2026, répond à un autre
  besoin : une ligne par jour permet de voir une dégradation lente, qu'une
  photographie du jour ne montrerait jamais.
⑨ CE QUI CLOCHE —
  ① CORRIGÉ LE 27-09-2026 (défaut 3 de A-491) — l'appariement est exact, et
  chaque opération ne compte que dans sa comptabilité, lue dans la colonne
  `comptabilite` ajoutée au journal le même jour. Constat d'origine :
  une opération était comptée dans DEUX stratégies à la fois. Les opérations
  d'une stratégie sont retrouvées en cherchant le nom du journal COMME MORCEAU
  du nom du registre, et non par égalité. Mesuré le 19-09-2026 sur le vrai
  journal de cinq opérations : l'opération Bureau Veritas, écrite au journal
  sous le nom `C5-ETENDU-10`, est attribuée à `C5E10-QA-V1` ET à
  `C5E10-OBS-V1`, parce que ce nom est contenu dans l'intitulé des deux. Les
  deux stratégies annoncent donc le même cumul de 1 292,25 € sur trois
  opérations, alors que le journal n'en porte que cinq en tout.
  ② CORRIGÉ LE 27-09-2026 avec le ① : un nom doit être ÉGAL, plus contenu.
  Constat d'origine : un nom court est avalé par un nom long. La même recherche par morceau fait
  qu'une stratégie nommée `COURS_BAS_ARGENT_REVIENT_1` au journal serait
  attribuée à la stratégie `COURS_BAS_ARGENT_REVIENT_10` du registre : vérifié
  le 19-09-2026, le premier nom est bien contenu dans le second. Aucun message
  ne le dirait.
  ③ Le référentiel qui relie les noms aux codes de bourse n'est jamais trouvé
  dans le circuit du soir. Il est cherché à plat dans le dossier de sources,
  alors qu'il vit dans `donnees/REFERENTIEL_VALEURS_v3_Lun_17-08-2026_10h54.csv`.
  Mesuré le 19-09-2026 en lançant le programme sur une copie du dépôt :
  l'affichage porte « ATTENTION : referentiel introuvable ». La conséquence est
  une fausse alerte : Bureau Veritas, dont le code `BVI` figure bien dans
  l'univers autorisé des deux stratégies, est signalé « HORS UNIVERS declare »
  parce que son nom n'a pas pu être traduit en code.
  ④ Les chiffres de référence figés ne sont jamais chargés. Ils sont cherchés à
  plat dans le dossier de sources, alors qu'ils vivent dans
  `gouvernance/golden_tests_Sam_01-08-2026_20h19.json`. Mesuré le 19-09-2026 :
  les quatre lignes écrites portent toutes « non calculable » dans la colonne
  qui devrait dire quelle part du résultat promis a été tenue, alors que le
  fichier existe et annonce 111 334,24 € pour la comptabilité jetons illimités.
  ⑤ Le programme tombe si le dossier `donnees/` n'existe pas sous le dossier de
  sortie. Mesuré le 19-09-2026 en le lançant depuis un dossier vide :
  « FileNotFoundError: [Errno 2] No such file or directory:
  './donnees/historique_mesures.csv' », levée à la ligne d'ouverture du fichier,
  après que tout le calcul a été fait et affiché. Le travail est perdu.
  ⑥ Une fonction chargée de lire le taux de frais chez son propriétaire,
  `_frais_du_proprietaire`, n'est appelée nulle part. Vérifié le 19-09-2026 par
  recherche de son nom dans tout le dossier `programmes/` : elle n'apparaît
  qu'à sa propre définition, ligne 119. Elle fonctionne — appelée à la main,
  elle rend 0,0015 — mais rien ne s'en sert.
  ⑦ Deux chiffres sont écrits à l'identique sur toutes les lignes alors qu'ils
  ne valent que pour l'ensemble. Le rapport gain sur secousses et les deux
  témoins de comparaison sont calculés UNE fois, sur toutes les opérations
  réunies, puis recopiés sur chaque ligne de chaque stratégie et de chaque
  comptabilité. Mesuré le 19-09-2026 : les quatre lignes écrites portent toutes
  « 0.35 », y compris celles des deux comptabilités dont les cumuls diffèrent
  (+1 292,25 € contre −1 898,50 €).
  ⑧ La courbe du capital ignore l'historique des cours qui grandit. Elle est
  reconstruite à partir de `cac40_ohlcv.csv` et `cours_nouveaux.csv`, et jamais
  à partir de `donnees/cours_maitre.csv`, le fichier unique où s'empilent
  désormais les séances. Vérifié le 19-09-2026 : le nom `cours_maitre` n'apparaît
  nulle part dans ce programme.
⑩ EFFET — AJOUTE des lignes à la fin du fichier `donnees/historique_mesures.csv`
  placé sous le dossier de sortie, ou le crée avec son en-tête s'il n'existe pas.
  Il ne réécrit jamais une ligne déjà présente : une ligne portant la même date,
  la même stratégie et la même comptabilité est passée. Mesuré le 19-09-2026 sur
  une copie : le fichier passe de 85 à 89 lignes et son empreinte change.
  Aucun autre fichier n'est écrit, aucun accès réseau. Il LIT le journal des
  opérations, le registre des stratégies, le référentiel des valeurs, les
  chiffres figés et les fichiers de cours, et parcourt l'arborescence du dossier
  de sources pour les trouver. Il ajoute le dossier du programme au chemin de
  recherche des modules de Python.
⑪ TERMINAISON — SORT DU PROGRAMME avec le code rendu par `main` : 0 ou 1. Et un
  de ses appels peut ne pas revenir : `main` laisse remonter une erreur non
  rattrapée quand le dossier de sortie ne porte pas de sous-dossier `donnees/`,
  et quand le point mort calculé tombe hors de l'intervalle de 0 à 100.
⑫ DÉFINITIONS
  une comptabilité : une façon de compter le résultat. Il y en a DEUX, qui
    stop. Le même journal donne donc deux résultats différents : mesuré le
    19-09-2026, +1 292,25 € en un jeton et −1 898,50 € en jetons illimités.
  le point mort : le taux de réussite en dessous duquel une stratégie perd de l'argent
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
  le registre des stratégies : le fichier `cac40_strategies.csv`, une ligne par stratégie, qui porte leur état civil — identifiant, réglages, résultats connus
  le référentiel des valeurs : donnees/REFERENTIEL_VALEURS_*.csv, la liste des valeurs à suivre, avec pour chacune son mnémonique et sa place de cotation.
  le témoin permanent : ce qu'auraient rapporté 100 000 € placés sur l'indice
    du début à la fin, sans rien faire
  le témoin miroir : ce qu'aurait rapporté l'indice en n'étant exposé que les jours où une position était ouverte
  C5-ETENDU-10 : le nom de la stratégie vivante ; ses seuils et son horizon sont lus dans `donnees/cac40_strategies.csv`.
  PRODUCTION : l etat d une strategie dont le seuil d operations est atteint et les resultats conformes, donc exploitee.
  hors univers : une valeur que Jean-Luc a volontairement retiree du champ, avec son motif ecrit dans la colonne `hors_univers` du referentiel
  l'univers : la liste des valeurs sur lesquelles une stratégie a le droit d'acheter, désignées par leur mnémonique
  l'univers autorisé : la liste des valeurs qu'une stratégie a le droit de jouer, écrite dans le registre des stratégies
  la pire chute : la plus forte baisse du cumul depuis un sommet precedent.
  le Chat : la conversation qui rédige la gouvernance du projet et dépose ses versions
  le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
  le cockpit : la page web que ce programme fabrique et que Jean-Luc ouvre pour voir l etat du systeme.
  le journal des opérations : le fichier où s'écrit chaque opération simulée refermée, avec son prix d'entrée, son prix de sortie et son résultat
  une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
"""
import csv, json, os, sys, math
from datetime import datetime
from zoneinfo import ZoneInfo

PARIS = ZoneInfo('Europe/Paris')
CAPITAL = 100000.0          # capital engage par position (carte d'identite)
# LE FICHIER DES MESURES VIT DANS `donnees/`, COMME TOUS LES FICHIERS DE LIAISON.
# CASSURE DE COWORK, tour 51 puis 53 — et c est la cause de TROIS JOURS de silence.
# **Ce programme ecrivait `historique_mesures.csv` a la RACINE. Le workflow
# commite `donnees/historique_mesures.csv`, et le cockpit le lit la aussi.
# Deux fichiers portaient le meme nom et divergeaient : 64 lignes du 15-08 au
# 06-09 dans `donnees/`, 16 lignes du 12-09 au 16-09 a la racine.**
# **Consequence mesuree : le pas qui commite mesures, PILOTE et rapport du radar
# n a rien depose depuis le 13-09. Le rituel de debut de session lisait un
# rapport de dimanche, et rien ne comparait sa date au jour.**
# Les deux fichiers ont ete FUSIONNES le 16-09 — periodes disjointes, memes
# colonnes, aucune ligne perdue : 80 lignes du 15-08 au 16-09.
# **Il reste un trou du 07 au 11-09 : la mesure n a pas tourne pendant la
# migration vers GitHub. Les cours, eux, sont complets.**
FICHIER_MESURES = os.path.join('donnees', 'historique_mesures.csv')

COLONNES = ['date_mesure','strategie','comptabilite','etat','n_operations','gagnantes',
            'taux_reussite','borne_basse_wilson','point_mort','verdict_c7','cumul_net_eur',
            'esperance_eur','facteur_profit','serie_en_cours','pertes_consecutives',
            'pire_chute_pct','pire_chute_eur','compteur','seuil','conformite_promis',
            'voyant_c7','voyant_pertes','voyant_chute','temoin_permanent','temoin_miroir',
            'rapport_gain_secousses','source_calibrage']

# ---------------------------------------------------------------- lecture
def _p(base, *noms):
    """Trouve un fichier par son nom, OU QU IL SOIT DANS L ARBORESCENCE.

    Corrige le 12-09-2026 : cette fonction connaissait le prefixe `claude_` mais
    cherchait A PLAT. Au depot, les donnees vivent dans `donnees/` — et la mesure
    s arretait sur « journal des operations introuvable » alors que
    `donnees/claude_journal_trades.csv` etait la. Meme famille que `chemin_de()`
    du radar : un radar aveugle a l arborescence rend des verdicts faux.
    A egalite de nom, c est le PLUS RECENT par la date de son nom qui gagne.

    ① RÔLE — Retrouver un fichier de données sans savoir où il est rangé, pour
      qu'un déplacement de fichier n'arrête pas la mesure. Le journal des
      opérations a changé de nom et de dossier plusieurs fois : il s'est appelé
      `journal_trades.csv`, puis `claude_journal_trades.csv`, et il est passé de
      la racine à `donnees/`. Cette fonction accepte les quatre écritures et
      cherche dans tous les sous-dossiers.
    ② CONTEXTE D'APPEL — Quatre appels, tous dans ce programme. `main` l'appelle
      deux fois, pour le journal des opérations puis pour le registre des
      stratégies. `courbe_capital` l'appelle pour chacun des deux fichiers de
      cours. `temoins` l'appelle pour chacun des trois noms possibles du fichier
      d'indice.
    ③ ENTRÉE — `base` : le dossier où chercher, celui reçu sur la ligne de
      commande, `"$GITHUB_WORKSPACE"` dans le circuit du soir · `noms` : un ou
      plusieurs noms de fichier à essayer, donnés sans dossier, par exemple
      `'journal_trades.csv'`.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un dossier inexistant ne la fait pas tomber :
      le parcours de l'arborescence ne rend alors rien et la fonction rend
      `None`.
    ⑤ SORTIE — UNE valeur, de deux formes. Un chemin de fichier quand un fichier
      a été trouvé. `None` quand aucun ne l'a été.
      [rend: 1]
    ⑥ TRAITEMENT — ① pour chaque nom demandé, fabriquer quatre écritures : le nom
      tel quel, le nom avec des espaces à la place des tirets bas, le nom
      précédé de `claude_`, et le nom précédé de `claude/` · ② essayer chacune à
      plat dans le dossier reçu, et rendre la première qui existe · ③ sinon,
      parcourir toute l'arborescence en écartant `archives`, `.git`,
      `__pycache__` et `_site_travail` · ④ rendre `None` si rien n'a été trouvé ·
      ⑤ sinon, demander à `programmes/COMMUN.py` lequel est le plus récent
      d'après la date écrite dans son nom · ⑥ si ce module ne se charge pas,
      rendre le premier par ordre alphabétique.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — L'essai à plat vient d'abord pour ne rien changer au
      comportement là où il fonctionnait déjà : un fichier présent à la racine
      continue d'être pris en premier, et le parcours de l'arborescence ne sert
      que de secours. Les quatre dossiers écartés sont ceux qui portent des
      copies : prendre une mesure sur un fichier d'`archives/` donnerait un
      résultat juste sur des données mortes, sans qu'aucune erreur ne le dise.
      Le départage par la date du nom vient de ce que plusieurs versions d'un
      même fichier peuvent coexister : c'est la plus récente qui fait foi.
    ⑨ CE QUI CLOCHE —
      ① Le repli en cas d'échec du module voisin est le PREMIER par ordre
      alphabétique, donc le plus ancien quand les noms portent une date écrite
      jour-mois-année. L'intention affichée est l'inverse : prendre le plus
      récent. L'erreur qui déclenche ce repli est rattrapée sans être affichée,
      donc rien ne signale que le départage a changé de sens.
      ② Le chemin du dossier du programme est ajouté au chemin de recherche des
      modules de Python à CHAQUE passage dans ce repli, sans jamais être retiré.
      Sur les quatre appels d'un passage, la même entrée peut être ajoutée
      quatre fois.
      ③ L'écriture `'claude/' + nom` n'a de sens qu'à plat : au-delà, le parcours
      ne compare que le dernier morceau du chemin, donc cette écriture ne
      distingue plus rien des autres.
    ⑩ EFFET — LIT l'arborescence du dossier reçu. N'écrit aucun fichier et ne
      touche pas au réseau. MODIFIE le chemin de recherche des modules de Python
      quand le parcours de l'arborescence a trouvé quelque chose.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas : l'échec de
      chargement du module voisin est rattrapé. Aucun de ses appels ne se
      termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir, qui contrôle l'ensemble du système et range chacun de ses constats sous un numéro de maillon, par exemple 18-Tâches pour le contrôle des traces laissées par les tâches planifiées.
      `archives` : le dossier du dépôt où sont rangées les versions tombées, sous un nom qui dit pourquoi elles sont tombées
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
      le journal des opérations : le fichier où s'écrit chaque opération simulée refermée, avec son prix d'entrée, son prix de sortie et son résultat
      le registre : gouvernance/REGISTRE_REGLES.md, le document qui porte les regles numerotees du projet ; une regle absente du registre n'existe pas
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    variantes = []
    for n in noms:
        variantes += [n, n.replace('_', ' '), 'claude_' + n, 'claude/' + n]
    # d abord a plat, pour ne rien changer au comportement quand ca marchait deja
    for c in variantes:
        p = os.path.join(base, c)
        if os.path.exists(p):
            return p
    # puis dans toute l arborescence, en ignorant ce qui n est pas vivant
    cibles = {os.path.basename(v).lower() for v in variantes}
    trouves = []
    for r, sd, fs in os.walk(base):
        sd[:] = [x for x in sd if x not in ('archives', '.git', '__pycache__', '_site_travail')]
        for nom in fs:
            if nom.lower() in cibles:
                trouves.append(os.path.join(r, nom))
    if not trouves:
        return None
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from COMMUN import le_plus_recent
        return le_plus_recent(trouves)
    except Exception:
        return sorted(trouves)[0]

def lire_csv(chemin, sep=','):
    """Lit un fichier de tableau et rend ses lignes, chacune sous forme de dictionnaire.

    ① RÔLE — Donner à tout le programme une seule façon d'ouvrir un fichier de
      tableau, pour qu'aucun appelant n'ait à se soucier du codage des
      caractères ni des fins de ligne. Sans elle, chaque lecture réglerait ces
      détails à sa façon et une seule les oublierait.
    ② CONTEXTE D'APPEL — Cinq appels, tous dans ce programme : `main` deux fois,
      pour le journal des opérations puis pour le registre des stratégies, et
      une troisième fois pour relire l'historique des mesures déjà écrit ·
      `courbe_capital` pour chaque fichier de cours trouvé · `temoins` pour le
      fichier d'indice · `charger_referentiel` pour le référentiel des valeurs.
    ③ ENTRÉE — `chemin` : le chemin du fichier à lire, tel que `_p` l'a rendu ·
      `sep` : le caractère qui sépare les colonnes, la virgule par défaut, et
      aucun appelant ne la change.
    ④ CONDITIONS D'ENTRÉE — Le fichier doit exister et se lire en UTF-8. Sa
      première ligne doit porter les noms des colonnes : c'est elle qui donne
      leurs clés aux dictionnaires rendus.
    ⑤ SORTIE — UNE valeur : une liste de dictionnaires, un par ligne de données,
      dont les clés sont les noms des colonnes. Une liste VIDE quand le fichier
      ne porte que son en-tête.
      [rend: 1]
    ⑥ TRAITEMENT — ① ouvrir le fichier en UTF-8 en écartant la marque d'ordre des
      octets si elle est présente · ② lire toutes les lignes d'un coup et les
      rendre sous forme de liste.
    ⑦ UNITÉ — Un NOMBRE DE LIGNES DE DONNÉES, en-tête non compris.
    ⑧ POURQUOI — Le codage demandé écarte la marque d'ordre des octets, trois
      caractères invisibles que certains tableurs placent en tête de fichier. Sans
      cette précaution, le nom de la première colonne porterait ces caractères
      collés devant lui et aucune recherche par nom de colonne ne le trouverait :
      un fichier parfaitement lisible à l'œil perdrait sa première colonne en
      silence. Et les fins de ligne sont laissées au lecteur de tableau, parce
      qu'une valeur peut contenir un retour à la ligne — c'est le cas de la
      colonne d'explication du journal des opérations, qui porte des paragraphes
      entiers.
    ⑨ CE QUI CLOCHE —
      ① Le fichier est lu en entier et gardé en mémoire. Sur les fichiers du
      projet c'est sans conséquence — l'historique des mesures compte 85 lignes
      au 19-09-2026 — mais rien ne borne cette taille.
      ② Aucune erreur n'est rattrapée. Un fichier absent, un droit de lecture
      manquant ou un octet non conforme à l'UTF-8 font tomber le programme
      entier, sans message qui nomme le fichier fautif.
    ⑩ EFFET — LIT le fichier reçu. N'écrit rien, ne touche pas au réseau,
      n'affiche rien.
    ⑪ TERMINAISON — Rend la main. PEUT LEVER si le fichier n'existe pas, ne se
      lit pas, ou n'est pas de l'UTF-8 valide. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le journal des opérations : le fichier où s'écrit chaque opération simulée
        refermée, avec son prix d'entrée, son prix de sortie et son résultat
      la marque d'ordre des octets : trois octets invisibles que certains tableurs posent en tête d'un fichier et qui, s'ils ne sont pas écartés, se collent au nom de la première colonne
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
      le registre : gouvernance/REGISTRE_REGLES.md, le document qui porte les regles numerotees du projet ; une regle absente du registre n'existe pas
      le registre des stratégies : le fichier `cac40_strategies.csv`, une ligne par stratégie, qui porte leur état civil — identifiant, réglages, résultats connus
      le référentiel : donnees/REFERENTIEL_VALEURS_*.csv, la liste des valeurs à suivre, avec pour chacune son mnémonique et sa place de cotation.
      le référentiel des valeurs : donnees/REFERENTIEL_VALEURS_*.csv, la liste des valeurs à suivre, avec pour chacune son mnémonique et sa place de cotation.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    with open(chemin, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=sep))

def _norm(s):
    """Forme normalisee pour comparer des noms ecrits differemment
    (tirets, tirets bas, espaces, casse). Le defaut d'appariement le plus
    courant du projet : une valeur ou une strategie ecrite de deux facons.

    ① RÔLE — Ramener deux écritures d'un même nom à une seule forme, pour qu'on
      puisse les comparer. La même entreprise s'écrit `UNIBAIL-RODAMCO-WESTFIELD`
      dans un fichier et `UNIBAIL_RODAMCO` dans un autre ; sans cette mise en
      forme commune, le programme croit qu'il s'agit de deux sociétés distinctes
      et n'en retient qu'une.
    ② CONTEXTE D'APPEL — Cinq appels, tous dans ce programme. `charger_referentiel`
      l'appelle pour chaque nom et chaque code du référentiel. `main` l'appelle
      pour composer la clé de chaque stratégie, pour chaque valeur à confronter à
      l'univers autorisé, et pour chaque clé des chiffres de référence figés.
      Depuis le 27-09-2026, les noms de stratégie lus au journal ne passent plus
      par elle : ils se comparent par égalité (`noms_d_une_strategie`, au contrat).
    ③ ENTRÉE — `s` : le texte à mettre en forme, par exemple `'C5-ETENDU-10'` ou
      `'Bureau Veritas'`. N'importe quelle valeur est acceptée : elle est
      convertie en texte avant traitement.
    ④ CONDITIONS D'ENTRÉE — Aucune. `None` est accepté et donne `'NONE'`.
    ⑤ SORTIE — UNE valeur : un texte en majuscules ne portant que des lettres et
      des chiffres. `'C5-ETENDU-10'` devient `'C5ETENDU10'`.
      [rend: 1]
    ⑥ TRAITEMENT — ① convertir en texte · ② passer en majuscules · ③ ne garder
      que les lettres et les chiffres, ce qui fait tomber tirets, tirets bas,
      espaces, points et parenthèses.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Comparer les noms tels quels a déjà fait disparaître des
      opérations entières. Le journal écrit `C5-ETENDU-10` et le registre
      `C5E10-QA-V1` avec `C5-ETENDU-10` dans son intitulé : sans mise en forme
      commune, les tirets et la casse suffisent à empêcher le rapprochement, et
      la stratégie est mesurée sur zéro opération sans qu'aucune erreur
      n'apparaisse.
    ⑨ CE QUI CLOCHE —
      ① Les accents sont retirés avec les autres caractères non alphanumériques,
      et non transformés en leur lettre de base. `SOCIÉTÉ` devient `SOCIT` et
      `SOCIETE` devient `SOCIETE` : deux écritures d'un même nom qui restent
      différentes après mise en forme, alors que le but est précisément de les
      rapprocher. Vérifié le 19-09-2026 : aucun nom du référentiel ni du journal
      ne porte d'accent aujourd'hui, donc le défaut ne se voit pas.
      ② `None` devient `'NONE'` au lieu d'une chaîne vide. Une valeur absente
      devient alors un nom comparable à celui d'une entreprise qui s'appellerait
      NONE.
    ⑩ EFFET — Aucun. Elle ne lit ni n'écrit rien, ne touche pas au réseau,
      n'affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels
      ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le registre des stratégies : le fichier `cac40_strategies.csv`, une ligne par stratégie, qui porte leur état civil — identifiant, réglages, résultats connus
      le journal des opérations : le fichier où s'écrit chaque opération simulée refermée, avec son prix d'entrée, son prix de sortie et son résultat
      C5-ETENDU-10 : le nom de la stratégie vivante ; ses seuils et son horizon sont lus dans `donnees/cac40_strategies.csv`.
      l'univers : la liste des valeurs sur lesquelles une stratégie a le droit d'acheter, désignées par leur mnémonique
      l'univers autorisé : la liste des valeurs qu'une stratégie a le droit de jouer, écrite dans le registre des stratégies
      le rapprochement : le fait de reconnaître que deux écritures différentes désignent le même fichier ou la même entreprise
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    return ''.join(c for c in str(s).upper() if c.isalnum())

def nombre(x, defaut=None):
    """Convertit en nombre ou rend le defaut — ne devine JAMAIS.

    ① RÔLE — Transformer en nombre ce qui est lu dans un fichier de tableau, où
      tout est du texte, et dire clairement quand ce n'est pas possible plutôt
      que de fabriquer une valeur. Les fichiers du projet écrivent les nombres
      de plusieurs façons : le registre porte `+4.0%` pour un objectif de gain
      et `-2.5%` pour une perte acceptée, et une cellule peut être vide.
    ② CONTEXTE D'APPEL — Onze appels, tous dans ce programme. `stats` pour chaque
      résultat d'opération · `courbe_capital` pour chaque cours de clôture,
      chaque prix d'entrée et chaque résultat · `temoins` pour chaque cours de
      l'indice · `calibrage` pour chaque chiffre de référence et pour la somme
      de contrôle · `ligne` pour l'objectif, la perte acceptée, le seuil de
      validation et le résultat promis.
    ③ ENTRÉE — `x` : la valeur à convertir, en général une cellule de tableau
      comme `'+4.0%'` ou `'1 234,5'` · `defaut` : ce qu'il faut rendre quand la
      conversion échoue, `None` par défaut. Les appelants qui somment des euros
      passent `0.0`, ceux qui veulent savoir si la valeur existe laissent `None`.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur, de deux formes. Un nombre à virgule quand la
      conversion réussit. La valeur de `defaut` quand elle échoue. Mesuré le
      19-09-2026 : `'+4.0%'` rend `4.0`, `'1 234,5'` rend `1234.5`, et `None`
      rend `None`.
      [rend: 1]
    ⑥ TRAITEMENT — ① convertir en texte · ② remplacer la virgule décimale par un
      point · ③ retirer le signe pourcent · ④ retirer les espaces, qui servent de
      séparateur de milliers · ⑤ convertir en nombre à virgule · ⑥ rendre le
      défaut si la conversion échoue.
    ⑦ UNITÉ — CELLE DE LA VALEUR REÇUE, ET ELLE N'EST PAS CONSERVÉE. Le signe
      pourcent est retiré sans que la valeur soit divisée par cent : `'+4.0%'`
      rend `4.0`, pas `0.04`. C'est à l'appelant de savoir dans quelle unité il
      travaille.
    ⑧ POURQUOI — Rendre un défaut plutôt que de deviner. Une cellule vide dans la
      colonne du résultat d'une opération n'est pas un zéro : c'est une valeur
      qu'on n'a pas. L'appelant qui peut vivre avec un zéro le demande
      explicitement ; celui qui ne le peut pas reçoit `None` et décide lui-même.
      Sans cette séparation, une colonne vide passerait pour une opération à
      résultat nul et fausserait tous les cumuls.
    ⑨ CE QUI CLOCHE —
      ① Le signe pourcent est retiré sans conversion, et c'est précisément le
      genre de silence qui a déjà coûté un faux chiffre au projet : le point mort
      a été calculé le 12-09-2026 à 38,51 % au lieu de 43,08 % parce que deux
      fonctions portant le même nom attendaient l'une des pourcents et l'autre
      des fractions. Ici, un appelant qui croirait recevoir une fraction
      obtiendrait un résultat cent fois trop grand, et plausible.
      ② Les espaces sont retirés partout, pas seulement entre les chiffres.
      `'1 2'` devient `12` : deux valeurs séparées par un espace deviennent un
      seul nombre, sans erreur.
      ③ Seules deux familles d'erreurs sont rattrapées. Une valeur d'un type qui
      n'accepte pas la conversion en texte ferait tomber le programme.
    ⑩ EFFET — Aucun. Elle ne lit ni n'écrit rien, ne touche pas au réseau,
      n'affiche rien.
    ⑪ TERMINAISON — Rend toujours la main dans les cas rencontrés. Aucun de ses
      appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le point mort : le taux de réussite en dessous duquel une stratégie perd
        de l'argent
      le registre des stratégies : le fichier `cac40_strategies.csv`, une ligne par stratégie, qui porte leur état civil — identifiant, réglages, résultats connus
      la perte acceptée : le pourcentage de baisse à partir duquel la position se referme sur une perte
      une fraction : la façon d'écrire un pourcentage entre 0 et 1 — 0,040 pour +4 % — par opposition au pourcent, qui écrirait 4.0
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    try:
        return float(str(x).replace(',', '.').replace('%', '').replace(' ', ''))
    except (TypeError, ValueError):
        return defaut

# ---------------------------------------------------------------- calculs
def wilson_borne_basse(gagnantes, n, z=1.96):
    """Borne basse a 95 % du taux de reussite — formule de WILSON.
    Decision 1 du 15/08 : Wilson remplace Wald (moins fiable a petit echantillon).
    Rend None sous 10 operations : annoncer un intervalle serait trompeur.

    ① RÔLE — Donner le taux de réussite le plus défavorable qui reste compatible
      avec ce qui a été observé, pour qu'une stratégie ne soit jamais jugée sur
      un taux brut que le hasard suffirait à expliquer. Une stratégie qui affiche
      3 gagnantes sur 5 a un taux brut de 60 %, mais cinq opérations ne prouvent
      rien : la borne basse dit jusqu'où la vérité peut descendre.
    ② CONTEXTE D'APPEL — Un seul appel, dans `ligne`, une fois par ligne écrite,
      donc deux fois par stratégie vivante. Elle reçoit le nombre d'opérations
      gagnantes et le nombre total d'opérations de la comptabilité en cours.
    ③ ENTRÉE — `gagnantes` : le nombre d'opérations terminées en gain ·
      `n` : le nombre total d'opérations terminées · `z` : le nombre d'écarts
      types qui fixe le niveau de confiance, 1.96 par défaut pour 95 %, et
      l'unique appelant ne le change jamais.
    ④ CONDITIONS D'ENTRÉE — `gagnantes` ne doit pas dépasser `n`, sans quoi le
      calcul rend un nombre dépourvu de sens ; rien ne le vérifie.
    ⑤ SORTIE — UNE valeur, de deux formes. Un pourcentage entre 0 et 100 quand il
      y a au moins dix opérations. `None` en dessous de dix. Mesuré le
      19-09-2026 : 6 gagnantes sur 10 rendent 31,27 %, et 6 sur 9 rendent `None`.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre `None` en dessous de dix opérations · ② calculer le
      taux observé · ③ appliquer la formule de Wilson, qui corrige le centre du
      taux observé et lui retranche une marge d'autant plus large que
      l'échantillon est petit · ④ rendre le résultat en pourcents.
    ⑦ UNITÉ — `gagnantes` et `n` en NOMBRE D'OPÉRATIONS TERMINÉES · le résultat
      en POURCENTS entre 0 et 100, jamais en fraction · `z` sans unité.
    ⑧ POURQUOI — Wilson plutôt que la formule ordinaire, décidé le 15-08-2026.
      La formule ordinaire centre l'intervalle sur le taux observé, ce qui la
      rend fausse aux petits échantillons et aux taux proches de 0 ou de 100 :
      elle peut descendre sous 0 % ou dépasser 100 %. Wilson ne le fait jamais.
      Et le refus de répondre en dessous de dix opérations vient de ce qu'un
      intervalle calculé sur trois opérations est si large qu'il n'exclut rien :
      l'afficher donnerait à croire qu'on sait quelque chose. Mesuré le
      19-09-2026 sur le vrai journal, les deux stratégies vivantes comptent trois
      opérations chacune : la colonne de la borne basse est VIDE dans les quatre
      lignes écrites, et le verdict porte « echantillon insuffisant ».
    ⑨ CE QUI CLOCHE —
      ① Le seuil de dix opérations est écrit en dur dans la fonction, alors que
      le registre des stratégies porte déjà un seuil de validation par stratégie.
      Mesuré le 19-09-2026 : ce seuil vaut 50 pour les deux stratégies vivantes.
      Deux chiffres règlent donc la même idée, à deux endroits, sans lien entre
      eux — et un chiffre qui existe ailleurs ne se recopie pas (R-708).
      ② Aucune vérification que `gagnantes` tient dans `n`. Avec 12 gagnantes sur
      10 opérations, la formule rend un nombre sans lever, et ce nombre serait
      écrit dans l'historique comme n'importe quel autre.
      ③ `n` est au dénominateur sans garde, mais le refus en dessous de dix
      opérations l'écarte : `n` valant zéro rend `None` avant tout calcul.
    ⑩ EFFET — Aucun. Elle ne lit ni n'écrit rien, ne touche pas au réseau,
      n'affiche rien.
    ⑪ TERMINAISON — Rend toujours la main dans les cas rencontrés. Aucun de ses
      appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      une comptabilité : une façon de compter le résultat. Il y en a DEUX, qui
        ne s'additionnent jamais : « un jeton » et « jetons illimités »
      le registre des stratégies : le fichier `cac40_strategies.csv`, une ligne par stratégie, qui porte leur état civil — identifiant, réglages, résultats connus
      la borne basse : la valeur en dessous de laquelle ne tombe qu'un tirage sur vingt
      le taux de réussite : la part des opérations qui se sont refermées sur un gain, écrite en pourcent
      une stratégie : une règle qui dit QUOI acheter, avec son objectif de gain, sa perte acceptée et son horizon
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if n < 10:
        return None
    p = gagnantes / n
    d = 1 + z*z/n
    c = p + z*z/(2*n)
    r = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n))
    return 100 * (c - r) / d

def _frais_du_proprietaire():
    """Le taux vient de MODULE_POSITIONS, jamais d une copie (R-708, 12-09-2026).

    ① RÔLE — Aller chercher le taux de frais là où il est écrit, au lieu de le
      recopier ici. Le taux de frais du courtier vit à UN SEUL endroit du
      système, la variable `FRAIS_TAUX` de `programmes/MODULE_POSITIONS.py`, qui
      vaut 0,0015 soit 0,15 % par ordre. Le recopier créerait une seconde source
      qui dériverait le jour où le tarif change, sans que rien ne le dise.
    ② CONTEXTE D'APPEL — AUCUN APPELANT. Vérifié le 19-09-2026 par recherche de
      son nom dans tout le dossier `programmes/` : il n'apparaît qu'à sa propre
      définition. Le taux de frais est bien lu chez son propriétaire, mais par un
      autre chemin : `point_mort_en_pourcents` passe le module entier au calcul
      du point mort, qui y prend lui-même le taux.
    ③ ENTRÉE — Aucun paramètre.
    ④ CONDITIONS D'ENTRÉE — Le fichier `MODULE_POSITIONS.py` doit se trouver dans
      le dossier de ce programme ou l'un de ses sous-dossiers, et porter une
      variable nommée `FRAIS_TAUX` dont la valeur se convertit en nombre.
    ⑤ SORTIE — UNE valeur : le taux de frais d'un ordre. Mesuré le 19-09-2026 en
      l'appelant à la main : 0.0015.
      [rend: 1]
    ⑥ TRAITEMENT — ① parcourir le dossier du programme et ses sous-dossiers ·
      ② y chercher un fichier nommé `MODULE_POSITIONS.py` ou `MODULE POSITIONS.py`
      · ③ le charger comme un module · ④ rendre la valeur de sa variable
      `FRAIS_TAUX` convertie en nombre · ⑤ si aucun des deux noms n'est trouvé,
      lever une erreur plutôt que de rendre une valeur de repli.
    ⑦ UNITÉ — Une FRACTION, jamais un pourcent : 0,0015 vaut 0,15 %. Confondre
      les deux donne des frais cent fois trop grands, et plausibles.
    ⑧ POURQUOI — Lever plutôt que rendre une valeur de repli. Un taux de repli
      serait une seconde source : le jour où le courtier change son tarif, le
      système continuerait de calculer avec l'ancien sans que rien ne l'annonce.
      Une erreur qui arrête le programme est visible ; un chiffre périmé ne l'est
      pas. Le tarif appliqué est celui du compte Fortuneo Progress, tranché par
      Jean-Luc le 11-08-2026 : 0,15 % par ordre sur la valeur échangée, et non un
      forfait.
    ⑨ CE QUI CLOCHE —
      ① Elle n'est appelée par personne, et elle marche. C'est du code mort qui
      donne l'impression que le taux est lu ici, alors qu'il l'est ailleurs.
      ② La valeur trouvée est rendue telle quelle, sans contrôle d'ordre de
      grandeur : un `FRAIS_TAUX` passé par erreur à 0,15 au lieu de 0,0015
      serait accepté et appliquerait 15 % de frais par ordre.
      ③ Le parcours ne retire aucun dossier, contrairement à la fonction `_p` du
      même programme qui écarte `archives`, `.git`, `__pycache__` et
      `_site_travail`. Une ancienne copie du module rangée en archive sous le
      dossier du programme pourrait être prise. Vérifié le 19-09-2026 : le
      dossier `programmes/` ne porte aujourd'hui aucun sous-dossier autre que
      `__pycache__`, donc le cas ne se produit pas.
    ⑩ EFFET — LIT l'arborescence du dossier du programme et EXÉCUTE le fichier
      `MODULE_POSITIONS.py` qu'elle y trouve, ce qui déroule tout ce que ce
      fichier fait à son chargement. N'écrit aucun fichier, ne touche pas au
      réseau.
    ⑪ TERMINAISON — Rend la main. LÈVE une erreur de chargement de module quand
      aucun fichier portant l'un des deux noms n'est trouvé. Un de ses appels
      peut ne pas revenir : l'exécution du module chargé peut elle-même lever.
      [sort: non]
    ⑫ DÉFINITIONS
      le propriétaire d'un chiffre : le seul fichier où ce chiffre est écrit ;
        tous les autres le lisent chez lui au lieu de le recopier
      `archives` : le dossier du dépôt où sont rangées les versions tombées, sous un nom qui dit pourquoi elles sont tombées
      une fraction : la façon d'écrire un pourcentage entre 0 et 1 — 0,040 pour +4 % — par opposition au pourcent, qui écrirait 4.0
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    import os as _os, importlib.util as _ilu
    for _r, _sd, _fs in _os.walk(_os.path.dirname(_os.path.abspath(__file__))):
        for _n in ("MODULE_POSITIONS.py", "MODULE POSITIONS.py"):
            if _n in _fs:
                _sp = _ilu.spec_from_file_location("_mp_f", _os.path.join(_r, _n))
                _m = _ilu.module_from_spec(_sp); _sp.loader.exec_module(_m)
                return float(_m.FRAIS_TAUX)
    raise ImportError("MODULE_POSITIONS introuvable : on ne recopie PAS son taux")


def point_mort_en_pourcents(tp_pct, sl_pct, frais_par_ordre=None):
    """Taux de reussite en dessous duquel la strategie perd de l argent.

    ICI, TOUT EST EN POURCENTS : tp=4.0, sl=2.5, frais=0.15.

    X1 de Cowork, 12-09-2026, ET C EST LA CAUSE DE MA QUASI-FAUTE DU SOIR :
      « Deux fonctions portent le meme nom, prennent les deux memes arguments,
       et les attendent dans des unites OPPOSEES. Tu as corrige la conversion
       des frais et laisse debout la cause. »
    `MODULE_JUGEMENT.point_mort(0.040, 0.025)` travaille en FRACTIONS et rend
    43,08. Celle-ci travaille en POURCENTS et rend 43,08 aussi. **Deux chemins,
    deux unites, un seul nom : j ai vu `0.15` en venant du monde des fractions
    et j ai cru a un facteur cent.**
    Ce qui m a arrete n etait ni un test ni un raisonnement, mais une donnee
    ecrite hier — `historique_mesures.csv` portait deja 43,1. **La prochaine
    fois, la valeur ecrite hier sera peut-etre celle qui est fausse.**

    DONC : LE CALCUL VIT A UN SEUL ENDROIT. Cette fonction ne calcule plus,
    elle CONVERTIT et delegue au proprietaire — MODULE_JUGEMENT — exactement
    comme les frais delegent a MODULE_POSITIONS.

    ① RÔLE — Donner à chaque stratégie le taux de réussite en dessous duquel elle
      perd de l'argent, compte tenu de son objectif de gain, de sa perte acceptée
      et des frais. Sans ce chiffre, un taux de réussite nu ne veut rien dire :
      55 % de réussite est excellent avec un objectif de +5 % et une perte
      acceptée de −2 %, et ruineux avec +1,2 % et −1 %. Cette fonction NE CALCULE
      PAS : elle convertit les unités du registre vers celles du propriétaire du
      calcul, et lui passe la main.
    ② CONTEXTE D'APPEL — Un seul appel, dans `ligne`, une fois par ligne écrite,
      donc quatre fois par passage du circuit du soir avec les deux stratégies
      vivantes au 19-09-2026. Elle reçoit l'objectif et la perte acceptée lus au
      registre des stratégies, et jamais le troisième paramètre.
    ③ ENTRÉE — `tp_pct` : l'objectif de gain en POURCENTS, `4.0` pour +4 %, tel
      que `nombre` le rend après avoir retiré le signe pourcent de la cellule
      `+4.0%` du registre · `sl_pct` : la perte acceptée en POURCENTS, `-2.5`
      pour −2,5 %, signe négatif compris · `frais_par_ordre` : le taux de frais
      en POURCENTS, `None` par défaut, et l'unique appelant ne le passe jamais.
    ④ CONDITIONS D'ENTRÉE — LES DEUX PREMIERS PARAMÈTRES SONT DES POURCENTS, ET
      C'EST LE PIÈGE DE CE PROGRAMME. Passer des fractions rend un chiffre faux
      sans aucune erreur. Le résultat doit tomber entre 0 et 100, sans quoi la
      fonction lève.
    ⑤ SORTIE — UNE valeur, de deux formes. Un pourcentage entre 0 et 100 quand
      les deux premiers paramètres sont renseignés. `None` quand l'un des deux
      vaut `None`, ce qui arrive lorsque le registre ne porte pas l'objectif ou
      la perte acceptée. Mesuré le 19-09-2026 : `4.0` et `-2.5` rendent
      43,0838…, écrit `43.1` dans l'historique.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre `None` si l'objectif ou la perte acceptée manque ·
      ② charger le module propriétaire du calcul · ③ diviser les trois valeurs
      par cent pour passer des pourcents aux fractions, en prenant la valeur
      absolue de la perte acceptée · ④ appeler le calcul du propriétaire en lui
      passant aussi le module qui détient le taux de frais · ⑤ refuser un
      résultat hors de l'intervalle de 0 à 100.
    ⑦ UNITÉ — EN ENTRÉE des POURCENTS : `4.0` vaut +4 %, `-2.5` vaut −2,5 %,
      `0.15` vaudrait 0,15 %. EN SORTIE un POURCENTAGE entre 0 et 100. Le
      propriétaire du calcul, lui, travaille en FRACTIONS — c'est toute la raison
      d'être de cette fonction.
    ⑧ POURQUOI — Le calcul ne vit qu'à un seul endroit, parce que deux
      implémentations d'une même chose divergent toujours (R-708). Ici la
      divergence a failli produire un faux chiffre : deux fonctions ont porté le
      nom `point_mort`, pris les deux mêmes arguments et attendu des unités
      opposées. Croisées le 12-09-2026, elles rendaient 38,51 % au lieu de
      43,08 % — un chiffre plausible, qu'aucun contrôle de sortie n'aurait
      attrapé. Ce qui a arrêté l'erreur n'était ni un test ni un raisonnement,
      mais une valeur écrite la veille dans l'historique des mesures. Depuis, le
      nom du propriétaire porte son unité et cette fonction ne fait plus que
      convertir.
      Le module des positions est passé au calcul plutôt que le taux lui-même,
      parce que le propriétaire du taux est `programmes/MODULE_POSITIONS.py` : le
      lui passer entier lui permet d'y prendre le taux et d'appliquer les frais
      séparément à la sortie au gain et à la sortie au stop, qui ne coûtent pas
      la même chose.
    ⑨ CE QUI CLOCHE —
      ① Les deux modules voisins sont rechargés depuis le disque À CHAQUE APPEL.
      Sur un passage du circuit du soir avec deux stratégies vivantes, cela fait
      quatre appels, donc huit chargements de module, chacun exécutant le fichier
      entier. Rien n'est gardé d'un appel à l'autre.
      ② Le nom de cette fonction dit son unité, mais rien ne la fait respecter.
      Le propriétaire du calcul, lui, refuse une fraction supérieure à 1 en
      valeur absolue. Ici, recevoir `0.040` au lieu de `4.0` donnerait un
      résultat faux et plausible, et c'est exactement le sens dangereux : la
      garde de sortie ne ferme que la moitié bruyante du piège.
      ③ Le troisième paramètre n'a jamais été utilisé par personne. Vérifié le
      19-09-2026 : l'unique appelant ne passe que deux arguments.
    ⑩ EFFET — LIT l'arborescence du dossier du programme et EXÉCUTE deux fichiers
      voisins, `MODULE_JUGEMENT.py` et `MODULE_POSITIONS.py`, à chaque appel.
      N'écrit aucun fichier, ne touche pas au réseau, n'affiche rien.
    ⑪ TERMINAISON — Rend la main. LÈVE quand le résultat sort de l'intervalle de
      0 à 100, et quand l'un des deux fichiers voisins est introuvable. Un de ses
      appels peut ne pas revenir : le calcul du propriétaire lève lui-même si les
      fractions qu'il reçoit dépassent 1 en valeur absolue.
      [sort: non]
    ⑫ DÉFINITIONS
      le point mort : le taux de réussite en dessous duquel une stratégie perd
        de l'argent
      le propriétaire d'un calcul : le seul fichier où ce calcul est écrit ; les
        autres le lui délèguent au lieu de le refaire
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
      Cowork : le relecteur du projet, qui clone le dépôt, casse le code et rend ses cassures par écrit
      l'objectif de gain : le pourcentage de hausse à partir duquel la position se referme sur un gain
      la perte acceptée : le pourcentage de baisse à partir duquel la position se referme sur une perte
      la raison : le texte court qui dit pourquoi une lecture a échoué, retenu sous le nom `motif`
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
      le registre : gouvernance/REGISTRE_REGLES.md, le document qui porte les regles numerotees du projet ; une regle absente du registre n'existe pas
      le sens dangereux : celui des deux croisements d'unité qui rend un chiffre plausible au lieu d'un chiffre absurde, donc celui qu'aucun contrôle de sortie ne peut attraper
      une fraction : la façon d'écrire un pourcentage entre 0 et 1 — 0,040 pour +4 % — par opposition au pourcent, qui écrirait 4.0
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if tp_pct is None or sl_pct is None:
        return None
    _j = _jugement()
    _frais = None if frais_par_ordre is None else frais_par_ordre / 100.0
    _r = _j.point_mort_en_fractions(tp_pct / 100.0, abs(sl_pct) / 100.0,
                       frais=_frais, mod_positions=_positions())
    return _refuser_l_impossible(_r, tp_pct, sl_pct)


def _refuser_l_impossible(r, tp, sl):
    """UN POINT MORT HORS DE [0 ; 100] EST IMPOSSIBLE PAR CONSTRUCTION.

    Y1 de Cowork, 13-09-2026, et il n a pas fabrique un exemple : il a REPRODUIT
    ma quasi-faute du soir en croisant les deux fonctions homonymes.
        MESURER.point_mort(0.040, 0.025)  -> 500.69 %   absurde, et ca CRIE
        JUGEMENT.point_mort(4.0, 2.5)     ->  38.51 %   plausible, et ca SE TAIT
    **38,51 est exactement le chiffre que j avais failli produire. Aucun controle
    de sortie ne l attraperait jamais — c est le sens dangereux.**
    Cette garde ferme la moitie BRUYANTE : au-dessus de 100, on refuse. Elle ne
    ferme pas la silencieuse — c est le NOM qui s en charge desormais.

    ① RÔLE — Arrêter le programme plutôt que d'écrire dans l'historique un point
      mort qui ne peut pas exister. Un point mort est un taux de réussite : il
      vit forcément entre 0 et 100. En trouver un à 500,69 % prouve qu'une unité
      a été croisée quelque part en amont, et mieux vaut une erreur bruyante
      qu'un chiffre faux rangé dans un fichier que tout le système relit.
    ② CONTEXTE D'APPEL — Un seul appel, en dernière ligne de
      `point_mort_en_pourcents`, sur la valeur que le propriétaire du calcul
      vient de rendre. Jamais appelée ailleurs.
    ③ ENTRÉE — `r` : le point mort à contrôler, tel que le propriétaire du calcul
      l'a rendu · `tp` : l'objectif de gain reçu par l'appelant, repris tel quel
      pour le message d'erreur · `sl` : la perte acceptée, de même.
    ④ CONDITIONS D'ENTRÉE — Aucune. `None` est accepté et rendu tel quel.
    ⑤ SORTIE — UNE valeur : le point mort reçu, inchangé, quand il tient entre
      0 et 100 — ou `None` quand elle a reçu `None`. Elle ne rend RIEN dans
      l'autre cas : elle lève.
      [rend: 1]
    ⑥ TRAITEMENT — ① rendre `None` tel quel · ② lever si la valeur sort de
      l'intervalle de 0 à 100, en nommant dans le message la cause la plus
      probable · ③ sinon rendre la valeur inchangée.
    ⑦ UNITÉ — `r` en POURCENTS entre 0 et 100. `tp` et `sl` en POURCENTS, et ils
      ne servent qu'à composer le message : ils ne sont pas contrôlés.
    ⑧ POURQUOI — Cette garde ne ferme que la moitié bruyante du piège, et c'est
      assumé. Le 13-09-2026, Cowork a reproduit le croisement des deux fonctions
      homonymes dans les deux sens : passer des fractions à la fonction qui
      attend des pourcents rend 500,69 %, ce qui est absurde et se voit ; passer
      des pourcents à celle qui attend des fractions rend 38,51 %, ce qui est
      plausible et ne se voit pas. Aucun contrôle de sortie ne peut attraper le
      second cas : c'est le NOM de la fonction propriétaire, qui porte désormais
      son unité, qui s'en charge. Mesuré le 19-09-2026 : appelée avec 500,69,
      elle lève sur « point mort impossible : 500.69 % pour tp=0.04 sl=0.025 ».
    ⑨ CE QUI CLOCHE —
      ① La moitié silencieuse du piège reste ouverte, et la fonction le dit
      elle-même. Un point mort de 38,51 % passe ce contrôle sans difficulté.
      ② Les bornes de l'intervalle sont écrites en dur dans le contrôle ET
      recopiées dans le texte du message d'erreur. Deux endroits pour le même
      couple de nombres : élargir l'intervalle sans toucher le message ferait
      annoncer des bornes qui ne sont plus celles appliquées.
      ③ Le même contrôle existe aussi chez le propriétaire du calcul,
      `programmes/MODULE_JUGEMENT.py`, qui refuse lui aussi un résultat hors de
      0 à 100. La valeur est donc contrôlée deux fois de suite, avec deux
      messages différents.
    ⑩ EFFET — Aucun. Elle ne lit ni n'écrit rien, ne touche pas au réseau,
      n'affiche rien : elle lève ou elle rend.
    ⑪ TERMINAISON — Rend la main quand la valeur est acceptable. LÈVE une erreur
      de valeur sinon, ce qui remonte jusqu'à l'arrêt du programme, car rien ne
      la rattrape sur le chemin. Aucun de ses appels ne se termine : elle
      n'appelle personne.
      [sort: non]
    ⑫ DÉFINITIONS
      le point mort : le taux de réussite en dessous duquel une stratégie perd
        de l'argent
      le sens dangereux : celui des deux croisements d'unité qui rend un chiffre
        plausible au lieu d'un chiffre absurde, donc celui qu'aucun contrôle de
        sortie ne peut attraper
      Cowork : le relecteur du projet, qui clone le dépôt, casse le code et rend ses cassures par écrit
      l'objectif de gain : le pourcentage de hausse à partir duquel la position se referme sur un gain
      la perte acceptée : le pourcentage de baisse à partir duquel la position se referme sur une perte
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if r is None:
        return None
    if not (0.0 <= r <= 100.0):
        raise ValueError(
            f"point mort impossible : {r:.2f} % pour tp={tp} sl={sl}. "
            f"Un point mort est un TAUX DE REUSSITE — il ne peut pas sortir de "
            f"[0 ; 100]. Cause la plus probable : une UNITE croisee (pourcents "
            f"contre fractions).")
    return r


def _jugement():
    """Le proprietaire du calcul de point mort. On ne le reecrit pas (R-708).

    ① RÔLE — Mettre la main sur le fichier qui détient le calcul du point mort,
      pour le lui déléguer au lieu de le refaire ici. Deux implémentations d'une
      même chose divergent toujours (R-708), et celle-ci a failli produire un
      faux chiffre le 12-09-2026 : 38,51 % au lieu de 43,08 %.
    ② CONTEXTE D'APPEL — Un seul appel, dans `point_mort_en_pourcents`, à chaque
      calcul de point mort, donc quatre fois par passage du circuit du soir avec
      les deux stratégies vivantes au 19-09-2026.
    ③ ENTRÉE — Aucun paramètre.
    ④ CONDITIONS D'ENTRÉE — Le fichier `MODULE_JUGEMENT.py` doit se trouver dans
      le dossier de ce programme ou l'un de ses sous-dossiers.
    ⑤ SORTIE — UNE valeur : le module chargé, sur lequel l'appelant va chercher
      la fonction `point_mort_en_fractions`.
      [rend: 1]
    ⑥ TRAITEMENT — ① demander le chargement du fichier voisin nommé
      `MODULE_JUGEMENT.py`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le nom de la fonction cherchée chez le voisin porte son unité,
      et ce n'est pas de la décoration : elle travaille en FRACTIONS quand ce
      programme travaille en POURCENTS. Deux fonctions ont porté le même nom
      court, pris les deux mêmes arguments et attendu des unités opposées ;
      croisées, elles rendaient un chiffre plausible et faux.
    ⑨ CE QUI CLOCHE —
      ① Le module est rechargé depuis le disque à chaque appel : rien n'est
      gardé d'un calcul de point mort au suivant.
      ② Elle n'apporte rien qu'un appel direct au chargeur de fichiers voisins
      n'apporterait, et sa jumelle `_positions` fait exactement la même chose
      pour un autre nom de fichier.
    ⑩ EFFET — LIT l'arborescence du dossier du programme et EXÉCUTE le fichier
      `MODULE_JUGEMENT.py`, ce qui déroule tout ce que ce fichier fait à son
      chargement. N'écrit aucun fichier, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main. LÈVE une erreur de chargement de module quand
      le fichier est introuvable. Un de ses appels peut ne pas revenir :
      l'exécution du module chargé peut elle-même lever.
      [sort: non]
    ⑫ DÉFINITIONS
      le point mort : le taux de réussite en dessous duquel une stratégie perd
        de l'argent
      le propriétaire d'un calcul : le seul fichier où ce calcul est écrit ; les
        autres le lui délèguent au lieu de le refaire
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    return _charger_voisin("MODULE_JUGEMENT.py")


def _positions():
    """Le proprietaire du taux de frais.

    ① RÔLE — Mettre la main sur le fichier qui détient le taux de frais du
      courtier, pour le PASSER au calcul du point mort au lieu de recopier le
      taux ici. C'EST PAR CE CHEMIN, ET PAR AUCUN AUTRE, QUE CE PROGRAMME LIT LE
      TAUX DE FRAIS : le nombre 0,0015 n'est écrit nulle part dans ce fichier,
      vérifié le 19-09-2026 par recherche du littéral.
    ② CONTEXTE D'APPEL — Un seul appel, dans `point_mort_en_pourcents`, à chaque
      calcul de point mort, donc quatre fois par passage du circuit du soir avec
      les deux stratégies vivantes au 19-09-2026. Le module rendu est passé tel
      quel au calcul du propriétaire du point mort.
    ③ ENTRÉE — Aucun paramètre.
    ④ CONDITIONS D'ENTRÉE — Un fichier nommé `MODULE_POSITIONS.py` ou
      `MODULE POSITIONS.py` doit se trouver dans le dossier de ce programme ou
      l'un de ses sous-dossiers, et porter la variable `FRAIS_TAUX` et la
      fonction `frais_ordre` que le calcul du point mort y cherchera.
    ⑤ SORTIE — UNE valeur : le module chargé.
      [rend: 1]
    ⑥ TRAITEMENT — ① demander le chargement du fichier voisin, en essayant deux
      écritures du nom, avec tiret bas puis avec espace.
    ⑦ UNITÉ — Le taux que porte le module rendu est une FRACTION, jamais un
      pourcent : 0,0015 vaut 0,15 % par ordre. Confondre les deux donne des frais
      cent fois trop grands, et plausibles.
    ⑧ POURQUOI — Passer le module entier plutôt que le taux seul. Les frais sont
      proportionnels à la valeur échangée : une sortie au gain coûte plus cher
      qu'une sortie au stop, parce qu'on vend davantage. Le calcul du point mort
      a donc besoin de la fonction de frais, pas seulement du taux, pour chiffrer
      séparément les deux branches. Appliquer les frais de la branche gagnante
      aux deux donnait 32,96 % au lieu de 32,86 % sur un couple d'essai — écart
      trouvé le 29-08-2026, alors qu'un forfait de 300 € était écrit en dur chez
      le propriétaire du point mort pendant que le module des positions
      appliquait 0,15 % à l'entrée et à la sortie.
    ⑨ CE QUI CLOCHE —
      ① Le module est rechargé depuis le disque à chaque appel : rien n'est
      gardé d'un calcul de point mort au suivant.
      ② Ce programme porte une SECONDE façon de lire le même taux,
      `_frais_du_proprietaire`, qui charge le même fichier pour y prendre
      directement `FRAIS_TAUX`. Vérifié le 19-09-2026 : cette seconde fonction
      n'est appelée par personne. Deux chemins pour un même besoin, dont un
      mort.
      ③ La seconde écriture du nom, avec un espace, n'a plus de raison d'être :
      vérifié le 19-09-2026, le seul fichier de ce nom dans le dépôt est
      `programmes/MODULE_POSITIONS.py`, avec un tiret bas.
    ⑩ EFFET — LIT l'arborescence du dossier du programme et EXÉCUTE le fichier
      `MODULE_POSITIONS.py`, ce qui déroule tout ce que ce fichier fait à son
      chargement. N'écrit aucun fichier, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main. LÈVE une erreur de chargement de module quand
      aucun des deux noms n'est trouvé. Un de ses appels peut ne pas revenir :
      l'exécution du module chargé peut elle-même lever.
      [sort: non]
    ⑫ DÉFINITIONS
      le propriétaire d'un chiffre : le seul fichier où ce chiffre est écrit ;
        tous les autres le lisent chez lui au lieu de le recopier
      le point mort : le taux de réussite en dessous duquel une stratégie perd
        de l'argent
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
      une fraction : la façon d'écrire un pourcentage entre 0 et 1 — 0,040 pour +4 % — par opposition au pourcent, qui écrirait 4.0
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    return _charger_voisin("MODULE_POSITIONS.py", "MODULE POSITIONS.py")


def _charger_voisin(*noms):
    """Charge un fichier de programme voisin et rend le module obtenu.

    ① RÔLE — Donner accès à un autre fichier du dossier `programmes/` sans passer
      par le mécanisme d'importation ordinaire de Python, qui exigerait que ce
      dossier soit installé comme un paquet. C'est ce qui permet à ce programme
      de déléguer un calcul et un taux à leurs propriétaires au lieu de les
      recopier — deux implémentations d'une même chose divergent toujours (R-708).
    ② CONTEXTE D'APPEL — Deux appels, tous deux dans ce programme : `_jugement`
      pour le fichier qui détient le calcul du point mort, et `_positions` pour
      celui qui détient le taux de frais.
    ③ ENTRÉE — `noms` : un ou plusieurs noms de fichier à essayer dans l'ordre,
      donnés sans dossier. `_jugement` passe `'MODULE_JUGEMENT.py'`, `_positions`
      passe `'MODULE_POSITIONS.py'` puis `'MODULE POSITIONS.py'`.
    ④ CONDITIONS D'ENTRÉE — Au moins un nom doit être donné : le message d'erreur
      cite le premier, et le composer sur une liste vide ferait tomber la
      fonction sur une autre erreur que celle prévue.
    ⑤ SORTIE — UNE valeur : le module chargé. Elle ne rend RIEN quand aucun des
      noms n'est trouvé : elle lève.
      [rend: 1]
    ⑥ TRAITEMENT — ① partir du dossier de ce programme · ② le parcourir avec tous
      ses sous-dossiers · ③ dans chaque dossier visité, essayer les noms dans
      l'ordre donné · ④ au premier trouvé, le charger, l'exécuter et le rendre ·
      ⑤ si le parcours s'achève sans rien trouver, lever une erreur en nommant le
      premier nom cherché.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Lever plutôt que rendre une valeur de repli. Un repli silencieux
      ferait recalculer ici ce qui appartient à un autre fichier, et la copie
      dériverait le jour où l'original change, sans que rien ne le dise. Une
      erreur qui arrête le programme se voit ; un calcul périmé ne se voit pas.
      Le nom du module chargé est fabriqué à partir des huit premiers caractères
      du nom de fichier afin que deux fichiers différents ne se recouvrent pas
      dans la table des modules de Python.
    ⑨ CE QUI CLOCHE —
      ① Huit caractères ne suffisent pas à distinguer deux fichiers dont les noms
      commencent pareil. `MODULE_JUGEMENT.py` et `MODULE_POSITIONS.py` donnent
      tous deux `_v_MODULE_`, donc le même nom de module. Vérifié le 19-09-2026 :
      cela ne se voit pas aujourd'hui, parce que chaque module chargé est rendu
      directement à son appelant sans être rangé dans la table des modules de
      Python.
      ② Le parcours ne retire aucun dossier, contrairement à la fonction `_p` du
      même programme qui écarte `archives`, `.git`, `__pycache__` et
      `_site_travail`. Une ancienne copie rangée en archive sous le dossier du
      programme pourrait être chargée à la place de la version vivante, et
      l'ordre du parcours déciderait laquelle. Vérifié le 19-09-2026 : le dossier
      `programmes/` ne porte aujourd'hui aucun sous-dossier autre que
      `__pycache__`.
      ③ Le fichier trouvé est exécuté entièrement, y compris ce qu'il fait à son
      chargement. Un fichier voisin qui afficherait ou écrirait au chargement le
      ferait à chaque appel.
      ④ Rien n'est gardé d'un appel à l'autre : le même fichier est relu et
      réexécuté à chaque fois.
    ⑩ EFFET — LIT l'arborescence du dossier du programme et EXÉCUTE le fichier
      trouvé, ce qui déroule tout ce que ce fichier fait à son chargement.
      N'écrit aucun fichier, ne touche pas au réseau, n'affiche rien.
    ⑪ TERMINAISON — Rend la main avec le module chargé. LÈVE une erreur de
      chargement de module quand aucun des noms n'est trouvé. Un de ses appels
      peut ne pas revenir : l'exécution du fichier chargé peut elle-même lever ou
      ne pas se terminer.
      [sort: non]
    ⑫ DÉFINITIONS
      le propriétaire d'un calcul : le seul fichier où ce calcul est écrit ; les
        autres le lui délèguent au lieu de le refaire
      `archives` : le dossier du dépôt où sont rangées les versions tombées, sous un nom qui dit pourquoi elles sont tombées
      la table : `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740, qui porte les neuf seuils et le sens de comparaison de chacun
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    import os as _os, importlib.util as _ilu
    _base = _os.path.dirname(_os.path.abspath(__file__))
    for _r, _sd, _fs in _os.walk(_base):
        for _n in noms:
            if _n in _fs:
                _sp = _ilu.spec_from_file_location("_v_" + _n[:8],
                                                   _os.path.join(_r, _n))
                _m = _ilu.module_from_spec(_sp)
                _sp.loader.exec_module(_m)
                return _m
    raise ImportError(f"{noms[0]} introuvable : on ne reecrit PAS son calcul")

def serie_en_cours(pnls):
    """Nombre de gains (positif) ou de pertes (negatif) consecutifs, en partant de la fin.

    ① RÔLE — Dire si la stratégie est en train d'enchaîner les gains ou les
      pertes, et depuis combien d'opérations. C'est le seul indicateur du
      programme qui regarde l'ordre des opérations plutôt que leur somme : trois
      pertes de suite après dix gains ne se voient pas dans un cumul.
    ② CONTEXTE D'APPEL — Un seul appel, dans `stats`, une fois par comptabilité
      et par stratégie, donc quatre fois par passage du circuit du soir avec les
      deux stratégies vivantes au 19-09-2026.
    ③ ENTRÉE — `pnls` : la liste des résultats des opérations terminées, en
      euros, DANS L'ORDRE DU JOURNAL. `stats` la construit en lisant la colonne
      de résultat de la comptabilité en cours.
    ④ CONDITIONS D'ENTRÉE — La liste doit être dans l'ordre chronologique : la
      fonction la parcourt à l'envers en supposant que la dernière entrée est
      l'opération la plus récente. Rien ne le vérifie.
    ⑤ SORTIE — UNE valeur : un entier. Positif pour une série de gains, négatif
      pour une série de pertes, zéro sur une liste vide. Mesuré le 19-09-2026 sur
      les trois opérations de la comptabilité un jeton, +6 884,75 € puis
      −2 796,25 € puis −2 796,25 € : la fonction rend −2, écrit `-2` dans
      l'historique.
      [rend: 1]
    ⑥ TRAITEMENT — ① parcourir les résultats en partant du dernier · ② au premier
      résultat rencontré, poser la série à +1 s'il est en gain, à −1 sinon ·
      ③ continuer tant que les résultats suivants vont dans le même sens, en
      allongeant la série · ④ s'arrêter au premier changement de sens.
    ⑦ UNITÉ — `pnls` en EUROS · le résultat en NOMBRE D'OPÉRATIONS CONSÉCUTIVES,
      avec un signe qui dit le sens.
    ⑧ POURQUOI — Une série de pertes ne se voit pas dans un cumul. Une stratégie
      qui a gagné 10 000 € sur vingt opérations puis perdu cinq fois de suite
      affiche toujours un cumul positif : c'est la série qui dit que quelque
      chose a changé. Ce chiffre alimente un voyant du tableau de bord.
    ⑨ CE QUI CLOCHE —
      ① Un résultat exactement nul est compté comme une PERTE. Mesuré le
      19-09-2026 : une liste ne portant que la valeur zéro rend −1. Une opération
      qui rentre dans ses frais au centime près allongerait donc une série de
      pertes, ce que le mot « perte » ne laisse pas attendre.
      ② Le sens de la série et sa longueur sont portés par un seul nombre signé.
      Zéro veut dire DEUX choses : la liste était vide, ou l'appelant n'a pas
      d'opérations. Rien ne les distingue.
      ③ La condition qui allonge une série de gains exige un résultat
      strictement positif, celle qui allonge une série de pertes accepte zéro :
      les deux branches ne traitent donc pas le zéro de la même façon, mais la
      branche qui s'arrête rattrape le cas, donc le résultat reste cohérent.
    ⑩ EFFET — Aucun. Elle ne lit ni n'écrit rien, ne modifie pas la liste reçue,
      ne touche pas au réseau, n'affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels
      ne se termine : elle n'appelle personne.
      [sort: non]
    ⑫ DÉFINITIONS
      une comptabilité : une façon de compter le résultat. Il y en a DEUX, qui
        ne s'additionnent jamais : « un jeton » et « jetons illimités »
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
      un voyant : une case du tableau de bord qui vaut « vert » ou « rouge »
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      une stratégie : une règle qui dit QUOI acheter, avec son objectif de gain, sa perte acceptée et son horizon
      une série de pertes : une suite d'opérations perdantes qui se succèdent sans qu'aucune gagnante vienne l'interrompre
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    s = 0
    for p in reversed(pnls):
        if s == 0:
            s = 1 if p > 0 else -1
        elif p > 0 and s > 0:
            s += 1
        elif p <= 0 and s < 0:
            s -= 1
        else:
            break
    return s

def pertes_consecutives(pnls):
    """Nombre de pertes qui se suivent en fin de liste, zero si la derniere est un gain.

    ① RÔLE — Compter les pertes qui se suivent à la fin, pour allumer un voyant
      quand elles s'accumulent. Le tableau de bord passe au rouge à partir de
      cinq pertes consécutives : c'est le signal qu'une stratégie ne fonctionne
      plus comme elle le devrait, bien avant que son cumul ne devienne négatif.
    ② CONTEXTE D'APPEL — Un seul appel, dans `stats`, une fois par comptabilité
      et par stratégie, donc quatre fois par passage du circuit du soir avec les
      deux stratégies vivantes au 19-09-2026.
    ③ ENTRÉE — `pnls` : la liste des résultats des opérations terminées, en
      euros, DANS L'ORDRE DU JOURNAL.
    ④ CONDITIONS D'ENTRÉE — La liste doit être dans l'ordre chronologique : la
      fonction la parcourt à l'envers en supposant que la dernière entrée est
      l'opération la plus récente. Rien ne le vérifie.
    ⑤ SORTIE — UNE valeur : un entier positif ou nul. Zéro quand la dernière
      opération est un gain, ou quand la liste est vide. Mesuré le 19-09-2026 sur
      les trois opérations de la comptabilité un jeton : la fonction rend 2,
      écrit `2` dans l'historique.
      [rend: 1]
    ⑥ TRAITEMENT — ① parcourir les résultats en partant du dernier · ② compter
      tant qu'ils sont négatifs ou nuls · ③ s'arrêter au premier gain.
    ⑦ UNITÉ — `pnls` en EUROS · le résultat en NOMBRE D'OPÉRATIONS CONSÉCUTIVES.
    ⑧ POURQUOI — Compter depuis la fin, et non chercher la plus longue série de
      tout l'historique. La question posée est « où en est-on maintenant », pas
      « quel est le pire moment qu'on ait connu » : une série de huit pertes il y
      a six mois ne dit rien de l'état d'aujourd'hui, alors que trois pertes en
      cours en disent beaucoup.
    ⑨ CE QUI CLOCHE —
      ① Un résultat exactement nul est compté comme une PERTE. Mesuré le
      19-09-2026 : la liste formée d'un gain, d'une perte et d'un zéro rend 2.
      Une opération qui rentre dans ses frais au centime près rapprocherait donc
      le voyant du rouge, ce que le mot « perte » ne laisse pas attendre.
      ② Elle refait une partie du travail de `serie_en_cours`, qui rend déjà la
      même information sous forme de nombre négatif quand la série en cours est
      une série de pertes. Les deux chiffres sont écrits côte à côte dans
      l'historique : mesuré le 19-09-2026, `-2` et `2` sur la même ligne, et deux
      implémentations d'une même chose divergent toujours (R-708) — ici elles ne
      divergent que sur le zéro, qui n'allonge une série que dans l'une des deux.
      ③ Le seuil qui fait rougir le voyant, cinq, n'est pas ici : il est écrit
      dans la fonction `ligne` du même programme. Lire cette fonction ne dit donc
      pas à partir de quand le chiffre devient inquiétant.
    ⑩ EFFET — Aucun. Elle ne lit ni n'écrit rien, ne modifie pas la liste reçue,
      ne touche pas au réseau, n'affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels
      ne se termine : elle n'appelle personne.
      [sort: non]
    ⑫ DÉFINITIONS
      une comptabilité : une façon de compter le résultat. Il y en a DEUX, qui
        ne s'additionnent jamais : « un jeton » et « jetons illimités »
      le voyant : une case du tableau de bord qui vaut « vert » ou « rouge »
      le signal : le jour où la stratégie dit d'acheter ; l'achat lui-même a lieu à l'ouverture de la séance suivante
      un voyant : une case du tableau de bord qui vaut « vert » ou « rouge »
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      une stratégie : une règle qui dit QUOI acheter, avec son objectif de gain, sa perte acceptée et son horizon
      une série de pertes : une suite d'opérations perdantes qui se succèdent sans qu'aucune gagnante vienne l'interrompre
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    n = 0
    for p in reversed(pnls):
        if p <= 0:
            n += 1
        else:
            break
    return n

def pire_chute(pnls, capital=CAPITAL):
    """Plus forte baisse DEPUIS UN SOMMET (et non depuis le capital de depart).
    Correction du 15/08 : 100 000 -> 120 000 -> 105 000 est une chute de 12,5 %,
    meme si l'on reste en gain par rapport au depart.

    ① RÔLE — Mesurer le pire recul qu'aurait subi quelqu'un qui aurait suivi la
      stratégie depuis le début, en partant du plus haut atteint et non du
      capital de départ. C'est ce chiffre qui dit ce qu'il aurait fallu supporter
      pour rester en place, et c'est souvent lui qui décide d'abandonner une
      stratégie, bien plus que son résultat final.
    ② CONTEXTE D'APPEL — Un seul appel, dans `stats`, une fois par comptabilité
      et par stratégie, donc quatre fois par passage du circuit du soir avec les
      deux stratégies vivantes au 19-09-2026. `stats` ne lui passe que la liste
      des résultats.
    ③ ENTRÉE — `pnls` : la liste des résultats des opérations terminées, en
      euros, DANS L'ORDRE DU JOURNAL · `capital` : le capital de départ,
      100 000 € par défaut, et l'unique appelant ne le change jamais.
    ④ CONDITIONS D'ENTRÉE — La liste doit être dans l'ordre chronologique : la
      fonction la parcourt du début à la fin en cumulant. Rien ne le vérifie, et
      un désordre change le résultat sans qu'aucune erreur ne se produise.
    ⑤ SORTIE — DEUX valeurs : la pire chute en pourcents, puis la même en euros.
      Les deux sont négatives ou nulles. Mesuré le 19-09-2026 sur les trois
      opérations de la comptabilité un jeton, +6 884,75 € puis −2 796,25 € puis
      −2 796,25 € : −5,23 % et −5 592,50 €.
      [rend: 2]
    ⑥ TRAITEMENT — ① partir du capital de départ · ② pour chaque opération,
      ajouter son résultat au capital courant · ③ tenir à jour le plus haut
      atteint · ④ mesurer l'écart au plus haut · ⑤ garder le pire écart rencontré,
      en euros et en part du plus haut de ce moment-là.
    ⑦ UNITÉ — `pnls` et `capital` en EUROS · la première valeur rendue en
      POURCENTS, la seconde en EUROS. Les deux sont NÉGATIVES : une chute de
      12,5 % s'écrit −12,5.
    ⑧ POURQUOI — Depuis le sommet, et non depuis le départ. Corrigé le
      15-08-2026 : un capital qui monte de 100 000 € à 120 000 € puis redescend à
      105 000 € a subi une chute de 12,5 %, même s'il reste en gain par rapport au
      départ. Compter depuis le départ aurait annoncé une chute nulle, alors que
      quelqu'un qui a vu son compte passer de 120 000 à 105 000 a bien perdu
      15 000 €. La part est rapportée au plus haut du MOMENT DE LA CHUTE, pas au
      plus haut de toute l'histoire : c'est ce qu'on ressentait à cet instant.
    ⑨ CE QUI CLOCHE —
      ① Le paramètre `capital` n'est jamais passé par personne. Vérifié le
      19-09-2026 : l'unique appelant n'envoie que la liste. Un lecteur croit
      pouvoir régler quelque chose que rien ne règle.
      ② Le capital de départ vaut 100 000 €, qui est le capital engagé par UNE
      position, alors que les résultats sont cumulés comme s'ils s'étaient suivis
      sur un seul compte. La part en pourcents dépend donc directement de ce
      choix : le même enchaînement de résultats rapporté à 10 000 € donnerait une
      chute dix fois plus profonde en pourcents.
      ③ La chute en euros est identique dans les deux comptabilités alors que la
      chute en pourcents diffère. Mesuré le 19-09-2026 : −5 592,50 € dans les deux
      cas, mais −5,23 % en un jeton et −5,39 % en jetons illimités, parce que le
      sommet atteint n'est pas le même (106 884,75 € contre 103 694,00 €). Ce
      n'est pas une faute, mais deux colonnes voisines qui semblent se
      contredire.
      ④ Les opérations sont supposées s'être suivies sans se chevaucher. C'est
      vrai de la comptabilité un jeton, qui n'ouvre qu'une position à la fois,
      mais pas de la comptabilité jetons illimités, où plusieurs positions
      peuvent vivre en même temps : leur chute réelle n'est alors pas la somme
      de leurs résultats pris l'un après l'autre.
    ⑩ EFFET — Aucun. Elle ne lit ni n'écrit rien, ne modifie pas la liste reçue,
      ne touche pas au réseau, n'affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas : une liste vide rend
      deux zéros. Aucun de ses appels ne se termine : elle n'appelle personne.
      [sort: non]
    ⑫ DÉFINITIONS
      une comptabilité : une façon de compter le résultat. Il y en a DEUX, qui
      jetons illimités : la seconde comptabilité, où toute position s'ouvre sans limite ; elle ne correspond à aucun portefeuille réel.
      la pire chute : la plus forte baisse du cumul depuis un sommet precedent.
      un jeton : la comptabilité où une seule position peut être ouverte à la fois par stratégie ; un signal reçu pendant une position est ignoré.
"""
    equity = capital
    sommet = capital
    creux_eur = 0.0
    creux_pct = 0.0
    for p in pnls:
        equity += p
        sommet = max(sommet, equity)
        ecart = equity - sommet
        if ecart < creux_eur:
            creux_eur = ecart
            creux_pct = 100 * ecart / sommet
    return creux_pct, creux_eur

def rapport_gain_secousses(courbe):
    """Gain moyen quotidien rapporte a l'ampleur des variations quotidiennes,
    calcule sur la COURBE DE CAPITAL jour apres jour (decision 3 du 15/08),
    et non sur les operations, qui ne sont pas independantes.
    Rend None si la courbe quotidienne n'est pas disponible.

    ① RÔLE — Dire si le gain obtenu vaut les secousses subies pour l'obtenir.
      Deux stratégies qui rapportent autant ne se valent pas si l'une monte
      régulièrement et l'autre par à-coups : ce rapport les sépare. Plus il est
      élevé, plus le gain est régulier.
    ② CONTEXTE D'APPEL — Un seul appel, dans `main`, UNE SEULE FOIS par passage,
      sur la courbe reconstruite à partir de TOUTES les opérations du journal.
      La valeur obtenue est ensuite recopiée sur chaque ligne écrite.
    ③ ENTRÉE — `courbe` : la valeur du portefeuille séance après séance, telle
      que `courbe_capital` la rend, ou `None` quand les cours n'ont pas été
      trouvés.
    ④ CONDITIONS D'ENTRÉE — La courbe doit compter au moins trente points, et
      donner au moins trente variations exploitables. En dessous, la fonction
      refuse de répondre.
    ⑤ SORTIE — UNE valeur, de deux formes. Un nombre sans unité, ramené à
      l'année, quand la courbe est assez longue. `None` quand elle est absente,
      trop courte, ou que toutes les variations sont identiques. Mesuré le
      19-09-2026 sur la courbe du dépôt, 694 séances : 0,3513…, écrit `0.35`
      dans l'historique.
      [rend: 1]
    ⑥ TRAITEMENT — ① refuser si la courbe est absente ou compte moins de trente
      points · ② calculer la variation relative d'une séance à la suivante, en
      écartant les séances de valeur nulle · ③ refuser s'il reste moins de trente
      variations · ④ calculer la moyenne de ces variations · ⑤ calculer leur
      dispersion · ⑥ refuser si la dispersion est nulle · ⑦ diviser la moyenne
      par la dispersion et multiplier par la racine de 252.
    ⑦ UNITÉ — `courbe` en EUROS · le résultat SANS UNITÉ, ramené à l'année. Le
      nombre 252 est le nombre de séances de bourse d'une année : c'est ce qui
      transforme un rapport quotidien en rapport annuel, et il permet de comparer
      deux mesures faites sur des durées différentes.
    ⑧ POURQUOI — Sur la courbe de capital jour après jour, et non sur les
      opérations, décidé le 15-08-2026. Les opérations ne sont pas indépendantes
      les unes des autres — elles se suivent, se chevauchent, portent parfois sur
      la même valeur — et la dispersion calculée sur elles n'aurait pas de sens.
      Le refus en dessous de trente points vient de ce qu'une dispersion calculée
      sur quelques valeurs est elle-même si imprécise que le rapport n'apprend
      rien : mieux vaut ne rien annoncer.
    ⑨ CE QUI CLOCHE —
      ① La valeur est calculée UNE FOIS sur toutes les opérations réunies, puis
      recopiée à l'identique sur chaque ligne. Mesuré le 19-09-2026 : les quatre
      lignes écrites portent toutes `0.35`, y compris celles des deux
      comptabilités dont les cumuls diffèrent (+1 292,25 € contre −1 898,50 €), et
      celles des deux stratégies. La colonne laisse croire à un chiffre propre à
      chaque stratégie.
      ② La courbe reçue passe par toutes les séances de l'historique des cours,
      y compris celles où aucune position n'était ouverte. Mesuré le 19-09-2026 :
      694 séances pour cinq opérations. Les longues périodes sans position
      apportent des variations nulles qui écrasent la dispersion et gonflent le
      rapport.
      ③ Le nombre 252 est écrit en dur. Le nombre réel de séances de bourse d'une
      année varie d'une année à l'autre, et le fichier des cours du projet le
      donnerait exactement.
      ④ Les séances de valeur nulle sont écartées sans être comptées, ce qui peut
      faire passer une courbe de trente points en dessous du seuil sans que rien
      ne le dise : la fonction rend alors `None` pour une raison différente de
      celle du premier refus, et l'appelant ne peut pas les distinguer.
    ⑩ EFFET — Aucun. Elle ne lit ni n'écrit rien, ne modifie pas la courbe reçue,
      ne touche pas au réseau, n'affiche rien.
    ⑪ TERMINAISON — Rend toujours la main dans les cas rencontrés. Aucun de ses
      appels ne se termine : elle n'appelle personne.
      [sort: non]
    ⑫ DÉFINITIONS
      une comptabilité : une façon de compter le résultat. Il y en a DEUX, qui
        ne s'additionnent jamais : « un jeton » et « jetons illimités »
      la courbe de capital : la valeur qu'aurait eue le portefeuille à la fin de
        chaque séance de bourse, positions ouvertes comprises
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      le fichier des cours : le fichier où les séances s'empilent sans jamais être réécrites ; au dépôt, c'est donnees/claude_cours_nouveaux.csv.
      une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if not courbe or len(courbe) < 30:
        return None
    rend = []
    for a, b in zip(courbe, courbe[1:]):
        if a:
            rend.append((b - a) / a)
    if len(rend) < 30:
        return None
    m = sum(rend) / len(rend)
    var = sum((x - m) ** 2 for x in rend) / (len(rend) - 1)
    et = math.sqrt(var)
    if et == 0:
        return None
    return (m / et) * math.sqrt(252)

def stats(operations, cle_pnl):
    """Statistiques d'une comptabilite. cle_pnl choisit la colonne de resultat.

    ① RÔLE — Réduire une liste d'opérations terminées aux dix chiffres qui
      décrivent une comptabilité : combien d'opérations, combien de gagnantes,
      quel taux, quel cumul, quelle espérance, quel rapport entre les gains et
      les pertes, où en est la série, combien de pertes de suite, et quelle a été
      la pire chute. C'est le passage obligé entre le journal et la ligne écrite.
    ② CONTEXTE D'APPEL — Deux appelants. ① `main`, deux fois par stratégie
      vivante, une fois par comptabilité, donc quatre fois par passage avec les
      deux stratégies vivantes au 19-09-2026. ② `calibrage`, une fois, sur
      TOUTES les opérations du journal, pour vérifier que le cumul qu'elle
      calcule est bien la somme des résultats.
    ③ ENTRÉE — `operations` : la liste des opérations terminées, chacune sous
      forme de dictionnaire lu au journal · `cle_pnl` : le nom de la colonne de
      résultat à lire, `'pnl_net_eur'` pour la comptabilité un jeton et
      `'pnl_net_convention_eur'` pour la comptabilité jetons illimités.
    ④ CONDITIONS D'ENTRÉE — La liste doit être dans l'ordre chronologique, parce
      que la série en cours, les pertes consécutives et la pire chute en
      dépendent. Rien ne le vérifie.
    ⑤ SORTIE — UNE valeur : un dictionnaire de DIX clés — `n`, `gagnantes`,
      `taux`, `cumul`, `esperance`, `pf`, `serie`, `pertes`, `chute_pct`,
      `chute_eur` — plus la liste des résultats sous la clé `pnls`. Les mêmes
      clés dans les deux cas, mais sur une liste vide le taux, l'espérance et le
      rapport gains sur pertes valent `None` et tout le reste vaut zéro.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire la colonne de résultat de chaque opération, en comptant
      zéro quand elle est vide ou illisible · ② rendre un jeu de valeurs à zéro
      si la liste est vide · ③ compter les opérations en gain · ④ additionner
      séparément les gains et les pertes · ⑤ appeler le calcul de la pire chute ·
      ⑥ composer le dictionnaire, taux et espérance compris.
    ⑦ UNITÉ — Le cumul, l'espérance et la chute en euros sont en EUROS · le taux
      et la chute en pourcents sont en POURCENTS, jamais en fractions · le nombre
      d'opérations, les gagnantes, la série et les pertes consécutives sont des
      NOMBRES D'OPÉRATIONS TERMINÉES · le rapport gains sur pertes est SANS UNITÉ.
    ⑧ POURQUOI — La colonne de résultat est choisie par l'appelant, et c'est ce
      qui fait exister les deux comptabilités. Le même journal, lu sur deux
      colonnes différentes, donne deux histoires : « un jeton » compte au prix de
      sortie réellement observé, « jetons illimités » au prix théorique de
      l'objectif ou du stop. Mesuré le 19-09-2026 sur les trois opérations d'une
      stratégie vivante : +1 292,25 € d'un côté, −1 898,50 € de l'autre. CES DEUX
      CHIFFRES NE S'ADDITIONNENT JAMAIS : ce sont deux façons de raconter les
      mêmes opérations, pas deux portefeuilles.
      Et le rapport gains sur pertes vaut `None` plutôt que l'infini quand il n'y
      a aucune perte, parce qu'une stratégie sans aucune perte n'a pas un rapport
      infiniment bon : elle a un échantillon trop pauvre pour qu'on se prononce.
    ⑨ CE QUI CLOCHE —
      ① Une colonne de résultat vide ou illisible est comptée comme un ZÉRO.
      L'opération existe alors dans le compte, dans le taux et dans la série,
      avec un résultat nul, et comme le zéro est traité en perte, elle allonge
      une série de pertes. Une donnée manquante devient ainsi une opération
      perdante, sans aucun message.
      ② Le rapport gains sur pertes range les résultats nuls du côté des pertes,
      alors qu'une valeur nulle n'ajoute rien à leur somme : le classement est
      donc sans effet sur ce rapport-là, mais il en a un sur le compte des
      gagnantes, qui exige un résultat strictement positif.
      ③ Le dictionnaire rendu porte, sous la clé `pnls`, la liste complète des
      résultats, qu'aucun appelant n'utilise. Vérifié le 19-09-2026 : ni `main`
      ni `calibrage` ne la lisent.
      ④ Le cas de la liste vide est écrit une seconde fois, à la main, avec dix
      clés à recopier. Un chiffre ou une clé ajoutés plus bas et oubliés ici
      feraient tomber l'appelant sur une clé manquante, uniquement quand une
      stratégie n'a aucune opération.
    ⑩ EFFET — Aucun. Elle ne lit ni n'écrit aucun fichier, ne modifie pas la liste
      reçue, ne touche pas au réseau, n'affiche rien.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas dans les cas
      rencontrés. Aucun de ses appels ne se termine : `nombre`, `pire_chute`,
      `serie_en_cours` et `pertes_consecutives` rendent toutes la main.
      [sort: non]
    ⑫ DÉFINITIONS
      une comptabilité : une façon de compter le résultat. Il y en a DEUX, qui
      le rapport gains sur pertes : la somme des gains divisée par la somme des
        pertes, en valeur absolue
      l'espérance : le résultat moyen d'une opération, en euros
      le journal des opérations : le fichier où s'écrit chaque opération simulée refermée, avec son prix d'entrée, son prix de sortie et son résultat
      jetons illimités : la seconde comptabilité, où toute position s'ouvre sans limite ; elle ne correspond à aucun portefeuille réel.
      la pire chute : la plus forte baisse du cumul depuis un sommet precedent.
      ne s'additionnent jamais : « un jeton » et « jetons illimités »
      un jeton : la comptabilité où une seule position peut être ouverte à la fois par stratégie ; un signal reçu pendant une position est ignoré.
      une clé : le texte obtenu après rapprochement, qui sert à comparer deux noms et n'est jamais affiché à un lecteur
      une comptabilite : la facon de compter les resultats, et il y en a deux, jamais additionnees — un jeton, une seule position a la fois avec 100 000 € simules, et jetons illimites, toutes les occurrences du signal mesurees.
      une stratégie : une règle qui dit QUOI acheter, avec son objectif de gain, sa perte acceptée et son horizon
      une série de pertes : une suite d'opérations perdantes qui se succèdent sans qu'aucune gagnante vienne l'interrompre
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    pnls = [nombre(o.get(cle_pnl), 0.0) for o in operations]
    n = len(pnls)
    if n == 0:
        return dict(n=0, gagnantes=0, taux=None, cumul=0.0, esperance=None, pf=None,
                    serie=0, pertes=0, chute_pct=0.0, chute_eur=0.0, pnls=[])
    gag = sum(1 for p in pnls if p > 0)
    gains = sum(p for p in pnls if p > 0)
    pertes_tot = abs(sum(p for p in pnls if p <= 0))
    cp, ce = pire_chute(pnls)
    return dict(n=n, gagnantes=gag, taux=100.0*gag/n, cumul=sum(pnls),
                esperance=sum(pnls)/n, pf=(gains/pertes_tot if pertes_tot else None),
                serie=serie_en_cours(pnls), pertes=pertes_consecutives(pnls),
                chute_pct=cp, chute_eur=ce, pnls=pnls)

# ---------------------------------------------------------------- temoins
def courbe_capital(operations, base, strategie):
    """Reconstruit la valeur du portefeuille jour apres jour.
    Sert au rapport gain/secousses et au temoin miroir.
    Rend (dates, courbe) ou (None, None) si les cours manquent.

    ① RÔLE — Reconstituer ce qu'aurait valu le portefeuille à la fin de chaque
      séance de bourse, positions ouvertes comprises. Le journal ne donne que le
      résultat d'une opération refermée : il ne dit pas ce qui se passait entre
      l'entrée et la sortie. Sans cette reconstitution, on ne peut ni mesurer la
      régularité des gains ni comparer la stratégie à l'indice jour par jour.
    ② CONTEXTE D'APPEL — Un seul appel, dans `main`, UNE SEULE FOIS par passage,
      avant la boucle sur les stratégies. Elle reçoit toutes les opérations du
      journal, et son troisième paramètre vaut `None`.
    ③ ENTRÉE — `operations` : toutes les opérations terminées du journal ·
      `base` : le dossier où chercher le fichier maître des cours, celui reçu sur la
      ligne de commande · `strategie` : TOUJOURS `None`, et la fonction ne s'en
      sert jamais.
    ④ CONDITIONS D'ENTRÉE — Le fichier maître des cours doit exister — sinon elle
      lève (A-442) — et porter des colonnes
      nommées `valeur`, `date` et `close`. La colonne `date` est obligatoire : son
      absence fait tomber la fonction. Les opérations doivent porter `date_entree`,
      `date_sortie`, `valeur` et `prix_entree`.
    ⑤ SORTIE — DEUX valeurs. La liste des dates de séance triées et la valeur du
      portefeuille à chacune, deux listes de même longueur, quand des cours ont
      été trouvés. DEUX valeurs `None` quand aucun fichier de cours n'a donné de
      cours exploitable. Mesuré le 19-09-2026 sur le dépôt : 694 séances, de
      100 000,00 € au départ à 104 088,50 € à la fin.
      [rend: 2]
    ⑥ TRAITEMENT — ① lire le fichier maître des cours, ou lever s'il manque, et ranger chaque clôture par
      valeur et par date · ② lever si aucun cours n'a été lu (A-471 ; avant le 24-09-2026, elle abandonnait en silence) · ③ dresser la
      liste triée de toutes les séances connues · ④ ranger les opérations par
      date d'entrée · ⑤ parcourir les séances dans l'ordre : ouvrir une position
      si une opération entre ce jour-là et qu'aucune n'est ouverte, sinon reporter
      la valeur courante · ⑥ tant qu'une position est ouverte, ajouter son gain ou
      sa perte du moment, calculé sur le cours de clôture du jour · ⑦ à la date de
      sortie, encaisser le résultat définitif du journal et refermer la position.
    ⑦ UNITÉ — Les cours et les prix d'entrée en EUROS · la courbe en EUROS · les
      dates en année-mois-jour, comparées comme du texte · le capital engagé vaut
      100 000 € par position.
    ⑧ POURQUOI — Le gain du moment est calculé sur le capital engagé et non sur
      le nombre de titres, parce que chaque position engage la même somme,
      100 000 €, avec une quantité fractionnaire : une variation de +2 % du cours
      vaut +2 000 € quel que soit le prix de l'action. C'est ce qui rend deux
      opérations comparables entre elles.
      À la date de sortie, la valeur du jour est REMPLACÉE par le résultat écrit
      au journal, et non par le gain du moment : le journal tient compte des
      frais et du prix de sortie réellement obtenu, et c'est lui qui fait foi.
    ⑨ CE QUI CLOCHE —
      ① QUATRE OPÉRATIONS SUR CINQ DISPARAISSENT QUAND ELLES ENTRENT LE MÊME
      JOUR. Les opérations sont rangées dans un dictionnaire dont la clé est la
      date d'entrée : deux opérations entrées le même jour écrasent la première.
      Mesuré le 19-09-2026 sur le vrai journal de cinq opérations : quatre
      portent la date d'entrée 2026-08-21, il ne reste que deux clés, et la
      courbe se termine à 104 088,50 €, c'est-à-dire 100 000 € plus le résultat
      de DEUX opérations seulement. Aucun message ne le dit.
      ② Le troisième paramètre n'est jamais utilisé. Son nom, `strategie`,
      laisse croire que la courbe est propre à une stratégie, alors qu'elle est
      construite sur toutes les opérations du journal confondues. L'appelant lui
      passe `None`.
      ③ Les noms de valeurs sont mis en forme à la main, en passant en majuscules
      et en remplaçant tirets et tirets bas par des espaces, alors que ce
      programme porte déjà une fonction faite pour cela, `_norm`, qui retire tous
      les caractères non alphanumériques. Deux façons de faire la même chose dans
      le même fichier, et deux implémentations d'une même chose divergent
      toujours (R-708) : ici, `UNIBAIL-RODAMCO` et `UNIBAIL_RODAMCO` se
      rejoignent par les deux chemins, mais `UNIBAIL RODAMCO WESTFIELD` et
      `UNIBAILRODAMCOWESTFIELD` ne se rejoignent que par le second.
      ④ **[RÉGLÉ LE 24-09-2026, A-442 : plus aucun repli ; le maître seul, et son absence arrête.]** L'historique des cours qui grandit n'est jamais lu. Les cours sont
      cherchés dans `cac40_ohlcv.csv` et `cours_nouveaux.csv`, jamais dans
      `donnees/cours_maitre.csv`, le fichier unique où s'empilent désormais les
      séances. Vérifié le 19-09-2026 : le nom `cours_maitre` n'apparaît nulle
      part dans ce programme. La courbe s'arrête donc à ce que portent les deux
      anciens fichiers.
      ⑤ Un cours manquant un jour donné compte comme un gain du moment NUL, et
      non comme une valeur inconnue. La courbe reste alors plate au lieu de
      signaler un trou.
      ⑥ La courbe ne connaît qu'UNE position à la fois, ce qui correspond à la
      comptabilité un jeton. Elle est pourtant la seule courbe du programme, et
      les chiffres qui en dérivent sont écrits aussi sur les lignes de la
      comptabilité jetons illimités.
      ⑦ Les dates sont comparées comme du texte. Cela fonctionne tant qu'elles
      s'écrivent année-mois-jour avec deux chiffres partout ; une date écrite
      autrement se classerait au mauvais endroit sans erreur.
    ⑩ EFFET — LIT le fichier maître des cours, qu'elle cherche dans toute
      l'arborescence du dossier reçu. N'écrit aucun fichier, ne modifie pas les
      opérations reçues, ne touche pas au réseau, n'affiche rien.
    ⑪ TERMINAISON — Rend la main. LÈVE `FileNotFoundError` si le fichier maître des cours manque, ou s'il ne porte aucun cours lisible (A-471) — voulu, A-442. PEUT LEVER si un fichier de cours ne porte pas
      de colonne `date`. Un de ses appels peut ne pas revenir : `lire_csv` lève
      si un fichier trouvé ne se lit pas.
      [sort: non]
    ⑫ DÉFINITIONS
      une comptabilité : une façon de compter le résultat. Il y en a DEUX, qui
      le gain du moment : ce que rapporterait la position si elle était refermée
        au cours de clôture du jour, frais non déduits
      le témoin miroir : ce qu'aurait rapporté l'indice en n'étant exposé que les
        jours où une position était ouverte
      la courbe de capital : la valeur qu'aurait eue le portefeuille à la fin de
        chaque séance de bourse, positions ouvertes comprises
      jetons illimités : la seconde comptabilité, où toute position s'ouvre sans limite ; elle ne correspond à aucun portefeuille réel.
      la boucle : la tache planifiee qui lit les signaux et rend compte
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
      un jeton : la comptabilité où une seule position peut être ouverte à la fois par stratégie ; un signal reçu pendant une position est ignoré.
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      une stratégie : une règle qui dit QUOI acheter, avec son objectif de gain, sa perte acceptée et son horizon
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    cours = {}
    # LE SEUL FICHIER MAITRE, jamais les anciens (A-442) ; son absence arrete.
    ch = _p(base, 'cours_maitre.csv')
    if not ch:
        raise FileNotFoundError(
            "ARRET : le fichier maitre des cours, donnees/cours_maitre.csv, est "
            "introuvable. Aucun repli sur les anciens fichiers de cours (A-442).")
    for r in lire_csv(ch):
        v = (r.get('valeur') or '').strip().upper().replace('_', ' ').replace('-', ' ')
        c = nombre(r.get('close'))
        if c is not None:
            cours.setdefault(v, {})[r['date']] = c
    if not cours:
        # UN MAITRE VIDE ARRETE, COMME UN MAITRE ABSENT (A-471, 24-09-2026).
        raise FileNotFoundError(
            "ARRET : le fichier maitre des cours, %s, ne porte aucun cours lisible." % ch)
    seances = sorted({d for v in cours.values() for d in v})
    equity = CAPITAL
    courbe = []
    ouvertes = {o['date_entree']: o for o in operations if o.get('date_entree')}
    en_cours = None
    for d in seances:
        if en_cours is None and d in ouvertes:
            o = ouvertes[d]
            val = (o.get('valeur') or '').strip().upper().replace('_', ' ').replace('-', ' ')
            pe = nombre(o.get('prix_entree'))
            if pe:
                en_cours = dict(valeur=val, pe=pe, fin=o.get('date_sortie'),
                                pnl=nombre(o.get('pnl_net_eur'), 0.0))
        if en_cours:
            px = cours.get(en_cours['valeur'], {}).get(d)
            latent = ((px - en_cours['pe']) / en_cours['pe'] * CAPITAL) if px else 0.0
            courbe.append(equity + latent)
            if d == en_cours['fin']:
                equity += en_cours['pnl']
                en_cours = None
                courbe[-1] = equity
        else:
            courbe.append(equity)
    return seances, courbe

def temoins(base, seances, courbe, operations):
    """Deux temoins de comparaison (decision 4 du 15/08).
    PERMANENT : 100 000 EUR places sur l'indice du debut a la fin (buy and hold).
    MIROIR    : expose au marche exactement quand la strategie l'est.
    Indice attendu : PX1GR (dividendes reinvestis). Rend 'non disponible' si absent —
    JAMAIS de valeur inventee.

    ① RÔLE — Donner les deux points de comparaison sans lesquels un résultat ne
      veut rien dire. Gagner 5 % est excellent si l'indice a perdu 10 %, et
      médiocre s'il en a gagné 20 %. Le premier témoin répond à « valait-il mieux
      ne rien faire », le second à « le gain vient-il de la stratégie ou
      simplement du fait d'être sur le marché ces jours-là ».
    ② CONTEXTE D'APPEL — Un seul appel, dans `main`, UNE SEULE FOIS par passage,
      après la reconstitution de la courbe et avant la boucle sur les stratégies.
      Les deux valeurs obtenues sont ensuite recopiées sur chaque ligne écrite.
    ③ ENTRÉE — `base` : le dossier où chercher le fichier de l'indice, celui reçu
      sur la ligne de commande · `seances` : la liste des dates de séance, telle
      que `courbe_capital` la rend, ou `None` · `courbe` : la courbe du capital,
      REÇUE MAIS JAMAIS UTILISÉE · `operations` : toutes les opérations du
      journal, pour savoir quels jours une position était ouverte.
    ④ CONDITIONS D'ENTRÉE — Aucune : une liste de séances vide ou absente et un
      fichier d'indice introuvable sont traités et donnent « non disponible ». Le
      fichier d'indice, s'il existe, doit porter les colonnes `date` et `close`.
    ⑤ SORTIE — DEUX valeurs : le témoin permanent puis le témoin miroir, chacun
      sous forme de texte. Un pourcentage signé quand l'indice est disponible,
      par exemple `+12.40 %`. Le texte `'non disponible'` dans les deux cas
      sinon. Mesuré le 19-09-2026 sur le dépôt : `'non disponible'` et
      `'non disponible'`, parce qu'aucun fichier d'indice n'y existe — vérifié
      par recherche des noms `indice` et `px1gr` dans tout le dépôt, qui ne
      trouve aucun fichier.
      [rend: 2]
    ⑥ TRAITEMENT — ① essayer trois noms de fichier d'indice, et s'arrêter au
      premier trouvé · ② ranger chaque clôture par date · ③ abandonner si aucun
      cours d'indice n'a été lu, ou si la liste des séances est vide · ④ ne
      garder que les séances pour lesquelles l'indice a une valeur · ⑤ abandonner
      s'il en reste moins de deux · ⑥ le témoin permanent est la variation de
      l'indice entre la première et la dernière de ces séances · ⑦ relever les
      jours où au moins une position était ouverte · ⑧ le témoin miroir multiplie
      les variations de l'indice, jour après jour, uniquement sur ces jours-là.
    ⑦ UNITÉ — Les cours de l'indice en POINTS · les deux témoins en POURCENTS,
      rendus SOUS FORME DE TEXTE avec leur signe et le caractère pourcent, prêts
      à être écrits dans l'historique.
    ⑧ POURQUOI — Rendre « non disponible » plutôt qu'un zéro, décidé le
      15-08-2026 : un zéro se lirait comme un indice qui n'a pas bougé, et la
      stratégie paraîtrait meilleure qu'elle n'est. Une donnée absente n'est pas
      une donnée nulle, et aucune valeur n'est inventée.
      L'indice attendu est celui qui réinvestit les dividendes, parce qu'une
      stratégie qui détient les actions touche les dividendes : la comparer à un
      indice qui les ignore la flatterait d'environ trois points par an.
      Le témoin miroir multiplie les variations au lieu de les additionner, parce
      que c'est ainsi que se composent des rendements : +10 % puis −10 % ne
      ramènent pas au point de départ mais à −1 %.
    ⑨ CE QUI CLOCHE —
      ① Le témoin miroir n'est pas exposé les jours qu'il devrait. Les variations
      sont parcourues d'une séance disponible à la suivante, et la variation est
      retenue quand la SECONDE des deux est un jour exposé. Le jour d'entrée en
      position n'apporte donc aucune variation, alors qu'il est bien un jour
      d'exposition, et le lendemain de la sortie en apporte une si la sortie est
      comprise dans l'intervalle.
      ② Les jours exposés sont relevés sur TOUTES les opérations du journal, sans
      distinction de stratégie ni de comptabilité, puis la valeur obtenue est
      recopiée sur chaque ligne écrite. La colonne laisse croire à un chiffre
      propre à chaque stratégie.
      ③ Le paramètre `courbe` est reçu et jamais utilisé. Vérifié le 19-09-2026 :
      son nom n'apparaît pas une seule fois dans le corps de la fonction.
      ④ Les trois noms de fichier d'indice sont épelés en dur, et le contrôle
      s'éteint entièrement si le fichier arrive sous un quatrième nom. Le critère
      qui tranche tient en une question : si je renomme un fichier, mon contrôle
      change-t-il d'avis ? Ici oui, donc il épelle.
      ⑤ Le premier fichier trouvé est pris même s'il est vide ou illisible : la
      recherche s'arrête après lui, sans essayer les suivants.
      ⑥ Aucun message n'est affiché quand les témoins sont indisponibles. Mesuré
      le 19-09-2026 : les quatre lignes écrites portent `non disponible` dans les
      deux colonnes, et l'affichage du programme n'en dit pas un mot. Les deux
      témoins décidés le 15-08-2026 ne fonctionnent donc pas, et rien ne le
      signale depuis.
    ⑩ EFFET — LIT un fichier d'indice, qu'elle cherche dans toute l'arborescence
      du dossier reçu. N'écrit aucun fichier, ne modifie rien de ce qu'elle
      reçoit, ne touche pas au réseau, n'affiche rien.
    ⑪ TERMINAISON — Rend la main. PEUT LEVER si le fichier d'indice trouvé ne
      porte pas de colonne `date`. Un de ses appels peut ne pas revenir :
      `lire_csv` lève si le fichier ne se lit pas.
      [sort: non]
    ⑫ DÉFINITIONS
      le témoin permanent : ce qu'auraient rapporté 100 000 € placés sur l'indice
        du début à la fin, sans rien faire
      le témoin miroir : ce qu'aurait rapporté l'indice en n'étant exposé que les
        jours où une position était ouverte
      une comptabilité : une façon de compter le résultat. Il y en a DEUX, qui
        ne s'additionnent jamais : « un jeton » et « jetons illimités »
      la boucle : la tache planifiee qui lit les signaux et rend compte
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
      une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    idx = {}
    for f in ('cac40_indice.csv', 'indice_px1gr.csv', 'px1gr.csv'):
        ch = _p(base, f)
        if ch:
            for r in lire_csv(ch):
                c = nombre(r.get('close'))
                if c is not None:
                    idx[r['date']] = c
            break
    if not idx or not seances:
        return 'non disponible', 'non disponible'
    dispo = [d for d in seances if d in idx]
    if len(dispo) < 2:
        return 'non disponible', 'non disponible'
    perm = 100 * (idx[dispo[-1]] - idx[dispo[0]]) / idx[dispo[0]]
    # miroir : ne cumule le rendement de l'indice que les jours ou une position existe
    jours_exposes = set()
    for o in operations:
        de, ds = o.get('date_entree'), o.get('date_sortie')
        if de and ds:
            jours_exposes.update(d for d in seances if de <= d <= ds)
    mir = 1.0
    for a, b in zip(dispo, dispo[1:]):
        if b in jours_exposes and idx[a]:
            mir *= 1 + (idx[b] - idx[a]) / idx[a]
    return f"{perm:+.2f} %", f"{100*(mir-1):+.2f} %"

# ---------------------------------------------------------------- calibrage
def charger_referentiel(base):
    """Le referentiel est le SEUL endroit ou un nom et un code se rencontrent
    (chapitre GESTION DE L'IDENTITE DES VALEURS, regle I-3). Sans lui, aucun
    programme ne peut relier « BUREAU_VERITAS » a « BVI ».
    Rend un dictionnaire forme normalisee -> mnemonique.

    ① RÔLE — Construire la table qui relie le nom d'une entreprise à son code de
      bourse, pour que le programme puisse vérifier qu'une opération porte sur
      une valeur autorisée. Le journal des opérations écrit `BUREAU_VERITAS`, le
      registre des stratégies écrit `BVI` : sans cette table, les deux écritures
      ne se rejoignent jamais et toute opération paraît porter sur une valeur
      inconnue.
    ② CONTEXTE D'APPEL — Un seul appel dans ce programme, dans `main`, UNE SEULE
      FOIS par passage, avant la boucle sur les stratégies ; et les épreuves
      `tests/EPREUVES_DU_REFERENTIEL_DE_LA_MESURE_Mer_30-09-2026.py`. La table obtenue sert ensuite à
      traduire chaque valeur jouée avant de la confronter à l'univers autorisé.
    ③ ENTRÉE — `base` : le dossier où chercher le référentiel, celui reçu sur la
      ligne de commande, `"$GITHUB_WORKSPACE"` dans le circuit du soir.
    ④ CONDITIONS D'ENTRÉE — Un tableau .csv dont le nom commence par
      `REFERENTIEL_VALEURS` doit se trouver DIRECTEMENT dans le dossier `donnees/`
      de la racine reçue (depuis le 30-09-2026 ; avant, à la racine elle-même). Il
      doit porter une colonne `mnemonique`.
    ⑤ SORTIE — UNE valeur : un dictionnaire qui va d'un nom mis en forme vers un
      code de bourse. Un dictionnaire VIDE quand aucun fichier n'a été trouvé.
      Mesuré le 19-09-2026, avant la réparation : appelée sur la racine du dépôt,
      elle rendait un dictionnaire vide. Depuis le 30-09-2026, appelée sur la
      racine, elle relie BUREAU_VERITAS à BVI (40 valeurs connues).
      [rend: 1]
    ⑥ TRAITEMENT — ① lister le dossier `donnees/` de la racine reçue · ② y garder
      les fichiers dont le nom commence par `REFERENTIEL_VALEURS` et finit par
      « .csv » en minuscules · ③ prendre le plus récent par la date de son nom
      (`COMMUN.le_plus_recent`) — le même choix que la collecte du soir,
      `COLLECTER_ABC_GITHUB.py`, qui elle s arrête quand il n y en a pas · ④ pour
      chaque ligne, relever le code de bourse · ⑤ enregistrer, sous leur forme
      mise en forme, le nom usuel, le nom de l'onglet et le nom officiel, tous
      pointant vers ce code · ⑥ enregistrer aussi le code lui-même, pour qu'un
      fichier qui écrit déjà le code soit reconnu.
    ⑦ UNITÉ — UN NOMBRE D'ÉCRITURES CONNUES, et non un nombre de valeurs : la
      même entreprise apporte jusqu'à quatre entrées. Mesuré le 19-09-2026 sur
      le fichier `donnees/REFERENTIEL_VALEURS_v3_Lun_17-08-2026_10h54.csv` :
      93 entrées.
    ⑧ POURQUOI — Une seule table, et un seul endroit où un nom et un code se
      rencontrent. Une même entreprise s'écrit différemment selon le fichier :
      `UNIBAIL-RODAMCO-WESTFIELD` dans l'un, `UNIBAIL_RODAMCO` dans l'autre. Sans
      table commune, le programme croit qu'il s'agit de deux sociétés distinctes
      et en ignore une. Le code de bourse est la clé, jamais le nom, parce que
      c'est lui qui ne change pas.
    ⑨ CE QUI CLOCHE —
      ① et ② RÉGLÉS LE 30-09-2026 (A-495 (d)) : le référentiel est cherché dans
      `donnees/`, par la règle de la collecte du soir, le plus récent l emporte.
      Mesuré sur une copie de la version en attente : « referentiel : 40 valeurs
      connues », plus aucune alerte « HORS UNIVERS », lignes écrites dans
      l historique des mesures identiques avant et après. La même règle reste
      écrite deux fois, ici et dans la collecte (R-708) : une fonction commune
      manque. Ce qui était mesuré :
      ① LE RÉFÉRENTIEL N'EST JAMAIS TROUVÉ DANS LE CIRCUIT DU SOIR. Le dossier
      reçu est listé à plat, alors que le fichier vit dans `donnees/`. Mesuré le
      19-09-2026 en lançant le programme sur une copie du dépôt : l'affichage
      porte « ATTENTION : referentiel introuvable — le controle d'univers ne peut
      pas fonctionner ». La conséquence n'est pas un silence mais une FAUSSE
      ALERTE : Bureau Veritas, dont le code `BVI` figure bien dans l'univers
      autorisé des deux stratégies vivantes, est signalé « operation(s) sur une
      valeur HORS UNIVERS declare » parce que son nom n'a pas pu être traduit.
      Le même programme porte pourtant une fonction qui cherche dans toute
      l'arborescence, `_p`, dont il se sert pour le journal et pour le registre.
      ② Le premier fichier par ordre alphabétique est pris, et la boucle s'arrête
      là. Avec deux versions du référentiel côte à côte, c'est la première
      alphabétiquement qui gagne, donc pas forcément la plus récente. Là encore,
      la fonction `_p` du même programme sait départager par la date du nom.
      ③ Les trois colonnes de noms sont épelées en dur. Une colonne de nom
      ajoutée au référentiel ne serait pas reprise, et aucun message ne le
      dirait.
      ④ Une ligne sans code de bourse est passée en silence : la valeur n'entre
      pas dans la table et sera plus tard déclarée inconnue du référentiel.
      ⑤ Rien ne signale qu'un même nom mis en forme pointe vers deux codes
      différents : la dernière ligne lue l'emporte, sans message.
    ⑩ EFFET — LIT la liste du dossier `donnees/`, puis le référentiel retenu.
      Ajoute le dossier de ce programme au chemin des imports. N'écrit aucun
      fichier, ne touche pas au réseau, n'affiche rien.
    ⑪ TERMINAISON — Rend la main ; un dossier reçu absent rend une table vide.
      PEUT LEVER si le fichier trouvé ne se lit pas. Aucun de ses appels ne se
      termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le code de bourse : l'abréviation courte et stable qui désigne une valeur,
        par exemple `BVI` pour Bureau Veritas. C'est lui la clé, jamais le nom
      l'univers autorisé : la liste des valeurs qu'une stratégie a le droit de
        jouer, écrite dans le registre des stratégies
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
      hors univers : une valeur que Jean-Luc a volontairement retiree du champ, avec son motif ecrit dans la colonne `hors_univers` du referentiel
      la boucle : la tache planifiee qui lit les signaux et rend compte
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      la table : `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740, qui porte les neuf seuils et le sens de comparaison de chacun
      le journal des opérations : le fichier où s'écrit chaque opération simulée refermée, avec son prix d'entrée, son prix de sortie et son résultat
      le referentiel : le fichier qui donne l identite de chaque valeur — son nom usuel, son mnemonique, sa place de cotation, et le motif de son exclusion
      le référentiel : donnees/REFERENTIEL_VALEURS_*.csv, la liste des valeurs à suivre, avec pour chacune son mnémonique et sa place de cotation.
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
"""
    # LE RÉFÉRENTIEL VIT DANS donnees/, PAS À LA RACINE (A-495 (d), 30-09-2026) : la
    # liste à plat de la racine ne le trouvait jamais dans le circuit du soir, d'où
    # chaque soir la fausse alerte « HORS UNIVERS » sur Bureau Veritas et Unibail.
    # On le cherche par LA MÊME RÈGLE que la collecte du soir
    # (programmes/COLLECTER_ABC_GITHUB.py) : dans donnees/, un tableau .csv dont le
    # nom commence par REFERENTIEL_VALEURS, le plus récent par la date de son nom
    # (COMMUN.le_plus_recent). Même choix de fichier que la collecte, extension
    # comprise ; une seule différence : sans référentiel, la collecte s'arrête, la
    # mesure affiche « referentiel introuvable » et continue.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from COMMUN import le_plus_recent
    d = os.path.join(base, "donnees")
    cands = [f for f in (os.listdir(d) if os.path.isdir(d) else [])
             if f.upper().startswith("REFERENTIEL_VALEURS") and f.endswith(".csv")]
    corr = {}
    for f in ([os.path.join(d, le_plus_recent(cands))] if cands else []):
        for r in lire_csv(f):
            mn = (r.get('mnemonique') or '').strip().upper()
            if not mn:
                continue
            for champ in ('nom_usuel', 'onglet_google', 'nom_officiel_euronext'):
                v = (r.get(champ) or '').strip()
                if v:
                    corr[_norm(v)] = mn
            corr[_norm(mn)] = mn
    return corr


def operations_de(operations, carte, comptabilite=None):
    """Rend les operations du journal qui appartiennent a une strategie, et a une comptabilite.

    ① RÔLE — Dire, en un seul endroit, quelles lignes du journal comptent pour une
      stratégie et une comptabilité. C'est le cœur de la réparation du défaut 3 :
      une même vente est écrite une fois par comptabilité, et ne doit compter que
      dans la sienne.
    ② CONTEXTE D'APPEL — `main`, trois fois par stratégie vivante : toutes
      comptabilités (contrôle d'univers, lignes orphelines) ; `mesurer_une_strategie`,
      une fois par comptabilité — pour `main` comme pour `calibrage`, qui la
      rejoue sur le témoin (cinq vraies lignes et deux fabriquées).
    ③ ENTRÉE — `operations` : des lignes du journal · `carte` : une ligne du
      registre des stratégies, avec `id` et `nom` · `comptabilite` : `un_jeton`,
      `jetons_illimites`, ou None pour toutes.
    ④ CONDITIONS D'ENTRÉE — Aucune : une case absente vaut vide.
    ⑤ SORTIE — UNE valeur : la liste des lignes retenues, dans l'ordre du journal.
      [rend: 1]
    ⑥ TRAITEMENT — ① prendre les noms de la stratégie par `noms_d_une_strategie`
      (contrat) · ② garder les lignes dont le nom de stratégie est ÉGAL à l'un
      d'eux · ③ si une comptabilité est demandée, ne garder que les siennes.
    ⑦ UNITÉ — Des LIGNES du journal.
    ⑧ POURQUOI — Défaut 3 de A-491, 27-09-2026 : la mesure prenait chaque ligne
      dans les deux comptabilités, et rattachait les noms par morceau — « un jeton :
      3 operation(s) · cumul 1292.25 EUR » pour un seul trade réel à −2 796,25 €.
      Sortie de `main` pour être éprouvée CHAQUE SOIR par `calibrage` : Cowork a
      remis le défaut le 27-09 à 22h46 et tout ce qui était au dépôt est resté vert.
    ⑨ CE QUI CLOCHE — Le témoin est une copie FIGÉE des lignes du 27-09-2026 : il
      prouve que le chemin de comptage est juste, pas que le journal du jour est
      bien rangé — c'est l'arrêt sur comptabilité inconnue, dans `main`, qui garde
      les vraies lignes. Et l'appel de `main` hors de `mesurer_une_strategie`
      (toutes comptabilités, pour l'univers et les orphelines) n'est pas éprouvé.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    from CONTRATS_DES_FICHIERS import noms_d_une_strategie
    noms = noms_d_une_strategie(carte)
    return [o for o in operations if (o.get('strategie') or '').strip() in noms
            and (comptabilite is None or o.get('comptabilite') == comptabilite)]


def mesurer_une_strategie(operations, carte):
    """Rend les statistiques d'une strategie dans chacune des deux comptabilites.

    ① RÔLE — LE SEUL CHEMIN par lequel `main` compte les trades d'une stratégie :
      le même que rejoue `calibrage` chaque soir sur le témoin.
    ② CONTEXTE D'APPEL — `main`, une fois par stratégie vivante ; `calibrage`,
      une fois par fiche du témoin.
    ③ ENTRÉE — `operations` : des lignes du journal · `carte` : une ligne du
      registre des stratégies, avec `id` et `nom`.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : une liste de DEUX triplets (libellé écrit dans
      l'historique, nom de la comptabilité, statistiques rendues par `stats`),
      un jeton d'abord.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque comptabilité : garder ses seules lignes par
      `operations_de`, puis les compter par `stats` sur sa colonne de résultat —
      le résultat réel en un jeton, le résultat de convention en jetons
      illimités (A-330, encore à faire, changera ce choix).
    ⑦ UNITÉ — EUROS ; des NOMBRES DE TRADES.
    ⑧ POURQUOI — Relecteur du Chat, 27-09-2026 : tant que `main` gardait sa
      propre ligne de comptage, le sabotage de Cowork (`s = stats(ops, cle)`)
      passait le calibrage, qui n'éprouvait que `operations_de`. Main et
      calibrage empruntent désormais le même chemin.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    from CONTRATS_DES_FICHIERS import UN_JETON, JETONS_ILLIMITES
    return [(libelle, compta, stats(operations_de(operations, carte, compta), cle))
            for libelle, cle, compta in (('un jeton', 'pnl_net_eur', UN_JETON),
                                         ('jetons illimites', 'pnl_net_convention_eur', JETONS_ILLIMITES))]


# LE TEMOIN DES COMPTABILITES : les cinq VRAIES lignes du journal au 27-09-2026
# (strategie, valeur, comptabilite, resultat reel, resultat de convention), et les
# deux vraies fiches du registre (id, nom), plus deux lignes FABRIQUEES pour les
# pieges connus (sept en tout). Rejoue chaque soir par `calibrage`, par le meme
# chemin que `main` : `mesurer_une_strategie`.
_TEMOIN_JOURNAL = [
    ("COURS_BAS_ARGENT_REVIENT_10", "BUREAU_VERITAS", "jetons_illimites", "6884.75", "3694.00"),
    ("COURS_BAS_ARGENT_REVIENT_6", "UNIBAIL_RODAMCO", "un_jeton", "-2796.25", "-2796.25"),
    ("COURS_BAS_ARGENT_REVIENT_6", "UNIBAIL_RODAMCO", "jetons_illimites", "-2796.25", "-2796.25"),
    ("COURS_BAS_ARGENT_REVIENT_10", "UNIBAIL_RODAMCO", "un_jeton", "-2796.25", "-2796.25"),
    ("COURS_BAS_ARGENT_REVIENT_10", "UNIBAIL_RODAMCO", "jetons_illimites", "-2796.25", "-2796.25"),
    # l'ancienne ecriture de Bureau Veritas : elle ne doit aller a AUCUNE des deux
    ("C5-ETENDU-10", "BUREAU_VERITAS", "jetons_illimites", "6884.75", "3694.00"),
    # un nom court contenu dans un nom long : il ne doit pas etre avale
    ("COURS_BAS_ARGENT_REVIENT_1", "VEOLIA", "un_jeton", "1000.00", "1000.00"),
]
_TEMOIN_FICHES = {
    "C5E10-QA-V1": "COURS_BAS_ARGENT_REVIENT_6 (C5-ETENDU-10 production 6 valeurs)",
    "C5E10-OBS-V1": "COURS_BAS_ARGENT_REVIENT_10 (C5-ETENDU-10 observation 10 valeurs)",
}
# attendu : (strategie, comptabilite) -> (nombre, cumul)
_TEMOIN_ATTENDU = {
    ("C5E10-QA-V1", "un_jeton"): (1, -2796.25),
    ("C5E10-QA-V1", "jetons_illimites"): (1, -2796.25),
    ("C5E10-OBS-V1", "un_jeton"): (1, -2796.25),
    ("C5E10-OBS-V1", "jetons_illimites"): (2, 897.75),
}


def calibrage(operations):
    """REPRODUIRE AVANT DE PRODUIRE. Le service doit retrouver des chiffres deja
    connus et verifies. S'il echoue : ARRET TOTAL, rien n'est ecrit.
    Reference : premiere operation reelle du systeme, Bureau Veritas, +6 884,75 EUR
    (sortie TP_GAP le 29/07/2026), et sa convention backtest +3 694,00 EUR.

    ① RÔLE — Refuser de produire des mesures tant que le programme n'a pas
      retrouvé des chiffres déjà connus et vérifiés. Sans ce garde-fou, un
      journal corrompu, tronqué ou remplacé par un autre fichier produirait des
      mesures d'apparence normale, qui seraient empilées dans l'historique et
      relues ensuite par le tableau de bord comme si de rien n'était.
    ② CONTEXTE D'APPEL — Un seul appel, dans `main`, juste après la lecture du
      journal et AVANT tout le reste. Son résultat décide si le programme
      continue ou s'arrête.
    ③ ENTRÉE — `operations` : toutes les opérations terminées lues au journal.
    ④ CONDITIONS D'ENTRÉE — Le journal doit porter au moins une opération dont le
      nom de valeur contient `BUREAU`, avec les colonnes `pnl_net_eur`,
      `pnl_net_convention_eur` et `prix_entree` renseignées.
    ⑤ SORTIE — DEUX valeurs : un vrai ou faux qui dit si tout a été retrouvé, puis
      la liste des textes de contrôle à afficher. En cas d'échec, la liste
      s'arrête au premier contrôle manqué. Mesuré le 19-09-2026 sur le vrai
      journal : vrai, et quatre lignes de contrôle toutes marquées OK.
      [rend: 2]
    ⑥ TRAITEMENT — ① retenir les opérations dont le nom de valeur contient
      `BUREAU` · ② abandonner immédiatement s'il n'y en a aucune · ③ sur la
      PREMIÈRE, comparer trois chiffres à leur valeur attendue, au centime près :
      le résultat réel, le résultat de convention et le prix d'entrée ·
      ④ s'arrêter au premier écart · ⑤ vérifier que le cumul calculé par
      `stats` est bien la somme des résultats du journal · ⑥ depuis le 27-09-2026,
      rejouer `mesurer_une_strategie`, le chemin même de `main`, sur le témoin
      (`_TEMOIN_JOURNAL` : cinq vraies lignes, deux fabriquées) :
      chaque stratégie et chaque comptabilité doit retrouver son nombre de trades
      et son cumul, et s'arrêter au premier écart (défaut 3 de A-491).
    ⑦ UNITÉ — Les résultats et le prix d'entrée en EUROS · la tolérance est d'un
      CENTIME.
    ⑧ POURQUOI — Reproduire avant de produire. Le calcul d'un cumul est
      exactement le genre d'opération qui ne tombe jamais en panne : elle rend
      toujours un nombre, juste ou faux. Le seul moyen de savoir si elle est
      juste est de lui demander un résultat qu'on connaît déjà. La référence
      choisie est la première opération du système, Bureau Veritas, entrée le
      27-07-2026 à 27,28 € et sortie le 29-07-2026 par un saut d'ouverture
      au-dessus de l'objectif.
      Le dernier contrôle est d'une autre nature : il ne compare pas à une valeur
      écrite d'avance, il refait la même somme par un autre chemin et compare les
      deux. Un garde-fou porte sur une propriété — deux façons de compter les
      mêmes lignes doivent donner le même nombre — et jamais sur un nombre écrit
      en dur (R-721).
    ⑨ CE QUI CLOCHE —
      ① LA VALEUR ATTENDUE EST UN CHIFFRE QUE LE SYSTÈME NE SAIT PLUS PRODUIRE.
      Le résultat réel attendu, 6 884,75 €, a été calculé avec un forfait de frais
      de 300 €. Au tarif officiel du projet, 0,15 % par ordre sur la valeur
      échangée, la même opération donne 6 873,97 € — mesuré le 19-09-2026 en
      appelant le calcul de `programmes/MODULE_POSITIONS.py` sur les mêmes prix.
      L'écart de 10,78 € est figé dans le journal, qui ne se réécrit jamais, et ce
      contrôle le fige à son tour : il vérifie que le journal n'a pas bougé, pas
      que le calcul est juste.
      ② Seule la PREMIÈRE opération Bureau Veritas est contrôlée. Le jour où une
      seconde opération sur cette valeur sera écrite au journal avant la
      première, les trois comparaisons porteront sur elle et échoueront, arrêtant
      le programme pour une raison qui n'a rien à voir avec une régression.
      ③ La valeur de référence est reconnue par le fragment de texte `BUREAU`
      dans le nom. Le critère qui tranche tient en une question : si je renomme
      un fichier ou une valeur, mon contrôle change-t-il d'avis ? Ici oui, donc
      il épelle. Une entreprise dont le nom contiendrait aussi `BUREAU` serait
      prise pour la référence.
      ④ Les trois chiffres attendus sont écrits ici, et deux d'entre eux le sont
      une SECONDE fois plus bas dans `main`, dans le texte
      `'Bureau Veritas +6884.75 / +3694.00 : OK'` recopié à chaque ligne écrite.
      Un chiffre qui existe ailleurs ne se recopie pas (R-708) : modifier la
      référence ici ferait écrire dans l'historique une phrase qui annonce
      l'ancienne.
      ⑤ Le dernier contrôle compare `stats` à une somme calculée juste à côté,
      avec la même fonction de conversion et le même défaut de zéro. Les deux
      chemins ne peuvent pas diverger sur les cas que ce défaut recouvre : une
      colonne vide vaut zéro des deux côtés.
      ⑥ L'échec ne dit pas ce qu'il faut faire. Le message affiché par l'appelant
      annonce l'arrêt total sans distinguer une régression de calcul d'un journal
      simplement remplacé ou vidé.
    ⑩ EFFET — Aucun. Elle ne lit ni n'écrit aucun fichier, ne modifie pas les
      opérations reçues, ne touche pas au réseau, n'affiche rien : elle rend des
      textes que son appelant affiche.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas dans les cas
      rencontrés. Aucun de ses appels ne se termine : `nombre` et `stats` rendent
      toutes deux la main.
      [sort: non]
    ⑫ DÉFINITIONS
      la convention : le prix de sortie théorique, celui de l'objectif ou du
        stop, par opposition au prix réellement observé. C'est ce qui permet de
        comparer une opération vécue à un test sur le passé
      un saut d'ouverture : une séance qui s'ouvre directement au-delà de
        l'objectif ou du stop, si bien que la position sort au prix d'ouverture
        et non au seuil prévu
      le journal des opérations : le fichier où s'écrit chaque opération simulée refermée, avec son prix d'entrée, son prix de sortie et son résultat
      un garde-fou : une limite qui, franchie, fait cesser a la strategie de prendre position tout en continuant a la mesurer.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    controles = []
    bv = [o for o in operations if 'BUREAU' in (o.get('valeur') or '').upper()]
    if not bv:
        return False, ["aucune operation Bureau Veritas dans le journal : reference introuvable"]
    o = bv[0]
    for cle, attendu, lib in (('pnl_net_eur', 6884.75, 'resultat reel'),
                              ('pnl_net_convention_eur', 3694.00, 'convention backtest'),
                              ('prix_entree', 27.28, "prix d'entree")):
        v = nombre(o.get(cle))
        ok = v is not None and abs(v - attendu) < 0.01
        controles.append(f"{lib} : {v} attendu {attendu} -> {'OK' if ok else 'ECHEC'}")
        if not ok:
            return False, controles
    # controle de coherence interne : le cumul doit egaler la somme des operations
    s = stats(operations, 'pnl_net_eur')
    somme = sum(nombre(x.get('pnl_net_eur'), 0.0) for x in operations)
    ok = abs(s['cumul'] - somme) < 0.01
    controles.append(f"cumul recalcule : {s['cumul']:.2f} vs somme {somme:.2f} -> {'OK' if ok else 'ECHEC'}")
    if not ok:
        return False, controles
    # CHAQUE LIGNE DANS SA STRATEGIE ET SA COMPTABILITE, ET NULLE PART AILLEURS
    # (defaut 3 de A-491). Rejoue sur le temoin des vraies lignes, chaque soir.
    tem = [dict(zip(('strategie', 'valeur', 'comptabilite', 'pnl_net_eur', 'pnl_net_convention_eur'), x))
           for x in _TEMOIN_JOURNAL]
    vus = {}
    for sid, nom in _TEMOIN_FICHES.items():
        for _lib, compta, st in mesurer_une_strategie(tem, {'id': sid, 'nom': nom}):
            vus[(sid, compta)] = st
    if set(vus) != set(_TEMOIN_ATTENDU):
        controles.append(f"temoin : comptabilites rendues {sorted(vus)} -> ECHEC")
        return False, controles
    for (sid, compta), (n_att, cumul_att) in _TEMOIN_ATTENDU.items():
        st = vus[(sid, compta)]
        ok = st['n'] == n_att and abs(st['cumul'] - cumul_att) < 0.01
        controles.append(f"temoin {sid} {compta} : {st['n']} operation(s), {st['cumul']:.2f} "
                         f"attendu {n_att}, {cumul_att:.2f} -> {'OK' if ok else 'ECHEC'}")
        if not ok:
            return False, controles
    return True, controles

# ---------------------------------------------------------------- production
def ligne(date_mesure, strat_id, comptabilite, etat, s, carte, golden, temoin_p,
          temoin_m, gs, source_cal):
    """Compose la ligne de mesure d'UNE strategie dans UNE comptabilite, prete a ecrire.

    ① RÔLE — Transformer les chiffres bruts d'une comptabilité en une ligne
      d'historique complète, mise en forme et prête à écrire : les vingt-sept
      colonnes, arrondies, avec leurs verdicts et leurs voyants. C'est le dernier
      endroit où un chiffre devient du texte ; tout ce qui vient après ne fait que
      l'écrire ou l'afficher.
    ② CONTEXTE D'APPEL — Un seul appel, dans `main`, DEUX FOIS par stratégie
      vivante, une fois par comptabilité, donc quatre fois par passage avec les
      deux stratégies vivantes au 19-09-2026.
    ③ ENTRÉE — `date_mesure` : le jour du passage, en année-mois-jour, heure de
      Paris · `strat_id` : l'identifiant de la stratégie au registre, par exemple
      `'C5E10-QA-V1'` · `comptabilite` : `'un jeton'` ou `'jetons illimites'` ·
      `etat` : l'état de vie lu au registre, `'QA'` ou `'PRODUCTION'` · `s` : le
      dictionnaire de chiffres rendu par `stats` · `carte` : la ligne du registre
      décrivant la stratégie, ou `None` · `golden` : les chiffres de référence
      figés de cette stratégie et de cette comptabilité, ou `None` · `temoin_p` :
      le témoin permanent, déjà mis en forme · `temoin_m` : le témoin miroir ·
      `gs` : le rapport gain sur secousses, ou `None` · `source_cal` : le texte
      qui rappelle sur quoi le calibrage a porté.
    ④ CONDITIONS D'ENTRÉE — Le dictionnaire `s` doit porter les dix clés que
      `stats` produit : une clé manquante fait tomber la fonction. Les deux
      témoins doivent déjà être du texte.
    ⑤ SORTIE — UNE valeur : un dictionnaire de VINGT-SEPT clés, exactement les
      colonnes de l'historique des mesures, toutes renseignées, les valeurs
      absentes étant du texte vide.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire au registre l'objectif de gain, la perte acceptée et le
      seuil de validation · ② calculer le point mort en déléguant au propriétaire
      du calcul · ③ calculer la borne basse du taux de réussite · ④ poser le
      verdict : vert si la borne basse dépasse le point mort, rouge sinon, et
      « echantillon insuffisant » si l'un des deux manque · ⑤ comparer le cumul
      au résultat promis par les chiffres figés, quand ils existent · ⑥ arrondir
      chaque chiffre et composer les vingt-sept colonnes · ⑦ allumer les deux
      autres voyants, sur les pertes consécutives et sur la pire chute.
    ⑦ UNITÉ — Les cumuls, l'espérance et la chute en euros sont en EUROS, à deux
      décimales · le taux, la borne basse, le point mort et la chute en pourcents
      sont en POURCENTS, à une ou deux décimales · le compteur et le seuil sont
      des NOMBRES D'OPÉRATIONS TERMINÉES · TOUTES LES VALEURS SONT RENDUES SOUS
      FORME DE TEXTE, sans leur unité : c'est le nom de la colonne qui la porte.
    ⑧ POURQUOI — Le verdict compare la borne basse au point mort, et non le taux
      brut à un seuil fixe, décidé le 15-08-2026. Un taux brut de 60 % sur cinq
      opérations ne prouve rien, et un seuil unique n'a pas de sens : 55 % de
      réussite est excellent avec un objectif de +5 % et une perte acceptée de
      −2 %, ruineux avec +1,2 % et −1 %. Comparer le pire taux encore compatible
      avec ce qu'on a vu au taux minimal qui couvre les frais répond à la seule
      question qui compte : cette stratégie gagne-t-elle de l'argent, ou pas.
      Le texte vide plutôt qu'un zéro quand une valeur manque, parce qu'un zéro
      dans une colonne de pourcentage se lit comme un taux nul.
    ⑨ CE QUI CLOCHE —
      ① Le nombre d'opérations est écrit DEUX FOIS, dans la colonne
      `n_operations` et dans la colonne `compteur`, avec la même valeur. Mesuré
      le 19-09-2026 : les quatre lignes écrites portent `3` dans les deux
      colonnes. Un chiffre qui existe ailleurs ne se recopie pas (R-708) : rien
      ne garantit que les deux resteront d'accord.
      ② Les deux seuils qui allument les voyants sont écrits en dur ici : cinq
      pertes consécutives et une chute de 20 %. Ils ne sont ni au registre des
      stratégies, ni dans les règles du projet, et ils valent pour toutes les
      stratégies alors que l'objectif de gain et la perte acceptée, eux, sont par
      stratégie.
      ③ La comparaison au résultat promis est silencieusement abandonnée quand le
      chiffre promis vaut zéro, parce que la condition ne distingue pas zéro
      d'absent : la colonne porte alors « non calculable » sans autre explication.
      Mesuré le 19-09-2026 : les quatre lignes portent « non calculable », mais
      pour une autre raison — les chiffres figés ne sont jamais chargés par
      `main`, qui les cherche à plat alors qu'ils vivent dans `gouvernance/`.
      ④ Le seuil de validation est ramené à un entier, et un seuil valant zéro
      devient du texte vide au lieu de zéro : la condition ne distingue pas zéro
      d'absent. La valeur de repli est 50, écrite en dur, alors que le registre
      porte déjà ce chiffre par stratégie.
      ⑤ Le dernier paramètre, `source_cal`, est un texte recopié par l'appelant
      sur chaque ligne, qui répète deux montants appartenant au calibrage. Il
      annonce « OK » sans que rien ici ne l'ait vérifié : c'est l'appelant qui
      garantit qu'on n'arrive ici qu'après un calibrage réussi.
      ⑥ Trois des paramètres reçus — les deux témoins et le rapport gain sur
      secousses — sont les mêmes pour toutes les lignes d'un passage. Les écrire
      colonne par colonne laisse croire qu'ils sont propres à chaque stratégie.
    ⑩ EFFET — Aucun fichier écrit, aucun accès réseau, aucun affichage. Elle LIT
      l'arborescence du dossier du programme et EXÉCUTE deux fichiers voisins, par
      l'intermédiaire du calcul du point mort.
    ⑪ TERMINAISON — Rend la main. PEUT LEVER : si une clé manque au dictionnaire
      de chiffres, et si le point mort calculé sort de l'intervalle de 0 à 100.
      Un de ses appels peut ne pas revenir : `point_mort_en_pourcents` lève quand
      un fichier voisin est introuvable, et quand les unités ont été croisées.
      [sort: non]
    ⑫ DÉFINITIONS
      une comptabilité : une façon de compter le résultat. Il y en a DEUX, qui
      le point mort : le taux de réussite en dessous duquel une stratégie perd de l'argent
      la borne basse : la valeur en dessous de laquelle ne tombe qu'un tirage sur vingt
      les chiffres figés : les résultats d'un test sur le passé, enregistrés une
        fois pour toutes, auxquels on compare ce que le système obtient vraiment
      un voyant : une case du tableau de bord qui vaut « vert » ou « rouge »
      le registre des stratégies : le fichier `cac40_strategies.csv`, une ligne par stratégie, qui porte leur état civil — identifiant, réglages, résultats connus
      PRODUCTION : l etat d une strategie dont le seuil d operations est atteint et les resultats conformes, donc exploitee.
      QA : l etat d une strategie validee sur l historique mais qui n a pas encore realise assez d operations reelles pour etre jugee.
      l'espérance : le résultat moyen d'une opération, en euros
      l'objectif de gain : le pourcentage de hausse à partir duquel la position se referme sur un gain
      l'état de vie : la place d'une stratégie dans son cycle. `QA` veut dire en essai, `PRODUCTION` veut dire en service
      la perte acceptée : le pourcentage de baisse à partir duquel la position se referme sur une perte
      la pire chute : la plus forte baisse du cumul depuis un sommet precedent.
      le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
      le seuil de validation : le nombre d operations qu une strategie doit realiser avant qu on juge ses resultats.
      le témoin : le fichier temoins/TEMOIN_cours_reels.csv, copie figée de vraies séances, sur laquelle les épreuves tournent toujours à l'identique.
      le témoin miroir : ce qu'aurait rapporté l'indice en n'étant exposé que les jours où une position était ouverte
      le témoin permanent : ce qu'auraient rapporté 100 000 € placés sur l'indice du début à la fin, sans rien faire
      un jeton : la comptabilité où une seule position peut être ouverte à la fois par stratégie ; un signal reçu pendant une position est ignoré.
      une clé : le texte obtenu après rapprochement, qui sert à comparer deux noms et n'est jamais affiché à un lecteur
      une comptabilite : la facon de compter les resultats, et il y en a deux, jamais additionnees — un jeton, une seule position a la fois avec 100 000 € simules, et jetons illimites, toutes les occurrences du signal mesurees.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    tp = nombre((carte or {}).get('tp'))
    sl = nombre((carte or {}).get('sl'))
    pm = point_mort_en_pourcents(tp, sl)
    bb = wilson_borne_basse(s['gagnantes'], s['n'])
    seuil = nombre((carte or {}).get('seuil_validation'), 50)
    # verdict C7 : borne basse > point mort (decision 2 du 15/08)
    if bb is None or pm is None:
        verdict, voyant_c7 = 'echantillon insuffisant', 'attente'
    elif bb > pm:
        verdict, voyant_c7 = f"{bb:.1f} % > {pm:.1f} %", 'vert'
    else:
        verdict, voyant_c7 = f"{bb:.1f} % <= {pm:.1f} %", 'rouge'
    conf = 'non calculable'
    if golden:
        att = nombre(golden.get('net'))
        if att:
            conf = f"{100*s['cumul']/att:+.1f} % du promis"
    return {
        'date_mesure': date_mesure, 'strategie': strat_id, 'comptabilite': comptabilite,
        'etat': etat, 'n_operations': s['n'], 'gagnantes': s['gagnantes'],
        'taux_reussite': f"{s['taux']:.1f}" if s['taux'] is not None else '',
        'borne_basse_wilson': f"{bb:.1f}" if bb is not None else '',
        'point_mort': f"{pm:.1f}" if pm is not None else '',
        'verdict_c7': verdict,
        'cumul_net_eur': f"{s['cumul']:.2f}",
        'esperance_eur': f"{s['esperance']:.2f}" if s['esperance'] is not None else '',
        'facteur_profit': f"{s['pf']:.2f}" if s['pf'] is not None else '',
        'serie_en_cours': f"{s['serie']:+d}",
        'pertes_consecutives': s['pertes'],
        'pire_chute_pct': f"{s['chute_pct']:.2f}",
        'pire_chute_eur': f"{s['chute_eur']:.2f}",
        'compteur': s['n'], 'seuil': int(seuil) if seuil else '',
        'conformite_promis': conf,
        'voyant_c7': voyant_c7,
        'voyant_pertes': 'rouge' if s['pertes'] >= 5 else 'vert',
        'voyant_chute': 'rouge' if s['chute_pct'] <= -20 else 'vert',
        'temoin_permanent': temoin_p, 'temoin_miroir': temoin_m,
        'rapport_gain_secousses': f"{gs:.2f}" if gs is not None else 'non calculable',
        'source_calibrage': source_cal,
    }

# ---------------------------------------------------------------- main
def main():
    """Deroule la mesure du jour de bout en bout et rend le code de sortie du programme.

    ① RÔLE — Enchaîner tout le travail du soir : lire le journal, refuser de
      continuer si les chiffres connus ne sont pas retrouvés, mesurer chaque
      stratégie vivante dans les deux comptabilités, et ajouter les lignes du
      jour à l'historique des mesures. C'est le seul point du système où ces
      chiffres naissent : le tableau de bord, le document de pilotage et la
      surveillance du soir ne font que relire le fichier écrit ici.
    ② CONTEXTE D'APPEL — Le lancement du programme, et lui seul. Sa valeur de
      retour est passée directement à la sortie du processus. Le seul lancement
      automatique est l'étape « Mesurer la performance » de
      `.github/workflows/collecte_abc.yml`, ligne 223, chaque soir après la
      collecte des cours et la tenue des positions.
    ③ ENTRÉE — La ligne de commande, deux arguments facultatifs. Le premier est
      le dossier où chercher les fichiers à lire, le dossier courant par défaut.
      Le second est le dossier où écrire l'historique, le dossier courant par
      défaut. Le circuit du soir ne passe que le premier, `"$GITHUB_WORKSPACE"`.
    ④ CONDITIONS D'ENTRÉE — Le journal des opérations doit être trouvable sous le
      dossier de sources et passer le calibrage. LE DOSSIER `donnees/` DOIT DÉJÀ
      EXISTER sous le dossier de sortie : le programme ne le crée pas.
    ⑤ SORTIE — UNE valeur : un entier. 0 quand les mesures ont été écrites, 0
      également quand aucune stratégie n'est vivante au registre, 1 quand le
      journal est introuvable, 1 quand le calibrage échoue, 1 quand une
      opération du journal ne porte pas l'une des deux comptabilités déclarées
      au contrat (depuis le 27-09-2026), 1 quand, pour une stratégie, les opérations
      écrites dans ses deux comptabilités ne font pas le nombre de ses lignes au
      journal.
      [rend: 1]
    ⑥ TRAITEMENT — ① relever la date du jour en heure de Paris · ② trouver et lire
      le journal des opérations, et s'arrêter s'il manque · ③ refaire les chiffres
      de référence, et s'arrêter s'ils ne tombent pas juste · ③bis s'arrêter si
      une opération n'a pas de comptabilité reconnue · ④ relever au
      registre les stratégies en essai ou en production, et s'arrêter s'il n'y en
      a aucune · ④bis signaler un nom qui désigne deux d'entre elles · ⑤ charger les chiffres de référence figés · ⑥ charger le
      référentiel des valeurs et dire s'il manque · ⑦ reconstituer la courbe du
      capital et calculer le rapport gain sur secousses et les deux témoins ·
      ⑧ pour chaque stratégie : retrouver ses opérations — celles dont le nom
      écrit au journal est ÉGAL à l'identifiant du registre ou au nom court avant
      la parenthèse —, signaler celles qui
      portent sur une valeur hors de son univers autorisé, signaler si aucune
      opération n'a été appariée, retrouver ses chiffres figés, et composer DEUX
      lignes, une par comptabilité, chacune sur les seules opérations de SA
      comptabilité, par `mesurer_une_strategie` · ⑧bis vérifier, sur ce qui va
      être écrit, que chaque stratégie compte autant d'opérations que de lignes
      au journal, et s'arrêter sinon · ⑧ter signaler les opérations comptées dans
      aucune stratégie vivante · ⑨ relire l'historique pour savoir ce qui y
      est déjà, et n'ajouter que les lignes nouvelles · ⑩ afficher le bilan, une
      ligne par mesure, et le chemin du fichier écrit.
    ⑦ UNITÉ — Les cumuls en EUROS · les taux et les verdicts en POURCENTS · les
      compteurs en NOMBRES D'OPÉRATIONS TERMINÉES · la date de mesure en
      année-mois-jour, heure de Paris.
    ⑧ POURQUOI — L'historique s'empile et ne s'écrase jamais, décidé par Jean-Luc
      le 15-08-2026. Une ligne par jour permet de voir une dégradation lente, que
      la photographie du jour ne montrerait pas, et de savoir ce que le système
      savait à une date donnée. L'unicité est assurée par le trio date,
      stratégie, comptabilité : relancer le programme deux fois le même jour
      n'ajoute rien, mesuré le 19-09-2026 par un second passage qui annonce
      « 0 ecrite(s), 4 deja presente(s) ».
      Le calibrage vient avant tout le reste, et son échec arrête tout sans rien
      écrire, parce qu'une mesure fausse empilée dans l'historique y reste : le
      fichier ne se réécrit pas, et le tableau de bord la relira chaque jour.
      Le fichier vit dans `donnees/` et non à la racine. Il a vécu aux deux
      endroits en même temps : 64 lignes du 15-08 au 06-09 dans `donnees/`, 16
      lignes du 12-09 au 16-09 à la racine, deux fichiers de même nom qui
      divergeaient. Le pas du circuit qui dépose les mesures n'a plus rien déposé
      à partir du 13-09, et le rituel de début de session lisait un rapport de
      dimanche sans que rien ne compare sa date au jour. Les deux fichiers ont
      été réunis le 16-09 — périodes disjointes, mêmes colonnes, aucune ligne
      perdue, 80 lignes du 15-08 au 16-09 — et il reste un trou du 07 au 11-09,
      pendant lequel la mesure n'a pas tourné. Vérifié le 19-09-2026 : il n'existe
      plus qu'un seul fichier, `donnees/historique_mesures.csv`, 85 lignes, et
      aucun fichier de ce nom à la racine du dépôt.
    ⑨ CE QUI CLOCHE —
      ① CORRIGÉ LE 27-09-2026 (défaut 3 de A-491), avec le ② : appariement
      exact, filtre par comptabilité. Mesuré sur une copie : « C5E10-OBS-V1 · un
      jeton : 1 operation(s) · cumul -2796.25 EUR », au lieu de 3 et 1292.25.
      Constat d'origine : UNE OPÉRATION EST COMPTÉE DANS DEUX STRATÉGIES À LA FOIS. Les opérations
      d'une stratégie sont retrouvées en cherchant le nom écrit au journal comme
      MORCEAU du nom du registre, et non par égalité. Mesuré le 19-09-2026 sur le
      vrai journal de cinq opérations : l'opération Bureau Veritas, écrite sous
      le nom `C5-ETENDU-10`, est attribuée à `C5E10-QA-V1` ET à `C5E10-OBS-V1`,
      parce que ce nom est contenu dans l'intitulé des deux. Les deux stratégies
      annoncent le même cumul de 1 292,25 € sur trois opérations.
      ② CORRIGÉ LE 27-09-2026 avec le ① : un nom doit être ÉGAL, plus contenu.
      Constat d'origine : un nom court est avalé par un nom long. La même recherche par morceau
      ferait attribuer une stratégie nommée `COURS_BAS_ARGENT_REVIENT_1` au
      journal à la stratégie `COURS_BAS_ARGENT_REVIENT_10` du registre : vérifié
      le 19-09-2026, le premier nom est bien contenu dans le second. Aucun
      message ne le dirait.
      ③ LE PROGRAMME TOMBE SI LE DOSSIER `donnees/` N'EXISTE PAS SOUS LE DOSSIER
      DE SORTIE. Mesuré le 19-09-2026 en le lançant depuis un dossier vide :
      « FileNotFoundError: [Errno 2] No such file or directory:
      './donnees/historique_mesures.csv' », levée à l'ouverture du fichier, APRÈS
      que tout le calcul a été fait et affiché. Le travail est perdu et le
      programme ne rend pas de code d'erreur : il s'arrête sur une erreur non
      rattrapée.
      ④ Les chiffres de référence figés ne sont jamais chargés. Ils sont cherchés
      à plat dans le dossier de sources alors qu'ils vivent dans
      `gouvernance/golden_tests_Sam_01-08-2026_20h19.json`. Mesuré le 19-09-2026 :
      les quatre lignes écrites portent « non calculable » dans la colonne qui
      devrait dire quelle part du résultat promis a été tenue, alors que le
      fichier existe et annonce 111 334,24 € pour la comptabilité jetons
      illimités. Aucun message ne signale l'absence, contrairement au référentiel
      qui, lui, est annoncé manquant.
      ⑤ La même recherche à plat manque le référentiel des valeurs. Mesuré le
      19-09-2026 : « ATTENTION : referentiel introuvable ». La conséquence est une
      FAUSSE ALERTE sur l'univers autorisé : Bureau Veritas, dont le code `BVI`
      figure bien dans l'univers des deux stratégies, est signalé « HORS UNIVERS
      declare » parce que son nom n'a pas pu être traduit en code. Le programme
      porte pourtant une fonction qui cherche dans toute l'arborescence, `_p`,
      dont il se sert pour le journal et pour le registre.
      ⑥ Le rapport gain sur secousses et les deux témoins sont calculés UNE fois,
      sur toutes les opérations réunies, puis recopiés sur chaque ligne. Mesuré
      le 19-09-2026 : les quatre lignes portent toutes `0.35`, y compris celles
      des deux comptabilités dont les cumuls diffèrent (+1 292,25 € contre
      −1 898,50 €).
      ⑦ Le texte du calibrage écrit dans chaque ligne, `'Bureau Veritas +6884.75
      / +3694.00 : OK'`, recopie deux montants qui vivent déjà dans `calibrage`.
      Un chiffre qui existe ailleurs ne se recopie pas (R-708) : changer la
      référence sans toucher ce texte ferait écrire dans l'historique une phrase
      qui annonce l'ancienne.
      ⑧ L'alerte « hors univers » et l'alerte « aucune opération appariée » sont
      AFFICHÉES et n'ont aucune autre conséquence : la mesure est écrite quand
      même, et le code de sortie reste 0. Un pas vert sur un contrôle qui vient
      de trouver une faute est un silence.
      ⑨ Un fichier de chiffres figés mal formé est remplacé par un dictionnaire
      vide, sans message : la comparaison au promis s'éteint alors exactement
      comme si le fichier était absent.
      ⑩ Les états de vie retenus, `QA` et `PRODUCTION`, sont épelés en dur, comme
      les deux noms de comptabilité et les deux colonnes de résultat. Une
      troisième comptabilité ou un troisième état demanderait de modifier ce
      code.
    ⑩ EFFET — AJOUTE des lignes à la fin de `donnees/historique_mesures.csv` sous
      le dossier de sortie, ou le crée avec son en-tête s'il n'existe pas. Il ne
      réécrit jamais une ligne déjà présente. Mesuré le 19-09-2026 sur une copie :
      le fichier passe de 85 à 89 lignes et son empreinte change. LIT le journal
      des opérations, le registre des stratégies, les chiffres figés, le
      référentiel, les fichiers de cours et l'historique lui-même, et parcourt
      l'arborescence du dossier de sources pour les trouver. Affiche une dizaine
      de lignes. Aucun accès réseau.
    ⑪ TERMINAISON — Rend la main avec 0 ou 1 dans le cas normal. PEUT LEVER une
      erreur non rattrapée, qui arrête alors le programme : quand le dossier de
      sortie ne porte pas de sous-dossier `donnees/`, et quand un point mort
      calculé sort de l'intervalle de 0 à 100. Et un de ses appels peut ne pas
      revenir : `ligne` lève si un fichier voisin est introuvable, `courbe_capital`
      et `temoins` lèvent si un fichier de cours trouvé ne porte pas de colonne
      `date`.
      [sort: non]
    ⑫ DÉFINITIONS
      une comptabilité : une façon de compter le résultat. Il y en a DEUX, qui
        Mesuré le 19-09-2026 sur une même stratégie : +1 292,25 € d'un côté,
        −1 898,50 € de l'autre
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
      le registre des stratégies : le fichier `cac40_strategies.csv`, une ligne par stratégie, qui porte leur état civil — identifiant, réglages, résultats connus
      l'univers autorisé : la liste des valeurs qu'une stratégie a le droit de jouer, écrite dans le registre des stratégies
      les chiffres figés : les résultats d'un test sur le passé, enregistrés une
        fois pour toutes, auxquels on compare ce que le système obtient vraiment
      l'état de vie : la place d'une stratégie dans son cycle. `QA` veut dire en
        essai, `PRODUCTION` veut dire en service
      C5-ETENDU-10 : le nom de la stratégie vivante ; ses seuils et son horizon sont lus dans `donnees/cac40_strategies.csv`.
      hors univers : une valeur que Jean-Luc a volontairement retiree du champ, avec son motif ecrit dans la colonne `hors_univers` du referentiel
      la photographie du jour : l'état de la performance mesuré un seul jour ; seul l'historique des mesures dit comment il a évolué.
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
      le journal des opérations : le fichier où s'écrit chaque opération simulée refermée, avec son prix d'entrée, son prix de sortie et son résultat
      le rituel de début de session : les gestes imposés à l'ouverture d'une conversation — relever la date, cloner le dépôt, lire le PILOTE, lire le rapport du radar
      le référentiel : donnees/REFERENTIEL_VALEURS_*.csv, la liste des valeurs à suivre, avec pour chacune son mnémonique et sa place de cotation.
      le référentiel des valeurs : donnees/REFERENTIEL_VALEURS_*.csv, la liste des valeurs à suivre, avec pour chacune son mnémonique et sa place de cotation.
      une opération : un achat simulé suivi de sa revente, avec son gain net en euros ; aucun ordre réel n'est jamais passé
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    base = sys.argv[1] if len(sys.argv) > 1 else '.'
    sortie = sys.argv[2] if len(sys.argv) > 2 else '.'
    now = datetime.now(PARIS)
    jour = now.strftime('%Y-%m-%d')

    ch = _p(base, 'journal_trades.csv')
    if not ch:
        print("ARRET : journal des operations introuvable — rien n'est ecrit.")
        return 1
    operations = lire_csv(ch)

    ok, controles = calibrage(operations)
    print("CALIBRAGE :")
    for c in controles:
        print("   ", c)
    if not ok:
        print("ARRET TOTAL : le calibrage a echoue, aucune mesure n'est ecrite.")
        return 1
    # CHAQUE OPERATION DIT SA COMPTABILITE, OU RIEN NE S'ECRIT (defaut 3 de A-491,
    # 27-09-2026). Les deux noms se lisent au contrat, jamais recopies (R-708).
    # Avant, le journal n'avait pas cette colonne : la vente d'Unibail du 27-08,
    # ecrite une fois par comptabilite, etait comptee dans les deux — « un jeton :
    # 3 operation(s) · cumul 1292.25 EUR » pour un seul trade a -2 796,25 EUR.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from CONTRATS_DES_FICHIERS import COMPTABILITES, UN_JETON, JETONS_ILLIMITES, noms_d_une_strategie
    sans = [o for o in operations if (o.get('comptabilite') or '') not in COMPTABILITES]
    if sans:
        print(f"ARRET : {len(sans)} operation(s) sans comptabilite reconnue — aucune mesure n'est ecrite.")
        for o in sans:
            print(f"   {o.get('strategie')} · {o.get('valeur')} · {o.get('date_sortie')} : "
                  f"comptabilite {o.get('comptabilite')!r} ; admises : {', '.join(COMPTABILITES)}")
        return 1

    # carte d'identite de chaque strategie vivante (registre = etat civil)
    cartes, etats = {}, {}
    ch = _p(base, 'cac40_strategies.csv')
    if ch:
        for r in lire_csv(ch):
            ev = (r.get('etat_vie') or '').strip().upper()
            if ev in ('QA', 'PRODUCTION'):
                nom = (r.get('id') or '').strip()
                cartes[nom] = r
                etats[nom] = ev
    if not cartes:
        print("Aucune strategie en QA ou en PRODUCTION au registre : rien a mesurer.")
        return 0
    # UN NOM QUI DESIGNE DEUX STRATEGIES VIVANTES FERAIT COMPTER LES MEMES TRADES DANS
    # LES DEUX : on le dit (relecteur du Chat, 27-09-2026 ; le registre porte 28 noms
    # courts non uniques, sans effet sur les strategies vivantes ce jour-la).
    _vus = {}
    for _sid, _carte in cartes.items():
        for _n in noms_d_une_strategie(_carte):
            _vus.setdefault(_n, []).append(_sid)
    for _n, _ids in sorted(_vus.items()):
        if len(_ids) > 1:
            print(f"   ALERTE : le nom {_n!r} designe {len(_ids)} strategies vivantes ({', '.join(_ids)}) : "
                  "leurs trades ecrits sous ce nom sont comptes dans chacune.")

    # chiffres de reference figes
    golden = {}
    g = sorted([f for f in os.listdir(base) if f.startswith('golden_tests') and f.endswith('.json')])
    if g:
        try:
            golden = json.load(open(os.path.join(base, g[-1]), encoding='utf-8'))
        except json.JSONDecodeError:
            golden = {}

    corr = charger_referentiel(base)
    if corr:
        print(f"referentiel : {len(set(corr.values()))} valeurs connues (noms et codes relies)")
    else:
        print("ATTENTION : referentiel introuvable — le controle d'univers ne peut pas fonctionner")

    seances, courbe = courbe_capital(operations, base, None)
    gs = rapport_gain_secousses(courbe)
    tp_, tm_ = temoins(base, seances, courbe, operations)

    lignes = []
    apparies = set()
    _lignes_au_journal = {}
    for sid, carte in cartes.items():
        # les operations de cette strategie. On ALERTE si aucune operation n'est
        # appariee — jamais de zero silencieux. `cle_carte` ne sert plus qu'aux
        # chiffres figes, cherches plus bas.
        cle_carte = _norm(sid + ' ' + (carte.get('nom') or ''))
        # APPARIEMENT EXACT depuis le 27-09-2026 (defaut 3 de A-491) : le nom ecrit au
        # journal doit ETRE l'identifiant du registre (ce qu'ecrit le teneur de
        # positions depuis le 12-09) ou le nom court, avant la parenthese (ce que
        # portent les lignes d'avant). La recherche par morceau attribuait Bureau
        # Veritas, ecrit `C5-ETENDU-10`, aux DEUX strategies.
        ops = operations_de(operations, carte)         # toutes comptabilites
        apparies.update(id(o) for o in ops)

        # --- UNIVERS DECLARE : les valeurs que la strategie a le droit de jouer
        # (colonne ajoutee au registre le 17-08-2026, action A-238).
        # Le controle ci-dessous applique la regle I-8 du chapitre GESTION DE
        # L'IDENTITE DES VALEURS : une strategie ne joue QUE son univers declare.
        # Sans lui, une operation sur une valeur hors univers passerait en silence
        # — c'est ce qui s'est produit avec Eiffage et Bureau Veritas, jouees
        # avant leur entree dans l'indice (11 operations sur 100, 24,9 % du resultat).
        univers = [x.strip().upper() for x in (carte.get('univers') or '').split(',') if x.strip()]
        if univers:
            hors = []
            for op in ops:
                brut = (op.get('mnemonique') or op.get('valeur') or '').strip()
                mn = corr.get(_norm(brut))          # traduction par le referentiel
                if mn is None:
                    hors.append(f"{brut} (inconnue du referentiel)")
                elif mn not in univers:
                    hors.append(f"{brut} [{mn}]")
            hors = sorted(set(hors))
            if hors:
                print(f"   ALERTE : {sid} — operation(s) sur une valeur HORS UNIVERS declare : {hors}")
                print(f"            univers declare : {', '.join(univers)}")
        else:
            print(f"   ATTENTION : {sid} n'a pas d'univers declare au registre — controle impossible (regle I-8)")
        if not ops and operations:
            print(f"   ALERTE : aucune operation appariee pour {sid}. Noms au journal : "
                  f"{sorted({o.get('strategie') for o in operations})} — verifier la correspondance.")
        ref = None
        for k, v in golden.items():
            if k != 'meta' and _norm(k) in cle_carte:
                ref = v
                break
        # UNE OPERATION NE COMPTE QUE DANS SA COMPTABILITE (defaut 3 de A-491), et
        # par le SEUL chemin que le calibrage eprouve chaque soir.
        _lignes_au_journal[sid] = len(ops)
        for comptabilite, gref, s in mesurer_une_strategie(operations, carte):
            lignes.append(ligne(jour, sid, comptabilite, etats[sid], s, carte,
                                (ref or {}).get(gref), tp_, tm_, gs,
                                'Bureau Veritas +6884.75 / +3694.00 : OK'))

    # LA PROPRIETE SE VERIFIE SUR CE QUI VA ETRE ECRIT, CHAQUE SOIR, SUR LE VRAI JOURNAL :
    # chaque ligne d'une strategie compte dans UNE comptabilite, donc les operations
    # ecrites pour ses deux comptabilites font exactement le nombre de ses lignes. Une
    # ligne comptee deux fois (le defaut 3, que Cowork a remis le 27-09 a 22h46 sans
    # que rien ne rougisse) ou nulle part arrete tout, quel que soit l'endroit du code
    # qui l'a produite (relecteur du Chat, tour 7).
    for _sid, _n_lignes in _lignes_au_journal.items():
        _n_ecrit = sum(int(l['n_operations']) for l in lignes if l['strategie'] == _sid)
        if _n_ecrit != _n_lignes:
            print(f"ARRET : {_sid} — {_n_ecrit} operation(s) comptee(s) dans ses deux comptabilites "
                  f"pour {_n_lignes} ligne(s) au journal : une ligne compte deux fois ou nulle part. "
                  "Aucune mesure n'est ecrite.")
            return 1
    orphelines = [o for o in operations if id(o) not in apparies]
    if orphelines:
        print(f"   ALERTE : {len(orphelines)} operation(s) du journal ne sont comptees dans AUCUNE "
              f"strategie vivante : " + ", ".join(sorted({f"{o.get('strategie')} ({o.get('valeur')})"
                                                           for o in orphelines})))
    # ECRITURE : on EMPILE, on n'ecrase JAMAIS (decision JL du 15/08)
    dest = os.path.join(sortie, FICHIER_MESURES)
    existe = os.path.exists(dest)
    deja = set()
    if existe:
        for r in lire_csv(dest):
            deja.add((r.get('date_mesure'), r.get('strategie'), r.get('comptabilite')))
    neuves = [l for l in lignes if (l['date_mesure'], l['strategie'], l['comptabilite']) not in deja]
    with open(dest, 'a' if existe else 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLONNES)
        if not existe:
            w.writeheader()
        for l in neuves:
            w.writerow(l)

    print(f"MESURES : {len(cartes)} strategie(s) vivante(s) · {len(lignes)} ligne(s) du jour · "
          f"{len(neuves)} ecrite(s), {len(lignes)-len(neuves)} deja presente(s)")
    for l in lignes:
        print(f"   {l['strategie']} · {l['comptabilite']} : {l['n_operations']} operation(s) · "
              f"cumul {l['cumul_net_eur']} EUR · C7 {l['verdict_c7']} · compteur {l['compteur']}/{l['seuil']}")
    print(f"ECRIT   : {dest} (empile, jamais ecrase)")
    return 0

if __name__ == '__main__':
    sys.exit(main())
