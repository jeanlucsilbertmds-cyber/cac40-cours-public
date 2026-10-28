#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MESSAGE_DU_SOIR — écrit le message unique que Jean-Luc reçoit chaque soir.

① RÔLE — Composer, à partir de ce que le circuit du soir de GitHub a écrit dans le
  dépôt, UN message court : la séance lue, le signal du jour, les positions, les
  trades clos ce soir, et le verdict du radar. Tout ce qui doit alerter vient en
  première ligne : circuit non passé, séance attendue non lue (le dernier jour de
  bourse, week-ends et jours fériés sautés), valeurs sans cours, source illisible, ❌ du
  radar, alerte nouvelle, fin prochaine du calendrier de la Bourse, certification de la
  nuit non déposée.
② CONTEXTE D'APPEL — La tâche planifiée « MESSAGE DU SOIR » (décision de Jean-Luc du
  30-09-2026, 17h34-17h42 : un seul message chaque soir, construit sur ce que fait
  GitHub, testé en forçant le passage) le lance après le circuit de GitHub, puis
  envoie sa sortie en notification. À la main, pour relire la situation du jour.
③ ENTRÉE — `sys.argv[1]` : la racine d'un clone COMPLET du dépôt (avec son historique
  git, pour relire le rapport du radar de la veille). La date du jour est lue à
  l'horloge de Paris, par `CONTRATS_DES_FICHIERS.fabrique_du_jour` pour le rapport.
④ CONDITIONS D'ENTRÉE — La racine doit porter `rapports/audit_du_jour.md`,
  `donnees/signaux_du_jour.json`, `donnees/claude_positions_ouvertes.csv` et
  `donnees/claude_journal_trades.csv` ; `CONTRATS_DES_FICHIERS.py`,
  `CALENDRIER_DE_LA_BOURSE.py` et `FABRIQUER_LE_CIRCUIT_PUBLIC.py` doivent se trouver
  à côté de ce programme ; l'historique git doit être complet (pas un clone superficiel). Un
  fichier absent ou illisible (quelle qu'en soit la raison) n'arrête pas le
  message : il y est nommé en première ligne.
⑤ SORTIE — Le message sur la sortie standard : une première ligne de bilan, coupée à
  200 caractères pour la bannière du téléphone, puis le détail. Code de sortie : 1 si
  une source manquait ou n'était pas lisible (R-734 : un contrôle qui n'a pas pu
  conclure ne rend jamais 0) ; 2 si le circuit du soir n'a pas tourné ou si la
  séance lue n'est pas celle qu'on attend (en retard, postérieure, ou hors jour de
  bourse), ou si le certificat de la nuit n'a pas été déposé ; 0 sinon.
⑥ TRAITEMENT — ① dire si le rapport du radar est du jour (`fabrique_du_jour`) et en
  lire le score, les ❌ et les ⚠️ · ② relire la version précédente du même rapport
  dans l'historique git, pour dire ce qui est nouveau · ③ lire les signaux et
  confronter leurs champs au contrat, et la séance à la séance attendue selon le
  calendrier de la Bourse · ④ lire les positions ouvertes et les trades
  clos à la date de la séance, chacun compté une fois quelle que soit sa comptabilité
  · ④bis lire dans l'historique git le dernier dépôt du certificat de la version par
  son auteur `certification-publique`, et dire s'il est plus ancien que la nuit
  attendue · ⑤ écrire le bilan, puis le détail.
⑦ UNITÉ — Des dates AAAA-MM-JJ, affichées JJ-MM ; des euros pour les trades.
⑧ POURQUOI — Le 30-09-2026, relevé par le Chat : la tâche de 22h ne fait plus
  tourner le radar depuis le 09-09 (clone refusé), et le seul message du soir venait
  d'une boucle Cowork qui refait le travail de GitHub en double. Jean-Luc veut un
  seul endroit : ce message, construit sur le dépôt, que GitHub a écrit.
⑨ CE QUI CLOCHE — ① La publication du cockpit n'est pas vérifiée : le circuit n'en
  garde aucune trace dans le dépôt privé tant que sa modification n'est pas
  fusionnée ; le message le dit. ② La séance attendue vient du calendrier de la Bourse
  (donnees/CALENDRIER_EURONEXT.csv, par programmes/CALENDRIER_DE_LA_BOURSE.py, depuis
  le 30-09-2026) ; il ne couvre que 2026 : trente jours avant la fin, le message le
  dit (⚠️) ; au-delà, il dit le calendrier illisible (code 1) au lieu de deviner. Une
  fermeture exceptionnelle non annoncée n'y figure pas. Tant que le circuit du soir
  n'est pas passé (le matin, ou un soir de panne), la séance de la veille de bourse
  suffit : le retard du jour même est alors dit par « Circuit du soir NON passé ». ③ Deux alertes sont « la même » selon `cle` : un ❌ comparé en entier, un ⚠️
  par son titre, chiffres retirés. ④ La certification est jugée par son FRUIT, le
  certificat déposé, et non par ses causes de panne (superviseurs R-759 du 28-10-2026,
  A-629) : voir `juger_la_certification`. Le réveil de la certification et son délai
  maximal sont lus dans le gabarit de programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, comme
  une donnée, sans exécuter ce programme.
⑩ EFFET — Lit des fichiers et lance `git` en lecture. N'écrit aucun fichier du dépôt ; Python
  peut laisser le cache compilé des modules qu'il importe à côté (`__pycache__`), sauf lancé avec -B.
