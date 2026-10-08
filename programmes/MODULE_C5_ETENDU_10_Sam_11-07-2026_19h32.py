# -*- coding: utf-8 -*-
# ══════════════════════════════════════════════════════════════
# MODULE C5-ETENDU-10 — RECONSTRUCTION v1.0
# Jour 11-07-2026 19h27 (Paris)
#
# BLOC DE REMPLACEMENT COMPLET à insérer dans le monolithe
# (après calculer_signal_c5ei). Reconstruit d'après les specs
# actées (PASSATION §3) : le code original (extension_moteur.py)
# est perdu — ce module devient LA référence reproductible.
#
# RÈGLE : CMF(14) croise 0↑  ET  CCI(14) < -50
# UNIVERS (10) : TOTALENERGIES ENGIE VEOLIA BOUYGUES EIFFAGE
#                AIRBUS RENAULT UNIBAIL_RODAMCO BUREAU_VERITAS VINCI
# ENTRÉE  : Open J+1 après signal en clôture J
# SORTIE  : TP +4.0% · SL -2.5% · Horizon 20 séances (close)
# CONVENTION PESSIMISTE : TP et SL touchés le même jour → SL compté
# FRAIS   : 0.15% par ordre (150€ sur 100 000€) → 300€ aller-retour
# SÉLECTION multi-signaux même jour : CCI le plus bas
#   (choix logique NON validé empiriquement — réévaluer à 30 trades)
# ══════════════════════════════════════════════════════════════

"""Calcule les signaux d'achat de la stratégie C5-ETENDU-10 et rejoue son backtest.

① RÔLE — C'est le SEUL endroit du dépôt où sont écrites les deux formules qui
  décident un achat sur cette stratégie : le CMF, qui dit si l'argent entre ou
  sort d'une valeur, et le CCI, qui dit de combien le cours s'est écarté de sa
  moyenne récente. Chaque soir de semaine, le programme qui détecte les signaux
  charge ce fichier et lui demande, valeur par valeur, si le signal est actif à
  la clôture du jour ; ce que ce module répond devient la proposition d'achat du
  lendemain à l'ouverture. Il porte en plus le backtest qui a produit les
  chiffres de référence de la stratégie. Il ne lit aucun fichier de données,
  n'en écrit aucun, et ne choisit pas quelle valeur acheter : il constate.
② CONTEXTE D'APPEL — Trois appelants, tous par chargement du fichier depuis son
  chemin, jamais par un `import` ordinaire, parce que son nom porte une date.
  ① programmes/DETECTER_LES_SIGNAUX_GITHUB.py, pas n°5 du circuit du soir, lancé
    par .github/workflows/collecte_abc.yml à l'horaire `0 18 * * 1-5`, soit du
    lundi au vendredi à 18 h UTC. Il charge ce fichier par un chemin écrit en
    entier, `programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py`, et appelle
    `signaux_c5etendu10`, `_c5e10_cmf` et `_c5e10_cci`.
  ② programmes/audit_ecosysteme.py : son maillon 10 recalcule chaque trade déjà
    clôturé en appelant `_c5e10_sortie`, et son maillon 11 compare le prix
    d'objectif et le prix de stop des positions ouvertes à `C5E10_TP` et
    `C5E10_SL`.
  ③ programmes/JUGE_DES_STRATEGIES.py, qui lit `C5E10_UNIVERS` et appelle
    `signaux_c5etendu10` pour son calibrage. Le fichier gouvernance/SOCLE.csv le
    range ligne 135 en VIVANT, avec le motif « appele par JUGE_DES_STRATEGIES.py ». Lancé
    directement en ligne de commande, il ne fait que son jeu d'épreuves.
③ ENTRÉE — Aucune ligne de commande, aucun fichier de données. Ce sont ses
  fonctions qui reçoivent des listes de séances. Une seule dépendance au
  chargement : le fichier `MODULE_POSITIONS.py` doit se trouver dans le MÊME
  dossier que lui, parce que le taux de frais y est lu au lieu d'être recopié.
④ CONDITIONS D'ENTRÉE — `MODULE_POSITIONS.py` présent à côté. Mesuré le
  19-09-2026 : copié seul dans un dossier vide, ce fichier refuse de se charger
  sur « ImportError: MODULE_POSITIONS introuvable : on ne recopie PAS son taux
  de frais ». Les séances qu'on lui passe doivent être triées par date
  croissante, sans doublon, et porter les six clés `date`, `open`, `high`,
  `low`, `close` et `volume`.
⑤ SORTIE — Lancé seul : un code de sortie, 0 quand la suite des épreuves passe.
  Employé comme module : six constantes et neuf fonctions, dont trois publiques
  — `signaux_c5etendu10`, `backtest_c5etendu10` — et le reste préfixé d'un blanc
  souligné, marque d'usage interne que trois programmes du dépôt ignorent.
⑥ TRAITEMENT — ① au chargement, aller lire le taux de frais chez son
  propriétaire, `MODULE_POSITIONS.FRAIS_TAUX` · ② poser les constantes de la
  stratégie et définir les fonctions · ③ rien d'autre ne s'exécute, sauf la
  suite des épreuves lorsque le fichier est lancé directement.
⑦ UNITÉ — `C5E10_TP` et `C5E10_SL` sont des FRACTIONS, jamais des pourcents :
  0,040 vaut +4,0 % et 0,025 vaut −2,5 %. Les confondre donne un résultat cent
  fois trop grand, et plausible. `C5E10_HORIZON` se compte en SÉANCES DE BOURSE,
  jamais en jours de calendrier : 20 séances font environ quatre semaines.
  `C5E10_CAPITAL`, les prix et tous les résultats sont en EUROS.
  `C5E10_CCI_SEUIL` est un niveau d'indice sans unité. Le CMF est un rapport
  sans unité borné à ±1 ; le CCI est un indice sans unité qui vaut couramment
  entre −200 et +200.
⑧ POURQUOI — Ce fichier existe parce que le code d'origine a été PERDU. La
  stratégie avait été validée en mai 2026 sur un programme nommé
  `extension_moteur.py` qui ne se trouve plus nulle part ; ses résultats
  n'étaient donc plus reproductibles, et deux résultats nets contradictoires
  circulaient sans qu'aucun ne puisse être refait. Ce module a été réécrit le
  11-07-2026 d'après les paramètres consignés, pour redevenir la référence que
  l'on peut rejouer. Le taux de frais, lui, est LU chez son propriétaire au lieu
  d'être recopié, parce qu'un chiffre qui existe ailleurs ne se recopie pas —
  deux implémentations d'une même chose divergent toujours (R-708). La mesure du
  12-09-2026, inscrite en commentaire juste au-dessus de la lecture, dit
  pourquoi : le taux Fortuneo était alors écrit à CINQ endroits, et le jour où
  le courtier change son tarif, on en corrige un et quatre restent faux, sans
  aucune erreur affichée.
⑨ CE QUI CLOCHE —
  ① Les seuils de la stratégie sont écrits dans le code. `C5E10_TP = 0.040`,
    `C5E10_SL = 0.025` et `C5E10_HORIZON = 20` sont posés ici, et les mêmes
    valeurs sont écrites une seconde fois dans gouvernance/REGISTRE_REGLES.md à
    la règle R-201 : « TP +4 % · SL −2,5 % · 20 séances ». La loi du projet dit
    pourtant l'inverse : les seuils vivent au REGISTRE, jamais dans le code
    (R-743 §②). Les deux écritures disent la même chose aujourd'hui, vérifié le
    19-09-2026 ; le jour où Jean-Luc décide de passer l'objectif à +5 %, il
    corrige le REGISTRE et le programme continue de calculer à +4 % sans rien
    dire.
  ② L'univers est écrit ici une troisième fois, et les trois écritures ne se
    ressemblent plus. `C5E10_UNIVERS` porte dix noms de sociétés. La règle R-201
    du REGISTRE porte les mêmes dix. Mais donnees/cac40_strategies.csv, qui est
    l'état civil des stratégies, donne à la stratégie en production
    `C5E10-QA-V1` un univers de SIX mnémoniques — `EN,BVI,FGR,RNO,URW,VIE` — et
    garde les dix pour `C5E10-OBS-V1`. Et
    programmes/DETECTER_LES_SIGNAUX_GITHUB.py, ligne 105, en porte une quatrième
    copie sous le commentaire « les dix valeurs du module ». Quatre listes,
    relevées le 19-09-2026, dont une qui a déjà divergé.
  ③ L'orthographe `UNIBAIL_RODAMCO` n'existe dans aucun fichier de cours. Mesuré
    le 19-09-2026 sur donnees/cours_maitre.csv : le fichier porte
    `UNIBAIL-RODAMCO-WESTFIELD` sur 644 lignes et `UNIBAIL_RODAMCO_WESTFIELD`
    sur 50, jamais `UNIBAIL_RODAMCO`. Un appelant qui range les cours sous le
    nom écrit dans le fichier obtient, sur ces mêmes données, 75 opérations et
    +83 834,24 € ; le même appel après rapprochement des orthographes en donne
    103 et +109 434,24 €. Vingt- huit opérations et 25 600 € disparaissent, sans
    aucune erreur affichée. Ce module ne s'en protège pas : c'est `cle_valeur`
    de programmes/JUGE_DES_STRATEGIES.py qui rapproche les graphies, et rien n'oblige un
    appelant à passer par elle.
  ④ La mécanique de sortie est une seconde implémentation de celle qui vit chez
    `MODULE_POSITIONS.sortie_position`, et les deux divergent. Celle d'ici teste
    seulement si le plus bas de la séance touche le stop puis si le plus haut
    touche l'objectif ; celle de MODULE_POSITIONS teste d'abord l'OUVERTURE, ce
    qui attrape les sauts de cours. Mesuré le 19-09-2026 sur une séance qui
    ouvre à 94,00 pour une entrée à 100,00 et un stop à 97,50 : ce module compte
    −2 800,00 € en sortant au prix du stop, MODULE_POSITIONS compte −6 291,00 €
    en sortant au prix d'ouverture réel. Trois mille quatre cent
    quatre-vingt-onze euros d'écart sur une seule opération. Deux
    implémentations d'une même chose divergent toujours (R-708).
  ⑤ Les frais sont un forfait sur le capital, alors que le tarif porte sur la
    valeur échangée. Ici le calcul est deux fois le taux multiplié par les 100
    000 € de capital, soit 300,00 € quel que soit le résultat du trade. Chez
    MODULE_POSITIONS, les frais du second ordre portent sur ce que la vente
    rapporte. Mesuré le 19-09-2026 sur une entrée à 100,00 : un objectif touché
    à 104,00 coûte 306,00 € de frais au lieu de 300,00 €, et un stop touché à
    97,50 en coûte 296,25 €. Le radar du soir connaît déjà cet écart et le range
    en avertissement, jamais en erreur : programmes/audit_ecosysteme.py
    l'appelle « écart de CONVENTION DE FRAIS » et précise que « le journal
    inscrit les frais RÉELS, le module applique un forfait ».
  ⑥ La suite des épreuves reste verte quand on lui retire une épreuve. Mesuré le
    19-09-2026 sur une copie dont la septième épreuve a été supprimée :
    l'affichage est « ✅ 6/7 tests unitaires PASSÉS — mécanique C5-ETENDU-10
    prouvée » et le code de sortie relevé juste après est 0. Le nombre 7 est
    écrit en dur dans le message au lieu d'être compté, et rien ne compare le
    nombre d'épreuves passées au nombre d'épreuves attendues. Une épreuve qui
    disparaît ne fait donc pas rougir.
  ⑦ Le nom du fichier porte une date, et un appelant l'écrit en entier.
    programmes/DETECTER_LES_SIGNAUX_GITHUB.py, ligne 154, charge
    `programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py` caractère par
    caractère. Renommer ce fichier — ce que la règle d'horodatage des noms
    invite à faire à chaque nouvelle version — arrête le pas n°5 du circuit du
    soir, et donc la détection des signaux, sans qu'aucun autre programme ne
    prévienne.
  ⑧ Les deux textes d'origine des fonctions de calcul renvoient à un fichier
    disparu. `_c5e10_cmf` annonce être « identique à calculer_cmf du monolithe »
    et `_c5e10_cci` « identique à calculer_cci_vpb du monolithe ». Mesuré le
    19-09-2026 : une recherche de `calculer_cmf` et de `calculer_cci_vpb` dans
    tous les fichiers Python du dépôt ne les trouve que dans ce module lui-même.
    La comparaison promise n'est donc vérifiable par personne.
⑩ EFFET — N'écrit aucun fichier et ne touche pas au réseau. Au chargement, il
  EXÉCUTE le fichier `MODULE_POSITIONS.py` voisin, en entier, pour y lire une
  seule constante : tout ce que ce fichier ferait à son propre chargement se
  produirait donc ici. Mesuré le 19-09-2026 : ce voisin ne fait que poser des
  constantes et définir des fonctions, et le chargement rend `C5E10_FRAIS =
  0.0015`.
⑪ TERMINAISON — Lancé seul : SORT DU PROGRAMME avec le code 0 quand les sept
  épreuves passent, mesuré le 19-09-2026 ; une épreuve fausse lève
  `AssertionError`, ce qui arrête le programme avec le code 1. Chargé comme
  module : LÈVE `ImportError` si `MODULE_POSITIONS.py` n'est pas dans son
  dossier, et le chargement ne rend alors jamais la main.
⑫ DÉFINITIONS
  CCI : l'indice du canal des matières premières, qui mesure de combien le
    cours s'écarte de sa moyenne récente ; sans unité, typiquement entre −200
    et +200.
  CMF : le flux monétaire de Chaikin, qui mesure si l'argent entre ou sort
    d'une valeur ; sans unité, borné à ±1.
  l'univers : la liste des valeurs sur lesquelles une stratégie a le droit d'acheter, désignées par leur mnémonique
  la grille : la liste des huit critères et de leurs seuils ; celle qui tourne s'appelle GRILLE-26-04 et vit dans `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740 de ce fichier
  le backtest : le rejeu d'une stratégie sur des cours passés, pour estimer ce
    qu'elle aurait donné
  le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir, qui contrôle l'ensemble du système et range chacun de ses constats sous un numéro de maillon, par exemple 18-Tâches pour le contrôle des traces laissées par les tâches planifiées.
  le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
  une séance : une journée de bourse pour une valeur, avec son ouverture, son
    plus haut, son plus bas, sa clôture et son volume.
  C5-ETENDU-10 : le nom de la stratégie vivante ; ses seuils et son horizon sont lus dans `donnees/cac40_strategies.csv`.
  PRODUCTION : l etat d une strategie dont le seuil d operations est atteint et les resultats conformes, donc exploitee.
  le CCI : un indicateur de bourse qui mesure de combien le prix s'écarte de sa moyenne des quatorze dernières séances.
  le CMF : un indicateur de bourse qui mesure si l'argent entre ou sort d'une valeur sur les quatorze dernières séances.
  le signal : le jour où la stratégie dit d'acheter ; l'achat lui-même a lieu à l'ouverture de la séance suivante
"""
import statistics as _st

