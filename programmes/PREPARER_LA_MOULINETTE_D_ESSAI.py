#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PREPARER_LA_MOULINETTE_D_ESSAI — Lun 16-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Décision de Jean-Luc A-853 (16-11-2026 à 15h18, réponse « 1 ») : la moulinette des 20 ans
(programmes/JOUER_LES_VERSIONS.py avec --cours=) s'éprouve sur une FICHE D'ESSAI C5 couvrant 2000-2026, qui n'entre
dans aucun compte d'essais ni dans aucune sélection ; IND-001-RETEST garde son regard. Décision de Jean-Luc A-861
(16-11-2026 à 20h05, réponse « 1 ») : cette fiche vit dans une COPIE JETABLE du registre, que seule la moulinette d'essai
utilise ; elle n'entre jamais dans le vrai registre. Ce programme fabrique cette copie, dans une copie de travail du
dépôt, et peut ensuite y lancer la moulinette.

① RÔLE — Dans une copie de travail du dépôt (jamais le dépôt) : remplacer donnees/cac40_strategies.csv, SOUS LE MÊME NOM,
  par le registre augmenté d'UNE ligne, la fiche d'essai ESSAI-C5-2000-2026, recopiée à l'identique de la première fiche
  C5 présente parmi SOURCES ; seuls changent l'identifiant, la période (premier jour de cours de l'an 2000 → dernière
  séance avant BORNE_DE_FIN_EXCLUE, calculées sur le fichier des 20 ans) et le statut. Écrire à côté une combinatoire
  d'une seule version, la fiche elle-même. Avec « --jouer » : lancer ensuite la moulinette sur cette version avec
  --cours= le fichier des 20 ans, et recopier ses résultats sur la sortie standard.
② CONTEXTE D'APPEL — L'épreuve longue « MoulinetteEssai » de tests/LANCEMENT_DES_EPREUVES.json, lancée sur GitHub par
  tests/outils/jouer_une_epreuve_longue.py dans la copie du circuit (sans .git) ; à la main, sur une copie faite par
  « git archive » ; l'épreuve tests/EPREUVES_DE_LA_MOULINETTE_D_ESSAI_Lun_16-11-2026.py.
