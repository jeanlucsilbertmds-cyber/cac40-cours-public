#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIER_LES_VARIANTES.py — Mer 11-11-2026 (Paris)
EN ESSAI · outil · Rôle : écarter les versions jouées qui n'atteignent pas le seuil du tri et rendre les autres,
chacune avec le NOMBRE DE VERSIONS ESSAYÉES pour la trouver. Simulation uniquement.
Quand l'appeler : à la main, après JOUER_LES_VERSIONS, avant le jugement complet.

USAGE
    python3 programmes/TRIER_LES_VARIANTES.py <racine_du_depot> <fichier_trie> <resultats> [<resultats> ...]
    exemple :
    python3 programmes/TRIER_LES_VARIANTES.py . /tmp/TRI_C5E10-OBS-V1_E01.csv /tmp/RESULTATS_C5E10-OBS-V1_E01.csv
    (un fichier de résultats écrit par JOUER_LES_VERSIONS depuis le 11-11-2026 au soir : ceux d'avant n'ont pas la
    partie de réglage et sont refusés)

CE QUE CE PROGRAMME EST DANS LA CHAÎNE (action A-541 du BACKLOG, fonction ③ ; plan V7, bloc 5l ①)
    ⓪ PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES propose les réglages ; Jean-Luc valide ·
    ① DECLINER_LES_STRATEGIES fabrique les versions · ② JOUER_LES_VERSIONS les rejoue par le juge ·
    ③ CE PROGRAMME écarte celles qui n'atteignent pas le seuil · ④ `juger` mesure à fond celles qui restent.
    A-541 : « écarte les variantes qui n'atteignent pas un seuil et rend les autres, chacune avec le NOMBRE DE
    VARIANTES ESSAYÉES pour la trouver » ; « LE SEUIL N'EST PAS DANS LE CODE : il s'écrit au REGISTRE […] c'est
    Jean-Luc qui le fixe ».

① RÔLE — Réduire des milliers de versions jouées à celles qui méritent le jugement complet, sans perdre le compte
  de tout ce qui a été essayé.
② CONTEXTE D'APPEL — À la main, par le Chat. Aucune tâche automatique ne l'appelle.
③ ENTRÉE — La ligne de commande : la racine d'un dépôt (pour le REGISTRE des règles, le seuil provisoire et le
  contrat des fichiers) ; le chemin du fichier trié à écrire, qui ne doit pas exister ; un ou plusieurs fichiers
  de résultats écrits par JOUER_LES_VERSIONS, d'une même stratégie et d'essais différents.
④ CONDITIONS D'ENTRÉE — ① chaque fichier de résultats porte exactement les champs du contrat
  `RESULTATS_DES_VERSIONS`, dont la partie de réglage (colonnes « _70 ») · ② il n'est pas vide, ne porte qu'une
  stratégie et qu'un essai, des identifiants uniques, et autant de lignes que sa colonne `versions_dans_l_essai` ·
  ③ tous les fichiers portent la même stratégie, des essais différents, et UNE seule valeur pour chacune des
  `COLONNES_COMMUNES_A_UN_TRI` du contrat (période, fin, barème, cours et leur empreinte, frontière 70/30) ·
  ④ tout nombre est fini ; une version à zéro opération porte un gain « 0.00 » et une réussite vide ·
  ⑤ le critère du tri existe, au REGISTRE ou, à défaut, dans le fichier provisoire, marqué « À DÉCIDER PAR
  JEAN-LUC », et ne lit que les `COLONNES_DU_TRI` du contrat. Le moindre manquement arrête tout, sans rien écrire.
