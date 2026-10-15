#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fait jouer une stratégie par le juge des stratégies, puis produit les mesures que le
juge à huit critères attend.

USAGE : python3 JUGER_SUR_8_CRITERES.py <racine> [--calibrage] [--strategie ID]
CODE : 0 = mesuré · 1 = calibrage échoué, rien produit · 2 = source absente

① RÔLE — Relier deux programmes qui existaient sans se parler. `JUGE_DES_STRATEGIES.py`
  sait rejouer une stratégie sur l'historique des cours et rendre la liste des
  opérations qu'elle aurait faites. `MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py`
  porte les huit calculs de la grille d'évaluation, et le juge à huit critères qui en tire un
  score sur huit. Aucun des deux n'appelait l'autre. Ce programme est ce
  branchement : il prend les opérations rendues par le juge des stratégies, les met dans la
  forme que les calculs attendent, appelle ces calculs, et affiche ce qu'ils
  rendent. Il n'écrit aucun calcul de son cru. Mesuré le 19-09-2026 sur la
  stratégie C5E10-OBS-V1 : 103 opérations jouées, taux de réussite 63,1 %,
  p-value 0,0078, chute maximale 14,3 %, 85 jours sous l'eau, Kelly fractionnel
  0,1886, cinq mesures chiffrées sur les neuf attendues.
② CONTEXTE D'APPEL — À la main, en ligne de commande, et rien d'autre. AUCUN
  LANCEUR AUTOMATIQUE : le 19-09-2026, une recherche du nom `JUGER` dans les
  deux tâches planifiées du dépôt — `.github/workflows/collecte_abc.yml` et
  `.github/workflows/comparer_google_abc.yml` — puis dans `programmes/` et dans
  `prompts_taches/`, ne rend aucune ligne hors de l'en-tête de ce fichier et du
  tableau d'une consigne de commentage. Et `gouvernance/SOCLE.csv` le range
  ligne 133 en PRESUME, avec le motif « aucun lanceur detecte — un lancement a
  la main ne s ecrit nulle part ».
③ ENTRÉE — La ligne de commande, trois éléments. `<racine>` : le dossier à
  parcourir pour y trouver programmes et données, en pratique le dossier du
  dépôt cloné, écrit `.` quand on lance depuis ce dossier. `--calibrage` :
  s'arrêter après les contrôles de calibrage, sans rien jouer. `--strategie ID` :
  l'identifiant d'une ligne du registre des stratégies, par exemple
  `C5E10-OBS-V1`.
④ CONDITIONS D'ENTRÉE — La racine donnée doit porter, à n'importe quelle
  profondeur, quatre programmes et trois fichiers : `MODULE_STATISTIQUES_*`,
  `MODULE_POSITIONS.py`, `JUGE_DES_STRATEGIES.py`, `MODULE_C5_ETENDU_10_*`, un fichier
  dont le nom commence par `REFERENTIEL_VALEURS`, `REGISTRE_REGLES.md` et
  `cac40_strategies.csv`. Le REGISTRE doit porter le bloc de la grille
  GRILLE-26-04 avec ses seuils écrits en toutes lettres. La stratégie demandée
  doit exister au registre des stratégies et y porter un univers renseigné.
⑤ SORTIE — Un code de sortie, et des lignes affichées. 0 quand la mesure a été
  prise, 1 quand un calibrage a échoué ou qu'un seuil diverge, 2 quand une
  source est absente. Aucun fichier n'est écrit : tout le reste est affiché.
⑥ TRAITEMENT — ① sans argument, afficher ce texte et sortir en 2 · ② charger
  `MODULE_STATISTIQUES_*` depuis la racine, et sortir en 2 s'il est absent ·
  ③ calibrer le juge à huit critères sur les chiffres connus de la stratégie C5-EI au
  26-04-2026, et sortir en 1 s'il ne les reproduit plus · ④ calibrer le
  branchement lui-même sur 60 opérations fabriquées dont on connaît le résultat,
  et sortir en 1 s'il ne rend pas ce qu'il doit · ⑤ vérifier que les seuils de
  la grille s'écrivent au REGISTRE, et sortir en 1 sinon · ⑥ s'arrêter là si
  `--calibrage` est demandé · ⑦ charger `JUGE_DES_STRATEGIES.py`, et sortir en 2 s'il est
  absent · ⑧ si une stratégie est nommée, la jouer et afficher ses mesures ·
  ⑨ sinon, afficher ce qui manque encore pour produire un score, et rendre 0.
⑦ UNITÉ — Chaque mesure porte la sienne, et elles ne se mélangent pas. Le taux
  de réussite et la chute maximale sont des POURCENTS. La durée sous l'eau est
  un NOMBRE DE JOURS de calendrier. Les gains sont des EUROS, sur un capital de
  100 000 € par opération. Le taux de frais, le Kelly fractionnel, la p-value et
  les objectifs de gain et de perte sont des FRACTIONS entre 0 et 1, jamais des
  pourcents : 0,0015 vaut 15 points de base, et 0,04 vaut 4 %. L'horizon d'une
  stratégie est un NOMBRE DE SÉANCES de bourse.
⑧ POURQUOI — Le travail que ce programme refait existait déjà et a été perdu.
  Le 26-04-2026, une évaluation sur huit critères a été passée sur
  28 stratégies ; le fichier qui en portait les résultats complets,
  `resultats_FINAL_8c.json`, ne se retrouve ni au dépôt ni sur le Drive, et
  aucune des 68 lignes du registre
  des stratégies n'en porte la trace. Seuls subsistent les deux programmes qui
  savent faire le travail, et le résultat d'une seule stratégie, retenu dans un
  mémo. Refaire le pont coûte moins cher que retrouver le fichier.
  Le programme ne rend AUCUN SCORE, délibérément. Quatre des neuf mesures ne
  sont pas produites : mesuré le 19-09-2026 sur C5E10-OBS-V1, l'affichage annonce
  « 5 mesure(s) chiffrée(s) sur 9 ». Un score calculé sur cinq mesures et
  présenté comme un score sur huit critères serait indiscernable d'un vrai, et
  personne ne saurait qu'il manque la moitié de l'instrument.
  Et il ne modifie aucun statut de stratégie : il mesure, Jean-Luc décide.
⑨ CE QUI CLOCHE —
  ① Le code 0 annonce « mesuré » alors qu'il recouvre aussi « rien mesuré ».
  Mesuré le 19-09-2026 sur une copie du dépôt : `--strategie MA200-S1` affiche
  « univers « A TRANCHER — voir etude_ref » — INJOUABLE, rien mesuré. » et le
  code de sortie relevé juste après est 0, exactement comme pour C5E10-OBS-V1
  qui a produit cinq mesures. Une tâche qui ne regarderait que le code de sortie
  ne pourrait pas les distinguer. Un contrôle qui n'a pas pu tourner rend un code
  de sortie non nul (R-734).
  ② Le programme ne dit jamais QUAND il a mesuré. La zone horaire de Paris est
  préparée ligne 59 sous le nom `PARIS`, et `datetime` est importé ligne 56 :
  mesuré le 19-09-2026, ni l'un ni l'autre n'apparaît ailleurs dans le fichier,
  et aucune des lignes affichées ne porte de date. Deux passages sur des cours
  différents rendent donc des sorties que rien ne permet de dater ni d'ordonner,
  alors que le projet impose un horodatage de Paris en tête de tout ce qui est
  produit.
  ③ Quatre éléments importés ou préparés ne servent à rien. Mesuré le
  19-09-2026, `json` n'apparaît que dans un nom de fichier cité en commentaire,
  `csv` n'est employé nulle part sous ce nom — la fonction qui lit les fichiers
  à colonnes le réimporte pour elle seule sous le nom `_csv` —, `datetime` et
  `PARIS` ne sont jamais employés. Un lecteur qui voit `import json` cherche une
  écriture de fichier qui n'existe pas.
  ④ Lancé sans aucun argument, le programme affiche ce texte-ci EN ENTIER avant
  de sortir en 2, parce que la ligne 359 affiche le texte d'en-tête du fichier en
  guise de mode d'emploi. Ce texte tenait en quelques lignes ; commenté selon la
  règle qui impose les douze éléments (R-752), il en fait plusieurs centaines, et
  le mode d'emploi défile à l'écran. Les deux lignes USAGE et CODE sont pour
  cette raison placées en tête, juste sous le titre, afin de rester visibles au
  début du déroulement.
⑩ EFFET — N'ÉCRIT AUCUN FICHIER et ne touche pas au réseau. Vérifié le
  19-09-2026 : après un passage complet sur une copie du dépôt, la comparaison
  fichier par fichier avec l'original ne rend aucune différence, hors le dossier
  `__pycache__` que Python crée pour son propre compte. LIT l'arborescence de la
  racine donnée, plusieurs fois, et EXÉCUTE les programmes qu'il y trouve pour
  s'en servir : mesuré le 19-09-2026 en marquant `MODULE_POSITIONS.py`, ce
  fichier est exécuté 2 fois sur un passage `--calibrage` et 5 fois sur un
  passage `--strategie`. AFFICHE de quatre à une vingtaine de lignes.
⑪ TERMINAISON — SORT DU PROGRAMME avec le code rendu par `main` : 0, 1 ou 2. Et
  un de ses appels peut ne pas revenir : la lecture du taux de frais lève une
  erreur non rattrapée quand `MODULE_POSITIONS.py` ou son taux sont introuvables,
  et la conversion d'un objectif de gain ou de perte lève quand la case est vide
  ou porte du texte — mesuré le 19-09-2026, « ValueError: could not convert
  string to float: '' ». Dans les deux cas, la trace Python s'affiche et le code
  de sortie est 1.
⑫ DÉFINITIONS
  le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
  le juge à huit critères : `evaluer_strategie_8_criteres`, la fonction de
    `MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py` qui compare neuf mesures à
    leurs seuils et rend un score sur huit
  la grille : la liste des huit critères et de leurs seuils ; celle qui tourne s'appelle GRILLE-26-04 et vit dans `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740 de ce fichier
  une opération : un achat simulé suivi de sa revente, avec son gain net en
    euros ; aucun ordre réel n'est jamais passé
  le pont : le branchement entre le juge des stratégies et le juge à huit critères, qui est tout ce que ce
    programme ajoute
  le registre des stratégies : le fichier `cac40_strategies.csv`, une ligne par stratégie, qui porte leur état civil — identifiant, réglages, résultats connus
  le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
  l'univers : la liste des valeurs sur lesquelles une stratégie a le droit
    d'acheter, désignées par leur mnémonique
  la p-value : la probabilité qu'un taux de réussite au moins aussi bon soit
    obtenu par le seul hasard ; plus elle est petite, moins le hasard explique
    le résultat
  le Kelly fractionnel : la part du capital qu'il serait raisonnable d'engager
    sur une opération, compte tenu du taux de réussite et des gains et pertes
    attendus
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
    étant qu'une copie de lecture
  l'horizon : le nombre de séances pendant lesquelles une position est tenue si ni l'objectif de gain ni la perte acceptée ne sont atteints
  la durée sous l'eau : le nombre de jours pendant lesquels le cumul des gains reste sous son plus haut précédent
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
  la trace : la liste des sources avec leur etat — LU, ABSENT ou ILLISIBLE — et un detail chiffre, affichee en pied de page.
