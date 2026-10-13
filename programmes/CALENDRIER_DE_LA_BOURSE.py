"""CALENDRIER DE LA BOURSE — dire si un jour est un jour de bourse à Paris, et quelle séance on attend.

① RÔLE — Donner au circuit du soir la connaissance des jours fériés de la Bourse de Paris,
  que seules les boucles Cowork avaient jusqu'ici, écrite dans leur texte. Sans elle, un
  programme ne distingue pas « pas de séance aujourd'hui, c'est férié » de « la séance du
  jour manque ».
② CONTEXTE D'APPEL — Importé par programmes/MESSAGE_DU_SOIR.py, qui dit chaque soir sur
  le téléphone de Jean-Luc si la séance attendue a été lue. Lancé seul, il affiche le
  calendrier lu et le jour de bourse attendu ce soir, pour vérification.
③ ENTRÉE — Le fichier donnees/CALENDRIER_EURONEXT.csv du dépôt, colonnes déclarées au
  contrat CALENDRIER de programmes/CONTRATS_DES_FICHIERS.py : `date` (AAAA-MM-JJ),
  `etat` (FERME, DEMI_SEANCE, COUVERT_DEPUIS, COUVERT_JUSQU_AU), `source`.
④ CONDITIONS D'ENTRÉE — Le fichier porte exactement une ligne COUVERT_DEPUIS et une ligne
  COUVERT_JUSQU_AU ; toute autre forme est refusée (ValueError), jamais devinée.
⑤ SORTIE — Voir chaque fonction.
⑥ TRAITEMENT — lire le fichier, le confronter au contrat, puis répondre aux questions :
  ce jour est-il un jour de bourse ? quel est le dernier jour de bourse jusqu'à tel jour ?
  combien de jours de bourse entre deux dates ?
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
    ici = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("contrats_cal", os.path.join(ici, "CONTRATS_DES_FICHIERS.py"))
    contrats = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(contrats)
    with open(os.path.join(racine, FICHIER), encoding="utf-8-sig", newline="") as f:
        lignes = list(csv.reader(f))
    if not lignes or lignes[0] != list(contrats.CALENDRIER):
        raise ValueError(f"en-tête {lignes[0] if lignes else 'absent'} au lieu du contrat {contrats.CALENDRIER}")
    fermes, depuis, jusqu_au, jours = set(), [], [], {}
    for n, l in enumerate(lignes[1:], start=2):
        if not l:
            continue
        if len(l) != 3:
            raise ValueError(f"ligne {n} : {len(l)} colonnes au lieu de 3")
        try:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", l[0]):
                raise ValueError
            d = date.fromisoformat(l[0])
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
