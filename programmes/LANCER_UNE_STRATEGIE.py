#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LANCER_UNE_STRATEGIE.py — Mer 25-11-2026 (Paris). EN ESSAI · outil. Simulation uniquement : aucun ordre réel.

LE SENS EN TÊTE. Le LANCEUR UNIQUE (A-965, décision de Jean-Luc du 21-11-2026 à 14h43, plan V8, rail ③) : UNE commande
prend une fiche de stratégie et un essai, et enchaîne les étapes de la moulinette (A-541) — ⓪ PREPARER · ① DECLINER ·
② JOUER (par tranches, puis assemblées, sur la partie de réglage, les 70 %) · ③ TRIER · ④ le JUGE (qui coupe lui-même
la période de la fiche en 70/30 et juge sur les 30 % — lu dans le code du juge et de JOUER, non éprouvé ici) — en appelant, étape après étape, l'enchaîneur
programmes/ENCHAINER_LA_MOULINETTE.py, qui garde l'ordre (A-919) et écrit le témoin de chaque étape. Le lanceur ne
calcule rien et ne lance aucun programme de la moulinette lui-même (R-708 : deux implémentations d'une même chose
divergent toujours) ; il ajoute quatre choses : ① il reprend où la chaîne s'est arrêtée (une étape témoignée n'est pas
relancée) ; ② il S'ARRÊTE PROPREMENT sur la seule décision qui revient à Jean-Luc en cours de route : la validation
des réglages ⓪ (mention « Jean-Luc le JJ-MM-AAAA » de la colonne valide_par) ; ③ AVANT ⓪, il REFUSE une famille déjà
jouée sur 2000-2023, sauf déclaration explicite, qu'il écrit alors au journal de la chaîne par l'enchaîneur (étape
« declarer ») ; LA GARDE ELLE-MÊME VIT À LA PORTE DE ④ (VERIFIER_LA_CHAINE.garde_de_famille, appelée par `motifs` pour
l'enchaîneur ET pour la porte du juge) : le lanceur ne fait que la lire plus tôt, pour ne pas calculer ② pour rien ;
④ il écrit son avancement, après chaque étape, dans un fichier d'état lisible par un autre programme.
LES DÉCISIONS QUI LE FONDENT. A-777 (Jean-Luc, Sam 14-11-2026 à 15h55, « 3 » à : « D'abord une autre famille de
stratégies, jamais jouée sur 2000-2023, par exemple IND-001-RETEST. Preuve propre tout de suite, et C5 attend. »).
C12 TRANCHÉ (Jean-Luc, Mer 25-11-2026 à 12h40, rapporté par le Chat coordinateur, PAS ENCORE CONSIGNÉ AU BACKLOG au
moment de l'écriture) : « la première vraie traversée se fait avec une famille de stratégies jamais jouée sur
2000-2023, et C5 reste jugée en direct » ; les années de jugement sont celles de la méthode 70/30 pour une famille
neuve. Versions jugées : TOUTES celles que ③ retient (méthode de Jean-Luc du 14-11-2026 14h39, consignée en
substance à A-775 : « rejouer TOUTES les sélectionnées sur les 30 % ») ; les seuils de ③ restent ceux de TRIER_LES_VARIANTES (A-775, critères EN COURS).
② SUR GITHUB : le relais des demandes (.github/workflows/demande_de_serie.yml du dépôt public, fabriqué par
programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, table CIRCUITS_DU_RELAIS) ne sait pas aujourd'hui lancer l'étape « jouer » :
le lanceur le LIT dans cette table, et joue alors les tranches EN LOCAL, l'une après l'autre, en le disant.

USAGE
    python3 -B programmes/LANCER_UNE_STRATEGIE.py <racine> <STRATÉGIE> <ESSAI> [--tranches=N]
        [--famille-deja-jouee-declaree=<qui, quand, mots de la décision>]
    exemple : python3 -B programmes/LANCER_UNE_STRATEGIE.py /dev/shm/x/depot IND-001-RETEST E01 --tranches=5

① RÔLE — Enchaîner ⓪ → ① → ② → ③ → ④ d'une stratégie sans intervention, et s'arrêter sur les décisions de Jean-Luc.
② CONTEXTE D'APPEL — À la main (le Chat, à la demande de Jean-Luc), autant de fois qu'il faut : chaque appel reprend
  où la chaîne s'est arrêtée. Aucune tâche automatique ne l'appelle. Éprouvé par
  tests/EPREUVES_LANCER_UNE_STRATEGIE_Mer_25-11-2026.py.
③ ENTRÉE — `<racine>` : une COPIE du dépôt, sans .git (A-861 : la moulinette ne tourne que sur une copie) ;
  `<STRATÉGIE>` `<ESSAI>` : exemple réel C5E10-OBS-V1 E01 ; `--tranches=N` (1 à 99) : en combien de tranches ② est
  découpé ; par défaut la largeur du réservoir des places de GitHub (FABRIQUER_LE_CIRCUIT_PUBLIC.
  LARGEUR_DES_CIRCUITS_LONGS, 18, A-888), lue et non recopiée, pour que le même découpage serve le jour où ② partira
  sur GitHub ; `--famille-deja-jouee-declaree=<texte non vide>` : la déclaration explicite qui lève le refus d'une famille
  déjà jouée sur 2000-2023 (écrite au journal de la chaîne par l'enchaîneur, et recopiée dans l'état ; le lanceur ne
  la vérifie pas ; inutile et non écrite pour une famille neuve). Lu : <racine>/donnees/combinatoires/VARIABLES_DE_DECLINAISON_<STRATÉGIE>_<ESSAI>.csv (les réglages
  validés), le journal de la chaîne (VERIFIER_LA_CHAINE), le fichier d'état d'un appel précédent.
④ CONDITIONS D'ENTRÉE — La racine existe et ne porte pas .git. Un appel qui reprend une chaîne garde le découpage
  des tranches déjà jouées, quel qu'en soit l'auteur (sinon des tranches de deux découpages se mêleraient : refus,
  lu dans le JOURNAL par `V.decoupage_mele`, jamais dans le fichier d'état — L-3 du RELU Cowork du 25-11-2026).
⑤ SORTIE — UNE valeur, le code : 0 la chaîne est faite jusqu'à ④ (chaque version retenue jugée) · 1 une étape a
  échoué, ou refus (dont la famille déjà jouée sans déclaration) · 2 un contrôle n'a pas pu tourner, usage faux, racine
  avec .git (R-734) · 3 « ATTEND JEAN-LUC : validation des réglages (⓪) ». Fichiers : sous
  <racine>/CHAINE_<STRATÉGIE>_<ESSAI>/ (ceux de l'enchaîneur), plus ETAT_DU_LANCEUR.json et lanceur/<étape>.txt.
⑥ TRAITEMENT — ① arguments, .git refusé · ② les tranches déjà témoignées comparées au découpage en N
  (`V.decoupage_mele`) · ③ la famille (`V.famille_deja_jouee`, sauf déclaration déjà au journal) : déjà jouée sans
  déclaration → refus AVANT ⓪ ; avec déclaration → l'enchaîneur « declarer » · ④ avant ⓪ (si ⓪ n'est pas témoigné) :
  les réglages validés, sinon arrêt code 3 · ⑤ pour chaque étape non témoignée, dans l'ordre : l'enchaîneur, puis son
  code, puis son témoin, l'état écrit après chacune · ⑥ après ⓪ : la validation relue sur la copie figée que DECLINER
  lira · ⑦ avant ② : où jouer (GitHub ou local, lu dans la table du relais) · ⑧ après ③ : ④ pour chaque version
  retenue par ③, dans l'ordre du tri (l'enchaîneur refait la garde de famille à sa porte).
⑦ UNITÉ — secondes (délais, durées) ; heure de Paris (horodatages).
⑧ POURQUOI — A-965 (Jean-Luc, 21-11-2026 14h43) : une commande au lieu de cinq étapes tapées à la main ; A-919 :
  l'ordre est gardé par l'enchaîneur et le juge, jamais sauté ; A-777 et C12 (ci-dessus) : ④ seulement sur une
  famille jamais jouée sur 2000-2023, sauf déclaration.
⑨ CE QUI CLOCHE — ① Trois noms sont recopiés de l'enchaîneur faute de constante qui les porte : le chemin du
  tableau validé (« donnees/combinatoires/VARIABLES_DE_DECLINAISON_<S>_<E>.csv »), la forme du témoin d'une tranche
  (« 2-tranche-<k> ») et la règle « jouable OUI et paramètre obligatoire et validation_valable » (aussi dans
  VERIFIER_LA_CHAINE.motifs). Si l'un change là-bas, le lanceur se trompe : il refusera à tort (validation) ou relancera
  une tranche que l'enchaîneur refusera (code 1, visible) — jamais en silence vers un vert. ② ② ne part pas sur GitHub :
  le circuit manque (proposition dans echanges/A_RELIRE.md) ; si la table du relais apprend « moulinette » sans que le
  lanceur soit branché, il s'arrête en code 2 plutôt que de jouer en local en silence. ③ L'avancement n'est pas publié
  (aucune écriture au dépôt public ici). ④ « Le soir » (le circuit du soir après ④) n'est pas enchaîné. ⑤ La mention de validation ne prouve qu'une ligne écrite (⑨ ① de
  VERIFIER_LA_CHAINE). ⑥ LA FAMILLE est lue comme « même CODE de module de signal » (empreinte du code sans ses
  textes, `V.famille_deja_jouee`) qu'une fiche de CONTRATS.FICHES_DEJA_VUES_SUR_LE_REGARD_UNIQUE : définition de
  l'écrivain, NON décidée par Jean-Luc (question dans la note, L-5) ; une copie du code C5 changée d'une instruction,
  ou un module qui charge C5 par son chemin, passe ; elle ne voit pas une famille jouée sur 2000-2023 qui n'y est pas
  inscrite, ni le registre des essais (lu au dépôt distant, injoignable d'une copie sans .git) : le juge garde de toute
  façon sa propre porte du regard unique.
  ⑦ Le format du témoin « 4-juger-<version> » est recopié de l'enchaîneur. ⑧ La déclaration n'est qu'un texte.
⑩ EFFET — Écrit sous le dossier de la chaîne de la racine (par l'enchaîneur, et ici l'état et les sorties) ; à ④,
  l'enchaîneur ajoute la fiche de chaque version jugée au registre de la racine, et le juge écrit ce qu'il écrit. Aucun cours n'est lu ici.
⑪ TERMINAISON — Chaque appel à l'enchaîneur est borné (`DELAI`) ; l'enchaîneur borne lui-même chaque programme.
  [sort: oui — code]
"""
import json
import os
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo

sys.dont_write_bytecode = True
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import VERIFIER_LA_CHAINE as V  # noqa: E402  journal, témoins, dossier de la chaîne (R-708)
import ENCHAINER_LA_MOULINETTE as E  # noqa: E402  `lancer` et les noms des témoins (FAITE) vivent là (R-708)
import DECLINER_LES_STRATEGIES as DECLINER  # noqa: E402  la règle de validation vit là (R-708)

ENCHAINEUR = os.path.join(ICI, "ENCHAINER_LA_MOULINETTE.py")
ETAT = "ETAT_DU_LANCEUR.json"
DELAI = 620                 # secondes : au-dessus des 580 s que l'enchaîneur laisse à JOUER
PARIS = ZoneInfo("Europe/Paris")
FIN = "TERMINÉ : ⓪ ① ② ③ ④ faits"
ARRET_REGLAGES = "ATTEND JEAN-LUC : validation des réglages (⓪)"
CODE_REGLAGES = 3
DECLARER = "--famille-deja-jouee-declaree="


def maintenant():
    """Rend l'heure de Paris, « AAAA-MM-JJ HHhMM:SS ».

    ① RÔLE — Horodater l'état.
    ② CONTEXTE D'APPEL — `ecrire_l_etat`, `executer`.
    ③ ENTRÉE — aucune.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte.
    [rend: 1]
    ⑥ TRAITEMENT — l'horloge, fuseau Europe/Paris.
    ⑦ UNITÉ — heure de Paris.
    ⑧ POURQUOI — horodatage Europe/Paris exigé par les instructions du projet.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — aucun.
    ⑪ TERMINAISON — rend la main.
    [sort: non]
    """
    return datetime.now(PARIS).strftime("%Y-%m-%d %Hh%M:%S")


def ecrire_l_etat(ch, etat, statut, message):
    """Écrit l'état du lanceur, en entier, d'un seul geste (fichier temporaire puis remplacement).

    ① RÔLE — Publier l'avancement dans un fichier lisible par un programme.
    ② CONTEXTE D'APPEL — `executer`, après chaque étape et à chaque arrêt.
    ③ ENTRÉE — `ch` : le dossier de la chaîne ; `etat` : le dictionnaire (strategie, essai, tranches, etapes…) ;
      `statut` : « EN COURS », « ÉCHEC », « ATTEND JEAN-LUC », « CONTRÔLE IMPOSSIBLE » ; `message` : une ligne.
      Exemple de message : ARRET_REGLAGES.
    ④ CONDITIONS D'ENTRÉE — `ch` existe.
    ⑤ SORTIE — aucune.
    [rend: rien]
    ⑥ TRAITEMENT — statut, message et heure posés dans `etat` ; JSON écrit dans `<ch>/ETAT_DU_LANCEUR.json.tmp`, puis
      `os.replace` sur `<ch>/ETAT_DU_LANCEUR.json`.
    ⑦ UNITÉ — heure de Paris.
    ⑧ POURQUOI — A-965 : « il publie l'avancement » ; un remplacement d'un seul geste évite qu'un lecteur voie un
      fichier à moitié écrit.
    ⑨ CE QUI CLOCHE — l'état n'est pas publié ailleurs que dans la racine (⑨ ③ de l'en-tête).
    ⑩ EFFET — écrit le fichier d'état.
    ⑪ TERMINAISON — rend la main ; une erreur d'écriture lève OSError (`main` la convertit en code 2).
    [sort: non]
    """
    etat.update(statut=statut, message=message, mis_a_jour=maintenant())
    tmp = os.path.join(ch, ETAT + ".tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(etat, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    os.replace(tmp, os.path.join(ch, ETAT))


def reglages_non_valides(chemin):
    """Rend la liste des réglages obligatoires non validés par Jean-Luc dans un tableau de réglages (vide : valide).

    ① RÔLE — Dire si ⓪ peut céder la place à ①.
    ② CONTEXTE D'APPEL — `executer`, avant ⓪ (tableau de donnees/combinatoires) et après ⓪ (copie figée valide/).
    ③ ENTRÉE — `chemin` : un tableau VARIABLES_DE_DECLINAISON (colonnes parametre, jouable, valide_par, prepare_le).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE liste de textes ; ["tableau absent : <chemin>"] si le fichier n'existe pas.
    [rend: 1]
    ⑥ TRAITEMENT — `V.lire` ; une ligne compte si jouable = OUI et parametre dans DECLINER.OBLIGATOIRES ; elle est non
      validée si `DECLINER.validation_valable` la refuse ; aucune ligne obligatoire du tout est aussi un motif.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — A-965 : le lanceur s'arrête sur la validation des réglages. Vérifier AVANT ⓪ évite de figer un
      tableau non validé : l'enchaîneur refuserait ensuite de refaire ⓪ (« un essai ne se refait pas »).
    ⑨ CE QUI CLOCHE — la règle est recopiée de VERIFIER_LA_CHAINE.motifs (⑨ ① de l'en-tête).
    ⑩ EFFET — lit.
    ⑪ TERMINAISON — rend la main, ou lève V.Impossible (fichier illisible).
    [sort: non]
    """
    if not os.path.exists(chemin):
        return ["tableau absent : %s" % chemin]
    lignes = [l for l in V.lire(chemin, ["parametre", "jouable", "valide_par"])
              if l.get("jouable") == "OUI" and l.get("parametre") in DECLINER.OBLIGATOIRES]
    if not lignes:
        return ["aucun réglage obligatoire (%s) jouable dans %s" % (", ".join(DECLINER.OBLIGATOIRES), chemin)]
    return ["réglage %s : valide_par = %r (attendu « Jean-Luc le JJ-MM-AAAA »)" % (l["parametre"], l["valide_par"])
            for l in lignes if not DECLINER.validation_valable(l)]


def ou_jouer():
    """Rend (où, raison) : « local » quand le relais de GitHub ne sait pas lancer l'étape jouer.

    ① RÔLE — Décider où ② se joue, d'après ce que le relais sait faire, jamais d'après une liste écrite ici.
    ② CONTEXTE D'APPEL — `executer`, une fois, avant la première tranche à jouer.
    ③ ENTRÉE — aucune ; lu : FABRIQUER_LE_CIRCUIT_PUBLIC.CIRCUITS_DU_RELAIS (nom de chaque circuit en tête de ligne).
    ④ CONDITIONS D'ENTRÉE — FABRIQUER_LE_CIRCUIT_PUBLIC.py est à côté de ce programme.
    ⑤ SORTIE — DEUX valeurs : « local » ou « github-non-branche », et la raison en une ligne.
    [rend: 2]
    ⑥ TRAITEMENT — import du fabricant ; si « moulinette » est parmi les circuits du relais → « github-non-branche »
      (le lanceur n'a pas encore le geste de dépôt de la demande) ; sinon « local ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — A-965 : ② sur GitHub si possible, sinon en local avec un message clair ; A-888 : le réservoir des
      places est celui des circuits longs.
    ⑨ CE QUI CLOCHE — le nom « moulinette » est celui PROPOSÉ dans la note ; il n'existe nulle part encore.
    ⑩ EFFET — importe le fabricant (aucune écriture).
    ⑪ TERMINAISON — rend la main ; l'import peut lever (`main` convertit en code 2).
    [sort: non]
    """
    import FABRIQUER_LE_CIRCUIT_PUBLIC as F
    connus = [c[0] for c in F.CIRCUITS_DU_RELAIS]
    if "moulinette" in connus:
        return "github-non-branche", ("le relais sait lancer « moulinette » mais le lanceur n'a pas encore le geste qui "
                                      "dépose la demande : à écrire avant tout usage")
    return "local", ("② EN LOCAL, tranche après tranche : le relais de GitHub (demande_de_serie.yml) ne sait lancer que "
                     "%s — le circuit « moulinette » est à créer (proposition dans echanges/A_RELIRE.md)"
                     % ", ".join(connus))


def etapes_restantes(t, n):
    """Rend la liste ordonnée des étapes non témoignées : (étape, arguments, témoin attendu).

    ① RÔLE — Reprendre où la chaîne s'est arrêtée.
    ② CONTEXTE D'APPEL — `executer`, une fois.
    ③ ENTRÉE — `t` : les témoins (`V.temoins`) ; `n` : le nombre de tranches. Exemple : t vide, n = 3 → preparer,
      decliner, jouer 0 3, jouer 1 3, jouer 2 3, assembler, trier.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE liste de triplets.
    [rend: 1]
    ⑥ TRAITEMENT — l'ordre de l'enchaîneur (A-919) ; les témoins viennent de E.FAITE, et « 2-tranche-<k> » pour une
      tranche ; une étape est gardée si son témoin manque.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — l'enchaîneur refuse une étape déjà faite : la relancer ferait échouer une reprise.
    ⑨ CE QUI CLOCHE — la forme « 2-tranche-<k> » est recopiée de l'enchaîneur (⑨ ① de l'en-tête).
    ⑩ EFFET — aucun.
    ⑪ TERMINAISON — rend la main.
    [sort: non]
    """
    tout = [("preparer", (), E.FAITE["preparer"]), ("decliner", (), E.FAITE["decliner"])]
    tout += [("jouer", (str(k), str(n)), "2-tranche-%d" % k) for k in range(n)]
    tout += [("assembler", (), E.FAITE["assembler"]), ("trier", (), E.FAITE["trier"])]
    return [x for x in tout if x[2] not in t]


def executer(racine, sid, essai, n, declaration=None):
    """Enchaîne les étapes restantes ; rend le code de sortie.

    ① RÔLE — Le cœur du lanceur.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `racine` (absolu, sans .git), `sid`, `essai`, `n` (tranches) ; `declaration` : le texte de
      --famille-deja-jouee-declaree, ou None.
    ④ CONDITIONS D'ENTRÉE — `main` a vérifié les arguments et l'absence de .git.
    ⑤ SORTIE — UNE valeur : 0, 1, 2 ou 3 (voir ⑤ de l'en-tête).
    [rend: 1]
    ⑥ TRAITEMENT — voir ⑥ ② à ⑧ de l'en-tête ; chaque étape : `E.lancer` de l'enchaîneur, sortie dans
      `<ch>/lanceur/<étape>.txt`, puis code ≠ 0 → ÉCHEC, puis témoin absent → ÉCHEC.
    ⑦ UNITÉ — secondes.
    ⑧ POURQUOI — A-965, A-919, A-777 et C12.
    ⑨ CE QUI CLOCHE — voir ⑨ de l'en-tête.
    ⑩ EFFET — l'enchaîneur écrit sous la chaîne ; ici l'état et les sorties.
    ⑪ TERMINAISON — rend la main, ou lève V.Impossible (délai, fichier illisible, famille inconnue), ValueError (état
      illisible).
    [sort: non]
    """
    ch = V.dossier(racine, sid, essai)
    os.makedirs(os.path.join(ch, "lanceur"), exist_ok=True)
    chemin_etat = os.path.join(ch, ETAT)
    if os.path.exists(chemin_etat):
        with open(chemin_etat, encoding="utf-8") as fh:
            etat = json.load(fh)
    else:
        etat = {"strategie": sid, "essai": essai, "etapes": []}
    etat["tranches"] = n
    # LE DÉCOUPAGE, LU DANS LE JOURNAL (L-3) : les tranches déjà témoignées doivent être celles du découpage en n.
    mele = V.decoupage_mele(ch, n)
    if mele:
        message = "REFUS : --tranches=%d mêlerait deux découpages — %s" % (n, " · ".join(mele))
        ecrire_l_etat(ch, etat, "ÉCHEC", message)
        print(message)
        return 1
    # LA FAMILLE, AVANT ⓪ (L-4) : la garde de ④ (V.garde_de_famille) refuserait de toute façon ; la lire ici évite
    # de calculer ② pour rien.
    t = V.temoins(ch)
    if V.TEMOIN_DE_FAMILLE not in t:
        deja = V.famille_deja_jouee(racine, sid)
        if deja and not declaration:
            message = ("REFUS ④ avant ⓪ : la famille de %s est déjà jouée sur 2000-2023 (%s) — décision %s ; rien n'est "
                       "lancé ; pour juger quand même : --famille-deja-jouee-declaree=<qui, quand, mots>"
                       % (sid, " · ".join(deja), V.DECISION_FAMILLE))
            ecrire_l_etat(ch, etat, "ÉCHEC", message)
            print(message)
            return 1
        if deja:
            code = E.lancer(racine, ch, "lanceur/declarer", ENCHAINEUR, racine, sid, essai, "declarer", declaration,
                            delai=DELAI)
            if code != 0 or V.TEMOIN_DE_FAMILLE not in V.temoins(ch):
                ecrire_l_etat(ch, etat, "ÉCHEC", "déclaration de famille : l'enchaîneur a rendu le code %d" % code)
                print("ÉCHEC — déclaration de famille : code %d" % code)
                return 1
            etat["famille_deja_jouee_declaree"] = {"motifs": deja, "declaration": declaration}
            print("④ permis malgré une famille déjà jouée sur 2000-2023, sur déclaration : %s" % declaration)
        elif declaration:
            print("famille neuve : la déclaration n'est pas écrite (rien à lever)")
        t = V.temoins(ch)
    variables = "VARIABLES_DE_DECLINAISON_%s_%s.csv" % (sid, essai)
    if E.FAITE["preparer"] not in t:
        m = reglages_non_valides(os.path.join(racine, "donnees", "combinatoires", variables))
        if m:
            ecrire_l_etat(ch, etat, "ATTEND JEAN-LUC", ARRET_REGLAGES + " — " + " · ".join(m))
            print("%s — rien n'est lancé :\n  %s\n  proposition des réglages : python3 -B programmes/PREPARER_LES_"
                  "VARIABLES_DE_DECLINAISON_DES_STRATEGIES.py donnees/cac40_strategies.csv %s donnees/combinatoires/"
                  "VOISINAGE.csv %s donnees/combinatoires" % (ARRET_REGLAGES, "\n  ".join(m), sid, essai))
            return CODE_REGLAGES
    ou = None
    for etape, args, temoin in etapes_restantes(t, n):
        if etape == "jouer" and ou is None:
            ou, raison = ou_jouer()
            print(raison)
            etat["ou_jouer"] = {"ou": ou, "raison": raison}
            if ou != "local":
                ecrire_l_etat(ch, etat, "CONTRÔLE IMPOSSIBLE", raison)
                return 2
        ecrire_l_etat(ch, etat, "EN COURS", "étape %s %s lancée" % (etape, " ".join(args)))
        debut, t0 = maintenant(), time.monotonic()
        code = E.lancer(racine, ch, "lanceur/%s%s" % (etape, "_" + args[0] if etape == "jouer" else ""),
                        ENCHAINEUR, racine, sid, essai, etape, *args, delai=DELAI)
        etat["etapes"].append({"etape": etape, "arguments": list(args), "code": code, "ou": ou or "local",
                               "debut": debut, "secondes": round(time.monotonic() - t0, 1)})
        if code != 0:
            ecrire_l_etat(ch, etat, "ÉCHEC", "étape %s %s : l'enchaîneur a rendu le code %d (sortie : lanceur/)"
                          % (etape, " ".join(args), code))
            print("ÉCHEC — étape %s %s : l'enchaîneur a rendu le code %d" % (etape, " ".join(args), code))
            return 1
        if temoin not in V.temoins(ch):
            ecrire_l_etat(ch, etat, "ÉCHEC", "étape %s %s : code 0 mais sans témoin %s au journal"
                          % (etape, " ".join(args), temoin))
            print("ÉCHEC — étape %s : code 0 sans témoin %s" % (etape, temoin))
            return 1
        if etape == "preparer":
            m = reglages_non_valides(os.path.join(ch, V.temoins(ch)["0-variables-validees"][0]))
            if m:
                ecrire_l_etat(ch, etat, "ATTEND JEAN-LUC", ARRET_REGLAGES + " — copie figée : " + " · ".join(m))
                print("%s — copie figée non validée :\n  %s" % (ARRET_REGLAGES, "\n  ".join(m)))
                return CODE_REGLAGES
    return juger_les_retenues(racine, sid, essai, ch, etat)


def juger_les_retenues(racine, sid, essai, ch, etat):
    """Le juge, par l'enchaîneur, pour chaque version retenue par le tri et non encore jugée ; rend le code.

    ① RÔLE — Faire ④ sans choisir à la place de Jean-Luc : TOUTES les versions retenues.
    ② CONTEXTE D'APPEL — `executer`, quand le tri est témoigné.
    ③ ENTRÉE — `racine` ; `sid` ; `essai` ; `ch` : le dossier de la chaîne ; `etat` : le dictionnaire d'état.
    ④ CONDITIONS D'ENTRÉE — le témoin « 3-trier » est au journal ; la famille a été lue avant ⓪ par `executer`.
    ⑤ SORTIE — UNE valeur : 0 toutes jugées · 1 refus (dont celui de la garde de famille de l'enchaîneur) ou juge en
      échec.
    [rend: 1]
    ⑥ TRAITEMENT — ① les versions du tri (`V.lire`), dans l'ordre · ② pour chacune sans témoin « 4-juger-<version> » :
      l'enchaîneur « juger » (sa garde, `V.motifs`, refait la garde de famille), code ≠ 0 ou témoin absent → ÉCHEC ·
      ③ état TERMINÉ.
    ⑦ UNITÉ — un nombre de versions.
    ⑧ POURQUOI — A-775 (méthode de Jean-Luc, en substance : « rejouer TOUTES les sélectionnées sur les 30 % ») ; A-777 et C12.
    ⑨ CE QUI CLOCHE — ⑨ ⑥ à ⑧ de l'en-tête.
    ⑩ EFFET — l'enchaîneur ajoute une fiche par version au registre de la racine ; écrit l'état ; affiche.
    ⑪ TERMINAISON — rend la main, ou lève V.Impossible ; chaque appel est borné par `E.lancer`.
    [sort: non]
    """
    retenues = [r["id_version"] for r in V.lire(os.path.join(ch, V.temoins(ch)[E.FAITE["trier"]][0]), ["id_version"])]
    for ident in retenues:
        temoin = "4-juger-%s" % ident
        if temoin in V.temoins(ch):
            continue
        ecrire_l_etat(ch, etat, "EN COURS", "étape juger %s lancée" % ident)
        debut, t0 = maintenant(), time.monotonic()
        code = E.lancer(racine, ch, "lanceur/juger_%s" % ident, ENCHAINEUR, racine, sid, essai, "juger", ident,
                        delai=DELAI)
        etat["etapes"].append({"etape": "juger", "arguments": [ident], "code": code, "ou": "local", "debut": debut,
                               "secondes": round(time.monotonic() - t0, 1)})
        if code != 0 or temoin not in V.temoins(ch):
            message = "étape juger %s : l'enchaîneur a rendu le code %d%s" % (
                ident, code, "" if code else " sans témoin %s" % temoin)
            ecrire_l_etat(ch, etat, "ÉCHEC", message)
            print("ÉCHEC — " + message)
            return 1
    message = "%s — %d version(s) retenue(s) par ③, toutes jugées" % (FIN, len(retenues))
    ecrire_l_etat(ch, etat, "TERMINÉ", message)
    print(message)
    return 0


def main(argv):
    """Rend le code de sortie de la ligne de commande.

    ① RÔLE — Lire les arguments, refuser un dépôt, convertir les erreurs en code 2.
    ② CONTEXTE D'APPEL — `__main__`.
    ③ ENTRÉE — `argv` : exemple `[…, "/dev/shm/x/depot", "C5E10-OBS-V1", "E01", "--tranches=5"]`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 0, 1, 2 ou 3.
    [rend: 1]
    ⑥ TRAITEMENT — ① 3 arguments, au plus une fois « --tranches=N » (N de 1 à 99) et au plus une fois
      « --famille-deja-jouee-declaree=<texte non vide> », aucune autre option, sinon usage et 2 · ② racine absente ou
      portant .git → 2 · ③ `executer` · ④ V.Impossible, OSError, ValueError, KeyError, IndexError → 2.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734 : un contrôle qui n'a pas pu tourner ne rend jamais 0 ; A-861 : jamais dans un dépôt.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — voir l'en-tête.
    ⑪ TERMINAISON — rend la main ; `__main__` passe le code à `sys.exit`.
    [sort: non]
    """
    pos = [a for a in argv[1:] if not a.startswith("--")]
    tr = [a[len("--tranches="):] for a in argv[1:] if a.startswith("--tranches=")]
    dec = [a[len(DECLARER):].strip() for a in argv[1:] if a.startswith(DECLARER)]
    autres = [a for a in argv[1:] if a.startswith("--") and not a.startswith(("--tranches=", DECLARER))]
    n = int(tr[0]) if len(tr) == 1 and tr[0].isdigit() else None
    if len(pos) != 3 or autres or len(tr) > 1 or len(dec) > 1 or (tr and not (n and 1 <= n <= 99)) or \
            (dec and not dec[0]):
        print(__doc__.split("① RÔLE")[0])
        return 2
    racine, sid, essai = os.path.abspath(pos[0]), pos[1], pos[2]
    if not os.path.isdir(racine) or os.path.lexists(os.path.join(racine, ".git")):
        print("ARRÊT : %s absent ou porteur de .git — la moulinette ne tourne que sur une copie (A-861)" % racine)
        return 2
    try:
        if n is None:
            import FABRIQUER_LE_CIRCUIT_PUBLIC as F
            n = F.LARGEUR_DES_CIRCUITS_LONGS
        return executer(racine, sid, essai, n, dec[0] if dec else None)
    except (V.Impossible, OSError, ValueError, KeyError, IndexError) as e:
        print("CONTRÔLE IMPOSSIBLE (R-734) : %s: %s" % (type(e).__name__, e))
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
