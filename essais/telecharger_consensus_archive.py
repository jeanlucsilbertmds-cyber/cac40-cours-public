#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TÉLÉCHARGER L'HISTORIQUE DU CONSENSUS BOURSORAMA DEPUIS LES ARCHIVES DU WEB — opération ponctuelle.

① RÔLE — Lire chaque copie archivée de la liste « consensus CAC 40 » de Boursorama (pages 1 à 3) et en
  tirer une ligne par valeur : recommandation, cours, objectif, potentiel, nombre d'analystes.
② CONTEXTE D'APPEL — Lancé une fois sur une machine GitHub par `.github/workflows/essai_archives_web.yml`
  du dépôt public (accord de Jean-Luc du 10-10-2026 à 14h24). Reprend là où il s'est arrêté s'il est relancé.
③ ENTRÉE — Un argument : le dossier racine du clone du dépôt privé, où écrire.
④ CONDITIONS D'ENTRÉE — Accès à web.archive.org. Sinon : code 1 et rapport qui le dit.
⑤ SORTIE — UNE valeur : code 0 si toutes les copies listées ont été traitées (lues ou refusées avec motif),
  1 si l'index n'a pas répondu ou si le temps a manqué. [rend: 1]
⑥ TRAITEMENT — Pour chaque page : index des copies → pour chaque copie non encore traitée : lecture,
  contrôle (le tableau « Reco. / Obj. Cours » doit être là, sinon la copie est REFUSÉE avec son motif),
  extraction des lignes, écriture immédiate.
⑦ UNITÉ — cours et objectif en euros, potentiel en %, horodatage de copie en UTC.
⑧ POURQUOI — Seul historique complet du consensus trouvé (ÉTUDE 19 §10). Un test sur le passé demande des
  années de données ; Jean-Luc, 10-10-2026 : « si on les fait dans l'avenir, il va falloir attendre 600 ans ».
⑨ CE QUI CLOCHE — La lecture du tableau suit la forme de la page Boursorama ; une forme inconnue est
  refusée, pas devinée. La date « Mis à jour le » est celle de Boursorama, pas celle de la copie.
⑩ EFFET — ÉCRIT au dépôt privé : `donnees/consensus_archives_boursorama.csv` (les lignes),
  `donnees/consensus_archives_index.csv` (chaque copie et son sort), `rapports/TELECHARGEMENT_CONSENSUS_ARCHIVES_<horodatage>.md`.
⑪ TERMINAISON — S'arrête de lui-même après `DUREE_MAX` secondes, en ayant tout écrit au fur et à mesure.
  [sort: oui]
"""
import csv
import datetime
import html
import os
import re
import sys
import time
import zoneinfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import archives_web  # noqa: E402

PAGES = {
    "1": "boursorama.com/bourse/actions/consensus/recommandations-paris/",
    "2": "boursorama.com/bourse/actions/consensus/recommandations-paris/page-2",
    "3": "boursorama.com/bourse/actions/consensus/recommandations-paris/page-3",
}
ENTETES = ["Libellé", "Reco.", "Der. Cours*", "Obj. Cours**", "Potentiel", "Nb. Analystes."]
CHAMPS = ["horodatage_copie", "page", "mis_a_jour", "valeur", "code_bourso", "recommandation",
          "cours", "objectif", "potentiel_pct", "nb_analystes", "delta_analystes"]
CHAMPS_INDEX = ["page", "horodatage_copie", "empreinte", "sort", "lignes", "motif"]
PAUSE = 4.0
DUREE_MAX = 5 * 3600


def _texte(x):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(x))).strip()


def _nombre(x):
    """Lit « 1 234,56 », « 1,234.56 », « +20.964% » ; « atteint » reste « atteint » ; lève ValueError sinon."""
    x = _texte(x).replace("EUR", "").replace("%", "").replace("\xa0", "").replace(" ", "").replace("+", "")
    if x.lower().startswith("atteint"):
        return "atteint"
    if x in ("", "-", "--"):
        return ""
    if "," in x and "." in x:  # le dernier des deux séparateurs est la décimale
        x = x.replace(",", "") if x.rfind(".") > x.rfind(",") else x.replace(".", "").replace(",", ".")
    else:
        x = x.replace(",", ".")
    float(x)
    return x


def lire_liste(page):
    """Rend (date « Mis à jour le », [lignes]) ; lève ValueError si le tableau attendu n'est pas là."""
    i = page.find("Recommandations des analystes professionnels")
    if i < 0:
        raise ValueError("bloc « Recommandations des analystes professionnels » absent")
    t0 = page.find("<table", i)
    t1 = page.find("</table>", t0)
    if t0 < 0 or t1 < 0:
        raise ValueError("tableau absent")
    tab = page[t0:t1]
    heads = [_texte(h) for h in re.findall(r"<th[^>]*>(.*?)</th>", tab, re.S)]
    if heads[:6] != ENTETES:
        raise ValueError(f"en-têtes inattendus : {heads[:6]}")
    m = re.search(r"Mis à jour le\s*([0-9]{2}[./][0-9]{2}[./][0-9]{2,4})", _texte(page))
    maj = m.group(1) if m else ""
    lignes = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", tab, re.S):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        if len(tds) < 6:
            continue
        code = re.search(r'/cours/consensus/([0-9A-Za-z]+)/', tds[0])
        reco = re.search(r'u-only-clipboard">([^<]*)<', tds[1])
        reco = reco.group(1).strip() if reco else _texte(tds[1])
        nb = re.match(r"(\d+)\s*\(([+-]?\d+)\)", _texte(tds[5]))
        lignes.append(dict(valeur=_texte(tds[0]), code_bourso=code.group(1) if code else "",
                           recommandation=reco, cours=_nombre(tds[2]), objectif=_nombre(tds[3]),
                           potentiel_pct=_nombre(tds[4]),
                           nb_analystes=nb.group(1) if nb else "", delta_analystes=nb.group(2) if nb else ""))
    if not lignes:
        raise ValueError("tableau sans ligne")
    for l in lignes:  # contrôle croisé : le potentiel affiché doit se retrouver à partir du cours et de l'objectif
        if l["potentiel_pct"] not in ("", "atteint") and l["cours"] and l["objectif"]:
            recalc = (float(l["objectif"]) / float(l["cours"]) - 1) * 100
            if abs(recalc - float(l["potentiel_pct"])) > 0.2:
                raise ValueError(f"{l['valeur']} : potentiel affiché {l['potentiel_pct']} ≠ recalculé {recalc:.3f}")
    return maj, lignes


