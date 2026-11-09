#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPREUVES_DE_LA_VERSION_DU_REGISTRE — Lun 28-09-2026 (Paris)
DÉCIDÉ · Rôle : prouver que le pilote annonce la version du registre lue en pied de page, et que l'épreuve a des dents.
Quand l'appeler : avant toute livraison qui touche la lecture du registre dans programmes/claude_FABRIQUER_LE_PILOTE.py (R-755 ②).

À QUOI ÇA SERT. gouvernance/PILOTE.md, lu à chaque début de session, annonçait « version du registre : 4.0 »
pour un registre en v6.8 (A-435 ①, relevé le 19-09-2026 ; encore vrai le 28-09-2026). Le programme prenait le
premier « vN.N » des 400 premiers caractères du registre — c'est-à-dire l'avertissement qui dit que la
version se lit en pied de page, et qui cite « v4.0 » comme contre-exemple. Réparé : la version se lit sur la
dernière occurrence, dans tout le texte, du titre du registre suivi d'une virgule et de sa version
(« REGISTRE DES RÈGLES …, vN.N ») — et non
sur la dernière ligne non vide, première réparation, cassée par le relecteur parce qu'une ligne posée après le
pied de page la trompait (texte corrigé le 30-09-2026, A-495 (j)). Calibré sur l'histoire du registre au dépôt,
le 28-09-2026 : ses six dernières versions enregistrées
portent en pied de page v6.8, v6.8, v6.8, v6.8, v6.7, v6.6.

LES ÉPREUVES, sur une copie du dépôt dont le registre est remplacé : E1, un registre qui cite « v4.0 » en tête
et porte « v9.9 » en pied de page → le pilote annonce 9.9 ; E2, un pied de page sans version → « ? », jamais
un chiffre pris ailleurs ; E3, une annexe citant « v5.3 » et une ligne de contrôle du garde-fou posées
après le pied → 9.9 ; E4, un ancien pied de page « …, v1.0 » cité plus haut dans le texte → 9.9, la dernière
occurrence (ajoutée le 30-09-2026 : aucune épreuve ne posait deux occurrences, relecteur). S1 remet la lecture des
400 premiers caractères ; S2, celle de la dernière ligne non vide (première réparation, cassée par le relecteur :
une ligne posée après le pied la trompait) ; S3 prend la première occurrence au lieu de la dernière.

