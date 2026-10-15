#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_COCKPIT_AU_RADAR — Mer 30-09-2026 (Paris)
Rôle : prouver que le radar (programmes/audit_ecosysteme.py, maillon 18 « Tâches ») ne surveille plus le
cockpit par des fichiers du dépôt privé, que les autres tâches restent surveillées, et que la raison de ce
retrait reste vraie dans le circuit du soir.
Quand l'appeler : avant toute livraison qui touche la liste `_declarations` du radar, ou le pas du cockpit
dans .github/workflows/collecte_abc.yml (R-755 ②).

À QUOI ÇA SERT. Chaque soir, le radar écrivait « le cockpit n'a rien écrit depuis 7 jour(s) » (rapport du
29-09-2026, version officielle). Faux : le cockpit est publié chaque soir au dépôt PUBLIC (commit « cockpit
2026-09-29 20h22 ») et n'écrit aucun fichier au dépôt privé ; le motif « cockpit » trouvait une image du 22-09
(etudes/illustrations/A443_cockpit_courbe_3D_4D_Mar_22-09-2026_12h35.jpeg). Travail demandé par Jean-Luc pour
la nuit du 30-09-2026 (« OK pour le 1 », 29-09 à 22h29) : faire regarder la vraie trace, ou retirer le motif
en le disant. Le motif est retiré, parce que le radar ne peut de toute façon pas voir le cockpit s'arrêter :
le pas du cockpit passe AVANT le radar, sans `continue-on-error` ; s'il tombe, le passage s'arrête et c'est la
trace de l'audit du soir qui vieillit.

LES ÉPREUVES, chacune sur une COPIE du dépôt :
E1 deux preuves. ① PROPRIÉTÉ : aucun motif de tâche déclaré au maillon 18 ne correspond à un fichier de
   la copie dont le nom contient « cockpit » (les relecteurs du 30-09-2026 avaient fait passer le libellé
   « la page publiée », puis le motif « claude_cockpit »). Les motifs sont lus dans la liste littérale
   `_declarations` du radar, par son arbre syntaxique ; les noms sont ramenés à la forme du radar
   (minuscules, espaces et tirets devenus « _ »). ② CHEMIN RÉEL, qui couvre toute forme de DÉCLARATION
   (ajoutée hors de la liste, motif mêlé, motif sur une date) et tout ajout de fichiers à la liste d'une
   tâche : un TÉMOIN enveloppe, dans une copie du radar, la fonction `_date_declaree`, par laquelle le
   maillon 18 fait passer chaque fichier retenu, et écrit tout fichier reçu dont le nom contient
   « cockpit » ; il ne doit rien écrire. CE QU'IL NE COUVRE PAS (relecteur du tour 9) : du code écrit
   exprès pour prendre la date d'un fichier au nom de cockpit par une autre route — un alias de
   `_date_declaree` posé avant le témoin, une date lue directement dans un nom, ou `_date_declaree`
   modifiée pour lire un autre fichier que celui qu'elle reçoit. Ces cas sont des réécritures du radar,
   pas des déclarations ; une épreuve ne peut pas les exclure tous. La propriété porte sur ce que le radar RETIENT, pas sur la date qu'il affiche :
   un fichier retenu mais masqué par une trace plus récente passait les versions précédentes (relecteurs du
   30-09-2026, tours 5 à 8). HORS DE LA PROPRIÉTÉ : un motif qui ne vise aucun fichier au nom de cockpit —
   par exemple une tâche « la page publiée » déclarée hors de la liste au motif « cockpit_du_soir », qui ne
   trouve rien et fait dire chaque soir « AUCUNE trace » ; aucune épreuve ne la voit, puisque aucun fichier
   au nom de cockpit n'est retenu (relecteur du tour 8).
E2 les tâches encore déclarées (boucle du jour, audit du soir, mesure de performance) ont chacune leur ligne,
   à la date d'aujourd'hui fabriquée pour elles ;
