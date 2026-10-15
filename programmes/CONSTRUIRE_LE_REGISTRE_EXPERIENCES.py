#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSTRUIRE LE REGISTRE DES EXPÉRIENCES — amorce les deux fichiers qui compteront
les essais de recherche, et rend un code de sortie.

① RÔLE — Rendre visible le nombre d'essais faits avant de retenir une stratégie.
  Sans ce compte, une stratégie qui affiche 70 % de réussite peut être la
  meilleure de 3 888 combinaisons essayées sur le même passé — 6 modes d'entrée
  × 9 objectifs × 8 seuils × 9 horizons — et personne ne peut distinguer une
  trouvaille d'un tirage chanceux. Ce programme ne compte rien lui-même : il crée
  les deux fichiers qui recevront ce compte, et inscrit dans le premier les
  stratégies déjà connues avec la mention « nombre d'essais inconnu ». Il ne
  calcule aucune performance et ne teste aucune stratégie. Demandé par l'action
  A-226 du tableau des décisions du projet, ouverte le 16-08-2026 et encore au
  statut « À FAIRE·16/08 » le 19-09-2026.
② CONTEXTE D'APPEL — Lancé à la main, une fois, pour amorcer les fichiers. AUCUN
  LANCEUR AUTOMATIQUE : une recherche du nom de ce programme dans les deux tâches
  planifiées du dépôt, `.github/workflows/collecte_abc.yml` et
  `.github/workflows/comparer_google_abc.yml`, et dans les 34 programmes de
  `programmes/`, ne trouve aucun appel le 19-09-2026. Le relevé
  `gouvernance/SOCLE.csv` le range en PRÉSUMÉ avec le motif « aucun lanceur
  detecte — un lancement a la main ne s ecrit nulle part ».
③ ENTRÉE — La ligne de commande, deux arguments FACULTATIFS : le dossier où
  chercher le registre des stratégies, puis le dossier où écrire les deux
  fichiers. Sans argument, les deux valent le dossier courant.
④ CONDITIONS D'ENTRÉE — Le registre des stratégies `cac40_strategies.csv` doit
  exister, soit dans `donnees/` sous le dossier source, soit à plat dans ce
  dossier. Le dossier de sortie doit DÉJÀ porter un sous-dossier `donnees/` : le
  programme crée le dossier de sortie, jamais ce sous-dossier.
⑤ SORTIE — Un code de sortie, et rien d'autre : 0 si les deux fichiers ont été
  écrits puis relus conformes, 1 si le registre des stratégies est introuvable ou
  si la relecture ne concorde pas. Les deux fichiers sont écrits sur le disque.
⑥ TRAITEMENT — ① lire le registre des stratégies · ② en tirer une ligne par
  stratégie, au statut HISTORIQUE_NON_COMPTABILISE · ③ écrire le fichier de
  détail · ④ écrire le fichier de résumé, vide, avec son seul en-tête · ⑤ relire
  les deux fichiers et vérifier cinq propriétés · ⑥ afficher le bilan · ⑦ rendre
  0 ou 1.
⑦ UNITÉ — Les expériences se comptent en LIGNES DE FICHIER, une ligne par essai
  pour le détail, une ligne par balayage pour le résumé. Les tailles s'affichent
  en OCTETS. Les dates inscrites dans les fichiers s'écrivent année-mois-jour.
⑧ POURQUOI — DEUX FICHIERS ET NON UN, parce que le détail ne tient pas dans la
  place disponible. Mesure du 20-08-2026 : une ligne d'expérience pesait
  221 octets, un seul balayage de 3 888 combinaisons pesait 863 254 octets, et la
  marge restante était de 304 925 octets. Le détail part donc sur Google Drive,
  et le résumé — une ligne par balayage, pas par essai, soit quelques centaines
  d'octets — reste avec les données du système.
  LE STATUT HISTORIQUE_NON_COMPTABILISE, ET JAMAIS ZÉRO : pour les stratégies
  antérieures au registre, le nombre de variantes essayées avant de les retenir
  n'a jamais été noté. Écrire 0 affirmerait qu'aucune variante n'a été essayée,
  ce qui est faux et indémontrable. Conséquence assumée : une stratégie dont
  l'historique de recherche est inconnu ne peut pas être présentée comme
  proprement comptabilisée — elle vit, mais son niveau de preuve est inférieur.
  AUCUNE PÉNALITÉ MATHÉMATIQUE n'est appliquée, du type « 1 000 essais exigent un
  résultat d'autant meilleur ». 3 888 combinaisons ne sont pas 3 888 essais
  indépendants : faire passer un objectif de +1,0 % à +1,2 % donne deux séries de
  trades presque identiques, et les deux résultats se ressemblent par
  construction. On rend d'abord le phénomène observable ; pénaliser viendra
  ensuite, si le besoin est démontré.
  LE PROGRAMME RELIT CE QU'IL VIENT D'ÉCRIRE avant d'annoncer quoi que ce soit,
  parce qu'un fichier ouvert en écriture peut être écrit ailleurs que là où on
  croit, ou tronqué. Tant que la relecture n'a pas concordé, rien n'est présenté
  comme fait.
⑨ CE QUI CLOCHE — LES DEUX FICHIERS NE VONT PAS AU MÊME ENDROIT, ET RIEN NE LE
  JUSTIFIE. Le résumé est écrit dans `donnees/` sous le dossier de sortie, le
  détail à la racine de ce même dossier. Lancé le 19-09-2026 sur une copie du
  dépôt, le programme a écrit `donnees/registre_experiences_resume.csv` et
  `registre_experiences.csv`, ce dernier à la racine, à côté des documents de
  gouvernance. Le relevé `gouvernance/SOCLE.csv` range d'ailleurs
  `registre_experiences.csv` en DORMANT avec le motif « aucun lecteur detecte ».
  Le commentaire qui accompagne le chemin du résumé dit pourtant que les fichiers
  de données vivent dans `donnees/`.
