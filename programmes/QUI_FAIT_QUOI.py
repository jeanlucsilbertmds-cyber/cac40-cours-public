#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QUI_FAIT_QUOI.py — Ven 20-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Question de Jean-Luc du 20-11-2026 à 19h40 : « comment piloter un graphe d'actions parallèles si tu
ne sais pas qui fait quoi ? ». Le registre etudes/REGISTRE_DES_TRAVAUX/ (un fichier JSON par entrée) reçoit chaque lancement de
programmes/LIVRER.py et de programmes/INSTALLER.py, et ceux que le Chat note ici (« noter »). Ce programme le relit
et confronte chaque ligne aux sources VIVANTES, pour que l'état ne repose jamais sur la mémoire du Chat. Cas
fondateur du même jour : Cowork, lancé avant GitHub, a rejoué lui-même les épreuves longues que GitHub jouait.

① RÔLE — Dire ce qui tourne, ce qui est fini, ce qui est en DOUBLON (la même épreuve chez deux exécutants, ou deux
  passages vivants pour la même), et ce qui est INCOHÉRENT (registre contredit par GitHub ou git ; Cowork lancé avant
  la fin des épreuves de GitHub sur la même branche).
② CONTEXTE D'APPEL — À la main par le Chat, depuis son clone privé :
  python3 -B programmes/QUI_FAIT_QUOI.py [--sans-fetch]
  python3 -B programmes/QUI_FAIT_QUOI.py noter <étape> <branche> <exécutant> <identifiant> [--fini=<résultat>]
  (« noter » : le Chat écrit un lancement qu'aucun programme n'écrit, par exemple Cowork : « noter relecture
  travail-x cowork <pointe> », ou une épreuve jouée chez Cowork : « noter epreuve:CircuitPublic travail-x cowork
  <pointe> ».)
③ ENTRÉE — La ligne de commande ; les variables LIVRER_* de programmes/LIVRER.py.
④ CONDITIONS D'ENTRÉE — Lancé dans un clone git du dépôt privé ; gh autorisé.
⑤ SORTIE — Le code de sortie : 0 rien en double ni d'incohérent · 1 au moins un DOUBLON ou une INCOHÉRENCE ·
  2 registre illisible ou hors contrat · 3 « noter » refusé · 5 PLANTAGE (exception imprévue, jamais lue comme un
  verdict).
⑥ TRAITEMENT — Lire le registre sur origin/main, sur chaque origin/travail-* et dans chaque worktree local (les
  lignes en cours d'un LIVRER qui n'a pas encore poussé) ; garder la dernière ligne de chaque travail ; confronter
  (GitHub : « gh run view » ; branches : « git ls-remote » et l'histoire ; Cowork : le dernier commit d'auteur
  « cowork » de la branche) ; afficher.
⑦ UNITÉ — Heures de Paris.
⑧ POURQUOI — Voir le sens en tête. Les fonctions de registre, de git et de gh sont celles de LIVRER.py (R-708).
⑨ CE QUI CLOCHE — Une épreuve jouée par Cowork n'est vue que si le Chat la note : aucun programme ne lit encore les
  RELU pour en extraire les épreuves rejouées. Le commit « cowork » d'une branche dit qu'il a écrit, pas ce qu'il a
  joué.
