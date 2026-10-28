#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DU_MESSAGE_DU_SOIR — Mer 30-09-2026 (Paris)
Rôle : prouver que programmes/MESSAGE_DU_SOIR.py dit ce qu'il doit dire à Jean-Luc, et que chaque épreuve a des dents.
Quand l'appeler : avant toute livraison qui touche programmes/MESSAGE_DU_SOIR.py (R-755 ②).

À QUOI ÇA SERT. Le message du soir est le seul endroit où Jean-Luc apprend, chaque soir, ce qu'a fait le circuit de
GitHub (décision de Jean-Luc du 30-09-2026, 17h34-17h42). S'il se tait sur une panne, personne ne la voit.

LES ÉPREUVES, chacune dans un petit dépôt git fabriqué (deux versions du rapport du radar : la veille, puis le jour),
à l'heure FIXÉE du mercredi 30-09-2026 à 20h45 (Paris), posée dans chaque programme lancé (voir JOUR_FIXE) :
E1 soir normal sans ❌ : la première ligne commence par ✅ et dit « rien à signaler », « aucun signal », « 0 position » ;
E1b un ❌ déjà présent la veille : la première ligne commence par ⚠️ et dit « ❌ connu » ;
E2 rapport du radar de la veille seulement : « Circuit du soir NON passé (dernier radar du JJ-MM) », code 2 ;
E3 un signal ENGIE : la première ligne le nomme ;
E4 un ❌ absent la veille : 🚨 et « ❌ nouveau » ;
E5 un ⚠️ absent la veille : la première ligne commence par ⚠️ et dit « ⚠️ nouveau » ;
E6 un ⚠️ dont seule la liste change (« depuis 7 jours : A-1 » puis « depuis 8 jours : A-1, A-2 ») : ✅ ;
E7 le fichier des signaux manque : « Message incomplet », code 1 ;
E8 une copie sans historique git : « veille non relue » en première ligne, rien de « NOUVEAU » ;
E9 un trade clos ce soir écrit sous deux comptabilités, et un plus ancien : « Trades clos ce soir : 1 » ;
E11 séance de bourse précédente dans le fichier des signaux : « Séance du JJ-MM NON lue », code 2 ;
E12 deux valeurs sans la séance : la première ligne le dit ;
E13 rapport coupé (le score annonce 1 ❌, la ligne manque) : « Message incomplet » ;
E14 fichier des signaux valant null : « Message incomplet », code 1, sans plantage ;
E15 dix signaux : la première ligne tient en 200 caractères ;
E16 un échec de plus dans la ligne ❌ du BACKLOG : « ❌ nouveau » ;
E17 fichier des signaux sans « signaux » : « Message incomplet », code 1 ;
E18 fichier des positions avec une colonne hors contrat : « Message incomplet » ;
E19 sans historique git et avec un ❌ : 🚨, jamais « connu » ;
LA CERTIFICATION DE LA NUIT (A-629), jugée par son fruit : chaque passage de la certification fait un commit de l'identité
« certification-publique », même raté ; le message juge le DERNIER. Les heures sont écrites ici à la main, depuis le réveil
« 0 21 * * 1-5 » que E52 épingle dans le gabarit du fabricant (jamais recopiées du programme) :
E40 passage de la nuit (veille ouvrée, 21h30 UT) qui dépose le certificat : rien n'est dit, le détail le date ;
E41 aucun passage : 🚨 « Certification absente (aucun passage) », code 2 ;
E42 dernier passage trois jours ouvrés avant : 🚨 « Certification absente (dernier passage JJ-MM) », code 2 ;
E43 passage de la nuit qui ne dépose que son journal : 🚨 « Certification sans certificat », code 2 ;
E44 lancement manuel à 15h00 la veille, puis nuit qui ne dépose que son journal : 🚨 « sans certificat » ;
E45 bornes : dépôt la veille à 20h59 UT → 🚨 « absente » ; à 21h01 UT → rien ;
E46 identités voisines (« certification-claude », « certification-publique-test ») : elles ne comptent pas, 🚨 ;
E47 passage recopié par un autre committer : illisible, code 1 ; même identité, date d'auteur vieille et date de
    committer fraîche : la date d'auteur fait foi, 🚨 ;
E48 passage daté du lendemain : illisible, code 1 ;
E49 certificat sans ligne « **VERSION … ** » : illisible, code 1 ;
E50 clone superficiel (--depth 1) d'un dépôt dont le dernier passage n'a déposé que son journal : illisible, code 1, et
    jamais « déposé » ;
E51 un lundi soir : passage du vendredi déposé le samedi 03h22 → rien ; dernier passage le vendredi 04h24 → 🚨 ; un soir
    d'heure d'hiver (28-10-2026) : passage de la veille à 21h30 UT → rien ;
E52 le gabarit du fabricant porte le réveil « 0 21 * * 1-5 », un pas « deposer » en « if: always() », et l'identité
    « certification-publique » : si l'un change, les heures de ces épreuves sont à revoir ;
E53 fabricant au réveil changé en « 30 6 * * 1-5 » : passage du jour à 10h00 UT → rien, passage de la veille à 10h00 UT
    → 🚨 (le réveil du matin du jour a eu le temps de finir) ; réveil « 0 21 * * * » : illisible, code 1 ;
E55 réveil « 0 21 * * 1-4 », un lundi : passage du jeudi 21h30 UT → rien (les jours du réveil sont lus) ;
E56 réveil « 45 20 * * 1-5 » : passage la veille à 20h30 UT → 🚨 (la minute est lue) ;
E57 identité où les points de l'adresse sont remplacés : elle ne compte pas, « aucun passage » ;
E58 committer du même nom avec une autre adresse : illisible, code 1 ;
E59 message lancé à 1h00 la nuit qui suit la veille ouvrée, pendant son passage : le passage d'avant suffit, rien n'est dit ;
E60 gabarit sans « timeout-minutes » : délai illisible, code 1 ;
E61 fabricant qui arrête Python à son import : le message n'est pas touché, il ne l'exécute pas ;
E54 copie sans historique git : la certification est dite illisible, code 1 ;
E20 un ❌ nouveau en fin de ligne longue : le détail l'écrit en entier ;
E21 fichier des signaux portant une clé hors contrat : « Message incomplet » ;
E22 un signal portant un champ hors contrat : « Message incomplet » ;
E26 aujourd'hui sans bourse (jour férié du calendrier, ou week-end) et la dernière séance ouvrée lue : aucune alerte de
    séance, « Pas de bourse aujourd'hui », code 0 ;
E27 trois séances de retard : « 3 jour(s) de bourse de retard » ;
E28 calendrier qui ne couvre pas aujourd'hui : « Message incomplet », code 1 ;
E29 calendrier absent de la racine lue mais présent dans le dépôt du programme : lu là, et le détail le dit ;
    absent des deux : « Message incomplet », « Séance attendue : inconnue », aucune « NON lue » devinée ;
E30 calendrier dans la racine lue et dans le dépôt du programme : celui de la racine, et le détail le dit ;
E31 séance lue postérieure à l'attendue : « POSTÉRIEURE », code 2 ;
E32 séance « 2026-02-30 » : c'est le fichier des signaux qui est dit illisible, jamais le calendrier ; bannière « séance ? » ;
E33 rapport du radar de la veille (circuit pas encore passé) et séance de la veille de bourse : « Circuit du soir NON
    passé », mais aucune « Séance … NON lue » (le matin, rien ne manque encore) ;
