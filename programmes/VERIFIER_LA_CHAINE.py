#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""VERIFIER_LA_CHAINE.py — Jeu 19-11-2026 (Paris). EN ESSAI · outil. Simulation uniquement : aucun ordre réel.

LE SENS EN TÊTE. La moulinette (A-541) se fait dans l'ordre : ⓪ réglages préparés et validés · ① DECLINER · ② JOUER
(par tranches, puis assemblées) · ③ TRIER · ④ le juge. Le 19-11-2026, le juge a été lancé sur C5 sans ① ② ③, et rien
ne l'a arrêté (A-919). Ce programme lit le JOURNAL DE LA CHAÎNE — un témoin par étape : le fichier produit et son
empreinte sha256 — et dit si une fiche peut être jugée. LE JUGE L'APPELLE LUI-MÊME (`porte_du_juge`) avant de juger
une fiche qui porte la MARQUE DE MOULINETTE : la porte est là où le saut a eu lieu. La version se reconnaît à la marque
que l'enchaîneur écrit sur la fiche qu'il ajoute au registre, JAMAIS à la forme de son nom (A-921, décision de
Jean-Luc du 19-11-2026 à 12h31, « 1 ») : le 19-11-2026, un relecteur a fait passer « C5E10-OBS-V1-E01-00001 », un
espace final et des minuscules sous l'ancienne épellation du nom. Et la porte confronte les RÉGLAGES jugés à ceux que
② a joués (même relecteur : même identifiant, tp 9.5 au lieu de 0.02, jugé, +31 077,77 € au lieu de −6 413,37 €).

USAGE
    python3 programmes/VERIFIER_LA_CHAINE.py <racine> <id_version> [--juge-fait]
    exemple : python3 programmes/VERIFIER_LA_CHAINE.py /dev/shm/x/depot C5E10-OBS-V1-E01-0001

① RÔLE — Refuser toute fiche marquée dont la chaîne ⓪ ① ② ③ n'est pas faite, dont un fichier a changé depuis son
  témoin, dont les réglages ne sont pas ceux que ② a joués, ou que le tri ③ n'a pas retenue.
② CONTEXTE D'APPEL — `JUGE_DES_STRATEGIES.main` (fonction `porte_du_juge`), `ENCHAINER_LA_MOULINETTE.py` avant chaque
  étape (fonction `motifs`), ou à la main. Aucune tâche automatique.