⑪ TERMINAISON — Sort du programme par `sys.exit`, en 0, 1 ou 2. Chaque appel à `git`
  est borné à 60 secondes.
  [sort: oui]
"""
import csv, importlib.util, json, os, re, subprocess, sys
from datetime import date as _date, datetime, timedelta
from zoneinfo import ZoneInfo

RAPPORT = "rapports/audit_du_jour.md"
SIGNAUX = "donnees/signaux_du_jour.json"
POSITIONS = "donnees/claude_positions_ouvertes.csv"
JOURNAL = "donnees/claude_journal_trades.csv"
CERTIFICAT = "rapports/CERTIFICAT_DE_LA_VERSION.md"
IDENTITE_CERTIFICATION = "certification-publique <certification-publique@users.noreply.github.com>"
# L'identité git du pas « deposer » de la certification, écrite par programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py
# (CERTIFICATION) : épinglée par l'épreuve E52 des épreuves du message, qui rougit si le gabarit change.
BANNIERE = 200


def contrats(racine):
    """Charge programmes/CONTRATS_DES_FICHIERS.py de la racine et rend le module.

    ① RÔLE — Emprunter la date du rapport et les contrats des fichiers là où ils sont
      écrits une fois, jamais les recopier (R-708 : deux implémentations d'une même
      chose divergent toujours). Le module est pris à côté de ce programme, et non
      dans la racine lue : le programme et ses règles voyagent ensemble.
    ② CONTEXTE D'APPEL — `composer`, une fois.
    ③ ENTRÉE — `racine` : le clone lu (non employé : voir le rôle).
    ④ CONDITIONS D'ENTRÉE — CONTRATS_DES_FICHIERS.py doit se trouver dans le même
      dossier que ce programme et s'importer ; sinon l'erreur remonte à `composer`,
      qui le nomme illisible.
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — importer le fichier sous un nom propre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le message juge ce que le circuit a écrit avec les règles du circuit.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Importe un module.
    ⑪ TERMINAISON — Rend la main, ou lève si l'import échoue.
      [sort: non]
    """
    ici = os.path.dirname(os.path.abspath(__file__))
    sp = importlib.util.spec_from_file_location("CONTRATS_message", os.path.join(ici, "CONTRATS_DES_FICHIERS.py"))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def calendrier(racine):
    """Charge le calendrier de la Bourse et rend le module qui l'interroge, avec le calendrier lu.

    ① RÔLE — Dire quelle séance on attend ce soir : le dernier jour de bourse, et non le
      jour du calendrier. Un samedi ou un jour férié, aucune séance n'est due.
    ② CONTEXTE D'APPEL — `composer`, une fois.
    ③ ENTRÉE — `racine` : le clone lu.
    ④ CONDITIONS D'ENTRÉE — programmes/CALENDRIER_DE_LA_BOURSE.py se trouve à côté de ce
      programme. Le fichier donnees/CALENDRIER_EURONEXT.csv est cherché d'abord dans la
      racine lue, puis dans le dépôt d'où vient ce programme (le dossier parent de son
      dossier) : tant que la version en attente n'est pas fusionnée, la version
      officielle ne le porte pas.
    ⑤ SORTIE — TROIS valeurs : le module · le calendrier lu (voir `lire` du module) ·
      d'où il vient, en toutes lettres, pour que le message le dise.
      [rend: 3]
    ⑥ TRAITEMENT — ① importer le module · ② choisir la racine qui porte le fichier ·
      ③ le lire.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Décision de Jean-Luc du 30-09-2026 à 22h32 : reprendre dans GitHub
      l'alerte « séance manquante » et les jours fériés, que seules les boucles Cowork
      avaient (R-758 ; tableau des fonctions, lignes 10.10 et 10.12).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Importe un module, lit un fichier.
    ⑪ TERMINAISON — Rend la main, ou lève (OSError, ValueError, ou toute erreur d'import,
      par exemple AttributeError si le module des contrats voisin ne porte pas le contrat
      CALENDRIER) : `composer` nomme alors le calendrier illisible.
      [sort: non]
    """
    ici = os.path.dirname(os.path.abspath(__file__))
    sp = importlib.util.spec_from_file_location("CALENDRIER_message", os.path.join(ici, "CALENDRIER_DE_LA_BOURSE.py"))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    if os.path.exists(os.path.join(racine, m.FICHIER)):
        base, ou = racine, "dans le dépôt lu"
    else:
        base = os.path.dirname(ici)
        ou = "dans le dépôt du programme (…" + os.path.join(base, m.FICHIER)[-70:] + ")"
    return m, m.lire(base), ou


def lire_rapport(texte):
    """Rend le score et les alertes d'un rapport du radar.

    ① RÔLE — Extraire d'un rapport du radar ce que le message en dit.
    ② CONTEXTE D'APPEL — `composer`, deux fois : le rapport du jour et le précédent.
    ③ ENTRÉE — `texte` : le contenu d'un `rapports/audit_du_jour.md`.
    ④ CONDITIONS D'ENTRÉE — Le rapport porte une ligne « # Score : N ✅ · N ⚠️ · N ❌ » ;
      sinon le score vaut None.
    ⑤ SORTIE — TROIS valeurs : le triplet (✅, ⚠️, ❌) lu dans la ligne de score, ou
      None · la liste des lignes ❌ · la liste des lignes ⚠️.
      [rend: 3]
    ⑥ TRAITEMENT — ① lire les trois nombres de la ligne de score · ② garder les lignes
      qui commencent par ❌ ou ⚠️.
    ⑦ UNITÉ — Des nombres de lignes.
    ⑧ POURQUOI — Comparer le score annoncé aux lignes réellement présentes dit si le
      rapport est entier : un rapport coupé annoncerait des ❌ qu'il ne porte plus.
    ⑨ CE QUI CLOCHE — Une alerte écrite sur deux lignes n'en compte qu'une.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    lignes = texte.splitlines()
    score = None
    for l in lignes:
        m = re.match(r"^#\s*Score\s*:\s*(\d+)\s*✅\s*·\s*(\d+)\s*⚠️\s*·\s*(\d+)\s*❌", l)
        if m:
            score = tuple(int(x) for x in m.groups())
            break
    return score, [l.strip() for l in lignes if l.startswith("❌")], [l.strip() for l in lignes if l.startswith("⚠️")]


