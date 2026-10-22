# -*- coding: utf-8 -*-
"""N_EXECUTER_AU_PUBLIC_QUE_LE_CODE_PUBLIE.py — Mar 20-10-2026 (Paris). Simulation uniquement.
Renommé le 22-10-2026 sur décision de Jean-Luc (09h08, « Finalement 3 », parmi trois noms proposés ; à 09h06 il
avait formulé la fonction : « Ne pas exécuter de code privé au public ») ;
son ancien nom, GARDE_DU_CODE.py, ne disait pas sa fonction. Les brouillons d'étude gardent l'ancien nom.

Le garde qui empêche le circuit du soir, sur les machines du dépôt PUBLIC, d'exécuter un seul octet de code
venu du clone du dépôt PRIVÉ qui ne soit pas, à l'identique, dans la copie publique.

① RÔLE — Arrêter net (code de sortie 97) tout programme Python qui s'apprête à exécuter un fichier de code
  pris dans le dossier des données (le clone du privé) si ce fichier n'existe pas, octet pour octet, au même
  chemin relatif dans la copie publique du code. Propriété, et non liste : le garde ne connaît aucun nom de
  fichier ; il compare des octets.
② CONTEXTE D'APPEL — Jamais lancé à la main. Le pas « Poser » du circuit public (fabriqué par
  programmes/FABRIQUER_LE_CIRCUIT_PUBLIC.py) le recopie sous le nom `sitecustomize.py` dans un dossier hors
  du clone, et pose PYTHONPATH sur ce dossier : Python le charge alors au démarrage de CHAQUE programme du
  passage, enfants compris. Les épreuves : E7 de tests/EPREUVES_DU_CIRCUIT_PUBLIC_Jeu_15-10-2026.py (pièges A à D,
  garde mutant ; sabotages qui modifient ce programme : S29, S31, S33, S34, S35 ; qui visent sa pose : S26,
  S36).
③ ENTRÉE — Deux variables d'environnement : GARDE_DONNEES, le dossier du clone du privé (la racine où le
  circuit travaille) ; GARDE_CODE, le dossier de la copie publique du code (le dépôt public cloné à part).
  Lancé directement (`python3 N_EXECUTER_AU_PUBLIC_QUE_LE_CODE_PUBLIE.py`), il ne lit rien et dit seulement à quoi il sert.
④ CONDITIONS D'ENTRÉE — Les deux variables désignent deux dossiers existants et distincts. Si l'une manque,
  le garde ne pose RIEN : un programme lancé hors du circuit (épreuves, machine du Chat) tourne comme avant.
  C'est pourquoi le circuit éprouve, juste après l'avoir posé, que le garde mord (pas « Le garde du code
  mord-il ? ») : un garde absent sans que rien ne le dise serait une protection crue et inexistante.
⑤ SORTIE — Aucune valeur rendue au programme gardé. Sur un refus : une ligne sur la sortie d'erreur, puis
  la fin immédiate du processus avec le code 97.
⑥ TRAITEMENT — Poser un crochet d'audit de Python (sys.addaudithook), qui reçoit, avant qu'ils aient lieu :
  ① « exec » — l'exécution d'un objet de code, ce que fait tout import de module et tout exec() ; on lit le
  fichier d'origine de l'objet ; ② « cpython.run_file » — le fichier lancé par `python3 X.py` ; ③
  « subprocess.Popen » — tout argument terminé par « .py » d'un sous-processus, vérifié AVANT le lancement,
  dans le parent ; ④ « open » d'un fichier « .pyc » — un fichier compilé qui EXISTE dans le clone. Pour ①
  à ③ : le chemin, résolu, est-il sous GARDE_DONNEES ? Si non (bibliothèque de Python, copie publique),
  rien. Si oui, le fichier au même chemin relatif sous GARDE_CODE existe-t-il, avec les mêmes octets ? Si
  non : refus. Un chemin déjà accepté n'est pas relu.
⑦ UNITÉ — —
⑧ POURQUOI — Décision de Jean-Luc du 08-10-2026 (BACKLOG A-543) : faire tourner au public du code resté au
  privé est écarté, « Non pas question de prendre ces risques » (les conditions de GitHub visent, sur leurs
  machines, toute activité sans lien avec « the software project associated with the repository »). Le
  20-10-2026, un auditeur puis un superviseur (rapports bruts : etudes/brouillons_chat/
  PRIVE_ET_PUBLIC_Mar_20-10-2026/) ont éprouvé six portes par lesquelles du code du clone pouvait tourner
  quand même : des recherches de fichiers par leur nom (le radar a exécuté un brouillon homonyme de
  verif_backlog et a passé de 9 à 6 alertes), un paquet `programmes/X/` qui masque un module, et un
  `git pull` du circuit qui réécrit `programmes/` si un versement arrive pendant un passage. Le superviseur
  (20-10-2026, 18h02) a jugé « arrêter et simplifier » la réparation programme par programme et proposé ce
  garde, qui les ferme toutes par une seule propriété. Décision de Jean-Luc du 20-10-2026 à 17h35 : si le
  code n'est pas celui publié, le circuit « s'arrête et alerte » — d'où l'arrêt, et non un avertissement.
⑨ CE QUI CLOCHE — Ce que le garde ne voit pas, nommé : du code exécuté à partir d'un TEXTE (exec d'une
  chaîne, compile sous un nom inventé hors du clone) ; un Python lancé sans l'environnement du garde
  (`-I`, `-E`, `-S`, ou `env=` vidé) — l'enfant tourne alors sans garde, mais le parent a vérifié le script
  qu'il lançait s'il finit par « .py » ; une extension compilée `.so` (aucun événement « open » de Python ne
  la précède) — le pas « Poser » la refuse avant le passage ; un script shell du clone. · La comparaison
  porte sur le fichier d'ORIGINE de l'objet de code : un `.pyc` qui ne correspondrait pas à sa source passe
  si sa source est identique — d'où le refus de tout `.pyc` présent dans le clone. · Le refus arrive au
  moment de l'exécution : un passage commencé peut s'arrêter au milieu (cas du versement pendant un
  passage) ; les données écrites jusque-là restent ; la collecte se refait au réveil suivant. · La porte
  « cpython.run_file » n'a pas de sabotage propre : morte, la porte « exec » arrête encore le même script
  (doublon relevé par le superviseur le 21-10-2026) ; aucune épreuve ne peut donc la prouver seule. · Du code
  compilé chargé depuis une archive `.zip` du clone, ou depuis un fichier qui ne finit pas par `.pyc`, passe le
  garde et le pas « Poser » (relecteur du 21-10-2026, mesuré : marqueur écrit) ; aucun programme du soir ne
  charge du code ainsi aujourd'hui (BACKLOG). · Le témoin des épreuves ne prouve que l'import d'un module
  publié : une porte « lancement » ou « sous-processus » qui refuserait aussi le code publié n'est pas vue
  (même relecteur) ; l'échec serait du bon côté — tout le passage tomberait, rien ne fuirait.
⑩ EFFET — Sur un refus : écrit une ligne sur la sortie d'erreur et met fin au processus (os._exit). Sinon :
  aucun effet ; ne lit que les fichiers de code exécutés et leurs homologues publics.
⑪ TERMINAISON — Le chargement rend la main aussitôt. Le crochet rend la main, ou met fin au processus sur un
  refus. Aucun de ses appels ne peut ne pas revenir.
"""
import os
import sys

