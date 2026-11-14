#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_UN_IDENTIFIANT_UNE_EMPREINTE — Sam 14-11-2026 (Paris). Lot CARNET, partie 1. SIMULATION UNIQUEMENT.

À QUOI ÇA SERT, EN FRANÇAIS SIMPLE. Jean-Luc a décidé, le 13-11-2026 à 16h30 (BACKLOG A-754) : « s'il y a un
changement de paramètre, une stratégie […] c'est une autre stratégie » — et l'a redit le 14-11 : passer le stop de
1 % à 2 %, c'est une NOUVELLE stratégie. Le 14-11-2026 à 11h48 (« Oui, ok. Je suis d'accord », BACKLOG A-768) : ①
l'identifiant d'une stratégie reste la colonne `id` du registre des stratégies, jamais réutilisé ni renommé, et un
réglage changé demande un nouvel identifiant ; ② un programme calcule une EMPREINTE DES RÉGLAGES, et le contrôle est
« même identifiant ⇒ même empreinte, sinon rouge ». Cette épreuve est ce contrôle. L'empreinte est
`empreinte_des_reglages` (programmes/JUGE_DES_STRATEGIES.py), construite sur `lecture_de_jeu`, la seule définition de
« ce qui change un calcul » (R-708 : deux définitions d'une même chose divergent toujours). Elle regarde DEUX choses,
parce qu'un réglage peut changer de deux façons : par une LIGNE AJOUTÉE sous le même identifiant (le registre du
jour le montre), ou par une ligne RÉÉCRITE SUR PLACE (seule l'histoire du dépôt le montre — superviseur R-759 du
14-11-2026, fait F10 : IND-001-RETEST a été rempli sur place le 11-11-2026, et un contrôle qui ne compare que les
lignes présentes ne le voit pas).

UNE RÉSERVE, QUI REVIENT À JEAN-LUC. Dans l'histoire, une fiche REFUSÉE (incomplète : le juge ne peut pas la jouer)
qu'on complète sur place change d'empreinte. C'est la question ⑥ du superviseur R-759 du 14-11-2026 : « Compléter sur
place une fiche qui n'a jamais été jouée ni jugée est-il permis, ou faut-il un nouvel identifiant ? ». Tant qu'elle
n'est pas tranchée, l'épreuve ne rougit PAS sur une complétion : elle la NOMME (« COMPLÉTIONS — question ⑥ »). Elle
rougit sur tout changement d'empreinte d'une ligne qui était JOUABLE : sur ce cas-là, les deux réponses possibles à
la question ⑥ disent « autre stratégie ». Si Jean-Luc répond « nouvel identifiant », une condition change dans
`histoire_du_registre` (voir son ⑨) et l'épreuve rougit aussitôt sur les fiches nommées.

LES CAS, JOUÉS DANS UNE COPIE DU DÉPÔT (sans .git) ; l'histoire est lue en lecture seule dans le dépôt donné :
  U1 le vrai registre du commit courant (R-732) : pour chaque identifiant, une seule empreinte ; et
     `versions_du_registre` rend 1 pour chaque identifiant (la propriété citée par le superviseur, R2) ; les deux
     relevés s'accordent.
  U2 des registres fabriqués à partir de VRAIES lignes : la ligne 70 de C5-EI-PARAMS recopiée sous le même
     identifiant avec un tp de +9,0 % (le cas de l'épreuve E5 de la branche v7-E4) puis avec un stop de −1,0 % →
     rouge sur C5-EI-PARAMS, et sur lui seul ; la dernière ligne de MA200-S1 recopiée avec une note changée, et la
     ligne de C5-EI-PARAMS recopiée avec une entrée vide → aucun rouge (cas qui doivent échouer à rougir).
  U3 la vraie histoire de la branche principale : aucun changement d'empreinte d'une ligne jouable ; les complétions
     sont nommées.
  U4 une histoire fabriquée dans un dépôt git jetable, avec de vraies lignes : une réécriture sur place du tp d'une
     ligne jouable → rouge ; une note changée → rien ; une fiche refusée complétée → complétion nommée ; une branche
     HEAD propre posée à côté → ignorée (l'histoire se lit sur la branche principale, jamais sur HEAD).
  U5 l'empreinte ne dépend pas du lancement : calculée sous deux graines de hachage, elle est identique, alors que
     l'écriture brute de la lecture (`repr`) diffère — ce qui prouve que le cas a des dents.
  U6 un dépôt superficiel (sans histoire) rend INCONNU, jamais « aucune réécriture » (R-734).

USAGE : python3 -B tests/EPREUVES_UN_IDENTIFIANT_UNE_EMPREINTE_Sam_14-11-2026.py <racine> [--saboter | nom]
  sans option : Z0, le dépôt tel quel ; --saboter : Z0 puis chaque sabotage ; un nom de sabotage : celui-là seul.
CODE : 0 si Z0 est tout vert et que chaque sabotage joué fait rougir au moins un cas ; 1 sinon ; 2 si la racine est
inutilisable, si son histoire est illisible (dépôt superficiel, branche principale absente : les seuls cas rouges de
Z0 disent INCONNU), si une cible de sabotage est introuvable ou si le nom demandé n'existe pas (R-734 : un contrôle
qui n'a pas pu tourner ne rend pas 0).

① RÔLE — Voir « À QUOI ÇA SERT ».
② CONTEXTE D'APPEL — À la main ; et par la vérification de version (programmes/CERTIFIER_LA_VERSION.py), qui lance
  chaque épreuve de tests/ depuis la racine avec la racine en argument, et avec `--saboter` (elle la trouve seule :
  aucune déclaration à ajouter). Ce programme se relance lui-même avec « --cas <copie> <dépôt> » pour jouer les cas
  dans une copie : ce mode n'est pas fait pour la main.
③ ENTRÉE — La racine d'un dépôt git complet (pas superficiel) qui porte la branche principale du contrat ;
  `--saboter` ou un nom de sabotage, facultatif.
④ CONDITIONS D'ENTRÉE — Sous la racine : programmes/JUGE_DES_STRATEGIES.py (avec `empreinte_des_reglages`,
  `versions_du_registre`), programmes/CONTRATS_DES_FICHIERS.py (REGISTRE_DES_STRATEGIES, BRANCHE_PRINCIPALE,
  `lignes_du_registre`, `lignes_du_registre_pour_compter_k`), programmes/TENIR_LE_REGISTRE_DES_ESSAIS.py (`git_de`),
  le registre des stratégies ; `git` installé.
⑤ SORTIE — Le code de sortie dit en « CODE » ; une ligne par cas et par sabotage. [rend: 1]
⑥ TRAITEMENT — Pour Z0 puis chaque sabotage : ① copier la racine dans un dossier temporaire (sans .git, etudes,
  caches) · ② appliquer le sabotage à la copie (remplacer un texte qui doit y être une fois) · ③ relancer la copie
  de ce programme en mode « --cas » · ④ Z0 doit être vert, un sabotage doit faire échouer au moins un cas.
⑦ UNITÉ — Des lignes du registre, des identifiants, des empreintes (16 caractères hexadécimaux), des commits.
⑧ POURQUOI — Décisions de Jean-Luc du 13-11-2026 à 16h30 et du 14-11-2026 à 11h48 (voir plus haut). Superviseur
  R-759 du 14-11-2026, R2 : « La propriété est déjà calculable : pour chaque identifiant, `versions_du_registre`
  rend 1 […] Il manque […] comparer aussi dans L'HISTOIRE de main ».
⑨ CE QUI CLOCHE — ① Les modules de signal sont pris au jour pour TOUTE l'histoire : un module corrigé ne change
  donc aucune empreinte ici (question ⑤ du superviseur, à Jean-Luc ; F11). ② L'histoire est lue en ordre
  topologique sur tous les commits de la branche principale qui touchent le registre : si deux branches fusionnées
  avaient changé le MÊME identifiant en parallèle, l'ordre entre elles serait arbitraire. ③ Une ligne SUPPRIMÉE du
  registre n'est pas vue ici (ce n'est pas un changement d'empreinte ; R-727 l'interdit ailleurs). ④ Les lignes
  sont lues dans l'histoire avec le CODE du jour (`lecture_de_jeu` d'aujourd'hui sur les octets d'hier) : c'est
  voulu — « même empreinte » veut dire « le juge d'aujourd'hui calculerait la même chose ». ⑤ La réserve de la
  question ⑥ (voir plus haut) laisse passer, en vert, une complétion sur place ; elle est nommée, pas cachée.
⑩ EFFET — Crée et efface des dossiers temporaires ; lance `git` (lecture seule sur la racine) et `python3`.
  N'écrit rien sous la racine.
