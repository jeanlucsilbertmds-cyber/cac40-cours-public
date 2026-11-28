#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTROLER_LA_GRILLE — chaque critère décidé de R-505 v2 est-il BRANCHÉ dans le code ? Écrit le Ven 27-11-2026 (Paris),
lot L4 du plan R505. Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE — POUR LE RELECTEUR ET POUR « LE MARÉCHAL » (l'agent qui surveille que les actions du projet restent
conformes à ses objectifs). Jean-Luc, 27-11-2026 à 13h25 (BACKLOG A-1067) : « toutes les décisions qu'on prend, là,
elles seront bien documentées en autoportant, n'est-ce pas? Et surtout, elles seront bien branchées sur le circuit.
Parce que si on fait tout ça et qu'à la fin, le circuit ne fonctionne pas et que tu me reposes la question et que tu
me dis "Ah oui, c'est vrai, on l'a noté, mais on ne l'a pas fait", ça n'a pas de sens. » La veille, deux décisions
notées n'avaient jamais été exécutées : le lanceur devait tourner sur GitHub (A-965) et tournait en local ; la
correction pour le nombre d'essais devait être branchée avant la première moulinette (A-654) et ne l'était pas.
La réponse est une MATRICE DE TRAÇABILITÉ exécutable : décision → code → épreuve, contrôlée par programme et non par
la mémoire (R-754 : ce qu'un programme peut faire, un programme le fait).

COMMENT SE LIT LA GRILLE — `donnees/GRILLE_R505_V2.csv`, séparateur « ; », une ligne par critère ou affichage de la loi
R-505 version 2 (la règle qui dit si l'on peut se fier à une stratégie, et laquelle joue en direct). Ses colonnes sont
déclarées UNE fois dans programmes/CONTRATS_DES_FICHIERS.py (`GRILLE_R505_V2`) :
  identifiant      E5-3, AFF-7, DIR-2… (numérotés : le numéro que la loi porte) ou E3-GLISSEMENT… (nommés)
  libelle          ce que le critère exige, en une ligne
  role             DÉCIDE (le critère fait le verdict ou le choix) ou AFFICHE (montré, ne décide jamais)
  etape            PRINCIPE, 1 à 6, VERDICT, AFFICHAGE, DIRECT
  decisions        les décisions dont il vient : A-nnn (BACKLOG), n°nn (relevé du 31-10-2026), DÉL-Dnn, R-nnn
  phrase_de_la_loi un extrait COPIÉ TEL QUEL du texte de la loi : il doit s'y retrouver, mot pour mot
  seuils_de_la_loi les clés de la table « LES SEUILS DE CETTE LOI » que ce critère applique (séparées par « , »)
  fonction         `MODULE:fonction` (programmes/MODULE.py) qui l'applique, ou vide ; plusieurs : séparées par « , »
  epreuve          `FICHIER.py:CAS` (tests/FICHIER.py, cas CAS) qui le prouve, ou vide ; plusieurs : « , »
  etat             DÉCIDÉ_NON_BRANCHÉ · BRANCHÉ · PLUS_TARD (la loi dit elle-même « plus tard »)
  constat          ce qui existe aujourd'hui, ce qui manque, l'écart relevé avec la loi (texte libre, ne décide rien)

① RÔLE — Dire, par un code de sortie et une liste lisible, si chaque critère décidé de R-505 v2 est branché : une
  fonction du code qui l'applique et une épreuve qui le prouve, toutes deux EXISTANTES ; et offrir au juge la fonction
  `motifs_de_refus_du_verdict`, qui rend la liste des raisons de REFUSER un verdict (vide seulement si tout ce qui
  retient le verdict est branché), et `motifs_de_refus_de_la_mise_en_direct` (vide seulement si tout est branché).
② CONTEXTE D'APPEL — À la main ou par une relecture : `python3 programmes/CONTROLER_LA_GRILLE.py [--racine D]
  [--grille F] [--loi SOURCE] [--backlog SOURCE] [--voir-les-lots]` ; par l'épreuve tests/EPREUVES_DE_LA_GRILLE_R505_Ven_27-11-2026.py ;
  par le juge à l'installation (étape I1 du plan R505) : `motifs_de_refus_du_verdict(racine)`, appelée là où le
  verdict se rend (aujourd'hui `MODULE_JUGEMENT.grille_de_validation`, appelée par `JUGER_UNE_FICHE.juger_une_fiche`),
  et `motifs_de_refus_de_la_mise_en_direct(racine)` là où une stratégie passerait en direct (étape 6). Au 27-11-2026,
  AUCUN programme du circuit ne les appelle (voir ⑨).
  LES DEUX PORTES (A-1109, application d'A-1067 intégrée à la loi le 27-11-2026, point ⓗ) : « le VERDICT attend que
  toutes les lignes des étapes 1 à 5 soient branchées, la MISE EN DIRECT attend en plus celles de l'étape 6 et du suivi
  en direct ». Lecture de ce programme : les lignes des étapes « 6 » et « DIRECT » ne retiennent que la mise en direct ;
  toutes les autres (PRINCIPE, 1 à 5, VERDICT, AFFICHAGE) retiennent les deux portes. Une FAUTE de la grille ferme les
  deux portes, quelle que soit la ligne : une grille fausse ne dit plus rien de sûr.
③ ENTRÉE — La ligne de commande. `--racine` : le dépôt (défaut : le dossier parent de programmes/). `--grille` : défaut
  `donnees/GRILLE_R505_V2.csv` (CONTRATS_DES_FICHIERS.GRILLE_R505). `--loi` : défaut `gouvernance/REGISTRE_REGLES.md`,
  où la loi vivra après l'installation ; une SOURCE est un chemin (absolu ou sous la racine) ou une référence git
  `REF:CHEMIN`, par exemple `origin/travail-carte:etudes/R505_V2/R505_v2_corps.md`. `--backlog` : défaut
  `BACKLOG_DECISIONS.md`, même forme. `--voir-les-lots` : avant que le Chat réunisse les lots, une fonction ou une
  épreuve absente du dépôt est cherchée aussi sur la branche que le `constat` de la ligne cite (« branche
  origin/lot-r505-… ») ; ce mode ne sert QU'À la relecture : les deux portes ne l'emploient jamais, car le juge ne
  tourne que sur le code qui est dans son dépôt.
④ CONDITIONS D'ENTRÉE — La loi lue doit porter le bloc « R-505 — VERSION 2 » ; la grille doit exister ; le BACKLOG
  doit se lire. Sinon : code 3, la raison à l'écran (R-734 : un contrôle qui n'a pas pu tourner ne rend pas 0).
⑤ SORTIE — Le programme : UN code de sortie. 0 = aucune faute et toute ligne décidée est BRANCHÉE ; 1 = aucune faute,
  mais au moins une ligne DÉCIDÉ_NON_BRANCHÉ (la vérité du 27-11-2026) ; 2 = au moins une FAUTE (fonction ou épreuve
  nommée qui n'existe pas, ligne BRANCHÉE sans fonction ou sans épreuve, critère de la loi sans ligne, ligne sans
  critère dans la loi, extrait introuvable dans la loi, décision absente du BACKLOG, case decisions sans aucun A-nnn,
  rôle contraire à la loi, seuil retiré réclamé par une ligne qui décide, seuil non réclamé, grille sans ligne,
  empreinte de la loi ou des lignes changée depuis le dernier recalage, forme fausse) ;
  3 = le contrôle n'a pas pu tourner. À l'écran : les comptes, chaque faute, les lignes non branchées.
⑥ TRAITEMENT — Voir `controler` (le contrôle) et `identifiants_de_la_loi` (le lien mécanique loi → grille).
⑦ UNITÉ — Des lignes de grille et des identifiants ; aucune grandeur physique.
⑧ POURQUOI — Une décision notée n'est pas une décision exécutée (A-1067, ci-dessus). Le lien entre la loi et la grille
  est MÉCANIQUE dans les deux sens : chaque ligne cite un extrait que le programme retrouve dans la loi (grille → loi),
  et chaque critère NUMÉROTÉ par la loi (étape 2 ① à ⑤, sortie ① à ⑤ de l'étape 3, conditions 1 à 4 de l'étape 4,
  contrôles 1 à 6 de l'étape 5, étape 6 ① à ⑤, affichages ① à ⑪, en direct ① à ⑥, les quatre verdicts, et chaque
  seuil non retiré de la table) doit avoir sa ligne (loi → grille) : retirer une ligne rougit. Ce lien se fait
  TOUJOURS, même sur une grille réduite à son en-tête (défaut D1 de la relecture du 27-11-2026 : une grille vidée
  rendait « TOUT CRITÈRE DÉCIDÉ EST BRANCHÉ — code 0 »).
  LA LOI CHANGE → LA GRILLE ROUGIT (défaut D4) : la ligne LOI-EMPREINTE porte, dans son `constat`, deux empreintes
  sha256 prises au dernier recalage — « loi=… » celle du bloc entier de la loi ramené à ses mots, « lignes=… » celle de
  la liste triée des identifiants de la grille. Toute différence est une FAUTE (code 2) jusqu'à ce qu'un relecteur ait
  relu chaque ligne contre la loi nouvelle et recopié les deux empreintes que la faute affiche. Ainsi une phrase
  NOUVELLE de la loi, même sans numéro, et une ligne supprimée, même sans numéro, rougissent.
  Une fonction est cherchée dans l'ARBRE SYNTAXIQUE du programme, sans l'importer : importer exécute du code, et un
  programme du circuit écrit des fichiers (R-752 : on relance sur une copie, jamais sur le dépôt).
⑨ CE QUI CLOCHE — (1) BRANCHÉ veut dire « une fonction NOMMÉE qui existe et une épreuve NOMMÉE qui existe » : le
  programme ne prouve ni que la fonction applique EXACTEMENT la phrase (A-1083), ni que le juge l'appelle, ni que
  l'épreuve rougit sans elle. C'est le travail du relecteur, et de la revue de bout en bout (A-1077). (2) Les critères
  NON NUMÉROTÉS par la loi (étape 1, contrôles nommés de l'étape 3, k…) ne sont liés que dans un sens : leur extrait est
  retrouvé ; une phrase NOUVELLE de la loi rougit désormais par l'empreinte, mais l'empreinte ne dit pas QUELLE ligne
  manque : le relecteur le cherche à la main. Proposition pour l'installation (I1) : poser dans la loi une marque par
  critère, par exemple « ⟦G:E3-GLISSEMENT⟧ », et remplacer l'extraction par numéros par la lecture de ces marques (une
  seule lecture, jamais les deux : R-708). L'empreinte rougit aussi sur une retouche qui ne change pas le sens (une
  virgule) : c'est voulu, le recalage est alors une relecture courte. (3) L'extraction suit la forme du texte du
  27-11-2026 (paragraphes « *Ce qu'elle fait* », numéros « 1. », chiffres cerclés) : une réécriture de forme peut la
  tromper ; l'épreuve la calibre sur le texte réel et sur des textes sabotés, mais pas sur une forme future.
  (4) Un extrait copié reste vrai si la loi ajoute ailleurs une condition à ce critère. (5) Le texte libre `constat`
  n'est pas contrôlé, sauf la ligne LOI-EMPREINTE. (6) Un cas d'épreuve est cherché dans l'ARBRE SYNTAXIQUE (défaut
  D2) : une fonction de ce nom, ou ce nom écrit comme premier argument d'un appel ou premier élément d'un couple ; un
  mot en commentaire ne suffit plus, mais une chaîne posée là sans être un cas suffirait encore. (7) Le rôle attendu
  est déduit des MOTS de l'extrait (« affich », « ne décide », « ne bloque »), du préfixe AFF- et des seuils retirés :
  un extrait mal choisi peut tromper ce contrôle, que les lignes PLUS_TARD ne passent pas (elles ne bloquent rien).
⑩ EFFET — Lit la grille, la loi, le BACKLOG et les programmes et épreuves nommés ; lance `git show` en lecture si une
  source est une référence, ou avec --voir-les-lots. N'écrit rien.
⑪ TERMINAISON — `main` sort du programme ; les autres fonctions rendent la main. `git show` est borné à 60 secondes.
"""
import ast
import csv
import functools
import hashlib
import importlib.util
import os
import re
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))

ENTETE_DE_LA_LOI = "R-505 — VERSION 2"
LOI_PAR_DEFAUT = "gouvernance/REGISTRE_REGLES.md"
BACKLOG_PAR_DEFAUT = "BACKLOG_DECISIONS.md"
CERCLES = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳"
# A-1109 : les lignes de ces étapes ne retiennent que la mise en direct ; toutes les autres retiennent aussi le verdict.
ETAPES_DE_LA_MISE_EN_DIRECT = ("6", "DIRECT")
# D4 : la ligne qui porte les empreintes du dernier recalage, dans sa case constat (« loi=<64 hex> lignes=<64 hex> »).
LIGNE_D_EMPREINTE = "LOI-EMPREINTE"
# D3 : mots de l'extrait qui disent que le critère s'AFFICHE sans décider.
MOTS_D_AFFICHAGE = re.compile(r"affich|ne décide|ne bloque", re.IGNORECASE)


class ErreurDeLecture(Exception):
    """Le contrôle ne peut pas tourner : une entrée manque ou ne se lit pas (code 3)."""


def _contrat():
    """Charge programmes/CONTRATS_DES_FICHIERS.py comme module, depuis le dossier de ce programme.

    ① RÔLE — Lire les colonnes, les états, les rôles, les étapes et le chemin de la grille là où ils sont déclarés, une
      fois (R-708 : deux écritures d'une même chose divergent toujours).
    ② CONTEXTE D'APPEL — `controler` et `main`, une fois chacun.
    ③ ENTRÉE — Aucune.
    ④ CONDITIONS D'ENTRÉE — CONTRATS_DES_FICHIERS.py est à côté de ce programme.
    ⑤ SORTIE — UNE valeur : le module chargé.
      [rend: 1]
    ⑥ TRAITEMENT — Charger le fichier par son chemin, sans passer par sys.path.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le contrat ne fait que déclarer : le charger n'écrit rien (son ⑤).
    ⑨ CE QUI CLOCHE — Le contrat est un grand fichier ; une faute de syntaxe y fait lever ici, et `main` rend alors 3.
    ⑩ EFFET — Exécute le corps du contrat (déclarations seulement).
    ⑪ TERMINAISON — Rend la main ; lève si le fichier manque ou ne se charge pas.
      [sort: non]
    """
    sp = importlib.util.spec_from_file_location("CONTRATS_DES_FICHIERS_grille",
                                                os.path.join(ICI, "CONTRATS_DES_FICHIERS.py"))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def lire_une_source(racine, source):
    """Rend le texte d'une source : un chemin, ou une référence git « REF:CHEMIN ».

    ① RÔLE — Lire la loi ou le BACKLOG là où ils sont, y compris sur une branche non fusionnée (la loi du 27-11-2026
      vit sur origin/travail-carte), sans copier de fichier.
    ② CONTEXTE D'APPEL — `controler`, deux fois (la loi, le BACKLOG).
    ③ ENTRÉE — `racine` : le dépôt · `source` : un chemin absolu, un chemin sous la racine, ou « REF:CHEMIN ».
    ④ CONDITIONS D'ENTRÉE — Pour une référence, la racine est un dépôt git qui la connaît.
    ⑤ SORTIE — UNE valeur : le texte, en UTF-8.
      [rend: 1]
    ⑥ TRAITEMENT — ① un fichier qui existe (absolu, ou sous la racine) est lu · ② sinon, une source qui porte « : » est
      passée à `git -C racine show` · ③ sinon : ErreurDeLecture.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le Chat réunit les lots sur une branche ; le contrôle doit pouvoir lire la loi avant son installation.
    ⑨ CE QUI CLOCHE — Un chemin de fichier qui contiendrait « : » et n'existerait pas serait tenté comme référence ;
      git échoue alors, et c'est ErreurDeLecture.
    ⑩ EFFET — Lit un fichier ou lance `git show` en lecture.
    ⑪ TERMINAISON — Rend la main ; `git show` est borné à 60 secondes ; lève ErreurDeLecture.
      [sort: non]
    """
    for chemin in (source, os.path.join(racine, source)):
        if os.path.isfile(chemin):
            with open(chemin, encoding="utf-8") as f:
                return f.read()
    if ":" in source:
        try:
            r = subprocess.run(["git", "-C", racine, "show", source], capture_output=True, timeout=60)
        except (OSError, subprocess.TimeoutExpired) as ex:
            raise ErreurDeLecture("git show %s impossible : %s" % (source, ex))
        if r.returncode == 0:
            return r.stdout.decode("utf-8")
        raise ErreurDeLecture("git show %s : %s" % (source, r.stderr.decode("utf-8", "replace").strip()[:200]))
    raise ErreurDeLecture("source introuvable : %s" % source)


def bloc_de_la_loi(texte):
    """Rend le seul bloc de R-505 version 2 dans un texte (le fichier de la loi, ou le REGISTRE entier).

    ① RÔLE — Isoler la loi, pour que les extraits et les numéros ne soient cherchés que dans elle.
    ② CONTEXTE D'APPEL — `controler`, une fois.
    ③ ENTRÉE — `texte` : le texte lu.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte du bloc, de sa ligne d'ouverture à la règle suivante du REGISTRE (ligne qui
      commence par « - **R- ») ou à la fin.
      [rend: 1]
    ⑥ TRAITEMENT — Chercher ENTETE_DE_LA_LOI ; remonter au début de sa ligne ; couper à la règle suivante.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Après l'installation, la loi vit au REGISTRE parmi d'autres règles : un extrait trouvé dans une autre
      règle ne prouverait rien.
    ⑨ CE QUI CLOCHE — Si le REGISTRE portait deux fois l'en-tête, seul le premier bloc serait lu.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève ErreurDeLecture si l'en-tête manque.
      [sort: non]
    """
    i = texte.find(ENTETE_DE_LA_LOI)
    if i < 0:
        raise ErreurDeLecture("la loi lue ne porte pas « %s »" % ENTETE_DE_LA_LOI)
    debut = texte.rfind("\n", 0, i) + 1
    m = re.search(r"\n- \*\*R-", texte[i:])
    return texte[debut:i + m.start()] if m else texte[debut:]


def _nu(texte):
    """Ramène un texte à ses mots séparés d'une seule espace.

    ① RÔLE — Comparer un extrait à la loi aux espaces près.
    ② CONTEXTE D'APPEL — `controler`, pour chaque extrait et chaque paragraphe.
    ③ ENTRÉE — `texte` : un texte.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte ramené.
      [rend: 1]
    ⑥ TRAITEMENT — Découper aux blancs, recoller par une espace.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un retour à la ligne de plus ou de moins n'est pas un changement de la loi.
    ⑨ CE QUI CLOCHE — Une espace insécable compte comme un blanc (`split` de Python la coupe) ; un tiret ou une
      apostrophe différents restent, eux, une différence.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return " ".join(texte.split())


def identifiants_de_la_loi(bloc):
    """Rend les critères NUMÉROTÉS que la loi porte, et les clés de sa table des seuils.

    ① RÔLE — Le lien loi → grille : la liste de ce que la loi exige sous un numéro, pour que chaque numéro ait sa ligne.
    ② CONTEXTE D'APPEL — `controler`, une fois ; l'épreuve, pour la calibrer sur le texte réel et sur des sabotages.
    ③ ENTRÉE — `bloc` : le bloc rendu par `bloc_de_la_loi`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : {identifiant : paragraphe où il est numéroté} et {clé de seuil : vrai si RETIRÉE (valeur
      « — »)}. Exemple réel (27-11-2026) : 46 identifiants (E2-1…E2-5, E3-S1…E3-S5, E4-1…E4-4, E5-1…E5-6, E6-1…E6-5,
      AFF-1…AFF-11, DIR-1…DIR-6, VERDICT-1…VERDICT-4) et 20 clés, dont 3 retirées.
      [rend: 2]
    ⑥ TRAITEMENT — Les paragraphes sont les lignes non vides. ① Le paragraphe « *Ce qu'elle fait* » qui suit l'en-tête
      « **ÉTAPE n » : étapes 2 et 6, les chiffres cerclés suivis d'une espace puis de « ** » ou d'une lettre, sauf
      « ① à ④ » (une mention, pas un critère) ; étape 3, les mêmes, après « LA SORTIE, CE QUI EST DÉCIDÉ » (E3-S1…) ;
      étapes 4 et 5, les « n. » précédés d'un début, d'une espace ou de « : » et suivis de « ** » ou d'une minuscule.
      ② Le paragraphe « **CE QUE LE VERDICT AFFICHE » : chiffres cerclés suivis d'une majuscule (AFF-n). ③ « **EN
      DIRECT, APRÈS LA VALIDATION** » : chiffres cerclés, sauf mention « ① à ⑥ » (DIR-n). ④ « **LES QUATRE
      VERDICTS** » : chaque passage en gras après le titre (VERDICT-n, dans l'ordre). ⑤ La table qui suit « **LES
      SEUILS DE CETTE LOI** » : chaque ligne « | clé | valeur | … » hors en-tête et filet.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La loi du 27-11-2026 ne porte pas de marque par critère ; ses NUMÉROS en sont une, déjà là, que
      Jean-Luc a validée étape par étape. Les lire évite d'inventer une seconde numérotation.
    ⑨ CE QUI CLOCHE — Dépend de la forme du texte (⑨ (3) du programme). Une mention d'un numéro qui n'existe pas
      (« l'étape 6 ⑦ ») créerait un identifiant de trop : la grille rougirait, ce qui est le sens prudent.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    paras = [p for p in bloc.split("\n") if p.strip()]
    ids, seuils = {}, {}
    cercle_item = re.compile(r"([%s]) (?![àÀ] [%s])(?=\*\*|[^\W\d_])" % (CERCLES, CERCLES))
    numero_item = re.compile(r"(?:^|[\s:])([1-9])\. (?=\*\*|[a-zàâçéèêëîïôûù])")
    etape = None
    for i, p in enumerate(paras):
        s = p.strip()
        m = re.match(r"\*\*ÉTAPE (\d) ", s)
        if m:
            etape = int(m.group(1))
            continue
        if s.startswith("**") and not s.startswith("**ÉPREUVE D'ARRIVÉE") and not s.startswith("**LE JUGE DOIT"):
            etape = None
        if etape and s.startswith("*Ce qu'elle fait*"):
            if etape in (2, 6):
                for c in cercle_item.findall(s):
                    ids["E%d-%d" % (etape, CERCLES.index(c) + 1)] = p
            elif etape == 3:
                j = s.find("LA SORTIE, CE QUI EST DÉCIDÉ")
                if j >= 0:
                    for c in cercle_item.findall(s[j:]):
                        ids["E3-S%d" % (CERCLES.index(c) + 1)] = p
            elif etape in (4, 5):
                for n in numero_item.findall(s):
                    ids["E%d-%s" % (etape, n)] = p
        if s.startswith("**CE QUE LE VERDICT AFFICHE"):
            for c in re.findall(r"([%s]) (?=[A-ZÀ-Ý])" % CERCLES, s):
                ids["AFF-%d" % (CERCLES.index(c) + 1)] = p
        if s.startswith("**EN DIRECT, APRÈS LA VALIDATION**"):
            for c in cercle_item.findall(s):
                ids["DIR-%d" % (CERCLES.index(c) + 1)] = p
        if s.startswith("**LES QUATRE VERDICTS**"):
            gras = re.findall(r"\*\*(.+?)\*\*", s)[1:]
            for n, _g in enumerate(gras, 1):
                ids["VERDICT-%d" % n] = p
        if s.startswith("**LES SEUILS DE CETTE LOI**"):
            for q in paras[i + 1:]:
                q = q.strip()
                if not q.startswith("|"):
                    break
                cases = [x.strip() for x in q.strip("|").split("|")]
                if len(cases) < 2 or cases[0] in ("clé", "") or set(cases[0]) <= set("-: "):
                    continue
                seuils[cases[0]] = (cases[1] == "—")
    return ids, seuils


def _texte_du_depot(racine, chemin_rel, branche=None):
    """Rend le texte d'un fichier du dépôt, dans l'arbre de travail ou sur une branche ; None s'il n'y est pas.

    ① RÔLE — Lire un programme ou une épreuve nommés par la grille, là où on les cherche.
    ② CONTEXTE D'APPEL — `fonction_existe` et `epreuve_existe`, une fois par référence.
    ③ ENTRÉE — `racine` : le dépôt · `chemin_rel` : « programmes/M.py » ou « tests/F.py » · `branche` : None (l'arbre de
      travail) ou une référence git (« origin/lot-r505-W2b ») lue par `git show`.
    ④ CONDITIONS D'ENTRÉE — Pour une branche, la racine est un dépôt git qui la connaît.
    ⑤ SORTIE — UNE valeur : le texte (UTF-8), ou None si le fichier n'existe pas là.
      [rend: 1]
    ⑥ TRAITEMENT — ① sans branche : ouvrir racine/chemin_rel s'il existe · ② avec branche : `git -C racine show
      branche:chemin_rel` ; un refus de git vaut « absent ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Avant que le Chat réunisse les lots, la fonction d'un lot n'est que sur sa branche (--voir-les-lots).
    ⑨ CE QUI CLOCHE — Un fichier illisible en UTF-8 lève UnicodeDecodeError : l'appelant en fait une faute. Un git
      absent vaut « absent » : sens prudent (la ligne rougit).
    ⑩ EFFET — Lit un fichier ou lance `git show` en lecture.
    ⑪ TERMINAISON — Rend la main ; `git show` est borné à 60 secondes.
      [sort: non]
    """
    if branche is None:
        chemin = os.path.join(racine, chemin_rel)
        if not os.path.isfile(chemin):
            return None
        with open(chemin, encoding="utf-8") as f:
            return f.read()
    return _git_show_memorise(racine, branche, chemin_rel)


@functools.lru_cache(maxsize=512)
def _git_show_memorise(racine, branche, chemin_rel):
    """Rend `git -C racine show branche:chemin_rel` décodé en UTF-8, ou None ; mémorisé le temps du processus.

    ① RÔLE — Lire un fichier d'une branche de lot une seule fois par processus.
    ② CONTEXTE D'APPEL — `_texte_du_depot`, avec une branche.
    ③ ENTRÉE — `racine` : le dépôt · `branche` : la référence git · `chemin_rel` : le chemin dans l'arbre.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte, ou None si git refuse (fichier ou branche absents, git introuvable).
      [rend: 1]
    ⑥ TRAITEMENT — `git show`, borné à 60 secondes ; mémoire de 512 entrées.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — L'épreuve contrôle la grille des dizaines de fois : sans mémoire, chaque contrôle relançait git
      pour chacune des quelque 70 références des lots.
    ⑨ CE QUI CLOCHE — Une branche poussée de nouveau pendant le processus n'est pas relue : sans effet sur un
      contrôle, qui dure quelques secondes.
    ⑩ EFFET — Lance `git show` en lecture.
    ⑪ TERMINAISON — Rend la main ; `git show` est borné à 60 secondes.
      [sort: non]
    """
    try:
        r = subprocess.run(["git", "-C", racine, "show", "%s:%s" % (branche, chemin_rel)], capture_output=True,
                           timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return r.stdout.decode("utf-8") if r.returncode == 0 else None


def fonction_existe(racine, ref, branche=None):
    """Dit si `MODULE:fonction` (ou `MODULE:Classe.methode`) est défini dans programmes/MODULE.py.

    ① RÔLE — Vérifier qu'une fonction nommée par la grille existe vraiment.
    ② CONTEXTE D'APPEL — `controler`, pour chaque fonction nommée (une seconde fois sur la branche citée, avec
      --voir-les-lots).
    ③ ENTRÉE — `racine` : le dépôt · `ref` : « MODULE:fonction » · `branche` : None (l'arbre de travail) ou une
      référence git.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : une phrase qui dit pourquoi la fonction n'existe pas, ou "" si elle existe.
      [rend: 1]
    ⑥ TRAITEMENT — ① exiger la forme · ② lire programmes/MODULE.py (`_texte_du_depot`) · ③ chercher, au premier
      niveau de son arbre syntaxique, une définition de fonction (ou une classe puis sa méthode) de ce nom.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — L'arbre syntaxique, et non l'import : importer exécute le programme (⑧ du programme).
    ⑨ CE QUI CLOCHE — Une fonction définie à l'intérieur d'une autre, ou créée à l'exécution, n'est pas vue : elle
      rougit, sens prudent. Une fonction qui existe mais ne fait rien (« return 1 ») passe : le fond est au relecteur.
    ⑩ EFFET — Lit un fichier, ou lance `git show`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    m = re.fullmatch(r"([A-Za-z_][\w-]*):([A-Za-z_]\w*)(?:\.([A-Za-z_]\w*))?", ref)
    if not m:
        return "forme fausse « %s » (attendu MODULE:fonction)" % ref
    ou = "programmes/%s.py%s" % (m.group(1), " sur %s" % branche if branche else "")
    try:
        texte = _texte_du_depot(racine, "programmes/%s.py" % m.group(1), branche)
        if texte is None:
            return "%s n'existe pas" % ou
        arbre = ast.parse(texte)
    except (SyntaxError, UnicodeDecodeError) as ex:
        return "%s illisible (%s)" % (ou, type(ex).__name__)
    for n in arbre.body:
        if m.group(3) is None and isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == m.group(2):
            return ""
        if m.group(3) is not None and isinstance(n, ast.ClassDef) and n.name == m.group(2):
            if any(isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef)) and x.name == m.group(3) for x in n.body):
                return ""
    return "%s n'est pas défini dans %s" % (ref.split(":", 1)[1], ou)


def cas_dans_l_arbre(arbre, cas):
    """Dit si l'arbre syntaxique d'une épreuve DÉFINIT le cas `cas` (défaut D2 de la relecture du 27-11-2026).

    ① RÔLE — Reconnaître un vrai cas d'épreuve, et refuser un mot qui n'est qu'un commentaire ou un texte.
    ② CONTEXTE D'APPEL — `epreuve_existe`, une fois par épreuve nommée.
    ③ ENTRÉE — `arbre` : l'arbre de `ast.parse` du fichier d'épreuve · `cas` : le nom du cas (« E3 », « G6 », « F10 »,
      « e06_cycles_regle_des_auteurs »).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : vrai si le cas est défini.
      [rend: 1]
    ⑥ TRAITEMENT — Parcourir tout l'arbre ; le cas est défini si l'on trouve ① une définition de fonction dont le nom
      est le cas, sans tenir compte des majuscules (« def e3 » pour E3 : les épreuves du projet nomment ainsi leurs cas) ;
      ou ② un appel, autre que print, dont le PREMIER argument est la chaîne exacte du cas (« essai("E3", e3) »,
      « voulu("F10") », « @cas("G1") ») ; ou ③ un couple ou une liste d'au moins deux éléments dont le premier est la
      chaîne exacte du cas (« ("E1", e1) »).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un commentaire « # CAS1 » n'est dans aucun arbre : il ne prouve rien. Le défaut D2 : toute la grille
      BRANCHÉE sur une épreuve faite d'un seul commentaire ouvrait le verrou. Les trois formes ① ② ③ sont celles que
      les épreuves des lots du 27-11-2026 emploient réellement (mesuré sur W2b, W2c, W2d, W2e, L2, L3FIX, L5CORR et le
      tri du 11-11).
    ⑨ CE QUI CLOCHE — Une chaîne écrite comme premier élément d'un couple de données, sans être un cas, passe encore ;
      un nom de fonction quelconque (« main ») passe aussi : le relecteur juge si c'est le bon cas.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    for n in ast.walk(arbre):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.lower() == cas.lower():
            return True
        if isinstance(n, ast.Call) and n.args and isinstance(n.args[0], ast.Constant) and n.args[0].value == cas:
            if not (isinstance(n.func, ast.Name) and n.func.id == "print"):
                return True
        if isinstance(n, (ast.Tuple, ast.List)) and len(n.elts) >= 2 and isinstance(n.elts[0], ast.Constant) \
                and n.elts[0].value == cas:
            return True
    return False


def epreuve_existe(racine, ref, branche=None):
    """Dit si `FICHIER.py:CAS` existe : tests/FICHIER.py présent, et CAS défini dans son arbre syntaxique.

    ① RÔLE — Vérifier qu'une épreuve nommée par la grille existe vraiment.
    ② CONTEXTE D'APPEL — `controler`, pour chaque épreuve nommée (une seconde fois sur la branche citée, avec
      --voir-les-lots).
    ③ ENTRÉE — `racine` : le dépôt · `ref` : « FICHIER.py:CAS » (« tests/ » devant est admis) · `branche` : None ou
      une référence git.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : une phrase qui dit pourquoi l'épreuve n'existe pas, ou "" si elle existe.
      [rend: 1]
    ⑥ TRAITEMENT — ① exiger la forme, le cas étant un nom (lettres, chiffres, « _ ») · ② lire tests/FICHIER.py · ③ le
      cas doit être défini dans l'arbre (`cas_dans_l_arbre`).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve sans cas désigné ne dit pas ce qu'elle prouve ; un fichier seul ne suffit pas ; un mot
      en commentaire non plus (défaut D2).
    ⑨ CE QUI CLOCHE — Voir ⑨ de `cas_dans_l_arbre`. Que le cas ROUGISSE sans la fonction n'est pas prouvé ici.
    ⑩ EFFET — Lit un fichier, ou lance `git show`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    m = re.fullmatch(r"(?:tests/)?([\w.-]+\.py):([A-Za-z_]\w*)", ref)
    if not m:
        return "forme fausse « %s » (attendu FICHIER.py:CAS, CAS étant un nom)" % ref
    ou = "tests/%s%s" % (m.group(1), " sur %s" % branche if branche else "")
    try:
        texte = _texte_du_depot(racine, "tests/" + m.group(1), branche)
        if texte is None:
            return "%s n'existe pas" % ou
        arbre = ast.parse(texte)
    except (SyntaxError, UnicodeDecodeError) as ex:
        return "%s illisible (%s)" % (ou, type(ex).__name__)
    if not cas_dans_l_arbre(arbre, m.group(2)):
        return "le cas %s n'est pas défini dans %s (ni fonction, ni cas nommé)" % (m.group(2), ou)
    return ""


def empreintes(bloc, identifiants):
    """Rend les deux empreintes du recalage : celle de la loi et celle de la liste des lignes (défaut D4).

    ① RÔLE — La propriété « la loi change → la grille rougit », et « une ligne disparaît → la grille rougit ».
    ② CONTEXTE D'APPEL — `controler`, une fois ; l'épreuve.
    ③ ENTRÉE — `bloc` : le bloc de la loi (`bloc_de_la_loi`) · `identifiants` : les identifiants des lignes de la grille.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : l'empreinte sha256 (64 caractères hexadécimaux) du bloc ramené à ses mots (`_nu`), et
      celle des identifiants triés, joints par un retour à la ligne.
      [rend: 2]
    ⑥ TRAITEMENT — sha256 sur l'UTF-8 de chaque texte.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — L'extraction par numéros ne voit pas une phrase nouvelle sans numéro (D4, S8 de la relecture), ni une
      ligne non numérotée supprimée (S7) ; une empreinte du TOUT les voit, quelle que soit la forme (R-505 v2 n'a pas
      encore de marque par critère). Le bloc est ramené à ses mots : un retour à la ligne n'est pas un changement de la
      loi, comme pour les extraits.
    ⑨ CE QUI CLOCHE — L'empreinte dit QU'il y a un changement, pas lequel : le relecteur compare les deux textes.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    loi = hashlib.sha256(_nu(bloc).encode("utf-8")).hexdigest()
    lignes = hashlib.sha256("\n".join(sorted(identifiants)).encode("utf-8")).hexdigest()
    return loi, lignes


def _liste(case):
    """Découpe une case à plusieurs valeurs séparées par « , ».

    ① RÔLE — Lire les cases `fonction`, `epreuve` et `seuils_de_la_loi`.
    ② CONTEXTE D'APPEL — `controler`, trois fois par ligne.
    ③ ENTRÉE — `case` : le texte de la case, ou None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des valeurs non vides.
      [rend: 1]
    ⑥ TRAITEMENT — Couper aux virgules, ôter les blancs, écarter les vides.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un critère peut être appliqué par deux fonctions et prouvé par deux cas.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return [x.strip() for x in (case or "").split(",") if x.strip()]


def _existe_ici_ou_sur_le_lot(racine, ref, verifier, constat, voir_les_lots):
    """Vérifie une fonction ou une épreuve dans le dépôt, puis, avec --voir-les-lots, sur la branche que cite le constat.

    ① RÔLE — Dire si une référence existe, et où elle a été vue.
    ② CONTEXTE D'APPEL — `controler`, pour chaque fonction et chaque épreuve nommées.
    ③ ENTRÉE — `racine` : le dépôt · `ref` : la référence · `verifier` : `fonction_existe` ou `epreuve_existe` ·
      `constat` : la case constat de la ligne · `voir_les_lots` : vrai pour chercher aussi sur la branche citée.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : la raison de l'absence ("" si elle existe), et la branche où elle a été vue (None si
      elle est dans le dépôt, ou absente).
      [rend: 2]
    ⑥ TRAITEMENT — ① dans le dépôt · ② sinon, si voir_les_lots, sur chaque « branche origin/… » citée par le constat,
      dans l'ordre · ③ sinon la raison du dépôt.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les lots du 27-11-2026 vivent sur des branches à part tant que le Chat ne les a pas réunis ; la
      relecture doit pouvoir vérifier la grille avant la réunion, sans jamais ouvrir le verrou du juge (les portes
      n'emploient pas ce mode).
    ⑨ CE QUI CLOCHE — Une branche supprimée après la réunion n'est plus lue : la fonction doit alors être dans le dépôt.
    ⑩ EFFET — Lit des fichiers ; peut lancer `git show`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    r = verifier(racine, ref)
    if not r or not voir_les_lots:
        return r, None
    for branche in re.findall(r"branche (origin/[\w./-]+[\w])", constat or ""):
        if not verifier(racine, ref, branche):
            return "", branche
    return r, None


def controler(racine, chemin_grille=None, source_loi=None, source_backlog=None, voir_les_lots=False):
    """Confronte la grille à la loi, au BACKLOG, aux programmes et aux épreuves.

    ① RÔLE — Le contrôle entier, rendu en données pour `main` et pour les deux portes.
    ② CONTEXTE D'APPEL — `main` ; `motifs_de_refus_du_verdict` ; `motifs_de_refus_de_la_mise_en_direct` ; l'épreuve.
    ③ ENTRÉE — `racine` : le dépôt · `chemin_grille` : la grille (défaut : CONTRATS.GRILLE_R505 sous la racine) ·
      `source_loi` : la loi (défaut LOI_PAR_DEFAUT) · `source_backlog` : le BACKLOG (défaut BACKLOG_PAR_DEFAUT) ·
      `voir_les_lots` : vrai pour chercher aussi les références absentes sur la branche citée (③ du programme).
    ④ CONDITIONS D'ENTRÉE — Voir ④ du programme.
    ⑤ SORTIE — UNE valeur : un dictionnaire de huit clés — `fautes` (liste de phrases), `non_branchees` (identifiants
      DÉCIDÉ_NON_BRANCHÉ), `non_branchees_du_verdict` (les mêmes, hors étapes 6 et DIRECT : A-1109), `pretes` (non
      branchées dont fonction et épreuve existent déjà : à passer BRANCHÉ après relecture), `plus_tard` (identifiants
      PLUS_TARD), `vus_sur_un_lot` (« identifiant : référence sur branche », avec voir_les_lots), `empreintes`
      ({loi, lignes} : celles du texte lu, à recopier au recalage), `comptes` ({lignes, branchees, ids_de_la_loi,
      seuils}).
      [rend: 1]
    ⑥ TRAITEMENT — ① lire le contrat, la grille (en-tête égal au contrat, sinon faute), la loi (bloc R-505 v2) et le
      BACKLOG · ② par ligne : identifiant unique et non vide ; role, etape, etat dans les valeurs du contrat ; decisions
      portant au moins un A-nnn (D5), et chaque A-nnn présent au BACKLOG en tête de ligne de table ; extrait non vide et
      retrouvé dans la loi aux espaces près ; pour un identifiant numéroté, extrait dans LE paragraphe où la loi le
      numérote ; hors PLUS_TARD, rôle égal au rôle que dit la loi (D3 : AFFICHE si l'identifiant commence par AFF-, si
      l'extrait porte un mot d'affichage, ou si tous ses seuils sont retirés ; DÉCIDE sinon) ; chaque seuil réclamé
      dans la table, et jamais un seuil retiré par une ligne qui DÉCIDE ; chaque fonction et épreuve nommées
      existantes ; BRANCHÉ exige au moins une fonction et une épreuve ; PLUS_TARD exige « plus tard » dans le même
      paragraphe de la loi, avant ou dans l'extrait · ③ TOUJOURS (D1) : une grille sans ligne est une faute ; chaque
      identifiant numéroté de la loi a sa ligne ; chaque seuil non retiré est réclamé · ④ les empreintes de la loi et
      des lignes égales à celles de la ligne LOI-EMPREINTE (D4).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir ⑧ du programme. D1 à D6 : relecture neuve du lot L4, 27-11-2026 (fichier de preuve V1_RELU_L4).
    ⑨ CE QUI CLOCHE — Voir ⑨ du programme.
    ⑩ EFFET — Lit des fichiers ; peut lancer `git show`.
    ⑪ TERMINAISON — Rend la main ; lève ErreurDeLecture si une entrée manque.
      [sort: non]
    """
    C = _contrat()
    colonnes = list(C.GRILLE_R505_V2)
    chemin_grille = chemin_grille or os.path.join(racine, C.GRILLE_R505)
    if not os.path.isfile(chemin_grille):
        raise ErreurDeLecture("grille introuvable : %s" % chemin_grille)
    bloc = bloc_de_la_loi(lire_une_source(racine, source_loi or LOI_PAR_DEFAUT))
    backlog = lire_une_source(racine, source_backlog or BACKLOG_PAR_DEFAUT)
    actions = set(re.findall(r"(?m)^\| (A-\d+) \|", backlog))
    if not actions:
        raise ErreurDeLecture("le BACKLOG lu ne porte aucune action « | A-nnn | »")
    ids_loi, seuils_loi = identifiants_de_la_loi(bloc)
    paras = [p for p in bloc.split("\n") if p.strip()]
    paras_nus = [_nu(p) for p in paras]
    bloc_nu = _nu(bloc)
    fautes, non_branchees, pretes, plus_tard, vus, reclames = [], [], [], [], set(), set()
    du_verdict, sur_un_lot, constat_d_empreinte = [], [], None
    with open(chemin_grille, encoding="utf-8", newline="") as f:
        lecteur = csv.DictReader(f, delimiter=";")
        if list(lecteur.fieldnames or []) != colonnes:
            fautes.append("en-tête de la grille différent du contrat GRILLE_R505_V2 : %s" % lecteur.fieldnames)
            lignes = []
        else:
            lignes = list(lecteur)
    forme_numerotee = re.compile(r"(E[2-6]-S?\d+|AFF-\d+|DIR-\d+|VERDICT-\d+)")
    branchees = 0
    for n, l in enumerate(lignes, 2):
        ident = (l.get("identifiant") or "").strip()
        ou = "ligne %d (%s)" % (n, ident or "sans identifiant")
        if None in l or any(v is None for v in l.values()):
            fautes.append("%s : nombre de cases différent de l'en-tête" % ou)
            continue
        if not ident:
            fautes.append("%s : identifiant vide" % ou)
            continue
        if ident in vus:
            fautes.append("%s : identifiant écrit deux fois" % ou)
        vus.add(ident)
        if ident == LIGNE_D_EMPREINTE:
            constat_d_empreinte = l["constat"]
        if l["role"] not in C.ROLES_DE_LA_GRILLE:
            fautes.append("%s : role « %s » hors contrat %s" % (ou, l["role"], C.ROLES_DE_LA_GRILLE))
        if l["etape"] not in C.ETAPES_DE_LA_GRILLE:
            fautes.append("%s : etape « %s » hors contrat" % (ou, l["etape"]))
        if l["etat"] not in C.ETATS_DE_LA_GRILLE:
            fautes.append("%s : etat « %s » hors contrat %s" % (ou, l["etat"], C.ETATS_DE_LA_GRILLE))
        if not l["decisions"].strip():
            fautes.append("%s : aucune décision citée" % ou)
        elif not re.search(r"A-\d+", l["decisions"]):
            fautes.append("%s : aucune décision du BACKLOG (A-nnn) dans « %s »" % (ou, l["decisions"]))
        for a in re.findall(r"A-\d+", l["decisions"]):
            if a not in actions:
                fautes.append("%s : %s absente du BACKLOG lu" % (ou, a))
        extrait = _nu(l["phrase_de_la_loi"])
        if not extrait:
            fautes.append("%s : phrase_de_la_loi vide" % ou)
        elif extrait not in bloc_nu:
            fautes.append("%s : l'extrait n'est pas dans la loi, mot pour mot : « %s »" % (ou, extrait[:80]))
        elif forme_numerotee.fullmatch(ident):
            if ident not in ids_loi:
                fautes.append("%s : la loi ne numérote pas ce critère" % ou)
            elif extrait not in _nu(ids_loi[ident]):
                fautes.append("%s : l'extrait n'est pas dans le paragraphe où la loi numérote %s" % (ou, ident))
        if l["etat"] == "PLUS_TARD" and extrait and extrait in bloc_nu:
            para = next((q for q in paras_nus if extrait in q), "")
            if "plus tard" not in para[:para.find(extrait) + len(extrait)].lower():
                fautes.append("%s : PLUS_TARD sans « plus tard » dans la loi, avant ou dans l'extrait" % ou)
        seuils = _liste(l["seuils_de_la_loi"])
        for s in seuils:
            reclames.add(s)
            if s not in seuils_loi:
                fautes.append("%s : seuil « %s » absent de la table de la loi" % (ou, s))
            elif seuils_loi[s] and l["role"] == "DÉCIDE":
                fautes.append("%s : DÉCIDE avec le seuil « %s », que la loi a retiré (valeur « — »)" % (ou, s))
        if l["etat"] != "PLUS_TARD" and l["role"] in C.ROLES_DE_LA_GRILLE:
            affiche = (ident.startswith("AFF-") or bool(MOTS_D_AFFICHAGE.search(extrait))
                       or bool(seuils and all(seuils_loi.get(s) for s in seuils)))
            attendu = "AFFICHE" if affiche else "DÉCIDE"
            if l["role"] != attendu:
                fautes.append("%s : role %s, la loi dit %s (préfixe AFF-, mots d'affichage de l'extrait, seuils "
                              "retirés)" % (ou, l["role"], attendu))
        fonctions, epreuves = _liste(l["fonction"]), _liste(l["epreuve"])
        trouvees = []
        for ref, verifier, quoi in ([(x, fonction_existe, "fonction") for x in fonctions]
                                    + [(x, epreuve_existe, "épreuve") for x in epreuves]):
            r, branche = _existe_ici_ou_sur_le_lot(racine, ref, verifier, l["constat"], voir_les_lots)
            if r:
                fautes.append("%s : %s %s" % (ou, quoi, r))
            else:
                trouvees.append(ref)
                if branche:
                    sur_un_lot.append("%s : %s sur %s" % (ident, ref, branche))
        if l["etat"] == "BRANCHÉ":
            if not fonctions or not epreuves:
                fautes.append("%s : BRANCHÉ sans %s" % (ou, "fonction" if not fonctions else "épreuve"))
            else:
                branchees += 1
        elif l["etat"] == "DÉCIDÉ_NON_BRANCHÉ":
            non_branchees.append(ident)
            if l["etape"] not in ETAPES_DE_LA_MISE_EN_DIRECT:
                du_verdict.append(ident)
            if fonctions and epreuves and len(trouvees) == len(fonctions) + len(epreuves):
                pretes.append(ident)
        elif l["etat"] == "PLUS_TARD":
            plus_tard.append(ident)
    # ③ le lien loi → grille se fait TOUJOURS, même sur une grille vide (défaut D1)
    if not lignes:
        fautes.append("la grille ne porte aucune ligne : le lien loi → grille ne se saute jamais")
    for ident in sorted(set(ids_loi) - vus):
        fautes.append("la loi porte %s, la grille n'a pas sa ligne" % ident)
    for s in sorted(k for k, retire in seuils_loi.items() if not retire and k not in reclames):
        fautes.append("le seuil « %s » de la loi n'est réclamé par aucune ligne" % s)
    # ④ la loi change → la grille rougit (défaut D4)
    e_loi, e_lignes = empreintes(bloc, vus)
    if constat_d_empreinte is None:
        fautes.append("la grille n'a pas de ligne %s : la loi peut changer sans que la grille rougisse"
                      % LIGNE_D_EMPREINTE)
    else:
        portee = dict(re.findall(r"\b(loi|lignes)=([0-9a-f]{64})\b", constat_d_empreinte))
        if portee.get("loi") != e_loi:
            fautes.append("la loi a changé depuis le dernier recalage de la grille (empreinte du texte lu : loi=%s) :"
                          " relire chaque ligne contre la loi, puis recopier l'empreinte dans %s" % (e_loi,
                                                                                       LIGNE_D_EMPREINTE))
        if portee.get("lignes") != e_lignes:
            fautes.append("les lignes de la grille ont changé depuis le dernier recalage (empreinte des identifiants "
                          "lus : lignes=%s) : une ligne retirée ou ajoutée se relit, puis l'empreinte se recopie dans "
                          "%s" % (e_lignes, LIGNE_D_EMPREINTE))
    return {"fautes": fautes, "non_branchees": non_branchees, "non_branchees_du_verdict": du_verdict,
            "pretes": pretes, "plus_tard": plus_tard, "vus_sur_un_lot": sur_un_lot,
            "empreintes": {"loi": e_loi, "lignes": e_lignes},
            "comptes": {"lignes": len(lignes), "branchees": branchees, "ids_de_la_loi": len(ids_loi),
                        "seuils": len(seuils_loi)}}


def motifs_de_refus_du_verdict(racine, chemin_grille=None, source_loi=None, source_backlog=None):
    """Rend les raisons de REFUSER un verdict de R-505 v2 ; une liste vide seulement si les étapes 1 à 5 sont branchées.

    ① RÔLE — Le verrou que Jean-Luc a demandé (A-1067 ②) : « le juge REFUSE de rendre un verdict tant qu'un critère
      décidé n'est pas branché », réglé PAR ÉTAPE par A-1109 : le verdict attend les lignes des étapes 1 à 5 (et les
      lignes PRINCIPE, VERDICT, AFFICHAGE), pas celles de l'étape 6 ni du suivi en direct.
    ② CONTEXTE D'APPEL — Le juge, juste avant de rendre un verdict (appel posé à l'installation, étape I1) : si la liste
      n'est pas vide, aucun verdict n'est rendu et la liste est écrite. L'épreuve.
    ③ ENTRÉE — `racine`, `chemin_grille`, `source_loi`, `source_backlog` : comme `controler`.
    ④ CONDITIONS D'ENTRÉE — Aucune : toute impossibilité devient un motif.
    ⑤ SORTIE — UNE valeur : une liste de phrases. Vide = le verdict peut sortir.
      [rend: 1]
    ⑥ TRAITEMENT — Appeler `controler` (jamais en mode --voir-les-lots) ; motifs = chaque faute, puis une phrase par
      ligne DÉCIDÉ_NON_BRANCHÉ hors étapes 6 et DIRECT ; une exception, quelle qu'elle soit, devient un motif.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Fermé par défaut : une grille illisible, absente, vide ou fausse ne laisse jamais passer un verdict
      (R-734).
    ⑨ CE QUI CLOCHE — Les lignes PLUS_TARD ne bloquent pas : c'est la loi qui les dit « plus tard », et le programme
      l'exige mot pour mot ; décider qu'une ligne passe en PLUS_TARD reste un changement de la grille, relu, et qui
      change l'empreinte des lignes.
    ⑩ EFFET — Celui de `controler`.
    ⑪ TERMINAISON — Rend la main, toujours.
      [sort: non]
    """
    try:
        r = controler(racine, chemin_grille, source_loi, source_backlog)
    except Exception as ex:  # fermé par défaut : toute panne refuse
        return ["grille non contrôlée (%s) : %s" % (type(ex).__name__, ex)]
    return list(r["fautes"]) + ["critère décidé non branché : %s" % i for i in r["non_branchees_du_verdict"]]


def motifs_de_refus_de_la_mise_en_direct(racine, chemin_grille=None, source_loi=None, source_backlog=None):
    """Rend les raisons de REFUSER une mise en direct ; une liste vide seulement si TOUTES les lignes sont branchées.

    ① RÔLE — La seconde porte d'A-1109 : « la MISE EN DIRECT attend en plus celles de l'étape 6 et du suivi en
      direct ».
    ② CONTEXTE D'APPEL — Le programme qui ferait passer une stratégie validée en direct (étape 6), avant de le faire
      (appel à poser à l'installation, étape I1). L'épreuve.
    ③ ENTRÉE — `racine` : le dépôt · `chemin_grille` : la grille (défaut : celle du contrat) · `source_loi` : la loi ·
      `source_backlog` : le BACKLOG — comme `controler`.
    ④ CONDITIONS D'ENTRÉE — Aucune : toute impossibilité devient un motif.
    ⑤ SORTIE — UNE valeur : une liste de phrases. Vide = la mise en direct peut se faire.
      [rend: 1]
    ⑥ TRAITEMENT — Appeler `controler` ; motifs = chaque faute, puis une phrase par ligne DÉCIDÉ_NON_BRANCHÉ, quelle
      que soit son étape ; une exception devient un motif.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — « Rien ne passe en direct sans l'étape 6 branchée » (A-1109).
    ⑨ CE QUI CLOCHE — Comme `motifs_de_refus_du_verdict`.
    ⑩ EFFET — Celui de `controler`.
    ⑪ TERMINAISON — Rend la main, toujours.
      [sort: non]
    """
    try:
        r = controler(racine, chemin_grille, source_loi, source_backlog)
    except Exception as ex:  # fermé par défaut : toute panne refuse
        return ["grille non contrôlée (%s) : %s — aucune mise en direct" % (type(ex).__name__, ex)]
    return list(r["fautes"]) + ["critère décidé non branché : %s" % i for i in r["non_branchees"]]


def main():
    """Lance le contrôle depuis la ligne de commande et sort avec son code.

    ① RÔLE — Rendre le contrôle visible au relecteur, au maréchal et au circuit.
    ② CONTEXTE D'APPEL — La ligne de commande (② du programme).
    ③ ENTRÉE — sys.argv : `--racine`, `--grille`, `--loi`, `--backlog`, `--voir-les-lots` (③ du programme).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Aucune valeur : le code de sortie 0, 1, 2 ou 3 (⑤ du programme).
      [rend: rien]
    ⑥ TRAITEMENT — Lire les options ; appeler `controler` ; afficher les comptes, les fautes, les lignes non branchées
      (et celles qui retiennent le verdict), les lignes prêtes, PLUS_TARD et vues sur un lot, les empreintes ; sortir.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Quatre codes, pour que « pas encore branché » (1) ne se confonde ni avec une grille fausse (2) ni avec
      un contrôle qui n'a pas tourné (3).
    ⑨ CE QUI CLOCHE — Une option inconnue est une faute d'usage : code 3. Le code 0 dit « tout est branché » au sens de
      la mise en direct ; le verdict peut être permis avant (A-1109), ce que la ligne « PORTE DU VERDICT » affiche.
    ⑩ EFFET — Écrit à l'écran.
    ⑪ TERMINAISON — Sort du programme, toujours.
      [sort: oui]
    """
    args, opts = sys.argv[1:], {}
    while args:
        a = args.pop(0)
        if a in ("--racine", "--grille", "--loi", "--backlog") and args:
            opts[a[2:]] = args.pop(0)
        elif a == "--voir-les-lots":
            opts["lots"] = True
        else:
            print("CONTROLER_LA_GRILLE : option inconnue ou sans valeur « %s »" % a)
            sys.exit(3)
    racine = os.path.abspath(opts.get("racine") or os.path.dirname(ICI))
    try:
        r = controler(racine, opts.get("grille"), opts.get("loi"), opts.get("backlog"), bool(opts.get("lots")))
    except Exception as ex:
        print("CONTROLER_LA_GRILLE : LE CONTRÔLE N'A PAS PU TOURNER (%s) : %s" % (type(ex).__name__, ex))
        sys.exit(3)
    c = r["comptes"]
    print("CONTROLER_LA_GRILLE — %d ligne(s) · %d BRANCHÉE(S) · %d DÉCIDÉE(S) NON BRANCHÉE(S) · %d PLUS_TARD · "
          "%d critère(s) numéroté(s) par la loi · %d seuil(s) dans sa table"
          % (c["lignes"], c["branchees"], len(r["non_branchees"]), len(r["plus_tard"]), c["ids_de_la_loi"],
             c["seuils"]))
    for x in r["fautes"]:
        print("  FAUTE : " + x)
    if r["non_branchees"]:
        print("  NON BRANCHÉES : " + " ".join(r["non_branchees"]))
    print("  PORTE DU VERDICT (A-1109, étapes 1 à 5) : %s" % (
        "FERMÉE — %d ligne(s) non branchée(s)" % len(r["non_branchees_du_verdict"]) if r["non_branchees_du_verdict"]
        else ("FERMÉE PAR LES FAUTES" if r["fautes"] else "OUVERTE")))
    if r["pretes"]:
        print("  PRÊTES (fonction et épreuve existent, à relire puis passer BRANCHÉ) : " + " ".join(r["pretes"]))
    if r["plus_tard"]:
        print("  PLUS TARD (la loi le dit) : " + " ".join(r["plus_tard"]))
    for x in r["vus_sur_un_lot"]:
        print("  VU SUR UN LOT SEULEMENT (--voir-les-lots ; absent du dépôt) : " + x)
    print("  EMPREINTES DU TEXTE LU : loi=%s lignes=%s" % (r["empreintes"]["loi"], r["empreintes"]["lignes"]))
    if r["fautes"]:
        print("VERDICT DU CONTRÔLE : GRILLE FAUSSE — code 2")
        sys.exit(2)
    if r["non_branchees"]:
        print("VERDICT DU CONTRÔLE : %d CRITÈRE(S) DÉCIDÉ(S) NON BRANCHÉ(S) — AUCUN VERDICT NE PEUT SORTIR — code 1"
              % len(r["non_branchees"]) if r["non_branchees_du_verdict"] else
              "VERDICT DU CONTRÔLE : %d CRITÈRE(S) DE L'ÉTAPE 6 OU DU DIRECT NON BRANCHÉ(S) — VERDICT PERMIS, AUCUNE "
              "MISE EN DIRECT — code 1" % len(r["non_branchees"]))
        sys.exit(1)
    print("VERDICT DU CONTRÔLE : TOUT CRITÈRE DÉCIDÉ EST BRANCHÉ — code 0")
    sys.exit(0)


if __name__ == "__main__":
    main()
