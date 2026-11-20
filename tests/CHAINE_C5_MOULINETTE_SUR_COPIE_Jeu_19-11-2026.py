#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CHAINE_C5_MOULINETTE_SUR_COPIE_Jeu_19-11-2026.py — Jeu 19-11-2026 (Paris). Simulation uniquement : aucun ordre réel.

LE SENS EN TÊTE. A-916 (C5 sert à éprouver TOUTE la chaîne, verdict « déjà vu, ne prouve rien ») et A-917 (sur une COPIE,
rien au vrai registre). L'épreuve tests/EPREUVE_DE_LA_CHAINE_C5_SUR_COPIE_Jeu_19-11-2026.py lançait le juge sur UNE
version de C5 sans passer par la moulinette. Ce programme rejoue la chaîne OFFICIELLE d'A-541 (en-tête de
programmes/JOUER_LES_VERSIONS.py), dans l'ordre, sans en sauter : ⓪ PREPARER_LES_VARIABLES… · ① DECLINER_LES_STRATEGIES ·
② JOUER_LES_VERSIONS · ③ TRIER_LES_VARIANTES · ④ le juge — puis la fiche marquée, puis le circuit du soir.

① RÔLE — Une étape par appel (chaque appel tient sous 10 minutes, consigne du 19-11-2026 : lots au premier plan) :
  copie · preparer · decliner · jouer <k> <N> (k = 0 … N-1) · assembler · trier · juger · fiche · soir · bilan.
  ⓪ à ④ PASSENT PAR programmes/ENCHAINER_LA_MOULINETTE.py (relecteur du 19-11-2026, M2 ; superviseur R-759 du
  19-11-2026, ⑥) : la porte du juge exige le journal de la chaîne et la fiche MARQUÉE que l'enchaîneur écrit.
