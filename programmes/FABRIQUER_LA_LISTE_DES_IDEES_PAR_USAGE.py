#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fabrique etudes/IDEES_VIDEOS_INSTAGRAM/LISTE_PAR_USAGE.md : les idées tirées des
vidéos Instagram, rangées par USAGE (stratégie, protection, paramètre, taille de
la mise, connaissance), une ligne par idée, à partir du seul tableau
etudes/IDEES_VIDEOS_INSTAGRAM/idees_videos.csv.

① RÔLE — Répondre en un coup d'œil à « quelles stratégies, quels filtres, quelles
  protections les vidéos nous ont-elles donnés ? ». Le 20-11-2026 à 13h23,
  Jean-Luc demandait si tout ce qu'on apprend est repris « de façon très
  synthétique […] qu'on puisse ensuite les exploiter au travers de filtres, de
  stratégies ou autres ». Mesure faite à cette heure : 56 idées, réparties dans
  onze actions du BACKLOG et un tableau, aucune vue par usage. Décision de
  Jean-Luc à 13h44 : « Oui, liste générée ».
② CONTEXTE D'APPEL — À la main, par le Chat, après chaque ajout au tableau.
  Aucun lanceur automatique (non branché au circuit du soir).
③ ENTRÉE — La ligne de commande : la racine du dépôt (obligatoire), puis, en
  option, le fichier à écrire.
  USAGE : python3 programmes/FABRIQUER_LA_LISTE_DES_IDEES_PAR_USAGE.py <racine> [sortie.md]
④ CONDITIONS D'ENTRÉE — Le tableau existe, en UTF-8, séparateur « ; », avec au
  moins les colonnes id, video, producteur, idee_en_clair, case, testable,
  action_backlog.
⑤ SORTIE — UNE valeur, le code de sortie : 0 si toutes les idées sont rangées,
  1 si au moins une n'a pas pu l'être (elle est alors listée sous « NON
  CLASSÉES », et le fichier est quand même écrit), 2 si le tableau manque ou
  n'a pas ses colonnes. Le fichier Markdown est écrit à côté.
⑥ TRAITEMENT — ① lire le tableau · ② ranger chaque idée selon les chiffres de
  sa colonne « case » · ③ écrire une section par usage, dans l'ordre des
  numéros · ④ afficher les comptes.
