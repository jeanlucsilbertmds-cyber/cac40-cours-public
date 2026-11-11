#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_SIGNAL_RSI_REBOND — Mer 11-11-2026 16h34 (Paris) · corrigé le Mer 11-11-2026 17h56 et 18h06 (Paris)
EN ESSAI · Rôle : éprouver `programmes/MODULE_SIGNAL_RSI_REBOND.py` (signal de IND-001-RETEST), et prouver que
l'épreuve a des dents. SIMULATION UNIQUEMENT : aucun ordre réel.
Quand l'appeler : à chaque changement du module ou de `rsi_wilder` du module RSI(2).

ÉCRIT PAR UN AGENT DU DÉROULÉ DU 11-11-2026 (branche locale deroule-ind001) : corrigé après un relecteur neuf ; NON
VALIDÉ.

USAGE
    python3 tests/EPREUVES_DU_SIGNAL_RSI_REBOND_Mer_11-11-2026.py <racine>             # les épreuves
    python3 tests/EPREUVES_DU_SIGNAL_RSI_REBOND_Mer_11-11-2026.py <racine> --saboter   # + chaque sabotage doit rougir

LES ÉPREUVES (réglages de la fiche : période 14, seuil 30, chauffe 100, sauf mention)
  E1 cas à la main, chauffe 0 : clôtures 10, 9, 8, 9, période 2 → RSI None, None, 0, 50 : au seuil 30, un signal au
     rang 3 ; avec une chauffe de 4, aucun ; avec une chauffe de 3, le rang 3.
  E1' SECOND SEUIL (second relecteur, N1) : clôtures 10, 9, 8, 9, 10, période 2 → RSI None, None, 0, 50, 75 ; au
     seuil 60 → un signal au rang 4 (veille 50, entre 30 et 60). Une veille comparée à 30 écrit en dur au lieu du
     seuil (`rv < 30`, `rv <= 30`) n'y voit pas de signal.
  E1b ÉGALITÉ LE JOUR, deux seuils : 10, 9, 8, 9 au seuil 50 (jour 50 pile) et 10, 9, 8, 9, 10 au seuil 75 (jour 75
     pile) → AUCUN signal (strictement au-dessus).
  E1c ÉGALITÉ LA VEILLE, deux seuils, différents de 30 : 10, 9, 8, 9, 10 au seuil 50 (veille 50 pile, jour 75) et
     10, 9, 8, 9, 10, 11 au seuil 75 (veille 75 pile, jour 87,5) → AUCUN signal (strictement en dessous la veille).
  E1d ÉGALITÉ LA VEILLE AU SEUIL 30 : 10, 13, 6, 7, période 2 → RSI None, None, 30 pile, 41,67 → AUCUN signal.
  E2 VRAIE LIGNE du fichier maître `donnees/cours_maitre.csv`, lue par le lecteur unique du juge : VINCI. Le RSI
     RENDU PAR LE MODULE au signal du 2025-04-08 vaut 29,776 la veille et 37,820 le jour (arrondis au millième) ;
     ni le 2025-04-07 ni le 2025-04-09 ne sont signalés.
  E3 tous les signaux du module sur VINCI = les franchissements stricts, hors chauffe, trouvés par une seconde
     écriture du RSI de Wilder, indépendante du module.
  E4 PAS D'AVENIR, PARTOUT : pour CHAQUE valeur du maître et CHAQUE séance J, la série coupée à J dit, pour J, la même
     chose que la série entière.
  E5 réglages mal formés refusés (période 0, période « 14 » en texte, seuil 100, seuil vrai/faux, chauffe -1).
  E5b UNE CLÔTURE NaN est refusée bruyamment (ValueError), jamais une liste vide en silence (R-734).
  E5c UNE SÉRIE EN ORDRE INVERSE (et une date en double) est refusée.
  E5d UNE CLÔTURE None, ABSENTE, VIDE ou « 1,5 » est refusée par ValueError dont le message porte le rang et la date.
  E6 le juge accepte une fiche qui nomme ce module (`signal_de_la_fiche`), la sortie a la forme attendue
     (`forme_du_signal`), la mémoire déclarée vaut 615 à (14, 30, 100) et 701 à (14, 30, 700).
