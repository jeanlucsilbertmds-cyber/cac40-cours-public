"""CALENDRIER DE LA BOURSE — dire si un jour est un jour de bourse à Paris, et quelle séance on attend.

① RÔLE — Donner au circuit du soir la connaissance des jours fériés de la Bourse de Paris,
  que seules les boucles Cowork avaient jusqu'ici, écrite dans leur texte. Sans elle, un
  programme ne distingue pas « pas de séance aujourd'hui, c'est férié » de « la séance du
  jour manque ». Depuis le 10-10-2026, aussi LE CALENDRIER DES SÉANCES de R-110 : dans le
  passé, une séance est un jour où l'indice CAC 40 est publié ; pour l'avenir, la liste
  d'Euronext (`lire_les_seances`, `etat_du_jour`, `seances_entre`).
② CONTEXTE D'APPEL — Importé par programmes/MESSAGE_DU_SOIR.py, qui dit chaque soir sur
  le téléphone de Jean-Luc si la séance attendue a été lue. Lancé seul, il affiche le
  calendrier lu et le jour de bourse attendu ce soir, pour vérification. Le calendrier des
  séances est lu par programmes/LIRE_LES_COURS.py (R-111), une fois par lecture des cours.
③ ENTRÉE — Le fichier donnees/CALENDRIER_EURONEXT.csv du dépôt, colonnes déclarées au
  contrat CALENDRIER de programmes/CONTRATS_DES_FICHIERS.py : `date` (AAAA-MM-JJ),
  `etat` (FERME, DEMI_SEANCE, COUVERT_DEPUIS, COUVERT_JUSQU_AU), puis `source`, `citation`,
  `fichiers_cites` — les trois colonnes d'un fichier écrit à la main (depuis le 27-10-2026,
  pour la provenance des 20 ans, K23 ; ce programme ne les lit pas). Pour le
  calendrier des séances, aussi donnees/sources_indice/INDICE_CAC40.csv, contrat
  INDICE_CAC40 : `date`, `bnains`, `yahoo` (une clôture de l'indice par source).
④ CONDITIONS D'ENTRÉE — Le fichier porte exactement une ligne COUVERT_DEPUIS et une ligne
  COUVERT_JUSQU_AU ; toute autre forme est refusée (ValueError), jamais devinée.
⑤ SORTIE — Voir chaque fonction.
⑥ TRAITEMENT — lire le fichier, le confronter au contrat, puis répondre aux questions :
  ce jour est-il un jour de bourse ? quel est le dernier jour de bourse jusqu'à tel jour ?
  combien de jours de bourse entre deux dates ? Pour le calendrier des séances : lire
  l'indice, relever ses désaccords avec la liste d'Euronext, puis dire de chaque jour s'il
  est une séance CONSTATÉE (indice publié), PRÉVUE (annoncée par Euronext) ou FERMÉE.
⑦ UNITÉ — Des jours du calendrier de Paris (dates AAAA-MM-JJ) ; des nombres de jours de
  bourse pour les écarts.
⑧ POURQUOI — Décision de Jean-Luc du 30-09-2026 (« 2 » à 22h32) : faire reprendre par
  GitHub les manques graves relevés dans le tableau des fonctions des tâches
  (rapports/TABLEAU_FONCTIONS_DES_TACHES_Mer_30-09-2026.md, lignes 10.10 et 10.12), en
  commençant par la séance manquante et les jours fériés. Règle : avant d'arrêter ce qui
  tourne, reprendre chacune de ses fonctions (R-758).
⑨ CE QUI CLOCHE — Le calendrier ne couvre que 2026 : au-delà du 31-12-2026, toute question
  lève une erreur « hors du calendrier ». C'est voulu (mieux vaut une alerte qu'un faux
  « jour de bourse ») ; le relevé de 2027 sur la page officielle d'Euronext reste à faire.
  Une fermeture exceptionnelle non annoncée (panne de la place) n'y figure jamais.
  L'indice n'est relevé par aucun programme du soir : il s'arrête au 02-10-2026 (relevé le
  10-10-2026) ; les séances d'après ne sont que PRÉVUES. La relecture hebdomadaire de la
  liste d'Euronext (R-110 ②) n'existe pas encore.
  POUR RELEVER UNE ANNÉE NOUVELLE, ÉTENDRE LE FICHIER, NE JAMAIS LE REMPLACER : un fichier
  qui commencerait un jour férié ferait lever la recherche de la dernière séance (voir
  `dernier_jour_de_bourse`).
⑩ EFFET — Aucun, sinon l'affichage quand il est lancé seul.
⑪ TERMINAISON — Rend la main ; lancé seul, sort par le code 0 si le calendrier se lit et
  couvre aujourd'hui, 1 sinon.
  [sort: oui]
"""
import csv
import importlib.util
import math
import os
import re
import sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

