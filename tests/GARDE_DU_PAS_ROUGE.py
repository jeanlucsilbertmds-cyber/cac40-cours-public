#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GARDE_DU_PAS_ROUGE — dit si le pas de fin qui doit faire rougir le circuit sur une sortie de pas est bien formé.

Simulation uniquement : aucun ordre réel n'est jamais passé.
Écrit le samedi 14-11-2026 (Paris).

LE SENS EN TÊTE. Le pas « Tenir les positions » de `.github/workflows/collecte_abc.yml` sort en 0 et écrit des sorties
de pas (`positions_signalees=<n>`, `signaux_mis_a_part=<n>`). Pour chacune, un pas de fin « Rougir si … » doit faire
ROUGIR le passage quand elle ne vaut pas 0. Une retouche du YAML (condition inversée, `always()` retiré, `exit 0`,
`continue-on-error`, id renommé, pas retiré) rendrait le soir VERT en silence. Cette fonction est LA SEULE garde de
ces pas : `tests/EPREUVES_DE_LA_VENTE_UNIQUE_A_Mer_11-11-2026.py` (V10f) l'appelle pour `positions_signalees`,
`tests/EPREUVES_DU_DEPARTAGE_R207BIS_Sam_14-11-2026.py` (T10) pour chaque nom que le teneur écrit réellement.

① RÔLE — Outil d'épreuve (comme `tests/HORLOGE_D_EPREUVE.py`) : une fonction, `garde_du_pas_rouge`.
② CONTEXTE D'APPEL — Importé par `tests/EPREUVES_DU_DEPARTAGE_R207BIS_Sam_14-11-2026.py` (instruction `import`, ce qui
  le range parmi les outils dans `CERTIFIER_LA_VERSION.lister_les_epreuves`), et chargé PAR CHEMIN par
  `tests/EPREUVES_DE_LA_VENTE_UNIQUE_A_Mer_11-11-2026.py` depuis sa copie sabotée. Ne s'exécute pas seul.
③ ENTRÉE — Voir `garde_du_pas_rouge`.
④ CONDITIONS D'ENTRÉE — Le module `yaml` (PyYAML) est installé.
⑤ SORTIE — Voir `garde_du_pas_rouge`.
⑥ TRAITEMENT — Voir `garde_du_pas_rouge`.
⑦ UNITÉ — —
⑧ POURQUOI — Superviseur R-759 du 14-11-2026, tour 2 (N-2, « rustine, à reprendre ») : trois gardes de pas rouges
  existaient déjà, écrites séparément, et une quatrième, à côté de V10f, aurait divergé dès sa naissance : V10f
  ne voyait ni la condition inversée ni un `exit 0` (mesuré par le superviseur). Deux implémentations d'une même chose
  divergent toujours (R-708) : une seule fonction, appelée par les deux épreuves.
