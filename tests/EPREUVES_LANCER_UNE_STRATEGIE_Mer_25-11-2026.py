#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_LANCER_UNE_STRATEGIE_Mer_25-11-2026.py — Mer 25-11-2026 (Paris). Simulation uniquement.

LE SENS EN TÊTE. Éprouve le LANCEUR UNIQUE, programmes/LANCER_UNE_STRATEGIE.py (A-965), en moins de deux minutes : il
enchaîne ⓪ → ① → ② → ③ → ④ par le VRAI enchaîneur (programmes/ENCHAINER_LA_MOULINETTE.py) et sa VRAIE garde
(programmes/VERIFIER_LA_CHAINE.py), sur une copie fabriquée qui porte une FICHE FACTICE (FAUX-LANCEUR-V1, essai E01) et
des cours FABRIQUÉS, tous datés de 2024 ou après ; les programmes de la moulinette de cette copie (PREPARER, DECLINER,
JOUER, TRIER, et le JUGE) sont des DOUBLURES de quelques lignes qui écrivent ce que l'enchaîneur attend. Aucun cours réel n'est lu,
aucun cours de 2000 à 2023 n'est regardé : la doublure de JOUER refuse (code 3) toute date d'avant 2024. Puis des
SABOTAGES du lanceur, de la garde (VERIFIER_LA_CHAINE.py) et de l'enchaîneur (une copie du programme, texte changé) :
chacun doit faire tomber au moins un cas ; un sabotage qui ne fait rien tomber rend l'épreuve rouge (« une épreuve qui
reste verte quand on retire ce qu'elle teste est une décoration »). Depuis le RELU Cowork du 25-11-2026 (pointe
c83732b53) : la famille se lit au CODE du module (L-1 : graphies du chemin, copie sous un autre nom), la garde vit à la
porte de ④ et tient contre l'enchaîneur appelé à la main (L-2), le découpage se lit dans le journal (L-3), la famille
est refusée avant ⓪ (L-4). Depuis le RELU Cowork du 25-11-2026 à 14h20 (pointe c5a0f4c5b) et le superviseur R-759
du même jour : la garde compte aussi la VERSION visée et le module de la fiche jugée (L-6, cas C15, C15c) ; la doublure
de JOUER lit la tranche par la vraie fonction (L-12, cas C16) ; l'enchaîneur refuse une tranche écrite avec un zéro de
tête ou hors du découpage (L-10, L-7, cas C17) ; la déclaration se lit au journal, pas au fichier seul (L-8, cas C18).
Depuis le RELU Cowork du 25-11-2026 à 15h03 et la décision de Jean-Luc du même jour à 15h09 : la VRAIE porte du juge
passe le module de la fiche jugée à la garde (N-1, cas C19, juge factice) ; « jouer 3 3 » est refusé (N-2, C17) ; la
version visée « fiche elle-même » et le module vide ont leurs cas (N-4, C20, C21) ; la référence de la famille est
FIGÉE au contrat (L-11, C13 fermés : C13, C13b) et s'auto-vérifie (C22).

USAGE
    python3 -B tests/EPREUVES_LANCER_UNE_STRATEGIE_Mer_25-11-2026.py <source> [--sans-sabotages]

① RÔLE — Prouver que le lanceur enchaîne, reprend, s'arrête sur la validation des réglages, refuse ④ pour une famille
  déjà jouée sur 2000-2023 sans déclaration (A-777, C12), juge toutes les versions retenues, et rougit quand une étape
  est sautée.
② CONTEXTE D'APPEL — À la main, ou par la certification (qui lance chaque tests/*.py avec la seule copie).
③ ENTRÉE — `<source>` : la racine d'une copie du dépôt (ses programmes/ sont éprouvés) ; `--sans-sabotages` : les cas
  seulement.
④ CONDITIONS D'ENTRÉE — `<source>/programmes/LANCER_UNE_STRATEGIE.py` existe.
⑤ SORTIE — UNE valeur, le code : 0 tout tient · 1 un cas tombe ou un sabotage ne mord pas · 2 l'épreuve n'a pas pu
  tourner (ancre de sabotage absente, usage faux — R-734).
⑥ TRAITEMENT — ① un dossier de travail sous /dev/shm (sinon /tmp) · ② les cas C1 à C22 sur les vrais programmes ·
  ③ chaque sabotage : une copie du dossier des programmes faite de liens (et emp.py lié à côté, que LIRE_LE_CODE
  cherche au-dessus de programmes/), le programme visé remplacé par son texte saboté, les cas rejoués, au moins un doit
  tomber · ④ le dossier de travail effacé.
⑦ UNITÉ — secondes.
⑧ POURQUOI — R-731 : épreuves avec sabotages ; A-965.
⑨ CE QUI CLOCHE — ① Les programmes de la moulinette sont des doublures : leur vrai comportement est éprouvé par
  tests/EPREUVES_ENCHAINER_LA_MOULINETTE_Jeu_19-11-2026.py, pas ici. ② Le contrôle « code 0 sans témoin » du lanceur
  n'a aucun cas : le vrai enchaîneur n'écrit jamais l'un sans l'autre (nommé à la passe ④). ③ La branche
  « github-non-branche » de `ou_jouer` n'est pas jouée : la table du relais ne porte pas « moulinette ». ④ La porte du
  VRAI juge n'est pas jouée (doublure) : C11b appelle `V.motifs` comme elle, avec une version visée. ⑤ La doublure de
  JOUER découpe par la VRAIE fonction `JOUER_LES_VERSIONS.tranche` de la source, et sa doublure d'assemblage refuse un
  doublon ou un manque comme la vraie (MINEUR de L-3) ; elle LIT la tranche par la VRAIE
  `JOUER_LES_VERSIONS.lire_la_tranche` (L-12). C16 n'a PAS de sabotage propre : la doublure vit dans l'épreuve, pas
  dans programmes/ (accepté par le superviseur R-759 du 25-11-2026, Q5). ⑥ L-11 et C13 FERMÉS par la décision de Jean-Luc
  du 25-11-2026 à 15h09 (« 1 » à « graver au contrat les empreintes du code de C5 ») : la référence de la famille est
  l'ensemble FIGÉ de CONTRATS.CODE_DES_FAMILLES_DEJA_JOUEES ; C13 (lignes C5E10-QA-V1 retirées) et C13b (une ligne
  C5E10-QA-V1 ajoutée sur un autre module) REFUSENT désormais, C22 prouve l'auto-vérification (code de C5 changé sous
  la racine → code 2). Les modules « C5 » de la copie fabriquée portent donc le VRAI code de C5, lu dans la source
  (jamais exécuté ici : seule son empreinte compte). ⑦ `porte_du_juge` est jouée par C19 avec un juge FACTICE
  (`porte_du_juge_factice`, ⑨ ①) : le VRAI juge ne l'est pas.
⑩ EFFET — Écrit sous le dossier de travail seulement.
⑪ TERMINAISON — Chaque lancement est borné à 120 s. [sort: oui — code]
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
SID, ESSAI, N = "FAUX-LANCEUR-V1", "E01", 3
CH = "CHAINE_%s_%s" % (SID, ESSAI)
LANCEUR = "LANCER_UNE_STRATEGIE.py"
FIN = "TERMINÉ : ⓪ ① ② ③ ④ faits"
DECL = "--famille-deja-jouee-declaree=Jean-Luc, essai factice de l'épreuve"

