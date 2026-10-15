#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dit quels programmes, épreuves, tâches du soir et consignes nomment un fichier donné.
DÉCIDÉ · Rôle : lister, avant de modifier un fichier, tout ce qui le lit ou l'écrit (R-755 ①, A-494 ①).

① RÔLE — **Faire, par un programme, le premier geste de R-755** : avant de
  modifier un fichier, lister tout ce qui le lit ou l'écrit, pour ne pas oublier
  un lecteur. Le 27-09-2026, pendant la réparation du défaut 3 de A-491, le radar
  (`programmes/audit_ecosysteme.py`) lisait le journal des trades et avait été
  oublié ; le relecteur l'a trouvé au premier tour. Ce programme rend la liste en
  trois parties : ① les fichiers qui ÉCRIVENT LE NOM du fichier · ② ceux qui le
  cherchent par un MOTIF, selon la règle du socle · ③ ceux qui importent un
  programme des deux premières parties, le lancent ou écrivent son nom, et
  peuvent donc l'atteindre sans nommer la cible. Une mention dans un texte
  explicatif compte aussi — mieux vaut un nom de trop qu'un lecteur oublié.
② CONTEXTE D'APPEL — À la main, par le Chat ou par Cowork, avant d'écrire du code
  qui touche un fichier. Aucune tâche du soir ne le lance.
③ ENTRÉE — Deux arguments : la racine du dépôt (un clone), puis le fichier, soit
  par son chemin relatif à la racine (`donnees/claude_journal_trades.csv`), soit
  par son seul nom s'il n'existe qu'une fois dans l'arbre.
④ CONDITIONS D'ENTRÉE — `programmes/FABRIQUER_LE_SOCLE.py` doit se trouver à côté
  de ce fichier : ses fonctions `lister`, `cles_de`, `lecteurs` et
  `ce_qu_il_appelle` sont employées telles quelles.
⑤ SORTIE — Un affichage, et un code de sortie : 0 si la recherche a tourné
  jusqu'au bout, qu'elle ait trouvé ou non · 2 si les arguments manquent, si le
  fichier demandé n'existe pas dans l'arbre, ou si son seul nom en désigne
  plusieurs · 3 si un fichier du périmètre n'a pas pu être lu.
⑥ TRAITEMENT — ① retrouver le fichier demandé dans l'arbre · ② faire la liste du
  périmètre : les fichiers de `programmes/`, `tests/`, `.github/workflows/` et
  `prompts_taches/` · ③ confier à `qui_touche` les trois recherches · ④ afficher
  les trois parties, chaque fichier avec ses premiers numéros de ligne ou son motif
  · ⑤ afficher ce que l'outil ne voit pas · ⑥ sortir sur le code.
⑦ UNITÉ — Des NOMBRES DE FICHIERS et des NUMÉROS DE LIGNE.
⑧ POURQUOI — R-754 : ce qu'un programme peut faire, un programme le fait. Le
  premier geste de R-755 reposait sur la mémoire de celui qui livre ; il a manqué
  le radar une fois. La règle qui dit « tel motif désigne tel fichier » est celle
  du socle, importée et jamais recopiée (R-708).
⑨ CE QUI CLOCHE — **Il ne distingue pas lire et écrire** : un nom posé dans une
  constante sert aux deux, à une autre ligne. **Il ne voit pas un nom fabriqué à
  l'exécution** (`f"{x}_journal_trades.csv"`, une concaténation). **La partie
  « par motif » hérite de la sur-détection du socle** : un motif d'au moins cinq
  caractères désigne tout fichier dont le nom commence par lui. **La partie
  indirecte ne descend que d'un niveau d'import.** Les documents de gouvernance et
  les notes ne sont pas dans le périmètre. **Un nom court sur-détecte** : il est
  aussi un mot ordinaire (`emp.py` sort tout fichier qui écrit `emp`).
⑩ EFFET — N'écrit rien. Lit les fichiers du périmètre.
⑪ TERMINAISON — Rend la main après une lecture de chaque fichier du périmètre.
  Aucun de ses appels ne peut ne pas revenir.

