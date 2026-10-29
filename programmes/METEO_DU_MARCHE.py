#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MÉTÉO DU MARCHÉ — le voyant « moyenne des 200 séances » du CAC 40 (A-615). Simulation uniquement.

① RÔLE — Dire chaque soir où en est la bourse entière : le CAC 40 est-il AU-DESSUS (🟢) ou EN DESSOUS (🔴) de
  la moyenne de ses 200 dernières clôtures, depuis combien de séances, et est-il en zone de krach (20 % ou plus
  sous son plus haut d'un an). C'est un VOYANT, pas un ordre : il n'achète ni ne vend rien.
② CONTEXTE D'APPEL — Le circuit du soir (.github/workflows/collecte_abc.yml, pas « Calculer la meteo du
  marche »), après la collecte ; ou à la main. Décision de Jean-Luc du 29-10-2026 à 13h39 (« Faire la
  moyenne »), après l'étude etudes/PLAN_PREVOIR_ET_SE_PROTEGER_CAC40_INDICE_Mer_28-10-2026.
③ ENTRÉE — argv[1] : racine du dépôt · argv[2] facultatif : `sans_collecte` (ne va pas sur le réseau) ou
  `epreuves` (jeu d'épreuves interne, sur des copies, jamais sur la racine donnée).
④ CONDITIONS D'ENTRÉE — donnees/sources_indice/INDICE_CAC40.csv (historique figé depuis 2000) et
  donnees/CALENDRIER_EURONEXT.csv (lu par CALENDRIER_DE_LA_BOURSE) existent.
⑤ SORTIE — UN code de sortie : 0 si la météo est à jour et sûre · 2 sinon (page non lue, page incohérente,
  révision, série trouée, données en retard, erreur imprévue) — R-734 : un contrôle qui n'a pas tourné ne se tait
  pas. Écrit toujours le rapport et les deux fichiers de données, même vides.
  [rend: 1]
⑥ TRAITEMENT — ① lire la page de l'indice chez ABC (code PX1p) avec `telecharger` et `extraire` de
  COLLECTER_ABC_GITHUB (importés, jamais recopiés : R-708) · ② confronter la page : à l'historique figé (un écart
  > 0,1 % sur une séance commune) ET au fichier quotidien : UN SEUL désaccord et RIEN n'est écrit ce soir-là
  (relecture du 29-10-2026, tour 2 : sinon une page fausse s'écrit dès qu'elle ne recouvre plus l'historique) ;
  exiger au moins une séance commune ; refuser une variation de plus de 15 % d'une séance à l'autre · l'issue
  d'un blocage est une DÉCISION DE JEAN-LUC, lue dans donnees/meteo_decisions.csv (date, close retenue ou vide
  pour garder ABC, motif), comme A-231 pour les actions · ③ ajouter les séances neuves et sûres · ④ vérifier,
  DATE PAR DATE au calendrier d'Euronext, que les séances connues après l'historique sont exactement les jours
  de bourse jusqu'à la dernière séance close (ni trou, ni jour en trop, ni retard) · ⑤ calculer le voyant en un
  seul passage, ne l'afficher que si la série est sûre · ⑥ écrire le rapport et une ligne PAR PASSAGE qui
  apporte une séance nouvelle dans donnees/meteo_du_marche.csv.
⑦ UNITÉ — Points d'indice ; écarts en fraction (0,05 = 5 %) ; retards en JOURS DE BOURSE.
⑧ POURQUOI — Étude du 28-29-10-2026 : hors marché sous la moyenne des 200 séances, la pire baisse a été
  ramenée de −60 % à −37 % (2001-2016) et de −39 % à −17 % (2017-2023), pour un peu de rendement en moins, et
  a été pire en 2024-2026 sans krach (−27 % contre −17 %). Non prouvé statistiquement (5 krachs en 23 ans) :
  d'où un voyant de prudence, pas une règle automatique.