C5E10_UNIVERS  = ["TOTALENERGIES", "ENGIE", "VEOLIA", "BOUYGUES", "EIFFAGE",
                  "AIRBUS", "RENAULT", "UNIBAIL_RODAMCO", "BUREAU_VERITAS", "VINCI"]
C5E10_CMF_P    = 14
C5E10_CCI_P    = 14
C5E10_CCI_SEUIL = -50.0
C5E10_TP       = 0.040     # +4.0%
C5E10_SL       = 0.025     # -2.5%
C5E10_HORIZON  = 20        # séances de détention max après l'entrée
C5E10_CAPITAL  = 100_000
# LE TAUX VIENT DE SON PROPRIETAIRE, JAMAIS D UNE COPIE (R-708).
# Mesure du 12-09-2026 : le taux Fortuneo etait ecrit a CINQ endroits —
# MODULE_POSITIONS (le proprietaire declare, decision A-50 du 11/08),
# ici, deux fois dans MODULE_JUGEMENT, et en parametre par defaut de
# MESURER_LA_PERFORMANCE. **Le jour ou Fortuneo change son tarif, on en
# corrige un et quatre restent faux — sans erreur visible.**
# Le radar signale deja « ecart de CONVENTION DE FRAIS » sur cinq trades.
def _frais_du_proprietaire():
    """Va lire le taux de frais chez le programme qui en est propriétaire.

    ① RÔLE — Empêcher que le tarif du courtier soit écrit une fois de plus.
      Cette fonction ne calcule rien : elle ouvre le fichier voisin
      `MODULE_POSITIONS.py`, y prend la valeur de `FRAIS_TAUX` et la rend, pour
      que ce module travaille sur le même chiffre que le reste du système au
      lieu d'en garder une copie.
    ② CONTEXTE D'APPEL — Une seule fois, au CHARGEMENT du fichier, pour donner
      sa valeur à `C5E10_FRAIS`. Jamais appelée ensuite. Tout programme qui
      charge ce module la déclenche donc sans le savoir : le détecteur de
      signaux du soir, le radar de 22 h et le juge des stratégies.
    ③ ENTRÉE — Aucun paramètre. Elle se repère toute seule, à partir du dossier
      où se trouve ce fichier.
    ④ CONDITIONS D'ENTRÉE — Le fichier `MODULE_POSITIONS.py` doit exister dans
      le même dossier que ce module, être du Python valide, et porter une
      variable nommée `FRAIS_TAUX` dont la valeur se convertit en nombre.
    ⑤ SORTIE — UNE valeur : le taux de frais d'un ordre, en fraction. Mesuré le
      19-09-2026, elle rend 0,0015, soit 0,15 %.
      [rend: 1]
    ⑥ TRAITEMENT — ① relever le dossier où vit ce fichier · ② y chercher, dans
      l'ordre, `MODULE_POSITIONS.py` puis `MODULE POSITIONS.py` · ③ au premier
      trouvé, charger et EXÉCUTER ce fichier entier · ④ rendre sa variable
      `FRAIS_TAUX` convertie en nombre · ⑤ si aucun des deux noms n'existe,
      lever une erreur au lieu de se rabattre sur une valeur écrite ici.
    ⑦ UNITÉ — Une FRACTION, jamais un pourcent : 0,0015 vaut 0,15 %. Confondre
      les deux fait payer cent fois les frais, et le résultat reste plausible.
    ⑧ POURQUOI — Un chiffre qui existe ailleurs ne se recopie pas, parce que
      deux copies divergent toujours (R-708). Le commentaire posé juste
      au-dessus de cette fonction donne la mesure qui l'a fait écrire : le
      12-09-2026, le taux Fortuneo était inscrit à CINQ endroits — chez son
      propriétaire déclaré `MODULE_POSITIONS`, ici, deux fois dans
      `MODULE_JUGEMENT`, et comme valeur par défaut d'un paramètre de
      `MESURER_LA_PERFORMANCE`. Le jour où le courtier change son tarif, on en
      corrige un et quatre restent faux, sans aucune erreur affichée. Et elle
      LÈVE au lieu de se replier sur une valeur de secours : une valeur de
      secours serait exactement la sixième copie que cette fonction existe pour
      empêcher.
    ⑨ CE QUI CLOCHE —
      ① Elle épelle deux noms de fichier au lieu de porter sur une propriété. Le
        critère qui tranche tient en une question : si je renomme un fichier,
        mon contrôle change-t-il d'avis ? Ici oui. `MODULE_POSITIONS.py` et
        `MODULE POSITIONS.py` sont cherchés à la lettre ; toute autre graphie, y
        compris un nom horodaté comme en portent la moitié des programmes du
        dépôt, fait lever l'erreur alors que le fichier est là.
      ② Le taux lu n'est contrôlé par rien. La valeur est convertie en nombre et
        rendue telle quelle : un `FRAIS_TAUX` passé par erreur à 0,15 au lieu de
        0,0015 serait accepté, et chaque opération porterait 30 000 € de frais
        au lieu de 300 €.
      ③ Elle exécute un fichier entier pour lire une seule constante. Le
        chargement n'est pas une lecture : tout ce que `MODULE_POSITIONS.py`
        ferait à son propre chargement — écrire, afficher, appeler le réseau —
        se produirait ici, au simple chargement de ce module. Mesuré le
        19-09-2026, ce voisin ne fait aujourd'hui que poser des constantes et
        définir des fonctions ; rien ne garantit qu'il en restera là.
    ⑩ EFFET — LIT le dossier de ce fichier et EXÉCUTE le fichier voisin trouvé.
      N'écrit rien, ne touche pas au réseau. Importe deux modules du langage au
      moment de l'appel plutôt qu'en tête de fichier.
    ⑪ TERMINAISON — Rend la main avec le taux quand le voisin est là. LÈVE
      `ImportError` sinon, avec le message « MODULE_POSITIONS introuvable : on
      ne recopie PAS son taux de frais » — mesuré le 19-09-2026 en copiant ce
      module seul dans un dossier vide. Comme elle est appelée au chargement,
      cette erreur empêche le module entier de se charger. Et un de ses appels
      peut ne pas revenir : l'exécution du fichier voisin lève tout ce que ce
      fichier lèverait.
      [sort: non]
    ⑫ DÉFINITIONS
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
      le détecteur : programmes/DETECTER_LES_SIGNAUX_GITHUB.py, qui écrit les
        signaux du jour
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir, qui contrôle l'ensemble du système et range chacun de ses constats sous un numéro de maillon, par exemple 18-Tâches pour le contrôle des traces laissées par les tâches planifiées.
    
      une fraction : la façon d'écrire un pourcentage entre 0 et 1 — 0,040 pour +4 % — par opposition au pourcent, qui écrirait 4.0
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    import os as _os, importlib.util as _ilu
    _ici = _os.path.dirname(_os.path.abspath(__file__))
    for _n in ("MODULE_POSITIONS.py", "MODULE POSITIONS.py"):
        _p = _os.path.join(_ici, _n)
        if _os.path.isfile(_p):
            _sp = _ilu.spec_from_file_location("_mp_frais", _p)
            _m = _ilu.module_from_spec(_sp); _sp.loader.exec_module(_m)
            return float(_m.FRAIS_TAUX)
    raise ImportError("MODULE_POSITIONS introuvable : on ne recopie PAS son taux de frais")


C5E10_FRAIS    = _frais_du_proprietaire()   # 0,15 % par ordre, lu chez MODULE_POSITIONS


def _c5e10_cmf(ohlcv, periode=C5E10_CMF_P):
    """Calcule, séance par séance, le flux monétaire de Chaikin sur une fenêtre
      glissante.

    ① RÔLE — Fournir la première des deux conditions du signal d'achat : dire si
      l'argent entre ou sort d'une valeur. Le nombre rendu est négatif quand les
      clôtures se font près du bas des séances, positif quand elles se font près
      du haut. C'est son passage du négatif au positif que la stratégie guette.
    ② CONTEXTE D'APPEL — `signaux_c5etendu10`, une fois par valeur, sur toute
      son histoire. Et programmes/DETECTER_LES_SIGNAUX_GITHUB.py, ligne 307, qui
      l'appelle directement chaque soir de semaine pour inscrire la valeur du
      jour dans le fichier de signaux publié, alors que le blanc souligné en
      tête de son nom annonce un usage interne à ce module.
    ③ ENTRÉE — `ohlcv` : la liste des séances d'UNE valeur, triée par date
      croissante, chaque séance portant au moins `high`, `low`, `close` et
      `volume`. `periode` : le nombre de séances de la fenêtre, 14 par défaut,
      valeur de `C5E10_CMF_P` ; aucun appelant ne passe autre chose, mesuré le
      19-09-2026.
    ④ CONDITIONS D'ENTRÉE — Les séances doivent être triées par date croissante
      : la fonction ne trie pas et ne vérifie pas l'ordre. Chaque séance doit
      porter les quatre clés nommées, sans quoi la fonction lève. `periode` doit
      valoir au moins 1.
    ⑤ SORTIE — UNE valeur : une liste EXACTEMENT aussi longue que `ohlcv`, où
      les `periode − 1` premières cases valent `None` faute d'assez d'histoire,
      et les suivantes un nombre. Rendre une liste de même longueur est ce qui
      permet à l'appelant d'utiliser le même indice pour les cours et pour
      l'indicateur.
      [rend: 1]
    ⑥ TRAITEMENT — ① parcourir les séances une à une · ② pour les `periode − 1`
      premières, poser `None` et passer · ③ sinon, prendre la fenêtre des
      `periode` dernières séances · ④ dans chaque séance de la fenêtre, mesurer
      où la clôture se situe entre le plus bas et le plus haut, sur une échelle
      de −1 à +1, et sauter la séance si le plus haut égale le plus bas · ⑤
      pondérer cette position par le volume de la séance · ⑥ diviser la somme
      pondérée par la somme des volumes, ou poser zéro si cette somme est nulle.
    ⑦ UNITÉ — Un rapport SANS UNITÉ, borné à ±1. Les prix entrent en euros et
      les volumes en titres, mais les deux s'annulent dans la division : le
      résultat ne s'exprime ni en euros ni en titres. `periode` se compte en
      SÉANCES DE BOURSE.
    ⑧ POURQUOI — La pondération par le volume est tout l'intérêt de cet
      indicateur : une clôture au plus haut sur une séance sans échanges ne dit
      rien, la même sur une séance très échangée dit que des acheteurs sont
      arrivés. La suite des épreuves de ce module s'en sert d'ailleurs comme
      d'un levier : sa série construite fait basculer le CMF au-dessus de zéro
      en donnant à une seule séance un volume de 500 000 contre 1 000 aux
      autres. La fenêtre est de 14 séances parce que c'est le réglage de la
      stratégie, inscrit au REGISTRE sous la règle R-201 : « CMF(14) croise 0↑
      ET CCI(14)<−50 le même jour ».
    ⑨ CE QUI CLOCHE —
      ① Une fenêtre entièrement sans volume rend exactement zéro, et ce zéro est
        compté comme un retour de l'argent. Quand la somme des volumes de la
        fenêtre est nulle, la fonction pose 0 plutôt que `None` ; le test de
        croisement, lui, accepte zéro comme un passage au-dessus. Mesuré le
        19-09-2026 sur une série construite où le cours baisse de 0,50 € par
        séance et où le volume est rapporté à zéro pendant les dernières séances
        : `signaux_c5etendu10` rend un signal à l'indice 33, avec le CMF passant
        de −1,0 à 0 et le CCI à −123,8. C'est un ordre d'achat sur une valeur
        qui tombe et où il n'est entré aucun argent. La même mesure sur les 26
        690 lignes de donnees/cours_maitre.csv ne trouve aucune séance à volume
        nul : le défaut n'a jamais eu l'occasion de se produire sur les données
        réelles, et rien ne l'empêcherait le jour où la source en rendrait une.
      ② Une séance où le plus haut égale le plus bas est sautée sans que son
        volume soit compté, alors que les titres se sont bien échangés à ce
        prix-là. Deux traitements du même cas cohabitent donc dans cette
        fonction : une séance à prix figé disparaît de la moyenne, une fenêtre
        entière à prix figé rend zéro.
      ③ Le texte d'origine annonce « identique à calculer_cmf du monolithe ».
        Mesuré le 19-09-2026, une recherche de `calculer_cmf` dans tous les
        fichiers Python du dépôt ne le trouve que dans ce module : le fichier
        auquel la phrase renvoie n'existe plus, et l'identité promise n'est
        vérifiable par personne.
      ④ La fenêtre est recalculée en entier à chaque séance au lieu d'être
        glissée. Sur 694 séances et 14 de fenêtre, cela fait environ 9 700
        opérations au lieu de 700. Sans conséquence au volume actuel, mesuré
        instantané le 19-09-2026 ; c'est un coût, pas une faute.
    ⑩ EFFET — Aucun. N'écrit rien, ne lit aucun fichier, ne touche pas au
      réseau, et ne modifie pas la liste qu'elle reçoit.
    ⑪ TERMINAISON — Rend toujours la main quand les séances portent leurs quatre
      clés. LÈVE `KeyError` sur une séance à laquelle il manque `high`, `low`,
      `close` ou `volume`, et `TypeError` si l'une de ces valeurs est un texte
      au lieu d'un nombre. Aucun de ses appels ne se termine : elle n'appelle
      que des fonctions du langage.
      [sort: non]
    ⑫ DÉFINITIONS
      CCI : l'indice du canal des matières premières, qui mesure de combien le
        cours s'écarte de sa moyenne récente ; sans unité, typiquement entre −200
        et +200.
      CMF : le flux monétaire de Chaikin, qui mesure si l'argent entre ou sort
        d'une valeur ; sans unité, borné à ±1.
      un signal : le repérage, sur la dernière séance connue, d'une configuration
        de cours qui déclenche une simulation d'achat.
      une séance : une journée de bourse pour une valeur, avec son ouverture, son
        plus haut, son plus bas, sa clôture et son volume.
    
      le CCI : un indicateur de bourse qui mesure de combien le prix s'écarte de sa moyenne des quatorze dernières séances.
      le CMF : un indicateur de bourse qui mesure si l'argent entre ou sort d'une valeur sur les quatorze dernières séances.
      une fenêtre : un morceau de la période, jugé séparément des autres
