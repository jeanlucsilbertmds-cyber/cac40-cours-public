#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DÉCLARER UNE STRATÉGIE — écrire, en ajout seul, la déclaration datée d'une stratégie AVANT qu'on regarde ses années
d'examen, et dire quelle déclaration était ENGAGÉE au dépôt avant un regard. Simulation uniquement.

LE SENS EN TÊTE — R-505 ① : « Exiger la déclaration datée, écrite avant le regard, sinon rendre NON JUGEABLE en nommant
le champ qui manque ». Un seuil, un découpage ou un univers choisi après avoir vu le résultat ne protège de rien :
regarder chaque soir et s'arrêter dès que c'est bon fait passer une stratégie sans valeur environ 27 fois sur 100
(grille, Q2). La déclaration vit dans `donnees/DECLARATIONS_DATEES.csv` (contrat DECLARATION_DATEE de
`programmes/CONTRATS_DES_FICHIERS.py`, gelé). Ce programme en est l'écrivain : il n'ajoute qu'une ligne complète, sans
jamais toucher aux lignes déjà écrites, et il dit si une déclaration avait été COMMITÉE avant le regard — la date
qu'une ligne déclare ne suffit pas, puisqu'on peut l'écrire après coup.

① RÔLE — `ajouter_une_declaration` : ajouter une ligne au fichier, refusée si elle est incomplète, mal datée ou si
  le fichier a été réécrit ; `empreintes_du_code` : calculer les deux empreintes « sans textes » que la déclaration
  fixe ; `declaration_engagee` : la déclaration qui fait foi pour le regard, celle que portait la branche
  principale au commit que le premier regard a vu en naissant (jamais par les dates).
  Mission B3 du plan V7 (11-11-2026, découpe du lot B par le superviseur R-759 de 22h19, point 5) :
  `preparer_une_declaration` calcule la date et les empreintes (R-728) ; `lire_la_declaration` est LA lecture
  contrôlée que le juge appelle, qui rend la liste des champs en défaut CALCULÉE, jamais reçue de l'appelant ;
  `defauts_par_champ` est la seule définition d'un champ en défaut, partagée par l'écriture et la lecture.
② CONTEXTE D'APPEL — Au 11-11-2026 : les épreuves `tests/EPREUVES_B_DU_BLOC_5A_Mer_11-11-2026.py` et
  `tests/EPREUVES_B3_DECLARATION_Mer_11-11-2026.py`. Destiné au Chat, qui prépare une déclaration, Jean-Luc la
  confirmant (DÉL-D21), et à la porte du juge (agent J), qui appelle `lire_la_declaration`.
③ ENTRÉE — Ligne de commande : `python3 programmes/DECLARER_UNE_STRATEGIE.py <racine> --controler` contrôle le fichier.
④ CONDITIONS D'ENTRÉE — `programmes/CONTRATS_DES_FICHIERS.py` voisin ; `emp.py` à la racine du dépôt ; git pour la
  déclaration engagée.
⑤ SORTIE — Ligne de commande : code 0 si le fichier tient son contrat et que chaque ligne est complète, 1 sinon, 2 si
  l'usage est faux.
