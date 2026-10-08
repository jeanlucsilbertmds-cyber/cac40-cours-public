#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Copie les fichiers de cours du depot prive vers le depot public.

① ROLE — **Donner aux taches planifiees une adresse qu elles peuvent lire.**
  Elles n ont plus le droit de cloner le depot prive ; leur outil de lecture
  web, lui, fonctionne, mais il lui faut une adresse publique sans jeton. Ce
  programme entretient cette adresse.
② CONTEXTE D APPEL — Le pas n°10 du circuit du soir, « Publier les cours et
  l historique dans le depot PUBLIC », apres la detection des signaux.
③ ENTREE — La ligne de commande : la racine du depot, ou le dossier courant a
  defaut. **Et une variable d environnement `GH_TOKEN`**, le jeton d ecriture
  du depot public. **Un seul appelant, le circuit du soir, et il le prend dans
  les secrets de l hebergeur.**
④ CONDITIONS D ENTREE — `GH_TOKEN` doit etre pose et donner le droit d ecrire
  sur le depot public. Les trois fichiers a publier peuvent manquer : chacun
  est un cas prevu, compte comme un echec, et ne bloque pas les autres.
⑤ SORTIE — **Un code de sortie, et rien d autre.** 0 si les trois fichiers sont
  publies, 1 si au moins un manque ou est refuse.
⑥ TRAITEMENT — ① lire le jeton, et s arreter s il manque · ② pour chacun des
  trois fichiers : verifier qu il existe, demander au depot public l empreinte
  de la version deja publiee, envoyer le contenu · ③ afficher l adresse de
  lecture · ④ s arreter sur 1 si un echec.
⑦ UNITE — Les tailles affichees sont en OCTETS. Les codes HTTP sont ceux du
  protocole web : 200 et 201 valent succes, tout le reste est un echec.
⑧ POURQUOI — **Le reseau des taches a cesse d autoriser le depot prive dans la
  nuit du 10 au 11-09-2026.** Le refus a ete confirme sur une machine demarree
  une heure quarante-cinq APRES l ajout du domaine dans les reglages : ce n est
  ni l anciennete de la session ni un delai de propagation. **Les taches ne
  peuvent plus cloner. Elles peuvent encore lire une adresse publique.**
  **Aucune donnee sensible n y passe** : des cours de bourse, publics par
  nature. La gouvernance — la loi, les decisions, les etudes — reste au depot
  prive.
  **Et l ordre des trois fichiers n est pas indifferent** : le fichier des
  signaux passe en premier parce que c est celui que la boucle lit vraiment, et
  qu il pese un kilo-octet. **L outil de lecture web tronque a environ 49 000
  octets sans le dire** — mesure le 11-09-2026 sur un fichier de 73 904 octets.
  Les deux autres restent publies pour qui veut les donnees brutes, mais aucune
  boucle ne doit s appuyer dessus.
⑨ CE QUI CLOCHE — **Une panne de reseau n est pas rattrapee.** La fonction `api`
  rattrape les refus du serveur — un code 404, un code 403 — mais pas une
  coupure, un nom de domaine introuvable ou un delai depasse. Dans ces cas le
  programme s arrete sur une erreur de langage, sans message et sans publier les
  fichiers suivants. **Le pas du circuit rougirait, mais personne ne saurait que
  la cause etait le reseau et non le jeton.**
⑩ EFFET — **ECRIT trois fichiers sur un depot distant, sur Internet.** C est le
  seul programme du systeme qui ecrit hors de la machine qui l execute. Il ne
  modifie rien localement.
⑪ TERMINAISON — **NE REND JAMAIS LA MAIN : tous les chemins se terminent.**
  0 = les trois publies · 1 = jeton absent, ou au moins un fichier manquant ou
  refuse. **Et un de ses appels peut ne pas revenir : `api` remonte une panne
  de reseau sans la rattraper.**