FICHIER = os.path.join("donnees", "CALENDRIER_EURONEXT.csv")
ETATS = ("FERME", "DEMI_SEANCE", "COUVERT_DEPUIS", "COUVERT_JUSQU_AU")


class HorsCalendrier(ValueError):
    """Signale une question posée sur un jour que le calendrier ne couvre pas.

    ① RÔLE — Distinguer « le calendrier ne sait pas » d'une autre erreur.
    ② CONTEXTE D'APPEL — Levée par `_verifier_couvert`, attrapée par les appelants.
    ③ ENTRÉE — Le message.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Ne rend rien : c'est une classe d'erreur.
      [rend: rien]
    ⑥ TRAITEMENT — —
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un jour hors couverture ne doit jamais passer pour un jour de bourse.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — —
      [sort: non]
    """


def _contrats():
    """Charge programmes/CONTRATS_DES_FICHIERS.py, posé à côté de ce module.

    ① RÔLE — Donner aux deux lectures de ce module (la liste d'Euronext, l'indice) le même contrat.
    ② CONTEXTE D'APPEL — `lire` et `lire_les_seances`, une fois par lecture.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — CONTRATS_DES_FICHIERS.py est dans le même dossier que ce module.
    ⑤ SORTIE — UNE valeur : le module des contrats.
      [rend: 1]
    ⑥ TRAITEMENT — l'importer par son chemin, sans toucher au chemin des imports.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Deux lectures, un seul chargement écrit (R-708 : deux implémentations d'une même chose
      divergent toujours). Écrit le 10-10-2026 en sortant ces lignes de `lire`, qui les portait seule.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute le fichier des contrats (des déclarations seulement).
    ⑪ TERMINAISON — Rend la main ou lève l'erreur d'import.
      [sort: non]
    """
    ici = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("contrats_cal", os.path.join(ici, "CONTRATS_DES_FICHIERS.py"))
    contrats = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(contrats)
    return contrats


