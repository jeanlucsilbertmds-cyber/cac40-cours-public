#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GIT_SANS_LA_MACHINE.py — Dim 15-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.
EN ESSAI · outil d'épreuve · Rôle : rendre les dépôts git JETABLES des épreuves indépendants du réglage git de la
machine qui les rejoue (étape MIN du plan V7, A-751 ⑤, défaut RF-2 relevé par Cowork le 13-11-2026 ; tour 2 du
15-11-2026 : défaut 5/N-1 de la relecture de Cowork, le réglage passé par l'ENVIRONNEMENT n'était pas neutralisé).

LE SENS, EN TÊTE. Plusieurs épreuves fabriquent des dépôts git dans /tmp et y commitent. Sans précaution, chaque
`git commit` lit le réglage global de la machine (`~/.gitconfig`). Cas survenu le 13-11-2026 chez Cowork : une
machine dont le réglage global SIGNE chaque commit par un service réseau ; réseau coupé, chaque commit jetable échoue
(B du bloc 5A : R5, R6, D4 rouges ; B3 : relance illisible), et le garde-fou de livraison appelle cela « SORTIE
FABRIQUÉE » — il accuse l'auteur alors que la cause est la machine. La machine du Chat porte le même réglage
(`commit.gpgsign=true`, lu le 15-11-2026). Une épreuve dont le verdict dépend de la machine ne prouve rien.

USAGE (depuis une épreuve, avant tout appel à git, y compris les sous-processus qu'elle lance) :
    import importlib.util
    _sp = importlib.util.spec_from_file_location("GIT_SANS_LA_MACHINE", os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "outils", "GIT_SANS_LA_MACHINE.py"))
    _gsm = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_gsm); _gsm.isoler_git_de_la_machine()
