#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""COMPTER_LES_DEFAUTS.py — compte les défauts OUVERTS d'un RELU, par gravité, et la tendance. Mer 25-11-2026,
corrigé le même soir (lecture d'un FORMAT, plus de négations devinées).
Simulation uniquement : aucun ordre réel, jamais.

① RÔLE — Dire, sans lecture humaine, combien de défauts bloquants, importants et mineurs restent ouverts dans une
  relecture (echanges/RELU.md), si ce nombre monte par rapport à la relecture précédente, et si une ligne ne se lit
  pas selon le format.
② CONTEXTE D'APPEL — Par le programme de pilotage (programmes/PILOTER_UN_PLANNING.py), comme contrôle préparé par
  l'adaptateur du projet ou déclaré dans controles.csv ; à la main :
  python3 -I programmes/COMPTER_LES_DEFAUTS.py <RELU> [<RELU précédent>]   (« - » = entrée standard pour le premier)
③ ENTRÉE — Un ou deux chemins de RELU.
④ CONDITIONS D'ENTRÉE — LE FORMAT (écrit pour Cowork dans echanges/SECTION_MODE_EMPLOI_PILOTAGE.md, § 8) :
  un défaut se DÉFINIT par « N-<nombre> (<GRAVITÉ>) » — GRAVITÉ = BLOQUANT, IMPORTANT ou MINEUR (pluriel permis ;
  la parenthèse vaut pour la liste de N-… qui la précède immédiatement) ; son STATUT s'écrit JUSTE APRÈS la
  parenthèse, et seulement là : « [FERMÉ] » le ferme, « [OUVERT] » ou rien le laisse ouvert, tout autre texte entre
  crochets (« [FERME] », « [CLOS] ») est un STATUT ILLISIBLE. Un jeton écrit ailleurs sur la ligne, ou sur une ligne
  qui ne définit pas le défaut, n'a AUCUN effet. Deux définitions du même N-… aux statuts contraires sont ILLISIBLES
  (le doute ouvre, il ne ferme pas). Un N-… cité sans gravité nulle part est SANS GRAVITÉ. Exemples :
  « - N-12 (BLOQUANT) [FERMÉ] — le compte est juste » → fermé ; « ### N-62 (MINEUR) — l'empreinte … » (vraie ligne
  du RELU de travail-planning-20, c212e07c7) → ouvert ; « - N-57 (IMPORTANT) : CORRIGÉ sur le fond » (même RELU) →
  OUVERT, faute du jeton ; « - N-7 (BLOQUANT) [OUVERT] — ancien statut [FERMÉ] retiré » (N-66 du RELU du
  25-11-2026, 22h54) → OUVERT : le second jeton n'est pas juste après la gravité.
⑤ SORTIE — Des lignes, et UNE valeur : le code de sortie — 0 aucun bloquant ouvert, rien d'illisible, total qui ne
  monte pas · 3 au moins un bloquant ouvert, OU un statut illisible, OU un défaut sans gravité, OU le total ouvert
  a MONTÉ par rapport au RELU précédent · 2 lecture impossible.
⑥ TRAITEMENT — `compter` sur chaque texte (normalisé NFC) ; tendance = total ouvert actuel − total précédent.
⑦ UNITÉ — Des défauts.
⑧ POURQUOI — Constat du Chat, 25-11-2026 20h41 (A-1016) : le comptage des défauts n'était qu'une consigne ; R-754.
  Corrigé après D7 de la relecture à mandat inversé du 25-11-2026 (21h45) : « pas encore corrigé », « **PAS**
  CORRIGÉ », « NON-CORRIGÉ » fermaient un BLOQUANT ; jugement du superviseur R-759 (21h48) : deviner une négation
  échouera sur la cinquième formulation — lire un FORMAT, et tout ce qui n'est pas lisible alerte. N-66 du RELU du
  25-11-2026 (22h54) : le jeton fermait n'importe où dans le segment, même nié ou après [OUVERT] ; jugement du
  superviseur R-759 tour 2 : seule la ligne qui DÉFINIT le défaut porte le statut, juste après la gravité.
⑨ CE QUI CLOCHE — Les RELU écrits avant ce format n'ont pas de jeton [FERMÉ] : tous leurs défauts sont comptés
  ouverts, et leurs N-… sans gravité donnent une alerte. C'est voulu (le doute ouvre, il ne ferme pas), mais le
  pilote alertera sur chaque branche dont le RELU est à l'ancien format, jusqu'à ce que Cowork écrive le format.
  « [FERMÉ] » dans une liste « N-1, N-2 (MINEURS) [FERMÉ] » ferme TOUTE la liste (la définition vaut pour elle).
