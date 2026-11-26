#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_FORME_D_UN_JETON — Jeu 26-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Défaut N-90 (relecture de Cowork du 26-11-2026 à 00h13, branche travail-publication-auto, commit
2cc16746) : le garde-fou « M5 » du fabricant du dépôt public (programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py) refusait un
fichier portant un jeton GitHub en clair ou un en-tête « Authorization: basic <base64> », mais publiait, code 0, un
fichier portant la valeur base64 NUE de « x-access-token:<jeton> » — la valeur même que calcule le circuit
(`printf 'x-access-token:%s' "$JETON" | base64 -w0`). Le superviseur R-759 du 26-11-2026 à 00h16 (BACKLOG A-1027) :
« N-90 RUSTINE si doublé (R-708) : à corriger dans FORME_D_UN_JETON.py sur une branche à part ». La correction vit
donc dans programmes/FORME_D_UN_JETON.py, le seul motif de jeton du dépôt : une suite base64 dont le décodage porte
une forme de jeton est une forme de jeton. Cette épreuve prouve la propriété, et que rien de ce qui était reconnu
avant ne cesse de l'être.

① RÔLE — Juger `porte_une_forme_de_jeton` de programmes/FORME_D_UN_JETON.py sur des cas connus (positifs et
  négatifs), sur de vrais fichiers du dépôt, et à travers le fabricant ; avec --saboter, prouver que chaque cas qui
  garde la correction rougit quand on retire ce qu'il garde.
② CONTEXTE D'APPEL — À la main avant toute livraison qui touche programmes/FORME_D_UN_JETON.py (R-731), et par la
  certification (épreuve de tests/, lancée avec la racine) :
  python3 -B tests/EPREUVES_DE_LA_FORME_D_UN_JETON_Jeu_26-11-2026.py [<racine>] [--saboter]
③ ENTRÉE — La racine d'un dépôt (par défaut, le dossier parent de tests/) : programmes/FORME_D_UN_JETON.py,
  programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py (sa liste `code_a_publier` et son garde `refus_avant_publication`),
  tests/EPREUVES_DU_CIRCUIT_PUBLIC_Jeu_15-10-2026.py (ses cas CAS_DU_MOTIF, IMPORTÉS et jamais recopiés : deux
  écritures d'une même chose divergent toujours, R-708), tests/EPREUVES_DU_CIRCUIT_DES_SERIES_Jeu_05-11-2026.py (une
  vraie ligne de shell qui calcule le base64, R-732) et temoins/PAGES_BNAINS_DES_ACTIONS/ (de vraies images en
  base64, R-732).