⑩ EFFET — Lit GitHub et git ; « noter » commite et pousse le registre sur la branche notée (jamais main).
⑪ TERMINAISON — Sort du programme par sys.exit.
"""
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import LIVRER as L

SANS_DEFAUT, DEFAUT, ILLISIBLE, NOTE_REFUSEE = 0, 1, 2, 3


def lignes_du_registre(racine, sans_fetch):
    """Rend toutes les entrées du registre, lues sur les branches d'origin et dans les worktrees locaux, sans double.

    ① RÔLE — UN registre, même s'il vit dans plusieurs branches et disques.
    ② CONTEXTE D'APPEL — `rapport`, `noter_a_la_main`.
    ③ ENTRÉE — `racine` : le clone privé · `sans_fetch` : vrai pour ne pas lire le réseau.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des dicts (colonnes du contrat TRAVAUX), ou lève L.Arret(2).
      [rend: 1]
    ⑥ TRAITEMENT — fetch ; `LIVRER.entrees_du_registre` (le seul lecteur, R-708) pour origin/main, chaque
      origin/travail-* et le disque de chaque worktree local ; une entrée est un FICHIER : son nom la rend unique, la
      même entrée vue sur deux branches compte une fois.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les entrées d'un LIVRER en cours ne sont poussées qu'à sa fin (LIVRER.py, ⑨).
    ⑨ CE QUI CLOCHE — Une branche supprimée emporte ses entrées si elles n'ont pas été fusionnées.
    ⑩ EFFET — Lit git et le disque.
    ⑪ TERMINAISON — Rend la main, ou lève L.Arret.
      [sort: non]
    """
    if not sans_fetch:
        L.git(racine, "fetch", "-q", "origin")
    refs = ["refs/remotes/origin/main"] + [r for r in L.git(racine, "for-each-ref", "--format=%(refname)",
                                                             "refs/remotes/origin/travail-*").stdout.split() if r]
    vues, rendu = set(), []
    sources = [(r, racine, r) for r in refs]
    for l in L.git(racine, "worktree", "list", "--porcelain").stdout.splitlines():
        if l.startswith("worktree "):
            chemin = l[len("worktree "):]
            sources.append((chemin, chemin, None))
    for origine, depot, ref in sources:
        try:
            entrees = L.entrees_du_registre(depot, ref)
        except (ValueError, OSError) as e:
            raise L.Arret(ILLISIBLE, f"registre illisible dans {origine} : {e}")
        for nom, d in entrees:
            if nom not in vues:
                vues.add(nom)
                rendu.append(d)
    return rendu


def derniers_etats(lignes):
    """Rend la dernière ligne de chaque travail (étape, branche, exécutant, identifiant).

    ① RÔLE — Une ligne au lancement, une à la fin : la plus avancée fait foi.
    ② CONTEXTE D'APPEL — `rapport`.
    ③ ENTRÉE — `lignes` : les dicts du registre.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des dicts retenus, dans l'ordre de lancement.
      [rend: 1]
    ⑥ TRAITEMENT — Clé = (étape, branche, exécutant, identifiant) ; une ligne finie l'emporte sur une non finie ;
      entre deux finies, la plus tardive.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Ajout seul, jamais de réécriture (LIVRER.noter).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    retenu = {}
    for d in lignes:
        k = (d["etape"], d["branche"], d["executant"], d["identifiant"])
        a = retenu.get(k)
        if a is None or (bool(d["fini_le"]), d["fini_le"]) > (bool(a["fini_le"]), a["fini_le"]):
            retenu[k] = d
    return sorted(retenu.values(), key=lambda d: (d["lance_le"], d["etape"]))


