# -*- coding: cp1252 -*-
import pickle
from classes_bddl import bddl

class base_freqlex:
    def __init__(self):
        self.n_base=0
        self.forme=[]
        self.liste_freq=[]
        self.bddl_brute=[]
        self.extension=".pickle"
        
    def liste_freq2forme(self,forme):
        rep=[]
        #test
        #print(forme,"->")
        for b in self.bddl_brute:
            freq=b.requete_sql('select freq from lexique where ortho="{}"'.format(forme))
            s=0
            for x in freq:
                s=s+x
            rep.append(s)
        #test
        #print(rep)
        return rep

    def ajoute_bddl(self,bddl_source):
        """Ajoute une base de donnée lexicale"""
        bddl_source.extraire_listes()
        self.bddl_brute.append(bddl_source)
        self.n_base=self.n_base+1
        print("Ajout de la base:",bddl_source.nom)
            
                
    def sauvegarde(self,nom):
        """Sauvegarde l'objet bddl"""
        print("*"*30)
        print("Sauvegarde de la base.")
        
        fichier=open(nom+self.extension,"wb")
        pickle.dump(self,fichier)
        fichier.close()
        print("Sauvegarde effectuée dans le fichier",nom+self.extension)
        print("Voici les vingt premières entrées de cette base:")
        for x in self.bddl_brute[0].forme[:19]:
            print(x,self.liste_freq2forme(x))
    def lecture(self,nom):
        """Lecture de l'objet bddl"""
        fichier=open(nom+self.extension,"rb")
        self=pickle.load(fichier)
        fichier.close()
        print("Lecture du fichier",nom+self.extension)
        print("Voici les vingt premières entrées de cette base:")
        for x in self.bddl_brute[0].forme[:19]:
            print(x,self.liste_freq2forme(x))
        
            
            
            

if __name__=="__main__":
    from time import time
    n_test=1000
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
    
    t0=time()
    print("Test2: fréquences des mots dans twitter")
    print("*"*30)
    f=bddl("bases_brutes/Fre.Freq.2.txt",max_iter=n_test)
    f.nom=("Twitter-test")
    f.nom_colonne_forme="Word"
    f.nom_colonne_freq="TwitterFreqPm"
    #f.extraire()
    f.creer_fichier_sqlite()
    print("Durée:",str(time()-t0))

    t0=time()
    print("Test3: Agrégation dans une base")
    print("*"*30)
    d=base_freqlex()
    d.ajoute_bddl(b)
    d.ajoute_bddl(f)
    d.sauvegarde("base_test")
    e=base_freqlex()
    e.lecture("base_test")
    print("Durée:",str(time()-t0))

    
