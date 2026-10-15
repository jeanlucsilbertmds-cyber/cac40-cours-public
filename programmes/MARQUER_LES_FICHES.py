#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Écrit dans chaque fiche la MARQUE exacte de ce que sa fonction rend et de sa terminaison.

① RÔLE — **Remplacer une lecture du français par une comparaison exacte.** Le garde-fou
  `programmes/CONTROLER_MA_LIVRAISON.py` devinait le nombre de valeurs rendues en cherchant
  « UNE valeur », « DEUX valeurs »… dans le ⑤ de chaque fiche, et la terminaison en cherchant
  trois formules dans le ⑪. **Décision de Jean-Luc du 22-09-2026, après six défauts relevés
  par Cowork le même jour : « poser la marque exacte tout de suite ».** Ce programme calcule
  ces deux faits depuis le code et les écrit dans la fiche sous une forme fixe.
② CONTEXTE D APPEL — À la main, depuis la racine du dépôt, quand une fonction est écrite ou
  modifiée. Aucune tâche automatique ne l appelle.
③ ENTRÉE — `dossier` : le dossier des programmes à marquer, premier argument de la ligne de
  commande, `programmes` par défaut. `--essai` : ne rien écrire, seulement afficher.
④ CONDITIONS D ENTRÉE — Chaque fichier doit s analyser. Un fichier qui ne s analyse pas est
  nommé et laissé intact.
⑤ SORTIE — DEUX valeurs rendues par `marquer_un_fichier`, et pour le programme entier un code
  de sortie : 0 si tout a été marqué, 1 si un fichier n a pu être lu ou si une marque écrite
  contredit ce que la phrase du ⑤ annonçait — ces cas-là sont à lire à la main.
  [rend: 2]
⑥ TRAITEMENT — ① analyser le fichier · ② pour chaque fonction, à tous les niveaux, calculer
  ce qu elle rend et si elle rend la main · ③ comparer au nombre que la phrase annonçait, et
  le signaler quand les deux diffèrent · ④ écrire ou remplacer les deux marques dans la fiche
  · ⑤ réécrire le fichier seulement si son code, privé de ses textes, est inchangé.
⑦ UNITÉ — Des nombres de valeurs, sans unité physique.
⑧ POURQUOI — **Une liste de formules ne converge jamais** : chaque mot ajouté au garde-fou le
  22-09-2026 a produit un faux refus ailleurs — « une valeur » glané dans une phrase, puis
  « arrête le programme » qui parlait du programme appelant. Une marque ne se lit pas, elle
  se compare.
⑨ CE QUI CLOCHE — **La marque est calculée depuis le code : elle dit donc toujours vrai du
  code, et rien de la phrase qui l entoure.** C est le lecteur humain qui voit qu une phrase
  annonçant « DEUX valeurs » porte `[rend: 1]`. Le programme le signale au moment de marquer,
  une fois ; il ne le contrôlera plus ensuite.
⑩ EFFET — Réécrit les fichiers du dossier donné, sauf en mode essai. N écrit aucun autre
  fichier.
⑪ TERMINAISON — SORT DU PROGRAMME par sa dernière ligne. Aucun de ses appels ne peut ne pas
  revenir : ils lisent et écrivent des fichiers.
  [sort: oui]
⑫ DÉFINITIONS
  une fiche : le texte explicatif en tête d une fonction, qui porte ses onze ou douze éléments
  la marque : `[rend: …]` à la fin du ⑤ et `[sort: oui|non]` à la fin du ⑪, écrits par ce
    programme et comparés au code par le garde-fou
  le garde-fou : `programmes/CONTROLER_MA_LIVRAISON.py`, qui accepte ou refuse une livraison
