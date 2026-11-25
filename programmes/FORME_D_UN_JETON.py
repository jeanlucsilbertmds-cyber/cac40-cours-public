#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La forme d'un jeton d'accès : LE SEUL motif du dépôt qui dit si un texte porte un secret de connexion.

① RÔLE — Dire si des octets (ou un texte) portent une chaîne de la forme d'un jeton d'accès ou d'un identifiant
  de connexion, avant qu'ils ne sortent du dépôt privé. Quatre formes, dans cet ordre :
  ① un jeton fin de GitHub : le préfixe « github » « _pat_ » suivi d'au moins 20 caractères de mot ;
  ② un jeton GitHub des autres familles : « gh » suivi d'une lettre parmi p (classique), o (OAuth), u (utilisateur),
     s (serveur : la forme du GITHUB_TOKEN que reçoit chaque passage des Actions), r (renouvellement), puis « _ » et
     au moins 20 lettres ou chiffres ; « gh » n'est précédé ni d'une lettre ni d'un chiffre (un « _ » devant, comme
     dans « X_ghp_… », ne le cache pas : relecture du tour 2, D4) ;
  ③ une adresse web (http ou https) qui porte, avant « @ », un identifiant et un secret séparés par « : » ;
  ④ un en-tête « Authorization: Basic » suivi d'au moins 8 caractères de base64 (la forme que prend un jeton passé à
     git par http.extraheader).
  Majuscules indifférentes pour les quatre (git écrit « AUTHORIZATION: basic »).
② CONTEXTE D'APPEL — Chargé par programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py (`refus_avant_publication`), qui le lit
  à côté de lui-même, par son chemin ; éprouvé par tests/EPREUVES_DU_CIRCUIT_PUBLIC_Jeu_15-10-2026.py (E8 :
  l'épreuve unitaire du motif, et la propriété « aucun autre fichier de code publié ne compile un motif de jeton »).
  Jamais lancé seul.
③ ENTRÉE — Aucune ligne de commande ; voir la fonction.
④ CONDITIONS D'ENTRÉE — —
⑤ SORTIE — Le module rend MOTIF_DE_JETON (une expression rationnelle sur des octets), ACCES_DANS_UNE_ADRESSE, et deux
  fonctions : `porte_une_forme_de_jeton` (juger) et `masquer_les_acces` (afficher sans montrer).
⑥ TRAITEMENT — Voir la fonction.
⑦ UNITÉ — —
⑧ POURQUOI — Défaut M5 (relecture de Cowork du 04-11-2026 à 21h17, I1) : le fabricant du dépôt public publiait un
  fichier portant un jeton. Le premier motif (tour 1 de la réparation) ne voyait que les formes ① et ④ ; la
  relecture neuve du 04-11-2026 (D1) a fait publier un jeton classique, un jeton des Actions et un en-tête
  « Authorization: token … », fabricant au code 0, alors qu'un motif plus large existait déjà dans une étude datée :
  deux implémentations d'une même chose divergent toujours (R-708). Le superviseur R-759 du 05-11-2026 à 00h52 a
  jugé « DE FOND » d'en faire UN module de programmes/, importé par les programmes en usage, IGNORECASE gardé.
  Coût mesuré par lui : 0 fichier touché parmi les 145 que publie le fabricant (motif sur du texte, IGNORECASE),
  et la ligne du motif ne se prend pas elle-même.
⑨ CE QUI CLOCHE — C'est un motif : il ne voit pas un jeton coupé en deux littéraux (« 'github' '_pat_…' », la forme
  même qu'emploient les épreuves pour fabriquer leurs jetons fictifs), ni une valeur base64 écrite sans
  « Authorization: » devant (« http.extraheader basic <b64> »), ni un jeton d'un autre service, ni un mot de passe en
  clair : relecture du 04-11-2026, cas A4 et A7 ; élargir forme par forme serait les chasser une à une (superviseur
  R-759). Il lit les octets tels quels : un texte encodé autrement qu'en UTF-8 ou en ASCII lui échappe, y compris
  l'UTF-16 et l'UTF-32 SANS BOM, qui sont de l'UTF-8 valide entrelacé d'octets nuls ; c'est pourquoi le fabricant
  refuse tout fichier publié qui n'est pas du TEXTE UTF-8 STRICT (UTF-8 valide, et aucun caractère de contrôle hors
  tabulation et sauts de ligne). Un jeton collé derrière une lettre ou un chiffre (« abcghp_… ») n'est pas vu.
  · Faux rouge possible :
  « Authorization: Basic » suivi d'un mot de 8 lettres ou plus, ou un exemple d'adresse à identifiant et secret
  écrit d'un bloc dans un commentaire ; et une fiche qui pousse par une adresse « https://x-access-token: » suivie
  d'une variable (« ${VAR} ») puis de « @ » fait arrêter le circuit (une variable prise pour un secret ; remède au
  BACKLOG, relecture du tour 2, D3) ; le refus le dit, rien n'est publié. · Le filtre de
  etudes/JOURNEE_31-10-2026/nuit/pousser_si_propre.sh (grep, en shell) et les motifs des études datées
  (etudes/JOURNEE_31-10-2026/inscription_backlog/, etudes/JOURNEE_01-11-2026/inscription_backlog_2/) sont des
  copies qui ne lisent pas ce module : copies connues, laissées telles quelles (traces datées, ou shell), à
  aligner si elles resservent (BACKLOG).
  · Le masquage (`masquer_les_acces`, 25-11-2026) masque PLUS large que le motif ne refuse : toute partie « <…>@ »
  d'une adresse, y compris « ssh://git@ », devient « ***@ ». C'est voulu : afficher un refus de git sans rien montrer
  qui puisse être un accès ; MOTIF_DE_JETON, lui, n'est PAS élargi (il ferait refuser « ssh://git@… » à la publication).