"""
    serie = []
    for i in range(len(ohlcv)):
        if i < periode - 1:
            serie.append(None)
            continue
        fen = ohlcv[i - periode + 1: i + 1]
        num = den = 0.0
        for bar in fen:
            hl = bar["high"] - bar["low"]
            if hl == 0:
                continue
            mfm = ((bar["close"] - bar["low"]) - (bar["high"] - bar["close"])) / hl
            num += mfm * bar["volume"]
            den += bar["volume"]
        serie.append(num / den if den else 0)
    return serie


def _c5e10_cci(ohlcv, periode=C5E10_CCI_P):
    """Calcule, séance par séance, l'indice du canal des matières premières.

    ① RÔLE — Fournir la seconde des deux conditions du signal d'achat : dire de
      combien le cours s'est écarté de sa moyenne récente, vers le bas. La
      stratégie n'achète que sur une valeur très descendue, et c'est ce nombre
      qui le mesure : plus il est négatif, plus le cours est bas par rapport à
      ses dernières semaines.
    ② CONTEXTE D'APPEL — `signaux_c5etendu10`, une fois par valeur, sur toute
      son histoire. Et programmes/DETECTER_LES_SIGNAUX_GITHUB.py, ligne 307, qui
      l'appelle directement chaque soir de semaine pour inscrire la valeur du
      jour dans le fichier de signaux publié, alors que le blanc souligné en
      tête de son nom annonce un usage interne à ce module.
    ③ ENTRÉE — `ohlcv` : la liste des séances d'UNE valeur, triée par date
      croissante, chaque séance portant au moins `high`, `low` et `close`.
      `periode` : le nombre de séances de la fenêtre, 14 par défaut, valeur de
      `C5E10_CCI_P` ; aucun appelant ne passe autre chose, mesuré le 19-09-2026.
    ④ CONDITIONS D'ENTRÉE — Les séances doivent être triées par date croissante
      : la fonction ne trie pas et ne vérifie pas l'ordre. Chaque séance doit
      porter les trois clés nommées. `periode` doit valoir au moins 1.
    ⑤ SORTIE — UNE valeur : une liste EXACTEMENT aussi longue que `ohlcv`, où
      les `periode − 1` premières cases valent `None` faute d'assez d'histoire,
      et les suivantes un nombre. La même longueur que l'entrée est ce qui
      permet à l'appelant d'utiliser le même indice pour les cours et pour
      l'indicateur.
      [rend: 1]
    ⑥ TRAITEMENT — ① pour chaque séance à partir de la `periode`-ième, prendre
      la fenêtre des `periode` dernières séances · ② calculer pour chacune son
      prix typique, moyenne du plus haut, du plus bas et de la clôture · ③
      prendre la moyenne de ces prix typiques sur la fenêtre · ④ prendre la
      moyenne des écarts, en valeur absolue, entre chaque prix typique et cette
      moyenne · ⑤ diviser l'écart du jour à la moyenne par cet écart moyen
      multiplié par 0,015 · ⑥ poser 0,0 quand l'écart moyen est nul.
    ⑦ UNITÉ — Un indice SANS UNITÉ. Les prix entrent en euros et s'annulent dans
      la division. Le facteur 0,015 est une constante de la formule d'origine,
      choisie pour qu'environ 70 à 80 % des valeurs tombent entre −100 et +100 ;
      il ne se règle pas. `periode` se compte en SÉANCES DE BOURSE.
    ⑧ POURQUOI — Le prix typique est employé plutôt que la seule clôture parce
      qu'il résume la séance entière : une clôture peut être un accident de
      dernière minute, la moyenne du haut, du bas et de la clôture ne l'est pas.
      Et l'écart se rapporte à l'écart moyen de la période plutôt qu'à un nombre
      d'euros, ce qui rend l'indice comparable d'une valeur à l'autre : −60 veut
      dire la même chose sur une action à 10 € et sur une action à 300 €. Le
      seuil de −50 et la fenêtre de 14 séances viennent du REGISTRE, règle R-201
      : « CMF(14) croise 0↑ ET CCI(14)<−50 le même jour ».
    ⑨ CE QUI CLOCHE —
      ① Une fenêtre à prix strictement figé rend 0,0. Mesuré le 19-09-2026 sur
        quatorze séances toutes à 100,00 € : l'indice vaut 0,0. Ici le zéro est
        sans danger, parce que la stratégie n'achète que sous −50 et que zéro
        n'y est pas ; mais c'est le traitement INVERSE de celui que fait
        `_c5e10_cmf` sur la même situation dégénérée, où le zéro est compté
        comme un signal d'achat. Deux fonctions voisines du même fichier
        traitent donc « je ne sais pas » de deux façons opposées, et rien ne le
        dit.
      ② Le nom dit « vpb » dans son texte d'origine — « identique à
        calculer_cci_vpb du monolithe » — sans que ces trois lettres soient
        expliquées nulle part. Mesuré le 19-09-2026, une recherche de
        `calculer_cci_vpb` dans tous les fichiers Python du dépôt ne le trouve
        que dans ce module : le fichier auquel la phrase renvoie n'existe plus,
        et personne ne peut vérifier l'identité promise ni ce que « vpb »
        désignait.
      ③ Le facteur 0,015 est écrit dans la formule, sans nom. Un lecteur qui
        cherche à quoi correspond ce nombre ne trouve rien à quoi le rattacher,
        alors que tous les autres réglages du module portent un nom en tête de
        fichier.
      ④ La fenêtre est recalculée en entier à chaque séance. Sur 694 séances et
        14 de fenêtre, cela fait deux moyennes sur 14 valeurs pour chaque jour.
        Sans conséquence au volume actuel, mesuré instantané le 19-09-2026 ;
        c'est un coût, pas une faute.
    ⑩ EFFET — Aucun. N'écrit rien, ne lit aucun fichier, ne touche pas au
      réseau, et ne modifie pas la liste qu'elle reçoit.
    ⑪ TERMINAISON — Rend toujours la main quand les séances portent leurs trois
      clés. LÈVE `KeyError` sur une séance à laquelle il manque `high`, `low` ou
      `close`, et `TypeError` si l'une de ces valeurs est un texte au lieu d'un
      nombre. Aucun de ses appels ne se termine : elle n'appelle que des
      fonctions du langage et la moyenne de la bibliothèque de statistiques.
      [sort: non]
    ⑫ DÉFINITIONS
      CCI : l'indice du canal des matières premières, qui mesure de combien le
        cours s'écarte de sa moyenne récente ; sans unité, typiquement entre −200
        et +200.
      CMF : le flux monétaire de Chaikin, qui mesure si l'argent entre ou sort
        d'une valeur ; sans unité, borné à ±1.
      un signal : le repérage, sur la dernière séance connue, d'une configuration
        de cours qui déclenche une simulation d'achat.
      une séance : une journée de bourse pour une valeur, avec son ouverture, son
        plus haut, son plus bas, sa clôture et son volume.
    
      une action : une ligne de ce tableau, identifiée par `A-` suivi d'un nombre
      une fenêtre : un morceau de la période, jugé séparément des autres
