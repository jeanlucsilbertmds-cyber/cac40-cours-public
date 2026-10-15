#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COLLECTER_LE_CONSENSUS.py — Jeu 01-10-2026 (Paris) — PROPOSÉ, non validé.
Rôle : chaque soir, lire chez EasyBourse le consensus des analystes des valeurs
du référentiel, et l'EMPILER dans donnees/consensus_easybourse.csv.
Simulation uniquement : ce programme lit des pages publiques, il ne passe rien.

① RÔLE — Relever, pour chaque valeur du référentiel, le tableau « Consensus »
  d'EasyBourse : nombre d'avis Acheter, Renforcer, Conserver, Alléger, Vendre,
  nombre d'analystes, note, objectif de cours, chacun sur quatre colonnes (il y
  a 3 mois, il y a 1 mois, il y a 7 jours, actuel), plus la date « Prévisions
  des résultats (au JJ/MM/AAAA) » qui dit l'âge de la page. Puis ajouter ces
  lignes, datées du jour de lecture, au fichier qui grandit.
② CONTEXTE D'APPEL — Prévu : un circuit GitHub Actions à part,
  .github/workflows/collecte_consensus.yml, chaque soir de semaine, séparé du
  circuit des cours pour qu'une panne d'EasyBourse ne puisse jamais arrêter la
  collecte des cours. À la main : python3 programmes/COLLECTER_LE_CONSENSUS.py <racine>.
③ ENTRÉE — Un argument : la racine du dépôt. Option --pages DOSSIER : relire des
  pages déjà téléchargées au lieu d'aller sur le site (épreuves hors ligne).
④ CONDITIONS D'ENTRÉE — Un seul fichier donnees/REFERENTIEL_VALEURS_*.csv sous
  la racine, avec les colonnes nom_usuel, mnemonique et isin. L'accès réseau à
  www.easybourse.com, sauf avec --pages.
⑤ SORTIE — UNE valeur : le code de sortie. 0 = toutes les valeurs lues et
  écrites · 1 = au moins une valeur non lue (nommée à l'écran), les autres
  écrites quand même · 2 = rien n'a pu être fait (racine, référentiel ou fichier
  de sortie illisible, ou fichier de sortie qui n'est pas celui que ce programme
  laisse : en-tête autre que `CHAMPS`, une ligne qui n'a pas autant de champs,
  ou pas de « \n » final ; ou toute erreur imprévue, lancé en ligne de commande). Plus les lignes ajoutées au fichier, et un résumé à l'écran.
⑥ TRAITEMENT — ① lire le référentiel · ② pour chaque valeur, télécharger la page
  consensus par son ISIN ; si la page n'a pas de tableau, chercher l'adresse par
  la recherche du site · ③ lire le tableau (`lire_page`) · ④ vérifier l'identité :
  l'ISIN de la page doit être celui du référentiel · ⑤ refuser d'empiler deux
  fois la même valeur le même jour · ⑥ ajouter les lignes · ⑦ sortir.
⑦ UNITÉ — Des NOMBRES D'ANALYSTES (entiers), une NOTE de 1 (Acheter) à 5 (Vendre),
  des OBJECTIFS en EUROS, des DATES de calendrier en heure de Paris.
⑧ POURQUOI — Le 01-10-2026, mesuré : le consensus FactSet de Boursorama est figé
  au 18-08-2026 (fiche TotalEnergies identique sur 46 champs sur 49 entre le
  10-09 et le 01-10 ; liste du 21-09 identique à celle du 01-10, 8 valeurs sur 8).
  EasyBourse montre le même tableau, même échelle, même calcul de note (moyenne
  pondérée vérifiée 160 cellules sur 160), mais avec des chiffres différents et
  des prévisions datées du 26-09-2026. Empiler chaque soir est le seul moyen de
  savoir s'il bouge, et le seul moyen de constituer un historique : un consensus
  non relevé un jour est perdu, le site ne garde que quatre dates.