"""

import csv, importlib.util, json, os, sys
from datetime import datetime
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")

# Les chiffres de C5-EI au 26-04, et le résultat que le juge à huit critères DOIT rendre.
# Source : mémo ETAT_REFLEXION du 27-04-2026 08h05.
TEMOIN = {"p_value": 0.007, "dsr": 1.03, "pbo": 0.30, "dd_pct": 4.6,
          "underwater_jours": 119, "kelly_frac": 0.093, "stable": True,
          "wf_tous_positifs": True, "frais_pct": 0.005}
TEMOIN_ATTENDU = 7


def _charger(base, *noms):
    """Charge un programme voisin trouvé par son nom sous la racine, et le rend.

    ① RÔLE — Retrouver et rendre utilisable un programme du dépôt sans savoir
      d'avance dans quel dossier il vit. Les programmes ont déménagé : ils étaient
      à la racine, ils vivent aujourd'hui dans `programmes/`. Une recherche à plat
      ne les trouve plus, et un chemin écrit en dur serait à refaire au prochain
      rangement. Cette fonction parcourt toute l'arborescence, prend le premier
      fichier dont le nom correspond, l'exécute, et rend l'objet qui en résulte
      ainsi que le chemin où il a été trouvé.
    ② CONTEXTE D'APPEL — Quatre appelants, tous dans ce fichier : `_frais_taux`
      pour aller chercher le taux de frais dans `MODULE_POSITIONS.py`, `_juger_une`
      deux fois pour charger le module de signal et celui des positions, et `main`
      deux fois pour charger `MODULE_STATISTIQUES_*` puis `JUGE_DES_STRATEGIES.py`. Aucun
      appel depuis un autre programme : une recherche de `_charger(` dans tous les
      fichiers `.py` du dépôt, le 19-09-2026, ne rend aucune ligne hors de ce
      fichier.
    ③ ENTRÉE — `noms` reçu comme `*noms` : les noms de fichiers cherchés · `base` : le dossier à parcourir, sous-dossiers compris, qui est la
      racine donnée sur la ligne de commande et transmise sans modification par
      tous les appelants. `*noms` : un ou plusieurs noms de fichier à chercher ;
      tous les appels d'aujourd'hui n'en passent qu'un seul. Un nom qui se termine
      par une étoile désigne un début de nom : `MODULE_STATISTIQUES_*` retrouve
      `MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py`, dont la date fait partie du
      nom.
    ④ CONDITIONS D'ENTRÉE — Aucune. Une racine inexistante ne la fait pas tomber :
      le parcours ne rend simplement rien. C'est à l'appelant de vérifier ce qui
      est rendu.
    ⑤ SORTIE — DEUX valeurs, et sous deux formes selon la branche. Quand un fichier
      correspond : l'objet issu de son exécution, et son chemin, par exemple
      `./programmes/MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py` relevé le
      19-09-2026. Quand rien ne correspond : DEUX valeurs vides.
      [rend: 2]
    ⑥ TRAITEMENT — ① parcourir la racine et tous ses sous-dossiers · ② écarter du
      parcours les dossiers `archives`, `.git`, `__pycache__` et `_site_travail` ·
      ③ dans chaque dossier visité, pour chaque nom cherché, comparer aux fichiers
      présents, soit à l'identique, soit par début de nom quand le nom finit par
      une étoile · ④ au premier fichier qui correspond, l'exécuter et rendre
      l'objet obtenu avec son chemin · ⑤ si le parcours s'achève sans rien trouver,
      rendre deux valeurs vides.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les dossiers écartés le sont pour trois raisons différentes.
      `archives` porte les versions tombées : y prendre un programme ferait tourner
      une version périmée sous le nom de la version vivante, et rien ne le dirait,
      puisque le nom serait le bon. `.git` et `__pycache__` portent des copies que
      le système de versions et Python tiennent pour leur compte. `_site_travail`
      porte les pages fabriquées pour la publication.
      La recherche par début de nom existe parce que le projet horodate ses noms de
      fichier : `MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py` porte sa date dans son
      nom. Chercher le nom entier obligerait à réécrire ce programme à chaque
      nouvelle version du module cherché.
    ⑨ CE QUI CLOCHE —
      ① Elle ne cherche pas, elle EXÉCUTE. Le fichier trouvé est lancé en entier,
      et tout ce qu'il fait au moment d'être lancé se produit. Aucun des programmes
      chargés aujourd'hui n'en profite pour écrire quoi que ce soit — vérifié le
      19-09-2026 : après un passage complet, la copie du dépôt est identique à
      l'original. Mais rien dans cette fonction ne garantit cette propriété : un
      programme déposé demain dans `programmes/` sous un nom qui correspond serait
      exécuté sans que personne l'ait voulu.
      ② Elle reparcourt toute l'arborescence et réexécute le même fichier à chaque
      appel, sans rien garder du passage précédent. Mesuré le 19-09-2026 en
      marquant `MODULE_POSITIONS.py` d'une ligne d'affichage : ce fichier est
      exécuté 2 fois sur un passage `--calibrage` et 5 fois sur un passage
      `--strategie`. Rien ne garantit que les cinq exécutions portent sur le même
      fichier si l'arborescence change entre-temps.
      ③ Elle rend deux valeurs vides quand elle ne trouve rien, sans rien afficher.
      Un appelant qui oublie de vérifier ce qu'il reçoit tombe plus loin sur une
      erreur qui ne nommera pas le fichier manquant.
      ④ Le dossier `tests` n'est pas écarté du parcours, contrairement à
      `archives`. Le jour où un fichier d'épreuve y portera le nom d'un programme
      cherché, c'est lui qui pourra être pris, selon l'ordre dans lequel le système
      rend les dossiers. Le dépôt ne porte aujourd'hui qu'un seul fichier de chacun
      de ces noms — vérifié le 19-09-2026, un parcours complet du dépôt rend un
      seul `MODULE_POSITIONS.py`, un seul `JUGE_DES_STRATEGIES.py`, un seul
      `MODULE_STATISTIQUES_*` — donc le défaut ne se voit pas encore.
      ⑤ Quand plusieurs noms sont cherchés en un appel, l'ordre des noms ne décide
      pas. Le parcours des dossiers passe avant : un fichier répondant au DERNIER
      nom, trouvé dans un dossier visité tôt, est rendu avant un fichier répondant
      au PREMIER nom qui vivrait plus profond. Aucun appel d'aujourd'hui ne passe
      plus d'un nom, donc le cas ne se produit pas.
      ⑥ Le nom donné à l'objet chargé est tronqué aux dix premiers caractères du
      nom de fichier. `MODULE_POSITIONS.py` et `MODULE_POSITIONS_V2.py`
      donneraient tous deux `_m_MODULE_POS`. Cela ne change pas ce qui est rendu,
      mais une trace d'erreur ne permettrait plus de savoir lequel des deux a
      échoué.
    ⑩ EFFET — LIT l'arborescence de la racine, puis LIT ET EXÉCUTE le premier
      fichier qui correspond. N'écrit elle-même aucun fichier et ne touche pas au
      réseau, mais ce que fait le programme exécuté échappe à son contrôle.
    ⑪ TERMINAISON — Rend la main dans les deux cas, qu'elle ait trouvé ou non. Et
      un de ses appels peut ne pas revenir : l'exécution du fichier trouvé lève ce
      que ce fichier lève, et rien n'est rattrapé ici — un programme qui s'arrête
      sur une erreur au moment d'être lancé arrête aussi celui-ci.
      [sort: non]
    ⑫ DÉFINITIONS
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
      `archives` : le dossier du dépôt où sont rangées les versions tombées, sous
        un nom qui dit pourquoi elles sont tombées
    
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      le module de signal : le programme qui décide quelles valeurs acheter
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle a tourné — rapport de boucle, rapport d'audit, cockpit, historique des mesures.
"""
    for r, sd, fs in os.walk(base):
        sd[:] = [x for x in sd if x not in ("archives", ".git", "__pycache__", "_site_travail")]
        for n in noms:
            for f in fs:
                if f == n or (n.endswith("*") and f.startswith(n[:-1])):
                    sp = importlib.util.spec_from_file_location("_m_" + f[:10], os.path.join(r, f))
                    m = importlib.util.module_from_spec(sp)
                    sp.loader.exec_module(m)
                    return m, os.path.join(r, f)
    return None, None


def calibrer(stat):
    """Vérifie que le juge à huit critères reproduit un résultat connu, avant toute mesure neuve.

    ① RÔLE — Prouver que l'instrument fonctionne avant de s'en servir. Le juge à huit critères est
      appelé sur des chiffres dont on connaît d'avance le verdict, et son résultat
      est comparé à celui-là. Sans ce contrôle, un juge à huit critères modifié rendrait des scores
      plausibles et faux, et rien ne le dirait : personne ne connaît par cœur le
      bon résultat d'une stratégie qu'on n'a jamais jugée.
    ② CONTEXTE D'APPEL — `main`, une seule fois, immédiatement après le chargement
      de `MODULE_STATISTIQUES_*` et avant tout le reste. Jamais appelée ailleurs.
      Un échec arrête le programme en code 1, sans rien mesurer.
    ③ ENTRÉE — `stat` : l'objet issu de l'exécution de
      `MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py`. Un seul appelant, `main`, et
      il transmet sans le modifier ce que `_charger` lui a rendu.
    ④ CONDITIONS D'ENTRÉE — L'objet reçu doit porter la fonction
      `evaluer_strategie_8_criteres`, et celle-ci doit rendre un dictionnaire
      portant la clé `n_criteres_passes`.
    ⑤ SORTIE — UNE valeur : vrai si le juge à huit critères rend exactement le score attendu, faux
      sinon. Elle affiche en plus une ligne de constat, et deux lignes
      d'explication quand elle rend faux.
      [rend: 1]
    ⑥ TRAITEMENT — ① appeler le juge à huit critères sur une copie des chiffres témoins ·
      ② relever le nombre de critères qu'il annonce passés · ③ le comparer au
      nombre attendu · ④ afficher les deux nombres et le verdict · ⑤ afficher, en
      cas d'écart, que rien ne sera mesuré · ⑥ rendre le verdict.
    ⑦ UNITÉ — Un NOMBRE DE CRITÈRES PASSÉS, entre 0 et 8.
    ⑧ POURQUOI — Les chiffres témoins et le score attendu sont ceux de la stratégie
      C5-EI au 26-04-2026, relevés dans un mémo daté du 27-04-2026 08h05 :
      p-value 0,007, Deflated Sharpe 1,03, probabilité de sur-apprentissage 30 %,
      chute maximale 4,6 %, 119 jours sous l'eau, Kelly fractionnel 0,093,
      stabilité vraie, toutes les fenêtres positives, frais 0,005. Le mémo annonce
      7 sur 8. Mesuré le 19-09-2026, le juge à huit critères rend bien 7 sur 8 : l'affichage porte
      « CALIBRAGE — C5-EI au 26-04-2026 : obtenu 7/8 · attendu 7/8  OK ».
      Le juge à huit critères reçoit une COPIE des chiffres témoins et non les chiffres eux-mêmes,
      pour qu'une modification faite à l'intérieur du juge à huit critères ne se retrouve pas dans
      le témoin au calibrage suivant. Un témoin que l'instrument peut modifier
      cesse d'être un témoin.
      Et l'échec arrête tout au lieu d'avertir : un instrument non calibré produit
      des chiffres sans valeur, et un chiffre sans valeur qui s'affiche à côté de
      chiffres justes ne se distingue plus.
    ⑨ CE QUI CLOCHE —
      ① Elle n'éprouve que le juge à huit critères, pas ce que ce programme ajoute. Les chiffres
      témoins sont écrits en dur : ils ne passent ni par le juge des stratégies, ni par le calcul
      des mesures, ni par la lecture du taux de frais. Tout ce fichier peut donc
      être faux sans que ce calibrage rougisse — c'est arrivé le 13-09-2026, et
      c'est la raison d'être du second calibrage, celui du branchement.
      ② Le témoin est le résultat d'une grille et d'une seule. Le score attendu,
      7 sur 8, vaut pour la grille GRILLE-26-04 relevée au REGISTRE le 19-09-2026.
      Une modification légitime d'un seuil de cette grille ferait échouer le
      calibrage sans que rien ne soit cassé, et le message affiché dirait alors
      « Le juge à huit critères ne reproduit plus le résultat connu », ce qui désignerait le juge à huit critères
      plutôt que le seuil qui vient de changer.
      ③ Le nombre attendu et les neuf chiffres témoins sont écrits dans le code,
      alors que leur source est un mémo daté cité en commentaire. Rien ne relie les
      deux : si le mémo est corrigé, rien ne signalera que le témoin du code ne lui
      correspond plus.
      ④ Si le juge à huit critères change le nom de la clé qu'il rend, le nombre relevé est vide,
      la comparaison échoue et le message affiché est « obtenu None/8 ». Le lecteur
      lit alors un échec de calibrage là où il y a un désaccord de nom entre deux
      programmes.
    ⑩ EFFET — N'écrit aucun fichier, ne touche pas au réseau. AFFICHE une ligne en
      cas de succès, trois en cas d'échec. Elle appelle le juge à huit critères, qui ne modifie
      rien non plus.
    ⑪ TERMINAISON — Rend toujours la main, avec vrai ou faux. Et un de ses appels
      peut ne pas revenir : le juge à huit critères lève si une des valeurs qu'il compare à un
      seuil est vide — mesuré le 19-09-2026 sur des mesures comportant des valeurs
      vides, « TypeError: '>=' not supported between instances of 'NoneType' and
      'float' ». Les chiffres témoins étant tous renseignés, le cas ne se produit
      pas ici.
      [sort: non]
    ⑫ DÉFINITIONS
      le juge à huit critères : `evaluer_strategie_8_criteres`, la fonction de
        `MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py` qui compare neuf mesures à
        leurs seuils et rend un score sur huit
      la grille : la liste des huit critères et de leurs seuils ; celle qui tourne s'appelle GRILLE-26-04 et vit dans `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740 de ce fichier
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
      un témoin : un jeu de chiffres dont on connaît d'avance le résultat, employé
        pour prouver qu'un instrument fonctionne avant de s'en servir
    
      la raison : le texte court qui dit pourquoi une lecture a échoué, retenu sous le nom `motif`
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
      le témoin : le fichier temoins/TEMOIN_cours_reels.csv, copie figée de vraies séances, sur laquelle les épreuves tournent toujours à l'identique.
      une stratégie : une règle qui dit QUOI acheter, avec son objectif de gain, sa perte acceptée et son horizon
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    r = stat.evaluer_strategie_8_criteres(dict(TEMOIN))
    n = r.get("n_criteres_passes")
    ok = (n == TEMOIN_ATTENDU)
    print(f"  CALIBRAGE — C5-EI au 26-04-2026 : obtenu {n}/8 · attendu {TEMOIN_ATTENDU}/8"
          f"  {'OK' if ok else '*** ECHEC ***'}")
    if not ok:
        print("     Le juge à huit critères ne reproduit plus le résultat connu. RIEN N'EST MESURÉ :")
        print("     un instrument non calibré produit des chiffres sans valeur.")
    return ok