LES SABOTAGES (--saboter) — chacun modifie une copie du module (et du module RSI(2) copié à côté) ; au moins une
épreuve doit rougir :
  S1 franchissement inversé · S2 l'état au lieu du franchissement · S3 ligne « module de signal » retirée ·
  S4 rang décalé d'une séance · S5 chauffe ignorée · S6 NaN laissé passer · S7 ordre des dates non contrôlé ·
  N1a veille comparée à 30 écrit en dur (`rv < 30`) · N1b `rv <= 30` (la règle refusée par Jean-Luc) ·
  S8 clôture illisible non rattrapée · M2 « au seuil ou au-dessus » le jour (`r >= seuil`, l'ancienne règle) · M3 « au seuil ou en dessous » la veille
  (`rv <= seuil`) · M5 triche du relecteur : écarter le signal si la clôture J+5 est sous 95 % de celle de J.
CODE DE SORTIE : 0 si tout est vert (et, avec --saboter, si chaque sabotage a rougi) ; 1 sinon ; 2 sur arguments.
"""
import csv
import importlib.util
import math
import os
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
MODULE = os.path.join("programmes", "MODULE_SIGNAL_RSI_REBOND.py")
REGLAGES = {"periode": 14, "seuil": 30, "chauffe": 100}
_JUGE = {}


def charger(chemin, nom):
    """Charge un fichier Python par son chemin et rend le module.

    ① RÔLE — Charger le module éprouvé (vrai ou saboté) et le juge, sans passer par `import`.
    ② CONTEXTE D'APPEL — `epreuves`, `juge_et_cours`.
    ③ ENTRÉE — `chemin` : le fichier · `nom` : le nom donné au module chargé.
    ④ CONDITIONS D'ENTRÉE — Le fichier existe.
    ⑤ SORTIE — UNE valeur : le module. [rend: 1]
    ⑥ TRAITEMENT — `spec_from_file_location`, puis exécution du fichier.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un module saboté vit dans un dossier temporaire : il se charge par son chemin.
    ⑨ CE QUI CLOCHE — Exécute le fichier : un module qui ne revient pas bloquerait l'épreuve.
    ⑩ EFFET — Exécute le fichier chargé.
    ⑪ TERMINAISON — Rend la main, ou lève l'erreur du chargement ; l'exécution du fichier peut ne pas revenir. [sort: non]
    """
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def juge_et_cours(racine):
    """Rend le juge chargé et les séries du fichier maître lues par le lecteur unique (une seule fois par lancement).

    ① RÔLE — Donner aux épreuves les séries que le juge donnerait au signal.
    ② CONTEXTE D'APPEL — `epreuves`, `epreuves_s3`.
    ③ ENTRÉE — `racine` : la racine du dépôt (cours, référentiel, juge, lecteur).
    ④ CONDITIONS D'ENTRÉE — `donnees/cours_maitre.csv` et le référentiel existent sous la racine.
    ⑤ SORTIE — DEUX valeurs : le module du juge ; le dictionnaire clé de valeur → séances triées. [rend: 2]
    ⑥ TRAITEMENT — ① charger le juge · ② lire la table des mnémoniques · ③ lire le maître par `lire_par_le_lecteur` ·
      ④ garder en mémoire pour les appels suivants.
    ⑦ UNITÉ — Prix en euros, dates AAAA-MM-JJ.
    ⑧ POURQUOI — Le lecteur unique réunit les graphies d'une même valeur (« BUREAU VERITAS » / « BUREAU_VERITAS ») ;
      une lecture brute du CSV couperait ces séries en deux.
    ⑨ CE QUI CLOCHE — Ne lit QUE le maître (2024-2026) : rien sur les 20 ans, voulu (R-505, regard unique).
    ⑩ EFFET — Lit des fichiers ; n'écrit rien.
    ⑪ TERMINAISON — Rend la main, ou lève l'erreur du lecteur. [sort: non]
    """
    if racine not in _JUGE:
        sys.path.insert(0, os.path.join(racine, "programmes"))
        J = charger(os.path.join(racine, "programmes", "JUGE_DES_STRATEGIES.py"), "juge_pour_epreuve_rsi_rebond")
        mnemo = J.table_mnemoniques(J.trouver(racine, "REFERENTIEL_VALEURS"))
        cours, _lecture = J.lire_par_le_lecteur(racine, "donnees/cours_maitre.csv", mnemo)
        _JUGE[racine] = (J, cours)
    return _JUGE[racine]


def rsi_seconde_ecriture(c, p):
    """RSI de Wilder recalculé sans le module : la seconde écriture de l'épreuve (volontairement naïve).

    ① RÔLE — Donner une référence indépendante du code éprouvé.
    ② CONTEXTE D'APPEL — `epreuves`, E3.
    ③ ENTRÉE — `c` : clôtures dans l'ordre · `p` : période.
    ④ CONDITIONS D'ENTRÉE — `p` entier ≥ 1.
    ⑤ SORTIE — UNE valeur : liste de même longueur, None tant que le RSI n'est pas défini. [rend: 1]
    ⑥ TRAITEMENT — Moyennes simples des p premières hausses et baisses, puis lissage (ancienne × (p − 1) + jour) / p.
    ⑦ UNITÉ — RSI de 0 à 100.
    ⑧ POURQUOI — Comparer le module à lui-même ne prouverait rien.
    ⑨ CE QUI CLOCHE — Même méthode que le module (Wilder) : une erreur de conception commune ne serait pas vue ; E2
      ancre le module sur deux chiffres écrits en dur.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; boucle bornée. [sort: non]
    """
    out = [None] * len(c)
    if len(c) <= p:
        return out
    g = [max(c[k] - c[k - 1], 0.0) for k in range(1, len(c))]
    l = [max(c[k - 1] - c[k], 0.0) for k in range(1, len(c))]
    ag, al = sum(g[:p]) / p, sum(l[:p]) / p
    for k in range(p, len(c)):
        if k > p:
            ag = (ag * (p - 1) + g[k - 1]) / p
            al = (al * (p - 1) + l[k - 1]) / p
        out[k] = None if (ag == 0 and al == 0) else (100.0 if al == 0 else 100 - 100 / (1 + ag / al))
    return out


def jours(dates, liste):
    """Rend les dates des rangs signalés. ①-⑪ : aide d'affichage triviale — ① traduire rangs en dates ; ② `epreuves` ;
    ③ dates, sortie du signal ; ④ rangs valides ; ⑤ UNE liste [rend: 1] ; ⑥ lecture ; ⑦ dates ; ⑧ lisibilité ; ⑨ — ;
    ⑩ aucun ; ⑪ rend la main [sort: non]."""
    return [dates[x["i"]] for x in liste]


def epreuves(racine, chemin_module, racine_signal=None, rapide=False):
    """Joue E1 à E6 sur le module donné ; rend la liste des (nom, vert, détail).

    ① RÔLE — Le cœur de l'épreuve.
    ② CONTEXTE D'APPEL — `main`, une fois sur le vrai module, puis une fois par sabotage.
    ③ ENTRÉE — `racine` : la racine des cours et du juge · `chemin_module` : le module éprouvé · `racine_signal` : la
      racine sous laquelle le juge cherche le module (celle du sabotage), `racine` par défaut · `rapide` : arrêter E4
      au premier écart (sabotages).
    ④ CONDITIONS D'ENTRÉE — Le module RSI(2) est à côté du module éprouvé.
    ⑤ SORTIE — UNE valeur : la liste des (nom, vert, détail). [rend: 1]
    ⑥ TRAITEMENT — E1 à E6, chacune rattrapant ses propres erreurs pour que les suivantes tournent.
    ⑦ UNITÉ — RSI, séances, dates.
    ⑧ POURQUOI — Voir l'en-tête : chaque épreuve vise un défaut nommé par le relecteur ou une décision de Jean-Luc.
    ⑨ CE QUI CLOCHE — E4 coupe les séries depuis leur origine : il ne vérifie pas la mémoire déclarée (c'est l'épreuve
      d'arrivée des signaux qui le fait, non lancée ici).
    ⑩ EFFET — Charge le module éprouvé.
    ⑪ TERMINAISON — Rend la main ; E4 fait environ 29 000 appels bornés. [sort: non]
    """
    res = []
    try:
        m = charger(chemin_module, "rsi_rebond_eprouve")
    except Exception as e:
        return [("CHARGEMENT", False, "%s: %s" % (type(e).__name__, e))]

    def main_(cl):
        return [{"date": "2024-01-%02d" % (k + 1), "close": x} for k, x in enumerate(cl)]
    try:
        a = [x["i"] for x in m.signaux_rsi_rebond(main_((10, 9, 8, 9)), periode=2, seuil=30, chauffe=0)]
        b = [x["i"] for x in m.signaux_rsi_rebond(main_((10, 9, 8, 9)), periode=2, seuil=30, chauffe=4)]
        c = [x["i"] for x in m.signaux_rsi_rebond(main_((10, 9, 8, 9)), periode=2, seuil=30, chauffe=3)]
        res.append(("E1 cas à la main, chauffe", (a, b, c) == ([3], [], [3]), "chauffe 0:%s 4:%s 3:%s" % (a, b, c)))
    except Exception as e:
        res.append(("E1 cas à la main, chauffe", False, repr(e)))
    try:
        o = [x["i"] for x in m.signaux_rsi_rebond(main_((10, 9, 8, 9, 10)), periode=2, seuil=60, chauffe=0)]
        res.append(("E1' second seuil (60, veille 50)", o == [4], repr(o)))
    except Exception as e:
        res.append(("E1' second seuil (60, veille 50)", False, repr(e)))
    for nom, cl, seuil in (("E1b égalité le jour (50 pile)", (10, 9, 8, 9), 50),
                           ("E1b égalité le jour (75 pile)", (10, 9, 8, 9, 10), 75),
                           ("E1c égalité la veille (50 pile)", (10, 9, 8, 9, 10), 50),
                           ("E1c égalité la veille (75 pile)", (10, 9, 8, 9, 10, 11), 75),
                           ("E1d égalité la veille (30 pile)", (10, 13, 6, 7), 30)):
        try:
            o = m.signaux_rsi_rebond(main_(cl), periode=2, seuil=seuil, chauffe=0)
            res.append((nom, o == [], repr(o)))
        except Exception as e:
            res.append((nom, False, repr(e)))
    J, cours = juge_et_cours(racine)
    cle = [k for k in cours if "VINCI" in k.upper()][0]
    serie = cours[cle]
    dates = [b["date"] for b in serie]
    try:
        o = m.signaux_rsi_rebond(serie, **REGLAGES)
        s8 = [x for x in o if dates[x["i"]] == "2025-04-08"]
        ok2 = (len(s8) == 1 and round(s8[0]["rsi_veille"], 3) == 29.776 and round(s8[0]["rsi"], 3) == 37.820
               and "2025-04-07" not in jours(dates, o) and "2025-04-09" not in jours(dates, o))
        res.append(("E2 RSI du module, VINCI 2025-04-08", ok2, repr(s8)))
        ref = rsi_seconde_ecriture([b["close"] for b in serie], 14)
        attendus = [dates[k] for k in range(max(1, REGLAGES["chauffe"]), len(ref)) if ref[k] is not None
                    and ref[k - 1] is not None and ref[k - 1] < 30 < ref[k]]
        res.append(("E3 signaux VINCI = seconde écriture", jours(dates, o) == attendus,
                    "module %d / seconde écriture %d" % (len(o), len(attendus))))
    except Exception as e:
        res.append(("E2-E3", False, repr(e)))
    try:
        ecarts, appels = [], 0
        for v in sorted(cours):
            s = cours[v]
            pleine = {x["i"] for x in m.signaux_rsi_rebond(s, **REGLAGES)}
            for j in range(len(s)):
                appels += 1
                coupee = {x["i"] for x in m.signaux_rsi_rebond(s[:j + 1], **REGLAGES)}
                if (j in coupee) != (j in pleine):
                    ecarts.append((v, s[j]["date"], "coupée" if j in coupee else "entière"))
                    if rapide:
                        break
            if rapide and ecarts:
                break
        res.append(("E4 pas d'avenir, chaque valeur, chaque séance", not ecarts,
                    "%d valeurs, %d coupes, %d écart(s) %s" % (len(cours), appels, len(ecarts), ecarts[:2])))
    except Exception as e:
        res.append(("E4 pas d'avenir", False, repr(e)))
    refus = 0
    for kw in ({"periode": 0, "seuil": 30, "chauffe": 100}, {"periode": "14", "seuil": 30, "chauffe": 100},
               {"periode": 14, "seuil": 100, "chauffe": 100}, {"periode": 14, "seuil": True, "chauffe": 100},
               {"periode": 14, "seuil": 30, "chauffe": -1}):
        try:
            m.signaux_rsi_rebond(serie, **kw)
        except ValueError:
            refus += 1
        except Exception:
            pass
    res.append(("E5 réglages mal formés refusés", refus == 5, "%d/5 refus" % refus))
    nan = [dict(b) for b in serie]
    nan[200]["close"] = float("nan")
    try:
        o = m.signaux_rsi_rebond(nan, **REGLAGES)
        res.append(("E5b NaN refusé bruyamment", False, "rendu sans erreur : %d signaux" % len(o)))
    except ValueError as e:
        res.append(("E5b NaN refusé bruyamment", True, str(e)))
    except Exception as e:
        res.append(("E5b NaN refusé bruyamment", False, repr(e)))
    infini = [dict(b) for b in serie]
    infini[200]["close"] = float("inf")
    try:
        o = m.signaux_rsi_rebond(infini, **REGLAGES)
        res.append(("E5b infini refusé bruyamment", False, "rendu sans erreur : %d signaux" % len(o)))
    except ValueError as e:
        res.append(("E5b infini refusé bruyamment", "rang 200" in str(e), str(e)))
    except Exception as e:
        res.append(("E5b infini refusé bruyamment", False, repr(e)))
    import datetime as _dt
    for date_lue in (None, "", _dt.date(2025, 1, 6), "2025-1-6"):
        s = [dict(b) for b in serie]
        s[250]["date"] = date_lue
        nom = "E5f date %r refusée par ValueError avec le rang" % (date_lue,)
        try:
            m.signaux_rsi_rebond(s, **REGLAGES)
            res.append((nom, False, "accepté"))
        except ValueError as e:
            res.append((nom, "rang 250" in str(e), str(e)))
        except Exception as e:
            res.append((nom, False, "%s: %s" % (type(e).__name__, e)))
    plat = [{"date": "2025-01-%02d" % (k + 1), "close": c} for k, c in enumerate((10, 10, 10, 10, 10, 11, 12))]
    try:
        o = m.signaux_rsi_rebond(plat, periode=2, seuil=30, chauffe=1)
        res.append(("E7 série plate puis hausse : aucun signal (veille indéfinie)", o == [], "%d signal(s) %s" % (len(o), o[:1])))
    except Exception as e:
        res.append(("E7 série plate puis hausse : aucun signal", False, "%s: %s" % (type(e).__name__, e)))
    for nom, s in (("E5c série inversée refusée", list(reversed(serie))),
                   ("E5c date en double refusée", serie[:300] + serie[299:])):
        try:
            m.signaux_rsi_rebond(s, **REGLAGES)
            res.append((nom, False, "accepté"))
        except ValueError as e:
            res.append((nom, True, str(e)))
        except Exception as e:
            res.append((nom, False, repr(e)))
    for valeur_lue in (None, "ABSENTE", "", "1,5"):
        s = [dict(b) for b in serie]
        if valeur_lue == "ABSENTE":
            del s[150]["close"]
        else:
            s[150]["close"] = valeur_lue
        nom = "E5d clôture %r refusée avec rang et date" % (valeur_lue,)
        try:
            m.signaux_rsi_rebond(s, **REGLAGES)
            res.append((nom, False, "accepté"))
        except ValueError as e:
            res.append((nom, "rang 150" in str(e) and s[150]["date"] in str(e), str(e)))
        except Exception as e:
            res.append((nom, False, "%s: %s" % (type(e).__name__, e)))
    try:
        rs = racine_signal or racine
        J._MODULES_DE_SIGNAL.clear()
        fiche = {"id": "EPREUVE", "module_signal": os.path.relpath(chemin_module, rs),
                 "fonction_signal": "signaux_rsi_rebond", "reglages_signal": '{"periode": 14, "seuil": 30, "chauffe": 100}'}
        sig = J.signal_de_la_fiche(rs, fiche)
        sortie = sig(serie)
        mem = (m.memoire_signaux_rsi_rebond(14, 30, 100), m.memoire_signaux_rsi_rebond(14, 30, 700))
        ok6 = J.forme_du_signal(sortie, len(serie)) is None and mem == (615, 701)
        res.append(("E6 accepté par le juge, forme et mémoire", ok6, "%d signaux, mémoires %s" % (len(sortie), mem)))
    except Exception as e:
        res.append(("E6 accepté par le juge, forme et mémoire", False, "%s: %s" % (type(e).__name__, e)))
    return res


SABOTAGES = (
    ("S1 franchissement inversé", "if rv < seuil and r > seuil:", "if r < seuil and rv > seuil:"),
    ("S2 l'état au lieu du franchissement", "if rv < seuil and r > seuil:", "if r > seuil:"),
    ("S3 ligne « module de signal » retirée", "EN ESSAI · module de signal · ", "EN ESSAI · module · "),
    ("S4 rang décalé d'une séance", 'out.append({"i": i, ', 'out.append({"i": min(i + 1, len(clotures) - 1), '),
    ("S5 chauffe ignorée", "range(max(1, chauffe), len(clotures))", "range(1, len(clotures))"),
    ("S6 NaN laissé passer", "if not math.isfinite(c):", "if False:"),
    ("S7 ordre des dates non contrôlé", "if precedente is not None and not d > precedente:", "if False:"),
    ("N1a veille comparée à 30 en dur", "if rv < seuil and r > seuil:", "if rv < 30 and r > seuil:"),
    ("N1b veille <= 30 en dur", "if rv < seuil and r > seuil:", "if rv <= 30 and r > seuil:"),
    ("S8 clôture illisible non rattrapée", "except (KeyError, TypeError, ValueError) as e:", "except ZeroDivisionError as e:"),
    ("S9 infini laissé passer (relecture Cowork RB-1, C1)", "if not math.isfinite(c):", "if math.isnan(c):"),
    ("S10 date non contrôlée (relecture Cowork RB-1, C2)", 'if not isinstance(d, str) or not re.fullmatch(r"\\d{4}-\\d{2}-\\d{2}", d):', "if False:"),
    ("S11 veille indéfinie comptée 0 (relecture Cowork RB-1, C7)", "        if r is None or rv is None:\n            continue\n",
     "        if r is None:\n            continue\n        rv = 0 if rv is None else rv\n"),
    ("M2 au seuil ou au-dessus le jour", "if rv < seuil and r > seuil:", "if rv < seuil and r >= seuil:"),
    ("M3 au seuil ou en dessous la veille", "if rv < seuil and r > seuil:", "if rv <= seuil and r > seuil:"),
    ("M5 triche J+5 sous 95 %", "            continue\n        if rv < seuil and r > seuil:",
     "            continue\n        if i + 5 < len(clotures) and clotures[i + 5] < 0.95 * clotures[i]:\n"
     "            continue\n        if rv < seuil and r > seuil:"),
)


def afficher(res):
    """Affiche les résultats et rend vrai si tout est vert.

    ① RÔLE — Une ligne par épreuve. ② CONTEXTE D'APPEL — `main`. ③ ENTRÉE — la liste des (nom, vert, détail).
    ④ CONDITIONS D'ENTRÉE — —. ⑤ SORTIE — UNE valeur : vrai si tout est vert [rend: 1]. ⑥ TRAITEMENT — afficher,
    puis `all`. ⑦ UNITÉ — —. ⑧ POURQUOI — lisible sur téléphone. ⑨ CE QUI CLOCHE — détails coupés à 150 signes.
    ⑩ EFFET — écrit à l'écran. ⑪ TERMINAISON — rend la main [sort: non].
    """
    for nom, ok, det in res:
        print("  %s %-46s %s" % ("VERT " if ok else "ROUGE", nom, str(det)[:150]))
    return all(ok for _, ok, _ in res)


def epreuves_s3(racine, d):
    """Pour S3 : le juge doit refuser le module non déclaré, présenté sous la racine du sabotage.

    ① RÔLE — Mordre S3 par la bonne raison. ② CONTEXTE D'APPEL — `main`, sabotage S3. ③ ENTRÉE — `racine` : celle du
    juge · `d` : la racine du sabotage. ④ CONDITIONS D'ENTRÉE — le module saboté est sous `d/programmes`.
    ⑤ SORTIE — UNE liste d'un (nom, vert, détail) [rend: 1]. ⑥ TRAITEMENT — `signal_de_la_fiche(d, fiche)` ; un refus
    rend « rouge » (le sabotage est vu). ⑦ UNITÉ — —. ⑧ POURQUOI — le juge lit la ligne de déclaration sans exécuter.
    ⑨ CE QUI CLOCHE — —. ⑩ EFFET — lit le module saboté. ⑪ TERMINAISON — rend la main [sort: non].
    """
    J, _ = juge_et_cours(racine)
    J._MODULES_DE_SIGNAL.clear()
    fiche = {"id": "EPREUVE", "module_signal": "programmes/MODULE_SIGNAL_RSI_REBOND.py",
             "fonction_signal": "signaux_rsi_rebond", "reglages_signal": '{"periode": 14, "seuil": 30, "chauffe": 100}'}
    try:
        J.signal_de_la_fiche(d, fiche)
        return [("E6 module non déclaré accepté par le juge", True, "accepté")]
    except ValueError as e:
        return [("E6 le juge refuse le module non déclaré", False, str(e)[:120])]


def main():
    """Lance les épreuves, puis les sabotages si demandé ; rend le code de sortie.

    ① RÔLE — Programme principal. ② CONTEXTE D'APPEL — la ligne de commande. ③ ENTRÉE — `<racine>` et `--saboter`.
    ④ CONDITIONS D'ENTRÉE — une racine de dépôt (de préférence un clone neuf). ⑤ SORTIE — UNE valeur : le code 0, 1
    ou 2 [rend: 1]. ⑥ TRAITEMENT — ① épreuves sur le vrai module · ② avec --saboter, pour chaque sabotage : copier
    les deux modules dans un dossier temporaire, appliquer le remplacement (cible unique exigée), rejouer, exiger au
    moins un rouge, effacer le dossier. ⑦ UNITÉ — —. ⑧ POURQUOI — une épreuve qui reste verte quand on retire ce
    qu'elle teste n'est pas une preuve. ⑨ CE QUI CLOCHE — une cible de sabotage introuvable compte comme un sabotage
    qui ne mord pas (rouge). ⑩ EFFET — écrit et efface des dossiers temporaires ; affiche. ⑪ TERMINAISON — rend le
    code ; aucun appel non borné hors du chargement des modules [sort: oui].
    """
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 2
    racine = os.path.abspath(args[0])
    print("ÉPREUVES DU SIGNAL RSI REBOND — module %s" % MODULE)
    tout_vert = afficher(epreuves(racine, os.path.join(racine, MODULE)))
    print("Z0 :", "TOUT VERT" if tout_vert else "ROUGE")
    if "--saboter" not in sys.argv:
        return 0 if tout_vert else 1
    source = open(os.path.join(racine, MODULE), encoding="utf-8").read()
    mordent = 0
    for nom, avant, apres in SABOTAGES:
        if source.count(avant) != 1:
            print("SABOTAGE %-40s cible introuvable ou multiple (%d) — NE MORD PAS" % (nom, source.count(avant)))
            continue
        d = tempfile.mkdtemp(prefix="sabotage_rsi_rebond_")
        try:
            os.makedirs(os.path.join(d, "programmes"))
            shutil.copy(os.path.join(racine, "programmes", "MODULE_SIGNAL_RSI2_CONNORS.py"), os.path.join(d, "programmes"))
            p = os.path.join(d, "programmes", "MODULE_SIGNAL_RSI_REBOND.py")
            open(p, "w", encoding="utf-8").write(source.replace(avant, apres))
            res = epreuves_s3(racine, d) if nom.startswith("S3") else epreuves(racine, p, racine_signal=d, rapide=True)
            rouges = [n for n, ok, _ in res if not ok]
            print("SABOTAGE %-40s %s" % (nom, "MORD (%s)" % ", ".join(rouges) if rouges else "NE MORD PAS"))
            mordent += bool(rouges)
        finally:
            shutil.rmtree(d, ignore_errors=True)
    print("SABOTAGES : %d/%d mordent" % (mordent, len(SABOTAGES)))
    return 0 if (tout_vert and mordent == len(SABOTAGES)) else 1


if __name__ == "__main__":
    sys.exit(main())
