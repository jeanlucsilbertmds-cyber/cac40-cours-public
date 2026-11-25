#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Avant toute question à Jean-Luc, cherche les décisions qui en parlent et les affiche, à lire avant la question.

① RÔLE — Le programme d'A-819 ② (étape DEJA, ramenée par A-906) : il reçoit la question en mots, cherche les
  mêmes idées dans BACKLOG_DECISIONS.md (une ligne par action), gouvernance/REGISTRE_REGLES.md (une section par
  règle), MODE_EMPLOI_DEPOT.md et gouvernance/PILOTE.md (un paragraphe chacun), et affiche ce qu'il trouve sous
  « DÉCISIONS QUI EN PARLENT — À LIRE », rangé par statut, chaque ERRATUM à côté de la ligne qu'il cite. Il ne
  tranche RIEN : la ligne de trace d'A-819 ③ (« déjà tranché : A-… — reste ouvert : … ») est écrite par le Chat
  APRÈS lecture. Ce n'est pas un moteur de recherche : une recherche de mots, avec quelques synonymes, dans une
  même phrase.
  Exemple réel : « quand ai-je le droit d'installer ? » (15-11-2026, 15h41) rend A-711 et A-814.

② CONTEXTE D APPEL — Par le Chat avant toute question à Jean-Luc ; la ligne LANCER humain de
  programmes/ORDONNER_UN_PLANNING.py porte la commande à lancer d'abord. Par
  tests/EPREUVES_DU_TUNNEL_DE_PLANIFICATION_Mer_18-11-2026.py (calibrage).

③ ENTRÉE — Les mots de la question, en arguments ; option --racine=<dépôt> (défaut : le dépôt de ce programme).

④ CONDITIONS D ENTRÉE — BACKLOG_DECISIONS.md et gouvernance/REGISTRE_REGLES.md se lisent en UTF-8 ; sinon code 2.
  MODE_EMPLOI_DEPOT.md et gouvernance/PILOTE.md sont lus s'ils existent.

⑤ SORTIE — L'en-tête « DÉCISIONS QUI EN PARLENT — À LIRE … », puis des lignes « À LIRE <identifiant> [<statut>] … »
  (au plus 15 du BACKLOG, 5 de chaque autre source) en trois groupes : décidées ou closes, erratums, ouvertes ou
  sans statut ; puis « À LIRE AVANT DE DEMANDER : … ». Code 0 rien trouvé, « ce qui ne prouve rien » · 1 trouvé ·
  2 lecture impossible ou question sans mot utile (R-734).
  [rend: 1]

