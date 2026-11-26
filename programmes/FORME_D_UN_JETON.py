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
  Et une propriété qui les enveloppe (défaut N-90, 26-11-2026) : une suite de caractères base64 dont le DÉCODAGE porte
  une des quatre formes en est une aussi — par exemple le base64 nu de « x-access-token:<jeton> », la valeur même que
  le circuit calcule (`printf 'x-access-token:%s' "$JETON" | base64 -w0`) et qui passait jusque-là, faute de
  « Authorization: » devant.
② CONTEXTE D'APPEL — Chargé par programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py (`refus_avant_publication`), qui le lit
  à côté de lui-même, par son chemin ; éprouvé par tests/EPREUVES_DU_CIRCUIT_PUBLIC_Jeu_15-10-2026.py (E8 :
  l'épreuve unitaire du motif, et la propriété « aucun autre fichier de code publié ne compile un motif de jeton »).
  Jamais lancé seul.
③ ENTRÉE — Aucune ligne de commande ; voir la fonction.
④ CONDITIONS D'ENTRÉE — —
⑤ SORTIE — Le module rend MOTIF_DE_JETON (une expression rationnelle sur des octets), SUITE_BASE64 (l'expression qui
  découpe les suites base64 à décoder), PLUS_COURTE_SUITE (un nombre de caractères), ACCES_DANS_UNE_ADRESSE, et deux
  fonctions : `porte_une_forme_de_jeton` (juger) et `masquer_les_acces` (afficher sans montrer) ; en interne,
  _SEPARATEURS (les octets retirés pour la seconde vue : blancs et guillemets, défaut N-99).
⑥ TRAITEMENT — Voir la fonction.
⑦ UNITÉ — PLUS_COURTE_SUITE est un nombre de caractères base64.
⑧ POURQUOI — Défaut M5 (relecture de Cowork du 04-11-2026 à 21h17, I1) : le fabricant du dépôt public publiait un
  fichier portant un jeton. Le premier motif (tour 1 de la réparation) ne voyait que les formes ① et ④ ; la
  relecture neuve du 04-11-2026 (D1) a fait publier un jeton classique, un jeton des Actions et un en-tête
  « Authorization: token … », fabricant au code 0, alors qu'un motif plus large existait déjà dans une étude datée :
  deux implémentations d'une même chose divergent toujours (R-708). Le superviseur R-759 du 05-11-2026 à 00h52 a
  jugé « DE FOND » d'en faire UN module de programmes/, importé par les programmes en usage, IGNORECASE gardé.
  Coût mesuré par lui : 0 fichier touché parmi les 145 que publie le fabricant (motif sur du texte, IGNORECASE),
  et la ligne du motif ne se prend pas elle-même. · Défaut N-90 (relecture de Cowork du 26-11-2026 à 00h13, branche
  travail-publication-auto, commit 2cc16746) : un fichier programmes/FUITE_B64NU.py portant le base64 nu de
  « x-access-token:<PAT fictif> » était publié par le fabricant, code 0. Le superviseur R-759 du 26-11-2026 à 00h16
  (BACKLOG A-1027) a écrit « N-90 RUSTINE si doublé (R-708) : à corriger dans FORME_D_UN_JETON.py sur une branche à
  part, condition d'installation du circuit » : la correction vit donc ici, et elle porte sur une PROPRIÉTÉ (« ce que
  le décodage révèle est jugé par le même motif »), pas sur le texte « x-access-token: » : renommer le préfixe ne la
  fait pas changer d'avis.