E3 la raison du retrait tient dans le circuit : une panne du pas qui publie le cockpit arrête le passage avant
   le radar. PROPRIÉTÉ vérifiée : dans le même job, le pas dont la clé `run:` appelle PUBLIER_LE_SITE.py
   précède celui dont la clé `run:` appelle le radar ; sa clé `run:` vaut EXACTEMENT l'appel seul
   (`python3 programmes/PUBLIER_LE_SITE.py "$GITHUB_WORKSPACE"`), sans rien avant ni après ; il ne porte ni
   `continue-on-error`, ni `shell:`, ni `if:` ; aucun pas jusqu'au radar inclus ne porte de `if:`, à quelque
   indentation que ce soit. Si l'une de ces conditions tombe, un cockpit en panne pourrait ne plus rien
   arrêter, et il faudrait de nouveau le surveiller. Limite : le code de sortie de PUBLIER_LE_SITE.py
   lui-même n'est pas éprouvé ici ;
E4 le chemin réel : sur la copie telle quelle, aucune ligne du maillon 18 ne parle du cockpit.
LES SABOTAGES : S1 remet la déclaration du cockpit (E1 et E4 doivent rougir) · S2 donne `continue-on-error`
au pas du cockpit (E3) · S3 retire la déclaration de la mesure de performance (E2) · S4 ajoute `|| true` à la
commande du cockpit (E3) · S5 donne `if: always()` au pas du radar (E3) · S6 ajoute `; exit 0` (E3) · S7 cite
PUBLIER_LE_SITE.py dans un commentaire d'un pas antérieur ET ajoute `|| true` au vrai pas (E3) · S8 remet la
surveillance sous un autre libellé, « la page publiée » (E1) · S9 la remet sous le motif « claude_cockpit » (E1)
· S10 écrit la clé `"continue-on-error"` entre guillemets (E3) · S11 ajoute la surveillance APRÈS la liste,
par `_declarations.append`, sous le motif « claude_cockpit » (E1②) · S12 ajoute « claude_cockpit » aux motifs de
la boucle du jour (E1②) · S13 déclare une tâche aux motifs « claude_cockpit » ET « rapport_boucle » (E1②) · S14
ajoute aux motifs de la boucle un morceau de nom qui vise la DATE d'un fichier au nom de cockpit,
« 07_09_2026_22h02 » (E1②) · S15 déclare hors de la liste une tâche « la page publiée » au motif « html »,
qui atteint des fichiers au nom de cockpit mais dont la date affichée vient d'une autre page, plus récente (E1②).
· S16 ajoute des fichiers au nom de cockpit à la liste `_f` de la boucle APRÈS son relevé, juste avant le
calcul des dates (E1②). S4 à S16 viennent des relecteurs du 30-09-2026.
LIMITE CONNUE : E2 fabrique une trace de l'audit du soir datée dans son nom ; en production, le rapport du
radar est vidé par le pas du radar avant d'être lu (« SANS DATE LISIBLE » chaque soir) — défaut consigné au
BACKLOG le 30-09-2026. E2 prouve que le radar surveille encore trois tâches, pas que la trace de l'audit est
lisible en production.

