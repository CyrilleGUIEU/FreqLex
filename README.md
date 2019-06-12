# FreqLex
Un outil pour détecter les difficultés lexicales d'un texte

**Installation:**

* **Python 3** doit être installé sur votre ordinateur, si ce n'est pas le cas allez sur www.python.org
* Téléchargez ensuite l'archive **FreqLex.zip**
* Décompressez l'archive dans un dossier

**Utilisation:**

Le logiciel se lance en exécutant le fichier **FreqLex.py** du dossier décompressé précédent. 

Vous êtes ensuite invité.e à accepter la licence et à répondre à un rapide questionnaire si vous le souhaitez.

Pour analyser un texte il suffit de coller un texte dans la zone de texte de gauche et d'appuyer sur la touche **"Entrée"** pour voir les classement des mots à droite de la fenêtre.


**Notes:**
* Ces évaluations sont relatives au **lexique** et ne prennent pas en compte d'autres paramètres très importants comme les structures grammaticales
* La base lexicale est construite sur un corpus de sous-titres de films et de livres ces deux fréquences ont les même poids dans le calcul global de fréquence, ce choix est bien sûr arbitraire et vous pouvez le modifier grâce au curseur central. Par ailleurs le choix même du corpus est lui-même porteur d'un arbitraire culturel.

**Making Of**

Les fichiers mentionnés dans cette section sont dans le dossier "MakingOf". 

Le fichier **Data/freqlex.dat** a été généré par le script **MakeBase.py**. Celui-ci utilise le fichier de données **Scripts/lexique382.txt** qui provient du projet www.lexique.org. Il peut être remplacé par une autre base de lexique fréquentiel au même format. 

Pour construire l'archive il faut lancer **MakeZip.py**.

**En savoir plus**

Un [article](https://www.researchgate.net/publication/333718295_FreqLex_un_outil_pour_evaluer_les_difficultes_lexicales_d%27un_texte "Article sur Research Gate") explique la construction de ce projet.