⑤ SORTIE — UNE valeur : le code de sortie, 0 quand le fichier trié est écrit (même vide de versions retenues :
  c'est un résultat), 1 si un fichier de résultats est refusé, 2 si le critère est introuvable ou illisible (le
  contrôle n'a pas pu tourner, R-734).
  [rend: 1]
⑥ TRAITEMENT — ① lire la ligne de commande · ② lire le critère (`lire_le_critere`) · ③ lire et contrôler chaque
  fichier de résultats (`lire_les_resultats`) · ④ exiger des conditions de jeu communes · ④bis recalculer la
  frontière 70/30 depuis le registre des stratégies et les cours joués (`frontiere_attendue`, par la même fonction
  que le juge et JOUER) et refuser tout écart · ⑤ compter les versions essayées par leur EMPREINTE de réglages
  (`empreinte_des_reglages`) : une même version recopiée sous un autre essai ne compte qu'une fois et n'est écrite
  qu'une fois si ses chiffres sont les mêmes ; des chiffres différents pour les mêmes réglages arrêtent tout · ⑥ écarter toute version sans opération dans la partie de
  réglage, quel que soit le critère, et garder chaque autre version qui passe TOUTES les conditions
  (`passe_le_critere`) · ⑦ écrire le fichier trié, par un fichier provisoire renommé à la fin · ⑧ afficher le bilan.
⑦ UNITÉ — Les colonnes gardent l'unité de JOUER_LES_VERSIONS : gains en EUROS pour 100 000 € par opération,
  réussite en POURCENTS, opérations en NOMBRE ; le compte des versions essayées en VERSIONS.
⑧ POURQUOI — Des milliers de versions ne peuvent pas toutes passer le jugement complet, et plus on en essaie, plus
  l'une paraît bonne par chance : le juge doit connaître ce nombre pour placer la barre plus haut (A-541). Le tri ne
  lit QUE la partie de réglage (les 70 % les plus anciens, coupés par le module de jugement) : choisir sur les 30 %
  gardés pour le jugement ferait du jugement un examen déjà vu (relecteur neuf du 11-11-2026, D1). Le seuil
  est une décision de Jean-Luc, pas un réglage du code (A-541, R-743 ②) : tant qu'il ne l'a pas écrit au REGISTRE,
  le tri tourne sur une valeur provisoire, lue dans un fichier, et chaque ligne écrite le dit.
⑨ CE QUI CLOCHE — ① Le compte des versions essayées ne voit que les fichiers donnés sur la ligne de commande : un
  essai oublié n'est pas compté. Le registre des expériences qui compterait tout (A-226) n'est pas fait. Les lignes
  du registre des stratégies (le « k » de R-505) ne sont pas ajoutées : elles comptent d'autres choses (question
  à Jean-Luc, echanges/A_RELIRE_TRI.md). ② Une version dont la case lue par le critère est vide (zéro opération
  pour la réussite) est ÉCARTÉE et comptée à part comme « non mesurable » : le tri ne laisse pas passer ce qu'il ne
  peut pas mesurer ; ce choix est soumis à Jean-Luc ; une version sans opération dans la partie de réglage est
  toujours écartée (D2). ③ Le critère ne lit que les colonnes de la partie de réglage :
  un critère qui demanderait un calcul (gain moyen par opération, point mort) n'est pas possible sans une colonne
  de plus. ④ Le fichier trié garde l'ordre des fichiers lus : classer est le travail du bloc 5m ④.
⑩ EFFET — Écrit le fichier trié, via un fichier provisoire `.en_cours` effacé en cas d'échec s'il a été créé par ce
  lancement. Rien d'autre.
⑪ TERMINAISON — Sort du programme avec le code 0, 1 ou 2. Un de mes appels peut-il ne pas revenir ? Non : rien n'est
  lancé, seuls des fichiers locaux sont lus.
  [sort: oui]
⑫ DÉFINITIONS
  une version : une ligne du fichier de résultats, une stratégie dont chaque réglage n'a qu'une valeur.
  le critère du tri : une ou plusieurs conditions « colonne, comparaison, valeur » ; une version est retenue si
    elle les passe TOUTES.
  le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, la loi du projet ; le critère y vit dans le tableau qui suit la
    ligne portant `MARQUE_DU_REGISTRE`.
  le fichier provisoire : `donnees/combinatoires/SEUIL_DU_TRI_PROVISOIRE.csv`, lu seulement quand le REGISTRE ne
    porte pas le critère ; chaque ligne y porte le statut « À DÉCIDER PAR JEAN-LUC ».
"""
import csv
import hashlib
import math
import os
import re
import sys

sys.dont_write_bytecode = True

REGISTRE = "gouvernance/REGISTRE_REGLES.md"
MARQUE_DU_REGISTRE = "LES SEUILS DU TRI DES VARIANTES"
PROVISOIRE = "donnees/combinatoires/SEUIL_DU_TRI_PROVISOIRE.csv"
STATUT_PROVISOIRE = "À DÉCIDER PAR JEAN-LUC"
STATUT_DECIDE = "DÉCIDÉ AU REGISTRE"
# Le statut d'une décision de Jean-Luc consignée au BACKLOG, en attendant son tableau au REGISTRE : sa date, son heure
# et le numéro de l'action, par exemple « DÉCIDÉ PAR JEAN-LUC LE 12-11-2026 À 09h10 (A-708) ». C'est une FORME
# exigée, jamais une date écrite dans le code.
FORME_D_UNE_DECISION = r"^DÉCIDÉ PAR JEAN-LUC LE \d{2}-\d{2}-\d{4} À \d{2}h\d{2} \(A-\d+\)$"
COMPARAISONS = {">": lambda a, b: a > b, ">=": lambda a, b: a >= b,
                "<": lambda a, b: a < b, "<=": lambda a, b: a <= b}
AJOUTS = ["variantes_essayees", "essais_comptes", "critere_du_tri", "statut_du_critere"]


def nombre(texte):
    """Lit un nombre écrit à la française ou à l'anglaise.

    ① RÔLE — Une seule lecture des nombres du critère et des résultats.
    ② CONTEXTE D'APPEL — `lire_le_critere` (la valeur du seuil), `lire_les_resultats` et `passe_le_critere`.
    ③ ENTRÉE — `texte` : « 0 », « 0,05 », « -138375.20 », « 1 000 ».
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nombre, ou None si le texte est vide, n'est pas un nombre, ou n'est pas fini
      (« nan », « inf »).
      [rend: 1]
    ⑥ TRAITEMENT — ① ôter les espaces, y compris insécables · ② la virgule devient un point · ③ convertir ·
      ④ refuser un nombre non fini (relecteur neuf du 11-11-2026, D3 : un gain « inf » était retenu, un seuil « nan »
      vidait le tri avec le code 0).
    ⑦ UNITÉ — Celle du texte.
    ⑧ POURQUOI — Le REGISTRE écrit « 0,05 » (table de R-505) ; JOUER écrit « 0.00 ».
    ⑨ CE QUI CLOCHE — « 1,000 » se lit 1,0 et non mille : le REGISTRE n'emploie pas la virgule des milliers.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    t = (texte or "").replace(" ", "").replace(" ", "").replace(" ", "").replace(",", ".")
    if not t:
        return None
    try:
        x = float(t)
    except ValueError:
        return None
    return x if math.isfinite(x) else None