def calibrer_le_pont(stat, base):
    """Vérifie sur des opérations fabriquées que le branchement rend ce qu'il doit.

    ① RÔLE — Éprouver la seule chose que ce programme ajoute : le passage des
      opérations rendues par le juge des stratégies aux calculs du module de statistiques. Soixante
      opérations sont fabriquées dont on connaît le résultat exact, on demande les
      mesures, et on vérifie six attentes. Chacune de ces six attentes vise une
      faute réellement commise le 13-09-2026, et non un défaut imaginé.
    ② CONTEXTE D'APPEL — `main`, une seule fois, juste après le calibrage du juge à huit critères
      et avant le contrôle des seuils. Jamais appelée ailleurs. Un échec arrête le
      programme en code 1, sans rien mesurer.
    ③ ENTRÉE — `stat` : l'objet issu de l'exécution de
      `MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py`. `base` : la racine à parcourir
      pour y trouver `MODULE_POSITIONS.py` et son taux de frais. Un seul appelant,
      `main`, qui transmet les deux sans les modifier.
    ④ CONDITIONS D'ENTRÉE — L'objet reçu doit porter les fonctions de calcul
      appelées par le branchement. La racine doit porter `MODULE_POSITIONS.py` avec
      son taux de frais, faute de quoi la lecture de ce taux lève.
    ⑤ SORTIE — UNE valeur : vrai si les six attentes sont tenues, faux sinon. Elle
      affiche en plus une ligne portant les cinq mesures obtenues en cas de succès,
      ou la liste des attentes déçues en cas d'échec.
      [rend: 1]
    ⑥ TRAITEMENT — ① fabriquer 60 opérations, dont 36 gagnantes à +4 000 € et 24
      perdantes à −2 500 €, soit un taux de réussite de 60 % exactement ·
      ② fabriquer une fiche de stratégie portant un objectif de +4 %, une perte
      acceptée de 2,5 % et un horizon de 20 séances · ③ demander les mesures, en
      passant le taux de frais lu chez son propriétaire · ④ s'arrêter si aucune
      mesure n'est rendue · ⑤ vérifier que le taux de réussite vaut exactement 60 ·
      ⑥ vérifier que la p-value est renseignée et inférieure à 0,5 · ⑦ vérifier que
      la chute maximale, la durée sous l'eau et le Kelly fractionnel sont
      renseignés · ⑧ vérifier que le taux de frais rendu est bien celui qui a été
      lu · ⑨ afficher le résultat et rendre le verdict.
    ⑦ UNITÉ — Les gains fabriqués sont des EUROS : +4 000 € et −2 500 €. Le taux de
      réussite attendu est un POURCENT, 60,0. L'objectif et la perte acceptée sont
      écrits en POURCENTS dans la fiche, et convertis en fractions par le
      branchement. Le taux de frais est une FRACTION, 0,0015 relevé le 19-09-2026.
      Les opérations se comptent en NOMBRE D'OPÉRATIONS, fixé à 60.
    ⑧ POURQUOI — Le premier calibrage écrit pour ce programme n'appelait le juge à huit critères que
      sur des chiffres écrits en dur : il éprouvait le juge à huit critères, et pas une seule ligne
      de ce que ce fichier ajoute. Le 13-09-2026, le relecteur a remis trois fautes
      du soir sur une copie jetable ; le calibrage est resté vert, le programme a
      rendu une p-value de 1,0 sur 103 opérations à 63 % de réussite, et il est
      sorti en code 0. Une épreuve qui reste verte quand on retire ce qu'elle teste
      n'est pas une preuve.
      Chaque attente vise donc une faute précise, et se trompe bruyamment si cette
      faute revient. Une p-value de 1,0 est la signature exacte d'un taux de
      réussite passé en pourcent là où une fraction est attendue. Une mesure vide
      est la signature exacte d'un nom de clé deviné au lieu d'être relevé. Un taux
      de frais différent de celui du fichier des positions est la signature exacte
      d'un nombre recopié à la main.
      Les 60 opérations sont fabriquées et non tirées du dépôt parce qu'il faut
      connaître le résultat à l'avance : 36 gagnantes sur 60 font 60,0 % et rien
      d'autre, et toute valeur différente dénonce le branchement plutôt que les
      données.
    ⑨ CE QUI CLOCHE —
      ① Le taux de frais est relu deux fois, par deux parcours complets de
      l'arborescence : une fois pour le passer aux mesures, une fois pour comparer
      ce qui est rendu. Mesuré le 19-09-2026 en marquant `MODULE_POSITIONS.py`, ce
      fichier est exécuté 2 fois sur un passage `--calibrage`. La comparaison ne
      prouve donc pas que le branchement a transmis le taux reçu : elle prouve
      seulement que deux lectures successives du même fichier donnent la même
      valeur.
      ② L'attente sur la p-value est très large. Elle exige seulement une valeur
      inférieure à 0,5, alors que la valeur réellement obtenue est 0,1213, mesurée
      le 19-09-2026. La faute visée donnait 1,0 ; n'importe quelle valeur entre
      0,1213 et 0,4999 passerait sans que rien ne soit dit, y compris une valeur
      fausse.
      ③ La fiche fabriquée porte un horizon de 20 séances qui n'est jamais lu. Le
      calcul des mesures ne consulte que l'objectif de gain et la perte acceptée :
      mesuré le 19-09-2026, le mot horizon n'apparaît dans ce fichier qu'à cette
      seule ligne. L'horizon n'est donc éprouvé nulle part ici.
      ④ Les 60 opérations portent toutes la même valeur, écrite `X`, et des dates
      réparties sur neuf mois d'une seule année. Un défaut qui n'apparaîtrait
      qu'avec plusieurs valeurs, ou sur deux années, ne serait pas vu.
      ⑤ Quatre des neuf mesures ne sont éprouvées par aucune attente : la
      probabilité de sur-apprentissage, la stabilité, le Deflated Sharpe et le
      walk-forward. Elles valent toutes vide, et ce vide est justement ce que le
      programme annonce ne pas savoir produire ; mais rien ici ne vérifie qu'elles
      sont présentes, et l'absence d'une clé se lit autrement qu'un vide.
      ⑥ Le compte des gagnantes tient à un calcul sur le rang de l'opération :
      trois sur cinq sont gagnantes. Le jour où le nombre d'opérations fabriquées
      changerait, le taux ne serait plus 60 % et l'attente échouerait sans qu'aucun
      défaut n'existe.
    ⑩ EFFET — N'écrit aucun fichier, ne touche pas au réseau. LIT l'arborescence de
      la racine deux fois et EXÉCUTE `MODULE_POSITIONS.py` deux fois, pour y lire
      le taux de frais. AFFICHE une ligne en cas de succès, une par attente déçue
      plus deux lignes de conclusion en cas d'échec.
    ⑪ TERMINAISON — Rend la main avec vrai ou faux dans le cas normal. Et un de ses
      appels peut ne pas revenir : la lecture du taux de frais lève une erreur non
      rattrapée quand `MODULE_POSITIONS.py` ou son taux sont introuvables, et cette
      erreur arrête alors le programme avec une trace Python.
      [sort: non]
    ⑫ DÉFINITIONS
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
      le pont : le branchement entre le juge des stratégies et le juge à huit critères, qui est tout ce que ce programme ajoute
      une opération : un achat simulé suivi de sa revente, avec son gain net en
        euros ; aucun ordre réel n'est jamais passé
      une fiche : la ligne qui décrit une stratégie dans le registre des stratégies, `donnees/cac40_strategies.csv` — son identifiant, ses réglages et ce qu'elle déclare.
      la p-value : la probabilité qu'un taux de réussite au moins aussi bon soit
        obtenu par le seul hasard ; plus elle est petite, moins le hasard explique
        le résultat
      le Kelly fractionnel : la part du capital qu'il serait raisonnable d'engager
        sur une opération, compte tenu du taux de réussite et des gains et pertes
        attendus
      le relecteur : celui qui relit le travail de l autre, ici Cowork
    
      l'horizon : le nombre de séances pendant lesquelles une position est tenue si ni l'objectif de gain ni la perte acceptée ne sont atteints
      l'objectif de gain : le pourcentage de hausse à partir duquel la position se referme sur un gain
      la durée sous l'eau : le nombre de jours pendant lesquels le cumul des gains reste sous son plus haut précédent
      la fiche : la ligne d'une stratégie au registre des stratégies `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte acceptée, son horizon et son univers
      la perte acceptée : le pourcentage de baisse à partir duquel la position se referme sur une perte
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
      le taux de réussite : la part des opérations qui se sont refermées sur un gain, écrite en pourcent
      une clé : le texte obtenu après rapprochement, qui sert à comparer deux noms et n'est jamais affiché à un lecteur
      une fraction : la façon d'écrire un pourcentage entre 0 et 1 — 0,040 pour +4 % — par opposition au pourcent, qui écrirait 4.0
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle a tourné — rapport de boucle, rapport d'audit, cockpit, historique des mesures.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    # 60 operations : 36 gagnantes, 24 perdantes -> 60 % exactement
    ops = []
    for k in range(60):
        ops.append({"valeur": "X", "date_signal": f"2026-{1+k%9:02d}-{1+k%27:02d}",
                    "pe": 100.0, "px": 104.0 if k % 5 < 3 else 97.5,
                    "net": 4000.0 if k % 5 < 3 else -2500.0})
    fiche = {"tp": "+4.0%", "sl": "-2.5%", "horizon": "20j"}
    m, motif = mesures_disponibles(fiche, ops, stat, None, _frais_taux(base))
    if m is None:
        print(f"  CALIBRAGE DU PONT — ECHEC : {motif}"); return False
    echecs = []
    # ① le taux : 36 gagnantes sur 60 = 60,0 % exactement
    if m.get("wr_pct") != 60.0:
        echecs.append(f"wr_pct = {m.get('wr_pct')} au lieu de 60.0")
    # ② la p-value : 60 % sur 60 tirages bat le hasard. Une p-value de 1.0 est
    #    la signature EXACTE de `p_null` passe en pourcentage — ma faute du soir.
    p = m.get("p_value")
    if p is None or p >= 0.5:
        echecs.append(f"p_value = {p} — un 1.0 signe p_null passé en pourcentage")
    # ③④⑤ les trois cles devinees : chacune rendait None, ce qui se lit
    #    « critere non passe » et ne se voit pas.
    for cle in ("dd_pct", "underwater_jours", "kelly_frac"):
        if m.get(cle) is None:
            echecs.append(f"{cle} = None — clé de retour devinée au lieu d être relevée")
    # ⑥ les frais : lus chez leur proprietaire, jamais ecrits ici
    if m.get("frais_pct") != _frais_taux(base):
        echecs.append(f"frais_pct = {m.get('frais_pct')} au lieu de MODULE_POSITIONS.FRAIS_TAUX")
    if echecs:
        print("  CALIBRAGE DU PONT — *** ECHEC ***")
        for e in echecs:
            print(f"     · {e}")
        print("     RIEN N EST MESURÉ : le branchement ne rend pas ce qu il doit.")
        return False
    print(f"  CALIBRAGE DU PONT — 60 opérations fabriquées : wr={m['wr_pct']} · "
          f"p={m['p_value']} · dd={m['dd_pct']} · kelly={m['kelly_frac']} · "
          f"frais={m['frais_pct']}  OK")
    return True


def _frais_taux(base):
    """Rend le taux de frais lu chez son propriétaire, jamais écrit ici.

    ① RÔLE — Aller chercher le taux de frais là où il est défini, une fois pour
      toutes, au lieu de le recopier. Ce taux entre dans le calcul du Kelly
      fractionnel : une valeur approchée y produit un résultat approché que rien ne
      distingue d'un résultat juste.
    ② CONTEXTE D'APPEL — Deux appelants, tous deux dans ce fichier :
      `calibrer_le_pont`, deux fois, pour passer le taux aux mesures puis pour
      vérifier qu'il est bien ressorti ; et `_juger_une`, une fois, avant de
      demander les mesures d'une vraie stratégie. Jamais appelée ailleurs.
    ③ ENTRÉE — `base` : la racine à parcourir pour y trouver `MODULE_POSITIONS.py`.
      Les deux appelants transmettent sans la modifier la racine reçue sur la ligne
      de commande.
    ④ CONDITIONS D'ENTRÉE — La racine doit porter, à n'importe quelle profondeur, un
      fichier nommé exactement `MODULE_POSITIONS.py`, et ce fichier doit porter un
      taux de frais nommé `FRAIS_TAUX`.
    ⑤ SORTIE — UNE valeur : le taux de frais, en fraction. Mesuré le 19-09-2026 :
      0,0015. Il n'y a pas de seconde forme : ou bien la valeur est rendue, ou bien
      la fonction lève.
      [rend: 1]
    ⑥ TRAITEMENT — ① chercher `MODULE_POSITIONS.py` sous la racine et l'exécuter ·
      ② lever si le fichier est introuvable ou s'il ne porte pas de taux de frais ·
      ③ rendre le taux, converti en nombre à virgule.
    ⑦ UNITÉ — Une FRACTION du montant de l'ordre, jamais un pourcent : 0,0015 vaut
      15 points de base, soit 0,15 % par ordre. C'est le tarif Fortuneo PROGRESS,
      décidé pour ce projet.
    ⑧ POURQUOI — Un chiffre qui existe ailleurs ne se recopie pas (R-708), et ce
      taux-ci a déjà été recopié faux. Le 13-09-2026, la valeur 0,005 était écrite à
      la main dans ce fichier, là où `MODULE_POSITIONS.py` pose 0,0015 : plus de
      trois fois le taux réel. Mesure faite le même jour, le Kelly fractionnel
      passait de 0,1574 à 0,1885, soit 19,8 % d'écart, dans un programme qui ne
      lisait jamais la source. La confusion a une cause nommable : 0,005 est bien un
      nombre du projet, mais c'est le SEUIL du huitième critère — l'exigence que le
      backtest ait supposé au moins 50 points de base de frais — et non le tarif du
      courtier. Les deux se ressemblent et ne veulent pas dire la même chose.
      Et la fonction lève au lieu de poser une valeur de repli. Un taux de repli
      serait indiscernable du vrai : il ne ferait échouer aucun contrôle, il
      fausserait le Kelly fractionnel, et le chiffre faux s'afficherait à côté des
      chiffres justes sans rien qui le distingue.
    ⑨ CE QUI CLOCHE —
      ① Elle reparcourt l'arborescence et réexécute `MODULE_POSITIONS.py` à chaque
      appel, sans rien garder. Mesuré le 19-09-2026 en marquant ce fichier d'une
      ligne d'affichage : 2 exécutions sur un passage `--calibrage`, 5 sur un
      passage `--strategie`. Rien ne garantit que les exécutions successives portent
      sur le même fichier ni rendent la même valeur.
      ② Elle cherche le fichier par son NOM. Le critère qui tranche tient en une
      question : si je renomme un fichier, mon contrôle change-t-il d'avis ? Ici
      oui, donc il épelle. Le jour où le taux de frais déménagerait dans un fichier
      d'un autre nom, cette fonction lèverait « introuvable » alors que le taux
      existe.
      ③ Le message d'erreur cite la règle qui interdit de recopier un chiffre
      existant (R-708), mais ne dit pas au lecteur quelle valeur est attendue ni où
      la retrouver : il nomme le fichier manquant sans dire ce qu'il faut y écrire.
    ⑩ EFFET — LIT l'arborescence de la racine, puis LIT ET EXÉCUTE
      `MODULE_POSITIONS.py`. N'écrit rien, n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main avec le taux quand le fichier et son taux existent.
      LÈVE autrement une erreur non rattrapée ici, qui arrête le programme avec une
      trace Python et un code de sortie 1. Et un de ses appels peut ne pas revenir :
      l'exécution de `MODULE_POSITIONS.py` lève ce que ce fichier lève.
      [sort: non]
    ⑫ DÉFINITIONS
      le Kelly fractionnel : la part du capital qu'il serait raisonnable d'engager
        sur une opération, compte tenu du taux de réussite et des gains et pertes
        attendus
      un point de base : un centième de pourcent ; 15 points de base valent 0,15 %
      le backtest : le rejeu d'une stratégie sur des cours passés, pour estimer ce
        qu'elle aurait donné
    
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      une fraction : la façon d'écrire un pourcentage entre 0 et 1 — 0,040 pour +4 % — par opposition au pourcent, qui écrirait 4.0
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    mp, _ch = _charger(base, "MODULE_POSITIONS.py")
    if mp is None or not hasattr(mp, "FRAIS_TAUX"):
        raise RuntimeError("MODULE_POSITIONS.FRAIS_TAUX introuvable — "
                           "on ne pose PAS de taux de repli (R-708)")
    return float(mp.FRAIS_TAUX)


