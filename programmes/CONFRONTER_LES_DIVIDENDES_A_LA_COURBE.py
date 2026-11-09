#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONFRONTER_LES_DIVIDENDES_A_LA_COURBE.py — Jeu 05-11-2026 (Paris). Simulation uniquement.

① RÔLE — SIGNALER, sans rien décider, l'écart entre chaque dividende de la table (donnees/TABLE_DES_DIVIDENDES.csv) et
  la baisse d'ouverture observée le jour de son détachement dans une courbe de cours ; puis, par année et par source
  des barres de la courbe, le rapport « baisse observée moyenne ÷ baisse attendue moyenne », et la part des
  dividendes où la courbe ne baisse pas (baisse observée plus proche de zéro que de la baisse attendue), avec la même
  mesure à la séance d'avant comme témoin : « avec le mouvement de la séance d'avant, un dividende ENTIER sortirait-il
  sans baisse ? ». Il dit enfin ce qu'il ne peut pas vérifier, et pourquoi, et la partie de la courbe que la table ne
  couvre pas (séances d'une valeur après le dernier jour couvert par la source de la table, colonne couverte_jusqu_au).
② CONTEXTE D'APPEL — À la main par le Chat, ou par l'épreuve de la table
  (tests/EPREUVES_DE_LA_TABLE_DES_DIVIDENDES_Jeu_05-11-2026.py, E12). Commande :
  python3 programmes/CONFRONTER_LES_DIVIDENDES_A_LA_COURBE.py <racine> <table> <courbe>
  <table> et <courbe> sont relatifs à la racine. Aucune valeur par défaut : la courbe que lit le juge des stratégies
  est donnees/cours_maitre.csv (`fichiers_de_cours` de programmes/JUGE_DES_STRATEGIES.py) ; l'essai sur vingt ans lit
  donnees/sources_yahoo/historique_long_repare.csv (option --cours= du juge). Aucune tâche du soir ne l'appelle.
③ ENTRÉE — La table des dividendes ; la courbe, lue par le lecteur unique des cours (`LIRE_LES_COURS.lire`, R-111),
  qui connaît les mnémoniques et le calendrier des séances.
④ CONDITIONS D'ENTRÉE — L'en-tête de la table est TABLE_DES_DIVIDENDES (programmes/FABRIQUER_LA_TABLE_DES_DIVIDENDES.py,
  en attendant le contrat du lot C) ; la courbe se lit par `LIRE_LES_COURS.lire`.
⑤ SORTIE — Le code de sortie, UNE valeur : 0 si la confrontation a pu être faite (quels que soient les écarts : ils
  sont signalés, jamais jugés) ; 1 « REFUSÉ » si la table n'a pas l'en-tête attendu ; 2 « IMPOSSIBLE » si le
  programme n'a pas pu tourner (arguments, fichier absent, lecture refusée). À l'écran : la courbe et son empreinte,
  les comptes, la partie de la courbe non couverte par la table (valeurs, dates, nombre de séances), le tableau par
  année et source, puis la liste des écarts du plus grand au plus petit.
  [rend: 1]
⑥ TRAITEMENT — ① lire la table et la courbe · ② pour chaque ligne : la veille est la séance du calendrier qui
  précède la date de détachement ; baisse observée = ouverture du jour ÷ clôture de la veille − 1 ; baisse attendue
  = −rendement ; témoin = la même mesure à la séance d'avant · ③ une ligne qui ne se mesure pas reçoit sa raison
  (RAISONS) · ④ pour chaque valeur de la courbe, compter ses séances après le dernier jour que la table couvre pour
  elle (le plus tard de ses couverte_jusqu_au ; toute la courbe si la table n'a aucune ligne d'elle) · ⑤ regrouper
  par année et par source de la barre du jour · ⑥ afficher. Les séances sont celles de R-110 (`CAL.seances_entre`) :
  constatées par l'indice, puis prévues par Euronext au-delà de son dernier jour (02-10-2026).
⑦ UNITÉ — Fractions dans le calcul ; points de pourcentage à l'affichage ; dates AAAA-MM-JJ.
⑧ POURQUOI — Superviseur R-759 du 05-11-2026 (« ARRÊTER ET SIMPLIFIER ») : le statut CONFIRMÉE / CONTREDITE, ligne
  par ligne, se trompait environ une fois sur quatre (un jour sans dividende sortait CONFIRMÉE dans 22 à 24 % des
  cas, placebo du relecteur ; deux vrais dividendes récents, Engie 30-04-2026 et EssilorLuxottica 05-05-2026, sortaient
  CONTREDITE) ; le vrai signal est une propriété d'ÉPOQUE (rapport des moyennes 0,90 sur 2024-2026, 0,29 à 0,72 chaque
  année de 2000 à 2008). Décision de Jean-Luc du 05-11-2026 à 14h22, « 1 » (Q-DIV5) : les dividendes sont pris tels
  quels, les écarts SIGNALÉS, jamais corrigés. Ce programme n'écrit donc rien que `jouer` lise. Le témoin à la séance
  d'avant donne la part attendue « par hasard » : sans lui, une part de « courbe qui ne baisse pas » ne se lit pas.
  Superviseur R-759 du 05-11-2026, avant le tour 3 (T2, T3) : le témoin du tour 2 demandait « un jour SANS dividende
  sort-il sans baisse ? » (87,8 % sur la courbe du juge), un chiffre qui ne se compare pas aux 15,6 % « sans baisse »
  du jour du détachement ; le bon témoin ajoute le dividende entier au mouvement de la séance d'avant,
  ne_baisse_pas(témoin + attendue, attendue), et se lit directement à côté (environ 12 % mesurés par le relecteur).
  Même superviseur (T1) : la table ne couvre pas toute la courbe du juge (elle s'arrête au relevé de Yahoo du
  21-10-2026, la courbe au 04-11-2026) ; ce qui n'est pas couvert est signalé, pas tu.