"""
    n = len(ohlcv)
    vals = [None] * n
    for i in range(periode - 1, n):
        sl  = ohlcv[i - periode + 1: i + 1]
        tps = [(s["high"] + s["low"] + s["close"]) / 3 for s in sl]
        m   = _st.mean(tps)
        md  = _st.mean([abs(t - m) for t in tps])
        vals[i] = (tps[-1] - m) / (0.015 * md) if md else 0.0
    return vals


def signaux_c5etendu10(ohlcv):
    """Relève toutes les séances où le signal d'achat C5-ETENDU-10 est actif.

    ① RÔLE — C'est LA fonction qui décide un achat. Chaque soir de semaine, le
      pas n°5 du circuit lui passe l'histoire d'une valeur et retient ce qu'elle
      dit de la dernière séance ; ce qu'elle répond devient la proposition
      d'achat du lendemain à l'ouverture. Elle travaille sur une valeur à la
      fois et ne sait pas laquelle : c'est son appelant qui a choisi.
    ② CONTEXTE D'APPEL — Trois appelants. ①
      programmes/DETECTER_LES_SIGNAUX_GITHUB.py, pas n°5 du circuit du soir, une
      fois par valeur de son univers, chaque soir de semaine. ②
      programmes/JUGE_DES_STRATEGIES.py, qui la désigne par son nom dans le champ
      `_fonction_signal` de chaque fiche de stratégie et s'en sert pour son
      calibrage.
      ③ `backtest_c5etendu10` et la suite des épreuves, dans ce fichier.
    ③ ENTRÉE — `ohlcv` : la liste des séances d'UNE valeur, triée par date
      croissante, chaque séance portant `high`, `low`, `close` et `volume`.
      Aucun nom de valeur n'est demandé et aucun n'est vérifié.
    ④ CONDITIONS D'ENTRÉE — Les séances doivent être triées par date croissante
      et sans doublon : la fonction ne trie ni ne dédoublonne, et deux fois la
      même date décaleraient toute la fenêtre de calcul. Il en faut au moins 16
      — la fenêtre de 14, plus la veille, plus le jour — sans quoi la fonction
      rend une liste vide sans rien dire.
    ⑤ SORTIE — UNE valeur : une liste de dictionnaires, un par séance où le
      signal est actif, chacun portant `i` l'indice de la séance dans `ohlcv`,
      `cci` la valeur de l'indice ce jour-là et `cmf` celle du flux monétaire.
      Liste VIDE quand aucun signal n'est trouvé, et vide aussi quand l'histoire
      est trop courte — les deux cas ne se distinguent pas.
      [rend: 1]
    ⑥ TRAITEMENT — ① si l'histoire compte moins de 16 séances, rendre une liste
      vide ·
      ② calculer le flux monétaire sur toute l'histoire · ③ calculer l'indice
        sur toute l'histoire · ④ à partir de la quinzième séance, comparer le
        flux de la veille et celui du jour · ⑤ retenir la séance quand le flux
        était négatif la veille, est supérieur ou égal à zéro le jour même, et
        que l'indice du jour est sous −50.
    ⑦ UNITÉ — `i` est un INDICE DE LISTE, jamais une date : la séance
      correspondante se lit en reprenant `ohlcv[i]["date"]`. `cci` et `cmf` sont
      des nombres sans unité. Le seuil de −50 est un niveau d'indice, la fenêtre
      se compte en SÉANCES DE BOURSE.
    ⑧ POURQUOI — Les deux conditions doivent tomber LE MÊME JOUR, et c'est tout
      le sens de la stratégie : l'indice sous −50 dit que la valeur a beaucoup
      baissé, le flux qui repasse au-dessus de zéro dit que l'argent recommence
      à y entrer. Prise seule, la première condition fait acheter une valeur qui
      continue de tomber ; prise seule, la seconde fait acheter n'importe quoi.
      Le REGISTRE l'écrit sous la règle R-201 : « CMF(14) croise 0↑ ET
      CCI(14)<−50 le même jour ». Le croisement est exigé, et non simplement un
      flux positif : la fonction regarde la veille. Acheter tant que le flux
      reste positif ferait entrer sur une valeur déjà remontée depuis des
      semaines ; c'est le MOMENT du retournement qui est visé.
    ⑨ CE QUI CLOCHE —
      ① Elle ne connaît pas l'univers de la stratégie et n'a aucun moyen de le
        contrôler. Mesuré le 19-09-2026 : passée l'histoire d'une valeur
        bancaire, elle rend un signal normalement, alors que les banques sont
        exclues en permanence des signaux techniques par la règle R-204 du
        REGISTRE. Le filtre vit chez chaque appelant — `C5E10_UNIVERS` pour
        `backtest_c5etendu10`, une liste séparée dans le détecteur du soir — et
        rien ici ne le rappelle.
      ② Le croisement accepte l'égalité stricte à zéro. Le test retient le jour
        où le flux est « supérieur OU ÉGAL à zéro », et la fonction qui calcule
        ce flux rend exactement zéro quand elle ne sait pas conclure, faute de
        volume sur la fenêtre. Mesuré le 19-09-2026 sur une série construite où
        le cours baisse et où le volume est rapporté à zéro : un signal est
        rendu à l'indice 33, flux passant de −1,0 à 0, indice à −123,8. Un « je
        ne sais pas » est compté comme un « oui ».
      ③ Une histoire trop courte et une histoire sans aucun signal rendent la
        même réponse : une liste vide. Un appelant qui reçoit zéro signal ne
        peut pas savoir si la valeur n'a rien donné ou si ses cours manquent. Le
        détecteur du soir s'en protège par un calibrage sur un signal connu,
        mais c'est lui qui s'en protège, pas cette fonction.
      ④ Le seuil de déclenchement de la boucle et la longueur minimale exigée ne
        viennent pas du même endroit. Le refus porte sur « moins de 14 + 2
        séances » et la boucle démarre à la quatorzième, ce qui rend la fonction
        juste aujourd'hui parce que les deux fenêtres, celle du flux et celle de
        l'indice, valent toutes deux 14. Le jour où l'une des deux changerait,
        le refus et la boucle ne parleraient plus de la même chose.
    ⑩ EFFET — Aucun. N'écrit rien, ne lit aucun fichier, ne touche pas au
      réseau, et ne modifie pas la liste qu'elle reçoit.
    ⑪ TERMINAISON — Rend toujours la main. LÈVE `KeyError` ou `TypeError` par
      l'intermédiaire des deux fonctions de calcul qu'elle appelle, si une
      séance ne porte pas ses clés ou porte du texte à la place d'un nombre.
      Aucun de ses appels ne se termine : `_c5e10_cmf` et `_c5e10_cci` rendent
      toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS
      CCI : l'indice du canal des matières premières, qui mesure de combien le
        cours s'écarte de sa moyenne récente ; sans unité, typiquement entre −200
        et +200.
      CMF : le flux monétaire de Chaikin, qui mesure si l'argent entre ou sort
        d'une valeur ; sans unité, borné à ±1.
      l'univers : la liste des valeurs sur lesquelles une stratégie a le droit d'acheter, désignées par leur mnémonique
      la grille : la liste des huit critères et de leurs seuils ; celle qui tourne s'appelle GRILLE-26-04 et vit dans `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740 de ce fichier
      le détecteur : programmes/DETECTER_LES_SIGNAUX_GITHUB.py, qui écrit les
        signaux du jour
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
      un signal : le repérage, sur la dernière séance connue, d'une configuration
        de cours qui déclenche une simulation d'achat.
    
      C5-ETENDU-10 : le nom de la stratégie vivante ; ses seuils et son horizon sont lus dans `donnees/cac40_strategies.csv`.
      la boucle : la tache planifiee qui lit les signaux et rend compte
      le signal : le jour où la stratégie dit d'acheter ; l'achat lui-même a lieu à l'ouverture de la séance suivante
