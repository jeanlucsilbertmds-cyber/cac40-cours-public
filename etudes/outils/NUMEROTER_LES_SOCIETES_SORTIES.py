#!/usr/bin/env python3
"""NUMÉROTER LES SOCIÉTÉS SORTIES — Plan V7, mission E2a, tour 3 (jeudi 12-11-2026). SIMULATION UNIQUEMENT.

① RÔLE — Donner un numéro interne (41 et suivants) à chaque société sortie du CAC 40 qui n'en a pas, dans
  donnees/sources_indice/IDENTITES_DES_SOCIETES.csv, puis remplacer, dans les listes annuelles de la taxe
  (donnees/VALEURS_TTF.csv), chaque code ISIN écrit dans la colonne « mnemonique » par le mnémonique de la société.
② CONTEXTE D'APPEL — À la main, par le Chat ou un agent : `python3 -I <ce fichier> <racine>` (essai à blanc, rien
  n'est écrit) puis `... <racine> --ecrire`. Aucun programme du circuit du soir ne l'appelle.
③ ENTRÉE — La racine du dépôt ; l'option « --ecrire ». Fichiers lus : la table des identités, la table des passages
  (PASSAGES_DANS_LE_CAC40.csv), la liste des taxes, et trois tables du dossier etudes/VINGT_ANS_A_PART_Mer_11-11-2026/
  du dépôt qui porte ce programme (DOSSIER_DES_TABLES ; « à côté de ce programme » jusqu'au 15-11-2026) :
  MNEMONIQUES_DES_SOCIETES_SORTIES.csv (le mnémonique de chaque société, avec sa source et la phrase lue) et
  ISIN_D_UNE_MEME_SOCIETE.csv (les codes ISIN successifs d'une même société), NOMS_DES_SOCIETES_SORTIES.csv (le
  nom, avec sa source, quand le libellé bnains est tronqué — tour 4, D2 du relecteur : « Aventis (Ex Rh », « Cr »).
④ CONDITIONS D'ENTRÉE — Les fichiers existent ; l'en-tête des identités est celui du contrat
  (CONTRATS.IDENTITES_DES_SOCIETES). Sinon : ARRET, code 2.
⑤ SORTIE — Le code de sortie : 0 (fait, ou rien à faire), 2 (arrêt, rien n'est écrit). [rend: 1]
⑥ TRAITEMENT — ① lire · ② `plan_des_numeros` : les lignes nouvelles · ③ `ramener_la_taxe` : la liste des taxes
  réécrite · ④ à blanc : afficher ; avec --ecrire : écrire les deux fichiers, puis relire les passages par le lecteur
  unique (LIRE_LES_COURS.lire_les_passages) et exiger le MÊME rendu qu'avant — sinon remettre les deux fichiers
  d'origine et rendre 2.
⑦ UNITÉ — —
⑧ POURQUOI — Décisions de Jean-Luc du 11-11-2026 à 22h26 (« 1 » : les règles I-2 à I-4 du registre s'appliquent
  telles quelles aux sociétés sorties, numéros 41 et suivants, le fichier des 20 ans les désigne par leur mnémonique)
  et rappel du Chat du 12-11-2026 à 09h15 (plan V7, section 7bis) : I-2, chaque identifiant (nom, mnémonique, ISIN)
  est rattaché au numéro AVEC SES DATES ; I-7, une société absorbée GARDE SON NUMÉRO, sa série se clôt (« un titre
  disparaît, un autre naît — clore l'un, ouvrir l'autre — jamais fusionner les séries »). Le juge cherche la taxe
  d'une valeur par son mnémonique (MODULE_POSITIONS, `_taxee`) : une liste écrite en ISIN ne trouvait aucune
  société sortie (point M1 de la note E2a).
⑨ CE QUI CLOCHE — Les dates `debut` et `fin` écrites sont la PREMIÈRE et la DERNIÈRE séance DANS L'INDICE (table des
  passages), pas la validité réelle de l'identifiant : chaque ligne nouvelle est donc « à compléter ». · Un mnémonique
  est une observation datée (la date de sa source) : sa validité sur toute la période n'est pas vérifiée (Teleperformance
  a pu porter un autre code avant 2020). · 21 sociétés n'ont pas de mnémonique sourcé : « non trouvé ». · Toutes les
  lignes nouvelles ont une `fin` : le lecteur unique ne range donc pas encore leurs passages (point M2, au Chat).
⑩ EFFET — Avec --ecrire : réécrit les deux fichiers de données (fins de ligne gardées ligne à ligne).
⑪ TERMINAISON — Rend la main ; aucun de mes appels ne peut ne pas revenir. [sort: oui]
"""
import csv
import io
import os
import re
import sys

