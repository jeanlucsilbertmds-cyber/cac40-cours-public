"""Lance le protocole de verification des chiffres et fabrique le bandeau d'etat du cockpit.

① RÔLE — Le systeme affiche des chiffres de performance : nombre de trades, taux de
  reussite, gain net en euros. Ce module apporte la garantie que ces chiffres ont ete
  recalcules par un second jeu de programmes et compares avant d'etre montres. Il ne
  calcule lui-meme aucun chiffre : il recopie huit fichiers, lance un programme
  exterieur, `runner_protocole_v1.py`, retient son verdict et sait le peindre en vert,
  en rouge ou en orange sur la page du cockpit.
② CONTEXTE D'APPEL — Le texte livre a l'origine en tete de ce fichier decrit un appel
  depuis `projet_cac40.run()`, avant tout calcul, sous la forme
  `from protocole_qualite import executer_protocole_si_necessaire` puis
  `executer_protocole_si_necessaire()`. **Aucun appelant n'existe dans ce depot.** La
  recherche du mot `protocole_qualite` dans les 34 programmes de `programmes/`, menee le
  19-09-2026, rend trois fichiers qui le NOMMENT sans jamais l'importer :
  `FABRIQUER_LE_SOCLE.py`, `EPREUVES_DU_SOCLE.py` et `audit_ecosysteme.py`. Le fichier ne
  porte pas non plus de bloc `if __name__ == "__main__"` : il ne se lance pas seul.
③ ENTRÉE — Aucun argument de ligne de commande. Quatre valeurs ecrites en dur dans le
  fichier : `PROTOCOLE_DIR`, le dossier source /mnt/user-data/outputs/PROTOCOLE_v1 ·
  `HOME`, le dossier de travail /home/claude · `STATUS_FILE`, le fichier de memoire
  /home/claude/_protocole_status.json · `FICHIERS_PROTOCOLE`, la liste des huit noms a
  recopier, de `CONVENTIONS_FIGEES_v1.md` a `runner_protocole_v1.py`.
④ CONDITIONS D'ENTRÉE — Le dossier source doit exister, sinon le module renonce et le
  dit sans rien bloquer. Le dossier /home/claude doit exister et accepter l'ecriture : le
  module ne le cree pas. L'interpreteur `python3` doit etre appelable par son seul nom.
⑤ SORTIE — Le module ne rend rien a l'import. Il expose quatre fonctions : `hash_dir`
  (UNE valeur, une empreinte de 16 caracteres) · `synchroniser_protocole_local` (DEUX
  valeurs, un booleen et un texte) · `executer_protocole_si_necessaire` (UNE valeur, un
  dictionnaire de quatre formes possibles) · `bandeau_html_protocole` (UNE valeur, une
  chaine HTML de quatre formes possibles, dont la chaine vide).
⑥ TRAITEMENT — ① recopier les huit fichiers du protocole du dossier source vers
  /home/claude · ② calculer une empreinte de leur contenu · ③ relire le verdict du
  dernier passage et renoncer a relancer si rien n'a change depuis moins de 30 minutes ·
  ④ sinon lancer `runner_protocole_v1.py` et l'attendre au plus 300 secondes ·
  ⑤ enregistrer le verdict dans /home/claude/_protocole_status.json · ⑥ afficher le
  resultat a la console · ⑦ a la demande, fabriquer le bandeau HTML qui porte ce verdict.
⑦ UNITÉ — L'empreinte est un NOMBRE HEXADECIMAL de 16 caracteres. L'age du dernier
  verdict est en MINUTES, avec un seuil de 30. Le delai d'attente du programme lance est
  en SECONDES, 300, soit 5 minutes. Les extraits de sortie conserves se comptent en
  CARACTERES : 1 500 pour la sortie normale, 500 pour la sortie d'erreur. Les chiffres
  affiches a la fin viennent du protocole : `n` est un nombre de trades, `wr` un
  pourcentage, `net_50bps` un montant en euros.
⑧ POURQUOI — Un chiffre calcule une seule fois par un seul programme ne se verifie pas :
  deux implementations d'une meme chose divergent toujours (R-708). Le protocole fait
  donc recalculer les memes trades par un second moteur et compare les deux resultats,
  et ce module refuse de laisser afficher les chiffres sans dire si cette comparaison a
  eu lieu. **Il n'interrompt jamais le programme qui l'appelle** : un protocole
  indisponible ferait alors tomber toute la chaine du soir, alors que le seul besoin est
  de savoir que les chiffres ne sont pas garantis. L'avertissement remplace le blocage.
⑨ CE QUI CLOCHE —
  · **Les trois chemins sont ecrits en dur et absolus, et aucun n'existe ici.** Le
    19-09-2026, `ls /mnt/user-data/outputs/PROTOCOLE_v1` rend « No such file or
    directory », et la recherche des huit noms de `FICHIERS_PROTOCOLE` dans tout le depot
    ne rend aucun fichier. Consequence : appele aujourd'hui, le module s'arrete a son
    premier pas et rend `{"ok": False}` ; le bandeau reste orange quoi qu'il arrive. Le
    protocole qu'il pilote n'est pas dans le depot.
  · **`os` et `sys` sont importes et jamais employes** (lignes 21 et 23) : le fichier ne
    contient aucune occurrence de `os.` ni de `sys.`, mesure faite le 19-09-2026 sur les
    204 lignes du fichier.
  · **Le texte livre a l'origine en tete annoncait « Si CONVENTIONS_FIGEES_v1.md absent →
    ecrit un message d'alerte ».** Le code ne regarde jamais ce fichier : il teste
    l'existence du DOSSIER. Un dossier present d'ou ce fichier a disparu passe sans un
    mot, et le protocole tourne sans ses conventions.
  · **Le meme texte annoncait « lance une fois par session ».** Le code n'a aucune notion
    de session : il compare une empreinte et une duree de 30 minutes. Deux sessions qui
    se suivent dans la meme demi-heure ne relancent rien ; une session de trois heures
    relance six fois.
⑩ EFFET — ÉCRASE jusqu'a huit fichiers dans /home/claude, sans sauvegarde ni
  avertissement · ÉCRIT et ecrase /home/claude/_protocole_status.json · LANCE un
  processus exterieur qui peut lui-meme ecrire ce qu'il veut · affiche des lignes a la
  console. Il ne touche a aucun fichier du depot, ni aux cours, ni aux positions, ni au
  journal des trades. Aucun acces reseau.
⑪ TERMINAISON — Le module rend la main a l'import et aucune de ses fonctions n'appelle
  `sys.exit` : rien ici ne se termine par un code de sortie. Un de ses appels peut ne pas
  revenir avant longtemps : `subprocess.run` attend le programme lance, au plus 300
  secondes, et le depassement est rattrape. Si `python3` est introuvable, le meme appel
  leve `FileNotFoundError`, que rien ne rattrape et qui remonte a l'appelant.
⑫ DÉFINITIONS
  le cockpit : la page web que ce programme fabrique et que Jean-Luc ouvre pour voir l etat du systeme.
  le protocole : la chaine de verification exterieure a ce module — moteur de reference,
    moteur alternatif, comparaison, tests, invariances, juge critique
  le runner : `runner_protocole_v1.py`, le programme qui enchaine ces pas et dont le code
    de sortie vaut verdict
  l'empreinte : le nombre SHA-256 calculé sur le contenu d'un fichier ; deux fichiers de même empreinte ont le même contenu
  le bandeau : la boite de couleur inseree en haut du cockpit pour porter un verdict
  un trade : une opération simulée, de l'achat à la revente
  la chaine du soir : la suite de pas lancee chaque soir a 20h — collecte, signaux, positions, mesure, cockpit
  le depot : le depot GitHub ou vivent les fichiers du systeme, le projet n'en etant qu'une copie de lecture
  une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
import json
import os
import subprocess
import sys
import hashlib
from datetime import datetime
from pathlib import Path


PROTOCOLE_DIR = Path("/mnt/user-data/outputs/PROTOCOLE_v1")
STATUS_FILE = Path("/home/claude/_protocole_status.json")
HOME = Path("/home/claude")

FICHIERS_PROTOCOLE = [
    "CONVENTIONS_FIGEES_v1.md",
    "moteur_reference_v1.py",
    "moteur_alternatif_v1.py",
    "comparaison_moteurs.py",
    "tests_non_regression.py",
    "audit_invariances.py",
    "juge_critique.py",
    "runner_protocole_v1.py",
]


def hash_dir(d: Path, files: list) -> str:
    """Calcule une empreinte unique du contenu des huit fichiers du protocole.

    ① RÔLE — Donner une identite courte a l'ensemble des fichiers du protocole, pour
      repondre a une seule question : est-ce toujours exactement le meme protocole que la
      derniere fois ? C'est ce qui permet de ne pas relancer 5 minutes de calcul pour
      rien, et de relancer des qu'un octet a bouge.
    ② CONTEXTE D'APPEL — `executer_protocole_si_necessaire`, une fois par passage, juste
      apres la recopie des fichiers en local et avant la decision de relancer.
    ③ ENTRÉE — `d` : le dossier ou lire les fichiers · `files` : la liste des noms de
      fichiers a prendre en compte. **Un seul appelant, et il passe toujours `HOME`, soit
      /home/claude, et `FICHIERS_PROTOCOLE`, les huit noms.** Le dossier source
      /mnt/user-data/outputs/PROTOCOLE_v1 n'est jamais pese : c'est la copie de travail
      qui l'est.
    ④ CONDITIONS D'ENTRÉE — `d` doit etre un chemin `Path`. Les fichiers absents sont
      admis : ils sont sautes sans erreur. Les fichiers presents doivent etre lisibles.
    ⑤ SORTIE — **UNE valeur : une chaine de 16 caracteres hexadecimaux**, par exemple
      `e3b0c44298fc1c14`.
      [rend: 1]
    ⑥ TRAITEMENT — ① trier les noms recus par ordre alphabetique · ② pour chaque nom
      present dans le dossier, ajouter le contenu du fichier au calcul en cours · ③ rendre
      les 16 premiers caracteres de l'empreinte SHA-256 obtenue.
    ⑦ UNITÉ — 16 caracteres hexadecimaux, soit 64 bits conserves sur les 256 calcules.
    ⑧ POURQUOI — **Le tri des noms rend le resultat independant de l'ordre de la liste
      recue** : la meme liste ecrite dans un autre ordre donnerait sinon une autre
      empreinte, et le protocole serait relance sans raison. **La coupe a 16 caracteres**
      tient a l'usage : cette valeur sert a comparer deux passages, pas a verrouiller quoi
      que ce soit, et elle est affichee a l'ecran puis reduite a 8 caracteres dans le
      bandeau du cockpit.
    ⑨ CE QUI CLOCHE —
      · **Un fichier absent est saute en silence.** Si `juge_critique.py` n'a jamais ete
        recopie, l'empreinte est calculee sur sept fichiers et rien ne distingue ce cas
        d'un protocole complet. Cas limite mesure le 19-09-2026 : sur un dossier ou aucun
        des huit fichiers n'existe, la fonction rend `e3b0c44298fc1c14`, qui est
        l'empreinte SHA-256 de rien du tout. Cette valeur d'apparence normale peut etre
        comparee a celle du passage precedent et faire conclure « rien n'a change ».
      · **Les contenus sont mis bout a bout sans separateur et sans les noms de
        fichiers.** Deux repartitions differentes du meme texte total donnent donc la
        meme empreinte : recopier les lignes de `juge_critique.py` a la fin de
        `audit_invariances.py` puis supprimer le premier fichier ne change pas la valeur
        rendue, alors que le protocole n'est plus le meme.
    ⑩ EFFET — LIT jusqu'a huit fichiers. N'ecrit rien, n'affiche rien, ne touche au
      reseau en rien.
    ⑪ TERMINAISON — Rend toujours la main, sauf si un fichier present ne se lit pas :
      `read_bytes` leve alors — `PermissionError` par exemple — et l'erreur remonte a
      l'appelant, que rien ne protege. Aucun de ses appels ne se termine de lui-meme.
      [sort: non]
    ⑫ DÉFINITIONS
      le protocole : la chaine de verification exterieure a ce module — moteur de
        reference, moteur alternatif, comparaison, tests, invariances, juge critique
      l'empreinte : le nombre SHA-256 calculé sur le contenu d'un fichier ; deux fichiers de même empreinte ont le même contenu
      le cockpit : la page web que ce programme fabrique et que Jean-Luc ouvre pour voir l etat du systeme.
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    h = hashlib.sha256()
    for fn in sorted(files):
        p = d / fn
        if p.exists():
            h.update(p.read_bytes())
    return h.hexdigest()[:16]