AJOUT DU 04-11-2026 (lot G, réparation R5 demandée par le superviseur R-759 le 04-11-2026 à 19h22) —
DEUX PROPRIÉTÉS DU REGISTRE LUI-MÊME, vérifiées sur le vrai `gouvernance/REGISTRE_REGLES.md` de la racine :
U, UNICITÉ — un numéro de règle n'ouvre qu'une seule règle, quelle que soit sa graphie (fonction
`ouvertures`) ; R, RENVOIS — une règle déclarée REMPLACÉE par une autre porte une note qui renvoie à
celle-ci, toute note « REMPLACÉE … par R-nnn » renvoie à une règle qui existe, et toute règle citée par
une règle NON FIGÉE existe (fonction `renvois`). Raison : le 04-11-2026, un doublon de R-505 écrit avec
un tiret insécable, une puce « * » ou une puce en retrait passait l'unicité de l'auteur, et aucun outil
rejouable du dépôt ne vérifiait les renvois (relecture du lot G, U1 à U3, R1, R2) ; ces contrôles
vivaient au scratchpad, hors du dépôt, où ni Cowork ni le circuit ne peuvent les rejouer.
Avec --saboter, sept registres sabotés doivent rougir (U0 doublon ordinaire, U1 tiret U+2011, U2 puce
« * », U3 puce en retrait, U4 tiret U+2010, U5 puce numérotée « 1. », R1 R-502bis sans sa note de
renvoi, R2 R-505 qui cite R-514, qui n'existe pas) et un témoin doit rester vert (T1 une mention de
R-505 dans le corps d'une phrase).
CE QUI N'EST PAS COUVERT (dit, pas caché) : un doublon écrit dans une citation « > », ou comme puce sous
un titre de niveau 3 ou plus (là, une puce est une mention : listes « règles touchées ») ; une règle
remplacée qui n'est déclarée REMPLACÉE dans la liste d'aucune autre règle ; une décision de la SECTION 0
(« SECTION 0-D6 ») déclarée REMPLACÉE, qui n'est pas une règle ouverte ; un doublon écrit SANS gras ni
titre (« - R-505 … ») : une ouverture se reconnaît à sa marque d'emphase, et une puce sans emphase est
lue comme une mention (sabotage S6 de la relecture T3 du lot G, 04-11-2026 : VERT ; mesuré le même
jour : les 180 ouvertures du registre, 140 puces en gras et 40 titres, suivent la convention).

USAGE : python3 tests/EPREUVES_DE_LA_VERSION_DU_REGISTRE_Lun_28-09-2026.py <racine du dépôt> [--saboter] [--registre-seul]
  --registre-seul : ne lance que les contrôles U et R (sans refabriquer le pilote, qui copie le dépôt).
CODE : 0 si Z0 est vert, si U et R sont verts sur le vrai registre et, avec --saboter, si chaque
sabotage fait rougir au moins une épreuve et le témoin reste vert ; 1 sinon ; 2 si le registre est absent.
"""
import os, re, shutil, subprocess, sys, tempfile, unicodedata

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
DEPOT = os.path.abspath(_args[0] if _args else ".")

NUMERO_DE_REGLE = re.compile(r"(?:R|I)-\d+(?:bis|ter)?\b|GRILLE-(?!D\d)[0-9A-Z]+(?:-[0-9A-Z]+)*\b")
MARQUEUR_DE_LISTE = re.compile(r"\d+[.)]\s")
REF = r"((?:R|I)-\d+(?:bis|ter)?|GRILLE-(?!D\d)[0-9A-Z]+(?:-[0-9A-Z]+)*)"
NOTE_DE_RENVOI = re.compile(r"REMPLACÉE?S?\**\s+(?:le\s+\S+\s+)?par\s+(?:la\s+|le\s+)?\**\s*" + REF + r"\b")


def forme_canonique(ligne):
    """Rend la ligne ramenée à sa forme canonique, en deux morceaux : le préfixe retiré et le reste.

    ① RÔLE — Ramener une ligne à une forme où toutes les graphies d'un même début se confondent.
    ② CONTEXTE D'APPEL — `ouvertures`, pour chaque ligne du registre.
    ③ ENTRÉE — `ligne` : une ligne du registre.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : le préfixe retiré (texte) ; le reste de la ligne (texte).
      [rend: 2]
    ⑥ TRAITEMENT — NFKC ; tout caractère de la catégorie Unicode Pd (tirets) devient « - » ; puis,
      tant que possible, retirer en tête tout ce qui n'est ni lettre ni chiffre, et un marqueur de
      liste numérotée « 1. » ou « 1) ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Avis du superviseur du 04-11-2026 : énumérer les graphies connues laisse passer la
      suivante (U+2010, liste numérotée, __gras__) ; une forme canonique les couvre par propriété.
    ⑨ CE QUI CLOCHE — Une lettre d'une autre écriture qui ressemble à « R » (cyrillique) n'est pas
      ramenée à « R » par NFKC : un tel doublon passerait.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    l = unicodedata.normalize("NFKC", ligne)
    l = "".join("-" if unicodedata.category(c) == "Pd" else c for c in l)
    i = 0
    while True:
        while i < len(l) and not l[i].isalnum():
            i += 1
        m = MARQUEUR_DE_LISTE.match(l, i)
        if not m:
            break
        i = m.end()
    return l[:i], l[i:]


