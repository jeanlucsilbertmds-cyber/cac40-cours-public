#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_ENVOYER_LES_EPREUVES_SUR_GITHUB — Jeu 26-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Éprouve programmes/ENVOYER_LES_EPREUVES_SUR_GITHUB.py SANS RÉSEAU, dans les mondes jetables du
harnais de LIVRER (tests/EPREUVES_DE_LIVRER_ET_INSTALLER_Ven_20-11-2026.py, IMPORTÉ et non recopié : sa classe
`Monde` bâtit un privé et un public nus, une branche travail-x poussée au privé, un clone privé, et son faux
fabricant publie comme le vrai). Une seule retouche : le faux fabricant de chaque monde commence par appeler la
VRAIE fonction `refus_selon_l_historique` du fabricant de la racine éprouvée, pour que le refus d'un clone
superficiel emprunte le vrai chemin (celui que le programme ne recopie pas).

① RÔLE — Dire, cas par cas, si le programme envoie ce qu'il doit et refuse ce qu'il doit (défauts D-1 à D-5 du RELU
  de Cowork du 26-11-2026, 12h04 ; D-6, D-7 et D-10 du RELU de 12h45) ; avec « --saboter », que chaque garde du programme, retirée, fait rougir au moins
  un cas (« MORD ») — sinon « NE MORD PAS » et code 1.
② CONTEXTE D'APPEL — À la main, depuis la racine : python3 -B tests/EPREUVES_ENVOYER_LES_EPREUVES_SUR_GITHUB_Jeu_26-11-2026.py
  [<racine>] [--saboter].
③ ENTRÉE — La racine éprouvée (par défaut le dossier courant) ; « --saboter ».
④ CONDITIONS D'ENTRÉE — git et python3 installés ; aucun réseau nécessaire.
⑤ SORTIE — Une ligne « OK » ou « ÉCHEC » par cas, une ligne « MORD » ou « NE MORD PAS » par sabotage, un BILAN. Le
  code de sortie : 0 tout passe (et chaque sabotage mord) ; 1 sinon ; 2 option inconnue.
⑥ TRAITEMENT — Chaque cas : un `Monde` neuf, le programme copié (saboté ou non) à côté de LIVRER.py et de ses deux
  modules, un lancement, puis des vérifications sur l'ÉTAT des dépôts : code de sortie, raison du refus, demandes
  présentes au public avec leur statut git (A ajouté, M modifié), lignes « ENVOYÉ », dossiers laissés sous /tmp,
  et, pour tout refus, l'ENSEMBLE des branches du public avant et après (D-7 : une propriété, pas un compte — un
  refus ne crée aucune branche publique). Les jetons des cas J, B64 et T2 sont FICTIFS, assemblés à l'exécution.
⑦ UNITÉ — Secondes (durée affichée).
⑧ POURQUOI — R-731 : épreuves à la main avec sabotages ; « un jeu d'épreuves se sabote contre sa propre
  correction ».
⑨ CE QUI CLOCHE — Le fabricant est faux (sauf son étage A) : la vraie publication n'est pas jouée. Le vrai GitHub et
  le relais ne sont pas joués : « ENVOYÉ » n'est confronté qu'au dépôt public local. Le compte des clones publics
  laissés lit /tmp/livrer_pub_* avant et après chaque cas : un LIVRER lancé en même temps ailleurs sur la machine
  peut faire rougir à tort. Le cas D-1 « même minute » prend la minute suivante sans attendre
  (LIVRER_SANS_ATTENTE_DE_MINUTE, posé par le harnais) : l'attente réelle (jusqu'à trois fois ≈ 61 s) n'est pas
  jouée. Le cas T2 provoque le plantage par une copie de LIVRER.py dont `worktree_nomme` lève une exception
  portant les jetons fictifs : c'est le chemin du plantage qui est éprouvé, pas une cause réelle de plantage.
  L'ensemble des branches publiques ne voit pas une branche publique DÉJÀ là que le refus aurait republiée (cas
  « noms pris ») : seul ce cas-là publie avant de refuser, et c'est voulu.