# LE NOM DE LA GRILLE QUE CE PROGRAMME APPLIQUE — R-743, 13-09-2026.
# « 7/8 » ne veut rien dire ; « 7/8 selon GRILLE-26-04 » le dit.
# Il existe une SECONDE grille, GRILLE-A210, commencée le 14-08 et INACHEVÉE :
# sept de ses huit critères diffèrent de celle-ci, et aucun programme ne
# l applique. **Ce ne sont pas deux versions d une grille, ce sont deux grilles.**
GRILLE = "GRILLE-26-04"


def seuils_du_registre(base):
    """Vérifie que les seuils de la grille s'écrivent bien au REGISTRE.

    ① RÔLE — Refuser que les seuils du code et ceux du REGISTRE divergent en
      silence. Les huit critères et leurs seuils vivent aujourd'hui dans le code,
      à l'intérieur de `MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py`, et sont
      recopiés au REGISTRE dans un tableau. Cette fonction ne déplace pas les
      seuils : elle cherche, dans le bloc du REGISTRE qui porte le nom de la
      grille, les nombres que le code applique, et rend la liste de ceux qu'elle
      n'y trouve pas.
    ② CONTEXTE D'APPEL — `main`, une seule fois, après les deux calibrages et avant
      le chargement du juge des stratégies. Jamais appelée ailleurs. Une liste non vide arrête le
      programme en code 1, sans rien mesurer.
    ③ ENTRÉE — `base` : la racine à parcourir pour y trouver `REGISTRE_REGLES.md`.
      Un seul appelant, `main`, qui transmet sans la modifier la racine reçue sur
      la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — Aucune. Une racine sans REGISTRE ne la fait pas lever :
      elle rend un écart qui le dit.
    ⑤ SORTIE — UNE valeur : la liste des écarts constatés, vide quand tout
      concorde. Trois formes différentes selon la branche. Une seule ligne disant
      que le REGISTRE est introuvable. Une seule ligne disant que le nom de la
      grille n'y figure pas. Ou bien une ligne par seuil non retrouvé, de la forme
      « C5 (seuil 0,05) absent du bloc GRILLE-26-04 ».
      [rend: 1]
    ⑥ TRAITEMENT — ① parcourir la racine en écartant `archives`, `.git` et
      `__pycache__`, et s'arrêter au premier dossier portant `REGISTRE_REGLES.md` ·
      ② rendre un écart si aucun n'est trouvé · ③ lire le fichier en entier ·
      ④ rendre un écart si le nom de la grille n'y figure pas · ⑤ découper les
      2 200 caractères qui suivent la première apparition de ce nom · ⑥ chercher
      dans ce morceau chacun des seuils attendus, écrits comme des textes ·
      ⑦ rendre la liste de ceux qui manquent.
    ⑦ UNITÉ — Les seuils sont cherchés comme des TEXTES, pas comme des nombres :
      « 0,05 » avec une virgule, comme le REGISTRE l'écrit, et non 0.05 avec un
      point comme le code le pose. La fenêtre de lecture est un NOMBRE DE
      CARACTÈRES, fixé à 2 200.
    ⑧ POURQUOI — La loi du projet est claire et n'est PAS respectée aujourd'hui :
      les seuils vivent au REGISTRE, jamais dans le code (R-743, deuxième geste),
      et il est déjà demandé que le moteur LISE ses seuils au REGISTRE au lieu de
      les contenir — « la brique D devra LIRE ses seuils dans le REGISTRE, jamais
      les contenir » (A-210). Neuf seuils écrits en dur dans
      `MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py` enfreignent cette consigne :
      relevés le 19-09-2026, ils sont rassemblés sous le nom
      `CRITERES_VALIDATION_EXPERTS`, et c'est là que le juge à huit critères va les chercher, pas
      au REGISTRE. Cette fonction ne corrige pas cela — elle n'est qu'un détecteur
      de divergence, ce qui est la seule chose qui coûte cher tant que le
      déplacement n'est pas fait.
      La grille est nommée dans le verdict parce que « 7 sur 8 » ne veut rien dire
      sans elle (R-743, premier geste). Il existe une seconde grille commencée le
      14-08-2026 et inachevée, dont sept critères sur huit diffèrent de celle-ci :
      ce ne sont pas deux versions d'une grille, ce sont deux grilles, et aucun
      programme n'applique la seconde.
      L'arrêt sur divergence, plutôt qu'un avertissement, tient à ce qu'un seuil
      qui diverge ne se voit nulle part ailleurs : il ne fait rien échouer, il
      déplace seulement la frontière entre une stratégie validée et une stratégie
      archivée.
    ⑨ CE QUI CLOCHE —
      ① Un des sept seuils attendus est perdu avant même d'être cherché. La table
      des attendus range les seuils par leur écriture, et « 0,05 » y est écrit deux
      fois, pour le premier critère puis pour le cinquième : la seconde écriture
      efface la première. Mesuré le 19-09-2026 en rejouant cette table seule : elle
      compte 6 entrées et non 7, et l'entrée rescapée porte le nom du cinquième
      critère. Le premier critère n'est donc jamais contrôlé. La conséquence est
      limitée aujourd'hui parce que les deux critères partagent la même valeur,
      mais le jour où l'un des deux seuils changera, l'autre couvrira son absence.
      ② Le message de succès annonce neuf seuils alors que six textes ont été
      cherchés. Mesuré le 19-09-2026 sur le dépôt, l'affichage porte
      « SEUILS — GRILLE-26-04 au REGISTRE porte les neuf seuils du code ». Deux des
      huit critères — la stabilité et le walk-forward — n'ont pas de seuil
      chiffré : leur exigence est « vraie », et rien ici ne la cherche. Le lecteur
      croit donc que neuf valeurs ont concordé, alors que six textes ont été
      trouvés.
      ③ Le contrôle porte sur la PRÉSENCE d'un texte, jamais sur l'égalité de deux
      valeurs. Il vérifie que la suite de caractères « 0,30 » figure quelque part
      dans le morceau lu ; il ne compare rien à ce que le code applique. Un
      REGISTRE qui écrirait « 0,30 » dans une phrase sans rapport passerait le
      contrôle, et un code dont le seuil passerait à 0,10 le passerait aussi, tant
      que le REGISTRE garderait l'ancien nombre écrit quelque part dans la fenêtre.
      ④ Le seuil « 365 » est un nombre de trois chiffres qui peut figurer n'importe
      où : dans une date, dans un autre nombre, dans un identifiant. Il se
      retrouverait sans que le seuil existe.
      ⑤ La fenêtre de 2 200 caractères est un nombre écrit dans le code sans
      justification, et sa marge est mesurable. Mesuré le 19-09-2026 sur le
      REGISTRE du dépôt : le nom de la grille apparaît une première fois au
      caractère 137 495, et le dernier seuil cherché se trouve au caractère 1 238
      de la fenêtre — il reste 962 caractères de marge. Ajouter au REGISTRE une
      explication d'un millier de caractères entre la première mention de la grille
      et la ligne du dernier seuil ferait échouer le contrôle et arrêterait le
      programme en code 1, sans qu'aucun seuil ait changé.
      ⑥ La fenêtre part de la PREMIÈRE apparition du nom de la grille, qui n'est pas
      le tableau. Relevé le 19-09-2026, cette première apparition est dans une
      phrase d'explication située cinq lignes avant le titre du tableau. Le tableau
      est atteint par chance, parce qu'il suit de près.
      ⑦ Le module de recherche de texte est importé au début de la fonction sous le
      nom `_re`, et n'est employé nulle part : vérifié le 19-09-2026, ce nom
      n'apparaît qu'une fois dans tout le fichier, à sa propre importation.
      ⑧ Le parcours s'arrête au PREMIER `REGISTRE_REGLES.md` rencontré, sans
      signaler qu'il pourrait y en avoir un second. Le dépôt n'en porte qu'un —
      vérifié le 19-09-2026, un parcours complet n'en rend qu'un seul, dans
      `gouvernance/` — mais deux fichiers de même nom à deux endroits sont un
      défaut, jamais une intention : l'un serait lu, l'autre écrit, et rien ne le
      dirait.
    ⑩ EFFET — LIT l'arborescence de la racine, puis LIT EN ENTIER le premier
      `REGISTRE_REGLES.md` trouvé. N'écrit aucun fichier, n'affiche rien elle-même,
      ne touche pas au réseau : elle rend une liste que son appelant affiche.
    ⑪ TERMINAISON — Rend toujours la main, avec une liste vide ou non. Elle ne lève
      pas : le REGISTRE introuvable est rendu comme un écart, et les octets que la
      lecture ne sait pas interpréter sont remplacés au lieu de la faire tomber.
      Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      la grille : la liste des huit critères et de leurs seuils ; celle qui tourne s'appelle GRILLE-26-04 et vit dans `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740 de ce fichier
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
      le juge à huit critères : `evaluer_strategie_8_criteres`, la fonction de
        `MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py` qui compare neuf mesures à
        leurs seuils et rend un score sur huit
      le walk-forward : le rejeu d'une stratégie sur des tranches de temps
        successives, pour voir si elle tient hors de la période qui a servi à la
        régler
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
    
      `archives` : le dossier du dépôt où sont rangées les versions tombées, sous un nom qui dit pourquoi elles sont tombées
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      la table : `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740, qui porte les neuf seuils et le sens de comparaison de chacun
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    import re as _re
    ch = None
    for r, sd, fs in os.walk(base):
        sd[:] = [x for x in sd if x not in ("archives", ".git", "__pycache__")]
        if "REGISTRE_REGLES.md" in fs:
            ch = os.path.join(r, "REGISTRE_REGLES.md"); break
    if not ch:
        return ["REGISTRE_REGLES.md introuvable"]
    t = open(ch, encoding="utf-8", errors="replace").read()
    if GRILLE not in t:
        return [f"{GRILLE} absente du REGISTRE — le verdict ne peut pas nommer sa grille"]
    bloc = t[t.find(GRILLE):t.find(GRILLE) + 2200]
    attendus = {"0,05": "C1", "0,95": "C2", "0,30": "C3", "25 %": "C4a",
                "365": "C4b", "0,05": "C5", "0,005": "C8"}
    manquants = [f"{v} (seuil {k}) absent du bloc {GRILLE}"
                 for k, v in attendus.items() if k not in bloc]
    return manquants


def _pct(v):
    """Convertit un pourcent écrit dans une fiche en fraction, sans son signe.

    ① RÔLE — Traduire ce qu'un humain a écrit dans le registre des stratégies en ce
      que les calculs attendent. La fiche porte `+4.0%` et `-2.5%` ; les calculs
      veulent 0,04 et 0,025. Sans cette traduction, un objectif de 4 % serait pris
      pour 4, soit 400 %.
    ② CONTEXTE D'APPEL — Le calcul des mesures, deux fois de suite sur la même
      ligne, sur l'objectif de gain puis sur la perte acceptée de la fiche en
      cours. Jamais appelée ailleurs : une recherche de `_pct(` dans ce fichier, le
      19-09-2026, ne rend que sa définition et cette seule ligne d'appel.
    ③ ENTRÉE — `v` : la valeur écrite dans la fiche. Son unique appelant y passe
      l'objectif de gain puis la perte acceptée, lus dans le registre des
      stratégies, par exemple `+4.0%` et `-2.5%` pour la stratégie C5E10-OBS-V1
      relevés le 19-09-2026.
    ④ CONDITIONS D'ENTRÉE — La valeur doit porter un nombre, avec ou sans signe,
      avec un point ou une virgule, suivi ou non d'un signe pourcent. Une case vide
      ou du texte la font lever.
    ⑤ SORTIE — UNE valeur : une fraction, toujours positive. Mesuré le 19-09-2026 :
      `-2.5%` rend 0,025 et `+4.0%` rend 0,04. Rien ne la borne à 1 : une fiche
      portant `+150%` rendrait 1,5.
      [rend: 1]
    ⑥ TRAITEMENT — ① écarter le signe pourcent · ② remplacer une virgule décimale
      par un point · ③ écarter un signe plus · ④ nettoyer les espaces de bord ·
      ⑤ convertir en nombre à virgule · ⑥ en prendre la valeur absolue · ⑦ diviser
      par 100.
    ⑦ UNITÉ — Elle change d'unité : elle reçoit un POURCENT et rend une FRACTION.
      4 % entre, 0,04 sort.
    ⑧ POURQUOI — Le signe est écarté parce qu'il ne porte aucune information ici :
      la perte acceptée est toujours une perte, l'objectif toujours un gain. Les
      deux nombres sont ensuite employés comme des distances à un prix d'entrée, et
      le calcul qui les reçoit sait déjà lequel est en haut et lequel est en bas.
      Garder le signe obligerait chaque appelant à savoir quoi en faire, et un
      appelant qui se tromperait produirait un Kelly fractionnel négatif sans que
      rien ne le signale.
      Les deux écritures du séparateur décimal sont acceptées parce que le registre
      des stratégies est tenu à la main, et qu'une virgule y est aussi naturelle
      qu'un point pour qui écrit en français.
    ⑨ CE QUI CLOCHE —
      ① Elle lève sur une case vide et sur du texte. Mesuré le 19-09-2026 : une
      case vide donne « ValueError: could not convert string to float: '' », et la
      valeur `Intraday` donne la même erreur sur ce mot. Le registre des stratégies
      porte aujourd'hui 68 lignes dont aucune n'a d'objectif ni de perte vide —
      vérifié le même jour — mais une case d'horizon y porte bien le mot
      `Intraday`, ce qui montre que du texte se trouve dans ces colonnes.
      ② Écarter le signe fait accepter une fiche mal écrite sans rien dire. Un
      objectif de gain écrit `-4.0%` par erreur serait lu comme un gain de 4 %. La
      faute de saisie disparaît au lieu d'être signalée.
      ③ Elle accepte un nombre sans signe pourcent et le traite comme un pourcent.
      La valeur `0.04`, qui est déjà une fraction, serait rendue à 0,0004 : cent
      fois trop petite, et sans aucune alerte.
      ④ Le nom de la fonction ne dit pas dans quel sens elle convertit. Un lecteur
      qui voit `_pct` peut comprendre aussi bien « donne-moi un pourcent » que
      « prends un pourcent ». C'est le second.
    ⑩ EFFET — Ne lit ni n'écrit aucun fichier, n'affiche rien, ne touche pas au
      réseau. Elle ne modifie pas la valeur reçue.
    ⑪ TERMINAISON — Rend la main quand la valeur porte un nombre. LÈVE autrement une
      erreur non rattrapée ici, qui remonte jusqu'au lancement et arrête le
      programme avec une trace Python. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      une fiche : la ligne qui décrit une stratégie dans le registre des stratégies, `donnees/cac40_strategies.csv` — son identifiant, ses réglages et ce qu'elle déclare.
      le registre des stratégies : le fichier `cac40_strategies.csv`, une ligne par stratégie, qui porte leur état civil — identifiant, réglages, résultats connus
      le Kelly fractionnel : la part du capital qu'il serait raisonnable d'engager
        sur une opération, compte tenu du taux de réussite et des gains et pertes
        attendus
    
      l'objectif de gain : le pourcentage de hausse à partir duquel la position se referme sur un gain
      la fiche : la ligne d'une stratégie au registre des stratégies `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte acceptée, son horizon et son univers
      la perte acceptée : le pourcentage de baisse à partir duquel la position se referme sur une perte
      une fraction : la façon d'écrire un pourcentage entre 0 et 1 — 0,040 pour +4 % — par opposition au pourcent, qui écrirait 4.0
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle a tourné — rapport de boucle, rapport d'audit, cockpit, historique des mesures.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    return abs(float(str(v).replace("%", "").replace(",", ".").replace("+", "").strip())) / 100.0