def ouvertures(texte):
    """Rend la liste des ouvertures de règle : (numéro, numéro de ligne), dans l'ordre du texte.

    ① RÔLE — Dire quelles lignes ouvrent une règle, quelle que soit leur graphie.
    ② CONTEXTE D'APPEL — `controler_le_registre` et `renvois`.
    ③ ENTRÉE — `texte` : le texte entier du registre.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : liste de (numéro de règle, numéro de ligne).
      [rend: 1]
    ⑥ TRAITEMENT — Pour chaque ligne, forme canonique ; le premier jeton est-il un numéro de règle ?
      Un TITRE Markdown dont le premier jeton est un numéro ouvre cette règle ; un titre de niveau 3
      ou plus sans numéro ouvre une zone où les puces sont des mentions ; un titre de niveau 1 ou 2
      (une SECTION) ouvre une zone où les puces ouvrent des règles. Hors titre, une ligne ouvre une
      règle si son préfixe retiré finit par une marque d'emphase (« ** », « __ », « * », « _ »),
      ne contient pas « > » (citation), et si elle n'est pas, en retrait, une mention d'une AUTRE
      règle à l'intérieur de la règle en cours ; une ligne en retrait qui commence par la règle en
      cours elle-même est une seconde ouverture de cette règle.
    ⑦ UNITÉ — Des lignes.
    ⑧ POURQUOI — Le motif du pilote prend pour doublons les listes « règles touchées » (20 faux
      doublons le 04-11-2026) ; ces listes sont des puces sous un titre de règle, ou des puces en
      retrait qui nomment d'autres règles.
    ⑨ CE QUI CLOCHE — Voir l'en-tête, « CE QUI N'EST PAS COUVERT ».
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    out, cur, mode = [], None, None
    for n, ligne in enumerate(texte.split("\n"), 1):
        pre, reste = forme_canonique(ligne)
        m = NUMERO_DE_REGLE.match(reste)
        tok = m.group(0) if m else None
        h = re.match(r"\s{0,3}(#{1,6})\s", ligne)
        if h:
            if tok:
                out.append((tok, n))
                cur, mode = tok, "titre"
            else:
                cur, mode = None, ("titre" if len(h.group(1)) >= 3 else None)
            continue
        if not tok or ">" in pre or not re.search(r"(\*\*|__|\*|_)\s*$", pre) or mode == "titre":
            continue
        if ligne[:1].isspace() and cur and tok != cur:
            continue
        out.append((tok, n))
        cur, mode = tok, "puce"
    return out


def renvois(texte, ouv):
    """Rend la liste des fautes de renvoi du registre.

    ① RÔLE — Vérifier que les remplacements et les citations des règles NON FIGÉES tiennent.
    ② CONTEXTE D'APPEL — `controler_le_registre`.
    ③ ENTRÉE — `texte` : le registre · `ouv` : la sortie de `ouvertures`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : liste de textes, une faute chacun.
      [rend: 1]
    ⑥ TRAITEMENT — (1) Toute note « REMPLACÉE … par R-nnn » renvoie à une règle ouverte. (2) Dans le
      bloc d'une règle Y, une puce dont une clause porte « **REMPLACÉE** » déclare remplacées les
      règles nommées avant la marque dans cette clause ; chacune (autre que Y) doit porter dans son
      propre bloc une note « REMPLACÉE … par Y ». (3) Toute règle citée dans le bloc d'une règle
      dont la ligne d'ouverture porte « NON FIGÉE » est ouverte au registre. Le bloc d'une règle va
      de son ouverture à l'ouverture ou au titre suivant.
    ⑦ UNITÉ — Des renvois.
    ⑧ POURQUOI — « Toute règle marquée REMPLACÉE porte un renvoi vers une règle qui existe » (avis du
      superviseur du 04-11-2026) ; sans (2), retirer la note d'une règle remplacée ne rougit rien.
    ⑨ CE QUI CLOCHE — (3) ne vaut que pour les règles NON FIGÉES : les anciennes règles citent des
      numéros jamais écrits (R-511 cite R-212, « annoncée mais jamais écrite »). « GRILLE-Dnn » est un
      préfixe d'espace (une divergence de la grille du 31-10-2026, avis du superviseur), pas une
      règle : le motif des numéros l'écarte.
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    lignes = texte.split("\n")
    noms = {k for k, _ in ouv}
    debuts = {}
    for k, n in ouv:
        debuts.setdefault(k, n)
    titres = [n for n, l in enumerate(lignes, 1) if re.match(r"\s{0,3}#{1,6}\s", l)]
    bornes = sorted({n for _, n in ouv} | set(titres) | {len(lignes) + 1})

    def bloc(k):
        """Rend les lignes du bloc de la règle k et le numéro de sa première ligne.

        ① RÔLE — Délimiter une règle. ② CONTEXTE D'APPEL — `renvois`.
        ③ ENTRÉE — `k` : un numéro de règle ouvert. ④ CONDITIONS D'ENTRÉE — `k` est dans `debuts`.
        ⑤ SORTIE — DEUX valeurs : la liste des lignes ; le numéro de la première.
          [rend: 2]
        ⑥ TRAITEMENT — de la première ouverture de k à l'ouverture ou au titre suivant.
        ⑦ UNITÉ — Des lignes. ⑧ POURQUOI — une note de renvoi se cherche dans le bloc de la règle.
        ⑨ CE QUI CLOCHE — seule la première ouverture compte : un doublon est déjà une faute U.
        ⑩ EFFET — — ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        n = debuts[k]
        fin = next(b for b in bornes if b > n)
        return lignes[n - 1:fin - 1], n
    fautes = []
    for n, l in enumerate(lignes, 1):
        for m in NOTE_DE_RENVOI.finditer(l):
            if m.group(1) not in noms:
                fautes.append(f"ligne {n} : note de remplacement qui renvoie à {m.group(1)}, absente")
    for y in debuts:
        corps, n0 = bloc(y)
        for j, l in enumerate(corps):
            if re.match(r"\s+[·\-*]\s", l) and "**REMPLAC" in l:
                for clause in l.split(";"):
                    mm = re.search(r"\*\*REMPLACÉE?S?\*\*", clause)
                    for x in (re.findall(REF, clause[:mm.start()]) if mm else []):
                        if x != y and x in debuts and not any(
                                q.group(1) == y for q in NOTE_DE_RENVOI.finditer("\n".join(bloc(x)[0]))):
                            fautes.append(f"ligne {n0 + j} : {x} déclarée REMPLACÉE par {y}, sans note de renvoi vers {y}")
        if "NON FIGÉE" in corps[0]:
            for j, l in enumerate(corps):
                for x in re.findall(r"(?<![\w-])" + REF + r"\b", l):
                    if x not in noms:
                        fautes.append(f"ligne {n0 + j} : {y} cite {x}, qui n'ouvre aucune règle")
    return fautes


def controler_le_registre(texte):
    """Rend la liste des fautes d'unicité et de renvoi du registre (vide = vert).

    ① RÔLE — Réunir les deux propriétés U et R.
    ② CONTEXTE D'APPEL — Corps de l'épreuve : vrai registre, puis registres sabotés.
    ③ ENTRÉE — `texte` : le registre.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : liste de textes.
      [rend: 1]
    ⑥ TRAITEMENT — `ouvertures` ; tout numéro qui ouvre plus d'une ligne est une faute U ; puis
      `renvois`.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir l'en-tête, « AJOUT DU 04-11-2026 ».
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    ouv = ouvertures(texte)
    vus = {}
    for k, n in ouv:
        vus.setdefault(k, []).append(n)
    fautes = [f"{k} ouvre {len(v)} règles (lignes {v})" for k, v in vus.items() if len(v) > 1]
    return fautes + renvois(texte, ouv)
