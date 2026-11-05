#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MÉTÉO DU MARCHÉ — le voyant « moyenne des 200 séances » du CAC 40 (A-615). Simulation uniquement.

① RÔLE — Dire chaque soir où en est la bourse entière : le CAC 40 est-il AU-DESSUS (🟢) ou EN DESSOUS (🔴) de
  la moyenne de ses 200 dernières clôtures, depuis combien de séances, et est-il en zone de krach (20 % ou plus
  sous son plus haut d'un an). C'est un VOYANT, pas un ordre : il n'achète ni ne vend rien.
② CONTEXTE D'APPEL — Le circuit du soir (.github/workflows/collecte_abc.yml, pas « Calculer la meteo du
  marche »), après la collecte ; ou à la main. Décision de Jean-Luc du 29-10-2026 à 13h39 (« Faire la
  moyenne »), après l'étude etudes/PLAN_PREVOIR_ET_SE_PROTEGER_CAC40_INDICE_Mer_28-10-2026.
③ ENTRÉE — argv[1] : racine du dépôt · argv[2] facultatif : `sans_collecte` (ne va pas sur le réseau) ou
  `epreuves` (jeu d'épreuves interne, sur des copies, jamais sur la racine donnée).
④ CONDITIONS D'ENTRÉE — donnees/sources_indice/INDICE_CAC40.csv (historique figé depuis 2000) et
  donnees/CALENDRIER_EURONEXT.csv (lu par CALENDRIER_DE_LA_BOURSE) existent.
⑤ SORTIE — UN code de sortie : 0 si la météo est à jour et sûre · 2 sinon (page non lue, page incohérente,
  révision, série trouée, données en retard, erreur imprévue) — R-734 : un contrôle qui n'a pas tourné ne se tait
  pas. Écrit toujours le rapport et les deux fichiers de données, même vides.
  [rend: 1]
⑥ TRAITEMENT — ① lire la page de l'indice chez ABC (code PX1p) avec `telecharger` et `extraire` de
  COLLECTER_ABC_GITHUB (importés, jamais recopiés : R-708) · ② confronter la page : à l'historique figé (un écart
  > 0,1 % sur une séance commune) ET au fichier quotidien : UN SEUL désaccord et RIEN n'est écrit ce soir-là
  (relecture du 29-10-2026, tour 2 : sinon une page fausse s'écrit dès qu'elle ne recouvre plus l'historique) ;
  exiger au moins une séance commune ; refuser une variation de plus de 15 % d'une séance à l'autre · l'issue
  d'un blocage est une DÉCISION DE JEAN-LUC, lue dans donnees/meteo_decisions.csv (date, close retenue ou vide
  pour garder ABC, motif), comme A-231 pour les actions · ③ ajouter les séances neuves et sûres · ④ vérifier,
  DATE PAR DATE au calendrier d'Euronext, que les séances connues après l'historique sont exactement les jours
  de bourse jusqu'à la dernière séance close (ni trou, ni jour en trop, ni retard) · ⑤ calculer le voyant en un
  seul passage, ne l'afficher que si la série est sûre · ⑥ écrire le rapport et une ligne PAR PASSAGE qui
  apporte une séance nouvelle dans donnees/meteo_du_marche.csv.
⑦ UNITÉ — Points d'indice ; écarts en fraction (0,05 = 5 %) ; retards en JOURS DE BOURSE.
⑧ POURQUOI — Étude du 28-29-10-2026 : hors marché sous la moyenne des 200 séances, la pire baisse a été
  ramenée de −60 % à −37 % (2001-2016) et de −39 % à −17 % (2017-2023), pour un peu de rendement en moins, et
  a été pire en 2024-2026 sans krach (−27 % contre −17 %). Non prouvé statistiquement (5 krachs en 23 ans) :
  d'où un voyant de prudence, pas une règle automatique.
⑨ CE QUI CLOCHE — La page PX1p d'ABC n'a jamais été lue par ce programme (réseau fermé là où il a été écrit) :
  THÉORIQUE jusqu'au premier passage réel (BACKLOG). Le calendrier d'Euronext ne couvre que 2026 : à partir du
  02-01-2027 la continuité ne sera plus vérifiable et le voyant sortira en code 2 chaque soir tant que 2027
  n'est pas relevé (BACKLOG). Six séances de fin d'année n'ont que la source `bnains` et sont ignorées.
  La moyenne des 200 séances est aussi calculée dans l'étude : deux écritures d'un même calcul. Aucune reprise
  automatique si la page ne recouvre plus rien de connu (panne longue) : issue = décision de Jean-Luc (BACKLOG).
  Une page dont le volume s'écrit « - » serait ignorée par `extraire` : THÉORIQUE.
⑩ EFFET — Écrit rapports/meteo_du_marche.md, donnees/meteo_du_marche.csv, donnees/indice_cac40_quotidien.csv ;
  sort sur le réseau une fois (une page).
⑪ TERMINAISON — Rend toujours la main : le téléchargement a un délai de 30 secondes, toute erreur est
  rattrapée et écrite au rapport.
  [sort: oui]