def mesures_disponibles(fiche, ops, stat, rejouer, frais, capital=100_000.0):
    """Produit les neuf mesures que le juge à huit critères attend, à partir des opérations jouées.

    ① RÔLE — Traduire une liste d'opérations en les neuf chiffres que le juge à huit critères
      compare à ses seuils. C'est le cœur du branchement, et il n'écrit AUCUN
      CALCUL : chaque mesure est demandée à
      `MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py`, qui les porte toutes. Ce corps
      ne fait que mettre les opérations dans la forme attendue, appeler, et relever
      les résultats sous les noms que le juge à huit critères emploie.
    ② CONTEXTE D'APPEL — Deux appelants, tous deux dans ce fichier :
      `calibrer_le_pont`, une fois, sur 60 opérations fabriquées ; et `_juger_une`,
      une fois, sur les opérations d'une vraie stratégie rendues par le juge des stratégies.
      Jamais appelée ailleurs.
    ③ ENTRÉE — `fiche` : la ligne de la stratégie, dont seuls l'objectif de gain et
      la perte acceptée sont lus. `ops` : la liste des opérations, chacune portant
      sa date de signal et son gain net en euros. `stat` : l'objet issu de
      l'exécution du module de statistiques. `rejouer` : une façon de rejouer la
      stratégie avec d'autres réglages — les DEUX appelants d'aujourd'hui y passent
      une valeur vide. `frais` : le taux de frais, que les deux appelants obtiennent
      en le lisant dans `MODULE_POSITIONS.py`, soit 0,0015 relevé le 19-09-2026.
      `capital` : le capital engagé par opération, qu'aucun appelant ne remplace
      et qui vaut donc toujours sa valeur par défaut, 100 000 €.
    ④ CONDITIONS D'ENTRÉE — La liste des opérations doit en porter au moins cinq.
      La fiche doit porter un objectif de gain et une perte acceptée lisibles,
      faute de quoi leur conversion lève. L'objet de statistiques doit porter les
      cinq fonctions de calcul appelées ici.
    ⑤ SORTIE — DEUX valeurs, et sous deux formes selon la branche. Quand il y a
      assez d'opérations : le tableau des mesures, et une raison vide. Quand il y en
      a moins de cinq : une valeur vide, et la raison « moins de 5 opérations — rien
      à juger ». Le tableau porte toujours les mêmes clés, celles que le juge à huit critères
      cherche, plus le nombre d'opérations, le taux de réussite, le Sharpe et le
      compte des mesures chiffrées. Mesuré le 19-09-2026 sur la stratégie
      C5E10-OBS-V1 : 103 opérations, taux de réussite 63,1, frais 0,0015,
      p-value 0,0078, chute maximale 14,3, 85 jours sous l'eau, Kelly fractionnel
      0,1886, Sharpe 6,42, et quatre mesures vides.
      [rend: 2]
    ⑥ TRAITEMENT — ① compter les opérations et s'arrêter s'il y en a moins de cinq ·
      ② calculer le taux de réussite comme la part des opérations au gain positif ·
      ③ convertir l'objectif de gain et la perte acceptée de la fiche en fractions ·
      ④ recopier les opérations sous les deux noms que le module de statistiques
      attend, la date et le gain · ⑤ demander la significativité du taux de
      réussite contre le hasard · ⑥ demander la chute maximale et la durée sous
      l'eau, et en relever les deux valeurs voulues · ⑦ demander le Kelly
      fractionnel · ⑧ demander le Sharpe · ⑨ demander la stabilité, uniquement si
      une façon de rejouer a été fournie · ⑩ poser à vide les quatre mesures qu'on
      ne sait pas produire, pour qu'aucune clé ne manque · ⑪ compter les mesures
      réellement chiffrées sur les neuf · ⑫ rendre le tableau.
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
    ⑦ UNITÉ — Chaque mesure porte la sienne. Le taux de réussite est un POURCENT,
      arrondi au dixième. La chute maximale est un POURCENT du capital. La durée
      sous l'eau est un NOMBRE DE JOURS. Les gains sont des EUROS, sur un capital
      de 100 000 € par opération. La p-value, le Kelly fractionnel, le taux de
      frais, l'objectif de gain et la perte acceptée sont des FRACTIONS entre 0 et
      1. Le Sharpe est un rapport sans unité.
    ⑧ POURQUOI — Ce qui ne peut pas être mesuré est rendu VIDE, jamais à zéro. Un
      zéro inventé serait indiscernable d'une vraie mesure : le juge à huit critères le comparerait
      à son seuil, le trouverait insuffisant, et compterait le critère non passé
      sans que personne ne sache qu'aucun calcul n'a eu lieu. Le vide, lui, se lit
      dans l'affichage sous la forme d'un tiret.
      Et les neuf clés sont TOUJOURS posées, même vides. L'absence d'une clé est
      pire qu'un vide : le juge à huit critères ne la voit pas du tout, le lecteur ne peut pas
      savoir qu'elle manque, et le compte des mesures chiffrées serait faux. Le
      13-09-2026, deux clés — la probabilité de sur-apprentissage et la stabilité —
      n'étaient jamais produites, pas même vides ; le relecteur l'a relevé, et la
      pose systématique répond à ce défaut.
      Trois des quatre mesures manquantes exigent plus qu'une stratégie prise
      seule : le Deflated Sharpe exige le lot entier des stratégies testées et la
      variance de leurs Sharpe, la probabilité de sur-apprentissage exige une
      matrice de rejeux, et le walk-forward exige un découpage en fenêtres. Ce sont
      des grandeurs d'ensemble, et les produire à partir d'une seule stratégie
      donnerait des chiffres faux plutôt que des chiffres manquants.
      La valeur 0,5 passée à la significativité est la probabilité du hasard pur,
      pas un pourcent : le 13-09-2026, en passant 50, la variance devenait négative
      et la fonction rendait son cas de repli, une p-value de 1,0 sur
      103 opérations à 63 % de réussite. Un tel résultat est impossible, et c'est
      ce qui a permis de voir la faute.
    ⑨ CE QUI CLOCHE —
      ① Ce texte a longtemps affirmé que le juge à huit critères compte une mesure vide comme un
      critère non passé. C'est faux, et mesuré le 19-09-2026 : en appelant
      `evaluer_strategie_8_criteres` sur les mesures réellement produites pour
      C5E10-OBS-V1, avec ses quatre valeurs vides, la réponse est « TypeError: '>='
      not supported between instances of 'NoneType' and 'float' ». Le juge à huit critères ne
      compte pas le critère, il tombe. La cause est qu'il prend sa valeur par
      défaut uniquement quand la clé est ABSENTE : une clé présente et vide lui rend
      le vide. La conséquence est aujourd'hui sans effet parce que ce programme
      n'appelle jamais le juge à huit critères sur ces mesures — il s'arrête avant — mais le jour où
      il le fera, il s'arrêtera sur une erreur au lieu de rendre un score partiel.
      ② La stabilité n'est jamais calculée, et le code qui la calcule n'est jamais
      atteint. Les DEUX appelants passent une valeur vide comme façon de rejouer :
      vérifié le 19-09-2026, les deux seules lignes d'appel de cette fonction
      passent `None` à cette place. Le bloc qui demanderait la stabilité est donc du
      code inatteignable aujourd'hui, et le texte qui annonce que la stabilité est
      produite « si une façon de rejouer est fournie » décrit une possibilité que
      rien n'exerce.
      ③ Le compte annoncé « sur 9 » ne porte pas sur les neuf clés du juge à huit critères. Il
      compte le Sharpe, qui n'est pas un critère mais seulement un ingrédient du
      Deflated Sharpe, et il ne compte pas le taux de frais, qui est bien le
      huitième critère et qui est toujours renseigné. Relevé le 19-09-2026 dans le
      juge à huit critères, les neuf clés qu'il consulte sont la p-value, le Deflated Sharpe, la
      probabilité de sur-apprentissage, la chute maximale, la durée sous l'eau, le
      Kelly fractionnel, la stabilité, le walk-forward et le taux de frais. Les deux
      comptes donnent le même total ce jour-là, 5, par coïncidence : le Sharpe est
      chiffré et le taux de frais aussi.
      ④ Quatre nombres gouvernent la fonction sans qu'aucune phrase ne dise d'où ils
      viennent : le minimum de cinq opérations, le capital de 100 000 €, et les deux
      réglages passés au calcul de stabilité, 0,10 et 4. Le module de statistiques
      attend par défaut 5 variations et non 4 — relevé le 19-09-2026 dans sa
      signature — et rien ne dit pourquoi ce programme en demande une de moins.
      ⑤ Le Sharpe est relevé avec la précaution « si c'est un tableau, prends la
      clé, sinon prends la valeur », alors que la fonction appelée rend un nombre
      seul. Mesuré le 19-09-2026, le Sharpe rendu vaut 6,420448807904917, un nombre
      brut. La précaution ne coûte rien mais laisse croire que les deux formes ont
      été vues.
      ⑥ Le taux de réussite affiché n'est pas celui qui a servi aux calculs. La
      valeur rangée dans le tableau est arrondie au dixième, tandis que la
      significativité et le Kelly fractionnel reçoivent la valeur non arrondie.
      Mesuré le 19-09-2026 sur C5E10-OBS-V1, l'affichage porte 63,1 pour une valeur
      calculée qui compte bien plus de décimales. Un lecteur qui refait le calcul à
      partir du chiffre affiché ne retrouve pas exactement la p-value ni le Kelly
      rendus, et rien ne l'avertit que deux valeurs coexistent.
      ⑦ Les mesures sont produites sans aucune date. Deux passages à quelques jours
      d'intervalle, sur des cours différents, rendent des tableaux que rien ne
      permet de distinguer ni d'ordonner.
    ⑩ EFFET — Ne lit ni n'écrit aucun fichier, n'affiche rien, ne touche pas au
      réseau. Elle ne modifie pas la liste des opérations qu'elle reçoit : elle en
      construit une copie sous les noms attendus par le module de statistiques.
    ⑪ TERMINAISON — Rend toujours la main dans le cas normal, avec le tableau ou
      avec la raison de son absence. Et un de ses appels peut ne pas revenir : la
      conversion de l'objectif de gain ou de la perte acceptée lève si la case est
      vide ou porte du texte — mesuré le 19-09-2026, « ValueError: could not convert
      string to float: '' » — et l'absence de l'une de ces deux cases dans la fiche
      lève également.
      [sort: non]
    ⑫ DÉFINITIONS
      le juge à huit critères : `evaluer_strategie_8_criteres`, la fonction de
        `MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py` qui compare neuf mesures à
        leurs seuils et rend un score sur huit
      une opération : un achat simulé suivi de sa revente, avec son gain net en
        euros ; aucun ordre réel n'est jamais passé
      une fiche : la ligne qui décrit une stratégie dans le registre des stratégies, `donnees/cac40_strategies.csv` — son identifiant, ses réglages et ce qu'elle déclare.
      la p-value : la probabilité qu'un taux de réussite au moins aussi bon soit
        obtenu par le seul hasard ; plus elle est petite, moins le hasard explique
        le résultat
      le Kelly fractionnel : la part du capital qu'il serait raisonnable d'engager
        sur une opération, compte tenu du taux de réussite et des gains et pertes
        attendus
      la durée sous l'eau : le nombre de jours pendant lesquels le cumul des gains
        reste sous son plus haut précédent
      le Sharpe : le rapport du gain moyen à sa dispersion, ramené à l'année
      le Deflated Sharpe : le Sharpe corrigé du nombre de stratégies essayées ;
        plus on en essaie, plus un bon Sharpe peut n'être que du hasard
      la probabilité de sur-apprentissage : la probabilité qu'une stratégie doive
        ses bons résultats au réglage sur les données passées plutôt qu'à un effet
        réel
      le walk-forward : le rejeu d'une stratégie sur des tranches de temps
        successives, pour voir si elle tient hors de la période qui a servi à la
        régler
      le relecteur : celui qui relit le travail de l autre, ici Cowork
    """
    n = len(ops)
    if n < 5:
        return None, "moins de 5 opérations — rien à juger"
    wr = 100.0 * sum(1 for o in ops if o.get("net", 0) > 0) / n
    tp, sl = _pct(fiche["tp"]), _pct(fiche["sl"])
    # les operations, dans la forme que MODULE_STATISTIQUES attend
    trades = [{"date": o.get("date_signal"), "gain": o.get("net", 0.0)} for o in ops]

    # LE TAUX DE FRAIS SE LIT CHEZ SON PROPRIETAIRE — CC2 de Cowork, 13-09.
    # J avais ecrit 0.005 (50 bps) a la main, la ou `MODULE_POSITIONS.FRAIS_TAUX`
    # pose 0.0015 — le tarif Fortuneo PROGRESS, decision A-50. **Trois virgules
    # trois fois le taux reel, dans un programme qui ne lisait jamais la source.**
    # Et ce n est pas cosmetique : mesure du 13-09, le Kelly passe de 0.1574 a
    # 0.1885 — 19,8 % d ecart. « Il n invente pas le calcul, il invente son
    # entree. » C est R-708 : un chiffre qui existe ailleurs ne se recopie pas.
    m = {"n_trades": n, "wr_pct": round(wr, 1), "frais_pct": frais}

    # C1 — significativite du taux de reussite contre le hasard.
    # `p_null` EST UNE PROBABILITE, pas un pourcentage — 0.5 et non 50.
    # Mesure du 13-09 : en passant 50, la variance devenait negative et la
    # fonction rendait son cas de repli, z=0 et p=1.0. **Une p-value de 1.0 sur
    # 103 trades a 63 % est impossible, et c est ce qui m a alerte.**
    # Cinquieme fois aujourd hui que l unite se croise.
    r = stat.calculer_significativite_wr(n, wr, 0.5)
    m["p_value"] = r.get("p_value") if isinstance(r, dict) else r

    # C4 — pire chute et duree sous l eau
    # LES CLES SONT CELLES QUE LA FONCTION REND, relevees le 13-09 en l appelant :
    # {dd_max_eur, dd_max_pct, time_underwater_max_jours, time_underwater_total_jours}
    # **J avais devine `dd_pct` et `underwater_jours` : les deux rendaient None,
    # et un None se lit comme « critere non passe ».** On ne devine pas une cle.
    r = stat.calculer_time_underwater(trades, capital)
    if isinstance(r, dict):
        m["dd_pct"] = r.get("dd_max_pct")
        m["underwater_jours"] = r.get("time_underwater_max_jours")

    # C5 — Kelly fractionnel, depuis les reglages de la fiche
    # la cle est `kelly_fractionnel`, relevee de la meme facon
    r = stat.calculer_kelly_fractionnel(wr, tp, sl, frais, 0.5)
    m["kelly_frac"] = r.get("kelly_fractionnel") if isinstance(r, dict) else r

    # le Sharpe, qui nourrit C2
    r = stat.calculer_sharpe_ratio(trades)
    m["sharpe"] = r.get("sharpe") if isinstance(r, dict) else r

    # C6 — stabilite parametrique, et C3 — PBO : les deux exigent de REJOUER
    if rejouer is not None:
        r = stat.calculer_stabilite_parametrique(rejouer, {"tp": tp, "sl": sl}, 0.10, 4)
        m["stable"] = r.get("stable") if isinstance(r, dict) else r

    # CC3 de Cowork : « cinq mesures sur neuf, et non sept. `pbo` et `stable`
    # n etaient JAMAIS PRODUITES — pas meme a None. » Il a raison, et l absence
    # d une cle est pire qu un None : le juge à huit critères ne la voit pas du tout, et le
    # lecteur ne peut pas savoir qu elle manque.
    # **LES NEUF CLES SONT DESORMAIS TOUJOURS PRESENTES.** Celles qu on ne sait
    # pas produire valent None, et le compte ci-dessous le dit sans detour.
    m.setdefault("pbo", None)          # exige une MATRICE de rejeux
    m.setdefault("stable", None)       # exige un rejeu sous variations
    m["dsr"] = None                    # exige le LOT ENTIER
    m["wf_tous_positifs"] = None       # exige un decoupage en fenetres
    chiffrees = sum(1 for k in ("p_value", "dsr", "pbo", "dd_pct", "underwater_jours",
                                "kelly_frac", "stable", "wf_tous_positifs", "sharpe")
                    if m.get(k) is not None)
    m["_chiffrees_sur_9"] = chiffrees
    return m, None


