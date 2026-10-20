#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_CIRCUIT_PUBLIC — Jeu 15-10-2026 (Paris). Simulation uniquement.

① RÔLE — Prouver que programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py publie TOUT le code que les circuits publics
  exécutent (programmes, code des épreuves, fichier de lancement), et rien des données des épreuves ; que les
  deux circuits publics (circuit du soir, certification) refusent de tourner si un seul fichier de code diffère
  entre le dépôt privé et le dépôt public, ou n'existe que d'un côté ; et que chaque épreuve a des dents.
② CONTEXTE D'APPEL — À la main, avant toute livraison qui touche programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py (R-731) :
  python3 tests/EPREUVES_DU_CIRCUIT_PUBLIC_Jeu_15-10-2026.py <racine du dépôt privé> [--saboter]
③ ENTRÉE — La racine du dépôt privé (ses vrais programmes, ses vraies épreuves, ses vrais fichiers de données).
④ CONDITIONS D'ENTRÉE — Le module yaml (PyYAML) s'importe : sans lui, l'épreuve s'arrête (code 2).
⑤ SORTIE — UNE valeur : le code de sortie — 0 si Z0 est vert et, avec --saboter, si chaque sabotage fait rougir
  l'épreuve ; 1 sinon ; 2 si un sabotage ne s'applique plus ou si yaml manque.
  [rend: 1]
⑥ TRAITEMENT — Pour Z0 puis pour chaque sabotage : copier le dépôt (sans .git), y appliquer le sabotage, lancer le
  fabricant vers un faux clone public qui porte un programme et une épreuve « seulement au public », puis :
  E1 chaque fichier de code du privé arrive, identique, au public, chaque fiche de circuit du privé arrive,
     identique, sous circuits_du_prive/, et aucun fichier de données des épreuves n'y arrive ; E2 ce qui n'existe qu'au public est retiré ; E3 le circuit de la certification se lit (YAML) et ne se
     déclenche ni sur une proposition de modification (pull_request, pull_request_target) ni sur un commentaire
     (issue_comment) ni sur un autre circuit (workflow_run) — les seuls déclenchements qui donnent les secrets du
     dépôt à un inconnu ; et, dans les deux circuits, aucun pas qui tourne après un échec (« always() », « != success »)
     ne le fait sur un code non posé, sauf les pas en bash qui ne lancent que git (relecture du 15-10-2026, A3) ;
     E4 son pas « poser le code », EXÉCUTÉ par bash -e dans un espace fabriqué : vert quand
     tout est identique, rouge sur un programme différent, une épreuve seulement au privé, une épreuve seulement au
     public, un programme seulement au privé, un fichier de lancement différent, emp.py différent, un outil
     d'études différent ou seulement au privé, un lien symbolique, un programme caché (« .x.py ») seulement au privé,
     une fiche de circuit du privé modifiée, ou présente d'un seul côté (cassure L de Cowork, 15-10-2026 : une épreuve
     publiée exécute un pas écrit dans une fiche du privé) ;
     et, quand il passe, plus aucun code privé non publié ne reste sur la machine (un fichier d'archives/, un
     sous-dossier de programmes/, un paquet compilé programmes/COMMUN/__init__.pyc, que Python préférerait à
     COMMUN.py — relecture du 15-10-2026, A1) ; E5 le pas « poser les
     programmes » du circuit du soir, exécuté de même : vert quand tout est identique, rouge sur un programme
     seulement au privé et sur un programme différent ; E6 chaque logiciel que le code publié cherche par
     shutil.which (relevé dans le code : pdftotext, soffice, libreoffice le 16-10-2026) est vérifié par
     « command -v » dans un pas placé avant la certification (ajouté le 16-10-2026 : pdftotext et soffice
     manquaient à la machine de GitHub, trois épreuves rouges au certificat f5aac6b).