def table_apres_la_marque(lignes, marque):
    """Rend les lignes du premier tableau qui suit la ligne portant une marque, dans un texte au format Markdown.

    ① RÔLE — Trouver le critère du tri au REGISTRE, sans dépendre de sa position dans le fichier.
    ② CONTEXTE D'APPEL — `lire_le_critere`, une fois.
    ③ ENTRÉE — `lignes` : les lignes du REGISTRE · `marque` : le texte qui annonce le tableau.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : None si la marque est absente ; sinon la liste des rangées du tableau, chacune une liste
      de cases sans espaces de bord, l'en-tête en premier et la ligne de tirets ôtée (vide si aucun tableau ne suit).
      [rend: 1]
    ⑥ TRAITEMENT — ① chercher la première ligne qui contient la marque · ② sauter jusqu'à la première ligne qui
      commence par « | » · ③ lire les lignes consécutives qui commencent par « | » · ④ ôter la ligne de tirets.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les seuils de R-505 vivent dans un tableau du REGISTRE (« LES SEUILS DE CETTE LOI ») ; le critère
      du tri suit la même forme, pour que Jean-Luc l'écrive comme les autres.
    ⑨ CE QUI CLOCHE — ① Une marque écrite deux fois : seule la première compte, et rien ne le signale ici —
      `lire_le_critere` refuse ce cas. ② Une barre verticale dans une case casse le découpage ; une rangée qui n'a
      pas autant de cases que l'en-tête est refusée par `lire_le_critere` (D9).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    debut = next((i for i, l in enumerate(lignes) if marque in l), None)
    if debut is None:
        return None
    rangees, dedans = [], False
    for l in lignes[debut + 1:]:
        s = l.strip()
        if s.startswith("|"):
            dedans = True
            cases = [c.strip() for c in s.strip("|").split("|")]
            if not all(set(c) <= set("-: ") for c in cases):
                rangees.append(cases)
        elif dedans:
            break
    return rangees


def lire_le_critere(racine):
    """Lit le critère du tri au REGISTRE, ou à défaut dans le fichier provisoire.

    ① RÔLE — Donner au tri ses conditions sans qu'aucune ne soit écrite dans le code (A-541, R-743 ②).
    ② CONTEXTE D'APPEL — `main`, une fois ; les épreuves du tri, par import.
    ③ ENTRÉE — `racine` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — TROIS valeurs : la liste des conditions, chacune un triplet (colonne, comparaison, valeur) ; le
      statut, `STATUT_DECIDE`, `STATUT_PROVISOIRE` ou le texte d'une décision à la `FORME_D_UNE_DECISION` ; la
      source lue, en texte (fichier et lignes).
      [rend: 3]
    ⑥ TRAITEMENT — ① lire le REGISTRE ; la marque y figure-t-elle ? · ② si oui : exiger UNE seule marque, un tableau
      d'en-tête « colonne | comparaison | valeur | source », au moins une rangée ; statut DÉCIDÉ · ③ sinon : lire le
      fichier provisoire, exiger les colonnes « colonne, comparaison, valeur, statut, source », au moins une ligne,
      et UN seul statut, « À DÉCIDER PAR JEAN-LUC » ou une décision datée renvoyant au BACKLOG
      (`FORME_D_UNE_DECISION`) · ④ pour chaque condition : colonne parmi
      `COLONNES_DU_TRI` du contrat (la partie de réglage seule), comparaison parmi `COMPARAISONS`, valeur numérique
      finie.
    ⑦ UNITÉ — La valeur a l'unité de sa colonne (euros, pourcents, opérations).
    ⑧ POURQUOI — Le REGISTRE fait foi : un critère écrit des deux côtés n'en a qu'un, celui du REGISTRE, et
      l'écran dit que le provisoire est ignoré. Le fichier provisoire ne peut pas se faire passer pour une
      décision : un statut qui n'est ni « À DÉCIDER PAR JEAN-LUC » ni une décision datée renvoyant au BACKLOG
      l'arrête. Décision de Jean-Luc du 12-11-2026 à 09h10 (« 1 », BACKLOG A-708) : le critère est « gain net > 0
      sur la part de réglage » ; son tableau au REGISTRE s'écrira à l'installation, d'ici là le fichier la porte. Plusieurs conditions sont permises parce
      que les critères proposés à Jean-Luc en combinent (echanges/A_RELIRE_TRI.md).
    ⑨ CE QUI CLOCHE — Le REGISTRE est cherché à son chemin fixe ; un second exemplaire ailleurs ne serait pas vu.
    ⑩ EFFET — Lit deux fichiers au plus ; affiche si le provisoire est ignoré.
    ⑪ TERMINAISON — Rend la main ; lève ValueError sur tout critère absent ou mal écrit.
      [sort: non]
    """
    sys.path.insert(0, os.path.join(racine, "programmes"))
    import CONTRATS_DES_FICHIERS as contrat
    lignes = open(os.path.join(racine, REGISTRE), encoding="utf-8").read().splitlines()
    f_prov = os.path.join(racine, PROVISOIRE)
    table = table_apres_la_marque(lignes, MARQUE_DU_REGISTRE)
    if table is not None:
        if sum(MARQUE_DU_REGISTRE in l for l in lignes) != 1:
            raise ValueError("la marque « %s » figure plusieurs fois au REGISTRE" % MARQUE_DU_REGISTRE)
        if not table or [c.lower() for c in table[0]] != ["colonne", "comparaison", "valeur", "source"]:
            raise ValueError("le tableau qui suit « %s » au REGISTRE n'a pas l'en-tête « colonne | comparaison | "
                             "valeur | source »" % MARQUE_DU_REGISTRE)
        courtes = [r for r in table[1:] if len(r) != 4]
        if courtes:
            # UNE RANGÉE COURTE EST UN CRITÈRE ILLISIBLE, PAS UNE KeyError (relecteur neuf du 11-11-2026, D9)
            raise ValueError("le tableau « %s » au REGISTRE a une rangée de %d case(s) au lieu de 4 : %s"
                             % (MARQUE_DU_REGISTRE, len(courtes[0]), courtes[0]))
        brutes = [dict(zip(["colonne", "comparaison", "valeur", "source"], r)) for r in table[1:]]
        statut, source = STATUT_DECIDE, "%s, tableau « %s »" % (REGISTRE, MARQUE_DU_REGISTRE)
        if os.path.exists(f_prov):
            print("LE REGISTRE PORTE LE CRITÈRE : le fichier provisoire %s est IGNORÉ" % PROVISOIRE)
    else:
        if not os.path.exists(f_prov):
            raise ValueError("aucun critère du tri : ni « %s » au REGISTRE, ni %s" % (MARQUE_DU_REGISTRE, PROVISOIRE))
        lecteur = csv.DictReader(open(f_prov, encoding="utf-8-sig"))
        if lecteur.fieldnames != ["colonne", "comparaison", "valeur", "statut", "source"]:
            raise ValueError("%s : en-tête %s au lieu de colonne, comparaison, valeur, statut, source"
                             % (PROVISOIRE, lecteur.fieldnames))
        brutes = list(lecteur)
        if any(None in b or None in b.values() for b in brutes):
            raise ValueError("%s : une ligne n'a pas autant de cases que l'en-tête" % PROVISOIRE)
        statuts = {(b.get("statut") or "").strip() for b in brutes}
        mauvais = [x for x in statuts if x != STATUT_PROVISOIRE and not re.match(FORME_D_UNE_DECISION, x)]
        if mauvais or len(statuts) > 1:
            raise ValueError("%s : statut « %s » ; il faut UN seul statut, « %s » ou une décision datée renvoyant au "
                             "BACKLOG (« DÉCIDÉ PAR JEAN-LUC LE JJ-MM-AAAA À HHhMM (A-nnn) ») — une décision s'écrit "
                             "au REGISTRE ou se consigne au BACKLOG" % (PROVISOIRE, sorted(statuts), STATUT_PROVISOIRE))
        statut, source = (statuts.pop() if statuts else STATUT_PROVISOIRE), PROVISOIRE
    if not brutes:
        raise ValueError("le critère du tri (%s) n'a aucune condition" % source)
    conditions = []
    for b in brutes:
        col, comp, val = b["colonne"].strip(), b["comparaison"].strip(), nombre(b["valeur"])
        if col not in contrat.COLONNES_DU_TRI:
            raise ValueError("critère du tri (%s) : la colonne « %s » n'est pas une colonne de la partie de réglage "
                             "(permises : %s) — le tri ne lit jamais les 30 %% gardés pour le jugement"
                             % (source, col, ", ".join(contrat.COLONNES_DU_TRI)))
        if comp not in COMPARAISONS:
            raise ValueError("critère du tri (%s) : comparaison « %s » inconnue (permises : %s)"
                             % (source, comp, " ".join(COMPARAISONS)))
        if val is None:
            raise ValueError("critère du tri (%s) : la valeur « %s » n'est pas un nombre fini" % (source, b["valeur"]))
        conditions.append((col, comp, val))
    return conditions, statut, source


def lire_les_resultats(chemin, contrat):
    """Lit un fichier de résultats de JOUER_LES_VERSIONS et refuse ce qui ne tient pas.

    ① RÔLE — Garantir que le tri compte et compare sur un fichier complet et cohérent.
    ② CONTEXTE D'APPEL — `main`, une fois par fichier de résultats ; les épreuves du tri, par import.
    ③ ENTRÉE — `chemin` : le fichier · `contrat` : le module `CONTRATS_DES_FICHIERS`.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe.
    ⑤ SORTIE — UNE valeur : la liste des lignes, chacune un dictionnaire.
      [rend: 1]
    ⑥ TRAITEMENT — ① exiger exactement les champs du contrat (un fichier d'avant le 11-11-2026, sans partie de
      réglage, est refusé) · ② exiger au moins une ligne, une seule stratégie, un seul essai, des identifiants
      uniques, et `versions_dans_l_essai` égal au nombre de lignes · ③ pour la période entière ET pour la partie de
      réglage : un nombre entier positif ou nul d'opérations, un gain fini, et, à zéro opération, un gain nul et une
      réussite vide ; ailleurs une réussite finie.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le nombre de versions essayées est la moitié du travail du tri (A-541) : un fichier tronqué
      le fausserait sans bruit. JOUER annonce le nombre de versions de l'essai sur chaque ligne ; il est relu ici.
    ⑨ CE QUI CLOCHE — Le contenu des réglages (tp, sl, horizon, univers) n'est pas contrôlé : JOUER le fait.
    ⑩ EFFET — Lit le fichier.
    ⑪ TERMINAISON — Rend la main ; lève ValueError sur le premier défaut.
      [sort: non]
    """
    nom = os.path.basename(chemin)
    lecteur = csv.DictReader(open(chemin, encoding="utf-8-sig"))
    champs = lecteur.fieldnames or []
    exiges = list(contrat.RESULTATS_DES_VERSIONS)
    manquants = [c for c in exiges if c not in champs]
    hors = [c for c in champs if c not in contrat.RESULTATS_DES_VERSIONS]
    if manquants or hors:
        raise ValueError("%s : champs absents %s, champs hors contrat %s" % (nom, manquants, hors))
    lignes = list(lecteur)
    if not lignes:
        raise ValueError("%s : aucune version" % nom)
    if len({l["strategie"] for l in lignes}) != 1 or len({l["essai"] for l in lignes}) != 1:
        raise ValueError("%s : plusieurs stratégies ou essais" % nom)
    ids = [l["id_version"] for l in lignes]
    if len(set(ids)) != len(ids):
        raise ValueError("%s : identifiants de version en double" % nom)
    annonces = {l["versions_dans_l_essai"] for l in lignes}
    if annonces != {str(len(lignes))}:
        raise ValueError("%s : annonce %s versions et en porte %d" % (nom, sorted(annonces), len(lignes)))
    for l in lignes:
        for suffixe in ("", "_70"):
            ops = l["operations" + suffixe].strip()
            if not ops.isdigit():
                raise ValueError("%s : %s, nombre d'opérations%s illisible « %s »" % (nom, l["id_version"], suffixe, ops))
            gain = nombre(l["gain_net_euros" + suffixe])
            if gain is None:
                raise ValueError("%s : %s, gain%s illisible ou non fini « %s »"
                                 % (nom, l["id_version"], suffixe, l["gain_net_euros" + suffixe]))
            reussite = l["reussite_pourcents_exacte" + suffixe].strip()
            if int(ops) == 0 and (gain != 0 or reussite):
                raise ValueError("%s : %s, zéro opération%s mais un gain ou une réussite écrits"
                                 % (nom, l["id_version"], suffixe))
            if int(ops) > 0 and nombre(reussite) is None:
                raise ValueError("%s : %s, réussite%s illisible ou non finie « %s »"
                                 % (nom, l["id_version"], suffixe, reussite))
    return lignes


def passe_le_critere(ligne, conditions):
    """Dit si une version passe toutes les conditions du critère.

    ① RÔLE — La seule comparaison d'une version au seuil.
    ② CONTEXTE D'APPEL — `main`, une fois par version ; les épreuves du tri.
    ③ ENTRÉE — `ligne` : une version · `conditions` : la liste rendue par `lire_le_critere`.
    ④ CONDITIONS D'ENTRÉE — La ligne a passé `lire_les_resultats`.
    ⑤ SORTIE — DEUX valeurs : vrai si TOUTES les conditions sont passées ; vrai si une case lue était vide (la
      version est alors « non mesurable » et ne passe pas).
      [rend: 2]
    ⑥ TRAITEMENT — ① zéro opération dans la partie de réglage → non mesurable, ne passe JAMAIS, quel que soit le
      critère (relecteur neuf du 11-11-2026, D2 : « gain_net_euros >= 0 » retenait une version sans opération) ·
      ② pour chaque condition : lire la case ; vide → non mesurable, ne passe pas ; sinon comparer.
    ⑦ UNITÉ — Celle de chaque colonne.
    ⑧ POURQUOI — « Toutes » plutôt qu'« une » : chaque condition est une exigence ; ce choix est soumis à
      Jean-Luc avec les critères (echanges/A_RELIRE_TRI.md).
    ⑨ CE QUI CLOCHE — Voir ⑨ ② de l'en-tête : la case vide écarte.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    ops70 = (ligne.get("operations_70") or "").strip()
    if ops70.isdigit() and int(ops70) == 0:      # le NOMBRE, pas le texte : « 00 » est zéro (relecteur, tour 2, N4)
        return False, True
    passe, non_mesurable = True, False
    for col, comp, val in conditions:
        x = nombre(ligne.get(col))
        if x is None:
            passe, non_mesurable = False, True
        elif not COMPARAISONS[comp](x, val):
            passe = False
    return passe, non_mesurable


