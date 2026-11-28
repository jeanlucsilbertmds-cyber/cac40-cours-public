#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRANSPORTER_LA_MOULINETTE.py — Ven 27-11-2026 (Paris). EN ESSAI · outil. Simulation uniquement : aucun ordre réel.

LE SENS EN TÊTE. A-965 (Jean-Luc, 21-11-2026 à 14h43, réponse « 1 » : « Construire ce lanceur unique » ; le lanceur
« répartit l'étape "jouer" sur la file des 18 places ») : les tranches de la moulinette se jouent sur les machines de
GitHub. Le lot W2f a écrit les deux bouts (programmes/DECOUPER_LA_MOULINETTE.py : « tranche » sur la machine,
« rassembler » au centre) ; ce programme est le CENTRE du TRANSPORT entre les deux. Le circuit est celui des épreuves
longues (epreuves_longues.yml du dépôt public, fabriqué par programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py), qui joue
désormais des FAMILLES DE TRANCHES : une entrée de tests/LANCEMENT_DES_EPREUVES.json qui porte « tranches » = N se
déplie en N codes « <famille>T<k> », chacun une machine, sa commande figée dans la table (k et N compris). Exemple
réel : la famille « MoulEssai » (fiche d'essai ESSAI-C5-2000-2026, 3 tranches).
  ① ENVOYER : publier la version en attente et déposer, par paquets d'au plus PLACES_DE_LA_MOULINETTE codes, les
    demandes des tranches voulues (toutes, ou celles « À REJOUER ») — par programmes/ENVOYER_LES_EPREUVES_SUR_GITHUB.py.
  ② RECEVOIR : rapatrier les sorties des passages (tests/outils/rapatrier_les_epreuves_longues.py), garder celles des
    tranches de la famille dont le code de sortie est 0, et les confier à DECOUPER_LA_MOULINETTE.rassembler, qui
    refuse tout bloc d'une autre chaîne et dit « À REJOUER » ; ce programme écrit alors la ligne qui les renvoie.

USAGE
    python3 -B programmes/TRANSPORTER_LA_MOULINETTE.py envoyer <branche travail-…> <FAMILLE> <k,k,…|toutes>
    python3 -B programmes/TRANSPORTER_LA_MOULINETTE.py recevoir <copie du centre> <FAMILLE> <passage> [<passage> …]
    (depuis la racine d'un clone COMPLET du dépôt privé, ou avec PRIVE=<ce clone>)

① RÔLE — Envoyer les tranches d'une famille sur GitHub et recevoir leurs blocs au centre, avec la reprise de celles qui
  sont tombées ou qui manquent.
② CONTEXTE D'APPEL — À la main, par le Chat (ou le pilote), une commande par geste. Aucune tâche automatique.
③ ENTRÉE — La ligne de commande (USAGE) ; la variable PRIVE (le clone privé ; par défaut le dossier courant).
  `<copie du centre>` : une COPIE du dépôt sans .git, à la version des tranches, où la chaîne de la famille est
  commencée (⓪ ① par l'enchaîneur ; pour la chaîne d'essai, ce programme la fait).
④ CONDITIONS D'ENTRÉE — Celles de ENVOYER_LES_EPREUVES_SUR_GITHUB (branche travail-… déjà poussée, clone complet) pour
  « envoyer » ; un clone git du privé pour « recevoir » (le rapatrieur y range les sorties).
⑤ SORTIE — UNE valeur, le code : « envoyer » : 0 tous les paquets envoyés · 1 un paquet refusé · 2 usage faux, famille
  ou tranche inconnue (R-734) · 5 un plantage d'ENVOYER. « recevoir » : celui de `rassembler` — 0 toutes les tranches
  sont là · 1 refus (bloc d'une autre chaîne, conflit ; rien n'est écrit) · 3 il en manque (« À REJOUER », avec la
  ligne d'envoi) — ou 2 si un contrôle n'a pas pu tourner (aucun passage lisible, famille inconnue, copie avec .git).
⑥ TRAITEMENT — Voir `envoyer`, `recevoir`, `main`.
⑦ UNITÉ — Tranches ; places (machines de GitHub en même temps).
⑧ POURQUOI — Voir le sens en tête. Aucun geste n'est réécrit ici (R-708) : la publication et le dépôt de la demande
  sont ceux d'ENVOYER (qui importe LIVRER), le rapatriement celui du rapatrieur, l'accueil et la reprise ceux de
  `rassembler`, le dépliage des familles celui du fabricant (`tranches_du_circuit`).
⑨ CE QUI CLOCHE — ① Le passage lancé par une demande n'est pas suivi (gh n'est pas exigé) : « recevoir » prend les
  numéros de passage en argument (page Actions du dépôt public, ou « gh run list »). ② Les paquets d'une même branche
  se suivent (groupe de passage « epreuves-longues-<branche> », « queue: max ») : au plus PLACES_DE_LA_MOULINETTE
  machines de cette branche à la fois, vague après vague ; la file des 18 places du réservoir (A-888) les borne
  aussi. ③ Une tranche qui rend 0 sans bloc lisible (sortie tronquée) est refusée par `rassembler` (bloc tronqué) :
  tout le paquet reçu est alors refusé, rien n'est écrit — la tranche fautive est nommée. ④ Le délai de JOUER dans
  l'enchaîneur (580 s) n'est pas porté à la borne du job : une vraie tranche de plus de 580 s tombe (code 124 de
  l'enchaîneur) ; la tranche d'essai n'y passe pas (DECOUPER, délai de 30 min). ⑤ Les sorties rapatriées restent sous
  tests/resultats/epreuves_longues/<passage>/ du clone privé (fichiers non suivis) : elles portent les résultats de
  la fiche jouée ; ce programme ne les affiche jamais.
⑩ EFFET — « envoyer » : celui d'ENVOYER (poussées au dépôt public : code de la branche, demandes). « recevoir » : des
  références refs/epreuves_lues/… et des fichiers sous tests/resultats/ du clone privé (le rapatrieur) ; dans la
  copie du centre, la chaîne (d'essai) et ses tranches reçues (DECOUPER).
⑪ TERMINAISON — Sort par sys.exit ; chaque commande lancée est bornée (git : 600 s par le rapatrieur ; ENVOYER : ses
  bornes). Un de mes appels peut-il ne pas revenir ? Non.
[sort: oui]
"""
import importlib.util
import json
import os
import sys

sys.dont_write_bytecode = True
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import DECOUPER_LA_MOULINETTE as D  # noqa: E402  les deux bouts du trajet vivent là (R-708)
import ENVOYER_LES_EPREUVES_SUR_GITHUB as ENV  # noqa: E402  publication et demande (par LIVRER), une fois (R-708)
import LIVRER  # noqa: E402  le chargement d'un programme par son chemin, une fois (R-708)

FABRICANT = os.path.join("programmes", "FABRIQUER_LE_CIRCUIT_PUBLIC.py")
RAPATRIEUR = os.path.join("tests", "outils", "rapatrier_les_epreuves_longues.py")
# LES PLACES D'UN PAQUET : au plus 8 tranches par demande, donc 8 machines de GitHub en même temps pour une branche
# (les paquets d'une même branche se suivent, ⑨ ②). Chiffre du plan du lot W2f (preuve W2f_LIVRE.md du 27-11-2026 :
# « 8 tranches de 2 625 versions, 1 vague » pour IND-001-RETEST), repris par le mandat du lot TRANSPORT ; le réservoir
# commun en a 18 (A-888 : 2 restent toujours libres pour le circuit du soir et le relais).
PLACES_DE_LA_MOULINETTE = 8
CODES = (0, 1, 2, 3, 5)


def fabricant(racine):
    """Rend le fabricant du circuit public de la racine, chargé comme module.

    ① RÔLE — Lire les familles et le dépliage des tranches là où ils sont écrits (R-708).
    ② CONTEXTE D'APPEL — `famille`.
    ③ ENTRÉE — `racine` : un clone ou une copie du dépôt.
    ④ CONDITIONS D'ENTRÉE — `racine`/programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py existe.
    ⑤ SORTIE — UNE valeur : le module.
    [rend: 1]
    ⑥ TRAITEMENT — LIVRER.charger.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le fabricant de LA VERSION traitée, jamais celui de ce dossier.
    ⑨ CE QUI CLOCHE — Le code de tête du fabricant s'exécute (il lit sa table).
    ⑩ EFFET — Exécute le code de tête du fabricant.
    ⑪ TERMINAISON — Rend la main, ou lève.
    [sort: non]
    """
    return LIVRER.charger(os.path.join(racine, FABRICANT), "FABRICANT_DU_TRANSPORT")


def famille(racine, nom):
    """Rend la famille de tranches `nom` de la table de la racine : (n, arguments, [codes de tranche]) ; lève ValueError.

    ① RÔLE — Savoir combien de tranches porte une famille, quelle commande elles jouent, et leurs codes.
    ② CONTEXTE D'APPEL — `envoyer`, `recevoir`.
    ③ ENTRÉE — `racine` ; `nom` : le code de la famille (exemple réel : MoulEssai).
    ④ CONDITIONS D'ENTRÉE — Le fabricant de la racine porte `tranches_du_circuit` (depuis le 27-11-2026).
    ⑤ SORTIE — TROIS valeurs : n ; les arguments de la tranche 0 (« {k} » et « {n} » remplacés) ; les codes, k croissant.
    [rend: 3]
    ⑥ TRAITEMENT — `tranches_du_circuit` du fabricant de la racine, gardées celles de la famille ; aucune → ValueError.
    ⑦ UNITÉ — Tranches.
    ⑧ POURQUOI — R-708 : le dépliage vit dans le fabricant, qui le fabrique aussi pour le relais.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui de `fabricant`.
    ⑪ TERMINAISON — Rend la main, ou lève.
    [sort: non]
    """
    F = fabricant(racine)
    if not hasattr(F, "tranches_du_circuit"):
        raise ValueError("le fabricant de %s ne connaît pas les familles de tranches (d'avant le 27-11-2026)" % racine)
    tranches = [t for t in F.tranches_du_circuit(racine) if t[3] == nom]
    if not tranches:
        raise ValueError("famille de tranches inconnue de la table de %s : %r" % (racine, nom))
    return tranches[0][5], tranches[0][2], [t[0] for t in tranches]


def lire_les_k(texte, n):
    """Rend la liste des k demandés (« toutes », ou « 0,2,5 ») ; lève ValueError.

    ① RÔLE — Lire la liste des tranches à envoyer, sans en deviner aucune (R-734).
    ② CONTEXTE D'APPEL — `main`, mode envoyer.
    ③ ENTRÉE — `texte` ; `n` : le nombre de tranches de la famille.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des k, dans l'ordre donné, chacun une fois.
    [rend: 1]
    ⑥ TRAITEMENT — « toutes » → 0 … n-1 ; sinon des entiers séparés par des virgules, lus par D.entier (chiffres ASCII
      sans zéro de tête), chacun < n, sans doublon.
    ⑦ UNITÉ — Tranches.
    ⑧ POURQUOI — La ligne « À REJOUER » de `recevoir` s'écrit dans cette forme.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main, ou lève.
    [sort: non]
    """
    if texte == "toutes":
        return list(range(n))
    ks = [D.entier(x, "k", 0) for x in texte.split(",")]
    if any(k >= n for k in ks) or len(set(ks)) != len(ks):
        raise ValueError("tranches %r : chacune une fois, de 0 à %d" % (texte, n - 1))
    return ks


def paquets(codes, taille=PLACES_DE_LA_MOULINETTE):
    """Rend les codes coupés en paquets d'au plus `taille`, dans l'ordre.

    ① RÔLE — Une demande par paquet : au plus PLACES_DE_LA_MOULINETTE machines d'une branche à la fois.
    ② CONTEXTE D'APPEL — `envoyer`.
    ③ ENTRÉE — `codes` : une liste ; `taille` ≥ 1.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des paquets (listes non vides).
    [rend: 1]
    ⑥ TRAITEMENT — tranches contiguës de la liste.
    ⑦ UNITÉ — Codes.
    ⑧ POURQUOI — Commentaire de PLACES_DE_LA_MOULINETTE ; une demande reste aussi sous les 1 000 octets du relais
      (8 codes de 20 caractères au plus).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    return [codes[i:i + taille] for i in range(0, len(codes), taille)]


def envoyer(racine, branche, nom, texte_des_k):
    """Envoie les tranches demandées d'une famille, paquet par paquet ; rend le code de sortie.

    ① RÔLE — Le geste ① du sens en tête.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` : le clone privé ; `branche` : la version en attente (travail-…) ; `nom` : la famille ;
      `texte_des_k` : « toutes » ou « 0,2 ».
    ④ CONDITIONS D'ENTRÉE — Celles d'ENVOYER.
    ⑤ SORTIE — UNE valeur : 0, 1, 2 ou 5 (en-tête ⑤).
    [rend: 1]
    ⑥ TRAITEMENT — La famille lue dans la table du CLONE (`famille` sur la racine) ; les k ; les codes ; LIVRER.constantes_du_fabricant et « git fetch » (comme
      ENVOYER.main) ; pour chaque paquet, ENV.envoyer_une_branche(racine, « branche|codes », …) — ENVOYER y revérifie
      chaque code contre le fabricant de la branche — puis une ligne ENVOYÉ / REFUSÉ / PLANTAGE par ENV.ligne
      (masquée). Un paquet qui tombe n'arrête pas les suivants.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-708 : chaque geste est celui d'ENVOYER.
    ⑨ CE QUI CLOCHE — La famille est lue dans le clone, pas dans la branche : si les deux diffèrent, ENVOYER refuse
      les codes inconnus de la branche (« code(s) absent(s) »), jamais en silence. Chaque paquet republie la branche (ENVOYER publie puis dépose) : la seconde publication ne pousse
      rien si le code n'a pas changé (LIVRER.publier_au_public). Deux paquets dans la même minute : ENVOYER attend la
      minute suivante (nom de demande).
    ⑩ EFFET — Celui d'ENVOYER.
    ⑪ TERMINAISON — Rend la main ; ENVOYER est borné.
    [sort: non]
    """
    try:
        n, _, codes = famille(racine, nom)
        ks = lire_les_k(texte_des_k, n)
    except (ValueError, OSError) as e:
        ENV.ligne("REFUSÉ", branche, ": %s — rien n'est envoyé" % e)
        return 2
    voulus = [codes[k] for k in ks]
    try:
        k_fab = LIVRER.constantes_du_fabricant(racine)
        if LIVRER.git(racine, "fetch", "-q", "origin").returncode != 0:
            raise LIVRER.Arret(ENV.REFUSE, "fetch du dépôt privé refusé dans %s" % racine)
    except LIVRER.Arret as e:
        ENV.ligne("REFUSÉ", branche, ": %s — rien n'est envoyé" % e.args[1])
        return 1
    code = 0
    for paquet in paquets(voulus):
        item = "%s|%s" % (branche, ",".join(paquet))
        try:
            b, pointe, cs = ENV.envoyer_une_branche(racine, item, k_fab)
            ENV.ligne("ENVOYÉ", b, "%s : %s" % (pointe[:9], ",".join(cs)))
        except LIVRER.Arret as e:
            ENV.ligne("REFUSÉ", branche, ": %s" % e.args[1])
            code = max(code, 1)
        except Exception as e:   # noqa: BLE001 — un plantage n'est jamais lu comme un envoi ni comme un refus
            ENV.ligne("PLANTAGE", branche, ": %s : %s" % (type(e).__name__, e))
            code = 5
    return code


def sorties_des_passages(racine, passages, codes, depuis="origin"):
    """Rapatrie les passages et rend ({k : chemin de SORTIE.txt}, lignes à dire, passages lus).

    ① RÔLE — Trouver, pour chaque tranche de la famille, une sortie de code 0 parmi les passages donnés.
    ② CONTEXTE D'APPEL — `recevoir`.
    ③ ENTRÉE — `racine` : le clone privé ; `passages` : des numéros ; `codes` : les codes de tranche, k croissant ;
      `depuis` : le dépôt d'où lire les branches (« origin » ; les épreuves donnent un dépôt local).
    ④ CONDITIONS D'ENTRÉE — Le rapatrieur existe dans la racine.
    ⑤ SORTIE — TROIS valeurs : {k : [chemins de SORTIE.txt de code 0]} (plusieurs si plusieurs passages l'ont jouée :
      `rassembler` les compare) ; les lignes (bilans masqués, tranches tombées) ; le nombre de passages lisibles.
    [rend: 3]
    ⑥ TRAITEMENT — Pour chaque passage : `rapatrier` du rapatrieur de la racine (code 2 d'une tranche ABSENTE : normal,
      elle est À REJOUER) ; un bilan qui commence par « ARRET » = passage illisible. Puis, pour chaque code de la
      famille, le dossier tests/resultats/epreuves_longues/<passage>/<code>/ : RESULTAT.json lisible et code 0 → la
      sortie est gardée ; sinon « TOMBÉE ». Les branches d'autres codes du passage sont ignorées.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le code de sortie est LU dans RESULTAT.json (comme le rapatrieur), jamais déduit de la couleur du job ;
      une tranche tombée n'est pas offerte à `rassembler` (une sortie coupée au délai peut porter un bloc incomplet).
    ⑨ CE QUI CLOCHE — Les lignes du bilan reprennent des messages de git : passées par ENV.masquer.
    ⑩ EFFET — Celui du rapatrieur (références et fichiers dans la racine).
    ⑪ TERMINAISON — Rend la main ; le rapatrieur borne git.
    [sort: non]
    """
    spec = importlib.util.spec_from_file_location("RAPATRIEUR_DU_TRANSPORT", os.path.join(racine, RAPATRIEUR))
    R = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(R)
    recues, lignes, lus = {}, [], 0
    for passage in passages:
        _code, bilan = R.rapatrier(racine, passage, depuis)
        lignes += [ENV.masquer(b) for b in bilan]
        if bilan and bilan[0].startswith("ARRET"):
            continue
        lus += 1
        for k, c in enumerate(codes):
            dossier = os.path.join(racine, R.RANGEMENT, passage, c)
            if not os.path.isdir(dossier):
                continue
            try:
                with open(os.path.join(dossier, "RESULTAT.json"), encoding="utf-8") as fh:
                    cs = json.load(fh)["code_de_sortie"]
            except (OSError, ValueError, KeyError, TypeError):
                cs = None
            if cs == 0 and os.path.isfile(os.path.join(dossier, "SORTIE.txt")):
                recues.setdefault(k, []).append(os.path.join(dossier, "SORTIE.txt"))
            else:
                lignes.append("TOMBÉE : %s du passage %s (code de sortie %r) — sa sortie n'est pas reçue" % (c, passage,
                                                                                                          cs))
    return recues, lignes, lus


def recevoir(racine, copie, nom, passages, branche=None, depuis="origin"):
    """Reçoit au centre les tranches d'une famille jouées par des passages ; rend le code de sortie.

    ① RÔLE — Le geste ② du sens en tête.
    ② CONTEXTE D'APPEL — `main` ; les épreuves.
    ③ ENTRÉE — `racine` : le clone privé ; `copie` : la copie du centre (sans .git) ; `nom` : la famille ;
      `passages` : des numéros ; `branche` : la version, pour la ligne « À REJOUER » (None : « <branche> ») ;
      `depuis` : comme `sorties_des_passages`.
    ④ CONDITIONS D'ENTRÉE — La chaîne de la famille est commencée dans la copie (⓪ ①), sauf la chaîne d'essai, que ce
      programme fait (D.chaine_d_essai).
    ⑤ SORTIE — UNE valeur : 0, 1, 2 ou 3 (en-tête ⑤).
    [rend: 1]
    ⑥ TRAITEMENT — .git dans la copie → 2 ; la famille lue dans la table de la COPIE (la version reçue) ; la chaîne par
      D.chaine_de_la_commande ; commande « tranche-essai » → D.chaine_d_essai(copie, n) ; `sorties_des_passages` ;
      aucun passage lisible → 2 ; D.rassembler(copie, S, E, n, sorties) ; code 3 → la ligne d'envoi des k manquants.
    ⑦ UNITÉ — Tranches.
    ⑧ POURQUOI — L'accueil, le refus d'une tranche d'une autre chaîne et la reprise sont ceux de `rassembler` (R-708).
    ⑨ CE QUI CLOCHE — En-tête ⑨ ③.
    ⑩ EFFET — En-tête ⑩.
    ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    if os.path.lexists(os.path.join(copie, ".git")):
        print("ARRÊT : %s porte .git — le centre reçoit dans une copie (A-861)" % copie)
        return 2
    try:
        n, arguments, codes = famille(copie, nom)
        sid, essai = D.chaine_de_la_commande(arguments)
        if arguments[0] == "tranche-essai":
            D.chaine_d_essai(copie, n)
        recues, lignes, lus = sorties_des_passages(racine, passages, codes, depuis)
    except (ValueError, OSError, D.V.Impossible) as e:
        print("CONTRÔLE IMPOSSIBLE (R-734) : %s: %s" % (type(e).__name__, e))
        return 2
    for ligne in lignes:
        print(ligne)
    if not lus:
        print("CONTRÔLE IMPOSSIBLE (R-734) : aucun des passages %s n'a pu être lu" % " ".join(passages))
        return 2
    chemins = [c for k in sorted(recues) for c in recues[k]]
    try:
        code, manquent = D.rassembler(copie, sid, essai, n, chemins)
    except (ValueError, OSError, D.V.Impossible) as e:
        print("CONTRÔLE IMPOSSIBLE (R-734) : %s: %s" % (type(e).__name__, e))
        return 2
    if code == 3:
        print("POUR LES REJOUER : python3 -B programmes/TRANSPORTER_LA_MOULINETTE.py envoyer %s %s %s"
              % (branche or "<branche>", nom, ",".join(str(k) for k in manquent)))
    return code


def main(argv):
    """Rend le code de sortie de la ligne de commande.

    ① RÔLE — Aiguiller vers le mode.
    ② CONTEXTE D'APPEL — `__main__`.
    ③ ENTRÉE — `argv` (USAGE) ; PRIVE.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : en-tête ⑤.
    [rend: 1]
    ⑥ TRAITEMENT — « envoyer » : 3 arguments ; « recevoir » : au moins 3 ; « --depuis=<dépôt> » facultatif pour
      recevoir (les épreuves) ; « --branche=<nom> » facultatif pour la ligne « À REJOUER » ; sinon l'usage, code 2.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Celui du mode.
    ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    racine = os.path.abspath(os.environ.get("PRIVE") or os.getcwd())
    options = [a for a in argv[1:] if a.startswith("--")]
    a = [x for x in argv[1:] if not x.startswith("--")]
    depuis, branche = "origin", None
    for o in options:
        if o.startswith("--depuis=") and a[:1] == ["recevoir"]:
            depuis = o[len("--depuis="):]
        elif o.startswith("--branche=") and a[:1] == ["recevoir"]:
            branche = o[len("--branche="):]
        else:
            a = []
    if len(a) == 4 and a[0] == "envoyer":
        return envoyer(racine, a[1], a[2], a[3])
    if len(a) >= 4 and a[0] == "recevoir" and all(p.isascii() and p.isdigit() for p in a[3:]):
        return recevoir(racine, os.path.abspath(a[1]), a[2], a[3:], branche, depuis)
    print(__doc__.split("① RÔLE")[0])
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