def heure_git(texte):
    """Rend une heure git ISO (« 2026-11-20 17:58:30 +0100 ») en heure de Paris « AAAA-MM-JJ HH:MM:SS ».

    ① RÔLE — Comparer une heure de commit au registre.
    ② CONTEXTE D'APPEL — `confirmer`.
    ③ ENTRÉE — `texte`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte, ou « » s'il est illisible.
      [rend: 1]
    ⑥ TRAITEMENT — strptime %z, conversion Europe/Paris.
    ⑦ UNITÉ — Heure de Paris.
    ⑧ POURQUOI — Les commits de Cowork sont en heure universelle (A-826).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    try:
        return datetime.strptime(texte.strip(), "%Y-%m-%d %H:%M:%S %z").astimezone(L.PARIS).strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return ""


def confirmer(racine, d, memo):
    """Confronte une ligne retenue à sa source vivante ; rend (état vu, défaut ou « »).

    ① RÔLE — Ne jamais croire le registre sur parole.
    ② CONTEXTE D'APPEL — `rapport`, une fois par ligne retenue.
    ③ ENTRÉE — `racine` : le clone privé · `d` : la ligne · `memo` : un dict de réponses déjà lues.
    ④ CONDITIONS D'ENTRÉE — fetch fait.
    ⑤ SORTIE — DEUX valeurs : ce que la source dit ; le défaut (texte) ou « ».
      [rend: 2]
    ⑥ TRAITEMENT — github : « gh run view <n> --json status,conclusion » ; fini au registre et vivant chez GitHub,
      ou l'inverse → défaut. cowork : dernier commit d'auteur « cowork » sur origin/<branche> ; fini au registre
      sans commit de Cowork depuis le lancement → défaut ; en cours avec un commit depuis → « a écrit ». chat :
      publication/republication → la branche publique existe (ls-remote) ; installation → l'identifiant est dans
      l'histoire d'origin/main ; note → la branche privée existe.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Ajout du Chat du 20-11-2026 à 19h40 : « interroge les sources VIVANTES pour confirmer chaque
      ligne ».
    ⑨ CE QUI CLOCHE — Une réponse illisible de gh est un défaut (R-734), pas un silence.
    ⑩ EFFET — Lit GitHub et git.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    fini = bool(d["fini_le"])
    if d["executant"] == "github":
        n = d["identifiant"]
        if n not in memo:
            try:
                memo[n] = L.gh_json("run", "view", n, "--repo", L.repo_public(), "--json", "status,conclusion") or {}
            except L.Arret as e:
                memo[n] = {"erreur": e.args[1]}
        v = memo[n]
        if "erreur" in v:
            return "illisible", f"passage {n} non vérifiable : {v['erreur'][:120]}"
        vivant = v.get("status") != "completed"
        vu = f"GitHub {v.get('status')} {v.get('conclusion') or ''}".strip()
        if fini and vivant:
            return vu, f"le registre dit fini, GitHub dit {v.get('status')}"
        if not fini and not vivant:
            return vu, "GitHub a fini, le registre dit en cours (LIVRER arrêté ?)"
        return vu, ""
    if d["executant"] == "cowork":
        # D-5 : « --author » est un motif (« Claude (pas cowork) » y répond) ; seul le nom EXACT compte, comme pour
        # INSTALLER.juger_le_relu ; la règle est écrite une fois, LIVRER.est_cowork (N-26, R-708).
        log = L.git(racine, "log", "--author=cowork", "--format=%H %ci\t%an", f"refs/remotes/origin/{d['branche']}")
        exacts = [l.split("\t", 1)[0] for l in log.stdout.splitlines()
                  if "\t" in l and L.est_cowork(l.split("\t", 1)[1])]
        morceaux = (exacts[0] if exacts else "").split(" ", 1)
        quand = heure_git(morceaux[1]) if len(morceaux) == 2 else ""
        if quand and quand >= d["lance_le"]:
            return f"Cowork a écrit {morceaux[0][:12]} à {quand}", ""
        if fini:
            return "aucun commit de Cowork depuis le lancement", "le registre dit fini, git ne montre rien de Cowork"
        return "aucun commit de Cowork depuis le lancement (au travail ou silencieux)", ""
    if d["etape"] in ("publication", "republication"):
        p = L.pointe_publique(d["branche"])
        if p:
            return f"branche publique à {p[:12]}", ""
        return "branche publique absente", "branche publique absente"
    if d["etape"] == "installation":
        ok = L.git(racine, "merge-base", "--is-ancestor", d["identifiant"], "refs/remotes/origin/main").returncode == 0
        if ok:
            return "dans main", ""
        return "hors de main", "installation notée, pointe absente de main"
    existe = L.git(racine, "rev-parse", "--verify", "-q", f"refs/remotes/origin/{d['branche']}").stdout.strip()
    if existe:
        return "branche présente", ""
    return "branche absente", ""


