#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SABOTER_LES_REPARATIONS_DU_FILET — Ven 16-10-2026 (Paris). Simulation uniquement.

① RÔLE — Prouver que les deux épreuves réparées le 16-10-2026 pour la certification ont des dents : celle du détecteur
  par l'indice et celle des ajustements de Yahoo rendaient TOUJOURS 0, même quand un de leurs sabotages ne mordait
  pas ; elles doivent maintenant rendre 1 dans ce cas, et celle de Yahoo 2 quand son témoin manque ou a changé.
② CONTEXTE D'APPEL — À la main, avant de livrer une modification de ces deux épreuves (R-731) :
  python3 -I tests/outils/SABOTER_LES_REPARATIONS_DU_FILET_Ven_16-10-2026.py <racine du dépôt> [<relevé à écrire>]
③ ENTRÉE — La racine du dépôt (ses vraies épreuves, son vrai témoin des réponses de Yahoo) ; le chemin du relevé,
  facultatif (par défaut tests/resultats/SABOTAGES_DES_REPARATIONS_DU_FILET_<date>.txt sous la racine).
④ CONDITIONS D'ENTRÉE — Le témoin temoins/TEMOIN_REPONSES_DE_YAHOO_DES_39_VALEURS_Jeu_08-10-2026_10h40.tar.gz est au
  dépôt.
⑤ SORTIE — Le code de sortie : 0 si chacun des quatre cas rend le code attendu, 1 sinon. Le relevé est écrit et
  affiché.
  [rend: 1]
⑥ TRAITEMENT — Une copie du dépôt (sans .git ni archives) par cas, dans un dossier jetable : X0 les deux épreuves telles
  quelles → 0 et 0 · X1 un sabotage du détecteur rendu sans effet (le seuil « centuplé » laissé tel quel) → 1 ·
  X2 un sabotage de l'outil de Yahoo rendu sans effet (la marche « décuplée » laissée telle quelle) → 1 · X3 le témoin
  de Yahoo altéré d'un octet → 2 · X4 le témoin de Yahoo absent → 2.
⑦ UNITÉ — Des CODES DE SORTIE.
⑧ POURQUOI — Un jeu d'épreuves se sabote contre sa propre correction : une épreuve qui reste verte quand on retire ce
  qu'elle teste n'est pas une preuve (R-731) ; un contrôle qui n'a pas pu tourner rend un code non nul (R-734). Le
  relevé est écrit par le programme, jamais à la main (R-728).
⑨ CE QUI CLOCHE — Les sabotages portent sur le texte des épreuves, recopié dans la copie ; une épreuve renommée fait
  échouer ce programme (AssertionError), ce qui est voulu. · L'épreuve de Yahoo dure plusieurs minutes : X0 et X2 la
  jouent en entier.
⑩ EFFET — Écrit le relevé ; écrit des copies du dépôt dans le dossier temporaire, effacées à la fin.
⑪ TERMINAISON — Six lancements bornés à 1 800 secondes chacun ; sort par sys.exit avec le code dit en ⑤.
  [sort: oui]
"""
import datetime
import os
import shutil
import subprocess
import sys
import tempfile
import zoneinfo

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "programmes"))
import CERTIFIER_LA_VERSION as CERTIF  # noqa: E402  (l'environnement de la nuit, défini une fois, R-708)

DET = "tests/EPREUVES_DU_DETECTEUR_PAR_L_INDICE_Jeu_08-10-2026.py"
AJ = "tests/EPREUVES_DES_AJUSTEMENTS_DE_YAHOO_Jeu_08-10-2026.py"
TEMOIN = "temoins/TEMOIN_REPONSES_DE_YAHOO_DES_39_VALEURS_Jeu_08-10-2026_10h40.tar.gz"


def copie_du_depot(racine, ou):
    """Copie la racine dans `ou`, sans .git ni archives, et rend le chemin de la copie.

    ① RÔLE — Donner à chaque cas un dépôt qu'il peut abîmer. ② CONTEXTE D'APPEL — `jouer`, une fois par cas.
    ③ ENTRÉE — `racine` : le dépôt · `ou` : un dossier jetable. ④ CONDITIONS D'ENTRÉE — —
    ⑤ SORTIE — UNE valeur : le chemin de la copie. [rend: 1] ⑥ TRAITEMENT — shutil.copytree. ⑦ UNITÉ — —
    ⑧ POURQUOI — Les épreuves écrivent dans leur racine ; le vrai dépôt ne doit pas bouger. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit la copie. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    c = os.path.join(ou, "depot")
    shutil.copytree(racine, c, ignore=shutil.ignore_patterns(".git", "archives", "__pycache__"))
    return c