⑩ EFFET — Aucun : ni lecture ni écriture.
⑪ TERMINAISON — —
"""
import re

# LE MOTIF, sur une seule ligne : les quatre formes de la fiche, dans l'ordre, majuscules indifférentes. Il porte sur
# des OCTETS : le fabricant lit les fichiers en octets, sans les décoder.
MOTIF_DE_JETON = re.compile(rb"github_pat_\w{20,}|(?<![A-Za-z0-9])gh[pousr]_[A-Za-z0-9]{20,}|https?://[^/\s:@]+:[^/\s@]+@|authorization:[ \t]*basic[ \t]+[A-Za-z0-9+/=]{8,}", re.IGNORECASE)


def porte_une_forme_de_jeton(donnee):
    """Rend vrai si `donnee` porte une chaîne de la forme d'un jeton (MOTIF_DE_JETON).

    ① RÔLE — Répondre à « ces octets portent-ils un secret de connexion ? » d'une seule façon, pour tout le dépôt.
    ② CONTEXTE D'APPEL — `refus_avant_publication` de programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, une fois par
      fichier à publier ; l'épreuve unitaire du motif (E8 de tests/EPREUVES_DU_CIRCUIT_PUBLIC_Jeu_15-10-2026.py).
    ③ ENTRÉE — `donnee` : des octets (le contenu brut d'un fichier), ou un texte, encodé alors en UTF-8 avant
      d'être lu.
    ④ CONDITIONS D'ENTRÉE — `donnee` est de type bytes ou str.
    ⑤ SORTIE — UNE valeur : True si une des quatre formes y figure, False sinon.
      [rend: 1]
    ⑥ TRAITEMENT — encoder le texte en UTF-8 s'il en est un ; chercher MOTIF_DE_JETON n'importe où dans les octets.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une seule fonction, un seul motif : deux implémentations d'une même chose divergent toujours
      (R-708 ; relecture neuve du 04-11-2026, D1).
    ⑨ CE QUI CLOCHE — Voir la fiche du module (jeton coupé en deux, valeur base64 sans en-tête, autres services,
      faux rouges possibles). Ne dit pas OÙ est la chaîne ni laquelle : celui qui refuse ne doit pas l'afficher.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; une recherche dans des octets en mémoire.
      [sort: non]
    """
    if isinstance(donnee, str):
        donnee = donnee.encode("utf-8")
    return MOTIF_DE_JETON.search(donnee) is not None


# TOUT ACCÈS ÉCRIT DANS UNE ADRESSE, avant « @ » (« https://<accès>@hôte », « ssh://git@hôte ») : servi UNIQUEMENT au
# masquage, jamais au refus (superviseur R-759 du 25-11-2026, point 3 : le masquage vit DANS ce module, sous une fonction
# distincte ; MOTIF_DE_JETON n'est pas élargi). Cas fondateur : DEPOSER_UNE_DEMANDE.py compilait ce motif lui-même
# (ligne 371 depuis 9bc157ee0), seconde écriture d'un motif de jeton que l'épreuve E8 ② signale.
ACCES_DANS_UNE_ADRESSE = re.compile(rb"://[^/@\s]*@")


def masquer_les_acces(texte):
    """Rend `texte` où chaque forme de jeton et chaque accès écrit dans une adresse est remplacé par « *** ».

    ① RÔLE — Afficher un message venu d'ailleurs (un refus de git) en entier, sans y laisser un accès en clair.
    ② CONTEXTE D'APPEL — programmes/DEPOSER_UNE_DEMANDE.py, sur le refus d'une poussée (point T5 du RELU de
      travail-file-demandes) et sur l'erreur d'un fetch (E3 du RELU du 25-11-2026) ; éprouvé par D10 et D15 de
      tests/EPREUVES_DU_RELAIS_DES_SERIES_Dim_08-11-2026.py.
    ③ ENTRÉE — `texte` : un texte (str).
    ④ CONDITIONS D'ENTRÉE — `texte` est de type str.
    ⑤ SORTIE — UNE valeur : le texte masqué (str) ; un caractère non encodable devient « ? » (encodage UTF-8 avec
      remplacement), sans effet sur un texte venu de git.
      [rend: 1]
    ⑥ TRAITEMENT — encoder en UTF-8 ; remplacer chaque MOTIF_DE_JETON par « *** », puis chaque
      ACCES_DANS_UNE_ADRESSE par « ://***@ » ; décoder.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un refus de git cite l'adresse de « origin », qui peut porter un accès ; le motif seul ne voit pas
      « https://<accès>@ » sans « : » ni préfixe de jeton. R-708 : les motifs de jeton vivent ici et nulle part ailleurs.
    ⑨ CE QUI CLOCHE — Les limites de MOTIF_DE_JETON (fiche du module) ; un accès écrit hors d'une adresse et hors des
      quatre formes passe en clair (« Authorization: Bearer <x> » sans préfixe de jeton, « token <40 hexadécimaux> »,
      « utilisateur:secret@hote:depot » sans « :// »). Mesuré par les relecteurs du 25-11-2026 (C3 et constat de C4),
      sur des chaînes FACTICES (non recopiées ici : ce fichier ne doit porter aucune forme de jeton) : un « / » dans
      l'accès arrête ACCES_DANS_UNE_ADRESSE, qui ne masque rien ; un « @ » littéral dans l'accès laisse ressortir ce
      qui suit le premier « @ » ; un blanc dans l'accès (tabulation) le laisse en clair. Ces trois adresses sont invalides pour git (ces
      caractères s'y écrivent encodés), et les jetons GitHub n'en portent pas : risque bas. Le schéma « https:// »
      d'une adresse peut être mangé par MOTIF_DE_JETON (cosmétique). Une entrée `bytes` lève AttributeError :
      DEPOSER la rattrape (sens prudent).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; deux remplacements en mémoire.
      [sort: non]
    """
    octets = MOTIF_DE_JETON.sub(b"***", texte.encode("utf-8", "replace"))
    return ACCES_DANS_UNE_ADRESSE.sub(b"://***@", octets).decode("utf-8", "replace")