③ ENTRÉE — `<racine>` : la copie où la chaîne a tourné ; `<id_version>` : l'identifiant d'une fiche du registre de la
  racine (comparé après `norme` : espaces de bord ôtés, majuscules) ; `--juge-fait` : exiger aussi le témoin du juge ④.
  Lu : <racine>/donnees/cac40_strategies.csv (la dernière ligne de l'identifiant, n°83) ; la marque de la fiche
  (colonne CONTRATS.COLONNE_DE_LA_MARQUE_DE_MOULINETTE, forme « MOULINETTE (A-919) <STRATÉGIE> <ESSAI> », comparée
  après la même `norme`) ;
  <racine>/CHAINE_<STRATÉGIE>_<ESSAI>/JOURNAL_DE_LA_CHAINE.csv (colonnes etape, fichier, sha256, ecrit_le ; la
  dernière ligne d'une étape fait foi) et les fichiers qu'il nomme, relatifs à son dossier.
④ CONDITIONS D'ENTRÉE — —
⑤ SORTIE — UNE valeur, le code : 0 la fiche peut être jugée · 1 refus, motifs affichés · 2 le contrôle n'a pas pu
  tourner (fichier illisible, journal mal formé, fiche absente ou non marquée, fiche marquée sans chaîne — R-734).
⑥ TRAITEMENT — ① chaque étape exigée a un témoin · ② chaque fichier du journal est présent et à son empreinte ·
  ③ le fichier assemblé de ② porte exactement les versions de la combinatoire de ① · ④ les réglages gardés à ⓪
  portent la mention de validation · ⑤ la version est parmi les retenues du tri ③ · ⑥ l'empreinte des réglages de la
  fiche jugée (`JUGE_DES_STRATEGIES.empreinte_des_reglages`, la seule définition) est celle que JOUER a écrite pour
  cette version dans le fichier ② témoigné — rien n'est recalculé depuis la combinatoire ni la fiche mère ·
  ⑥bis LES CONDITIONS DE JEU (I2 du relecteur du 19-11-2026) : le NOM du barème sous lequel le juge chiffrerait
  (`JUGE_DES_STRATEGIES.bareme_des_verdicts`) est celui de la colonne `bareme` du fichier ②, et l'EMPREINTE DE SON
  CONTENU (`JOUER_LES_VERSIONS.empreinte_du_bareme`) celle de la colonne `empreinte_du_bareme` ; les cours que ② a joués
  (colonne `cours_joues`) ont encore, jusqu'à `fin_ecrite_dans_la_fiche`, l'empreinte que JOUER a écrite
  (`JOUER_LES_VERSIONS.empreinte_des_cours_jusqu_a`, la fonction qui l'a écrite) ; la PÉRIODE de la fiche est dans
  l'empreinte des réglages (les bornes, par `lecture_de_jeu`) · ⑥ter LA FAMILLE (A-777, C12 ; L-1, L-2 du RELU Cowork
  du 25-11-2026) : une version visée dont la stratégie est d'une famille déjà jouée sur 2000-2023 (même CODE de module
  de signal qu'une fiche de CONTRATS.FICHES_DEJA_VUES_SUR_LE_REGARD_UNIQUE, `famille_deja_jouee`) est refusée, sauf
  déclaration explicite au journal (`declarer_la_famille`) · ⑦ sous --juge-fait, le témoin ④.
⑦ UNITÉ — —
⑧ POURQUOI — A-919 et A-921 (décisions de Jean-Luc du 19-11-2026) ; superviseur R-759 du 19-11-2026 : la porte dans
  le juge, la marque sur la fiche, les réglages confrontés à ② ; superviseur R-759 du 19-11-2026, tour 3 : une seule
  désignation de la fiche visée (`fiche_du_registre`), la marque par `norme`, le barème et les cours confrontés.
⑨ CE QUI CLOCHE — ① LA MENTION « Jean-Luc le JJ-MM-AAAA » (colonne `valide_par` du tableau VARIABLES_DE_DECLINAISON,
  jugée par `DECLINER_LES_STRATEGIES.validation_valable`) NE PROUVE RIEN D'AUTRE QU'UNE LIGNE ÉCRITE : n'importe qui
  peut l'écrire. ② Le témoin prouve qu'un fichier n'a pas changé depuis son étape, pas qu'un programme l'a produit :
  un journal réécrit à la main avec les bonnes empreintes passe. ③ TROU ASSUMÉ (A-921) : une fiche fabriquée à la main
  SANS la marque n'est pas gardée ici — le juge la juge comme toute fiche. ④ La règle du choix de la version jugée
  n'est pas décidée (A-775) : ce programme vérifie seulement qu'elle est parmi les retenues. ⑤ La porte n'est appelée
  que par `JUGE_DES_STRATEGIES.main` : un programme qui importe le juge et appelle `jouer` ou `juger` lui-même la saute.
  ⑥ L'empreinte du module de signal est lue au jour du jugement ; un module changé entre ② et ④ fait refuser la fiche.
  ⑦ TROU (A-921) PRÉCISÉ : la marque est comparée après `norme` (casse, espaces de bord) ; une marque mal écrite à la
  main AUTREMENT — deux espaces intérieurs, une faute, « A-91 » — n'est pas une marque : la fiche est jugée comme une
  fiche non marquée, comme celle qui n'en porte pas (③). Aucune règle « ressemble à une marque » (superviseur R-759 du
  19-11-2026, ②). ⑧ LE BARÈME EST CONFRONTÉ PAR SON NOM ET PAR LE CONTENU DE SES LIGNES (courtage REEL 0.0015 →
  0.015 refusé, S20b) ; la liste des valeurs taxées (donnees/VALEURS_TTF.csv) n'y entre pas. ⑨ LE CODE DE programmes/MODULE_POSITIONS.py N'EST CONFRONTÉ À RIEN : l'empreinte des
  réglages porte le code du module de SIGNAL (`empreinte_d_un_module`), pas celui des positions (sorties, frais). ⑩ Le
  fichier de cours confronté est celui que ② a joué (`cours_joues`), pas celui que le juge lira : `--cours=<autre>`
  donné au juge n'est pas vu ici. ⑪ La période JOUÉE par ② (`periode_debut`, `periode_fin`, fin ramenée par JOUER) n'est
  pas recalculée : seules les bornes de la fiche le sont, par l'empreinte des réglages.
⑩ EFFET — Lit ; `temoigner` (appelée par l'enchaîneur) ajoute une ligne au journal.
⑪ TERMINAISON — Rend la main. [sort: oui — code, sous la ligne de commande]
"""
import csv
import hashlib
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

sys.dont_write_bytecode = True
JOURNAL = "JOURNAL_DE_LA_CHAINE.csv"
CHAMPS = ["etape", "fichier", "sha256", "ecrit_le"]
ORDRE = ["0-variables-validees", "0-proposition", "1-decliner", "2-assembler", "3-trier"]
# LA GARDE DE FAMILLE (A-777, C12 ; défauts L-1 et L-2 du RELU Cowork du 25-11-2026 sur c83732b53) : le témoin d'une
# déclaration explicite, et le fichier qui en porte le texte, relatif au dossier de la chaîne.
TEMOIN_DE_FAMILLE = "0-famille-declaree"
FICHIER_DE_FAMILLE = "famille_declaree.txt"
DECISION_FAMILLE = ("A-777 (Jean-Luc, 14-11-2026 15h55 : « D'abord une autre famille de stratégies, jamais jouée sur "
                    "2000-2023 […] et C5 attend ») et C12 (Jean-Luc, 25-11-2026 12h40, rapporté par le Chat "
                    "coordinateur : « la première vraie traversée se fait avec une famille de stratégies jamais jouée "
                    "sur 2000-2023, et C5 reste jugée en direct »)")


class Impossible(Exception):
    """Un contrôle n'a pas pu tourner (R-734), code 2. ①–⑪ — sans objet. [rend: rien] [sort: non]"""


def norme(ident):
    """Rend l'identifiant comparable.

    ① RÔLE — LA comparaison d'identifiants et de marques, une fois (superviseur R-759 du 19-11-2026, ③).
    ② CONTEXTE D'APPEL — partout où deux identifiants se comparent : `motifs`, `marque_de`, `fiche_du_registre`, et
      l'enchaîneur.
    ③ ENTRÉE — `ident` : un texte ou None. Exemple réel : « c5e10-obs-v1-e01-0001 » suivi d'un espace.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte, espaces de bord ôtés, en majuscules ; « » pour None.
    [rend: 1]
    ⑥ TRAITEMENT — `strip`, puis `upper`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — « c5e10-obs-v1-e01-0001 » avec un espace final échappait à l'ancienne porte (relecteur du 19-11-2026).
    ⑨ CE QUI CLOCHE — les espaces intérieurs ne sont pas ramenés : « MOULINETTE  (A-919) » (deux espaces) n'est pas la
      marque (trou A-921, ⑨ ③ du fichier).
    ⑩ EFFET — aucun.
    ⑪ TERMINAISON — rend la main.
    [sort: non]
    """
    return (ident or "").strip().upper()


def dossier(racine, sid, essai):
    """Rend le dossier de la chaîne.

    ① RÔLE — Dire, à un seul endroit, où vit la chaîne d'une stratégie et d'un essai.
    ② CONTEXTE D'APPEL — `motifs`, `porte_du_juge`, l'enchaîneur.
    ③ ENTRÉE — `racine`, `sid`, `essai` ; exemple réel : C5E10-OBS-V1, E01.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : `<racine>/CHAINE_<sid>_<essai>`.
    [rend: 1]
    ⑥ TRAITEMENT — jointure de chemins.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — un seul endroit dit où vit la chaîne (R-708 : deux définitions d'une même chose divergent).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — aucun.
    ⑪ TERMINAISON — rend la main.
    [sort: non]
    """
    return os.path.join(racine, "CHAINE_%s_%s" % (sid, essai))


def lire(chemin, champs=None):
    """Rend les lignes d'un CSV.

    ① RÔLE — Lire un fichier de la chaîne, ou dire que le contrôle n'a pas pu tourner.
    ② CONTEXTE D'APPEL — `temoins`, `motifs`, l'enchaîneur.
    ③ ENTRÉE — `chemin` ; `champs` : les colonnes exigées, ou None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE liste de dictionnaires.
    [rend: 1]
    ⑥ TRAITEMENT — `csv.DictReader` ; colonnes exigées absentes → Impossible.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — un fichier mal formé est un contrôle qui n'a pas pu tourner, jamais une trace Python (relecteur du
      19-11-2026, M1).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — lit.
    ⑪ TERMINAISON — rend la main ; lève Impossible si le fichier est illisible ou mal formé.
    [sort: non]
    """
    try:
        with open(chemin, encoding="utf-8-sig", newline="") as fh:
            lecteur = csv.DictReader(fh)
            lignes = list(lecteur)
            entete = lecteur.fieldnames or []
    except (OSError, UnicodeDecodeError, csv.Error) as e:
        raise Impossible("lecture impossible de %s : %s" % (chemin, e))
    if champs and [c for c in champs if c not in entete]:
        raise Impossible("%s mal formé : colonnes %s absentes (en-tête lu : %s)"
                         % (chemin, [c for c in champs if c not in entete], entete))
    return lignes


def sha(chemin):
    """Rend le sha256 d'un fichier, None s'il n'existe pas.

    ① RÔLE — L'empreinte d'un témoin.
    ② CONTEXTE D'APPEL — `temoigner`, `motifs`.
    ③ ENTRÉE — `chemin`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 64 caractères hexadécimaux, ou None.
    [rend: 1]
    ⑥ TRAITEMENT — lire les octets, hacher.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — le témoin dit qu'un fichier n'a pas changé depuis son étape (A-919).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — lit.
    ⑪ TERMINAISON — rend la main ; lève Impossible si le fichier est illisible.
    [sort: non]
    """
    if not os.path.lexists(chemin):
        return None
    try:
        with open(chemin, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError as e:
        raise Impossible("empreinte impossible de %s : %s" % (chemin, e))


def temoigner(ch, etape, fichier):
    """Ajoute au journal le témoin d'une étape.

    ① RÔLE — Consigner qu'une étape a réussi, avec l'empreinte de son fichier.
    ② CONTEXTE D'APPEL — l'enchaîneur, après chaque étape RÉUSSIE.
    ③ ENTRÉE — `ch` : le dossier de la chaîne ; `etape` : exemple réel « 2-tranche-3 » ; `fichier` : relatif à `ch`.
    ④ CONDITIONS D'ENTRÉE — le fichier existe.
    ⑤ SORTIE — aucune.
    [rend: rien]
    ⑥ TRAITEMENT — sha256 du fichier ; une ligne ajoutée au journal, l'en-tête écrit s'il est neuf.
    ⑦ UNITÉ — heure de Paris (`ecrit_le`).
    ⑧ POURQUOI — A-919.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — écrit le journal.
    ⑪ TERMINAISON — rend la main ; lève Impossible si le fichier n'existe pas.
    [sort: non]
    """
    j, h = os.path.join(ch, JOURNAL), sha(os.path.join(ch, fichier))
    if h is None:
        raise Impossible("témoin impossible : %s n'existe pas" % fichier)
    neuf = not os.path.exists(j)
    with open(j, "a", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=CHAMPS, lineterminator="\n")
        if neuf:
            w.writeheader()
        w.writerow({"etape": etape, "fichier": fichier, "sha256": h,
                    "ecrit_le": datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d %Hh%M:%S")})


def temoins(ch):
    """Rend {étape: (fichier, sha256)}, la dernière ligne d'une étape faisant foi.

    ① RÔLE — Lire le journal de la chaîne.
    ② CONTEXTE D'APPEL — `motifs`, l'enchaîneur.
    ③ ENTRÉE — `ch` : le dossier de la chaîne.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UN dictionnaire, vide sans journal.
    [rend: 1]
    ⑥ TRAITEMENT — `lire`, en-tête exigé (CHAMPS).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — M1 du relecteur du 19-11-2026 : un en-tête « etap » levait KeyError.
    ⑨ CE QUI CLOCHE — une étape relancée a deux lignes ; la dernière fait foi, les autres ne sont pas relues (M1 du
      relecteur du 19-11-2026 : deux « 4-juger-… »).
    ⑩ EFFET — lit.
    ⑪ TERMINAISON — rend la main, ou lève Impossible.
    [sort: non]
    """
    j = os.path.join(ch, JOURNAL)
    return {l["etape"]: (l["fichier"], l["sha256"]) for l in lire(j, CHAMPS)} if os.path.exists(j) else {}


def marque_de(fiche):
    """Rend (stratégie, essai) si la fiche porte la marque de moulinette, None sinon.

    ① RÔLE — Reconnaître une version à SA MARQUE, jamais à son nom (A-921).
    ② CONTEXTE D'APPEL — `porte_du_juge`.
    ③ ENTRÉE — `fiche` : une ligne du registre (dictionnaire).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur, None (fiche non marquée), ou DEUX : la stratégie et l'essai lus dans la marque.
    [rend: 1 ou 2]
    ⑥ TRAITEMENT — la case CONTRATS.COLONNE_DE_LA_MARQUE_DE_MOULINETTE et CONTRATS.MARQUE_DE_MOULINETTE passent par
      `norme` (la même que les identifiants : espaces de bord, casse) ; si la case commence par la marque, le reste doit
      être exactement deux mots.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — A-921 ; I1 du relecteur du 19-11-2026 : « moulinette (A-919) C5E10-OBS-V1 E01 » était rangée parmi les
      fiches non marquées, et jugée.
    ⑨ CE QUI CLOCHE — voir ⑨ ③ du fichier : une marque mal écrite à la main autrement qu'en casse ou en espaces de bord
      n'est pas une marque.
    ⑩ EFFET — aucun.
    ⑪ TERMINAISON — rend la main, ou lève Impossible sur une marque mal formée.
    [sort: non]
    """
    import CONTRATS_DES_FICHIERS as C          # la marque vit au contrat, une fois (R-708)
    case, marque = norme(fiche.get(C.COLONNE_DE_LA_MARQUE_DE_MOULINETTE)), norme(C.MARQUE_DE_MOULINETTE)
    if not case.startswith(marque):
        return None
    mots = case[len(marque):].split()
    if len(mots) != 2:
        raise Impossible("marque de moulinette mal formée sur %r : %r (attendu « %s <STRATÉGIE> <ESSAI> »)"
                         % (fiche.get("id"), case, C.MARQUE_DE_MOULINETTE))
    return mots[0], mots[1]


def famille_deja_jouee(racine, sid, J=None, version=None, module=None):
    """Rend la liste des motifs qui disent la famille de `sid` déjà jouée sur 2000-2023 (vide : famille neuve).

    ① RÔLE — LA définition de « même famille », une fois, pour la garde de ④ (`garde_de_famille`) et pour le lanceur
      (programmes/LANCER_UNE_STRATEGIE.py, qui la lit avant ⓪).
    ② CONTEXTE D'APPEL — `garde_de_famille` (avec la version visée, et le module de la fiche jugée quand c'est la
      porte du juge) ; `LANCER_UNE_STRATEGIE.executer`, avant ⓪ (sans eux).
    ③ ENTRÉE — `racine` : la copie ; `sid` : exemple réel C5E10-OBS-V1 (refusée : même code que C5E10-QA-V1),
      IND-001-RETEST (passe) ; `J` : le module du juge, ou None (importé ici) ; `version` : la version visée par
      l'étape juger (exemple : FAUX-LANCEUR-V1-E01-0007), ou None — absente du registre permise (l'enchaîneur garde AVANT d'ajouter
      la fiche) ; `module` : le module_signal de la fiche que le juge va lire (`porte_du_juge`), ou None. Lus : le
      registre de la racine
      (`fiche_du_registre`, n°83 : la dernière ligne d'un identifiant fait foi), colonne module_signal ; le CODE de
      chaque module nommé, sous la racine ; CONTRATS.FICHES_DEJA_VUES_SUR_LE_REGARD_UNIQUE (« la famille de ces
      fiches a déjà été jouée sur 2000-2023 (A-777) », texte du contrat).
    ④ CONDITIONS D'ENTRÉE — `sid` est au registre avec un module_signal lisible ; chaque fiche déjà vue présente au
      registre aussi.
    ⑤ SORTIE — UNE liste de textes, un par fiche déjà vue de la même famille.
    [rend: 1]
    ⑥ TRAITEMENT — ① « mes » empreintes du CODE : celle du module de `sid`, celle du module de `version` si elle est
      au registre, celle de `module` s'il est donné (`J.lire_module_du_jour`, qui passe par `J.empreinte_d_un_module` :
      l'arbre syntaxique privé de ses textes explicatifs ; la seule mesure, R-708) ; module_signal vide, fichier absent
      ou illisible → Impossible (on ne sait pas, R-734) · ② pour chaque fiche déjà vue : `sid` ou `version` elle-même
      (après `norme`), ou une empreinte de code parmi les miennes → un motif qui la nomme.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — DECISION_FAMILLE. L-1 du RELU Cowork du 25-11-2026 : l'ancienne garde comparait le TEXTE du chemin ;
      « ./programmes/… », « programmes/./… » ou une copie du module C5 sous un autre nom passaient sans déclaration.
      Critère : si je renomme le module, ce contrôle ne change pas d'avis — il mesure le code, pas le nom. L-6 du RELU
      Cowork du 25-11-2026 (14h20) : seule la ligne ACTUELLE de `sid` était lue ; une ligne de version sur le module C5
      (la fiche que le juge lirait) passait. Superviseur R-759 du 25-11-2026 (R2 « de fond pour la version visée », Q4
      « passer aussi fiche["module_signal"] ») : la version visée et le module de la fiche jugée comptent.
    ⑨ CE QUI CLOCHE — ① LA DÉFINITION DE LA FAMILLE (« même code de module de signal » qu'une fiche déjà vue) est
      celle de l'écrivain, NON DÉCIDÉE par Jean-Luc (L-5 du même RELU) ; une copie du module C5 dont UNE instruction
      change (un seuil, un nom de variable) n'a plus la même empreinte et passe ; un module qui CHARGE le module C5 par
      son chemin a sa propre empreinte et passe (même trou que N7, `J.empreinte_d_un_module` ⑨ ①). ② Seules les
      fiches de FICHES_DEJA_VUES_SUR_LE_REGARD_UNIQUE sont vues (aujourd'hui une, C5E10-QA-V1) ; une famille jouée sur
      2000-2023 qui n'y est pas inscrite passe (L-5). ③ Le code est lu AU JOUR sous la racine, pas à la date de la
      fiche déjà vue. ④ OUVERT — DÉCISION DE JEAN-LUC DEMANDÉE LE 25-11-2026 (L-11 du RELU Cowork de 14h20) : la
      RÉFÉRENCE de la famille est le module de la DERNIÈRE ligne de la fiche déjà vue, lue dans le registre DE LA
      COPIE ; UNE ligne C5E10-QA-V1 ajoutée qui nomme un autre module fait juger C5 sans déclaration (cas A3). Le
      superviseur R-759 du 25-11-2026 a refusé la réparation par l'historique (« arrêter et simplifier ») ; la forme
      proposée à Jean-Luc : un ensemble d'empreintes du CODE de C5 FIGÉ au contrat. TROU VOISIN, MÊME DÉCISION : une
      fiche déjà vue ABSENTE du registre de la racine n'est pas comparée (sa colonne
      module_signal n'existe pas) ; une copie dont on a retiré C5E10-QA-V1 du registre laisse passer C5. Choisi
      plutôt que « contrôle impossible » parce que les racines fabriquées des épreuves (exemple réel :
      tests/EPREUVES_PAR_PROPRIETES_DE_LA_CHAINE_Ven_20-11-2026.py, registre réduit à ses fiches PROP-) n'en portent
      pas ; même nature que la limite acceptée par Jean-Luc pour l'essai sans regard (A-867 : une copie modifiée
      exprès n'est pas gardée). Une fiche déjà vue PRÉSENTE dont le module est illisible → Impossible.
    ⑩ EFFET — lit le registre et des modules.
    ⑪ TERMINAISON — rend la main, ou lève Impossible.
    [sort: non]
    """
    import CONTRATS_DES_FICHIERS as C
    if J is None:
        import JUGE_DES_STRATEGIES as J
    lire_module = J.lire_module_du_jour(racine)

    def module_de(ident):
        """Rend (chemin, empreinte du code) du module de signal de `ident`.

        ① RÔLE — Lire le module de signal d'une fiche du registre.
        ② CONTEXTE D'APPEL — `famille_deja_jouee`, pour `sid` puis pour chaque fiche déjà vue présente au registre.
        ③ ENTRÉE — `ident` : un identifiant du registre de la racine ; exemple réel C5E10-QA-V1.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — DEUX valeurs : le chemin écrit au registre, l'empreinte du code (16 hexadécimaux).
        [rend: 2]
        ⑥ TRAITEMENT — `fiche_du_registre`, colonne module_signal, puis `lire_module`.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — voir ⑧ de `famille_deja_jouee` : le code, pas le nom.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — lit le registre et le module.
        ⑪ TERMINAISON — rend la main, ou lève Impossible (vide, introuvable, illisible).
        [sort: non]
        """
        chemin = (fiche_du_registre(racine, ident).get("module_signal") or "").strip()
        if not chemin:
            raise Impossible("famille de %s inconnue : module_signal vide au registre" % ident)
        try:
            emp = lire_module(chemin)
        except (ValueError, ImportError, OSError) as e:     # module non analysable, emp.py introuvable : on ne sait pas
            raise Impossible("famille de %s inconnue : module %s illisible (%s: %s)" % (ident, chemin,
                                                                                    type(e).__name__, e))
        if emp is None:
            raise Impossible("famille de %s inconnue : module %s introuvable sous %s" % (ident, chemin, racine))
        return chemin, emp

    chemin, emp = module_de(sid)
    mien = {emp: chemin}
    if version and fiche_du_registre(racine, version, absente_permise=True) is not None:
        chemin, emp = module_de(version)
        mien.setdefault(emp, chemin)
    if module is not None:
        chemin = module.strip()
        try:
            emp = lire_module(chemin) if chemin else None
        except (ValueError, ImportError, OSError) as e:
            raise Impossible("famille de la fiche jugée inconnue : module %s illisible (%s: %s)" % (chemin,
                                                                                               type(e).__name__, e))
        if emp is None:
            raise Impossible("famille de la fiche jugée inconnue : module %r vide ou introuvable sous %s" % (chemin,
                                                                                                         racine))
        mien.setdefault(emp, chemin)
    moi = {norme(sid)} | ({norme(version)} if version else set())
    m = []
    for f in sorted(C.FICHES_DEJA_VUES_SUR_LE_REGARD_UNIQUE):
        if norme(f) in moi:
            m.append("%s : c'est la fiche elle-même" % f)
        elif fiche_du_registre(racine, f, absente_permise=True) is None:
            continue        # absente du registre de la racine : rien à comparer (⑨ ④)
        elif module_de(f)[1] in mien:
            ref = module_de(f)
            m.append("%s : même code de module de signal (%s et %s, empreinte %s)" % (f, ref[0], mien[ref[1]], ref[1]))
    return m


def declarer_la_famille(ch, texte):
    """Écrit au journal de la chaîne la déclaration explicite qui lève le refus d'une famille déjà jouée.

    ① RÔLE — Donner à la déclaration une place que la garde de ④ lit, quel que soit le chemin vers ④ (L-2).
    ② CONTEXTE D'APPEL — `ENCHAINER_LA_MOULINETTE.py … declarer "<texte>"` (le lanceur passe par là).
    ③ ENTRÉE — `ch` : le dossier de la chaîne ; `texte` : qui, quand, les mots de la décision. Exemple : « Jean-Luc,
      25-11-2026 14h02 : « oui, rejouer C5 sur les 30 % » ».
    ④ CONDITIONS D'ENTRÉE — `texte` non vide après `strip`.
    ⑤ SORTIE — UNE valeur : vrai si la déclaration est écrite, faux si une déclaration était déjà au journal.
    [rend: 1]
    ⑥ TRAITEMENT — déjà témoignée → rien (la première fait foi) ; sinon `<ch>/famille_declaree.txt` écrit (le texte,
      une ligne), puis `temoigner` sous TEMOIN_DE_FAMILLE : son empreinte est ensuite vérifiée par `motifs` comme
      celle de tout témoin.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — consigne du Chat coordinateur du 25-11-2026 : « un refus d'une famille déjà jouée sur 2000-2023 sauf
      déclaration explicite, la décision citée ».
    ⑨ CE QUI CLOCHE — la déclaration n'est qu'un texte : rien ne vérifie que Jean-Luc l'a dite (même limite que la
      mention de validation, ⑨ ① du fichier).
    ⑩ EFFET — écrit un fichier et une ligne au journal.
    ⑪ TERMINAISON — rend la main ; lève ValueError (texte vide) ou Impossible.
    [sort: non]
    """
    texte = (texte or "").strip()
    if not texte:
        raise ValueError("déclaration vide : il faut qui, quand et les mots de la décision")
    if TEMOIN_DE_FAMILLE in temoins(ch):
        return False
    os.makedirs(ch, exist_ok=True)
    with open(os.path.join(ch, FICHIER_DE_FAMILLE), "w", encoding="utf-8") as fh:
        fh.write(texte + "\n")
    temoigner(ch, TEMOIN_DE_FAMILLE, FICHIER_DE_FAMILLE)
    return True


def garde_de_famille(racine, sid, essai, J=None, version=None, module=None):
    """Rend [] si ④ est permis pour la famille de `sid`, sinon UN motif de refus.

    ① RÔLE — La garde d'A-777 et de C12, à la porte de ④, là où l'ordre de la chaîne est déjà gardé.
    ② CONTEXTE D'APPEL — `motifs`, quand une version est visée sur une chaîne complète : donc l'enchaîneur à l'étape
      juger ET la porte du juge (`porte_du_juge`), quel que soit celui qui les lance (L-2).
    ③ ENTRÉE — `racine`, `sid`, `essai` ; `J` : le module du juge, ou None ; `version` : la version visée par l'étape
      juger, ou None ; `module` : le module_signal de la fiche jugée (porte du juge), ou None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE liste : vide, ou un texte « REFUS ④ … », la décision citée.
    [rend: 1]
    ⑥ TRAITEMENT — une déclaration au journal (TEMOIN_DE_FAMILLE) → [] sans rien lire d'autre ; sinon
      `famille_deja_jouee`, avec la version visée et le module de la fiche jugée (L-6) ; un motif → le refus.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — L-2 du RELU Cowork du 25-11-2026 : la garde ne vivait que dans le lanceur ; l'enchaîneur appelé à la
      main jugeait une fiche de famille C5 sans déclaration, code 0.
    ⑨ CE QUI CLOCHE — ① voir ⑨ de `famille_deja_jouee` · ② une fiche NON MARQUÉE jugée directement par le juge ne
      passe pas par ici (trou assumé d'A-921, ⑨ ③ du fichier) · ③ un journal réécrit à la main avec une déclaration
      passe (⑨ ② du fichier).
    ⑩ EFFET — lit.
    ⑪ TERMINAISON — rend la main, ou lève Impossible.
    [sort: non]
    """
    if TEMOIN_DE_FAMILLE in temoins(dossier(racine, sid, essai)):
        return []
    deja = famille_deja_jouee(racine, sid, J, version, module)
    if not deja:
        return []
    return ["REFUS ④ : la famille de %s est déjà jouée sur 2000-2023 (%s) — décision %s ; pour juger quand même, une "
            "déclaration explicite au journal de la chaîne : ENCHAINER_LA_MOULINETTE.py <racine> %s %s declarer "
            "\"<qui, quand, mots de la décision>\"" % (sid, " · ".join(deja), DECISION_FAMILLE, sid, essai)]


def decoupage_mele(ch, n):
    """Rend la liste des tranches déjà témoignées qui ne sont pas la tranche de même rang du découpage en `n`.

    ① RÔLE — Refuser qu'une chaîne mêle des tranches de deux découpages (L-3), d'après ce que le journal PROUVE.
    ② CONTEXTE D'APPEL — `ENCHAINER_LA_MOULINETTE.main` avant « jouer k n » ; `LANCER_UNE_STRATEGIE.executer` avant
      toute étape.
    ③ ENTRÉE — `ch` : le dossier de la chaîne ; `n` : le nombre de tranches voulu. Exemple réel (cas de L-3) :
      sept versions, tranches 0, 1, 2 jouées en 3, n = 5 → trois motifs.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE liste de textes (vide : aucune tranche, ou toutes conformes au découpage en `n`).
    [rend: 1]
    ⑥ TRAITEMENT — pour chaque témoin « 2-tranche-<k> » : k ≥ n → motif ; sinon les id_version de son fichier
      (ensemble) comparés à ceux de `JOUER_LES_VERSIONS.tranche(combinatoire, k, n)` — LE découpage, une fois (R-708) —
      sur la combinatoire témoignée à ① ; différents → motif. Une tranche témoignée sans combinatoire témoignée →
      motif.
    ⑦ UNITÉ — tranches, versions.
    ⑧ POURQUOI — L-3 du RELU Cowork du 25-11-2026 : le découpage n'était comparé qu'au fichier d'état du lanceur ;
      une chaîne commencée à la main (ou un état effacé) laissait jouer `jouer 3 5` après `jouer 0..2 3`.
    ⑨ CE QUI CLOCHE — deux découpages qui donnent les MÊMES tranches déjà jouées (sept versions en 4 ou en 5 : tranches
      0 à 3 identiques) sont acceptés : c'est juste, la partition finale reste exacte.
    ⑩ EFFET — lit.
    ⑪ TERMINAISON — rend la main, ou lève Impossible (fichier illisible).
    [sort: non]
    """
    t = temoins(ch)
    pref = "2-tranche-"
    faites = sorted((int(e[len(pref):]), f) for e, (f, _h) in t.items() if e.startswith(pref) and e[len(pref):].isdigit())
    if not faites:
        return []
    if "1-decliner" not in t:
        return ["tranches témoignées sans combinatoire témoignée à ① : découpage invérifiable"]
    import JOUER_LES_VERSIONS as JOUER
    comb = [norme(r["id_version"]) for r in lire(os.path.join(ch, t["1-decliner"][0]), ["id_version"])]
    m = []
    for k, f in faites:
        attendu = set(JOUER.tranche(comb, k, n)) if k < n else None
        vu = {norme(r["id_version"]) for r in lire(os.path.join(ch, f), ["id_version"])}
        if vu != attendu:
            m.append("tranche %d déjà jouée (%d versions) : ce n'est pas la tranche %d d'un découpage en %d%s" % (
                k, len(vu), k, n, "" if attendu is None else " (%d versions attendues)" % len(attendu)))
    return m


def motifs(racine, sid, essai, exigees, version=None, juge_fait=False, empreinte=None, bareme=None, module=None):
    """Rend la liste des motifs de refus (vide : tout tient).

    ① RÔLE — LA GARDE.
    ② CONTEXTE D'APPEL — `porte_du_juge`, l'enchaîneur (avant chaque étape).
    ③ ENTRÉE — `racine`, `sid`, `essai` ; `exigees` : combien d'étapes d'ORDRE doivent avoir leur témoin ; `version` :
      la version visée, ou None ; `juge_fait` ; `empreinte` : celle des réglages de la fiche jugée, ou None
      (l'enchaîneur, avant d'ajouter la fiche) ; `bareme` : le couple (nom, empreinte du contenu) du barème sous lequel le juge chiffrerait, ou None ;
      `module` : le module_signal de la fiche jugée (porte du juge, Q4 du superviseur R-759 du 25-11-2026), ou None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE liste de textes.
    [rend: 1]
    ⑥ TRAITEMENT — voir ⑥ du fichier ; puis, une version visée sur une chaîne complète et AUCUN autre motif, la garde
      de famille (`garde_de_famille`, ⑥ter du fichier). Après les autres : un refus déjà acquis n'a pas besoin d'elle,
      et un module illisible (Impossible) ne masque pas un refus connu.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — A-919.
    ⑨ CE QUI CLOCHE — voir ⑨ du fichier.
    ⑩ EFFET — lit.
    ⑪ TERMINAISON — rend la main, ou lève Impossible.
    [sort: non]
    """
    import DECLINER_LES_STRATEGIES as DECLINER     # la règle de validation vit là (R-708) ; importée au besoin
    ch = dossier(racine, sid, essai)
    t, m = temoins(ch), []
    m += ["étape %s absente du journal %s : elle n'a pas été faite" % (e, os.path.join(ch, JOURNAL))
          for e in ORDRE[:exigees] if e not in t]
    for e, (f, h) in sorted(t.items()):
        vu = sha(os.path.join(ch, f))
        if vu is None:
            m.append("étape %s : le fichier %s a disparu" % (e, f))
        elif vu != h:
            m.append("étape %s : le fichier %s a changé depuis son témoin (%s… attendu, %s… lu)" % (e, f, h[:12], vu[:12]))
    if exigees >= 4 and "1-decliner" in t and "2-assembler" in t and not m:
        ids = [norme(r["id_version"]) for r in lire(os.path.join(ch, t["1-decliner"][0]), ["id_version"])]
        jouees = [norme(r["id_version"]) for r in lire(os.path.join(ch, t["2-assembler"][0]), ["id_version"])]
        if ids != jouees:
            m.append("② ne porte pas les versions de ① : %d sans résultat, %d en trop"
                     % (len(set(ids) - set(jouees)), len(set(jouees) - set(ids))))
    if exigees >= len(ORDRE) and not m:
        for l in lire(os.path.join(ch, t["0-variables-validees"][0])):
            if l.get("jouable") == "OUI" and l.get("parametre") in DECLINER.OBLIGATOIRES and \
                    not DECLINER.validation_valable(l):
                m.append("réglage %s NON VALIDÉ PAR JEAN-LUC : valide_par = %r (attendu « Jean-Luc le JJ-MM-AAAA ») —"
                         " une mention écrite, rien de plus" % (l.get("parametre"), l.get("valide_par")))
        retenues = {norme(r["id_version"]) for r in lire(os.path.join(ch, t["3-trier"][0]), ["id_version"])}
        if version is not None and norme(version) not in retenues:
            m.append("la version %r n'est pas parmi les %d retenues par le tri ③ — la règle du choix n'est pas décidée"
                     " (A-775)" % (version, len(retenues)))
        if version is not None and empreinte is not None:
            jouee = [r for r in lire(os.path.join(ch, t["2-assembler"][0]),
                                     ["id_version", "empreinte_des_reglages", "bareme", "empreinte_du_bareme",
                                      "cours_joues", "fin_ecrite_dans_la_fiche", "empreinte_des_cours"])
                     if norme(r["id_version"]) == norme(version)]
            if len(jouee) != 1:
                m.append("la version %r est %d fois dans le fichier ② : ses réglages joués sont introuvables"
                         % (version, len(jouee)))
            else:
                j = jouee[0]
                if j["empreinte_des_reglages"] != empreinte:
                    m.append("les réglages de la fiche %r ne sont pas ceux que ② a joués : empreinte des réglages %s, ②"
                             " a joué %s (JUGE_DES_STRATEGIES.empreinte_des_reglages)"
                             % (version, empreinte, j["empreinte_des_reglages"]))
                # LES CONDITIONS DE JEU (I2 du relecteur du 19-11-2026 ; superviseur R-759, ③) : le barème, par son NOM
                # et par l'EMPREINTE DE SON CONTENU, et les cours que ② a joués — chacun par la fonction de JOUER qui a
                # écrit son empreinte (R-708).
                if bareme is not None and j["bareme"] != bareme[0]:
                    m.append("le barème du juge n'est pas celui que ② a joué : le juge chiffrerait sous %r, ② a joué "
                             "sous %r (colonne bareme du fichier ②)" % (bareme[0], j["bareme"]))
                elif bareme is not None and j["empreinte_du_bareme"] != bareme[1]:
                    m.append("le contenu du barème %r a changé depuis ② : empreinte %s aujourd'hui, ② a écrit %s "
                             "(JOUER_LES_VERSIONS.empreinte_du_bareme)" % (bareme[0], bareme[1], j["empreinte_du_bareme"]))
                import JOUER_LES_VERSIONS as JOUER
                vu = JOUER.empreinte_des_cours_jusqu_a(os.path.join(racine, j["cours_joues"]),
                                                       j["fin_ecrite_dans_la_fiche"])
                if vu != j["empreinte_des_cours"]:
                    m.append("les cours que ② a joués ont changé : %s jusqu'au %s a pour empreinte %s, ② a écrit %s "
                             "(JOUER_LES_VERSIONS.empreinte_des_cours_jusqu_a)"
                             % (j["cours_joues"], j["fin_ecrite_dans_la_fiche"], vu, j["empreinte_des_cours"]))
    if exigees >= len(ORDRE) and version is not None and not m:
        m += garde_de_famille(racine, sid, essai, version=version, module=module)
    if juge_fait and not any(norme(e) == norme("4-juger-%s" % version) for e in t):
        m.append("témoin du juge ④ absent pour %s : le juge n'a pas tourné, ou a échoué" % version)
    return m


def porte_du_juge(racine, fiche, juge_fait=False, J=None, mod_pos=None):
    """Rend None si la fiche ne porte pas la marque de moulinette, sinon la liste des motifs de refus.

    ① RÔLE — La porte que le juge appelle.
    ② CONTEXTE D'APPEL — `JUGE_DES_STRATEGIES.main`, avant de juger ; `main` ci-dessous.
    ③ ENTRÉE — `racine` ; `fiche` : la ligne du registre qui sera jugée ; `juge_fait` ; `J` : le module du juge (le
      juge se passe lui-même ; None : importé) ; `mod_pos` : le module de positions que le juge a chargé (None : chargé
      ici comme le juge le charge, `J.trouver` puis `J.charger_module`).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : None, ou une liste de textes.
    [rend: 1]
    ⑥ TRAITEMENT — `marque_de` → chaîne trouvable, sinon Impossible → empreinte des réglages de la fiche
      (`J.empreinte_des_reglages`, module de signal lu au jour sous `racine`) et barème du juge : son nom
      (`J.bareme_des_verdicts(None, mod_pos)`) et l'empreinte de son contenu (`JOUER_LES_VERSIONS.empreinte_du_bareme`,
      lue par ce même module) → `motifs` sur toute la chaîne, avec le module_signal de la fiche (la garde de famille
      compare AUSSI ce module, Q4 du superviseur R-759 du 25-11-2026 ; vide → Impossible) → puis (depuis le 19-11-2026, A-923) les refus du
      CONTRAT DE STRATÉGIE (`CONTRATS_DES_FICHIERS.manques_du_contrat`, avec le juge et le module de positions de
      l'appelant), chacun préfixé « contrat de stratégie (A-923) — <case> : ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — A-921 ; superviseur R-759 du 19-11-2026 (②, ⑤). Le contrat : A-923 et A-925 (décision de Jean-Luc
      du 19-11-2026 à 19h23, « écrire le contrat » ; consigne du Chat : le brancher à l'entrée, PREPARER ⓪ et ici).
    ⑨ CE QUI CLOCHE — voir ⑨ ③ ⑤ ⑥ du fichier. Le contrat ne s'applique qu'aux fiches MARQUÉES : une fiche non
      marquée passe la porte 0 du juge seule (trou assumé d'A-921) ; ses avis (`avis_du_contrat`) ne sont pas rendus ici.
    ⑩ EFFET — lit ; le contrat charge le module de signal de la fiche (déjà chargé par le juge à sa porte 0).
    ⑪ TERMINAISON — rend la main, ou lève Impossible — TOUTE exception est convertie ici, à la frontière (superviseur
      R-759 du 19-11-2026, ⑤), `ContratImpossible` du contrat comprise.
    [sort: non]
    """
    try:
        quoi = marque_de(fiche)
        if quoi is None:
            return None
        sid, essai = quoi
        if not os.path.exists(os.path.join(dossier(racine, sid, essai), JOURNAL)):
            raise Impossible("la fiche %r porte la marque de moulinette %s %s, mais aucune chaîne n'est trouvée (%s "
                             "absent)" % (fiche.get("id"), sid, essai, os.path.join(dossier(racine, sid, essai), JOURNAL)))
        if J is None:
            import JUGE_DES_STRATEGIES as J
        propre = {k: v for k, v in fiche.items() if not str(k).startswith("_")}   # sans les ajouts du juge
        emp = J.empreinte_des_reglages(propre, J.lire_module_du_jour(racine))[0]
        if mod_pos is None:
            mod_pos = J.charger_module(J.trouver(racine, "MODULE_POSITIONS.py"), "pos")
        import JOUER_LES_VERSIONS as JOUER
        nom = J.bareme_des_verdicts(None, mod_pos)
        # LE CONTRAT DE STRATÉGIE À LA PORTE DU JUGE (A-923, A-925 du 19-11-2026) : chaque case refusée, nommée.
        import CONTRATS_DES_FICHIERS as C
        contrat = ["contrat de stratégie (A-923) — " + r for r in C.manques_du_contrat(propre, racine, J=J, mod_pos=mod_pos)]
        return motifs(racine, sid, essai, len(ORDRE), fiche.get("id"), juge_fait, emp,
                      module=fiche.get("module_signal") or "", bareme=(nom, JOUER.empreinte_du_bareme(mod_pos, nom))) + contrat
    except Impossible:
        raise
    except Exception as e:      # noqa: BLE001 — la frontière : rien ne sort d'ici en trace Python (R-734)
        raise Impossible("%s: %s" % (type(e).__name__, e))


def fiche_du_registre(racine, ident, fiches=None, absente_permise=False):
    """Rend LA fiche du registre de la racine dont l'identifiant vaut `ident` après `norme`.

    ① RÔLE — Désigner LA fiche visée, une seule définition : le juge l'appelle aussi (B1 du relecteur du 19-11-2026 ;
      superviseur R-759, ①).
    ② CONTEXTE D'APPEL — `main` ; `JUGE_DES_STRATEGIES.main`, quand une fiche est visée.
    ③ ENTRÉE — `racine`, `ident` ; `fiches` : le registre déjà lu ({identifiant: fiche}, celui de
      CONTRATS.fiches_du_registre), ou None : lu ici sous `racine` ; `absente_permise` : vrai, aucune fiche rend None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la fiche (dictionnaire), ou None (aucune, sous `absente_permise`).
    [rend: 1]
    ⑥ TRAITEMENT — CONTRATS.fiches_du_registre (n°83 : la dernière ligne d'un identifiant fait foi), puis les
      identifiants comparés par `norme`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — B1 du relecteur du 19-11-2026 : « C5E10-OBS-V1-E01-0001 » et le même suivi d'un espace sont deux
      identifiants au registre ; le juge, qui avait son propre filtre, jugeait LES DEUX, la fiche marquée refusée
      ailleurs et son jumeau non marqué à tp 9.5.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — lit.
    ⑪ TERMINAISON — rend la main ; lève Impossible si plusieurs, ou aucune hors `absente_permise`.
    [sort: non]
    """
    import CONTRATS_DES_FICHIERS as C
    try:
        if fiches is None:
            fiches = C.fiches_du_registre(os.path.join(racine, C.REGISTRE_DES_STRATEGIES))
    except Exception as e:      # noqa: BLE001
        raise Impossible("registre illisible : %s: %s" % (type(e).__name__, e))
    trouvees = [f for i, f in fiches.items() if norme(i) == norme(ident)]
    if not trouvees and absente_permise:
        return None
    if len(trouvees) != 1:
        raise Impossible("%d fiche(s) %r au registre de %s (attendu une)" % (len(trouvees), ident, racine))
    return trouvees[0]


def main(argv):
    """Rend le code de sortie de la ligne de commande.

    ① RÔLE — Lire, garder, dire.
    ② CONTEXTE D'APPEL — `__main__`.
    ③ ENTRÉE — `argv`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2 (voir ⑤ du fichier).
    [rend: 1]
    ⑥ TRAITEMENT — `fiche_du_registre`, `porte_du_juge`, affichage.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — affiche.
    ⑪ TERMINAISON — rend la main ; c'est `__main__` qui passe le code à `sys.exit`.
    [sort: non]
    """
    args = [a for a in argv[1:] if a != "--juge-fait"]
    if len(args) != 2 or len(argv) - 1 - len(args) > 1 or any(a.startswith("--") for a in args):
        print(__doc__.split("① RÔLE")[0])
        return 2
    racine = os.path.abspath(args[0])
    try:
        m = porte_du_juge(racine, fiche_du_registre(racine, args[1]), "--juge-fait" in argv)
    except Impossible as e:
        print("CONTRÔLE IMPOSSIBLE (R-734) : %s" % e)
        return 2
    if m is None:
        print("CONTRÔLE IMPOSSIBLE : la fiche %r ne porte pas la marque de moulinette : ce n'est pas une version" % args[1])
        return 2
    print("CHAÎNE %s : %s" % (args[1], "REFUS\n  " + "\n  ".join(m) if m else "complète, témoins intacts"))
    return 1 if m else 0


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.exit(main(sys.argv))
