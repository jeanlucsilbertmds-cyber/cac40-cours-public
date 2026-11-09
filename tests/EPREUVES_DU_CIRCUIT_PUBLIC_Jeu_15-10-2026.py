#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_CIRCUIT_PUBLIC — Jeu 15-10-2026 (Paris). Simulation uniquement.

① RÔLE — Prouver que programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py publie TOUT le code que les circuits publics
  exécutent (programmes, code des épreuves, fichier de lancement), et rien des données des épreuves ; que les
  deux circuits publics (circuit du soir, certification) refusent de tourner si un seul fichier de code diffère
  entre le dépôt privé et le dépôt public, ou n'existe que d'un côté ; et que chaque épreuve a des dents.
② CONTEXTE D'APPEL — À la main, avant toute livraison qui touche programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py ou
  .github/workflows/collecte_abc.yml, que le fabricant transforme (R-731 ; superviseur R-759 du 30-10-2026, ③3) :
  python3 tests/EPREUVES_DU_CIRCUIT_PUBLIC_Jeu_15-10-2026.py <racine du dépôt privé> [--saboter]
③ ENTRÉE — La racine du dépôt privé (ses vrais programmes, ses vraies épreuves, ses vrais fichiers de données).
④ CONDITIONS D'ENTRÉE — Le module yaml (PyYAML) s'importe : sans lui, l'épreuve s'arrête (code 2).
⑤ SORTIE — UNE valeur : le code de sortie — 0 si Z0 est vert et, avec --saboter, si chaque sabotage fait rougir
  l'épreuve ; 1 sinon ; 2 si un sabotage ne s'applique plus, si yaml manque ou si deux sabotages portent le même
  numéro.
  [rend: 1]
