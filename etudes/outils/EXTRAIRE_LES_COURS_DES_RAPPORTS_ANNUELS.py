"""EXTRAIRE_LES_COURS_DES_RAPPORTS_ANNUELS.py — Mer 07-10-2026 (Paris) — OUTIL D'ÉTUDE, hors du circuit.

À quoi il sert : recopier SANS MAIN les tableaux « cours extrêmes mensuels » des rapports annuels des
sociétés (documents de référence), pour recouper l'historique long par une source officielle (méthode A
du chapitre « Comment l'historique long a été construit » de donnees/LISEZ_MOI_LES_COURS.md).

Comment s'en servir :
1. Télécharger les PDF dont l'adresse est dans SOURCES ci-dessous (un en-tête de navigateur suffit).
2. Les convertir en texte : pdftotext -layout <fichier>.pdf <fichier>.txt (même nom, dans un même dossier).
3. Lancer : python3 -I etudes/outils/EXTRAIRE_LES_COURS_DES_RAPPORTS_ANNUELS.py <dossier des PDF> <CSV de sortie>
   La sortie du 07-10-2026 est donnees/sources_rapports_annuels/COURS_MENSUELS_DES_RAPPORTS_ANNUELS.csv
   (44 lignes) ; chaque ligne porte l'adresse et l'empreinte SHA-256 du PDF lu.

Pour ajouter une société : une ligne de plus dans SOURCES — valeur, nom du fichier, adresse, un texte qui
précède le tableau (« ancre »), l'année du premier mois, le nombre de lignes à lire, les mois à garder,
la convention du tableau (bruts, ou ajustés de quoi).

Ce qui cloche : la lecture repose sur la mise en page du texte (un mois par ligne, plus haut puis plus
bas en fin de ligne) ; un tableau mis en page autrement ne donne rien, ou donne moins de mois — compter
les lignes écrites. Les chiffres du 07-10-2026 ont été confrontés à la lecture humaine du texte : 44 sur 44.
Simulation uniquement.
"""
import csv, hashlib, re, sys
MOIS = {m: i + 1 for i, m in enumerate("Janvier Février Mars Avril Mai Juin Juillet Août Septembre Octobre Novembre Décembre".split())}
def tableau(texte, ancre, an_initial, nb_lignes):
    lignes = texte.split("\n"); i = next(k for k, l in enumerate(lignes) if ancre in l)
    an, out = an_initial, {}
    for l in lignes[i:i + nb_lignes]:
        s = l.strip()
        if re.fullmatch(r"(19|20)\d\d", s):
            an = s; continue
        m = re.match(r"(\S+)\s.*?(\d+,\d\d)\s+(\d+,\d\d)\s*\*?\s*$", s)
        if m and m.group(1) in MOIS:
            out[f"{an}-{MOIS[m.group(1)]:02d}"] = (m.group(2).replace(",", "."), m.group(3).replace(",", "."))
    return out
dossier, sortie = sys.argv[1], sys.argv[2]
SOURCES = [
 ("AXA", "axa_ddr2006", "https://www-axa-com.cdn.axa-contento-118412.eu/www-axa-com/b4f171ab-6f95-46fa-b865-6dfdafb56ab5_axa_document_reference_2006d.pdf",
  "Transactions de l’action AXA et de l’ADS AXA sur 20 mois à Paris et New York", "2005", 30, lambda k: True,
  "cours en séance ; avant le détachement de juin 2006, ajustés de la valeur théorique du droit"),
 ("ESSILORLUXOTTICA", "20010412_Document_de_reference_2000_Essilor", "https://www.bnains.org/archives/communiques/Essilor/20010412_Document_de_reference_2000_Essilor.pdf",
  "Cours extrêmes", "1999", 30, lambda k: k.startswith("2000"),
  "action ordinaire, cours d'avant la division par dix de 2001"),
 ("ESSILORLUXOTTICA", "20020412_Document_de_reference_2001_Essilor", "https://www.bnains.org/archives/communiques/Essilor/20020412_Document_de_reference_2001_Essilor.pdf",
  "Cours extrêmes (ajustés)", "2001", 20, lambda k: k.startswith("2001"),
  "cours ajustés de la division par dix de 2001, source Euronext"),
]
lignes = [["valeur", "mois", "plus_haut", "plus_bas", "convention", "source", "empreinte_sha256_du_pdf"]]
for valeur, nom, url, ancre, an, n, garde, convention in SOURCES:
    texte = open(f"{dossier}/{nom}.txt", encoding="utf-8", errors="replace").read()
    empreinte = hashlib.sha256(open(f"{dossier}/{nom}.pdf", "rb").read()).hexdigest()
    for mois, (h, b) in sorted(tableau(texte, ancre, an, n).items()):
        if garde(mois):
            lignes.append([valeur, mois, h, b, convention, url, empreinte])
with open(sortie, "w", encoding="utf-8", newline="") as f:
    csv.writer(f, lineterminator="\n").writerows(lignes)
print(len(lignes) - 1, "lignes écrites")