def _juger_une(base, banc, stat, ident):
    """Joue UNE stratégie du registre par le juge des stratégies, et affiche ses mesures.

    ① RÔLE — Traverser la chaîne entière pour une stratégie nommée : retrouver sa
      ligne au registre des stratégies, réunir tout ce dont le juge des stratégies a besoin, le
      faire jouer, puis afficher les mesures obtenues et dire combien manquent.
      Elle ne juge pas : aucun score n'est rendu, parce que quatre des neuf mesures
      ne sont pas produites et qu'un score calculé sur cinq serait indiscernable
      d'un score complet.
    ② CONTEXTE D'APPEL — `main`, une seule fois, et seulement quand `--strategie`
      est suivi d'un identifiant. Jamais appelée ailleurs. Ce qu'elle rend devient
      le code de sortie du programme.
    ③ ENTRÉE — `base` : la racine à parcourir. `banc` : le juge des stratégies, l'objet issu de l'exécution
      de `JUGE_DES_STRATEGIES.py`. `stat` : l'objet issu de l'exécution du module de
      statistiques. `ident` : l'identifiant de la stratégie, pris sur la ligne de
      commande juste après `--strategie`, par exemple `C5E10-OBS-V1`. Un seul
      appelant, `main`, qui transmet les quatre sans les modifier.
    ④ CONDITIONS D'ENTRÉE — La racine doit porter `cac40_strategies.csv`, un fichier
      dont le nom commence par `REFERENTIEL_VALEURS`, `MODULE_C5_ETENDU_10_*` et
      `MODULE_POSITIONS.py`. L'identifiant doit correspondre à une ligne du registre
      des stratégies, et cette ligne doit porter un univers renseigné. Le juge des stratégies doit
      savoir trouver et charger les cours à partir de la même racine.
    ⑤ SORTIE — UNE valeur : le code de sortie du programme. 0 dans quatre cas
      différents — la mesure prise, l'univers non renseigné, l'échec du juge des stratégies, et
      moins de cinq opérations. 2 dans trois cas — registre des stratégies
      introuvable, identifiant absent du registre, module de signal ou de positions
      introuvable. Elle affiche en plus de deux à une vingtaine de lignes.
      [rend: 1]
    ⑥ TRAITEMENT — ① chercher `cac40_strategies.csv` sous la racine, et rendre 2
      s'il est absent · ② y chercher la ligne de l'identifiant, et rendre 2 si elle
      n'y est pas · ③ s'arrêter en rendant 0 si l'univers est vide, porte le mot
      « renseigner » ou le mot « TRANCHER » · ④ demander au juge des stratégies de charger les
      cours · ⑤ charger le module de signal et celui des positions, et rendre 2 si
      l'un manque · ⑥ lire le référentiel des valeurs pour associer chaque
      mnémonique au nom employé dans les cours · ⑦ poser sur la fiche le nom de la
      fonction de signal, repris du juge des stratégies · ⑧ faire jouer la stratégie et récupérer
      ses opérations, en rendant 0 si le juge des stratégies échoue · ⑨ afficher le nombre
      d'opérations et les mnémoniques inconnus · ⑩ demander les mesures · ⑪ les
      afficher une par ligne, un tiret pour celles qui manquent · ⑫ afficher le nom
      de la grille appliquée, le compte des mesures chiffrées, celles qui manquent,
      et qu'aucun score n'est rendu.
    la fiche : la ligne d'une stratégie au registre des stratégies `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte acceptée, son horizon et son univers
    le module de signal : le programme qui décide quelles valeurs acheter
    ⑦ UNITÉ — Les opérations se comptent en NOMBRE D'OPÉRATIONS : 103 pour
      C5E10-OBS-V1, mesuré le 19-09-2026. Les mnémoniques inconnus se comptent en
      NOMBRE DE VALEURS. Les mesures affichées portent chacune l'unité que le calcul
      des mesures leur donne.
    ⑧ POURQUOI — Un univers non renseigné arrête la mesure au lieu d'être traité
      comme un univers vide. Relevé le 19-09-2026 dans le registre des stratégies :
      sur 68 lignes, 9 portent un univers, et parmi elles trois disent « à
      renseigner » et une dit « A TRANCHER — voir etude_ref ». Quatre stratégies
      seulement sont réellement jouables. Deviner l'univers d'une stratégie qui n'en
      déclare pas produirait un résultat que rien ne distinguerait d'une vraie
      mesure, alors que l'univers est le paramètre le plus puissant du système.
      L'identité d'une valeur est son MNÉMONIQUE, jamais son nom. Le registre des
      stratégies désigne ses valeurs par des codes courts comme `TTE` ou `URW`, et
      les cours les désignent par un nom d'usage. Le référentiel des valeurs est le
      seul endroit qui relie les deux, et il est relu ici plutôt que deviné : une
      même entreprise s'écrit différemment selon le fichier, et sans rapprochement
      le programme croirait qu'il s'agit de deux sociétés distinctes.
      Le nom de la fonction de signal est REPRIS DU JUGE DES STRATÉGIES plutôt que choisi ici. Le
      juge des stratégies pose lui-même une valeur par défaut, et le registre des stratégies ne
      porte pas cette information. Si ce programme en choisissait une, deux endroits
      décideraient du même nom et divergeraient un jour ; un chiffre ou un nom qui
      existe ailleurs ne se recopie pas (R-708).
    ⑨ CE QUI CLOCHE —
      ① Trois chemins d'échec rendent 0. Mesuré le 19-09-2026 sur une copie du
      dépôt, `--strategie MA200-S1` affiche « INJOUABLE, rien mesuré. » et le code
      de sortie relevé est 0, le même que pour une mesure réussie. Il en va de même
      quand le juge des stratégies échoue à jouer la stratégie et quand il y a moins de cinq
      opérations. Une tâche qui ne regarderait que le code de sortie ne verrait
      aucune différence. Un contrôle qui n'a pas pu tourner rend un code de sortie
      non nul (R-734).
      ② L'échec du juge des stratégies est rattrapé en bloc, quelle qu'en soit la cause. Le message
      affiché nomme le type de l'erreur et son texte, mais la trace est perdue : une
      erreur de programmation dans le juge des stratégies et une donnée manquante produisent la
      même ligne d'affichage et le même code 0.
      ③ Le nom de la fonction de signal est repris du juge des stratégies PAR RECOPIE, et c'est
      exactement ce que la raison invoquée interdit. La valeur `signaux_c5etendu10`
      est écrite ici, en toutes lettres, à côté d'un commentaire qui explique que le
      juge des stratégies la pose déjà par défaut. Les deux endroits portent donc bien le même nom
      écrit deux fois : si le juge des stratégies change sa valeur par défaut, celle-ci ne suivra
      pas.
      ④ Les seuils et l'horizon de la stratégie viennent du registre des stratégies,
      pas du REGISTRE. Vérifié le 19-09-2026 : la ligne C5E10-OBS-V1 de
      `donnees/cac40_strategies.csv` porte objectif +4.0 %, perte acceptée −2.5 %,
      horizon 20, et la règle R-201 du REGISTRE écrit pour la même famille de
      stratégies « TP +4 % · SL −2,5 % · 20 séances ». Les deux disent aujourd'hui
      la même chose, et rien ne le vérifie : c'est le fichier à colonnes qui est lu,
      et le REGISTRE ne l'est jamais pour cela. La loi du projet veut que les seuils
      et l'horizon d'une stratégie viennent du REGISTRE et non d'ailleurs (R-743,
      deuxième geste) ; cette fonction ne l'applique pas.
      ⑤ L'horizon n'est contrôlé nulle part ici. Il est transmis au juge des stratégies dans la
      fiche, et c'est le juge des stratégies qui le lit. Une case d'horizon portant du texte — le
      registre en porte une, `Intraday`, relevée le 19-09-2026 — n'est donc vue
      qu'une fois le juge des stratégies lancé.
      ⑥ Les mnémoniques inconnus sont affichés et n'arrêtent rien. Une valeur
      attendue qui ne renvoie rien est pourtant une alerte : une stratégie qui
      devait acheter sur dix valeurs et n'en retrouve que huit mesure autre chose
      que ce qu'annonce sa fiche, et le compte des opérations ne le dit pas.
      ⑦ Le parcours qui cherche le référentiel des valeurs s'arrête au premier
      dossier qui en porte un, et il n'écarte pas `_site_travail`, contrairement au
      parcours qui cherche le registre des stratégies quelques lignes plus haut.
      Deux parcours voisins dans la même fonction n'écartent pas les mêmes dossiers.
      ⑧ Le module des positions est chargé ici puis passé au juge des stratégies, et le taux de
      frais est relu une seconde fois par un parcours séparé au lieu d'être demandé
      au module déjà chargé. Mesuré le 19-09-2026 en marquant `MODULE_POSITIONS.py`,
      il est exécuté 5 fois sur un passage `--strategie`.
    ⑩ EFFET — LIT l'arborescence de la racine plusieurs fois, LIT le registre des
      stratégies et le référentiel des valeurs, et LIT ET EXÉCUTE le module de
      signal et celui des positions. Fait LIRE les cours par le juge des stratégies. N'écrit aucun
      fichier et ne touche pas au réseau : vérifié le 19-09-2026, après un passage
      complet sur une copie du dépôt, la comparaison avec l'original ne rend aucune
      différence hors le dossier `__pycache__` de Python. AFFICHE de deux à une
      vingtaine de lignes.
    ⑪ TERMINAISON — Rend toujours la main avec 0 ou 2 dans les cas prévus. Et un de
      ses appels peut ne pas revenir : la lecture du taux de frais lève si
      `MODULE_POSITIONS.py` ou son taux sont introuvables, et la conversion de
      l'objectif de gain ou de la perte acceptée lève si la case est vide ou porte
      du texte. L'échec du juge des stratégies, lui, est rattrapé et ne termine rien.
      [sort: non]
    ⑫ DÉFINITIONS
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
      le registre des stratégies : le fichier `cac40_strategies.csv`, une ligne par stratégie, qui porte leur état civil — identifiant, réglages, résultats connus
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
      la grille : la liste des huit critères et de leurs seuils ; celle qui tourne s'appelle GRILLE-26-04 et vit dans `CRITERES_VALIDATION_EXPERTS`, lignes 1730 à 1740 de ce fichier
      un mnémonique : le code court d'une valeur de bourse, `TTE` pour TotalEnergies
        par exemple ; c'est lui qui identifie une valeur, jamais son nom
      le référentiel des valeurs : donnees/REFERENTIEL_VALEURS_*.csv, la liste des valeurs à suivre, avec pour chacune son mnémonique et sa place de cotation.
      l'univers : la liste des valeurs sur lesquelles une stratégie a le droit d'acheter, désignées par leur mnémonique
      une opération : un achat simulé suivi de sa revente, avec son gain net en
        euros ; aucun ordre réel n'est jamais passé
      une fiche : la ligne qui décrit une stratégie dans le registre des stratégies, `donnees/cac40_strategies.csv` — son identifiant, ses réglages et ce qu'elle déclare.
    """
    import csv as _csv
    ch = None
    for r, sd, fs in os.walk(base):
        sd[:] = [x for x in sd if x not in ("archives", ".git", "__pycache__", "_site_travail")]
        if "cac40_strategies.csv" in fs:
            ch = os.path.join(r, "cac40_strategies.csv"); break
    if not ch:
        print("CODE 2 — registre des stratégies introuvable."); return 2
    fiche = None
    for x in _csv.DictReader(open(ch, encoding="utf-8-sig")):
        if x["id"] == ident:
            fiche = x; break
    if not fiche:
        print(f"CODE 2 — {ident} absente du registre."); return 2
    u = (fiche.get("univers") or "").strip()
    if not u or "renseigner" in u.lower() or "TRANCHER" in u:
        print(f"  {ident} : univers « {u[:40]} » — INJOUABLE, rien mesuré.")
        print("     Un univers non renseigné n'est pas un univers vide : on ne devine pas.")
        return 0
    cours = banc.charger_cours(*banc.fichiers_de_cours(base))
    mod_sig, _ = _charger(base, "MODULE_C5_ETENDU_10_*")
    mod_pos, _ = _charger(base, "MODULE_POSITIONS.py")
    if mod_sig is None or mod_pos is None:
        print("CODE 2 — module de signal ou de positions introuvable."); return 2
    mnemo = {}
    for r2, sd2, fs2 in os.walk(base):
        sd2[:] = [x for x in sd2 if x not in ("archives", ".git", "__pycache__")]
        for f2 in fs2:
            if f2.startswith("REFERENTIEL_VALEURS"):
                for x in _csv.DictReader(open(os.path.join(r2, f2), encoding="utf-8-sig")):
                    m2 = (x.get("mnemonique") or "").strip().upper()
                    n2 = (x.get("onglet_google") or x.get("nom_usuel") or "").strip()
                    if m2 and n2: mnemo[m2] = banc.cle_valeur(n2)
                break
    # LE NOM DE LA FONCTION DE SIGNAL VIENT DU JUGE DES STRATÉGIES, PAS DE MOI.
    # `JUGE_DES_STRATEGIES` ligne 883 pose lui-même `_fonction_signal` par défaut ; le
    # registre ne porte pas cette clé. **Je reprends SA valeur plutôt que d en
    # choisir une** — sinon deux endroits décideraient du même nom (R-708).
    fiche = dict(fiche)
    fiche.setdefault("_fonction_signal", "signaux_c5etendu10")
    try:
        ops, inconnus = banc.jouer(fiche, cours, mnemo, mod_sig, mod_pos)
    except Exception as e:
        print(f"  {ident} : le juge des stratégies n'a pas pu la jouer — {type(e).__name__} : {e}")
        return 0
    print(f"  {ident} : {len(ops)} opération(s)"
          + (f" · {len(inconnus)} mnémonique(s) inconnu(s) : {inconnus}" if inconnus else ""))
    m, motif = mesures_disponibles(fiche, ops, stat, None, _frais_taux(base))
    if m is None:
        print(f"     {motif}"); return 0
    print("     mesures produites :")
    for k, v in m.items():
        etat = "—" if v is None else v
        print(f"       {k:<20} {etat}")
    print(f"     GRILLE APPLIQUÉE : {GRILLE} — tout verdict la nomme (R-743).")
    print(f"     {m.get('_chiffrees_sur_9')} mesure(s) chiffrée(s) sur 9 —"
          f" les autres sont à None, et le juge à huit critères les comptera NON PASSÉES.")
    print("     dsr (lot entier) · pbo (matrice de rejeux) · stable (rejeu sous")
    print("     variations) · wf (découpage en fenêtres) : aucune n'est produite.")
    print("     AUCUN SCORE N'EST RENDU tant qu'elles manquent.")
    return 0


