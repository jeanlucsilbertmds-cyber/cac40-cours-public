#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DES_FRAIS_DU_HASARD — Lun 28-09-2026 (Paris)
DÉCIDÉ · Rôle : prouver que le hasard de référence du juge des stratégies paie les mêmes frais que la stratégie qu'il juge, et que l'épreuve a des dents.
Quand l'appeler : avant toute livraison qui touche etalon_hasard dans programmes/MODULE_JUGEMENT.py,
ou pnl_net et frais_ordre dans programmes/MODULE_POSITIONS.py (R-755 ②).

À QUOI ÇA SERT. Les frais se calculent à UN SEUL endroit, MODULE_POSITIONS (`frais_ordre`, qui lit depuis le
29-10-2026 le barème daté `donnees/BAREME_FRAIS.csv`, courtage et taxe sur les transactions financières, A-550 ;
jusque-là un taux unique de 0,15 % par ordre, MODULE_POSITIONS.FRAIS_TAUX), et tout autre programme l'APPELLE. Le hasard de référence du juge des stratégies
(MODULE_JUGEMENT.etalon_hasard) retranchait pourtant un forfait de 300 € écrit chez lui : sur un
aller-retour de 100 à 104 € avec 100 000 € engagés, il comptait 3 700,00 € quand le module des positions
compte 3 694,00 € — +6 € pour le hasard sur ce gain, −3,75 € sur une perte à −2,5 % : l'écart vaut
1,50 € par point de pourcentage de rendement (A-435 ④, relevé le 19-09-2026 ; signe mesuré par le relecteur le 28-09-2026).
Réparé le 28-09-2026 : le hasard appelle mod_positions.pnl_net. Depuis le 28-10-2026, le hasard achète et sort par
JUGE_DES_STRATEGIES.jouer_une_entree, la mécanique même de la stratégie (R-708, superviseur R-759) : les frais sont
ceux de MODULE_POSITIONS.frais_aller_retour (depuis le 29-10-2026, A-550), et le sabotage remet le forfait DANS cette
mécanique.

L'ÉPREUVE joue le hasard sur une série fabriquée au nom de Bouygues (valeur taxée en 2025 : depuis A-550, une
valeur inconnue de la liste des valeurs taxées arrête le calcul, à juste titre), où chaque tirage achète à 100 €
au premier trimestre 2025 et touche l'objectif de +4 % le jour même (R-608) : le gain médian doit valoir EXACTEMENT
MODULE_POSITIONS.pnl_net(100, 104) par opération, soit 4 000 − 150 − 156 = 3 694,00 € — un achat revendu le jour même ne
paie pas la taxe (BOFiP BOI-TCA-FIN-10-10-20151221, § 60 ; A-550, 29-10-2026). Cette épreuve ne voit donc pas la taxe :
c'est `tests/EPREUVES_DU_BAREME_DES_FRAIS_Jeu_29-10-2026.py` qui la garde.
Le sabotage remet le forfait.

USAGE : python3 tests/EPREUVES_DES_FRAIS_DU_HASARD_Lun_28-09-2026.py <racine du dépôt> [--saboter]
CODE : 0 si Z0 est vert et que le sabotage fait rougir l'épreuve ; 1 sinon.
"""
import os, shutil, subprocess, sys, tempfile

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
JUG = "programmes/MODULE_JUGEMENT.py"
SABOTAGES = {
    "Z0": [],
    "S1_forfait_de_300": [("programmes/JUGE_DES_STRATEGIES.py",
                           '        f_tot = _far(q, pe, px, v, serie[j]["date"], d_sortie, bareme)["total"]\n',
                           "        f_tot = 300.0\n")],
}
CODE = (
    "import sys; sys.path.insert(0, 'programmes'); import MODULE_JUGEMENT as J, MODULE_POSITIONS as P, JUGE_DES_STRATEGIES as B\n"
    "s = []\n"
    "for k in range(60):\n"
    "    d = '2025-%02d-%02d' % (1 + k // 28, 1 + k % 28)\n"
    "    s.append(dict(date=d, open=100.0, high=104.5, low=99.9, close=100.0))\n"
    "ops = [{'valeur': 'BOUYGUES', 'date_signal': s[k]['date']} for k in range(0, 30, 3)]\n"
    "r = J.etalon_hasard(ops, {'BOUYGUES': s}, ['BOUYGUES'], 0.04, 0.025, 20, P, mode='valeur', n_tirages=3, "
    "entree=lambda v, j: B.jouer_une_entree(v, s, j, 0.04, 0.025, 20, P, None), admis=lambda v, j: B.achat_admis(v, s, j, None))\n"
    "print(round(r['gain_median'], 2), round(len(ops) * P.pnl_net(100.0, 104.0, 'BOUYGUES', '2025-01-02', '2025-01-02'), 2))\n")


def epreuve(sab):
    d = tempfile.mkdtemp(prefix="frais_hasard_")
    try:
        shutil.copytree(DEPOT, os.path.join(d, "r"), ignore=shutil.ignore_patterns(".git", "_site_travail", "__pycache__"))
        r = os.path.join(d, "r")
        for f, a, b in SABOTAGES[sab]:
            p = os.path.join(r, f)
            t = open(p, encoding="utf-8").read()
            assert t.count(a) == 1, (sab, a[:50])
            with open(p, "w", encoding="utf-8") as h:
                h.write(t.replace(a, b))
        x = subprocess.run([sys.executable, "-c", CODE], cwd=r, capture_output=True, text=True, timeout=300)
        mots = (x.stdout.strip().splitlines() or [""])[-1].split()
        ok = x.returncode == 0 and len(mots) == 2 and mots[0] == mots[1]
        return ok, "gain médian du hasard %s · attendu (pnl_net × opérations) %s" % tuple((mots + ["?", "?"])[:2])
    finally:
        shutil.rmtree(d, ignore_errors=True)


_choix = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
_faute = False
for sab in _choix:
    ok, det = epreuve(sab)
    vert = sab == "Z0"
    bon = ok if vert else not ok
    print(f"== {sab} : {'vert' if ok else 'rouge'} {'(attendu)' if bon else '<-- ' + ('ATTENDU VERT' if vert else 'SABOTAGE NON VU')} · {det}")
    _faute = _faute or not bon
print("VERDICT :", "tout est conforme" if not _faute else "ECHEC — voir ci-dessus")
sys.exit(1 if _faute else 0)
