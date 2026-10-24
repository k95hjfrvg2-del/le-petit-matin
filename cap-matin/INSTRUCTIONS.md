# Cap Matin — recette de production

Podcast quotidien en français, 7 jours sur 7, pour Nicolas (Londres ; famille et attaches à Paris,
Asnières-sur-Seine et Audierne, dans le Finistère). Durée cible : **6 à 8 minutes** (950 à 1 150 mots
de script ; la voix lit environ 155 mots par minute ; jamais plus de 1 250 mots). Épisode publié dans
le fil Apple Podcasts **avant 6h00, heure de Paris** (5h00 à Londres).

Tout ce qui concerne Cap Matin vit dans le dossier `cap-matin/` de ce dépôt. Ne jamais toucher aux
fichiers de Petit Matin Good Vibes (racine du dépôt).

## 1. Déroulé (toujours dans cet ordre)

**Ouverture** (≈30 mots, dite sur la musique) : « Bonjour, et bienvenue dans Cap Matin. Nous sommes
le <jour> <date>. » + une phrase qui donne envie (deux ou trois thèmes du jour).

**0. Fêtes et anniversaires** (≈20 à 70 mots, toujours présente, juste après l'ouverture). Lire
`anniversaires.json` et comparer avec la date du jour (heure de Paris) :
1. Anniversaires du jour : « Et aujourd'hui, on souhaite un très joyeux anniversaire à Mémé ! »
   (nom indiqué dans `qui`, avec la `note` si elle existe ; les cent ans de Pépé : deux ou trois
   phrases d'émotion). Le 20 juillet, souhaiter directement son anniversaire à l'auditeur.
2. Rappels : la veille de chaque anniversaire (« Petit rappel : demain, c'est l'anniversaire de
   Mémé. ») ; sept jours avant pour `"rappel_long": true` ; trois jours avant pour Annabelle, Arthur,
   la fête des mères et la fête des pères.
3. La fête du jour : le ou les saints du calendrier français (vérifier sur nominis.cef.fr ou un
   calendrier des fêtes). Si un prénom de `prenoms_pour_les_fetes` est fêté, le dire nommément.
4. Jours spéciaux : jours fériés en France et au Royaume-Uni, fêtes des mères et des pères (dates
   différentes en France et au Royaume-Uni), Toussaint, Noël, Pâques, Saint-Valentin, Halloween,
   changement d'heure (la veille et le jour même), grandes fêtes bretonnes (Fest-noz notables,
   Festival de Cornouaille à Quimper en juillet, Saint-Yves le 19 mai).
Ne jamais dire d'âge ni d'année de naissance, sauf une `note` qui le prévoit.

**1. L'actualité française** (2 ou 3 infos, ≈55 mots chacune) : les sujets les plus importants des
dernières 24 heures. Factuel, neutre, sans opinion ; quoi, qui, pourquoi ça compte.

**2. Le monde** (1 info, ≈60 mots) : le sujet international du jour.

**3. Deux bonnes nouvelles** (≈60 mots chacune) : science, santé, environnement, solidarité, une
réussite française… récentes (moins d'une semaine), vérifiées et datées. Jamais de publicité.

**4. Paris** (≈55 mots) : une nouvelle de Paris ou d'Île-de-France (de préférence Asnières ou les
Hauts-de-Seine quand il y a quelque chose) : ville, transports, expositions, vie de quartier.

**5. Audierne et le Finistère** (≈60 mots) : une nouvelle d'Audierne, du Cap Sizun ou, à défaut, du
Finistère : port et pêche, mer, patrimoine, événements, vie locale. Sources : audierne.bzh,
Ouest-France, Le Télégramme, France 3 Bretagne, ICI Breizh Izel, meteo.bzh.

**6. Le fait culturel** (≈90 mots) : un fait de culture (art, littérature, musique, cinéma,
gastronomie, langue, Bretagne), avec un détail vivant.

**Le mercredi seulement : les sorties cinéma** (≈110 mots, entre le fait culturel et l'histoire) :
deux ou trois films qui sortent ce mercredi en France, en privilégiant le cinéma français, européen,
d'auteur ou asiatique ; **jamais de blockbusters américains** (super-héros, Marvel, DC, grandes
franchises). Une phrase par film : de quoi il parle et pourquoi il donne envie.

**7. Le fait historique** (≈100 mots) : de préférence un événement survenu à la même date
(« ce jour-là, en… »), faits, chiffres, une anecdote ; si possible un lien avec la France, la mer,
la finance ou aujourd'hui.

**8. La minute de philosophie** (≈140 mots, une minute) : une idée d'un philosophe (antique,
classique ou moderne), expliquée simplement, avec une citation authentique et vérifiée (éviter les
citations apocryphes) et une application concrète pour la journée. Varier les auteurs.

**9. La météo, la mer et les marées (toujours à la fin)** (≈120 mots) :
- Audierne : temps de la journée, températures, vent (direction, force, rafales), pluie ;
  température de la mer ; heures de pleine mer et de basse mer du jour, avec le coefficient.
- Asnières-sur-Seine : temps de la journée, températures, pluie, vent si notable.
- Les jours suivants seulement s'il y a un vrai changement (tempête, vigilance Météo-France,
  coup de froid ou de chaud, fin de la pluie…).
- Toujours dire les heures en heure française.

**Clôture** : « C'était Cap Matin. Belle journée, et à demain. » (on peut varier légèrement).

## 2. Ton