"""
    n = len(ohlcv)
    if n < C5E10_CMF_P + 2:
        return []
    cmf = _c5e10_cmf(ohlcv)
    cci = _c5e10_cci(ohlcv)
    out = []
    for i in range(C5E10_CMF_P, n):
        c, cp, cv = cmf[i], cmf[i - 1], cci[i]
        if c is None or cp is None or cv is None:
            continue
        if cp < 0 and c >= 0 and cv < C5E10_CCI_SEUIL:
            out.append({"i": i, "cci": cv, "cmf": c})
    return out


def _c5e10_sortie(ohlcv, i_signal):
    """Rejoue la vie d'un trade, de l'entrée du lendemain jusqu'à sa sortie.

    ① RÔLE — Chiffrer ce qu'un signal aurait rapporté. Elle pose l'achat à
      l'ouverture de la séance qui suit le signal, puis suit les séances une à
      une jusqu'à ce que le prix touche l'objectif, touche le stop, ou que le
      temps imparti soit écoulé. Elle sert deux fois : pour le backtest de ce
      module, et pour le contrôle du soir qui recalcule chaque trade déjà
      clôturé afin de vérifier que le journal ne s'est pas trompé.
    ② CONTEXTE D'APPEL — Deux appelants. ① `backtest_c5etendu10`, dans ce
      fichier, une fois par signal. ② programmes/audit_ecosysteme.py, maillon
      10, ligne 697 : chaque soir, il reprend chaque trade clôturé du journal,
      retrouve la séance d'entrée dans les cours, et lui passe l'indice de la
      séance PRÉCÉDENTE, puisque cette fonction entre au lendemain. Il compare
      ensuite le résultat qu'elle rend à celui inscrit au journal et alerte
      au-delà d'un euro d'écart.
    ③ ENTRÉE — `ohlcv` : la liste des séances d'UNE valeur, triée par date
      croissante. `i_signal` : l'indice, dans cette liste, de la séance où le
      signal a été vu.
    ④ CONDITIONS D'ENTRÉE — `i_signal` doit désigner une séance qui existe dans
      `ohlcv`, et chaque séance doit porter `open`, `high`, `low` et `close`. La
      fonction ne vérifie pas que le signal était réellement actif à cet indice
      : elle rejoue ce qu'on lui donne.
    ⑤ SORTIE — UNE valeur, de deux formes. Soit un dictionnaire de six cases :
      `i_in` et `i_out`, les indices des séances d'entrée et de sortie, `px_in`
      et `px_out`, les prix d'entrée et de sortie arrondis au dix-millième,
      `motif`, qui vaut « TP », « SL » ou « HORIZON », et `pnl`, le résultat net
      en euros arrondi au centime. Soit `None`, dans DEUX situations qui ne se
      distinguent pas : il n'existe pas de séance après le signal, ou le trade
      est encore ouvert à la fin des données disponibles.
      [rend: 1]
    ⑥ TRAITEMENT — ① l'entrée se fait à la séance suivant le signal ; s'il n'y
      en a pas, rendre `None` · ② prendre le prix d'ouverture de cette séance
      comme prix d'entrée ·
      ③ poser l'objectif à +4,0 % et le stop à −2,5 % de ce prix · ④ borner la
        recherche à 20 séances après l'entrée, ou à la dernière séance connue si
        elle arrive avant ·
      ⑤ parcourir les séances : si le plus bas touche le stop, sortir au stop ;
        sinon, si le plus haut touche l'objectif, sortir à l'objectif · ⑥ si
        rien n'a été touché et que les données se sont arrêtées avant la fin du
        délai, rendre `None` · ⑦ sinon, sortir à la clôture de la dernière
        séance du délai · ⑧ chiffrer le résultat brut sur 100 000 € et
        retrancher les frais de deux ordres.
    ⑦ UNITÉ — `px_in` et `px_out` en EUROS, `pnl` en EUROS. `i_in` et `i_signal`
      sont des INDICES DE LISTE, jamais des dates. Le délai de 20 se compte en
      SÉANCES DE BOURSE, jamais en jours de calendrier : 20 séances font environ
      quatre semaines.
    ⑧ POURQUOI — L'entrée se fait à l'OUVERTURE DU LENDEMAIN, et jamais à la
      clôture du jour du signal, parce qu'au moment où le cours de clôture est
      connu le marché est fermé : acheter à ce prix est impossible. Le REGISTRE
      en fait une règle, R-601 : « Entrée Open J+1, JAMAIS au close ». Trois
      stratégies du registre des stratégies ont été archivées pour ce seul vice
      de méthode. Le stop est testé AVANT l'objectif dans chaque séance, et
      c'est la convention pessimiste, règle R-602 du REGISTRE : « TP et SL même
      jour → SL compté ». Une séance ne dit pas dans quel ordre le plus haut et
      le plus bas ont été atteints ; choisir systématiquement le moins favorable
      fait des résultats un plancher plutôt qu'une promesse.
    ⑨ CE QUI CLOCHE —
      ① C'est une seconde implémentation de la mécanique de sortie, et elle
        diverge de la première. `MODULE_POSITIONS.sortie_position` teste quatre
        choses dans l'ordre, en commençant par l'OUVERTURE, ce qui attrape les
        sauts de cours ; celle-ci n'en teste que deux et ne regarde jamais
        l'ouverture. Mesuré le 19-09-2026 sur une séance qui ouvre à 94,00 €
        pour une entrée à 100,00 € et un stop à 97,50 € : cette fonction rend «
        SL, −2 800,00 € » en supposant une sortie au prix du stop, quand
        MODULE_POSITIONS rend « SL_GAP, −6 291,00 € » au prix d'ouverture
        réellement disponible. Trois mille quatre cent quatre-vingt-onze euros
        d'écart sur une seule opération. Deux implémentations d'une même chose
        divergent toujours (R-708).
      ② Les frais sont un forfait sur le capital. Le calcul retranche deux fois
        le taux multiplié par les 100 000 € engagés, soit 300,00 € quel que soit
        le résultat. Le tarif réel porte sur la valeur échangée, donc sur ce que
        la vente rapporte. Mesuré le 19-09-2026 sur une entrée à 100,00 € : un
        objectif touché à 104,00 € coûte 306,00 € de frais et non 300,00 €, un
        stop touché à 97,50 € en coûte 296,25 €. Le radar du soir connaît
        l'écart et le range en avertissement, jamais en erreur.
      ③ `None` recouvre deux situations opposées. Pas de séance après le signal,
        et trade encore ouvert à la fin des données, rendent la même réponse.
        L'appelant ne peut pas les distinguer, et le premier appelant en tire
        une conséquence fausse — voir le point ④ du texte de
        `backtest_c5etendu10`.
      ④ Les seuils sont lus dans le code et non au REGISTRE. `C5E10_TP`,
        `C5E10_SL` et `C5E10_HORIZON` sont posés en tête de ce fichier, alors
        que la loi du projet dit que les seuils vivent au REGISTRE et jamais
        dans le code (R-743 §②), et que la règle R-201 les y écrit déjà. Les
        deux disent la même chose aujourd'hui, vérifié le 19-09-2026 ; rien ne
        garantit qu'elles le diront demain.
      ⑤ La sortie par délai écoulé n'est atteinte que si les données vont
        jusqu'au bout. Une valeur retirée de la cote, ou un historique qui
        s'arrête, fait disparaître le trade au lieu de le clôturer au dernier
        cours connu. Ce choix est défendable pour un backtest, mais il n'est
        écrit nulle part ailleurs que dans ce code.
    ⑩ EFFET — Aucun. N'écrit rien, ne lit aucun fichier, ne touche pas au
      réseau, et ne modifie pas la liste qu'elle reçoit.
    ⑪ TERMINAISON — Rend toujours la main. LÈVE `KeyError` sur une séance à
      laquelle il manque `open`, `high`, `low` ou `close`, `IndexError` si
      `i_signal` désigne une séance qui n'existe pas, et `TypeError` si un prix
      est un texte au lieu d'un nombre. Aucun de ses appels ne se termine : elle
      n'appelle que des fonctions du langage.
      [sort: non]
    ⑫ DÉFINITIONS
      la grille : la liste des huit critères et de leurs seuils ; celle qui tourne s'appelle GRILLE-26-04 et vit dans `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740 de ce fichier
      le backtest : le rejeu d'une stratégie sur des cours passés, pour estimer ce
        qu'elle aurait donné
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir, qui contrôle l'ensemble du système et range chacun de ses constats sous un numéro de maillon, par exemple 18-Tâches pour le contrôle des traces laissées par les tâches planifiées.
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
      un signal : le repérage, sur la dernière séance connue, d'une configuration
        de cours qui déclenche une simulation d'achat.
      un trade : une opération simulée, de l'achat à la revente
      une opération : un achat simulé suivi de sa revente, avec son gain net en
        euros ; aucun ordre réel n'est jamais passé
      une séance : une journée de bourse pour une valeur, avec son ouverture, son
        plus haut, son plus bas, sa clôture et son volume.
    
      la convention : le prix de sortie théorique, celui de l'objectif ou du stop, par opposition au prix réellement observé. C'est ce qui permet de comparer une opération vécue à un test sur le passé
      le signal : le jour où la stratégie dit d'acheter ; l'achat lui-même a lieu à l'ouverture de la séance suivante
