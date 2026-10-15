#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMBLER_LE_TROU_DEPUIS_EURONEXT.py — Jeu 24-09-2026 (Paris)
Rôle : préparer les séances manquantes d'une période, prises chez Euronext, pour
que le programme de versement les ajoute au fichier maître des cours.

À QUOI IL SERT, ET SUR QUELS FAITS IL REPOSE
Du 13-07 au 30-07-2026, soit 14 séances, le fichier maître `donnees/cours_maitre.csv`
ne portait que 10 valeurs sur 39 (A-473). Euronext, la bourse elle-même, publie ces
séances. Mesure du 24-09-2026, sur les séances du 15-06 au 23-09-2026 que le maître
possédait déjà : les quatre prix d'Euronext sont identiques au centime à ceux d'ABC
sur 431 lignes sur 431, et à ceux de Google sur 2 021 lignes sur 2 040 ; les 19
autres diffèrent d'un ou deux centimes sur le plus haut ou le plus bas.

CE QU'IL NE FAIT PAS, ET C'EST VOULU : il n'écrit JAMAIS le fichier maître. Il écrit
un fichier témoin, que `programmes/TENIR_L_HISTORIQUE.py --increment` verse ensuite
avec toutes ses protections : le maître ne rétrécit pas, et une séance déjà présente
qui diffère arrête tout sans rien écrire. Deux programmes qui écriraient le même
fichier divergeraient un jour (R-708).

① RÔLE — Construire le fichier des couples valeur-séance absents du maître sur une
  période, avec les cours d'Euronext et la source « euronext », après avoir prouvé
  pour chaque valeur que les cours d'Euronext sont bien les siens.
② CONTEXTE D'APPEL — À la main, une fois par trou constaté. Aucune tâche du soir ne
  l'appelle. Premier usage : le trou de juillet 2026 (A-473).
③ ENTRÉE — La ligne de commande : la racine du dépôt ; `--du AAAA-MM-JJ` et
  `--au AAAA-MM-JJ`, les bornes du trou, incluses ; `--brut DOSSIER`, le dossier des
  fichiers bruts d'Euronext, un par code ISIN, chemin relatif à la racine ;
  `--telecharger` pour les télécharger d'abord dans ce dossier. Et trois fichiers :
  le maître, le référentiel des valeurs le plus récent, et les fichiers bruts.
④ CONDITIONS D'ENTRÉE — La racine est un clone du dépôt. Chaque valeur à combler a
  son fichier brut, qui couvre aussi des séances hors du trou : c'est sur elles que se
  fait le calibrage.
⑤ SORTIE — Un code de sortie, et un fichier : `temoins/TEMOIN_EURONEXT_TROU_<du>_AU_<au>.csv`,
  aux huit colonnes du maître, déclarées dans `programmes/CONTRATS_DES_FICHIERS.py`.
⑥ TRAITEMENT — ① lire le maître et le référentiel · ② retenir les valeurs présentes
  au maître AVANT et APRÈS le trou : une valeur entrée plus tard n'a pas de trou, elle
  n'a pas encore d'histoire · ③ télécharger si demandé · ④ pour chaque valeur,
  calibrer : sur les 10 séances qui précèdent le trou et les 10 qui le suivent, la
  clôture d'Euronext doit être celle du maître à un demi-centime près, sinon tout
  s'arrête ·
  ⑤ relever dans le trou les séances qu'Euronext publie et que le maître n'a pas ·
  ⑥ exiger que chaque séance du trou connue du maître soit publiée par Euronext pour
  chaque valeur retenue, et qu'Euronext ne publie aucune séance inconnue du maître ·
  ⑦ s'arrêter s'il n'y a rien à combler · ⑧ écrire le témoin, trié par valeur puis
  par date.
⑦ UNITÉ — Prix en euros, volume en nombre de titres échangés à Paris, dates au format
  AAAA-MM-JJ. Les comptes affichés sont des nombres de LIGNES valeur-séance.
