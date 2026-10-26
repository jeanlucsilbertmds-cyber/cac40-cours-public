#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fabrique, à partir du dépôt privé, ce que le dépôt public doit porter pour faire tourner le circuit du soir.

① RÔLE — Recopier dans un clone du dépôt PUBLIC `cac40-cours-public` : ① TOUS
  les programmes du dépôt privé (`programmes/*.py`), ses outils d'études
  (`etudes/outils/*.py`) et le code de sa racine (`*.py`, `emp.py` le 15-10-2026),
  tels qu'ils y sont ; ② le
  CODE des épreuves (`tests/*.py` et `tests/LANCEMENT_DES_EPREUVES.json`), sans
  leurs fichiers de données, qui restent au privé ; ③ le fichier du circuit du
  soir, `.github/workflows/circuit_du_soir.yml`, FABRIQUÉ à partir de celui du
  dépôt privé (`.github/workflows/collecte_abc.yml`), pour qu'il n'existe qu'une
  seule rédaction des pas ; ④ le fichier du circuit de la certification,
  `.github/workflows/certifier_la_version.yml`, écrit ICI et nulle part ailleurs ;
  ⑤ les fiches de circuit du privé (`.github/workflows/*.yml`), sous
  `circuits_du_prive/`, où GitHub ne les met pas en service.
② CONTEXTE D'APPEL — Lancé à la main par le Chat, chaque fois qu'un des
  programmes publiés ou le fichier du circuit change au dépôt privé ; puis le
  Chat pousse le clone public. Jamais par une tâche automatique.
③ ENTRÉE — La ligne de commande : DEUX arguments, la racine du dépôt privé et
  celle du clone du dépôt public.
④ CONDITIONS D'ENTRÉE — Les deux dossiers existent ; le dépôt privé porte au
  moins un programme et `tests/LANCEMENT_DES_EPREUVES.json` ; le fichier du
  circuit privé a la forme attendue (voir ⑥). Sinon : arrêt, code 1, RIEN n'est
  écrit.
⑤ SORTIE — UNE valeur : le code de sortie, 0 si tout est écrit, 1 sinon ; à
  l'écran, ce qui a été copié, retiré et fabriqué. [rend: 1]
