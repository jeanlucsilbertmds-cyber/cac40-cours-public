#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FABRIQUER_LA_CARTE_DU_CIRCUIT — Sam 21-11-2026 (Paris). Simulation uniquement : aucun ordre réel, jamais.

LE SENS EN TÊTE. Ce programme FABRIQUE `etudes/CARTE_DU_CIRCUIT.md` : l'enchaînement du circuit du soir et de la
moulinette, pas par pas, avec, pour chaque programme appelé, son rôle et son contexte d'appel TELS QUE SON CODE LES
ÉCRIT. Il ne lit que le code ; il n'écrit à la main aucun texte de la carte. À chaque évolution du code, on relance le
programme et on relit la carte.
POURQUOI UNE CARTE FABRIQUÉE, ET PAS ÉCRITE À LA MAIN. Décision de Jean-Luc du Sam 21-11-2026 à 14h36 (« 1 »), dont
les mots, à 14h35, étaient : « la lecture de l'enchaînement de ce circuit et les informations dans le code qui
permettent de déterminer précisément comment il fonctionne, et du coup à chaque évolution on pourra relire cet
enchaînement ». Une carte écrite à la main vieillit dès que le code change, et rien ne le dit : deux descriptions d'une
même chose divergent toujours (R-708). Avant ce programme, deux cartes écrites à la main existaient
(etudes/CARTE_ECOSYSTEME_Ven_11-09-2026_15h15.md, etudes/ETUDE_12_CARTE_DU_CIRCUIT_COMPLET_v2_Mer_26-08-2026_14h47.md) ;
elles décrivent le circuit de leur date, pas celui d'aujourd'hui. Ici, la seule source est le code : ce qui se calcule
ne s'écrit jamais à la main (R-728).
LES SOURCES, ET SEULEMENT ELLES. ① L'ordre du soir : `.github/workflows/collecte_abc.yml`, chaque pas et chaque
programme que son « run » lance, dans l'ordre du fichier. ② L'ordre de la moulinette :
`programmes/ENCHAINER_LA_MOULINETTE.py` — l'ordre de ses étapes est celui de son dictionnaire EXIGEES, le programme de
chaque étape est celui que sa fonction `faire` lance. ③ Pour chaque programme appelé : ses éléments « ① RÔLE » et
« ② CONTEXTE D'APPEL » (R-752), lus dans son texte de tête et recopiés tels quels.
LE MARQUAGE DE CHAQUE ÉTAPE, D'APRÈS LE TEXTE DU CODE. AUTOMATIQUE : l'étape appartient à un fichier de tâches qui se
réveille seul — il porte « schedule », ou un programme de programmes/ écrit son réveil (une ligne « - cron: » et le
nom du fichier ; le 21-11-2026, c'est programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py, qui fabrique le circuit du dépôt
public depuis collecte_abc.yml). À LA MAIN : le contexte d'appel de l'appelant commence par « À la main » (le cas de
l'enchaîneur de la moulinette). ATTEND JEAN-LUC : le contexte d'appel du programme appelé dit qu'il attend la
validation, la demande ou l'accord de Jean-Luc (motif MOTIF_ATTEND, calibré le 21-11-2026 : il prend PREPARER et
DECLINER, il ne prend pas METEO_DU_MARCHE, dont le contexte cite une « Décision de Jean-Luc » passée).
CE QUE LA CARTE NE VOIT PAS — SES LIMITES. ① Elle ne voit que ce que le code DÉCLARE : un programme lancé autrement que
par « python3 <chemin> » dans un « run », ou importé par un autre, n'apparaît pas comme étape. ② Elle recopie les
éléments ① et ② sans juger s'ils sont vrais : un texte de tête faux donne une carte fausse (R-756 : chercher le sens
reste au lecteur). ③ Le marquage est une lecture de mots : un contexte d'appel mal écrit est mal marqué. ④ L'AMONT DU
LABORATOIRE — de l'idée à la fiche — n'a pas encore de programme, donc pas de place sur la carte : il est décrit, à la
main, dans etudes/ETUDE_11_CIRCUIT_DU_LABORATOIRE_Dim_23-08-2026_20h42.md (étapes ① NAÎTRE et ② S'INSTRUIRE). ⑤ Les
autres fichiers de tâches (certifier.yml, rattrapage_du_matin.yml, collecte_consensus.yml…) ne sont pas cartographiés.
⑥ Le programme n'est PAS branché au circuit du soir : ce branchement est proposé à Jean-Luc, pas décidé.

USAGE
    python3 programmes/FABRIQUER_LA_CARTE_DU_CIRCUIT.py <racine> [<carte>]
    <carte> par défaut : <racine>/etudes/CARTE_DU_CIRCUIT.md

① RÔLE — Fabriquer la carte du circuit du soir et de la moulinette à partir du seul code, et rougir quand un programme
  cité est introuvable ou ne porte pas son élément ① RÔLE.
② CONTEXTE D'APPEL — À la main, par le Chat ou Cowork, après toute évolution du circuit ; par l'épreuve
  tests/EPREUVE_DE_LA_CARTE_DU_CIRCUIT_Sam_21-11-2026.py (code « Carte »). Aucune tâche automatique ne l'appelle.
③ ENTRÉE — La ligne de commande : la racine d'un dépôt ; facultatif, le chemin de la carte à écrire.
④ CONDITIONS D'ENTRÉE — La racine porte .github/workflows/collecte_abc.yml (YAML lisible, module yaml installé) et
  programmes/ENCHAINER_LA_MOULINETTE.py.
⑤ SORTIE — Le code de sortie : 0 carte écrite, aucune anomalie · 1 carte écrite, au moins une anomalie (programme
  introuvable, élément ① absent, étape de la moulinette sans programme) — la carte les nomme · 2 la carte n'a pas pu
  être fabriquée (source absente ou illisible), rien n'est écrit (R-734).
  [rend: 1]
⑥ TRAITEMENT — ① lire les pas du soir · ② lire les étapes de la moulinette · ③ lire ① et ② de chaque programme cité ·
  ④ marquer chaque étape · ⑤ écrire la carte, anomalies en tête.
⑦ UNITÉ — —
⑧ POURQUOI — Voir « POURQUOI UNE CARTE FABRIQUÉE » ci-dessus.
⑨ CE QUI CLOCHE — Voir « CE QUE LA CARTE NE VOIT PAS » ci-dessus ; la carte recopie ce paragraphe dans sa section
  « Limites », lu ici même, jamais recopié à la main.
⑩ EFFET — Écrit un seul fichier, la carte. Ne lance aucun programme, n'écrit rien d'autre.
⑪ TERMINAISON — Sort par sys.exit depuis le bloc final. Un de mes appels peut-il ne pas revenir ? Non : aucune
  attente, aucun réseau, aucun sous-processus.
  [sort: non]
"""
import ast
import datetime
import os
import re
import sys

sys.dont_write_bytecode = True

SOIR = os.path.join(".github", "workflows", "collecte_abc.yml")
MOULINETTE = os.path.join("programmes", "ENCHAINER_LA_MOULINETTE.py")
CARTE = os.path.join("etudes", "CARTE_DU_CIRCUIT.md")
LANCE = re.compile(r"python3?\s+(?:-\w+\s+)*[\"']?((?:programmes|tests)/[^\s\"']+\.py)")
ROLE = re.compile(r"^[ \t]*①[ \t]*R[ÔO]LE[ \t]*—(.*?)(?=^[ \t]*②|\Z)", re.M | re.S)
CONTEXTE = re.compile(r"^[ \t]*②[ \t]*CONTEXTE D.APPEL[ \t]*—(.*?)(?=^[ \t]*③|\Z)", re.M | re.S)
LIMITES = re.compile(r"^CE QUE LA CARTE NE VOIT PAS.*?(?=^\n|^USAGE)", re.M | re.S)
MOTIF_ATTEND = re.compile(r"(validation|demande|accord) de Jean-Luc|Jean-Luc (valide|décide)", re.I)
REVEIL = re.compile(r"^\s*- cron: \"", re.M)


def elements(racine, chemin):
    """Lit les éléments ① RÔLE et ② CONTEXTE D'APPEL du texte de tête d'un programme.

    ① RÔLE — Donner, tels que le code les écrit, le rôle et le contexte d'appel d'un programme.
    ② CONTEXTE D'APPEL — `fabriquer`, une fois par programme cité ; l'épreuve de la carte.
    ③ ENTRÉE — `racine` : la racine du dépôt ; `chemin` : le programme, relatif à la racine.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — TROIS valeurs : le rôle ou None ; le contexte ou None ; l'anomalie ou None.
      [rend: 3]
    ⑥ TRAITEMENT — Lire le fichier ; prendre le texte de tête par l'arbre syntaxique ; chercher ① et ② ; garder leur
      texte, chaque ligne débarrassée de ses blancs de bord.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un programme introuvable ou sans ① fait rougir la carte (R-734) : la carte ne doit pas taire un trou.
    ⑨ CE QUI CLOCHE — Un ① écrit en commentaire et non dans le texte de tête n'est pas vu : il compte comme absent.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    complet = os.path.join(racine, chemin)
    if not os.path.isfile(complet):
        return None, None, "%s : PROGRAMME INTROUVABLE" % chemin
    try:
        tete = ast.get_docstring(ast.parse(open(complet, encoding="utf-8").read()), clean=False) or ""
    except (SyntaxError, UnicodeDecodeError, ValueError) as e:
        return None, None, "%s : ILLISIBLE (%s)" % (chemin, type(e).__name__)
    trouves = []
    for motif in (ROLE, CONTEXTE):
        m = motif.search(tete)
        trouves.append(" ".join(l.strip() for l in m.group(1).strip().splitlines()) if m else None)
    return trouves[0], trouves[1], (None if trouves[0] else "%s : ÉLÉMENT ① RÔLE ABSENT" % chemin)


def pas_du_soir(racine):
    """Lit les pas du circuit du soir dans l'ordre du fichier de tâches.

    ① RÔLE — Rendre l'ordre du soir tel que le fichier de tâches l'écrit.
    ② CONTEXTE D'APPEL — `fabriquer`, une fois.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — SOIR existe et se lit en YAML ; sinon l'exception remonte (code 2 de `main`).
    ⑤ SORTIE — DEUX valeurs : le nom du circuit ; la liste des pas, chacun un dictionnaire (nom, programmes,
      non_bloquant, condition).
      [rend: 2]
    ⑥ TRAITEMENT — yaml.safe_load ; pour chaque job puis chaque pas : nom (ou « uses »), programmes lancés par son
      « run » (motif LANCE), « continue-on-error », « if ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le fichier de tâches est la seule source de l'ordre du soir.
    ⑨ CE QUI CLOCHE — Un programme lancé par une variable de l'interpréteur de commandes n'est pas vu (limite ①).
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main ; lève ce que lèvent l'import de yaml et la lecture.
      [sort: non]
    """
    import yaml
    doc = yaml.safe_load(open(os.path.join(racine, SOIR), encoding="utf-8"))
    pas = []
    for job in (doc.get("jobs") or {}).values():
        for p in job.get("steps") or []:
            pas.append({"nom": p.get("name") or "uses: %s" % p.get("uses"),
                        "programmes": LANCE.findall(p.get("run") or ""),
                        "non_bloquant": bool(p.get("continue-on-error")),
                        "condition": p.get("if")})
    return doc.get("name") or SOIR, pas


def reveil_du_soir(racine):
    """Dit si le circuit du soir se réveille seul, et qui écrit son réveil.

    ① RÔLE — Marquer les pas du soir AUTOMATIQUE ou À LA MAIN d'après le code.
    ② CONTEXTE D'APPEL — `fabriquer`, une fois.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — SOIR existe.
    ⑤ SORTIE — DEUX valeurs : le marquage (« AUTOMATIQUE » ou « À LA MAIN ») ; la raison, lue dans le code.
      [rend: 2]
    ⑥ TRAITEMENT — « schedule » dans le fichier de tâches → AUTOMATIQUE ; sinon un programme de programmes/ qui porte
      une ligne « - cron: » et le nom du fichier → AUTOMATIQUE (réveil fabriqué) ; sinon À LA MAIN.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Depuis le 08-10-2026 (A-543), l'horaire n'est plus dans collecte_abc.yml mais au circuit public,
      fabriqué depuis lui : lire le seul fichier dirait à tort « À LA MAIN ».
    ⑨ CE QUI CLOCHE — La présence du réveil n'est pas la preuve qu'il tourne : la carte lit le code, pas GitHub.
    ⑩ EFFET — Lit les programmes de programmes/.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if re.search(r"^\s*schedule\s*:", open(os.path.join(racine, SOIR), encoding="utf-8").read(), re.M):
        return "AUTOMATIQUE", "le fichier de tâches porte « schedule »"
    dossier = os.path.join(racine, "programmes")
    for nom in sorted(os.listdir(dossier)):
        if nom.endswith(".py"):
            texte = open(os.path.join(dossier, nom), encoding="utf-8", errors="replace").read()
            if os.path.basename(SOIR) in texte and REVEIL.search(texte):
                return "AUTOMATIQUE", "réveil écrit par programmes/%s" % nom
    return "À LA MAIN", "aucun réveil trouvé dans le code"


def etapes_de_la_moulinette(racine):
    """Lit les étapes de la moulinette et le programme de chacune, dans le code de l'enchaîneur.

    ① RÔLE — Rendre l'ordre de la moulinette tel que l'enchaîneur l'exige.
    ② CONTEXTE D'APPEL — `fabriquer`, une fois.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — MOULINETTE existe et s'analyse ; sinon l'exception remonte (code 2 de `main`).
    ⑤ SORTIE — DEUX valeurs : la liste ordonnée des (étape, programmes) ; la liste des anomalies.
      [rend: 2]
    ⑥ TRAITEMENT — ① l'ordre : les clés du dictionnaire EXIGEES · ② dans `faire`, chaque branche « etape == "x" » :
      les chaînes « programmes/….py » qu'elle contient · ③ la branche finale « else » revient à la seule étape restante.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — L'ordre vit dans le code de l'enchaîneur (A-919 : « la chaîne ne se saute pas ») ; le recopier ici le
      ferait diverger.
    ⑨ CE QUI CLOCHE — Si `faire` change de forme (plus de chaîne de « if etape == »), les étapes sortent sans
      programme : la carte rougit, elle ne se tait pas.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    arbre = ast.parse(open(os.path.join(racine, MOULINETTE), encoding="utf-8").read())
    ordre, branches = [], {}
    for n in arbre.body:
        if isinstance(n, ast.Assign) and any(getattr(c, "id", "") == "EXIGEES" for c in n.targets):
            ordre = [ast.literal_eval(k) for k in n.value.keys]
        if isinstance(n, ast.FunctionDef) and n.name == "faire":
            noeud = next((s for s in n.body if isinstance(s, ast.If)), None)
            while noeud is not None:
                t = noeud.test
                cle = (t.comparators[0].value if isinstance(t, ast.Compare) and getattr(t.left, "id", "") == "etape"
                       and isinstance(t.comparators[0], ast.Constant) else None)
                branches[cle] = [c.value for b in noeud.body for c in ast.walk(b) if isinstance(c, ast.Constant)
                                 and isinstance(c.value, str) and LANCE.search("python3 " + c.value)]
                suite = noeud.orelse
                if len(suite) == 1 and isinstance(suite[0], ast.If):
                    noeud = suite[0]
                else:
                    restantes = [e for e in ordre if e not in branches]
                    if suite and len(restantes) == 1:
                        branches[restantes[0]] = [c.value for b in suite for c in ast.walk(b)
                                                  if isinstance(c, ast.Constant) and isinstance(c.value, str)
                                                  and LANCE.search("python3 " + c.value)]
                    noeud = None
    anomalies = ["moulinette : aucune étape lue (EXIGEES absent)"] if not ordre else []
    etapes = []
    for e in ordre:
        progs = branches.get(e) or []
        if not progs:
            anomalies.append("moulinette, étape %s : AUCUN PROGRAMME LU dans `faire`" % e)
        etapes.append((e, progs))
    return etapes, anomalies


def marquer(mode_appelant, contexte):
    """Marque une étape AUTOMATIQUE, À LA MAIN ou ATTEND JEAN-LUC.

    ① RÔLE — Appliquer la règle de marquage écrite en tête.
    ② CONTEXTE D'APPEL — `fabriquer`, une fois par programme cité.
    ③ ENTRÉE — `mode_appelant` : le marquage de l'appelant ; `contexte` : le ② du programme appelé, ou None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le marquage.
      [rend: 1]
    ⑥ TRAITEMENT — MOTIF_ATTEND dans le contexte → ATTEND JEAN-LUC ; sinon le marquage de l'appelant.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — L'appelant décide comment l'étape part ; le programme appelé dit s'il attend Jean-Luc.
    ⑨ CE QUI CLOCHE — Lecture de mots : limite ③ de la tête.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    return "ATTEND JEAN-LUC" if contexte and MOTIF_ATTEND.search(contexte) else mode_appelant


def fabriquer(racine):
    """Fabrique le texte de la carte.

    ① RÔLE — Assembler la carte depuis les lectures du code.
    ② CONTEXTE D'APPEL — `main`, une fois ; l'épreuve de la carte.
    ③ ENTRÉE — `racine`.
    ④ CONDITIONS D'ENTRÉE — Celles de `pas_du_soir` et `etapes_de_la_moulinette`.
    ⑤ SORTIE — DEUX valeurs : le texte de la carte ; la liste des anomalies.
      [rend: 2]
    ⑥ TRAITEMENT — Mention « FABRIQUÉE — ne pas éditer » en tête · anomalies · le soir, pas par pas · la moulinette,
      étape par étape · les limites, lues dans ce programme même.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir la tête.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Lit des fichiers.
    ⑪ TERMINAISON — Rend la main ; lève ce que lèvent les lectures des deux sources.
      [sort: non]
    """
    nom_soir, pas = pas_du_soir(racine)
    mode_soir, raison = reveil_du_soir(racine)
    etapes, anomalies = etapes_de_la_moulinette(racine)
    _, ctx_moul, an_moul = elements(racine, MOULINETTE.replace(os.sep, "/"))
    mode_moul = "À LA MAIN" if (ctx_moul or "").startswith("À la main") else "AUTOMATIQUE"
    corps = []

    def bloc(chemin, mode):
        """Écrit un programme cité.

        ① RÔLE — Une entrée de la carte.
        ② CONTEXTE D'APPEL — `fabriquer`, une fois par programme cité.
        ③ ENTRÉE — `chemin` : le programme ; `mode` : le marquage de l'appelant.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Aucune valeur.
          [rend: rien]
        ⑥ TRAITEMENT — `elements`, `marquer`, lignes ajoutées à `corps`, anomalie ajoutée à `anomalies`.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Une seule mise en forme pour les deux circuits.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Modifie `corps` et `anomalies`.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        role, ctx, an = elements(racine, chemin)
        if an:
            anomalies.append(an)
        corps.append("- `%s` — **%s**" % (chemin, marquer(mode, ctx) if not an else "❌ " + an))
        corps.append("  - ① RÔLE — %s" % (role or "❌ ABSENT"))
        corps.append("  - ② CONTEXTE D'APPEL — %s" % (ctx or "❌ ABSENT"))

    corps += ["", "## 1 · LE CIRCUIT DU SOIR — « %s » (`%s`)" % (nom_soir, SOIR.replace(os.sep, "/")), "",
              "Marquage des pas : **%s** — %s." % (mode_soir, raison), ""]
    for i, p in enumerate(pas, 1):
        traits = [mode_soir] + (["non bloquant (continue-on-error)"] if p["non_bloquant"] else []) + \
                 (["seulement si : `%s`" % p["condition"]] if p["condition"] else [])
        corps.append("### Pas %d — %s · %s" % (i, p["nom"], " · ".join(traits)))
        if not p["programmes"]:
            corps.append("- aucun programme : commandes écrites dans le fichier de tâches")
        for prog in p["programmes"]:
            bloc(prog, mode_soir)
        corps.append("")
    corps += ["## 2 · LA MOULINETTE — `%s`" % MOULINETTE.replace(os.sep, "/"), "",
              "L'enchaîneur : **%s** — ② CONTEXTE D'APPEL — %s" % (mode_moul, ctx_moul or "❌ ABSENT"), ""]
    if an_moul:
        anomalies.append(an_moul)
    for i, (e, progs) in enumerate(etapes, 1):
        corps.append("### Étape %d — %s" % (i, e))
        for prog in progs:
            bloc(prog, mode_moul)
        corps.append("")
    limites = LIMITES.search(__doc__)
    corps += ["## 3 · LIMITES DE CETTE CARTE (lues dans le texte de tête du programme qui la fabrique)", "",
              " ".join(l.strip() for l in limites.group(0).splitlines()) if limites else "❌ LIMITES ILLISIBLES", ""]
    heure = datetime.datetime.now(_paris()).strftime("%Y-%m-%d_%Hh%M")
    tete = ["<!-- FABRIQUÉE — ne pas éditer : toute modification à la main sera écrasée. -->",
            "# CARTE DU CIRCUIT — FABRIQUÉE — ne pas éditer", "",
            "Fabriquée le %s (Paris) par `programmes/FABRIQUER_LA_CARTE_DU_CIRCUIT.py`, depuis le seul code." % heure,
            "Simulation uniquement : aucun ordre réel, jamais.", "",
            "## ANOMALIES : %s" % ("aucune" if not anomalies else "%d — LA CARTE ROUGIT" % len(anomalies))]
    tete += ["- ❌ %s" % a for a in anomalies]
    return "\n".join(tete + corps) + "\n", anomalies


def _paris():
    """Rend le fuseau de Paris.

    ① RÔLE — Horodater en Europe/Paris.
    ② CONTEXTE D'APPEL — `fabriquer`, une fois.
    ③ ENTRÉE — —
    ④ CONDITIONS D'ENTRÉE — La base des fuseaux est installée.
    ⑤ SORTIE — UNE valeur : le fuseau.
      [rend: 1]
    ⑥ TRAITEMENT — ZoneInfo.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Horodatage Europe/Paris exigé dans chaque en-tête.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; lève si la base des fuseaux manque.
      [sort: non]
    """
    from zoneinfo import ZoneInfo
    return ZoneInfo("Europe/Paris")


def main(argv):
    """Point d'entrée.

    ① RÔLE — Voir la tête.
    ② CONTEXTE D'APPEL — Le bloc final ; l'épreuve de la carte.
    ③ ENTRÉE — `argv` : la racine, puis facultativement le chemin de la carte.
    ④ CONDITIONS D'ENTRÉE — Voir la tête.
    ⑤ SORTIE — UNE valeur : 0, 1 ou 2 (voir la tête).
      [rend: 1]
    ⑥ TRAITEMENT — Arguments · `fabriquer` (une erreur de lecture d'une source → 2, rien d'écrit) · écriture ·
      anomalies affichées.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — R-734 : un contrôle qui n'a pas pu tourner rend un code non nul.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit la carte.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if len(argv) not in (1, 2):
        print("usage : FABRIQUER_LA_CARTE_DU_CIRCUIT.py <racine> [<carte>]")
        return 2
    racine = os.path.abspath(argv[0])
    sortie = argv[1] if len(argv) == 2 else os.path.join(racine, CARTE)
    try:
        texte, anomalies = fabriquer(racine)
    except Exception as e:  # une source absente ou illisible : la carte n'a pas pu être fabriquée (R-734)
        print("ARRÊT : la carte n'a pas pu être fabriquée : %s: %s" % (type(e).__name__, e))
        return 2
    os.makedirs(os.path.dirname(os.path.abspath(sortie)), exist_ok=True)
    with open(sortie, "w", encoding="utf-8") as f:
        f.write(texte)
    print("carte écrite : %s" % sortie)
    for a in anomalies:
        print("ANOMALIE : %s" % a)
    return 1 if anomalies else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