REFUS = 97


def _dossier(nom):
    """Rend le dossier désigné par une variable d'environnement, résolu, ou None.

    ① RÔLE — Lire GARDE_DONNEES ou GARDE_CODE.
    ② CONTEXTE D'APPEL — `poser`.
    ③ ENTRÉE — `nom` : le nom de la
    variable.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin résolu du dossier, ou None si la
    variable est vide ou ne désigne pas un dossier.
      [rend: 1]
    ⑥ TRAITEMENT — os.path.realpath, pour que les liens symboliques ne fassent pas sortir un chemin du clone.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — ④ du programme : sans dossier, pas de garde.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Regarde le disque.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    v = os.environ.get(nom, "")
    if not v:
        return None
    c = os.path.realpath(v)
    return c if os.path.isdir(c) else None


def poser():
    """Pose le crochet d'audit si les deux dossiers sont donnés ; rend vrai s'il est posé.

    ① RÔLE — Mettre le garde en place.
    ② CONTEXTE D'APPEL — Le chargement du module (sous le nom
    sitecustomize.py, au démarrage de Python) ; les épreuves.
    ③ ENTRÉE — Les variables GARDE_DONNEES et
    GARDE_CODE.
    ④ CONDITIONS D'ENTRÉE — ④ du programme.
    ⑤ SORTIE — UNE valeur : vrai si le crochet est posé, faux sinon.
      [rend: 1]
    ⑥ TRAITEMENT — ⑥ du programme ; le crochet est une fermeture sur les deux dossiers et sur l'ensemble des
    chemins déjà acceptés.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — ⑧ du programme.
    ⑨ CE QUI CLOCHE — Un crochet d'audit ne se retire pas : posé deux fois, il vérifie deux fois (sans autre
    effet).
    ⑩ EFFET — sys.addaudithook.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    donnees, code = _dossier("GARDE_DONNEES"), _dossier("GARDE_CODE")
    if not donnees or not code or donnees == code:
        return False
    vus = set()

    def refuser(quoi, rel):
        """Écrit le refus et met fin au processus.

        ① RÔLE — L'arrêt dur.
        ② CONTEXTE D'APPEL — `verifier`, le crochet.
        ③ ENTRÉE — `quoi` : ce qui allait
        se passer · `rel` : le chemin, relatif au clone.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Aucune : le
        processus prend fin.
          [rend: rien]
        ⑥ TRAITEMENT — Une ligne sur la sortie d'erreur, puis os._exit(97),
        qui ne laisse aucun bloc `try` du programme gardé attraper l'arrêt.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Une exception pourrait être avalée par le programme gardé (un `except
        Exception` du radar) ; os._exit ne l'est jamais.
        ⑨ CE QUI CLOCHE — Les fichiers ouverts du processus ne
        sont pas vidés : ce qu'il écrivait est perdu, ce qui est voulu.
        ⑩ EFFET — Fin du processus.
        ⑪ TERMINAISON — Ne revient jamais : os._exit met fin au processus.
          [sort: oui]
        """
        os.write(2, ("\nGARDE DU CODE : REFUS — %s : %s (absent de la copie publique, ou différent d'elle)\n"
                     % (quoi, rel)).encode("utf-8", "replace"))
        os._exit(REFUS)

    def verifier(chemin, quoi):
        """Refuse un fichier de code du clone qui n'est pas, à l'octet, dans la copie publique.

        ① RÔLE — La comparaison.
        ② CONTEXTE D'APPEL — `crochet`.
        ③ ENTRÉE — `chemin` : le fichier qui va être
        exécuté · `quoi` : ce qui allait se passer, pour le message.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Aucune valeur ; un refus met fin au processus.
          [rend: rien]
        ⑥ TRAITEMENT — Ignorer les noms entre chevrons (code venu d'un texte) ; résoudre le chemin ; hors du
        clone, accepter ; dans le clone, comparer les octets au fichier de même chemin relatif dans la copie.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — ⑧ du programme.
        ⑨ CE QUI CLOCHE — ⑨ du programme (code venu d'un texte).
        ⑩ EFFET — Lit deux fichiers.
        ⑪ TERMINAISON — Rend la main, ou met fin au processus.
          [sort: non]
        """
        if not chemin or chemin.startswith("<"):
            return
        c = os.path.realpath(chemin)
        if c in vus:
            return
        if c != donnees and not c.startswith(donnees + os.sep):
            vus.add(c)
            return
        rel = os.path.relpath(c, donnees)
        publie = os.path.join(code, rel)
        try:
            with open(c, "rb") as a, open(publie, "rb") as b:
                pareil = a.read() == b.read()
        except OSError:
            pareil = False
        if not pareil:
            refuser(quoi, rel)
        vus.add(c)

    def crochet(evenement, arguments):
        """Reçoit les événements d'audit de Python et vérifie ceux qui exécutent du code.

        ① RÔLE — Le tri des événements.
        ② CONTEXTE D'APPEL — Python, avant chaque événement audité.
        ③ ENTRÉE — `evenement` : son nom · `arguments` : ses arguments (forme fixée par Python).
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — Aucune valeur.
          [rend: rien]
        ⑥ TRAITEMENT — ⑥ ① à ④ du programme.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Le sous-processus est vérifié dans le PARENT : mesuré le 20-10-2026 par le superviseur,
          le refus d'un enfant lancé avec capture de sa sortie était avalé, et le radar rendait 0. Un
          « .pyc » n'arrête que s'il existe : Python tente d'ouvrir le cache à chaque import, présent ou non.
        ⑨ CE QUI CLOCHE — ⑨ du programme.
        ⑩ EFFET — Celui de `verifier`.
        ⑪ TERMINAISON — Rend la main, ou met fin au processus.
          [sort: non]
        """
        if evenement == "exec":
            verifier(getattr(arguments[0], "co_filename", "") if arguments else "", "exécution")
        elif evenement == "cpython.run_file":
            f = arguments[0] if arguments else ""
            verifier(os.fsdecode(f) if isinstance(f, bytes) else str(f), "lancement")
        elif evenement == "subprocess.Popen":
            argv = arguments[1] if len(arguments) > 1 else None
            liste = [argv] if isinstance(argv, (str, bytes)) else list(argv or [])
            dossier = arguments[2] if len(arguments) > 2 and arguments[2] else os.getcwd()
            for a in liste:
                a = os.fsdecode(a) if isinstance(a, bytes) else str(a)
                if a.endswith(".py"):
                    verifier(a if os.path.isabs(a) else os.path.join(os.fsdecode(dossier), a), "sous-processus")
        elif evenement == "open" and arguments and isinstance(arguments[0], str) and arguments[0].endswith(".pyc"):
            c = os.path.realpath(arguments[0])
            if (c == donnees or c.startswith(donnees + os.sep)) and os.path.exists(c):
                refuser("lecture d'un fichier compilé du clone", os.path.relpath(c, donnees))

    sys.addaudithook(crochet)
    return True


if __name__ == "__main__":
    print(__doc__.split("\n\n")[1])
else:
    poser()
