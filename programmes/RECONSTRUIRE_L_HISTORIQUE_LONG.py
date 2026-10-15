#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RECONSTRUIRE_L_HISTORIQUE_LONG.py — Sam 10-10-2026 (Paris) — PROPOSÉ, non validé (A-555, décision de Jean-Luc du
09-10-2026 à 20h57). Simulation uniquement.

① RÔLE — Reconstruire chaque ligne de l'historique long réparé à partir de ses sources, et dire, ligne par ligne, si
  elle se retrouve. Une ligne se reconstruit ainsi : sa clôture = la clôture BRUTE de Paris ce jour-là × le produit
  des facteurs de TOUTES les opérations sur le capital postérieures à ce jour (divisions, actions gratuites, droits
  de souscription, distributions d'actions d'une autre société), chaque facteur étant pris à sa source. Le
  dividende n'est jamais corrigé (R-108 : « la courbe de calcul est corrigée sauf des dividendes »). Là où aucun
  cours brut n'existe mais où le fichier maître porte un cours de Google, la ligne est seulement CONFRONTÉE à
  Google : Google corrige lui aussi le passé des divisions (mesuré le 10-10-2026 sur Air Liquide : ses cours d'avant
  le 08-06-2026 portent déjà l'attribution d'une action gratuite pour dix), ce n'est donc pas un cours brut.
② CONTEXTE D'APPEL — À la main, avant toute décision de verser l'historique long au fichier maître (A-538) :
  python3 programmes/RECONSTRUIRE_L_HISTORIQUE_LONG.py <racine> [--ligne VALEUR AAAA-MM-JJ].
  Avec --ligne, il explique une seule ligne, opération par opération. Ses épreuves :
  tests/EPREUVES_DE_LA_RECONSTRUCTION_Sam_10-10-2026.py.
③ ENTRÉE — La racine du dépôt ; facultatif, une valeur et une date.
④ CONDITIONS D'ENTRÉE — Le fichier réparé (donnees/sources_yahoo/historique_long_repare.csv), l'extrait bnains et
  ses barres prouvées fausses, le fichier maître (donnees/cours_maitre.csv : ses lignes « euronext » et « abc »
  sont des cours bruts, ses lignes « google » des cours corrigés par Google), les divisions déclarées par Yahoo
  (donnees/sources_yahoo/evenements.json), les verdicts sur Yahoo (AJUSTEMENTS_DE_YAHOO.csv), les opérations
  déclarées (DETACHEMENTS_OFFICIELS.csv et DROITS_BNAINS.csv), la table des divisions relevée chez bnains
  (donnees/sources_bnains/DIVISIONS_BNAINS.csv, écrite par etudes/outils/RELEVER_LES_DIVISIONS_BNAINS.py ; sans
  elle, le programme tourne et le dit). Les cours et les opérations sont lus par les fonctions de
  programmes/CONTROLER_L_HISTORIQUE_LONG.py, jamais relu autrement (R-708 : deux implémentations d'une même chose
  divergent toujours).
⑤ SORTIE — UNE valeur : le code de sortie — 0 quand le programme a tourné (le verdict est dans ce qu'il écrit, il
  ne refuse rien : c'est un instrument de mesure, pas un contrôle), 2 quand il n'a pas pu tourner (R-734). Écrit
  deux tables, et affiche un résumé.
⑥ TRAITEMENT — ① lire · ② `operations` : la liste des opérations de chaque valeur, avec leur facteur et leur
  source, confrontée à la table de bnains (`confronter`), qui en ajoute · ③ `bruts` : la clôture brute de Paris de chaque ligne quand une source l'a (bnains jusqu'au
  28-02-2017 ; les lignes « euronext » et « abc » du fichier maître, depuis le 13-07-2026), et la clôture de
  Google ailleurs (fichier maître, 02-01-2024 → 08-09-2026) · ④ `deduire` : le facteur d'une opération que Yahoo a
  ajustée sans le dire ni le documenter, mesuré entre les deux périodes qui l'encadrent · ⑤ `reconstruire` :
  pour chaque ligne, l'écart = clôture du fichier ÷ (brut × facteurs) − 1, et son statut ; pour chaque opération,
  l'écart du facteur que le fichier APPLIQUE à son facteur documenté · ⑥ écrire et résumer.
⑦ UNITÉ — Des euros pour les cours ; des RAPPORTS sans unité pour les facteurs ; des FRACTIONS pour les écarts.
⑧ POURQUOI — Demande de Jean-Luc du 09-10-2026 à 20h55 : « on doit pouvoir comprendre chaque valeur de
  l'historique et pouvoir absolument tout retrouver et reconstituer ». Avant ce programme, le journal des
  réparations expliquait 39 451 lignes modifiées ; les 205 542 autres étaient la valeur de Yahoo, sans rien qui
  dise comment elle se déduit du vrai cours de Paris.
