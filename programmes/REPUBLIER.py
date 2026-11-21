#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REPUBLIER.py — Ven 20-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Le 20-11-2026 à 15h29, une installation sur main sans republication au public a fait tomber le
circuit du soir (le pas « Poser les programmes publics » refuse des programmes publics différents du privé). La
réparation du même soir (relecteur neuf : « NON DÉPLOYABLE » ; superviseur R-759 : « RUSTINE, À REPRENDRE, AVEC
SIMPLIFICATION ») sépare les deux gestes : programmes/INSTALLER.py s'arrête à la fusion poussée sur main, et CE
programme amène le public au code de main. Il est IDEMPOTENT : sur un public déjà égal à main, il ne fait rien.
Depuis la décision de Jean-Luc du 21-11-2026 à 13h27 (réponse « 1 » à N-2 : « INSTALLER enchaîne lui-même la
republication »), INSTALLER le lance lui-même après la fusion poussée, en (a) puis en (b).

① RÔLE — Deux usages. (a) PUBLIER : fabriquer le circuit de main, le comparer au public, ne rien faire s'ils sont
  égaux, publier sinon. (b) VÉRIFIER (--verifier) : sans réseau, dire si un clone public porte exactement ce que
  fabrique un dépôt privé ; rougit et nomme la commande (a) sinon.
② CONTEXTE D'APPEL — (a) Par INSTALLER (étape ⑤, sous-processus, depuis la racine du clone du Chat) ; à la main par
  le Chat seulement après un code 4 d'INSTALLER, ou sur la ligne « ::error:: » du circuit du soir :
  python3 -B programmes/REPUBLIER.py
  (b) Par le pas « Le public porte-t-il le code de main ? » en tête du circuit du soir fabriqué
  (programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, PUBLIC_A_JOUR) :
  python3 -B programmes/REPUBLIER.py --verifier <dépôt privé> <clone public>
  et par INSTALLER (étape ⑤), avec --fabricant-du-prive : le fabricant du worktree de main, celui qui a publié.
③ ENTRÉE — La ligne de commande. Les variables LIVRER_* de programmes/LIVRER.py valent ici aussi (épreuves).
④ CONDITIONS D'ENTRÉE — (a) Celles de LIVRER.py ; main n'est extraite dans aucun worktree, ou dans un worktree propre
  à la pointe d'origin/main. (b) Les deux dossiers existent ; le clone public est un dépôt git.