⑥ TRAITEMENT — Pour Z0 puis pour chaque sabotage : copier le dépôt (sans .git), y appliquer le sabotage, lancer le
  fabricant vers un faux clone public qui porte un programme et une épreuve « seulement au public », puis :
  E1 chaque fichier de code du privé arrive, identique, au public, chaque fiche de circuit du privé arrive,
     identique, sous circuits_du_prive/, et aucun fichier de données des épreuves n'y arrive ; E2 ce qui n'existe qu'au public est retiré ; E3 le circuit de la certification se lit (YAML) et ne se
     déclenche ni sur une proposition de modification (pull_request, pull_request_target) ni sur un commentaire
     (issue_comment) ni sur un autre circuit (workflow_run) — les seuls déclenchements qui donnent les secrets du
     dépôt à un inconnu ; et, dans tous les jobs des deux circuits, aucun pas dont la condition appelle une fonction
     d'état (always(), failure(), cancelled(), success(), avec ou sans « ! ») ne peut tourner sur un code non posé —
     jugé par LA propriété du fabricant, `condition_exige_le_code_pose`, importée du dépôt éprouvé et jamais recopiée
     (R-708) —, sauf les pas déclarés `shell: bash` : le fabricant refuse tout `shell:` venu du privé, ce sont donc
     les pas écrits par lui, JOURNAL et « deposer » (relecture du 15-10-2026, A3 ; superviseur R-759 du 30-10-2026) ;
     E3 ter la propriété est calibrée sur des cas connus, qui doivent la satisfaire ou la violer ; E3 quater sur le
     circuit privé accepté et les deux circuits fabriqués, la liste blanche du fabricant (`conditions_du_circuit`) et
     yaml trouvent les mêmes conditions — un étalonnage, pas un arbitre : PyYAML n'est pas le lecteur de GitHub ; E3 quinquies le fabricant de la copie refuse chaque forme hors du
     sous-ensemble YAML qu'il lit (FORMES_HORS_SOUS_ENSEMBLE ; superviseur R-759, second tour, R3) ;
     E4 son pas « poser le code », EXÉCUTÉ par bash -e dans un espace fabriqué : vert quand
     tout est identique, rouge sur un programme différent, une épreuve seulement au privé, une épreuve seulement au
     public, un programme seulement au privé, un fichier de lancement différent, emp.py différent, un outil
     d'études différent ou seulement au privé, un lien symbolique, un programme caché (« .x.py ») seulement au privé,
     une fiche de circuit du privé modifiée, ou présente d'un seul côté (cassure L de Cowork, 15-10-2026 : une épreuve
     publiée exécute un pas écrit dans une fiche du privé) ;
     et, quand il passe, plus aucun code privé non publié ne reste sur la machine (un fichier d'archives/, un
     sous-dossier de programmes/, un paquet compilé programmes/COMMUN/__init__.pyc, que Python préférerait à
     COMMUN.py — relecture du 15-10-2026, A1) ; E5 le pas « poser les
     programmes » du circuit du soir, exécuté de même : vert quand tout est identique, rouge sur un programme
     seulement au privé et sur un programme différent ; E6 chaque logiciel que le code publié cherche par
     shutil.which (relevé dans le code : pdftotext, soffice, libreoffice le 16-10-2026) est vérifié par
     « command -v » dans un pas placé avant la certification (ajouté le 16-10-2026 : pdftotext et soffice
     manquaient à la machine de GitHub, trois épreuves rouges au certificat f5aac6b) ; E6 bis chaque paquet Python
     qu'installe la certification privée (« pip install » de .github/workflows/certifier.yml, lus dans le fichier) est
     installé, écrit de même, avant le pas « certifier » du job fabriqué, par un pas sans « if » ni
     « continue-on-error », sur une ligne qui commence par la commande, et au moins un paquet y est lu (ajouté le
     31-10-2026 : pyflakes manquait au public, E12 des frais y rougissait, certificat 7980a86) ; E7 le garde du code
     (programmes/N_EXECUTER_AU_PUBLIC_QUE_LE_CODE_PUBLIE.py) : le pas « Le garde du code mord-il ? » est vert avec le garde, rouge sans
     lui et rouge avec un garde dont la porte des imports est morte ; un module publié s'importe ; les pièges
     A à D sont arrêtés (ajouté le 21-10-2026 sur le prototype du superviseur) ; E8 (défaut M5, relecture de Cowork du
     04-11-2026 à 21h17 ; tour 2 sur le superviseur R-759 du 05-11-2026 à 00h52), JOUÉE AVANT la fabrication
     principale : ① le motif de programmes/FORME_D_UN_JETON.py de la copie reconnaît chaque cas positif de
     CAS_DU_MOTIF et aucun cas négatif ; ② parmi le code publié, ce module est le SEUL à compiler un motif de jeton,
     détecteur calibré à chaque passage sur un motif (doit être vu) et sur une citation du mot (ne doit pas l'être) ;
     ③ en UNE course, un lien hors du dépôt et un jeton placé après 9 000 octets dans CHAQUE emplacement de code LU
     AU FABRICANT, un jeton loin dans le fichier de lancement, une fiche liée hors du dépôt et une fiche à jeton loin,
     un lien vers un fichier du dépôt, un lien dur hors du dépôt, un jeton en UTF-16-LE sans BOM (clause des
     contrôles du texte strict) et un jeton en EBCDIC cp500 (clause UTF-8) : code non nul, CHAQUE
     fichier posé nommé dans le refus avec sa raison, 0 fichier écrit au public ; ④ un emplacement de code qui est
     un dossier lié hors du dépôt : refusé, rien écrit ; ⑤ le mot « github_pat_ » seul, le filtre sed du dépôt et
     « Basic ${B64} » : publiés.
  S122 à S136 et V6 (circuit des séries, 04-11-2026, numérotés le 05-11-2026) : le filet des gabarits publics du
  fabricant (`verifier_les_gabarits_publics` : actions permises, permissions en lecture, identités distinctes, résultat
  des parts lu, branches à soi, une seule forme permise de la poussée), chaque propriété sabotée séparément ; le
  fabricant doit refuser, pour la raison attendue.
  E9 (05-11-2026, décision de Jean-Luc à 13h36, « 2 » : les séries éprouvent la version en attente AVANT sa fusion,
  depuis la branche publique du même nom) : le fabricant refuse d'écrire dans un clone public sur « main » quand le
  dépôt privé est sur « travail-essai », et écrit quand les deux sont sur « travail-essai » (`cas_de_branche`).
  S137 (E9 sans sa propriété) et S138 (« preparer » clone le privé sans « ref: » : le filet, propriété ⑦, refuse).
  Avant tout : deux sabotages au même numéro → code 2 (`numeros_en_double`).
  Avec --saboter, les cas « V… » sont des VARIANTES qui doivent rester vertes (le fabricant protège cette forme), les
  cas « S… » doivent rougir ; un cas de MOTIFS_ATTENDUS doit rougir POUR CETTE RAISON-LÀ (le motif se lit dans le
  détail), sinon il compte comme un sabotage sans effet.
⑦ UNITÉ — —
⑧ POURQUOI — Décision de Jean-Luc du 08-10-2026 (A-543 : « Non pas question de prendre ces risques ») : un dépôt
  public ne doit pas exécuter le code du dépôt privé. Décision du 12-10-2026 à 16h46 (« Oui, construire ») et
  ordre du 15-10-2026 à 08h36 (A-580, A-576) : la certification passe au dépôt public en y publiant tout le code
  qu'elle exécute. Ce qui garantit qu'aucun code privé ne tourne au public, ce sont deux choses : le fabricant
  publie TOUS les fichiers de code, et les pas « poser » refusent tout écart, dans les deux sens. Une épreuve qui
  reste verte quand on retire ce qu'elle teste n'est pas une preuve (R-731).
⑨ CE QUI CLOCHE — E4 et E5 exécutent le texte des pas extrait du YAML, pas le circuit sur une machine de GitHub :
  les actions de clonage (actions/checkout) ne sont pas jouées. Le passage réel reste à faire, à la main, après
  la publication (A-576 ③).
⑩ EFFET — Écrit dans des dossiers jetables, effacés à la fin ; lance des processus.
⑪ TERMINAISON — Rend la main ; chaque processus est borné (120 secondes pour le fabricant, 60 pour un pas).
  [sort: oui]
"""
import ast
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import warnings

try:
    import yaml
except ImportError:
    print("ARRÊT : le module yaml (PyYAML) manque")
    sys.exit(2)

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
FAB = "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"
CIRC = ".github/workflows/collecte_abc.yml"
CERT = ".github/workflows/certifier_la_version.yml"
# La certification PRIVÉE : ses « pip install » sont ce que la certification publique doit installer (E6 bis).
CERT_PRIVE = ".github/workflows/certifier.yml"
# LA PROPRIÉTÉ DES PAS QUI TOURNENT APRÈS UN ÉCHEC, IMPORTÉE DU FABRICANT DU DÉPÔT ÉPROUVÉ (jamais celui de la copie
# sabotée) : un sabotage qui affaiblit la propriété du fabricant est ainsi jugé par la propriété livrée (S48).
import importlib.util as _iu
_spec = _iu.spec_from_file_location("fabricant_de_l_epreuve", os.path.join(DEPOT, FAB))
PROPRIETE = _iu.module_from_spec(_spec)
_spec.loader.exec_module(PROPRIETE)
# LE MODULE DE LA FORME D'UN JETON, à côté du fabricant, sous le nom que le fabricant lui donne (jamais épelé ici).
MOD = os.path.dirname(FAB) + "/" + PROPRIETE.MODULE_DU_JETON
# J5 et « Dire quels pas… » du circuit privé : les ancres des formes éprouvées.
_J5 = "        if: always() && steps.versement.outputs.a_part == '1'\n"
_DIRE = "        if: always()\n        env:\n"
# Le fabricant SANS sa transformation et SANS sa post-condition : ce qu'il publie alors, seule E3 bis peut le juger.
_SANS_PROTECTION = [(FAB, "    corps = proteger_les_pas(corps)\n", "    corps = corps\n"),
                    (FAB, '    verifier_les_pas("\\n".join(lignes))\n', "    pass\n")]
# LES FORMES HORS DU SOUS-ENSEMBLE YAML LU PAR LE FABRICANT (superviseur R-759, second tour, R3 ; relecteur, I1 et M6) :
# YAML — donc GitHub — lit chacune comme une condition, ou comme une valeur qui peut en devenir une ; le fabricant doit
# les REFUSER. Nom → (remplacements dans le circuit privé, motif du refus). Écrites une fois, servies à deux usages : un
# sabotage par forme (le vrai fichier privé la porte : le fabricant doit rougir sur le motif) et E3 quinquies (le
# fabricant de la copie refuse chaque forme : c'est ce qui fait rougir S60, où le refus est remplacé par un saut).
_ROUGIR = "      - name: Rougir si des lignes de cours ont ete mises a part\n"
_TENIR = '        run: python3 programmes/TENIR_LES_POSITIONS.py "$GITHUB_WORKSPACE"\n'
# Les numéros des sabotages tirés des formes : S51 à S59 pour les neuf premières (tour 2), S62 et suivants ensuite
# (S60 et S61 sont pris).
_NUMERO = lambda k: 51 + k if k < 9 else 53 + k
FORMES_HORS_SOUS_ENSEMBLE = {
    "cle_entre_guillemets": ([(CIRC, _J5, "        \"if\": always() && steps.versement.outputs.a_part == '1'\n")], "ni « clé: valeur »"),
    "cle_entre_apostrophes": ([(CIRC, _J5, "        'if': always() && steps.versement.outputs.a_part == '1'\n")], "ni « clé: valeur »"),
    "cle_complexe": ([(CIRC, _J5, "        ? if\n        : always() && steps.versement.outputs.a_part == '1'\n")], "ni « clé: valeur »"),
    "alias": ([(CIRC, _J5, "        if: *c\n")], "indicateur YAML"),
    # Motif propre (relecteur du tour 2, I1) : la ligne de l'ANCRE, refusée parce que le texte privé ENTIER passe la
    # liste blanche ; sans cela, c'est l'alias de la ligne de J5 qui serait refusé, avec le même motif générique.
    "ancre_dans_on": ([(CIRC, "  group: circuit-du-soir\n", "  group: &c always()\n"), (CIRC, _J5, "        if: *c\n")],
                      "« group: &c always() »"),
    "etiquette": ([(CIRC, _J5, "        if: !!str always() && steps.versement.outputs.a_part == '1'\n")], "indicateur YAML"),
    "style_en_ligne": ([(CIRC, _ROUGIR, "      - {name: x, id: x, if: always(), run: echo x}\n" + _ROUGIR)], "indicateur YAML"),
    "tabulation": ([(CIRC, _J5, "        if:\talways() && steps.versement.outputs.a_part == '1'\n")], "U+0009"),
    "cle_en_majuscule": ([(CIRC, _J5, "        If: always() && steps.versement.outputs.a_part == '1'\n")], "autre casse"),
    # TROISIÈME TOUR (superviseur R-759, ③1 à ③4 ; relecteur du tour 2, B1 et I1). PyYAML lit U+2028 et U+0085 comme des
    # fins de ligne : derrière eux, une clé du pas (`shell:` — même trou hors de `if:` — ou `if:`) échappait au découpage
    # par « \n ». Refusés par leur catégorie Unicode, dans tout le texte.
    "u2028_puis_shell": ([(CIRC, _TENIR, _TENIR.rstrip("\n") + "\u2028        shell: bash\n")], "U+2028"),
    "u0085_puis_if": ([(CIRC, _TENIR, _TENIR.rstrip("\n") + "\x85        if: failure()\n")], "U+0085"),
    # Une chaîne laissée ouverte se continue, même moins indentée : « z: | » y ouvrirait un faux bloc qui cacherait le
    # « if: » qui suit (relecteur, B1(b)).
    "chaine_ouverte_faux_bloc": ([(CIRC, "      - name: Tenir les positions\n",
                                   '      - name: "Tenir les positions\n      z: |\n          fin"\n        if: always()\n')],
                                 "non fermée sur sa ligne"),
    # Le refus d'un élément de liste entre guillemets n'était éprouvé nulle part (relecteur, I1).
    "element_de_liste_entre_guillemets": ([(CIRC, _ROUGIR, '      - "if": always()\n' + _ROUGIR)],
                                          "élément de liste entre guillemets"),
}
_COMPOSITION_CASSEE = (FAB, "f\"if: ${{{{ always() && steps.{PAS_POSE}.outcome == 'success' && ({x}) }}}}\"", "f\"if: ${{{{ {x} }}}}\"")
SOIR = ".github/workflows/circuit_du_soir.yml"
SABOTAGES = {
    "Z0": [],
    "S1_certif_sans_controle_absent_du_public": [(FAB,
        '              [ -f "_code/$d/$n" ] || D="$D $d/$n(absent-du-public)"\n', '              true\n')],
    "S2_certif_sans_controle_absent_du_prive": [(FAB,
        'if [ ! -f "$d/$n" ]; then D="$D $d/$n(absent-du-prive)"; elif ! cmp',
        'if false; then true; elif [ -f "$d/$n" ] && ! cmp')],
    "S3_epreuves_non_publiees": [(FAB, 'DOSSIERS_DE_CODE = ("", "programmes", "tests", "etudes/outils", "tests/outils")',
                                  'DOSSIERS_DE_CODE = ("", "programmes", "etudes/outils", "tests/outils")')],
    "S9_outils_non_publies": [(FAB, 'DOSSIERS_DE_CODE = ("", "programmes", "tests", "etudes/outils", "tests/outils")',
                               'DOSSIERS_DE_CODE = ("", "programmes", "tests", "tests/outils")')],
    "S10_racine_non_publiee": [(FAB, 'DOSSIERS_DE_CODE = ("", "programmes", "tests", "etudes/outils", "tests/outils")',
                                'DOSSIERS_DE_CODE = ("programmes", "tests", "etudes/outils", "tests/outils")')],
    # tests/outils/ (décision de Jean-Luc du 01-11-2026 à 13h39) : retiré de la liste, ses programmes n'arrivent plus
    # au public (E1) ; la boucle et le motif tirés d'une autre liste que celle qui publie (une seconde définition) :
    # le pas efface ce que le fabricant publie (E4). Le motif d'effacement seul, épelé sans tests/outils, n'est PAS un
    # défaut : la boucle de copie qui suit remet ce qu'il efface, après la comparaison (mesuré le 01-11-2026, ce
    # sabotage restait vert) ; il n'est donc pas joué.
    "S96_outils_d_epreuves_non_publies": [(FAB, 'DOSSIERS_DE_CODE = ("", "programmes", "tests", "etudes/outils", "tests/outils")',
                                           'DOSSIERS_DE_CODE = ("", "programmes", "tests", "etudes/outils")')],
    "S97_pas_poser_d_une_autre_liste": [(FAB, "BOUCLE_DU_CODE, MOTIF_DU_CODE = pour_le_pas_poser(DOSSIERS_DE_CODE)\n",
                                         "BOUCLE_DU_CODE, MOTIF_DU_CODE = pour_le_pas_poser(DOSSIERS_DE_CODE[:-1])\n")],
    # ancre déplacée le 01-11-2026 : le motif est tiré de DOSSIERS_DE_CODE, la fin de ligne reste
    "S11_code_prive_non_efface": [(FAB, "\"\"\"' | xargs -0 -r rm -f\n", "\"\"\"' | xargs -0 -r true\n")],
    "S12_liens_admis": [(FAB, '          [ -z "$L" ] || D="$D liens-symboliques:$L"\n', '')],
    "S14_code_compile_non_efface": [(FAB, '''grep -zE "($X)$" | xargs -0 -r rm -f''', '''grep -zE "($X)$" | xargs -0 -r true''')],
    "S15_fichiers_caches_non_vus": [(FAB, "            done < <(find \"$d\" -maxdepth 1 -name '*.py' -type f -print0)",
                                     "            done < <(find \"$d\" -maxdepth 1 -name '[!.]*.py' -type f -print0)")],
    # S16 réécrit le 30-10-2026 : « if: steps.certifier.outcome != 'success' » seul garde le success() implicite de
    # GitHub et ne tourne pas sur un code non posé (superviseur R-759, ②) ; le défaut est de garder « !cancelled() »
    # en retirant l'exigence du code posé.
    "S16_verdict_sur_code_non_pose": [(FAB, "        if: ${{ !cancelled() && steps.poser_le_code.outcome == 'success' && steps.certifier.outcome != 'success' }}",
                                       "        if: ${{ !cancelled() && steps.certifier.outcome != 'success' }}")],
    # S17 réécrit le 30-10-2026 (superviseur R-759) : l'ancienne ancre, la chaîne exacte remplacée, n'existe plus.
    "S17_pas_final_sur_code_non_pose": _SANS_PROTECTION,
    # UNE FORME PAR CAS (superviseur R-759 du 30-10-2026, ②5). « V… » : le fabricant la protège, tout reste vert.
    # « S… » : la même forme, fabricant sans protection ni post-condition : E3 bis doit rougir.
    "V1_prive_failure": [(CIRC, _J5, "        if: failure()\n")],
    "S37_prive_failure_non_protege": _SANS_PROTECTION + [(CIRC, _J5, "        if: failure()\n")],
    "V2_prive_success_ou": [(CIRC, _J5, "        if: success() || steps.versement.outputs.a_part == '1'\n")],
    "S38_prive_success_ou_non_protege": _SANS_PROTECTION + [(CIRC, _J5, "        if: success() || steps.versement.outputs.a_part == '1'\n")],
    "V3_prive_always_enveloppe": [(CIRC, _DIRE, "        if: ${{ always() }}\n        env:\n")],
    "S39_prive_always_enveloppe_non_protege": _SANS_PROTECTION + [(CIRC, _DIRE, "        if: ${{ always() }}\n        env:\n")],
    "V4_prive_non_annule_enveloppe": [(CIRC, _J5, "        if: ${{ !cancelled() && steps.versement.outputs.a_part == '1' }}\n")],
    "S40_prive_non_annule_non_protege": _SANS_PROTECTION + [(CIRC, _J5, "        if: ${{ !cancelled() && steps.versement.outputs.a_part == '1' }}\n")],
    # V5 et S41 enveloppés depuis le second tour : « if: ! … » nu est une ÉTIQUETTE pour YAML, refusée par la liste blanche.
    "V5_prive_espaces_et_majuscules": [(CIRC, _J5, "        if: ${{ ! Cancelled ( ) && steps.versement.outputs.a_part == '1' }}\n")],
    "S41_prive_espaces_et_majuscules_non_protege": _SANS_PROTECTION + [(CIRC, _J5, "        if: ${{ ! Cancelled ( ) && steps.versement.outputs.a_part == '1' }}\n")],
    # LES FORMES NON PRISES EN CHARGE : le fabricant doit REFUSER, jamais publier en silence (motif dans MOTIFS_ATTENDUS).
    "S42_prive_condition_entre_guillemets": [(CIRC, _J5, "        if: \"always() && steps.versement.outputs.a_part == '1'\"\n")],
    "S43_prive_condition_en_bloc": [(CIRC, _J5, "        if: >-\n          always() &&\n          steps.versement.outputs.a_part == '1'\n")],
    "S44_prive_condition_sur_deux_lignes": [(CIRC, _J5, "        if: always() &&\n          steps.versement.outputs.a_part == '1'\n")],
    "S45_prive_if_de_job": [(CIRC, "    runs-on: ubuntu-latest\n", "    runs-on: ubuntu-latest\n    if: ${{ !cancelled() }}\n")],
    "S46_prive_condition_commentee": [(CIRC, _J5, "        if: always() && steps.versement.outputs.a_part == '1' # x\n")],
    "S47_prive_if_a_une_autre_colonne": [(CIRC, "        env:\n          PAS:", "        env:\n          if: always()\n          PAS:")],
    # LA POST-CONDITION : une composition cassée est arrêtée par elle (S49) ; sans elle, E3 bis la voit (S50).
    "S49_composition_cassee": [_COMPOSITION_CASSEE],
    "S50_composition_cassee_sans_post_condition": [_COMPOSITION_CASSEE, _SANS_PROTECTION[1]],
    # LA PROPRIÉTÉ DU FABRICANT AFFAIBLIE (failure() oublié) : la transformation ET la post-condition sont trompées ;
    # E3 bis, qui juge avec la propriété du dépôt éprouvé, ne l'est pas.
    # LA LISTE BLANCHE (R3) : le fabricant qui SAUTE une ligne incomprise au lieu de la refuser — la cause d'I1. Les
    # formes refusées par cette branche passent alors ; E3 quinquies le voit.
    "S60_ligne_incomprise_sautee": [(FAB, '                raise ValueError(f"{HORS_DU_SOUS_ENSEMBLE} : ligne ni « clé: valeur » ni « - scalaire » ({ou})")\n',
                                     "                continue\n")],
    # M1 du relecteur : E3 bis est le SEUL garde du job de décision (la post-condition ne le couvre pas).
    "S61_decision_sur_code_non_pose": [(FAB, "        id: decision\n        run: |\n", "        id: decision\n        if: always()\n        run: |\n")],
    "S48_propriete_affaiblie": [(FAB, "(?:always|failure|cancelled|success)", "(?:always|cancelled|success)"),
                                (CIRC, _J5, "        if: failure()\n")],
    "S18_fiches_non_comparees": [(FAB, '''elif ! cmp -s "$f" ".github/workflows/$n"; then D="$D fiche:$n"; fi''',
                                  '''else true; fi''')],
    "S19_fiches_non_publiees": [(FAB, "    d = os.path.join(prive, FICHES_PRIVEES)\n    if not os.path.isdir(d):\n        return []\n",
                                 "    return []\n")],
    # la boucle est tirée de DOSSIERS_DE_CODE depuis le 01-11-2026 : le sabotage ôte « . » de ce qu'elle reçoit
    "S13_racine_non_comparee": [(FAB, '          for d in """ + BOUCLE_DU_CODE + """; do\n            while IFS',
                                 '          for d in """ + BOUCLE_DU_CODE.replace(". ", "", 1) + """; do\n            while IFS')],
    "S4_rien_n_est_retire": [(FAB, "        os.remove(os.path.join(public, f))\n", "        pass\n")],
    "S5_soir_sans_controle_absent_du_public": [(FAB,
        '            [ -f "_code/programmes/$n" ] || D="$D $n(absent-du-public)"\n', '            true\n')],
    "S6_lancement_non_compare": [(FAB,
        '          cmp -s _code/tests/LANCEMENT_DES_EPREUVES.json tests/LANCEMENT_DES_EPREUVES.json || D="$D tests/LANCEMENT_DES_EPREUVES.json"\n', '')],
    "S7_declenchement_sur_proposition": [(FAB, "  workflow_dispatch:\n  # 21h00", "  workflow_dispatch:\n  pull_request:\n  # 21h00")],
    "S8_donnees_des_epreuves_publiees": [(FAB, 'if f.endswith(".py") and os.path.isfile(os.path.join(d, f))]',
                                          'if os.path.isfile(os.path.join(d, f))]')],
    "S20_sans_lecteur_de_doc": [(FAB, "          command -v soffice >/dev/null || command -v libreoffice >/dev/null || { sudo apt-get update -qq && sudo apt-get install -y -qq --no-install-recommends libreoffice-writer-nogui; }\n", "")],
    "S21_sans_lecteur_de_pdf": [(FAB, "          command -v pdftotext >/dev/null || { sudo apt-get update -qq && sudo apt-get install -y -qq poppler-utils; }\n", "")],
    "S22_logiciel_par_une_variable": [("programmes/COMMUN.py", "\nimport csv\n", "\nimport csv\nimport shutil as _sh_e6\n_x_e6 = 'gs'\n_sh_e6.which(_x_e6)\n")],
    "S23_logiciel_ecrit_autrement": [("programmes/COMMUN.py", "\nimport csv\n", "\nimport csv\nfrom shutil import which as which\nwhich( 'convert' )\n")],
    "S24_soir_sous_dossiers_admis": [(FAB, '          for x in programmes/*; do [ -d "$x" ] && D="$D $x(dossier)"; done\n', '')],
    "S25_soir_compiles_admis": [(FAB, "\\\\( -name '*.pyc' -o -name '*.so' -o -name '*.pyd' \\\\) -print); do D=\"$D $x(compile)\"; done\n",
                                 "\\\\( -name '*.pyc' -o -name '*.so' -o -name '*.pyd' \\\\) -print); do true; done\n")],
    "S26_garde_non_pose": [(FAB, '          cp _code/programmes/N_EXECUTER_AU_PUBLIC_QUE_LE_CODE_PUBLIE.py "$RUNNER_TEMP/garde/sitecustomize.py"\n', '')],
    "S27_environnement_du_garde_non_ecrit": [(FAB, '{ echo "PYTHONPATH=$RUNNER_TEMP/garde"; ', '{ ')],
    "S28_garde_qui_ne_mord_pas_accepte": [(FAB, '[ "$c" -eq 97 ] ||', 'true ||')],
    "S29_garde_sans_comparaison": [("programmes/N_EXECUTER_AU_PUBLIC_QUE_LE_CODE_PUBLIE.py", "        if not pareil:\n            refuser(quoi, rel)\n", "        pass\n")],
    "S31_garde_porte_exec_morte": [("programmes/N_EXECUTER_AU_PUBLIC_QUE_LE_CODE_PUBLIE.py", '        if evenement == "exec":\n', '        if False:\n')],
    "S33_garde_porte_popen_morte": [("programmes/N_EXECUTER_AU_PUBLIC_QUE_LE_CODE_PUBLIE.py", '        elif evenement == "subprocess.Popen":\n', '        elif False:\n')],
    "S34_garde_porte_pyc_morte": [("programmes/N_EXECUTER_AU_PUBLIC_QUE_LE_CODE_PUBLIE.py", '        elif evenement == "open" and arguments', '        elif False and arguments')],
    "S35_garde_qui_refuse_tout": [("programmes/N_EXECUTER_AU_PUBLIC_QUE_LE_CODE_PUBLIE.py", "        if not pareil:\n            refuser(quoi, rel)\n", "        refuser(quoi, rel)\n")],
    "S36_pas_du_garde_revenu_au_lancement": [(FAB, '          c=0; python3 -c "import sys; sys.path.insert(0, \'.\'); import _piege_du_garde" || c=$?\n', '          c=0; python3 _piege_du_garde.py || c=$?\n')],
    "S30_code_laisse_dans_le_clone": [(FAB, 'rm -rf "$RUNNER_TEMP/code" && mv _code "$RUNNER_TEMP/code"', 'cp -r _code "$RUNNER_TEMP/code"')],
    # E6 bis (reprise de la version A après la relecture de Cowork du 31-10-2026, 18h49). Numérotés à 90 : les formes
    # ci-dessous prennent S62 et la suite.
    "S90_paquet_du_prive_non_installe": [(FAB, ' "pyflakes==4.1.0" cryptography pyyaml\n"""', ' cryptography pyyaml\n"""')],
    "S91_version_du_paquet_perdue": [(FAB, ' "pyflakes==4.1.0" cryptography pyyaml\n"""', ' "pyflakes" cryptography pyyaml\n"""')],
    "S92_aucun_paquet_lu_au_prive": [(CERT_PRIVE, "        run: python3 -m pip install --quiet", "        run: python3 -m pip list --quiet")],
    # Relecture neuve du 31-10-2026, M2 (ses cas I3, I4, I6, qui restaient verts).
    "S93_installation_desactivee": [(FAB, "        id: installer\n        run: python3 -m pip install", "        id: installer\n        if: ${{ false }}\n        run: python3 -m pip install")],
    "S94_installation_qui_peut_echouer": [(FAB, "        id: installer\n        run: python3 -m pip install", "        id: installer\n        continue-on-error: true\n        run: python3 -m pip install")],
    # M5 (relecture de Cowork du 04-11-2026 à 21h17, I1) : chaque garde de `refus_avant_publication` et son appel,
    # retirés un à un. Tour 2 (superviseur R-759 du 05-11-2026 à 00h52) : le motif vit dans programmes/FORME_D_UN_JETON.py
    # (MOD) ; chaque branche y est RETIRÉE (le cas positif de CAS_DU_MOTIF correspondant doit rougir) et ÉLARGIE (le cas
    # négatif correspondant doit rougir), le motif attendu NOMME le cas ; S112 à S115 sont les mutations G1 à G4 de la
    # relecture neuve du 04-11-2026 (D2), qui laissaient E8 vert ; S116 et S117 retirent les refus du lien dur (D4) et du
    # non-UTF-8 (D5) ; S118 compile un motif de jeton hors du module ; S119 retire l'appel au module. Tour 3 (superviseur
    # R-759 du 05-11-2026 à 03h10, D1 et D4) : S117 retire la seule clause UTF-8 du texte strict (le cas cp500 doit
    # rougir), S120 la seule clause des contrôles (le cas UTF-16-LE sans BOM doit rougir), S121 remet « \b » devant
    # « gh » (le cas « X_ghp_… » doit rougir).
    "S98_garde_m5_retiree": [(FAB, '        refus = refus_avant_publication(prive, a_publier + [FICHES_PRIVEES.replace(os.sep, "/") + "/" + f for f in fiches])\n', "        refus = []\n")],
    "S99_fiches_hors_de_la_garde_m5": [(FAB, '        refus = refus_avant_publication(prive, a_publier + [FICHES_PRIVEES.replace(os.sep, "/") + "/" + f for f in fiches])\n', "        refus = refus_avant_publication(prive, a_publier)\n")],
    "S100_liens_suivis_par_le_fabricant": [(FAB, "        if os.path.islink(p):\n", "        if False:\n"),
                                           (FAB, "        reel = os.path.realpath(p)\n",
                                            "        reel = os.path.normpath(os.path.join(racine, rel))\n")],
    "S101_dossier_lie_admis": [(FAB, "        reel = os.path.realpath(p)\n",
                                "        reel = os.path.normpath(os.path.join(racine, rel))\n")],
    "S102_jeton_github_non_cherche": [(MOD, 'rb"github_pat_\\w{20,}|', 'rb"')],
    "S103_en_tete_basic_non_cherche": [(MOD, '|authorization:[ \\t]*basic[ \\t]+[A-Za-z0-9+/=]{8,}"', '"')],
    "S104_motif_github_trop_large": [(MOD, 'rb"github_pat_\\w{20,}|', 'rb"github_pat_\\w{0,}|')],
    "S105_motif_basic_trop_large": [(MOD, '[A-Za-z0-9+/=]{8,}"', '[A-Za-z0-9+/=]{0,}"')],
    "S106_ecrit_avant_de_refuser": [(FAB, "    fiches = fiches_a_publier(prive)\n    try:\n",
                                     "    fiches = fiches_a_publier(prive)\n    os.makedirs(os.path.join(public, \"programmes\"), exist_ok=True)\n"
                                     "    shutil.copyfile(os.path.join(prive, a_publier[0]), os.path.join(public, a_publier[0]))\n    try:\n")],
    "S107_jetons_gh_non_cherches": [(MOD, '|(?<![A-Za-z0-9])gh[pousr]_[A-Za-z0-9]{20,}|', '|')],
    "S108_motif_gh_trop_large": [(MOD, '[pousr]_[A-Za-z0-9]{20,}|', '[pousr]_[A-Za-z0-9]{0,}|')],
    "S109_adresse_a_identifiants_non_cherchee": [(MOD, '|https?://[^/\\s:@]+:[^/\\s@]+@|', '|')],
    "S110_motif_adresse_trop_large": [(MOD, ':[^/\\s@]+@|', ':[^/@]+@|')],
    "S111_majuscules_non_cherchees": [(MOD, '{8,}", re.IGNORECASE)', '{8,}")')],
    "S112_G1_lecture_des_4096_premiers_octets": [(FAB, "                octets = e.read()\n", "                octets = e.read(4096)\n")],
    "S113_G2_racine_hors_de_la_garde": [(FAB, "    for rel in chemins:\n        p = os.path.join(prive, rel)\n",
                                         "    for rel in [c for c in chemins if \"/\" in c]:\n        p = os.path.join(prive, rel)\n")],
    "S114_G3_json_hors_du_motif": [(FAB, "            if forme.porte_une_forme_de_jeton(octets):\n",
                                    "            if not rel.endswith(\".json\") and forme.porte_une_forme_de_jeton(octets):\n")],
    "S115_G4_tests_racine_hors_de_la_garde": [(FAB, "    for rel in chemins:\n        p = os.path.join(prive, rel)\n",
                                               "    for rel in [c for c in chemins if not (c.startswith(\"tests/\") and c.count(\"/\") == 1)]:\n"
                                               "        p = os.path.join(prive, rel)\n")],
    "S116_lien_dur_admis": [(FAB, "        elif os.stat(p).st_nlink > 1:\n", "        elif False:\n")],
    "S117_non_utf8_admis": [(FAB, "                texte = octets.decode(\"utf-8\")\n",
                             "                texte = octets.decode(\"utf-8\", \"replace\")\n")],
    "S118_motif_compile_hors_du_module": [(FAB, 'MODULE_DU_JETON = "FORME_D_UN_JETON.py"\n',
                                           'MODULE_DU_JETON = "FORME_D_UN_JETON.py"\n_AUTRE = re.compile(rb"\\bghp_[A-Za-z0-9]{20,}")\n')],
    "S119_module_non_appele": [(FAB, "            if forme.porte_une_forme_de_jeton(octets):\n", "            if False:\n")],
    "S120_controles_admis": [(FAB, "            if controle is not None:\n", "            if False:\n")],
    "S121_borne_gh_remise_a_b": [(MOD, '(?<![A-Za-z0-9])gh[pousr]_', '\\bgh[pousr]_')],
    # Ancre sans le paquet qui suit coverage : numpy y a été inséré le 08-11-2026 (bloc 3, cas E7 de la lecture de la fiche).
    "S95_installation_en_echo": [(FAB, "        run: python3 -m pip install --quiet \"coverage==7.16.2\"", "        run: echo pip install --quiet \"coverage==7.16.2\"")],
    # LE FILET DES GABARITS PUBLICS (circuit des séries, 04-11-2026, superviseur R-759, R3 ; tour 4, R2 : les poussées
    # hors de la forme permise) : chaque propriété de `verifier_les_gabarits_publics` sabotée SÉPARÉMENT ; la variante
    # renomme la garde des parts et doit rester verte (le filet lit une propriété, pas un nom). Numéros S122 à S136 et V6
    # pris par programme au premier libre le 05-11-2026 (la réparation M5 avait pris S100 à S121).
    'S122_series_sans_garde_des_parts': [(FAB, '      - name: Toutes les parts sont-elles vertes ?\n        id: parts_vertes\n        shell: bash\n        env:\n          JOUER: ${{ needs.jouer.result }}\n        run: |\n          [ "$JOUER" = "success" ] || { echo "::error::une part au moins n\'est pas verte ($JOUER) : rien n\'est rassemble, aucun releve"; exit 1; }\n', '')],
    'S123_series_identite_de_la_certification': [(FAB, 'SERIES_IDENTITE = "series-longues-publiques"', 'SERIES_IDENTITE = "certification-publique"')],
    'S124_series_archive_jointe': [(FAB, '          exit "$code"\n%(deposer_final)s"""', '          exit "$code"\n      - uses: actions/upload-artifact@v4\n        with:\n          path: rapports/series_longues\n%(deposer_final)s"""')],
    'S125_series_contents_write': [(FAB, 'permissions:\n  contents: read\njobs:\n  preparer:', 'permissions:\n  contents: write\njobs:\n  preparer:')],
    'S126_series_pousse_sur_main': [(FAB, 'branche=SERIES_BRANCHES + "${GITHUB_RUN_ID}/${SERIE}/releve",', 'branche="main",')],
    'S127_series_branches_travail': [(FAB, 'SERIES_BRANCHES = "series-longues/"', 'SERIES_BRANCHES = "travail-series/"')],
    'S128_certification_identite_du_soir': [(FAB, 'auteur="certification-publique", message=', 'auteur="circuit-public", message=')],
    'S129_series_permission_en_ligne': [(FAB, 'permissions:\n  contents: read\njobs:\n  preparer:', 'permissions: write-all\njobs:\n  preparer:')],
    'S130_series_permission_de_job': [(FAB, '  jouer:\n    needs: preparer\n', '  jouer:\n    needs: preparer\n    permissions: write-all\n')],
    'S131_M1_sa_branche_et_main': [(FAB, 'branche=SERIES_BRANCHES + "${GITHUB_RUN_ID}/${SERIE}/part_${PART}",', 'branche=SERIES_BRANCHES + "${GITHUB_RUN_ID}/${SERIE}/part_${PART}\\" \\"HEAD:refs/heads/main",')],
    'S132_N1_cible_courte_main': [(FAB, 'branche=SERIES_BRANCHES + "${GITHUB_RUN_ID}/${SERIE}/part_${PART}",', 'branche=SERIES_BRANCHES + "${GITHUB_RUN_ID}/${SERIE}/part_${PART}\\" \\"HEAD:main",')],
    'S133_N2_seconde_cible_ligne_suivante': [(FAB, 'branche=SERIES_BRANCHES + "${GITHUB_RUN_ID}/${SERIE}/part_${PART}",', 'branche=SERIES_BRANCHES + "${GITHUB_RUN_ID}/${SERIE}/part_${PART}\\" \\\\\\n            \\"HEAD:main",')],
    'S134_N3_git_c_push_vers_main': [(FAB, 'git push -q origin "HEAD:refs/heads/""" + branche + """" \\\\', 'git -c x.y=1 push -q origin "HEAD:refs/heads/main" \\\\')],
    'S135_N4_force': [(FAB, 'git push -q origin "HEAD:refs/heads/"""', 'git push -q --force origin "HEAD:refs/heads/"""')],
    'S136_N5_plus_refspec': [(FAB, 'git push -q origin "HEAD:refs/heads/"""', 'git push -q origin "+HEAD:refs/heads/"""')],
    # LA VERSION EN ATTENTE (décision de Jean-Luc du 05-11-2026 à 13h36, « 2 ») : la branche du clone public non
    # comparée à celle du privé (E9), et le clonage de la version demandée sans « ref: » (filet, propriété ⑦).
    'S137_branche_publique_non_comparee': [(FAB, '        refus = refus_de_branche(prive, public)\n', '        refus = None\n')],
    # Ancre reprise le 08-11-2026 (bloc 3) : le bloc 2 (e50dd73c) a ajouté « aussi=… » après ce « ref: », et l'ancienne
    # ancre « ref=…), » n'existait plus (INAPPLICABLE, code 2).
    'S138_series_preparation_sans_version': [(FAB, 'apres_le_clonage=SERIES_VERSION, ref="${{ inputs.version }}",', 'apres_le_clonage=SERIES_VERSION,')],
    'V6_series_garde_renommee': [(FAB, '      - name: Toutes les parts sont-elles vertes ?\n        id: parts_vertes\n', '      - name: Les parts ont-elles toutes reussi ?\n        id: verifier_les_parts\n')],
}
for _k, (_n, (_r, _m)) in enumerate(FORMES_HORS_SOUS_ENSEMBLE.items()):
    SABOTAGES[f"S{_NUMERO(_k)}_prive_{_n}"] = _r