"""
import ast, glob, os, re, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from LIRE_LE_CODE import faits_de_la_fonction, empreinte_du_code, fonctions_du_fichier


def marquer_un_fichier(chemin, essai):
    """Écrit les deux marques dans chaque fiche d un fichier, et rend ce qui a été fait.

    ① RÔLE — Poser `[rend: …]` et `[sort: …]` dans la fiche de chaque fonction du fichier,
      d après ce que le code fait réellement.
    ② CONTEXTE D APPEL — Depuis la partie principale de ce programme, une fois par fichier.
    ③ ENTRÉE — `chemin` : le fichier Python à marquer. `essai` : vrai pour ne rien écrire.
    ④ CONDITIONS D ENTRÉE — Le fichier doit s analyser.
    ⑤ SORTIE — DEUX valeurs : le nombre de fiches marquées, et la liste des fiches dont la
      phrase annonçait un autre nombre que la marque calculée.
      [rend: 2]
    ⑥ TRAITEMENT — ① lire et analyser · ② calculer les faits de chaque fonction · ③ écrire
      les marques de la dernière vers la première, pour que les positions restent justes ·
      ④ comparer l empreinte du code avant et après · ⑤ écrire le fichier.
    ⑦ UNITÉ — Des comptes de fiches.
    ⑧ POURQUOI — Marquer fichier par fichier permet de s arrêter au premier qui change du
      code, au lieu de réécrire tout le dossier.
    ⑨ CE QUI CLOCHE — Une fiche sans ⑤ ou sans ⑪ n est pas marquée, et rien ne le dit ici.
    ⑩ EFFET — Réécrit le fichier, sauf en mode essai.
    ⑪ TERMINAISON — Rend la main. LÈVE si le code a changé pendant le marquage, ce qui ne
      doit jamais arriver.
      [sort: non]
    ⑫ DÉFINITIONS
      la marque : `[rend: …]` à la fin du ⑤ et `[sort: oui|non]` à la fin du ⑪
    """
    source = open(chemin, encoding="utf-8").read()
    avant = empreinte_du_code(source)
    arbre = ast.parse(source)
    marques, discordances = 0, []
    a_faire = []
    for fn in fonctions_du_fichier(arbre):
        if not (fn.body and isinstance(fn.body[0], ast.Expr)
                and isinstance(fn.body[0].value, ast.Constant)
                and isinstance(fn.body[0].value.value, str)):
            continue
        brut = ast.get_source_segment(source, fn.body[0].value)
        if brut is None or not all(re.search(rf"(?m)^\s*{c}", brut) for c in "⑤⑪"):
            continue
        # **LES GUILLEMETS RESTENT AU DEHORS.** Le texte rendu par l arbre porte ses
        # guillemets ; poser la marque sans les retirer d abord l écrivait APRÈS le
        # guillemet fermant, et le fichier ne s analysait plus — mesuré le 22-09-2026 sur
        # dix-sept fichiers d un coup.
        ouvre = re.match(r"^[A-Za-z]*(\"\"\"|\'\'\'|\"|\')", brut)
        if not ouvre:
            continue
        tete, queue = brut[:ouvre.end()], ouvre.group(1)
        dedans = brut[ouvre.end():len(brut) - len(queue)]
        rend, sort = faits_de_la_fonction(fn, arbre)
        neuf = _poser(dedans, "⑤", "⑥", f"[rend: {rend}]")
        neuf = _poser(neuf, "⑪", "⑫", f"[sort: {'oui' if sort else 'non'}]")
        neuf = tete + neuf + queue
        annonce = _nombre_annonce(brut)
        if annonce is not None and annonce != rend:
            discordances.append(f"{os.path.basename(chemin)}:{fn.name} "
                                f"phrase « {annonce} » · code « {rend} »")
        if neuf != brut:
            a_faire.append((fn.body[0].value, neuf))
            marques += 1
    for noeud, neuf in sorted(a_faire, key=lambda x: -x[0].lineno):
        # **LES COLONNES SE COMPTENT EN OCTETS, LES TEXTES EN CARACTÈRES.** L arbre de
        # Python donne `col_offset` en octets ; une ligne accentuée en porte plus que de
        # caractères. Les mélanger a coupé huit fichiers au mauvais endroit, mesuré le
        # 22-09-2026. On convertit donc chaque colonne sur SA ligne.
        lignes = source.split("\n")
        def _place(no_ligne, colonne):
            """Rend la position d une colonne de l arbre dans le texte du fichier.

            ① RÔLE — Convertir une colonne comptée en octets par Python en une position
              comptée en caractères dans le texte.
            ② CONTEXTE D APPEL — Depuis `marquer_un_fichier`, deux fois par fiche à écrire.
            ③ ENTRÉE — `no_ligne` : le numéro de ligne, à partir de 1. `colonne` : la
              colonne en octets.
            ④ CONDITIONS D ENTRÉE — La ligne doit exister dans le fichier.
            ⑤ SORTIE — UNE valeur : la position en caractères depuis le début du texte.
              [rend: 1]
            ⑥ TRAITEMENT — Additionne les longueurs des lignes précédentes, puis convertit
              la colonne sur sa propre ligne.
            ⑦ UNITÉ — Des caractères.
            ⑧ POURQUOI — Une ligne accentuée porte plus d octets que de caractères : mélanger
              les deux a coupé huit fichiers au mauvais endroit le 22-09-2026.
            ⑨ CE QUI CLOCHE — Rien de relevé.
            ⑩ EFFET — Aucun.
            ⑪ TERMINAISON — Rend la main.
              [sort: non]
            ⑫ DÉFINITIONS — —
            """
            avant_ = sum(len(l) + 1 for l in lignes[:no_ligne - 1])
            ligne_ = lignes[no_ligne - 1]
            return avant_ + len(ligne_.encode("utf-8")[:colonne].decode("utf-8", "ignore"))
        debut = _place(noeud.lineno, noeud.col_offset)
        fin = _place(noeud.end_lineno, noeud.end_col_offset)
        source = source[:debut] + neuf + source[fin:]
    if empreinte_du_code(source) != avant:
        raise AssertionError(f"{chemin} : le code a changé pendant le marquage")
    if not essai and marques:
        open(chemin, "w", encoding="utf-8").write(source)
    return marques, discordances


def _poser(brut, signe, suivant, marque):
    """Écrit la marque à la fin d un élément d une fiche, en remplaçant celle qui s y trouvait.

    ① RÔLE — Poser une marque au bon endroit sans toucher au reste du texte.
    ② CONTEXTE D APPEL — Depuis `marquer_un_fichier`, deux fois par fiche.
    ③ ENTRÉE — `brut` : le texte de la fiche, sans ses guillemets.
      `signe` : le signe de l élément à marquer, guillemets exclus. `suivant` : le signe de l élément qui le
      suit, ou `None` s il n y en a pas. `marque` : le texte à poser.
    ④ CONDITIONS D ENTRÉE — L élément doit ouvrir une ligne de `brut`.
    ⑤ SORTIE — UNE valeur : le texte de la fiche, marque posée.
      [rend: 1]
    ⑥ TRAITEMENT — ① trouver la ligne qui ouvre l élément · ② trouver où il finit · ③ retirer
      toute marque déjà posée dans cet intervalle · ④ écrire la nouvelle à la fin, seule sur
      sa ligne, avec le retrait de l élément plus deux espaces.
    ⑦ UNITÉ — Aucune.
    ⑧ POURQUOI — Une marque posée deux fois, ou posée dans l élément voisin, ferait mentir le
      contrôle qu elle est censée rendre exact.
    ⑨ CE QUI CLOCHE — Si l élément suivant manque, la marque va à la fin de la fiche.
    ⑩ EFFET — Aucun : rend un texte, n écrit rien.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    ⑫ DÉFINITIONS — —
    """
    ouverture = re.search(rf"(?m)^([ \t]*){signe}", brut)
    if not ouverture:
        return brut
    retrait = ouverture.group(1)
    debut = ouverture.start()
    fin = len(brut)
    if suivant:
        apres = re.search(rf"(?m)^[ \t]*{suivant}", brut[ouverture.end():])
        if apres:
            fin = ouverture.end() + apres.start()
    corps = brut[debut:fin]
    corps = re.sub(r"(?m)^[ \t]*\[(?:rend|sort): [^\]]*\]\n", "", corps)
    corps = corps.rstrip() + f"\n{retrait}  {marque}\n"
    if fin == len(brut):
        corps = corps.rstrip() + f"\n{retrait}"
    return brut[:debut] + corps + brut[fin:]


def _nombre_annonce(brut):
    """Rend ce que la PHRASE du ⑤ annonce, pour le comparer une fois à ce que le code fait.

    ① RÔLE — Repérer, au moment de marquer, les fiches dont la phrase dit autre chose que le
      code : ce sont celles qu un humain doit relire.
    ② CONTEXTE D APPEL — Depuis `marquer_un_fichier`, une fois par fiche.
    ③ ENTRÉE — `brut` : le texte de la fiche.
    ④ CONDITIONS D ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : le nombre annoncé écrit en chiffres, `rien` quand la phrase dit
      qu elle ne rend rien, ou `None` quand la phrase n annonce aucun nombre lisible.
      [rend: 1]
    ⑥ TRAITEMENT — Cherche, dans le ⑤, la première des cinq formes écrites en toutes lettres,
      sans égard à la casse, ou les mots « ne rend rien ».
    ⑦ UNITÉ — Un compte de valeurs.
    ⑧ POURQUOI — **Cette lecture ne sert qu une fois, au marquage.** Le garde-fou ne lira plus
      jamais la phrase : c est tout l objet de la marque.
    ⑨ CE QUI CLOCHE — Une phrase qui annonce son compte autrement n est pas lue, et la fiche
      passe alors sans que personne la relise.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    ⑫ DÉFINITIONS — —
    """
    ouverture = re.search(r"(?m)^[ \t]*⑤", brut)
    if not ouverture:
        return None
    suite = brut[ouverture.start():]
    apres = re.search(r"(?m)^[ \t]*⑥", suite)
    zone = (suite[:apres.start()] if apres else suite).upper()
    zone = "".join(c for c in unicodedata.normalize("NFD", zone)
                   if unicodedata.category(c) != "Mn")
    trouve, place = None, None
    for mot, nb in (("UNE VALEUR", "1"), ("DEUX VALEURS", "2"), ("TROIS VALEURS", "3"),
                    ("QUATRE VALEURS", "4"), ("CINQ VALEURS", "5"),
                    ("NE REND RIEN", "rien"), ("NE REND JAMAIS RIEN", "rien")):
        i = zone.find(mot)
        if i >= 0 and (place is None or i < place):
            trouve, place = nb, i
    return trouve


def main():
    """Marque toutes les fiches d un dossier de programmes, et rend un code de sortie.

    ① RÔLE — Enchaîner le marquage sur tous les fichiers, afficher ce qui a été fait, et
      signaler les fiches dont la phrase contredit le code.
    ② CONTEXTE D APPEL — Depuis la ligne de commande, à la main.
    ③ ENTRÉE — La ligne de commande : `dossier` en premier argument, `--essai` pour ne rien
      écrire.
    ④ CONDITIONS D ENTRÉE — Le dossier doit exister et porter des fichiers Python.
    ⑤ SORTIE — UNE valeur : le code de sortie, 0 si tout s est bien passé, 1 s il reste une
      discordance à relire ou un fichier illisible.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire la ligne de commande · ② marquer chaque fichier · ③ afficher le
      compte et les discordances · ④ rendre le code de sortie.
    ⑦ UNITÉ — Des comptes de fiches.
    ⑧ POURQUOI — Un contrôle qui n a pas pu tourner rend un code non nul (R-734).
    ⑨ CE QUI CLOCHE — Rien de relevé.
    ⑩ EFFET — Réécrit les fichiers marqués, sauf en mode essai. Affiche.
    ⑪ TERMINAISON — Rend la main avec un code. Aucun de ses appels ne peut ne pas revenir.
      [sort: non]
    ⑫ DÉFINITIONS — —
    """
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    essai = "--essai" in sys.argv
    dossier = args[0] if args else "programmes"
    total, toutes, casses = 0, [], []
    for chemin in sorted(glob.glob(os.path.join(dossier, "*.py"))):
        try:
            marques, discordances = marquer_un_fichier(chemin, essai)
        except Exception as e:
            casses.append(f"{os.path.basename(chemin)} : {type(e).__name__} {e}")
            continue
        total += marques
        toutes.extend(discordances)
    print(f"  {total} fiche(s) marquée(s){' — ESSAI, rien écrit' if essai else ''}")
    for d in toutes:
        print(f"  ⚠️  À RELIRE — {d}")
    for c in casses:
        print(f"  ❌ {c}")
    return 1 if (toutes or casses) else 0


if __name__ == "__main__":
    sys.exit(main())