# LES DOUBLURES — chacune écrit ce que l'enchaîneur attend d'elle, au nom qu'il lui donne.
DOUBLURES = {
    "PREPARER_LES_VARIABLES_DE_DECLINAISON_DES_STRATEGIES.py": r'''
import os, shutil, sys
reg, sid, vois, essai, sortie = sys.argv[1:6]
nom = "VARIABLES_DE_DECLINAISON_%s_%s.csv" % (sid, essai)
shutil.copyfile(os.path.join("donnees", "combinatoires", nom), os.path.join(sortie, nom))
''',
    "DECLINER_LES_STRATEGIES.py": r'''
import csv, os, sys
reg, variables, sortie = sys.argv[1:4]
sid, essai = os.path.basename(variables)[len("VARIABLES_DE_DECLINAISON_"):-4].rsplit("_", 1)
with open(os.path.join(sortie, "COMBINATOIRE_%s_%s.csv" % (sid, essai)), "w", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["id_version", "tp", "sl", "horizon", "univers"])
    for i in range(1, 8):
        w.writerow(["%s-%s-%04d" % (sid, essai, i), 2 + i, 2, 10, "CAC40"])
''',
    "JOUER_LES_VERSIONS.py": r'''
import csv, os, sys
sys.path.insert(0, SOURCE_DES_PROGRAMMES)
from JOUER_LES_VERSIONS import tranche as decouper, lire_la_tranche   # LE découpage et SA lecture, les vraies (R-708)
def lire(p):
    with open(p, newline="") as fh:
        return list(csv.DictReader(fh))
def ecrire(p, lignes):
    with open(p, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=CHAMPS, lineterminator="\n")
        w.writeheader(); w.writerows(lignes)
CHAMPS = ["id_version", "tp", "sl", "horizon", "univers", "gain"]
if sys.argv[1] == "--assembler":
    # « --cours=… » (l'enchaîneur le passe depuis le 27-11-2026, A-1076) n'est pas une tranche
    comb, sortie, tranches = sys.argv[2], sys.argv[3], [a for a in sys.argv[4:] if not a.startswith("--")]
    toutes = [l for t in tranches for l in lire(t)]
    par_id = {l["id_version"]: l for l in toutes}
    ids = [l["id_version"] for l in lire(comb)]
    if len(par_id) != len(toutes) or set(par_id) != set(ids):
        print("doublure : assemblage refusé, version en double ou manquante"); sys.exit(1)
    ecrire(sortie, [par_id[i] for i in ids])
    sys.exit(0)
comb, sortie, tranche = sys.argv[2], sys.argv[3], sys.argv[4]
try:
    k, n = lire_la_tranche([tranche])      # refuse k >= N comme le vrai (L-12 du RELU Cowork du 25-11-2026)
except ValueError as e:
    print("doublure : %s" % e); sys.exit(2)
if os.path.exists("SABOTAGE_JOUER_%d" % k):
    print("doublure : tranche %d en échec demandé" % k); sys.exit(1)
cours = lire(os.path.join("donnees", "cours_factices_2024.csv"))
if any(c["date"] < "2024-01-01" for c in cours):
    print("doublure : date d'avant 2024 refusée"); sys.exit(3)
somme = sum(float(c["cloture"]) for c in cours)
ecrire(sortie, [dict(l, gain=round(somme * float(l["tp"]) / 1000, 2)) for l in decouper(lire(comb), k, n)])
''',
    "TRIER_LES_VARIANTES.py": r'''
import csv, sys
sortie, resultats = sys.argv[2], sys.argv[3]
with open(resultats, newline="") as fh:
    lignes = sorted(csv.DictReader(fh), key=lambda l: -float(l["gain"]))[:2]
with open(sortie, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(lignes[0]), lineterminator="\n")
    w.writeheader(); w.writerows(lignes)
''',
    "JUGE_DES_STRATEGIES.py": r'''
import os, sys
racine, ident = sys.argv[1:3]
if os.path.exists(os.path.join(racine, "SABOTAGE_JUGE")):
    print("doublure : juge en échec demandé"); sys.exit(1)
print("doublure du juge : %s jugée (aucun cours lu)" % ident)
''',
}


# LES MODULES DE SIGNAL FACTICES — du CODE (la famille se lit à l'empreinte du code, sans les textes explicatifs).
def code_de_c5():
    """Rend (chemin de référence, texte du VRAI module C5) lus dans la source. [rend: 2]

    ①–⑪ : ① la famille déjà vue de l'épreuve est C5 elle-même, depuis que sa référence est FIGÉE au contrat (L-11,
    décision de Jean-Luc du 25-11-2026 à 15h09) · ② `fabriquer` · ③ — (SOURCE_DES_PROGRAMMES) · ④ la source porte le
    contrat et le module · ⑤ DEUX valeurs · ⑥ le chemin vient de CONTRATS.CODE_DES_FAMILLES_DEJA_JOUEES de la source
    (jamais recopié, R-708), le texte du fichier de la source · ⑦ — · ⑧ le code n'est jamais exécuté : seule son
    empreinte compte · ⑨ — · ⑩ lit · ⑪ rend la main. [sort: non]
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location("contrats_de_la_source",
                                                  os.path.join(SOURCE_DES_PROGRAMMES, "CONTRATS_DES_FICHIERS.py"))
    C = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(C)
    chemin = C.CODE_DES_FAMILLES_DEJA_JOUEES["C5E10-QA-V1"][0]
    return chemin, open(os.path.join(os.path.dirname(SOURCE_DES_PROGRAMMES), chemin), encoding="utf-8").read()


MODULE_NEUF = '''"""Module factice d'une famille neuve."""
def signal(cours):
    return [c < 100 for c in cours]