def texte_du_critere(conditions):
    """Écrit le critère en une ligne lisible, recopiée dans chaque ligne du fichier trié.

    ① RÔLE — Que chaque version retenue dise sous quel critère elle l'a été (R-743 ① : un verdict nomme sa grille).
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `conditions` : la liste rendue par `lire_le_critere`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte, conditions jointes par « ET ».
      [rend: 1]
    ⑥ TRAITEMENT — « colonne comparaison valeur » pour chaque condition.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un fichier trié lu dans six mois doit dire son critère sans rien ouvrir d'autre.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    return " ET ".join("%s %s %s" % (c, o, repr(v)) for c, o, v in conditions)


def empreinte_des_reglages(ligne, jouer):
    """Rend l'empreinte des réglages d'une version : deux versions de même empreinte sont la même version.

    ① RÔLE — Reconnaître une version recopiée sous un autre essai ou un autre identifiant, par ce qu'elle EST et
      jamais par son nom (relecteur neuf du 11-11-2026, D4).
    ② CONTEXTE D'APPEL — `main`, une fois par version lue ; les épreuves, par import.
    ③ ENTRÉE — `ligne` : une version du fichier de résultats · `jouer` : le module `JOUER_LES_VERSIONS` de la
      racine, pour sa liste `REGLAGES` et son découpage d'univers `codes`.
    ④ CONDITIONS D'ENTRÉE — La ligne a passé `lire_les_resultats`.
    ⑤ SORTIE — UNE valeur : seize caractères hexadécimaux.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque réglage de `jouer.REGLAGES` : l'univers découpé et trié par `jouer.codes`, l'horizon
      en entier, les autres en nombre ; joindre, hacher (SHA-256), garder seize caractères.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le nombre de versions essayées relève la barre du jugement : compter deux fois la même version la
      relève à tort (sonde D2 du relecteur : une combinatoire recopiée sous E09 faisait passer le compte de 4 à 8).
      La liste des réglages et le découpage des univers sont ceux de JOUER, importés (R-708).
    ⑨ CE QUI CLOCHE — Le signal de la fiche n'est pas dans les résultats : deux essais joués avec deux signaux
      différents sous le même identifiant de stratégie seraient vus comme les mêmes versions (n°83 : la dernière ligne
      d'une fiche fait foi, elle peut changer entre deux essais).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ValueError sur un réglage illisible.
      [sort: non]
    """
    morceaux = []
    for k in jouer.REGLAGES:
        if k == "univers":
            morceaux.append(",".join(jouer.codes(ligne[k])))
        elif k == "horizon":
            morceaux.append(str(int(ligne[k])))
        else:
            x = nombre(ligne[k])
            if x is None:
                raise ValueError("%s : réglage %s illisible « %s »" % (ligne.get("id_version"), k, ligne[k]))
            morceaux.append(repr(x))
    return hashlib.sha256("|".join(morceaux).encode("utf-8")).hexdigest()[:16]


CHIFFRES_D_UNE_VERSION = ("operations", "reussite_pourcents_exacte", "gain_net_euros", "operations_70",
                          "reussite_pourcents_exacte_70", "gain_net_euros_70")


def frontiere_attendue(racine, ligne):
    """Recalcule, depuis le registre des stratégies et les cours nommés, la frontière que le juge appliquera.

    ① RÔLE — Garantir que les colonnes « _70 » d'un fichier de résultats sont bien les années de réglage de la
      fiche TELLE QU'ELLE EST AU REGISTRE AUJOURD'HUI, et non celles d'une période changée depuis le jeu.
    ② CONTEXTE D'APPEL — `main`, une fois (toutes les lignes portent les mêmes conditions communes) ; les épreuves.
    ③ ENTRÉE — `racine` : la racine du dépôt · `ligne` : une ligne du fichier de résultats (stratégie, cours joués
      et leur empreinte, début de période, fin écrite dans la fiche).
    ④ CONDITIONS D'ENTRÉE — Sous la racine : le juge, le module de jugement, le contrat, le registre des
      stratégies, le référentiel et le fichier de cours nommé.
    ⑤ SORTIE — UNE valeur : la frontière attendue, AAAA-MM-JJ.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire la DERNIÈRE ligne de la fiche (n°83) par `fiches_du_registre` du contrat · ② ses bornes
      par `porte_0` du juge, qui doivent être le début et la fin écrits dans le fichier · ③ exiger que le fichier de
      cours existe et que ses séances jusqu'à la fin de la fiche portent l'empreinte écrite
      (`empreinte_des_cours_jusqu_a` de JOUER ; une séance ajoutée après la fin ne compte pas, M2) · ④ lire ses séances par `lire_par_le_lecteur` du juge, comme JOUER
      et le juge · ⑤ demander la frontière à `frontiere_de_la_fiche` du module de jugement, la seule fonction qui
      l'établit.
    ⑦ UNITÉ — Des dates.
    ⑧ POURQUOI — Relecteur neuf de la mission TRI, tour 2, N1 MAJEUR : un fichier joué avant un changement de la
      période de la fiche, ou sur d'autres cours, faisait choisir sur les 30 % du juge ; superviseur R-759 du
      12-11-2026 : le tri recalcule depuis le registre et REFUSE tout écart, par la même fonction que le juge et
      JOUER (R-708) — et non par une comparaison de plus entre fichiers.
    ⑨ CE QUI CLOCHE — ① Le juge n'est lancé que comme bibliothèque : si son `main` lisait autrement les cours, ce
      contrôle ne le verrait pas ; l'épreuve J10 compare la frontière écrite par JOUER à celle que le juge imprime.
      ② Lit tout le fichier de cours (quelques secondes sur le maître, davantage sur 20 ans).
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main ; lève ValueError sur tout écart.
      [sort: non]
    """
    import CONTRATS_DES_FICHIERS as contrat
    import JUGE_DES_STRATEGIES as J
    sid = ligne["strategie"]
    fiche = contrat.fiches_du_registre(os.path.join(racine, contrat.REGISTRE_DES_STRATEGIES)).get(sid)
    if fiche is None:
        raise ValueError("fiche %s absente du registre des stratégies : frontière impossible à vérifier" % sid)
    ok, manques, bornes = J.porte_0(fiche)
    if not ok:
        raise ValueError("la porte 0 refuse la fiche %s : %s" % (sid, manques))
    if (ligne["periode_debut"], ligne["fin_ecrite_dans_la_fiche"]) != tuple(bornes):
        raise ValueError("la fiche %s a changé de période depuis le jeu : %s -> %s au registre, %s -> %s dans les "
                         "résultats" % (sid, bornes[0], bornes[1], ligne["periode_debut"],
                                        ligne["fin_ecrite_dans_la_fiche"]))
    f_cours = os.path.join(racine, ligne["cours_joues"])
    if not os.path.isfile(f_cours):
        raise ValueError("fichier de cours joué introuvable : %s" % ligne["cours_joues"])
    import JOUER_LES_VERSIONS as jouer_
    # L'EMPREINTE PORTE SUR LES SÉANCES JUSQU'À LA FIN DE LA FICHE (M2, 12-11-2026), calculée par la fonction de JOUER
    emp = jouer_.empreinte_des_cours_jusqu_a(f_cours, bornes[1])
    if emp != ligne["empreinte_des_cours"]:
        # LE MESSAGE NE DIT QUE CE QUI EST MESURÉ (relecteur du tour 4, m2 ; superviseur R-759 du tour 5) : deux causes
        # possibles, un seul remède. Ni version ni détection d'un ancien format : il n'a jamais existé sur main.
        raise ValueError("l'empreinte des cours %s jusqu'à la fin de la fiche (%s) diffère de celle des résultats (%s) "
                         ": soit les cours de la période ont changé, soit le fichier a été écrit par une version "
                         "antérieure de JOUER — à rejouer" % (ligne["cours_joues"], emp, ligne["empreinte_des_cours"]))
    mnemo = J.table_mnemoniques(J.trouver(racine, "REFERENTIEL_VALEURS"))
    cours, _ = J.lire_par_le_lecteur(racine, os.path.relpath(f_cours, racine), mnemo)
    mod_jug = J.charger_module(os.path.join(racine, "programmes", "MODULE_JUGEMENT.py"), "jug_tri")
    return mod_jug.frontiere_de_la_fiche(fiche, {b["date"] for s in cours.values() for b in s}, bornes)


def main():
    """Lit le critère et les résultats, trie, écrit.

    ① RÔLE — Point d'entrée du programme.
    ② CONTEXTE D'APPEL — Le lancement, et lui seul.
    ③ ENTRÉE — La ligne de commande (voir l'en-tête).
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête, ④.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2, passée à la sortie du processus.
      [rend: 1]
    ⑥ TRAITEMENT — Voir l'en-tête, ⑥.
    ⑦ UNITÉ — Voir l'en-tête, ⑦.
    ⑧ POURQUOI — Voir l'en-tête, ⑧.
    ⑨ CE QUI CLOCHE — Voir l'en-tête, ⑨.
    ⑩ EFFET — Écrit le fichier trié.
    ⑪ TERMINAISON — Rend la main ; une exception imprévue efface le fichier provisoire puis remonte.
      [sort: non]
    """
    if len(sys.argv) < 4 or any(a.startswith("--") for a in sys.argv[1:]):
        print(__doc__.split("①")[0])
        return 1
    racine, f_out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    fichiers = [os.path.abspath(a) for a in sys.argv[3:]]
    if os.path.exists(f_out):
        print("ARRÊT : le fichier trié existe déjà : %s" % f_out)
        return 1
    if len(set(fichiers)) != len(fichiers):
        print("ARRÊT : un fichier de résultats est donné deux fois : ses versions seraient comptées deux fois")
        return 1
    try:
        conditions, statut, source = lire_le_critere(racine)
    except (ValueError, OSError) as e:
        # UN CRITÈRE ILLISIBLE EST UN CONTRÔLE QUI N'A PAS PU TOURNER : code 2 (R-734 ; relecteur neuf, D3)
        print("ARRÊT (critère illisible) : %s" % e)
        return 2
    import CONTRATS_DES_FICHIERS as contrat   # chargé depuis la racine par `lire_le_critere`
    import JOUER_LES_VERSIONS as jouer        # idem : sa liste de réglages et son découpage d'univers
    try:
        par_fichier = [lire_les_resultats(f, contrat) for f in fichiers]
    except (ValueError, OSError) as e:
        print("ARRÊT : %s" % e)
        return 1
    strategies = {l[0]["strategie"] for l in par_fichier}
    essais = [l[0]["essai"] for l in par_fichier]
    if len(strategies) != 1 or len(set(essais)) != len(essais):
        print("ARRÊT : les fichiers doivent porter UNE stratégie et des essais différents : %s %s"
              % (sorted(strategies), essais))
        return 1
    # DES VERSIONS JOUÉES DANS DES CONDITIONS DIFFÉRENTES NE SE TRIENT PAS ENSEMBLE (relecteur neuf, D4).
    for c in contrat.COLONNES_COMMUNES_A_UN_TRI:
        valeurs = {l[c] for lignes in par_fichier for l in lignes}
        if len(valeurs) != 1:
            print("ARRÊT : les versions n'ont pas été jouées dans les mêmes conditions — « %s » prend %d valeurs : %s"
                  % (c, len(valeurs), sorted(valeurs)[:4]))
            return 1
    # LA FRONTIÈRE DES FICHIERS EST CELLE QUE LE JUGE APPLIQUERA, recalculée depuis le registre (N1, 12-11-2026).
    try:
        attendue = frontiere_attendue(racine, par_fichier[0][0])
    except (ValueError, OSError) as e:
        print("ARRÊT : %s" % e)
        return 1
    if attendue != par_fichier[0][0]["frontiere_70_30"]:
        print("ARRÊT : frontière 70/30 des résultats %s, frontière de la fiche au registre %s : les colonnes « _70 » "
              "ne sont pas les années de réglage que le juge retiendra ; rien n'est trié"
              % (par_fichier[0][0]["frontiere_70_30"], attendue))
        return 1
    try:
        vues, doublons, uniques = {}, 0, []
        for f, lignes in zip(fichiers, par_fichier):
            for l in lignes:
                e = empreinte_des_reglages(l, jouer)
                if e in vues:
                    # MÊMES RÉGLAGES : mêmes chiffres -> comptée une fois ; chiffres différents -> ARRÊT, en nommant
                    # les deux fichiers (relecteur, tour 2, N3 ; lecture la plus stricte, à confirmer par Jean-Luc)
                    f0, l0 = vues[e]
                    if any(l0[c] != l[c] for c in CHIFFRES_D_UNE_VERSION):
                        print("ARRÊT : mêmes réglages, chiffres différents : %s dans %s et %s dans %s — un défaut de "
                              "jeu, pas un choix à faire" % (l0["id_version"], os.path.basename(f0), l["id_version"],
                                                              os.path.basename(f)))
                        return 1
                    doublons += 1
                    continue
                vues[e] = (f, l)
                uniques.append(l)
    except ValueError as e:
        print("ARRÊT : %s" % e)
        return 1
    essayees = len(uniques)
    critere = texte_du_critere(conditions)
    print("CRITÈRE DU TRI : %s · %s · lu dans %s · sur la PARTIE DE RÉGLAGE seule (frontière %s)"
          % (critere, statut, source, par_fichier[0][0]["frontiere_70_30"]))
    if statut == STATUT_PROVISOIRE:
        print("  ⚠ CE SEUIL EST PROVISOIRE — %s (A-541 : « c'est Jean-Luc qui le fixe »)" % STATUT_PROVISOIRE)
    if doublons:
        print("  %d version(s) en double (mêmes réglages sous un autre essai ou identifiant) : comptée(s) une fois"
              % doublons)
    gardees, non_mesurables, zero = [], 0, 0
    for l in uniques:
        passe, nm = passe_le_critere(l, conditions)
        non_mesurables += nm
        zero += int(l["operations_70"]) == 0
        if passe:
            gardees.append(l)
    champs = list(contrat.RESULTATS_DES_VERSIONS) + AJOUTS
    provisoire = f_out + ".en_cours"
    cree = False
    try:
        with open(provisoire, "x", encoding="utf-8", newline="") as s:
            cree = True
            w = csv.DictWriter(s, fieldnames=champs)
            w.writeheader()
            for l in gardees:
                w.writerow(dict({c: l.get(c, "") for c in contrat.RESULTATS_DES_VERSIONS},
                                variantes_essayees=essayees, essais_comptes="+".join(essais),
                                critere_du_tri=critere, statut_du_critere=statut))
    except BaseException:
        if cree and os.path.exists(provisoire):
            os.remove(provisoire)
        raise
    os.replace(provisoire, f_out)
    print("VERSIONS ESSAYÉES : %d (%s, essais %s) · RETENUES : %d · ÉCARTÉES : %d, dont %d non mesurables"
          " · versions sans opération dans la partie de réglage : %d"
          % (essayees, strategies.pop(), "+".join(essais), len(gardees), essayees - len(gardees), non_mesurables,
             zero))
    print("ÉCRIT : %s" % f_out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
