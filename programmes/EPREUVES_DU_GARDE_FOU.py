#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Éprouve le garde-fou des livraisons, et rougit s il ne surveille plus rien.

① RÔLE — **Empêcher que le contrôle des livraisons s affaiblisse sans que
  personne le voie.** Le programme `programmes/CONTROLER_MA_LIVRAISON.py`
  décide si un travail part à la relecture ou s il est refusé. Ce programme-ci
  lui soumet des documents, accompagnés des programmes dont il doit confronter
  les fiches, en sachant à l avance s ils doivent être acceptés ou refusés, puis il neutralise ses refus un par un pour vérifier qu au moins
  une épreuve tombe à chaque fois.
② CONTEXTE D APPEL — À la main, après toute modification du garde-fou.
  **Aucun appelant automatique n a pu être établi sur cette copie du dépôt** :
  la recherche du nom EPREUVES_DU_GARDE_FOU dans les fichiers .py, .md, .yml et
  .yaml ne rend qu une seule mention, à la ligne 174 de
  `programmes/SYNTHETISER_LA_PHOTOGRAPHIE.py`, rangé aux archives le 24-09-2026 (A-452), qui est un document fabriqué et
  non un appel ; et le dossier `.github`, où vivraient les tâches du soir, est
  absent de cette copie. Qui le lance, et quand, reste donc inconnu.
③ ENTRÉE — Aucun argument de ligne de commande n est lu. Le programme se
  fournit lui-même : les cas de la liste `CAS`, documents et programmes écrits
  dans son propre texte, et le fichier
  `programmes/CONTROLER_MA_LIVRAISON.py`, cherché dans le dossier où il se
  trouve lui-même.
④ CONDITIONS D ENTRÉE — Le garde-fou doit exister à côté de ce fichier. Il faut
  pouvoir créer des dossiers temporaires et lancer des processus Python.
⑤ SORTIE — **Un code de sortie, et un compte rendu affiché.** 0 si tous les cas
  de la liste `CAS` rendent le verdict attendu ET si chaque refus du garde-fou est surveillé par
  au moins une épreuve · 1 sinon. Un contrôle qui n a pas pu tourner rend un
  code non nul (R-734).
⑥ TRAITEMENT — ① afficher l en-tête et le nombre de cas · ② s arrêter si le
  garde-fou est introuvable · ③ soumettre chaque cas au garde-fou, dans un
  dépôt jetable fabriqué par `batir`, et compter ceux qui rendent le code
  attendu · ④ neutraliser tour à tour chacun des refus du garde-fou et vérifier qu au moins une épreuve rougit ·
  ⑤ rendre 1 si un cas est tombé à côté ou si un refus n est surveillé par rien.
⑦ UNITÉ — Aucune grandeur physique : ce programme ne touche à aucune donnée de
  marché, aucun cours, aucune position. Les chiffres affichés sont des NOMBRES
  DE CAS, des NUMÉROS DE LIGNE dans le fichier du garde-fou, et des CODES DE
  SORTIE de processus.
⑧ POURQUOI — Le garde-fou a été modifié quatre fois en vingt-cinq minutes le
  17-09-2026, et chaque version a été cassée par la relecture. Son calibrage
  était du code jeté dans un dossier temporaire, non déposé : ni son auteur le
  lendemain ni le relecteur ne pouvaient le rejouer. R-731 impose des épreuves
  à tout code écrit ou modifié ; ce programme y avait échappé parce qu il est
  lui-même l outil qui vérifie les autres.
  **Chaque cas vient d une faute réellement commise et attrapée** : livraison
  sans passes affichées (12-09), passe affirmée sans sa preuve (13-09), ligne
  écrite à la main dans un bloc de sortie (14-09), « rien » sans énumérer
  (15-09), conformité affirmée sans l avoir ouverte (16-09), passe ② fausse
  deux fois de suite (17 et 18-09).
  **Et un cas qui DOIT passer est joué à côté de chaque cas qui doit échouer** :
  un jeu d épreuves qui reste vert quand on retire ce qu il teste n est pas une
  preuve, c est une décoration (R-731). Un garde-fou qui refuserait tout
  satisferait tous les cas qui doivent être refusés sans rien valoir.
⑨ CE QUI CLOCHE — **Deux défauts relevés le 19-09-2026 sont RÉGLÉS le
  20-09-2026.** ① Le cas de référence ne passait que si l on lançait ce
  programme depuis la racine du VRAI dépôt : le garde-fou rejoue les commandes
  citées depuis le dossier courant quand le dépôt du document n a pas de dossier
  `programmes`, et les deux commandes du document de référence n existaient que
  dans le vrai dépôt. Mesuré le 19-09-2026 : 8 cas justes sur 9 et 7 refus sur 9
  sans surveillance quand ces commandes ne rendaient pas ce qui était écrit.
  Chaque dépôt jetable porte désormais les deux scripts cités, `SCRIPTS_CITES` :
  **mesuré le 20-09-2026, tous les cas passent quand le programme est lancé
  depuis `/tmp`.** ② Le contrôle des fiches et celui des onze éléments n étaient
  surveillés par aucune épreuve, parce qu ils exigeaient un dépôt Git ; le
  garde-fou ne consulte plus Git depuis le 20-09-2026, et des cas leur sont
  dédiés. **Ce qui reste** : les deux scripts cités sont des doublures, ils ne
  font qu afficher la ligne attendue — le rejeu est éprouvé, pas les vrais
  programmes que le document de référence nomme. Et aucun cas n éprouve une
  fonction imbriquée — le contrôle des onze éléments, lui, les regarde : le
  28-09-2026 il a refusé `_une`, imbriquée dans le calibrage de
  `programmes/TENIR_LES_POSITIONS.py` et livrée sans fiche. **Un reste réglé le
  28-09-2026** : le cas « aucun programme à confronter » n a pas de dossier
  `programmes`, et le garde-fou rejouait donc ses commandes depuis le dossier
  d où l on lançait CE programme. Lancé depuis `programmes/`, le sabotage
  concluait à tort que ce refus n était surveillé par aucune épreuve (code 1).
  Le garde-fou est désormais lancé depuis `dossier_neutre()`.
⑩ EFFET — **N écrit rien dans le dépôt.** Crée des dossiers temporaires qu il
  ne supprime jamais : un par cas joué, un par copie sabotée du garde-fou, un
  par document rejoué pendant le sabotage — 79 au total sur l exécution mesurée
  le 19-09-2026, quand la liste comptait neuf cas. Il lance des
  processus Python et affiche un compte rendu.
⑪ TERMINAISON — **SORT DU PROGRAMME**, par la dernière ligne du fichier qui
  transforme la valeur rendue en code de sortie : 0 si tout tient, 1 sinon.
  Les processus lancés le sont sans délai maximal : un garde-fou qui bouclerait
  retiendrait le programme indéfiniment.
⑫ DÉFINITIONS
  le garde-fou : le programme `CONTROLER_MA_LIVRAISON.py`, qui accepte ou
    refuse un travail avant qu il parte à la relecture
  une livraison : le document `echanges/A_RELIRE.md`, qui porte le travail
    soumis à la relecture
  une passe : l une des cinq vérifications qu une livraison doit afficher —
    mandat inversé, famille, régression, non éprouvé, lien (R-740)
  une sortie capturée : un bloc de texte qui porte la trace d une exécution —
    une invite de commande ou un code de sortie — et non de la prose
  un refus : une ligne du garde-fou qui ajoute un motif à sa liste de refus et
    fait donc rendre le code 1
  le sabotage : retirer ce qu un contrôle surveille pour vérifier qu il tombe
  le relecteur : celui qui relit le travail de l autre, ici Cowork
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
  un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré rejoué à l'identique pour vérifier qu'il n'est pas revenu.
  un garde-fou : une limite qui, franchie, fait cesser a la strategie de prendre position tout en continuant a la mesurer.
"""
import os
import shutil
import subprocess
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
GARDE = os.path.join(ICI, "CONTROLER_MA_LIVRAISON.py")

# ── LE DOCUMENT QUI DOIT PASSER ────────────────────────────────────────
# Il porte tout ce que R-740 exige : les cinq passes, une sortie capturée
# sur les passes ① et ③, une énumération dans la passe ④.
CORRECT = """DÉCIDÉ · Rôle : porter le travail soumis à relecture.
Quand l'appeler : après chaque dépôt.

# À RELIRE — UN DOCUMENT CORRECT

**PRODUIT PAR : les épreuves · RELIT : personne**

Un texte quelconque qui décrit ce qui a été fait.

---

# R-740 — LES CINQ PASSES

**① MANDAT INVERSÉ** — le cas d'attaque et son résultat :
```
$ python3 programmes/EPREUVES_DU_SOCLE.py .
  toutes les épreuves passent
```

