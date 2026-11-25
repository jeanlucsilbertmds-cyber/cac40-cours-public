#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVE_DE_LA_CARTE_DU_CIRCUIT — Sam 21-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Épreuve COURTE (quelques secondes) de programmes/FABRIQUER_LA_CARTE_DU_CIRCUIT.py, le programme qui
fabrique etudes/CARTE_DU_CIRCUIT.md depuis le seul code (décision de Jean-Luc du 21-11-2026 à 14h36, « 1 », A-963).
Elle prouve que la carte SUIT le code et qu'elle ROUGIT sur un trou, sur le VRAI fichier de tâches (R-732) :
C1 la carte du vrai dépôt nomme chaque programme que le vrai collecte_abc.yml lance (relevé ici par une lecture
indépendante, ligne à ligne, sans YAML), s'ouvre par « FABRIQUÉE — ne pas éditer » et porte les trois marquages
(AUTOMATIQUE pour le soir, À LA MAIN et ATTEND JEAN-LUC pour la moulinette — vrais le 25-11-2026) ; C2 le vrai pas « Calculer la
meteo du marche » retiré du fichier de tâches → la carte change et ne nomme plus METEO_DU_MARCHE.py ; C3 le vrai
programme METEO_DU_MARCHE.py privé de son élément ① → code 1, anomalie nommée ; C4 le même programme renommé → code 1,
« INTROUVABLE » ; C5 le fichier de tâches absent → code 2, rien d'écrit (R-734).
Avec « --saboter », chaque garde du fabricant est retirée à son tour dans une copie (dictionnaire SABOTAGES) : au moins
un cas doit tomber, sinon le cas est une décoration.

① RÔLE — Éprouver le fabricant de la carte sur le vrai circuit, et ses gardes par sabotage.
② CONTEXTE D'APPEL — Le lancement des épreuves de GitHub (tests/LANCEMENT_DES_EPREUVES.json, code « Carte ») ; à la
  main : python3 -B tests/EPREUVE_DE_LA_CARTE_DU_CIRCUIT_Sam_21-11-2026.py <racine> [--saboter].
③ ENTRÉE — La ligne de commande : la racine d'un dépôt (lue, jamais écrite) ; « --saboter » facultatif.
④ CONDITIONS D'ENTRÉE — La racine porte le fabricant, .github/workflows/collecte_abc.yml avec le pas « Calculer la
  meteo du marche », programmes/METEO_DU_MARCHE.py et l'enchaîneur de la moulinette ; module yaml installé.
⑤ SORTIE — Le code de sortie : 0 tous les cas tiennent (et chaque sabotage mord) · 1 un cas tombe ou un sabotage ne
  mord pas · 2 l'épreuve n'a pas pu tourner (cas réel absent de la racine, sabotage inapplicable).
  [rend: 1]