⑨ CE QUI CLOCHE — De mars 2017 à décembre 2023, aucune source de cours n'est au dépôt : ces lignes sont « sans
  cours brut », non reconstruites ; de janvier 2024 à septembre 2026, seulement confrontées à Google. · Le facteur documenté d'un droit de souscription se calcule avec le
  cours de la veille déclaré : s'il n'est pas celui de la veille de séance, l'écart se voit sur toute la période
  d'avant (Euronext 2021, Veolia 2021, Air Liquide 2016 : relecture de Cowork du 09-10-2026). · Une opération dont
  le facteur n'est pas documenté et que rien ne mesure laisse les lignes d'avant « facteur inconnu ». · « Reconstruite »
  veut dire « conforme à la liste des opérations » : une opération ABSENTE de toutes les sources rend la ligne
  « reconstruite » ET fausse, car le fichier et le cours brut portent alors la même marche (Sagem, une action gratuite
  pour six, 19-12-2003 : invisible jusqu'à la table de bnains). La liste n'est donc complète que pour ce que Yahoo,
  les documents déclarés et bnains écrivent ensemble. · La table de bnains ne liste ni les droits de souscription ni
  les distributions d'une autre société.
⑩ EFFET — Lit les fichiers du ④. Écrit donnees/sources_yahoo/RECONSTRUCTION_PAR_OPERATION.csv et
  donnees/sources_yahoo/RECONSTRUCTION_ECARTS.csv. Affiche.
⑪ TERMINAISON — Rend la main : chaque étape parcourt un nombre fini de lignes. Aucun de mes appels ne peut
  boucler.
"""
import bisect, csv, datetime, json, os, re, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CONTROLER_L_HISTORIQUE_LONG as K
from CONTRATS_DES_FICHIERS import COURS_BNAINS

MAITRE = os.path.join("donnees", "cours_maitre.csv")
FIN_BNAINS = "2017-02-28"          # dernière séance archivée par bnains (LISEZ-MOI des cours)
TOLERANCE = 0.002                  # une ligne se retrouve quand l'écart est de moins de 0,2 %
DIVISIONS = os.path.join("donnees", "sources_bnains", "DIVISIONS_BNAINS.csv")   # relevé par RELEVER_LES_DIVISIONS_BNAINS
RAPPROCHEMENT = 40                 # jours : une division de bnains et une opération à moins de 40 jours sont la même
DEBUT = "2000-01-01"               # l'historique long commence en janvier 2000 ; une division d'avant ne touche aucune ligne
MEME_FACTEUR = 1e-3                # deux facteurs sont les mêmes à 0,1 % près
ARRONDI_BNAINS = 0.005             # le diviseur de bnains n'a souvent que deux décimales utiles (Sagem 2003, une
                                   # action pour six : « 1.17000 » pour 7 ÷ 6 = 1,16667) : la parité ÉCRITE dans le
                                   # commentaire le remplace quand elle s'accorde avec lui à cette tolérance près
NOMBRES = {"deux": 2, "trois": 3, "quatre": 4, "cinq": 5, "six": 6, "sept": 7, "huit": 8, "neuf": 9, "dix": 10,
           "vingt": 20, "cinquante": 50}
CHAMP_DE_BNAINS = ("division", "actions gratuites", "complément")   # les natures que la table de bnains liste
PAR_OPERATION = os.path.join("donnees", "sources_yahoo", "RECONSTRUCTION_PAR_OPERATION.csv")
ECARTS = os.path.join("donnees", "sources_yahoo", "RECONSTRUCTION_ECARTS.csv")


def operations(evenements, a_defaire, detachements, bnains, divisions=None):
    """Rend, pour chaque valeur, ses opérations sur le capital avec leur facteur et leur source.

    ① RÔLE — Une seule liste des opérations qui changent le rapport entre la courbe et le cours brut.
    ② CONTEXTE D'APPEL — `main` ; les épreuves.
    ③ ENTRÉE — `evenements` : le contenu de evenements.json · `a_defaire` : `K.lire_a_defaire` · `detachements` :
      `K.lire_detachements` · `bnains` : l'extrait, barres fausses ôtées (pour la valeur d'un droit vu chez bnains) ·
      `divisions` : les lignes de DIVISIONS_BNAINS.csv (`lire_divisions`), ou None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : ① valeur → liste triée de (date, facteur, nature, source), où le facteur est ce par
      quoi la courbe multiplie les cours d'avant la date, ou None quand il n'est pas documenté ; ② (valeur, date) →
      ce que la table des divisions de bnains dit de cette opération.
      [rend: 2]
    ⑥ TRAITEMENT — ① les divisions déclarées par Yahoo, sauf celles qu'il faut défaire (`K.sans_les_divisions_fausses`),
      facteur = dénominateur ÷ numérateur · ② les opérations déclarées par un document ou vues chez bnains,
      facteur = 1 ÷ (1 + `K.marche_permise`), nommées « actions gratuites » quand le prix de souscription est nul · ③ les verdicts « ajustée par Yahoo » sans facteur documenté
      (une distribution que Yahoo a corrigée sans la déclarer) : facteur None, à mesurer — `confronter` passe
      entre ② et ③.
    ⑦ UNITÉ — Des RAPPORTS.
    ⑧ POURQUOI — Les opérations vivent dans trois fichiers ; la reconstruction doit les voir toutes, et chacune avec
      la source qui la justifie.
    ⑨ CE QUI CLOCHE — Le verdict d'un ajustement caché se reconnaît à sa colonne ce_que_yahoo_declare, qui commence
      par « aucune déclaration » : un autre texte le ferait manquer. Jusqu'au 10-10-2026 il se reconnaissait au
      verdict (« ajustée par Yahoo »), et la division de Carrefour du 11-04-2000, dont le verdict dit « légitime »,
      manquait.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    ops = {}
    ev = K.sans_les_divisions_fausses(evenements, a_defaire)
    for v, e in ev.items():
        for d, num, den in e.get("divisions", []):
            ops.setdefault(v, []).append((d, den / num, f"division déclarée par Yahoo, {num:g} pour {den:g}",
                                          "donnees/sources_yahoo/evenements.json"))
    for v, jours in (detachements or {}).items():
        for d, droit in jours.items():
            m = K.marche_permise(bnains.get(v, {}), droit)
            genre = "actions gratuites" if droit[0] == "document" and droit[2] == 0 else droit[0]
            ops.setdefault(v, []).append((d, 1 / (1 + m), f"{genre} (marche permise {100 * m:+.4f} %)",
                                          "donnees/sources_bnains/DETACHEMENTS_OFFICIELS.csv"))
    avis = confronter(ops, divisions or [])
    deja = {(v, d) for v, liste in ops.items() for d, *_ in liste}
    for r in csv.DictReader(open(K.VERDICTS_YAHOO, encoding="utf-8")):
        if (r["ce_que_yahoo_declare"].startswith("aucune déclaration") and not r["facteur_a_defaire"]
                and (r["valeur"], r["date"]) not in deja):
            ops.setdefault(r["valeur"], []).append((r["date"], None, "ajustement caché de Yahoo, facteur non documenté",
                                                    "donnees/sources_yahoo/AJUSTEMENTS_DE_YAHOO.csv"))
    for v, liste in ops.items():
        for x, *_ in liste:
            avis.setdefault((v, x), "absente de la table de bnains")
    return {v: sorted(liste, key=lambda o: (o[0], o[2])) for v, liste in ops.items()}, avis


