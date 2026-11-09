#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES DU COMPTE DES ESSAIS — lot S_kk de l'étape D, Jeu 05-11-2026 (Paris). Simulation uniquement.

① RÔLE — Prouver que le compte de k écrit dans `programmes/JUGE_DES_STRATEGIES.py` (`lecture_de_jeu`,
  `versions_du_registre`, `k_a_la_date`, et les quatre lectures extraites) applique la décision de Jean-Luc du
  05-11-2026 à 13h40 (Q-G5, « 1 ») : k compte chaque VERSION QUI CHANGE UN CALCUL ; la ligne 70 du fichier
  `donnees/cac40_strategies.csv` (C5-EI-PARAMS, entrée vide puis « DÉFAUT », mêmes 48 opérations) ne compte pas.
② CONTEXTE D'APPEL — À la main, par l'auteur du lot S_kk, son relecteur et Cowork. Aucune tâche du soir.
③ ENTRÉE — La ligne de commande : la racine d'un clone du dépôt ; option « --sabotages » pour jouer les seize
  sabotages K1 à K16 ; option « --un-sabotage=Kn » pour n'en jouer qu'un.
④ CONDITIONS D'ENTRÉE — La racine porte `programmes/` (le juge, le contrat), `donnees/cac40_strategies.csv` et
  `temoins/ETALON_DES_VERSIONS.csv` ; `git` est installé (dépôts jetables fabriqués ici).
⑤ SORTIE — Un affichage (une ligne par épreuve, puis une par sabotage) et un code de sortie : 0 si tout passe (et
  chaque sabotage joué rougit) ; 1 sinon ; 2 si la racine est inutilisable (R-734). [rend: 1]
⑥ TRAITEMENT — ① E1 l'étalon cas par cas · ② E2 le vrai registre · ③ E3 la trace (relevé `ast` contre relevé
  dynamique) · ④ E4 la forme du module (M1 de n°184) · ⑤ E5 k à la date sur des dépôts git jetables · ⑥ E6 une seule
  écriture de chaque lecture extraite, et aucune colonne du signal lue hors de `declaration_du_signal` · ⑦ avec sabotage : copier `programmes/`, le registre et l'étalon dans un
  dossier temporaire, réécrire UN endroit, rejouer ce programme sur la copie, exiger le code 1, remettre l'octet.
⑦ UNITÉ — Des versions, des cas, des essais.
⑧ POURQUOI — Un jeu d'épreuves se sabote contre sa propre correction (instructions du projet, §7). Les défauts D3 à D6
  de la relecture du tour 2 du lot C : l'étalon n'avait pas de dents sur la VÉRITÉ des cas ; c'est ici qu'il en a.
⑨ CE QUI CLOCHE — ① Le TOTAL des versions du vrai registre est affiché, jamais comparé à un chiffre (il grandit avec
  le registre). ② Les dépôts jetables ne portent que deux colonnes utiles changées ; l'histoire réelle du registre
  (réécritures de colonnes) n'est pas éprouvée. ③ La trace suit `jouer` et `juger` : ce que `main` lit seul
  (`etat_vie`) n'y est pas — le cas `etat_vie_ligne_jouee` de l'étalon le couvre.
⑩ EFFET — Crée et efface des dossiers temporaires ; lance `git` et `python3`. N'écrit rien sous la racine.
⑪ TERMINAISON — Sort du programme. Un appel à `git` ou au programme rejoué peut ne pas revenir (aucun délai posé
  pour git ; 120 s pour chaque rejeu).
  [sort: oui]