⑥ TRAITEMENT — ① vérifier que chaque programme à publier existe · ② fabriquer
  le fichier du circuit : en-tête public, horaire, `defaults` qui fait passer
  chaque pas par `ETAPE_MUETTE.py`, les deux clonages (le privé à la racine,
  le public dans `_code/`) et le pas qui vérifie que les programmes publics
  sont ceux du privé puis les pose et efface `_code/` (sinon les programmes qui
  fouillent l'arborescence y trouveraient des fichiers en double), un pas qui
  refabrique le circuit et le compare à celui qui tourne, tous les pas du privé SANS leurs
  commentaires, le jeton du dépôt public remplacé par le secret `JETON_DEPOTS`
  (un commit fait avec le jeton de GitHub ne reconstruit pas la page publique du
  cockpit, relecture du 08-10-2026), et un
  dernier pas qui enregistre le journal au dépôt privé ; DEVANT ce job, un premier job
  `faut_il_tourner` (mêmes clonages, même journal) qui lance programmes/FAUT_IL_TOURNER.py,
  et dont la réponse conditionne le job du circuit ; la case « rattrapage » des pas du
  privé est remplacée par la réponse de ce premier job ; quatre réveils planifiés
  (décision de Jean-Luc du 13-10-2026, voir la fiche de FAUT_IL_TOURNER.py) · ③ refuser un pas privé
  qui rendrait quelque chose lisible au public (voir le code) · ④ écrire : programmes, code
  des épreuves, les deux fichiers de circuit ; retirer du clone public tout programme
  ou tout code d'épreuve qui n'est plus au dépôt privé. LES DEUX CIRCUITS REFUSENT DE
  TOURNER si un seul fichier de code diffère entre les deux dépôts, ou n'existe que d'un
  côté : ce que la machine exécute est donc, octet pour octet, ce que le dépôt public
  montre.
⑦ UNITÉ — —
⑧ POURQUOI — Décision de Jean-Luc du 08-10-2026 (A-543) : le quota gratuit des
  machines GitHub du dépôt privé est épuisé ; un dépôt public ne consomme rien ;
  Jean-Luc a écarté de faire tourner depuis le public le code du privé (« Non
  pas question de prendre ces risques », zone grise des conditions d'usage de
  GitHub) et retenu de publier le circuit ET les programmes qu'il lance ; puis,
  le même soir à 22h29, de les publier avec leurs chiffres de stratégie pour le
  moment (A-556). Deux rédactions d'un même circuit divergent toujours (R-708) :
  celle du public est donc FABRIQUÉE depuis celle du privé, jamais écrite à la main.
  Décision de Jean-Luc du 12-10-2026 à 16h46 (« Oui, construire », après la liste des
  fichiers et le point « il publierait tous les programmes au lieu d'une liste tenue à
  la main ») : la certification passe elle aussi au dépôt public, en y PUBLIANT le code
  qu'elle exécute, au lieu d'y exécuter le code du privé, qu'il avait écarté le
  08-10-2026 ; ordre confirmé le 15-10-2026 à 08h36 (A-580, A-576). Publier TOUS les
  programmes, et non une liste, répare le défaut que cette fiche consignait : un
  programme oublié dans la liste s'exécutait depuis le clone du dépôt privé, sans
  alarme.
⑨ CE QUI CLOCHE — Le contrôle d'identité porte sur `programmes/*.py`, `tests/*.py`
  et `tests/LANCEMENT_DES_EPREUVES.json`. Un pas qui lancerait du code rangé ailleurs
  (`etudes/outils/`, `tests/outils/`…) l'exécuterait depuis le clone du dépôt privé :
  relevé le 15-10-2026 par une relecture indépendante, des épreuves en lançaient
  (`emp.py`, cinq outils de `etudes/outils/`) : ils sont désormais publiés, et le pas
  « poser le code » de la certification EFFACE de la machine tout autre `*.py` privé, et
  tout code compilé (les suffixes que Python importe, calculés par Python lui-même :
  un paquet `.pyc` ou une extension `.so` passeraient avant le `.py` publié), avant de
  rien lancer ; il refuse les liens symboliques et voit les fichiers cachés. Un pas qui
  tourne après un échec (`always()`) ne tourne que si le code public est posé. Le circuit du soir, lui, n'efface rien : ses pas lisent tout le
  dépôt (le pilote, le radar) et son contrôle porte sur `programmes/*.py` seulement ;
  relevé le 08-10-2026, il ne lance aucun programme hors de `programmes/`. Le pas « Poser » du soir
  refuse tout fichier compilé (.pyc, .so, .pyd) OÙ QU'IL SOIT dans le clone, même hors de
  `programmes/` : plus large que nécessaire, laissé tel quel (relecteur du 21-10-2026, mineur 1). Il les
  reconnaît à leur SUFFIXE : une archive `.zip` ou un code compilé sous un autre nom n'est pas vu (voir ⑨ du garde). Le circuit de la certification est
  écrit dans ce programme, et non fabriqué depuis un fichier du privé :
  `.github/workflows/certifier.yml`, au privé, ne tourne plus (quota épuisé) et n'est
  pas la source de celui-ci.
  Le job du circuit ne tourne que si le premier job a répondu « tourner » : si ce
  premier job tombe avant de répondre (clonage refusé, réseau), le passage ne fait
  rien et rougit ; le réveil suivant (secours du soir, rattrapage du matin) reprend.
⑩ EFFET — ÉCRIT dans le clone public : les `*.py` de la racine, de `programmes/`,
  de `tests/` et de `etudes/outils/`, `tests/LANCEMENT_DES_EPREUVES.json`,
  `.github/workflows/circuit_du_soir.yml` et `.github/workflows/certifier_la_version.yml` ;
  et `circuits_du_prive/*.yml` ; RETIRE du clone public, à ces emplacements, ce qui
  est absent du dépôt privé. Ne pousse rien.
⑪ TERMINAISON — Rend la main. Aucun appel qui puisse ne pas revenir. [sort: oui]
⑫ DÉFINITIONS
  le circuit du soir : la suite de programmes lancés chaque soir de bourse par
    GitHub Actions — collecte des cours, versement, signaux, positions, mesure,
    pilote, radar.
  le dépôt privé : `jeanlucsilbertmds-cyber/Cac-40-signals-sur-git-hub-pour-Claude-`.
  le dépôt public : `jeanlucsilbertmds-cyber/cac40-cours-public`.
"""
import os
import re
import shutil
import sys

DEPOT_PRIVE = "jeanlucsilbertmds-cyber/Cac-40-signals-sur-git-hub-pour-Claude-"
CIRCUIT_PRIVE = os.path.join(".github", "workflows", "collecte_abc.yml")
CIRCUIT_PUBLIC = os.path.join(".github", "workflows", "circuit_du_soir.yml")

# LES QUATRE EMPLACEMENTS DU CODE PUBLIÉ, chacun sans ses sous-dossiers : la racine du dépôt (""), programmes/,
# tests/ et etudes/outils/. Décision de Jean-Luc du 15-10-2026 à 15h29 (« 1 ») : publier aussi les outils
# d'études et le code de la racine (emp.py), que des épreuves exécutent, et effacer tout autre code privé de la
# machine de la certification avant de rien lancer (relecture indépendante du 15-10-2026, cassures B1 et B2).
DOSSIERS_DE_CODE = ("", "programmes", "tests", "etudes/outils")


def _chemin(dossier, fichier):
    """Rend le chemin d'un fichier d'un emplacement de code, relatif à la racine.

    ① RÔLE — Écrire « emp.py » pour la racine et « programmes/X.py » ailleurs.
    ② CONTEXTE D'APPEL — `code_a_publier`, `main`.
    ③ ENTRÉE — `dossier` : un emplacement de DOSSIERS_DE_CODE (« » pour la racine) · `fichier` : un nom.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin.
      [rend: 1]
    ⑥ TRAITEMENT — joindre par « / », sauf pour la racine.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un seul endroit qui écrit ces chemins : le contrôle et la copie parlent la même langue.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return fichier if not dossier else dossier + "/" + fichier
LANCEMENT = "tests/LANCEMENT_DES_EPREUVES.json"
CIRCUIT_CERTIFICATION = os.path.join(".github", "workflows", "certifier_la_version.yml")
# LES FICHES DE CIRCUIT DU PRIVÉ, PUBLIÉES À PART (décision de Jean-Luc du 15-10-2026 à 20h32, « 1 ») : une épreuve
# publiée (celle du rattrapage) EXÉCUTE un pas écrit dans une fiche `.github/workflows/*.yml` du dépôt qu'on lui donne
# (relecture de Cowork 5855cd4, cassure L). Les fiches du privé sont donc publiées, et comparées comme le code, mais
# dans ce dossier-ci et jamais dans `.github/workflows/` du public, où GitHub les mettrait en service.
FICHES_PRIVEES = os.path.join(".github", "workflows")
FICHES_PUBLIEES = "circuits_du_prive"


def fiches_a_publier(prive):
    """Rend les noms des fiches de circuit du dépôt privé (`.github/workflows/*.yml` et `*.yaml`).

    ① RÔLE — Dire quelles fiches de circuit vont au public, sous `circuits_du_prive/`.
    ② CONTEXTE D'APPEL — `main` ; les épreuves du circuit public.
    ③ ENTRÉE — `prive` : la racine du dépôt privé.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste triée des noms de fichiers (vide si aucun).
      [rend: 1]
    ⑥ TRAITEMENT — lister le dossier des fiches, garder les fichiers `.yml` et `.yaml`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une fiche de circuit est du code : ses pas s'exécutent (cassure L, 15-10-2026). Une propriété, pas
      une liste : une fiche ajoutée au privé est publiée sans qu'on y pense.
    ⑨ CE QUI CLOCHE — Les sous-dossiers ne sont pas parcourus : GitHub n'y lit aucune fiche.
    ⑩ EFFET — Lit un dossier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    d = os.path.join(prive, FICHES_PRIVEES)
    if not os.path.isdir(d):
        return []
    return sorted(f for f in os.listdir(d) if f.endswith((".yml", ".yaml")) and os.path.isfile(os.path.join(d, f)))


def code_a_publier(prive):
    """Rend la liste des fichiers de code du dépôt privé qui vont au public.

    ① RÔLE — Dire quels fichiers publier : tout `*.py` de la racine, de `programmes/`,
      de `tests/` et de `etudes/outils/`, et `tests/LANCEMENT_DES_EPREUVES.json`, en
      chemins relatifs à la racine.
    ② CONTEXTE D'APPEL — `main` ; les épreuves du circuit public.
    ③ ENTRÉE — `prive` : la racine du dépôt privé.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste triée des chemins (vide si rien).
      [rend: 1]
    ⑥ TRAITEMENT — lister les quatre emplacements, garder les fichiers `.py`, ajouter
      le fichier de lancement s'il existe.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une propriété, jamais une énumération : renommer ou ajouter un
      programme ne doit pas le faire sortir de la publication (voir la fiche du
      fichier, ⑧).
    ⑨ CE QUI CLOCHE — Les sous-dossiers ne sont pas parcourus : relevé le 15-10-2026,
      `programmes/` n'en a pas ; ceux de `tests/` portent des données (`resultats/`,
      `temoins_*`) et un programme, `tests/outils/`. Le code qui n'est pas publié est
      EFFACÉ de la machine de la certification avant qu'elle ne lance rien (son pas
      « poser le code ») : une épreuve qui en aurait besoin rougit, elle ne l'exécute pas.
    ⑩ EFFET — Lit deux dossiers.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    rendu = []
    for dossier in DOSSIERS_DE_CODE:
        d = os.path.join(prive, dossier)
        if os.path.isdir(d):
            rendu += [_chemin(dossier, f) for f in os.listdir(d)
                      if f.endswith(".py") and os.path.isfile(os.path.join(d, f))]
    if os.path.isfile(os.path.join(prive, LANCEMENT)):
        rendu.append(LANCEMENT)
    return sorted(rendu)