⑧ POURQUOI — Combler à la main ou avec une source non calibrée ferait entrer dans le
  maître des cours dont rien ne garantit l'origine. Le calibrage rend impossible
  l'erreur la plus traîtresse : un code ISIN qui désigne une autre action, dont les
  cours seraient plausibles mais faux. Mesuré le 24-09-2026 : trois codes ISIN du
  référentiel ne rendent rien chez Euronext.
⑨ CE QUI CLOCHE — Les codes de `CORRECTIONS_ISIN` doublent le référentiel pour trois
  valeurs tant que le référentiel n'est pas corrigé : c'est une seconde source,
  inscrite au BACKLOG pour disparaître. Les volumes d'Euronext diffèrent de ceux de
  Google ou d'ABC sur quelques séances — mesuré le 24-09-2026 : plus de 1 % d'écart
  sur 18 lignes Google sur 2 040 et sur 6 lignes ABC sur 431 — ; le témoin porte le
  volume d'Euronext, et la source « euronext » le dit.
⑩ EFFET — Écrit le témoin dans `temoins/` ; avec `--telecharger`, écrit un fichier
  brut par valeur dans le dossier `--brut`. Change le dossier de travail pour la
  racine. N'écrit rien d'autre, et jamais le maître.
⑪ TERMINAISON — Ne rend jamais la main : 0 = témoin écrit · 1 = calibrage échoué,
  séance manquante, séance inconnue, fichier brut illisible, ou rien à combler, et
  rien n'est écrit ·
  2 = ligne de commande incomplète. Un téléchargement peut attendre jusqu'à 60
  secondes par valeur, puis échoue.

USAGE : python3 COMBLER_LE_TROU_DEPUIS_EURONEXT.py <racine> --du AAAA-MM-JJ --au AAAA-MM-JJ --brut DOSSIER [--telecharger]

⑫ DÉFINITIONS —
  le maître : `donnees/cours_maitre.csv`, le fichier unique qui porte tout
    l'historique des cours.
  le trou : une suite de séances où le maître n'a pas toutes les valeurs.
  un fichier brut : le fichier CSV tel qu'Euronext le rend, nommé `<ISIN>.csv`.
  le calibrage : la vérification, faite avant tout usage, que la source reproduit au
    centime des cours déjà connus.
  une séance : une journée de bourse pour une valeur, avec son ouverture, son plus
    haut, son plus bas, sa clôture et son volume.
