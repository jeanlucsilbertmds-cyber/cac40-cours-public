#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MODULE_CONTROLE_2_DU_HASARD — Sam 28-11-2026 (Paris), lot W2a du plan R505. SIMULATION UNIQUEMENT : aucun ordre réel.

À QUOI SERT CE MODULE, EN FRANÇAIS SIMPLE. Gagner ne suffit pas : en marché qui monte, presque tout achat gagne. Le
contrôle 2 de la loi R-505 version 2 demande si la version CHOISIT mieux que le hasard : pour chaque vrai achat, des
achats imaginaires — une action et un jour tirés au hasard parmi les jours du MÊME TYPE DE MARCHÉ, MESURÉ LE JOUR MÊME,
mêmes sorties, mêmes frais — et l'on compte la part des tirages qui font aussi bien ou mieux (exemple de la loi :
3 sur 1 000 → 0,3 %).

SUR QUELLES DÉCISIONS IL REPOSE (BACKLOG) :
- A-1072 (Jean-Luc, 27-11-2026 à 13h50, « 1 ») : le hasard est tiré dans le MÊME TYPE DE MARCHÉ que chaque vrai achat
  (hausse calme, hausse agitée, baisse calme, baisse agitée), et non plus dans la même année (remplace DÉL-D38).
- A-1105 (Jean-Luc, 27-11-2026 à 22h15, « Alors le 1 ») : ce type de marché est celui MESURÉ LE JOUR MÊME, jamais le
  découpage daté après coup de l'étape 2 — un expert ne compare une décision qu'à ce qui était possible au moment de la
  prendre. Le découpage vient de `MODULE_QUAND_JOUER.decoupage_par_defaut` (lot W2e-FIX), importé, jamais recopié
  (R-708 : deux écritures d'une même chose divergent toujours).
- A-1081 (Jean-Luc, 27-11-2026 à 16h40, « c'est le 1 ») : DEUX BARRES. Sur les 70 %, un FILTRE LARGE (« faire mieux
  que le hasard ») ; sur les 30 %, la PREUVE STRICTE. « La largeur du filtre des 70 % est à fixer par programme et à
  éprouver par simulation (fausses stratégies sans avantage) avant de servir » : elle n'est PAS fixée ; tant qu'elle
  ne l'est pas, ce module rend le filtre large INCONNU (garde-fou A-1067 : aucun verdict sur un critère non branché).
- A-1070 (Jean-Luc, 27-11-2026 à 13h40, « 1 oui ») et A-1095 corrigée le 27-11-2026 à 21h19 : « le contrôle 2 (jour
  au hasard) garde 0,05 ÷ k ». Le seuil se lit à la table de la loi (`MODULE_JUGEMENT.seuil_de_la_loi`, clé
  `seuil_du_hasard`, « 0,05 ÷ k ») ; k vient de `COMPTER_LES_ESSAIS_PAR_RESSEMBLANCE.compter_les_essais` (lot W2c),
  passé en paramètre par l'appelant.
- Loi R-505 v2, étape 5 : « le nombre de tirages au hasard doit être assez grand pour que 1 ÷ (nombre de tirages) passe
  sous 0,05 ÷ k », sinon le contrôle est INCONNU (DÉL-D38).

LE TIRAGE N'EST PAS RECOPIÉ : c'est celui du juge, `MODULE_JUGEMENT.etalon_hasard`, en mode « meme_type » (ajouté par
ce lot), avec la mécanique d'achat-sortie de la stratégie (`entree`) et sa règle d'achat (`admis`) que passe le juge.
La part des tirages battus est `MODULE_JUGEMENT.p_du_hasard`.

UN TYPE DE MARCHÉ SANS OPÉRATION DE LA VERSION : rien à tirer ; il est AFFICHÉ (« aucune opération »), il ne bloque
pas (même logique qu'A-1113, Jean-Luc 28-11-2026 à 12h12 : « il est simplement affiché »).
"""
import math
import os
import sys

_ICI = os.path.dirname(os.path.abspath(__file__))
if _ICI not in sys.path:
    sys.path.insert(0, _ICI)

import MODULE_JUGEMENT as J          # noqa: E402  le tirage du juge et la part des tirages battus (R-708)
import MODULE_QUAND_JOUER as QJ      # noqa: E402  le découpage du jour même (lot W2e-FIX, A-1105)

CLE_DU_SEUIL_STRICT = "seuil_du_hasard"            # la ligne de la table de la loi : « 0,05 ÷ k »
CLE_DU_FILTRE_LARGE = "hasard_filtre_large_70"     # la ligne attendue dans les seuils en attente ; ABSENTE à ce jour


def nombre_de_tirages(seuil):
    """Rend le plus petit nombre de tirages dont l'inverse passe sous le seuil.

    ① RÔLE — Dire combien de tirages il faut pour que le contrôle puisse conclure (loi R-505 v2, étape 5 : « 1 ÷
      (nombre de tirages) passe sous 0,05 ÷ k », sinon INCONNU, DÉL-D38).
    ② CONTEXTE D'APPEL — `tirer_le_jour_au_hasard`, quand l'appelant ne fixe pas le nombre ; les épreuves du lot W2a.
    ③ ENTRÉE — `seuil` : un nombre dans ]0, 1].
    ④ CONDITIONS D'ENTRÉE — Un seuil hors de ]0, 1] ou non fini lève ValueError.
    ⑤ SORTIE — UNE valeur : un entier ≥ 2.
      [rend: 1]
    ⑥ TRAITEMENT — ① partir de la partie entière de 1 ÷ seuil (au moins 1) · ② tant que 1 ÷ n ne passe pas
      STRICTEMENT sous le seuil en nombres flottants, n + 1 : le premier n qui passe est rendu, donc le plus petit
      (W2a-N3, lot I1FIX du 28-11-2026 : 0,05 ÷ 21 s'inverse en 419,999…, « partie entière plus un » donnait 420
      tirages, et 1 ÷ 420 n'est pas sous la barre : le contrôle était INCONNU par DÉL-D38 pour k = 21, 42, 49, 83… ;
      la même formule donnait 141 pour k = 7, un de trop — la propriété est désormais vérifiée par la même inégalité
      que `controle_2`).
    ⑦ UNITÉ — Des tirages.
    ⑧ POURQUOI — Un chiffre qui se calcule ne s'écrit pas à la main (R-728) : `n_tirages=120` écrit dans le juge rend
      le contrôle INCONNU dès que k dépasse 6 (loi R-505 v2, étape 5).
    ⑨ CE QUI CLOCHE — — (la seconde écriture de `JUGER_UNE_FICHE`, consignée ici jusqu'au 28-11-2026, a été réunie à
      la réunion I1 : `JUGER_UNE_FICHE._hasard` appelle cette fonction).
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main ; la boucle s'arrête car seuil > 0 (1 ÷ n tend vers 0 ; en pratique un tour au plus).
      [sort: non]
    """
    if isinstance(seuil, bool) or not isinstance(seuil, (int, float)) or not math.isfinite(seuil) \
            or not 0.0 < seuil <= 1.0:
        raise ValueError("nombre_de_tirages : seuil hors de ]0, 1] : %r" % (seuil,))
    n = max(1, int(1.0 / seuil))
    while 1.0 / n >= seuil:   # W2a-N3 : la même inégalité que `controle_2` (DÉL-D38), en flottants
        n += 1
    return n


def tirer_le_jour_au_hasard(ops, cours, univers, entree, admis, periode, decoupage, n_tirages, graine=None):
    """Tire, pour chaque vrai achat, des achats au hasard dans le même type de marché mesuré le jour même.

    ① RÔLE — Fabriquer la distribution du hasard du contrôle 2 (A-1072, A-1105), par le tirage du juge.
    ② CONTEXTE D'APPEL — `controle_2` ; les épreuves du lot W2a. À venir : le juge (30 %) et la moulinette (70 %), au
      branchement (A-1067).
    ③ ENTRÉE — `ops` : les opérations réelles de la version (cases `date_signal`, `net`) · `cours`, `univers`,
      `entree`, `admis`, `periode` : comme pour `MODULE_JUGEMENT.etalon_hasard` (la mécanique et la règle d'achat du
      juge, `JUGE_DES_STRATEGIES.jouer_une_entree` et `achat_admis`) · `decoupage` : un `MODULE_QUAND_JOUER.Decoupage`
      du jour même, en pratique `QJ.decoupage_par_defaut(racine)` · `n_tirages` : un entier ≥ 1 · `graine` : None pour
      la graine du juge (`MODULE_JUGEMENT.GRAINE`).
    ④ CONDITIONS D'ENTRÉE — `decoupage.jour_meme` vrai, sinon ValueError (levée par `etalon_hasard`).
    ⑤ SORTIE — UNE valeur : le rendu d'`etalon_hasard` en mode « meme_type » (seize cases, ou deux si rien n'est tiré).
      [rend: 1]
    ⑥ TRAITEMENT — appel d'`etalon_hasard(mode="meme_type")` ; objectif, stop, horizon et module des positions ne sont
      pas lus par l'étalon (ils voyagent dans `entree`), d'où None.
    ⑦ UNITÉ — Gains en EUROS.
    ⑧ POURQUOI — Un seul tirage dans le dépôt (R-708) : le juge et ce contrôle tirent de la même façon.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Ceux d'`entree` (le module des positions).
    ⑪ TERMINAISON — Rend la main ; le nombre d'appels à `entree` est borné par n_tirages × nombre d'opérations.
      [sort: non]
    """
    return J.etalon_hasard(ops, cours, univers, None, None, None, None, mode="meme_type", n_tirages=n_tirages,
                           graine=J.GRAINE if graine is None else graine, entree=entree, admis=admis,
                           periode=periode, decoupage=decoupage)


def types_sans_operation(rendu):
    """Rend les types de marché où la version n'a aucune opération : rien à tirer, affiché.

    ① RÔLE — Garder l'information qu'un type n'a jamais été éprouvé (A-1113, même logique : « il est simplement
      affiché »).
    ② CONTEXTE D'APPEL — `controle_2`.
    ③ ENTRÉE — `rendu` : un rendu de `tirer_le_jour_au_hasard`.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : la liste, dans l'ordre de `MODULE_QUAND_JOUER.TYPES_DE_MARCHE`, des types sans opération.
      [rend: 1]
    ⑥ TRAITEMENT — les types de `QJ.TYPES_DE_MARCHE` absents d'`operations_par_type` (tous si la case manque).
    ⑦ UNITÉ — —
    ⑧ POURQUOI — Un type sans opération ne se tire pas ; le taire laisserait croire que la version y a été éprouvée.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    par = rendu.get("operations_par_type") if isinstance(rendu, dict) else None
    par = par if isinstance(par, dict) else {}
    return [t for t in QJ.TYPES_DE_MARCHE if not par.get(t)]