ENTETE = """# CIRCUIT DU SOIR — FICHIER FABRIQUÉ, NE PAS ÉCRIRE À LA MAIN.
# Fabriqué par programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py à partir du fichier du circuit
# du dépôt privé (A-543). Il fait tourner les programmes de ce dépôt sur les données
# du dépôt privé. Chaque pas passe par programmes/ETAPE_MUETTE.py : le journal public
# ne dit que « étape … : OK » ou « étape … : ÉCHEC » ; le détail est au dépôt privé.
name: Circuit du soir
on:
  workflow_dispatch:
    inputs:
      rattrapage:
        description: "Passage sans mesure de la performance"
        type: boolean
        default: false
  # QUATRE REVEILS, ET C'EST L'HORLOGE DE PARIS QUI DECIDE (decision de Jean-Luc du
  # 13-10-2026 : 18h07, secours 21h23, rattrapage 7h41). GitHub compte en heure
  # universelle, qui ne suit pas l'heure d'ete ; programmes/FAUT_IL_TOURNER.py lit
  # l'heure de Paris au demarrage reel : il tourne seulement si la derniere seance
  # close n'est pas finie (celle du jour apres 18h, la veille avant). Aucun reveil a l'heure pile : GitHub les
  # retarde en forte charge (passages de 23h25, 00h17, 02h10 avec 18h00 pile).
  schedule:
    - cron: "7 16 * * 1-5"     # 18h07 l'ete · 17h07 l'hiver (s'arrete si la veille est faite)
    - cron: "7 17 * * 1-5"     # 19h07 l'ete (travail deja fait) · 18h07 l'hiver
    - cron: "23 19 * * 1-5"    # secours : 21h23 l'ete · 20h23 l'hiver
    - cron: "41 5 * * 2-6"     # rattrapage : 7h41 l'ete · 6h41 l'hiver
concurrency:
  group: circuit-du-soir
  cancel-in-progress: false
permissions:
  contents: write
jobs:
"""