E34 séance lue un samedi : « pas un jour de bourse », avec le retard compté sans le module, code 2 ;
E35 calendrier qui finit dans 10 ou 29 jours : ⚠️ « Calendrier de la Bourse à relever », code 0 ; dans 31 : rien ;
E36 séance antérieure au début du calendrier : « au moins N jour(s) de bourse de retard », N compté sans le module ;
E37 séance « AAAAMMJJ » : illisible, code 1 ;
E38 circuit pas encore passé, séance deux jours de bourse avant la veille de bourse : « 2 jour(s) » ;
E39 circuit pas encore passé mais séance attendue déjà lue : jamais « POSTÉRIEURE » ;
E10 le chemin réel : le programme lancé sur la racine donnée rend 0, 1 ou 2, et sa ligne « Séance lue : » porte la séance
    du fichier des signaux de cette racine.
LES SABOTAGES : S1 le circuit est toujours dit passé (E2) · S2 tout est nouveau (E1, E6) · S3 les chiffres ne sont
plus retirés (E6) · S4 le code de sortie reste 0 (E2, E7) · S5 les signaux sont ignorés (E3) · S6 tous les trades du
journal sont dits clos ce soir (E9) · S7 chaque comptabilité compte pour un trade (E9) · S8 la séance n'est plus
confrontée au jour (E11) · S9 la bannière n'est plus coupée (E15) · S10 le score n'est plus confronté aux lignes
(E13) · S11 seule l'absence du fichier des signaux est rattrapée (E14) · S12 un ❌ est comparé sur 60 caractères
(E16) · S13 les clés du fichier des signaux ne sont plus confrontées (E17) · S14 le contrat des positions est ignoré
(E18) · S15 un ❌ est dit « connu » sans veille (E19) · S16 un ❌ nouveau est coupé à 160 caractères (E20) · S17
l'enveloppe des signaux n'est plus confrontée au contrat (E21) · S18 chaque signal non plus (E22) · S21 la séance
attendue est le jour même (E26) · S22 le retard n'est plus compté (E27) · S23 un calendrier hors couverture est toléré
(E28) · S24 le calendrier n'est cherché que dans la racine lue (E29) · S25 la veille de bourse ne suffit plus avant le
circuit (E33 ; un samedi ou un dimanche, la veille de bourse et la séance attendue se confondent : ce sabotage n'y est
pas attrapé) · S26 une séance postérieure est tolérée (E31) · S27 une séance hors jour de bourse est tolérée (E34) ·
S28 la séance attendue inconnue est tue (E29) · S29 l'origine du calendrier est tue (E29, E30) · S30 le dépôt du
programme est lu d'abord (E30) · S31 la fin prochaine du calendrier est tue (E35) · S32 une séance illisible est
tolérée (E32) · S33 le retard est compté hors couverture (E36) · S34 « POSTÉRIEURE » jugé sur la veille de bourse
(E39) · S35 seuil de fin du calendrier à 11 jours (E35) · S36 la veille de bourse cherchée trois jours avant (E38) ·
S37 forme de la séance non exigée (E37) · S38 compte faux avant la couverture (E36) · S39 le retard tu quand la séance
tombe un samedi (E34) · S40 une séance impossible affichée comme une date (E32) · S41 la date du radar mal lue (E2).
LA LOGIQUE DU CALENDRIER lui-même (week-ends, fériés, bornes) est éprouvée à part, sur des réponses écrites à la main :
tests/EPREUVES_DU_CALENDRIER_DE_LA_BOURSE_Mer_30-09-2026.py. Ici, les dates d'épreuve viennent du module : elles ne
jugent que le message.