def largeur_du_filtre_large(racine):
    """Lit la largeur du filtre large des 70 % aux seuils en attente ; None tant qu'elle n'est pas fixée.

    ① RÔLE — Lire, jamais écrire, la barre du filtre large (A-1081).
    ② CONTEXTE D'APPEL — `controle_2` sur les 70 %, quand l'appelant ne la passe pas.
    ③ ENTRÉE — `racine` : la racine d'un dépôt ou d'une copie.
    ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — DEUX valeurs : la largeur (une probabilité) ou None, et la raison (vide si la largeur est rendue).
      [rend: 2]
    ⑥ TRAITEMENT — `MODULE_JUGEMENT.table_des_seuils_en_attente(racine)` puis `seuil_de_la_loi` sur
      `hasard_filtre_large_70`.
    ⑦ UNITÉ — Une probabilité.
    ⑧ POURQUOI — A-1081 : « la largeur du filtre des 70 % est à fixer par programme et à éprouver par simulation
      (fausses stratégies sans avantage) avant de servir ». Elle ne s'invente pas dans le code (R-728, R-754).
    ⑨ CE QUI CLOCHE — À ce jour la ligne n'existe pas : le filtre large rend INCONNU tant que la simulation n'est pas
      faite et la largeur décidée (BACKLOG).
    ⑩ EFFET — Lit un fichier.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    try:
        table = J.table_des_seuils_en_attente(racine)
    except (OSError, ValueError) as ex:
        return None, "seuils en attente illisibles : %s" % ex
    if not isinstance(table, dict) or CLE_DU_FILTRE_LARGE not in table:
        return None, ("largeur du filtre large des 70 %% non fixée (ligne « %s » absente) : « à fixer par programme "
                      "et à éprouver par simulation (fausses stratégies sans avantage) avant de servir » (A-1081)"
                      % CLE_DU_FILTRE_LARGE)
    largeur, raison = J.seuil_de_la_loi(table, CLE_DU_FILTRE_LARGE)
    return largeur, raison


def controle_2(ops, rendu, part, k=None, table=None, largeur=None, raison_largeur=""):
    """Rend l'état du contrôle 2 « mieux que le hasard » sur les 70 % (filtre large) ou les 30 % (preuve stricte).

    ① RÔLE — Juger la part des tirages du même type, mesuré le jour même, qui font aussi bien que la version, à la
      barre de la partie (A-1081) ; afficher les types sans opération.
    ② CONTEXTE D'APPEL — Le juge : `MODULE_JUGEMENT.grille_de_validation`, contrôle ⑥, `part="30"` (branché à la
      réunion I1 du 28-11-2026) ; la moulinette (étape 4, `part="70"`) : PAS ENCORE branchée ; les épreuves.
    ③ ENTRÉE — `ops` : les opérations réelles (case `net`, en euros) · `rendu` : celui de `tirer_le_jour_au_hasard`
      sur ces mêmes opérations · `part` : « 70 » ou « 30 » · `k` : le nombre d'essais de
      `COMPTER_LES_ESSAIS_PAR_RESSEMBLANCE.compter_les_essais` (clé « k »), exigé sur les 30 % · `table` : la table de
      la loi (`MODULE_JUGEMENT.table_de_la_loi`), exigée sur les 30 % · `largeur` : la barre du filtre large (de
      `largeur_du_filtre_large`), exigée sur les 70 % ; `raison_largeur` : la raison rendue avec une largeur None.
    ④ CONDITIONS D'ENTRÉE — `part` hors de {« 70 », « 30 »} lève ValueError.
    ⑤ SORTIE — UNE valeur : un dictionnaire {etat : PASSE, BLOQUE ou INCONNU ; valeur : p ou None ; seuil ; raison ;
      barre : « filtre large (70 %) » ou « preuve stricte 0,05 ÷ k (30 %) » ; tirages ; types_sans_operation ;
      operations_par_type ; operations_sans_type ; operations_exclues_sans_type : le nombre d'opérations EXCLUES parce
      que leur jour n'a pas de type mesuré le jour même (A-1117), AFFICHÉ ; None si le rendu ne le dit pas ;
      operations_absentes_du_decoupage : le nombre d'opérations dont le jour MANQUE dans le découpage (A-1118 (b)) ;
      None si le rendu ne le dit pas}.
      [rend: 1]
    ⑥ TRAITEMENT — ① la barre : sur les 30 %, `seuil_de_la_loi(table, "seuil_du_hasard", k)` ; sur les 70 %, `largeur`
      · ② A-1117 et A-1118 (a) (28-11-2026) : les opérations dont la date de signal est dans `signaux_sans_type` du
      rendu (jour typé « INCONNU » : première année des données) sont EXCLUES, leur nombre est rendu ; A-1118 (b) : les
      opérations dont la date est dans `signaux_absents_du_decoupage` (jour qui MANQUE au fichier de l'indice) sont
      comptées · ③ INCONNU si la barre manque, si aucune opération ne reste, si le rendu ne dit pas quels signaux sont
      sans type ou absents du découpage, si UNE opération tombe un jour absent du découpage (A-1118 (b), décision de
      Jean-Luc du 28-11-2026 à 15h48 : « 1 »), si une opération TYPÉE n'a rien à tirer dans son
      type (DÉL-D26), ou si 1 ÷ tirages ne passe pas sous la barre (DÉL-D38) · ④ p par `MODULE_JUGEMENT.p_du_hasard`
      sur le gain net des opérations GARDÉES (celles que le tirage a remplacées) ; PASSE si p < barre, sinon BLOQUE.
    ⑦ UNITÉ — p et barres sont des probabilités ; gains en EUROS.
    ⑧ POURQUOI — Deux barres (A-1081) : sur les 70 %, une barre stricte éliminerait de vraies bonnes versions avant le
      juge ; sur les 30 %, la preuve stricte est la seule qui décide. 0,05 ÷ k sur les 30 % (A-1070, A-1095 corrigée).
    ⑨ CE QUI CLOCHE — ① Un tirage qui joue moins d'opérations que la version a une somme plus petite, ce qui avantage
      la version (déjà consigné à `p_du_hasard`). ② La largeur du filtre large n'existe pas encore (A-1081). ③ A-1117
      était une application par le Chat de la règle de Jean-Luc d'A-1113 ; A-1118 (Jean-Luc, 28-11-2026 à 15h48) la
      confirme pour la première année et la refuse pour les jours absents du fichier de l'indice.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend la main.
      [sort: non]
    """
    if part not in ("70", "30"):
        raise ValueError("controle_2 : part « 70 » ou « 30 », reçu %r" % (part,))
    barre = "filtre large (70 %)" if part == "70" else "preuve stricte 0,05 ÷ k (30 %)"
    sans = types_sans_operation(rendu)
    sans_type = (rendu or {}).get("signaux_sans_type") if isinstance(rendu, dict) else None
    absents = (rendu or {}).get("signaux_absents_du_decoupage") if isinstance(rendu, dict) else None
    # A-1118 (b) (décision de Jean-Luc du 28-11-2026 à 15h48, « 1 ») : une opération dont le jour MANQUE dans le
    # découpage (fichier de l'indice trop court) rend le contrôle INCONNU ; compté AVANT l'exclusion d'A-1118 (a)
    absentes = None
    if isinstance(absents, (list, tuple)):
        _abs = set(absents)
        absentes = sum(1 for o in (ops or []) if o.get("date_signal") in _abs)
    exclues = None
    if isinstance(sans_type, (list, tuple)):
        # A-1117 : une opération au jour SANS TYPE mesuré le jour même est EXCLUE du contrôle, et comptée (affichée)
        dates_sans_type = set(sans_type)
        gardees = [o for o in (ops or []) if o.get("date_signal") not in dates_sans_type]
        exclues = len(ops or []) - len(gardees)
        ops = gardees
    base = {"barre": barre, "types_sans_operation": sans,
            "operations_par_type": (rendu or {}).get("operations_par_type"),
            "operations_sans_type": (rendu or {}).get("operations_sans_type"),
            "operations_exclues_sans_type": exclues,
            "operations_absentes_du_decoupage": absentes,
            "tirages": (rendu or {}).get("n_tirages", 0)}

    def fin(etat, raison="", valeur=None, seuil=None):
        """Rend le dictionnaire de sortie du contrôle.

        ① RÔLE — Écrire la sortie en un seul endroit, pour que chaque sortie porte les mêmes cases.
        ② CONTEXTE D'APPEL — `controle_2`, à chacune de ses sorties.
        ③ ENTRÉE — `etat` : PASSE, BLOQUE ou INCONNU · `raison` · `valeur` : p ou None · `seuil` : la barre ou None.
        ④ CONDITIONS D'ENTRÉE — —
        ⑤ SORTIE — UNE valeur : le dictionnaire décrit au ⑤ de `controle_2`.
          [rend: 1]
        ⑥ TRAITEMENT — réunir les quatre cases reçues et celles de `base`.
        ⑦ UNITÉ — —
        ⑧ POURQUOI — Une sortie qui oublierait les types sans opération les tairait (A-1113).
        ⑨ CE QUI CLOCHE — —
        ⑩ EFFET — Aucun.
        ⑪ TERMINAISON — Rend la main.
          [sort: non]
        """
        return {"etat": etat, "valeur": valeur, "seuil": seuil, "raison": raison, **base}

    if part == "30":
        seuil, r = J.seuil_de_la_loi(table, CLE_DU_SEUIL_STRICT, k)
    else:
        seuil, r = largeur, (raison_largeur or "largeur du filtre large non fournie (A-1081)")
    if seuil is None:
        return fin("INCONNU", r)
    if not ops:
        return fin("INCONNU", "aucune opération", seuil=seuil)
    if not isinstance(rendu, dict) or (rendu.get("mode") is not None and rendu.get("mode") != "meme_type"):
        return fin("INCONNU", "le hasard reçu n'est pas tiré dans le même type de marché (mode %r)"
                   % ((rendu or {}).get("mode"),), seuil=seuil)
    if exclues is None:
        return fin("INCONNU", "le rendu du hasard ne dit pas quels signaux sont sans type (`signaux_sans_type`) : "
                   "l'exclusion d'A-1117 ne peut pas se faire", seuil=seuil)
    if absentes is None:
        return fin("INCONNU", "le rendu du hasard ne dit pas quels signaux manquent au découpage "
                   "(`signaux_absents_du_decoupage`) : A-1118 (b) ne peut pas se vérifier", seuil=seuil)
    if absentes:
        return fin("INCONNU", "%d opération(s) un jour absent du fichier de l'indice (A-1118) : le contrôle attend "
                   "l'allongement du fichier" % absentes, seuil=seuil)
    if not ops:
        return fin("INCONNU", "aucune opération après l'exclusion de %d opération(s) sans type (A-1117)" % exclues,
                   seuil=seuil)
    if rendu.get("operations_sans_achat_tirable"):
        return fin("INCONNU", "%d opération(s) d'un type de marché sans achat tirable dans ce type (DÉL-D26)"
                   % rendu["operations_sans_achat_tirable"], seuil=seuil)
    p, n_t, r = J.p_du_hasard(math.fsum(o["net"] for o in ops), rendu)
    if p is None:
        return fin("INCONNU", r, seuil=seuil)
    if 1.0 / n_t >= seuil:
        return fin("INCONNU", "%d tirages : 1 ÷ tirages = %.6f ne passe pas sous la barre %.6f (DÉL-D38)"
                   % (n_t, 1.0 / n_t, seuil), valeur=p, seuil=seuil)
    return fin("PASSE" if p < seuil else "BLOQUE", valeur=p, seuil=seuil)