"""

import csv, os, re, sys, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from TENIR_L_HISTORIQUE import cle_valeur, lire, MAITRE      # une seule règle de graphie (R-708)
from CONTRATS_DES_FICHIERS import COURS_MAITRE               # les huit colonnes, déclarées une fois
from COMMUN import le_plus_recent                            # le même choix de référentiel que la collecte

# Trois codes du référentiel ne rendent AUCUNE séance chez Euronext — mesuré le
# 24-09-2026. Ceux-ci rendent des clôtures identiques au maître : le calibrage le
# reprouve à chaque exécution. À retirer quand le référentiel sera corrigé (BACKLOG).
CORRECTIONS_ISIN = {
    "DASSAULT SYSTEMES": "FR0014003TT8",
    "MICHELIN": "FR001400AJ45",
    "UNIBAIL-RODAMCO-WESTFIELD": "FR0013326246",
}
ADRESSE = ("https://live.euronext.com/en/ajax/AwlHistoricalPrice/getFullDownloadAjax/"
           "{isin}-XPAR?format=csv&decimal_separator=.&date_form=Y-m-d&op=&adjusted=N"
           "&base100=&startdate={debut}&enddate={fin}")
# LE CALIBRAGE PORTE SUR LES BORDS DU TROU, là où les séances ajoutées se raccordent.
# Mesuré le 24-09-2026 : plus loin, un calibrage peut échouer pour une raison qui ne
# touche pas le trou — AIR LIQUIDE, du 03-06 au 08-06-2026, maître 163,55 contre
# Euronext 179,90, un rapport de 1,1 : l'historique Google est ajusté d'une
# attribution d'actions gratuites, Euronext rend les cours bruts.
SEANCES_DE_BORD = 10        # séances comparées de chaque côté du trou
# UN DEMI-CENTIME, en euros. Mesuré le 24-09-2026 : Euronext publie des prix au
# demi-centime (CARREFOUR 16,255 le 25-06-2026) que Google arrondit (16,26).
ECART_TOLERE = 0.005


def propre(texte):
    """Écrit un nombre comme le maître l'écrit : sans zéro inutile après la virgule.

    ① RÔLE — Rendre « 45.90 » en « 45.9 » et « 48.00 » en « 48 », comme les lignes
      déjà présentes au maître, sans passer par un nombre à virgule flottante qui
      pourrait changer un chiffre.
    ② CONTEXTE D'APPEL — `lire_euronext`, pour chacun des cinq champs d'une séance.
    ③ ENTRÉE — `texte` : un nombre écrit par Euronext, par exemple « 193.9400 ».
    ④ CONDITIONS D'ENTRÉE — Aucune : un texte sans point est rendu sans ses espaces.
    ⑤ SORTIE — UNE valeur : le texte raccourci.
      [rend: 1]
    ⑥ TRAITEMENT — ① retirer les espaces · ② si le texte porte un point, retirer les
      zéros de fin, puis le point s'il termine le texte.
    ⑦ UNITÉ — Celle du nombre reçu, inchangée.
    ⑧ POURQUOI — Mesuré le 24-09-2026 : le maître écrit « 35 » et « 44.9 », jamais
      « 35.00 ». Deux écritures d'un même prix feraient croire à une révision.
    ⑨ CE QUI CLOCHE — Rien de relevé.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    t = texte.strip()
    if "." in t:
        t = t.rstrip("0").rstrip(".")
    return t


def lire_euronext(chemin):
    """Lit un fichier brut d'Euronext et rend ses séances, date par date.

    ① RÔLE — Transformer le fichier tel qu'Euronext le rend en séances utilisables :
      date au format AAAA-MM-JJ, cinq champs écrits comme au maître.
    ② CONTEXTE D'APPEL — `main`, une fois par valeur retenue.
    ③ ENTRÉE — `chemin` : le fichier brut d'une valeur.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe. Ses lignes de séance sont séparées par
      des points-virgules et commencent par une date jj/mm/aaaa ; les autres lignes
      (titre, période, code, en-tête) sont ignorées.
    ⑤ SORTIE — UNE valeur : un dictionnaire {date: {open, high, low, close, volume}}.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire le fichier en retirant la marque d'ordre des octets ·
      ② garder les lignes dont le premier champ est une date jj/mm/aaaa · ③ prendre
      l'ouverture, le plus haut, le plus bas, la CLÔTURE (6e champ, et non « Last »,
      le 5e) et le nombre de titres (7e champ).
    ⑦ UNITÉ — Prix en euros, volume en titres.
    ⑧ POURQUOI — Mesuré le 24-09-2026 : Euronext rend ses dates en jj/mm/aaaa même
      quand on lui demande AAAA-MM-JJ ; une première comparaison qui l'ignorait n'a
      trouvé aucune séance commune.
    ⑨ CE QUI CLOCHE — Une séance sans volume rend un volume vide ; le calibrage ne
      porte pas sur le volume et ne le voit donc pas.
    ⑩ EFFET — Aucun : lecture seule.
    ⑪ TERMINAISON — Rend la main ; lève si le fichier manque ou si un champ de prix
      n'est pas un nombre — `main` en fait un arrêt.
      [sort: non]
    """
    seances = {}
    with open(chemin, encoding="utf-8-sig") as f:
        for ligne in f.read().splitlines():
            p = ligne.split(";")
            if len(p) >= 7 and re.fullmatch(r"\d\d/\d\d/\d{4}", p[0]):
                jj, mm, aa = p[0].split("/")
                for x in p[1:4] + p[5:6]:
                    float(x)
                seances[f"{aa}-{mm}-{jj}"] = dict(
                    open=propre(p[1]), high=propre(p[2]), low=propre(p[3]),
                    close=propre(p[5]), volume=propre(p[6]))
    return seances