USAGE : python3 tests/EPREUVES_DU_MESSAGE_DU_SOIR_Mer_30-09-2026.py <racine du dépôt> [--saboter] [--jour=AAAA-MM-JJ]
CODE : 0 si Z0 est vert et, avec --saboter, si chaque sabotage fait rougir au moins une épreuve ; 1 sinon ; 2 si un
sabotage ne s'applique plus.
"""
import json, os, re, shutil, subprocess, sys, tempfile
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")
PROG = "programmes/MESSAGE_DU_SOIR.py"
SABOTAGES = {
    "Z0": [],
    "S1_toujours_passe": [("            passe = C.fabrique_du_jour(racine, ch, motif, quoi) is None\n",
                           "            passe = True\n")],
    "S2_tout_nouveau": [("        cles_avant = {cle(x) for x in r0 + o0}\n", "        cles_avant = set()\n")],
    "S3_chiffres_gardes": [('    return re.sub(r"\\d+", "", ligne)\n', "    return ligne\n")],
    "S4_code_toujours_0": [("    sys.exit(code)\n", "    sys.exit(0)\n")],
    "S5_signaux_ignores": [('seance, signaux = s.get("seance"), s.get("signaux") or []', 'seance, signaux = s.get("seance"), []')],
    "S6_tout_le_journal": [('if seance and t.get("date_sortie") == seance]', 'if True]')],
    "S7_une_ligne_un_trade": [("        k = tuple(l.get(c, \"\") for c in champs)\n", "        k = id(l)\n")],
    "S8_seance_non_confrontee": [("        elif seance_d < plancher:\n", "        elif False:\n")],
    "S9_banniere_entiere": [("    if len(bilan) > BANNIERE:\n", "    if False:\n")],
    "S10_score_non_confronte": [("        elif score[1] != len(oranges) or score[2] != len(rouges):\n", "        elif False:\n")],
    "S11_seule_absence": [("    except Exception as e:\n        illisibles.append(f\"{SIGNAUX} ({type(e).__name__})\")",
                           "    except OSError as e:\n        illisibles.append(f\"{SIGNAUX} ({type(e).__name__})\")")],
    "S12_soixante_caracteres": [('    return re.sub(r"\\d+", "", ligne)\n', '    return re.sub(r"\\d+", "", ligne)[:60]\n')],
    "S13_cles_du_fichier_ignorees": [("        if ec:\n            illisibles.append(SIGNAUX", "        if False:\n            illisibles.append(SIGNAUX")],
    "S14_contrat_des_positions_ignore": [('        if C is not None and C.verifier("POSITION", cols, "LU"):', '        if False:')],
    "S15_connu_sans_veille": [("    if connus and cles_avant is None:\n", "    if False:\n")],
    "S17_enveloppe_hors_contrat_toleree": [('            ec += C.verifier("SIGNAUX_DU_JOUR", list(s.keys()), "LU")\n', "")],
    "S18_signal_hors_contrat_tolere": [('                ec += C.verifier("SIGNAL", list(x.keys()), "LU") if isinstance(x, dict) else ["signal illisible"]\n',
                                        '                ec += [] if isinstance(x, dict) else ["signal illisible"]\n')],
    "S21_attendue_jour_meme": [("        attendue = K.dernier_jour_de_bourse(_auj, cal)\n", "        attendue = _auj\n")],
    "S22_retard_non_compte": [("                           + f\" — {retard} jour(s) de bourse de retard\"\n", "")],
    "S23_hors_couverture_tolere": [("    except Exception as e:\n        # Le chemin d'un fichier absent", "    except OSError as e:\n        # Le chemin d'un fichier absent")],
    "S24_calendrier_racine_seule": [("    else:\n        base = os.path.dirname(ici)\n", "    else:\n        base = racine\n")],
    "S25_plancher_ignore": [("        plancher = attendue if passe else veille_de_bourse\n", "        plancher = attendue\n")],
    "S26_posterieure_toleree": [("        if seance_d > attendue:\n", "        if False:\n")],
    "S27_hors_jour_de_bourse_tolere": [('        elif seance_d >= cal["depuis"] and not K.est_jour_de_bourse(seance_d, cal):\n', "        elif False:\n")],
    "S28_attendue_inconnue_tue": [('        detail.append("Séance attendue : inconnue (calendrier de la Bourse illisible)")\n', "        pass\n")],
    "S29_origine_du_calendrier_tue": [("        detail.append(f\"Calendrier de la Bourse lu {ou_cal}, couvert", "        detail.append(f\"Calendrier de la Bourse lu, couvert")],
    "S30_depot_du_programme_d_abord": [("    if os.path.exists(os.path.join(racine, m.FICHIER)):\n", "    if not os.path.exists(os.path.join(os.path.dirname(ici), m.FICHIER)):\n")],
    "S31_fin_de_couverture_tue": [('    if K is not None and (cal["jusqu_au"] - _auj).days < 30:\n', "    if False:\n")],
    "S32_seance_illisible_toleree": [('                ec.append(f"« seance » illisible : {str(seance)[:20]}")\n', "                pass\n")],
    "S33_retard_hors_couverture": [('            if seance_d >= cal["depuis"]:\n                retard', "            if True:\n                retard")],
    "S34_posterieure_au_plancher": [("        if seance_d > attendue:\n", "        if seance_d > plancher:\n")],
    "S35_seuil_de_fin_a_11_jours": [('(cal["jusqu_au"] - _auj).days < 30:', '(cal["jusqu_au"] - _auj).days < 11:')],
    "S36_plancher_trois_jours": [("K.dernier_jour_de_bourse(_auj - timedelta(days=1), cal)\n", "K.dernier_jour_de_bourse(_auj - timedelta(days=3), cal)\n")],
    "S37_forme_de_seance_libre": [('            if not re.fullmatch(r"\\d{4}-\\d{2}-\\d{2}", str(seance)):\n', "            if not isinstance(seance, str):\n")],
    "S38_compte_hors_couverture_faux": [('retard = "au moins " + str(', 'retard = "au moins " + str(1 + ')],
    "S39_samedi_sans_retard": [('" sur la séance du {jj(plancher.isoformat())}" if seance_d < plancher else ""))', '" sur la séance du {jj(plancher.isoformat())}" if False else ""))')],
    "S40_seance_impossible_affichee": [('    etat = f"séance {jj(seance if seance_d else None)} · ', '    etat = f"séance {jj(seance)} · ')],
    "S41_date_du_radar_mal_lue": [("if x[0] == RAPPORT))[0]   # la date seule", "if x[0] == RAPPORT))[1]   # la date seule")],
    "S42_seuil_ignore": [("    if quand < seuil:\n", "    if False:\n")],
    "S43_auteur_non_ancre": [('"--author=^" + motif + "$"', '"--author=certification"')],
    "S44_seuil_en_heure_de_paris": [('h, mi, tzinfo=ZoneInfo("UTC"))', 'h, mi, tzinfo=ZoneInfo("Europe/Paris"))')],
    "S45_jours_du_reveil_ignores": [("        if a <= (jour.isoweekday() % 7) <= b and seuil + timedelta(minutes=delai) <= maintenant:\n", "        if seuil + timedelta(minutes=delai) <= maintenant:\n")],
    "S46_superficiel_accepte": [('    if lire_git(racine, "rev-parse", "--is-shallow-repository") != "false\\n":\n', "    if False:\n")],
    "S47_committer_ignore": [("    if committer != auteur:\n", "    if False:\n")],
    "S48_futur_accepte": [("    if quand > maintenant + timedelta(minutes=10):\n", "    if False:\n")],
    "S49_regle_a_retiree": [('    if CERTIFICAT not in touche.split("\\n"):\n', "    if False:\n")],
    "S50_verdict_illisible_tolere": [("    if not v:\n", "    if False:\n")],
    "S51_date_du_committer": [('"--format=%H%x09%an <%ae>%x09%cn <%ce>%x09%at")', '"--format=%H%x09%an <%ae>%x09%cn <%ce>%x09%ct")')],
    "S52_code_sans_certificat": [("(not passe or alerte_seance or alerte_certif is not None)", "(not passe or alerte_seance)")],
    "S53_detail_tu": [("    detail.append(ligne_certif)\n", "")],
    "S54_reveil_suppose": [("    mi, h, a, b = (int(x) for x in forme[0].groups())\n", "    mi, h, a, b = 0, 21, 1, 5\n")],
    "S55_reveil_libre": [("    if len(lignes) != 1 or not forme[0]:\n", "    if len(lignes) != 1:\n")],
    "S56_aucun_passage_tu": [('        return "🚨 Certification absente (aucun passage)", None, \\\n', '        return None, None, \\\n')],
    "S57_jours_en_dur": [("    mi, h, a, b = (int(x) for x in forme[0].groups())\n", "    mi, h, a, b = (int(x) for x in forme[0].groups()); a, b = 1, 5\n")],
    "S58_minute_ignoree": [("seuil = datetime(jour.year, jour.month, jour.day, h, mi, tzinfo", "seuil = datetime(jour.year, jour.month, jour.day, h, 0, tzinfo")],
    "S59_motif_non_echappe": [('    motif = "".join("\\\\" + c if c in ".[]*^$\\\\" else c for c in IDENTITE_CERTIFICATION)\n', "    motif = IDENTITE_CERTIFICATION\n")],
    "S60_adresse_du_committer_ignoree": [("    if committer != auteur:\n", '    if committer.split(" <")[0] != auteur.split(" <")[0]:\n')],
    "S61_delai_ignore": [("seuil + timedelta(minutes=delai) <= maintenant", "seuil < maintenant")],
    "S16_nouveau_coupe": [('        detail.append("  NOUVEAU " + x if x in nouv_r else "  " + x[:160])',
                           '        detail.append("  NOUVEAU " + x[:160] if x in nouv_r else "  " + x[:160])')],
}
ENTETE_J = "strategie,valeur,date_entree,prix_entree,date_sortie,prix_sortie,motif_sortie,pnl_net_eur,comptabilite\n"
ENTETE_P = "strategie,valeur,date_signal,date_entree,prix_entree,tp,sl,horizon_fin,statut,comptabilite\n"
# L'HORLOGE DES ÉPREUVES EST FIXÉE (relecteur, 30-09-2026) : lancées un lundi, un samedi ou un dimanche, trois sabotages
# échappaient (la veille de bourse et la séance attendue se confondent ces jours-là). Chaque programme lancé lit donc
# l'heure d'un mercredi ordinaire, posée par tests/HORLOGE_D_EPREUVE.py. --jour=AAAA-MM-JJ
# choisit un autre jour, pour voir le message un jour particulier ; un week-end, S25 et S34 n'y sont pas attrapés.
JOUR_FIXE = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--jour=")), "2026-09-30")
HORLOGE = f"{JOUR_FIXE}T20:45:00"
_J = datetime.fromisoformat(HORLOGE).date()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from HORLOGE_D_EPREUVE import lancer_a_l_heure   # l horloge posée à un seul endroit (R-708)
AUJ, HIER = _J.isoformat(), (_J - timedelta(days=1)).isoformat()
sys.path.insert(0, os.path.join(DEPOT, "programmes"))
import CALENDRIER_DE_LA_BOURSE as _K
_CAL = {"fermes": set(), "depuis": _J - timedelta(days=90), "jusqu_au": _J + timedelta(days=90)}
_S = [_K.dernier_jour_de_bourse(_J, _CAL)]          # la séance attendue ce soir, puis celles d'avant
for _i in range(4):
    _S.append(_K.dernier_jour_de_bourse(_S[-1] - timedelta(days=1), _CAL))
ATT, PREC, PREC3 = _S[0].isoformat(), _S[1].isoformat(), _S[3].isoformat()
# la séance qui suffit tant que le circuit du soir n'est pas passé : la veille de bourse
PLANCHER = _K.dernier_jour_de_bourse(_J - timedelta(days=1), _CAL).isoformat()
_sam = _S[0] - timedelta(days=1)
while _sam.weekday() != 5:
    _sam -= timedelta(days=1)
SAMEDI = _sam.isoformat()   # le dernier samedi avant la séance attendue, dans la couverture
# COMPTÉS SANS LE MODULE (relecteur, 30-09-2026) : les jours du lundi au vendredi, le calendrier d'épreuve n'ayant
# aucune fermeture. Du samedi (exclu) à la séance attendue ; puis du début de la couverture à la séance attendue.
_ouvres = lambda a, b: sum((a + timedelta(days=k)).weekday() < 5 for k in range((b - a).days + 1))
RETARD_SAMEDI = _ouvres(_sam + timedelta(days=1), _S[0])
N_COUVERTURE = _ouvres(_J - timedelta(days=90), _S[0])
_p = _K.dernier_jour_de_bourse(_J - timedelta(days=1), _CAL)
for _i in range(2):
    _p = _K.dernier_jour_de_bourse(_p - timedelta(days=1), _CAL)
PLANCHER_MOINS_2 = _p.isoformat()


def calendrier_d_epreuve(d, forme="normal"):
    """Écrit un calendrier d'épreuve dans la racine `d`, couvrant 90 jours autour d'aujourd'hui.

    ① RÔLE — Rendre les épreuves indépendantes du calendrier réel et du jour où elles tournent.
    ② CONTEXTE D'APPEL — `monter`.
    ③ ENTRÉE — `d` : la racine · `forme` : « normal » (aucune fermeture), « ferie » (aujourd'hui
      fermé, s'il tombe en semaine : un week-end n'a pas de séance de toute façon), « hors » (couvert jusqu'à
      hier), « fin_proche », « fin_29 », « fin_31 » (couvert jusqu'à dans 10, 29 ou 31 jours), « absent » (aucun
      fichier).
    ④ CONDITIONS D'ENTRÉE — Le dossier donnees/ existe.
    ⑤ SORTIE — Ne rend rien : écrit un fichier.
      [rend: rien]
    ⑥ TRAITEMENT — écrire l'en-tête du contrat, les bornes, et la fermeture demandée.
    ⑦ UNITÉ — Des dates.
    ⑧ POURQUOI — E26 à E29 visent le calendrier ; les autres épreuves ne doivent pas en dépendre.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans `d`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if forme == "absent":
        return
    fin = {"hors": _J - timedelta(days=1), "fin_proche": _J + timedelta(days=10), "fin_29": _J + timedelta(days=29),
           "fin_31": _J + timedelta(days=31)}.get(forme, _J + timedelta(days=90))
    L = ["date,etat,source,citation,fichiers_cites", f"{(_J - timedelta(days=90)).isoformat()},COUVERT_DEPUIS,epreuve,,",
         f"{fin.isoformat()},COUVERT_JUSQU_AU,epreuve,,"]
    if forme == "ferie" and _J.weekday() < 5:
        L.append(f"{AUJ},FERME,epreuve,,")
    open(os.path.join(d, "donnees", "CALENDRIER_EURONEXT.csv"), "w", encoding="utf-8").write("\n".join(L) + "\n")