⑦ UNITÉ — —
⑧ POURQUOI — Décision de Jean-Luc du 08-10-2026 (A-543 : « Non pas question de prendre ces risques ») : un dépôt
  public ne doit pas exécuter le code du dépôt privé. Décision du 12-10-2026 à 16h46 (« Oui, construire ») et
  ordre du 15-10-2026 à 08h36 (A-580, A-576) : la certification passe au dépôt public en y publiant tout le code
  qu'elle exécute. Ce qui garantit qu'aucun code privé ne tourne au public, ce sont deux choses : le fabricant
  publie TOUS les fichiers de code, et les pas « poser » refusent tout écart, dans les deux sens. Une épreuve qui
  reste verte quand on retire ce qu'elle teste n'est pas une preuve (R-731).
⑨ CE QUI CLOCHE — E4 et E5 exécutent le texte des pas extrait du YAML, pas le circuit sur une machine de GitHub :
  les actions de clonage (actions/checkout) ne sont pas jouées. Le passage réel reste à faire, à la main, après
  la publication (A-576 ③).
⑩ EFFET — Écrit dans des dossiers jetables, effacés à la fin ; lance des processus.
⑪ TERMINAISON — Rend la main ; chaque processus est borné (120 secondes pour le fabricant, 60 pour un pas).
  [sort: oui]