⑨ CE QUI CLOCHE — La page PX1p d'ABC n'a jamais été lue par ce programme (réseau fermé là où il a été écrit) :
  THÉORIQUE jusqu'au premier passage réel (BACKLOG). Le calendrier d'Euronext ne couvre que 2026 : à partir du
  02-01-2027 la continuité ne sera plus vérifiable et le voyant sortira en code 2 chaque soir tant que 2027
  n'est pas relevé (BACKLOG). Six séances de fin d'année n'ont que la source `bnains` et sont ignorées.
  La moyenne des 200 séances est aussi calculée dans l'étude : deux écritures d'un même calcul. Aucune reprise
  automatique si la page ne recouvre plus rien de connu (panne longue) : issue = décision de Jean-Luc (BACKLOG).
  Une page dont le volume s'écrit « - » serait ignorée par `extraire` : THÉORIQUE.
⑩ EFFET — Écrit rapports/meteo_du_marche.md, donnees/meteo_du_marche.csv, donnees/indice_cac40_quotidien.csv ;
  sort sur le réseau une fois (une page).
⑪ TERMINAISON — Rend toujours la main : le téléchargement a un délai de 30 secondes, toute erreur est
  rattrapée et écrite au rapport.
  [sort: oui]
"""
import sys, os, csv, shutil, tempfile, traceback
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo

CODE_ABC = 'PX1p'
SEANCES_MOYENNE = 200          # Faber (2007) ; demandé par Jean-Luc le 28-10-2026
SEANCES_PLUS_HAUT = 252        # un an de bourse
SEUIL_KRACH = -0.20            # décision de Jean-Luc du 28-10-2026 à 19h08
ECART_SOURCES = 0.001          # 0,1 % : deux sources de la même clôture ; l'historique diffère de bnains de 1,1 % au plus sur 12 séances
VARIATION_MAX = 0.15           # 15 % : la plus forte variation d'une séance depuis 2000 est −12,28 % (12-03-2020), mesuré le 29-10-2026
ENTETE_QUOTIDIEN = ['date', 'close', 'source']
ENTETE_METEO = ['date', 'cloture', 'moyenne_200', 'ecart', 'couleur', 'depuis', 'sous_plus_haut', 'krach']


def chemins(racine):
    """rend les chemins utilisés, tous sous la racine donnée — [rend: 1] [sort: non]"""
    j = lambda *p: os.path.join(racine, *p)
    return {'historique': j('donnees', 'sources_indice', 'INDICE_CAC40.csv'), 'quotidien': j('donnees', 'indice_cac40_quotidien.csv'),
            'meteo': j('donnees', 'meteo_du_marche.csv'), 'decisions': j('donnees', 'meteo_decisions.csv'),
            'rapport': j('rapports', 'meteo_du_marche.md'), 'programmes': j('programmes')}


def modules(racine):
    """importe COLLECTER_ABC_GITHUB et CALENDRIER_DE_LA_BOURSE du dépôt donné — [rend: 2] [sort: non]"""
    sys.path.insert(0, chemins(racine)['programmes'])
    import COLLECTER_ABC_GITHUB as ABC, CALENDRIER_DE_LA_BOURSE as K
    return ABC, K


def creer_si_absent(chemin, entete):
    """crée un CSV vide avec son en-tête (le circuit enregistre ce fichier chaque soir, il doit exister) ;
    ajoute un saut de ligne final s'il manque (sinon la ligne suivante se collerait). — [rend: 0] [sort: non]"""
    if not os.path.exists(chemin) or os.path.getsize(chemin) == 0:
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        with open(chemin, 'w', encoding='utf-8', newline='') as f: csv.writer(f).writerow(entete)
        return
    with open(chemin, 'rb') as f:
        f.seek(-1, 2); dernier = f.read(1)
    if dernier != b'\n':
        with open(chemin, 'a', encoding='utf-8') as f: f.write('\n')