④ CONDITIONS D'ENTRÉE — bash et base64 (coreutils) sont présents ; le module yaml s'importe (les cas CAS_DU_MOTIF
  vivent dans une épreuve qui l'exige). Un fichier d'entrée absent, une ligne réelle introuvable : une FAUTE, code 1
  (R-734 : un contrôle qui n'a pas pu tourner ne rend pas 0).
⑤ SORTIE — Le code de sortie : 0 si chaque cas donne la réponse attendue et, avec --saboter, si chaque sabotage fait
  rougir EXACTEMENT les cas qu'il vise (au moins un) ; 1 sinon ; 2 si un sabotage ne s'applique plus. À l'écran :
  une ligne par cas (VERT ou ROUGE), une ligne par sabotage.
  [rend: 1]
⑥ TRAITEMENT — Les cas (`les_cas`) : B1-B9, des jetons FICTIFS fabriqués à l'exécution (jamais écrits d'un bloc :
  ce fichier est publié, et le motif le refuserait), encodés en base64 et qui doivent être reconnus — nu, collé
  derrière 1, 2, 3 caractères de l'alphabet (le décalage d'alignement), jeton classique, alphabet sûr pour les
  adresses sans « = », jeton des Actions derrière « http.extraheader basic » sans « Authorization: », adresse à
  identifiants ; B10 le base64 nu de la plus courte forme du motif (« http:// », une lettre, « : », une lettre,
  « @ » : 11 octets, 16 caractères avec « = » ; défaut N-100, il épingle PLUS_COURTE_SUITE) ; C1-C6 (défaut N-99) la
  sortie de la VRAIE commande `base64 -w 76` ou `-w 64` (R-732) d'un texte « '#'×n, saut de ligne,
  x-access-token:<jeton fictif> », n de 0 à 119 — le jeton tombe à toute position, souvent à cheval sur deux lignes —
  qui doit être reconnue pour CHAQUE n : en lignes (jeton classique et jeton fin, 76 et 64), en chaînes indentées
  entre guillemets, en fins de ligne CRLF ; R1 la VRAIE commande de tests/EPREUVES_DU_CIRCUIT_DES_SERIES_Jeu_05-11-2026.py exécutée par bash
  avec un jeton fictif ; A* chaque cas de CAS_DU_MOTIF garde sa réponse ; N1-N5 des base64 innocents qui ne doivent
  PAS l'être (long texte, empreinte sha256, jeton trop court d'un caractère, secret qui n'a pas la forme d'un jeton,
  « x-access-token: » seul) ; N6 les vraies images base64 de temoins/PAGES_BNAINS_DES_ACTIONS/ ; N7 aucun des
  fichiers que publie le fabricant ; F1 le garde du fabricant, chargé d'un dossier jetable où le module est son
  voisin, refuse un fichier programmes/FUITE_B64NU.py (le cas de Cowork) et accepte un fichier innocent.
  Avec --saboter, pour chaque sabotage de SABOTAGES : copier le module dans un dossier jetable, y remplacer UNE fois
  le texte visé, rejouer tous les cas avec la copie, et comparer l'ensemble des cas rouges à l'ensemble attendu.
  Sept sabotages : Z1 sans décodage, Z2 sans décalage, Z3 alphabet sûr non ramené (N-90) ; S1 sans la vue privée des
  séparateurs, S2 saut de ligne gardé, S3 guillemets gardés (N-99) ; S4 PLUS_COURTE_SUITE 15 → 17 (N-100).
⑦ UNITÉ — —
⑧ POURQUOI — R-731 : tout code écrit ou modifié passe des épreuves sabotées. Un jeu d'épreuves se sabote contre sa
  propre correction : une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration.
⑨ CE QUI CLOCHE — Les jetons sont fictifs : leur forme suit les préfixes de GitHub, pas un vrai jeton. Le rejeu
  complet du fabricant (commit extrait, clone public) n'est pas joué ici : seul son garde `refus_avant_publication`
  l'est (le rejeu entier est capturé à la main dans echanges/A_RELIRE.md de la branche travail-jeton-b64). N7 lit le
  disque de la racine, pas un commit. Les cas « innocents » ne prouvent pas qu'aucun faux rouge n'existe ailleurs.
⑩ EFFET — Écrit puis efface des dossiers jetables (tempfile) ; lance bash. N'écrit rien dans la racine.
⑪ TERMINAISON — Rend la main ; chaque bash et chaque base64 est borné à 30 s.
  [sort: oui]