"""
import atexit
import importlib.util
import os
import shutil
import tempfile

# Le réglage global de remplacement : une identité d'épreuve et AUCUNE signature. Rien d'autre — en particulier pas
# de branche par défaut : une épreuve qui fait `git init` sans `-b` garde le défaut de git, comme avant.
REGLAGE_DES_EPREUVES = ("[user]\n\tname = epreuve\n\temail = epreuve@epreuve.invalid\n"
                        "[commit]\n\tgpgsign = false\n[tag]\n\tgpgsign = false\n")


def _variables_de_certifier():
    """Lit, dans `programmes/CERTIFIER_LA_VERSION.py`, la liste des variables qui retirent à git le réglage de la machine.

    ① RÔLE — Rendre LA définition unique de « git sans la configuration de la machine » :
      `CERTIFIER_LA_VERSION.SANS_LA_CONFIGURATION_GIT_DE_LA_MACHINE`.
    ② CONTEXTE D'APPEL — `isoler_git_de_la_machine`, une fois par appel.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — Ce fichier est à sa place, `tests/outils/` sous la racine du dépôt, et
      `programmes/CERTIFIER_LA_VERSION.py` existe sous la même racine.
    ⑤ SORTIE — UNE valeur : une copie du dictionnaire {nom de variable : valeur}.
      [rend: 1]
    ⑥ TRAITEMENT — ① remonter de deux dossiers depuis ce fichier · ② charger CERTIFIER comme module (sous un nom
      propre à cet outil, pour ne pas remplacer un CERTIFIER déjà chargé par l'appelant) · ③ copier sa constante.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Deux définitions d'une même chose divergent toujours (R-708) : la première version de cet outil
      (15-11-2026, 13h24) en écrivait une deuxième, qui avait déjà divergé — GLOBAL et NOSYSTEM seulement, sans
      `GIT_CONFIG_COUNT` ni `GIT_CONFIG_PARAMETERS`, que CERTIFIER neutralise depuis la cassure du 17-10-2026
      (« GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign faisait encore refuser un commit »). Relu par Cowork le
      15-11-2026 (RELU 5/N-1), mesuré : B3 réparé rougissait sous une signature passée par `GIT_CONFIG_COUNT`.
    ⑨ CE QUI CLOCHE — ① Charger CERTIFIER exécute le haut de ce programme (des imports de la bibliothèque standard et
      des définitions ; aucun effet mesuré) à chaque épreuve qui appelle l'outil. ② Un CERTIFIER introuvable fait
      lever l'outil, donc tomber l'épreuve qui l'appelle : voulu (R-734), plutôt qu'une isolation partielle muette.
    ⑩ EFFET — Lit un fichier ; n'écrit rien.
    ⑪ TERMINAISON — Rend la main ; lève OSError ou AttributeError si CERTIFIER ou sa constante manque. Aucun de ses
      appels ne peut ne pas revenir.
      [sort: non]
    """
    racine = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sp = importlib.util.spec_from_file_location("CERTIFIER_LA_VERSION_vu_par_GIT_SANS_LA_MACHINE",
                                                os.path.join(racine, "programmes", "CERTIFIER_LA_VERSION.py"))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return dict(m.SANS_LA_CONFIGURATION_GIT_DE_LA_MACHINE)


def isoler_git_de_la_machine():
    """Remplace, pour ce processus et tous ceux qu'il lance, le réglage git global par celui des épreuves.

    ① RÔLE — Que git, appelé par une épreuve ou par un programme qu'elle lance, ne lise plus AUCUN réglage de la
      machine — ni `~/.gitconfig`, ni le réglage du système, ni les variables `GIT_CONFIG_COUNT`/`GIT_CONFIG_KEY_n`,
      ni `GIT_CONFIG_PARAMETERS` — mais un réglage écrit ici : identité d'épreuve, aucune signature.
    ② CONTEXTE D'APPEL — Le haut de `tests/EPREUVES_B_DU_BLOC_5A_Mer_11-11-2026.py`,
      `tests/EPREUVES_B3_DECLARATION_Mer_11-11-2026.py`, `tests/EPREUVES_J_PORTE_D_ENTREE_Mer_11-11-2026.py` et
      (tour 2, RELU 1/N-2) `tests/EPREUVES_DU_REGARD_UNIQUE_Jeu_12-11-2026.py`, une fois par processus, juste après
      leurs imports (étape MIN, 15-11-2026) ; et `tests/EPREUVES_DE_GIT_SANS_LA_MACHINE_Dim_15-11-2026.py`, qui
      l'éprouve. L'appel se fait À L'IMPORT de ces épreuves : une épreuve qui en CHARGE une autre (J charge le bloc
      5A ; REGARD charge J et le bloc 5A) hérite de l'isolement — c'est pourquoi chacune l'appelle elle-même, au lieu
      d'en dépendre par accident.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — Être appelée AVANT que l'épreuve ne recopie `os.environ` dans un dictionnaire (`env =
      dict(os.environ, ...)`) : une copie faite avant ne porte pas le remplacement.
    ⑤ SORTIE — UNE valeur : le chemin du réglage écrit.
      [rend: 1]
    ⑥ TRAITEMENT — ① créer un dossier temporaire « git_sans_la_machine_ » sous le dossier temporaire du système ·
      ② y écrire `REGLAGE_DES_EPREUVES` · ③ poser dans `os.environ` (hérité par chaque sous-processus) TOUTES les
      variables de `CERTIFIER_LA_VERSION.SANS_LA_CONFIGURATION_GIT_DE_LA_MACHINE` (`_variables_de_certifier`), puis
      remplacer `GIT_CONFIG_GLOBAL` par ce fichier · ④ inscrire l'effacement du dossier à la sortie du processus.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le réglage global a la priorité la plus BASSE après celui du système : le réglage d'un dépôt
      (`git config user.email` dans l'épreuve J) et les variables `GIT_AUTHOR_*` (B du bloc 5A, B3) passent
      toujours devant, comme avant. Une option `-c commit.gpgsign=false` sur chaque commit aurait été une ÉNUMÉRATION
      (dix-huit appels dans le seul bloc 5A, plus ceux des programmes éprouvés) ; la variable couvre tout git lancé
      sous le processus, par une propriété. La LISTE des variables vient de CERTIFIER et n'est pas recopiée (R-708) :
      la recopier avait fait oublier `GIT_CONFIG_COUNT` et `GIT_CONFIG_PARAMETERS` (RELU 5/N-1, 15-11-2026).
    ⑨ CE QUI CLOCHE — ① Quatre épreuves l'appellent le 15-11-2026 (② ci-dessus) ; trois autres commitent dans des
      dépôts jetables sans neutraliser la signature (B2 du registre des essais, la boucle de check, le comblement ;
      relevé dans echanges/A_RELIRE.md, passe ②) : à consigner, pas corrigé ici. ② Le garde-fou de livraison ne distingue toujours pas « l'épreuve n'a pas pu
      tourner » de « sortie différente » (seconde moitié de RF-2) : à consigner. ③ Un réglage global qui servirait
      à joindre le réseau (identifiants) n'est plus lu : aucune des trois épreuves ne joint le réseau (recherche de
      « https », « github » et « ls-remote » dans les trois fichiers le 15-11-2026 : zéro). Le registre des essais
      GARDE `GIT_CONFIG_COUNT` pour pousser ses regards (`insteadOf`, identification) : sous l'outil, cette poussée ne
      vise que des dépôts nus LOCAUX fabriqués par les épreuves — les quatre appelantes rejouées vertes le 15-11-2026
      (echanges/A_RELIRE.md). ④ Le réglage `safe.directory` de la machine n'est plus lu non plus : une épreuve
      rejouée sur un clone appartenant à un autre utilisateur verrait git refuser ce clone (« dubious ownership »).
      THÉORIQUE, non mesuré (RELU 5/N-5) ; à consigner. ⑤ L'isolement est posé À L'IMPORT et pour tout le processus :
      une épreuve qui charge une épreuve appelante en hérite (②).
    ⑩ EFFET — Écrit un fichier temporaire ; modifie `os.environ` du processus.
    ⑪ TERMINAISON — Rend la main ; lève OSError si le dossier temporaire ne s'écrit pas. Aucun de ses appels ne
      peut ne pas revenir.
      [sort: non]
    """
    d = tempfile.mkdtemp(prefix="git_sans_la_machine_")
    f = os.path.join(d, "gitconfig")
    with open(f, "w", encoding="utf-8") as h:
        h.write(REGLAGE_DES_EPREUVES)
    os.environ.update(_variables_de_certifier())
    os.environ["GIT_CONFIG_GLOBAL"] = f
    atexit.register(shutil.rmtree, d, True)
    return f