⑥ TRAITEMENT — Définir les fonctions ; en ligne de commande, `main`.
⑦ UNITÉ — Des lignes du fichier ; des instants en heure de Paris avec leur décalage.
⑧ POURQUOI — `CONTRATS_DES_FICHIERS.declaration_de_la_fiche` lit la date que la ligne DÉCLARE et dit lui-même (⑨ ①)
  que rien ne la confronte à la date du commit qui l'a ajoutée. `declaration_engagee` comble ce manque, sans
  dupliquer la lecture : elle appelle cette fonction sur le fichier tel que la branche principale le portait au
  commit inscrit par le premier regard (décision de Jean-Luc du 12-11-2026 à 09h04, « Reparer » ; superviseur
  ANCRAGE du 12-11-2026). LIMITE J1 : l'erreur d'un agent, pas un faussaire (décision de Jean-Luc du 12-11-2026 à
  08h58, « 1 · Empêcher l'erreur (recommandé) », BACKLOG A-708).
⑨ CE QUI CLOCHE — ① Le sens d'une case remplie n'est pas jugé (une hypothèse d'un mot passe) : c'est le travail du
  relecteur des déclarations ; seule la forme l'est (`defauts_par_champ`). ④ `reglages`, `bareme` et `temoins` se
  saisissent encore et ne sont confrontés à rien de calculé (questions de la note B3). ③ `ajouter_une_declaration` réécrit le fichier entier (« wb ») avant de le relire :
  un ajout en mode « ab » serait plus sûr (BACKLOG, point 7 du relecteur). ② Le fichier ne porte aucune ligne au 11-11-2026 : la déclaration de C5 attend la
  confirmation de Jean-Luc (DÉL-D21), ce programme ne l'écrit pas.
⑩ EFFET — `ajouter_une_declaration` AJOUTE une ligne au fichier ; le reste lit, ou lance git en lecture.
⑪ TERMINAISON — En ligne de commande, sort avec 0, 1 ou 2. Un appel à git peut ne pas revenir.
⑫ DÉFINITIONS
  la déclaration datée : le texte, écrit et daté avant de regarder, qui fixe tout ce qui sera jugé (R-505, LES MOTS)
  le regard : le moment où les années d'examen d'une stratégie sont jouées pour la juger (R-505 ③)
  engagée : présente sur la branche principale au commit que le premier regard a vu
  la racine : le dossier du dépôt, ou d'une copie qui en garde l'arborescence
"""

import csv
import io
import json
import os
import shutil
import sys
from datetime import datetime

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)
import CONTRATS_DES_FICHIERS as C  # noqa: E402
import TENIR_LE_REGISTRE_DES_ESSAIS as T  # noqa: E402


def empreintes_du_code(racine, chemin_signal):
    """Rend l'empreinte, sans ses textes, du code du juge et de celle du module de signal d'une fiche.

    ① RÔLE — Remplir `empreinte_code_juge` et `empreinte_code_signal` (contrat : « la règle figée : l'empreinte du code
      du juge… et celle du code du signal (sans ses textes) »).
    ② CONTEXTE D'APPEL — Le Chat, en préparant une déclaration ; l'épreuve de B.
    ③ ENTRÉE — `racine` · `chemin_signal` : la case `module_signal` de la fiche, relative à la racine.
    ④ CONDITIONS D'ENTRÉE — `<racine>/emp.py` et les deux fichiers existent.
    ⑤ SORTIE — DEUX valeurs : l'empreinte du juge et celle du signal, 16 caractères chacune.
      [rend: 2]
    ⑥ TRAITEMENT — charger `emp.py` de la racine, appliquer `empreinte` aux deux sources.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — `emp.py` sert déjà de preuve dans les livraisons (`LIRE_LE_CODE.empreinte_du_code`) : une seconde
      façon de calculer divergerait (R-708). Sans les textes : une fiche explicative corrigée ne change pas la règle.
    ⑨ CE QUI CLOCHE — Le juge importe d'autres modules (jugement, positions) : leur changement ne change pas cette
      empreinte.
    ⑩ EFFET — Lit deux fichiers.
    ⑪ TERMINAISON — Rend la main ; lève FileNotFoundError.
      [sort: non]
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location("emp_de_la_racine", os.path.join(racine, "emp.py"))
    emp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(emp)
    with open(os.path.join(racine, "programmes", "JUGE_DES_STRATEGIES.py"), encoding="utf-8") as f:
        juge = emp.empreinte(f.read())
    with open(os.path.join(racine, chemin_signal), encoding="utf-8") as f:
        signal = emp.empreinte(f.read())
    return juge, signal


def defauts_par_champ(ligne):
    """Nomme, champ par champ, ce qui empêche une ligne d'être une déclaration datée complète et bien formée.

    ① RÔLE — LA définition, en un seul endroit, d'un champ « en défaut » : l'écrivain (`defauts_d_une_declaration`,
      donc `ajouter_une_declaration` et `preparer_une_declaration`) et le lecteur (`lire_la_declaration`) l'appellent
      tous deux, pour qu'une ligne refusée à l'écriture le soit aussi à la lecture, et inversement (R-708 : deux
      implémentations d'une même chose divergent toujours).
    ② CONTEXTE D'APPEL — `defauts_d_une_declaration` ; `lire_la_declaration`. Mission B3 du plan V7, 11-11-2026.
    ③ ENTRÉE — `ligne` : un dictionnaire {champ : texte}, ou None (aucune déclaration).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire {champ de DECLARATION_DATEE : raison}, dans l'ordre du contrat ; vide si
      la ligne est complète et bien formée. None rend chaque champ exigé avec la raison « aucune déclaration ».
      Exemple : une ligne dont `lignee` est vide et `parametres_libres` vaut « deux » rend {"lignee": "vide",
      "parametres_libres": "« deux » n'est pas un entier ≥ 0"}.
      [rend: 1]
    ⑥ TRAITEMENT — ① les champs manquants, par `CONTRATS_DES_FICHIERS.champs_de_la_declaration_manquants` (la seule
      définition de « manquant » ; `cas` hors de CAS_DE_LA_LOI y compte) · ② `date_declaration` lisible AVEC son
      décalage · ③ `reglages` objet JSON · ④ `parametres_libres` entier ≥ 0, en chiffres · ⑤ `date_regle_univers`
      AAAA-MM-JJ, et pas postérieure au jour de `date_declaration` · ⑥ aucune case ne contient de saut de ligne.
      Un champ manquant garde la raison « vide » et n'est pas contrôlé plus loin.
    ⑦ UNITÉ — Des noms de champs et des phrases.
    ⑧ POURQUOI — R-505 ① : « Exiger la déclaration datée, écrite avant le regard, sinon rendre NON JUGEABLE en
      nommant le champ qui manque ». Une case remplie de travers (« deux » réglages libres, une règle d'univers datée
      après la déclaration qui la fixe) n'est pas plus une déclaration qu'une case vide : la lecture la plus stricte
      la traite comme un champ en défaut (lecture de la mission B3, à confirmer par Jean-Luc ; la règle la plus
      stricte prime). Un saut de ligne casserait le compte par lignes du fichier.
    ⑨ CE QUI CLOCHE — ① Le SENS d'une case remplie n'est pas jugé (une hypothèse d'un mot passe) : c'est le travail
      du relecteur des déclarations. ② `annees_d_examen` et `epoques` ne sont pas lues ici : `MODULE_JUGEMENT.
      lire_les_epoques` les lit et rend « NON JUGEABLE — annees_d_examen / epoques » ; les relire ici en ferait une
      seconde lecture (R-708). ③ `temoins` n'est pas contrôlé : `JUGE_DES_STRATEGIES.k_a_la_date` n'admet que
      « aucun » ou un entier, le contrat dit « les témoins déclarés » — question laissée au Chat (note B3).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import re
    from datetime import date
    if ligne is None:
        return {c: "aucune déclaration" for c in C.champs_de_la_declaration_manquants(None)}
    defauts = {}
    for c in C.champs_de_la_declaration_manquants(ligne):
        defauts[c] = "vide" if not (ligne.get(c) or "").strip() else "%r hors de %s" % (ligne.get(c), C.CAS_DE_LA_LOI)
    jour = None
    if "date_declaration" not in defauts:
        try:
            d = datetime.fromisoformat(ligne["date_declaration"].strip())
            if d.tzinfo is None:
                defauts["date_declaration"] = "sans décalage horaire"
            else:
                jour = d.date()
        except ValueError:
            defauts["date_declaration"] = "illisible : %r" % ligne["date_declaration"]
    if "reglages" not in defauts:
        try:
            if not isinstance(json.loads(ligne["reglages"]), dict):
                defauts["reglages"] = "pas un objet JSON"
        except ValueError:
            defauts["reglages"] = "JSON illisible"
    if "parametres_libres" not in defauts and not re.fullmatch(r"[0-9]+", ligne["parametres_libres"].strip()):
        defauts["parametres_libres"] = "%r n'est pas un entier ≥ 0" % ligne["parametres_libres"]
    if "date_regle_univers" not in defauts:
        try:
            du = date.fromisoformat(ligne["date_regle_univers"].strip())
            if jour is not None and du > jour:
                defauts["date_regle_univers"] = ("%s, postérieure à la déclaration du %s : la règle d'univers n'était "
                                                 "pas écrite quand la déclaration l'a fixée" % (du, jour))
        except ValueError:
            defauts["date_regle_univers"] = "illisible : %r (attendu AAAA-MM-JJ)" % ligne["date_regle_univers"]
    for c in C.DECLARATION_DATEE:
        v = ligne.get(c)
        if c not in defauts and v is not None and ("\n" in str(v) or "\r" in str(v)):
            defauts[c] = "saut de ligne dans la case"
    return {c: defauts[c] for c in C.DECLARATION_DATEE if c in defauts}


def defauts_d_une_declaration(ligne):
    """Nomme tout ce qui empêche une ligne d'entrer au fichier des déclarations.

    ① RÔLE — Le contrôle d'une ligne AVANT de l'écrire.
    ② CONTEXTE D'APPEL — `ajouter_une_declaration`, `preparer_une_declaration`, `main`.
    ③ ENTRÉE — `ligne` : un dictionnaire {champ : texte}.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des défauts (phrases), vide si la ligne entre.
      [rend: 1]
    ⑥ TRAITEMENT — ① champs hors contrat · ② les champs manquants, en une phrase « champ(s) manquant(s) : … » ·
      ③ chaque autre défaut de `defauts_par_champ`, « champ : raison ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une ligne incomplète rendrait la fiche NON JUGEABLE au moment du regard, trop tard pour la réparer
      sans la dater après lui. La définition du défaut vit dans `defauts_par_champ`, partagée avec la lecture.
    ⑨ CE QUI CLOCHE — Ceux de `defauts_par_champ`.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    defauts = []
    hors = [c for c in ligne if c not in C.DECLARATION_DATEE]
    if hors:
        defauts.append("champ(s) hors contrat DECLARATION_DATEE : " + ", ".join(hors))
    par_champ = defauts_par_champ(ligne)
    vides = [c for c, r in par_champ.items() if r == "vide" or c in C.champs_de_la_declaration_manquants(ligne)]
    if vides:
        defauts.append("champ(s) manquant(s) : " + ", ".join(vides))
    defauts += ["%s : %s" % (c, r) for c, r in par_champ.items() if c not in vides]
    return defauts


def ligne_csv_de_la_declaration(ligne):
    """Rend les octets de la ligne CSV d'une déclaration, telle que le fichier la porte.

    ① RÔLE — UNE façon d'écrire une déclaration en CSV : l'écriture (`ajouter_une_declaration`) et l'empreinte de la
      déclaration (`lire_la_declaration`, clé « empreinte » de VERDICT.declaration) l'emploient toutes deux.
    ② CONTEXTE D'APPEL — `ajouter_une_declaration`, `lire_la_declaration`.
    ③ ENTRÉE — `ligne` : un dictionnaire {champ : texte} ; un champ absent s'écrit vide.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : des octets UTF-8 finis par « \\n ».
      [rend: 1]
    ⑥ TRAITEMENT — `csv.DictWriter` aux champs de DECLARATION_DATEE, fin de ligne « \\n ».
    ⑦ UNITÉ — Des octets.
    ⑧ POURQUOI — R-708 : une empreinte calculée sur une autre écriture que celle du fichier divergerait.
    ⑨ CE QUI CLOCHE — Une ligne écrite à la main avec d'autres guillemets a une autre empreinte que sa réécriture ici :
      l'empreinte est celle du CONTENU des cases, pas des octets du fichier.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    tampon = io.StringIO()
    csv.DictWriter(tampon, fieldnames=C.DECLARATION_DATEE, lineterminator="\n").writerow(
        {c: ligne.get(c, "") for c in C.DECLARATION_DATEE})
    return tampon.getvalue().encode("utf-8")


def ajouter_une_declaration(racine, ligne):
    """Ajoute une déclaration complète au fichier, sans jamais toucher aux lignes déjà écrites.

    ① RÔLE — La seule écriture de `donnees/DECLARATIONS_DATEES.csv`.
    ② CONTEXTE D'APPEL — Le Chat, une fois la déclaration préparée ; l'épreuve de B.
    ③ ENTRÉE — `racine` · `ligne` : un dictionnaire aux champs de DECLARATION_DATEE.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe et son en-tête est le contrat.
    ⑤ SORTIE — UNE valeur : le numéro de la ligne écrite dans le fichier (l'en-tête est la ligne 1).
      [rend: 1]
    ⑥ TRAITEMENT — ① refuser une ligne qui a un défaut · ② lire les octets du fichier et vérifier son en-tête ·
      ③ fabriquer la ligne CSV · ④ réécrire le fichier = anciens octets + la ligne (en ajoutant d'abord une fin de ligne
      si le fichier n'en finit pas) · ⑤ relire : les anciens octets sont un préfixe exact, et la ligne relue est égale
      à celle donnée.
    ⑦ UNITÉ — Des octets, puis des lignes.
    ⑧ POURQUOI — « On n'efface ni ne modifie jamais une ligne : une déclaration corrigée est une ligne de plus »
      (contrat DECLARATION_DATEE). La relecture : un fichier peut être écrit ailleurs ou tronqué (lot L4).
    ⑨ CE QUI CLOCHE — Aucun verrou : deux écrivains simultanés perdraient une ligne ; la relecture le verrait chez
      le second.
    ⑩ EFFET — Réécrit le fichier, avec une ligne de plus.
    ⑪ TERMINAISON — Rend la main ; lève ValueError (défaut, en-tête, relecture).
      [sort: non]
    """
    defauts = defauts_d_une_declaration(ligne)
    if defauts:
        raise ValueError("déclaration refusée : " + " ; ".join(defauts))
    chemin = os.path.join(racine, C.DECLARATIONS_DATEES)
    with open(chemin, "rb") as f:
        avant = f.read()
    entete = next(csv.reader(io.StringIO(avant.decode("utf-8-sig"))), None)
    if entete != C.DECLARATION_DATEE:
        raise ValueError("en-tête hors contrat DECLARATION_DATEE : %s" % entete)
    nouveau = avant + (b"" if avant.endswith(b"\n") else b"\n") + ligne_csv_de_la_declaration(ligne)
    with open(chemin, "wb") as f:
        f.write(nouveau)
    with open(chemin, "rb") as f:
        relu = f.read()
    if not relu.startswith(avant.rstrip(b"\n")):
        raise ValueError("relecture : les lignes déjà écrites ne sont plus un préfixe exact")
    lignes = list(csv.DictReader(io.StringIO(relu.decode("utf-8-sig"))))
    if {c: lignes[-1][c] for c in C.DECLARATION_DATEE} != {c: ligne.get(c, "") for c in C.DECLARATION_DATEE}:
        raise ValueError("relecture : la dernière ligne relue diffère de la ligne donnée")
    return len(lignes) + 1


def declaration_engagee(racine, fiche_id, annees_d_examen):
    """Rend la déclaration qui fait foi pour le regard sur les années d'examen : celle que portait la branche
    principale AU COMMIT QUE LE PREMIER REGARD A VU (son `sommet_principal`), ou à son sommet s'il n'y a pas de regard.

    ① RÔLE — R-505 ① : « Exiger la déclaration datée, écrite avant le regard ». Une déclaration est antérieure si elle
      était sur la branche principale au commit que le premier regard a inscrit en naissant.
    ② CONTEXTE D'APPEL — `lire_la_declaration` (la porte du juge) ; les épreuves de B, B3 et du regard unique.
    ③ ENTRÉE — `racine` : un dépôt git complet · `fiche_id` · `annees_d_examen` : « début..fin ».
    ④ CONDITIONS D'ENTRÉE — Celles de `declaration_de_la_fiche` ; le dépôt commun joignable (`premier_regard`).
    ⑤ SORTIE — DEUX valeurs : la ligne retenue (dictionnaire) ou None, et la raison ; quand une ligne est rendue, la
      raison nomme l'ancre (« sommet <12 car.>, vu par le premier regard » ou « …, aucun regard inscrit »).
      [rend: 2]
    ⑥ TRAITEMENT — ① sommet lisible de `C.BRANCHE_PRINCIPALE` (`TENIR_LE_REGISTRE_DES_ESSAIS.histoire_lisible`) ·
      ② le premier regard (`premier_regard`, sur la branche des regards) ; inconnu → None · ③ l'ancre : son
      `sommet_principal` (« INCONNU » ou absent → None : ancre inconnue) ; sans regard, le sommet de la branche ·
      ④ l'ancre doit être un ANCÊTRE de la branche principale (`git merge-base --is-ancestor`), sinon lever ValueError
      (la lecture devient ILLISIBLE, donc INCONNU) · ⑤ le fichier des déclarations à l'ancre, lu par
      `declaration_de_la_fiche` (la seule lecture du fichier, R-708), sans limite de date.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Décision de Jean-Luc du 12-11-2026 à 09h04, « Reparer » : l'ancrage par l'historique git est GARDÉ et
      RÉPARÉ. L'ancien chemin marchait l'histoire du fichier des déclarations ; une fusion ordinaire (un essai annulé
      sur une branche de travail) rendait TOUTE fiche NON JUGEABLE (relecteur REGARD tour 2, T2-D1), et le premier
      regard était cherché sur la branche principale, où plus aucun regard ne s'inscrit (ancrage INERTE, superviseur
      ANCRAGE, §1). L'instantané inscrit par le regard rend la déclaration d'avant lui, insensible aux fusions, aux
      retours arrière et aux déclarations postérieures (superviseur ANCRAGE, §2, mesuré).
    ⑨ CE QUI CLOCHE — ① Une ligne écrite mais pas encore sur la branche ne compte pas : c'est voulu. ② L'instantané
      est celui du poste qui inscrit : une déclaration poussée mais pas encore récupérée manque (côté strict). ③ LIMITE
      J1 (décision de Jean-Luc du 12-11-2026 à 08h58, « 1 · Empêcher l'erreur (recommandé) », BACKLOG A-708) :
      protège de l'ERREUR d'agent, pas d'un agent qui tricherait — une réécriture forcée de la branche principale est
      vue par le contrôle d'ascendance, au mieux, sans garantie.
    ⑩ EFFET — Lance git ; écrit puis efface une copie temporaire.
    ⑪ TERMINAISON — Rend la main ; lève ValueError (ancre qui n'est pas un ancêtre ; et ce que lève
      `declaration_de_la_fiche` : en-tête, dates).
      [sort: non]
    """
    import tempfile
    sommet, raison = T.histoire_lisible(racine, C.BRANCHE_PRINCIPALE)
    if sommet is None:
        return None, raison
    regard, raison = T.premier_regard(racine, annees_d_examen, fiche_id)
    if regard is None:
        return None, "premier regard inconnu : " + raison
    ancre = sommet
    if regard:
        ancre = (T.lire_le_registre(racine)[0].get(regard) or {}).get("sommet_principal") or ""
        if len(ancre) != 40:
            return None, "ancre inconnue : le premier regard %s n'a pas inscrit le sommet qu'il voyait (%r)" % (
                regard, ancre)
        code, _s, _e = T.lancer_git(racine, ["merge-base", "--is-ancestor", ancre, C.BRANCHE_PRINCIPALE])
        if code != 0:
            raise ValueError("ancre %s du premier regard %s : pas un ancêtre de %s (code %d)"
                             % (ancre[:12], regard, C.BRANCHE_PRINCIPALE, code))
    git = T.git_de(racine)
    code, octets = git("show", "%s:%s" % (ancre, C.DECLARATIONS_DATEES))
    if code != 0:
        return None, "fichier des déclarations absent au commit %s" % ancre[:13]
    with tempfile.TemporaryDirectory() as copie:
        os.makedirs(os.path.join(copie, os.path.dirname(C.DECLARATIONS_DATEES)))
        with open(os.path.join(copie, C.DECLARATIONS_DATEES), "wb") as f:
            f.write(octets)
        # `declaration_de_la_fiche` lit le registre des stratégies SOUS LA RACINE QU'ON LUI DONNE (forme canonique,
        # B2 tour 2) : le registre du disque est recopié dans la copie (fusion J + B2, mission REGARD).
        registre = C.chemin_du_registre(racine)
        if os.path.isfile(registre):
            os.makedirs(os.path.join(copie, os.path.dirname(C.REGISTRE_DES_STRATEGIES)), exist_ok=True)
            shutil.copyfile(registre, os.path.join(copie, C.REGISTRE_DES_STRATEGIES))
        ligne = C.declaration_de_la_fiche(copie, fiche_id, "9999-12-31T23:59:59+00:00")
    if ligne is None:
        return None, "aucune déclaration de %s au commit %s (%s)" % (
            fiche_id, ancre[:12], "vu par le premier regard" if regard else "sommet, aucun regard")
    return ligne, "sommet %s, %s" % (ancre[:12], "vu par le premier regard" if regard else "aucun regard inscrit")


def preparer_une_declaration(racine, saisie):
    """Rend la ligne complète d'une déclaration datée, ses champs calculés remplis par programme, prête pour
    `ajouter_une_declaration`.

    ① RÔLE — Faire que la date et les deux empreintes de la règle figée ne soient JAMAIS saisies à la main (R-728 :
      « ce qui se calcule ne s'écrit jamais à la main ») : l'appelant donne ce qui se DÉCIDE (hypothèse, lignée,
      années, univers…), ce programme calcule le reste.
    ② CONTEXTE D'APPEL — Le Chat, quand Jean-Luc a confirmé le texte d'une déclaration (DÉL-D21) ; l'épreuve B3
      (`tests/EPREUVES_B3_DECLARATION_Mer_11-11-2026.py`). Mission B3 du plan V7, 11-11-2026.
    ③ ENTRÉE — `racine` : la racine du dépôt · `saisie` : un dictionnaire {champ de DECLARATION_DATEE : texte} SANS
      les champs de CHAMPS_CALCULES_DE_LA_DECLARATION (absents, ou vides).
    ④ CONDITIONS D'ENTRÉE — `<racine>/emp.py`, `programmes/JUGE_DES_STRATEGIES.py`, le registre des stratégies, et le
      module de signal que la fiche y nomme (`module_signal`) existent.
    ⑤ SORTIE — UNE valeur : la ligne, un dictionnaire {champ : texte} aux champs de DECLARATION_DATEE. Exemple :
      pour la fiche C5E10-QA-V1, `empreinte_code_signal` est l'empreinte sans textes de son `module_signal`, et
      `date_declaration` l'instant de l'appel, « 2026-11-11T22:58+01:00 ».
      [rend: 1]
    ⑥ TRAITEMENT — ① refuser une saisie qui remplit un champ calculé · ② trouver la fiche au registre
      (`CONTRATS_DES_FICHIERS.lire_les_fiches`, dernière ligne, n°83) et son `module_signal` · ③ calculer les deux
      empreintes (`empreintes_du_code`) · ④ dater à l'horloge, heure de Paris, à la minute, avec le décalage ·
      ⑤ refuser la ligne si `defauts_d_une_declaration` y trouve un défaut.
    ⑦ UNITÉ — Un instant en heure de Paris (Europe/Paris) avec son décalage.
    ⑧ POURQUOI — Une empreinte recopiée à la main peut être celle d'un autre état du code ; une date tapée peut
      précéder un regard qu'elle suit. Calculées ici, et recalculées à la lecture (`lire_la_declaration`), elles
      lient la déclaration au code réellement jugé (R-505 ① : la déclaration fixe « la règle figée (empreinte du code
      du juge et du signal, réglages) »).
    ⑨ CE QUI CLOCHE — ① `reglages` reste saisi : aucun texte ne dit quelles colonnes de la fiche forment « les
      réglages » (question laissée au Chat, note B3) ; rien ne le confronte donc à la fiche. ② `bareme` se saisit
      aussi : le contrat le dit « les lignes de donnees/BAREME_FRAIS.csv et l'année de donnees/VALEURS_TTF.csv
      employées », sans forme calculable fixée. ③ La date est celle de l'appel, pas celle du commit qui portera la
      ligne : l'antériorité au regard se prouve à la lecture, par l'histoire (`declaration_engagee`).
    ⑩ EFFET — Lit le registre, `emp.py` et deux programmes ; lit l'horloge.
    ⑪ TERMINAISON — Rend la main ; lève ValueError (champ calculé saisi, fiche absente ou sans module, défaut) et
      FileNotFoundError (fichier manquant).
      [sort: non]
    """
    from zoneinfo import ZoneInfo
    saisis = [c for c in C.CHAMPS_CALCULES_DE_LA_DECLARATION if str(saisie.get(c) or "").strip()]
    if saisis:
        raise ValueError("déclaration refusée : %s se calcule(nt), ne se saisit(ssent) pas (R-728)" % ", ".join(saisis))
    fiche = C.lire_les_fiches(racine).get(saisie.get("fiche_id"))
    if fiche is None:
        raise ValueError("déclaration refusée : fiche %r absente du registre des stratégies" % saisie.get("fiche_id"))
    import JUGE_DES_STRATEGIES as JS              # LA lecture des colonnes du signal (A-542 ; relecteur REGARD, T2-D2)
    module = JS.declaration_du_signal(fiche)[0]
    if not module:
        raise ValueError("déclaration refusée : la fiche %r ne nomme aucun module de signal" % saisie.get("fiche_id"))
    juge, signal = empreintes_du_code(racine, module)
    ligne = dict(saisie)
    ligne.update(date_declaration=datetime.now(ZoneInfo("Europe/Paris")).isoformat(timespec="minutes"),
                 empreinte_code_juge=juge, empreinte_code_signal=signal)
    defauts = defauts_d_une_declaration(ligne)
    if defauts:
        raise ValueError("préparation refusée : " + " ; ".join(defauts))
    return ligne


def lire_la_declaration(racine, fiche_id, instant_du_regard):
    """LA LECTURE CONTRÔLÉE DE LA DÉCLARATION DATÉE : rend, calculé en lisant le dépôt, ce que la grille du juge doit
    recevoir pour le contrôle ① de R-505 — jamais une liste fournie par l'appelant.

    ① RÔLE — R-505 ① : « Exiger la déclaration datée, écrite avant le regard, sinon rendre NON JUGEABLE en nommant le
      champ qui manque ». Le superviseur R-759 du 11-11-2026 (22h19, point 2) a relevé que la grille passait ce
      contrôle sur `declaration_manquants == []` venu de l'appelant (MODULE_JUGEMENT, l. 3458-3464 de agentB) : « une
      liste vide ne distingue pas « j'ai lu et il n'y a rien » de « je n'ai pas lu » ». Cette fonction est la lecture
      qui produit cette liste : elle lit le fichier, prouve l'antériorité par l'histoire, recalcule les empreintes.
    ② CONTEXTE D'APPEL — La porte du juge écrite par l'agent J du plan V7 (`juger_une_fiche`, superviseur, point 3
      ②), une fois par fiche jugée, AVANT la grille ; l'épreuve B3. Mission B3, 11-11-2026.
    ③ ENTRÉE — `racine` : un dépôt git complet (non superficiel) · `fiche_id` : l'identifiant au registre des
      stratégies (« C5E10-QA-V1 ») · `instant_du_regard` : l'instant du regard, ISO AVEC décalage
      (« 2026-11-20T20:00:00+01:00 »). La branche principale n'est plus un paramètre : c'est `C.BRANCHE_PRINCIPALE`,
      lue dedans (relecteur B3, D1 ; superviseur ANCRAGE, §3.2 ; mission REGARD, tour 3).
    ④ CONDITIONS D'ENTRÉE — Aucune : ce qui ne se lit pas rend ILLISIBLE ou un champ en défaut, jamais COMPLETE.
    ⑤ SORTIE — UNE valeur : un dictionnaire aux clés de LECTURE_DE_LA_DECLARATION (contrat). `etat` : COMPLETE,
      NON_JUGEABLE ou ILLISIBLE ; `champs_en_defaut` : [] si COMPLETE, liste NON VIDE si NON_JUGEABLE, None si
      ILLISIBLE — à passer TEL QUEL en `declaration_manquants` à `MODULE_JUGEMENT.grille_de_validation`. Exemple réel
      au 11-11-2026 : `donnees/DECLARATIONS_DATEES.csv` n'a que son en-tête, donc toute fiche rend NON_JUGEABLE, chaque
      champ exigé « aucune déclaration ».
      [rend: 1]
    ⑥ TRAITEMENT — ① lire `instant_du_regard` (illisible ou sans décalage → ILLISIBLE) · ② la dernière ligne de la
      fiche écrite avant l'instant (`CONTRATS_DES_FICHIERS.declaration_de_la_fiche`, la seule lecture du fichier ;
      fichier absent, en-tête hors contrat, date illisible → ILLISIBLE ; de même à l'ancre, et une ancre qui n'est pas
      un ancêtre de la branche) · ③ si une ligne existe : la remplacer par la déclaration ENGAGÉE
      (`declaration_engagee` : au commit que le premier regard a vu) ; pas de ligne engagée, ligne engagée datée à
      l'instant du regard ou après, ou dernière ligne écrite DIFFÉRENTE de la ligne engagée (une déclaration écrite
      après le premier regard) → défaut `date_declaration` · ④ les défauts de forme,
      par `defauts_par_champ` (la même définition qu'à l'écriture) · ⑤ recalculer les deux empreintes
      (`empreintes_du_code`, sur le `module_signal` de la fiche au registre) : non recalculable, ou différente de la
      valeur déclarée → défaut du champ · ⑥ assembler, dans l'ordre du contrat ; empreinte de la déclaration =
      sha256 de `ligne_csv_de_la_declaration`, 16 premiers caractères.
    ⑦ UNITÉ — Des champs ; des instants comparés avec leur décalage.
    ⑧ POURQUOI — « Écrite avant le regard » ne se prouve pas par la date que la ligne déclare (`declaration_de_la_
      fiche`, ⑨ ①) mais par l'ordre de l'histoire (superviseur R-759, défaut 5) : sans branche, l'antériorité n'est
      pas prouvée, et la règle la plus stricte prime. Une empreinte qui a changé veut dire que le code jugé n'est plus
      la règle figée déclarée (R-505 ①) : juger quand même jugerait autre chose que ce qui a été déclaré (lecture de
      B3, à confirmer par Jean-Luc). ILLISIBLE ne devient jamais NON_JUGEABLE : un fichier qu'on n'a pas pu lire
      n'est pas une déclaration absente (R-734), et la grille, recevant None, rend son contrôle ① INCONNU — jamais
      PASSE.
    ⑨ CE QUI CLOCHE — ① Le premier regard est compté PAR FICHE (`TENIR_LE_REGISTRE_DES_ESSAIS.premier_regard`), ce
      que le superviseur du 11-11-2026 a jugé RUSTINE (point 4 : il faut compter par LIGNÉE) ; cette fonction en
      hérite tant que B2 ne l'a pas repris. ② Le module de signal est celui que la fiche nomme AUJOURD'HUI au
      registre : si la fiche a changé de module, l'empreinte diffère et la fiche est NON JUGEABLE, ce qui est voulu.
      ③ Le juge importe d'autres modules (jugement, positions) : leur changement ne change pas l'empreinte du juge
      (⑨ de `empreintes_du_code`). ④ `reglages`, `bareme`, `temoins` ne sont confrontés à rien de calculé (voir
      `preparer_une_declaration`, ⑨). ⑤ k n'est pas rendu ici : il se compte par `JUGE_DES_STRATEGIES.k_a_la_date`
      sur `date_declaration` et `temoins` de la ligne rendue (note B3, pour J).
    ⑩ EFFET — Lit le fichier des déclarations, le registre des stratégies, deux programmes et `emp.py` ; lance git en
      lecture ; écrit puis efface des copies temporaires (par `declaration_engagee`).
    ⑪ TERMINAISON — Rend la main ; un appel à git peut ne pas revenir (aucun délai posé, `TENIR_LE_REGISTRE_DES_
      ESSAIS.git_de`).
      [sort: non]
    """
    import hashlib
    lecture = {c: None for c in C.LECTURE_DE_LA_DECLARATION}
    branche = C.BRANCHE_PRINCIPALE
    lecture.update(fiche_id=fiche_id, instant_du_regard=instant_du_regard, branche=branche, raisons=[],
                   empreintes_calculees={c: None for c in C.CHAMPS_CALCULES_DE_LA_DECLARATION
                                         if c.startswith("empreinte_")})
    complete, non_jugeable, illisible = C.ETATS_DE_LA_LECTURE_DE_LA_DECLARATION
    try:
        limite = datetime.fromisoformat(instant_du_regard)
        if limite.tzinfo is None:
            raise ValueError("sans décalage horaire")
        ligne = C.declaration_de_la_fiche(racine, fiche_id, instant_du_regard)
    except (TypeError, ValueError, OSError) as e:
        lecture.update(etat=illisible, champs_en_defaut=None,
                       raisons=["fichier : lecture impossible (%s) — instant %r" % (e, instant_du_regard)])
        return lecture
    defauts = {}

    def defaut(champ, raison):
        """Ajoute une raison à un champ en défaut.
        ① RÔLE — un pas de l'assemblage des défauts.
        ② CONTEXTE D'APPEL — `lire_la_declaration`, à chaque défaut trouvé.
        ③ ENTRÉE — `champ` : un champ de DECLARATION_DATEE · `raison` : une phrase.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — aucune valeur.
          [rend: rien]
        ⑥ TRAITEMENT — créer l'entrée, ou joindre la raison à la précédente par « ; ».
        ⑦ UNITÉ — —
        ⑧ POURQUOI — un champ peut avoir plusieurs défauts (non engagé ET mal daté) : aucun ne doit en cacher un autre.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — modifie `defauts`.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]"""
        defauts[champ] = (defauts[champ] + " ; " + raison) if champ in defauts else raison

    if ligne is not None:
        examen = ligne.get("annees_d_examen") or ""
        try:
            engagee, raison = declaration_engagee(racine, fiche_id, examen)
        except (ValueError, OSError) as e:                 # ancre non ancêtre, ou fichier illisible à l'ancre
            lecture.update(etat=illisible, champs_en_defaut=None,
                           raisons=["fichier : lecture impossible à l'ancre de %s (%s)" % (branche, e)])
            return lecture
        if engagee is None:
            lecture["engagee"] = False
            defaut("date_declaration", "non engagée sur %s avant le premier regard : %s" % (branche, raison))
        else:
            lecture["engagee"] = True
            if ligne_csv_de_la_declaration(engagee) != ligne_csv_de_la_declaration(ligne):
                # LE FAIT MESURÉ, PAS UNE CAUSE (superviseur POSTE EN RETARD du 12-11-2026) : la différence peut venir
                # d'une ligne écrite après le regard OU d'un poste en retard au moment du regard
                defaut("date_declaration", "la dernière déclaration écrite diffère de celle que portait %s (%s)"
                       % (branche, raison))
            ligne = engagee
            try:
                if datetime.fromisoformat(ligne.get("date_declaration") or "") >= limite:
                    defaut("date_declaration", "la déclaration engagée est datée à l'instant du regard ou après")
            except (TypeError, ValueError):
                pass                                    # le défaut de forme le dira (defauts_par_champ)
    for champ, raison in defauts_par_champ(ligne).items():
        defaut(champ, raison)
    if ligne is not None:
        calculees, raison = {}, ""
        try:
            import JUGE_DES_STRATEGIES as JS      # LA lecture des colonnes du signal (A-542 ; T2-D2)
            fiche = C.lire_les_fiches(racine).get(fiche_id)
            module = JS.declaration_du_signal(fiche or {})[0]
            if not module.strip():
                raison = "la fiche %r ne nomme aucun module de signal au registre" % fiche_id
            else:
                juge, signal = empreintes_du_code(racine, module.strip())
                calculees = {"empreinte_code_juge": juge, "empreinte_code_signal": signal}
        except (OSError, ValueError, SyntaxError) as e:
            raison = "%s : %s" % (type(e).__name__, e)
        lecture["empreintes_calculees"].update(calculees)
        for champ in lecture["empreintes_calculees"]:
            if champ in defauts:
                continue
            if champ not in calculees:
                defaut(champ, "non recalculable : " + raison)
            elif calculees[champ] != (ligne.get(champ) or "").strip():
                defaut(champ, "déclarée %r, recalculée %r : le code a changé depuis la déclaration, ce n'est plus la "
                              "règle figée" % (ligne.get(champ), calculees[champ]))
        lecture["empreinte_de_la_declaration"] = hashlib.sha256(ligne_csv_de_la_declaration(ligne)).hexdigest()[:16]
    champs = [c for c in C.DECLARATION_DATEE if c in defauts]
    lecture.update(declaration=ligne, etat=non_jugeable if champs else complete, champs_en_defaut=champs,
                   raisons=["%s : %s" % (c, defauts[c]) for c in champs])
    return lecture


def main(argv):
    """Contrôle le fichier des déclarations d'une racine.
    ① RÔLE — Le contrôle à la main.
    ② CONTEXTE D'APPEL — la ligne de commande.
    ③ ENTRÉE — `argv` : la racine et
    « --controler ».
    ④ CONDITIONS D'ENTRÉE — —.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2 (voir l'en-tête).
      [rend: 1]
    ⑥ TRAITEMENT — lire l'en-tête, contrôler chaque ligne par `defauts_d_une_declaration`, afficher.
    ⑦ UNITÉ — lignes.
    ⑧ POURQUOI — R-734.
    ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — affiche, lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]"""
    if len(argv) != 2 or argv[1] != "--controler":
        print("usage : DECLARER_UNE_STRATEGIE.py <racine> --controler")
        return 2
    with open(os.path.join(argv[0], C.DECLARATIONS_DATEES), encoding="utf-8-sig", newline="") as f:
        lecteur = csv.DictReader(f)
        lignes = list(lecteur)
    if lecteur.fieldnames != C.DECLARATION_DATEE:
        print("DÉFAUT : en-tête hors contrat DECLARATION_DATEE")
        return 1
    n = 0
    for i, l in enumerate(lignes, 2):
        for d in defauts_d_une_declaration(l):
            print("DÉFAUT ligne %d (%s) : %s" % (i, l.get("fiche_id"), d))
            n += 1
    print("déclarations : %d ligne(s) · défauts : %d" % (len(lignes), n))
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