# LA RAISON DU ROUGE, pour les cas où un rouge pour une autre raison ne prouverait rien : le texte doit se lire dans le
# détail. Exemple : sans le motif, S49 resterait « rouge » même si la post-condition était retirée (E3 bis rougirait
# à sa place) — c'est le motif qui donne des dents à la post-condition.
MOTIFS_ATTENDUS = {
    "S16_verdict_sur_code_non_pose": "E3 certification",
    "S17_pas_final_sur_code_non_pose": "E3 soir",
    "S37_prive_failure_non_protege": "E3 soir",
    "S38_prive_success_ou_non_protege": "E3 soir",
    "S39_prive_always_enveloppe_non_protege": "E3 soir",
    "S40_prive_non_annule_non_protege": "E3 soir",
    "S41_prive_espaces_et_majuscules_non_protege": "E3 soir",
    "S42_prive_condition_entre_guillemets": "entre guillemets",
    "S43_prive_condition_en_bloc": "en bloc",
    "S44_prive_condition_sur_deux_lignes": "continuée sur la ligne suivante",
    "S45_prive_if_de_job": "if: » de job",
    "S46_prive_condition_commentee": "suivie d'un commentaire",
    "S47_prive_if_a_une_autre_colonne": "à la colonne 10",
    "S48_propriete_affaiblie": "E3 soir",
    "S49_composition_cassee": "POST-CONDITION",
    "S50_composition_cassee_sans_post_condition": "E3 soir",
    "S60_ligne_incomprise_sautee": "E3 quinquies",
    "S61_decision_sur_code_non_pose": "« decision » du job « faut_il_tourner »",
    "S90_paquet_du_prive_non_installe": "E6 bis paquet de la certification privée non installé au public : pyflakes==4.1.0",
    "S91_version_du_paquet_perdue": "E6 bis paquet de la certification privée non installé au public : pyflakes==4.1.0",
    "S92_aucun_paquet_lu_au_prive": "E6 bis aucun paquet installé lu",
    "S93_installation_desactivee": "E6 bis le pas qui installe",
    "S94_installation_qui_peut_echouer": "E6 bis le pas qui installe",
    "S98_garde_m5_retiree": "E8 groupe à refuser : publié, fabricant au code 0",
    "S99_fiches_hors_de_la_garde_m5": "E8 non refusé : .github/workflows/lien_m5_hors.yml",
    "S100_liens_suivis_par_le_fabricant": "E8 non refusé : LIEN_M5_HORS.py",
    "S101_dossier_lie_admis": "E8 « emplacement lié hors du dépôt » : publié",
    "S102_jeton_github_non_cherche": "E8 motif : « jeton fin github_pat_ » non reconnu",
    "S103_en_tete_basic_non_cherche": "E8 motif : « en-tête Basic » non reconnu",
    "S104_motif_github_trop_large": "E8 motif : « le mot github_pat_ seul » refusé à tort",
    "S105_motif_basic_trop_large": "E8 motif : « Authorization: Basic ${B64} » refusé à tort",
    "S106_ecrit_avant_de_refuser": "écrit(s) au public avant le refus",
    "S107_jetons_gh_non_cherches": "E8 motif : « jeton classique ghp_ » non reconnu",
    "S108_motif_gh_trop_large": "E8 motif : « ghp_ suivi de 19 caractères » refusé à tort",
    "S109_adresse_a_identifiants_non_cherchee": "E8 motif : « adresse à identifiants » non reconnu",
    "S110_motif_adresse_trop_large": "E8 motif : « ${{ secrets.X }} dans une adresse » refusé à tort",
    "S111_majuscules_non_cherchees": "E8 motif : « majuscules » non reconnu",
    "S112_G1_lecture_des_4096_premiers_octets": "E8 non refusé : JETON_M5_LOIN.py",
    "S113_G2_racine_hors_de_la_garde": "E8 non refusé : LIEN_M5_HORS.py",
    "S114_G3_json_hors_du_motif": "E8 non refusé : tests/LANCEMENT_DES_EPREUVES.json",
    "S115_G4_tests_racine_hors_de_la_garde": "E8 non refusé : tests/LIEN_M5_HORS.py",
    "S116_lien_dur_admis": "E8 non refusé : programmes/DUR_M5.py",
    "S117_non_utf8_admis": "E8 non refusé : tests/outils/CP500_M5.py",
    "S118_motif_compile_hors_du_module": "E8 propriété : motif de jeton compilé hors de programmes/FORME_D_UN_JETON.py : programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py",
    "S119_module_non_appele": "E8 non refusé : JETON_M5_LOIN.py",
    "S120_controles_admis": "E8 non refusé : tests/outils/U16NB_M5.py",
    "S121_borne_gh_remise_a_b": "E8 motif : « jeton ghp_ collé derrière « _ » » non reconnu",
    "S95_installation_en_echo": "E6 bis paquet de la certification privée non installé au public : coverage==7.16.2",
    'S122_series_sans_garde_des_parts': 'sans lire needs.jouer.result',
    'S123_series_identite_de_la_certification': 'identité partagée',
    'S124_series_archive_jointe': 'action non permise « actions/upload-artifact@v4 »',
    'S125_series_contents_write': "permissions ['contents: write']",
    'S126_series_pousse_sur_main': 'une poussée hors de la forme permise',
    'S127_series_branches_travail': 'commencent par « travail- »',
    'S128_certification_identite_du_soir': 'identité partagée avec circuit du soir',
    'S129_series_permission_en_ligne': 'pas de « permissions: » au premier niveau',
    'S130_series_permission_de_job': '« permissions: write-all »',
    'S131_M1_sa_branche_et_main': 'une poussée hors de la forme permise',
    'S132_N1_cible_courte_main': 'une poussée hors de la forme permise',
    'S133_N2_seconde_cible_ligne_suivante': 'une poussée hors de la forme permise',
    'S134_N3_git_c_push_vers_main': 'une poussée hors de la forme permise',
    'S135_N4_force': 'une poussée hors de la forme permise',
    'S136_N5_plus_refspec': 'une poussée hors de la forme permise',
    'S137_branche_publique_non_comparee': 'E9 branche publique « main », privé « travail-essai »',
    'S138_series_preparation_sans_version': 'un clonage du dépôt privé sans « ref: »',
}
for _k, (_n, (_r, _m)) in enumerate(FORMES_HORS_SOUS_ENSEMBLE.items()):
    MOTIFS_ATTENDUS[f"S{_NUMERO(_k)}_prive_{_n}"] = _m