def rapport(jour, lignes, score=None):
    """Rend le texte d'un rapport du radar fabriqué, daté du `jour` AAAA-MM-JJ.

    ① RÔLE — Fabriquer un rapport à la forme de rapports/audit_du_jour.md.
    ② CONTEXTE D'APPEL — `monter`, deux fois par cas.
    ③ ENTRÉE — `jour` : AAAA-MM-JJ · `lignes` : les lignes ❌ et ⚠️ · `score` : un triplet imposé, pour
      fabriquer un rapport coupé ; sinon compté sur les lignes.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte.
      [rend: 1]
    ⑥ TRAITEMENT — ① première ligne datée JJ-MM-AAAA, comme l'écrit le radar · ② ligne de score · ③ les lignes.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les épreuves ne dépendent pas du rapport réel du jour.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main.
      [sort: non]
    """
    a, m, j = jour.split("-")
    r = sum(l.startswith("❌") for l in lignes); o = sum(l.startswith("⚠️") for l in lignes)
    v, o, r = score or (40, o, r)
    return (f"# AUDIT ÉCOSYSTÈME CAC 40 — Mer {j}-{m}-{a} 20h22 (Paris)\n# Score : {v} ✅  ·  {o} ⚠️  ·  {r} ❌\n\n"
            + "✅ [1-Acquisition] ok\n" + "\n".join(lignes) + "\n")


IDENTITE = ("certification-publique", "certification-publique@users.noreply.github.com")
_UT = ZoneInfo("UTC")


def _veille_ouvree(j):
    """Rend le dernier jour du lundi au vendredi avant `j` (le réveil « 0 21 * * 1-5 », écrit ici à la main)."""
    j -= timedelta(days=1)
    while j.weekday() > 4:
        j -= timedelta(days=1)
    return j


_VO = _veille_ouvree(_J)
NUIT = datetime(_VO.year, _VO.month, _VO.day, 21, 30, tzinfo=_UT)          # le passage de la nuit attendue
SEUIL = datetime(_VO.year, _VO.month, _VO.day, 21, 0, tzinfo=_UT)          # l'heure du réveil, la veille ouvrée


def passage(quand, certificat=True, auteur=IDENTITE, committer=None, quand_committer=None, verdict="**VERSION CERTIFIÉE**"):
    """Décrit un passage de la certification à enregistrer (voir `enregistrer_un_passage`).

    ① RÔLE — Une ligne de l'historique des passages, telle que le pas « deposer » l'écrit.
    ② CONTEXTE D'APPEL — `epreuves`, par `monter`.
    ③ ENTRÉE — `quand` : une heure avec son fuseau · `certificat` : faux si le passage ne dépose que son journal ·
      `auteur`, `committer` : des couples (nom, adresse), le committer valant l'auteur par défaut ·
      `quand_committer` : la date du committer, `quand` par défaut · `verdict` : la ligne de verdict du certificat.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : un dictionnaire. [rend: 1]
    ⑥ TRAITEMENT — rassembler.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les heures sont construites avec leur fuseau, jamais « +02:00 » écrit en dur (relecture du
      28-10-2026, I3 : l'épreuve rougissait en heure d'hiver).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
    """
    return {"quand": quand, "certificat": certificat, "auteur": auteur, "committer": committer or auteur,
            "quand_committer": quand_committer or quand, "verdict": verdict}