# LES TROIS TABLES DE CE PROGRAMME restent dans le dossier daté de la mission (des données, que le circuit garde) ;
# le programme vit dans etudes/outils/ depuis le 15-11-2026 (superviseur R-759 du 15-11-2026, réparation 4 : le pas
# « poser le code public » efface tout .py hors des dossiers gardés, et son épreuve rougissait sur GitHub,
# FileNotFoundError). Le dossier des tables se lit à partir de l'emplacement de ce fichier : <dépôt>/etudes/outils/.
ICI = os.path.dirname(os.path.abspath(__file__))
DOSSIER_DES_TABLES = os.path.join("etudes", "VINGT_ANS_A_PART_Mer_11-11-2026")
TABLES = os.path.join(os.path.dirname(os.path.dirname(ICI)), DOSSIER_DES_TABLES)
MNEMOS = os.path.join(TABLES, "MNEMONIQUES_DES_SOCIETES_SORTIES.csv")
GROUPES = os.path.join(TABLES, "ISIN_D_UNE_MEME_SOCIETE.csv")
NOMS = os.path.join(TABLES, "NOMS_DES_SOCIETES_SORTIES.csv")   # 12-11-2026, tour 4 (D2) : les libellés bnains tronqués
NON_TROUVE = "non trouvé"          # la valeur déjà employée par la table des identités (Thales, Vinci avant 2000)
PREMIER_NUMERO = 41                # décision du 11-11-2026 à 22h26 : « 41 et suivants »