# LA CALIBRATION DE LA PROPRIÉTÉ (E3 ter) : (condition, pas qui pose le code, verdict attendu). Des cas qui doivent la
# satisfaire ET des cas qui doivent la violer (§4 : un motif se calibre sur un cas connu, et sur un cas qui doit échouer).
CALIBRATION = (
    ("always()", "poser_les_programmes", False),
    ("failure()", "poser_les_programmes", False),
    ("${{ !cancelled() }}", "poser_les_programmes", False),
    ("! Cancelled ( ) && steps.x.outputs.y == '1'", "poser_les_programmes", False),
    ("success() || steps.versement.outputs.a_part == '1'", "poser_les_programmes", False),
    ("failure() || steps.poser_les_programmes.outcome == 'success'", "poser_les_programmes", False),
    ("!(always() && steps.poser_les_programmes.outcome == 'success')", "poser_les_programmes", False),
    ("${{ always() && steps.poser_le_code.outcome == 'success' }}", "poser_les_programmes", False),
    ("${{ always() && steps.poser_les_programmes.outcome == 'success' && (failure()) }}", "poser_les_programmes", True),
    ("${{ always() && steps.poser_les_programmes.outcome == 'success' && (success() || x == '1') }}", "poser_les_programmes", True),
    ("${{ !cancelled() && steps.poser_le_code.outcome == 'success' && steps.certifier.outcome != 'success' }}", "poser_le_code", True),
    ("steps.collecte.outputs.code != '0'", "poser_les_programmes", True),
    ("steps.certifier.outcome != 'success'", "poser_le_code", True),
    ("steps.x.outputs.y == 'always()'", "poser_les_programmes", True),
    ("${{ always() }} && x", "poser_les_programmes", False),        # M2 : la branche « enveloppe partielle »
)


def pas(texte_yaml, job, ident):
    """Rend le texte du « run » du pas `ident` du job `job`, lu par yaml.

    ① RÔLE — Extraire le script d'un pas pour l'exécuter tel quel.
    ② CONTEXTE D'APPEL — `epreuve`, pour E4 et E5.
    ③ ENTRÉE — `texte_yaml` : le fichier de circuit · `job` : le nom du job · `ident` : l'id du pas.
    ④ CONDITIONS D'ENTRÉE — Le texte est du YAML valide.
    ⑤ SORTIE — UNE valeur : le script, ou None si le pas manque.
      [rend: 1]
    ⑥ TRAITEMENT — lire le YAML, chercher le pas par son id.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Lire par yaml et non par motif : le script éprouvé est celui que GitHub lirait.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    y = yaml.safe_load(texte_yaml)
    for p in y.get("jobs", {}).get(job, {}).get("steps", []):
        if p.get("id") == ident:
            return p.get("run")
    return None


# Une ligne qui INSTALLE : la commande en tête de ligne, espaces permis (relecture neuve du 31-10-2026, M2 : un
# « echo pip install … » ou un commentaire était lu comme une installation).
COMMANDE_PIP = re.compile(r"\s*(?:python3? -m )?pip3? install\b")


def paquets_installes(run):
    """Rend les paquets qu'installent les lignes « pip install » d'un texte de pas.

    ① RÔLE — Lire ce qu'un pas de circuit installe, pour confronter la certification publique à la privée (E6 bis).
    ② CONTEXTE D'APPEL — `epreuve`, pour E6 bis : une fois par pas du circuit privé .github/workflows/certifier.yml,
      une fois par pas du job « certifier » fabriqué placé avant le pas « certifier ».
    ③ ENTRÉE — `run` : le texte du « run » d'un pas, tel que yaml le rend (une chaîne, ou "" quand le pas n'en a pas).
    ④ CONDITIONS D'ENTRÉE — Chaque ligne qui porte « pip install » se découpe comme une ligne de commande (guillemets
      fermés) : sinon shlex lève ValueError, qui remonte.
    ⑤ SORTIE — UNE valeur : l'ensemble des mots qui suivent « pip install », options (« -… ») retirées, écrits tels
      quels, version comprise, pris sur les seules lignes qui COMMENCENT par la commande (`COMMANDE_PIP` : « pip »,
      « pip3 », « python3 -m pip » ; un « echo pip install … » ou un commentaire ne compte pas) — par exemple, pour la ligne réelle du privé du 31-10-2026,
      {"coverage==7.16.2", "pyflakes==4.1.0", "cryptography", "pyyaml"} ; vide si aucune ligne n'installe.
      [rend: 1]
    ⑥ TRAITEMENT — pour chaque ligne qui commence par la commande : découper ce qui suit « pip install », garder ce
      qui n'est pas une option.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Deux listes de paquets écrites à deux endroits divergent toujours (R-708) : le 31-10-2026, pyflakes
      était installé par la certification privée et pas par la publique (relecture de Cowork, 18h49).
    ⑨ CE QUI CLOCHE — La valeur d'une option (« -r fichier », « -c contraintes ») serait lue comme un paquet ; un
      paquet installé autrement (uv, apt, une commande précédée de « sudo » ou d'une variable) ne se voit pas ; une
      ligne continuée par « \\ » n'est lue que jusqu'à sa fin. Aucun des deux circuits ne le fait le 31-10-2026.
      E6 bis, qui appelle cette fonction, est un filet sur le TEXTE du circuit, pas une preuve que le paquet est
      installé quand les épreuves tournent : elle refuse un « if » ou un « continue-on-error » sur le pas qui installe,
      mais elle ne voit pas « pip install … || true » ni « pip install --target <ailleurs> … » (relecture neuve du
      31-10-2026, tour 3, N1 et N2 : tous deux restent verts). Que pyflakes soit là à l'exécution, c'est l'épreuve E12
      du barème qui l'observe, et le critère du premier lancement exige le barème vert.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    out = set()
    for ligne in str(run or "").splitlines():
        if COMMANDE_PIP.match(ligne):
            out |= {m for m in shlex.split(ligne.split("pip install", 1)[1]) if not m.startswith("-")}
    return out


def jouer(script, prep):
    """Fabrique un espace de travail, y applique `prep`, exécute `script` par bash -e ; rend le code.

    ① RÔLE — Exécuter un pas « poser » sur un cas fabriqué.
    ② CONTEXTE D'APPEL — `epreuve`, une fois par cas de E4 et E5.
    ③ ENTRÉE — `script` : le texte du pas · `prep` : une fonction qui modifie l'espace avant le pas.
    ④ CONDITIONS D'ENTRÉE — bash existe.
    ⑤ SORTIE — DEUX valeurs : le code de sortie du pas ; la liste de ce qui cloche après lui, chaque élément un texte :
      « encore présent : <chemin> » pour le code privé non publié resté sur la machine (archives/VIEUX.py,
      programmes/sous/CACHE.py, programmes/COMMUN/__init__.pyc), « effacé : <chemin> » pour un fichier publié du cas
      qui n'y est plus (ajouté le 01-11-2026 : un pas tiré d'une autre liste que celle qui publie effaçait
      tests/outils/ sans rougir).
      [rend: 2]
    ⑥ TRAITEMENT — créer, à la racine et sous _code/, deux programmes, une épreuve, un fichier de lancement, emp.py,
      un outil d'études, un outil d'épreuves (tests/outils/J.py) et les deux fichiers de circuit, identiques des deux
      côtés, plus deux fichiers de code privé non publiés ; appliquer `prep` ; exécuter ; relever ce qui reste et ce
      qui manque ; effacer.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — `bash -e` : la commande même de GitHub pour un pas, et celle d'ETAPE_MUETTE.py.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit et efface un dossier jetable.
    ⑪ TERMINAISON — Rend la main ; le pas est borné à 60 secondes.
      [sort: non]
    """
    w = tempfile.mkdtemp(prefix="pas_")
    try:
        for d in ("programmes", "tests", "etudes/outils", "tests/outils", "archives", "programmes/sous", ".github/workflows",
                  "_code/programmes", "_code/tests", "_code/etudes/outils", "_code/tests/outils", "_code/.github/workflows",
                  "_code/circuits_du_prive"):
            os.makedirs(os.path.join(w, d))
        publies = (("programmes/A.py", "a=1\n"), ("programmes/B.py", "b=2\n"), ("tests/T.py", "t=3\n"),
                   ("tests/LANCEMENT_DES_EPREUVES.json", "{}\n"), ("emp.py", "e=1\n"), ("etudes/outils/O.py", "o=1\n"),
                   ("tests/outils/J.py", "j=1\n"))
        for base in ("", "_code/"):
            for f, c in publies:
                open(os.path.join(w, base + f), "w").write(c)
        os.makedirs(os.path.join(w, "programmes", "COMMUN"))
        for f in ("archives/VIEUX.py", "programmes/sous/CACHE.py", "programmes/COMMUN/__init__.pyc"):   # code privé non publié
            open(os.path.join(w, f), "w").write("x=1\n")
        for n in ("certifier_la_version.yml", "circuit_du_soir.yml"):
            open(os.path.join(w, "_code/.github/workflows", n), "w").write("x\n")
        for f in (".github/workflows/F.yml", "_code/circuits_du_prive/F.yml"):      # une fiche du privé, publiée à part
            open(os.path.join(w, f), "w").write("pas: 1\n")
        prep(w)
        env = dict(os.environ, RUNNER_TEMP=os.path.join(w, "_temp"))
        x = subprocess.run(["bash", "-e", "-c", script], cwd=w, env=env, capture_output=True, text=True, timeout=60)
        restes = [f"encore présent : {f}" for f in ("archives/VIEUX.py", "programmes/sous/CACHE.py",
                                                    "programmes/COMMUN/__init__.pyc") if os.path.exists(os.path.join(w, f))]
        restes += [f"effacé : {f}" for f, _ in publies if not os.path.exists(os.path.join(w, f))]
        return x.returncode, restes
    finally:
        shutil.rmtree(w, ignore_errors=True)


def ecrire(chemin, contenu):
    """Rend une fonction qui écrit `contenu` dans `chemin` sous l'espace donné.

    ① RÔLE — Fabriquer un écart. ② CONTEXTE D'APPEL — `epreuve`. ③ ENTRÉE — un chemin relatif, un texte.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la fonction. [rend: 1] ⑥ TRAITEMENT — fermer sur les deux.
    ⑦ UNITÉ — — ⑧ POURQUOI — Un cas par écart. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun (la fonction rendue écrit).
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    def f(w):
        open(os.path.join(w, chemin), "w").write(contenu)
    return f


def lien_vers_le_prive(w):
    """Pose programmes/L.py en lien vers du code privé, et au public un fichier de même contenu.

    ① RÔLE — Le cas du relecteur du 15-10-2026 (N1) : un programme publié qui est en fait un lien vers un dossier
      privé ; Python mettrait alors ce dossier privé en tête de ses chemins d'import.
    ② CONTEXTE D'APPEL — `epreuve`, un cas de E4. ③ ENTRÉE — `w` : l'espace de travail.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Aucune valeur.
      [rend: 0]
    ⑥ TRAITEMENT — créer un fichier privé qui n'est pas du code (donnees/CIBLE.txt, que rien n'efface), le lien
      programmes/L.py vers lui, et la copie publique de même contenu (la comparaison des contenus passe).
    ⑦ UNITÉ — — ⑧ POURQUOI — Seul le refus des liens arrête ce cas. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans `w`. ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    os.makedirs(os.path.join(w, "donnees"), exist_ok=True)
    open(os.path.join(w, "donnees", "CIBLE.txt"), "w").write("x=1\n")
    os.symlink("../donnees/CIBLE.txt", os.path.join(w, "programmes", "L.py"))
    open(os.path.join(w, "_code", "programmes", "L.py"), "w").write("x=1\n")