"""
import base64
import glob
import hashlib
import importlib.util as _iu
import os
import re
import shutil
import subprocess
import sys
import tempfile

MODULE = "programmes/FORME_D_UN_JETON.py"
FABRICANT = "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"
EPREUVE_DU_MOTIF = "tests/EPREUVES_DU_CIRCUIT_PUBLIC_Jeu_15-10-2026.py"
LIGNE_REELLE = "tests/EPREUVES_DU_CIRCUIT_DES_SERIES_Jeu_05-11-2026.py"
IMAGES_REELLES = "temoins/PAGES_BNAINS_DES_ACTIONS"

# Jetons FICTIFS, coupés en littéraux : écrits d'un bloc, ce fichier publié serait refusé par le motif qu'il éprouve.
PAT = "github" + "_pat_" + "11AB2CD3E" + "Zx9" * 25
GHP = "gh" + "p_" + "A1b2C3d4E5" * 3 + "Qq"
GHS = "gh" + "s_" + "Z9y8X7w6V5" * 3 + "Uu"
PREFIXE = "x-access-token:"

# Les sabotages : (nom, texte visé dans le module, remplacement, cas qui doivent rougir — et eux seuls).
DECALES = {"B2 collé derrière 1 caractère", "B3 collé derrière 2 caractères", "B4 collé derrière 3 caractères"}
# Les cas N-99 : la sortie de la VRAIE commande `base64 -w <largeur>` (R-732), coupée en lignes.
COUPES = {"C1 base64 -w 76 de '#'×n + x-access-token:<ghp_>, n de 0 à 119",
          "C2 base64 -w 64 de '#'×n + x-access-token:<ghp_>, n de 0 à 119",
          "C3 base64 -w 76 de '#'×n + x-access-token:<PAT>, n de 0 à 119",
          "C4 base64 -w 64 de '#'×n + x-access-token:<PAT>, n de 0 à 119",
          "C6 base64 -w 76 en fins de ligne CRLF, n de 0 à 119"}
GUILLEMETS = "C5 base64 -w 76 en chaînes indentées entre guillemets, n de 0 à 119"
SABOTAGES = (
    ("Z1 sans décodage (le motif d'avant N-90)", "        for suite in SUITE_BASE64.finditer(vue):\n",
     "        for suite in ():\n",
     {"B1 base64 nu de x-access-token:<PAT>", "B5 base64 de x-access-token:<ghp_>",
      "B6 alphabet sûr pour les adresses, sans =", "B7 base64 suivi de = puis de texte",
      "B8 ghs_ derrière http.extraheader basic", "B9 base64 d'une adresse à identifiants",
      "R1 vraie ligne de shell qui calcule le base64", "F1 le garde du fabricant refuse FUITE_B64NU",
      "B10 base64 nu de la plus courte forme"} | DECALES | COUPES | {GUILLEMETS}),
    ("Z2 sans décalage d'alignement", "            for decalage in range(4):\n", "            for decalage in range(1):\n",
     set(DECALES)),
    # Sans le retour à l'alphabet standard, binascii JETTE « - » et « _ » : la longueur change et le décodage TOMBE
    # (binascii.Error, « Incorrect padding ») — sur le cas B6, et sur tout texte innocent où une suite de 15 caractères
    # ou plus porte « _ » ou « - » (mesuré le 26-11-2026 : 4 cas innocents, dont N7, les fichiers publiés ; un
    # cinquième depuis N-99, « le filtre sed du dépôt », dont la vue privée de ses blancs et guillemets forme une
    # telle suite). Le fabricant s'arrêterait alors sur du code innocent. Ce n'est pas le décalage qui le garde : les quatre décalages
    # rattrapent les caractères jetés ; et un jeton GitHub en ASCII ne fait jamais naître « - » ni « _ » dans son
    # propre base64 (seuls « > ? ~ » et le non-ASCII y mènent), d'où le suffixe de B6.
    ("Z3 alphabet sûr non ramené", "            brute = suite.group().rstrip(b\"=\").translate(_VERS_STANDARD)\n",
     "            brute = suite.group().rstrip(b\"=\")\n",
     {"B6 alphabet sûr pour les adresses, sans =", "A ${{ secrets.X }} dans une adresse", "A ghp_ suivi de 19 caractères",
      "A github_pat_ suivi de 19 caractères", "N7 aucun fichier publié par le fabricant", "A le filtre sed du dépôt"}),
    # N-99 : la seconde vue (texte privé de ses blancs et guillemets). S1 la retire ; S2 garde la vue mais n'y retire
    # plus les sauts de ligne ; S3 n'y retire plus les guillemets — seul le cas à guillemets doit alors rougir.
    ("S1 sans la vue privée des séparateurs", "    for vue in (donnee, donnee.translate(None, _SEPARATEURS)):\n",
     "    for vue in (donnee,):\n", COUPES | {GUILLEMETS}),
    ("S2 saut de ligne gardé dans la vue", "_SEPARATEURS = b\" \\t\\r\\n\\\"'\"\n", "_SEPARATEURS = b\" \\t\\r\\\"'\"\n",
     COUPES | {GUILLEMETS}),
    ("S3 guillemets gardés dans la vue", "_SEPARATEURS = b\" \\t\\r\\n\\\"'\"\n", "_SEPARATEURS = b\" \\t\\r\\n\"\n",
     {GUILLEMETS}),
    # N-100 : PLUS_COURTE_SUITE épinglé par la plus courte forme (11 octets, 16 caractères avec « = », 15 sans).
    ("S4 PLUS_COURTE_SUITE 15 → 17", "PLUS_COURTE_SUITE = 15\n", "PLUS_COURTE_SUITE = 17\n",
     {"B10 base64 nu de la plus courte forme"}),
)


def charger(chemin, nom):
    """Charge un fichier Python comme module, par son chemin.

    ① RÔLE — Juger le module de la racine (ou d'une copie sabotée), jamais un module de même nom déjà chargé.
    ② CONTEXTE D'APPEL — `les_cas`, `main`.
    ③ ENTRÉE — `chemin` : le fichier · `nom` : le nom du module.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe et s'exécute ; sinon l'exception remonte (l'appelant la compte).
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — spec_from_file_location, module_from_spec, exec_module.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une copie sabotée doit être jugée par son propre texte.
    ⑨ CE QUI CLOCHE — Exécute le fichier : la même confiance que pour le dépôt éprouvé.
    ⑩ EFFET — Exécute le fichier chargé.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    sp = _iu.spec_from_file_location(nom, chemin)
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def b64(texte):
    """Rend le base64 standard (avec « = ») du texte, en str.

    ① RÔLE — Fabriquer un base64 de cas.
    ② CONTEXTE D'APPEL — `les_cas`.
    ③ ENTRÉE — `texte` : une str.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : une str.
      [rend: 1]
    ⑥ TRAITEMENT — UTF-8 puis base64.b64encode.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return base64.b64encode(texte.encode("utf-8")).decode("ascii")


_DEJA_CODES = {}


def base64_coupe(texte, largeur):
    """Rend la sortie de la VRAIE commande `base64 -w <largeur>` sur le texte (octets), une fois par couple.

    ① RÔLE — Fabriquer les cas N-99 avec l'outil réel, pas avec une imitation (R-732 : un cas vient d'un vrai outil).
    ② CONTEXTE D'APPEL — `les_cas` (cas C1 à C6), une fois sans sabotage puis une fois par sabotage.
    ③ ENTRÉE — `texte` : une str · `largeur` : le nombre de caractères par ligne passé à `-w`.
    ④ CONDITIONS D'ENTRÉE — La commande base64 (coreutils) est présente ; sinon l'exception remonte et le cas est une
      FAUTE (R-734).
    ⑤ SORTIE — UNE valeur : les octets écrits par la commande (lignes terminées par « \\n »).
      [rend: 1]
    ⑥ TRAITEMENT — Lancer `base64 -w <largeur>` sur le texte en UTF-8, garder la sortie dans `_DEJA_CODES` pour
      ne pas relancer la commande à chaque sabotage ; une sortie vide ou un code non nul lève une erreur.
    ⑦ UNITÉ — `largeur` : des caractères base64.
    ⑧ POURQUOI — 120 positions × 4 couples × 8 passages : sans la mémoire, près de 4 000 lancements.
    ⑨ CE QUI CLOCHE — La mémoire suppose que la commande rend toujours la même sortie (vrai pour base64).
    ⑩ EFFET — Lance la commande base64.
    ⑪ TERMINAISON — Rend la main ; chaque lancement borné à 30 s.
      [sort: non]
    """
    cle = (texte, largeur)
    if cle not in _DEJA_CODES:
        r = subprocess.run(["base64", "-w", str(largeur)], input=texte.encode("utf-8"), capture_output=True,
                           timeout=30, check=True)
        if not r.stdout.strip():
            raise RuntimeError("la commande base64 n'a rien écrit")
        _DEJA_CODES[cle] = r.stdout
    return _DEJA_CODES[cle]


def urlsure_avec_tiret():
    """Rend un base64 « sûr pour les adresses », sans « = », de « x-access-token:<PAT fictif> », qui porte « - » ou « _ ».

    ① RÔLE — Garantir que le cas B6 éprouve vraiment l'alphabet sûr (un base64 sans « - » ni « _ » ne le distingue pas).
    ② CONTEXTE D'APPEL — `les_cas`.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : une str, ou None si aucun des 64 essais ne porte « - » ni « _ ».
      [rend: 1]
    ⑥ TRAITEMENT — Pour un suffixe de 0 à 63 caractères « ~ » (hors \\w : il clôt le jeton sans le changer), encoder et
      garder le premier essai qui porte « - » ou « _ ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le base64 d'un texte n'emploie « + / » (donc « - _ ») que pour certains octets.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; 64 essais au plus.
      [sort: non]
    """
    for n in range(64):
        e = base64.urlsafe_b64encode((PREFIXE + PAT + "~" * n + "?>").encode()).decode().rstrip("=")
        if "-" in e or "_" in e:
            return e
    return None


def les_cas(racine, forme):
    """Rend la liste des cas : (nom, réponse obtenue ou exception, réponse attendue).

    ① RÔLE — Jouer chaque cas de la fiche du programme avec le module `forme` (celui de la racine ou une copie).
    ② CONTEXTE D'APPEL — `main`, une fois sans sabotage, puis une fois par sabotage.
    ③ ENTRÉE — `racine` : le dépôt éprouvé · `forme` : le chemin du module à juger.
    ④ CONDITIONS D'ENTRÉE — Voir la fiche du programme.
    ⑤ SORTIE — UNE valeur : la liste des triplets (nom, obtenu, attendu) ; `obtenu` est True, False, ou un texte
      « FAUTE : … » quand le cas n'a pas pu se jouer (fichier absent, ligne réelle introuvable, exception).
      [rend: 1]
    ⑥ TRAITEMENT — Voir la fiche du programme (B, R1, A, N, F).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un cas qui ne peut pas se jouer est rouge, jamais sauté (R-734).
    ⑨ CE QUI CLOCHE — F1 copie le fabricant de la racine dans un dossier jetable, sans les données : son contrôle des
      lignes de données n'a rien à comparer (sans effet sur le refus d'un jeton).
    ⑩ EFFET — Lance bash ; écrit puis efface un dossier jetable.
    ⑪ TERMINAISON — Rend la main ; bash borné à 30 s.
      [sort: non]
    """
    cas = []

    def jouer(nom, attendu, fabrique):
        try:
            cas.append((nom, fabrique(), attendu))
        except Exception as e:        # un cas qui tombe est une faute nommée, jamais une épreuve qui s'arrête
            cas.append((nom, f"FAUTE : {type(e).__name__}: {e}"[:200], attendu))

    m = charger(forme, "forme_eprouvee")
    juge = m.porte_une_forme_de_jeton
    nu = b64(PREFIXE + PAT)
    jouer("B1 base64 nu de x-access-token:<PAT>", True, lambda: juge(nu))
    for k, n in zip((1, 2, 3), ("B2 collé derrière 1 caractère", "B3 collé derrière 2 caractères",
                                "B4 collé derrière 3 caractères")):
        jouer(n, True, lambda k=k: juge('JETON64 = "' + "Qz9"[:k] + nu + '"\n'))
    jouer("B5 base64 de x-access-token:<ghp_>", True, lambda: juge("valeur " + b64(PREFIXE + GHP) + " fin"))
    jouer("B6 alphabet sûr pour les adresses, sans =", True,
          lambda: juge("a=" + urlsure_avec_tiret() + ";") if urlsure_avec_tiret() else "FAUTE : pas d'essai à « - _ »")
    jouer("B7 base64 suivi de = puis de texte", True, lambda: juge(b64("x" + PREFIXE + GHP + "!?") + "suite"))
    jouer("B8 ghs_ derrière http.extraheader basic", True,
          lambda: juge("git -c http.extraheader=basic " + b64(PREFIXE + GHS) + " push"))
    jouer("B9 base64 d'une adresse à identifiants", True,
          lambda: juge(b64("https://" + "u" + ":" + "s3cr3t" + "@github.com/x/y")))
    # N-100 : la plus courte forme du motif (une adresse à identifiant et secret d'une lettre, 11 octets), seule.
    jouer("B10 base64 nu de la plus courte forme", True, lambda: juge(b64("http://" + "a" + ":" + "b" + "@")))

    # N-99 : la sortie ORDINAIRE de la vraie commande base64, coupée en lignes, jeton à toute position.
    def coupe(jeton, largeur, habiller=lambda sortie: sortie):
        manques = [n for n in range(120)
                   if not juge(habiller(base64_coupe("#" * n + "\n" + PREFIXE + jeton + "\n", largeur)))]
        return not manques
    jouer("C1 base64 -w 76 de '#'×n + x-access-token:<ghp_>, n de 0 à 119", True, lambda: coupe(GHP, 76))
    jouer("C2 base64 -w 64 de '#'×n + x-access-token:<ghp_>, n de 0 à 119", True, lambda: coupe(GHP, 64))
    jouer("C3 base64 -w 76 de '#'×n + x-access-token:<PAT>, n de 0 à 119", True, lambda: coupe(PAT, 76))
    jouer("C4 base64 -w 64 de '#'×n + x-access-token:<PAT>, n de 0 à 119", True, lambda: coupe(PAT, 64))
    jouer("C5 base64 -w 76 en chaînes indentées entre guillemets, n de 0 à 119", True,
          lambda: coupe(GHP, 76, lambda s: b"JETON64 = (\n" + b"".join(b'    "' + l + b'"\n' for l in s.split(b"\n") if l)
                        + b")\n"))
    jouer("C6 base64 -w 76 en fins de ligne CRLF, n de 0 à 119", True,
          lambda: coupe(GHP, 76, lambda s: s.replace(b"\n", b"\r\n")))

    def ligne_reelle():
        with open(os.path.join(racine, LIGNE_REELLE), encoding="utf-8") as e:
            for ligne in e:
                if PREFIXE + "%s" in ligne and "base64 -w0" in ligne:
                    t = re.search(r'"""(.*?)"""', ligne)
                    if t:
                        sortie = subprocess.run(["bash", "-c", t.group(1)], capture_output=True, timeout=30,
                                                env=dict(os.environ, JETON=PAT)).stdout
                        if not sortie.strip():
                            return "FAUTE : la commande réelle n'a rien écrit"
                        return juge(sortie)
        return f"FAUTE : aucune ligne réelle de {LIGNE_REELLE} ne calcule le base64 de {PREFIXE}"
    jouer("R1 vraie ligne de shell qui calcule le base64", True, ligne_reelle)

    try:
        anciens = charger(os.path.join(racine, EPREUVE_DU_MOTIF), "epreuve_du_motif").CAS_DU_MOTIF
    except BaseException as e:      # SystemExit compris : l'épreuve importée s'arrête si yaml manque
        cas.append(("A0 les cas CAS_DU_MOTIF se lisent", f"FAUTE : {type(e).__name__}: {e}"[:200], True))
        anciens = ()
    if not anciens:
        cas.append(("A0 les cas CAS_DU_MOTIF se lisent", "FAUTE : aucun cas lu", True))
    for nom, chaine, positif in anciens:
        jouer(f"A {nom}", positif, lambda chaine=chaine: juge(chaine))

    jouer("N1 long texte innocent en base64", False, lambda: juge(b64("Simulation uniquement. " * 200)))
    jouer("N2 empreinte sha256 en base64", False,
          lambda: juge(base64.b64encode(hashlib.sha256(b"cours_maitre.csv").digest()).decode()))
    jouer("N3 base64 d'un ghp_ trop court d'un caractère", False,
          lambda: juge(b64(PREFIXE + "gh" + "p_" + "A1b2C3d4E5" + "A1b2C3d4E")))
    jouer("N4 base64 d'un secret sans forme de jeton (limite déclarée)", False, lambda: juge(b64(PREFIXE + "FICTIF")))
    jouer("N5 base64 de x-access-token: seul", False, lambda: juge(b64(PREFIXE)))

    def images_reelles():
        pages = sorted(glob.glob(os.path.join(racine, IMAGES_REELLES, "*.html")))
        vues = 0
        for p in pages:
            with open(p, "rb") as e:
                for im in re.findall(rb"base64,([A-Za-z0-9+/=]{200,})", e.read()):
                    vues += 1
                    if juge(im):
                        return f"FAUTE : une image de {os.path.basename(p)} est prise pour un jeton"
        return False if vues else f"FAUTE : aucune image base64 lue sous {IMAGES_REELLES}"
    jouer("N6 vraies images base64 du dépôt", False, images_reelles)

    def fichiers_publies():
        fab = charger(os.path.join(racine, FABRICANT), "fabricant_liste")
        liste = fab.code_a_publier(racine)
        if not liste:
            return "FAUTE : le fabricant ne publie aucun fichier"
        pris = [f for f in liste if juge(open(os.path.join(racine, f), "rb").read())]
        return f"FAUTE : pris pour un jeton : {pris[:5]}" if pris else False
    jouer("N7 aucun fichier publié par le fabricant", False, fichiers_publies)

    def garde_du_fabricant():
        d = tempfile.mkdtemp(prefix="n90_")
        try:
            os.makedirs(os.path.join(d, "programmes"))
            shutil.copyfile(os.path.join(racine, FABRICANT), os.path.join(d, FABRICANT))
            shutil.copyfile(forme, os.path.join(d, MODULE))
            with open(os.path.join(d, "programmes/FUITE_B64NU.py"), "w", encoding="utf-8") as e:
                e.write('JETON64 = "' + nu + '"\n')
            with open(os.path.join(d, "programmes/INNOCENT.py"), "w", encoding="utf-8") as e:
                e.write('IMAGE = "' + b64("Simulation uniquement. " * 50) + '"\n')
            fab = charger(os.path.join(d, FABRICANT), "fabricant_jetable")
            refus_fuite = fab.refus_avant_publication(d, ["programmes/FUITE_B64NU.py"])
            refus_innocent = fab.refus_avant_publication(d, ["programmes/INNOCENT.py"])
            if refus_innocent:
                return f"FAUTE : le fichier innocent est refusé : {refus_innocent}"
            return any("forme d'un jeton" in r for r in refus_fuite)
        finally:
            shutil.rmtree(d, ignore_errors=True)
    jouer("F1 le garde du fabricant refuse FUITE_B64NU", True, garde_du_fabricant)
    return cas


def rouges(cas):
    """Rend l'ensemble des noms des cas rouges.

    ① RÔLE — Comparer un passage à son attendu.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `cas` : la liste de `les_cas`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un ensemble de noms.
      [rend: 1]
    ⑥ TRAITEMENT — Un cas est rouge si l'obtenu n'est pas exactement l'attendu (une FAUTE l'est toujours).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return {nom for nom, obtenu, attendu in cas if obtenu is not attendu}