⑩ EFFET — Crée et efface des dossiers temporaires ; aucun dépôt réel touché.
⑪ TERMINAISON — Sort par sys.exit ; chaque lancement est borné à 300 s par le harnais.
"""
import glob
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

NOM = "ENVOYER_LES_EPREUVES_SUR_GITHUB.py"
HARNAIS = "tests/EPREUVES_DE_LIVRER_ET_INSTALLER_Ven_20-11-2026.py"
RELAIS = "ENVOYER_LES_EPREUVES_SUR_GITHUB.sh"   # le relais bash, qui passe la main au programme
COMPAGNONS = ("LIVRER.py", "CONTRATS_DES_FICHIERS.py", "FORME_D_UN_JETON.py")
ETAGE_A = r'''import importlib.util, os, sys
_s = importlib.util.spec_from_file_location("VRAI_FAB", os.environ["VRAI_FABRICANT"])
_F = importlib.util.module_from_spec(_s); _s.loader.exec_module(_F)
try:
    _F.refus_selon_l_historique(sys.argv[1], sys.argv[2], [], exclus=(sys.argv[2],))
except OSError as _e:
    print("ARRET — l'etage A n'a pas pu tourner ; RIEN n'est publie :", _e); sys.exit(1)
'''
# Le dépôt à la main que faisait le script bash (nom à la minute, « open(…, "w") » qui écrase) : sabotage S5.
A_LA_MAIN = ('nom = "demandes/DEMANDE_" + datetime.now(LIVRER.PARIS).strftime("%Y-%m-%d_%Hh%M") + ".txt"; '
             'os.makedirs(os.path.join(public, "demandes"), exist_ok=True); '
             'open(os.path.join(public, nom), "w").write("circuit=epreuve\\nepreuves=" + ",".join(codes) + "\\npointe=" + pointe + "\\n"); '
             'LIVRER.git(public, "add", nom); LIVRER.git(public, "commit", "-q", "-m", "demande"); '
             'LIVRER.git(public, "push", "-q", "origin", "HEAD:refs/heads/" + branche)')
# M1, M2 du RELU de 12h45 (D-7) : la table absente acceptée ; la vérification des codes déplacée APRÈS la publication.
TABLE_ABSENTE = ('    if not os.path.isfile(chemin):\n'
                 '        raise LIVRER.Arret(REFUSE, f"{LIVRER.TABLE} absent de la branche : les codes ne peuvent pas être vérifiés")\n')
VERIF = ('        inconnus = codes_inconnus(wt, codes)\n'
         '        if inconnus:\n'
         '            raise LIVRER.Arret(REFUSE, "code(s) absent(s) de la clé epreuves_longues de " + LIVRER.TABLE + " : "\n'
         '                               + ", ".join(inconnus) + " — rien n\'est publié")\n')
PUBLIE = ('        pointe = LIVRER.git(wt, "rev-parse", "HEAD").stdout.strip()\n'
          '        public, _ = LIVRER.publier_au_public(wt, branche)\n')
VERIF_PUIS_PUBLIE, PUBLIE_PUIS_VERIF = VERIF + PUBLIE, PUBLIE + VERIF
SABOTAGES = (
    ("S1 codes non vérifiés (D-2)", "        if inconnus:\n", "        if False:\n"),
    ("S2 codes vides acceptés", "if not barre or not branche or not codes:", "if not barre or not branche:"),
    ("S3 refus affiché ENVOYÉ", 'ligne("REFUSÉ", nom, f": {e.args[1]}")', 'ligne("ENVOYÉ", nom, f": {e.args[1]}")'),
    ("S4 code final forcé à 0", "    sys.exit(code)\n", "    sys.exit(0)\n"),
    ("S5 demande écrite à la main, avec écrasement (D-1)",
     'LIVRER.deposer_la_demande(public, branche, codes, pointe, k["nom_de_demande"])', A_LA_MAIN),
    ("S6 branche main acceptée", 'not re.match(k["motif_version"], branche) or branche == "main"', "False"),
    ("S7 plantage compté comme refus", "            code = PLANTAGE\n", "            code = max(code, REFUSE)\n"),
    ("S8 dossier de travail laissé", "        if wt and jetable:\n", "        if False:\n"),
    ("S9 clone public laissé", "            shutil.rmtree(public, ignore_errors=True)\n", "            pass\n"),
    ("S10 fetch non vérifié", '"fetch", "-q", "origin").returncode != 0', '"fetch", "-q", "origin").returncode == 999'),
    ("S11 jeton non masqué", "        claire = JETON.sub(b\"***\", brute)\n", "        claire = brute\n"),
    ("S12 codes en double acceptés (D-6)", "    if doubles:\n", "    if False:\n"),
    ("S13 base64 nu non masqué (D-10)", "if FORME.porte_une_forme_de_jeton(claire) else claire", "if False else claire"),
    ("S14 table absente acceptée (D-7, M1)", TABLE_ABSENTE, "    if not os.path.isfile(chemin):\n        return []\n"),
    ("S15 codes vérifiés après la publication (D-7, M2)", VERIF_PUIS_PUBLIE, PUBLIE_PUIS_VERIF),
    ("S16 trace non masquée (D-7, M4)", "LIVRER.dire(masquer(traceback.format_exc().rstrip()))",
     "LIVRER.dire(traceback.format_exc().rstrip())"),
    ("S17 motif de version retiré (D-7, M8)", 'not re.match(k["motif_version"], branche) or branche == "main"',
     'branche == "main"'),
)
# Une copie de LIVRER.py dont `worktree_nomme` plante avec les jetons fictifs de PLANTAGE_FICTIF (cas T2).
PLANTAGE = """

def worktree_nomme(racine, branche):   # épreuve T2 : plantage imprévu dont le message porte des jetons fictifs
    raise RuntimeError(os.environ["PLANTAGE_FICTIF"])
"""


def charger_le_harnais(source):
    """Importe le harnais de LIVRER ; rend le module.

    ① RÔLE — Réutiliser `Monde` et le faux fabricant sans les recopier (R-708). ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `source` : la racine. ④ CONDITIONS D'ENTRÉE — Le harnais s'importe sans rien lancer (main gardé).
    ⑤ SORTIE — UNE valeur : le module.
      [rend: 1]
    ⑥ TRAITEMENT — importlib. ⑦ UNITÉ — — ⑧ POURQUOI — Consigne du pilote V8 (26-11-2026, 12h07) : importer, pas recopier.
    ⑨ CE QUI CLOCHE — Une évolution du harnais change ces mondes. ⑩ EFFET — Exécute la tête du harnais.
    ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    spec = importlib.util.spec_from_file_location("HARNAIS_DE_LIVRER", os.path.join(source, HARNAIS))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def copier(source, dossier, sabotage=None):
    """Copie le programme et ses compagnons dans `dossier`, avec au plus un sabotage ; lève ValueError si l'ancre manque.

    ① RÔLE — Éprouver une copie, jamais le dépôt. ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `source` · `dossier` · `sabotage` : (nom, avant, après) ou None. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — Copie ; « avant » doit être trouvé UNE fois dans le programme, remplacé par « après ».
    ⑦ UNITÉ — — ⑧ POURQUOI — Une ancre absente ne saboterait rien. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit des fichiers. ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    os.makedirs(dossier, exist_ok=True)
    for p in COMPAGNONS + (NOM, RELAIS):
        shutil.copyfile(os.path.join(source, "programmes", p), os.path.join(dossier, p))
    if sabotage:
        chemin = os.path.join(dossier, NOM)
        texte = open(chemin, encoding="utf-8").read()
        if texte.count(sabotage[1]) != 1:
            raise ValueError(f"ancre de {sabotage[0]} trouvée {texte.count(sabotage[1])} fois")
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(texte.replace(sabotage[1], sabotage[2]))


def monde(H, source, progs):
    """Rend un monde du harnais dont le faux fabricant passe d'abord par le VRAI étage A.

    ① RÔLE — Un monde neuf par cas. ② CONTEXTE D'APPEL — `jouer`. ③ ENTRÉE — `H` : le harnais · `source` · `progs`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le monde.
      [rend: 1]
    ⑥ TRAITEMENT — H.Monde ; fab.py réécrit : ETAGE_A puis le corps de H.FAUX_FABRICANT ; PRIVE retiré de
      l'environnement ; VRAI_FABRICANT posé.
    ⑦ UNITÉ — — ⑧ POURQUOI — Le refus d'un clone superficiel vit dans le vrai fabricant : le témoin doit l'emprunter.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Crée un dossier temporaire. ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    m = H.Monde(source, progs)
    with open(os.path.join(m.t, "fab.py"), "w") as f:
        f.write("#!/usr/bin/env python3\n" + ETAGE_A + H.FAUX_FABRICANT.split("\n", 1)[1])
    m.env.pop("PRIVE", None)
    m.env["VRAI_FABRICANT"] = os.path.join(source, "programmes", "FABRIQUER_LE_CIRCUIT_PUBLIC.py")
    return m