def _lire(chemin):
    """Lit un CSV en liste de dictionnaires, avec son en-tête.

    ① RÔLE — Lecture commune. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `chemin`. ④ CONDITIONS D'ENTRÉE — Le fichier
    existe (OSError sinon, que `main` transforme en ARRET). ⑤ SORTIE — DEUX valeurs : l'en-tête (liste), les lignes.
    [rend: 2] ⑥ TRAITEMENT — csv.DictReader, UTF-8, BOM accepté. ⑦ UNITÉ — — ⑧ POURQUOI — Une seule lecture.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        return list(r.fieldnames or []), list(r)


def plan_des_numeros(identites, passages, mnemos, groupes, est_un_isin, noms=None):
    """Rend les lignes d'identité à ajouter pour les codes ISIN des passages qui n'ont pas de numéro.

    ① RÔLE — Le cœur : qui reçoit quel numéro, avec quel nom, quel mnémonique, quelles dates.
    ② CONTEXTE D'APPEL — `main`, une fois ; l'épreuve, sur des tables d'essai.
    ③ ENTRÉE — `identites` : lignes de la table des identités · `passages` : lignes de la table des passages ·
      `mnemos` : {isin: ligne de MNEMONIQUES_DES_SOCIETES_SORTIES.csv} · `groupes` : {isin: ligne de
      ISIN_D_UNE_MEME_SOCIETE.csv} · `est_un_isin` : la fonction qui dit si un texte est un ISIN valide ·
      `noms` : {isin: ligne de NOMS_DES_SOCIETES_SORTIES.csv}, facultatif (vide : le libellé bnains).
    ④ CONDITIONS D'ENTRÉE — Les numéros existants sont des entiers.
    ⑤ SORTIE — DEUX valeurs : la liste des lignes nouvelles (dictionnaires aux colonnes de la table des identités),
      la liste des refus (textes ; non vide = ne rien écrire). [rend: 2]
    ⑥ TRAITEMENT — ① les codes déjà numérotés · ② les codes des passages sans numéro, rangés par leur première séance
      dans l'indice puis par code (ordre stable) · ③ un code déclaré « même société qu'un autre » (`groupes`) prend le
      numéro de l'autre, qui doit lui aussi être à numéroter ; sinon un numéro neuf, à partir du plus grand + 1 et au
      moins PREMIER_NUMERO · ④ une ligne par code : nom = celui de `noms` s'il y est, sinon le libellé bnains, debut/fin = première et dernière séance dans
      l'indice, mnémonique sourcé ou NON_TROUVE · ⑤ refus : un code mal formé, un passage encore ouvert (une société
      sortie a une dernière séance), un mnémonique sourcé déjà porté par une autre société.
    ⑦ UNITÉ — Des dates AAAA-MM-JJ, recopiées.
    ⑧ POURQUOI — Fiche en tête, ⑧ (I-2, I-7).
    ⑨ CE QUI CLOCHE — Fiche en tête, ⑨.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    refus = []
    noms = noms or {}
    numerotes = {r["isin"] for r in identites if r["isin"]}
    pris = {}
    for r in identites:
        if r["mnemonique"] and r["mnemonique"] != NON_TROUVE:
            pris.setdefault(r["mnemonique"], r["numero"])
    sejours = {}
    libelle = {}
    for p in passages:
        code = p["isin_bnains"]
        if not code or code in numerotes:
            continue
        if not est_un_isin(code):
            refus.append(f"code mal formé dans les passages : {code!r}")
            continue
        if not p["derniere_seance"]:
            refus.append(f"{code} ({p['libelle_bnains']}) est encore dans l'indice : ce n'est pas une société sortie")
        sejours.setdefault(code, []).append((p["premiere_seance"], p["derniere_seance"]))
        libelle.setdefault(code, p["libelle_bnains"])
    ordre = sorted(sejours, key=lambda c: (min(s[0] for s in sejours[c]), c))
    prochain = max([int(r["numero"]) for r in identites] + [PREMIER_NUMERO - 1]) + 1
    numero_de = {}
    for code in ordre:
        autre = groupes.get(code, {}).get("meme_societe_que")
        if autre:
            if autre not in sejours:
                refus.append(f"{code} : « même société que » {autre}, qui n'est pas à numéroter")
                continue
            numero_de.setdefault(autre, None)
    for code in ordre:
        autre = groupes.get(code, {}).get("meme_societe_que")
        cible = autre if autre in sejours else code
        if numero_de.get(cible) is None:
            numero_de[cible] = prochain
            prochain += 1
        numero_de[code] = numero_de[cible]
    lignes = []
    for code in ordre:
        m = mnemos.get(code)
        mnemo = m["mnemonique"] if m else NON_TROUVE
        n = str(numero_de[code])
        if m and pris.setdefault(mnemo, n) != n:
            refus.append(f"mnémonique {mnemo} de {code} déjà porté par la société {pris[mnemo]}")
        g = groupes.get(code)
        nm = noms.get(code)
        preuve = ("numéro attribué le 12-11-2026 (I-2 ; I-7 : une société absorbée garde son numéro) ; ISIN, nom et "
                  "dates : PASSAGES_DANS_LE_CAC40.csv (bnains), debut et fin = première et dernière séance DANS "
                  "L'INDICE, validité réelle de l'identifiant non relevée ; mnémonique : "
                  + (f"{m['source']} « {m['citation']} », lu le {m['lu_le']}, valable à la date de la source"
                     if m else "aucune source trouvée")
                  + (f" ; même société que {g['meme_societe_que']} : {g['raison']}" if g else "")
                  + (f" ; nom : {nm['source']} « {nm['citation']} », lu le {nm['lu_le']} (libellé bnains tronqué : "
                     f"« {libelle[code]} »)" if nm else ""))
        nom = nm["nom"] if nm else libelle[code]
        lignes.append({"numero": n, "societe": nom,
                       "debut": min(s[0] for s in sejours[code]), "fin": max(s[1] for s in sejours[code]),
                       "nom_cote": nom, "mnemonique": mnemo, "isin": code, "preuve": preuve,
                       "etat": g["etat"] if g else "à compléter"})
    return lignes, refus


