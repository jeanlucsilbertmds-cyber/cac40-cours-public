#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPREUVES_DE_LA_MOULINETTE_Mar_20-10-2026.py — Mar 20-10-2026 (Paris)
DÉCIDÉ · outil · Rôle : éprouver les refus des quatre programmes de la moulinette (A-541) et son rejeu complet.
Quand l'appeler : à la main avant toute modification de la moulinette ; et chaque nuit par le certificateur.

USAGE
    python3 tests/EPREUVES_DE_LA_MOULINETTE_Mar_20-10-2026.py <racine_du_depot>
    exemple : python3 tests/EPREUVES_DE_LA_MOULINETTE_Mar_20-10-2026.py .
    Rien n'est écrit dans le dépôt : chaque cas travaille dans un dossier temporaire, effacé à la fin.

① RÔLE — Provoquer, un par un, les refus de PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES,
  DECLINER_LES_STRATEGIES, JOUER_LES_VERSIONS et EPREUVES_DE_LA_DECLINAISON (tous dans `programmes/`), et
  exiger de chacun le code de sortie et la partie FIXE du message que son code annonce ; puis rejouer une
  fois les 2 695 versions de l'essai E01 de C5E10-OBS-V1 contre le témoin de résultats du 08-10-2026.
  Trois familles de cas :
  · EN SOUS-PROCESSUS, avec de vraies données (lignes réelles du registre, de la combinatoire et du témoin,
    R-732) : les refus atteignables de l'extérieur, et deux rejeux réduits à trois versions — l'un sans
    témoin, l'autre avec un témoin abîmé d'un euro, qui doit arrêter le programme sans rien écrire (cassure
    K1 de la relecture de Cowork du 20-10-2026, `80b04a2`) ;
  · PAR IMPORT, avec un FAUX JUGE qui fabrique chaque situation : les refus de JOUER_LES_VERSIONS que de
    vraies données ne peuvent pas atteindre (juge importé d'ailleurs, fiche en double, porte 0 qui refuse,
    valeurs absentes des cours, fiche sans opération, juge et programme en désaccord, période différente,
    écart d'horizon ou d'univers dans `controler_fusion`) ; et les deux fonctions de DECLINER qui rendent
    « rien » sur un paramètre inconnu ;
  · le REJEU COMPLET, une seule fois.
② CONTEXTE D'APPEL — À la main ; et par `programmes/CERTIFIER_LA_VERSION.py`, qui lance chaque épreuve de
  `tests/` depuis la racine d'une copie, avec la racine en argument, sous la mesure de ce qui est exécuté.
③ ENTRÉE — Un argument : la racine du dépôt.
④ CONDITIONS D'ENTRÉE — Sous la racine : les quatre programmes, `programmes/JUGE_DES_STRATEGIES.py`,
  `donnees/cac40_strategies.csv` et son référentiel des valeurs, et les fichiers de `donnees/combinatoires/`.