def jouer(racine, epreuve, ancien=None, nouveau=None, temoin=None):
    """Joue `epreuve` sur une copie, après un sabotage de son texte ou de son témoin ; rend son code de sortie.

    ① RÔLE — Un cas. ② CONTEXTE D'APPEL — `main`, une fois par cas.
    ③ ENTRÉE — `racine` : le dépôt · `epreuve` : le chemin de l'épreuve · `ancien`, `nouveau` : le remplacement à faire
      dans son texte (aucun si None) · `temoin` : « altéré » ou « absent » pour abîmer le témoin de Yahoo (aucun si None).
    ④ CONDITIONS D'ENTRÉE — `ancien` figure une fois exactement dans l'épreuve.
    ⑤ SORTIE — UNE valeur : le code de sortie de l'épreuve. [rend: 1]
    ⑥ TRAITEMENT — copier, abîmer, lancer avec la racine de la copie seule (comme la certification).
    ⑦ UNITÉ — Un code de sortie. ⑧ POURQUOI — Voir la fiche en tête.
    ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit puis efface une copie.
    ⑪ TERMINAISON — L'épreuve est bornée à 1 800 secondes. [sort: non]
    """
    d = tempfile.mkdtemp(prefix="filet_")
    try:
        c = copie_du_depot(racine, d)
        if ancien is not None:
            p = os.path.join(c, epreuve)
            t = open(p, encoding="utf-8").read()
            assert t.count(ancien) == 1, ancien
            open(p, "w", encoding="utf-8").write(t.replace(ancien, nouveau))
        if temoin == "altéré":
            open(os.path.join(c, TEMOIN), "ab").write(b"x")
        elif temoin == "absent":
            os.remove(os.path.join(c, TEMOIN))
        env = dict(os.environ)
        env.update(CERTIF.SANS_LA_CONFIGURATION_GIT_DE_LA_MACHINE)   # cassure N de Cowork, 17-10-2026
        return subprocess.run([sys.executable, "-I", os.path.join(c, epreuve), c], cwd=c, capture_output=True,
                              env=env, timeout=1800).returncode
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    """Joue les cas, écrit le relevé, rend le code.

    ① RÔLE — Le programme entier (voir la fiche en tête). ② CONTEXTE D'APPEL — La ligne de commande.
    ③ ENTRÉE — Voir la fiche en tête. ④ CONDITIONS D'ENTRÉE — Voir la fiche en tête.
    ⑤ SORTIE — UNE valeur : 0 ou 1. [rend: 1] ⑥ TRAITEMENT — Voir la fiche en tête, ⑥. ⑦ UNITÉ — —
    ⑧ POURQUOI — Voir la fiche en tête. ⑨ CE QUI CLOCHE — —
    ⑩ EFFET — Écrit le relevé. ⑪ TERMINAISON — Rend la main. [sort: non]
    """
    racine = os.path.abspath(sys.argv[1])
    maintenant = datetime.datetime.now(zoneinfo.ZoneInfo("Europe/Paris"))
    releve = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        racine, "tests", "resultats", f"SABOTAGES_DES_REPARATIONS_DU_FILET_{maintenant:%a_%d-%m-%Y_%Hh%M}.txt")
    cas = [
        ("X0 détecteur tel quel", DET, None, None, None, 0),
        ("X0 Yahoo tel quel", AJ, None, None, None, 0),
        ("X1 détecteur, un sabotage rendu sans effet", DET,
         '"if a * b < 0 and score > 100 * SEUIL:"', '"if a * b < 0 and score > SEUIL:"', None, 1),
        ("X2 Yahoo, un sabotage rendu sans effet", AJ,
         '("MARCHE = 0.005 ", "MARCHE = 0.05 ")', '("MARCHE = 0.005 ", "MARCHE = 0.005 ")', None, 1),
        ("X3 Yahoo, témoin altéré d'un octet", AJ, None, None, "altéré", 2),
        ("X4 Yahoo, témoin absent", AJ, None, None, "absent", 2),
    ]
    lignes = [f"# Sabotages des deux épreuves réparées le 16-10-2026, joués sur des copies le {maintenant:%d-%m-%Y à %Hh%M}"
              " (Paris) par tests/outils/SABOTER_LES_REPARATIONS_DU_FILET_Ven_16-10-2026.py."]
    fautes = 0
    for nom, epreuve, a, b, t, attendu in cas:
        code = jouer(racine, epreuve, a, b, t)
        ok = code == attendu
        fautes += not ok
        lignes.append(f"{nom} : code {code}, attendu {attendu} — {'conforme' if ok else 'NON CONFORME'}")
    lignes.append("VERDICT : " + ("tout est conforme" if not fautes else f"NON CONFORME — {fautes} cas"))
    os.makedirs(os.path.dirname(releve), exist_ok=True)
    open(releve, "w", encoding="utf-8").write("\n".join(lignes) + "\n")
    print("\n".join(lignes))
    print(f"relevé : {releve}")
    return 1 if fautes else 0


if __name__ == "__main__":
    sys.exit(main())
