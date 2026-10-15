#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fabrique le releve des prompts des taches planifiees, texte compris.

① ROLE — **Porter au depot le texte EXACT des taches planifiees.** Les taches
  vivent hors du depot, chez l hebergeur ; leur texte n est visible nulle part
  ailleurs. Sans ce releve, la mesure de perimetre croit que seul le circuit du
  soir fait tourner le systeme, et range parmi les dormants les programmes que
  les taches lancent.
② CONTEXTE D APPEL — A la main, apres toute dictee d un prompt de tache, et
  avant toute mesure de perimetre. **Aucun pas du circuit du soir ne le lance.**
③ ENTREE — La ligne de commande, trois arguments : `SRC`, le fichier JSON rendu
  par l outil de liste des taches · `DST`, le fichier a ecrire · et, en
  troisieme, l horodatage unix en secondes de l instant ou la source a ete lue.
  **Le troisieme est facultatif ; a defaut, l instant d ecriture est employe.**
④ CONDITIONS D ENTREE — `SRC` doit exister et porter une cle `data` qui est une
  liste. Chaque entree porte un `name` et un `id`. **Les deux premiers arguments
  sont obligatoires : sans eux le programme s arrete sur une erreur brute.**
⑤ SORTIE — **Un code de sortie, et rien d autre.** 0 si tous les textes sont
  ressortis octet pour octet, 1 sinon. Le fichier, lui, est ecrit dans `DST`.
⑥ TRAITEMENT — ① lire le JSON et trier les taches par nom · ② composer l en-tete
  et le sommaire, une ligne par tache avec sa taille et son empreinte courte ·
  ③ ecrire le texte integral de chaque tache entre deux barrieres nommees ·
  ④ ecrire le fichier · ⑤ **le relire et comparer chaque texte extrait au texte
  d origine** · ⑥ afficher le verdict tache par tache.
⑦ UNITE — Les tailles sont en OCTETS, jamais en caracteres : un texte francais
  pese plus d octets que de lettres. Les empreintes sont des sha256, affichees
  en 16 caracteres au sommaire et en entier dans la fiche de chaque tache.
⑧ POURQUOI — **Le texte ne transite jamais par la redaction.** Il est copie
  depuis la source, puis relu depuis le fichier ecrit et compare. Une recopie a
  la main d un prompt de 9 000 caracteres se trompe sans que rien ne le dise ;
  la comparaison apres relecture, elle, le dit a la ligne pres.
  **Et l instant du releve est celui ou la SOURCE a ete lue**, pas celui ou le
  fichier est ecrit : c est la premiere date qui dit la fraicheur. Un releve
  plus ancien que la derniere dictee est faux sans le dire.
⑨ CE QUI CLOCHE — **Une tache sans horaire affiche `None` au lieu du repli
  prevu.** La ligne `str(x.get("cron_expression")) or "aucun — declenchement a
  la demande"` calcule d abord `str(None)`, qui vaut la chaine `"None"` — non
  vide, donc vraie. Le repli n est jamais atteint. Un lecteur du releve lit
  `horaire : None` et ne sait pas si la tache n a pas d horaire ou si le champ
  a disparu de la source.
  **Et les trois arguments ne sont pas verifies** : lances sans eux, le
  programme s arrete sur une erreur de langage, sans dire ce qu il attendait.
⑩ EFFET — **ECRIT le fichier `DST` en entier**, ecrasant ce qui s y trouvait.
  Il ne touche a rien d autre : ni le depot, ni les taches, ni la source.
  **Le modifier ne change rien a ce qui tourne** — seule une dictee dans la
  tache elle-meme le fait.
⑪ TERMINAISON — **NE REND JAMAIS LA MAIN : le programme se termine toujours par
  `sys.exit`.** 0 = tous les textes relus sont identiques · 1 = au moins un
  ecart. Aucun de ses appels ne se termine.
⑫ DEFINITIONS
  la mesure de perimetre : le programme qui range chaque fichier du depot en
    vivant, presume ou dormant
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
  la fiche : la ligne d'une stratégie au registre des stratégies `donnees/cac40_strategies.csv`, avec son objectif de gain, sa perte acceptée, son horizon et son univers
  le depot : le depot GitHub ou vivent les fichiers du systeme, le projet n'en etant qu'une copie de lecture
