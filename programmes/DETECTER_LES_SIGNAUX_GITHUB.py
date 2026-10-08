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

CE QUE CE PROGRAMME NE RÉÉCRIT PAS — deux implémentations d'une même chose divergent toujours (R-708) : ni le chargement des cours, ni le
calcul du signal. Il importe `JUGE_DES_STRATEGIES.charger_cours` et
`MODULE_C5_ETENDU_10.signaux_c5etendu10` — le code éprouvé, celui qui a reproduit
au chiffre près le signal connu UNIBAIL du 20-08.

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
  cours, choisis par le juge des stratégies et non par ce programme.**
④ CONDITIONS D ENTRÉE — Le juge des stratégies `programmes/JUGE_DES_STRATEGIES.py` et le module
  de signal doivent être là, et au
  moins un fichier de cours. Tout le reste est un cas prévu.
⑤ SORTIE — **Un code de sortie, et un fichier de quelques centaines d octets.**
⑥ TRAITEMENT — ① charger juge des stratégies, module et cours · ② **CALIBRER sur un signal
  CONNU, et s arrêter s il manque** · ③ trouver la dernière séance · ④ relever
  les signaux de cette séance, valeur par valeur · ⑤ confronter au CONTRAT ·
  ⑥ écrire.
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
  **② RIEN N'EST RÉÉCRIT DE CE QUI EXISTE** : ce programme importe le chargement
  des cours et le calcul du signal au lieu de les refaire — deux implémentations
  d'une même chose divergent toujours (R-708).
  **③ LE CALIBRAGE PRÉCÈDE TOUTE CONCLUSION** : il reproduit d'abord un signal
  CONNU, et ne publie rien s'il ne le retrouve pas.
⑨ CE QUI CLOCHE — **Trois silences, aucun corrigé** — le ⑨ se consigne et ne se corrige pas (R-752) :
  · l étalon du calibrage est figé dans le programme — si sa séance disparaissait
    des cours, le message dirait « signal connu non retrouvé », **ce qui se lit
    comme un défaut du détecteur et non comme une donnée manquante** ;
  · `charger` empile un chemin de recherche sans vérifier s il y est déjà ;
  · **l univers est lu au chargement du programme** : une valeur ajoutée au
    référentiel pendant l exécution ne serait pas vue.
⑩ EFFET — **ÉCRIT `donnees/signaux_du_jour.json` EN ENTIER à chaque exécution**,
  y compris la ligne `calcule_le`. **Relancer hors du circuit écrase cette
  trace : une heure de midi sur une séance close la veille rend la preuve
  inutilisable.** Modifie aussi le chemin de recherche des modules.
⑪ TERMINAISON — **NE REND JAMAIS LA MAIN : quatre codes.** `0` publié ·
  `1` calibrage en échec, rien publié · `2` sources ou séance absentes ·
  `3` les signaux ne respectent pas le format déclaré dans
  `programmes/CONTRATS_DES_FICHIERS.py`, rien écrit. **Le circuit du soir n a pas
  de tolérance sur ce
  pas : un code non nul arrête la chaîne.**