def diviseur_exact(r):
    """Rend le diviseur d'une ligne de la table de bnains, exact quand la parité est écrite dans son commentaire.

    ① RÔLE — Ne pas prendre un arrondi de bnains pour un désaccord, ni un désaccord pour un arrondi.
    ② CONTEXTE D'APPEL — `confronter` ; les épreuves.
    ③ ENTRÉE — `r` : une ligne de DIVISIONS_BNAINS.csv.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le diviseur.
      [rend: 1]
    ⑥ TRAITEMENT — Un commentaire d'actions gratuites qui écrit « pour N » (en chiffres, ou en lettres : `NOMBRES`)
      donne (N + 1) ÷ N ; gardé seulement s'il s'accorde au diviseur écrit à `ARRONDI_BNAINS` près. Sinon le
      diviseur écrit.
    ⑦ UNITÉ — Un RAPPORT.
    ⑧ POURQUOI — Relecture indépendante du 10-10-2026 : une tolérance d'arrondi sur tout diviseur cachait deux vrais
      désaccords — Air Liquide 2012 (bnains « 1 action gratuite pour 10 », 1,1 exact ; Yahoo 1,10254 : +0,23 %) et
      Accor 2010 (bnains 1,5328, quatre décimales, sans parité écrite ; retenu 1,53886 : +0,39 %). La parité écrite
      tranche : Sagem 2003, « Attribution gratuite d'une action pour 6 », 1,17 écrit, 7 ÷ 6 exact.
    ⑨ CE QUI CLOCHE — Une parité composée (« une action gratuite pour 5, puis division du nominal par 3 ») ne
      s'accorde pas au diviseur écrit (3,6) : le diviseur écrit est gardé, exact dans ce cas.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    ecrit = float(r["diviseur"])
    c = r["commentaire"].lower()
    m = re.search(r"pour (\d+|" + "|".join(NOMBRES) + r")\b", c)
    if "gratuite" in c and m:
        n = int(m.group(1)) if m.group(1).isdigit() else NOMBRES[m.group(1)]
        if abs((n + 1) / n - ecrit) <= ARRONDI_BNAINS:
            return (n + 1) / n
    return ecrit


def lire_divisions(chemin):
    """Rend les lignes de la table des divisions relevée chez bnains, ou une liste vide si le fichier manque.

    ① RÔLE — Lire DIVISIONS_BNAINS.csv.
    ② CONTEXTE D'APPEL — `main` ; les épreuves.
    ③ ENTRÉE — `chemin`.
    ④ CONDITIONS D'ENTRÉE — Écrit par etudes/outils/RELEVER_LES_DIVISIONS_BNAINS.py.
    ⑤ SORTIE — UNE valeur : la liste des lignes (dictionnaires).
      [rend: 1]
    ⑥ TRAITEMENT — Lire ; un fichier absent rend une liste vide.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La reconstruction doit tourner sans ce relevé : il confronte, il n'est pas indispensable.
    ⑨ CE QUI CLOCHE — Un fichier absent fait tourner la reconstruction sans la confrontation à bnains : `main` le
      dit à l'écran.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    if not os.path.exists(chemin):
        return []
    return list(csv.DictReader(open(chemin, encoding="utf-8")))


