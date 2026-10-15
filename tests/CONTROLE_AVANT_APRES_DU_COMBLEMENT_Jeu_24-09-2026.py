#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTROLE_AVANT_APRES_DU_COMBLEMENT — Jeu 24-09-2026 (Paris)

À QUOI ÇA SERT : prouver, ligne entière de huit champs, que le comblement du trou de
juillet (A-473) n a touché aucune ligne ancienne du maître et n a ajouté que celles du
témoin. Compare la version officielle d'avant la fusion du comblement (6caf152^1) à la version présente.
Lecture seule.

USAGE : depuis la racine du dépôt, python3 tests/CONTROLE_AVANT_APRES_DU_COMBLEMENT_Jeu_24-09-2026.py
"""
import csv,io,subprocess,collections,sys
sys.path.insert(0,'programmes'); from TENIR_L_HISTORIQUE import cle_valeur
# LA VERSION D'AVANT EST FIXE (28-09-2026) : 6caf152^1, la version officielle juste avant la fusion du
# comblement du 25-09-2026. « origin/main » porte le comblement depuis la fusion, et la comparaison
# ne comparait plus rien (b et e rendaient 406 et 0 attendu 406).
AVANT_COMBLEMENT="6caf152^1"
if subprocess.run(["git","cat-file","-e",AVANT_COMBLEMENT+"^{commit}"],capture_output=True).returncode!=0:
    print(f"ARRÊT — la version {AVANT_COMBLEMENT} est absente (clone superficiel ?) : lancer « git fetch --unshallow » "
          "ou cloner sans --depth. Rien n'a été comparé."); sys.exit(2)
anc=subprocess.run(["git","show",AVANT_COMBLEMENT+":donnees/cours_maitre.csv"],capture_output=True,check=True).stdout.decode("utf-8-sig")
A=[tuple(r) for r in csv.reader(io.StringIO(anc))][1:]
N=[tuple(r) for r in csv.reader(open("donnees/cours_maitre.csv",encoding="utf-8-sig"))][1:]
# les séances versées APRÈS la version d'avant ne sont pas le comblement : on ne compare que
# jusqu'à sa dernière séance, sinon chaque soir nouveau ajouterait des lignes « hors témoin »
N=[r for r in N if r[1]<=max(x[1] for x in A)]
T=[tuple(r) for r in csv.reader(open("temoins/TEMOIN_EURONEXT_TROU_2026-07-13_AU_2026-07-30.csv",encoding="utf-8"))][1:]
print("  lignes : ancien",len(A),"· nouveau",len(N),"· témoin",len(T),"· nouveau - ancien =",len(N)-len(A))
print("  (a) lignes anciennes absentes ou modifiées dans le nouveau :",len(set(A)-set(N)))
print("  (b) lignes nouvelles qui ne sont pas celles du témoin :",len((set(N)-set(A))^set(T)))
print("      doublons dans le nouveau :",len(N)-len(set(N)))
par=collections.Counter(r[1] for r in N if "2026-07-10"<=r[1]<="2026-07-31")
print("  (c) valeurs par séance :"," · ".join(f"{d[8:]}-{d[5:7]} {n}" for d,n in sorted(par.items())))
print("  (d) par source :"," · ".join(f"{k} {v}" for k,v in sorted(collections.Counter(r[7] for r in N).items())))
def trous(rows):
    par=collections.defaultdict(set)
    for r in rows: par[r[1]].add(cle_valeur(r[0]))
    dates=sorted(par); prem={}; der={}
    for d in dates:
        for k in par[d]: prem.setdefault(k,d); der[k]=d
    return sum(1 for d in dates for k in prem if prem[k]<d<der[k] and k not in par[d])
print("  (e) détecteur de trous — version officielle :",trous(A),"(attendu 406) · cette version :",trous(N))
