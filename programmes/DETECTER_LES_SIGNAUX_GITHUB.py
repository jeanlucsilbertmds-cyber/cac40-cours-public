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
  lecteur unique · ② **CALIBRER sur un signal
  CONNU, et s arrêter s il manque** · ③ trouver la dernière séance · ④ relever
  les signaux de cette séance, valeur par valeur, sur le morceau sans trou qui finit à
  la séance, et refuser ceux d une valeur hors du CAC 40 ce jour-là · ⑤ confronter au
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
⑪ TERMINAISON — **NE REND JAMAIS LA MAIN : quatre codes.** `0` publié — Y COMPRIS QUAND LA
  GARDE DU SOIR MORD (11-11-2026, A-706) : la séance est publiée avec `signaux: []` et le champ
  `garde_du_soir`, et la ligne `garde=<verdict>` est écrite dans la sortie du pas ; c est un pas
  de fin du circuit qui rougit ou avertit · `1` calibrage en échec, rien publié · `2` sources ou
  séance absentes, lecture des cours refusée par le lecteur unique (29-10-2026), ou sortie du
  pas impossible à écrire · `3` le fichier ne respecte pas le format déclaré dans
  `programmes/CONTRATS_DES_FICHIERS.py`, rien écrit. **Le circuit du soir n a pas
  de tolérance sur ce pas : un code non nul — une vraie panne — arrête la chaîne.**

