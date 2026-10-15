#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dit ce qu une fonction rend et si elle rend la main, en lisant son CODE et jamais sa phrase.

① RÔLE — **Porter à UN SEUL endroit le calcul des deux faits que le garde-fou compare aux
  fiches** : combien de valeurs une fonction rend, et si elle rend la main. Le marqueur
  `programmes/MARQUER_LES_FICHES.py` écrit ces faits dans les fiches ; le garde-fou
  `programmes/CONTROLER_MA_LIVRAISON.py` les recalcule et compare. **Deux implémentations
  d une même chose divergent toujours (R-708) : il n y en a donc qu une, ici.**
② CONTEXTE D APPEL — Importé par le marqueur et par le garde-fou. Ne s exécute pas seul.
③ ENTRÉE — Aucune au niveau du fichier ; chaque fonction porte la sienne.
④ CONDITIONS D ENTRÉE — Les arbres passés viennent de `ast.parse` sur un fichier Python.
⑤ SORTIE — Aucune au niveau du fichier ; chaque fonction porte la sienne.
⑥ TRAITEMENT — Définit quatre fonctions et n en appelle aucune.
⑦ UNITÉ — Des comptes de valeurs rendues.
⑧ POURQUOI — Le 22-09-2026, corriger la façon de compter dans le garde-fou aurait demandé de
  la corriger aussi dans le marqueur : le même défaut aurait vécu à deux endroits.
⑨ CE QUI CLOCHE — Un appel à une fonction d un AUTRE fichier compte pour UNE valeur, faute
  de savoir ce qu elle rend. Inscrit au BACKLOG sous A-445.
⑩ EFFET — Aucun : ce fichier ne lit ni n écrit rien.
⑪ TERMINAISON — Rend la main à l import.
⑫ DÉFINITIONS
  les nœuds propres : les instructions d une fonction, sans celles des fonctions qu elle
    contient elle-même
