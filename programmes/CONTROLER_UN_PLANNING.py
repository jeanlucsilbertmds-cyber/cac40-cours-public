#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Refuse un planning qui ne suit pas la méthode de planning, et calcule lui-même son chemin critique et sa fin.

① RÔLE — Dire, par un code de sortie et des motifs nommés, si un planning peut
  être présenté à Jean-Luc. Le planning n'est pas lu dans de la prose : il vit
  dans trois fichiers CSV d'un même dossier (séparateur « ; ») que ce programme
  lit, et à partir desquels il CALCULE le chemin critique, les marges et les
  dates de fin — DEPUIS MAINTENANT, et sous le budget du forfait (depuis le
  16-11-2026). Ce qui se calcule ne s'écrit pas à la main (R-728).
  Les trois fichiers :
  · planning.csv — en-tête « cle;valeur », schéma fermé (clés connues lues aux
    réglages) : objectif, analyse de départ (forfait, ressources), début,
    limites du parallélisme, chemins des fichiers de jugement, d'estimation et
    de jalons ;
  · etapes.csv — une ligne par étape : etape;livre;depend_de;charge_h_min;
    charge_h_max;delai_h_min;delai_h_max;ecart;agents_min;agents_max;
    points_min;points_max;jugement_auteur;etat ;
  · leviers.csv — etape;levier;verdict;gain_ou_raison : les six leviers du
    §13.0quater sur chaque étape du chemin critique.
  Et, hors du dossier, la CARTE DES PANNES du projet (clé carte_des_pannes,
  depuis le 18-11-2026, A-898) : panne;categorie;detection;reponse;tenue_par;
  reste_a_l_humain — une carte par projet, partagée par ses plannings.
  Installé dans programmes/ le 18-11-2026 depuis
  etudes/PLAN_V7_SOUS_L_OUTIL_PLANNING/planning_reel_Lun_16-11-2026/programmes/
  (étape PANNES, A-897 à A-899), où il plantait sans PYTHONPATH (trace et
  code 1 au lieu du code 2 de R-734) : le veilleur n'y était pas à côté.
  Exemple réel : tests/PLANNING_TOUR5_Mer_11-11-2026/ (le planning du tour 5
  du plan V7, converti le 11-11-2026).

② CONTEXTE D APPEL — À la main, par le Chat, AVANT de présenter tout planning
  et à chaque réveil sous l'outil planning (règle proposée à Jean-Luc dans
  echanges/A_RELIRE_METHODE.md). Par les épreuves
  tests/EPREUVES_DU_CONTROLE_D_UN_PLANNING_Mer_11-11-2026.py, qui chargent ce
  fichier et appellent `main` (absentes de la copie du 16-11-2026, non
  relancées), et par tests/EPREUVES_PLANNING_REEL_Lun_16-11-2026.py, qui
  appellent `controler` et sabotent le calcul réel. Aucune tâche automatique
  ne l'appelle.

③ ENTRÉE — La ligne de commande : le chemin du dossier du planning ; option
  « --maintenant=AAAA-MM-JJ HH:MM » ou « --maintenant=AAAA-MM-JJTHH:MM » (heure
  de Paris) pour les épreuves, sinon l'horloge. Les réglages (seuils, listes,
  schéma) se lisent dans programmes/REGLAGES_DU_PLANNING.csv, jamais dans ce
  code.

④ CONDITIONS D ENTRÉE — Le dossier et ses trois fichiers existent et se lisent
  en UTF-8 ; les réglages se lisent. Sinon : ligne « ARRET » et code 2.

⑤ SORTIE — Des lignes affichées : « CALCUL … » (chemin critique, marges, fins
  sans forfait depuis maintenant, reste des étapes en cours, forfait, « fin
  réelle (forfait compris) » au mieux et réaliste, listes « avant la remise à
  zéro : … / après : … », étapes prêtes), « SIGNAL … » (à dire à Jean-Luc, sans refuser), « REFUS … »
  (un motif par ligne), puis « PLANNING ACCEPTÉ » ou « PLANNING REFUSÉ : N
  motif(s) ». Code 0 accepté · 1 refusé · 2 contrôle impossible, y compris
  toute erreur imprévue du programme (R-734 : un contrôle qui n'a pas pu
  tourner ne se confond jamais avec un refus).