"""
    n = len(ohlcv)
    i_in = i_signal + 1
    if i_in >= n:
        return None
    px_in = ohlcv[i_in]["open"]
    tp = px_in * (1 + C5E10_TP)
    sl = px_in * (1 - C5E10_SL)
    i_max = min(i_in + C5E10_HORIZON, n - 1)
    px_out, motif, i_out = None, None, None
    for j in range(i_in, i_max + 1):
        bar = ohlcv[j]
        if bar["low"] <= sl:            # pessimiste : SL d'abord
            px_out, motif, i_out = sl, "SL", j
            break
        if bar["high"] >= tp:
            px_out, motif, i_out = tp, "TP", j
            break
    if px_out is None:
        if i_max < i_in + C5E10_HORIZON:
            return None                 # trade encore ouvert (fin de données)
        px_out, motif, i_out = ohlcv[i_max]["close"], "HORIZON", i_max
    brut = C5E10_CAPITAL * (px_out / px_in - 1)
    pnl  = brut - 2 * C5E10_FRAIS * C5E10_CAPITAL
    return {"i_in": i_in, "i_out": i_out, "px_in": round(px_in, 4),
            "px_out": round(px_out, 4), "motif": motif, "pnl": round(pnl, 2)}


def backtest_c5etendu10(donnees):
    """Rejoue toute l'histoire de la stratégie et rend les deux comptabilités.

    ① RÔLE — Donner les chiffres de référence de la stratégie : combien
      d'opérations, quelle part de gagnantes, combien d'euros au total, sur
      toute la période disponible. Elle rend ces chiffres DEUX FOIS, selon deux
      façons de compter qui ne s'additionnent jamais — l'une mesure la qualité
      du signal, l'autre ce qu'un compte unique aurait réellement pu faire.
    ② CONTEXTE D'APPEL — AUCUN APPELANT AUTOMATIQUE à ce jour. Mesuré le
      19-09-2026 : une recherche de `backtest_c5etendu10` dans tous les fichiers
      Python, tous les fichiers de tâches planifiées et tous les prompts du
      dépôt ne la trouve appelée que par les sept épreuves de ce fichier même.
      Le circuit du soir n'appelle que `signaux_c5etendu10`, le radar n'appelle
      que `_c5e10_sortie`, et le juge des stratégies a sa propre mécanique de jeu. Elle
      reste la fonction qui a produit les chiffres figés de référence, et le
      seul moyen de les refaire à l'identique.
    ③ ENTRÉE — `donnees` : un dictionnaire dont chaque clé est un nom de valeur
      et chaque contenu la liste des séances de cette valeur, triée par date
      croissante. Les valeurs absentes du dictionnaire sont ignorées.
    ④ CONDITIONS D'ENTRÉE — Les clés doivent être écrites EXACTEMENT comme dans
      `C5E10_UNIVERS`, sans quoi la valeur est ignorée en silence. Les listes
      doivent être triées par date croissante et partager le même calendrier de
      dates, parce que la comptabilité à un jeton compare des dates d'une valeur
      à l'autre.
    ⑤ SORTIE — UNE valeur : un dictionnaire de deux entrées, `qualite_signal` et
      `vraie_vie`. Chacune porte `trades`, la liste des opérations, `n`, leur
      nombre, `wr`, la part de gagnantes en pourcent arrondie au dixième, et
      `net`, le total en euros arrondi au centime. `wr` vaut `None` — et non
      zéro — quand il n'y a aucune opération, parce qu'une part de gagnantes sur
      zéro opération n'existe pas.
      [rend: 1]
    ⑥ TRAITEMENT — ① pour chaque valeur de l'univers présente dans les données,
      relever tous ses signaux et les ranger par date · ② pour chaque date,
      désigner le candidat dont l'indice est le plus bas, à égalité le premier
      dans l'ordre alphabétique ·
      ③ comptabilité à jetons illimités : rejouer TOUS les signaux, y compris
        plusieurs le même jour · ④ comptabilité à un jeton : parcourir les
        candidats retenus dans l'ordre des dates, ignorer ceux qui tombent alors
        qu'une position est encore ouverte, et noter après chaque sortie la date
        où le capital redevient libre ·
      ⑤ résumer chaque liste en nombre, part de gagnantes et total.
    ⑦ UNITÉ — `net` en EUROS. `wr` en POURCENTS, pas en fraction : 61,0 veut
      dire 61,0 %. `n` se compte en OPÉRATIONS, jamais en signaux : un signal
      qu'on n'a pas pu jouer n'est pas une opération. Les dates sont comparées
      comme du texte, ce qui suppose qu'elles s'écrivent année, mois, jour.
    ⑧ POURQUOI — Les DEUX comptabilités existent parce qu'elles répondent à deux
      questions différentes et qu'on les confondait. « Jetons illimités » joue
      tous les signaux et mesure si le signal vaut quelque chose ; « un jeton »
      n'en détient qu'un à la fois et mesure ce qu'un compte de 100 000 € aurait
      fait. Les additionner, ou présenter l'une pour l'autre, revient à
      promettre des gains qu'aucun compte ne pouvait encaisser. La comptabilité
      à jetons illimités joue TOUS les signaux depuis une correction du
      25-08-2026 consignée dans le code : l'ancienne version ne jouait que le
      candidat retenu de chaque jour, soit 85 opérations au lieu de 100. C'était
      une troisième façon de compter, « un achat par jour », que Jean-Luc avait
      abandonnée le 01-08-2026 ; les chiffres de référence avaient été refaits
      ce jour-là, le module non. L'écart a vécu vingt-cinq jours sans que rien
      ne le signale, et c'est la première exécution du juge des stratégies qui l'a
      trouvé. Le choix du signal à jouer quand plusieurs tombent le même jour se
      fait sur l'indice le plus bas, c'est-à-dire la valeur la plus descendue.
      Le code le dit lui-même : ce choix est logique mais n'a pas été validé, et
      la mesure du 01-08-2026 l'a trouvé équivalent au hasard — −9 € par
      opération pour une incertitude de ±957 €.
    ⑨ CE QUI CLOCHE —
      ① L'univers est écrit ici, et ailleurs sous d'autres formes.
        `C5E10_UNIVERS` porte dix noms de sociétés ;
        donnees/cac40_strategies.csv donne à la stratégie en production
        `C5E10-QA-V1` un univers de SIX mnémoniques, `EN,BVI,FGR,RNO,URW,VIE`.
        Relevé le 19-09-2026. Cette fonction rejoue donc dix valeurs quand
        l'état civil de la stratégie n'en déclare que six, et rien ne les
        confronte.
      ② Une valeur absente des données est ignorée sans un mot. La boucle passe
        au suivant dès que le nom n'est pas trouvé. Mesuré le 19-09-2026 sur les
        26 690 lignes de donnees/cours_maitre.csv rangées sous le nom écrit dans
        le fichier : neuf des dix valeurs sont retrouvées, `UNIBAIL_RODAMCO` ne
        l'est pas — le fichier porte `UNIBAIL-RODAMCO-WESTFIELD` et
        `UNIBAIL_RODAMCO_WESTFIELD`, jamais cette orthographe-là. Résultat : 75
        opérations et +83 834,24 €, contre 103 opérations et +109 434,24 € après
        rapprochement des orthographes. Vingt-huit opérations et 25 600 €
        disparus, sans aucune erreur affichée. Une valeur attendue qui ne
        renvoie rien doit être une alerte, jamais un silence.
      ③ La sélection du jour est calculée pour les deux comptabilités mais n'en
        sert qu'une. La liste des candidats retenus est construite avant les
        deux comptages et n'est employée que par celle à un jeton ; la
        comptabilité à jetons illimités reconstruit sa propre liste, triée de la
        même façon. Deux tris identiques écrits deux fois, à quinze lignes
        d'écart.
      ④ Le jeton est libéré par un trade qui n'a jamais été fermé. Quand la vie
        du trade ne peut pas être rejouée jusqu'au bout — données arrêtées avant
        le délai — la fonction passe simplement au signal suivant SANS repousser
        la date de libération du capital. Mesuré le 19-09-2026 sur deux valeurs
        dont les données s'arrêtent cinq séances après le premier signal :
        l'opération du 30 disparaît, et celle du 31, qui tombait pendant que la
        première aurait encore été ouverte, est jouée. La règle d'un seul jeton
        est donc violée en fin d'historique, silencieusement.
      ⑤ Les dates sont comparées comme du texte. Cela fonctionne tant que toutes
        les valeurs écrivent leurs dates dans le même format, année d'abord ; un
        fichier qui écrirait le jour d'abord donnerait un ordre faux sans lever
        la moindre erreur.
    ⑩ EFFET — Aucun. N'écrit rien, ne lit aucun fichier, ne touche pas au
      réseau, et ne modifie pas le dictionnaire qu'elle reçoit.
    ⑪ TERMINAISON — Rend toujours la main. LÈVE `KeyError` ou `TypeError` par
      l'intermédiaire des fonctions de calcul et de sortie qu'elle appelle, si
      une séance ne porte pas ses clés ou porte du texte à la place d'un nombre.
      Aucun de ses appels ne se termine : `signaux_c5etendu10`, `_c5e10_sortie`
      et `_stats` rendent toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS
      jetons illimités : la seconde comptabilité, où toute position s'ouvre sans
        limite ; elle ne correspond à aucun portefeuille réel.
      l'univers : la liste des valeurs sur lesquelles une stratégie a le droit d'acheter, désignées par leur mnémonique
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par
        GitHub Actions — collecte, versement, signaux, positions, mesure,
        surveillance.
      le radar : le programme programmes/audit_ecosysteme.py, lancé chaque soir, qui contrôle l'ensemble du système et range chacun de ses constats sous un numéro de maillon, par exemple 18-Tâches pour le contrôle des traces laissées par les tâches planifiées.
      un jeton : la comptabilité où une seule position peut être ouverte à la fois
        par stratégie ; un signal reçu pendant une position est ignoré.
      un signal : le repérage, sur la dernière séance connue, d'une configuration
        de cours qui déclenche une simulation d'achat.
      un trade : une opération simulée, de l'achat à la revente
      une opération : un achat simulé suivi de sa revente, avec son gain net en
        euros ; aucun ordre réel n'est jamais passé
      une séance : une journée de bourse pour une valeur, avec son ouverture, son
        plus haut, son plus bas, sa clôture et son volume.
    
      PRODUCTION : l etat d une strategie dont le seuil d operations est atteint et les resultats conformes, donc exploitee.
      la boucle : la tache planifiee qui lit les signaux et rend compte
      le jeton : les 100 000 € simules du portefeuille, engages sur une seule position a la fois.
      le signal : le jour où la stratégie dit d'acheter ; l'achat lui-même a lieu à l'ouverture de la séance suivante
      les chiffres figés : les résultats d'un test sur le passé, enregistrés une fois pour toutes, auxquels on compare ce que le système obtient vraiment
      ne s'additionnent jamais : « un jeton » et « jetons illimités »
"""
    # 1. Tous les signaux, par valeur, avec dates
    par_date = {}
    for val in C5E10_UNIVERS:
        ohlcv = donnees.get(val)
        if not ohlcv:
            continue
        for s in signaux_c5etendu10(ohlcv):
            d = ohlcv[s["i"]]["date"]
            par_date.setdefault(d, []).append({"valeur": val, **s})

    dates_signal = sorted(par_date.keys())

    # 2. Sélection : même jour, CCI le plus bas.
    #    Elle ne sert QU'À LA COMPTABILITÉ UN JETON, où il faut bien choisir
    #    puisqu'on ne peut détenir qu'une position. En JETONS ILLIMITÉS aucun
    #    choix n'est nécessaire : tous les signaux se jouent (voir ci-dessous).
    selection = []
    for d in dates_signal:
        cands = sorted(par_date[d], key=lambda x: (x["cci"], x["valeur"]))
        selection.append(cands[0])          # le plus survendu

    # 3. JETONS ILLIMITÉS — TOUS les signaux deviennent un trade.
    #    CORRIGÉ LE 25-08-2026 (A-285). L'ancienne version ne jouait que la
    #    sélection d'un signal par jour, soit 85 opérations : c'était l'hybride
    #    « 1 achat par jour », ABANDONNÉ PAR JEAN-LUC LE 01-08-2026 (A-79) au
    #    profit des JETONS ILLIMITÉS, 100 opérations, tous les signaux joués.
    #    Les chiffres de référence avaient été refaits ce jour-là ; le module,
    #    non. La divergence a vécu 25 jours sans que rien ne la signale, et
    #    c'est la première exécution du juge des stratégies qui l'a trouvée.
    #    Motifs de la décision du 01/08, tels qu'écrits : l'hybride ne mesurait
    #    rien de propre · la règle « CCI le plus bas » a été mesurée équivalente
    #    au hasard (−9 € par trade, incertitude ±957 €), donc filtrer à un par
    #    jour ajoutait du bruit · N ≥ 100 rend accessible la validation stricte.
    tous_signaux = [s for d in dates_signal
                    for s in sorted(par_date[d], key=lambda x: (x["cci"], x["valeur"]))]
    trades_qs = []
    for s in tous_signaux:
        t = _c5e10_sortie(donnees[s["valeur"]], s["i"])
        if t:
            trades_qs.append({"valeur": s["valeur"], "cci": round(s["cci"], 1),
                              "date_signal": donnees[s["valeur"]][s["i"]]["date"], **t})

    # 4. Vraie vie — 1 position à la fois (dates réelles, pas indices)
    trades_vv = []
    date_libre = None                        # première date où le capital est libre
    for s in selection:
        ohlcv = donnees[s["valeur"]]
        d_sig = ohlcv[s["i"]]["date"]
        if date_libre is not None and d_sig < date_libre:
            continue                         # capital occupé → signal ignoré
        t = _c5e10_sortie(ohlcv, s["i"])
        if not t:
            continue
        trades_vv.append({"valeur": s["valeur"], "cci": round(s["cci"], 1),
                          "date_signal": d_sig, **t})
        date_libre = ohlcv[t["i_out"]]["date"]   # libéré à la clôture du trade

    def _stats(trades):
        """Résume une liste d'opérations en trois nombres.

        ① RÔLE — Réduire une liste d'opérations à ce qu'on en retient : combien,
          quelle part de gagnantes, combien d'euros. C'est le seul endroit où ces
          trois nombres sont calculés pour ce module, et les deux comptabilités
          passent toutes deux par lui, ce qui garantit qu'elles se comptent de la
          même façon.
        ② CONTEXTE D'APPEL — Définie à l'intérieur de `backtest_c5etendu10` et
          appelée deux fois par elle, juste avant qu'elle ne rende son résultat :
          une fois sur les opérations de la comptabilité à jetons illimités, une
          fois sur celles de la comptabilité à un jeton. Inaccessible depuis
          l'extérieur du module.
        ③ ENTRÉE — `trades` : la liste des opérations à résumer, chacune portant au
          moins la case `pnl`, le résultat net en euros.
        ④ CONDITIONS D'ENTRÉE — Chaque opération doit porter `pnl`, et cette valeur
          doit être un nombre. Une liste vide est une situation prévue.
        ⑤ SORTIE — UNE valeur : un dictionnaire de trois cases — `n` le nombre
          d'opérations, `wr` la part de gagnantes en pourcent arrondie au dixième,
          `net` le total en euros arrondi au centime. Sur une liste vide, `n` vaut
          0, `net` vaut 0,0 et `wr` vaut `None`.
          [rend: 1]
        ⑥ TRAITEMENT — ① si la liste est vide, rendre les trois valeurs du cas vide
          ·
          ② compter les opérations dont le résultat est strictement positif · ③
            rendre le nombre d'opérations, la part de gagnantes en pourcent et la
            somme des résultats.
        ⑦ UNITÉ — `n` en OPÉRATIONS, `wr` en POURCENTS et non en fraction — 61,0
          veut dire 61,0 % —, `net` en EUROS.
        ⑧ POURQUOI — `wr` vaut `None` et non zéro sur une liste vide, parce qu'une
          part de gagnantes sur zéro opération n'existe pas : écrire 0 ferait lire «
          aucune opération gagnante » là où il faut lire « rien à mesurer ». La
          distinction compte, puisque ces chiffres remontent jusqu'au cockpit. Est
          comptée gagnante une opération dont le résultat est STRICTEMENT positif :
          une opération qui rend exactement zéro n'a rien gagné, et les frais
          rendent cette situation presque impossible de toute façon.
        ⑨ CE QUI CLOCHE —
          ① La part de gagnantes est rendue arrondie au dixième, et c'est un arrondi
            d'AFFICHAGE appliqué à une donnée. Tout calcul ultérieur qui reprendrait
            ce nombre travaillerait sur la valeur arrondie sans le savoir.
          ② Elle ne rend ni le plus grand gain, ni la plus grande perte, ni la plus
            longue série de perdantes, alors que ce sont les chiffres qu'un jugement
            de stratégie réclame. Ils sont recalculés ailleurs, à partir de la liste
            des opérations.
        ⑩ EFFET — Aucun. N'écrit rien, ne lit aucun fichier, ne touche pas au
          réseau, et ne modifie pas la liste qu'elle reçoit.
        ⑪ TERMINAISON — Rend toujours la main. LÈVE `KeyError` sur une opération
          sans `pnl`, et `TypeError` si `pnl` est un texte au lieu d'un nombre.
          Aucun de ses appels ne se termine : elle n'appelle que des fonctions du
          langage.
          [sort: non]
        ⑫ DÉFINITIONS
          jetons illimités : la seconde comptabilité, où toute position s'ouvre sans
            limite ; elle ne correspond à aucun portefeuille réel.
          un jeton : la comptabilité où une seule position peut être ouverte à la fois
            par stratégie ; un signal reçu pendant une position est ignoré.
          un signal : le repérage, sur la dernière séance connue, d'une configuration
            de cours qui déclenche une simulation d'achat.
          une opération : un achat simulé suivi de sa revente, avec son gain net en
            euros ; aucun ordre réel n'est jamais passé
        
          une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
        if not trades:
            return {"n": 0, "wr": None, "net": 0.0}
        gagnants = sum(1 for t in trades if t["pnl"] > 0)
        return {"n": len(trades),
                "wr": round(100 * gagnants / len(trades), 1),
                "net": round(sum(t["pnl"] for t in trades), 2)}

    return {"qualite_signal": {"trades": trades_qs, **_stats(trades_qs)},
            "vraie_vie":      {"trades": trades_vv, **_stats(trades_vv)}}


