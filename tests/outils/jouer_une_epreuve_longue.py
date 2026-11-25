#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""jouer_une_epreuve_longue — Dim 15-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Étape GHUB ② (décisions de Jean-Luc A-809, A-811, A-816 du 15-11-2026, « GitHub en priorité ») : une
épreuve longue d'un tenant se joue sur une machine de GitHub, au circuit .github/workflows/epreuves_longues.yml du
dépôt public. La demande ne donne qu'un CODE ; ce programme lit la commande FIGÉE de ce code dans la table
« epreuves_longues » de tests/LANCEMENT_DES_EPREUVES.json de la version jouée, la lance, et écrit, pour le dépôt PRIVÉ
seulement, la sortie entière et le code de sortie.

① RÔLE — Deux usages. (a) `--matrice <racine> <liste>` : valider une liste de codes (« toutes », ou des codes séparés
  par des virgules) contre la table de la racine, et écrire la matrice JSON du circuit, [{"code": …}, …]. (b) `<copie>
  <code> --sortie=<dossier>` : jouer l'épreuve de ce code sur la copie, comme la certification de nuit la lance (la
  copie pour racine, sans la configuration Git de la machine, sans les fichiers de commandes de GitHub), et écrire
  dans <dossier> SORTIE.txt (la sortie entière, erreurs comprises) et RESULTAT.json (code, commande, heures, durée,
  pointe jouée lue dans POINTE_JOUEE, et, depuis le 25-11-2026 (A-995), le détail que l'épreuve a écrit dans le
  fichier nommé par RESULTAT_DE_L_EPREUVE, sous « detail_de_l_epreuve »).
② CONTEXTE D'APPEL — Le circuit des épreuves longues fabriqué par programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py : (a) au
  pas « Fabriquer la matrice » du job « preparer », (b) au pas « Jouer l epreuve » du job « jouer », sous
  « unshare -rn » (réseau coupé). Aussi l'épreuve tests/EPREUVES_DU_CIRCUIT_DES_EPREUVES_LONGUES_Dim_15-11-2026.py.