⑨ CE QUI CLOCHE — La baisse d'ouverture contient le mouvement du marché de la nuit : l'indice n'a pas d'ouverture au
  dépôt, elle n'en est pas corrigée. · Une courbe déjà corrigée des dividendes (ce que R-108 ② interdit) se verrait
  comme une part élevée de « courbe qui ne baisse pas » ; ce programme ne peut pas dire si un cas isolé (Engie
  30-04-2026) vient de la courbe ou du marché : il le montre, il ne conclut pas. · Le témoin à la séance d'avant
  n'est pas un jour quelconque : la veille d'un détachement peut avoir son propre mouvement ; et ajouter le dividende
  entier au mouvement d'un autre jour suppose que le bruit de la nuit est le même les deux jours. · La partie non
  couverte se compte en barres de la courbe, pas en séances du calendrier : une séance où la valeur n'a pas de barre
  n'y compte pas.
⑩ EFFET — Lit ; n'écrit aucun fichier.
⑪ TERMINAISON — Rend la main ; aucun appel réseau, aucune attente.
  [sort: oui]
"""
import bisect
import csv
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import LIRE_LES_COURS as L  # noqa: E402  le lecteur unique des cours (R-111)
import CALENDRIER_DE_LA_BOURSE as CAL  # noqa: E402  les séances de R-110, constatées puis prévues
import FABRIQUER_LA_TABLE_DES_DIVIDENDES as T  # noqa: E402  les colonnes de la table (R-708), en attendant le lot C

# Les raisons pour lesquelles une ligne ne se mesure pas, dans l'ordre où elles sont cherchées.
RAISONS = ("RENDEMENT INCONNU", "VALEUR ABSENTE DE LA COURBE", "HORS DE LA PÉRIODE DE LA COURBE",
           "BARRE DU JOUR OU DE LA VEILLE ABSENTE")


def ouverture(seances, barres, jour):
    """Rend l'écart d'ouverture d'un jour (ouverture ÷ clôture de la séance d'avant − 1) et la source de la barre.

    ① RÔLE — Mesurer la baisse d'ouverture d'une séance dans la courbe.
    ② CONTEXTE D'APPEL — `confronter`, deux fois par ligne (le jour, la séance d'avant).
    ③ ENTRÉE — `seances` : la liste triée des séances, AAAA-MM-JJ · `barres` : {AAAA-MM-JJ : la ligne lue (open,
      close, source…)} d'une valeur · `jour` : une date AAAA-MM-JJ.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : l'écart (fraction) ou None ; la source de la barre du jour (texte, « non dite » pour une
      courbe sans colonne source) ou None.
      [rend: 2]
    ⑥ TRAITEMENT — La séance d'avant se lit dans le calendrier, jamais dans les cours (R-110) : une barre qui enjambe
      un trou ne mesure rien (R-115).
    ⑦ UNITÉ — Fraction sans unité.
    ⑧ POURQUOI — R-113 : le détachement est « le jour où le cours ouvre plus bas du montant du dividende ».
    ⑨ CE QUI CLOCHE — Voir la fiche en tête : le mouvement du marché pendant la nuit n'est pas retiré.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    i = bisect.bisect_left(seances, jour)
    if i == 0 or i >= len(seances) or seances[i] != jour or jour not in barres or seances[i - 1] not in barres:
        return None, None
    b = barres[jour]
    return float(b["open"]) / float(barres[seances[i - 1]]["close"]) - 1, b.get("source") or "non dite"


