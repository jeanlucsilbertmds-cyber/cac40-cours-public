#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONTROLER_LES_CAUSES_DES_TROUS.py — Sam 31-10-2026 (Paris) — PROPOSÉ, non validé (A-633, décision de Jean-Luc du
31-10-2026 à 21h08, annexe n°48). Simulation uniquement.

① RÔLE — Dire, pour l'historique des 20 ans, si CHAQUE séance de Bourse où une valeur n'a pas de cours porte une cause
  prouvée, prise dans une liste fermée, et rougir sinon. Un trou compté n'est pas un trou expliqué.
② CONTEXTE D'APPEL — À la main, après programmes/REPARER_L_HISTORIQUE_LONG.py et avec
  programmes/CONTROLER_L_HISTORIQUE_LONG.py : python3 programmes/CONTROLER_LES_CAUSES_DES_TROUS.py <racine>
  [fichier de cours]. Aucun circuit ne le lance encore (le circuit du soir : BACKLOG). Ses épreuves :
  tests/EPREUVES_DES_CAUSES_DES_TROUS_Sam_31-10-2026.py.
③ ENTRÉE — La racine du dépôt ; facultatif, le fichier de cours à contrôler, depuis la racine (par défaut, l'historique
  long réparé, `K.FICHIER`).
④ CONDITIONS D'ENTRÉE — Sous la racine : le fichier de cours (huit colonnes, `K.lire_cours`), le calendrier officiel
  (`K.CAL.lire_les_seances`) et la table des causes donnees/CAUSES_DES_SEANCES_SANS_COURS.csv (contrat
  CAUSES_DES_SEANCES_SANS_COURS : valeur, debut, fin, cause, preuve, sources_cherchees).  Et ce que le lecteur unique
  programmes/LIRE_LES_COURS.py lit (référentiel, table des passages dans le CAC 40, identités, nature des trous) :
  `passages_par_valeur` l'appelle.
⑤ SORTIE — UNE valeur : le code de sortie. 0 = chaque séance sans cours a une cause et une seule, prouvée, et chaque
  ligne de la table sert · 1 = au moins un cas (chaque ligne de cause fausse affichée, puis huit séances au plus, et
  le compte) · 2 = le contrôle n'a pas pu
  tourner (fichier absent ou illisible, en-tête faux, erreur imprévue) — jamais 0 dans ce cas (R-734).
⑥ TRAITEMENT — ① lire le fichier, le calendrier, la table · ② les séances à couvrir : chaque séance du calendrier
  officiel entre la première et la dernière date du fichier (`K.calendrier`), pour chaque valeur du fichier ·
  ③ `cas_des_causes` : chaque séance sans cours doit être couverte par une ligne et une seule ; chaque ligne doit avoir
  une cause de CAUSES_DES_TROUS, des dates lisibles dans l'ordre, une preuve, et, pour « source perdue », les sources
  cherchées, et n'être pas contredite par les fichiers du dépôt (première et dernière barre, passages dans le CAC 40 ;
  « hors indice » sur une valeur sans aucune période connue est refusé, non vérifiable) ; une ligne ne doit couvrir AUCUNE séance où la valeur a un cours, et au moins une séance · ④ afficher et
  rendre le code.
⑦ UNITÉ — Des SÉANCES ; des dates AAAA-MM-JJ.
⑧ POURQUOI — Décision de Jean-Luc du 31-10-2026 à 21h08 (« 1 ») : « chaque séance manquante porte sa cause prouvée,
  sinon le contrôle rougit ». Le même soir, 2 582 séances avaient été laissées vides alors que le cours de Paris était
  dans nos fichiers (annexe n°47) ; les contrôles vérifiaient ce qui est DANS le fichier et comptaient ce qui manque,
  aucun ne demandait la cause de chaque manque. Une ligne de cause qui couvre une séance pourvue est refusée : quand un
  trou est comblé, sa cause doit partir, sinon la table ment sans bruit.
