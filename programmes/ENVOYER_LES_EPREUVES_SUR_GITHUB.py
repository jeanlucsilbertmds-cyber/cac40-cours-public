#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ENVOYER_LES_EPREUVES_SUR_GITHUB.py — Jeu 26-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Ce programme publie une branche travail-* du dépôt privé au dépôt PUBLIC (où GitHub joue les
épreuves longues gratuitement) puis y dépose une demande d'épreuves. Il REMPLACE le script bash du même nom
(25-11-2026, réparé le 26-11-2026 au matin) : la relecture de Cowork du 26-11-2026 à 12h04 l'a jugé « déployable
après corrections » (D-1 important : deux envois de la même branche dans la même minute, la seconde demande
MODIFIAIT la première, le relais l'aurait refusée, et le script écrivait « ENVOYÉ » ; D-2 : les codes d'épreuves
n'étaient pas vérifiés), et le superviseur R-759 neuf a jugé « ARRÊTER ET SIMPLIFIER » : le bash refaisait
programmes/LIVRER.py presque pas à pas, alors que deux implémentations d'une même chose divergent toujours (R-708).
Ce programme n'écrit donc AUCUN geste lui-même : il IMPORTE LIVRER et enchaîne ses fonctions.

① RÔLE — Pour chaque entrée « branche|Code1,Code2 » : vérifier la branche et ses codes, publier son code sur la
  branche publique du même nom, déposer la demande d'épreuves longues, et dire en une ligne ENVOYÉ ou REFUSÉ.
② CONTEXTE D'APPEL — À la main, par le pilote V8 ou le Chat, depuis la racine d'un clone COMPLET du dépôt privé
  (ou avec PRIVE=<ce clone>) :
  python3 -B programmes/ENVOYER_LES_EPREUVES_SUR_GITHUB.py travail-x|CircuitPublic,GardeFou [travail-y|Carte …]
  programmes/ENVOYER_LES_EPREUVES_SUR_GITHUB.sh relaie vers ce programme (même ligne de commande).
  Jamais par un circuit.
③ ENTRÉE — Une ou plusieurs chaînes « branche|Code1,Code2 ». Variables d'environnement : PRIVE (le clone privé ;
  par défaut le dossier courant) ; celles de LIVRER, pour les épreuves seulement : LIVRER_DEPOT_PUBLIC (adresse de
  clonage du public), LIVRER_FABRICANT (le fabricant lancé), LIVRER_SANS_ATTENTE_DE_MINUTE.
④ CONDITIONS D'ENTRÉE — PRIVE est un clone git du dépôt privé dont « origin » est le privé ; la branche est DÉJÀ
  POUSSÉE au privé (le programme part de origin/<branche>) ; le clone est COMPLET (un clone superficiel est refusé
  par le fabricant, avec le remède « git fetch --unshallow ») ; les identifiants git de la machine permettent de
  pousser au public.
