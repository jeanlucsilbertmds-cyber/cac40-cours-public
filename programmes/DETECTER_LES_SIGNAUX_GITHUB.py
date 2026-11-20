#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DETECTER_LES_SIGNAUX_GITHUB.py — Ven 11-09-2026 (Paris)
FABRIQUÉ · Rôle : sur une machine GitHub Actions, juste après la collecte, calculer
les signaux C5-ETENDU-10 sur la dernière séance et publier un fichier MINUSCULE que
la conversation avec Claude lira — quelques lignes au lieu d'un mégaoctet et demi.

POURQUOI, ET C'EST UNE DÉCISION D'ARCHITECTURE (Jean-Luc, 11-09-2026) :
  Jusqu'ici la conversation avec Claude transportait 1,4 Mo de cours chaque soir pour en tirer trois
  lignes de conclusion. Ce transport a cassé deux fois en deux jours — par git
  (github.com retiré de la liste de sortie des tâches, 11-09) puis par l'outil web
  (troncature mesurée à ~49 Ko sur un fichier de 73 904 : il a rendu 51 006 octets
  et coupé au milieu d'un nombre, sans le dire).
  Réduire le fichier pour passer sous la limite serait une combine : elle tiendrait
  jusqu'au jour où le fichier regrossit, et casserait en silence.
  LA RÉPONSE PROPRE : le calcul va où sont les données. GitHub a les cours, le
  réseau et les programmes. Il calcule. La conversation reçoit un RÉSULTAT et fait ce
  qu'elle seule peut faire — tenir les positions et écrire au projet.
  C'est le principe déjà retenu pour les autres maillons (A-395) : le calcul va où sont les données.

CE QUE CE PROGRAMME NE RÉÉCRIT PAS — deux implémentations d'une même chose divergent toujours (R-708) : ni la lecture des cours, ni le
calcul du signal, ni les règles de la composition et des trous. Il importe
`JUGE_DES_STRATEGIES.lire_par_le_lecteur` (depuis le 29-10-2026, A-577 étape 7 ;
jusque-là `charger_cours`), `couper_aux_trous`, `dans_l_indice`, `porte_0` et, depuis le
10-11-2026 (plan V7, bloc 9a), `signal_de_la_fiche` et `mnemoniques_de_l_univers` : LE SIGNAL
ET L'UNIVERS SE LISENT DANS LES FICHES SUIVIES du registre des stratégies, jamais dans ce
code. Pour C5, la fiche nomme `MODULE_C5_ETENDU_10.signaux_c5etendu10` — le code éprouvé,
celui qui a reproduit au chiffre près le signal connu UNIBAIL du 20-08.
LA GARDE DU SOIR (A-678) : une fiche suivie que le juge refuse n'est pas suivie, et c'est dit.
PLUSIEURS MODULES DE SIGNAL (A-925, décision de Jean-Luc du 19-11-2026 à 19h23) : les fiches sont rangées par signal
déclaré ; chaque groupe se calibre sur l'étalon de SON module et calcule SES signaux, chaque signal écrit avec les fiches
qui le reçoivent ; un groupe qui ne se charge pas, ne se calibre pas ou dont le calcul tombe est MIS À PART, ses fiches
nommées au fichier, sans empêcher les autres.

LE SIGNAL DU SOIR EST CELUI QUE LE JUGE A JUGÉ (A-577, étape 7 ; décision de Jean-Luc du
26-10-2026 à 19h43 : « n'oublie pas de le basculer plus tard, sinon on va se casser les
dents [...] il faut que ce soit fait rapidement »). Les cours passent par le lecteur
unique, avec ses refus ; un signal ne se donne que pour une valeur dans le CAC 40 le jour
du signal ; et il se calcule sur le morceau de série qui finit à la séance, jamais à
travers un trou. Exemple mesuré (fiche de `programmes/LIRE_LES_COURS.py`) : le CMF de
Vinci passe de −0,136 à −0,087 quand la séance du 03-07-2026 manque.

CALIBRAGE OBLIGATOIRE AVANT DE CONCLURE — reproduire un résultat connu avant d'en produire un nouveau (R-720) : le
programme reproduit d'abord un signal CONNU. S'il ne le retrouve pas, il ÉCHOUE et
ne publie rien — un « aucun signal » non calibré ne vaut rien.

════════════════════════════════════════════════════════════════════════
LES ONZE ÉLÉMENTS — ce programme est une fonction comme les autres
════════════════════════════════════════════════════════════════════════
① RÔLE — **LE PAS N°5 DU CIRCUIT DU SOIR**, entre le contrôle des cours et la
  tenue des positions. **Il décide ce qui sera proposé à l achat demain.**
② CONTEXTE D APPEL — Le circuit du soir, après la clôture, sur une machine
  GitHub Actions. **Un signal n est jamais connu avant la clôture.**
③ ENTRÉE — La ligne de commande : la racine du dépôt. **Et les fichiers de
  cours, choisis par le juge des stratégies et non par ce programme**, lus par le
  lecteur unique `programmes/LIRE_LES_COURS.py` depuis le 29-10-2026.
④ CONDITIONS D ENTRÉE — Le juge des stratégies `programmes/JUGE_DES_STRATEGIES.py` et le module
  de signal doivent être là, et au
  moins un fichier de cours, et ce que lit le lecteur unique (le référentiel, le
  calendrier officiel, la nature des trous, les passages dans le CAC 40). Tout le reste
  est un cas prévu.
⑤ SORTIE — **Un code de sortie, et un fichier de quelques centaines d octets** ; quand la garde
  du soir mord, une ligne `garde=<verdict>` dans le fichier nommé par `GITHUB_OUTPUT`.
⑥ TRAITEMENT — ① charger juge des stratégies, module et cours, ces derniers par le
  lecteur unique · ② **CALIBRER chaque module sur un signal
  CONNU ; mettre à part les fiches d un module qui ne se calibre pas, s arrêter si aucun ne se calibre** · ③ trouver
  la dernière séance · ④ relever les signaux de cette séance, groupe par groupe et valeur par valeur, sur le morceau
  sans trou qui finit à la séance, et refuser ceux d une valeur hors du CAC 40 ce jour-là · ⑤ confronter au
  CONTRAT · ⑥ écrire.
⑦ UNITÉ — **Le CMF — flux monétaire de Chaikin — mesure si l'argent entre ou
  sort d'une valeur ; c'est un rapport sans unité, borné à ±1.** **Le CCI —
  indice du canal des matières premières — mesure de combien le cours s'écarte de
  sa moyenne récente ; c'est un indice sans unité, typiquement entre −200 et
  +200.** La clôture est en euros.
⑧ POURQUOI — **Trois raisons, et chacune vient d'un fait mesuré.**
  **① LE CALCUL VA OÙ SONT LES DONNÉES.** Jusqu'au 11-09-2026, les 1,4 Mo de
  cours étaient transportés chaque soir jusqu'à la conversation pour en tirer
  trois lignes. Ce transport a cassé deux fois en deux jours. **GitHub a les
  cours, le réseau et les programmes : il calcule, et n'envoie que le résultat.**
  **② RIEN N'EST RÉÉCRIT DE CE QUI EXISTE** : ce programme importe la lecture
  des cours et le calcul du signal au lieu de les refaire — deux implémentations
  d'une même chose divergent toujours (R-708). Depuis le 29-10-2026, il lit comme le
  juge des stratégies : un signal du soir calculé à travers un trou, ou sur une valeur
  hors du CAC 40, ne serait plus celui que le juge a jugé.
  **③ LE CALIBRAGE PRÉCÈDE TOUTE CONCLUSION** : il reproduit d'abord un signal
  CONNU, et ne publie rien s'il ne le retrouve pas.
⑨ CE QUI CLOCHE — **Trois silences, aucun corrigé** — le ⑨ se consigne et ne se corrige pas (R-752) ;
  et, depuis le 10-11-2026, les limites de la garde écrites au ⑨ de `fiches_du_soir` :
  · l étalon du calibrage est figé dans le programme — si sa séance disparaissait
    des cours, le message dirait « signal connu non retrouvé », **ce qui se lit
    comme un défaut du détecteur et non comme une donnée manquante** ;
  · `charger` empile un chemin de recherche sans vérifier s il y est déjà ;
  · **l univers est lu dans les fiches au chargement du programme** : une valeur ajoutée
    au registre ou au référentiel pendant l exécution ne serait pas vue.
⑩ EFFET — **ÉCRIT `donnees/signaux_du_jour.json` EN ENTIER à chaque exécution**,
  y compris la ligne `calcule_le`. **Relancer hors du circuit écrase cette
  trace : une heure de midi sur une séance close la veille rend la preuve
  inutilisable.** Modifie aussi le chemin de recherche des modules.
⑪ TERMINAISON — **NE REND JAMAIS LA MAIN : quatre codes.** `0` publié — Y COMPRIS QUAND DES FICHES
  SONT MISES À PART (19-11-2026, A-925) ET QUAND LA GARDE DU SOIR MORD (11-11-2026, A-706) : la séance est publiée avec `signaux: []` et le champ
  `garde_du_soir`, et la ligne `garde=<verdict>` est écrite dans la sortie du pas ; c est un pas
  de fin du circuit qui rougit ou avertit · `1` aucun module calibré, rien publié · `2` sources ou
  séance absentes, lecture des cours refusée par le lecteur unique (29-10-2026), ou sortie du
  pas impossible à écrire · `3` le fichier ne respecte pas le format déclaré dans
  `programmes/CONTRATS_DES_FICHIERS.py`, rien écrit. **Le circuit du soir n a pas
  de tolérance sur ce pas : un code non nul — une vraie panne — arrête la chaîne.**

USAGE : python3 DETECTER_LES_SIGNAUX_GITHUB.py <racine_du_depot>
SORTIE : donnees/signaux_du_jour.json  (quelques centaines d'octets)
CODE : 0 = calculé et publié (fiches mises à part comprises), ou garde du soir publiée (signaux vides, champ
       garde_du_soir, sortie de pas garde=aucune_vivante|refus_total) · 1 = aucun module calibré, rien
       publié · 2 = sources absentes, lecture refusée ou sortie de pas impossible · 3 = contrat

⑫ DÉFINITIONS —
  le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
  CMF : le flux monétaire de Chaikin, qui mesure si l'argent entre ou sort d'une valeur ; sans unité, borné à ±1.
  CCI : l'indice du canal des matières premières, qui mesure de combien le cours
    s'écarte de sa moyenne récente ; sans unité, typiquement entre −200 et +200.
  C5-ETENDU-10 : le nom de la stratégie vivante ; ses seuils et son horizon sont
    lus dans `donnees/cac40_strategies.csv`.
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub
    Actions — collecte, versement, signaux, positions, mesure, surveillance.
  l'outil web : l'outil d'une tâche planifiée Cowork qui ouvre une page et en rend un texte écrit par un modèle, jamais la page elle-même.
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
  le CCI : un indicateur de bourse qui mesure de combien le prix s'écarte de sa moyenne des quatorze dernières séances.
  le CMF : un indicateur de bourse qui mesure si l'argent entre ou sort d'une valeur sur les quatorze dernières séances.
  le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
  le signal : le jour où la stratégie dit d'acheter ; l'achat lui-même a lieu à l'ouverture de la séance suivante
  un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré rejoué à l'identique pour vérifier qu'il n'est pas revenu.
  un signal : le repérage, sur la dernière séance connue, d'une configuration de cours qui déclenche une simulation d'achat.
  une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
"""

import json, os, sys
from datetime import datetime
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")

# L'ÉTALON DE CHAQUE MODULE DE SIGNAL, rangé sous « <module_signal> · <fonction_signal> » tels que la fiche les écrit
# (le chemin du module et le nom de sa fonction, sans les réglages : depuis le 19-11-2026, A-925, le calibrage se fait
# PAR MODULE, et un module se calibre sur SES réglages d'étalon, écrits ici avec le signal connu). « nom » est
# l'étiquette écrite dans la case `strategie` du fichier des signaux (C5 : « C5-ETENDU-10 », inchangée depuis le 11-09).
# Un module dont la clé est absente de cette table ne se calibre pas : ses fiches sont MISES À PART et nommées, les
# autres tournent ; si AUCUN module ne se calibre, rien n'est publié (code 1).
#   C5 : dernier trade réel, reproduit au chiffre près par Cowork le 10-09 à 20h34 — CMF +0.0018, CCI -62.5.
#   RSI REBOND : le signal donné en exemple réel au ⑤ de `signaux_rsi_rebond` (programmes/MODULE_SIGNAL_RSI_REBOND.py,
#     écrit et mesuré le 11-11-2026 sur le cours maître, relu par un relecteur neuf le même jour) : VINCI, RSI(14)
#     29,776 le 07-04-2025 puis 37,820 le 08-04-2025 → signal le 08-04-2025 (rang 324 depuis le 2024-01-02).
ETALONS = {
    "programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py · signaux_c5etendu10":
        {"nom": "C5-ETENDU-10", "valeur": "UNIBAIL_RODAMCO", "date": "2026-08-20", "reglages": {}},
    "programmes/MODULE_SIGNAL_RSI_REBOND.py · signaux_rsi_rebond":
        {"nom": "RSI-REBOND", "valeur": "VINCI", "date": "2025-04-08",
         "reglages": {"periode": 14, "seuil": 30, "chauffe": 100}},
}

# LES INDICATEURS DU DÉTAIL ET DU DÉPARTAGE — CMF(14) et CCI(14) — se calculent par UN module, toujours le même, quel
# que soit le signal de la fiche : celui de C5, qui a produit le golden et dont le départage R-207bis (« le CCI le plus
# bas ») a été mesuré (BACKLOG A-800, décision de Jean-Luc du 15-11-2026 à 12h17 : « 1 oui » — la même règle partout).
INDICATEURS_DU_DETAIL = "programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py"


def cle_d_etalon(signal):
    """Rend la clé sous laquelle `ETALONS` range l'étalon du module d'un signal : « <chemin du module> · <fonction> ».

    ① RÔLE — Dire, pour un signal lu dans une fiche, sous quel nom chercher son signal connu (A-925 : un étalon PAR
      MODULE, et non plus par déclaration complète, réglages compris).
    ② CONTEXTE D'APPEL — `fiches_du_soir`, une fois par fiche retenue, pour la ranger dans son groupe ; `main`, pour
      calibrer chaque groupe.
    ③ ENTRÉE — `signal` : un `SignalNomme` du juge (rendu par `fiche_suivie`, donc par `signal_de_la_fiche`), qui porte
      `chemin` (la case `module_signal` de la fiche, telle qu'écrite) et `fonction` (la fonction chargée).
    ④ CONDITIONS D'ENTRÉE — `signal.fonction` a un `__name__` (une fonction Python).
    ⑤ SORTIE — UNE valeur : un texte. Exemple réel : la fiche C5E10-OBS-V1 →
      « programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py · signaux_c5etendu10 ».
      [rend: 1]
    ⑥ TRAITEMENT — joindre le chemin et le nom de la fonction par « · ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Jusqu'au 19-11-2026, l'étalon était rangé sous la déclaration ENTIÈRE (« … · réglages aucun ») : une
      fiche du même module avec des réglages, ou un second module, n'avait aucun étalon et le soir s'arrêtait (inventaire
      du 19-11-2026, A-925 : « CALIBRAGE IMPOSSIBLE : aucun signal connu pour… MODULE_SIGNAL_RSI_REBOND »).
    ⑨ CE QUI CLOCHE — Le chemin est pris tel que la fiche l'écrit : « ./programmes/… » ou une autre graphie du même
      fichier n'aurait pas d'étalon (la fiche est alors mise à part, nommée — pas de faux étalon en silence).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; aucun de ses appels ne peut ne pas revenir.
      [sort: non]
    """
    return "%s · %s" % (signal.chemin, getattr(signal.fonction, "__name__", "?"))


class GroupeDuSoir:
    """Les fiches suivies le soir qui déclarent LE MÊME signal (module, fonction et réglages) : un calcul pour toutes.

    ① RÔLE — Porter un signal, les fiches qui le déclarent et la réunion de leurs univers, pour que le soir calcule les
      signaux FICHE PAR FICHE sans refaire le même calcul pour deux fiches au même signal (A-925, 19-11-2026).
    ② CONTEXTE D'APPEL — Construit par `fiches_du_soir` ; lu par `main` (calibrage du groupe) et par
      `signaux_de_la_seance` (calcul du groupe).
    ③ ENTRÉE — `signal` : un `SignalNomme` du juge · `fiches` : liste de couples (identifiant, liste des noms de valeurs
      de son univers), dans l'ordre « plus grand univers d'abord, puis l'ordre du registre ».
    ④ CONDITIONS D'ENTRÉE — `fiches` non vide.
    ⑤ SORTIE — Un objet ; aucune valeur rendue par lui-même.
      [rend: rien]
    ⑥ TRAITEMENT — Ranger ; l'univers est la réunion des univers des fiches, chaque valeur à sa première apparition.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le fichier des signaux dit, pour chaque signal, QUELLES FICHES le reçoivent (`fiches`) : le teneur de
      positions ne l'attribue qu'à elles, et non à toute fiche dont l'univers contient la valeur (la raison écrite au
      ⑧ de `fiches_du_soir` jusqu'au 19-11-2026 pour refuser un second signal).
    ⑨ CE QUI CLOCHE — Deux fiches au même module mais aux réglages écrits différemment (« {"seuil": 30} » et
      « {"seuil":30} ») font deux groupes : deux calculs identiques, sans erreur.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """

    def __init__(self, signal, fiches):
        """Range le signal et les fiches ; calcule l'univers du groupe.

        ① RÔLE — Construire le groupe.
        ② CONTEXTE D'APPEL — `fiches_du_soir`, une fois par signal distinct.
        ③ ENTRÉE — `self` : l'objet en construction · `signal`, `fiches` : voir ③ de la classe.
        ④ CONDITIONS D'ENTRÉE — voir ④ de la classe.
        ⑤ SORTIE — Aucune valeur (constructeur).
          [rend: rien]
        ⑥ TRAITEMENT — Ranger ; `univers` = réunion ordonnée ; `etalon` vide (posé par `main` au calibrage).
        ⑦ UNITÉ — —
        ⑧ POURQUOI — voir ⑧ de la classe.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun hors de l'objet.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        self.signal, self.fiches = signal, [(i, list(u)) for i, u in fiches]
        self.univers = []
        for _i, u in self.fiches:
            for v in u:
                if v not in self.univers:
                    self.univers.append(v)
        self.etalon, self.calibrage = None, None

    def fiches_de(self, valeur):
        """Rend les identifiants des fiches du groupe dont l'univers porte la valeur.

        ① RÔLE — Dire à quelles fiches va un signal du groupe.
        ② CONTEXTE D'APPEL — `signaux_de_la_seance`, une fois par signal donné ou refusé.
        ③ ENTRÉE — `self` : le groupe · `valeur` : un nom de valeur (clé des cours, comme dans l'univers).
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : la liste des identifiants, dans l'ordre du groupe. Exemple réel : VEOLIA, groupe C5 du
          19-11-2026 → ["C5E10-OBS-V1", "C5E10-QA-V1"] ; TOTALENERGIES → ["C5E10-OBS-V1"].
          [rend: 1]
        ⑥ TRAITEMENT — filtrer les fiches.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — voir ⑧ de la classe.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        return [i for i, u in self.fiches if valeur in u]


class SuiviDuSoir:
    """Ce que le soir suit, lu dans les fiches : les groupes de signal, l'univers, les fiches retenues et mises à part.

    ① RÔLE — Porter en un seul objet ce que `fiches_du_soir` a lu dans les fiches, et s'appeler comme un signal (celui
      du premier groupe, pour les appelants qui n'en connaissent qu'un).
    ② CONTEXTE D'APPEL — Construit par `fiches_du_soir` ; rendu par `charger` (deuxième valeur), puis passé à
      `signaux_sur` et `signaux_de_la_seance` sous le nom `mod`.
    ③ ENTRÉE — `groupes` : liste de `GroupeDuSoir` (vide quand `garde` est donnée) · `refusees` : liste de
      (identifiant, motif) des fiches que la garde refuse · `garde` : None, ou la garde du soir (voir `fiches_du_soir`).
    ④ CONDITIONS D'ENTRÉE — Chaque groupe porte un signal appelable.
    ⑤ SORTIE — L'appel rend UNE valeur : ce que rend le signal du premier groupe sur la série (liste des {"i", …}).
      [rend: 1]
    ⑥ TRAITEMENT — Ranger ; `signal`, `module`, `univers` et `fiches` se déduisent des groupes restants
      (`retirer`) ; à l'appel, déléguer au signal du premier groupe.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les épreuves du 29-10-2026 (`tests/EPREUVES_DU_CIRCUIT_PAR_LE_LECTEUR_Jeu_29-10-2026.py`) et du
      départage (`tests/EPREUVES_DU_DEPARTAGE_R207BIS_Sam_14-11-2026.py`) appellent `charger` puis
      `signaux_de_la_seance(cours, lecture, B, mod, séance)` : en gardant cette forme, elles éprouvent le chemin des
      fiches sans être réécrites. PLUSIEURS GROUPES depuis le 19-11-2026 (A-925).
    ⑨ CE QUI CLOCHE — `mises_a_part` grandit pendant le soir (calibrage, calcul) : l'objet change après sa construction.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; l'appel lève ce que lève le signal.
      [sort: non]
    """

    def __init__(self, groupes, refusees, garde=None):
        """Range les groupes, les refus et la garde ; déduit signal, module, univers et fiches.

        ① RÔLE — Construire l'objet.
        ② CONTEXTE D'APPEL — `fiches_du_soir`.
        ③ ENTRÉE — `self` : l'objet en construction · `groupes`, `refusees`, `garde` : voir ③ de la classe.
        ④ CONDITIONS D'ENTRÉE — voir ④ de la classe.
        ⑤ SORTIE — Aucune valeur (constructeur).
          [rend: rien]
        ⑥ TRAITEMENT — Ranger ; `mises_a_part` commence par les refus de la garde ; `indicateurs` est posé par
          `charger` (le module des indicateurs du détail, `INDICATEURS_DU_DETAIL`) ; puis `_deduire`.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — voir ⑧ de la classe.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun hors de l'objet.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        self.groupes, self.refusees, self.garde = list(groupes), list(refusees), garde
        self.mises_a_part = list(refusees)
        self.indicateurs = None
        self._deduire()

    def _deduire(self):
        """Recalcule le signal, le module, l'univers et les fiches à partir des groupes restants.

        ① RÔLE — Garder les attributs d'avant le 19-11-2026 (`signal`, `module`, `univers`, `fiches`) vrais quand un
          groupe est retiré.
        ② CONTEXTE D'APPEL — `__init__` et `retirer`.
        ③ ENTRÉE — `self`.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Aucune valeur.
          [rend: rien]
        ⑥ TRAITEMENT — premier groupe → `signal`, `module` (None sans groupe) ; réunion ordonnée des univers ; liste des
          identifiants retenus, groupe par groupe.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Un seul endroit où ces quatre valeurs se déduisent (R-708).
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Modifie l'objet.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        self.signal = self.groupes[0].signal if self.groupes else None
        self.module = self.signal.module if self.signal is not None else None
        self.univers, self.fiches = [], []
        for g in self.groupes:
            for v in g.univers:
                if v not in self.univers:
                    self.univers.append(v)
            self.fiches += [i for i, _u in g.fiches]

    def retirer(self, groupe, motif):
        """Met à part TOUTES les fiches d'un groupe, avec le même motif, et retire le groupe du soir.

        ① RÔLE — Isoler un module qui ne se calibre pas ou dont le calcul tombe : seules ses fiches sont mises à part,
          nommées ; les autres groupes tournent (A-925, 19-11-2026).
        ② CONTEXTE D'APPEL — `main` (calibrage impossible ou en échec), `signaux_de_la_seance` (calcul qui lève).
        ③ ENTRÉE — `self` · `groupe` : un `GroupeDuSoir` de `self.groupes` · `motif` : le texte dit pour chaque fiche.
        ④ CONDITIONS D'ENTRÉE — `groupe` est dans `self.groupes`.
        ⑤ SORTIE — Aucune valeur.
          [rend: rien]
        ⑥ TRAITEMENT — ajouter (identifiant, motif) à `mises_a_part` pour chaque fiche du groupe, l'afficher, retirer le
          groupe, `_deduire`.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Principe du versement partiel tranché par Jean-Luc le 30-10-2026 à 13h55 (BACKLOG A-638) : la ligne
          fautive est mise à part et nommée, les autres passent, le passage rougit.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Modifie l'objet ; affiche une ligne par fiche.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        for i, _u in groupe.fiches:
            self.mises_a_part.append((i, motif))
            print(f"  ⛔ FICHE {i} MISE À PART PAR LE DÉTECTEUR — {motif}")
        self.groupes = [g for g in self.groupes if g is not groupe]
        self._deduire()

    def __call__(self, serie):
        """Rend les séances de signal de la série, par le signal du PREMIER groupe.

        ① RÔLE — Appliquer le signal du premier groupe (forme d'avant le 19-11-2026, gardée pour `signaux_sur`).
        ② CONTEXTE D'APPEL — `signaux_sur`, quand on lui passe le suivi au lieu d'un signal.
        ③ ENTRÉE — `self` : le suivi du soir · `serie` : les séances d'une valeur.
        ④ CONDITIONS D'ENTRÉE — Au moins un groupe.
        ⑤ SORTIE — UNE valeur : la liste rendue par le signal.
          [rend: 1]
        ⑥ TRAITEMENT — Déléguer.
        ⑦ UNITÉ — Rangs dans `serie`.
        ⑧ POURQUOI — `SignalNomme` contrôle la forme de la sortie : on passe par lui, jamais par la fonction nue.
        ⑨ CE QUI CLOCHE — Avec plusieurs groupes, n'applique que le premier : le détecteur, lui, passe chaque groupe
          à `signaux_sur` (`signaux_de_la_seance`).
        ⑩ EFFET — Celui du signal.
        ⑪ TERMINAISON — Celle du signal.
          [sort: non]
        """
        return self.signal(serie)


def fiches_du_soir(racine, B, mnemo):
    """Lit les fiches suivies le soir, applique la GARDE DU SOIR, et range les fiches retenues par signal déclaré.

    ① RÔLE — Lire dans les fiches le signal (`signal_de_la_fiche`, par `fiche_suivie` du juge) et l'univers
      (`mnemoniques_de_l_univers`), et les ranger en GROUPES : un groupe par signal déclaré (module, fonction, réglages).
      ET LA GARDE : une fiche que la porte d'entrée du juge (`porte_0`) refuse, ou dont le signal est refusé (module
      introuvable, qui ne se charge pas, fonction absente…), n'est pas suivie ; son refus est dit, et elle est MISE À
      PART sans empêcher les autres.
    ② CONTEXTE D'APPEL — `charger`, une fois par exécution.
    ③ ENTRÉE — `racine` : le dépôt · `B` : le juge des stratégies · `mnemo` : la table mnémonique → nom de valeur du
      juge (`table_mnemoniques`).
    ④ CONDITIONS D'ENTRÉE — Le registre des stratégies existe sous la racine (`chemin_du_registre`).
    ⑤ SORTIE — UNE valeur : un `SuiviDuSoir`. Exemple réel au 19-11-2026 : fiches C5E10-OBS-V1 et C5E10-QA-V1
      retenues, UN groupe (signal `signaux_c5etendu10`), univers des dix valeurs de C5E10-OBS-V1 dans son ordre,
      `garde` None. Avec IND-001-RETEST suivie en plus (copie du 19-11-2026) : DEUX groupes, C5 puis RSI REBOND.
      QUAND LA GARDE MORD, le `SuiviDuSoir` n'a aucun groupe et porte `garde` = {"verdict": V, "fiches": [{"fiche":
      identifiant, "motif": texte}, …]}, V valant exactement l'un de : « aucune_vivante » (aucune fiche suivie au
      registre — une fermeture voulue) · « refus_total » (au moins une fiche suivie, toutes refusées par la garde).
      Les fiches refusées sont toujours dites, avec le motif de leur refus.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire les fiches (`fiches_du_registre`, la dernière ligne d'un identifiant fait foi) · ② garder
      celles que le soir suit : `suivie_par_le_soir` du contrat (`etat_vie` QA ou PRODUCTION et `univers` non vide) —
      le critère que `programmes/TENIR_LES_POSITIONS.py` appelle aussi · ③ LA GARDE : `fiche_suivie` du juge (porte,
      lecture du soir, signal, référentiel) · ④ rendre la garde « aucune_vivante » si aucune fiche n'est suivie,
      « refus_total » si aucune n'est retenue · ⑤ sinon, ranger les retenues par déclaration du signal : fiches au plus
      grand univers d'abord, puis l'ordre du registre ; les groupes dans l'ordre de leur première fiche.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Plan V7, bloc 9a : le soir joue la stratégie telle que la fiche la déclare et que le juge la juge.
      LA GARDE (A-678, décision de Jean-Luc du 31-10-2026 à 22h42 : « le soir n'achète plus pour une stratégie que le
      juge refuse ») repose sur la porte du juge rejouée sur la fiche du jour. Exemple du relecteur de la version B
      (31-10-2026, sortie R07) : C5E10-QA-V1 passée à « CLOSE » dans la case `entree` → le juge la refuse.
      PLUSIEURS SIGNAUX (A-925, décision de Jean-Luc du 19-11-2026 à 19h23, réponse « 1 » : « réparer le soir pour
      qu'il fasse tourner plusieurs signaux »). Jusqu'au 19-11-2026, deux signaux différents faisaient mordre la garde
      « signaux_multiples » et AUCUN signal n'était calculé, ceux de C5 compris, parce que « le teneur de positions
      attribue chaque signal à toute fiche suivie dont l'univers contient la valeur, sans regarder quel signal l'a
      donné ». Cette raison, écrite par le Chat (lot C du 10-11-2026), n'était pas une décision de Jean-Luc (recherche
      au BACKLOG et au REGISTRE du 19-11-2026 : A-706 ⑥ ne fait que PROPOSER, au nom du superviseur, de refuser les
      signaux multiples à l'écriture du registre). Elle tombe : chaque signal porte désormais la liste des fiches qui le
      reçoivent (champ `fiches` du contrat SIGNAL), et le teneur ne l'attribue qu'à elles.
      LA GARDE N'ARRÊTE PLUS LE SOIR (superviseur R-759 du 10-11-2026 sur C9-1, consigné en A-706) : elle rend la garde
      à `main`, qui publie la séance sans signal ; c'est le circuit qui rougit (refus_total) ou avertit (aucune_vivante).
      L'ORDRE « plus grand univers d'abord » rend les dix valeurs de C5 dans l'ordre exact de l'ancienne liste écrite
      en dur.
    ⑨ CE QUI CLOCHE — ① L'ordre « plus grand univers d'abord » est une convention choisie pour l'ordre du fichier.
      ② Une fiche refusée ici l'est aussi par le teneur, qui appelle le même `fiche_suivie` (R-708) : elle est dite
      deux fois à l'écran, comptée une fois.
    ⑩ EFFET — Lit le registre et le référentiel ; charge (donc EXÉCUTE) le module de signal de chaque fiche suivie,
      par `signal_de_la_fiche`. Affiche chaque refus, et la garde quand elle mord.
    ⑪ TERMINAISON — PEUT NE PAS RENDRE LA MAIN : code 2 si le registre est illisible. La garde, elle, rend la main.
      [sort: oui]
    """
    from CONTRATS_DES_FICHIERS import chemin_du_registre, fiches_du_registre, suivie_par_le_soir
    try:
        fiches = list(fiches_du_registre(chemin_du_registre(racine)).values())
    except (OSError, ValueError, KeyError) as e:
        print(f"CODE 2 — REGISTRE DES STRATÉGIES ILLISIBLE : {type(e).__name__} : {e}. RIEN N'EST PUBLIÉ.")
        sys.exit(2)
    retenues, refusees, suivies = [], [], 0
    for f in fiches:
        # LE SOIR SUIT LA STRATÉGIE DÉCIDÉE (étape E8, A-644 ; R-513 ①) : `etat_vie` QA ou PRODUCTION et univers non
        # vide, critère écrit UNE fois au contrat et appelé aussi par le teneur des positions (R-708).
        if not suivie_par_le_soir(f):
            continue
        suivies += 1
        ident = f.get("id") or "(sans identifiant)"
        # LE CRITÈRE DE REFUS VIT DANS LE JUGE, UNE FOIS (`fiche_suivie`) : le teneur des positions l'appelle aussi
        # (RELU Cowork ab8fc49f, LC-1, 11-11-2026 : les deux écritures divergeaient sur le référentiel).
        sig, valeurs, motif = B.fiche_suivie(racine, f, mnemo)
        if motif:
            refusees.append((ident, motif))
            continue
        retenues.append((ident, sig, valeurs))
    for ident, motif in refusees:
        print(f"  ⛔ GARDE DU SOIR — la fiche {ident} n'est PAS suivie : {motif}")
    dites = [{"fiche": i, "motif": m} for i, m in refusees]
    if not suivies:
        print("  GARDE DU SOIR — aucune fiche VIVANTE à univers non vide au registre : aucun signal ne sera calculé.")
        return SuiviDuSoir([], refusees, {"verdict": "aucune_vivante", "fiches": dites})
    if not retenues:
        print("  GARDE DU SOIR — aucune fiche suivie n'est acceptée par le juge : aucun signal ne sera calculé.")
        return SuiviDuSoir([], refusees, {"verdict": "refus_total", "fiches": dites})
    ordre = sorted(range(len(retenues)), key=lambda k: -len(retenues[k][2]))
    # UN GROUPE PAR SIGNAL DÉCLARÉ (A-925) : deux fiches au même signal partagent un calcul ; deux signaux différents
    # font deux groupes, calculés chacun pour ses fiches.
    par_signal = {}
    for k in ordre:
        ident, sig, valeurs = retenues[k]
        par_signal.setdefault(sig.declaration, (sig, []))[1].append((ident, valeurs))
    return SuiviDuSoir([GroupeDuSoir(sig, membres) for sig, membres in par_signal.values()], refusees)


def charger(racine):
    """Prépare tout le matériel du détecteur, ou arrête le programme.

    ① RÔLE — **Rassembler d un coup les choses sans lesquelles rien ne peut
      être calculé** : le juge des stratégies `programmes/JUGE_DES_STRATEGIES.py`, le module de signal
      les cours, lus par le lecteur unique avec leur lecture (passages dans le CAC 40, trous), et — depuis le
      10-11-2026 — ce que le soir suit, lu dans les fiches par `fiches_du_soir` (signal, univers, garde).
      Rien n est détecté ici.
    ② CONTEXTE D APPEL — `main`, en tout PREMIER, avant même le calibrage.
      **Si le matériel manque, il vaut mieux ne rien faire que calculer sur du
      vide.**
    ③ ENTRÉE — `racine` : le dossier du dépôt. Un seul appelant, et il passe la
      valeur reçue en ligne de commande, ou `"."` à défaut.
    ④ CONDITIONS D ENTRÉE — `programmes/` doit contenir le juge des stratégies et le
      module de signal. **Les fichiers de cours, eux, sont vérifiés ici : leur
      absence est un cas prévu, pas une condition.**
    ⑤ SORTIE — QUATRE valeurs : le juge des stratégies, le `SuiviDuSoir` (signal et univers des fiches, ou la
      garde du soir quand elle a mordu ; il tient la place de l ancien module C5), les cours
      (clé de la valeur → séances triées) et la lecture (le second rendu de
      `lire_par_le_lecteur` : « passages », « trous », « composition », « seances »).
      [rend: 4]
    ⑥ TRAITEMENT — ① ajouter `programmes/` au chemin de recherche · ② charger le
      juge des stratégies · ③ **lui demander AUSSI quels fichiers de
      cours lire** · ④ vérifier que chacun existe · ⑤ lire le fichier des cours par
      `lire_par_le_lecteur`, avec la table des mnémoniques du référentiel, comme `main`
      du juge · ⑥ lire les fiches et appliquer la garde (`fiches_du_soir`) · ⑥bis charger le module des
      indicateurs du détail (`INDICATEURS_DU_DETAIL`, par `charger_module` du juge ; depuis le 19-11-2026, A-925) et
      le poser sur le suivi · ⑦ rendre les quatre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — **LE CHOIX DES FICHIERS APPARTIENT À `programmes/JUGE_DES_STRATEGIES.py`,
      un seul point de décision.** Mesuré le 12-09-2026 : ce programme nommait
      les deux anciens fichiers en dur, comme dix-sept autres, **et le fichier
      maître existait pendant que personne ne le lisait.** **LA LECTURE AUSSI
      APPARTIENT AU JUGE** (A-577, étape 7, 29-10-2026) : `lire_par_le_lecteur` refuse
      une lecture qui a mis des lignes à part, un fichier figé modifié, une valeur sans
      passage dans l indice — le détecteur refuse avec lui, une fois pour tous (R-708).
    ⑨ CE QUI CLOCHE — **`sys.path.insert` empile un chemin à chaque appel sans
      jamais vérifier s il y est déjà.** Un seul appel par exécution le rend
      inoffensif ici ; il cesserait de l être si la fonction était appelée en
      boucle.
    ⑩ EFFET — **MODIFIE LE CHEMIN DE RECHERCHE DES MODULES du processus**, ce qui
      change ce que tout `import` ultérieur trouvera. N écrit aucun fichier.
    ⑪ TERMINAISON — **PEUT NE PAS RENDRE LA MAIN : code 2 de `fiches_du_soir`,
      code 2 si un programme est introuvable, code 2 si le module des indicateurs ne se charge pas (19-11-2026),
      code 2 si le fichier maître est absent ou vide, code 2 si la
      lecture des cours est refusée ou impossible** (ValueError — HorsCalendrier
      compris —, OSError, KeyError du lecteur ou du juge, 29-10-2026). `fiches_du_soir`,
      qu il appelle, peut terminer.
      [sort: oui]
    ⑫ DÉFINITIONS —
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
    
      le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
      le module de signal : le programme qui décide quelles valeurs acheter
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré rejoué à l'identique pour vérifier qu'il n'est pas revenu.
"""
    sys.path.insert(0, os.path.join(racine, "programmes"))
    try:
        import JUGE_DES_STRATEGIES as B
    except Exception as e:
        print(f"CODE 2 — programmes introuvables : {e}")
        sys.exit(2)
    # LE CHOIX DES FICHIERS APPARTIENT AU JUGE DES STRATÉGIES — un seul point de décision
    # (12-09-2026). Ce programme nommait les deux anciens fichiers en dur, comme
    # dix-sept autres ; le fichier maître existait et personne ne le lisait.
    try:
        fichiers = B.fichiers_de_cours(racine)
    except FileNotFoundError as e:
        print(f"CODE 2 — {e}")
        sys.exit(2)
    for c in fichiers:
        if not os.path.isfile(c):
            print(f"CODE 2 — {c} absent")
            sys.exit(2)
    # LA LECTURE APPARTIENT AU JUGE (A-577, étape 7, 29-10-2026) : la même que celle de son `main`,
    # avec ses refus. Une lecture refusée ne publie rien : le signal ne serait pas celui que le juge juge.
    try:
        mnemo = B.table_mnemoniques(B.trouver(racine, "REFERENTIEL_VALEURS"))
        cours, lecture = B.lire_par_le_lecteur(racine, os.path.relpath(fichiers[0], racine), mnemo)
    except (ValueError, OSError, KeyError) as e:
        print(f"CODE 2 — LECTURE DES COURS REFUSÉE OU IMPOSSIBLE : {type(e).__name__} : {e}. RIEN N'EST PUBLIÉ.")
        sys.exit(2)
    # LE SIGNAL ET L'UNIVERS VIENNENT DES FICHES, ET LA GARDE DU SOIR LES FILTRE (plan V7, bloc 9a, 10-11-2026).
    suivi = fiches_du_soir(racine, B, mnemo)
    # LES INDICATEURS DU DÉTAIL ET DU DÉPARTAGE (A-925, 19-11-2026) : CMF(14) et CCI(14) par un seul module, chargé par
    # la fonction du juge (`charger_module`, R-708) — ils ne dépendent plus du module de signal de la fiche.
    try:
        suivi.indicateurs = B.charger_module(os.path.join(racine, INDICATEURS_DU_DETAIL), "indicateurs_du_soir")
    except (Exception, SystemExit) as e:
        print(f"CODE 2 — MODULE DES INDICATEURS ({INDICATEURS_DU_DETAIL}) ILLISIBLE : {type(e).__name__} : {e}. "
              "RIEN N'EST PUBLIÉ.")
        sys.exit(2)
    return B, suivi, cours, lecture


def signaux_sur(cours, lecture, B, mod, valeur, jusqu_a=None):
    """Rend les signaux d'une valeur, éventuellement bornés à une date, calculés sans traverser un trou.

    ① RÔLE — **Chercher les signaux d UNE SEULE valeur.** C est le grain le plus
      fin du détecteur : tout le reste l appelle en boucle.
    ② CONTEXTE D APPEL — DEUX appelants, pour des raisons opposées.
      **① `main`, sur l étalon, avec une date, pour le calibrage** — reproduire un signal
      connu avant de conclure quoi que ce soit. **② `signaux_de_la_seance`, sur chaque
      valeur de l univers, bornée à la séance**, pour la détection du jour.
    ③ ENTRÉE — `cours` : toutes les séries · `lecture` : le second rendu de
      `lire_par_le_lecteur` (ses « trous » servent ici), obligatoire depuis le 29-10-2026 ·
      `B` : le juge des stratégies `programmes/JUGE_DES_STRATEGIES.py` ·
      `mod` : un appelable sur une série — le signal d un groupe (`SignalNomme`, depuis le 19-11-2026, A-925), le
      signal d étalon de `calibrer_le_groupe`, une fonction qui ne rend rien (le détail du soir : seul le découpage
      sert), ou le `SuiviDuSoir` (son premier groupe) · `valeur` : le nom d une valeur · `jusqu_a` : une date de borne,
      **absente pour la détection, renseignée pour le calibrage**.
    ④ CONDITIONS D ENTRÉE — Aucune. **Une valeur inconnue est un cas prévu.**
    ⑤ SORTIE — DEUX valeurs : la série bornée — réduite, depuis le 29-10-2026, à son
      DERNIER MORCEAU SANS TROU, celui qui finit à la borne —, et ses signaux, dont les
      rangs `i` sont des rangs dans ce morceau.
      **Si la série est vide, rend `(None, [])` — la série à None, PAS une liste
      vide : l appelant peut distinguer « valeur absente » de « aucun signal ».**
      [rend: 2]
    ⑥ TRAITEMENT — ① retrouver la série **par son MNÉMONIQUE, jamais par son nom**
      · ② la borner à la date si demandé · ③ si elle est vide, rendre `(None, [])`
      · ④ la couper à ses trous par `couper_aux_trous` du juge, et garder le dernier
      morceau · ⑤ déléguer le calcul au signal de la fiche (`mod(serie)`).
    ⑦ UNITÉ — `jusqu_a` est une date au format AAAA-MM-JJ.
    ⑧ POURQUOI — **Le mnémonique est la clé, jamais le nom** : deux sources
      écrivent le même nom différemment, et une valeur attendue qui ne renvoie
      rien doit être une alerte, pas un silence. **Aucun indicateur ne se calcule
      à travers un trou** (A-577 ② et étape 7) : le juge calcule ses signaux morceau
      par morceau ; le signal de la séance vit dans le dernier morceau. Exemple mesuré
      (fiche de `programmes/LIRE_LES_COURS.py`) : sans la séance du 03-07-2026, le
      CMF de Vinci passe de −0,136 à −0,087 ; coupé au trou, le morceau d après est
      trop court pour un CMF sur quatorze séances, et aucun signal n est donné.
    ⑨ CE QUI CLOCHE — **`None` VEUT DIRE DEUX CHOSES, et l appelant ne peut pas les
  distinguer.** Une valeur absente des cours rend `(None, [])` · une valeur
  PRÉSENTE mais dont le bornage par `jusqu_a` ne laisse aucune séance rend
  `(None, [])` aussi. **Mesuré le 20-09-2026.** C est la même famille que la
  liste vide à deux sens de `lire` dans `programmes/TENIR_L_HISTORIQUE.py`.
  **Et le calibrage passe justement un `jusqu_a` : une valeur bornée à rien s y
  lit comme une valeur inconnue.**
  **Le bornage recopie aussi la série entière à chaque appel** ; sur quarante
  valeurs et trente séances, le coût est invisible.
⑩ EFFET — Aucun : elle ne modifie ni les cours reçus ni rien d autre.
    ⑪ TERMINAISON — Rend toujours la main. **Aucun de ses appels ne termine le
      programme.**
      [sort: non]
    ⑫ DÉFINITIONS —
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
    
      le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
      le module de signal : le programme qui décide quelles valeurs acheter
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      un signal : le repérage, sur la dernière séance connue, d'une configuration de cours qui déclenche une simulation d'achat.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    cle = B.cle_valeur(valeur)
    serie = cours.get(cle, [])
    if jusqu_a:
        serie = [b for b in serie if b["date"] <= jusqu_a]
    if not serie:
        return None, []
    # LE DERNIER MORCEAU SANS TROU (A-577, étape 7) : la coupure est celle du juge, appelée et non recopiée.
    serie = B.couper_aux_trous(serie, lecture["trous"].get(cle, []))[-1]
    return serie, mod(serie)


def signaux_de_la_seance(cours, lecture, B, mod, seance):
    """Relève, groupe par groupe et valeur par valeur, les signaux d'une séance : ceux qui sont donnés, ceux qui sont
    refusés hors du CAC 40 — chacun avec les fiches qui le reçoivent.

    ① RÔLE — Le cœur de la détection du jour, sorti de `main` le 29-10-2026 pour qu une
      épreuve puisse le rejouer séance par séance, sans écrire le fichier des signaux. Depuis le 19-11-2026 (A-925),
      il calcule CHAQUE GROUPE de fiches avec SON signal.
    ② CONTEXTE D APPEL — `main`, une fois, sur la dernière séance ; les épreuves
      (`tests/EPREUVES_DU_CIRCUIT_PAR_LE_LECTEUR_Jeu_29-10-2026.py`, `tests/EPREUVES_DU_DEPARTAGE_R207BIS_Sam_14-11-2026.py`,
      `tests/EPREUVES_DU_SOIR_A_PLUSIEURS_MODULES_Jeu_19-11-2026.py`), sur des séances passées.
    ③ ENTRÉE — `cours`, `lecture` : le rendu de `charger` · `B` : le juge des stratégies ·
      `mod` : le `SuiviDuSoir` (groupes, univers, indicateurs) · `seance` : la séance, AAAA-MM-JJ.
    ④ CONDITIONS D ENTRÉE — `lecture` porte « passages » et « trous » pour chaque valeur lue ; `mod.indicateurs` est
      le module des indicateurs du détail (posé par `charger`).
    ⑤ SORTIE — QUATRE valeurs : ① les signaux donnés, chacun {valeur, date_signal, cmf,
      cci, close, fiches} (le contrat SIGNAL ; `fiches` : les identifiants des fiches du groupe dont l'univers porte la
      valeur) · ② les signaux REFUSÉS parce que la valeur n est
      pas dans le CAC 40 ce jour-là, même forme · ③ les valeurs de l univers sans cette
      séance · ④ le détail des indicateurs de chaque valeur qui a la séance, avec « dans_l_indice »,
      « signal_hors_de_l_indice », et la longueur et le début du morceau sans trou (« seances_sans_trou », « depuis »).
      Un groupe dont le calcul LÈVE (exemple : une clôture non finie refusée par le module RSI, A-710) est retiré par
      `mod.retirer`, ses fiches mises à part et nommées ; ses signaux ne sont pas rendus, ceux des autres le sont.
      [rend: 4]
    ⑥ TRAITEMENT — ① pour chaque groupe (`mod.groupes`) : pour chaque valeur de SON univers, ses signaux par
      `signaux_sur` avec LE SIGNAL DU GROUPE, bornés à la séance et sur le dernier morceau sans trou ; un signal tombé
      sur la séance est donné si la valeur est dans le CAC 40 ce jour-là (`dans_l_indice` du juge), refusé sinon ; son
      `cmf` et son `cci` sont ceux du signal s'il les porte (C5), sinon ceux du module des indicateurs au même rang
      (RSI REBOND : le CCI(14) sert au départage R-207bis) · ② un groupe qui lève est retiré, nommé · ③ pour chaque
      valeur de la réunion des univers : la séance absente est notée, et le détail des indicateurs calculé par le
      module des indicateurs sur le même morceau.
    ⑦ UNITÉ — Le CMF, sans unité, borné à ±1 ; le CCI, sans unité ; la clôture en euros.
    ⑧ POURQUOI — A-577, étape 7 : le juge n achète qu une valeur dans l indice ; un
      signal du soir sur une valeur hors de l indice serait un signal que le juge n a
      jamais jugé. Exemple réel, mesuré le 29-10-2026 en rejouant les 722 séances du
      maître : Eiffage, entrée dans le CAC 40 le 22-12-2025, avait 9 signaux avant cette
      date, Bureau Veritas, entrée le 23-12-2024, en avait 2 ; ils sont refusés. Le
      refus se dit (au fichier, dans le détail, et à l écran).
      LE GROUPE ET SES FICHES (A-925, décision de Jean-Luc du 19-11-2026 à 19h23) : le signal dit qui le reçoit ; le
      teneur ne l'attribue qu'aux fiches nommées. LE CCI DES SIGNAUX SANS CCI : R-207bis (« stratégies TECHNIQUES → le
      CCI le plus bas ») et A-800 (« PARTOUT », décision de Jean-Luc du 15-11-2026 à 12h17) exigent un CCI pour
      départager ; un signal qui n'en porte pas reçoit le CCI(14) du module des indicateurs, le CCI de la règle.
      UN GROUPE QUI LÈVE N'ARRÊTE PAS LES AUTRES (principe du versement partiel, A-638, 30-10-2026).
    ⑨ CE QUI CLOCHE — ① Une valeur qui sort de l indice le jour même du signal donne un
      signal ; c est le teneur de positions qui refuse l achat du lendemain. ② L'isolement d'une erreur se fait par
      GROUPE, pas par valeur : une clôture non finie sur une valeur met à part tout le groupe (A-710 demande
      l'isolement par valeur : reste à faire). ③ Le CCI donné à un signal RSI est celui de C5 (période 14) : c'est la
      lecture de R-207bis faite ici, pas une décision de Jean-Luc sur le départage d'un signal RSI.
    ⑩ EFFET — Peut retirer des groupes de `mod` (`mod.retirer`), qui l'affiche.
    ⑪ TERMINAISON — Rend la main ; des boucles bornées par les groupes et les univers. Un appel du signal d'un module
      peut ne pas revenir : du code de module, non borné.
      [sort: non]
    """
    du_jour, refuses, sans_seance, detail = [], [], [], []
    ind = mod.indicateurs
    for g in list(mod.groupes):
        donnes_g, refuses_g = [], []
        try:
            for v in g.univers:
                serie, sig = signaux_sur(cours, lecture, B, g.signal, v, seance)
                if not serie or serie[-1]["date"] != seance:
                    continue
                # LA VALEUR DANS LE CAC 40 LE JOUR DU SIGNAL (A-577, étape 7) : la règle du juge, appelée.
                dedans = B.dans_l_indice(lecture["passages"].get(B.cle_valeur(v), []), seance)
                for s in sig:
                    if serie[s["i"]]["date"] != seance:
                        continue
                    # « date_signal » ET NON « date » — le contrat tranche, il ne constate pas (12-09-2026).
                    cmf = s["cmf"] if "cmf" in s else ind._c5e10_cmf(serie)[s["i"]]
                    cci = s["cci"] if "cci" in s else ind._c5e10_cci(serie)[s["i"]]
                    x = {"valeur": v, "date_signal": seance,
                         "cmf": round(cmf, 6) if cmf is not None else None,
                         "cci": round(cci, 2) if cci is not None else None,
                         "close": serie[s["i"]]["close"], "fiches": g.fiches_de(v)}
                    (donnes_g if dedans else refuses_g).append(x)
        except Exception as e:
            # UN GROUPE QUI LÈVE N'ARRÊTE PAS LES AUTRES (A-925 ; A-638) : ses fiches sont mises à part, nommées.
            mod.retirer(g, "calcul du signal tombé le %s : %s : %s" % (seance, type(e).__name__, e))
            continue
        du_jour += donnes_g
        refuses += refuses_g
    hors_par_valeur = {x["valeur"] for x in refuses}
    for v in mod.univers:
        serie, _sig = signaux_sur(cours, lecture, B, lambda _s: [], v, seance)
        if not serie or serie[-1]["date"] != seance:
            sans_seance.append(v)
            continue
        # le détail sert à relire un « aucun signal » sans refaire le calcul
        dedans = B.dans_l_indice(lecture["passages"].get(B.cle_valeur(v), []), seance)
        c = ind._c5e10_cmf(serie); v_cci = ind._c5e10_cci(serie)
        detail.append({"valeur": v,
                       "cmf": round(c[-1], 6) if c[-1] is not None else None,
                       "cmf_veille": round(c[-2], 6) if len(c) > 1 and c[-2] is not None else None,
                       "cci": round(v_cci[-1], 2) if v_cci[-1] is not None else None,
                       "dans_l_indice": dedans, "signal_hors_de_l_indice": v in hors_par_valeur,
                       "seances_sans_trou": len(serie), "depuis": serie[0]["date"]})
    return du_jour, refuses, sans_seance, detail


def confronter_l_enveloppe(sortie):
    """Confronte les champs du fichier des signaux au contrat SIGNAUX_DU_JOUR avant de l'écrire, ou arrête en code 3.

    ① RÔLE — Faire se confronter l'ÉCRIVAIN au contrat de l'enveloppe, comme le lecteur `programmes/MESSAGE_DU_SOIR.py`
      le fait déjà en lecture : jusqu'au 11-11-2026, le détecteur ne confrontait que le premier signal (contrat SIGNAL).
    ② CONTEXTE D'APPEL — `main`, juste avant d'écrire, et `publier_la_garde`, juste avant d'écrire.
    ③ ENTRÉE — `sortie` : le dictionnaire qui va être écrit dans `donnees/signaux_du_jour.json`.
    ④ CONDITIONS D'ENTRÉE — `programmes/` est au chemin de recherche (posé par `charger`).
    ⑤ SORTIE — Aucune valeur : revient si l'enveloppe tient, ou si le contrat est introuvable (dit, comme pour le
      contrat SIGNAL).
      [rend: rien]
    ⑥ TRAITEMENT — ① importer `CONTRATS_DES_FICHIERS` · ② lire les champs FACULTATIFS de l'enveloppe, s'il en
      déclare (`CHAMPS_FACULTATIFS_DE_SIGNAUX_DU_JOUR`, aucun sinon) · ③ compter comme écrits les champs facultatifs
      absents, et confronter le reste avec `verifier(…, "ECRIT")` : un champ hors contrat, ou un champ obligatoire
      absent, arrête en code 3.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — « Chaque bout se confronte AU CONTRAT — l'écrivain ET le lecteur » (instructions du projet, §7).
      Le champ `garde_du_soir` (A-706) n'est écrit que les soirs où la garde mord : il est FACULTATIF, sinon un soir
      ordinaire serait « NON ÉCRIT » ; et s'il n'est pas au contrat, le lecteur le déclarerait hors contrat. Exemple
      mesuré le 11-11-2026 sur le contrat d'avant (sans ce champ) : `verifier("SIGNAUX_DU_JOUR",
      […, "garde_du_soir"], "LU")` rend « LU « garde_du_soir » : HORS CONTRAT SIGNAUX_DU_JOUR ». Mieux vaut que
      l'écrivain le refuse (code 3) que le lecteur le découvre.
    ⑨ CE QUI CLOCHE — ① Le nom `CHAMPS_FACULTATIFS_DE_SIGNAUX_DU_JOUR` et le champ `garde_du_soir` ont été posés au
      contrat par le Chat le 11-11-2026 ; si l'un des deux en disparaissait, un soir de garde (ou, sans le champ mais
      avec le nom, chaque soir) s'arrêterait en code 3 — l'épreuve C11 le joue. ② Le contrat introuvable laisse écrire sans contrôle, comme pour
      le contrat SIGNAL (choix ancien, gardé).
    ⑩ EFFET — Affiche les écarts.
    ⑪ TERMINAISON — PEUT NE PAS RENDRE LA MAIN : code 3.
      [sort: oui]
    """
    try:
        import CONTRATS_DES_FICHIERS as C
    except ImportError:
        print("  ⚠️ CONTRATS_DES_FICHIERS introuvable — enveloppe NON VERIFIEE")
        return
    facultatifs = tuple(getattr(C, "CHAMPS_FACULTATIFS_DE_SIGNAUX_DU_JOUR", ()))
    ec = C.verifier("SIGNAUX_DU_JOUR", list(sortie.keys()) + [c for c in facultatifs if c not in sortie], "ECRIT")
    if ec:
        print("CODE 3 — LE FICHIER DES SIGNAUX NE RESPECTE PAS SON CONTRAT (SIGNAUX_DU_JOUR) :")
        for x in ec:
            print("   " + x)
        print("  RIEN N EST ECRIT : un fichier hors contrat ne sera pas lu.")
        sys.exit(3)


def publier_la_garde(racine, B, cours, garde, maintenant):
    """Publie la séance du soir sans signal, avec la garde du soir, et le dit au circuit ; ne rend jamais la main.

    ① RÔLE — Le chemin de la GARDE DU SOIR : quand le soir ne suit aucune fiche, publier quand même la séance, avec
      `signaux: []` et le champ `garde_du_soir`, pour que la tenue des positions continue.
    ② CONTEXTE D'APPEL — `main`, juste après `charger`, quand `fiches_du_soir` a rendu une garde.
    ③ ENTRÉE — `racine` : le dépôt · `B` : le juge des stratégies · `cours` : toutes les séries (clé → séances) ·
      `garde` : {"verdict", "fiches"} rendu par `fiches_du_soir` · `maintenant` : l'heure de Paris du calcul.
    ④ CONDITIONS D'ENTRÉE — `donnees/` existe sous la racine.
    ⑤ SORTIE — Aucune valeur : le fichier `donnees/signaux_du_jour.json`, la ligne `garde=<verdict>` ajoutée au fichier
      nommé par la variable `GITHUB_OUTPUT` (affichée seulement si elle n'est pas posée, hors de GitHub), et le code.
      [rend: rien]
    ⑥ TRAITEMENT — ① la séance : la plus récente de TOUS les cours lus (sans fiche, pas d'univers) · ② l'enveloppe :
      les champs ordinaires, `strategie` à null (aucune stratégie n'est suivie), univers 0, aucun détail, le calibrage
      « SANS OBJET », et `garde_du_soir` · ③ la confronter au contrat (`confronter_l_enveloppe`) · ④ écrire · ⑤ écrire
      la sortie du pas · ⑥ dire la garde et sortir en 0.
    ⑦ UNITÉ — Une séance AAAA-MM-JJ.
    ⑧ POURQUOI — Superviseur R-759 du 10-11-2026 sur C9-1 (rapport brut : etudes/PLAN_V7_SOUS_L_OUTIL_PLANNING/
      superviseur/SUPERVISEUR_C9-1_Mar_10-11-2026_17h54.md), consigné en A-706 : la garde sortait en code 4 et le
      circuit sautait la tenue des positions. Le teneur (`programmes/TENIR_LES_POSITIONS.py`) refuse un fichier sans
      séance (code 2) : publier la séance du soir, et non garder celui de la veille, lui permet d'ouvrir, suivre et
      fermer les positions déjà prises. Pas de calibrage : sans fiche suivie, il n'y a pas de signal à calibrer, et
      `signaux: []` ne se lit pas « aucun signal » puisque `garde_du_soir` le dit.
    ⑨ CE QUI CLOCHE — ① La séance est prise sur toutes les valeurs, pas sur un univers : une valeur hors de tout univers
      qui aurait seule une séance plus récente la donnerait. ② Aucune valeur sans la séance n'est relevée
      (`valeurs_sans_cette_seance` vide) : le contrôle des valeurs, pas précédent du circuit, le dit déjà.
    ⑩ EFFET — ÉCRIT `donnees/signaux_du_jour.json` en entier ; ajoute une ligne au fichier de `GITHUB_OUTPUT`.
    ⑪ TERMINAISON — NE REND JAMAIS LA MAIN : code 0 publié · code 2 aucune séance dans les cours, ou sortie du pas
      impossible à écrire (le fichier est alors déjà écrit, et le pas tombe : le circuit rougit) · code 3 par
      `confronter_l_enveloppe`.
      [sort: oui]
    """
    toutes = sorted({b["date"] for serie in cours.values() for b in serie})
    if not toutes:
        print("CODE 2 — aucune séance dans les cours")
        sys.exit(2)
    sortie = {
        "calcule_le": maintenant.strftime("%Y-%m-%d %H:%M") + " (Europe/Paris)",
        "strategie": None,
        "seance": toutes[-1],
        "univers": 0,
        "valeurs_sans_cette_seance": [],
        "signaux": [],
        "detail_indicateurs": [],
        "calibrage": {"verdict": "SANS OBJET — garde du soir : aucune fiche suivie, aucun signal calculé"},
        "garde_du_soir": garde,
    }
    confronter_l_enveloppe(sortie)
    dest = os.path.join(racine, "donnees", "signaux_du_jour.json")
    json.dump(sortie, open(dest, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    ligne = "garde=" + garde["verdict"]
    sortie_du_pas = os.environ.get("GITHUB_OUTPUT")
    if sortie_du_pas:
        try:
            with open(sortie_du_pas, "a", encoding="utf-8") as fh:
                fh.write(ligne + "\n")
        except OSError as e:
            print(f"CODE 2 — SORTIE DU PAS IMPOSSIBLE À ÉCRIRE ({type(e).__name__} : {e}) : la garde « "
                  f"{garde['verdict']} » ne serait pas vue par le circuit.")
            sys.exit(2)
    else:
        print("  " + ligne + "  (GITHUB_OUTPUT absent : sortie du pas affichée seulement)")
    print(f"  GARDE DU SOIR « {garde['verdict']} » — séance {toutes[-1]} publiée SANS SIGNAL ; "
          f"{len(garde['fiches'])} fiche(s) dite(s) dans garde_du_soir.")
    print(f"  écrit : donnees/signaux_du_jour.json · {os.path.getsize(dest)} octets")
    sys.exit(0)


def _lisible(x, forme):
    """Rend un nombre mis en forme pour l'affichage, ou « — » s'il manque.

    ① RÔLE — Afficher le CMF ou le CCI d'un signal ou d'un calibrage sans tomber sur None.
    ② CONTEXTE D'APPEL — `main`, lignes d'affichage du calibrage et des signaux.
    ③ ENTRÉE — `x` : un nombre ou None · `forme` : une spécification de format Python (« +.4f », « .1f »).
    ④ CONDITIONS D'ENTRÉE — `forme` est une spécification valable pour un nombre.
    ⑤ SORTIE — UNE valeur : un texte. Exemple : (−62.5, « .1f ») → « -62.5 » ; (None, « .1f ») → « — ».
      [rend: 1]
    ⑥ TRAITEMENT — None → « — » ; sinon `format`.
    ⑦ UNITÉ — Celle du nombre (CMF, CCI : sans unité).
    ⑧ POURQUOI — Depuis le 19-11-2026 (A-925), un signal RSI peut porter un CMF ou un CCI à None (indicateur sans
      assez de séances) et le calibrage RSI n'en porte pas : `f"{None:+.4f}"` lèverait TypeError et arrêterait le soir
      APRÈS l'écriture du fichier.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return "—" if x is None else format(x, forme)


def calibrer_le_groupe(cours, lecture, B, groupe):
    """Calibre UN groupe : retrouve le signal connu de son module, avec les réglages de l'étalon.

    ① RÔLE — Le calibrage PAR MODULE (A-925, 19-11-2026) : avant de publier les signaux d'un groupe, reproduire le
      signal connu de son module ; un groupe qui ne se calibre pas est mis à part par l'appelant, sans arrêter les autres.
    ② CONTEXTE D'APPEL — `main`, une fois par groupe, avant la détection du jour.
    ③ ENTRÉE — `cours`, `lecture` : le rendu de `charger` · `B` : le juge des stratégies · `groupe` : un `GroupeDuSoir`.
    ④ CONDITIONS D'ENTRÉE — `groupe.signal` porte `fonction`, `module`, `chemin` (un `SignalNomme` du juge).
    ⑤ SORTIE — DEUX valeurs : (le dictionnaire du calibrage {valeur, date, cmf, cci, verdict « OK »}, None) s'il
      réussit ; (None, le motif) sinon — « CALIBRAGE IMPOSSIBLE … » (aucun étalon pour la clé du module) ou
      « CALIBRAGE EN ÉCHEC … » (signal connu non retrouvé). Exemple réel (cours maître du 19-11-2026) : groupe RSI
      REBOND → VINCI 2025-04-08, `cmf` et `cci` à None (le module RSI n'en rend pas).
      Pose aussi `groupe.etalon` et `groupe.calibrage` quand il réussit.
      [rend: 2]
    ⑥ TRAITEMENT — ① chercher l'étalon sous `cle_d_etalon` · ② construire, par la classe du juge (`SignalNomme`), le
      même signal que celui du groupe mais AVEC LES RÉGLAGES DE L'ÉTALON · ③ le jouer sur la valeur de l'étalon,
      bornée à sa date (`signaux_sur`, sans traverser un trou) · ④ exiger un signal à la date.
    ⑦ UNITÉ — Le CMF et le CCI sans unité ; une date AAAA-MM-JJ.
    ⑧ POURQUOI — « Reproduire un résultat connu avant d'en produire un nouveau » (R-720). Le calibrage éprouve le
      MODULE (son code et la lecture des cours), pas les réglages d'une fiche : il se fait avec les réglages sous
      lesquels le signal est connu. Jusqu'au 19-11-2026, il ne se faisait que pour le signal de la PREMIÈRE fiche, et
      un étalon rangé sous la déclaration complète interdisait tout autre module (inventaire du 19-11-2026, A-925).
    ⑨ CE QUI CLOCHE — ① Une fiche du même module avec d'autres réglages passe le calibrage du module sans que SES
      réglages soient éprouvés sur un signal connu. ② Le calibrage d'un module qui ne rend ni CMF ni CCI (RSI) les écrit à None :
      le calibrage ne prouve alors que la date du signal connu, pas la valeur de l'indicateur.
    ⑩ EFFET — Pose `groupe.etalon` et `groupe.calibrage`.
    ⑪ TERMINAISON — Rend la main ; lève ce que lève le signal (rattrapé par `main`). Un appel du signal du module peut
      ne pas revenir : du code de module, non borné.
      [sort: non]
    """
    cle = cle_d_etalon(groupe.signal)
    etalon = ETALONS.get(cle)
    if etalon is None:
        return None, "CALIBRAGE IMPOSSIBLE : aucun signal connu pour le module %s" % cle
    s0 = groupe.signal
    signal_d_etalon = B.SignalNomme(s0.fonction, etalon["reglages"], "%s · réglages de l'étalon %s"
                                    % (cle, json.dumps(etalon["reglages"], sort_keys=True)), s0.module, s0.chemin)
    serie, sig = signaux_sur(cours, lecture, B, signal_d_etalon, etalon["valeur"], etalon["date"])
    trouve = [s for s in sig if serie and serie[s["i"]]["date"] == etalon["date"]]
    if not trouve:
        return None, ("CALIBRAGE EN ÉCHEC : le signal connu %s du %s n'est pas retrouvé (module %s)"
                      % (etalon["valeur"], etalon["date"], cle))
    e = trouve[0]
    ind_cmf = e["cmf"] if "cmf" in e else None
    ind_cci = e["cci"] if "cci" in e else None
    groupe.etalon = etalon
    groupe.calibrage = {"valeur": etalon["valeur"], "date": etalon["date"],
                        "cmf": round(ind_cmf, 6) if ind_cmf is not None else None,
                        "cci": round(ind_cci, 2) if ind_cci is not None else None, "verdict": "OK"}
    return groupe.calibrage, None


def main():
    """Détecte les signaux de la dernière séance et les publie.

    ① RÔLE — **LE PAS N°5 DU CIRCUIT DU SOIR**, entre le contrôle des cours et la
      tenue des positions. Il décide ce qui sera proposé à l achat demain.
    ② CONTEXTE D APPEL — Le circuit du soir. **Un signal n est jamais connu avant
      la clôture : ce programme ne tourne qu après elle.**
    ③ ENTRÉE — La ligne de commande : la racine du dépôt, ou `"."` à défaut.
      **Et les fichiers de cours, choisis par le juge des stratégies
      `programmes/JUGE_DES_STRATEGIES.py`, pas par ce programme.**
    ④ CONDITIONS D ENTRÉE — Le chargement doit réussir. Tout le reste est prévu.
    ⑤ SORTIE — Ne rend rien. **Tout passe par le code de sortie, l affichage, et
      le fichier des signaux.**
      [rend: rien]
    ⑥ TRAITEMENT — ① charger juge des stratégies, cours (par le lecteur unique) et fiches
      suivies (signal, univers, garde) ; SI LA GARDE DU SOIR A MORDU, publier la séance sans
      signal par `publier_la_garde`, qui ne revient pas (11-11-2026, A-706) · ② **CALIBRER CHAQUE GROUPE
      (`calibrer_le_groupe`, étalon rangé par module dans `ETALONS`, depuis le 19-11-2026, A-925) : un groupe qui ne
      se calibre pas est mis à part, ses fiches nommées ; s arrêter si AUCUN ne se calibre** · ③ trouver la dernière
      séance, tous univers confondus · ④ relever les signaux de cette séance, groupe par groupe
      (`signaux_de_la_seance` : chaque signal avec ses fiches, sans traverser un trou, refusés hors du CAC 40 ; un
      groupe dont le calcul lève est mis à part), et noter les valeurs qui n ont pas la séance · ⑤ écrire, s il y a
      plus d un groupe, le calibrage de chacun (`calibrages`) et, s il y en a, les fiches mises à part
      (`fiches_mises_a_part`) · ⑥ confronter le résultat AU CONTRAT avant d écrire — CHAQUE signal (SIGNAL, depuis le
      19-11-2026 ; avant, le premier seulement) et l enveloppe (SIGNAUX_DU_JOUR, `confronter_l_enveloppe`) · écrire le
      fichier ·
      ⑦ dire chaque valeur qui a la séance mais un indicateur du jour à None (« ◌ »),
      et leur nombre (depuis le 29-10-2026, superviseur R-759).
    ⑦ UNITÉ — Le CMF est un flux monétaire sans unité, borné à ±1 · le CCI est un
      indice, typiquement entre −200 et +200 · la clôture est en euros.
    ⑧ POURQUOI — **LE CALIBRAGE EST LA PREMIÈRE CHOSE QU IL FAIT, AVANT TOUTE
      DÉTECTION.** Un détecteur qui ne retrouve pas un signal connu ne peut rien
      affirmer des inconnus : il publierait des chiffres plausibles et faux.
      **Et le format déclaré dans `programmes/CONTRATS_DES_FICHIERS.py` tranche AVANT l écriture** : le 12-09-2026, ce programme
      écrivait « date » quand le pas suivant attendait « date_signal ».
      **Aucun des deux n avait tort — ils n avaient rien en commun.**
    ⑨ CE QUI CLOCHE — **Les étalons du calibrage sont figés dans le programme.** Si la
      séance qu un étalon désigne disparaissait des cours, le calibrage de son module échouerait et
      ses fiches seraient mises à part (rien publié s il était le seul) — ce qui est le bon comportement, mais la cause
      afficherait « signal connu non retrouvé », **qui se lit comme un défaut du
      détecteur et non comme une donnée manquante.**
    ⑩ EFFET — **ÉCRIT `donnees/signaux_du_jour.json`, EN ENTIER, à chaque
      exécution** — y compris la ligne `calcule_le`, qui dit QUAND les signaux ont
      été calculés. **Relancer ce programme hors du circuit écrase cette trace :
      une heure de midi sur une séance close la veille rend la preuve
      inutilisable.** Modifie aussi le chemin de recherche des modules.
    ⑪ TERMINAISON — **NE REND JAMAIS LA MAIN : quatre codes.**
      `0` signaux écrits — Y COMPRIS QUAND DES FICHES SONT MISES À PART (19-11-2026 : le teneur les compte et le
      circuit rougit) —, ou garde du soir publiée (`publier_la_garde`) · `1` **AUCUN groupe ne se calibre, ou le
      calcul de chaque groupe calibré tombe : RIEN publié** · `2` matériel ou séance manquants, ou sortie du pas
      impossible · `3` le fichier ne respecte pas le format déclaré dans
      `programmes/CONTRATS_DES_FICHIERS.py`, rien écrit.
      **Et `charger`, qu il appelle en premier, peut terminer en code 2 sans
      revenir.** Le circuit du soir n a pas de tolérance sur ce pas.
      [sort: oui]
    ⑫ DÉFINITIONS —
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
      CMF : le flux monétaire de Chaikin, qui mesure si l'argent entre ou sort d'une
        valeur ; sans unité, borné à ±1.
      CCI : l'indice du canal des matières premières, qui mesure de combien le cours
        s'écarte de sa moyenne récente ; sans unité, typiquement entre −200 et +200.
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par
        GitHub Actions — collecte, versement, signaux, positions, mesure,
        surveillance.
    
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      le CCI : un indicateur de bourse qui mesure de combien le prix s'écarte de sa moyenne des quatorze dernières séances.
      le CMF : un indicateur de bourse qui mesure si l'argent entre ou sort d'une valeur sur les quatorze dernières séances.
      le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
      un signal : le repérage, sur la dernière séance connue, d'une configuration de cours qui déclenche une simulation d'achat.
      une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
"""
    racine = sys.argv[1] if len(sys.argv) > 1 else "."
    maintenant = datetime.now(PARIS)
    B, mod, cours, lecture = charger(racine)
    if mod.garde is not None:
        # LA GARDE DU SOIR N'ARRÊTE PAS LE SOIR (A-706, superviseur R-759 du 10-11-2026) : la séance est publiée sans
        # signal, et le circuit continue de tenir les positions ; c'est un pas de fin qui rougit ou avertit.
        publier_la_garde(racine, B, cours, mod.garde, maintenant)
    for g in mod.groupes:
        print(f"  fiches suivies : {', '.join(i for i, _u in g.fiches)} · signal {g.signal.declaration} · "
              f"{len(g.univers)} valeur(s)")

    # ─── CALIBRAGE, MODULE PAR MODULE : reproduire un signal CONNU avant de conclure quoi que ce soit (R-720). Un module
    # qui ne se calibre pas met à part SES fiches, nommées ; les autres tournent (A-925, 19-11-2026). Si AUCUN ne se
    # calibre, rien n'est publié : un « aucun signal » non calibré ne vaut rien.
    motifs_du_calibrage = []
    for g in list(mod.groupes):
        try:
            calib, motif = calibrer_le_groupe(cours, lecture, B, g)
        except Exception as e:
            calib, motif = None, "CALIBRAGE EN ÉCHEC : le signal du module lève : %s : %s" % (type(e).__name__, e)
        if calib is None:
            motifs_du_calibrage.append(motif)
            mod.retirer(g, motif)
            continue
        print(f"  calibrage OK — {cle_d_etalon(g.signal)} : {calib['valeur']} {calib['date']} : "
              f"CMF {_lisible(calib['cmf'], '+.4f')} · CCI {_lisible(calib['cci'], '.1f')}")
    if not mod.groupes:
        print("CODE 1 — " + " | ".join(motifs_du_calibrage) + ". RIEN N'EST PUBLIÉ.")
        sys.exit(1)

    # ─── la dernière séance disponible, tous univers confondus
    toutes = sorted({b["date"] for v in mod.univers for b in cours.get(B.cle_valeur(v), [])})
    if not toutes:
        print("CODE 2 — aucune séance dans les cours")
        sys.exit(2)
    seance = toutes[-1]

    # ─── les signaux de cette séance, groupe par groupe et valeur par valeur (sans traverser un trou ; refusés hors
    # du CAC 40) ; un groupe dont le calcul lève est mis à part par `signaux_de_la_seance`, nommé.
    du_jour, refuses, sans_seance, detail = signaux_de_la_seance(cours, lecture, B, mod, seance)
    if not mod.groupes:
        print("CODE 1 — le calcul de chaque module calibré est tombé ce soir. RIEN N'EST PUBLIÉ.")
        sys.exit(1)

    sortie = {
        "calcule_le": maintenant.strftime("%Y-%m-%d %H:%M") + " (Europe/Paris)",
        "strategie": " + ".join(g.etalon["nom"] for g in mod.groupes),
        "seance": seance,
        "univers": len(mod.univers),
        "valeurs_sans_cette_seance": sans_seance,
        "signaux": du_jour,
        "detail_indicateurs": detail,
        "calibrage": mod.groupes[0].calibrage,
    }
    # PLUSIEURS MODULES (A-925) : le calibrage de chacun, avec ses fiches — écrit seulement s'il y en a plus d'un, pour
    # qu'un soir à un seul module garde l'enveloppe d'avant (champ FACULTATIF au contrat SIGNAUX_DU_JOUR).
    if len(mod.groupes) > 1:
        sortie["calibrages"] = [dict(g.calibrage, module=cle_d_etalon(g.signal), nom=g.etalon["nom"],
                                     fiches=[i for i, _u in g.fiches]) for g in mod.groupes]
    # LES FICHES MISES À PART CE SOIR SONT ÉCRITES, PAS SEULEMENT AFFICHÉES (A-925) : le teneur de positions les lit,
    # les compte dans `fiches_mises_a_part`, et le pas de fin « Rougir si une fiche suivie a ete mise a part » rougit.
    if mod.mises_a_part:
        sortie["fiches_mises_a_part"] = [{"fiche": i, "motif": m} for i, m in mod.mises_a_part]
    # LE CONTRAT TRANCHE AVANT D ECRIRE — 13-09-2026.
    # Le 12-09, ce programme ecrivait « date » quand TENIR attendait
    # « date_signal ». **Aucun des deux n avait tort : ils n avaient rien en
    # commun.** Chaque bout se confronte desormais AU CONTRAT, jamais a l autre.
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from CONTRATS_DES_FICHIERS import verifier as _verifier
        _ec = []
        for _sg in du_jour + refuses:   # CHAQUE signal, pas le seul premier (même règle que le teneur, D1 ④ du 14-11)
            _ec += [_x for _x in _verifier("SIGNAL", list(_sg.keys()), "ECRIT") if _x not in _ec]
        if _ec:
            print("CODE 3 — LES SIGNAUX NE RESPECTENT PAS LEUR CONTRAT :")
            for _x in _ec:
                print("   " + _x)
            print("  RIEN N EST ECRIT : un signal hors contrat ne sera pas lu.")
            sys.exit(3)
    except ImportError:
        print("  ⚠️ CONTRATS_DES_FICHIERS introuvable — ecriture NON VERIFIEE")
    confronter_l_enveloppe(sortie)

    dest = os.path.join(racine, "donnees", "signaux_du_jour.json")
    json.dump(sortie, open(dest, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    taille = os.path.getsize(dest)
    print(f"  séance {seance} · {len(du_jour)} signal(aux) · "
          f"{len(sans_seance)} valeur(s) sans cette séance · {len(refuses)} signal(aux) refusé(s) hors du CAC 40")
    for s in du_jour:
        print(f"    ▶ {s['valeur']} · CMF {_lisible(s['cmf'], '+.4f')} · CCI {_lisible(s['cci'], '.1f')} · "
              f"clôture {s['close']} · fiches {', '.join(s['fiches'])}")
    for s in refuses:
        print(f"    ⛔ {s['valeur']} · signal REFUSÉ : la valeur n'est pas dans le CAC 40 le {seance} "
              f"(CMF {_lisible(s['cmf'], '+.4f')} · CCI {_lisible(s['cci'], '.1f')} · fiches {', '.join(s['fiches'])})")
    for i, m in mod.mises_a_part:
        print(f"    ⛔ fiche {i} MISE À PART ce soir — {m}")
    # UNE VALEUR AVEUGLE SE DIT (superviseur R-759 du 29-10-2026, DE FOND) : toute valeur qui a la séance du soir et
    # dont un indicateur du jour vaut None ne peut donner aucun signal ; quelle qu'en soit la raison, on le dit, avec
    # son morceau sans trou et ses derniers trous. Code 0 maintenu : une valeur aveugle n'éteint pas les autres.
    # Exemple réel (relecteur du 29-10-2026, I2) : VINCI privée du 20-10-2026, 6 séances sans trou au 28-10.
    aveugles = [x for x in detail if x["cmf"] is None or x["cci"] is None]
    print(f"  {len(aveugles)} valeur(s) sans calcul possible ce soir")
    for x in aveugles:
        tr = [d for d in lecture["trous"].get(B.cle_valeur(x["valeur"]), []) if d < x["depuis"]][-3:]
        print(f"    ◌ {x['valeur']} · aucun signal possible : {x['seances_sans_trou']} séance(s) sans trou "
              f"depuis le {x['depuis']} ; trou(s) : {', '.join(tr) or 'aucun'}")
    print(f"  écrit : donnees/signaux_du_jour.json · {taille} octets")
    sys.exit(0)


if __name__ == "__main__":
    main()