def ramener_la_taxe(octets, identites, est_un_isin):
    """Remplace, dans la liste des taxes, chaque code ISIN de la colonne « mnemonique » par le mnémonique sourcé.

    ① RÔLE — Point M1 : que le juge trouve la taxe d'une société sortie par son mnémonique.
    ② CONTEXTE D'APPEL — `main`, une fois, avec les identités APRÈS ajout ; l'épreuve.
    ③ ENTRÉE — `octets` : le fichier donnees/VALEURS_TTF.csv tel quel · `identites` : toutes les lignes d'identité ·
      `est_un_isin` : la fonction de forme.
    ④ CONDITIONS D'ENTRÉE — Une ligne de commentaire (« # ») en tête est admise ; la ligne d'en-tête porte
      « mnemonique » en deuxième colonne.
    ⑤ SORTIE — TROIS valeurs : les octets réécrits, le nombre de cases remplacées, la liste des refus. [rend: 3]
    ⑥ TRAITEMENT — Ligne à ligne, fin de ligne gardée : une case « mnemonique » qui a la forme d'un ISIN reçoit le
      mnémonique des lignes d'identité de ce code (hors NON_TROUVE) ; refus si ce n'est pas exactement UN mnémonique,
      ou si le même (année, mnémonique) existe déjà. Les autres octets ne changent pas.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le nom qui désigne une société vit UNE fois, dans la table des identités (deux implémentations d'une
      même chose divergent toujours, R-708) : la liste des taxes le lit, ne le recopie pas d'une autre source.
    ⑨ CE QUI CLOCHE — Le découpage par virgule suppose que la deuxième case n'est jamais entre guillemets (vrai : un
      mnémonique ou un ISIN). Les cases suivantes (nom, source) peuvent en avoir : elles ne sont pas relues.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    refus, n = [], 0
    mnemo_de = {}
    for r in identites:
        if r["isin"] and r["mnemonique"] and r["mnemonique"] != NON_TROUVE:
            mnemo_de.setdefault(r["isin"], set()).add(r["mnemonique"])
    texte = octets.decode("utf-8")
    sortie, vus = [], set()
    for ligne in texte.splitlines(keepends=True):
        corps = ligne.rstrip("\r\n")
        fin = ligne[len(corps):]
        cases = corps.split(",", 2)
        if corps.startswith("#") or len(cases) < 3 or cases[0] == "annee":
            sortie.append(ligne)
            continue
        if est_un_isin(cases[1]):
            m = mnemo_de.get(cases[1], set())
            if len(m) != 1:
                refus.append(f"{cases[0]} {cases[1]} : {len(m)} mnémonique(s) sourcé(s) dans les identités")
            else:
                cases[1] = next(iter(m))
                n += 1
        if (cases[0], cases[1]) in vus:
            refus.append(f"{cases[0]} {cases[1]} : deux lignes après remplacement")
        vus.add((cases[0], cases[1]))
        sortie.append(",".join(cases) + fin)
    return "".join(sortie).encode("utf-8"), n, refus


def _ecrire_les_identites(octets, nouvelles, entete):
    """Ajoute les lignes nouvelles à la table des identités, avec la fin de ligne du fichier.

    ① RÔLE — Écriture. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — les octets du fichier, les lignes, l'en-tête.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : les octets nouveaux. [rend: 1] ⑥ TRAITEMENT — csv.writer,
    fin de ligne de la dernière ligne du fichier (« \\r\\n » ici). ⑦ UNITÉ — — ⑧ POURQUOI — garder la forme du fichier.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — — ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    fin = "\r\n" if octets.endswith(b"\r\n") else "\n"
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator=fin)
    for r in nouvelles:
        w.writerow([r[c] for c in entete])
    base = octets if octets.endswith(b"\n") else octets + fin.encode()
    return base + buf.getvalue().encode("utf-8")