⑥ TRAITEMENT — Une copie jetable des seuls fichiers utiles (.github/workflows, programmes/*.py) ; les cas C1 à C5 ;
  sous --saboter, chaque sabotage appliqué au fabricant de la copie, les cas rejoués, le fabricant remis.
⑦ UNITÉ — —
⑧ POURQUOI — R-731 : tout code est éprouvé, sabotages compris ; R-732 : un cas au moins vient du vrai fichier.
⑨ CE QUI CLOCHE — ① Les cas visent METEO_DU_MARCHE parce que c'est un vrai pas ; s'il quitte le circuit, l'épreuve
  rend 2 et le dit (elle ne se tait pas). ② La lecture indépendante de C1 ne voit, comme le fabricant, que
  « python3 programmes/….py » : une forme de lancement nouvelle échapperait aux deux.
⑩ EFFET — Crée puis efface un dossier temporaire ; n'écrit rien dans la racine reçue.
⑪ TERMINAISON — Sort par sys.exit depuis le bloc final. Un de mes appels peut-il ne pas revenir ? Non : chaque
  lancement du fabricant est borné à DELAI secondes.
  [sort: non]
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

FAB = "programmes/FABRIQUER_LA_CARTE_DU_CIRCUIT.py"
SOIR = ".github/workflows/collecte_abc.yml"
PAS_REEL = "Calculer la meteo du marche"
PROG_REEL = "programmes/METEO_DU_MARCHE.py"
DELAI = 60
SABOTAGES = {
    "S1 element 1 absent ne rougit plus": ('(None if trouves[0] else', '(None if True else'),
    "S2 programme introuvable ne rougit plus": ('"%s : PROGRAMME INTROUVABLE" % chemin', 'None'),
    "S3 les programmes des pas ne sont plus lus": ('"programmes": LANCE.findall(p.get("run") or ""),',
                                                   '"programmes": [],'),
    "S4 une anomalie rend 0": ("return 1 if anomalies else 0", "return 0"),
    "S5 le marquage ATTEND JEAN-LUC n'est plus posé": (
        'return "ATTEND JEAN-LUC" if contexte and MOTIF_ATTEND.search(contexte) else mode_appelant',
        'return mode_appelant'),
    "S6 les étapes de la moulinette ne sont plus lues": ("ordre = [ast.literal_eval(k) for k in n.value.keys]",
                                                         "ordre = []"),
}
MARQUES = ("**AUTOMATIQUE**", "**À LA MAIN**", "**ATTEND JEAN-LUC**")


def lancer(racine, sortie):
    """Lance le fabricant d'une racine. ① RÔLE — Un passage du fabricant. ② CONTEXTE D'APPEL — les cas.
    ③ ENTRÉE — racine, chemin de la carte. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — DEUX valeurs : code, texte de la carte
    (ou None). [rend: 2] ⑥ TRAITEMENT — sous-processus borné. ⑦ UNITÉ — — ⑧ POURQUOI — éprouver le programme tel
    qu'il se lance. ⑨ CE QUI CLOCHE — — ⑩ EFFET — le fabricant écrit la carte. ⑪ TERMINAISON — Rend la main ; un
    dépassement de DELAI lève TimeoutExpired. [sort: non]"""
    r = subprocess.run([sys.executable, "-B", os.path.join(racine, FAB), racine, sortie],
                       capture_output=True, text=True, timeout=DELAI)
    texte = open(sortie, encoding="utf-8").read() if os.path.exists(sortie) else None
    if os.path.exists(sortie):
        os.remove(sortie)
    return r.returncode, texte


def sans_date(texte):
    """Retire la ligne d'horodatage. ① RÔLE — Comparer deux cartes sans l'heure. ② CONTEXTE D'APPEL — C2.
    ③ ENTRÉE — le texte. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : le texte. [rend: 1] ⑥ TRAITEMENT — filtre.
    ⑦ UNITÉ — — ⑧ POURQUOI — l'heure change à chaque passage. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. [sort: non]"""
    return "\n".join(l for l in texte.splitlines() if not l.startswith("Fabriquée le "))


def copie(depuis, vers):
    """Copie les seuls fichiers utiles. ① RÔLE — Une racine jetable. ② CONTEXTE D'APPEL — cas et sabotages.
    ③ ENTRÉE — deux racines. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : `vers`. [rend: 1]
    ⑥ TRAITEMENT — .github/workflows entier, programmes/*.py. ⑦ UNITÉ — — ⑧ POURQUOI — rapide, et rien n'écrit dans la
    racine reçue. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit dans `vers`. ⑪ TERMINAISON — Rend la main. [sort: non]"""
    shutil.copytree(os.path.join(depuis, ".github", "workflows"), os.path.join(vers, ".github", "workflows"))
    os.makedirs(os.path.join(vers, "programmes"))
    for n in os.listdir(os.path.join(depuis, "programmes")):
        if n.endswith(".py"):
            shutil.copy2(os.path.join(depuis, "programmes", n), os.path.join(vers, "programmes", n))
    return vers


def retirer_le_pas(texte):
    """Retire le vrai pas PAS_REEL du fichier de tâches. ① RÔLE — Cas C2. ② CONTEXTE D'APPEL — `cas`.
    ③ ENTRÉE — le YAML. ④ CONDITIONS D'ENTRÉE — le pas y est une fois. ⑤ SORTIE — UNE valeur : le YAML sans le pas.
    [rend: 1] ⑥ TRAITEMENT — de la ligne « - name: PAS_REEL » à la ligne « - name: » suivante. ⑦ UNITÉ — —
    ⑧ POURQUOI — R-732. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main ; lève ValueError.
    [sort: non]"""
    m = re.search(r"^ *- name: %s\n.*?(?=^ *- name: )" % re.escape(PAS_REEL), texte, re.M | re.S)
    if not m:
        raise ValueError("pas réel « %s » introuvable" % PAS_REEL)
    return texte[:m.start()] + texte[m.end():]


def cas(racine, travail):
    """Joue C1 à C5. ① RÔLE — Les cas de l'épreuve. ② CONTEXTE D'APPEL — `main`, puis une fois par sabotage.
    ③ ENTRÉE — la racine éprouvée, un dossier de travail. ④ CONDITIONS D'ENTRÉE — celles de la tête.
    ⑤ SORTIE — UNE valeur : la liste des cas tombés (vide si tout tient). [rend: 1] ⑥ TRAITEMENT — voir la tête.
    ⑦ UNITÉ — — ⑧ POURQUOI — voir la tête. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Écrit dans `travail`.
    ⑪ TERMINAISON — Rend la main ; lève ValueError si un cas réel manque. [sort: non]"""
    faux = []
    sortie = os.path.join(travail, "carte.md")
    yml = open(os.path.join(racine, SOIR), encoding="utf-8").read()
    attendus = set(re.findall(r"python3 \"?(programmes/[A-Za-z0-9_\-]+\.py)", yml))
    if PROG_REEL not in attendus:
        raise ValueError("%s n'est plus lancé par le vrai circuit" % PROG_REEL)
    code, carte = lancer(racine, sortie)
    manquent = sorted(p for p in attendus if carte is None or "`%s`" % p not in carte)
    marques = [m for m in MARQUES if carte is None or m not in carte]
    if code != 0 or carte is None or not carte.startswith("<!-- FABRIQUÉE — ne pas éditer") or manquent or marques:
        faux.append("C1 vrai circuit : code %s, manquent %s, marquages absents %s" % (code, manquent, marques))
    for nom, geste in (("C2", "pas"), ("C3", "role"), ("C4", "renomme"), ("C5", "source")):
        r = copie(racine, os.path.join(travail, nom))
        if geste == "pas":
            open(os.path.join(r, SOIR), "w", encoding="utf-8").write(retirer_le_pas(yml))
        elif geste == "role":
            p = os.path.join(r, PROG_REEL)
            t = open(p, encoding="utf-8").read()
            if not re.search(r"^[ \t]*①[ \t]*R[ÔO]LE", t, re.M):
                raise ValueError("%s ne porte pas d'élément ①" % PROG_REEL)
            open(p, "w", encoding="utf-8").write(re.sub(r"^([ \t]*)①([ \t]*R[ÔO]LE)", r"\1(1)\2", t, flags=re.M))
        elif geste == "renomme":
            os.rename(os.path.join(r, PROG_REEL), os.path.join(r, PROG_REEL[:-3] + "_RENOMME.py"))
        else:
            os.remove(os.path.join(r, SOIR))
        c, t = lancer(r, sortie)
        if geste == "pas" and (c != 0 or t is None or sans_date(t) == sans_date(carte or "") or PROG_REEL in t):
            faux.append("C2 pas retiré : code %s, carte inchangée ou %s encore nommé" % (c, PROG_REEL))
        if geste == "role" and (c != 1 or t is None or "%s : ÉLÉMENT ① RÔLE ABSENT" % PROG_REEL not in t):
            faux.append("C3 élément ① absent : code %s (attendu 1)" % c)
        if geste == "renomme" and (c != 1 or t is None or "%s : PROGRAMME INTROUVABLE" % PROG_REEL not in t):
            faux.append("C4 programme renommé : code %s (attendu 1)" % c)
        if geste == "source" and (c != 2 or t is not None):
            faux.append("C5 source absente : code %s (attendu 2, rien d'écrit)" % c)
    return faux


def main(argv):
    """Point d'entrée. ① RÔLE — voir la tête. ② CONTEXTE D'APPEL — le bloc final. ③ ENTRÉE — voir la tête.
    ④ CONDITIONS D'ENTRÉE — voir la tête. ⑤ SORTIE — UNE valeur : 0, 1 ou 2. [rend: 1] ⑥ TRAITEMENT — voir la tête.
    ⑦ UNITÉ — — ⑧ POURQUOI — voir la tête. ⑨ CE QUI CLOCHE — — ⑩ EFFET — dossier temporaire créé puis effacé.
    ⑪ TERMINAISON — Rend la main. [sort: non]"""
    args = [a for a in argv if not a.startswith("--")]
    options = [a for a in argv if a.startswith("--")]
    if len(args) != 1 or any(o != "--saboter" for o in options):
        print("usage : EPREUVE_DE_LA_CARTE_DU_CIRCUIT_Sam_21-11-2026.py <racine> [--saboter]")
        return 2
    racine = os.path.abspath(args[0])
    tmp = tempfile.mkdtemp(prefix="epreuve_carte_")
    try:
        try:
            faux = cas(racine, os.path.join(tmp, "propre"))
        except (ValueError, OSError, subprocess.TimeoutExpired) as e:
            print("ARRÊT : l'épreuve n'a pas pu tourner : %s: %s" % (type(e).__name__, e))
            return 2
        for f in faux:
            print("TOMBÉ : " + f)
        if faux:
            return 1
        print("C1 à C5 : conformes (vrai circuit, pas retiré, ① absent, programme renommé, source absente).")
        if "--saboter" not in options:
            return 0
        sale = copie(racine, os.path.join(tmp, "sabotee"))
        fab = os.path.join(sale, FAB)
        origine = open(fab, encoding="utf-8").read()
        ne_mord_pas = []
        for i, (nom, (avant, apres)) in enumerate(SABOTAGES.items()):
            if origine.count(avant) != 1:
                print("ARRÊT : sabotage %s inapplicable (motif présent %d fois)" % (nom, origine.count(avant)))
                return 2
            open(fab, "w", encoding="utf-8").write(origine.replace(avant, apres))
            try:
                f_s = cas(sale, os.path.join(tmp, "s%d" % i))
            finally:
                open(fab, "w", encoding="utf-8").write(origine)
            print("%s : %s" % (nom, "MORD (%s)" % f_s[0].split(" :")[0] if f_s else "NE MORD PAS"))
            if not f_s:
                ne_mord_pas.append(nom)
        if ne_mord_pas:
            print("SABOTAGES QUI NE MORDENT PAS : %s" % ne_mord_pas)
            return 1
        print("SABOTAGES JOUÉS : %d sur %d, tous mordent." % (len(SABOTAGES), len(SABOTAGES)))
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