③ ENTRÉE — La ligne de commande : la racine de la copie de travail, puis, facultative, l'option « --jouer ».
④ CONDITIONS D'ENTRÉE — La racine n'a PAS de .git (sinon refus : c'est le vrai dépôt, ou un clone) ; elle porte
  donnees/cac40_strategies.csv (terminé par une fin de ligne, sans ligne ESSAI-C5-2000-2026), COURS_DES_VINGT_ANS et
  programmes/JUGE_DES_STRATEGIES.py ; une fiche de SOURCES y figure.
⑤ SORTIE — Le code de sortie : 0 si la copie est préparée (et, avec --jouer, si la moulinette rend 0) ; le code de la
  moulinette avec --jouer ; 2 si rien n'a pu être préparé (lieu refusé, fichier absent, fiche introuvable) : un
  contrôle qui n'a pas pu tourner rend un code non nul (R-734).
  [rend: 1]
⑥ TRAITEMENT — `refus_du_lieu` · `seances_du_fichier` puis `periode_d_essai` · `ligne_source` · `ligne_d_essai` ·
  écriture du registre (octets d'origine + une ligne) et de la combinatoire (`preparer`) · avec --jouer, `jouer`.
⑦ UNITÉ — Dates AAAA-MM-JJ ; seuils de la combinatoire en FRACTIONS (lus par `pourcent` du juge) ; horizon en séances.
⑧ POURQUOI — A-861 : la fiche ne compte jamais PAR CONSTRUCTION, parce que k (le compte des versions, A-777) se lit sur
  origin/main par git (`k_a_la_date` du juge) et que la ligne n'existe que dans une copie sans .git. La période se
  CALCULE sur les cours (R-728 : ce qui se calcule ne s'écrit jamais à la main). La fin tombe avant le 2026-10-30
  parce que la moulinette exige, après la fin, l'horizon le plus long plus la séance d'achat, et refuse un recul de
  plus de 26 séances (JOUER_LES_VERSIONS.py, `fin_utilisable` et RECUL_MAXIMUM_DE_LA_FIN.csv).
⑨ CE QUI CLOCHE — ① MESURÉ le 16-11-2026 : le juge REFUSE cette fiche sur 2000-2023, par deux verrous du regard unique
  (fenêtre 2000-01-01..2023-12-31 de CONTRATS_DES_FICHIERS) : la garde M (univers borné, sans décision écrite dans
  UNIVERS_BORNES_ACCEPTES_SUR_LE_REGARD_UNIQUE), puis RegardNonInscrit (aucun reçu au registre des essais). Ce
  programme ne lève aucun de ces verrous lui-même : depuis A-863 (Jean-Luc, 16-11-2026 à 20h46, « 1 »), il passe à la
  moulinette l'option déclarée « --essai-sans-regard », que le juge n'accepte que pour une fiche identique à
  C5E10-QA-V1, une version, hors d'un dépôt. Aucun troisième verrou (frais, TTF) mesuré le 16-11-2026. ② Seul <racine>/.git est cherché : une
  copie posée DANS un dépôt (un sous-dossier d'un clone) n'est pas refusée. ③ SOURCES est une liste écrite : une
  fiche C5 renommée n'y serait plus trouvée (refus, code 2, jamais une autre fiche en silence).
⑩ EFFET — Remplace donnees/cac40_strategies.csv de la copie ; y crée la combinatoire d'essai ; avec --jouer, lance la
  moulinette (qui lance le juge), écrit ses résultats dans un dossier temporaire hors de la copie, puis l'efface.
⑪ TERMINAISON — Sort par sys.exit. Un de mes appels peut-il ne pas revenir ? Avec --jouer, la moulinette, lancée sans
  délai propre : sur GitHub, le joueur des épreuves longues la coupe.
  [sort: oui]
"""
import csv
import io
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

REGISTRE = os.path.join("donnees", "cac40_strategies.csv")
COURS_DES_VINGT_ANS = "temoins/TEMOIN_VINGT_ANS_2000_2026_COUPURE_2026-11-11_FIGE_Ven_13-11-2026_10h59.csv"
IDENTIFIANT = "ESSAI-C5-2000-2026"
ESSAI = "E01"
COMBINATOIRE = os.path.join("donnees", "combinatoires", "COMBINATOIRE_%s_%s.csv" % (IDENTIFIANT, ESSAI))
# LA FICHE RECOPIÉE : la première présente, dans cet ordre. « C5-ETENDU-10 » est la stratégie de production (R-201) ;
# absente du registre comme identifiant au 16-11-2026, sa ligne de vie de production est C5E10-QA-V1 (« C5-ETENDU-10
# production 6 valeurs ») ; puis la fiche d'observation C5E10-OBS-V1 (10 valeurs).
SOURCES = ("C5-ETENDU-10", "C5E10-QA-V1", "C5E10-OBS-V1")
ANNEE_DE_DEBUT = "2000"
BORNE_DE_FIN_EXCLUE = "2026-10-30"   # A-861 : « fin de période avant le 2026-10-30 (horizon) »
STATUT_D_ESSAI = "ESSAI (A-853, A-861) : copie jetable, hors de tout compte et de toute sélection"
MOULINETTE = os.path.join("programmes", "JOUER_LES_VERSIONS.py")


def refus_du_lieu(copie):
    """Rend la raison de ne pas préparer cette racine, ou "" si elle convient.

    ① RÔLE — Garder le vrai registre : ce programme ne travaille jamais dans un dépôt git.
    ② CONTEXTE D'APPEL — `main`, avant toute lecture ; l'épreuve (cas du refus et son sabotage).
    ③ ENTRÉE — `copie` : le chemin de la racine reçue.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte de la raison, vide si la racine convient.
      [rend: 1]
    ⑥ TRAITEMENT — pas un dossier → raison ; <copie>/.git existe (dossier, fichier ou lien) → raison ; registre ou
      fichier des 20 ans absent → raison.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Consigne du 16-11-2026 : « le programme refuse, avec un code de sortie non nul, s'il est lancé sur le
      vrai dépôt (racine contenant .git) ». Un clone porte .git ; la copie du circuit (git archive) n'en porte pas.
    ⑨ CE QUI CLOCHE — Fiche en tête, ⑨ ②.
    ⑩ EFFET — Lit l'existence de trois chemins.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if not os.path.isdir(copie):
        return "%s n'est pas un dossier" % copie
    if os.path.lexists(os.path.join(copie, ".git")):
        return "%s porte .git : c'est un dépôt, pas une copie jetable ; le vrai registre n'est jamais touché" % copie
    for rel in (REGISTRE, COURS_DES_VINGT_ANS):
        if not os.path.isfile(os.path.join(copie, rel)):
            return "%s absent de la copie" % rel
    return ""


def seances_du_fichier(chemin):
    """Rend les séances d'un fichier de cours : l'ensemble des dates de sa colonne « date ».

    ① RÔLE — Donner à `periode_d_essai` le calendrier réel des cours, jamais une date tapée.
    ② CONTEXTE D'APPEL — `preparer`, une fois.
    ③ ENTRÉE — `chemin` : un fichier CSV de cours (colonnes valeur, date, open, …).
    ④ CONDITIONS D'ENTRÉE — Le fichier se lit en UTF-8 et porte une colonne « date ».
    ⑤ SORTIE — UNE valeur : l'ensemble des dates (textes AAAA-MM-JJ).
      [rend: 1]
    ⑥ TRAITEMENT — csv.DictReader, colonne « date », lignes vides ignorées.
    ⑦ UNITÉ — Des dates.
    ⑧ POURQUOI — R-728.
    ⑨ CE QUI CLOCHE — Une date mal écrite entre telle quelle dans l'ensemble ; la moulinette relit les cours par le
      lecteur unique du juge, qui la refuserait.
    ⑩ EFFET — Lit le fichier (23 Mo pour les 20 ans).
    ⑪ TERMINAISON — Rend la main ; lève KeyError sans colonne « date ».
      [sort: non]
    """
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        return {r["date"] for r in csv.DictReader(f) if r.get("date")}


def periode_d_essai(dates):
    """Rend la période de la fiche d'essai : la première séance de l'an 2000, la dernière avant la borne exclue.

    ① RÔLE — Calculer la période à écrire dans la fiche d'essai.
    ② CONTEXTE D'APPEL — `preparer` ; l'épreuve (cas tiré des vraies dates).
    ③ ENTRÉE — `dates` : un ensemble de textes AAAA-MM-JJ.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le début, la fin (textes AAAA-MM-JJ).
      [rend: 2]
    ⑥ TRAITEMENT — début = la plus petite date qui commence par ANNEE_DE_DEBUT ; fin = la plus grande date strictement
      inférieure à BORNE_DE_FIN_EXCLUE ; l'une ou l'autre introuvable, ou fin avant début → ValueError.
    ⑦ UNITÉ — Des dates, comparées en texte (le format AAAA-MM-JJ s'ordonne comme le temps).
    ⑧ POURQUOI — Fiche en tête, ⑧ (R-728 ; borne A-861).
    ⑨ CE QUI CLOCHE — La fin est la dernière séance du FICHIER, toutes valeurs confondues ; la moulinette recalcule
      ensuite une fin utilisable valeur par valeur (`fin_utilisable`), et le dit.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError.
      [sort: non]
    """
    debuts = [d for d in dates if d.startswith(ANNEE_DE_DEBUT)]
    fins = [d for d in dates if d < BORNE_DE_FIN_EXCLUE]
    if not debuts or not fins:
        raise ValueError("aucune séance en %s, ou aucune avant le %s" % (ANNEE_DE_DEBUT, BORNE_DE_FIN_EXCLUE))
    debut, fin = min(debuts), max(fins)
    if fin < debut:
        raise ValueError("fin %s avant le début %s" % (fin, debut))
    return debut, fin


def ligne_source(lignes):
    """Rend l'identifiant et la ligne de la fiche recopiée : la première de SOURCES présente, sa DERNIÈRE ligne.

    ① RÔLE — Choisir la fiche C5 que la fiche d'essai recopie.
    ② CONTEXTE D'APPEL — `preparer` ; l'épreuve (cas tiré de la vraie ligne C5).
    ③ ENTRÉE — `lignes` : les lignes du registre lues par csv.reader, en-tête comprise.
    ④ CONDITIONS D'ENTRÉE — La première ligne est l'en-tête et porte « id ».
    ⑤ SORTIE — DEUX valeurs : l'identifiant choisi ; sa ligne (liste de textes, telle que lue).
      [rend: 2]
    ⑥ TRAITEMENT — pour chaque identifiant de SOURCES, dans l'ordre : ses lignes au registre ; s'il en a, rendre la
      dernière. Aucune → ValueError.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — « La dernière ligne ajoutée fait foi » (décision de Jean-Luc n°83 du 01-11-2026, lue ainsi par
      `fiches_du_registre` du contrat) ; ordre de SOURCES : consigne du 16-11-2026, « en commençant par la fiche de
      production C5-ETENDU-10 si elle existe ».
    ⑨ CE QUI CLOCHE — Fiche en tête, ⑨ ③.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError.
      [sort: non]
    """
    i_id = lignes[0].index("id")
    for ident in SOURCES:
        trouvees = [r for r in lignes[1:] if len(r) > i_id and r[i_id] == ident]
        if trouvees:
            return ident, trouvees[-1]
    raise ValueError("aucune fiche de %s au registre" % (SOURCES,))


def ligne_d_essai(entete, source, debut, fin):
    """Rend la ligne de la fiche d'essai : la ligne source, où seuls changent l'identifiant, la période et le statut.

    ① RÔLE — Fabriquer la fiche d'essai.
    ② CONTEXTE D'APPEL — `preparer` ; l'épreuve.
    ③ ENTRÉE — `entete` : la ligne d'en-tête ; `source` : la ligne recopiée ; `debut`, `fin` : la période.
    ④ CONDITIONS D'ENTRÉE — L'en-tête porte « id », « periode » et « statut ».
    ⑤ SORTIE — UNE valeur : une nouvelle liste de textes, de la longueur de `source`.
      [rend: 1]
    ⑥ TRAITEMENT — copier ; id ← IDENTIFIANT ; periode ← « début -> fin » (la forme des fiches, ex. C5E10-OBS-V1
      « 2024-01-02 -> 2026-07-10 ») ; statut ← STATUT_D_ESSAI.
    ⑦ UNITÉ — Des dates.
    ⑧ POURQUOI — Consigne du 16-11-2026 : « seuls changent l'identifiant, la période et un statut ou une mention
      d'essai ». Le statut ne contient pas « VIVANTE » : le soir ne la lirait pas, si elle sortait par erreur de la copie.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun : `source` n'est pas modifiée.
    ⑪ TERMINAISON — Rend la main ; lève ValueError si une colonne manque.
      [sort: non]
    """
    nouvelle = list(source)
    for colonne, valeur in (("id", IDENTIFIANT), ("periode", "%s -> %s" % (debut, fin)), ("statut", STATUT_D_ESSAI)):
        nouvelle[entete.index(colonne)] = valeur
    return nouvelle


def preparer(copie):
    """Prépare la copie : registre augmenté d'une ligne, combinatoire d'une version ; rend ce qui a été fait.

    ① RÔLE — Le geste entier de la préparation (fiche en tête, ①, sans --jouer).
    ② CONTEXTE D'APPEL — `main` ; l'épreuve.
    ③ ENTRÉE — `copie` : la racine, déjà acceptée par `refus_du_lieu`.
    ④ CONDITIONS D'ENTRÉE — Fiche en tête, ④.
    ⑤ SORTIE — UNE valeur : un dictionnaire {source, debut, fin, combinatoire, version}.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire les OCTETS du registre ; refuser s'il ne finit pas par une fin de ligne ou s'il porte déjà
      IDENTIFIANT ; ② la période sur COURS_DES_VINGT_ANS ; ③ la fiche source et la ligne d'essai ; ④ la ligne écrite par
      csv.writer avec la fin de ligne du fichier (« \\r\\n » si le fichier en porte) ; ⑤ registre = octets d'origine +
      cette ligne, écrit dans un fichier voisin puis renommé ; ⑥ la combinatoire : une version, tp et sl en fractions
      par `pourcent` du juge, horizon par `lire_horizon` du juge, l'univers tel qu'écrit, marquée « OUI » identique à
      la fiche ; refus si elle existe déjà.
    ⑦ UNITÉ — Fiche en tête, ⑦.
    ⑧ POURQUOI — Octets d'origine gardés : toutes les autres lignes restent identiques à l'octet (consigne). Les seuils
      se lisent par le juge, la seule lecture (R-708), parce que la moulinette les compare par lui (`controler_fusion`).
    ⑨ CE QUI CLOCHE — Le juge est importé depuis la copie (ses modules entrent dans sys.modules de ce processus).
    ⑩ EFFET — Remplace le registre de la copie ; crée la combinatoire.
    ⑪ TERMINAISON — Rend la main, ou lève ValueError, OSError.
      [sort: non]
    """
    chemin = os.path.join(copie, REGISTRE)
    with open(chemin, "rb") as f:
        octets = f.read()
    if not octets.endswith(b"\n"):
        raise ValueError("%s ne finit pas par une fin de ligne : la dernière ligne changerait" % REGISTRE)
    lignes = list(csv.reader(io.StringIO(octets.decode("utf-8-sig"), newline="")))
    i_id = lignes[0].index("id")
    if any(len(r) > i_id and r[i_id] == IDENTIFIANT for r in lignes[1:]):
        raise ValueError("%s est déjà au registre de la copie : rien n'est ajouté une seconde fois" % IDENTIFIANT)
    debut, fin = periode_d_essai(seances_du_fichier(os.path.join(copie, COURS_DES_VINGT_ANS)))
    ident, source = ligne_source(lignes)
    essai = ligne_d_essai(lignes[0], source, debut, fin)
    texte = io.StringIO()
    csv.writer(texte, lineterminator="\r\n" if octets.endswith(b"\r\n") else "\n").writerow(essai)
    provisoire = chemin + ".en_cours"
    with open(provisoire, "wb") as f:
        f.write(octets + texte.getvalue().encode("utf-8"))
    os.replace(provisoire, chemin)

    sys.path.insert(0, os.path.join(copie, "programmes"))
    import JUGE_DES_STRATEGIES as J
    fiche = dict(zip(lignes[0], essai))
    version = {"id_version": "%s-%s-0001" % (IDENTIFIANT, ESSAI), "strategie": IDENTIFIANT, "essai": ESSAI,
               "tp": repr(J.pourcent(fiche["tp"])), "sl": repr(J.pourcent(fiche["sl"])),
               "horizon": str(J.lire_horizon(fiche["horizon"])), "univers": fiche["univers"],
               "versions_dans_l_essai": "1", "version_de_la_fiche": "OUI"}
    f_comb = os.path.join(copie, COMBINATOIRE)
    with open(f_comb, "x", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(version), lineterminator="\n")
        w.writeheader()
        w.writerow(version)
    return {"source": ident, "debut": debut, "fin": fin, "combinatoire": COMBINATOIRE, "version": version}


def jouer(copie):
    """Lance la moulinette sur la combinatoire d'essai, avec --cours= les 20 ans ; recopie ses résultats ; rend son code.

    ① RÔLE — La seconde moitié de l'épreuve longue « MoulinetteEssai ».
    ② CONTEXTE D'APPEL — `main`, avec --jouer, après `preparer`.
    ③ ENTRÉE — `copie` : la racine préparée.
    ④ CONDITIONS D'ENTRÉE — `preparer` a réussi sur cette copie.
    ⑤ SORTIE — UNE valeur : le code de sortie de la moulinette.
      [rend: 1]
    ⑥ TRAITEMENT — dossier temporaire hors de la copie ; `python3 -B JOUER_LES_VERSIONS.py <copie> <combinatoire>
      <dossier>/RESULTATS.csv --cours=<20 ans> --essai-sans-regard` (l'essai déclaré d'A-863), sortie laissée sur la sortie standard ; le fichier de résultats, s'il
      existe, recopié sur la sortie standard ; le dossier effacé.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les résultats reviennent au PRIVÉ par SORTIE.txt du joueur des épreuves longues, comme pour les autres
      épreuves (A-835 : rien de privé au public) ; ils ne sont rangés dans aucun dossier qu'un tri lit.
    ⑨ CE QUI CLOCHE — Sans l'option d'essai, sur 2000-2023, la moulinette s'arrêtait au calibrage par le juge (code 1,
      garde M puis RegardNonInscrit, mesuré le 16-11-2026) ; l'option la fait passer, et seulement elle (A-863).
    ⑩ EFFET — Lance un processus ; crée puis efface un dossier temporaire.
    ⑪ TERMINAISON — Rend la main quand la moulinette rend la sienne (aucun délai ici).
      [sort: non]
    """
    # L'OPTION DE L'ESSAI DÉCLARÉ (A-863) se lit au contrat de ce dossier, écrite une fois (R-708)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import CONTRATS_DES_FICHIERS as _CE
    dossier = tempfile.mkdtemp(prefix="moulinette_essai_")
    try:
        resultats = os.path.join(dossier, "RESULTATS.csv")
        code = subprocess.call([sys.executable, "-B", os.path.join(copie, MOULINETTE), copie,
                                os.path.join(copie, COMBINATOIRE), resultats, "--cours=" + COURS_DES_VINGT_ANS,
                                _CE.OPTION_D_ESSAI_SANS_REGARD],
                               cwd=copie)
        if os.path.isfile(resultats):
            print("RÉSULTATS DE LA MOULINETTE D'ESSAI :")
            with open(resultats, encoding="utf-8") as f:
                sys.stdout.write(f.read())
        print("CODE DE LA MOULINETTE : %d" % code, flush=True)
        return code
    finally:
        shutil.rmtree(dossier, ignore_errors=True)


def main(arguments):
    """Lit la ligne de commande, refuse ou prépare, puis joue si demandé ; rend le code de sortie.

    ① RÔLE — Point d'entrée.
    ② CONTEXTE D'APPEL — `__main__`.
    ③ ENTRÉE — `arguments` : sys.argv[1:].
    ④ CONDITIONS D'ENTRÉE — Fiche en tête, ③ et ④.
    ⑤ SORTIE — UNE valeur : 0, 2, ou le code de la moulinette (fiche en tête, ⑤).
      [rend: 1]
    ⑥ TRAITEMENT — arguments lus (une racine, « --jouer » facultatif, rien d'autre) ; `refus_du_lieu` ; `preparer`,
      ses refus rendus en code 2 ; compte rendu ; `jouer` si demandé.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734 : un refus n'est jamais un vert.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Ceux de `preparer` et `jouer`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    options = [a for a in arguments if a.startswith("--")]
    positions = [a for a in arguments if not a.startswith("--")]
    if len(positions) != 1 or set(options) - {"--jouer"}:
        print("ARRET usage : PREPARER_LA_MOULINETTE_D_ESSAI.py <copie_sans_git> [--jouer]", file=sys.stderr)
        return 2
    copie = os.path.abspath(positions[0])
    refus = refus_du_lieu(copie)
    if refus:
        print("ARRET %s" % refus, file=sys.stderr)
        return 2
    try:
        fait = preparer(copie)
    except (OSError, ValueError, KeyError) as e:
        print("ARRET %s : %s" % (type(e).__name__, e), file=sys.stderr)
        return 2
    v = fait["version"]
    print("FICHE D'ESSAI %s : recopie de %s · période %s -> %s · %s" % (
        IDENTIFIANT, fait["source"], fait["debut"], fait["fin"], STATUT_D_ESSAI))
    print("COMBINATOIRE %s : 1 version, tp %s · sl %s · horizon %s · univers %s" % (
        fait["combinatoire"], v["tp"], v["sl"], v["horizon"], v["univers"]), flush=True)
    if "--jouer" in options:
        return jouer(copie)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
