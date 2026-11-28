#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REFAIRE_LE_TEMOIN_OBS.py — Sam 28-11-2026 (Paris). Outil d'essai du lot W2f, sur une branche d'essai seulement.
Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Le lot L1CORR2 (point ③ de sa note) demande de refaire le témoin de résultats de C5E10-OBS-V1 sur la
partie de réglage : rejouer les 2 695 versions de COMBINATOIRE_C5E10-OBS-V1_E01.csv (fiche 2024-01-02 → 2026-07-10,
aucune séance de 2000-2023) par JOUER_LES_VERSIONS, puis copier le fichier de résultats comme témoin. Sur GitHub, une
épreuve longue ne rend que sa sortie : ce programme joue UNE tranche k/N et écrit le fichier de la tranche sur la
sortie, entre deux repères, avec son empreinte ; le Chat les assemble ensuite par « JOUER_LES_VERSIONS.py --assembler ».

① RÔLE — Jouer la tranche k/N de la combinatoire E01 de C5E10-OBS-V1, sans l'ancien témoin, et rendre le fichier.
② CONTEXTE D'APPEL — Les épreuves longues TemoinT0, TemoinT1, TemoinT2 de la branche d'essai travail-r505-W2f-L1CORR2x.
③ ENTRÉE — argv[1] : la copie jouée (sans .git) ; argv[2] : k ; argv[3] : N.
④ CONDITIONS D'ENTRÉE — La copie n'a pas de .git ; elle porte la combinatoire et JOUER_LES_VERSIONS.py.
⑤ SORTIE — UNE valeur, le code : celui de JOUER (0 : la tranche est écrite sur la sortie) ; 2 si rien n'a pu tourner.
[rend: rien]
⑥ TRAITEMENT — ① l'ancien témoin de la COPIE est renommé (sinon JOUER le dit « non comparable » et s'arrête : c'est
  lui qu'on refait) · ② JOUER --tranche=k/N, cours par défaut (le fichier maître) · ③ ses dernières lignes, puis le
  fichier entre « === TRANCHE … === » et « === FIN DE LA TRANCHE === », avec son sha256.
⑦ UNITÉ — —
⑧ POURQUOI — Point ③ de la note de L1CORR2 ; mesure de W2f (2,6 s par version sur 20 ans) : en trois tranches.
⑨ CE QUI CLOCHE — Le témoin ne vit que dans la copie ; le vrai dépôt n'est jamais touché ici.
⑩ EFFET — Renomme un fichier de la copie ; écrit un fichier de tranche dans un dossier temporaire ; affiche.
⑪ TERMINAISON — Sort par sys.exit ; JOUER est borné à 18 000 s.
[sort: oui]
"""
import hashlib
import os
import subprocess
import sys
import tempfile

TEMOIN = os.path.join("donnees", "combinatoires", "TEMOIN_RESULTATS_C5E10-OBS-V1_E01.csv")
COMB = os.path.join("donnees", "combinatoires", "COMBINATOIRE_C5E10-OBS-V1_E01.csv")

copie, k, n = os.path.abspath(sys.argv[1]), sys.argv[2], sys.argv[3]
if os.path.lexists(os.path.join(copie, ".git")):
    print("ARRÊT : %s porte .git" % copie)
    sys.exit(2)
if os.path.exists(os.path.join(copie, TEMOIN)):
    os.replace(os.path.join(copie, TEMOIN), os.path.join(copie, TEMOIN + ".ancien_dans_la_copie"))
sortie = os.path.join(tempfile.mkdtemp(prefix="temoin_obs_"), "tranche_%s.csv" % k)
p = subprocess.run([sys.executable, "-B", os.path.join(copie, "programmes", "JOUER_LES_VERSIONS.py"), copie,
                    os.path.join(copie, COMB), sortie, "--tranche=%s/%s" % (k, n)], cwd=copie, capture_output=True,
                   text=True, timeout=18000)
print("\n".join((p.stdout + p.stderr).strip().split("\n")[-12:]))
print("CODE DE JOUER : %d" % p.returncode)
if p.returncode == 0:
    texte = open(sortie, encoding="utf-8", newline="").read()
    print("=== TRANCHE %s/%s sha256=%s ===" % (k, n, hashlib.sha256(texte.encode("utf-8")).hexdigest()))
    sys.stdout.write(texte)
    print("=== FIN DE LA TRANCHE ===")
sys.exit(p.returncode)