def _date_stricte(texte):
    """Rend la date écrite AAAA-MM-JJ, et rien d'autre.

    ① RÔLE — La seule lecture de date de ce module.
    ② CONTEXTE D'APPEL — `lire`, une fois par ligne de la liste d'Euronext ; `lire_les_seances`, une fois par ligne de
      l'indice ; programmes/LIRE_LES_COURS.py, une fois par ligne de cours.
    ③ ENTRÉE — `texte` : la case lue.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la date ; lève ValueError pour toute autre forme.
      [rend: 1]
    ⑥ TRAITEMENT — exiger la forme, puis la convertir.
    ⑦ UNITÉ — Une date.
    ⑧ POURQUOI — Relecture indépendante du 30-09-2026 : « 20260501 » et « 2026-W18-5 » passaient pour des dates, parce
      que `date.fromisoformat` les accepte. Sortie de `lire` le 10-10-2026 pour servir aussi à l'indice et aux cours :
      deux implémentations d'une même chose divergent toujours (R-708).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", texte):
        raise ValueError(texte)
    return date.fromisoformat(texte)


def lire(racine):
    """Lit le calendrier du dépôt et le rend sous une forme prête à interroger.

    ① RÔLE — Charger donnees/CALENDRIER_EURONEXT.csv une fois, en le confrontant au contrat.
    ② CONTEXTE D'APPEL — Appelée par programmes/MESSAGE_DU_SOIR.py une fois par message,
      et par `main`.
    ③ ENTRÉE — `racine` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe (une marque d'ordre d'octets en tête, que
      laisse Excel, est tolérée) ; son en-tête est exactement le contrat CALENDRIER ;
      chaque date s'écrit AAAA-MM-JJ, et rien d'autre ; chaque état est connu ; il y a une
      seule borne COUVERT_DEPUIS et une seule COUVERT_JUSQU_AU, la première au plus tard la
      seconde, dans n'importe quel ordre de lignes ; un jour FERME ou DEMI_SEANCE tombe
      entre les bornes, un lundi à vendredi, et n'est écrit qu'une fois.
    ⑤ SORTIE — UNE valeur : un dictionnaire {"fermes": ensemble de dates, "depuis": date,
      "jusqu_au": date}. Lève OSError si le fichier manque, ValueError s'il est mal formé,
      et toute erreur d'import du module des contrats (par exemple AttributeError s'il ne
      porte pas le contrat CALENDRIER).
      [rend: 1]
    ⑥ TRAITEMENT — ① charger le contrat · ② lire l'en-tête et le confronter · ③ lire
      chaque ligne · ④ vérifier les bornes · ⑤ vérifier chaque jour déclaré.
    ⑦ UNITÉ — Des dates.
    ⑧ POURQUOI — Un calendrier mal formé doit arrêter la lecture, jamais la fausser. Une
      fermeture un samedi, hors des bornes ou écrite deux fois trahit une faute de frappe
      (une mauvaise année, un mauvais mois) : elle est refusée plutôt que tue. Relecture
      indépendante du 30-09-2026 : « 20260501 » et « 2026-W18-5 » passaient pour des dates.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    contrats = _contrats()
    with open(os.path.join(racine, FICHIER), encoding="utf-8-sig", newline="") as f:
        lignes = list(csv.reader(f))
    if not lignes or lignes[0] != list(contrats.CALENDRIER):
        raise ValueError(f"en-tête {lignes[0] if lignes else 'absent'} au lieu du contrat {contrats.CALENDRIER}")
    fermes, depuis, jusqu_au, jours = set(), [], [], {}
    for n, l in enumerate(lignes[1:], start=2):
        if not l:
            continue
        if len(l) != len(contrats.CALENDRIER):   # le nombre vient du contrat, jamais écrit ici (R-708)
            raise ValueError(f"ligne {n} : {len(l)} colonnes au lieu de {len(contrats.CALENDRIER)}")
        try:
            d = _date_stricte(l[0])
        except ValueError:
            raise ValueError(f"ligne {n} : date illisible « {l[0]} »")
        if l[1] not in ETATS:
            raise ValueError(f"ligne {n} : état inconnu « {l[1]} »")
        if l[1] == "COUVERT_DEPUIS":
            depuis.append(d)
        elif l[1] == "COUVERT_JUSQU_AU":
            jusqu_au.append(d)
        else:
            if d in jours:
                raise ValueError(f"ligne {n} : le {l[0]} est déjà déclaré {jours[d]}")
            jours[d] = l[1]
            if l[1] == "FERME":
                fermes.add(d)
    if len(depuis) != 1 or len(jusqu_au) != 1 or depuis[0] > jusqu_au[0]:
        raise ValueError(f"bornes de couverture invalides : depuis {depuis}, jusqu'au {jusqu_au}")
    for d, etat in sorted(jours.items()):
        if not depuis[0] <= d <= jusqu_au[0]:
            raise ValueError(f"le {d.isoformat()} ({etat}) sort des bornes du calendrier")
        if d.weekday() >= 5:
            raise ValueError(f"le {d.isoformat()} ({etat}) tombe un week-end")
    return {"fermes": fermes, "depuis": depuis[0], "jusqu_au": jusqu_au[0]}