⑥ TRAITEMENT — `idees` (mots de 4 lettres au moins, hors mots vides, ramenés à 7 lettres, et leur groupe de
  synonymes) ; `unites` ; les unités qui parlent de ce programme lui-même sont écartées ; `noter` (le meilleur
  nombre d'idées présentes dans UNE phrase, puis dans toute l'unité) ; retenues : au moins toutes les idées moins
  une (toutes s'il y en a deux ou moins), dans une même phrase ; classées par ces deux nombres ; `afficher`.

⑦ UNITÉ — —

⑧ POURQUOI — Jean-Luc, 15-11-2026 15h42 (A-819) : « tu poses régulièrement des questions sur lesquelles on a déjà
  travaillé […] de façon obligatoire par programme » ; 18-11-2026 14h48 (A-906, « 1 ») après le refus des sociétés
  sorties (A-713, A-802, A-829). Le second cas d'A-906, la comptabilité des blocs de la fiche, était FAUX : A-141
  ne la tranchait pas, et la question revient à Jean-Luc (erratum A-907) — d'où l'en-tête « À LIRE » et jamais
  « tranché » : seule la lecture tranche (superviseur R-759, 18-11-2026 16h17). Les mots
  dans une même phrase, et non dans toute la ligne : les lignes du BACKLOG font jusqu'à 6 000 caractères, et une
  question jamais tranchée y trouvait des « décisions » par hasard (mesuré le 18-11 : 18 lignes pour une question
  sur des obligations japonaises).

⑨ CE QUI CLOCHE — Le RAPPEL EST LIMITÉ : les synonymes sont une courte liste écrite ici, et une décision écrite
  avec d'autres mots, ou dont les idées sont dans deux phrases, n'est pas trouvée (A-788, « DEUX BLOCS SÉPARÉS »,
  ne l'est que par l'erratum A-907 qui la cite). Des questions négatives jamais vues au réglage trouvent encore des
  lignes (mesure du 18-11-2026, rapportée telle quelle dans la note de livraison, sans réglage dessus). Le journal
  des questions posées (A-819 ④) n'existe pas. Trouver ne prouve pas que c'est tranché ; ne rien trouver ne prouve
  pas que c'est ouvert.

⑩ EFFET — Lit des fichiers, affiche.

⑪ TERMINAISON — Lectures locales ; revient toujours.
"""
import os
import re
import sys
import unicodedata

ICI = os.path.dirname(os.path.abspath(__file__))
# Synonymes (A-819 ② : installer/fusionner, fenêtre/heure/circuit) et ceux des cas du 18-11 ; débuts de mots.
# Retirés le 18-11-2026 (superviseur R-759, 16h17) : « comptab » (réglé sur l'erreur d'A-906), « jamais », « aucun »,
# « autoris » (des mots de tous les jours, qui faisaient trouver n'importe quoi).
SYNONYMES = (("install", "fusionn", "fusion"), ("quand", "heure", "fenetre", "circuit", "moment"),
             ("droit", "interdi", "permis"), ("societe", "entrepri"), ("refus", "rejet"))
CLOS = ("DÉCIDÉ", "RÈGLE", "CLOSE", "FAIT", "FUSIONN", "INSTALL")   # débuts de statut qui disent la chose tranchée
MOTS_VIDES = set("avec dans pour quel quelle quels quelles faut sont etre avoir cette celle ceux comme mais plus "
                 "moins tout tous toute sans sous elle elles nous vous leur leurs doit peut".split())
SOURCES = (("BACKLOG_DECISIONS.md", "ligne", 15, True), (os.path.join("gouvernance", "REGISTRE_REGLES.md"), "regle", 5, True),
           ("MODE_EMPLOI_DEPOT.md", "paragraphe", 5, False), (os.path.join("gouvernance", "PILOTE.md"), "paragraphe", 5, False))


def norme(t):
    """Rend le texte en minuscules, sans accents.

    ① RÔLE — Comparer « Comptabilité » et « comptabilite ».
    ② CONTEXTE D APPEL — Par idees et noter.
    ③ ENTRÉE — `t`.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le texte normalisé.
      [rend: 1]
    ⑥ TRAITEMENT — NFD, marques d'accent retirées.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Les dictées et le BACKLOG n'accentuent pas pareil.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")


def idees(question):
    """Rend les idées de la question : pour chaque mot utile, le groupe de débuts de mots qui le représentent.

    ① RÔLE — Transformer la question en idées comparables.
    ② CONTEXTE D APPEL — Par main.
    ③ ENTRÉE — `question` : texte.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste des groupes (tuples), sans doublon.
      [rend: 1]
    ⑥ TRAITEMENT — mots de 4 lettres au moins hors MOTS_VIDES, coupés à 7 lettres ; un mot qui commence comme un
      synonyme (ou l'inverse) prend tout son groupe.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — « installer » doit trouver « installation », et A-711 dit « fenêtre du circuit du soir ».
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    out = []
    for w in re.findall(r"[a-z0-9]+", norme(question)):
        if len(w) < 4 or w in MOTS_VIDES:
            continue
        s = w[:7]
        g = next((grp for grp in SYNONYMES if any(s.startswith(x) or x.startswith(s) for x in grp)), (s,))
        if g not in out:
            out.append(g)
    return out


def unites(chemin, coupe):
    """Rend les unités d'un fichier : (identifiant, statut, texte).

    ① RÔLE — Découper chaque source à la mesure d'une décision.
    ② CONTEXTE D APPEL — Par main.
    ③ ENTRÉE — `chemin` ; `coupe` : « ligne » (BACKLOG : lignes « | A-… | »), « regle » (sections « ### R-… »),
      « paragraphe » (blocs séparés par une ligne vide).
    ④ CONDITIONS D ENTRÉE — Fichier lisible ; sinon OSError ou UnicodeDecodeError (main rend 2).
    ⑤ SORTIE — UNE valeur : la liste des unités.
      [rend: 1]
    ⑥ TRAITEMENT — selon `coupe` ; statut = 4e colonne du BACKLOG, sinon « ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Une décision du BACKLOG est une ligne ; une règle, une section.
    ⑨ CE QUI CLOCHE — Un paragraphe du mode d'emploi est identifié par son numéro de ligne.
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Revient toujours ou lève.
      [sort: non]
    """
    texte = open(chemin, encoding="utf-8").read()
    nom = os.path.basename(chemin)
    if coupe == "ligne":
        out = []
        for l in texte.splitlines():
            m = re.match(r"\| (A-\d+) \|", l)
            if m:
                cols = [c.strip() for c in l.split("|")]
                out.append((m.group(1), cols[3] if len(cols) > 3 else "", l))
        return out
    if coupe == "regle":
        parts = re.split(r"\n(?=### R-\d+)", texte)
        return [(re.match(r"### (R-\d+)", p).group(1), "RÈGLE", p) for p in parts if re.match(r"### R-\d+", p)]
    out, n = [], 1
    for bloc in texte.split("\n\n"):
        if bloc.strip():
            out.append((f"{nom}:{n}", "", bloc))
        n += bloc.count("\n") + 2
    return out


def noter(texte, groupes):
    """Rend (meilleur nombre d'idées dans une même phrase, nombre d'idées dans tout le texte).

    ① RÔLE — La note d'une unité.
    ② CONTEXTE D APPEL — Par main.
    ③ ENTRÉE — `texte` ; `groupes` : les idées.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs.
      [rend: 2]
    ⑥ TRAITEMENT — phrases coupées sur « . ; ! ? » suivis d'une espace, guillemets, barres et fins de ligne ; une idée est présente
      si un mot commence par l'un de ses débuts.
    ⑦ UNITÉ — nombre d'idées.
    ⑧ POURQUOI — Voir la fiche (⑧) : la phrase, pas la ligne entière.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    t = norme(texte)
    return max((compter(s, groupes) for s in re.split(r"[.;!?]\s|«|»|\||\n", t)), default=0), compter(t, groupes)


def compter(seg, groupes):
    """Rend le nombre d'idées présentes dans un morceau de texte normalisé.

    ① RÔLE — Le compte élémentaire de noter.
    ② CONTEXTE D APPEL — Par noter, une fois par phrase et une fois pour l'unité entière.
    ③ ENTRÉE — `seg` : texte normalisé ; `groupes` : les idées.
    ④ CONDITIONS D ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le nombre d'idées dont un début de mot apparaît.
      [rend: 1]
    ⑥ TRAITEMENT — mots du morceau ; une idée compte si un mot commence par l'un de ses débuts.
    ⑦ UNITÉ — nombre d'idées.
    ⑧ POURQUOI — « installation » doit compter pour « installer ».
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — —
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    mots = re.findall(r"[a-z0-9]+", seg)
    return sum(1 for g in groupes if any(m.startswith(x) for m in mots for x in g))


def afficher(trouves, erratums):
    """Affiche les unités trouvées sous l'en-tête « À LIRE », rangées par statut, chaque erratum à côté de ce qu'il cite.

    ① RÔLE — La présentation : ne jamais laisser croire qu'une ligne trouvée est une décision prise.
    ② CONTEXTE D APPEL — Par main, une fois.
    ③ ENTRÉE — `trouves` : liste (identifiant, statut, résumé, mots de Jean-Luc ou None) ; `erratums` :
      {identifiant d'une ligne ERRATUM du BACKLOG: identifiants qu'elle cite}.
    ④ CONDITIONS D ENTRÉE — `trouves` non vide.
    ⑤ SORTIE — —
      [rend: rien]
    ⑥ TRAITEMENT — en-tête ; trois groupes dans cet ordre : statut commençant par l'un des CLOS, ERRATUM, le reste ;
      à côté d'une ligne citée par un erratum : « VOIR L'ERRATUM … » ; à côté d'un erratum : ce qu'il cite ; ligne
      finale « À LIRE AVANT DE DEMANDER : … ».
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Superviseur R-759 du 18-11-2026 (16h17), B3 : « jamais « tranché », en-tête « DÉCISIONS QUI EN
      PARLENT — À LIRE », rangées par statut, erratum à côté de la ligne corrigée ». Cas : A-141 présentée sous
      « déjà tranché ? » alors qu'A-907 la corrige.
    ⑨ CE QUI CLOCHE — Le statut est la 4e colonne du BACKLOG telle qu'écrite ; un statut mal écrit est mal rangé.
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    print("DÉCISIONS QUI EN PARLENT — À LIRE (ce programme ne tranche rien : le Chat lit, puis écrit lui-même ce qui "
          "est tranché et ce qui reste ouvert)")
    groupe = lambda st: 0 if st.upper().startswith(CLOS) else (1 if st.upper().startswith("ERRATUM") else 2)
    for g, titre in enumerate(("DÉCIDÉES OU CLOSES", "ERRATUMS", "OUVERTES OU SANS STATUT")):
        lignes = [t for t in trouves if groupe(t[1]) == g]
        if lignes:
            print(f"— {titre} :")
        for ident, statut, bref, mots in lignes:
            voir = [e for e, cites in erratums.items() if ident in cites and e != ident]
            print(f"À LIRE {ident} [{statut[:30]}] {bref}" + (f" — mots de Jean-Luc : « {mots} »" if mots else "")
                  + (f" — VOIR L'ERRATUM {', '.join(voir)}" if voir else "")
                  + (f" — cite {', '.join(erratums[ident])}" if ident in erratums else ""))
    print(f"À LIRE AVANT DE DEMANDER : {', '.join(t[0] for t in trouves)} — reste ouvert : (à écrire par le Chat, "
          "après lecture)")


def main(argv):
    """Cherche, affiche, rend le code.

    ① RÔLE — Tout le programme.
    ② CONTEXTE D APPEL — `python3 programmes/AVANT_DE_DEMANDER.py <mots de la question…> [--racine=<dépôt>]`.
    ③ ENTRÉE — `argv` sans le nom du programme.
    ④ CONDITIONS D ENTRÉE — Voir la fiche du programme.
    ⑤ SORTIE — UNE valeur : le code (0, 1 ou 2).
      [rend: 1]
    ⑥ TRAITEMENT — idées ; pour chaque source, unités (hors celles qui nomment ce programme) notées, retenues et
      classées ; erratums du BACKLOG et ce qu'ils citent ; afficher.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir la fiche du programme.
    ⑨ CE QUI CLOCHE — Voir la fiche du programme.
    ⑩ EFFET — Affiche.
    ⑪ TERMINAISON — Revient toujours.
      [sort: non]
    """
    racine = next((a.split("=", 1)[1] for a in argv if a.startswith("--racine=")), os.path.dirname(ICI))
    groupes = idees(" ".join(a for a in argv if not a.startswith("--")))
    if not groupes:
        print("ARRET aucune idée dans la question (mots de 4 lettres au moins)")
        return 2
    besoin = len(groupes) if len(groupes) <= 2 else len(groupes) - 1
    trouves, erratums = [], {}
    for fichier, coupe, plafond, obligatoire in SOURCES:
        chemin = os.path.join(racine, fichier)
        if not os.path.isfile(chemin) and not obligatoire:
            continue
        try:
            us = unites(chemin, coupe)
        except (OSError, UnicodeDecodeError) as e:
            print(f"ARRET lecture impossible de {fichier} : {e}")
            return 2
        notes = []
        for ident, statut, texte in us:
            if coupe == "ligne" and statut.upper().startswith("ERRATUM"):
                erratums[ident] = sorted(set(re.findall(r"A-\d+", texte)) - {ident})
            if "AVANT_DE_DEMANDER" in texte:
                continue
            phrase, tout = noter(texte, groupes)
            if phrase >= besoin:
                notes.append((-phrase, -tout, ident, statut, texte))
        for _, _, ident, statut, texte in sorted(notes)[:plafond]:
            bref = re.sub(r"\*+|\s+", " ", texte.split("|")[2] if coupe == "ligne" else texte).strip()[:170]
            mots = re.search(r"Jean-Luc[^«]{0,80}«([^»]{1,160})»", texte)
            trouves.append((ident, statut, bref, mots.group(1).strip() if mots else None))
    if not trouves:
        print("RIEN TROUVÉ, ce qui ne prouve rien : la recherche ne voit que les mots de la question et quelques "
              "synonymes — la trace à afficher est « recherche faite, rien trouvé », pas « rien de tranché »")
        return 0
    afficher(trouves, erratums)
    return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
