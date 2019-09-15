# -*- coding: cp1252 -*-
import sqlite3



class bddl:
    def __init__(self,nom_fichier="",max_iter=300000):
        self.encoding='utf8'
        self.dossier_sqlite="Data/"
        self.nom_fichier=nom_fichier
        self.description=""
        self.nom=nom_fichier
        self.nom_colonne_freq=""
        self.nom_colonne_forme="ortho"
        self.split_symbol="\t"
        self.max_iter=max_iter
        self.url=""
    def erreur_format(self,terme,liste):
        print("Erreur de format:")
        print("Le terme ",terme," n'est pas dans la liste ci-dessous:")
        print(str(liste))
    def affiche(self):
        k=0
        for x in self.forme:
            print(x,self.freq_forme[k])
            k=k+1

    def lire_fichier_sqlite(self):
        """Lecture du fichier sqlite3 -> self.sql"""
        chemin=self.dossier_sqlite+self.nom+".sqlite3"
        #print("Lecture du fichier "+chemin)
        conn = sqlite3.connect(chemin)
        self.sql = conn.cursor()
        

    def sonde_base_sql(self,nombre_tests):
        from random import choice
        k=0
        #Accès à la table
        self.lire_fichier_sqlite()
        test=self.sql.execute('SELECT * FROM lexique')
        test=list(test)
        print("{} entrées au hasard de la base {}:".format(nombre_tests,self.nom))
        while k<nombre_tests:
            k=k+1
            print(choice(test))
        self.sql.close()
        self.sql=""

    def requete_sql(self,r):
        #Accès à la table
        self.lire_fichier_sqlite()
        r=self.sql.execute(r)
        l=list(r)
        self.sql.close()
        self.sql=""
        rep=[]
        for x in l:
            rep.append(x[0])
        return rep
        


            
    def creer_fichier_sqlite(self):
        """Extrait les données de la base"""
        #Ouverture du fichier au format utf8 et chargement des entrées -> lecture
        fichier_data=open(self.nom_fichier,encoding=self.encoding)
        lignes=fichier_data.readlines()
        fichier_data.close()
        #Verification du format
        titres=lignes[0].split(self.split_symbol)
        if titres.count(self.nom_colonne_forme)>0:
            indice_forme=titres.index(self.nom_colonne_forme)
        else:
            self.erreur_format(self.nom_colonne_forme,titres)
        if titres.count(self.nom_colonne_freq)>0:
            indice_freq=titres.index(self.nom_colonne_freq)
        else:
            self.erreur_format(self.nom_colonne_freq,titres)
        #Sélection des entrées pertinentes -> entrees
        entrees=[]
        
        for ligne in lignes[1:]:
            ligne=ligne.split(self.split_symbol)
            entrees.append([ligne[indice_forme],ligne[indice_freq]])
           

        #test
        #print(entrees[12])

        print("Traitement des données de la base {}.".format(self.nom))


        #Création d'un fichier de base de données SQLITE3
        conn = sqlite3.connect(self.dossier_sqlite+self.nom+".sqlite3")
        cursor = conn.cursor()
        #Création de la table
        cursor.execute("""DROP TABLE IF EXISTS lexique""")
        cursor.execute("""
        CREATE TABLE lexique(
             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
             ortho TEXT,
             freq REAL
        )
        """)
        #La table est remplie avec les "entrees"
        cursor.executemany("""
        INSERT INTO lexique(ortho,freq) VALUES(?, ?)""", entrees)
        conn.commit()
        #Fermeture de la base
        conn.close()
        

      
            
    def freq2forme(self,forme):
        if self.forme.count(forme)==0:
            return -1
        else:
            return self.freq_forme[self.forme.index(forme)]
    def extraire_listes(self):
        self.forme=self.requete_sql("select ortho from lexique")
        self.freq_forme=self.requete_sql("select freq from lexique")
     

            
            
            

if __name__=="__main__":
    from time import time
    n_test=800000
    t0=time()
    print("Test1: fréquences des formes ortho correctes dans les livres")
    print("*"*30)
    b=bddl("bases_brutes/Lexique383.tsv",max_iter=n_test)
    b.nom=("L383-livre-formeOrtho-test")
    b.nom_colonne_freq="freqlivres"
    b.url="http://www.lexique.org/databases/Lexique383/Lexique383.zip"
    b.description="""Fréquence par million
d'occurrences de la forme orthographique selon notre corpus de livres. (14,7 millions de mots)."""
    b.creer_fichier_sqlite()
    b.extraire_listes()
    #b.lire_fichier_sqlite()
    b.sonde_base_sql(10)
    


    

