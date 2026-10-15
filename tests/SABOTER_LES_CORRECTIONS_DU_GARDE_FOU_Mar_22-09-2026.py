#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Retire une à une les corrections du garde-fou (depuis le 20-09-2026) et montre quel cas d épreuve rougit.

① RÔLE — Prouver que chaque correction apportée au garde-fou — dans
  `programmes/CONTROLER_MA_LIVRAISON.py` ou dans `programmes/LIRE_LE_CODE.py`, qui calcule
  ce que le code fait — est surveillée par au moins un cas de
  `programmes/EPREUVES_DU_GARDE_FOU.py` : on retire la correction, on rejoue les cas, et
  au moins un doit changer de verdict.
② CONTEXTE D APPEL — À la main, depuis la racine du dépôt, par le relecteur ou l auteur.
  Aucune tâche automatique ne l appelle.
③ ENTRÉE — Aucun argument. Lit `programmes/CONTROLER_MA_LIVRAISON.py` et
  `programmes/LIRE_LE_CODE.py` ; copie en plus, dans chaque dossier jetable, les épreuves,
  `emp.py`, `programmes/QUI_TOUCHE_CE_FICHIER.py` et `programmes/FABRIQUER_LE_SOCLE.py`.
④ CONDITIONS D ENTRÉE — Être lancé depuis la racine du dépôt. Chacune des lignes visées
  (une par sabotage de la liste SABOTAGES) doit figurer une fois et une seule dans le
  fichier qu elle vise — le garde-fou ou LIRE_LE_CODE —, sinon le programme s arrête.
⑤ SORTIE — Un code de sortie, et un compte rendu affiché. 0 si chaque correction retirée
  fait rougir au moins un cas · 1 sinon, si une ligne visée est introuvable ou multiple, ou si le
  témoin, joué sans rien retirer, fait rougir un cas.
⑥ TRAITEMENT — D'abord un témoin, sans rien retirer : aucun cas ne doit rougir
  (ajouté le 30-09-2026). Puis pour chaque correction : ① copier le garde-fou et
  LIRE_LE_CODE, l un des deux avec la correction retirée, dans un dossier jetable, à côté
  des épreuves et des programmes voisins · ② jouer tous les cas · ③ afficher ceux qui
  rougissent.
⑦ UNITÉ — Des nombres de cas et des codes de sortie.
⑧ POURQUOI — Un jeu d épreuves qui reste vert quand on retire ce qu il teste n est pas une
  preuve, c est une décoration (R-731). Le sabotage intégré aux épreuves neutralise les
  REFUS du garde-fou ; il ne retire pas les CORRECTIONS, qui changent la façon de compter
  sans ajouter de refus. Déposé plutôt que jeté : un calibrage laissé dans un dossier
  temporaire ne peut être rejoué ni par son auteur le lendemain ni par le relecteur —
  c est la raison même pour laquelle les épreuves du garde-fou ont été écrites le 18-09.
⑨ CE QUI CLOCHE — Les corrections sont désignées par le TEXTE exact d une ligne : une
  réécriture de ces lignes fait s arrêter ce programme au lieu de le faire mentir, mais il
  faudra alors le mettre à jour. La correction de la portée est sabotée en
  vidant la liste des programmes, ce qui déclenche le refus « aucun programme » : le
  retour à l ancien comportement, fondé sur Git, n est pas rejoué ici.
⑩ EFFET — Crée un dossier temporaire pour le témoin et un par sabotage, et un par cas joué, jamais supprimés.
  N écrit rien dans le dépôt.
⑪ TERMINAISON — SORT DU PROGRAMME par sa dernière ligne, en 0 ou en 1 ; plus tôt, en 1,
  si une ligne visée est introuvable ou multiple, ou si le témoin rougit. Chaque cas joué
  lance le garde-fou dans un processus sans délai maximal.
