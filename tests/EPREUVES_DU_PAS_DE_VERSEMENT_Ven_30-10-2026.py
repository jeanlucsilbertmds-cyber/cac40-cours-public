#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ÉPREUVES DU PAS DE VERSEMENT — Ven 30-10-2026 (Paris) — le pas `versement` du circuit du soir face aux codes 0, 1, 3.

Simulation uniquement — aucun ordre réel.

① RÔLE — Prouver que le pas `versement` de `.github/workflows/collecte_abc.yml` traite juste chaque code de sortie du
  versement (`programmes/TENIR_L_HISTORIQUE.py`) : 0, le maître est poussé et les alertes d'un soir précédent rangées
  aux archives ; 1, le pas tombe et l'alerte du maître est déposée ; 3 (des lignes neuves mises à part, décision de
  Jean-Luc du 30-10-2026 à 13h55), le pas continue, dit `a_part=1`, pousse le maître ET l'alerte des lignes ; et que le
  pas « Rougir si des lignes de cours ont ete mises a part » rougit le passage, placé après tout pas sans `always()`.
② CONTEXTE D APPEL — Depuis la racine, la racine en argument : par le certificateur (`programmes/CERTIFIER_LA_VERSION.py`)
  et à la main avant toute livraison qui touche ce pas. Avec `--saboter`, chaque sabotage doit faire rougir au moins
  une épreuve.
③ ENTRÉE — `sys.argv[1]` : la racine du dépôt ; `--saboter` facultatif.
④ CONDITIONS D ENTRÉE — `.github/workflows/collecte_abc.yml` sous la racine, avec un pas d'`id` `versement` ; `bash` et
  `git` installés ; le module `yaml` de Python.
⑤ SORTIE — UNE valeur : le code de sortie, 0 si Z0 est vert et, avec `--saboter`, si chaque sabotage rougit ; 1 sinon.
  [rend: 1] Une ligne « == » par jeu, puis le détail des rouges.