def _verifier_couvert(jour, cal):
    """Lève HorsCalendrier si `jour` sort de la couverture du calendrier.

    ① RÔLE — Garde commune des trois questions.
    ② CONTEXTE D'APPEL — `est_jour_de_bourse`.
    ③ ENTRÉE — `jour` : une date · `cal` : le rendu de `lire`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Ne rend rien : lève HorsCalendrier, ou rend la main.
      [rend: rien]
    ⑥ TRAITEMENT — comparer aux deux bornes.
    ⑦ UNITÉ — Des dates.
    ⑧ POURQUOI — Hors couverture, le calendrier ne sait pas : il le dit.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    if not (cal["depuis"] <= jour <= cal["jusqu_au"]):
        raise HorsCalendrier(f"le {jour.isoformat()} est hors du calendrier (couvert du "
                             f"{cal['depuis'].isoformat()} au {cal['jusqu_au'].isoformat()})")


def est_jour_de_bourse(jour, cal):
    """Dit si la Bourse de Paris tient séance ce jour-là.

    ① RÔLE — La question de base.
    ② CONTEXTE D'APPEL — `dernier_jour_de_bourse`, `jours_de_bourse_apres`, programmes/
      MESSAGE_DU_SOIR.py.
    ③ ENTRÉE — `jour` : une date · `cal` : le rendu de `lire`.
    ④ CONDITIONS D'ENTRÉE — `jour` dans la couverture, sinon HorsCalendrier.
    ⑤ SORTIE — UNE valeur : vrai du lundi au vendredi hors fermeture ; une demi-séance
      compte comme un jour de bourse.
      [rend: 1]
    ⑥ TRAITEMENT — couverture, puis week-end, puis fermetures.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La règle que les boucles appliquaient : samedis, dimanches et fermetures
      Euronext sautés ; les 24 et 31 décembre sont des jours de bourse.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    _verifier_couvert(jour, cal)
    return jour.weekday() < 5 and jour not in cal["fermes"]


def dernier_jour_de_bourse(jusqu_au_inclus, cal):
    """Rend le dernier jour de bourse qui tombe au plus tard le jour donné.

    ① RÔLE — Dire quelle séance on attend.
    ② CONTEXTE D'APPEL — programmes/MESSAGE_DU_SOIR.py, avec le jour même (la séance
      attendue) et avec la veille (la séance qui suffit tant que le circuit du soir n'est
      pas passé).
    ③ ENTRÉE — `jusqu_au_inclus` : une date · `cal` : le rendu de `lire`.
    ④ CONDITIONS D'ENTRÉE — Tous les jours parcourus doivent être couverts.
    ⑤ SORTIE — UNE valeur : une date.
      [rend: 1]
    ⑥ TRAITEMENT — reculer jour par jour jusqu'à un jour de bourse.
    ⑦ UNITÉ — Des dates.
    ⑧ POURQUOI — Un lundi, on attend le lundi ; un samedi, le vendredi ; un 25-12, le 24.
    ⑨ CE QUI CLOCHE — Si la couverture commence un jour sans bourse (le 01-01, férié),
      reculer depuis ce jour-là franchit la borne basse et lève HorsCalendrier, alors que
      le calendrier est juste : le message du soir le dirait illisible. D'où la règle du
      fichier : pour relever une année nouvelle, ÉTENDRE le fichier (déplacer la borne
      COUVERT_JUSQU_AU et ajouter les jours), ne jamais le REMPLACER (relecture
      indépendante du 30-09-2026, preuve sur un fichier 2027 seul).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève ; la boucle recule d'un jour à chaque tour et
      s'arrête au plus tard au jour qui précède la borne basse, où `est_jour_de_bourse`
      lève HorsCalendrier.
      [sort: non]
    """
    d = jusqu_au_inclus
    while not est_jour_de_bourse(d, cal):
        d -= timedelta(days=1)
    return d