def demandes(m, branche):
    """Rend la liste des (statut, fichier) des commits qui touchent demandes/ sur la branche publique.

    ① RÔLE — Lire ce qui a été déposé, et COMMENT (A ajouté, M modifié). ② CONTEXTE D'APPEL — Les vérifications.
    ③ ENTRÉE — `m` · `branche`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la liste (vide si la branche
      publique n'existe pas).
      [rend: 1]
    ⑥ TRAITEMENT — « git log --name-status -- demandes/ » au public nu. ⑦ UNITÉ — — ⑧ POURQUOI — Le relais exige un
      fichier AJOUTÉ (D-1). ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lit. ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if not m.git(m.public, "rev-parse", "-q", "--verify", f"refs/heads/{branche}").strip():
        return []
    sortie = m.git(m.public, "log", "--format=", "--name-status", f"refs/heads/{branche}", "--", "demandes/")
    return [tuple(l.split("\t", 1)) for l in sortie.splitlines() if l.strip()]


def restes(m, avant):
    """Rend ce que le lancement a laissé : dossiers de travail du clone et clones publics nouveaux sous /tmp.

    ① RÔLE — Garder le nettoyage (S8, S9). ② CONTEXTE D'APPEL — `verifier`.
    ③ ENTRÉE — `m` · `avant` : l'ensemble des /tmp/livrer_pub_* d'avant. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des chemins laissés.
      [rend: 1]
    ⑥ TRAITEMENT — « git worktree list » des clones du monde (lignes /tmp/livrer_) + glob nouveaux.
    ⑦ UNITÉ — — ⑧ POURQUOI — LIVRER ne retire que ce que son appelant lui demande de retirer.
    ⑨ CE QUI CLOCHE — Un LIVRER lancé ailleurs en même temps peut créer un /tmp/livrer_pub_* (voir l'en-tête).
    ⑩ EFFET — Lit. ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    laisses = []
    for clone in (m.clone, os.path.join(m.t, "sup")):
        if os.path.isdir(clone):
            laisses += [l.split(" ", 1)[1] for l in m.git(clone, "worktree", "list", "--porcelain").splitlines()
                        if l.startswith("worktree /tmp/livrer_")]
    return laisses + sorted(set(glob.glob("/tmp/livrer_pub_*")) - avant)


def branches_publiques(m):
    """Rend l'ensemble des noms de branches du public du monde.

    ① RÔLE — La propriété « un refus ne publie rien » (D-7 du RELU de Cowork, 26-11-2026, 12h45).
    ② CONTEXTE D'APPEL — `lancer`, avant et après chaque lancement.
    ③ ENTRÉE — `m` : le monde.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un frozenset de noms (« main », « travail-x »…).
      [rend: 1]
    ⑥ TRAITEMENT — « git for-each-ref refs/heads » au public nu.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un ENSEMBLE, pas un compte : une branche publiée à la place d'une autre se voit (R-751 : un
      garde-fou porte sur une propriété, jamais sur un compte).
    ⑨ CE QUI CLOCHE — Une branche publique déjà présente et republiée ne change pas l'ensemble (voir l'en-tête).
    ⑩ EFFET — Lit.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return frozenset(m.git(m.public, "for-each-ref", "--format=%(refname:short)", "refs/heads").split())


def lancer(m, *entrees):
    """Lance le programme éprouvé dans le monde ; rend (code, sortie, restes, branches publiques avant et après).

    ① RÔLE — Un lancement, et ce qu'il laisse. ② CONTEXTE D'APPEL — Les cas.
    ③ ENTRÉE — `m` · `entrees`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — QUATRE valeurs : le code, stdout+stderr, la
      liste des restes, le couple (branches publiques avant, après) de `branches_publiques`.
      [rend: 4]
    ⑥ TRAITEMENT — m.programme ; puis `restes`, et chaque reste est effacé (un clone public seulement si son origin
      est le public de CE monde). ⑦ UNITÉ — — ⑧ POURQUOI — Un sabotage ne doit rien laisser sous /tmp.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Celui du programme ; efface ce qu'il a laissé.
    ⑪ TERMINAISON — Rend la main (300 s au plus, harnais).
      [sort: non]
    """
    avant, publiques = set(glob.glob("/tmp/livrer_pub_*")), branches_publiques(m)
    r = m.programme(NOM, *entrees)
    laisses = restes(m, avant)
    for chemin in laisses:   # ce qui a été laissé est effacé ici, après avoir été compté (sabotages S8, S9)
        if chemin.startswith("/tmp/livrer_pub_") and m.git(chemin, "remote", "get-url", "origin").strip() == m.public:
            shutil.rmtree(chemin, ignore_errors=True)
        elif chemin.startswith("/tmp/livrer_wt_"):
            for clone in (m.clone, os.path.join(m.t, "sup")):
                if os.path.isdir(clone):
                    m.git(clone, "worktree", "remove", "--force", chemin)
    return r.returncode, r.stdout + r.stderr, laisses, (publiques, branches_publiques(m))


def refus(code, sortie, laisses, publiques, d, motif, attendu=1):
    """Rend la liste des écarts d'un cas de refus : code, raison, aucune demande, aucun ENVOYÉ, rien laissé, aucune branche publique neuve.

    ① RÔLE — Les six vérifications communes à tout refus (D-3 du RELU de 12h04 : l'absence d'« ENVOYÉ » vérifiée
      partout ; D-7 du RELU de 12h45 : l'ensemble des branches publiques inchangé).
    ② CONTEXTE D'APPEL — Les cas de refus. ③ ENTRÉE — le lancement (`publiques` : le couple avant, après de
      `lancer`), `d` : les demandes, `motif` : la raison attendue (expression régulière), `attendu` : le code.
      ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des écarts (vide : le cas passe).
      [rend: 1]
    ⑥ TRAITEMENT — Comparaisons. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    e = []
    if code != attendu:
        e.append(f"code {code} au lieu de {attendu}")
    if not re.search(motif, sortie):
        e.append(f"raison « {motif} » absente")
    if d:
        e.append(f"demande(s) déposée(s) : {d}")
    if " ENVOYÉ " in sortie:
        e.append("« ENVOYÉ » écrit")
    if laisses:
        e.append(f"laissé : {laisses}")
    if publiques[0] != publiques[1]:
        e.append(f"branches publiques changées : {sorted(publiques[0])} → {sorted(publiques[1])}")
    return e


def cas_nominal(m):
    """Nominal : ENVOYÉ, UNE demande AJOUTÉE au bon format, pointe publique = demande, code 0, rien laissé.

    ① RÔLE — Le chemin de l'envoi. ② CONTEXTE D'APPEL — `jouer`. ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des écarts.
      [rend: 1]
    ⑥ TRAITEMENT — Un envoi de travail-x. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lance.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    code, sortie, laisses, _ = lancer(m, "travail-x|CircuitPublic,GardeFou")
    pointe = m.git(m.prive, "rev-parse", "refs/heads/travail-x").strip()
    d, e = demandes(m, "travail-x"), []
    if code != 0:
        e.append(f"code {code}")
    if not re.search(r"(?m)^\d\dh\d\d ENVOYÉ travail-x " + pointe[:9] + " : CircuitPublic,GardeFou$", sortie):
        e.append("ligne ENVOYÉ absente ou fausse")
    if len(d) != 1 or d[0][0] != "A":
        e.append(f"demandes : {d}")
    else:
        texte = m.montrer("refs/heads/travail-x", d[0][1], m.public)
        if texte != f"circuit=epreuve\nepreuves=CircuitPublic,GardeFou\npointe={pointe}\n":
            e.append(f"contenu de la demande : {texte!r}")
    if laisses:
        e.append(f"laissé : {laisses}")
    return e


def cas_meme_minute(m):
    """D-1 et D-4 : deux envois de travail-x à la suite ; le 2e (branche publique déjà là) dépose une demande NEUVE.

    ① RÔLE — Jamais une demande MODIFIÉE. ② CONTEXTE D'APPEL — `jouer`. ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des écarts.
      [rend: 1]
    ⑥ TRAITEMENT — Deux lancements ; deux ENVOYÉ, deux fichiers distincts, tous au statut A.
    ⑦ UNITÉ — — ⑧ POURQUOI — D-1 du RELU de Cowork (26-11-2026, 12h04). ⑨ CE QUI CLOCHE — La minute suivante est
      prise sans attendre (LIVRER_SANS_ATTENTE_DE_MINUTE). ⑩ EFFET — Lance. ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    c1, s1, l1, _ = lancer(m, "travail-x|CircuitPublic")
    c2, s2, l2, _ = lancer(m, "travail-x|GardeFou")
    d, e = demandes(m, "travail-x"), []
    if (c1, c2) != (0, 0) or s1.count(" ENVOYÉ ") + s2.count(" ENVOYÉ ") != 2:
        e.append(f"codes {c1},{c2} ; sorties : {s1.strip()[-200:]} | {s2.strip()[-200:]}")
    if len(d) != 2 or {s for s, _ in d} != {"A"} or len({f for _, f in d}) != 2:
        e.append(f"demandes : {d}")
    if l1 or l2:
        e.append(f"laissé : {l1 + l2}")
    return e


def cas_noms_pris(m):
    """D-1 : tous les noms de minute proches déjà pris au public → REFUSÉ, aucune demande modifiée ni ajoutée.

    ① RÔLE — Le refus quand aucun nom neuf n'est libre, et la garde contre l'écrasement (S5). ② CONTEXTE D'APPEL — `jouer`.
    ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la liste des écarts.
      [rend: 1]
    ⑥ TRAITEMENT — Un premier envoi ; puis des demandes posées au public pour les minutes de −2 à +6 ; second envoi.
    ⑦ UNITÉ — Minutes. ⑧ POURQUOI — D-1. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Pousse au public du monde.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    lancer(m, "travail-x|CircuitPublic")
    w = os.path.join(m.t, "pose")
    m.git(None, "clone", "-q", "--branch", "travail-x", m.public, w)
    os.makedirs(os.path.join(w, "demandes"), exist_ok=True)
    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo
    maintenant = datetime.now(ZoneInfo("Europe/Paris"))
    for k in range(-2, 7):
        nom = "demandes/DEMANDE_" + (maintenant + timedelta(minutes=k)).strftime("%Y-%m-%d_%Hh%M") + ".txt"
        if not os.path.exists(os.path.join(w, nom)):
            open(os.path.join(w, nom), "w").write("circuit=epreuve\nepreuves=CircuitPublic\npointe=x\n")
    m.git(w, "add", "-A")
    m.git(w, "commit", "-q", "-m", "noms pris")
    m.git(w, "push", "-q", "origin", "travail-x")
    avant = demandes(m, "travail-x")
    code, sortie, laisses, publiques = lancer(m, "travail-x|GardeFou")
    apres = demandes(m, "travail-x")
    nouvelles = apres[:len(apres) - len(avant)]
    e = refus(code, sortie, laisses, publiques, nouvelles, r"REFUSÉ travail-x : nom de demande impossible")
    if any(s != "A" for s, _ in apres):
        e.append(f"demande modifiée : {apres}")
    return e


def cas_refus(entrees, motif, reglage=None, attendu=1, branche="travail-x"):
    """Fabrique un cas de refus : lancement, puis `refus`.

    ① RÔLE — Écrire chaque cas de refus en une ligne. ② CONTEXTE D'APPEL — `CAS`.
    ③ ENTRÉE — `entrees` · `motif` · `reglage` : fonction (m) appelée avant · `attendu` · `branche` : celle dont on
      compte les demandes. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la fonction du cas.
      [rend: 1]
    ⑥ TRAITEMENT — Fermeture. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    def cas(m):
        """Le cas de refus.

        ① RÔLE — Voir `cas_refus`. ② CONTEXTE D'APPEL — `jouer`. ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : la liste des écarts.
          [rend: 1]
        ⑥ TRAITEMENT — `reglage`, `lancer`, `refus`. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lance.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        if reglage:
            reglage(m)
        code, sortie, laisses, publiques = lancer(m, *entrees)
        return refus(code, sortie, laisses, publiques, demandes(m, branche) + demandes(m, "main"), motif, attendu)
    return cas


def regler_refus_du_fabricant(m):
    """Le faux fabricant refuse la publication (FAUX_FAB_REFUSE du harnais).

    ① RÔLE — Réglage. ② CONTEXTE D'APPEL — Le cas F. ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — Variable posée. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    m.env["FAUX_FAB_REFUSE"] = "1"


def regler_superficiel(m):
    """Le clone privé lancé est SUPERFICIEL (« --depth 1 »), désigné par PRIVE.

    ① RÔLE — Réglage. ② CONTEXTE D'APPEL — Le cas S. ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — « git clone --depth 1 --no-single-branch file://<privé> sup » ; PRIVE=sup ; superficiel vérifié.
    ⑦ UNITÉ — — ⑧ POURQUOI — D-5 du RELU : la copie de la session est superficielle ; le refus doit dire le remède.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Clone. ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    sup = os.path.join(m.t, "sup")
    m.git(None, "clone", "-q", "--depth", "1", "--no-single-branch", "file://" + m.prive, sup)
    if m.git(sup, "rev-parse", "--is-shallow-repository").strip() != "true":
        raise RuntimeError("le clone d'épreuve n'est pas superficiel")
    m.env["PRIVE"] = sup


def regler_branche_en_avance(m):
    """La branche locale travail-x du clone porte un commit non poussé.

    ① RÔLE — Réglage. ② CONTEXTE D'APPEL — Le cas L. ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — Commit vide sur une branche locale. ⑦ UNITÉ — — ⑧ POURQUOI — Rien d'effacé par « -B ».
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit au clone. ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    m.git(m.clone, "branch", "-q", "travail-x", "origin/travail-x")
    w = os.path.join(m.t, "avance")
    m.git(m.clone, "worktree", "add", "-q", w, "travail-x")
    m.git(w, "commit", "-q", "--allow-empty", "-m", "non poussé")
    m.git(m.clone, "worktree", "remove", "--force", w)


def regler_origin_injoignable(m):
    """L'origin du clone désigne un chemin absent : le fetch échoue.

    ① RÔLE — Réglage. ② CONTEXTE D'APPEL — Le cas R. ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — « git remote set-url ». ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit au clone.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    m.git(m.clone, "fetch", "-q", "origin")
    m.git(m.clone, "remote", "set-url", "origin", os.path.join(m.t, "absent.git"))


def regler_table_illisible(m):
    """Pousse au privé une branche travail-p dont la table des épreuves n'est pas du JSON (plantage attendu).

    ① RÔLE — Réglage. ② CONTEXTE D'APPEL — Le cas P. ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — Clone, table réécrite « { », commit, poussée. ⑦ UNITÉ — — ⑧ POURQUOI — Exception imprévue → code 5.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Pousse au privé du monde. ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    w = os.path.join(m.t, "table")
    m.git(None, "clone", "-q", "--branch", "travail-x", m.prive, w)
    m.git(w, "checkout", "-q", "-b", "travail-p")
    open(os.path.join(w, "tests", "LANCEMENT_DES_EPREUVES.json"), "w").write("{")
    m.git(w, "commit", "-q", "-am", "table illisible")
    m.git(w, "push", "-q", "origin", "travail-p")


def cas_mele(m):
    """Mêlé : une branche refusée (absente), une envoyée → code 1, une seule demande.

    ① RÔLE — Une entrée qui tombe n'arrête pas les suivantes. ② CONTEXTE D'APPEL — `jouer`. ③ ENTRÉE — `m`.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la liste des écarts.
      [rend: 1]
    ⑥ TRAITEMENT — — ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lance. ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    code, sortie, laisses, _ = lancer(m, "travail-zz|CircuitPublic", "travail-x|CircuitPublic")
    d, e = demandes(m, "travail-x"), []
    if code != 1:
        e.append(f"code {code}")
    if not re.search(r"REFUSÉ travail-zz : origin/travail-zz introuvable", sortie) or sortie.count(" ENVOYÉ travail-x ") != 1:
        e.append("lignes : " + sortie.strip()[-300:])
    if len(d) != 1 or d[0][0] != "A" or demandes(m, "travail-zz"):
        e.append(f"demandes : {d}")
    if laisses:
        e.append(f"laissé : {laisses}")
    return e


def cas_jeton(m):
    """Un jeton dans l'entrée n'est jamais affiché en clair.

    ① RÔLE — Garder le masquage (S11). ② CONTEXTE D'APPEL — `jouer`. ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des écarts.
      [rend: 1]
    ⑥ TRAITEMENT — Entrée sans « | » faite d'un faux jeton (assemblé ici, jamais écrit d'un tenant dans ce fichier).
    ⑦ UNITÉ — — ⑧ POURQUOI — Le bash masquait ; le programme lit FORME_D_UN_JETON.py. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lance. ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    jeton = "github" + "_pat_" + "A1b2C3d4" * 4
    code, sortie, laisses, publiques = lancer(m, jeton)
    e = refus(code, sortie, laisses, publiques, demandes(m, "travail-x"), r"REFUSÉ \S* : entrée mal formée « \*\*\* »")
    if jeton in sortie:
        e.append("jeton affiché en clair")
    return e