def confronter(ops, divisions):
    """Confronte chaque division de bnains aux opérations ; ajoute ce qui manque ; rend l'avis de bnains par opération.

    ① RÔLE — Une seconde source pour les divisions et actions gratuites : la table que bnains publie par action.
    ② CONTEXTE D'APPEL — `operations`, après les divisions de Yahoo et les opérations déclarées.
    ③ ENTRÉE — `ops` : valeur → liste de (date, facteur, nature, source), MODIFIÉE ici · `divisions` : `lire_divisions`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : (valeur, date) → le texte de l'avis de bnains sur cette opération.
      [rend: 1]
    ⑥ TRAITEMENT — Les lignes de bnains depuis `DEBUT` sont d'abord regroupées par jour (deux lignes du même jour se
      multiplient), chaque diviseur pris par `diviseur_exact`. Pour chaque jour de bnains : ① si une opération tombe
      le MÊME jour, comparer au produit des opérations de ce jour que bnains liste (`CHAMP_DE_BNAINS` : divisions,
      actions gratuites — Sagem, 10-07-2000 : la division par 3 de Yahoo et l'action gratuite pour cinq déclarée),
      ou de toutes s'il n'y en a aucune (Accor, 02-07-2010 : bnains liste la scission comme une division ; Total,
      18-05-2006 : la division par 4 seule, sans la distribution d'Arkema) ; même facteur à `MEME_FACTEUR` près →
      « même facteur » ; sinon un COMPLÉMENT est ajouté ce jour-là, (1 ÷ diviseur) ÷ produit retenu — si bnains a
      raison, les lignes d'avant s'écartent de ce complément, et la reconstruction le montre ; ② sinon, un jour de
      divisions ou d'actions gratuites à moins de `RAPPROCHEMENT` jours AU MÊME FACTEUR → « date différente » (Hermès
      2006) ; ③ sinon la division est AJOUTÉE à son jour, source bnains. Une opération que rien ne rapproche :
      « absente de la table de bnains » (posé par `operations`, après les ajustements cachés).
    ⑦ UNITÉ — Des RAPPORTS ; des jours.
    ⑧ POURQUOI — Le 10-10-2026, la table de bnains a montré des opérations que rien d'autre ne documentait :
      Société Générale (division par 4, 11-05-2000) et Pernod Ricard (une action gratuite pour quatre, 14-02-2003),
      ajustées par Yahoo sans être déclarées ; Sagem (une action gratuite pour 5 puis division par 3, 10-07-2000 ;
      une action gratuite pour 6, 19-12-2003), où Yahoo n'a corrigé que la division de 2000 et rien en 2003. Une
      opération absente de la liste rend la courbe fausse ET la ligne « reconstruite » : le fichier et le cours brut
      portent alors la même marche.
    ⑨ CE QUI CLOCHE — La table de bnains ne liste que les divisions et les actions gratuites, jamais les droits de
      souscription : « absente » n'accuse donc pas un droit. · Elle a ses propres fautes : Hermès, division datée d'un
      samedi (10-06-2006) ; Air Liquide 2014, ligne datée 07-05-2014 quand son commentaire dit 02-06 ; Schneider
      Electric, 01-08-2011 quand le document de référence et Francfort placent la division au 02-09-2011 (l'extrait
      bnains et Yahoo portent eux aussi la marche dès le 01-08 : BARRES_BNAINS_FAUSSES.csv). Une date différente est
      écrite, jamais tranchée ici. · Une table vide (Eiffage) ne prouve rien. · Une division de bnains à une autre
      date ET d'un autre facteur qu'une opération proche est ajoutée à part, jamais fondue dans l'autre (relecture
      indépendante du 10-10-2026 : l'ancien appariement défaisait une division de Yahoo pour une action gratuite
      omise trente jours plus tard).
    ⑩ EFFET — Ajoute des opérations à `ops`.
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    avis = {}
    par_jour = {}
    for r in divisions:
        if r["date"] >= DEBUT:
            x = par_jour.setdefault((r["valeur"], r["date"]), [1.0, []])
            x[0] *= diviseur_exact(r)
            x[1].append(f"÷{r['diviseur']} « {r['commentaire']} »")
    for (v, d), (diviseur, textes) in sorted(par_jour.items()):
        f = 1 / diviseur
        texte = f"bnains : {d}, " + " ; ".join(textes)
        tous, champ = {}, {}
        for x, g, nature, _ in ops.get(v, []):
            if g is not None:
                tous[x] = tous.get(x, 1.0) * g
                if nature.startswith(CHAMP_DE_BNAINS):
                    champ[x] = champ.get(x, 1.0) * g
        jd = datetime.date.fromisoformat(d)
        if d in tous:
            g = champ.get(d, tous[d])
            if abs(f / g - 1) <= MEME_FACTEUR:
                avis[(v, d)] = f"{texte} — même date, même facteur"
            else:
                avis[(v, d)] = (f"{texte} — même date, FACTEUR DIFFÉRENT (retenu ÷{1 / g:.6g}, bnains ÷{diviseur:.6g}, "
                                f"écart {100 * (f / g - 1):+.3f} %) : complément ajouté")
                ops[v].append((d, f / g, f"complément : bnains ÷{diviseur:.6g}, l'opération retenue ÷{1 / g:.6g}",
                               DIVISIONS))
            continue
        voisins = sorted((abs((datetime.date.fromisoformat(x) - jd).days), x) for x, g in champ.items()
                         if abs(f / g - 1) <= MEME_FACTEUR)
        voisins = [x for n, x in voisins if n <= RAPPROCHEMENT]
        if voisins:
            avis[(v, voisins[0])] = f"{texte} — date différente ({d}), même facteur"
            continue
        ops.setdefault(v, []).append((d, f, f"division relevée chez bnains, " + " ; ".join(textes), DIVISIONS))
        avis[(v, d)] = texte + " — seule source"
    return avis


def bruts(bnains, maitre, sources_maitre):
    """Rend la clôture brute de Paris de chaque (valeur, date) qu'une source a, et la clôture de Google à part.

    ① RÔLE — Le cours vrai contre lequel chaque ligne se reconstruit.
    ② CONTEXTE D'APPEL — `main` ; les épreuves.
    ③ ENTRÉE — `bnains` : l'extrait, barres fausses ôtées · `maitre` : le fichier maître, lu par `K.lire_cours` ·
      `sources_maitre` : (valeur, date) → la colonne source du fichier maître.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : ① valeur → {date : (clôture brute, source)} · ② valeur → {date : clôture de Google}.
      [rend: 2]
    ⑥ TRAITEMENT — bnains jusqu'à `FIN_BNAINS` ; les lignes « euronext » et « abc » du fichier maître ; les lignes
      « google » à part ; une clôture nulle ou négative est ignorée.
    ⑦ UNITÉ — Des EUROS.
    ⑧ POURQUOI — bnains archive les cours de Paris tels que cotés (2000 → 28-02-2017) ; Euronext et ABC Bourse
      donnent le cours du jour, brut. Google corrige le passé des divisions : sa clôture confirme une ligne, elle
      ne la reconstruit pas.
    ⑨ CE QUI CLOCHE — Rien entre le 01-03-2017 et le 31-12-2023.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    sortie, google = {}, {}
    for v, s in bnains.items():
        for d, x in s.items():
            if d <= FIN_BNAINS and x[3] > 0:
                sortie.setdefault(v, {})[d] = (x[3], "bnains")
    for v, s in maitre.items():
        for d, x in s.items():
            src = sources_maitre.get((v, d), "")
            if x[3] <= 0 or d in sortie.get(v, {}):
                continue
            if src in ("euronext", "abc"):
                sortie.setdefault(v, {})[d] = (x[3], f"maître, {src}")
            elif src == "google":
                google.setdefault(v, {})[d] = x[3]
    return sortie, google