def cle(ligne):
    """Rend la forme sous laquelle deux alertes sont dites « la même ».

    ① RÔLE — Comparer une alerte du jour à celles du rapport précédent.
    ② CONTEXTE D'APPEL — `composer`, pour chaque alerte des deux rapports.
    ③ ENTRÉE — `ligne` : une ligne ❌ ou ⚠️ du rapport.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : pour un ❌, la ligne entière ; pour un ⚠️, son maillon et son
      titre (le texte avant le premier « : ») ; chiffres retirés dans les deux cas.
      [rend: 1]
    ⑥ TRAITEMENT — ① pour un ⚠️, couper au premier « : » · ② retirer les chiffres.
    ⑦ UNITÉ — Un texte.
    ⑧ POURQUOI — Un ❌ est comparé en entier : la ligne ❌ du BACKLOG regroupe tous les
      échecs, et un échec de plus doit la rendre nouvelle (relecteur, 30-09-2026). Un ⚠️
      est comparé par son titre : ses listes s'allongent chaque soir (« sans mouvement
      depuis >14 j : A-48 (60 j), … ») sans que l'alerte soit nouvelle — mesuré le
      30-09-2026 entre les rapports du 28 et du 29-09.
    ⑨ CE QUI CLOCHE — Un ⚠️ dont seul le détail, après le titre, change de nature n'est
      pas vu comme nouveau ; un échec du BACKLOG qui ne diffère que par son numéro non
      plus.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    if ligne.startswith("⚠️"):
        ligne = ligne.split(" : ", 1)[0]
    return re.sub(r"\d+", "", ligne)


def lire_git(racine, *args):
    """Lance `git` en lecture dans la racine et rend sa sortie, ou None.

    ① RÔLE — Relire l'historique du dépôt : le rapport du radar de la veille, les passages de la certification.
    ② CONTEXTE D'APPEL — `precedent`, deux fois au plus ; `juger_la_certification`, quatre fois au plus.
    ③ ENTRÉE — `racine` : le clone · `args` : les arguments de `git`.
    ④ CONDITIONS D'ENTRÉE — `git` doit être installé ; la racine doit être un dépôt.
    ⑤ SORTIE — UNE valeur : le texte rendu par `git`, ou None s'il a échoué.
      [rend: 1]
    ⑥ TRAITEMENT — ① lancer `git -C racine args` · ② rendre sa sortie si le code est 0.
    ⑦ UNITÉ — Des SECONDES pour le délai maximal de 60.
    ⑧ POURQUOI — Le rapport est réécrit chaque soir ; seul l'historique garde la veille et les passages.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance un processus en lecture.
    ⑪ TERMINAISON — Rend la main ; un appel qui dépasse 60 secondes rend None.
      [sort: non]
    """
    try:
        p = subprocess.run(["git", "-C", racine, *args], capture_output=True, text=True,
                           errors="replace", timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return p.stdout if p.returncode == 0 else None


def precedent(racine):
    """Rend le texte du rapport du radar tel qu'il était avant sa dernière écriture.

    ① RÔLE — Donner la base de comparaison des alertes « nouvelles ».
    ② CONTEXTE D'APPEL — `composer`, une fois.
    ③ ENTRÉE — `racine` : le clone.
    ④ CONDITIONS D'ENTRÉE — L'historique git doit porter au moins deux versions du
      rapport ; sinon la base est absente.
    ⑤ SORTIE — UNE valeur : le texte de l'avant-dernière version enregistrée, ou None.
      [rend: 1]
    ⑥ TRAITEMENT — ① lister les deux derniers enregistrements qui touchent le rapport ·
      ② lire le rapport au second.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un clone superficiel ou une copie sans `.git` ne garde pas la veille :
      la comparaison est alors impossible, et la première ligne le dit.
    ⑨ CE QUI CLOCHE — Si le circuit a enregistré deux fois le rapport le même soir, la
      « veille » est le premier passage de ce soir-là.
    ⑩ EFFET — Lance `git` en lecture.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    liste = lire_git(racine, "log", "-2", "--format=%H", "--", RAPPORT)
    if not liste or len(liste.split()) < 2:
        return None
    return lire_git(racine, "show", liste.split()[1] + ":" + RAPPORT)