DEFAULTS = """    defaults:
      run:
        shell: python3 programmes/ETAPE_MUETTE.py {0}
"""

CLONAGES = """      - uses: actions/checkout@v5
        with:
          repository: %s
          token: ${{ secrets.JETON_DEPOTS }}
          fetch-depth: 0
      - uses: actions/checkout@v5
        with:
          path: _code
      - name: Poser les programmes publics, s'ils sont ceux du depot prive
        id: poser_les_programmes
        shell: python3 _code/programmes/ETAPE_MUETTE.py {0}
        run: |
          D=""
          for f in _code/programmes/*.py; do
            n=$(basename "$f")
            if [ -f "programmes/$n" ] && ! cmp -s "$f" "programmes/$n"; then D="$D $n"; fi
          done
          for f in programmes/*.py; do
            n=$(basename "$f")
            [ -f "_code/programmes/$n" ] || D="$D $n(absent-du-public)"
          done
          for x in programmes/*; do [ -d "$x" ] && D="$D $x(dossier)"; done
          for x in $(find . -path ./_code -prune -o -path ./.git -prune -o \\( -name '*.pyc' -o -name '*.so' -o -name '*.pyd' \\) -print); do D="$D $x(compile)"; done
          if [ -n "$D" ]; then echo "::error::PROGRAMMES PUBLICS DIFFERENTS DU DEPOT PRIVE :$D"; exit 1; fi
          cp _code/programmes/*.py programmes/
          mkdir -p "$RUNNER_TEMP/circuit_public" "$RUNNER_TEMP/garde"
          cp _code/.github/workflows/circuit_du_soir.yml "$RUNNER_TEMP/circuit_public/"
          cp _code/programmes/N_EXECUTER_AU_PUBLIC_QUE_LE_CODE_PUBLIE.py "$RUNNER_TEMP/garde/sitecustomize.py"
          rm -rf "$RUNNER_TEMP/code" && mv _code "$RUNNER_TEMP/code"
          { echo "PYTHONPATH=$RUNNER_TEMP/garde"; echo "PYTHONDONTWRITEBYTECODE=1"; echo "GARDE_DONNEES=$GITHUB_WORKSPACE"; echo "GARDE_CODE=$RUNNER_TEMP/code"; } >> "$GITHUB_ENV"
      - name: Le garde du code mord-il ?
        id: garde_du_code
        run: |
          printf 'print("piege du garde")\\n' > _piege_du_garde.py
          c=0; python3 -c "import sys; sys.path.insert(0, '.'); import _piege_du_garde" || c=$?
          rm -rf _piege_du_garde.py __pycache__/_piege_du_garde.*
          [ "$c" -eq 97 ] || { echo "::error::LE GARDE DU CODE NE MORD PAS (code $c au lieu de 97) — du code du depot prive pourrait tourner"; exit 1; }
          echo "garde du code : en place"
      - name: Le circuit public est-il celui que fabrique le depot prive ?
        id: circuit_a_jour
        continue-on-error: true
        run: |
          rm -rf "$RUNNER_TEMP/refait" && mkdir -p "$RUNNER_TEMP/refait"
          python3 programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py . "$RUNNER_TEMP/refait"
          cmp "$RUNNER_TEMP/refait/.github/workflows/circuit_du_soir.yml" "$RUNNER_TEMP/circuit_public/circuit_du_soir.yml" \
            || { echo "::error::LE CIRCUIT PUBLIC N EST PLUS CELUI DU DEPOT PRIVE — refabriquer et pousser"; exit 1; }
""" % DEPOT_PRIVE