**② FAMILLE** — cherché ailleurs par un parcours :
```
$ grep -rn "le meme defaut" programmes/
  aucune occurrence
```

**③ RÉGRESSION** — le circuit tient :
```
$ python3 programmes/CONTRATS_DES_FICHIERS.py .
  6/6 épreuves passent
```

**④ NON ÉPROUVÉ** — trois points nommés : le premier point · le deuxième point · le troisième point.

**⑤ LIEN** — dépendent de ceci : rien pour l'instant.
"""



# ── LES PROGRAMMES QUE LE GARDE-FOU CONFRONTE A LEURS MARQUES — 22-09-2026 ──
# **Depuis la decision de Jean-Luc du 22-09-2026, le garde-fou ne lit plus le
# francais.** Chaque fiche porte `[rend: …]` a la fin de son ⑤ et `[sort: oui|non]`
# a la fin de son ⑪, ecrits par `programmes/MARQUER_LES_FICHES.py` d apres le code ;
# le garde-fou recalcule ces deux faits et les compare a la marque.
FICHE = """{role}

    ① RÔLE — Servir d épreuve au garde-fou.
    ② CONTEXTE D APPEL — Aucun appelant : ce texte n est jamais exécuté.
    ③ ENTRÉE — {trois}
    ④ CONDITIONS D ENTRÉE — Aucune.
    ⑤ SORTIE — {cinq}
      [rend: {rend}]
    ⑥ TRAITEMENT — Aucun.
    ⑦ UNITÉ — Aucune.
    ⑧ POURQUOI — Rejouer un défaut réellement rencontré.
    ⑨ CE QUI CLOCHE — Rien.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — {onze}
      [sort: {sort}]
    ⑫ DÉFINITIONS — —
    """
_RENDRE = "Rend la main après son calcul."
PROG_CORRECT = f"""def compter(liste):
    \"\"\"{FICHE.format(role='Compte.', trois='`liste` : ce qu on compte.',
                    cinq='UNE valeur, le nombre d éléments.', rend='1',
                    onze=_RENDRE, sort='non')}\"\"\"
    return len(liste)
"""
# CAS REEL, 20-09-2026 : `_backlog_et_origine` et `_au_depot`, dans
# `programmes/claude_FABRIQUER_LE_PILOTE.py` (R-732).
PROG_APPEL_LOCAL = f"""def _au_depot(motif, sous_dossiers):
    \"\"\"{FICHE.format(role='Trouve.', trois='`motif` : le nom. `sous_dossiers` : où chercher.',
                    cinq='DEUX valeurs : le chemin et son origine.', rend='2',
                    onze=_RENDRE, sort='non')}\"\"\"
    for c in sous_dossiers:
        return os.path.abspath(os.path.join(c, motif)), "dépôt"
    return None, None

def _backlog_et_origine():
    \"\"\"{FICHE.format(role='Désigne.', trois='Aucun paramètre.',
                    cinq='DEUX valeurs, rendues par l appel à `_au_depot`.', rend='2',
                    onze=_RENDRE, sort='non')}\"\"\"
    return _au_depot("backlog_decisions", _racines_depot())
"""
# CASSURE DE COWORK, 22-09-2026 : un couple range dans une variable.
PROG_COUPLE_EN_VARIABLE = f"""def couple(x):
    \"\"\"{FICHE.format(role='Range.', trois='`x` : la valeur.',
                    cinq='DEUX valeurs, rangées d abord dans une variable.', rend='2',
                    onze=_RENDRE, sort='non')}\"\"\"
    r = (x, 2 * x)
    return r
"""
# CASSURE DE COWORK, 22-09-2026 : un parametre etoile nomme avec son etoile.
PROG_PARAM_ETOILE = f"""def additionner(*cours):
    \"\"\"{FICHE.format(role='Ajoute.', trois='`*cours` : les séries.',
                    cinq='UNE valeur, la somme.', rend='1',
                    onze=_RENDRE, sort='non')}\"\"\"
    return sum(cours)
"""
# CAS REEL : `point_mort`, dans `programmes/MODULE_JUGEMENT.py` (A-439).
PROG_LEVE_TOUJOURS = f"""def point_mort(a, k):
    \"\"\"{FICHE.format(role='Façade.', trois='`a` : inutilisé. `k` : inutilisé.',
                    cinq='Ne rend rien : elle lève.', rend='rien',
                    onze='Elle ne rend jamais la main : elle lève systématiquement.',
                    sort='oui')}\"\"\"
    raise AttributeError("employer point_mort_en_fractions ou point_mort_en_pourcents")
"""
# CAS REEL : `_marcher`, dans `programmes/claude_FABRIQUER_LE_PILOTE.py`.
PROG_GENERATEUR = f"""def _marcher(racine):
    \"\"\"{FICHE.format(role='Parcourt.', trois='`racine` : le dossier.',
                    cinq='UNE valeur à chaque tour, produite par `yield`.',
                    rend='générateur', onze=_RENDRE, sort='non')}\"\"\"
    for x in racine:
        yield x
"""
# CAS REEL, 19-09-2026 : la fiche de `tenir` annoncait DEUX valeurs, le code rendait
# UN dictionnaire. C est la marque qu on falsifie ici.
PROG_MARQUE_FAUSSE = f"""def tenir(positions):
    \"\"\"{FICHE.format(role='Tient.', trois='`positions` : les positions.',
                    cinq='DEUX valeurs : les ouvertes et les closes.', rend='2',
                    onze=_RENDRE, sort='non')}\"\"\"
    return {{"ouvertes": positions}}
"""
PROG_MARQUE_SORT_FAUSSE = PROG_LEVE_TOUJOURS.replace("[sort: oui]", "[sort: non]")
PROG_SANS_MARQUE = PROG_CORRECT.replace("      [rend: 1]\n", "")
# CASSURE DE COWORK, 22-09-2026 : une methode de classe, jamais confrontee avant.
PROG_METHODE_DE_CLASSE = f"""class Serie:
    def deux(self, x):
        \"\"\"{FICHE.format(role='Rend un couple.', trois='`self` : la série. `x` : la valeur.',
                        cinq='UNE valeur.', rend='1', onze=_RENDRE, sort='non')}\"\"\"
        return x, x
"""
# CASSURE DE COWORK, 22-09-2026 : un element absent, masque par une etape numerotee.
PROG_ELEMENT_MASQUE = PROG_CORRECT.replace(
    "    ⑦ UNITÉ — Aucune.\n", "").replace(
    "    ⑥ TRAITEMENT — Aucun.",
    "    ⑥ TRAITEMENT — sept étapes, ① lire · ② compter · ③ ④ ⑤ ⑥ ⑦ rendre.")
# CASSURE DE COWORK, 22-09-2026 : `exit(2)` ecrit sans prefixe. Aucun programme du
# depot ne l ecrit ainsi aujourd hui ; ce cas est la pour que cela se voie s il arrive.
PROG_EXIT_NU = f"""def stopper(code):
    \"\"\"{FICHE.format(role='Arrête.', trois='`code` : le code de sortie.',
                    cinq='Ne rend rien : elle sort du programme.', rend='rien',
                    onze='Rend toujours la main après son appel.', sort='non')}\"\"\"
    exit(code)
"""
# CASSURES DE COWORK, 22-09-2026, second tour : trois formes dont la marque, posee
# par le marqueur, disait faux — et le garde-fou l acceptait. Chaque cas porte ici la
# marque VRAIE : avant la correction, le calcul en trouvait une autre et refusait.
PROG_APPEL_IMBRIQUE = f"""def f():
    \"\"\"{FICHE.format(role='Délègue.', trois='Aucun paramètre.',
                    cinq='DEUX valeurs, rendues par `g`.', rend='2', onze=_RENDRE, sort='non')}\"\"\"
    def g():
        \"\"\"{FICHE.format(role='Rend un couple.', trois='Aucun paramètre.',
                        cinq='DEUX valeurs.', rend='2', onze=_RENDRE, sort='non')}\"\"\"
        return 1, 2
    return g()
"""
PROG_APPEL_METHODE = f"""class Serie:
    def m(self):
        \"\"\"{FICHE.format(role='Rend un couple.', trois='`self` : la série.',
                        cinq='DEUX valeurs.', rend='2', onze=_RENDRE, sort='non')}\"\"\"
        return 1, 2

    def n(self):
        \"\"\"{FICHE.format(role='Délègue.', trois='`self` : la série.',
                        cinq='DEUX valeurs, rendues par `m`.', rend='2', onze=_RENDRE, sort='non')}\"\"\"
        return self.m()
"""
PROG_TOUTES_BRANCHES_LEVENT = f"""def refuser(x):
    \"\"\"{FICHE.format(role='Refuse.', trois='`x` : le motif.',
                    cinq='Ne rend rien : elle lève.', rend='rien',
                    onze='Ne rend jamais la main : chaque branche lève.', sort='oui')}\"\"\"
    if x:
        raise ValueError(x)
    else:
        raise KeyError(x)