"""
import ast
import os
import re
import shutil
import subprocess
import sys
import tempfile

try:
    import yaml
except ImportError:
    print("ARRÊT : le module yaml (PyYAML) manque")
    sys.exit(2)

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
FAB = "programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py"
CERT = ".github/workflows/certifier_la_version.yml"
SOIR = ".github/workflows/circuit_du_soir.yml"
SABOTAGES = {
    "Z0": [],
    "S1_certif_sans_controle_absent_du_public": [(FAB,
        '              [ -f "_code/$d/$n" ] || D="$D $d/$n(absent-du-public)"\n', '              true\n')],
    "S2_certif_sans_controle_absent_du_prive": [(FAB,
        'if [ ! -f "$d/$n" ]; then D="$D $d/$n(absent-du-prive)"; elif ! cmp',
        'if false; then true; elif [ -f "$d/$n" ] && ! cmp')],
    "S3_epreuves_non_publiees": [(FAB, 'DOSSIERS_DE_CODE = ("", "programmes", "tests", "etudes/outils")',
                                  'DOSSIERS_DE_CODE = ("", "programmes", "etudes/outils")')],
    "S9_outils_non_publies": [(FAB, 'DOSSIERS_DE_CODE = ("", "programmes", "tests", "etudes/outils")',
                               'DOSSIERS_DE_CODE = ("", "programmes", "tests")')],
    "S10_racine_non_publiee": [(FAB, 'DOSSIERS_DE_CODE = ("", "programmes", "tests", "etudes/outils")',
                                'DOSSIERS_DE_CODE = ("programmes", "tests", "etudes/outils")')],
    "S11_code_prive_non_efface": [(FAB, "[^/]+[.]py$' | xargs -0 -r rm -f\n", "[^/]+[.]py$' | xargs -0 -r true\n")],
    "S12_liens_admis": [(FAB, '          [ -z "$L" ] || D="$D liens-symboliques:$L"\n', '')],
    "S14_code_compile_non_efface": [(FAB, '''grep -zE "($X)$" | xargs -0 -r rm -f''', '''grep -zE "($X)$" | xargs -0 -r true''')],
    "S15_fichiers_caches_non_vus": [(FAB, "            done < <(find \"$d\" -maxdepth 1 -name '*.py' -type f -print0)",
                                     "            done < <(find \"$d\" -maxdepth 1 -name '[!.]*.py' -type f -print0)")],
    "S16_verdict_sur_code_non_pose": [(FAB, "        if: ${{ !cancelled() && steps.poser_le_code.outcome == 'success' && steps.certifier.outcome != 'success' }}",
                                       "        if: steps.certifier.outcome != 'success'")],
    "S17_pas_final_sur_code_non_pose": [(FAB, '''"        if: ${{ always() && steps.poser_les_programmes.outcome == 'success' }}\\n")''',
                                         '''"        if: always()\\n")''')],
    "S18_fiches_non_comparees": [(FAB, '''elif ! cmp -s "$f" ".github/workflows/$n"; then D="$D fiche:$n"; fi''',
                                  '''else true; fi''')],
    "S19_fiches_non_publiees": [(FAB, "    d = os.path.join(prive, FICHES_PRIVEES)\n    if not os.path.isdir(d):\n        return []\n",
                                 "    return []\n")],
    "S13_racine_non_comparee": [(FAB, "          for d in . programmes tests etudes/outils; do\n            while IFS",
                                 "          for d in programmes tests etudes/outils; do\n            while IFS")],
    "S4_rien_n_est_retire": [(FAB, "        os.remove(os.path.join(public, f))\n", "        pass\n")],
    "S5_soir_sans_controle_absent_du_public": [(FAB,
        '            [ -f "_code/programmes/$n" ] || D="$D $n(absent-du-public)"\n', '            true\n')],
    "S6_lancement_non_compare": [(FAB,
        '          cmp -s _code/tests/LANCEMENT_DES_EPREUVES.json tests/LANCEMENT_DES_EPREUVES.json || D="$D tests/LANCEMENT_DES_EPREUVES.json"\n', '')],
    "S7_declenchement_sur_proposition": [(FAB, "  workflow_dispatch:\n  # 21h00", "  workflow_dispatch:\n  pull_request:\n  # 21h00")],
    "S8_donnees_des_epreuves_publiees": [(FAB, 'if f.endswith(".py") and os.path.isfile(os.path.join(d, f))]',
                                          'if os.path.isfile(os.path.join(d, f))]')],
    "S20_sans_lecteur_de_doc": [(FAB, "          command -v soffice >/dev/null || command -v libreoffice >/dev/null || { sudo apt-get update -qq && sudo apt-get install -y -qq --no-install-recommends libreoffice-writer-nogui; }\n", "")],
    "S21_sans_lecteur_de_pdf": [(FAB, "          command -v pdftotext >/dev/null || { sudo apt-get update -qq && sudo apt-get install -y -qq poppler-utils; }\n", "")],
    "S22_logiciel_par_une_variable": [("programmes/COMMUN.py", "\nimport csv\n", "\nimport csv\nimport shutil as _sh_e6\n_x_e6 = 'gs'\n_sh_e6.which(_x_e6)\n")],
    "S23_logiciel_ecrit_autrement": [("programmes/COMMUN.py", "\nimport csv\n", "\nimport csv\nfrom shutil import which as which\nwhich( 'convert' )\n")],
}


def pas(texte_yaml, job, ident):
    """Rend le texte du « run » du pas `ident` du job `job`, lu par yaml.

    ① RÔLE — Extraire le script d'un pas pour l'exécuter tel quel.
    ② CONTEXTE D'APPEL — `epreuve`, pour E4 et E5.
    ③ ENTRÉE — `texte_yaml` : le fichier de circuit · `job` : le nom du job · `ident` : l'id du pas.
    ④ CONDITIONS D'ENTRÉE — Le texte est du YAML valide.
    ⑤ SORTIE — UNE valeur : le script, ou None si le pas manque.
      [rend: 1]
    ⑥ TRAITEMENT — lire le YAML, chercher le pas par son id.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Lire par yaml et non par motif : le script éprouvé est celui que GitHub lirait.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    y = yaml.safe_load(texte_yaml)
    for p in y.get("jobs", {}).get(job, {}).get("steps", []):
        if p.get("id") == ident:
            return p.get("run")
    return None