⑩ EFFET — Aucun : lecture seule.
⑪ TERMINAISON — Toujours ; aucun appel externe.
"""
import re
import sys
import unicodedata

GRAVITES = ("BLOQUANT", "IMPORTANT", "MINEUR")
MOTIF_DEFINITION = re.compile(r"((?:N-\d+\s*[a-z]?\s*(?:,|/|et)\s*)*N-\d+)\s*[a-z]?\s*\(\s*(BLOQUANT|IMPORTANT|MINEUR)S?\b"
                              r"(?:[^)\n]*\))?\s*(?:\[([^\]\n]*)\])?", re.I)
MOTIF_ID = re.compile(r"N-\d+")
JETON_FERME = "FERMÉ"
JETON_OUVERT = "OUVERT"


def compter(texte):
    """① RÔLE — Compter les défauts ouverts d'un texte de RELU, selon le format du ④ du module.
    ② CONTEXTE D'APPEL — `main`, une fois par RELU ; les épreuves.
    ③ ENTRÉE — `texte` : le RELU entier.
    ④ CONDITIONS D'ENTRÉE — voir ④ du module.
    ⑤ SORTIE — QUATRE valeurs : {gravité: liste triée des N-… ouverts} · liste triée des fermés · liste triée des
      N-… sans gravité · liste des statuts illisibles (« N-… [JETON] » ou « N-… (définitions contraires) »).
      [rend: 4]
    ⑥ TRAITEMENT — texte normalisé NFC ; chaque DÉFINITION (« N-… (GRAVITÉ…) », éventuellement suivie, juste après
      la parenthèse, d'un statut entre crochets) donne une gravité et un statut à chaque N-… de sa liste : [FERMÉ] →
      fermé ; [OUVERT] ou rien → ouvert ; autre chose → illisible (et ouvert). Gravité retenue : la plus forte.
      Un N-… est FERMÉ seulement si TOUTES ses définitions disent [FERMÉ] ; des définitions contraires → illisible,
      et ouvert. Toute autre mention d'un N-… (hors définition) ne compte que pour « sans gravité ».
    ⑦ UNITÉ — des défauts.
    ⑧ POURQUOI — voir ⑧ du module.
    ⑨ CE QUI CLOCHE — voir ⑨ du module.
    ⑩ EFFET — —
    ⑪ TERMINAISON — revient toujours.
      [sort: non]
    """
    texte = unicodedata.normalize("NFC", texte)
    grav, statuts, vus, illisibles = {}, {}, set(), []
    for ligne in texte.splitlines():
        vus.update(MOTIF_ID.findall(ligne))
        for m in MOTIF_DEFINITION.finditer(ligne):
            g, jeton = m.group(2).upper(), m.group(3)
            for i in MOTIF_ID.findall(m.group(1)):
                if i not in grav or GRAVITES.index(g) < GRAVITES.index(grav[i]):
                    grav[i] = g
                if jeton is None or jeton == JETON_OUVERT:
                    statuts.setdefault(i, set()).add("ouvert")
                elif jeton == JETON_FERME:
                    statuts.setdefault(i, set()).add("fermé")
                else:
                    statuts.setdefault(i, set()).add("ouvert")
                    illisibles.append(f"{i} [{jeton}]")
    for i, s in sorted(statuts.items()):
        if len(s) > 1:
            illisibles.append(f"{i} (définitions contraires)")
    fermes = {i for i, s in statuts.items() if s == {"fermé"}}
    cle = lambda x: int(x[2:])
    ouverts = {g: sorted((i for i, gi in grav.items() if gi == g and i not in fermes), key=cle) for g in GRAVITES}
    return ouverts, sorted(fermes, key=cle), sorted(vus - set(grav), key=cle), illisibles


def main(argv):
    """① RÔLE — Ligne de commande du comptage des défauts : lire un ou deux RELU, compter, comparer, afficher.
    ② CONTEXTE D'APPEL — voir ② du module.
    ③ ENTRÉE — `argv` : la ligne de commande, un ou deux chemins.
    ④ CONDITIONS D'ENTRÉE — un ou deux chemins lisibles en UTF-8.
    ⑤ SORTIE — UNE valeur : le code de sortie, 0, 2 ou 3.
      [rend: 1]
    ⑥ TRAITEMENT — lire, `compter`, tendance, affichage ; alerte si bloquant ouvert, illisible, sans gravité, ou
      total qui monte.
    ⑦ UNITÉ — des défauts.
    ⑧ POURQUOI — voir ⑧ du module.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — affichage.
    ⑪ TERMINAISON — toujours.
      [sort: non]
    """
    if len(argv) not in (2, 3):
        print("USAGE : COMPTER_LES_DEFAUTS.py <RELU|-> [<RELU précédent>]")
        return 2
    try:
        textes = [sys.stdin.read() if argv[1] == "-" else open(argv[1], encoding="utf-8").read()]
        if len(argv) == 3:
            textes.append(open(argv[2], encoding="utf-8").read())
    except (OSError, UnicodeDecodeError) as e:
        print(f"LECTURE IMPOSSIBLE : {e}")
        return 2
    ouverts, fermes, sans, illisibles = compter(textes[0])
    total = sum(len(v) for v in ouverts.values())
    print("OUVERTS : " + " · ".join(f"{g.lower()}s {len(ouverts[g])}" + (f" ({', '.join(ouverts[g])})" if ouverts[g] else "")
                                    for g in GRAVITES))
    print(f"FERMÉS ([{JETON_FERME}]) : {len(fermes)}" + (f" ({', '.join(fermes)})" if fermes else ""))
    print(f"SANS GRAVITÉ : {len(sans)}" + (f" ({', '.join(sans)})" if sans else ""))
    print(f"STATUTS ILLISIBLES : {len(illisibles)}" + (f" ({', '.join(illisibles)})" if illisibles else ""))
    monte = False
    if len(textes) == 2:
        avant = sum(len(v) for v in compter(textes[1])[0].values())
        monte = total > avant
        print(f"TENDANCE : {avant} → {total} ouverts ({'+' if total >= avant else ''}{total - avant})")
    raisons = [t for t, oui in (("bloquant ouvert", ouverts["BLOQUANT"]), ("statut illisible", illisibles),
                                ("défaut sans gravité", sans), ("le total ouvert monte", monte)) if oui]
    if raisons:
        print("ALERTE : " + " ; ".join(raisons))
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