def doublons(retenus):
    """Rend les doublons : la même épreuve d'une branche chez deux exécutants, ou deux passages GitHub non finis.

    ① RÔLE — Voir le travail fait deux fois.
    ② CONTEXTE D'APPEL — `rapport`.
    ③ ENTRÉE — `retenus` : les dernières lignes.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des phrases « DOUBLON … ».
      [rend: 1]
    ⑥ TRAITEMENT — Regroupe les étapes « epreuve:<CODE> » par (étape, branche) : plus d'un exécutant → doublon ;
      plus d'une ligne non finie du même exécutant → doublon.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — 20-11-2026 : la même épreuve chez Cowork et sur GitHub.
    ⑨ CE QUI CLOCHE — Deux tours d'une même branche (pointes différentes) comptent pour un doublon s'ils jouent la
      même épreuve chez deux exécutants : voulu, c'est du travail fait deux fois.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    groupes = {}
    for d in retenus:
        if d["etape"].startswith("epreuve:"):
            groupes.setdefault((d["etape"], d["branche"]), []).append(d)
    rendu = []
    for (etape, branche), ds in sorted(groupes.items()):
        executants = sorted({d["executant"] for d in ds})
        if len(executants) > 1:
            rendu.append(f"DOUBLON {etape[len('epreuve:'):]} sur {branche} : "
                         + " et ".join(f"{d['executant']} {d['identifiant'][:12]}" for d in ds))
        for e in executants:
            vivants = [d for d in ds if d["executant"] == e and not d["fini_le"]]
            if len(vivants) > 1:
                rendu.append(f"DOUBLON {etape[len('epreuve:'):]} sur {branche} : {len(vivants)} travaux {e} non finis")
    return rendu


def cowork_avant_github(retenus):
    """Rend les relectures de Cowork lancées avant la fin des épreuves GitHub de la même branche.

    ① RÔLE — Voir le défaut du 20-11-2026 : Cowork lancé avant GitHub.
    ② CONTEXTE D'APPEL — `rapport`.
    ③ ENTRÉE — `retenus`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des phrases.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque « relecture » cowork : une épreuve github de la même branche lancée avant elle et
      finie après elle (ou pas finie) → défaut.
    ⑦ UNITÉ — Heures de Paris, comparées en texte (même forme).
    ⑧ POURQUOI — LIVRER ne rend 0 qu'après les résultats de GitHub ; ceci attrape un lancement fait sans lui.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    rendu = []
    for r in retenus:
        if r["etape"] != "relecture" or r["executant"] != "cowork":
            continue
        for g in retenus:
            if (g["executant"] == "github" and g["etape"].startswith("epreuve:") and g["branche"] == r["branche"]
                    and g["lance_le"] <= r["lance_le"] and (not g["fini_le"] or g["fini_le"] > r["lance_le"])):
                rendu.append(f"COWORK AVANT GITHUB sur {r['branche']} : relecture lancée à {r['lance_le']}, "
                             f"{g['etape']} (passage {g['identifiant']}) {'non finie' if not g['fini_le'] else 'finie à ' + g['fini_le']}")
                break
    return rendu