"""
import sys, os, csv, shutil, tempfile, traceback
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo

CODE_ABC = 'PX1p'
SEANCES_MOYENNE = 200          # Faber (2007) ; demandé par Jean-Luc le 28-10-2026
SEANCES_PLUS_HAUT = 252        # un an de bourse
SEUIL_KRACH = -0.20            # décision de Jean-Luc du 28-10-2026 à 19h08
ECART_SOURCES = 0.001          # 0,1 % : deux sources de la même clôture ; l'historique diffère de bnains de 1,1 % au plus sur 12 séances
VARIATION_MAX = 0.15           # 15 % : la plus forte variation d'une séance depuis 2000 est −12,28 % (12-03-2020), mesuré le 29-10-2026
ENTETE_QUOTIDIEN = ['date', 'close', 'source']
ENTETE_METEO = ['date', 'cloture', 'moyenne_200', 'ecart', 'couleur', 'depuis', 'sous_plus_haut', 'krach']


def chemins(racine):
    """rend les chemins utilisés, tous sous la racine donnée.

    ① RÔLE — Écrire à UN SEUL endroit où vivent les fichiers et le dossier de programmes de la
      météo, pour que le passage réel et les épreuves, qui travaillent dans un dossier temporaire,
      lisent et écrivent les mêmes chemins relatifs.
    ② CONTEXTE D'APPEL — `modules` et `executer`, une fois par passage ; `epreuves`, une fois sur
      la racine donnée ; `cas`, une fois par cas sur son dossier temporaire.
    ③ ENTRÉE — `racine` : la racine du dépôt ou de sa copie. Au passage réel, le premier argument
      de la ligne de commande (« $GITHUB_WORKSPACE » dans le circuit du soir), « . » s'il manque.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire de six clés (historique, quotidien, meteo, decisions,
      rapport, programmes), chacune vers un chemin sous la racine.
      [rend: 1]
    ⑥ TRAITEMENT — Assemble chaque chemin à partir de la racine.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Deux écritures d'une même chose finissent par différer (R-708) : les épreuves et
      le passage réel partagent donc la même table.
    ⑨ CE QUI CLOCHE — Rien vu.
    ⑩ EFFET — Aucun : ne lit ni n'écrit rien.
    ⑪ TERMINAISON — Rend la main. Ses appels assemblent des chemins et reviennent toujours.
      [sort: non]
    ⑫ DÉFINITIONS
      le circuit du soir : le passage automatique de chaque soir sur une machine GitHub,
        .github/workflows/collecte_abc.yml, réveillé depuis le dépôt public (18h07, secours 21h23,
        rattrapage 7h41 le lendemain matin, d'après l'en-tête de collecte_abc.yml)
    """
    j = lambda *p: os.path.join(racine, *p)
    return {'historique': j('donnees', 'sources_indice', 'INDICE_CAC40.csv'), 'quotidien': j('donnees', 'indice_cac40_quotidien.csv'),
            'meteo': j('donnees', 'meteo_du_marche.csv'), 'decisions': j('donnees', 'meteo_decisions.csv'),
            'rapport': j('rapports', 'meteo_du_marche.md'), 'programmes': j('programmes')}


def modules(racine):
    """importe COLLECTER_ABC_GITHUB et CALENDRIER_DE_LA_BOURSE du dépôt donné.

    ① RÔLE — Emprunter sans les recopier la lecture de la page d'ABC (téléchargement, extraction,
      heure de clôture) et le calendrier de la bourse.
    ② CONTEXTE D'APPEL — `executer`, une fois par passage ; `epreuves`, une fois, avant de
      remplacer le téléchargement et l'extraction par des simulations.
    ③ ENTRÉE — `racine` : la racine du dépôt (voir `chemins`) ; son dossier programmes est mis en
      tête du chemin d'import.
    ④ CONDITIONS D'ENTRÉE — programmes/COLLECTER_ABC_GITHUB.py et programmes/CALENDRIER_DE_LA_BOURSE.py
      existent sous la racine et s'importent.
    ⑤ SORTIE — DEUX valeurs : le module COLLECTER_ABC_GITHUB, puis le module CALENDRIER_DE_LA_BOURSE.
      [rend: 2]
    ⑥ TRAITEMENT — ① placer programmes/ en tête du chemin d'import (sys.path) · ② importer les
      deux modules.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La lecture de la page et le calendrier existent déjà et sont éprouvés ailleurs :
      les recopier en ferait deux versions qui divergent (R-708).
    ⑨ CE QUI CLOCHE — ① Chaque appel AJOUTE une entrée à sys.path, jamais retirée : les épreuves
      l'allongent d'une entrée par cas. ② Python garde en mémoire un module déjà importé : un
      second appel avec une AUTRE racine rend les modules de la PREMIÈRE, sans rien dire ; les
      épreuves en dépendent (voir le ⑨ d'`epreuves`).
    ⑩ EFFET — Modifie sys.path pour tout le processus ; au premier import, exécute le haut des deux
      modules (des constantes et des imports, aucune écriture : lu le 31-10-2026).
    ⑪ TERMINAISON — Rend la main, ou LÈVE si un import échoue (rattrapé par `executer`, pas par
      `epreuves`). Aucun appel ne peut ne pas revenir.
      [sort: non]
    ⑫ DÉFINITIONS
      ABC : ABC Bourse, le site d'où le projet lit les cours ; PX1p y est le code du CAC 40
    """
    sys.path.insert(0, chemins(racine)['programmes'])
    import COLLECTER_ABC_GITHUB as ABC, CALENDRIER_DE_LA_BOURSE as K
    return ABC, K


def creer_si_absent(chemin, entete):
    """crée un CSV vide avec son en-tête (le circuit enregistre ce fichier chaque soir, il doit exister) ;
    ajoute un saut de ligne final s'il manque (sinon la ligne suivante se collerait).

    ① RÔLE — Garantir que les deux fichiers de données de la météo existent et finissent par un
      saut de ligne, pour que les ajouts du soir partent sur une ligne neuve.
    ② CONTEXTE D'APPEL — `executer`, deux fois par passage (fichier quotidien, fichier de la
      météo) ; `cas`, pour préparer un fichier quotidien d'épreuve.
    ③ ENTRÉE — `chemin` : le fichier CSV · `entete` : la liste des noms de colonnes à écrire s'il
      faut le créer (ENTETE_QUOTIDIEN ou ENTETE_METEO).
    ④ CONDITIONS D'ENTRÉE — Le dossier parent peut manquer (il est créé). Un fichier existant doit
      pouvoir s'ouvrir en lecture et en ajout.
    ⑤ SORTIE — Ne rend rien.
      [rend: rien]
    ⑥ TRAITEMENT — ① fichier absent ou vide : créer son dossier, écrire l'en-tête seul, s'arrêter
      · ② sinon lire son dernier octet · ③ si ce n'est pas un saut de ligne, en ajouter un.
    ⑦ UNITÉ — Octets (le dernier caractère du fichier).
    ⑧ POURQUOI — Le circuit du soir enregistre ces deux fichiers au dépôt chaque soir (git add dans
      .github/workflows/collecte_abc.yml, qui échoue si un fichier manque). Un fichier retouché à
      la main sans saut de ligne final collerait la ligne suivante à la dernière.
    ⑨ CE QUI CLOCHE — L'en-tête d'un fichier qui existe déjà n'est pas comparé à `entete` : un
      fichier aux colonnes différentes passe ici, et la lecture échoue plus loin.
    ⑩ EFFET — Crée le dossier et le fichier s'ils manquent ; ajoute au plus un saut de ligne en fin
      de fichier. Ne retire jamais rien.
    ⑪ TERMINAISON — Rend la main, ou LÈVE sur une erreur du disque. Aucun appel ne peut ne pas
      revenir.
      [sort: non]
    ⑫ DÉFINITIONS
      le circuit du soir : le passage automatique de chaque soir sur une machine GitHub,
        .github/workflows/collecte_abc.yml, réveillé depuis le dépôt public (18h07, secours 21h23,
        rattrapage 7h41 le lendemain matin, d'après l'en-tête de collecte_abc.yml)
      le fichier quotidien : donnees/indice_cac40_quotidien.csv (colonnes date, close, source),
        les clôtures lues chez ABC après la fin de l'historique figé
    """
    if not os.path.exists(chemin) or os.path.getsize(chemin) == 0:
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        with open(chemin, 'w', encoding='utf-8', newline='') as f: csv.writer(f).writerow(entete)
        return
    with open(chemin, 'rb') as f:
        f.seek(-1, 2); dernier = f.read(1)
    if dernier != b'\n':
        with open(chemin, 'a', encoding='utf-8') as f: f.write('\n')


def lire_serie(chemin, colonne):
    """lit {date: clôture} ; une ligne illisible LÈVE (rattrapé par `executer`, écrit au rapport).

    ① RÔLE — Charger une série de clôtures du CAC 40 depuis un CSV, en refusant une date ou un
      nombre illisible plutôt que de le sauter.
    ② CONTEXTE D'APPEL — `executer` (historique figé, colonne yahoo ; fichier quotidien, colonne
      close) ; `epreuves` (historique figé) ; `cas` (fichier quotidien, et fichier de la météo,
      colonne cloture, pour compter ses lignes).
    ③ ENTRÉE — `chemin` : le fichier CSV, qui porte une colonne date · `colonne` : le nom de la
      colonne de clôture à lire.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe et porte une colonne date (sinon KeyError).
    ⑤ SORTIE — UNE valeur : un dictionnaire {date telle qu'écrite dans le fichier : clôture en
      nombre}.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque ligne : ① la sauter si la colonne est absente ou vide · ② vérifier
      que la date se lit (date.fromisoformat) · ③ convertir la clôture en nombre.
    ⑦ UNITÉ — Points d'indice.
    ⑧ POURQUOI — Une ligne fausse sautée en silence ferait un trou que seule la continuité verrait,
      sans dire pourquoi ; une erreur levée s'écrit au rapport avec la ligne en cause (cas E10).
    ⑨ CE QUI CLOCHE — ① La clé gardée est le texte brut de la date, pas la date relue : depuis
      Python 3.11, date.fromisoformat accepte aussi « 20261030 » et « 2026-W44-5 » (essayé le
      31-10-2026 sous Python 3.13), gardés tels quels et mal triés parmi les AAAA-MM-JJ
      (THÉORIQUE : aucune ligne de ce genre au 31-10-2026). ② Une date écrite deux fois : la
      dernière gagne sans rien dire. ③ « nan » et « inf » passent float() sans lever. ④ Une
      ligne dont la colonne est vide est sautée : dans l'historique figé, six séances n'ont que
      la source bnains (2010-12-24, 2010-12-31, 2012-01-02, 2012-12-24, 2012-12-31, 2015-12-31)
      et manquent donc à la série (déjà au ⑨ du programme).
    ⑩ EFFET — Lit un fichier ; n'écrit rien.
    ⑪ TERMINAISON — Rend la main, ou LÈVE (ValueError, KeyError, OSError). Aucun appel ne peut ne
      pas revenir.
      [sort: non]
    ⑫ DÉFINITIONS
      l'historique figé : donnees/sources_indice/INDICE_CAC40.csv, clôtures du CAC 40 depuis le
        03-01-2000 (colonnes date, bnains, yahoo ; seule yahoo est lue), jamais écrit par ce programme
      le fichier quotidien : donnees/indice_cac40_quotidien.csv (colonnes date, close, source),
        les clôtures lues chez ABC après la fin de l'historique figé
      bnains : l'une des deux sources de l'historique figé, l'autre étant yahoo
    """
    serie = {}
    with open(chemin, encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            if r.get(colonne) in (None, ''): continue
            date.fromisoformat(r['date'])
            serie[r['date']] = float(r[colonne])
    return serie


def lire_decisions(chemin):
    """{date: clôture retenue, ou None pour garder la valeur d'ABC} — décisions de Jean-Luc.

    ① RÔLE — Lire les arbitrages de Jean-Luc sur les séances que la météo a refusé d'écrire seule
      (page qui contredit, variation trop forte, page invérifiable).
    ② CONTEXTE D'APPEL — `executer`, une fois par passage.
    ③ ENTRÉE — `chemin` : donnees/meteo_decisions.csv sous la racine (colonnes date, close, motif).
    ④ CONDITIONS D'ENTRÉE — Aucune : un fichier absent vaut « aucune décision ». S'il existe, il
      porte une colonne date et une colonne close.
    ⑤ SORTIE — UNE valeur : un dictionnaire {date : clôture retenue en nombre, ou None quand close
      est vide}.
      [rend: 1]
    ⑥ TRAITEMENT — ① fichier absent : rendre un dictionnaire vide · ② sinon, pour chaque ligne,
      vérifier que la date se lit, puis retenir close en nombre, ou None si close est vide.
    ⑦ UNITÉ — Points d'indice.
    ⑧ POURQUOI — L'issue d'un blocage appartient à Jean-Luc, comme pour les cours des actions
      (A-231 : une séance révisée est signalée, jamais écrasée) ; le programme ne tranche pas seul.
    ⑨ CE QUI CLOCHE — ① La colonne motif n'est pas lue : une décision sans motif passe. ② Rien ne
      vérifie que la date est un jour de bourse ni que la clôture retenue est plausible : une faute
      de frappe passerait sans alerte (BACKLOG A-634). ③ Une date écrite deux fois : la dernière
      gagne sans rien dire. ④ La clé est le texte brut de la date (voir le ⑨ de `lire_serie`). ⑤ Au
      31-10-2026 le fichier n'existe pas dans la copie du dépôt : ce code n'a tourné que dans les
      épreuves. ⑥ Une colonne close absente ou mal nommée ne lève pas : chaque décision vaut alors
      « garder la valeur d'ABC » (essayé le 31-10-2026).
    ⑩ EFFET — Lit un fichier s'il existe ; n'écrit rien.
    ⑪ TERMINAISON — Rend la main, ou LÈVE ValueError, ou KeyError si la colonne date manque. Aucun appel ne peut ne pas
      revenir.
      [sort: non]
    ⑫ DÉFINITIONS
      une décision de Jean-Luc : une ligne de donnees/meteo_decisions.csv (date, close, motif) ;
        close fixe la clôture retenue pour la séance, close vide accepte la valeur d'ABC
      ABC : ABC Bourse, le site d'où le projet lit les cours ; PX1p y est le code du CAC 40
    """
    dec = {}
    if os.path.exists(chemin):
        with open(chemin, encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                date.fromisoformat(r['date'])
                dec[r['date']] = float(r['close']) if r.get('close') else None
    return dec


def derniere_seance_close(maintenant, ABC, K, cal):
    """la dernière séance de bourse close à l'heure donnée (aujourd'hui après la clôture, sinon avant).

    ① RÔLE — Dire jusqu'à quelle séance la série DOIT aller à cette heure : c'est la borne que
      `continuite` impose, pour refuser une série en retard.
    ② CONTEXTE D'APPEL — `executer`, une fois par passage.
    ③ ENTRÉE — `maintenant` : l'heure du passage, en heure de Paris (l'horloge réelle au passage,
      une heure fixée dans les épreuves) · `ABC` : le module COLLECTER_ABC_GITHUB, dont seule
      HEURE_CLOTURE_PARIS (18) est lue · `K` : le module CALENDRIER_DE_LA_BOURSE · `cal` : le
      calendrier rendu par K.lire.
    ④ CONDITIONS D'ENTRÉE — L'heure est celle de Paris (rien ne le vérifie). Le jour et les jours
      parcourus en reculant sont couverts par le calendrier (l'année 2026 seulement, relevé le
      31-10-2026).
    ⑤ SORTIE — UNE valeur : une date. Exemple : le passage réel du vendredi 30-10-2026 à 21h41
      attend la séance du 30-10-2026 ; un passage le samedi 31-10-2026 à 21h41 attendrait
      encore le 30-10-2026.
      [rend: 1]
    ⑥ TRAITEMENT — ① partir du jour de l'heure donnée · ② avant 18 h, ou si ce n'est pas un jour de
      bourse : reculer d'un jour, puis encore tant que ce n'est pas un jour de bourse.
    ⑦ UNITÉ — Une date ; l'heure en heures de Paris.
    ⑧ POURQUOI — Avant 18 h la ligne du jour chez ABC est partielle (commentaire de
      HEURE_CLOTURE_PARIS) : la séance du jour n'est pas encore due.
    ⑨ CE QUI CLOCHE — ① Refait le recul que CALENDRIER_DE_LA_BOURSE.dernier_jour_de_bourse fait
      déjà : deux écritures d'un même calcul (R-708). ② Une heure donnée dans un autre fuseau
      déplacerait le seuil de 18 h sans rien dire. ③ Dès qu'un passage tombe en 2027 (après 18 h
      le 01-01, ou à toute heure à partir du 02-01), est_jour_de_bourse lève HorsCalendrier,
      rattrapé par `executer` en code 2 (déjà au ⑨ du programme).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main, ou LÈVE HorsCalendrier. La boucle de recul s'arrête au premier
      jour de bourse ou lève en sortant du calendrier : elle revient toujours.
      [sort: non]
    ⑫ DÉFINITIONS
      ABC : ABC Bourse, le site d'où le projet lit les cours ; PX1p y est le code du CAC 40
    """
    d = maintenant.date()
    if maintenant.hour < ABC.HEURE_CLOTURE_PARIS or not K.est_jour_de_bourse(d, cal):
        d -= timedelta(days=1)
        while not K.est_jour_de_bourse(d, cal): d -= timedelta(days=1)
    return d


def lire_page(ABC, maintenant, notes):
    """lit la page ABC de l'indice ; rend les séances closes [(date, clôture)], de la plus ancienne à la plus récente.

    ① RÔLE — Aller chercher chez ABC les dernières clôtures du CAC 40 : la seule donnée neuve de la
      météo chaque soir.
    ② CONTEXTE D'APPEL — `executer`, une fois par passage, seulement quand la collecte est
      demandée (pas en mode sans_collecte).
    ③ ENTRÉE — `ABC` : le module COLLECTER_ABC_GITHUB, dont sont appelés le téléchargement et
      l'extraction · `maintenant` : l'heure du passage, Paris · `notes` : la liste des contrôles
      du rapport, complétée ici.
    ④ CONDITIONS D'ENTRÉE — Aucune exigée : réseau fermé ou page illisible deviennent une note ❌.
    ⑤ SORTIE — UNE valeur : une liste de couples (date AAAA-MM-JJ, clôture en nombre), de la plus
      ancienne à la plus récente ; vide en cas d'échec. Exemple réel, passage du 30-10-2026 à
      21h41 (rapports/meteo_du_marche.md) : 30 séances, du 2026-09-21 au 2026-10-30.
      [rend: 1]
    ⑥ TRAITEMENT — ① télécharger https://www.abcbourse.com/cotation/PX1p et en extraire les
      séances ; une erreur de l'un ou de l'autre devient une note ❌ · ② aucune séance : note ❌ · ③ avant
      18 h, retirer la séance du jour, encore partielle · ④ garder les séances qui ont une clôture,
      triées · ⑤ aucune : note ❌ ; sinon noter le nombre de séances et leurs dates extrêmes.
    ⑦ UNITÉ — Points d'indice ; l'heure en heures de Paris.
    ⑧ POURQUOI — Une page non lue ne doit ni arrêter le passage ni passer pour « rien de neuf » :
      elle s'écrit en ❌ au rapport et le code de sortie devient 2 (un contrôle qui n'a pas pu
      tourner le dit et rend un code non nul, R-734 et R-734bis).
    ⑨ CE QUI CLOCHE — ① Une séance dont la clôture vaudrait 0 serait écartée comme sans clôture
      (test de vérité sur close). ② L'extraction d'ABC ignore sans le compter une ligne dont une
      case est illisible (son propre ⑨) : une séance peut manquer sans note ici, et c'est
      `continuite` qui la verra manquer. ③ Le délai de 30 secondes du téléchargement porte sur
      chaque attente du réseau, pas sur la page entière : un serveur qui répond goutte à goutte
      pourrait le dépasser (THÉORIQUE).
    ⑩ EFFET — SORT SUR LE RÉSEAU (une page) ; ajoute exactement une note à `notes`.
    ⑪ TERMINAISON — Rend la main : toute erreur du téléchargement ou de l'extraction est rattrapée.
      L'appel réseau est borné par le délai de 30 secondes du téléchargement (voir ⑨).
      [sort: non]
    ⑫ DÉFINITIONS
      ABC : ABC Bourse, le site d'où le projet lit les cours ; PX1p y est le code du CAC 40
    """
    try:
        seances, note = ABC.extraire(ABC.telecharger(f'https://www.abcbourse.com/cotation/{CODE_ABC}'))
    except Exception as e:
        notes.append(f'❌ page {CODE_ABC} non lue : {e}'); return []
    if not seances:
        notes.append(f'❌ page {CODE_ABC} lue mais aucune séance extraite : {note}'); return []
    if maintenant.hour < ABC.HEURE_CLOTURE_PARIS:
        seances = [s for s in seances if s['date'] != maintenant.date().isoformat()]   # la séance du jour n'est pas close
    page = sorted((s['date'], float(s['close'])) for s in seances if s.get('close'))
    if not page: notes.append(f'❌ page {CODE_ABC} sans clôture'); return []
    notes.append(f'page {CODE_ABC} lue : {len(page)} séances, du {page[0][0]} au {page[-1][0]}')
    return page


ISSUE = ('issue : décision de Jean-Luc — inscrire la séance dans donnees/meteo_decisions.csv (colonnes date, close, motif ; '
         'close = la clôture retenue ; vide = séance nouvelle acceptée telle qu ABC la donne, ou séance connue qui n est plus contrôlée)')


def confronter(page, connu, decisions, notes):
    """rend les séances de la page à AJOUTER au fichier quotidien ; un seul désaccord et rien n'est rendu.

    ① RÔLE — Ne laisser entrer dans la série que des clôtures d'ABC vérifiées contre ce qui est déjà
      connu : c'est la garde de la météo contre une page fausse.
    ② CONTEXTE D'APPEL — `executer`, une fois par passage avec collecte, sur ce que `lire_page` a
      rendu.
    ③ ENTRÉE — `page` : les couples (date, clôture) de la page, du plus ancien au plus récent ·
      `connu` : {date : clôture} de l'historique figé et du fichier quotidien, avec les valeurs des
      décisions qui portent sur une date déjà connue · `decisions` : les décisions de Jean-Luc,
      rendues par `lire_decisions` · `notes` : la liste des contrôles du rapport, complétée ici.
    ④ CONDITIONS D'ENTRÉE — La page est triée du plus ancien au plus récent (l'ordre des ajouts en
      dépend) ; aucune clôture connue ne vaut 0.
    ⑤ SORTIE — UNE valeur : la liste des couples (date, clôture) à ajouter, dans l'ordre ; vide si
      la page est vide, contredit le connu ou ne recouvre rien de connu. Exemple réel, passage du
      30-10-2026 à 21h41 : 29 séances communes vérifiées, 1 ajoutée (le 2026-10-30, 7969.42) ; à ce
      niveau la tolérance de 0,1 % vaut 7969.42 × 0,001 = 7,97 points.
      [rend: 1]
    ⑥ TRAITEMENT — ① page vide : rendre une liste vide sans note (`lire_page` a déjà noté)
      · ② retenir les séances communes à la page et au connu, hors décisions · ③ si l'une diffère
      de plus de 0,1 % : note ❌, liste vide · ④ aucune séance commune : note ❌, liste vide
      · ⑤ pour chaque séance neuve, dans l'ordre : avec décision, prendre la valeur décidée, ou
      celle d'ABC si la décision est vide ; sans décision, la comparer à la dernière clôture connue
      avant elle et, au-delà de 15 %, noter ❌ et ne garder ni elle ni les suivantes · ⑥ noter le
      nombre de séances vérifiées et ajoutées.
    ⑦ UNITÉ — Points d'indice ; écarts et variations en fraction (0,001 = 0,1 % ; 0,15 = 15 %).
    ⑧ POURQUOI — Relecture du 29-10-2026, tour 2 : vérifier seulement contre l'historique figé
      laissait passer une page fausse dès qu'elle ne le recouvrait plus ; d'où la confrontation au
      fichier quotidien aussi, et « un seul désaccord, rien n'est écrit ». Relecture du tour 3
      (A1) : une décision ne remplace jamais la vérification, d'où au moins une séance commune
      hors décisions. Seuil de 15 % : la plus forte variation d'une séance depuis 2000 est −12,28 %
      (12-03-2020, mesuré le 29-10-2026, commentaire de VARIATION_MAX). Seuil de 0,1 % : deux
      sources de la même clôture (commentaire d'ECART_SOURCES).
    ⑨ CE QUI CLOCHE — ① Une séance de la page absente du connu mais ANTÉRIEURE à la fin de
      l'historique figé (un trou de l'historique) serait ajoutée au fichier quotidien, puis ignorée
      par `executer`, qui ne garde que les dates postérieures (THÉORIQUE). ② Une clôture connue à 0
      ferait lever une division par zéro, rattrapée par `executer` (THÉORIQUE). ③ La variation se
      mesure contre la dernière clôture connue même si des séances manquent entre les deux ; c'est
      `continuite` qui verra le trou. ④ Une valeur décidée ne passe aucun contrôle de
      vraisemblance (voir le ⑨ de `lire_decisions`).
    ⑩ EFFET — Ajoute une ou deux notes à `notes` (aucune si la page est vide) ; ne modifie ni
      `connu` (travaille sur une copie) ni aucun fichier.
    ⑪ TERMINAISON — Rend la main, ou LÈVE sur une clôture connue nulle (voir ⑨). Aucun appel ne
      peut ne pas revenir.
      [sort: non]
    ⑫ DÉFINITIONS
      l'historique figé : donnees/sources_indice/INDICE_CAC40.csv, clôtures du CAC 40 depuis le
        03-01-2000 (colonnes date, bnains, yahoo ; seule yahoo est lue), jamais écrit par ce programme
      le fichier quotidien : donnees/indice_cac40_quotidien.csv (colonnes date, close, source),
        les clôtures lues chez ABC après la fin de l'historique figé
      une décision de Jean-Luc : une ligne de donnees/meteo_decisions.csv (date, close, motif) ;
        close fixe la clôture retenue pour la séance, close vide accepte la valeur d'ABC
      ABC : ABC Bourse, le site d'où le projet lit les cours ; PX1p y est le code du CAC 40
    """
    if not page: return []
    communes = [(d, x) for d, x in page if d in connu and d not in decisions]
    faux = [(d, connu[d], x) for d, x in communes if abs(x / connu[d] - 1) > ECART_SOURCES]
    if faux:
        notes.append('❌ LA PAGE CONTREDIT DES CLÔTURES DÉJÀ CONNUES — rien n est écrit ce soir : ' +
                     ' · '.join(f'{d} connue {a} contre ABC {b}' for d, a, b in faux[:5]) + f' ({len(faux)} séance(s)) — ' + ISSUE)
        return []
    if not communes:                     # une décision ne remplace jamais la vérification (relecture tour 3, A1)
        notes.append('❌ AUCUNE SÉANCE COMMUNE entre la page et ce qu on connaît : la page ne peut pas être vérifiée — rien n est écrit — ' + ISSUE)
        return []
    connu = dict(connu); ajout = []
    for d, x in page:
        if d in connu: continue
        if d in decisions:
            x = decisions[d] if decisions[d] is not None else x
        else:
            prec = [k for k in connu if k < d]
            v = x / connu[max(prec)] - 1 if prec else 0.0
            if abs(v) > VARIATION_MAX:
                notes.append(f'❌ VARIATION DE {v:+.2%} le {d} (au-delà de {VARIATION_MAX:.0%}) — cette séance et les suivantes ne sont pas écrites — ' + ISSUE)
                break
        ajout.append((d, x)); connu[d] = x
    notes.append(f'{len(communes)} séance(s) commune(s) vérifiée(s), {len(ajout)} ajoutée(s)')
    return ajout


def voyant(serie):
    """voyant de la dernière séance, en UN passage sur toute la série ; None si moins de 252 séances.

    ① RÔLE — Calculer le voyant de la météo : la couleur, depuis combien de séances, l'écart à la
      moyenne des 200 séances et la distance au plus haut d'un an.
    ② CONTEXTE D'APPEL — `executer`, une fois par passage, seulement si la série est sûre
      (`continuite` vraie) ; `epreuves`, cinq fois (cas E1), sur l'historique figé coupé à une date.
    ③ ENTRÉE — `serie` : {date AAAA-MM-JJ : clôture}, l'historique figé prolongé du fichier
      quotidien après sa fin.
    ④ CONDITIONS D'ENTRÉE — Les dates s'écrivent AAAA-MM-JJ (leur tri en texte est alors leur ordre
      dans le temps) ; la série est sans trou (vérifié avant par `continuite`, pas ici).
    ⑤ SORTIE — UNE valeur : None si moins de 252 séances ; sinon un dictionnaire de neuf clés :
      date, cloture, moyenne_200, ecart, couleur (🟢 ou 🔴), depuis, plus_haut_an, sous_plus_haut,
      krach (vrai ou faux). Exemple calculé à la main le 31-10-2026 sur les vraies données (les
      clôtures relues par awk, hors de ce programme) : séance du 2026-10-30, clôture 7969.42 ;
      somme des 200 dernières 1 640 672.54, moyenne 8203.36 ; écart 7969.42 / 8203.36 − 1 =
      −0,0285 ; plus haut des 252 dernières 8726.03 (le 2026-08-10) ; 7969.42 / 8726.03 − 1 =
      −0,0867, donc pas de krach. Le passage réel du 30-10-2026 a écrit les mêmes chiffres, 🔴
      depuis 38 séances (donnees/meteo_du_marche.csv).
      [rend: 1]
    ⑥ TRAITEMENT — ① trier les dates · ② moins de 252 séances : rendre None · ③ en un seul
      passage, tenir la somme glissante des 200 dernières clôtures et noter, à partir de la 200e
      séance, si la clôture est STRICTEMENT au-dessus de la moyenne · ④ compter, en remontant
      depuis la dernière séance, les séances consécutives du même côté, la dernière comprise
      · ⑤ prendre le plus haut des 252 dernières clôtures · ⑥ assembler le résultat ; krach si la
      clôture est à 20 % ou plus sous ce plus haut.
    ⑦ UNITÉ — Points d'indice ; ecart et sous_plus_haut en fraction (−0,0285 = −2,85 %) ; depuis
      en séances.
    ⑧ POURQUOI — Moyenne des 200 séances : Faber (2007), demandée par Jean-Luc le 28-10-2026 ;
      seuil de krach de 20 % : décision de Jean-Luc du 28-10-2026 à 19h08 (commentaires des
      constantes). Le compte « depuis » exige de savoir de quel côté était CHAQUE séance : la somme
      glissante le donne en un seul passage.
    ⑨ CE QUI CLOCHE — ① Une clôture exactement égale à la moyenne compte comme EN DESSOUS (🔴). ② La
      somme glissante accumule les arrondis sur toute la série (6 858 séances au 30-10-2026,
      comptées par awk) : l'écart n'est pas mesuré ici, les cas E1 le bornent à 0,01 point sur
      quatre dates. ③ Le plus haut d'un an est pris sur les CLÔTURES, pas sur les plus hauts de
      séance, que la série ne porte pas ; le rapport dit seulement « plus haut d un an ». ④ La
      moyenne des 200 séances est aussi calculée dans l'étude du 28-10-2026 : deux écritures d'un
      même calcul (déjà au ⑨ du programme).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. Aucun appel ne peut ne pas revenir.
      [sort: non]
    ⑫ DÉFINITIONS
      le voyant : 🟢 si la clôture du CAC 40 est au-dessus de la moyenne de ses 200 dernières
        clôtures, 🔴 sinon ; un signal de prudence, pas un ordre
      l'historique figé : donnees/sources_indice/INDICE_CAC40.csv, clôtures du CAC 40 depuis le
        03-01-2000 (colonnes date, bnains, yahoo ; seule yahoo est lue), jamais écrit par ce programme
      le fichier quotidien : donnees/indice_cac40_quotidien.csv (colonnes date, close, source),
        les clôtures lues chez ABC après la fin de l'historique figé
    """
    dates = sorted(serie)
    if len(dates) < SEANCES_PLUS_HAUT: return None
    c = [serie[d] for d in dates]
    somme, dessus = 0.0, []
    for k, x in enumerate(c):
        somme += x
        if k >= SEANCES_MOYENNE: somme -= c[k - SEANCES_MOYENNE]
        dessus.append(x > somme / SEANCES_MOYENNE if k >= SEANCES_MOYENNE - 1 else None)
    mm = somme / SEANCES_MOYENNE
    depuis = 0
    for x in reversed(dessus):
        if x is None or x != dessus[-1]: break
        depuis += 1
    haut = max(c[-SEANCES_PLUS_HAUT:])
    return {'date': dates[-1], 'cloture': c[-1], 'moyenne_200': mm, 'ecart': c[-1] / mm - 1, 'couleur': '🟢' if dessus[-1] else '🔴',
            'depuis': depuis, 'plus_haut_an': haut, 'sous_plus_haut': c[-1] / haut - 1, 'krach': c[-1] / haut - 1 <= SEUIL_KRACH}


def continuite(fin_histo, dates_apres, fin_attendue, K, cal, notes):
    """vrai si les dates connues après l'historique sont EXACTEMENT les jours de bourse jusqu'à `fin_attendue`.

    ① RÔLE — Interdire un voyant calculé sur une série trouée, gonflée d'un faux jour ou en retard :
      sans ce contrôle, une moyenne fausse s'afficherait en couleur sans rien dire.
    ② CONTEXTE D'APPEL — `executer`, une fois par passage, avant `voyant`.
    ③ ENTRÉE — `fin_histo` : la dernière date de l'historique figé, AAAA-MM-JJ (le 2026-10-02,
      relevé le 31-10-2026) · `dates_apres` : les dates connues après elle ; l'appelant passe un
      dictionnaire, dont seules les clés comptent · `fin_attendue` : la dernière séance close,
      rendue par `derniere_seance_close` · `K` : le module CALENDRIER_DE_LA_BOURSE · `cal` : le
      calendrier rendu par K.lire · `notes` : la liste des contrôles du rapport, complétée ici.
    ④ CONDITIONS D'ENTRÉE — Tous les jours du lendemain de la fin de l'historique à la séance
      attendue sont couverts par le calendrier (l'année 2026 seulement, relevé le 31-10-2026),
      sinon HorsCalendrier est levée.
    ⑤ SORTIE — UNE valeur : vrai si rien ne manque et rien n'est en trop, faux sinon. Exemple
      réel, passage du 30-10-2026 : du 2026-10-05 au 2026-10-30, 20 jours de bourse attendus,
      les mêmes 20 dates au fichier quotidien : vrai.
      [rend: 1]
    ⑥ TRAITEMENT — ① énumérer les jours de bourse du lendemain de la fin de l'historique jusqu'à
      la séance attendue incluse · ② comparer à l'ensemble des dates connues · ③ noter ❌ les
      séances manquantes et les séances en trop, huit au plus nommées de chaque · ④ rendre vrai si
      les deux listes sont vides.
    ⑦ UNITÉ — Des dates ; des jours de bourse.
    ⑧ POURQUOI — Comparer DATE PAR DATE et non des comptes : un samedi en trop et un jour manquant
      font le même nombre de lignes (cas E7 des épreuves). Une séance manquante fausse la moyenne
      sans que rien ne se voie.
    ⑨ CE QUI CLOCHE — ① Seul l'après-historique est vérifié : l'historique figé lui-même n'est pas
      confronté au calendrier, qui ne couvre que 2026. ② À partir de 2027, HorsCalendrier
      (déjà au ⑨ du programme).
    ⑩ EFFET — Ajoute zéro, une ou deux notes à `notes`.
    ⑪ TERMINAISON — Rend la main, ou LÈVE HorsCalendrier. La boucle avance d'un jour par tour
      jusqu'à la séance attendue : elle se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      l'historique figé : donnees/sources_indice/INDICE_CAC40.csv, clôtures du CAC 40 depuis le
        03-01-2000 (colonnes date, bnains, yahoo ; seule yahoo est lue), jamais écrit par ce programme
      le fichier quotidien : donnees/indice_cac40_quotidien.csv (colonnes date, close, source),
        les clôtures lues chez ABC après la fin de l'historique figé
      le voyant : 🟢 si la clôture du CAC 40 est au-dessus de la moyenne de ses 200 dernières
        clôtures, 🔴 sinon ; un signal de prudence, pas un ordre
    """
    attendues, d = set(), date.fromisoformat(fin_histo)
    while d < fin_attendue:
        d += timedelta(days=1)
        if K.est_jour_de_bourse(d, cal): attendues.add(d.isoformat())
    connues = set(dates_apres)
    manquent = sorted(attendues - connues); en_trop = sorted(connues - attendues)
    if manquent: notes.append(f'❌ SÉANCES MANQUANTES ({len(manquent)}) : {", ".join(manquent[:8])}{" …" if len(manquent) > 8 else ""} — voyant non calculable')
    if en_trop: notes.append(f'❌ SÉANCES EN TROP, absentes du calendrier d Euronext : {", ".join(en_trop[:8])} — voyant non calculable')
    return not manquent and not en_trop


def executer(racine, collecte, maintenant):
    """tout le passage, à l'heure `maintenant` (Paris) ; rend le code de sortie.

    ① RÔLE — Faire le passage entier de la météo et TOUJOURS laisser un rapport, que tout aille
      bien ou non.
    ② CONTEXTE D'APPEL — `main`, une fois, à l'heure réelle de Paris ; `cas`, une fois par cas des
      épreuves, sur un dossier temporaire et à une heure fixée.
    ③ ENTRÉE — `racine` : la racine du dépôt ou de sa copie · `collecte` : vrai pour lire la page
      d'ABC, faux en mode sans_collecte · `maintenant` : l'heure du passage, Paris.
    ④ CONDITIONS D'ENTRÉE — Sous la racine : l'historique figé, donnees/CALENDRIER_EURONEXT.csv et
      programmes/ avec COLLECTER_ABC_GITHUB et CALENDRIER_DE_LA_BOURSE. Leur absence ne lève pas :
      elle s'écrit au rapport en ❌.
    ⑤ SORTIE — UNE valeur : le code de sortie, 0 si aucune note ne commence par ❌, 2 sinon.
      Exemple réel : le passage du 30-10-2026 à 21h41 n'a écrit aucune note ❌
      (rapports/meteo_du_marche.md), donc 0.
      [rend: 1]
    ⑥ TRAITEMENT — ① créer au besoin le fichier quotidien et celui de la météo · ② importer les
      modules ; lire le calendrier, l'historique figé, le fichier quotidien et les décisions
      · ③ composer le connu : historique, quotidien, et valeurs décidées sur une date connue
      · ④ avec collecte : lire la page, la confronter, ajouter les séances retenues au fichier
      quotidien (source abc) · ⑤ appliquer les valeurs décidées aux dates du quotidien, garder les
      dates postérieures à l'historique et prolonger l'historique avec elles · ⑥ vérifier la
      continuité jusqu'à la dernière séance close ; si elle tient, calculer et écrire le voyant
      au rapport, et une ligne au fichier de la météo si sa date n'y est pas encore · ⑦ toute
      erreur imprévue devient une note ❌ avec sa trace · ⑧ écrire le rapport, l'afficher, rendre
      le code.
    ⑦ UNITÉ — Points d'indice ; écarts en fraction ; code de sortie 0 ou 2.
    ⑧ POURQUOI — Un voyant ne doit ni s'afficher sur une série douteuse ni se taire quand il n'a pas
      pu être calculé : un contrôle qui n'a pas pu tourner le dit et rend un code non nul (R-734 et
      R-734bis). Le circuit du soir lance cette étape avec continue-on-error : son échec s'affiche
      sans arrêter la collecte.
    ⑨ CE QUI CLOCHE — ① L'écriture du rapport est HORS du bloc qui rattrape les erreurs : si elle
      échoue (dossier non inscriptible), le programme s'arrête sur une trace Python, code 1 et non
      2, sans rapport (THÉORIQUE) ; le ⑪ du programme dit pourtant « toute erreur est
      rattrapée ». ② Une ligne de la météo déjà écrite pour une date n'est jamais réécrite : si une décision de
      Jean-Luc change ensuite une clôture, la ligne ancienne reste. ③ Une décision non vide sur une
      séance NEUVE est écrite au fichier quotidien avec la source « abc » : `confronter` rend la
      valeur décidée, et elle est ajoutée telle quelle. La source est alors fausse, et la valeur
      reste même si la décision est retirée (cas du relecteur du 31-10-2026 : 1234.56 écrit « abc »,
      relu après retrait). Une décision sur une séance DÉJÀ au quotidien n'est appliquée qu'à la
      lecture : si elle disparaît du fichier des décisions, la valeur d'ABC revient sans rien dire. ④ Les
      séances retenues sont écrites au fichier quotidien AVANT le contrôle de continuité : un soir
      refusé pour un trou garde ses ajouts.
    ⑩ EFFET — Crée au besoin donnees/indice_cac40_quotidien.csv et donnees/meteo_du_marche.csv ;
      AJOUTE au premier les séances retenues (la valeur d'ABC, ou la valeur décidée pour une séance
      neuve, toujours avec la source abc), au second une ligne par date de voyant nouvelle ;
      ÉCRASE rapports/meteo_du_marche.md ; affiche le rapport ; avec collecte, sort sur le réseau
      (une page) ; allonge sys.path (voir `modules`).
    ⑪ TERMINAISON — Rend la main avec 0 ou 2 ; LÈVE seulement si l'écriture ou l'affichage du
      rapport échoue (voir ⑨). L'appel réseau est borné par le délai de 30 secondes du téléchargement (voir le ⑨
      de `lire_page`).
      [sort: non]
    ⑫ DÉFINITIONS
      le circuit du soir : le passage automatique de chaque soir sur une machine GitHub,
        .github/workflows/collecte_abc.yml, réveillé depuis le dépôt public (18h07, secours 21h23,
        rattrapage 7h41 le lendemain matin, d'après l'en-tête de collecte_abc.yml)
      ABC : ABC Bourse, le site d'où le projet lit les cours ; PX1p y est le code du CAC 40
      l'historique figé : donnees/sources_indice/INDICE_CAC40.csv, clôtures du CAC 40 depuis le
        03-01-2000 (colonnes date, bnains, yahoo ; seule yahoo est lue), jamais écrit par ce programme
      le fichier quotidien : donnees/indice_cac40_quotidien.csv (colonnes date, close, source),
        les clôtures lues chez ABC après la fin de l'historique figé
      une décision de Jean-Luc : une ligne de donnees/meteo_decisions.csv (date, close, motif) ;
        close fixe la clôture retenue pour la séance, close vide accepte la valeur d'ABC
      le voyant : 🟢 si la clôture du CAC 40 est au-dessus de la moyenne de ses 200 dernières
        clôtures, 🔴 sinon ; un signal de prudence, pas un ordre
    """
    P = chemins(racine); notes = []
    lignes = [f'# MÉTÉO DU MARCHÉ — {maintenant.strftime("%d-%m-%Y %Hh%M")} (Paris)', '', 'Voyant de prudence, pas un ordre. Simulation uniquement.', '']
    try:
        creer_si_absent(P['quotidien'], ENTETE_QUOTIDIEN); creer_si_absent(P['meteo'], ENTETE_METEO)
        ABC, K = modules(racine); cal = K.lire(racine)
        histo = lire_serie(P['historique'], 'yahoo'); quot = lire_serie(P['quotidien'], 'close')
        decisions = lire_decisions(P['decisions'])
        fin_h = max(histo)
        connu = dict(histo); connu.update(quot); connu.update({d: x for d, x in decisions.items() if x is not None and d in connu})
        if collecte:
            ajout = confronter(lire_page(ABC, maintenant, notes), connu, decisions, notes)
            if ajout:
                with open(P['quotidien'], 'a', encoding='utf-8', newline='') as f:
                    w = csv.writer(f)
                    for d, x in ajout: w.writerow([d, x, 'abc']); quot[d] = x
        quot.update({d: x for d, x in decisions.items() if x is not None and d in quot})
        apres = {d: x for d, x in quot.items() if d > fin_h}
        serie = dict(histo); serie.update(apres)
        sure = continuite(fin_h, apres, derniere_seance_close(maintenant, ABC, K, cal), K, cal, notes)
        v = voyant(serie) if sure else None
        if not sure:
            lignes.append('❌ **Voyant non calculable ce soir : la série des cours n est pas complète (voir les contrôles).**')
        elif v is None:
            notes.append('❌ moins de 252 séances')
        else:
            lignes += [f'**{v["couleur"]} CAC 40 {"AU-DESSUS" if v["couleur"] == "🟢" else "EN DESSOUS"} de sa moyenne des 200 séances**, depuis {v["depuis"]} séance(s).', '',
                       f'- Séance du {v["date"]} : clôture {v["cloture"]:.2f} · moyenne 200 séances {v["moyenne_200"]:.2f} · écart {v["ecart"]:+.2%}',
                       f'- Plus haut d un an : {v["plus_haut_an"]:.2f} · le CAC est à {v["sous_plus_haut"]:+.2%} de ce plus haut'
                       + (' · 🚨 ZONE DE KRACH (20 % ou plus sous le plus haut)' if v['krach'] else ''), '',
                       'Ce que dit l étude (29-10-2026) : sous la moyenne, la pire baisse a été réduite en 2008 et 2020, '
                       'mais le voyant change souvent de couleur hors krach et n est pas prouvé statistiquement.']
            with open(P['meteo'], encoding='utf-8') as f: deja = {r['date'] for r in csv.DictReader(f)}
            if v['date'] not in deja:
                with open(P['meteo'], 'a', encoding='utf-8', newline='') as f:
                    csv.writer(f).writerow([v['date'], f'{v["cloture"]:.2f}', f'{v["moyenne_200"]:.2f}', f'{v["ecart"]:.4f}',
                                            'vert' if v['couleur'] == '🟢' else 'rouge', v['depuis'], f'{v["sous_plus_haut"]:.4f}', int(v['krach'])])
    except Exception as e:
        notes.append(f'❌ ERREUR IMPRÉVUE : {type(e).__name__} : {e}')
        notes.append('```\n' + traceback.format_exc() + '```')
    lignes += ['', '## Contrôles'] + [f'- {n}' for n in notes or ['collecte non demandée (sans_collecte)']]
    os.makedirs(os.path.dirname(P['rapport']), exist_ok=True)
    with open(P['rapport'], 'w', encoding='utf-8') as f: f.write('\n'.join(lignes) + '\n')
    print('\n'.join(lignes))
    return 2 if any(n.startswith('❌') for n in notes) else 0


def epreuves(racine):
    """jeu d'épreuves interne (R-731). Valeurs attendues venues d'un calcul INDÉPENDANT (pandas, 29-10-2026) ;
    pages simulées ; heure FIXÉE, calculée depuis la fin de l'historique (jamais l'horloge réelle) ; chaque cas dans
    un dossier temporaire effacé même en cas d'échec.

    ① RÔLE — Prouver, sans réseau et sans écrire sous la racine donnée, que la météo calcule juste
      et refuse d'écrire ce qu'elle ne peut pas vérifier.
    ② CONTEXTE D'APPEL — `main`, quand le second argument est « epreuves » ; la certification de la
      nuit le lance sur une copie du dépôt (tests/LANCEMENT_DES_EPREUVES.json, arguments
      « {copie} epreuves »).
    ③ ENTRÉE — `racine` : la racine du dépôt ou de sa copie, premier argument de la ligne de
      commande ; on y lit l'historique figé, le calendrier et les programmes.
    ④ CONDITIONS D'ENTRÉE — L'historique figé contient au moins les séances jusqu'au 2026-10-02 (les
      attendus de E1 en dépendent) ; le calendrier couvre les huit jours de bourse qui suivent la
      fin de l'historique.
    ⑤ SORTIE — UNE valeur : 0 si les 21 contrôles passent (5 de E1, 16 cas joués par `cas`), 2 sinon. Mesuré le 31-10-2026 sur une copie
      jetable : 21 OK, 0 échec.
      [rend: 1]
    ⑥ TRAITEMENT — ① E1 : le voyant de l'historique coupé au 2026-10-02, au 2020-03-16, au
      2006-06-05 et au 2008-10-06, comparé aux attendus, et la zone de krach au 16-03-2020
      · ② fabriquer les huit jours de bourse qui suivent l'historique et cinq clôtures neuves (la
      dernière de l'historique augmentée de 0,1 %, 0,2 % … 0,5 %) · ③ jouer avec `cas` les cas E2
      à E10 : page saine, passage de 18h07, page fausse sur des séances décidées, avant 18 h,
      retard, page qui contredit le quotidien, désaccord tranché, samedi en trop, six pages
      refusées, variation acceptée par décision, ligne illisible · ④ afficher OK ou ÉCHEC par cas,
      puis le compte des échecs.
    ⑦ UNITÉ — Points d'indice ; moyenne à 0,01 point près ; écarts en fraction à 5e-5 près.
    ⑧ POURQUOI — Tout programme écrit ou modifié passe des épreuves (R-731). L'heure est fixée pour que le résultat
      ne dépende pas du jour du lancement ; les attendus viennent d'un autre calcul que celui
      qu'on éprouve.
    ⑨ CE QUI CLOCHE — ① Le calcul pandas d'où viennent les attendus de E1 n'est pas dans la copie
      du dépôt (recherche de 8238.2, 5654.96 et 4684.24 le 31-10-2026 : seul ce fichier les
      porte) ; la moyenne du 2026-10-02 refaite par awk le 31-10-2026 donne 8238.1987, d'accord. ② Le
      remplacement du téléchargement ne joue que parce que Python garde en mémoire le module
      importé par `modules` : `executer` réimporte depuis le dossier temporaire et reçoit le même
      objet. Sans ce cache, un cas sortirait sur le réseau réel. ③ Aucun cas ne joue le passage du
      matin (7h41, séance de la veille) ni un passage un jour sans bourse.
    ⑩ EFFET — Crée puis efface un dossier temporaire du système par cas (16 cas) ; remplace un temps
      le téléchargement et l'extraction dans le module ABC chargé, puis les remet ; affiche chaque
      rapport et chaque résultat. N'écrit rien sous la racine, sauf les fichiers compilés de Python
      (__pycache__) si on ne lance pas avec -B ; allonge sys.path.
    ⑪ TERMINAISON — Rend la main avec 0 ou 2 ; LÈVE si l'historique ou le calendrier manque, ou si
      le calendrier ne couvre pas les huit jours suivants. Aucun appel ne sort sur le réseau ni ne
      peut ne pas revenir.
      [sort: non]
    ⑫ DÉFINITIONS
      l'historique figé : donnees/sources_indice/INDICE_CAC40.csv, clôtures du CAC 40 depuis le
        03-01-2000 (colonnes date, bnains, yahoo ; seule yahoo est lue), jamais écrit par ce programme
      le fichier quotidien : donnees/indice_cac40_quotidien.csv (colonnes date, close, source),
        les clôtures lues chez ABC après la fin de l'historique figé
      le voyant : 🟢 si la clôture du CAC 40 est au-dessus de la moyenne de ses 200 dernières
        clôtures, 🔴 sinon ; un signal de prudence, pas un ordre
      la certification de la nuit : programmes/CERTIFIER_LA_VERSION.py, qui lance les épreuves
        déclarées dans tests/LANCEMENT_DES_EPREUVES.json sur une copie du dépôt
      ABC : ABC Bourse, le site d'où le projet lit les cours ; PX1p y est le code du CAC 40
    """
    echecs = []
    def ok(cond, txt):
        """note le résultat d'un cas des épreuves.

        ① RÔLE — Afficher chaque cas et retenir les échecs, pour que le compte final ne dépende pas de
          la lecture de l'affichage.
        ② CONTEXTE D'APPEL — `epreuves`, une fois par contrôle (21 fois).
        ③ ENTRÉE — `cond` : vrai si le cas passe · `txt` : le libellé du cas, avec l'obtenu et
          l'attendu.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Ne rend rien.
          [rend: rien]
        ⑥ TRAITEMENT — ① afficher « OK — » ou « ÉCHEC — » suivi du libellé · ② si le cas échoue,
          ajouter le libellé à la liste des échecs d'`epreuves`.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Le code de sortie des épreuves se lit sur cette liste : un échec ne peut pas se
          perdre dans l'affichage.
        ⑨ CE QUI CLOCHE — Rien vu.
        ⑩ EFFET — Affiche une ligne ; allonge la liste des échecs d'`epreuves`.
        ⑪ TERMINAISON — Rend la main. Aucun appel ne peut ne pas revenir.
          [sort: non]
        """
        print(('OK — ' if cond else 'ÉCHEC — ') + txt)
        if not cond: echecs.append(txt)
    P0 = chemins(racine); histo = lire_serie(P0['historique'], 'yahoo')
    attendu = {'2026-10-02': (8238.20, -0.0414, '🔴', 18, -0.0950), '2020-03-16': (5654.96, -0.3136, '🔴', 13, -0.3649),
               '2006-06-05': (4804.65, 0.0232, '🟢', 413, -0.0746), '2008-10-06': (4684.24, -0.2076, '🔴', 237, -0.3669)}
    for J, (mm, ec, coul, dep, sph) in attendu.items():
        v = voyant({d: x for d, x in histo.items() if d <= J})
        ok(abs(v['moyenne_200'] - mm) < 0.01 and abs(v['ecart'] - ec) < 5e-5 and v['couleur'] == coul and v['depuis'] == dep and abs(v['sous_plus_haut'] - sph) < 5e-5,
           f'E1 {J} : moyenne {v["moyenne_200"]:.2f}/{mm} · écart {v["ecart"]:.4f}/{ec} · {v["couleur"]}/{coul} · depuis {v["depuis"]}/{dep} · sous le plus haut {v["sous_plus_haut"]:.4f}/{sph}')
    ok(voyant({d: x for d, x in histo.items() if d <= '2020-03-16'})['krach'], 'E1 16-03-2020 en zone de krach')
    ABC, K = modules(racine); cal = K.lire(racine)
    fin = max(histo); dates = sorted(histo); suite, d = [], date.fromisoformat(fin)
    while len(suite) < 8:
        d += timedelta(days=1)
        if K.est_jour_de_bourse(d, cal): suite.append(d.isoformat())
    def heure(jour, h):
        """rend l'heure fixée d'un cas : le jour donné à h heures pile, heure de Paris.

        ① RÔLE — Donner aux cas une heure de passage FIXE, jamais l'horloge réelle.
        ② CONTEXTE D'APPEL — `epreuves`, pour l'heure de chaque cas joué par `cas` (20 h, 18 h, 15 h).
        ③ ENTRÉE — `jour` : une date AAAA-MM-JJ · `h` : l'heure, de 0 à 23.
        ④ CONDITIONS D'ENTRÉE — La date s'écrit AAAA-MM-JJ et l'heure est entre 0 et 23.
        ⑤ SORTIE — UNE valeur : la date et l'heure (datetime) à h h 00, fuseau Europe/Paris.
          [rend: 1]
        ⑥ TRAITEMENT — Lit « jourThh:00 », puis y attache le fuseau de Paris.
        ⑦ UNITÉ — Heures, heure de Paris.
        ⑧ POURQUOI — Une épreuve qui dépend du jour où on la lance ne prouve plus rien le lendemain.
        ⑨ CE QUI CLOCHE — Rien vu.
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main, ou LÈVE ValueError si la date ou l'heure ne se lit pas.
          [sort: non]
        """
        return datetime.fromisoformat(f'{jour}T{h:02d}:00').replace(tzinfo=ZoneInfo('Europe/Paris'))
    def page(seances):
        """rend une page simulée d'ABC : les séances données, de la plus récente à la plus ancienne.

        ① RÔLE — Imiter ce que rend l'extraction d'ABC, pour jouer les cas sans réseau.
        ② CONTEXTE D'APPEL — `epreuves`, pour fabriquer la page de chaque cas.
        ③ ENTRÉE — `seances` : des couples (date AAAA-MM-JJ, clôture).
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : une liste de dictionnaires {date, close}, de la plus récente à la plus
          ancienne, l'ordre de la vraie page.
          [rend: 1]
        ⑥ TRAITEMENT — Trie les couples par date décroissante et les met sous la forme de l'extraction.
        ⑦ UNITÉ — Points d'indice.
        ⑧ POURQUOI — `lire_page` retrie la page : la servir dans l'ordre de la vraie page éprouve ce tri.
        ⑨ CE QUI CLOCHE — La page simulée ne porte que date et close, pas les autres champs de la vraie
          extraction (ouverture, plus haut, plus bas, volume) : `lire_page` n'en lit pas d'autres
          aujourd'hui ; s'il en lisait, les épreuves ne le verraient pas.
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main. Aucun appel ne peut ne pas revenir.
          [sort: non]
        ⑫ DÉFINITIONS
          ABC : ABC Bourse, le site d'où le projet lit les cours ; PX1p y est le code du CAC 40
        """
        return [{'date': d, 'close': x} for d, x in sorted(seances, reverse=True)]
    base = [(d, histo[d]) for d in dates[-3:]]
    neuves = [(d, histo[fin] * (1 + 0.001 * k)) for k, d in enumerate(suite[:5], 1)]
    soir = heure(suite[4], 20)
    vrais = (ABC.telecharger, ABC.extraire)
    def cas(nom, pg, maintenant, quotidien=(), decisions=(), erreur=None, collecte=True, illisible=False):
        """joue un cas des épreuves dans un dossier temporaire et rend ce qu'il a produit.

        ① RÔLE — Faire tourner `executer` pour de vrai, mais sur une copie minimale et une page
          simulée, puis relever ce qu'il a écrit.
        ② CONTEXTE D'APPEL — `epreuves`, 16 fois (cas E2 à E10).
        ③ ENTRÉE — `nom` : le libellé du cas, jamais utilisé · `pg` : la page simulée, liste de
          {date, close} · `maintenant` : l'heure fixée du passage · `quotidien` : les couples (date,
          clôture) déjà au fichier quotidien avant le passage · `decisions` : les couples (date,
          clôture ou None) à écrire au fichier des décisions · `erreur` : l'exception que le faux
          téléchargement lève, ou None · `collecte` : faux pour jouer le mode sans_collecte
          · `illisible` : vrai pour ajouter au fichier quotidien une ligne dont la date ne se lit pas.
        ④ CONDITIONS D'ENTRÉE — La racine des épreuves porte l'historique figé, le calendrier et
          programmes/. La page vaut None dans le cas « réseau 403 » : elle n'est pas lue, puisque le
          faux téléchargement lève avant.
        ⑤ SORTIE — CINQ valeurs : le code de sortie d'`executer` · le nombre de séances du fichier
          quotidien après le passage (−1 dans le cas illisible) · le nombre de lignes du fichier de
          la météo · le fichier quotidien relu, {date : clôture} (vide dans le cas illisible) · le
          texte du rapport.
          [rend: 5]
        ⑥ TRAITEMENT — ① créer un dossier temporaire · ② y copier l'historique figé et le calendrier,
          y lier programmes/ · ③ écrire le fichier quotidien et celui des décisions demandés
          · ④ remplacer le téléchargement d'ABC (rend « page » ou lève l'erreur) et l'extraction (rend
          la page simulée) · ⑤ lancer `executer` · ⑥ relire le quotidien, la météo et le rapport
          · ⑦ remettre les vraies fonctions d'ABC et effacer le dossier, même en cas d'échec.
        ⑦ UNITÉ — Des comptes de lignes ; points d'indice.
        ⑧ POURQUOI — Éprouver le programme entier, écritures comprises, sans toucher la racine ni le
          réseau.
        ⑨ CE QUI CLOCHE — ① Le libellé n'est jamais utilisé. ② Le rapport est relu sans fermeture
          explicite du fichier. ③ Le remplacement du téléchargement repose sur le cache des modules
          (voir le ⑨ d'`epreuves`).
        ⑩ EFFET — Crée puis efface un dossier temporaire ; remplace puis rétablit deux fonctions du
          module ABC chargé ; `executer` y écrit ses fichiers et affiche son rapport.
        ⑪ TERMINAISON — Rend la main, ou LÈVE si la préparation ou la relecture échoue (le dossier est
          effacé et les fonctions remises quand même). Aucun appel ne sort sur le réseau.
          [sort: non]
        ⑫ DÉFINITIONS
          l'historique figé : donnees/sources_indice/INDICE_CAC40.csv, clôtures du CAC 40 depuis le
            03-01-2000 (colonnes date, bnains, yahoo ; seule yahoo est lue), jamais écrit par ce programme
          le fichier quotidien : donnees/indice_cac40_quotidien.csv (colonnes date, close, source),
            les clôtures lues chez ABC après la fin de l'historique figé
          ABC : ABC Bourse, le site d'où le projet lit les cours ; PX1p y est le code du CAC 40
        """
        tmp = tempfile.mkdtemp()
        try:
            for p in ('donnees/sources_indice/INDICE_CAC40.csv', 'donnees/CALENDRIER_EURONEXT.csv'):
                os.makedirs(os.path.dirname(os.path.join(tmp, p)), exist_ok=True); shutil.copy(os.path.join(racine, p), os.path.join(tmp, p))
            os.symlink(P0['programmes'], os.path.join(tmp, 'programmes'))
            P = chemins(tmp)
            if quotidien or illisible:
                creer_si_absent(P['quotidien'], ENTETE_QUOTIDIEN)
                with open(P['quotidien'], 'a', encoding='utf-8', newline='') as f:
                    for d, x in quotidien: csv.writer(f).writerow([d, x, 'abc'])
                    if illisible: f.write('pas-une-date,abc,abc\n')
            if decisions:
                with open(P['decisions'], 'w', encoding='utf-8', newline='') as f:
                    w = csv.writer(f); w.writerow(['date', 'close', 'motif'])
                    for d, x in decisions: w.writerow([d, '' if x is None else x, 'épreuve'])
            def tel(url, e=erreur):
                """faux téléchargement : lève l'erreur prévue par le cas, sinon rend un texte quelconque.

                ① RÔLE — Remplacer le téléchargement d'ABC pendant un cas, pour qu'aucune épreuve ne sorte sur
                  le réseau.
                ② CONTEXTE D'APPEL — `lire_page`, à travers le module ABC, pendant un cas joué par `cas`.
                ③ ENTRÉE — `url` : l'adresse demandée (https://www.abcbourse.com/cotation/PX1p),
                  ignorée · `e` : l'exception à lever, ou None ; par défaut l'erreur du cas, figée à la
                  définition.
                ④ CONDITIONS D'ENTRÉE — —
                ⑤ SORTIE — UNE valeur : le texte « page », que la fausse extraction ignore.
                  [rend: 1]
                ⑥ TRAITEMENT — Lever l'exception si elle est donnée, sinon rendre « page ».
                ⑦ UNITÉ — —
                ⑧ POURQUOI — Simuler une page refusée (« HTTP Error 403 ») aussi bien qu'une page lue.
                ⑨ CE QUI CLOCHE — Rien vu.
                ⑩ EFFET — Aucun.
                ⑪ TERMINAISON — Rend la main, ou LÈVE l'exception donnée. Aucun appel ne peut ne pas revenir.
                  [sort: non]
                ⑫ DÉFINITIONS
                  ABC : ABC Bourse, le site d'où le projet lit les cours ; PX1p y est le code du CAC 40
                """
                if e: raise e
                return 'page'
            ABC.telecharger = tel; ABC.extraire = lambda h, p=pg: (p, '' if p else 'aucune ligne')
            code = executer(tmp, collecte, maintenant)
            n_q = len(lire_serie(P['quotidien'], 'close')) if not illisible else -1
            n_m = len(lire_serie(P['meteo'], 'cloture'))
            q = lire_serie(P['quotidien'], 'close') if not illisible else {}
            return code, n_q, n_m, q, open(P['rapport'], encoding='utf-8').read()
        finally:
            ABC.telecharger, ABC.extraire = vrais
            shutil.rmtree(tmp, ignore_errors=True)
    c, nq, nm, q, r = cas('saine', page(base + neuves), soir)
    ok(c == 0 and nq == 5 and nm == 1 and ('AU-DESSUS' in r or 'EN DESSOUS' in r), f'E2 page saine à jour : code {c} (0), {nq} séances (5), {nm} ligne de météo (1)')
    c, nq, nm, q, r = cas('18h07', page(base + neuves), heure(suite[4], 18).replace(minute=7))
    ok(c == 0 and nq == 5 and nm == 1, f'E2b passage réel du circuit à 18h07 : code {c} (0), {nq} séances (5), {nm} ligne de météo (1)')
    c, nq, nm, q, r = cas('page fausse et décision isolée', page([(d, x * 1.02) for d, x in neuves[2:]] + [(suite[5], neuves[-1][1] * 1.02)]),
                          heure(suite[5], 20), quotidien=neuves, decisions=[(suite[2], None), (suite[3], None), (suite[4], None)])
    ok(c == 2 and nq == 5, f'E5b page fausse dont toutes les séances connues portent une décision vide : code {c} (2), rien écrit ({nq} séances, 5)')
    c, nq, nm, q, r = cas('avant 18h', page(base + neuves), heure(suite[4], 15))
    ok(c == 0 and nq == 4 and suite[4] not in q, f'E3 avant 18h : la séance du jour est retirée — code {c} (0), {nq} séances (4)')
    c, nq, nm, q, r = cas('retard', page(base + neuves), heure(suite[7], 20))
    ok(c == 2 and nm == 0 and 'SÉANCES MANQUANTES' in r and 'AU-DESSUS' not in r and 'EN DESSOUS' not in r, f'E4 en retard de 3 séances : code {c} (2), voyant non affiché, {nm} ligne de météo (0)')
    rev = page(base[-1:] + neuves[:-1] + [(neuves[-1][0], neuves[-1][1] * 1.03)] + [(suite[5], neuves[-1][1])])
    c, nq, nm, q, r = cas('désaccord', [s for s in rev if s['date'] > fin], heure(suite[5], 20), quotidien=neuves)
    ok(c == 2 and nq == 5 and suite[5] not in q and abs(q[neuves[-1][0]] - neuves[-1][1]) < 1e-9 and 'CONTREDIT' in r,
       f'E5 page qui contredit le fichier quotidien (sans aucune séance de l historique) : code {c} (2), rien écrit ({nq} séances, 5), valeur d origine gardée')
    c, nq, nm, q, r = cas('désaccord tranché', [s for s in rev if s['date'] > fin], heure(suite[5], 20), quotidien=neuves, decisions=[(neuves[-1][0], neuves[-1][1] * 1.03)])
    ok(c == 0 and nq == 6 and nm == 1, f'E6 désaccord tranché par une décision de Jean-Luc : code {c} (0), {nq} séances (6), {nm} ligne de météo (1)')
    samedi = next(dd for dd in (date.fromisoformat(suite[0]) + timedelta(days=k) for k in range(1, 10)) if dd.weekday() == 5).isoformat()
    trou = [x for x in neuves if x[0] != suite[1]] + [(samedi, neuves[0][1])]
    c, nq, nm, q, r = cas('samedi', [], soir, quotidien=trou, collecte=False)
    ok(c == 2 and nm == 0 and 'EN TROP' in r and 'MANQUANTES' in r, f'E7 un samedi en trop et un jour de bourse manquant (même nombre) : code {c} (2), {nm} ligne de météo (0)')
    for nom, pg, err in [('vide', [], None), ('réseau 403', None, Exception('HTTP Error 403')),
                         ('mauvaise colonne', page([(d, x / 1000) for d, x in base + neuves]), None),
                         ('écart de 2 % avec l historique', page([(d, x * 1.02) for d, x in base] + neuves), None),
                         ('sans séance commune', page(neuves[2:]), None),
                         ('variation de 40 %', page(base + [(suite[0], histo[fin] * 0.6)]), None)]:
        c, nq, nm, q, r = cas(nom, pg, soir, erreur=err)
        ok(c == 2 and nq == 0 and nm == 0 and '❌' in r, f'E8 {nom} : code {c} (2), {nq} séances écrites (0), {nm} ligne de météo (0)')
    c, nq, nm, q, r = cas('variation acceptée', page(base + [(suite[0], histo[fin] * 0.6)]), heure(suite[0], 20), decisions=[(suite[0], None)])
    ok(c == 0 and nq == 1, f'E9 variation de 40 % acceptée par une décision de Jean-Luc : code {c} (0), {nq} séance écrite (1)')
    c, nq, nm, q, r = cas('illisible', [], soir, collecte=False, illisible=True)
    ok(c == 2 and 'ERREUR IMPRÉVUE' in r, f'E10 ligne illisible : code {c} (2), rapport écrit avec l erreur')
    print(f'\nÉPREUVES DE LA MÉTÉO : {len(echecs)} échec(s)')
    return 2 if echecs else 0


def main():
    """lit la ligne de commande et lance le passage (à l'heure réelle de Paris) ou les épreuves.

    ① RÔLE — Point d'entrée du programme : choisir entre le passage et les épreuves, et rendre leur
      code de sortie au système.
    ② CONTEXTE D'APPEL — En ligne de commande : par le circuit du soir (étape « Calculer la meteo du
      marche » de .github/workflows/collecte_abc.yml, avec la racine seule), par la certification
      de la nuit (avec « epreuves »), ou à la main.
    ③ ENTRÉE — La ligne de commande : premier argument, la racine (« . » s'il manque) ; second
      argument facultatif, « sans_collecte » ou « epreuves » ; tout autre mot vaut un passage AVEC
      collecte.
    ④ CONDITIONS D'ENTRÉE — Celles d'`executer` ou d'`epreuves`.
    ⑤ SORTIE — Ne rend rien : sort du programme avec le code d'`executer` ou d'`epreuves`, 0 ou 2.
      [rend: rien]
    ⑥ TRAITEMENT — ① lire les deux arguments · ② « epreuves » : lancer les épreuves · ③ sinon
      lancer le passage à l'heure réelle de Paris, avec collecte sauf « sans_collecte ».
    ⑦ UNITÉ — Un code de sortie.
    ⑧ POURQUOI — L'heure réelle n'est lue qu'ici : tout le reste la reçoit en paramètre, ce qui
      permet aux épreuves de la fixer.
    ⑨ CE QUI CLOCHE — Un second argument mal écrit (« sans-collecte ») lance un passage AVEC
      collecte, donc sur le réseau, sans rien dire.
    ⑩ EFFET — Ceux d'`executer` ou d'`epreuves`.
    ⑪ TERMINAISON — SORT DU PROGRAMME (sys.exit) avec 0 ou 2 ; avec 1, par une trace Python, si
      `executer` lève en écrivant le rapport (voir son ⑨) ou si `epreuves` lève. Le seul appel qui attend un tiers est le
      téléchargement, borné à 30 secondes par attente.
      [sort: oui]
    ⑫ DÉFINITIONS
      le circuit du soir : le passage automatique de chaque soir sur une machine GitHub,
        .github/workflows/collecte_abc.yml, réveillé depuis le dépôt public (18h07, secours 21h23,
        rattrapage 7h41 le lendemain matin, d'après l'en-tête de collecte_abc.yml)
      la certification de la nuit : programmes/CERTIFIER_LA_VERSION.py, qui lance les épreuves
        déclarées dans tests/LANCEMENT_DES_EPREUVES.json sur une copie du dépôt
    """
    racine = sys.argv[1] if len(sys.argv) > 1 else '.'
    mode = sys.argv[2] if len(sys.argv) > 2 else ''
    if mode == 'epreuves': sys.exit(epreuves(racine))
    sys.exit(executer(racine, mode != 'sans_collecte', datetime.now(ZoneInfo('Europe/Paris'))))


if __name__ == '__main__':
    main()