"""
PROG_OS_EXIT = f"""import os
def couper(code):
    \"\"\"{FICHE.format(role='Coupe.', trois='`code` : le code de sortie.',
                    cinq='Ne rend rien : le processus s arrête.', rend='rien',
                    onze='Sort du programme sans rendre la main.', sort='oui')}\"\"\"
    os._exit(code)
"""
# CASSURES DE COWORK, 22-09-2026, troisieme tour : la meme famille, par une variable
# ou par un appel qui sort du programme. Chaque cas porte la marque VRAIE.
PROG_VARIABLE_APPEL = f"""def g():
    \"\"\"{FICHE.format(role='Rend un couple.', trois='Aucun paramètre.',
                    cinq='DEUX valeurs.', rend='2', onze=_RENDRE, sort='non')}\"\"\"
    return 1, 2

def f():
    \"\"\"{FICHE.format(role='Délègue.', trois='Aucun paramètre.',
                    cinq='DEUX valeurs, reçues de `g` dans une variable.', rend='2',
                    onze=_RENDRE, sort='non')}\"\"\"
    r = g()
    return r
"""
PROG_VARIABLE_METHODE = f"""class K:
    def duo(self):
        \"\"\"{FICHE.format(role='Rend un couple.', trois='`self` : l objet.',
                        cinq='DEUX valeurs.', rend='2', onze=_RENDRE, sort='non')}\"\"\"
        return 1, 2

    def f(self):
        \"\"\"{FICHE.format(role='Délègue.', trois='`self` : l objet.',
                        cinq='DEUX valeurs, reçues de `duo` dans une variable.', rend='2',
                        onze=_RENDRE, sort='non')}\"\"\"
        r = self.duo()
        return r
"""
PROG_APPEL_QUI_SORT = f"""import sys
def g():
    \"\"\"{FICHE.format(role='Sort.', trois='Aucun paramètre.',
                    cinq='Ne rend rien.', rend='rien',
                    onze='Sort du programme.', sort='oui')}\"\"\"
    sys.exit(2)

def f():
    \"\"\"{FICHE.format(role='Appelle g.', trois='Aucun paramètre.',
                    cinq='Ne rend rien.', rend='rien',
                    onze='Peut ne pas rendre la main : g sort du programme.', sort='oui')}\"\"\"
    g()
"""
# REGRESSIONS DE MA MAIN, RELEVEES PAR COWORK LE 23-09-2026 : deux marques justes
# avant la correction du 22-09, fausses apres. Chaque cas porte la marque VRAIE.
PROG_SORTIE_RATTRAPEE = f"""import sys
def g():
    \"\"\"{FICHE.format(role='Sort.', trois='Aucun paramètre.', cinq='Ne rend rien.',
                    rend='rien', onze='Sort du programme.', sort='oui')}\"\"\"
    sys.exit(2)

def f():
    \"\"\"{FICHE.format(role='Rattrape la sortie de g.', trois='Aucun paramètre.',
                    cinq='UNE valeur.', rend='1', onze=_RENDRE, sort='non')}\"\"\"
    try:
        g()
    except SystemExit:
        pass
    return 1
"""
PROG_RECURSIVE_EN_VARIABLE = f"""def f(x):
    \"\"\"{FICHE.format(role='Compte à rebours.', trois='`x` : le départ.',
                    cinq='UNE valeur.', rend='1', onze=_RENDRE, sort='non')}\"\"\"
    if x == 0:
        return 0
    n = f(x - 1)
    return n + 1
"""
PROG_OS_EXIT_DANS_UN_TRY = f"""import os
def f():
    \"\"\"{FICHE.format(role='Coupe, même rattrapée.', trois='Aucun paramètre.',
                    cinq='UNE valeur, jamais atteinte.', rend='1',
                    onze='Sort du programme : os._exit ne se rattrape pas.', sort='oui')}\"\"\"
    try:
        os._exit(3)
    except BaseException:
        pass
    return 1
"""
PROG_SANS_FICHE = PROG_CORRECT + """
def nue(x):
    return x