⑪ TERMINAISON — Sort du programme. Un appel à `git` peut ne pas revenir (aucun délai posé) ; chaque relance de la
  copie a un délai de DELAI secondes.
  [sort: oui]
"""
import ast
import csv
import hashlib
import io
import os
import shutil
import subprocess
import sys
import tempfile
import time

SOI = os.path.join("tests", os.path.basename(__file__))
JUGE = os.path.join("programmes", "JUGE_DES_STRATEGIES.py")
DELAI = 600          # secondes, pour chaque relance de la copie
NOMBRE_DE_CAS = 11   # U1 à U11 ; le marqueur de fin le vérifie
JOUER = os.path.join("programmes", "JOUER_LES_VERSIONS.py")
COMBINATOIRE_REELLE = os.path.join("donnees", "combinatoires", "COMBINATOIRE_C5E10-OBS-V1_E01.csv")
# Le commit de main SUR LEQUEL U9 SE CALIBRE : il porte encore la seconde définition (TRIER_LES_VARIANTES.py, l.414,
# « def empreinte_des_reglages(ligne, jouer) »), que le relecteur neuf du 14-11-2026 a trouvée (D2).
AVANT_LA_REPARATION = "431b8c86"
LIGNE_DU_HACHAGE = "    texte = json.dumps(canonique(lue), ensure_ascii=False, sort_keys=True)\n"


def charger(racine):
    """Charge le juge, le contrat et le teneur du registre des essais de la racine.
    ① RÔLE — importer le code ÉPROUVÉ (celui de la copie), pas un autre.
    ② CONTEXTE D'APPEL — `cas`, une fois.
    ③ ENTRÉE — `racine` : la copie éprouvée.
    ④ CONDITIONS D'ENTRÉE — `programmes/` y est.
    ⑤ SORTIE — TROIS valeurs : le juge, le contrat, le teneur du registre des essais (pour `git_de`).
    [rend: 3]
    ⑥ TRAITEMENT — mettre `programmes/` en tête du chemin, importer.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — le lanceur git unique vit chez le teneur du registre des essais (R-708) : on le réutilise.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — exécute le chargement des trois modules.
    ⑪ TERMINAISON — Rend la main, ou lève (rattrapé par `un`, qui fait rougir).
    [sort: non]"""
    sys.path.insert(0, os.path.join(racine, "programmes"))
    import JUGE_DES_STRATEGIES as J
    import CONTRATS_DES_FICHIERS as C
    import TENIR_LE_REGISTRE_DES_ESSAIS as T
    return J, C, T


def module_du_jour(racine):
    """Rend la fonction qui donne l'empreinte d'un module de signal tel qu'il est AUJOURD'HUI dans `racine`.
    ① RÔLE — fournir l'octet du module à `empreinte_des_reglages`.
    ② CONTEXTE D'APPEL — `cas`.
    ③ ENTRÉE — `racine` : la racine dont on lit les modules.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : une fonction (chemin, rang=None) → 16 caractères hexadécimaux, ou None si le module
      n'existe pas.
    [rend: 1]
    ⑥ TRAITEMENT — sha256 du fichier, seize premiers caractères.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — le module du jour pour toute l'histoire : voir le ⑨ ① du programme.
    ⑨ CE QUI CLOCHE — voir le ⑨ ① du programme.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
    [sort: non]"""
    def lire(chemin, rang=None):
        """Empreinte du module du jour.
        ① RÔLE — lire un module. ② CONTEXTE D'APPEL — le juge. ③ ENTRÉE — `chemin` : le module · `rang` : ignoré.
        ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur. [rend: 1] ⑥ TRAITEMENT — sha256. ⑦ UNITÉ — —
        ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — — ⑩ EFFET — lit un fichier. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        p = os.path.join(racine, chemin)
        return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16] if os.path.isfile(p) else None
    return lire


def empreintes_par_identifiant(J, lignes, lire):
    """Rend, pour chaque identifiant d'un registre, ses empreintes distinctes dans l'ordre, et ceux qui en ont plus d'une.

    ① RÔLE — Le contrôle « même identifiant ⇒ même empreinte » sur UN état du registre (point ② de la décision de
      Jean-Luc du 14-11-2026 à 11h48).
    ② CONTEXTE D'APPEL — U1, U2, et `histoire_du_registre` pour chaque commit.
    ③ ENTRÉE — `J` : le juge · `lignes` : les lignes du registre, dans l'ordre du fichier (dictionnaires) · `lire` :
      la fonction de `module_du_jour`.
    ④ CONDITIONS D'ENTRÉE — Chaque ligne porte `id`.
    ⑤ SORTIE — DEUX valeurs : un dictionnaire {identifiant : liste de (empreinte, jouable), distinctes, dans l'ordre
      d'apparition} et la liste triée des identifiants qui ont plus d'une empreinte.
    [rend: 2]
    ⑥ TRAITEMENT — `empreinte_des_reglages` sur chaque ligne ; une paire déjà vue pour l'identifiant n'est pas
      reprise.
    ⑦ UNITÉ — Des empreintes de 16 caractères hexadécimaux.
    ⑧ POURQUOI — Une suite A → B → A sous un même identifiant rougit ici (deux empreintes distinctes), comme elle
      compte trois versions chez `versions_du_registre` : les deux relevés rougissent ensemble.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui de `lire`.
    ⑪ TERMINAISON — Rend la main ; lève si le juge lève.
    [sort: non]"""
    par_id = {}
    for ligne in lignes:
        paire = J.empreinte_des_reglages(ligne, lire)
        vues = par_id.setdefault(ligne["id"], [])
        if paire not in vues:
            vues.append(paire)
    return par_id, sorted(i for i, v in par_id.items() if len({e for e, _ in v}) > 1)


def histoire_du_registre(J, C, T, depot, lire):
    """Relève, sur la branche principale du dépôt, chaque changement d'empreinte d'un identifiant d'un commit à l'autre.

    ① RÔLE — Voir une RÉÉCRITURE SUR PLACE d'un réglage, que le registre du jour ne montre pas (superviseur R-759 du
      14-11-2026, F10 et R2 : « comparer aussi dans L'HISTOIRE de main »).
    ② CONTEXTE D'APPEL — U3 (le vrai dépôt), U4 et U6 (dépôts jetables).
    ③ ENTRÉE — `J`, `C`, `T` : le juge, le contrat, le teneur du registre des essais · `depot` : un dépôt git ·
      `lire` : la fonction de `module_du_jour`.
    ④ CONDITIONS D'ENTRÉE — Le dépôt porte la branche principale du contrat (`C.BRANCHE_PRINCIPALE`) et n'est pas
      superficiel ; sinon INCONNU.
    ⑤ SORTIE — QUATRE valeurs : les RÉÉCRITURES (liste de (identifiant, commit d'avant, commit d'après) où une ligne
      JOUABLE a changé d'empreinte, ou où un même commit porte deux empreintes pour un identifiant), les COMPLÉTIONS
      (même forme, où la ligne d'avant était REFUSÉE), le nombre de commits lus, et la raison d'INCONNU (texte vide si
      l'histoire a été lue ; les trois premières valeurs sont alors None).
    [rend: 4]
    ⑥ TRAITEMENT — ① la branche existe (`git rev-parse --verify`) · ② le dépôt n'est pas superficiel · ③ les commits
      de la branche qui touchent le registre, du plus ancien au plus récent (`git rev-list --reverse --topo-order`) ·
      ④ pour chacun : le registre à ce commit (`git show`, puis `lignes_du_registre_pour_compter_k` du contrat),
      `empreintes_par_identifiant` · ⑤ pour chaque identifiant, comparer sa dernière empreinte à celle du commit
      précédent où il figurait : différente et JOUABLE avant → réécriture ; différente et REFUSÉE avant → complétion.
    ⑦ UNITÉ — Des commits (8 premiers caractères), des identifiants.
    ⑧ POURQUOI — k_a_la_date lit déjà le registre à une date par la branche principale et jamais par HEAD (superviseur
      J du 12-11-2026, réponse 3b : un commit antidaté posé au-dessus de la branche choisissait le registre) ; la même
      branche est lue ici, par le même lanceur git (`T.git_de`).
    ⑨ CE QUI CLOCHE — ① LA RÉSERVE DE LA QUESTION ⑥ VIT DANS LA CONDITION « jouable_avant » : si Jean-Luc répond qu'une
      fiche complétée doit changer d'identifiant, cette condition tombe et toute complétion devient une réécriture.
      ② Voir le ⑨ du programme, points ① à ④.
    ⑩ EFFET — Lance `git` en lecture seule.
    ⑪ TERMINAISON — Rend la main ; un appel à `git` peut ne pas revenir.
    [sort: non]"""
    git = T.git_de(depot)
    branche = C.BRANCHE_PRINCIPALE
    code, _ = git("rev-parse", "--verify", "--quiet", branche + "^{commit}")
    if code != 0:
        return None, None, None, "branche principale %s absente du dépôt — l'histoire ne se lit que sur elle" % branche
    code, sortie = git("rev-parse", "--is-shallow-repository")
    if code != 0 or sortie.strip() != b"false":
        return None, None, None, "dépôt superficiel ou illisible : l'histoire n'est pas lisible"
    code, sortie = git("rev-list", "--reverse", "--topo-order", branche, "--", C.REGISTRE_DES_STRATEGIES)
    commits = sortie.decode().split()
    if code != 0 or not commits:
        return None, None, None, "aucun commit du registre sur %s" % branche
    reecritures, completions, dernier = [], [], {}
    for commit in commits:
        code, octets = git("show", "%s:%s" % (commit, C.REGISTRE_DES_STRATEGIES))
        if code != 0:
            continue          # le registre n'existait pas encore à ce commit (renommage) : rien à comparer
        par_id, doubles = empreintes_par_identifiant(J, C.lignes_du_registre_pour_compter_k(octets), lire)
        for ident in doubles:
            reecritures.append((ident, commit[:8], commit[:8]))
        for ident, vues in par_id.items():
            empreinte, jouable = vues[-1]
            if ident in dernier and dernier[ident][0] != empreinte:
                empreinte_avant, jouable_avant, commit_avant = dernier[ident]
                if jouable_avant:
                    reecritures.append((ident, commit_avant, commit[:8]))
                else:
                    completions.append((ident, commit_avant, commit[:8]))
            dernier[ident] = (empreinte, jouable, commit[:8])
    return sorted(set(reecritures)), completions, len(commits), ""


