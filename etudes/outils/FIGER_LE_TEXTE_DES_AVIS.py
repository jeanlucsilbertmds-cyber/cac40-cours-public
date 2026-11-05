#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FIGER_LE_TEXTE_DES_AVIS — Dim 01-11-2026 (Paris). Simulation uniquement.

① RÔLE — Figer au dépôt, une fois, le texte de chaque avis PDF que cite le référentiel des valeurs, et prouver qu'il
  est fidèle : pdftotext 24.02.0 -layout, relancé sur l'avis, rend ce texte octet pour octet. Le texte figé vit dans
  donnees/sources_du_referentiel/textes_figes/<empreinte sha256 du PDF>.txt, avec une ligne au carnet
  donnees/PROVENANCE_DES_FICHIERS.csv qui dit son empreinte. programmes/VERIFIER_LES_PREUVES_DU_REFERENTIEL.py lit ce
  texte au lieu de lancer pdftotext.
② CONTEXTE D'APPEL — À la main, par le Chat ou par un relecteur, sur une machine où pdftotext 24.02.0 est installé
  (celles du Chat et de Cowork au 01-11-2026) ; jamais la nuit : la machine de GitHub a pdftotext 26.01.0 depuis le
  29-10-2026, et cet outil y rendrait 2.
  python3 -I etudes/outils/FIGER_LE_TEXTE_DES_AVIS.py <racine du dépôt>            contrôle seul, n'écrit rien
  python3 -I etudes/outils/FIGER_LE_TEXTE_DES_AVIS.py <racine du dépôt> --ecrire   écrit les textes et le carnet,
                                                                                  puis contrôle
③ ENTRÉE — La racine du dépôt : le référentiel (donnees/REFERENTIEL_VALEURS_*.csv, sa colonne fichiers_cites), les
  avis PDF qu'il cite, le carnet, et programmes/VERIFIER_LES_PREUVES_DU_REFERENTIEL.py ; l'option --ecrire.
