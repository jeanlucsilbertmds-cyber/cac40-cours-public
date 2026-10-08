#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COLLECTER_ABC_GITHUB.py — Jeu 10-09-2026 (Paris)
FABRIQUÉ · Rôle : tourner sur une machine GitHub Actions, télécharger la page brute
d'ABC Bourse pour chaque valeur du référentiel, extraire le tableau des cours par
des règles fixes sur le HTML, et EMPILER les séances nouvelles dans le fichier des
cours — après contrôle de vraisemblance, jamais d'écrasement.

POURQUOI SUR GITHUB ET PAS DANS UNE TÂCHE CLAUDE (décision de Jean-Luc, 10-09-2026) :
  · le réseau Python d'une tâche Claude est fermé (403, organization policy) ;
  · l'outil web d'une tâche ne rend pas la page mais un résumé écrit par un modèle,
    dont la forme varie avec le prompt, dont l'horodatage peut mentir, et qui peut
    glisser un chiffre dans un volume (mesuré par Cowork le 10-09) ;
  · une machine GitHub Actions a le réseau ouvert et rend la page BRUTE — 70 236
    octets, 399 cellules <td>, mesuré le 10-09 à 20h03. Aucun modèle entre la page
    et ce programme. Même page, même résultat, toujours.

LA STRUCTURE HTML, RELEVÉE LE 10-09 À 20h09 SUR LA VRAIE PAGE — pas supposée :
  <tr> <th>Date</th> <th>Ouverture</th> <th>Plus Haut</th> <th>Plus Bas</th>
       <th>Volume</th> <th>Dernier</th> <th>Variation</th> </tr>
  <tr> <td data-name="10/09/2026" ...>10/09/2026</td> <td class="mobno">78,80</td>
       <td>79,22</td> <td>78,16</td> <td>3&#xA0;502&#xA0;416</td>
       <td class="bold">78,38</td> <td><span ...>0,22%</span></td> </tr>
  Sept cellules. Volume avec &#xA0; (espace insécable) pour les milliers.

CE QUE CE PROGRAMME DÉLÈGUE — deux implémentations d'une même chose divergent toujours (R-708) : normalisation, vraisemblance, dédoublonnage et
écriture viennent de CONTROLER_LES_COURS.py. Son seul rôle : télécharger, extraire.

CODE ABC = mnémonique Euronext + 'p' (Paris) ou 'n' (Amsterdam) — vérifié 11/11.

FRAÎCHEUR : la ligne du jour est finale après 17h55 Paris (mesuré). Ce programme
tourne à 19h Paris : la ligne du jour est acceptée pour Paris. Pour Amsterdam, la
ligne la plus récente est ÉCARTÉE (partielle, mesurée le 10-09).

════════════════════════════════════════════════════════════════════════
LES ONZE ÉLÉMENTS — ce programme est une fonction comme les autres
════════════════════════════════════════════════════════════════════════
① RÔLE — **LE PAS N°1 DU CIRCUIT DU SOIR.** Tout le reste en dépend : sans
  cours neufs, le détecteur calcule sur la veille et tout reste vert.
② CONTEXTE D APPEL — Le circuit du soir, en tout premier, après la clôture.
  **Une séance non lue le jour même perd ses signaux pour toujours : les cours
  se rattrapent, les signaux ne se calculent que sur la dernière séance.**
③ ENTRÉE — La ligne de commande : la racine du dépôt. **Et deux fichiers** : le
  référentiel des valeurs, et le fichier d arrivée déjà écrit, relu pour savoir
  où chaque valeur s était arrêtée. **Et quarante pages web.**
④ CONDITIONS D ENTRÉE — Un argument, un référentiel, et le module de contrôle
  des cours. **Le fichier d arrivée peut ne pas exister : c est le premier soir.**
