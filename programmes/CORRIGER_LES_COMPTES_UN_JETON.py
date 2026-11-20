#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CORRIGER_LES_COMPTES_UN_JETON.py — retire des comptes « un jeton » un achat fait contre la règle, et y met l'achat
que la règle donnait, CALCULÉ par la tenue des positions du soir.

Simulation uniquement : aucun ordre réel n'est jamais passé.
Écrit le mercredi 18-11-2026 (Paris), étape CORR du planning (BACKLOG A-801).

LE SENS EN TÊTE. Le soir du 20-10-2026, la stratégie C5E10-OBS-V1 a signalé deux valeurs : ENGIE (CCI −57,03) et
EIFFAGE (CCI −166,47). En « un jeton » (une seule position à la fois par stratégie), la règle R-207bis donne le jeton
à la plus survendue, le CCI le plus bas : EIFFAGE. Le circuit d'alors lisait l'univers de haut en bas et l'a donné à
ENGIE. Jean-Luc a décidé le 15-11-2026 à 12h29 : « on le retire des comptes, mais du coup tu fais bien l'achat
d'Eiffage ». Ce programme fait ce geste SANS RIEN ÉCRIRE À LA MAIN (R-728) : il rejoue le soir du signal par les
fonctions mêmes du circuit (`TENIR_LES_POSITIONS.tenir` : départage R-207bis, achat à l'ouverture de la séance
suivante, objectif, stop et échéance lus à la fiche, frais lus au barème daté par `MODULE_POSITIONS`), et écrit le
fichier des corrections que la mesure de la performance lit. Le journal des trades n'est jamais touché.

① RÔLE — Écrire `donnees/corrections_des_comptes_un_jeton.csv` : pour chaque décision déclarée dans
  `programmes/CONTRATS_DES_FICHIERS.py` (`CORRECTIONS_UN_JETON_DECIDEES`), la copie à l'octet de la ligne du journal
  retirée des comptes un jeton, et la ligne de remplacement calculée par le rejeu ; ou, avec `--verifier`, refaire
  ce calcul et dire si le fichier déposé lui est identique.
② CONTEXTE D'APPEL — Lancé à la main par le Chat, une fois par décision nouvelle :
  `python3 programmes/CORRIGER_LES_COMPTES_UN_JETON.py .` ; puis `--verifier` par le relecteur et par Cowork. Importé
  par l'épreuve `tests/EPREUVES_DE_LA_CORRECTION_UN_JETON_Mer_18-11-2026.py`. Aucune tâche du soir ne le lance : la
  mesure ne lit que le fichier écrit.
③ ENTRÉE — En ligne de commande : la racine du dépôt (« . » par défaut) et, facultative, l'option `--verifier`.
④ CONDITIONS D'ENTRÉE — La racine est un clone git qui porte le commit des signaux nommé par chaque décision (un
  clone superficiel ne l'a pas) ; `donnees/claude_journal_trades.csv`, `donnees/claude_positions_ouvertes.csv`, le
  registre des stratégies, le référentiel des valeurs et les cours lisibles par le lecteur unique du soir.
⑤ SORTIE — Un code de sortie : 0 si le fichier est écrit (ou déjà identique) ou, en `--verifier`, identique au
  calcul ; 1 si une confrontation échoue ou si le fichier déposé diffère du calcul ; 2 si le calcul n'a pas pu tourner
  (commit des signaux introuvable, fichier absent, lecture des cours refusée) — R-734 : un contrôle qui n'a pas pu
  tourner ne rend jamais 0.
⑥ TRAITEMENT — Pour chaque décision : ① relire au dépôt les signaux du soir (`signaux_du_soir`) · ② les attribuer à
  la stratégie par `TENIR_LES_POSITIONS.attribuer_aux_strategies`, et mettre à part un CCI fautif · ③ rejouer, séance
  après séance depuis celle du signal, `TENIR_LES_POSITIONS.tenir` sur les cours coupés au soir joué, jusqu'à ce que
  toutes les positions nées de ces signaux soient vendues (`rejouer_la_decision`) · ④ confronter le rejeu au journal
  et à la décision (`confronter`) · ⑤ fabriquer les deux lignes (`lignes_de_correction`). Puis écrire le fichier, ou
  le comparer en `--verifier`.
⑦ UNITÉ — Prix et montants en euros, tels que `cloturer` les écrit (cinq décimales pour les prix, deux pour les
  montants) ; dates AAAA-MM-JJ ; échéance en séances de bourse.
⑧ POURQUOI — BACKLOG A-801 (décision de Jean-Luc du 15-11-2026 à 12h29), étape CORR du planning. Un remplacement
  recopié du journal des jetons illimités aurait été « écrit à la main » par copie : il est recalculé, puis confronté à
  la ligne des jetons illimités que le circuit a écrite le 02-11-2026 (même achat, même vente) — deux chemins, un
  seul résultat. La décision nomme EIFFAGE : le programme la RETROUVE par la règle et refuse si la règle en donne une
  autre, pour qu'une décision mal recopiée ne s'applique jamais.