def pousser_une_branche(m, nom, retirer_la_table=False):
    """Pousse au privé du monde une branche `nom` faite de travail-x, sans sa table des épreuves si demandé.

    ① RÔLE — Réglage commun des cas T et H. ② CONTEXTE D'APPEL — `regler_table_absente`, `regler_branche_autre`.
    ③ ENTRÉE — `m` · `nom` : la branche à créer · `retirer_la_table` : retirer tests/LANCEMENT_DES_EPREUVES.json.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — Clone de travail-x, nouvelle branche, table retirée (commit) si demandé, poussée au privé.
    ⑦ UNITÉ — — ⑧ POURQUOI — Une branche qui EXISTE : sans elle, un mutant serait arrêté plus loin, par
      « introuvable », et le cas ne garderait rien. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Pousse au privé du monde.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    w = os.path.join(m.t, "pousse_" + re.sub(r"\W", "_", nom))
    m.git(None, "clone", "-q", "--branch", "travail-x", m.prive, w)
    m.git(w, "checkout", "-q", "-b", nom)
    if retirer_la_table:
        m.git(w, "rm", "-q", "tests/LANCEMENT_DES_EPREUVES.json")
        m.git(w, "commit", "-q", "-m", "table retirée")
    m.git(w, "push", "-q", "origin", nom)


def regler_table_absente(m):
    """Pousse au privé une branche travail-t SANS tests/LANCEMENT_DES_EPREUVES.json (cas T, D-7 ②, mutant M1).

    ① RÔLE — Réglage. ② CONTEXTE D'APPEL — Le cas T. ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — `pousser_une_branche`. ⑦ UNITÉ — — ⑧ POURQUOI — D-7 du RELU de 12h45 : aucun cas ne gardait le
      refus d'une table absente. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Pousse au privé du monde. ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    pousser_une_branche(m, "travail-t", retirer_la_table=True)


