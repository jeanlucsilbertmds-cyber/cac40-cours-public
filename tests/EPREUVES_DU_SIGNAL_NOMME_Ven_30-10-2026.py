#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_SIGNAL_NOMME — Ven 30-10-2026 20h10 (Paris)
EN ESSAI · Rôle : prouver que chaque fiche du registre des stratégies est jouée par le signal QU'ELLE NOMME, et que
l'épreuve a des dents. SIMULATION UNIQUEMENT : aucun ordre réel.
Quand l'appeler : avant toute livraison qui touche `manques_du_signal`, `signal_de_la_fiche`, `SignalNomme`, `jouer`,
`porte_0` ou `calibrer` de programmes/JUGE_DES_STRATEGIES.py, `jouer_une` de programmes/JOUER_LES_VERSIONS.py,
`_juger_une` de programmes/JUGER_SUR_8_CRITERES.py, ou un module de signal.

À QUOI ÇA SERT (A-542 ① ②, plan du circuit validé par Jean-Luc le 30-10-2026). Jusqu'au 30-10-2026, le juge, la
moulinette et le juge à 8 critères imposaient le signal C5-ETENDU-10 à N'IMPORTE QUELLE fiche. Désormais la fiche
nomme son signal dans trois colonnes (`module_signal`, `fonction_signal`, `reglages_signal`), lues par UNE seule
fonction, `signal_de_la_fiche` du juge. Cette épreuve vérifie, sur une copie du dépôt :
  E1 le calibrage du juge retrouve ses 100 opérations de référence, sortie par sortie (le calibrage existant du juge,
     lancé par son programme principal) ; et `calibrer` refuse un golden qui déclare un autre module ;
  E2 les trois fiches C5 du registre (C5E10-QA-V1, C5E10-OBS-V1, C5-EI-PARAMS) rendent EXACTEMENT les opérations
     qu'elles rendaient avant : même empreinte que l'ancienne lecture (module cherché par le motif
     « MODULE_C5_ETENDU_10 », fonction `signaux_c5etendu10`) et, tant que le fichier maître des cours est celui de la
     mesure du 30-10-2026, mêmes empreintes que celles mesurées sur le code d'avant (version officielle 9307c78) ;
  E3 une fiche RSI(2) est jouée par SA fonction, avec SES réglages : en mémoire, par le programme principal du juge,
     par la moulinette (une version, même nombre d'opérations) et par le juge à 8 critères (même nombre que `jouer`
     sans période ni lecture, comme lui, et différent de celui de C5) ;
  E4 le signal au hasard est reproductible à graine égale, et la graine compte ;
  E5 une fiche sans signal nommé, ou mal nommé, est refusée par la porte 0 ou par la lecture, avec son motif (dont un
     lien symbolique vers un module hors de la racine) ;
  E6 les trois programmes refusent une fiche sans signal (juge : code 1 ; juge à 8 critères : code 2 ; moulinette :
     code 1), et `jouer` refuse un signal qui ne vient pas de la lecture de la fiche ; le juge SANS cible, avec en tête
     du registre une fiche à la graine en texte et une fiche au module introuvable, met la première « EN ÉCHEC »,
     refuse la seconde, juge ensuite C5E10-QA-V1 et rend le code 1 (tour 2, 31-10-2026) ; tour 3 : un module NON
     déclaré (dont le vrai `programmes/audit_ecosysteme.py`) est refusé SANS être exécuté (fichier témoin absent), un
     module illisible, ou déclaré mais qui lève ou fait `sys.exit` au chargement, est refusé, un `sys.exit` au jeu met
     la fiche EN ÉCHEC ; et un `juger` en panne pour C5E10-QA-V1 laisse juger C5E10-OBS-V1, code 1 ;
  E7 propriété du code : dans programmes/, aucune lecture d'une colonne du signal (ni de l'ancien `_fonction_signal`)
     hors des deux fonctions de lecture, et tout programme qui appelle `jouer` appelle aussi `signal_de_la_fiche`.

USAGE : python3 -B tests/EPREUVES_DU_SIGNAL_NOMME_Ven_30-10-2026.py <racine du dépôt> [--saboter | nom]
  sans option : Z0, le dépôt tel quel (environ une minute) ; --saboter : Z0 puis chaque sabotage (environ dix minutes) ;
  un nom de sabotage : celui-là seul.
