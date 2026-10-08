#!/usr/bin/env python3
# verif_backlog.py — v2.2 — Sam 01-08-2026 21h19 (Paris) — ajout du statut « A DECIDER » (proposition non validee par Jean-Luc) — controle du BACKLOG + ACTION CENTER
# NOM FIXE (exception a la regle d horodatage des noms) : ce script est appele par son nom
# par le Chat et par l audit de 22h (A-46). La version vit dans CET en-tete.
# v1 : doublons d'ID, trous de numerotation, renvois obscurs, tampon.
# v2 ajoute : statuts valides · CLOSE sans preuve interdit · vieillissement >14 j ·
#             coherence de la ligne SANTE · date de MAJ presente sur les statuts vivants.
# 30-09-2026 : trois elements en tete de chaque action (R-757 proposee) : ❌ a partir de A-502,
#             ⚠ qui compte les vivantes plus anciennes (fonction trois_elements).
"""Contrôle le tableau des décisions du projet, y pose un tampon horodaté, et rend
un code de sortie.

① RÔLE — Empêcher que la liste des décisions du projet dérive sans que personne
  le voie. Le fichier contrôlé, BACKLOG_DECISIONS.md, est un tableau dont chaque
  ligne porte sept cases : un identifiant de la forme `A-282`, un titre, un
  statut, un responsable, une origine, une décision et une preuve. Ce programme
  relit ce tableau, affiche ce qui ne tient pas, et réécrit en tête du fichier
  une ligne unique — le tampon — qui dit combien d'actions ont été comptées,
  comment elles se répartissent par statut, et à quelle heure la lecture a eu
  lieu. Exemple de tampon produit le 19-09-2026 sur un backlog d'épreuve de
  quatre lignes : « CONTRÔLE AUTOMATIQUE : ÉCHEC — 4 actions au tableau
  (CLOSE 1 · EN COURS 1 · À FAIRE 2) — v2.2 — 19-09-2026 22h34 (Paris) ».
② CONTEXTE D'APPEL — Deux appelants, dont un seul est automatique.
  ① programmes/audit_ecosysteme.py, maillon 16 : il lance ce programme en
  sous-processus sur une COPIE du backlog déposée dans le dossier temporaire du
  système sous le nom `_bl_audit.md`, avec une limite de 60 secondes, puis ne
  retient que le code de sortie, la dernière ligne affichée et les lignes
  d'affichage commençant par ❌ ou ⚠.
  ② Jean-Luc ou le Chat, à la main, sur le vrai fichier.
③ ENTRÉE — La ligne de commande, un seul argument : le chemin du fichier à
  contrôler. Sans argument, le programme prend `/mnt/project/BACKLOG_DECISIONS.md`.
④ CONDITIONS D'ENTRÉE — Le fichier doit exister, se lire en UTF-8, compter au
  moins trois lignes, et être accessible EN ÉCRITURE : ce programme ne fait pas
  que lire, il réécrit le fichier qu'on lui donne.
⑤ SORTIE — Un code de sortie, et rien d'autre : 0 si aucune erreur n'a été
  trouvée, 1 s'il y en a au moins une. Les avertissements ne changent pas ce
  code. Tout le reste est affiché à l'écran.
⑥ TRAITEMENT — ① lire le fichier en entier · ② relever les numéros d'action et
  signaler ceux qui manquent · ③ relever les lignes du tableau et signaler un
  identifiant vu deux fois · ④ comparer deux façons de compter ces lignes ·
  ⑤ contrôler chaque ligne : trois éléments en tête (❌ à partir de A-502, ⚠ compté
  pour une ligne vivante plus ancienne), statut connu, preuve présente si la ligne est
  close, date de mise à jour présente si la ligne est vivante, âge de cette
  date · ⑥ comparer le nombre annoncé par la ligne SANTÉ DU PILOTAGE au nombre
  de lignes réellement trouvées · ⑦ écrire le tampon dans le fichier ·
  ⑧ afficher le verdict, l'unicité du backlog, le tampon, l'empreinte du
  fichier et une question au Chat.
⑦ UNITÉ — Les actions se comptent en LIGNES DE TABLEAU. Le vieillissement se
  compte en JOURS de calendrier, avec un seuil de 14. L'empreinte affichée est
  un nombre hexadécimal de 16 caractères. L'horodatage est en heure de Paris.
⑧ POURQUOI — Deux écrivains touchent le même fichier sans mémoire commune : le
  Chat rédige le backlog pendant une session, Jean-Luc le dépose ensuite, et
  rien ne prouve que le dépôt a pris. Le tampon donne un repère comparable :
  quand Jean-Luc colle la sortie du programme au Chat, le Chat compare le tampon
  affiché au dernier tampon qu'il a lui-même écrit ; s'ils diffèrent, le dépôt
  n'a pas pris. Ce besoin est consigné dans le code sous l'identifiant A-189,
  daté du 12-08-2026.
  Le nom de ce fichier est FIXE, sans horodatage, contrairement à la règle
  d'horodatage des noms du projet, parce que l'audit de 22h l'appelle par son
  nom (A-46) : un nom daté le rendrait introuvable le lendemain. La version vit
  donc dans le commentaire d'en-tête.
⑨ CE QUI CLOCHE —
  ① Le message final ment sur ce qui a été écrit. Quand une erreur est trouvée,
  le programme affiche « NON tamponné OK. » alors qu'il vient d'écrire le tampon
  dans le fichier. Mesuré le 19-09-2026 sur un backlog d'épreuve portant une
  ligne CLOSE sans preuve : la sortie annonce « NON tamponné OK. » et la
  deuxième ligne du fichier porte « CONTRÔLE AUTOMATIQUE : ÉCHEC — 4 actions au
  tableau ». Un lecteur qui croit le message cherche un tampon qui est déjà là.
  ② Le doublon de backlog s'affiche mais ne fait pas rougir. Avec deux fichiers
  voisins dans le même dossier, le programme affiche « ❌ DOUBLON DE BACKLOG —
  2 fichiers » et sort quand même en code 0 : mesuré le 19-09-2026. L'audit de
  22h ne juge son maillon 16 que sur ce code, et n'ajoute à son rapport que les
  lignes commençant par ⚠ : la ligne ❌ disparaît entièrement. Un pas vert sur
  un contrôle qui vient de trouver une faute est un silence.
  ③ La dernière ligne affichée n'est pas un résumé. L'audit prend la dernière
  ligne de l'affichage pour résumé du maillon 16 ; mesuré le 19-09-2026, cette
  dernière ligne est « tampon que tu as toi-même écrit. Divergence = le dépôt
  n'a pas pris. » — un morceau de phrase adressé au Chat, sans aucun chiffre. Le
  compte d'actions est trois lignes plus haut dans l'affichage.
  ④ Le chemin par défaut vise le projet monté, `/mnt/project/BACKLOG_DECISIONS.md`,
  alors que le backlog a quitté le projet pour le dépôt : la fonction
  `chemin_backlog` de programmes/audit_ecosysteme.py cherche au dépôt d'abord et
  ne garde le projet qu'en repli, et son texte date ce déplacement du
  05-09-2026. Un lancement sans argument contrôle donc une copie qui peut être
  en retard, ou rien du tout : le 19-09-2026, `ls /mnt/project` ne trouve aucun
  dossier de ce nom.
  ⑤ La version du programme est écrite à deux endroits : dans le commentaire
  d'en-tête du fichier et dans la chaîne de caractères qui compose le tampon,
  toutes deux à « v2.2 ». Un chiffre qui existe ailleurs ne se recopie pas
  (R-708) : corriger le programme sans toucher la chaîne fait poser un tampon
  qui annonce une version périmée, et personne ne le verra.
⑩ EFFET — RÉÉCRIT le fichier passé en argument à chaque passage, que le contrôle
  réussisse ou échoue, en remplaçant la première ligne de tampon trouvée ou en
  insérant une nouvelle ligne juste après la première ligne du fichier. Aucun
  autre fichier n'est écrit. Aucun accès réseau. Le dossier du fichier est lu
  pour y chercher d'autres backlogs.
⑪ TERMINAISON — SORT DU PROGRAMME avec le code rendu par `main` : 0 si aucune
  erreur, 1 sinon. Et un de ses appels peut ne pas revenir : `main` lève une
  erreur non rattrapée sur un fichier de moins de trois lignes, et sur une date
  de mise à jour du 29 février d'une année non bissextile — les deux mesurés le
  19-09-2026.
⑫ DÉFINITIONS
  le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions et
    des actions du projet
  une action : une ligne de ce tableau, identifiée par `A-` suivi d'un nombre
  le tampon : la ligne d'horodatage posee en tete du backlog par programmes/verif_backlog.py, qui annonce elle-meme un nombre d'actions
  un statut vivant : un statut qui n'est pas terminé — À DÉCIDER, À FAIRE,
    EN COURS ou BLOQUÉE
  l'audit de 22h : programmes/audit_ecosysteme.py, lancé chaque soir, qui
    contrôle l'ensemble du système et délègue le backlog à ce programme
  le Chat : la conversation qui rédige la gouvernance du projet et dépose ses
    versions
  le dépôt : le dépôt GitHub où vivent les fichiers du système, le projet n'en
    étant qu'une copie de lecture
  l'empreinte : le nombre SHA-256 calculé sur le contenu d'un fichier ; deux fichiers de même empreinte ont le même contenu
  le tableau des décisions : le fichier `BACKLOG_DECISIONS.md`, dont chaque ligne porte un identifiant de la forme `A-238`
"""
import re, sys, os
from datetime import datetime, date
from zoneinfo import ZoneInfo