# ══════════════════════════════════════════════════════════════
# TESTS UNITAIRES DÉTERMINISTES — la preuve de la mécanique
# ══════════════════════════════════════════════════════════════

def _barre(d, o, h, l, c, v=1000):
    """Fabrique une séance de bourse pour la suite des épreuves.

    ① RÔLE — Donner aux épreuves de ce module un moyen d'écrire une séance en
      une ligne, au lieu de recopier six noms de cases à chaque fois. Elle sert
      uniquement à construire des cours inventés pour éprouver la mécanique ;
      aucune séance réelle ne passe par elle.
    ② CONTEXTE D'APPEL — `_serie_signal_a` et la suite des épreuves, dans ce
      fichier, et rien d'autre. Mesuré le 19-09-2026 : une recherche de `_barre`
      dans tous les fichiers Python du dépôt ne la trouve appelée que dans ce
      module.
    ③ ENTRÉE — `d` : la date de la séance, écrite en texte · `o` : le cours
      d'ouverture · `h` : le plus haut · `l` : le plus bas · `c` : le cours de
      clôture · `v` : le volume échangé, 1 000 par défaut.
    ④ CONDITIONS D'ENTRÉE — Aucune. La fonction n'exige rien et ne vérifie rien
      : elle accepte un plus bas supérieur au plus haut, un volume négatif, une
      clôture hors de l'intervalle de la séance.
    ⑤ SORTIE — UNE valeur : un dictionnaire de six cases nommées `date`, `open`,
      `high`, `low`, `close` et `volume`, dans cet ordre.
      [rend: 1]
    ⑥ TRAITEMENT — ① ranger les six valeurs reçues sous les six noms de cases
      attendus par les fonctions de calcul de ce module.
    ⑦ UNITÉ — `o`, `h`, `l` et `c` en EUROS · `v` en TITRES échangés · `d` est
      un texte, jamais une date du langage : les fonctions de ce module ne font
      que comparer ces textes entre eux.
    ⑧ POURQUOI — Les noms de cases sont écrits ICI, et une seule fois. Sans
      cette fonction, les six noms seraient recopiés dans chacune des sept
      épreuves ; le jour où le format d'une séance change, on en corrigerait une
      et six resteraient fausses, sans erreur affichée — deux implémentations
      d'une même chose divergent toujours (R-708). Le volume vaut 1 000 par
      défaut parce que la quasi-totalité des séances construites n'ont pas
      besoin d'un volume particulier ; seules celles qui doivent faire basculer
      le flux monétaire en portent un autre, et l'écart saute alors aux yeux —
      la séance du signal en porte 500 000.
    ⑨ CE QUI CLOCHE —
      ① Les paramètres sont nommés d'une seule lettre. `l` en particulier se
        confond avec le chiffre 1 dans la plupart des polices de caractères, et
        rien dans la signature ne dit lequel de `h` et de `l` est le plus haut.
        Un appel dont deux valeurs seraient interverties construirait une séance
        impossible sans que rien ne le signale.
      ② Elle ne vérifie aucune cohérence. Une séance dont le plus bas dépasse le
        plus haut est acceptée ; les fonctions de calcul en tireraient un flux
        monétaire au signe inversé, sans erreur. La suite des épreuves n'en
        construit aucune aujourd'hui.
      ③ Les six noms de cases qu'elle pose ne sont confrontés à rien. Le dépôt
        tient un fichier qui déclare les champs des fichiers partagés,
        programmes/CONTRATS_DES_FICHIERS.py, et cette fonction ne le consulte
        pas : les noms sont écrits une seconde fois, ici.
    ⑩ EFFET — Aucun. N'écrit rien, ne lit aucun fichier, ne touche pas au
      réseau.
    ⑪ TERMINAISON — Rend toujours la main. Ne lève jamais. Aucun de ses appels
      ne se termine : elle n'appelle rien.
      [sort: non]
    ⑫ DÉFINITIONS
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
      une séance : une journée de bourse pour une valeur, avec son ouverture, son
        plus haut, son plus bas, sa clôture et son volume.
    """
    return {"date": d, "open": o, "high": h, "low": l, "close": c, "volume": v}


def _serie_signal_a(idx_signal, n=60, apres="tp"):
    """Construit des cours inventés où le signal se déclenche à la séance voulue.

    ① RÔLE — Donner au jeu d'épreuves une série de cours dont on connaît
      d'avance la réponse : un signal à un indice choisi, et ensuite une
      trajectoire choisie. Sans elle, éprouver la mécanique exigerait de vrais
      cours, donc des résultats qui changeraient à chaque collecte, et une
      épreuve dont la réponse bouge ne prouve rien.
    ② CONTEXTE D'APPEL — La suite des épreuves de ce fichier, neuf fois, et rien
      d'autre. Mesuré le 19-09-2026 : une recherche de `_serie_signal_a` dans
      tous les fichiers Python du dépôt ne la trouve appelée que dans ce module.
    ③ ENTRÉE — `idx_signal` : l'indice de la séance où le signal doit se
      déclencher · `n` : le nombre total de séances à construire, 60 par défaut
      · `apres` : ce qui doit arriver après le signal, quatre trajectoires
      prévues — « tp » pour une montée qui touche l'objectif, « sl » pour une
      chute qui touche le stop, « flat » pour une stagnation qui va jusqu'au
      bout du délai, et « both » pour une séance qui touche l'objectif ET le
      stop, ce qui éprouve la convention pessimiste ; « tp » par défaut.
    ④ CONDITIONS D'ENTRÉE — `idx_signal` doit laisser au moins quatorze séances
      avant lui pour que la fenêtre de calcul existe, et il doit être plus petit
      que `n`. Mesuré le 19-09-2026, le signal tombe bien à l'indice demandé
      pour les valeurs 14, 15, 16, 20, 30 et 45.
    ⑤ SORTIE — UNE valeur : une liste de `n` séances, chacune construite par
      `_barre`, dont les dates vont de « D000 » à « D0NN » dans l'ordre.
      [rend: 1]
    ⑥ TRAITEMENT — ① partir d'un cours de 100,00 € · ② avant l'indice du signal,
      faire baisser le cours de 0,80 € par séance sur les quinze dernières
      séances et clôturer près du bas, ce qui rend le flux monétaire négatif et
      l'indice très bas ·
      ③ à l'indice du signal, clôturer au plus haut de la séance avec un volume
        de 500 000 contre 1 000 les autres jours, ce qui fait basculer le flux
        au-dessus de zéro pendant que l'indice reste sous −50 · ④ après le
        signal, construire chaque séance à partir de la clôture de la précédente
        selon ce que demande `apres`.
    ⑦ UNITÉ — Les cours en EUROS, les volumes en TITRES, `idx_signal` et `n` en
      SÉANCES. Les dates sont des textes de la forme « D030 », jamais des dates
      du langage : les fonctions de ce module ne font que les comparer entre
      elles, et l'écriture choisie fait que l'ordre alphabétique est l'ordre
      chronologique.
    ⑧ POURQUOI — Le volume de 500 000 contre 1 000 est le levier de toute la
      construction : le flux monétaire pondère chaque séance par son volume,
      donc une seule séance qui pèse cinq cents fois les autres suffit à faire
      basculer la fenêtre entière au-dessus de zéro. C'est ce qui permet de
      placer le signal exactement où on le veut, au lieu de tâtonner. Et la
      baisse ne porte que sur les quinze dernières séances avant le signal,
      jamais sur toute la série : l'indice mesure l'écart du cours à sa moyenne
      des quatorze dernières séances, une baisse ancienne serait déjà dans la
      moyenne et ne ferait pas descendre l'indice.
    ⑨ CE QUI CLOCHE —
      ① Une valeur inconnue de `apres` tombe dans le cas de la stagnation sans
        un mot. Mesuré le 19-09-2026 avec `apres` à « xyz » : la série
        construite est identique à celle de « flat », et l'opération rejouée
        sort par le délai. Une faute de frappe dans le nom d'une trajectoire
        donnerait donc une épreuve verte qui ne teste pas ce qu'elle annonce.
      ② Le nom finit par `_a` alors qu'aucune fonction `_b` n'existe. Mesuré le
        19-09-2026, ce module ne contient qu'une seule fabrique de série. La
        lettre promet une famille qui n'est pas là, et un lecteur cherche la
        variante.
      ③ Les cours produits sont construits pour satisfaire le calcul, pas pour
        ressembler à un marché. Une séance à 500 000 titres au milieu de séances
        à 1 000 n'arrive pas en bourse. Les épreuves prouvent donc que la
        mécanique fait ce qu'elle annonce, jamais que la stratégie se comporte
        comme cela sur des cours réels — ce qui est le travail du juge des stratégies,
        et non le sien.
      ④ Le nombre 0,80 € de baisse par séance, le 500 000 de volume et le 15 de
        longueur de la baisse sont écrits dans le code sans nom. Un lecteur qui
        voudrait déplacer le signal ou le rendre plus faible ne sait pas lequel
        de ces trois nombres toucher.
    ⑩ EFFET — Aucun. N'écrit rien, ne lit aucun fichier, ne touche pas au
      réseau. La sixième épreuve du module, elle, MODIFIE en place la liste que
      cette fonction lui a rendue, pour fabriquer une seconde valeur dont
      l'indice est moins bas.
    ⑪ TERMINAISON — Rend toujours la main. Ne lève jamais sur les valeurs que le
      jeu d'épreuves lui passe. Aucun de ses appels ne se termine : `_barre`
      rend toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS
      un signal : le repérage, sur la dernière séance connue, d'une configuration
        de cours qui déclenche une simulation d'achat.
      une séance : une journée de bourse pour une valeur, avec son ouverture, son
        plus haut, son plus bas, sa clôture et son volume.
    
      la convention : le prix de sortie théorique, celui de l'objectif ou du stop, par opposition au prix réellement observé. C'est ce qui permet de comparer une opération vécue à un test sur le passé
      le signal : le jour où la stratégie dit d'acheter ; l'achat lui-même a lieu à l'ouverture de la séance suivante
"""
    bars = []
    px = 100.0
    for i in range(n):
        if i < idx_signal:
            px = px - 0.8 if i > idx_signal - 16 else px   # chute récente → CCI bas
            bars.append(_barre(f"D{i:03d}", px + 0.3, px + 0.5, px - 0.5, px - 0.4, 1000))
        elif i == idx_signal:
            # clôture au plus haut, volume énorme → CMF de la fenêtre bascule positif
            bars.append(_barre(f"D{i:03d}", px - 0.3, px + 0.2, px - 0.5, px + 0.2, 500_000))
        else:
            o = bars[-1]["close"]
            if apres == "tp":
                bars.append(_barre(f"D{i:03d}", o, o * 1.06, o * 0.999, o * 1.05, 1000))
            elif apres == "sl":
                bars.append(_barre(f"D{i:03d}", o, o * 1.001, o * 0.95, o * 0.96, 1000))
            elif apres == "both":
                bars.append(_barre(f"D{i:03d}", o, o * 1.08, o * 0.90, o, 1000))
            else:
                bars.append(_barre(f"D{i:03d}", o, o * 1.002, o * 0.998, o, 1000))
    return bars


