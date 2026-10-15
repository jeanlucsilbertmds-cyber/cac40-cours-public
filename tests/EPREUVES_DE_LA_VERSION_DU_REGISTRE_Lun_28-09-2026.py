#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_VERSION_DU_REGISTRE — Lun 28-09-2026 (Paris)
DÉCIDÉ · Rôle : prouver que le pilote annonce la version du registre lue en pied de page, et que l'épreuve a des dents.
Quand l'appeler : avant toute livraison qui touche la lecture du registre dans programmes/claude_FABRIQUER_LE_PILOTE.py (R-755 ②).

À QUOI ÇA SERT. gouvernance/PILOTE.md, lu à chaque début de session, annonçait « version du registre : 4.0 »
pour un registre en v6.8 (A-435 ①, relevé le 19-09-2026 ; encore vrai le 28-09-2026). Le programme prenait le
premier « vN.N » des 400 premiers caractères du registre — c'est-à-dire l'avertissement qui dit que la
version se lit en pied de page, et qui cite « v4.0 » comme contre-exemple. Réparé : la version se lit sur la
dernière occurrence, dans tout le texte, du titre du registre suivi d'une virgule et de sa version
(« REGISTRE DES RÈGLES …, vN.N ») — et non
sur la dernière ligne non vide, première réparation, cassée par le relecteur parce qu'une ligne posée après le
pied de page la trompait (texte corrigé le 30-09-2026, A-495 (j)). Calibré sur l'histoire du registre au dépôt,
le 28-09-2026 : ses six dernières versions enregistrées
portent en pied de page v6.8, v6.8, v6.8, v6.8, v6.7, v6.6.

LES ÉPREUVES, sur une copie du dépôt dont le registre est remplacé : E1, un registre qui cite « v4.0 » en tête
et porte « v9.9 » en pied de page → le pilote annonce 9.9 ; E2, un pied de page sans version → « ? », jamais
un chiffre pris ailleurs ; E3, une annexe citant « v5.3 » et une ligne de contrôle du garde-fou posées
après le pied → 9.9 ; E4, un ancien pied de page « …, v1.0 » cité plus haut dans le texte → 9.9, la dernière
occurrence (ajoutée le 30-09-2026 : aucune épreuve ne posait deux occurrences, relecteur). S1 remet la lecture des
400 premiers caractères ; S2, celle de la dernière ligne non vide (première réparation, cassée par le relecteur :
une ligne posée après le pied la trompait) ; S3 prend la première occurrence au lieu de la dernière.