⑤ SORTIE — **Un code de sortie, un rapport affiché, et deux fichiers écrits.**
⑥ TRAITEMENT — ① charger le contrôleur et le référentiel · ② relire le fichier
  d arrivée pour connaître la dernière séance de chaque valeur · ③ pour chaque
  valeur : télécharger, extraire, **écarter la séance du jour si la place n a pas
  encore clôturé**, ne garder que ce qui est plus récent · ④ soumettre le LOT
  ENTIER au contrôle de vraisemblance · ⑤ n écrire que ce qui passe.
⑦ UNITÉ — Prix en euros, volume en titres, dates au format AAAA-MM-JJ.
  **L heure de clôture est une heure de Paris ; la pause entre pages est en
  secondes ; l écart maximal entre deux séances est en jours.**
⑧ POURQUOI — **Le nom écrit est le nom NORMALISÉ** : le 10-09-2026, le programme
  écrivait « BUREAU VERITAS » quand le fichier portait « BUREAU_VERITAS » — deux
  noms pour une valeur. **Et le lot entier passe le contrôle avant écriture** :
  un lot bloquant n écrit rien, plutôt que d écrire la moitié.
⑨ CE QUI CLOCHE — **Quatre silences, aucun corrigé** — le ⑨ se consigne et ne se corrige pas (R-752) :
  · **une colonne `hors_univers` ABSENTE et une colonne VIDE donnent le même
    résultat** — un référentiel qui perdrait cette colonne ramènerait
    silencieusement tout l univers, y compris ce que Jean-Luc en avait retiré ;
  · **le rapport porte le jour dans son nom** — deux exécutions le même jour
    écrasent le premier sans un mot, et la première peut avoir échoué pour une
    raison que la seconde efface ;
  · **la forme de la page est une SUPPOSITION** : sept cellules, un titre, une
    date en première colonne. Une colonne de plus chez ABC et tout est ignoré ;
  · **le délai réseau et l annonce du navigateur sont en dur**, et ne sont
    déclarés nulle part.
      ⑩ EFFET — **AJOUTE au fichier `donnees/claude_cours_nouveaux.csv`** — il n est
  pas réécrit, il grandit · **crée `rapports/` s il manque et y écrit le rapport
  du jour, en l écrasant s il existe** · **SORT SUR LE RÉSEAU quarante fois** ·
  modifie le chemin de recherche des modules.
      ⑪ TERMINAISON — **NE REND JAMAIS LA MAIN : trois codes.** `0` tout est collecté ·
  `1` au moins une valeur en échec, le reste est écrit · `2` aucun argument,
  module introuvable, référentiel absent, ou **lot bloquant — rien écrit**.
  **Et `lire_referentiel`, appelée avant toute descente sur le réseau, peut
  terminer en code 2 sans revenir.**

USAGE : python3 COLLECTER_ABC_GITHUB.py <racine_du_depot>
  lit  donnees/REFERENTIEL_VALEURS_*.csv et donnees/claude_cours_nouveaux.csv
  écrit donnees/claude_cours_nouveaux.csv (empile) et rapports/collecte_abc_<date>.md

CODE DE SORTIE : 0 = tout lu · 1 = au moins une valeur en échec · 2 = lot bloquant
ou contrôle impossible. Le workflow commite dans tous les cas où quelque chose a
été écrit, et échoue bruyamment sinon.

      ⑫ DÉFINITIONS —
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub
    Actions — collecte, versement, signaux, positions, mesure, surveillance.
  Cowork : le relecteur du projet, qui clone le dépôt, casse le code et rend ses cassures par écrit
  l'outil web : l'outil d'une tâche planifiée Cowork qui ouvre une page et en rend un texte écrit par un modèle, jamais la page elle-même.
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
  le détecteur : programmes/DETECTER_LES_SIGNAUX_GITHUB.py, qui écrit les signaux du jour
  le référentiel : donnees/REFERENTIEL_VALEURS_*.csv, la liste des valeurs à suivre, avec pour chacune son mnémonique et sa place de cotation.
  un lot BLOQUANT : un ensemble de séances dont l'une est jugée fausse, ce qui fait refuser l'écriture de tout l'ensemble.
  une séance : une journée de bourse pour une valeur, avec son ouverture, son plus haut, son plus bas, sa clôture et son volume.
  une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""

