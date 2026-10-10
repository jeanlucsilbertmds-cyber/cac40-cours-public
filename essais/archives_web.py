#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ARCHIVES DU WEB — lire les anciennes copies d'une page, gardées par l'Internet Archive (web.archive.org).

① RÔLE — Deux fonctions réutilisables par tout programme : `lister_copies` (quelles copies d'une page
  existent, à quelles dates) et `lire_copie` (le texte d'une copie, tel que la page était ce jour-là).
② CONTEXTE D'APPEL — Importé par un programme qui tourne sur une machine GitHub. Les outils du Chat sont
  bloqués sur web.archive.org (mesuré le 01 et le 10-10-2026) ; une machine GitHub passe (essai du
  10-10-2026, 14h12 et 14h14, ÉTUDE 19 §10).
③ ENTRÉE — Une adresse de page SANS « https:// » ni « www. » (ex. « boursorama.com/cours/consensus/1rPTTE/ »),
  et pour `lire_copie` un horodatage de 14 chiffres rendu par `lister_copies`.
④ CONDITIONS D'ENTRÉE — Accès réseau à web.archive.org. Sinon : `ErreurArchives`, jamais un résultat vide
  silencieux.
⑤ SORTIE — `lister_copies` : UNE valeur, la liste des (horodatage, empreinte) des copies lisibles (code
  200), une seule par contenu distinct, de la plus ancienne à la plus récente. `lire_copie` : UNE valeur,
  le texte de la page. [rend: 1]
⑥ TRAITEMENT — Demande à l'index des archives (« CDX ») ; télécharge la copie brute (suffixe « id_ », sans
  le bandeau ajouté par les archives) ; décompresse le gzip ; réessaie après une pause sur les refus
  temporaires (429, 503) et les coupures.
⑦ UNITÉ — horodatage AAAAMMJJhhmmss en heure UTC, tel que l'archive le donne.
⑧ POURQUOI — Les archives sont le seul historique COMPLET du consensus Boursorama trouvé (349 + 299 copies,
  2019-2026). Demande de Jean-Luc du 10-10-2026 à 13h29 : « une belle mécanique qui fonctionne bien sur
  GitHub, il faut absolument l'exploiter […] qu'on puisse appeler de n'importe où ».
⑨ CE QUI CLOCHE — Interface publique non contractuelle de l'Internet Archive : elle peut changer. Une
  copie peut être la page d'erreur ou de consentement d'un site : c'est à l'appelant de vérifier qu'elle
  contient ce qu'il attend. Pas de limite de débit garantie : l'appelant espace ses demandes.
⑩ EFFET — Aucun fichier écrit. Demandes réseau seulement.
⑪ TERMINAISON — Chaque demande a un délai de 60 s ; au plus `ESSAIS` tentatives ; rend toujours la main.
  [sort: oui]
"""
import gzip
import json
import time
import urllib.error
import urllib.request

ESSAIS = 4
AGENT = "Mozilla/5.0 (compatible; archives-cac40/1.0; simulation)"


class ErreurArchives(Exception):
    """Les archives n'ont pas répondu, ou ont répondu autre chose que ce qui était attendu."""


def _demander(url, essais=ESSAIS, pause=20.0, ouvrir=urllib.request.urlopen):
    """Rend les octets de la réponse ; réessaie sur 429, 503 et coupure ; lève ErreurArchives sinon."""
    dernier = ""
    for i in range(essais):
        try:
            with ouvrir(urllib.request.Request(url, headers={"User-Agent": AGENT}), timeout=60) as r:
                b = r.read()
                if b[:2] == b"\x1f\x8b":
                    b = gzip.decompress(b)
                return b
        except urllib.error.HTTPError as e:
            dernier = f"code {e.code}"
            if e.code not in (429, 503):
                break
        except Exception as e:  # coupure réseau, délai dépassé
            dernier = str(e)
        if i < essais - 1:
            time.sleep(pause * (i + 1))
    raise ErreurArchives(f"{url} : {dernier}")


def lister_copies(adresse, ouvrir=urllib.request.urlopen, pause=20.0):
    """Rend [(horodatage, empreinte), …] des copies lisibles d'une page, une par contenu distinct."""
    url = ("https://web.archive.org/cdx/search/cdx?url=" + adresse +
           "&output=json&fl=timestamp,statuscode,digest&filter=statuscode:200&collapse=digest")
    t = _demander(url, ouvrir=ouvrir, pause=pause).decode("utf-8", "replace").strip()
    if not t:
        return []
    try:
        lignes = json.loads(t)
    except ValueError:
        raise ErreurArchives(f"index illisible pour {adresse} : {t[:80]!r}")
    if not lignes or lignes[0] != ["timestamp", "statuscode", "digest"]:
        raise ErreurArchives(f"en-tête d'index inattendu pour {adresse} : {lignes[:1]}")
    return [(ts, emp) for ts, code, emp in lignes[1:] if code == "200"]


def lire_copie(adresse, horodatage, ouvrir=urllib.request.urlopen, pause=20.0):
    """Rend le texte de la copie de `adresse` prise à `horodatage` (14 chiffres)."""
    if not (len(horodatage) == 14 and horodatage.isdigit()):
        raise ErreurArchives(f"horodatage invalide : {horodatage!r}")
    url = f"https://web.archive.org/web/{horodatage}id_/https://www.{adresse}"
    return _demander(url, ouvrir=ouvrir, pause=pause).decode("utf-8", "replace")