def main():
    """Joue les cas, puis les sabotages avec --saboter ; rend le code de sortie.

    ① RÔLE — Voir la fiche du programme.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — sys.argv : [<racine>] [--saboter].
    ④ CONDITIONS D'ENTRÉE — Voir la fiche du programme.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2.
      [rend: 1]
    ⑥ TRAITEMENT — Jouer `les_cas` avec le module de la racine et afficher chaque cas ; avec --saboter, pour chaque
      sabotage, copier le module, appliquer le remplacement (exactement une occurrence, sinon code 2), rejouer, et
      comparer l'ensemble rouge à l'attendu.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-731.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche ; écrit puis efface des dossiers jetables.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    saboter = "--saboter" in sys.argv[1:]
    racine = os.path.abspath(args[0] if args else os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    forme = os.path.join(racine, MODULE)
    if not os.path.isfile(forme):
        print(f"ARRÊT : {MODULE} introuvable sous {racine}")
        return 1
    cas = les_cas(racine, forme)
    for nom, obtenu, attendu in cas:
        print(("VERT  " if obtenu is attendu else "ROUGE ") + f"{nom} : obtenu {obtenu}, attendu {attendu}")
    code = 1 if rouges(cas) else 0
    print(f"Z0 : {len(cas)} cas, {len(rouges(cas))} rouges")
    if not saboter:
        return code
    texte = open(forme, encoding="utf-8").read()
    for nom, vise, remplace, attendus in SABOTAGES:
        if texte.count(vise) != 1:
            print(f"SABOTAGE NON APPLICABLE : {nom} (texte visé trouvé {texte.count(vise)} fois)")
            return 2
        d = tempfile.mkdtemp(prefix="n90_sab_")
        try:
            copie = os.path.join(d, "FORME_D_UN_JETON.py")
            with open(copie, "w", encoding="utf-8") as e:
                e.write(texte.replace(vise, remplace))
            r = rouges(les_cas(racine, copie))
        finally:
            shutil.rmtree(d, ignore_errors=True)
        juste = bool(attendus) and r == attendus
        print(("MORD  " if juste else "RATE  ") + f"{nom} : {len(r)} rouges"
              + ("" if juste else f" ; en trop {sorted(r - attendus)} ; manquants {sorted(attendus - r)}"))
        code = code or (0 if juste else 1)
    return code


if __name__ == "__main__":
    sys.exit(main())