def facteur_apres(ops, d):
    """Rend le produit des facteurs des opérations postérieures à `d`, ou None si l'un est inconnu.

    ① RÔLE — Le facteur total qu'une ligne du jour `d` doit porter.
    ② CONTEXTE D'APPEL — `deduire`, `reconstruire`, `expliquer`.
    ③ ENTRÉE — `ops` : la liste d'une valeur, rendue par `operations` (facteurs éventuellement déduits) · `d` : une date.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le produit, ou None.
      [rend: 1]
    ⑥ TRAITEMENT — Multiplier les facteurs des opérations de date strictement postérieure à `d`.
    ⑦ UNITÉ — Un RAPPORT.
    ⑧ POURQUOI — Une opération change les cours d'AVANT sa date : le jour même, la ligne est déjà ex-opération.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    p = 1.0
    for x, f, *_ in ops:
        if x > d:
            if f is None:
                return None
            p *= f
    return p


def deduire(fichier, brut, ops):
    """Mesure le facteur des opérations non documentées ; rend les opérations complétées.

    ① RÔLE — Donner un facteur, MESURÉ, à un ajustement que Yahoo a fait sans le documenter (Kering → Puma, 2018).
    ② CONTEXTE D'APPEL — `main` ; les épreuves.
    ③ ENTRÉE — `fichier` : le fichier réparé · `brut` : `bruts` · `ops` : `operations`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : les opérations, où chaque facteur None est remplacé par (facteur mesuré) quand il se
      mesure ; la nature dit alors « facteur MESURÉ ». Ce qui ne se mesure pas reste None.
      [rend: 1]
    ⑥ TRAITEMENT — De la plus récente à la plus ancienne : le rapport fichier ÷ (brut × facteurs connus des
      opérations postérieures), médian sur la période qui précède l'opération (jusqu'à l'opération d'avant) et sur
      celle qui la suit (jusqu'à l'opération d'après) ; le facteur est le premier ÷ le second.
    ⑦ UNITÉ — Un RAPPORT.
    ⑧ POURQUOI — Sans facteur, toutes les lignes d'avant seraient « facteur inconnu » ; mesuré, il est écrit comme
      tel, et ce qui reste d'écart ne lui est plus imputable.
    ⑨ CE QUI CLOCHE — Un facteur mesuré confirme la cohérence, pas la justesse : il vaut ce que Yahoo a appliqué.
      Deux opérations non documentées sans cours brut entre elles ne se séparent pas.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    sortie = {}
    for v, liste in ops.items():
        liste = list(liste)
        for i in range(len(liste) - 1, -1, -1):
            d, f, nature, source = liste[i]
            if f is not None:
                continue
            debut = liste[i - 1][0] if i > 0 else ""
            fin = liste[i + 1][0] if i + 1 < len(liste) else "9999"
            avant, apres = [], []
            for x in fichier.get(v, {}):
                if x in brut.get(v, {}):
                    p = facteur_apres(liste[i + 1:], x)
                    if p is None:
                        continue
                    r = fichier[v][x][3] / brut[v][x][0] / p
                    if debut <= x < d:
                        avant.append(r)
                    elif d <= x < fin:
                        apres.append(r)
            if avant and apres:
                liste[i] = (d, statistics.median(avant) / statistics.median(apres),
                            "ajustement caché de Yahoo, facteur MESURÉ (non documenté)", source)
        sortie[v] = liste
    return sortie


def reconstruire(fichier, brut, ops, google=None, avis=None):
    """Reconstruit chaque ligne et juge chaque opération ; rend les écarts par ligne et par opération.

    ① RÔLE — Le cœur : dire de chaque ligne si elle se retrouve depuis ses sources.
    ② CONTEXTE D'APPEL — `main` ; les épreuves.
    ③ ENTRÉE — `fichier`, `brut`, `ops` (complétées par `deduire`), `google` (`bruts`, seconde valeur), ou None ·
      `avis` (`operations`, seconde valeur), ou None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : ① la liste des lignes, chacune (valeur, date, clôture du fichier, clôture brute, source
      du brut, facteur attendu, écart, statut) ; ② la liste des opérations, chacune (valeur, date, nature, source,
      facteur, écart médian de la période d'avant, écart médian de la période d'après, lignes d'avant, lignes
      d'après, écart du facteur appliqué au facteur documenté, avis de bnains).
      [rend: 2]
    ⑥ TRAITEMENT — Pour chaque ligne : sans brut mais avec Google → « confirmée par Google » quand elle en est à
      moins de `TOLERANCE`, « écart à Google » sinon ; sans brut ni Google → « sans cours brut » ; facteur inconnu → « facteur inconnu » ;
      sinon écart = clôture ÷ (brut × facteur attendu) − 1. Pour chaque période entre deux dates d'opération,
      l'écart médian ; pour chaque date d'opération, l'écart du facteur APPLIQUÉ par le fichier au facteur documenté
      = (1 + médiane d'avant) ÷ (1 + médiane d'après) − 1, compté seulement au-delà de `TOLERANCE`. Une ligne est
      « reconstruite » quand son écart est sous `TOLERANCE` ; « reconstruite au facteur appliqué » quand elle se
      retrouve en remplaçant chaque facteur documenté par le facteur appliqué (le fichier porte un facteur que les
      documents ne donnent pas : Yahoo l'a calculé autrement, ou a oublié l'opération) ; « ligne isolée » sinon
      (cette ligne seule s'écarte, la source brute ou le fichier a tort ce jour-là).
    ⑦ UNITÉ — Des FRACTIONS pour les écarts.
    ⑧ POURQUOI — Séparer ce qui est durable (un facteur) de ce qui est ponctuel (une barre) : le premier se règle
      par une opération, le second par une séance.
    ⑨ CE QUI CLOCHE — Une période qui ne contient qu'une ligne se juge comme sa ligne. · Deux opérations du même jour
      (une division et son complément) ont un seul écart, commun aux deux. · Une période sans cours brut (mars 2017 →
      juin 2026) ne mesure rien : l'écart des opérations qui la bornent n'est pas mesuré, compté nul.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    lignes, par_op = [], []
    for v in sorted(fichier):
        liste = ops.get(v, [])
        bornes = [d for d, *_ in liste]
        periodes, brutes = {}, []
        for d in sorted(fichier[v]):
            c = fichier[v][d][3]
            if d not in brut.get(v, {}):
                g = (google or {}).get(v, {}).get(d)
                if g is None:
                    lignes.append((v, d, c, None, "", None, None, "sans cours brut"))
                else:
                    e = c / g - 1
                    lignes.append((v, d, c, g, "google", None, e,
                                   "confirmée par Google" if abs(e) <= TOLERANCE else "écart à Google"))
                continue
            b, src = brut[v][d]
            p = facteur_apres(liste, d)
            if p is None:
                lignes.append((v, d, c, b, src, None, None, "facteur inconnu"))
                continue
            e = c / (b * p) - 1
            k = bisect.bisect_right(bornes, d)
            periodes.setdefault(k, []).append(e)
            brutes.append(len(lignes))
            lignes.append((v, d, c, b, src, p, e, k))
        med = {k: statistics.median(x) for k, x in periodes.items()}
        ecart_op = {}
        for d in sorted(set(bornes)):
            a, z = med.get(bisect.bisect_left(bornes, d)), med.get(bisect.bisect_right(bornes, d))
            if a is not None and z is not None and abs((1 + a) / (1 + z) - 1) > TOLERANCE:
                ecart_op[d] = (1 + a) / (1 + z)
        for i in brutes:
            v_, d, c, b, src, p, e, k = lignes[i]
            q = 1.0
            for x, g in ecart_op.items():
                if x > d:
                    q *= g
            statut = ("reconstruite" if abs(e) <= TOLERANCE else
                      "reconstruite au facteur appliqué" if abs((1 + e) / q - 1) <= TOLERANCE else "ligne isolée")
            lignes[i] = (v_, d, c, b, src, p, e, statut)
        for d, f, nature, source in liste:
            ka, kz = bisect.bisect_left(bornes, d), bisect.bisect_right(bornes, d)
            par_op.append((v, d, nature, source, f, med.get(ka), med.get(kz), len(periodes.get(ka, [])),
                           len(periodes.get(kz, [])), ecart_op.get(d, 1.0) - 1, (avis or {}).get((v, d), "")))
    return lignes, par_op


def expliquer(v, d, fichier, brut, ops):
    """Rend le texte qui explique une ligne, opération par opération.

    ① RÔLE — Répondre à « d'où vient cette valeur ? » pour une ligne.
    ② CONTEXTE D'APPEL — `main`, avec --ligne.
    ③ ENTRÉE — `v`, `d` : la ligne · `fichier`, `brut`, `ops`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte.
      [rend: 1]
    ⑥ TRAITEMENT — La clôture du fichier, le brut et sa source, chaque opération postérieure avec son facteur et
      sa source, le produit, la clôture reconstruite et l'écart.
    ⑦ UNITÉ — Des EUROS et des RAPPORTS.
    ⑧ POURQUOI — Chaque valeur doit pouvoir se comprendre (demande de Jean-Luc du 09-10-2026 à 20h55).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    if d not in fichier.get(v, {}):
        return f"{v} {d} : aucune ligne dans le fichier réparé"
    t = [f"{v} {d} — clôture du fichier : {fichier[v][d][3]}"]
    if d in brut.get(v, {}):
        t.append(f"  clôture brute de Paris : {brut[v][d][0]} ({brut[v][d][1]})")
    else:
        t.append("  clôture brute de Paris : aucune source au dépôt pour ce jour")
    p = 1.0
    for x, f, nature, source in ops.get(v, []):
        if x > d:
            t.append(f"  × {'inconnu' if f is None else f'{f:.6f}'} — {x}, {nature} ({source})")
            p = None if (p is None or f is None) else p * f
    t.append(f"  facteur total : {'inconnu' if p is None else f'{p:.6f}'}")
    if p is not None and d in brut.get(v, {}):
        r = brut[v][d][0] * p
        t.append(f"  clôture reconstruite : {r:.6f} · écart du fichier : {100 * (fichier[v][d][3] / r - 1):+.4f} %")
    return "\n".join(t)


def main(argv):
    """Lit, reconstruit, écrit, résume ; rend le code de sortie.

    ① RÔLE — Porter la ligne de commande.
    ② CONTEXTE D'APPEL — Le bloc final ; les épreuves.
    ③ ENTRÉE — `argv` : la racine, et facultativement « --ligne VALEUR AAAA-MM-JJ ».
    ④ CONDITIONS D'ENTRÉE — ④ du programme.
    ⑤ SORTIE — UNE valeur : 0 ou 2 (⑤ du programme).
      [rend: 1]
    ⑥ TRAITEMENT — ⑥ du programme.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un instrument qui n'a pas pu tourner ne rend jamais 0 (R-734).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit les deux tables (sauf avec --ligne). Affiche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if not argv or not os.path.isdir(argv[0]):
        print("USAGE : RECONSTRUIRE_L_HISTORIQUE_LONG.py <racine> [--ligne VALEUR AAAA-MM-JJ]")
        return 2
    os.chdir(argv[0])
    try:
        fichier, _, _ = K.lire_cours(K.FICHIER)
        bnains, defauts_b, _ = K.lire_cours(K.BNAINS, COURS_BNAINS)
        K.oter_les_barres_fausses(K.FAUSSES, bnains)
        maitre, _, _ = K.lire_cours(MAITRE, K.CHAMPS)
        sources_maitre = {(r["valeur"], r["date"]): r["source"]
                          for r in csv.DictReader(open(MAITRE, encoding="utf-8"))}
        a_defaire = K.lire_a_defaire(K.VERDICTS_YAHOO)
        evenements = json.load(open(K.EVENEMENTS, encoding="utf-8"))
        detachements, _ = K.lire_detachements(K.DROITS, K.OFFICIELS)
    except (OSError, ValueError) as e:
        print(f"ARRÊT — la reconstruction n'a pas pu tourner : {type(e).__name__} : {e}")
        return 2
    if not fichier or not bnains or defauts_b:
        print("ARRÊT — le fichier réparé ou l'extrait bnains est vide ou illisible")
        return 2
    brut, google = bruts(bnains, maitre, sources_maitre)
    divisions = lire_divisions(DIVISIONS)
    if not divisions:
        print(f"ATTENTION — {DIVISIONS} absent ou vide : pas de confrontation à la table des divisions de bnains")
    ops, avis = operations(evenements, a_defaire, detachements, bnains, divisions)
    ops = deduire(fichier, brut, ops)
    if "--ligne" in argv:
        i = argv.index("--ligne")
        print(expliquer(argv[i + 1], argv[i + 2], fichier, brut, ops))
        return 0
    lignes, par_op = reconstruire(fichier, brut, ops, google, avis)
    with open(PAR_OPERATION, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["valeur", "date", "nature", "source", "facteur", "ecart_median_avant", "ecart_median_apres",
                    "lignes_avant", "lignes_apres", "ecart_du_facteur_applique", "bnains"])
        for v, d, nature, source, fa, ea, ep, na, np_, eo, bn in par_op:
            w.writerow([v, d, nature, source, "" if fa is None else f"{fa:.6f}",
                        "" if ea is None else f"{ea:+.6f}", "" if ep is None else f"{ep:+.6f}", na, np_,
                        f"{eo:+.6f}", bn])
    with open(ECARTS, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["valeur", "date", "close_fichier", "close_brut", "source_brut", "facteur", "ecart", "statut"])
        for v, d, c, b, src, p, e, statut in lignes:
            if statut not in ("reconstruite", "sans cours brut", "confirmée par Google"):
                w.writerow([v, d, c, "" if b is None else b, src, "" if p is None else f"{p:.6f}",
                            "" if e is None else f"{e:+.6f}", statut])
    compte = {}
    for *_, statut in lignes:
        compte[statut] = compte.get(statut, 0) + 1
    print(f"lignes : {len(lignes)} · " + " · ".join(f"{k} : {n}" for k, n in sorted(compte.items())))
    ecartes = [x for x in par_op if abs(x[9]) > 0]
    jours = {(x[0], x[1]) for x in ecartes}
    print(f"opérations : {len(par_op)} · jours d'opération où le facteur appliqué par le fichier s'écarte du facteur "
          f"documenté de plus de {TOLERANCE:.1%} : {len(jours)} ({len(ecartes)} opérations)")
    for v, d, nature, source, fa, ea, ep, na, np_, eo, bn in sorted(ecartes, key=lambda x: (x[0], x[1])):
        print(f"  {v} {d} — {nature[:70]} : facteur appliqué = documenté × {1 + eo:.6f} ({100 * eo:+.3f} %)")
    print(f"écrit : {PAR_OPERATION} · {ECARTS}")
    return 0


if __name__ == "__main__":
    try:
        code = main(sys.argv[1:])
    except Exception as e:
        print(f"ARRÊT — erreur imprévue {type(e).__name__} : {e}")
        code = 2
    sys.exit(code)
