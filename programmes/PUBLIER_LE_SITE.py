#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rassemble les donnees, fabrique le cockpit, et le publie protege.

① ROLE — **Porter jusqu a la page web que Jean-Luc ouvre ce que le systeme a
  calcule dans la journee.** Il ne calcule rien lui-meme : il prepare les
  entrees du generateur, lance le generateur, fait proteger sa sortie par une
  phrase secrete, et l envoie au depot public sous le nom `index.html`.
② CONTEXTE D APPEL — Le pas n°9 du circuit du soir, « Fabriquer et publier le
  cockpit en page web », apres la tenue des positions.
③ ENTREE — La ligne de commande : la racine du depot, ou le dossier courant a
  defaut. **Et deux variables d environnement** : `GH_TOKEN`, le jeton
  d ecriture du depot public, et `PHRASE`, la phrase secrete qui protege la
  page. **Un seul appelant, le circuit du soir, et il prend les deux dans les
  secrets de l hebergeur.**
④ CONDITIONS D ENTREE — Le generateur doit exister dans `programmes/`. `PHRASE`
  doit etre posee : **sans elle, rien n est publie, par refus delibere.**
  `GH_TOKEN` doit donner le droit d ecrire sur le depot public. Les six
  fichiers d entree peuvent manquer : c est signale, et le generateur fait au
  mieux avec ce qu il a.
⑤ SORTIE — **Un code de sortie, et rien d autre.** La page part sur Internet.
⑥ TRAITEMENT — ① creer un dossier de travail dans la racine · ② y copier les
  six fichiers de donnees SOUS LES NOMS QUE LE GENERATEUR ATTEND · ③ y copier
  les chiffres de reference et les signaux du jour · ④ lancer le generateur ·
  ⑤ prendre la page qu il a produite · ⑥ la faire chiffrer par la phrase ·
  ⑦ demander au depot public l empreinte de la page en place · ⑧ envoyer la
  nouvelle.
⑦ UNITE — Les tailles sont en OCTETS. Les delais sont en SECONDES : dix minutes
  pour le generateur, cinq pour le chiffrement. Les codes HTTP sont ceux du
  protocole web.
⑧ POURQUOI — **Les taches planifiees ne peuvent plus atteindre le depot.** Ce
  n est ni un reglage ni une formulation : le relais des sessions en nuage
  exige qu un depot soit declare comme source de session, et l outil des taches
  n offre aucun moyen de le declarer. Le rapport officiel n°84581 du 6 aout
  2026, toujours ouvert, le dit : *« There is no repo picker, no session-source
  setting, and no slash command. The user cannot fix this from the product, and
  neither can the agent. »*
  **Decision du 11-09-2026 : on cesse de faire lire le depot par les taches.
  L hebergeur fait tout et publie une page web.** Le mur demeure, il ne gene
  plus personne.
  **ET LES NOMS SONT CHANGES A LA COPIE, JAMAIS AU DEPOT.** Le generateur
  cherche `cours_nouveaux.csv`, le depot porte `claude_cours_nouveaux.csv`. Le
  prefixe est retire dans le dossier de travail — une seule graphie reste
  vivante au depot, et le generateur n est pas touche.
  **Le generateur lui-meme n est pas reecrit** : deux implementations d une
  meme chose divergent toujours (R-708). Ce programme ne fait que preparer ses
  entrees et publier sa sortie.
⑨ CE QUI CLOCHE — **Deux defauts, et le premier peut publier la mauvaise page.**
  · **La page publiee est choisie par l ALPHABET, pas par la date.** La ligne
    `pages = sorted(...); page = pages[-1]` trie des noms de la forme
    `cockpit_Ven_19-09-2026_21h48.html`, qui commencent par le jour de la
    semaine. Tries, les sept jours donnent : Dim, Jeu, Lun, Mar, Mer, Sam, Ven.
    **« Ven » sort toujours dernier.** Si le dossier de travail contient deux
    cockpits, celui du vendredi est publie meme s il est plus ancien. Le dossier
    n est jamais vide : il est cree avec `exist_ok`, et ce qui s y trouve reste.
    Sur la machine de l hebergeur, neuve a chaque passage, le cas ne se produit
    pas ; en local, il se produit.
  · **La fonction `api` de ce programme est une SECONDE implementation de celle
    de `PUBLIER_AU_DEPOT_PUBLIC.py`**, avec une signature differente — ici les
    quatre parametres sont obligatoires, la-bas deux ont une valeur par defaut.
    C est exactement ce que R-708 interdit, dans le programme dont le texte
    proclame qu il ne reecrit rien.
