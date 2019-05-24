# FreqLex
Un outil pour évaluer la difficulté lexicale d'un texte

**Installation:**

Vous devez au préalable installer Python 3 sur www.python.org
Il faut ensuite télécharger les trois fichiers: 
* FreqLex.py
* gestion_texte.py 
* freqlex.dat

Ce dernier fichier a été généré par le script base_lexique.py. Celui-ci utilise le fichier de données lexique381.txt qui provient du projet www.lexique.org. Il peut être remplacé par une autre base de lexique fréquentiel au même format.

**Utilisation:**

Le logiciel se lance en exécutant FreqLex.py
Une fenêtre s'ouvre après quelques secondes de calcul dans une console.
Ensuite il suffit de coller un texte dans la zone de texte de gauche et d'appuyer sur la touche "Entrée" pour voir le classement des mots dans la zone de droite.


**Notes:**
* Ces évaluations sont relatives au **lexique** et ne prennent pas en compte d'autres paramètres très importants comme les structures grammaticales
* La base lexicale est construite sur un corpus de sous-titres de films et de livres ces deux fréquences ont les même poids dans le calcul global de fréquence, ce choix est bien sûr arbitraire 
