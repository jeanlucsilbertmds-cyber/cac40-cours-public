#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chiffre une page web pour qu elle ne s ouvre qu avec une phrase secrete.

① ROLE — **Rendre le cockpit illisible pour qui passe par hasard sur son
  adresse.** Le cockpit est publie sur un depot public : quiconque connait
  l adresse voit les positions, le journal des trades et les mesures. Ce
  programme remplace la page par une page autonome qui ne contient QUE du texte
  chiffre et une case ou taper la phrase.
② CONTEXTE D APPEL — Le pas n°9 du circuit du soir, « Fabriquer et publier le
  cockpit en page web », juste avant la publication. Jamais a la main, sauf
  pour eprouver.
③ ENTREE — La ligne de commande, deux arguments : le chemin de la page en clair,
  et le chemin de la page protegee a ecrire. **Et une variable d environnement
  `PHRASE`**, qui porte la phrase secrete. **Un seul appelant, le circuit du
  soir, et il la prend dans les secrets de l hebergeur.**
④ CONDITIONS D ENTREE — La page en clair doit exister. `PHRASE` doit etre non
  vide. **Le module de chiffrement `cryptography` doit etre installe.**
⑤ SORTIE — **Un code de sortie, et rien d autre.** La page protegee est ecrite
  dans le fichier demande.
⑥ TRAITEMENT — ① lire la page en clair · ② tirer au sort un sel et un nonce ·
  ③ deriver une cle de la phrase · ④ chiffrer la page · ⑤ coller le coffre dans
  le gabarit de la page-porte · ⑥ ecrire le resultat.
⑦ UNITE — Les iterations sont un NOMBRE DE PASSAGES de la fonction de derivation
  — 310 000, recommandation publique de 2023 pour cette fonction. Les tailles
  affichees sont en caracteres pour la page en clair, en octets pour la sortie.
⑧ POURQUOI — Rendre le depot prive couterait un abonnement payant pour garder la
  publication en page web. **Le chiffrement resout le meme probleme sans rien
  payer : la page publiee ne contient rien de lisible.** Le dechiffrement se
  fait dans le navigateur, par une fonction native depuis 2017 — aucune
  dependance reseau, aucune bibliotheque a charger.
  **LA PHRASE N EST NI ENREGISTREE NI ENVOYEE** : elle ne sert qu a deriver la
  cle, dans le navigateur du lecteur.
⑨ CE QUI CLOCHE — **Le code de sortie 2 porte TROIS causes differentes** :
  arguments manquants, page introuvable, et module de chiffrement absent. La
  ligne d usage en pied de ce texte n en annonce qu une, « page absente ». Un
  circuit qui rougit sur un code 2 ne sait pas laquelle des trois s est
  produite, et les trois se reparent autrement.
  **Et ce que ce programme ne protege pas doit se lire ici** : les fichiers de
  donnees publies a cote — cours, historique — restent en clair au depot
  public. Ce sont des cours de bourse, publics par nature. Une phrase faible,
  elle, se devine hors ligne par essais repetes : quatre mots ou plus.
⑩ EFFET — **ECRIT la page protegee**, ecrasant ce qui se trouvait a ce chemin.
  Il ne touche pas a la page en clair.
⑪ TERMINAISON — **NE REND JAMAIS LA MAIN : tous les chemins se terminent.**
  0 = page protegee · 1 = phrase absente · 2 = arguments manquants, page
  introuvable, ou module de chiffrement absent. **Et un de ses appels peut ne
  pas revenir : `chiffrer` se termine elle-meme en code 2.**
⑫ DEFINITIONS
  le cockpit : la page web que ce programme fabrique et que Jean-Luc ouvre pour voir l etat du systeme.
  le circuit du soir : la suite de programmes lancés chaque soir à 20 h par GitHub Actions — collecte, versement, signaux, positions, mesure, surveillance.
  le coffre : le sel, le nonce et les donnees chiffrees, colles dans la page
  le depot : le depot GitHub ou vivent les fichiers du systeme, le projet n'en etant qu'une copie de lecture