⑩ EFFET — ÉCRIT deux fichiers, en écrasant sans avertissement ce qui portait déjà
  ces noms. CRÉE le dossier de sortie s'il manque. LIT le registre des stratégies
  puis relit les deux fichiers qu'il vient d'écrire. Affiche une quinzaine de
  lignes. Aucun accès réseau.
⑪ TERMINAISON — SORT DU PROGRAMME avec le code rendu par `main` : 0 si tout
  concorde, 1 si le registre des stratégies est introuvable ou si la relecture
  échoue. Et un de ses appels peut ne pas revenir : `main` lève une erreur non
  rattrapée quand le dossier de sortie ne porte pas de sous-dossier `donnees/` —
  mesuré le 19-09-2026, « FileNotFoundError », après que le fichier de détail a
  déjà été écrit.
⑫ DÉFINITIONS
  une expérience : un essai de recherche — une variante de stratégie jouée sur
    les cours passés, qu'elle ait donné un résultat ou non
  un balayage : une série d'essais faits d'un coup en faisant varier les réglages
    d'une même stratégie, par exemple 3 888 combinaisons d'entrée, d'objectif, de
    seuil de perte et d'horizon
  le registre des stratégies : le fichier `cac40_strategies.csv`, une ligne par
    stratégie, qui porte leur état civil — identifiant, réglages, résultats connus
  le détail : le fichier `registre_experiences.csv`, une ligne par expérience
  le résumé : le fichier `registre_experiences_resume.csv`, une ligne par balayage — une série d'essais faits d'un coup sur une même stratégie
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
    étant qu'une copie de lecture
  le tableau des décisions : le fichier `BACKLOG_DECISIONS.md`, dont chaque ligne porte un identifiant de la forme `A-238`
  HISTORIQUE_NON_COMPTABILISE : le statut porté par ces lignes
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
  une stratégie : une règle qui dit QUOI acheter, avec son objectif de gain, sa perte acceptée et son horizon
"""

import csv
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")
JOURS = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

# --------------------------------------------------------------------------
# LES DEUX EN-TETES — la definition des champs vit ICI et nulle part ailleurs
# --------------------------------------------------------------------------

# LE DETAIL : une ligne par experience. Meme une experience sans resultat est
# enregistree (A-226 : « Meme une experience sans resultat est enregistree »).
CHAMPS_DETAIL = [
    "id_exp",             # R000001, R000002... jamais reutilise
    "strategie_parente",  # de quelle strategie cette experience est une variante
    "hypothese",          # ce qu'on cherchait a savoir, en clair
    "parametres",         # entree | tp | sl | horizon, separes par |
    "univers",            # mnemoniques ou nom du groupe (l'univers EST un parametre, A-238)
    "periode",            # AAAA-MM-JJ..AAAA-MM-JJ reellement utilisee
    "donnees",            # quels fichiers de cours ont servi
    "resultat",           # n=.. | wr=.. | net=.. — vide si l'essai n'a rien donne
    "statut",             # ESSAYE / RETENUE / ECARTEE / ABANDONNEE / HISTORIQUE_NON_COMPTABILISE
    "niveau_preuve",      # A / B / C / — (voir docstring)
    "date",               # AAAA-MM-JJ
    "motif_abandon",      # pourquoi ecartee — vide si retenue
]

# LE RESUME : une ligne par BALAYAGE, pas par experience. C'est cette ligne
# qui repond a la seule question qui compte : combien en a-t-on essayes ?
CHAMPS_RESUME = [
    "id_balayage",        # B0001, B0002...
    "strategie_parente",
    "grille",             # description de la grille testee, en clair
    "n_essais",           # LE CHIFFRE CENTRAL — jamais estime, toujours compte
    "n_retenues",
    "retenue_id_exp",     # renvoi vers la ligne du detail
    "retenue_resultat",
    "niveau_preuve",
    "periode",
    "date",
    "fichier_detail",     # ou vit le detail (Drive)
]

STATUT_HISTORIQUE = "HISTORIQUE_NON_COMPTABILISE"

NOM_DETAIL = "registre_experiences.csv"
# LE RESUME VIT DANS `donnees/`, COMME TOUS LES FICHIERS DE DONNEES.
# Deuxieme homonyme trouve le 16-09-2026 par le controle du socle, le meme
# jour ou il a ete ecrit. **Deux `registre_experiences_resume.csv` coexistaient
# — racine et `donnees/` — avec la MEME empreinte `ba427f0bde1a8bf0`.**
# Identiques aujourd hui, donc sans degat : **mais c est exactement la
# configuration qui a coute trois jours sur `historique_mesures.csv`, ou
# l ecrivain et le lecteur avaient diverge sans que rien ne le dise.**
# On corrige avant la divergence, pas apres.
NOM_RESUME = os.path.join("donnees", "registre_experiences_resume.csv")


def horodatage():
    """Rend la date et l'heure de Paris en toutes lettres, pour l'affichage.

    ① RÔLE — Donner à l'en-tête affiché par le programme un repère de temps
      lisible, pour que la personne qui lit la sortie sache de quand elle date.
      Exemple produit le 19-09-2026 : `Sam 19-09-2026 22h53 (Paris)`.
    ② CONTEXTE D'APPEL — `main`, une seule fois, à la première ligne affichée,
      avant toute lecture de fichier. Jamais appelée ailleurs.
    ③ ENTRÉE — Aucun paramètre.
    ④ CONDITIONS D'ENTRÉE — Aucune. Elle lit l'horloge de la machine.
    ⑤ SORTIE — UNE valeur : un texte, toujours de la même forme, par exemple
      `Sam 19-09-2026 22h53 (Paris)`.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire l'heure courante dans le fuseau Europe/Paris · ② prendre
      le nom abrégé du jour dans la liste des sept jours · ③ composer le texte.
    ⑦ UNITÉ — Une DATE et une HEURE D'HORLOGE, en heure de Paris, arrêtées à la
      minute. Les secondes ne sont pas rendues.
    ⑧ POURQUOI — Le fuseau est fixé à Europe/Paris et jamais pris de la machine :
      les tâches planifiées du dépôt s'exécutent sur des machines réglées en temps
      universel, en retard d'une ou deux heures sur Paris selon la saison. Un
      horodatage pris de la machine daterait un passage de 00h30 à Paris de la
      veille 22h30, et deux traces ne se compareraient plus. Le nom du jour est
      écrit en français dans une liste plutôt que demandé au langage, qui le rend
      en anglais ou en français selon le réglage de la machine.
    ⑨ CE QUI CLOCHE — Cette fonction existe en TROIS exemplaires identiques dans le
      dépôt, au caractère près : `programmes/JUGE_DES_STRATEGIES.py`,
      `programmes/claude_FABRIQUER_LE_PILOTE.py` et ce fichier portent les trois
      mêmes lignes, relevées le 19-09-2026 en cherchant les définitions de
      `horodatage` dans les 34 programmes de `programmes/`. Un calcul qui existe
      ailleurs ne se recopie pas, parce que deux implémentations d'une même chose
      finissent toujours par diverger (R-708) : le jour où le format changera dans
      l'un des trois, les deux autres continueront d'écrire l'ancien, et aucune
      alerte ne le dira.
    ⑩ EFFET — LIT l'horloge de la machine. N'écrit aucun fichier, n'affiche rien
      elle-même, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas. Aucun de ses appels ne
      se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    n = datetime.now(PARIS)
    return f"{JOURS[n.weekday()]} {n.strftime('%d-%m-%Y %Hh%M')} (Paris)"