def regler_branche_autre(m):
    """Pousse au privé une branche « autre », hors du motif de version (cas H, D-7 ③, mutant M8).

    ① RÔLE — Réglage. ② CONTEXTE D'APPEL — Le cas H. ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — Rien.
      [rend: rien]
    ⑥ TRAITEMENT — `pousser_une_branche`. ⑦ UNITÉ — — ⑧ POURQUOI — D-7 du RELU de 12h45 : seul « main » était
      essayé ; la branche existe, pour que le mutant M8 aille jusqu'à publier. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Pousse au privé du monde. ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    pousser_une_branche(m, "autre")


def jetons_fictifs():
    """Rend (jeton fin fictif en clair, base64 nu FICTIF de « x-access-token:<jeton classique fictif> »).

    ① RÔLE — Les jetons des cas B64 et T2, assemblés ici, jamais écrits d'un tenant dans ce fichier (il est publié,
      et le motif du dépôt le refuserait). ② CONTEXTE D'APPEL — `cas_base64_nu`, `cas_trace`. ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — DEUX valeurs : deux textes.
      [rend: 2]
    ⑥ TRAITEMENT — Concaténation, puis base64 standard sans retour à la ligne (la forme que calcule le circuit,
      `printf 'x-access-token:%s' "$JETON" | base64 -w0`). ⑦ UNITÉ — — ⑧ POURQUOI — D-10 du RELU de 12h45.
    ⑨ CE QUI CLOCHE — Fictifs : la forme suit les préfixes de GitHub. ⑩ EFFET — — ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    import base64
    clair = "github" + "_pat_" + "Q9w8E7r6" * 4
    nu = base64.b64encode(("x-access-token:" + "gh" + "p_" + "Z1y2X3w4" * 5).encode()).decode()
    return clair, nu


