#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_DECOUPER_LA_MOULINETTE_Ven_27-11-2026.py — Ven 27-11-2026 (Paris). Simulation uniquement.

LE SENS EN TÊTE. Éprouve programmes/DECOUPER_LA_MOULINETTE.py (lot W2f du plan R505, A-965) : le plan de découpage,
la relecture d'un chronométrage, le bout « machine » (tranche) et le bout « centre » (rassembler, reprise, refus), de
bout en bout par le VRAI enchaîneur et sa VRAIE garde, sur des copies FABRIQUÉES par la fonction `fabriquer` de
tests/EPREUVES_LANCER_UNE_STRATEGIE_Mer_25-11-2026.py (importée, R-708 : fiche factice, cours fabriqués de 2024,
doublures de PREPARER, DECLINER, JOUER — 7 versions). Aucun cours réel n'est joué, aucune date d'avant 2024 regardée.
Puis des SABOTAGES de DECOUPER_LA_MOULINETTE.py : chacun doit faire tomber au moins un cas.

USAGE
    python3 -B tests/EPREUVES_DE_DECOUPER_LA_MOULINETTE_Ven_27-11-2026.py <source> [--sans-sabotages]

① RÔLE — Prouver : le plan couvre toutes les versions sous le budget ; la mesure se relit d'une sortie au format réel ;
  trois machines jouent trois tranches que le centre reçoit et que l'enchaîneur assemble ; une tranche manquante est
  dite « À REJOUER » puis reçue ; un bloc d'une autre chaîne (réglages, cours, découpage), corrompu, ou en conflit est
  refusé SANS RIEN ÉCRIRE ; une copie avec .git est refusée.
② CONTEXTE D'APPEL — À la main, ou par la certification (chaque tests/*.py avec la seule copie).
③ ENTRÉE — `<source>` : racine d'une copie du dépôt ; `--sans-sabotages` : les cas seulement.
④ CONDITIONS D'ENTRÉE — `<source>/programmes/DECOUPER_LA_MOULINETTE.py` et l'épreuve du lanceur existent.
⑤ SORTIE — UNE valeur, le code : 0 tout tient · 1 un cas tombe ou un sabotage ne mord pas · 2 l'épreuve n'a pas pu
  tourner (ancre absente, usage faux — R-734).
⑥ TRAITEMENT — ① dossier de travail sous /dev/shm (sinon /tmp) · ② cas D1 à D11 · ③ chaque sabotage : dossier de
  programmes fait de liens, DECOUPER remplacé par son texte saboté, cas rejoués, au moins un doit tomber · ④ ménage.