"""
import ast, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import emp as _emp


def empreinte_du_code(source):
    """Rend l empreinte du code privé de tous ses textes explicatifs.

    ① RÔLE — Donner une empreinte qui ne change que si le CODE change, et jamais si un texte
      explicatif change. C est le contrôle du marqueur : il ne doit toucher que des textes.
    ② CONTEXTE D APPEL — Depuis le marqueur, avant et après avoir posé les marques.
    ③ ENTRÉE — `source` : le texte entier d un fichier Python.
    ④ CONDITIONS D ENTRÉE — Le fichier doit s analyser.
    ⑤ SORTIE — UNE valeur : l empreinte, seize caractères.
      [rend: 1]
    ⑥ TRAITEMENT — Passe la main à `empreinte` du fichier `emp.py`, à la racine du dépôt, qui
      retire les textes de l arbre avant de le résumer.
    ⑦ UNITÉ — Aucune.
    ⑧ POURQUOI — `emp.py` fait déjà ce travail et sert déjà de preuve dans les livraisons : le
      recopier ici en ferait deux versions qui divergeraient (R-708).
    ⑨ CE QUI CLOCHE — L import dépend de la place de ce fichier dans le dépôt.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. Son seul appel lit du texte et ne peut pas bloquer.
      [sort: non]
    ⑫ DÉFINITIONS — —
    """
    return _emp.empreinte(source)


def fonctions_du_fichier(arbre):
    """Rend toutes les fonctions d un fichier, à tous les niveaux.

    ① RÔLE — Donner la liste des fonctions à contrôler : celles du premier niveau, les
      méthodes de classe, et les fonctions écrites dans une autre fonction.
    ② CONTEXTE D APPEL — Depuis le marqueur et depuis le garde-fou, une fois par fichier.
    ③ ENTRÉE — `arbre` : l arbre d un fichier Python, rendu par `ast.parse`.
    ④ CONDITIONS D ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : la liste des nœuds de fonction, dans l ordre où ils apparaissent.
      [rend: 1]
    ⑥ TRAITEMENT — Parcourt l arbre entier et retient les définitions de fonction.
    ⑦ UNITÉ — Aucune.
    ⑧ POURQUOI — **Cowork a mesuré le 22-09-2026 que 34 fonctions sur 330 n étaient jamais
      confrontées à leur fiche** — 14 méthodes de classe et 20 fonctions imbriquées — parce
      que seul le premier niveau était parcouru.
    ⑨ CE QUI CLOCHE — Une fonction créée à l exécution échappe à ce relevé.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. Aucun de ses appels ne peut ne pas revenir.
      [sort: non]
    ⑫ DÉFINITIONS — —
    """
    return [n for n in ast.walk(arbre)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]


def noeuds_propres(fn):
    """Rend les instructions d une fonction, sans celles des fonctions qu elle contient.

    ① RÔLE — Éviter qu un `return`, un `yield` ou un `exit` écrit dans une fonction imbriquée
      soit compté à la fonction qui l enveloppe.
    ② CONTEXTE D APPEL — Depuis `faits_de_la_fonction` et depuis ses trois fonctions
      intérieures — `_cible`, `formes`, `sort_du_programme` —, pour chaque fonction qu elles
      examinent.
    ③ ENTRÉE — `fn` : le nœud d une fonction.
    ④ CONDITIONS D ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : la liste de ses nœuds propres.
      [rend: 1]
    ⑥ TRAITEMENT — Descend dans l arbre de la fonction en s arrêtant à chaque définition de
      fonction, de classe ou de fonction anonyme. **Premier essai, faux** : la définition
      imbriquée était écartée au moment d ajouter les enfants, mais celles du premier niveau
      du corps y entraient quand même, et leurs instructions étaient comptées.
    ⑦ UNITÉ — Aucune.
    ⑧ POURQUOI — `ast.walk` descend partout : une fonction imbriquée qui rend un couple
      faisait croire que celle qui la contient en rend un.
    ⑨ CE QUI CLOCHE — Rien de relevé.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main : la descente est finie puisque l arbre l est.
      [sort: non]
    ⑫ DÉFINITIONS — —
    """
    AUTRES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)
    pile, vus = list(fn.body), []
    while pile:
        n = pile.pop()
        vus.append(n)
        if isinstance(n, AUTRES):
            continue          # une fonction imbriquée : on la voit, on n y entre pas
        pile.extend(ast.iter_child_nodes(n))
    return vus


def faits_de_la_fonction(fn, arbre):
    """Rend ce que la fonction rend, et si elle sort du programme.

    ① RÔLE — Calculer depuis le code les deux faits que porte la marque d une fiche.
    ② CONTEXTE D APPEL — Depuis le marqueur, qui écrit la marque, et depuis le garde-fou, qui
      la compare. Une fois par fonction.
    ③ ENTRÉE — `fn` : le nœud de la fonction. `arbre` : l arbre du fichier entier, nécessaire
      pour résoudre un `return` qui appelle une autre fonction du même fichier.
    ④ CONDITIONS D ENTRÉE — `fn` doit appartenir à `arbre`.
    ⑤ SORTIE — DEUX valeurs : ce que la fonction rend, écrit `rien`, `générateur`, un nombre,
      plusieurs nombres séparés par « ou », ou `?` quand la chaîne d appels ne se résout pas ·
      et vrai si la fonction ne rend pas la main.
      [rend: 2]
    ⑥ TRAITEMENT — ① relever ses nœuds propres · ② un `yield` en fait un générateur · ③ pour
      chaque `return`, compter : un couple écrit en clair vaut sa longueur, une variable vaut
      ce qu on lui a affecté, un appel à une fonction du même fichier — écrite dans la
      fonction, au premier niveau, ou méthode de la même classe appelée par `self` — vaut ce
      que celle-ci rend — y compris quand l appel est d abord rangé dans une variable —,
      tout le reste vaut UNE valeur · ④ elle ne rend pas la main si elle appelle
      `sys.exit`, `os._exit`, `exit` ou `quit`, elle-même ou par une fonction du même
      fichier qu elle appelle, ou si toutes ses branches finissent par un `raise` sans
      qu elle porte de `return` ni de `yield`.
    ⑦ UNITÉ — Des comptes de valeurs.
    ⑧ POURQUOI — Ce sont les deux seuls faits qu une fiche peut contredire sans qu un lecteur
      s en aperçoive : le nombre de valeurs et la terminaison.
    ⑨ CE QUI CLOCHE — Un appel vers un autre fichier compte pour UNE valeur (A-445). Une
      variable affectée dans une seule branche est comptée comme si elle l était toujours.
      Un `try`, une boucle ou un `match` dont toutes les issues lèvent ne sont pas reconnus.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. La résolution des appels s arrête dès qu une fonction
      revient dans la chaîne.
      [sort: non]
    ⑫ DÉFINITIONS
      un générateur : une fonction qui produit ses valeurs une à une, par `yield`
    """
    haut = {n.name: n for n in arbre.body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    # **UN APPEL SE RÉSOUT AUSSI VERS UNE FONCTION IMBRIQUÉE OU UNE MÉTHODE — relevé de
    # Cowork, 22-09-2026.** Premier état : seules les fonctions du premier niveau du
    # fichier étaient suivies. Cas construit par lui : `return g()` où `g`, écrite dans
    # la fonction, rend un couple — marque posée `rend: 1`, et le garde-fou l acceptait.
    # On relève donc, pour chaque classe, ses méthodes, pour qu un `return self.m()` soit
    # suivi jusqu à `m`.
    classe_de = {}
    for c in ast.walk(arbre):
        if isinstance(c, ast.ClassDef):
            methodes = {m.name: m for m in c.body
                        if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))}
            for m in methodes.values():
                classe_de[m] = methodes
    def _cible(appel, f):
        """Rend la fonction du même fichier qu un appel désigne, ou `None`.

        ① RÔLE — Trouver quelle fonction un appel `nom(...)` ou `self.nom(...)` désigne,
          quand elle est écrite dans le même fichier.
        ② CONTEXTE D APPEL — Depuis `formes`, pour chaque `return` qui appelle et pour
          chaque variable qui reçoit un appel ; et depuis `sort_du_programme`, pour chaque
          appel qu elle suit.
        ③ ENTRÉE — `appel` : le nœud de l appel. `f` : la fonction qui le fait.
        ④ CONDITIONS D ENTRÉE — Aucune.
        ⑤ SORTIE — UNE valeur : le nœud de la fonction appelée, ou `None`.
          [rend: 1]
        ⑥ TRAITEMENT — ① un nom nu désigne d abord une fonction écrite DANS `f`, puis une
          fonction du premier niveau · ② `self.nom` désigne une méthode de la classe de `f`.
        ⑦ UNITÉ — Aucune.
        ⑧ POURQUOI — Une fonction écrite dans une autre masque celle du premier niveau qui
          porterait le même nom : c est elle que Python appelle.
        ⑨ CE QUI CLOCHE — Un appel vers un autre fichier, ou vers une méthode d une autre
          classe, n est pas résolu.
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        ⑫ DÉFINITIONS — —
        """
        fn_ = appel.func
        if isinstance(fn_, ast.Name):
            locales = {n.name: n for n in noeuds_propres(f)
                       if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
            return locales.get(fn_.id) or haut.get(fn_.id)
        if (isinstance(fn_, ast.Attribute) and isinstance(fn_.value, ast.Name)
                and fn_.value.id == "self" and f in classe_de):
            return classe_de[f].get(fn_.attr)
        return None

    def formes(f, chaine):
        """Rend l ensemble des nombres de valeurs que peut rendre une fonction.

        ① RÔLE — Compter, pour une fonction, toutes les formes de ce qu elle rend.
        ② CONTEXTE D APPEL — Depuis `faits_de_la_fonction`, et depuis elle-même quand un
          `return`, ou une variable, reçoit l appel d une autre fonction du même fichier.
        ③ ENTRÉE — `f` : le nœud de la fonction. `chaine` : les fonctions déjà traversées.
        ④ CONDITIONS D ENTRÉE — Aucune.
        ⑤ SORTIE — UNE valeur : l ensemble des nombres, ou `None` si la chaîne d appels
          revient sur une fonction déjà vue.
          [rend: 1]
        ⑥ TRAITEMENT — Relève les affectations, puis chaque `return`, et résout les appels.
        ⑦ UNITÉ — Des comptes de valeurs.
        ⑧ POURQUOI — Une fonction peut rendre une valeur dans une branche et un couple dans
          une autre : les deux doivent être connus.
        ⑨ CE QUI CLOCHE — Deux chemins vers la même fonction sont pris pour une boucle, et
          le compte devient inconnu.
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main : la chaîne d appels s arrête à la première répétition.
          [sort: non]
        ⑫ DÉFINITIONS — —
        """
        propres = noeuds_propres(f)
        vars_ = {}
        for n in propres:
            cibles = n.targets if isinstance(n, ast.Assign) else (
                [n.target] if isinstance(n, (ast.AnnAssign, ast.AugAssign)) else [])
            for c in cibles:
                if isinstance(c, ast.Name):
                    v = getattr(n, "value", None)
                    # **UNE VARIABLE QUI REÇOIT UN APPEL PREND CE QUE L APPEL REND —
                    # relevé de Cowork, 22-09-2026, second tour.** Cas construit par
                    # lui : `r = g()` puis `return r`, `g` rendant un couple — marque
                    # `rend: 1`. Le chemin du `return` direct résolvait l appel, celui
                    # de la variable non : les deux chemins suivent désormais la même
                    # règle, `_cible`.
                    cv = _cible(v, f) if isinstance(v, ast.Call) else None
                    # **UNE BOUCLE D APPELS DANS UNE VARIABLE N ABANDONNE PAS LA
                    # FONCTION — régression relevée par Cowork, 23-09-2026.** Premier
                    # état de la correction du 22-09 : `n = f(x - 1)` dans une fonction
                    # récursive faisait tout abandonner, et la marque passait de
                    # `rend: 1`, juste, à `rend: ?`. La variable reprend alors ce
                    # qu elle valait avant cette correction : UNE valeur.
                    sous = None
                    if cv is not None and cv not in chaine and cv is not f:
                        sous = formes(cv, chaine + [f])
                    if sous is not None:
                        vars_.setdefault(c.id, set()).update(sous)
                    elif cv is not None:
                        vars_.setdefault(c.id, set()).add(1)
                    else:
                        vars_.setdefault(c.id, set()).add(
                            len(v.elts) if isinstance(v, ast.Tuple) else 1)
        res = set()
        for n in propres:
            if not (isinstance(n, ast.Return) and n.value is not None):
                continue
            v = n.value
            if isinstance(v, ast.Tuple):
                res.add(len(v.elts))
            elif isinstance(v, ast.Name) and v.id in vars_:
                res |= vars_[v.id]
            elif isinstance(v, ast.Call) and _cible(v, f) is not None:
                cible = _cible(v, f)
                if cible in chaine:
                    return None
                sous = formes(cible, chaine + [f])
                if sous is None:
                    return None
                res |= sous
            else:
                res.add(1)
        return res
    propres = noeuds_propres(fn)
    generateur = any(isinstance(n, (ast.Yield, ast.YieldFrom)) for n in propres)
    ensemble = formes(fn, [])
    if generateur:
        rend = "générateur"
    elif ensemble is None:
        rend = "?"
    elif not ensemble:
        rend = "rien"
    else:
        rend = " ou ".join(str(x) for x in sorted(ensemble))
    corps = [x for x in fn.body
             if not (isinstance(x, ast.Expr) and isinstance(x.value, ast.Constant)
                     and isinstance(x.value.value, str))]
    # **TOUTES LES BRANCHES QUI LÈVENT — relevé de Cowork, 22-09-2026.** Premier état :
    # seule une DERNIÈRE instruction `raise` comptait. Cas construit par lui :
    # `if x: raise … else: raise …`, marqué `sort: non`, accepté. Une suite d instructions
    # lève toujours si sa dernière est un `raise`, ou un `if` dont les deux branches
    # lèvent toujours, `else` compris.
    leve = (_leve_toujours(corps) and not generateur
            and not any(isinstance(x, ast.Return) for x in propres))
    # **UNE FONCTION QUI APPELLE UNE FONCTION QUI SORT, SORT AUSSI — relevé de Cowork,
    # 22-09-2026, second tour.** Cas construit par lui : `f` appelle `g`, `g` fait
    # `sys.exit(2)` — `g` marquée `sort: oui`, `f` marquée `sort: non`. On suit donc les
    # appels vers les fonctions du même fichier, par `_cible`, en ne propageant que les
    # SORTIES du programme.
    # **CE QUI ÉTAIT ÉCRIT ICI LE 22-09 ÉTAIT FAUX, relevé par Cowork le 23-09-2026** :
    # « une sortie ne se rattrape pas ». En Python, `sys.exit`, `exit` et `quit` LÈVENT
    # l exception `SystemExit`, qu un `try` rattrape s il attrape `SystemExit`,
    # `BaseException`, ou tout, par un `except:` nu. Seul `os._exit` arrête le processus
    # sans rien lever. Une sortie placée dans un tel `try` ne compte donc pas.
    def sort_du_programme(g, chaine):
        """Dit si une fonction peut terminer le programme, elle-même ou par un appel.

        ① RÔLE — Suivre une sortie du programme à travers les appels du même fichier.
        ② CONTEXTE D APPEL — Depuis `faits_de_la_fonction`, puis depuis elle-même.
        ③ ENTRÉE — `g` : le nœud de la fonction. `chaine` : les fonctions déjà traversées.
        ④ CONDITIONS D ENTRÉE — Aucune.
        ⑤ SORTIE — UNE valeur : vrai si `g`, ou une fonction qu elle appelle dans le même
          fichier, appelle `sys.exit`, `os._exit`, `exit` ou `quit`.
          [rend: 1]
        ⑥ TRAITEMENT — Cherche un appel de sortie dans les nœuds propres de `g`, puis
          descend dans chaque appel que `_cible` résout, en s arrêtant sur une fonction
          déjà traversée.
        ⑦ UNITÉ — Aucune.
        ⑧ POURQUOI — Si `g` sort, l appel `g()` dans `f` peut faire que `f` ne rende
          jamais la main — sauf si `f` rattrape la sortie : `sys.exit` lève `SystemExit`,
          qu un `try` peut attraper. `os._exit`, lui, ne se rattrape pas.
        ⑨ CE QUI CLOCHE — Un appel conditionnel compte comme s il avait toujours lieu : la
          marque dit alors « peut sortir », jamais « sort toujours ». Un `raise SystemExit`
          écrit en toutes lettres n est pas vu comme une sortie (A-449).
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main : la descente s arrête à la première répétition.
          [sort: non]
        ⑫ DÉFINITIONS — —
        """
        noeuds = noeuds_propres(g)
        # Les nœuds placés dans un `try` qui rattrape `SystemExit`.
        rattrapes = set()
        for t in noeuds:
            if isinstance(t, ast.Try) and any(
                    h.type is None
                    or any(isinstance(e, ast.Name) and e.id in ("SystemExit", "BaseException")
                           for e in ([h.type] + list(getattr(h.type, "elts", []))))
                    for h in t.handlers):
                for instr in t.body:
                    rattrapes.update(id(z) for z in ast.walk(instr))
        for x in noeuds:
            if not isinstance(x, ast.Call):
                continue
            if isinstance(x.func, ast.Attribute) and x.func.attr == "_exit":
                return True            # os._exit : rien ne le rattrape
            if id(x) in rattrapes:
                continue
            if ((isinstance(x.func, ast.Attribute) and x.func.attr == "exit")
                    or (isinstance(x.func, ast.Name) and x.func.id in ("exit", "quit"))):
                return True
        for x in noeuds:
            if isinstance(x, ast.Call) and id(x) not in rattrapes:
                h = _cible(x, g)
                if h is not None and h not in chaine and h is not g:
                    if sort_du_programme(h, chaine + [g]):
                        return True
        return False
    sort = leve or sort_du_programme(fn, [])
    return rend, sort


def _leve_toujours(instructions):
    """Dit si une suite d instructions finit toujours par lever une erreur.

    ① RÔLE — Reconnaître une fonction qui ne rend jamais la main parce que chacune de ses
      branches se termine par un `raise`.
    ② CONTEXTE D APPEL — Depuis `faits_de_la_fonction`, sur le corps de la fonction, puis
      depuis elle-même sur les branches d un `if`.
    ③ ENTRÉE — `instructions` : une liste de nœuds, le corps sans son texte explicatif.
    ④ CONDITIONS D ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : vrai si toute exécution de cette suite finit par un `raise`.
      [rend: 1]
    ⑥ TRAITEMENT — Regarde la dernière instruction : un `raise` suffit ; un `if` suffit si
      ses deux branches, `else` compris, lèvent toujours ; tout le reste ne suffit pas.
    ⑦ UNITÉ — Aucune.
    ⑧ POURQUOI — Cowork a construit le 22-09-2026 une fonction dont les deux branches
      lèvent : elle était marquée « rend la main ».
    ⑨ CE QUI CLOCHE — Un `try`, une boucle ou un `match` dont toutes les issues lèvent ne
      sont pas reconnus.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main : la descente suit l arbre, qui est fini.
      [sort: non]
    ⑫ DÉFINITIONS — —
    """
    if not instructions:
        return False
    fin = instructions[-1]
    if isinstance(fin, ast.Raise):
        return True
    if isinstance(fin, ast.If):
        return bool(fin.orelse) and _leve_toujours(fin.body) and _leve_toujours(fin.orelse)
    return False