"""
import json, sys, hashlib
from datetime import datetime
from zoneinfo import ZoneInfo

SRC, DST = sys.argv[1], sys.argv[2]
PARIS = ZoneInfo("Europe/Paris")
# L INSTANT DU RELEVE EST CELUI OU LA SOURCE A ETE LUE, jamais celui ou le fichier
# est ecrit : c est la premiere date qui dit la fraicheur. Passe en 3e argument
# (horodatage unix en secondes) ; a defaut, l instant d ecriture, et on le dit.
maintenant = (datetime.fromtimestamp(float(sys.argv[3]), PARIS)
              if len(sys.argv) > 3 else datetime.now(PARIS))
JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]


def en_francais(d):
    """Rend une date en francais, jour de la semaine compris.

    ① ROLE — **Donner au releve une date qui ne change pas de langue selon la
      machine.** Un fichier de gouvernance lu par Jean-Luc doit dire « Samedi »,
      pas « Saturday ».
    ② CONTEXTE D APPEL — Une seule fois, a la composition de l en-tete du
      releve, sur l instant de lecture de la source.
    ③ ENTREE — `d` : un objet date-heure. **Un seul appelant, et il passe
      l instant du releve, deja place dans le fuseau Europe/Paris.**
    ④ CONDITIONS D ENTREE — `d` doit repondre a `weekday()` et `strftime()`.
    ⑤ SORTIE — **UNE valeur : du texte**, de la forme `Samedi 19-09-2026`.
      [rend: 1]
    ⑥ TRAITEMENT — ① lire le rang du jour dans la semaine · ② le remplacer par
      son nom francais pris dans la table · ③ y coller la date chiffree.
    ⑦ UNITE — —
    ⑧ POURQUOI — **Le format `%A` du langage suit la langue du systeme, qui est
      l anglais dans le conteneur qui execute ce programme.** Une table francaise
      ecrite dans le code donne le meme resultat sur toutes les machines.
    ⑨ CE QUI CLOCHE — Rien vu.
    ⑩ EFFET — Aucun : elle ne modifie rien.
    ⑪ TERMINAISON — Rend toujours la main. Aucun de ses appels ne se termine.
      [sort: non]
    """
    return JOURS[d.weekday()] + d.strftime(" %d-%m-%Y")

taches = sorted(json.load(open(SRC, encoding="utf-8"))["data"], key=lambda z: z["name"])
BARRE = "=" * 78
SEP = "-" * 78


def emp(txt):
    """Rend l empreinte sha256 d un texte.

    ① ROLE — **Donner a chaque texte de tache une signature courte qui change
      des qu un seul caractere change.** C est elle qui permet de dire, d un
      releve a l autre, si un prompt a ete redicte.
    ② CONTEXTE D APPEL — Deux fois par tache : une fois au sommaire, tronquee a
      16 caracteres, une fois dans la fiche de la tache, en entier.
    ③ ENTREE — `txt` : le texte du prompt d une tache. **Deux appelants, et tous
      deux passent la meme valeur — le prompt, ou une chaine vide s il manque.**
    ④ CONDITIONS D ENTREE — `txt` doit etre du texte, jamais `None` : l appelant
      remplace l absence par une chaine vide avant d appeler.
    ⑤ SORTIE — **UNE valeur : du texte**, 64 caracteres hexadecimaux.
      [rend: 1]
    ⑥ TRAITEMENT — ① encoder le texte en octets UTF-8 · ② en calculer le sha256 ·
      ③ le rendre en hexadecimal.
    ⑦ UNITE — —
    ⑧ POURQUOI — **L empreinte est calculee sur la SOURCE, avant ecriture, et
      reverifiee apres relecture du fichier.** C est ce qui rend la comparaison
      possible : deux textes de meme taille peuvent differer, deux empreintes
      egales ne le peuvent pas.
    ⑨ CE QUI CLOCHE — Rien vu.
    ⑩ EFFET — Aucun.
    ⑪ TERMINAISON — Rend toujours la main. Aucun de ses appels ne se termine.
      [sort: non]
    """
    return hashlib.sha256(txt.encode("utf-8")).hexdigest()


L = []
L.append("DECIDE · Role : porter le texte exact des taches planifiees, seule source")
L.append("de verite hors du depot. Racine du socle avec le workflow.")
L.append("Quand l appeler : apres toute dictee de prompt, et avant toute mesure de perimetre.")
L.append("")
L.append(BARRE)
L.append("RELEVE DES PROMPTS DES TACHES PLANIFIEES")
L.append("Releve le " + en_francais(maintenant) + maintenant.strftime(" a %Hh%M") + " (Europe/Paris)")
L.append(BARRE)
L.append("")
L.append("CE QUE CE FICHIER EST : le texte integral des taches planifiees, releve par")
L.append("outil dans la liste des taches, jamais recopie a la main ni repris du Drive.")
L.append("Chaque texte est suivi de sa taille en octets et de son empreinte sha256,")
L.append("relevees sur la source AVANT ecriture et verifiees APRES relecture du fichier.")
L.append("")
L.append("POURQUOI IL VIT AU DEPOT : les taches planifiees lancent des programmes que")
L.append("le workflow ne lance pas. Sans ce fichier, la mesure de perimetre croit que")
L.append("seul GitHub Actions fait tourner le systeme, et range parmi les dormants les")
L.append("programmes qui prouvent que le systeme dit vrai.")
L.append("")
L.append("CE QU IL N EST PAS : il ne remplace pas les taches. Le modifier ici ne change")
L.append("rien a ce qui tourne ; seule une dictee dans la tache elle-meme le fait.")
L.append("")
L.append("FRAICHEUR : ce releve vaut pour l etat du " + maintenant.strftime("%d-%m-%Y a %Hh%M") + ",")
L.append("instant ou la source a ete lue — pas l instant ou ce fichier a ete ecrit.")
L.append("Un releve plus ancien que la derniere dictee est faux sans le dire.")
L.append("")
L.append(BARRE)
L.append("SOMMAIRE — " + str(len(taches)) + " taches, toutes relevees")
L.append(BARRE)
L.append("")
for i, x in enumerate(taches, 1):
    p = (x.get("derived_state") or {}).get("prompt") or ""
    L.append("%2d. %-52s %8d o  %s" % (i, x["name"], len(p.encode("utf-8")), emp(p)[:16]))
L.append("")

for i, x in enumerate(taches, 1):
    p = (x.get("derived_state") or {}).get("prompt") or ""
    b = p.encode("utf-8")
    L.append("")
    L.append(BARRE)
    L.append("TACHE %d · %s" % (i, x["name"]))
    L.append(BARRE)
    L.append("identifiant   : " + str(x["id"]))
    L.append("horaire       : " + (str(x.get("cron_expression")) or "aucun — declenchement a la demande"))
    L.append("active        : " + ("oui" if x.get("enabled") else "non"))
    L.append("modele        : " + str((x.get("derived_state") or {}).get("model")))
    L.append("creee le      : " + str(x.get("created_at")))
    L.append("modifiee le   : " + str(x.get("updated_at")))
    L.append("taille        : %d octets" % len(b))
    L.append("empreinte     : " + emp(p))
    L.append(SEP)
    L.append("DEBUT DU TEXTE DE LA TACHE %d" % i)
    L.append(SEP)
    L.append(p)
    L.append(SEP)
    L.append("FIN DU TEXTE DE LA TACHE %d" % i)
    L.append(SEP)

L.append("")
L.append(BARRE)
L.append("FIN DU RELEVE — " + str(len(taches)) + " taches")
L.append(BARRE)

open(DST, "w", encoding="utf-8").write("\n".join(L) + "\n")

# ── RELECTURE : chaque texte est-il ressorti octet pour octet ?
lu = open(DST, encoding="utf-8").read()
ok = 0
for i, x in enumerate(taches, 1):
    p = (x.get("derived_state") or {}).get("prompt") or ""
    d = "\n".join([SEP, "DEBUT DU TEXTE DE LA TACHE %d" % i, SEP, ""])
    f = "\n".join(["", SEP, "FIN DU TEXTE DE LA TACHE %d" % i])
    a = lu.index(d) + len(d)
    z = lu.index(f, a)
    extrait = lu[a:z]
    identique = extrait == p
    ok += identique
    print("  %2d. %-52s %s" % (i, x["name"][:52], "IDENTIQUE" if identique else ">>> ECART <<<"))
print("\n  %d/%d textes relus identiques" % (ok, len(taches)))
import os
print("  fichier : %s · %d octets · %s" % (DST, os.path.getsize(DST),
      hashlib.sha256(open(DST, 'rb').read()).hexdigest()[:16]))
sys.exit(0 if ok == len(taches) else 1)