def confronter(racine, table, courbe):
    """Rend la mesure de chaque ligne de la table dans la courbe.

    ① RÔLE — Le calcul entier, sans affichage.
    ② CONTEXTE D'APPEL — `main` ; l'épreuve (E12).
    ③ ENTRÉE — `racine` · `table`, `courbe` : relatifs à la racine.
    ④ CONDITIONS D'ENTRÉE — Voir la fiche en tête, ④.
    ⑤ SORTIE — DEUX valeurs : la liste des mesures, une par ligne de la table, chacune {valeur, mnemonique, source,
      date, rendement, attendue, observee, temoin, source_barre, raison} (fractions ; None quand inconnu ; `raison`
      None pour une ligne mesurée, sinon un texte de RAISONS) ; la description de la courbe {fichier, empreinte, debut,
      fin, non_couvert}, où non_couvert = {mnémonique : (première date, dernière date, nombre de barres)} pour chaque
      valeur de la courbe qui a des barres après le dernier jour que la table couvre pour elle.
      [rend: 2]
    ⑥ TRAITEMENT — Lire la table (refus si l'en-tête diffère) ; lire la courbe par `LIRE_LES_COURS.lire` ; les séances
      de R-110 du début du calendrier à la dernière barre de la courbe (au plus la fin de la liste d'Euronext) ; pour
      chaque ligne, chercher la première raison qui empêche la mesure, sinon mesurer le jour et la séance d'avant ;
      puis la partie non couverte, valeur par valeur.
    ⑦ UNITÉ — Fractions.
    ⑧ POURQUOI — Voir la fiche en tête, ⑧.
    ⑨ CE QUI CLOCHE — `LIRE_LES_COURS.lire` met à part les barres en conflit : une séance mise à part est « absente »
      ici, sans que la raison le distingue.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ; lève T.Refus (en-tête) ou l'erreur du lecteur.
      [sort: non]
    """
    with open(os.path.join(racine, table), encoding="utf-8", newline="") as f:
        lecteur = csv.DictReader(f)
        if lecteur.fieldnames != T.TABLE_DES_DIVIDENDES:
            raise T.Refus(f"{table} : en-tête {lecteur.fieldnames} au lieu de {T.TABLE_DES_DIVIDENDES}")
        lignes = list(lecteur)
    lu = L.lire(racine, courbe)
    sc = lu["seances"]
    barres = {m: {d.isoformat(): b for d, b in parm.items()} for m, parm in lu["barres"].items()}
    debut, fin = lu["debut"].isoformat(), max(max(b) for b in barres.values()) if barres else ""
    jusqu = min(max(max(parm) for parm in lu["barres"].values()), sc["euronext"]["jusqu_au"]) if barres else sc["fin"]
    seances = [d.isoformat() for d, _ in CAL.seances_entre(sc["debut"], jusqu, sc)]
    out = []
    for r in lignes:
        x = {"valeur": r["valeur"], "mnemonique": r["mnemonique"], "source": r["source"],
             "date": r["date_detachement"], "rendement": float(r["rendement"]) if r["rendement"] else None,
             "attendue": None, "observee": None, "temoin": None, "source_barre": None, "raison": None}
        b = barres.get(r["mnemonique"], {})
        if x["rendement"] is None:
            x["raison"] = RAISONS[0]
        elif not b:
            x["raison"] = RAISONS[1]
        elif not (debut < x["date"] <= fin):
            x["raison"] = RAISONS[2]
        else:
            x["observee"], x["source_barre"] = ouverture(seances, b, x["date"])
            if x["observee"] is None:
                x["raison"] = RAISONS[3]
            else:
                x["attendue"] = -x["rendement"]
                i = bisect.bisect_left(seances, x["date"])
                x["temoin"] = ouverture(seances, b, seances[i - 1])[0] if i > 0 else None
        out.append(x)
    couverture = {}
    for r in lignes:
        couverture[r["mnemonique"]] = max(couverture.get(r["mnemonique"], ""), r["couverte_jusqu_au"])
    non_couvert = {}
    for m, b in sorted(barres.items()):
        apres = sorted(d for d in b if d > couverture.get(m, ""))
        if apres:
            non_couvert[m] = (apres[0], apres[-1], len(apres))
    empreinte = hashlib.sha256(open(os.path.join(racine, courbe), "rb").read()).hexdigest()
    return out, {"fichier": courbe.replace(os.sep, "/"), "empreinte": empreinte, "debut": debut, "fin": fin,
                 "non_couvert": non_couvert}