"""
import os, shutil, subprocess, sys, tempfile
GARDE = open("programmes/CONTROLER_MA_LIVRAISON.py", encoding="utf-8").read()
LIRE = open("programmes/LIRE_LE_CODE.py", encoding="utf-8").read()
# Chaque correction est designee par UNE ligne et par le fichier ou elle vit. Depuis
# la decision de Jean-Luc du 22-09-2026, ce que le code fait est calcule dans
# `programmes/LIRE_LE_CODE.py` ; le garde-fou, lui, compare ce calcul a la marque.
SABOTAGES = [
    ("lire : la levée systématique", "LIRE",
     '    leve = (_leve_toujours(corps) and not generateur\n',
     '    leve = (False and not generateur\n'),
    ("lire : le couple rangé dans une variable", "LIRE",
     '            elif isinstance(v, ast.Name) and v.id in vars_:\n',
     '            elif False and isinstance(v, ast.Name) and v.id in vars_:\n'),
    ("lire : l appel à une fonction du même fichier", "LIRE",
     '            elif isinstance(v, ast.Call) and _cible(v, f) is not None:\n',
     '            elif False and isinstance(v, ast.Call):\n'),
    ("lire : le générateur", "LIRE",
     '    generateur = any(isinstance(n, (ast.Yield, ast.YieldFrom)) for n in propres)\n',
     '    generateur = False\n'),
    ("lire : les fonctions de tous les niveaux", "LIRE",
     '    return [n for n in ast.walk(arbre)\n',
     '    return [n for n in arbre.body\n'),
    ("lire : sortir par exit sans préfixe", "LIRE",
     '                    or (isinstance(x.func, ast.Name) and x.func.id in ("exit", "quit"))):\n',
     '                    or False):\n'),
    ("lire : l appel à une fonction imbriquée", "LIRE",
     '            return locales.get(fn_.id) or haut.get(fn_.id)\n',
     '            return haut.get(fn_.id)\n'),
    ("lire : l appel à une méthode par self", "LIRE",
     '            return classe_de[f].get(fn_.attr)\n',
     '            return None\n'),
    ("lire : toutes les branches qui lèvent", "LIRE",
     '        return bool(fin.orelse) and _leve_toujours(fin.body) and _leve_toujours(fin.orelse)\n',
     '        return False\n'),
    ("lire : os._exit", "LIRE",
     '            if isinstance(x.func, ast.Attribute) and x.func.attr == "_exit":\n',
     '            if False:\n'),
    ("lire : la variable qui reçoit un appel", "LIRE",
     '                    cv = _cible(v, f) if isinstance(v, ast.Call) else None\n',
     '                    cv = None\n'),
    ("lire : l appel à une fonction qui sort", "LIRE",
     '                    if sort_du_programme(h, chaine + [g]):\n',
     '                    if False:\n'),
    ("lire : la boucle d appels dans une variable ne fait pas abandonner", "LIRE",
     '                    elif cv is not None:\n'
     '                        vars_.setdefault(c.id, set()).add(1)\n',
     '                    elif cv is not None:\n'
     '                        return None\n'),
    ("lire : la sortie rattrapée ne compte pas", "LIRE",
     '                    rattrapes.update(id(z) for z in ast.walk(instr))\n',
     '                    pass\n'),
    ("lire : os._exit ne se rattrape pas", "LIRE",
     '                return True            # os._exit : rien ne le rattrape\n',
     '                pass\n'),
    ("garde-fou : la marque manquante est refusée", "GARDE",
     '                _faux.append(f"{_ou5} : fiche sans sa marque — relancer "\n'
     '                             f"programmes/MARQUER_LES_FICHES.py")\n',
     '                pass  # SABOTE\n'),
    ("garde-fou : la marque comparée au code", "GARDE",
     '                if _mq_rend5.group(1) != _rend5:\n',
     '                if False:\n'),
    ("garde-fou : l élément reconnu en début de ligne", "GARDE",
     r'                   if not re.search(rf"(?m)^\s*{c}", _d6)]' + '\n',
     '                   if c not in _d6]\n'),
    ("garde-fou : l apostrophe d un piège de R-755 ③", "GARDE",
     """                _motif = r"\\*\\*\\s*" + r"\\s+".join("['’]".join(re.escape(x) for x in re.split(r"['’]", w))\n""",
     """                _motif = r"\\*\\*\\s*" + r"\\s+".join(re.escape(w).replace("'", "['’]").replace("’", "['’]")\n"""),
    ("garde-fou : la portée, tous les programmes", "GARDE",
     '                  if x.endswith(".py"))\n',
     '                  if x.endswith(".py") and False)\n'),
]
nus = []
# LE TÉMOIN D'ABORD (relecteur du 30-09-2026) : sans correction retirée, aucun cas ne doit
# rougir. Sinon un cas qui rougit toujours — ici les cas R-755, faute des deux programmes
# voisins dont le garde-fou a besoin — ferait passer chaque sabotage pour « surveillé ».
TEMOIN = ("témoin, aucune correction retirée", "GARDE", "", "")
for nom, quel, avant, apres in [TEMOIN] + SABOTAGES:
    source = GARDE if quel == "GARDE" else LIRE
    if nom != TEMOIN[0] and source.count(avant) != 1:
        print(f"  ❌ ligne visée introuvable ou multiple : {nom}")
        sys.exit(1)
    d = tempfile.mkdtemp(prefix="sab_corr_")
    os.makedirs(os.path.join(d, "programmes"), exist_ok=True)
    shutil.copy("emp.py", os.path.join(d, "emp.py"))
    open(os.path.join(d, "programmes", "CONTROLER_MA_LIVRAISON.py"), "w", encoding="utf-8").write(
        GARDE.replace(avant, apres) if quel == "GARDE" else GARDE)
    open(os.path.join(d, "programmes", "LIRE_LE_CODE.py"), "w", encoding="utf-8").write(
        LIRE.replace(avant, apres) if quel == "LIRE" else LIRE)
    shutil.copy("programmes/EPREUVES_DU_GARDE_FOU.py", os.path.join(d, "programmes"))
    for voisin in ("QUI_TOUCHE_CE_FICHIER.py", "FABRIQUER_LE_SOCLE.py"):   # importés par epreuves_de (R-755 ②)
        shutil.copy(os.path.join("programmes", voisin), os.path.join(d, "programmes"))
    r = subprocess.run([sys.executable, "-c",
                        f"import sys; sys.path.insert(0, {os.path.join(d, 'programmes')!r}); "
                        "import EPREUVES_DU_GARDE_FOU as E; [E.jouer(*c) for c in E.CAS]"],
                       capture_output=True, text=True, errors="replace", cwd=d)
    rouges = [l.strip()[3:].split("  code")[0].strip() for l in r.stdout.split("\n")
              if l.strip().startswith("❌") and "code" in l]
    print(f"  correction retirée : {nom} -> {len(rouges)} cas rouge(s)")
    for x in rouges:
        print(f"     · {x}")
    if nom == TEMOIN[0]:
        if rouges:
            print("  ❌ LE TÉMOIN ROUGIT : aucun sabotage ne prouverait rien")
            sys.exit(1)
    elif not rouges:
        nus.append(nom)
print(f"  {len(SABOTAGES) - len(nus)}/{len(SABOTAGES)} corrections surveillées")
sys.exit(1 if nus else 0)