def enregistrer_un_passage(d, x):
    """Enregistre un passage de la certification dans le dépôt d'épreuve : son journal, et son certificat s'il en dépose.

    ① RÔLE — Fabriquer l'historique que le message relit.
    ② CONTEXTE D'APPEL — `monter`.
    ③ ENTRÉE — `d` : le dépôt d'épreuve · `x` : un passage décrit par `passage`.
    ④ CONDITIONS D'ENTRÉE — `d` est un dépôt git.
    ⑤ SORTIE — Aucune valeur rendue. [rend: 0]
    ⑥ TRAITEMENT — écrire un journal neuf, et le certificat s'il en dépose ; enregistrer avec l'auteur, le
      committer et les deux dates donnés.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un passage raté ne dépose que son journal (pas « deposer » en « if: always() »).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans `d` et lance `git`.
    ⑪ TERMINAISON — Rend la main ; `git` peut lever.
      [sort: non]
    """
    os.makedirs(os.path.join(d, "rapports", "journal_du_circuit"), exist_ok=True)
    n = len(os.listdir(os.path.join(d, "rapports", "journal_du_circuit")))
    open(os.path.join(d, "rapports", "journal_du_circuit", f"circuit_{n}_1_certifier.log"), "w").write("journal\n")
    if x["certificat"]:
        open(os.path.join(d, "rapports", "CERTIFICAT_DE_LA_VERSION.md"), "w", encoding="utf-8").write(
            f"# CERTIFICAT DE LA VERSION {n}\n\n{x['verdict']}\n")
    subprocess.run(["git", "-C", d, "add", "-A"], capture_output=True, check=True)
    env = dict(os.environ, GIT_AUTHOR_NAME=x["auteur"][0], GIT_AUTHOR_EMAIL=x["auteur"][1],
               GIT_COMMITTER_NAME=x["committer"][0], GIT_COMMITTER_EMAIL=x["committer"][1],
               GIT_AUTHOR_DATE=x["quand"].isoformat(), GIT_COMMITTER_DATE=x["quand_committer"].isoformat())
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", "certificat de la version"], capture_output=True, check=True, env=env)


def monter(d, veille, jour, seance=None, signaux=None, journal="", git=True, fichier_signaux="normal",
           manquantes=None, score=None, entete_p=None, cal="normal", passages="nuit"):
    """Fabrique un petit dépôt git : le rapport de la veille, puis celui du jour.

    ① RÔLE — Poser chaque cas dans un dépôt neuf.
    ② CONTEXTE D'APPEL — `epreuves`, une fois par cas.
    ③ ENTRÉE — `d` : dossier vide · `veille`, `jour` : couples (date, lignes) · `seance` : la séance du fichier
      des signaux · `signaux` : liste · `journal` : lignes du journal · `git` : faux pour une copie sans historique ·
      `fichier_signaux` : « normal », « absent », « null » ou « sans_cle » (ni « signaux » ni les valeurs sans
      séance) · `manquantes` : valeurs sans la séance · `score` : un triplet imposé au rapport du jour · `entete_p` :
      un en-tête imposé au fichier des positions · `passages` : les passages de la certification à enregistrer,
      « nuit » (celui de la veille ouvrée à 21h30 UT, qui dépose le certificat) ou une liste de `passage(...)`.
    ④ CONDITIONS D'ENTRÉE — `git` doit être installé.
    ⑤ SORTIE — UNE valeur : la racine fabriquée.
      [rend: 1]
    ⑥ TRAITEMENT — ① écrire les données · ② enregistrer le rapport de la veille · ③ enregistrer celui du jour.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Le programme relit la veille dans l'historique git : l'épreuve doit en fabriquer un.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit dans `d` et lance `git`.
    ⑪ TERMINAISON — Rend la main ; `git` peut lever.
      [sort: non]
    """
    for s in ("rapports", "donnees"):
        os.makedirs(os.path.join(d, s), exist_ok=True)
    seance = ATT if seance is None else seance
    calendrier_d_epreuve(d, cal)
    fs = os.path.join(d, "donnees", "signaux_du_jour.json")
    if fichier_signaux == "normal":
        json.dump({"seance": seance, "signaux": signaux or [], "valeurs_sans_cette_seance": manquantes or []},
                  open(fs, "w", encoding="utf-8"))
    elif fichier_signaux == "null":
        open(fs, "w", encoding="utf-8").write("null")
    elif fichier_signaux == "sans_cle":
        json.dump({"seance": seance}, open(fs, "w", encoding="utf-8"))
    elif fichier_signaux == "cle_en_trop":
        json.dump({"seance": seance, "signaux": [], "valeurs_sans_cette_seance": [], "cle_inconnue": 1},
                  open(fs, "w", encoding="utf-8"))
    open(os.path.join(d, "donnees", "claude_positions_ouvertes.csv"), "w", encoding="utf-8").write(entete_p or ENTETE_P)
    open(os.path.join(d, "donnees", "claude_journal_trades.csv"), "w", encoding="utf-8").write(ENTETE_J + journal)
    g = lambda *a: subprocess.run(["git", "-C", d, *a], capture_output=True, check=True)
    if git:
        g("init", "-q"); g("config", "user.email", "e@e"); g("config", "user.name", "e")
        g("config", "commit.gpgsign", "false")   # dépôt jetable : la signature de l'environnement sature à la longue
        for x in ([passage(NUIT)] if passages == "nuit" else passages):
            enregistrer_un_passage(d, x)
    for k, (date_, lignes) in enumerate((veille, jour)):
        open(os.path.join(d, "rapports", "audit_du_jour.md"), "w", encoding="utf-8").write(
            rapport(date_, lignes, score if k == 1 else None))
        if git:
            g("add", "-A"); g("commit", "-q", "-m", date_)
    return d


def lancer(prog, racine, horloge=None):
    """Lance le programme (éventuellement saboté) et rend (code, première ligne, sortie).

    ① RÔLE — Emprunter le chemin réel : le programme en ligne de commande, jamais une copie de sa logique.
    ② CONTEXTE D'APPEL — `epreuves`, une fois par cas.
    ③ ENTRÉE — `prog` : le programme · `racine` : la racine.
    ④ CONDITIONS D'ENTRÉE — CONTRATS_DES_FICHIERS.py doit être à côté du programme.
    ⑤ SORTIE — TROIS valeurs : le code de sortie, la première ligne, la sortie entière.
      [rend: 3]
    ⑥ TRAITEMENT — poser l'horloge fixée à côté du programme, lancer, capturer.
    ⑦ UNITÉ — Des SECONDES pour le délai maximal de 120.
    ⑧ POURQUOI — Le code de sortie fait partie de ce qui est éprouvé (E2, E7, E11, E14).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit _horloge/sitecustomize.py à côté du programme ; lance un processus.
    ⑪ TERMINAISON — Rend la main ; au-delà de 120 secondes, lève.
      [sort: non]
    """
    p = lancer_a_l_heure([sys.executable, prog, racine], horloge or HORLOGE, os.path.join(os.path.dirname(os.path.abspath(prog)), "_horloge"))
    return p.returncode, (p.stdout.splitlines() or [""])[0], p.stdout + p.stderr