⑤ SORTIE — Le code de sortie. (a) 0 le public porte main (déjà égal : rien fait ; ou publié et prouvé par un clone
  neuf) · 3 ÉTAPE TOMBÉE (fetch, worktree, clone, fabrication à blanc ou publication refusés) · 5 PLANTAGE.
  (b) 0 égal · 1 DIFFÉRENT (le public n'est pas celui de main ; la commande (a) est nommée) · 2 non vérifiable ·
  5 PLANTAGE.
⑥ TRAITEMENT — (a) fetch ; worktree de main (`LIVRER.worktree_nomme`) ; clone public neuf de main
  (`LIVRER.cloner_le_public`) ; fabrication à blanc (`LIVRER.fabriquer`) ; « git status --porcelain » vide → rien à
  faire, code 0 ; sinon `LIVRER.publier_au_public` (essai à blanc, --publier, preuve par un second clone neuf), code 0.
  (b) copie du clone public sous un dossier temporaire ; le fabricant posé À CÔTÉ DE CE PROGRAMME (le code publié,
  dans le circuit), ou avec --fabricant-du-prive celui du dépôt privé (`LIVRER.fabricant_de`, N-21), fabrique à blanc
  depuis le dépôt privé dans la copie ; « git status --porcelain » de la copie.
⑦ UNITÉ — —
⑧ POURQUOI — Voir le sens en tête. TOUT passe par FABRIQUER_LE_CIRCUIT_PUBLIC.py (R-708 : deux implémentations d'une
  même chose divergent toujours) : la comparaison est une fabrication à blanc, jamais une liste de fichiers recopiée.
⑨ CE QUI CLOCHE — ① La publication depuis GitHub Actions, sans le Chat, n'est PAS faite : le circuit du soir porte
  « permissions: contents: write » (son jeton peut pousser au public), mais GitHub refuse à ce jeton toute poussée
  qui crée ou modifie un fichier .github/workflows/ (permission « workflows » non attribuable au jeton d'un
  passage), et la portée de secrets.JETON_DEPOTS sur le public n'est écrite nulle part au dépôt. Le circuit du soir
  ROUGIT donc et nomme la commande (a), sans publier. ② Aucune entrée au registre des travaux : un programme
  idempotent n'a rien à suivre, et son effet se lit au public. ③ (b) la fabrication à blanc écrit dans la COPIE,
  jamais dans le clone donné.
⑩ EFFET — (a) Crée et retire un worktree, clone le public sous /tmp, pousse au public (branche main) par le
  fabricant si et seulement si le public diffère. (b) Écrit une copie temporaire, effacée.
⑪ TERMINAISON — Sort du programme par sys.exit. Chaque commande lancée est bornée (LIVRER.lancer).
"""
import os
import shutil
import sys
import tempfile
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import LIVRER as L

EGAL, DIFFERENT, INVERIFIABLE = 0, 1, 2
# Le « code » que rend `ecart_avec_le_public` quand le fabricant sort en 0 sans rien réécrire (N-4 du RELU de Cowork
# sur 0f18a8d2a) : aucun code de sortie de processus n'est négatif, il ne peut donc pas en être confondu.
MUET = -1


def ecart_avec_le_public(prive, public, fabricant):
    """Fabrique à blanc depuis `prive` dans une COPIE de `public` ; rend (code du fabricant, écart, sortie).

    ① RÔLE — La comparaison unique « le public porte-t-il ce que fabrique le privé ? », pour (a) et (b).
    ② CONTEXTE D'APPEL — `publier_si_different`, `verifier`.
    ③ ENTRÉE — `prive` : le dépôt privé · `public` : un clone public (dépôt git) · `fabricant` : le chemin du
      fabricant à lancer.
    ④ CONDITIONS D'ENTRÉE — `public` est un dépôt git.
    ⑤ SORTIE — TROIS valeurs : le code de sortie du fabricant, ou MUET s'il sort en 0 sans avoir réécrit aucun
      fichier suivi ; l'écart rendu par `LIVRER.ecart_apres_fabrication` (« git status --porcelain
      --untracked-files=all » de la copie, plus les fichiers ignorés que la fabrication a écrits ; vide = égal) ; les
      dernières lignes du fabricant, ou la raison du MUET.
      [rend: 3]
    ⑥ TRAITEMENT — copie de `public` (liens gardés) sous un dossier temporaire ; « python3 -B <fabricant> <prive>
      <copie> » à blanc, par `LIVRER.ecart_apres_fabrication` (dates figées avant, écart et fichiers réécrits après) ;
      copie effacée.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — `LIVRER._publier_dans` prouve une publication par la même propriété (fabrication à blanc sur un
      clone neuf, rien ne change) ; ici sur une copie, pour ne jamais salir le clone donné.
    ⑨ CE QUI CLOCHE — La copie double l'espace disque du clone public le temps de la fabrication.
    ⑩ EFFET — Écrit puis efface un dossier temporaire ; lance le fabricant.
    ⑪ TERMINAISON — Rend la main ; le fabricant est borné à 3 600 s.
      [sort: non]
    """
    base = tempfile.mkdtemp(prefix="livrer_republier_")
    try:
        copie = os.path.join(base, "public")
        shutil.copytree(public, copie, symlinks=True)
        r, reste, reecrits = L.ecart_apres_fabrication(copie, lambda: L.lancer(
            [sys.executable, "-B", fabricant, os.path.abspath(prive), copie], dossier=prive, borne=3600))
        if r.returncode == 0 and not reecrits:
            return MUET, reste, "le fabricant sort en 0 sans avoir réécrit aucun fichier : un fabricant muet ne prouve rien"
        return r.returncode, reste, (r.stdout + r.stderr).strip()[-300:]
    finally:
        shutil.rmtree(base, ignore_errors=True)


def verifier(prive, public, fabricant_du_prive=False):
    """Usage (b) : rend 0 si `public` porte exactement ce que fabrique `prive`, 1 sinon, 2 si invérifiable.

    ① RÔLE — Le pas du circuit du soir qui dit, en tête, que le public est en retard sur main.
    ② CONTEXTE D'APPEL — `main`, sur --verifier.
    ③ ENTRÉE — `prive` · `public` · `fabricant_du_prive` : vrai pour --fabricant-du-prive.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2.
      [rend: 1]
    ⑥ TRAITEMENT — Fabricant : avec `fabricant_du_prive`, `LIVRER.fabricant_de(prive)` (celui qui publie depuis main,
      N-21 du RELU de Cowork sur 4e4dc386f) ; sinon LIVRER_FABRICANT, sinon celui posé à côté de ce programme ;
      `ecart_avec_le_public` ;
      la ligne « ::error:: » nomme la commande (`LIVRER.commande_de_republication`).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Dans le circuit, le fabricant posé à côté de ce programme est le code PUBLIÉ (après le pas « Poser
      les programmes publics ») : aucun code du dépôt privé n'y tourne.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui de `ecart_avec_le_public`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if not os.path.isdir(os.path.join(public, ".git")) or not os.path.isdir(prive):
        L.dire("::error::PUBLIC NON VÉRIFIABLE — dossiers absents ou clone public sans .git")
        return INVERIFIABLE
    fabricant = L.fabricant_de(prive) if fabricant_du_prive else os.environ.get(
        "LIVRER_FABRICANT", os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.basename(L.FABRICANT)))
    code, reste, sortie = ecart_avec_le_public(prive, public, fabricant)
    if code != 0:
        L.dire(f"::error::PUBLIC NON VÉRIFIABLE — fabrication à blanc refusée (code {code}) : {sortie}")
        return INVERIFIABLE
    if reste:
        n = len(reste.splitlines())
        L.dire(f"::error::LE PUBLIC N'EST PAS CELUI DE MAIN ({n} fichier(s) différent(s)) — lancer : "
               f"{L.commande_de_republication(prive)}")
        for ligne in reste.splitlines()[:10]:
            L.dire("  " + ligne)
        return DIFFERENT
    L.dire("public égal à main : rien à republier")
    return EGAL