③ ENTRÉE — (a) la racine, la liste ; (b) la copie jouée (racine d'un dépôt sans .git), le code, `--sortie=<dossier>`.
④ CONDITIONS D'ENTRÉE — programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, programmes/CERTIFIER_LA_VERSION.py et
  tests/outils/jouer_une_part.py existent dans la racine (ou la copie) : la table se lit par le fabricant, la
  configuration Git à retirer par le certificateur, les programmes interdits par le joueur des parts (R-708).
⑤ SORTIE — Le code de sortie. (a) 0 et la matrice sur la sortie standard ; 2 si la liste est refusée (la raison sur
  la sortie d'erreur). (b) le code de sortie de l'épreuve si elle a été lancée (124 si elle a dépassé DELAI) ; 2 si
  elle n'a pas pu l'être (code inconnu, fichier absent, programme interdit, sortie impossible à écrire) : un contrôle
  qui n'a pas pu tourner rend un code non nul (R-734).
  [rend: 1]
⑥ TRAITEMENT — (a) `lire_la_liste`. (b) `jouer` : la table de la COPIE (`epreuves_du_circuit` du fabricant de la
  copie), le code cherché, le fichier vérifié (présent, pas un lien, dans la copie, ne nomme aucun programme
  interdit), puis `python3 -B <copie>/<chemin> <arguments>` lancé dans la copie, sortie et erreurs écrites au fil de
  l'eau dans SORTIE.txt, arrêt du groupe de processus au délai de `delai_restant` (le temps qui reste au job, au
  plus DELAI secondes) ; RESULTAT.json écrit après.
⑦ UNITÉ — Des secondes.
⑧ POURQUOI — Point 1 de l'étape GHUB ② : aucun argument libre ne vient de la demande, la commande est celle de la
  table. Lancement imité de celui de la nuit (`jouer` de programmes/CERTIFIER_LA_VERSION.py) : même racine, même
  environnement nettoyé ; mais la sortie est écrite ENTIÈRE dans un fichier (la nuit n'en garde que trois lignes),
  car c'est elle que le Chat rapatrie pour juger l'épreuve.
⑨ CE QUI CLOCHE — Sans la mesure de couverture (la nuit l'a) : une épreuve qui dépend de cette mesure se comporterait
  autrement ; aucune n'est connue. Une épreuve qui écrit dans la copie peut gêner une autre : sur GitHub, chaque
  épreuve a sa machine. La copie est celle du circuit (sans .git) : une épreuve qui exige un dépôt git à sa racine
  rougit, comme elle rougirait la nuit. La recherche d'un programme interdit dans le texte de l'épreuve est une
  recherche de NOM : une épreuve qui fabriquerait ce nom par morceaux n'est pas vue (la copie jouée ne porte de
  toute façon pas ces programmes : le circuit les retire).
⑩ EFFET — (a) aucun ; (b) écrit SORTIE.txt et RESULTAT.json dans le dossier de sortie, et ce qu'écrit l'épreuve.
⑪ TERMINAISON — Rend la main ; l'épreuve est arrêtée au délai de `delai_restant` (au plus DELAI secondes). Un de mes
  appels peut-il ne pas revenir ? Le lancement, borné par ce délai ; le circuit borne aussi le job
  (DUREE_D_UNE_EPREUVE_LONGUE du fabricant).
  [sort: oui]
"""
import datetime
import importlib.util
import json
import os
import re
import signal
import subprocess
import sys
import tempfile
import time
import zoneinfo

PARIS = zoneinfo.ZoneInfo("Europe/Paris")
FABRICANT = os.path.join("programmes", "FABRIQUER_LE_CIRCUIT_PUBLIC.py")
CERTIFICATEUR = os.path.join("programmes", "CERTIFIER_LA_VERSION.py")
JOUEUR_DES_PARTS = os.path.join("tests", "outils", "jouer_une_part.py")
# LE PLAFOND, 320 minutes : sous les 330 du job « jouer » du circuit, pour que RESULTAT.json soit écrit et déposé avant
# la coupure. Depuis le 15-11-2026 (R-D7 du relecteur, jugé DE FOND), la coupure réelle est le temps qui RESTE au job
# (`delai_restant`), quand le circuit donne l'heure de départ du job (DEPART_DU_JOB) ; le plafond reste la borne.
DELAI = 320 * 60
SORTIE = "SORTIE.txt"
RESULTAT = "RESULTAT.json"
# Le détail facultatif qu'une épreuve écrit pour RESULTAT.json (25-11-2026, A-995) : la variable qui en donne le chemin,
# le nom du fichier, et sa taille au plus (au-delà, il n'est pas rangé : RESULTAT.json reste court).
RESULTAT_DE_L_EPREUVE = "RESULTAT_DE_L_EPREUVE"
DETAIL = "DETAIL.json"
DETAIL_AU_PLUS = 64 * 1024


def lire_le_detail(chemin, resultat):
    """Range dans `resultat` le détail qu'une épreuve a écrit, s'il existe.

    ① RÔLE — Porter dans RESULTAT.json ce qu'une épreuve sait dire d'elle-même (pour « Livraison » : verdict, pointe,
    empreinte). ② CONTEXTE D'APPEL — `jouer`, après l'épreuve. ③ ENTRÉE — `chemin` : le fichier donné à l'épreuve
    par RESULTAT_DE_L_EPREUVE ; `resultat` : le dictionnaire de RESULTAT.json. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Aucune valeur ; `resultat` reçoit « detail_de_l_epreuve » (un objet JSON lu), ou « detail_illisible »
    (la raison), ou rien si l'épreuve n'a rien écrit. [rend: 0] ⑥ TRAITEMENT — absent : rien ; plus de DETAIL_AU_PLUS
    octets, JSON illisible ou pas un objet : « detail_illisible ». ⑦ UNITÉ — Des octets. ⑧ POURQUOI — Décision A-995 :
    le RESULTAT.json du contrôle final porte le verdict, la pointe et l'empreinte ; la plupart des épreuves n'écrivent
    rien, et leur RESULTAT.json ne change pas. ⑨ CE QUI CLOCHE — Le détail est écrit par le code de la version jouée :
    il ne prouve rien de plus que la sortie de l'épreuve ; le code de sortie reste celui du processus.
    ⑩ EFFET — Lit un fichier. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    if not os.path.lexists(chemin):
        return
    try:
        if os.path.islink(chemin) or os.path.getsize(chemin) > DETAIL_AU_PLUS:
            raise ValueError(f"lien, ou plus de {DETAIL_AU_PLUS} octets")
        with open(chemin, encoding="utf-8") as f:
            d = json.load(f)
        if not isinstance(d, dict):
            raise ValueError("pas un objet JSON")
        resultat["detail_de_l_epreuve"] = d
    except (OSError, ValueError) as e:
        resultat["detail_illisible"] = f"{type(e).__name__} : {e}"


def charger(racine, chemin, nom):
    """Charge un programme de la racine comme un module, par son chemin.

    ① RÔLE — Lire la table par le fabricant, la configuration Git par le certificateur, les interdits par le joueur
    des parts, ceux de la racine jouée (R-708). ② CONTEXTE D'APPEL — `lire_la_liste`, `jouer`. ③ ENTRÉE — `racine`,
    `chemin` relatif, `nom` du module. ④ CONDITIONS D'ENTRÉE — Le fichier existe. ⑤ SORTIE — UNE valeur : le module.
    [rend: 1] ⑥ TRAITEMENT — importlib, sans passer par sys.path. ⑦ UNITÉ — — ⑧ POURQUOI — Toujours le voisin de la
    version jouée, jamais un module de même nom chargé d'ailleurs. ⑨ CE QUI CLOCHE — Le code de tête du module
    s'exécute (le fabricant lit sa table et fabrique ses gabarits, environ un dixième de seconde). ⑩ EFFET — Lit et
    exécute un fichier de la racine. ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]
    """
    spec = importlib.util.spec_from_file_location(nom, os.path.join(racine, chemin))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def lire_la_liste(racine, liste):
    """Rend la matrice du circuit pour une liste de codes demandée.

    ① RÔLE — Usage (a) de la fiche en tête. ② CONTEXTE D'APPEL — `main`, avec `--matrice`. ③ ENTRÉE — `racine` : la
    version jouée ; `liste` : « toutes », ou des codes séparés par des virgules. ④ CONDITIONS D'ENTRÉE — Fiche en
    tête, ④. ⑤ SORTIE — UNE valeur : la liste [{"code": …}, …], dans l'ordre demandé (dans l'ordre de la table pour
    « toutes »). Lève ValueError si la liste est refusée. [rend: 1] ⑥ TRAITEMENT — forme de la liste ; chaque code
    connu de la table (`epreuves_du_circuit`), une seule fois ; son fichier présent dans la racine et non interdit
    (`refus_du_fichier`). ⑦ UNITÉ — — ⑧ POURQUOI — Le relais valide déjà la liste, mais il ne lit pas la version
    jouée : un code de la table de main absent de la version en attente se voit ICI, avant d'occuper une machine.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lit la racine. ⑪ TERMINAISON — Rend la main, ou lève. [sort: non]
    """
    F = charger(racine, FABRICANT, "FABRICANT_DE_L_EPREUVE_LONGUE")
    table = {c: (ch, a) for c, ch, a in F.epreuves_du_circuit(racine)}
    if liste == F.TOUTES:
        codes = list(table)
    elif re.fullmatch(F.CODE_DE_SERIE + "(?:," + F.CODE_DE_SERIE + ")*", liste or ""):
        codes = liste.split(",")
    else:
        raise ValueError(f"liste d'épreuves illisible : {liste[:80]!r} (« toutes », ou des codes séparés par des virgules)")
    if not codes:
        raise ValueError("aucune épreuve longue dans la table")
    if len(set(codes)) != len(codes):
        raise ValueError("une épreuve est demandée deux fois")
    for c in codes:
        if c not in table:
            raise ValueError(f"épreuve inconnue de la table : {c}")
        refus = refus_du_fichier(racine, table[c][0])
        if refus:
            raise ValueError(f"épreuve {c} : {refus}")
    return [{"code": c} for c in codes]


def refus_du_fichier(racine, chemin):
    """Rend la raison de ne pas lancer le fichier d'une épreuve, ou "" s'il peut l'être.

    ① RÔLE — Garder la porte du lancement : le fichier est là, c'est un vrai fichier de la racine, il n'est pas
    interdit. ② CONTEXTE D'APPEL — `lire_la_liste`, `jouer`. ③ ENTRÉE — `racine`, `chemin` relatif.
    ④ CONDITIONS D'ENTRÉE — tests/outils/jouer_une_part.py est dans la racine. ⑤ SORTIE — UNE valeur : le texte de
    la raison, vide si rien. [rend: 1] ⑥ TRAITEMENT — absent ; lien symbolique ou chemin réel hors de la racine ;
    nom d'INTERDITS (du joueur des parts) ; texte qui nomme un programme d'INTERDITS (son nom sans « .py »).
    ⑦ UNITÉ — — ⑧ POURQUOI — Point 3 de l'étape GHUB ② : « une épreuve qui nomme un programme interdit est exclue » ;
    la liste vit une fois, chez le joueur des parts (R-708). ⑨ CE QUI CLOCHE — Fiche en tête, ⑨ (recherche de nom).
    ⑩ EFFET — Lit le fichier. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    p = os.path.join(racine, chemin)
    if not os.path.isfile(p):
        return f"{chemin} absent de la version jouée"
    if os.path.islink(p) or os.path.realpath(p) != os.path.join(os.path.realpath(racine), os.path.normpath(chemin)):
        return f"{chemin} est un lien, ou hors de la version jouée"
    interdits = charger(racine, JOUEUR_DES_PARTS, "JOUEUR_DES_PARTS_DE_L_EPREUVE_LONGUE").INTERDITS
    if os.path.basename(chemin) in interdits:
        return f"{chemin} est un programme interdit dans ce circuit"
    texte = open(p, encoding="utf-8", errors="replace").read()
    nommes = [n for n in interdits if n[:-3] in texte]
    if nommes:
        return f"{chemin} nomme un programme interdit dans ce circuit ({', '.join(nommes)})"
    return ""


def delai_restant(F, depart, maintenant):
    """Rend le délai de l'épreuve, en secondes : le temps qui reste au job, moins la marge d'écriture, borné par DELAI.

    ① RÔLE — Couper l'épreuve AVANT que GitHub ne coupe le job, quelle qu'ait été la durée de l'installation.
    ② CONTEXTE D'APPEL — `jouer`, une fois, juste avant le lancement ; l'épreuve du circuit des épreuves longues (E7).
    ③ ENTRÉE — `F` : le fabricant de la copie jouée (DUREE_D_UNE_EPREUVE_LONGUE, MARGE_D_ECRITURE, en minutes) ·
      `depart` : le texte de DEPART_DU_JOB (secondes depuis 1970, écrit par le pas « depart » du job), ou None ·
      `maintenant` : l'heure, en secondes depuis 1970.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un nombre entier de secondes, au moins 1, au plus DELAI.
      [rend: 1]
    ⑥ TRAITEMENT — `depart` absent ou qui n'est pas un nombre entier : DELAI. Sinon : DUREE × 60 − MARGE × 60 −
      (maintenant − depart), ramené entre 1 et DELAI.
    ⑦ UNITÉ — Des secondes (DUREE et MARGE sont en minutes : × 60).
    ⑧ POURQUOI — R-D7 du relecteur du 15-11-2026 : le job dure DUREE minutes, dont l'installation (logiciels, paquets,
      clonage) ; une épreuve coupée à une constante pouvait l'être par GitHub avant d'écrire RESULTAT.json. La durée du
      job s'écrit UNE fois, dans le fabricant, qui fabrique aussi le « timeout-minutes » du job (R-708).
    ⑨ CE QUI CLOCHE — Sans DEPART_DU_JOB (pas « depart » tombé, lancement à la main), le plafond DELAI s'applique, comme
      avant. L'heure de la machine est crue.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    try:
        debut = int(depart)
    except (TypeError, ValueError):
        return DELAI
    reste = F.DUREE_D_UNE_EPREUVE_LONGUE * 60 - F.MARGE_D_ECRITURE * 60 - (int(maintenant) - debut)
    return max(1, min(DELAI, reste))


def jouer(copie, code, sortie):
    """Joue l'épreuve d'un code sur la copie ; rend le code de sortie du programme.

    ① RÔLE — Usage (b) de la fiche en tête. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `copie`, `code`, `sortie` (le
    dossier où écrire). ④ CONDITIONS D'ENTRÉE — Fiche en tête, ④. ⑤ SORTIE — UNE valeur : le code de l'épreuve, 124
    si elle a dépassé DELAI, 2 si elle n'a pas pu être lancée. [rend: 1] ⑥ TRAITEMENT — Fiche en tête, ⑥ (b).
    RESULTAT.json est écrit dans tous les cas où le dossier de sortie peut l'être, refus compris (clé « refus »).
    ⑦ UNITÉ — Des secondes. ⑧ POURQUOI — Fiche en tête, ⑧. ⑨ CE QUI CLOCHE — Fiche en tête, ⑨.
    ⑩ EFFET — Lance un processus ; écrit deux fichiers. ⑪ TERMINAISON — Rend la main ; DELAI au plus. [sort: non]
    """
    # LA POINTE JOUÉE (20-11-2026 au soir, consigne A) : le commit privé que « preparer » a cloné et vérifié, passé
    # par le circuit (POINTE_JOUEE) ; INSTALLER n'accepte une preuve que si elle porte le code relu par Cowork.
    pointe = os.environ.get("POINTE_JOUEE", "")
    resultat = {"code_epreuve": code, "delai_secondes": DELAI,
                "pointe_jouee": pointe if re.fullmatch(r"[0-9a-f]{40}", pointe) else ""}
    try:
        os.makedirs(sortie, exist_ok=True)
    except OSError as e:
        print(f"ARRET dossier de sortie impossible : {e}", file=sys.stderr)
        return 2

    def ecrire(code_de_sortie):
        """Écrit RESULTAT.json et rend le code. ① RÔLE — Une seule écriture du résultat. ② CONTEXTE D'APPEL —
        `jouer`. ③ ENTRÉE — le code. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le code, ou 2 si l'écriture
        tombe. [rend: 1] ⑥ TRAITEMENT — json. ⑦ UNITÉ — — ⑧ POURQUOI — Le rapatriement lit ce fichier.
        ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit un fichier. ⑪ TERMINAISON — Rend la main. [sort: non]"""
        resultat["code_de_sortie"] = code_de_sortie
        try:
            with open(os.path.join(sortie, RESULTAT), "w", encoding="utf-8") as f:
                json.dump(resultat, f, ensure_ascii=False, indent=1)
                f.write("\n")
        except OSError as e:
            print(f"ARRET résultat non écrit : {e}", file=sys.stderr)
            return 2
        return code_de_sortie

    try:
        F = charger(copie, FABRICANT, "FABRICANT_DE_L_EPREUVE_LONGUE")
        table = {c: (ch, a) for c, ch, a in F.epreuves_du_circuit(copie)}
        if code not in table:
            raise ValueError(f"épreuve inconnue de la table : {code}")
        chemin, arguments = table[code]
        resultat.update(chemin=chemin, arguments=arguments)
        refus = refus_du_fichier(copie, chemin)
        if refus:
            raise ValueError(refus)
        C = charger(copie, CERTIFICATEUR, "CERTIFICATEUR_DE_L_EPREUVE_LONGUE")
        env = dict(os.environ, PYTHONUNBUFFERED="1", **C.SANS_LA_CONFIGURATION_GIT_DE_LA_MACHINE)
        for v in F.FICHIERS_DE_COMMANDES_DE_GITHUB:
            env.pop(v, None)
    except Exception as e:   # noqa: BLE001 — tout échec avant le lancement est un refus dit, jamais un vert
        resultat["refus"] = f"{type(e).__name__} : {e}"
        print(f"ARRET {resultat['refus']}", file=sys.stderr)
        ecrire(2)
        return 2
    args = [sys.executable, "-B", os.path.join(copie, chemin)] + [a.replace("{copie}", copie) for a in arguments]
    # LE DÉTAIL DE L'ÉPREUVE (25-11-2026, A-995) : un fichier neuf, hors de la copie et du dossier déposé, dont le nom
    # est donné à l'épreuve par RESULTAT_DE_L_EPREUVE ; si elle y écrit un objet JSON, il est rangé dans RESULTAT.json
    # sous « detail_de_l_epreuve » (programmes/CONTROLER_LA_LIVRAISON_SUR_GITHUB.py y met verdict, pointe, empreinte).
    detail = os.path.join(tempfile.mkdtemp(prefix="detail_"), DETAIL)
    env[RESULTAT_DE_L_EPREUVE] = detail
    delai = delai_restant(F, os.environ.get("DEPART_DU_JOB"), time.time())
    resultat["delai_secondes"] = delai
    debut = time.time()
    resultat["debut"] = datetime.datetime.now(PARIS).strftime("%Y-%m-%d %H:%M:%S")
    with open(os.path.join(sortie, SORTIE), "wb") as f:
        p = subprocess.Popen(args, cwd=copie, env=env, stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                             start_new_session=True)
        try:
            code_de_sortie = p.wait(timeout=delai)
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, signal.SIGKILL)
            p.wait()
            code_de_sortie = 124
            f.write(f"\nARRÊTÉE : plus de {delai} s\n".encode("utf-8"))
    resultat["fin"] = datetime.datetime.now(PARIS).strftime("%Y-%m-%d %H:%M:%S")
    resultat["duree_secondes"] = round(time.time() - debut)
    lire_le_detail(detail, resultat)
    code_ecrit = ecrire(code_de_sortie)
    print(f"épreuve {code} : code {code_de_sortie}, {resultat['duree_secondes']} s")
    return code_de_sortie if code_ecrit == code_de_sortie else 2


def main():
    """La ligne de commande (fiche en tête).

    ① RÔLE — Aiguiller vers l'usage (a) ou (b). ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — sys.argv.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le code de sortie. [rend: 1] ⑥ TRAITEMENT — `--matrice
    <racine> <liste>`, ou `<copie> <code> --sortie=<dossier>` ; toute autre forme : usage, code 2.
    ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Fiche en tête. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    a = sys.argv[1:]
    if len(a) == 3 and a[0] == "--matrice":
        try:
            print(json.dumps(lire_la_liste(a[1], a[2]), separators=(",", ":")))
        except Exception as e:   # noqa: BLE001 — un refus, jamais une matrice
            print(f"ARRET {type(e).__name__} : {e}", file=sys.stderr)
            return 2
        return 0
    if len(a) == 3 and a[2].startswith("--sortie=") and not a[0].startswith("--") and not a[1].startswith("--"):
        return jouer(os.path.abspath(a[0]), a[1], os.path.abspath(a[2][len("--sortie="):]))
    print("usage : jouer_une_epreuve_longue.py --matrice <racine> <liste> | <copie> <code> --sortie=<dossier>",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