def epreuves(prog, tmp):
    """Joue les épreuves avec le programme `prog` et rend la liste (nom, verdict).

    ① RÔLE — Les épreuves décrites en tête.
    ② CONTEXTE D'APPEL — `main`, une fois par sabotage.
    ③ ENTRÉE — `prog` : le programme, saboté ou non · `tmp` : un dossier jetable.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des couples (nom, vrai si verte).
      [rend: 1]
    ⑥ TRAITEMENT — un dépôt fabriqué par cas, puis le chemin réel sur la racine donnée (E10).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Chaque cas vise une phrase que Jean-Luc lira.
    ⑨ CE QUI CLOCHE — E10 ne contrôle que la séance annoncée sur les vraies données.
    ⑩ EFFET — Écrit dans `tmp`.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    V, J = HIER, AUJ
    o7 = ["⚠️ [16-Backlog] sans mouvement depuis 7 jours : A-1"]
    o8 = ["⚠️ [16-Backlog] sans mouvement depuis 8 jours : A-1, A-2"]
    r1 = ["❌ [16-Backlog] BACKLOG EN ÉCHEC : ❌ A-425 : statut inconnu « DÉCIDÉ·19/09 », à réécrire avec Jean-Luc"]
    n = iter(range(100))
    dos = lambda: os.path.join(tmp, "c%d" % next(n))
    res = []
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8)))
    res.append(("E1 soir normal : ✅, rien à signaler, aucun signal, 0 position", c == 0 and l1.startswith("✅") and "rien à signaler" in l1 and "aucun signal" in l1 and "0 position(s)" in l1))
    res.append(("E6 un ⚠️ dont seule la liste change n'est pas nouveau", "nouveau" not in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7 + r1), (J, o8 + r1)))
    res.append(("E1b un ❌ connu : ⚠️ et « ❌ connu »", l1.startswith("⚠️") and "❌ connu" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (V, o8)))
    res.append(("E2 rapport de la veille : « Circuit du soir NON passé (dernier radar du JJ-MM) », code 2",
                c == 2 and f"Circuit du soir NON passé (dernier radar du {V[8:10]}-{V[5:7]})" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), signaux=[{"valeur": "ENGIE", "close": 20.1}]))
    res.append(("E3 un signal ENGIE est nommé en première ligne", "1 signal(s) : ENGIE" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8 + ["❌ [14-Fraîcheur] DONNÉES PÉRIMÉES"])))
    res.append(("E4 un ❌ nouveau : 🚨 et « ❌ nouveau »", l1.startswith("🚨") and "❌ nouveau" in l1 and "NOUVEAU ❌" in o))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8 + ["⚠️ [18-Tâches] cockpit muet"])))
    res.append(("E5 un ⚠️ nouveau : ⚠️ en tête et « ⚠️ nouveau »", l1.startswith("⚠️") and "⚠️ nouveau" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), fichier_signaux="absent"))
    res.append(("E7 signaux absents : « Message incomplet », code 1", c == 1 and "Message incomplet" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8 + ["❌ [14-Fraîcheur] X"]), git=False))
    res.append(("E8 sans historique : « veille non relue » en tête, rien de « NOUVEAU »", "veille non relue" in l1 and "NOUVEAU" not in o))
    jr = (f"S,ENGIE,{PREC},20,{ATT},21,TP,500,un_jeton\nS,ENGIE,{PREC},20,{ATT},21,TP,500,jetons_illimites\n"
          "S,VINCI,2026-09-01,100,2026-09-10,98,SL,-300,un_jeton\n")
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), journal=jr))
    res.append(("E9 un trade clos ce soir, écrit sous deux comptabilités", "Trades clos ce soir : 1 " in o))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), seance=PREC))
    res.append(("E11 séance précédente : « Séance du JJ-MM NON lue », code 2", c == 2 and f"Séance du {ATT[8:10]}-{ATT[5:7]} NON lue" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), manquantes=["ENGIE", "VINCI"]))
    res.append(("E12 deux valeurs sans la séance : dit en première ligne", "2 valeur(s) sans la séance" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), score=(40, 1, 1)))
    res.append(("E13 rapport coupé : « Message incomplet »", c == 1 and "Message incomplet" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), fichier_signaux="null"))
    res.append(("E14 signaux null : « Message incomplet », code 1, sans plantage", c == 1 and "Message incomplet" in l1 and "Traceback" not in o))
    dix = [{"valeur": "VALEUR_%02d" % k, "close": 1} for k in range(10)]
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), signaux=dix))
    res.append(("E15 dix signaux : première ligne de 200 caractères au plus", 0 < len(l1) <= 200))
    r2 = [r1[0] + " | ❌ A-509 : CLOSE sans preuve"]   # même début que r1 sur plus de 60 caractères
    c, l1, o = lancer(prog, monter(dos(), (V, o7 + r1), (J, o8 + r2)))
    res.append(("E16 un échec de plus dans la ligne ❌ du BACKLOG : « ❌ nouveau »", "❌ nouveau" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), fichier_signaux="sans_cle"))
    res.append(("E17 signaux sans « signaux » : « Message incomplet », code 1", c == 1 and "Message incomplet" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), entete_p=ENTETE_P.strip() + ",colonne_inconnue\n"))
    res.append(("E18 positions hors contrat : « Message incomplet »", c == 1 and "Message incomplet" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7 + r1), (J, o8 + r1), git=False))
    res.append(("E19 sans historique, un ❌ : 🚨 et jamais « connu »", l1.startswith("🚨") and "connu" not in l1))
    _P = ZoneInfo("Europe/Paris")
    _h = lambda dt: dt.astimezone(_P).strftime("%d-%m à %Hh%M")
    _vo = lambda j, n: [j := _veille_ouvree(j) for _ in range(n)][-1]
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8)))
    res.append(("E40 passage de la nuit qui dépose : rien n'est dit, le détail le date", c == 0 and "Certification" not in l1
                and f"Certificat de la version : déposé le {_h(NUIT)} · VERSION CERTIFIÉE" in o))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), passages=[]))
    res.append(("E41 aucun passage : 🚨 « Certification absente (aucun passage) », code 2",
                c == 2 and l1.startswith("🚨") and "Certification absente (aucun passage)" in l1))
    _d3 = _vo(_J, 3)
    _q3 = datetime(_d3.year, _d3.month, _d3.day, 21, 30, tzinfo=_UT)
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), passages=[passage(_q3)]))
    res.append(("E42 dernier passage trois jours ouvrés avant : 🚨 « absente » et sa date, code 2",
                c == 2 and f"Certification absente (dernier passage {_q3.astimezone(_P):%d-%m})" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), passages=[passage(_q3), passage(NUIT, certificat=False)]))
    res.append(("E43 passage de la nuit qui ne dépose que son journal : 🚨 « sans certificat », code 2",
                c == 2 and f"Certification sans certificat (passage du {NUIT.astimezone(_P):%d-%m %Hh%M})" in l1))
    _man = datetime(_VO.year, _VO.month, _VO.day, 15, 0, tzinfo=_P)
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), passages=[passage(_man), passage(NUIT, certificat=False)]))
    res.append(("E44 manuel de l'après-midi puis nuit ratée : 🚨 « sans certificat »", c == 2 and "Certification sans certificat" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), passages=[passage(SEUIL - timedelta(minutes=1))]))
    ok_av = c == 2 and "Certification absente" in l1
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), passages=[passage(SEUIL + timedelta(minutes=1))]))
    res.append(("E45 bornes : 20h59 UT la veille → 🚨 « absente » ; 21h01 UT → rien", ok_av and c == 0 and "Certification" not in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), passages=[passage(NUIT, auteur=("certification-claude", "c@c"))]))
    ok_cl = c == 2 and "Certification absente (aucun passage)" in l1
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), passages=[passage(NUIT, auteur=("certification-publique-test", IDENTITE[1]))]))
    res.append(("E46 identités voisines : elles ne comptent pas, 🚨", ok_cl and c == 2 and "Certification absente (aucun passage)" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), passages=[passage(NUIT, committer=("chat", "chat@chat"))]))
    ok_rec = c == 1 and "réécrit par chat" in o
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), passages=[passage(_q3, quand_committer=NUIT)]))
    res.append(("E47 passage recopié par un autre : illisible ; date d'auteur vieille, committer frais : 🚨",
                ok_rec and c == 2 and "Certification absente" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), passages=[passage(datetime.fromisoformat(HORLOGE).replace(tzinfo=_P) + timedelta(days=1))]))
    res.append(("E48 passage daté du futur : illisible, code 1", c == 1 and "daté du futur" in o))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), passages=[passage(NUIT, verdict="sans verdict")]))
    res.append(("E49 certificat sans verdict : illisible, code 1", c == 1 and "verdict illisible" in o))
    src = monter(dos(), (V, o7), (J, o8), passages=[passage(_q3), passage(NUIT, certificat=False)])
    peu = dos()
    subprocess.run(["git", "clone", "-q", "--depth", "1", "file://" + src, peu], capture_output=True, check=True)
    c, l1, o = lancer(prog, peu)
    res.append(("E50 clone superficiel : illisible, code 1, jamais « déposé »", c == 1 and "clone superficiel" in o and "déposé le" not in o))
    _lun = datetime(2026, 10, 5, 20, 45)                          # un lundi d'heure d'été
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), passages=[passage(datetime(2026, 10, 3, 3, 22, tzinfo=_P))]),
                      horloge=_lun.isoformat())
    ok_sam = "Certification" not in l1
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), passages=[passage(datetime(2026, 10, 2, 4, 24, tzinfo=_P))]),
                      horloge=_lun.isoformat())
    ok_ven = "Certification absente (dernier passage 02-10)" in l1
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), passages=[passage(datetime(2026, 10, 27, 21, 30, tzinfo=_UT))]),
                      horloge="2026-10-28T20:45:00")
    res.append(("E51 un lundi : samedi 03h22 → rien, vendredi 04h24 → 🚨 ; en heure d'hiver : la veille 21h30 UT → rien",
                ok_sam and ok_ven and "Certification" not in l1 and "déposé le 27-10 à 22h30" in o))
    _fab = open(os.path.join(os.path.dirname(prog), "FABRIQUER_LE_CIRCUIT_PUBLIC.py"), encoding="utf-8").read()
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("FAB_epreuve", os.path.join(os.path.dirname(prog), "FABRIQUER_LE_CIRCUIT_PUBLIC.py"))
    _F = _iu.module_from_spec(_sp); _sp.loader.exec_module(_F)
    _dep = _F.CERTIFICATION[_F.CERTIFICATION.find("id: deposer"):][:400]
    res.append(("E52 le gabarit : réveil « 0 21 * * 1-5 », « deposer » en « if: always() », identité certification-publique",
                re.findall(r'cron: "([^"]*)"', _F.CERTIFICATION) == ["0 21 * * 1-5"] and "if: always()" in _dep[:60]
                and f"git config user.name {IDENTITE[0]}" in _dep and f"git config user.email {IDENTITE[1]}" in _dep))
    autre = os.path.join(tmp, "reveil_change")
    shutil.copytree(os.path.dirname(prog), autre, ignore=shutil.ignore_patterns("_horloge"))
    open(os.path.join(autre, "FABRIQUER_LE_CIRCUIT_PUBLIC.py"), "w", encoding="utf-8").write(
        _fab.replace('cron: "0 21 * * 1-5"', 'cron: "30 6 * * 1-5"', 1))
    _dix = datetime(_J.year, _J.month, _J.day, 10, 0, tzinfo=_UT)
    c, l1, o = lancer(os.path.join(autre, os.path.basename(prog)), monter(dos(), (V, o7), (J, o8), passages=[passage(_dix)]))
    ok_lu = c == 0 and "Certification" not in l1
    c, l1, o = lancer(os.path.join(autre, os.path.basename(prog)),
                      monter(dos(), (V, o7), (J, o8), passages=[passage(_dix - timedelta(days=1))]))
    ok_lu = ok_lu and c == 2 and "Certification absente" in l1
    open(os.path.join(autre, "FABRIQUER_LE_CIRCUIT_PUBLIC.py"), "w", encoding="utf-8").write(
        _fab.replace('cron: "0 21 * * 1-5"', 'cron: "0 21 * * *"', 1))
    c, l1, o = lancer(os.path.join(autre, os.path.basename(prog)), monter(dos(), (V, o7), (J, o8)))
    res.append(("E53 réveil lu : « 30 6 * * 1-5 » → le jour 10h UT suffit, la veille 10h UT non ; « 0 21 * * * » → illisible",
                ok_lu and c == 1 and "(ValueError: réveil de la certification illisible" in o))
    def gabarit(nouveau):
        open(os.path.join(autre, "FABRIQUER_LE_CIRCUIT_PUBLIC.py"), "w", encoding="utf-8").write(nouveau)
        return os.path.join(autre, os.path.basename(prog))
    p14 = gabarit(_fab.replace('cron: "0 21 * * 1-5"', 'cron: "0 21 * * 1-4"', 1))
    c, l1, o = lancer(p14, monter(dos(), (V, o7), (J, o8), passages=[passage(datetime(2026, 10, 1, 21, 30, tzinfo=_UT))]),
                      horloge="2026-10-05T20:45:00")
    res.append(("E55 réveil « 1-4 », un lundi : le passage du jeudi suffit", "Certification" not in l1 and "déposé le 01-10" in o))
    p45 = gabarit(_fab.replace('cron: "0 21 * * 1-5"', 'cron: "45 20 * * 1-5"', 1))
    c, l1, o = lancer(p45, monter(dos(), (V, o7), (J, o8), passages=[passage(datetime(_VO.year, _VO.month, _VO.day, 20, 30, tzinfo=_UT))]))
    res.append(("E56 réveil « 45 20 » : la veille 20h30 UT → 🚨, la minute est lue", c == 2 and "Certification absente" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), passages=[passage(NUIT, auteur=(IDENTITE[0], IDENTITE[1].replace(".", "X")))]))
    res.append(("E57 adresse aux points remplacés : « aucun passage »", c == 2 and "Certification absente (aucun passage)" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), passages=[passage(NUIT, committer=(IDENTITE[0], "autre@autre"))]))
    res.append(("E58 committer du même nom, autre adresse : illisible, code 1", c == 1 and "réécrit par" in o))
    _avant = _veille_ouvree(_VO)
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), passages=[passage(datetime(_avant.year, _avant.month, _avant.day, 21, 30, tzinfo=_UT))]),
                      horloge=f"{(_VO + timedelta(days=1)).isoformat()}T01:00:00")
    res.append(("E59 message à 1h00 pendant le passage : l'avant-veille suffit, rien", "Certification" not in l1 and "déposé le" in o))
    pto = gabarit(re.sub(r"timeout-minutes: *\d+ *\n", "", _fab, count=1))
    c, l1, o = lancer(pto, monter(dos(), (V, o7), (J, o8)))
    res.append(("E60 gabarit sans délai : illisible, code 1", c == 1 and "délai de la certification illisible" in o))
    pex = gabarit("import sys\nsys.exit(0)\nprint('X')\n" + _fab)
    c, l1, o = lancer(pex, monter(dos(), (V, o7), (J, o8)))
    res.append(("E61 fabricant qui arrête Python à l'import : le message n'est pas touché", c == 0 and l1.startswith("✅")))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), git=False))
    res.append(("E54 sans historique : la certification est dite illisible, code 1", c == 1 and "Illisible : rapports/CERTIFICAT_DE_LA_VERSION.md" in o))
    c, l1, o = lancer(prog, monter(dos(), (V, o7 + r1), (J, o8 + [r1[0] + " " + "x" * 200 + " | ❌ A-509 : CLOSE sans preuve"])))
    res.append(("E20 un ❌ nouveau en fin de longue ligne : écrit en entier", "A-509" in o))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), fichier_signaux="cle_en_trop"))
    res.append(("E21 enveloppe des signaux hors contrat : « Message incomplet »", c == 1 and "Message incomplet" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), signaux=[{"valeur": "ENGIE", "close": 20.1, "champ_inconnu": 1}]))
    res.append(("E22 un signal hors contrat : « Message incomplet »", c == 1 and "Message incomplet" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), seance=_K.dernier_jour_de_bourse(_J - timedelta(days=1), _CAL).isoformat(), cal="ferie"))
    res.append(("E26 aujourd'hui sans bourse, dernière séance ouvrée lue : aucune alerte de séance, code 0",
                c == 0 and "NON lue" not in l1 and "Pas de bourse aujourd'hui" in o))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), seance=PREC3))
    res.append(("E27 trois séances de retard : « 3 jour(s) de bourse de retard »", "3 jour(s) de bourse de retard" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), cal="hors"))
    res.append(("E28 calendrier hors couverture : « Message incomplet », code 1", c == 1 and "Message incomplet" in l1 and "CALENDRIER" in o))
    # E29 : le programme dans un dépôt qui porte le calendrier, la racine lue sans calendrier
    dp = os.path.join(tmp, "depot_du_programme")
    os.makedirs(os.path.join(dp, "programmes"), exist_ok=True); os.makedirs(os.path.join(dp, "donnees"), exist_ok=True)
    for f in os.listdir(os.path.dirname(prog)):
        if f.endswith(".py"):
            shutil.copy(os.path.join(os.path.dirname(prog), f), os.path.join(dp, "programmes", f))
    calendrier_d_epreuve(dp)
    c, l1, o = lancer(os.path.join(dp, "programmes", os.path.basename(prog)), monter(dos(), (V, o7), (J, o8), cal="absent"))
    ok_a = c == 0 and "Message incomplet" not in l1 and "lu dans le dépôt du programme" in o
    c, l1, o = lancer(os.path.join(dp, "programmes", os.path.basename(prog)), monter(dos(), (V, o7), (J, o8)))
    ok_b = c == 0 and "lu dans le dépôt lu" in o
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), cal="absent"))
    res.append(("E29 calendrier lu dans le dépôt du programme, et dit ; absent des deux : « Message incomplet », "
                "séance attendue inconnue, aucune séance devinée",
                ok_a and c == 1 and "Message incomplet" in l1 and "Séance attendue : inconnue" in o and "NON lue" not in l1))
    res.append(("E30 calendrier dans la racine lue ET dans le dépôt du programme : celui de la racine, et dit", ok_b))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), seance=(_J + timedelta(days=1)).isoformat()))
    res.append(("E31 séance lue postérieure à l'attendue : « POSTÉRIEURE », code 2", c == 2 and "POSTÉRIEURE" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), seance="2026-02-30"))
    res.append(("E32 séance « 2026-02-30 » : le fichier des signaux est illisible, jamais le calendrier, et la bannière "
                "dit « séance ? »", c == 1 and "« seance » illisible" in o and "Illisible : donnees/CALENDRIER" not in o
                and "séance ? ·" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), seance=ATT.replace("-", "")))
    res.append(("E37 séance sans tirets (« AAAAMMJJ ») : illisible, code 1", c == 1 and "« seance » illisible" in o))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (V, o8), seance=PLANCHER_MOINS_2))
    res.append(("E38 circuit pas encore passé, séance deux jours de bourse avant la veille : « 2 jour(s) »",
                c == 2 and f"Séance du {PLANCHER[8:10]}-{PLANCHER[5:7]} NON lue — 2 jour(s)" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (V, o8), seance=ATT))
    res.append(("E39 circuit pas encore passé mais séance attendue déjà lue : jamais « POSTÉRIEURE »",
                c == 2 and "POSTÉRIEURE" not in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (V, o8), seance=PLANCHER))
    res.append(("E33 circuit pas encore passé, séance de la veille de bourse : « Circuit NON passé », aucune séance NON lue",
                c == 2 and "Circuit du soir NON passé" in l1 and "NON lue" not in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), seance=SAMEDI))
    res.append(("E34 séance lue un samedi : « pas un jour de bourse », avec le retard, code 2",
                c == 2 and "pas un jour de bourse" in l1 and f"{RETARD_SAMEDI} jour(s) de bourse de retard" in l1))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), cal="fin_proche"))
    ok10 = c == 0 and l1.startswith("⚠️") and "Calendrier de la Bourse à relever" in l1
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), cal="fin_29"))
    ok29 = "Calendrier de la Bourse à relever" in l1
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), cal="fin_31"))
    ok31 = c == 0 and "Calendrier de la Bourse à relever" not in l1
    res.append(("E35 calendrier qui finit dans 10 et 29 jours : ⚠️ « à relever », code 0 ; dans 31 jours : rien",
                ok10 and ok29 and ok31))
    c, l1, o = lancer(prog, monter(dos(), (V, o7), (J, o8), seance=(_J - timedelta(days=120)).isoformat()))
    res.append(("E36 séance antérieure à la couverture : « au moins N jour(s) de bourse de retard », N exact, sans plantage",
                c == 2 and f"au moins {N_COUVERTURE} jour(s) de bourse de retard" in l1 and "Traceback" not in o))
    try:
        s_reel = json.load(open(os.path.join(DEPOT, "donnees", "signaux_du_jour.json"), encoding="utf-8")).get("seance", "")
    except (OSError, ValueError, AttributeError):
        s_reel = ""
    c, l1, o = lancer(prog, DEPOT)
    res.append(("E10 chemin réel : code 0, 1 ou 2, et la séance du fichier annoncée",
                c in (0, 1, 2) and len(s_reel) == 10 and f"Séance lue : {s_reel[8:10]}-{s_reel[5:7]}" in o))
    return res


def main():
    """Joue les épreuves sans sabotage, puis chaque sabotage avec --saboter.

    ① RÔLE — Dire si les épreuves prouvent quelque chose.
    ② CONTEXTE D'APPEL — Le lancement du fichier.
    ③ ENTRÉE — La ligne de commande.
    ④ CONDITIONS D'ENTRÉE — La racine donnée doit porter le programme et programmes/CONTRATS_DES_FICHIERS.py.
    ⑤ SORTIE — UNE valeur : le code de sortie.
      [rend: 1]
    ⑥ TRAITEMENT — pour chaque cas : copier le programme et le module des contrats, saboter, jouer, compter les
      rouges.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une épreuve qui reste verte quand on retire ce qu'elle teste est une décoration (R-731).
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Crée puis efface des dossiers jetables ; affiche un compte rendu.
    ⑪ TERMINAISON — Rend la main par son code.
      [sort: non]
    """
    src = open(os.path.join(DEPOT, PROG), encoding="utf-8").read()
    choix = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
    bon = True
    for sab in choix:
        tmp = tempfile.mkdtemp(prefix="message_du_soir_")
        try:
            t = src
            for a, b in SABOTAGES[sab]:
                if t.count(a) != 1:
                    print(f"SABOTAGE {sab} INAPPLICABLE : ancre absente ou multiple")
                    return 2
                t = t.replace(a, b)
            prog = os.path.join(tmp, "MESSAGE_DU_SOIR.py")
            open(prog, "w", encoding="utf-8").write(t)
            shutil.copy(os.path.join(DEPOT, "programmes", "CONTRATS_DES_FICHIERS.py"), tmp)
            shutil.copy(os.path.join(DEPOT, "programmes", "CALENDRIER_DE_LA_BOURSE.py"), tmp)
            shutil.copy(os.path.join(DEPOT, "programmes", "FABRIQUER_LE_CIRCUIT_PUBLIC.py"), tmp)
            res = epreuves(prog, tmp)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        rouges = [x for x, ok in res if not ok]
        print(f"== {sab} : {len(res) - len(rouges)} vertes, {len(rouges)} rouges")
        for x in rouges:
            print("     ROUGE " + x)
        if sab == "Z0" and rouges:
            bon = False
        if sab != "Z0" and not rouges:
            print(f"     ⚠ LE SABOTAGE {sab} NE FAIT RIEN ROUGIR : épreuve sans dents")
            bon = False
    print("VERDICT :", "tout est conforme" if bon else "NON CONFORME")
    return 0 if bon else 1


if __name__ == "__main__":
    sys.exit(main())