PIL = "programmes/claude_FABRIQUER_LE_PILOTE.py"
SABOTAGES = {
    "Z0": [],
    "S1_quatre_cents_premiers_caracteres": [(PIL, '        c["version du registre"] = _pieds[-1] if _pieds else "?"',
                                             '        c["version du registre"] = (re.findall(r"v(\\d+\\.\\d+)", t[:400]) or ["?"])[0]')],
    "S2_derniere_ligne_non_vide": [(PIL, '        c["version du registre"] = _pieds[-1] if _pieds else "?"',
                                    '        c["version du registre"] = (re.findall(r"\\bv(\\d+\\.\\d+)\\b", [x for x in t.split("\\n") if x.strip()][-1]) or ["?"])[0]')],
    # S3 (relecteur du 30-09-2026) : la PREMIÈRE occurrence du titre suivi d'une version, au lieu de la dernière.
    "S3_premiere_occurrence": [(PIL, '        c["version du registre"] = _pieds[-1] if _pieds else "?"',
                                '        c["version du registre"] = _pieds[0] if _pieds else "?"')],
}
TETE = ("# REGISTRE DES RÈGLES DE L'ÉCOSYSTÈME CAC 40\n>\n> LA VERSION SE LIT EN PIED DE PAGE. Corrigé le 13-09-2026 : "
        "cette ligne portait « v4.0 » quand le pied de page portait « v4.4 ».\n\n- **R-722** — texte.\n")