# LES CAS DU MOTIF DE JETON (E8 ①, superviseur R-759 du 05-11-2026 à 00h52, D2) : (nom, chaîne, doit être reconnue ?).
# Chaque branche du motif a son cas positif (la retirer le fait rougir) et son cas négatif (l'élargir le fait rougir).
# Les chaînes sont FABRIQUÉES par concaténation : ce fichier est lui-même publié, et le fabricant le refuserait s'il
# portait une forme de jeton écrite d'un bloc (Z0 le vérifie à chaque passage). Jetons fictifs.
_PAT = "github" + "_pat_"
CAS_DU_MOTIF = (
    ("jeton fin github_pat_", _PAT + "A1b2" * 6, True),
    ("majuscules", (_PAT + "A1b2" * 6).upper(), True),
    ("jeton classique ghp_", "gh" + "p_" + "A1b2C3d4E5" * 2 + "xy", True),
    # un « _ » devant « gh » : « \b » ne voyait pas ce jeton (relecture du tour 2, D4 ; superviseur du 05-11-2026 à 03h10)
    ("jeton ghp_ collé derrière « _ »", "X_" + "gh" + "p_" + "A1b2C3d4E5" * 2 + "xy", True),
    ("jeton des Actions ghs_", "gh" + "s_" + "Z9y8X7w6V5" * 2 + "uv", True),
    ("jeton OAuth gho_", "gh" + "o_" + "A1b2C3d4E5" * 2 + "xy", True),
    ("jeton utilisateur ghu_", "gh" + "u_" + "A1b2C3d4E5" * 2 + "xy", True),
    ("jeton de renouvellement ghr_", "gh" + "r_" + "A1b2C3d4E5" * 2 + "xy", True),
    ("adresse à identifiants", "https://" + "u" + ":" + "s3cr3t" + "@github.com/x/y", True),
    ("en-tête Basic", "Authorization: " + "Basic " + "eC1hY2Nlc3M6", True),
    ("le mot github_pat_ seul", _PAT, False),
    # le même mot en majuscules : sans lui, le détecteur de la propriété prenait « [A-Z]{4,} » ou un « .split("T") »
    # pour des motifs de jeton (mesuré le 05-11-2026 sur deux études et une archive du dépôt)
    ("le mot GITHUB_PAT_ seul, en majuscules", _PAT.upper(), False),
    ("github_pat_ suivi de 19 caractères", _PAT + "A1b2" * 4 + "xyz", False),
    ("ghp_ suivi de 19 caractères", "gh" + "p_" + "A1b2C3d4E5" + "A1b2C3d4E", False),
    ("le filtre sed du dépôt", "sed 's/" + _PAT + "[A-Za-z0-9_]*/***/g; s/basic [A-Za-z0-9+\\/=]*/***/g'", False),
    ("Authorization: Basic ${B64}", "Authorization: " + "Basic ${B64}", False),
    ("${{ secrets.X }} dans une adresse", "https://x-access-token:" + "${{ secrets.X }}" + "@github.com", False),
)
# Les appels du module re dont le premier argument est un motif.
APPELS_A_MOTIF = ("compile", "search", "match", "fullmatch", "findall", "finditer", "sub", "subn", "split")