def jouer(script, prep):
    """Fabrique un espace de travail, y applique `prep`, exécute `script` par bash -e ; rend le code.

    ① RÔLE — Exécuter un pas « poser » sur un cas fabriqué.
    ② CONTEXTE D'APPEL — `epreuve`, une fois par cas de E4 et E5.
    ③ ENTRÉE — `script` : le texte du pas · `prep` : une fonction qui modifie l'espace avant le pas.
    ④ CONDITIONS D'ENTRÉE — bash existe.
    ⑤ SORTIE — DEUX valeurs : le code de sortie du pas ; la liste du code privé non publié encore présent après lui
      (archives/VIEUX.py, programmes/sous/CACHE.py).
      [rend: 2]
    ⑥ TRAITEMENT — créer, à la racine et sous _code/, deux programmes, une épreuve, un fichier de lancement, emp.py,
      un outil d'études et les deux fichiers de circuit, identiques des deux côtés, plus deux fichiers de code privé
      non publiés ; appliquer `prep` ; exécuter ; relever ce qui reste ; effacer.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — `bash -e` : la commande même de GitHub pour un pas, et celle d'ETAPE_MUETTE.py.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit et efface un dossier jetable.
    ⑪ TERMINAISON — Rend la main ; le pas est borné à 60 secondes.
      [sort: non]
    """
    w = tempfile.mkdtemp(prefix="pas_")
    try:
        for d in ("programmes", "tests", "etudes/outils", "archives", "programmes/sous", ".github/workflows", "_code/programmes",
                  "_code/tests", "_code/etudes/outils", "_code/.github/workflows", "_code/circuits_du_prive"):
            os.makedirs(os.path.join(w, d))
        for base in ("", "_code/"):
            for f, c in (("programmes/A.py", "a=1\n"), ("programmes/B.py", "b=2\n"), ("tests/T.py", "t=3\n"),
                         ("tests/LANCEMENT_DES_EPREUVES.json", "{}\n"), ("emp.py", "e=1\n"), ("etudes/outils/O.py", "o=1\n")):
                open(os.path.join(w, base + f), "w").write(c)
        os.makedirs(os.path.join(w, "programmes", "COMMUN"))
        for f in ("archives/VIEUX.py", "programmes/sous/CACHE.py", "programmes/COMMUN/__init__.pyc"):   # code privé non publié
            open(os.path.join(w, f), "w").write("x=1\n")
        for n in ("certifier_la_version.yml", "circuit_du_soir.yml"):
            open(os.path.join(w, "_code/.github/workflows", n), "w").write("x\n")
        for f in (".github/workflows/F.yml", "_code/circuits_du_prive/F.yml"):      # une fiche du privé, publiée à part
            open(os.path.join(w, f), "w").write("pas: 1\n")
        prep(w)
        env = dict(os.environ, RUNNER_TEMP=os.path.join(w, "_temp"))
        x = subprocess.run(["bash", "-e", "-c", script], cwd=w, env=env, capture_output=True, text=True, timeout=60)
        restes = [f for f in ("archives/VIEUX.py", "programmes/sous/CACHE.py", "programmes/COMMUN/__init__.pyc")
                  if os.path.exists(os.path.join(w, f))]
        return x.returncode, restes
    finally:
        shutil.rmtree(w, ignore_errors=True)


def ecrire(chemin, contenu):
    """Rend une fonction qui écrit `contenu` dans `chemin` sous l'espace donné.

    ① RÔLE — Fabriquer un écart. ② CONTEXTE D'APPEL — `epreuve`. ③ ENTRÉE — un chemin relatif, un texte.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : la fonction. [rend: 1] ⑥ TRAITEMENT — fermer sur les deux.
    ⑦ UNITÉ — — ⑧ POURQUOI — Un cas par écart. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun (la fonction rendue écrit).
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    def f(w):
        open(os.path.join(w, chemin), "w").write(contenu)
    return f


def lien_vers_le_prive(w):
    """Pose programmes/L.py en lien vers du code privé, et au public un fichier de même contenu.

    ① RÔLE — Le cas du relecteur du 15-10-2026 (N1) : un programme publié qui est en fait un lien vers un dossier
      privé ; Python mettrait alors ce dossier privé en tête de ses chemins d'import.
    ② CONTEXTE D'APPEL — `epreuve`, un cas de E4. ③ ENTRÉE — `w` : l'espace de travail.
    ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Aucune valeur.
      [rend: 0]
    ⑥ TRAITEMENT — créer un fichier privé qui n'est pas du code (donnees/CIBLE.txt, que rien n'efface), le lien
      programmes/L.py vers lui, et la copie publique de même contenu (la comparaison des contenus passe).
    ⑦ UNITÉ — — ⑧ POURQUOI — Seul le refus des liens arrête ce cas. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans `w`. ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    os.makedirs(os.path.join(w, "donnees"), exist_ok=True)
    open(os.path.join(w, "donnees", "CIBLE.txt"), "w").write("x=1\n")
    os.symlink("../donnees/CIBLE.txt", os.path.join(w, "programmes", "L.py"))
    open(os.path.join(w, "_code", "programmes", "L.py"), "w").write("x=1\n")