def jours_de_bourse_apres(apres, jusqu_au_inclus, cal):
    """Compte les jours de bourse strictement après `apres`, jusqu'à `jusqu_au_inclus` compris.

    ① RÔLE — Dire de combien de séances on est en retard.
    ② CONTEXTE D'APPEL — programmes/MESSAGE_DU_SOIR.py.
    ③ ENTRÉE — `apres` : la date de départ, exclue · `jusqu_au_inclus` : la date d'arrivée,
      comprise · `cal` : le rendu de `lire`.
    ④ CONDITIONS D'ENTRÉE — Les jours parcourus sont couverts.
    ⑤ SORTIE — UNE valeur : un entier, zéro si `apres` n'est pas antérieur.
      [rend: 1]
    ⑥ TRAITEMENT — compter jour par jour.
    ⑦ UNITÉ — Des JOURS DE BOURSE.
    ⑧ POURQUOI — « 2 jours de bourse de retard » dit plus que « 4 jours » sur un week-end.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    n, d = 0, apres + timedelta(days=1)
    while d <= jusqu_au_inclus:
        n += est_jour_de_bourse(d, cal)
        d += timedelta(days=1)
    return n


# ─────────────────────────────────────────────────────────────────────────
# LE CALENDRIER DES SÉANCES (R-110, décision de Jean-Luc du 10-10-2026)
# Dans le passé, une séance est un jour où l'indice CAC 40 est publié ; pour l'avenir,
# la liste d'Euronext. Jamais les cours eux-mêmes : une séance qui manque pour toutes
# les valeurs à la fois passerait pour un jour de fermeture.
# ─────────────────────────────────────────────────────────────────────────
INDICE = os.path.join("donnees", "sources_indice", "INDICE_CAC40.csv")
CONSTATEE, PREVUE, FERMEE = "CONSTATÉE", "PRÉVUE", "FERMÉE"


def lire_les_seances(racine):
    """Lit l'indice CAC 40 et la liste d'Euronext, et rend le calendrier des séances.

    ① RÔLE — Construire le calendrier des séances de R-110 : le passé lu dans l'indice CAC 40, l'avenir dans la
      liste d'Euronext, et chaque désaccord entre les deux relevé comme une alerte.
    ② CONTEXTE D'APPEL — programmes/LIRE_LES_COURS.py, une fois par lecture des cours ; `main`.
    ③ ENTRÉE — `racine` : la racine du dépôt, qui porte donnees/sources_indice/INDICE_CAC40.csv (contrat INDICE_CAC40 :
      date, bnains, yahoo) et donnees/CALENDRIER_EURONEXT.csv (lu par `lire`).
    ④ CONDITIONS D'ENTRÉE — Les deux fichiers existent. L'en-tête de l'indice est exactement le contrat ; chaque date
      s'écrit AAAA-MM-JJ et n'apparaît qu'une fois ; chaque ligne porte au moins un cours de l'indice, positif, et aucun
      cours infini ou indéfini (« inf », « nan ») ; aucune ligne ne tombe un samedi, un dimanche, ni après aujourd'hui
      (heure de Paris) : un indice ne se publie pas d'avance. Toute autre forme est refusée (ValueError), jamais devinée.
    ⑤ SORTIE — UNE valeur : un dictionnaire {"indice": ensemble des dates où l'indice est publié, "debut": la première,
      "fin": la dernière, "euronext": le rendu de `lire`, "alertes": liste de textes}. Exemple mesuré le 10-10-2026 :
      6 844 dates, du 03-01-2000 au 02-10-2026, aucune alerte.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire la liste d'Euronext · ② lire l'indice et le confronter au contrat, ligne à ligne · ③ relever
      chaque jour qu'Euronext déclare fermé et où l'indice est publié · ④ relever chaque jour de semaine qu'Euronext
      n'annonce pas fermé, couvert par les deux fichiers, où l'indice manque.
    ⑦ UNITÉ — Des dates.
    ⑧ POURQUOI — R-110 ① et ③. Les deux désaccords sont des alertes, pas des refus : R-109 veut que tout problème soit
      signalé, et l'indice d'un jour suffit à dire que la Bourse était ouverte. Exemple réel : l'indice est publié le
      24-12-2010, le 31-12-2010, le 24-12-2012, le 31-12-2012 et le 31-12-2015 ; aucune valeur n'a de cours ces jours-là
      dans l'historique réparé, et aucun contrôle ne le voyait parce que le calendrier venait des cours. Relecture
      indépendante du 10-10-2026 : un cours « inf » et une date à venir passaient ; ils sont refusés.
    ⑨ CE QUI CLOCHE — L'indice n'est relevé par aucun programme du soir : le fichier s'arrête au 02-10-2026 (relevé le
      10-10-2026), et toute séance d'après n'est que PRÉVUE par la liste d'Euronext, sans constat (R-110 ③ pas encore
      vrai). · Avant 2026, la liste d'Euronext n'existe pas : un jour sans indice y est un jour fermé, sans seconde
      source ; les 12-06-2000, 14-07-2000, 04-06-2001 et 31-12-2001, jours de semaine sans indice hors des fériés
      habituels, sont donc des fermetures, ce que personne n'a vérifié sur un avis d'Euronext.
    ⑩ EFFET — Lit deux fichiers et l'horloge.
    ⑪ TERMINAISON — Rend la main ou lève ; un passage sur chaque fichier, une boucle bornée par les dates couvertes.
      [sort: non]
    """
    contrats = _contrats()
    euronext = lire(racine)
    aujourd_hui = datetime.now(ZoneInfo("Europe/Paris")).date()
    with open(os.path.join(racine, INDICE), encoding="utf-8-sig", newline="") as f:
        lignes = list(csv.reader(f))
    if not lignes or lignes[0] != list(contrats.INDICE_CAC40):
        raise ValueError(f"indice : en-tête {lignes[0] if lignes else 'absent'} au lieu du contrat {contrats.INDICE_CAC40}")
    jours = set()
    for n, l in enumerate(lignes[1:], start=2):
        if not l:
            continue
        if len(l) != len(contrats.INDICE_CAC40):
            raise ValueError(f"indice, ligne {n} : {len(l)} colonnes")
        try:
            d = _date_stricte(l[0])
        except ValueError:
            raise ValueError(f"indice, ligne {n} : date illisible « {l[0]} »")
        if d in jours:
            raise ValueError(f"indice, ligne {n} : le {l[0]} est écrit deux fois")
        if d.weekday() in (5, 6):
            raise ValueError(f"indice, ligne {n} : le {l[0]} tombe un week-end")
        cours = []
        for x in l[1:]:
            try:
                cours.append(float(x) if x.strip() else None)
            except ValueError:
                raise ValueError(f"indice, ligne {n} : cours illisible « {x} »")
        if not any(c is not None and c > 0 for c in cours):
            raise ValueError(f"indice, ligne {n} : aucun cours positif le {l[0]}")
        if not all(c is None or math.isfinite(c) for c in cours):
            raise ValueError(f"indice, ligne {n} : cours infini ou indéfini le {l[0]}")
        if d > aujourd_hui:
            raise ValueError(f"indice, ligne {n} : le {l[0]} est après aujourd'hui ({aujourd_hui.isoformat()})")
        jours.add(d)
    if not jours:
        raise ValueError("indice : aucune séance")
    debut, fin = min(jours), max(jours)
    alertes = []
    for d in sorted(euronext["fermes"]):
        if d in jours:
            alertes.append(f"le {d.isoformat()} : l'indice est publié, Euronext déclarait la Bourse fermée")
    d = max(debut, euronext["depuis"])
    while d <= min(fin, euronext["jusqu_au"]):
        if d.weekday() < 5 and d not in euronext["fermes"] and d not in jours:
            alertes.append(f"le {d.isoformat()} : Euronext annonçait une séance, l'indice manque (séance gardée, R-110 ③)")
        d += timedelta(days=1)
    return {"indice": jours, "debut": debut, "fin": fin, "euronext": euronext, "alertes": alertes}


def etat_du_jour(jour, sc):
    """Dit si un jour est une séance constatée, une séance prévue, ou un jour fermé.

    ① RÔLE — La question de base du calendrier des séances.
    ② CONTEXTE D'APPEL — `seances_entre` ; programmes/LIRE_LES_COURS.py, une fois par barre lue.
    ③ ENTRÉE — `jour` : une date · `sc` : le rendu de `lire_les_seances`.
    ④ CONDITIONS D'ENTRÉE — `jour` couvert : dans la période de l'indice, ou dans celle de la liste d'Euronext ; sinon
      HorsCalendrier.
    ⑤ SORTIE — UNE valeur : CONSTATÉE (l'indice est publié), PRÉVUE (pas d'indice, la liste d'Euronext annonce une
      séance) ou FERMÉE.
      [rend: 1]
    ⑥ TRAITEMENT — ① indice publié : CONSTATÉE · ② jour dans la liste d'Euronext : PRÉVUE si elle annonce une séance,
      FERMÉE sinon · ③ jour dans la période de l'indice, hors liste d'Euronext : FERMÉE · ④ sinon HorsCalendrier.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-110 : l'indice tranche quand il est publié ; son absence seule ne ferme jamais la Bourse quand
      Euronext annonçait une séance. Exemples réels : 02-10-2026 CONSTATÉE ; 09-10-2026 PRÉVUE (l'indice s'arrête au
      02-10) ; 25-12-2015 FERMÉE (aucun indice, avant la liste d'Euronext).
    ⑨ CE QUI CLOCHE — Un jour couvert par l'indice ET la liste d'Euronext, où l'indice manque alors qu'Euronext annonçait
      une séance, rend PRÉVUE : c'est une séance sans constat, que `lire_les_seances` relève en alerte.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    if jour in sc["indice"]:
        return CONSTATEE
    eu = sc["euronext"]
    if eu["depuis"] <= jour <= eu["jusqu_au"]:
        return PREVUE if est_jour_de_bourse(jour, eu) else FERMEE
    if sc["debut"] <= jour <= sc["fin"]:
        return FERMEE
    raise HorsCalendrier(f"le {jour.isoformat()} est hors du calendrier des séances (indice du {sc['debut'].isoformat()} "
                         f"au {sc['fin'].isoformat()}, Euronext du {eu['depuis'].isoformat()} au {eu['jusqu_au'].isoformat()})")


def seances_entre(debut, fin, sc):
    """Rend les séances du calendrier entre deux dates, bornes comprises.

    ① RÔLE — Donner la suite des séances sur laquelle on compte, au lieu des lignes d'un fichier de cours.
    ② CONTEXTE D'APPEL — programmes/LIRE_LES_COURS.py ; `main`.
    ③ ENTRÉE — `debut`, `fin` : deux dates · `sc` : le rendu de `lire_les_seances`.
    ④ CONDITIONS D'ENTRÉE — Chaque jour entre les deux dates est couvert, sinon HorsCalendrier.
    ⑤ SORTIE — UNE valeur : la liste, dans l'ordre, des couples (date, CONSTATÉE ou PRÉVUE) ; vide si `debut` est
      après `fin`.
      [rend: 1]
    ⑥ TRAITEMENT — parcourir jour par jour, garder ce qui n'est pas FERMÉE.
    ⑦ UNITÉ — Des SÉANCES.
    ⑧ POURQUOI — R-111 ② : compter en séances du calendrier, jamais en lignes. Exemple mesuré le 10-10-2026 : du
      20-12-2010 au 31-12-2010, dix séances, dont le 24 et le 31 que les cours ne montrent pas.
    ⑨ CE QUI CLOCHE — Un jour à la fois : sur vingt-six ans, environ 9 700 tours, sans gêne mesurée.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ou lève ; la boucle avance d'un jour à chaque tour jusqu'à `fin`.
      [sort: non]
    """
    out, d = [], debut
    while d <= fin:
        e = etat_du_jour(d, sc)
        if e != FERMEE:
            out.append((d, e))
        d += timedelta(days=1)
    return out


def main():
    """Affiche le calendrier lu et le jour de bourse attendu aujourd'hui.

    ① RÔLE — Vérification à la main.
    ② CONTEXTE D'APPEL — La ligne de commande : python3 programmes/CALENDRIER_DE_LA_BOURSE.py [racine].
    ③ ENTRÉE — `sys.argv[1]`, la racine du dépôt ; à défaut, le dossier courant.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Ne rend rien : sort par sys.exit.
      [rend: rien]
    ⑥ TRAITEMENT — lire, afficher, sortir.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un calendrier illisible doit se voir (R-734 : un contrôle qui n'a pas pu
      tourner rend un code non nul).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — sys.exit(0) si le calendrier se lit ET couvre aujourd'hui ; 1 sinon
      (la ligne des bornes a pu s'afficher avant l'erreur de couverture).
      [sort: oui]
    """
    racine = sys.argv[1] if len(sys.argv) > 1 else "."
    try:
        cal = lire(racine)
        auj = datetime.now(ZoneInfo("Europe/Paris")).date()
        print(f"couvert du {cal['depuis']} au {cal['jusqu_au']} · {len(cal['fermes'])} fermeture(s) : "
              + ", ".join(sorted(x.isoformat() for x in cal["fermes"])))
        print(f"aujourd'hui {auj} : {'jour de bourse' if est_jour_de_bourse(auj, cal) else 'pas de séance'}"
              f" · dernier jour de bourse : {dernier_jour_de_bourse(auj, cal)}")
    except (OSError, ValueError) as e:
        print(f"CALENDRIER INUTILISABLE : {e}")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
