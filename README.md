# FreqLex
Un outil pour évaluer la difficulté lexicale d'un texte

**Installation:**

* **Python 3** doit être installé sur votre ordinateur, si ce n'est pas le cas allez sur www.python.org
* Téléchargez ensuite l'archive **FreqLex.zip**
* Décompressez l'archive dans un dossier

**Utilisation:**

Le logiciel se lance en exécutant le fichier **FreqLex.py** du dossier décompressé précédent. Une fenêtre s'ouvre après quelques secondes de calcul dans une console.

Ensuite il suffit de coller un texte dans la zone de texte de gauche et d'appuyer sur la touche **"Entrée"** pour voir le classement des mots dans la zone de texte de droite.


**Notes:**
* Ces évaluations sont relatives au **lexique** et ne prennent pas en compte d'autres paramètres très importants comme les structures grammaticales
* La base lexicale est construite sur un corpus de sous-titres de films et de livres ces deux fréquences ont les même poids dans le calcul global de fréquence, ce choix est bien sûr arbitraire. Par ailleurs le choix même du corpus est lui-même porteur d'un arbitraire culturel.

**Making Of**

Les fichiers mentionnés dans cette section sont dans le dossier "MakingOf". 

Le fichier **freqlex.dat** a été généré par le script **base_lexique.py**. Celui-ci utilise le fichier de données **lexique381.txt** qui provient du projet www.lexique.org. Il peut être remplacé par une autre base de lexique fréquentiel au même format. 

Pour construire l'archive il faut lancer **MakeZip.py**.