def _deja(chemin):
    """Copies déjà traitées pour de bon (lues ou refusées pour leur contenu) ; un échec réseau sera réessayé."""
    if not os.path.exists(chemin):
        return set()
    return {(r["page"], r["horodatage_copie"]) for r in csv.DictReader(open(chemin, encoding="utf-8"))
            if r["sort"] != "échec réseau"}


def _purger(f_lignes, f_index):
    """Retire du fichier des lignes celles d'une copie que l'index ne dit pas « lue » (arrêt entre deux écritures)."""
    if not os.path.exists(f_lignes):
        return 0
    lues = set()
    if os.path.exists(f_index):
        lues = {(r["page"], r["horodatage_copie"]) for r in csv.DictReader(open(f_index, encoding="utf-8"))
                if r["sort"] == "lue"}
    lignes = list(csv.DictReader(open(f_lignes, encoding="utf-8")))
    garde = [l for l in lignes if (l["page"], l["horodatage_copie"]) in lues]
    if len(garde) != len(lignes):
        tmp = f_lignes + ".tmp"
        with open(tmp, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, CHAMPS)
            w.writeheader()
            w.writerows(garde)
        os.replace(tmp, f_lignes)
    return len(lignes) - len(garde)


def _ajouter(chemin, champs, lignes):
    neuf = not os.path.exists(chemin)
    with open(chemin, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, champs)
        if neuf:
            w.writeheader()
        w.writerows(lignes)


def main():
    racine = sys.argv[1]
    debut = time.time()
    maintenant = datetime.datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d_%Hh%M")
    os.makedirs(os.path.join(racine, "donnees"), exist_ok=True)
    os.makedirs(os.path.join(racine, "rapports"), exist_ok=True)
    f_lignes = os.path.join(racine, "donnees", "consensus_archives_boursorama.csv")
    f_index = os.path.join(racine, "donnees", "consensus_archives_index.csv")
    purgees = _purger(f_lignes, f_index)
    deja = _deja(f_index)
    bilan, complet, echecs_suite = [f"- lignes orphelines retirées au démarrage : {purgees}"], True, 0
    for num, adresse in PAGES.items():
        try:
            copies = archives_web.lister_copies(adresse)
        except archives_web.ErreurArchives as e:
            bilan.append(f"- page {num} : INDEX EN ÉCHEC — {e}")
            complet = False
            continue
        lues = refusees = reseau = sautees = 0
        for ts, emp in copies:
            if echecs_suite >= 5:
                complet = False
                break
            if (num, ts) in deja:
                sautees += 1
                continue
            if time.time() - debut > DUREE_MAX:
                complet = False
                break
            time.sleep(PAUSE)
            try:
                maj, lignes = lire_liste(archives_web.lire_copie(adresse, ts))
                _ajouter(f_lignes, CHAMPS, [dict(horodatage_copie=ts, page=num, mis_a_jour=maj, **x) for x in lignes])
                _ajouter(f_index, CHAMPS_INDEX, [dict(page=num, horodatage_copie=ts, empreinte=emp, sort="lue",
                                                      lignes=len(lignes), motif="")])
                lues += 1
                echecs_suite = 0
            except archives_web.ErreurArchives as e:
                _ajouter(f_index, CHAMPS_INDEX, [dict(page=num, horodatage_copie=ts, empreinte=emp, sort="échec réseau",
                                                      lignes=0, motif=str(e)[:200])])
                reseau += 1
                echecs_suite += 1
                complet = False
            except ValueError as e:
                _ajouter(f_index, CHAMPS_INDEX, [dict(page=num, horodatage_copie=ts, empreinte=emp, sort="refusée",
                                                      lignes=0, motif=str(e)[:200])])
                refusees += 1
        bilan.append(f"- page {num} : {len(copies)} copies à l'index · {lues} lues · {refusees} refusées · "
                     f"{reseau} échecs réseau (à reprendre) · {sautees} déjà traitées"
                     + (" · ARRÊT : 5 échecs réseau de suite" if echecs_suite >= 5 else ""))
    duree = int(time.time() - debut)
    texte = [f"# TÉLÉCHARGEMENT DU CONSENSUS ARCHIVÉ — {maintenant} (Paris)", "",
             "Opération ponctuelle sur machine GitHub (ÉTUDE 19 §10, A-534). Simulation uniquement.", ""] + bilan + [
             "", f"Durée : {duree} s · {'TERMINÉ' if complet else 'INCOMPLET — relancer : reprise automatique'}"]
    open(os.path.join(racine, "rapports", f"TELECHARGEMENT_CONSENSUS_ARCHIVES_{maintenant}.md"), "w",
         encoding="utf-8").write("\n".join(texte) + "\n")
    return 0 if complet else 1


if __name__ == "__main__":
    sys.exit(main())
