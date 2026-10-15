#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HORLOGE_D_EPREUVE — fait lire à un programme lancé une heure de Paris choisie.

① RÔLE — Rendre les épreuves indépendantes du jour où on les lance. Un programme lancé
  par `lancer_a_l_heure` lit, par datetime.now(), l'heure donnée, et non l'horloge.
② CONTEXTE D'APPEL — Importé par tests/EPREUVES_DU_MESSAGE_DU_SOIR_Mer_30-09-2026.py et
  tests/EPREUVES_DU_RATTRAPAGE_Jeu_01-10-2026.py. Ne s'exécute pas seul.
③ ENTRÉE — Voir `lancer_a_l_heure`.
④ CONDITIONS D'ENTRÉE — —
⑤ SORTIE — Voir `lancer_a_l_heure`.
⑥ TRAITEMENT — écrire un sitecustomize.py dans un dossier, le placer en tête du
  PYTHONPATH du programme lancé ; au démarrage, Python le charge et remplace
  datetime.datetime par une classe dont now() et today() rendent l'heure donnée.
⑦ UNITÉ — Une heure de Paris, AAAA-MM-JJTHH:MM:SS.
⑧ POURQUOI — Relecture indépendante du 30-09-2026 : lancées un lundi, un samedi ou un
  dimanche, les épreuves du message laissaient passer trois sabotages. L'horloge posée
  par les épreuves le fait à un seul endroit, ici, pour tous les jeux qui en ont besoin
  (R-708 : deux implémentations d'une même chose divergent toujours).
⑨ CE QUI CLOCHE — Seul datetime.datetime est remplacé : un programme qui lirait l'heure
  par time.time() ou date.today() lirait la vraie. Les programmes éprouvés le 01-10-2026
  (MESSAGE_DU_SOIR, FAUT_IL_RATTRAPER, CONTRATS_DES_FICHIERS.fabrique_du_jour) lisent
  datetime.now(ZoneInfo("Europe/Paris")).
⑩ EFFET — Écrit un fichier sitecustomize.py ; lance un processus.
⑪ TERMINAISON — Rend la main.
  [sort: non]
"""
import os
import subprocess

SITECUSTOMIZE = """import os
if os.environ.get("EPREUVE_HORLOGE"):
    import datetime as _dtm
    from zoneinfo import ZoneInfo
    _vrai = _dtm.datetime
    _fixe = _vrai.fromisoformat(os.environ["EPREUVE_HORLOGE"]).replace(tzinfo=ZoneInfo("Europe/Paris"))
    class _Fausse(_vrai):
        @classmethod
        def now(cls, tz=None):
            return _fixe.astimezone(tz) if tz else _fixe.replace(tzinfo=None)
        @classmethod
        def today(cls):
            return _fixe.replace(tzinfo=None)
    _dtm.datetime = _Fausse
"""


def lancer_a_l_heure(commande, horloge, dossier, delai=120):
    """Lance `commande` en lui faisant lire l'heure `horloge`, et rend le processus fini.

    ① RÔLE — Le seul geste de ce module.
    ② CONTEXTE D'APPEL — Les jeux d'épreuves, une fois par cas.
    ③ ENTRÉE — `commande` : la liste des mots de la commande · `horloge` : l'heure de
      Paris, AAAA-MM-JJTHH:MM:SS · `dossier` : un dossier jetable où poser le
      sitecustomize.py · `delai` : le délai maximal.
    ④ CONDITIONS D'ENTRÉE — `dossier` peut être créé.
    ⑤ SORTIE — UNE valeur : le résultat de subprocess.run (code, sorties en texte).
      [rend: 1]
    ⑥ TRAITEMENT — écrire le sitecustomize.py, composer l'environnement, lancer.
    ⑦ UNITÉ — Des SECONDES pour `delai`.
    ⑧ POURQUOI — Voir la fiche du fichier.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit `dossier`/sitecustomize.py ; lance un processus.
    ⑪ TERMINAISON — Rend la main ; au-delà de `delai`, lève TimeoutExpired.
      [sort: non]
    """
    os.makedirs(dossier, exist_ok=True)
    open(os.path.join(dossier, "sitecustomize.py"), "w", encoding="utf-8").write(SITECUSTOMIZE)
    env = dict(os.environ, EPREUVE_HORLOGE=horloge,
               PYTHONPATH=dossier + os.pathsep + os.environ.get("PYTHONPATH", ""))
    return subprocess.run(commande, capture_output=True, text=True, errors="replace", timeout=delai, env=env)