⑨ CE QUI CLOCHE — C'est un motif : il ne voit pas un jeton coupé en deux littéraux (« 'github' '_pat_…' », la forme
  même qu'emploient les épreuves pour fabriquer leurs jetons fictifs), ni une valeur base64 écrite sans
  « Authorization: » devant (« http.extraheader basic <b64> ») QUAND SON DÉCODAGE ne porte pas une des quatre formes
  (depuis N-90, le 26-11-2026, le base64 d'un jeton GitHub est vu ; celui d'un mot de passe quelconque ne l'est
  pas), ni un jeton d'un autre service, ni un mot de passe en
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
  aligner si elles resservent (BACKLOG). · CE QUE LE DÉCODAGE COUVRE (N-90, puis N-99 le 26-11-2026) : le base64,
  standard ou sûr pour les adresses, avec ou sans « = », d'un texte qui porte une des quatre formes, écrit sur une
  ligne OU coupé par des blancs ou des guillemets SEULS, à toute largeur et toute position — la sortie par défaut de
  « base64 » (lignes de 76), PEM et MIME (64, 76), les fins de ligne CRLF, des chaînes entre guillemets posées
  côte à côte ou sur plusieurs lignes indentées. CE QUI EST HORS PÉRIMÈTRE est une CLASSE, pas une liste : tout autre
  codage ou transformation — exemples non limitatifs : hexadécimal, base32, %-URL, double encodage, compression,
  échappement « \\n » littéral, UTF-16 avant encodage, coupe qui insère tout autre caractère que des
  blancs ou des guillemets (préfixe de littéral b, r ou f, « # » d'un commentaire, « > » de citation, « - » de liste,
  « \\ », espace insécable : relecture de Cowork du 26-11-2026 05h56, N-103,
  littéraux b"…" côte à côte vus 76 fois sur 120 seulement), jeton coupé en deux littéraux (en clair toujours ;
  en base64 quand les morceaux sont joints par « + » ou séparés par une virgule), secrets d'autres services
  (« x-access-token:motdepasse » encodé échappe comme il échappe en clair). Une forme de cette classe qui est vue
  l'est par hasard (un morceau porte encore la forme entière), jamais par garantie. · RÈGLE D'ARRÊT — PROPOSITION du
  superviseur R-759 du 26-11-2026 (rapport brut : echanges/SUPERVISEUR_R759_JETON_B64.md), EN ATTENTE DE JEAN-LUC,
  NON DÉCIDÉE : « un défaut nouveau de cette famille n'est corrigé que s'il montre qu'un outil du circuit, ou une
  commande standard dans son mode par défaut, produit la forme qui passe ; sinon il rejoint la limite déclarée ».
  Sa raison : un motif est un filet contre l'accident, pas contre l'intention ; contre une fuite volontaire, le
  rempart est ailleurs (jeton à droits minimaux, protection de poussée de GitHub : sujet séparé). · Faux rouge
  possible : un base64 innocent (image, empreinte), ou un texte qui, privé de ses blancs et guillemets, forme une
  suite base64, dont le décodage contiendrait par hasard une forme — mesuré à 0 fichier nouveau sur le dépôt pour
  N-90 puis pour N-99, et à 0 sur 200 blocs aléatoires de 10 ko (alphabet base64, blancs, guillemets) le 26-11-2026
  (echanges/A_RELIRE.md de la branche travail-jeton-b64).
  · Le masquage (`masquer_les_acces`, 25-11-2026) masque PLUS large que le motif ne refuse : toute partie « <…>@ »
  d'une adresse, y compris « ssh://git@ », devient « ***@ ». C'est voulu : afficher un refus de git sans rien montrer
  qui puisse être un accès ; MOTIF_DE_JETON, lui, n'est PAS élargi (il ferait refuser « ssh://git@… » à la publication).