⑨ CE QUI CLOCHE — La source réelle d'EasyBourse n'est écrite nulle part sur la
  page : le format FactSet le suggère, rien ne le prouve. · Le référentiel porte
  trois ISIN périmés (Dassault Systèmes, Michelin, URW) : ces trois valeurs
  tombent en code 1 tant qu'il n'est pas corrigé — c'est voulu, une valeur
  attendue qui ne renvoie rien est une alerte. MAIS tant qu'il n'est pas corrigé,
  le circuit est rouge CHAQUE soir, et une quatrième valeur qui tomberait ne
  changerait rien à ce rouge : l'alerte est muette dès le premier soir (relecture
  de Cowork du 03-10-2026, cassure 2). · Le 01-10-2026, Hermès n'était trouvé
  que par la recherche du site ; le 03-10-2026, il l'est par son adresse directe
  (relecture de Cowork). · La page est en windows-1252 (le symbole euro arrive
  en octet 0x80) et elle est décodée en latin-1 : cela ne change aucun chiffre
  (relecture de Cowork du 03-10-2026). → BACKLOG.
⑩ EFFET — Ajoute des lignes à donnees/consensus_easybourse.csv (le crée s'il
  n'existe pas). Ne modifie ni n'efface jamais une ligne existante. N'ajoute
  rien si le fichier existant n'est pas celui que ce programme laisse : en-tête
  exactement `CHAMPS`, chaque ligne avec autant de champs, « \n » final (code 2).
  Lancé sans --pages, laisse les pages téléchargées dans .consensus_pages/ (que
  Git ignore, et que le circuit efface).
⑪ TERMINAISON — Toujours : chaque téléchargement est borné à 40 secondes et ne
  se répète pas. Aucun de mes appels ne peut boucler.
"""
import csv, glob, html, os, re, subprocess, sys, time
from datetime import datetime
from zoneinfo import ZoneInfo

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124 Safari/537.36")
SITE = "https://www.easybourse.com"
SORTIE = os.path.join("donnees", "consensus_easybourse.csv")
LIGNES = {"Acheter": "acheter", "Renforcer": "renforcer", "Conserver": "conserver",
          "Alléger": "alleger", "Vendre": "vendre", "Nb analystes": "nb_analystes",
          "Note médiane": "note", "Historique des objectifs de cours": "objectif"}
COLONNES = ["m3", "m1", "j7", "actuel"]
ENTETES = ["Il y a 3 mois", "Il y a 1 mois", "Il y a 7 jours", "Actuel"]
CHAMPS = (["date_lecture", "valeur", "mnemonique", "isin", "adresse", "previsions_au"]
          + [f"{v}_{c}" for v in LIGNES.values() for c in COLONNES])


def lire_page(s):
    """
    ① RÔLE — Lire, dans le texte d'une page consensus EasyBourse, le tableau des
      avis et la date des prévisions.
    ② CONTEXTE D'APPEL — `collecter`, une fois par page ; les épreuves.
    ③ ENTRÉE — `s` : le texte de la page, déjà décodé.
    ④ CONDITIONS D'ENTRÉE — Aucune : une page sans tableau lève une erreur nommée.
    ⑤ SORTIE — UNE valeur : un dictionnaire, 32 grandeurs (8 lignes × 4 colonnes),
      plus `isin_page` et `previsions_au`. Ou ValueError qui dit ce qui manque.
      [rend: 1]
    ⑥ TRAITEMENT — trouver le tableau par ses en-têtes, exiger exactement les quatre
      en-têtes attendus dans l'ordre, lire chaque ligne connue, exiger quatre
      nombres, exiger que les 32 soient là.
    ⑦ UNITÉ — Celles du programme (⑦ plus haut).
    ⑧ POURQUOI — Lire par cellules et vérifier les en-têtes : un changement de mise
      en page doit arrêter la lecture, pas décaler les colonnes en silence.
    ⑨ CE QUI CLOCHE — Seul le premier tableau qui porte « Il y a 3 mois » est lu.
      Les deux pages témoins du 02-10-2026 n'en portent qu'un, hors commentaire
      HTML (relecture de Cowork du 03-10-2026) ; la phrase écrite d'abord ici, « la
      page contient le tableau deux fois », était fausse.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Toujours. Aucun appel externe.
      [sort: non]
    """
    i = s.find("Il y a 3 mois")
    if i < 0:
        raise ValueError("tableau du consensus absent")
    t0, t1 = s.rfind("<table", 0, i), s.find("</table>", i)
    tab = s[t0:t1]
    ent = [html.unescape(re.sub(r"<[^>]+>", "", h)).strip()
           for h in re.findall(r"<th[^>]*>(.*?)</th>", tab, re.S)]
    ent = [e for e in ent if e]
    if ent[-4:] != ENTETES:
        raise ValueError(f"en-têtes inattendus : {ent}")
    d = {}
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", tab, re.S):
        tds = [html.unescape(re.sub(r"<[^>]+>", "", x)).replace("\xa0", " ").strip()
               for x in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
        if not tds:
            continue
        lib = tds[0].replace("*", "").strip()
        if lib not in LIGNES:
            continue
        if len(tds) != 5:
            raise ValueError(f"ligne « {lib} » : {len(tds) - 1} cellules au lieu de 4")
        for c, v in zip(COLONNES, tds[1:]):
            d[f"{LIGNES[lib]}_{c}"] = nombre(v, lib, c)
    manq = [k for k in CHAMPS[6:] if k not in d]
    if manq:
        raise ValueError(f"grandeurs manquantes : {manq[:4]}")
    m = re.search(r"Pr(?:&eacute;|é)visions des r(?:&eacute;|é)sultats\s*<span>\(au (\d\d/\d\d/\d{4})\)", s)
    d["previsions_au"] = m.group(1) if m else ""
    isins = re.findall(r"[A-Z]{2}[A-Z0-9]{9}\d", s[:s.find("Il y a 3 mois")])
    d["isin_page"] = max(set(isins), key=isins.count) if isins else ""
    return d


def nombre(v, lib="", col=""):
    """
    ① RÔLE — Convertir le texte d'une cellule en nombre écrit à la façon Python.
    ② CONTEXTE D'APPEL — `lire_page`, pour chaque cellule.
    ③ ENTRÉE — `v` : le texte · `lib` et `col` : la ligne et la colonne, pour nommer l'erreur.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : le nombre en texte, point décimal, sans séparateur de
      milliers (« 2.000,00 » → « 2000.00 », « 86,86 » → « 86.86 », « 1.96 » → « 1.96 »).
      Ou ValueError si la cellule ne porte pas de nombre.
      [rend: 1]
    ⑥ TRAITEMENT — si la cellule contient une virgule, la virgule est la décimale et
      les points sont des milliers ; sinon le point est la décimale.
    ⑦ UNITÉ — Celle de la cellule.
    ⑧ POURQUOI — Le 01-10-2026, l'objectif d'Hermès « 2.000,00 » était lu 2.000 :
      un facteur mille, en silence. Les notes s'écrivent avec un point décimal,
      les objectifs avec une virgule : la page mélange les deux conventions.
    ⑨ CE QUI CLOCHE — Un nombre à point de milliers SANS virgule (« 2.000 ») serait
      lu 2 : le garde-fou de plausibilité de `collecter` est là pour ce cas.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Toujours.
      [sort: non]
    """
    m = re.search(r"-?\d[\d.,]*", v.replace(" ", ""))
    if not m:
        raise ValueError(f"ligne « {lib} », colonne {col} : cellule vide")
    t = m.group(0).rstrip(".,")
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    float(t)
    return t


def telecharger(adresse, chemin):
    """
    ① RÔLE — Télécharger une page dans un fichier.
    ② CONTEXTE D'APPEL — `collecter` et `chercher_adresse`.
    ③ ENTRÉE — `adresse` : l'URL · `chemin` : le fichier où écrire.
    ④ CONDITIONS D'ENTRÉE — Le dossier du chemin existe.
    ⑤ SORTIE — UNE valeur : le texte de la page décodé en latin-1, ou "" si rien n'est venu.
      [rend: 1]
    ⑥ TRAITEMENT — curl, 40 secondes au plus, une seule tentative.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une tentative seulement : répéter masquerait une source qui se dégrade.
    ⑨ CE QUI CLOCHE — Le code HTTP n'est pas rendu ; une page vide suffit à dire l'échec.
    ⑩ EFFET — Écrit le fichier `chemin`.
    ⑪ TERMINAISON — Toujours, au plus 40 secondes.
      [sort: non]
    """
    subprocess.run(["curl", "-sS", "-L", "--max-time", "40", "-A", UA, "-o", chemin, adresse],
                   capture_output=True)
    try:
        return open(chemin, "rb").read().decode("latin-1")
    except OSError:
        return ""


def chercher_adresse(isin, dossier):
    """
    ① RÔLE — Trouver l'adresse de la page consensus d'un ISIN par la recherche du site.
    ② CONTEXTE D'APPEL — `collecter`, quand la page par l'ISIN n'a pas de tableau.
    ③ ENTRÉE — `isin` : le code de la valeur · `dossier` : où ranger la page de recherche.
    ④ CONDITIONS D'ENTRÉE — Accès réseau.
    ⑤ SORTIE — UNE valeur : l'adresse complète, ou "" si aucune ne porte cet ISIN.
      [rend: 1]
    ⑥ TRAITEMENT — lancer la recherche, garder les liens /action-consensus/ qui
      contiennent l'ISIN exact, préférer le suffixe -25 (Paris).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Hermès, le 01-10-2026, n'a répondu que par son adresse nommée ;
      la recherche le trouve sans qu'on écrive son nom dans le code.
    ⑨ CE QUI CLOCHE — Dépend de la mise en page de la recherche.
    ⑩ EFFET — Écrit la page de recherche dans `dossier`.
    ⑪ TERMINAISON — Toujours, au plus 40 secondes.
      [sort: non]
    """
    s = telecharger(f"{SITE}/recherche?q={isin}", os.path.join(dossier, f"_recherche_{isin}.html"))
    liens = sorted(set(re.findall(r'/action-consensus/[^"\s]*/' + re.escape(isin) + r'-\d+', s)),
                   key=lambda u: (not u.endswith("-25"), u))
    return SITE + liens[0] if liens else ""


def collecter(racine, pages=None):
    """
    ① RÔLE — Faire le travail du programme (⑥ plus haut) et rendre son code de sortie.
    ② CONTEXTE D'APPEL — Le bloc de lancement, en bas du fichier ; les épreuves.
    ③ ENTRÉE — `racine` : la racine du dépôt · `pages` : un dossier de pages déjà
      téléchargées, ou None pour aller sur le site.
    ④ CONDITIONS D'ENTRÉE — Celles du programme (④ plus haut).
    ⑤ SORTIE — UNE valeur : le code de sortie, 0, 1 ou 2 (⑤ plus haut).
      [rend: 1]
    ⑥ TRAITEMENT — Celui du programme (⑥ plus haut).
    ⑦ UNITÉ — Celles du programme.
    ⑧ POURQUOI — Une fonction plutôt que du code au niveau du fichier : les épreuves
      l'appellent sur une copie.
    ⑨ CE QUI CLOCHE — Le jour de lecture est celui de l'horloge de Paris, pas celui
      de la page : deux lectures le même soir comptent pour une.
    ⑩ EFFET — Ajoute des lignes au fichier de sortie.
    ⑪ TERMINAISON — Toujours : une boucle sur les valeurs du référentiel, finie.
      [sort: non]
    """
    refs = sorted(glob.glob(os.path.join(racine, "donnees", "REFERENTIEL_VALEURS_*.csv")))
    if len(refs) != 1:
        print(f"ARRÊT : {len(refs)} référentiel(s) trouvé(s), il en faut exactement un")
        return 2
    valeurs = list(csv.DictReader(open(refs[0], encoding="utf-8-sig")))
    if not valeurs or not {"nom_usuel", "mnemonique", "isin"} <= set(valeurs[0]):
        print("ARRÊT : référentiel vide ou sans les colonnes nom_usuel, mnemonique, isin")
        return 2
    jour = datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d")
    sortie = os.path.join(racine, SORTIE)
    deja = set()
    if os.path.exists(sortie):
        # L'EN-TÊTE DU FICHIER EXISTANT DOIT ÊTRE `CHAMPS`, colonne pour colonne : les lignes s'ajoutent dans l'ordre
        # de `CHAMPS`, sous l'en-tête déjà écrit. Relecture de Cowork du 03-10-2026, cassure 1 : deux colonnes
        # échangées dans l'en-tête, et l'objectif d'Hermès était lu 24, le nombre d'analystes 2000.00, code 0.
        # LE FICHIER EXISTANT DOIT ÊTRE CELUI QUE CE PROGRAMME LAISSE, en entier — sinon rien n'est écrit (code 2).
        # Relecture de Cowork du 03-10-2026, deuxième tour, cas C4 : une ligne coupée à 6 champs sur 38, finie par
        # un saut de ligne, passait avec le seul contrôle de l'en-tête et du dernier octet.
        try:
            existantes = list(csv.reader(open(sortie, encoding="utf-8", newline="")))
            entete = existantes[0] if existantes else []
            if entete != CHAMPS:
                ecarts = [f"{i + 1} : {a!r} au lieu de {b!r}" for i, (a, b) in enumerate(zip(entete, CHAMPS)) if a != b]
                print(f"ARRÊT : l'en-tête de {SORTIE} n'est pas celui que ce programme écrit "
                      f"({len(entete)} colonnes au lieu de {len(CHAMPS)} ; "
                      f"écarts {ecarts[:3]}) — rien n'est écrit, les nombres changeraient de colonne")
                return 2
            # CHAQUE LIGNE A EXACTEMENT len(CHAMPS) CHAMPS ; une ligne vide en a zéro et est fautive aussi.
            fautives = [n for n, l in enumerate(existantes[1:], 2) if len(l) != len(CHAMPS)]
            if fautives:
                print(f"ARRÊT : {len(fautives)} ligne(s) de {SORTIE} n'ont pas {len(CHAMPS)} champs (ligne(s) "
                      f"{fautives[:5]}) — rien n'est écrit : le fichier n'est pas celui que ce programme laisse")
                return 2
            for l in existantes[1:]:
                deja.add((l[CHAMPS.index("date_lecture")], l[CHAMPS.index("isin")]))
            # LE FICHIER DOIT FINIR PAR « \n » : sinon la première ligne ajoutée se soude à la dernière, et deux
            # relevés deviennent une ligne fausse. Même famille que le défaut trouvé par Cowork le 06-09-2026 dans
            # programmes/CONTROLER_LES_COURS.py (qui, lui, ajoute le saut) ; ici on refuse, comme pour l'en-tête. Un
            # « \r » seul ne suffit pas : l'ajout y créait une ligne vide (relecture de Cowork du 03-10-2026, cas C2).
            with open(sortie, "rb") as f:
                f.seek(-1, os.SEEK_END)
                if f.read(1) != b"\n":
                    print(f"ARRÊT : {SORTIE} ne finit pas par un saut de ligne — rien n'est écrit, la ligne "
                          "ajoutée se souderait à la dernière")
                    return 2
        except csv.Error as e:
            print(f"ARRÊT : fichier de sortie illisible ({e})")
            return 2
    tmp = pages or os.path.join(racine, ".consensus_pages")
    os.makedirs(tmp, exist_ok=True)
    lues, echecs, sautees, pas_de_cours = [], [], 0, []
    derniers = {}
    maitre = os.path.join(racine, "donnees", "cours_maitre.csv")
    if os.path.exists(maitre):
        for x in csv.DictReader(open(maitre, encoding="utf-8")):
            if x["valeur"] not in derniers or x["date"] >= derniers[x["valeur"]][0]:
                derniers[x["valeur"]] = (x["date"], float(x["close"]))
    derniers = {k: v[1] for k, v in derniers.items()}
    for r in valeurs:
        nom, isin = r["nom_usuel"], r["isin"].strip()
        if (jour, isin) in deja:
            sautees += 1
            continue
        chemin = os.path.join(tmp, f"{isin}.html")
        adresse = f"{SITE}/action-consensus/x/{isin}-25"
        try:
            if pages:
                s = open(chemin, "rb").read().decode("latin-1")
            else:
                s = telecharger(adresse, chemin)
                time.sleep(0.7)
                if "Il y a 3 mois" not in s:
                    adresse = chercher_adresse(isin, tmp)
                    if not adresse:
                        raise ValueError("aucune page consensus pour cet ISIN")
                    s = telecharger(adresse, chemin)
            d = lire_page(s)
            if d["isin_page"] != isin:
                raise ValueError(f"IDENTITÉ : la page porte {d['isin_page']}, le référentiel {isin}")
            cours = derniers.get(nom)
            if cours:
                ratio = float(d["objectif_actuel"]) / cours
                if not 0.5 <= ratio <= 3.0:
                    raise ValueError(f"PLAUSIBILITÉ : objectif {d['objectif_actuel']} pour un dernier "
                                     f"cours de {cours} (rapport {ratio:.3f}, admis 0,5 à 3)")
            else:
                pas_de_cours.append(nom)
        except (ValueError, OSError) as e:
            echecs.append(f"{nom} ({isin}) : {e}")
            continue
        d.update(date_lecture=jour, valeur=nom, mnemonique=r["mnemonique"], isin=isin, adresse=adresse)
        lues.append({k: d[k] for k in CHAMPS})
    neuf = not os.path.exists(sortie)
    with open(sortie, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, CHAMPS)
        if neuf:
            w.writeheader()
        w.writerows(lues)
    ages = sorted({x["previsions_au"] for x in lues})
    print(f"CONSENSUS {jour} : {len(lues)} lue(s) · {len(echecs)} non lue(s) · "
          f"{sautees} déjà relevée(s) ce jour · prévisions au {ages}")
    for e in echecs:
        print(f"  ALERTE {e}")
    if pas_de_cours:
        print(f"  ATTENTION plausibilité non contrôlée, aucun cours au fichier maître : {pas_de_cours}")
    return 1 if echecs else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage : COLLECTER_LE_CONSENSUS.py <racine> [--pages DOSSIER]")
        sys.exit(2)
    p = sys.argv[sys.argv.index("--pages") + 1] if "--pages" in sys.argv else None
    # UNE ERREUR QUE `collecter` N'A PAS PRÉVUE REND 2, jamais 1 : le code 1 dit « une valeur non lue », et une
    # trace sortie en 1 le disait à tort (relecture de Cowork du 03-10-2026, cas C5 : un dossier à la place du
    # fichier de sortie).
    try:
        code = collecter(sys.argv[1], p)
    except Exception as e:
        print(f"ARRÊT : erreur imprévue, rien n'est garanti écrit — {type(e).__name__} : {e}")
        code = 2
    sys.exit(code)
