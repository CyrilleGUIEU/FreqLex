# coding: utf8
import sqlite3
import pickle

#Ouverture du fichier au format utf8 et chargement des entrées -> lecture
print("Lecture du fichier de lexique.")
lexique_complet=open("Lexique381.txt",encoding='utf8')
lecture=lexique_complet.readlines()

#Sélection des entrées pertinentes -> entrees
graphemes=[]
dernier_grapheme=""
premier=True
for ligne in lecture:
    ligne=ligne.split("\t")
    if not premier:
        #0->graphemes
        #8->freq livres
        #9->freq films
        #une_entree=[ligne[0],ligne[9]+ligne[8]]
        #entrees.append(une_entree)
        g,freq=ligne[0],float(ligne[9])+float(ligne[8])
        if g==dernier_grapheme:
            graphemes[-1][1]=graphemes[-1][1]+freq
        else:
            graphemes=graphemes+[[g,freq]]
            dernier_grapheme=g
        if len(graphemes)%1000==0:
            print(len(graphemes))
    else:
        premier=False
#On ferme de fichier
lexique_complet.close()

#test
#print(entrees[12])

print("Traitement des données.")


#Création d'une base de données en mémoire
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
#Création de la table
cursor.execute("""
CREATE TABLE IF NOT EXISTS lexique(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     ortho TEXT,
     freq REAL
)
""")
#La table est remplie avec les "entrees"
cursor.executemany("""
INSERT INTO lexique(ortho,freq) VALUES(?, ?)""", graphemes)
#On trie par fréquence décroissante
lexique_classe=cursor.execute('SELECT * FROM lexique ORDER BY freq DESC')
conn.commit()
#On récupère les données -> lexique
lexique=[]
for row in lexique_classe:
    lexique.append(row[1])
#Fermeture de la base
conn.close()

#Calcul du nombre d'entrées
taille_lexique=len(lexique)
print("Il y a "+str(taille_lexique)+" mots dans ce lexique.")

#Sauvegarde de la liste
with open('freqlex.dat', 'wb') as fp:
    pickle.dump(lexique, fp)

#Cette fonction renvoie la position du mot dans la liste
def rang_mot(mot):
    if mot in lexique:
        return(lexique.index(mot))
    else:
        return(None)
    

if __name__=="__main__":
    print("test:")
    for i in range(100):
        print(str(i)+"->"+lexique[i])
    while True:
        mot=input("Entrer un mot:")
        r=rang_mot(mot)
        if r!=None:
            print(r)
        else:
            print("Le mot "+mot+" n'est pas dans le lexique.")