def rapport(racine, sans_fetch):
    """Affiche ce qui tourne, ce qui est fini, les doublons et les incohérences ; rend le code de sortie.

    ① RÔLE — La commande par défaut.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` · `sans_fetch`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2.
      [rend: 1]
    ⑥ TRAITEMENT — `lignes_du_registre`, `derniers_etats`, `confirmer` pour chacune, `doublons`,
      `cowork_avant_github`, affichage par section.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir l'en-tête.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    try:
        retenus = derniers_etats(lignes_du_registre(racine, sans_fetch))
    except L.Arret as e:
        L.dire(f"ILLISIBLE — {e.args[1]}")
        return ILLISIBLE
    except (OSError, ValueError, AttributeError) as e:
        L.dire(f"ILLISIBLE — {type(e).__name__} : {e}")
        return ILLISIBLE
    memo, en_cours, finis, incoherents = {}, [], [], []
    for d in retenus:
        vu, defaut = confirmer(racine, d, memo)
        ligne = (f"{d['etape']} · {d['branche']} · {d['executant']} {d['identifiant'][:12]} · lancé {d['lance_le']}"
                 + (f" · fini {d['fini_le']} : {d['resultat']}" if d["fini_le"] else "") + f" — vu : {vu}")
        (finis if d["fini_le"] else en_cours).append(ligne)
        if defaut:
            incoherents.append(f"INCOHÉRENT {d['etape']} · {d['branche']} · {d['executant']} : {defaut}")
    incoherents += cowork_avant_github(retenus)
    doubles = doublons(retenus)
    for titre, liste in (("EN COURS", en_cours), ("FINI", finis), ("DOUBLON", doubles), ("INCOHÉRENT", incoherents)):
        L.dire(f"== {titre} ({len(liste)})")
        for l in liste:
            L.dire("  " + l)
    return DEFAUT if doubles or incoherents else SANS_DEFAUT


def noter_a_la_main(racine, args, fini):
    """« noter » : écrit un lancement dans le registre de la branche, commite et pousse ; rend le code.

    ① RÔLE — Donner au Chat un geste écrit pour ce qu'aucun programme n'écrit (Cowork).
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` · `args` : étape, branche, exécutant, identifiant · `fini` : le résultat, ou None.
    ④ CONDITIONS D'ENTRÉE — La branche est une travail-… présente sur origin.
    ⑤ SORTIE — UNE valeur : 0, ou 3.
      [rend: 1]
    ⑥ TRAITEMENT — `LIVRER.worktree_nomme` ; `LIVRER.noter` ; `LIVRER.pousser` ; retrait du worktree jetable.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le registre vit au dépôt, pas dans la mémoire du Chat.
    ⑨ CE QUI CLOCHE — Pousser change la pointe de la branche : jamais pendant un passage GitHub de cette branche
      (la porte « preparer » compare la pointe) ; ce programme le refuse si une épreuve github y est en cours.
    ⑩ EFFET — Commit et poussée privés sur la branche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    etape, branche, executant, identifiant = args
    if not branche.startswith("travail-"):
        L.dire("REFUS — on ne note que sur une branche travail-… (jamais main)")
        return NOTE_REFUSEE
    wt, jetable = None, False
    try:
        L.git(racine, "fetch", "-q", "origin")
        retenus = derniers_etats(lignes_du_registre(racine, True))
        if any(d["branche"] == branche and d["executant"] == "github" and not d["fini_le"] for d in retenus):
            L.dire("REFUS — une épreuve GitHub de cette branche est en cours : pousser changerait sa pointe")
            return NOTE_REFUSEE
        wt, jetable = L.worktree_nomme(racine, branche)
        heure = L.maintenant()
        L.noter(wt, etape, branche, executant, identifiant, heure, heure if fini is not None else "", fini or "")
        if not L.pousser(wt, branche, f"registre des travaux : {etape} {executant} sur {branche}", [L.REGISTRE]):
            L.dire("REFUS — le registre n'a pas pu être poussé")
            return NOTE_REFUSEE
        L.dire(f"NOTÉ — {etape} · {branche} · {executant} {identifiant} · {heure}")
        return SANS_DEFAUT
    except (L.Arret, ValueError) as e:
        L.dire(f"REFUS — {e.args[-1]}")
        return NOTE_REFUSEE
    finally:
        if wt and jetable:
            L.retirer_worktree(racine, wt)


def main():
    """Lit la ligne de commande et lance le rapport ou « noter » ; sort avec le code.

    ① RÔLE — Voir l'en-tête.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — sys.argv.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien : sort (0, 1, 2, 3 ou 5).
      [rend: rien]
    ⑥ TRAITEMENT — « noter » + quatre mots → `noter_a_la_main` ; sinon `rapport`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Voir l'en-tête.
    ⑪ TERMINAISON — Sort du programme par sys.exit.
      [sort: oui]
    """
    mots = [a for a in sys.argv[1:] if not a.startswith("--")]
    fini = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--fini=")), None)
    racine = os.getcwd()
    try:
        if mots[:1] == ["noter"]:
            if len(mots) != 5:
                L.dire("usage : QUI_FAIT_QUOI.py noter <étape> <branche> <exécutant> <identifiant> [--fini=<résultat>]")
                code = NOTE_REFUSEE
            else:
                code = noter_a_la_main(racine, mots[1:], fini)
        else:
            code = rapport(racine, "--sans-fetch" in sys.argv)
    except Exception as e:   # noqa: BLE001 — un plantage n'est jamais lu comme un verdict
        L.dire(f"PLANTAGE (code {L.PLANTAGE}) — {type(e).__name__} : {e}")
        code = L.PLANTAGE
    sys.exit(code)


if __name__ == "__main__":
    main()