"""


def sans(bloc, quoi):
    """Rend le document de référence privé d une de ses parties.

    ① RÔLE — **Fabriquer un document fautif en retirant du document correct
      exactement la partie qu un contrôle surveille.** C est le sabotage exigé par
      R-731 : on retire ce que le contrôle surveille, et le contrôle doit tomber ;
      s il passe encore, il ne surveillait rien.
    ② CONTEXTE D APPEL — Au chargement du module, pendant la construction de la
      liste des cas. **Un seul appel dans tout le fichier**, celui qui bâtit le
      deuxième cas, celui où le titre de la passe de régression est retiré.
    ③ ENTRÉE — `bloc` : le texte dont on retire une partie ; l unique appel lui
      passe le document de référence du module · `quoi` : le fragment à retirer ;
      l unique appel lui passe le titre de la passe ③, soit la chaîne
      « **③ RÉGRESSION** — le circuit tient : ».
    ④ CONDITIONS D ENTRÉE — Les deux sont du texte. Aucune vérification que le
      fragment demandé se trouve bien dans le document.
    ⑤ SORTIE — **UNE valeur : le texte privé de TOUTES les occurrences du
      fragment.** Le remplacement n est pas borné à la première.
      [rend: 1]
    ⑥ TRAITEMENT — ① remplacer chaque occurrence du fragment par du vide ·
      ② rendre le texte obtenu.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — **Le retrait est écrit une seule fois, ici, au lieu d être recopié
      dans chaque cas.** Un même geste écrit à deux endroits finit par diverger
      (R-708). Et le retrait se fait sur le document de référence, jamais sur un
      document écrit à part : un cas fautif doit différer du cas correct par une
      seule chose, sinon on ne sait pas ce qui a déclenché le refus.
    ⑨ CE QUI CLOCHE — **Un fragment absent passe en silence, et le cas bâti dessus
      est compté juste.** Mesuré le 19-09-2026 : appelée avec un fragment
      inexistant, elle rend un texte strictement identique au document de
      référence ; ce texte soumis au garde-fou rendait alors le code 1, qui est
      justement le code attendu d un cas fautif, et la ligne affichée était « OK »,
      parce que le document de référence était lui-même refusé pour une autre
      raison. **Depuis le 20-09-2026 le document de référence passe : un fragment
      absent rend un texte accepté, le cas attend un refus, et il rougit.** Le
      défaut se voit désormais ; il n est pas corrigé — la fonction ne vérifie
      toujours pas que le fragment existe.
    ⑩ EFFET — **Ne change rien** : elle rend un nouveau texte, l original reste
      intact. Aucun fichier, aucun réseau.
    ⑪ TERMINAISON — Rend la main à tous les coups. Aucun de ses appels ne peut
      rester bloqué : elle n emploie que le remplacement de texte du langage.
      [sort: non]
    """
    return bloc.replace(quoi, "")


# ── LES CAS ────────────────────────────────────────────────────────────
# Chacun porte : son nom, le document, et ce qui doit arriver.
# **UN CAS QUI DOIT PASSER EST JOUÉ POUR CHAQUE CONTRÔLE.**

# ── R-755 ② ET ③ — 30-09-2026 (A-494, décision de Jean-Luc du 29-09 à 09h36) ──
# Le garde-fou compare les programmes à la version officielle (origin/main) : chaque
# dépôt jetable est donc un vrai dépôt Git dont la version de départ tient lieu de
# version officielle. Un montage dit ce qu on écrit AVANT cette version (registre,
# épreuves) et ce qu on change APRÈS (le travail livré).
_PIEGE_SORTIE = "```\n$ python3 programmes/EPREUVES_DU_SOCLE.py .\n  toutes les épreuves passent\n```\n"
# Le troisième porte une apostrophe, comme un vrai piège du registre : le 30-09-2026 à 06h35,
# le garde-fou ne savait pas le reconnaître et refusait toute livraison qui modifie un programme.
PIEGES_FAUX_REGISTRE = ("un lecteur du même fichier oublié", "une épreuve sans dents",
                        "un témoin qui n'emprunte pas le chemin du calcul réel")
CORRECT_PIEGES = CORRECT + "\n**PIÈGES DE R-755 ③**\n\n" + "".join(
    f"**{pg}** — écarté :\n{_PIEGE_SORTIE}\n" for pg in PIEGES_FAUX_REGISTRE)
REGISTRE_R755 = ("# REGISTRE\n\n### R-755 — UN TRAVAIL DE CODE SE LIVRE AVEC SES ÉPREUVES\n\n"
                 "③ **Le relecteur reçoit la liste des pièges :**\n"
                 + "".join(f"- **{pg}** — exemple ;\n" for pg in PIEGES_FAUX_REGISTRE)
                 + "Un piège nouveau trouvé en relecture s ajoute à cette liste.\n\n### R-756 — SUITE\n")
REGISTRE_SANS_LISTE = REGISTRE_R755.split("③")[0] + "### R-756 — SUITE\n"
EPREUVE_DE_CAS = "# éprouve programmes/cas.py\n"
CAS_CODE_CHANGE = PROG_CORRECT.replace("    return len(liste)\n", "    return len(list(liste))\n")
CAS_TEXTE_CHANGE = PROG_CORRECT.replace("Servir d épreuve au garde-fou.", "Servir d épreuve au garde-fou, texte changé.")
PROG_NEUF = PROG_CORRECT.replace("def compter(", "def compter_aussi(")
MONTAGE_MODIFIE = {"fichiers": {"gouvernance/REGISTRE_REGLES.md": REGISTRE_R755},
                   "apres": {"programmes/cas.py": CAS_CODE_CHANGE}}
MONTAGE_EPROUVE = {"fichiers": {"gouvernance/REGISTRE_REGLES.md": REGISTRE_R755,
                                "tests/EPREUVE_DE_CAS.py": EPREUVE_DE_CAS},
                   "apres": {"programmes/cas.py": CAS_CODE_CHANGE}}

CAS = [
    # ① le cas de référence — il doit passer, sinon tout le reste ne prouve rien
    ("document correct", CORRECT, 0,
     "le cas de reference : sans lui, un garde-fou qui refuse tout passerait"),

    # ② les cinq passes — faute du 12-09 : livraisons sans passes affichées
    ("passe ③ absente", sans(CORRECT, "**③ RÉGRESSION** — le circuit tient :"), 1,
     "R-740 : les cinq passes s affichent avec la livraison ou il n y a pas de livraison"),

    # ③ sortie capturée — faute du 13-09 : une passe affirmée sans sa preuve
    ("passe ① sans sortie capturée",
     CORRECT.replace("```\n$ python3 programmes/EPREUVES_DU_SOCLE.py .\n"
                     "  toutes les épreuves passent\n```", "rien trouvé"), 1,
     "R-728 : ce qui se mesure ne s ecrit pas a la main"),

    # ④ sortie fabriquée — faute du 14-09 : une ligne ecrite a la main
    #    dans un bloc de sortie, que la commande ne rend pas
    ("sortie fabriquée",
     CORRECT.replace("  6/6 épreuves passent",
                     "  6/6 épreuves passent\n  et tout va bien par ailleurs"), 1,
     "la commande citee ne rend pas cette ligne"),

    # ⑤ passe ④ sans énumération — faute du 15-09 : « rien » sans nommer
    ("passe ④ dit « rien » sans énumérer",
     CORRECT.replace("trois points nommés : le premier point · le deuxième point · "
                     "le troisième point.", "rien à signaler."), 1,
     "ce qui n a pas ete eprouve se NOMME, un par un"),

    # ⑥ passe ② sans sortie — faute des 17 et 18-09 : deux affirmations fausses
    #    de suite dans la seule passe qui s ecrivait sans lancer d outil
    ("passe ② sans sortie capturée",
     CORRECT.replace("```\n$ grep -rn \"le meme defaut\" programmes/\n"
                     "  aucune occurrence\n```", "rien trouvé de semblable."), 1,
     "la passe ② s ecrivait sans outil, et elle a ete fausse deux fois de suite"),

    # ⑦ deux marqueurs — faute du 14-09 : un document portant deux tampons,
    #    dont l un ment forcement
    ("deux lignes de contrôle",
     CORRECT + "\n<!-- CONTROLE 0000000000000000 · 2026-01-01 00h00 Paris -->\n"
               "<!-- CONTROLE 1111111111111111 · 2026-01-01 00h00 Paris -->\n", 1,
     "deux tampons dans un document : l un des deux ment"),

    # ⑧ R-744 — la mesure vient avant l ecriture, jamais apres.
    #    **La forme exacte est reprise du calibrage interne du garde-fou**, au
    #    lieu d etre devinee : un corps long dont la PREMIERE sortie capturee
    #    n arrive qu a la fin. Un document qui mesure apres avoir ecrit son
    #    propos JUSTIFIE au lieu de contraindre.
    #    Mon premier essai de ce cas ne declenchait pas, et **il masquait le trou
    #    au sabotage : une epreuve qui echoue toujours passe pour surveillante.**
    ("mesure placée après le propos (R-744)",
     CORRECT.replace("Un texte quelconque qui décrit ce qui a été fait.",
                     "\n".join(f"phrase {k} du propos, écrite avant toute mesure"
                               for k in range(300))), 1,
     "R-744 : un document qui mesure apres avoir ecrit justifie au lieu de contraindre"),

    # LE CAS MAL CONSTRUIT A ETE REMPLACE — 18-09-2026.
    # J en avais ecrit un a la main ; **il ne declenchait pas, parce que je ne
    # savais pas reproduire la forme exacte que le controle surveille.**
    # **Et il etait inutile : le SABOTAGE DU PROGRAMME, plus bas, neutralise ce
    # refus et verifie qu une epreuve rougit. Il prouve la couverture sans que
    # j aie a deviner la forme du document fautif.**
    # Un cas ecrit a la main qui ne declenche pas est pire qu absent : il fait
    # croire que le controle est surveille.

    # ⑧ conformité sans preuve — faute du 16-09 : « complet » sans l ouvrir
    ("conformité affirmée sans preuve",
     CORRECT.replace("Un texte quelconque qui décrit ce qui a été fait.",
                     "Le document est complet et conforme au registre."), 1,
     "R-720 : citer c est avoir ouvert"),

    # ── LA MARQUE — 22-09-2026. Le garde-fou ne lit plus le francais : il compare
    #    `[rend: …]` et `[sort: …]` a ce que le code fait. Un cas qui doit PASSER
    #    prouve qu une fiche juste n est pas accusee ; un cas qui doit ECHOUER
    #    prouve que le controle n est pas devenu muet.
    ("marque juste, appel à une fonction du même fichier", CORRECT, 0,
     "cas réel du 20-09 : return _au_depot(...) rend un couple",
     {"cas.py": PROG_APPEL_LOCAL}),
    ("marque juste, couple rangé dans une variable", CORRECT, 0,
     "cassure de Cowork du 22-09 : r = (x, 2*x) puis return r",
     {"cas.py": PROG_COUPLE_EN_VARIABLE}),
    ("marque juste, paramètre étoilé", CORRECT, 0,
     "cassure de Cowork du 22-09 : le ③ écrit `*cours`",
     {"cas.py": PROG_PARAM_ETOILE}),
    ("marque juste, fonction qui lève toujours", CORRECT, 0,
     "cas réel A-439 : point_mort, recopié tel quel",
     {"cas.py": PROG_LEVE_TOUJOURS}),
    ("marque juste, générateur", CORRECT, 0,
     "cas réel : _marcher produit ses valeurs par yield",
     {"cas.py": PROG_GENERATEUR}),
    ("marque contredite par le code", CORRECT, 1,
     "cas réel du 19-09 : deux valeurs annoncées, un dictionnaire rendu",
     {"cas.py": PROG_MARQUE_FAUSSE}),
    ("marque de terminaison contredite", CORRECT, 1,
     "une fonction qui lève toujours, marquée « sort: non »",
     {"cas.py": PROG_MARQUE_SORT_FAUSSE}),
    ("fiche sans marque", CORRECT, 1,
     "sans marque rien n est confronté, et le contrôle doit le dire (R-734)",
     {"cas.py": PROG_SANS_MARQUE}),
    ("méthode de classe", CORRECT, 1,
     "cassure de Cowork du 22-09 : 34 fonctions jamais confrontées",
     {"cas.py": PROG_METHODE_DE_CLASSE}),
    ("élément masqué par une étape numérotée", CORRECT, 1,
     "cassure de Cowork du 22-09 : le ⑦ d une étape tenait lieu du ⑦ UNITÉ",
     {"cas.py": PROG_ELEMENT_MASQUE}),
    ("sortie par exit sans préfixe", CORRECT, 1,
     "cassure de Cowork du 22-09 : exit(2) marqué « sort: non »",
     {"cas.py": PROG_EXIT_NU}),
    ("marque juste, appel à une fonction imbriquée", CORRECT, 0,
     "cassure de Cowork du 22-09 : return g() où g rend un couple",
     {"cas.py": PROG_APPEL_IMBRIQUE}),
    ("marque juste, appel à une méthode par self", CORRECT, 0,
     "cassure de Cowork du 22-09 : return self.m() où m rend un couple",
     {"cas.py": PROG_APPEL_METHODE}),
    ("marque juste, toutes les branches lèvent", CORRECT, 0,
     "cassure de Cowork du 22-09 : if … raise … else … raise",
     {"cas.py": PROG_TOUTES_BRANCHES_LEVENT}),
    ("marque juste, os._exit", CORRECT, 0,
     "cassure de Cowork du 22-09 : os._exit termine le processus",
     {"cas.py": PROG_OS_EXIT}),
    ("marque juste, variable qui reçoit un appel", CORRECT, 0,
     "cassure de Cowork du 22-09 : r = g() puis return r",
     {"cas.py": PROG_VARIABLE_APPEL}),
    ("marque juste, variable qui reçoit une méthode", CORRECT, 0,
     "cassure de Cowork du 22-09 : r = self.duo() puis return r",
     {"cas.py": PROG_VARIABLE_METHODE}),
    ("marque juste, appel à une fonction qui sort", CORRECT, 0,
     "cassure de Cowork du 22-09 : f appelle g, g fait sys.exit",
     {"cas.py": PROG_APPEL_QUI_SORT}),
    ("marque juste, sortie rattrapée", CORRECT, 0,
     "régression relevée par Cowork le 23-09 : try: g() except SystemExit",
     {"cas.py": PROG_SORTIE_RATTRAPEE}),
    ("marque juste, récursive en variable", CORRECT, 0,
     "régression relevée par Cowork le 23-09 : n = f(x - 1) puis return n + 1",
     {"cas.py": PROG_RECURSIVE_EN_VARIABLE}),
    ("marque juste, os._exit dans un try", CORRECT, 0,
     "os._exit arrête le processus sans lever : aucun try ne le rattrape",
     {"cas.py": PROG_OS_EXIT_DANS_UN_TRY}),
    ("fonction sans ses onze éléments", CORRECT, 1,
     "toute fonction porte ses onze premiers éléments",
     {"cas.py": PROG_SANS_FICHE}),
    ("aucun programme à confronter", CORRECT, 1,
     "R-734 : un contrôle qui n a rien pu confronter le dit",
     None),

    # R-755 ② et ③ — 30-09-2026 (A-494) : la base est la version officielle
    ("R-755 : sans version officielle", CORRECT, 1,
     "R-734 : sans origin/main, les programmes modifiés ne sont pas mesurés — refus",
     {"cas.py": PROG_CORRECT}, {"sans_git": True}),
    ("R-755 : programme modifié sans épreuve", CORRECT_PIEGES, 1,
     "R-755 ② : un programme dont le code diffère de la version officielle a une épreuve",
     {"cas.py": PROG_CORRECT}, MONTAGE_MODIFIE),
    ("R-755 : modifié ET COMMITÉ, sans épreuve", CORRECT_PIEGES, 1,
     "défaut du 20-09 : commiter ne doit pas faire taire le contrôle",
     {"cas.py": PROG_CORRECT}, {**MONTAGE_MODIFIE, "commiter_apres": True}),
    ("R-755 : programme NEUF sans épreuve", CORRECT_PIEGES, 1,
     "un programme neuf, non suivi par git, est un programme modifié",
     {"cas.py": PROG_CORRECT}, {"fichiers": {"gouvernance/REGISTRE_REGLES.md": REGISTRE_R755},
               "apres": {"programmes/neuf.py": PROG_NEUF}}),
    ("R-755 : programme modifié avec son épreuve", CORRECT_PIEGES, 0,
     "une épreuve de tests/ qui nomme le programme suffit ; les pièges sont écartés",
     {"cas.py": PROG_CORRECT}, MONTAGE_EPROUVE),
    ("R-755 : apostrophe typographique dans le document", CORRECT_PIEGES.replace("n'emprunte", "n’emprunte"), 0,
     "le registre écrit « n'emprunte », le document « n’emprunte » : le même piège (30-09-2026)",
     {"cas.py": PROG_CORRECT}, MONTAGE_EPROUVE),
    ("R-755 : texte seul changé, sans épreuve", CORRECT, 0,
     "une fiche corrigée n est pas un changement de code : ni épreuve ni pièges exigés",
     {"cas.py": PROG_CORRECT}, {"apres": {"programmes/cas.py": CAS_TEXTE_CHANGE}}),
    ("R-755 : un piège sans sa sortie", CORRECT_PIEGES.replace(
        "**une épreuve sans dents** — écarté :\n" + _PIEGE_SORTIE, "**une épreuve sans dents** — écarté.\n"), 1,
     "R-755 ③ : chaque piège porte la sortie qui l écarte",
     {"cas.py": PROG_CORRECT}, MONTAGE_EPROUVE),
    ("R-755 : pièges sur une ligne, une sortie", CORRECT + "\n**" + "** · **".join(PIEGES_FAUX_REGISTRE)
     + "** — écartés :\n" + _PIEGE_SORTIE, 1,
     "relecteur du 30-09 : une seule sortie ne sert pas à tous les pièges",
     {"cas.py": PROG_CORRECT}, MONTAGE_EPROUVE),
    ("R-755 : piège cité sans gras", CORRECT_PIEGES.replace("**une épreuve sans dents**", "une épreuve sans dents"), 1,
     "relecteur du 30-09 : une phrase qui cite le piège n est pas son intitulé",
     {"cas.py": PROG_CORRECT}, MONTAGE_EPROUVE),
    ("R-755 : programme neuf au nom accentué", CORRECT_PIEGES, 1,
     "relecteur du 30-09 : git échappait les noms accentués, le programme passait inaperçu",
     {"cas.py": PROG_CORRECT}, {"fichiers": {"gouvernance/REGISTRE_REGLES.md": REGISTRE_R755},
                                "apres": {"programmes/ÉPREUVE_NEUVE.py": PROG_NEUF}}),
    ("R-755 : liste des pièges illisible", CORRECT_PIEGES, 1,
     "R-734 : sans la liste de R-755 ③, le contrôle ne peut pas tourner — refus",
     {"cas.py": PROG_CORRECT}, {**MONTAGE_EPROUVE, "fichiers": {"gouvernance/REGISTRE_REGLES.md": REGISTRE_SANS_LISTE,
                                               "tests/EPREUVE_DE_CAS.py": EPREUVE_DE_CAS}}),
]




# ── LES DEUX COMMANDES QUE LE DOCUMENT DE REFERENCE CITE — 20-09-2026 ──────
# Le garde-fou REJOUE chaque commande citee depuis la racine du depot ou vit le
# document, **si cette racine porte un dossier `programmes` ; sinon, depuis le
# dossier courant.** Jusqu au 20-09-2026 le depot d epreuve n avait pas de
# dossier `programmes` : les commandes du document de reference se rejouaient
# donc dans le VRAI depot, par la seule grace du dossier d ou l on lancait ce
# programme. Lance d ailleurs, le cas de reference tombait. **Mesure du
# 20-09-2026 : des que le depot d epreuve a recu son dossier `programmes`, les
# cinq cas qui doivent passer ont ete refuses pour « sortie fabriquee ».**
# Ces deux scripts rendent exactement les lignes que le document ecrit sous
# leur invite. Ils ne portent aucune fonction, donc aucune fiche a confronter.
# **Le cas « sortie fabriquee » reste vrai** : il ajoute une ligne que ces
# scripts ne rendent pas.
SCRIPTS_CITES = {
    "EPREUVES_DU_SOCLE.py": 'print("  toutes les épreuves passent")\n',
    "CONTRATS_DES_FICHIERS.py": 'print("  6/6 épreuves passent")\n',
}

_DEFAUT = object()


def _ecrire(d, fichiers):
    """Écrit des fichiers dans le dépôt jetable.

    ① RÔLE — Poser les fichiers d un montage.
    ② CONTEXTE D APPEL — `batir`, deux fois : avant et après la version de départ.
    ③ ENTRÉE — `d` : le dossier jetable · `fichiers` : un dictionnaire, chemin
      relatif vers texte.
    ④ CONDITIONS D ENTRÉE — Pouvoir écrire dans `d`.
    ⑤ SORTIE — Ne rend rien.
      [rend: rien]
    ⑥ TRAITEMENT — pour chaque fichier, créer son dossier puis l écrire.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — un seul endroit pour une même écriture (R-708).
    ⑨ CE QUI CLOCHE — un fichier déjà présent est écrasé sans le dire.
    ⑩ EFFET — ÉCRIT des fichiers dans le dossier jetable.
    ⑪ TERMINAISON — Rend la main après les écritures.
      [sort: non]
    """
    for rel, contenu in fichiers.items():
        os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
        open(os.path.join(d, rel), "w", encoding="utf-8").write(contenu)


def batir(texte, programmes=_DEFAUT, montage=None):
    """Fabrique un dépôt jetable où le garde-fou trouvera un document et des programmes.

    ① RÔLE — **Construire, en un seul endroit, le dépôt d épreuve que le
      garde-fou examine** : un dossier jetable qui porte le document à contrôler
      sous `echanges/A_RELIRE.md` et, sauf demande contraire, un dossier
      `programmes` dont le garde-fou confrontera les fiches à leur code.
    ② CONTEXTE D APPEL — Deux appelants, dans ce fichier : `jouer`, une fois par
      cas, et `saboter_le_programme`, une fois par cas qui doit être refusé et
      par refus neutralisé.
    ③ ENTRÉE — `texte` : le document à contrôler, une chaîne. `programmes` : un
      dictionnaire dont chaque clé est un nom de fichier et chaque valeur le
      texte Python à y écrire ; `None` pour ne créer AUCUN dossier `programmes` ;
      omis, un seul programme correct, `PROG_CORRECT`. `montage` (30-09-2026) : un
      dictionnaire facultatif — `fichiers`, écrits AVANT la version de départ ;
      `apres`, écrits APRÈS ; `commiter_apres`, vrai pour enregistrer ces
      changements ; `sans_git`, vrai pour ne pas faire de dépôt Git.
    ④ CONDITIONS D ENTRÉE — Pouvoir créer un dossier temporaire et y écrire ;
      `git` doit être installé, sauf avec `sans_git`.
    ⑤ SORTIE — UNE valeur : le chemin absolu du document écrit, une chaîne.
      [rend: 1]
    ⑥ TRAITEMENT — ① créer un dossier jetable · ② y écrire le document sous
      `echanges/A_RELIRE.md` · ③ si des programmes sont fournis, créer
      `programmes` et y écrire chacun · ④ écrire les `fichiers` du montage ·
      ⑤ sauf `sans_git`, faire du dossier un dépôt Git, enregistrer la version de
      départ et la nommer `origin/main`, puis écrire les fichiers `apres` et, si
      demandé, les enregistrer · ⑥ rendre le chemin du document.
    ⑦ UNITÉ — Aucune grandeur : des chemins et des textes.
    ⑧ POURQUOI — **Deux endroits fabriquaient ce dépôt, `jouer` et
      `saboter_le_programme`, chacun à sa façon.** Depuis le 20-09-2026 le
      garde-fou refuse un dépôt sans programmes : si un seul des deux avait
      appris à en écrire, le sabotage aurait vu tous ses documents refusés pour
      cette seule raison, et conclu à tort que chaque refus était surveillé.
      Deux implémentations d une même chose divergent toujours (R-708).
    ⑨ CE QUI CLOCHE — Le dossier créé n est jamais supprimé, comme ceux que
      `jouer` créait avant cette fonction.
    ⑩ EFFET — Crée un dossier temporaire et y écrit un fichier, plus un par
      programme fourni et par fichier du montage ; y LANCE `git` pour créer le dépôt
      jetable.
    ⑪ TERMINAISON — Rend la main après avoir écrit. Aucun de ses appels ne peut
      bloquer au-delà d une écriture de fichier.
      [sort: non]
    ⑫ DÉFINITIONS
      le garde-fou : le programme `CONTROLER_MA_LIVRAISON.py`, qui accepte ou
        refuse un travail avant qu il parte à la relecture
      une fiche : le texte explicatif écrit en tête d une fonction, qui porte ses
        onze ou douze éléments
    """
    if programmes is _DEFAUT:
        programmes = {"cas.py": PROG_CORRECT}
    d = tempfile.mkdtemp(prefix="epreuve_")
    os.makedirs(os.path.join(d, "echanges"), exist_ok=True)
    p = os.path.join(d, "echanges", "A_RELIRE.md")
    open(p, "w", encoding="utf-8").write(texte)
    if programmes is not None:
        os.makedirs(os.path.join(d, "programmes"), exist_ok=True)
        for nom, source in {**SCRIPTS_CITES, **programmes}.items():
            open(os.path.join(d, "programmes", nom), "w", encoding="utf-8").write(source)
    montage = montage or {}
    _ecrire(d, montage.get("fichiers", {}))
    if not montage.get("sans_git"):
        # la version de départ tient lieu de version officielle (origin/main)
        g = ["git", "-C", d, "-c", "user.name=epreuve", "-c", "user.email=epreuve@local"]
        for a in (["init", "-q"], ["add", "-A"], ["commit", "-q", "-m", "base"],
                  ["update-ref", "refs/remotes/origin/main", "HEAD"]):
            subprocess.run(g + a, capture_output=True, check=True)
        _ecrire(d, montage.get("apres", {}))
        if montage.get("commiter_apres"):
            for a in (["add", "-A"], ["commit", "-q", "-m", "travail"]):
                subprocess.run(g + a, capture_output=True, check=True)
    return p


_NEUTRE = []


def dossier_neutre():
    """Fabrique, une fois, le dossier d où le garde-fou est lancé pendant les épreuves.

    ① RÔLE — **Donner au garde-fou un dossier de lancement qui ne dépend pas de
      l endroit d où l on lance ces épreuves.** Ce dossier porte un sous-dossier
      `programmes` avec les deux scripts que le document de référence cite, et
      rien d autre.
    ② CONTEXTE D APPEL — Depuis `jouer`, une fois par cas, et depuis
      `saboter_le_programme`, une fois par cas rejoué contre une copie sabotée.
      Seul le premier appel crée le dossier ; les suivants rendent le même.
    ③ ENTRÉE — Aucune.
    ④ CONDITIONS D ENTRÉE — Pouvoir créer un dossier temporaire et y écrire.
    ⑤ SORTIE — UNE valeur : le chemin absolu du dossier, une chaîne.
      [rend: 1]
    ⑥ TRAITEMENT — ① si le dossier existe déjà pour ce processus, le rendre ·
      ② sinon créer un dossier jetable, y créer `programmes`, y écrire chacun
      des scripts de `SCRIPTS_CITES` · ③ le retenir et le rendre.
    ⑦ UNITÉ — Aucune grandeur : un chemin.
    ⑧ POURQUOI — **Quand le dépôt d épreuve n a pas de dossier `programmes`,
      le garde-fou rejoue les commandes citées depuis le DOSSIER COURANT**
      (`CONTROLER_MA_LIVRAISON.py`, `_rac = "."`). C est le cas « aucun
      programme à confronter ». Mesure du 28-09-2026 : lancées depuis la racine
      du dépôt, les épreuves rendaient « OK refus ligne 1110 surveillé » ;
      lancées depuis `programmes/`, sur le même code, « ❌ refus ligne 1110
      AUCUNE ÉPREUVE NE LE VOIT », code 1. Depuis `programmes/`, la commande
      citée `python3 programmes/EPREUVES_DU_SOCLE.py .` ne trouve rien, le rejeu
      ajoute un second refus, et neutraliser le premier ne suffit plus à faire
      passer le cas. **Le verdict de couverture dépendait donc du dossier de
      lancement.** Depuis la racine, il dépendait en outre du VRAI dépôt : le
      garde-fou recopiait tout le dépôt et y lançait les vraies épreuves du
      socle. Un dossier neutre, identique à chaque lancement, retire les deux
      dépendances.
    ⑨ CE QUI CLOCHE — Le dossier créé n est jamais supprimé, comme ceux de
      `batir`.
    ⑩ EFFET — Au premier appel : crée un dossier temporaire et y écrit un
      fichier par script cité. Ensuite : aucun.
    ⑪ TERMINAISON — Rend la main après au plus quelques écritures de fichiers.
      Aucun de ses appels ne peut bloquer.
      [sort: non]
    ⑫ DÉFINITIONS
      le garde-fou : le programme `CONTROLER_MA_LIVRAISON.py`, qui accepte ou
        refuse un travail avant qu il parte à la relecture
      le rejeu : relancer chaque commande citée dans le document et comparer sa
        sortie réelle à la sortie écrite
    """
    if not _NEUTRE:
        d = tempfile.mkdtemp(prefix="neutre_")
        os.makedirs(os.path.join(d, "programmes"), exist_ok=True)
        for nom, source in SCRIPTS_CITES.items():
            with open(os.path.join(d, "programmes", nom), "w", encoding="utf-8") as f:
                f.write(source)
        _NEUTRE.append(d)
    return _NEUTRE[0]


def jouer(nom, texte, attendu, motif, programmes=_DEFAUT, montage=None):
    """Écrit le document dans un fichier jetable et lance le garde-fou dessus.

    ① RÔLE — **Soumettre un document au garde-fou et dire si le verdict est celui
      qu on attendait.** C est l unité de mesure du programme : un cas, un verdict.
    ② CONTEXTE D APPEL — Depuis la fonction principale, une fois par cas de la
      liste `CAS`. Le sabotage des refus, lui, relance le garde-fou directement
      sans passer par elle, mais construit son dépôt jetable par la même
      fonction `batir`.
    ③ ENTRÉE — `nom` : le libellé du cas, affiché en tête de la ligne de résultat,
      par exemple « sortie fabriquée » · `texte` : le contenu du document à
      soumettre · `attendu` : le code de sortie que le garde-fou doit rendre, 0
      pour un cas qui doit passer et 1 pour un cas fautif · `motif` : la phrase
      qui explique ce que le cas surveille, affichée uniquement quand le cas tombe
      à côté · `programmes` : les programmes du dépôt jetable, transmis tels quels
      à `batir`. Omis, un programme correct ; `None`, aucun dossier
      `programmes` · `montage` : transmis tel quel à `batir` (30-09-2026).
    ④ CONDITIONS D ENTRÉE — Le fichier du garde-fou doit exister ; la fonction
      principale l a vérifié avant le premier appel. Il faut pouvoir créer un
      dossier temporaire et lancer un processus Python.
    ⑤ SORTIE — **UNE valeur : vrai si le garde-fou a rendu le code attendu, faux
      sinon.** Le détail part à l affichage, pas dans la valeur rendue.
      [rend: 1]
    ⑥ TRAITEMENT — ①② faire fabriquer par `batir` le dépôt jetable qui porte le
      document sous `echanges/A_RELIRE.md` et ses programmes · ③ lancer le
      garde-fou sur ce fichier dans un processus séparé, depuis le dossier
      `dossier_neutre()` · ④ comparer le code rendu
      au code attendu · ⑤ afficher une ligne de résultat portant le nom du cas, le
      code obtenu et le code attendu · ⑥ si le cas tombe à côté, afficher le motif
      puis les lignes de la sortie du garde-fou qui contiennent un point médian ou
      le mot REFUS, tronquées à 86 caractères · ⑦ rendre le verdict.
    ⑦ UNITÉ — Des CODES DE SORTIE de processus. Les deux autres nombres sont des
      NOMBRES DE CARACTÈRES d affichage : 38 pour la largeur de la colonne du nom,
      86 pour la troncature des lignes de sortie recopiées.
    ⑧ POURQUOI — **Le document est écrit sous `echanges/A_RELIRE.md` et non sous un
      nom quelconque** : le garde-fou déduit la racine du dépôt en remontant de
      deux dossiers depuis le fichier qu on lui donne, et c est ce chemin qui sert
      à rejouer les commandes citées. **Et il est écrit dans un dossier jetable, pas
      dans le dépôt** : quand le garde-fou accepte un document, il le RÉÉCRIT pour
      y poser en queue une ligne de contrôle portant l empreinte du texte accepté.
      L éprouver sur le vrai fichier de livraison le modifierait.
    ⑨ CE QUI CLOCHE — Le cas « aucun programme à confronter » crée un dépôt sans
      dossier `programmes` : pour lui seul, le garde-fou rejoue les commandes
      citées depuis le dossier courant. **Depuis le 28-09-2026 ce dossier courant
      est fixé** : le garde-fou est lancé depuis `dossier_neutre()`, qui porte les
      deux scripts cités. Avant, le verdict de ce cas ne changeait pas, mais le
      SABOTAGE du refus « aucun programme » en dépendait : lancé depuis
      `programmes/`, il concluait à tort que ce refus n était surveillé par
      aucune épreuve (mesure du 28-09-2026, refus ligne 1110).
    ⑩ EFFET — **Crée un dossier temporaire par appel, par `batir`, et ne le
      supprime jamais.** Y écrit le document et les programmes du cas. Lance un processus Python. Quand
      le garde-fou accepte le document, il réécrit ce fichier temporaire.
    ⑪ TERMINAISON — Rend la main après le verdict. **Le processus lancé l est sans
      délai maximal** : si le garde-fou ne se terminait pas, cette fonction ne
      reviendrait pas non plus.
      [sort: non]
    ⑫ DÉFINITIONS
      le garde-fou : le programme `CONTROLER_MA_LIVRAISON.py`, qui accepte ou
        refuse un travail avant qu il parte à la relecture
      une ligne de contrôle : la ligne que ce programme pose en queue d un document accepté, portant l empreinte de seize caractères du texte validé
    
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en étant qu'une copie de lecture
      le détail : le fichier `registre_experiences.csv`, une ligne par expérience
      le sabotage : retirer ce qu un contrôle surveille pour vérifier qu il tombe
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    p = batir(texte, programmes, montage)
    r = subprocess.run([sys.executable, GARDE, p],
                       capture_output=True, text=True, errors="replace",
                       cwd=dossier_neutre())
    ok = r.returncode == attendu
    print(f"  {'OK ' if ok else '❌ '} {nom:<38} code {r.returncode} "
          f"(attendu {attendu})")
    if not ok:
        print(f"       {motif}")
        for l in (r.stdout + r.stderr).split("\n"):
            if "·" in l or "REFUS" in l:
                print(f"       {l.strip()[:86]}")
    return ok


