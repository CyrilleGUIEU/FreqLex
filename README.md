# FreqLex
Un outil pour détecter les difficultés lexicales d'un texte

Ce dépôt contient les sources du logiciel FreqLex. Les exécutables sont disponibles [ici](https://www.researchgate.net/project/FreqLex).

**Dépendances:**

* **Python 3** 
* **Numpy**



**Principes de fonctionnement**
* **FreqLex.py** permet de lancer le programme
* **FreqLEx_core.py** contient la définition de l'interface graphique
* **gui_freqlex.py** contient les défintions de certains objets de l'interface
* Les autres scripts définissent la structure de données du programme
* Les dossiers **Data** et **bases_sql** contiennent les données lexicales

**Construire les archives**
Pour construire les archives (sous Windows) il faut lancer **make.bat**. Les versions Windows, Linux et MacOS sont alors générées dans le répertoire parent. Seule la version Windows contient un exécutable. Les autres versions doivent être lancée avec un interpréteur Python.