def _tests():
    """Lance les sept épreuves de la mécanique et affiche leur résultat.

    ① RÔLE — Prouver que la mécanique de ce module fait ce qu'elle annonce, sur
      des cours construits dont on connaît la réponse d'avance. C'est ce qui
      permet de rejouer la stratégie des mois plus tard et de savoir que le
      calcul n'a pas bougé : les sept épreuves portent sur la détection du
      signal, sur les trois façons de sortir d'une position, sur la convention
      pessimiste, sur le choix entre plusieurs signaux du même jour, et sur la
      règle d'une seule position à la fois.
    ② CONTEXTE D'APPEL — Le lancement direct du fichier, et lui seul. AUCUN
      LANCEUR AUTOMATIQUE : mesuré le 19-09-2026, une recherche du nom de ce
      module dans les deux fichiers de tâches planifiées du dépôt,
      `.github/workflows/collecte_abc.yml` et
      `.github/workflows/comparer_google_abc.yml`, ne rend aucune ligne qui
      l'exécute directement ; le circuit du soir le CHARGE pour appeler ses
      fonctions, ce qui ne déclenche pas les épreuves.
    ③ ENTRÉE — Aucun paramètre, aucune ligne de commande, aucun fichier. Les
      cours sont construits par `_serie_signal_a`.
    ④ CONDITIONS D'ENTRÉE — Le module doit avoir pu se charger, donc
      `MODULE_POSITIONS.py` doit être dans le même dossier, puisque le taux de
      frais y est lu au chargement.
    ⑤ SORTIE — Ne rend rien. Tout passe par l'affichage : une seule ligne, de la
      forme « ✅ 7/7 tests unitaires PASSÉS — mécanique C5-ETENDU-10 prouvée »,
      mesurée le 19-09-2026.
      [rend: rien]
    ⑥ TRAITEMENT — ① T1, le signal est détecté à l'indice voulu et l'indice y
      est bien sous −50 · ② T2, une sortie à l'objectif rend exactement 4 % du
      capital moins 300 € de frais · ③ T3, une sortie au stop rend exactement
      −2,5 % moins 300 € ·
      ④ T4, une séance qui touche l'objectif ET le stop est comptée au stop · ⑤
        T5, une stagnation sort au délai, exactement vingt séances après
        l'entrée · ⑥ T6, quand deux valeurs donnent un signal le même jour,
        celle dont l'indice est le plus bas est retenue · ⑦ T7, un signal reçu
        pendant qu'une position est ouverte est joué en jetons illimités et
        ignoré en un jeton · ⑧ afficher le compte.
    ⑦ UNITÉ — Le compte affiché est un NOMBRE D'ÉPREUVES. Les montants vérifiés
      sont en EUROS, le délai en SÉANCES DE BOURSE.
    ⑧ POURQUOI — Ces épreuves existent parce que le code d'origine de cette
      stratégie a été PERDU. Ses résultats n'étaient plus reproductibles et deux
      résultats nets contradictoires circulaient sans qu'aucun ne puisse être
      refait. Le module a été réécrit le 11-07-2026 d'après les paramètres
      consignés ; les épreuves sont ce qui permet de dire que la réécriture fait
      bien ce que les paramètres décrivent. Et elles portent sur des cours
      CONSTRUITS et non sur les vrais cours, parce qu'une épreuve dont la
      réponse change à chaque collecte ne prouve rien. Juger la stratégie sur
      les vraies données est un autre travail, celui du juge des stratégies.
    ⑨ CE QUI CLOCHE —
      ① La suite des épreuves reste verte quand on lui retire une épreuve. Le
        nombre 7 est écrit en dur dans le message affiché au lieu d'être compté,
        et rien ne compare le nombre d'épreuves passées au nombre d'épreuves
        attendues. Mesuré le 19-09-2026 sur une copie dont la septième épreuve a
        été supprimée : l'affichage est « ✅ 6/7 tests unitaires PASSÉS —
        mécanique C5-ETENDU-10 prouvée », et le code de sortie relevé juste
        après est 0. Le mot « prouvée » et la coche verte s'affichent sur une
        preuve amputée. Une épreuve qui reste verte quand on retire ce qu'elle
        teste n'est pas une preuve.
      ② Les montants attendus des deuxième et troisième épreuves recopient le
        montant des frais. Le nombre 300 est écrit en dur dans les deux, alors
        que ce montant se déduit de `C5E10_FRAIS` et de `C5E10_CAPITAL`,
        lesquels sont lus chez leur propriétaire précisément pour ne pas être
        recopiés. Un changement de tarif du courtier ferait échouer ces deux
        épreuves pour une raison qui n'est pas une faute de calcul.
      ③ Aucune épreuve ne porte sur les situations d'échec. Rien n'éprouve une
        histoire trop courte, une séance manquante, une valeur absente des
        données, ni un signal en fin d'historique dont la position n'a pas pu
        être fermée — c'est-à-dire exactement les cas où les défauts consignés
        de ce module se produisent.
      ④ Les deux dernières épreuves dépendent de l'ordre dans lequel les
        opérations sont rangées, et non seulement du résultat. La sixième lit la
        PREMIÈRE opération de la liste rendue en jetons illimités pour vérifier
        quel signal a été retenu, alors que cette comptabilité joue tous les
        signaux et que l'ordre de la liste ne fait partie d'aucune promesse
        écrite.
    ⑩ EFFET — AFFICHE une ligne. N'écrit aucun fichier, ne lit aucun fichier, ne
      touche pas au réseau.
    ⑪ TERMINAISON — Rend la main après avoir affiché sa ligne, ce que le
      lancement du fichier traduit en code de sortie 0 — mesuré le 19-09-2026.
      LÈVE `AssertionError` à la première épreuve fausse, ce qui arrête le
      programme avec le code 1 et laisse les épreuves suivantes non exécutées.
      Et un de ses appels peut ne pas revenir : `_c5e10_sortie` peut rendre
      `None`, et la lecture d'une case sur `None` lève alors `TypeError` au lieu
      de l'`AssertionError` attendue.
      [sort: non]
    ⑫ DÉFINITIONS
      jetons illimités : la seconde comptabilité, où toute position s'ouvre sans
        limite ; elle ne correspond à aucun portefeuille réel.
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par
        GitHub Actions — collecte, versement, signaux, positions, mesure,
        surveillance.
      un jeton : la comptabilité où une seule position peut être ouverte à la fois
        par stratégie ; un signal reçu pendant une position est ignoré.
      un signal : le repérage, sur la dernière séance connue, d'une configuration
        de cours qui déclenche une simulation d'achat.
      une séance : une journée de bourse pour une valeur, avec son ouverture, son
        plus haut, son plus bas, sa clôture et son volume.
    
      C5-ETENDU-10 : le nom de la stratégie vivante ; ses seuils et son horizon sont lus dans `donnees/cac40_strategies.csv`.
      la convention : le prix de sortie théorique, celui de l'objectif ou du stop, par opposition au prix réellement observé. C'est ce qui permet de comparer une opération vécue à un test sur le passé
      le signal : le jour où la stratégie dit d'acheter ; l'achat lui-même a lieu à l'ouverture de la séance suivante
"""
    ok = 0

    # T1 — le signal est détecté au bon indice, et nulle part ailleurs après
    serie = _serie_signal_a(30, apres="flat")
    sigs = signaux_c5etendu10(serie)
    assert any(s["i"] == 30 for s in sigs), f"T1: signal attendu à 30, trouvé {[s['i'] for s in sigs]}"
    s30 = [s for s in sigs if s["i"] == 30][0]
    assert s30["cci"] < -50, f"T1: CCI={s30['cci']} devrait être < -50"
    ok += 1

    # T2 — sortie TP : prix de sortie = entrée × 1.04, PnL = 4% - frais
    serie = _serie_signal_a(30, apres="tp")
    t = _c5e10_sortie(serie, 30)
    assert t["motif"] == "TP", f"T2: motif={t['motif']}"
    attendu = C5E10_CAPITAL * C5E10_TP - 300
    assert abs(t["pnl"] - attendu) < 0.01, f"T2: pnl={t['pnl']} vs {attendu}"
    ok += 1

    # T3 — sortie SL : PnL = -2.5% - frais
    serie = _serie_signal_a(30, apres="sl")
    t = _c5e10_sortie(serie, 30)
    assert t["motif"] == "SL", f"T3: motif={t['motif']}"
    attendu = -C5E10_CAPITAL * C5E10_SL - 300
    assert abs(t["pnl"] - attendu) < 0.01, f"T3: pnl={t['pnl']} vs {attendu}"
    ok += 1

    # T4 — CONVENTION PESSIMISTE : TP et SL touchés le même jour → SL
    serie = _serie_signal_a(30, apres="both")
    t = _c5e10_sortie(serie, 30)
    assert t["motif"] == "SL", f"T4: pessimiste violée, motif={t['motif']}"
    ok += 1

    # T5 — sortie HORIZON : exactement 20 séances après l'entrée, au close
    serie = _serie_signal_a(30, apres="flat")
    t = _c5e10_sortie(serie, 30)
    assert t["motif"] == "HORIZON" and t["i_out"] == 31 + 20, f"T5: {t}"
    ok += 1

    # T6 — sélection multi-signaux : CCI le plus bas gagne
    sA = _serie_signal_a(30, apres="flat")            # CCI bas
    sB = _serie_signal_a(30, apres="flat")
    for k, b in enumerate(sB[20:30]):                 # remontée progressive → pente
        for cle in ("open", "high", "low", "close"):  # moins descendante → CCI moins bas
            b[cle] += (k + 1) * 0.35
    donnees = {"TOTALENERGIES": sA, "ENGIE": sB}
    cciA = [s for s in signaux_c5etendu10(sA) if s["i"] == 30][0]["cci"]
    cciB = [s for s in signaux_c5etendu10(sB) if s["i"] == 30][0]["cci"]
    r = backtest_c5etendu10(donnees)
    gagnant = "TOTALENERGIES" if cciA < cciB else "ENGIE"
    assert r["qualite_signal"]["trades"][0]["valeur"] == gagnant, \
        f"T6: retenu={r['qualite_signal']['trades'][0]['valeur']}, attendu={gagnant}"
    ok += 1

    # T7 — vraie vie : signal pendant position ouverte → ignoré
    sA = _serie_signal_a(30, apres="flat")            # position 20 j (D031→D051)
    sB = _serie_signal_a(40, apres="tp")              # signal D040, pendant la position
    donnees = {"TOTALENERGIES": sA, "ENGIE": sB}
    r = backtest_c5etendu10(donnees)
    assert r["qualite_signal"]["n"] == 2, f"T7a: QS n={r['qualite_signal']['n']}"
    assert r["vraie_vie"]["n"] == 1, f"T7b: VV n={r['vraie_vie']['n']} (signal D040 aurait dû être ignoré)"
    ok += 1

    print(f"✅ {ok}/7 tests unitaires PASSÉS — mécanique C5-ETENDU-10 prouvée")


if __name__ == "__main__":
    _tests()