def ne_baisse_pas(observee, attendue):
    """Dit si la courbe ne montre pas la baisse : l'écart observé est au moins aussi proche de zéro que de la baisse
    attendue.

    ① RÔLE — Compter, sans décider, les dividendes que la courbe ne montre pas.
    ② CONTEXTE D'APPEL — `resumer`, pour le jour et pour le témoin.
    ③ ENTRÉE — `observee`, `attendue` : fractions (attendue < 0).
    ④ CONDITIONS D'ENTRÉE — Les deux sont connues.
    ⑤ SORTIE — UNE valeur : vrai ou faux.
      [rend: 1]
    ⑥ TRAITEMENT — |observée| ≤ |observée − attendue| : le point milieu entre « rien » et « le dividende ».
    ⑦ UNITÉ — Fractions.
    ⑧ POURQUOI — Aucun seuil écrit dans le code (règle commune aux lots de D) ; le point milieu est la seule frontière
      qui ne se choisit pas. Elle ne sert qu'à COMPTER : ce n'est plus un statut de la table (superviseur R-759 du
      05-11-2026, D3).
    ⑨ CE QUI CLOCHE — Un jour quelconque passe cette frontière dans un sens ou dans l'autre par le seul bruit : d'où
      le témoin à la séance d'avant, mesuré de la même façon.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return abs(observee) <= abs(observee - attendue)


def resumer(mesures):
    """Regroupe les mesures par année et par source de la barre du jour.

    ① RÔLE — Montrer la propriété d'époque que la ligne à ligne ne montre pas.
    ② CONTEXTE D'APPEL — `main` ; l'épreuve (E12).
    ③ ENTRÉE — `mesures` : le premier rendu de `confronter`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : {(année, source de la barre) : {n, attendue_moy, observee_moy, rapport, sans_baisse,
      temoin_n, temoin_sans_baisse}} — moyennes en fractions, `rapport` = observée moyenne ÷ attendue moyenne,
      `sans_baisse` et `temoin_sans_baisse` en nombres de lignes.
      [rend: 1]
    ⑥ TRAITEMENT — Seules les lignes mesurées (raison None) comptent ; le témoin compte quand il se mesure : il est
      « sans baisse » quand ne_baisse_pas(témoin + attendue, attendue), c'est-à-dire quand le mouvement de la séance
      d'avant, ajouté à un dividende entier, sortirait sans baisse.
    ⑦ UNITÉ — Fractions ; nombres de lignes.
    ⑧ POURQUOI — M3 du superviseur R-759 du 05-11-2026 : le rapport des moyennes est le signal d'époque. Le témoin
      se compare directement à `sans_baisse` (superviseur avant le tour 3, T2 : l'ancien témoin, un jour sans
      dividende, ne se comparait pas).
    ⑨ CE QUI CLOCHE — Une année de peu de lignes donne un rapport instable : le nombre est affiché à côté.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    groupes = {}
    for x in mesures:
        if x["raison"] is not None:
            continue
        g = groupes.setdefault((x["date"][:4], x["source_barre"]), [])
        g.append(x)
    out = {}
    for k, xs in sorted(groupes.items()):
        att = sum(x["attendue"] for x in xs) / len(xs)
        obs = sum(x["observee"] for x in xs) / len(xs)
        tem = [x for x in xs if x["temoin"] is not None]
        out[k] = {"n": len(xs), "attendue_moy": att, "observee_moy": obs, "rapport": obs / att,
                  "sans_baisse": sum(1 for x in xs if ne_baisse_pas(x["observee"], x["attendue"])),
                  "temoin_n": len(tem), "temoin_sans_baisse": sum(1 for x in tem if ne_baisse_pas(x["temoin"] + x["attendue"], x["attendue"]))}
    return out