⑩ EFFET — Aucun : ni lecture ni écriture.
⑪ TERMINAISON — —
"""
import binascii
import re

# LE MOTIF, sur une seule ligne : les quatre formes de la fiche, dans l'ordre, majuscules indifférentes. Il porte sur
# des OCTETS : le fabricant lit les fichiers en octets, sans les décoder.
MOTIF_DE_JETON = re.compile(rb"github_pat_\w{20,}|(?<![A-Za-z0-9])gh[pousr]_[A-Za-z0-9]{20,}|https?://[^/\s:@]+:[^/\s@]+@|authorization:[ \t]*basic[ \t]+[A-Za-z0-9+/=]{8,}", re.IGNORECASE)

# LA SUITE BASE64 À DÉCODER (défaut N-90) : les deux alphabets à la fois (standard « + / », sûr pour les adresses
# « - _ »), et les « = » de fin s'il y en a. Une suite plus courte que PLUS_COURTE_SUITE ne peut pas porter la plus
# courte des quatre formes, la ③ réduite à « http:// », une lettre, « : », une lettre et « @ » : 11 octets, soit
# 88 bits, soit au moins 15 caractères de 6 bits.
PLUS_COURTE_SUITE = 15
SUITE_BASE64 = re.compile(rb"[A-Za-z0-9+/_-]{%d,}={0,2}" % PLUS_COURTE_SUITE)
_VERS_STANDARD = bytes.maketrans(b"-_", b"+/")
# LES SÉPARATEURS (défaut N-99, 26-11-2026) : les blancs (espace, tabulation, retour chariot, saut de ligne) et les
# guillemets ne sont pas des caractères base64. La commande `base64` sans « -w0 » coupe sa sortie en lignes de 76
# caractères, PEM et MIME en lignes de 64 ou 76, un programme la colle en chaînes entre guillemets sur plusieurs
# lignes : le texte privé de ces caractères redonne la suite entière, jugée par la même boucle.
_SEPARATEURS = b" \t\r\n\"'"


def porte_une_forme_de_jeton(donnee):
    """Rend vrai si `donnee` porte une chaîne de la forme d'un jeton (MOTIF_DE_JETON), en clair ou en base64.

    ① RÔLE — Répondre à « ces octets portent-ils un secret de connexion ? » d'une seule façon, pour tout le dépôt.
    ② CONTEXTE D'APPEL — `refus_avant_publication` de programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, une fois par
      fichier à publier ; l'épreuve unitaire du motif (E8 de tests/EPREUVES_DU_CIRCUIT_PUBLIC_Jeu_15-10-2026.py).
    ③ ENTRÉE — `donnee` : des octets (le contenu brut d'un fichier), ou un texte, encodé alors en UTF-8 avant
      d'être lu.
    ④ CONDITIONS D'ENTRÉE — `donnee` est de type bytes ou str.
    ⑤ SORTIE — UNE valeur : True si une des quatre formes y figure, en clair ou dans le décodage d'une suite base64
      lue dans les octets tels quels ou dans les octets privés de leurs blancs et guillemets, False sinon.
      [rend: 1]
    ⑥ TRAITEMENT — ① encoder le texte en UTF-8 s'il en est un ; ② chercher MOTIF_DE_JETON n'importe où dans les
      octets : trouvé, rendre True ; ③ sinon, pour chacune des deux vues — les octets tels quels, puis les octets
      privés de _SEPARATEURS (blancs et guillemets, qui ne sont pas des caractères base64 : une sortie de « base64 »
      coupée en lignes, ou collée en chaînes entre guillemets, y redevient une seule suite ; défaut N-99) — et pour
      chaque suite SUITE_BASE64 de cette vue : retirer ses « = », ramener l'alphabet
      sûr pour les adresses (« - _ ») à l'alphabet standard (« + / »), puis la décoder à partir de chacun de ses quatre
      premiers caractères (le base64 se lit par groupes de quatre caractères ; une suite collée derrière d'autres
      caractères de l'alphabet, comme dans « B64eC1h… » ou « dossier/eC1h… », ne commence pas sur un groupe) — chaque
      essai coupé à un multiple de quatre caractères, les un à trois derniers caractères étant complétés par « = »
      quand ils portent au moins un octet ; chercher MOTIF_DE_JETON dans chaque décodage : trouvé, rendre True ;
      ④ rendre False.
    ⑦ UNITÉ — PLUS_COURTE_SUITE et les décalages : des caractères base64.
    ⑧ POURQUOI — Une seule fonction, un seul motif : deux implémentations d'une même chose divergent toujours
      (R-708 ; relecture neuve du 04-11-2026, D1). Le décodage : défaut N-90 (relecture de Cowork du 26-11-2026 à
      00h13) — le base64 nu de « x-access-token:<jeton> », la valeur que le circuit calcule, était publié ; le
      superviseur R-759 du 26-11-2026 à 00h16 (A-1027) a demandé la correction ici, sans doubler le motif. Le même
      MOTIF_DE_JETON juge le clair et le décodé : une forme ajoutée au motif est vue aussi en base64. La seconde vue :
      défaut N-99 (relecture de Cowork du 26-11-2026 à 05h23) — la sortie ORDINAIRE de « base64 » (sans « -w0 »,
      lignes de 76) d'un texte qui porte un jeton à cheval sur deux lignes était publiée, code 0 (46 positions sur
      120) ; le superviseur R-759 du 26-11-2026 a jugé « DE FOND » de l'écrire comme une propriété, dans la MÊME
      boucle et avec le MÊME motif (R-708), et non comme une expression qui recolle des lignes.
    ⑨ CE QUI CLOCHE — Voir la fiche du module (ce que le décodage couvre ; la classe hors périmètre : tout autre
      codage ou transformation ; la règle d'arrêt proposée, en attente de Jean-Luc ; faux rouges possibles). Ne dit
      pas OÙ est la chaîne ni laquelle : celui qui refuse ne doit pas l'afficher. · LE COÛT dépend de la part de
      caractères base64 dans `donnee` (« _ » et « - » compris : un identifiant snake_case est une suite à décoder) :
      quatre décodages par suite de 15 caractères ou plus, et cela DEUX fois depuis N-99 (une fois par vue). Mesuré
      le 26-11-2026 : environ ×8 par rapport au motif seul, dont ×2 dû à N-99, sur un fichier qui n'en contient que (20 Mo
      de base64 en lignes, mesure de Cowork, N-104 : motif seul 0,75 s, N-90 3,25 s, N-99 5,67 s ; mesure de l'auteur :
      3,3 s → 6,0 s ;
      20 Mo de snake_case : 2,6 s → 4,7 s), environ ×1,7 sur le dépôt entier (superviseur : 19,3 s → 32,5 s) —
      chiffres et remesure dans echanges/A_RELIRE.md de la branche travail-jeton-b64. Sans effet aujourd'hui : le
      fabricant ne publie que du code.
      · PLUS_COURTE_SUITE est déduit à la main de la plus courte forme de MOTIF_DE_JETON (11 octets) : une forme plus
      courte ajoutée au motif demanderait de l'abaisser.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; des recherches et des décodages dans des octets en mémoire, en nombre borné par la
      taille de `donnee`.
      [sort: non]
    """
    if isinstance(donnee, str):
        donnee = donnee.encode("utf-8")
    if MOTIF_DE_JETON.search(donnee) is not None:
        return True
    # Deux vues, une seule boucle (N-99) : les octets tels quels, puis les mêmes privés de leurs séparateurs.
    for vue in (donnee, donnee.translate(None, _SEPARATEURS)):
        for suite in SUITE_BASE64.finditer(vue):
            brute = suite.group().rstrip(b"=").translate(_VERS_STANDARD)
            for decalage in range(4):
                morceau = brute[decalage:]
                reste = len(morceau) % 4
                if reste == 1:             # un caractère seul ne porte aucun octet : il est laissé
                    morceau = morceau[:-1]
                elif reste:
                    morceau += b"=" * (4 - reste)
                if len(morceau) < 4:
                    continue
                if MOTIF_DE_JETON.search(binascii.a2b_base64(morceau)) is not None:
                    return True
    return False


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