JOURNAL = """      - name: Enregistrer le journal du passage au depot prive
        id: journal
        if: always()
        shell: bash
        run: |
          git rebase --abort 2>/dev/null || true
          git add rapports/journal_du_circuit/ || { echo "journal introuvable"; exit 1; }
          if git diff --cached --quiet; then echo "journal : rien a enregistrer"; exit 0; fi
          git -c user.name=circuit-public -c user.email=circuit-public@users.noreply.github.com commit -q -m "journal du circuit public, passage ${GITHUB_RUN_ID} [skip ci]"
          for i in 1 2 3; do
            if git pull -q --rebase --autostash origin main && git push -q; then echo "journal : enregistre"; exit 0; fi
            sleep 5
          done
          echo "journal : POUSSEE REFUSEE 3 FOIS"; exit 1
"""

DECISION_ENTETE = """  faut_il_tourner:
    runs-on: ubuntu-latest
    outputs:
      tourner: ${{ steps.decision.outputs.tourner }}
      rattrapage: ${{ steps.decision.outputs.rattrapage }}
""" + DEFAULTS + "    steps:\n"

DECISION_PAS = """      - name: Faut-il tourner ?
        id: decision
        run: |
          set +e
          python3 programmes/FAUT_IL_TOURNER.py . "${{ github.event_name }}" "${{ inputs.rattrapage }}"
          echo "code=$?" >> "$GITHUB_OUTPUT"
      - name: Rougir si la decision n a pas pu se prendre
        if: steps.decision.outputs.code != '0'
        run: |
          echo "::error::DECISION IMPOSSIBLE OU PAR PRECAUTION — voir le journal du passage au depot prive"
          exit 1
"""

JOB_PRIVE = "  collecte:\n"
JOB_CONDITION = """  collecte:
    needs: faut_il_tourner
    if: ${{ !cancelled() && needs.faut_il_tourner.outputs.tourner == 'true' }}
"""
RATTRAPAGE_PRIVE = "${{ inputs.rattrapage }}"
RATTRAPAGE_PUBLIC = "${{ needs.faut_il_tourner.outputs.rattrapage }}"