def ligne_masquee(m):
    """Rend la constante LIGNE_MASQUEE du programme éprouvé, lue dans sa copie (jamais recopiée ici, R-708).

    ① RÔLE — Le texte attendu à la place d'une ligne masquée. ② CONTEXTE D'APPEL — `cas_base64_nu`, `cas_trace`.
    ③ ENTRÉE — `m` : le monde (sa copie des programmes). ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte.
      [rend: 1]
    ⑥ TRAITEMENT — L'arbre syntaxique de la copie ; l'affectation LIGNE_MASQUEE. ⑦ UNITÉ — —
    ⑧ POURQUOI — Une écriture de la même chose à deux endroits diverge (R-708).
    ⑨ CE QUI CLOCHE — Absente : lève ValueError, le cas est rouge. ⑩ EFFET — Lit. ⑪ TERMINAISON — Rend la main, ou lève.
      [sort: non]
    """
    import ast
    for n in ast.parse(open(os.path.join(m.progs, NOM), encoding="utf-8").read()).body:
        if isinstance(n, ast.Assign) and [getattr(c, "id", None) for c in n.targets] == ["LIGNE_MASQUEE"]:
            return n.value.value
    raise ValueError("LIGNE_MASQUEE absente du programme")


def cas_base64_nu(m):
    """D-10 : un base64 nu fictif de « x-access-token:<jeton> » repris dans une ligne REFUSÉ n'est jamais affiché.

    ① RÔLE — Garder le masquage par la FONCTION porte_une_forme_de_jeton (S13). ② CONTEXTE D'APPEL — `jouer`.
    ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la liste des écarts.
      [rend: 1]
    ⑥ TRAITEMENT — Entrée « travail-x|<base64 nu> » : un code inconnu, repris par la raison du refus ; la ligne doit
      être remplacée en entier par LIGNE_MASQUEE ; refus ordinaire (code 1, rien publié).
    ⑦ UNITÉ — — ⑧ POURQUOI — D-10 du RELU de Cowork (26-11-2026, 12h45) : « 1 FUITE ». ⑨ CE QUI CLOCHE — La
      ligne masquée ne dit plus « REFUSÉ » : seul le code de sortie le dit. ⑩ EFFET — Lance.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    _, nu = jetons_fictifs()
    code, sortie, laisses, publiques = lancer(m, "travail-x|" + nu)
    e = refus(code, sortie, laisses, publiques, demandes(m, "travail-x"), re.escape(ligne_masquee(m)))
    if nu in sortie:
        e.append("base64 nu affiché en clair")
    return e


def cas_trace(m):
    """D-7 ④ et D-10 : la trace d'un plantage qui porte un jeton en clair et un base64 nu ne les affiche pas.

    ① RÔLE — Garder le masquage de la trace (S16, mutant M4) ligne par ligne (S13). ② CONTEXTE D'APPEL — `jouer`.
    ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la liste des écarts.
      [rend: 1]
    ⑥ TRAITEMENT — Une copie des programmes dans le monde, où LIVRER.py finit par PLANTAGE (`worktree_nomme` lève
      RuntimeError(PLANTAGE_FICTIF)) ; PLANTAGE_FICTIF = jeton en clair, saut de ligne, base64 nu. Attendu : code 5,
      ligne PLANTAGE, une trace (« Traceback »), LIGNE_MASQUEE, ni le jeton ni le base64, rien publié.
    ⑦ UNITÉ — — ⑧ POURQUOI — D-7 du RELU de 12h45 : aucun cas ne mettait un jeton dans une trace (M4 survivait).
    ⑨ CE QUI CLOCHE — Le plantage est provoqué (voir l'en-tête). ⑩ EFFET — Écrit une copie dans le monde ; lance.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    clair, nu = jetons_fictifs()
    copie = os.path.join(m.t, "progs_plantage")
    shutil.copytree(m.progs, copie)
    with open(os.path.join(copie, "LIVRER.py"), "a", encoding="utf-8") as f:
        f.write(PLANTAGE)
    m.progs, m.env["PLANTAGE_FICTIF"] = copie, clair + "\n" + nu
    code, sortie, laisses, publiques = lancer(m, "travail-x|CircuitPublic")
    e = refus(code, sortie, laisses, publiques, demandes(m, "travail-x"), r"PLANTAGE travail-x : RuntimeError", attendu=5)
    if "Traceback" not in sortie or ligne_masquee(m) not in sortie:
        e.append("trace ou ligne masquée absente : " + sortie.strip()[-300:])
    if clair in sortie:
        e.append("jeton en clair affiché")
    if nu in sortie:
        e.append("base64 nu affiché")
    return e


def cas_relais(m):
    """Le relais bash : mêmes entrées, même envoi, même code (0), une demande ajoutée.

    ① RÔLE — Les appels déjà écrits avec le .sh continuent de marcher. ② CONTEXTE D'APPEL — `jouer`.
    ③ ENTRÉE — `m`. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la liste des écarts.
      [rend: 1]
    ⑥ TRAITEMENT — « bash <progs>/ENVOYER_LES_EPREUVES_SUR_GITHUB.sh travail-x|CircuitPublic », depuis le clone.
    ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Lance. ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    r = m.lancer(["bash", os.path.join(m.progs, RELAIS), "travail-x|CircuitPublic"], m.clone)
    d, e = demandes(m, "travail-x"), []
    if r.returncode != 0 or r.stdout.count(" ENVOYÉ travail-x ") != 1:
        e.append(f"code {r.returncode} ; sortie : {(r.stdout + r.stderr).strip()[-200:]}")
    if len(d) != 1 or d[0][0] != "A":
        e.append(f"demandes : {d}")
    return e


# Ordre : les cas qui gardent une garde précise d'abord, pour que « --saboter » (arrêt au premier cas rouge) reste court.
CAS = (
    ("N nominal", cas_nominal),
    ("D2 code inconnu, vérifié avant publication", cas_refus(["travail-x|CircuitPublic,Inconnu"],
                                                             r"REFUSÉ travail-x : code\(s\) absent\(s\).*Inconnu")),
    ("D6 code en double", cas_refus(["travail-x|CircuitPublic,GardeFou,CircuitPublic"],
                                    r"(?m)REFUSÉ travail-x : code demandé deux fois : CircuitPublic — rien n'est publié$")),
    ("T table absente de la branche", cas_refus(["travail-t|CircuitPublic"],
                                                r"REFUSÉ travail-t : tests/LANCEMENT_DES_EPREUVES\.json absent de la branche",
                                                regler_table_absente, branche="travail-t")),
    ("H branche hors « travail-… »", cas_refus(["autre|CircuitPublic"], r"REFUSÉ autre : branche refusée",
                                              regler_branche_autre, branche="autre")),
    ("B64 base64 nu masqué (D-10)", cas_base64_nu),
    ("T2 trace de plantage masquée", cas_trace),
    ("D1 même minute, branche publique déjà là (D-1, D-4)", cas_meme_minute),
    ("V codes vides « br| »", cas_refus(["travail-x|"], r"REFUSÉ travail-x : entrée mal formée")),
    ("M branche main", cas_refus(["main|CircuitPublic"], r"REFUSÉ main : branche refusée")),
    ("P table illisible → plantage", cas_refus(["travail-p|CircuitPublic"], r"PLANTAGE travail-p : JSONDecodeError",
                                               regler_table_illisible, attendu=5, branche="travail-p")),
    ("R fetch refusé", cas_refus(["travail-x|CircuitPublic"], r"REFUSÉ \(toutes\) : fetch du dépôt privé refusé",
                                 regler_origin_injoignable)),
    ("J jeton masqué", cas_jeton),
    ("V2 entrée sans « | »", cas_refus(["travail-x"], r"REFUSÉ travail-x : entrée mal formée")),
    ("F fabricant qui refuse", cas_refus(["travail-x|CircuitPublic"], r"REFUSÉ travail-x : publication refusée",
                                         regler_refus_du_fabricant)),
    ("A branche absente", cas_refus(["travail-zz|CircuitPublic"], r"REFUSÉ travail-zz : origin/travail-zz introuvable",
                                    branche="travail-zz")),
    ("L branche locale en avance", cas_refus(["travail-x|CircuitPublic"], r"REFUSÉ travail-x : .*commit\(s\) absent",
                                             regler_branche_en_avance)),
    ("S copie privée superficielle", cas_refus(["travail-x|CircuitPublic"],
                                               r"REFUSÉ travail-x : essai à blanc.*SUPERFICIEL.*git fetch --unshallow",
                                               regler_superficiel)),
    ("X mêlé", cas_mele),
    ("Z aucune entrée", cas_refus([], r"REFUSÉ \(toutes\) : usage")),
    ("B nominal par le relais bash", cas_relais),
    ("D1 noms de minute tous pris (D-1)", cas_noms_pris),
)


def jouer(H, source, progs, au_premier_echec=False):
    """Joue les cas sur une copie des programmes ; rend la liste des (nom, écarts).

    ① RÔLE — Un passage. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — `H` · `source` · `progs` · `au_premier_echec` :
      s'arrêter au premier cas rouge (sabotages : un seul suffit pour dire MORD).
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la liste.
      [rend: 1]
    ⑥ TRAITEMENT — Un monde neuf par cas, fermé après ; une exception du cas compte comme écart.
    ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — Dossiers temporaires. ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    rendu = []
    for nom, cas in CAS:
        m = monde(H, source, progs)
        try:
            ecarts = cas(m)
        except Exception as e:   # noqa: BLE001 — un cas qui lève est rouge, jamais vert
            ecarts = [f"exception de l'épreuve : {type(e).__name__} : {e}"]
        finally:
            m.fermer()
        rendu.append((nom, ecarts))
        if ecarts and au_premier_echec:
            break
    return rendu


def main():
    """Joue les cas, puis les sabotages avec --saboter ; sort avec le code.

    ① RÔLE — Voir l'en-tête. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — sys.argv.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Rien : sort (0, 1, 2).
      [rend: rien]
    ⑥ TRAITEMENT — Options vérifiées (inconnue → 2, R-734) ; cas sur une copie propre ; avec --saboter, chaque
      sabotage sur sa copie, arrêt au premier cas rouge ; avant les sabotages, la copie propre doit
      être verte (sinon code 1). ⑦ UNITÉ — Secondes. ⑧ POURQUOI — R-731.
    ⑨ CE QUI CLOCHE — Voir l'en-tête. ⑩ EFFET — Dossiers temporaires. ⑪ TERMINAISON — Sort par sys.exit.
      [sort: oui]
    """
    options = [a for a in sys.argv[1:] if a.startswith("--")]
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if [o for o in options if o != "--saboter"] or len(args) > 1:
        print("ÉCHEC — option inconnue ou argument en trop · usage : [<racine>] [--saboter]")
        sys.exit(2)
    source = os.path.abspath(args[0] if args else ".")
    H = charger_le_harnais(source)
    t0, ok = time.time(), True
    base = tempfile.mkdtemp(prefix="epreuve_envoyer_")
    try:
        if "--saboter" in options:
            copier(source, os.path.join(base, "propre"))
            rouges = [n for n, ecarts in jouer(H, source, os.path.join(base, "propre")) if ecarts]
            if rouges:   # sur une copie propre déjà rouge, un sabotage « mordrait » sans rien prouver
                print("ÉCHEC — la copie PROPRE est déjà rouge (" + ", ".join(rouges) + ") : sabotages non joués")
                sys.exit(1)
            for s in SABOTAGES:
                d = os.path.join(base, re.sub(r"\W", "_", s[0])[:12])
                try:
                    copier(source, d, s)
                except ValueError as e:
                    print(f"NE MORD PAS  {s[0]} : {e}", flush=True)
                    ok = False
                    continue
                rouges = [n for n, ecarts in jouer(H, source, d, au_premier_echec=True) if ecarts]
                print((f"MORD         {s[0]} (cas rouge : {rouges[0]})" if rouges else f"NE MORD PAS  {s[0]}"), flush=True)
                ok = ok and bool(rouges)
            print("BILAN SABOTAGES : " + ("TOUS MORDENT" if ok else "AU MOINS UN NE MORD PAS")
                  + f" ({len(SABOTAGES)} sabotages)")
        else:
            copier(source, os.path.join(base, "propre"))
            for nom, ecarts in jouer(H, source, os.path.join(base, "propre")):
                print(("OK      " if not ecarts else "ÉCHEC   ") + nom + ("" if not ecarts else " : " + " ; ".join(ecarts)),
                      flush=True)
                ok = ok and not ecarts
            print(("BILAN : TOUT VERT" if ok else "BILAN : ÉCHEC") + f" ({len(CAS)} cas)")
    finally:
        shutil.rmtree(base, ignore_errors=True)
    print(f"durée : {time.time() - t0:.0f} s")   # ligne à part : le BILAN reste identique d'un passage à l'autre
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