def lire_csv(chemin):
    """Rend les lignes d'un fichier CSV, sous forme de dictionnaires, et ses colonnes.

    ① RÔLE — Lire les positions et le journal des trades.
    ② CONTEXTE D'APPEL — `composer`, deux fois.
    ③ ENTRÉE — `chemin` : le fichier.
    ④ CONDITIONS D'ENTRÉE — Le fichier doit exister, être en UTF-8 et porter une ligne
      d'en-tête ; sinon l'erreur remonte à l'appelant, qui le nomme illisible.
    ⑤ SORTIE — DEUX valeurs : la liste des lignes · la liste des noms de colonnes.
      [rend: 2]
    ⑥ TRAITEMENT — ① ouvrir en UTF-8 avec BOM toléré · ② lire par en-tête.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les colonnes se lisent par leur nom, jamais par leur place, et se
      confrontent au contrat.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main, ou lève si le fichier manque ou n'est pas lisible.
      [sort: non]
    """
    with open(chemin, encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        lignes = list(r)
        return lignes, list(r.fieldnames or [])


def une_fois(lignes, champs):
    """Regroupe les lignes qui décrivent la même opération sous plusieurs comptabilités.

    ① RÔLE — Compter un trade ou une position une seule fois, en nommant ses
      comptabilités (« un jeton », « jetons illimités »).
    ② CONTEXTE D'APPEL — `composer`, deux fois : positions ouvertes, trades clos.
    ③ ENTRÉE — `lignes` : des lignes du fichier · `champs` : les colonnes qui disent
      « la même opération ».
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des couples (première ligne, comptabilités).
      [rend: 1]
    ⑥ TRAITEMENT — regrouper par les champs, dans l'ordre d'apparition.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une même position est écrite une fois par comptabilité : sans ce
      regroupement, un trade réel paraissait quatre fois (relecteur, 30-09-2026).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    groupes = {}
    for l in lignes:
        k = tuple(l.get(c, "") for c in champs)
        groupes.setdefault(k, [l, []])[1].append(l.get("comptabilite") or "?")
    return [(v[0], v[1]) for v in groupes.values()]


def reveil_de_la_certification():
    """Lit le réveil de la certification et son délai maximal là où ils sont écrits, et les rend.

    ① RÔLE — Ne jamais recopier le réveil de la certification (R-708 : deux implémentations d'une même chose
      divergent toujours) : il est écrit une fois, dans le gabarit CERTIFICATION de
      programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, qui fabrique la fiche du dépôt public.
    ② CONTEXTE D'APPEL — `juger_la_certification`, une fois.
    ③ ENTRÉE — Aucune : le fabricant est lu à côté de ce programme.
    ④ CONDITIONS D'ENTRÉE — Le fabricant affecte CERTIFICATION à un texte écrit en dur (seul ou suivi de
      « % … ») ; ce texte porte UNE ligne `cron: "M H * * a-b"` et UNE ligne `timeout-minutes: N`, sous ces
      formes exactes. Toute autre forme lève ValueError, jamais devinée.
    ⑤ SORTIE — CINQ valeurs : la minute et l'heure du réveil en temps universel, le premier et le dernier jour
      de la semaine au sens de cron (0 dimanche … 6 samedi), le délai maximal d'un passage en minutes.
      [rend: 5]
    ⑥ TRAITEMENT — lire le fichier comme du texte ; en tirer l'arbre syntaxique ; prendre le texte affecté à
      CERTIFICATION ; y chercher les deux lignes ; exiger leurs formes strictes.
    ⑦ UNITÉ — Minutes et heures en temps universel ; jours de cron ; minutes pour le délai.
    ⑧ POURQUOI — Superviseur R-759 du 28-10-2026, condition C3 : ne pas recopier le réveil. Relecture du tour
      2, IMP-1 : le fabricant n'est pas exécuté, car un programme importé pourrait écrire à l'écran ou
      arrêter le message ; son texte est lu comme une donnée.
    ⑨ CE QUI CLOCHE — On lit l'intention du dépôt privé, pas la fiche publique qui tourne ; si les deux
      divergent, la certification échoue à son pas « circuit_a_jour », et son dernier passage n'a pas de
      certificat : la règle (a) de `juger_la_certification` le dit.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main, ou lève (OSError, SyntaxError, ValueError).
      [sort: non]
    """
    import ast
    ici = os.path.dirname(os.path.abspath(__file__))
    arbre = ast.parse(open(os.path.join(ici, "FABRIQUER_LE_CIRCUIT_PUBLIC.py"), encoding="utf-8").read())
    valeurs = [n.value for n in arbre.body if isinstance(n, ast.Assign)
               and any(getattr(x, "id", "") == "CERTIFICATION" for x in n.targets)]
    if len(valeurs) != 1:
        raise ValueError(f"réveil de la certification illisible : {len(valeurs)} affectation(s) de CERTIFICATION")
    v = valeurs[0].left if isinstance(valeurs[0], ast.BinOp) else valeurs[0]
    if not (isinstance(v, ast.Constant) and isinstance(v.value, str)):
        raise ValueError("réveil de la certification illisible : CERTIFICATION n'est pas un texte écrit en dur")
    lignes = re.findall(r"cron:[^\n]*", v.value)
    forme = [re.fullmatch(r'cron: "(\d{1,2}) (\d{1,2}) \* \* ([0-6])-([0-6])"', x) for x in lignes]
    if len(lignes) != 1 or not forme[0]:
        raise ValueError(f"réveil de la certification illisible : {lignes!r}"[:150])
    delais = re.findall(r"timeout-minutes: *(\d+) *\n", v.value)
    if len(delais) != 1:
        raise ValueError(f"délai de la certification illisible : {len(delais)} ligne(s) « timeout-minutes »")
    mi, h, a, b = (int(x) for x in forme[0].groups())
    if mi > 59 or h > 23 or a > b:
        raise ValueError(f"réveil de la certification hors bornes : {lignes[0]}")
    return mi, h, a, b, int(delais[0])


def juger_la_certification(racine, maintenant):
    """Juge la certification de la nuit par son fruit, le certificat déposé, et rend ce que le message en dit.

    ① RÔLE — Dire, chaque soir, si la certification a tourné et déposé son certificat. Le 27 et le 28-10-2026,
      elle a refusé de tourner deux nuits de suite sans que personne le sache avant le lendemain midi (A-629).
    ② CONTEXTE D'APPEL — `composer`, une fois.
    ③ ENTRÉE — `racine` : le clone lu, avec son historique · `maintenant` : l'heure de Paris du message.
    ④ CONDITIONS D'ENTRÉE — Un clone COMPLET : un clone superficiel est refusé (voir ⑥ ①).
    ⑤ SORTIE — TROIS valeurs : l'alerte de la bannière ou None · la source illisible ou None · la ligne du
      détail.
      [rend: 3]
    ⑥ TRAITEMENT — ① refuser un clone superficiel : son plus ancien commit n'a pas de parent, git le croit
      auteur de tous les fichiers, et un passage raté semblerait avoir déposé le certificat (relecture du
      28-10-2026, B1) · ② lire le DERNIER commit d'auteur `IDENTITE_CERTIFICATION`, quel que soit le fichier :
      chaque passage qui atteint son pas « deposer » (lancé en `if: always()`) en fait un, même raté ; un
      passage arrêté avant n'en laisse aucun, et la règle (b) le voit · ③ exiger que son
      committer soit le même, sinon il a été recopié ou réécrit ailleurs et sa date ne dit rien · ④ refuser une
      date dans le futur · ⑤ règle (a) : ce commit doit toucher le certificat, sinon le dernier passage n'a rien
      certifié · ⑥ règle (b) : il doit dater d'après le dernier réveil qui a eu le temps de finir (heure du
      réveil plus son délai maximal, avant maintenant, lus par `reveil_de_la_certification`), sinon ce
      réveil n'a rien déposé · ⑦ lire le verdict du certificat ;
      illisible, il rend la source illisible.
    ⑦ UNITÉ — Dates de Paris ; le réveil en temps universel.
    ⑧ POURQUOI — Superviseurs R-759 du 28-10-2026 : juger par le fruit et non par une cause de panne ; règles
      (a) et (b) rejouées sur les soirs du 12 au 28-10 : les alertes tombent le 13, le 14, le 15, le 20, le 27
      et le 28, et nulle part ailleurs.
    ⑨ CE QUI CLOCHE — Un réveil qui n'est pas parti, suivi d'un lancement manuel APRÈS l'heure du réveil, ne se
      voit pas. Un conflit de poussée qui empêche le dépôt du certificat se dit « absente », sans cause. Le
      verdict « VERSION NON CERTIFIÉE » n'alerte pas : décision de Jean-Luc en attente. Un dépôt de la nuit
      retardé par GitHub au-delà de 20h45 le lendemain se dit « absente ».
    ⑩ EFFET — Lance `git` en lecture ; lit le fabricant du circuit public comme une donnée.
    ⑪ TERMINAISON — Rend la main ; chaque appel à `git` est borné à 60 secondes.
      [sort: non]
    """
    if lire_git(racine, "rev-parse", "--is-shallow-repository") != "false\n":
        return None, f"{CERTIFICAT} (clone superficiel ou historique illisible : certification non jugée)", \
            "Certificat de la version : non jugé (clone superficiel ou historique illisible)"
    try:
        mi, h, a, b, delai = reveil_de_la_certification()
    except Exception as e:
        return None, f"programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py ({type(e).__name__}: {e})"[:200], \
            "Certificat de la version : non jugé (réveil de la certification illisible)"
    # le motif d'auteur de git est une expression rationnelle de base : seuls ses caractères spéciaux sont échappés
    motif = "".join("\\" + c if c in ".[]*^$\\" else c for c in IDENTITE_CERTIFICATION)
    trace = lire_git(racine, "log", "-1", "--basic-regexp", "--author=^" + motif + "$", "--format=%H%x09%an <%ae>%x09%cn <%ce>%x09%at")
    if trace is None:
        return None, f"{CERTIFICAT} (historique git illisible : certification non jugée)", \
            "Certificat de la version : non jugé (historique git illisible)"
    # le dernier réveil qui a eu le temps de finir : un jour du réveil, à son heure, plus son délai maximal,
    # avant maintenant (relecture du tour 2, IMP-2 : un réveil du matin ; et le message lancé pendant la nuit)
    jour = maintenant.astimezone(ZoneInfo("UTC")).date()
    while True:
        seuil = datetime(jour.year, jour.month, jour.day, h, mi, tzinfo=ZoneInfo("UTC"))
        if a <= (jour.isoweekday() % 7) <= b and seuil + timedelta(minutes=delai) <= maintenant:
            break
        jour -= timedelta(days=1)
    if not trace.strip():
        return "🚨 Certification absente (aucun passage)", None, \
            "Certificat de la version : aucun passage de la certification dans l'historique"
    sha, auteur, committer, at = trace.strip().split("\t")
    if committer != auteur:
        return None, f"{CERTIFICAT} (dernier passage {sha[:7]} réécrit par {committer} : certification non jugée)"[:200], \
            "Certificat de la version : non jugé (dernier passage recopié ou réécrit)"
    quand = datetime.fromtimestamp(int(at), ZoneInfo("Europe/Paris"))
    if quand > maintenant + timedelta(minutes=10):
        return None, f"{CERTIFICAT} (dernier passage daté du futur : {quand:%d-%m %Hh%M})", \
            "Certificat de la version : non jugé (date dans le futur)"
    touche = lire_git(racine, "show", "--format=", "--name-only", sha)
    if touche is None:
        return None, f"{CERTIFICAT} (historique git illisible : certification non jugée)", \
            "Certificat de la version : non jugé (historique git illisible)"
    if CERTIFICAT not in touche.split("\n"):
        return f"🚨 Certification sans certificat (passage du {quand:%d-%m %Hh%M})", None, \
            f"Certificat de la version : le dernier passage, le {quand:%d-%m à %Hh%M}, n'a déposé que son journal"
    v = re.search(r"^\*\*(VERSION[^*\n]*)\*\*", lire_git(racine, "show", sha + ":" + CERTIFICAT) or "", re.M)
    if not v:
        return None, f"{CERTIFICAT} (verdict illisible au dépôt {sha[:7]})", \
            f"Certificat de la version : déposé le {quand:%d-%m à %Hh%M}, verdict illisible"
    detail = f"Certificat de la version : déposé le {quand:%d-%m à %Hh%M} · {v.group(1).strip()}"
    if quand < seuil:
        return f"🚨 Certification absente (dernier passage {quand:%d-%m})", None, detail
    return None, None, detail


def composer(racine):
    """Compose le message du soir et rend aussi son code de sortie.

    ① RÔLE — Le cœur du programme : tout ce que le message dit vient d'ici.
    ② CONTEXTE D'APPEL — `main`, une fois.
    ③ ENTRÉE — `racine` : le clone.
    ④ CONDITIONS D'ENTRÉE — Voir la fiche du fichier : une source absente est nommée.
    ⑤ SORTIE — DEUX valeurs : le message (texte) · le code de sortie (0, 1 ou 2, voir
      la fiche du fichier).
      [rend: 2]
    ⑥ TRAITEMENT — ① date du rapport par `date_ecrite`, circuit passé ou non par
      `fabrique_du_jour`, score, alertes, et ce qui
      est nouveau · ② signaux, confrontés au contrat · ③ positions et trades, confrontés
      au contrat et comptés une fois · ④bis certification de la nuit, par
      `juger_la_certification` · ④ bilan : ce qui alerte d'abord, l'alerte de la certification
      après celles du radar, coupé à 200 caractères · ⑤ détail.
    ⑦ UNITÉ — Dates AAAA-MM-JJ affichées JJ-MM ; euros pour les trades.
    ⑧ POURQUOI — Un seul message, qui commence par ce qui doit alerter.
    ⑨ CE QUI CLOCHE — Voir la fiche du fichier.
    ⑩ EFFET — Lit des fichiers et l'historique git.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    jj = lambda d: f"{d[8:10]}-{d[5:7]}" if isinstance(d, str) and len(d) == 10 else "?"
    aujourd_hui = datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d")
    illisibles, alertes, detail = [], [], []
    # ① le radar
    C = None
    try:
        C = contrats(racine)
    except Exception as e:
        illisibles.append(f"programmes/CONTRATS_DES_FICHIERS.py ({type(e).__name__})")
    score, rouges, oranges, date_rap = None, [], [], None
    try:
        texte = open(os.path.join(racine, RAPPORT), encoding="utf-8").read()
        score, rouges, oranges = lire_rapport(texte)
        # LA DATE DU RAPPORT se lit là où le circuit la lit (R-708, 01-10-2026) : une
        # recherche écrite ici prenait la première date de la première ligne.
        if C is not None:
            date_rap = C.date_ecrite(racine, RAPPORT, next(x[1] for x in C.FABRIQUES_DU_SOIR if x[0] == RAPPORT))[0]   # la date seule
        if score is None:
            illisibles.append(RAPPORT + " (score illisible)")
        elif score[1] != len(oranges) or score[2] != len(rouges):
            illisibles.append(f"{RAPPORT} (coupé : score {score[1]} ⚠️ · {score[2]} ❌, lignes {len(oranges)} ⚠️ · {len(rouges)} ❌)")
    except Exception as e:
        illisibles.append(f"{RAPPORT} ({type(e).__name__})")
    passe = False
    if C is not None:
        try:
            ch, motif, quoi = next(x for x in C.FABRIQUES_DU_SOIR if x[0] == RAPPORT)
            passe = C.fabrique_du_jour(racine, ch, motif, quoi) is None
        except Exception as e:
            illisibles.append(f"date du rapport ({type(e).__name__})")
    if not passe:
        alertes.append(f"🚨 Circuit du soir NON passé (dernier radar du {jj(date_rap)})")
    avant = precedent(racine)
    cles_avant = None
    if avant is not None:
        _s, r0, o0 = lire_rapport(avant)
        cles_avant = {cle(x) for x in r0 + o0}
    else:
        alertes.append("⚠️ veille non relue : rien n'est dit nouveau")
    nouv_r = [x for x in rouges if cles_avant is not None and cle(x) not in cles_avant]
    nouv_o = [x for x in oranges if cles_avant is not None and cle(x) not in cles_avant]
    # ② les signaux
    seance, signaux, manquantes, seance_d = None, [], [], None
    try:
        s = json.load(open(os.path.join(racine, SIGNAUX), encoding="utf-8"))
        if not isinstance(s, dict) or not isinstance(s.get("signaux", []), list):
            raise ValueError("forme inattendue")
        seance, signaux = s.get("seance"), s.get("signaux") or []
        manquantes = s.get("valeurs_sans_cette_seance") or []
        # LES CLÉS DU FICHIER, et non une liste écrite ici (relecteur, 30-09-2026) : un
        # fichier privé de « signaux » passait pour un soir sans signal.
        ec = [f"« {k} » absent" for k in ("seance", "signaux", "valeurs_sans_cette_seance") if k not in s]
        # LA SÉANCE SE LIT ICI, et non dans le calendrier (relecteur, 30-09-2026) : une
        # séance « 2026-02-30 » faisait dire le CALENDRIER illisible.
        try:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(seance)):
                raise ValueError
            seance_d = _date.fromisoformat(seance)
        except ValueError:
            seance_d = None
            if "seance" in s:
                ec.append(f"« seance » illisible : {str(seance)[:20]}")
        if C is not None:
            ec += C.verifier("SIGNAUX_DU_JOUR", list(s.keys()), "LU")
            for x in signaux:
                ec += C.verifier("SIGNAL", list(x.keys()), "LU") if isinstance(x, dict) else ["signal illisible"]
                if isinstance(x, dict) and "valeur" not in x:
                    ec.append("signal sans « valeur »")
        if ec:
            illisibles.append(SIGNAUX + " (" + " ; ".join(ec) + ")")
    except Exception as e:
        illisibles.append(f"{SIGNAUX} ({type(e).__name__})")
    # LA SÉANCE ATTENDUE vient du calendrier de la Bourse : un samedi ou un jour férié,
    # c'est la dernière séance ouvrée (30-09-2026). Tant que le circuit du soir n'est pas
    # passé, la séance de la veille de bourse suffit (`plancher`) : le matin, rien ne
    # manque encore. Sans calendrier, la séance attendue est INCONNUE : le calendrier est
    # nommé illisible, et aucune séance n'est devinée.
    attendue, plancher, sans_bourse, ou_cal, K, cal, fin_cal = None, None, False, None, None, None, False
    _auj = _date.fromisoformat(aujourd_hui)
    try:
        K, cal, ou_cal = calendrier(racine)
        attendue = K.dernier_jour_de_bourse(_auj, cal)
        veille_de_bourse = K.dernier_jour_de_bourse(_auj - timedelta(days=1), cal)
        plancher = attendue if passe else veille_de_bourse
        sans_bourse = not K.est_jour_de_bourse(_auj, cal)
    except Exception as e:
        # Le chemin d'un fichier absent se coupe par la FIN : c'est là qu'est le nom.
        quoi = f"{e.strerror} — …{str(e.filename)[-80:]}" if isinstance(e, OSError) else str(e)
        illisibles.append(f"donnees/CALENDRIER_EURONEXT.csv ({type(e).__name__}: {quoi})"[:200])
        K = None
    alerte_seance = False
    if K is not None and seance_d is not None:
        if seance_d > attendue:
            alerte_seance = True
            alertes.append(f"🚨 Séance lue du {jj(seance)} POSTÉRIEURE à la séance attendue du {jj(attendue.isoformat())}")
        elif seance_d >= cal["depuis"] and not K.est_jour_de_bourse(seance_d, cal):
            alerte_seance = True
            alertes.append(f"🚨 Séance lue du {jj(seance)} : ce n'est pas un jour de bourse"
                           + (f" — {K.jours_de_bourse_apres(seance_d, plancher, cal)} jour(s) de bourse de retard"
                              f" sur la séance du {jj(plancher.isoformat())}" if seance_d < plancher else ""))
        elif seance_d < plancher:
            alerte_seance = True
            if seance_d >= cal["depuis"]:
                retard = str(K.jours_de_bourse_apres(seance_d, plancher, cal))
            else:   # avant la couverture : on compte ce qu'on sait, et on le dit
                retard = "au moins " + str(K.jours_de_bourse_apres(cal["depuis"] - timedelta(days=1), plancher, cal))
            alertes.append(f"🚨 Séance du {jj(plancher.isoformat())} NON lue"
                           + f" — {retard} jour(s) de bourse de retard"
                           + f" (dernière : {jj(seance)})")
    if K is not None and (cal["jusqu_au"] - _auj).days < 30:
        # COURT dans la bannière (relecteur, 30-09-2026) : la phrase longue faisait passer la
        # séance au-delà des 200 caractères les soirs chargés ; la phrase entière est au détail.
        alertes.append(f"⚠️ Calendrier de la Bourse à relever (fin {jj(cal['jusqu_au'].isoformat())})")
        fin_cal = True
    if manquantes:
        alertes.append(f"⚠️ {len(manquantes)} valeur(s) sans la séance")
    # ③ positions ouvertes et trades clos, chacun compté une fois
    ouvertes, clos = [], []
    try:
        lignes, cols = lire_csv(os.path.join(racine, POSITIONS))
        if C is not None and C.verifier("POSITION", cols, "LU"):
            raise ValueError("colonnes hors contrat : " + " ; ".join(C.verifier("POSITION", cols, "LU")))
        ouvertes = une_fois(lignes, ("strategie", "valeur", "date_entree"))
    except Exception as e:
        illisibles.append(f"{POSITIONS} ({type(e).__name__}: {e})"[:160])
    try:
        lignes, cols = lire_csv(os.path.join(racine, JOURNAL))
        if C is not None and C.verifier("TRADE", cols, "LU"):
            raise ValueError("colonnes hors contrat : " + " ; ".join(C.verifier("TRADE", cols, "LU")))
        clos = une_fois([t for t in lignes if seance and t.get("date_sortie") == seance],
                        ("strategie", "valeur", "date_entree", "date_sortie"))
    except Exception as e:
        illisibles.append(f"{JOURNAL} ({type(e).__name__}: {e})"[:160])
    # ④bis la certification de la nuit, jugée par son fruit (A-629)
    alerte_certif, ill_certif, ligne_certif = juger_la_certification(
        racine, datetime.now(ZoneInfo("Europe/Paris")))
    if ill_certif:
        illisibles.append(ill_certif)
    # ④ le bilan : ce qui alerte d'abord
    if illisibles:
        alertes.insert(0, f"🚨 Message incomplet : {len(illisibles)} source(s) illisible(s)")
    if nouv_r:
        alertes.append(f"🚨 {len(nouv_r)} ❌ nouveau(x) au radar")
    if nouv_o:
        alertes.append(f"⚠️ {len(nouv_o)} ⚠️ nouveau(x) au radar")
    connus = len(rouges) - len(nouv_r)
    if connus and cles_avant is None:
        alertes.append(f"🚨 {connus} ❌ au radar, veille non relue")   # « connu » serait faux
    elif connus:
        alertes.append(f"⚠️ {connus} ❌ connu(s) au radar")
    if alerte_certif:   # après le radar : la bannière garde d'abord ce qui touche la séance et le radar
        alertes.append(alerte_certif)
    sig = "aucun signal" if not signaux else f"{len(signaux)} signal(s) : " + ", ".join(str(x.get("valeur", "?")) for x in signaux if isinstance(x, dict))
    etat = f"séance {jj(seance if seance_d else None)} · {sig} · {len(ouvertes)} position(s) ouverte(s)"
    tete = "🚨" if any(a.startswith("🚨") for a in alertes) else ("⚠️" if alertes else "✅")
    bilan = f"{tete} Soir du {jj(aujourd_hui)} · " + (" · ".join(a[2:].strip() for a in alertes) + " · " if alertes else "rien à signaler · ") + etat
    if len(bilan) > BANNIERE:
        bilan = bilan[:BANNIERE - 1] + "…"
    # ⑤ le détail
    if sans_bourse:
        detail.append(f"Pas de bourse aujourd'hui (week-end ou jour férié) : séance attendue {jj(attendue.isoformat())}")
    detail.append(f"Séance lue : {jj(seance if seance_d else None)}" + (f" · valeurs sans cette séance : {', '.join(map(str, manquantes))}" if manquantes else ""))
    detail.append("Signal du jour : " + ("aucun" if not signaux else " ; ".join(
        f"{x.get('valeur', '?')} (clôture {x.get('close', '?')})" for x in signaux if isinstance(x, dict))))
    detail.append(f"Positions ouvertes : {len(ouvertes)}" + ("" if not ouvertes else " — " + " ; ".join(
        f"{p.get('valeur', '?')} ({p.get('strategie', '?')} · {', '.join(cs)})" for p, cs in ouvertes)))
    detail.append(f"Trades clos ce soir : {len(clos)}" + ("" if not clos else " — " + " ; ".join(
        f"{t.get('valeur', '?')} {t.get('motif_sortie', '?')} {t.get('pnl_net_eur', '?')} € ({t.get('strategie', '?')} · {', '.join(cs)})" for t, cs in clos)))
    detail.append(f"Radar du {jj(date_rap)} : " + (f"{score[0]} ✅ · {score[1]} ⚠️ · {score[2]} ❌" if score else "score illisible"))
    for x in rouges:   # un ❌ nouveau s'écrit en entier : ce qui est nouveau peut être en fin de ligne
        detail.append("  NOUVEAU " + x if x in nouv_r else "  " + x[:160])
    for x in nouv_o:
        detail.append("  NOUVEAU " + x)
    detail.append(ligne_certif)
    detail.append("Cockpit : publication pas encore vérifiée par ce message.")
    if K is None:
        detail.append("Séance attendue : inconnue (calendrier de la Bourse illisible)")
    else:
        detail.append(f"Calendrier de la Bourse lu {ou_cal}, couvert du {jj(cal['depuis'].isoformat())}-{cal['depuis'].year}"
                      f" au {jj(cal['jusqu_au'].isoformat())}-{cal['jusqu_au'].year}")
        if fin_cal:
            detail.append("  Au-delà de cette date, le message dira le calendrier illisible : relever l'année suivante sur la"
                          " page officielle d'Euronext et ÉTENDRE le fichier (ne jamais le remplacer).")
    for x in illisibles:
        detail.append("Illisible : " + x)
    code = 1 if illisibles else (2 if (not passe or alerte_seance or alerte_certif is not None) else 0)
    return bilan + "\n" + "\n".join(detail), code


def main():
    """Lance la composition sur la racine donnée et affiche le message.

    ① RÔLE — Point d'entrée du programme.
    ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — `sys.argv[1]` : la racine du clone.
    ④ CONDITIONS D'ENTRÉE — Un argument ; sinon le mode d'emploi, et code 1.
    ⑤ SORTIE — Ne rend rien : sort par sys.exit.
      [rend: rien]
    ⑥ TRAITEMENT — ① lire l'argument · ② composer · ③ afficher · ④ sortir.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le code de sortie dit ce que le message dit, pour un programme qui le
      lirait sans lire le texte.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Affiche le message.
    ⑪ TERMINAISON — Sort du programme par `sys.exit`.
      [sort: oui]
    """
    if len(sys.argv) < 2:
        print("usage : python3 programmes/MESSAGE_DU_SOIR.py <racine du dépôt>")
        sys.exit(1)
    message, code = composer(sys.argv[1])
    print(message)
    sys.exit(code)


if __name__ == "__main__":
    main()