② CONTEXTE D'APPEL — À la main : `python3 -B tests/CHAINE_C5_MOULINETTE_SUR_COPIE_Jeu_19-11-2026.py <racine> <travail>
  <étape> [argument]`, les étapes dans l'ordre ci-dessus.
③ ENTRÉE — `<racine>` : un clone ou worktree (jamais modifié) ; `<travail>` : un dossier hors de la racine, qui reçoit la
  copie (<travail>/depot) et tout ce que les étapes écrivent.
④ CONDITIONS D'ENTRÉE — La racine est un dépôt git et porte la combinatoire validée de C5E10-OBS-V1 E01 et son témoin.
⑤ SORTIE — UNE valeur, le code de sortie : 0 si l'étape a tenu, 1 sinon, 2 si l'étape n'a pas pu tourner. [rend: 1]
⑥ TRAITEMENT — voir chaque fonction `etape_*`.
⑦ UNITÉ — Euros pour 100 000 € par opération ; tp et sl en fractions dans les versions ; horizon en séances.
⑧ POURQUOI — R-708 : chaque calcul vit dans le programme du circuit ; ce fichier ne fait que les lancer et relever.
⑨ CE QUI CLOCHE — ① LA MOULINETTE EST JOUÉE PAR TRANCHES (consigne : moins de 10 minutes par appel), par l'option
  --tranche=k/N de JOUER_LES_VERSIONS, puis assemblée par --assembler (témoin entier comparé) : les lots fabriqués ici
  jusqu'au 19-11-2026 sont retirés (le découpage vit dans JOUER, une fois — R-708). ② ⓪ propose aujourd'hui une autre grille que la grille validée (le stop s'étend à 15 % et « sans
  stop ») : la chaîne joue la table VALIDÉE (« Jean-Luc le 08-10-2026 »), et ⓪ n'est que rejoué et comparé.
  ③ LA PÉRIODE JOUÉE EST CELLE DE LA FICHE (2024-01-02 → 2026-07-10, cours maître), PAS 2000-2026 : l'essai sans regard
  (A-863) refuse plus d'une version (mesuré : code 2, « un essai sans regard n'en joue qu'une ») et sans lui la fenêtre
  2000-2023 consommerait un regard. ④ LE CHOIX DE LA VERSION JUGÉE : A-774 (Jean-Luc, 14-11-2026 14h31) — seule la
  version choisie sur les 70 % est jugée ; le classement n'existe pas encore (bloc 5m ④). Ce programme prend le plus grand
  `gain_net_euros_70` parmi les retenues : CRITÈRE NON DÉCIDÉ PAR JEAN-LUC. ⑤ La boucle du soir (`etape_soir`) reprend
  celle de l'épreuve du 19-11 (M5), qui n'est pas une fonction importable : ~20 lignes en double (R-708 à reprendre).
  ⑥ Le juge est lancé par l'enchaîneur sur la version mise en fiche MARQUÉE dans le registre de la COPIE,
  identifiant = id_version.
⑩ EFFET — Écrit sous <travail> seulement ; ne touche jamais la racine (empreintes avant/après, étape `bilan`).
⑪ TERMINAISON — Chaque programme lancé est borné (580 s la moulinette et le juge, 300 s les autres). [sort: oui — code]
"""
import csv
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time

sys.dont_write_bytecode = True

ICI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("EPREUVE_C5", os.path.join(ICI, "EPREUVE_DE_LA_CHAINE_C5_SUR_COPIE_Jeu_19-11-2026.py"))
E = importlib.util.module_from_spec(_spec)
_argv = sys.argv
sys.argv = [_argv[0]]
_spec.loader.exec_module(E)          # helpers réutilisés (R-708) : ignorer, empreintes, lancer, ecrire_dans_la_fiche…
sys.argv = _argv

SID, ESSAI = "C5E10-OBS-V1", "E01"
COMB = "donnees/combinatoires/COMBINATOIRE_%s_%s.csv" % (SID, ESSAI)
VARIABLES = "donnees/combinatoires/VARIABLES_DE_DECLINAISON_%s_%s.csv" % (SID, ESSAI)
TEMOIN = "donnees/combinatoires/TEMOIN_RESULTATS_%s_%s.csv" % (SID, ESSAI)
VOISINAGE = "donnees/combinatoires/VOISINAGE.csv"
sys.path.insert(0, os.path.join(os.path.dirname(ICI), "programmes"))
import CONTRATS_DES_FICHIERS as _C  # noqa: E402  le registre est nommé au contrat (R-708)
REG = _C.REGISTRE_DES_STRATEGIES


def lire(chemin):
    with open(chemin, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def ecrire(chemin, champs, lignes):
    with open(chemin, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=champs, lineterminator="\n")
        w.writeheader()
        w.writerows(lignes)


def lancer(copie, travail, *args, delai=300):
    t0 = time.time()
    code, sortie, _ = E.lancer(copie, os.path.join(travail, "sortie_du_pas"), *args, delai=delai)
    return code, sortie, time.time() - t0


def empreintes(racine):
    git = subprocess.run(["git", "-C", racine, "rev-parse", "HEAD"], capture_output=True, text=True).stdout
    st = subprocess.run(["git", "-C", racine, "status", "--porcelain"], capture_output=True, text=True).stdout
    arbre = E.empreinte_du_depot(racine)
    return {"git_head_status": hashlib.sha256((git + st).encode()).hexdigest()[:16], "arbre": arbre[0],
            "fichiers": arbre[1], "regards": E.regards_du_depot(racine), "registre_essais": E.registres_d_essais(racine)}


def etape_copie(racine, travail):
    """Empreinte avant, puis copie sans .git ni ce que `ignorer` écarte."""
    copie = os.path.join(travail, "depot")
    if os.path.exists(copie):
        print("ARRÊT : %s existe déjà" % copie)
        return 2
    av = empreintes(racine)
    json.dump(av, open(os.path.join(travail, "avant.json"), "w"))
    shutil.copytree(racine, copie, ignore=E.ignorer, symlinks=False)
    print("EMPREINTE AVANT : %s" % av)
    print("COPIE : %s · .git : %s" % (copie, os.path.lexists(os.path.join(copie, ".git"))))
    return 0


ENCH = "programmes/ENCHAINER_LA_MOULINETTE.py"


def chaine(copie):
    """Le dossier de la chaîne, tel que l'enchaîneur le nomme (VERIFIER_LA_CHAINE.dossier, la seule définition)."""
    return os.path.join(copie, "CHAINE_%s_%s" % (SID, ESSAI))


def enchainer(copie, travail, *args, delai=600):
    """Une étape PAR L'ENCHAÎNEUR (relecteur du 19-11-2026, M2 ; superviseur R-759 du 19-11-2026, ⑥) : le journal de la
    chaîne et ses témoins sont tenus par lui, et la porte du juge les exige. Rend (code, sortie, durée). [rend: 3]"""
    return lancer(copie, travail, ENCH, copie, SID, ESSAI, *args, delai=delai)


def etape_preparer(copie, travail):
    """⓪ par l'enchaîneur (PREPARER rejoué, table validée recopiée et témoignée) ; comparé à la table validée."""
    c, o, t = enchainer(copie, travail, "preparer")
    print("⓪ PREPARER (enchaîneur) code %d en %.1f s · %s" % (c, t, [l for l in o.splitlines() if "VERSIONS QUE" in l]))
    if c:
        print(o)
        return c
    val = {r["parametre"]: r for r in lire(os.path.join(chaine(copie), "valide", os.path.basename(VARIABLES)))}
    pre = {r["parametre"]: r for r in lire(os.path.join(chaine(copie), "e0", os.path.basename(VARIABLES)))}
    for p in val:
        if val[p]["jouable"] == "OUI":
            print("  %s · validé (%s) : %s · proposé aujourd'hui : %s%s" % (
                p, val[p]["valide_par"], val[p]["valeurs_a_essayer"], pre.get(p, {}).get("valeurs_a_essayer"),
                "" if val[p]["valeurs_a_essayer"] == pre.get(p, {}).get("valeurs_a_essayer") else "  ← DIFFÉRENT"))
    return c


def etape_decliner(copie, travail):
    """① par l'enchaîneur ; la combinatoire comparée à l'octet à celle du dépôt."""
    c, o, t = enchainer(copie, travail, "decliner")
    neuve = os.path.join(chaine(copie), "e1", os.path.basename(COMB))
    n = len(lire(neuve)) if os.path.isfile(neuve) else -1
    same = os.path.isfile(neuve) and open(neuve, "rb").read() == open(os.path.join(copie, COMB), "rb").read()
    print("① DECLINER (enchaîneur) code %d en %.2f s · %d versions déclinées · identique à l'octet à %s : %s"
          % (c, t, n, COMB, same))
    print("  " + " | ".join(l for l in o.splitlines() if l.strip()))
    return 0 if c == 0 and same else 1


def etape_jouer(copie, travail, k, n):
    """② une tranche k sur n, par l'enchaîneur (JOUER_LES_VERSIONS --tranche=k/n, témoin comparé sur la tranche)."""
    c, o, t = enchainer(copie, travail, "jouer", str(k), str(n))
    print("② JOUER tranche %d/%d (enchaîneur) code %d en %.1f s" % (k, n, c, t))
    print("\n".join("  " + l for l in o.splitlines()[-8:]))
    return c


def etape_assembler(copie, travail):
    """② les tranches assemblées par l'enchaîneur (JOUER_LES_VERSIONS --assembler, témoin ENTIER comparé)."""
    c, o, t = enchainer(copie, travail, "assembler")
    print("② ASSEMBLER (enchaîneur) code %d en %.1f s" % (c, t))
    print("\n".join("  " + l for l in o.splitlines()[-8:]))
    return c


def etape_trier(copie, travail):
    """③ par l'enchaîneur ; choix de la version jugée (⑨ ④)."""
    c, o, t = enchainer(copie, travail, "trier")
    print("③ TRIER (enchaîneur) code %d en %.1f s" % (c, t))
    print("\n".join("  " + l for l in o.splitlines()[-8:]))
    if c != 0:
        return c
    rs = lire(os.path.join(chaine(copie), "e3", "TRI_%s_%s.csv" % (SID, ESSAI)))
    if not rs:
        print("③ AUCUNE VERSION RETENUE")
        return 0
    meilleure = max(rs, key=lambda r: float(r["gain_net_euros_70"]))
    os.makedirs(os.path.join(travail, "e3"), exist_ok=True)
    json.dump(meilleure, open(os.path.join(travail, "e3", "choisie.json"), "w"))
    print("③ RETENUES : %d · CHOISIE (plus grand gain_net_euros_70, critère NON DÉCIDÉ) : %s tp %s sl %s h %s univers %s"
          " · 70 %% : %s op · %s €" % (len(rs), meilleure["id_version"], meilleure["tp"], meilleure["sl"],
                                       meilleure["horizon"], meilleure["univers"], meilleure["operations_70"],
                                       meilleure["gain_net_euros_70"]))
    return 0


def etape_juger(copie, travail):
    """④ par l'enchaîneur : la version choisie mise en fiche MARQUÉE au registre de la COPIE, puis le juge, qui passe
    sa porte de la chaîne (A-919, A-921)."""
    v = json.load(open(os.path.join(travail, "e3", "choisie.json")))
    c, o, d = enchainer(copie, travail, "juger", v["id_version"])
    f = os.path.join(chaine(copie), "e4", "juge_%s.txt" % v["id_version"])
    o = open(f, encoding="utf-8").read() if os.path.isfile(f) else o
    open(os.path.join(travail, "e3", "juge.txt"), "w", encoding="utf-8").write(o)
    bloc = o.split("=== %s" % v["id_version"], 1)[1] if ("=== %s" % v["id_version"]) in o else ""
    m = re.search(r"(\d+) operations \. ([\d.]+) % de reussite \. ([+-][\d,]+\.\d\d) EUR", bloc)
    print("④ JUGE (enchaîneur) code %d en %.1f s · %s · %s" % (c, d, v["id_version"],
                                                              m.groups() if m else "chiffres introuvables"))
    print("\n".join("  " + l for l in (bloc or o).splitlines()[:40]))
    json.dump({"code": c, "chiffres": m.groups() if m else None}, open(os.path.join(travail, "e3", "juge.json"), "w"))
    return c


def etape_fiche(copie, travail):
    """Le verdict marqué MARQUE_D_ESSAI écrit dans la fiche de la copie, puis état QA (suivi par le soir)."""
    v = json.load(open(os.path.join(travail, "e3", "choisie.json")))
    j = json.load(open(os.path.join(travail, "e3", "juge.json")))
    ch = j["chiffres"]
    texte = "%s · juge code %d sur la période de la fiche : %s (A-916, A-917)" % (
        E.MARQUE_D_ESSAI, j["code"], "%s opérations · %s %% · %s EUR" % tuple(ch) if ch else "sans chiffres")
    E.ecrire_dans_la_fiche(copie, REG, v["id_version"], {"statut": texte})
    E.ecrire_dans_la_fiche(copie, REG, v["id_version"], {"etat_vie": "QA"})
    sys.path.insert(0, os.path.join(copie, "programmes"))
    import CONTRATS_DES_FICHIERS as C
    f = C.fiches_du_registre(os.path.join(copie, REG)).get(v["id_version"]) or {}
    print("FICHE %s · statut %r · etat_vie %r · suivie par le soir : %s" % (
        v["id_version"], f.get("statut"), f.get("etat_vie"), C.suivie_par_le_soir(f)))
    return 0 if E.MARQUE_D_ESSAI in f.get("statut", "") and C.suivie_par_le_soir(f) else 1


def etape_soir(copie, travail):
    """Le circuit du soir rejoué séance par séance (⑨ ⑤ : boucle reprise de l'épreuve du 19-11, M5)."""
    v = json.load(open(os.path.join(travail, "e3", "choisie.json")))
    ident = v["id_version"]
    cm = os.path.join(copie, E.COURS_MAITRE)
    with open(cm, encoding="utf-8") as fh:
        cours = fh.read().splitlines(True)
    seances = sorted({l.split(",")[1] for l in cours[1:] if E.PREMIERE_SEANCE <= l.split(",")[1] <= E.DERNIERE_SEANCE})
    for f in (E.POSITIONS, E.JOURNAL):
        with open(os.path.join(copie, f), encoding="utf-8") as fh:
            ent = fh.readline()
        with open(os.path.join(copie, f), "w", encoding="utf-8") as fh:
            fh.write(ent)
    positions, codes, suivie = {}, [], 0
    for s in seances:
        with open(cm, "w", encoding="utf-8") as fh:
            fh.writelines([cours[0]] + [l for l in cours[1:] if l.split(",")[1] <= s])
        cd, od, _ = lancer(copie, travail, "programmes/DETECTER_LES_SIGNAUX_GITHUB.py", ".")
        ct, ot, _ = lancer(copie, travail, "programmes/TENIR_LES_POSITIONS.py", ".")
        cr, orad, _ = lancer(copie, travail, "programmes/audit_ecosysteme.py", ".")
        suivies = od.split("fiches suivies : ", 1)[1].splitlines()[0] if "fiches suivies : " in od else ""
        suivie += ident in suivies
        codes.append((s, cd, ct, cr))
        for p in E.lire_csv(os.path.join(copie, E.POSITIONS)):
            if p["strategie"] == ident and p["statut"] == "OUVERTE":
                positions[(p["valeur"], p["date_entree"], p["comptabilite"])] = p
    with open(cm, "w", encoding="utf-8") as fh:
        fh.writelines(cours)
    trades = [t for t in E.lire_csv(os.path.join(copie, E.JOURNAL)) if t["strategie"] == ident]
    print("SOIR : %d séances %s → %s · fiche suivie par le détecteur %d soir(s) · codes non nuls : %s"
          % (len(seances), seances[0], seances[-1], suivie, [x for x in codes if any(x[1:])] or "aucun"))
    print("  positions %s ouvertes vues : %d · %s" % (ident, len(positions), sorted(positions)))
    print("  trades %s au journal : %d · net %+.2f EUR · %s" % (
        ident, len(trades), sum(float(t["pnl_net_eur"]) for t in trades),
        ["%s %s→%s %s %s %s" % (t["valeur"], t["date_entree"], t["date_sortie"], t["motif_sortie"], t["comptabilite"],
                                t["pnl_net_eur"]) for t in trades]))
    return 0 if all(not any(x[1:]) for x in codes) else 1


def etape_bilan(racine, travail):
    av = json.load(open(os.path.join(travail, "avant.json")))
    ap = empreintes(racine)
    ap["arbre"], ap["fichiers"] = ap["arbre"], ap["fichiers"]
    egal = all(av[k] == ap[k] for k in av)
    print("EMPREINTE AVANT : %s" % av)
    print("EMPREINTE APRÈS : %s" % ap)
    print("IDENTIQUES : %s · registre_essais dans la copie : %d" % (
        egal, len(E.registres_d_essais(os.path.join(travail, "depot")))))
    return 0 if egal and not ap["regards"] else 1


def main():
    if len(sys.argv) < 4:
        print(__doc__.split("①")[0])
        return 2
    racine, travail, etape = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]), sys.argv[3]
    if os.path.commonpath([racine, travail]) == racine:
        print("ARRÊT : le travail doit être hors de la racine")
        return 2
    E.RACINE = racine
    os.makedirs(travail, exist_ok=True)
    copie = os.path.join(travail, "depot")
    if etape == "copie":
        return etape_copie(racine, travail)
    if etape == "bilan":
        return etape_bilan(racine, travail)
    if os.path.lexists(os.path.join(copie, ".git")):
        print("ARRÊT : la copie porte .git")
        return 2
    table = {"preparer": etape_preparer, "decliner": etape_decliner, "assembler": etape_assembler,
             "trier": etape_trier, "juger": etape_juger, "fiche": etape_fiche, "soir": etape_soir}
    if etape == "jouer":
        return etape_jouer(copie, travail, int(sys.argv[4]), int(sys.argv[5]))
    if etape in table:
        return table[etape](copie, travail)
    print("ARRÊT : étape inconnue %s" % etape)
    return 2


if __name__ == "__main__":
    sys.exit(main())