USAGE : python3 tests/EPREUVES_DE_LA_VERSION_DU_REGISTRE_Lun_28-09-2026.py <racine du dépôt> [--saboter]
CODE : 0 si Z0 est vert et, avec --saboter, si chaque sabotage fait rougir au moins une épreuve ; 1 sinon.
"""
import os, re, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
PIL = "programmes/claude_FABRIQUER_LE_PILOTE.py"
SABOTAGES = {
    "Z0": [],
    "S1_quatre_cents_premiers_caracteres": [(PIL, '        c["version du registre"] = _pieds[-1] if _pieds else "?"',
                                             '        c["version du registre"] = (re.findall(r"v(\\d+\\.\\d+)", t[:400]) or ["?"])[0]')],
    "S2_derniere_ligne_non_vide": [(PIL, '        c["version du registre"] = _pieds[-1] if _pieds else "?"',
                                    '        c["version du registre"] = (re.findall(r"\\bv(\\d+\\.\\d+)\\b", [x for x in t.split("\\n") if x.strip()][-1]) or ["?"])[0]')],
    # S3 (relecteur du 30-09-2026) : la PREMIÈRE occurrence du titre suivi d'une version, au lieu de la dernière.
    "S3_premiere_occurrence": [(PIL, '        c["version du registre"] = _pieds[-1] if _pieds else "?"',
                                '        c["version du registre"] = _pieds[0] if _pieds else "?"')],
}
TETE = ("# REGISTRE DES RÈGLES DE L'ÉCOSYSTÈME CAC 40\n>\n> LA VERSION SE LIT EN PIED DE PAGE. Corrigé le 13-09-2026 : "
        "cette ligne portait « v4.0 » quand le pied de page portait « v4.4 ».\n\n- **R-722** — texte.\n")


def version(sab, pied):
    d = tempfile.mkdtemp(prefix="version_registre_")
    try:
        r = os.path.join(d, "r")
        shutil.copytree(DEPOT, r, ignore=shutil.ignore_patterns(".git", "_site_travail", "__pycache__"))
        for f, a, b in SABOTAGES[sab]:
            p = os.path.join(r, f)
            t = open(p, encoding="utf-8").read()
            assert t.count(a) == 1, (sab, a[:50])
            with open(p, "w", encoding="utf-8") as h:
                h.write(t.replace(a, b))
        with open(os.path.join(r, "gouvernance", "REGISTRE_REGLES.md"), "w", encoding="utf-8") as h:
            h.write(TETE + "\n\n" + pied + "\n\n")
        sortie = os.path.join(d, "pilote.md")
        subprocess.run([sys.executable, PIL, ".", sortie], cwd=r, capture_output=True, text=True, timeout=900)
        m = re.search(r"\| version du registre \| \*\*([^*]*)\*\* \|", open(sortie, encoding="utf-8").read()) \
            if os.path.exists(sortie) else None
        return m.group(1) if m else "(pilote non écrit)"
    finally:
        shutil.rmtree(d, ignore_errors=True)


_choix = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
_faute = False
for sab in _choix:
    v1 = version(sab, "*Lun 28-09-2026 03h00 (Paris) — REGISTRE DES RÈGLES DE L'ÉCOSYSTÈME CAC 40, v9.9 · révisé le 28-09-2026*")
    v2 = version(sab, "*Lun 28-09-2026 03h00 (Paris) — REGISTRE DES RÈGLES DE L'ÉCOSYSTÈME CAC 40 · révisé le 28-09-2026*")
    v3 = version(sab, "*Lun 28-09-2026 03h00 (Paris) — REGISTRE DES RÈGLES DE L'ÉCOSYSTÈME CAC 40, v9.9 · révisé le 28-09-2026*"
                      "\n\n## ANNEXE\nancienne version v5.3\n\n<!-- CONTROLE 00b375b816065f80 · 2026-09-28 03:10 Paris -->")
    v4 = version(sab, "Ancien pied de page, cité : « REGISTRE DES RÈGLES DE L'ÉCOSYSTÈME CAC 40, v1.0 »\n\n"
                      "*Lun 28-09-2026 03h00 (Paris) — REGISTRE DES RÈGLES DE L'ÉCOSYSTÈME CAC 40, v9.9 · révisé le 28-09-2026*")
    res = [("E1 pied de page v9.9, tête « v4.0 » : 9.9 annoncé", v1 == "9.9", v1),
           ("E4 ancien pied de page « v1.0 » cité plus haut : 9.9, la dernière occurrence", v4 == "9.9", v4),
           ("E2 pied de page sans version : « ? »", v2 == "?", v2),
           ("E3 annexe « v5.3 » et ligne de contrôle après le pied : 9.9", v3 == "9.9", v3)]
    rouges = [x for x in res if not x[1]]
    vert = sab == "Z0"
    print(f"== {sab} : {len(res) - len(rouges)} vertes, {len(rouges)} rouges" + (
        "  <-- ATTENDU : 0 rouge" if vert and rouges else "  <-- SABOTAGE NON VU" if not vert and not rouges else ""))
    for nom, ok, det in res:
        if not ok:
            print(f"     ROUGE {nom} · annoncé : {det}")
    _faute = _faute or (vert and bool(rouges)) or (not vert and not rouges)
print("VERDICT :", "tout est conforme" if not _faute else "ECHEC — voir ci-dessus")
sys.exit(1 if _faute else 0)
