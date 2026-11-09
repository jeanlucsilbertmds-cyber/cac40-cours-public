#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES DES CONTRATS DE LA LOI — lot C de l'étape D, Jeu 05-11-2026 (Paris). Simulation uniquement.

① RÔLE — Prouver que les contrats écrits par le lot C dans `programmes/CONTRATS_DES_FICHIERS.py` (la déclaration
  datée et ses champs P0, l'entrée du registre des essais, le verdict, le tableau de bord, les fichiers « à venir »)
  MORDENT : chaque épreuve fait une faute connue et exige que la confrontation la voie. Le superviseur R-759 « avant D »
  (05-11-2026, §1 « C ») a fixé trois sabotages qui doivent faire rougir `CONFRONTER_AUX_CONTRATS.py` : retirer un champ
  P0, retirer le champ k du verdict, ajouter une colonne au registre sans contrat (« il est vert et muet aujourd'hui
  sur B. Il faut donc prouver qu'il peut rougir avant de s'en servir comme preuve »).
② CONTEXTE D'APPEL — À la main, par l'auteur du lot C, son relecteur et Cowork. Aucune tâche du soir.
③ ENTRÉE — La ligne de commande : la racine d'un clone du dépôt ; option « --saboter » pour jouer en plus les sabotages
  du code éprouvé ET de l'étalon des versions (`temoins/ETALON_DES_VERSIONS.csv`) ; option « --div=<racine d'un dépôt
  du lot DIV> », où C17 lit les en-têtes RÉELS des deux fichiers du lot DIV au commit COMMIT_DU_LOT_DIV (inutile
  quand les deux fichiers existent sous la racine, après l'assemblage de D).
④ CONDITIONS D'ENTRÉE — La racine porte `programmes/CONTRATS_DES_FICHIERS.py`, `programmes/CONFRONTER_AUX_CONTRATS.py`,
  `gouvernance/REGISTRE_REGLES.md`, et chaque fichier nommé par CONTRATS_PAR_FICHIER exactement une fois (hors .git).
  Pour C17 : les deux fichiers du lot DIV sous la racine, ou « --div » vers un dépôt qui porte le commit
  COMMIT_DU_LOT_DIV ; sinon C17 rougit (un contrôle qui n'a pas pu tourner ne passe jamais, R-734).
⑤ SORTIE — Un affichage (une ligne par épreuve, puis une par sabotage) et un code de sortie : 0 si toutes les épreuves
  passent (et, avec --saboter, si chaque sabotage fait rougir au moins une épreuve) ; 1 sinon ; 2 si la racine ne
  permet pas de bâtir la copie (un contrôle qui n'a pas pu tourner ne rend jamais 0, R-734). [rend: 1]
⑥ TRAITEMENT — ① bâtir une COPIE RÉDUITE dans un dossier temporaire : les deux programmes, et chaque fichier sous
  contrat à son chemin réel, réduit à ses premières lignes (le registre des stratégies entier) — la confrontation ne
  lit que l'en-tête · ② jouer les épreuves C01 à C20 sur cette copie, chacune dans sa propre copie · ③ avec --saboter,
  pour chaque sabotage : réécrire le module, ou l'étalon des versions, dans une copie neuve, rejouer toutes les
  épreuves, exiger au moins un rouge.
⑦ UNITÉ — Des épreuves et des écarts.
⑧ POURQUOI — Un jeu d'épreuves se sabote contre sa propre correction : une épreuve qui reste verte quand on retire ce
  qu'elle teste est une décoration (instructions du projet, §7). Les objets fabriqués (verdict, déclarations) sont
  écrits ICI avec des clés littérales, jamais tirés du contrat : tirés du contrat, ils suivraient son sabotage et
  l'épreuve ne mordrait plus.
⑨ CE QUI CLOCHE — ① Les CHIFFRES des objets fabriqués (k, seuils, gains) sont des valeurs de forme, inventées pour
  l'épreuve : aucun n'est une mesure. ② Les deux entrées du registre des essais (C08) sont les octets écrits le
  05-11-2026 à 13h14 par le vrai écrivain du lot L4 (`lot_L4/programmes/TENIR_LE_REGISTRE_DES_ESSAIS.py`, empreinte git
  0aea573), recopiés ici : le jour où L4 change sa forme, ce cas ne le voit pas — la confrontation du dossier réel, si.
  ③ La copie réduite ne garde que les premières lignes : un défaut au-delà n'est pas l'affaire de la confrontation.
  ④ C18 et C19 éprouvent l'ÉTALON des versions (forme, ancres, couverture), JAMAIS un compte : aucune lecture de jeu
  n'est écrite ici (le témoin `_versions` du premier tour a été retiré, seconde lecture du juge, R-708). Les
  sabotages de l'étalon portent sur sa FORME, pas sur la vérité de ses cas : que chaque cas soit VRAI, seule la
  fonction que le lot S_kk écrit dans le juge le dira, à l'épreuve de S_kk (superviseur R-759 du 05-11-2026,
  15h55-15h57, D3). ⑤ C19 lit les colonnes
  par leur NOM dans deux fichiers du juge : une lecture par une variable (`fiche[nom]`) ne se voit pas, et un nom lu
  sur un autre objet que la fiche (« wr ») se voit et doit être couvert. ⑥ C17 lit le lot DIV à UN commit nommé
  (COMMIT_DU_LOT_DIV) : quand DIV avance, C17 confronte encore l'ancien commit jusqu'à ce qu'on change ce nom — le
  contrat, lui, n'en garde aucune copie. Le jour où les deux fichiers passent dans CONTRATS_PAR_FICHIER (assemblage
  de D), la copie réduite les porte et le cas « absents, muets » de C17 est à revoir dans le même geste.
⑩ EFFET — Écrit dans un dossier temporaire, effacé à la fin ; ne touche pas à la racine ; lit le dépôt DIV par
  « git show » sans l'écrire ; aucun réseau.
⑪ TERMINAISON — Sort du programme. Les sous-processus (C01) ont une limite de 120 s. [sort: oui]

USAGE : python3 tests/EPREUVES_DES_CONTRATS_DE_LA_LOI_Jeu_05-11-2026.py <racine> [--saboter] [--div=<dépôt DIV>]
"""
import ast
import copy
import csv
import importlib.util
import inspect
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

CONTRATS = os.path.join("programmes", "CONTRATS_DES_FICHIERS.py")
CONFRONTER = os.path.join("programmes", "CONFRONTER_AUX_CONTRATS.py")
REGISTRE_DES_REGLES = os.path.join("gouvernance", "REGISTRE_REGLES.md")
LIGNES_GARDEES = 20            # premières lignes gardées d'un fichier sous contrat : la confrontation ne lit que l'en-tête
TAILLE_GARDEE_ENTIERE = 400_000  # octets : sous cette taille, le fichier est copié entier (le registre des stratégies)
REGARD = "2026-11-20T20:00:00+01:00"   # date de regard fabriquée pour C10 et C16

# Le verdict fabriqué : clés LITTÉRALES (⑧). Chiffres de forme (⑨ ①).
def _c(etat, role="CONDITION", detail=None, raison=""):
    """Fabrique un contrôle de verdict aux clés littérales.

    ① RÔLE — Écrire un contrôle sans tirer ses clés du contrat. ② CONTEXTE D'APPEL — `verdict_etalon`.
    ③ ENTRÉE — l'état, le rôle, le détail, la raison. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire. [rend: 1] ⑥ TRAITEMENT — le composer. ⑦ UNITÉ — —
    ⑧ POURQUOI — voir ⑧ du programme. ⑨ CE QUI CLOCHE — — ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    return {"etat": etat, "valeur": None, "seuil": None, "raison": raison, "role": role, "detail": detail or {}}


def verdict_etalon():
    """Rend un verdict complet, conforme au contrat VERDICT, écrit à la main avec des clés littérales.

    ① RÔLE — Le « bon » verdict que chaque épreuve abîme d'une seule faute. ② CONTEXTE D'APPEL — C04 à C07.
    ③ ENTRÉE — — ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — UNE valeur : un dictionnaire neuf à chaque appel. [rend: 1]
    ⑥ TRAITEMENT — composer. ⑦ UNITÉ — chiffres de forme (⑨ ① du programme).
    ⑧ POURQUOI — La forme d'un NON TRANCHÉE (DONNÉES DE CHOIX), l'exemple de R-505 ⑫ pour C5 sur 2024-2026.
    ⑨ CE QUI CLOCHE — Aucun chiffre n'est une mesure. ⑩ EFFET — Aucun. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    epoque = {"debut": "2000-01-03", "fin": "2007-12-31", "n_operations": 20, "gain_moyen_eur": 100.0,
              "p_perdante": 0.4, "gagnante": True}
    return {
        "regle": "R-505 v1 du 04-11-2026", "date_verdict": REGARD, "fiche_id": "C5E10-QA-V1", "cas": "1",
        "declaration": {"date_declaration": "2026-11-10T09:00:00+01:00", "empreinte": "0123456789abcdef"},
        "verdict": "NON TRANCHÉE", "motif": "DONNÉES DE CHOIX", "premier_controle_bloquant": "annees_d_examen",
        "k": {"valeur": 69, "date_de_comptage": "2026-11-10T09:00:00+01:00", "lignes_du_registre": 69,
              "fiches_du_registre": 68, "versions_comptees": 68, "temoins": 1,
              "compte": "chaque_version_qui_change_un_calcul"},
        "seuil_de_preuve": 0.0007,
        "controles": {
            "declaration": _c("PASSE"), "annees_d_examen": _c("BLOQUE", raison="2024-2026 a servi à régler"),
            "regard_unique": _c("PASSE"),
            "observations_independantes": _c("PASSE", detail={"n_operations": 89, "observations_independantes": 87,
                                                                "taille_des_groupes": 1, "methode": "permutations"}),
            "gain_bat_zero": _c("INCONNU", raison="forme"), "bat_le_hasard": _c("INCONNU", raison="forme"),
            "epoques": _c("PASSE", detail={"epoques": [epoque], "epoques_gagnantes": 1,
                                           "minimum_d_epoques_gagnantes": 1}),
            "surapprentissage": _c("SANS_OBJET", raison="cas 1"), "sharpe_degonfle": _c("SANS_OBJET", raison="cas 1"),
            "kelly": _c("PASSE", detail={"kelly": 0.1, "gain_moyen_net_eur": 500.0}),
            "voisins": _c("INCONNU", raison="forme"), "frais_doubles": _c("INCONNU", raison="forme"),
            "taux_face_au_point_mort": _c("INCONNU", role="AFFICHAGE", raison="forme"),
            "borne_basse_du_gain": _c("INCONNU", role="AFFICHAGE", raison="forme"),
            "gain_un_jeton": _c("INCONNU", role="AFFICHAGE", raison="forme"),
            "creux_un_jeton": _c("INCONNU", role="AFFICHAGE", raison="forme"),
        },
        "affichages": {n: {"valeur": None, "confiance": None, "raison": "forme"} for n in
                       ("temoin", "avantage_du_moment", "probabilite_de_gain", "gain_moyen_par_operation",
                        "operations_necessaires", "nombre_d_essais")},
        "empreinte_code_juge": "fedcba9876543210", "preenregistrement": "a45b3aef853ba396",
    }


# Les deux entrées écrites par le vrai écrivain de L4 le 05-11-2026 à 13h14 (⑨ ②), octet pour octet.
ENTREES_REELLES_DE_L4 = {
    "517b8ec03ce412ee.json": '{"alea":"0e842da9","echec":"","horodatage_paris":"2026-11-05T13:14:12+01:00",'
                             '"nature":"RESULTAT","preenregistrement":"a45b3aef853ba396","resultat":{"n":0}}',
    "a45b3aef853ba396.json": '{"alea":"ec09a977","date_regle_univers":"NON_DECLARE","empreinte_hypothese":'
                             '"546a08e987286167","famille":"NON_DECLARE","fiche_id":"C5E10-QA-V1","horodatage_paris":'
                             '"2026-11-05T13:14:12+01:00","hypothese":{"bareme":"REEL","horizon":20,"periode":"TOUT",'
                             '"signal":["f","x"],"sl_pct":2.5,"tp_pct":4.0,"univers":["EN"]},"mere":"","nature":'
                             '"PREENREGISTREMENT","octets":{},"part_regardee":"NON_DECLARE","periode_conception":'
                             '"NON_DECLARE","regle_univers":"NON_DECLARE"}',
}

# Une déclaration complète, clés littérales (⑧).
def declaration_etalon(fiche_id="C5E10-QA-V1", date="2026-11-10T09:00:00+01:00", univers="règle datée de forme"):
    """Rend une ligne de déclaration datée complète, aux clés littérales.

    ① RÔLE — La « bonne » déclaration que C10, C11 et C16 abîment. ② CONTEXTE D'APPEL — C10, C11, C16.
    ③ ENTRÉE — la fiche, la date, la règle d'univers. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire {champ : texte}. [rend: 1] ⑥ TRAITEMENT — composer. ⑦ UNITÉ — textes.
    ⑧ POURQUOI — voir ⑧ du programme. ⑨ CE QUI CLOCHE — valeurs de forme. ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    return {"fiche_id": fiche_id, "date_declaration": date, "declaree_par": "Chat",
            "confirmee_par": "Jean-Luc, forme", "cas": "1", "periode_conception": "2024-01-02..2026-07-10",
            "part_regardee": "2000-2023, rejeu du 28-10-2026", "regle_univers": univers,
            "date_regle_univers": "2026-11-10", "lignee": "aucune", "hypothese": "forme", "parametres_libres": "4",
            "moment_du_regard": "forme", "biais_du_survivant": "forme", "annees_d_examen": "2000-01-03..2023-12-29",
            "regard_sans_decision": "", "empreinte_code_juge": "forme", "empreinte_code_signal": "forme",
            "reglages": "{}", "bareme": "forme", "reference_hasard": "forme", "temoins": "aucun",
            "epoques": "forme", "regle_de_departage": "alphabétique", "source": "épreuve du lot C"}


def charger(racine):
    """Charge le module des contrats d'une copie, sous un nom neuf.

    ① RÔLE — Éprouver le module de la COPIE (sabotée ou non), jamais celui de la racine. ② CONTEXTE D'APPEL — chaque
    épreuve. ③ ENTRÉE — la racine de la copie. ④ CONDITIONS D'ENTRÉE — le module y est. ⑤ SORTIE — UNE valeur : le
    module. [rend: 1] ⑥ TRAITEMENT — importlib. ⑦ UNITÉ — — ⑧ POURQUOI — un module neuf par épreuve : une épreuve qui
    modifie une liste en mémoire ne contamine pas la suivante. ⑨ CE QUI CLOCHE — — ⑩ EFFET — exécute le module (il ne
    fait que déclarer). ⑪ TERMINAISON — Rend la main ; lève si le module ne se charge pas. [sort: non]
    """
    charger.n = getattr(charger, "n", 0) + 1
    sp = importlib.util.spec_from_file_location(f"contrats_eprouves_{charger.n}", os.path.join(racine, CONTRATS))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def batir_la_copie(racine, dossier, texte_du_module=None, texte_de_l_etalon=None):
    """Bâtit la copie réduite : les deux programmes et chaque fichier sous contrat, à son chemin réel.

    ① RÔLE — Donner aux épreuves une vraie racine, petite. ② CONTEXTE D'APPEL — `main`, une fois par jeu.
    ③ ENTRÉE — la racine réelle, le dossier à remplir, le texte du module à poser (sabotage) ou None, le texte de
    l'étalon des versions à poser (sabotage) ou None.
    ④ CONDITIONS D'ENTRÉE — ④ du programme. ⑤ SORTIE — UNE valeur : None si tout est copié, sinon la phrase qui dit
    pourquoi la copie ne peut pas se bâtir. [rend: 1] ⑥ TRAITEMENT — ① copier les deux programmes · ② trouver chaque
    nom de CONTRATS_PAR_FICHIER dans l'arbre réel (hors .git) · ③ refuser un nom absent ou présent deux fois ·
    ④ copier le fichier entier s'il est petit, sinon ses premières lignes · ⑤ poser le texte sabotant de l'étalon, au
    chemin que le contrat de la racine lui donne. ⑦ UNITÉ — fichiers.
    ⑧ POURQUOI — Le nom est cherché partout hors .git, sans recopier la liste des dossiers que `confronter_tous` saute
    (R-708) : mesuré le 05-11-2026, chacun des 29 noms n'existe qu'une fois ; un doublon arrête l'épreuve (deux
    fichiers de même nom sont un défaut, jamais une intention). ⑨ CE QUI CLOCHE — ⑨ ③ du programme.
    ⑩ EFFET — écrit dans `dossier`. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    os.makedirs(os.path.join(dossier, "programmes"), exist_ok=True)
    shutil.copy(os.path.join(racine, CONFRONTER), os.path.join(dossier, CONFRONTER))
    if texte_du_module is None:
        shutil.copy(os.path.join(racine, CONTRATS), os.path.join(dossier, CONTRATS))
    else:
        open(os.path.join(dossier, CONTRATS), "w", encoding="utf-8").write(texte_du_module)
    noms = set(charger(racine).CONTRATS_PAR_FICHIER)
    trouves = {}
    for r, sd, fs in os.walk(racine):
        sd[:] = [x for x in sd if x != ".git"]
        for f in fs:
            if f in noms:
                trouves.setdefault(f, []).append(os.path.relpath(os.path.join(r, f), racine))
    for nom in sorted(noms):
        if len(trouves.get(nom, [])) != 1:
            return f"{nom} : trouvé {len(trouves.get(nom, []))} fois sous la racine (attendu : 1)"
        rel = trouves[nom][0]
        os.makedirs(os.path.dirname(os.path.join(dossier, rel)), exist_ok=True)
        if os.path.getsize(os.path.join(racine, rel)) <= TAILLE_GARDEE_ENTIERE:
            shutil.copy(os.path.join(racine, rel), os.path.join(dossier, rel))
        else:
            with open(os.path.join(racine, rel), encoding="utf-8-sig", errors="replace") as f:
                lignes = [l for _, l in zip(range(LIGNES_GARDEES), f)]
            open(os.path.join(dossier, rel), "w", encoding="utf-8").writelines(lignes)
    if texte_de_l_etalon is not None:
        open(os.path.join(dossier, charger(racine).ETALON_DES_VERSIONS), "w", encoding="utf-8").write(texte_de_l_etalon)
    return None


def poser(copie, chemin, objet):
    """Écrit un objet JSON (ou un texte) à un chemin de la copie.

    ① RÔLE — poser une entrée fabriquée. ② CONTEXTE D'APPEL — les épreuves. ③ ENTRÉE — copie, chemin relatif, objet
    ou texte. ④ CONDITIONS D'ENTRÉE — — ⑤ SORTIE — Ne rend rien. [rend: rien] ⑥ TRAITEMENT — créer le dossier,
    écrire. ⑦ UNITÉ — — ⑧ POURQUOI — — ⑨ CE QUI CLOCHE — — ⑩ EFFET — écrit un fichier.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    p = os.path.join(copie, chemin)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(objet if isinstance(objet, str) else json.dumps(objet, ensure_ascii=False))


def ecrire_declarations(copie, lignes, entete=None):
    """Réécrit le fichier des déclarations datées de la copie avec des lignes données.

    ① RÔLE — poser des déclarations fabriquées. ② CONTEXTE D'APPEL — C10, C11, C16. ③ ENTRÉE — copie, lignes, en-tête
    (par défaut celui du fichier de la copie : la forme réelle). ④ CONDITIONS D'ENTRÉE — le fichier existe dans la copie.
    ⑤ SORTIE — Ne rend rien. [rend: rien] ⑥ TRAITEMENT — lire l'en-tête réel, écrire. ⑦ UNITÉ — —
    ⑧ POURQUOI — l'en-tête vient du FICHIER, pas du contrat (⑧ du programme). ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — écrit un fichier. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    p = os.path.join(copie, "donnees", "DECLARATIONS_DATEES.csv")
    if entete is None:
        entete = next(csv.reader(open(p, encoding="utf-8-sig")))
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=entete, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for l in lignes:
            w.writerow(l)


# ── LES ÉPREUVES : chacune rend (vrai si elle passe, phrase) ─────────────────────────────────────────────────────────
def c01_vraie_racine_verte(copie, racine):
    """C01 — Le vrai programme du circuit, sur les vrais en-têtes, est vert et muet. (11 éléments : voir le programme ;
    rend: 1 ; sort: non)"""
    r = subprocess.run([sys.executable, "-B", os.path.join(copie, CONFRONTER), copie], capture_output=True, text=True,
                       timeout=120)
    return r.returncode == 0 and not r.stdout.strip(), f"code {r.returncode}, sortie « {r.stdout.strip()[:300]} »"


def c02_chaque_champ_p0_retire_rougit(copie, racine):
    """C02 — Sabotage n°1 du superviseur : retirer CHAQUE champ P0 du contrat fait rougir (un à un). (rend: 1 ; sort: non)"""
    muets = []
    for champ in charger(copie).CHAMPS_P0:
        m = charger(copie)
        m.DECLARATION_DATEE.remove(champ)
        if not any("HORS CONTRAT" in e and champ in e for e in m.confronter_tous(copie)):
            muets.append(champ)
    n = len(charger(copie).CHAMPS_P0)
    return n > 0 and not muets, f"{n} champs P0 retirés un à un ; muets : {muets or 'aucun'}"


def c03_colonne_sans_contrat_rougit(copie, racine):
    """C03 — Sabotage n°3 du superviseur : une colonne ajoutée au registre sans contrat rougit. (rend: 1 ; sort: non)"""
    m = charger(copie)
    p = os.path.join(copie, m.REGISTRE_DES_STRATEGIES)
    lignes = open(p, encoding="utf-8-sig").read().split("\n")
    lignes[0] += ",station"
    open(p, "w", encoding="utf-8").write("\n".join(lignes))
    e = m.confronter_tous(copie)
    return any("HORS CONTRAT" in x and "station" in x for x in e), f"écarts : {e}"


def c04_verdict_etalon_conforme(copie, racine):
    """C04 — Un verdict complet posé dans verdicts/ ne rend aucun écart (la forme est tenable). (rend: 1 ; sort: non)"""
    poser(copie, "verdicts/etalon.json", verdict_etalon())
    e = charger(copie).confronter_tous(copie)
    return e == [], f"écarts : {e}"


def c05_k_retire_du_contrat_rougit(copie, racine):
    """C05 — Sabotage n°2 du superviseur : retirer k du contrat du verdict rougit. (rend: 1 ; sort: non)"""
    poser(copie, "verdicts/etalon.json", verdict_etalon())
    m = charger(copie)
    m.VERDICT.remove("k")
    e = m.confronter_tous(copie)
    return any("HORS CONTRAT VERDICT" in x and "k" in x.split("—")[-1] for x in e), f"écarts : {e}"


def c06_verdict_sans_k_rougit(copie, racine):
    """C06 — L'écrivain qui oublie k est vu de son côté (ABSENT). (rend: 1 ; sort: non)"""
    v = verdict_etalon()
    del v["k"]
    poser(copie, "verdicts/sans_k.json", v)
    e = charger(copie).confronter_tous(copie)
    return any("ABSENT" in x and x.endswith("— k") for x in e), f"écarts : {e}"


def c07_interieur_du_verdict(copie, racine):
    """C07 — Neuf fautes à l'intérieur d'un verdict, une à une : chacune rougit. (rend: 1 ; sort: non)"""
    def oublie(v): del v["controles"]["kelly"]
    def accent(v): v["controles"]["declaration"]["etat"] = "PASSÉ"
    def role(v): v["controles"]["gain_un_jeton"]["role"] = "DECIDE"
    def compte(v): v["k"]["compte"] = "chaque_variante"
    def epoque(v): del v["controles"]["epoques"]["detail"]["epoques"][0]["p_perdante"]
    def detail(v): del v["controles"]["observations_independantes"]["detail"]["taille_des_groupes"]
    def affichage(v): del v["affichages"]["temoin"]
    def motif(v): v["motif"] = "AUTRE"
    def mot(v): v["verdict"] = "VALIDÉE STRICTE"
    muettes = []
    for faute in (oublie, accent, role, compte, epoque, detail, affichage, motif, mot):
        c = tempfile.mkdtemp(dir=os.path.dirname(copie))
        shutil.copytree(copie, c, dirs_exist_ok=True)
        v = verdict_etalon()
        faute(v)
        poser(c, "verdicts/faute.json", v)
        if not charger(c).confronter_tous(c):
            muettes.append(faute.__name__)
        shutil.rmtree(c)
    return not muettes, f"9 fautes ; muettes : {muettes or 'aucune'}"


def c08_entrees_reelles_de_L4(copie, racine):
    """C08 — Les deux entrées écrites par le vrai écrivain de L4 sont conformes ; une nature inconnue et un champ
    oublié rougissent. (rend: 1 ; sort: non)"""
    for nom, texte in ENTREES_REELLES_DE_L4.items():
        poser(copie, f"registre_essais/{nom}", texte)
    e0 = charger(copie).confronter_tous(copie)
    pre = json.loads(ENTREES_REELLES_DE_L4["a45b3aef853ba396.json"])
    autre = dict(pre, nature="AUTRE")
    sans = {k: v for k, v in pre.items() if k != "octets"}
    poser(copie, "registre_essais/autre.json", autre)
    poser(copie, "registre_essais/sans_octets.json", sans)
    e1 = charger(copie).confronter_tous(copie)
    vu_autre = any("autre.json" in x and "nature" in x for x in e1)
    vu_sans = any("sans_octets.json" in x and "ABSENT" in x and "octets" in x for x in e1)
    return e0 == [] and vu_autre and vu_sans, f"réelles : {e0} ; fautes : {e1}"


def c09_tableau_de_bord(copie, racine):
    """C09 — Le tableau de bord : absent, muet (la limite déclarée) ; complet, conforme ; sans « positions », rouge.
    (rend: 1 ; sort: non)"""
    e_absent = charger(copie).confronter_tous(copie)
    t = {b: {"valeur": None, "etat": "ABSENTE"} for b in ("bandeau", "circuit", "positions", "signaux", "cours",
                                                          "calendrier", "strategies", "alertes")}
    t["fabrique_le"] = "2026-11-05T20:30+01:00"
    poser(copie, "rapports/tableau_de_bord.json", t)
    e_ok = charger(copie).confronter_tous(copie)
    del t["positions"]
    poser(copie, "rapports/tableau_de_bord.json", t)
    e_ko = charger(copie).confronter_tous(copie)
    return (e_absent == [] and e_ok == [] and any("positions" in x and "ABSENT" in x for x in e_ko),
            f"absent : {e_absent} ; complet : {e_ok} ; sans positions : {e_ko}")


def c10_lecture_de_la_declaration(copie, racine):
    """C10 — La déclaration retenue est la dernière écrite AVANT le regard ; une date sans décalage, une date illisible
    et un en-tête hors contrat lèvent. (rend: 1 ; sort: non)"""
    m = charger(copie)
    avant = declaration_etalon(date="2026-11-10T09:00:00+01:00")
    apres = dict(declaration_etalon(date="2026-11-25T09:00:00+01:00"), hypothese="écrite après le regard")
    autre = declaration_etalon(fiche_id="C5E10-OBS-V1")
    ecrire_declarations(copie, [avant, apres, autre])
    d = m.declaration_de_la_fiche(copie, "C5E10-QA-V1", REGARD)
    bon = d is not None and d["date_declaration"] == avant["date_declaration"]
    aucune = m.declaration_de_la_fiche(copie, "INCONNUE", REGARD) is None
    leves = []
    for essai in ("naive", "illisible", "entete"):
        try:
            if essai == "naive":
                m.declaration_de_la_fiche(copie, "C5E10-QA-V1", "2026-11-20T20:00:00")
            elif essai == "illisible":
                ecrire_declarations(copie, [dict(avant, date_declaration="10-11-2026")])
                m.declaration_de_la_fiche(copie, "C5E10-QA-V1", REGARD)
            else:
                entete = next(csv.reader(open(os.path.join(copie, "donnees", "DECLARATIONS_DATEES.csv"),
                                              encoding="utf-8")))
                ecrire_declarations(copie, [avant], entete=entete[:-1])
                m.declaration_de_la_fiche(copie, "C5E10-QA-V1", REGARD)
        except ValueError:
            leves.append(essai)
    return bon and aucune and len(leves) == 3, f"avant le regard : {bon} ; inconnue : {aucune} ; levées : {leves}"


def c11_champs_manquants(copie, racine):
    """C11 — Complète : rien ; chaque champ exigé vidé : nommé ; le facultatif vide : rien ; cas « 3 » : nommé ;
    aucune déclaration : tous les exigés. (rend: 1 ; sort: non)"""
    m = charger(copie)
    complete = declaration_etalon()
    ok = m.champs_de_la_declaration_manquants(complete) == []
    rates = []
    for champ in complete:
        if champ == "regard_sans_decision":
            continue
        if m.champs_de_la_declaration_manquants(dict(complete, **{champ: "  "})) != [champ]:
            rates.append(champ)
    facultatif = m.champs_de_la_declaration_manquants(dict(complete, regard_sans_decision="")) == []
    cas = m.champs_de_la_declaration_manquants(dict(complete, cas="3")) == ["cas"]
    rien = m.champs_de_la_declaration_manquants(None)
    tous = len(rien) == len(complete) - 1 and "regard_sans_decision" not in rien
    return ok and not rates and facultatif and cas and tous, (
        f"complète : {ok} ; non nommés : {rates or 'aucun'} ; facultatif : {facultatif} ; cas 3 : {cas} ; "
        f"aucune déclaration : {len(rien)} champs")


MOTIF_D_UN_SEUIL = re.compile(r"seuil|seance|observation|plancher|horizon|avant|minimum|kelly|date|k$")


def c12_aucun_defaut_sur_un_seuil(copie, racine):
    """C12 — Propriété commune du superviseur : aucun argument d'une fonction du module qui porte un seuil, une date, un
    nombre de séances ou d'observations n'a de valeur par défaut. (rend: 1 ; sort: non)"""
    m = charger(copie)
    fautes = []
    for nom, f in inspect.getmembers(m, inspect.isfunction):
        if f.__module__ != m.__name__:
            continue
        for p in inspect.signature(f).parameters.values():
            if p.default is not inspect.Parameter.empty and MOTIF_D_UN_SEUIL.search(p.name):
                fautes.append(f"{nom}({p.name}={p.default!r})")
    return not fautes, f"défauts sur un seuil : {fautes or 'aucun'}"


# La seule donnée chiffrée admise au niveau du module : le seuil d'exigence C8 de l'ANCIENNE grille, déclaré comme tel
# le 29-10-2026 (ÉTUDE 18, S11). R-505 ⑤ l'a remplacé : il est consigné à retirer (RAPPORT du lot C, ⑨).
DONNEE_CHIFFREE_ADMISE = "SEUILS_D_EXIGENCE_SUR_LES_FRAIS"


def c13_aucun_chiffre_dans_les_contrats(copie, racine):
    """C13 — Aucun nombre dans une donnée déclarée au niveau du module (un seuil se lit à la table de la loi, R-743 ②),
    hors la donnée admise. (rend: 1 ; sort: non)"""
    arbre = ast.parse(open(os.path.join(copie, CONTRATS), encoding="utf-8").read())
    fautes = []
    for n in arbre.body:
        if not isinstance(n, (ast.Assign, ast.AnnAssign)):
            continue
        cibles = [t.id for t in (n.targets if isinstance(n, ast.Assign) else [n.target]) if isinstance(t, ast.Name)]
        if DONNEE_CHIFFREE_ADMISE in cibles or not isinstance(n.value, (ast.Constant, ast.List, ast.Tuple, ast.Dict,
                                                                           ast.Set, ast.BinOp)):
            continue
        for x in ast.walk(n.value):
            if isinstance(x, ast.Constant) and type(x.value) in (int, float):
                fautes.append(f"{cibles} ligne {n.lineno} : {x.value}")
    return not fautes, f"nombres dans une donnée déclarée : {fautes or 'aucun'}"


def c14_mots_du_verdict_au_registre(copie, racine):
    """C14 — Chaque mot du verdict et chaque motif est écrit tel quel au REGISTRE (R-505 ⑫). (rend: 1 ; sort: non)"""
    m = charger(copie)
    texte = open(os.path.join(racine, REGISTRE_DES_REGLES), encoding="utf-8").read()
    absents = [x for x in m.MOTS_DU_VERDICT + m.MOTIFS_DE_NON_TRANCHEE if x not in texte]
    return not absents, f"absents du REGISTRE : {absents or 'aucun'}"


def c15_fichiers_a_venir_bien_formes(copie, racine):
    """C15 — Chaque fichier à venir nomme un contrat déclaré (liste, ou natures de listes), un écrivain sans « .py » et
    un lot. (rend: 1 ; sort: non)"""
    m = charger(copie)
    fautes = []
    for chemin, (contrat, ecrivain, lot) in m.FICHIERS_A_VENIR.items():
        c = getattr(m, contrat, None)
        listes = list(c.values()) if isinstance(c, dict) else [c]
        if not listes or not all(isinstance(l, list) and l and all(isinstance(x, str) for x in l) for l in listes):
            fautes.append(f"{chemin} : contrat {contrat} non déclaré comme liste de champs")
        if not ecrivain or ecrivain.endswith(".py") or not lot:
            fautes.append(f"{chemin} : écrivain « {ecrivain} » ou lot « {lot} »")
    return not fautes, f"fautes : {fautes or 'aucune'}"


def c16_vraie_ligne_du_registre(copie, racine):
    """C16 — Une VRAIE ligne : la fiche C5E10-QA-V1 lue au vrai registre ; sa déclaration, bâtie sur sa vraie colonne
    `univers`, est lue et complète. (rend: 1 ; sort: non)"""
    m = charger(copie)
    fiche = m.lire_les_fiches(racine).get("C5E10-QA-V1")
    if fiche is None:
        return False, "C5E10-QA-V1 absente du vrai registre"
    d = declaration_etalon(univers=f"les valeurs de la fiche au registre : {fiche['univers']} (forme, pas une règle)")
    ecrire_declarations(copie, [d])
    lue = m.declaration_de_la_fiche(copie, fiche["id"], REGARD)
    return (lue is not None and m.champs_de_la_declaration_manquants(lue) == [] and fiche["univers"] in lue["regle_univers"],
            f"univers réel « {fiche['univers']} » ; lue : {lue is not None}")


# LE LOT DIV : ses deux fichiers sont lus TELS QUE DIV LES ÉCRIT, jamais recopiés ici (superviseur R-759 du 05-11-2026,
# 15h55-15h57, D2 : une liste littérale, remise à jour à chaque tour de DIV, est une rustine qui casse au tour suivant ;
# R-708 : deux écritures d'une même chose divergent toujours). Retirés au tour 3 : EN_TETE_TABLE_DES_DIVIDENDES et
# EN_TETE_DISTRIBUTIONS_DECIDEES, les deux en-têtes littéraux du tour 2. Le commit lu est celui du tour 3 de DIV.
COMMIT_DU_LOT_DIV = "8317391c"
DEPOT_DIV = None                # posé par `main` depuis « --div=<racine> »
TABLE_DIV = os.path.join("donnees", "TABLE_DES_DIVIDENDES.csv")
DECIDEES_DIV = os.path.join("donnees", "sources_dividendes", "DISTRIBUTIONS_DECIDEES.csv")


def _en_tete_reel_du_lot_DIV(racine, chemin):
    """Rend la première ligne réelle d'un fichier du lot DIV, ou None avec la raison.

    ① RÔLE — Donner à C17 l'en-tête tel que DIV l'écrit, sans en garder de copie. ② CONTEXTE D'APPEL — C17, deux fois.
    ③ ENTRÉE — la racine réelle ; `chemin`, relatif (TABLE_DIV ou DECIDEES_DIV). ④ CONDITIONS D'ENTRÉE — le fichier est
    sous la racine (après l'assemblage de D), ou DEPOT_DIV nomme un dépôt git qui porte COMMIT_DU_LOT_DIV.
    ⑤ SORTIE — DEUX valeurs : l'en-tête (texte sans fin de ligne) ou None ; la source lue, ou la raison de l'échec.
    Exemple réel au 05-11-2026 : la table au commit 8317391c rend dix colonnes, de « valeur » à « couverte_jusqu_au ».
    [rend: 2] ⑥ TRAITEMENT — ① sous la racine si le fichier y est · ② sinon « git show COMMIT:chemin » dans DEPOT_DIV ·
    ③ première ligne, marque d'ordre des octets retirée. ⑦ UNITÉ — un texte. ⑧ POURQUOI — D2 du superviseur de 15h55 :
    C17 confronte le contrat à l'en-tête RÉEL. ⑨ CE QUI CLOCHE — le commit est nommé ici : quand DIV avance, il faut
    changer ce nom (⑨ ⑥ du programme). ⑩ EFFET — lit un fichier ou un objet git ; n'écrit rien. ⑪ TERMINAISON — Rend la
    main ; « git show » a une limite de 60 s. [sort: non]
    """
    sur_place = os.path.join(racine, chemin)
    if os.path.isfile(sur_place):
        return open(sur_place, encoding="utf-8-sig").readline().rstrip("\r\n"), sur_place
    if not DEPOT_DIV:
        return None, f"{chemin} absent sous la racine, et aucun « --div=<dépôt DIV> » donné"
    r = subprocess.run(["git", "-C", DEPOT_DIV, "show", f"{COMMIT_DU_LOT_DIV}:{chemin}"], capture_output=True,
                       timeout=60)
    if r.returncode != 0:
        return None, f"git show {COMMIT_DU_LOT_DIV}:{chemin} dans {DEPOT_DIV} : code {r.returncode}"
    texte = r.stdout.decode("utf-8-sig")
    return texte.splitlines()[0] if texte else None, f"{DEPOT_DIV} au commit {COMMIT_DU_LOT_DIV}"


def c17_contrats_du_lot_DIV(copie, racine):
    """C17 — Les deux fichiers du lot DIV, lus TELS QUE DIV LES ÉCRIT (au commit COMMIT_DU_LOT_DIV, ou sous la racine
    après l'assemblage) : muets absents ; leurs en-têtes RÉELS verts par le vrai programme du circuit (le contrat est
    à jour) ; rouges sans `statut` ou avec une colonne de plus. Sans source lisible, rouge (R-734). (rend: 1 ; sort: non)"""
    table, source_t = _en_tete_reel_du_lot_DIV(racine, TABLE_DIV)
    decidees, source_d = _en_tete_reel_du_lot_DIV(racine, DECIDEES_DIV)
    if table is None or decidees is None:
        return False, f"en-têtes réels du lot DIV illisibles : {source_t if table is None else source_d}"

    def confronter():
        r = subprocess.run([sys.executable, "-B", os.path.join(copie, CONFRONTER), copie], capture_output=True,
                           text=True, timeout=120)
        return r.returncode, r.stdout
    absents = confronter()
    poser(copie, TABLE_DIV, table + "\n")
    poser(copie, DECIDEES_DIV, decidees + "\n")
    conformes = confronter()
    poser(copie, TABLE_DIV, ",".join(c for c in table.split(",") if c != "statut") + "\n")
    sans_statut = confronter()
    poser(copie, TABLE_DIV, table + "\n")
    poser(copie, DECIDEES_DIV, decidees + ",remarque\n")
    colonne_de_plus = confronter()
    ok = ("statut" in table.split(",") and absents[0] == 0 and conformes[0] == 0 and "statut" in sans_statut[1]
          and sans_statut[0] != 0 and "remarque" in colonne_de_plus[1] and colonne_de_plus[0] != 0)
    return ok, (f"lu : {source_t} ; {len(table.split(','))} colonnes réelles · absents : code {absents[0]} · "
                f"conformes : code {conformes[0]} « {conformes[1].strip()[-160:] if conformes[0] else ''} » · "
                f"sans statut : code {sans_statut[0]} « {sans_statut[1].strip()[-120:]} » · colonne de plus : code "
                f"{colonne_de_plus[0]}")


def _etalon(copie):
    """Lit l'étalon des versions de la copie par la fonction du contrat (sa seule lecture).

    ① RÔLE — Donner à C18 et C19 les cas et les fautes. ② CONTEXTE D'APPEL — C18, C19. ③ ENTRÉE — la copie.
    ④ CONDITIONS D'ENTRÉE — l'étalon et le registre y sont. ⑤ SORTIE — DEUX valeurs : le module des contrats de la
    copie, et ce que rend `cas_de_l_etalon_des_versions` (cas, fautes). [rend: 2] ⑥ TRAITEMENT — charger, appeler.
    ⑦ UNITÉ — des cas. ⑧ POURQUOI — une seule lecture de l'étalon (R-708). ⑨ CE QUI CLOCHE — — ⑩ EFFET — lit deux
    fichiers. ⑪ TERMINAISON — Rend la main ; lève si l'étalon manque (l'épreuve rougit alors). [sort: non]
    """
    m = charger(copie)
    return m, m.cas_de_l_etalon_des_versions(copie)


def c18_etalon_des_versions(copie, racine):
    """C18 — L'étalon des versions (temoins/ETALON_DES_VERSIONS.csv), lu par `cas_de_l_etalon_des_versions`, porte les
    CAS de la décision du 05-11-2026 à 13h40 et du superviseur, jamais un total : aucune faute de forme ; le cas de
    Jean-Luc (deux VRAIES lignes d'une même fiche, qui ne diffèrent que par `entree` : 1 version) ; chaque réglage
    nommé par Jean-Luc et chaque élément de la lecture de jeu ont un cas à 2 versions. RETIRÉ par le lot S_kk
    (05-11-2026, n°184 M1) : le sous-contrôle « signal avec / sans module existant », qui décidait par l'EXISTENCE d'un
    fichier — rustine : renommer un module changeait son avis (T7), un module déclaré inexistant passait muet (T8) ; il
    est repris au sens de la lecture de jeu (`forme_du_module` du juge) par l'épreuve du compte des essais.
    Réduite au tour 3 (superviseur R-759 du 05-11-2026, 15h55-15h57) : le contrôle
    « fonction déclarée à venir » et l'ancrage au `VIDE` du juge (`_vide_du_juge`) sont RETIRÉS ; la lecture du vide
    appartient à S_kk. Elle n'éprouve que la FORME de l'étalon. (rend: 1 ; sort: non)"""
    m, (cas, fautes) = _etalon(copie)
    deux = [c for c in cas if c["versions_attendues"] == 2]
    jean_luc = [c for c in cas if not c["colonne_changee"] and c["versions_attendues"] == 1
                and {k for k in c["ligne_a"] if c["ligne_a"][k] != c["ligne_b"].get(k)} == {"entree"}]
    mots_sans_cas = [x for x in m.REGLAGES_NOMMES_PAR_JEAN_LUC if x not in {c["mot_de_jean_luc"] for c in deux}]
    elements_sans_cas = [x for x in m.ELEMENTS_DE_LA_LECTURE_DE_JEU
                         if x not in {c["ce_que_le_juge_tire_autrement"] for c in deux}]
    fabriques_mal_faites = [c["cas"] for c in cas if c["colonne_changee"] and
                            {k for k in c["ligne_a"] if c["ligne_a"][k] != c["ligne_b"].get(k)} != {c["colonne_changee"]}]
    # Le second cas que le superviseur exige nommément : changer les indicateurs d'une fiche SANS module de signal
    # compte deux versions. Pris par sa propriété, jamais par son nom. Sans ce compte, E06 ne mordait sur la pointe
    # de N72 que parce que le lot DIV manquait (c17) ; réunis, il était muet (bloc 3, 08-11-2026).
    sans_module = [c for c in deux if c["colonne_changee"] == "indicateurs"
                   and not (c["ligne_a"].get("module_signal") or "").strip()]
    ok = (cas and not fautes and len(jean_luc) == 1 and not mots_sans_cas and not elements_sans_cas
          and not fabriques_mal_faites and len(sans_module) >= 1)
    return ok, (f"{len(cas)} cas, fautes : {fautes or 'aucune'} ; cas de Jean-Luc : {[c['cas'] for c in jean_luc]} ; "
                f"indicateurs changés sans module, à 2 versions : {[c['cas'] for c in sans_module] or 'aucun'} ; "
                f"mots sans cas à 2 : {mots_sans_cas or 'aucun'} ; éléments sans cas à 2 : {elements_sans_cas or 'aucun'} ; "
                f"copies mal faites : {fabriques_mal_faites or 'aucune'}")


FICHIERS_DU_JUGE = (os.path.join("programmes", "JUGE_DES_STRATEGIES.py"), os.path.join("programmes", "MODULE_JUGEMENT.py"))


def c19_colonnes_lues_par_le_juge_couvertes(copie, racine):
    """C19 — Propriété : chaque colonne du registre que le juge lit par son nom (`x["col"]`, `x.get("col")`) est
    changée par au moins un cas de l'étalon des versions — sauf `id`, qui fait la fiche (deux lignes d'une même fiche
    le partagent par définition). Le jour où le juge lit une colonne de plus, cette épreuve rougit jusqu'à ce qu'un
    cas dise combien de versions fait son changement. (rend: 1 ; sort: non)"""
    m, (cas, fautes) = _etalon(copie)
    lues = set()
    for f in FICHIERS_DU_JUGE:
        for n in ast.walk(ast.parse(open(os.path.join(racine, f), encoding="utf-8").read())):
            k = None
            if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant):
                k = n.slice.value
            elif (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "get" and n.args
                  and isinstance(n.args[0], ast.Constant)):
                k = n.args[0].value
            if k in m.STRATEGIE:
                lues.add(k)
    changees = {k for c in cas for k in c["ligne_a"] if c["ligne_a"][k] != c["ligne_b"].get(k)}
    non_couvertes = sorted(lues - changees - {"id"})
    return bool(lues) and not non_couvertes, (f"lues : {sorted(lues)} ; non couvertes par l'étalon : "
                                              f"{non_couvertes or 'aucune'}")


# Les cas MAL FORMÉS que C20 ajoute à l'étalon de sa copie : {nom du cas : ligne CSV}. Chacun doit être écarté par
# `cas_de_l_etalon_des_versions`, avec une faute qui le nomme. Écrits ici en clair (⑧ du programme).
CAS_MAL_FORMES = {
    "faux_deux_sans_element": "faux_deux_sans_element,C5-EI-PARAMS,70,,tp,+7.0%,2,,,épreuve",
    "faux_un_avec_element": "faux_un_avec_element,C5-EI-PARAMS,70,,tp,+8.0%,1,seuils,,épreuve",
    "faux_mot_inconnu": "faux_mot_inconnu,C5-EI-PARAMS,70,,tp,+9.0%,2,seuils,levier,épreuve",
    "faux_mot_sur_un": "faux_mot_sur_un,C5-EI-PARAMS,70,,note,x,1,,objectif,épreuve",
    "faux_element_inconnu": "faux_element_inconnu,C5-EI-PARAMS,70,,tp,+4.0%,2,frais,,épreuve",
    "faux_colonne_id": "faux_colonne_id,C5-EI-PARAMS,70,,id,AUTRE,2,signal,,épreuve",
    "faux_valeur_inchangee": "faux_valeur_inchangee,C5-EI-PARAMS,70,,tp,+5.0%,1,,,épreuve",
    "faux_autre_fiche": "faux_autre_fiche,C5-EI-PARAMS,6,,tp,+3.0%,2,seuils,,épreuve",
    "faux_paire_qui_change": "faux_paire_qui_change,C5-EI-PARAMS,65,70,tp,+3.0%,1,,,épreuve",
    "faux_sans_source": "faux_sans_source,C5-EI-PARAMS,70,,tp,+2.0%,2,seuils,,",
    "faux_versions_trois": "faux_versions_trois,C5-EI-PARAMS,70,,tp,+1.0%,3,seuils,,épreuve",
}


def c20_etalon_sous_contrat_et_fautes_vues(copie, racine):
    """C20 — L'étalon des versions MORD sur sa forme : ① chaque cas de CAS_MAL_FORMES, ajouté à l'étalon de la copie,
    est écarté avec une faute qui le nomme, et les vrais cas restent ; ② un nom en double est écarté ; ③ une colonne
    de plus dans l'étalon fait rougir le vrai programme du circuit (l'étalon est sous contrat). (rend: 1 ; sort: non)"""
    m = charger(copie)
    chemin = os.path.join(copie, m.ETALON_DES_VERSIONS)
    vrai = open(chemin, encoding="utf-8").read()
    vrais = len(m.cas_de_l_etalon_des_versions(copie)[0])
    lignes = list(CAS_MAL_FORMES.values()) + [vrai.splitlines()[1]]          # + le premier vrai cas, en double
    open(chemin, "w", encoding="utf-8").write(vrai + "\n".join(lignes) + "\n")
    cas, fautes = m.cas_de_l_etalon_des_versions(copie)
    non_vus = [n for n in CAS_MAL_FORMES if not any(f.startswith(n + " ") for f in fautes)]
    double_vu = any("en double" in f for f in fautes)
    open(chemin, "w", encoding="utf-8").write(vrai.replace("\n", ",remarque\n", 1))
    r = subprocess.run([sys.executable, "-B", os.path.join(copie, CONFRONTER), copie], capture_output=True, text=True,
                       timeout=120)
    sous_contrat = r.returncode != 0 and "remarque" in r.stdout
    ok = not non_vus and double_vu and len(cas) == vrais and sous_contrat
    return ok, (f"mal formés non vus : {non_vus or 'aucun'} ; double vu : {double_vu} ; vrais cas gardés : {len(cas)}/"
                f"{vrais} ; colonne de plus : code {r.returncode} « {r.stdout.strip()[-140:]} »")


EPREUVES = [c01_vraie_racine_verte, c02_chaque_champ_p0_retire_rougit, c03_colonne_sans_contrat_rougit,
            c04_verdict_etalon_conforme, c05_k_retire_du_contrat_rougit, c06_verdict_sans_k_rougit,
            c07_interieur_du_verdict, c08_entrees_reelles_de_L4, c09_tableau_de_bord, c10_lecture_de_la_declaration,
            c11_champs_manquants, c12_aucun_defaut_sur_un_seuil, c13_aucun_chiffre_dans_les_contrats,
            c14_mots_du_verdict_au_registre, c15_fichiers_a_venir_bien_formes, c16_vraie_ligne_du_registre,
            c17_contrats_du_lot_DIV, c18_etalon_des_versions,
            c19_colonnes_lues_par_le_juge_couvertes, c20_etalon_sous_contrat_et_fautes_vues]

# LES SABOTAGES DU CODE ÉPROUVÉ : (nom, texte du module à remplacer, remplacement). Chacun doit faire rougir au moins une
# épreuve ; un texte introuvable (ou trouvé deux fois) est un sabotage NON APPLIQUÉ, et fait échouer le jeu.
SABOTAGES = [
    ("S01 la confrontation des fichiers à venir n'est plus appelée",
     "    ecarts += confronter_les_fichiers_a_venir(base)\n    return ecarts", "    return ecarts"),
    ("S02 la date du regard n'est plus lue", "        if date < limite:\n", "        if True:\n"),
    ("S03 le champ facultatif devient exigé",
     "    exiges = [c for c in DECLARATION_DATEE if c not in CHAMPS_FACULTATIFS_DE_LA_DECLARATION]",
     "    exiges = list(DECLARATION_DATEE)"),
    ("S04 l'état d'un contrôle n'est plus confronté", '        if c.get("etat") not in ETATS_D_UN_CONTROLE:',
     "        if False:"),
    ("S05 la déclaration datée n'est plus sous contrat", "    NOM_DES_DECLARATIONS_DATEES: DECLARATION_DATEE,\n", ""),
    ("S06 la nature d'une entrée n'est plus confrontée", "        if nature not in contrat:", "        if False:"),
    ("S07 l'intérieur du verdict n'est plus confronté",
     'CONFRONTATIONS_INTERIEURES = {"VERDICT": _ecarts_d_un_verdict}', "CONFRONTATIONS_INTERIEURES = {}"),
    ("S08 la date du regard reçoit une valeur par défaut",
     "def declaration_de_la_fiche(racine, fiche_id, avant):", "def declaration_de_la_fiche(racine, fiche_id, avant=None):"),
    ("S09 un seuil écrit dans le contrat", 'CAS_DE_LA_LOI = ("1", "2")', 'CAS_DE_LA_LOI = ("1", "2")\nPLANCHER = 30'),
    ("S10 un mot du verdict n'est plus celui du REGISTRE", '"RÉFUTÉE", "NON TRANCHÉE",', '"REFUTEE", "NON TRANCHÉE",'),
    ("S11 un écrivain nommé avec « .py »", '("VERDICT", "JUGE_DES_STRATEGIES", "JG")',
     '("VERDICT", "JUGE_DES_STRATEGIES.py", "JG")'),
    ("S12 le détail des contrôles n'est plus confronté",
     '        if c.get("etat") in ("PASSE", "BLOQUE") and cle in DETAILS_DES_CONTROLES:', "        if False:"),
    ("S13 le cas n'est plus confronté dans la déclaration",
     '    if "cas" not in manquants and (declaration.get("cas") or "").strip() not in CAS_DE_LA_LOI:', "    if False:"),
    # second geste du lot C (05-11-2026, après 13h40) : la décision Q-G5, les contrats du lot DIV, l'en-tête en colonnes
    # tour 2 du lot C (05-11-2026, après le superviseur de 15h05) : la propriété, la fonction à venir, l'étalon
    # S14, S20 et S21 RETIRÉS au tour 3 : leurs cibles (ENTREE_VIDE_LUE_POUR_COMPTER_LES_VERSIONS, FONCTIONS_A_VENIR,
    # DEFINITION_DU_VIDE) ont quitté le contrat pour le lot S_kk (superviseur R-759 du 05-11-2026, 15h55-15h57).
    ("S15 l'objectif n'est plus un réglage nommé par Jean-Luc",
     'REGLAGES_NOMMES_PAR_JEAN_LUC = ("signal", "valeurs", "objectif", "stop",',
     'REGLAGES_NOMMES_PAR_JEAN_LUC = ("signal", "valeurs", "stop",'),
    ("S16 la période n'est plus un élément de la lecture de jeu", '"signal", "bornes_de_la_periode",', '"signal",'),
    ("S17 la table des dividendes n'est plus à venir",
     '    "donnees/TABLE_DES_DIVIDENDES.csv": ("TABLE_DES_DIVIDENDES", "FABRIQUER_LA_TABLE_DES_DIVIDENDES", "DIV"),\n', ""),
    ("S18 un fichier à venir en colonnes n'est plus lu par son en-tête",
     '            if not entree.endswith(".json"):', '            if False:'),
    ("S19 le compte de k revient à « chaque ligne »", 'COMPTES_DE_K = ("chaque_version_qui_change_un_calcul",)',
     'COMPTES_DE_K = ("chaque_ligne", "chaque_fiche")'),
    ("S22 la copie fabriquée n'est plus changée", "            b[colonne] = e[\"valeur_b\"]\n", ""),
    ("S23 les numéros de ligne du fichier sont décalés d'une ligne",
     "        return lignes[n - 2] if 2 <= n <= len(lignes) + 1 else None",
     "        return lignes[n - 1] if 1 <= n <= len(lignes) else None"),
    ("S24 l'étalon des versions n'est plus sous contrat", "    NOM_DE_L_ETALON_DES_VERSIONS: CAS_D_ETALON,\n", ""),
    ("S25 un cas à 2 versions n'a plus à dire ce que le juge tire autrement",
     " or bool(tire) != (attendu == deux_versions)", ""),
    ("S28 la colonne qui fait la fiche peut être changée", ' or colonne == "id"', ""),
    ("S29 une copie qui ne change rien est acceptée", ' or (a.get(colonne) or "") == e["valeur_b"]', ""),
    ("S30 un mot de Jean-Luc est admis sur un cas à 1 version", " or (mot and attendu != deux_versions)", ""),
    ("S31 un nom de cas en double est admis", "        if not nom or nom in noms:", "        if not nom:"),
    # tour 3 : C17 sabotée contre sa propre correction — le contrat revient aux neuf colonnes du tour 2 de DIV
    ("S32 la table des dividendes perd `couverte_jusqu_au` au contrat", '"rendement", "statut", "couverte_jusqu_au"]',
     '"rendement", "statut"]'),
    # les deux sabotages du module joués par le relecteur du lot C (D/lot_C_relecture/saboter.py, R6 et R7), gardés ici
    ("S26 (relecteur R6) le dossier des verdicts mal nommé", '    "verdicts/": ("VERDICT",', '    "verdict/": ("VERDICT",'),
    ("S27 (relecteur R7) l'empreinte du code du signal devient facultative",
     'CHAMPS_FACULTATIFS_DE_LA_DECLARATION = ("regard_sans_decision",)',
     'CHAMPS_FACULTATIFS_DE_LA_DECLARATION = ("regard_sans_decision", "empreinte_code_signal")'),
]

# LES SABOTAGES DE L'ÉTALON DES VERSIONS (temoins/ETALON_DES_VERSIONS.csv), même forme. Les cinq premiers sont ceux du
# relecteur du lot C (R1 à R5 : « l'univers, l'horizon, le module du signal, le stop, la période ne comptent plus »),
# traduits du premier tour, où ils déplaçaient une colonne de REGLAGES_DE_CALCUL, au second, où l'étalon dit ce qui
# compte : chacun retire ou retourne le cas qui l'exige. Les deux derniers retirent les deux cas que le superviseur
# exige nommément (CCI(14) → CCI(20) sur une fiche sans module ; les lignes 65 et 70 du fichier).
SABOTAGES_DE_L_ETALON = [
    ("E01 (relecteur R1) l'univers changé ne compte plus",
     '"TTE,ENGI,VIE,EN,FGR,AIR,SAF,HO",2,valeurs,valeurs,', '"TTE,ENGI,VIE,EN,FGR,AIR,SAF,HO",1,valeurs,valeurs,'),
    ("E02 (relecteur R2) l'horizon changé n'est plus un cas", "horizon_change,C5-EI-PARAMS,70,,horizon,20,2,horizon,horizon,",
     "horizon_change,C5-EI-PARAMS,70,,nom,autre,1,,,"),
    ("E03 (relecteur R3) le module du signal n'est plus changé par aucun cas",
     "module_change,C5-EI-PARAMS,70,,module_signal,programmes/MODULE_SIGNAL_RSI2_CONNORS.py,2,signal,signal,",
     "module_change,C5-EI-PARAMS,70,,fonction_signal,signaux_encore_autres,2,signal,signal,"),
    ("E04 (relecteur R4) le stop changé ne compte plus, sans le dire", "stop_change,C5-EI-PARAMS,70,,sl,-3.0%,2,seuils,stop,",
     "stop_change,C5-EI-PARAMS,70,,sl,-3.0%,1,,,"),
    ("E05 (relecteur R5) la période changée ne compte plus, sans le dire (Q-C1 tranchée en silence)",
     "2020-01-02 -> 2026-03-11,2,bornes_de_la_periode,,", "2020-01-02 -> 2026-03-11,1,,,"),
    ("E06 le cas CCI(14) → CCI(20) sur une fiche sans module ne compte plus, sans le dire",
     "CCI(20) < -50 · Un,2,signal,signal,", "CCI(20) < -50 · Un,1,,,"),
    ("E07 le cas de Jean-Luc (lignes 65 et 70 du fichier) disparaît",
     "jean_luc_lignes_65_70,C5-EI-PARAMS,65,70,,,1,", "jean_luc_lignes_65_70,C5-EI-PARAMS,65,65,,,1,"),
]


def jouer(racine, texte_du_module, base_tmp, dire, texte_de_l_etalon=None):
    """Bâtit une copie et joue les épreuves ; rend {nom : (passe, phrase)}, ou une phrase si la copie échoue.

    ① RÔLE — un jeu complet. ② CONTEXTE D'APPEL — `main`, une fois sans sabotage, puis une fois par sabotage.
    ③ ENTRÉE — racine réelle, texte du module (None = le vrai), dossier temporaire, vrai pour afficher, texte de
    l'étalon des versions (None = le vrai).
    ④ CONDITIONS D'ENTRÉE — ④ du programme. ⑤ SORTIE — UNE valeur : un dictionnaire, ou un texte d'échec. [rend: 1]
    ⑥ TRAITEMENT — ① bâtir la copie · ② pour chaque épreuve, une copie de la copie, l'épreuve, une exception comptant
    comme un rouge. ⑦ UNITÉ — épreuves. ⑧ POURQUOI — une épreuve qui lève a rougi : sous sabotage, le code peut lever.
    ⑨ CE QUI CLOCHE — — ⑩ EFFET — écrit sous `base_tmp`. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    mere = tempfile.mkdtemp(dir=base_tmp)
    pourquoi = batir_la_copie(racine, mere, texte_du_module, texte_de_l_etalon)
    if pourquoi:
        return pourquoi
    resultats = {}
    for e in EPREUVES:
        c = tempfile.mkdtemp(dir=base_tmp)
        shutil.copytree(mere, c, dirs_exist_ok=True)
        try:
            resultats[e.__name__] = e(c, racine)
        except Exception as x:          # une épreuve qui lève a rougi (⑧)
            resultats[e.__name__] = (False, f"LÈVE {type(x).__name__}: {x}")
        shutil.rmtree(c, ignore_errors=True)
        if dire:
            ok, phrase = resultats[e.__name__]
            print(f"  {'✅' if ok else '❌'} {e.__name__} — {phrase[:400]}")
    shutil.rmtree(mere, ignore_errors=True)
    return resultats


def main():
    """Lance le jeu, puis les sabotages si demandé. (11 éléments : voir le programme ; rend: 1 ; sort: oui)"""
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1 or not os.path.isfile(os.path.join(args[0], CONTRATS)):
        print(__doc__.split("USAGE")[-1].strip())
        return 2
    racine = os.path.abspath(args[0])
    global DEPOT_DIV
    DEPOT_DIV = next((os.path.abspath(a.split("=", 1)[1]) for a in sys.argv[1:] if a.startswith("--div=")), None)
    base_tmp = tempfile.mkdtemp(prefix="epreuves_contrats_loi_")
    try:
        print("ÉPREUVES DES CONTRATS DE LA LOI — racine :", racine)
        r = jouer(racine, None, base_tmp, True)
        if isinstance(r, str):
            print("  ❌ la copie ne se bâtit pas :", r)
            return 2
        verts = all(ok for ok, _ in r.values())
        print(f"\n  {sum(ok for ok, _ in r.values())}/{len(r)} épreuves passent")
        if "--saboter" not in sys.argv[1:]:
            return 0 if verts else 1
        print("\nSABOTAGES DU CODE ÉPROUVÉ — chacun doit faire rougir au moins une épreuve")
        texte = open(os.path.join(racine, CONTRATS), encoding="utf-8").read()
        mordent = True
        for nom, avant, apres in SABOTAGES:
            if texte.count(avant) != 1:
                print(f"  ❌ {nom} — NON APPLIQUÉ (texte trouvé {texte.count(avant)} fois)")
                mordent = False
                continue
            rs = jouer(racine, texte.replace(avant, apres), base_tmp, False)
            rouges = [n for n, (ok, _) in rs.items() if not ok] if isinstance(rs, dict) else [f"copie : {rs}"]
            print(f"  {'✅ MORD' if rouges else '❌ MUET'} {nom} — rouges : {', '.join(rouges) or 'aucun'}")
            mordent = mordent and bool(rouges)
        print("\nSABOTAGES DE L'ÉTALON DES VERSIONS — chacun doit faire rougir au moins une épreuve")
        chemin_etalon = os.path.join(racine, charger(racine).ETALON_DES_VERSIONS)
        etalon = open(chemin_etalon, encoding="utf-8").read()
        for nom, avant, apres in SABOTAGES_DE_L_ETALON:
            if etalon.count(avant) != 1:
                print(f"  ❌ {nom} — NON APPLIQUÉ (texte trouvé {etalon.count(avant)} fois)")
                mordent = False
                continue
            rs = jouer(racine, None, base_tmp, False, etalon.replace(avant, apres))
            rouges = [n for n, (ok, _) in rs.items() if not ok] if isinstance(rs, dict) else [f"copie : {rs}"]
            print(f"  {'✅ MORD' if rouges else '❌ MUET'} {nom} — rouges : {', '.join(rouges) or 'aucun'}")
            mordent = mordent and bool(rouges)
        print(f"\n  VERDICT : {'tout est conforme' if verts and mordent else 'ÉCHEC'}")
        return 0 if verts and mordent else 1
    finally:
        shutil.rmtree(base_tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