"""
import base64, hashlib, json, os, secrets, sys

ITERATIONS = 310000


def chiffrer(texte: str, phrase: str) -> dict:
    """Chiffre un texte avec une phrase, ou arrete le programme.

    ① ROLE — **Transformer la page en clair en un coffre que seule la phrase
      ouvre.** C est le seul endroit du systeme ou un chiffrement est fait.
    ② CONTEXTE D APPEL — `main`, une seule fois, apres avoir lu la page en clair
      et verifie que la phrase est presente.
    ③ ENTREE — `texte` : la page web en clair · `phrase` : la phrase secrete.
      **Un seul appelant, et il passe le contenu du fichier source et la
      variable d environnement `PHRASE`.**
    ④ CONDITIONS D ENTREE — Les deux doivent etre du texte non vide — `main` le
      verifie pour la phrase avant d appeler. **Le module de chiffrement doit
      etre installe : c est verifie ICI, pas avant.**
    ⑤ SORTIE — **UNE valeur : un dictionnaire de QUATRE cles** — `sel`,
      `nonce`, `donnees` et `iterations`. Les trois premieres sont en base64,
      la quatrieme est un nombre.
      [rend: 1]
    ⑥ TRAITEMENT — ① tirer au sort un sel de 16 octets et un nonce de 12 ·
      ② deriver une cle de 32 octets a partir de la phrase et du sel ·
      ③ charger le module de chiffrement, et s arreter s il manque ·
      ④ sceller le texte · ⑤ rendre le coffre.
    ⑦ UNITE — Le sel et le nonce sont des NOMBRES D OCTETS tires au hasard ;
      la cle fait 32 octets, soit 256 bits. Les iterations sont un nombre de
      passages, pas une duree.
    ⑧ POURQUOI — **Le sel et le nonce sont tires au sort a chaque appel.** Deux
      pages chiffrees avec la meme phrase ne se ressemblent donc pas, et
      comparer deux publications n apprend rien sur la phrase.
      **Le module est charge ICI et non en tete de fichier** : le programme peut
      ainsi afficher son mode d emploi meme sur une machine ou il manque.
    ⑨ CE QUI CLOCHE — **Son nom dit qu elle chiffre, et elle peut arreter tout
      le programme.** Un lecteur qui l appelle depuis un autre programme
      s attend a recevoir une valeur ou une erreur rattrapable ; il obtient une
      fin de processus en code 2. Le ⑪ le dit, le nom ne le dit pas.
    ⑩ EFFET — **Consomme du hasard du systeme** pour le sel et le nonce. N ecrit
      aucun fichier, ne modifie rien.
    ⑪ TERMINAISON — **PEUT NE PAS RENDRE LA MAIN : code 2 si le module de
      chiffrement est absent.** Sinon elle rend le coffre. Aucun de ses appels
      ne se termine.
      [sort: oui]
    """
    sel = secrets.token_bytes(16)
    nonce = secrets.token_bytes(12)
    cle = hashlib.pbkdf2_hmac("sha256", phrase.encode(), sel, ITERATIONS, 32)
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError:
        print("CODE 2 — le module cryptography est requis (pip install cryptography)")
        sys.exit(2)
    scelle = AESGCM(cle).encrypt(nonce, texte.encode("utf-8"), None)
    return {"sel": base64.b64encode(sel).decode(),
            "nonce": base64.b64encode(nonce).decode(),
            "donnees": base64.b64encode(scelle).decode(),
            "iterations": ITERATIONS}


GABARIT = """<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cockpit CAC 40</title>
<style>
 body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
      background:#0f1115;color:#e8eaed;display:flex;align-items:center;
      justify-content:center;min-height:100vh}
 #porte{text-align:center;padding:2rem;max-width:22rem}
 h1{font-size:1.1rem;font-weight:600;letter-spacing:.02em;margin:0 0 1.5rem;color:#9aa0a6}
 input{width:100%;padding:.9rem 1rem;font-size:1rem;border:1px solid #2d3139;
       border-radius:.6rem;background:#1a1d23;color:#e8eaed;box-sizing:border-box}
 input:focus{outline:none;border-color:#5b8def}
 button{width:100%;margin-top:.8rem;padding:.9rem;font-size:1rem;font-weight:600;
        border:0;border-radius:.6rem;background:#5b8def;color:#fff;cursor:pointer}
 #err{margin-top:1rem;color:#f28b82;font-size:.9rem;min-height:1.2rem}
 #contenu{display:none;width:100%}
</style></head><body>
<div id="porte">
  <h1>COCKPIT CAC 40</h1>
  <input type="password" id="phrase" placeholder="phrase secrete" autocomplete="current-password">
  <button id="ouvrir">Ouvrir</button>
  <div id="err"></div>
</div>
<div id="contenu"></div>
<script>
const COFFRE = __COFFRE__;
const b64 = s => Uint8Array.from(atob(s), c => c.charCodeAt(0));
async function ouvrir(){
  const err = document.getElementById('err');
  const phrase = document.getElementById('phrase').value;
  if(!phrase){ err.textContent = 'phrase vide'; return; }
  err.textContent = 'dechiffrement...';
  try{
    const base = await crypto.subtle.importKey('raw', new TextEncoder().encode(phrase),
                        'PBKDF2', false, ['deriveKey']);
    const cle = await crypto.subtle.deriveKey(
      {name:'PBKDF2', salt:b64(COFFRE.sel), iterations:COFFRE.iterations, hash:'SHA-256'},
      base, {name:'AES-GCM', length:256}, false, ['decrypt']);
    const clair = await crypto.subtle.decrypt({name:'AES-GCM', iv:b64(COFFRE.nonce)},
                        cle, b64(COFFRE.donnees));
    document.getElementById('porte').remove();
    const c = document.getElementById('contenu');
    c.style.display = 'block';
    document.body.style.display = 'block';
    c.innerHTML = new TextDecoder().decode(clair);
    c.querySelectorAll('script').forEach(v => {
      const n = document.createElement('script');
      n.textContent = v.textContent; v.replaceWith(n);
    });
  }catch(e){ err.textContent = 'phrase incorrecte'; }
}
document.getElementById('ouvrir').onclick = ouvrir;
document.getElementById('phrase').addEventListener('keydown', e => { if(e.key==='Enter') ouvrir(); });
document.getElementById('phrase').focus();
</script></body></html>"""


def main():
    """Lit les arguments, chiffre la page, ecrit le resultat.

    ① ROLE — **Enchainer les quatre gestes du programme** : verifier ce qui est
      donne, lire, chiffrer, ecrire.
    ② CONTEXTE D APPEL — Le lancement du programme, et lui seul.
    ③ ENTREE — Aucun parametre. Elle lit la ligne de commande — deux chemins —
      et la variable d environnement `PHRASE`.
    ④ CONDITIONS D ENTREE — Deux arguments au moins. La page source doit
      exister. `PHRASE` doit etre non vide.
    ⑤ SORTIE — **Ne rend rien : elle se termine toujours par un code de
      sortie.**
      [rend: rien]
    ⑥ TRAITEMENT — ① si moins de deux arguments, afficher le mode d emploi et
      s arreter · ② s arreter si la phrase manque · ③ s arreter si la page
      manque · ④ lire la page · ⑤ la chiffrer · ⑥ coller le coffre dans le
      gabarit · ⑦ ecrire la page protegee · ⑧ afficher la taille et les
      reglages de chiffrement.
    ⑦ UNITE — La page en clair est comptee en CARACTERES, la page protegee en
      OCTETS. Les deux ne se comparent pas : le chiffrement et l encodage en
      base64 font grossir le resultat d environ un tiers.
    ⑧ POURQUOI — **Le mode d emploi complet est affiche quand les arguments
      manquent** : le programme est lance a la main pour eprouver, et un message
      d une ligne obligerait a ouvrir le fichier.
    ⑨ CE QUI CLOCHE — **Le dossier de destination n est pas verifie.** Si le
      chemin de sortie designe un dossier qui n existe pas, l ecriture echoue
      sur une erreur de langage, apres que le chiffrement a ete fait — donc
      apres 310 000 iterations de calcul perdues.
    ⑩ EFFET — **ECRIT la page protegee** et affiche deux lignes de bilan.
    ⑪ TERMINAISON — **NE REND JAMAIS LA MAIN : tous les chemins se terminent.**
      0 = page protegee · 1 = phrase absente · 2 = arguments manquants ou page
      introuvable. **Et un de ses appels peut ne pas revenir : `chiffrer` se
      termine en code 2 si le module de chiffrement manque.**
      [sort: oui]
    """
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    src, dst = sys.argv[1], sys.argv[2]
    phrase = os.environ.get("PHRASE", "")
    if not phrase:
        print("CODE 1 — PHRASE absente"); sys.exit(1)
    if not os.path.isfile(src):
        print(f"CODE 2 — {src} absent"); sys.exit(2)
    clair = open(src, encoding="utf-8").read()
    coffre = chiffrer(clair, phrase)
    page = GABARIT.replace("__COFFRE__", json.dumps(coffre))
    open(dst, "w", encoding="utf-8").write(page)
    print(f"  page protegee : {len(clair)} caracteres chiffres -> {len(page)} octets")
    print(f"  AES-256-GCM · PBKDF2-SHA256 · {ITERATIONS} iterations")
    sys.exit(0)


if __name__ == "__main__":
    main()