def main():
    """Enchaîne les contrôles, charge les programmes, et rend le code de sortie.

    ① RÔLE — Conduire le programme du début à la fin dans un ordre qui ne peut pas
      s'inverser : rien n'est mesuré tant que l'instrument n'a pas prouvé qu'il
      fonctionne. Deux calibrages et un contrôle des seuils passent avant tout
      chargement du juge des stratégies, et chacun des trois arrête le programme s'il échoue.
    ② CONTEXTE D'APPEL — Le lancement du programme, et lui seul. Sa valeur de retour
      est passée directement à la sortie du processus.
    ③ ENTRÉE — Aucun paramètre. Elle lit elle-même la ligne de commande : le premier
      argument est la racine à parcourir, et les mots `--calibrage` et
      `--strategie` sont cherchés n'importe où dans les arguments suivants.
    ④ CONDITIONS D'ENTRÉE — La ligne de commande doit porter au moins un argument.
      La racine doit porter les programmes et les fichiers que les étapes suivantes
      cherchent.
    ⑤ SORTIE — UNE valeur : un entier, le code de sortie. 2 quand aucun argument
      n'est donné ou qu'une source est absente. 1 quand un calibrage échoue ou qu'un
      seuil ne se retrouve pas au REGISTRE. 0 quand la mesure a été prise, quand
      `--calibrage` s'est bien déroulé, ou quand aucune stratégie n'a été nommée.
      [rend: 1]
    ⑥ TRAITEMENT — ① sans argument, afficher le texte d'en-tête du fichier et rendre
      2 · ② charger le module de statistiques, et rendre 2 s'il manque · ③ afficher
      son chemin · ④ calibrer le juge à huit critères, et rendre 1 s'il ne reproduit plus le
      résultat connu · ⑤ calibrer le branchement, et rendre 1 s'il ne rend pas ce
      qu'il doit · ⑥ vérifier que les seuils s'écrivent au REGISTRE, et rendre 1
      sinon · ⑦ s'arrêter en rendant 0 si `--calibrage` est demandé · ⑧ charger le
      juge des stratégies, et rendre 2 s'il manque · ⑨ chercher un identifiant de stratégie après
      `--strategie` · ⑩ s'il y en a un, faire juger cette stratégie et rendre ce
      qu'elle rend · ⑪ sinon, afficher ce qui reste à faire et rendre 0.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — L'ordre des étapes est la seule chose qui garantit qu'un chiffre
      faux ne s'affiche pas. Les trois contrôles portent sur trois choses
      différentes et ne se remplacent pas : le premier prouve que le juge à huit critères reproduit
      un résultat connu, le deuxième prouve que le branchement rend ce qu'il doit,
      le troisième prouve que les seuils du code et ceux du REGISTRE ne divergent
      pas. Le 13-09-2026, seul le premier existait ; il est resté vert alors que le
      branchement rendait une p-value de 1,0 sur 103 opérations à 63 % de réussite,
      et le programme est sorti en code 0.
      Les trois arrêtent le programme au lieu d'avertir. Un chiffre produit par un
      instrument non calibré s'affiche exactement comme un chiffre juste : le
      laisser sortir avec un avertissement, c'est le laisser sortir.
      `--calibrage` existe pour que les trois contrôles puissent être passés seuls,
      sans jouer aucune stratégie. Mesuré le 19-09-2026 sur une copie du dépôt, ce
      passage rend quatre lignes et un code de sortie 0.
    ⑨ CE QUI CLOCHE —
      ① `--strategie` écrit sans identifiant ne dit rien. Mesuré le 19-09-2026 sur
      une copie du dépôt : `--strategie` en dernier argument ne fait afficher ni
      erreur ni avertissement ; le programme déroule le message qui explique ce qui
      reste à faire et sort en code 0, exactement comme s'il avait été lancé sans
      demander de stratégie. Qui a fait une faute de frappe dans son identifiant
      obtient donc un passage vert et aucune mesure.
      ② Les arguments sont cherchés n'importe où, et le premier est pris pour la
      racine quoi qu'il soit. Lancer le programme avec `--calibrage` comme premier
      argument fait chercher les programmes dans un dossier nommé `--calibrage`, qui
      n'existe pas : le module de statistiques est déclaré introuvable et le
      programme sort en 2, avec un message qui désigne le module plutôt que
      l'argument mal placé.
      ③ Le mode d'emploi affiché sans argument est le texte d'en-tête du fichier
      tout entier. Ce texte fait aujourd'hui plusieurs centaines de lignes, puisque
      la règle qui gouverne les textes explicatifs impose douze éléments (R-752) :
      le mode d'emploi défile à l'écran et les deux lignes qui comptent vraiment,
      l'usage et les codes de sortie, se perdent dedans. Elles ont pour cette raison
      été placées en tête du texte d'en-tête.
      ④ Le code de sortie ne distingue pas « mesuré » de « rien mesuré ». Ce que
      rend le jugement d'une stratégie est repris tel quel, et ce jugement rend 0
      aussi bien quand cinq mesures ont été produites que quand l'univers n'était
      pas renseigné — mesuré le 19-09-2026 sur la stratégie MA200-S1.
      ⑤ Aucune ligne affichée ne porte de date ni d'heure, alors que la zone horaire
      de Paris est préparée en tête du fichier. Deux passages sur des cours
      différents rendent des sorties que rien ne permet de dater ni d'ordonner.
      ⑥ Le message final, celui qui s'affiche quand aucune stratégie n'est nommée,
      annonce que le pont n'est pas encore traversé. Il l'est pourtant : la fonction
      qui joue une stratégie existe et fonctionne, mesurée le 19-09-2026 sur
      C5E10-OBS-V1 avec 103 opérations et cinq mesures produites. Le texte décrit un
      état antérieur du programme.
    ⑩ EFFET — N'ÉCRIT AUCUN FICHIER et ne touche pas au réseau. Vérifié le
      19-09-2026 : après un passage complet sur une copie du dépôt, la comparaison
      fichier par fichier avec l'original ne rend aucune différence, hors le dossier
      `__pycache__` que Python crée pour son propre compte. LIT l'arborescence de la
      racine plusieurs fois et EXÉCUTE les programmes qu'elle y trouve. AFFICHE de
      quatre à une vingtaine de lignes, ou le texte d'en-tête entier quand aucun
      argument n'est donné.
    ⑪ TERMINAISON — Rend toujours la main avec 0, 1 ou 2 dans les cas prévus, et sa
      valeur devient le code de sortie du programme. Et un de ses appels peut ne pas
      revenir : le calibrage du branchement et le jugement d'une stratégie appellent
      la lecture du taux de frais, qui lève si `MODULE_POSITIONS.py` ou son taux
      sont introuvables ; le chargement d'un programme lève ce que ce programme
      lève ; et la conversion d'un objectif de gain ou d'une perte acceptée lève sur
      une case vide ou textuelle. Dans tous ces cas la trace Python s'affiche et le
      code de sortie est 1.
      [sort: non]
    ⑫ DÉFINITIONS
      le juge des stratégies : `programmes/JUGE_DES_STRATEGIES.py`, le programme qui rejoue une stratégie sur l'historique des cours et rend la liste de ses opérations
      le juge à huit critères : `evaluer_strategie_8_criteres`, la fonction de
        `MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py` qui compare neuf mesures à
        leurs seuils et rend un score sur huit
      le pont : le branchement entre le juge des stratégies et le juge à huit critères, qui est tout ce que ce
        programme ajoute
      le REGISTRE : `gouvernance/REGISTRE_REGLES.md`, le document qui porte les règles numérotées du projet
      la p-value : la probabilité qu'un taux de réussite au moins aussi bon soit
        obtenu par le seul hasard ; plus elle est petite, moins le hasard explique
        le résultat
      une opération : un achat simulé suivi de sa revente, avec son gain net en
        euros ; aucun ordre réel n'est jamais passé
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
    
      l'univers : la liste des valeurs sur lesquelles une stratégie a le droit d'acheter, désignées par leur mnémonique
      la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
      la trace : la liste des sources avec leur etat — LU, ABSENT ou ILLISIBLE — et un detail chiffre, affichee en pied de page.
      le calibrage : le contrôle qui rejoue une stratégie déjà mesurée et exige de retrouver son résultat connu avant que le juge des stratégies ne juge quoi que ce soit.
      le module de statistiques : le programme qui porte le voisinage des réglages et le pire creux, `programmes/MODULE_STATISTIQUES_Lun_24-08-2026_22h00.py`.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    base = sys.argv[1]
    stat, chemin = _charger(base, "MODULE_STATISTIQUES_*")
    if stat is None:
        print("CODE 2 — MODULE_STATISTIQUES introuvable : on ne réécrit PAS ses calculs.")
        return 2
    print(f"  statistiques : {chemin}")
    if not calibrer(stat):
        return 1
    if not calibrer_le_pont(stat, base):
        return 1
    ecarts = seuils_du_registre(base)
    if ecarts:
        print(f"  SEUILS — *** {GRILLE} et le code ne disent pas la même chose ***")
        for e in ecarts:
            print(f"     · {e}")
        print("     RIEN N'EST MESURÉ : un seuil qui diverge en silence fausse tout verdict.")
        return 1
    print(f"  SEUILS — {GRILLE} au REGISTRE porte les neuf seuils du code")
    if "--calibrage" in sys.argv:
        return 0

    banc, ch_banc = _charger(base, "JUGE_DES_STRATEGIES.py")
    if banc is None:
        print("CODE 2 — JUGE_DES_STRATEGIES introuvable : il seul sait jouer une stratégie.")
        return 2
    print(f"  juge des stratégies : {ch_banc}")

    # ─── ON TRAVERSE : une stratégie est jouée, puis mesurée ───
    cible = None
    if "--strategie" in sys.argv:
        i = sys.argv.index("--strategie")
        if i + 1 < len(sys.argv):
            cible = sys.argv[i + 1]
    if cible:
        code = _juger_une(base, banc, stat, cible)
        return code

    print()
    print("  ─── CE PONT EST POSÉ, IL N'EST PAS ENCORE TRAVERSÉ ───")
    print("  Le juge à huit critères est calibré et les deux modules se chargent. Ce qui reste :")
    print("   · faire jouer chaque stratégie par le juge des stratégies et récupérer ses opérations ;")
    print("   · en tirer les NEUF mesures que le juge à huit critères attend — `juger` du juge des stratégies n'en")
    print("     produit que trois : taux de réussite, point mort, borne de Wilson ;")
    print("   · pour C2 (Deflated Sharpe), il faut le lot ENTIER : le nombre de")
    print("     stratégies testées et la variance de leurs Sharpe sont des grandeurs")
    print("     d'ensemble. Juger une seule stratégie rendrait un C2 faux.")
    print()
    print("  RIEN N'EST ÉCRIT : ce programme ne produit pas de score tant que les")
    print("  neuf mesures ne sont pas toutes disponibles. Un score partiel présenté")
    print("  comme complet serait pire que pas de score.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