USAGE : python3 programmes/QUI_TOUCHE_CE_FICHIER.py <racine> <fichier>
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import FABRIQUER_LE_SOCLE as SOCLE            # la règle de rapprochement du socle (R-708)

PERIMETRE = ("programmes/", "tests/", ".github/workflows/", "prompts_taches/")
_RE_MOT = re.compile(r"[A-Za-z0-9_.\-]+")


def mots(ligne):
    """Rend, en minuscules, toutes les écritures de nom qu'une ligne peut porter.

    ① RÔLE — Découper une ligne en noms possibles sans rater un nom collé à un
      point final.
    ② CONTEXTE D'APPEL — `qui_touche`, une fois par ligne de chaque fichier du
      périmètre.
    ③ ENTRÉE — `ligne` : une ligne de texte.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : un ensemble de chaînes en minuscules.
      [rend: 1]
    ⑥ TRAITEMENT — ① relever les suites de lettres, chiffres, soulignés, points et
      tirets · ② retirer à chacune ses points et tirets de fin · ③ les rendre en
      minuscules. Un nom suivi d'un attribut (`MODULE_POSITIONS.FRAIS_TAUX`) reste
      entier : c'est `designe` qui le rapproche d'un programme.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Mesure du relecteur, 28-09-2026 : sans le retrait du point
      final, un nom en fin de phrase (`…19h32.py.`) échappait. Le découpage aux
      points, essayé au tour 1, faisait passer `rapports/AUDIT_ECOSYSTEME.md` pour
      `programmes/audit_ecosysteme.py` (17 fichiers au lieu de 2, relecteur, tour
      2) : il a été retiré.
    ⑨ CE QUI CLOCHE — Un nom court est aussi un mot ordinaire : pour `emp.py`, tout
      fichier qui écrit le mot `emp` sort. Un nom qui contient une espace n'est
      jamais un seul mot : hors guillemets, il échappe. Mieux vaut un nom de trop
      qu'un lecteur oublié.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    out = set()
    for m in _RE_MOT.findall(ligne):
        m = m.rstrip(".-").lower()
        if m:
            out.add(m)
    return out


def designe(mots_vus, cles, module, noms):
    """Dit si l'un des mots vus désigne un fichier donné.

    ① RÔLE — Décider, en un seul endroit, qu'un mot relevé nomme le fichier.
    ② CONTEXTE D'APPEL — `qui_touche`, une fois par ligne pour la cible, et une
      fois par fichier et par programme retenu pour la partie ③.
    ③ ENTRÉE — `mots_vus` : un ensemble de mots en minuscules, sortis de `mots` ·
      `cles` : les écritures du fichier, sorties de `SOCLE.cles_de` · `module` : le
      nom du fichier sans `.py` en minuscules si c'est un programme, sinon `None` ·
      `noms` : les noms, en minuscules, de tous les fichiers de l'arbre.
    ④ CONDITIONS D'ENTRÉE — Tout en minuscules.
    ⑤ SORTIE — UNE valeur : vrai ou faux.
      [rend: 1]
    ⑥ TRAITEMENT — ① vrai si un mot est l'une des écritures · ② sinon, pour un
      programme seulement, vrai si un mot commence par son nom suivi d'un point et
      n'est pas lui-même le nom d'un fichier de l'arbre : `module_positions.frais_taux`
      désigne `MODULE_POSITIONS.py` ; `audit_ecosysteme.md`, nom de
      `rapports/AUDIT_ECOSYSTEME.md`, ne désigne pas `audit_ecosysteme.py`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un attribut (`MODULE_POSITIONS.FRAIS_TAUX`) atteint un programme
      sans écrire son nom de fichier : mesure du relecteur, tour 1,
      `programmes/MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py` était oublié. Mais
      un fichier de même radical n'est pas le programme (tour 2 : trois paires
      réelles au dépôt). Le critère est une PROPRIÉTÉ — le mot est-il le nom d'un
      fichier existant ? — et non une liste d'extensions.
    ⑨ CE QUI CLOCHE — Un nom de fichier qui n'existe pas encore
      (`audit_ecosysteme.log`) passe pour un attribut du programme.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    if mots_vus & cles:
        return True
    if module:
        tete = module + "."
        return any(m.startswith(tete) and m not in noms for m in mots_vus)
    return False