def lire_strategies(chemin):
    """Rend les lignes du registre des stratégies, ou rien si le fichier manque.

    ① RÔLE — Fournir au programme la liste des stratégies déjà connues, qui est la
      seule matière dont il dispose pour amorcer le registre des expériences, et
      distinguer le cas « fichier absent » du cas « fichier présent mais vide ».
      Sans cette distinction, un fichier manquant produirait un registre vide
      présenté comme un registre complet.
    ② CONTEXTE D'APPEL — `main`, une seule fois, après avoir choisi entre deux
      chemins possibles pour le registre des stratégies. Jamais appelée ailleurs.
    ③ ENTRÉE — `chemin` : le chemin du registre des stratégies à lire. Un seul
      appelant, `main`, et il passe `donnees/cac40_strategies.csv` sous le dossier
      source quand ce fichier existe, sinon `cac40_strategies.csv` à plat dans ce
      dossier.
    ④ CONDITIONS D'ENTRÉE — Aucune sur la forme du chemin. Si le fichier existe, il
      doit être lisible en UTF-8 et porter une première ligne d'en-tête nommant ses
      colonnes.
    ⑤ SORTIE — UNE valeur, de DEUX formes selon le cas. Une LISTE de lignes quand
      le fichier existe, chaque ligne étant un dictionnaire dont les clés sont les
      noms de colonnes ; cette liste est vide si le fichier ne porte que son
      en-tête. `None` quand le chemin n'existe pas.
      [rend: 1]
    ⑥ TRAITEMENT — ① si le chemin n'existe pas, rendre `None` et s'arrêter là ·
      ② ouvrir le fichier · ③ lire toutes ses lignes en dictionnaires et les rendre.
    ⑦ UNITÉ — Un NOMBRE DE LIGNES : 68 stratégies lues le 19-09-2026 dans
      `donnees/cac40_strategies.csv`, pour un fichier de 69 lignes, en-tête compris.
    ⑧ POURQUOI — Le fichier est ouvert en `utf-8-sig` et non en `utf-8` simple :
      un tableur qui enregistre un CSV place trois octets invisibles en tête du
      fichier, et lus en `utf-8` simple ils se collent au nom de la première
      colonne : la colonne `id` porte alors un nom qui n'est plus `id`, et toute
      demande de cette colonne rend du vide pour chaque ligne, sans aucune erreur
      affichée. Le mode
      `utf-8-sig` retire ces octets.
      Tout le fichier est chargé en mémoire d'un coup, et non lu ligne à ligne,
      parce qu'il est petit et connu : 68 lignes pour 39 725 octets le 19-09-2026.
    ⑨ CE QUI CLOCHE — ① Le fichier absent et le fichier vide se ressemblent trop
      dans la suite du traitement. Lancé le 19-09-2026 sur un registre de
      stratégies ne portant que sa ligne d'en-tête, le programme écrit un fichier
      de détail de zéro ligne, puis échoue au contrôle sous le libellé « colonnes
      conformes : ECHEC » — alors que les colonnes sont correctes et que la vraie
      cause est l'absence de stratégies.
      ② `os.path.exists` accepte aussi un dossier. Mesuré le 19-09-2026 en créant
      un dossier nommé `donnees/cac40_strategies.csv` : `main` écarte ce chemin de
      lui-même parce qu'il vérifie de son côté qu'il s'agit d'un fichier, et se
      rabat sur le second chemin, qui n'existe pas ; le message d'arrêt nomme alors
      ce second chemin et non le dossier fautif.
    ⑩ EFFET — LIT le fichier désigné, en entier et en mémoire. N'écrit rien,
      n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main dans les cas prévus. PEUT LEVER une erreur
      non rattrapée si le chemin existe mais n'est pas lisible : un dossier donne
      `IsADirectoryError`, un fichier sans droit de lecture donne
      `PermissionError`, et un fichier qui n'est pas de l'UTF-8 donne
      `UnicodeDecodeError`. Aucun de ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le registre des stratégies : le fichier `cac40_strategies.csv`, une ligne par
        stratégie, qui porte leur état civil — identifiant, réglages, résultats
        connus
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if not os.path.exists(chemin):
        return None
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def amorcer_detail(strategies, aujourd_hui):
    """Transforme chaque stratégie connue en une déclaration d'ignorance.

    ① RÔLE — Inscrire dans le registre des expériences les stratégies antérieures
      à ce registre, en disant explicitement que le nombre d'essais qui a mené à
      chacune est INCONNU. Les lignes produites ne sont PAS des expériences : ce
      sont des déclarations d'ignorance. Leur présence empêche qu'une stratégie
      ancienne soit un jour comptée comme née de zéro essai.
    ② CONTEXTE D'APPEL — `main`, une seule fois, entre la lecture du registre des
      stratégies et l'écriture du fichier de détail. Jamais appelée ailleurs.
    ③ ENTRÉE — `strategies` : les lignes du registre des stratégies, chacune étant
      un dictionnaire dont les clés sont les noms de colonnes · `aujourd_hui` : la
      date du jour en année-mois-jour, par exemple `2026-09-19`. Un seul appelant,
      `main`, et il passe les 68 lignes lues dans `donnees/cac40_strategies.csv` le
      19-09-2026 et la date du jour prise à l'horloge de Paris.
    ④ CONDITIONS D'ENTRÉE — `strategies` doit être une suite, éventuellement vide ;
      ses éléments doivent répondre à une demande de colonne par leur nom. Aucune
      colonne n'est obligatoire : une colonne absente est traitée comme vide.
      `aujourd_hui` est recopié tel quel, sans contrôle de format.
    ⑤ SORTIE — UNE valeur : une liste de lignes prêtes à écrire, une par stratégie
      reçue, chacune portant les douze colonnes du fichier de détail. Liste vide si
      aucune stratégie n'est reçue.
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque stratégie, dans l'ordre où elle arrive : ① lui
      donner un identifiant d'expérience formé de la lettre R et de son rang sur
      six chiffres · ② recopier son identifiant de stratégie · ③ écrire une
      hypothèse fixe qui dit que le nombre d'essais n'a jamais été tracé ·
      ④ assembler ses réglages — objectif, seuil de perte, horizon — en écartant
      ceux qui sont vides · ⑤ assembler ses résultats connus — nombre de trades et
      taux de réussite — de la même façon · ⑥ poser le statut
      HISTORIQUE_NON_COMPTABILISE et un niveau de preuve sans objet · ⑦ poser la
      date du jour.
    ⑦ UNITÉ — L'objectif et le seuil de perte sont recopiés TELS QUELS depuis le
      registre des stratégies, avec leur signe et leur symbole : `tp=+1.0%` et
      `sl=-1.0%` pour la stratégie C1-002 le 19-09-2026. L'horizon est un NOMBRE DE
      SÉANCES de bourse, écrit `5j`, ou le mot `Intraday` quand la position se
      ferme le jour même. Le nombre de trades est un NOMBRE D'OPÉRATIONS, le taux
      de réussite un POURCENTAGE d'opérations gagnantes : `n=12|wr=75%`.
    ⑧ POURQUOI — Les réglages et les résultats sont assemblés en un seul texte
      séparé par des barres verticales, plutôt que rangés chacun dans sa colonne,
      parce que les réglages d'une stratégie future ne sont pas connus d'avance :
      une stratégie à venir pourra porter un filtre de volume ou un seuil de
      volatilité qui n'existe dans aucune colonne aujourd'hui. Un texte accueille
      ces réglages sans changer la forme du fichier, donc sans casser les lignes
      déjà écrites.
      Les réglages vides sont écartés plutôt qu'écrits vides : `tp=+1.0%|sl=-1.0%`
      dit que l'horizon n'est pas connu, là où `tp=+1.0%|sl=-1.0%|horizon=` laisse
      croire à un horizon nul.
    ⑨ CE QUI CLOCHE — ① Les identifiants d'expérience sont attribués par la POSITION
      de la stratégie dans le fichier source, alors que le code promet à côté de la
      colonne `id_exp` qu'un identifiant n'est « jamais reutilise ». Mesuré le
      19-09-2026 : sur le registre des stratégies tel qu'il est, C1-002 reçoit
      `R000001` ; en insérant une seule stratégie en deuxième ligne du fichier
      source et en relançant, `R000001` désigne la stratégie insérée et C1-002
      devient `R000002`. Le même identifiant désigne alors deux expériences
      différentes selon la date du passage, et tout renvoi vers lui devient faux.
      ② Trois colonnes sur douze sont écrites vides pour toutes les lignes.
      Mesuré le 19-09-2026 sur les 68 lignes produites : `periode`, `donnees` et
      `motif_abandon` sont vides 68 fois sur 68, et `univers` 59 fois sur 68. Or le
      registre des stratégies porte lui-même une colonne `periode` renseignée pour
      3 stratégies, qui n'est jamais recopiée. L'univers — la liste des valeurs sur
      lesquelles une stratégie est jouée — est le paramètre le plus puissant du
      système : 61 % de réussite à l'intérieur contre 40,8 % à l'extérieur, ce que
      consigne l'action A-238 du tableau des décisions. Une colonne prévue pour lui
      et laissée vide neuf fois sur dix ne remplit pas son office.
      ③ Le motif d'abandon reste vide alors que la matière existe : 30 des
      68 stratégies portent le statut « 📦 ARCHIVÉE » dans le registre des
      stratégies, avec une note qui explique pourquoi, et aucune de ces notes n'est
      reprise.
    ⑩ EFFET — Ne change rien : elle lit les lignes reçues et en compose de
      nouvelles. N'écrit aucun fichier, n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas tant que les éléments
      reçus répondent à une demande de colonne par leur nom. Aucun de ses appels ne
      se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      une déclaration d'ignorance : une ligne du registre des expériences qui dit
        qu'on ne sait pas combien d'essais ont précédé une stratégie, par
        opposition à une ligne qui dirait qu'il n'y en a eu aucun
      HISTORIQUE_NON_COMPTABILISE : le statut porté par ces lignes
      le registre des stratégies : le fichier `cac40_strategies.csv`, une ligne par
        stratégie, qui porte leur état civil — identifiant, réglages, résultats
        connus
      l'univers : la liste des valeurs sur lesquelles une stratégie a le droit d'acheter, désignées par leur mnémonique
      un trade : une opération simulée, de l'achat à la revente
      le tableau des décisions : le fichier `BACKLOG_DECISIONS.md`, dont chaque
        ligne porte un identifiant de la forme `A-238`
    
      l'horizon : le nombre de séances pendant lesquelles une position est tenue si ni l'objectif de gain ni la perte acceptée ne sont atteints
      le seuil de perte : le prix auquel la position se ferme en perte.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    lignes = []
    for i, s in enumerate(strategies, start=1):
        lignes.append({
            "id_exp": f"R{i:06d}",
            "strategie_parente": (s.get("id") or "").strip(),
            "hypothese": "historique anterieur au registre — nombre d'essais jamais trace",
            "parametres": "|".join(x for x in [
                f"tp={(s.get('tp') or '').strip()}",
                f"sl={(s.get('sl') or '').strip()}",
                f"horizon={(s.get('horizon') or '').strip()}",
            ] if not x.endswith("=")),
            "univers": (s.get("univers") or "").strip(),
            "periode": "",
            "donnees": "",
            "resultat": "|".join(x for x in [
                f"n={(s.get('n_trades') or '').strip()}",
                f"wr={(s.get('wr') or '').strip()}",
            ] if not x.endswith("=")),
            "statut": STATUT_HISTORIQUE,
            "niveau_preuve": "—",
            "date": aujourd_hui,
            "motif_abandon": "",
        })
    return lignes


