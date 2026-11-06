#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""comparer_les_releves — versé au dépôt le Jeu 05-11-2026 (superviseur R-759 du 05-11-2026 : B1, et M3 « les épreuves au
dépôt ») depuis github_series/comparer_releves.py. Compare deux relevés de séries de sabotages : celui de la machine
du Chat et celui de GitHub. Simulation uniquement.

① RÔLE — Dire si deux relevés d'une même série sont identiques partout où ils doivent l'être (test de calibrage du
  circuit GitHub des séries, 05-11-2026).
② CONTEXTE D'APPEL — Lancé à la main par le Chat après le premier passage GitHub : relevé local, relevé GitHub,
  avec --calibrage pour LA preuve « GitHub = machine ».
③ ENTRÉE — Deux chemins de fichiers texte ; l'option --calibrage, n'importe où.
④ CONDITIONS D'ENTRÉE — Les deux fichiers existent et sont en UTF-8. Sinon : code 2.
⑤ SORTIE — UNE valeur : le code de sortie. 0 = identiques hors de la ligne 3 (dates et « P à la fois ») et de la
  ligne « # joué par : » (machine, Python, commit, passage, place libre : tests/outils/JOUER_UNE_SERIE_DE_SABOTAGES.py,
  `ligne_joue_par`, EXACTEMENT UNE de chaque côté ; avec --calibrage, celle du premier dit « machine locale » et
  celle du second « GitHub ») ;
  1 = au moins une autre différence, ou une ligne « joué par » manquante, en double, ou (--calibrage) qui ne dit
  pas la bonne machine (la solution est REFUSÉE) ; 2 = comparaison impossible.
⑥ TRAITEMENT — ① lire les deux fichiers en lignes, SANS traduction des fins de ligne (newline="" : relecture du
  05-11-2026, B1 — en mode texte ordinaire, « \r\n » et « \r » devenaient « \n », et deux relevés différents à
  l'octet sortaient IDENTIQUES), puis exiger une seule ligne « # joué par : » de chaque côté (et, avec --calibrage,
  « machine locale » à gauche, « GitHub » à droite), puis la retirer · ② vérifier que la ligne 3 a la forme « série jouée du … au …
  (Paris), L lots de T au plus, P à la fois, » des deux côtés, et que L et T sont égaux · ③ comparer toutes les
  autres lignes une à une, dans l'ordre, octet pour octet · ④ afficher chaque différence (numéro de ligne, les deux
  textes coupés à 160 caractères).
⑦ UNITÉ — —
⑧ POURQUOI — Règle du projet : avant tout résultat nouveau, reproduire un résultat déjà connu au chiffre près. Seules
  les heures et le nombre de lots joués en même temps peuvent changer d'une machine à l'autre ; le découpage en lots
  (L, T) change les lignes « lot k : Z0 », il doit donc être le même. La ligne « joué par » exigée : superviseur
  R-759 du 05-11-2026, tour 3, m-3 (« Le comparateur exige une ligne « joué par » de chaque côté. Avec --calibrage,
  l'une dit GitHub et l'autre la machine ») — sans cela, deux relevés LOCAUX pouvaient servir de preuve
  « GitHub = machine ».
⑨ CE QUI CLOCHE — Ne vérifie pas que les deux relevés portent sur le même commit : c'est l'égalité des lignes
  EMPREINTE qui le garantit pour les fichiers lus, pas pour le reste du dépôt.
⑩ EFFET — Écrit à l'écran seulement.
⑪ TERMINAISON — Rend la main ; aucun appel qui puisse ne pas revenir.
"""
import re
import sys

JOUE_PAR = "# joué par : "    # la ligne d'en-tête qui dit où la série a été jouée (le joueur, LIGNE_JOUE_PAR)
LIGNE_3 = re.compile(r"^# série jouée du .+ au .+ \(Paris\), (\d+) lots de (\d+) au plus, (\d+) à la fois,$")


def main():
    """Le programme entier (voir la fiche en tête).

    ① RÔLE — Fiche en tête.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — Fiche en tête.
    ④ CONDITIONS D'ENTRÉE — Fiche en tête.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1]
    ⑥ TRAITEMENT — Fiche en tête.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Fiche en tête.
    ⑨ CE QUI CLOCHE — Fiche en tête.
    ⑩ EFFET — Écrit à l'écran.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    chemins = [x for x in sys.argv[1:] if x != "--calibrage"]
    calibrage = "--calibrage" in sys.argv[1:]
    if len(chemins) != 2:
        print("usage : comparer_releves.py <relevé local> <relevé GitHub> [--calibrage]")
        return 2
    try:
        a_brut = open(chemins[0], encoding="utf-8", newline="").read().split("\n")
        b_brut = open(chemins[1], encoding="utf-8", newline="").read().split("\n")
    except (OSError, UnicodeDecodeError) as e:
        print(f"IMPOSSIBLE : {type(e).__name__} — {e}")
        return 2
    for cote, brut, machine in (("local", a_brut, "machine locale"), ("GitHub", b_brut, "GitHub")):
        joue = [l for l in brut if l.startswith(JOUE_PAR)]
        if len(joue) != 1:
            print(f"REFUS : le relevé {cote} porte {len(joue)} ligne(s) « joué par » au lieu d'une")
            return 1
        if calibrage and not joue[0].startswith(JOUE_PAR + machine + " ; "):
            print(f"REFUS (calibrage) : le relevé {cote} ne dit pas « joué par : {machine} » : {joue[0][:120]}")
            return 1
    a = [l for l in a_brut if not l.startswith(JOUE_PAR)]
    b = [l for l in b_brut if not l.startswith(JOUE_PAR)]
    ecarts = []
    if len(a) < 3 or len(b) < 3:
        print("IMPOSSIBLE : relevé de moins de 3 lignes")
        return 2
    ma, mb = LIGNE_3.match(a[2]), LIGNE_3.match(b[2])
    if not ma or not mb:
        ecarts.append((3, a[2], b[2]))
    elif ma.group(1, 2) != mb.group(1, 2):
        ecarts.append((3, f"découpage {ma.group(1)} lots de {ma.group(2)}", f"découpage {mb.group(1)} lots de {mb.group(2)}"))
    n = max(len(a), len(b))
    for i in range(n):
        if i == 2:
            continue
        la = a[i] if i < len(a) else "<absente>"
        lb = b[i] if i < len(b) else "<absente>"
        if la != lb:
            ecarts.append((i + 1, la, lb))
    if ecarts:
        print(f"REFUS : {len(ecarts)} différence(s) hors des heures et du nombre de lots joués en même temps")
        for k, la, lb in ecarts[:20]:
            print(f"  ligne {k}\n    local  : {la[:160]}\n    GitHub : {lb[:160]}")
        return 1
    print(f"IDENTIQUES : {n} lignes ; seule la ligne 3 diffère ou peut différer :\n  local  : {a[2]}\n  GitHub : {b[2]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