⑦ UNITÉ — —
⑧ POURQUOI — Le tableau reste la SEULE source : recopier les idées au BACKLOG
  ferait deux textes qui finiraient par se contredire (R-708, « deux
  implémentations d'une même chose divergent toujours »). La liste est donc
  FABRIQUÉE et ne s'édite jamais à la main (R-728, « ce qui se calcule ne
  s'écrit jamais à la main »).
⑨ CE QUI CLOCHE — Le rangement dépend des mots écrits dans la colonne « case »
  (« 1 stratégie », « 2 protection »…) ; une case écrite autrement tombe en
  « NON CLASSÉES » et rend le code 1, elle n'est jamais devinée.
⑩ EFFET — Écrit un seul fichier.
⑪ TERMINAISON — Rend toujours la main ; aucun appel réseau.
"""
import csv
import hashlib
import os
import re
import sys

USAGES = [
    ("1", "STRATÉGIES — quoi acheter"),
    ("2", "PROTECTIONS ET CONTRÔLES DU JUGE — quand ne pas acheter, comment juger"),
    ("3", "PARAMÈTRES DE LA MOULINETTE — filtres et réglages à faire varier"),
    ("4", "TAILLE DE LA MISE ET PORTEFEUILLE"),
    ("5", "CONNAISSANCES ET IDÉES POUR PLUS TARD"),
    ("0", "PUBLICITÉS ET VIDÉOS SANS CONTENU"),
    ("D", "DOUBLONS — renvoient à d'autres idées"),
    ("X", "NON CLASSÉES — case illisible, à corriger dans le tableau"),
]
MOTS = r"(stratégie|protection|paramètre|taille|portefeuille|connaissance|plus tard)"
COLONNES = ("id", "video", "producteur", "idee_en_clair", "case", "testable", "action_backlog")


def classer(case):
    """Dit dans quels usages ranger une idée, d'après sa colonne « case ».

    ① RÔLE — Traduire « 2 protection + 3 paramètre » en ["2", "3"].
    ② CONTEXTE D'APPEL — `fabriquer`, une fois par idée.
    ③ ENTRÉE — `case` : le texte de la colonne, tel qu'écrit.
    ④ CONDITIONS D'ENTRÉE — Aucune : un texte vide rend ["X"].
    ⑤ SORTIE — UNE valeur : la liste des codes d'usage, sans doublon, dans
      l'ordre d'apparition ; ["0"] pour « — », ["D"] pour « voir I… »,
      ["X"] si rien n'est reconnu.
      [rend: 1]
    ⑥ TRAITEMENT — ① cas « — » et « voir » · ② chercher chaque chiffre 1 à 5
      suivi d'un mot d'usage.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un chiffre seul ne suffit pas : « (③) » ou « 2 939 » ne sont
      pas des cases ; le mot qui suit le confirme.
    ⑨ CE QUI CLOCHE — Un usage écrit sans son chiffre n'est pas vu.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    t = (case or "").strip()
    if t in ("—", "-"):
        return ["0"]
    if t.lower().startswith("voir "):
        return ["D"]
    codes = []
    for m in re.finditer(r"(?<![\d\w])([1-5])\s+" + MOTS, t):
        if m.group(1) not in codes:
            codes.append(m.group(1))
    return codes or ["X"]


def ligne(idee, autres, plus_tard=frozenset()):
    """Écrit la ligne Markdown d'une idée.

    ① RÔLE — Donner en une ligne : numéro, titre, testabilité, action, source.
    ② CONTEXTE D'APPEL — `fabriquer`, une fois par idée et par usage.
    ③ ENTRÉE — `idee` : un dictionnaire du tableau ; `autres` : les autres
      usages de la même idée (liste de codes) ; `plus_tard` : les numéros
      d'idées cités par l'action A-837 du BACKLOG (liste des idées « plus tard »).
    ④ CONDITIONS D'ENTRÉE — Les colonnes de COLONNES existent.
    ⑤ SORTIE — UNE valeur : la ligne, sans retour à la ligne final.
      [rend: 1]
    ⑥ TRAITEMENT — Titre = texte de l'idée avant le premier « : » ; source =
      colonne video avant le premier « · » ou « ( » ; testabilité
      = texte avant le premier « ; » ; producteur = avant la première
      parenthèse ou le premier tiret long.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une liste se lit vite ; le détail reste dans le tableau.
    ⑨ CE QUI CLOCHE — Un titre sans « : » est repris en entier.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    titre = idee["idee_en_clair"].split(" : ")[0].strip()
    test = idee["testable"].split(" ; ")[0].strip() or "—"
    prod = re.split(r" \(| —", idee["producteur"])[0].strip()
    action = idee["action_backlog"].strip() or "—"
    if action in ("—", "-") and idee["id"] in plus_tard:
        action = "A-837 (liste des idées « plus tard »)"
    aussi = (" · aussi en " + ", ".join(autres)) if autres else ""
    return (f"- **{idee['id']}** — {titre} · testable : {test} · action : {action}"
            f" · source : {idee['video'].split(' · ')[0].split(' (')[0]}, {prod}{aussi}")


def fabriquer(racine, sortie=None):
    """Lit le tableau, range les idées et écrit la liste.

    ① RÔLE — Le travail entier du programme.
    ② CONTEXTE D'APPEL — `__main__`, ou les épreuves.
    ③ ENTRÉE — `racine` : dossier du dépôt ; `sortie` : chemin du fichier, ou
      None pour etudes/IDEES_VIDEOS_INSTAGRAM/LISTE_PAR_USAGE.md.
    ④ CONDITIONS D'ENTRÉE — Voir ④ du module.
    ⑤ SORTIE — UNE valeur : le code de sortie (0, 1 ou 2, voir ⑤ du module).
      [rend: 1]
    ⑥ TRAITEMENT — Voir ⑥ du module.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir ⑧ du module.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit le fichier de sortie.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    src = os.path.join(racine, "etudes", "IDEES_VIDEOS_INSTAGRAM", "idees_videos.csv")
    if not os.path.isfile(src):
        print(f"ÉCHEC : tableau introuvable : {src}")
        return 2
    brut = open(src, "rb").read()
    idees = list(csv.DictReader(brut.decode("utf-8").splitlines(), delimiter=";"))
    manque = [c for c in COLONNES if not idees or c not in idees[0]]
    if manque:
        print(f"ÉCHEC : colonnes absentes : {manque}")
        return 2
    # Les idées sans action au tableau mais citées par A-837 (liste « plus tard ») :
    # la colonne action_backlog du tableau ne le dit pas toujours (mesure du 20-11-2026).
    plus_tard = frozenset()
    bk = os.path.join(racine, "BACKLOG_DECISIONS.md")
    if os.path.isfile(bk):
        for l in open(bk, encoding="utf-8").read().split("\n"):
            if l.startswith("| A-837 |"):
                plus_tard = frozenset(re.findall(r"\bI\d{2}\b", l))
    sections = {code: [] for code, _ in USAGES}
    for idee in idees:
        codes = classer(idee["case"])
        for c in codes:
            sections[c].append(ligne(idee, [x for x in codes if x != c], plus_tard))
    empreinte = hashlib.sha256(brut).hexdigest()[:12]
    out = [
        "# LES IDÉES DES VIDÉOS INSTAGRAM, RANGÉES PAR USAGE",
        "",
        "**FICHIER FABRIQUÉ — ne pas l'éditer à la main.** Il est refait par "
        "`programmes/FABRIQUER_LA_LISTE_DES_IDEES_PAR_USAGE.py` à partir du seul tableau "
        "`etudes/IDEES_VIDEOS_INSTAGRAM/idees_videos.csv` "
        f"(empreinte sha256 du tableau lu : `{empreinte}`, {len(idees)} idées). "
        "Le détail de chaque idée (étude publiée, vérification faite, avis, verdict) est dans le tableau ; "
        "le contexte et la méthode sont dans `LISEZ_MOI.md` du même dossier. "
        "Une idée peut apparaître sous plusieurs usages. Simulation uniquement : aucun ordre réel.",
        "",
        "Comment lire une ligne : **numéro** — titre de l'idée · testable : quand et sur quelles données · "
        "action : l'action du BACKLOG qui la porte · source : vidéo et producteur.",
    ]
    for code, nom in USAGES:
        if code == "X" and not sections[code]:
            continue
        out += ["", f"## {nom} ({len(sections[code])})", ""]
        out += sections[code] or ["- (aucune)"]
    chemin = sortie or os.path.join(racine, "etudes", "IDEES_VIDEOS_INSTAGRAM", "LISTE_PAR_USAGE.md")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    for code, nom in USAGES:
        print(f"{code} · {len(sections[code]):3d} · {nom.split(' —')[0]}")
    if sections["X"]:
        print(f"ATTENTION : {len(sections['X'])} idée(s) non classée(s)")
        return 1
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__.split("③")[1].split("④")[0])
        sys.exit(2)
    sys.exit(fabriquer(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