CERTIFICATION = """# CERTIFIER LA VERSION — FICHIER FABRIQUÉ, NE PAS ÉCRIRE À LA MAIN.
# Fabriqué par programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py (décision de Jean-Luc du 12-10-2026 à
# 16h46, ordre confirmé le 15-10-2026 à 08h36). La certification rejoue toutes les épreuves et
# dit si la version du dépôt privé est certifiée. Elle n'exécute QUE le code de ce dépôt public :
# le pas « poser le code public » refuse de continuer si un seul fichier de programmes/ ou de
# tests/ diffère du dépôt privé ou n'existe que d'un côté. Les données des épreuves sont lues au
# dépôt privé, jamais publiées. Chaque pas passe par programmes/ETAPE_MUETTE.py : le journal
# public ne dit que « OK » ou « ÉCHEC » ; le détail est au dépôt privé.
name: Certifier la version
on:
  workflow_dispatch:
  # 21h00 en heure universelle : 23h00 à Paris l'été, 22h00 l'hiver, après le circuit du soir
  # (dont des épreuves lisent les données). GitHub peut retarder un réveil de plusieurs heures.
  schedule:
    - cron: "0 21 * * 1-5"
concurrency:
  group: certifier-la-version
  cancel-in-progress: false
permissions:
  contents: read
jobs:
  certifier:
    runs-on: ubuntu-latest
    # 330 minutes (16-10-2026) : la série de la lecture des cours reçoit 3 heures à elle ; GitHub coupe à 6 heures.
    timeout-minutes: 330
    defaults:
      run:
        shell: python3 programmes/ETAPE_MUETTE.py {0}
    steps:
      - uses: actions/checkout@v5
        with:
          repository: %s
          token: ${{ secrets.JETON_DEPOTS }}
          fetch-depth: 0
      - uses: actions/checkout@v5
        with:
          path: _code
      - name: Poser le code public, s'il est celui du depot prive
        id: poser_le_code
        shell: python3 _code/programmes/ETAPE_MUETTE.py {0}
        run: |
          D=""
          L=$(find . -name '*.py' -type l -print | head -5 | paste -sd ' ' -)
          [ -z "$L" ] || D="$D liens-symboliques:$L"
          for d in . programmes tests etudes/outils; do
            while IFS= read -r -d '' f; do
              n=${f##*/}
              if [ ! -f "$d/$n" ]; then D="$D $d/$n(absent-du-prive)"; elif ! cmp -s "$f" "$d/$n"; then D="$D $d/$n"; fi
            done < <(find "_code/$d" -maxdepth 1 -name '*.py' -type f -print0 2>/dev/null)
            while IFS= read -r -d '' f; do
              n=${f##*/}
              [ -f "_code/$d/$n" ] || D="$D $d/$n(absent-du-public)"
            done < <(find "$d" -maxdepth 1 -name '*.py' -type f -print0)
          done
          cmp -s _code/tests/LANCEMENT_DES_EPREUVES.json tests/LANCEMENT_DES_EPREUVES.json || D="$D tests/LANCEMENT_DES_EPREUVES.json"
          while IFS= read -r -d '' f; do
            n=${f##*/}
            if [ ! -f ".github/workflows/$n" ]; then D="$D fiche:$n(absent-du-prive)"; elif ! cmp -s "$f" ".github/workflows/$n"; then D="$D fiche:$n"; fi
          done < <(find _code/circuits_du_prive -maxdepth 1 \\( -name '*.yml' -o -name '*.yaml' \\) -type f -print0 2>/dev/null)
          while IFS= read -r -d '' f; do
            n=${f##*/}
            [ -f "_code/circuits_du_prive/$n" ] || D="$D fiche:$n(absent-du-public)"
          done < <(find .github/workflows -maxdepth 1 \\( -name '*.yml' -o -name '*.yaml' \\) -type f -print0)
          if [ -n "$D" ]; then echo "::error::CODE PUBLIC DIFFERENT DU DEPOT PRIVE :$D"; exit 1; fi
          find . -path ./_code -prune -o -path ./.git -prune -o -name __pycache__ -type d -prune -exec rm -rf {} +
          find . -path ./_code -prune -o -path ./.git -prune -o -name '*.py' -type f -print0 | grep -zvE '^[.]/[^/]+[.]py$|^[.]/(programmes|tests|etudes/outils)/[^/]+[.]py$' | xargs -0 -r rm -f
          X=$(python3 -c "import importlib.machinery as m; print('|'.join(s.replace('.', '[.]') for s in m.all_suffixes() if s != '.py'))")
          find . -path ./_code -prune -o -path ./.git -prune -o -type f -print0 | grep -zE "($X)$" | xargs -0 -r rm -f
          R=$(find . -path ./_code -prune -o -path ./.git -prune -o -name '*.py' -print | grep -cvE '^[.]/[^/]+[.]py$|^[.]/(programmes|tests|etudes/outils)/[^/]+[.]py$' || true)
          C=$(find . -path ./_code -prune -o -path ./.git -prune -o -type f -print | grep -cE "($X)$" || true)
          [ "$R" = "0" ] && [ "$C" = "0" ] || { echo "::error::CODE PRIVE NON PUBLIE ENCORE PRESENT : $R source(s), $C compile(s)"; exit 1; }
          for d in . programmes tests etudes/outils; do
            for f in _code/$d/*.py; do [ -e "$f" ] && cp "$f" "$d/"; done
          done
          cp _code/tests/LANCEMENT_DES_EPREUVES.json tests/
          mkdir -p "$RUNNER_TEMP/circuit_public"
          cp _code/.github/workflows/certifier_la_version.yml "$RUNNER_TEMP/circuit_public/"
          rm -rf _code
      - name: Le circuit de certification est-il celui que fabrique le depot prive ?
        id: circuit_a_jour
        run: |
          rm -rf "$RUNNER_TEMP/refait" && mkdir -p "$RUNNER_TEMP/refait"
          python3 programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py . "$RUNNER_TEMP/refait"
          cmp "$RUNNER_TEMP/refait/.github/workflows/certifier_la_version.yml" "$RUNNER_TEMP/circuit_public/certifier_la_version.yml" \\
            || { echo "::error::LE CIRCUIT DE CERTIFICATION N EST PLUS CELUI DU DEPOT PRIVE — refabriquer et pousser"; exit 1; }
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      # Les logiciels que les programmes cherchent par shutil.which : pdftotext (les PDF) et soffice
      # (les .doc). Absents de la machine de GitHub, ils ont fait rougir trois epreuves au premier
      # certificat public (16-10-2026, f5aac6b). continue-on-error : si l'installation tombe, la
      # certification tourne quand meme, et les epreuves qui en ont besoin rougissent en le disant.
      - name: Installer les logiciels que lisent les programmes
        id: logiciels
        continue-on-error: true
        run: |
          command -v pdftotext >/dev/null || { sudo apt-get update -qq && sudo apt-get install -y -qq poppler-utils; }
          command -v soffice >/dev/null || command -v libreoffice >/dev/null || { sudo apt-get update -qq && sudo apt-get install -y -qq --no-install-recommends libreoffice-writer-nogui; }
          pdftotext -v
          soffice --version || libreoffice --version
      - name: Installer la mesure et les dependances des programmes
        id: installer
        run: python3 -m pip install --quiet "coverage==7.16.2" cryptography pyyaml
      - name: Certifier
        id: certifier
        continue-on-error: true
        run: python3 -B programmes/CERTIFIER_LA_VERSION.py "$GITHUB_WORKSPACE"
      - name: Deposer le certificat et le journal au depot prive
        id: deposer
        if: always()
        shell: bash
        run: |
          git config user.name certification-publique
          git config user.email certification-publique@users.noreply.github.com
          git rebase --abort 2>/dev/null || true
          git add rapports/CERTIFICAT_DE_LA_VERSION.md rapports/journal_du_circuit/ \\
            || { echo "::error::certificat ou journal introuvable"; exit 1; }
          if git diff --cached --quiet; then echo "rien a deposer"; exit 0; fi
          git commit -q -m "certificat de la version, passage public ${GITHUB_RUN_ID} [skip ci]"
          for i in 1 2 3; do
            if git pull -q --rebase --autostash origin main && git push -q; then echo "depose"; exit 0; fi
            sleep 5
          done
          echo "::error::POUSSEE REFUSEE 3 FOIS — le certificat reste sur la machine jetable"; exit 1
      - name: Rougir si la version n'est pas certifiee
        id: verdict
        if: ${{ !cancelled() && steps.poser_le_code.outcome == 'success' && steps.certifier.outcome != 'success' }}
        run: |
          echo "::error::VERSION NON CERTIFIEE — lire rapports/CERTIFICAT_DE_LA_VERSION.md au depot prive"
          exit 1
""" % DEPOT_PRIVE