"""
import ast
import csv
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

JUGE = os.path.join("programmes", "JUGE_DES_STRATEGIES.py")
CONTRAT = os.path.join("programmes", "CONTRATS_DES_FICHIERS.py")
LECTURES_EXTRAITES = {   # chaque lecture extraite : les fonctions qui DOIVENT l'appeler (superviseur S_kk, §3.2)
    "mnemoniques_de_l_univers": {"jouer", "juger", "lecture_de_jeu"},
    "cle_d_entree": {"manques_du_jeu", "lecture_de_jeu"},
    "reglages_du_texte": {"manques_du_signal", "signal_de_la_fiche", "lecture_de_jeu"},
    "donnees_du_texte": {"manques_du_jeu", "lecture_de_jeu"},
    # la seule lecture des colonnes du signal (superviseur R-759 du lot S_kk, avant le tour 2, 17h33-17h38)
    "declaration_du_signal": {"manques_du_signal", "signal_de_la_fiche", "forme_du_module", "lecture_de_jeu"},
}


def charger(racine):
    """Charge le juge et le contrat de la racine.
    ① RÔLE — importer.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` : la racine éprouvée.
    ④ CONDITIONS D'ENTRÉE — `programmes/` y est.
    ⑤ SORTIE — DEUX valeurs : le juge, le contrat.
    [rend: 2]
    ⑥ TRAITEMENT — mettre `programmes/` en tête du chemin, importer.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — éprouver la racine
    donnée, pas une autre.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — exécute le chargement des deux modules.
    ⑪ TERMINAISON —
    Rend la main.
    [sort: non]"""
    sys.path.insert(0, os.path.join(racine, "programmes"))
    import JUGE_DES_STRATEGIES as J
    import CONTRATS_DES_FICHIERS as C
    return J, C


def module_du_jour(racine):
    """Rend `lire_module` sur les fichiers du jour.
    ① RÔLE — fournir l'octet au compteur.
    ② CONTEXTE D'APPEL — E1, E2,
    E3, E4.
    ③ ENTRÉE — `racine` : la racine éprouvée.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : une fonction (chemin, rang=None)
    → 16 caractères hexadécimaux ou None.
    [rend: 1]
    ⑥ TRAITEMENT — sha256 du fichier.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — au
    jour, le module du jour est le bon.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — lit des fichiers.
    ⑪ TERMINAISON — Rend la main.
    [sort: non]"""
    def lire(chemin, rang=None):
        """Empreinte du fichier du jour.
        ① RÔLE — lire.
        ② CONTEXTE D'APPEL — le juge.
        ③ ENTRÉE — `chemin` : le module · `rang` : ignoré (au jour, le module est celui du jour).
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur.
        [rend: 1]
        ⑥ TRAITEMENT — sha256.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — lit.
        ⑪ TERMINAISON — Rend la main.
        [sort: non]"""
        p = os.path.join(racine, chemin)
        return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16] if os.path.isfile(p) else None
    return lire


def e1_etalon(racine, J, C):
    """E1 — Chaque cas de l'étalon rend ses `versions_attendues` ; aucune faute ; cas confrontés = lignes de données.

    ① RÔLE — ce que dit la première phrase : une propriété éprouvée, jamais un total figé.
    ② CONTEXTE D'APPEL — `main`, une fois ; et chaque rejeu d'un sabotage.
    ③ ENTRÉE — `racine` : la racine éprouvée · `J` : le juge chargé · `C` : le contrat chargé.
    ④ CONDITIONS D'ENTRÉE — la racine porte le registre et l'étalon ; sinon l'épreuve lève et `main` la fait rougir.
    ⑤ SORTIE — DEUX valeurs : vrai si l'épreuve passe, et le détail affiché.
    [rend: 2]
    ⑥ TRAITEMENT — appeler les fonctions du juge, comparer à ce que la décision attend.
    ⑦ UNITÉ — des versions, des cas, des essais.
    ⑧ POURQUOI — superviseur S_kk, §3.4 ; défauts D3 à D6 de la relecture du tour 2 du lot C.
    ⑨ CE QUI CLOCHE — voir le ⑨ du programme.
    ⑩ EFFET — Aucun : lit des fichiers.
    ⑪ TERMINAISON — Rend la main, ou lève (rattrapé par `main`, qui fait rougir).
    [sort: non]"""
    cas, fautes = C.cas_de_l_etalon_des_versions(racine)
    with open(os.path.join(racine, C.ETALON_DES_VERSIONS), encoding="utf-8-sig", newline="") as f:
        lignes = [r for r in list(csv.reader(f))[1:] if any(x.strip() for x in r)]
    lm = module_du_jour(racine)
    faux = [(c["cas"], J.versions_du_registre([c["ligne_a"], c["ligne_b"]], lm)[1], c["versions_attendues"])
            for c in cas]
    faux = [x for x in faux if x[1] != x[2]]
    ok = not fautes and not faux and len(cas) == len(lignes)
    return ok, f"{len(cas)} cas confrontés sur {len(lignes)} lignes de l'étalon ; fautes : {fautes or 'aucune'} ; " \
               f"cas faux (cas, rendu, attendu) : {faux or 'aucun'}"


def e2_vrai_registre(racine, J, C):
    """E2 — Le vrai registre : lignes 65 et 70 du fichier (C5-EI-PARAMS) = 1 version ; chaque fiche entre 1 et son
    nombre de lignes ; le total est AFFICHÉ, jamais comparé.

    ① RÔLE — ce que dit la première phrase : une propriété éprouvée, jamais un total figé.
    ② CONTEXTE D'APPEL — `main`, une fois ; et chaque rejeu d'un sabotage.
    ③ ENTRÉE — `racine` : la racine éprouvée · `J` : le juge chargé · `C` : le contrat chargé.
    ④ CONDITIONS D'ENTRÉE — la racine porte le registre et l'étalon ; sinon l'épreuve lève et `main` la fait rougir.
    ⑤ SORTIE — DEUX valeurs : vrai si l'épreuve passe, et le détail affiché.
    [rend: 2]
    ⑥ TRAITEMENT — appeler les fonctions du juge, comparer à ce que la décision attend.
    ⑦ UNITÉ — des versions, des cas, des essais.
    ⑧ POURQUOI — superviseur S_kk, §3.4 ; défauts D3 à D6 de la relecture du tour 2 du lot C.
    ⑨ CE QUI CLOCHE — voir le ⑨ du programme.
    ⑩ EFFET — Aucun : lit des fichiers.
    ⑪ TERMINAISON — Rend la main, ou lève (rattrapé par `main`, qui fait rougir).
    [sort: non]"""
    lignes = C.lignes_du_registre(os.path.join(racine, C.REGISTRE_DES_STRATEGIES))
    l65, l70 = lignes[65 - 2], lignes[70 - 2]
    paire = J.versions_du_registre([l65, l70], module_du_jour(racine))[1]
    par_fiche, total = J.versions_du_registre(lignes, module_du_jour(racine))
    nb = {}
    for l in lignes:
        nb[l["id"]] = nb.get(l["id"], 0) + 1
    hors = sorted(f for f in nb if not 1 <= par_fiche.get(f, 0) <= nb[f])
    ok = (l65["id"] == l70["id"] == "C5-EI-PARAMS" and paire == 1 and par_fiche.get("C5-EI-PARAMS") == 1 and not hors)
    return ok, f"lignes 65/70 : {paire} version(s) ; C5-EI-PARAMS au registre : {par_fiche.get('C5-EI-PARAMS')} ; " \
               f"fiches hors [1, lignes] : {hors or 'aucune'} ; TOTAL AFFICHÉ : {total} versions, {len(lignes)} " \
               f"lignes, {len(nb)} fiches"


def releve_statique(source):
    """Clés lues sur le paramètre `fiche` dans `jouer`, `juger` et toute fonction à paramètre `fiche` qu'elles
    appellent (de proche en proche).
    ① RÔLE — le relevé `ast` de la trace (point 7 du superviseur du lot C).
    ② CONTEXTE D'APPEL — E3.
    ③ ENTRÉE — `source` : le texte d'un programme.
    ④ CONDITIONS D'ENTRÉE — il se lit en Python.
    ⑤ SORTIE — UNE valeur : l'ensemble des clés.
    [rend: 1]
    ⑥ TRAITEMENT — `fiche["x"]`, `fiche.get("x")`, et un texte
    constant passé À CÔTÉ de `fiche` dans un appel (`seuil_de_la_fiche(fiche, "tp")`).
    ⑦ UNITÉ — des noms de cases.
    ⑧ POURQUOI — ce que le jeu lit doit entrer dans la lecture.
    ⑨ CE QUI CLOCHE — une clé lue par une variable n'est
    pas vue.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
    [sort: non]"""
    arbre = ast.parse(source)
    defs = {n.name: n for n in arbre.body if isinstance(n, ast.FunctionDef)}
    a_voir, vues, cles = ["jouer", "juger"], set(), set()
    while a_voir:
        nom = a_voir.pop()
        if nom in vues or nom not in defs or "fiche" not in [p.arg for p in defs[nom].args.args]:
            continue
        vues.add(nom)
        for n in ast.walk(defs[nom]):
            if (isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name) and n.value.id == "fiche"
                    and isinstance(n.slice, ast.Constant)):
                cles.add(n.slice.value)
            if isinstance(n, ast.Call):
                f = n.func
                if (isinstance(f, ast.Attribute) and f.attr == "get" and isinstance(f.value, ast.Name)
                        and f.value.id == "fiche" and n.args and isinstance(n.args[0], ast.Constant)):
                    cles.add(n.args[0].value)
                if any(isinstance(a, ast.Name) and a.id == "fiche" for a in n.args):
                    cles |= {a.value for a in n.args if isinstance(a, ast.Constant) and isinstance(a.value, str)}
                    if isinstance(f, ast.Name):
                        a_voir.append(f.id)
    return cles


class Trace(dict):
    """Un dictionnaire qui retient les clés lues. ① RÔLE — le relevé dynamique. ② CONTEXTE D'APPEL — E3. ③ ENTRÉE — une
    ligne. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — — ⑥ TRAITEMENT — noter chaque lecture. ⑦ UNITÉ — — ⑧ POURQUOI — voir
    ce que `lecture_de_jeu` lit. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — —"""

    def __init__(self, *a):
        """Initialise.
        ① RÔLE — copier.
        ② CONTEXTE D'APPEL — E3.
        ③ ENTRÉE — `self` : la trace · `*a` : la ligne à copier.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — —
        [rend: rien]
        ⑥ TRAITEMENT — copier, vider les lues.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main.
        [sort: non]"""
        super().__init__(*a)
        self.lues = set()

    def get(self, k, d=None):
        """Lit et note.
        ① RÔLE — lire.
        ② CONTEXTE D'APPEL — le juge.
        ③ ENTRÉE — `self` : la trace · `k` : la case · `d` : le défaut.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur.
        [rend: 1]
        ⑥ TRAITEMENT — noter, lire.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main.
        [sort: non]"""
        self.lues.add(k)
        return super().get(k, d)

    def __getitem__(self, k):
        """Lit et note.
        ① RÔLE — lire.
        ② CONTEXTE D'APPEL — le juge.
        ③ ENTRÉE — `self` : la trace · `k` : la case.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur.
        [rend: 1]
        ⑥ TRAITEMENT — noter, lire.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — —.
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main ; KeyError si absente.
        [sort: non]"""
        self.lues.add(k)
        return super().__getitem__(k)


def e3_trace(racine, J, C):
    """E3 — Clés lues par le jeu ⊆ clés lues par `lecture_de_jeu` pour sa valeur ∪ {la clé qui fait la fiche}.
    Calibrage : le relevé trouve univers, horizon, tp, sl ; il trouve « zzz » dans une fonction fabriquée.

    ① RÔLE — ce que dit la première phrase : une propriété éprouvée, jamais un total figé.
    ② CONTEXTE D'APPEL — `main`, une fois ; et chaque rejeu d'un sabotage.
    ③ ENTRÉE — `racine` : la racine éprouvée · `J` : le juge chargé · `C` : le contrat chargé.
    ④ CONDITIONS D'ENTRÉE — la racine porte le registre et l'étalon ; sinon l'épreuve lève et `main` la fait rougir.
    ⑤ SORTIE — DEUX valeurs : vrai si l'épreuve passe, et le détail affiché.
    [rend: 2]
    ⑥ TRAITEMENT — appeler les fonctions du juge, comparer à ce que la décision attend.
    ⑦ UNITÉ — des versions, des cas, des essais.
    ⑧ POURQUOI — superviseur S_kk, §3.4 ; défauts D3 à D6 de la relecture du tour 2 du lot C.
    ⑨ CE QUI CLOCHE — voir le ⑨ du programme.
    ⑩ EFFET — Aucun : lit des fichiers.
    ⑪ TERMINAISON — Rend la main, ou lève (rattrapé par `main`, qui fait rougir).
    [sort: non]"""
    statique = releve_statique(open(os.path.join(racine, JUGE), encoding="utf-8").read())
    fabrique = releve_statique("def jouer(fiche):\n    return aide(fiche)\n\ndef aide(fiche):\n    return fiche['zzz']\n")
    lignes = C.lignes_du_registre(os.path.join(racine, C.REGISTRE_DES_STRATEGIES))
    t = Trace(lignes[70 - 2])
    valeur = J.lecture_de_jeu(t, module_du_jour(racine))
    cle_de_fiche = {"id"}   # la clé qui fait la fiche : égale par construction entre deux lignes comparées
    manquent = sorted(statique - t.lues - cle_de_fiche)
    calibre = {"univers", "horizon", "tp", "sl"} <= statique and "zzz" in fabrique and "zzz" not in t.lues
    ok = valeur[0] == "JOUABLE" and not manquent and calibre
    return ok, f"lues par le jeu : {sorted(statique)} ; non lues par la lecture : {manquent or 'aucune'} ; " \
               f"calibrage (univers, horizon, tp, sl trouvés ; zzz trouvé dans la fonction fabriquée) : {calibre}"


def e4_forme_du_module(racine, J, C):
    """E4 — M1 (n°184) au sens de la lecture : un cas signal à 2 versions sur une ligne « module déclaré » (l.70) et
    un sur une ligne « sans module » (l.6) ; un module déclaré mais introuvable (renommé, ou inexistant sur la l.6)
    reste « module déclaré, introuvable ».

    ① RÔLE — ce que dit la première phrase : une propriété éprouvée, jamais un total figé.
    ② CONTEXTE D'APPEL — `main`, une fois ; et chaque rejeu d'un sabotage.
    ③ ENTRÉE — `racine` : la racine éprouvée · `J` : le juge chargé · `C` : le contrat chargé.
    ④ CONDITIONS D'ENTRÉE — la racine porte le registre et l'étalon ; sinon l'épreuve lève et `main` la fait rougir.
    ⑤ SORTIE — DEUX valeurs : vrai si l'épreuve passe, et le détail affiché.
    [rend: 2]
    ⑥ TRAITEMENT — appeler les fonctions du juge, comparer à ce que la décision attend.
    ⑦ UNITÉ — des versions, des cas, des essais.
    ⑧ POURQUOI — superviseur S_kk, §3.4 ; défauts D3 à D6 de la relecture du tour 2 du lot C.
    ⑨ CE QUI CLOCHE — voir le ⑨ du programme.
    ⑩ EFFET — Aucun : lit des fichiers.
    ⑪ TERMINAISON — Rend la main, ou lève (rattrapé par `main`, qui fait rougir).
    [sort: non]"""
    cas, _ = C.cas_de_l_etalon_des_versions(racine)
    lm = module_du_jour(racine)
    par_nom = {c["cas"]: c for c in cas}
    f70 = J.forme_du_module(par_nom["reglages_du_signal"]["ligne_a"], lm)[0]
    f6 = J.forme_du_module(par_nom["cci_14_20_sans_module"]["ligne_a"], lm)[0]
    renomme = dict(par_nom["reglages_du_signal"]["ligne_a"])
    renomme["module_signal"] = "programmes/MODULE_C5_ETENDU_10_RENOMME_PAR_L_EPREUVE.py"
    inexistant = dict(par_nom["cci_14_20_sans_module"]["ligne_a"])
    inexistant["module_signal"] = "programmes/MODULE_INEXISTANT_DE_L_EPREUVE.py"
    fr, fi = J.forme_du_module(renomme, lm)[0], J.forme_du_module(inexistant, lm)[0]
    deux = (par_nom["reglages_du_signal"]["versions_attendues"] == 2
            and par_nom["cci_14_20_sans_module"]["versions_attendues"] == 2)
    ok = (deux and f70 == "module déclaré" and f6 == "sans module" and fr == fi == "module déclaré, introuvable")
    return ok, f"l.70 : {f70} ; l.6 : {f6} ; l.70 module renommé : {fr} ; l.6 module inexistant : {fi}"


def git(dossier, *args, date=None):
    """Lance git dans un dépôt jetable.
    ① RÔLE — fabriquer l'histoire.
    ② CONTEXTE D'APPEL — E5.
    ③ ENTRÉE — `dossier` : le dépôt jetable · `*args` : les arguments de git · `date` : la date ISO du commit, ou None.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la sortie texte.
    [rend: 1]
    ⑥ TRAITEMENT — dates de commit fixées.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — histoire reproductible.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — écrit dans le dépôt jetable.
    ⑪ TERMINAISON — Rend la main ; lève si git échoue.
    [sort: non]"""
    env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    if date:
        env.update(GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date)
    return subprocess.run(["git", "-C", dossier, "-c", "user.name=epreuve", "-c", "user.email=epreuve@local",
                           "-c", "commit.gpgsign=false"] + list(args),
                          env=env, check=True, capture_output=True, text=True).stdout


def e5_k_a_la_date(racine, J, C):
    """E5 — k à la date, sur un dépôt jetable : 2026-01-10 ligne ZZ-1 (module v1) ; 2026-02-10 ligne ZZ-1 identique,
    module v2 ; 2026-03-10 ligne ZZ-2. Au 15-02 avec 2 témoins : 2 versions, k = 4. « aucun » = 0. Avant le premier
    commit : INCONNU. Clone superficiel au 01-04 : INCONNU.

    ① RÔLE — ce que dit la première phrase : une propriété éprouvée, jamais un total figé.
    ② CONTEXTE D'APPEL — `main`, une fois ; et chaque rejeu d'un sabotage.
    ③ ENTRÉE — `racine` : la racine éprouvée · `J` : le juge chargé · `C` : le contrat chargé.
    ④ CONDITIONS D'ENTRÉE — la racine porte le registre et l'étalon ; sinon l'épreuve lève et `main` la fait rougir.
    ⑤ SORTIE — DEUX valeurs : vrai si l'épreuve passe, et le détail affiché.
    [rend: 2]
    ⑥ TRAITEMENT — appeler les fonctions du juge, comparer à ce que la décision attend.
    ⑦ UNITÉ — des versions, des cas, des essais.
    ⑧ POURQUOI — superviseur S_kk, §3.4 ; défauts D3 à D6 de la relecture du tour 2 du lot C.
    ⑨ CE QUI CLOCHE — voir le ⑨ du programme.
    ⑩ EFFET — crée et efface un dépôt git jetable et un clone superficiel, dans un dossier temporaire.
    ⑪ TERMINAISON — Rend la main, ou lève (rattrapé par `main`, qui fait rougir).
    [sort: non]"""
    lignes = C.lignes_du_registre(os.path.join(racine, C.REGISTRE_DES_STRATEGIES))
    entete = list(lignes[0].keys())
    modele = dict(lignes[70 - 2])
    modele["module_signal"] = "programmes/MODULE_DE_L_EPREUVE.py"
    with tempfile.TemporaryDirectory() as tmp:
        d = os.path.join(tmp, "depot")
        os.makedirs(os.path.join(d, os.path.dirname(C.REGISTRE_DES_STRATEGIES)))
        os.makedirs(os.path.join(d, "programmes"))
        git(d, "init", "-q")

        def ecrire(ids, module, date):
            """Écrit le registre et le module, commite.
            ① RÔLE — un pas d'histoire.
            ② CONTEXTE D'APPEL — E5.
            ③ ENTRÉE — `ids` : les identifiants des lignes · `module` : le texte du module · `date` : la date ISO.
            ④ CONDITIONS D'ENTRÉE — —
            ⑤ SORTIE — —
            [rend: rien]
            ⑥ TRAITEMENT — écrire,
            commiter.
            ⑦ UNITÉ — —
            ⑧ POURQUOI — —.
            ⑨ CE QUI CLOCHE — —
            ⑩ EFFET — écrit.
            ⑪ TERMINAISON — Rend la main.
            [sort: non]"""
            with open(os.path.join(d, C.REGISTRE_DES_STRATEGIES), "w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=entete, lineterminator="\n")
                w.writeheader()
                for i in ids:
                    w.writerow(dict(modele, id=i))
            with open(os.path.join(d, "programmes", "MODULE_DE_L_EPREUVE.py"), "w", encoding="utf-8") as f:
                f.write(module)
            git(d, "add", "-A")
            git(d, "commit", "-q", "-m", "pas " + date, date=date)

        ecrire(["ZZ-1"], "# v1\n", "2026-01-10T12:00:00+01:00")
        ecrire(["ZZ-1", "ZZ-1"], "# v2\n", "2026-02-10T12:00:00+01:00")
        ecrire(["ZZ-1", "ZZ-1", "ZZ-2"], "# v2\n", "2026-03-10T12:00:00+01:00")
        k, raison = J.k_a_la_date(d, "2026-02-15T12:00+01:00", 2)
        k0, _ = J.k_a_la_date(d, "2026-02-15T12:00+01:00", "aucun")
        kav, raison_av = J.k_a_la_date(d, "2025-12-01T12:00+01:00", 0)
        s = os.path.join(tmp, "superficiel")
        subprocess.run(["git", "clone", "-q", "--depth", "1", "file://" + d, s], check=True, capture_output=True)
        ks, raison_s = J.k_a_la_date(s, "2026-04-01T12:00+01:00", 0)
    ok = (not raison and k["valeur"] == 4 and k["versions_comptees"] == 2 and k["lignes_du_registre"] == 2
          and k["temoins"] == 2 and k["compte"] == C.COMPTES_DE_K[0] and set(k) == set(C.K_DU_VERDICT)
          and k0["valeur"] == 2 and kav["valeur"] == "INCONNU" and raison_av and ks["valeur"] == "INCONNU"
          and raison_s)
    return ok, f"au 15-02, 2 témoins : valeur {k['valeur']}, versions {k['versions_comptees']}, lignes " \
               f"{k['lignes_du_registre']}, témoins {k['temoins']} ; « aucun » : {k0['valeur']} ; avant tout commit : " \
               f"{kav['valeur']} ; clone superficiel : {ks['valeur']} ({raison_s})"


def e6_une_seule_ecriture(racine, J, C):
    """E6 — Chaque lecture extraite a UNE définition et est appelée par chacun de ses appelants (K15) ; aucune
    fonction du juge autre que `declaration_du_signal` ne lit une colonne du signal par son nom (K16).

    ① RÔLE — ce que dit la première phrase : une propriété éprouvée, jamais un total figé.
    ② CONTEXTE D'APPEL — `main`, une fois ; et chaque rejeu d'un sabotage.
    ③ ENTRÉE — `racine` : la racine éprouvée · `J` : le juge chargé · `C` : le contrat chargé.
    ④ CONDITIONS D'ENTRÉE — la racine porte le registre et l'étalon ; sinon l'épreuve lève et `main` la fait rougir.
    ⑤ SORTIE — DEUX valeurs : vrai si l'épreuve passe, et le détail affiché.
    [rend: 2]
    ⑥ TRAITEMENT — appeler les fonctions du juge, comparer à ce que la décision attend.
    ⑦ UNITÉ — des versions, des cas, des essais.
    ⑧ POURQUOI — superviseur S_kk, §3.4 ; défauts D3 à D6 de la relecture du tour 2 du lot C.
    ⑨ CE QUI CLOCHE — voir le ⑨ du programme.
    ⑩ EFFET — Aucun : lit des fichiers.
    ⑪ TERMINAISON — Rend la main, ou lève (rattrapé par `main`, qui fait rougir).
    [sort: non]"""
    arbre = ast.parse(open(os.path.join(racine, JUGE), encoding="utf-8").read())
    defs = [n for n in arbre.body if isinstance(n, ast.FunctionDef)]
    fautes = []
    for lecture, appelants in LECTURES_EXTRAITES.items():
        if sum(1 for n in defs if n.name == lecture) != 1:
            fautes.append(f"{lecture} : définie {sum(1 for n in defs if n.name == lecture)} fois")
        for n in defs:
            appelle = any(isinstance(x, ast.Call) and isinstance(x.func, ast.Name) and x.func.id == lecture
                          for x in ast.walk(n))
            if n.name in appelants and not appelle:
                fautes.append(f"{n.name} n'appelle pas {lecture}")
    # aucune lecture d'une colonne du signal, par son nom, hors de `declaration_du_signal` (superviseur R-759 du lot
    # S_kk, 17h33-17h38) : `fiche["x"]` ou `fiche.get("x")`, partout dans le juge sauf dans la lecture unique
    permis = {id(x) for n in defs if n.name == "declaration_du_signal" for x in ast.walk(n)}
    for x in ast.walk(arbre):
        cle = None
        if isinstance(x, ast.Subscript) and isinstance(x.slice, ast.Constant):
            cle = x.slice.value
        elif (isinstance(x, ast.Call) and isinstance(x.func, ast.Attribute) and x.func.attr == "get" and x.args
              and isinstance(x.args[0], ast.Constant)):
            cle = x.args[0].value
        if cle in J.COLONNES_DU_SIGNAL and id(x) not in permis:
            fautes.append(f"l.{x.lineno} lit {cle} hors de declaration_du_signal")
    return not fautes, f"{len(LECTURES_EXTRAITES)} lectures extraites ; fautes : {fautes or 'aucune'}"


EPREUVES = (e1_etalon, e2_vrai_registre, e3_trace, e4_forme_du_module, e5_k_a_la_date, e6_une_seule_ecriture)

# LES SABOTAGES (superviseur S_kk, §4.3) : {nom : (fichier, texte exact, remplacement, ce qui doit rougir)}.
SABOTAGES = {
    "K1": (JUGE, '            copie["entree"] = "DÉFAUT"\n', '            pass\n', "plus de vide → DÉFAUT"),
    "K2": (JUGE, 'seuil_de_la_fiche(fiche, "tp"), seuil_de_la_fiche(fiche, "sl"),',
           'fiche["tp"], seuil_de_la_fiche(fiche, "sl"),', "tp comparé en texte"),
    "K3": (JUGE, 'VIDE = ("", "-", "\\u2014", ', 'VIDE = ("", "-", ', "« — » retiré de VIDE"),
    "K4": (CONTRAT, "    une_version, deux_versions = VERSIONS_D_UN_CAS\n",
           "    return [], []\n    une_version, deux_versions = VERSIONS_D_UN_CAS\n", "étalon non lu"),
    "K5": (JUGE, "    lue = _FicheLue(fiche)\n    rendu = porte_0(lue)\n",
           "    return (\"CONSTANTE\",)\n    lue = _FicheLue(fiche)\n    rendu = porte_0(lue)\n", "lecture constante"),
    "K6": (JUGE, '    demandes = mnemoniques_de_l_univers(fiche["univers"])\n',
           '    _filtres = fiche.get("filtres")\n    demandes = mnemoniques_de_l_univers(fiche["univers"])\n',
           "jouer lit filtres"),
    "K7": (JUGE, 'frozenset(mnemoniques_de_l_univers(fiche["univers"]))', 'tuple(mnemoniques_de_l_univers(fiche["univers"]))',
           "univers en liste"),
    "K8": (JUGE, "        if ident not in precedente or precedente[ident] != lue:\n", "        if True:\n",
           "chaque ligne compte"),
    "K9": (JUGE, '"--before=" + date_declaration, "HEAD"', '"HEAD"', "date ignorée"),
    "K10": (JUGE, 'git("show", "%s:%s" % (sha, chemin_module)) if sha else (1, b"")',
            'git("show", "HEAD:%s" % chemin_module)', "empreinte du module du jour"),
    "K11": (JUGE, 'frozenset(donnees_du_texte(fiche["donnees_demandees"])))',
            'frozenset(donnees_du_texte(fiche["donnees_demandees"])), fiche.get("etat_vie"))', "etat_vie dans la lecture"),
    "K12": (JUGE, '    if code != 0 or sortie.strip() != b"false":\n', '    if False:\n', "histoire absente ignorée"),
    "K13": (JUGE, "valeur=total + nb_temoins,", "valeur=total,", "témoins oubliés"),
    "K14": (JUGE, '    if chemin.lower() in VIDE:\n        return "sans module", None\n',
            '    if chemin.lower() in VIDE or not os.path.isfile(chemin):\n        return "sans module", None\n',
            "« avec module » par l'existence du fichier"),
    "K15": (JUGE, '    demandes = mnemoniques_de_l_univers(fiche["univers"])\n',
            '    demandes = [x.strip().upper() for x in fiche["univers"].split(",") if x.strip()]\n',
            "univers relu en ligne dans jouer"),
    # superviseur R-759 du lot S_kk, avant le tour 2 : la même relecture que S11 de l'épreuve du signal nommé
    "K16": (JUGE, "            forme, emp, fonction,\n", "            forme, emp, fiche[\"fonction_signal\"].strip(),\n",
            "fonction_signal relue dans la lecture de jeu"),
}


def jouer_les_sabotages(racine, noms):
    """Joue chaque sabotage sur une COPIE, exige le code 1, remet l'octet.
    ① RÔLE — prouver que les épreuves mordent.
    ② CONTEXTE D'APPEL — `main`.
    ③ ENTRÉE — `racine` : la racine éprouvée · `noms` : les sabotages à jouer.
    ④ CONDITIONS D'ENTRÉE — chaque texte exact est
    présent UNE fois.
    ⑤ SORTIE — UNE valeur : le nombre de sabotages restés verts ou injouables.
    [rend: 1]
    ⑥ TRAITEMENT — copier `programmes/`, le registre, l'étalon ; pour chacun : réécrire, rejouer, remettre, vérifier
    l'empreinte.
    ⑦ UNITÉ — des sabotages.
    ⑧ POURQUOI — une épreuve verte sans ce qu'elle teste est une décoration.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — écrit dans un dossier temporaire, l'efface.
    ⑪ TERMINAISON — Rend la main ; un
    rejeu est borné à 120 s.
    [sort: non]"""
    ratés = 0
    with tempfile.TemporaryDirectory() as tmp:
        copie = os.path.join(tmp, "copie")
        shutil.copytree(os.path.join(racine, "programmes"), os.path.join(copie, "programmes"),
                        ignore=shutil.ignore_patterns("__pycache__"))
        sys.path.insert(0, os.path.join(racine, "programmes"))
        import CONTRATS_DES_FICHIERS as C   # le nom du registre se lit au contrat (G1 de EPREUVES_DU_REGISTRE_DES_STRATEGIES)
        for f in (C.REGISTRE_DES_STRATEGIES, "temoins/ETALON_DES_VERSIONS.csv"):
            os.makedirs(os.path.join(copie, os.path.dirname(f)), exist_ok=True)
            shutil.copy2(os.path.join(racine, f), os.path.join(copie, f))
        for nom in noms:
            fichier, avant, apres, quoi = SABOTAGES[nom]
            p = os.path.join(copie, fichier)
            octets = open(p, "rb").read()
            texte = octets.decode("utf-8")
            if texte.count(avant) != 1:
                print(f"  {nom} INJOUABLE — le texte à saboter est présent {texte.count(avant)} fois ({quoi})")
                ratés += 1
                continue
            open(p, "w", encoding="utf-8").write(texte.replace(avant, apres))
            r = subprocess.run([sys.executable, "-I", "-B", os.path.abspath(__file__), copie],
                               capture_output=True, text=True, timeout=120)
            open(p, "wb").write(octets)
            if hashlib.sha256(open(p, "rb").read()).digest() != hashlib.sha256(octets).digest():
                print(f"  {nom} : la copie n'a pas été remise à l'octet")
                ratés += 1
            rouges = [l.split(" ")[1] for l in r.stdout.splitlines() if l.startswith("ROUGE ")]
            if r.returncode == 1 and rouges:
                print(f"  {nom} MORD — {quoi} — code 1 ; rouges : {', '.join(rouges)}")
            else:
                print(f"  {nom} MUET — {quoi} — code {r.returncode} ; rouges : {', '.join(rouges) or 'aucun'}")
                ratés += 1
    return ratés


def main():
    """Joue les épreuves, puis les sabotages demandés.
    ① RÔLE — le programme.
    ② CONTEXTE D'APPEL — la ligne de
    commande.
    ③ ENTRÉE — sys.argv (aucun paramètre).
    ④ CONDITIONS D'ENTRÉE — une racine.
    ⑤ SORTIE — —
    [rend: rien]
    ⑥ TRAITEMENT — E1 à E6, puis
    les sabotages.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — —.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — affiche.
    ⑪ TERMINAISON — Sort du
    programme avec 0, 1 ou 2.
    [sort: oui]"""
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    options = [a for a in sys.argv[1:] if a.startswith("--")]
    if len(args) != 1 or not os.path.isfile(os.path.join(args[0], JUGE)):
        print("usage : EPREUVES_DU_COMPTE_DES_ESSAIS_Jeu_05-11-2026.py <racine> [--sabotages | --un-sabotage=Kn]")
        sys.exit(2)
    racine = os.path.realpath(args[0])
    os.chdir(racine)
    J, C = charger(racine)
    rouge = 0
    for e in EPREUVES:
        try:
            ok, detail = e(racine, J, C)
        except Exception as x:   # une épreuve qui n'a pas pu tourner rougit (R-734)
            ok, detail = False, f"n'a pas pu tourner : {type(x).__name__} : {x}"
        print(("VERT  " if ok else "ROUGE ") + e.__name__.split("_")[0].upper() + " — " + detail)
        rouge += not ok
    noms = []
    for o in options:
        if o == "--sabotages":
            noms = list(SABOTAGES)
        elif o.startswith("--un-sabotage=") and o.split("=", 1)[1] in SABOTAGES:
            noms = [o.split("=", 1)[1]]
        else:
            print(f"option inconnue : {o}")
            sys.exit(2)
    if noms:
        print(f"SABOTAGES ({len(noms)}), chacun doit rougir :")
        rates = jouer_les_sabotages(racine, noms)
        print(f"sabotages qui mordent : {len(noms) - rates} sur {len(noms)}")
        rouge += rates
    sys.exit(1 if rouge else 0)


if __name__ == "__main__":
    main()