def lire_serie(chemin, colonne):
    """lit {date: clôture} ; une ligne illisible LÈVE (rattrapé par `executer`, écrit au rapport) — [rend: 1] [sort: non]"""
    serie = {}
    with open(chemin, encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            if r.get(colonne) in (None, ''): continue
            date.fromisoformat(r['date'])
            serie[r['date']] = float(r[colonne])
    return serie


def lire_decisions(chemin):
    """{date: clôture retenue, ou None pour garder la valeur d'ABC} — décisions de Jean-Luc — [rend: 1] [sort: non]"""
    dec = {}
    if os.path.exists(chemin):
        with open(chemin, encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                date.fromisoformat(r['date'])
                dec[r['date']] = float(r['close']) if r.get('close') else None
    return dec


def derniere_seance_close(maintenant, ABC, K, cal):
    """la dernière séance de bourse close à l'heure donnée (aujourd'hui après la clôture, sinon avant) — [rend: 1] [sort: non]"""
    d = maintenant.date()
    if maintenant.hour < ABC.HEURE_CLOTURE_PARIS or not K.est_jour_de_bourse(d, cal):
        d -= timedelta(days=1)
        while not K.est_jour_de_bourse(d, cal): d -= timedelta(days=1)
    return d


def lire_page(ABC, maintenant, notes):
    """lit la page ABC de l'indice ; rend les séances closes [(date, clôture)], de la plus ancienne à la plus récente — [rend: 1] [sort: non]"""
    try:
        seances, note = ABC.extraire(ABC.telecharger(f'https://www.abcbourse.com/cotation/{CODE_ABC}'))
    except Exception as e:
        notes.append(f'❌ page {CODE_ABC} non lue : {e}'); return []
    if not seances:
        notes.append(f'❌ page {CODE_ABC} lue mais aucune séance extraite : {note}'); return []
    if maintenant.hour < ABC.HEURE_CLOTURE_PARIS:
        seances = [s for s in seances if s['date'] != maintenant.date().isoformat()]   # la séance du jour n'est pas close
    page = sorted((s['date'], float(s['close'])) for s in seances if s.get('close'))
    if not page: notes.append(f'❌ page {CODE_ABC} sans clôture'); return []
    notes.append(f'page {CODE_ABC} lue : {len(page)} séances, du {page[0][0]} au {page[-1][0]}')
    return page


ISSUE = ('issue : décision de Jean-Luc — inscrire la séance dans donnees/meteo_decisions.csv (colonnes date, close, motif ; '
         'close = la clôture retenue ; vide = séance nouvelle acceptée telle qu ABC la donne, ou séance connue qui n est plus contrôlée)')


def confronter(page, connu, decisions, notes):
    """rend les séances de la page à AJOUTER au fichier quotidien ; un seul désaccord et rien n'est rendu — [rend: 1] [sort: non]"""
    if not page: return []
    communes = [(d, x) for d, x in page if d in connu and d not in decisions]
    faux = [(d, connu[d], x) for d, x in communes if abs(x / connu[d] - 1) > ECART_SOURCES]
    if faux:
        notes.append('❌ LA PAGE CONTREDIT DES CLÔTURES DÉJÀ CONNUES — rien n est écrit ce soir : ' +
                     ' · '.join(f'{d} connue {a} contre ABC {b}' for d, a, b in faux[:5]) + f' ({len(faux)} séance(s)) — ' + ISSUE)
        return []
    if not communes:                     # une décision ne remplace jamais la vérification (relecture tour 3, A1)
        notes.append('❌ AUCUNE SÉANCE COMMUNE entre la page et ce qu on connaît : la page ne peut pas être vérifiée — rien n est écrit — ' + ISSUE)
        return []
    connu = dict(connu); ajout = []
    for d, x in page:
        if d in connu: continue
        if d in decisions:
            x = decisions[d] if decisions[d] is not None else x
        else:
            prec = [k for k in connu if k < d]
            v = x / connu[max(prec)] - 1 if prec else 0.0
            if abs(v) > VARIATION_MAX:
                notes.append(f'❌ VARIATION DE {v:+.2%} le {d} (au-delà de {VARIATION_MAX:.0%}) — cette séance et les suivantes ne sont pas écrites — ' + ISSUE)
                break
        ajout.append((d, x)); connu[d] = x
    notes.append(f'{len(communes)} séance(s) commune(s) vérifiée(s), {len(ajout)} ajoutée(s)')
    return ajout


def voyant(serie):
    """voyant de la dernière séance, en UN passage sur toute la série ; None si moins de 252 séances — [rend: 1] [sort: non]"""
    dates = sorted(serie)
    if len(dates) < SEANCES_PLUS_HAUT: return None
    c = [serie[d] for d in dates]
    somme, dessus = 0.0, []
    for k, x in enumerate(c):
        somme += x
        if k >= SEANCES_MOYENNE: somme -= c[k - SEANCES_MOYENNE]
        dessus.append(x > somme / SEANCES_MOYENNE if k >= SEANCES_MOYENNE - 1 else None)
    mm = somme / SEANCES_MOYENNE
    depuis = 0
    for x in reversed(dessus):
        if x is None or x != dessus[-1]: break
        depuis += 1
    haut = max(c[-SEANCES_PLUS_HAUT:])
    return {'date': dates[-1], 'cloture': c[-1], 'moyenne_200': mm, 'ecart': c[-1] / mm - 1, 'couleur': '🟢' if dessus[-1] else '🔴',
            'depuis': depuis, 'plus_haut_an': haut, 'sous_plus_haut': c[-1] / haut - 1, 'krach': c[-1] / haut - 1 <= SEUIL_KRACH}


def continuite(fin_histo, dates_apres, fin_attendue, K, cal, notes):
    """vrai si les dates connues après l'historique sont EXACTEMENT les jours de bourse jusqu'à `fin_attendue` — [rend: 1] [sort: non]"""
    attendues, d = set(), date.fromisoformat(fin_histo)
    while d < fin_attendue:
        d += timedelta(days=1)
        if K.est_jour_de_bourse(d, cal): attendues.add(d.isoformat())
    connues = set(dates_apres)
    manquent = sorted(attendues - connues); en_trop = sorted(connues - attendues)
    if manquent: notes.append(f'❌ SÉANCES MANQUANTES ({len(manquent)}) : {", ".join(manquent[:8])}{" …" if len(manquent) > 8 else ""} — voyant non calculable')
    if en_trop: notes.append(f'❌ SÉANCES EN TROP, absentes du calendrier d Euronext : {", ".join(en_trop[:8])} — voyant non calculable')
    return not manquent and not en_trop


def executer(racine, collecte, maintenant):
    """tout le passage, à l'heure `maintenant` (Paris) ; rend le code de sortie — [rend: 1] [sort: non]"""
    P = chemins(racine); notes = []
    lignes = [f'# MÉTÉO DU MARCHÉ — {maintenant.strftime("%d-%m-%Y %Hh%M")} (Paris)', '', 'Voyant de prudence, pas un ordre. Simulation uniquement.', '']
    try:
        creer_si_absent(P['quotidien'], ENTETE_QUOTIDIEN); creer_si_absent(P['meteo'], ENTETE_METEO)
        ABC, K = modules(racine); cal = K.lire(racine)
        histo = lire_serie(P['historique'], 'yahoo'); quot = lire_serie(P['quotidien'], 'close')
        decisions = lire_decisions(P['decisions'])
        fin_h = max(histo)
        connu = dict(histo); connu.update(quot); connu.update({d: x for d, x in decisions.items() if x is not None and d in connu})
        if collecte:
            ajout = confronter(lire_page(ABC, maintenant, notes), connu, decisions, notes)
            if ajout:
                with open(P['quotidien'], 'a', encoding='utf-8', newline='') as f:
                    w = csv.writer(f)
                    for d, x in ajout: w.writerow([d, x, 'abc']); quot[d] = x
        quot.update({d: x for d, x in decisions.items() if x is not None and d in quot})
        apres = {d: x for d, x in quot.items() if d > fin_h}
        serie = dict(histo); serie.update(apres)
        sure = continuite(fin_h, apres, derniere_seance_close(maintenant, ABC, K, cal), K, cal, notes)
        v = voyant(serie) if sure else None
        if not sure:
            lignes.append('❌ **Voyant non calculable ce soir : la série des cours n est pas complète (voir les contrôles).**')
        elif v is None:
            notes.append('❌ moins de 252 séances')
        else:
            lignes += [f'**{v["couleur"]} CAC 40 {"AU-DESSUS" if v["couleur"] == "🟢" else "EN DESSOUS"} de sa moyenne des 200 séances**, depuis {v["depuis"]} séance(s).', '',
                       f'- Séance du {v["date"]} : clôture {v["cloture"]:.2f} · moyenne 200 séances {v["moyenne_200"]:.2f} · écart {v["ecart"]:+.2%}',
                       f'- Plus haut d un an : {v["plus_haut_an"]:.2f} · le CAC est à {v["sous_plus_haut"]:+.2%} de ce plus haut'
                       + (' · 🚨 ZONE DE KRACH (20 % ou plus sous le plus haut)' if v['krach'] else ''), '',
                       'Ce que dit l étude (29-10-2026) : sous la moyenne, la pire baisse a été réduite en 2008 et 2020, '
                       'mais le voyant change souvent de couleur hors krach et n est pas prouvé statistiquement.']
            with open(P['meteo'], encoding='utf-8') as f: deja = {r['date'] for r in csv.DictReader(f)}
            if v['date'] not in deja:
                with open(P['meteo'], 'a', encoding='utf-8', newline='') as f:
                    csv.writer(f).writerow([v['date'], f'{v["cloture"]:.2f}', f'{v["moyenne_200"]:.2f}', f'{v["ecart"]:.4f}',
                                            'vert' if v['couleur'] == '🟢' else 'rouge', v['depuis'], f'{v["sous_plus_haut"]:.4f}', int(v['krach'])])
    except Exception as e:
        notes.append(f'❌ ERREUR IMPRÉVUE : {type(e).__name__} : {e}')
        notes.append('```\n' + traceback.format_exc() + '```')
    lignes += ['', '## Contrôles'] + [f'- {n}' for n in notes or ['collecte non demandée (sans_collecte)']]
    os.makedirs(os.path.dirname(P['rapport']), exist_ok=True)
    with open(P['rapport'], 'w', encoding='utf-8') as f: f.write('\n'.join(lignes) + '\n')
    print('\n'.join(lignes))
    return 2 if any(n.startswith('❌') for n in notes) else 0


def epreuves(racine):
    """jeu d'épreuves interne (R-731). Valeurs attendues venues d'un calcul INDÉPENDANT (pandas, 29-10-2026) ;
    pages simulées ; heure FIXÉE, calculée depuis la fin de l'historique (jamais l'horloge réelle) ; chaque cas dans
    un dossier temporaire effacé même en cas d'échec. — [rend: 1] [sort: non]"""
    echecs = []
    def ok(cond, txt):
        print(('OK — ' if cond else 'ÉCHEC — ') + txt)
        if not cond: echecs.append(txt)
    P0 = chemins(racine); histo = lire_serie(P0['historique'], 'yahoo')
    attendu = {'2026-10-02': (8238.20, -0.0414, '🔴', 18, -0.0950), '2020-03-16': (5654.96, -0.3136, '🔴', 13, -0.3649),
               '2006-06-05': (4804.65, 0.0232, '🟢', 413, -0.0746), '2008-10-06': (4684.24, -0.2076, '🔴', 237, -0.3669)}
    for J, (mm, ec, coul, dep, sph) in attendu.items():
        v = voyant({d: x for d, x in histo.items() if d <= J})
        ok(abs(v['moyenne_200'] - mm) < 0.01 and abs(v['ecart'] - ec) < 5e-5 and v['couleur'] == coul and v['depuis'] == dep and abs(v['sous_plus_haut'] - sph) < 5e-5,
           f'E1 {J} : moyenne {v["moyenne_200"]:.2f}/{mm} · écart {v["ecart"]:.4f}/{ec} · {v["couleur"]}/{coul} · depuis {v["depuis"]}/{dep} · sous le plus haut {v["sous_plus_haut"]:.4f}/{sph}')
    ok(voyant({d: x for d, x in histo.items() if d <= '2020-03-16'})['krach'], 'E1 16-03-2020 en zone de krach')
    ABC, K = modules(racine); cal = K.lire(racine)
    fin = max(histo); dates = sorted(histo); suite, d = [], date.fromisoformat(fin)
    while len(suite) < 8:
        d += timedelta(days=1)
        if K.est_jour_de_bourse(d, cal): suite.append(d.isoformat())
    def heure(jour, h): return datetime.fromisoformat(f'{jour}T{h:02d}:00').replace(tzinfo=ZoneInfo('Europe/Paris'))
    def page(seances): return [{'date': d, 'close': x} for d, x in sorted(seances, reverse=True)]
    base = [(d, histo[d]) for d in dates[-3:]]
    neuves = [(d, histo[fin] * (1 + 0.001 * k)) for k, d in enumerate(suite[:5], 1)]
    soir = heure(suite[4], 20)
    vrais = (ABC.telecharger, ABC.extraire)
    def cas(nom, pg, maintenant, quotidien=(), decisions=(), erreur=None, collecte=True, illisible=False):
        tmp = tempfile.mkdtemp()
        try:
            for p in ('donnees/sources_indice/INDICE_CAC40.csv', 'donnees/CALENDRIER_EURONEXT.csv'):
                os.makedirs(os.path.dirname(os.path.join(tmp, p)), exist_ok=True); shutil.copy(os.path.join(racine, p), os.path.join(tmp, p))
            os.symlink(P0['programmes'], os.path.join(tmp, 'programmes'))
            P = chemins(tmp)
            if quotidien or illisible:
                creer_si_absent(P['quotidien'], ENTETE_QUOTIDIEN)
                with open(P['quotidien'], 'a', encoding='utf-8', newline='') as f:
                    for d, x in quotidien: csv.writer(f).writerow([d, x, 'abc'])
                    if illisible: f.write('pas-une-date,abc,abc\n')
            if decisions:
                with open(P['decisions'], 'w', encoding='utf-8', newline='') as f:
                    w = csv.writer(f); w.writerow(['date', 'close', 'motif'])
                    for d, x in decisions: w.writerow([d, '' if x is None else x, 'épreuve'])
            def tel(url, e=erreur):
                if e: raise e
                return 'page'
            ABC.telecharger = tel; ABC.extraire = lambda h, p=pg: (p, '' if p else 'aucune ligne')
            code = executer(tmp, collecte, maintenant)
            n_q = len(lire_serie(P['quotidien'], 'close')) if not illisible else -1
            n_m = len(lire_serie(P['meteo'], 'cloture'))
            q = lire_serie(P['quotidien'], 'close') if not illisible else {}
            return code, n_q, n_m, q, open(P['rapport'], encoding='utf-8').read()
        finally:
            ABC.telecharger, ABC.extraire = vrais
            shutil.rmtree(tmp, ignore_errors=True)
    c, nq, nm, q, r = cas('saine', page(base + neuves), soir)
    ok(c == 0 and nq == 5 and nm == 1 and ('AU-DESSUS' in r or 'EN DESSOUS' in r), f'E2 page saine à jour : code {c} (0), {nq} séances (5), {nm} ligne de météo (1)')
    c, nq, nm, q, r = cas('18h07', page(base + neuves), heure(suite[4], 18).replace(minute=7))
    ok(c == 0 and nq == 5 and nm == 1, f'E2b passage réel du circuit à 18h07 : code {c} (0), {nq} séances (5), {nm} ligne de météo (1)')
    c, nq, nm, q, r = cas('page fausse et décision isolée', page([(d, x * 1.02) for d, x in neuves[2:]] + [(suite[5], neuves[-1][1] * 1.02)]),
                          heure(suite[5], 20), quotidien=neuves, decisions=[(suite[2], None), (suite[3], None), (suite[4], None)])
    ok(c == 2 and nq == 5, f'E5b page fausse dont toutes les séances connues portent une décision vide : code {c} (2), rien écrit ({nq} séances, 5)')
    c, nq, nm, q, r = cas('avant 18h', page(base + neuves), heure(suite[4], 15))
    ok(c == 0 and nq == 4 and suite[4] not in q, f'E3 avant 18h : la séance du jour est retirée — code {c} (0), {nq} séances (4)')
    c, nq, nm, q, r = cas('retard', page(base + neuves), heure(suite[7], 20))
    ok(c == 2 and nm == 0 and 'SÉANCES MANQUANTES' in r and 'AU-DESSUS' not in r and 'EN DESSOUS' not in r, f'E4 en retard de 3 séances : code {c} (2), voyant non affiché, {nm} ligne de météo (0)')
    rev = page(base[-1:] + neuves[:-1] + [(neuves[-1][0], neuves[-1][1] * 1.03)] + [(suite[5], neuves[-1][1])])
    c, nq, nm, q, r = cas('désaccord', [s for s in rev if s['date'] > fin], heure(suite[5], 20), quotidien=neuves)
    ok(c == 2 and nq == 5 and suite[5] not in q and abs(q[neuves[-1][0]] - neuves[-1][1]) < 1e-9 and 'CONTREDIT' in r,
       f'E5 page qui contredit le fichier quotidien (sans aucune séance de l historique) : code {c} (2), rien écrit ({nq} séances, 5), valeur d origine gardée')
    c, nq, nm, q, r = cas('désaccord tranché', [s for s in rev if s['date'] > fin], heure(suite[5], 20), quotidien=neuves, decisions=[(neuves[-1][0], neuves[-1][1] * 1.03)])
    ok(c == 0 and nq == 6 and nm == 1, f'E6 désaccord tranché par une décision de Jean-Luc : code {c} (0), {nq} séances (6), {nm} ligne de météo (1)')
    samedi = next(dd for dd in (date.fromisoformat(suite[0]) + timedelta(days=k) for k in range(1, 10)) if dd.weekday() == 5).isoformat()
    trou = [x for x in neuves if x[0] != suite[1]] + [(samedi, neuves[0][1])]
    c, nq, nm, q, r = cas('samedi', [], soir, quotidien=trou, collecte=False)
    ok(c == 2 and nm == 0 and 'EN TROP' in r and 'MANQUANTES' in r, f'E7 un samedi en trop et un jour de bourse manquant (même nombre) : code {c} (2), {nm} ligne de météo (0)')
    for nom, pg, err in [('vide', [], None), ('réseau 403', None, Exception('HTTP Error 403')),
                         ('mauvaise colonne', page([(d, x / 1000) for d, x in base + neuves]), None),
                         ('écart de 2 % avec l historique', page([(d, x * 1.02) for d, x in base] + neuves), None),
                         ('sans séance commune', page(neuves[2:]), None),
                         ('variation de 40 %', page(base + [(suite[0], histo[fin] * 0.6)]), None)]:
        c, nq, nm, q, r = cas(nom, pg, soir, erreur=err)
        ok(c == 2 and nq == 0 and nm == 0 and '❌' in r, f'E8 {nom} : code {c} (2), {nq} séances écrites (0), {nm} ligne de météo (0)')
    c, nq, nm, q, r = cas('variation acceptée', page(base + [(suite[0], histo[fin] * 0.6)]), heure(suite[0], 20), decisions=[(suite[0], None)])
    ok(c == 0 and nq == 1, f'E9 variation de 40 % acceptée par une décision de Jean-Luc : code {c} (0), {nq} séance écrite (1)')
    c, nq, nm, q, r = cas('illisible', [], soir, collecte=False, illisible=True)
    ok(c == 2 and 'ERREUR IMPRÉVUE' in r, f'E10 ligne illisible : code {c} (2), rapport écrit avec l erreur')
    print(f'\nÉPREUVES DE LA MÉTÉO : {len(echecs)} échec(s)')
    return 2 if echecs else 0


def main():
    """lit la ligne de commande et lance le passage (à l'heure réelle de Paris) ou les épreuves — [rend: 0] [sort: oui]"""
    racine = sys.argv[1] if len(sys.argv) > 1 else '.'
    mode = sys.argv[2] if len(sys.argv) > 2 else ''
    if mode == 'epreuves': sys.exit(epreuves(racine))
    sys.exit(executer(racine, mode != 'sans_collecte', datetime.now(ZoneInfo('Europe/Paris'))))


if __name__ == '__main__':
    main()