④ CONDITIONS D'ENTRÉE — `pdftotext -v` dit « pdftotext version 24.02.0 » ; un seul référentiel ; le vérificateur est
  sous la racine (cet outil lui prend le dossier, la règle de nom, la lecture du carnet et la comparaison
  d'empreinte `inscrite_au_carnet`).
⑤ SORTIE — Le code de sortie : 0 si chaque avis cité a son texte figé, identique octet pour octet à ce que rend
  pdftotext 24.02.0 -layout, et inscrit UNE fois au carnet à son empreinte, produit par cet outil, avec l'avis pour
  fichier lu ; 1 si un avis ne l'a pas ; 2 si le contrôle n'a pas pu tourner (appel mal formé, pdftotext absent, d'une
  autre version ou en échec, référentiel absent ou double, aucun avis cité, erreur imprévue) — un contrôle qui n'a pas
  pu tourner ne rend jamais 0 (R-734). L'écran : une ligne par avis (« IDENTIQUE » ou le défaut), puis « VERDICT … ».
  [rend: 1]
⑥ TRAITEMENT — (1) vérifier la version de pdftotext ; (2) relever les avis cités, un par contenu (`avis_cites`) ;
  (3) avec --ecrire : pour chaque avis, écrire la sortie brute de pdftotext sous le nom que donne le vérificateur (`texte_fige_de`), et
  remplacer au carnet les lignes de ce texte par une seule (`ecrire_au_carnet`) ; (4) dans tous les cas, contrôler
  chaque avis (`ecarts`).
⑦ UNITÉ — —
⑧ POURQUOI — Décisions de Jean-Luc du 01-11-2026 : à 13h41 (« 1 » à « prouver la cause, puis figer au dépôt le texte
  extrait de chaque PDF du référentiel ; le vérificateur compare à ce texte figé ») et à 14h05 (« 1 » à « on vérifie
  une fois, au moment de figer, avec l'ancienne version 24.02 ; ensuite c'est l'empreinte qui protège chaque nuit »).
  Cause prouvée le même jour : pdftotext 26.01.0, installé par GitHub depuis le 29-10-2026, coupe en colonnes le
  tableau de l'avis ERF ; deux citations sur douze ne sont plus des lignes entières, et l'épreuve du vérificateur rendait
  38/42 sur un dépôt inchangé. Les citations ont été écrites le 24-10-2026 contre la sortie de 24.02.0 : c'est elle
  qu'on fige. Ce qui se calcule ne s'écrit pas à la main (R-728) : l'empreinte et la ligne du carnet sont écrites par
  ce programme ; et ce qu'un programme peut faire, un programme le fait (R-754).
⑨ CE QUI CLOCHE — Le contrôle de fidélité exige pdftotext 24.02.0 : il ne tourne pas la nuit (décision de 14h05 :
  « on vérifie une fois, au moment de figer »). · La sortie de pdftotext 24.02.0 dépend du code de poppler, pas de la
  construction : mesuré le 01-11-2026, le paquet Ubuntu 24.04 et une construction depuis l'archive officielle
  (poppler-24.02.0.tar.xz, sha256 19187a3f…) rendent le même texte sur les six avis ; un autre paquet 24.02.0 portant
  un correctif de mise en page ne serait pas reconnu. · Un ancien texte figé que plus aucun avis ne nomme reste au
  dossier : rien ne se supprime sans accord. · Les lignes du carnet d'un ancien texte ne sont pas retirées non plus.
  · La colonne `le` prend la date de Paris du jour où l'outil écrit : relancé avec --ecrire un autre jour sur des
  textes inchangés, il réécrit la ligne avec la nouvelle date.
⑩ EFFET — Lance pdftotext ; avec --ecrire, écrit les textes figés et réécrit le carnet (les autres lignes à l'octet
  près : vérifié le 01-11-2026, la relecture-écriture du carnet par le module csv rend le fichier identique).
⑪ TERMINAISON — Rend la main ; chaque appel à pdftotext est borné à 60 s ; sort par sys.exit.
  [sort: oui]
"""
import csv
import datetime
import glob
import hashlib
import importlib.util
import io
import os
import subprocess
import sys
import zoneinfo

VERSION_EXIGEE = "24.02.0"
OUTIL = "etudes/outils/FIGER_LE_TEXTE_DES_AVIS.py"
VERIF = os.path.join("programmes", "VERIFIER_LES_PREUVES_DU_REFERENTIEL.py")
PREUVE = ("pdftotext 24.02.0 -layout, sortie brute ; décisions de Jean-Luc du 01-11-2026 à 13h41 (« 1 » à « prouver "
          "la cause, puis figer au dépôt le texte extrait de chaque PDF du référentiel ; le vérificateur compare à ce "
          "texte figé ») et à 14h05 (« 1 » à « on vérifie une fois, au moment de figer, avec l'ancienne version 24.02 ; "
          "ensuite c'est l'empreinte qui protège chaque nuit »)")


class Impossible(Exception):
    """Le contrôle ne peut pas tourner (code 2)."""


def charger_le_verificateur(racine):
    """Charge programmes/VERIFIER_LES_PREUVES_DU_REFERENTIEL.py depuis la racine donnée.

    ① RÔLE — Prendre au vérificateur le dossier des textes figés, la règle de nom, la lecture du carnet et la
      comparaison d'empreinte du carnet.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — Le vérificateur est sous la racine.
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — importlib, sans écrire de cache de compilation.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Deux implémentations d'une même chose divergent toujours (R-708) : le nom qu'écrit cet outil est celui
      que lit le vérificateur, parce que c'est la même fonction.
    ⑨ CE QUI CLOCHE — Le module est celui de la racine contrôlée, pas celui du dossier de cet outil : sur un dépôt
      dont le vérificateur a changé de règle, c'est la nouvelle règle qui s'applique, et c'est voulu.
    ⑩ EFFET — Exécute le module (il ne fait que définir des fonctions).
    ⑪ TERMINAISON — Rend la main ou lève Impossible. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    chemin = os.path.join(racine, VERIF)
    if not os.path.isfile(chemin):
        raise Impossible(f"{VERIF} absent de la racine")
    spec = importlib.util.spec_from_file_location("VERIFIER_LES_PREUVES_DU_REFERENTIEL", chemin)
    module = importlib.util.module_from_spec(spec)
    avant = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = avant
    return module


def verifier_la_version():
    """Vérifie que pdftotext est la version 24.02.0.

    ① RÔLE — Refuser de figer ou de contrôler avec une autre version que celle contre laquelle les citations ont été
      écrites.
    ② CONTEXTE D'APPEL — `main`, avant tout.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Aucune valeur.
      [rend: 0]
    ⑥ TRAITEMENT — `pdftotext -v` ; une ligne de sa sortie doit être exactement « pdftotext version 24.02.0 ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — 26.01.0 coupe autrement l'avis ERF (voir le ⑧ du programme).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance pdftotext.
    ⑪ TERMINAISON — Rend la main ou lève Impossible ; borné à 60 s.
      [sort: non]
    """
    try:
        r = subprocess.run(["pdftotext", "-v"], capture_output=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise Impossible(f"pdftotext n'a pas pu être lancé : {e}")
    lignes = (r.stdout + r.stderr).decode("utf-8", "replace").splitlines()
    if f"pdftotext version {VERSION_EXIGEE}" not in [l.strip() for l in lignes]:
        raise Impossible(f"pdftotext n'est pas la version {VERSION_EXIGEE} : « {lignes[0] if lignes else ''} »")


def avis_cites(racine, V):
    """Rend les avis PDF que cite le référentiel des valeurs, un par contenu.

    ① RÔLE — Dire quels textes il faut figer.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `racine` · `V` : le vérificateur chargé (sa règle de nom `texte_fige_de`).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des chemins, depuis la racine, dans l'ordre du référentiel, sans doublon de chemin
      NI de contenu : de deux avis aux octets identiques, seul le premier cité est rendu. Au 01-11-2026 : 6 avis,
      6 contenus distincts.
      [rend: 1]
    ⑥ TRAITEMENT — Chaque morceau de la colonne fichiers_cites (séparateur « ; ») qui finit par .pdf, sans tenir compte
      de la casse (comme le vérificateur) ; un avis dont `V.texte_fige_de` rend un nom déjà rendu (même empreinte
      SHA-256 du PDF) n'est pas ajouté.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une propriété, pas une liste : un avis ajouté au référentiel est figé sans changer ce programme. Un
      texte, une ligne au carnet : relecture neuve du 01-11-2026, M3 (cas F1) — deux avis aux octets identiques, cités
      tous les deux, faisaient écrire deux lignes de carnet pour un même texte, puis l'outil et le vérificateur
      rougissaient (« inscrite 2 fois »). L'empreinte vient de la règle de nom du vérificateur, jamais d'un second calcul
      ici (R-708) : deux avis ont le même texte figé exactement quand ils ont le même nom.
    ⑨ CE QUI CLOCHE — L'avis écarté n'est ni contrôlé par `ecarts`, ni nommé dans la colonne `lu` du carnet : il est
      identique à l'octet à celui qui l'est, et le vérificateur lui trouve le même texte figé par son nom. · Inverser
      l'ordre des citations de deux avis identiques (« COPIE;DSY » au lieu de « DSY;COPIE »), sans changer aucun
      contenu, fait garder l'autre avis : le contrôle de la colonne `lu` (`ecarts`) rougit alors jusqu'au prochain
      --ecrire, qui réécrit `lu` avec l'avis gardé. Faux rouge, jamais faux vert ; sans effet au 01-11-2026 (6 avis,
      6 contenus). Relecture n° 2 du 04-11-2026, m5 ; laissé tel quel sur l'avis du superviseur R-759 du même jour
      (tour 3) : accepter tout avis identique dans `lu` affaiblirait le contrôle.
    ⑩ EFFET — Lit le référentiel et chaque avis cité.
    ⑪ TERMINAISON — Rend la main ou lève Impossible (référentiel absent ou double, aucun avis, avis illisible).
      [sort: non]
    """
    refs = glob.glob(os.path.join(racine, "donnees", "REFERENTIEL_VALEURS_*.csv"))
    if len(refs) != 1:
        raise Impossible(f"{len(refs)} référentiel(s) trouvé(s) au lieu d'un")
    with open(refs[0], encoding="utf-8-sig", newline="") as x:
        lus = list(csv.DictReader(x))
    avis, textes = [], set()
    for r in lus:
        for f in (r.get("fichiers_cites") or "").split(";"):
            if f.lower().endswith(".pdf") and f not in avis:
                try:
                    texte = V.texte_fige_de(racine, f)
                except OSError as e:
                    raise Impossible(f"l'avis {f} est illisible : {e}")
                if texte not in textes:                   # un contenu, un texte, une ligne au carnet (M3)
                    textes.add(texte)
                    avis.append(f)
    if not avis:
        raise Impossible("le référentiel ne cite aucun avis PDF")
    return avis


def extraire(racine, chemin):
    """Rend la sortie brute de pdftotext -layout sur un avis.

    ① RÔLE — Extraire le texte d'un avis, tel qu'il sera figé.
    ② CONTEXTE D'APPEL — `main`, une fois par avis.
    ③ ENTRÉE — `racine` · `chemin` : l'avis, depuis la racine.
    ④ CONDITIONS D'ENTRÉE — La version a été vérifiée (`verifier_la_version`).
    ⑤ SORTIE — UNE valeur : les octets de la sortie.
      [rend: 1]
    ⑥ TRAITEMENT — pdftotext -layout <avis> -, sortie standard capturée, sans aucune retouche.
    ⑦ UNITÉ — Des octets.
    ⑧ POURQUOI — La normalisation des espaces vit dans le vérificateur, à un seul endroit : on fige la sortie brute pour
      qu'une ré-extraction se compare octet pour octet.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance pdftotext.
    ⑪ TERMINAISON — Rend la main ou lève Impossible ; borné à 60 s.
      [sort: non]
    """
    try:
        r = subprocess.run(["pdftotext", "-layout", os.path.join(racine, chemin), "-"], capture_output=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise Impossible(f"pdftotext n'a pas pu lire {chemin} : {e}")
    if r.returncode != 0:
        raise Impossible(f"pdftotext a échoué sur {chemin} (code {r.returncode})")
    return r.stdout


def ecrire_au_carnet(racine, V, lignes_neuves):
    """Remplace au carnet les lignes des textes figés donnés par une ligne chacun.

    ① RÔLE — Inscrire chaque texte figé au carnet de provenance avec son empreinte.
    ② CONTEXTE D'APPEL — `main`, avec --ecrire, une fois.
    ③ ENTRÉE — `racine` · `V` : le vérificateur chargé · `lignes_neuves` : une liste de dictionnaires aux colonnes du
      carnet.
    ④ CONDITIONS D'ENTRÉE — Le carnet existe et a l'en-tête du contrat (CONTRATS_DES_FICHIERS.PROVENANCE_DES_FICHIERS).
    ⑤ SORTIE — Aucune valeur.
      [rend: 0]
    ⑥ TRAITEMENT — Lire le carnet par le vérificateur (`lignes_du_carnet`), retirer les lignes dont le fichier est l'un
      des textes donnés, ajouter les lignes neuves à la fin, réécrire (UTF-8, fins de ligne « \\n », guillemets au
      besoin, comme le fichier existant).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une seule ligne par texte : K23 exige qu'un fichier présent ait exactement une ligne à son empreinte
      actuelle, et le vérificateur aussi.
    ⑨ CE QUI CLOCHE — L'en-tête est lu dans le fichier, pas dans le contrat : un carnet à l'en-tête faux le garde.
      K23 le refuse alors (`maillons_manquants`, ValueError).
    ⑩ EFFET — Réécrit le carnet.
    ⑪ TERMINAISON — Rend la main ou lève.
      [sort: non]
    """
    with open(os.path.join(racine, V.CARNET), encoding="utf-8-sig", newline="") as x:
        colonnes = next(csv.reader(x))
    neufs = {l["fichier"] for l in lignes_neuves}
    garde = [r for r in V.lignes_du_carnet(racine) if r["fichier"] not in neufs]
    t = io.StringIO()
    w = csv.DictWriter(t, fieldnames=colonnes, lineterminator="\n")
    w.writeheader()
    w.writerows(garde + lignes_neuves)
    with open(os.path.join(racine, V.CARNET), "w", encoding="utf-8", newline="") as x:
        x.write(t.getvalue())


def ecarts(racine, V, chemin, extrait):
    """Rend les écarts d'un avis : texte figé absent, différent de l'extraction, ou mal inscrit au carnet.

    ① RÔLE — Le contrôle de fidélité d'un avis.
    ② CONTEXTE D'APPEL — `main`, une fois par avis, après l'écriture s'il y en a une.
    ③ ENTRÉE — `racine` · `V` : le vérificateur chargé · `chemin` : l'avis · `extrait` : la sortie de `extraire`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des écarts, en textes ; vide si l'avis est conforme.
      [rend: 1]
    ⑥ TRAITEMENT — (1) le texte figé nommé par `V.texte_fige_de` existe et est égal, octet pour octet, à `extrait` ;
      (2) le carnet porte exactement une ligne pour ce texte, et cette ligne l'inscrit à son empreinte selon
      `V.inscrite_au_carnet` (la même comparaison que le vérificateur), produite par cet outil, avec l'avis pour seul
      fichier lu.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — (1) est la fidélité décidée à 14h05 ; (2) est ce que le vérificateur exigera chaque nuit, plus ce que
      K23 exigerait s'il atteignait ce texte (un programme du dépôt, au moins un fichier lu). Une seule comparaison
      d'empreinte pour les deux programmes : relecture neuve du 01-11-2026, M2 (R-708).
    ⑨ CE QUI CLOCHE — Exiger UNE ligne pour le texte, quelle que soit son empreinte, est plus que ce qu'exige le
      vérificateur (une ligne à la bonne empreinte) : une vieille ligne restée au carnet est refusée ici, acceptée là.
      C'est voulu : l'outil qui écrit le carnet le veut propre.
    ⑩ EFFET — Lit le texte figé et le carnet.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    texte = V.texte_fige_de(racine, chemin)
    p = os.path.join(racine, texte)
    if not os.path.isfile(p):
        return [f"aucun texte figé ({texte})"]
    octets = open(p, "rb").read()
    if octets != extrait:
        return [f"le texte figé {texte} diffère de pdftotext {VERSION_EXIGEE} ({len(octets)} octets figés, "
                f"{len(extrait)} extraits)"]
    e = hashlib.sha256(octets).hexdigest()
    carnet = V.lignes_du_carnet(racine)
    lignes = [r for r in carnet if r["fichier"] == texte]
    if (len(lignes) != 1 or V.inscrite_au_carnet(carnet, texte, e) != 1 or lignes[0]["produit_par"] != OUTIL
            or lignes[0]["lu"] != chemin):
        return [f"le carnet ne porte pas exactement une ligne pour {texte} à l'empreinte {e[:16]}…, produite "
                f"par {OUTIL}, avec cet avis pour fichier lu ({len(lignes)} ligne(s))"]
    return []


def main(argv):
    """Le point d'entrée.

    ① RÔLE — Lancer le contrôle, et l'écriture si elle est demandée.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — `argv` : le nom du programme, la racine, et --ecrire facultatif.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le code de sortie 0, 1 ou 2 (voir le ⑤ du programme).
      [rend: 1]
    ⑥ TRAITEMENT — Le ⑥ du programme ; une erreur Impossible ou imprévue rend « VERDICT IMPOSSIBLE » et 2.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734 : un contrôle qui n'a pas pu tourner ne rend jamais 0.
    ⑨ CE QUI CLOCHE — Avec --ecrire, une panne au milieu laisse les textes déjà écrits, et le carnet inchangé (il est
      écrit après tous les textes) : relancer suffit.
    ⑩ EFFET — Voir le ⑩ du programme.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    args = [a for a in argv[1:] if a != "--ecrire"]
    ecrire = "--ecrire" in argv[1:]
    if len(args) != 1 or not os.path.isdir(args[0]):
        print(__doc__.split("③")[0])
        print("VERDICT IMPOSSIBLE — appel mal formé")
        return 2
    racine = args[0]
    try:
        V = charger_le_verificateur(racine)
        verifier_la_version()
        avis = avis_cites(racine, V)
        extraits = {a: extraire(racine, a) for a in avis}
        if ecrire:
            le = datetime.datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d")
            neuves = []
            for a in avis:
                texte = V.texte_fige_de(racine, a)
                os.makedirs(os.path.join(racine, V.TEXTES_FIGES), exist_ok=True)
                with open(os.path.join(racine, texte), "wb") as x:
                    x.write(extraits[a])
                neuves.append({"fichier": texte, "sha256": hashlib.sha256(extraits[a]).hexdigest(), "produit_par": OUTIL,
                               "lu": a, "adresse": "", "le": le, "preuve": PREUVE})
            ecrire_au_carnet(racine, V, neuves)
        tous = []
        for a in avis:
            e = ecarts(racine, V, a, extraits[a])
            print(f"{a} : " + ("; ".join(e) if e else f"IDENTIQUE à pdftotext {VERSION_EXIGEE}, inscrit au carnet"))
            tous += e
    except Impossible as e:
        print(f"VERDICT IMPOSSIBLE — {e}")
        return 2
    except Exception as e:                                # dernier filet : une panne n'est pas un verdict
        print(f"VERDICT IMPOSSIBLE — erreur imprévue : {type(e).__name__} : {e}")
        return 2
    print("VERDICT", f"CONFORME — {len(avis)} avis figés et fidèles" if not tous else f"{len(tous)} ÉCART(S)")
    return 0 if not tous else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