USAGE : python3 DETECTER_LES_SIGNAUX_GITHUB.py <racine_du_depot>
SORTIE : donnees/signaux_du_jour.json  (quelques centaines d'octets)
CODE : 0 = calculé et publié, ou garde du soir publiée (signaux vides, champ garde_du_soir, sortie de pas
       garde=aucune_vivante|refus_total|signaux_multiples) · 1 = calibrage en échec ou signal sans étalon, rien
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

# L'ÉTALON DE CHAQUE SIGNAL CONNU, rangé sous la déclaration que rend `signal_de_la_fiche` (module · fonction ·
# réglages). Le signal connu de C5 : dernier trade réel, reproduit au chiffre près par Cowork le 10-09 à 20h34 —
# CMF +0.0018, CCI -62.5. Un signal lu dans une fiche et absent de cette table ne se calibre pas : rien n'est publié
# (code 1). « nom » est l'étiquette écrite dans la case `strategie` du fichier des signaux, inchangée depuis le 11-09.
ETALONS = {
    "programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py · signaux_c5etendu10 · réglages aucun":
        {"nom": "C5-ETENDU-10", "valeur": "UNIBAIL_RODAMCO", "date": "2026-08-20"},
}


class SuiviDuSoir:
    """Ce que le soir suit, lu dans les fiches : le signal, l'univers, les fiches retenues et celles que la garde refuse.

    ① RÔLE — Porter en un seul objet ce que `fiches_du_soir` a lu dans les fiches, et s'appeler comme un signal.
    ② CONTEXTE D'APPEL — Construit par `fiches_du_soir` ; rendu par `charger` à la place de l'ancien module C5 (même
      rang, deuxième valeur), puis passé à `signaux_sur` et `signaux_de_la_seance` sous le nom `mod`.
    ③ ENTRÉE — `signal` : un `SignalNomme` du juge · `univers` : la liste des NOMS des valeurs (clés des cours) ·
      `fiches` : les identifiants retenus · `refusees` : liste de (identifiant, motif) · `garde` : None, ou la garde
      du soir (voir `fiches_du_soir`).
    ④ CONDITIONS D'ENTRÉE — `signal` est appelable et porte `module` et `declaration` ; il vaut None, avec un univers
      vide, quand `garde` est donné.
    ⑤ SORTIE — L'appel rend UNE valeur : ce que rend le signal sur la série (liste des {"i", …}).
      [rend: 1]
    ⑥ TRAITEMENT — Ranger ; à l'appel, déléguer au signal.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les épreuves du 29-10-2026 (`tests/EPREUVES_DU_CIRCUIT_PAR_LE_LECTEUR_Jeu_29-10-2026.py`) appellent
      `charger` puis `signaux_de_la_seance(cours, lecture, B, mod, séance)` : en gardant cette forme, elles éprouvent
      le chemin de la fiche sans être réécrites.
    ⑨ CE QUI CLOCHE — `module` est le module CHARGÉ par le juge sous un nom à lui : le détail des indicateurs y appelle
      `_c5e10_cmf` et `_c5e10_cci`, propres à C5 (voir ⑨ de `signaux_de_la_seance`).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; l'appel lève ce que lève le signal.
      [sort: non]
    """

    def __init__(self, signal, univers, fiches, refusees, garde=None):
        """Range les quatre lectures, et la garde du soir quand elle a mordu.

        ① RÔLE — Construire l'objet.
        ② CONTEXTE D'APPEL — `fiches_du_soir`, les épreuves C.
        ③ ENTRÉE — `self` : l'objet en construction · `signal`, `univers`, `fiches`, `refusees` : voir ③ de la
          classe ; `garde` : None (aucune garde, cas ordinaire) ou le dictionnaire
          {"verdict", "fiches"} que `fiches_du_soir` construit quand le soir ne peut suivre aucune fiche (11-11-2026) ;
          `signal` vaut alors None.
        ④ CONDITIONS D'ENTRÉE — voir ④ de la classe ; `signal` peut être None si `garde`
          ne l'est pas.
        ⑤ SORTIE — Aucune valeur (constructeur).
          [rend: rien]
        ⑥ TRAITEMENT — Ranger ; `module` repris du signal, None sans signal.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Un seul objet voyage là où voyageait le module ; la garde voyage avec lui jusqu'à `main`, qui
          publie alors la séance sans signal au lieu d'arrêter le soir (superviseur R-759 du 10-11-2026 sur C9-1).
        ⑨ CE QUI CLOCHE — Rien n'interdit un `garde` à None avec un `signal` à None : `fiches_du_soir` ne le construit
          jamais, mais l'objet ne le vérifie pas.
        ⑩ EFFET — Aucun hors de l'objet.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        self.signal, self.univers, self.fiches, self.refusees = signal, list(univers), list(fiches), list(refusees)
        self.garde = garde
        self.module = signal.module if signal is not None else None

    def __call__(self, serie):
        """Rend les séances de signal de la série, par le signal de la fiche.

        ① RÔLE — Appliquer le signal.
        ② CONTEXTE D'APPEL — `signaux_sur`, une fois par valeur.
        ③ ENTRÉE — `self` : le suivi du soir · `serie` : les séances d'une valeur.
        ④ CONDITIONS D'ENTRÉE — Celles du signal.
        ⑤ SORTIE — UNE valeur : la liste rendue par le signal.
          [rend: 1]
        ⑥ TRAITEMENT — Déléguer.
        ⑦ UNITÉ — Rangs dans `serie`.
        ⑧ POURQUOI — `SignalNomme` contrôle la forme de la sortie : on passe par lui, jamais par la fonction nue.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Celui du signal.
        ⑪ TERMINAISON — Celle du signal.
          [sort: non]
        """
        return self.signal(serie)


def fiches_du_soir(racine, B, mnemo):
    """Lit les fiches suivies le soir, applique la GARDE DU SOIR, et rend le signal et l'univers qu'elles déclarent.

    ① RÔLE — Remplacer le câblage sur C5 (module écrit en dur, dix valeurs écrites en dur) par la lecture des fiches :
      le signal par `signal_de_la_fiche`, l'univers par `mnemoniques_de_l_univers`, les deux du juge, appelés.
      ET LA GARDE : une fiche que la porte d'entrée du juge (`porte_0`) refuse, ou dont le signal est refusé, n'est
      pas suivie ; son refus est dit.
    ② CONTEXTE D'APPEL — `charger`, une fois par exécution.
    ③ ENTRÉE — `racine` : le dépôt · `B` : le juge des stratégies · `mnemo` : la table mnémonique → nom de valeur du
      juge (`table_mnemoniques`).
    ④ CONDITIONS D'ENTRÉE — Le registre des stratégies existe sous la racine (`chemin_du_registre`).
    ⑤ SORTIE — UNE valeur : un `SuiviDuSoir`. Exemple réel au 10-11-2026 : fiches C5E10-OBS-V1 et C5E10-QA-V1
      retenues, signal `signaux_c5etendu10`, univers des dix valeurs de C5E10-OBS-V1 dans son ordre, `garde` None.
      QUAND LA GARDE MORD (11-11-2026), le `SuiviDuSoir` n'a ni signal ni univers, et porte `garde` =
      {"verdict": V, "fiches": [{"fiche": identifiant, "motif": texte}, …]}, V valant exactement l'un de :
      « aucune_vivante » (aucune fiche VIVANTE à univers non vide au registre — une fermeture voulue) ·
      « refus_total » (au moins une fiche suivie, toutes refusées par la garde) · « signaux_multiples » (les fiches
      retenues déclarent plusieurs signaux ; chacune est alors dite avec « signal déclaré : <déclaration> »).
      Les fiches refusées sont toujours dites, avec le motif de leur refus.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire les fiches (`fiches_du_registre`, la dernière ligne d'un identifiant fait foi) · ② garder
      celles que le soir suit : « VIVANTE » dans `statut` et `univers` non vide — le critère de
      `programmes/TENIR_LES_POSITIONS.py`, qui leur attribue les signaux · ③ LA GARDE : refuser si `porte_0` dit non,
      si `signal_de_la_fiche` lève, ou si un mnémonique de l'univers n'est pas au référentiel · ④ rendre la garde
      « aucune_vivante » si aucune fiche n'est suivie, « refus_total » si aucune n'est retenue, « signaux_multiples » si
      les fiches retenues déclarent des signaux différents · ⑤ sinon, l'univers est la réunion des univers retenus :
      fiche au plus grand univers d'abord, puis l'ordre du registre, chaque valeur à sa première apparition.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Plan V7, bloc 9a : le soir doit jouer la stratégie telle que la fiche la déclare et que le juge la
      juge ; avant, le détecteur calculait C5 sur dix valeurs écrites dans le code, quelle que soit la fiche.
      LA GARDE (A-678, décision de Jean-Luc du 31-10-2026 à 22h42 : « le soir n'achète plus pour une stratégie que le
      juge refuse ») repose sur la porte du juge rejouée sur la fiche du jour, pas sur une colonne nouvelle : le
      champ qui porte le refus n'est pas tranché (point ④ de PROPRIETAIRES_DES_FICHIERS.md), et `porte_0` est le refus
      même du juge. Exemple du relecteur de la version B (31-10-2026, sortie R07) : C5E10-QA-V1 passée à « CLOSE »
      dans la case `entree` → le juge la refuse.
      UN SEUL SIGNAL : le teneur de positions attribue chaque signal à toute fiche suivie dont l'univers contient la
      valeur, sans regarder quel signal l'a donné ; deux signaux différents seraient attribués de travers — mieux vaut
      ne publier aucun signal.
      LA GARDE N'ARRÊTE PLUS LE SOIR (superviseur R-759 du 10-11-2026 sur le défaut C9-1 de la relecture Cowork
      4b441349, consigné en A-706) : jusqu'au 10-11, elle sortait en code 4, et le circuit du soir sautait alors la
      tenue des positions, le cockpit, la publication et la mesure — pour un état de gouvernance (Jean-Luc ferme une
      stratégie au registre), pas pour une panne. Exemple relevé par Cowork : `C5E10-OBS-V1,TOTALENERGIES,2026-11-09,…,
      EN_ATTENTE_ENTREE` n'aurait plus été ni ouverte ni suivie. Elle rend donc la garde à `main`, qui publie la
      séance sans signal ; c'est le circuit qui rougit (refus_total, signaux_multiples) ou avertit (aucune_vivante).
      L'ORDRE DE L'UNIVERS fixe l'ordre des listes du fichier publié : le plus grand univers d'abord rend les dix
      valeurs de C5 dans l'ordre exact de l'ancienne liste écrite en dur, donc un fichier identique à l'octet.
    ⑨ CE QUI CLOCHE — ① Le critère « VIVANTE et univers non vide » est RECOPIÉ de `TENIR_LES_POSITIONS.py`
      (l. 2900-2904 au 10-11-2026), qui l'écrit en ligne et ne l'expose pas : deux écritures (R-708). ② La garde
      d'ici ne retire une fiche refusée que de l'UNIVERS DU DÉTECTEUR : si son univers est contenu dans celui d'une
      fiche retenue (C5E10-QA-V1 ⊂ C5E10-OBS-V1), le teneur de positions lui attribuera encore un signal — il faut
      qu'il lise la garde (reste connu, fichier de l'agent A : BACKLOG A-706 ④). ③ L'ordre « plus grand univers
      d'abord » est une convention choisie pour l'identité du fichier, sans autre raison. ④ La garde ne regarde pas
      `etat_vie`. ⑤ Un refus PARTIEL (une fiche refusée, une autre retenue) n'est dit qu'à l'écran, pas dans le
      fichier : `garde_du_soir` n'est écrit que si le soir ne suit aucune fiche — sinon le fichier d'un soir ordinaire
      cesserait d'être identique à l'octet à celui de l'ancien détecteur.
    ⑩ EFFET — Lit le registre et le référentiel ; charge (donc EXÉCUTE) le module de signal de chaque fiche suivie,
      par `signal_de_la_fiche`. Affiche chaque refus, et la garde quand elle mord.
    ⑪ TERMINAISON — PEUT NE PAS RENDRE LA MAIN : code 2 si le registre est illisible. La garde, elle, rend la main.
      [sort: oui]
    """
    from CONTRATS_DES_FICHIERS import chemin_du_registre, fiches_du_registre
    try:
        fiches = list(fiches_du_registre(chemin_du_registre(racine)).values())
    except (OSError, ValueError, KeyError) as e:
        print(f"CODE 2 — REGISTRE DES STRATÉGIES ILLISIBLE : {type(e).__name__} : {e}. RIEN N'EST PUBLIÉ.")
        sys.exit(2)
    retenues, refusees, suivies = [], [], 0
    for f in fiches:
        if "VIVANTE" not in (f.get("statut") or "") or not (f.get("univers") or "").strip():
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
        return SuiviDuSoir(None, [], [], refusees, {"verdict": "aucune_vivante", "fiches": dites})
    if not retenues:
        print("  GARDE DU SOIR — aucune fiche suivie n'est acceptée par le juge : aucun signal ne sera calculé.")
        return SuiviDuSoir(None, [], [], refusees, {"verdict": "refus_total", "fiches": dites})
    declarations = sorted({s.declaration for _i, s, _u in retenues})
    if len(declarations) > 1:
        print("  GARDE DU SOIR — les fiches suivies déclarent plusieurs signaux ; le teneur de positions ne sait pas "
              "les distinguer : aucun signal ne sera calculé. Signaux : " + " | ".join(declarations))
        dites += [{"fiche": i, "motif": "signal déclaré : " + s.declaration} for i, s, _u in retenues]
        return SuiviDuSoir(None, [], [], refusees, {"verdict": "signaux_multiples", "fiches": dites})
    ordre = sorted(range(len(retenues)), key=lambda k: -len(retenues[k][2]))
    univers = []
    for k in ordre:
        for v in retenues[k][2]:
            if v not in univers:
                univers.append(v)
    return SuiviDuSoir(retenues[ordre[0]][1], univers, [retenues[k][0] for k in ordre], refusees)


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
      du juge · ⑥ lire les fiches et appliquer la garde (`fiches_du_soir`) · ⑦ rendre les quatre.
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
      code 2 si un programme est introuvable, code 2 si le fichier maître est absent ou vide, code 2 si la
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
      `mod` : le `SuiviDuSoir` rendu par `charger` (le signal lu dans la fiche, appelable) · `valeur` : le nom d une valeur · `jusqu_a` : une date de borne,
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
    """Relève, valeur par valeur, les signaux d'une séance : ceux qui sont donnés, ceux qui sont refusés hors du CAC 40.

    ① RÔLE — Le cœur de la détection du jour, sorti de `main` le 29-10-2026 pour qu une
      épreuve puisse le rejouer séance par séance, sans écrire le fichier des signaux.
    ② CONTEXTE D APPEL — `main`, une fois, sur la dernière séance ; les épreuves
      (`tests/EPREUVES_DU_CIRCUIT_PAR_LE_LECTEUR_Jeu_29-10-2026.py`), sur des séances passées.
    ③ ENTRÉE — `cours`, `lecture` : le rendu de `charger` · `B` : le juge des stratégies ·
      `mod` : le `SuiviDuSoir` (signal, univers et module lus dans les fiches) · `seance` : la séance, AAAA-MM-JJ.
    ④ CONDITIONS D ENTRÉE — `lecture` porte « passages » et « trous » pour chaque valeur lue.
    ⑤ SORTIE — QUATRE valeurs : ① les signaux donnés, chacun {valeur, date_signal, cmf,
      cci, close} (le contrat SIGNAL) · ② les signaux REFUSÉS parce que la valeur n est
      pas dans le CAC 40 ce jour-là, même forme · ③ les valeurs de l univers sans cette
      séance · ④ le détail des indicateurs de chaque valeur qui a la séance, avec, depuis
      le 29-10-2026, « dans_l_indice », « signal_hors_de_l_indice », et la longueur et le
      début du morceau sans trou sur lequel ils sont calculés (« seances_sans_trou »,
      « depuis »).
      [rend: 4]
    ⑥ TRAITEMENT — pour chaque valeur de l univers lu dans les fiches (`mod.univers`) : ① ses signaux par `signaux_sur`,
      bornés à la séance et sur le dernier morceau sans trou · ② une valeur sans la
      séance est notée · ③ un signal tombé sur la séance est donné si la valeur est dans
      le CAC 40 ce jour-là (`dans_l_indice` du juge), refusé sinon · ④ le détail des
      indicateurs, calculé sur le même morceau.
    ⑦ UNITÉ — Le CMF, sans unité, borné à ±1 ; le CCI, sans unité ; la clôture en euros.
    ⑧ POURQUOI — A-577, étape 7 : le juge n achète qu une valeur dans l indice ; un
      signal du soir sur une valeur hors de l indice serait un signal que le juge n a
      jamais jugé. Exemple réel, mesuré le 29-10-2026 en rejouant les 722 séances du
      maître : Eiffage, entrée dans le CAC 40 le 22-12-2025, avait 9 signaux avant cette
      date, Bureau Veritas, entrée le 23-12-2024, en avait 2 ; ils sont refusés, et les
      96 autres signaux des 722 séances sont rendus à l identique (mêmes CMF, CCI et
      clôtures que la lecture d avant). Le
      refus se dit (au fichier, dans le détail, et à l écran) : un signal écarté en
      silence ne se relit pas.
      Le jour regardé est celui du SIGNAL, faute de connaître le lendemain dans les
      cours ; le teneur de positions regarde, lui, le jour de l ACHAT, avec la règle du
      juge (`achat_admis`).
    ⑨ CE QUI CLOCHE — Une valeur qui sort de l indice le jour même du signal donne un
      signal ; c est le teneur de positions qui refuse l achat du lendemain. Le détail des
      indicateurs appelle `_c5e10_cmf` et `_c5e10_cci` du module de la fiche, propres à C5 : un
      autre signal n arrive pas jusqu ici aujourd hui (sans étalon, `main` s arrête en code 1),
      mais le jour où il aura un étalon, ce détail sera à rendre générique.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; une boucle sur les valeurs de l univers des fiches.
      [sort: non]
    """
    du_jour, refuses, sans_seance, detail = [], [], [], []
    module = mod.module
    for v in mod.univers:
        serie, sig = signaux_sur(cours, lecture, B, mod, v, seance)
        if not serie:
            sans_seance.append(v)
            continue
        if serie[-1]["date"] != seance:
            sans_seance.append(v)
        # LA VALEUR DANS LE CAC 40 LE JOUR DU SIGNAL (A-577, étape 7) : la règle du juge, appelée.
        dedans = B.dans_l_indice(lecture["passages"].get(B.cle_valeur(v), []), seance)
        hors = False
        for s in sig:
            if serie[s["i"]]["date"] == seance:
                # « date_signal » ET NON « date » — le contrat tranche, il ne
                # constate pas. C est le maillon casse du 12-09 repare A LA
                # SOURCE : jusqu ici, l adaptateur de TENIR traduisait l un en
                # l autre. Traduire, c est entretenir le desaccord.
                x = {"valeur": v, "date_signal": seance,
                     "cmf": round(s["cmf"], 6), "cci": round(s["cci"], 2),
                     "close": serie[s["i"]]["close"]}
                if dedans:
                    du_jour.append(x)
                else:
                    refuses.append(x)
                    hors = True
        # le détail sert à relire un « aucun signal » sans refaire le calcul
        if serie[-1]["date"] == seance:
            c = module._c5e10_cmf(serie); v_cci = module._c5e10_cci(serie)
            detail.append({"valeur": v,
                           "cmf": round(c[-1], 6) if c[-1] is not None else None,
                           "cmf_veille": round(c[-2], 6) if len(c) > 1 and c[-2] is not None else None,
                           "cci": round(v_cci[-1], 2) if v_cci[-1] is not None else None,
                           "dans_l_indice": dedans, "signal_hors_de_l_indice": hors,
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
      signal par `publier_la_garde`, qui ne revient pas (11-11-2026, A-706) · ② **CALIBRER, par l étalon rangé sous la déclaration du
      signal de la fiche (`ETALONS`) : retrouver un
      signal CONNU, et s arrêter s il manque** · ③ trouver la dernière séance,
      tous univers confondus · ④ pour chaque valeur de l univers, relever ses
      signaux de cette séance (`signaux_de_la_seance` : sans traverser un trou,
      refusés hors du CAC 40), et noter celles qui n ont pas la séance ·
      ⑤ confronter le résultat AU CONTRAT avant d écrire — le premier signal (SIGNAL) et, depuis
      le 11-11-2026, l enveloppe (SIGNAUX_DU_JOUR, `confronter_l_enveloppe`) · ⑥ écrire le fichier ·
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
    ⑨ CE QUI CLOCHE — **L étalon du calibrage est figé dans le programme.** Si la
      séance qu il désigne disparaissait des cours, le calibrage échouerait et
      RIEN ne serait publié — ce qui est le bon comportement, mais la cause
      afficherait « signal connu non retrouvé », **qui se lit comme un défaut du
      détecteur et non comme une donnée manquante.**
    ⑩ EFFET — **ÉCRIT `donnees/signaux_du_jour.json`, EN ENTIER, à chaque
      exécution** — y compris la ligne `calcule_le`, qui dit QUAND les signaux ont
      été calculés. **Relancer ce programme hors du circuit écrase cette trace :
      une heure de midi sur une séance close la veille rend la preuve
      inutilisable.** Modifie aussi le chemin de recherche des modules.
    ⑪ TERMINAISON — **NE REND JAMAIS LA MAIN : quatre codes.**
      `0` signaux écrits, ou garde du soir publiée (`publier_la_garde`) · `1` **calibrage en échec ou
      signal sans étalon, RIEN publié** · `2` matériel ou séance manquants, ou sortie du pas
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
    print(f"  fiches suivies : {', '.join(mod.fiches)} · signal {mod.signal.declaration} · {len(mod.univers)} valeur(s)")

    # ─── CALIBRAGE : reproduire un signal CONNU avant de conclure quoi que ce soit
    ETALON = ETALONS.get(mod.signal.declaration)
    if ETALON is None:
        print(f"CODE 1 — CALIBRAGE IMPOSSIBLE : aucun signal connu pour le signal {mod.signal.declaration}. "
              "RIEN N'EST PUBLIÉ.")
        sys.exit(1)
    serie, sig = signaux_sur(cours, lecture, B, mod, ETALON["valeur"], ETALON["date"])
    trouvé = [s for s in sig if serie and serie[s["i"]]["date"] == ETALON["date"]]
    if not trouvé:
        print(f"CODE 1 — CALIBRAGE EN ÉCHEC : le signal connu {ETALON['valeur']} "
              f"du {ETALON['date']} n'est pas retrouvé. RIEN N'EST PUBLIÉ.")
        sys.exit(1)
    e = trouvé[0]
    print(f"  calibrage OK — {ETALON['valeur']} {ETALON['date']} : "
          f"CMF {e['cmf']:+.4f} · CCI {e['cci']:.1f}")

    # ─── la dernière séance disponible, tous univers confondus
    toutes = sorted({b["date"] for v in mod.univers for b in cours.get(B.cle_valeur(v), [])})
    if not toutes:
        print("CODE 2 — aucune séance dans les cours")
        sys.exit(2)
    seance = toutes[-1]

    # ─── les signaux de cette séance, valeur par valeur (sans traverser un trou ; refusés hors du CAC 40)
    du_jour, refuses, sans_seance, detail = signaux_de_la_seance(cours, lecture, B, mod, seance)

    sortie = {
        "calcule_le": maintenant.strftime("%Y-%m-%d %H:%M") + " (Europe/Paris)",
        "strategie": ETALON["nom"],
        "seance": seance,
        "univers": len(mod.univers),
        "valeurs_sans_cette_seance": sans_seance,
        "signaux": du_jour,
        "detail_indicateurs": detail,
        "calibrage": {"valeur": ETALON["valeur"], "date": ETALON["date"],
                      "cmf": round(e["cmf"], 6), "cci": round(e["cci"], 2), "verdict": "OK"},
    }
    # LE CONTRAT TRANCHE AVANT D ECRIRE — 13-09-2026.
    # Le 12-09, ce programme ecrivait « date » quand TENIR attendait
    # « date_signal ». **Aucun des deux n avait tort : ils n avaient rien en
    # commun.** Chaque bout se confronte desormais AU CONTRAT, jamais a l autre.
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from CONTRATS_DES_FICHIERS import verifier as _verifier
        if du_jour:
            _ec = _verifier("SIGNAL", list(du_jour[0].keys()), "ECRIT")
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
        print(f"    ▶ {s['valeur']} · CMF {s['cmf']:+.4f} · CCI {s['cci']:.1f} · clôture {s['close']}")
    for s in refuses:
        print(f"    ⛔ {s['valeur']} · signal REFUSÉ : la valeur n'est pas dans le CAC 40 le {seance} "
              f"(CMF {s['cmf']:+.4f} · CCI {s['cci']:.1f})")
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