def motifs_de_jeton_compiles(source):
    """Rend les numéros des lignes où `source` passe à re un motif LITTÉRAL qui reconnaît un jeton.

    ① RÔLE — Le détecteur de la propriété « un seul motif de jeton dans le code publié » (E8 ②).
    ② CONTEXTE D'APPEL — `epreuve_du_motif`, une fois par fichier `.py` publié et deux fois pour se calibrer.
    ③ ENTRÉE — `source` : le texte d'un fichier Python.
    ④ CONDITIONS D'ENTRÉE — `source` s'analyse (sinon SyntaxError remonte, et l'appelant le compte comme une faute).
    ⑤ SORTIE — UNE valeur : la liste des numéros de ligne (vide si aucun).
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque appel `x.<un de APPELS_A_MOTIF>(…)` dont le premier argument est une chaîne ou des
      octets littéraux : le compiler (re.IGNORECASE s'il figure parmi les autres arguments) ; c'est un motif de jeton
      s'il reconnaît au moins un cas POSITIF de CAS_DU_MOTIF et AUCUN cas négatif. Un motif qui ne se compile pas est
      ignoré.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une PROPRIÉTÉ, pas une liste d'écritures : « reconnaît un jeton et pas ses sosies ». Un motif qui
      reconnaît aussi un cas négatif (« \\w+ », « : ») n'est pas un motif de jeton ; une citation du mot n'est pas un
      motif (superviseur R-759 du 05-11-2026, D1 : calibrer sur le module, porteur attendu, et sur une citation).
    ⑨ CE QUI CLOCHE — Un motif construit (concaténé, lu dans une variable, `"|".join(…)`) ou passé à grep dans une
      chaîne de shell n'est pas vu : seul le littéral passé directement à re l'est. Un appel `.split(",")` d'une
      chaîne est examiné comme un motif : sans effet, une virgule seule reconnaît aussi des cas négatifs. · Il ne voit
      qu'une copie AUSSI STRICTE que les cas : une copie divergente (seuil abaissé, masquage plus lâche) ou appelée par
      `from re import compile` ne se voit pas (relecture du tour 2, D2, cas P2, P4, P5).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    lignes = []
    with warnings.catch_warnings():       # un échappement douteux d'un autre fichier n'est pas l'affaire de ce détecteur
        warnings.simplefilter("ignore", SyntaxWarning)
        arbre = ast.parse(source)
    for n in ast.walk(arbre):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in APPELS_A_MOTIF
                and n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, (str, bytes))):
            continue
        motif = n.args[0].value
        autres = list(n.args[1:]) + [k.value for k in n.keywords]
        drapeaux = re.IGNORECASE if any(isinstance(x, ast.Attribute) and x.attr in ("IGNORECASE", "I")
                                        for a in autres for x in ast.walk(a)) else 0
        try:
            c = re.compile(motif, drapeaux)
        except (re.error, TypeError, ValueError):
            continue
        sous = (lambda s: s.encode("utf-8")) if isinstance(motif, bytes) else (lambda s: s)
        if any(c.search(sous(ch)) for _, ch, pos in CAS_DU_MOTIF if pos) and \
                not any(c.search(sous(ch)) for _, ch, pos in CAS_DU_MOTIF if not pos):
            lignes.append(n.lineno)
    return lignes


def epreuve_du_motif(r):
    """E8 ① et ② — le motif de la copie sur CAS_DU_MOTIF, et la propriété « un seul porteur » ; rend les fautes.

    ① RÔLE — Juger le motif de jeton de la copie (sabotée ou non) AVANT toute fabrication, et vérifier qu'aucun
      autre fichier de code publié n'en compile un.
    ② CONTEXTE D'APPEL — `epreuve`, une fois par sabotage, avant le fabricant.
    ③ ENTRÉE — `r` : la copie du dépôt privé.
    ④ CONDITIONS D'ENTRÉE — La copie porte MOD (sinon : une faute, pas une exception).
    ⑤ SORTIE — UNE valeur : la liste des fautes, d'abord celles du motif (« E8 motif : « nom » non reconnu » pour un
      cas positif, « … refusé à tort » pour un cas négatif, dans l'ordre de CAS_DU_MOTIF), puis celles de la
      propriété (« E8 propriété : … »).
      [rend: 1]
    ⑥ TRAITEMENT — ① charger MOD de la copie par son chemin et passer chaque cas à sa fonction
      `porte_une_forme_de_jeton` ; ② calibrer le détecteur `motifs_de_jeton_compiles` sur un motif (doit être vu)
      et sur une citation du mot (ne doit pas l'être) ; ③ le passer sur chaque `.py` que publie le fabricant DE
      L'ÉPREUVE (`code_a_publier`, PROPRIETE : jamais la liste de la copie sabotée) : MOD doit être vu, et seul.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur R-759 du 05-11-2026 à 00h52 (D1, D2) : le motif attendu des sabotages S104 et S105 du
      tour 1 (« ne peuvent pas aller au dépôt public ») collait à n'importe quel refus ; une épreuve unitaire nomme le
      cas. Et un motif vit à UN endroit (R-708) : la propriété empêche qu'une copie revienne dans le code publié.
    ⑨ CE QUI CLOCHE — Le détecteur a les limites de `motifs_de_jeton_compiles` (motif construit, motif en shell).
      Les cas sont fictifs : leur forme suit la documentation des préfixes de GitHub telle que la portait l'étude
      du 01-11-2026, pas un vrai jeton.
    ⑩ EFFET — Exécute le module de la copie ; lit les fichiers de code de la copie.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    fautes = []
    try:
        sp = _iu.spec_from_file_location("forme_d_un_jeton_de_la_copie", os.path.join(r, MOD))
        module = _iu.module_from_spec(sp)
        sp.loader.exec_module(module)
        for nom, chaine, positif in CAS_DU_MOTIF:
            if module.porte_une_forme_de_jeton(chaine) != positif:
                fautes.append(f"E8 motif : « {nom} » " + ("non reconnu" if positif else "refusé à tort"))
    except Exception as e:      # un module absent ou cassé est une faute nommée, jamais une épreuve qui tombe
        fautes.append(f"E8 motif : {MOD} illisible ({type(e).__name__}: {e})"[:200])
    if not motifs_de_jeton_compiles('import re\nM = re.compile(r"\\bgh' + 's_[A-Za-z0-9]{20,}")\n'):
        fautes.append("E8 propriété : le détecteur ne voit pas un motif de jeton (calibrage positif)")
    if motifs_de_jeton_compiles('import re\nM = re.compile(r"github' + '_pat_")\n'):
        fautes.append("E8 propriété : le détecteur prend une citation du mot pour un motif (calibrage négatif)")
    porteurs = {}
    for rel in PROPRIETE.code_a_publier(r):
        if rel.endswith(".py"):
            try:
                lignes = motifs_de_jeton_compiles(open(os.path.join(r, rel), encoding="utf-8").read())
            except (SyntaxError, UnicodeDecodeError, ValueError) as e:
                fautes.append(f"E8 propriété : {rel} illisible ({type(e).__name__})")
                continue
            if lignes:
                porteurs[rel] = lignes
    if MOD not in porteurs:
        fautes.append(f"E8 propriété : {MOD} ne compile aucun motif de jeton (calibrage sur le porteur attendu)")
    for rel in sorted(set(porteurs) - {MOD}):
        fautes.append(f"E8 propriété : motif de jeton compilé hors de {MOD} : {rel} (ligne {porteurs[rel][0]})")
    return fautes


def cas_de_branche(r, d):
    """E9 — le fabricant DE LA COPIE n'écrit dans un clone public que s'il est sur la branche du dépôt privé.

    ① RÔLE — Prouver la propriété `refus_de_branche` du fabricant : le code d'une version en attente (dépôt privé sur
      une branche « travail-… ») ne peut pas être écrit dans un clone public sur main, et l'est sur la branche publique
      du même nom.
    ② CONTEXTE D'APPEL — `epreuve`, une fois par sabotage, avant la fabrication principale.
    ③ ENTRÉE — `r` : la copie (sabotée ou non) du dépôt privé, sans « .git » · `d` : son dossier jetable.
    ④ CONDITIONS D'ENTRÉE — git ≥ 2.28 (« git init -b ») ; `r` n'a pas de « .git » (la copie de `epreuve` l'exclut).
    ⑤ SORTIE — UNE valeur : la liste des fautes, vide si tout est conforme (« E9 branche publique « main », privé
      « travail-essai » : … » ; « E9 même branche refusée : … »).
      [rend: 1]
    ⑥ TRAITEMENT — « git init -b travail-essai » dans `r` (une branche non née suffit : le fabricant lit le nom) ; pour
      un clone public « git init -b main » puis « git init -b travail-essai », lancer le fabricant de la copie : le
      premier doit rendre un code non nul et ne rien écrire hors de « .git », le second rendre 0 et écrire le circuit
      des séries ; le « .git » de `r` et les deux clones sont retirés, même en cas d'erreur.
    ⑦ UNITÉ — Des secondes : la borne du fabricant, 120.
    ⑧ POURQUOI — Décision de Jean-Luc du 05-11-2026 à 13h36, « 2 » : les séries longues tournent sur GitHub AVANT la
      fusion, depuis une branche publique qui porte le code de la version en attente, du même nom (« publier ce qui
      tourne », cadre du 08-10-2026) ; option 1 (après la fusion, retour arrière) refusée, une version non éprouvée
      serait la version officielle environ une heure. Aucun écrit sur main du dépôt public par erreur de branche.
    ⑨ CE QUI CLOCHE — Les dépôts sont des « git init » sans commit, pas des clones : la lecture de la branche est la
      même (symbolic-ref), la poussée qui suivrait n'est pas jouée. Le cas « clone public sans .git » n'est pas
      joué ici : c'est la fabrication principale de chaque passage.
    ⑩ EFFET — Écrit puis efface, dans `d` et dans `r`.
    ⑪ TERMINAISON — Rend la main ; chaque appel est borné (git 30 s, fabricant 120 s).
      [sort: non]
    """
    fautes = []
    env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")

    def init(dossier, branche):
        """Crée un dépôt git vide sur `branche` (nom d'une branche non née).

        ① RÔLE — Poser un dépôt git dont la branche courante est connue.
        ② CONTEXTE D'APPEL — `cas_de_branche`, trois fois.
        ③ ENTRÉE — `dossier`, `branche`.
        ④ CONDITIONS D'ENTRÉE — git ≥ 2.28.
        ⑤ SORTIE — Aucune valeur ; lève CalledProcessError si git échoue.
          [rend: 0]
        ⑥ TRAITEMENT — « git init -q -b ».
        ⑦ UNITÉ — Des secondes : la borne de git, 30.
        ⑧ POURQUOI — Voir `cas_de_branche`.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Écrit `dossier`/.git.
        ⑪ TERMINAISON — Rend la main, ou lève ; l'appel à git est borné à 30 s.
          [sort: non]
        """
        subprocess.run(["git", "init", "-q", "-b", branche, dossier], check=True, capture_output=True, env=env,
                       timeout=30)

    try:
        init(r, "travail-essai")
        for branche_pub, permis in (("main", False), ("travail-essai", True)):
            pub = os.path.join(d, "public_e9_" + branche_pub)
            os.makedirs(pub)
            init(pub, branche_pub)
            x = subprocess.run([sys.executable, os.path.join(r, FAB), r, pub], capture_output=True, text=True,
                               timeout=120, env=env)
            ecrits = sorted(f for f in os.listdir(pub) if f != ".git")
            if not permis and (x.returncode == 0 or ecrits):
                fautes.append(f"E9 branche publique « main », privé « travail-essai » : code {x.returncode}, "
                              f"{len(ecrits)} entrée(s) écrite(s) au public")
            if permis and (x.returncode != 0 or not os.path.isfile(os.path.join(pub, PROPRIETE.CIRCUIT_SERIES))):
                fautes.append(f"E9 même branche refusée : code {x.returncode} : {(x.stdout + x.stderr).strip()[-200:]}")
            shutil.rmtree(pub, ignore_errors=True)
    except (OSError, subprocess.SubprocessError) as e:
        fautes.append(f"E9 n'a pas pu tourner : {e}")
    finally:
        shutil.rmtree(os.path.join(r, ".git"), ignore_errors=True)
    return fautes


def cas_m5(r, d):
    """E8 ③ à ⑤ — joue le fabricant DE LA COPIE sur les cas du défaut M5 ; rend les fautes.

    ① RÔLE — Prouver que le fabricant refuse, avant d'écrire quoi que ce soit au public, tout lien symbolique, tout
      fichier dont le chemin réel sort de sa place dans le dépôt privé, tout lien dur, tout fichier qui n'est pas du
      texte UTF-8 strict (chaque clause par son cas) et
      tout fichier portant une chaîne de la forme d'un jeton, DANS CHAQUE EMPLACEMENT qu'il publie, pour le code, le
      fichier de lancement ET les fiches de circuit ; et qu'il publie, sans rien refuser, ce qui n'en a que
      l'apparence (le mot « github_pat_ » seul, le filtre sed du dépôt, une valeur « Basic » écrite par variable).
    ② CONTEXTE D'APPEL — `epreuve`, une fois par sabotage, avant la fabrication principale.
    ③ ENTRÉE — `r` : la copie (sabotée ou non) du dépôt privé · `d` : son dossier jetable, qui contient `r` ; ce qui
      est posé dans `d` hors de `r` est HORS du dépôt.
    ④ CONDITIONS D'ENTRÉE — La copie porte les emplacements de code du fabricant de l'épreuve (PROPRIETE), son
      fichier de lancement, .github/workflows/ et tests/outils/.
    ⑤ SORTIE — UNE valeur : la liste des fautes (vide si tout est conforme), dans l'ordre : course groupée
      (« E8 groupe à refuser : publié, fabricant au code 0 », puis « E8 non refusé : <fichier> (<nature>) » ou
      « E8 refusé pour une autre raison : … » dans l'ordre de pose, puis les fichiers écrits), dossier lié, cas qui
      doit passer.
      [rend: 1]
    ⑥ TRAITEMENT — ③ UNE course où tout ce qui doit être refusé est posé ensemble : dans chaque emplacement de
      DOSSIERS_DE_CODE lu au fabricant de l'épreuve, LIEN_M5_HORS.py (lien vers un fichier hors du dépôt) et
      JETON_M5_LOIN.py (un jeton après 9 000 octets : une lecture partielle ne le voit pas) ; un jeton loin AJOUTÉ au
      fichier de lancement ; dans .github/workflows/, une fiche liée hors du dépôt et une fiche portant un en-tête
      Basic loin ; programmes/LIEN_M5_DEDANS.py, lien vers un fichier du dépôt ; programmes/DUR_M5.py, lien DUR vers
      le fichier hors du dépôt ; tests/outils/U16NB_M5.py, jeton en UTF-16-LE sans BOM (raison attendue : « clause des
      contrôles ») ; tests/outils/CP500_M5.py, jeton en EBCDIC cp500 (« clause UTF-8 »). Exigé : code non nul, chaque fichier
      posé nommé sur une ligne du refus avec sa raison, 0 fichier au public (le fabricant liste TOUS les refus :
      retirer une garde laisse un nom absent). ④ À part : tests/outils/ déplacé hors du dépôt et remplacé par un lien
      → refusé, rien écrit. ⑤ À part : le cas qui doit passer → code 0, fichier publié. Tout ce qui est posé est
      retiré après chaque course, même en cas d'erreur.
    ⑦ UNITÉ — Octets (le préfixe de 9 000 octets, au-delà des 8 Ko demandés par le superviseur).
    ⑧ POURQUOI — Défaut M5 (relecture de Cowork du 04-11-2026 à 21h17, I1). Relecture neuve du 04-11-2026, D2 :
      l'E8 du tour 1 épelait quatre emplacements et posait ses écarts en tête de petits fichiers ; quatre mutations
      (lecture des 4 096 premiers octets, racine, .json, tests/*.py hors de la garde) le laissaient vert. Superviseur
      R-759 du 05-11-2026 à 00h52 : emplacements LUS au fabricant, une seule course groupée, chaque fichier nommé.
    ⑨ CE QUI CLOCHE — Le fichier « hors du dépôt » est dans le dossier jetable, pas ailleurs sur la machine : la
      propriété jugée est la même (sortir de la racine du dépôt). · La raison est jugée sur un mot (« lien dur »,
      « clause UTF-8 »…), pas sur la phrase entière ; un lien hors du dépôt admet « lien symbolique » OU « HORS du dépôt »,
      les deux gardes qui l'arrêtent. · La course entre le contrôle et la copie (D3) et un lien
      posé dans le clone public (D6) ne sont pas éprouvés ici : voir le ⑨ de `refus_avant_publication`.
    ⑩ EFFET — Écrit dans `r` et dans `d`, puis retire ce qu'il a posé ; lance le fabricant (trois processus).
    ⑪ TERMINAISON — Rend la main ; chaque lancement est borné à 120 secondes.
      [sort: non]
    """
    jeton = "github" + "_pat_" + "A1b2" * 6 + "_fictif"
    basique = "AUTHORIZATION: " + "basic " + "eC1hY2Nlc3MtdG9rZW46ZmljdGlm"
    loin = "#" * 9000 + "\n"
    dehors = os.path.join(d, "hors_du_depot")
    os.makedirs(dehors, exist_ok=True)
    secret = os.path.join(dehors, "SECRET_M5.txt")
    open(secret, "w").write("SECRET-HORS-DEPOT-M5\n")
    # la cible du lien DUR est un AUTRE fichier : sinon les liens symboliques vers `secret` le verraient à deux noms
    # et seraient refusés comme liens durs quand le refus des liens est retiré (S100, mesuré le 05-11-2026)
    secret_dur = os.path.join(dehors, "SECRET_DUR_M5.txt")
    open(secret_dur, "w").write("SECRET-HORS-DEPOT-M5-DUR\n")
    fiches = PROPRIETE.FICHES_PRIVEES.replace(os.sep, "/")
    programmes = os.path.dirname(FAB)
    fautes, poses, retraits = [], [], []
    # un lien vers un fichier hors du dépôt est bien refusé par l'une OU l'autre garde (① le lien, ② le chemin réel) :
    # chaque raison admise protège (S101 retire ② seul : ① dit alors « lien symbolique », sans « HORS »)
    HORS = ("lien symbolique", "HORS du dépôt")

    def lancer(pub):
        os.makedirs(pub)
        return subprocess.run([sys.executable, os.path.join(r, FAB), r, pub], capture_output=True, text=True,
                              timeout=120)

    def poser(rel, nature, raison, octets=None, cible=None, dur=None):
        p = os.path.join(r, rel)
        if octets is not None:
            open(p, "wb").write(octets)
        elif cible is not None:
            os.symlink(cible, p)
        else:
            os.link(dur, p)
        retraits.append(lambda: os.remove(p))
        poses.append((rel, nature, raison))

    try:
        # ③ la course groupée
        for dossier in PROPRIETE.DOSSIERS_DE_CODE:
            if not os.path.isdir(os.path.join(r, dossier)):
                fautes.append(f"E8 emplacement de code absent de la copie : {dossier or 'la racine'}")
                continue
            poser(PROPRIETE._chemin(dossier, "LIEN_M5_HORS.py"), "lien hors du dépôt", HORS, cible=secret)
            poser(PROPRIETE._chemin(dossier, "JETON_M5_LOIN.py"), "jeton après 9 000 octets", "forme d'un jeton",
                  octets=(loin + f"X = '{jeton}'\n").encode())
        lanc = os.path.join(r, PROPRIETE.LANCEMENT)
        avant = open(lanc, "rb").read()
        open(lanc, "wb").write(avant + ("\n" + loin + f'"{jeton}"\n').encode())
        retraits.append(lambda: open(lanc, "wb").write(avant))
        poses.append((PROPRIETE.LANCEMENT, "jeton après 9 000 octets", "forme d'un jeton"))
        poser(fiches + "/lien_m5_hors.yml", "fiche liée hors du dépôt", HORS, cible=secret)
        poser(fiches + "/jeton_m5_loin.yml", "en-tête Basic après 9 000 octets", "forme d'un jeton",
              octets=(loin + f"        run: git -c http.extraheader='{basique}' push\n").encode())
        cible_dedans = os.path.join(r, "donnees_m5_cible.txt")       # pas publiée : la cible, pas un cas
        open(cible_dedans, "w").write("x = 1\n")
        retraits.append(lambda: os.remove(cible_dedans))
        poser(programmes + "/LIEN_M5_DEDANS.py", "lien vers un fichier du dépôt", "lien symbolique",
              cible="../donnees_m5_cible.txt")
        poser(programmes + "/DUR_M5.py", "lien dur hors du dépôt", "lien dur", dur=secret_dur)
        # le texte strict, une clause par cas (superviseur R-759 du 05-11-2026 à 03h10, D1) : l'UTF-16 AVEC BOM était
        # refusé par les DEUX clauses, il ne prouvait donc aucune des deux. L'UTF-16-LE SANS BOM est de l'UTF-8 valide
        # (seule la clause des contrôles l'arrête, par U+0000) ; le cp500 n'est pas de l'UTF-8 et ne porte aucun
        # caractère de contrôle (seule la clause UTF-8 l'arrête).
        poser("tests/outils/U16NB_M5.py", "jeton en UTF-16-LE sans BOM", "clause des contrôles",
              octets=f"X = '{jeton}'\n".encode("utf-16-le"))
        poser("tests/outils/CP500_M5.py", "jeton en EBCDIC cp500", "clause UTF-8",
              octets=f"X = '{jeton}'\n".encode("cp500"))
        pub = os.path.join(d, "public_m5_groupe")
        x = lancer(pub)
    finally:
        for f in reversed(retraits):
            f()
    nommes = {}
    for ligne in x.stdout.splitlines():
        if ligne.startswith("  ") and " : " in ligne:
            rel, raison = ligne[2:].split(" : ", 1)
            nommes[rel] = raison
    if x.returncode == 0:
        fautes.append("E8 groupe à refuser : publié, fabricant au code 0")
    for rel, nature, raison in poses:
        if rel not in nommes:
            fautes.append(f"E8 non refusé : {rel} ({nature})")
        elif not any(x in nommes[rel] for x in ((raison,) if isinstance(raison, str) else raison)):
            fautes.append(f"E8 refusé pour une autre raison : {rel} (attendu « {raison} », lu « {nommes[rel]} »)")
    ecrits = sum(len(fs) for _, _, fs in os.walk(pub))
    if ecrits:
        fautes.append(f"E8 groupe à refuser : {ecrits} fichier(s) écrit(s) au public avant le refus")
    shutil.rmtree(pub, ignore_errors=True)

    # ④ un emplacement de code qui est un dossier lié hors du dépôt
    vrai, ailleurs = os.path.join(r, "tests", "outils"), os.path.join(dehors, "outils")
    shutil.move(vrai, ailleurs)
    os.symlink(ailleurs, vrai)
    try:
        pub = os.path.join(d, "public_m5_lie")
        x = lancer(pub)
    finally:
        os.remove(vrai)
        shutil.move(ailleurs, vrai)
    ecrits = sum(len(fs) for _, _, fs in os.walk(pub))
    if x.returncode == 0:
        fautes.append("E8 « emplacement lié hors du dépôt » : publié, fabricant au code 0")
    elif "  tests/outils/" not in x.stdout:
        fautes.append(f"E8 « emplacement lié hors du dépôt » : refusé sans nommer tests/outils/ ({x.stdout.strip()[-120:]})")
    if ecrits:
        fautes.append(f"E8 « emplacement lié hors du dépôt » : {ecrits} fichier(s) écrit(s) au public avant le refus")
    shutil.rmtree(pub, ignore_errors=True)

    # ⑤ ce qui n'a que l'apparence d'un jeton est publié
    rel = programmes + "/FILTRE_M5.py"
    open(os.path.join(r, rel), "w").write(
        "# le mot github_pat_ seul ; filtre : sed 's/github_pat_[A-Za-z0-9_]*/***/g; s/basic [A-Za-z0-9+\\/=]*/***/g'\n"
        "B = 'Authorization: Basic ${B64}'\n")
    try:
        pub = os.path.join(d, "public_m5_passe")
        x = lancer(pub)
    finally:
        os.remove(os.path.join(r, rel))
    if x.returncode != 0 or not os.path.isfile(os.path.join(pub, rel)):
        fautes.append(f"E8 « le mot github_pat_ seul » : refusé à tort, code {x.returncode} ({x.stdout.strip()[-120:]})")
    shutil.rmtree(pub, ignore_errors=True)
    return fautes


def jouer_soir(poser, mord, prep, garde):
    """Joue le pas « Poser » puis le pas « Le garde du code mord-il ? » du circuit du soir ; rend leur état.

    ① RÔLE — Éprouver les pas du circuit du soir qui posent le code public et le garde (20-10-2026).
    ② CONTEXTE D'APPEL — `epreuve`, une fois par cas de E5 et E7.
    ③ ENTRÉE — `poser`, `mord` : les textes des deux pas · `prep` : une fonction qui modifie l'espace avant le
      premier pas · `garde` : le texte du programme du garde (programmes/N_EXECUTER_AU_PUBLIC_QUE_LE_CODE_PUBLIE.py de la copie éprouvée).
    ④ CONDITIONS D'ENTRÉE — bash et python3 existent.
    ⑤ SORTIE — CINQ valeurs : le code du pas « Poser » ; les codes du pas du garde (None si « Poser » est tombé) ;
      vrai si le code public est rangé hors du clone ($RUNNER_TEMP/code) et `_code` effacé ; les lignes écrites
      dans GITHUB_ENV ; la liste des fautes du témoin et des pièges (vide si tout va bien, vide aussi si
      « Poser » est tombé). Les codes du pas du garde sont TROIS : avec le garde, sans le garde, avec un garde MUTANT dont la porte « exec » est morte
      (None si non joué).
      [rend: 5]
    ⑥ TRAITEMENT — Fabriquer, à la racine et sous _code/, deux programmes (A.py, B.py) et le garde,
      identiques ; appliquer `prep` ; jouer « Poser » par bash -e avec RUNNER_TEMP, GITHUB_ENV et GITHUB_WORKSPACE ;
      relever GITHUB_ENV ; jouer le pas du garde dans l'environnement que GITHUB_ENV donne, comme GitHub au pas
      suivant ; le rejouer avec un garde mutant ; puis, dans ce même environnement : un témoin (importer un
      module publié doit rendre 0) et quatre pièges qui doivent rendre 97 sans écrire leur marqueur — A lancé
      par `python3 etudes/X.py`, B importé par `python3 -c`, C lancé par un parent qui démarre l'enfant avec
      `-I` (le parent doit être arrêté), D un `.pyc` UNCHECKED_HASH glissé à côté d'un module publié (joué
      en dernier, il salit le cache).
    ⑦ UNITÉ — — ⑧ POURQUOI — Le pas du garde n'a de sens que dans l'environnement que « Poser » a écrit :
      les jouer à part ne prouverait rien. ⑨ CE QUI CLOCHE — GITHUB_ENV est lu ligne à ligne, sans la forme
      « nom<<délimiteur » que GitHub accepte aussi (le pas ne l'emploie pas).
    ⑩ EFFET — Écrit et efface un dossier jetable. ⑪ TERMINAISON — Rend la main ; chaque pas est borné à 60 secondes.
      [sort: non]
    """
    w = tempfile.mkdtemp(prefix="soir_")
    try:
        ws, rt = os.path.join(w, "ws"), os.path.join(w, "rt")
        for d in ("programmes", "etudes", "_code/programmes", "_code/.github/workflows"):
            os.makedirs(os.path.join(ws, d))
        os.makedirs(rt)
        for base in ("", "_code/"):
            for f, c in (("programmes/A.py", "a=1\n"), ("programmes/B.py", "b=2\n"),
                         ("programmes/N_EXECUTER_AU_PUBLIC_QUE_LE_CODE_PUBLIE.py", garde)):
                open(os.path.join(ws, base + f), "w", encoding="utf-8").write(c)
        open(os.path.join(ws, "_code/.github/workflows/circuit_du_soir.yml"), "w").write("x\n")
        prep(ws)
        env_f = os.path.join(rt, "github_env")
        open(env_f, "w").close()
        env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "GARDE_DONNEES", "GARDE_CODE")}
        env.update(RUNNER_TEMP=rt, GITHUB_ENV=env_f, GITHUB_WORKSPACE=ws)
        c1 = subprocess.run(["bash", "-e", "-c", poser], cwd=ws, env=env, capture_output=True, text=True, timeout=60).returncode
        lignes = [l.rstrip("\n") for l in open(env_f, encoding="utf-8")]
        range_ = os.path.isdir(os.path.join(rt, "code")) and not os.path.exists(os.path.join(ws, "_code"))
        if c1 != 0:
            return c1, None, range_, lignes, []
        for l in lignes:
            if "=" in l:
                k, v = l.split("=", 1)
                env[k] = v
        c2 = subprocess.run(["bash", "-e", "-c", mord], cwd=ws, env=env, capture_output=True, text=True, timeout=60).returncode
        sans = {k: v for k, v in env.items() if k != "PYTHONPATH"}
        c3 = subprocess.run(["bash", "-e", "-c", mord], cwd=ws, env=sans, capture_output=True, text=True, timeout=60).returncode
        gf = os.path.join(rt, "garde", "sitecustomize.py")
        mutant = garde.replace('        if evenement == "exec":\n', '        if False:\n', 1)
        c4 = None
        if mutant != garde and os.path.isfile(gf):
            open(gf, "w", encoding="utf-8").write(mutant)
            c4 = subprocess.run(["bash", "-e", "-c", mord], cwd=ws, env=env, capture_output=True, text=True, timeout=60).returncode
            open(gf, "w", encoding="utf-8").write(garde)
        import py_compile, importlib.util
        for n in "ABC":
            open(os.path.join(ws, "etudes", "PIEGE_%s.py" % n), "w").write("open('MARQUEUR_%s', 'w')\n" % n)
        fautes = []
        t = subprocess.run([sys.executable, "-c", "import sys; sys.path.insert(0, 'programmes'); import A"],
                           cwd=ws, env=env, capture_output=True, text=True, timeout=60)
        if t.returncode != 0:
            fautes.append("témoin : un module publié, importé, est refusé (code %d)" % t.returncode)
        source = os.path.join(w, "source_piegee.py")
        open(source, "w").write("open('MARQUEUR_D', 'w')\n")
        def compile_piege():
            a = os.path.join(ws, "programmes", "A.py")
            py_compile.compile(source, cfile=importlib.util.cache_from_source(a), dfile=a,
                               invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH)
        for n, prep2, cmd in (
                ("A", None, [sys.executable, "etudes/PIEGE_A.py"]),
                ("B", None, [sys.executable, "-c", "import sys; sys.path.insert(0, 'etudes'); import PIEGE_B"]),
                ("C", None, [sys.executable, "-c", "import subprocess, sys; subprocess.run([sys.executable, '-I', 'etudes/PIEGE_C.py']); sys.exit(0)"]),
                ("D", compile_piege, [sys.executable, "-c", "import sys; sys.path.insert(0, 'programmes'); import A"])):
            if prep2:
                prep2()
            x = subprocess.run(cmd, cwd=ws, env=env, capture_output=True, text=True, timeout=60)
            if x.returncode != 97 or os.path.exists(os.path.join(ws, "MARQUEUR_" + n)):
                fautes.append("piège %s : code %d, marqueur %s" % (n, x.returncode, os.path.exists(os.path.join(ws, "MARQUEUR_" + n))))
        return c1, (c2, c3, c4), range_, lignes, fautes
    finally:
        shutil.rmtree(w, ignore_errors=True)