USAGE : python3 DETECTER_LES_SIGNAUX_GITHUB.py <racine_du_depot>
SORTIE : donnees/signaux_du_jour.json  (quelques centaines d'octets)
CODE : 0 = calculé et publié · 1 = calibrage en échec, rien publié · 2 = sources absentes

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

# les dix valeurs du module — relevées dans le rapport de boucle du 10-09
UNIVERS = ["TOTALENERGIES", "ENGIE", "VEOLIA", "BOUYGUES", "EIFFAGE",
           "AIRBUS", "RENAULT", "UNIBAIL_RODAMCO", "BUREAU_VERITAS", "VINCI"]

# le signal connu qui sert d'étalon : dernier trade réel, reproduit au chiffre près
# par Cowork le 10-09 à 20h34 — CMF +0.0018, CCI -62.5.
ETALON = {"valeur": "UNIBAIL_RODAMCO", "date": "2026-08-20"}


def charger(racine):
    """Prépare tout le matériel du détecteur, ou arrête le programme.

    ① RÔLE — **Rassembler d un coup les trois choses sans lesquelles rien ne peut
      être calculé** : le juge des stratégies `programmes/JUGE_DES_STRATEGIES.py`, le module de signal
      `programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py` qui sait calculer les signaux, et les cours. Rien n est détecté ici.
    ② CONTEXTE D APPEL — `main`, en tout PREMIER, avant même le calibrage.
      **Si le matériel manque, il vaut mieux ne rien faire que calculer sur du
      vide.**
    ③ ENTRÉE — `racine` : le dossier du dépôt. Un seul appelant, et il passe la
      valeur reçue en ligne de commande, ou `"."` à défaut.
    ④ CONDITIONS D ENTRÉE — `programmes/` doit contenir le juge des stratégies et le
      module de signal. **Les fichiers de cours, eux, sont vérifiés ici : leur
      absence est un cas prévu, pas une condition.**
    ⑤ SORTIE — TROIS valeurs : le juge des stratégies, le module de signal, les cours chargés.
      [rend: 3]
    ⑥ TRAITEMENT — ① ajouter `programmes/` au chemin de recherche · ② charger le
      juge des stratégies et lui demander le module · ③ **lui demander AUSSI quels fichiers de
      cours lire** · ④ vérifier que chacun existe · ⑤ rendre le triplet.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — **LE CHOIX DES FICHIERS APPARTIENT À `programmes/JUGE_DES_STRATEGIES.py`,
      un seul point de décision.** Mesuré le 12-09-2026 : ce programme nommait
      les deux anciens fichiers en dur, comme dix-sept autres, **et le fichier
      maître existait pendant que personne ne le lisait.**
    ⑨ CE QUI CLOCHE — **`sys.path.insert` empile un chemin à chaque appel sans
      jamais vérifier s il y est déjà.** Un seul appel par exécution le rend
      inoffensif ici ; il cesserait de l être si la fonction était appelée en
      boucle.
    ⑩ EFFET — **MODIFIE LE CHEMIN DE RECHERCHE DES MODULES du processus**, ce qui
      change ce que tout `import` ultérieur trouvera. N écrit aucun fichier.
    ⑪ TERMINAISON — **PEUT NE PAS RENDRE LA MAIN : code 2 si un programme est
      introuvable, code 2 si un fichier de cours est absent.** Aucun de ses
      propres appels ne termine.
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
        mod = B.charger_module(
            os.path.join(racine, "programmes", "MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py"),
            "MODULE_C5_ETENDU_10")
    except Exception as e:
        print(f"CODE 2 — programmes introuvables : {e}")
        sys.exit(2)
    # LE CHOIX DES FICHIERS APPARTIENT AU JUGE DES STRATÉGIES — un seul point de décision
    # (12-09-2026). Ce programme nommait les deux anciens fichiers en dur, comme
    # dix-sept autres ; le fichier maître existait et personne ne le lisait.
    fichiers = B.fichiers_de_cours(racine)
    for c in fichiers:
        if not os.path.isfile(c):
            print(f"CODE 2 — {c} absent")
            sys.exit(2)
    return B, mod, B.charger_cours(*fichiers)


def signaux_sur(cours, B, mod, valeur, jusqu_a=None):
    """Rend les signaux d'une valeur, éventuellement bornés à une date.

    ① RÔLE — **Chercher les signaux d UNE SEULE valeur.** C est le grain le plus
      fin du détecteur : tout le reste l appelle en boucle.
    ② CONTEXTE D APPEL — `main`, DEUX fois, pour des raisons opposées.
      **① sur l étalon, avec une date, pour le calibrage** — reproduire un signal
      connu avant de conclure quoi que ce soit. **② sur chaque valeur de
      l univers, sans date**, pour la détection du jour.
    ③ ENTRÉE — `cours` : toutes les séries · `B` : le juge des stratégies `programmes/JUGE_DES_STRATEGIES.py` ·
      `mod` : le module de signal `programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py` · `valeur` : le nom d une valeur · `jusqu_a` : une date de borne,
      **absente pour la détection, renseignée pour le calibrage**.
    ④ CONDITIONS D ENTRÉE — Aucune. **Une valeur inconnue est un cas prévu.**
    ⑤ SORTIE — DEUX valeurs : la série bornée, et ses signaux.
      **Si la série est vide, rend `(None, [])` — la série à None, PAS une liste
      vide : l appelant peut distinguer « valeur absente » de « aucun signal ».**
      [rend: 2]
    ⑥ TRAITEMENT — ① retrouver la série **par son MNÉMONIQUE, jamais par son nom**
      · ② la borner à la date si demandé · ③ si elle est vide, rendre `(None, [])`
      · ④ sinon, déléguer le calcul au module de signal.
    ⑦ UNITÉ — `jusqu_a` est une date au format AAAA-MM-JJ.
    ⑧ POURQUOI — **Le mnémonique est la clé, jamais le nom** : deux sources
      écrivent le même nom différemment, et une valeur attendue qui ne renvoie
      rien doit être une alerte, pas un silence.
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
    serie = cours.get(B.cle_valeur(valeur), [])
    if jusqu_a:
        serie = [b for b in serie if b["date"] <= jusqu_a]
    if not serie:
        return None, []
    return serie, mod.signaux_c5etendu10(serie)


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
    ⑥ TRAITEMENT — ① charger juge des stratégies, module et cours · ② **CALIBRER : retrouver un
      signal CONNU, et s arrêter s il manque** · ③ trouver la dernière séance,
      tous univers confondus · ④ pour chaque valeur de l univers, relever ses
      signaux de cette séance, et noter celles qui n ont pas la séance ·
      ⑤ confronter le résultat AU CONTRAT avant d écrire · ⑥ écrire le fichier.
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
      `0` signaux écrits · `1` **calibrage en échec, RIEN publié** · `2` matériel
      ou séance manquants · `3` les signaux ne respectent pas le format déclaré dans
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
    B, mod, cours = charger(racine)

    # ─── CALIBRAGE : reproduire un signal CONNU avant de conclure quoi que ce soit
    serie, sig = signaux_sur(cours, B, mod, ETALON["valeur"], ETALON["date"])
    trouvé = [s for s in sig if serie[s["i"]]["date"] == ETALON["date"]]
    if not trouvé:
        print(f"CODE 1 — CALIBRAGE EN ÉCHEC : le signal connu {ETALON['valeur']} "
              f"du {ETALON['date']} n'est pas retrouvé. RIEN N'EST PUBLIÉ.")
        sys.exit(1)
    e = trouvé[0]
    print(f"  calibrage OK — {ETALON['valeur']} {ETALON['date']} : "
          f"CMF {e['cmf']:+.4f} · CCI {e['cci']:.1f}")

    # ─── la dernière séance disponible, tous univers confondus
    toutes = sorted({b["date"] for v in UNIVERS for b in cours.get(B.cle_valeur(v), [])})
    if not toutes:
        print("CODE 2 — aucune séance dans les cours")
        sys.exit(2)
    seance = toutes[-1]

    # ─── les signaux de cette séance, valeur par valeur
    du_jour, sans_seance, detail = [], [], []
    for v in UNIVERS:
        serie, sig = signaux_sur(cours, B, mod, v)
        if not serie:
            sans_seance.append(v)
            continue
        if serie[-1]["date"] != seance:
            sans_seance.append(v)
        for s in sig:
            if serie[s["i"]]["date"] == seance:
                # « date_signal » ET NON « date » — le contrat tranche, il ne
                # constate pas. C est le maillon casse du 12-09 repare A LA
                # SOURCE : jusqu ici, l adaptateur de TENIR traduisait l un en
                # l autre. Traduire, c est entretenir le desaccord.
                du_jour.append({"valeur": v, "date_signal": seance,
                                "cmf": round(s["cmf"], 6), "cci": round(s["cci"], 2),
                                "close": serie[s["i"]]["close"]})
        # le détail sert à relire un « aucun signal » sans refaire le calcul
        if serie[-1]["date"] == seance:
            c = mod._c5e10_cmf(serie); v_cci = mod._c5e10_cci(serie)
            detail.append({"valeur": v,
                           "cmf": round(c[-1], 6) if c[-1] is not None else None,
                           "cmf_veille": round(c[-2], 6) if len(c) > 1 and c[-2] is not None else None,
                           "cci": round(v_cci[-1], 2) if v_cci[-1] is not None else None})

    sortie = {
        "calcule_le": maintenant.strftime("%Y-%m-%d %H:%M") + " (Europe/Paris)",
        "strategie": "C5-ETENDU-10",
        "seance": seance,
        "univers": len(UNIVERS),
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

    dest = os.path.join(racine, "donnees", "signaux_du_jour.json")
    json.dump(sortie, open(dest, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    taille = os.path.getsize(dest)
    print(f"  séance {seance} · {len(du_jour)} signal(aux) · "
          f"{len(sans_seance)} valeur(s) sans cette séance")
    for s in du_jour:
        print(f"    ▶ {s['valeur']} · CMF {s['cmf']:+.4f} · CCI {s['cci']:.1f} · clôture {s['close']}")
    print(f"  écrit : donnees/signaux_du_jour.json · {taille} octets")
    sys.exit(0)


if __name__ == "__main__":
    main()