def version(sab, pied):
    d = tempfile.mkdtemp(prefix="version_registre_")
    try:
        r = os.path.join(d, "r")
        shutil.copytree(DEPOT, r, ignore=shutil.ignore_patterns(".git", "_site_travail", "__pycache__"))
        for f, a, b in SABOTAGES[sab]:
            p = os.path.join(r, f)
            t = open(p, encoding="utf-8").read()
            assert t.count(a) == 1, (sab, a[:50])
            with open(p, "w", encoding="utf-8") as h:
                h.write(t.replace(a, b))
        with open(os.path.join(r, "gouvernance", "REGISTRE_REGLES.md"), "w", encoding="utf-8") as h:
            h.write(TETE + "\n\n" + pied + "\n\n")
        sortie = os.path.join(d, "pilote.md")
        subprocess.run([sys.executable, PIL, ".", sortie], cwd=r, capture_output=True, text=True, timeout=900)
        m = re.search(r"\| version du registre \| \*\*([^*]*)\*\* \|", open(sortie, encoding="utf-8").read()) \
            if os.path.exists(sortie) else None
        return m.group(1) if m else "(pilote non écrit)"
    finally:
        shutil.rmtree(d, ignore_errors=True)


_faute = False
_chemin_registre = os.path.join(DEPOT, "gouvernance", "REGISTRE_REGLES.md")
if not os.path.isfile(_chemin_registre):
    print("IMPOSSIBLE : registre absent :", _chemin_registre)
    sys.exit(2)
_REG = open(_chemin_registre, encoding="utf-8").read()
_vrai = controler_le_registre(_REG)
print(f"== U et R sur le vrai registre : {'VERT' if not _vrai else 'ROUGE'}")
for _f in _vrai:
    print("     ROUGE", _f)
