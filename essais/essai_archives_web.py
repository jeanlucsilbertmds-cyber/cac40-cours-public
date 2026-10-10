#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ESSAI PONCTUEL — les archives du web (web.archive.org) sont-elles lisibles depuis une machine GitHub ?

Rôle : répondre par une mesure à la question de Jean-Luc du 10-10-2026 à 13h29 (ÉTUDE 19 §10, fiche A-534).
Les outils du Chat sont bloqués sur web.archive.org ; une machine GitHub passe peut-être.
Ce n'est PAS un programme du circuit : il est lancé une fois, par un dépôt de son fichier d'essai.
Entrée : un argument, le dossier où écrire (le clone du dépôt privé). Sortie : code 0 si l'index des archives
a répondu, 1 sinon. Écrit : rapports/ESSAI_ARCHIVES_WEB_<horodatage>.md et temoins/archives_web/*.html.
"""
import gzip, json, os, sys, time, urllib.request, urllib.error, datetime, zoneinfo, re

UA = "Mozilla/5.0 (compatible; essai-archives-cac40/1.0)"
CIBLES = {
    "liste Boursorama page 1": "boursorama.com/bourse/actions/consensus/recommandations-paris/",
    "liste Boursorama page 2": "boursorama.com/bourse/actions/consensus/recommandations-paris/page-2",
    "fiche Boursorama TotalEnergies": "boursorama.com/cours/consensus/1rPTTE/",
    "fiche EasyBourse TotalEnergies": "easybourse.com/action-consensus/x/FR0000120271-25",
}


def lire(url, essais=4):
    """Rend (code HTTP, texte) ; décompresse le gzip ; réessaie sur 429/503 ; code 0 si la connexion échoue."""
    dernier = ""
    for i in range(essais):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                b = r.read()
                if b[:2] == b"\x1f\x8b":
                    b = gzip.decompress(b)
                return r.status, b.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and i < essais - 1:
                time.sleep(20 * (i + 1)); continue
            return e.code, ""
        except Exception as e:
            dernier = str(e)
            time.sleep(5 * (i + 1))
    return 0, dernier


def lignes_de_la_liste(page):
    """Nombre de lignes de valeurs du tableau « Reco. / Obj. Cours », et la date « Mis à jour le »."""
    n = len(re.findall(r'href="/cours/consensus/[0-9A-Za-z]+/"', page))
    m = re.search(r"Mis à jour le ([0-9./]+)", page)
    return n, (m.group(1) if m else "?"), ("Obj. Cours" in page)


def lister_copies(cible):
    """Index des copies (CDX) : liste de (horodatage, code, empreinte), sans doublon de contenu."""
    u = ("https://web.archive.org/cdx/search/cdx?url=" + cible +
         "&output=json&fl=timestamp,statuscode,digest&filter=statuscode:200&collapse=digest")
    code, t = lire(u)
    if code != 200:
        return code, None
    lignes = json.loads(t) if t.strip() else []
    return code, lignes[1:]


def main():
    sortie = sys.argv[1]
    maintenant = datetime.datetime.now(zoneinfo.ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d_%Hh%M")
    os.makedirs(os.path.join(sortie, "rapports"), exist_ok=True)
    dossier = os.path.join(sortie, "temoins", "archives_web")
    os.makedirs(dossier, exist_ok=True)
    rapport = [f"# ESSAI — ARCHIVES DU WEB DEPUIS UNE MACHINE GITHUB — {maintenant} (Paris)", "",
               "Essai ponctuel lancé par le Chat (ÉTUDE 19 §10, A-534). Simulation uniquement.", ""]
    index_ok = False
    for nom, cible in CIBLES.items():
        code, copies = lister_copies(cible)
        if copies is None:
            rapport.append(f"- **{nom}** : index des archives → code {code} (échec)")
            continue
        index_ok = True
        if not copies:
            rapport.append(f"- **{nom}** : index → 200, aucune copie")
            continue
        rapport.append(f"- **{nom}** : index → 200, **{len(copies)} copies au contenu distinct**, "
                       f"de {copies[0][0][:8]} à {copies[-1][0][:8]}")
        k = len(copies)
        choix = [copies[j] for j in sorted({0, k // 4, k // 2, 3 * k // 4, k - 1})]
        for ts, _, _ in choix:
            time.sleep(3)
            c, page = lire(f"https://web.archive.org/web/{ts}id_/https://www.{cible}")
            n, maj, obj = lignes_de_la_liste(page)
            f = os.path.join(dossier, f"{re.sub(r'[^A-Za-z0-9]+', '_', nom)}_{ts}.html")
            if c == 200 and page:
                open(f, "w", encoding="utf-8").write(page)
            rapport.append(f"  - copie {ts} → code {c}, {len(page)} caractères, {n} liens de consensus, "
                           f"colonne « Obj. Cours » : {'oui' if obj else 'non'}, « Mis à jour le » {maj}")
        time.sleep(15)
    rapport += ["", f"**Verdict** : index des archives {'LISIBLE' if index_ok else 'ILLISIBLE'} depuis une machine GitHub."]
    open(os.path.join(sortie, "rapports", f"ESSAI_ARCHIVES_WEB_{maintenant}.md"), "w", encoding="utf-8").write("\n".join(rapport) + "\n")
    print("index lisible" if index_ok else "index illisible")
    return 0 if index_ok else 1


if __name__ == "__main__":
    sys.exit(main())