def telecharger(isin, debut, fin, chemin):
    """Télécharge chez Euronext le fichier brut d'une valeur sur une période.

    ① RÔLE — Aller chercher la source primaire, et la garder telle quelle sur le
      disque pour que toute la suite se refasse sans réseau.
    ② CONTEXTE D'APPEL — `main`, une fois par valeur retenue, seulement avec
      `--telecharger`.
    ③ ENTRÉE — `isin` : le code de la valeur · `debut`, `fin` : la période, au format
      AAAA-MM-JJ · `chemin` : le fichier à écrire.
    ④ CONDITIONS D'ENTRÉE — Le réseau atteint live.euronext.com. Le GET fonctionne,
      le POST non — mesuré le 24-09-2026 : « No format specified ».
    ⑤ SORTIE — Rend `None`.
      [rend: rien]
    ⑥ TRAITEMENT — ① composer l'adresse · ② la lire, 60 secondes au plus · ③ écrire
      les octets reçus, sans les transformer.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le fichier brut est la preuve de l'origine : on le garde au dépôt.
    ⑨ CE QUI CLOCHE — Un fichier reçu vide ou sans séance n'est pas refusé ici :
      c'est le calibrage qui l'arrête, faute de séances communes.
    ⑩ EFFET — ÉCRIT `chemin`, en le remplaçant.
    ⑪ TERMINAISON — Rend la main, ou lève après 60 secondes sans réponse, ou sur une
      erreur du réseau.
      [sort: non]
    """
    adresse = ADRESSE.format(isin=isin, debut=debut, fin=fin)
    octets = urllib.request.urlopen(adresse, timeout=60).read()
    with open(chemin, "wb") as f:
        f.write(octets)