def ecrire_csv(chemin, champs, lignes):
    """Écrit un fichier CSV avec son en-tête, en écrasant ce qui s'y trouvait.

    ① RÔLE — Donner aux deux fichiers du registre des expériences une seule et même
      façon d'être écrits, pour que le détail et le résumé ne puissent pas prendre
      deux formats différents. C'est le seul endroit du programme où un fichier est
      écrit.
    ② CONTEXTE D'APPEL — `main`, deux fois : d'abord pour le fichier de détail avec
      ses lignes, ensuite pour le fichier de résumé sans aucune ligne. Jamais
      appelée ailleurs.
    ③ ENTRÉE — `chemin` : où écrire le fichier · `champs` : les noms de colonnes, en
      ordre, qui formeront la première ligne · `lignes` : les lignes à écrire,
      chacune étant un dictionnaire dont les clés sont ces noms de colonnes. Un seul
      appelant, `main`, et il passe soit les douze colonnes du détail avec
      68 lignes, soit les onze colonnes du résumé avec aucune ligne — mesuré le
      19-09-2026.
    ④ CONDITIONS D'ENTRÉE — Le dossier du chemin doit DÉJÀ exister : cette fonction
      ne le crée pas. Chaque ligne doit porter exactement les clés annoncées dans
      `champs`, ni plus ni moins : une clé en trop fait lever une erreur, une clé
      manquante fait écrire une case vide.
    ⑤ SORTIE — Ne rend rien. Le résultat est le fichier écrit.
      [rend: rien]
    ⑥ TRAITEMENT — ① ouvrir le fichier en écriture, en écrasant ce qui s'y trouvait ·
      ② écrire la ligne d'en-tête avec les noms de colonnes · ③ écrire chaque ligne
      dans l'ordre reçu.
    ⑦ UNITÉ — Un NOMBRE DE LIGNES écrites. Le fichier de détail produit le
      19-09-2026 pesait 12 208 octets pour 68 lignes de données, soit 178 octets par
      ligne en moyenne, en-tête de 119 octets déduit.
    ⑧ POURQUOI — Le fichier est ouvert avec un réglage de fin de ligne neutre. Sans
      ce réglage, l'écriture d'un CSV sous Windows ajoute un retour chariot en trop
      à chaque ligne, et le fichier relu porte une ligne vide entre chaque ligne de
      données : le compte de lignes relues vaudrait alors le double du compte de
      lignes écrites, et le contrôle de relecture échouerait sans que la cause soit
      visible.
    ⑨ CE QUI CLOCHE — Le dossier de destination n'est pas vérifié, et ce n'est pas
      théorique. Le chemin du fichier de résumé contient toujours un sous-dossier
      `donnees/` que rien ne crée. Mesuré le 19-09-2026 sur un dossier de sortie sans
      ce sous-dossier : le programme écrit d'abord le fichier de détail, puis
      s'arrête ici sur « FileNotFoundError: [Errno 2] No such file or directory ». Il
      laisse alors sur le disque un fichier de détail complet et aucun résumé, sans
      qu'aucun contrôle ne s'exécute — l'état sur lequel le programme s'arrête n'est
      donc ni l'état d'avant ni l'état d'après.
    ⑩ EFFET — ÉCRIT le fichier désigné, en écrasant sans avertissement ce qui portait
      déjà ce nom. N'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main dans le cas normal. PEUT LEVER une erreur non
      rattrapée : `FileNotFoundError` si le dossier n'existe pas,
      `PermissionError` si le fichier n'est pas accessible en écriture, et
      `ValueError` si une ligne porte une clé qui n'est pas dans `champs`. Aucun de
      ses appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le détail : le fichier `registre_experiences.csv`, une ligne par expérience
      le résumé : le fichier `registre_experiences_resume.csv`, une ligne par
        balayage — une série d'essais faits d'un coup sur une même stratégie
    
      un réglage : un des nombres qui définissent une stratégie — l'objectif de gain, la perte acceptée, l'horizon
      une clé : le texte obtenu après rapprochement, qui sert à comparer deux noms et n'est jamais affiché à un lecteur
"""
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=champs)
        w.writeheader()
        for l in lignes:
            w.writerow(l)