CHECKOUT_PRIVE = re.compile(r"      - uses: actions/checkout@v5\n        with:\n(?:\s*#.*\n)*\s*fetch-depth: 0\n")


def fabriquer_le_circuit(texte_prive):
    """Fabrique le texte du fichier du circuit public à partir de celui du privé.

    ① RÔLE — Transformer le texte du circuit privé en circuit public.
    ② CONTEXTE D'APPEL — `main`, une fois ; les épreuves.
    ③ ENTRÉE — `texte_prive` : le contenu de `.github/workflows/collecte_abc.yml`.
    ④ CONDITIONS D'ENTRÉE — Le texte porte `jobs:`, `runs-on: ubuntu-latest` et un
      clonage `actions/checkout@v5` avec `fetch-depth: 0`, chacun UNE fois ; son job
      s'appelle `collecte` ; il porte `${{ inputs.rattrapage }}` UNE fois.
    ⑤ SORTIE — UNE valeur : le texte du circuit public ; lève `ValueError` si une
      forme attendue manque ou s'il reste du code Python écrit. [rend: 1]
      [rend: 1]
    ⑥ TRAITEMENT — Voir l'en-tête du programme, ⑥ ②-③.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir l'en-tête, ⑧ : une seule rédaction des pas.
    ⑨ CE QUI CLOCHE — Les commentaires sont retirés ligne entière : un « # » en
      fin de ligne de commande reste.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. [sort: non]
      [sort: non]
    """
    if texte_prive.count("\njobs:\n") != 1:
        raise ValueError("le circuit privé ne porte pas une seule ligne « jobs: »")
    corps = corps_prive = texte_prive.split("\njobs:\n", 1)[1]
    if corps.count("    runs-on: ubuntu-latest\n") != 1:
        raise ValueError("« runs-on: ubuntu-latest » absent ou répété")
    if len(CHECKOUT_PRIVE.findall(corps)) != 1:
        raise ValueError("le clonage du dépôt privé n'a pas la forme attendue")
    if not corps.startswith(JOB_PRIVE):
        raise ValueError("le circuit privé ne commence pas par le job « collecte: »")
    if corps.count(RATTRAPAGE_PRIVE) != 1:
        raise ValueError(f"« {RATTRAPAGE_PRIVE} » absent ou répété dans le circuit privé")
    corps = corps.replace(JOB_PRIVE, JOB_CONDITION, 1).replace(RATTRAPAGE_PRIVE, RATTRAPAGE_PUBLIC)
    corps = CHECKOUT_PRIVE.sub(lambda m: CLONAGES, corps)
    corps = corps.replace("    runs-on: ubuntu-latest\n", "    runs-on: ubuntu-latest\n" + DEFAULTS, 1)
    corps = corps.replace("${{ secrets.TOKEN_PUBLIC }}", "${{ secrets.JETON_DEPOTS }}")
    # UN PAS « always() » DU PRIVÉ NE TOURNE QUE SI LE CODE PUBLIC EST POSÉ : sinon il exécuterait les programmes du
    # clone privé (relecture du 15-10-2026, A3 : un refus de « poser les programmes », puis le pas qui dit les pas tombés).
    corps = corps.replace("        if: always()\n", "        if: ${{ always() && steps.poser_les_programmes.outcome == 'success' }}\n")
    lignes = [l for l in corps.split("\n") if not l.lstrip().startswith("#")]
    texte = (ENTETE + DECISION_ENTETE + CLONAGES + DECISION_PAS + JOURNAL
             + "\n".join(lignes).rstrip("\n") + "\n" + JOURNAL)
    for interdit in ("secrets.TOKEN_PUBLIC",):
        if interdit in texte:
            raise ValueError(f"il reste « {interdit} » dans le circuit public")
    # CE QUE LES PAS DU PRIVÉ NE DOIVENT PAS PORTER, parce que le circuit public le
    # rendrait lisible (relecture du 08-10-2026, sabotages S1 à S5) : un interpréteur
    # propre (sa sortie échapperait à l'enrobage), une action autre que le clonage
    # (une archive jointe est téléchargeable), du code Python écrit, un texte « << »
    # (un commentaire y serait retiré), le résumé public du passage.
    for motif, raison in ((r"^\s*shell:", "un pas qui déclare son propre interpréteur"),
                          (r"^\s*-?\s*uses:\s*(?!\s|actions/checkout@)", "une action autre que le clonage"),
                          (r"python3?\s+(?:-\w+\s+)*-c\b", "du code Python écrit dans le fichier"),
                          (r"python3?\s+(?:-\w+\s+)*-\s", "du code Python lu sur l'entrée"),
                          (r"<<", "un texte « << »"),
                          (r"GITHUB_STEP_SUMMARY", "le résumé public du passage")):
        if re.search(motif, corps_prive, re.M):
            raise ValueError(f"le circuit privé porte {raison}")
    return texte