def main(argv):
    """Point d'entrée : confronte et affiche.

    ① RÔLE — La ligne de commande (fiche en tête, ②).
    ② CONTEXTE D'APPEL — La ligne de commande ; l'épreuve (E9, E12).
    ③ ENTRÉE — `argv` : <racine> <table> <courbe>.
    ④ CONDITIONS D'ENTRÉE — Voir la fiche en tête, ④.
    ⑤ SORTIE — UNE valeur : le code 0, 1 ou 2 (fiche en tête, ⑤).
      [rend: 1]
    ⑥ TRAITEMENT — Lire les arguments ; `confronter` (un refus rend 1, toute autre panne rend 2) ; `resumer` ; afficher.
    ⑦ UNITÉ — Points de pourcentage à l'écran.
    ⑧ POURQUOI — Un code 1 d'une erreur Python non attrapée passerait pour un refus.
    ⑨ CE QUI CLOCHE — La liste des écarts est longue (une ligne par dividende mesuré) : c'est voulu, rien n'est caché.
    ⑩ EFFET — Affiche ; n'écrit aucun fichier.
    ⑪ TERMINAISON — Rend la main ; le bas du fichier sort par sys.exit.
      [sort: non]
    """
    if len(argv) != 3 or any(a.startswith("--") for a in argv):
        print("IMPOSSIBLE : usage <racine> <table> <courbe> (aucune valeur par défaut)")
        return 2
    racine, table, courbe = argv
    try:
        mesures, c = confronter(racine, table, courbe)
    except T.Refus as e:
        print(f"REFUSÉ : {e}")
        return 1
    except Exception as e:  # toute panne rend 2
        print(f"IMPOSSIBLE : {type(e).__name__} : {e}")
        return 2
    print(f"courbe : {c['fichier']} · sha256 {c['empreinte']} · du {c['debut']} au {c['fin']}")
    print(f"table : {table} · {len(mesures)} lignes · mesurées {sum(1 for x in mesures if x['raison'] is None)}")
    print("CE QUI NE PEUT PAS ÊTRE VÉRIFIÉ : " + " · ".join(
        f"{r} {sum(1 for x in mesures if x['raison'] == r)}" for r in RAISONS))
    nc = c["non_couvert"]
    print(f"COURBE NON COUVERTE PAR LA TABLE : {len(nc)} valeur(s), {sum(n for _, _, n in nc.values())} barre(s)"
          + (f", du {min(a for a, _, _ in nc.values())} au {max(b for _, b, _ in nc.values())}" if nc else "")
          + (" : " + " · ".join(f"{m} {a}→{b} ({n})" for m, (a, b, n) in nc.items()) if nc else ""))
    print("PAR ANNÉE ET SOURCE DE LA BARRE (attendue et observée en points de % ; rapport = observée ÷ attendue ; "
          "« sans baisse » = la courbe ne montre pas la baisse ; témoin = un dividende entier ajouté au mouvement de "
          "la séance d'avant sortirait-il sans baisse ?) :")
    for (a, s), g in resumer(mesures).items():
        print(f"  {a} {s:<9} n={g['n']:>4}  attendue {100 * g['attendue_moy']:+.3f}  observée {100 * g['observee_moy']:+.3f}"
              f"  rapport {g['rapport']:.2f}  sans baisse {g['sans_baisse']:>3}  témoin sans baisse "
              f"{g['temoin_sans_baisse']:>3}/{g['temoin_n']}")
    ecarts = sorted((x for x in mesures if x["raison"] is None), key=lambda x: -abs(x["observee"] - x["attendue"]))
    print(f"ÉCARTS (baisse observée − baisse attendue, en points), {len(ecarts)} lignes, du plus grand au plus petit :")
    for x in ecarts:
        print(f"  {100 * (x['observee'] - x['attendue']):+9.4f} · {x['valeur']} · {x['date']} · attendue "
              f"{100 * x['attendue']:+.4f} · observée {100 * x['observee']:+.4f} · barre {x['source_barre']} · {x['source']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