def registre_fabrique(C, entete, lignes):
    """Écrit un registre (texte CSV) à partir de lignes lues par le contrat.
    ① RÔLE — fabriquer un registre avec de VRAIES lignes (R-732) légèrement changées.
    ② CONTEXTE D'APPEL — U2, U4.
    ③ ENTRÉE — `C` : le contrat · `entete` : la liste des colonnes du vrai registre · `lignes` : des dictionnaires.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte du registre.
    [rend: 1]
    ⑥ TRAITEMENT — `csv.DictWriter` aux colonnes du vrai registre, fins de ligne « \\n ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — relire par le contrat ce qu'on a écrit : le chemin de lecture reste celui du système.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
    [sort: non]"""
    f = io.StringIO()
    w = csv.DictWriter(f, fieldnames=entete, extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    for l in lignes:
        w.writerow({k: l.get(k, "") for k in entete})
    return f.getvalue()


def git_jetable(dossier, *args):
    """Lance git dans un dépôt jetable, sans configuration de l'utilisateur, et lève s'il échoue.
    ① RÔLE — fabriquer les histoires de U4 et U6. ② CONTEXTE D'APPEL — U4, U6. ③ ENTRÉE — `dossier`, les arguments.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la sortie texte. [rend: 1] ⑥ TRAITEMENT — subprocess, auteur et
    dates fixés. ⑦ UNITÉ — — ⑧ POURQUOI — un dépôt jetable ne doit dépendre d'aucun réglage de la machine.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — écrit dans le dépôt jetable. ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]"""
    env = dict(os.environ, GIT_AUTHOR_NAME="epreuve", GIT_AUTHOR_EMAIL="epreuve@exemple.invalid",
               GIT_COMMITTER_NAME="epreuve", GIT_COMMITTER_EMAIL="epreuve@exemple.invalid",
               GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
    for v in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(v, None)
    p = subprocess.run(["git", *args], cwd=dossier, env=env, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("git %s : %s" % (" ".join(args), p.stderr.strip()[:300]))
    return p.stdout


def cas(copie, depot):
    """Joue U1 à U6 sur la copie, l'histoire réelle étant lue dans `depot`.

    ① RÔLE — Voir l'en-tête, LES CAS.
    ② CONTEXTE D'APPEL — Le mode « --cas », relancé par le programme principal dans chaque copie.
    ③ ENTRÉE — `copie` : la copie éprouvée (sabotée ou non) · `depot` : le dépôt git dont on lit l'histoire.
    ④ CONDITIONS D'ENTRÉE — Celles du programme.
    ⑤ SORTIE — UNE valeur : la liste de (nom du cas, réussi, détail), un élément par cas.
    [rend: 1]
    ⑥ TRAITEMENT — Chaque cas dans `un`, qui fait rougir un cas qui lève (R-734).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir l'en-tête.
    ⑨ CE QUI CLOCHE — Voir l'en-tête.
    ⑩ EFFET — Écrit et efface des dossiers temporaires ; lance git et python3.
    ⑪ TERMINAISON — Rend la main.
    [sort: non]"""
    res = []

    def un(nom, f):
        """Joue un cas ; une exception le fait rougir.
        ① RÔLE — R-734. ② CONTEXTE D'APPEL — `cas`. ③ ENTRÉE — `nom`, `f` (sans argument, rend (réussi, détail)).
        ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Aucune (ajoute à `res`). [rend: rien] ⑥ TRAITEMENT — appeler, rattraper.
        ⑦ UNITÉ — — ⑧ POURQUOI — un cas qui n'a pas pu tourner n'est pas vert. ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — celui de `f`. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        try:
            ok, detail = f()
        except Exception as e:  # un cas qui n'a pas pu tourner rougit (R-734)
            ok, detail = False, "N'A PAS PU TOURNER : %s: %s" % (type(e).__name__, str(e)[:300])
        res.append((nom, bool(ok), detail))

    J, C, T = charger(copie)
    lire = module_du_jour(copie)
    chemin = os.path.join(copie, C.REGISTRE_DES_STRATEGIES)
    lignes = C.lignes_du_registre(chemin)
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        entete = next(csv.reader(f))

    def derniere(ident):
        """La dernière ligne de `ident` au vrai registre. ① RÔLE — prendre une VRAIE ligne (R-732).
        ② CONTEXTE D'APPEL — U2, U4. ③ ENTRÉE — `ident`. ④ CONDITIONS D'ENTRÉE — l'identifiant est au registre.
        ⑤ SORTIE — UNE valeur : une copie de la ligne. [rend: 1] ⑥ TRAITEMENT — la dernière ligne de cet id.
        ⑦ UNITÉ — — ⑧ POURQUOI — —. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main, ou lève
        IndexError si l'id manque (le cas rougit). [sort: non]"""
        return dict([l for l in lignes if l["id"] == ident][-1])

    def u1():
        """U1 — le vrai registre. ① RÔLE — voir l'en-tête. ② CONTEXTE D'APPEL — `un`. ③ ENTRÉE — par fermeture.
        ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — DEUX valeurs : réussi, détail. [rend: 2] ⑥ TRAITEMENT — les deux
        relevés, et leur accord. ⑦ UNITÉ — lignes, identifiants. ⑧ POURQUOI — R2 du superviseur. ⑨ CE QUI CLOCHE — les
        totaux sont affichés, jamais comparés à un chiffre (ils grandissent avec le registre). ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main. [sort: non]"""
        par_id, doubles = empreintes_par_identifiant(J, lignes, lire)
        par_fiche, total = J.versions_du_registre(lignes, lire)
        plus_d_une = sorted(i for i, n in par_fiche.items() if n != 1)
        a_deux_lignes = sorted(i for i in par_id if sum(1 for l in lignes if l["id"] == i) > 1)
        jouables = sum(1 for v in par_id.values() if v[-1][1])
        ok = not doubles and not plus_d_une and set(par_fiche) == set(par_id)
        return ok, ("%d lignes · %d identifiants (%d jouables) · %d versions · identifiants à plusieurs lignes : %s · "
                    "plus d'une empreinte : %s · plus d'une version : %s" % (
                        len(lignes), len(par_id), jouables, total, a_deux_lignes or "aucun", doubles or "aucun",
                        plus_d_une or "aucun"))
    un("U1 le vrai registre : un identifiant, une empreinte", u1)

    def u2():
        """U2 — registres fabriqués de vraies lignes. ① RÔLE — voir l'en-tête. ② CONTEXTE D'APPEL — `un`.
        ③ ENTRÉE — par fermeture. ④ CONDITIONS D'ENTRÉE — C5-EI-PARAMS et MA200-S1 sont au registre, C5-EI-PARAMS
        porte « +5.0% » et « -2.0% ». ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — quatre registres, quatre
        attentes. ⑦ UNITÉ — identifiants. ⑧ POURQUOI — un contrôle se calibre sur un cas qui doit rougir et sur un cas
        qui doit rester vert. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        c5, ma = derniere("C5-EI-PARAMS"), derniere("MA200-S1")
        assert c5["tp"] == "+5.0%" and c5["sl"] == "-2.0%", "la vraie ligne a changé : %r %r" % (c5["tp"], c5["sl"])
        ind = derniere("IND-001-RETEST")
        variantes = {
            "tp +9,0 %": (dict(c5, tp="+9.0%"), ["C5-EI-PARAMS"]),
            "stop -1,0 %": (dict(c5, sl="-1.0%"), ["C5-EI-PARAMS"]),
            # relecteur neuf du 14-11-2026, D1 et D3 : chaque autre réglage, et les deux mots « sans stop », « aucune »
            "sans stop": (dict(c5, sl="sans stop"), ["C5-EI-PARAMS"]),
            "durée aucune": (dict(c5, horizon="aucune"), ["C5-EI-PARAMS"]),
            "durée 31": (dict(c5, horizon="31"), ["C5-EI-PARAMS"]),
            "univers sans sa dernière valeur": (dict(c5, univers=",".join(c5["univers"].split(",")[:-1])),
                                                ["C5-EI-PARAMS"]),
            "signal d'IND-001-RETEST": (dict(c5, module_signal=ind["module_signal"], fonction_signal=ind["fonction_signal"],
                                             reglages_signal=ind["reglages_signal"]), ["C5-EI-PARAMS"]),
            "période finie un jour plus tôt": (dict(c5, periode=c5["periode"][:-2] + "%02d" % (int(c5["periode"][-2:]) - 1)),
                                               ["C5-EI-PARAMS"]),
            "note changée": (dict(ma, note=ma["note"] + " [note de l'épreuve]"), []),
            "entrée vide": (dict(c5, entree=""), []),
            "tp écrit « +5,00 % »": (dict(c5, tp="+5.00%"), []),
        }
        faux, vus = [], []
        for nom, (ajout, attendu) in variantes.items():
            relu = C.lignes_du_registre_pour_compter_k(registre_fabrique(C, entete, lignes + [ajout]).encode("utf-8"))
            _par_id, doubles = empreintes_par_identifiant(J, relu, lire)
            vus.append("%s → %s" % (nom, doubles or "rien"))
            if doubles != attendu:
                faux.append(nom)
        return not faux, " ; ".join(vus) + (" ; FAUX : %s" % faux if faux else "")
    un("U2 une ligne ajoutée sous le même identifiant : tout réglage changé rougit, note, entrée vide ou écriture non",
       u2)

    def u3():
        """U3 — la vraie histoire. ① RÔLE — voir l'en-tête. ② CONTEXTE D'APPEL — `un`. ③ ENTRÉE — `depot`.
        ④ CONDITIONS D'ENTRÉE — dépôt complet. ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — `histoire_du_registre`.
        ⑦ UNITÉ — commits. ⑧ POURQUOI — F10 du superviseur. ⑨ CE QUI CLOCHE — les complétions sont nommées, pas
        jugées (question ⑥). ⑩ EFFET — lance git en lecture. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        reecritures, completions, n, raison = histoire_du_registre(J, C, T, depot, lire)
        if raison:
            return False, "INCONNU : " + raison
        return not reecritures, ("%d commits lus sur %s · réécritures d'une ligne jouable : %s · COMPLÉTIONS — "
                                 "question ⑥ à Jean-Luc : %s" % (
                                     n, C.BRANCHE_PRINCIPALE, reecritures or "aucune",
                                     ", ".join("%s (%s→%s)" % x for x in completions) or "aucune"))
    un("U3 la vraie histoire de la branche principale : aucune réécriture d'une ligne jouable", u3)

    def fabriquer_l_histoire(d):
        """Fabrique le dépôt jetable de U4 et U6. ① RÔLE — une histoire connue. ② CONTEXTE D'APPEL — U4, U6.
        ③ ENTRÉE — `d` : un dossier vide. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — Aucune. [rend: rien]
        ⑥ TRAITEMENT — commit 1 : C5-EI-PARAMS (jouable), MA200-S1, IND-001-RETEST sans ses trois cases de signal
        (refusée, comme au commit 81fd7fa6 du 11-11-2026) · branche « propre » posée là, HEAD dessus · commit 2 sur la
        branche principale : tp de C5-EI-PARAMS réécrit +5.0 % → +9.0 % SUR PLACE, note de MA200-S1 changée,
        IND-001-RETEST complétée ; la branche principale du contrat posée sur ce commit. ⑦ UNITÉ — —
        ⑧ POURQUOI — les trois conduites de `histoire_du_registre`, et HEAD ignoré. ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — écrit sous `d`. ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]"""
        c5, ma, ind = derniere("C5-EI-PARAMS"), derniere("MA200-S1"), derniere("IND-001-RETEST")
        ind_refusee = dict(ind, module_signal="", fonction_signal="", reglages_signal="")
        rel = C.REGISTRE_DES_STRATEGIES
        os.makedirs(os.path.join(d, os.path.dirname(rel)))
        git_jetable(d, "init", "-q", "-b", "travail")
        open(os.path.join(d, rel), "w", encoding="utf-8").write(registre_fabrique(C, entete, [c5, ma, ind_refusee]))
        git_jetable(d, "add", "-A")
        git_jetable(d, "commit", "-q", "-m", "un")
        git_jetable(d, "branch", "propre")
        open(os.path.join(d, rel), "w", encoding="utf-8").write(registre_fabrique(
            C, entete, [dict(c5, tp="+9.0%"), dict(ma, note=ma["note"] + " [note de l'épreuve]"), ind]))
        git_jetable(d, "commit", "-q", "-am", "deux")
        git_jetable(d, "update-ref", "refs/remotes/" + C.BRANCHE_PRINCIPALE, "HEAD")
        git_jetable(d, "checkout", "-q", "propre")

    def u4():
        """U4 — une histoire fabriquée. ① RÔLE — voir l'en-tête. ② CONTEXTE D'APPEL — `un`. ③ ENTRÉE — —.
        ④ CONDITIONS D'ENTRÉE — la branche principale du contrat a la forme « <distant>/<branche> ». ⑤ SORTIE — DEUX
        valeurs. [rend: 2] ⑥ TRAITEMENT — fabriquer, lire, comparer à l'attendu : une réécriture (C5-EI-PARAMS), une
        complétion (IND-001-RETEST), MA200-S1 nulle part, et d'abord la ligne refusée vérifiée refusée.
        ⑦ UNITÉ — identifiants. ⑧ POURQUOI — calibrer sur un cas connu et sur un cas qui doit échouer. ⑨ CE QUI CLOCHE
        — —. ⑩ EFFET — dossier temporaire, effacé. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        ind = derniere("IND-001-RETEST")
        refusee = not J.empreinte_des_reglages(dict(ind, module_signal="", fonction_signal="", reglages_signal=""),
                                               lire)[1]
        d = tempfile.mkdtemp(prefix="une_empreinte_histoire_")
        try:
            fabriquer_l_histoire(d)
            reecritures, completions, n, raison = histoire_du_registre(J, C, T, d, lire)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        if raison:
            return False, "INCONNU : " + raison
        r_ids = sorted({x[0] for x in reecritures})
        c_ids = sorted({x[0] for x in completions})
        ok = refusee and n == 2 and r_ids == ["C5-EI-PARAMS"] and c_ids == ["IND-001-RETEST"]
        return ok, ("IND-001-RETEST sans signal refusée : %s · %s commits · réécritures : %s (attendu "
                    "['C5-EI-PARAMS']) · complétions : %s (attendu ['IND-001-RETEST'])" % (
                        "oui" if refusee else "NON", n, r_ids, c_ids))
    un("U4 une histoire fabriquée : réécriture sur place rougit, note non, complétion nommée, HEAD ignoré", u4)

    def u5():
        """U5 — indépendance du lancement. ① RÔLE — voir l'en-tête. ② CONTEXTE D'APPEL — `un`. ③ ENTRÉE — —.
        ④ CONDITIONS D'ENTRÉE — python3 relançable. ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — relancer ce
        programme en mode « --empreintes » sous PYTHONHASHSEED=1 puis 2 ; comparer les empreintes (égales attendues)
        et les écritures brutes `repr` des lectures (différentes attendues : sinon le cas n'a pas de dents).
        ⑦ UNITÉ — —. ⑧ POURQUOI — voir le ⑧ d'`empreinte_des_reglages`. ⑨ CE QUI CLOCHE — si un jour aucune ligne
        jouable n'a un ensemble de plus d'un élément, les `repr` seront égaux et le cas rougira : il le dira.
        ⑩ EFFET — lance python3. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        sorties = []
        for graine in ("1", "2"):
            p = subprocess.run([sys.executable, "-B", os.path.join(copie, SOI), "--empreintes", copie],
                               env=dict(os.environ, PYTHONHASHSEED=graine), capture_output=True, text=True,
                               timeout=DELAI)
            if p.returncode != 0:
                return False, "relance sous la graine %s : code %d · %s" % (graine, p.returncode, p.stderr[-300:])
            emp, brut = p.stdout.split("\n--\n")
            sorties.append((emp, brut))
        memes = sorties[0][0] == sorties[1][0]
        bruts_differents = sorties[0][1] != sorties[1][1]
        return memes and bruts_differents, "empreintes identiques sous deux graines : %s · écritures brutes " \
            "différentes (le cas a des dents) : %s · %d empreintes" % (
                "oui" if memes else "NON", "oui" if bruts_differents else "NON", len(sorties[0][0].splitlines()))
    un("U5 l'empreinte ne dépend pas du lancement", u5)

    def u6():
        """U6 — dépôt superficiel. ① RÔLE — voir l'en-tête. ② CONTEXTE D'APPEL — `un`. ③ ENTRÉE — —.
        ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — cloner l'histoire fabriquée à
        une profondeur de 1 (« file:// », sinon git ignore la profondeur), poser la branche principale, lire.
        ⑦ UNITÉ — —. ⑧ POURQUOI — R-734. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — dossiers temporaires, effacés.
        ⑪ TERMINAISON — Rend la main. [sort: non]"""
        d = tempfile.mkdtemp(prefix="une_empreinte_superficiel_")
        try:
            source, clone = os.path.join(d, "source"), os.path.join(d, "clone")
            os.makedirs(source)
            fabriquer_l_histoire(source)
            git_jetable(source, "checkout", "-q", "travail")
            git_jetable(d, "clone", "-q", "--depth", "1", "file://" + source, clone)
            git_jetable(clone, "update-ref", "refs/remotes/" + C.BRANCHE_PRINCIPALE, "HEAD")
            reecritures, _c, _n, raison = histoire_du_registre(J, C, T, clone, lire)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        return bool(raison) and reecritures is None, "rendu : %s" % (("INCONNU : " + raison) if raison else
                                                                       "LU (réécritures %s)" % reecritures)
    un("U6 un dépôt superficiel rend INCONNU", u6)

    def avec_lecture(changer, ligne):
        """Rend l'empreinte de `ligne` quand la lecture du juge est changée par `changer`.
        ① RÔLE — éprouver l'empreinte champ par champ de la lecture, sans fabriquer une fiche par champ.
        ② CONTEXTE D'APPEL — U7, U8. ③ ENTRÉE — `changer` : lecture → lecture · `ligne` : une vraie ligne.
        ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : l'empreinte, ou le texte de l'exception levée.
        [rend: 1] ⑥ TRAITEMENT — remplacer `J.lecture_de_jeu` le temps d'un appel, le remettre (finally).
        ⑦ UNITÉ — —. ⑧ POURQUOI — l'empreinte appelle `lecture_de_jeu` par son nom de module : la remplacer là suffit.
        ⑨ CE QUI CLOCHE — —. ⑩ EFFET — modifie le module chargé le temps d'un appel. ⑪ TERMINAISON — Rend la main.
        [sort: non]"""
        vraie = J.lecture_de_jeu
        J.lecture_de_jeu = lambda f, lm: changer(vraie(f, lm))
        try:
            return J.empreinte_des_reglages(ligne, lire)[0]
        except Exception as e:  # le cas lit le texte
            return "LÈVE %s: %s" % (type(e).__name__, e)
        finally:
            J.lecture_de_jeu = vraie

    def autre_valeur(v):
        """Une valeur différente de `v`, de même nature. ① RÔLE — changer UN champ de la lecture.
        ② CONTEXTE D'APPEL — U7. ③ ENTRÉE — `v`. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur. [rend: 1]
        ⑥ TRAITEMENT — nombre +0,5 ; ensemble + un élément ; tuple + un élément ; texte + « · » ; None → « x » ;
          une valeur unique de COMMUN → 7.0. ⑦ UNITÉ — —. ⑧ POURQUOI — « si j'ajoute un champ, l'épreuve change-t-elle
          d'avis ? » : chaque champ de la lecture est changé, qu'il soit connu de l'épreuve ou non.
        ⑨ CE QUI CLOCHE — un type nouveau dans la lecture lève : le cas rougit (voulu). ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main, ou lève TypeError. [sort: non]"""
        if isinstance(v, bool):
            return not v
        if isinstance(v, (int, float)):
            return v + 0.5
        if isinstance(v, frozenset):
            return v | {"ZZ_EPREUVE"}
        if isinstance(v, tuple):
            return v + ("ZZ_EPREUVE",)
        if isinstance(v, str):
            return v + "·"
        if v is None:
            return "x"
        if str(v) in ("sans stop", "aucune"):
            return 7.0
        raise TypeError("champ de lecture de type inconnu : %r" % (v,))

    def u7():
        """U7 — chaque champ de la lecture compte. ① RÔLE — relecteur neuf du 14-11-2026, D3 : quatre mutants
        (empreinte sans univers, sans horizon, sans signal, sur tp et sl seuls) laissaient U verte.
        ② CONTEXTE D'APPEL — `un`. ③ ENTRÉE — par fermeture. ④ CONDITIONS D'ENTRÉE — C5-EI-PARAMS l.70 jouable.
        ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — pour chaque rang de la lecture réelle (le rang 0, le mot
        JOUABLE, compris), changer ce champ SEUL et exiger une autre empreinte. Le nombre de champs est LU, jamais
        écrit : un champ ajouté demain est éprouvé sans toucher l'épreuve. ⑦ UNITÉ — champs. ⑧ POURQUOI — voir ①.
        ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        c5 = derniere("C5-EI-PARAMS")
        lu = J.lecture_de_jeu(dict(c5), lire)
        base = J.empreinte_des_reglages(c5, lire)[0]
        muets = []
        for i in range(len(lu)):
            e = avec_lecture(lambda l, i=i: l[:i] + (autre_valeur(l[i]),) + l[i + 1:], c5)
            if e == base or e.startswith("LÈVE"):
                muets.append((i, e))
        return lu[0] == "JOUABLE" and not muets, "%d champs dans la lecture réelle ; champs sans effet sur " \
            "l'empreinte : %s" % (len(lu), muets or "aucun")
    un("U7 chaque champ de la lecture du juge change l'empreinte (le nombre de champs est lu)", u7)

    def u8():
        """U8 — une seule écriture des nombres et des mots. ① RÔLE — relecteur neuf du 14-11-2026, D5 et D1.
        ② CONTEXTE D'APPEL — `un`. ③ ENTRÉE — par fermeture. ④ CONDITIONS D'ENTRÉE — la lecture porte tp au rang 1,
        sl au rang 2, l'horizon au rang 3 (vérifié sur la vraie ligne : 0,05, 0,02, 30). ⑤ SORTIE — DEUX valeurs.
        [rend: 2] ⑥ TRAITEMENT — 30 et 30.0 au rang 3 : même empreinte · 0.0 et −0.0 au rang 1 : même · True au
        rang 3 : lève · NaN au rang 1 : lève · « sans stop » et « aucune » (vraies lignes) : une empreinte, sans lever.
        ⑦ UNITÉ — —. ⑧ POURQUOI — D5 : `canonique` séparait 4 et 4.0, −0.0 et 0.0, et rendait NaN égale à elle-même.
        ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        c5 = derniere("C5-EI-PARAMS")
        lu = J.lecture_de_jeu(dict(c5), lire)
        assert (lu[1], lu[2], lu[3]) == (0.05, 0.02, 30), "la vraie ligne a changé : %r" % (lu[1:4],)
        poser = lambda i, v: (lambda l: l[:i] + (v,) + l[i + 1:])
        vus = {
            "30 et 30.0": (avec_lecture(poser(3, 30), c5), avec_lecture(poser(3, 30.0), c5)),
            "0.0 et -0.0": (avec_lecture(poser(1, 0.0), c5), avec_lecture(poser(1, -0.0), c5)),
        }
        egaux = all(a == b and not a.startswith("LÈVE") for a, b in vus.values())
        vrai = avec_lecture(poser(3, True), c5)
        nan = avec_lecture(poser(1, float("nan")), c5)
        mots = [J.empreinte_des_reglages(dict(c5, sl="sans stop"), lire), J.empreinte_des_reglages(dict(c5, horizon="aucune"), lire)]
        ok = egaux and vrai.startswith("LÈVE") and nan.startswith("LÈVE") and all(m[1] for m in mots)
        return ok, "égaux : %s · True : %s · NaN : %s · « sans stop », « aucune » : %s" % (
            {k: v[0] == v[1] for k, v in vus.items()}, vrai[:60], nan[:60], [m[0] for m in mots])
    un("U8 une seule écriture des nombres (4 = 4.0, -0.0 = 0.0, booléen et NaN refusés) et des mots", u8)

    def definitions_d_empreinte(texte, nom):
        """Relève, dans un texte Python, les fonctions qui DÉFINISSENT une empreinte des réglages.
        ① RÔLE — la propriété de U9 : une seule définition au dépôt (R-708 ; relecteur neuf du 14-11-2026, D2).
        ② CONTEXTE D'APPEL — U9 (le dépôt, son calibrage). ③ ENTRÉE — `texte` : un programme · `nom` : son nom affiché.
        ④ CONDITIONS D'ENTRÉE — du Python lisible. ⑤ SORTIE — UNE valeur : la liste de (nom, fonction, ligne).
        [rend: 1] ⑥ TRAITEMENT — une fonction (à tout niveau) est relevée si ① son nom porte « empreinte » ET
          « reglage », ou ② elle hache (sha256, sha1, md5, blake2b) ET lit une liste nommée REGLAGES (nom ou attribut)
          — la forme de la seconde définition trouvée le 14-11-2026. ⑦ UNITÉ — —. ⑧ POURQUOI — un nom seul se
          contourne en renommant ; le hachage d'une liste de réglages, non.
        ⑨ CE QUI CLOCHE — CE N'EST QU'UN FILET CONTRE L'OUBLI, PAS UNE GARDE (superviseur R-759 du 14-11-2026, tour 3,
          N3 ; même statut que le contrôle des conformités de CONTROLER_MA_LIVRAISON, décision de Jean-Luc du
          17-10-2026 à 16h10). Le relecteur du tour 2 a mesuré huit formes de seconde définition : celle-ci en voit
          UNE (la forme du 11-11, plus « import hashlib as H ») ; X1 à X7 passent (sha256 importé seul,
          hashlib.new, sha512, lambda, clé en tuple sans hachage, nom accentué, liste en clair). Ne pas l'étendre :
          la vraie garde est la confrontation de l'empreinte écrite à la fiche aux carrefours (N5, partie 2).
        ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main ; lève SyntaxError. [sort: non]"""
        trouves = []
        for n in ast.walk(ast.parse(texte)):
            if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            par_le_nom = "empreinte" in n.name.lower() and "reglage" in n.name.lower()
            hache = any(isinstance(x, ast.Attribute) and x.attr in ("sha256", "sha1", "md5", "blake2b")
                        for x in ast.walk(n))
            reglages = any((isinstance(x, ast.Name) and x.id == "REGLAGES")
                           or (isinstance(x, ast.Attribute) and x.attr == "REGLAGES") for x in ast.walk(n))
            if par_le_nom or (hache and reglages):
                trouves.append((nom, n.name, n.lineno))
        return trouves

    def u9():
        """U9 — une seule définition de l'empreinte des réglages dans programmes/. ① RÔLE — voir
        `definitions_d_empreinte`. ② CONTEXTE D'APPEL — `un`. ③ ENTRÉE — la copie ; le dépôt pour le calibrage.
        ④ CONDITIONS D'ENTRÉE — le commit AVANT_LA_REPARATION est dans l'histoire du dépôt. ⑤ SORTIE — DEUX valeurs.
        [rend: 2] ⑥ TRAITEMENT — ① calibrage : sur `programmes/TRIER_LES_VARIANTES.py` d'AVANT_LA_REPARATION, la
          fonction de la ligne 414 est trouvée ; sur deux textes fabriqués, une fonction qui hache REGLAGES sous un
          autre nom est trouvée, une `empreinte_des_cours` non · ② la copie : la seule définition trouvée est celle du
          juge (`J.empreinte_des_reglages`, nom et fichier lus sur l'objet). ⑦ UNITÉ — fonctions.
        ⑧ POURQUOI — coordinateur du tour 2 (14-11-2026) : « une épreuve de propriété rougit si une seconde définition
          d'empreinte réapparaît dans programmes/, calibrée sur l'état actuel ». ⑨ CE QUI CLOCHE — voir
          `definitions_d_empreinte`. ⑩ EFFET — lance git en lecture. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        code, ancien = T.git_de(depot)("show", "%s:programmes/TRIER_LES_VARIANTES.py" % AVANT_LA_REPARATION)
        if code != 0:
            return False, "INCONNU : calibrage impossible, %s absent de l'histoire" % AVANT_LA_REPARATION
        cal_ancien = definitions_d_empreinte(ancien.decode("utf-8"), "TRIER@" + AVANT_LA_REPARATION)
        cal_vu = definitions_d_empreinte("import hashlib\ndef cle(l, j):\n    return hashlib.sha256("
                                         "'|'.join(l[k] for k in j.REGLAGES).encode()).hexdigest()\n", "FABRIQUE_VU")
        cal_pas = definitions_d_empreinte("import hashlib\ndef empreinte_des_cours(c):\n    return "
                                          "hashlib.sha256(c).hexdigest()\n", "FABRIQUE_PAS_VU")
        calibre = [x[1:] for x in cal_ancien] == [("empreinte_des_reglages", 414)] and len(cal_vu) == 1 and not cal_pas
        trouvees = []
        dossier_p = os.path.join(copie, "programmes")
        for racine_d, _ds, fichiers in os.walk(dossier_p):
            for f in sorted(fichiers):
                if f.endswith(".py"):
                    chemin = os.path.join(racine_d, f)
                    trouvees += definitions_d_empreinte(open(chemin, encoding="utf-8").read(),
                                                        os.path.relpath(chemin, copie))
        la_seule = (os.path.relpath(J.__file__, copie), J.empreinte_des_reglages.__name__)
        autres = [x for x in trouvees if (x[0], x[1]) != la_seule]
        return calibre and not autres and len(trouvees) == 1, (
            "calibrage : avant la réparation %s, fabriqué vu %s, fabriqué non vu %s · dans la copie : %s · autres que "
            "la définition du juge : %s" % (cal_ancien, len(cal_vu), cal_pas, trouvees, autres or "aucune"))
    un("U9 filet contre l'oubli : la forme de la seconde définition du 11-11 ne revient pas (1 forme vue sur 8)", u9)

    def u10():
        """U10 — fiche et version de moulinette aux mêmes réglages : même empreinte. ① RÔLE — superviseur R-759 du
        14-11-2026, §4.5. ② CONTEXTE D'APPEL — `un`. ③ ENTRÉE — la combinatoire RÉELLE de C5E10-OBS-V1 (2 695
        versions). ④ CONDITIONS D'ENTRÉE — la version marquée « OUI » (version_de_la_fiche) existe. ⑤ SORTIE — DEUX
        valeurs. [rend: 2] ⑥ TRAITEMENT — par `JOUER_LES_VERSIONS.empreinte_de_la_version` (ce que JOUER écrit) :
        la version de la fiche porte l'empreinte de la fiche ; toutes les empreintes sont distinctes ; une SEULE égale
        celle de la fiche (la version-mère comptée deux fois, F4 du superviseur, se voit). ⑦ UNITÉ — versions.
        ⑧ POURQUOI — une seconde définition renaîtrait ici d'abord. ⑨ CE QUI CLOCHE — JOUER réel n'est pas lancé ici
        (il l'est par T1e de l'épreuve du tri). ⑩ EFFET — charge JOUER. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        import importlib.util
        sp = importlib.util.spec_from_file_location("jouer_u10", os.path.join(copie, JOUER))
        V = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(V)
        fiche = derniere("C5E10-OBS-V1")
        with open(os.path.join(copie, COMBINATOIRE_REELLE), encoding="utf-8", newline="") as f:
            versions = list(csv.DictReader(f))
        e_fiche = J.empreinte_des_reglages(fiche, lire)[0]
        emp = {v["id_version"]: V.empreinte_de_la_version(J, fiche, v, lire) for v in versions}
        de_la_fiche = [v["id_version"] for v in versions if (v.get("version_de_la_fiche") or "").strip()]
        egales = sorted(i for i, e in emp.items() if e == e_fiche)
        ok = len(de_la_fiche) == 1 and egales == de_la_fiche and len(set(emp.values())) == len(versions)
        return ok, "%d versions · %d empreintes distinctes · fiche %s · versions de même empreinte : %s (marquée : %s)" % (
            len(versions), len(set(emp.values())), e_fiche, egales, de_la_fiche)
    un("U10 fiche et version de moulinette aux mêmes réglages : même empreinte (combinatoire réelle)", u10)

    def u11():
        """U11 — l'empreinte d'un module est celle de son CODE. ① RÔLE — relecteur du tour 2 (14-11-2026), N1 et N2 ;
        superviseur R-759, tour 3, §1.2 et §3.3. ② CONTEXTE D'APPEL — `un`. ③ ENTRÉE — le VRAI module
        MODULE_SIGNAL_RSI_REBOND.py de la copie (R-732). ④ CONDITIONS D'ENTRÉE — il commence par un texte explicatif.
        ⑤ SORTIE — DEUX valeurs. [rend: 2] ⑥ TRAITEMENT — dans un dossier jetable, cinq versions du module lues par
        `J.lire_module_du_jour` : telle quelle (base) · une ligne de code ajoutée → AUTRE empreinte · un commentaire
        ajouté → MÊME · une phrase ajoutée au texte explicatif du module → MÊME · une ligne non analysable → LÈVE
        ValueError (jamais None) ; et un module absent → None. ⑦ UNITÉ — —. ⑧ POURQUOI — sur l'octet brut, un
        commentaire changeait l'empreinte (N1) ; un sabotage « 0 » × 16 de la lecture restait vert partout (N2).
        ⑨ CE QUI CLOCHE — `k_a_la_date` lit par la même fonction (`empreinte_d_un_module`) ; il n'est pas rejoué ici
        sur un module changé (son épreuve, E5 du compte des essais, le fait). ⑩ EFFET — dossier temporaire effacé.
        ⑪ TERMINAISON — Rend la main. [sort: non]"""
        rel = os.path.join("programmes", "MODULE_SIGNAL_RSI_REBOND.py")
        source = open(os.path.join(copie, rel), encoding="utf-8").read()
        debut = source.index('"""') + 3
        versions = {"base": source, "code": source + "\nX_EPREUVE_CODE = 1\n",
                    "commentaire": source + "\n# un commentaire de l'épreuve\n",
                    "texte explicatif": source[:debut] + "Une phrase de l'épreuve.\n" + source[debut:],
                    "non analysable": source + "\ndef (:\n"}
        rendus = {}
        d = tempfile.mkdtemp(prefix="une_empreinte_module_")
        try:
            os.makedirs(os.path.join(d, "programmes"))
            for nom, texte in versions.items():
                open(os.path.join(d, rel), "w", encoding="utf-8").write(texte)
                try:
                    rendus[nom] = J.lire_module_du_jour(d)(rel)
                except ValueError as e:
                    rendus[nom] = "LÈVE ValueError"
            absent = J.lire_module_du_jour(d)(os.path.join("programmes", "ABSENT.py"))
        finally:
            shutil.rmtree(d, ignore_errors=True)
        ok = (rendus["code"] != rendus["base"] and rendus["commentaire"] == rendus["base"]
              and rendus["texte explicatif"] == rendus["base"] and rendus["non analysable"] == "LÈVE ValueError"
              and absent is None and len(rendus["base"] or "") == 16)
        return ok, "%s · absent : %s" % (rendus, absent)
    un("U11 l'empreinte d'un module est celle de son code : code → autre, commentaire ou texte → même, illisible → lève",
       u11)
    return res


SABOTAGES = {   # nom : [(fichier, texte exact, remplacement)], ce qui doit rougir dit en commentaire
    # l'empreinte ne lit plus la fiche : U2 (tp +9 % passe) et U4
    "S1_empreinte_constante": [(JUGE, "    lue = lecture_de_jeu(copie, lire_module)\n",
                                "    lue = (\"JOUABLE\",)\n")],
    # la règle de D1 retirée : U1 (C5-EI-PARAMS, lignes 65 et 70, deux empreintes) et U2 (entrée vide)
    "S2_sans_la_regle_de_D1": [(JUGE, '        copie["entree"] = "DÉFAUT"\n', '        pass\n')],
    # l'empreinte prise sur l'écriture brute : U5
    "S3_texte_non_canonique": [(JUGE, "    texte = json.dumps(canonique(lue), ensure_ascii=False, sort_keys=True)\n",
                                "    texte = repr(lue)\n")],
    # l'histoire ne compare plus d'un commit à l'autre : U4
    "S4_histoire_sans_comparaison": [(SOI, "            if ident in dernier and dernier[ident][0] != empreinte:\n",
                                      "            if False:\n")],
    # l'histoire lue sur HEAD : U4 (la branche propre ne montre rien)
    "S5_histoire_lue_sur_HEAD": [(SOI, '    code, sortie = git("rev-list", "--reverse", "--topo-order", branche, "--", '
                                       'C.REGISTRE_DES_STRATEGIES)\n',
                                  '    code, sortie = git("rev-list", "--reverse", "--topo-order", "HEAD", "--", '
                                  'C.REGISTRE_DES_STRATEGIES)\n')],
    # un dépôt superficiel accepté : U6
    "S6_superficiel_accepte": [(SOI, '    if code != 0 or sortie.strip() != b"false":\n        return None, None, None, '
                                     '"dépôt superficiel',
                                '    if False:\n        return None, None, None, "dépôt superficiel')],
    # toute réécriture prise pour une complétion : U4
    "S7_tout_est_completion": [(SOI, "                if jouable_avant:\n", "                if False:\n")],
    # un identifiant à deux empreintes toléré : U1 n'a rien à voir aujourd'hui, U2 rougit
    "S8_deux_empreintes_tolerees": [(SOI, "    return par_id, sorted(i for i, v in par_id.items() if len({e for e, _ in v}) > 1)\n",
                                     "    return par_id, sorted(i for i, v in par_id.items() if len({e for e, _ in v}) > 2)\n")],
    # D5 : les nombres en forme unique — U8
    "S9_moins_zero_garde": [(JUGE, "            return [\"nombre\", repr(x + 0.0)]\n",
                             "            return [\"nombre\", repr(x)]\n")],
    "S10_type_du_nombre_garde": [(JUGE, "            return [\"nombre\", repr(x + 0.0)]\n",
                                  "            return [\"nombre\", repr(valeur)]\n")],
    "S11_booleen_accepte": [(JUGE, "        if isinstance(valeur, bool):\n            raise ValueError(",
                             "        if False:\n            raise ValueError(")],
    # D1 : « sans stop » sans son mot — U2, U8
    "S12_sans_stop_sans_son_mot": [(JUGE, '        if valeur is STOP_AUCUN:\n            return ["mot", MOT_DU_STOP_AUCUN]\n',
                                    "")],
    # D2 : une seconde définition renaît dans programmes/ — U9
    "S13_seconde_definition": [(JOUER, "def empreinte_de_la_version(J, fiche, version, lire_module):",
                                "def empreinte_des_reglages_de_la_version(J, fiche, version, lire_module):\n"
                                "    return empreinte_de_la_version(J, fiche, version, lire_module)\n\n\n"
                                "def empreinte_de_la_version(J, fiche, version, lire_module):")],
    # N2 du relecteur du tour 2 : le module n'est plus lu — U11
    "S15_module_non_lu": [(JUGE, "            return empreinte_d_un_module(f.read(), chemin)\n",
                           '            return "0" * 16\n')],
    # N1 : retour à l'octet brut (un commentaire change l'empreinte) — U11
    "S16_octet_brut": [(JUGE, "            return empreinte_d_un_module(f.read(), chemin)\n",
                        "            return hashlib.sha256(f.read()).hexdigest()[:16]\n")],
    # un module illisible rendu None au lieu de lever — U11
    "S17_illisible_rend_none": [(JUGE, '        raise ValueError("module de signal %s non analysable',
                                 '        return None\n        raise ValueError("module de signal %s non analysable')],
    # §4.2 : JOUER hache la version seule, sans la fiche — U10
    "S14_version_sans_la_fiche": [(JOUER, "    return J.empreinte_des_reglages(fusionner(fiche, version), lire_module)[0]\n",
                                   "    return J.empreinte_des_reglages(dict(version), lire_module)[0]\n")],
}


def sabotages_par_champ(depot):
    """Ajoute à SABOTAGES un sabotage PAR CHAMP de la lecture du juge : l'empreinte qui oublie ce champ.
    ① RÔLE — relecteur neuf du 14-11-2026, D3 ; superviseur R-759, §4.4 : « générés depuis la lecture, pas énumérés
      à la main (si j'ajoute un champ, l'épreuve change-t-elle d'avis ? doit répondre oui) ».
    ② CONTEXTE D'APPEL — le programme principal, avant de choisir les sabotages.
    ③ ENTRÉE — `depot` : la racine éprouvée. ④ CONDITIONS D'ENTRÉE — le juge, le contrat et le registre s'y chargent.
    ⑤ SORTIE — Aucune valeur (SABOTAGES complété). [rend: rien]
    ⑥ TRAITEMENT — compter les champs de la lecture de la vraie ligne C5-EI-PARAMS (dernière) par un processus à
      part (le juge n'est pas chargé dans ce processus) ; pour chaque rang i, « SC<i>_champ_oublie » remplace la ligne
      du hachage par celle qui hache la lecture privée du champ i.
    ⑦ UNITÉ — champs. ⑧ POURQUOI — voir ①. ⑨ CE QUI CLOCHE — un juge illisible : aucun sabotage par champ, et le
      programme rend 2 (R-734). ⑩ EFFET — lance python3. ⑪ TERMINAISON — Rend la main, ou sort en 2. [sort: oui]"""
    code = ("import os, sys\nsys.path.insert(0, os.path.join(sys.argv[1], 'programmes'))\nimport JUGE_DES_STRATEGIES as J"
            "\nimport CONTRATS_DES_FICHIERS as C\nL = C.lignes_du_registre(os.path.join(sys.argv[1], "
            "C.REGISTRE_DES_STRATEGIES))\nl = [x for x in L if x['id'] == 'C5-EI-PARAMS'][-1]\n"
            "print(len(J.lecture_de_jeu(dict(l), J.lire_module_du_jour(sys.argv[1]))))\n")
    p = subprocess.run([sys.executable, "-B", "-c", code, depot], capture_output=True, text=True, timeout=DELAI)
    if p.returncode != 0 or not p.stdout.strip().isdigit():
        print("LECTURE DU JUGE IMPOSSIBLE : aucun sabotage par champ — %s" % p.stderr[-300:])
        sys.exit(2)
    for i in range(int(p.stdout.strip())):
        SABOTAGES["SC%02d_champ_oublie" % i] = [(JUGE, LIGNE_DU_HACHAGE, LIGNE_DU_HACHAGE.replace(
            "canonique(lue)", "canonique(lue[:%d] + lue[%d:])" % (i, i + 1)))]


def preparer(depot, sab):
    """Copie le dépôt (sans .git) et y applique un sabotage.
    ① RÔLE — Donner à chaque sabotage sa copie, pour que rien ne touche au dépôt.
    ② CONTEXTE D'APPEL — Le programme principal, une fois par lancement (Z0 ou un sabotage).
    ③ ENTRÉE — `depot` : la racine · `sab` : le nom du sabotage, ou « Z0 ».
    ④ CONDITIONS D'ENTRÉE — Chaque texte visé existe UNE fois dans son fichier.
    ⑤ SORTIE — DEUX valeurs : le dossier temporaire et la racine de la copie. [rend: 2]
    ⑥ TRAITEMENT — ① copier sans .git, etudes, archives, caches · ② remplacer chaque texte visé.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une cible introuvable ne sabote rien : elle lève au lieu de passer pour un sabotage qui mord.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit un dossier temporaire.
    ⑪ TERMINAISON — Rend la main, ou lève AssertionError. [sort: non]"""
    d = tempfile.mkdtemp(prefix="une_empreinte_")
    r = os.path.join(d, "r")
    shutil.copytree(depot, r, ignore=shutil.ignore_patterns(".git", "etudes", "archives", "__pycache__",
                                                             "_site_travail"))
    for f, a, b in ([] if sab == "Z0" else SABOTAGES[sab]):
        p = os.path.join(r, f)
        t = open(p, encoding="utf-8").read()
        assert t.count(a) == 1, "%s : cible trouvée %d fois dans %s : %r" % (sab, t.count(a), f, a[:60])
        open(p, "w", encoding="utf-8").write(t.replace(a, b))
    return d, r


def empreintes_pour_u5(copie):
    """Le mode « --empreintes » de U5 : écrit les empreintes du vrai registre, puis les `repr` bruts des lectures.
    ① RÔLE — donner à U5 ce que rend un lancement. ② CONTEXTE D'APPEL — U5, sous deux graines.
    ③ ENTRÉE — `copie` : la copie éprouvée. ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — Aucune (affiche). [rend: rien]
    ⑥ TRAITEMENT — pour chaque ligne : l'empreinte ; puis une ligne « -- » ; puis le `repr` de chaque lecture (après
    la même règle de D1 que l'empreinte, appliquée par `empreinte_des_reglages` : ici on ne prend que la ligne telle
    quelle, ce qui suffit à montrer l'ordre des ensembles). ⑦ UNITÉ — —. ⑧ POURQUOI — U5. ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — affiche. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    J, C, _T = charger(copie)
    lire = module_du_jour(copie)
    lignes = C.lignes_du_registre(os.path.join(copie, C.REGISTRE_DES_STRATEGIES))
    print("".join("%s %s\n" % (l["id"], J.empreinte_des_reglages(l, lire)[0]) for l in lignes), end="")
    print("--")
    print("\n".join(repr(J.lecture_de_jeu(l, lire)) for l in lignes))


if __name__ == "__main__":
    if len(sys.argv) > 3 and sys.argv[1] == "--cas":
        resultats = cas(os.path.abspath(sys.argv[2]), os.path.abspath(sys.argv[3]))
        for nom_du_cas, ok, detail in resultats:
            print(("  ok    " if ok else "  ÉCHEC ") + nom_du_cas + " — " + detail)
        # LE MARQUEUR DE FIN : sans lui, une épreuve interrompue ne passe ni pour verte ni pour mordue
        print("FIN DES CAS : %d" % len(resultats))
        sys.exit(0 if all(ok for _, ok, _ in resultats) else 1)
    if len(sys.argv) > 2 and sys.argv[1] == "--empreintes":
        empreintes_pour_u5(os.path.abspath(sys.argv[2]))
        sys.exit(0)
    _args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not _args or not os.path.isfile(os.path.join(_args[0], JUGE)):
        print(__doc__.split("① RÔLE")[0])
        sys.exit(2)
    DEPOT = os.path.abspath(_args[0])
    sabotages_par_champ(DEPOT)
    if "--saboter" in sys.argv:
        _choix = ["Z0"] + list(SABOTAGES)
    else:
        _choix = [_args[1]] if len(_args) > 1 else ["Z0"]
        if _choix[0] != "Z0" and _choix[0] not in SABOTAGES:
            print("%s N'EXISTE PAS dans SABOTAGES" % _choix[0])
            sys.exit(2)
    _faute = False
    for sab in _choix:
        t0 = time.time()
        try:
            d, r = preparer(DEPOT, sab)
        except AssertionError as e:
            print("%s NE S'APPLIQUE PLUS : CIBLE INTROUVABLE — %s" % (sab, e))
            sys.exit(2)
        try:
            p = subprocess.run([sys.executable, "-B", os.path.join(r, SOI), "--cas", r, DEPOT], cwd=r,
                               capture_output=True, text=True, timeout=DELAI)
            code, out = p.returncode, p.stdout + p.stderr
        except subprocess.TimeoutExpired:
            code, out = 124, "délai de %d s dépassé" % DELAI
        finally:
            shutil.rmtree(d, ignore_errors=True)
        echecs = [l.strip()[len("ÉCHEC "):].split(" — ")[0] for l in out.splitlines() if l.strip().startswith("ÉCHEC")]
        fin = ("FIN DES CAS : %d" % NOMBRE_DE_CAS) in out
        if sab == "Z0":
            bon = code == 0 and not echecs and fin
            print("Z0 dépôt tel quel : %s" % ("tout vert" if bon else "ROUGE (code %d)" % code))
            print("\n".join(l for l in out.splitlines() if l.strip()))
            if not bon and (not fin or (echecs and all(
                    "— INCONNU : " in l for l in out.splitlines() if l.strip().startswith("ÉCHEC")))):
                # R-734 : une histoire illisible (dépôt superficiel, branche absente) n'est pas un rouge, c'est un
                # contrôle qui n'a pas pu tourner — code 2, comme une racine inutilisable
                print("Z0 N'A PAS PU TOURNER JUSQU'AU BOUT")
                sys.exit(2)
        else:
            bon = code == 1 and bool(echecs) and fin
            print(("%s mord : %r" % (sab, echecs)) if bon else "%s NE MORD PAS : code %d · %s" % (
                sab, code, out.strip()[-600:]))
        print("   durée : %d s" % (time.time() - t0))
        sys.stdout.flush()
        _faute = _faute or not bon
    print("VERDICT :", "tout est conforme" if not _faute else "ECHEC — voir ci-dessus")
    sys.exit(1 if _faute else 0)