⑨ CE QUI CLOCHE — La preuve n'est pas lue : « x » passe ; seules trois causes se confrontent aux fichiers (pas encore
  cotée, plus cotée, hors indice) ; « suspension » et « source perdue » reposent sur la preuve écrite (comme la preuve d'un fichier écrit à la main au registre de
  provenance, K23). · Les fichiers nommés dans une preuve ne sont pas confrontés au dépôt : la preuve est un texte
  libre, et on ne cherche pas de chemin dans un texte libre (décision de Jean-Luc du 19-10-2026 à 08h23 : « Une
  colonne à part pour les fichiers cités … sans rien deviner ») ; un fichier cité renommé ou supprimé passe sans bruit.
  · La table des causes n'est pas inscrite au registre de provenance (donnees/PROVENANCE_DES_FICHIERS.csv) : une
  modification de la table passe sans bruit. Ces deux limites vont ensemble au BACKLOG (une colonne `fichiers_cites`,
  question à Jean-Luc ; superviseur R-759 du 01-11-2026, e). · Une valeur absente de tout le fichier n'a pas de séance à couvrir : l'univers est celui du fichier
  (ArcelorMittal, hors univers par décision du 13-09-2026, n'y est pas). · Les séances du calendrier avant la première
  date et après la dernière date du fichier ne sont pas couvertes. · La règle n'est pas encore écrite au REGISTRE
  (annexe n°48 : « LA RÈGLE À ÉCRIRE AU REGISTRE », avec R-109 et R-112) → BACKLOG.
⑩ EFFET — Lit trois fichiers ; écrit seulement à l'écran.
⑪ TERMINAISON — Rend la main : chaque boucle parcourt un nombre fini de séances et de lignes. Aucun de mes appels ne
  peut ne pas revenir.
"""
import bisect, csv, datetime, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CONTROLER_L_HISTORIQUE_LONG as K     # la lecture des cours et le calendrier, une seule façon (R-708)
import LIRE_LES_COURS as M                   # le lecteur unique : les passages dans le CAC 40, par mnémonique (R-708)
from CONTRATS_DES_FICHIERS import CAUSES_DES_SEANCES_SANS_COURS, CAUSES_DES_TROUS

CAUSES = os.path.join("donnees", "CAUSES_DES_SEANCES_SANS_COURS.csv")
SOURCE_PERDUE = "source perdue"      # la seule cause qui exige les sources cherchées (annexe n°48)
PAS_ENCORE, PLUS_COTEE, HORS_INDICE = "pas encore cotée", "plus cotée", "hors indice"   # les causes qui se vérifient
assert {SOURCE_PERDUE, PAS_ENCORE, PLUS_COTEE, HORS_INDICE} <= set(CAUSES_DES_TROUS)


def lire_les_causes(chemin):
    """Lit la table des causes ; rend ses lignes.

    ① RÔLE — Lire donnees/CAUSES_DES_SEANCES_SANS_COURS.csv, contre son contrat.
    ② CONTEXTE D'APPEL — `main` ; les épreuves.
    ③ ENTRÉE — `chemin` : le fichier.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe (OSError sinon).
    ⑤ SORTIE — UNE valeur : la liste des lignes, des dictionnaires aux colonnes du contrat, chacun avec son numéro de
      ligne (« n »). Lève ValueError si l'en-tête n'est pas le contrat.
      [rend: 1]
    ⑥ TRAITEMENT — Lire.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un en-tête faux ferait lire des colonnes vides comme des causes absentes : il arrête (code 2).
    ⑨ CE QUI CLOCHE — Le contenu des lignes est jugé par `cas_des_causes`, pas ici.
    ⑩ EFFET — Lit le fichier.
    ⑪ TERMINAISON — Rend la main ou lève. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    with open(chemin, encoding="utf-8", newline="") as f:
        lecteur = csv.DictReader(f)
        if lecteur.fieldnames != CAUSES_DES_SEANCES_SANS_COURS:
            raise ValueError(f"{chemin} : en-tête {lecteur.fieldnames} au lieu de {CAUSES_DES_SEANCES_SANS_COURS}")
        return [dict(r, n=n) for n, r in enumerate(lecteur, start=2)]


def passages_par_valeur(racine, fichier):
    """Rend, pour chaque valeur du fichier, ses périodes dans le CAC 40, lues par le lecteur unique.

    ① RÔLE — Donner à `cas_des_causes` de quoi contredire une cause « hors indice ».
    ② CONTEXTE D'APPEL — `main` ; les épreuves.
    ③ ENTRÉE — `racine` : la racine du dépôt · `fichier` : le fichier de cours, depuis la racine.
    ④ CONDITIONS D'ENTRÉE — Ce que `LIRE_LES_COURS.lire` exige (référentiel, table des passages, calendrier).
    ⑤ SORTIE — UNE valeur : valeur (le nom écrit dans le fichier) → liste de (début, fin) en AAAA-MM-JJ, fin None pour
      une période ouverte ; une valeur que le lecteur ne relie à aucun mnémonique est absente, et `cas_des_causes`
      refuse alors toute cause « hors indice » sur elle (non vérifiable). Lève ce que `lire` lève.
      [rend: 1]
    ⑥ TRAITEMENT — `M.lire` ; pour chaque mnémonique, chaque nom écrit qu'il a rencontré reçoit ses périodes
      (« dans_l_indice », tirées de donnees/sources_indice/PASSAGES_DANS_LE_CAC40.csv).
    ⑦ UNITÉ — Des dates.
    ⑧ POURQUOI — Relecture du lot de comblement (31-10-2026, D3) : une cause « hors indice » écrite sur LVMH, qui est au
      CAC 40 tout le temps, passait ; la table des passages est au dépôt, un programme la lit (R-754).
    ⑨ CE QUI CLOCHE — Les périodes sont celles du lecteur unique : une table des passages fausse rend un verdict faux.
    ⑩ EFFET — Lit les fichiers du lecteur.
    ⑪ TERMINAISON — Rend la main ou lève. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    lu = M.lire(racine, fichier, None)
    sortie = {}
    for m, noms in lu["ecritures"].items():
        for nom in noms:
            sortie[nom] = [(a.isoformat(), b.isoformat() if b else None) for a, b in lu["dans_l_indice"].get(m, [])]
    return sortie


def cas_des_causes(series, cal, causes, passages):
    """Rend les cas : séances sans cours sans cause, ou à deux causes, et lignes de cause fausses ou inutiles.

    ① RÔLE — Le contrôle lui-même, sans lecture de fichier, pour qu'une épreuve le joue sur des données fabriquées.
    ② CONTEXTE D'APPEL — `main` ; les épreuves.
    ③ ENTRÉE — `series` : valeur → {date : barre} (`K.lire_cours`) · `cal` : les séances à couvrir, triées (AAAA-MM-JJ)
      · `causes` : `lire_les_causes` · `passages` : `passages_par_valeur` (depuis la relecture du 31-10-2026, D3).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste triée des cas, un texte chacun ; vide si tout est couvert et prouvé.
      [rend: 1]
    ⑥ TRAITEMENT — ① chaque ligne : valeur connue du fichier, dates lisibles et dans l'ordre, cause de
      CAUSES_DES_TROUS, preuve non vide, sources cherchées non vides pour SOURCE_PERDUE ; et la cause n'est pas
      contredite par les fichiers du dépôt : « pas encore cotée » finit avant la première barre de la valeur, « plus
      cotée » commence après sa dernière, « hors indice » ne recouvre aucune période de la valeur dans le CAC 40
      (`passages`), et une valeur sans aucune période connue rend « hors indice » NON VÉRIFIABLE, donc refusé ;
      sinon un cas, et la ligne ne couvre rien · ② chaque ligne valable : les séances de `cal` entre ses deux dates ; aucune → un cas ; celles où
      la valeur a un cours → un cas (la ligne et le compte) · ③ chaque valeur, chaque séance de `cal` sans cours : zéro
      ligne valable qui la couvre → « SANS CAUSE » ; deux ou plus → « DEUX CAUSES ».
    ⑦ UNITÉ — Des séances.
    ⑧ POURQUOI — ⑧ du programme. Une séance couverte par deux lignes dirait deux vérités : refusée, comme un doublon.
      Le contrôle se FERME quand il lui manque sa donnée : jusqu'au 01-11-2026, `passages.get(valeur, [])` lisait
      « aucune période » comme « rien ne contredit », et un `main` qui ne passait plus les passages acceptait un
      « hors indice » sur LVMH avec le code 0 (relecture du tour 2, N1 ; superviseur R-759 du 01-11-2026, a′ ; un
      contrôle qui n'a pas pu tourner ne rend pas 0, R-734).
    ⑨ CE QUI CLOCHE — Une ligne fausse ne couvre rien : ses séances sortent aussi « SANS CAUSE » — deux cas pour une
      faute, jamais zéro.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main. Aucun de mes appels ne peut ne pas revenir.
      [sort: non]
    """
    cas, couvre = [], {}
    for r in causes:
        ici = f"ligne {r['n']} ({r['valeur']} {r['debut']} → {r['fin']}, « {r['cause']} »)"
        try:
            a, z = (datetime.date.fromisoformat(r[c]).isoformat() for c in ("debut", "fin"))
            dates_ok = a == r["debut"] and z == r["fin"] and a <= z
        except ValueError:
            dates_ok = False
        faute = ("valeur absente du fichier" if r["valeur"] not in series
                 else "dates illisibles ou dans le désordre" if not dates_ok
                 else f"cause hors de la liste fermée {list(CAUSES_DES_TROUS)}" if r["cause"] not in CAUSES_DES_TROUS
                 else "sans preuve" if not r["preuve"].strip()
                 else "« source perdue » sans les sources cherchées" if r["cause"] == SOURCE_PERDUE
                 and not r["sources_cherchees"].strip() else "")
        if not faute and series[r["valeur"]]:
            premiere, derniere = min(series[r["valeur"]]), max(series[r["valeur"]])
            periodes = passages.get(r["valeur"]) or []
            dedans = [(x, y) for x, y in periodes if x <= r["fin"] and (y is None or r["debut"] <= y)]
            faute = (f"« pas encore cotée » contredit : la première barre est le {premiere}"
                     if r["cause"] == PAS_ENCORE and r["fin"] >= premiere
                     else f"« plus cotée » contredit : la dernière barre est le {derniere}"
                     if r["cause"] == PLUS_COTEE and r["debut"] <= derniere
                     # fermé quand la donnée manque (superviseur R-759 du 01-11-2026, a′) : sans période connue, rien
                     # ne peut contredire la cause, donc rien ne la prouve non plus
                     else "« hors indice » non vérifiable : aucune période connue de la valeur dans le CAC 40"
                     if r["cause"] == HORS_INDICE and not periodes
                     else f"« hors indice » contredit par la table des passages dans le CAC 40 : {dedans[:2]}"
                     if r["cause"] == HORS_INDICE and dedans else "")
        if faute:
            cas.append(f"{ici} : {faute}")
            continue
        jours = cal[bisect.bisect_left(cal, a): bisect.bisect_right(cal, z)]
        pourvues = [d for d in jours if d in series[r["valeur"]]]
        if not jours:
            cas.append(f"{ici} : ne couvre aucune séance du calendrier")
        if pourvues:
            cas.append(f"{ici} : couvre {len(pourvues)} séance(s) où la valeur a un cours, dont {pourvues[:3]} — une "
                       f"cause ne vit que sur un trou")
        for d in jours:
            couvre.setdefault((r["valeur"], d), []).append(r["n"])
    for v in sorted(series):
        for d in cal:
            if d in series[v]:
                continue
            n = couvre.get((v, d), [])
            if not n:
                cas.append(f"{v} {d} : séance sans cours, SANS CAUSE")
            elif len(n) > 1:
                cas.append(f"{v} {d} : séance sans cours, DEUX CAUSES (lignes {n})")
    return sorted(cas)


def main(argv):
    """Porte la ligne de commande ; rend le code de sortie.

    ① RÔLE — Lire, contrôler, afficher.
    ② CONTEXTE D'APPEL — Le bloc final ; les épreuves.
    ③ ENTRÉE — `argv` : les arguments, sans le nom du programme.
    ④ CONDITIONS D'ENTRÉE — ④ du programme.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2 (⑤ du programme).
      [rend: 1]
    ⑥ TRAITEMENT — ⑥ du programme ; chaque ligne de cause fausse affichée (une par ligne de la table au plus), puis
      huit séances au plus, et le compte du reste.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un compte sans exemple ne se vérifie pas ; une liste coupée sans le dire ment. Les lignes fausses
      d'abord (tour 3, 01-11-2026) : une ligne fausse ne couvre rien, ses séances sortent « SANS CAUSE », et, triées
      par ordre alphabétique, ces séances cachaient la ligne qui en est la cause (sous le sabotage C14, 2 101 cas, et
      les huit affichés étaient des séances).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Rend la main ; une erreur imprévue devient 2 dans le bloc final.
      [sort: non]
    """
    if not argv or not os.path.isdir(argv[0]):
        print("USAGE : CONTROLER_LES_CAUSES_DES_TROUS.py <racine> [fichier de cours]")
        return 2
    racine = argv[0]
    fichier = argv[1] if len(argv) > 1 else K.FICHIER
    try:
        series, defauts, _ = K.lire_cours(os.path.join(racine, fichier))
        if defauts:
            raise ValueError(f"{fichier} : {len(defauts)} défaut(s) de lecture, dont {defauts[0]}")
        if not series:
            raise ValueError(f"{fichier} : aucune ligne")
        cal = sorted(K.calendrier(series, K.CAL.lire_les_seances(racine)))
        causes = lire_les_causes(os.path.join(racine, CAUSES))
        passages = passages_par_valeur(racine, fichier)
    except (OSError, ValueError) as e:
        print(f"ARRÊT — le contrôle des causes n'a pas pu tourner : {type(e).__name__} : {e}")
        return 2
    sans = sum(1 for v in series for d in cal if d not in series[v])
    print(f"contrôlé : {fichier} — {len(series)} valeurs, {len(cal)} séances du calendrier, du {cal[0]} au {cal[-1]} ; "
          f"{sans} séances sans cours ; {len(causes)} lignes de cause ({CAUSES})")
    par_cause = {}
    for r in causes:
        par_cause[r["cause"]] = par_cause.get(r["cause"], 0) + 1
    print(f"lignes par cause : {dict(sorted(par_cause.items()))}")
    cas = cas_des_causes(series, cal, causes, passages)
    # les lignes de cause fausses d'abord, toutes : ce sont les causes ; les séances qui en découlent, huit au plus
    de_ligne = [c for c in cas if c.startswith("ligne ")]
    de_seance = [c for c in cas if not c.startswith("ligne ")]
    for c in de_ligne + de_seance[:8]:
        print(f"   {c}")
    if len(de_seance) > 8:
        print(f"   … et {len(de_seance) - 8} séance(s) de plus")
    print("VERDICT : " + (f"ROUGE, {len(cas)} cas" if cas else "chaque séance sans cours porte une cause prouvée"))
    return 1 if cas else 0


if __name__ == "__main__":
    try:
        code = main(sys.argv[1:])
    except Exception as e:
        print(f"ARRÊT — erreur imprévue {type(e).__name__} : {e}")
        code = 2
    sys.exit(code)