def epreuve(sab):
    """Joue E1 à E6 sur une copie du dépôt sabotée par `sab` ; rend (vert ?, détail).

    ① RÔLE — Une passe complète des épreuves. ② CONTEXTE D'APPEL — la boucle principale, une fois par sabotage.
    ③ ENTRÉE — `sab` : le nom du sabotage (Z0 : aucun). ④ CONDITIONS D'ENTRÉE — DEPOT est un dépôt privé.
    ⑤ SORTIE — DEUX valeurs : vrai si tout est conforme ; le détail (les quatre premières fautes).
      [rend: 2]
    ⑥ TRAITEMENT — copier, saboter, fabriquer vers un faux public, confronter E1 à E6.
    ⑦ UNITÉ — — ⑧ POURQUOI — Voir la fiche du fichier. ⑨ CE QUI CLOCHE — Voir la fiche du fichier.
    ⑩ EFFET — Écrit et efface un dossier jetable. ⑪ TERMINAISON — Rend la main ; le fabricant est borné à 120 s.
      [sort: non]
    """
    d = tempfile.mkdtemp(prefix="circuit_public_")
    fautes = []
    try:
        r = os.path.join(d, "prive")
        shutil.copytree(DEPOT, r, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        for f, a, b in SABOTAGES[sab]:
            p = os.path.join(r, f)
            t = open(p, encoding="utf-8").read()
            if t.count(a) != 1:
                return None, f"sabotage inapplicable : ancre absente ou multiple ({a[:50]!r})"
            open(p, "w", encoding="utf-8").write(t.replace(a, b))
        pub = os.path.join(d, "public")
        for x in ("programmes", "tests"):
            os.makedirs(os.path.join(pub, x))
            open(os.path.join(pub, x, "SEULEMENT_AU_PUBLIC.py"), "w").write("x=1\n")
        x = subprocess.run([sys.executable, os.path.join(r, FAB), r, pub], capture_output=True, text=True, timeout=120)
        if x.returncode != 0:
            return False, "le fabricant a rendu %d : %s" % (x.returncode, (x.stdout + x.stderr).strip()[-200:])
        # E1
        for dossier in ("", "programmes", "tests", "etudes/outils"):
            for f in os.listdir(os.path.join(r, dossier)):
                src = os.path.join(r, dossier, f)
                dst = os.path.join(pub, dossier, f)
                if os.path.isdir(src):
                    if dossier and os.path.exists(dst):
                        fautes.append(f"E1 un dossier de données est publié : {dossier}/{f}")
                    continue
                if not dossier and not f.endswith(".py"):
                    continue
                code = f.endswith(".py") or dossier + "/" + f == "tests/LANCEMENT_DES_EPREUVES.json"
                if code and (not os.path.isfile(dst) or open(src, "rb").read() != open(dst, "rb").read()):
                    fautes.append(f"E1 code absent ou différent : {(dossier + '/') if dossier else ''}{f}")
                if not code and os.path.exists(dst):
                    fautes.append(f"E1 donnée publiée : {(dossier + '/') if dossier else ''}{f}")
        # E1 bis — chaque fiche de circuit du privé arrive, identique, sous circuits_du_prive/, et nulle part ailleurs
        for f in os.listdir(os.path.join(r, ".github", "workflows")):
            if f.endswith((".yml", ".yaml")):
                src, dst = os.path.join(r, ".github", "workflows", f), os.path.join(pub, "circuits_du_prive", f)
                if not os.path.isfile(dst) or open(src, "rb").read() != open(dst, "rb").read():
                    fautes.append(f"E1 fiche de circuit absente ou différente : circuits_du_prive/{f}")
        # E2
        for f in ("programmes/SEULEMENT_AU_PUBLIC.py", "tests/SEULEMENT_AU_PUBLIC.py"):
            if os.path.exists(os.path.join(pub, f)):
                fautes.append("E2 non retiré : " + f)
        # E3
        if not os.path.isfile(os.path.join(pub, CERT)):
            return False, "E3 circuit de certification absent"
        cert = open(os.path.join(pub, CERT), encoding="utf-8").read()
        soir = open(os.path.join(pub, SOIR), encoding="utf-8").read()
        y = yaml.safe_load(cert)
        decl = y.get("on", y.get(True)) or {}
        ouverts = [k for k in ("pull_request", "pull_request_target", "issue_comment", "workflow_run") if k in decl]
        if ouverts:
            fautes.append("E3 déclencheur ouvert aux inconnus : " + ", ".join(ouverts))
        # E3 bis — aucun pas qui tourne après un échec n'exécute le code du privé : son « if » exige le code posé
        for nom, texte, job, pose in (("certification", cert, "certifier", "poser_le_code"),
                                      ("soir", soir, "collecte", "poser_les_programmes")):
            for p_ in (yaml.safe_load(texte).get("jobs", {}).get(job, {}).get("steps") or []):
                si = str(p_.get("if", ""))
                if ("always()" in si or "!= 'success'" in si) and p_.get("shell") != "bash" and pose not in si:
                    fautes.append(f"E3 {nom} : le pas « {p_.get('id')} » peut tourner sur un code non posé")
        # E6 — chaque logiciel que le code publié cherche par shutil.which est vérifié (« command -v ») par un pas
        # placé AVANT la certification. Raison : pdftotext et soffice manquaient à la machine de GitHub, trois
        # épreuves ont rougi au premier certificat public (16-10-2026, f5aac6b). Lu dans le code, jamais listé ici.
        # Lu dans l'arbre syntaxique, pas par un motif : « sh.which(…) », « which(…) » importé seul, une espace dans
        # les parenthèses, un second argument (relecture du 16-10-2026, cassure 7). Un nom qui n'est pas écrit en
        # clair (une variable) est une faute : on ne peut pas savoir quoi installer.
        noms = set()
        for dossier in ("", "programmes", "tests", "etudes/outils"):
            for f in os.listdir(os.path.join(r, dossier)):
                if f.endswith(".py") and os.path.isfile(os.path.join(r, dossier, f)):
                    try:
                        arbre = ast.parse(open(os.path.join(r, dossier, f), encoding="utf-8", errors="replace").read())
                    except SyntaxError:
                        continue
                    for n in ast.walk(arbre):
                        if isinstance(n, ast.Call) and (getattr(n.func, "attr", None) == "which"
                                                        or getattr(n.func, "id", None) == "which"):
                            if n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str):
                                noms.add(n.args[0].value)
                            else:
                                fautes.append(f"E6 logiciel cherché par un nom non écrit en clair : {dossier}/{f}, "
                                              f"ligne {n.lineno}")
        etapes = y.get("jobs", {}).get("certifier", {}).get("steps") or []
        rang = next((k for k, p_ in enumerate(etapes) if p_.get("id") == "certifier"), None)
        if rang is None:
            fautes.append("E6 pas « certifier » introuvable")
        else:
            avant = "\n".join(str(p_.get("run", "")) for p_ in etapes[:rang])
            for n in sorted(noms):
                if not re.search(r"command -v %s\b" % re.escape(n), avant):
                    fautes.append(f"E6 logiciel non vérifié avant la certification : {n}")
        # E4
        s = pas(cert, "certifier", "poser_le_code")
        if s is None:
            fautes.append("E4 pas « poser_le_code » introuvable")
        else:
            for nom, prep, attendu in (("identique", lambda w: None, 0),
                                       ("programme différent", ecrire("_code/programmes/A.py", "a=9\n"), 1),
                                       ("épreuve seulement au privé", ecrire("tests/U.py", "u=1\n"), 1),
                                       ("épreuve seulement au public", ecrire("_code/tests/U.py", "u=1\n"), 1),
                                       ("programme seulement au privé", ecrire("programmes/C.py", "c=1\n"), 1),
                                       ("lancement différent", ecrire("_code/tests/LANCEMENT_DES_EPREUVES.json", "[]\n"), 1),
                                       ("racine différente", ecrire("_code/emp.py", "e=9\n"), 1),
                                       ("outil différent", ecrire("_code/etudes/outils/O.py", "o=9\n"), 1),
                                       ("outil seulement au privé", ecrire("etudes/outils/P.py", "p=1\n"), 1),
                                       ("lien symbolique", lien_vers_le_prive, 1),
                                       ("programme caché seulement au privé", ecrire("programmes/.cache.py", "c=1\n"), 1),
                                       ("fiche de circuit privée modifiée", ecrire(".github/workflows/F.yml", "pas: 2\n"), 1),
                                       ("fiche seulement au privé", ecrire(".github/workflows/G.yml", "pas: 1\n"), 1),
                                       ("fiche seulement au public", ecrire("_code/circuits_du_prive/G.yml", "pas: 1\n"), 1)):
                c, restes = jouer(s, prep)
                if (c == 0) != (attendu == 0):
                    fautes.append(f"E4 {nom} : code {c}, attendu {'0' if attendu == 0 else 'non nul'}")
                if c == 0 and restes:
                    fautes.append(f"E4 {nom} : code privé non publié encore présent : {', '.join(restes)}")
        # E5
        s = pas(soir, "collecte", "poser_les_programmes")
        if s is None:
            fautes.append("E5 pas « poser_les_programmes » introuvable")
        else:
            for nom, prep, attendu in (("identique", lambda w: None, 0),
                                       ("programme seulement au privé", ecrire("programmes/C.py", "c=1\n"), 1),
                                       ("programme différent", ecrire("_code/programmes/A.py", "a=9\n"), 1)):
                c, _ = jouer(s, prep)
                if (c == 0) != (attendu == 0):
                    fautes.append(f"E5 {nom} : code {c}, attendu {'0' if attendu == 0 else 'non nul'}")
        return not fautes, ("; ".join(fautes[:4]) if fautes else "E1 à E6 conformes")
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    """Joue Z0, et chaque sabotage avec --saboter ; affiche ; rend le code de sortie.

    ① RÔLE — Voir la fiche du fichier. ② CONTEXTE D'APPEL — La ligne de commande. ③ ENTRÉE — `sys.argv`.
    ④ CONDITIONS D'ENTRÉE — Voir la fiche du fichier. ⑤ SORTIE — UNE valeur : le code de sortie. [rend: 1]
    ⑥ TRAITEMENT — Voir la fiche du fichier. ⑦ UNITÉ — — ⑧ POURQUOI — Voir la fiche du fichier.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — Affiche. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    choix = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
    code = 0
    for sab in choix:
        ok, det = epreuve(sab)
        if ok is None:
            print(f"== {sab} : INAPPLICABLE · {det}")
            code = 2
            continue
        bon = ok if sab == "Z0" else not ok
        print(f"== {sab} : {'vert' if ok else 'rouge'} {'(attendu)' if bon else '<-- ' + ('ATTENDU VERT' if sab == 'Z0' else 'SABOTAGE SANS EFFET')} · {det}")
        if not bon:
            code = max(code, 1)
    print("VERDICT : " + ("tout est conforme" if code == 0 else f"NON CONFORME (code {code})"))
    return code


if __name__ == "__main__":
    sys.exit(main())