def synchroniser_protocole_local():
    """Recopie les huit fichiers du protocole du dossier source vers /home/claude.

    ① RÔLE — Amener les fichiers du protocole la ou ils seront lus et lances, et signaler
      d'un mot si la source est introuvable. Sans ce pas, le programme lance chercherait
      ses voisins dans un dossier ou ils ne sont pas.
    ② CONTEXTE D'APPEL — `executer_protocole_si_necessaire`, en tout premier geste, avant
      le calcul de l'empreinte et avant toute decision de relance.
    ③ ENTRÉE — Aucun parametre. Elle lit trois valeurs ecrites en dur dans le fichier :
      `PROTOCOLE_DIR`, le dossier source /mnt/user-data/outputs/PROTOCOLE_v1 · `HOME`, le
      dossier de destination /home/claude · `FICHIERS_PROTOCOLE`, les huit noms.
    ④ CONDITIONS D'ENTRÉE — Le dossier /home/claude doit exister et accepter l'ecriture :
      la fonction ne le cree pas et ne verifie pas qu'il est la.
    ⑤ SORTIE — **DEUX valeurs, toujours un couple** : un booleen et un texte. Deux formes
      seulement : `(False, "PROTOCOLE_v1/ absent : ...")` quand le dossier source manque,
      et `(True, "OK")` dans tous les autres cas.
      [rend: 2]
    ⑥ TRAITEMENT — ① si le dossier source n'existe pas, rendre l'echec accompagne du
      chemin cherche · ② pour chacun des huit noms, si le fichier existe a la source, le
      recopier octet pour octet sur le fichier de meme nom dans /home/claude · ③ rendre
      le succes.
    ⑦ UNITÉ — —
    ⑧ POURQUOI — **La copie se fait en octets et non en texte.** Un fichier recopie en
      texte peut changer de fin de ligne ou d'encodage selon la machine : son contenu
      serait alors different a l'octet sans qu'une seule instruction ait bouge,
      l'empreinte changerait a chaque passage, et les 5 minutes du protocole seraient
      relancees pour rien a chaque appel.
    ⑨ CE QUI CLOCHE —
      · **Un fichier manquant a la source est saute sans un mot, et le couple rendu reste
        `(True, "OK")`.** La copie precedente, plus ancienne, reste alors en place dans
        /home/claude : c'est elle qui sera pesee par le calcul d'empreinte et employee par
        le programme lance. Le protocole tourne sur une version que personne n'a voulue,
        et le verdict porte sur elle.
      · **La fonction rend `(True, "OK")` meme quand elle n'a recopie aucun fichier.** Il
        suffit que le dossier source existe et soit vide : le succes est annonce, et
        l'empreinte calculee ensuite vaut `e3b0c44298fc1c14`, celle de rien du tout.
    ⑩ EFFET — **ÉCRASE jusqu'a huit fichiers dans /home/claude**, sans sauvegarde ni
      avertissement. Ne touche a aucun fichier du depot ni a aucune donnee de cours ou de
      trade. Aucun acces reseau. N'affiche rien : elle rend son motif a l'appelant.
    ⑪ TERMINAISON — Rend la main dans les deux cas prevus. Elle leve si /home/claude
      n'existe pas ou refuse l'ecriture — `FileNotFoundError` ou `PermissionError` — et
      rien ne rattrape ici. Aucun de ses appels ne se termine de lui-meme.
      [sort: non]
    ⑫ DÉFINITIONS
      le protocole : la chaine de verification exterieure a ce module — moteur de
        reference, moteur alternatif, comparaison, tests, invariances, juge critique
      l'empreinte : le nombre SHA-256 calculé sur le contenu d'un fichier ; deux fichiers de même empreinte ont le même contenu
      un trade : une opération simulée, de l'achat à la revente
    """
    if not PROTOCOLE_DIR.exists():
        return False, f"PROTOCOLE_v1/ absent : {PROTOCOLE_DIR}"
    for fn in FICHIERS_PROTOCOLE:
        src = PROTOCOLE_DIR / fn
        dst = HOME / fn
        if src.exists():
            dst.write_bytes(src.read_bytes())
    return True, "OK"