def saboter_le_programme():
    """Neutralise chaque refus du garde-fou, et exige qu une épreuve rougisse.

    ① RÔLE — **Vérifier que le jeu d épreuves couvre bien chacun des refus du
      garde-fou**, et nommer ceux que rien ne surveille.
    ② CONTEXTE D APPEL — Depuis la fonction principale, une seule fois, après que
      tous les cas de la liste `CAS` ont été joués.
    ③ ENTRÉE — Aucun paramètre. Elle lit le fichier du garde-fou désigné par la
      constante GARDE en tête du module, et la liste `CAS` du même module.
    ④ CONDITIONS D ENTRÉE — Le fichier du garde-fou doit être lisible. Il faut
      pouvoir créer des dossiers temporaires et lancer des processus Python.
    ⑤ SORTIE — **UNE valeur : la liste des NUMÉROS DE LIGNE des refus qu aucune
      épreuve ne voit**, comptés à partir de 1. Liste vide si tous sont surveillés.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire le texte du garde-fou · ② relever les lignes qui
      contiennent le texte `refus.append` · ③ pour chacune,
      recopier le programme en remplaçant cette ligne et ses lignes de continuation
      par une instruction vide de même indentation, puis écrire la copie dans un
      dossier jetable · ④ lui soumettre chaque cas qui doit être refusé, dans un
      dépôt jetable fabriqué par `batir` comme pour `jouer`, en lançant la copie
      depuis `dossier_neutre()` — c est ici que ce dossier change un verdict : le
      cas « aucun programme à confronter » rejoue ses commandes depuis le dossier
      de lancement —, en s arrêtant au premier qui ne rend plus le code 1 · ⑤ afficher pour ce refus
      s il est surveillé ou non · ⑥ rendre la liste des refus non surveillés.
    ⑦ UNITÉ — Des NUMÉROS DE LIGNE dans le fichier du garde-fou, comptés à partir
      de 1 alors que la lecture du fichier les compte à partir de 0, d où le +1 à
      l affichage et dans la valeur rendue. Le reste est un nombre de refus et des
      codes de sortie.
    ⑧ POURQUOI — **Le sabotage du document ne suffit pas.** Cowork l a relevé le
      18-09-2026 : « les épreuves ne sabotent que le DOCUMENT, jamais le
      PROGRAMME ». Retirer une partie du document ne peut éprouver que les
      contrôles qu une partie de document déclenche ; deux contrôles passaient au
      travers sans qu aucune épreuve ne le voie. Le critère est le même que pour le
      document : une épreuve qui reste verte quand on retire ce qu elle teste n est
      pas une preuve, c est une décoration (R-731). Ici on l applique au jeu
      d épreuves lui-même.
      **On s arrête au premier cas qui rougit** : il suffit qu une seule épreuve
      voie le refus pour qu il soit surveillé. Mesuré le 19-09-2026, avec neuf
      refus et huit cas fautifs : soixante et un lancements au lieu de
      soixante-douze.
    ⑨ CE QUI CLOCHE — Trois points.
      **① La cible est choisie sur du texte, pas sur une propriété.** Une ligne est
      prise pour cible parce qu elle contient les douze caractères `refus.append`.
      Mesuré le 19-09-2026 : les neuf occurrences du garde-fou sont bien neuf
      instructions. Le jour où ce texte apparaîtrait dans un commentaire ou dans
      une chaîne affichée, il serait neutralisé comme les autres, et le compte de
      refus annoncé serait faux.
      **② Un plantage du programme saboté se lit comme un refus légitime.** Un
      refus est déclaré surveillé dès qu un cas rend un code différent de 1 ; or
      Python rend précisément le code 1 sur une exception non rattrapée — mesuré :
      `python3 -c "raise ValueError('x')"` rend 1. Une copie sabotée qui ne
      compilerait plus serait donc rangée parmi les refus que rien ne surveille,
      ce qui est le bon verdict pour une mauvaise raison.
      **③ Le verdict dépend entièrement du document de référence.** Tant qu il
      est refusé pour un motif qui lui est propre, tous les documents le sont
      aussi, et neutraliser un refus ne change plus rien au code rendu. Mesuré le
      19-09-2026 : 7 des 9 refus déclarés non surveillés pour cette seule raison.
      **Mesuré le 20-09-2026 : les 10 refus du garde-fou sont surveillés.**
    ⑩ EFFET — **Écrit une copie sabotée du garde-fou par refus, chacune dans son
      dossier temporaire, et un dépôt jetable par cas essayé**, par `batir` ;
      au premier appel de `dossier_neutre()`, un dossier de lancement de plus.
      Aucun n est supprimé. Ne touche ni au fichier du garde-fou, ni au dépôt.
    ⑪ TERMINAISON — Rend la liste puis la main. **Les processus lancés le sont sans
      délai maximal** : une copie sabotée qui bouclerait retiendrait cette fonction
      indéfiniment.
      [sort: non]
    ⑫ DÉFINITIONS
      le garde-fou : le programme `CONTROLER_MA_LIVRAISON.py`, qui accepte ou
        refuse un travail avant qu il parte à la relecture
      un refus : une ligne du garde-fou qui ajoute un motif à sa liste de refus et
        fait donc rendre le code 1
    
      Cowork : le relecteur du projet, qui clone le dépôt, casse le code et rend ses cassures par écrit
      le sabotage : retirer ce qu un contrôle surveille pour vérifier qu il tombe
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    src = open(GARDE, encoding="utf-8", errors="replace").read()
    lignes = src.split("\n")
    cibles = [i for i, l in enumerate(lignes) if "refus.append" in l]
    print(f"\n  SABOTAGE DU PROGRAMME — {len(cibles)} refus neutralisés un à un")
    nus = []
    for i in cibles:
        mod = list(lignes)
        # on neutralise le refus sans toucher a l indentation
        creux = len(mod[i]) - len(mod[i].lstrip())
        mod[i] = " " * creux + "pass  # SABOTE"
        # les lignes de continuation de l appel
        j = i + 1
        while j < len(mod) and mod[j].strip() and not mod[j].lstrip().startswith("#") \
                and (len(mod[j]) - len(mod[j].lstrip())) > creux:
            mod[j] = " " * creux + "pass  # SABOTE"
            j += 1
        # **LA COPIE SABOTEE A BESOIN DE SES VOISINS — 22-09-2026.** Depuis que le
        # garde-fou fait calculer `programmes/LIRE_LE_CODE.py`, qui lui-meme fait
        # calculer `emp.py` a la racine, une copie posee seule dans un dossier vide
        # ne demarre plus : elle s arrete sur « No module named LIRE_LE_CODE », rend
        # le code 1 comme un refus, et le sabotage conclut a tort que le refus
        # neutralise n est surveille par personne. On recree donc autour d elle la
        # forme du depot : un dossier `programmes`, et `emp.py` au-dessus.
        d = tempfile.mkdtemp(prefix="sabot_")
        os.makedirs(os.path.join(d, "programmes"), exist_ok=True)
        g = os.path.join(d, "programmes", "GARDE.py")
        open(g, "w", encoding="utf-8").write("\n".join(mod))
        for voisin, ou in ((os.path.join(ICI, "LIRE_LE_CODE.py"),
                            os.path.join(d, "programmes", "LIRE_LE_CODE.py")),
                           (os.path.join(ICI, "QUI_TOUCHE_CE_FICHIER.py"),
                            os.path.join(d, "programmes", "QUI_TOUCHE_CE_FICHIER.py")),
                           (os.path.join(ICI, "FABRIQUER_LE_SOCLE.py"),
                            os.path.join(d, "programmes", "FABRIQUER_LE_SOCLE.py")),
                           (os.path.join(os.path.dirname(ICI), "emp.py"),
                            os.path.join(d, "emp.py"))):
            if os.path.exists(voisin):
                shutil.copy(voisin, ou)
        tombe = False
        for cas in CAS:
            if cas[2] != 1:
                continue
            p = batir(cas[1], *cas[4:6])
            r = subprocess.run([sys.executable, g, p],
                               capture_output=True, text=True, errors="replace",
                               cwd=dossier_neutre())
            if r.returncode != 1:
                tombe = True
                break
        etat = "surveillé" if tombe else "*** AUCUNE ÉPREUVE NE LE VOIT ***"
        print(f"  {'OK ' if tombe else '❌ '} refus ligne {i + 1:<5} {etat}")
        if not tombe:
            nus.append(i + 1)
    return nus


def main():
    """Enchaîne les deux mesures du programme et rend un verdict unique.

    ① RÔLE — **Donner un seul verdict à partir de deux mesures indépendantes** :
      les cas de la liste `CAS` joués, et les refus du garde-fou neutralisés un
      par un.
    ② CONTEXTE D APPEL — Le lancement du programme, et lui seul. La dernière ligne
      du fichier passe la valeur rendue au code de sortie du processus.
    ③ ENTRÉE — Aucun paramètre, et aucun argument de ligne de commande n est lu.
    ④ CONDITIONS D ENTRÉE — Aucune. L absence du fichier du garde-fou est traitée
      par la fonction elle-même, pas exigée de l appelant.
    ⑤ SORTIE — **UNE valeur, un entier : 0 si tout tient, 1 sinon.** Le compte
      rendu complet part à l affichage.
      [rend: 1]
    ⑥ TRAITEMENT — ① afficher le nom du garde-fou éprouvé et le nombre de cas ·
      ② rendre 1 si le fichier du garde-fou est introuvable · ③ jouer tous les cas
      de la liste `CAS` et compter ceux qui rendent le verdict attendu · ④ afficher ce compte ·
      ⑤ neutraliser les refus un par un · ⑥ afficher la liste des refus non
      surveillés s il y en a · ⑦ rendre 1 si un cas est tombé à côté ou si un refus
      n est surveillé par rien, sinon 0.
    ⑦ UNITÉ — Un NOMBRE DE CAS, un NOMBRE DE REFUS, des NUMÉROS DE LIGNE dans le
      fichier du garde-fou, et un CODE DE SORTIE.
    ⑧ POURQUOI — **Les deux mesures sont jouées en entier avant de conclure, et
      non arrêtées à la première faute.** Un jeu d épreuves qui s arrête au premier
      échec cache les suivants, et il faut les voir tous pour savoir par où
      commencer. **Et le verdict est un code de sortie, pas une phrase** : un
      contrôle qui n a pas pu tourner rend un code non nul (R-734), ce qui permet
      à une tâche automatique de rougir sans que personne lise l affichage.
    ⑨ CE QUI CLOCHE — Deux points.
      **① Le code 1 porte trois causes différentes** : garde-fou introuvable, cas
      tombé à côté, refus non surveillé. Mesuré le 19-09-2026, il en portait deux à
      la fois — 8 cas justes sur 9, et 7 refus sur 9 sans surveillance — et le code
      rendu, 1, ne permet pas de les distinguer. Qui ne lit que le code ne sait pas
      laquelle des trois s est produite, et les trois se réparent autrement.
      **② La phrase affichée en tête compte le cas de référence parmi les fautes.**
      Elle annonce que chaque cas vient « d une faute réellement commise », alors
      que les cas dont le code attendu est 0 doivent être ACCEPTÉS : le cas de
      référence, et depuis le 20-09-2026 ceux qui prouvent qu une fiche juste
      n est pas accusée à tort.
    ⑩ EFFET — **N écrit elle-même aucun fichier** : elle affiche. Ses deux appels
      créent en revanche des dossiers temporaires qui ne sont pas supprimés — 79
      sur l exécution mesurée le 19-09-2026.
    ⑪ TERMINAISON — Rend un entier, que la dernière ligne du fichier transforme en
      code de sortie du processus. Ses deux appels lancent des processus sans délai
      maximal : si l un d eux ne se terminait pas, elle ne reviendrait pas non plus.
      [sort: non]
    ⑫ DÉFINITIONS
      le garde-fou : le programme `CONTROLER_MA_LIVRAISON.py`, qui accepte ou
        refuse un travail avant qu il parte à la relecture
      un refus : une ligne du garde-fou qui ajoute un motif à sa liste de refus et
        fait donc rendre le code 1
    
      un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré rejoué à l'identique pour vérifier qu'il n'est pas revenu.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    print(f"\n  ÉPREUVES DU GARDE-FOU — {os.path.basename(GARDE)}")
    print(f"  {len(CAS)} cas, chacun venu d une faute réellement commise\n")
    if not os.path.isfile(GARDE):
        print(f"  ❌ {GARDE} introuvable")
        return 1
    bons = sum(jouer(*c) for c in CAS)
    print(f"\n  {bons}/{len(CAS)} épreuves passent")
    nus = saboter_le_programme()
    if nus:
        print(f"\n  ❌ {len(nus)} refus NE SONT SURVEILLÉS PAR AUCUNE ÉPREUVE : "
              f"lignes {', '.join(str(x) for x in nus)}")
    if bons < len(CAS) or nus:
        print("  ❌ LE JEU D ÉPREUVES NE COUVRE PAS LE GARDE-FOU.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