⑥ TRAITEMENT — Dans `controler`, dans cet ordre, chaque bloc portant son
  repère dans le code :
  C1 lire réglages et fichiers ·
  C2 schéma fermé de planning.csv (clé inconnue, clé en double) ·
  C3 objectif en une phrase ·
  C4 forfait : relevé daté (pas dans le futur), pourcentage dans 0 à 100,
     remise à zéro à moins de 7 jours après la capture ; relevé périmé ou
     remise à zéro passée → ESTIMATION marquée ESTIMÉ (estimer_le_forfait,
     A-899 : le forfait ne freine jamais), au-delà du plafond → signal ·
  C5 ressources : relevé daté, valeurs numériques finies, processeurs ≥ 1,
     disque ≥ seuil, agents au travail ≤ plafond ·
  C6 début du planning (heure du relevé des états et des restes) : présent,
     pas plus vieux que la fraîcheur ; les fins n'en partent plus ·
  C7 limites du parallélisme ·
  C8 chaque étape : champs, nombres finis et min ≤ max, charge réalisable
     dans le délai par ses agents quand elle en a (sans agent, la charge est
     celle de Jean-Luc ou de GitHub, non divisée), jugement (mot entier ; « non raisonnable »
     refusé, « long » et « impossible à juger » signalés), état, dépendances
     connues ·
  C8bis la somme des délais max (plus l'attente de la remise à zéro) tient
     dans le calendrier calculable, sinon REFUS et dates non calculées ·
  C9 jugement daté de l'auteur et estimation de l'expert neuf (fichiers
     distincts, datés, expert APRÈS l'auteur, chaque étape non tenue présente
     dans les deux) ·
  C10 calcul (cycle ; chemin critique, marges et fins au mieux et réaliste,
     depuis MAINTENANT ; budget de forfait de la fenêtre courante = (plafond −
     pourcentage capturé) × points_par_pourcent, lus dans planning.csv et les
     réglages, jamais dans le code (R-708) ; étapes placées avant ou après la
     remise à zéro dans l'ordre du chemin critique par planifier_sous_forfait,
     d'où la fin réelle ; forfait suffisant ; étape lancée avant ses dépendances ; agents déclarés
     sans étape active ; ressources sous-employées) ·
  C11 les six leviers sur chaque étape critique de l'un ou l'autre calcul ·
  C13 carte des pannes (controler_la_carte) ·
  C9bis l'état vu par l'ordonnanceur (ORDONNER_UN_PLANNING.lire_tout sans
     réseau, puis situation, AVEC OU SANS branche d'état — sans elle, comme
     l'ordonnanceur à son premier passage) : il donne à C10 les étapes prêtes
     et occupées, et à C14 les étapes non tenues et le signe de vie ; une
     lecture impossible (C.Impossible, OSError, UnicodeError, csv.Error :
     une ENTRÉE illisible) → ERREUR ÉTAT ILLISIBLE (refus, R-734), et C10 ne
     dit rien des étapes prêtes ; toute autre exception (un PROGRAMME faux :
     SyntaxError, NameError, KeyError…) n'est jamais un refus, elle remonte,
     et la ligne de commande rend 2 (m12 de la relecture f2ce23138) ·
  C14 signe de vie de la conversation (vie/chat.txt de la branche d'état,
     références locales, age_du_signe) : absent → signal ; plus vieux que
     signe_de_vie_max_min ou daté dans le futur, une étape non TENUE selon
     situation (la même liste que le chien de garde) → ERREUR (refus) ·
  C12 jalons : lus par le veilleur (TENIR_UN_PLANNING.passage_unique, qui
     n'écrit rien), un jalon par étape, une étape déclarée tenue a sa preuve
     (jugée par le veilleur), échéance pas avant la fin au plus tôt
     calculée (depuis maintenant, forfait compris) ni avant le jalon d'une
     dépendance. C13 et C14 passent AVANT C12, qui peut sortir tôt.

⑦ UNITÉ — Charges et délais en HEURES ; points de forfait en points ; forfait
  en pourcentage ; disque en Go ; heures de Paris.

⑧ POURQUOI — Le 11-11-2026, le Chat a présenté un planning sans section
  « Leviers passés », sans relevé des ressources, avec un seul agent lancé alors
  que tout était prêt. La méthode disait elle-même que ce contrôle « repose sur
  le Chat » tant que l'action A-698 du BACKLOG (rendre la méthode déterministe
  par programme) n'est pas faite. Jean-Luc, 11-11-2026 à 22h19 : « fais en sorte
  que la méthodologie planning soit contraignante vraiment ». Ce qu'un programme
  peut faire, un programme le fait (R-754).

⑨ CE QUI CLOCHE — Il contrôle la FORME et le CALCUL, jamais la justesse : un
  gain de levier inventé, une estimation d'expert recopiée de l'auteur, un
  levier qui retire un contrôle passent s'ils sont bien écrits. La « présence »
  d'une étape dans le fichier de l'expert est un identifiant trouvé comme mot :
  « E1 … E9 : non estimés » passe (relecteur neuf du 11-11-2026, D10). Les
  dates des fichiers de jugement et d'expert et celle de la capture sont lues
  dans le texte : elles reposent sur la parole de qui les écrit. Une estimation
  du forfait suppose une consommation régulière dans la fenêtre ; elle ne se
  corrige pas seule (l'écart au relevé est journalisé par l'ordonnanceur). La
  carte des pannes est contrôlée dans sa forme, jamais dans sa justesse. « --maintenant »
  permet de faire passer une capture périmée : réservé aux épreuves, rien ne
  l'interdit. « agents_en_cours » est déclaré : il n'est borné que par le
  plafond et par la somme des agents des étapes actives, jamais compté. Le
  calendrier ne connaît QUE la remise à zéro du forfait : ni circuit du soir
  absent le week-end, ni plages de Jean-Luc. La décision « seulement l'urgent » (A-834) se lit
  dans la clé « avant_remise_seulement » ; la limite de concurrence dans
  « agents_simultanes_max », qui compte des étapes et non des agents. Le reste
  d'une étape « en cours » n'est déclaré qu'au relevé du début : il est compté
  pour TOUT son délai depuis maintenant (le temps passé depuis le début n'est
  pas déduit, rien ne dit qu'il a servi). Aucune conversion heures de charge →
  points n'existe : les points viennent des colonnes points_min/points_max,
  déclarées par étape, et sont comptés en entier dans la fenêtre où l'étape
  commence. Une seule fenêtre après la remise à zéro est calculée : son
  dépassement est signalé, pas reporté. Les jalons, posés depuis l'ancien
  début, sont refusés en nombre tant qu'ils ne sont pas redatés. Le superviseur après un défaut grave (R-759) n'est pas
  contrôlé. Aucun contrôle que l'expert n'a pas vu le jugement de l'auteur. Les
  chiffres du CSV ne sont pas confrontés à ceux des fichiers de jugement.

⑩ EFFET — Aucun : il lit et affiche (dont, par git, la branche d'état dans les
  références locales). Le veilleur appelé (passage_unique) n'écrit rien non plus.

⑪ TERMINAISON — Rend un code de sortie ; aucun appel réseau (git local, chaque
  appel borné à 120 s), aucune boucle ouverte : revient toujours.
"""
import csv
import datetime
import math
import os
import re
import sys
from zoneinfo import ZoneInfo

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
try:
    import TENIR_UN_PLANNING  # noqa: E402  (le veilleur : une seule lecture des jalons, R-708)
except ImportError as _e:   # R-734 : sans le veilleur, le contrôle n'a pas pu tourner — code 2, jamais une trace en code 1
    if __name__ == "__main__":
        print(f"ARRET contrôle impossible : le veilleur TENIR_UN_PLANNING.py ne s'importe pas depuis {ICI} ({_e})")
        sys.exit(2)
    raise

P = ZoneInfo("Europe/Paris")
REGLAGES = os.path.join(ICI, "REGLAGES_DU_PLANNING.csv")
COLONNES_ETAPES = ("etape", "livre", "depend_de", "charge_h_min", "charge_h_max",
                   "delai_h_min", "delai_h_max", "ecart", "agents_min", "agents_max",
                   "points_min", "points_max", "jugement_auteur", "etat")
COLONNES_LEVIERS = ("etape", "levier", "verdict", "gain_ou_raison")
JOURS = ("Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim")
REGLAGES_NOMBRES = ("fraicheur_max_h", "plafond_forfait_pct", "points_par_pourcent",
                    "remise_a_zero_max_j", "disque_min_go", "seuil_calcul_lourd_h", "calculs_lourds_max",
                    "signe_de_vie_max_min")
REGLAGES_LISTES = ("leviers", "verdicts_levier", "jugements_permis", "jugements_refuses",
                   "jugements_signales", "etats", "etats_qui_liberent", "etats_actifs",
                   "ressources_exigees", "cles_connues", "categories_de_pannes", "executants_de_pannes")
COLONNES_PANNES = ("panne", "categorie", "detection", "reponse", "tenue_par", "reste_a_l_humain")
# Marques admises dans la colonne « detection » de la carte des pannes, à la place d'un programme
NON_PROGRAMMABLE = "NON PROGRAMMABLE :"
SANS_OBJET = "SANS OBJET :"


class Impossible(Exception):
    """Le contrôle ne peut pas tourner (fichier absent, illisible) : code 2."""


def lire_table(chemin, colonnes):
    """Lit un CSV « ; » et rend ses lignes, en refusant une colonne en trop ou manquante.

    ① RÔLE — La seule lecture de CSV de ce programme (réglages, en-tête, étapes,
      leviers).
    ② CONTEXTE D APPEL — Par lire_reglages et controler, une fois par fichier.
    ③ ENTRÉE — `chemin` : le fichier ; `colonnes` : les noms d'en-tête exigés.
    ④ CONDITIONS D ENTRÉE — Fichier existant, UTF-8. Sinon Impossible.
    ⑤ SORTIE — UNE valeur : la liste des lignes (dictionnaires, valeurs nettoyées
      de leurs espaces).
      [rend: 1]
    ⑥ TRAITEMENT — csv.DictReader ; en-tête comparé à `colonnes` ; une ligne qui
      porte un champ en trop (un « ; » dans un texte), un champ manquant, ou une
      valeur qui contient un saut de ligne (un guillemet ouvrant non fermé avale
      les lignes suivantes) lève Impossible.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un « ; » glissé dans un texte décale toutes les colonnes : mieux
      vaut s'arrêter que lire une charge dans un délai.
    ⑨ CE QUI CLOCHE — Une valeur vide écrite « ; ; » reste une valeur vide : seul
      le contrôle des champs, plus loin, la juge. Mesuré le 25-11-2026 sur tous
      les planning/etapes/leviers/jalons/réglages/carte du dépôt et du planning
      réel du 17-11 : aucune ligne courte, aucun saut de ligne (m9 de la relecture
      f2ce23138).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Lecture d'un fichier local, revient toujours ou lève.
      [sort: non]
    """
    if not os.path.isfile(chemin):
        raise Impossible(f"fichier absent : {chemin}")
    try:
        with open(chemin, newline="", encoding="utf-8-sig") as f:
            lecteur = csv.DictReader(f, delimiter=";")
            entete = [c.strip() for c in (lecteur.fieldnames or [])]
            if tuple(entete) != tuple(colonnes):
                raise Impossible(f"en-tête de {os.path.basename(chemin)} : {';'.join(entete)} "
                                 f"— attendu {';'.join(colonnes)}")
            lignes = []
            for brut in lecteur:
                # line_num : la ligne PHYSIQUE où finit l'enregistrement — une ligne vide, que le lecteur saute, ne
                # décale pas le numéro (n2 de la relecture a1e52c568 : enumerate comptait les enregistrements)
                n = lecteur.line_num
                if None in brut:
                    raise Impossible(f"{os.path.basename(chemin)} ligne {n} : colonne en trop "
                                     "(un « ; » dans un texte ?)")
                # le saut de ligne d'abord : un guillemet non fermé avale la suite ET laisse la ligne courte
                if any(v is not None and ("\n" in v or "\r" in v) for v in brut.values()):
                    raise Impossible(f"{os.path.basename(chemin)} enregistrement qui se termine à la ligne {n} : "
                                     "saut de ligne dans une valeur "
                                     "(un guillemet ouvrant non fermé ?)")
                if None in brut.values():
                    raise Impossible(f"{os.path.basename(chemin)} ligne {n} : colonne manquante")
                lignes.append({k.strip(): (v or "").strip() for k, v in brut.items()})
            return lignes
    except (UnicodeDecodeError, csv.Error) as e:
        raise Impossible(f"{chemin} illisible : {e}")


def lire_reglages(chemin):
    """Rend les réglages de la méthode, lus dans REGLAGES_DU_PLANNING.csv.

    ① RÔLE — Donner au contrôle ses seuils et ses listes sans les écrire dans le
      code.
    ② CONTEXTE D APPEL — Par controler, une fois.
    ③ ENTRÉE — `chemin` : le fichier des réglages.
    ④ CONDITIONS D ENTRÉE — Toutes les clés de REGLAGES_NOMBRES et
      REGLAGES_LISTES présentes, les nombres finis. Sinon Impossible.
    ⑤ SORTIE — UNE valeur : un dictionnaire (nombres et listes).
      [rend: 1]
    ⑥ TRAITEMENT — lire_table ; nombres lus par `nombre` ; listes découpées sur
      « | » ou « , ».
    ⑦ UNITÉ — fraicheur_max_h en heures, plafond_forfait_pct en %,
      points_par_pourcent en points, remise_a_zero_max_j en jours,
      disque_min_go en Go.
    ⑧ POURQUOI — Un seuil se lit dans un fichier, jamais dans le code (cadre
      commun du plan V7, point 4).
    ⑨ CE QUI CLOCHE — Le fichier n'est pas au registre des règles : sa place est
      une question posée à Jean-Luc.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Revient toujours ou lève.
      [sort: non]
    """
    brut = {l["cle"]: l["valeur"] for l in lire_table(chemin, ("cle", "valeur", "raison"))}
    manque = [c for c in REGLAGES_NOMBRES + REGLAGES_LISTES if not brut.get(c)]
    if manque:
        raise Impossible(f"réglages incomplets : {', '.join(manque)}")
    r = {}
    for c in REGLAGES_NOMBRES:
        r[c] = nombre(brut[c])
        if r[c] is None:
            raise Impossible(f"réglage {c} non numérique")
    for c in REGLAGES_LISTES:
        r[c] = [x.strip() for x in re.split(r"[|,]", brut[c]) if x.strip()]
    return r


def nombre(texte):
    """Rend un nombre FINI écrit avec une virgule ou un point décimal, ou None.

    ① RÔLE — La seule lecture d'un nombre du planning et des réglages.
    ② CONTEXTE D APPEL — Par lire_reglages et controler, pour chaque champ
      numérique.
    ③ ENTRÉE — `texte`.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nombre, ou None s'il ne se lit pas ou n'est pas
      fini (« nan », « inf »).
      [rend: 1]
    ⑥ TRAITEMENT — virgule remplacée par un point ; float ; math.isfinite.
    ⑦ UNITÉ — celle du champ.
    ⑧ POURQUOI — Jean-Luc écrit « 1,5 ». « nan » passait toutes les
      comparaisons (« nan < 0 » est faux) et retirait des étapes du chemin
      critique : un planning sans leviers était accepté (relecteur neuf du
      11-11-2026, D1).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    try:
        x = float(texte.replace(",", "."))
    except (ValueError, AttributeError):
        return None
    return x if math.isfinite(x) else None


def heure(texte):
    """Rend une heure de Paris écrite « AAAA-MM-JJ HH:MM », ou None.

    ① RÔLE — La seule lecture d'une heure écrite dans les CSV du planning.
    ② CONTEXTE D APPEL — Par controler et main.
    ③ ENTRÉE — `texte`.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : datetime avec fuseau de Paris, ou None.
      [rend: 1]
    ⑥ TRAITEMENT — strptime au format du fichier de jalons (même format que le
      veilleur, §13.5 geste 4).
    ⑦ UNITÉ — heure de Paris.
    ⑧ POURQUOI — Un seul format d'heure dans tout l'outil planning.
    ⑨ CE QUI CLOCHE — L'heure absente du changement d'heure de mars n'est pas
      traitée (même limite que le veilleur).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    try:
        return datetime.datetime.strptime((texte or "").strip(), "%Y-%m-%d %H:%M").replace(tzinfo=P)
    except ValueError:
        return None


def date_du_fichier(chemin):
    """Rend l'heure écrite dans les cinq premières lignes d'un fichier de jugement, ou None.

    ① RÔLE — Dater le jugement de l'auteur et l'estimation de l'expert, pour
      vérifier que l'expert vient APRÈS.
    ② CONTEXTE D APPEL — Par controler, deux fois.
    ③ ENTRÉE — `chemin` : le fichier.
    ④ CONDITIONS D ENTRÉE — Fichier lisible ; sinon None.
    ⑤ SORTIE — UNE valeur : datetime de Paris, ou None si aucune date n'est lue.
      [rend: 1]
    ⑥ TRAITEMENT — Cherche d'abord « AAAA-MM-JJ HH:MM », sinon « JJ-MM-AAAA »
      suivi, à moins de 40 caractères, d'une heure « HHhMM » ou « HH:MM ».
      Exemples réels : « écrit le Mer 11-11-2026 à 22h00 » ; « Écrit le mercredi
      11-11-2026, vers 22h15 » ; « écrite le Mer 11-11-2026 à 23:13 (Paris) »
      (expert neuf du tour 7, refusé « non datée » avant le 11-11-2026 23h30 :
      les deux écritures d'une heure sont acceptées, pas une seule).
    ⑦ UNITÉ — heure de Paris.
    ⑧ POURQUOI — §13.4 ③ : le jugement de l'auteur est daté AVANT tout autre
      avis ; la date doit être lisible par programme.
    ⑨ CE QUI CLOCHE — La date est celle que l'auteur a écrite, pas celle du
      fichier sur le disque ni du commit.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Lecture locale, revient toujours.
      [sort: non]
    """
    try:
        with open(chemin, encoding="utf-8") as f:
            tete = "".join(f.readline() for _ in range(5))
    except (OSError, UnicodeDecodeError):
        return None
    m = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", tete)
    if m:
        return heure(m.group(1))
    m = re.search(r"(\d{2})-(\d{2})-(\d{4})\D{1,40}?(\d{1,2})[h:](\d{2})", tete)
    if not m:
        return None
    j, mo, a, h, mi = (int(x) for x in m.groups())
    try:
        return datetime.datetime(a, mo, j, h, mi, tzinfo=P)
    except ValueError:
        return None


def calculer_chemin(duree, deps):
    """Calcule fin du projet, marges et étapes critiques à partir des dépendances.

    ① RÔLE — Le cœur d'A-698 : la méthode du chemin critique, faite par
      programme et non à la main.
    ② CONTEXTE D APPEL — Par controler, deux fois (délais min et max).
    ③ ENTRÉE — `duree` : {étape: heures} ; `deps` : {étape: liste d'étapes}.
    ④ CONDITIONS D ENTRÉE — Dépendances connues et sans cycle (vérifié par
      l'appelant, qui ne l'appelle pas sinon).
    ⑤ SORTIE — TROIS valeurs : la fin (heures depuis le début), {étape: (début
      au plus tôt, fin au plus tôt, marge)}, la liste ordonnée des étapes
      critiques (marge nulle).
      [rend: 3]
    ⑥ TRAITEMENT — Ordre topologique ; passe avant (début = max des fins des
      dépendances) ; passe arrière (fin au plus tard = min des débuts au plus
      tard des suivantes, ou la fin du projet) ; marge = fin au plus tard − fin
      au plus tôt ; critique si marge < 1e-9.
    ⑦ UNITÉ — heures.
    ⑧ POURQUOI — §13.0bis : « Calculer le chemin critique : la plus longue
      chaîne de dépendances jusqu'à la fin ».
    ⑨ CE QUI CLOCHE — Ressources supposées illimitées ; aucun calendrier : la
      remise à zéro du forfait est appliquée ensuite par planifier_sous_forfait.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Boucles bornées par le nombre d'étapes ; revient toujours.
      [sort: non]
    """
    ordre, faits = [], set()
    while len(ordre) < len(duree):
        for e in sorted(duree):
            if e not in faits and all(d in faits for d in deps[e]):
                ordre.append(e)
                faits.add(e)
    tot = {}
    for e in ordre:
        debut = max((tot[d][1] for d in deps[e]), default=0.0)
        tot[e] = (debut, debut + duree[e])
    fin = max((v[1] for v in tot.values()), default=0.0)
    suivantes = {e: [s for s in duree if e in deps[s]] for e in duree}
    tard = {}
    for e in reversed(ordre):
        lf = min((tard[s] - duree[s] for s in suivantes[e]), default=fin)
        tard[e] = lf
    res = {e: (tot[e][0], tot[e][1], tard[e] - tot[e][1]) for e in ordre}
    critiques = [e for e in ordre if res[e][2] < 1e-9]
    return fin, res, critiques


def premier_creneau(t0, d, poses, cap):
    """Rend la première heure ≥ t0 où une étape de durée d tient sous la limite de concurrence.

    ① RÔLE — La limite « agents_simultanes_max » de planning.csv : jamais plus de
      `cap` étapes occupant un agent en même temps.
    ② CONTEXTE D APPEL — Par planifier_sous_forfait, pour chaque étape qui occupe un agent.
    ③ ENTRÉE — `t0` : heure au plus tôt (heures depuis maintenant) ; `d` : durée (h) ;
      `poses` : liste des intervalles (début, fin) déjà placés qui occupent un agent ;
      `cap` : entier ≥ 1, ou None (aucune limite).
    ④ CONDITIONS D ENTRÉE — d ≥ 0 ; cap ≥ 1 ou None.
    ⑤ SORTIE — UNE valeur : l'heure de début retenue.
      [rend: 1]
    ⑥ TRAITEMENT — Candidats : t0 puis chaque fin d'intervalle placé après t0, dans
      l'ordre ; un candidat t est retenu si, à t et à chaque début d'intervalle placé
      dans ]t, t+d[, moins de `cap` intervalles sont ouverts.
    ⑦ UNITÉ — heures depuis maintenant.
    ⑧ POURQUOI — Décision du 16-11-2026 : le Chat lance rarement plus de 3 agents à
      la fois ; sans cette limite, 14 étapes en cours partaient toutes à l'heure zéro.
    ⑨ CE QUI CLOCHE — Compte des ÉTAPES, pas des agents : une étape qui en déclare
      18 compte pour une. Une étape de durée nulle n'occupe rien.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Au plus len(poses)+1 candidats ; revient toujours.
      [sort: non]
    """
    if cap is None or d <= 0:
        return t0
    ouverts = lambda x: sum(1 for a, b in poses if a <= x + 1e-9 and x < b - 1e-9)
    for t in [t0] + sorted(b for _, b in poses if b > t0):
        pts = [t] + [a for a, _ in poses if t < a < t + d - 1e-9]
        if all(ouverts(x) < cap for x in pts):
            return t
    return max([t0] + [b for _, b in poses])


def planifier_sous_forfait(duree, deps, points, marge, budget_avant, raz_h, occupe=(), cap=None, permis_avant=None):
    """Place chaque étape avant ou après la remise à zéro du forfait, et en tire les fins réelles.

    ① RÔLE — Le calendrier réel du forfait : avant la remise à zéro, seuls les
      points qui restent sous le plafond peuvent être dépensés ; une étape qui ne
      tient pas dans ce reste attend la remise à zéro.
    ② CONTEXTE D APPEL — Par controler (bloc C10), deux fois : délais et points
      minimaux (au mieux), puis maximaux (réaliste).
    ③ ENTRÉE — `duree` : {étape: heures restantes, 0 si tenue} ; `deps` :
      {étape: liste d'étapes} ; `points` : {étape: points de forfait, 0 si
      tenue} ; `marge` : {étape: marge en heures du chemin critique sans
      forfait, qui donne l'ordre de priorité} ; `budget_avant` : points
      disponibles avant la remise à zéro ; `raz_h` : heures de maintenant à la
      remise à zéro (> 0) ; `occupe` : étapes qui occupent un agent ; `cap` :
      agents_simultanes_max (None = sans limite) ; `permis_avant` : ensemble
      des étapes autorisées avant la remise à zéro (None = toutes).
    ④ CONDITIONS D ENTRÉE — Dépendances connues et sans cycle, mêmes clés dans
      les quatre dictionnaires (vérifié par l'appelant).
    ⑤ SORTIE — CINQ valeurs : la fin (heures depuis maintenant) ; {étape:
      (début, fin, « avant » ou « après »)} ; la liste ordonnée des étapes
      placées avant (tenues comprises : l'appelant les retire de l'affichage) ; celle des étapes placées après ; les points
      dépensés avant.
      [rend: 5]
    ⑥ TRAITEMENT — Une seule passe : parmi les étapes dont toutes les
      dépendances sont placées, prendre celle de plus petite marge (puis
      l'identifiant) — c'est l'ordre du chemin critique. Son début libre est la
      plus tardive des fins de ses dépendances, retardé par premier_creneau si
      elle occupe un agent (`occupe`) et que `cap` étapes tournent déjà. Elle
      passe AVANT si ce début tombe avant la remise à zéro, si elle figure dans
      `permis_avant` (None = toutes ; A-834), si aucune de ses dépendances n'est
      APRÈS et si ses points tiennent dans ce qui reste du budget ; sinon elle
      passe APRÈS, ne commence pas avant la remise à zéro et attend elle aussi
      un créneau sous `cap`. Une étape à zéro point (tenue, ou attente de
      Jean-Luc) ne consomme rien ; une étape de durée nulle (tenue) n'est
      jamais retenue par `permis_avant`.
    ⑦ UNITÉ — heures depuis maintenant ; points de forfait.
    ⑧ POURQUOI — Le 16-11-2026 à 09h05, Jean-Luc : « Pourquoi tu n'en tiens pas
      compte? Je comprends pas, je demande un planning réel. » La jauge était à
      66 % (capture de 07h57), remise à zéro le 18-11 à 01h59, et le contrôle
      rendait « 95 points jusqu'à 95 % » et une fin calculée comme si tout le
      travail pouvait partir tout de suite.
    ⑨ CE QUI CLOCHE — Les points d'une étape sont comptés EN ENTIER dans la
      fenêtre où elle commence, même si elle déborde la remise à zéro. La
      fenêtre d'après est supposée assez grande : son dépassement est signalé
      par l'appelant, aucune troisième fenêtre n'est calculée. Gourmand, pas optimal : une petite étape
      à forte marge peut rester après alors qu'un autre ordre l'aurait casée.
      La limite de concurrence compte des étapes, pas des agents.
      Les étapes qui n'attendent que Jean-Luc ont 0 point : le budget ne les
      retarde jamais.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Une étape placée par tour, autant de tours que d'étapes ;
      revient toujours.
      [sort: non]
    """
    place, avant, apres, poses = {}, [], [], []
    reste = budget_avant
    while len(place) < len(duree):
        pretes = [e for e in duree if e not in place and all(d in place for d in deps[e])]
        e = min(pretes, key=lambda x: (marge[x], x))
        libre = max((place[d][1] for d in deps[e]), default=0.0)
        compte = e in occupe and duree[e] > 0
        tot = premier_creneau(libre, duree[e], poses, cap) if compte else libre
        permis = permis_avant is None or e in permis_avant or duree[e] == 0
        if (tot < raz_h and permis and all(place[d][2] == "avant" for d in deps[e])
                and points[e] <= reste + 1e-9):
            reste -= points[e]
            place[e] = (tot, tot + duree[e], "avant")
            avant.append(e)
        else:
            debut = max(libre, raz_h)
            if compte:
                debut = premier_creneau(debut, duree[e], poses, cap)
            place[e] = (debut, debut + duree[e], "après")
            apres.append(e)
        if compte:
            poses.append(place[e][:2])
    fin = max((v[1] for v in place.values()), default=0.0)
    return fin, place, avant, apres, budget_avant - reste


def a_un_cycle(deps):
    """Dit si les dépendances forment un cycle, et le nomme.

    ① RÔLE — Refuser un planning dont aucune étape ne pourrait démarrer.
    ② CONTEXTE D APPEL — Par controler, avant calculer_chemin.
    ③ ENTRÉE — `deps` : {étape: liste d'étapes connues}.
    ④ CONDITIONS D ENTRÉE — Toutes les dépendances sont des étapes connues.
    ⑤ SORTIE — UNE valeur : la liste des étapes prises dans un cycle (vide s'il
      n'y en a pas).
      [rend: 1]
    ⑥ TRAITEMENT — Retire une à une les étapes dont les dépendances sont
      retirées ; ce qui reste est pris dans un cycle (ou en dépend).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Sans ce contrôle, la passe avant de calculer_chemin ne
      finirait pas.
    ⑨ CE QUI CLOCHE — Nomme aussi les étapes qui dépendent d'un cycle sans en
      faire partie.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Au plus autant de tours que d'étapes ; revient toujours.
      [sort: non]
    """
    reste = dict(deps)
    change = True
    while change:
        change = False
        for e in sorted(reste):
            if all(d not in reste for d in reste[e]):
                del reste[e]
                change = True
    return sorted(reste)


# La dernière date que les calculs de fin peuvent écrire : la plus grande date de Python, moins un jour pour le
# passage à l'heure de Paris (montrer ajoute en temps universel PUIS convertit ; à la toute fin, la conversion déborde).
FIN_DU_CALENDRIER = datetime.datetime.max.replace(tzinfo=datetime.timezone.utc) - datetime.timedelta(days=1)


def heures_jusqu_a_la_fin_du_calendrier(debut):
    """Rend le nombre d'heures entre `debut` et FIN_DU_CALENDRIER.

    ① RÔLE — La seule borne des calculs de fin (C8bis du contrôle) : au-delà, montrer déborderait.
    ② CONTEXTE D APPEL — Par controler, une fois, juste après la lecture des étapes.
    ③ ENTRÉE — `debut` : datetime avec fuseau (maintenant).
    ④ CONDITIONS D ENTRÉE — `debut` antérieur à FIN_DU_CALENDRIER.
    ⑤ SORTIE — UNE valeur : un nombre d'heures (float).
      [rend: 1]
    ⑥ TRAITEMENT — différence en temps universel, en heures.
    ⑦ UNITÉ — heures.
    ⑧ POURQUOI — Relecture a1e52c568 (n1) et superviseurs R-759 du 25-11-2026 : delai_h_max = 1e12 levait
      OverflowError dans montrer ; la borne se compare en nombre, sans fabriquer de timedelta (qui déborde seul).
    ⑨ CE QUI CLOCHE — Borne de calendrier, pas de vraisemblance : un délai de 5e7 h (~5 700 ans) passe. Une plage
      plausible est une décision de Jean-Luc (question posée le 25-11-2026, BACKLOG).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    return (FIN_DU_CALENDRIER - debut.astimezone(datetime.timezone.utc)).total_seconds() / 3600


def montrer(debut, heures):
    """Rend une heure de fin lisible : « Jjj JJ-MM-AAAA HHhMM ».

    ① RÔLE — Afficher les fins calculées en heures de Paris.
    ② CONTEXTE D APPEL — Par controler.
    ③ ENTRÉE — `debut` : datetime de Paris ; `heures` : durée depuis le début.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte.
      [rend: 1]
    ⑥ TRAITEMENT — addition en temps universel, puis retour à Paris.
    ⑦ UNITÉ — heure de Paris.
    ⑧ POURQUOI — §13.1 règle 8 : présenter le plan en heures de début et de fin.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    t = (debut.astimezone(datetime.timezone.utc) + datetime.timedelta(hours=heures)).astimezone(P)
    return f"{JOURS[t.weekday()]} {t:%d-%m-%Y %Hh%M}"


def chemin_de(tete, dossier, cle):
    """Rend le chemin d'un fichier nommé dans planning.csv, relatif au dossier du planning.

    ① RÔLE — Résoudre les chemins du jugement, de l'expert et des jalons.
    ② CONTEXTE D APPEL — Par controler.
    ③ ENTRÉE — `tete` : l'en-tête lue ; `dossier` : le dossier du planning ;
      `cle` : la clé du chemin.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin (absolu tel quel, relatif joint au
      dossier), ou « » si la clé manque.
      [rend: 1]
    ⑥ TRAITEMENT — os.path.join si le chemin est relatif.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un planning se déplace avec ses fichiers.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    v = tete.get(cle, "")
    return v if not v or os.path.isabs(v) else os.path.join(dossier, v)


def recent(tete, cle, quoi, maintenant, frais_h, refus):
    """Lit une heure de l'en-tête et ajoute un motif si elle manque, est future ou périmée.

    ① RÔLE — Contrôler la date de la capture du forfait et du relevé des
      ressources.
    ② CONTEXTE D APPEL — Par controler, deux fois.
    ③ ENTRÉE — `tete`, `cle`, `quoi` (le nom affiché), `maintenant`, `frais_h`
      (fraîcheur maximale, lue aux réglages), `refus` (liste complétée).
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : l'heure lue, ou None.
      [rend: 1]
    ⑥ TRAITEMENT — heure() ; âge en heures, comparé en temps universel.
    ⑦ UNITÉ — heures.
    ⑧ POURQUOI — §13.2.0 : « tout chiffre plus vieux que la journée est
      périmé » ; mission du 11-11-2026 : capture « DATÉE de moins de 24 h ».
    ⑨ CE QUI CLOCHE — La date est écrite par le Chat : rien ne prouve qu'elle
      est celle de la capture de Jean-Luc.
    ⑩ EFFET — Ajoute à `refus`.
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    t = heure(tete.get(cle, ""))
    if t is None:
        refus.append(f"{quoi} NON DATÉ : clé « {cle} » absente ou hors format AAAA-MM-JJ HH:MM")
        return None
    age = (maintenant.astimezone(datetime.timezone.utc) - t.astimezone(datetime.timezone.utc)).total_seconds() / 3600
    if age < 0:
        refus.append(f"{quoi} DATÉ DANS LE FUTUR : {tete[cle]}")
    elif age > frais_h:
        refus.append(f"{quoi} PÉRIMÉ : {tete[cle]}, il y a {age:.1f} h (plus de {frais_h:g} h) — refaire la capture")
    return t


def mot_de_jugement(texte, permis):
    """Rend le mot de jugement par lequel commence un texte, ou None.

    ① RÔLE — Lire le jugement de l'auteur sur une étape (« LONG : le lot B… »).
    ② CONTEXTE D APPEL — Par controler, une fois par étape.
    ③ ENTRÉE — `texte` : la cellule ; `permis` : les mots permis (réglages).
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le mot permis (en capitales), ou None.
      [rend: 1]
    ⑥ TRAITEMENT — le plus long mot permis d'abord ; il doit être suivi d'autre
      chose qu'une lettre ou un chiffre.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un préfixe acceptait « JUSTEMENT FAUX » comme « JUSTE »
      (relecteur neuf du 11-11-2026, D2).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    t = texte.strip().upper()
    for p in sorted(permis, key=len, reverse=True):
        if re.match(re.escape(p.upper()) + r"(?![\wÀ-ÿ])", t):
            return p.upper()
    return None


def estimer_le_forfait(capture, pct, raz, maintenant, periode_h, frais_h, forcer=False):
    """Rend le forfait à utiliser maintenant : le relevé s'il vaut encore, sinon une estimation marquée ESTIMÉ.

    ① RÔLE — Supprimer le frein « pas de relevé, pas de dates » (A-899) : sans
      relevé valide de Jean-Luc, le pourcentage consommé et la remise à zéro
      suivante sont ESTIMÉS à partir du dernier relevé ; un relevé réel, dès
      qu'il est frais, remplace l'estimation.
    ② CONTEXTE D APPEL — Par controler (bloc C4), une fois ; par
      ORDONNER_UN_PLANNING.journaliser_le_forfait avec `forcer=True`, pour
      calculer ce que l'estimateur aurait dit à l'heure d'un nouveau relevé.
    ③ ENTRÉE — `capture` : heure du dernier relevé (datetime de Paris) ; `pct` :
      pourcentage relevé (0 à 100) ; `raz` : remise à zéro écrite avec ce relevé ;
      `maintenant` ; `periode_h` : période du forfait en heures (réglage
      remise_a_zero_max_j × 24, la remise à zéro est hebdomadaire) ; `frais_h` :
      fraîcheur maximale (réglage fraicheur_max_h) ; `forcer` : estimer même si
      le relevé est valide.
    ④ CONDITIONS D ENTRÉE — capture, pct et raz lus (non None), capture ≤
      maintenant, capture < raz ≤ capture + periode_h, periode_h > 0 : vérifié
      par l'appelant, qui ne l'appelle pas sinon.
    ⑤ SORTIE — QUATRE valeurs : la source (« RELEVÉ » ou « ESTIMÉ »), le
      pourcentage (borné à 100), la remise à zéro à venir (datetime >
      maintenant), le texte du calcul affiché.
      [rend: 4]
    ⑥ TRAITEMENT — Relevé valide (âge ≤ frais_h et raz future) et non forcé →
      rendu tel quel. Sinon : début de la fenêtre du relevé = raz − période ;
      taux = pct ÷ heures entre ce début et la capture (0 si aucune heure) ;
      remise à zéro avancée de période en période jusqu'à passer maintenant ;
      même fenêtre → pct + taux × heures depuis la capture ; fenêtre suivante →
      taux × heures depuis le début de la fenêtre courante.
    ⑦ UNITÉ — pourcentage de la jauge ; heures ; heures de Paris comparées en UTC.
    ⑧ POURQUOI — Jean-Luc, 18-11-2026 à 12h36 (A-899) : « La mécanique d'arrêt
      ou de ralentissement parce que tu n'as pas reçu le forfait ne doit pas
      exister […] tu dois partir sur les principes que tu as, estimer la
      consommation ». Le 18-11 à 11h52, le contrôle ne datait aucune étape
      (« non calculée — remise à zéro absente ou passée »). Le taux se tire du
      relevé lui-même : 5 % relevés le 18-11 à 12h36, remise à zéro le 25-11 à
      02h00, donc fenêtre ouverte le 18-11 à 02h00, 10,6 h → 0,47 % par heure.
    ⑨ CE QUI CLOCHE — Le taux suppose une consommation régulière depuis le début
      de la fenêtre : un relevé pris juste après la remise à zéro donne un taux
      instable. L'écart relevé − estimation est journalisé par l'ordonnanceur,
      jamais réinjecté : corriger l'estimateur reste une décision.
    ⑩ EFFET — —
    ⑪ TERMINAISON — La boucle d'avance de la remise à zéro est bornée par
      (maintenant − raz) ÷ période + 1 tours ; revient toujours.
      [sort: non]
    """
    U = datetime.timezone.utc
    h = lambda a, b: (a.astimezone(U) - b.astimezone(U)).total_seconds() / 3600
    age = h(maintenant, capture)
    if not forcer and age <= frais_h and h(raz, maintenant) > 0:
        return "RELEVÉ", pct, raz, f"RELEVÉ de {capture:%Y-%m-%d %H:%M} ({age:.1f} h) : {pct:g} %"
    debut_rel = raz - datetime.timedelta(hours=periode_h)
    base = h(capture, debut_rel)
    taux = pct / base if base > 0 else 0.0
    raz_now = raz
    while h(raz_now, maintenant) <= 0:
        raz_now = raz_now + datetime.timedelta(hours=periode_h)
    if raz_now == raz:
        est = pct + taux * max(age, 0.0)
        quoi = f"{pct:g} % + {taux:.3g} %/h × {age:.1f} h depuis le relevé"
    else:
        depuis = h(maintenant, raz_now - datetime.timedelta(hours=periode_h))
        est = taux * depuis
        quoi = f"remise à zéro passée ; {taux:.3g} %/h × {depuis:.1f} h depuis la remise à zéro du " \
               f"{raz_now - datetime.timedelta(hours=periode_h):%Y-%m-%d %H:%M}"
    est = min(est, 100.0)
    return "ESTIMÉ", est, raz_now, (f"ESTIMÉ {est:.1f} % = {quoi} (taux = {pct:g} % relevés le {capture:%Y-%m-%d %H:%M} "
                                    f"÷ {base:.1f} h depuis le début de leur fenêtre) ; remise à zéro {raz_now:%Y-%m-%d %H:%M}")


def etapes_pretes(ids, deps, etat, qui_liberent):
    """Rend les étapes PRÊTES : à faire, et dont toutes les dépendances sont dans un état qui libère.

    ① RÔLE — LA définition de « prête », la seule (R-708 : deux implémentations
      d'une même chose divergent toujours).
    ② CONTEXTE D APPEL — Par ORDONNER_UN_PLANNING.situation seulement ; le
      contrôle lit « prête » dans situation (M5 de la relecture 8887e31e).
    ③ ENTRÉE — `ids` : identifiants ; `deps` : {étape: dépendances} ; `etat` :
      {étape: état parmi les états des réglages} ; `qui_liberent` : liste des
      états qui libèrent (réglage etats_qui_liberent).
    ④ CONDITIONS D ENTRÉE — Toute dépendance est dans `etat`.
    ⑤ SORTIE — UNE valeur : la liste des étapes prêtes, dans l'ordre de `ids`.
      [rend: 1]
    ⑥ TRAITEMENT — état « a_faire » et toutes les dépendances dans `qui_liberent`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur R-759 du 18-11-2026 : « une seule définition de
      « prête » » partagée par le contrôle et l'ordonnanceur.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    return [i for i in ids if etat[i] == "a_faire" and all(etat[d] in qui_liberent for d in deps[i])]


def racine_du_depot(dossier):
    """Rend le premier dossier parent qui porte un « .git », ou None.

    ① RÔLE — Trouver la racine du dépôt pour lire les chemins de programmes de
      la carte des pannes, écrits relatifs à elle.
    ② CONTEXTE D APPEL — Par controler (bloc C13, la racine qu'il passe à
      controler_la_carte) et par ORDONNER_UN_PLANNING.
    ③ ENTRÉE — `dossier` : un chemin.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin absolu, ou None.
      [rend: 1]
    ⑥ TRAITEMENT — remonte les parents jusqu'à la racine du disque.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une carte vaut pour tout le projet : ses chemins ne dépendent
      pas du dossier du planning.
    ⑨ CE QUI CLOCHE — Un dossier hors de tout dépôt rend None : la carte est
      alors refusée (chemin invérifiable). Une copie sans « .git » (celle des
      épreuves longues sur GitHub) n'a pas de racine : un appelant qui CONNAÎT
      la racine la passe lui-même (B7 de la relecture f2ce23138).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Au plus la profondeur du chemin ; revient toujours.
      [sort: non]
    """
    d = os.path.abspath(dossier)
    while True:
        if os.path.exists(os.path.join(d, ".git")):
            return d
        p = os.path.dirname(d)
        if p == d:
            return None
        d = p


def age_du_signe(texte, maintenant):
    """Rend l'âge, en minutes, d'une ligne de signe de vie, ou None si elle est absente ou hors format.

    ① RÔLE — La seule lecture d'un signe de vie (R-708) : le contrôle (bloc C14) et le chien de garde de
      l'ordonnanceur l'appellent.
    ② CONTEXTE D APPEL — Par controler et par ORDONNER_UN_PLANNING.chien_de_garde.
    ③ ENTRÉE — `texte` : la ligne « SIGNE DE VIE <heure ISO avec décalage> · … » ; `maintenant` : datetime de Paris.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : l'âge en minutes (négatif si la ligne est datée dans le futur), ou None.
      [rend: 1]
    ⑥ TRAITEMENT — motif « SIGNE DE VIE <mot> » ; datetime.fromisoformat ; écart en temps universel.
    ⑦ UNITÉ — minutes.
    ⑧ POURQUOI — A-904 (choix « 1 » de Jean-Luc, 18-11-2026 13h33) et sa précision de 13h43 : le chien de garde
      « bien aussi dans l'outil de planification, en autoportant et par programme » ; A-905 (13h46) : l'alerte part
      par la notification de l'application Claude. Cas fondateur : 18-11-2026, machine arrêtée de 08h17 à 11h43,
      personne prévenu.
    ⑨ CE QUI CLOCHE — L'heure est celle qu'a écrite l'ordonnanceur.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    m = re.match(r"SIGNE DE VIE (\S+)", (texte or "").strip())
    try:
        quand = datetime.datetime.fromisoformat(m.group(1)) if m else None
    except ValueError:
        quand = None
    if quand is None or quand.tzinfo is None:
        return None
    U = datetime.timezone.utc
    return (maintenant.astimezone(U) - quand.astimezone(U)).total_seconds() / 60


def controler_la_carte(chemin, racine, R, refus, signaux):
    """Contrôle la carte des pannes du projet : présente, chaque catégorie traitée, chaque ligne bien formée.

    ① RÔLE — Rendre la carte des pannes obligatoire pour tout planning (A-898),
      UNE carte par projet, partagée par ses plannings.
    ② CONTEXTE D APPEL — Par controler (bloc C13), une fois, avec
      racine_du_depot du dossier de la carte ; par l'épreuve k13 avec la racine
      de l'arbre qui porte le fichier d'épreuves (B7 de la relecture f2ce23138 :
      la copie jouée sur GitHub n'a pas de « .git », la racine ne s'y devine pas).
    ③ ENTRÉE — `chemin` : la carte (clé carte_des_pannes de planning.csv) ;
      `racine` : la racine du dépôt, à laquelle les chemins de « detection »
      sont relatifs, ou None (aucune : toute détection par programme refusée) ;
      `R` : réglages (categories_de_pannes, executants_de_pannes) ; `refus`,
      `signaux` : listes complétées.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nombre de lignes lues (0 si la carte manque).
      [rend: 1]
    ⑥ TRAITEMENT — lire_table (en-tête COLONNES_PANNES) ; pour chaque ligne :
      catégorie connue ; « detection » = un chemin existant relatif à la racine
      du dépôt (premier mot), ou « NON PROGRAMMABLE : raison » (signalé), ou
      « SANS OBJET : raison » (la catégorie ne concerne pas ce projet) ; réponse
      non vide hors SANS OBJET ; tenue_par dans les exécutants. Puis chaque
      catégorie des réglages a au moins une ligne (réelle ou SANS OBJET).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Jean-Luc, 18-11-2026 à 12h31 (A-898) : « le lancement de la
      cartographie et le calcul des pannes potentielles et des réparations est
      intégré dans le planning » ; superviseur du 18-11 : une carte par projet,
      « SANS OBJET : raison » admis. Cas réel : arrêt de la machine à 08h17,
      rien relancé avant 11h43.
    ⑨ CE QUI CLOCHE — Forme seulement : il voit qu'un programme EXISTE, jamais
      qu'il détecte la panne. Une raison d'un mot passe.
    ⑩ EFFET — Ajoute à `refus` et `signaux`.
    ⑪ TERMINAISON — Lecture locale ; revient toujours ou lève Impossible
      (fichier présent mais illisible).
      [sort: non]
    """
    if not chemin or not os.path.isfile(chemin):
        refus.append(f"CARTE DES PANNES ABSENTE : {chemin or '(clé « carte_des_pannes » manquante)'} — "
                     "une carte par projet, obligatoire (A-898)")
        return 0
    lignes = lire_table(chemin, COLONNES_PANNES)
    vues = set()
    for n, l in enumerate(lignes, start=2):
        quoi = f"CARTE DES PANNES ligne {n} ({l['panne'] or '?'})"
        if l["categorie"] not in R["categories_de_pannes"]:
            refus.append(f"{quoi} : catégorie « {l['categorie']} » hors de {', '.join(R['categories_de_pannes'])}")
        else:
            vues.add(l["categorie"])
        det = l["detection"]
        if det.upper().startswith(SANS_OBJET):
            if not det[len(SANS_OBJET):].strip():
                refus.append(f"{quoi} : « {SANS_OBJET} » sans raison")
            continue
        if det.upper().startswith(NON_PROGRAMMABLE):
            if not det[len(NON_PROGRAMMABLE):].strip():
                refus.append(f"{quoi} : « {NON_PROGRAMMABLE} » sans raison")
            else:
                signaux.append(f"{quoi} NON PROGRAMMABLE : {det[len(NON_PROGRAMMABLE):].strip()}")
        else:
            prog = det.split()[0].rstrip(":,;") if det.split() else ""
            if not prog or racine is None or not os.path.isfile(os.path.join(racine, prog)):
                refus.append(f"{quoi} : la détection doit commencer par le chemin d'un programme existant (relatif "
                             f"à la racine du dépôt), ou « {NON_PROGRAMMABLE} raison », ou « {SANS_OBJET} raison » — "
                             f"lu « {prog or det} »")
        if not l["reponse"]:
            refus.append(f"{quoi} : réponse vide")
        if l["tenue_par"] not in R["executants_de_pannes"]:
            refus.append(f"{quoi} : tenue_par « {l['tenue_par']} » hors de {', '.join(R['executants_de_pannes'])}")
    manque = [c for c in R["categories_de_pannes"] if c not in vues]
    if manque:
        refus.append(f"CARTE DES PANNES : catégorie(s) non traitée(s) {', '.join(manque)} — une ligne, ou "
                     f"« {SANS_OBJET} raison »")
    return len(lignes)


def controler(dossier, maintenant, reglages_chemin=REGLAGES):
    """Contrôle un planning entier et rend ses lignes de calcul, ses signaux et ses motifs de refus.

    ① RÔLE — Toute la décision du programme, sans affichage ni sortie, pour être
      éprouvée.
    ② CONTEXTE D APPEL — Par main.
    ③ ENTRÉE — `dossier` : le dossier du planning ; `maintenant` : datetime de
      Paris ; `reglages_chemin` : le fichier des réglages.
    ④ CONDITIONS D ENTRÉE — Fichiers lisibles ; sinon Impossible.
    ⑤ SORTIE — TROIS valeurs : les lignes « CALCUL … » (dont « fin réelle
      (forfait compris) » et les listes avant/après la remise à zéro), les
      signaux, la liste des motifs de refus (vide = accepté).
      [rend: 3]
    ⑥ TRAITEMENT — Les blocs C1 à C14 du ⑥ de la fiche du programme, dans cet
      ordre ; chaque bloc porte son repère en commentaire. Toutes les fins
      partent de `maintenant`, plus de la clé « debut ».
    ⑦ UNITÉ — heures, points, pourcentage, Go.
    ⑧ POURQUOI — Voir la fiche du programme.
    ⑨ CE QUI CLOCHE — Forme et calcul seulement (fiche du programme, ⑨). Le
      reste des étapes en cours est celui du relevé du début, compté en entier.
      La fin réelle n'est calculée que si le pourcentage, la remise à zéro
      (future) et les points de toutes les étapes non tenues se lisent. Le
      calcul ne tourne pas si une étape a un délai illisible, une dépendance
      inconnue ou un identifiant en double : les contrôles C10 à C12 qui en
      dépendent sont alors sautés, et le refus déjà posé suffit.
    ⑩ EFFET — Aucun : passage_unique du veilleur n'écrit rien.
    ⑪ TERMINAISON — Revient toujours ou lève Impossible.
      [sort: non]
    """
    # C1 — lire réglages et fichiers
    R = lire_reglages(reglages_chemin)
    if not os.path.isdir(dossier):
        raise Impossible(f"dossier du planning absent : {dossier}")
    tete_l = lire_table(os.path.join(dossier, "planning.csv"), ("cle", "valeur"))
    etapes = lire_table(os.path.join(dossier, "etapes.csv"), COLONNES_ETAPES)
    leviers = lire_table(os.path.join(dossier, "leviers.csv"), COLONNES_LEVIERS)
    refus, signaux, calcul = [], [], []
    frais_h = R["fraicheur_max_h"]

    # C2 — schéma fermé : toute clé hors de la liste connue est refusée (R-728 : un
    # résultat calculé recopié à la main, sous quelque nom que ce soit, tombe ici)
    tete = {}
    for l in tete_l:
        if l["cle"] in tete:
            refus.append(f"CLÉ EN DOUBLE dans planning.csv : {l['cle']}")
        elif l["cle"] not in R["cles_connues"]:
            refus.append(f"CLÉ INCONNUE dans planning.csv : « {l['cle']} » — schéma fermé ; un chemin "
                         "critique, une fin ou une marge se calculent et ne s'écrivent pas (R-728)")
        tete[l["cle"]] = l["valeur"]

    # C3 — l'objectif, en une phrase (§13.5 geste 1, n°341)
    obj = tete.get("objectif", "")
    if not obj:
        refus.append("OBJECTIF ABSENT : clé « objectif » vide ou manquante (§13.5 geste 1)")
    elif re.search(r"[.!?]\s+[A-ZÀ-Ý]", obj):
        refus.append("OBJECTIF EN PLUSIEURS PHRASES : il s'écrit en une phrase (§13.5 geste 1)")

    # C4 — le forfait (§13.5 geste 2, §13.1 règle 7). A-899 (18-11-2026, 12h36) : le forfait ne freine
    # JAMAIS. Un relevé périmé ou une remise à zéro passée ne refusent plus rien : estimer_le_forfait
    # rend une estimation marquée ESTIMÉ ; seul un relevé inutilisable (absent, illisible, daté dans le
    # futur, incohérent) est refusé, car il n'y a alors rien à partir de quoi estimer.
    plafond_pct = R["plafond_forfait_pct"]
    capture = heure(tete.get("forfait_capture", ""))
    pct = nombre(tete.get("forfait_pourcentage", ""))
    raz = heure(tete.get("forfait_remise_a_zero", ""))
    source_forfait = None
    if capture is None:
        refus.append("FORFAIT NON DATÉ : clé « forfait_capture » absente ou hors format AAAA-MM-JJ HH:MM — "
                     "aucun relevé à partir duquel estimer")
    elif capture > maintenant:
        refus.append(f"FORFAIT DATÉ DANS LE FUTUR : {tete['forfait_capture']}")
        capture = None
    if pct is None or not (0 <= pct <= 100):
        refus.append("FORFAIT : « forfait_pourcentage » absent ou hors de 0 à 100 %")
        pct = None
    if raz is None:
        refus.append("FORFAIT : clé « forfait_remise_a_zero » absente ou hors format AAAA-MM-JJ HH:MM")
    elif capture is not None and not (capture < raz <= capture + datetime.timedelta(days=R["remise_a_zero_max_j"])):
        refus.append(f"FORFAIT : la remise à zéro doit tomber après la capture et à moins de "
                     f"{R['remise_a_zero_max_j']:g} jours d'elle")
        raz = None
    if capture is not None and pct is not None and raz is not None:
        source_forfait, pct, raz, texte_forfait = estimer_le_forfait(
            capture, pct, raz, maintenant, R["remise_a_zero_max_j"] * 24, frais_h)
        calcul.append(f"CALCUL forfait {source_forfait} : {texte_forfait}")
        if source_forfait == "ESTIMÉ":
            signaux.append(f"FORFAIT ESTIMÉ (relevé du {tete['forfait_capture']} périmé ou remise à zéro passée) : "
                           "toutes les dates qui en dépendent sont ESTIMÉES ; un relevé réel les recale (A-899)")
        if pct > plafond_pct:
            signaux.append(f"FORFAIT {source_forfait} {pct:.1f} % au-delà du plafond de {plafond_pct:g} % : les "
                           "étapes du Chat sont datées après la remise à zéro — rien ne s'arrête (A-899)")
    else:
        pct = raz = None

    # C5 — les ressources (§13.2.0)
    recent(tete, "ressources_releve", "RELEVÉ DES RESSOURCES", maintenant, frais_h, refus)
    res = {}
    for c in R["ressources_exigees"]:
        v = tete.get(c, "")
        if not v:
            refus.append(f"RESSOURCE NON RELEVÉE : clé « {c} » absente (§13.2.0)")
        elif c != "github":
            res[c] = nombre(v)
            if res[c] is None or res[c] < 0:
                refus.append(f"RESSOURCE ILLISIBLE : « {c} » = « {v} » n'est pas un nombre positif fini")
                res[c] = None
    if res.get("processeurs") is not None and res["processeurs"] < 1:
        refus.append("RESSOURCE : « processeurs » inférieur à 1")
    if res.get("disque_libre_go") is not None and res["disque_libre_go"] < R["disque_min_go"]:
        refus.append(f"RESSOURCE : disque libre {res['disque_libre_go']:g} Go, moins de {R['disque_min_go']:g} Go "
                     "(seuil PROPOSÉ au §13.2.1, aux réglages)")
    plafond, en_cours = res.get("agents_plafond"), res.get("agents_en_cours")
    if plafond is not None and en_cours is not None and en_cours > plafond:
        refus.append(f"AGENTS : {en_cours:g} au travail pour un plafond de {plafond:g}")

    # C6 — le début du planning : l'heure du relevé des états et des restes des étapes.
    # Les fins ne partent PLUS de lui mais de MAINTENANT (bloc C10) : parties du début,
    # elles ne bougeaient pas quand le temps passait (Jean-Luc, 16-11-2026 09h05).
    debut = heure(tete.get("debut", ""))
    if debut is None:
        refus.append("DÉBUT ABSENT : clé « debut » (AAAA-MM-JJ HH:MM) : heure du relevé des états et des restes des étapes")
    elif (maintenant - debut).total_seconds() / 3600 > frais_h:
        refus.append(f"DÉBUT PÉRIMÉ : {tete['debut']}, plus de {frais_h:g} h avant maintenant — "
                     "les états et les restes des étapes, relevés à ce début, sont périmés ; les relever à nouveau")
        debut = None

    # C7 — ce qui limite le parallélisme
    if not tete.get("limites_parallelisme"):
        refus.append("LIMITES DU PARALLÉLISME ABSENTES : clé « limites_parallelisme »")

    # C7bis — limite de concurrence (décision du 16-11-2026 : le Chat lance rarement plus de
    # 3 agents à la fois) et liste des étapes permises avant la remise à zéro (A-834, décision
    # de Jean-Luc du 15-11-2026 à 21h11 : « tout est réduit sauf GitHub »). Données, jamais code.
    cap = nombre(tete.get("agents_simultanes_max", ""))
    if cap is None or cap < 1 or cap != int(cap):
        refus.append("LIMITE DE CONCURRENCE : clé « agents_simultanes_max » absente ou pas un entier ≥ 1")
        cap = None
    else:
        cap = int(cap)
    permis_avant = None
    if "avant_remise_seulement" in tete:
        permis_avant = [x.strip() for x in tete["avant_remise_seulement"].split(",") if x.strip()]
        if not permis_avant:
            refus.append("A-834 : clé « avant_remise_seulement » vide — lister les étapes permises ou retirer la clé")

    # C8 — chaque étape
    ids = [e["etape"] for e in etapes]
    if not etapes:
        refus.append("AUCUNE ÉTAPE dans etapes.csv")
    if len(ids) != len(set(ids)):
        refus.append("ÉTAPE EN DOUBLE dans etapes.csv")
    connues = set(ids)
    if permis_avant is not None:
        hors = [x for x in permis_avant if x not in connues]
        if hors:
            refus.append(f"A-834 : « avant_remise_seulement » cite des étapes inconnues : {', '.join(hors)}")
        permis_avant = set(permis_avant) & connues
    deps, dmin, dmax, val = {}, {}, {}, {}
    ok_calcul = bool(etapes) and len(ids) == len(set(ids))
    for e in etapes:
        i = e["etape"] or "?"
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", i):
            refus.append(f"ÉTAPE {i} : identifiant vide ou avec une espace ou un signe (il doit aussi être un jalon)")
        for c in ("livre", "ecart"):
            if not e[c]:
                refus.append(f"ÉTAPE {i} : « {c} » vide")
        v = {}
        for c in ("charge_h", "delai_h", "agents", "points"):
            a, b = nombre(e[c + "_min"]), nombre(e[c + "_max"])
            if a is None or b is None or a < 0 or b < a:
                refus.append(f"ÉTAPE {i} : « {c}_min/{c}_max » illisibles, non finis, négatifs ou min > max "
                             f"({e[c + '_min']} / {e[c + '_max']})")
                v[c] = None
                if c == "delai_h":
                    ok_calcul = False
            else:
                v[c] = (a, b)
        val[i] = v
        # sans agent (agents_max = 0), la charge est celle de Jean-Luc ou de GitHub : rien à diviser
        # (étape Q du tour 7 : questions à Jean-Luc, 0,5 h, 0 agent)
        if v["charge_h"] and v["delai_h"] and v["agents"] and v["agents"][1] >= 1:
            if v["charge_h"][0] / v["agents"][1] > v["delai_h"][1]:
                refus.append(f"ÉTAPE {i} : charge irréalisable — {v['charge_h'][0]:g} h de charge au moins, "
                             f"{v['agents'][1]:g} agent(s) au plus, {v['delai_h'][1]:g} h de délai au plus")
        j = mot_de_jugement(e["jugement_auteur"], R["jugements_permis"])
        if j is None:
            refus.append(f"ÉTAPE {i} : jugement de l'auteur « {e['jugement_auteur']} » — attendu l'un de "
                         f"{', '.join(R['jugements_permis'])} (§13.4 ③)")
        elif j in [x.upper() for x in R["jugements_refuses"]]:
            refus.append(f"ÉTAPE {i} : jugée « {j} » par l'auteur — la boucle du §13.4 n'est pas finie : proposer "
                         "une alternative sans baisse de qualité, réestimer, rejuger")
        elif j in [x.upper() for x in R["jugements_signales"]]:
            signaux.append(f"ÉTAPE {i} jugée « {j} » : à présenter à Jean-Luc avec sa raison (§13.4) — "
                           f"« {e['jugement_auteur']} »")
        if e["etat"] not in R["etats"]:
            refus.append(f"ÉTAPE {i} : état « {e['etat']} » — attendu l'un de {', '.join(R['etats'])}")
        d = [x.strip() for x in e["depend_de"].split(",") if x.strip()]
        inconnues = [x for x in d if x not in connues]
        if inconnues:
            refus.append(f"ÉTAPE {i} : dépend d'étapes inconnues {', '.join(inconnues)}")
            ok_calcul = False
        deps[i] = [x for x in d if x in connues]
        fini = e["etat"] == "tenu"
        dmin[i] = 0.0 if fini or v["delai_h"] is None else v["delai_h"][0]
        dmax[i] = 0.0 if fini or v["delai_h"] is None else v["delai_h"][1]
    # C8bis — les délais tiennent dans le calendrier. Toute fin calculée plus bas (chemin critique, ou calendrier
    # repoussé après LA remise à zéro du forfait — une seule fenêtre est calculée) vaut au plus « maintenant + attente
    # de la remise + somme des délais max ». Comparé en NOMBRE d'heures, sans fabriquer de durée : sinon un délai
    # de 1e12 h levait OverflowError, et une donnée mal tapée sortait en « erreur imprévue du programme »
    # (superviseurs R-759 du 25-11-2026, 14h16 et 14h19). Aucune borne « plausible » ici : ce nombre revient à Jean-Luc.
    if ok_calcul:
        attente_h = max(0.0, (raz.astimezone(datetime.timezone.utc) - maintenant.astimezone(datetime.timezone.utc)
                              ).total_seconds() / 3600) if raz is not None else 0.0
        somme_h = sum(dmax.values())
        if somme_h + attente_h > heures_jusqu_a_la_fin_du_calendrier(maintenant):
            refus.append(f"DÉLAIS HORS DU CALENDRIER : {somme_h:g} h de délais max (somme des étapes non tenues), "
                         f"plus {attente_h:g} h jusqu'à la remise à zéro, dépassent la dernière date calculable "
                         f"({FIN_DU_CALENDRIER:%Y-%m-%d}) — un délai mal tapé ? Dates non calculées")
            ok_calcul = False

    # C9 — jugement de l'auteur DATÉ, puis estimation de l'expert neuf, fichier séparé daté APRÈS
    f_aut, f_exp = chemin_de(tete, dossier, "jugement_auteur"), chemin_de(tete, dossier, "estimation_expert")
    textes = {}
    for cle, f in (("jugement_auteur", f_aut), ("estimation_expert", f_exp)):
        if not f or not os.path.isfile(f) or os.path.getsize(f) == 0:
            refus.append(f"FICHIER « {cle} » ABSENT OU VIDE : {f or '(clé manquante)'} (§13.4 ③ ④)")
            continue
        try:
            textes[cle] = open(f, encoding="utf-8").read()
        except (OSError, UnicodeDecodeError) as x:
            refus.append(f"FICHIER « {cle} » ILLISIBLE : {x}")
    if len(textes) == 2:
        if os.path.realpath(f_aut) == os.path.realpath(f_exp) or textes["jugement_auteur"] == textes["estimation_expert"]:
            refus.append("EXPERT NON SÉPARÉ : l'estimation de l'expert doit être un fichier distinct du jugement de l'auteur")
        t_a, t_e = date_du_fichier(f_aut), date_du_fichier(f_exp)
        if t_a is None:
            refus.append("JUGEMENT DE L'AUTEUR NON DATÉ : aucune heure lisible dans ses cinq premières lignes")
        if t_e is None:
            refus.append("ESTIMATION DE L'EXPERT NON DATÉE : aucune heure lisible dans ses cinq premières lignes")
        if t_a and t_e and not t_e > t_a:
            refus.append(f"EXPERT DATÉ AVANT L'AUTEUR : expert {t_e:%Y-%m-%d %H:%M}, auteur {t_a:%Y-%m-%d %H:%M} "
                         "— l'auteur juge d'abord (§13.4 ③)")
        for t, nom in ((t_a, "JUGEMENT DE L'AUTEUR"), (t_e, "ESTIMATION DE L'EXPERT")):
            if t and t > maintenant:
                refus.append(f"{nom} DATÉ DANS LE FUTUR : {t:%Y-%m-%d %H:%M}")
    for e in etapes:
        if e["etat"] == "tenu":
            continue
        for cle, nom in (("jugement_auteur", "JUGEMENT DATÉ DE L'AUTEUR"), ("estimation_expert", "ESTIMATION DE L'EXPERT NEUF")):
            if cle in textes and not re.search(rf"(?<![\w-]){re.escape(e['etape'])}(?![\w-])", textes[cle]):
                refus.append(f"ÉTAPE {e['etape']} SANS {nom} : absente de {os.path.basename(chemin_de(tete, dossier, cle))}")

    # C9bis — l'état tel que l'ordonnanceur le voit : SA lecture (sans réseau) et SA règle d'état (situation),
    # jamais une copie (R-708 ; superviseur R-759 du 18-11-2026, 16h17), avec ou sans branche d'état (sans elle,
    # situation fait ce que fait le premier passage de l'ordonnanceur). Ne pas pouvoir la calculer est un REFUS,
    # jamais un signal (R-734 ; M5 de la relecture 8887e31e : l'ancien rabat en signal laissait le contrôle
    # conclure sur les états déclarés)
    # Seule une ENTRÉE illisible devient ce refus : les échecs de lecture déclarés (Impossible, des deux exemplaires
    # du module — le contrôle lancé en ligne de commande s'appelle __main__, l'ordonnanceur importe le sien) et les
    # erreurs de lecture de fichier. Un programme faux (SyntaxError à l'import, NameError, KeyError…) remonte et la
    # ligne de commande rend 2 : un bogue n'est jamais un refus (m12 de la relecture f2ce23138 — sous Python 3.11, la
    # SyntaxError de l'ordonnanceur passait pour un « état illisible » et l'épreuve k15 restait verte)
    import ORDONNER_UN_PLANNING as O
    try:
        Lo = O.lire_tout(dossier, maintenant, reseau=False)
        vue, ligne_sv = O.situation(Lo, maintenant), Lo["vie"].get("chat")
    except (Impossible, O.C.Impossible, OSError, UnicodeError, csv.Error) as e:
        vue, ligne_sv, illisible = None, None, f" — état illisible : {type(e).__name__} {e}"
        refus.append(f"ERREUR ÉTAT ILLISIBLE : la situation de l'ordonnanceur ne se calcule pas ({type(e).__name__} "
                     f"{e}) — ni étapes prêtes, ni signe de vie jugés (R-734)")
    else:
        illisible = ""

    # C10 — le calcul : chemin critique, marges, fins, forfait suffisant, états, sous-emploi
    critiques, tot_min = set(), None
    etat = {e["etape"]: e["etat"] for e in etapes}
    if ok_calcul:
        cycle = a_un_cycle(deps)
        if cycle:
            refus.append(f"DÉPENDANCES EN CYCLE : {', '.join(cycle)}")
            ok_calcul = False
    if ok_calcul:
        # les fins partent de MAINTENANT : le temps écoulé depuis le début ne se compte plus
        fins = {}
        for nom, dur in (("au mieux (délais min)", dmin), ("réaliste (délais max)", dmax)):
            fin, r, crit = calculer_chemin(dur, deps)
            fins[nom] = (fin, r)
            critiques |= set(crit)
            calcul.append(f"CALCUL fin {nom}, sans forfait, depuis maintenant : {montrer(maintenant, fin)} "
                          f"({fin:g} h) — chemin critique {' → '.join(crit)}")
            calcul.append("CALCUL marges " + nom + " : " + " · ".join(f"{k} {x[2]:g} h" for k, x in r.items()))
        fin_min, tot_min = fins["au mieux (délais min)"]
        _, res_max = fins["réaliste (délais max)"]
        plus_tot = {i: tot_min[i][1] for i in ids}   # fin au plus tôt de chaque étape, en heures depuis maintenant
        # le reste d'une étape en cours n'est déclaré qu'au relevé du début : il est compté en entier
        en_cours_l = [i for i in ids if etat[i] in R["etats_actifs"]]
        calcul.append("CALCUL reste des étapes en cours (" + (", ".join(en_cours_l) or "aucune") + ") : leur délai "
                      f"déclaré au relevé du {tete.get('debut', '?')}, compté EN ENTIER depuis maintenant — "
                      "aucun reste plus récent n'est déclaré (limite)")
        # forfait suffisant (§13.1 règle 7) : sinon les dates reculent après la remise à zéro
        restantes = [i for i in ids if etat[i] != "tenu"]
        if pct is not None and all(val[i]["points"] for i in restantes):
            reste = max(0.0, plafond_pct - pct) * R["points_par_pourcent"]   # au-delà du plafond : 0, jamais négatif
            plein = plafond_pct * R["points_par_pourcent"]
            p_min = sum(val[i]["points"][0] for i in restantes)
            p_max = sum(val[i]["points"][1] for i in restantes)
            quand_raz = montrer(raz, 0) if raz else "?"
            calcul.append(f"CALCUL forfait : {p_min:g} à {p_max:g} points prévus ; {reste:g} points disponibles avant "
                          f"la remise à zéro du {quand_raz} ({plafond_pct:g} % − {pct:g} % × "
                          f"{R['points_par_pourcent']:g} point par %, réglage points_par_pourcent) ; {plein:g} points "
                          "dans la fenêtre suivante · les points sont déclarés par étape (points_min/points_max), "
                          f"aucune conversion heures → points n'existe · forfait {source_forfait}")
            # le calendrier réel : ce qui ne tient pas dans le reste attend la remise à zéro
            raz_h = (raz.astimezone(datetime.timezone.utc) - maintenant.astimezone(datetime.timezone.utc)
                     ).total_seconds() / 3600 if raz is not None else None
            if raz_h is not None and raz_h > 0:
                marge_crit = {i: res_max[i][2] for i in ids}
                occupe = {i for i in ids if etat[i] != "tenu" and (val[i]["agents"] is None or val[i]["agents"][1] >= 1)}
                places = {}
                for nom, dur, k in (("au mieux", dmin, 0), ("réaliste", dmax, 1)):
                    pts = {i: 0.0 if etat[i] == "tenu" else val[i]["points"][k] for i in ids}
                    fin_r, place, av, ap, depense = planifier_sous_forfait(dur, deps, pts, marge_crit, reste, raz_h,
                                                                           occupe, cap, permis_avant)
                    places[nom] = place
                    if k == 0:
                        plus_tot = {i: place[i][1] for i in ids}
                    # contrôles du calendrier rendu, indépendants de la façon dont il a été fait
                    if permis_avant is not None:
                        hors = [i for i in av if i not in permis_avant and dur[i] > 0]
                        if hors:
                            refus.append(f"A-834 ({nom}) : étape(s) {', '.join(hors)} placée(s) avant la remise à "
                                         "zéro sans figurer dans « avant_remise_seulement »")
                    if cap is not None:
                        iv = [place[i][:2] for i in occupe if dur[i] > 0]
                        pic = max((sum(1 for a, b in iv if a <= x < b) for x, _ in iv), default=0)
                        if pic > cap:
                            refus.append(f"CONCURRENCE ({nom}) : {pic} étapes en même temps pour "
                                         f"agents_simultanes_max = {cap}")
                    av = [i for i in av if etat[i] != "tenu"]
                    p_apres = sum(pts[i] for i in ap)
                    calcul.append(f"CALCUL fin réelle (forfait compris) {nom} : {montrer(maintenant, fin_r)} "
                                  f"({fin_r:g} h depuis maintenant) — forfait {source_forfait}")
                    calcul.append(f"CALCUL {nom} — avant la remise à zéro ({depense:g} points sur {reste:g}) : "
                                  f"{', '.join(av) or 'aucune'} / après ({p_apres:g} points) : {', '.join(ap) or 'aucune'}")
                    if p_apres > plein:
                        signaux.append(f"FORFAIT ({nom}) : {p_apres:g} points après la remise à zéro pour {plein:g} "
                                       "dans la fenêtre — la fenêtre suivante n'est pas calculée, la fin réelle est trop tôt")
                calcul.append(f"CALCUL limite de concurrence : {cap if cap is not None else 'aucune'} étape(s) "
                              "occupant un agent à la fois (agents_simultanes_max) · permises avant la remise à "
                              "zéro (avant_remise_seulement, A-834) : "
                              + (", ".join(sorted(permis_avant)) if permis_avant is not None else "toutes"))
                m_, r_ = places["au mieux"], places["réaliste"]
                for i in sorted((i for i in ids if etat[i] != "tenu"), key=lambda i: (m_[i][0], r_[i][0], i)):
                    calcul.append(f"CALCUL étape {i} : fenêtre au mieux {m_[i][2]} · réaliste {r_[i][2]} · "
                                  f"au mieux {montrer(maintenant, m_[i][0])} → {montrer(maintenant, m_[i][1])} · "
                                  f"réaliste {montrer(maintenant, r_[i][0])} → {montrer(maintenant, r_[i][1])}")
            else:
                calcul.append("CALCUL fin réelle (forfait compris) : non calculée — aucun relevé du forfait utilisable")
            fin_avant_raz = raz is not None and maintenant + datetime.timedelta(hours=fin_min) < raz
            if p_min > reste and fin_avant_raz:
                (signaux if source_forfait == "ESTIMÉ" else refus).append(f"FORFAIT INSUFFISANT : {p_min:g} points au moins pour {reste:g} restants avant "
                             f"{plafond_pct:g} %, et la fin au mieux tombe avant la remise à zéro — les dates "
                             "reculent, rien n'est réduit (§13.1 règle 7)")
            elif p_max > reste:
                signaux.append(f"FORFAIT : jusqu'à {p_max:g} points prévus pour {reste:g} restants avant {plafond_pct:g} %")
        # une étape lancée avant ses dépendances
        for i in ids:
            if etat[i] in R["etats_actifs"] + ["tenu"]:
                avant = [d for d in deps[i] if etat[d] not in R["etats_qui_liberent"]]
                if avant:
                    refus.append(f"ÉTAPE {i} « {etat[i]} » alors que ses dépendances {', '.join(avant)} "
                                 "ne sont ni écrites ni tenues")
        # agents déclarés sans étape active pour les occuper
        actifs = [i for i in ids if etat[i] in R["etats_actifs"]]
        if en_cours is not None and all(val[i]["agents"] for i in actifs):
            cap = sum(val[i]["agents"][1] for i in actifs)
            if en_cours > cap:
                refus.append(f"AGENTS DÉCLARÉS SANS ÉTAPE : {en_cours:g} au travail, mais les étapes actives "
                             f"({', '.join(actifs) or 'aucune'}) en occupent {cap:g} au plus")
        # ressources sous-employées : prêtes et occupées lues dans la situation de l'ordonnanceur, la seule
        # « prête » (M3 de la relecture bcf7756c, M5 de la relecture 8887e31e) ; situation illisible → refus
        # C9bis déjà écrit, rien n'est conclu ici
        if vue:
            pretes, en_cours = [i for i in ids if vue["etat"].get(i) == "prete"], vue["occupe"]
        else:
            pretes = []
        pretes.sort(key=lambda i: (res_max[i][2], i))
        calcul.append("CALCUL étapes prêtes non lancées, la moins de marge d'abord ("
                      + ("situation de l'ordonnanceur) : " + (", ".join(pretes) or "aucune") if vue
                         else "état illisible) : non calculées"))
        if pretes and plafond is not None and en_cours is not None and en_cours < plafond:
            refus.append(f"RESSOURCES SOUS-EMPLOYÉES : {', '.join(pretes)} prête(s) et non lancée(s), "
                         f"{en_cours:g} agent(s) sur {plafond:g} — lancer d'abord {pretes[0]} (§13.1 règle 4)")

    # C11 — les six leviers sur CHAQUE étape du chemin critique (§13.0quater)
    vus = {}
    for l in leviers:
        cle = (l["etape"], l["levier"])
        if cle in vus:
            refus.append(f"LEVIER EN DOUBLE : étape {l['etape']}, levier {l['levier']}")
        vus[cle] = l
        if l["etape"] not in connues:
            refus.append(f"LEVIER SUR UNE ÉTAPE INCONNUE : {l['etape']}")
        if l["levier"] not in R["leviers"]:
            refus.append(f"LEVIER INCONNU : « {l['levier']} » sur {l['etape']}")
    for i in sorted(critiques):
        manquants, mal = [], []
        for n in R["leviers"]:
            l = vus.get((i, n))
            if l is None:
                manquants.append(n)
            elif l["verdict"].upper() not in R["verdicts_levier"] or not l["gain_ou_raison"]:
                mal.append(n)
        if manquants:
            refus.append(f"LEVIERS NON PASSÉS sur l'étape critique {i} : levier(s) {', '.join(manquants)} (§13.0quater)")
        if mal:
            refus.append(f"LEVIERS SANS VERDICT OU SANS GAIN/RAISON sur {i} : levier(s) {', '.join(mal)} — "
                         f"« {' » ou « '.join(R['verdicts_levier'])} » suivi du gain ou de la raison (§13.0quater)")

    # C13 — la carte des pannes DU PROJET (A-897, A-898) : une carte, partagée par les plannings du projet
    carte = chemin_de(tete, dossier, "carte_des_pannes")
    controler_la_carte(carte, racine_du_depot(os.path.dirname(carte)) if carte else None, R, refus, signaux)

    # C14 — le signe de vie de la conversation (A-904, A-905) : plus vieux que signe_de_vie_max_min, ou daté dans
    # le futur, alors qu'une étape n'est pas TENUE selon situation = ERREUR (refus). « Non tenue » est lu dans
    # situation, comme le chien de garde, jamais dans les états déclarés (M5 de la relecture 8887e31e)
    age = age_du_signe(ligne_sv, maintenant)
    reste = [i for i in vue["etat"] if vue["etat"][i] != "tenue"] if vue else []
    if age is None:
        signaux.append(f"SIGNE DE VIE DE LA CONVERSATION ABSENT (vie/chat.txt de « {tete.get('branche_d_etat', '?')} », "
                       f"références locales) : le tunnel n'a jamais tourné ici, ou le clone n'a pas relu la branche{illisible}")
    elif reste and (age < 0 or age > R["signe_de_vie_max_min"]):
        refus.append(f"ERREUR SIGNE DE VIE {'DATÉ DANS LE FUTUR' if age < 0 else 'PÉRIMÉ'} : « {ligne_sv} », "
                     f"{age:.0f} min (plus de {R['signe_de_vie_max_min']:g} min) — le tunnel ne tourne plus")

    # C12 — le fichier de jalons, lu par le veilleur lui-même, confronté au calcul
    f_j = chemin_de(tete, dossier, "jalons")
    if not f_j or not os.path.isfile(f_j):
        refus.append(f"JALONS ABSENTS : {f_j or '(clé « jalons » manquante)'} (§13.5 geste 4)")
        return calcul, signaux, refus
    lignes, _, _ = TENIR_UN_PLANNING.passage_unique(f_j, maintenant)
    arrets = [x for x in lignes if x.startswith("ARRET")]
    if arrets:
        refus.append("JALONS INVALIDES POUR LE VEILLEUR : " + " | ".join(arrets))
        return calcul, signaux, refus
    ech = {j["jalon"].strip(): heure(j["echeance"]) for j in TENIR_UN_PLANNING.lire(f_j)}
    sans = [i for i in ids if i not in ech]
    # une étape DÉCLARÉE tenue sans preuve : refusée ici (l'ordonnanceur la dit BLOQUÉE à chaque passage)
    for j in TENIR_UN_PLANNING.lire(f_j):
        if (TENIR_UN_PLANNING.preparer(j) is None and etat.get(j["jalon"]) == "tenu"
                and TENIR_UN_PLANNING.etat_de_la_preuve(j, maintenant) != "tenu"):
            refus.append(f"ÉTAPE {j['jalon']} DÉCLARÉE TENUE, PREUVE ABSENTE OU MAL DATÉE : {j['_chemin']}")
    if sans:
        refus.append(f"ÉTAPE(S) SANS JALON : {', '.join(sans)} — chaque étape a un jalon de même identifiant")
    if tot_min is not None:
        for i in ids:
            if etat[i] == "tenu" or i not in ech:
                continue
            tot = (maintenant.astimezone(datetime.timezone.utc) + datetime.timedelta(hours=plus_tot[i])).astimezone(P)
            if ech[i] < tot:
                refus.append(f"JALON {i} AVANT LA FIN AU PLUS TÔT CALCULÉE (depuis maintenant, forfait compris) : "
                             f"échéance {ech[i]:%Y-%m-%d %H:%M}, fin au plus tôt {tot:%Y-%m-%d %H:%M}")
            for d in deps[i]:
                if d in ech and ech[i] < ech[d]:
                    refus.append(f"JALON {i} AVANT CELUI DE SA DÉPENDANCE {d} : {ech[i]:%Y-%m-%d %H:%M} < "
                                 f"{ech[d]:%Y-%m-%d %H:%M}")
    return calcul, signaux, refus


def main(argv):
    """Lance le contrôle depuis la ligne de commande et rend le code de sortie.

    ① RÔLE — Lire les arguments, appeler controler, afficher, rendre le code.
    ② CONTEXTE D APPEL — `python3 programmes/CONTROLER_UN_PLANNING.py <dossier>
      [--maintenant=AAAA-MM-JJ HH:MM]` ; les épreuves l'appellent directement.
    ③ ENTRÉE — `argv` : les arguments, sans le nom du programme.
    ④ CONDITIONS D ENTRÉE — Un dossier donné.
    ⑤ SORTIE — UNE valeur : le code, 0 accepté · 1 refusé · 2 contrôle
      impossible (fichier, argument, ou toute erreur imprévue).
      [rend: 1]
    ⑥ TRAITEMENT — arguments (dans --maintenant, un « T » vaut une espace) ;
      controler, dont toute exception rend 2 avec son nom ; lignes CALCUL, puis
      SIGNAL, puis REFUS, puis le verdict.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un contrôle qui n'a pas pu tourner ne rend jamais 0, et ne se
      confond pas avec un refus (R-734) : un plantage rendait 1 (relecteur neuf
      du 11-11-2026, D1).
    ⑨ CE QUI CLOCHE — « --maintenant » n'est pas réservé aux épreuves.
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Revient toujours : toute exception de controler est
      rattrapée.
      [sort: non]
    """
    pos = [a for a in argv if not a.startswith("--")]
    opt = [a for a in argv if a.startswith("--")]
    maintenant = datetime.datetime.now(P)
    for o in opt:
        if o.startswith("--maintenant="):
            maintenant = heure(o.split("=", 1)[1].replace("T", " "))   # « AAAA-MM-JJTHH:MM » s'écrit sans guillemets
            if maintenant is None:
                print("ARRET --maintenant hors format AAAA-MM-JJ HH:MM")
                return 2
        else:
            print(f"ARRET option inconnue : {o}")
            return 2
    if len(pos) != 1:
        print("ARRET usage : CONTROLER_UN_PLANNING.py <dossier du planning> [--maintenant=AAAA-MM-JJ HH:MM]")
        return 2
    try:
        calcul, signaux, refus = controler(pos[0], maintenant)
    except Impossible as e:
        print(f"ARRET contrôle impossible : {e}")
        return 2
    except Exception as e:   # R-734 : un plantage n'est jamais un refus
        print(f"ARRET contrôle impossible, erreur imprévue du programme : {type(e).__name__} {e}")
        return 2
    print(f"CONTRÔLE DU PLANNING {os.path.abspath(pos[0])} — {maintenant:%Y-%m-%d %H:%M} (Paris)")
    for l in calcul:
        print(l)
    for s in signaux:
        print("SIGNAL " + s)
    for r in refus:
        print("REFUS " + r)
    if refus:
        print(f"PLANNING REFUSÉ : {len(refus)} motif(s)")
        return 1
    print("PLANNING ACCEPTÉ")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