⑥ TRAITEMENT — Pour Z0 puis chaque sabotage : lire le fichier du circuit (saboté dans une copie en mémoire), en tirer le
  texte du pas `versement` par son `id` (jamais par des numéros de ligne) ; pour chaque cas, monter un dépôt git
  jetable avec un dépôt distant local, y poser un FAUX versement qui rend le code du cas (et écrit l'alerte des lignes
  si le cas le dit), lancer le pas sous `bash --noprofile --norc -eo pipefail` comme GitHub, et comparer : code du pas,
  sortie `a_part`, fichiers sous `rapports/` et `archives/`, nombre de commits poussés. Puis un cas statique : la
  condition et la place du pas « Rougir ».
  Les cas (ceux du relecteur du 30-10-2026, I4) :
  W1 code 3, alerte écrite : pas 0, `a_part=1`, alerte des lignes au commit poussé.
  W2 code 3, une alerte du maître d'un soir précédent : pas 0, `a_part=1`, alerte du maître rangée aux archives.
  W3 code 0, une alerte des lignes d'un soir précédent : pas 0, pas de `a_part`, alerte rangée aux archives « resolue ».
  W4 code 1, le faux versement ayant écrit l'alerte du maître : le pas tombe (1) et l'alerte du maître est au commit
     poussé (relecteur du 30-10-2026, tour 4 : la fiche le promettait, rien ne le vérifiait).
  Dans W2 et W3, l'archive « resolue » et l'absence de l'alerte se lisent dans le COMMIT POUSSÉ, pas sur le disque :
  une alerte rangée sur le disque mais restée au dépôt alerterait pour toujours (défaut d'A-442).
  W5 code 3 sans alerte écrite : le pas tombe (1) — une mise à part sans alerte ne passe pas en silence.
  W6 code 0, aucune alerte : pas 0, maître poussé.
  W7 statique, une PROPRIÉTÉ lue sur la liste des pas : « Rougir » a `if: always() && steps.versement.outputs.a_part ==
     '1'`, échoue (`exit 1`), et TOUT pas placé après lui porte `always()` (superviseur R-759 du 30-10-2026, tour 3) ;
     et le pas `versement` ne porte pas `continue-on-error` : un code 1 laisserait le détecteur calculer sur des cours
     périmés (relecteur du tour 4).
⑦ UNITÉ — Des codes de sortie et des nombres de commits.
⑧ POURQUOI — Relecteur du 30-10-2026, tour 3, I4 : la partie du code 3 qui vit dans le circuit n'était gardée par
  aucune épreuve ; « -eq 3 » changé en « -eq 4 » laissait un passage VERT avec une valeur mise à part (R-731 : tout code
  écrit ou modifié passe des épreuves avec sabotages).
⑨ CE QUI CLOCHE — W7 cherche « always() » comme une sous-chaîne de la condition : `!always()` passerait (relecteur
  du tour 4, improbable, non réparé). · Le vrai GitHub Actions n'est pas lancé : le `success()` implicite des conditions et l'ordre des pas
  sont lus dans le fichier (W7), pas observés. Le faux versement ne juge rien : ce sont les épreuves du circuit par le
  lecteur et du comblement qui éprouvent le versement lui-même.
⑩ EFFET — Des dossiers temporaires, effacés. N'écrit rien sous la racine.
⑪ TERMINAISON — Chaque pas joué est borné à 60 secondes.
  [sort: oui]
"""
import os, shutil, subprocess, sys, tempfile
import yaml

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
CIRCUIT = os.path.join(DEPOT, ".github", "workflows", "collecte_abc.yml")
SABOTAGES = {
    "Z0": [],
    "W_le_code_3_mal_lu": [('if [ "$VERSE" -eq 3 ]; then', 'if [ "$VERSE" -eq 4 ]; then')],
    "W_a_part_tu": [('            echo "a_part=1" >> "$GITHUB_OUTPUT"\n', "")],
    "W_alerte_des_lignes_non_poussee": [("            git add rapports/ALERTE_LIGNES_MISES_A_PART.md \\\n",
                                         "            true \\\n")],
    "W_alerte_des_lignes_jamais_rangee": [('if [ "$VERSE" -eq 0 ] && [ -f rapports/ALERTE_LIGNES_MISES_A_PART.md ]; then',
                                           'if false; then')],
    "W_le_code_1_accepte": [('[ "$VERSE" -eq 0 ] || [ "$VERSE" -eq 3 ] \\', '[ "$VERSE" -ne 99 ] \\')],
    "W_rougir_sans_always": [("        if: always() && steps.versement.outputs.a_part == '1'",
                              "        if: steps.versement.outputs.a_part == '1'")],
    # Superviseur R-759 du 30-10-2026, tour 3 : remettre « Rougir » AVANT le pas qui le suivait sans always() (I1).
    "W_rougir_avant_un_pas_sans_always": "deplacer",
    # Relecteur du 30-10-2026, tour 4 (SA à SD)
    "W_versement_tolere": [("      - name: Verser la seance du jour dans le fichier maitre\n        id: versement\n",
                            "      - name: Verser la seance du jour dans le fichier maitre\n        id: versement\n        continue-on-error: true\n")],
    "W_alerte_du_maitre_non_poussee": [("                     && git push \\\n                     || echo \"::error::L ALERTE DU FICHIER MAITRE N A PAS PU ETRE DEPOSEE\";",
                                        "                     && true \\\n                     || echo \"::error::L ALERTE DU FICHIER MAITRE N A PAS PU ETRE DEPOSEE\";")],
    "W_alerte_du_maitre_resolue_hors_commit": [('            git add "$RESOLUE" \\\n              && git rm -q --cached --ignore-unmatch rapports/ALERTE_FICHIER_MAITRE.md',
                                                '            true \\\n              && true')],
    "W_alerte_des_lignes_resolue_hors_commit": [('            git add "$RESOLUE" \\\n              && git rm -q --cached --ignore-unmatch rapports/ALERTE_LIGNES_MISES_A_PART.md',
                                                 '            true \\\n              && true')],
}


def deplacer_rougir(t):
    """Remet le pas « Rougir… » juste avant le pas qui le précède — la place qu'il avait avant le 30-10-2026 (I1).

    ① RÔLE — Le sabotage « W_rougir_avant_un_pas_sans_always ». ② CONTEXTE D APPEL — `jeu`. ③ ENTRÉE — `t` : le texte du
    fichier du circuit. ④ CONDITIONS D ENTRÉE — Les pas commencent par « - name: » à six espaces. ⑤ SORTIE — UNE valeur :
    le texte saboté, ou None si le pas est introuvable ou le premier. [rend: 1] ⑥ TRAITEMENT — couper le texte en blocs
    de pas, échanger le bloc « Rougir » avec le précédent. ⑦ UNITÉ — —. ⑧ POURQUOI — R-731 : W7 doit rougir si la faute
    I1 revient. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — —. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    import re
    morceaux = re.split(r"(?m)^(?=      - name: )", t)
    i = next((k for k, m in enumerate(morceaux) if m.startswith("      - name: Rougir si des lignes")), None)
    if i is None or i < 2:
        return None
    morceaux[i - 1], morceaux[i] = morceaux[i], morceaux[i - 1]
    return "".join(morceaux)
GIT = dict(os.environ, GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="commit.gpgsign", GIT_CONFIG_VALUE_0="false")


def jouer(texte_du_pas, code, alerte, prealable):
    """Joue le pas `versement` dans un dépôt jetable, avec un faux versement, et rend ce qu'il a fait.

    ① RÔLE — Un cas W1 à W6. ② CONTEXTE D APPEL — `jeu`. ③ ENTRÉE — `texte_du_pas` : le `run` du pas ; `code` : le code
    rendu par le faux versement ; `alerte` : « lignes » ou « maitre » (l'alerte que le faux écrit), ou faux ; `prealable` : « lignes »,
    « maitre » ou « » (alerte d'un soir précédent posée et commitée). ④ CONDITIONS D ENTRÉE — bash et git installés.
    ⑤ SORTIE — UNE valeur : un dictionnaire (code du pas, sortie, rapports, archives, suivis au commit, commits poussés).
    [rend: 1] ⑥ TRAITEMENT — dépôt distant nu + dépôt de travail, faux versement, pas lancé sous bash -eo pipefail.
    ⑦ UNITÉ — —. ⑧ POURQUOI — Le pas parle git et `$GITHUB_OUTPUT` : il ne se juge qu'en le jouant. ⑨ CE QUI CLOCHE — —.
    ⑩ EFFET — Un dossier temporaire, effacé. ⑪ TERMINAISON — Borné à 60 secondes. [sort: non]
    """
    d = tempfile.mkdtemp(prefix="pas_versement_")
    try:
        nu, ws = os.path.join(d, "distant.git"), os.path.join(d, "ws")
        run = lambda c, cwd: subprocess.run(c, cwd=cwd, shell=True, env=GIT, capture_output=True, text=True)
        run(f"git init -q --bare {nu} && git init -q -b main {ws}", d)
        os.makedirs(os.path.join(ws, "programmes")); os.makedirs(os.path.join(ws, "donnees"))
        os.makedirs(os.path.join(ws, "rapports"))
        open(os.path.join(ws, "donnees", "cours_maitre.csv"), "w").write("v,d\n")
        if prealable == "lignes":
            open(os.path.join(ws, "rapports", "ALERTE_LIGNES_MISES_A_PART.md"), "w").write("ancienne\n")
        if prealable == "maitre":
            open(os.path.join(ws, "rapports", "ALERTE_FICHIER_MAITRE.md"), "w").write("ancienne\n")
        open(os.path.join(ws, "programmes", "TENIR_L_HISTORIQUE.py"), "w").write(
            "import sys\n"
            + ("open('rapports/ALERTE_LIGNES_MISES_A_PART.md','w').write('neuve\\n')\n" if alerte == "lignes" else "")
            + ("open('rapports/ALERTE_FICHIER_MAITRE.md','w').write('neuve\\n')\n" if alerte == "maitre" else "")
            + "open('donnees/cours_maitre.csv','a').write('x,y\\n')\n"
            + f"sys.exit({code})\n")
        run(f"git remote add origin {nu} && git add -A && git -c user.name=a -c user.email=a@a commit -qm init "
            "&& git push -q -u origin main", ws)
        sortie = os.path.join(d, "sortie.txt")
        open(sortie, "w").close()
        pas = os.path.join(d, "pas.sh")
        open(pas, "w").write(texte_du_pas)
        env = dict(GIT, GITHUB_OUTPUT=sortie, GITHUB_WORKSPACE=ws)
        try:
            p = subprocess.run(["bash", "--noprofile", "--norc", "-eo", "pipefail", pas], cwd=ws, env=env,
                               capture_output=True, text=True, timeout=60)
            c = p.returncode
        except subprocess.TimeoutExpired:
            c = 124
        suivis = run("git ls-tree -r --name-only main", nu).stdout.split()     # ce qui est POUSSÉ
        return dict(pas=c, sortie=open(sortie).read().split(),
                    rapports=sorted(os.listdir(os.path.join(ws, "rapports"))),
                    archives=sorted(os.listdir(os.path.join(ws, "archives"))) if os.path.isdir(os.path.join(ws, "archives")) else [],
                    suivis=[s for s in suivis if s.startswith(("rapports/", "archives/"))],
                    pousses=len(run("git log --oneline main", nu).stdout.split("\n")) - 1)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def jeu(sab):
    """Joue W1 à W7 sur le fichier du circuit, saboté ou non, et rend la liste des rouges.

    ① RÔLE — Un jeu complet. ② CONTEXTE D APPEL — Le programme principal, une fois par jeu. ③ ENTRÉE — `sab` : une clé
    de SABOTAGES. ④ CONDITIONS D ENTRÉE — Chaque texte de sabotage existe une seule fois dans le fichier du circuit.
    ⑤ SORTIE — UNE valeur : la liste des rouges, ou None si le sabotage ne s'applique pas. [rend: 1]
    ⑥ TRAITEMENT — saboter le texte en mémoire, en tirer le pas `versement` par son id, jouer les cas.
    ⑦ UNITÉ — —. ⑧ POURQUOI — R-731. ⑨ CE QUI CLOCHE — —. ⑩ EFFET — Ceux de `jouer`. ⑪ TERMINAISON — Rend la main.
    [sort: non]
    """
    t = open(CIRCUIT, encoding="utf-8").read()
    if SABOTAGES[sab] == "deplacer":
        t = deplacer_rougir(t)
        if t is None:
            return None
    else:
        for a, b in SABOTAGES[sab]:
            if t.count(a) != 1:
                return None
            t = t.replace(a, b)
    pas_ = [p for job in yaml.safe_load(t)["jobs"].values() for p in job.get("steps", [])]
    v = next(p for p in pas_ if p.get("id") == "versement")["run"]
    rouges = []

    def dire(nom, ok, det):
        if not ok:
            rouges.append(f"{nom} · {det}")
    r = jouer(v, 3, "lignes", "")
    dire("W1 code 3 : pas 0, a_part=1, alerte des lignes poussée", r["pas"] == 0 and "a_part=1" in r["sortie"]
         and "rapports/ALERTE_LIGNES_MISES_A_PART.md" in r["suivis"] and r["pousses"] == 2, r)
    r = jouer(v, 3, "lignes", "maitre")
    dire("W2 code 3 et alerte du maître d'un soir précédent : rangée aux archives, au commit poussé", r["pas"] == 0
         and "a_part=1" in r["sortie"] and any(a.startswith("archives/ALERTE_FICHIER_MAITRE_resolue_") for a in r["suivis"])
         and "rapports/ALERTE_FICHIER_MAITRE.md" not in r["suivis"], r)
    r = jouer(v, 0, False, "lignes")
    dire("W3 code 0 et alerte des lignes d'un soir précédent : rangée aux archives, pas de a_part", r["pas"] == 0
         and "a_part=1" not in r["sortie"] and "rapports/ALERTE_LIGNES_MISES_A_PART.md" not in r["suivis"]
         and any(a.startswith("archives/ALERTE_LIGNES_MISES_A_PART_resolue_") for a in r["suivis"]), r)
    r = jouer(v, 1, "maitre", "")
    dire("W4 code 1 : le pas tombe, l'alerte du maître est poussée", r["pas"] == 1 and r["pousses"] == 2
         and "rapports/ALERTE_FICHIER_MAITRE.md" in r["suivis"], r)
    r = jouer(v, 3, False, "")
    dire("W5 code 3 sans alerte écrite : le pas tombe", r["pas"] != 0, r)
    r = jouer(v, 0, False, "")
    dire("W6 code 0 : pas 0, maître poussé", r["pas"] == 0 and r["pousses"] == 2 and "a_part=1" not in r["sortie"], r)
    noms = [p.get("name", "") for p in pas_]
    i = next((k for k, p in enumerate(pas_) if p.get("id") == "rougir_si_des_lignes_mises_a_part"), None)
    ok = i is not None and str(pas_[i].get("if", "")).replace(" ", "") == "always()&&steps.versement.outputs.a_part=='1'" \
        and "exit 1" in pas_[i].get("run", "") \
        and all("always()" in str(p.get("if", "")) for p in pas_[i + 1:]) \
        and "continue-on-error" not in next(p for p in pas_ if p.get("id") == "versement")
    dire("W7 « Rougir » : condition always(), échoue, et aucun pas sans always() après lui", ok,
         noms[i + 1:] if i is not None else "pas introuvable")
    return rouges


_choix = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
_faute = False
for sab in _choix:
    rg = jeu(sab)
    if sab == "Z0":
        bon = rg == []
        print(f"== Z0 : {'vert (attendu)' if bon else str(len(rg)) + ' rouge(s) <-- ATTENDU VERT'}")
    else:
        bon = bool(rg)
        etat = "INAPPLICABLE" if rg is None else ("vert" if not rg else f"{len(rg)} rouge(s)")
        print(f"== {sab} : {etat} {'(attendu)' if bon else '<-- SABOTAGE NON VU OU INVALIDE'}")
    if rg and (sab == "Z0"):
        print("\n".join("  " + x for x in rg))
    _faute = _faute or not bon
print("VERDICT :", "tout est conforme" if not _faute else "ECHEC — voir ci-dessus")
sys.exit(1 if _faute else 0)