'''


def fabriquer(dossier, valide=True, module="programmes/MODULE_FAUX_NEUF.py"):
    """Fabrique une racine factice ; rend son chemin. [rend: 1]

    ① RÔLE — La copie jetable : fiche factice, réglages, cours de 2024, doublures, modules de signal factices.
    ② CONTEXTE D'APPEL — chaque cas.
    ③ ENTRÉE — `dossier` (absent) ; `valide` : la mention de validation est-elle écrite ? `module` : le module de
      signal de la fiche factice, tel qu'écrit au registre (programmes/MODULE_FAUX_C5.py porte le VRAI code de C5,
      `code_de_c5`, et fait donc une famille déjà jouée ; « ./programmes/… » ou la copie MODULE_COPIE_DU_C5.py aussi).
    ④ CONDITIONS D'ENTRÉE — SOURCE_DES_PROGRAMMES est posé par `main`.
    ⑤ SORTIE — UNE valeur : le chemin. ⑥ TRAITEMENT — fichiers écrits. ⑦ UNITÉ — —
    ⑧ POURQUOI — aucun cours réel, aucune date d'avant 2024 (consigne du 25-11-2026). ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — écrit sous `dossier`. ⑪ TERMINAISON — rend la main. [sort: non]
    """
    os.makedirs(os.path.join(dossier, "donnees", "combinatoires"))
    os.makedirs(os.path.join(dossier, "programmes"))
    for nom, texte in DOUBLURES.items():
        with open(os.path.join(dossier, "programmes", nom), "w", encoding="utf-8") as fh:
            fh.write(texte.lstrip().replace("SOURCE_DES_PROGRAMMES", repr(SOURCE_DES_PROGRAMMES)))
    ref, c5 = code_de_c5()
    # Le VRAI code de C5 : au chemin de référence (l'auto-vérification le lit), sous un autre nom (MODULE_FAUX_C5.py),
    # et recopié avec un commentaire de plus (MODULE_COPIE_DU_C5.py : L-1, A1c du RELU Cowork).
    for nom, texte in ((os.path.basename(ref), c5), ("MODULE_FAUX_C5.py", c5),
                       ("MODULE_COPIE_DU_C5.py", "# un commentaire qui n'est pas du code\n" + c5),
                       ("MODULE_FAUX_NEUF.py", MODULE_NEUF)):
        with open(os.path.join(dossier, "programmes", nom), "w", encoding="utf-8") as fh:
            fh.write(texte)
    with open(os.path.join(dossier, "donnees", "cac40_strategies.csv"), "w", encoding="utf-8") as fh:
        fh.write("id,tp,sl,horizon,univers,etat_vie,statut,origine,module_signal\n")
        fh.write("C5E10-QA-V1,4,2,10,CAC40,LABO,fiche factice,,programmes/MODULE_FAUX_C5.py\n")
        fh.write("%s,4,2,10,CAC40,LABO,fiche factice de l'épreuve,,%s\n" % (SID, module))
    mention = "Jean-Luc le 25-11-2026" if valide else "à valider"
    with open(os.path.join(dossier, "donnees", "combinatoires",
                           "VARIABLES_DE_DECLINAISON_%s_%s.csv" % (SID, ESSAI)), "w", encoding="utf-8") as fh:
        fh.write("strategie,essai,parametre,valeur_fiche,valeurs_a_essayer,unite,jouable,raison,valide_par,prepare_le\n")
        for p, v in (("tp", "3;4;5"), ("sl", "2"), ("horizon", "10"), ("univers", "CAC40")):
            fh.write("%s,%s,%s,x,%s,u,OUI,factice,%s,2026-11-25 12h00 Paris\n" % (SID, ESSAI, p, v, mention))
    with open(os.path.join(dossier, "donnees", "cours_factices_2024.csv"), "w", encoding="utf-8") as fh:
        fh.write("date,cloture\n")
        for j in range(1, 21):
            fh.write("2024-03-%02d,%d\n" % (j, 100 + j))
    return dossier


def lancer(prog, racine, *opts):
    """Lance le lanceur ; rend (code, sortie). Borné à 120 s. [rend: 2]

    ①–⑪ : ① lancer · ② chaque cas · ③ `prog` : chemin du lanceur, `racine`, options · ④ — · ⑤ DEUX valeurs ·
    ⑥ subprocess · ⑦ secondes · ⑧ — · ⑨ — · ⑩ le lanceur écrit sous la racine · ⑪ borné. [sort: non]
    """
    p = subprocess.run([sys.executable, "-B", prog, racine, SID, ESSAI] + list(opts), capture_output=True, text=True,
                       timeout=120)
    return p.returncode, p.stdout + p.stderr


def ench(prog, racine, *args):
    """Lance l'enchaîneur À LA MAIN, sans le lanceur ; rend (code, sortie). Borné à 120 s. [rend: 2]

    ①–⑪ : ① l'enchaîneur voisin du lanceur `prog` · ② C11, C12 · ③ `racine`, l'étape et ses arguments · ④ — ·
    ⑤ DEUX valeurs · ⑥ subprocess · ⑦ secondes · ⑧ L-2, L-3 : un chemin vers ④ qui ne passe pas par le lanceur ·
    ⑨ — · ⑩ l'enchaîneur écrit sous la racine · ⑪ borné. [sort: non]
    """
    p = subprocess.run([sys.executable, "-B", os.path.join(os.path.dirname(prog), "ENCHAINER_LA_MOULINETTE.py"),
                        racine, SID, ESSAI] + list(args), capture_output=True, text=True, timeout=120, cwd=racine)
    return p.returncode, p.stdout + p.stderr


def motifs_de_la_porte(prog, racine, version, module=None):
    """Rend la sortie de `V.motifs` (chaîne complète, version visée), comme la porte du juge l'appelle. [rend: 1]

    ①–⑪ : ① C11b, C15, C15c · ② `les_cas` · ③ `prog` : le lanceur (la garde est sa voisine), `racine`, `version`,
    `module` : le module de la fiche jugée, comme la porte le passe (None : non passé) · ④ — ·
    ⑤ UNE valeur : le texte affiché · ⑥ un python neuf importe VERIFIER_LA_CHAINE voisin et affiche les motifs ·
    ⑦ — · ⑧ L-2 : la garde vit dans `motifs`, que la porte du juge appelle aussi · ⑨ — · ⑩ lit · ⑪ borné. [sort: non]
    """
    code = ("import sys; sys.path.insert(0, %r); import VERIFIER_LA_CHAINE as V; "
            "print(V.motifs(%r, %r, %r, len(V.ORDRE), %r, module=%r))" % (os.path.dirname(prog), racine, SID, ESSAI,
                                                                           version, module))
    p = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True, timeout=120, cwd=racine)
    return p.stdout + p.stderr


def porte_du_juge_factice(prog, racine, version, module):
    """Rend la sortie de la VRAIE `V.porte_du_juge`, appelée avec un juge factice ; rend le texte affiché. [rend: 1]

    ① RÔLE — C19 : faire passer un cas par la ligne de `porte_du_juge` qui donne à la garde le module de la fiche jugée
      (Q4 du superviseur R-759 du 25-11-2026), que C15c ne traverse pas (N-1 du RELU Cowork du 25-11-2026, 14h58).
    ② CONTEXTE D'APPEL — `les_cas`, C19.
    ③ ENTRÉE — `prog` : le lanceur (la garde est sa voisine) ; `racine` : une copie fabriquée dont la chaîne est faite
      jusqu'à ③ ; `version` : l'identifiant de la fiche jugée, ABSENT du registre de la copie (la branche « version
      visée », L-6, ne voit donc rien : seul le module passé par la porte peut refuser) ; `module` : sa case
      module_signal. Exemple : version FAUX-LANCEUR-V1-E01-0007, module programmes/MODULE_FAUX_C5.py.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte affiché (la liste des motifs, ou la trace d'une exception).
    ⑥ TRAITEMENT — un python neuf importe la garde voisine, puis NEUTRALISE ce que la copie fabriquée ne porte pas :
      le juge est un espace de noms factice (lecture des modules : la VRAIE `lire_module_du_jour` ; empreinte des
      réglages et nom du barème : des constantes) ; `JOUER_LES_VERSIONS.empreinte_du_bareme` et
      `CONTRATS_DES_FICHIERS.manques_du_contrat` : des constantes ; `V.motifs` est enveloppée pour recevoir
      empreinte=None et bareme=None (la doublure de ② n'écrit pas ces colonnes) — TOUT LE RESTE, dont l'argument
      `module`, est passé tel que `porte_du_juge` l'a écrit. Puis `V.porte_du_juge(racine, fiche, J=…, mod_pos=…)`
      sur une fiche marquée « MOULINETTE (A-919) <SID> <ESSAI> ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-731 : une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration ; le RELU de
      14h58 (mutation M2) a retiré l'argument `module` de la porte sans qu'aucun cas ne tombe.
    ⑨ CE QUI CLOCHE — ① le VRAI juge n'est pas joué : son empreinte des réglages, son barème et le contrat sont
      neutralisés ; ce cas ne prouve QUE le passage du module par la porte à la garde. ② Le texte des neutralisations
      suppose les noms `empreinte_des_reglages`, `lire_module_du_jour`, `bareme_des_verdicts`, `empreinte_du_bareme`,
      `manques_du_contrat` : un renommage fait tomber C19 en trace (rouge), pas en vert.
    ⑩ EFFET — lit.
    ⑪ TERMINAISON — bornée à 120 s. [sort: non]
    """
    code = "\n".join([
        "import sys, types",
        "sys.path.insert(0, %r)" % os.path.dirname(prog),
        "import VERIFIER_LA_CHAINE as V, JOUER_LES_VERSIONS as JOUER, CONTRATS_DES_FICHIERS as C",
        "import JUGE_DES_STRATEGIES as VRAI",
        "J = types.SimpleNamespace(lire_module_du_jour=VRAI.lire_module_du_jour,",
        "                          empreinte_des_reglages=lambda f, l: ('neutralisee',),",
        "                          bareme_des_verdicts=lambda *a: 'bareme-factice')",
        "JOUER.empreinte_du_bareme = lambda *a: 'neutralisee'",
        "C.manques_du_contrat = lambda *a, **k: []",
        "vrai = V.motifs",
        "import inspect",
        "def enveloppe(*a, **k):",
        "    b = inspect.signature(vrai).bind(*a, **k)",
        "    b.arguments['empreinte'], b.arguments['bareme'] = None, None",
        "    return vrai(*b.args, **b.kwargs)",
        "V.motifs = enveloppe",
        "fiche = {'id': %r, C.COLONNE_DE_LA_MARQUE_DE_MOULINETTE: C.MARQUE_DE_MOULINETTE + ' %s %s', "
        "'module_signal': %r}" % (version, SID, ESSAI, module),
        "print(V.porte_du_juge(%r, fiche, J=J, mod_pos=object()))" % racine,
    ])
    p = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True, timeout=120, cwd=racine)
    return p.stdout + p.stderr


def famille_directe(prog, racine, version, module=None):
    """Rend la sortie de `V.famille_deja_jouee(racine, SID, None, version, module)`. [rend: 1]

    ①–⑪ : ① C20 · ② `les_cas` · ③ `prog` : le lanceur (la garde est sa voisine), `racine`, `version`, `module` · ④ — ·
    ⑤ UNE valeur : le texte affiché · ⑥ un python neuf importe VERIFIER_LA_CHAINE voisin et affiche le résultat, ou la
      trace d'une exception · ⑦ — · ⑧ N-4 du RELU Cowork du 25-11-2026 : la branche « version visée = la fiche déjà vue
      elle-même » n'est atteinte par aucun cas passant par `motifs` (une version hors du tri ③ y est refusée avant) ·
      ⑨ — · ⑩ lit · ⑪ bornée à 120 s. [sort: non]
    """
    code = ("import sys; sys.path.insert(0, %r); import VERIFIER_LA_CHAINE as V; "
            "print(V.famille_deja_jouee(%r, %r, None, %r, %r))" % (os.path.dirname(prog), racine, SID, version, module))
    p = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True, timeout=120, cwd=racine)
    return p.stdout + p.stderr


def etat(racine):
    """Rend l'état du lanceur, ou {} s'il est absent. [rend: 1] ①–⑪ : lecture seule, rend la main. [sort: non]"""
    p = os.path.join(racine, CH, "ETAT_DU_LANCEUR.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def journal(racine):
    """Rend l'ensemble des étapes témoignées. [rend: 1] ①–⑪ : lecture seule, rend la main. [sort: non]"""
    p = os.path.join(racine, CH, "JOURNAL_DE_LA_CHAINE.csv")
    return {l.split(",")[0] for l in open(p, encoding="utf-8").read().splitlines()[1:]} if os.path.exists(p) else set()


def sha(p):
    """Empreinte sha256 d'un fichier. [rend: 1] ①–⑪ : lecture seule, rend la main. [sort: non]"""
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def refuse_avant_zero(code, out, racine):
    """Vrai si le lanceur a refusé la famille AVANT ⓪ : code 1, la décision citée, aucun témoin. [rend: 1]
    ①–⑪ : lecture seule, rend la main. [sort: non]"""
    m = etat(racine).get("message", "")
    return code == 1 and "REFUS ④ avant ⓪" in out and "A-777" in m and "C12" in m and not journal(racine)


def les_cas(prog, travail):
    """Joue les cas ; rend la liste (nom, vrai/faux, détail). [rend: 1]

    ① RÔLE — Les cas. ② CONTEXTE D'APPEL — `main`, une fois pour les vrais programmes, une fois par sabotage.
    ③ ENTRÉE — `prog` : le lanceur (l'enchaîneur et la garde sont ses voisins) ; `travail` : un dossier vide.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE liste de triplets. ⑥ TRAITEMENT — voir chaque cas. ⑦ UNITÉ — —
    ⑧ POURQUOI — A-965 : enchaîner, reprendre, s'arrêter sur Jean-Luc, rougir sur une étape sautée ; L-1 à L-4.
    ⑨ CE QUI CLOCHE — voir ⑨ de l'en-tête. ⑩ EFFET — écrit sous `travail`. ⑪ TERMINAISON — rend la main. [sort: non]
    """
    r = []
    # C1 — passage complet ⓪→④, deux versions jugées, registre augmenté, état complet, aucune déclaration (famille neuve).
    a = fabriquer(os.path.join(travail, "c1"))
    reg = sha(os.path.join(a, "donnees", "cac40_strategies.csv"))
    code, out = lancer(prog, a, "--tranches=%d" % N)
    e, j = etat(a), journal(a)
    # « 0-cours-de-la-chaine » : les cours fixés à ⓪ par l'enchaîneur (A-1076, lot L1 du 27-11-2026)
    attendu = {"0-variables-validees", "0-proposition", "0-cours-de-la-chaine", "1-decliner", "2-assembler",
               "3-trier"} | {"2-tranche-%d" % k for k in range(N)}
    juges = {"4-juger-%s-%s-%04d" % (SID, ESSAI, i) for i in (7, 6)}   # la doublure de TRIER garde les 2 meilleures
    ok = code == 0 and FIN in out and e.get("statut") == "TERMINÉ" and e.get("message", "").startswith(FIN) \
        and j == attendu | juges and sha(os.path.join(a, "donnees", "cac40_strategies.csv")) != reg \
        and len(e.get("etapes", [])) == N + 6 \
        and e.get("ou_jouer", {}).get("ou") == "local" and "relais" in e.get("ou_jouer", {}).get("raison", "")
    r.append(("C1 passage complet ⓪→④, deux versions jugées", ok, "code %d, %d étapes, témoins %d" %
              (code, len(e.get("etapes", [])), len(j))))
    # C2 — reprise d'une chaîne finie : rien n'est relancé, même arrêt.
    code, out = lancer(prog, a, "--tranches=%d" % N)
    ok = code == 0 and FIN in out and len(etat(a).get("etapes", [])) == N + 6
    r.append(("C2 reprise : aucune étape relancée", ok, "code %d" % code))
    # C3 — réglages non validés : arrêt code 3 AVANT ⓪, rien de figé.
    b = fabriquer(os.path.join(travail, "c3"), valide=False)
    code, out = lancer(prog, b, "--tranches=%d" % N)
    ok = code == 3 and "validation des réglages" in out and not journal(b) and \
        not os.path.exists(os.path.join(b, CH, "e0")) and etat(b).get("statut") == "ATTEND JEAN-LUC"
    r.append(("C3 réglages non validés : arrêt avant ⓪", ok, "code %d" % code))
    # C4 — la tranche 1 échoue : ÉCHEC code 1, assembler non fait ; C4b : sabotage retiré, la reprise finit sans
    # rejouer la tranche 0.
    c = fabriquer(os.path.join(travail, "c4"))
    open(os.path.join(c, "SABOTAGE_JOUER_1"), "w").close()
    code, out = lancer(prog, c, "--tranches=%d" % N)
    e, j = etat(c), journal(c)
    ok = code == 1 and e.get("statut") == "ÉCHEC" and "a rendu le code 1" in e.get("message", "") and \
        "2-assembler" not in j and "2-tranche-0" in j and "2-tranche-1" not in j
    r.append(("C4 une tranche échoue : ÉCHEC, rien après", ok, "code %d" % code))
    os.remove(os.path.join(c, "SABOTAGE_JOUER_1"))
    code, out = lancer(prog, c, "--tranches=%d" % N)
    jouees0 = [x for x in etat(c).get("etapes", []) if x["etape"] == "jouer" and x["arguments"][0] == "0"]
    ok = code == 0 and FIN in out and len(jouees0) == 1 and "3-trier" in journal(c)
    r.append(("C4b reprise après échec : tranche 0 non rejouée", ok, "code %d, tranche 0 jouée %d fois" %
              (code, len(jouees0))))
    # C5 — reprise d'une chaîne finie, avec un autre découpage, fichier d'état présent : refus code 1.
    code, out = lancer(prog, a, "--tranches=%d" % (N + 1))
    r.append(("C5 autre nombre de tranches : refus", code == 1 and "mêlerait" in out, "code %d" % code))
    # C6 — racine portant .git : code 2, rien écrit.
    d = fabriquer(os.path.join(travail, "c6"))
    os.makedirs(os.path.join(d, ".git"))
    code, out = lancer(prog, d, "--tranches=%d" % N)
    r.append(("C6 racine avec .git : code 2", code == 2 and not os.path.exists(os.path.join(d, CH)), "code %d" % code))
    # C7 — usage faux : code 2.
    code, out = lancer(prog, a, "--tranches=0")
    r.append(("C7 --tranches=0 : code 2", code == 2, "code %d" % code))
    # C8 — famille déjà jouée (même module que C5E10-QA-V1) : refus AVANT ⓪ (L-4), la décision citée, rien de calculé.
    f = fabriquer(os.path.join(travail, "c8"), module="programmes/MODULE_FAUX_C5.py")
    code, out = lancer(prog, f, "--tranches=%d" % N)
    r.append(("C8 famille déjà jouée sans déclaration : refus avant ⓪", refuse_avant_zero(code, out, f),
              "code %d, témoins %d" % (code, len(journal(f)))))
    # C8b — la même, reprise avec une déclaration explicite : écrite au journal par l'enchaîneur, ④ fait.
    code, out = lancer(prog, f, "--tranches=%d" % N, DECL)
    e, j = etat(f), journal(f)
    ok = code == 0 and FIN in out and "0-famille-declaree" in j and any(x.startswith("4-juger") for x in j) and \
        e.get("famille_deja_jouee_declaree", {}).get("declaration") == DECL.split("=", 1)[1]
    r.append(("C8b la même avec déclaration : au journal, ④ fait", ok, "code %d" % code))
    # C8c — L-1 : la même famille, chemin écrit « ./programmes/… » puis « programmes/./… » : refus avant ⓪.
    oks = []
    for i, graphie in enumerate(("./programmes/MODULE_FAUX_C5.py", "programmes/./MODULE_FAUX_C5.py")):
        g = fabriquer(os.path.join(travail, "c8c%d" % i), module=graphie)
        code, out = lancer(prog, g, "--tranches=%d" % N)
        oks.append(refuse_avant_zero(code, out, g))
    r.append(("C8c graphies du chemin (L-1) : refus avant ⓪", all(oks), "%s" % oks))
    # C8d — L-1 : une COPIE du code C5 sous un autre nom, texte explicatif et commentaire changés : refus avant ⓪.
    g = fabriquer(os.path.join(travail, "c8d"), module="programmes/MODULE_COPIE_DU_C5.py")
    code, out = lancer(prog, g, "--tranches=%d" % N)
    r.append(("C8d copie du code sous un autre nom (L-1) : refus avant ⓪", refuse_avant_zero(code, out, g),
              "code %d" % code))
    # C8e — famille neuve avec une déclaration inutile : rien n'est écrit au journal, ④ fait.
    g = fabriquer(os.path.join(travail, "c8e"))
    code, out = lancer(prog, g, "--tranches=%d" % N, DECL)
    ok = code == 0 and FIN in out and "0-famille-declaree" not in journal(g) and \
        "famille_deja_jouee_declaree" not in etat(g)
    r.append(("C8e famille neuve, déclaration inutile : non écrite", ok, "code %d" % code))
    # C9 — module de signal vide : la famille est inconnue, code 2, rien de lancé.
    g = fabriquer(os.path.join(travail, "c9"), module="")
    code, out = lancer(prog, g, "--tranches=%d" % N)
    ok = code == 2 and not journal(g)
    r.append(("C9 famille inconnue : code 2", ok, "code %d" % code))
    # C10 — le juge échoue : ÉCHEC code 1.
    h = fabriquer(os.path.join(travail, "c10"))
    open(os.path.join(h, "SABOTAGE_JUGE"), "w").close()
    code, out = lancer(prog, h, "--tranches=%d" % N)
    ok = code == 1 and etat(h).get("statut") == "ÉCHEC" and not any(x.startswith("4-juger") for x in journal(h))
    r.append(("C10 le juge échoue : ÉCHEC", ok, "code %d" % code))
    # C11 — L-2 : famille C5, chaîne faite À LA MAIN par l'enchaîneur, SANS le lanceur : juger refusé (code 1, la
    # décision citée) ; C11b : `V.motifs` avec une version visée — l'appel de la porte du juge — refuse aussi ;
    # C11c : après « declarer », juger passe.
    k = fabriquer(os.path.join(travail, "c11"), module="programmes/MODULE_FAUX_C5.py")
    codes = [ench(prog, k, *x)[0] for x in (["preparer"], ["decliner"], ["jouer", "0", "1"], ["assembler"], ["trier"])]
    version = "%s-%s-0007" % (SID, ESSAI)
    code, out = ench(prog, k, "juger", version)
    ok = codes == [0] * 5 and code == 1 and "REFUS ④" in out and "C12" in out and \
        not any(x.startswith("4-juger") for x in journal(k))
    r.append(("C11 enchaîneur à la main, famille C5 : juger refusé (L-2)", ok, "codes %s puis %d" % (codes, code)))
    porte = motifs_de_la_porte(prog, k, version)
    r.append(("C11b V.motifs, version visée (porte du juge) : refus", "REFUS ④" in porte and "A-777" in porte,
              porte.strip()[2:100]))
    c1, o1 = ench(prog, k, "declarer", "Jean-Luc, essai factice de l'épreuve C11")
    code, out = ench(prog, k, "juger", version)
    ok = c1 == 0 and code == 0 and "4-juger-%s" % version in journal(k) and "[]" in motifs_de_la_porte(prog, k, version)
    r.append(("C11c après declarer : juger passe", ok, "declarer %d, juger %d" % (c1, code)))
    # C12 — L-3 : chaîne commencée À LA MAIN en 3 tranches, sans fichier d'état ; le lanceur en 5 : refus, rien joué ;
    # C12b : l'enchaîneur « jouer 3 5 » à la main : refus ; C12c : le lanceur en 3 finit la même chaîne.
    m = fabriquer(os.path.join(travail, "c12"))
    codes = [ench(prog, m, *x)[0] for x in (["preparer"], ["decliner"], ["jouer", "0", "3"], ["jouer", "1", "3"],
                                            ["jouer", "2", "3"])]
    code, out = lancer(prog, m, "--tranches=5")
    j = journal(m)
    ok = codes == [0] * 5 and code == 1 and "mêlerait" in out and "2-tranche-3" not in j and "2-assembler" not in j
    r.append(("C12 trois tranches à la main, lanceur en 5 : refus (L-3)", ok, "codes %s puis %d" % (codes, code)))
    code, out = ench(prog, m, "jouer", "3", "5")
    r.append(("C12b enchaîneur « jouer 3 5 » après 3 tranches en 3 : refus", code == 1 and "découpage" in out and
              "2-tranche-3" not in journal(m), "code %d" % code))
    code, out = lancer(prog, m, "--tranches=3")
    r.append(("C12c le lanceur dans le même découpage finit", code == 0 and FIN in out, "code %d" % code))
    # C13 — L-11 et C13 du RELU Cowork du 25-11-2026, FERMÉS par la décision de Jean-Luc du 25-11-2026 à 15h09 : la
    # fiche déjà vue retirée du registre de la copie, la famille C5 est TOUJOURS vue (référence figée au contrat) :
    # refus avant ⓪. Sous l'ancien code (référence lue au registre), ce cas passait (code 0).
    q = fabriquer(os.path.join(travail, "c13"), module="programmes/MODULE_FAUX_C5.py")
    reg = os.path.join(q, "donnees", "cac40_strategies.csv")
    lignes = open(reg, encoding="utf-8").read().splitlines()
    open(reg, "w", encoding="utf-8").write("\n".join(l for l in lignes if not l.startswith("C5E10-QA-V1,")) + "\n")
    code, out = lancer(prog, q, "--tranches=%d" % N)
    r.append(("C13 fiche déjà vue retirée du registre : C5 refusée avant ⓪ (L-11 fermé)", refuse_avant_zero(code, out, q),
              "code %d" % code))
    # C13b — le cas X3 du RELU Cowork de 15h03 : une ligne C5E10-QA-V1 AJOUTÉE sur le module neuf (la dernière ligne
    # faisait foi) ; refus avant ⓪ quand même.
    q = fabriquer(os.path.join(travail, "c13b"), module="programmes/MODULE_FAUX_C5.py")
    with open(os.path.join(q, "donnees", "cac40_strategies.csv"), "a", encoding="utf-8") as fh:
        fh.write("C5E10-QA-V1,4,2,10,CAC40,LABO,ligne ajoutée (X3),,programmes/MODULE_FAUX_NEUF.py\n")
    code, out = lancer(prog, q, "--tranches=%d" % N)
    r.append(("C13b ligne C5E10-QA-V1 ajoutée sur un autre module : C5 refusée avant ⓪ (L-11 fermé)",
              refuse_avant_zero(code, out, q), "code %d" % code))
    # C22 — AUTO-VÉRIFICATION (A-957) : le code du module de référence de C5 changé sous la racine (une instruction
    # ajoutée), empreinte absente de l'ensemble figé : contrôle impossible, code 2, rien de lancé — même pour une
    # famille neuve, pour forcer à refiger.
    q = fabriquer(os.path.join(travail, "c22"))
    ref = os.path.join(q, code_de_c5()[0])
    with open(ref, "a", encoding="utf-8") as fh:
        fh.write("\n_INSTRUCTION_AJOUTEE_PAR_L_EPREUVE = 1\n")
    code, out = lancer(prog, q, "--tranches=%d" % N)
    r.append(("C22 code de C5 changé sous la racine, hors de l'ensemble figé : code 2 (A-957)",
              code == 2 and "A-957" in out and not journal(q), "code %d" % code))
    # C15 — L-6 : stratégie sur un module NEUF, chaîne faite à la main jusqu'à ③ ; puis une ligne de VERSION ajoutée
    # sur le module C5 : la garde (`V.motifs`, version visée) refuse. C15c : sans ligne de version, le module C5 passé
    # comme la porte du juge passe celui de la fiche jugée : refus aussi (Q4 du superviseur R-759 du 25-11-2026).
    q = fabriquer(os.path.join(travail, "c15"))
    codes = [ench(prog, q, *x)[0] for x in (["preparer"], ["decliner"], ["jouer", "0", "1"], ["assembler"], ["trier"])]
    version = "%s-%s-0007" % (SID, ESSAI)
    sans = motifs_de_la_porte(prog, q, version, "programmes/MODULE_FAUX_C5.py")
    neuf = motifs_de_la_porte(prog, q, version, "programmes/MODULE_FAUX_NEUF.py")
    r.append(("C15c module de la fiche jugée sur C5 (Q4) : refus ; sur un module neuf : rien", codes == [0] * 5 and
              "REFUS ④" in sans and neuf.strip() == "[]", "codes %s, porte %s" % (codes, sans.strip()[:60])))
    with open(os.path.join(q, "donnees", "cac40_strategies.csv"), "a", encoding="utf-8") as fh:
        fh.write("%s,4,2,10,CAC40,LABO,version sur le module C5 (L-6),,programmes/MODULE_FAUX_C5.py\n" % version)
    porte = motifs_de_la_porte(prog, q, version)
    r.append(("C15 version visée sur le module C5 (L-6) : refus", "REFUS ④" in porte, porte.strip()[:80]))
    # C16 — L-12 : la doublure de JOUER refuse k >= N, comme le vrai (`lire_la_tranche`). Sans sabotage propre (⑨ ⑤).
    q = fabriquer(os.path.join(travail, "c16"))
    p = subprocess.run([sys.executable, "-B", os.path.join(q, "programmes", "JOUER_LES_VERSIONS.py"), ".", "x", "y",
                        "--tranche=5/3"], capture_output=True, text=True, timeout=120, cwd=q)
    r.append(("C16 doublure de JOUER, --tranche=5/3 : refus comme le vrai (L-12)", p.returncode == 2,
              "code %d" % p.returncode))
    # C17 — L-10, L-7 : « jouer 00 3 », « jouer 5 3 » et « jouer 3 3 » (la borne exacte k < N, N-2 du RELU Cowork de
    # 14h58) refusés par l'enchaîneur (usage, code 2), aucun témoin écrit.
    q = fabriquer(os.path.join(travail, "c17"))
    codes = [ench(prog, q, *x)[0] for x in (["preparer"], ["decliner"], ["jouer", "0", "3"], ["jouer", "00", "3"],
                                            ["jouer", "5", "3"], ["jouer", "3", "3"])]
    j = journal(q)
    r.append(("C17 « jouer 00 3 », « jouer 5 3 » et « jouer 3 3 » refusés (L-10, L-7)", codes == [0, 0, 0, 2, 2, 2] and
              "2-tranche-00" not in j and "2-tranche-5" not in j and "2-tranche-3" not in j, "codes %s" % codes))
    # C18 — L-8 : famille C5, chaîne faite à la main jusqu'à ③, le FICHIER de déclaration écrit à la main SANS témoin
    # au journal : juger refusé (la garde lit le journal, pas le fichier).
    q = fabriquer(os.path.join(travail, "c18"), module="programmes/MODULE_FAUX_C5.py")
    codes = [ench(prog, q, *x)[0] for x in (["preparer"], ["decliner"], ["jouer", "0", "1"], ["assembler"], ["trier"])]
    with open(os.path.join(q, CH, "famille_declaree.txt"), "w", encoding="utf-8") as fh:
        fh.write("écrite à la main, sans témoin au journal\n")
    code, out = ench(prog, q, "juger", "%s-%s-0007" % (SID, ESSAI))
    r.append(("C18 fichier de déclaration sans témoin au journal (L-8) : juger refusé", codes == [0] * 5 and
              code == 1 and "REFUS ④" in out, "codes %s puis %d" % (codes, code)))
    # C19 — N-1 du RELU Cowork du 25-11-2026 (14h58) : la VRAIE `porte_du_juge` (juge factice, ⑨ ① de
    # `porte_du_juge_factice`), stratégie sur un module NEUF, chaîne faite à la main jusqu'à ③, fiche jugée ABSENTE du
    # registre (la version visée ne voit rien) : sa case module_signal sur C5 → refus ; sur le module neuf → rien.
    # Seule la ligne Q4 de la porte peut faire ce refus.
    q = fabriquer(os.path.join(travail, "c19"))
    codes = [ench(prog, q, *x)[0] for x in (["preparer"], ["decliner"], ["jouer", "0", "1"], ["assembler"], ["trier"])]
    version = "%s-%s-0007" % (SID, ESSAI)
    c5 = porte_du_juge_factice(prog, q, version, "programmes/MODULE_FAUX_C5.py")
    neuf = porte_du_juge_factice(prog, q, version, "programmes/MODULE_FAUX_NEUF.py")
    r.append(("C19 porte_du_juge, fiche jugée sur C5 hors registre (Q4, N-1) : refus ; module neuf : rien",
              codes == [0] * 5 and "REFUS ④" in c5 and "A-777" in c5 and neuf.strip() == "[]",
              "codes %s, porte %s | %s" % (codes, c5.strip()[:60], neuf.strip()[:40])))
    # C21 — N-4 (M4) : module de la fiche jugée vide ou blanc → contrôle impossible, jamais accepté en silence.
    vides = [motifs_de_la_porte(prog, q, version, m) for m in ("", "   ")]
    r.append(("C21 module de la fiche jugée vide ou blanc (N-4) : contrôle impossible",
              all("Impossible" in v and "famille de la fiche jugée inconnue" in v for v in vides),
              "%d sur 2 : « famille de la fiche jugée inconnue »" % sum("famille de la fiche jugée inconnue" in v
                                                                        for v in vides)))
    # C20 — N-4 (M3) : la version visée EST la fiche déjà vue, absente du registre de la copie : « c'est la fiche
    # elle-même » — la seule branche qui la voit, puisque l'absente du registre n'est pas comparée (⑨ ④ de la garde).
    q = fabriquer(os.path.join(travail, "c20"))
    reg = os.path.join(q, "donnees", "cac40_strategies.csv")
    lignes = open(reg, encoding="utf-8").read().splitlines()
    open(reg, "w", encoding="utf-8").write("\n".join(l for l in lignes if not l.startswith("C5E10-QA-V1,")) + "\n")
    out = famille_directe(prog, q, "C5E10-QA-V1")
    r.append(("C20 version visée = la fiche déjà vue, hors registre (N-4) : « c'est la fiche elle-même »",
              "C5E10-QA-V1 : c'est la fiche elle-même" in out, out.strip()[:80]))
    return r


# LES SABOTAGES — (nom, ce qui est retiré, programme visé, texte d'origine, texte saboté). Chacun doit faire tomber au
# moins un cas.
L, V, EN = "LANCER_UNE_STRATEGIE.py", "VERIFIER_LA_CHAINE.py", "ENCHAINER_LA_MOULINETTE.py"
SABOTAGES = [
    ("S1", "étape ① sautée", L,
     '    tout = [("preparer", (), E.FAITE["preparer"]), ("decliner", (), E.FAITE["decliner"])]',
     '    tout = [("preparer", (), E.FAITE["preparer"])]'),
    ("S2", "validation des réglages non vérifiée", L,
     "    if not os.path.exists(chemin):\n        return [",
     "    return []\n    if not os.path.exists(chemin):\n        return ["),
    ("S3", "état jamais écrit", L,
     "    os.replace(tmp, os.path.join(ch, ETAT))",
     "    os.remove(tmp)"),
    ("S4", "④ sauté", L,
     "    return juger_les_retenues(racine, sid, essai, ch, etat)",
     "    return 0"),
    ("S5", "code de l'enchaîneur ignoré", L,
     "        if code != 0:\n            ecrire_l_etat(ch, etat, \"ÉCHEC\", \"étape", "        if False:\n            ecrire_l_etat(ch, etat, \"ÉCHEC\", \"étape"),
    ("S6", "étapes déjà témoignées relancées", L,
     "    return [x for x in tout if x[2] not in t]", "    return tout"),
    ("S7", "découpage non comparé par le lanceur (L-3)", L,
     "    mele = V.decoupage_mele(ch, n)", "    mele = []"),
    ("S7e", "découpage non comparé par l'enchaîneur (L-3)", EN,
     "            m += V.decoupage_mele(V.dossier(racine, sid, essai), int(args[1]))", "            pass"),
    ("S7v", "découpage : la garde ne compare plus rien (L-3)", V,
     "    if not faites:\n        return []", "    if True:\n        return []"),
    ("S8", ".git non refusé", L,
     ' or os.path.lexists(os.path.join(racine, ".git")):', ":"),
    ("S9", "famille non lue avant ⓪ (L-4)", L,
     "        deja = V.famille_deja_jouee(racine, sid)", "        deja = []"),
    ("S10", "déclaration du lanceur ignorée", L,
     "        if deja and not declaration:", "        if deja:"),
    ("S11", "seule la première version retenue jugée", L,
     "    for ident in retenues:", "    for ident in retenues[:1]:"),
    ("S12", "échec du juge ignoré", L,
     "        if code != 0 or temoin not in V.temoins(ch):", "        if False:"),
    ("S13", "famille vue au TEXTE du chemin, pas au code (L-1)", V,
     "        touches = sorted(e for e in mien if e in ensemble)",
     "        touches = sorted(e for e, ch in mien.items() if ch == chemin_ref)"),
    ("S14", "garde de famille retirée de la porte de ④ (L-2)", V,
     "        m += garde_de_famille(racine, sid, essai, version=version, module=module)", "        pass"),
    ("S15", "déclaration au journal ignorée par la garde", V,
     "    if TEMOIN_DE_FAMILLE in temoins(dossier(racine, sid, essai)):\n        return []\n",
     ""),
    ("S17", "version visée ignorée par la garde (L-6)", V,
     "    deja = famille_deja_jouee(racine, sid, J, version, module)",
     "    deja = famille_deja_jouee(racine, sid, J, None, module)"),
    ("S18", "module de la fiche jugée ignoré par la garde (Q4)", V,
     "    deja = famille_deja_jouee(racine, sid, J, version, module)",
     "    deja = famille_deja_jouee(racine, sid, J, version, None)"),
    ("S19a", "tranche écrite avec un zéro de tête acceptée (L-10)", EN,
     "a.isascii() and a.isdigit() and a == str(int(a)) for a in argv[5:]",
     "a.isascii() and a.isdigit() for a in argv[5:]"),
    ("S19b", "tranche hors du découpage acceptée, k >= N (L-7)", EN,
     "0 <= int(argv[5]) < int(argv[6])", "int(argv[6]) >= 1"),
    ("S20", "la garde croit le fichier de déclaration, pas le journal (L-8, SC1 du RELU de 14h12)", V,
     "    if TEMOIN_DE_FAMILLE in temoins(dossier(racine, sid, essai)):\n        return []\n    deja",
     "    if os.path.exists(os.path.join(dossier(racine, sid, essai), FICHIER_DE_FAMILLE)):\n        return []\n    deja"),
    ("S24", "ensemble figé vidé (L-11)", V,
     "        chemin_ref, ensemble = C.CODE_DES_FAMILLES_DEJA_JOUEES[f]",
     "        chemin_ref, ensemble = C.CODE_DES_FAMILLES_DEJA_JOUEES[f][0], frozenset()"),
    ("S25", "la garde relit la référence au registre de la copie (L-11, l'ancien code)", V,
     "        chemin_ref, ensemble = C.CODE_DES_FAMILLES_DEJA_JOUEES[f]",
     "        chemin_ref, ensemble = C.CODE_DES_FAMILLES_DEJA_JOUEES[f][0], {module_de(f)[1]}"),
    ("S26", "auto-vérification retirée : code de C5 changé sans refiger (A-957)", V,
     "        if emp_ref is not None and emp_ref not in ensemble:", "        if False:"),
    ("S19c", "borne k <= N au lieu de k < N, « jouer 3 3 » accepté (N-2 du RELU Cowork de 14h58)", EN,
     "0 <= int(argv[5]) < int(argv[6])", "0 <= int(argv[5]) <= int(argv[6])"),
    ("S21", "porte du juge : module de la fiche jugée non passé à la garde (Q4, N-1 du RELU Cowork de 14h58)", V,
     '                      module=fiche.get("module_signal") or "", bareme=', "                      bareme="),
    ("S22", "version visée retirée de « moi » (N-4, M3 du RELU Cowork de 14h58)", V,
     "    moi = {norme(sid)} | ({norme(version)} if version else set())", "    moi = {norme(sid)}"),
    ("S23", "module de la fiche jugée vide accepté en silence (N-4, M4 du RELU Cowork de 14h58)", V,
     "        if emp is None:\n            raise Impossible(\"famille de la fiche jugée inconnue",
     "        if emp is None and chemin:\n            raise Impossible(\"famille de la fiche jugée inconnue"),
]


def main(argv):
    """Rend le code de sortie. [rend: 1]

    ① RÔLE — Jouer les cas, puis les sabotages. ② CONTEXTE D'APPEL — `__main__`.
    ③ ENTRÉE — `<source>` [--sans-sabotages]. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2. ⑥ TRAITEMENT — voir ⑥ de l'en-tête. ⑦ UNITÉ — —
    ⑧ POURQUOI — R-731. ⑨ CE QUI CLOCHE — voir l'en-tête. ⑩ EFFET — dossier de travail, effacé à la fin.
    ⑪ TERMINAISON — rend la main. [sort: non]
    """
    global SOURCE_DES_PROGRAMMES
    opts = [a for a in argv[1:] if a.startswith("--")]
    pos = [a for a in argv[1:] if not a.startswith("--")]
    if len(pos) != 1 or set(opts) - {"--sans-sabotages"}:
        print("usage : %s <source> [--sans-sabotages]" % argv[0])
        return 2
    source = os.path.abspath(pos[0])
    prog_dir = SOURCE_DES_PROGRAMMES = os.path.join(source, "programmes")
    prog = os.path.join(prog_dir, LANCEUR)
    if not os.path.exists(prog) or not os.path.exists(os.path.join(source, "emp.py")):
        print("❌ IMPOSSIBLE — %s ou emp.py absent" % prog)
        return 2
    base = "/dev/shm" if os.path.isdir("/dev/shm") else None
    travail = tempfile.mkdtemp(prefix="lanceur_", dir=base)
    rouge = False
    try:
        for nom, ok, detail in les_cas(prog, os.path.join(travail, "vrai")):
            print("%s %s : %s" % ("✅" if ok else "❌", nom, detail))
            rouge |= not ok
        if "--sans-sabotages" in opts:
            return 1 if rouge else 0
        os.symlink(os.path.join(source, "emp.py"), os.path.join(travail, "emp.py"))  # LIRE_LE_CODE le cherche là
        for nom, quoi, cible, avant, apres in SABOTAGES:
            texte = open(os.path.join(prog_dir, cible), encoding="utf-8").read()
            if texte.count(avant) != 1:
                print("❌ IMPOSSIBLE — ancre du sabotage %s trouvée %d fois dans %s" % (nom, texte.count(avant), cible))
                return 2
            sab = os.path.join(travail, "prog_" + nom)
            os.makedirs(sab)
            for f in os.listdir(prog_dir):
                if f.endswith(".py") and f != cible:
                    os.symlink(os.path.join(prog_dir, f), os.path.join(sab, f))
            with open(os.path.join(sab, cible), "w", encoding="utf-8") as fh:
                fh.write(texte.replace(avant, apres))
            tombes = [c for c, ok, _ in les_cas(os.path.join(sab, LANCEUR), os.path.join(travail, nom)) if not ok]
            mord = bool(tombes)
            print("%s %s %s (%s) → %s" % ("✅" if mord else "❌", nom, quoi, cible,
                                          ("tombe(nt) : " + " · ".join(c.split()[0] for c in tombes)) if mord
                                          else "AUCUN CAS NE TOMBE"))
            rouge |= not mord
            shutil.rmtree(os.path.join(travail, nom))
        return 1 if rouge else 0
    finally:
        shutil.rmtree(travail, ignore_errors=True)


SOURCE_DES_PROGRAMMES = None

if __name__ == "__main__":
    sys.exit(main(sys.argv))