⑨ CE QUI CLOCHE — Elle LIT le YAML, elle ne l'exécute pas. Restent invisibles : `|| true` ou `set +e` dans un `run`,
  un `shell:` changé, un `exit 1` dans une branche qui ne s'exécute pas — dont une ligne `exit 0` placée AVANT
  `exit 1` (mesuré par Cowork le 15-11-2026, n-2 : garde verte) —, un `timeout`, un `if:` posé sur le JOB (par
  exemple `if: false` sur `collecte` : tout le soir saute, garde comprise ; mesuré vert par Cowork, n-2 et R-c1 ; se
  voit ailleurs, aucun cours n'arrive). Restent invisibles aussi les formes où « Tenir » RÉUSSIT SANS ÉCRIRE SA
  SORTIE : la sortie vaut alors '', que la forme du `if` lit comme « rien à dire », et les pas rouges ne tournent
  pas. La condition « lance le teneur » ne cherche que le chemin du programme DANS le texte du `run` ; mesuré vert par
  Cowork le 15-11-2026 (a-2 et r-1) : le programme seulement CITÉ (dans un commentaire ou un `echo`) ;
  `GITHUB_OUTPUT` DÉTOURNÉ (par `env:` sur le pas — peut-être refusé par GitHub, non mesuré — ou en ligne,
  `GITHUB_OUTPUT=/dev/null python3 …`) ou VIDÉ dans le `run` ; le teneur lancé en `--calibrage` (cas le plus
  probable, une retouche de débogage : il calibre et rend 0 sans tenir aucune position ni écrire sa sortie, et le
  pas « Rougir si la garde du soir a mordu », qui ne lit que l'issue `success`, dit même que les positions ont été
  tenues). Une parade par propriété (rougir quand « Tenir » a réussi et que sa sortie est vide) est au BACKLOG ;
  seul un vrai passage GitHub
  (`workflow_dispatch` sur une branche d'essai, jamais un soir de séance, A-643 ①) le prouve. Les gardes de W7
  (`EPREUVES_DU_PAS_DE_VERSEMENT`) et de `EPREUVES_C_LE_SOIR_LIT_LA_FICHE` restent à part (leur `if` n'a pas la même
  forme) : les réunir est au BACKLOG.
⑩ EFFET — Aucun au chargement.
⑪ TERMINAISON — —
"""

import re


def garde_du_pas_rouge(texte_yaml, nom_de_sortie, programme):
    """Rend la liste des manques du pas de fin qui doit rougir quand la sortie `nom_de_sortie` ne vaut pas 0.

    ① RÔLE — Vérifier, par propriété, qu'un pas « Rougir si … » existe pour une sortie de pas, qu'il rougit, qu'il
      tourne, et qu'il lit bien le pas qui écrit cette sortie.
    ② CONTEXTE D'APPEL — V10f de `tests/EPREUVES_DE_LA_VENTE_UNIQUE_A_Mer_11-11-2026.py` (`positions_signalees`) ;
      T10 de `tests/EPREUVES_DU_DEPARTAGE_R207BIS_Sam_14-11-2026.py` (chaque nom écrit dans `GITHUB_OUTPUT`).
    ③ ENTRÉE — `texte_yaml` : le texte de `.github/workflows/collecte_abc.yml` · `nom_de_sortie` : par exemple
      « signaux_mis_a_part » · `programme` : le chemin que le pas lu doit lancer, par exemple
      « programmes/TENIR_LES_POSITIONS.py ».
    ④ CONDITIONS D'ENTRÉE — Le texte est un YAML de workflow GitHub (clé `jobs`, chaque job avec `steps`).
    ⑤ SORTIE — UNE valeur : la liste des manques, en phrases ; vide si tout tient.
      [rend: 1]
    ⑥ TRAITEMENT — ① aplatir les pas, chacun avec son job · ② le pas rouge : celui dont le `if` lit
      `.outputs.<nom>` et dont la dernière ligne non vide du `run` est `exit 1` ; il en faut UN · ③ l'id qu'il lit,
      extrait de `steps.<id>.outputs.<nom>` ; il en faut UN · ④ son `if` est exactement
      `always() && steps.<id>.outputs.<nom> != '' && steps.<id>.outputs.<nom> != '0'` (un `${{ }}` autour est
      admis) · ⑤ il vient après tout pas dont le `if` ne porte pas `always()` · ⑥ ni lui ni son job ne portent
      `continue-on-error` · ⑦ un pas, et un seul, porte cet id ; il précède le pas rouge, lance `programme`, n'a pas
      de `continue-on-error` (ni son job), n'a d'autre `if` que rien ou `always()`, et vit dans le MÊME job que le
      pas rouge.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Chaque condition répond à une façon mesurée de faire taire le soir : condition inversée et `exit 0`
      (superviseur du tour 2, invisibles à l'ancien V10f) ; `always()` retiré (un pas rouge plus tôt le sauterait) ;
      `continue-on-error` sur le pas ou le job (un `exit 1` y laisse le passage vert, relecture Cowork du 14-11-2026
      à 02h39, N-1) ; id renommé d'un seul côté (sur GitHub, `steps.<id absent>.outputs.x` vaut '' et le pas ne
      tourne jamais) ; « Tenir » sauté par un `if` ; « Tenir » et le pas rouge dans deux jobs (sur GitHub, le contexte
      `steps` n'existe que dans le job courant : la sortie lue y vaut '' et le pas ne tourne jamais — relecture
      Cowork du 15-11-2026 à 17h46, c-1, déduit de la règle documentée, non mesuré sur GitHub). CHAQUE condition a
      son sabotage qui mord, et mord pour sa raison : `tests/EPREUVES_DU_DEPARTAGE_R207BIS_Sam_14-11-2026.py`, cas
      T12 et sabotages S34 à S43 (S35 à S38 répondent à la relecture Cowork du 15-11-2026, N-1 et B-1 : quatre
      conditions pouvaient être retirées sans qu'aucune épreuve ne rougisse ; S39 garde la condition « même job »).
    ⑨ CE QUI CLOCHE — Voir le ⑨ du module. Deux refus à tort, voulus (une forme unique se compare ; un refus à
      tort se voit, rouge) : ① la forme exacte du `if` refuse une écriture équivalente, par exemple des parenthèses
      en plus ; ② `_neutralise` lit comme un `continue-on-error` tout texte non vide, donc refuse aussi
      `continue-on-error: ${{ false }}` et `continue-on-error: 'false'` (entre guillemets) — seul le booléen
      `continue-on-error: false` passe (mesuré par Cowork le 15-11-2026, F4 et F5).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève si le texte n'est pas du YAML.
      [sort: non]
    """
    import yaml
    manques = []
    jobs = (yaml.safe_load(texte_yaml) or {}).get("jobs") or {}
    pas, job_du_pas = [], []
    for j in jobs.values():
        for x in (j or {}).get("steps") or []:
            pas.append(x)
            job_du_pas.append(j)

    def _if(x):
        brut = str(x.get("if", "")).strip()
        if brut.startswith("${{") and brut.endswith("}}"):
            brut = brut[3:-2].strip()
        return brut

    def _derniere_ligne(x):
        lignes = [l.strip() for l in str(x.get("run", "")).splitlines() if l.strip()]
        return lignes[-1] if lignes else ""

    def _neutralise(k):
        return bool(pas[k].get("continue-on-error")) or bool(job_du_pas[k].get("continue-on-error"))

    motif = re.compile(r"steps\.([A-Za-z0-9_-]+)\.outputs\." + re.escape(nom_de_sortie) + r"\b")
    rang = [k for k, x in enumerate(pas) if motif.search(_if(x)) and _derniere_ligne(x) == "exit 1"]
    if len(rang) != 1:
        return ["%d pas rouge(s) pour « %s » (if qui lit la sortie et run qui finit par « exit 1 ») : un seul attendu"
                % (len(rang), nom_de_sortie)]
    r = rang[0]
    lus = set(motif.findall(_if(pas[r])))
    if len(lus) != 1:
        return ["le pas rouge de « %s » lit %d id(s) : un seul attendu" % (nom_de_sortie, len(lus))]
    ident = lus.pop()
    canonique = ("always() && steps.%s.outputs.%s != '' && steps.%s.outputs.%s != '0'"
                 % (ident, nom_de_sortie, ident, nom_de_sortie))
    if _if(pas[r]) != canonique:
        manques.append("if du pas rouge de « %s » : %r au lieu de %r" % (nom_de_sortie, _if(pas[r]), canonique))
    sans_always = [k for k, x in enumerate(pas) if "always()" not in _if(x)]
    if sans_always and r < max(sans_always):
        manques.append("le pas rouge de « %s » (rang %d) précède un pas sans always() (rang %d)"
                       % (nom_de_sortie, r, max(sans_always)))
    if _neutralise(r):
        manques.append("le pas rouge de « %s » ou son job porte continue-on-error" % nom_de_sortie)
    tenir = [k for k, x in enumerate(pas) if x.get("id") == ident]
    if len(tenir) != 1:
        manques.append("%d pas portent l'id « %s » lu par le pas rouge : un seul attendu" % (len(tenir), ident))
        return manques
    t = tenir[0]
    if job_du_pas[t] is not job_du_pas[r]:
        manques.append("le pas « %s » et le pas rouge de « %s » ne sont pas dans le même job" % (ident, nom_de_sortie))
    if t >= r:
        manques.append("le pas « %s » ne précède pas le pas rouge" % ident)
    if programme not in str(pas[t].get("run", "")):
        manques.append("le pas « %s » ne lance pas %s" % (ident, programme))
    if _neutralise(t):
        manques.append("le pas « %s » ou son job porte continue-on-error" % ident)
    if _if(pas[t]) not in ("", "always()"):
        manques.append("le pas « %s » porte un if autre que always() : %r" % (ident, _if(pas[t])))
    return manques