def executer_protocole_si_necessaire(force=False):
    """Relance le protocole si quelque chose a change, et enregistre son verdict.

    ① RÔLE — **C'est la porte d'entree du module.** Elle repond a la question « peut-on
      afficher les chiffres ? » en relancant la verification quand c'est utile, en
      l'evitant quand elle vient d'etre faite, et en laissant derriere elle une trace
      ecrite du verdict que le bandeau du cockpit ira relire.
    ② CONTEXTE D'APPEL — Le texte livre a l'origine en tete de ce fichier la place au
      debut de `projet_cac40.run()`, avant tout calcul. **Aucun appelant n'existe dans ce
      depot** : la recherche du mot `executer_protocole_si_necessaire` dans les 34
      programmes de `programmes/`, menee le 19-09-2026, ne rend que ce fichier-ci ; aucun
      autre programme ne l'importe ni ne l'appelle.
    ③ ENTRÉE — `force` : un booleen, faux par defaut ; vrai, il fait relancer le protocole
      meme si le dernier verdict est vert, recent et porte la meme empreinte. **Aucun
      appelant connu : aucune valeur reellement passee n'a pu etre relevee.**
    ④ CONDITIONS D'ENTRÉE — L'interpreteur `python3` doit etre appelable par son seul nom.
      /home/claude doit exister et accepter l'ecriture. Le fichier lance,
      `runner_protocole_v1.py`, doit rendre 0 pour dire que tout va bien et autre chose
      pour dire l'echec.
    ⑤ SORTIE — **UNE valeur, un dictionnaire — mais de QUATRE formes differentes selon la
      branche, et l'appelant ne peut pas les confondre impunement** :
      · dossier source absent → DEUX cles, `ok` (faux) et `raison`
      · verdict recent reutilise → **le dictionnaire relu du fichier de statut, rendu tel
        quel** : ses cles sont celles du passage precedent, inconnues a l'avance
      · delai depasse → DEUX cles, `ok` (faux) et `raison` valant `"timeout"`
      · protocole reellement lance → QUATRE cles toujours — `ok`, `hash`,
        `derniere_execution`, `exit_code` — plus `csv_sha256` et `resultats_resume` quand
        il est vert, plus `stderr_tail` et `stdout_tail` quand il est rouge.
      Un appelant qui veut lire `resultats_resume` doit donc verifier sa presence avant.
      [rend: 1]
    ⑥ TRAITEMENT — ① afficher l'en-tete du protocole · ② recopier les huit fichiers en
      local · ③ renoncer, sans bloquer, si la copie a echoue · ④ calculer l'empreinte des
      fichiers locaux · ⑤ relire le verdict du passage precedent, en ignorant un fichier
      illisible · ⑥ renoncer a relancer si ce verdict est vert, porte la meme empreinte et
      a moins de 30 minutes · ⑦ sinon lancer `runner_protocole_v1.py`, en capturant ses
      sorties et en l'attendant au plus 300 secondes · ⑧ construire le statut a partir de
      son code de sortie · ⑨ y joindre le resume des resultats quand il est vert, les
      1 500 derniers caracteres de sortie et les 500 derniers d'erreur quand il est rouge ·
      ⑩ ecrire ce statut dans /home/claude/_protocole_status.json · ⑪ afficher le bilan.
    ⑦ UNITÉ — L'age du dernier verdict est en MINUTES, seuil 30. Le delai d'attente est en
      SECONDES, 300, soit 5 minutes. Les extraits conserves sont en CARACTERES, 1 500 et
      500. Dans les lignes affichees, `N` est un nombre de trades, `WR` un pourcentage a
      une decimale, `Net` un montant en euros arrondi a l'unite.
    ⑧ POURQUOI — **Deux garde-fous decident de la relance, et ils ne disent pas la meme
      chose.** L'empreinte repond « les fichiers du protocole ont-ils change ? » ; les 30
      minutes repondent « le verdict est-il encore frais ? ». Le premier seul laisserait
      un verdict vieux d'un jour passer pour valide tant que personne ne touche aux
      fichiers ; le second seul relancerait 5 minutes de calcul toutes les demi-heures
      sans qu'une ligne ait bouge. **Et l'echec ne bloque jamais l'appelant** : la fonction
      rend un dictionnaire, jamais une erreur ni un arret, parce qu'un protocole
      indisponible ne doit pas faire tomber la chaine du soir — il doit seulement empecher
      de croire les chiffres.
    ⑨ CE QUI CLOCHE —
      · **Deux chemins d'echec sur trois n'ecrivent pas le fichier de statut.** Le dossier
        source absent rend sans ecrire, le delai depasse rend sans ecrire ; seul l'echec du
        programme lance est enregistre. Le fichier
        /home/claude/_protocole_status.json garde donc son contenu precedent, `"ok": true`
        compris, et le bandeau du cockpit reste VERT alors que le protocole vient
        d'echouer. Un verdict vert vieux d'une semaine survit a ces deux echecs.
      · **Le chemin du delai depasse n'affiche pas la ligne de fermeture** — les 80 tirets
        et la ligne vide — que tous les autres chemins affichent. A la console, l'en-tete
        du protocole reste ouvert et la suite de la chaine du soir s'imprime a l'interieur,
        ce qui donne a lire un bloc protocole qui ne se referme jamais.
      · **Le resume des resultats exige six cles — `id`, `n`, `wr`, `net_50bps`, `score`,
        `statut` — et le filet tendu autour ne rattrape que les erreurs de lecture JSON et
        de fichier.** Une cle manquante leve `KeyError`, que rien ne rattrape et qui remonte
        a l'appelant. Cela se produit APRES un protocole reussi et AVANT l'ecriture du
        statut : le protocole est passe, il est vert, et il n'en reste aucune trace.
      · **La date du verdict est enregistree sans fuseau horaire** : `datetime.now()` rend
        par exemple `2026-09-19T20:36:24.610994`, sans indication de pays. Le systeme exige
        pourtant un horodatage Europe/Paris dans chaque en-tete et chaque nom de fichier.
        Deux machines reglees sur des fuseaux differents lisent alors deux ages differents
        dans le meme fichier de statut, et la fenetre de 30 minutes s'ouvre ou se ferme a
        tort.
      · **Le montant affiche porte le nom `net_50bps`, ou 50 points de base valent 0,50 %,
        alors que le courtage du systeme vaut 0,15 % par ordre** — releve le 19-09-2026
        dans `MODULE_POSITIONS.py`, `FRAIS_TAUX = 0.0015`, tarif Fortuneo Progress ; depuis
        le 29-10-2026 (A-550), le bareme date `donnees/BAREME_FRAIS.csv`, taxe sur les
        transactions financieres comprise pour les valeurs taxees. Le fichier qui produit
        cette cle, `resultats_reference_v1.json`, n'existe pas dans le depot : **je n'ai
        pas pu etablir si les deux nombres parlent de la meme chose.** Si ce sont bien les
        memes frais, un des deux chiffres est faux et un chiffre qui existe ailleurs ne se
        recopie pas (R-708).
    ⑩ EFFET — **ÉCRASE jusqu'a huit fichiers dans /home/claude** par la recopie ·
      **ÉCRIT et ecrase /home/claude/_protocole_status.json** · **LANCE un processus
      `python3` exterieur**, qui peut a son tour ecrire ce qu'il veut · affiche une
      quinzaine de lignes a la console. Elle ne touche a aucun fichier du depot, ni aux
      cours, ni aux positions, ni au journal des trades. Aucun acces reseau de son fait.
    ⑪ TERMINAISON — **Rend toujours la main sur ses quatre chemins prevus** : elle
      n'appelle jamais `sys.exit` et ne se termine par aucun code de sortie. **Un de ses
      appels peut ne pas revenir avant 300 secondes** : `subprocess.run` attend le
      programme lance, et le depassement est rattrape. Elle leve, en revanche, dans trois
      cas que rien ne rattrape : `python3` introuvable (`FileNotFoundError`), une cle
      absente du fichier de resultats (`KeyError`), un fichier de statut qui n'est pas du
      texte lisible (`UnicodeDecodeError`, qui n'est ni une erreur JSON ni une erreur
      systeme).
      [sort: non]
    ⑫ DÉFINITIONS
      le protocole : la chaine de verification exterieure a ce module — moteur de
        reference, moteur alternatif, comparaison, tests, invariances, juge critique
      le runner : `runner_protocole_v1.py`, le programme qui enchaine ces pas et dont le
        code de sortie vaut verdict
      l'empreinte : le nombre SHA-256 calculé sur le contenu d'un fichier ; deux fichiers de même empreinte ont le même contenu
      le cockpit : la page web que ce programme fabrique et que Jean-Luc ouvre pour voir l etat du systeme.
      la chaine du soir : la suite de pas lancee chaque soir a 20h — collecte, signaux,
        positions, mesure, cockpit
      un trade : une opération simulée, de l'achat à la revente
    
      le bandeau : la boite de couleur inseree en haut du cockpit pour porter un verdict
      le depot : le depot GitHub ou vivent les fichiers du systeme, le projet n'en etant qu'une copie de lecture
      un bloc : une suite de lignes qui se suivent dans le texte et dont les dates décroissent sans trou plus grand que six jours.
      une trace : le fichier qu'une tâche planifiée laisse derrière elle quand elle a tourné — rapport de boucle, rapport d'audit, cockpit, historique des mesures.
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    print("\n" + "─" * 80)
    print("🛡  PROTOCOLE DE VÉRIFICATION SCIENTIFIQUE OBSESSIONNELLE — auto-check")
    print("─" * 80)

    # 1. Synchroniser le protocole en local
    ok_sync, msg = synchroniser_protocole_local()
    if not ok_sync:
        print(f"⚠ {msg}")
        print("⚠ Le protocole de vérification n'est pas disponible — exécution non bloquée")
        print("─" * 80 + "\n")
        return {"ok": False, "raison": msg}

    # 2. Vérifier hash actuel
    h_actuel = hash_dir(HOME, FICHIERS_PROTOCOLE)

    # 3. Charger statut précédent
    statut_prec = {}
    if STATUS_FILE.exists():
        try:
            statut_prec = json.loads(STATUS_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass

    # 4. Si déjà passé avec le même hash et < 30 min, skip (éviter relances inutiles)
    derniere = statut_prec.get("derniere_execution")
    if (not force
            and statut_prec.get("hash") == h_actuel
            and statut_prec.get("ok") is True
            and derniere):
        try:
            d = datetime.fromisoformat(derniere)
            age_min = (datetime.now() - d).total_seconds() / 60
            if age_min < 30:
                print(f"✅ Protocole déjà validé il y a {age_min:.0f} min "
                      f"(hash {h_actuel}) — skip")
                print("─" * 80 + "\n")
                return statut_prec
        except (ValueError, TypeError):
            pass

    # 5. Lancer le runner
    print(f"⏵ Lancement du runner ({h_actuel})...")
    try:
        result = subprocess.run(
            ["python3", str(HOME / "runner_protocole_v1.py")],
            capture_output=True, text=True, timeout=300,
        )
    except subprocess.TimeoutExpired:
        print("❌ Timeout (>5 min) — protocole non validé")
        return {"ok": False, "raison": "timeout"}

    succes = result.returncode == 0

    # 6. Stocker statut
    statut = {
        "ok": succes,
        "hash": h_actuel,
        "derniere_execution": datetime.now().isoformat(),
        "exit_code": result.returncode,
    }
    if succes:
        # Lire les résultats de référence pour les avoir dans le statut
        try:
            ref_path = HOME / "resultats_reference_v1.json"
            if ref_path.exists():
                ref = json.loads(ref_path.read_text())
                statut["csv_sha256"] = ref.get("csv_sha256")
                statut["resultats_resume"] = [
                    {"id": r["id"], "n": r["n"], "wr": r["wr"],
                     "net_50bps": r["net_50bps"], "score": r["score"],
                     "statut": r["statut"]}
                    for r in ref.get("resultats", [])
                ]
        except (json.JSONDecodeError, OSError):
            pass
    else:
        statut["stderr_tail"] = result.stderr[-500:] if result.stderr else ""
        statut["stdout_tail"] = result.stdout[-1500:] if result.stdout else ""

    STATUS_FILE.write_text(json.dumps(statut, indent=2, default=str))

    # 7. Affichage
    if succes:
        print("\n✅ PROTOCOLE VALIDÉ — chiffres officiels :")
        for r in statut.get("resultats_resume", []):
            print(f"    {r['id']:25s} N={r['n']:3d} WR={r['wr']:.1%} "
                  f"Net={r['net_50bps']:+9.0f}€ → {r['statut']}")
    else:
        print(f"\n❌ PROTOCOLE EN ÉCHEC (exit code {result.returncode})")
        if statut.get("stdout_tail"):
            print("\n--- dernières sorties ---")
            print(statut["stdout_tail"])
        print("\n⚠ NE PAS UTILISER les chiffres tant que le protocole n'est pas vert.")
    print("─" * 80 + "\n")
    return statut


def bandeau_html_protocole() -> str:
    """Fabrique la boite de couleur qui annonce l'etat du protocole en haut du cockpit.

    ① RÔLE — **Porter le verdict du protocole sur la page que Jean-Luc regarde.** Sans
      cette boite, le cockpit affiche des chiffres sans dire s'ils ont ete verifies : un
      taux de reussite non valide y ressemble trait pour trait a un taux valide.
    ② CONTEXTE D'APPEL — Au moment de fabriquer la page du cockpit, le texte rendu devant
      etre insere en haut de la page. **Aucun appelant n'existe dans ce depot** : la
      recherche du mot `bandeau_html_protocole` dans les 34 programmes de `programmes/`,
      menee le 19-09-2026, ne rend que sa propre ligne de definition.
    ③ ENTRÉE — Aucun parametre. Elle lit une seule chose : le fichier
      /home/claude/_protocole_status.json, ecrit par `executer_protocole_si_necessaire`.
    ④ CONDITIONS D'ENTRÉE — Aucune. Les trois etats du fichier sont prevus : absent,
      present mais illisible, present et lisible.
    ⑤ SORTIE — **UNE valeur, une chaine de caracteres — sous QUATRE formes** : un bandeau
      ORANGE si le fichier n'existe pas · **une chaine VIDE si le fichier existe mais ne
      se lit pas** · un bandeau VERT si le verdict enregistre est bon · un bandeau ROUGE
      sinon.
      [rend: 1]
    ⑥ TRAITEMENT — ① si le fichier de statut est absent, rendre le bandeau orange
      « non encore execute » · ② le lire, et rendre une chaine vide s'il ne se lit pas ·
      ③ si le verdict est bon, couper la date a la seconde et les deux empreintes a 8
      caracteres, puis rendre le bandeau vert qui les porte · ④ sinon, rendre le bandeau
      rouge qui porte le code de sortie du programme lance.
    ⑦ UNITÉ — Les coupes sont en CARACTERES : 19 pour la date, ce qui la laisse a la
      seconde, et 8 pour chacune des deux empreintes. Les tailles du style sont en PIXELS
      pour les marges et le trait de gauche, en pixels aussi pour le texte — 11 pour les
      bandeaux vert et orange, 12 pour le rouge.
    ⑧ POURQUOI — **Le style est ecrit dans la balise elle-meme, sans feuille de style ni
      fichier exterieur** : la page du cockpit ne doit dependre d'aucun chargement reseau,
      puisqu'elle est consultee depuis un iPhone et doit s'afficher entiere meme sans
      reseau. **Les empreintes sont coupees a 8 caracteres** parce qu'elles servent a
      comparer deux affichages d'un coup d'oeil, pas a verrouiller quoi que ce soit.
      **Le bandeau rouge est ecrit plus gros que les deux autres** — 12 pixels contre 11 —
      parce qu'il est le seul qui demande de ne pas se servir des chiffres affiches en
      dessous.
    ⑨ CE QUI CLOCHE —
      · **Un fichier de statut illisible rend une chaine VIDE.** Le cockpit n'affiche
        alors AUCUN bandeau, ce qui se lit comme une page sans protocole et non comme un
        protocole dont l'etat est inconnu. C'est le seul des quatre cas qui n'avertit de
        rien, alors que l'autre cas d'ignorance — fichier absent — affiche, lui, un bandeau
        orange.
      · **L'age du verdict n'est jamais regarde.** La date est affichee, mais rien ne la
        compare au jour courant : un verdict vert du 12-09 s'affiche le 19-09 dans les
        memes termes et la meme couleur, a sept jours de distance.
      · **Le bandeau vert affirme « Tous les chiffres affiches ci-dessous proviennent de
        resultats_reference_v1.json ».** Cette fonction ne verifie rien de tel : elle ne
        lit pas le cockpit et ne sait pas d'ou viennent les chiffres imprimes a cote
        d'elle. La phrase est ecrite d'avance, et elle sera affichee meme si le cockpit
        tire ses nombres d'ailleurs.
    ⑩ EFFET — LIT un fichier, /home/claude/_protocole_status.json. N'ecrit rien,
      n'affiche rien, ne touche au reseau en rien. Le texte rendu est destine a etre
      insere tel quel dans une page HTML.
    ⑪ TERMINAISON — Rend toujours la main sur ses quatre chemins. Elle leve si le fichier
      de statut n'est pas du texte lisible : `read_text` rend alors `UnicodeDecodeError`,
      qui n'est ni une erreur JSON ni une erreur systeme et n'est donc pas rattrapee.
      Aucun de ses appels ne se termine de lui-meme.
      [sort: non]
    ⑫ DÉFINITIONS
      le cockpit : la page web que ce programme fabrique et que Jean-Luc ouvre pour voir l etat du systeme.
      le protocole : la chaine de verification exterieure a ce module — moteur de
        reference, moteur alternatif, comparaison, tests, invariances, juge critique
      le bandeau : la boite de couleur inseree en haut du cockpit pour porter un verdict
      l'empreinte : le nombre SHA-256 calculé sur le contenu d'un fichier ; deux fichiers de même empreinte ont le même contenu
    
      une valeur : une entreprise cotée du CAC 40, telle qu'elle est nommée dans les fichiers du projet