⑦ UNITÉ — secondes (délais).
⑧ POURQUOI — R-731, R-732 (D2 porte des lignes réelles du chronométrage du 27-11-2026, machine du Chat).
⑨ CE QUI CLOCHE — La doublure de JOUER ne lit pas les cours : la propriété « l'assemblage refuse une tranche jouée sur
  d'autres cours » de JOUER (L1) n'est pas rejouée ici ; c'est le témoin des cours, comparé par « rassembler », qui
  l'est (D7). Le transport par GitHub n'est pas éprouvé (le circuit n'existe pas).
⑩ EFFET — écrit sous le dossier de travail, effacé.
⑪ TERMINAISON — chaque lancement borné à 120 s. [sort: oui]
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
PROG = "DECOUPER_LA_MOULINETTE.py"
EPREUVE_DU_LANCEUR = os.path.join("tests", "EPREUVES_LANCER_UNE_STRATEGIE_Mer_25-11-2026.py")
N = 3
# LIGNES RÉELLES (R-732) du chronométrage de la fiche d'essai, machine du Chat, 27-11-2026 vers 20h50 (sans résultat).
CHRONO_REEL = """[+    1.7 s] ESSAI — NI RÉSULTAT NI SÉLECTION · CONTRAT DE STRATÉGIE : la fiche et les 1 versions le suivent
[+   15.8 s] ESSAI — NI RÉSULTAT NI SÉLECTION · COURS LUS : temoins/TEMOIN_VINGT_ANS_2000_2026_COUPURE_2026-11-11_FIGE_Ven_13-11-2026_10h59.csv
[+   47.7 s] ESSAI — NI RÉSULTAT NI SÉLECTION · CALIBRAGE PAR LE JUGE SEUL : OK
[+   52.5 s] ESSAI — NI RÉSULTAT NI SÉLECTION ·   ce programme : (chiffres retirés de l'épreuve)
[+   57.9 s] ESSAI — NI RÉSULTAT NI SÉLECTION ·   version identique ESSAI-C5-2000-2026-E01-0001 : même résultat
[+   63.1 s] ESSAI — NI RÉSULTAT NI SÉLECTION · PARTIE DE RÉGLAGE : signaux avant la frontière 2018-10-15
[+   69.3 s] CODE DE LA MOULINETTE : 0
CHRONO total=69.5 · fin
"""
L = None   # le module de l'épreuve du lanceur (sa `fabriquer`), chargé par `main`


def lancer(prog_dir, *args):
    """Lance DECOUPER ; rend (code, sortie). Borné à 120 s. [rend: 2]

    ①–⑪ : ① lancer · ② chaque cas · ③ le dossier des programmes éprouvés, les arguments · ④ — · ⑤ DEUX valeurs ·
    ⑥ subprocess · ⑦ secondes · ⑧ — · ⑨ — · ⑩ ce qu'écrit le mode · ⑪ borné. [sort: non]
    """
    p = subprocess.run([sys.executable, "-B", os.path.join(prog_dir, PROG)] + list(args), capture_output=True,
                       text=True, timeout=120)
    return p.returncode, p.stdout + p.stderr


def ench(prog_dir, racine, *args):
    """Lance l'enchaîneur voisin ; rend (code, sortie). Borné. [rend: 2] — ①–⑪ comme `lancer`. [sort: non]"""
    p = subprocess.run([sys.executable, "-B", os.path.join(prog_dir, "ENCHAINER_LA_MOULINETTE.py"), racine, L.SID,
                        L.ESSAI] + list(args), capture_output=True, text=True, timeout=120, cwd=racine)
    return p.returncode, p.stdout + p.stderr


def machine(prog_dir, travail, nom, k, n=N, modifier=None, maitre=False):
    """Fabrique une copie « machine », y joue la tranche k/n ; rend (code, chemin de la sortie). [rend: 2]

    ①–⑪ : ① le bout machine · ② les cas · ③ `modifier` : fonction appliquée à la copie avant le jeu · ④ — ·
    ⑤ DEUX valeurs · ⑥ fabriquer, modifier, DECOUPER tranche, sortie écrite dans un fichier · ⑦ — · ⑧ — · ⑨ — ·
    ⑩ écrit sous `travail` · ⑪ borné. [sort: non]
    """
    copie = L.fabriquer(os.path.join(travail, nom))
    if modifier:
        modifier(copie)
    code, out = lancer(prog_dir, "tranche", copie, L.SID, L.ESSAI, str(k), str(n),
                       *(["--cours-du-maitre"] if maitre else []))
    chemin = os.path.join(travail, nom + ".txt")
    with open(chemin, "w", encoding="utf-8") as fh:
        fh.write(out)
    return code, chemin


def centre(prog_dir, travail, nom):
    """Fabrique la copie « centre » et y fait ⓪ ① par l'enchaîneur ; rend son chemin. [rend: 1] — ①–⑪ comme
    `machine`. [sort: non]"""
    c = L.fabriquer(os.path.join(travail, nom))
    for etape in ("preparer", "decliner"):
        code, out = ench(prog_dir, c, etape)
        if code:
            raise RuntimeError("centre : %s a rendu %d : %s" % (etape, code, out[-300:]))
    return c


def journal(c):
    """Rend le texte du journal de la chaîne (vide s'il manque). [rend: 1] [sort: non]"""
    j = os.path.join(c, L.CH, "JOURNAL_DE_LA_CHAINE.csv")
    return open(j, encoding="utf-8").read() if os.path.exists(j) else ""


def changer_un_bloc(src, dst, transforme):
    """Recopie une sortie en appliquant `transforme` au JSON du bloc. [rend: rien] [sort: non]"""
    lignes = open(src, encoding="utf-8").read().split("\n")
    i = next(i for i, l in enumerate(lignes) if l.startswith("=== BLOC DE TRANCHE"))
    b = json.loads(lignes[i + 1])
    transforme(b)
    lignes[i + 1] = json.dumps(b, ensure_ascii=True, sort_keys=True)
    open(dst, "w", encoding="utf-8").write("\n".join(lignes))


def les_cas(prog_dir, travail):
    """Rend la liste (nom, tenu, détail) des cas. [rend: 1]

    ①–⑪ : ① les propriétés · ② `main` · ③ le dossier des programmes, un dossier de travail neuf · ④ — · ⑤ UNE liste ·
    ⑥ voir l'en-tête · ⑦ — · ⑧ R-731 · ⑨ — · ⑩ écrit sous `travail` · ⑪ borné. [sort: non]
    """
    os.makedirs(travail)
    cas = []
    spec = importlib.util.spec_from_file_location("decouper_eprouve", os.path.join(prog_dir, PROG))
    D = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(D)
    # D1 — le plan couvre, sous le budget, et compte les vagues
    p = D.planifier(21000, 63.1, 6.2, 580, 8, 70)
    t = p["versions_par_tranche"]
    ok = (p["tranches"] * t >= 21000 and (p["tranches"] - 1) * t < 21000 and 63.1 + t * 6.2 <= 580
          and p["vagues"] * 8 >= p["tranches"] > (p["vagues"] - 1) * 8)
    cas.append(("D1 plan couvrant sous le budget", ok, str(p)))
    try:
        D.planifier(10, 63.1, 6.2, 60, 8, 70)
        cas.append(("D1b budget sous le fixe refusé", False, "accepté"))
    except ValueError:
        cas.append(("D1b budget sous le fixe refusé", True, "ValueError"))
    # D2 — la mesure relue d'une sortie au format réel
    f = os.path.join(travail, "chrono.txt")
    open(f, "w", encoding="utf-8").write(CHRONO_REEL)
    fixe, pv, d = D.couts(D.lire_un_chronometrage(f))
    ok = (fixe, pv, d["lecture"], d["calibrage"], d["un_jeu"], d["total"]) == (63.1, 6.2, 14.1, 31.9, 4.8, 69.5)
    cas.append(("D2 mesure relue (lignes réelles)", ok, str(d)))
    try:
        D.couts({k: v for k, v in D.lire_un_chronometrage(f).items() if k != "calibrage"})
        cas.append(("D2b marque absente refusée", False, "accepté"))
    except ValueError:
        cas.append(("D2b marque absente refusée", True, "ValueError"))
    # D3 — bout en bout : trois machines, le centre reçoit, l'enchaîneur assemble
    sorties = []
    for k in range(N):
        code, s = machine(prog_dir, travail, "m%d" % k, k)
        sorties.append(s)
        cas.append(("D3 machine %d" % k, code == 0 and "=== FIN DU BLOC" in open(s).read(), "code %d" % code))
    c = centre(prog_dir, travail, "centre")
    code, out = lancer(prog_dir, "rassembler", c, L.SID, L.ESSAI, str(N), *sorties)
    ca, oa = ench(prog_dir, c, "assembler")
    res = os.path.join(c, L.CH, "e2", "RESULTATS_%s_%s.csv" % (L.SID, L.ESSAI))
    lignes = open(res).read().strip().split("\n") if os.path.exists(res) else []
    cas.append(("D3 rassemblé puis assemblé", code == 0 and ca == 0 and len(lignes) == 8,
                "rassembler %d, assembler %d, %d lignes" % (code, ca, len(lignes))))
    # D4 — reprise : une tranche manque, dite, puis reçue ; tout renvoyer est sans effet
    c = centre(prog_dir, travail, "reprise")
    c1, o1 = lancer(prog_dir, "rassembler", c, L.SID, L.ESSAI, str(N), sorties[0], sorties[2])
    c2, o2 = lancer(prog_dir, "rassembler", c, L.SID, L.ESSAI, str(N), *sorties)
    cas.append(("D4 reprise", c1 == 3 and "À REJOUER : 1 " in o1 and c2 == 0 and journal(c).count("2-tranche-") == 3,
                "codes %d puis %d" % (c1, c2)))

    def refuse(nom, *fichiers):
        """Le centre neuf refuse et n'écrit rien. [rend: 1] [sort: non]"""
        cc = centre(prog_dir, travail, nom)
        avant = journal(cc)
        code, out = lancer(prog_dir, "rassembler", cc, L.SID, L.ESSAI, str(N), *fichiers)
        ok = code == 1 and journal(cc) == avant and not os.path.exists(os.path.join(cc, L.CH, "e2"))
        return ok, "code %d · %s" % (code, out.strip().split("\n")[-1][:120])

    # D5 — bloc corrompu (texte changé, empreinte non recalculée)
    f5 = os.path.join(travail, "corrompu.txt")
    changer_un_bloc(sorties[1], f5, lambda b: b.update(tranche=b["tranche"] + "x"))
    cas.append(("D5 bloc corrompu refusé",) + refuse("c5", sorties[0], f5))

    # D6 — réglages validés différents sur la machine
    def autres_reglages(copie):
        v = os.path.join(copie, "donnees", "combinatoires", "VARIABLES_DE_DECLINAISON_%s_%s.csv" % (L.SID, L.ESSAI))
        texte = open(v, encoding="utf-8").read()
        open(v, "w", encoding="utf-8").write(texte.replace("factice", "factice bis"))
    _, f6 = machine(prog_dir, travail, "m6", 1, modifier=autres_reglages)
    cas.append(("D6 autres réglages refusés",) + refuse("c6", sorties[0], f6))
    # D7 — autres cours (la machine a joué le maître)
    _, f7 = machine(prog_dir, travail, "m7", 1, maitre=True)
    cas.append(("D7 autres cours refusés",) + refuse("c7", sorties[0], f7))
    # D8 — autre découpage
    _, f8 = machine(prog_dir, travail, "m8", 1, n=4)
    cas.append(("D8 autre découpage refusé",) + refuse("c8", sorties[0], f8))
    # D9 — deux blocs différents pour une même tranche (empreintes recalculées : chacun est sain en lui-même)

    def autre_texte(b):
        b["tranche"] += "\n"
        b["sha256"] = D.empreinte(b["tranche"])
        b["temoins"]["2-tranche-%d" % b["k"]] = b["sha256"]
    f9 = os.path.join(travail, "conflit.txt")
    changer_un_bloc(sorties[1], f9, autre_texte)
    cas.append(("D9 conflit sur une tranche refusé",) + refuse("c9", sorties[1], f9))
    # D10 — tranche déjà reçue, renvoyée autrement
    c = centre(prog_dir, travail, "c10")
    lancer(prog_dir, "rassembler", c, L.SID, L.ESSAI, str(N), sorties[1])
    av = journal(c)
    code, out = lancer(prog_dir, "rassembler", c, L.SID, L.ESSAI, str(N), f9)
    cas.append(("D10 déjà reçue autrement refusée", code == 1 and journal(c) == av, "code %d" % code))
    # D11 — une copie avec .git est refusée par le bout machine
    g = L.fabriquer(os.path.join(travail, "git"))
    os.makedirs(os.path.join(g, ".git"))
    code, out = lancer(prog_dir, "tranche", g, L.SID, L.ESSAI, "0", str(N))
    cas.append(("D11 .git refusé avant tout lancement", code == 2 and "ARRÊT (DECOUPER)" in out, "code %d" % code))
    return cas


SABOTAGES = [
    ("S1", "aucun témoin comparé", "TEMOINS_COMPARES = (E.TEMOIN_DES_COURS, \"0-variables-validees\", E.FAITE[\"decliner\"])",
     "TEMOINS_COMPARES = ()"),
    ("S2", "empreinte du bloc non vérifiée", "if empreinte(b[\"tranche\"]) != b[\"sha256\"] or", "if False and"),
    ("S3", "découpage du bloc non comparé", "if (b[\"strategie\"], b[\"essai\"], b[\"n\"]) != (sid, essai, n):",
     "if (b[\"strategie\"], b[\"essai\"]) != (sid, essai):"),
    ("S4", "conflit entre blocs non vu", "if b[\"k\"] in neufs and neufs[b[\"k\"]][\"sha256\"] != b[\"sha256\"]:",
     "if False:"),
    ("S5", "manquantes jamais dites", "manquent = [k for k in range(n) if TEMOIN_DE_TRANCHE % k not in t]",
     "manquent = []"),
    ("S6", "écrit avant de tout vérifier", "    if refus:\n        print(\"REFUS — rien n'est écrit :\\n  %s\" % \"\\n  \".join(refus))\n        return 1, []\n",
     ""),
    ("S7", "budget sans le fixe", "vpt = int((budget - fixe) // par_version)", "vpt = int(budget // par_version)"),
    ("S8", "déjà reçue autrement non vue", "if cle in local and local[cle][1] != b[\"sha256\"]:", "if False:"),
    ("S9", ".git accepté", "    if os.path.lexists(os.path.join(copie, \".git\")):\n        print(\"ARRÊT (DECOUPER)",
     "    if False:\n        print(\"ARRÊT (DECOUPER)"),
]


def main(argv):
    """Rend le code de sortie. [rend: 1]

    ①–⑪ : ① cas puis sabotages · ② `__main__` · ③ `<source>` [--sans-sabotages] · ④ — · ⑤ 0, 1 ou 2 · ⑥ en-tête ⑥ ·
    ⑦ — · ⑧ R-731 · ⑨ — · ⑩ dossier de travail effacé · ⑪ rend la main. [sort: non]
    """
    global L
    opts = [a for a in argv[1:] if a.startswith("--")]
    pos = [a for a in argv[1:] if not a.startswith("--")]
    if len(pos) != 1 or set(opts) - {"--sans-sabotages"}:
        print("usage : %s <source> [--sans-sabotages]" % argv[0])
        return 2
    source = os.path.abspath(pos[0])
    prog_dir = os.path.join(source, "programmes")
    if not os.path.exists(os.path.join(prog_dir, PROG)) or not os.path.exists(os.path.join(source, EPREUVE_DU_LANCEUR)):
        print("❌ IMPOSSIBLE — %s ou %s absent" % (PROG, EPREUVE_DU_LANCEUR))
        return 2
    spec = importlib.util.spec_from_file_location("epreuve_du_lanceur", os.path.join(source, EPREUVE_DU_LANCEUR))
    L = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(L)
    L.SOURCE_DES_PROGRAMMES = prog_dir
    travail = tempfile.mkdtemp(prefix="decouper_", dir="/dev/shm" if os.path.isdir("/dev/shm") else None)
    rouge = False
    try:
        for nom, ok, detail in les_cas(prog_dir, os.path.join(travail, "vrai")):
            print("%s %s : %s" % ("✅" if ok else "❌", nom, detail))
            rouge |= not ok
        if "--sans-sabotages" in opts:
            return 1 if rouge else 0
        texte = open(os.path.join(prog_dir, PROG), encoding="utf-8").read()
        for nom, quoi, avant, apres in SABOTAGES:
            if texte.count(avant) != 1:
                print("❌ IMPOSSIBLE — ancre du sabotage %s trouvée %d fois" % (nom, texte.count(avant)))
                return 2
            sab = os.path.join(travail, "prog_" + nom)
            os.makedirs(sab)
            for f in os.listdir(prog_dir):
                if f.endswith(".py") and f != PROG:
                    os.symlink(os.path.join(prog_dir, f), os.path.join(sab, f))
            with open(os.path.join(sab, PROG), "w", encoding="utf-8") as fh:
                fh.write(texte.replace(avant, apres))
            try:
                tombes = [c for c, ok, _ in les_cas(sab, os.path.join(travail, nom)) if not ok]
            except Exception as e:   # noqa: BLE001 — un sabotage qui fait planter l'épreuve la fait tomber
                tombes = ["plantage %s" % type(e).__name__]
            print("%s %s %s → %s" % ("✅" if tombes else "❌", nom, quoi,
                                     ("tombe(nt) : " + " · ".join(c.split()[0] for c in tombes)) if tombes
                                     else "AUCUN CAS NE TOMBE"))
            rouge |= not tombes
            shutil.rmtree(os.path.join(travail, nom), ignore_errors=True)
        return 1 if rouge else 0
    finally:
        shutil.rmtree(travail, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