def publier_si_different(racine):
    """Usage (a) : amène le public à main si, et seulement si, il en diffère ; rend 0, 3.

    ① RÔLE — La republication idempotente.
    ② CONTEXTE D'APPEL — `main`, sans --verifier.
    ③ ENTRÉE — `racine` : le clone privé.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête.
    ⑤ SORTIE — UNE valeur : 0, ou 3 (lève Arret).
      [rend: 1]
    ⑥ TRAITEMENT — Voir l'en-tête, ⑥ (a). Le fabricant est celui du worktree de main (LIVRER.fabriquer).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Ne rien pousser quand rien ne diffère : une republication inutile ne doit laisser aucune trace.
    ⑨ CE QUI CLOCHE — Entre la comparaison et la publication, un autre geste peut changer le public : la publication
      le reprend (elle reclone) et sa preuve finale le constate.
    ⑩ EFFET — Voir l'en-tête, ⑩ (a).
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    wt, jetable, public, publication = None, False, None, None
    try:
        if L.git(racine, "fetch", "-q", "origin").returncode != 0:
            raise L.Arret(L.TOMBE, "fetch du dépôt privé refusé")
        wt, jetable = L.worktree_nomme(racine, "main")
        pointe = L.git(wt, "rev-parse", "HEAD").stdout.strip()
        public = L.cloner_le_public("main")
        code, reste, sortie = ecart_avec_le_public(wt, public, L.fabricant_de(wt))
        if code != 0:
            raise L.Arret(L.TOMBE, f"fabrication à blanc refusée (code {code}) : {sortie}")
        if not reste:
            L.dire(f"ÉGAL — le public porte déjà main ({pointe[:12]}) : rien à republier")
            return 0
        L.dire(f"DIFFÉRENT — {len(reste.splitlines())} fichier(s) : publication de main ({pointe[:12]})")
        publication, pub = L.publier_au_public(wt, "main")
        L.dire(f"REPUBLIÉ — pointe publique {pub['avant'][:12]} → {pub['apres'][:12]} ; un clone neuf porte exactement "
               "le code de main")
        return 0
    finally:
        if wt and jetable:
            L.retirer_worktree(racine, wt)
        for d in (public, publication):
            if d:
                shutil.rmtree(d, ignore_errors=True)


def main():
    """Aiguille vers (a) ou (b) ; sort avec le code.

    ① RÔLE — Voir l'en-tête.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — sys.argv : rien, ou « --verifier [--fabricant-du-prive] <privé> <public> ».
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête.
    ⑤ SORTIE — Rien : sort (voir l'en-tête, ⑤).
      [rend: rien]
    ⑥ TRAITEMENT — `verifier` ou `publier_si_different` ; un arrêt prévu sort avec son code ; toute autre exception
      sort en 5 (PLANTAGE).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un plantage n'est jamais lu comme « égal » ni comme « différent ».
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Voir l'en-tête.
    ⑪ TERMINAISON — Sort du programme par sys.exit.
      [sort: oui]
    """
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    try:
        if "--verifier" in sys.argv:
            if len(args) != 2:
                L.dire("usage : REPUBLIER.py --verifier <dépôt privé> <clone public>")
                sys.exit(INVERIFIABLE)
            code = verifier(os.path.abspath(args[0]), os.path.abspath(args[1]),
                            fabricant_du_prive="--fabricant-du-prive" in sys.argv)
        elif args:
            L.dire("usage : REPUBLIER.py   (depuis la racine du clone privé)")
            code = L.TOMBE
        else:
            code = publier_si_different(os.getcwd())
    except L.Arret as e:
        code = e.args[0]
        L.dire(f"ARRÊT (code {code}) — {e.args[1]}")
    except Exception as e:   # noqa: BLE001 — un plantage n'est jamais lu comme un verdict
        code = L.PLANTAGE
        L.dire(f"PLANTAGE (code {L.PLANTAGE}) — {type(e).__name__} : {e}")
        L.dire(traceback.format_exc().rstrip())
    sys.exit(code)


if __name__ == "__main__":
    main()