def relire_csv(chemin):
    """Relit un fichier CSV qui vient d'être écrit, et rend ses lignes.

    ① RÔLE — Ramener du disque ce qui y a été écrit, pour que le programme puisse
      comparer ce qu'il croit avoir écrit à ce qui s'y trouve réellement. C'est ce
      qui permet au programme de ne présenter aucun travail comme fait tant qu'il ne
      l'a pas revu.
    ② CONTEXTE D'APPEL — `main`, deux fois de suite, juste après l'écriture des deux
      fichiers et avant l'affichage du bilan : une fois sur le détail, une fois sur
      le résumé. Jamais appelée ailleurs.
    ③ ENTRÉE — `chemin` : le chemin du fichier à relire. Un seul appelant, `main`, et
      il passe les deux chemins qu'il vient lui-même de faire écrire.
    ④ CONDITIONS D'ENTRÉE — Le fichier doit exister, être lisible en UTF-8 et porter
      une première ligne d'en-tête nommant ses colonnes.
    ⑤ SORTIE — UNE valeur : une liste de lignes, chacune étant un dictionnaire dont
      les clés sont les noms de colonnes lus dans l'en-tête. Liste vide si le fichier
      ne porte que son en-tête, ce qui est le cas attendu pour le résumé.
      [rend: 1]
    ⑥ TRAITEMENT — ① ouvrir le fichier · ② lire toutes ses lignes en dictionnaires et
      les rendre.
    ⑦ UNITÉ — Un NOMBRE DE LIGNES de données, en-tête non compté : 68 pour le détail
      et 0 pour le résumé le 19-09-2026.
    ⑧ POURQUOI — Relire le disque plutôt que se fier aux lignes gardées en mémoire :
      une écriture peut aller ailleurs que là où on croit, un fichier peut être
      tronqué, et un texte peut changer de forme en traversant l'encodage. Seule la
      relecture rend le fichier tel qu'un autre programme le lira.
      Le fichier est ouvert en `utf-8-sig`, qui retire les trois octets invisibles
      qu'un tableur place en tête d'un CSV. Ces octets, lus autrement, se colleraient
      au nom de la première colonne : `id_exp` ne s'appellerait plus `id_exp`, et la
      comparaison des noms de colonnes échouerait sans que le fichier ait le
      moindre défaut.
    ⑨ CE QUI CLOCHE — La relecture ne peut pas voir un défaut que l'écriture et la
      lecture partagent. Les deux passent par le même outil de lecture-écriture de
      CSV et par le même encodage : un caractère mal encodé à l'écriture est relu de
      la même façon, donc jugé conforme. Le contrôle prouve que le fichier est
      arrivé sur le disque et qu'il porte le bon nombre de lignes ; il ne prouve pas
      que son contenu est juste.
    ⑩ EFFET — LIT le fichier désigné, en entier et en mémoire. N'écrit rien,
      n'affiche rien, ne touche pas au réseau.
    ⑪ TERMINAISON — Rend la main dans le cas normal. PEUT LEVER une erreur non
      rattrapée : `FileNotFoundError` si le fichier a disparu entre son écriture et
      sa relecture, et `UnicodeDecodeError` s'il n'est pas de l'UTF-8. Aucun de ses
      appels ne se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le détail : le fichier `registre_experiences.csv`, une ligne par expérience
      le résumé : le fichier `registre_experiences_resume.csv`, une ligne par
        balayage — une série d'essais faits d'un coup sur une même stratégie
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    """Lit les stratégies, écrit les deux fichiers, les relit, et rend 0 ou 1.

    ① RÔLE — Enchaîner les gestes du programme et refuser de présenter le travail
      comme fait tant que la relecture ne concorde pas. Sans ce refus, un registre
      tronqué ou écrit au mauvais endroit serait annoncé comme construit, et le
      compte des essais reposerait sur un fichier que personne n'a vérifié.
    ② CONTEXTE D'APPEL — Le lancement du programme, et lui seul. Sa valeur de retour
      est passée directement au code de sortie du processus.
    ③ ENTRÉE — Aucun paramètre. Elle lit la ligne de commande : premier argument le
      dossier source, deuxième argument le dossier de sortie, tous deux facultatifs
      et valant le dossier courant s'ils manquent.
    ④ CONDITIONS D'ENTRÉE — Le registre des stratégies doit exister, dans `donnees/`
      sous le dossier source ou à plat dans ce dossier. Le dossier de sortie doit
      déjà porter un sous-dossier `donnees/`.
    ⑤ SORTIE — UNE valeur : un entier. 0 quand les deux fichiers ont été écrits et
      relus conformes, 1 quand le registre des stratégies est introuvable ou quand
      l'un des cinq contrôles de relecture échoue.
      [rend: 1]
    ⑥ TRAITEMENT — ① prendre les deux dossiers sur la ligne de commande et créer le
      dossier de sortie · ② afficher l'heure et les deux dossiers · ③ chercher le
      registre des stratégies d'abord dans `donnees/`, puis à plat · ④ le lire, et
      rendre 1 s'il est introuvable · ⑤ composer une ligne par stratégie · ⑥ écrire
      le fichier de détail · ⑦ écrire le fichier de résumé, vide · ⑧ relire les deux
      fichiers · ⑨ vérifier cinq propriétés : autant de lignes relues qu'écrites au
      détail, aucune ligne au résumé, colonnes du détail conformes à la liste
      attendue, statut historique sur toutes les lignes, et aucune case portant la
      valeur zéro · ⑩ afficher le résultat de chaque contrôle · ⑪ rendre 1 si l'un
      d'eux a échoué · ⑫ afficher la taille des deux fichiers, leur destination et un
      rappel sur la nature des lignes écrites · ⑬ rendre 0.
    une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
    ⑦ UNITÉ — Les lignes se comptent en LIGNES DE DONNÉES, en-tête non compté : 68 au
      détail et 0 au résumé le 19-09-2026. Les tailles s'affichent en OCTETS :
      12 208 pour le détail, 132 pour le résumé, mesurés le même jour. La date
      inscrite dans les lignes s'écrit année-mois-jour, par exemple `2026-09-19`.
    ⑧ POURQUOI — LE REGISTRE DES STRATÉGIES EST CHERCHÉ À DEUX ENDROITS parce que le
      système a déménagé. Le code consigne la correction du 13-09-2026 : ce programme
      ne cherchait qu'à plat et s'arrêtait sur « introuvable », alors que les données
      vivent désormais dans `donnees/`. Le commentaire note que c'était la quatrième
      fois en une journée — après le programme de surveillance quotidienne, celui de
      mesure de la performance, celui qui tient les positions et celui qui fabrique le
      document de pilotage.
      LES CINQ CONTRÔLES PORTENT SUR DES PROPRIÉTÉS ET NON SUR DES NOMBRES ÉCRITS
      D'AVANCE : « autant de lignes relues qu'écrites » vaut quel que soit le nombre
      de stratégies, là où « 68 lignes attendues » deviendrait faux dès la
      soixante-neuvième stratégie et ferait échouer le programme pour une bonne
      raison.
      LE PROGRAMME REND 1 SANS EFFACER LES FICHIERS quand un contrôle échoue, et le
      dit à l'écran : les fichiers restent disponibles pour comprendre ce qui s'est
      passé, mais ne doivent pas être déposés. Effacer ferait disparaître la preuve
      du défaut.
    ⑨ CE QUI CLOCHE — ① Le rappel affiché en fin de passage annonce un nombre faux.
      Il dit « les 61 lignes du detail ne sont PAS des experiences », alors que le
      registre des stratégies en portait 68 le 19-09-2026 et que le programme venait
      d'afficher « lignes ecrites au detail : 68 » quatre lignes plus haut. Le nombre
      est écrit en toutes lettres dans le texte affiché au lieu d'être repris du
      compte réel. Un chiffre qui existe ailleurs ne se recopie pas (R-728, R-708) :
      ici, le même affichage porte deux valeurs contradictoires pour la même chose.
      Le texte en tête du programme porte la même valeur périmée.
      ② Le cinquième contrôle ne peut pas échouer. Il vérifie qu'aucune case `statut`
      ni `resultat` ne vaut exactement `0`. Or le statut est posé à la constante
      HISTORIQUE_NON_COMPTABILISE pour toutes les lignes sans exception, et le
      résultat est composé de morceaux de la forme `n=...` et `wr=...` joints par une
      barre verticale, ou reste vide. Mesuré le 19-09-2026 sur les 68 lignes
      produites : aucune case `statut` ni `resultat` ne vaut `0`, et aucune ne le
      peut par construction. Le contrôle affiche donc « OK » à chaque passage quoi
      qu'il arrive. Une sortie qui reste verte quelle que soit la livraison
      n'apporte rien.
      ③ Le message d'arrêt nomme un chemin qui n'est pas celui qui a échoué. Quand le
      fichier de `donnees/` n'est pas un fichier ordinaire, le programme se rabat sur
      le chemin à plat et n'annonce que celui-là. Mesuré le 19-09-2026 en créant un
      DOSSIER nommé `donnees/cac40_strategies.csv` : le message est « ARRET :
      /tmp/e5/cac40_strategies.csv introuvable. » Le lecteur cherche un fichier à
      l'endroit où il n'a jamais été attendu.
      ④ Un registre de stratégies vide est signalé sous une cause fausse. Mesuré le
      19-09-2026 sur un fichier ne portant que sa ligne d'en-tête : le programme
      écrit un détail de zéro ligne et affiche « colonnes conformes : ECHEC ». Les
      colonnes sont pourtant exactes ; le contrôle échoue seulement parce qu'il
      regarde la première ligne du fichier relu et qu'il n'y en a aucune.
      ⑤ Le fichier de détail est réécrit en entier à chaque passage, sans
      avertissement, et les expériences qu'il porterait seraient perdues. Mesuré le
      19-09-2026 sur une copie du dépôt : le fichier `registre_experiences.csv`
      portait 68 lignes toutes datées du `2026-09-13`, et après un simple relancement
      les 68 lignes portaient la date `2026-09-19`, l'ancien contenu ayant disparu.
      Le nom du programme annonce une construction, pas une reconstruction : rien
      dans son affichage n'avertit qu'un registre déjà rempli va être écrasé.
    ⑩ EFFET — CRÉE le dossier de sortie s'il manque, mais jamais son sous-dossier
      `donnees/`. ÉCRIT deux fichiers en écrasant ce qui portait déjà ces noms, y
      compris quand le contrôle échoue ensuite. LIT le registre des stratégies, puis
      relit les deux fichiers écrits. Affiche une quinzaine de lignes. Aucun accès
      réseau, aucun autre fichier touché.
    ⑪ TERMINAISON — Rend la main avec 0 ou 1 dans les cas prévus. PEUT LEVER une
      erreur non rattrapée, qui arrête alors le programme : quand le dossier de
      sortie ne porte pas de sous-dossier `donnees/`, l'écriture du résumé s'arrête
      sur « FileNotFoundError », mesuré le 19-09-2026, après que le fichier de détail
      a déjà été écrit. Et un de ses appels peut ne pas revenir : `ecrire_csv` et
      `relire_csv` lèvent toutes deux sur un fichier inaccessible.
      [sort: non]
    ⑫ DÉFINITIONS
      le registre des stratégies : le fichier `cac40_strategies.csv`, une ligne par
        stratégie, qui porte leur état civil — identifiant, réglages, résultats
        connus
      le détail : le fichier `registre_experiences.csv`, une ligne par expérience
      le résumé : le fichier `registre_experiences_resume.csv`, une ligne par
        balayage — une série d'essais faits d'un coup sur une même stratégie
      HISTORIQUE_NON_COMPTABILISE : le statut porté par les lignes qui disent qu'on
        ne sait pas combien d'essais ont précédé une stratégie
      le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
        étant qu'une copie de lecture
    """
    src = sys.argv[1] if len(sys.argv) > 1 else "."
    out = sys.argv[2] if len(sys.argv) > 2 else "."
    os.makedirs(out, exist_ok=True)

    print(f"CONSTRUIRE LE REGISTRE DES EXPERIENCES — {horodatage()}")
    print(f"  sources : {os.path.abspath(src)}")
    print(f"  sortie  : {os.path.abspath(out)}")
    print()

    # ---- 1. le detail -----------------------------------------------------
    # LE REGISTRE VIT DANS `donnees/`, PAS A LA RACINE. Corrige le 13-09-2026 :
    # ce programme cherchait a plat et s arretait sur « introuvable ». **Quatrieme
    # occurrence de la meme faute en une journee** — apres le radar, la mesure, le
    # teneur de positions et le pilote. Au depot, les donnees sont rangees ; les
    # programmes ecrits pour le projet, non.
    chemin_strategies = os.path.join(src, "donnees", "cac40_strategies.csv")
    if not os.path.isfile(chemin_strategies):
        chemin_strategies = os.path.join(src, "cac40_strategies.csv")
    strategies = lire_strategies(chemin_strategies)
    if strategies is None:
        print(f"ARRET : {chemin_strategies} introuvable.")
        print("  Le registre n'est pas cree. Rien n'a ete ecrit.")
        return 1

    aujourd_hui = datetime.now(PARIS).strftime("%Y-%m-%d")
    lignes_detail = amorcer_detail(strategies, aujourd_hui)

    chemin_detail = os.path.join(out, NOM_DETAIL)
    ecrire_csv(chemin_detail, CHAMPS_DETAIL, lignes_detail)

    # ---- 2. le resume (vide : aucun balayage n'a encore eu lieu) -----------
    chemin_resume = os.path.join(out, NOM_RESUME)
    ecrire_csv(chemin_resume, CHAMPS_RESUME, [])

    # ---- 3. CALIBRAGE : relire ce qu'on vient d'ecrire ---------------------
    # Tant que ce controle n'est pas passe, rien n'est presente comme fait.
    relu_detail = relire_csv(chemin_detail)
    relu_resume = relire_csv(chemin_resume)

    ok_detail = len(relu_detail) == len(lignes_detail)
    ok_resume = len(relu_resume) == 0
    ok_champs_d = (relu_detail[0].keys() == dict.fromkeys(CHAMPS_DETAIL).keys()) if relu_detail else False
    ok_statut = all(l["statut"] == STATUT_HISTORIQUE for l in relu_detail)
    ok_pas_de_zero = all(l["statut"] != "0" and l["resultat"] != "0" for l in relu_detail)

    print("CALIBRAGE — relecture de ce qui vient d'etre ecrit")
    print(f"  lignes ecrites au detail : {len(lignes_detail)}")
    print(f"  lignes relues au detail  : {len(relu_detail)}   -> {'OK' if ok_detail else 'ECHEC'}")
    print(f"  resume vide (0 balayage) : {len(relu_resume)}   -> {'OK' if ok_resume else 'ECHEC'}")
    print(f"  colonnes conformes       : {'OK' if ok_champs_d else 'ECHEC'}")
    print(f"  statut historique partout: {'OK' if ok_statut else 'ECHEC'}")
    print(f"  aucun zero invente       : {'OK' if ok_pas_de_zero else 'ECHEC'}")
    print()

    if not (ok_detail and ok_resume and ok_champs_d and ok_statut and ok_pas_de_zero):
        print("ARRET : le calibrage a echoue. Les fichiers existent mais NE DOIVENT PAS")
        print("        etre deposes tant que la cause n'est pas trouvee.")
        return 1

    t_d = os.path.getsize(chemin_detail)
    t_r = os.path.getsize(chemin_resume)
    print("CALIBRAGE : OK")
    print(f"  {NOM_DETAIL} : {len(relu_detail)} lignes, {t_d} octets  -> destination GOOGLE DRIVE")
    print(f"  {NOM_RESUME} : {len(relu_resume)} lignes, {t_r} octets  -> destination PROJET")
    print()
    print("RAPPEL : les 61 lignes du detail ne sont PAS des experiences.")
    print("         Ce sont des declarations d'ignorance (HISTORIQUE_NON_COMPTABILISE).")
    print("         Le comptage reel commence a la premiere experience volontaire.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