USAGE : python3 tests/EPREUVES_DU_COCKPIT_AU_RADAR_Mer_30-09-2026.py <racine du dépôt> [--saboter]
CODE : 0 si les épreuves sont vertes sans sabotage et que chaque sabotage fait rougir au moins une épreuve ;
1 sinon ; 2 si un sabotage ou le témoin de E1② ne s'applique plus (ancre absente : l'épreuve ne prouverait plus rien).
"""
import ast, os, re, shutil, subprocess, sys, tempfile
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
RAD = "programmes/audit_ecosysteme.py"
WF = ".github/workflows/collecte_abc.yml"
DECL_MESURE = '        ("la mesure de performance", ["historique_mesures"], 2, "calendaire"),\n'
SABOTAGES = {
    "Z0": [],
    "S1_cockpit_remis": [(RAD, DECL_MESURE, '        ("le cockpit", ["cockpit"], 2, "calendaire"),\n' + DECL_MESURE)],
    "S2_cockpit_non_bloquant": [(WF, "        id: fabriquer_et_publier_le_cockpit_en_pag\n",
                                 "        id: fabriquer_et_publier_le_cockpit_en_pag\n        continue-on-error: true\n")],
    "S3_mesure_retiree": [(RAD, DECL_MESURE, "")],
    "S4_cockpit_ou_vrai": [(WF, 'run: python3 programmes/PUBLIER_LE_SITE.py "$GITHUB_WORKSPACE"\n',
                            'run: python3 programmes/PUBLIER_LE_SITE.py "$GITHUB_WORKSPACE" || true\n')],
    "S5_radar_toujours": [(WF, "        id: radar\n", "        id: radar\n        if: always()\n")],
    "S6_cockpit_exit0": [(WF, 'run: python3 programmes/PUBLIER_LE_SITE.py "$GITHUB_WORKSPACE"\n',
                          'run: python3 programmes/PUBLIER_LE_SITE.py "$GITHUB_WORKSPACE"; exit 0\n')],
    "S7_leurre_et_masque": [(WF, "        id: commiter_les_signaux\n",
                             "        id: commiter_les_signaux\n        # ancien appel : PUBLIER_LE_SITE.py\n"),
                            (WF, 'run: python3 programmes/PUBLIER_LE_SITE.py "$GITHUB_WORKSPACE"\n',
                             'run: python3 programmes/PUBLIER_LE_SITE.py "$GITHUB_WORKSPACE" || true\n')],
    "S8_autre_libelle": [(RAD, DECL_MESURE, '        ("la page publiée", ["cockpit"], 2, "calendaire"),\n' + DECL_MESURE)],
    "S9_autre_motif": [(RAD, DECL_MESURE, '        ("la page publiée", ["claude_cockpit"], 2, "calendaire"),\n' + DECL_MESURE)],
    "S10_cle_entre_guillemets": [(WF, "        id: fabriquer_et_publier_le_cockpit_en_pag\n",
                                  '        id: fabriquer_et_publier_le_cockpit_en_pag\n        "continue-on-error": true\n')],
    "S11_ajout_hors_liste": [(RAD, "    _propres = []\n",
                              '    _declarations.append(("la page publiée", ["claude_cockpit"], 2, "calendaire"))\n    _propres = []\n')],
    "S12_motif_ajoute_a_la_boucle": [(RAD, "    _propres = []\n", '    _declarations[0][1].append("claude_cockpit")\n    _propres = []\n')],
    "S14_motif_sur_la_date": [(RAD, "    _propres = []\n", '    _declarations[0][1].append("07_09_2026_22h02")\n    _propres = []\n')],
    "S15_html_masque": [(RAD, "    _propres = []\n", '    _declarations.append(("la page publiée", ["html"], 2, "calendaire"))\n    _propres = []\n')],
    "S16_ajout_apres_releve": [(RAD, "        _dates = [d for d in (_date_declaree(p) for p in _f) if d]\n",
                                "        if _lib == \"la boucle du jour\":\n            _f = _f + [p for p in _chemins if \"claude_cockpit\" in _norm(os.path.basename(p))]\n"
                                "        _dates = [d for d in (_date_declaree(p) for p in _f) if d]\n")],
    "S13_motifs_meles": [(RAD, "    _propres = []\n",
                          '    _declarations.append(("la page publiée", ["claude_cockpit", "rapport_boucle"], 2, "calendaire"))\n    _propres = []\n')],
}


def motifs_declares(r):
    """Rend les motifs de fichiers des tâches déclarées au maillon 18 du radar de la copie `r`.

    ① RÔLE — lire ce que le radar cherche, sans l'exécuter. ② CONTEXTE D'APPEL — `epreuves`, une fois.
    ③ ENTRÉE — `r` : la racine d'une copie. ④ CONDITIONS D'ENTRÉE — le radar doit se lire en Python.
    ⑤ SORTIE — UNE valeur : la liste des motifs, vide si la liste `_declarations` est introuvable. [rend: 1]
    ⑥ TRAITEMENT — parcourir l'arbre syntaxique, trouver l'affectation à `_declarations`, évaluer sa
    valeur littérale, prendre le deuxième élément de chaque déclaration. ⑦ UNITÉ — des motifs de noms.
    ⑧ POURQUOI — un motif de ligne se trompe sur les guillemets et les lignes coupées (relecteur du tour 1
    sur `_nb_taches`) ; l'arbre syntaxique non. ⑨ CE QUI CLOCHE — elle ne lit que la liste littérale : une
    déclaration ajoutée ensuite (`_declarations.append(…)`, ou une somme de listes) n'est pas lue, et la
    liste rendue est alors INCOMPLÈTE sans que rien le dise (relecteur du 30-09-2026) ; c'est E1② qui
    couvre ce cas par le chemin réel, grâce à un témoin posé dans le radar (sabotages S11 à S15). Une liste entièrement calculée rend une liste
    vide, et E1① rougit.
    ⑩ EFFET — lit un fichier. ⑪ TERMINAISON — rend la main ; lève si le radar ne se lit pas en Python. [sort: non]
    """
    arbre = ast.parse(open(os.path.join(r, RAD), encoding="utf-8").read())
    for n in ast.walk(arbre):
        if isinstance(n, ast.Assign) and any(isinstance(c, ast.Name) and c.id == "_declarations" for c in n.targets):
            try:
                return [m for d in ast.literal_eval(n.value) if len(d) > 1 for m in d[1]]
            except ValueError:
                return []
    return []


def lignes18(r):
    """Lance le radar sur la copie `r` et rend ses lignes du maillon 18.

    ① RÔLE — Isoler ce que le radar dit des tâches planifiées. ② CONTEXTE D'APPEL — `epreuves`, deux fois.
    ③ ENTRÉE — `r` : la racine d'une copie du dépôt. ④ CONDITIONS D'ENTRÉE — le radar doit exister dans
    la copie. ⑤ SORTIE — UNE valeur : la liste des lignes qui contiennent « 18-T ». [rend: 1]
    ⑥ TRAITEMENT — lancer le radar, garder les lignes du maillon. ⑦ UNITÉ — des lignes de texte.
    ⑧ POURQUOI — les épreuves ne regardent que ce maillon. ⑨ CE QUI CLOCHE — un radar qui tombe avant le
    maillon 18 rend une liste vide ; E2 rougit alors, ce qui est voulu. ⑩ EFFET — lance un programme qui
    lit la copie. ⑪ TERMINAISON — rend la main ; le radar est arrêté au bout de 900 secondes. [sort: non]
    """
    p = subprocess.run([sys.executable, os.path.join(r, RAD), r], cwd=r, capture_output=True,
                       text=True, errors="replace", timeout=900)
    return [l for l in (p.stdout + p.stderr).splitlines() if "18-T" in l]


def cockpit_bloquant(wf):
    """Dit si, dans le circuit `wf`, une panne du pas du cockpit arrête le passage avant le radar.

    ① RÔLE — la propriété E3 décrite en tête. ② CONTEXTE D'APPEL — `epreuves`, une fois.
    ③ ENTRÉE — `wf` : le texte de .github/workflows/collecte_abc.yml. ④ CONDITIONS D'ENTRÉE — aucune.
    ⑤ SORTIE — UNE valeur : vrai si la propriété tient. [rend: 1]
    ⑥ TRAITEMENT — ① découper en jobs, puis en pas · ② repérer les pas par leur clé `run:`, jamais par un
    mot ailleurs · ③ exiger même job, ordre, commande exacte, aucune clé de masque. ⑦ UNITÉ — —.
    ⑧ POURQUOI — le relecteur du 30-09-2026 a montré qu'une liste de masques interdits en oublie toujours
    (« ; true », « ; exit 0 », « if ! … », un leurre en commentaire) : on exige donc la seule forme sûre.
    ⑨ CE QUI CLOCHE — elle lit le texte du circuit comme des lignes, sans lecteur YAML : une commande
    écrite en bloc (« run: | ») serait refusée alors qu'elle bloque ; les clés sont reconnues avec ou
    sans guillemets (relecteur du 30-09-2026), mais une forme non essayée, comme une clé posée par un
    ancrage YAML, lui échapperait. ⑩ EFFET — aucun.
    ⑪ TERMINAISON — rend la main. [sort: non]
    """
    appel = 'python3 programmes/PUBLIER_LE_SITE.py "$GITHUB_WORKSPACE"'
    for job in re.split(r"(?m)^  (?=\S)", wf.split("\njobs:", 1)[-1]):
        pas = re.split(r"\n      - ", job)
        runs = [re.findall(r"(?m)^        run:\s*(.*)$", p) for p in pas]
        i_ck = next((k for k, x in enumerate(runs) if any("PUBLIER_LE_SITE.py" in v for v in x)), None)
        i_rad = next((k for k, p in enumerate(pas)
                      if re.search(r"(?m)^\s*[^#\s].*" + re.escape(os.path.basename(RAD)), p.split("run:", 1)[-1]) and "run:" in p), None)
        if i_ck is None or i_rad is None:
            continue
        if i_ck > i_rad or [v.strip() for v in runs[i_ck]] != [appel]:
            return False
        if re.search(r"(?m)^\s+[\"']?(continue-on-error|shell|if)[\"']?\s*:", pas[i_ck]):
            return False
        if any(re.search(r"(?m)^\s+[\"']?if[\"']?\s*:", pas[k]) for k in range(i_ck, i_rad + 1)):
            return False
        return True
    return False


def epreuves(r):
    """Joue E1 à E4 sur la copie `r` et rend la liste (nom, verdict).

    ① RÔLE — les épreuves décrites en tête. ② CONTEXTE D'APPEL — `main`, une fois par sabotage.
    ③ ENTRÉE — `r` : une copie du dépôt, éventuellement sabotée. ④ CONDITIONS D'ENTRÉE — le radar de la
    copie doit porter une seule fois le commentaire qui suit la définition de `_date_declaree`, où le
    témoin s'insère, et le texte « _date_declaree( » exactement deux fois (sa définition et son appel) ;
    sinon LÈVE. Ce compte porte sur le texte, pas sur les appels : un alias n'est pas vu.
    ⑤ SORTIE — UNE valeur : une liste de couples (nom de l'épreuve, vrai si verte). [rend: 1]
    ⑥ TRAITEMENT — ① lancer le radar sur la copie telle quelle (E4) · ② lire le circuit (E3) · ③ lire les
    motifs déclarés (E1①) · ④ E1② : envelopper, dans le radar de la copie, la fonction `_date_declaree`
    — par laquelle le maillon 18 fait passer chaque fichier retenu — d'un témoin qui écrit chaque fichier
    reçu dont le nom contient « cockpit », lancer ce radar, exiger qu'il n'écrive rien · ⑤ E2 : fabriquer une trace du jour par tâche, relancer, exiger les
    trois libellés à la date du jour. ⑦ UNITÉ — —. ⑧ POURQUOI — la propriété porte sur ce que le radar
    RETIENT, pas sur la date qu'il affiche : un fichier au nom de cockpit retenu puis masqué par une trace
    plus récente passait toutes les versions précédentes de E1② (relecteurs du 30-09-2026, tours 5 à 8).
    ⑨ CE QUI CLOCHE — le témoin s'accroche à une ligne du radar : si elle change, l'épreuve LÈVE au lieu
    de conclure, ce qui est voulu. Une date de trace qui ne passerait pas par `_date_declaree` échapperait
    au témoin (le relecteur du tour 8 avait contourné un témoin posé sur la liste `_f`). E2 cherche les libellés des tâches tels qu'ils sont écrits ; un libellé
    renommé la ferait rougir sans défaut. ⑩ EFFET — dans la copie : RÉÉCRIT le radar (témoin), écrit trois
    fichiers sous sous/dossier/. ⑪ TERMINAISON — rend la main, ou lève sur une ancre absente. [sort: non]
    """
    res = []
    l0 = lignes18(r)
    res.append(("E4 copie réelle : aucune ligne du maillon 18 ne parle du cockpit",
                bool(l0) and not any("cockpit" in l.lower() for l in l0)))
    wf = open(os.path.join(r, WF), encoding="utf-8").read()
    res.append(("E3 une panne du cockpit arrête le passage avant le radar", cockpit_bloquant(wf)))
    norm = lambda s: re.sub(r"[ \-_]+", "_", s.lower())      # la forme du radar (_norm)
    noms = [norm(x) for _rac, _sd, fs in os.walk(r) for x in fs if "cockpit" in x.lower()]
    motifs = motifs_declares(r)
    touches = [m for m in motifs for x in noms if m in x]
    res.append(("E1① aucun motif déclaré ne vise un fichier au nom de cockpit",
                bool(motifs) and not touches))
    rad = os.path.join(r, RAD)
    src = open(rad, encoding="utf-8").read()
    ancre = "    # CHAQUE TÂCHE A SON PROPRE CALENDRIER, ET LE COMPTAGE DOIT LE SUIVRE.\n"
    if src.count(ancre) != 1 or src.count("_date_declaree(") != 2:
        raise RuntimeError("ancre du témoin absente ou multiple, ou _date_declaree appelée ailleurs")
    temoin = ('    _date_declaree_sans_temoin = _date_declaree\n'
              '    def _date_declaree(chemin):\n'
              '        if "cockpit" in os.path.basename(chemin).lower():\n'
              '            print("TEMOIN_COCKPIT_RETENU", chemin)\n'
              '        return _date_declaree_sans_temoin(chemin)\n')
    open(rad, "w", encoding="utf-8").write(src.replace(ancre, temoin + ancre))
    p = subprocess.run([sys.executable, rad, r], cwd=r, capture_output=True, text=True, errors="replace", timeout=900)
    sortie = p.stdout + p.stderr
    open(rad, "w", encoding="utf-8").write(src)
    res.append(("E1② le radar ne retient comme trace aucun fichier au nom de cockpit",
                "18-T" in sortie and "TEMOIN_COCKPIT_RETENU" not in sortie))
    jour = datetime.now(ZoneInfo("Europe/Paris")).date().isoformat()
    d = os.path.join(r, "sous", "dossier")
    os.makedirs(d, exist_ok=True)
    for nom, texte in ((f"claude_rapport_boucle_{jour}.md", f"# boucle {jour}\n"),
                       (f"audit_du_jour_{jour}.md", f"# audit {jour}\n"),
                       ("historique_mesures.csv", f"date_mesure,valeur\n{jour},1\n")):
        with open(os.path.join(d, nom), "w", encoding="utf-8") as f:
            f.write(texte)
    l2 = lignes18(r)
    res.append(("E2 boucle, audit et mesure ont chacune leur ligne, datée du jour",
                all(any(lib in l and f"DÉCLARÉE {jour}" in l for l in l2)
                    for lib in ("la boucle du jour", "l'audit du soir", "la mesure de performance"))))
    return res


def main():
    """Joue les épreuves sans sabotage, puis avec chaque sabotage si --saboter est donné.

    ① RÔLE — dire si les épreuves prouvent quelque chose. ② CONTEXTE D'APPEL — le lancement du fichier.
    ③ ENTRÉE — la ligne de commande. ④ CONDITIONS D'ENTRÉE — la racine doit être un dépôt complet.
    ⑤ SORTIE — UNE valeur : le code de sortie, 0, 1 ou 2. [rend: 1] ⑥ TRAITEMENT — pour chaque cas :
    copier le dépôt, appliquer le sabotage, jouer les épreuves, compter les rouges. ⑦ UNITÉ — —.
    ⑧ POURQUOI — une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration (R-731).
    ⑨ CE QUI CLOCHE — chaque cas recopie le dépôt entier : plusieurs minutes avec --saboter.
    ⑩ EFFET — crée puis efface des copies dans le dossier temporaire ; affiche un compte rendu.
    ⑪ TERMINAISON — rend la main par son code ; les copies sont effacées même en cas d'erreur. [sort: non]
    """
    choix = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
    bon = True
    for sab in choix:
        t = tempfile.mkdtemp(prefix="cockpit_radar_")
        try:
            r = os.path.join(t, "r")
            shutil.copytree(DEPOT, r, ignore=shutil.ignore_patterns(".git", "_site_travail", "__pycache__"))
            for f, a, b in SABOTAGES[sab]:
                p = os.path.join(r, f)
                x = open(p, encoding="utf-8").read()
                if x.count(a) != 1:
                    print(f"SABOTAGE {sab} INAPPLICABLE : ancre absente ou multiple — l'épreuve ne prouve plus rien")
                    return 2
                open(p, "w", encoding="utf-8").write(x.replace(a, b))
            try:
                res = epreuves(r)
            except RuntimeError as e:
                print(f"ÉPREUVE INAPPLICABLE ({sab}) : {e}")
                return 2
        finally:
            shutil.rmtree(t, ignore_errors=True)
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
