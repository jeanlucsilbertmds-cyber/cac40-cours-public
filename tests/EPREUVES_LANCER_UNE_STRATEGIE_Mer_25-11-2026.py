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
⑥ TRAITEMENT — ① un dossier de travail sous /dev/shm (sinon /tmp) · ② les cas C1 à C12 sur les vrais programmes ·
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
  dans programmes/ (accepté par le superviseur R-759 du 25-11-2026, Q5). ⑥ C13 reste VERT EXPRÈS et L-11 est OUVERT —
  DÉCISION DE JEAN-LUC DEMANDÉE LE 25-11-2026 : la référence de la famille se lit encore dans le registre de la copie,
  à sa dernière ligne ; une ligne C5E10-QA-V1 ajoutée sur un autre module, ou ses lignes retirées, laissent passer C5.
  ⑦ `porte_du_juge` elle-même n'est pas jouée : C15c appelle `V.motifs` avec le module comme elle le passe.
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
    comb, sortie, tranches = sys.argv[2], sys.argv[3], sys.argv[4:]
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
MODULE_C5 = '''"""Module factice de la famille déjà vue (rôle de C5 dans l'épreuve)."""
def signal(cours):
    return [c > 100 for c in cours]
'''
MODULE_C5_RECOPIE = '''"""Le même code sous un autre nom, texte explicatif et commentaire changés (L-1, A1c du RELU Cowork)."""
def signal(cours):
    # un commentaire qui n'est pas du code
    return [c > 100 for c in cours]
'''
MODULE_NEUF = '''"""Module factice d'une famille neuve."""
def signal(cours):
    return [c < 100 for c in cours]
'''


def fabriquer(dossier, valide=True, module="programmes/MODULE_FAUX_NEUF.py"):
    """Fabrique une racine factice ; rend son chemin. [rend: 1]

    ① RÔLE — La copie jetable : fiche factice, réglages, cours de 2024, doublures, modules de signal factices.
    ② CONTEXTE D'APPEL — chaque cas.
    ③ ENTRÉE — `dossier` (absent) ; `valide` : la mention de validation est-elle écrite ? `module` : le module de
      signal de la fiche factice, tel qu'écrit au registre (celui de la fiche déjà vue C5E10-QA-V1, recopiée en
      factice, fait une famille déjà jouée ; « ./programmes/… » ou la copie MODULE_COPIE_DU_C5.py aussi).
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
    for nom, texte in (("MODULE_FAUX_C5.py", MODULE_C5), ("MODULE_COPIE_DU_C5.py", MODULE_C5_RECOPIE),
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
    attendu = {"0-variables-validees", "0-proposition", "1-decliner", "2-assembler", "3-trier"} | \
        {"2-tranche-%d" % k for k in range(N)}
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
    # C13 — LE TROU NOMMÉ (⑨ ④ de V.famille_deja_jouee), OUVERT — DÉCISION DE JEAN-LUC DEMANDÉE LE 25-11-2026 (L-11) :
    # la fiche déjà vue retirée du registre de la copie, la famille C5 n'est plus vue et passe. Vert tant que le trou existe ; il rougira le jour où il sera bouché (comme S17 de
    # tests/EPREUVES_ENCHAINER_LA_MOULINETTE_Jeu_19-11-2026.py).
    q = fabriquer(os.path.join(travail, "c13"), module="programmes/MODULE_FAUX_C5.py")
    reg = os.path.join(q, "donnees", "cac40_strategies.csv")
    lignes = open(reg, encoding="utf-8").read().splitlines()
    open(reg, "w", encoding="utf-8").write("\n".join(l for l in lignes if not l.startswith("C5E10-QA-V1,")) + "\n")
    code, out = lancer(prog, q, "--tranches=%d" % N)
    r.append(("C13 TROU MONTRÉ : fiche déjà vue retirée du registre, C5 passe", code == 0 and FIN in out,
              "code %d" % code))
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
    # C17 — L-10, L-7 : « jouer 00 3 » et « jouer 5 3 » refusés par l'enchaîneur (usage, code 2), aucun témoin écrit.
    q = fabriquer(os.path.join(travail, "c17"))
    codes = [ench(prog, q, *x)[0] for x in (["preparer"], ["decliner"], ["jouer", "0", "3"], ["jouer", "00", "3"],
                                            ["jouer", "5", "3"])]
    j = journal(q)
    r.append(("C17 « jouer 00 3 » et « jouer 5 3 » refusés (L-10, L-7)", codes == [0, 0, 0, 2, 2] and
              "2-tranche-00" not in j and "2-tranche-5" not in j, "codes %s" % codes))
    # C18 — L-8 : famille C5, chaîne faite à la main jusqu'à ③, le FICHIER de déclaration écrit à la main SANS témoin
    # au journal : juger refusé (la garde lit le journal, pas le fichier).
    q = fabriquer(os.path.join(travail, "c18"), module="programmes/MODULE_FAUX_C5.py")
    codes = [ench(prog, q, *x)[0] for x in (["preparer"], ["decliner"], ["jouer", "0", "1"], ["assembler"], ["trier"])]
    with open(os.path.join(q, CH, "famille_declaree.txt"), "w", encoding="utf-8") as fh:
        fh.write("écrite à la main, sans témoin au journal\n")
    code, out = ench(prog, q, "juger", "%s-%s-0007" % (SID, ESSAI))
    r.append(("C18 fichier de déclaration sans témoin au journal (L-8) : juger refusé", codes == [0] * 5 and
              code == 1 and "REFUS ④" in out, "codes %s puis %d" % (codes, code)))
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
     "        elif module_de(f)[1] in mien:", "        elif module_de(f)[0] in mien.values():"),
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
