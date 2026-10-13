#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fabrique, à partir du dépôt privé, ce que le dépôt public doit porter pour faire tourner le circuit du soir.

① RÔLE — Recopier dans un clone du dépôt PUBLIC `cac40-cours-public` : ① les
  programmes que le circuit du soir exécute, tels qu'ils sont au dépôt privé ;
  ② le fichier du circuit, `.github/workflows/circuit_du_soir.yml`, FABRIQUÉ à
  partir de celui du dépôt privé (`.github/workflows/collecte_abc.yml`), pour
  qu'il n'existe qu'une seule rédaction des pas.
② CONTEXTE D'APPEL — Lancé à la main par le Chat, chaque fois qu'un des
  programmes publiés ou le fichier du circuit change au dépôt privé ; puis le
  Chat pousse le clone public. Jamais par une tâche automatique.
③ ENTRÉE — La ligne de commande : DEUX arguments, la racine du dépôt privé et
  celle du clone du dépôt public.
④ CONDITIONS D'ENTRÉE — Les deux dossiers existent ; chaque programme de
  `PROGRAMMES_PUBLICS` existe au dépôt privé ; le fichier du circuit privé a la
  forme attendue (voir ⑥). Sinon : arrêt, code 1, RIEN n'est écrit.
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
  qui rendrait quelque chose lisible au public (voir le code) · ④ écrire : programmes, fichier du
  circuit ; retirer du clone public tout programme qui n'est plus dans la liste.
⑦ UNITÉ — —
⑧ POURQUOI — Décision de Jean-Luc du 08-10-2026 (A-543) : le quota gratuit des
  machines GitHub du dépôt privé est épuisé ; un dépôt public ne consomme rien ;
  Jean-Luc a écarté de faire tourner depuis le public le code du privé (« Non
  pas question de prendre ces risques », zone grise des conditions d'usage de
  GitHub) et retenu de publier le circuit ET les programmes qu'il lance ; puis,
  le même soir à 22h29, de les publier avec leurs chiffres de stratégie pour le
  moment (A-556). Deux rédactions d'un même circuit divergent toujours (R-708) :
  celle du public est donc FABRIQUÉE depuis celle du privé, jamais écrite à la main.
⑨ CE QUI CLOCHE — `PROGRAMMES_PUBLICS` est une LISTE, relevée le 08-10-2026 en
  faisant tourner chaque pas du circuit sur une copie du dépôt et en notant
  chaque programme importé ou lancé : 20 programmes, plus les trois de ce
  chantier. Un chemin du circuit qui n'a pas tourné ce soir-là peut en appeler
  un autre ; ce programme-là serait alors exécuté depuis le clone du dépôt
  privé, sans alarme. Le pas qui pose les programmes n'en voit que la présence.
  Le job du circuit ne tourne que si le premier job a répondu « tourner » : si ce
  premier job tombe avant de répondre (clonage refusé, réseau), le passage ne fait
  rien et rougit ; le réveil suivant (secours du soir, rattrapage du matin) reprend.
⑩ EFFET — ÉCRIT dans le clone public : `programmes/*.py` et
  `.github/workflows/circuit_du_soir.yml` ; RETIRE de `programmes/` du clone
  public les programmes hors liste. Ne pousse rien.
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