def main():
    """Vérifie, fabrique, écrit.

    ① RÔLE — Voir l'en-tête.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — Deux arguments : racine privée, clone public.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête.
    ⑤ SORTIE — UNE valeur : le code de sortie. [rend: 1]
      [rend: 1]
    ⑥ TRAITEMENT — Voir l'en-tête.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir l'en-tête.
    ⑨ CE QUI CLOCHE — Voir l'en-tête.
    ⑩ EFFET — Voir l'en-tête.
    ⑪ TERMINAISON — Rend la main. [sort: oui]
      [sort: non]
    """
    if len(sys.argv) != 3:
        print("usage : FABRIQUER_LE_CIRCUIT_PUBLIC.py <racine du dépôt privé> <clone du dépôt public>")
        return 1
    prive, public = sys.argv[1], sys.argv[2]
    a_publier = code_a_publier(prive)
    if not any(f.startswith("programmes/") for f in a_publier) or LANCEMENT not in a_publier:
        print("ARRÊT — le dépôt privé ne porte pas de programmes, ou pas", LANCEMENT)
        return 1
    try:
        texte = fabriquer_le_circuit(open(os.path.join(prive, CIRCUIT_PRIVE), encoding="utf-8").read())
    except (OSError, ValueError) as e:
        print("ARRÊT — circuit public non fabriqué :", e)
        return 1
    for dossier in DOSSIERS_DE_CODE:
        os.makedirs(os.path.join(public, dossier), exist_ok=True)
    os.makedirs(os.path.dirname(os.path.join(public, CIRCUIT_PUBLIC)), exist_ok=True)
    for f in a_publier:
        shutil.copyfile(os.path.join(prive, f), os.path.join(public, f))
    fiches = fiches_a_publier(prive)
    os.makedirs(os.path.join(public, FICHES_PUBLIEES), exist_ok=True)
    for f in fiches:
        shutil.copyfile(os.path.join(prive, FICHES_PRIVEES, f), os.path.join(public, FICHES_PUBLIEES, f))
    fiches_retirees = sorted(f for f in os.listdir(os.path.join(public, FICHES_PUBLIEES)) if f not in fiches)
    for f in fiches_retirees:
        os.remove(os.path.join(public, FICHES_PUBLIEES, f))
    retires = sorted(_chemin(d, f) for d in DOSSIERS_DE_CODE for f in os.listdir(os.path.join(public, d))
                     if f.endswith(".py") and os.path.isfile(os.path.join(public, d, f)) and _chemin(d, f) not in a_publier)
    for f in retires:
        os.remove(os.path.join(public, f))
    with open(os.path.join(public, CIRCUIT_PUBLIC), "w", encoding="utf-8") as s:
        s.write(texte)
    with open(os.path.join(public, CIRCUIT_CERTIFICATION), "w", encoding="utf-8") as s:
        s.write(CERTIFICATION)
    print(f"{len(a_publier)} fichiers de code copiés · {len(retires)} retiré(s) {' '.join(retires)}".rstrip())
    print(f"{len(fiches)} fiches de circuit du privé copiées dans {FICHES_PUBLIEES}/ · {len(fiches_retirees)} retirée(s) "
          f"{' '.join(fiches_retirees)}".rstrip())
    print(f"circuit fabriqué : {CIRCUIT_PUBLIC} ({len(texte.splitlines())} lignes)")
    print(f"circuit fabriqué : {CIRCUIT_CERTIFICATION} ({len(CERTIFICATION.splitlines())} lignes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