⑤ SORTIE — Une ligne par branche : « HHhMM ENVOYÉ <branche> <pointe, 9 caractères> : <codes> », « HHhMM REFUSÉ
  <branche> : <raison> » ou « HHhMM PLANTAGE <branche> : <exception> ». UNE valeur : le code de sortie — 0 tout est
  envoyé · 1 au moins une branche refusée (les autres sont quand même traitées) · 5 au moins un plantage (une
  exception imprévue : ni un envoi, ni un refus ; l'état est à relire).
⑥ TRAITEMENT — Voir `main` et `envoyer_une_branche`.
⑦ UNITÉ — Heures de Paris (les lignes).
⑧ POURQUOI — Voir le sens en tête. Chaque geste vient de LIVRER : `constantes_du_fabricant` (motif de version, nom
  de demande), `worktree_nomme` (refus d'une branche locale en avance, jamais de tête détachée),
  `publier_au_public` (essai à blanc, publication, preuve par un second clone neuf), `deposer_la_demande`
  (« pull --ff-only », nom à la minute avec attente de la minute suivante si le nom est pris, fichier AJOUTÉ seul
  dans son commit, pointe publique relue — c'est la correction de D-1). Le refus d'un clone superficiel est déjà
  écrit dans le fabricant (`refus_selon_l_historique`, avec le remède) : il n'est pas recopié ici. Ce qui est
  LAISSÉ de LIVRER (D-9 du RELU de Cowork du 26-11-2026, 12h45) : verifier_la_note de LIVRER n'est pas appelée :
  choix hérité du script bash ; les épreuves longues servent AVANT la livraison ; choix qui revient à Jean-Luc,
  NON TRANCHÉ (A-1053 ; D-13). Le suivi du relais (attendre_la_file) est laissé aussi (voir ⑨).
⑨ CE QUI CLOCHE — Le programme NE SUIT PAS le relais (LIVRER.attendre_la_file et le suivi du passage demandent gh,
  absent des sessions) : « ENVOYÉ » dit que la demande est AJOUTÉE au public sous un nom neuf et que ses codes
  existent dans la table, pas que le relais l'a acceptée (un passage déjà en cours la fait refuser par le relais,
  « redéposer »). Le clone superficiel n'est refusé qu'à l'essai à blanc du fabricant, après la pose du dossier de
  travail et le clone public, mais avant toute poussée. Les messages de refus de LIVRER reprennent jusqu'à 300
  caractères des sorties de git et du fabricant : ils passent par `masquer` avant d'être affichés (motif de jeton
  du dépôt, puis ligne entière remplacée si la forme ne se voit qu'au décodage, D-10). · D-9 : verifier_la_note de
  LIVRER n'est pas appelée : choix hérité du script bash ; les épreuves longues servent AVANT la livraison ; choix
  qui revient à Jean-Luc, NON TRANCHÉ (A-1053 ; D-13). Conséquence mesurée par Cowork : l'outil
  publie au dépôt public une branche que le garde-fou refuse. · L'outil refuse « toutes » (absent de la clé
  epreuves_longues, donc « code absent ») alors que le relais l'accepte (programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py:1846
  et 2617) : capacité perdue par rapport au relais, non corrigée. · Défaut de LIVRER.deposer_la_demande, consigné,
  pas corrigé (LIVRER.py n'est pas touché ici) : après la 3e attente d'une minute, le nom n'est pas recalculé ; il
  refuse « nom de demande impossible » alors qu'une minute neuve est peut-être libre.
⑩ EFFET — Pousse au public (branche du même nom : code publié par le fabricant, puis un commit de demande) ; crée
  puis retire sous /tmp un dossier de travail du clone privé (« livrer_wt_* ») et des clones publics
  (« livrer_pub_* ») ; lance « git fetch origin » dans le clone privé. N'écrit jamais au dépôt privé.
⑪ TERMINAISON — Sort du programme par sys.exit. Chaque commande lancée par LIVRER est bornée ; deposer_la_demande
  fait, par branche, jusqu'à trois attentes d'une minute libre (≈ 183 s), puis refus (D-8 du RELU de Cowork du
  26-11-2026, 12h45 : la fiche disait « 61 s »).
"""
import json
import os
import re
import shutil
import sys
import traceback
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import LIVRER  # noqa: E402 — le chemin de programmes/ est posé juste au-dessus

ENVOYE, REFUSE, PLANTAGE = 0, 1, 5
FORME = LIVRER.charger(os.path.join(os.path.dirname(os.path.abspath(__file__)), "FORME_D_UN_JETON.py"),
                       "JETON_POUR_ENVOYER")
JETON = FORME.MOTIF_DE_JETON
# Ce qui remplace une ligne ENTIÈRE dont la forme de jeton ne se voit qu'au décodage (D-10, RELU de Cowork du
# 26-11-2026 à 12h45) : la ligne est retirée en bloc, jamais seulement la sous-chaîne (superviseur R-759, 13h12).
LIGNE_MASQUEE = "*** ligne masquée : forme de jeton ***"


def masquer(texte):
    """Rend le texte où chaque forme de jeton en clair devient « *** » et où chaque ligne qui en porte encore une est remplacée en entier.

    ① RÔLE — Ne jamais afficher un secret de connexion repris d'une sortie de git, du fabricant ou d'une trace.
    ② CONTEXTE D'APPEL — `ligne`, pour chaque ligne affichée ; `main`, pour la trace d'un plantage.
    ③ ENTRÉE — `texte` : une ligne ou plusieurs (une trace, un message de LIVRER qui reprend une sortie de git).
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte masqué, autant de lignes que l'entrée.
      [rend: 1]
    ⑥ TRAITEMENT — Le texte encodé en UTF-8 est coupé aux sauts de ligne ; pour CHAQUE ligne : ① le motif
      MOTIF_DE_JETON de programmes/FORME_D_UN_JETON.py remplace chaque forme en clair par « *** » (le reste de la
      ligne reste lisible) ; ② si `porte_une_forme_de_jeton` du même module dit encore vrai (une forme qui ne se voit
      qu'au décodage, comme le base64 nu de « x-access-token:<jeton> »), la ligne entière devient LIGNE_MASQUEE.
      Les lignes sont recollées, puis décodées.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le script bash masquait deux formes à la main ; le dépôt a UN motif de jeton, dans
      FORME_D_UN_JETON.py : on le lit, on ne le recopie pas (R-708). D-10 du RELU de Cowork (26-11-2026, 12h45) :
      le motif seul laissait passer le base64 nu, que seule la FONCTION voit ; le décodage n'est pas réécrit ici
      (R-708 : deux implémentations d'une même chose divergent toujours). Ligne entière, pas sous-chaîne : la
      fonction dit SI une forme est là, pas OÙ (sa fiche), et le superviseur R-759 neuf (26-11-2026, 13h12) a jugé
      « DE FOND, à une condition : écarter le masquage de sous-chaîne ».
    ⑨ CE QUI CLOCHE — Une forme que ni le motif ni la fonction ne connaissent passe (la classe hors périmètre de
      FORME_D_UN_JETON.py). Le test est fait LIGNE PAR LIGNE : un base64 coupé sur deux lignes (sortie de
      « base64 » sans « -w0 ») est vu sur la ligne qui porte encore la forme, mais les AUTRES lignes du bloc restent
      affichées : mesuré par Cowork le 26-11-2026 à 13h37, 52 octets sur 94 d'un jeton fictif lisibles en décodant la
      2e ligne (D-11, non corrigé : outil provisoire, fuite rare ; remède au BACKLOG). Une ligne masquée perd
      tout ce qu'elle disait (y compris « REFUSÉ » et la raison) ; le code de sortie, lui, reste juste. Faux rouge
      possible : une ligne innocente dont un morceau base64 se décoderait par hasard en une forme (mesuré à 0 par
      FORME_D_UN_JETON.py sur le dépôt).
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main ; un décodage par suite base64 de chaque ligne, borné par sa taille.
      [sort: non]
    """
    lignes = []
    for brute in texte.encode("utf-8", "surrogateescape").split(b"\n"):
        claire = JETON.sub(b"***", brute)
        lignes.append(LIGNE_MASQUEE.encode("utf-8") if FORME.porte_une_forme_de_jeton(claire) else claire)
    return b"\n".join(lignes).decode("utf-8", "replace")


def ligne(etat, branche, reste):
    """Affiche « HHhMM <ETAT> <branche> <reste> », masquée.

    ① RÔLE — La seule forme d'une ligne de compte rendu.
    ② CONTEXTE D'APPEL — `main`, une fois par branche (plus la trace d'un plantage).
    ③ ENTRÉE — `etat` : ENVOYÉ, REFUSÉ ou PLANTAGE · `branche` · `reste` : la suite de la ligne.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — L'heure de Paris (LIVRER.PARIS), `masquer`, LIVRER.dire.
    ⑦ UNITÉ — Heure de Paris, à la minute.
    ⑧ POURQUOI — Forme reprise du script bash, que le pilote V8 lit déjà.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit sur la sortie.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    heure = datetime.now(LIVRER.PARIS).strftime("%Hh%M")
    LIVRER.dire(masquer(f"{heure} {etat} {branche} {reste}"))


def lire_l_entree(item):
    """Découpe « branche|Code1,Code2 » ; rend (branche, codes) ; lève LIVRER.Arret si l'entrée est mal formée ou si un code y est deux fois.

    ① RÔLE — Refuser une entrée sans branche, sans code ou avec un code en double AVANT tout geste.
    ② CONTEXTE D'APPEL — `envoyer_une_branche`, en premier.
    ③ ENTRÉE — `item` : la chaîne de la ligne de commande.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : la branche (texte), les codes (liste de textes, au moins un, chacun une seule fois).
      [rend: 2]
    ⑥ TRAITEMENT — Coupe au premier « | » ; codes séparés par « , », blancs retirés, vides écartés ; puis les codes
      présents plus d'une fois (comparés tels quels, majuscules comprises, comme le relais) : s'il y en a, refus
      « code demandé deux fois : X — rien n'est publié ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — D-3 du RELU de Cowork (26-11-2026, 12h04) : « branche| » n'était pas éprouvé ; une demande sans
      code serait refusée par le relais. D-6 du RELU de Cowork (26-11-2026, 12h45) : « CircuitPublic,CircuitPublic »
      partait avec « ENVOYÉ », code 0, alors que le relais refuse (« epreuve demandee deux fois »,
      programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py:2622) ; refus plutôt que dédoublonnage silencieux : le pilote
      apprend que sa ligne était fausse, et le plus tôt possible, avant toute publication.
    ⑨ CE QUI CLOCHE — Un nom de branche qui contient « | » est coupé (les branches travail-* n'en portent pas ; le
      motif de version du fabricant le refuserait ensuite). Le relais accepte « toutes » (FABRIQUER_LE_CIRCUIT_PUBLIC.py:1846
      et 2617) ; ici, « toutes » n'est pas une clé de la table et `codes_inconnus` le refuse : capacité perdue, voir
      la fiche du programme. L'ordre « doublons refusés avant la pose du dossier de travail » n'est gardé par aucune
      épreuve (D-12, non corrigé) ; seul « rien n'est publié » l'est.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main, ou lève Arret.
      [sort: non]
    """
    branche, barre, reste = item.partition("|")
    codes = [c.strip() for c in reste.split(",") if c.strip()]
    if not barre or not branche or not codes:
        raise LIVRER.Arret(REFUSE, f"entrée mal formée « {item} » (attendu branche|Code1,Code2, au moins un code)")
    doubles = sorted({c for c in codes if codes.count(c) > 1})
    if doubles:
        raise LIVRER.Arret(REFUSE, "code demandé deux fois : " + ", ".join(doubles) + " — rien n'est publié")
    return branche, codes


def codes_inconnus(dossier, codes):
    """Rend les codes absents de la table des épreuves longues du dossier ; lève Arret si la table manque.

    ① RÔLE — Ne jamais demander au relais une épreuve qu'il refusera (« épreuve inconnue »).
    ② CONTEXTE D'APPEL — `envoyer_une_branche`, après la pose du dossier de travail, AVANT la publication.
    ③ ENTRÉE — `dossier` : le dossier de travail de la branche · `codes` : la liste demandée.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des codes inconnus (vide : tous connus).
      [rend: 1]
    ⑥ TRAITEMENT — Lit la clé « epreuves_longues » de LIVRER.TABLE (tests/LANCEMENT_DES_EPREUVES.json) du dossier,
      comme `main` de LIVRER ; garde les codes qui n'y sont pas.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — D-2 du RELU de Cowork (26-11-2026, 12h04) : « Inconnu » partait, « ENVOYÉ » était écrit, et le relais
      refuse (« epreuve inconnue », FABRIQUER_LE_CIRCUIT_PUBLIC.py). La table de LA BRANCHE fait foi : c'est elle
      que le relais lira.
    ⑨ CE QUI CLOCHE — Une table illisible (JSON faux) lève ValueError : `main` la compte comme un plantage, comme
      LIVRER.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    chemin = os.path.join(dossier, LIVRER.TABLE)
    if not os.path.isfile(chemin):
        raise LIVRER.Arret(REFUSE, f"{LIVRER.TABLE} absent de la branche : les codes ne peuvent pas être vérifiés")
    with open(chemin, encoding="utf-8") as f:
        table = json.load(f).get("epreuves_longues", {})
    return [c for c in codes if c not in table]


def envoyer_une_branche(racine, item, k):
    """Publie une branche et dépose sa demande ; rend (branche, pointe, codes) ; lève Arret sur tout refus.

    ① RÔLE — Le travail complet pour UNE entrée.
    ② CONTEXTE D'APPEL — `main`, une fois par entrée.
    ③ ENTRÉE — `racine` : le clone privé · `item` : « branche|Code1,Code2 » · `k` : les constantes du fabricant
      (LIVRER.constantes_du_fabricant).
    ④ CONDITIONS D'ENTRÉE — « git fetch origin » fait juste avant (par `main`).
    ⑤ SORTIE — TROIS valeurs : la branche, la pointe privée publiée (40 caractères), la liste des codes.
      [rend: 3]
    ⑥ TRAITEMENT — Dans l'ordre, arrêt au premier refus : ① `lire_l_entree` (entrée mal formée, code en double : D-6) ; ② la branche suit le motif de version
      du fabricant et n'est pas main ; ③ LIVRER.worktree_nomme (refus d'une branche absente d'origin ou d'une
      branche locale en avance) ; ④ `codes_inconnus` vide exigé ; ⑤ LIVRER.publier_au_public ; ⑥
      LIVRER.deposer_la_demande. Dans tous les cas, le dossier de travail créé ici est retiré
      (LIVRER.retirer_worktree) et le clone public effacé.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les codes sont vérifiés AVANT la publication : un refus ne laisse rien au public.
    ⑨ CE QUI CLOCHE — Un dossier de travail déjà posé par le Chat sur la branche est pris tel quel (propre et à la
      pointe d'origin exigés par worktree_nomme) et n'est pas retiré.
    ⑩ EFFET — Celui des fonctions de LIVRER appelées : poussées au public, dossiers sous /tmp créés puis retirés.
    ⑪ TERMINAISON — Rend la main, ou lève Arret ; un de mes appels peut-il ne pas revenir ? Non : les commandes de
      LIVRER sont bornées, l'attente d'une minute libre aussi : jusqu'à trois attentes d'une minute libre
      (≈ 183 s), puis refus (D-8).
      [sort: non]
    """
    branche, codes = lire_l_entree(item)
    if not re.match(k["motif_version"], branche) or branche == "main":
        raise LIVRER.Arret(REFUSE, f"branche refusée : {branche!r} (une version en attente travail-…)")
    wt, jetable, public = None, False, None
    try:
        wt, jetable = LIVRER.worktree_nomme(racine, branche)
        inconnus = codes_inconnus(wt, codes)
        if inconnus:
            raise LIVRER.Arret(REFUSE, "code(s) absent(s) de la clé epreuves_longues de " + LIVRER.TABLE + " : "
                               + ", ".join(inconnus) + " — rien n'est publié")
        pointe = LIVRER.git(wt, "rev-parse", "HEAD").stdout.strip()
        public, _ = LIVRER.publier_au_public(wt, branche)
        LIVRER.deposer_la_demande(public, branche, codes, pointe, k["nom_de_demande"])
        return branche, pointe, codes
    finally:
        if wt and jetable:
            LIVRER.retirer_worktree(racine, wt)
        if public:
            shutil.rmtree(public, ignore_errors=True)


def main():
    """Envoie chaque entrée de la ligne de commande ; sort avec 0, 1 ou 5.

    ① RÔLE — Voir l'en-tête.
    ② CONTEXTE D'APPEL — La ligne de commande (ou le relais ENVOYER_LES_EPREUVES_SUR_GITHUB.sh).
    ③ ENTRÉE — sys.argv : les entrées « branche|Code1,Code2 » ; la variable PRIVE.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête.
    ⑤ SORTIE — Rien : sort du programme (0, 1 ou 5, voir l'en-tête).
      [rend: rien]
    ⑥ TRAITEMENT — Aucune entrée → refus, code 1. Puis, une fois pour toutes : LIVRER.constantes_du_fabricant de la
      racine et « git fetch -q origin » ; un échec refuse toutes les entrées (« (toutes) »). Puis chaque entrée par
      `envoyer_une_branche` : réussite → ligne ENVOYÉ ; Arret → ligne REFUSÉ et code au moins 1 ; toute autre
      exception → ligne PLANTAGE, la trace (passée par `masquer`, ligne par ligne : D-10), et code 5. Une entrée qui tombe n'arrête pas les suivantes.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un plantage n'est jamais lu comme un envoi ni comme un refus (même règle que LIVRER, code 5).
    ⑨ CE QUI CLOCHE — Voir l'en-tête : le relais n'est pas suivi.
    ⑩ EFFET — Voir l'en-tête.
    ⑪ TERMINAISON — Sort du programme par sys.exit.
      [sort: oui]
    """
    racine = os.path.abspath(os.environ.get("PRIVE") or os.getcwd())
    entrees = sys.argv[1:]
    code = ENVOYE
    if not entrees:
        ligne("REFUSÉ", "(toutes)", ": usage : ENVOYER_LES_EPREUVES_SUR_GITHUB.py branche|Code1,Code2 [...]")
        sys.exit(REFUSE)
    try:
        k = LIVRER.constantes_du_fabricant(racine)
        if LIVRER.git(racine, "fetch", "-q", "origin").returncode != 0:
            raise LIVRER.Arret(REFUSE, f"fetch du dépôt privé refusé dans {racine}")
    except LIVRER.Arret as e:
        ligne("REFUSÉ", "(toutes)", f": {e.args[1]} — rien n'est envoyé")
        sys.exit(REFUSE)
    for item in entrees:
        nom = item.partition("|")[0] or "?"
        try:
            branche, pointe, codes = envoyer_une_branche(racine, item, k)
            ligne("ENVOYÉ", branche, f"{pointe[:9]} : {','.join(codes)}")
        except LIVRER.Arret as e:
            ligne("REFUSÉ", nom, f": {e.args[1]}")
            code = max(code, REFUSE)
        except Exception as e:   # noqa: BLE001 — un plantage n'est jamais lu comme un envoi ni comme un refus
            ligne("PLANTAGE", nom, f": {type(e).__name__} : {e}")
            LIVRER.dire(masquer(traceback.format_exc().rstrip()))
            code = PLANTAGE
    sys.exit(code)


if __name__ == "__main__":
    main()