def option(nom):
    """Rend la valeur qui suit une option sur la ligne de commande, ou rien.

    ① RÔLE — Lire `--du`, `--au` et `--brut` sans confondre leur valeur avec l'option
      suivante.
    ② CONTEXTE D'APPEL — `main`, trois fois, au début.
    ③ ENTRÉE — `nom` : le nom de l'option, par exemple « --du ».
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : le texte qui suit l'option, ou `None` si l'option manque,
      termine la ligne, ou est suivie d'une autre option.
      [rend: 1]
    ⑥ TRAITEMENT — ① chercher l'option dans `sys.argv` · ② prendre le mot suivant s'il
      existe et ne commence pas par « -- ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une option sans valeur doit arrêter le programme, et non prendre
      l'option suivante pour valeur : « --du --au 2026-07-30 » donnerait sinon « --au »
      comme date de début.
    ⑨ CE QUI CLOCHE — Une option écrite deux fois : seule la première compte, sans un mot.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    if nom in sys.argv:
        i = sys.argv.index(nom)
        if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("--"):
            return sys.argv[i + 1]
    return None


def main():
    """Prépare le témoin des séances manquantes, ou s'arrête sans rien écrire.

    ① RÔLE — Enchaîner le choix des valeurs, le calibrage, le relevé des manques et
      l'écriture du témoin ; refuser tout ou rien.
    ② CONTEXTE D'APPEL — Le lancement du programme, à la main.
    ③ ENTRÉE — La ligne de commande décrite en tête du programme.
    ④ CONDITIONS D'ENTRÉE — Celles du programme : racine, bornes, dossier brut.
    ⑤ SORTIE — Ne rend rien : code de sortie et affichage.
      [rend: rien]
    ⑥ TRAITEMENT — Les huit étapes décrites en tête du programme.
    ⑦ UNITÉ — Comptes en lignes valeur-séance.
    ⑧ POURQUOI — TOUT OU RIEN : un comblement partiel laisserait un trou plus petit
      et moins visible, ce qui est pire que le trou entier.
    ⑨ CE QUI CLOCHE — Voir la tête du programme : la table `CORRECTIONS_ISIN`.
    ⑩ EFFET — Écrit le témoin, et les fichiers bruts avec `--telecharger`.
    ⑪ TERMINAISON — Ne rend jamais la main : codes 0, 1, 2 décrits en tête.
      [sort: oui]
    """
    du, au, brut = option("--du"), option("--au"), option("--brut")
    if len(sys.argv) < 2 or not (du and au and brut) or sys.argv[1].startswith("--"):
        print(__doc__.split("⑫")[0]); sys.exit(2)
    for d in (du, au):
        if not re.fullmatch(r"\d{4}-\d\d-\d\d", d):
            print(f"  ❌ ARRÊT : date illisible « {d} », format attendu AAAA-MM-JJ."); sys.exit(2)
    os.chdir(sys.argv[1])

    # ① le maître et le référentiel
    maitre, orthographe = {}, {}
    for r in lire(MAITRE):
        k = cle_valeur(r["valeur"])
        maitre[(k, r["date"])] = r
        if r["date"] > au and (k not in orthographe or r["date"] < orthographe[k][0]):
            orthographe[k] = (r["date"], r["valeur"])
    if not maitre:
        print(f"  ❌ ARRÊT : {MAITRE} est absent ou vide."); sys.exit(1)
    noms = [f for f in os.listdir("donnees")
            if f.upper().startswith("REFERENTIEL_VALEURS") and f.endswith(".csv")]
    referentiel = os.path.join("donnees", le_plus_recent(noms))
    with open(referentiel, encoding="utf-8-sig") as f:
        isin_de = {cle_valeur(r["nom_usuel"]): CORRECTIONS_ISIN.get(r["nom_usuel"], r["isin"]).strip()
                   for r in csv.DictReader(f)}

    # ② les valeurs qui ont un trou : présentes avant ET après
    avant = {k for (k, d) in maitre if d < du}
    apres = {k for (k, d) in maitre if d > au}
    retenues = sorted(avant & apres)
    sans_isin = [k for k in retenues if k not in isin_de]
    if sans_isin:
        print(f"  ❌ ARRÊT : valeurs du maître absentes du référentiel : {sans_isin}"); sys.exit(1)
    dates_connues = sorted({d for (k, d) in maitre if du <= d <= au})
    print(f"  trou du {du} au {au} · {len(dates_connues)} séance(s) connue(s) du maître "
          f"· {len(retenues)} valeur(s) présente(s) avant et après")

    # ③ ④ ⑤ ⑥ par valeur : télécharger, calibrer, relever
    os.makedirs(brut, exist_ok=True)
    manques, refus = [], []
    for k in retenues:
        chemin = os.path.join(brut, f"{isin_de[k]}.csv")
        try:
            if "--telecharger" in sys.argv:
                telecharger(isin_de[k], _jours_avant(du, 40), _jours_apres(au, 40), chemin)
            eu = lire_euronext(chemin)
        except Exception as e:
            refus.append(f"{k} ({isin_de[k]}) : fichier brut illisible — {e}"); continue
        bord_avant = sorted(d for d in eu if d < du and (k, d) in maitre)[-SEANCES_DE_BORD:]
        bord_apres = sorted(d for d in eu if d > au and (k, d) in maitre)[:SEANCES_DE_BORD]
        communes = bord_avant + bord_apres
        faux = [d for d in communes          # 1e-9 : la marge d'arrondi des nombres à virgule
                if abs(float(eu[d]["close"]) - float(maitre[(k, d)]["close"])) > ECART_TOLERE + 1e-9]
        if len(bord_avant) < SEANCES_DE_BORD or len(bord_apres) < SEANCES_DE_BORD or faux:
            refus.append(f"{k} ({isin_de[k]}) : calibrage échoué — {len(bord_avant)} séance(s) "
                         f"avant, {len(bord_apres)} après, {len(faux)} clôture(s) différente(s), "
                         f"ex. {faux[:3]}")
            continue
        dans_le_trou = {d for d in eu if du <= d <= au}
        inconnues = sorted(dans_le_trou - set(dates_connues))
        absentes = sorted(set(dates_connues) - dans_le_trou)
        if inconnues or absentes:
            refus.append(f"{k} : séances inconnues du maître {inconnues} · "
                         f"séances non publiées par Euronext {absentes}")
            continue
        for d in sorted(dans_le_trou):
            if (k, d) not in maitre:
                manques.append(dict(eu[d], valeur=orthographe[k][1], date=d, source="euronext"))
        print(f"  ✅ {k:<28} calibré sur {len(communes)} séances · "
              f"{sum(1 for m in manques if cle_valeur(m['valeur']) == k)} à combler")

    if refus:
        print(f"  ❌ ARRÊT — {len(refus)} refus, RIEN N'EST ÉCRIT :")
        for r in refus:
            print(f"     · {r}")
        sys.exit(1)

    # RIEN À COMBLER N'EST PAS UN SUCCÈS SILENCIEUX : relancé après le versement, le
    # programme écraserait le témoin déposé par un fichier vide. Trouvé le 24-09-2026
    # par le mandat inversé de son auteur.
    if not manques:
        print(f"  ⚠️ RIEN À COMBLER du {du} au {au} : aucun témoin écrit.")
        sys.exit(1)

    # ⑦ le témoin
    os.makedirs("temoins", exist_ok=True)
    sortie = os.path.join("temoins", f"TEMOIN_EURONEXT_TROU_{du}_AU_{au}.csv")
    manques.sort(key=lambda m: (cle_valeur(m["valeur"]), m["date"]))
    with open(sortie, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COURS_MAITRE)
        w.writeheader()
        w.writerows(manques)
    print(f"  écrit : {sortie} · {len(manques)} ligne(s) valeur-séance")
    sys.exit(0)


def _jours_avant(date, n):
    """Rend la date située n jours calendaires avant `date`.

    ① RÔLE — Élargir la période téléchargée pour que le calibrage ait des séances
      hors du trou, avant lui.
    ② CONTEXTE D'APPEL — `main`, avec `--telecharger`, une fois par valeur.
    ③ ENTRÉE — `date` : AAAA-MM-JJ · `n` : un nombre de jours.
    ④ CONDITIONS D'ENTRÉE — `date` est une date valide.
    ⑤ SORTIE — UNE valeur : la date décalée, au format AAAA-MM-JJ.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire la date · ② retirer n jours · ③ la réécrire.
    ⑦ UNITÉ — Jours calendaires.
    ⑧ POURQUOI — 40 jours calendaires donnent environ 28 séances, au-dessus des
      10 séances de bord qu'exige le calibrage, même avec des jours fériés.
    ⑨ CE QUI CLOCHE — Rien de relevé.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève sur une date invalide.
      [sort: non]
    """
    from datetime import date as _d, timedelta
    return (_d.fromisoformat(date) - timedelta(days=n)).isoformat()


def _jours_apres(date, n):
    """Rend la date située n jours calendaires après `date`.

    ① RÔLE — Élargir la période téléchargée pour que le calibrage ait des séances
      hors du trou, après lui.
    ② CONTEXTE D'APPEL — `main`, avec `--telecharger`, une fois par valeur.
    ③ ENTRÉE — `date` : AAAA-MM-JJ · `n` : un nombre de jours.
    ④ CONDITIONS D'ENTRÉE — `date` est une date valide.
    ⑤ SORTIE — UNE valeur : la date décalée, au format AAAA-MM-JJ.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire la date · ② ajouter n jours · ③ la réécrire.
    ⑦ UNITÉ — Jours calendaires.
    ⑧ POURQUOI — Symétrique de `_jours_avant`.
    ⑨ CE QUI CLOCHE — Rien de relevé.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève sur une date invalide.
      [sort: non]
    """
    from datetime import date as _d, timedelta
    return (_d.fromisoformat(date) + timedelta(days=n)).isoformat()


if __name__ == "__main__":
    main()