PROGRAMMES_PUBLICS = (
    # relevés le 08-10-2026 en exécutant chaque pas du circuit (voir ⑨)
    "COLLECTER_ABC_GITHUB.py", "COMMUN.py", "CONTRATS_DES_FICHIERS.py",
    "CONTROLER_LES_COURS.py", "CONTROLER_LES_VALEURS_Lun_17-08-2026_18h20.py",
    "DETECTER_LES_SIGNAUX_GITHUB.py", "GENERATEUR_COCKPIT_Sam_15-08-2026_21h50.py",
    "JUGE_DES_STRATEGIES.py", "MESURER_LA_PERFORMANCE_Lun_17-08-2026_19h30.py",
    "MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py", "MODULE_JUGEMENT.py",
    "MODULE_POSITIONS.py", "PROTEGER_LA_PAGE.py", "PUBLIER_AU_DEPOT_PUBLIC.py",
    "PUBLIER_LE_SITE.py", "TENIR_LES_POSITIONS.py", "TENIR_L_HISTORIQUE.py",
    "audit_ecosysteme.py", "claude_FABRIQUER_LE_PILOTE.py", "verif_backlog.py",
    # écrits pour ce chantier (A-543)
    "ETAPE_MUETTE.py", "CONFRONTER_AUX_CONTRATS.py", "DIRE_LES_PAS_TOMBES.py",
    "FABRIQUER_LE_CIRCUIT_PUBLIC.py",
    # le premier job du circuit, qui dit si le passage doit tourner (13-10-2026)
    "FAUT_IL_TOURNER.py", "FAUT_IL_RATTRAPER.py", "CALENDRIER_DE_LA_BOURSE.py",
)

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
        description: "Relance du matin (saute la mesure de la performance)"
        type: boolean
        default: false
  # QUATRE REVEILS, ET C'EST L'HORLOGE DE PARIS QUI DECIDE (decision de Jean-Luc du
  # 13-10-2026 : 18h07, secours 21h23, rattrapage 7h41). GitHub compte en heure
  # universelle, qui ne suit pas l'heure d'ete ; programmes/FAUT_IL_TOURNER.py lit
  # l'heure de Paris au demarrage reel : jamais entre 9h et 18h, et seulement si la
  # derniere seance close n'est pas finie. Aucun reveil a l'heure pile : GitHub les
  # retarde en forte charge (passages de 23h25, 00h17, 02h10 avec 18h00 pile).
  schedule:
    - cron: "7 16 * * 1-5"     # 18h07 l'ete · 17h07 l'hiver (s'arrete)
    - cron: "7 17 * * 1-5"     # 19h07 l'ete (travail deja fait) · 18h07 l'hiver
    - cron: "23 19 * * 1-5"    # secours : 21h23 l'ete · 20h23 l'hiver
    - cron: "41 5 * * 2-6"     # rattrapage : 7h41 l'ete · 6h41 l'hiver, mesure sautee
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
          if [ -n "$D" ]; then echo "::error::PROGRAMMES PUBLICS DIFFERENTS DU DEPOT PRIVE :$D"; exit 1; fi
          cp _code/programmes/*.py programmes/
          mkdir -p "$RUNNER_TEMP/circuit_public"
          cp _code/.github/workflows/circuit_du_soir.yml "$RUNNER_TEMP/circuit_public/"
          rm -rf _code
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
    manquants = [p for p in PROGRAMMES_PUBLICS if not os.path.isfile(os.path.join(prive, "programmes", p))]
    if manquants:
        print("ARRÊT — programmes à publier absents du dépôt privé :", " ".join(manquants))
        return 1
    try:
        texte = fabriquer_le_circuit(open(os.path.join(prive, CIRCUIT_PRIVE), encoding="utf-8").read())
    except (OSError, ValueError) as e:
        print("ARRÊT — circuit public non fabriqué :", e)
        return 1
    os.makedirs(os.path.join(public, "programmes"), exist_ok=True)
    os.makedirs(os.path.dirname(os.path.join(public, CIRCUIT_PUBLIC)), exist_ok=True)
    for p in PROGRAMMES_PUBLICS:
        shutil.copyfile(os.path.join(prive, "programmes", p), os.path.join(public, "programmes", p))
    retires = sorted(f for f in os.listdir(os.path.join(public, "programmes"))
                     if f.endswith(".py") and f not in PROGRAMMES_PUBLICS)
    for f in retires:
        os.remove(os.path.join(public, "programmes", f))
    with open(os.path.join(public, CIRCUIT_PUBLIC), "w", encoding="utf-8") as s:
        s.write(texte)
    print(f"{len(PROGRAMMES_PUBLICS)} programmes copiés · {len(retires)} retiré(s) {' '.join(retires)}".rstrip())
    print(f"circuit fabriqué : {CIRCUIT_PUBLIC} ({len(texte.splitlines())} lignes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
