#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DES_TROIS_ELEMENTS — Mer 30-09-2026 (Paris)
DÉCIDÉ · Rôle : prouver que programmes/verif_backlog.py refuse une action nouvelle qui ne commence pas par ses trois éléments, et que chaque épreuve a des dents.
Quand l'appeler : avant toute livraison qui touche `trois_elements` ou la boucle des lignes dans programmes/verif_backlog.py (R-755 ②).

À QUOI ÇA SERT. Jean-Luc, 29-09-2026 à 22h09 : « trouve le moyen de systématiquement ajouter ces trois éléments
en en-tête de chaque future action ». Depuis la nuit du 30-09-2026, verif_backlog.py rend ❌ pour toute action
numérotée à partir de A-502 dont le texte ne commence pas par « **EN BREF** : », suivi de « **SI ON LE FAIT** : »
puis de « **SI ON NE LE FAIT PAS** : » ; une action vivante plus ancienne sans eux n'est comptée qu'en ⚠.
Chaque épreuve travaille sur une COPIE du dépôt ; la ligne ajoutée est la vraie ligne A-502 (R-732), renumérotée.

LES ÉPREUVES : Z0 le vrai BACKLOG : aucun ❌ « trois éléments », et le nombre annoncé par le ⚠ égale le nombre de
lignes vivantes anciennes qui ne commencent pas par « **EN BREF** : », compté ici sans passer par verif_backlog
(zéro ⚠ attendu quand il n'y en a plus) · E1 une action
A-9001 sans les trois éléments : ❌ qui la nomme · E2 la même avec eux : pas de ❌ pour elle · E3 les trois dans le
désordre : ❌ · E4 un élément manquant : ❌ · E5 une action vivante ancienne, choisie dans le fichier, privée de ses
éléments : ⚠, jamais ❌ · E6 une action CLOSE sans éléments n'est jamais comptée · E7 la frontière : la vraie A-502
privée de ses éléments : ❌ · E8 éléments enfouis loin du début : ❌ · E9 étiquette sans phrase : ❌ · E10 pas de
« — » final : ❌ · E12 les trois éléments présents mais pas en tête : ❌ · E13 une phrase sans aucune lettre
(« ... ») : ❌ · E14 une action nouvelle dont le texte porte une barre « | » entourée d'espaces, sans ses
éléments : ❌ quand même · E11 le chemin réel : le radar du soir
(audit_ecosysteme.py) affiche le ❌ nouveau (A-9004), même derrière trois ❌ anciens que l'épreuve pose elle-même
devant lui (A-9001 à A-9003 ; depuis le 16-10-2026, le vrai BACKLOG n'en ayant plus aucun).
LES SABOTAGES : S1 change le ❌ en ⚠ · S2 relève le seuil au-delà de A-9001 · S3 accepte tout texte · S5 compte aussi
les actions closes · S6 met la frontière à A-600 · S7 ne vérifie plus le début · S8 remet au radar « les trois
premières alertes » · S9 ne borne plus la longueur · S10 n'exige plus le « — » · S11 accepte une phrase vide ·
S12 accepte une phrase non vide sans lettre.
Chacun doit faire rougir au moins une épreuve. Un sabotage S4 (« ne plus vérifier l'ordre ») a été essayé et
retiré le 30-09-2026 : mesuré sans effet, parce que l'exigence d'une phrase non vide entre deux étiquettes refuse
déjà le désordre.
LIMITE CONNUE (corrigée le 30-09-2026 après le tour 3 du relecteur) : une ligne dont le texte porte une barre
verticale entourée d'espaces EST vue, mais ses cases sont décalées ; le ❌ des trois éléments s'applique encore,
puisqu'il ne lit que le début du texte (E14), mais l'état est mal lu : verif_backlog rend ❌ « statut inconnu », et
une action ancienne dans ce cas n'est pas comptée en ⚠ (cas réel : A-435). Une ligne à qui il manque une case n'est
signalée que par l'écart de comptage. Une ligne dont le début s'écarte de la forme exacte (espace manquant après la
barre, tabulation) n'est vue par rien, pas même l'écart de comptage (mesuré par le relecteur le 30-09-2026 ; A-503).

USAGE : python3 tests/EPREUVES_DES_TROIS_ELEMENTS_Mer_30-09-2026.py <racine du dépôt> [--saboter]
CODE : 0 si Z0 est vert et que chaque sabotage fait rougir au moins une épreuve ; 1 sinon.
"""
import os, re, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
VB = "programmes/verif_backlog.py"
SABOTAGES = {
    "Z0": [],
    "S1_pas_de_refus": [(VB, 'err.append(f"{aid} : ne commence pas', 'warn.append(f"{aid} : ne commence pas')],
    "S2_seuil_releve": [(VB, "PREMIERE_ACTION_A_TROIS_ELEMENTS = 502", "PREMIERE_ACTION_A_TROIS_ELEMENTS = 99999")],
    "S3_tout_accepte": [(VB, '    t = (texte or "").strip()\n    if not t.startswith', '    return True\n    t = (texte or "").strip()\n    if not t.startswith')],
    # S4 (« ne plus vérifier l'ordre ») est RETIRÉ le 30-09-2026 : mesuré, il ne fait rien rougir, parce que
    # l'exigence d'une phrase non vide entre deux étiquettes suffit à refuser le désordre (la tranche est vide).
    "S5_compte_tout": [(VB, "            elif base in VIVANTS:\n                sans_trois.append(aid)", "            else:\n                sans_trois.append(aid)")],
    "S6_seuil_600": [(VB, "PREMIERE_ACTION_A_TROIS_ELEMENTS = 502", "PREMIERE_ACTION_A_TROIS_ELEMENTS = 600")],
    "S7_tete_ignoree": [(VB, "    if not t.startswith(TROIS_ELEMENTS[0]):\n        return False\n    debuts", "    debuts")],
    "S8_radar_trois_premieres": [("programmes/audit_ecosysteme.py", "{' | '.join(_echecs) or _resume}", "{' | '.join(_alertes[:3]) or _resume}")],
    "S9_longueur_ignoree": [(VB, "if not any(c.isalpha() for c in phrase) or len(phrase.split()) > MOTS_PAR_ELEMENT:", "if not any(c.isalpha() for c in phrase):")],
    "S10_tiret_ignore": [(VB, "    if fin_tete < 0:\n        return False\n", "    if fin_tete < 0:\n        fin_tete = len(t)\n")],
    "S11_vide_accepte": [(VB, "if not any(c.isalpha() for c in phrase) or len(phrase.split()) > MOTS_PAR_ELEMENT:", "if len(phrase.split()) > MOTS_PAR_ELEMENT:")],
    "S12_lettre_ignoree": [(VB, "if not any(c.isalpha() for c in phrase) or", "if not phrase or")],
}
EB, SF, SP = "**EN BREF** :", "**SI ON LE FAIT** :", "**SI ON NE LE FAIT PAS** :"


def verif(racine, lignes_en_plus=(), remplacer=None):
    b = os.path.join(racine, "BACKLOG_DECISIONS.md")
    t = open(b, encoding="utf-8").read()
    if remplacer:
        a, n = remplacer
        assert t.count(a) == 1, "ancre absente : " + a[:40]
        t = t.replace(a, n)
    if lignes_en_plus:
        L = t.split("\n")
        i = max(k for k, l in enumerate(L) if l.startswith("| A-"))
        L[i + 1:i + 1] = list(lignes_en_plus)
        t = "\n".join(L)
    open(b, "w", encoding="utf-8").write(t)
    p = subprocess.run([sys.executable, os.path.join(racine, VB), b], capture_output=True, text=True)
    return p.stdout + p.stderr


def epreuves(r):
    t = open(os.path.join(r, "BACKLOG_DECISIONS.md"), encoding="utf-8").read()
    a502 = next(l for l in t.split("\n") if l.startswith("| A-502 | "))
    corps = a502[len("| A-502 | "):]
    sans = corps.split(" — ", 1)[1]           # le texte d'origine, privé de ses trois éléments
    orig, queue = sans.split(" | ", 1)        # la 2e case seule, et les cases qui la suivent
    res = []
    out = verif(r)
    # Z0 — une PROPRIÉTÉ, pas une présence : le ⚠ annonce exactement les lignes vivantes anciennes sans
    # « **EN BREF** : » en tête, comptées ici par un motif simple, indépendant de trois_elements.
    attendu = 0
    for m in re.finditer(r"^\| A-(\d+)[A-Za-z]* \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|", t, re.M):
        if int(m.group(1)) < 502 and m.group(3).split("·")[0].strip() in ("À FAIRE", "À DÉCIDER", "EN COURS", "BLOQUÉE") \
                and not m.group(2).strip().startswith(EB):
            attendu += 1
    mw = re.search(r"⚠ (\d+) action\(s\) vivante\(s\) sans leurs trois éléments en tête", out)
    res.append(("Z0 vrai BACKLOG : aucun ❌ trois éléments, ⚠ = %d lignes vivantes anciennes sans éléments" % attendu,
                "ne commence pas par ses trois" not in out and (int(mw.group(1)) if mw else 0) == attendu))
    sauve = t
    def essai(ligne):
        open(os.path.join(r, "BACKLOG_DECISIONS.md"), "w", encoding="utf-8").write(sauve)
        return verif(r, [ligne])
    out = essai("| A-9001 | " + sans)
    res.append(("E1 action nouvelle sans ses trois éléments : ❌", re.search(r"❌ A-9001 : ne commence pas", out) is not None))
    out = essai("| A-9001 | " + corps)
    res.append(("E2 action nouvelle avec ses trois éléments : pas de ❌", "A-9001 : ne commence pas" not in out))
    desordre = EB + " x. " + SP + " z. " + SF + " y. — " + sans
    out = essai("| A-9001 | " + desordre)
    res.append(("E3 trois éléments dans le désordre : ❌", re.search(r"❌ A-9001 : ne commence pas", out) is not None))
    out = essai("| A-9001 | " + corps.replace(SP, "**SI ON NE FAIT RIEN** :", 1))
    res.append(("E4 un élément manquant : ❌", re.search(r"❌ A-9001 : ne commence pas", out) is not None))
    # E5 — une action VIVANTE ANCIENNE qui porte ses éléments, choisie dans le vrai fichier,
    # en est privée : elle doit passer en ⚠, jamais en ❌ (le choix ne dépend d'aucun numéro écrit ici)
    vieille = next(l for l in sauve.split("\n") if re.match(r"^\| A-(\d+) \| \*\*EN BREF\*\*", l)
                   and int(re.match(r"^\| A-(\d+)", l).group(1)) < 502
                   and re.search(r"\| (À FAIRE|À DÉCIDER|EN COURS|BLOQUÉE)·", l))
    vid = re.match(r"^\| (A-\d+)", vieille).group(1)
    open(os.path.join(r, "BACKLOG_DECISIONS.md"), "w", encoding="utf-8").write(sauve)
    out = verif(r, remplacer=(vieille, "| %s | " % vid + vieille.split(" — ", 1)[1]))
    res.append(("E5 action vivante ancienne privée de ses éléments : ⚠, pas ❌",
                ("%s : ne commence pas" % vid) not in out
                and re.search(r"sans leurs trois éléments en tête : .*\b%s\b" % re.escape(vid), out) is not None))
    # E6 — une action CLOSE ancienne sans éléments n'est jamais comptée
    close = next(l for l in sauve.split("\n") if re.search(r"^\| A-\d+ \| .*? \| CLOSE·", l)
                 and not re.match(r"^\| A-\d+ \| \*\*EN BREF", l))
    cid = re.match(r"^\| (A-\d+)", close).group(1)
    open(os.path.join(r, "BACKLOG_DECISIONS.md"), "w", encoding="utf-8").write(sauve)
    out = verif(r)
    ligne_w = next((l for l in out.split("\n") if "sans leurs trois éléments en tête" in l), "")
    res.append(("E6 action CLOSE sans éléments : jamais comptée", re.search(r"\b%s\b" % re.escape(cid), ligne_w) is None))
    # E7 — la frontière : la vraie A-502, privée de ses éléments, doit être refusée
    open(os.path.join(r, "BACKLOG_DECISIONS.md"), "w", encoding="utf-8").write(sauve)
    out = verif(r, remplacer=(a502, "| A-502 | " + sans))
    res.append(("E7 frontière : A-502 sans ses éléments : ❌", re.search(r"❌ A-502 : ne commence pas", out) is not None))
    # E8 — éléments 2 et 3 enfouis loin du début : ❌ (seule la borne de longueur l'arrête)
    out = essai("| A-9001 | " + EB + " x. " + orig + " — " + SF + " y. " + SP + " z. — suite | " + queue)
    res.append(("E8 éléments enfouis loin du début : ❌", re.search(r"❌ A-9001 : ne commence pas", out) is not None))
    # E9 — une étiquette sans phrase : ❌
    out = essai("| A-9001 | " + EB + " x. " + SF + " " + SP + " z. — " + sans)
    res.append(("E9 étiquette sans phrase : ❌", re.search(r"❌ A-9001 : ne commence pas", out) is not None))
    # E10 — trois phrases courtes, mais pas de « — » qui les ferme : ❌ (seul le « — » l'arrête)
    out = essai("| A-9001 | " + EB + " x. " + SF + " y. " + SP + " z. fin courte | " + queue)
    res.append(("E10 trois phrases sans « — » final : ❌", re.search(r"❌ A-9001 : ne commence pas", out) is not None))
    # E12 — les trois éléments présents, mais pas en tête : ❌ (seul le contrôle du début l'arrête)
    out = essai("| A-9001 | Texte d'abord. " + EB + " x. " + SF + " y. " + SP + " z. — suite | " + queue)
    res.append(("E12 éléments présents mais pas en tête : ❌", re.search(r"❌ A-9001 : ne commence pas", out) is not None))
    # E13 — une phrase sans aucune lettre : ❌ (seule l'exigence d'une lettre l'arrête)
    out = essai("| A-9001 | " + EB + " x. " + SF + " ... " + SP + " z. — " + sans)
    res.append(("E13 phrase sans lettre : ❌", re.search(r"❌ A-9001 : ne commence pas", out) is not None))
    # E14 — texte avec une barre « | » entourée d'espaces, sans éléments : la ligne est vue, ❌ quand même
    out = essai("| A-9001 | " + orig + " | coupure | " + queue)
    res.append(("E14 barre entourée d'espaces, sans éléments : ❌", re.search(r"❌ A-9001 : ne commence pas", out) is not None))
    # E11 — le chemin réel : le radar du soir montre le ❌ nouveau, même derrière trois ❌ anciens.
    # Les trois ❌ anciens sont POSÉS ICI (A-9001 à A-9003), devant le nouveau (A-9004) : l'épreuve ne compte plus
    # sur l'état du vrai BACKLOG. Raison (16-10-2026) : les trois ❌ réels de 2026-09 (A-425, A-435, A-471) ont été
    # réparés depuis ; le BACKLOG n'en a plus aucun, le ❌ nouveau tombait parmi les trois premières alertes, et le
    # sabotage S8 (« les trois premières alertes seulement ») ne mordait plus — rouge au certificat du 14-10-2026
    # (10eda9a) et du 16-10-2026 (f5aac6b).
    open(os.path.join(r, "BACKLOG_DECISIONS.md"), "w", encoding="utf-8").write(sauve)
    b = os.path.join(r, "BACKLOG_DECISIONS.md")
    L = sauve.split("\n"); i = max(k for k, l in enumerate(L) if l.startswith("| A-"))
    L[i + 1:i + 1] = ["| A-%d | " % n + sans for n in (9001, 9002, 9003, 9004)]
    open(b, "w", encoding="utf-8").write("\n".join(L))
    p = subprocess.run([sys.executable, os.path.join(r, "programmes", "audit_ecosysteme.py"), r],
                       capture_output=True, text=True, cwd=r, timeout=900)
    res.append(("E11 radar : le ❌ de A-9004 arrive au rapport, derrière trois ❌ posés devant lui",
                re.search(r"❌ A-9004 : ne commence pas", p.stdout + p.stderr) is not None))
    open(b, "w", encoding="utf-8").write(sauve)
    return res


def main():
    choix = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
    bon = True
    for sab in choix:
        d = tempfile.mkdtemp(prefix="trois_elements_")
        try:
            r = os.path.join(d, "r")
            shutil.copytree(DEPOT, r, ignore=shutil.ignore_patterns(".git", "_site_travail", "__pycache__"))
            for f, a, b in SABOTAGES[sab]:
                p = os.path.join(r, f)
                t = open(p, encoding="utf-8").read()
                if a not in t:
                    raise SystemExit(f"SABOTAGE {sab} INAPPLICABLE : ancre absente — l'épreuve ne prouve plus rien")
                open(p, "w", encoding="utf-8").write(t.replace(a, b, 1))
            res = epreuves(r)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        rouges = [n for n, ok in res if not ok]
        print(f"== {sab} : {len(res) - len(rouges)} vertes, {len(rouges)} rouges")
        for n in rouges:
            print("     ROUGE " + n)
        if sab == "Z0" and rouges:
            bon = False
        if sab != "Z0" and not rouges:
            print(f"     ⚠ LE SABOTAGE {sab} NE FAIT RIEN ROUGIR : épreuve sans dents")
            bon = False
    print("VERDICT :", "tout est conforme" if bon else "NON CONFORME")
    return 0 if bon else 1


if __name__ == "__main__":
    sys.exit(main())