def epreuve(sab):
    """Joue E1 à E9 sur une copie du dépôt sabotée par `sab` ; rend (vert ?, détail).

    ① RÔLE — Une passe complète des épreuves.
    ② CONTEXTE D'APPEL — la boucle principale, une fois par sabotage.
    ③ ENTRÉE — `sab` : le nom du sabotage (Z0 : aucun).
    ④ CONDITIONS D'ENTRÉE — DEPOT est un dépôt privé.
    ⑤ SORTIE — DEUX valeurs : vrai si tout est conforme ; le détail (les quatre premières fautes).
      [rend: 2]
    ⑥ TRAITEMENT — copier, saboter, jouer E8 (motif, propriété, cas M5) et E9 (branches), fabriquer vers un faux
      public, confronter E1 à E7 ; si la fabrication principale tombe, le détail porte d'abord les fautes de E8 et E9.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir la fiche du fichier.
    ⑨ CE QUI CLOCHE — Voir la fiche du fichier.
    ⑩ EFFET — Écrit et efface un dossier jetable.
    ⑪ TERMINAISON — Rend la main ; le fabricant est borné à 120 s.
      [sort: non]
    """
    d = tempfile.mkdtemp(prefix="circuit_public_")
    fautes = []
    try:
        r = os.path.join(d, "prive")
        shutil.copytree(DEPOT, r, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        for f, a, b in SABOTAGES[sab]:
            p = os.path.join(r, f)
            t = open(p, encoding="utf-8").read()
            if t.count(a) != 1:
                return None, f"sabotage inapplicable : ancre absente ou multiple ({a[:50]!r})"
            open(p, "w", encoding="utf-8").write(t.replace(a, b))
        # E8 — le défaut M5, JOUÉ AVANT la fabrication principale : un motif élargi ou une lecture tronquée fait aussi
        # refuser le vrai dépôt, et le détail doit alors nommer le cas (superviseur R-759 du 05-11-2026, D2). Le motif
        # et la propriété (`epreuve_du_motif`), puis les cas du fabricant (`cas_m5`) ; ses fautes viennent en tête.
        fautes += epreuve_du_motif(r)
        fautes += cas_m5(r, d)
        fautes += cas_de_branche(r, d)
        pub = os.path.join(d, "public")
        for x in ("programmes", "tests"):
            os.makedirs(os.path.join(pub, x))
            open(os.path.join(pub, x, "SEULEMENT_AU_PUBLIC.py"), "w").write("x=1\n")
        x = subprocess.run([sys.executable, os.path.join(r, FAB), r, pub], capture_output=True, text=True, timeout=120)
        if x.returncode != 0:
            return False, "; ".join(fautes[:4] + ["le fabricant a rendu %d : %s" % (x.returncode, (x.stdout + x.stderr).strip()[-400:])])
        # E1 — sur les emplacements du fabricant du dépôt éprouvé (PROPRIETE), jamais ceux de la copie sabotée ni une
        # liste écrite ici (R-708 ; tests/outils/ ajouté le 01-11-2026) ; un sous-dossier qui est lui-même un
        # emplacement de code (tests/outils/) n'est pas un dossier de données
        for dossier in PROPRIETE.DOSSIERS_DE_CODE:
            for f in os.listdir(os.path.join(r, dossier)):
                src = os.path.join(r, dossier, f)
                dst = os.path.join(pub, dossier, f)
                if os.path.isdir(src):
                    if dossier and os.path.exists(dst) and dossier + "/" + f not in PROPRIETE.DOSSIERS_DE_CODE:
                        fautes.append(f"E1 un dossier de données est publié : {dossier}/{f}")
                    continue
                if not dossier and not f.endswith(".py"):
                    continue
                code = f.endswith(".py") or dossier + "/" + f == "tests/LANCEMENT_DES_EPREUVES.json"
                if code and (not os.path.isfile(dst) or open(src, "rb").read() != open(dst, "rb").read()):
                    fautes.append(f"E1 code absent ou différent : {(dossier + '/') if dossier else ''}{f}")
                if not code and os.path.exists(dst):
                    fautes.append(f"E1 donnée publiée : {(dossier + '/') if dossier else ''}{f}")
        # E1 bis — chaque fiche de circuit du privé arrive, identique, sous circuits_du_prive/, et nulle part ailleurs
        for f in os.listdir(os.path.join(r, ".github", "workflows")):
            if f.endswith((".yml", ".yaml")):
                src, dst = os.path.join(r, ".github", "workflows", f), os.path.join(pub, "circuits_du_prive", f)
                if not os.path.isfile(dst) or open(src, "rb").read() != open(dst, "rb").read():
                    fautes.append(f"E1 fiche de circuit absente ou différente : circuits_du_prive/{f}")
        # E2
        for f in ("programmes/SEULEMENT_AU_PUBLIC.py", "tests/SEULEMENT_AU_PUBLIC.py"):
            if os.path.exists(os.path.join(pub, f)):
                fautes.append("E2 non retiré : " + f)
        # E3
        if not os.path.isfile(os.path.join(pub, CERT)):
            return False, "E3 circuit de certification absent"
        cert = open(os.path.join(pub, CERT), encoding="utf-8").read()
        soir = open(os.path.join(pub, SOIR), encoding="utf-8").read()
        y = yaml.safe_load(cert)
        decl = y.get("on", y.get(True)) or {}
        ouverts = [k for k in ("pull_request", "pull_request_target", "issue_comment", "workflow_run") if k in decl]
        if ouverts:
            fautes.append("E3 déclencheur ouvert aux inconnus : " + ", ".join(ouverts))
        # E3 bis — aucun pas qui tourne après un échec n'exécute le code du privé : son « if » exige le code posé. Jugé
        # par LA propriété du fabricant du dépôt éprouvé, sur tous les jobs ; seuls les pas `shell: bash` sont exemptés.
        for nom, texte, pose in (("certification", cert, "poser_le_code"), ("soir", soir, "poser_les_programmes")):
            for job, contenu in (yaml.safe_load(texte).get("jobs") or {}).items():
                for p_ in ((contenu or {}).get("steps") or []):
                    if p_.get("shell") != "bash" and not PROPRIETE.condition_exige_le_code_pose(str(p_.get("if", "")), pose):
                        fautes.append(f"E3 {nom} : le pas « {p_.get('id')} » du job « {job} » peut tourner sur un code non posé")
        # E3 ter — la propriété dit vrai sur des cas connus
        for cond, pose, attendu in CALIBRATION:
            if PROPRIETE.condition_exige_le_code_pose(cond, pose) != attendu:
                fautes.append(f"E3 calibration : « {cond} » ({pose}) jugé {not attendu}, attendu {attendu}")
        # E3 quater — LA SECONDE LECTURE, PAR YAML, ICI ET PAS DANS LE FABRICANT (superviseur R-759, second tour, R3 ③ :
        # le fabricant tourne sans yaml ; l'épreuve l'exige). Sur ce que le fabricant a accepté — le circuit privé de
        # la copie — et sur les deux circuits qu'il a fabriqués, la liste blanche du dépôt éprouvé
        # (`conditions_du_circuit`) et yaml trouvent les mêmes conditions de job (colonne 4) et de pas (colonne 8).
        # UN ÉTALONNAGE, PAS UN ARBITRE (superviseur R-759, troisième tour, ③5) : PyYAML n'est pas le lecteur de GitHub
        # (il lit `on` comme True) ; un accord ne prouve pas l'accord avec GitHub, un désaccord ne prouve pas un trou.
        for nom, texte in (("privé", open(os.path.join(r, CIRC), encoding="utf-8").read()), ("soir", soir), ("certification", cert)):
            try:
                par_liste = sorted((c, v) for _, c, v in PROPRIETE.conditions_du_circuit(texte))
            except ValueError as e:
                fautes.append(f"E3 quater {nom} : la liste blanche refuse un texte que le fabricant a accepté ({e})")
                continue
            par_yaml = []
            for job, contenu in (yaml.safe_load(texte).get("jobs") or {}).items():
                contenu = contenu or {}
                if "if" in contenu:
                    par_yaml.append((PROPRIETE.COLONNE_JOB, contenu["if"]))
                par_yaml += [(PROPRIETE.COLONNE_PAS, p_["if"]) for p_ in (contenu.get("steps") or []) if "if" in p_]
            par_yaml = sorted((c, str(v).lower() if isinstance(v, bool) else str(v)) for c, v in par_yaml)
            if par_liste != par_yaml:
                fautes.append(f"E3 quater {nom} : la liste blanche lit {len(par_liste)} condition(s), yaml {len(par_yaml)} ; "
                              f"écart {sorted(set(par_liste) ^ set(par_yaml))[:2]}")
        # E3 quinquies — le fabricant DE LA COPIE refuse chaque forme hors du sous-ensemble (motif « hors du
        # sous-ensemble »). Sans ce contrôle, un fabricant qui saute les lignes incomprises (S60) resterait vert tant
        # que le vrai circuit privé n'en porte aucune.
        _s = _iu.spec_from_file_location("fabricant_de_la_copie_%d" % id(d), os.path.join(r, FAB))
        _f = _iu.module_from_spec(_s)
        _s.loader.exec_module(_f)
        # les formes s'appliquent au circuit privé du DÉPÔT ÉPROUVÉ : une variante (V1…) a déjà changé celui de la copie
        prive_copie = open(os.path.join(DEPOT, CIRC), encoding="utf-8").read()
        for nom, (remplacements, _m) in FORMES_HORS_SOUS_ENSEMBLE.items():
            texte = prive_copie
            for _f_, a, b in remplacements:
                texte = texte.replace(a, b, 1)
            if texte == prive_copie:
                fautes.append(f"E3 quinquies {nom} : forme inapplicable au circuit privé du dépôt éprouvé")
                continue
            try:
                _f.fabriquer_le_circuit(texte)
                fautes.append(f"E3 quinquies {nom} : le fabricant de la copie PUBLIE une forme hors du sous-ensemble")
            except ValueError as e:
                if "hors du sous-ensemble" not in str(e):
                    fautes.append(f"E3 quinquies {nom} : refusée pour une autre raison ({str(e)[:80]})")
        # E6 — chaque logiciel que le code publié cherche par shutil.which est vérifié (« command -v ») par un pas
        # placé AVANT la certification. Raison : pdftotext et soffice manquaient à la machine de GitHub, trois
        # épreuves ont rougi au premier certificat public (16-10-2026, f5aac6b). Lu dans le code, jamais listé ici.
        # Lu dans l'arbre syntaxique, pas par un motif : « sh.which(…) », « which(…) » importé seul, une espace dans
        # les parenthèses, un second argument (relecture du 16-10-2026, cassure 7). Un nom qui n'est pas écrit en
        # clair (une variable) est une faute : on ne peut pas savoir quoi installer.
        noms = set()
        for dossier in PROPRIETE.DOSSIERS_DE_CODE:
            for f in os.listdir(os.path.join(r, dossier)):
                if f.endswith(".py") and os.path.isfile(os.path.join(r, dossier, f)):
                    try:
                        arbre = ast.parse(open(os.path.join(r, dossier, f), encoding="utf-8", errors="replace").read())
                    except SyntaxError:
                        continue
                    for n in ast.walk(arbre):
                        if isinstance(n, ast.Call) and (getattr(n.func, "attr", None) == "which"
                                                        or getattr(n.func, "id", None) == "which"):
                            if n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str):
                                noms.add(n.args[0].value)
                            else:
                                fautes.append(f"E6 logiciel cherché par un nom non écrit en clair : {dossier}/{f}, "
                                              f"ligne {n.lineno}")
        etapes = y.get("jobs", {}).get("certifier", {}).get("steps") or []
        rang = next((k for k, p_ in enumerate(etapes) if p_.get("id") == "certifier"), None)
        if rang is None:
            fautes.append("E6 pas « certifier » introuvable")
        else:
            avant = "\n".join(str(p_.get("run", "")) for p_ in etapes[:rang])
            for n in sorted(noms):
                if not re.search(r"command -v %s\b" % re.escape(n), avant):
                    fautes.append(f"E6 logiciel non vérifié avant la certification : {n}")
            # E6 bis — chaque paquet Python qu'installe la certification PRIVÉE (les « pip install » de
            # .github/workflows/certifier.yml, lus dans le fichier, jamais listés ici) est installé, écrit de même
            # (version comprise), avant le pas « certifier » du job fabriqué. Raison : pyflakes manquait au public,
            # l'épreuve E12 des frais y a rougi au certificat du 31-10-2026 (7980a86 ; relecture de Cowork du
            # 31-10-2026 à 18h49). Aucun paquet lu au privé est une faute : l'épreuve ne serait verte que par vide.
            prives = set()
            try:
                for _job in (yaml.safe_load(open(os.path.join(r, CERT_PRIVE), encoding="utf-8")).get("jobs") or {}).values():
                    for p_ in ((_job or {}).get("steps") or []):
                        prives |= paquets_installes(p_.get("run", ""))
            except (OSError, AttributeError, ValueError, yaml.YAMLError) as e:
                fautes.append(f"E6 bis {CERT_PRIVE} illisible ({type(e).__name__})")
            publics = set()
            for p_ in etapes[:rang]:
                ici = paquets_installes(p_.get("run", ""))
                publics |= ici
                # le TEXTE du pas qui installe ne doit ni le désactiver ni taire son échec (relecture neuve, M2 : un pas
                # désactivé ou « continue-on-error » laissait pyflakes absent) ; un filet sur le texte, pas une preuve
                # d'installation — voir le ⑨ de `paquets_installes`
                if ici and ("if" in p_ or p_.get("continue-on-error") not in (None, False)):
                    fautes.append(f"E6 bis le pas qui installe « {p_.get('id') or p_.get('name')} » peut ne pas tourner "
                                  f"ou échouer sans arrêter le job (if / continue-on-error)")
            if not prives:
                fautes.append(f"E6 bis aucun paquet installé lu dans {CERT_PRIVE}")
            for n in sorted(prives - publics):
                fautes.append(f"E6 bis paquet de la certification privée non installé au public : {n}")
        # E4
        s = pas(cert, "certifier", "poser_le_code")
        if s is None:
            fautes.append("E4 pas « poser_le_code » introuvable")
        else:
            for nom, prep, attendu in (("identique", lambda w: None, 0),
                                       ("programme différent", ecrire("_code/programmes/A.py", "a=9\n"), 1),
                                       ("épreuve seulement au privé", ecrire("tests/U.py", "u=1\n"), 1),
                                       ("épreuve seulement au public", ecrire("_code/tests/U.py", "u=1\n"), 1),
                                       ("programme seulement au privé", ecrire("programmes/C.py", "c=1\n"), 1),
                                       ("lancement différent", ecrire("_code/tests/LANCEMENT_DES_EPREUVES.json", "[]\n"), 1),
                                       ("racine différente", ecrire("_code/emp.py", "e=9\n"), 1),
                                       ("outil différent", ecrire("_code/etudes/outils/O.py", "o=9\n"), 1),
                                       ("outil seulement au privé", ecrire("etudes/outils/P.py", "p=1\n"), 1),
                                       ("outil d'épreuves différent", ecrire("_code/tests/outils/J.py", "j=9\n"), 1),
                                       ("outil d'épreuves seulement au privé", ecrire("tests/outils/K.py", "k=1\n"), 1),
                                       ("lien symbolique", lien_vers_le_prive, 1),
                                       ("programme caché seulement au privé", ecrire("programmes/.cache.py", "c=1\n"), 1),
                                       ("fiche de circuit privée modifiée", ecrire(".github/workflows/F.yml", "pas: 2\n"), 1),
                                       ("fiche seulement au privé", ecrire(".github/workflows/G.yml", "pas: 1\n"), 1),
                                       ("fiche seulement au public", ecrire("_code/circuits_du_prive/G.yml", "pas: 1\n"), 1)):
                c, restes = jouer(s, prep)
                if (c == 0) != (attendu == 0):
                    fautes.append(f"E4 {nom} : code {c}, attendu {'0' if attendu == 0 else 'non nul'}")
                if c == 0 and restes:
                    fautes.append(f"E4 {nom} : après le pas, {', '.join(restes)}")
        # E5 — le pas « poser les programmes » du circuit du soir : vert quand tout est identique ; rouge sur un
        # programme seulement au privé, un programme différent, un sous-dossier de programmes/ (un paquet qui
        # masquerait un module publié, porte T4 du 20-10-2026) et un fichier compilé dans le clone ; quand il passe,
        # le code public est rangé hors du clone et l'environnement du garde est écrit.
        # E7 — le garde du code (programmes/N_EXECUTER_AU_PUBLIC_QUE_LE_CODE_PUBLIE.py), posé par ce pas : le pas « Le garde du code mord-il ? »
        # est vert avec le garde, rouge sans lui et rouge avec un garde dont la porte des imports est morte ; un
        # module publié s'importe (témoin) ; quatre pièges du clone absents de la copie publique (A lancé, B importé,
        # C lancé par un enfant en -I, D .pyc glissé) sont arrêtés (code 97) avant d'avoir rien écrit (portes T1 à
        # T6 du 20-10-2026 ; prototype du superviseur du 21-10-2026).
        s = pas(soir, "collecte", "poser_les_programmes")
        m = pas(soir, "collecte", "garde_du_code")
        garde = open(os.path.join(r, "programmes", "N_EXECUTER_AU_PUBLIC_QUE_LE_CODE_PUBLIE.py"), encoding="utf-8").read() \
            if os.path.isfile(os.path.join(r, "programmes", "N_EXECUTER_AU_PUBLIC_QUE_LE_CODE_PUBLIE.py")) else ""
        if s is None or m is None or not garde:
            fautes.append("E5/E7 pas « poser_les_programmes » ou « garde_du_code », ou programme du garde, introuvable")
        else:
            def sous_dossier(w):
                os.makedirs(os.path.join(w, "programmes", "B"))
                open(os.path.join(w, "programmes", "B", "__init__.py"), "w").write("b=9\n")
            for nom, prep, attendu in (("identique", lambda w: None, 0),
                                       ("programme seulement au privé", ecrire("programmes/C.py", "c=1\n"), 1),
                                       ("programme différent", ecrire("_code/programmes/A.py", "a=9\n"), 1),
                                       ("sous-dossier dans programmes/", sous_dossier, 1),
                                       ("fichier compilé dans le clone", ecrire("etudes/X.pyc", "x"), 1)):
                c1, c2, range_, lignes, arrete = jouer_soir(s, m, prep, garde)
                if (c1 == 0) != (attendu == 0):
                    fautes.append(f"E5 {nom} : code {c1}, attendu {'0' if attendu == 0 else 'non nul'}")
                if attendu == 0 and c1 == 0:
                    if not range_:
                        fautes.append("E5 le code public n'est pas rangé hors du clone, ou _code reste")
                    for v in ("PYTHONPATH=", "PYTHONDONTWRITEBYTECODE=1", "GARDE_DONNEES=", "GARDE_CODE="):
                        if not any(l.startswith(v) for l in lignes):
                            fautes.append(f"E5 environnement du garde incomplet : {v} manque")
                    if c2[0] != 0:
                        fautes.append(f"E7 le pas « Le garde du code mord-il ? » rend {c2[0]}, attendu 0")
                    if c2[1] == 0:
                        fautes.append("E7 le pas « Le garde du code mord-il ? » reste vert SANS le garde : il ne prouve rien")
                    if c2[2] is None:
                        fautes.append("E7 garde mutant inapplicable : ancre de la porte « exec » absente")
                    elif c2[2] == 0:
                        fautes.append("E7 le pas « Le garde du code mord-il ? » reste vert avec la porte des imports morte")
                    for f_ in arrete:
                        fautes.append("E7 " + f_)
        return not fautes, ("; ".join(fautes[:4]) if fautes else "E1 à E9 conformes")
    finally:
        shutil.rmtree(d, ignore_errors=True)


