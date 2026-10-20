"""EPREUVES_DU_DETECTEUR_PAR_L_INDICE_Jeu_08-10-2026.py — Jeu 08-10-2026 (Paris) — épreuves d'un outil d'étude.

① RÔLE — Prouver que le calibrage de etudes/outils/DETECTER_PAR_L_INDICE.py a des dents : chaque sabotage doit le
  faire échouer.
② CONTEXTE D'APPEL — À la main : python3 -I tests/EPREUVES_DU_DETECTEUR_PAR_L_INDICE_Jeu_08-10-2026.py <racine>
  [<fichier de résultats>] ; et chaque soir par la certification (programmes/CERTIFIER_LA_VERSION.py), qui ne
  donne que la racine (depuis le 16-10-2026 : sans relevé demandé, il est écrit dans le dossier temporaire).
③ ENTRÉE — Un ou deux arguments : la racine du dépôt ; le chemin du relevé à écrire, facultatif.
④ CONDITIONS D'ENTRÉE — Le détecteur et ses fichiers d'entrée sont sous la racine.
⑤ SORTIE — AUCUNE valeur rendue : le relevé est écrit et affiché ; une cible de sabotage introuvable lève
  AssertionError. Code de sortie : 0 si le programme tel quel rend 0 et que chaque sabotage mord ; 1 sinon
  (jusqu'au 16-10-2026 il rendait toujours 0, même quand un sabotage ne mordait pas : R-734).
⑥ TRAITEMENT — Pour le programme tel quel, puis pour chaque sabotage de `SAB` : une copie du détecteur, modifiée,
  qui importe les programmes du dépôt ; la lancer ; noter son code de sortie.
⑦ UNITÉ — Des CODES DE SORTIE.
⑧ POURQUOI — Un jeu d'épreuves se sabote contre sa propre correction : un calibrage qui reste vert quand on retire
  ce qu'il teste n'est pas une preuve. Le relevé est écrit par le programme, jamais à la main (R-728).
⑨ CE QUI CLOCHE — Trois sabotages seulement : le seuil, l'écart au maître, le bruit ; le choix des valeurs d'un bloc
  et la règle des signes opposés n'en ont pas.
⑩ EFFET — Écrit le relevé ; écrit des copies dans un dossier temporaire.
⑪ TERMINAISON — Quatre lancements du détecteur, chacun fini ; sort par sys.exit avec le code dit en ⑤.
  [sort: oui]
"""
import subprocess, sys, os, tempfile, datetime, zoneinfo
racine = sys.argv[1]
sortie = sys.argv[2] if len(sys.argv) > 2 else os.path.join(tempfile.mkdtemp(), "RELEVE_DU_DETECTEUR_PAR_L_INDICE.txt")
src = os.path.join(racine, "etudes/outils/DETECTER_PAR_L_INDICE.py")
prog = os.path.abspath(os.path.join(racine, "programmes"))
SAB = {"D1 seuil centuplé": ("if a * b < 0 and score > SEUIL:", "if a * b < 0 and score > 100 * SEUIL:"),
       "D2 écart au maître à 50 %": ("ECART_MAITRE = 0.005", "ECART_MAITRE = 0.5"),
       "D3 bruit décuplé": ("        bruit = statistics.median(abs(x) for x in e) * 1.4826",
                            "        bruit = 10 * statistics.median(abs(x) for x in e) * 1.4826")}
cible_chemin = 'os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "programmes")'
lignes = [f"# Sabotages de etudes/outils/DETECTER_PAR_L_INDICE.py, joués sur des copies le "
          f"{datetime.datetime.now(zoneinfo.ZoneInfo('Europe/Paris')):%d-%m-%Y à %Hh%M} (Paris) par un programme.",
          "# Un sabotage mord quand le code de sortie n'est plus 0 (le calibrage échoue)."]
t = open(src, encoding="utf-8").read()
fautes = 0
for nom, (a, b) in [("Z0 programme tel quel", ("", ""))] + list(SAB.items()):
    s = t.replace(cible_chemin, repr(prog))
    if a:
        assert s.count(a) == 1, nom
        s = s.replace(a, b)
    d = tempfile.mkdtemp(); p = os.path.join(d, "D.py"); open(p, "w", encoding="utf-8").write(s)
    code = subprocess.run([sys.executable, "-I", p, racine], capture_output=True).returncode
    __import__("shutil").rmtree(d, ignore_errors=True)   # chaque copie jetable effacée (relecture du 16-10-2026)
    lignes.append(f"{nom} : code {code}" + ("" if not a else (" — mord" if code else " — NE MORD PAS")))
    fautes += (code != 0) if not a else (code == 0)
open(sortie, "w", encoding="utf-8").write("\n".join(lignes) + "\n")
print("\n".join(lignes))
print(f"relevé : {sortie}")
print("VERDICT : " + ("tout est conforme" if not fautes else f"NON CONFORME — {fautes} faute(s)"))
sys.exit(1 if fautes else 0)