Chaleureux, vif, élégant, une pointe d'humour, jamais niais. Vouvoiement. Phrases courtes.
**Transitions naturelles, jamais d'annonce de rubrique** : ne pas dire « rubrique suivante », ne pas
numéroter ; enchaîner par le sujet (« À Paris, … », « Cap à l'ouest : à Audierne… », « Et ce
jour-là, en mille neuf cent vingt-neuf… »). L'animatrice ne se donne pas de nom. Ne jamais citer le
prénom de l'auditeur ni de détails personnels, sauf dans la rubrique 0.

## 3. Recherche (≈15 minutes)

Le terminal n'a pas accès aux sites web : utiliser **WebSearch** puis **WebFetch** sur un lien
trouvé par la recherche (WebFetch refuse les adresses qui ne viennent pas d'une recherche).
- Marées : chercher « horaires marée Audierne » ; le site surf-report.com
  (`horaires-marees/audierne.html`) donne heures et coefficients ; à défaut marine.meteoconsult.fr.
- Météo Audierne : chercher « météo Audierne » ; meteociel.fr (`previsions/9464/audierne.htm`)
  ou meteo-marine. Vigilances : audierne.bzh, meteofrance.
- Température de la mer : chercher « audierne sea temperature » ; seatemperature.net
  (`current/france/audierne-brittany-france-sea-temperature`) ; vérifier que la date est celle du jour.
- Météo Asnières : chercher « météo Asnières-sur-Seine » ; tameteo.com ou meteo.franceinfo.fr.
- Actualité : mode « extended » ; sources fiables et datées (AFP, Reuters, Le Monde, franceinfo,
  France 24, BBC, Ouest-France, Le Télégramme, Le Parisien, sortiraparis.com pour Paris) ; vérifier
  la date sur la page. Certains sites refusent la lecture : passer à une autre source.
- Ne rien inventer. Paraphraser ; pas de longues citations d'articles.
- **Anti-répétition** : lire `history.json` avant de choisir. Ne pas répéter dans les 30 derniers
  jours un fait culturel, un événement historique, un philosophe ou une citation. Ajouter l'épisode
  du jour en tête de `history.json` (même format).

## 4. Écrire pour l'oreille

- Nombres, dates et heures en toutes lettres : « seize heures quinze », « coefficient
  quatre-vingt-quatre », « mille neuf cent vingt-neuf », « quarante-quatre pour cent ».
- Sigles développés ou épelés.
- Chaque mot étranger se prononce comme dans sa langue d'origine, jamais « à la française ».
- Noms propres : garder l'orthographe correcte dans le script et ajouter dans `prononciation.txt`
  (une ligne `Orthographe => graphie phonétique française`) chaque nom étranger, breton ou difficile
  qui n'y est pas encore. Le rendu applique ces remplacements automatiquement.
- Paragraphes de moins de 90 mots, séparés par une ligne vide (chacun est lu séparément, avec une
  courte pause).
- Enregistrer le script : `cap-matin/scripts/cap_matin_YYYY-MM-DD.txt`.

## 5. Audio (S = dossier de travail temporaire, R = racine du dépôt cloné)

Voix choisie par l'auditeur : **Piper, fr_FR-upmc-medium, voix féminine « jessica »**. Ne pas la
changer sans son accord. Musique : générique original d'inspiration bretonne, acoustique (harpe
celtique, bombarde, violon, flûte, guitare), pas d'électronique.

Installation (≈1 minute, à lancer en arrière-plan dès le début) :

```bash
pip install --break-system-packages -q piper-tts tinysoundfont
mkdir -p $S/voice $S/sf
curl -sS -L -o $S/voice/upmc.onnx "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/upmc/medium/fr_FR-upmc-medium.onnx"
curl -sS -L -o $S/voice/upmc.onnx.json "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/upmc/medium/fr_FR-upmc-medium.onnx.json"
curl -sS -L -o $S/sf/GeneralUser-GS.sf2 "https://huggingface.co/datasets/jbilcke/soundfonts/resolve/main/GeneralUser-GS.sf2"
```

Rendu de la voix (≈1 à 2 minutes), musique, assemblage :

```bash
python3 R/cap-matin/tools/piper_paras.py R/cap-matin/scripts/cap_matin_YYYY-MM-DD.txt $S/paras $S/voice/upmc.onnx
python3 R/cap-matin/tools/bed_breton.py $S/sf/GeneralUser-GS.sf2 $S/bed.wav 34
bash R/cap-matin/tools/assemble.sh $S/paras $S/bed.wav $S/Cap_Matin_YYYY-MM-DD.mp3
```

Vérifier la durée affichée (6 à 8 minutes, fin non coupée). Si un nom est mal lu, corriger
`prononciation.txt` et relancer le rendu (c'est rapide).

## 6. Publication

```bash
cd R && python3 cap-matin/publish_episode.py cap-matin https://k95hjfrvg2-del.github.io/le-petit-matin/cap-matin $S/Cap_Matin_YYYY-MM-DD.mp3 "<Jour JJ mois> : <titre de 3 à 6 mots>" "<une phrase résumant l'épisode>" YYYY-MM-DD
```

Puis `git pull --rebase origin main` (l'autre podcast publie dans le même dépôt), commit (auteur
Claude <noreply@anthropic.com>, message « Cap Matin YYYY-MM-DD ») incluant tout le dossier
`cap-matin/` ; push sur main si autorisé, sinon sur une branche `claude/cap-matin-YYYY-MM-DD` (le
workflow du dépôt la fusionne dans main). Jamais de force-push ni de réécriture d'historique.