CODE : 0 si Z0 est tout vert et que chaque sabotage joué fait rougir au moins une épreuve ; 1 sinon ; 2 si une cible
de sabotage est introuvable (R-734 : un contrôle qui n'a pas pu tourner ne rend pas 0).

① RÔLE — Voir « À QUOI ÇA SERT ».
② CONTEXTE D'APPEL — À la main ; et par la certification (`programmes/CERTIFIER_LA_VERSION.py`), qui lance chaque
  épreuve de tests/ depuis la racine avec la racine en argument. Ce programme se relance lui-même avec
  « --cas <copie> » pour jouer les épreuves dans une copie : ce mode n'est pas fait pour la main.
③ ENTRÉE — La racine du dépôt ; `--saboter` ou un nom de sabotage, facultatif.
④ CONDITIONS D'ENTRÉE — Sous la racine : les trois programmes, le module C5, les deux modules de signal ajoutés le
  30-10-2026, le registre des stratégies avec ses trois colonnes du signal, le fichier maître des cours, le
  référentiel, le golden, son témoin et le tableau des 100 trades, la combinatoire de C5E10-OBS-V1.
⑤ SORTIE — Le code de sortie dit en « CODE » ; une ligne par épreuve et par sabotage. [rend: 1]
⑥ TRAITEMENT — Pour Z0 puis chaque sabotage : ① copier la racine dans un dossier temporaire (sans .git, etudes,
  caches) · ② appliquer le sabotage, en exigeant que sa cible existe une fois · ③ relancer ce programme en mode
  « --cas » sur la copie · ④ Z0 doit être vert, un sabotage doit faire échouer au moins une épreuve.
⑦ UNITÉ — Des codes de sortie, des nombres d'opérations, des empreintes SHA-256 tronquées à 16 caractères.
⑧ POURQUOI — Un jeu d'épreuves se sabote contre sa propre correction (R-731) : une épreuve qui reste verte quand on
  retire ce qu'elle teste est une décoration. Les cas réels (R-732) : les vraies fiches C5E10-QA-V1, C5E10-OBS-V1,
  C5-EI-PARAMS et MA200-S1 du registre, le vrai maître des cours.
⑨ CE QUI CLOCHE — ① Les empreintes figées de E2 ne valent que pour le maître mesuré le 30-10-2026 (empreinte
  95533af96e512515) : sur un autre maître, E2 le DIT et ne compare plus qu'à l'ancienne lecture. ② E7 lit le code
  sans l'exécuter : une lecture des colonnes par un nom calculé (`getattr`, chaîne composée) lui échappe ; et un appel
  de `jouer` du juge par son nom nu, dans un programme qui définit sa propre `jouer`, n'est pas compté. ③ La
  moulinette refuse une fiche sans signal parce que le juge, qu'elle lance d'abord, la refuse : son propre repli
  éventuel n'est vu que par E7.
⑩ EFFET — Écrit seulement dans des dossiers temporaires, effacés ; `-B` partout, aucun fichier compilé.
⑪ TERMINAISON — Sort lui-même. Chaque sous-processus a un délai ; un délai dépassé compte comme un échec.
  [sort: oui]
"""
import ast
import csv
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

C5 = "programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py"
RSI = "programmes/MODULE_SIGNAL_RSI2_CONNORS.py"
HASARD = "programmes/MODULE_SIGNAL_AU_HASARD.py"
JUGE = "programmes/JUGE_DES_STRATEGIES.py"
J8 = "programmes/JUGER_SUR_8_CRITERES.py"
JOUER = "programmes/JOUER_LES_VERSIONS.py"
# Mesurées le 30-10-2026 à 19h25 sur le code d'AVANT (version officielle 9307c78, juge generique-1.5), maître des
# cours d'empreinte 95533af96e512515, par le jeu de chaque fiche au lecteur unique sur sa période : nombre
# d'opérations et empreinte de la liste des opérations (json trié).
MAITRE_DE_LA_MESURE = "95533af96e512515"
AVANT = {"C5E10-QA-V1": (51, "564ccafa9527e254"), "C5E10-OBS-V1": (89, "cabc7102d02c9b35"),
         "C5-EI-PARAMS": (48, "1eb3d8510391f590")}
RSI_REGLAGES = '{"periode": 2, "seuil": 10, "tendance": 200}'
# le nombre de cas que `cas` doit rendre (E1, E1b, E2 à E7) : une épreuve qui en rend moins a été interrompue
NOMBRE_DE_CAS = 8
MODULE_DU_C5_AVANT = "programmes/MODULE_C5_ETENDU_10_Sam_11-07-2026_19h32.py"

SABOTAGES = {
    "Z0": [],
    # le repli vers C5 remis dans le programme principal du juge, avant la porte 0
    "S1_repli_C5_dans_le_juge": [(JUGE, "        ok, manq, _b0 = porte_0(f)\n",
                                  "        f[\"module_signal\"] = f.get(\"module_signal\") or %r\n"
                                  "        f[\"fonction_signal\"] = f.get(\"fonction_signal\") or \"signaux_c5etendu10\"\n"
                                  "        ok, manq, _b0 = porte_0(f)\n" % MODULE_DU_C5_AVANT)],
    # le repli vers C5 remis dans le juge à 8 critères
    "S2_repli_C5_dans_J8": [(J8, "        mod_sig = banc.signal_de_la_fiche(base, fiche)\n",
                             "        fiche[\"module_signal\"] = fiche.get(\"module_signal\") or %r\n"
                             "        fiche[\"fonction_signal\"] = fiche.get(\"fonction_signal\") or \"signaux_c5etendu10\"\n"
                             "        mod_sig = banc.signal_de_la_fiche(base, fiche)\n" % MODULE_DU_C5_AVANT)],
    # le repli vers C5 remis dans la moulinette, à la fusion d'une version
    "S3_repli_C5_dans_la_moulinette": [(JOUER, "    f = dict(fiche)\n",
                                        "    f = dict(fiche)\n"
                                        "    f[\"fonction_signal\"] = f.get(\"fonction_signal\") or \"signaux_c5etendu10\"\n")],
    # une fiche sans fonction de signal passe la porte 0
    "S4_fiche_sans_fonction_acceptee": [(JUGE, "    if fonction.lower() in VIDE:\n        manq.append(\"fonction_signal (aucun signal nommé)\")\n    elif",
                                         "    if False:\n        pass\n    elif")],
    # la lecture des colonnes recopiée dans la moulinette au lieu d'appeler la fonction unique
    "S5_lecture_recopiee_dans_la_moulinette": [(JOUER, "        mod_sig = J.signal_de_la_fiche(base, f)",
                                                "        mod_sig = J.SignalNomme(getattr(J.charger_module(os.path.join(base, f[\"module_signal\"]), \"s\"), "
                                                "f[\"fonction_signal\"]), {}, \"recopie\")")],
    # la lecture des colonnes recopiée dans le juge à 8 critères
    "S6_lecture_recopiee_dans_J8": [(J8, "        mod_sig = banc.signal_de_la_fiche(base, fiche)\n",
                                     "        mod_sig = banc.SignalNomme(getattr(banc.charger_module(os.path.join(base, fiche[\"module_signal\"]), \"s\"), "
                                     "fiche[\"fonction_signal\"]), {}, \"recopie\")\n")],
    # le tirage du hasard dépend de l'heure : il n'est plus reproductible
    "S7_hasard_sans_graine": [(HASARD, '    texte = "%d|%s|%r" % (graine, date, float(cloture))',
                               '    texte = "%d|%s|%r|%r" % (graine, date, float(cloture), __import__("time").perf_counter_ns())')],
    # les réglages de la fiche ne sont plus passés à la fonction
    "S8_reglages_ignores": [(JUGE, "        return self.fonction(serie, **self.reglages)",
                             "        return self.fonction(serie)")],
    # `jouer` accepte n'importe quoi en guise de signal
    "S9_jouer_accepte_un_module": [(JUGE, "    if not isinstance(mod_signal, SignalNomme):\n",
                                    "    if False:\n")],
    # le calibrage ne confronte plus son module à celui que le golden déclare
    "S10_calibrage_sans_le_module_du_golden": [(JUGE, "    if _mod_golden != _mod_cal:\n", "    if False:\n")],
    # tour 2 (relecture et superviseur R-759 du 31-10-2026)
    # M1 : le contrôle « sort de la racine » retiré
    "M1_commonpath_retire": [(JUGE, "    if os.path.commonpath([racine, chemin]) != racine:\n", "    if False:\n")],
    # M2 : le programme principal du juge lève au lieu de refuser une fiche au module introuvable
    "M2_main_leve_au_lieu_de_refuser": [(JUGE, "            try:\n                f[\"_signal\"] = signal_de_la_fiche(base, f)\n"
                                               "            except ValueError as _e:\n                ok, manq = False, [str(_e)]\n",
                                         "            f[\"_signal\"] = signal_de_la_fiche(base, f)\n")],
    # M3 : la moulinette joue C5 à la place du signal nommé, en passant toujours par la lecture unique
    "M3_moulinette_joue_C5_a_la_place": [(JOUER, "        mod_sig = J.signal_de_la_fiche(base, f)",
                                          "        mod_sig = J.signal_de_la_fiche(base, dict(f, **J.SIGNAL_DU_CALIBRAGE))")],
    # M3 bis : le même dans le juge à 8 critères
    "M3bis_J8_joue_C5_a_la_place": [(J8, "        mod_sig = banc.signal_de_la_fiche(base, fiche)",
                                     "        mod_sig = banc.signal_de_la_fiche(base, dict(fiche, **banc.SIGNAL_DU_CALIBRAGE))")],
    # l'isolation des fiches retirée : une fiche qui lève au jeu arrête tout le juge
    "isolation_retiree": [(JUGE, "        except (Exception, SystemExit) as _ex_jeu:\n", "        except ZeroDivisionError as _ex_jeu:\n")],
    # tour 3 (relecture de clôture et superviseur R-759 du 31-10-2026) : un sabotage par garde
    "N1_isolation_du_jugement_retiree": [(JUGE, "            except (Exception, SystemExit) as _ex_jugement:\n",
                                          "            except ZeroDivisionError as _ex_jugement:\n")],
    "T1_declaration_non_lue": [(JUGE, "        if _refus:\n", "        if False:\n")],
    "T2_syntaxe_non_rattrapee": [(JUGE, "    except (SyntaxError, ValueError) as _e_syntaxe:",
                                  "    except ZeroDivisionError as _e_syntaxe:")],
    "T3_filet_du_chargement_retire": [(JUGE, "        except (Exception, SystemExit) as _e_charge:\n",
                                       "        except ZeroDivisionError as _e_charge:\n")],
    "T4_SystemExit_hors_du_filet": [(JUGE, "        except (Exception, SystemExit) as _e_charge:\n",
                                     "        except Exception as _e_charge:\n")],
    "T5_SystemExit_hors_de_l_isolation_du_jeu": [(JUGE, "        except (Exception, SystemExit) as _ex_jeu:\n",
                                                  "        except Exception as _ex_jeu:\n")],
}


def lancer(copie, *arguments, delai=600):
    """Lance un programme Python dans la copie et rend son code et sa sortie.

    ① RÔLE — Un seul geste pour tous les lancements de programmes de la copie.
    ② CONTEXTE D'APPEL — Les épreuves E1, E3, E6.
    ③ ENTRÉE — `copie` : la racine de la copie · `arguments` : le programme et ses arguments · `delai` : en secondes.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le code de sortie (124 si le délai est dépassé), la sortie, erreurs comprises. [rend: 2]
    ⑥ TRAITEMENT — `python3 -B` depuis la racine de la copie.
    ⑦ UNITÉ — Secondes.
    ⑧ POURQUOI — Les programmes s'éprouvent tels qu'ils tournent, ligne de commande comprise.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Ce que fait le programme lancé ; dans la copie seulement.
    ⑪ TERMINAISON — Rend la main ; borné par le délai. [sort: non]
    """
    try:
        r = subprocess.run([sys.executable, "-B"] + list(arguments), cwd=copie, capture_output=True, text=True,
                           timeout=delai)
        return r.returncode, r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return 124, "délai de %d s dépassé" % delai


def empreinte_ops(ops):
    """Rend l'empreinte d'une liste d'opérations.

    ① RÔLE — Comparer deux listes d'opérations à l'octet près, champ par champ.
    ② CONTEXTE D'APPEL — E2, E3, E4.
    ③ ENTRÉE — `ops` : la liste rendue par `jouer`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : 16 caractères hexadécimaux. [rend: 1]
    ⑥ TRAITEMENT — json trié, SHA-256, tronqué.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — La même écriture que la mesure du 30-10-2026 qui a produit les empreintes de `AVANT`.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    return hashlib.sha256(json.dumps(ops, sort_keys=True).encode()).hexdigest()[:16]


def ajouter_des_fiches(copie, fiches, en_tete=False):
    """Ajoute des fiches au registre des stratégies de la copie.

    ① RÔLE — Poser dans la copie les fiches d'épreuve que le programme principal du juge, le juge à 8 critères et la
      moulinette liront.
    ② CONTEXTE D'APPEL — `cas`, une fois, avant les épreuves.
    ③ ENTRÉE — `copie` · `fiches` : des dictionnaires, chacun complété par les colonnes de l'en-tête · `en_tete` :
      vrai pour les écrire juste après l'en-tête, AVANT les fiches réelles (le juge joue dans l'ordre du registre).
    ④ CONDITIONS D'ENTRÉE — Le registre de la copie existe.
    ⑤ SORTIE — Aucune valeur. [rend: 0]
    ⑥ TRAITEMENT — Lire l'en-tête, écrire chaque fiche en fin de fichier, ou juste après l'en-tête.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — « Ajouter une famille = son module et sa fiche » se prouve en ajoutant une fiche, et rien d'autre.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans le registre de la COPIE, jamais dans celui du dépôt.
    ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    # le chemin du registre vit au contrat de la copie (n°83, 05-11-2026)
    sys.path.insert(0, os.path.join(copie, "programmes"))
    import CONTRATS_DES_FICHIERS as contrat
    p = os.path.join(copie, contrat.REGISTRE_DES_STRATEGIES)
    entete = next(csv.reader(open(p, encoding="utf-8-sig")))
    import io
    tampon = io.StringIO()
    w = csv.writer(tampon, lineterminator="\r\n")
    for f in fiches:
        w.writerow([f.get(c, "") for c in entete])
    if not en_tete:
        with open(p, "a", encoding="utf-8", newline="") as h:
            h.write(tampon.getvalue())
        return
    brut = open(p, "rb").read().decode("utf-8")
    k = brut.index("\n") + 1
    with open(p, "w", encoding="utf-8", newline="") as h:
        h.write(brut[:k] + tampon.getvalue() + brut[k:])


def cas(copie):
    """Joue les épreuves E1 à E7 dans une copie, et rend la liste de leurs verdicts.

    ① RÔLE — Le cœur de l'épreuve : chaque cas dit vert ou rouge, avec ce qu'il a vu.
    ② CONTEXTE D'APPEL — Le mode « --cas » de ce programme, une fois par copie (Z0 ou un sabotage).
    ③ ENTRÉE — `copie` : la racine d'une copie du dépôt, éventuellement sabotée.
    ④ CONDITIONS D'ENTRÉE — Voir l'en-tête, ④.
    ⑤ SORTIE — UNE valeur : la liste des (nom, réussi, détail). [rend: 1]
    ⑥ TRAITEMENT — ① ajouter au registre de la copie une fiche RSI(2) et une fiche sans signal · ② E1 à E7 ; un cas
      qui lève compte comme échoué, avec l'erreur en détail.
    ⑦ UNITÉ — Voir l'en-tête, ⑦.
    ⑧ POURQUOI — Voir l'en-tête, ⑧.
    ⑨ CE QUI CLOCHE — Voir l'en-tête, ⑨.
    ⑩ EFFET — Écrit dans la copie (registre, combinatoire d'épreuve) ; lance des programmes de la copie.
    ⑪ TERMINAISON — Rend la main ; chaque lancement est borné. [sort: non]
    """
    res = []

    def un(nom, f):
        # SystemExit COMPRIS (tour 3, 31-10-2026) : un module d'épreuve qui fait `sys.exit(0)` dans un appel EN MÉMOIRE
        # (le `main` du juge en E6) aurait fait sortir l'épreuve elle-même avec 0, sans rien dire ; mesuré sur les
        # sabotages T4 et T5 avant ce correctif : « NE MORD PAS (code 0) », sortie vide.
        try:
            ok, detail = f()
        except (Exception, SystemExit) as e:
            ok, detail = False, "%s : %s" % (type(e).__name__, str(e)[:200])
        res.append((nom, bool(ok), detail))

    sys.path.insert(0, os.path.join(copie, "programmes"))
    os.chdir(copie)
    import JUGE_DES_STRATEGIES as B
    # le registre se nomme et se lit au contrat de la copie ; la dernière ligne d'un identifiant fait foi (n°83)
    import CONTRATS_DES_FICHIERS as contrat
    par_id = contrat.fiches_du_registre(contrat.REGISTRE_DES_STRATEGIES)
    qa, obs = dict(par_id["C5E10-QA-V1"]), dict(par_id["C5E10-OBS-V1"])
    rsi_fiche = dict(obs, id="EPREUVE-RSI2", nom="EPREUVE RSI(2) de Connors", etat_vie="LABO",
                     module_signal=RSI, fonction_signal="signaux_rsi2", reglages_signal=RSI_REGLAGES)
    sans = dict(qa, id="EPREUVE-SANS-SIGNAL", nom="EPREUVE sans signal nomme", etat_vie="LABO",
                module_signal="", fonction_signal="", reglages_signal="")
    ajouter_des_fiches(copie, [rsi_fiche, sans])
    # EN TÊTE du registre, avant C5E10-QA-V1 (superviseur R-759 du 31-10-2026, I1 et I2-M2) : une fiche qui passe la
    # porte 0 mais lève au jeu (graine « 7 » en texte), et une fiche dont le module est introuvable.
    graine_texte = dict(obs, id="AAA-EPREUVE-GRAINE-TEXTE", nom="EPREUVE graine en texte", etat_vie="LABO",
                        module_signal=HASARD, fonction_signal="signaux_au_hasard",
                        reglages_signal='{"graine": "7", "proportion": 0.02}')
    introuvable = dict(qa, id="AAA-EPREUVE-INTROUVABLE", nom="EPREUVE module introuvable", etat_vie="LABO",
                       module_signal="programmes/N_EXISTE_PAS.py")
    # TOUR 3 (superviseur R-759 du 31-10-2026, voie D) : des modules d'épreuve écrits dans la copie, et leurs fiches en
    # tête du registre. Un module NON déclaré écrit un fichier témoin à son chargement : s'il existe après les
    # lancements, le juge l'a exécuté.
    temoin_exec = os.path.join(copie, "donnees", "TEMOIN_EXECUTION_NON_DECLARE.txt")
    declare = '"""EN ESSAI · module de signal · Rôle : module d\'épreuve du signal nommé.\n"""\n'
    modules = {
        "programmes/EPREUVE_NON_DECLARE_ECRIT.py": ('"""Module d\'épreuve, NON déclaré."""\n'
                                                   'open(%r, "w").write("execute")\n'
                                                   'def signaux(ohlcv):\n    return []\n' % temoin_exec),
        "programmes/EPREUVE_SYNTAXE.py": declare + "def signaux(ohlcv:\n",
        "programmes/EPREUVE_DECLARE_LEVE.py": declare + 'raise RuntimeError("module d\'épreuve cassé au chargement")\n',
        "programmes/EPREUVE_DECLARE_EXIT_CHARGEMENT.py": declare + "import sys\nsys.exit(0)\n",
        "programmes/EPREUVE_DECLARE_EXIT_JEU.py": declare + "import sys\ndef signaux(ohlcv):\n    sys.exit(0)\n",
    }
    for chemin_m, texte_m in modules.items():
        open(os.path.join(copie, chemin_m), "w", encoding="utf-8").write(texte_m)
    fiche_m = lambda ident, module_m, fonction_m="signaux": dict(qa, id=ident, nom="EPREUVE " + ident, etat_vie="LABO",
                                                                 module_signal=module_m, fonction_signal=fonction_m,
                                                                 reglages_signal="")
    ajouter_des_fiches(copie, [graine_texte, introuvable,
                               fiche_m("AAA-EPREUVE-NON-DECLARE", "programmes/EPREUVE_NON_DECLARE_ECRIT.py"),
                               fiche_m("AAA-EPREUVE-AUDIT", "programmes/audit_ecosysteme.py", "main"),
                               fiche_m("AAA-EPREUVE-SYNTAXE", "programmes/EPREUVE_SYNTAXE.py"),
                               fiche_m("AAA-EPREUVE-LEVE", "programmes/EPREUVE_DECLARE_LEVE.py"),
                               fiche_m("AAA-EPREUVE-EXIT-CHARGEMENT", "programmes/EPREUVE_DECLARE_EXIT_CHARGEMENT.py"),
                               fiche_m("AAA-EPREUVE-EXIT-JEU", "programmes/EPREUVE_DECLARE_EXIT_JEU.py")],
                       en_tete=True)
    mnemo = B.table_mnemoniques(B.trouver(".", "REFERENTIEL_VALEURS"))
    cours, lec = B.lire_par_le_lecteur(".", "donnees/cours_maitre.csv", mnemo)
    pos = B.charger_module(B.trouver(".", "MODULE_POSITIONS.py"), "pos")

    def jouer_la_fiche(f):
        ok0, manq, bornes = B.porte_0(f)
        if not ok0:
            raise ValueError("porte 0 : %s" % manq)
        ops, _ = B.jouer(f, cours, mnemo, B.signal_de_la_fiche(".", f), pos, periode=bornes, lecture=lec)
        return ops

    # ── E1 le calibrage du juge, par son programme principal ; et le module du golden ─────────────────────────────
    def e1():
        code, out = lancer(copie, JUGE, ".", "C5E10-QA-V1")
        vu = {"code 0": code == 0,
              "témoin du golden": "calibrage sur le TEMOIN du golden" in out,
              "100 sorties": re.search(r"sorties : 100/100 identiques", out) is not None,
              "calibré": "-> OK, l'instrument est calibre." in out,
              "signal de la fiche affiché": ("signal : %s · signaux_c5etendu10" % C5) in out}
        return all(vu.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items())
    un("E1 calibrage du juge : 100 opérations de référence, sortie par sortie", e1)

    def e1b():
        golden = json.load(open(B.trouver(".", "golden_tests_"), encoding="utf-8"))
        golden = dict(golden, meta=dict(golden.get("meta") or {}, module="AUTRE_MODULE.py (pour l'épreuve)"))
        ok, l = B.calibrer(cours, mnemo, ".", pos, golden)
        return (not ok) and any("le golden declare le module" in x for x in l), "calibre %s · %s" % (ok, l[:1])
    un("E1b calibrer refuse un golden qui déclare un autre module", e1b)

    # ── E2 les fiches C5 : mêmes opérations qu'avant ───────────────────────────────────────────────────────────────
    def e2():
        ancien = B.SignalNomme(getattr(B.charger_module(B.trouver(".", "MODULE_C5_ETENDU_10"), "ancien"),
                                       "signaux_c5etendu10"), {}, "ancienne lecture (motif MODULE_C5_ETENDU_10)")
        maitre = hashlib.sha256(open("donnees/cours_maitre.csv", "rb").read()).hexdigest()[:16]
        ok, d = True, []
        for ident, (n_avant, e_avant) in AVANT.items():
            f = dict(par_id[ident])
            if not (f.get("entree") or "").strip():
                # depuis le 31-10-2026 (version B, point 5), une case entree VIDE est refusée (C5-EI-PARAMS) ; la
                # comparaison des opérations se fait à mécanique égale, avec « DÉFAUT » (l'ouverture du lendemain)
                f["entree"] = "DÉFAUT"
            ok0, _m, bornes = B.porte_0(f)
            neuf = jouer_la_fiche(f)
            vieux, _ = B.jouer(f, cours, mnemo, ancien, pos, periode=bornes, lecture=lec)
            bon = empreinte_ops(neuf) == empreinte_ops(vieux) and len(neuf) > 0
            if maitre == MAITRE_DE_LA_MESURE:
                bon = bon and (len(neuf), empreinte_ops(neuf)) == (n_avant, e_avant)
            ok = ok and bon
            d.append("%s %d op %s (ancienne lecture %s%s)" % (ident, len(neuf), empreinte_ops(neuf), empreinte_ops(vieux),
                                                            ", avant %s" % e_avant if maitre == MAITRE_DE_LA_MESURE else ""))
        if maitre != MAITRE_DE_LA_MESURE:
            d.append("maître %s, pas celui de la mesure (%s) : comparé à l'ancienne lecture seulement" % (maitre, MAITRE_DE_LA_MESURE))
        return ok, " · ".join(d)
    un("E2 C5E10-QA-V1, C5E10-OBS-V1, C5-EI-PARAMS : mêmes opérations qu'avant", e2)

    # ── E3 une fiche RSI(2) jouée par SA fonction, avec SES réglages ───────────────────────────────────────────────
    def e3():
        import importlib.util as iu
        sp = iu.spec_from_file_location("rsi_independant", RSI)
        M = iu.module_from_spec(sp)
        sp.loader.exec_module(M)
        cas_main = (M.rsi_wilder([10, 11, 10, 9], 2) == [None, None, 50.0, 25.0]
                    and M.signaux_rsi2([{"close": c} for c in (10, 11, 10, 9)], 2, 30, 0) == [{"i": 3, "rsi": 25.0}])
        reg = json.loads(RSI_REGLAGES)
        attendus = set()
        for x in rsi_fiche["univers"].split(","):
            v = mnemo.get(x.strip().upper(), B.cle_valeur(x))
            for s in B.couper_aux_trous(cours[v], lec["trous"].get(v, [])):
                attendus |= {(v, s[sg["i"]]["date"]) for sg in M.signaux_rsi2(s, **reg)}
        ops = jouer_la_fiche(dict(rsi_fiche))
        joues = {(o["valeur"], o["date_signal"]) for o in ops}
        ops5 = jouer_la_fiche(dict(rsi_fiche, reglages_signal=RSI_REGLAGES.replace('"seuil": 10', '"seuil": 5')))
        c5 = jouer_la_fiche(dict(obs))
        # PAR LA MOULINETTE ET PAR LE JUGE À 8 CRITÈRES (superviseur R-759 du 31-10-2026, I2-M3) : une épreuve de
        # COMPORTEMENT, qui attrape toute substitution du signal, quelle que soit la façon de l'écrire.
        dossier = tempfile.mkdtemp(prefix="comb_rsi_")
        comb = os.path.join(dossier, "COMBINATOIRE_EPREUVE-RSI2_E01.csv")
        with open(comb, "w", encoding="utf-8", newline="") as h:
            w = csv.writer(h)
            w.writerow(["id_version", "strategie", "essai", "tp", "sl", "horizon", "univers", "versions_dans_l_essai",
                        "version_de_la_fiche"])
            w.writerow(["EPREUVE-RSI2-E01-0001", "EPREUVE-RSI2", "E01", repr(B.pourcent(rsi_fiche["tp"])),
                        repr(B.pourcent(rsi_fiche["sl"])), str(B.lire_horizon(rsi_fiche["horizon"])),
                        rsi_fiche["univers"], "1", "OUI"])
        res_comb = os.path.join(dossier, "RESULTATS_EPREUVE-RSI2_E01.csv")
        c_m, out_m = lancer(copie, JOUER, ".", comb, res_comb)
        n_moulinette = (int(next(csv.DictReader(open(res_comb, encoding="utf-8")))["operations"])
                        if c_m == 0 and os.path.exists(res_comb) else None)
        shutil.rmtree(dossier, ignore_errors=True)
        # le juge à 8 critères joue sans période ni lecture — DÉFAUT CONNU, antérieur au lot, consigné au BACKLOG (m-b de
        # la relecture du 31-10-2026 ; ⑨ ⑨ de `_juger_une`) : on lui compare `jouer` appelé de la même façon, et non les
        # 128 opérations de la période. Le jour où il sera réparé, ce cas rougira : c'est voulu.
        cours_j8 = B.charger_cours(*B.fichiers_de_cours("."))
        attendu_j8 = len(B.jouer(dict(rsi_fiche), cours_j8, mnemo, B.signal_de_la_fiche(".", rsi_fiche), pos)[0])
        c5_j8 = len(B.jouer(dict(obs), cours_j8, mnemo, B.signal_de_la_fiche(".", obs), pos)[0])
        c_8, out_8 = lancer(copie, J8, ".", "--strategie", "EPREUVE-RSI2")
        m8 = re.search(r"EPREUVE-RSI2 : (\d+) opération", out_8)
        n_j8 = int(m8.group(1)) if c_8 == 0 and m8 else None
        code, out = lancer(copie, JUGE, ".", "EPREUVE-RSI2")
        m = re.search(r"=== EPREUVE-RSI2 [^\n]*\n(?:[^\n]*\n){0,3}?\s+(\d+) operations[^\n]*\n"
                      r"\s+signal : (\S+) · (\S+) · réglages ([^\n]*?) \. empreinte", out)
        vu = {"cas à la main": cas_main,
              "opérations jouées": len(ops) > 0,
              "toutes sur un signal RSI": joues <= attendus,
              "autres que C5": empreinte_ops(ops) != empreinte_ops(c5),
              "le seuil compte": empreinte_ops(ops5) != empreinte_ops(ops),
              "le juge la joue": code == 0 and m is not None and m.group(2) == RSI and m.group(3) == "signaux_rsi2"
                                 and int(m.group(1)) == len(ops),
              "la moulinette la joue": n_moulinette == len(ops),
              "le juge à 8 critères la joue": n_j8 == attendu_j8 and attendu_j8 != c5_j8}
        return all(vu.values()), ("%d opérations (%d signaux RSI possibles) · seuil 5 : %d · moulinette %s · juge à 8 "
                                  "critères %s (attendu %d, C5 aurait %d) · %s") % (
            len(ops), len(attendus), len(ops5), n_moulinette, n_j8, attendu_j8, c5_j8,
            " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items()))
    un("E3 une fiche RSI(2) est jouée par SA fonction et SES réglages", e3)

    # ── E4 le signal au hasard ─────────────────────────────────────────────────────────────────────────────────────
    def e4():
        h = lambda g: dict(obs, id="EPREUVE-HASARD", module_signal=HASARD, fonction_signal="signaux_au_hasard",
                           reglages_signal='{"graine": %d, "proportion": 0.02}' % g)
        a, b, c = jouer_la_fiche(h(7)), jouer_la_fiche(h(7)), jouer_la_fiche(h(8))
        c5 = jouer_la_fiche(dict(obs))
        vu = {"graine égale, mêmes opérations": empreinte_ops(a) == empreinte_ops(b) and len(a) > 0,
              "autre graine, autres opérations": empreinte_ops(a) != empreinte_ops(c),
              "autres que C5": empreinte_ops(a) != empreinte_ops(c5)}
        return all(vu.values()), "graine 7 : %d op (%s, puis %s) · graine 8 : %d op · %s" % (
            len(a), empreinte_ops(a), empreinte_ops(b), len(c), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items()))
    un("E4 le signal au hasard est reproductible à graine égale", e4)

    # ── E5 refus : porte 0 et lecture ──────────────────────────────────────────────────────────────────────────────
    def e5():
        vu = {}
        ok, m, _ = B.porte_0(dict(qa, fonction_signal=""))
        vu["sans fonction : porte 0 refuse"] = (not ok) and "fonction_signal (aucun signal nommé)" in m
        ok, m, _ = B.porte_0(dict(qa, module_signal=""))
        vu["sans module : porte 0 refuse"] = (not ok) and "module_signal (aucun signal nommé)" in m
        ok, m, _ = B.porte_0(dict(par_id["MA200-S1"], periode="2024-01-02 -> 2026-07-10"))
        vu["MA200-S1 réelle, sans signal : refusée pour le signal"] = (not ok) and "fonction_signal (aucun signal nommé)" in m
        ok, m, _ = B.porte_0(dict(qa, reglages_signal="{x"))
        vu["réglages illisibles : porte 0 refuse"] = (not ok) and any(x.startswith("reglages_signal illisible") for x in m)
        ok, m, _ = B.porte_0(dict(qa, module_signal="../MODULE.py"))
        vu["chemin hors racine : porte 0 refuse"] = (not ok) and any(x.startswith("module_signal illisible") for x in m)
        # m1 (relecture du 31-10-2026) : un lien symbolique sous programmes/ vers un module HORS de la racine
        dehors = tempfile.mkdtemp(prefix="dehors_")
        shutil.copyfile(C5, os.path.join(dehors, "MODULE_DEHORS.py"))
        lien = os.path.join("programmes", "LIEN_DEHORS_EPREUVE.py")
        if os.path.lexists(lien):
            os.remove(lien)
        os.symlink(os.path.join(dehors, "MODULE_DEHORS.py"), lien)
        for lib, f, motif in (("lien hors racine", dict(qa, module_signal=lien), "sort de la racine"),
                              ("module introuvable", dict(qa, module_signal="programmes/N_EXISTE_PAS.py"), "introuvable"),
                              ("fonction absente", dict(qa, fonction_signal="n_existe_pas"), "n'expose pas"),
                              ("réglages hors signature", dict(qa, reglages_signal='{"seuil": 3}'), "ne s'appliquent pas")):
            try:
                B.signal_de_la_fiche(".", f)
                vu[lib + " : lecture refuse"] = False
            except ValueError as e:
                vu[lib + " : lecture refuse"] = motif in str(e)
        os.remove(lien)
        shutil.rmtree(dehors, ignore_errors=True)
        return all(vu.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items())
    un("E5 une fiche sans signal, ou mal nommé, est refusée avec son motif", e5)

    # ── E6 les trois programmes refusent une fiche sans signal ; `jouer` refuse un module ──────────────────────────
    def e6():
        vu = {}
        code, out = lancer(copie, JUGE, ".", "EPREUVE-SANS-SIGNAL")
        vu["juge : code 1, refusée à la porte 0"] = code == 1 and re.search(
            r"EPREUVE-SANS-SIGNAL refusee .*fonction_signal \(aucun signal nommé\)", out) is not None
        # LE JUGE SANS CIBLE (superviseur R-759 du 31-10-2026, I1 et I2-M2) : en tête du registre, une fiche à la graine
        # en texte (passe la porte 0, lève au jeu) et une fiche au module introuvable ; les fiches réelles qui suivent
        # doivent être jugées, et le code final doit être non nul.
        code, out = lancer(copie, JUGE, ".")
        m_qa = re.search(r"=== C5E10-QA-V1 [^\n]*\n(?:[^\n]*\n){0,3}?\s+(\d+) operations", out)
        maitre = hashlib.sha256(open("donnees/cours_maitre.csv", "rb").read()).hexdigest()[:16]
        vu["juge sans cible : graine texte EN ÉCHEC"] = re.search(
            r"=== AAA-EPREUVE-GRAINE-TEXTE [^\n]*\n(?:[^\n]*\n){0,4}?\s+EN ÉCHEC \(ce n'est pas un refus\) : ValueError",
            out) is not None
        vu["juge sans cible : module introuvable refusé"] = re.search(
            r"AAA-EPREUVE-INTROUVABLE refusee .*introuvable sous la racine", out) is not None
        vu["juge sans cible : C5E10-QA-V1 jugée ensuite"] = m_qa is not None and (
            maitre != MAITRE_DE_LA_MESURE or int(m_qa.group(1)) == AVANT["C5E10-QA-V1"][0])
        vu["juge sans cible : code 1, échec dit"] = code == 1 and "FICHES EN ÉCHEC" in out
        # TOUR 3 : la déclaration, le filet du chargement, SystemExit au jeu
        refus = lambda ident, motif: re.search(r"%s refusee .*%s" % (re.escape(ident), motif), out) is not None
        vu["non déclaré : refusé, jamais exécuté"] = (refus("AAA-EPREUVE-NON-DECLARE", "ne se déclare pas « module de signal »")
                                                     and not os.path.exists(temoin_exec))
        vu["audit_ecosysteme.py : refusé, radar non lancé"] = (refus("AAA-EPREUVE-AUDIT", "ne se déclare pas « module de signal »")
                                                               and "AUDIT ÉCOSYSTÈME" not in out)
        vu["syntaxe : refusé, pas du Python lisible"] = refus("AAA-EPREUVE-SYNTAXE", "n'est pas du Python lisible")
        vu["déclaré qui lève au chargement : refusé"] = refus("AAA-EPREUVE-LEVE", "ne se charge pas : RuntimeError")
        vu["déclaré qui sort au chargement : refusé"] = refus("AAA-EPREUVE-EXIT-CHARGEMENT", "ne se charge pas : SystemExit")
        vu["déclaré qui sort au jeu : EN ÉCHEC"] = re.search(
            r"=== AAA-EPREUVE-EXIT-JEU [^\n]*\n(?:[^\n]*\n){0,4}?\s+EN ÉCHEC \(ce n'est pas un refus\) : SystemExit",
            out) is not None
        # m-a : l'isolation du JUGEMENT — `juger` remplacé en mémoire par une fonction qui lève pour C5E10-QA-V1 ; la fiche
        # suivante, C5E10-OBS-V1, doit être jugée, et le code doit être 1
        import io, contextlib
        vrai_juger, vrai_argv = B.juger, sys.argv

        def juger_en_panne(f, *a, **k):
            if f["id"] == "C5E10-QA-V1":
                raise RuntimeError("jugement d'épreuve en panne")
            return vrai_juger(f, *a, **k)
        B.juger, sys.argv = juger_en_panne, ["JUGE_DES_STRATEGIES.py", "."]
        tampon = io.StringIO()
        try:
            with contextlib.redirect_stdout(tampon):
                code_d = B.main()
        finally:
            B.juger, sys.argv = vrai_juger, vrai_argv
        out_d = tampon.getvalue()
        vu["jugement en panne : EN ÉCHEC, la suivante jugée, code 1"] = (
            code_d == 1
            and re.search(r"=== C5E10-QA-V1 .*?EN ÉCHEC \(ce n'est pas un refus\) : RuntimeError", out_d, re.S) is not None
            and re.search(r"=== C5E10-OBS-V1 [^\n]*\n(?:[^\n]*\n){0,3}?\s+\d+ operations", out_d) is not None)
        code, out = lancer(copie, J8, ".", "--strategie", "EPREUVE-SANS-SIGNAL")
        vu["juge à 8 critères : code 2, motif"] = code == 2 and "aucun signal nommé" in out
        comb = os.path.join(tempfile.mkdtemp(prefix="comb_"), "COMBINATOIRE_EPREUVE-SANS-SIGNAL_E01.csv")
        with open(comb, "w", encoding="utf-8", newline="") as h:
            w = csv.writer(h)
            w.writerow(["id_version", "strategie", "essai", "tp", "sl", "horizon", "univers", "versions_dans_l_essai",
                        "version_de_la_fiche"])
            w.writerow(["EPREUVE-SANS-SIGNAL-E01-0001", "EPREUVE-SANS-SIGNAL", "E01", "0.04", "0.025", "20",
                        sans["univers"], "1", "OUI"])
        sortie = comb.replace("COMBINATOIRE", "RESULTATS")
        code, out = lancer(copie, JOUER, ".", comb, sortie)
        vu["moulinette : code 1, rien écrit"] = code == 1 and not os.path.exists(sortie) and "ARRÊT" in out
        shutil.rmtree(os.path.dirname(comb), ignore_errors=True)
        try:
            B.jouer(dict(qa), cours, mnemo, B.charger_module(C5, "c5_nu"), pos)
            vu["jouer refuse un module"] = False
        except TypeError as e:
            vu["jouer refuse un module"] = "signal_de_la_fiche" in str(e)
        return all(vu.values()), " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items())
    def e6_puis_ranger():
        # les modules d'épreuve sont retirés même si E6 lève : E7 lit tous les programmes, et l'un d'eux n'est
        # volontairement pas du Python lisible
        try:
            return e6()
        finally:
            for chemin_m in modules:
                if os.path.exists(os.path.join(copie, chemin_m)):
                    os.remove(os.path.join(copie, chemin_m))
    un("E6 les trois programmes refusent une fiche sans signal ; jouer refuse un module", e6_puis_ranger)

    # ── E7 propriété du code ───────────────────────────────────────────────────────────────────────────────────────
    def e7():
        cles = set(B.COLONNES_DU_SIGNAL) | {"_fonction_signal"}
        foyers = []          # les fichiers qui définissent la lecture unique
        lectures, sans_lecture = [], []
        for p in sorted(glob.glob("programmes/*.py")):
            arbre = ast.parse(open(p, encoding="utf-8").read())
            noms_def = {n.name for n in ast.walk(arbre) if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
            foyer = {"SignalNomme", "signal_de_la_fiche", "manques_du_signal"} <= noms_def
            if foyer:
                foyers.append(p)
            permis = set()
            if foyer:
                for n in ast.walk(arbre):
                    if isinstance(n, ast.FunctionDef) and n.name in ("signal_de_la_fiche", "manques_du_signal"):
                        permis |= {id(x) for x in ast.walk(n)}
            appelle_jouer = appelle_lecture = False
            for n in ast.walk(arbre):
                cle = None
                if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant) and n.slice.value in cles:
                    cle = n.slice.value
                elif isinstance(n, ast.Call):
                    nom = n.func.attr if isinstance(n.func, ast.Attribute) else getattr(n.func, "id", None)
                    # l'appel de `jouer` DU JUGE : par un attribut (`J.jouer`, `banc.jouer`), ou par son nom nu dans un
                    # programme qui ne définit pas lui-même de fonction `jouer` (CERTIFIER_LA_VERSION et
                    # EPREUVES_DU_GARDE_FOU ont chacun la leur, sans rapport)
                    if nom == "jouer" and (isinstance(n.func, ast.Attribute) or "jouer" not in noms_def):
                        appelle_jouer = True
                    if nom == "signal_de_la_fiche":
                        appelle_lecture = True
                    if nom in ("get", "setdefault", "pop", "getattr") and any(
                            isinstance(a, ast.Constant) and a.value in cles for a in n.args):
                        cle = next(a.value for a in n.args if isinstance(a, ast.Constant) and a.value in cles)
                    for k in n.keywords:
                        if k.arg in cles:
                            cle = k.arg
                if cle and id(n) not in permis:
                    lectures.append("%s:%d %s" % (p, n.lineno, cle))
            if appelle_jouer and not appelle_lecture and not foyer:
                sans_lecture.append(p)
        vu = {"une seule lecture définie": len(foyers) == 1,
              "aucune lecture ailleurs": not lectures,
              "qui joue lit la fiche": not sans_lecture}
        return all(vu.values()), "foyer %s · lectures hors foyer %s · appellent jouer sans lire %s · %s" % (
            foyers, lectures[:4], sans_lecture, " · ".join("%s %s" % (k, "oui" if v else "NON") for k, v in vu.items()))
    un("E7 propriété : les colonnes du signal ne se lisent qu'à un endroit", e7)
    return res


def preparer(depot, sab):
    """Copie le dépôt et y applique un sabotage.

    ① RÔLE — Donner à chaque sabotage sa copie, pour que rien ne touche au dépôt.
    ② CONTEXTE D'APPEL — Le programme principal, une fois par sabotage joué.
    ③ ENTRÉE — `depot` : la racine · `sab` : le nom du sabotage.
    ④ CONDITIONS D'ENTRÉE — Chaque cible du sabotage existe UNE fois dans son fichier.
    ⑤ SORTIE — DEUX valeurs : le dossier temporaire et la racine de la copie. [rend: 2]
    ⑥ TRAITEMENT — ① copier sans .git, etudes, caches · ② remplacer chaque cible.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une cible introuvable ne sabote rien : elle lève au lieu de passer pour un sabotage qui mord.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit un dossier temporaire.
    ⑪ TERMINAISON — Rend la main, ou lève AssertionError. [sort: non]
    """
    d = tempfile.mkdtemp(prefix="signal_nomme_")
    r = os.path.join(d, "r")
    shutil.copytree(depot, r, ignore=shutil.ignore_patterns(".git", "etudes", "__pycache__", "_site_travail"))
    for f, a, b in SABOTAGES[sab]:
        p = os.path.join(r, f)
        t = open(p, encoding="utf-8").read()
        assert t.count(a) == 1, "%s : cible trouvée %d fois dans %s : %r" % (sab, t.count(a), f, a[:60])
        open(p, "w", encoding="utf-8").write(t.replace(a, b))
    return d, r


if len(sys.argv) > 2 and sys.argv[1] == "--cas":
    resultats = cas(os.path.abspath(sys.argv[2]))
    for nom, ok, detail in resultats:
        print(("  ok    " if ok else "  ÉCHEC ") + nom + " — " + detail)
    # LE MARQUEUR DE FIN : sans lui, une épreuve interrompue (sortie silencieuse) ne passe ni pour verte ni pour mordue
    print("FIN DES CAS : %d" % len(resultats))
    sys.exit(0 if all(ok for _, ok, _ in resultats) else 1)

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
if not _args:
    print(__doc__.split("① RÔLE")[0])
    sys.exit(2)
DEPOT = os.path.abspath(_args[0])
_choix = list(SABOTAGES) if "--saboter" in sys.argv else [_args[1]] if len(_args) > 1 else ["Z0"]
_faute = False
for sab in _choix:
    try:
        d, r = preparer(DEPOT, sab)
    except AssertionError as e:
        print("== %s : CIBLE INTROUVABLE — %s" % (sab, e))
        sys.exit(2)
    try:
        code, out = lancer(r, os.path.abspath(__file__), "--cas", r, delai=1800)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    echecs = [l.strip()[len("ÉCHEC "):].split(" — ")[0] for l in out.splitlines() if l.strip().startswith("ÉCHEC")]
    if sab == "Z0":
        bon = code == 0 and not echecs and "FIN DES CAS : %d" % NOMBRE_DE_CAS in out
        print("== Z0 dépôt tel quel : %s" % ("tout vert" if bon else "ROUGE (code %d)" % code))
        print("\n".join(l for l in out.splitlines() if l.strip()))
    else:
        bon = code == 1 and bool(echecs) and "FIN DES CAS : %d" % NOMBRE_DE_CAS in out
        print("== %s : %s" % (sab, ("mord (" + " · ".join(echecs) + ")") if bon else
                                    "NE MORD PAS (code %d) %s" % (code, out.strip()[-300:])))
    _faute = _faute or not bon
print("VERDICT :", "tout est conforme" if not _faute else "ECHEC — voir ci-dessus")
sys.exit(1 if _faute else 0)