_faute = bool(_vrai)
if "--saboter" in sys.argv:
    _avant = "\n- **R-506**"
    _note = " → **REMPLACÉE le 04-11-2026 par R-505 ⑤**"
    _ouv505 = "- **R-505** ("
    for _a in (_avant, _note, _ouv505):
        assert _REG.count(_a) == 1, _a
    _cas = [("U0 doublon de R-505, tiret ordinaire", _REG.replace(_avant, "\n- **R-505** DOUBLON" + _avant), True),
            ("U1 doublon de R-505, tiret insécable U+2011", _REG.replace(_avant, "\n- **R‑505** DOUBLON" + _avant), True),
            ("U2 doublon de R-505, puce « * »", _REG.replace(_avant, "\n* **R-505** DOUBLON" + _avant), True),
            ("U3 doublon de R-505, puce en retrait", _REG.replace(_avant, "\n  - **R-505** DOUBLON" + _avant), True),
            ("U4 doublon de R-505, tiret U+2010", _REG.replace(_avant, "\n- **R‐505** DOUBLON" + _avant), True),
            ("U5 doublon de R-505, puce numérotée « 1. »", _REG.replace(_avant, "\n1. **R-505** DOUBLON" + _avant), True),
            ("R1 R-502bis sans sa note de renvoi", _REG.replace(_note, ""), True),
            ("R2 R-505 cite R-514, qui n'existe pas", _REG.replace(_ouv505, "- **R-505** (voir R-514 ; "), True),
            ("T1 témoin : R-505 mentionnée dans le corps d'une phrase", _REG.replace(_avant, "\n  La règle R-505 est citée ici." + _avant), False)]
    for _nom, _t, _doit in _cas:
        _f = controler_le_registre(_t)
        _ok = bool(_f) == _doit
        _faute = _faute or not _ok
        print(f"== {_nom} : {'ROUGE' if _f else 'VERT'}" + ("" if _ok else "  <-- SABOTAGE NON VU" if _doit else "  <-- ATTENDU : VERT")
              + (f" · {_f[0]}" if _f else ""))
if "--registre-seul" in sys.argv:
    print("VERDICT :", "tout est conforme" if not _faute else "ECHEC — voir ci-dessus")
    sys.exit(1 if _faute else 0)

_choix = list(SABOTAGES) if "--saboter" in sys.argv else ["Z0"]
for sab in _choix:
    v1 = version(sab, "*Lun 28-09-2026 03h00 (Paris) — REGISTRE DES RÈGLES DE L'ÉCOSYSTÈME CAC 40, v9.9 · révisé le 28-09-2026*")
    v2 = version(sab, "*Lun 28-09-2026 03h00 (Paris) — REGISTRE DES RÈGLES DE L'ÉCOSYSTÈME CAC 40 · révisé le 28-09-2026*")
    v3 = version(sab, "*Lun 28-09-2026 03h00 (Paris) — REGISTRE DES RÈGLES DE L'ÉCOSYSTÈME CAC 40, v9.9 · révisé le 28-09-2026*"
                      "\n\n## ANNEXE\nancienne version v5.3\n\n<!-- CONTROLE 00b375b816065f80 · 2026-09-28 03:10 Paris -->")
    v4 = version(sab, "Ancien pied de page, cité : « REGISTRE DES RÈGLES DE L'ÉCOSYSTÈME CAC 40, v1.0 »\n\n"
                      "*Lun 28-09-2026 03h00 (Paris) — REGISTRE DES RÈGLES DE L'ÉCOSYSTÈME CAC 40, v9.9 · révisé le 28-09-2026*")
    res = [("E1 pied de page v9.9, tête « v4.0 » : 9.9 annoncé", v1 == "9.9", v1),
           ("E4 ancien pied de page « v1.0 » cité plus haut : 9.9, la dernière occurrence", v4 == "9.9", v4),
           ("E2 pied de page sans version : « ? »", v2 == "?", v2),
           ("E3 annexe « v5.3 » et ligne de contrôle après le pied : 9.9", v3 == "9.9", v3)]
    rouges = [x for x in res if not x[1]]
    vert = sab == "Z0"
    print(f"== {sab} : {len(res) - len(rouges)} vertes, {len(rouges)} rouges" + (
        "  <-- ATTENDU : 0 rouge" if vert and rouges else "  <-- SABOTAGE NON VU" if not vert and not rouges else ""))
    for nom, ok, det in res:
        if not ok:
            print(f"     ROUGE {nom} · annoncé : {det}")
    _faute = _faute or (vert and bool(rouges)) or (not vert and not rouges)
print("VERDICT :", "tout est conforme" if not _faute else "ECHEC — voir ci-dessus")
sys.exit(1 if _faute else 0)