⑩ EFFET — **CREE un dossier `_site_travail` dans la racine du depot et y copie
  jusqu a huit fichiers** ; il n est jamais efface. **LANCE deux autres
  programmes.** **ECRIT une page sur le depot public, sur Internet.**
⑪ TERMINAISON — **NE REND JAMAIS LA MAIN : tous les chemins se terminent.**
  0 = page publiee · 1 = phrase absente, protection en echec, jeton absent, ou
  publication refusee · 2 = generateur absent ou aucun cockpit produit.
  **Et un de ses appels peut ne pas revenir : `api` leve sur une panne de
  reseau.**
⑫ DEFINITIONS
  le cockpit : la page web que ce programme fabrique et que Jean-Luc ouvre pour voir l etat du systeme.
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
  les chiffres de reference : les resultats figes des fichiers golden_tests_*.json, qui servent a dire si un calcul a change de comportement.
  le depot public : `jeanlucsilbertmds-cyber/cac40-cours-public`, lisible sans jeton, qui ne porte que des cours et les signaux du jour
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
  le jeton : les 100 000 € simules du portefeuille, engages sur une seule position a la fois.
  une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
import base64, json, os, shutil, subprocess, sys, glob, urllib.request, urllib.error
from datetime import datetime
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")
PUBLIC = "jeanlucsilbertmds-cyber/cac40-cours-public"
GENERATEUR = "GENERATEUR_COCKPIT_Sam_15-08-2026_21h50.py"

# fichier du dépôt -> nom attendu par le générateur
ENTREES = [
    ("donnees/cours_maitre.csv",             "cours_maitre.csv"),
    ("donnees/cac40_strategies.csv",         "cac40_strategies.csv"),
    ("donnees/historique_mesures.csv",       "historique_mesures.csv"),
    ("donnees/claude_journal_trades.csv",    "journal_trades.csv"),
    ("donnees/claude_positions_ouvertes.csv","positions_ouvertes.csv"),
]