⑤ SORTIE — Un code de sortie : 0 si tous les cas passent · 1 si un cas échoue · 2 sans argument ou si un
  fichier attendu manque (R-734 : un contrôle qui n'a pas pu tourner ne rend jamais 0). Une ligne par cas.
⑥ TRAITEMENT — ① vérifier les fichiers · ② cas de PREPARER · ③ cas de DECLINER · ④ cas
  d'EPREUVES_DE_LA_DECLINAISON · ⑤ cas de JOUER_LES_VERSIONS en sous-processus · ⑥ cas de
  JOUER_LES_VERSIONS par import, avec le faux juge · ⑦ rejeu complet · ⑧ bilan.
⑦ UNITÉ — Des codes de sortie ; des euros dans le témoin abîmé ; des secondes pour les délais.
⑧ POURQUOI — Le certificateur de nuit refuse un programme nouveau tant qu'une de ses instructions n'est
  exécutée par aucune épreuve ; mesuré le 20-10-2026 par Cowork puis par le Chat avec les fonctions du
  certificateur : 70 instructions, dont les 20 refus de JOUER_LES_VERSIONS. Jean-Luc a choisi le 20-10-2026
  à 17h51 de les éprouver plutôt que de les accepter à la référence (« 1 », voie A). Une épreuve qui
  n'exige que le code laisserait passer un refus pour une autre raison : chaque cas exige aussi la partie
  fixe de son message (avis du superviseur du 20-10-2026).
⑨ CE QUI CLOCHE — ① Les cas par import éprouvent la LOGIQUE de JOUER_LES_VERSIONS avec un faux juge : ils ne
  prouvent pas que le vrai juge produit ces situations. ② Un changement de libellé d'un refus fait tomber
  le cas : c'est voulu, le changement devient visible. ③ Le rejeu complet prend environ deux minutes, cinq
  sous la mesure. ④ Le témoin ne vaut que tant que les cours de la période jouée (02-01-2024 → 10-07-2026)
  ne sont pas corrigés.
⑩ EFFET — Lance des programmes ; écrit seulement dans des dossiers temporaires, effacés ; n'écrit aucun fichier compilé
  (`sys.dont_write_bytecode`, et `-B` pour chaque sous-processus).
⑪ TERMINAISON — Sort lui-même. Chaque sous-processus a un délai ; un délai dépassé compte comme un échec.
  Un de ses appels peut-il ne pas revenir ? Non : délai sur chaque sous-processus.
"""
import contextlib
import csv
import importlib.util
import io
import os
import shutil
import subprocess
import sys
import tempfile
import types

sys.dont_write_bytecode = True   # l'épreuve importe des programmes de la racine : rien ne doit s'écrire dans le dépôt

DELAI_SECONDES = 1500
SID, ESSAI = "C5E10-OBS-V1", "E01"
P_PREP = "programmes/PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES.py"
P_DECL = "programmes/DECLINER_LES_STRATEGIES.py"
P_JOUER = "programmes/JOUER_LES_VERSIONS.py"
P_EPDE = "programmes/EPREUVES_DE_LA_DECLINAISON.py"
REGISTRE = "donnees/cac40_strategies.csv"
VARIABLES = "donnees/combinatoires/VARIABLES_DE_DECLINAISON_%s_%s.csv" % (SID, ESSAI)
VOISINAGE = "donnees/combinatoires/VOISINAGE.csv"
COMBINATOIRE = "donnees/combinatoires/COMBINATOIRE_%s_%s.csv" % (SID, ESSAI)
TEMOIN = "donnees/combinatoires/TEMOIN_RESULTATS_%s_%s.csv" % (SID, ESSAI)
ATTENDUS = (P_PREP, P_DECL, P_JOUER, P_EPDE, "programmes/JUGE_DES_STRATEGIES.py", REGISTRE, VARIABLES,
            VOISINAGE, COMBINATOIRE, TEMOIN)
# Trois versions réelles de la combinatoire : celle qui est identique à la fiche, et deux autres.
TROIS = ("%s-%s-0914" % (SID, ESSAI), "%s-%s-0001" % (SID, ESSAI), "%s-%s-0500" % (SID, ESSAI))

RESULTATS = []
DOSSIERS = []


def noter(nom, ok, detail=""):
    """Retient le verdict d'un cas et l'affiche.

    ① RÔLE — Garder une trace de chaque cas.
    ② CONTEXTE D'APPEL — Chaque cas, une fois.
    ③ ENTRÉE — `nom` : le cas · `ok` : vrai s'il passe · `detail` : ce qui a été vu.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Aucune valeur.
      [rend: 0]
    ⑥ TRAITEMENT — Ajouter à RESULTATS et afficher une ligne.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un bilan qui ne nomme pas le cas tombé ne se relit pas.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche ; remplit RESULTATS.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    RESULTATS.append((nom, bool(ok)))
    print(("  OK     " if ok else "  ÉCHEC  ") + nom + (("  — " + detail) if (detail and not ok) else ""))


def dossier():
    """Crée un dossier temporaire, effacé à la fin.

    ① RÔLE — Donner à chaque cas un endroit à lui.
    ② CONTEXTE D'APPEL — Les cas qui fabriquent des fichiers.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin du dossier.
      [rend: 1]
    ⑥ TRAITEMENT — Créer, retenir pour l'effacement final.
    ⑦ UNITÉ — Un chemin.
    ⑧ POURQUOI — Ne rien écrire dans le dépôt.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Crée un dossier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    d = tempfile.mkdtemp(prefix="epreuve_moulinette_")
    DOSSIERS.append(d)
    return d


def lancer(racine, *arguments):
    """Lance un programme de la racine en sous-processus et rend son code et sa sortie.

    ① RÔLE — Exécuter un programme comme le ferait quelqu'un en ligne de commande.
    ② CONTEXTE D'APPEL — Les cas en sous-processus.
    ③ ENTRÉE — `racine` : la racine du dépôt · `arguments` : le chemin relatif du programme, puis ses arguments.
    ④ CONDITIONS D'ENTRÉE — Le programme existe sous la racine.
    ⑤ SORTIE — DEUX valeurs : le code de sortie (124 si le délai est dépassé) et la sortie entière (texte).
      [rend: 2]
    ⑥ TRAITEMENT — Lancer avec l'interpréteur courant et l'environnement courant, depuis la racine.
    ⑦ UNITÉ — Un code ; un texte.
    ⑧ POURQUOI — `sys.executable` et `os.environ` : le certificateur suit la mesure dans les sous-processus
      par son interpréteur et une variable d'environnement ; un autre interpréteur ou un environnement vidé
      la perdrait sans rien dire (avis du superviseur du 20-10-2026).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance un programme.
    ⑪ TERMINAISON — Rend la main ; le délai empêche un appel de ne jamais revenir.
      [sort: non]
    """
    try:
        r = subprocess.run([sys.executable, "-B"] + list(arguments), cwd=racine, capture_output=True,
                           text=True, timeout=DELAI_SECONDES, env=dict(os.environ))
    except subprocess.TimeoutExpired:
        return 124, "délai dépassé"
    return r.returncode, r.stdout + "\n" + r.stderr


def attendre(nom, code, sortie, code_attendu, fragment):
    """Note un cas en exigeant un code ET un fragment fixe du message.

    ① RÔLE — Juger un cas lancé en sous-processus.
    ② CONTEXTE D'APPEL — Les cas en sous-processus.
    ③ ENTRÉE — `nom` · `code`, `sortie` : ce qu'a rendu `lancer` · `code_attendu` · `fragment` : texte qui
      doit figurer dans la sortie, ou tuple de textes qui doivent TOUS y figurer.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Aucune valeur.
      [rend: 0]
    ⑥ TRAITEMENT — Comparer le code, chercher le fragment, noter.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un code seul laisserait passer un refus venu d'ailleurs.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Note.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    fragments = fragment if isinstance(fragment, tuple) else (fragment,)
    vus = all(f in sortie for f in fragments)
    ok = code == code_attendu and vus
    noter(nom, ok, "code %s (attendu %s), fragment %s" % (code, code_attendu, "vu" if vus else "ABSENT")
          + " · fin : " + " | ".join(l for l in sortie.strip().splitlines()[-3:]))


def lire(chemin):
    """Lit un CSV en liste de dictionnaires, avec ses colonnes.

    ① RÔLE — Prendre de vraies lignes des fichiers du dépôt.
    ② CONTEXTE D'APPEL — Les cas qui fabriquent une combinatoire, un témoin ou un tableau réduits.
    ③ ENTRÉE — `chemin` : un fichier CSV.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe et se lit en UTF-8 (une marque d'ordre en tête est retirée).
    ⑤ SORTIE — DEUX valeurs : les colonnes (liste) et les lignes (liste de dictionnaires).
      [rend: 2]
    ⑥ TRAITEMENT — Lire.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-732 : au moins un cas vient d'une vraie ligne du fichier.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        return list(r.fieldnames), list(r)


def ecrire(chemin, colonnes, lignes):
    """Écrit un CSV.

    ① RÔLE — Fabriquer une entrée de cas.
    ② CONTEXTE D'APPEL — Les cas qui fabriquent des fichiers.
    ③ ENTRÉE — `chemin` · `colonnes` · `lignes` : liste de dictionnaires.
    ④ CONDITIONS D'ENTRÉE — Le dossier existe.
    ⑤ SORTIE — UNE valeur : le chemin écrit.
      [rend: 1]
    ⑥ TRAITEMENT — Écrire l'en-tête et les lignes.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit un fichier temporaire.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=colonnes)
        w.writeheader()
        w.writerows(lignes)
    return chemin


def importer(racine, rel, nom):
    """Importe un programme de la racine comme module.

    ① RÔLE — Appeler une fonction d'un programme sans passer par la ligne de commande.
    ② CONTEXTE D'APPEL — Les cas par import.
    ③ ENTRÉE — `racine` · `rel` : chemin relatif du programme · `nom` : nom du module.
    ④ CONDITIONS D'ENTRÉE — Le programme existe.
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — Charger depuis le fichier de la racine.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La mesure crédite le fichier exécuté ; il doit donc être celui de la racine.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Exécute le haut du programme (pas son bloc principal).
    ⑪ TERMINAISON — Rend la main ; l'import peut lever.
      [sort: non]
    """
    sys.path.insert(0, os.path.join(racine, "programmes"))
    spec = importlib.util.spec_from_file_location(nom, os.path.join(racine, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def cas_preparer(racine):
    """Provoque les refus de PREPARER.

    ① RÔLE — Éprouver les refus de PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES en ligne de commande.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — Le registre, son référentiel et le voisinage existent.
    ⑤ SORTIE — Aucune valeur.
      [rend: 0]
    ⑥ TRAITEMENT — Sans argument (code 2) · registre absent à côté d'un référentiel (lecture ratée) ·
      voisinage illisible (pas « abc ») · voisinage invalide (pas négatif) · pas d'horizon non numérique.
      Exemple réel de départ : le voisinage du 08-10-2026, ligne `sl,0.5,4,1.5,4.5,…`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Instructions mesurées non exécutées le 20-10-2026 : 159, 220-224, 299-300, 429-430,
      447-449, 457-459, 489.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance le programme ; écrit dans des dossiers temporaires.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    c, s = lancer(racine, P_PREP)
    attendre("PREPARER sans argument : son mode d'emploi, code 2", c, s, 2, "USAGE")
    d = dossier()
    refs = [f for f in os.listdir(os.path.join(racine, "donnees")) if f.startswith("REFERENTIEL_VALEURS") and f.endswith(".csv")]
    shutil.copy(os.path.join(racine, "donnees", refs[0]), d)
    c, s = lancer(racine, P_PREP, os.path.join(d, "registre_absent.csv"), SID, os.path.join(racine, VOISINAGE), "E99", d)
    attendre("PREPARER, registre absent : lecture ratée, code 1", c, s, 1, "REFUS : lecture ratée de")
    col, vois = lire(os.path.join(racine, VOISINAGE))
    for nom, champ, valeur, fragment in (
            ("pas illisible", "pas", "abc", "règle de voisinage illisible"),
            ("pas négatif", "pas", "-1", "règle de voisinage invalide")):
        lignes = [dict(l, **({champ: valeur} if l["parametre"] == "sl" else {})) for l in vois]
        f = ecrire(os.path.join(dossier(), "VOISINAGE.csv"), col, lignes)
        c, s = lancer(racine, P_PREP, os.path.join(racine, REGISTRE), SID, f, "E99", dossier())
        attendre("PREPARER, voisinage du stop au %s : code 1" % nom, c, s, 1, "REFUS : " + fragment)
    lignes = [dict(l, **({"pas": "cinq"} if l["parametre"] == "horizon" else {})) for l in vois]
    f = ecrire(os.path.join(dossier(), "VOISINAGE.csv"), col, lignes)
    c, s = lancer(racine, P_PREP, os.path.join(racine, REGISTRE), SID, f, "E99", dossier())
    attendre("PREPARER, pas d'horizon « cinq » : code 1", c, s, 1, "le pas de voisinage de l'horizon doit être un nombre entier")


def cas_decliner(racine):
    """Provoque les refus de DECLINER.

    ① RÔLE — Éprouver les refus de DECLINER_LES_STRATEGIES, en ligne de commande et par import.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — Le registre et le tableau des variables de l'essai E01 existent.
    ⑤ SORTIE — Aucune valeur.
      [rend: 0]
    ⑥ TRAITEMENT — Sans argument · registre seul, sans référentiel · tableau absent · tableau vide · ligne du
      stop sans valeur (tableau réel du 08-10-2026, ligne `sl` vidée) · par import, `normaliser` et
      `valeur_au_registre` sur un paramètre inconnu.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Instructions mesurées non exécutées le 20-10-2026 : 187, 212, 261, 343, 413-414, 418-419,
      425-427, 459.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance le programme ; écrit dans des dossiers temporaires.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    c, s = lancer(racine, P_DECL)
    attendre("DECLINER sans argument : son mode d'emploi, code 2", c, s, 2, "USAGE")
    d = dossier()
    shutil.copy(os.path.join(racine, REGISTRE), d)
    c, s = lancer(racine, P_DECL, os.path.join(d, os.path.basename(REGISTRE)), os.path.join(racine, VARIABLES), dossier())
    attendre("DECLINER, registre sans référentiel à côté : code 1", c, s, 1, "il faut exactement un référentiel")
    c, s = lancer(racine, P_DECL, os.path.join(racine, REGISTRE), os.path.join(dossier(), "absent.csv"), dossier())
    attendre("DECLINER, tableau absent : lecture ratée, code 1", c, s, 1, "REFUS : lecture ratée de")
    col, var = lire(os.path.join(racine, VARIABLES))
    f = ecrire(os.path.join(dossier(), "vide.csv"), col, [])
    c, s = lancer(racine, P_DECL, os.path.join(racine, REGISTRE), f, dossier())
    attendre("DECLINER, tableau vide : code 1", c, s, 1, "le tableau est vide")
    lignes = [dict(l, **({"valeurs_a_essayer": ""} if l["parametre"] == "sl" else {})) for l in var]
    f = ecrire(os.path.join(dossier(), "sans_valeur.csv"), col, lignes)
    c, s = lancer(racine, P_DECL, os.path.join(racine, REGISTRE), f, dossier())
    attendre("DECLINER, ligne du stop sans valeur : code 1", c, s, 1, "ligne « sl » sans valeur à essayer")
    decl = importer(racine, P_DECL, "decliner_epreuve")
    noter("DECLINER.normaliser sur un paramètre inconnu : rien", decl.normaliser("inconnu", "4") is None)
    noter("DECLINER.valeur_au_registre sur un paramètre inconnu : rien", decl.valeur_au_registre("inconnu", {"inconnu": "4"}) is None)


def cas_epreuves_de_la_declinaison(racine):
    """Provoque les refus d'EPREUVES_DE_LA_DECLINAISON.

    ① RÔLE — Éprouver l'épreuve de la déclinaison elle-même : sans argument, et devant un sabotage
      inapplicable (texte absent du programme), qui doit la faire conclure en DÉFAUT.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — Le registre existe.
    ⑤ SORTIE — Aucune valeur.
      [rend: 0]
    ⑥ TRAITEMENT — Sous-processus sans argument (code 2) ; par import, la liste des sabotages remplacée par un
      seul sabotage dont le texte n'existe pas : code 1 et « INAPPLICABLE ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Instructions mesurées non exécutées le 20-10-2026 : 509-510, 523-525. Un sabotage dont le
      texte a disparu du programme ne prouve plus rien : l'épreuve doit le dire, pas le compter vert.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance l'épreuve ; joue ses épreuves une fois de plus par import (quelques secondes).
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    c, s = lancer(racine, P_EPDE)
    attendre("EPREUVES_DE_LA_DECLINAISON sans argument : code 2", c, s, 2, "USAGE")
    ep = importer(racine, P_EPDE, "epreuves_declinaison_epreuve")
    ep.SABOTAGES = [(ep.P_PREP, "texte introuvable", "CE TEXTE N'EXISTE DANS AUCUN PROGRAMME", "x")]
    tampon = io.StringIO()
    with contextlib.redirect_stdout(tampon):
        code = ep.main([os.path.join(racine, REGISTRE)])
    s = tampon.getvalue()
    attendre("EPREUVES_DE_LA_DECLINAISON, sabotage inapplicable : DÉFAUT, code 1", code, s, 1, "INAPPLICABLE  sabotage « texte introuvable »")


def combinatoire_reduite(racine, d, changer=None, fiche="%s-%s-0914" % (SID, ESSAI)):
    """Fabrique une combinatoire de trois versions réelles.

    ① RÔLE — Donner à JOUER_LES_VERSIONS une entrée courte, faite de vraies lignes.
    ② CONTEXTE D'APPEL — Les cas de JOUER en sous-processus.
    ③ ENTRÉE — `racine` · `d` : le dossier · `changer` : fonction qui modifie la liste des lignes, ou rien ·
      `fiche` : l'identifiant marqué identique à la fiche.
    ④ CONDITIONS D'ENTRÉE — Les trois versions de TROIS existent dans la combinatoire du dépôt.
    ⑤ SORTIE — UNE valeur : le chemin de la combinatoire écrite.
      [rend: 1]
    ⑥ TRAITEMENT — Garder les trois lignes, annoncer 3 versions, marquer `fiche`, appliquer `changer`, écrire.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un rejeu de trois versions dure quelques secondes ; le rejeu complet n'est joué qu'une fois.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit un fichier temporaire.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    col, toutes = lire(os.path.join(racine, COMBINATOIRE))
    lignes = [dict(l) for l in toutes if l["id_version"] in TROIS]
    for l in lignes:
        l["versions_dans_l_essai"] = str(len(lignes))
        l["version_de_la_fiche"] = "OUI" if l["id_version"] == fiche else ""
    if changer:
        lignes = changer(lignes)
    return ecrire(os.path.join(d, "COMBINATOIRE_%s_%s.csv" % (SID, ESSAI)), col, lignes)


def cas_jouer_dehors(racine):
    """Provoque, en ligne de commande, les refus de JOUER_LES_VERSIONS atteignables avec de vraies données.

    ① RÔLE — Éprouver les contrôles d'entrée, le calibrage, la marge de cours, la fusion, et les deux issues
      de la comparaison au témoin sur une combinatoire réduite.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — La combinatoire et le témoin de l'essai E01 existent.
    ⑤ SORTIE — Aucune valeur.
      [rend: 0]
    ⑥ TRAITEMENT — Un cas par refus ; puis le rejeu réduit sans témoin (code 0, « AUCUN TÉMOIN ») et avec un
      témoin réel abîmé d'un euro sur la version 0500 (code 1, « rien n'est écrit », aucun fichier écrit).
    ⑦ UNITÉ — Des euros pour le témoin abîmé.
    ⑧ POURQUOI — Les 20 refus de JOUER_LES_VERSIONS n'étaient exécutés par aucune épreuve (mesure du
      20-10-2026) ; et l'ancienne épreuve restait verte quand on retirait la comparaison au témoin (K1).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance le programme ; écrit dans des dossiers temporaires.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    c, s = lancer(racine, P_JOUER)
    attendre("JOUER sans argument : son mode d'emploi, code 1", c, s, 1, "USAGE")

    def un_cas(nom, changer, fragment, code_attendu=1, fiche="%s-%s-0914" % (SID, ESSAI), sortie_existante=False,
               temoin=None):
        """Lance JOUER_LES_VERSIONS sur une combinatoire réduite et juge le cas.

        ① RÔLE — Jouer un refus de JOUER_LES_VERSIONS en ligne de commande, sur trois versions réelles.
        ② CONTEXTE D'APPEL — `cas_jouer_dehors`, une fois par cas.
        ③ ENTRÉE — `nom` · `changer` : fonction qui modifie les lignes, ou rien · `fragment` : texte fixe exigé ·
          `code_attendu` · `fiche` : la version marquée identique à la fiche · `sortie_existante` : vrai pour créer
          d'avance le fichier de résultats · `temoin` : fonction qui écrit un témoin dans le dossier, ou rien.
        ④ CONDITIONS D'ENTRÉE — Les trois versions de TROIS existent dans la combinatoire du dépôt.
        ⑤ SORTIE — TROIS valeurs : le dossier du cas, le chemin du fichier de résultats, le code de sortie.
          [rend: 3]
        ⑥ TRAITEMENT — ① fabriquer la combinatoire · ② écrire le témoin s'il y a lieu · ③ créer le fichier de
          résultats s'il y a lieu · ④ lancer · ⑤ juger par `attendre`.
        ⑦ UNITÉ — Un code de sortie.
        ⑧ POURQUOI — Un dossier par cas : un cas ne voit jamais les fichiers d'un autre.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit dans un dossier temporaire ; lance un programme ; note.
        ⑪ TERMINAISON — Rend la main ; `lancer` borne la durée.
          [sort: non]
        """
        d = dossier()
        f = combinatoire_reduite(racine, d, changer, fiche)
        if temoin is not None:
            temoin(d)
        f_out = os.path.join(d, "RESULTATS.csv")
        if sortie_existante:
            open(f_out, "w").close()
        c, s = lancer(racine, P_JOUER, ".", f, f_out)
        attendre(nom, c, s, code_attendu, fragment)
        return d, f_out, c

    def sur_0500(**changements):
        """Rend une fonction qui modifie la version 0500 de la combinatoire réduite.

        ① RÔLE — Viser une version qui n'est pas celle de la fiche.
        ② CONTEXTE D'APPEL — `cas_jouer_dehors`, pour les cas qui doivent passer le contrôle de la version identique.
        ③ ENTRÉE — `changements` : les colonnes à remplacer et leurs nouvelles valeurs.
        ④ CONDITIONS D'ENTRÉE — La version 0500 fait partie de TROIS.
        ⑤ SORTIE — UNE valeur : la fonction, qui prend la liste des lignes et rend la liste modifiée.
          [rend: 1]
        ⑥ TRAITEMENT — Remplacer les colonnes de la seule ligne dont l'identifiant finit par « -0500 ».
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Le 20-10-2026, la première écriture modifiait la dernière ligne, qui est la version 0914 de la
          fiche : le programme s'arrêtait plus tôt, pour une autre raison.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        # La version 0500 n'est pas celle de la fiche : la modifier n'arrête pas le programme au contrôle de
        # la version identique (le 20-10-2026, la première écriture modifiait la dernière ligne, qui est 0914).
        return lambda L: [dict(l, **changements) if l["id_version"].endswith("-0500") else l for l in L]

    def sur_0914(**changements):
        """Rend une fonction qui modifie la version 0914, celle de la fiche.

        ① RÔLE — Viser la version identique à la fiche, jouée avant le contrôle de la marge de cours.
        ② CONTEXTE D'APPEL — `cas_jouer_dehors`, pour les refus que seule cette version atteint (porte 0, valeurs absentes).
        ③ ENTRÉE — `changements` : les colonnes à remplacer et leurs nouvelles valeurs.
        ④ CONDITIONS D'ENTRÉE — La version 0914 fait partie de TROIS.
        ⑤ SORTIE — UNE valeur : la fonction, qui prend la liste des lignes et rend la liste modifiée.
          [rend: 1]
        ⑥ TRAITEMENT — Remplacer les colonnes de la seule ligne dont l'identifiant finit par « -0914 ».
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Lu dans JOUER_LES_VERSIONS : la version identique est jouée avant la marge ; un défaut posé
          sur une autre version est arrêté d'abord par la marge.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        return lambda L: [dict(l, **changements) if l["id_version"].endswith("-0914") else l for l in L]

    un_cas("JOUER, fichier de résultats déjà présent", None, "le fichier de résultats existe déjà", sortie_existante=True)
    un_cas("JOUER, combinatoire vide", lambda L: [], "la combinatoire est vide")
    un_cas("JOUER, deux stratégies", lambda L: L[:-1] + [dict(L[-1], strategie="AUTRE")], "plusieurs stratégies ou essais")
    un_cas("JOUER, identifiant en double", lambda L: L[:-1] + [dict(L[-1], id_version=L[0]["id_version"])], "identifiants de version en double")
    un_cas("JOUER, nombre annoncé faux", lambda L: [dict(l, versions_dans_l_essai="4") for l in L], "la combinatoire annonce")
    un_cas("JOUER, univers vide", lambda L: L[:-1] + [dict(L[-1], univers="")], "univers vide pour")
    un_cas("JOUER, valeur écrite deux fois", lambda L: L[:-1] + [dict(L[-1], univers="TTE,TTE")], "valeur écrite deux fois dans l'univers")
    un_cas("JOUER, aucune version identique à la fiche", None, "0 versions marquées identiques à la fiche", fiche="aucune")
    un_cas("JOUER, stratégie inconnue : le juge ne se calibre pas",
           lambda L: [dict(l, strategie="STRATEGIE-INCONNUE", id_version="STRATEGIE-INCONNUE-" + l["id_version"]) for l in L],
           "le juge des stratégies ne se calibre pas")
    un_cas("JOUER, version marquée identique qui ne l'est pas", None, "identique à la fiche, ne retrouve pas la fiche",
           fiche="%s-%s-0001" % (SID, ESSAI))
    un_cas("JOUER, horizon de 500 séances : marge de cours insuffisante", sur_0500(horizon="500"),
           "pas assez de cours après la période")
    d, f_out, _ = un_cas("JOUER, objectif écrit 1.5 au lieu d'une fraction : fusion fausse",
                         sur_0500(tp="1.5"),
                         ("fusion fausse pour %s-%s-0500" % (SID, ESSAI), "tp lu '1.5', version '1.5'"))
    noter("JOUER, fusion fausse : le fichier provisoire est effacé", not os.path.exists(f_out + ".en_cours") and not os.path.exists(f_out))
    un_cas("JOUER, horizon 0 sur une version : la lecture du juge le refuse, fusion fausse", sur_0500(horizon="0"),
           "horizon lu '0'")
    # La version identique à la fiche est jouée AVANT le contrôle de la marge de cours : un code inconnu y donne
    # « valeurs absentes » ; sur une autre version, la marge l'arrête d'abord (lu dans le code, vu le 20-10-2026).
    un_cas("JOUER, un code inconnu des cours dans la version identique à la fiche : valeurs absentes",
           sur_0914(univers="ZZZ"), "valeurs absentes des cours")
    un_cas("JOUER, un code inconnu des cours dans une autre version : marge insuffisante", sur_0500(univers="ZZZ"),
           "pas assez de cours après la période pour ZZZ")
    un_cas("JOUER, horizon 0 sur la version identique à la fiche : la porte 0 refuse", sur_0914(horizon="0"),
           "la porte 0 refuse")
    d, f_out, c = un_cas("JOUER, combinatoire réduite sans témoin : écrit, code 0", None, "AUCUN TÉMOIN DE RÉSULTATS", code_attendu=0)
    noter("JOUER, sans témoin : le fichier de résultats est écrit", c == 0 and os.path.exists(f_out))

    def temoin_abime(d):
        """Écrit dans un dossier un témoin réel réduit, abîmé d'un euro.

        ① RÔLE — Fabriquer le témoin qui doit faire arrêter JOUER_LES_VERSIONS (cassure K1).
        ② CONTEXTE D'APPEL — `cas_jouer_dehors`, par `un_cas`, après la combinatoire.
        ③ ENTRÉE — `d` : le dossier du cas.
        ④ CONDITIONS D'ENTRÉE — Le témoin du dépôt porte les trois versions de TROIS.
        ⑤ SORTIE — Aucune valeur.
          [rend: 0]
        ⑥ TRAITEMENT — Garder les trois lignes réelles du témoin, ajouter 1 euro au gain net de la version 0500,
          écrire sous le nom que JOUER cherche à côté de la combinatoire.
        ⑦ UNITÉ — Des euros.
        ⑧ POURQUOI — Un témoin bâti de vraies lignes ne peut échouer que par l'euro ajouté (R-732).
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit un fichier temporaire.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        col, tem = lire(os.path.join(racine, TEMOIN))
        garde = [dict(l) for l in tem if l["id_version"] in TROIS]
        for l in garde:
            if l["id_version"].endswith("-0500"):
                l["gain_net_euros"] = "%.2f" % (float(l["gain_net_euros"]) + 1)
        ecrire(os.path.join(d, os.path.basename(TEMOIN)), col, garde)

    # Le détail de l'écart est exigé aussi (cassure M2 de Cowork, 9702048) ; le montant est relu dans le témoin,
    # jamais recopié (R-708 : un chiffre qui existe ailleurs ne se recopie pas).
    vrai = [l for l in lire(os.path.join(racine, TEMOIN))[1] if l["id_version"].endswith("-0500")][0]
    detail = "%s gain_net_euros : %s au lieu de %.2f" % (vrai["id_version"], vrai["gain_net_euros"], float(vrai["gain_net_euros"]) + 1)
    d, f_out, _ = un_cas("JOUER, témoin réel abîmé d'un euro : arrêt",
                         None, ("les résultats ne retrouvent pas le témoin : rien n'est écrit", detail), temoin=temoin_abime)
    noter("JOUER, témoin abîmé : aucun fichier de résultats", not os.path.exists(f_out) and not os.path.exists(f_out + ".en_cours"))

    # LE TÉMOIN SE COMPARE SOUS SON BARÈME (A-550, superviseur R-759, C15, 29-10-2026). Deux témoins FAUX, faits des trois
    # vraies lignes : ① sans étiquette de barème -> arrêt ; ② étiqueté d'un autre barème (le forfait de 300 €) -> l'écart
    # entre les deux barèmes n'est plus la taxe -> arrêt. Le témoin intact, lui, passe : le cas « témoin abîmé d'un euro »
    # ne rougit que sur l'euro ajouté (son détail est exigé).
    def temoin_etiquete(etiquette):
        def ecrire_le(d):
            col, tem = lire(os.path.join(racine, TEMOIN))
            garde = [dict(l) for l in tem if l["id_version"] in TROIS]
            if etiquette is None:
                col = [c for c in col if c != "bareme"]
                for l in garde:
                    l.pop("bareme", None)
            else:
                for l in garde:
                    l["bareme"] = etiquette
            ecrire(os.path.join(d, os.path.basename(TEMOIN)), col, garde)
        return ecrire_le

    d, f_out, _ = un_cas("JOUER, témoin sans barème : arrêt", None,
                         "ne dit pas sous quel barème des frais il a été fait", temoin=temoin_etiquete(None))
    d, f_out, _ = un_cas("JOUER, témoin étiqueté d'un autre barème : l'écart n'est pas la taxe, arrêt", None,
                         "l'écart au témoin n'est pas expliqué par la taxe : rien n'est écrit",
                         temoin=temoin_etiquete("HIST_FORFAIT_300"))
    noter("JOUER, témoin d'un autre barème : aucun fichier de résultats",
          not os.path.exists(f_out) and not os.path.exists(f_out + ".en_cours"))


def faux_juge(base, **reglages):
    """Fabrique un faux juge des stratégies, pour atteindre les refus internes de JOUER_LES_VERSIONS.

    ① RÔLE — Remplacer le module `JUGE_DES_STRATEGIES` par un objet qui rend des situations choisies.
    ② CONTEXTE D'APPEL — `cas_jouer_dedans`.
    ③ ENTRÉE — `base` : la racine que JOUER croira être le dépôt · `reglages` : `ailleurs` (vrai : le faux juge
      dit venir d'un autre dossier), `porte` (ok, manques, bornes) ou une fonction de la fiche, `inconnus`,
      `n` (nombre d'opérations), `registre` (chemin du registre à lire), `refus_lecture` (vrai : le lecteur
      refuse la lecture, comme le vrai juge quand des lignes sont mises à part, 27-10-2026).
      Les situations que de vraies données atteignent (porte 0, valeurs absentes) sont AUSSI jouées en
      sous-processus par `cas_jouer_dehors` ; elles restent ici pour éprouver la logique seule.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le module fabriqué.
      [rend: 1]
    ⑥ TRAITEMENT — Créer un module, poser chaque fonction que JOUER appelle.
    ⑦ UNITÉ — Les opérations, la réussite en pourcents, le gain en euros, comme le vrai juge.
    ⑧ POURQUOI — Ces refus protègent contre un juge ou des données incohérents ; de vraies données
      cohérentes ne peuvent pas les produire. On éprouve donc la logique de JOUER, pas le juge.
    ⑨ CE QUI CLOCHE — Le faux juge ne prouve pas que le vrai produit ces situations.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    J = types.ModuleType("JUGE_DES_STRATEGIES")
    dossier_j = os.path.join(dossier(), "programmes") if reglages.get("ailleurs") else os.path.join(base, "programmes")
    J.__file__ = os.path.join(dossier_j, "JUGE_DES_STRATEGIES.py")
    bornes = ("2024-01-02", "2026-07-10")
    J.fichiers_de_cours = lambda b: ["cours"]
    J.charger_cours = lambda f: {"TTE": [{"date": "2026-08-%02d" % k} for k in range(1, 31)]}
    # JOUER_LES_VERSIONS lit les cours par le lecteur unique, comme le juge, depuis le 27-10-2026 (A-577, étape 1) :
    # le faux juge rend les mêmes séances et une lecture neutre — aucun passage, aucun trou, aucun défaut.
    def lire_par_le_lecteur(b, f, m, jusqu_au=None):
        if reglages.get("refus_lecture"):
            raise ValueError("le lecteur unique a mis 1 ligne(s) de cours à part dans %s : rien n'est jugé" % f)
        return J.charger_cours(f), {"passages": {}, "trous": {}, "composition": False}
    J.lire_par_le_lecteur = lire_par_le_lecteur
    J.table_mnemoniques = lambda f: {"TTE": "TTE"}
    J.cle_valeur = lambda m: m
    J.charger_module = lambda f, nom: None
    # le barème des verdicts (A-550, 29-10-2026) : le faux juge n'a pas de module des positions, il en donne le nom
    J.bareme_des_verdicts = lambda bareme, mod: bareme or "HIST_COURTAGE_SANS_TTF"
    J.trouver = lambda b, motif: reglages.get("registre") if motif == "cac40_strategies.csv" else "fichier"
    porte = reglages.get("porte", (True, [], bornes))
    J.porte_0 = porte if callable(porte) else (lambda f: porte)
    def jouer(f, cours, mnemo, sig, pos, periode=None, lecture=None):
        # JOUER doit jouer comme `main` du juge, avec la lecture (superviseur du 27-10-2026 : un `lecture=` oublié ne
        # se voyait qu'au calibrage sur le maître, jamais ici).
        if lecture is None:
            raise RuntimeError("faux juge : jouer appelé sans la lecture")
        return ["op"], reglages.get("inconnus", [])
    J.jouer = jouer
    n = reglages.get("n", 1)
    J.resumer = lambda ops: {"n": n, "wr": 100.0, "net": 10.0, "wr_exact": 100.0}
    J.pourcent = lambda t: float(t)
    J.lire_horizon = lambda t: int(t)
    return J


def cas_jouer_dedans(racine):
    """Provoque, par import et avec un faux juge, les refus internes de JOUER_LES_VERSIONS.

    ① RÔLE — Éprouver les refus que de vraies données ne peuvent pas atteindre.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Aucune valeur.
      [rend: 0]
    ⑥ TRAITEMENT — Pour chaque cas : une combinatoire de deux versions, un registre d'une ou deux fiches, un
      faux juge, puis `main` de JOUER appelé dans ce processus ; on exige le code 1 et le message, ou
      l'erreur levée et son message, et qu'aucun fichier ne reste. Enfin `controler_fusion` appelé seul.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Instructions mesurées non exécutées le 20-10-2026 : 194, 196, 352, 360, 389, 393, 398, 402, 442.
    ⑨ CE QUI CLOCHE — Voir `faux_juge`, ⑨.
    ⑩ EFFET — Écrit dans des dossiers temporaires ; modifie `sys.modules` et `sys.argv` le temps d'un cas.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    jouer = importer(racine, P_JOUER, "jouer_les_versions_epreuve")
    colonnes = ["id_version", "strategie", "essai", "tp", "sl", "horizon", "univers", "versions_dans_l_essai", "version_de_la_fiche"]
    deux = [{"id_version": "F-E01-1", "strategie": "F", "essai": "E01", "tp": "0.04", "sl": "0.025", "horizon": "20",
             "univers": "TTE", "versions_dans_l_essai": "2", "version_de_la_fiche": "OUI"},
            {"id_version": "F-E01-2", "strategie": "F", "essai": "E01", "tp": "0.05", "sl": "0.025", "horizon": "20",
             "univers": "TTE", "versions_dans_l_essai": "2", "version_de_la_fiche": ""}]
    fiche = {"id": "F", "tp": "0.04", "sl": "0.025", "horizon": "20", "univers": "TTE"}

    def un_cas(nom, fragment, nb_fiches=1, ligne_juge="1 operations . 100.0 % de reussite . +10.00 EUR", leve=False, **reglages):
        """Appelle `main` de JOUER_LES_VERSIONS dans ce processus, avec un faux juge, et juge le cas.

        ① RÔLE — Jouer un refus interne de JOUER_LES_VERSIONS.
        ② CONTEXTE D'APPEL — `cas_jouer_dedans`, une fois par cas.
        ③ ENTRÉE — `nom` · `fragment` : texte fixe exigé · `nb_fiches` : nombre de fois où la fiche figure au registre ·
          `ligne_juge` : ce que le calibrage du juge est censé avoir affiché · `leve` : vrai si le refus est une
          erreur levée et non un code · `reglages` : passés à `faux_juge`.
        ④ CONDITIONS D'ENTRÉE — `jouer` est le module importé de la racine.
        ⑤ SORTIE — Aucune valeur.
          [rend: 0]
        ⑥ TRAITEMENT — ① fabriquer un dépôt factice, un registre, une combinatoire de deux versions · ② poser le
          faux juge dans `sys.modules`, les arguments dans `sys.argv`, un calibrage qui rend `ligne_juge` ·
          ③ appeler `main` · ④ TOUT rétablir dans un `finally` · ⑤ exiger le code 1 ou l'erreur, le fragment, et
          qu'aucun fichier ne reste.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Ces refus ne s'atteignent pas avec de vraies données cohérentes.
        ⑨ CE QUI CLOCHE — Voir `faux_juge`, ⑨.
        ⑩ EFFET — Écrit dans un dossier temporaire ; modifie `sys.modules`, `sys.argv` et `jouer.calibrer_par_le_juge` le temps du cas.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        d = dossier()
        base = os.path.join(d, "depot")
        os.makedirs(os.path.join(base, "programmes"))
        f_reg = ecrire(os.path.join(d, "registre.csv"), list(fiche), [fiche] * nb_fiches)
        f_comb = ecrire(os.path.join(d, "COMBINATOIRE_F_E01.csv"), colonnes, deux)
        f_out = os.path.join(d, "RESULTATS.csv")
        J = faux_juge(os.path.abspath(base), registre=f_reg, **reglages)
        avant_mod, avant_argv, avant_cal = sys.modules.get("JUGE_DES_STRATEGIES"), sys.argv, jouer.calibrer_par_le_juge
        sys.modules["JUGE_DES_STRATEGIES"] = J
        sys.argv = ["JOUER_LES_VERSIONS.py", base, f_comb, f_out]
        jouer.calibrer_par_le_juge = lambda b, i: (True, ligne_juge)
        tampon, code, erreur = io.StringIO(), None, ""
        try:
            with contextlib.redirect_stdout(tampon):
                code = jouer.main()
        except ValueError as e:
            erreur = str(e)
        finally:
            jouer.calibrer_par_le_juge = avant_cal
            sys.argv = avant_argv
            if avant_mod is None:
                sys.modules.pop("JUGE_DES_STRATEGIES", None)
            else:
                sys.modules["JUGE_DES_STRATEGIES"] = avant_mod
        texte = tampon.getvalue() + erreur
        reste = os.path.exists(f_out) or os.path.exists(f_out + ".en_cours")
        ok = (bool(erreur) if leve else code == 1) and fragment in texte and not reste
        noter(nom, ok, "code %s · erreur %r · fragment %s · fichier restant %s" % (code, erreur[:80], "vu" if fragment in texte else "ABSENT", reste))

    un_cas("JOUER (faux juge), juge importé d'ailleurs", "le juge importé n'est pas celui du dépôt", ailleurs=True)
    un_cas("JOUER (faux juge), fiche deux fois au registre", "trouvée 2 fois au registre", nb_fiches=2)
    un_cas("JOUER (faux juge), la porte 0 refuse", "la porte 0 refuse", leve=True, porte=(False, ["tp illisible"], None))
    un_cas("JOUER (faux juge), valeurs absentes des cours", "valeurs absentes des cours", leve=True, inconnus=["XYZ"])
    un_cas("JOUER (faux juge), la fiche ne produit aucune opération", "la fiche elle-même ne produit aucune opération", n=0)
    un_cas("JOUER (faux juge), le lecteur refuse la lecture", "le lecteur unique a mis 1 ligne(s)", refus_lecture=True)
    un_cas("JOUER (faux juge), le juge seul dit autre chose", "ne rendent pas la même chose pour la fiche",
           ligne_juge="2 operations . 50.0 % de reussite . +5.00 EUR")
    un_cas("JOUER (faux juge), période différente pour une version", "période différente pour F-E01-2", leve=True,
           porte=lambda f: (True, [], ("2024-01-02", "2026-07-10") if f.get("tp") == "0.04" else ("2024-01-03", "2026-07-10")))
    J = faux_juge("x")
    e_h = jouer.controler_fusion(J, {"tp": "0.04", "sl": "0.025", "horizon": "20", "univers": "TTE"},
                                 {"tp": "0.04", "sl": "0.025", "horizon": "25", "univers": "TTE"})
    noter("JOUER.controler_fusion, horizon différent : un écart « horizon lu »", len(e_h) == 1 and e_h[0].startswith("horizon lu"), str(e_h))
    e_u = jouer.controler_fusion(J, {"tp": "0.04", "sl": "0.025", "horizon": "20", "univers": "TTE"},
                                 {"tp": "0.04", "sl": "0.025", "horizon": "20", "univers": "ENGI"})
    noter("JOUER.controler_fusion, univers différent : un écart « univers lu »", len(e_u) == 1 and e_u[0].startswith("univers lu"), str(e_u))


def cas_rejeu_complet(racine):
    """Rejoue les 2 695 versions de l'essai E01 contre le témoin, une fois.

    ① RÔLE — Prouver que la moulinette refait exactement les résultats du 08-10-2026.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — La combinatoire et le témoin de l'essai E01 existent.
    ⑤ SORTIE — Aucune valeur.
      [rend: 0]
    ⑥ TRAITEMENT — Lancer JOUER_LES_VERSIONS sur la vraie combinatoire, résultats dans un dossier temporaire ;
      exiger le code 0 et « 2695 versions comparées, 0 écarts ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — C'est la preuve de fond ; les cas réduits n'en sont que les refus.
    ⑨ CE QUI CLOCHE — Environ deux minutes, cinq sous la mesure du certificateur.
    ⑩ EFFET — Lance le programme ; écrit dans un dossier temporaire.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    c, s = lancer(racine, P_JOUER, ".", COMBINATOIRE, os.path.join(dossier(), "RESULTATS.csv"))
    attendre("JOUER, rejeu complet contre le témoin : 0 écart", c, s, 0, "2695 versions comparées, 0 écarts")


def main(argv):
    """Joue tous les cas et sort sur un seul verdict.

    ① RÔLE — Rendre le verdict des épreuves de la moulinette.
    ② CONTEXTE D'APPEL — Le bas de ce fichier.
    ③ ENTRÉE — `argv` : les arguments de la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — Un argument, la racine du dépôt.
    ⑤ SORTIE — Aucune valeur rendue : sort avec 0, 1 ou 2.
      [rend: 0]
    ⑥ TRAITEMENT — ① vérifier les fichiers · ② jouer les familles de cas · ③ effacer les dossiers · ④ sortir.
    ⑦ UNITÉ — Des codes de sortie.
    ⑧ POURQUOI — Un seul geste pour savoir si la moulinette tient.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance des programmes ; affiche ; efface ses dossiers temporaires.
    ⑪ TERMINAISON — Sort lui-même.
      [sort: oui]
    """
    if len(argv) != 2:
        print(__doc__)
        sys.exit(2)
    racine = os.path.abspath(argv[1])
    manquants = [f for f in ATTENDUS if not os.path.isfile(os.path.join(racine, f))]
    if manquants:
        print("ARRÊT : fichiers attendus absents : " + " · ".join(manquants))
        sys.exit(2)
    try:
        for famille in (cas_preparer, cas_decliner, cas_epreuves_de_la_declinaison, cas_jouer_dehors,
                        cas_jouer_dedans, cas_rejeu_complet):
            try:
                famille(racine)
            except Exception as e:
                noter("famille %s interrompue" % famille.__name__, False, "%s : %s" % (type(e).__name__, e))
    finally:
        for d in DOSSIERS:
            shutil.rmtree(d, ignore_errors=True)
    tombes = [n for n, ok in RESULTATS if not ok]
    print("CAS : %d / %d tenus" % (len(RESULTATS) - len(tombes), len(RESULTATS)))
    if tombes:
        print("VERDICT : LA MOULINETTE NE TIENT PAS")
        sys.exit(1)
    print("VERDICT : LA MOULINETTE TIENT")
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)