STATUTS={"À DÉCIDER","À FAIRE","EN COURS","BLOQUÉE","CLOSE","RÈGLE","FUSIONNÉE"}
VIVANTS={"À DÉCIDER","À FAIRE","EN COURS","BLOQUÉE"}
AUJ=datetime.now(ZoneInfo("Europe/Paris")).date()
# LES TROIS ÉLÉMENTS EN TÊTE D'UNE ACTION (demande de Jean-Luc du 29-09-2026 à 22h09 ;
# règle R-757 PROPOSÉE, en attente de son oui). À partir de cette action, toute action
# nouvelle doit commencer par eux, sinon ❌ ; les actions vivantes plus anciennes qui
# ne les portent pas sont seulement comptées en ⚠. A-502 est la première écrite ainsi.
PREMIERE_ACTION_A_TROIS_ELEMENTS = 502
TROIS_ELEMENTS = ("**EN BREF** :", "**SI ON LE FAIT** :", "**SI ON NE LE FAIT PAS** :")
MOTS_PAR_ELEMENT = 80   # la consigne d'écriture de la nuit du 30-09 demandait 40 mots au plus ; 80 laisse de la marge sans laisser passer un élément enfoui


def trois_elements(texte):
    """Dit si le texte d'une action commence par ses trois éléments, dans l'ordre.

    ① RÔLE — Reconnaître une action qui porte en tête « EN BREF », « SI ON LE FAIT »
      et « SI ON NE LE FAIT PAS », pour que chacune se comprenne d'un coup d'œil.
    ② CONTEXTE D'APPEL — `main`, une fois par ligne du tableau des décisions.
    ③ ENTRÉE — `texte` : la deuxième case de la ligne, telle qu'elle est écrite.
    ④ CONDITIONS D'ENTRÉE — Aucune : un texte vide rend False.
    ⑤ SORTIE — UNE valeur : True si le texte commence par le premier élément, porte
      les deux autres juste après, dans cet ordre, chacun suivi d'une phrase non vide
      d'au plus MOTS_PAR_ELEMENT mots, la troisième fermée par « — » ; False sinon.
      [rend: 1]
    ⑥ TRAITEMENT — ① vérifier le début · ② chercher chaque élément après le
      précédent, puis le « — » après le troisième · ③ exiger, entre deux bornes, une
      phrase non vide et courte.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Jean-Luc, 29-09-2026 à 22h09 : « trouve le moyen de
      systématiquement ajouter ces trois éléments en en-tête de chaque future
      action ». Un programme le garantit, pas la mémoire (R-754). Exemple réel :
      l'action A-502 commence par « **EN BREF** : ajouter au rituel… ».
    ⑨ CE QUI CLOCHE — Il vérifie la présence et l'ordre des trois étiquettes, pas
      la justesse des phrases qui les suivent. Une ligne dont le texte porte une
      barre verticale entourée d'espaces est vue, mais ses cases sont décalées : ce
      contrôle s'applique encore (il ne lit que le début du texte), mais `main` lit
      mal l'état — ❌ « statut inconnu », et une action ancienne n'est alors pas
      comptée en ⚠ (mesuré le 30-09-2026 : A-435). Une ligne à qui il manque une
      case n'est signalée que par l'écart de comptage. Une ligne dont le début
      s'écarte de la forme exacte (espace manquant après la barre, tabulation)
      n'est vue par rien, pas même l'écart de comptage, dont le motif exige lui
      aussi les espaces (mesuré par le relecteur le 30-09-2026 ; porté par A-503).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    t = (texte or "").strip()
    if not t.startswith(TROIS_ELEMENTS[0]):
        return False
    debuts = []
    pos = 0
    for e in TROIS_ELEMENTS:
        pos = t.find(e, pos)
        if pos < 0:
            return False
        debuts.append(pos)
        pos += len(e)
    fin_tete = t.find(" — ", pos)
    if fin_tete < 0:
        return False
    bornes = debuts[1:] + [fin_tete]
    for e, d, f in zip(TROIS_ELEMENTS, debuts, bornes):
        phrase = t[d + len(e):f].strip()
        # une phrase par élément : non vide, et courte — un élément enfoui loin dans
        # le texte d'origine laisse entre deux étiquettes un long passage
        if not any(c.isalpha() for c in phrase) or len(phrase.split()) > MOTS_PAR_ELEMENT:
            return False
    return True

def controle_unicite(p):
    """Dit s'il existe plus d'un backlog dans le dossier du fichier contrôlé.

    ① RÔLE — Faire voir, dans l'affichage du soir, qu'un second backlog est apparu
      à côté du premier, et nommer celui qui vient d'être lu. Sans ce relevé, deux
      fichiers voisins vivent en parallèle et personne ne sait lequel fait foi.
    ② CONTEXTE D'APPEL — `main`, une seule fois, après l'écriture du tampon et avant
      l'affichage de l'empreinte du fichier. Jamais appelée ailleurs.
    ③ ENTRÉE — `p` : le chemin du fichier backlog. Un seul appelant, `main`, et il
      transmet sans le modifier l'argument reçu sur la ligne de commande, par exemple
      `/mnt/project/BACKLOG_DECISIONS.md` quand le programme est lancé sans argument.
    ④ CONDITIONS D'ENTRÉE — Aucune. Un chemin vide, inexistant ou dont le dossier
      est illisible ne la fait pas tomber.
    ⑤ SORTIE — UNE valeur : une liste de textes à afficher, de trois formes
      différentes. DEUX lignes si plusieurs fichiers ont été trouvés : le constat et
      la consigne. UNE ligne si un seul a été trouvé. Une liste VIDE si aucun n'a été
      trouvé, ou si le dossier n'a pas pu être listé.
      [rend: 1]
    ⑥ TRAITEMENT — ① prendre le dossier du chemin reçu, et le dossier courant si le
      chemin n'en porte pas · ② lister ce dossier, et rendre une liste vide si le
      système refuse · ③ garder les noms qui commencent par BACKLOG_DECISIONS,
      majuscules et minuscules confondues, triés · ④ composer le message selon le
      nombre trouvé.
    ⑦ UNITÉ — Un NOMBRE DE FICHIERS.
    ⑧ POURQUOI — Un dépôt qui répond « garder les deux » crée une seconde copie sous
      un nom voisin : `BACKLOG_DECISIONS (1).md`, `BACKLOG_DECISIONS_2.md`. Les deux
      copies vivent alors ensemble, le Chat écrit dans l'une, l'audit lit l'autre, et
      aucun des deux ne s'en aperçoit. Le projet impose qu'un seul backlog vive, sous
      un nom fixe (A-67), et ce contrôle a été demandé pour cette raison (A-170).
      Afficher le nom du fichier lu sert en plus à rendre la version lisible dans la
      notification du soir, sans avoir à ouvrir le fichier.
    ⑨ CE QUI CLOCHE —
      ① Le contrôle porte sur le DOSSIER, jamais sur le fichier reçu, et son seul
      appelant automatique le met en défaut. L'audit de 22h copie le backlog sous le
      nom `_bl_audit.md` dans le dossier temporaire du système avant de lancer ce
      programme : dans ce dossier, aucun nom ne commence par BACKLOG_DECISIONS, la
      fonction rend une liste vide, et rien du tout ne s'affiche. Mesuré le
      19-09-2026, sur un dossier neuf contenant le seul fichier `_bl_audit.md` :
      l'affichage ne porte ni « Backlog unique » ni « DOUBLON DE BACKLOG ». Le
      contrôle d'unicité ne tourne donc que lors d'un lancement à la main.
      ② Le contrôle épelle un nom au lieu de porter sur une propriété. Un fichier
      d'archive rangé à côté du backlog est compté comme un doublon : avec
      BACKLOG_DECISIONS.md et BACKLOG_DECISIONS_ARCHIVE_2025.md dans le même dossier,
      la sortie mesurée le 19-09-2026 est « ❌ DOUBLON DE BACKLOG — 2 fichiers :
      BACKLOG_DECISIONS.md, BACKLOG_DECISIONS_ARCHIVE_2025.md ». Le critère qui
      tranche tient en une question : si je renomme un fichier, mon contrôle
      change-t-il d'avis ? Ici oui, donc il épelle.
      ③ Le second message dit « Supprimer les autres », alors que rien ne se supprime
      sans validation dans ce projet : une version antérieure se range en archive
      sous un nom qui dit pourquoi elle est tombée.
      ④ Le texte rendu affiche « dans le projet », alors que la fonction n'a regardé
      qu'un seul dossier, celui du fichier reçu. Un second backlog rangé ailleurs ne
      sera jamais vu, et l'affichage « ✅ Backlog unique dans le projet » promet
      pourtant davantage.
    ⑩ EFFET — LIT la liste des noms d'un dossier. N'écrit aucun fichier, ne touche
      pas au réseau, et n'affiche rien elle-même : elle rend des textes que son
      appelant affiche.
    ⑪ TERMINAISON — Rend toujours la main. Elle ne lève pas : l'échec de lecture du
      dossier est rattrapé et rendu sous forme de liste vide. Aucun de ses appels ne
      se termine.
      [sort: non]
    ⑫ DÉFINITIONS
      le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions et
        des actions du projet
      le tampon : la ligne d'horodatage posee en tete du backlog par programmes/verif_backlog.py, qui annonce elle-meme un nombre d'actions
      l'audit de 22h : programmes/audit_ecosysteme.py, lancé chaque soir, qui
        contrôle l'ensemble du système et délègue le backlog à ce programme
      le Chat : la conversation qui rédige la gouvernance du projet et dépose ses
        versions
    
      l'empreinte : le nombre SHA-256 calculé sur le contenu d'un fichier ; deux fichiers de même empreinte ont le même contenu
      le projet : le dossier reçu sur la ligne de commande, celui que le radar examine
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    d = os.path.dirname(os.path.abspath(p)) or "."
    try:
        candidats = sorted(f for f in os.listdir(d)
                           if f.upper().startswith("BACKLOG_DECISIONS"))
    except OSError:
        return []
    msgs = []
    if len(candidats) > 1:
        msgs.append("❌ DOUBLON DE BACKLOG — %d fichiers : %s"
                    % (len(candidats), ", ".join(candidats)))
        msgs.append("   Un seul doit vivre (A-67). Supprimer les autres.")
    elif len(candidats) == 1:
        msgs.append("✅ Backlog unique dans le projet : %s" % candidats[0])
    return msgs

