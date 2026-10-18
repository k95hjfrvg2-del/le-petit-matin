# Petit Matin Good Vibes — recette de production

Podcast quotidien en français, 7 jours sur 7, pour Nicolas (Londres, cadre senior en finance,
marié, un fils d'âge scolaire). Durée cible : **5 à 7 minutes** (950 à 1 100 mots de script : la voix lit environ
175 mots par minute ; jamais plus de 1 200). Épisode publié dans le fil Apple Podcasts **avant 6h00, heure de Londres**.

## 1. Les six rubriques (toujours dans cet ordre)

1. **Le conseil management du jour** (≈150 mots). Un outil concret, applicable aujourd'hui :
   d'où il vient (auteur, entreprise, étude réelle et vérifiée), pourquoi il marche, comment
   le faire en pratique (durée, étapes). Public : manager senior en finance. Pas de banalités
   (« écoutez vos équipes ») ; des méthodes précises (pré-mortem, RACI, désaccord et engagement,
   one-on-one, revue après action, délégation par niveaux, feedback SBI, etc.).
2. **L'idée de voyage** (≈150 mots), surtout en **Asie** (Japon, Corée, Chine, Taïwan, Asie du
   Sud-Est, Inde…) ; environ une fois sur cinq, ailleurs. Toujours **de saison** (feuillages,
   festivals, météo) et datée quand un événement a lieu. Trois étapes concrètes et un conseil
   pratique. Vérifier les dates d'événements sur une source de l'année en cours.
3. **L'Asie qui bouge : mode ou anecdote du Japon, de la Corée ou de la Chine** (≈170 mots).
   Une tendance ou une histoire **récente** (moins de 2 mois, source datée), avec un chiffre ou un
   détail concret. Alterner les pays d'un jour à l'autre (consulter history.json) ; on peut
   ajouter une brève sur un deuxième pays.
4. **La citation française** (≈60 mots). Auteur français ou francophone, citation **authentique
   et vérifiée** (attention aux citations apocryphes, ex. le « bateau » attribué à
   Saint-Exupéry, le « je ne suis pas d'accord » attribué à Voltaire : à éviter). Préférer des
   auteurs tombés dans le domaine public (morts avant 1956). Une phrase courte, puis une ou deux
   phrases de commentaire avec une pointe d'esprit.
5. **Un moment de l'histoire de France** (≈180 mots). De préférence un événement survenu **à la
   même date** (« ce jour-là, en… »), sinon un épisode marquant. Faits, chiffres, un détail
   vivant, et si possible un lien avec Londres, la finance ou aujourd'hui.
6. **Le fait de culture générale** (≈150 mots). Un fait historique important, mondial, de
   préférence à la même date, avec une anecdote mémorable. Conclure par une chute qui relie, si
   possible, à une autre rubrique du jour.

Ouverture (≈30 mots, dite sur la musique) : « Bonjour, et bienvenue dans Petit Matin Good Vibes. Nous
sommes le <jour> <date>. » + une phrase. Clôture : « C’était Petit Matin Good Vibes. Belle journée, et à
demain. » (on peut varier légèrement).

## 2. Ton

Une voix parisienne : vive, complice, élégante, une pointe d'humour, jamais niaise. Vouvoiement.
Phrases courtes. Transitions brèves (« Deuxième rubrique : … »). L'animatrice ne se donne pas de
nom. Ne jamais citer le prénom de l'auditeur ni des détails personnels dans l'épisode.

## 3. Recherche (≈12 minutes, 8 à 15 recherches)

- WebSearch (mode « extended » pour l'actualité) puis WebFetch pour lire la page.
- Rubriques 2 et 3 : sources de l'année en cours, dates vérifiées sur la page.
- Rubriques 5 et 6 : « <jour> <mois> dans l'histoire », Hérodote.net (« <jour>_<mois>_<année> »),
  Wikipédia ; confirmer date et chiffres sur une deuxième source si possible. Quand les
  historiens divergent, donner une fourchette.
- Ne rien inventer. Paraphraser les sources ; pas de longues citations d'articles.
- **Anti-répétition** : lire `history.json` (dans ce dépôt) avant de choisir. Ne jamais répéter
  un conseil, une destination, une citation, un auteur cité dans les 30 derniers jours, ni un
  événement historique. Ajouter l'épisode du jour à `history.json` (voir le format existant).

## 4. Écrire pour l'oreille

- Nombres et dates en toutes lettres : « seize cent quatre-vingt-cinq », « soixante-trois pour
  cent », « sept millions deux cent mille dollars ».
- Sigles épelés ou développés ; mots étrangers écrits comme ils se prononcent si la voix risque
  de les écorcher (tester au besoin).
- Paragraphes de moins de 100 mots, séparés par une ligne vide (chaque paragraphe est lu
  séparément, avec une courte pause).
- Enregistrer le script : `petit_matin_YYYY-MM-DD.txt`.

## 5. Audio (S = dossier de travail temporaire)

Voix : **Kokoro v1.0, voix ff_siwis, vitesse 1.08, langue fr-fr**. Hugging Face et GitHub
releases sont bloqués ; le modèle est fourni dans le paquet npm expo-kokoro.

```bash
mkdir -p $S/kok/expo && cd $S/kok/expo
npm pack expo-kokoro && tar xzf expo-kokoro-*.tgz
pip install --break-system-packages -q kokoro-onnx
python3 - <<EOF
import numpy as np, glob, os
P = "$S/kok/expo/package/build"
d = {os.path.basename(f)[:-4]: np.fromfile(f, dtype=np.float32).reshape(-1, 1, 256) for f in glob.glob(P + "/voices/*.bin")}
np.savez("$S/kok/voices_v1.npz", **d)
EOF
```

Installer pendant la recherche (en arrière-plan) pour gagner du temps.

Rendu de la voix (≈1,3 × temps réel : compter 10 à 15 minutes), en arrière-plan, reprise possible :

```bash
P=$S/kok/expo/package/build
nohup python3 <repo>/tools/tts_paras.py $P/kokoro-quantized.onnx $S/kok/voices_v1.npz petit_matin_YYYY-MM-DD.txt $S/paras ff_siwis 1.08 > $S/tts.log 2>&1 &
```

Musique (originale, style café parisien, 3 s de calcul) puis assemblage :

```bash
python3 <repo>/tools/bed_cafe.py $S/bed.wav 34
bash <repo>/tools/assemble.sh $S/paras $S/bed.wav $S/Le_Petit_Matin_YYYY-MM-DD.mp3
```

Vérifier la durée affichée (5 à 7 minutes, fin non coupée).
Ne jamais utiliser espeak seul, festival ou Piper : voix jugées robotiques.

## 6. Publication

```bash
python3 publish_episode.py . https://k95hjfrvg2-del.github.io/le-petit-matin $S/Le_Petit_Matin_YYYY-MM-DD.mp3 "<Jour JJ mois> : <titre de 3 à 6 mots>" "<une phrase résumant les six rubriques>" YYYY-MM-DD
```

Puis commit (auteur Claude <noreply@anthropic.com>, message « Épisode YYYY-MM-DD ») incluant episodes/, episodes.json, feed.xml, history.json ; push sur main
si autorisé, sinon sur la branche claude/ de la session (le workflow du dépôt la fusionne dans
main). Jamais de force-push ni de réécriture d'historique.