import sys, os, re, csv, html, time
import urllib.request
from datetime import datetime, date
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")
DATE_PLANCHER = "2026-07-10"
PAUSE_ENTRE_PAGES = 1.5          # secondes — un visiteur, pas une rafale
HEURE_CLOTURE_PARIS = 18         # avant, la ligne du jour est partielle
ECART_MAX_JOURS = 6              # deux séances ne sont jamais espacées de plus (pont, fermeture)

_TR = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
_TD = re.compile(r"<td[^>]*>(.*?)</td>", re.S)
_TAG = re.compile(r"<[^>]+>")


def _texte(cellule):
    """Texte d'une cellule : balises retirées, entités décodées, espaces normalisés.

    ① RÔLE — Rendre lisible le contenu d une cellule de tableau HTML.
    ② CONTEXTE D APPEL — `extraire`, pour chaque cellule de chaque ligne du
      tableau des cours. Sur quarante valeurs et soixante séances, des milliers
      de fois par soirée.
    ③ ENTRÉE — `cellule` : le contenu brut d une cellule, balises comprises.
    ④ CONDITIONS D ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : le texte nettoyé.
      [rend: 1]
    ⑥ TRAITEMENT — ① retirer les balises · ② décoder les entités HTML ·
      ③ **remplacer les deux espaces insécables par des espaces ordinaires** ·
      ④ écraser les espaces multiples.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — **Les deux espaces insécables sont traités séparément parce
      qu ils sont INVISIBLES dans un affichage.** Une valeur numérique qui les
      porte échoue à la conversion sans qu on voie pourquoi.
    ⑨ CE QUI CLOCHE — Rien vu.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    t = _TAG.sub("", cellule)
    t = html.unescape(t).replace("\u00a0", " ").replace("\u202f", " ")
    return " ".join(t.split())


def _nombre(s):
    """Convertit un nombre écrit à la française en nombre calculable.

    ① RÔLE — Traduire « 1 234,56 » en 1234.56.
    ② CONTEXTE D APPEL — `extraire`, pour les cinq cellules chiffrées de chaque
      séance : ouverture, plus haut, plus bas, volume, clôture.
    ③ ENTRÉE — `s` : un nombre écrit à la française, déjà nettoyé par `_texte`.
    ④ CONDITIONS D ENTRÉE — **La chaîne DOIT être convertible.** Une chaîne qui
      ne l est pas fait lever, et `extraire` attrape la levée pour ignorer la
      ligne.
    ⑤ SORTIE — UNE valeur : le nombre.
      [rend: 1]
    ⑥ TRAITEMENT — ① retirer les espaces, qui séparent les milliers ·
      ② remplacer la virgule décimale par un point · ③ convertir.
    ⑦ UNITÉ — Celle de la cellule reçue : euros pour les prix, titres pour le
      volume. **La fonction ne le sait pas et ne peut pas le vérifier.**
    ⑧ POURQUOI — ABC Bourse sert ses chiffres à la française. **Convertir ici,
      une fois, évite que chaque appelant s en charge à sa façon.**
    ⑨ CE QUI CLOCHE — **DEUX SILENCES.**
      **① Elle lève DEUX types d erreur, pas un.** `ValueError` sur une chaîne
      non convertible — `_nombre('abc')` · et `AttributeError` sur `None` ou sur
      un nombre déjà converti — `_nombre(None)` rend « 'NoneType' object has no
      attribute 'replace' ». **`extraire` n attrape que le premier.** Le cas est
      dormant : `_texte` rend toujours une chaîne, donc `None` ne peut pas
      arriver depuis `extraire`. **Il deviendrait actif si un autre appelant
      passait autre chose.**
      **② Quand elle lève, `extraire` fait `except ValueError: continue` : la
      séance est ignorée, ET RIEN NE LE COMPTE.** Le motif rendu reste vide.
      **Mesuré sur une page à deux séances dont une porte un volume illisible :
      `extraire` rend UNE séance et un motif VIDE. L appelant ne peut pas savoir
      qu il en manque une.**
      **C est grave ici : une séance non lue le jour même perd ses signaux pour
      toujours — les cours se rattrapent, les signaux ne se calculent que sur la
      dernière séance.** Une séance qui disparaît sans compte ni motif est
      exactement ce que ce principe interdit.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — **PEUT LEVER** si la chaîne n est pas convertible.
      Rend la main sinon.
      [sort: non]
    """
    return float(s.replace(" ", "").replace(",", "."))


def extraire(page_html):
    """Rend les séances du tableau « Cours historiques », du plus récent au plus ancien.
    Règle : les lignes <tr> à SEPT cellules <td> dont la première est une date
    JJ/MM/AAAA, situées après le titre « Cours historiques ». Les dates doivent
    décroître strictement — sinon la ligne est ignorée et comptée.

    ① RÔLE — **Tirer les séances d une page HTML d ABC Bourse.** C est le seul
      endroit du programme qui comprend la forme de la page.
    ② CONTEXTE D APPEL — `main`, une fois par valeur, juste après le
      téléchargement.
    ③ ENTRÉE — `page_html` : la page brute telle que le serveur l a rendue.
    ④ CONDITIONS D ENTRÉE — Aucune. **Une page vide, tronquée ou refusée est un
      cas prévu : la fonction rend une liste vide et un motif.**
    ⑤ SORTIE — DEUX valeurs : les séances, du plus récent au plus ancien, **et un
      motif** — vide si tout s est bien passé. **Le motif est ce qui distingue
      « aucune séance nouvelle » de « la page a changé de forme ».**
      [rend: 2]
    ⑥ TRAITEMENT — ① trouver le titre du tableau · ② relever toutes les lignes à
      SEPT cellules dont la première est une date · ③ **refuser tout si le
      tableau est servi du plus ancien au plus récent** · ④ ne garder que le bloc
      contigu, strictement décroissant, avec un écart borné · ⑤ s arrêter à 60.
    ⑦ UNITÉ — Prix en euros, volume en titres, dates converties au format
      AAAA-MM-JJ.
    ⑧ POURQUOI — **Trois gardes protègent cette lecture, et chacun vient d un
      silence mesuré.** L ordre inversé rendait « sans séance nouvelle » sans
      rien dire · l écart borné coupe le tableau des dividendes, qui continuerait
      la décroissance · la borne est celle de l autre collecteur, un seul chiffre
      et pas deux.
    ⑨ CE QUI CLOCHE — **La forme de la page est une SUPPOSITION : sept cellules,
      un titre, une date en première colonne.** Si ABC en ajoute une, chaque
      ligne est ignorée et le motif dira « aucune ligne à sept cellules datée » —
      **exact, et il faut le lire pour comprendre que la page a changé.**
      **② UNE LIGNE À SEPT CELLULES DONT UNE CASE EST ILLISIBLE EST IGNORÉE SANS
      ÊTRE COMPTÉE.** Le `except ValueError: continue` la saute, et le motif
      rendu reste vide. **Ce n est pas le même cas que le précédent : la page a
      la bonne forme, c est une séance isolée qui disparaît.**
    ⑩ EFFET — Aucun : elle ne lit aucun fichier et n en écrit aucun.
    ⑪ TERMINAISON — Rend toujours la main. **`_nombre`, qu elle appelle, peut
      lever — la levée est attrapée et la ligne ignorée.**
      [sort: non]
    """
    i = page_html.find("Cours historiques")
    if i < 0:
        return [], "titre « Cours historiques » absent de la page"
    zone = page_html[i:]
    # ① toutes les lignes bien formées, dans l'ordre de la page
    brutes = []
    for tr in _TR.findall(zone):
        cells = [_texte(c) for c in _TD.findall(tr)]
        if len(cells) != 7:
            continue
        m = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", cells[0])
        if not m:
            continue
        try:
            d = date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
            brutes.append((d, {"date": d.isoformat(),
                               "open": _nombre(cells[1]), "high": _nombre(cells[2]),
                               "low": _nombre(cells[3]), "volume": int(_nombre(cells[4])),
                               "close": _nombre(cells[5])}))
        except ValueError:
            continue
    if not brutes:
        return [], "aucune ligne à sept cellules datée"
    # ② ORDRE INVERSÉ → ZÉRO, bruyant. Cowork, 10-09 : l'ancienne version gardait la
    # première ligne — la plus vieille, déjà au fichier — et rendait « sans séance
    # nouvelle » en silence. Servi du plus ancien au plus récent, on refuse tout.
    if len(brutes) >= 2 and brutes[0][0] < brutes[-1][0]:
        return [], f"tableau servi du plus ancien au plus récent ({len(brutes)} lignes) — refusé"
    # ③ LE BLOC DES COURS : contigu, strictement décroissant, ÉCART BORNÉ. Un tableau
    # plus bas — dividendes, événements — aux dates plus anciennes continuerait la
    # décroissance sans la borne ; l'écart de plusieurs semaines le coupe. Même borne
    # que COLLECTER_LES_COURS_ABC — un seul chiffre, jamais deux (R-708).
    seances, derniere = [], None
    for d, s in brutes:
        if derniere is not None and (d >= derniere or (derniere - d).days > ECART_MAX_JOURS):
            break
        derniere = d
        seances.append(s)
        if len(seances) >= 60:
            break
    return seances, ""


def telecharger(url):
    """Rend le contenu d une page web.

    ① RÔLE — Le seul point du programme qui sort sur le réseau.
    ② CONTEXTE D APPEL — `main`, une fois par valeur, dans une boucle espacée
      d une pause entre chaque appel.
    ③ ENTRÉE — `url` : l adresse de la page. Un seul appelant, et il construit
      toujours la même forme : l adresse de cotation d ABC Bourse suivie du code
      de la valeur.
    ④ CONDITIONS D ENTRÉE — Aucune. **Une adresse injoignable est un cas prévu :
      la levée remonte, et `main` compte la valeur en échec.**
    ⑤ SORTIE — UNE valeur : le texte de la page.
      [rend: 1]
    ⑥ TRAITEMENT — ① annoncer un navigateur ordinaire · ② appeler, avec un délai
      maximal · ③ décoder, en remplaçant les octets illisibles.
    ⑦ UNITÉ — Le délai maximal est en secondes.
    ⑧ POURQUOI — **Le décodage tolérant évite qu un seul octet abîmé fasse
      perdre toute la page** : les chiffres, eux, sont vérifiés plus loin.
    ⑨ CE QUI CLOCHE — **Le délai et l annonce du navigateur sont écrits en dur
      ici.** Les deux relèvent d un réglage, pas d un calcul — et ils ne sont
      déclarés nulle part.
    ⑩ EFFET — **SORT SUR LE RÉSEAU.** C est le seul effet du programme qui
      dépende de quelqu un d autre.
    ⑪ TERMINAISON — **PEUT LEVER** : réseau coupé, délai dépassé, page refusée.
      Rend la main sinon.
      [sort: non]
    """
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (collecte quotidienne, usage personnel)"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")


def lire_referentiel(racine):
    """Rend la liste des valeurs à collecter, ou arrête le programme.

    ① RÔLE — **Dire QUI collecter.** C est le seul endroit qui décide du
      périmètre de la soirée.
    ② CONTEXTE D APPEL — `main`, avant toute descente sur le réseau. **Si le
      périmètre est inconnu, rien ne doit être collecté.**
    ③ ENTRÉE — `racine` : le dossier du dépôt. Un seul appelant, qui passe la
      valeur reçue en ligne de commande.
    ④ CONDITIONS D ENTRÉE — **`donnees/` doit contenir au moins un référentiel.**
      C est la seule vraie condition du programme.
    ⑤ SORTIE — DEUX valeurs : le nom du référentiel retenu, et la liste des
      valeurs — nom usuel, code de cotation, place.
      [rend: 2]
    ⑥ TRAITEMENT — ① lister les référentiels · ② **prendre le plus récent PAR SA
      DATE** · ③ écarter les lignes sans mnémonique · ④ écarter celles marquées
      hors univers · ⑤ suffixer le code selon la place de cotation.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le plus récent se
      lit dans la date et jamais dans l alphabet, parce que les noms du projet
      commencent par le jour de la semaine. Et l exclusion hors univers est une
      DÉCISION écrite dans la donnée, avec son motif — pas une exclusion cachée
      dans le code.
    ⑨ CE QUI CLOCHE — **Une colonne `hors_univers` ABSENTE et une colonne VIDE
      donnent le même résultat : la valeur est collectée.** Un référentiel qui
      perdrait cette colonne ramènerait silencieusement tout l univers, y compris
      ce que Jean-Luc en avait retiré.
      **Et `sys.path.insert` empile un chemin sans vérifier s il y est déjà.**
    ⑩ EFFET — **MODIFIE LE CHEMIN DE RECHERCHE DES MODULES du processus.**
      N écrit aucun fichier.
    ⑪ TERMINAISON — **PEUT NE PAS RENDRE LA MAIN : code 2 si aucun référentiel
      n est trouvé.** Aucun de ses appels ne termine.
      [sort: oui]
    """
    d = os.path.join(racine, "donnees")
    # LE PLUS RÉCENT SE LIT DANS LA DATE, JAMAIS DANS L'ALPHABET (12-09-2026).
    # Le référentiel porte un nom daté ; `sorted()[-1]` prenait le dernier par
    # l'alphabet, et les noms du projet commencent par le jour de la semaine.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from COMMUN import le_plus_recent
    cands = [f for f in os.listdir(d) if f.upper().startswith("REFERENTIEL_VALEURS") and f.endswith(".csv")]
    if not cands:
        print("CODE 2 — référentiel introuvable"); sys.exit(2)
    out = []
    with open(os.path.join(d, le_plus_recent(cands)), encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            m = (r.get("mnemonique") or "").strip()
            if not m:
                continue
            # HORS UNIVERS — DECISION DE JEAN-LUC, 13-09-2026.
# Certaines valeurs du CAC 40 ne doivent pas etre collectees. Le referentiel
# porte une colonne `hors_univers` : quand elle est remplie, elle dit POURQUOI,
# et la valeur est sautee. Ce n est pas un oubli, c est une decision. (A-410)
            # La colonne `hors_univers` du referentiel porte le motif. Une valeur
            # qui la porte n est PAS collectee, et ce n est pas un oubli.
            # **La difference avec l exclusion retiree ce matin est entiere** :
            # celle-la etait cachee dans le code, en dur sur un prefixe de nom, et
            # citait une action du backlog comme si elle l autorisait, alors que cette
# action (A-235) demandait de
            # RESOUDRE. Celle-ci est une decision, ecrite dans la DONNEE que le
            # programme lit, avec son motif et son action.
            if (r.get("hors_univers") or "").strip():
                continue
            ams = "AMSTERDAM" in (r.get("place_cotation") or "").upper()
            out.append((r["nom_usuel"].strip(), m + ("n" if ams else "p"), "AMSTERDAM" if ams else "PARIS"))
    return le_plus_recent(cands), out


def main():
    """Collecte les cours du jour chez ABC Bourse et les empile.

    ① RÔLE — **LE PAS N°1 DU CIRCUIT DU SOIR.** Tout le reste en dépend : sans
      cours neufs, le détecteur calcule sur la veille.
    ② CONTEXTE D APPEL — Le circuit du soir, après la clôture. **Un signal n est
      jamais connu avant la clôture, et un cours du jour non plus.**
    ③ ENTRÉE — La ligne de commande : la racine du dépôt. **Et deux fichiers** :
      le référentiel des valeurs, et le fichier d arrivée déjà écrit, relu pour
      savoir où chaque valeur s était arrêtée.
    ④ CONDITIONS D ENTRÉE — Un argument, et le module de contrôle des cours.
      **Le fichier d arrivée peut ne pas exister : c est le premier soir.**
    ⑤ SORTIE — Ne rend rien. **Tout passe par le code de sortie, le rapport
      affiché, et les deux fichiers écrits.**
      [rend: rien]
    ⑥ TRAITEMENT — ① charger le contrôleur et le référentiel · ② relire le
      fichier d arrivée pour connaître la dernière séance de chaque valeur ·
      ③ pour chaque valeur : télécharger, extraire, **écarter la séance du jour
      si la place n a pas encore clôturé**, ne garder que ce qui est plus récent
      · ④ soumettre le lot au contrôle de vraisemblance · ⑤ n écrire que ce qui
      passe · ⑥ écrire le rapport.
    ⑦ UNITÉ — Prix en euros, volume en titres, dates au format AAAA-MM-JJ.
      **L heure de clôture est une heure de Paris, et la pause entre pages est en
      secondes.**
    ⑧ POURQUOI — **Le nom écrit est le nom NORMALISÉ** : le
      10-09-2026, le programme écrivait « BUREAU VERITAS » quand le fichier
      portait « BUREAU_VERITAS » — deux noms pour une valeur.
      **Et le lot entier est soumis au contrôle avant écriture** : un lot
      bloquant n écrit rien, plutôt que d écrire la moitié.
    ⑨ CE QUI CLOCHE — **Le rapport est écrit sous un nom qui porte le jour.**
      Deux exécutions le même jour écrasent le premier rapport sans un mot — et
      la première peut avoir échoué pour une raison que la seconde efface.
    ⑩ EFFET — **AJOUTE au fichier `donnees/claude_cours_nouveaux.csv`** — il
      n est pas réécrit, il grandit · **crée `rapports/` s il manque et y écrit
      le rapport du jour, en l écrasant s il existe** · **SORT SUR LE RÉSEAU
      quarante fois** · modifie le chemin de recherche des modules.
    ⑪ TERMINAISON — **NE REND JAMAIS LA MAIN : trois codes.** `0` tout est
      collecté · `1` au moins une valeur en échec, le reste est écrit ·
      `2` aucun argument, module introuvable, ou **lot bloquant — rien écrit**.
      **Et `lire_referentiel`, qu il appelle, peut terminer en code 2 sans
      [sort: oui]
    ⑫ DÉFINITIONS —
      le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      le détecteur : programmes/DETECTER_LES_SIGNAUX_GITHUB.py, qui écrit les signaux du jour
      le référentiel : donnees/REFERENTIEL_VALEURS_*.csv, la liste des valeurs à suivre, avec pour chacune son mnémonique et sa place de cotation.
      le référentiel des valeurs : donnees/REFERENTIEL_VALEURS_*.csv, la liste des valeurs à suivre, avec pour chacune son mnémonique et sa place de cotation.
      un signal : le repérage, sur la dernière séance connue, d'une configuration de cours qui déclenche une simulation d'achat.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    racine = sys.argv[1]
    sys.path.insert(0, os.path.join(racine, "programmes"))
    try:
        import CONTROLER_LES_COURS as C
    except Exception as e:
        print(f"CODE 2 — CONTROLER_LES_COURS introuvable : {e}"); sys.exit(2)

    maintenant = datetime.now(PARIS)
    jour = maintenant.strftime("%Y-%m-%d")
    ref_nom, valeurs = lire_referentiel(racine)
    cible = os.path.join(racine, "donnees", "claude_cours_nouveaux.csv")

    derniere, cloture_prec = {}, {}
    if os.path.isfile(cible):
        with open(cible, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                v = C.normaliser_valeur(r["valeur"]); d = C.normaliser_date(r["date"])
                if d and (v not in derniere or d > derniere[v]):
                    derniere[v] = d
                    try: cloture_prec[v] = float(r["close"])
                    except (ValueError, KeyError): pass

    rapport = [f"# COLLECTE ABC BOURSE DEPUIS GITHUB — {maintenant.strftime('%a %d-%m-%Y %Hh%M')} (Paris)",
               f"référentiel : {ref_nom} · {len(valeurs)} valeurs · fichier : donnees/claude_cours_nouveaux.csv",
               f"ligne du jour acceptée pour Paris : {'OUI' if maintenant.hour >= HEURE_CLOTURE_PARIS else 'NON (avant 18h)'} · Amsterdam : jamais", ""]
    a_ajouter, echecs, sans_nouveau, details = [], [], [], []

    for nom, code, place in valeurs:
        url = f"https://www.abcbourse.com/cotation/{code}"
        try:
            page = telecharger(url)
        except Exception as e:
            echecs.append((nom, code, f"téléchargement : {e}")); time.sleep(PAUSE_ENTRE_PAGES); continue
        seances, note = extraire(page)
        if not seances:
            echecs.append((nom, code, note or "0 séance extraite")); time.sleep(PAUSE_ENTRE_PAGES); continue
        plus_recente = seances[0]["date"]
        if place == "AMSTERDAM" or (maintenant.hour < HEURE_CLOTURE_PARIS and plus_recente == jour):
            seances = seances[1:]
        seuil = derniere.get(C.normaliser_valeur(nom), DATE_PLANCHER)
        neuves = [s for s in seances if s["date"] > seuil]
        for s in neuves:
            # LE NOM ÉCRIT EST LE NOM NORMALISÉ. Une même valeur s'écrit de deux façons
# selon la source : avec des espaces ou avec des tirets bas. Écrire les deux
# formes dans le même fichier crée deux valeurs là où il n'y en a qu'une, et
# les cours se répartissent entre elles sans que rien ne le dise. (R-719)
# Mesuré au
            # premier tir du 10-09 : le programme écrivait « BUREAU VERITAS » quand le
            # fichier portait « BUREAU_VERITAS » — deux noms pour une valeur. Le fichier
            # entier utilise la forme normalisée depuis ce même soir.
            s["valeur"] = C.normaliser_valeur(nom)
        if neuves:
            a_ajouter += neuves
            details.append(f"- {nom} ({code}) : +{len(neuves)} — {neuves[-1]['date']} → {neuves[0]['date']}" + (f" · {note}" if note else ""))
        else:
            sans_nouveau.append((nom, code, seuil, plus_recente))
        time.sleep(PAUSE_ENTRE_PAGES)

    ecrites, verdict, alertes, bloquant = 0, "OK", [], ""
    if a_ajouter:
        verdict, bonnes, alertes, bloquant = C.controler(a_ajouter, clotures_precedentes=cloture_prec)
        if bonnes:
            ecrites, _, _ = C.ajouter_au_fichier(bonnes, cible)

    rapport.append("## RÉSULTAT")
    rapport.append(f"valeurs lues : {len(valeurs) - len(echecs)}/{len(valeurs)} · séances proposées : {len(a_ajouter)} · verdict : {verdict} · écrites : {ecrites} · alertes : {len(alertes)}")
    if bloquant:
        rapport.append(f"\n## ❌ LOT BLOQUANT — rien écrit : {bloquant}")
    if details:
        rapport.append("\n## séances ajoutées par valeur"); rapport += details
    if echecs:
        rapport.append("\n## ⚠️ VALEURS EN ÉCHEC — une valeur attendue qui ne renvoie rien est une ALERTE")
        rapport += [f"- {n} ({c}) : {m}" for n, c, m in echecs]
    if alertes:
        rapport.append("\n## ⚠️ alertes du contrôle de vraisemblance"); rapport += [f"- {a}" for a in alertes]
    if sans_nouveau:
        rapport.append(f"\n## sans séance nouvelle ({len(sans_nouveau)})")
        rapport += [f"- {n} : fichier {s}, ABC {p}" for n, c, s, p in sans_nouveau]

    os.makedirs(os.path.join(racine, "rapports"), exist_ok=True)
    chemin_rapport = os.path.join(racine, "rapports", f"collecte_abc_{jour}.md")
    open(chemin_rapport, "w", encoding="utf-8").write("\n".join(rapport) + "\n")
    print("\n".join(rapport))
    sys.exit(2 if bloquant else (1 if echecs else 0))


if __name__ == "__main__":
    main()