⑫ DEFINITIONS
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
  la boucle : la tache planifiee qui lit les signaux et rend compte
  le depot public : `jeanlucsilbertmds-cyber/cac40-cours-public`, lisible sans
    jeton, qui ne porte que des cours et les signaux du jour
  la racine : le dossier reçu sur la ligne de commande, celui dont on classe les fichiers — en général un clone du dépôt.
  le jeton : les 100 000 € simules du portefeuille, engages sur une seule position a la fois.
  un cas : une épreuve de ce programme, c'est-à-dire un défaut déjà rencontré rejoué à l'identique pour vérifier qu'il n'est pas revenu.
"""
import base64, json, os, sys, urllib.request, urllib.error

PUBLIC = "jeanlucsilbertmds-cyber/cac40-cours-public"
# signaux_du_jour.json D'ABORD : c'est le fichier que la boucle lit vraiment, et il
# fait un kilo-octet — jamais tronqué. Les deux autres restent publiés pour qui veut
# les données brutes, mais la boucle ne doit PAS s'appuyer dessus : l'outil web
# tronque à ~49 Ko sans le dire (mesuré le 11-09 sur 73 904 octets).
A_PUBLIER = [("donnees/signaux_du_jour.json",      "signaux_du_jour.json"),
             ("donnees/claude_cours_nouveaux.csv", "cours_nouveaux.csv"),
             ("donnees/cac40_ohlcv.csv",           "cac40_ohlcv.csv")]


def api(methode, url, corps=None, jeton=""):
    """Envoie une demande au depot public et rend sa reponse.

    ① ROLE — **Parler au depot public.** C est le seul endroit du programme qui
      touche au reseau ; tout le reste est de la lecture de fichiers.
    ② CONTEXTE D APPEL — `main`, deux fois par fichier a publier : une fois pour
      demander l empreinte de la version deja en place, une fois pour envoyer la
      nouvelle.
    ③ ENTREE — `methode` : le verbe du protocole web, `GET` ou `PUT` · `url` :
      l adresse complete · `corps` : ce qu on envoie, ou rien pour une lecture ·
      `jeton` : le jeton d ecriture. **Un seul appelant, et il passe le jeton lu
      dans `GH_TOKEN`.**
    ④ CONDITIONS D ENTREE — `url` doit etre une adresse complete. `corps` doit
      pouvoir s ecrire en JSON, ou valoir `None`.
    ⑤ SORTIE — **DEUX valeurs : le code du protocole web, et la reponse
      decodee.** La reponse est un dictionnaire, vide si le serveur n a rien
      renvoye.
      [rend: 2]
    ⑥ TRAITEMENT — ① encoder le corps en JSON s il y en a un · ② composer la
      demande avec le jeton et les en-tetes attendus · ③ l envoyer, avec un
      delai maximal de soixante secondes · ④ rendre le code et la reponse ·
      ⑤ si le serveur refuse, rendre son code et son message au lieu de laisser
      l erreur remonter.
    ⑦ UNITE — Le delai est en SECONDES. Le code est un entier du protocole web.
    ⑧ POURQUOI — **Un refus du serveur est une reponse, pas une panne.** Un
      fichier absent du depot public rend un code 404, et c est normal la
      premiere fois qu on le publie : `main` s en sert pour savoir s il faut
      envoyer une empreinte de remplacement. Laisser cette erreur remonter
      arreterait le programme au premier fichier neuf.
    ⑨ CE QUI CLOCHE — **Elle ne rattrape que les refus du serveur.** Une coupure
      de reseau, un nom de domaine introuvable ou un delai depasse remontent
      tels quels et arretent le programme. **Et si le serveur repond autre chose
      que du JSON — une page d erreur en HTML, par exemple —, le decodage echoue
      de la meme facon.** Dans les deux cas, aucun message ne dit ce qui s est
      passe.
    ⑩ EFFET — **ENVOIE une demande sur Internet**, et en mode `PUT` ECRIT un
      fichier sur le depot public.
    ⑪ TERMINAISON — **Rend la main dans les deux cas prevus — reponse ou refus
      du serveur. Mais elle LEVE, sans rien rattraper, sur une panne de reseau
      ou une reponse illisible.** Aucun de ses appels ne se termine.
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
    """Publie les trois fichiers, un par un, et rend compte.

    ① ROLE — **Enchainer les publications sans qu un echec en cache un autre.**
      Chaque fichier est traite jusqu au bout, meme si le precedent a echoue.
    ② CONTEXTE D APPEL — Le lancement du programme, et lui seul.
    ③ ENTREE — Aucun parametre. Elle lit la racine sur la ligne de commande et
      le jeton dans `GH_TOKEN`.
    ④ CONDITIONS D ENTREE — Le jeton doit etre pose. La racine doit exister ; a
      defaut d argument, le dossier courant est employe.
    ⑤ SORTIE — **Ne rend rien : elle se termine toujours par un code de
      sortie.**
      [rend: rien]
    ⑥ TRAITEMENT — ① lire la racine et le jeton, s arreter si le jeton manque ·
      ② pour chacun des trois fichiers : s il manque, le signaler et compter un
      echec · sinon le lire, demander l empreinte de la version publiee, et
      l envoyer · ③ compter les echecs · ④ afficher l adresse de lecture ·
      ⑤ s arreter sur 1 si un echec, 0 sinon.
    ⑦ UNITE — Les tailles affichees sont en OCTETS, lues sur le fichier local.
    ⑧ POURQUOI — **L empreinte de la version deja publiee est exigee par le
      serveur pour ecraser un fichier.** Sans elle, le remplacement est refuse.
      C est pourquoi chaque fichier demande d abord, ecrit ensuite : deux
      allers-retours par fichier, et non un seul.
    ⑨ CE QUI CLOCHE — **Un fichier absent du depot local et un fichier refuse
      par le serveur comptent tous deux comme un echec, et donnent le meme code
      de sortie 1.** Le premier se repare en relancant le pas precedent du
      circuit, le second en changeant le jeton : deux causes, un seul code.
      Les symboles affiches les distinguent a l ecran, le code de sortie non.
    ⑩ EFFET — **ECRIT jusqu a trois fichiers sur le depot public**, sur
      Internet. Rien n est modifie localement.
    ⑪ TERMINAISON — **NE REND JAMAIS LA MAIN : tous les chemins se terminent.**
      0 = les trois publies · 1 = jeton absent, fichier manquant, ou refus du
      serveur. **Et un de ses appels peut ne pas revenir : `api` leve sur une
      panne de reseau.**
      [sort: oui]
    """
    racine = sys.argv[1] if len(sys.argv) > 1 else "."
    jeton = os.environ.get("GH_TOKEN", "")
    if not jeton:
        print("CODE 1 — GH_TOKEN absent : le secret TOKEN_PUBLIC n'est pas posé")
        sys.exit(1)
    echecs = 0
    for src, dst in A_PUBLIER:
        chemin = os.path.join(racine, src)
        if not os.path.isfile(chemin):
            print(f"  ⚠️ {src} absent du dépôt — non publié"); echecs += 1; continue
        contenu = open(chemin, "rb").read()
        # l'empreinte du fichier déjà publié est exigée par l'API pour écraser
        code, rep = api("GET", f"https://api.github.com/repos/{PUBLIC}/contents/{dst}", jeton=jeton)
        sha = rep.get("sha") if code == 200 else None
        corps = {"message": f"maj {dst}", "content": base64.b64encode(contenu).decode()}
        if sha:
            corps["sha"] = sha
        code, rep = api("PUT", f"https://api.github.com/repos/{PUBLIC}/contents/{dst}", corps, jeton)
        if code in (200, 201):
            print(f"  ✅ {dst} publié — {len(contenu)} octets")
        else:
            print(f"  ❌ {dst} — HTTP {code} : {rep.get('message','?')}"); echecs += 1
    print(f"\nadresse de lecture, sans jeton : https://raw.githubusercontent.com/{PUBLIC}/main/<fichier>")
    sys.exit(1 if echecs else 0)


if __name__ == "__main__":
    main()