def main(argv):
    """Le programme entier (fiche en tête).

    ① RÔLE — Voir la fiche en tête. ② CONTEXTE D'APPEL — ligne de commande. ③ ENTRÉE — `argv`.
    ④ CONDITIONS D'ENTRÉE — Fiche en tête. ⑤ SORTIE — UNE valeur : le code de sortie (0 ou 2). [rend: 1]
    ⑥ TRAITEMENT — Fiche en tête, ⑥. ⑦ UNITÉ — — ⑧ POURQUOI — Fiche en tête. ⑨ CE QUI CLOCHE — Fiche en tête.
    ⑩ EFFET — Fiche en tête. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    args = [a for a in argv if not a.startswith("--")]
    mauvaises = [a for a in argv if a.startswith("--") and a != "--ecrire"]
    if len(args) != 1 or mauvaises:
        print("ARRET usage : NUMEROTER_LES_SOCIETES_SORTIES.py <racine> [--ecrire]")
        return 2
    racine = os.path.abspath(args[0])
    sys.path.insert(0, os.path.join(racine, "programmes"))
    import CONTRATS_DES_FICHIERS as CONTRATS
    import LIRE_LES_COURS as LECTEUR
    f_id = os.path.join(racine, LECTEUR.IDENTITES)
    f_ttf = os.path.join(racine, "donnees", "VALEURS_TTF.csv")
    try:
        entete, identites = _lire(f_id)
        _, passages = _lire(os.path.join(racine, LECTEUR.PASSAGES))
        mnemos = {r["isin"]: r for r in _lire(MNEMOS)[1]}
        groupes = {r["isin"]: r for r in _lire(GROUPES)[1]}
        noms = {r["isin"]: r for r in _lire(NOMS)[1]}
        o_id, o_ttf = open(f_id, "rb").read(), open(f_ttf, "rb").read()
    except OSError as e:
        print(f"ARRET fichier illisible : {e}")
        return 2
    if entete != CONTRATS.IDENTITES_DES_SOCIETES:
        print(f"ARRET en-tête des identités hors contrat : {entete}")
        return 2
    nouvelles, refus = plan_des_numeros(identites, passages, mnemos, groupes, LECTEUR.isin_valide, noms)
    n_ttf_ttf, n_rempl, refus_t = ramener_la_taxe(o_ttf, identites + nouvelles, LECTEUR.isin_valide)
    refus += refus_t
    sans = sum(1 for r in nouvelles if r["mnemonique"] == NON_TROUVE)
    numeros = sorted({int(r["numero"]) for r in nouvelles})
    print(f"ETAPE {len(nouvelles)} ligne(s) d'identité nouvelles, {len(numeros)} numéro(s)"
          + (f" de {numeros[0]} à {numeros[-1]}" if numeros else "")
          + f" ; mnémonique sourcé : {len(nouvelles) - sans}, « {NON_TROUVE} » : {sans}")
    for r in nouvelles:
        print(f"   {r['numero']:>3} {r['isin']} {r['mnemonique']:<11} {r['debut']} → {r['fin']}  {r['societe']}  [{r['etat']}]")
    print(f"ETAPE liste des taxes : {n_rempl} case(s) ISIN remplacée(s) par le mnémonique")
    if refus:
        for r in refus[:10]:
            print("REFUS " + r)
        if len(refus) > 10:
            print(f"REFUS ... et {len(refus) - 10} autre(s)")
        print("ARRET rien n'est écrit")
        return 2
    if not nouvelles and not n_rempl:
        print("FINI rien à faire : tout est déjà numéroté et la liste des taxes ne porte aucun ISIN")
        return 0
    if "--ecrire" not in argv:
        print("FINI essai à blanc : rien n'est écrit (ajouter --ecrire)")
        return 0
    avant = LECTEUR.lire_les_passages(racine)
    open(f_id, "wb").write(_ecrire_les_identites(o_id, nouvelles, entete))
    open(f_ttf, "wb").write(n_ttf_ttf)
    try:
        apres = LECTEUR.lire_les_passages(racine)
        if apres != avant:
            raise ValueError("le rendu du lecteur unique a changé")
    except ValueError as e:
        open(f_id, "wb").write(o_id)
        open(f_ttf, "wb").write(o_ttf)
        print(f"ARRET après écriture, {e} : les deux fichiers sont remis à l'identique")
        return 2
    print("FINI écrit : table des identités et liste des taxes ; rendu du lecteur unique des passages inchangé")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