def api(methode, url, corps, jeton):
    """Envoie une demande au depot public et rend sa reponse.

    ① ROLE — **Parler au depot public.** Seul endroit de ce programme qui touche
      au reseau.
    ② CONTEXTE D APPEL — `main`, deux fois : demander l empreinte de la page en
      place, puis envoyer la nouvelle.
    ③ ENTREE — `methode` : `GET` ou `PUT` · `url` : l adresse complete ·
      `corps` : ce qu on envoie, ou `None` pour une lecture · `jeton` : le jeton
      d ecriture. **Un seul appelant, et il passe le jeton lu dans `GH_TOKEN`.
      Les quatre parametres sont obligatoires ici — c est la difference avec la
      fonction de meme nom de `PUBLIER_AU_DEPOT_PUBLIC.py`.**
    ④ CONDITIONS D ENTREE — `url` doit etre une adresse complete. `corps` doit
      pouvoir s ecrire en JSON, ou valoir `None`.
    ⑤ SORTIE — **DEUX valeurs : le code du protocole web, et la reponse
      decodee** — un dictionnaire, vide si le serveur n a rien renvoye.
      [rend: 2]
    ⑥ TRAITEMENT — ① encoder le corps s il y en a un · ② composer la demande
      avec le jeton · ③ l envoyer, delai maximal soixante secondes · ④ rendre le
      code et la reponse · ⑤ sur un refus du serveur, rendre son code et son
      message plutot que de laisser l erreur remonter.
    ⑦ UNITE — Le delai est en SECONDES ; le code est un entier du protocole web.
    ⑧ POURQUOI — **Un refus est une reponse, pas une panne.** Une page absente
      rend un code 404, et c est normal la premiere fois qu on publie.
    ⑨ CE QUI CLOCHE — **Elle ne rattrape que les refus du serveur** : une
      coupure de reseau ou une reponse qui n est pas du JSON remontent telles
      quelles et arretent le programme. **Et elle existe en deux exemplaires au
      depot, avec deux signatures differentes.**
    ⑩ EFFET — **ENVOIE une demande sur Internet**, et en mode `PUT` ECRIT la
      page sur le depot public.
    ⑪ TERMINAISON — **Rend la main sur une reponse comme sur un refus du
      serveur. LEVE sans rien rattraper sur une panne de reseau.** Aucun de ses
      appels ne se termine.
      [sort: non]
    """
    d = json.dumps(corps).encode() if corps is not None else None
    r = urllib.request.Request(url, data=d, method=methode,
                               headers={"Authorization": f"Bearer {jeton}",
                                        "Accept": "application/vnd.github+json",
                                        "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=60) as rep:
            return rep.status, json.loads(rep.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


def main():
    """Prepare, fabrique, protege, publie — et refuse de publier en clair.

    ① ROLE — **Enchainer les quatre gestes, et s arreter plutot que de publier
      une page lisible par tous.**
    ② CONTEXTE D APPEL — Le lancement du programme, et lui seul.
    ③ ENTREE — Aucun parametre. Elle lit la racine sur la ligne de commande,
      `GH_TOKEN` et `PHRASE` dans l environnement.
    ④ CONDITIONS D ENTREE — La racine doit exister ; a defaut, le dossier
      courant. Le generateur doit etre dans `programmes/`.
    ⑤ SORTIE — **Ne rend rien : elle se termine toujours par un code de
      sortie.**
      [rend: rien]
    ⑥ TRAITEMENT — ① creer le dossier de travail · ② y copier les six entrees
      sous les noms attendus, et signaler celles qui manquent · ③ y copier les
      chiffres de reference et les signaux du jour · ④ lancer le generateur et
      afficher la fin de son compte rendu · ⑤ prendre la page produite ·
      ⑥ la faire chiffrer, et **s arreter si la phrase manque ou si le
      chiffrement echoue** · ⑦ demander l empreinte de la page en place ·
      ⑧ envoyer la nouvelle.
    ⑦ UNITE — Les tailles sont en OCTETS ; les delais en SECONDES — 600 pour le
      generateur, 300 pour le chiffrement.
    ⑧ POURQUOI — **Le refus de publier sans phrase est delibere.** Le depot est
      public et le cockpit affiche les positions, le journal des trades et les
      mesures. **Mieux vaut une page non mise a jour qu une page lisible par
      quiconque connait l adresse.** C est une decision de Jean-Luc du
      11-09-2026.
      **Et seules les 400 dernieres lettres du compte rendu du generateur sont
      affichees** : le reste encombrerait le journal du circuit sans rien
      apprendre.
    ⑨ CE QUI CLOCHE — **Le choix de la page publiee se fait par l alphabet.**
      `sorted(...)[-1]` sur des noms qui commencent par le jour de la semaine
      rend toujours celui du vendredi quand plusieurs cockpits coexistent. Le
      dossier de travail n est jamais vide entre deux passages.
      **Et il n est jamais efface non plus** : sur une machine qui dure, il
      grossit d un cockpit par passage sans que rien ne le dise.
    ⑩ EFFET — **CREE un dossier dans la racine et y ecrit jusqu a huit
      fichiers** · **LANCE deux autres programmes** · **ECRIT une page sur
      Internet.**
    ⑪ TERMINAISON — **NE REND JAMAIS LA MAIN : tous les chemins se terminent.**
      0 = publie · 1 = phrase absente, protection en echec, jeton absent, ou
      refus du serveur · 2 = generateur absent ou aucun cockpit produit.
      **Et un de ses appels peut ne pas revenir : `api` leve sur une panne de
      reseau.**
      [sort: oui]
    """
    racine = sys.argv[1] if len(sys.argv) > 1 else "."
    jeton = os.environ.get("GH_TOKEN", "")
    maintenant = datetime.now(PARIS)
    travail = os.path.join(racine, "_site_travail")
    os.makedirs(travail, exist_ok=True)

    # ① rassembler les entrées sous les noms attendus
    manquants = []
    for src, dst in ENTREES:
        chemin = os.path.join(racine, src)
        if os.path.isfile(chemin):
            shutil.copy(chemin, os.path.join(travail, dst))
        else:
            manquants.append(src)
    # le golden porte un nom daté : on le copie tel quel, le générateur le cherche par motif
    for g in glob.glob(os.path.join(racine, "gouvernance", "golden_tests_*.json")):
        shutil.copy(g, travail)
    for r in (os.path.join(racine, "donnees", "signaux_du_jour.json"),):
        if os.path.isfile(r):
            shutil.copy(r, travail)
    if manquants:
        print(f"  ⚠️ entrées absentes : {', '.join(manquants)}")

    # ② fabriquer le cockpit — le programme éprouvé, inchangé
    gen = os.path.join(racine, "programmes", GENERATEUR)
    if not os.path.isfile(gen):
        print(f"CODE 2 — générateur absent : {gen}"); sys.exit(2)
    r = subprocess.run([sys.executable, gen, travail, travail],
                       capture_output=True, text=True, timeout=600)
    print(r.stdout.strip()[-400:] if r.stdout else "")
    pages = sorted(glob.glob(os.path.join(travail, "cockpit_*.html")))
    if not pages:
        print("CODE 2 — aucun cockpit fabriqué"); sys.exit(2)
    page = pages[-1]
    # ②bis PROTÉGER PAR PHRASE SECRÈTE avant publication — le dépôt est public, et
    # le cockpit affiche positions, journal et mesures. Sans la phrase, la page
    # publiée ne contient que du texte chiffré. Décision de Jean-Luc, 11-09-2026.
    phrase = os.environ.get("PHRASE", "")
    if phrase:
        protegee = os.path.join(travail, "index_protege.html")
        p = subprocess.run([sys.executable, os.path.join(racine, "programmes", "PROTEGER_LA_PAGE.py"),
                            page, protegee], capture_output=True, text=True,
                           env={**os.environ, "PHRASE": phrase}, timeout=300)
        print(p.stdout.strip())
        if p.returncode != 0 or not os.path.isfile(protegee):
            print("CODE 1 — protection en échec, RIEN N'EST PUBLIÉ"); sys.exit(1)
        page = protegee
    else:
        print("CODE 1 — PHRASE absente : refus de publier le cockpit en clair"); sys.exit(1)
    contenu = open(page, "rb").read()
    print(f"  cockpit : {os.path.basename(page)} · {len(contenu)} octets")

    # ③ publier sous index.html au dépôt PUBLIC — c'est la page que Jean-Luc ouvre
    if not jeton:
        print("CODE 1 — GH_TOKEN absent, rien publié"); sys.exit(1)
    code, rep = api("GET", f"https://api.github.com/repos/{PUBLIC}/contents/index.html", None, jeton)
    sha = rep.get("sha") if code == 200 else None
    corps = {"message": f"cockpit {maintenant.strftime('%Y-%m-%d %Hh%M')}",
             "content": base64.b64encode(contenu).decode()}
    if sha:
        corps["sha"] = sha
    code, rep = api("PUT", f"https://api.github.com/repos/{PUBLIC}/contents/index.html", corps, jeton)
    if code in (200, 201):
        print(f"  ✅ publié · https://jeanlucsilbertmds-cyber.github.io/cac40-cours-public/")
        sys.exit(0)
    print(f"  ❌ publication refusée — HTTP {code} : {rep.get('message','?')}")
    sys.exit(1)


if __name__ == "__main__":
    main()