"""
    if not STATUS_FILE.exists():
        return (
            '<div style="background:#3a1500;border-left:4px solid #ff8800;'
            'padding:12px 18px;margin:14px 0;font-size:11px;color:#ffb968;">'
            '⚠ Protocole de vérification scientifique non encore exécuté.'
            '</div>'
        )
    try:
        s = json.loads(STATUS_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return ''
    if s.get("ok"):
        d = s.get("derniere_execution", "")[:19]
        h = s.get("hash", "")[:8]
        csv_h = (s.get("csv_sha256") or "")[:8]
        return (
            '<div style="background:#0a2818;border-left:4px solid #2eb88a;'
            'padding:12px 18px;margin:14px 0;font-size:11px;color:#7feab0;">'
            f'✅ Protocole de vérification scientifique <strong>v1 validé</strong> '
            f'le {d} (hash protocole {h}, hash CSV {csv_h}).<br>'
            '<span style="color:#a0a0a0;">Tous les chiffres affichés ci-dessous '
            'proviennent de <code>resultats_reference_v1.json</code>.</span>'
            '</div>'
        )
    else:
        return (
            '<div style="background:#3a0000;border-left:4px solid #ff3333;'
            'padding:12px 18px;margin:14px 0;font-size:12px;color:#ff9090;">'
            '❌ <strong>PROTOCOLE EN ÉCHEC</strong> — '
            f'exit code {s.get("exit_code", "?")}. '
            'Les chiffres affichés ci-dessous ne sont PAS validés. '
            'À ne pas utiliser pour décision.'
            '</div>'
        )