⑨ CE QUI CLOCHE — Consigné, non corrigé (R-752) : · le rejeu ne repasse pas le filtre `juge.fiche_suivie` du soir (fiche refusée
  par le juge) : la fiche de la décision est prise au registre par son empreinte (`fiche_de_la_decision`, F3
  d'A-924, 20-11-2026), sans passer la porte du soir · les cours, le barème, le calendrier et le référentiel du rejeu
  restent ceux d'aujourd'hui (seule la fiche est désignée de façon stable) · « personne ne relance --verifier » est
  atténué depuis le 20-11-2026 : la mesure du soir exige que la ligne ajoutée ait sa jumelle au journal
  (`verifier_la_ligne_ajoutee`, F1 d'A-924) · le rejeu part de positions vides le
  soir du signal : `confronter` vérifie au journal qu'aucune position un jeton de la stratégie n'était en cours, pas
  aux positions de ce soir-là (le fichier des positions de l'époque n'est pas relu) · le radar et le message du soir
  lisent le journal brut ; le cockpit dit la ligne retirée · personne ne relance `--verifier` (BACKLOG, D5).
⑩ EFFET — Lit des fichiers et lance `git show` (lecture seule) ; écrit un seul fichier,
  `donnees/corrections_des_comptes_un_jeton.csv`, et seulement hors `--verifier` ; n'écrase JAMAIS un fichier qui
  diffère du calcul (code 1, rien n'est écrit) ; aucun accès réseau.
⑪ TERMINAISON — Rend un code de sortie ; un appel peut-il ne pas revenir ? `git show` est lancé avec un délai de
  60 secondes ; le rejeu s'arrête à la dernière séance des cours.

⑫ DÉFINITIONS —
  un jeton : la comptabilité où une seule position est ouverte à la fois par stratégie ; un signal reçu pendant une
    position est ignoré.
  jetons illimités : la comptabilité où tout signal est suivi ; elle juge la qualité du signal.
  R-207bis : la règle du départage — quand plusieurs valeurs signalent le même soir pour une stratégie, le jeton va à
    celle dont le CCI est le plus bas (la plus survendue), égalité → ordre alphabétique.
  une séance : une journée de bourse.
"""
import bisect
import csv
import io
import json
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)

import CONTRATS_DES_FICHIERS as C  # noqa: E402


class CalculImpossible(Exception):
    """Le calcul n'a pas pu tourner : une source manque ou se refuse (code 2, R-734).

    ① RÔLE — Distinguer « je n'ai pas pu calculer » (code 2) de « le calcul contredit le journal » (code 1).
    ② CONTEXTE D'APPEL — Levée par `signaux_du_soir` et `rejouer_la_decision` ; attrapée par `main`.
    ③ ENTRÉE — Le message.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — —
    ⑥ TRAITEMENT — —
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734 : un contrôle qui n'a pas pu tourner rend un code NON NUL, et différent d'un verdict.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — —
    """


def _briques(racine):
    """Charge la tenue des positions du soir et son moteur, depuis la racine donnée.

    ① RÔLE — Donner au rejeu les fonctions mêmes du circuit du soir, prises dans la racine examinée.
    ② CONTEXTE D'APPEL — `rejouer_la_decision`.
    ③ ENTRÉE — `racine` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — `programmes/TENIR_LES_POSITIONS.py` et `programmes/MODULE_POSITIONS.py` sous la racine.
    ⑤ SORTIE — DEUX valeurs : le module de la tenue des positions, et le moteur des positions qu'il charge.
      [rend: 2]
    ⑥ TRAITEMENT — Importer `TENIR_LES_POSITIONS` depuis `programmes/` de la racine, puis lui faire charger son moteur
      par `charger_module_positions(trouver_module(racine))`, comme `tenir_pour_de_vrai` le fait le soir.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-708 : deux implémentations d'une même chose divergent toujours ; le rejeu passe par le code du soir.
    ⑨ CE QUI CLOCHE — Le module est importé une fois par processus : deux racines différentes dans un même processus
      partageraient le premier chargé (l'épreuve lance chaque copie dans un sous-processus).
    ⑩ EFFET — Importe des modules.
    ⑪ TERMINAISON — Rend la main ; lève ce que l'import lève.
      [sort: non]
    """
    prog = os.path.join(os.path.realpath(racine), "programmes")
    if prog not in sys.path:
        sys.path.insert(0, prog)
    import TENIR_LES_POSITIONS as T
    return T, T.charger_module_positions(T.trouver_module(racine))


def signaux_du_soir(racine, trace):
    """Relit au dépôt le fichier des signaux d'un soir passé, tel que le circuit l'a écrit.

    ① RÔLE — Retrouver les signaux qui ont fondé la décision, sans les recopier à la main.
    ② CONTEXTE D'APPEL — `rejouer_la_decision`.
    ③ ENTRÉE — `racine` : la racine du clone · `trace` : « <commit>:<chemin> », la valeur `signaux_du_soir` d'une
      décision de `CORRECTIONS_UN_JETON_DECIDEES`.
    ④ CONDITIONS D'ENTRÉE — Le commit est présent dans le clone.
    ⑤ SORTIE — UNE valeur : le contenu JSON lu (un dictionnaire avec `seance` et `signaux`).
      [rend: 1]
    ⑥ TRAITEMENT — `git -C racine show trace`, délai 60 s ; décoder le JSON.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le fichier des signaux est réécrit chaque soir : seul l'historique du dépôt garde celui du
      20-10-2026 (commit 553c2fd2, poussé par le circuit à 21h59 Paris).
    ⑨ CE QUI CLOCHE — Un clone superficiel (une seule profondeur, comme la copie de GitHub Actions par défaut) n'a pas
      le commit : le calcul ne tourne pas (code 2), il ne se trompe pas.
    ⑩ EFFET — Lance `git show`, lecture seule.
    ⑪ TERMINAISON — Rend la main ; lève `CalculImpossible` si git échoue, dépasse 60 s, ou si le JSON est illisible.
      [sort: non]
    """
    try:
        r = subprocess.run(["git", "-C", racine, "show", trace], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise CalculImpossible("git show %s : %s" % (trace, e))
    if r.returncode != 0:
        raise CalculImpossible("git show %s : code %d — %s" % (trace, r.returncode, r.stderr.strip()[:200]))
    try:
        return json.loads(r.stdout)
    except ValueError as e:
        raise CalculImpossible("signaux de %s illisibles : %s" % (trace, e))


def fiche_de_la_decision(racine, decision):
    """Rend la ligne du registre des stratégies que la décision désigne par son empreinte.

    ① RÔLE — Donner au rejeu la fiche du soir du signal, quelle que soit la place de sa ligne au registre.
    ② CONTEXTE D'APPEL — `rejouer_la_decision` ; l'épreuve.
    ③ ENTRÉE — `racine` : la racine du dépôt · `decision` : une entrée de `CORRECTIONS_UN_JETON_DECIDEES`, qui porte
      `strategie` et `empreinte_de_la_fiche`.
    ④ CONDITIONS D'ENTRÉE — Le registre existe.
    ⑤ SORTIE — UNE valeur : la ligne (dictionnaire) ; s'il y en a plusieurs de même empreinte, la dernière — elles
      sont égales sur toutes les cases qui font le rejeu.
      [rend: 1]
    ⑥ TRAITEMENT — Lire TOUTES les lignes du registre (`lignes_du_registre`, pas `fiches_du_registre`, qui ne garde
      que la dernière) ; garder celles de la stratégie dont `empreinte_d_une_fiche` égale l'empreinte déclarée.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — F3 de la relecture de Cowork du 19-11-2026 (RELU 21ff6013, A-924) : le rejeu prenait la DERNIÈRE
      ligne de C5E10-OBS-V1 ; le jour où Jean-Luc ajoute une ligne à cette fiche (univers, seuils), l'épreuve aurait
      rougi sans que la correction soit fausse. Le registre ne fait qu'ajouter des lignes (R-727) : la ligne du soir
      du signal y reste.
    ⑨ CE QUI CLOCHE — Une ligne RÉÉCRITE sur place dans une case de l'empreinte fait perdre la fiche : le calcul
      s'arrête (CalculImpossible), il ne se trompe pas. Les autres entrées du rejeu restent celles d'AUJOURD'HUI :
      les cours du fichier maître, le barème des frais, le calendrier, le référentiel des valeurs ; une révision de
      l'une d'elles ferait encore diverger le rejeu (à consigner au BACKLOG).
    ⑩ EFFET — Lit le registre.
    ⑪ TERMINAISON — Rend la main ; lève `CalculImpossible` si aucune ligne ne porte l'empreinte, ou si le registre ne
      se lit pas.
      [sort: non]
    """
    try:
        lignes = C.lignes_du_registre(os.path.join(racine, C.REGISTRE_DES_STRATEGIES))
    except Exception as e:  # registre absent ou illisible : pas de calcul (R-734)
        raise CalculImpossible("registre des stratégies illisible : %s : %s" % (type(e).__name__, e))
    bonnes = [l for l in lignes if (l.get("id") or "") == decision["strategie"]
              and C.empreinte_d_une_fiche(l) == decision["empreinte_de_la_fiche"]]
    if not bonnes:
        raise CalculImpossible("aucune ligne %s du registre ne porte l'empreinte %s déclarée par la décision %s "
                               "(cases %s)" % (decision["strategie"], decision["empreinte_de_la_fiche"],
                                               decision["action"], ", ".join(C.CASES_DE_L_EMPREINTE_D_UNE_FICHE)))
    return bonnes[-1]


def rejouer_la_decision(racine, decision):
    """Rejoue, par la tenue des positions du soir, les signaux du soir de la décision, jusqu'à leurs ventes.

    ① RÔLE — Calculer l'achat que la règle donnait en un jeton, et ce que les jetons illimités en font, par le code
      même du circuit.
    ② CONTEXTE D'APPEL — `calculer` ; l'épreuve.
    ③ ENTRÉE — `racine` : la racine du dépôt · `decision` : une entrée de `CORRECTIONS_UN_JETON_DECIDEES`.
    ④ CONDITIONS D'ENTRÉE — Celles du programme (④ de l'en-tête).
    ⑤ SORTIE — TROIS valeurs : la liste des lignes de journal produites par `cloturer` pour la stratégie de la
      décision (les deux comptabilités) ; la liste des incidents du rejeu, chacun préfixé de sa séance ; la liste des
      positions encore ouvertes à la dernière séance des cours.
      [rend: 3]
    ⑥ TRAITEMENT — ① lire les cours par le lecteur unique du soir (`lire_les_cours_du_soir`) · ② relire les signaux
      du soir (`signaux_du_soir`) et vérifier que leur séance est celle de la décision · ③ prendre la fiche désignée
      par l'empreinte de la décision (`fiche_de_la_decision`, F3 d'A-924) et ses réglages (`reglages_des_fiches` du
      teneur), puis attribuer les signaux à cette seule stratégie (`attribuer_aux_strategies`, univers lu à cette
      fiche) et refuser un CCI fautif
      (`mettre_a_part_les_cci_fautifs`) · ④ pour chaque séance depuis celle du signal : couper les cours à cette
      séance (rien du lendemain n'est visible), appeler `tenir` avec les signaux le soir du signal et aucun ensuite,
      la séance suivante, les réglages de la fiche, la lecture et le juge — comme `tenir_pour_de_vrai` · ⑤ s'arrêter quand plus aucune position
      n'est ouverte, ou à la dernière séance.
    ⑦ UNITÉ — Euros, séances de bourse.
    ⑧ POURQUOI — R-708 : l'achat de remplacement se calcule par le chemin du soir, et non par une formule écrite ici ;
      même construction que `rejouer_les_signaux` de `programmes/MESURER_LES_INDICATEURS.py`, avec en plus la lecture
      et le juge que le soir passe à `tenir` (l'achat n'a lieu que dans le CAC 40 le jour de l'achat).
    ⑨ CE QUI CLOCHE — Voir le ⑨ de l'en-tête (positions vides le soir du signal, filtre `fiche_suivie` absent).
    ⑩ EFFET — Lit des fichiers et lance `git show` ; `tenir` n'écrit rien.
    ⑪ TERMINAISON — Rend la main ; lève `CalculImpossible` (briques introuvables, signaux introuvables, séance
      différente, aucune fiche à l'empreinte déclarée, fiche refusée par la lecture du soir, référentiel introuvable ou vide, CCI fautif, lecture des cours refusée) ; les autres
      exceptions de `tenir` remontent.
      [sort: non]
    """
    try:
        T, mod = _briques(racine)
    except Exception as e:  # brique absente ou illisible : pas de calcul (R-734), jamais une trace brute
        raise CalculImpossible("briques du circuit introuvables : %s : %s" % (type(e).__name__, e))
    try:
        cours, lecture, juge = T.lire_les_cours_du_soir(racine)
    except Exception as e:  # le lecteur unique lève des exceptions variées : toutes veulent dire « pas de calcul »
        raise CalculImpossible("lecture des cours refusée : %s : %s" % (type(e).__name__, e))
    sig = signaux_du_soir(racine, decision["signaux_du_soir"])
    seance = decision["seance_du_signal"]
    if sig.get("seance") != seance:
        raise CalculImpossible("les signaux de %s portent la séance %r, la décision %s dit %r"
                               % (decision["signaux_du_soir"], sig.get("seance"), decision["action"], seance))
    # LA FICHE DE LA DÉCISION, PAR SON EMPREINTE ET NON PAR SA PLACE (F3 d'A-924) ; ses seuils et son horizon passent
    # à `tenir` par `reglages`, sans quoi `tenir` relirait la DERNIÈRE ligne du registre
    fiche = fiche_de_la_decision(racine, decision)
    reglages = T.reglages_des_fiches(racine, [fiche])
    if fiche["id"] not in reglages:
        raise CalculImpossible("fiche %s (empreinte %s) refusée par la lecture du soir du juge"
                               % (fiche["id"], decision["empreinte_de_la_fiche"]))
    univers = {m.strip().upper() for m in (fiche.get("univers") or "").split(",") if m.strip()}
    # la table nom → mnémonique : celle du circuit (`TENIR_LES_POSITIONS.table_nom_vers_mnemonique`, R-708), sur le
    # référentiel trouvé comme le lecteur du soir le trouve (relecture du 18-11-2026, D4)
    ref = juge.trouver(racine, "REFERENTIEL_VALEURS")
    mnemo = T.table_nom_vers_mnemonique(ref) if ref else {}
    if not mnemo:
        raise CalculImpossible("référentiel des valeurs introuvable ou vide (trouver « REFERENTIEL_VALEURS » : %r)" % ref)
    traduits, _sans, _hors = T.attribuer_aux_strategies(sig.get("signaux") or [], [(fiche["id"], univers)], mnemo)
    traduits, a_part = T.mettre_a_part_les_cci_fautifs(traduits)
    if a_part:
        raise CalculImpossible("signaux du %s mis à part (CCI fautif) : %r" % (seance, a_part))
    if not traduits:
        raise CalculImpossible("aucun signal du %s n'appartient à %s" % (seance, decision["strategie"]))
    seances = sorted({b["date"] for s in cours.values() for b in s if b["date"] >= seance})
    if not seances or seances[0] != seance:
        raise CalculImpossible("la séance du signal %s est absente des cours" % seance)
    dates = {k: [b["date"] for b in s] for k, s in cours.items()}
    positions, trades, incidents = [], [], []
    for i, d in enumerate(seances):
        coupes = {k: s[:bisect.bisect_right(dates[k], d)] for k, s in cours.items()}
        suivante = seances[i + 1] if i + 1 < len(seances) else ""
        r = T.tenir(positions, coupes, traduits if d == seance else [], suivante, mod,
                    reglages=reglages, base=racine, lecture=lecture, juge=juge)
        positions = r["positions"]
        trades += [t for t in r["trades"] if t.get("strategie") == decision["strategie"]]
        incidents += ["%s : %s" % (d, x) for x in r["incidents"] + r["signaux_ignores"]]
        if not positions:
            break
    return trades, incidents, positions


def _lire_csv(chemin):
    """Lit un fichier CSV en dictionnaires, et rend aussi ses lignes de texte brutes.

    ① RÔLE — Lire le journal et les positions sans perdre le texte exact des lignes.
    ② CONTEXTE D'APPEL — `calculer`.
    ③ ENTRÉE — `chemin` : un fichier CSV séparé par des virgules, à en-tête.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe.
    ⑤ SORTIE — UNE valeur : la liste des lignes en dictionnaires.
      [rend: 1]
    ⑥ TRAITEMENT — `csv.DictReader`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ; lève OSError si le fichier manque.
      [sort: non]
    """
    with open(chemin, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def confronter(decision, journal, positions_ouvertes, trades):
    """Confronte le rejeu au journal des trades et à la décision ; rend la ligne retirée, le remplacement et les fautes.

    ① RÔLE — Refuser toute correction que le journal ou la règle ne soutiennent pas.
    ② CONTEXTE D'APPEL — `calculer` ; l'épreuve.
    ③ ENTRÉE — `decision` : une entrée de `CORRECTIONS_UN_JETON_DECIDEES` · `journal` : les lignes du journal des
      trades (dictionnaires) · `positions_ouvertes` : les lignes du fichier des positions (dictionnaires) · `trades` :
      les lignes rendues par `rejouer_la_decision`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — TROIS valeurs : la ligne du journal retirée (dictionnaire) ou None ; la ligne de remplacement
      (dictionnaire) ou None ; la liste des fautes, vide si tout tient.
      [rend: 3]
    ⑥ TRAITEMENT — ① le rejeu rend EXACTEMENT une vente en un jeton : le remplacement · ② sa valeur est celle que la
      décision nomme, et pas la valeur retirée · ③ le journal porte EXACTEMENT une ligne un jeton de la stratégie, sur
      la valeur retirée, achetée le même jour que le remplacement : la ligne retirée · ④ chaque vente rejouée en jetons
      illimités se retrouve au journal (même stratégie, valeur, jour d'achat, comptabilité) ; vendue au journal le
      jour de la mise en service du barème réel ou après (`MISE_EN_SERVICE_DU_BAREME_REEL`, contrat), elle lui est
      égale sur toutes les colonnes chiffrées, barème compris ; vendue avant, sur les prix, les jours et le motif ·
      ④bis le remplacement a, dans le rejeu, son jumeau en jetons illimités (même valeur, même jour d'achat), égal sur
      toutes les colonnes chiffrées : le ④ le confronte donc au journal · ⑤ aucun
      autre achat un jeton de la stratégie (journal, sauf la ligne retirée, et positions ouvertes) n'est fait entre le
      lendemain du signal et la vente du remplacement inclus : sinon le remplacement changerait la suite, et il faudrait
      la rejouer aussi.
    ⑦ UNITÉ — Textes tels qu'écrits au journal.
    ⑧ POURQUOI — Le ④ fait se croiser deux chemins : la ligne EIFFAGE des jetons illimités écrite par le circuit le
      02-11-2026 et le même achat rejoué aujourd'hui doivent coïncider au centime ; un rejeu qui dériverait (frais,
      seuils, séance d'achat) le dirait là. Le ⑤ porte ce que A-801 a « vérifié » à la main (TOTALENERGIES, entrée
      10-11, non touchée) : ici il se recalcule.
    ⑨ CE QUI CLOCHE — Le ④ ne compare pas les montants d'une vente antérieure à la mise en service du barème réel :
      l'achat ENGIE des jetons illimités a été vendu le 29-10-2026 sous le barème historique, et le rejeu le chiffre au
      barème réel (3 294,00 € au lieu de 3 694,00 € : la taxe de 0,4 % à l'achat). Si le remplacement lui-même était
      vendu avant cette date, son barème ne serait confronté à rien.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    fautes = []
    strat = decision["strategie"]
    uj = [t for t in trades if t.get("comptabilite") == C.UN_JETON]
    if len(uj) != 1:
        fautes.append("le rejeu rend %d vente(s) en un jeton pour %s, attendu exactement une" % (len(uj), strat))
        return None, None, fautes
    rempl = uj[0]
    if rempl["valeur"] != decision["valeur_nommee_par_la_decision"]:
        fautes.append("la règle donne %s, la décision %s nomme %s : rien n'est corrigé"
                      % (rempl["valeur"], decision["action"], decision["valeur_nommee_par_la_decision"]))
    if rempl["valeur"] == decision["valeur_retiree"]:
        fautes.append("la règle donne la valeur retirée elle-même (%s) : il n'y a rien à corriger" % rempl["valeur"])
    cand = [l for l in journal if l.get("strategie") == strat and l.get("comptabilite") == C.UN_JETON
            and l.get("valeur") == decision["valeur_retiree"] and l.get("date_entree") == rempl["date_entree"]]
    if len(cand) != 1:
        fautes.append("le journal porte %d ligne(s) un jeton %s %s achetée(s) le %s, attendu exactement une"
                      % (len(cand), strat, decision["valeur_retiree"], rempl["date_entree"]))
        return None, rempl, fautes
    retiree = cand[0]
    chiffres = ("date_entree", "prix_entree", "date_sortie", "prix_sortie", "motif_sortie", "pnl_net_eur",
                "prix_sortie_convention", "pnl_net_convention_eur", "bareme_reel", "bareme_convention")
    for t in trades:
        if t.get("comptabilite") != C.JETONS_ILLIMITES:
            continue
        j = [l for l in journal if l.get("strategie") == strat and l.get("comptabilite") == C.JETONS_ILLIMITES
             and l.get("valeur") == t["valeur"] and l.get("date_entree") == t["date_entree"]]
        if len(j) != 1:
            fautes.append("vente rejouée en jetons illimités %s achetée le %s : %d ligne(s) au journal, attendu une"
                          % (t["valeur"], t["date_entree"], len(j)))
            continue
        # vendue depuis la mise en service du barème réel : tout se compare, barème compris ; vendue avant, le journal
        # porte un barème historique que le rejeu ne reprend pas : les prix, les jours et le motif seulement
        avant = (j[0].get("date_sortie") or "") < C.MISE_EN_SERVICE_DU_BAREME_REEL
        cols = chiffres[:5] if avant else chiffres
        ecarts = [c for c in cols if (j[0].get(c) or "") != (t.get(c) or "")]
        if ecarts:
            fautes.append("jetons illimités %s du %s : le rejeu diffère du journal sur %s (%s)" % (
                t["valeur"], t["date_entree"], ", ".join(ecarts),
                "; ".join("%s journal %r / rejeu %r" % (c, j[0].get(c), t.get(c)) for c in ecarts)))
    jumeau = [t for t in trades if t.get("comptabilite") == C.JETONS_ILLIMITES and t["valeur"] == rempl["valeur"]
              and t["date_entree"] == rempl["date_entree"]]
    if len(jumeau) != 1 or any((jumeau[0].get(c) or "") != (rempl.get(c) or "") for c in chiffres):
        fautes.append("le remplacement un jeton %s n'a pas son jumeau identique en jetons illimités dans le rejeu"
                      % rempl["valeur"])
    autres = [("journal", l) for l in journal if l is not retiree] + [("positions", p) for p in positions_ouvertes]
    for ou, l in autres:
        if l.get("strategie") != strat or l.get("comptabilite") != C.UN_JETON:
            continue
        d = l.get("date_entree") or ""
        if decision["seance_du_signal"] < d <= rempl["date_sortie"]:
            fautes.append("%s : achat un jeton %s %s le %s pendant la position de remplacement (%s → %s) : la suite "
                          "des comptes un jeton changerait, à rejouer" % (ou, strat, l.get("valeur"), d,
                                                                         rempl["date_entree"], rempl["date_sortie"]))
    return retiree, rempl, fautes


def lignes_de_correction(decision, retiree, remplacement):
    """Fabrique les deux lignes du fichier des corrections : la ligne retirée, recopiée, et le remplacement calculé.

    ① RÔLE — Donner au fichier ses deux lignes, aux colonnes du contrat CORRECTION_UN_JETON.
    ② CONTEXTE D'APPEL — `calculer`.
    ③ ENTRÉE — `decision` : une entrée de `CORRECTIONS_UN_JETON_DECIDEES` · `retiree` : la ligne du journal retirée ·
      `remplacement` : la ligne rendue par `cloturer` dans le rejeu.
    ④ CONDITIONS D'ENTRÉE — Les deux portent les colonnes du contrat TRADE.
    ⑤ SORTIE — UNE valeur : une liste de deux dictionnaires, la retirée d'abord.
      [rend: 1]
    ⑥ TRAITEMENT — Recopier chaque colonne TRADE de chacune, sans rien changer ; ajouter l'action, le geste et une
      cause en une phrase qui cite la décision.
    ⑦ UNITÉ — Textes tels qu'écrits.
    ⑧ POURQUOI — La ligne retirée est recopiée à l'octet pour que la mesure la retrouve champ pour champ au journal.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main ; lève KeyError si une colonne manque.
      [sort: non]
    """
    cause_r = ("%s : achat %s retiré des comptes un jeton, ligne gardée au journal ; la règle R-207bis (CCI le plus "
               "bas) donnait %s le soir du %s. Décision : %s" % (
                   decision["action"], retiree["valeur"], remplacement["valeur"], decision["seance_du_signal"],
                   decision["decision"]))
    cause_a = ("%s : achat %s que la règle R-207bis donnait le soir du %s, rejoué par TENIR_LES_POSITIONS.tenir "
               "(programmes/CORRIGER_LES_COMPTES_UN_JETON.py), à la place de l'achat %s" % (
                   decision["action"], remplacement["valeur"], decision["seance_du_signal"], retiree["valeur"]))
    out = []
    for geste, ligne, cause in ((C.GESTE_RETIREE, retiree, cause_r), (C.GESTE_AJOUTEE, remplacement, cause_a)):
        d = {"action": decision["action"], "geste": geste}
        d.update({c: ligne[c] for c in C.TRADE})
        d["cause"] = cause
        out.append(d)
    return out


def en_texte(lignes):
    """Rend le texte exact du fichier des corrections pour ces lignes.

    ① RÔLE — Une seule forme d'écriture, pour écrire et pour comparer à l'octet.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `lignes` : les dictionnaires aux colonnes CORRECTION_UN_JETON.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte, en-tête compris, fins de ligne « \\n ».
      [rend: 1]
    ⑥ TRAITEMENT — `csv.DictWriter` sur les colonnes du contrat, guillemets au besoin.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — `--verifier` compare des octets, pas des valeurs relues.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=C.CORRECTION_UN_JETON, lineterminator="\n")
    w.writeheader()
    for l in lignes:
        w.writerow(l)
    return buf.getvalue()


def calculer(racine):
    """Calcule les lignes du fichier des corrections pour toutes les décisions déclarées.

    ① RÔLE — Enchaîner rejeu, confrontation et fabrication, décision par décision.
    ② CONTEXTE D'APPEL — `main` ; l'épreuve.
    ③ ENTRÉE — `racine` : la racine du dépôt.
    ④ CONDITIONS D'ENTRÉE — Celles du programme.
    ⑤ SORTIE — DEUX valeurs : la liste des lignes (deux par décision) ; la liste des fautes, vide si tout tient.
      [rend: 2]
    ⑥ TRAITEMENT — Lire le journal et les positions ouvertes ; pour chaque décision, `rejouer_la_decision`, refuser
      s'il reste une position ouverte née de ces signaux, `confronter`, puis `lignes_de_correction`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main ; laisse remonter `CalculImpossible`, et lève `CalculImpossible` si le journal ou les
      positions ne se lisent pas (OSError).
      [sort: non]
    """
    try:
        journal = _lire_csv(os.path.join(racine, "donnees", "claude_journal_trades.csv"))
        positions = _lire_csv(os.path.join(racine, "donnees", "claude_positions_ouvertes.csv"))
    except OSError as e:
        raise CalculImpossible("journal ou positions illisibles : %s" % e)
    lignes, fautes = [], []
    for decision in C.CORRECTIONS_UN_JETON_DECIDEES:
        trades, incidents, ouvertes = rejouer_la_decision(racine, decision)
        for x in incidents:
            print("   incident du rejeu %s : %s" % (decision["action"], x))
        if ouvertes:
            fautes.append("%s : %d position(s) née(s) des signaux du %s encore ouverte(s) à la dernière séance"
                          % (decision["action"], len(ouvertes), decision["seance_du_signal"]))
        retiree, rempl, f = confronter(decision, journal, positions, trades)
        fautes += ["%s : %s" % (decision["action"], x) for x in f]
        if not f and retiree and rempl:
            lignes += lignes_de_correction(decision, retiree, rempl)
    return lignes, fautes


def main(argv=None):
    """Écrit le fichier des corrections, ou le vérifie ; rend le code de sortie.

    ① RÔLE — Le point d'entrée en ligne de commande.
    ② CONTEXTE D'APPEL — Lancé à la main ; l'épreuve le lance en sous-processus.
    ③ ENTRÉE — `argv` : les mots de la ligne de commande sans le nom du programme (None : `sys.argv[1:]`) — la racine
      et, facultative, `--verifier`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le code, 0, 1 ou 2 (voir le ⑤ de l'en-tête).
      [rend: 1]
    ⑥ TRAITEMENT — ① `calculer` (code 2 si `CalculImpossible`) · ② une faute : l'afficher, code 1, rien n'est écrit ·
      ③ `--verifier` : comparer le texte calculé au fichier déposé, à l'octet (absent : code 2) · ④ sinon : écrire si
      le fichier n'existe pas, ne rien faire s'il est identique, refuser (code 1) s'il diffère.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un fichier de corrections qui diffère du calcul ne s'écrase jamais en silence : il a peut-être été
      relu et accepté ; c'est à un humain de trancher.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche ; écrit au plus un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    argv = list(sys.argv[1:] if argv is None else argv)
    verifier = "--verifier" in argv
    args = [a for a in argv if not a.startswith("--")]
    racine = os.path.realpath(args[0] if args else ".")
    dest = os.path.join(racine, C.CORRECTIONS_UN_JETON)
    print("CORRIGER LES COMPTES UN JETON — %d décision(s) déclarée(s) · racine %s%s"
          % (len(C.CORRECTIONS_UN_JETON_DECIDEES), racine, " · --verifier" if verifier else ""))
    try:
        lignes, fautes = calculer(racine)
    except CalculImpossible as e:
        print("CODE 2 — LE CALCUL N'A PAS PU TOURNER : %s" % e)
        return 2
    if fautes:
        print("CODE 1 — CORRECTION REFUSÉE, rien n'est écrit :")
        for x in fautes:
            print("   ❌ " + x)
        return 1
    for l in lignes:
        print("   %s %s · %s %s · entrée %s à %s · sortie %s à %s (%s) · net réel %s · net convention %s · barème %s"
              % (l["action"], l["geste"], l["strategie"], l["valeur"], l["date_entree"], l["prix_entree"],
                 l["date_sortie"], l["prix_sortie"], l["motif_sortie"], l["pnl_net_eur"],
                 l["pnl_net_convention_eur"], l["bareme_reel"]))
    texte = en_texte(lignes)
    existant = None
    if os.path.exists(dest):
        with open(dest, encoding="utf-8", newline="") as f:
            existant = f.read()
    if verifier:
        if existant is None:
            print("CODE 2 — %s absent : rien à vérifier" % C.CORRECTIONS_UN_JETON)
            return 2
        if existant != texte:
            print("CODE 1 — %s DIFFÈRE du calcul" % C.CORRECTIONS_UN_JETON)
            return 1
        print("VÉRIFIÉ — %s identique au calcul, à l'octet" % C.CORRECTIONS_UN_JETON)
        return 0
    if existant is not None:
        if existant == texte:
            print("DÉJÀ À JOUR — %s identique au calcul, rien n'est écrit" % C.CORRECTIONS_UN_JETON)
            return 0
        print("CODE 1 — %s existe et DIFFÈRE du calcul : il n'est pas écrasé (à trancher par un humain)"
              % C.CORRECTIONS_UN_JETON)
        return 1
    with open(dest, "w", encoding="utf-8", newline="") as f:
        f.write(texte)
    print("ÉCRIT — %s (%d ligne(s))" % (C.CORRECTIONS_UN_JETON, len(lignes)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