def main(p):
    """Contrôle le backlog, y écrit le tampon, affiche le verdict, rend 0 ou 1.

    ① RÔLE — Réduire l'état d'un tableau de décisions à un seul chiffre que l'audit
      du soir peut juger, et laisser dans le fichier lui-même une trace horodatée de
      ce qui a été compté. Sans ce chiffre, le maillon 16 de l'audit n'aurait rien à
      regarder ; sans le tampon, personne ne saurait quelle version a été lue.
    ② CONTEXTE D'APPEL — Le lancement du programme, et lui seul. Sa valeur de retour
      est passée directement à la sortie du processus.
    ③ ENTRÉE — `p` : le chemin du fichier backlog à contrôler. Un seul appelant, le
      lancement du programme, et il passe le premier argument de la ligne de
      commande, ou `/mnt/project/BACKLOG_DECISIONS.md` quand aucun argument n'est
      donné.
    ④ CONDITIONS D'ENTRÉE — Le fichier doit exister, se lire en UTF-8, compter au
      moins trois lignes, et être accessible en écriture.
    ⑤ SORTIE — UNE valeur : un entier. 0 si la liste des erreurs est vide, 1 sinon.
      Les avertissements, eux, ne changent jamais cette valeur.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire le fichier en entier · ② relever tous les numéros
      d'action du texte et signaler ceux qui manquent entre 1 et le plus grand ·
      ③ relever les lignes complètes du tableau, sept cases, et signaler un
      identifiant vu deux fois · ④ calibrer un motif large sur les identifiants déjà
      relevés puis sur trois identifiants témoins, et comparer le nombre de lignes
      que chaque motif voit · ⑤ pour chaque ligne du tableau : trois éléments en tête
      (❌ à partir de A-502, ⚠ compté pour une ligne vivante plus ancienne), statut connu, preuve
      présente si le statut est CLOSE, date de mise à jour présente si le statut est
      vivant, et plus de 14 jours sans mouvement · ⑥ comparer le nombre annoncé par
      la ligne SANTÉ DU PILOTAGE au nombre de lignes trouvées · ⑦ compter les lignes
      par statut · ⑧ afficher les erreurs puis les avertissements · ⑨ composer le
      tampon et l'écrire dans le fichier, en remplaçant la première ligne de tampon
      trouvée ou en l'insérant en deuxième ligne · ⑩ afficher le bilan, le résultat
      du contrôle d'unicité, le tampon, puis le nom du fichier, son nombre de lignes
      et son empreinte · ⑪ afficher la question au Chat · ⑫ rendre 0 ou 1.
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle a tourné — rapport de boucle, rapport d'audit, cockpit, historique des mesures.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
    ⑦ UNITÉ — Les actions se comptent en LIGNES DE TABLEAU. L'âge d'une action se
      compte en JOURS de calendrier, seuil 14. L'empreinte est un nombre hexadécimal
      de 16 caractères, calculé sur le texte du fichier APRÈS pose du tampon. Les
      dates de mise à jour s'écrivent jour puis mois, sans année. L'horodatage du
      tampon est en heure de Paris.
    ⑧ POURQUOI — Les constats sont rangés en deux tas, les erreurs et les
      avertissements, et seuls les premiers font rougir. Une action vieille de plus
      de 14 jours ou un numéro absent est une information, pas une faute : la monter
      en erreur ferait échouer l'audit tous les soirs pour la même raison, et une
      alerte permanente apprend à ne plus regarder. C'est exactement ce qui s'est
      produit ici, et le code le consigne : l'écart « 383 lignes contre 382 »
      revenait à chaque contrôle depuis des jours, le diagnostic était déjà écrit en
      commentaire dans le fichier, et personne n'avait fait le geste jusqu'au
      13-09-2026.
      La comparaison de deux comptages, plutôt qu'un nombre attendu, vient de la
      règle qui veut qu'un garde-fou porte sur une PROPRIÉTÉ et jamais sur un nombre
      écrit en dur (R-721) : la propriété est ici « deux façons de compter les mêmes
      lignes doivent donner le même nombre ». Et le motif large est calibré avant de
      servir, parce qu'un motif qui ne trouve rien ne prouve rien (R-720).
    ⑨ CE QUI CLOCHE —
      ① Tombe sur un fichier de moins de trois lignes. La troisième ligne du texte
      est lue sans vérifier qu'elle existe, pour y chercher le tampon. Mesuré le
      19-09-2026 sur un fichier de deux lignes : le programme s'arrête sur
      « IndexError: list index out of range », sans avoir écrit le tampon, et
      l'audit range alors son maillon 16 en avertissement « non exécutable » au lieu
      de dire que le backlog est illisible.
      ② Tombe sur une date de mise à jour du 29 février. L'année n'étant pas écrite
      dans le statut, elle est remplacée par l'année en cours ; un statut
      « À FAIRE ·29/02 » construit alors le 29 février 2026, qui n'existe pas.
      Mesuré le 19-09-2026 : « ValueError: day is out of range for month », le
      programme s'arrête et le fichier n'est pas tamponné.
      ③ Une action qui existe est déclarée absente. Le relevé des numéros n'accepte
      que des chiffres après « A- » et exige une fin de mot juste après, donc il ne
      voit pas un identifiant à suffixe ; le relevé des lignes du tableau, lui, les
      accepte. Mesuré le 19-09-2026 sur un tableau portant A-1, A-2bis et A-3 : la
      sortie annonce « 3 actions » et, dans le même affichage, « numéros absents du
      fichier : [2] ». L'action 2 est pourtant là, comptée, sous les yeux du lecteur.
      ④ Le commentaire qui explique la comparaison des comptages décrit un motif qui
      n'existe plus. Il annonce que le motif strict n'accepte que des chiffres après
      « A- », alors que la ligne qui relève les lignes du tableau accepte un suffixe
      de lettres depuis le 13-09-2026, exactement comme le motif large. Les deux
      motifs ne peuvent donc plus diverger sur ce point, et la comparaison ne peut
      plus signaler qu'une ligne de tableau mal formée — ce que son texte ne dit pas.
      ⑤ Les témoins de calibrage sont trois identifiants écrits en dur : A-282,
      A-283 et A-284. Sur un backlog qui ne les porte pas, le programme renonce à
      comparer. Mesuré le 19-09-2026 sur un tableau d'épreuve de trois lignes :
      « ⚠ motif large NON CALIBRE — il ne retrouve pas A-282, A-283, A-284 :
      comparaison des comptes ABANDONNEE ». Un témoin nommé meurt le jour où
      l'action qu'il désigne est renumérotée ou retirée, et le garde-fou s'éteint
      alors sans que rien ne soit cassé.
      ⑥ Un second tampon plus ancien survit. Le remplacement ne touche que la
      PREMIÈRE ligne de tampon rencontrée. Mesuré le 19-09-2026 sur un fichier en
      portant deux : après passage, le fichier porte toujours deux lignes
      « CONTRÔLE AUTOMATIQUE », dont l'ancienne, inchangée, en troisième ligne. Rien
      ne dit au lecteur laquelle fait foi.
      ⑦ Le vieillissement suppose l'année. Une date postérieure à aujourd'hui est
      reculée d'un an, sans autre vérification. Mesuré le 19-09-2026 sur un statut
      « EN COURS ·01/01 » : le programme annonce « sans mouvement depuis >14 j :
      A-284 (261 j) ». Une action réellement mise à jour le 01/01 de l'année
      suivante serait lue comme ayant 261 jours de retard.
      ⑧ Il n'existe aucun mode lecture seule. Le fichier est réécrit à chaque
      passage, même quand rien n'a changé et même quand le contrôle échoue. L'audit
      de 22h s'en protège en copiant le backlog avant de lancer le programme ; un
      lancement à la main, lui, modifie le vrai fichier, et c'est la seule façon de
      savoir ce que le contrôle dirait.
    ⑩ EFFET — RÉÉCRIT entièrement le fichier reçu, succès ou échec, en y posant le
      tampon. LIT le dossier de ce fichier pour y chercher d'autres backlogs.
      Affiche de six à une dizaine de lignes. Aucun autre fichier n'est touché,
      aucun accès réseau.
    ⑪ TERMINAISON — Rend la main avec 0 ou 1 dans le cas normal. PEUT LEVER une
      erreur non rattrapée, qui arrête alors le programme : sur un fichier de moins
      de trois lignes, et sur une date de mise à jour du 29 février d'une année non
      bissextile — les deux mesurés le 19-09-2026. Aucun de ses appels ne se
      termine : `controle_unicite` rend toujours la main.
      [sort: non]
    ⑫ DÉFINITIONS
      le backlog : le fichier BACKLOG_DECISIONS.md, tableau daté des décisions et
        des actions du projet
      une action : une ligne de ce tableau, identifiée par `A-` suivi d'un nombre
      le tampon : la ligne d'horodatage posee en tete du backlog par programmes/verif_backlog.py, qui annonce elle-meme un nombre d'actions
      un statut vivant : un statut qui n'est pas terminé — À DÉCIDER, À FAIRE,
        EN COURS ou BLOQUÉE
      la ligne SANTÉ DU PILOTAGE : une ligne du backlog qui annonce elle-même un
        nombre d'actions, écrite à la main et comparée ici au nombre compté
      l'audit de 22h : programmes/audit_ecosysteme.py, lancé chaque soir, qui
        contrôle l'ensemble du système et délègue le backlog à ce programme
      le Chat : la conversation qui rédige la gouvernance du projet et dépose ses
        versions
    """
    s=open(p,encoding="utf-8").read()
    err=[]; warn=[]
    # ---- v1 : IDs dans tout le fichier ----
    ids=re.findall(r"\bA-(\d+)\b",s)
    nums=sorted({int(x) for x in ids})
    # doublons de LIGNE de tableau
    # LE MOTIF STRICT ACCEPTE LES SUFFIXES, comme le motif large le fait deja.
    # Corrige le 13-09-2026. Le motif n acceptait que des CHIFFRES apres « A- » :
    # `A-23bis` etait INVISIBLE au tampon, et l ecart « 383 lignes contre 382 »
    # revenait a chaque controle depuis des jours. **Une alerte permanente qui
    # n apprend rien apprend a ne plus regarder.** Le fichier portait deja le
    # diagnostic en commentaire ; personne n avait fait le geste.
    rows=re.findall(r"^\| (A-\d+[A-Za-z]*) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|",s,re.M)
    vus={}
    for r in rows:
        if r[0] in vus: err.append(f"doublon au tableau : {r[0]}")
        vus[r[0]]=r
    trous=[n for n in range(1,max(nums)+1) if n not in nums] if nums else []
    if trous: warn.append(f"numéros absents du fichier : {trous}")
    # ═══ A-284 — DEUX COMPTES QUI DOIVENT CONCORDER ═══
    # Le motif de la ligne 43 n'accepte que des CHIFFRES apres « A- » : un identifiant
    # a suffixe alphabetique (A-23bis, meme famille que R-207bis) lui est INVISIBLE,
    # et le tampon sous-compte en silence. Ce bloc SIGNALE l'ecart, il n'ecrit ni ne
    # corrige rien : le tampon reste pose plus bas par le motif STRICT, inchange.
    # R-721 : on controle une PROPRIETE — deux comptes doivent concorder — jamais un
    # nombre ecrit en dur. R-720 : le motif se CALIBRE avant de servir.
    LARGE = r"^\| (A-\d+[A-Za-z]*) \|"
    larges  = re.findall(LARGE, s, re.M)
    stricts = [r[0] for r in rows]
    # calibrage 1 (propriete) : le motif large doit voir TOUT ce que le strict voit
    non_vus = [a for a in stricts if a not in larges]
    # calibrage 2 (temoins) : identifiants dont on SAIT qu'ils existent — R-720
    TEMOINS = ("A-282", "A-283", "A-284")
    temoins_absents = [t for t in TEMOINS if t not in larges]
    if non_vus or temoins_absents:
        warn.append("motif large NON CALIBRE — il ne retrouve pas "
                    + ", ".join(non_vus + temoins_absents)
                    + " : comparaison des comptes ABANDONNEE")
    elif len(larges) != len(stricts):
        invisibles = [a for a in larges if a not in stricts]
        warn.append("ECART DE COMPTAGE : motif large %d lignes, motif strict %d — ecart %d. "
                    "Invisible(s) au tampon : %s"
                    % (len(larges), len(stricts), len(larges) - len(stricts),
                       ", ".join(invisibles) or "non nommable"))
    # ---- v2 : cycle ----
    vieux=[]
    sans_trois=[]
    for aid,titre,st,resp,orig,dec,pr in rows:
        base=st.split("·")[0].strip()
        if not trois_elements(titre):
            if int(re.match(r"A-(\d+)",aid).group(1)) >= PREMIERE_ACTION_A_TROIS_ELEMENTS:
                err.append(f"{aid} : ne commence pas par ses trois éléments EN BREF · SI ON LE FAIT · "
                           f"SI ON NE LE FAIT PAS (R-757, proposée)")
            elif base in VIVANTS:
                sans_trois.append(aid)
        if base not in STATUTS: err.append(f"{aid} : statut inconnu « {st} »")
        if base=="CLOSE" and pr.strip() in ("","—","-"):
            err.append(f"{aid} : CLOSE sans preuve")
        if base in VIVANTS:
            m=re.search(r"·(\d{2})/(\d{2})",st)
            if not m: warn.append(f"{aid} : statut vivant sans date de MAJ")
            else:
                d=date(AUJ.year,int(m.group(2)),int(m.group(1)))
                if d>AUJ: d=date(AUJ.year-1,d.month,d.day)
                if (AUJ-d).days>14: vieux.append(f"{aid} ({(AUJ-d).days} j)")
    if vieux: warn.append("sans mouvement depuis >14 j : "+", ".join(vieux))
    if sans_trois: warn.append(f"{len(sans_trois)} action(s) vivante(s) sans leurs trois éléments en tête : "
                               + ", ".join(sans_trois))
    # sante annoncee vs comptee
    m=re.search(r"SANTÉ DU PILOTAGE : (\d+) actions",s)
    if m and int(m.group(1))!=len(rows):
        err.append(f"ligne SANTÉ ({m.group(1)}) ≠ lignes du tableau ({len(rows)})")
    # ---- verdict + tampon ----
    compte={}
    for r in rows:
        b=r[2].split("·")[0].strip(); compte[b]=compte.get(b,0)+1
    et=" · ".join(f"{k} {v}" for k,v in sorted(compte.items()))
    horo=datetime.now(ZoneInfo("Europe/Paris")).strftime("%d-%m-%Y %Hh%M")
    if err:
        print("ÉCHEC —",len(err),"erreur(s) :")
        for e in err: print("  ❌",e)
    for w in warn: print("  ⚠",w)
    ligne=f"> **CONTRÔLE AUTOMATIQUE : {'OK' if not err else 'ÉCHEC'}** — {len(rows)} actions au tableau ({et}) — v2.2 — {horo} (Paris)"
    s2=re.sub(r"^> \*\*CONTRÔLE AUTOMATIQUE.*$",ligne,s,count=1,flags=re.M)
    if "CONTRÔLE AUTOMATIQUE" not in s2.splitlines()[2] and "CONTRÔLE AUTOMATIQUE" not in s2:
        s2=s.split("\n",1)[0]+"\n"+ligne+"\n"+s.split("\n",1)[1]
    open(p,"w",encoding="utf-8").write(s2)
    print(("OK — fichier tamponné." if not err else "NON tamponné OK."),f"{len(rows)} actions · {et}")
    # A-170 — unicité du backlog + version lisible dans la notification de 22h
    for m in controle_unicite(p): print(m)
    print("TAMPON :", ligne.replace("> **","").replace("**",""))
    # A-189 — carte d'identité du fichier lu + question au Chat (JL, 12/08).
    # But : quand Jean-Luc colle ce résultat au Chat, le Chat compare ce tampon
    # au dernier tampon qu'il a lui-même écrit — deux écrits, aucun souvenir.
    import hashlib
    empreinte = hashlib.sha256(s2.encode("utf-8")).hexdigest()[:16]
    print(f"FICHIER LU : {os.path.basename(p)} · {len(s2.splitlines())} lignes · empreinte {empreinte}")
    print(f"❓ CHAT — j'ai lu le backlog tamponné [{len(rows)} actions · voir date du TAMPON ci-dessus].")
    print("   Est-ce bien la dernière version produite en session ? Compare au dernier")
    print("   tampon que tu as toi-même écrit. Divergence = le dépôt n'a pas pris.")
    return 0 if not err else 1

if __name__=="__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv)>1 else "/mnt/project/BACKLOG_DECISIONS.md"))