def _module(chemin_rel):
    """Rend le nom d'un programme sans `.py`, en minuscules, ou `None`.

    ① RÔLE — Donner à `designe` le nom sous lequel un programme s'importe.
    ② CONTEXTE D'APPEL — `qui_touche`, pour la cible et pour chaque programme retenu.
    ③ ENTRÉE — `chemin_rel` : un chemin relatif.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — UNE valeur : une chaîne, ou `None` si le fichier ne finit pas par `.py`.
      [rend: 1]
    ⑥ TRAITEMENT — Garder le nom, retirer `.py`, mettre en minuscules.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Seul un programme a des attributs.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    nom = os.path.basename(chemin_rel)
    return nom[:-3].lower() if nom.endswith(".py") else None


class Illisible(Exception):
    """Un fichier du périmètre n'a pas pu être lu. R-734 : un contrôle qui n'a pas pu
    tourner rend un code non nul, au lieu d'une liste incomplète présentée comme
    complète."""


def retrouver(racine, demande):
    """Rend le chemin relatif du fichier demandé, ou la raison pour laquelle on ne le peut pas.

    ① RÔLE — Transformer ce que la personne a tapé en UN chemin de l'arbre, ou dire
      pourquoi c'est impossible.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `racine` : le dossier du dépôt · `demande` : un chemin relatif à la
      racine ou un seul nom de fichier, par exemple `claude_journal_trades.csv`.
    ④ CONDITIONS D'ENTRÉE — Aucune.
    ⑤ SORTIE — DEUX valeurs : le chemin relatif trouvé (ou `None`) et un message
      (vide quand un chemin est trouvé).
      [rend: 2]
    ⑥ TRAITEMENT — ① si `demande` porte un chemin (une barre oblique, ou absolu) :
      résoudre les liens de son DOSSIER et de la racine, jamais son dernier nom ;
      hors du dépôt → `None` et le dire ; fichier → rendre son chemin
      relatif ; sinon → `None` · ② sinon chercher dans l'arbre du socle les
      chemins dont le nom est `demande` · ③ un seul : le rendre · aucun ou
      plusieurs : rendre `None` et le dire.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un nom inconnu doit arrêter la recherche : répondre « personne
      ne le touche » sur un nom mal tapé serait un vert faux (R-734). Un chemin
      hors du dépôt aussi : mesure du relecteur, 28-09-2026, `../g.txt` rendait le
      code 0 et 31 fichiers, la clé `g` étant prise pour un nom ; et un chemin
      absolu vers un fichier du dépôt n'était pas retiré de sa propre liste. **Seuls
      les dossiers sont résolus, jamais le dernier nom** : un lien symbolique est
      un fichier de l'arbre sous son propre nom (relecteur, tour 2 : résolu, le lien
      `alias_trades.csv` devenait sa cible et son lecteur était oublié) ; mais une
      racine ou un dossier atteint par un lien reste le même dossier (relecteur,
      tour 3 : sans résolution, un fichier du dépôt était dit « hors du dépôt »).
    ⑨ CE QUI CLOCHE — L'arbre est celui du socle : un fichier rangé dans
      `archives/` n'est pas trouvé par son seul nom.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main après un parcours de l'arbre.
      [sort: non]
    """
    rac = os.path.realpath(racine)
    brut = os.path.normpath(os.path.join(os.path.abspath(racine), demande))
    vrai = os.path.join(os.path.realpath(os.path.dirname(brut)), os.path.basename(brut))
    if os.path.isabs(demande) or os.sep in demande or "/" in demande:
        if not vrai.startswith(rac + os.sep):
            return None, f"« {demande} » est hors du dépôt {racine}"
        if os.path.isfile(vrai):
            return os.path.relpath(vrai, rac), ""
        return None, f"« {demande} » n'existe pas dans l'arbre de {racine}"
    rel = os.path.normpath(demande)
    tous = [p for p in SOCLE.lister(racine) if os.path.basename(p) == os.path.basename(rel)]
    if len(tous) == 1:
        return tous[0], ""
    if not tous:
        return None, f"« {demande} » n'existe pas dans l'arbre de {racine}"
    return None, f"« {demande} » désigne {len(tous)} fichiers : " + " · ".join(tous)


def qui_touche(racine, cible):
    """Rend, en trois parties, les fichiers du périmètre qui désignent la cible.

    ① RÔLE — Faire les trois recherches : par le nom écrit, par motif, par le nom d'un programme qui la nomme.
    ② CONTEXTE D'APPEL — `main`, une fois ; et les épreuves de
      `tests/EPREUVES_DE_QUI_TOUCHE_CE_FICHIER_Lun_28-09-2026.py`.
    ③ ENTRÉE — `racine` : le dossier du dépôt · `cible` : le chemin relatif du
      fichier, déjà retrouvé.
    ④ CONDITIONS D'ENTRÉE — Chaque fichier du périmètre doit pouvoir être ouvert.
    ⑤ SORTIE — TROIS valeurs, trois dictionnaires : ① chemin → liste des numéros
      de ligne où le nom est écrit · ② chemin → ensemble des motifs qui désignent
      la cible · ③ chemin → ensemble des programmes des deux premières parties
      qu'il nomme.
      [rend: 3]
    ⑥ TRAITEMENT — ① faire la liste du périmètre, sans la cible elle-même · ② pour
      chaque fichier, relever ligne par ligne les noms possibles (`mots`) ; retenir
      la ligne si `designe` dit que l'un d'eux nomme la cible · ③ pour
      chaque fichier, relever ses noms et motifs par `SOCLE.ce_qu_il_appelle` et
      retenir ceux que `SOCLE.lecteurs` rapproche de la cible · ④ pour chaque
      programme Python des deux premières parties, retenir les fichiers, pas déjà
      retenus, dont un mot le désigne (`designe`) : un import, un chemin entre
      guillemets, un `python3 programmes/X.py` d'une tâche, un attribut.
    ⑦ UNITÉ — Des NUMÉROS DE LIGNE, comptés à partir de 1.
    ⑧ POURQUOI — Le nom écrit trouve la plupart des lecteurs ; le motif trouve ceux
      qui cherchent un fichier par un morceau de son nom (cas réel : le radar
      cherche `PROMPT_BOUCLE` pour `etudes/PROMPT_BOUCLE_v4_Jeu_13-08-2026_14h39.md`) ;
      l'import trouve ceux qui l'atteignent par une fonction d'un autre programme.
      **La partie ③ cherche le NOM du programme, pas seulement un `import`** :
      mesure du relecteur, 28-09-2026, la version qui s'appuyait sur les imports
      du socle ne voyait ni `.github/workflows/collecte_abc.yml` (ligne 216,
      `python3 programmes/TENIR_LES_POSITIONS.py`, sans guillemets) ni un chemin
      `"programmes/X.py"` entre guillemets, barre oblique comprise.
    ⑨ CE QUI CLOCHE — Voir l'en-tête : lire et écrire ne sont pas distingués ; un
      nom fabriqué à l'exécution échappe ; l'import n'est suivi que d'un niveau.
    ⑩ EFFET — Aucun. Lit les fichiers.
    ⑪ TERMINAISON — Rend la main après une lecture de chaque fichier. Lève
      `Illisible` si un fichier ne s'ouvre pas.
      [sort: non]
    """
    perim = [p for p in SOCLE.lister(racine)
             if p.startswith(PERIMETRE) and os.path.normpath(p) != cible]
    cles, module = SOCLE.cles_de(cible), _module(cible)
    noms = {os.path.basename(x).lower() for x in SOCLE.lister(racine)}
    par_nom, par_motif, mots_de = {}, {}, {}
    for p in perim:
        chemin = os.path.join(racine, p)
        try:
            with open(chemin, encoding="utf-8", errors="replace") as f:
                texte = f.read()
            _progs, fichiers, _motifs = SOCLE.ce_qu_il_appelle(chemin)
        except (OSError, SOCLE.SocleIllisible) as e:
            raise Illisible(f"{p} : {type(e).__name__} {e}")
        mots_de[p] = [mots(l) for l in texte.split("\n")]
        lignes = [i for i, m in enumerate(mots_de[p], 1) if designe(m, cles, module, noms)]
        if lignes:
            par_nom[p] = lignes
        motifs = {m for m in fichiers if SOCLE.lecteurs({m.lower(): {p}}, cible)}
        if motifs and p not in par_nom:
            par_motif[p] = motifs
    touches = {t: (SOCLE.cles_de(t), _module(t)) for t in list(par_nom) + list(par_motif)
               if t.endswith(".py")}
    indirects = {}
    for p, lignes_de_mots in mots_de.items():
        if p in par_nom or p in par_motif:
            continue
        tous = set().union(*lignes_de_mots) if lignes_de_mots else set()
        via = {t for t, (c, mo) in touches.items() if designe(tous, c, mo, noms)}
        if via:
            indirects[p] = via
    return par_nom, par_motif, indirects


def main():
    """Lit les arguments, lance la recherche, affiche, et sort sur le code.

    ① RÔLE — Porter le programme de la ligne de commande à l'affichage.
    ② CONTEXTE D'APPEL — Le lancement du programme, et lui seul.
    ③ ENTRÉE — `sys.argv` : la racine puis le fichier.
    ④ CONDITIONS D'ENTRÉE — Deux arguments.
    ⑤ SORTIE — Aucune valeur : elle sort par `sys.exit`, avec 0, 2 ou 3.
      [rend: rien]
    ⑥ TRAITEMENT — ① sans deux arguments : l'usage, code 2 · ② retrouver la cible,
      sinon le dire, code 2 · ③ lancer `qui_touche` ; fichier illisible : le dire,
      code 3 · ④ afficher les trois parties et leurs comptes · ⑤ afficher ce que
      l'outil ne voit pas · ⑥ code 0.
    ⑦ UNITÉ — Des NOMBRES DE FICHIERS et des NUMÉROS DE LIGNE ; au plus 8 numéros
      affichés par fichier.
    ⑧ POURQUOI — Un code non nul pour tout ce qui empêche la recherche d'être
      complète (R-734).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche. N'écrit aucun fichier.
    ⑪ TERMINAISON — Sort toujours par `sys.exit`.
      [sort: oui]
    """
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__.split("USAGE :")[-1].strip())
        sys.exit(2)
    racine = os.path.abspath(args[0])
    cible, msg = retrouver(racine, args[1])
    if cible is None:
        print(f"ARRÊT — {msg}. Rien n'a été cherché.")
        sys.exit(2)
    try:
        par_nom, par_motif, indirects = qui_touche(racine, cible)
    except Illisible as e:
        print(f"ARRÊT — fichier du périmètre illisible : {e}. La liste serait incomplète.")
        sys.exit(3)
    print(f"QUI TOUCHE {cible}")
    print(f"  périmètre : {' · '.join(PERIMETRE)}")
    print(f"\n① LE NOM EST ÉCRIT — {len(par_nom)} fichier(s)")
    for p in sorted(par_nom):
        l = par_nom[p]
        print(f"   {p}  lignes {', '.join(map(str, l[:8]))}{' …' if len(l) > 8 else ''}")
    print(f"\n② PAR MOTIF, RÈGLE DU SOCLE — {len(par_motif)} fichier(s)")
    for p in sorted(par_motif):
        print(f"   {p}  motif(s) {', '.join(sorted(par_motif[p]))}")
    print(f"\n③ NOMME UN PROGRAMME CI-DESSUS (import, lancement, mention), UN NIVEAU — "
          f"{len(indirects)} fichier(s)")
    for p in sorted(indirects):
        print(f"   {p}  via {', '.join(sorted(os.path.basename(v) for v in indirects[p]))}")
    print("\nNE VOIT PAS : lire ou écrire (non distingués) · un nom fabriqué à l'exécution ·"
          " les imports au-delà d'un niveau · les documents hors périmètre ·"
          " un nom à espace hors guillemets."
          "\nSUR-DÉTECTE : un nom court est aussi un mot ordinaire.")
    sys.exit(0)


if __name__ == "__main__":
    main()