def numeros_en_double(noms):
    """Rend les numéros de cas portés par plus d'un nom de SABOTAGES.

    ① RÔLE — Garder la convention « un numéro, un cas » des sabotages de cette épreuve.
    ② CONTEXTE D'APPEL — `main`, une fois, avant de jouer quoi que ce soit.
    ③ ENTRÉE — `noms` : les clés de SABOTAGES (« S122_series_sans_garde_des_parts », « V6_… »).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste triée des préfixes en double (« S110 »…), vide si chaque numéro est unique.
      [rend: 1]
    ⑥ TRAITEMENT — le préfixe d'un nom est sa lettre et ses chiffres de tête (« S110 », « V6 ») ; compter.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Étude du 05-11-2026 (github_series/RAPPORT.md, §1.2) : le patch du filet des gabarits, régénéré sur
      la version B, reprenait S110 à S121, déjà pris par la réparation M5 : 12 numéros en double, sans rien qui le
      signale (les noms complets restaient distincts). Les numéros nouveaux se prennent par programme au premier libre,
      1 + le plus grand pris (un numéro retiré n'est pas repris : d'anciens relevés le citent) ; ce contrôle rend la
      convention vérifiée au lieu de supposée.
    ⑨ CE QUI CLOCHE — Un nom sans lettre ni chiffre de tête (« Z0 ») n'a pas de numéro et n'est pas compté.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    vus = {}
    for n in noms:
        m = re.match(r"([A-Z]\d+)_", n)
        if m:
            vus[m.group(1)] = vus.get(m.group(1), 0) + 1
    return sorted(k for k, v in vus.items() if v > 1)


def main():
    """Joue Z0, et chaque sabotage avec --saboter ; affiche ; rend le code de sortie.

    ① RÔLE — Voir la fiche du fichier.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — `sys.argv`.
    ④ CONDITIONS D'ENTRÉE — Voir la fiche du fichier.
    ⑤ SORTIE — UNE valeur : le code de sortie.
      [rend: 1]
    ⑥ TRAITEMENT — Refuser (code 2) si deux sabotages portent le même numéro (`numeros_en_double`) ; puis voir la
      fiche du fichier.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir la fiche du fichier.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    doubles = numeros_en_double(SABOTAGES)
    if doubles:
        print("ARRÊT : numéros de sabotages en double :", ", ".join(doubles), "(prendre le premier libre)")
        return 2
    choix = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
    code = 0
    for sab in choix:
        ok, det = epreuve(sab)
        if ok is None:
            print(f"== {sab} : INAPPLICABLE · {det}")
            code = 2
            continue
        vert_attendu = sab == "Z0" or sab.startswith("V")
        bon = ok if vert_attendu else not ok
        if bon and not ok and sab in MOTIFS_ATTENDUS and MOTIFS_ATTENDUS[sab] not in det:
            bon = False
            det = f"ROUGE POUR UNE AUTRE RAISON (attendu : « {MOTIFS_ATTENDUS[sab]} ») · {det}"
        print(f"== {sab} : {'vert' if ok else 'rouge'} {'(attendu)' if bon else '<-- ' + ('ATTENDU VERT' if vert_attendu else 'SABOTAGE SANS EFFET')} · {det}")
        if not bon:
            code = max(code, 1)
    print("VERDICT : " + ("tout est conforme" if code == 0 else f"NON CONFORME (code {code})"))
    return code


if __name__ == "__main__":
    sys.exit(main())
